# shrishtinigam.github.io

## New content workflow

Write posts and projects as Markdown files in `content/posts/` and
`content/projects/`. Put front matter at the top of each file.

For a blog post:

```markdown
Title: My project
Slug: my-project
Date: 2025-01-01
Summary: A short description.
Tags:
  - python
  - systems

The page body goes here.
```

For a project:

```markdown
Title: My project
Slug: my-project
Project Type: Personal Project
Duration: 2025
Summary: A short card description.
Skills: Python, Docker, PostgreSQL
Image: my-project.jpg

## Overview

Project details go here.
```

Images can be placed in `content/images/` and referenced from Markdown:

```markdown
![Architecture diagram](/static/images/architecture.png)
```

Images placed in `content/posts/images/`, `content/projects/images/`, or
`content/pages/images/` are also copied automatically to the generated site.

Run `make check` to validate and list the documents. To rebuild the site:

```bash
make build
```

The generated files are written to `output/`; do not edit that directory by
hand. Edit Markdown, templates, or static assets instead.

## Local setup

Use a virtual environment on a fresh machine:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m sitegen.cli check
.venv/bin/python -m unittest discover -s tests -v
```

The current design is intentionally kept in `templates/` and
`static/css/style.css`. Change those only when you intend to change the visual
appearance of the published site.

The generated site is written to `output/`. The existing visual templates are
kept in `templates/`, and the first migration can be repeated with:

```bash
make migrate
```

GitHub Actions builds and deploys `output/` through GitHub Pages. Enable
**Settings → Pages → Source: GitHub Actions** once in the repository settings.
