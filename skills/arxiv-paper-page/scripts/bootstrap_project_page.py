#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def write_sync_script(repo_root: Path) -> None:
    scripts_dir = repo_root / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    sync_script = scripts_dir / "sync_release_package.sh"
    sync_script.write_text(
        "#!/usr/bin/env bash\n\n"
        "set -euo pipefail\n\n"
        'ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"\n'
        'SRC_DIR="$ROOT_DIR/docs/"\n'
        'DST_DIR="$ROOT_DIR/release/github-pages-subpage/"\n\n'
        'mkdir -p "$DST_DIR"\n'
        'rsync -av --delete "$SRC_DIR" "$DST_DIR"\n\n'
        'echo "Release package synced to: $DST_DIR"\n',
        encoding="utf-8",
    )
    sync_script.chmod(0o755)


def copy_if_missing(src: Path, dst: Path, force: bool) -> None:
    if dst.exists():
        if not force:
            return
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a starter GitHub Pages paper project page scaffold."
    )
    parser.add_argument("repo_root", help="Target repository root")
    parser.add_argument("--pdf", help="Optional paper PDF to copy into docs/paper.pdf")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing starter-site files if they already exist",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    starter_root = skill_root / "assets" / "starter-site"
    config_template = skill_root / "assets" / "paper-page.config.template.json"

    repo_root = Path(args.repo_root).resolve()
    docs_dir = repo_root / "docs"
    release_dir = repo_root / "release" / "github-pages-subpage"

    docs_dir.mkdir(parents=True, exist_ok=True)
    release_dir.mkdir(parents=True, exist_ok=True)

    for name in ["index.html", "styles.css", "script.js", ".nojekyll"]:
        copy_if_missing(starter_root / name, docs_dir / name, args.force)

    assets_dst = docs_dir / "assets"
    assets_dst.mkdir(parents=True, exist_ok=True)

    copy_if_missing(
        config_template,
        docs_dir / "paper-page.config.json",
        args.force,
    )

    if args.pdf:
        pdf_src = Path(args.pdf).resolve()
        if not pdf_src.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_src}")
        shutil.copy2(pdf_src, docs_dir / "paper.pdf")

    write_sync_script(repo_root)
    print(f"Starter project page scaffold created under: {repo_root}")
    print("Next steps:")
    print("1. Edit docs/paper-page.config.json")
    print("2. Add public figures under docs/assets/")
    print("3. Preview with: python3 -m http.server 8123")
    print("4. Sync release package with: ./scripts/sync_release_package.sh")


if __name__ == "__main__":
    main()
