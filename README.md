# shrishtinigam.github.io — deployment repository

This repository hosts the GitHub Pages workflow for
**https://shrishtinigam.github.io/**. Edit your website in
**[github-pages-ssg](https://github.com/shrishtinigam/github-pages-ssg)**.
Its README covers setup, spg dev, authoring, and publishing.

## What deploys

.github/workflows/deploy.yml runs on a push to this repository's main or a
workflow-dispatch request. It checks out github-pages-ssg/main into .ssg/,
installs its constrained Python dependencies, validates, builds, tests, and
deploys output/ with the official Pages actions. Output is an artifact, not a
new commit or a manual copy operation. The source checkout is fixed for that
run; a later source push triggers another run.

The SSG repository requests this workflow after its main checks pass. Configure
SITE_DEPLOY_TOKEN **in the SSG repository**: a fine-grained token limited to this
repository with Actions read/write access. See the SSG README for exact setup.

In this repository's **Settings → Pages**, verify **Source: GitHub Actions**.
Keep the current domain; check github-pages environment restrictions. For manual
deployment, open **Actions → Build and deploy portfolio → Run workflow**, using
main. Inspect the deploy job before assuming a release succeeded.

## Migration boundary

This workflow now selects SSG **main**, replacing feature/markdown-ssg.
Merge the accompanying SSG changes first. The domain and routes stay the same;
the branch supplying future deployments changes.

The older sitegen/, templates/, content/, static/, Makefile, package files,
tests, and committed root HTML remain as historical migration material.
**The current workflow does not use them.** Editing those copies does not update
canonical source. They have deliberately not been deleted in this audit.
Use the SSG checkout for everyday editing, preview, tests, and exports.

When editing posts or projects, no changes to this repository are needed.
