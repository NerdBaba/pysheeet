# VitePress Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert the existing pysheeet Sphinx documentation (`docs/notes/*.rst`) into a self-contained VitePress site under a new top-level `vitepress/` folder, preserving the same category structure and producing a clean, modern, locally-runnable site for personal use.

**Architecture:** Three-phase one-shot conversion: (1) bulk `pandoc` `.rst` → `.md`, (2) Python cleanup script to fix links/code-fence languages/strikethrough/embed-stripping and add frontmatter, (3) auto-generated `.vitepress/config.mjs` from the converted tree. Source `.rst` files are not modified.

**Tech Stack:** Bash, Python 3 (stdlib only), pandoc, VitePress (Node 18+), default VitePress theme.

**Working directory:** `.worktrees/vitepress-migration` (branch `feature/vitepress-migration`).

---

## Task 1: Verify pandoc is available

**Files:** none

**Step 1: Check pandoc version**

Run: `pandoc --version | head -1`

Expected output on success: `pandoc 2.x.y` or `pandoc 3.x.y` (any version 2.19+ works; 3.x preferred for GFM improvements).

**Step 2: If missing, install**

macOS: `brew install pandoc`
Linux: `sudo apt-get install pandoc` (or distro equivalent)
Windows: `choco install pandoc`

**Step 3: Verify node + npm**

Run: `node --version && npm --version`

Expected: `v18.x` or higher for `node`, and any modern `npm` (9+).

**Step 4: Commit nothing (no files changed)**

No commit — this is environment verification only.

---

## Task 2: Scaffold the `vitepress/` folder and `package.json`

**Files:**
- Create: `vitepress/package.json`
- Create: `vitepress/.gitignore`

**Step 1: Create `vitepress/package.json`**

Write exactly this content:

```json
{
  "name": "pysheeet-vitepress",
  "version": "1.0.0",
  "private": true,
  "description": "Pysheeet cheat sheets as a VitePress site",
  "scripts": {
    "dev": "vitepress dev",
    "build": "vitepress build",
    "preview": "vitepress preview"
  },
  "devDependencies": {
    "vitepress": "^1.5.0"
  }
}
```

**Step 2: Create `vitepress/.gitignore`**

```
node_modules/
.vitepress/cache/
.vitepress/dist/
```

**Step 3: Commit**

```bash
git add vitepress/package.json vitepress/.gitignore
git commit -m "chore(vitepress): scaffold folder and package.json"
```

---

## Task 3: Write the pandoc conversion script `convert.sh`

**Files:**
- Create: `convert.sh` (at project root, next to `Makefile`)

**Step 1: Make scripts dir and write `convert.sh`**

Write the following to `convert.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Phase 1: Bulk pandoc convert docs/notes/*.rst -> vitepress/**/*.md
SRC="${1:-docs/notes}"
DST="${2:-vitepress}"

if [[ ! -d "$SRC" ]]; then
    echo "Source directory not found: $SRC" >&2
    exit 1
fi

# Mirror category folders; convert .rst -> .md
find "$SRC" -name "*.rst" -type f | while read -r f; do
    rel="${f#${SRC}/}"
    out="${DST}/${rel%.rst}.md"
    mkdir -p "$(dirname "$out")"
    pandoc "$f" \
        -f rst \
        -t gfm-raw_html \
        --wrap=none \
        -o "$out"
    echo "  converted: $rel"
done

echo "Phase 1 complete: $(find "$DST" -name "*.md" -type f | wc -l | tr -d ' ') files written"
```

**Step 2: Make executable and smoke-test it**

```bash
chmod +x convert.sh
./convert.sh docs/notes vitepress
```

Expected last line: `Phase 1 complete: <N> files written` where N matches the count from `find docs/notes -name "*.rst" | wc -l` (should be ~55, depending on whether you count `index.rst` in every category).

**Step 3: Spot-check one file**

```bash
head -40 vitepress/basic/python-basic.md
```

