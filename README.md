# shrishtinigam.github.io

This repository contains the published GitHub Pages site and its deployment
workflow. The canonical editable Markdown content and Pelican theme now live
in the standalone [github-pages-ssg repository](https://github.com/shrishtinigam/github-pages-ssg).

## Content workflow

Edit Markdown in the SSG repository:

```text
content/posts/       blog posts
content/projects/    project pages
content/pages/       about and collection pages
theme/static/        CSS, JavaScript, fonts, and images
```

Each file uses YAML front matter. For example:

```markdown
---
Title: My post
Slug: my-post
Date: 2025-01-01
Summary: A short description shown on listing pages.
Tags:
  - python
  - systems
---

Write the article in Markdown. Images can be added to the theme static assets
or referenced from the generated static path.
```

Build locally from the SSG repository with `make check`, `make test`, and
`make build`. The build writes to a sibling `pelican-output/` directory, never
inside the generator repository.

## Deployment

GitHub Actions clones the SSG repository's `feature/markdown-ssg` branch,
validates it, runs Pelican, and deploys the generated `output/` artifact to
GitHub Pages. Once the Pelican pull request is merged, update the workflow's
branch reference to `main`.

The existing HTML, CSS, JavaScript, assets, and URL structure are intentionally
preserved while the build system is migrated.
