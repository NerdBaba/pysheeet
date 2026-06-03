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
  - Replaces 'Table of Contents' placeholder text (from RST .. contents::) with [[toc]]
  - Converts GitHub alert syntax (> [!WARNING]) to VitePress admonitions (::: warning)
  - Fixes :ref: links from Sphinx (converts `` `→ path: text <notes/path:text>` `` to proper [text](path) links)
  - Fixes :doc: backtick references to proper markdown links
  - Fixes "See also" backtick paths to markdown links
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

# Matches standalone "Table of Contents" line (from RST .. contents::)
TOC_LINE = re.compile(r'^Table of Contents\s*$', re.MULTILINE)

# Matches GitHub alert syntax (> [!WARNING], > [!NOTE], etc.)
GITHUB_ALERT = re.compile(r'^> \[!(WARNING|NOTE|TIP|CAUTION|IMPORTANT)\]\n((?:> .*\n?)*)', re.MULTILINE)

# Matches :ref: style links from Sphinx that pandoc rendered as backtick text.
# Pattern: `→ section/page: Anchor Text <notes/section/page:Anchor Text>`
# or: `` → section/page: text <notes/section/page:text> `` (double backticks when text contains code)
REF_LINK_INLINE = re.compile(
    r'(?P<bt>`{1,2})(?:→\s*)?(?P<text>(?:(?!\s*<notes/)[^`])+?)\s*<notes/(?P<path>[a-z][a-z/.-]+):(?P<anchor>[^>`]+)>\s*(?P=bt)',
)

# Separate handler for double-backtick refs that contain escaped backticks inside
# e.g. `` → dict.keys() <notes/basic/python-dict:Get All Keys with ``dict.keys()``> ``
# Note: there may be whitespace between > and closing ``
REF_LINK_DOUBLE_BT = re.compile(
    r'``(?:→\s*)?(?P<text_d>.*?)<notes/(?P<path_d>[a-z][a-z/.-]+):(?P<anchor_d>(?:[^>`\\]|\\.)+)>\s*``',
)

# Matches backtick-wrapped paths like `../basic/index` or `notes/path`
BACKTICK_PATH = re.compile(r'`(\.\./[a-z][a-z/]*(?:/index)?)`')

# Remaining :doc: refs that became backtick-wrapped names (handled as a post-cleanup pass)


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


def fix_toc_text(text: str) -> str:
    """Replace standalone 'Table of Contents' with VitePress [[toc]] directive."""
    return TOC_LINE.sub('[[toc]]', text)


def fix_github_alerts(text: str) -> str:
    """Convert GitHub alert syntax to VitePress admonition containers."""
    def repl(m: re.Match) -> str:
        alert_type = m.group(1).lower()
        # Map GitHub alert types to VitePress container types
        vp_map = {
            'warning': 'warning',
            'note': 'tip',
            'tip': 'tip',
            'caution': 'danger',
            'important': 'tip',
        }
        vp_type = vp_map.get(alert_type, 'tip')
        body = m.group(2)
        # Strip '> ' prefix from each line
        body = re.sub(r'^> ', '', body, flags=re.MULTILINE)
        return f'::: {vp_type}\n{body.rstrip()}\n:::\n\n'
    return GITHUB_ALERT.sub(repl, text)


def slugify(text: str) -> str:
    """Convert heading text to a VitePress anchor ID."""
    s = text.lower().strip()
    s = s.replace('\\', '')
    s = re.sub(r'[`\'"]', '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s


def _ref_replacer(m: re.Match, text_key='text', path_key='path', anchor_key='anchor') -> str:
    """Shared replacer for Sphinx :ref: link conversion."""
    anchor_text = m.group(text_key).strip()
    path = m.group(path_key).strip()
    section = m.group(anchor_key).strip()
    # Unescape backslash-escaped characters (e.g. \`\` -> ``)
    section = section.replace('\\`', '`')
    anchor_text = anchor_text.replace('\\`', '`')
    # The link text is after the last colon (if any), or the whole text
    link_text = anchor_text.rsplit(':', 1)[-1].strip() if ':' in anchor_text else anchor_text
    if not link_text:
        link_text = section
    # Remove any backticks from link text (shouldn't be any after unescaping)
    link_text = link_text.replace('`', '')
    anchor = slugify(section)
    # No trailing slash before anchor — cleanUrls means /path#anchor, not /path/#anchor
    return f'[{link_text}](/{path}#{anchor})'


def fix_ref_links(text: str) -> str:
    """Convert Sphinx :ref: artifacts to proper markdown links.

    Handles patterns like:
      `→ Default Arguments <notes/basic/python-func:Default Arguments>`
      `` → dict.keys() <notes/basic/python-dict:Get All Keys with ``dict.keys()``> ``
    """
    text = REF_LINK_INLINE.sub(
        lambda m: _ref_replacer(m, 'text', 'path', 'anchor'), text
    )
    text = REF_LINK_DOUBLE_BT.sub(
        lambda m: _ref_replacer(m, 'text_d', 'path_d', 'anchor_d'), text
    )
    return text


def fix_backtick_paths(text: str) -> str:
    """Convert backtick-wrapped paths like `../basic/index` to markdown links."""
    def repl(m: re.Match) -> str:
        path = m.group(1)
        # Extract readable name
        name = path.split('/')[-2] if path.endswith('/index') else path.split('/')[-1]
        name = name.replace('-', ' ').title()
        # Link without trailing slash — VitePress cleanUrls doesn't need it
        link = path.removesuffix('/index')
        return f'[{name}]({link})'
    return BACKTICK_PATH.sub(repl, text)


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text
    text = strip_meta(text)
    text = strip_raw_html(text)
    text = fix_rst_links(text)
    text = fix_code_fences(text)
    text = strip_toctree_artifacts(text)
    text = fix_toc_text(text)
    text = fix_github_alerts(text)
    text = fix_ref_links(text)
    text = fix_backtick_paths(text)
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
