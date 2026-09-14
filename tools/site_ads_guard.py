"""Check AdSense loader multiplicity without making network requests."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class AdsLoaderError(ValueError):
    pass


class LoaderParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'script':
            return
        src = dict(attrs).get('src', '')
        url = urlsplit(src)
        if url.hostname == 'pagead2.googlesyndication.com' and url.path == '/pagead/js/adsbygoogle.js':
            self.count += 1

    handle_startendtag = handle_starttag


def check_html(content, label, required=False):
    parser = LoaderParser()
    parser.feed(content)
    if parser.count > 1 or (required and parser.count != 1):
        raise AdsLoaderError(f'{label}: AdSense loader count {parser.count}; expected ' + ('1' if required else 'at most 1'))
    return parser.count


def validate(web_root, include_generated=True):
    root = Path(web_root)
    paths = [root / 'templates' / name for name in ('index_template.html', 'master_template.html')]
    if include_generated:
        paths += [p for p in root.rglob('*.html') if 'templates' not in p.relative_to(root).parts]
    result = {}
    for path in paths:
        required = path.parent.name in ('templates', 'posts') or path.name == 'index.html'
        result[str(path.relative_to(root))] = check_html(path.read_text(encoding='utf-8-sig'), path.name, required)
    return result


if __name__ == '__main__':
    result = validate(Path(__file__).resolve().parents[1] / 'kkuldanji_web')
    print(f'AdSense loader check passed: {len(result)} HTML files')
