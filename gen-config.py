#!/usr/bin/env python3
"""
Generate .vitepress/config.mjs from the converted Markdown tree.

Each top-level subfolder of vitepress/ becomes a collapsible sidebar group;
all groups are shown globally so the sidebar acts as a site-wide table of contents.

Also generates sitemap.xml, robots.txt, and RSS feed.
"""
from __future__ import annotations
import sys
from pathlib import Path
import json
from datetime import datetime

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("vitepress")
CONFIG = ROOT / ".vitepress" / "config.mjs"
SITE_URL = "https://www.pythonsheets.com"

CATEGORY_ORDER = [
    'interview', 'basic', 'os', 'cli', 'concurrency', 'asyncio',
    'network', 'database', 'web', 'security', 'testing', 'extension',
    'llm', 'hpc', 'data-science', 'appendix',
]

FILE_ORDER: dict[str, list[str]] = {
    'basic': [
        'python-basic', 'python-future', 'python-func', 'python-object',
        'python-typing', 'python-list', 'python-set', 'python-dict',
        'python-heap', 'python-generator', 'python-unicode', 'python-rexp',
        'python-itertools', 'python-collections', 'python-functools',
        'python-dataclasses', 'python-profiling',
    ],
    'os': [
        'python-date', 'python-os', 'python-io',
        'python-pathlib', 'python-logging',
    ],
    'cli': [
        'python-argparse', 'python-click',
    ],
    'concurrency': [
        'python-threading', 'python-multiprocessing', 'python-futures',
    ],
    'asyncio': [
        'python-asyncio-guide', 'python-asyncio-basic',
        'python-asyncio-server', 'python-asyncio-advanced',
    ],
    'network': [
        'python-socket', 'python-socket-server', 'python-socket-async',
        'python-socket-ssl', 'python-socket-sniffer', 'python-ssh',
    ],
    'database': [
        'python-sqlalchemy', 'python-sqlalchemy-orm', 'python-sqlalchemy-query',
    ],
    'web': [
        'python-fastapi',
    ],
    'security': [
        'python-crypto', 'python-tls', 'python-vulnerability',
    ],
    'testing': [
        'python-pytest', 'python-unittest-mock',
    ],
    'extension': [
        'python-ctypes', 'python-capi', 'python-cext-modern', 'cpp-from-python',
    ],
    'llm': [
        'pytorch', 'megatron', 'llm-serving', 'llm-bench',
    ],
    'hpc': [
        'slurm', 'ray',
    ],
    'data-science': [
        'python-numpy', 'python-pandas',
    ],
    'appendix': [
        'nvshmem-multi-nic', 'disaggregated-prefill-decode',
        'megatron-efa-monitoring', 'nccl-gin',
        'python-walrus', 'python-gdb',
    ],
}

CATEGORIES = [p.name for p in ROOT.iterdir()
              if p.is_dir() and not p.name.startswith('.') and p.name != 'node_modules'
              and p.name in CATEGORY_ORDER]

CATEGORIES.sort(key=lambda c: CATEGORY_ORDER.index(c))

TOP_LEVEL_PAGES = [f for f in ROOT.glob('*.md')
                   if f.name not in ('index.md', '404.md')]

ALL_PAGES: list[str] = []


def page_link(p: Path, root: Path) -> str:
    rel = p.relative_to(root).with_suffix('')
    return '/' + str(rel).replace('\\', '/')


def sort_files(files: list[Path], cat: str) -> list[Path]:
    order = FILE_ORDER.get(cat, [])
    if not order:
        return sorted(files)
    def sort_key(f: Path) -> int:
        stem = f.stem
        try:
            return order.index(stem)
        except ValueError:
            return len(order)
    return sorted(files, key=sort_key)


def collect_pages() -> None:
    ALL_PAGES.clear()
    for f in TOP_LEVEL_PAGES:
        ALL_PAGES.append(page_link(f, ROOT))
    for cat in CATEGORIES:
        catdir = ROOT / cat
        for f in sort_files(list(catdir.glob('*.md')), cat):
            ALL_PAGES.append(page_link(f, ROOT))


def sidebar_global() -> list[dict]:
    groups: list[dict] = []
    if TOP_LEVEL_PAGES:
        items = []
        for f in TOP_LEVEL_PAGES:
            title = f.stem.replace('-', ' ').replace('_', ' ').title()
            items.append({'text': title, 'link': page_link(f, ROOT)})
        groups.append({
            'text': 'General',
            'collapsible': True,
            'collapsed': True,
            'items': items,
        })
    for cat in CATEGORIES:
        catdir = ROOT / cat
        files = sort_files(list(catdir.glob('*.md')), cat)
        items = []
        for f in files:
            if f.name == 'index.md':
                items.insert(0, {'text': 'Overview', 'link': f'/{cat}/'})
                continue
            title = f.stem.replace('-', ' ').replace('_', ' ').title()
            items.append({'text': title, 'link': page_link(f, ROOT)})
        groups.append({
            'text': cat.replace('-', ' ').title(),
            'collapsible': True,
            'collapsed': True,
            'items': items,
        })
    return groups


