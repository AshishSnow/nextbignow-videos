"""Grid-ready covers (1080x1920, everything that matters inside the 3:4 profile-grid crop y=240..1680)."""
import os, sys
os.environ.setdefault('GR_DIR', 'grid'); os.environ.setdefault('CB_DIR', 'cable')
import skia
from toon import W, H, R, paint, stroke, lin, argb
from edkit import *
from edkit import _grain
import render_grid as G
import render_cable as C

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'covers')
os.makedirs(OUT, exist_ok=True)


def save(surf, name):
    surf.makeImageSnapshot().save(os.path.join(OUT, name), skia.kPNG)


def tag(c, s, y=300, col=RED, txtc=PAPER):
    w = tw(s, 'mono', 30) + 40 if 'tw' in globals() else 420
    pill(c, 540, y, s, 1.0, col=col, txt=txtc, size=30)


def ep46():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    bg_cream(c, 0)
    c.drawCircle(540, 1330, 400, paint(RED))
    G.cutout(c, 'R5_tower_cut.png', 540, 1660, 760, 1.0)
    text(c, '60', 70, 810, 'blk', 380, INK, track=-0.06)
    text(c, 'data centers', 565, 650, 'blk', 64, INK)
    text(c, 'vanished', 565, 720, 'blk', 64, INK)
    text(c, 'in one night.', 565, 790, 'blk', 64, RED)
    pill(c, 540, 330, 'AI vs THE POWER GRID', 1.0, col=INK, size=40)
    mono(c, 'VIRGINIA · JULY 2024', 92, 440, 28, GREY)
    save(surf, 'ep46_cover.png')


def ep45():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    C.bg_sea(c, 3.0, floor=1560)
    C.cable_line(c, [(-20, 1600), (1100, 1590)], 1.0, t=1.0, w=22)
    C.cross_section(c, 540, 1380, 1.15)
    text(c, '99%', 70, 900, 'blk', 400, PAPER, track=-0.05)
    text(c, 'of the internet', 90, 1010, 'blk', 80, PAPER)
    text(c, 'is under the sea.', 90, 1095, 'blk', 80, YEL)
    pill(c, 540, 330, 'WHAT IF IT GETS CUT?', 1.0, col=RED, size=40)
    save(surf, 'ep45_cover.png')


def preview():
    from PIL import Image
    ims = []
    for n in ('ep45_cover.png', 'ep46_cover.png'):
        im = Image.open(os.path.join(OUT, n)).convert('RGB')
        full = im.resize((360, 640)); grid = im.crop((0, 240, 1080, 1680)).resize((360, 480))
        ims += [full, grid]
    sh = Image.new('RGB', (360 * 4 + 30, 640), 'white')
    x = 0
    for i, im in enumerate(ims):
        sh.paste(im, (x, 0)); x += 360 + (10 if i % 2 == 0 else 20)
    sh.save(os.path.join(OUT, 'preview.png'))


if __name__ == '__main__':
    ep45(); ep46(); preview()
