#!/usr/bin/env python3
"""
Static site generator for tmsmendez.github.io
=============================================

No theme, no Ruby, no Jekyll. Just Python.

Content lives in plain files:
    content/about.md          -> homepage text
    content/news/*.md         -> one file per news item
    content/research/*.md     -> one file per research topic
    content/projects/*.md     -> one file per project
    publications.bib          -> the publication list (BibTeX)

To build locally:
    pip install -r requirements.txt
    python build.py
    python -m http.server -d _site

The GitHub Action in .github/workflows/build.yml runs the same two
commands on every push and deploys `_site/` to GitHub Pages.
"""


import re
import shutil
from datetime import date, datetime
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "_site"

# Publications whose `status` field matches one of these are left out of the
# site (the entries stay in publications.bib). Empty the tuple to show them.
HIDDEN_PUB_STATUSES = ("in review", "in preparation")

SITE = {
    "title": "Tomás Méndez Echenagucia",
    "subtitle": "Associate Professor — University of Washington",
    "url": "https://tmsmendez.github.io",
    "email": "tmendeze@uw.edu",
    "github": "https://github.com/tmsmendez",
    "scholar": "https://scholar.google.com/citations?hl=en&user=OyDWXZwAAAAJ",
    "department": "Department of Architecture, College of Built Environments",
    # accent color — change these two values to re-skin the whole site.
    # They override the defaults in assets/css/main.css on every page.
    # The site renders light on every device (no dark palette), so there are
    # no dark-mode counterparts here.
    "accent": "#1b365d",              # links, buttons, headings
    "accent_soft": "#2f5d94",         # hover / secondary
    "author_names": [  # variants of the site owner's name, bolded in publication lists
        "Méndez Echenagucia",
        "Mendez Echenagucia",
        "Echenagucia",
    ],
    "year": date.today().year,
}

MD = markdown.Markdown(extensions=["extra", "smarty", "sane_lists"])

