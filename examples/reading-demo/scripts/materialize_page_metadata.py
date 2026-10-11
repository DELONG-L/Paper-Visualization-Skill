#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from html import escape as html_escape
from pathlib import Path
from xml.sax.saxutils import escape


def replace_html_lang(html: str, lang: str) -> str:
    if re.search(r"<html[^>]*\slang=", html):
        return re.sub(r'(<html[^>]*\slang=")[^"]*(")', rf"\1{lang}\2", html, count=1)
    return re.sub(r"<html", f'<html lang="{lang}"', html, count=1)


def upsert_meta(html: str, attr_name: str, attr_value: str, content: str) -> str:
    pattern = rf'<meta[^>]*{attr_name}="{re.escape(attr_value)}"[^>]*content="[^"]*"[^>]*>'
    replacement = f'<meta {attr_name}="{html_escape(attr_value, quote=True)}" content="{html_escape(content, quote=True)}">'
    if re.search(pattern, html):
        return re.sub(pattern, replacement, html, count=1)
    return html.replace("</head>", f"  {replacement}\n</head>", 1)


def upsert_link(html: str, rel: str, href: str) -> str:
    pattern = rf'<link[^>]*rel="{re.escape(rel)}"[^>]*href="[^"]*"[^>]*>'
    replacement = f'<link rel="{html_escape(rel, quote=True)}" href="{html_escape(href, quote=True)}">'
    if re.search(pattern, html):
        return re.sub(pattern, replacement, html, count=1)
    return html.replace("</head>", f"  {replacement}\n</head>", 1)


def replace_title(html: str, title: str) -> str:
    if re.search(r"<title>.*?</title>", html, flags=re.S):
        return re.sub(r"<title>.*?</title>", f"<title>{html_escape(title)}</title>", html, count=1, flags=re.S)
    return html.replace("</head>", f"  <title>{html_escape(title)}</title>\n</head>", 1)


def replace_generated_alternates(html: str, alternates: list[dict[str, str]]) -> str:
    html = re.sub(r"\n?\s*<link rel=\"alternate\"[^>]*data-generated=\"alternate\"[^>]*>", "", html)
    if not alternates:
        return html

    links = "\n".join(
        f'  <link rel="alternate" hreflang="{html_escape(item["hreflang"], quote=True)}" href="{html_escape(item["href"], quote=True)}" data-generated="alternate">'
        for item in alternates
    )
    return html.replace("</head>", f"{links}\n</head>", 1)


def patch_index_html(index_path: Path, config: dict) -> str | None:
    site = config.get("site", {})
    lang = site.get("lang", "en")
    title = site.get("og_title") or site.get("title") or "Paper visualization"
    description = site.get("meta_description") or site.get("subtitle") or "Static paper visualization site"
    theme_color = site.get("theme_color", "#faf9f5")
    canonical_url = site.get("canonical_url", "")
    og_url = site.get("og_url") or canonical_url
    og_image = site.get("og_image", "")
    og_description = site.get("og_description") or description
    twitter_title = site.get("twitter_title") or title
    twitter_description = site.get("twitter_description") or description
    alternates = site.get("alternates", [])

    html = index_path.read_text(encoding="utf-8")
    html = replace_html_lang(html, lang)
    html = replace_title(html, title)
    html = upsert_meta(html, "name", "description", description)
    html = upsert_meta(html, "name", "theme-color", theme_color)
    html = upsert_meta(html, "property", "og:title", title)
    html = upsert_meta(html, "property", "og:description", og_description)
    html = upsert_meta(html, "property", "og:type", "website")
    html = upsert_meta(html, "property", "og:url", og_url)
    html = upsert_meta(html, "property", "og:image", og_image)
    html = upsert_meta(html, "name", "twitter:card", site.get("twitter_card", "summary"))
    html = upsert_meta(html, "name", "twitter:title", twitter_title)
    html = upsert_meta(html, "name", "twitter:description", twitter_description)
    html = upsert_link(html, "canonical", canonical_url)
    html = replace_generated_alternates(html, alternates)

    index_path.write_text(html, encoding="utf-8")
    return canonical_url or None


def write_sitemap(docs_root: Path, urls: list[str]) -> None:
    if not urls:
        return
    url_entries = "\n".join(f"  <url>\n    <loc>{escape(url)}</loc>\n  </url>" for url in urls)
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{url_entries}\n"
        "</urlset>\n"
    )
    (docs_root / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def iter_page_dirs(site_root: Path, locale_dir: str) -> list[Path]:
    page_dirs = [site_root]
    localized_dir = site_root / locale_dir
    if localized_dir.exists():
        page_dirs.append(localized_dir)
    return page_dirs


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch static paper-visualization metadata from JSON config files.")
    parser.add_argument("site_root", help="Root site directory that contains index.html and paper-visualization.config.json")
    parser.add_argument(
        "--config-name",
        default="paper-visualization.config.json",
        help="Config filename used in each route directory",
    )
    parser.add_argument(
        "--locale-dir",
        default="zh",
        help="Localized route directory name",
    )
    args = parser.parse_args()

    site_root = Path(args.site_root).resolve()
    urls: list[str] = []

    for page_dir in iter_page_dirs(site_root, args.locale_dir):
        config_path = page_dir / args.config_name
        index_path = page_dir / "index.html"
        if not config_path.exists() or not index_path.exists():
            continue
        config = json.loads(config_path.read_text(encoding="utf-8"))
        canonical_url = patch_index_html(index_path, config)
        if canonical_url:
            urls.append(canonical_url)

    write_sitemap(site_root, urls)


if __name__ == "__main__":
    main()
