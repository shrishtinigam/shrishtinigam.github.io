import shutil
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .content import Document, load_documents


SITE_TITLE = "shrishtinigam.github.io"
BASE_URL = "https://shrishtinigam.github.io"
AUTHOR = "Meher Shrishti Nigam"
DESCRIPTION = "Performance, Projects, Perspective"


def _rendered(document: Document) -> dict:
    metadata = dict(document.metadata)
    metadata["kind"] = document.kind
    metadata["body_html"] = document.body_html
    metadata["title"] = metadata.get("title", document.slug)
    metadata["summary_html"] = markdown.markdown(str(metadata.get("summary", "")))
    metadata["created_at"] = metadata.get("date", "")
    metadata["updated_at"] = metadata.get("updated", "")
    metadata["tags"] = metadata.get("tags", []) or []
    if isinstance(metadata["tags"], str):
        metadata["tags"] = [tag.strip() for tag in metadata["tags"].split(",") if tag.strip()]
    return metadata


def build(root: Path, output: Path) -> None:
    documents = [_rendered(document) for document in load_documents(root / "content")]
    posts = [item for item in documents if item.get("kind", "") == "posts"]
    projects = [item for item in documents if item.get("kind", "") == "projects"]
    pages = [item for item in documents if item.get("kind", "") == "pages"]
    for item in documents:
        if "project_type" in item:
            item["project_type"] = item.pop("project_type")
        item["slug"] = item.get("slug", "")
        item["link"] = item.get("link")
        item["image"] = item.get("image", f"{item['slug']}.jpg")
        item["description_html"] = item.get("body_html", "")
        item["summary"] = item.get("summary", "")
        item["skills"] = item.get("skills", "")
    env = Environment(loader=FileSystemLoader(str(root / "templates")), autoescape=select_autoescape(["html", "xml"]))
    context = {"site_title": SITE_TITLE, "base_url": BASE_URL, "author": AUTHOR, "description": DESCRIPTION, "posts": posts, "projects": projects}
    if output.exists():
        shutil.rmtree(output)
    (output / "static").mkdir(parents=True)
    shutil.copytree(root / "static", output / "static", dirs_exist_ok=True)
    (output / ".nojekyll").touch()
    for filename in ("robots.txt", "sitemap.xml"):
        source = root / filename
        if source.exists():
            shutil.copy2(source, output / filename)

    def write(template: str, relative: str, **extra) -> None:
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        render_context = {**context, **extra}
        destination.write_text(env.get_template(template).render(**render_context), encoding="utf-8")

    write("index.html", "index.html")
    about = next((page for page in pages if page.get("slug") == "about"), {"body_html": ""})
    write("about.html", "about/index.html", about_html=about["body_html"])
    write("posts.html", "posts/index.html", posts=sorted(posts, key=lambda item: str(item.get("date", "")), reverse=True))
    write("projects.html", "projects/index.html", projects=projects)
    for post in posts:
        write("post.html", f"posts/{post['slug']}/index.html", post=post)
    for project in projects:
        write("project.html", f"projects/{project['slug']}/index.html", project=project)
