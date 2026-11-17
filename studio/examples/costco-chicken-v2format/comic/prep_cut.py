"""make sticker cut-outs: rembg -> comicify -> sticker. usage: prep_cut.py '{"chicken":["chicken",0]}'"""
import json, sys, os
from PIL import Image
from rembg import remove, new_session
SESS = new_session("isnet-general-use")
from comicfx import comicify, sticker
C = json.load(open('img/cand/cands.json')); OUT = 'cc/img'
cr = json.load(open(f'{OUT}/credits.json')) if os.path.exists(f'{OUT}/credits.json') else {}
for k, (ck, i) in json.loads(sys.argv[1]).items():
    r = C[ck][i]; im = Image.open(r['file']).convert('RGB'); im.thumbnail((1400, 1400))
    cut = remove(im, session=SESS)                                   # RGBA
    bb = cut.getbbox(); cut = cut.crop(bb)
    rgb = comicify(cut.convert('RGB')).convert('RGBA'); rgb.putalpha(cut.split()[3])
    sticker(rgb).save(f'{OUT}/{k}_cut.png')
    cr[k] = dict(author=r['author'], license=r['license'], title=r['title'], page=r['page']); print(k, r['title'], cut.size)
json.dump(cr, open(f'{OUT}/credits.json', 'w'), indent=1)
