# me0094.github.io

Source of <https://me0094.github.io>: cyber threat intelligence products — adversary profiles,
structured assessments, and the method and requirements behind them.

## What it is

A Jekyll site published with GitHub Pages. One product per file in `_posts/`, each with front matter
plus a product header (handling, version, review trigger) and a revision history.

## What it is not

- **Not a blog.** No commentary, no news roundups: each post is a product that answers a requirement.
- **Not a mirror of vendor reporting.** Where vendors disagree, the post says so; where the evidence
  stops, it states the gap.
- **Not the place for the tools.** They live in their own repositories and are linked from
  [`engineering.md`](engineering.md).

## Install

Nothing to install to read it: it is a static site. To build or preview it locally:

```console
$ gem install jekyll minima
$ jekyll serve
```

## Use

- `_posts/YYYY-MM-DD-slug.md` — one product. The permalink is the title.
- `about.md`, `method.md`, `requirements.md`, `engineering.md` — the pages in the header.
- `_config.yml` — title, description, theme and the header navigation.

## Method

Every claim carries its source and is graded on two independent axes, confidence and probability, per
claim rather than per section. `method.md` holds the standard (grading, review, corrections);
`requirements.md` holds the priority intelligence requirements the products answer, decomposed
PIR → EEI → product.

## Licence

- **Text and analysis** (posts, `about.md`, `method.md`, `requirements.md`, `engineering.md`):
  [CC BY 4.0](LICENSE). Quote, translate and reuse **with attribution** and a link to the original.
- **Site theme**: the `minima` theme keeps its own MIT licence; it is not content of this repository.
