# tmsmendez.github.io

Personal academic website of Tomás Méndez Echenagucia — built with a small,
self-contained Python generator (`build.py`). No Jekyll, no Ruby, no external theme.

## How it works

| You edit…                  | The site shows…                                  |
|----------------------------|--------------------------------------------------|
| `content/about.md`         | Homepage text                                    |
| `content/news/*.md`        | News (one file per item)                         |
| `content/research/*.md`    | Research topics (card + sub-page each)           |
| `content/projects/*.md`    | Projects (card + sub-page each)                  |
| `publications.bib`         | The full publication list, grouped by year       |
| `assets/img/…`             | All images                                       |

Every push to `main`/`master` triggers `.github/workflows/build.yml`, which runs
`python build.py` and deploys the resulting `_site/` folder to GitHub Pages.

> **One-time repo setting:** in *Settings → Pages*, set **Source** to
> **GitHub Actions** (instead of "deploy from a branch").

## Adding content

### A news item

Create `content/news/2026-09-01.md`:

```markdown
---
title: "New paper accepted!"
date: 2026-09-01
link: https://doi.org/...        # optional
---
Optional longer text shown on the /news/ page.
```

### A publication

Append a normal BibTeX entry to `publications.bib`. Extra fields the site
understands:

- `preview = {venue.png}` — thumbnail from `assets/img/publication_preview/`
  (reuse the same file for the same journal/conference)
- `html = {https://...}` — the link the title points to
- `pdf = {file.pdf}` — a PDF in `assets/pdf/`
- `status = {In Review}` / `status = {In Preparation}` — the entry is **hidden**
  from the site (it stays in the .bib). The list of hidden statuses is
  `HIDDEN_PUB_STATUSES` in `build.py`; any other status shows as a badge.

### A research topic or project

Create a markdown file in `content/research/` or `content/projects/`:

```markdown
---
title: My new topic
description: One-line teaser shown on the card.
img: assets/img/card_image.png       # card thumbnail
importance: 5                        # sort order within its category
category: University of Washington   # research only; section heading
gallery:                             # optional image grid, one row per line
  - [big_image.png]
  - [left.png, right.png]
---
Body text in plain markdown. Use `#### Collaborators`, `#### Publications`,
`#### Press` headings with bullet lists of links.
```

## Accent color

The site's accent color lives in the `SITE` dict at the top of **`build.py`**
(`accent`, `accent_soft`, `accent_dark`, `accent_soft_dark`). Those four values
are injected into every page and override the defaults in
`assets/css/main.css`. Change them there to re-skin the whole site.

## Building locally

```bash
pip install -r requirements.txt
python build.py
python -m http.server -d _site   # open http://localhost:8000
```
