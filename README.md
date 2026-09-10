# shrishtinigam.github.io

## New content workflow

Write posts and projects as Markdown files in `content/posts/` and
`content/projects/`. Put front matter at the top of each file:

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

Images can be placed in `static/images/` and referenced from Markdown:

```markdown
![Architecture diagram](/static/images/architecture.png)
```

Run `make check` to validate and list the documents. To rebuild the site:

```bash
make build
```

The generated site is written to `output/`. The existing visual templates are
kept in `templates/`, and the first migration can be repeated with:

```bash
make migrate
```

GitHub Actions builds and deploys `output/` through GitHub Pages. Enable
**Settings → Pages → Source: GitHub Actions** once in the repository settings.
