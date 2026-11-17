import json, sys, os
from PIL import Image
from comicfx import comicify
C = json.load(open('img/cand/cands.json')); OUT = 'cr/img'; os.makedirs(OUT, exist_ok=True)
pick = json.loads(sys.argv[1])  # {key: [candkey, index]}
cr = json.load(open(f'{OUT}/credits.json')) if os.path.exists(f'{OUT}/credits.json') else {}
for k, (ck, i) in pick.items():
    r = C[ck][i]; im = Image.open(r['file']); im.thumbnail((1600, 1600))
    comicify(im).save(f'{OUT}/{k}_comic.png'); cr[k] = dict(author=r['author'], license=r['license'], title=r['title'], page=r['page'])
    print(k, r['title'])
json.dump(cr, open(f'{OUT}/credits.json', 'w'), indent=1)
