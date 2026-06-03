#!/usr/bin/env python3
"""Compare word counts between RST source and MD output files."""
from pathlib import Path
import re


SRC = Path("docs/notes")
DST = Path("vitepress")


def strip_rst(text: str) -> str:
    """Strip all RST markup, leaving only plain text."""
    # Remove meta directives (multi-line, indented body)
    text = re.sub(
        r'^\.\. meta::.*?(?:^|\n)(?=\S)',
        '', text, flags=re.MULTILINE | re.DOTALL
    )
    # Remove code-block directives with their indented body
    text = re.sub(
        r'^\.\. code-block::.*?(?:^|\n)(?=\S)',
        '', text, flags=re.MULTILINE | re.DOTALL
    )
    # Remove other RST directives (note, warning, image, contents, etc.)
    text = re.sub(
        r'^\.\. (?:note|warning|tip|important|caution|seealso|versionadded|versionchanged|deprecated|image|contents|toctree|raw)::.*?(?:^|\n)(?=\S)',
        '', text, flags=re.MULTILINE | re.DOTALL
    )
    # Remove any remaining RST directive lines
    text = re.sub(r'^\.\. \w+::.*', '', text, flags=re.MULTILINE)
    # Remove indented directive arguments (continuation lines starting with ::)
    text = re.sub(r'^[ \t]+::[^\n]*', '', text, flags=re.MULTILINE)
    # Remove RST inline roles
    text = re.sub(r':\w+:`[^`]+`', '', text)
    # Remove RST inline literals (double backticks)
    text = re.sub(r'``[^`]+``', '', text)
    # Remove simple backtick inline code (pandoc may convert to single backticks)
    text = re.sub(r'`[^`]+`', '', text)
    # Remove RST hyperlink targets like .. _label:
    text = re.sub(r'^\.\. _[^:]+:', '', text, flags=re.MULTILINE)
    # Remove RST heading underlines
    text = re.sub(r'^[=\-~^\"\']+$', '', text, flags=re.MULTILINE)
    # Remove RST substitutions (|name|)
    text = re.sub(r'\|[^|]+\|', '', text)
    # Remove RST line blocks
    text = re.sub(r'^\| ', '', text, flags=re.MULTILINE)
    # Remove standalone bullets markers
    text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
    # Remove enumerated list markers
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    # Remove remaining special characters
    text = re.sub(r'[\*\_\>\|\\]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def strip_md(text: str) -> str:
    """Strip all Markdown/VitePress markup, leaving only plain text."""
    # Remove frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    # Remove code fences
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    # Remove links (keep link text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove heading markers
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove [[toc]] directive
    text = re.sub(r'\[\[toc\]\]', '', text)
    # Remove VitePress admonition markers
    text = re.sub(r':::\s*\w+', '', text)
    # Remove special characters
    text = re.sub(r'[\*\_\>\|\\]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def word_count(text: str, fmt: str = 'md') -> int:
    plain = strip_md(text) if fmt == 'md' else strip_rst(text)
    return len(plain.split()) if plain else 0


def main():
    rst_files = sorted(SRC.rglob("*.rst"))
    total_rst = 0
    total_md = 0
    mismatches = []

    print(f"{'File':<55} {'RST':>6} {'MD':>6} {'Diff':>6} {'%':>6}")
    print("-" * 80)

    for rst in rst_files:
        rel = rst.relative_to(SRC)
        md = DST / rel.with_suffix('.md')

        if not md.exists():
            print(f"{rel.as_posix():<55}  MISSING MD FILE")
            continue

        rst_wc = word_count(rst.read_text(encoding='utf-8'), 'rst')
        md_wc = word_count(md.read_text(encoding='utf-8'), 'md')

        total_rst += rst_wc
        total_md += md_wc

        pct = ((md_wc - rst_wc) / rst_wc * 100) if rst_wc > 0 else 0

        marker = ""
        if abs(pct) > 15:
            marker = " <<<"
            mismatches.append((rel.as_posix(), rst_wc, md_wc, pct))

        print(f"{rel.as_posix():<55} {rst_wc:>6} {md_wc:>6} {md_wc - rst_wc:>6} {round(pct, 1):>5}%{marker}")

    print("-" * 80)
    total_diff = total_md - total_rst
    total_pct = round((total_diff / total_rst * 100), 1) if total_rst > 0 else 0
    print(f"{'TOTAL':<55} {total_rst:>6} {total_md:>6} {total_diff:>6} {total_pct:>5}%")

    print(f"\nFiles with >15% deviation: {len(mismatches)}")
    for name, r, m, p in mismatches:
        print(f"  {name}: RST={r} MD={m} ({round(p,1)}%)")

    if mismatches:
        print("\nNOTE: Small deviations (<10%) are fine. Larger ones may indicate")
        print("content loss in code blocks (MD stripping handles ``` correctly)")
        print("or RST math/images/directives that don't have text equivalents.")


if __name__ == '__main__':
    main()
