# VitePress Migration Design

**Date:** 2026-06-03
**Status:** Approved
**Branch:** `feature/vitepress-migration`

## Goal

Convert the existing Sphinx-based pysheeet documentation (~50 `.rst` files in `docs/notes/`) into a VitePress site while preserving the same category structure. The result is for personal use — a self-contained, locally-runnable VitePress site with a cleaner look, local search, and modern navigation.

## Decisions (from brainstorming)

| Decision | Choice |
|---|---|
| Conversion method | Automated with `pandoc` + post-conversion cleanup script |
| Site location | New top-level folder `vitepress/` (sibling to `docs/`) |
| Scope | All 13 categories + top-level `python-new-py3.rst` |
| Theme | Default VitePress (light/dark toggle, local search) |
| Source files | Untouched — `docs/notes/*.rst` stays as-is |

## Target Structure

```
vitepress/
├── package.json              # vitepress + scripts (dev, build, preview)
├── .gitignore                # node_modules, .vitepress/cache, .vitepress/dist
├── README.md                 # how to run the site
├── index.md                  # landing page (rewritten from docs/index.rst)
├── python-new-py3.md         # top-level page from python-new-py3.rst
├── basic/                    # one folder per source category
│   ├── index.md              # category overview (from category's index.rst)
│   ├── python-basic.md
│   ├── python-future.md
│   └── ...
├── asyncio/
├── concurrency/
├── database/
├── extension/
├── hpc/                      # (includes hpc/images/ SVG files)
├── interview/
├── llm/
├── network/
├── os/
├── security/
├── appendix/
└── .vitepress/
    └── config.mjs            # nav + sidebar configuration
```

URLs become `/basic/python-basic`, `/asyncio/python-asyncio-basic`, etc. — same hierarchy as the source, cleaner URL form.

## Conversion Pipeline

A single bash script `convert.sh` at the project root runs three phases:

### Phase 1 — Bulk pandoc convert

```bash
find docs/notes -name "*.rst" | while read f; do
    rel="${f#docs/notes/}"
    out="vitepress/${rel%.rst}.md"
    mkdir -p "$(dirname "$out")"
    pandoc "$f" -f rst -t gfm-raw_html --wrap=none -o "$out"
done
```

`gfm-raw_html` chosen because some source files embed raw HTML (e.g. via `.. raw:: html`) and we want pandoc to pass it through rather than escape it.

### Phase 2 — Python cleanup script (`cleanup.py`)

Post-pandoc fixes:

- **Internal `.rst` links** → `.md` (regex replace)
- **Image paths** — copy `docs/notes/hpc/images/` → `vitepress/hpc/images/`, leave relative paths intact
- **Code fences** — ensure each `\`\`\`` block has a language hint; default to `python` when content looks like Python
- **Strikethrough conflicts** — `gfm` converts `~~text~~` to strikethrough, but the cheat sheets use `~` as a Python bitwise NOT operator. Escape `~~` when it appears inside code-fence-adjacent context.
- **Drop `.. meta::` blocks** — VitePress doesn't need them; description/keywords get frontmatter instead
- **Add frontmatter** to each page:
  ```yaml
  ---
  title: <derived from H1>
  ---
  ```
- **Strip `.. raw:: html` blocks from page bodies** — VitePress landing is written fresh; embedded raw HTML in source pages mostly targets the README, not the content

### Phase 3 — Generate `config.mjs`

`gen-config.py` walks the converted tree and emits `.vitepress/config.mjs` with:

- `nav` — top nav bar with one entry per category, ordered by source toctree
- `sidebar` — per-section sidebar listing pages in source toctree order
- `search: { provider: 'local' }` — enabled by default (one of the main "look" wins)

## Edge Cases

| Case | Handling |
|---|---|
| REPL output in code blocks | One-line CSS rule to visually distinguish `>>>` prompt lines; otherwise default fence |
| RST grid tables (database/, extension/) | Pandoc handles in `gfm` mode; cleanup script spot-checks alignment |
| `:ref:` and `:doc:` cross-refs | Convert `:doc:\`python-basic\`` → `/basic/python-basic`; unknown anchors get a TODO comment |
| `interview/` has only an `index.rst` | Create `interview/index.md`; sidebar lists "Overview" only |
| Mega file `python-new-py3.rst` (29KB) | Single page; right-side outline provides nav |
| `404.rst` | Not converted — VitePress provides a default 404 |

## Out of Scope

- Deploying to GitHub Pages / Netlify / Vercel (personal use → `npm run dev` is enough)
- Editing source `.rst` files in `docs/notes/`
- Custom domain, analytics, comments
- Migrating `README.rst` to the VitePress site
- Translations

## Deliverables

1. `vitepress/` — the new VitePress site (folder, fully self-contained)
2. `convert.sh` at the project root — one-shot conversion script
3. `cleanup.py` — the post-pandoc fixer
4. `gen-config.py` — emits `.vitepress/config.mjs` from the converted tree
5. `vitepress/README.md` — short instructions: `cd vitepress && npm install && npm run dev`

## Verification Plan

1. `cd vitepress && npm install` — confirm deps install cleanly
2. `npm run dev` — confirm dev server boots (then kill it)
3. `npm run build` — confirm production build succeeds (catches broken internal links, missing files, malformed config)
4. Spot-check 5 pages by opening in the dev server:
   - `basic/python-basic`
   - `asyncio/python-asyncio-basic`
   - `database/python-sqlalchemy`
   - `hpc/slurm` (has images)
   - `python-new-py3` (long)
   - Confirm: code blocks render with highlighting, internal links resolve, images load, right-side outline appears, local search finds the page by title
5. Final regex sweep: `rg -l '\.rst' vitepress/` must return zero matches

## Landing Page Source

Use `docs/index.rst` (not `docs/notes/index.rst`) as the basis for `vitepress/index.md` — the former has a better intro and is the documented site landing.
