"""Convert generated HTML pages into editable Markdown without extra tooling."""

from html import unescape
from pathlib import Path
import re


def _text(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def _section(html: str, class_name: str) -> str:
    """Extract a balanced element, including nested divs and comments."""
    opening = re.search(rf'<(div|article|section)\b[^>]*class="[^"]*\b{class_name}\b[^"]*"[^>]*>', html, flags=re.I | re.S)
    if not opening:
        return ""
    tag = opening.group(1)
    tokens = re.compile(rf'</?{tag}\b[^>]*>', flags=re.I)
    depth = 1
    for token in tokens.finditer(html, opening.end()):
        if token.group(0).startswith(f"</{tag}"):
            depth -= 1
        elif not token.group(0).rstrip().endswith("/>"):
            depth += 1
        if depth == 0:
            return html[opening.end():token.start()]
    return ""


def _convert(html: str) -> str:
    # Generated HTML is valid Markdown because Markdown permits raw HTML.
    # Keeping it raw preserves tables, comments, code blocks, and attributes.
    return html.strip() + "\n"


def _write(path: Path, metadata: list[str], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + "\n".join(metadata) + "\n---\n\n" + body, encoding="utf-8")


def migrate_existing_site(root: Path) -> None:
    for page in sorted((root / "posts").glob("*/index.html")):
        html = page.read_text(encoding="utf-8")
        article = _section(html, "post")
        if not article:
            continue
        title_match = re.search(r"<h1[^>]*>(.*?)</h1>", article, re.S)
        title = _text(title_match.group(1)) if title_match else page.parent.name
        muted = re.search(r'class="muted"[^>]*>(.*?)</p>', article, re.S)
        date_text = _text(muted.group(1)).replace("Published: ", "").split("|")[0].strip() if muted else ""
        tags = re.findall(r'class="tag"[^>]*>(.*?)</span>', article, re.S)
        slug = page.parent.name
        body_html = _section(article, "post-body")
        first_paragraph = re.search(r"<p[^>]*>(.*?)</p>", body_html, re.S)
        summary = _text(first_paragraph.group(1))[:240] if first_paragraph else ""
        _write(root / "content" / "posts" / f"{slug}.md", [f"Title: {title}", f"Slug: {slug}", f"Date: {date_text}", f"Summary: {summary}", "Tags:", *[f"  - {_text(tag)}" for tag in tags]], _convert(body_html))

    for page in sorted((root / "projects").glob("*/index.html")):
        html = page.read_text(encoding="utf-8")
        article = _section(html, "project")
        if not article:
            continue
        slug = page.parent.name
        title_match = re.search(r"<h1[^>]*>(.*?)</h1>", article, re.S)
        title = _text(title_match.group(1)) if title_match else slug.replace("-", " ").title()
        meta = re.findall(r'<span[^>]*>(.*?)</span>', _section(article, "project-meta"), re.S)
        skills = _text(_section(article, "project-skills")).replace("·", ",")
        body_html = _section(article, "project-body")
        summary_match = re.search(r"<p[^>]*>(.*?)</p>", body_html, re.S)
        summary = _text(summary_match.group(1)) if summary_match else ""
        _write(root / "content" / "projects" / f"{slug}.md", [f"Title: {title}", f"Slug: {slug}", f"Project Type: {_text(meta[0]) if meta else 'Personal Project'}", f"Duration: {_text(meta[1]) if len(meta) > 1 else ''}", f"Summary: {summary}", f"Skills: {skills}", f"Image: {slug}.jpg"], _convert(body_html))

    about = root / "about" / "index.html"
    if about.exists():
        html = about.read_text(encoding="utf-8")
        _write(root / "content" / "pages" / "about.md", ["Title: About Me", "Slug: about"], _convert(_section(html, "about-text")))
