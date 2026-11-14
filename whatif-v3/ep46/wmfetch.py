"""Search Wikimedia Commons, pick the first freely licensed photo per query, download ~2000px, record credit.
usage: python wmfetch.py <outdir> "<key>|<query1>;<query2>" ...   (tries queries in order, moves on if none found)"""
import sys, os, json, time, re, urllib.parse, urllib.request

UA = 'NextBigNowVideoBot/1.0 (https://github.com/AshishSnow/nextbignow-videos)'
API = 'https://commons.wikimedia.org/w/api.php'
OK = re.compile(r'^(cc0|cc[- ]by(-sa)?[- ]?[\d.]*|public domain|pd.*)', re.I)


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r: return r.read()
        except Exception as e:
            if '429' in str(e) or '503' in str(e): time.sleep(8 * (i + 1)); continue
            raise
    raise RuntimeError('rate limited: ' + url)


def api(**p):
    p.update(format='json')
    return json.loads(get(API + '?' + urllib.parse.urlencode(p)))


def clean(s): return re.sub(r'<[^>]+>', '', s or '').strip()


def find(q, n=12):
    if q.startswith('File:'):
        r = api(action='query', titles=q, prop='imageinfo', iiprop='url|extmetadata|size|mime', iiurlwidth=1920)
    else:
        r = api(action='query', generator='search', gsrsearch=q + ' filetype:bitmap', gsrnamespace=6, gsrlimit=n,
                prop='imageinfo', iiprop='url|extmetadata|size|mime', iiurlwidth=1920)
    pages = sorted(r.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
    for p in pages:
        ii = (p.get('imageinfo') or [{}])[0]
        md = ii.get('extmetadata', {})
        lic = clean(md.get('LicenseShortName', {}).get('value'))
        if not OK.match(lic) or ii.get('mime') not in ('image/jpeg', 'image/png'): continue
        if ii.get('width', 0) < 1920 or '/thumb/' not in (ii.get('thumburl') or ''): continue
        return dict(title=p['title'], url=ii['thumburl'].split('?')[0].replace('://thumb.wikimedia.org/', '://upload.wikimedia.org/'), page=ii.get('descriptionurl'),
                    author=clean(md.get('Artist', {}).get('value'))[:80], license=lic)
    return None


out = sys.argv[1]; os.makedirs(out, exist_ok=True)
cred_path = os.path.join(out, 'credits.json')
credits = json.load(open(cred_path)) if os.path.exists(cred_path) else {}
for arg in sys.argv[2:]:
    key, qs = arg.split('|', 1)
    if key in credits: print(key, 'already have'); continue
    hit = None
    for q in qs.split(';'):
        hit = find(q.strip()); time.sleep(1.5)
        if hit: break
        print(key, 'not found for', q, '-> next')
    if not hit: print(key, 'SKIPPED'); continue
    ext = '.png' if hit['url'].lower().endswith('.png') else '.jpg'
    fn = os.path.join(out, key + ext)
    open(fn, 'wb').write(get(hit['url'])); time.sleep(1.5)
    hit['file'] = fn; credits[key] = hit
    print(key, '->', hit['title'], '|', hit['author'], '|', hit['license'])
    json.dump(credits, open(cred_path, 'w'), indent=1)