def nav_entries() -> list[dict]:
    return []


def head_tags() -> list[list]:
    return [
        ['meta', {'property': 'og:site_name', 'content': 'Pysheeet'}],
        ['meta', {'property': 'og:type', 'content': 'website'}],
        ['meta', {'property': 'og:locale', 'content': 'en_US'}],
        ['meta', {'name': 'twitter:card', 'content': 'summary_large_image'}],
        ['link', {'rel': 'alternate', 'type': 'application/rss+xml',
                   'title': 'Pysheeet RSS Feed', 'href': '/rss.xml'}],
    ]


def render_config() -> str:
    cfg = {
        'title': 'Pysheeet',
        'description': 'Comprehensive Python cheat sheets covering core language, data structures, networking, databases, async, CLI, testing, data science, web development, and more.',
        'cleanUrls': True,
        'lastUpdated': True,
        'head': head_tags(),
        'themeConfig': {
            'logo': '/logo.svg',
            'nav': nav_entries(),
            'sidebar': sidebar_global(),
            'search': {'provider': 'local'},
            'outline': {'level': [2, 3]},
            'docFooter': {'prev': 'Previous', 'next': 'Next'},
            'socialLinks': [
                {'icon': 'github', 'link': 'https://github.com/crazyguitar/pysheeet'},
            ],
        },
    }
    body = json.dumps(cfg, indent=2)
    transform_head = (
        '\n  transformHead({ pageData }) {\n'
        f'    const canonical = `{SITE_URL}/${{pageData.relativePath.replace(/\\\\/g, "/").replace(/\\.md$/, "")}}`\n'
        '    return [\n'
        '      ["link", { rel: "canonical", href: canonical }],\n'
        '      ["meta", { property: "og:url", content: canonical }],\n'
        '      ["meta", { property: "og:title", content: pageData.title || "Pysheeet" }],\n'
        '      ["meta", { property: "og:description", content: pageData.description || "Comprehensive Python cheat sheets" }],\n'
        '      ["meta", { name: "twitter:title", content: pageData.title || "Pysheeet" }],\n'
        '      ["meta", { name: "twitter:description", content: pageData.description || "Comprehensive Python cheat sheets" }],\n'
        '    ]\n'
        '  },\n'
    )
    return (
        f"// Auto-generated by gen-config.py — do not edit by hand.\n"
        f"// Regenerate with: python3 gen-config.py vitepress\n\n"
        f"export default {body[:-1]},\n"
        f"{transform_head}"
        f"}};\n"
    )


def generate_sitemap() -> str:
    now = datetime.now().date().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>{SITE_URL}/</loc><lastmod>{now}</lastmod><priority>1.0</priority></url>',
    ]
    for page in ALL_PAGES:
        priority = '0.5' if page.startswith('/appendix/') else '0.8'
        lines.append(
            f'  <url><loc>{SITE_URL}{page}</loc><lastmod>{now}</lastmod><priority>{priority}</priority></url>'
        )
    lines.append('</urlset>\n')
    return '\n'.join(lines)


def generate_rss() -> str:
    now = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    items = []
    for page in ALL_PAGES:
        title = page.replace('/', ' ').replace('-', ' ').strip().title() or 'Pysheeet'
        items.append(f'''    <item>
      <title>{title}</title>
      <link>{SITE_URL}{page}</link>
      <guid>{SITE_URL}{page}</guid>
      <description>Python cheat sheet: {title}</description>
    </item>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Pysheeet</title>
    <link>{SITE_URL}</link>
    <description>Comprehensive Python cheat sheets</description>
    <language>en-us</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
'''


def main() -> int:
    collect_pages()
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(render_config(), encoding='utf-8')
    print(f'wrote {CONFIG}')

    public_dir = ROOT / 'public'
    public_dir.mkdir(parents=True, exist_ok=True)

    sitemap = public_dir / 'sitemap.xml'
    sitemap.write_text(generate_sitemap(), encoding='utf-8')
    print(f'wrote {sitemap}')

    rss = public_dir / 'rss.xml'
    rss.write_text(generate_rss(), encoding='utf-8')
    print(f'wrote {rss}')

    robots = public_dir / 'robots.txt'
    robots.write_text(
        f'User-agent: *\n'
        f'Allow: /\n'
        f'Sitemap: {SITE_URL}/sitemap.xml\n',
        encoding='utf-8',
    )
    print(f'wrote {robots}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
