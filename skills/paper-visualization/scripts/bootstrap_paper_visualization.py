#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

DEFAULT_SITE_DIR = "docs"
DEFAULT_LOCALE_DIR = "zh"
DEFAULT_RELEASE_DIR = "release/site-package"
DEFAULT_CONFIG_NAME = "paper-visualization.config.json"
DEFAULT_PDF_NAME = "paper.pdf"


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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_language_switch(page: str, bilingual: bool, locale_dir: str) -> dict | None:
    if not bilingual:
        return None

    if page == "zh":
        return {
            "aria_label": "Language switch",
            "links": [
                {"label": "EN", "href": "../"},
                {"label": "中文", "href": "./", "active": True},
            ],
        }

    return {
        "aria_label": "Language switch",
        "links": [
            {"label": "EN", "href": "./", "active": True},
            {"label": "中文", "href": f"{locale_dir}/"},
        ],
    }


def localize_seed_config_for_zh(config: dict) -> None:
    site = config.setdefault("site", {})
    summary = config.setdefault("summary", {})
    citation = config.setdefault("citation", {})

    if site.get("links"):
        labels = ["论文 PDF", "预印本", "BibTeX"]
        for link, label in zip(site["links"], labels):
            link["label"] = label

    summary["kicker"] = "概览"
    summary["nav_label"] = "概览"
    summary["title"] = "这篇论文的核心贡献"

    citation["kicker"] = "引用"
    citation["nav_label"] = "引用"
    citation["title"] = "引用本文"
    citation["button_label"] = "复制 BibTeX"
    citation["copied_label"] = "已复制"
    citation["error_label"] = "复制失败"

    section_labels = {
        "abstract": ("摘要", "摘要"),
        "framework": ("框架", "框架"),
        "evaluation": ("评测", "评测"),
    }
    for section in config.get("sections", []):
        if section.get("id") in section_labels:
            nav_label, kicker = section_labels[section["id"]]
            section["nav_label"] = nav_label
            section["kicker"] = kicker


def apply_bootstrap_defaults(
    config: dict,
    *,
    page: str,
    bilingual: bool,
    public_url: str | None,
    locale_dir: str,
) -> dict:
    seeded = json.loads(json.dumps(config))
    site = seeded.setdefault("site", {})

    site["lang"] = "zh-CN" if page == "zh" else "en"
    site.setdefault("theme_color", "#faf9f5")
    site.setdefault("meta_description", site.get("subtitle", "Static paper visualization site"))
    site.setdefault("brand_home_url", "#top")
    site.setdefault("brand_aria_label", "Back to top")
    site.setdefault("show_brand_mark", False)

    if page == "zh":
        localize_seed_config_for_zh(seeded)

    language_switch = build_language_switch(page, bilingual, locale_dir)
    if language_switch:
        site["language_switch"] = language_switch

    if public_url:
        base = public_url.rstrip("/")
        root_url = f"{base}/"
        localized_url = f"{base}/{locale_dir}/"
        page_url = localized_url if page == "zh" else root_url

        site["canonical_url"] = page_url
        site["og_url"] = page_url
        site.setdefault("alternates", [])

        alternates = [{"hreflang": "en", "href": root_url}]
        if bilingual:
            alternates.append({"hreflang": "zh-CN", "href": localized_url})
        alternates.append({"hreflang": "x-default", "href": root_url})
        site["alternates"] = alternates

        if site.get("language_switch", {}).get("links"):
            if page == "zh":
                site["language_switch"]["links"] = [
                    {"label": "EN", "href": root_url},
                    {"label": "中文", "href": localized_url, "active": True},
                ]
            else:
                links = [{"label": "EN", "href": root_url, "active": True}]
                if bilingual:
                    links.append({"label": "中文", "href": localized_url})
                site["language_switch"]["links"] = links

    return seeded


def write_sync_script(
    repo_root: Path,
    *,
    site_dir: str,
    release_dir: str,
    config_name: str,
    locale_dir: str,
) -> None:
    scripts_dir = repo_root / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    sync_script = scripts_dir / "sync_site_package.sh"
    sync_script.write_text(
        "#!/usr/bin/env bash\n\n"
        "set -euo pipefail\n\n"
        'ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"\n'
        f'SRC_DIR="$ROOT_DIR/{site_dir}/"\n'
        f'DST_DIR="$ROOT_DIR/{release_dir}/"\n\n'
        'if [ -f "$ROOT_DIR/scripts/materialize_page_metadata.py" ]; then\n'
        f'  python3 "$ROOT_DIR/scripts/materialize_page_metadata.py" "$SRC_DIR" --config-name "{config_name}" --locale-dir "{locale_dir}"\n'
        "fi\n\n"
        'mkdir -p "$DST_DIR"\n'
        'rsync -av --delete "$SRC_DIR" "$DST_DIR"\n\n'
        'echo "Site package synced to: $DST_DIR"\n',
        encoding="utf-8",
    )
    sync_script.chmod(0o755)


