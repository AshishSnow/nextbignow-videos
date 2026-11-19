"""usage: sticker.py src.jpg out.png [l,t,r,b]  -> comic sticker (cut-out, posterize, ink edges, cream border + ink outline)"""
import sys
from rembg import remove, new_session
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np
from scipy import ndimage
s = new_session('isnet-general-use')
def sticker(src, out, box=None):
    im = Image.open(src).convert('RGB')
    if box: im = im.crop(box)
    cut = remove(im, session=s); a = np.array(cut); al = a[..., 3] > 128
    al = ndimage.binary_opening(al, iterations=2)
    lab, n = ndimage.label(al); sizes = ndimage.sum(al, lab, range(1, n + 1)); al = lab == (1 + int(np.argmax(sizes))); al = ndimage.binary_fill_holes(al)
    m = Image.fromarray((al * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1)).point(lambda v: 255 if v > 127 else 0)
    im = im.convert('RGBA'); im.putalpha(m); im = im.crop(im.getbbox())
    rgb = im.convert('RGB'); rgb = ImageEnhance.Color(rgb).enhance(1.25); rgb = ImageEnhance.Contrast(rgb).enhance(1.12); rgb = ImageOps.posterize(rgb, 6)
    edges = rgb.convert('L').filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 80 else 0)
    rgbn = np.array(rgb); e = np.array(edges) > 0; rgbn[e] = (rgbn[e] * 0.5).astype('uint8')
    al = np.array(im.split()[3]); pad = 40; W, H = im.size
    big = Image.new('L', (W + 2 * pad, H + 2 * pad), 0); big.paste(Image.fromarray(al), (pad, pad))
    cream = big.filter(ImageFilter.MaxFilter(25)); ink = cream.filter(ImageFilter.MaxFilter(9))
    o = Image.new('RGBA', big.size, (0, 0, 0, 0)); o.paste((30, 22, 20, 255), (0, 0), ink); o.paste((252, 241, 210, 255), (0, 0), cream)
    ph = Image.fromarray(rgbn).convert('RGBA'); ph.putalpha(Image.fromarray(al)); o.alpha_composite(ph, (pad, pad)); o.save(out); print(out, o.size)
if __name__ == '__main__':
    sticker(sys.argv[1], sys.argv[2], tuple(map(int, sys.argv[3].split(','))) if len(sys.argv) > 3 else None)
