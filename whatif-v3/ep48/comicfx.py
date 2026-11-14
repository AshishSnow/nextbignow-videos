"""Turn photos / cut-outs into vintage-comic prints: posterised colour, Ben-Day halftone in the shadows, ink outline, sticker edge."""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops, ImageDraw


def halftone_mask(lum, cell=10, angle=0):
    """lum 0..1 (H,W). returns dot mask (0/255) where dot radius grows with darkness."""
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.deg2rad(angle)
    u = xx * np.cos(a) + yy * np.sin(a); v = -xx * np.sin(a) + yy * np.cos(a)
    cu = (np.floor(u / cell) + 0.5) * cell; cv = (np.floor(v / cell) + 0.5) * cell
    d = np.sqrt((u - cu) ** 2 + (v - cv) ** 2)
    r = (1 - lum) ** 0.9 * cell * 0.62
    return (d < r).astype(np.uint8) * 255


def comicify(im, cell=8, sat=1.35, tint=(250, 238, 210)):
    rgba = im.convert('RGBA'); alpha = rgba.split()[3]
    rgb = rgba.convert('RGB')
    rgb = ImageEnhance.Color(rgb).enhance(sat)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.06)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.15)
    smooth = rgb.filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.MedianFilter(5))
    flat = ImageOps.posterize(smooth, 4)
    arr = np.asarray(flat).astype(np.float32) / 255
    lum = np.asarray(smooth.convert('L')).astype(np.float32) / 255
    t = np.array(tint, np.float32) / 255
    hi = np.clip((lum - 0.8) / 0.2, 0, 1)[..., None]
    arr = arr * (1 - hi * 0.5) + t * hi * 0.5
    m = halftone_mask(np.clip(lum * 1.6, 0, 1), cell, 45) / 255.0
    shade = np.clip((0.78 - lum) / 0.78, 0, 1)
    arr = arr * (1 - (m * 0.6 * shade)[..., None])
    edges = smooth.convert('L').filter(ImageFilter.GaussianBlur(1.5)).filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 12 else 0)
    edges = edges.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    e = np.asarray(edges).astype(np.float32)[..., None] / 255
    arr = arr * (1 - e * 0.8)
    out = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), 'RGB').convert('RGBA')
    out.putalpha(alpha)
    return out


def sticker(cut, ink=12, white=14):
    """black ink outline + white sticker border around a cut-out."""
    a = cut.split()[3].point(lambda v: 255 if v > 100 else 0)
    pad = ink + white + 4
    W, H = cut.size
    big = Image.new('RGBA', (W + 2 * pad, H + 2 * pad), (0, 0, 0, 0))
    A = Image.new('L', big.size, 0); A.paste(a, (pad, pad))
    a_ink = A.filter(ImageFilter.MaxFilter(2 * ink + 1))
    a_white = a_ink.filter(ImageFilter.MaxFilter(2 * white + 1))
    big.paste((255, 250, 238, 255), (0, 0), a_white)
    big.paste((12, 12, 14, 255), (0, 0), a_ink)
    big.alpha_composite(cut, (pad, pad))
    return big


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'cut'
    im = Image.open(src)
    im.thumbnail((1400, 1400))
    out = comicify(im)
    if mode == 'cut': out = sticker(out)
    out.save(dst)
    print(dst, out.size)