Expected: First lines should show the page title as a Markdown `#` heading, followed by paragraphs and a ` ```python ` code fence. No `.. code-block::` directives should remain.

**Step 4: Verify directory structure mirrors source**

```bash
ls vitepress/ && echo "---" && ls vitepress/basic/ | head
```

Expected: One folder per source category (`basic`, `asyncio`, `concurrency`, `database`, `extension`, `hpc`, `interview`, `llm`, `network`, `os`, `security`, `appendix`) and the top-level `python-new-py3.md`.

**Step 5: Commit**

```bash
git add convert.sh
git commit -m "feat(vitepress): add pandoc bulk-conversion script"
```

---

## Task 4: Write the post-conversion cleanup script `cleanup.py`

**Files:**
- Create: `cleanup.py` (at project root)

**Step 1: Write `cleanup.py`**

```python
#!/usr/bin/env python3
"""
Post-pandoc cleanup for the VitePress conversion.

Fixes:
  - Internal .rst -> .md links
  - Code-fence language hints (default to 'python' when missing and content looks like Python)
  - ~~ strikethrough conflicts (escape when inside code context)
  - Drops .. meta:: blocks
  - Adds frontmatter with a title derived from the first H1
  - Strips .. raw:: html blocks (their content was for the README, not the docs)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("vitepress")

META_DIRECTIVE = re.compile(
    r'^\.\. meta::\s*\n((?:[ \t]+::?[^\n]*\n)+)', re.MULTILINE
)
RAW_HTML_DIRECTIVE = re.compile(
    r'^\.\. raw::\s+[^\n]*\n+(?:[ \t]+\S.*\n)+', re.MULTILINE
)
H1 = re.compile(r'^# (.+)$', re.MULTILINE)
RST_LINK = re.compile(r'\(([\w./-]+)\.rst(#[^)]*)?\)')
FENCE = re.compile(r'^```(\w*)\n(.*?)^```', re.MULTILINE | re.DOTALL)
PY_HINT_NEEDED = re.compile(r'```\n((?:>>> |\$ |\.\.\. ).+)', re.MULTILINE)


def add_frontmatter(text: str, title: str) -> str:
    if text.startswith('---'):
        return text
    return f'---\ntitle: {title}\n---\n\n{text}'


def derive_title(text: str) -> str:
    m = H1.search(text)
    if m:
        return m.group(1).strip()
    return "Untitled"


def fix_rst_links(text: str) -> str:
    return RST_LINK.sub(r'(\1.md\2)', text)


def fix_code_fences(text: str) -> str:
    """Default untagged fences to 'python' when they look like Python/REPL."""
    def repl(m: re.Match) -> str:
        lang, body = m.group(1), m.group(2)
        if lang:
            return m.group(0)
        if PY_HINT_NEEDED.match(m.group(0)):
            return f'```python\n{body}```'
        return m.group(0)
    return FENCE.sub(repl, text)


def strip_meta(text: str) -> str:
    return META_DIRECTIVE.sub('', text)


def strip_raw_html(text: str) -> str:
    return RAW_HTML_DIRECTIVE.sub('', text)


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text
    text = strip_meta(text)
    text = strip_raw_html(text)
    text = fix_rst_links(text)
    text = fix_code_fences(text)
    text = add_frontmatter(text, derive_title(text))
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main() -> int:
    changed = 0
    for md in ROOT.rglob('*.md'):
        if process(md):
            changed += 1
    print(f'cleanup: modified {changed} files under {ROOT}/')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

**Step 2: Run the cleanup**

```bash
python3 cleanup.py vitepress
```

Expected last line: `cleanup: modified <N> files under vitepress/` (N should be roughly equal to the number of .md files, since most will gain frontmatter and have link fixes).

**Step 3: Spot-check the changes**

```bash
head -20 vitepress/basic/python-basic.md
```

Expected first 6 lines:
```
---
title: From Scratch
---

# From Scratch
...
```

Confirm: frontmatter present, title is `From Scratch`, no `.. meta::` block remains, code fences have a language hint.

**Step 4: Verify internal links converted**

```bash
grep -rn '\.rst' vitepress/ || echo "no .rst references remaining"
```

Expected: `no .rst references remaining`.

**Step 5: Commit**

```bash
git add cleanup.py
git commit -m "feat(vitepress): add post-pandoc cleanup script"
```

---

## Task 5: Write the config generator `gen-config.py`

**Files:**
- Create: `gen-config.py` (at project root)
- Modify: `vitepress/.vitepress/config.mjs` (generated)

**Step 1: Write `gen-config.py`**

```python
#!/usr/bin/env python3
"""
Generate .vitepress/config.mjs from the converted Markdown tree.

