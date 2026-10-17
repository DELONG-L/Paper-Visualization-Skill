#!/usr/bin/env python3
"""Render this custom example from its bilingual configs; the starter is unchanged."""

from pathlib import Path
from html import escape as e
import json

ROOT = Path(__file__).resolve().parents[1] / 'site'
REPO = 'https://github.com/DELONG-L/Paper-Visualization-Skill'
SOURCES = [REPO+'/blob/main/skills/paper-visualization/references/workflow.md',REPO+'/blob/main/skills/paper-visualization/references/config-schema.md',REPO+'/blob/main/skills/paper-visualization/SKILL.md']

def render(locale: str) -> None:
    folder = ROOT / ('zh' if locale == 'zh' else '')
    config = json.loads((folder/'paper-visualization.config.json').read_text())
    d = config['demo']
    site = config['site']
    language = site['lang']
    en = '../' if locale == 'zh' else './'
    zh = './' if locale == 'zh' else 'zh/'
    navigation = ''.join(f'<a href="#{anchor}">{e(label)}</a>' for anchor,label in zip(['reading-path','approach','citation'],d['nav']))
    tabs = []
    panels = []
    for i,label in enumerate(d['labels']):
        diagram = '<span class="mechanism-mini" aria-hidden="true">' + '<b>→</b>'.join(f'<i>{e(label)}</i>' for label in d['nodes']) + '</span>' if i == 1 else ''
        tabs.append(f'<button class="passage" type="button" role="tab" id="passage-{i}" aria-selected="{str(i==0).lower()}" aria-controls="annotation-{i}" aria-label="{e(label)}" tabindex="{0 if i==0 else -1}"><span class="passage-index">0{i+1}</span><span><strong>{e(label)}</strong><small>{e(d["excerpts"][i])}</small>{diagram}</span><span class="passage-arrow" aria-hidden="true">↗</span></button>')
        panels.append(f'<div class="annotation" role="tabpanel" id="annotation-{i}" aria-labelledby="passage-{i}" tabindex="0" {"hidden" if i else ""}><strong class="annotation-label">{e(label)}</strong><p>{e(d["notes"][i])}</p><button type="button" data-sources aria-label="{e(d["source_button"])}">{e(d["source_button"])}</button></div>')
    graphics = [
        '<div class="paper-stack" aria-hidden="true"><span class="mini-page"></span><span class="mini-page offset"></span></div><span class="small-tag">PDF / Preprint</span>' if locale == 'en' else '<div class="paper-stack" aria-hidden="true"><span class="mini-page"></span><span class="mini-page offset"></span></div><span class="small-tag">PDF / 预印本</span>',
        '<span class="outline-node">'+e(d['labels'][0])+'</span><span aria-hidden="true">→</span><span class="outline-node">'+e(d['labels'][1])+'</span><span aria-hidden="true">→</span><span class="outline-node">'+e(d['labels'][2])+'</span>',
        '<span class="reader-lines" aria-hidden="true"><i></i><i></i><i></i></span><span aria-hidden="true">↗</span><span class="small-tag">'+('Original paper' if locale == 'en' else '原论文')+'</span>',
    ]
    steps = []
    for i,step in enumerate(d['steps']):
        target = SOURCES[i] if i < 2 else '#citation'
        attrs = 'target="_blank" rel="noopener noreferrer"' if i < 2 else ''
        steps.append(f'<article class="step"><p class="step-label">{e(step[0])}</p><h3>{e(step[1])}</h3><div class="step-graphic">{graphics[i]}</div><p>{e(step[2])}</p><a href="{target}" {attrs}>{e(step[3])}</a></article>')
    steps = ''.join(steps)
    scope = ''.join(f'<li><span class="scope-number">0{i+1}</span><div><h3>{e(item[0])}</h3><p>{e(item[1])}</p></div></li>' for i,item in enumerate(d['scope']))
    source_list = ''.join(f'<li><a href="{SOURCES[i]}" target="_blank" rel="noopener noreferrer">{e(item[0])} ↗</a><p>{e(item[1])}</p></li>' for i,item in enumerate(d['sources']))
    alternates = '\n'.join(f'  <link rel="alternate" hreflang="{e(a["hreflang"])}" href="{e(a["href"])}" data-generated="alternate">' for a in site['alternates'])
    html=f'''<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{e(site['title'])}</title>
  <meta name="description" content="{e(site['meta_description'])}">
  <meta name="theme-color" content="#f7f3ee">
  <link rel="canonical" href="{e(site['canonical_url'])}">
{alternates}
  <meta property="og:title" content="{e(site['title'])}">
  <meta property="og:description" content="{e(site['meta_description'])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{e(site['og_url'])}">
  <meta property="og:image" content="{e(site['og_image'])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(site['title'])}">
  <meta name="twitter:description" content="{e(site['meta_description'])}">
  <link rel="stylesheet" href="styles.css">
</head>
<body id="top">
  <header class="site-header"><div class="shell topbar">
    <a class="brand serif" href="#top" aria-label="{e(d['back'])}"><span class="brand-mark" aria-hidden="true"></span>{e(d['short'])}</a>
    <div class="header-end"><nav class="nav-links" aria-label="{e(d['primary_nav'])}">{navigation}</nav><nav class="languages" aria-label="{e(d['language'])}"><a href="{en}" data-language lang="en" {('aria-current="page"' if locale=='en' else '')}>EN</a><a href="{zh}" data-language lang="zh-CN" {('aria-current="page"' if locale=='zh' else '')}>中文</a></nav></div>
  </div><div class="reading-progress" aria-hidden="true"></div></header>
  <main>
    <section class="hero"><div class="shell hero-grid">
      <div class="hero-copy"><p class="eyebrow">{e(d['kicker'])}</p><h1>{e(site['title'])}</h1><p class="lede">{e(site['subtitle'])}</p><div class="hero-actions"><a class="button-primary" href="#reading-path">{e(d['primary'])}<span aria-hidden="true">↓</span></a><a class="quiet-link" href="{REPO}">{e(d['github'])} ↗</a></div><p class="hero-note">{e(d['note'])}</p><div class="fact-line">{''.join(f'<span>{e(x)}</span>' for x in d['facts'])}</div></div>
      <figure class="reading-canvas"><figcaption class="canvas-heading"><span>{e(d['canvas'])}</span><span>{e(d['hint'])}</span></figcaption><div class="paper-sheet"><p class="paper-heading serif">{e(d['paper'])}</p><div class="passage-list" role="tablist" aria-label="{e(d['tablist'])}" aria-orientation="vertical">{''.join(tabs)}</div></div>{''.join(panels)}</figure>
    </div></section>
    <section class="section" id="reading-path"><div class="shell"><div class="section-heading"><p class="section-index"><span>01</span>{e(d['nav'][0])}</p><div><h2>{e(d['reading_title'])}</h2><p>{e(d['reading_intro'])}</p></div></div><div class="steps">{steps}</div></div></section>
    <section class="section approach" id="approach"><div class="shell approach-grid"><div class="approach-copy"><p class="section-index">{e(d['approach_label'])}</p><h2>{e(d['approach_title'])}</h2><p>{e(d['approach_text'])}</p></div><ol class="scope-list">{scope}</ol></div></section>
    <section class="section" id="citation"><div class="shell citation-grid"><div class="citation-copy"><p class="section-index">{e(d['cite_label'])}</p><h2>{e(d['cite_title'])}</h2><p>{e(d['cite_text'])}</p><a class="citation-link" href="{REPO}">{e(d['cite_link'])}</a></div><div><div class="citation-box"><div class="citation-top"><span>{e(d['cite_type'])}</span><button class="copy-button" type="button" id="copy-citation" data-copied="{e(d['copied'])}" data-error="{e(d['copy_error'])}">{e(d['cite_button'])}</button></div><pre><code id="bibtex">{e(config['citation']['bibtex'])}</code></pre></div><p class="copy-status" role="status" id="copy-status" aria-live="polite"></p></div></div></section>
  </main>
  <footer class="site-footer"><div class="shell footer-row"><span>{e(d['footer'])}</span><nav aria-label="{e(d['nav'][2])}"><a href="{REPO}/blob/main/LICENSE">{e(d['license'])}</a><a href="{REPO}">{e(d['github'])} ↗</a></nav></div></footer>
  <dialog id="sources" aria-labelledby="source-title"><div class="dialog-top"><h2 id="source-title">{e(d['source_title'])}</h2><button type="button" class="dialog-close" id="close-sources" aria-label="{e(d['close'])}">×</button></div><div class="dialog-body"><p>{e(d['source_intro'])}</p><ul class="source-list">{source_list}</ul><p class="dialog-note">{e(d['source_note'])}</p></div></dialog>
  <script src="script.js"></script>
</body>
</html>
'''
    (folder/'index.html').write_text(html)
    print(f'Rendered {folder / "index.html"}')

if __name__ == '__main__':
    for language in ('en','zh'):
        render(language)
