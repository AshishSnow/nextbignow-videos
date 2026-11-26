"""thumbget.py <File:Name> <out> [width] — fetch a Wikimedia Commons standard-size thumbnail directly (no API call)."""
import sys, hashlib, urllib.request, urllib.parse
t = sys.argv[1].replace('File:', '').replace(' ', '_'); out = sys.argv[2]; w = sys.argv[3] if len(sys.argv) > 3 else '1280'
h = hashlib.md5(t.encode()).hexdigest(); q = urllib.parse.quote(t)
base = f'https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/'
name = (f'lossy-page1-{w}px-{q}.jpg' if t.lower().endswith(('.tif', '.tiff')) else f'{w}px-{q}' + ('.png' if t.lower().endswith('.webp') else ''))
r = urllib.request.Request(base + name, headers={'User-Agent': 'OMBStudioBot/1.0 (https://github.com/AshishSnow/nextbignow-videos) python-urllib/3.13'})
data = urllib.request.urlopen(r, timeout=60).read(); open(out, 'wb').write(data); print(len(data))
