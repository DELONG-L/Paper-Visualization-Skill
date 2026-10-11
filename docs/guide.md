# User guide

[Back to README](../README.md) · [简体中文](guide.zh-CN.md)

Run commands from the repository root.

# Paper Visualization

Reusable Codex skill for turning a paper PDF, preprint page, or source workspace into a readable static visualization site.

## Repository Layout

- `skills/paper-visualization/`: the installable skill
- `skills/paper-visualization/scripts/bootstrap_paper_visualization.py`: starter scaffold generator
- `skills/paper-visualization/assets/starter-site/`: static site template
- `skills/paper-visualization/assets/repo-scripts/materialize_page_metadata.py`: metadata materializer copied into target repos

## Core Principles

- Paper communication first, visual taste second
- Start from structured config, then promote to direct HTML/CSS/JS editing when the paper needs tighter composition
- Support bilingual routes when the paper benefits from them
- Keep the default output static and host-agnostic
- Avoid exposing authoring sources unless the user explicitly wants them public

## Install For Codex

```bash
git clone https://github.com/DELONG-L/Paper-Visualization-Skill.git
cd Paper-Visualization-Skill
mkdir -p ~/.codex/skills
cp -R skills/paper-visualization ~/.codex/skills/
```

## Use

Ask Codex:

```text
Use $paper-visualization to turn this paper into a readable static visualization site.
```

Or run the scaffold script directly:

```bash
python3 skills/paper-visualization/scripts/bootstrap_paper_visualization.py /path/to/target-repo --pdf /path/to/paper.pdf
```

Example with bilingual routes and seeded public URLs:

```bash
python3 skills/paper-visualization/scripts/bootstrap_paper_visualization.py /path/to/target-repo \
  --pdf /path/to/paper.pdf \
  --bilingual \
  --public-url https://example.com/publications/my-paper/
```

The default scaffold creates:

- `docs/`
- `docs/paper-visualization.config.json`
- `docs/zh/` and `docs/zh/paper-visualization.config.json` when `--bilingual` is used
- `release/site-package/`
- `scripts/materialize_page_metadata.py`
- `scripts/sync_site_package.sh`

The `docs/` root is only a default packaging choice. The generated site can be published from any static host, and the scaffold supports alternate site and release directories.

## Notes

- The starter template includes richer academic layouts such as `framework`, `lifecycle`, `showcase`, and `stats`.
- If the config schema starts fighting the paper, switch to direct HTML/CSS/JS editing.
- Live citation scraping is intentionally out of scope.

## License

MIT. See [LICENSE](../LICENSE).
