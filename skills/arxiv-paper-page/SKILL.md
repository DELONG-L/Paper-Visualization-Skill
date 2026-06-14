---
name: arxiv-paper-page
description: 'Turn an arXiv paper, local PDF, or LaTeX paper workspace into a GitHub Pages project page using a warm, readability-first template and a structured config file. Use when Codex needs to: (1) extract paper metadata, claims, and figures from arXiv/PDF/source materials, (2) scaffold a `docs/` website plus a clean public release package, (3) fill or update `paper-page.config.json`, or (4) prepare a paper website that does not expose LaTeX source files.'
---

# arXiv Paper Page

## Overview

Create a paper project page that prioritizes research communication over style mimicry.
Borrow warm color and typography cues when useful, but keep the page optimized for title clarity, contribution scanning, figure support, and GitHub Pages deployment.

## Workflow

### 1. Collect paper inputs

Start from the strongest available materials:

- arXiv abstract page or PDF
- local paper PDF
- local LaTeX source tree if available
- core figures that should appear on the page

Use LaTeX sources to extract structure when helpful, but do not publish them unless the user explicitly wants that.

### 2. Decide the publication boundary

Prefer a split between:

- paper-authoring workspace, which may contain LaTeX and private drafting material
- public website package, which should contain only website assets and `paper.pdf`

If the user does not want to expose LaTeX, keep the public deliverable limited to the website package.

### 3. Bootstrap the site scaffold

Run the bootstrap script from this skill to create a reusable starter layout:

```bash
python3 scripts/bootstrap_project_page.py /path/to/repo --pdf /path/to/paper.pdf
```

This creates:

- `docs/` with starter site files
- `docs/paper-page.config.json`
- `release/github-pages-subpage/`
- `scripts/sync_release_package.sh`

Read [references/config-schema.md](references/config-schema.md) before editing the config.

### 4. Fill the paper config

Edit `docs/paper-page.config.json` to define:

- paper title, subtitle, authors, affiliations, and links
- hero facts
- summary cards
- section-by-section content
- citation block

Use the example config in [assets/paper-page.config.template.json](assets/paper-page.config.template.json) as the starting point.

When translating the paper into web content, follow [references/workflow.md](references/workflow.md).

### 5. Add figures and public assets

Copy only public assets into `docs/assets/`:

- overview figures
- lifecycle or pipeline diagrams
- representative plots or tables rendered as images

Keep the page visually warm and editorial, but do not let branding or visual flourish reduce readability.
Prefer a direct title, concise summary text, and figures that support the paper's core claims.

### 6. Preview and refine

Preview locally:

```bash
python3 -m http.server 8123
```

Then open:

```text
http://127.0.0.1:8123/docs/
```

Check these first:

- title and author block are immediately legible
- first screen explains what the paper is about
- body text width remains readable
- section order matches the paper's logic
- figures appear where they help comprehension

### 7. Create the clean public package

After editing `docs/`, refresh the public release package:

```bash
./scripts/sync_release_package.sh
```

Publish `release/github-pages-subpage/` when the user wants a public package with no LaTeX source exposure.

## Design rules

- Prioritize paper communication first, visual taste second.
- Use warm neutrals, serif headlines, and restrained accent color as style cues only.
- Prefer explicit paper title over abstract slogans.
- Prefer representative figures over decorative hero art.
- Keep section copy shorter than the paper, but faithful to its claims.
- Treat GitHub Pages compatibility as a hard constraint: static HTML, CSS, JS, and local assets.

## Resources

### scripts/

- [scripts/bootstrap_project_page.py](scripts/bootstrap_project_page.py): Create a starter paper-page scaffold inside a target repository.

### references/

- [references/workflow.md](references/workflow.md): Content and design workflow for turning a paper into a readable project page.
- [references/config-schema.md](references/config-schema.md): Field-by-field guide for `paper-page.config.json`.

### assets/

- [assets/paper-page.config.template.json](assets/paper-page.config.template.json): Example config file.
- [assets/starter-site/](assets/starter-site): Generic static site template driven by `paper-page.config.json`.
