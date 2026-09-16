from pathlib import Path
import sys

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R/'tools'))
from site_ads_guard import check_html, validate, AdsLoaderError

loader = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=test"></script>'
assert check_html(loader, 'single', required=True) == 1
assert check_html('<!--'+loader+'-->'+loader, 'comment ignored', required=True) == 1
assert check_html('<script>window.adsbygoogle=[];</script>', 'queue') == 0
for content, required in [(loader+loader, True), ('', True), (loader+loader.replace('client=test', 'client=other'), False)]:
    try:
        check_html(content, 'invalid fixture', required)
    except AdsLoaderError:
        pass
    else:
        raise AssertionError('invalid fixture was accepted')
validate(R/'kkuldanji_web', include_generated=False)
print('Missing / duplicate / comment / queue fixtures and templates passed')
