"""commons.py search <q> | get <title> <out>  -- Wikimedia Commons PD/CC0 finder."""
import sys, json, urllib.parse, urllib.request, urllib.error, time
UA = {'User-Agent': 'OMBstudio/1.0 (shorts research; contact via github AshishSnow)'}
API = 'https://commons.wikimedia.org/w/api.php?'
def fetch(url):
    for i in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(20 + 20 * i)
    raise SystemExit('rate limited')
def q(params): return json.loads(fetch(API + urllib.parse.urlencode(params)))
if sys.argv[1] == 'search':
    d = q(dict(action='query', generator='search', gsrsearch=sys.argv[2] + ' filetype:bitmap', gsrnamespace=6, gsrlimit=int(sys.argv[3]) if len(sys.argv) > 3 else 15,
               prop='imageinfo', iiprop='url|size|extmetadata', iiurlwidth=1600, format='json'))
    for p in d.get('query', {}).get('pages', {}).values():
        ii = p['imageinfo'][0]; m = ii.get('extmetadata', {}); lic = m.get('LicenseShortName', {}).get('value', '?')
        ok = any(k in lic.lower() for k in ('public domain', 'cc0', 'pd'))
        print(('OK ' if ok else '-- ') + f"{lic[:22]:22} {ii['width']}x{ii['height']} {p['title']}")
else:
    d = q(dict(action='query', titles=sys.argv[2], prop='imageinfo', iiprop='url|extmetadata', iiurlwidth=1280, format='json'))
    p = list(d['query']['pages'].values())[0]; ii = p['imageinfo'][0]
    u = ii['url'] if not ii['url'].lower().endswith(('.tif', '.tiff')) else ii['thumburl']
    open(sys.argv[3], 'wb').write(fetch(u))
    m = ii['extmetadata']; print(json.dumps(dict(title=p['title'], license=m.get('LicenseShortName', {}).get('value'), artist=m.get('Artist', {}).get('value', '')[:120], page=ii['descriptionurl'])))
