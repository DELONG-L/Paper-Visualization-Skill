# Workflow Notes

## Goal

Create a paper visualization that helps a reader answer these questions quickly:

1. What is the paper?
2. Why does it matter?
3. What are the main contributions?
4. Which figure best explains the method, taxonomy, or system?
5. Where is the PDF?

If the page is bilingual, the same answers should remain easy to find in both routes.

## Readability-first rules

- Show the real paper title in the hero.
- Keep the subtitle to one sentence.
- Put the PDF and primary paper/preprint links on the first screen.
- Use 3-4 short fact blocks, not a dense metric wall.
- Keep paragraphs short enough to scan.
- Use figures to support claims, not as decoration.

## Typical section mapping

This starter template works best for papers that fit a standard academic narrative:

- Summary
- Abstract or positioning
- Core framework / method / taxonomy
- Lifecycle or pipeline
- Results or evaluation
- Security / limitations / discussion
- Citation

Not every paper needs all of these. Delete weak sections rather than forcing them.

## How to summarize from the paper

### Hero

Extract:

- exact paper title
- one-sentence subtitle describing the paper's scope
- authors
- affiliations
- PDF and primary paper links

### Summary cards

Use these for the most reusable claims:

- formal abstraction
- taxonomy
- lifecycle model
- benchmark or empirical takeaway

### Section prose

Rewrite for the web. Do not paste raw paragraphs unless the source text is already concise.

Keep:

- one idea per paragraph
- concrete nouns over hype
- paper terminology intact when it matters

## Layout selection

Use the template's richer layouts deliberately:

- `framework`: figure + formalization + definition cards
- `lifecycle`: figure + staged timeline
- `showcase`: wide figure + lenses + supporting figures
- `stats`: metric band + figure + prose
- `split`: one figure plus explanatory copy

Do not force a paper into one layout family if the content does not justify it.

If the paper needs stronger section-specific composition than the config schema provides cleanly, edit the generated HTML/CSS/JS directly and treat the starter template as a starting point, not a prison.

## Bilingual guidance

Use dual routes instead of a page-level language toggle when the site should publish both English and Chinese:

- `docs/`
- `docs/zh/`

Guidelines:

- keep formal author names unchanged unless the user explicitly wants localized names
- keep paper titles unchanged unless the user explicitly wants translated titles
- translate navigation, section labels, notes, and explanatory prose
- adapt Chinese typography and spacing instead of reusing English rhythm blindly

## Design interpretation

Use the warm editorial style as a constraint on tone, not as the main objective.

Good uses of the style:

- serif paper title
- warm background
- restrained coral CTA
- soft cards for summary and notes

Bad uses of the style:

- replacing the paper title with a slogan
- oversized decorative hero blocks that push content below the fold
- visual motifs that dominate academic content

## Publication boundary

If the user does not want to expose LaTeX:

- keep public output to `docs/`, `release/`, `paper.pdf`, and image assets
- do not include `.tex`, `.bib`, or source zip files in the public package

## Final checks

Before publishing, verify:

- all asset paths are relative and survive subpath deployment
- no source-only files leak into the release package
- the citation block matches the public paper version
- the page still reads well on a narrow viewport
- bilingual routes, if present, cross-link correctly
- canonical URLs, hreflang links, and `sitemap.xml` match the intended public path
