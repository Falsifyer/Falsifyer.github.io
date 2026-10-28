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

## Checks

Two workflows run on every push. `ci.yml` builds the site with Jekyll and fails if a page the header
links to is missing. `sitegate.yml` runs the site's own gate against the products:

- **handling** — the TLP rules, delegated to [`sharegate`](https://github.com/ME0094/cti-suite);
- **versioning** — a version in the product header must exist in its revision history;
- **freshness** — a product past its next review date fails;
- **vocabulary** — confidence and probability come from the declared lexicons;
- **cross-product consistency** — the same claim, graded differently in two products, fails.

To run the gate locally, put the suite beside the site:

```console
$ git clone --depth 1 --branch cti-method-v0.2.0 https://github.com/ME0094/cti-suite _suite
$ python3 scripts/sitegate.py
```

A contradiction between products is a build failure, not a reader's discovery.

## Claims

A product with a machine-readable ledger carries it in `_data/claims/<slug>.json`: the
claim, its id and stable key, its class and type, the declared confidence and probability,
and the sources — with `derived_from` for independence and `direct` for whether a source
bears on the claim itself.

The grade is not taken on trust. `sitegate` calls
`cti_method.grading.ceiling(..., mode="claim")` — the ceiling lives in the suite, not here —
and refuses a declared confidence above what the evidence supports. Two reports from one
publisher, or a source derived from another present, count as one voice.

A file may instead be an **ACH** (`hypotheses`, typed `evidence` and `judgements`): the
ceiling is then per hypothesis, computed in `mode="ach"` from diagnostic evidence and
independent sources. Both shapes can share one file — the ACH product uses one for its
identity question and one claim block for the mechanism it observed.

The table in a product is a **view** of its registry. `scripts/render_claims.py` regenerates
it between `<!-- claims:begin -->` and `<!-- claims:end -->`, and CI runs it with `--check`:
editing the registry without regenerating the table fails the build.

A claim a reader would act on also carries a **review trigger**: `documentary`, `technical` or
`behavioural`, the artefact that would satisfy it, and for the last two an expiry date. A
trigger that has expired fails the build. `scripts/source_drift.py` checks the ATT&CK
collection against `_data/sources.json` weekly and opens an issue when it moves — it does
not fail a build, because a source that changed is a reason to re-review, not a broken
commit.

`scripts/selftest.py` proves the three rejections: a grade above the ceiling, a derived
source counted twice, and a derivation cycle.

## Method

Every claim carries its source and is graded on two independent axes, confidence and probability, per
claim rather than per section. `method.md` holds the standard (grading, review, corrections);
`requirements.md` holds the priority intelligence requirements the products answer, decomposed
PIR → EEI → product.

## Licence

- **Text and analysis** (posts, `about.md`, `method.md`, `requirements.md`, `engineering.md`):
  [CC BY 4.0](LICENSE). Quote, translate and reuse **with attribution** and a link to the original.
- **Site theme**: the `minima` theme keeps its own MIT licence; it is not content of this repository.
