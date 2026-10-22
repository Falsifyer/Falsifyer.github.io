# me0094.github.io

Cyber threat intelligence from open sources: adversary profiles, structured assessments and the
tradecraft behind them. Every claim carries a source and is graded on two independent axes —
confidence and probability.

Published with GitHub Pages (Jekyll).

## Structure

- `_posts/` — dated products (actor profiles and assessments). Jekyll front matter plus a product
  header (handling, version, review trigger) and a revision history.
- `requirements.md` — the priority intelligence requirements the site answers (PIR → EEI → product).
- `method.md` — the tradecraft standard: grading, review and corrections.
- `about.md`, `index.md`, `_config.yml` — pages and site configuration.

## Conventions

- New products go in `_posts/` as `YYYY-MM-DD-slug.md` with Jekyll front matter.
- Each product carries a **version**, a **date**, a **review trigger** and a **revision history**.
- Grading is two-axis; the definition lives in `method.md`.

## Licencia

- **Texto y análisis** (posts, `about.md`, `method.md`, `requirements.md`, `engineering.md`):
  [CC BY 4.0](LICENSE). Se puede citar, traducir y reutilizar **con atribución** y enlace a la
  versión original.
- **Tema del sitio**: el tema `minima` de Jekyll conserva su licencia MIT; no es contenido de este
  repositorio.
