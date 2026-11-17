#!/usr/bin/env python3
"""Check generated pages, historical public URLs, and all local HTML links."""
import json
import re
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
origin = 'https://leopoldomt.github.io'
failures = []
def check(condition, message):
    if not condition:
        failures.append(message)

def exists(url):
    path = root / unquote(urlsplit(url).path).lstrip('/')
    return path.is_file() or (path / 'index.html').is_file()

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if attrs.get('srcset'):
            self.links.extend(p.strip().split()[0] for p in attrs['srcset'].split(',') if p.strip())

published = Path('migration/published-paths.txt').read_text().splitlines()
# HTML routes and every PDF are public contracts. Old runtime assets and
# accidentally published source/tooling files are separately reported.
contracts = [p for p in published if p.endswith(('.html', '.pdf'))]
contracts = sorted(set(contracts + ['_pages/about_einstein.md']))
for path in contracts:
    check((root / path).is_file(), 'Missing published path: /' + path)

home = (root / 'index.html').read_text()
pubs = (root / 'publications/index.html').read_text()
check('Leopoldo Teixeira' in home, 'Home: missing name')
check('lmt.jpg' in home, 'Home: missing profile image')
check('Room C012' in home, 'Home: missing office')
check('selected publications' in home, 'Home: missing selected publications')
latest_news = max(Path('_news').glob('*.md'))
latest_title = re.search(r'^title:\s*(.+)$', latest_news.read_text(), re.M).group(1).strip('\"\'')
check(latest_title in unescape(home), 'Home: missing latest news')
check('https://leopoldomt.github.io/' in home, 'Home: missing production canonical URL')
check('/al-folio/' not in home, 'Home: leaked starter baseurl')
check('Albert Einstein' not in home + pubs, 'Leaked starter identity')
# Compare actual BibTeX keys with rendered publication anchors using a build-
# independent parser for the field subset used here.
bib = Path('_bibliography/papers.bib').read_text()
entries = list(re.finditer(r'@(?!(?:string|comment|preamble)\b)\w+\s*\{\s*([^,]+),', bib, re.I))
selected = []
for i, match in enumerate(entries):
    key = match.group(1).strip()
    text = bib[match.end():entries[i+1].start() if i+1 < len(entries) else len(bib)]
    check(f'id="{key}"' in pubs, 'Missing publication: ' + key)
    if re.search(r'\bselected\s*=\s*\{true\}', text, re.I):
        selected.append(key)
        check(f'id="{key}"' in home, 'Missing selected publication: ' + key)
    for pdf in re.findall(r'\bpdf\s*=\s*\{([^}]+)\}', text):
        if '://' not in pdf:
            check(exists('/assets/pdf/' + pdf), 'Missing bibliography PDF: ' + pdf)

broken = []
html_files = list(root.rglob('*.html'))
for file in html_files:
    parser = Links()
    parser.feed(file.read_text(errors='replace'))
    route = '/' + file.relative_to(root).as_posix()
    if route.endswith('index.html'):
        route = route[:-10]
    for link in parser.links:
        if not link or link.startswith('#'):
            continue
        absolute = urlsplit(urljoin(origin + route, link))
        if absolute.scheme not in ('http', 'https') or absolute.netloc != urlsplit(origin).netloc:
            continue
        if not exists(absolute.path):
            broken.append({'page': route, 'target': link})
check(not broken, f'{len(broken)} broken local HTML links')
summary = {
    'destination': str(root),
    'historical_page_and_pdf_paths_checked': len(contracts),
    'html_files_checked': len(html_files),
    'publications_checked': len(entries),
    'selected_publications_checked': len(selected),
    'missing_old_files': [p for p in published if not (root / p).is_file()],
    'broken_local_links': broken,
    'failures': failures,
}
print(json.dumps(summary, indent=2))
sys.exit(bool(failures))
