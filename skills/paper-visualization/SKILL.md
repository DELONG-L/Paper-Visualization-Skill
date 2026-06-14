---
name: paper-visualization
description: 'Turn a paper PDF, preprint page, or source workspace into a readable static paper visualization using a structured config, optional bilingual routes, and a fallback path to direct HTML/CSS/JS editing. Use when Codex needs to: (1) extract paper metadata, claims, and figures from PDF/web/source materials, (2) scaffold a default web root plus a portable static site package, (3) build or update bilingual routes such as `docs/` and `docs/zh/`, (4) materialize canonical metadata such as descriptions, alternates, and sitemap entries, or (5) prepare a public paper presentation without exposing authoring sources.'
---

# Paper Visualization

## Overview

Create a paper visualization that prioritizes research communication over style mimicry.
Borrow warm color and typography cues when useful, but optimize first for title clarity, contribution scanning, figure support, multilingual routing when needed, and clean static delivery.

Treat homepage integration as optional. The core job of this skill is to ship a strong standalone paper visualization.

## Workflow

### 1. Collect paper inputs

Start from the strongest available materials:

- publisher page, preprint page, or paper landing page
- local paper PDF
- local LaTeX source tree if available
- core figures that should appear on the page

Use LaTeX sources to extract structure when helpful, but do not publish them unless the user explicitly wants that.

### 2. Decide the publication boundary

Prefer a split between:

- paper-authoring workspace, which may contain LaTeX and private drafting material
- public site package, which should contain only public assets, static HTML/CSS/JS, and `paper.pdf`

If the user does not want to expose LaTeX, keep the public deliverable limited to the website package.

### 3. Bootstrap the site scaffold

Run the bootstrap script from this skill:

```bash
python3 scripts/bootstrap_paper_visualization.py /path/to/repo --pdf /path/to/paper.pdf
```

Useful flags:

```bash
python3 scripts/bootstrap_paper_visualization.py /path/to/repo \
  --pdf /path/to/paper.pdf \
  --bilingual \
  --public-url https://example.com/publications/my-paper/ \
  --site-dir docs \
  --release-dir release/site-package
```

This creates:

- `docs/` with starter site files by default
- `docs/paper-visualization.config.json`
- `docs/zh/` plus `docs/zh/paper-visualization.config.json` when `--bilingual` is used
- `release/site-package/`
- `scripts/materialize_page_metadata.py`
- `scripts/sync_site_package.sh`

Read [references/config-schema.md](references/config-schema.md) before editing configs.

### 4. Fill the paper config

Edit `docs/paper-visualization.config.json` to define:

- paper title, subtitle, authors, affiliations, and links
- page metadata such as description, canonical URL, OG image, and alternates
- hero facts
- summary cards
- section-by-section content and layout
- citation block

If the site is bilingual, repeat the process for `docs/zh/paper-visualization.config.json`.

Use the example config in [assets/paper-visualization.config.template.json](assets/paper-visualization.config.template.json) as the starting point.

When translating the paper into web content, follow [references/workflow.md](references/workflow.md).

### 5. Add figures and public assets

Copy only public assets into `docs/assets/`:

- overview figures
- taxonomy, lifecycle, or pipeline diagrams
- representative plots or tables rendered as images

If the page is bilingual, prefer sharing the same public figures across routes rather than duplicating them.

### 6. Choose the right layout fidelity

Start with the config-driven template, but do not force every paper into the same structure.

Use the richer built-in section layouts first:

- `framework`
- `lifecycle`
- `showcase`
- `stats`
- `split`

If the page still needs stronger section-specific presentation after config edits, promote the generated page from "starter template" to "custom static page" and edit the HTML/CSS/JS directly.

Do not cling to the config abstraction when it reduces readability.

### 7. Preview and refine

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
- no mobile header or icon issue harms readability

If the site is bilingual, check both:

- `http://127.0.0.1:8123/docs/`
- `http://127.0.0.1:8123/docs/zh/`

### 8. Materialize metadata and release the public package

After editing configs and assets, refresh the public release package:

```bash
./scripts/sync_site_package.sh
```

This first materializes static metadata into the HTML head and writes `sitemap.xml`, then syncs the default site root into `release/site-package/`.

Publish `release/site-package/` when the user wants a clean static bundle with no LaTeX source exposure.

## Design rules

- Prioritize paper communication first, visual taste second.
- Use warm neutrals, serif headlines, and restrained accent color as style cues only.
- Prefer the exact paper title over abstract slogans.
- Prefer representative figures over decorative hero art.
- Keep section copy shorter than the paper, but faithful to its claims.
- Keep the default output host-agnostic: static HTML, CSS, JS, local assets, and relative paths.
- Keep formal author names unchanged across language routes unless the user explicitly requests localization.
- Treat subpath deployment as a convenient default, not the organizing principle.

## Resources

### scripts/

- [scripts/bootstrap_paper_visualization.py](scripts/bootstrap_paper_visualization.py): Create a starter paper-visualization scaffold inside a target repository.

### references/

- [references/workflow.md](references/workflow.md): Content and design workflow for turning a paper into a readable visualization.
- [references/config-schema.md](references/config-schema.md): Field-by-field guide for `paper-visualization.config.json`.

### assets/

- [assets/paper-visualization.config.template.json](assets/paper-visualization.config.template.json): Example config file.
- [assets/starter-site/](assets/starter-site): Static site starter template driven by `paper-visualization.config.json`.
- `assets/repo-scripts/materialize_page_metadata.py`: Copied into the target repo to materialize page metadata before release sync.