Each top-level subfolder of vitepress/ becomes a sidebar group;
the page order is alphabetical (VitePress will sort by file name).
The top-level index.md, python-new-py3.md become nav entries.
"""
from __future__ import annotations
import sys
from pathlib import Path
import json

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("vitepress")
CONFIG = ROOT / ".vitepress" / "config.mjs"

CATEGORIES = sorted(
    p.name for p in ROOT.iterdir()
    if p.is_dir() and not p.name.startswith('.') and not p.name.startswith('node_modules')
)


def page_link(p: Path, root: Path) -> str:
    rel = p.relative_to(root).with_suffix('')
    return '/' + str(rel).replace('\\', '/')


def sidebar_for(category: str) -> list[dict]:
    catdir = ROOT / category
    files = sorted(catdir.glob('*.md'))
    items: list[dict] = []
    for f in files:
        title = f.stem.replace('-', ' ').replace('_', ' ').title()
        items.append({'text': title, 'link': page_link(f, ROOT)})
    return items


def nav_entries() -> list[dict]:
    nav = [{'text': 'Home', 'link': '/'}]
    top_level = sorted(ROOT.glob('*.md'))
    for f in top_level:
        if f.name in ('index.md',):
            continue
        title = f.stem.replace('-', ' ').replace('_', ' ').title()
        nav.append({'text': title, 'link': page_link(f, ROOT)})
    for cat in CATEGORIES:
        title = cat.replace('-', ' ').title()
        nav.append({'text': title, 'link': f'/{cat}/'})
    return nav


def render_config() -> str:
    sidebar = {f'/{cat}/': [{'text': 'Overview', 'link': f'/{cat}/'}, *sidebar_for(cat)] for cat in CATEGORIES}
    cfg = {
        'title': 'Pysheeet',
        'description': 'Python cheat sheets',
        'cleanUrls': True,
        'nav': nav_entries(),
        'sidebar': sidebar,
        'search': {'provider': 'local'},
        'outline': {'level': [2, 3]},
    }
    body = json.dumps(cfg, indent=2)
    return (
        f"// Auto-generated by gen-config.py — do not edit by hand.\n"
        f"// Regenerate with: python3 gen-config.py vitepress\n\n"
        f"export default {body};\n"
    )


def main() -> int:
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(render_config(), encoding='utf-8')
    print(f'wrote {CONFIG}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

**Step 2: Run the generator**

```bash
python3 gen-config.py vitepress
```

Expected last line: `wrote vitepress/.vitepress/config.mjs`.

**Step 3: Verify the generated config is valid JS**

```bash
head -30 vitepress/.vitepress/config.mjs
```

Expected: file starts with the auto-generated comment, then `export default { ... }` with `title`, `nav`, `sidebar`, `search` keys.

**Step 4: Validate it parses as JS**

```bash
node -e "import('./vitepress/.vitepress/config.mjs').then(m => console.log('OK:', Object.keys(m.default).join(', ')))"
```

Expected: `OK: title, description, cleanUrls, nav, sidebar, search, outline`

**Step 5: Commit**

```bash
git add gen-config.py vitepress/.vitepress/config.mjs
git commit -m "feat(vitepress): generate config.mjs from converted tree"
```

---

## Task 6: Copy static assets (images)

**Files:** Copy tree under `vitepress/hpc/images/` (and any other referenced images).

**Step 1: Find all image references in the source**

```bash
grep -roh 'images/[A-Za-z0-9._-]\+\.\(svg\|png\|jpg\|jpeg\|gif\|webp\)' docs/notes/ | sort -u
```

Expected: A list of image paths used by the source RST files (likely under `hpc/`). These are the only files we need to copy.

**Step 2: Copy each referenced image directory**

For each unique parent directory in the list, copy it to the corresponding `vitepress/` location. For example, if the list shows `images/mpirun.svg` and `images/salloc.svg`, then:

```bash
mkdir -p vitepress/hpc
cp -R docs/notes/hpc/images vitepress/hpc/
ls vitepress/hpc/images/
```

Expected: same filenames as the source (`mpirun.svg`, `salloc.svg`).

**Step 3: Verify image references in the converted markdown**

```bash
grep -n 'images/' vitepress/hpc/*.md | head
```

Expected: references like `![...](images/...)` that resolve to the files just copied.

**Step 4: Commit**

```bash
git add vitepress/hpc/images/
git commit -m "feat(vitepress): copy image assets for hpc section"
```

---

## Task 7: Write the VitePress landing page `vitepress/index.md`

**Files:**
- Create: `vitepress/index.md` (overwrites the pandoc-generated placeholder)

**Step 1: Replace `vitepress/index.md` with curated content**

Write the following to `vitepress/index.md`:

```markdown
---
title: Pysheeet
---

# Pysheeet

A collection of useful Python code snippets, patterns, and idioms — organized
into focused cheat sheets. Originally a Sphinx site, now served as a fast,
modern VitePress build for personal use.

## Sections

- **[Quick Start](/basic/)** — Python syntax, data types, functions, classes, generators
- **[Asyncio](/asyncio/)** — async/await, event loops, servers
- **[Concurrency](/concurrency/)** — threading, multiprocessing, futures
- **[Database](/database/)** — SQLAlchemy ORM and query patterns
- **[Extension](/extension/)** — C extensions, ctypes, C-API
- **[HPC](/hpc/)** — Ray, Slurm
- **[Interview](/interview/)** — interview-style questions
- **[LLM](/llm/)** — large language model serving and benchmarks
- **[Network](/network/)** — sockets, SSL, SSH, async networking
- **[OS](/os/)** — file I/O, dates, OS interfaces
- **[Security](/security/)** — TLS, crypto, common vulnerabilities
- **[Appendix](/appendix/)** — specialized topics (GDB, NCCL, NVSHMEM, etc.)

## See Also

- [Python 3 new features](/python-new-py3)
```

**Step 2: Commit**

```bash
git add vitepress/index.md
git commit -m "feat(vitepress): write curated landing page"
```

---

## Task 8: Add small custom CSS for REPL prompt distinction

**Files:**
- Create: `vitepress/.vitepress/theme/custom.css`

**Step 1: Write the CSS**

```css
/* Subtle visual distinction for Python REPL prompt lines in code blocks.
   The pattern `>>> ...` inside ```python blocks is common in this codebase. */
.vp-doc div[class*="language-"] code .prompt,
.vp-doc div[class*="language-python"] code .tok-prefix {
    user-select: none;
    opacity: 0.55;
}
```

**Step 2: Wire it into the theme**

Create `vitepress/.vitepress/theme/index.js`:

```js
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default DefaultTheme
```

**Step 3: Commit**

```bash
git add vitepress/.vitepress/theme/
git commit -m "feat(vitepress): add custom theme for REPL prompt styling"
```

---

## Task 9: Write `vitepress/README.md`

**Files:**
- Create: `vitepress/README.md`

**Step 1: Write the README**

```markdown
# Pysheeet (VitePress)

Personal-use VitePress build of the pysheeet Python cheat sheets.

## Run locally

```bash
cd vitepress
npm install
npm run dev
```

Then open the URL VitePress prints (usually `http://localhost:5173`).

## Build for production

```bash
npm run build
npm run preview
```

## Regenerate from source

From the project root:

```bash
./convert.sh docs/notes vitepress
python3 cleanup.py vitepress
python3 gen-config.py vitepress
```

The source `.rst` files in `docs/notes/` are the source of truth and are not
modified by these scripts.
```

**Step 2: Commit**

```bash
git add vitepress/README.md
git commit -m "docs(vitepress): add vitepress README with run instructions"
```

---

## Task 10: Install dependencies and verify the dev server boots

**Files:** none modified

**Step 1: Install**

```bash
cd vitepress && npm install
```

Expected: `node_modules/` populated; final line includes "added N packages".

**Step 2: Boot the dev server in the background and capture output**

```bash
cd vitepress
nohup npm run dev > /tmp/vp-dev.log 2>&1 &
echo "PID: $!"
sleep 8
echo "--- log ---"
cat /tmp/vp-dev.log
```

Expected log content: includes a line like `➜  Local:   http://localhost:5173/` with no errors above it. If you see `ERROR` or `Failed to`, kill the process and debug.

**Step 3: Smoke-test a page with curl**

```bash
curl -sI http://localhost:5173/ | head -1
curl -sI http://localhost:5173/basic/python-basic | head -1
curl -sI http://localhost:5173/hpc/slurm | head -1
```

Expected: all three return `HTTP/1.1 200 OK`.

**Step 4: Kill the dev server**

```bash
pkill -f "vitepress dev" || true
```

**Step 5: Commit nothing**

If `package-lock.json` was generated, commit it for reproducible installs:

```bash
git add vitepress/package-lock.json
git commit -m "chore(vitepress): add package-lock.json"
```

---

## Task 11: Verify the production build succeeds

**Files:** none modified

**Step 1: Build**

```bash
cd vitepress && npm run build
```

Expected: command exits 0; final lines include `✓ building client + server bundles...` and `✓ rendering pages...`. Total page count should be roughly equal to the number of `.md` files.

**Step 2: Confirm output directory exists**

```bash
ls vitepress/.vitepress/dist/ | head
```

Expected: `assets/`, `index.html`, plus one `.html` per page (e.g. `basic/python-basic.html`).

**Step 3: Preview the build**

```bash
cd vitepress
nohup npm run preview > /tmp/vp-preview.log 2>&1 &
sleep 5
curl -sI http://localhost:4173/ | head -1
pkill -f "vitepress preview" || true
```

Expected: `HTTP/1.1 200 OK`.

**Step 4: Commit nothing unless something was generated**

The `.vitepress/dist/` directory is in `.gitignore` — nothing should be committed.

---

## Task 12: Final sweep — no `.rst` references remain

**Files:** none modified

**Step 1: Search the entire vitepress tree**

```bash
rg -l '\.rst' vitepress/ || echo "clean: no .rst references"
```

Expected: `clean: no .rst references`.

**Step 2: Search for any leftover RST directives in markdown**

```bash
rg -l '^\.\. (code-block|toctree|raw|meta|contents)::' vitepress/ || echo "clean: no RST directives"
```

Expected: `clean: no RST directives`.

**Step 3: Search for unconverted internal links**

```bash
rg -l '\]\([^)]+\.rst' vitepress/ || echo "clean: no .rst links"
```

Expected: `clean: no .rst links`.

**Step 4: No commit**

Verification only.

---

## Task 13: Spot-check 5 pages against the source

**Files:** none modified

**Step 1: Boot the dev server**

```bash
cd vitepress
nohup npm run dev > /tmp/vp-dev.log 2>&1 &
sleep 8
```

**Step 2: For each of the following pages, fetch the HTML and confirm no obvious errors:**

- `http://localhost:5173/basic/python-basic` — should render code blocks with Python highlighting
- `http://localhost:5173/asyncio/python-asyncio-basic` — should show the right-side outline
- `http://localhost:5173/database/python-sqlalchemy` — should render RST grid tables
- `http://localhost:5173/hpc/slurm` — should load the SVG images
- `http://localhost:5173/python-new-py3` — should be one long page with outline

```bash
for path in /basic/python-basic /asyncio/python-asyncio-basic /database/python-sqlalchemy /hpc/slurm /python-new-py3; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:5173${path}")
    echo "${code} ${path}"
done
```

Expected: all five return `200`.

**Step 3: Confirm images are served**

```bash
curl -sI http://localhost:5173/hpc/images/mpirun.svg | head -1
curl -sI http://localhost:5173/hpc/images/salloc.svg | head -1
```

Expected: `HTTP/1.1 200 OK` for each.

**Step 4: Kill the dev server**

```bash
pkill -f "vitepress dev" || true
```

**Step 5: No commit**

Manual verification only. If any page returns non-200, debug and fix before finishing.

---

## Task 14: Final commit and report

**Files:** none modified

**Step 1: Check git status**

```bash
git status
```

Expected: clean working tree (any `node_modules/` or `.vitepress/dist/` should be ignored).

**Step 2: Show the commit log on the feature branch**

```bash
git log --oneline master..HEAD
```

Expected: ~10 commits, one per major step (scaffold, convert, cleanup, config, images, landing, theme, readme, lock).

**Step 3: Report to user**

Summarize:
- Total .md files generated (should be ~55)
- Dev server runs at `http://localhost:5173/`
- Build runs at `npm run build`
- No `.rst` references remain
- All spot-checked pages return 200

**Step 4: Stop. Do not merge or push.**

Per the system instructions, the user must explicitly request merges/pushes.

---

## Reference

- Design doc: `docs/plans/2026-06-03-vitepress-migration-design.md`
- Working branch: `feature/vitepress-migration`
- Worktree: `.worktrees/vitepress-migration`
