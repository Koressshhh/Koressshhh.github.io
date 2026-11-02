"""Basic structural checks for the published static site; no third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids, self.links = [], set(), []
        self.h1, self.title, self.css = 0, False, False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag not in VOID:
            self.stack.append(tag)
        if tag == 'h1':
            self.h1 += 1
        if tag == 'title':
            self.title = True
        if tag == 'html' and not attrs.get('lang'):
            ERRORS.append('HTML language is missing')
        if tag == 'img' and not attrs.get('alt'):
            ERRORS.append('Image alternative text is missing')
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                ERRORS.append('Duplicate id: ' + attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.css = attrs.get('href') == 'style.css'
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            ERRORS.append('Mismatched closing tag: ' + tag)
        else:
            self.stack.pop()


def main():
    parser = SiteParser()
    parser.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    if parser.stack:
        ERRORS.append('Unclosed tags: ' + ', '.join(parser.stack))
    if parser.h1 != 1 or not parser.title or not parser.css:
        ERRORS.append('Expected one h1, title and style.css link')
    for target in parser.links:
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        if url.path and not (ROOT / unquote(url.path)).is_file():
            ERRORS.append('Missing local file: ' + url.path)
        if not url.path and url.fragment and url.fragment not in parser.ids:
            ERRORS.append('Missing section: ' + url.fragment)
    css = (ROOT / 'style.css').read_text(encoding='utf-8')
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', css)
    balance = 0
    for char in css:
        if char == '{':
            balance += 1
        elif char == '}':
            balance -= 1
        if balance < 0:
            ERRORS.append('Unexpected closing CSS brace')
            break
    if balance:
        ERRORS.append('Unbalanced CSS braces')
    if ERRORS:
        print('\n'.join('ERROR: ' + item for item in ERRORS))
        return 1
    print(f'PASS: HTML structure, {len(parser.links)} links/assets and CSS braces')
    return 0


if __name__ == '__main__':
    sys.exit(main())