env = Environment(
    loader=FileSystemLoader(ROOT / "templates"),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def read_front_matter(path):
    """Split a markdown file into (metadata-dict, body-string)."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm) or {}
        return meta, body.strip()
    return {}, text.strip()


def md_to_html(text):
    MD.reset()
    return MD.convert(text)


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def write(path, html):
    path = OUT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


# --------------------------------------------------------------------------
# BibTeX parsing (self-contained: tuned to BibDesk-style .bib files)
# --------------------------------------------------------------------------

LATEX_ACCENTS = [
    (r"\{\\'\{?([a-zA-Z])\}?\}", "\u0301"),  # {\'e} / {\'{e}}
    (r"\\'\{([a-zA-Z])\}", "\u0301"),
    (r"\{\\`\{?([a-zA-Z])\}?\}", "\u0300"),
    (r"\\`\{([a-zA-Z])\}", "\u0300"),
    (r"\{\\\^\{?([a-zA-Z])\}?\}", "\u0302"),
    (r"\{\\\"\{?([a-zA-Z])\}?\}", "\u0308"),
    (r"\\\"\{([a-zA-Z])\}", "\u0308"),
    (r"\{\\~\{?([a-zA-Z])\}?\}", "\u0303"),
    (r"\\~\{([a-zA-Z])\}", "\u0303"),
    (r"\{\\v\{?([a-zA-Z])\}?\}", "\u030c"),
    (r"\\v\{([a-zA-Z])\}", "\u030c"),
    (r"\{\\c\{?([a-zA-Z])\}?\}", "\u0327"),
]


def delatex(s):
    """Convert the LaTeX escapes used in the .bib file to unicode."""
    import unicodedata
    for pattern, combining in LATEX_ACCENTS:
        s = re.sub(pattern, lambda m: m.group(1) + combining, s)
    s = unicodedata.normalize("NFC", s)
    s = s.replace(r"\&", "&").replace("--", "\u2013")
    s = s.replace("``", "\u201c").replace("''", "\u201d")
    s = re.sub(r"\\textbf\{([^}]*)\}", r"\1", s)
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def parse_bib(path):
    """Parse a .bib file into a list of entry dicts."""
    text = path.read_text(encoding="utf-8")
    entries = []
    i = 0
    while True:
        at = text.find("@", i)
        if at == -1:
            break
        # skip comments
        line_start = text.rfind("\n", 0, at) + 1
        if text[line_start:at].strip().startswith("%"):
            i = at + 1
            continue
        brace = text.find("{", at)
        if brace == -1:
            break
        etype = text[at + 1:brace].strip().lower()
        # find matching closing brace
        depth, j = 1, brace + 1
        while j < len(text) and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[brace + 1:j - 1]
        i = j
        key, _, rest = body.partition(",")
        entry = {"type": etype, "key": key.strip(), "raw": text[at:j]}
        # parse fields: name = {value} | "value" | bare
        k = 0
        while k < len(rest):
            m = re.match(r"\s*([\w\-:.]+)\s*=\s*", rest[k:])
            if not m:
                k += 1
                continue
            name = m.group(1).lower()
            k += m.end()
            if k < len(rest) and rest[k] == "{":
                depth, start = 1, k + 1
                k += 1
                while k < len(rest) and depth:
                    if rest[k] == "{":
                        depth += 1
                    elif rest[k] == "}":
                        depth -= 1
                    k += 1
                value = rest[start:k - 1]
            elif k < len(rest) and rest[k] == '"':
                end = rest.find('"', k + 1)
                value = rest[k + 1:end]
                k = end + 1
            else:
                m2 = re.match(r"([^,\n]*)", rest[k:])
                value = m2.group(1)
                k += m2.end()
            entry[name] = value.strip()
            comma = rest.find(",", k)
            k = comma + 1 if comma != -1 else len(rest)
        entries.append(entry)
    return entries


def format_authors(author_field):
    """'Last, First and Last, First' -> 'F. Last, F. Last' with owner bolded."""
    people = re.split(r"\s+and\s+", delatex(author_field))
    out = []
    for p in people:
        p = p.strip().rstrip(",")
        if not p:
            continue
        if "," in p:
            last, first = [x.strip() for x in p.split(",", 1)]
        else:
            parts = p.split()
            last, first = parts[-1], " ".join(parts[:-1])
        initials = " ".join(
            (w[0] + "." if not w.endswith(".") and len(w) > 1 else w)
            for w in first.split()
        )
        name = f"{initials} {last}".strip()
        if any(v in last for v in SITE["author_names"]):
            name = f"<strong>{name}</strong>"
        out.append(name)
    return ", ".join(out)


def venue_of(e):
    for field in ("journal", "booktitle", "howpublished", "school", "publisher"):
        if e.get(field):
            v = delatex(e[field])
            if e.get("type") in ("phdthesis", "thesis") and field == "school":
                v = f"{delatex(e.get('type_', e.get('type', '')))} thesis, {v}" if False else f"{v}"
            return v
    return ""


def build_publications():
    entries = parse_bib(ROOT / "publications.bib")
    pubs = []
    for e in entries:
        status = e.get("status", "")
        if status.strip().lower() in HIDDEN_PUB_STATUSES:
            continue
        year = e.get("year", "n.d.")
        title = delatex(e.get("title", "Untitled"))
        link = e.get("html") or e.get("url") or (
            "https://doi.org/" + e["doi"].replace("https://doi.org/", "")
            if e.get("doi") else None
        )
        preview = e.get("preview")
        pubs.append({
            "key": e["key"],
            "year": year,
            "title": title,
            "authors": format_authors(e.get("author", "")),
            "venue": venue_of(e),
            "volume": e.get("volume", ""),
            "pages": e.get("pages", ""),
            "link": link,
            "pdf": e.get("pdf"),
            "status": status,
            "preview": f"/assets/img/publication_preview/{preview}" if preview else None,
            "bibtex": clean_bibtex(e["raw"]),
            "type": e["type"],
        })

    def sort_key(p):
        try:
            y = int(p["year"])
        except ValueError:
            y = 0
        return -y

    pubs.sort(key=sort_key)
    years = []
    for p in pubs:
        if p["year"] not in years:
            years.append(p["year"])
    grouped = [(y, [p for p in pubs if p["year"] == y]) for y in years]
    return pubs, grouped


def clean_bibtex(raw):
    """Strip BibDesk noise fields from the displayed BibTeX."""
    lines = []
    skip = ("date-added", "date-modified", "file", "bdsk-url", "bibtex_show", "preview")
    for line in raw.splitlines():
        name = line.strip().split("=")[0].strip().lower()
        if any(name.startswith(s) for s in skip):
            continue
        lines.append(line)
    text = "\n".join(lines)
    if not text.rstrip().endswith("}"):
        text += "}"
    return text


# --------------------------------------------------------------------------
# collections (news / research / projects)
# --------------------------------------------------------------------------

def load_collection(name):
    items = []
    for path in sorted((CONTENT / name).glob("*.md")):
        meta, body = read_front_matter(path)
        meta["body_html"] = md_to_html(body) if body else ""
        meta["slug"] = meta.get("slug") or slugify(meta.get("title", path.stem))
        meta["source"] = path.name
        items.append(meta)
    return items


def load_news():
    items = load_collection("news")
    for n in items:
        d = n.get("date")
        if isinstance(d, str):
            d = datetime.strptime(d, "%Y-%m-%d").date()
        n["date"] = d
        n["date_str"] = d.strftime("%b %-d, %Y") if d else ""
    items.sort(key=lambda n: n["date"], reverse=True)
    return items


def sorted_cards(items):
    return sorted(items, key=lambda x: x.get("importance", 99))


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------

def render(template, out_path, **ctx):
    html = env.get_template(template).render(site=SITE, **ctx)
    write(out_path, html)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    (OUT / ".nojekyll").write_text("")

    # about / homepage -----------------------------------------------------
    about_meta, about_body = read_front_matter(CONTENT / "about.md")
    news = load_news()
    render(
        "home.html", "index.html",
        page={"title": "About", "nav": "about"},
        about=md_to_html(about_body),
        about_meta=about_meta,
        news=news[: about_meta.get("news_limit", 8)],
    )

    # news ------------------------------------------------------------------
    render("news.html", "news/index.html",
           page={"title": "News", "nav": "news"}, news=news)

    # research + projects ---------------------------------------------------
    for name, nav, title, blurb in (
        ("research", "research", "Research",
         "Current and past research topics."),
        ("projects", "projects", "Projects",
         "Selected projects, pavilions and demonstrators."),
    ):
        items = load_collection(name)
        categories = []
        for it in items:
            c = it.get("category") or ""
            if c not in categories:
                categories.append(c)
        grouped = [(c, sorted_cards([i for i in items if (i.get("category") or "") == c]))
                   for c in categories]
        render("cards.html", f"{name}/index.html",
               page={"title": title, "nav": nav, "blurb": blurb},
               grouped=grouped, base=f"/{name}")
        for it in items:
            render("detail.html", f"{name}/{it['slug']}/index.html",
                   page={"title": it["title"], "nav": nav}, item=it)

    # publications ----------------------------------------------------------
    pubs, grouped = build_publications()
    render("publications.html", "publications/index.html",
           page={"title": "Publications", "nav": "publications"},
           grouped=grouped, count=len(pubs))

    # 404 -------------------------------------------------------------------
    render("404.html", "404.html", page={"title": "Not found", "nav": ""})

    print(f"Built {sum(1 for _ in OUT.rglob('*.html'))} pages "
          f"and {len(pubs)} publications into {OUT}/")


if __name__ == "__main__":
    main()
