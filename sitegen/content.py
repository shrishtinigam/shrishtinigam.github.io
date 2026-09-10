from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

import frontmatter
import markdown


@dataclass(frozen=True)
class Document:
    """A Markdown document plus its front matter and rendered HTML."""

    kind: str
    source: Path
    metadata: dict[str, Any]
    body_markdown: str
    body_html: str

    @property
    def slug(self) -> str:
        return str(self.metadata.get("slug") or self.source.stem)

    @property
    def url(self) -> str:
        return f"/{self.kind}/{self.slug}/"


def load_documents(content_dir: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(content_dir.glob("**/*.md")):
        kind = path.parent.name
        post = frontmatter.load(path)
        metadata = dict(post.metadata)
        metadata.setdefault("slug", path.stem)
        documents.append(
            Document(
                kind=kind,
                source=path,
                metadata=metadata,
                body_markdown=post.content,
                body_html=markdown.markdown(
                    post.content,
                    extensions=["extra", "fenced_code", "codehilite", "toc"],
                ),
            )
        )
    return documents


def parse_date(value: Any) -> Optional[date]:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    return None
