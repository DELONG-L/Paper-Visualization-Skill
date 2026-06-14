# `paper-page.config.json` schema

The starter site is driven by a single JSON config file in `docs/paper-page.config.json`.

## Top-level fields

```json
{
  "site": {},
  "authors": [],
  "affiliations": "",
  "hero_facts": [],
  "hero_figure": {},
  "summary": {},
  "sections": [],
  "citation": {},
  "footer": {}
}
```

## `site`

```json
{
  "title": "Exact paper title",
  "short_title": "Short brand label for nav",
  "kicker": "arXiv preprint · 2026 · systems paper",
  "subtitle": "One-sentence scope description",
  "links": [
    { "label": "Paper PDF", "href": "paper.pdf", "primary": true },
    { "label": "arXiv", "href": "https://arxiv.org/abs/..." }
  ]
}
```

Notes:

- `title` should be the real paper title.
- `short_title` appears in the top-left brand area.
- `kicker` should stay short and factual.
- `links` render as hero buttons.

## `authors`

Array of display strings:

```json
[
  "Author One",
  "Author Two",
  "Author Three"
]
```

## `affiliations`

Single display string:

```json
"University A · Lab B"
```

## `hero_facts`

Use 2-4 concise fact blocks.

```json
[
  { "label": "Corpus", "value": "65 papers, 24 systems" },
  { "label": "Taxonomy", "value": "7 patterns, 5 classes" }
]
```

## `hero_figure`

```json
{
  "src": "assets/overview.png",
  "alt": "Overview figure alt text",
  "caption": "Short caption for the hero figure"
}
```

If `src` is empty, the hero figure is omitted.

## `summary`

```json
{
  "title": "What this paper contributes",
  "cards": [
    {
      "label": "01",
      "title": "A unified abstraction",
      "body": "Short contribution summary"
    }
  ]
}
```

## `sections`

Each section uses:

```json
{
  "id": "framework",
  "kicker": "Framework",
  "title": "What counts as an agentic skill",
  "theme": "plain",
  "paragraphs": [
    "First paragraph.",
    "Second paragraph."
  ],
  "highlights": ["Reusable", "Composable"],
  "figure": {
    "src": "assets/skill-anatomy.png",
    "alt": "Alt text",
    "caption": "Figure caption"
  },
  "figure_first": false,
  "cards": [
    {
      "label": "Formalization",
      "title": "S = (C, pi, T, R)",
      "body": "Short explanation",
      "variant": "default"
    }
  ]
}
```

### Section field notes

- `id`: used for anchor navigation
- `kicker`: short nav/section label
- `title`: visible heading
- `theme`: `"plain"` or `"soft"`
- `paragraphs`: ordered text blocks
- `highlights`: optional pill labels
- `figure`: optional image block
- `figure_first`: if true, render figure before text on large screens
- `cards`: optional supporting cards

## Card variants

Cards support these optional fields:

```json
{
  "label": "P1",
  "metric": "+16.2pp",
  "title": "Curated skills",
  "body": "Average pass-rate lift",
  "items": ["bullet one", "bullet two"],
  "variant": "default"
}
```

Rules:

- use `metric` for stat cards
- use `items` for bullet lists
- use `variant: "accent"` for a coral callout

## `citation`

```json
{
  "title": "Cite the paper directly",
  "note": "Use the arXiv version for now.",
  "bibtex": "@article{...}"
}
```

## `footer`

```json
{
  "left": "Static project page for the arXiv version of the paper.",
  "right": "Prepared as a GitHub Pages-friendly public package."
}
```
