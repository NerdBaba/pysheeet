#!/usr/bin/env python3
"""
Post-pandoc cleanup for the VitePress conversion.

Fixes:
  - Internal .rst -> .md links
  - Code-fence language hints (default to 'python' when missing and content looks like Python or REPL)
  - Normalizes uncommon language names ('python3' -> 'python', 'cython' -> 'python')
  - Drops .. meta:: blocks
  - Adds frontmatter with a title derived from the first H1
  - Strips .. raw:: html blocks (their content was for the README, not the docs)
  - Strips toctree artifacts (space-separated filenames from pandoc-rendered .. toctree::)
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
FENCE = re.compile(r'^```[ \t]*(\w*)\n(.*?)^```', re.MULTILINE | re.DOTALL)
LANGUAGE_MAP = {'python3': 'python', 'cython': 'python'}
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
    """Default untagged fences to 'python' when they look like Python/REPL.
    Normalizes uncommon language names via LANGUAGE_MAP."""
    def repl(m: re.Match) -> str:
        lang, body = m.group(1), m.group(2)
        if lang:
            lang = LANGUAGE_MAP.get(lang, lang)
            return f'```{lang}\n{body}```'
        if PY_HINT_NEEDED.match(m.group(0)):
            return f'```python\n{body}```'
        return m.group(0)
    return FENCE.sub(repl, text)


def strip_meta(text: str) -> str:
    return META_DIRECTIVE.sub('', text)


def strip_raw_html(text: str) -> str:
    return RAW_HTML_DIRECTIVE.sub('', text)


def strip_toctree_artifacts(text: str) -> str:
    """Remove pandoc-rendered toctree artifacts from the end of files.
    These appear as a line of space-separated filenames, e.g.
    'python-basic python-future python-func'.
    """
    lines = text.splitlines(keepends=True)
    while lines and re.match(
        r'^[a-z][a-z0-9-]+(?: [a-z][a-z0-9-]+)+\n?$',
        lines[-1],
    ):
        lines.pop()
    return ''.join(lines)


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text
    text = strip_meta(text)
    text = strip_raw_html(text)
    text = fix_rst_links(text)
    text = fix_code_fences(text)
    text = strip_toctree_artifacts(text)
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