def scaffold_page_dir(
    page_dir: Path,
    starter_root: Path,
    config_template: dict,
    *,
    page: str,
    bilingual: bool,
    public_url: str | None,
    locale_dir: str,
    config_name: str,
    force: bool,
) -> None:
    page_dir.mkdir(parents=True, exist_ok=True)

    for name in ["index.html", "styles.css", "script.js"]:
        copy_if_missing(starter_root / name, page_dir / name, force)

    assets_dir = page_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    seeded_config = apply_bootstrap_defaults(
        config_template,
        page=page,
        bilingual=bilingual,
        public_url=public_url,
        locale_dir=locale_dir,
    )
    config_path = page_dir / config_name
    if not config_path.exists() or force:
        write_json(config_path, seeded_config)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a starter static paper-visualization scaffold."
    )
    parser.add_argument("repo_root", help="Target repository root")
    parser.add_argument("--pdf", help="Optional paper PDF to copy into the primary site root as paper.pdf")
    parser.add_argument(
        "--public-url",
        help="Optional final public base URL for the primary route, used to seed canonical and alternate links",
    )
    parser.add_argument(
        "--bilingual",
        action="store_true",
        help="Create both the primary route and a localized route with separate configs",
    )
    parser.add_argument(
        "--site-dir",
        default=DEFAULT_SITE_DIR,
        help=f"Primary site directory under the target repository (default: {DEFAULT_SITE_DIR})",
    )
    parser.add_argument(
        "--locale-dir",
        default=DEFAULT_LOCALE_DIR,
        help=f"Localized route directory name when --bilingual is used (default: {DEFAULT_LOCALE_DIR})",
    )
    parser.add_argument(
        "--release-dir",
        default=DEFAULT_RELEASE_DIR,
        help=f"Release package directory under the target repository (default: {DEFAULT_RELEASE_DIR})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing starter-site files if they already exist",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    starter_root = skill_root / "assets" / "starter-site"
    config_template = load_json(skill_root / "assets" / "paper-visualization.config.template.json")
    metadata_script_src = skill_root / "assets" / "repo-scripts" / "materialize_page_metadata.py"

    repo_root = Path(args.repo_root).resolve()
    site_dir = repo_root / args.site_dir
    localized_dir = site_dir / args.locale_dir
    release_dir = repo_root / args.release_dir
    scripts_dir = repo_root / "scripts"

    site_dir.mkdir(parents=True, exist_ok=True)
    release_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)

    scaffold_page_dir(
        site_dir,
        starter_root,
        config_template,
        page="en",
        bilingual=args.bilingual,
        public_url=args.public_url,
        locale_dir=args.locale_dir,
        config_name=DEFAULT_CONFIG_NAME,
        force=args.force,
    )

    if args.bilingual:
        scaffold_page_dir(
            localized_dir,
            starter_root,
            config_template,
            page="zh",
            bilingual=True,
            public_url=args.public_url,
            locale_dir=args.locale_dir,
            config_name=DEFAULT_CONFIG_NAME,
            force=args.force,
        )

    copy_if_missing(
        metadata_script_src,
        scripts_dir / "materialize_page_metadata.py",
        args.force,
    )
    (scripts_dir / "materialize_page_metadata.py").chmod(0o755)

    if args.pdf:
        pdf_src = Path(args.pdf).resolve()
        if not pdf_src.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_src}")
        shutil.copy2(pdf_src, site_dir / DEFAULT_PDF_NAME)

    write_sync_script(
        repo_root,
        site_dir=args.site_dir,
        release_dir=args.release_dir,
        config_name=DEFAULT_CONFIG_NAME,
        locale_dir=args.locale_dir,
    )
    print(f"Starter paper-visualization scaffold created under: {repo_root}")
    print("Next steps:")
    print(f"1. Edit {args.site_dir}/{DEFAULT_CONFIG_NAME}")
    if args.bilingual:
        print(f"2. Translate and edit {args.site_dir}/{args.locale_dir}/{DEFAULT_CONFIG_NAME}")
        print(f"3. Add public figures under {args.site_dir}/assets/")
        print("4. Preview with: python3 -m http.server 8123")
        print("5. Sync the site package with: ./scripts/sync_site_package.sh")
    else:
        print(f"2. Add public figures under {args.site_dir}/assets/")
        print("3. Preview with: python3 -m http.server 8123")
        print("4. Sync the site package with: ./scripts/sync_site_package.sh")


if __name__ == "__main__":
    main()
