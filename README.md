# ArXiv Paper Page Skill

Reusable Codex skill for turning an arXiv paper, local PDF, or paper workspace into a static GitHub Pages project page.

This repository contains only the reusable skill package, not a single paper instance.

## Contents

- `skills/arxiv-paper-page/`: the installable skill
- `skills/arxiv-paper-page/scripts/bootstrap_project_page.py`: bootstrap script for a target paper repository
- `skills/arxiv-paper-page/assets/starter-site/`: static site starter template

## What the skill does

The skill helps Codex:

- extract paper metadata, structure, and figures from arXiv/PDF/source material
- scaffold a static `docs/` project page
- generate a clean `release/github-pages-subpage/` package for GitHub Pages
- avoid publishing LaTeX sources when the public site should expose only the web page and `paper.pdf`

## Install for Codex

Clone this repository, then copy the skill into your local Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/arxiv-paper-page ~/.codex/skills/
```

## Use in a paper repository

Ask Codex:

```text
Use $arxiv-paper-page to turn this arXiv paper into a GitHub Pages project page.
```

Or run the bootstrap script directly:

```bash
python3 skills/arxiv-paper-page/scripts/bootstrap_project_page.py /path/to/target-repo --pdf /path/to/paper.pdf
```

This creates:

- `docs/`
- `docs/paper-page.config.json`
- `release/github-pages-subpage/`
- `scripts/sync_release_package.sh`

Then fill the paper content in:

- `docs/paper-page.config.json`
- `docs/assets/`

## Notes

- The generated site is static HTML/CSS/JS and GitHub Pages-friendly.
- The visual direction is warm and editorial, but the primary goal is paper readability.
- Google Scholar live citation counts are intentionally not included.

## License

This repository is licensed under the MIT License. See [LICENSE](/Users/muyi/Documents/arxiv-paper-page-skill/LICENSE).
