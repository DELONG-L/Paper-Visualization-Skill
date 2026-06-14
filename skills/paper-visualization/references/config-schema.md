# `paper-visualization.config.json` schema

The starter site is driven by a JSON config file in `docs/paper-visualization.config.json`.

For bilingual deployments, `docs/zh/paper-visualization.config.json` uses the same schema.

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
  "lang": "en",
  "kicker": "2026 · research paper",
  "subtitle": "One-sentence scope description",
  "meta_description": "Search and social description",
  "theme_color": "#faf9f5",
  "canonical_url": "https://example.com/publications/my-paper/",
  "og_url": "https://example.com/publications/my-paper/",
  "og_image": "https://example.com/publications/my-paper/assets/overview.png",
  "alternates": [
    { "hreflang": "en", "href": "https://example.com/publications/my-paper/" },
    { "hreflang": "zh-CN", "href": "https://example.com/publications/my-paper/zh/" },
    { "hreflang": "x-default", "href": "https://example.com/publications/my-paper/" }
  ],
  "brand_home_url": "../../",
  "brand_aria_label": "Back to homepage",
  "show_brand_mark": false,
  "language_switch": {
    "aria_label": "Language switch",
    "links": [
      { "label": "EN", "href": "./", "active": true },
      { "label": "中文", "href": "zh/" }
    ]
  },
  "links": [
    { "label": "Paper PDF", "href": "paper.pdf", "primary": true },
    { "label": "Preprint", "href": "https://example.com/preprint" }
  ]
}
```

Notes:

- `title` should stay the real paper title.
- `lang` controls the page `<html lang>` and Chinese typography overrides.
- `meta_description`, `canonical_url`, `og_url`, `og_image`, and `alternates` are consumed by the metadata materializer script for static head tags.
- `brand_home_url` is optional. Use `#top` when the page is standalone, or a homepage URL when the visualization is nested under a broader site.
- `show_brand_mark` defaults to false because the icon is not always appropriate on mobile.
- `language_switch.links` should be omitted or empty for monolingual pages.

## `authors`

Array of display strings:

```json
[
  "Author One",
  "Author Two",
  "Author Three"
]
```

Keep formal author names as the paper uses them. Do not localize author names unless the user explicitly wants that.

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
  "kicker": "Summary",
  "nav_label": "Summary",
  "title": "What this paper contributes",
  "cards_layout": "feature-grid",
  "cards": [
    {
      "label": "01",
      "title": "A unified abstraction",
      "body": "Short contribution summary"
    }
  ]
}
```

`cards_layout` is usually `feature-grid` here.

## `sections`

Each section uses this common envelope:

```json
{
  "id": "framework",
  "nav_label": "Framework",
  "kicker": "Framework",
  "title": "What counts as an agentic skill",
  "wide_heading": true,
  "section_note": "Short framing note",
  "theme": "plain",
  "layout": "framework",
  "paragraphs": ["First paragraph", "Second paragraph"],
  "highlights": ["Reusable", "Composable"],
  "figure": {},
  "wide_figure": {},
  "supporting_figures": [],
  "figure_first": false,
  "equation": {},
  "cards_layout": "definitions",
  "cards": []
}
```

### Section field notes

- `id`: anchor and navigation target
- `nav_label`: optional shorter label for the sticky nav
- `kicker`: visible section eyebrow
- `title`: visible section heading
- `wide_heading`: use when the heading and section note need more horizontal space
- `section_note`: optional explanatory note under the heading
- `theme`: `"plain"` or `"soft"`
- `layout`: one of:
  - `plain`: paragraphs/highlights/cards only
  - `split`: prose/cards paired with one figure
  - `framework`: figure + equation card + definition grid
  - `lifecycle`: figure + timeline
  - `showcase`: wide figure + pattern lenses + supporting figures
  - `stats`: metric band + figure + prose
- `wide_figure`: used by `showcase`
- `supporting_figures`: secondary figure list, typically length 2
- `equation`: used by `framework`
- `cards_layout`: how `cards` should render for that section

## Card layouts

### `feature-grid`

Used for top-level contribution summaries.

```json
[
  { "label": "01", "title": "Contribution", "body": "Summary" }
]
```

### `definitions`

Used for formal dimensions or anatomy cards.

```json
[
  { "label": "C", "title": "When to invoke", "body": "Explanation" }
]
```

### `timeline`

Used by lifecycle sections.

```json
[
  { "label": "01", "title": "Discovery", "body": "Explanation" }
]
```

### `lenses`

Used for pattern lenses or grouped design takeaways.

```json
[
  { "label": "P1", "title": "Disclosure", "body": "Explanation" }
]
```

### `stats`

Used for benchmark or results bands.

```json
[
  {
    "metric": "+16.2pp",
    "title": "Curated skills",
    "body": "Average pass-rate lift",
    "variant": "good"
  }
]
```

`variant` may be `good`, `bad`, or `neutral`.

### `stack`

Used for vertically stacked callouts such as security notes.

```json
[
  {
    "kind": "callout",
    "title": "Threats the paper emphasizes",
    "items": ["Point one", "Point two"]
  },
  {
    "label": "Anchor case",
    "body": "Short highlighted note",
    "variant": "accent"
  }
]
```

### `grid-1` / `grid-2` / `grid-3` / `grid-4`

Used for generic cards when the richer named layouts do not fit.

```json
[
  {
    "label": "Formalization",
    "title": "S = (C, pi, T, R)",
    "body": "Short explanation",
    "variant": "default"
  }
]
```

## `equation`

Used by `layout: "framework"`:

```json
{
  "label": "Formalization",
  "value": "S = (C, pi, T, R)",
  "body": "Short explanation"
}
```

## `citation`

```json
{
  "kicker": "Citation",
  "nav_label": "Citation",
  "title": "Cite the paper directly",
  "note": "Use the public version that matches this page.",
  "button_label": "Copy BibTeX",
  "copied_label": "Copied",
  "error_label": "Copy failed",
  "bibtex": "@article{...}"
}
```

Use localized `button_label`, `copied_label`, and `error_label` for non-English routes.

## `footer`

```json
{
  "enabled": false,
  "left": "Static paper visualization for the publication.",
  "right": "Prepared as a portable static site package."
}
```

Set `enabled` to false if the page should end after the citation block.
