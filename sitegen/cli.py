import argparse
from pathlib import Path

from .content import load_documents


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the portfolio website.")
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("--content", type=Path, default=Path("content"))
    args = parser.parse_args()

    documents = load_documents(args.content)
    if args.command == "check":
        for document in documents:
            print(f"OK  {document.kind:8} {document.url}  {document.source}")
        print(f"Checked {len(documents)} Markdown documents.")
        return

    raise SystemExit("The HTML rendering pipeline will be added in the next migration part.")


if __name__ == "__main__":
    main()
