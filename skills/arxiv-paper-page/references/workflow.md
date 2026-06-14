# Workflow Notes

## Goal

Create a paper page that helps a reader answer these questions quickly:

1. What is the paper?
2. Why does it matter?
3. What are the main contributions?
4. Which figure best explains the method or taxonomy?
5. Where is the PDF?

## Readability-first rules

- Show the real paper title in the hero.
- Keep the subtitle to one sentence.
- Put PDF and arXiv links on the first screen.
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
- PDF and arXiv links

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
- dark marketing panels that dominate academic content

## Publication boundary

If the user does not want to expose LaTeX:

- keep public output to `docs/`, `release/`, `paper.pdf`, and image assets
- do not include `.tex`, `.bib`, or source zip files in the public package

## Final checks

Before publishing, verify:

- all asset paths are relative and work under a GitHub Pages subpath
- no source-only files leak into the release package
- the citation block matches the public paper version
- the page still reads well on a narrow viewport
