"""Style test: vintage comic + modern editorial, on the GPS episode. Renders 4 sample frames."""
import os, math
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, pr, cl
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import place, img, cover
from comickit import *

PK.IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gps', 'img')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comic_test'); os.makedirs(OUT, exist_ok=True)
LX = 90


def frame1(c):  # hook / cover
    paper(c)
    caption(c, 'APRIL 2024 . ESTONIA', LX, 300, col=CYEL, size=30)
    title(c, 'JAMMED!', 520, 640, 196, CRED, align='c', rot=-3)
    text(c, "2 jets couldn't land.", 540, 760, 'blk', 66, KINK, 'c')
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 620), paint((22, 40, 92)))
        dots(cc, (0, 0, 900, 620), (40, 70, 150), cell=22, rmax=8, grad=(0.0, 1.0))
        for i in range(4):
            r = 120 + i * 110
            p = skia.Path(); p.addArc(R.MakeXYWH(700 - r, 60 - r, 2 * r, 2 * r), 100, 60)
            cc.drawPath(p, stroke(CRED if i > 1 else CCYN, 10, 0.9))
        cc.drawCircle(720, 470, 20, paint(CYEL)); cc.drawCircle(720, 470, 20, stroke(KINK, 5))
        cc.drawString('TARTU', 750, 482, font('LuckiestGuy.ttf', 40), paint(PAPER))
    panel(c, 90, 860, 900, 620, rot=1.5, draw=dr)
    place(c, 'G1_sat_cut_comic.png', 820, 900, 300, rot=-10, shadow=False)
    place(c, 'G6_plane_cut_comic.png', 420, 1260, 640, rot=-10, shadow=False)
    burst(c, 250, 1020, 115, 'ZZZT!', col=CYEL, txt=CRED, size=50, rot=-8)


def frame2(c):  # big question
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 300, col=PAPER, size=30)
    title(c, 'WHAT IF', 90, 560, 150, CYEL)
    title(c, 'GPS GOES', 90, 720, 150, PAPER)
    title(c, 'DOWN?', 90, 880, 190, CYEL)
    place(c, 'G1_sat_cut_comic.png', 560, 1230, 780, rot=-8, shadow=False)


def frame3(c):  # case study panel with speech bubble
    paper(c)
    caption(c, 'MEANWHILE, IN TARTU...', LX, 300, col=CYEL, size=32)
    title(c, 'NO GPS.', 90, 520, 140, CBLU)
    title(c, 'NO LANDING.', 90, 670, 140, CRED)
    def dr(cc):
        cover(cc, img('G3_tartu_comic.png'), 0, 0, 900, 640, 1.0, 0.65, 0.5)
    panel(c, 90, 760, 900, 640, rot=-1.5, draw=dr)
    bubble(c, 700, 860, 380, 170, 'NO SIGNAL!', (610, 1010), size=48)
    mono(c, 'PHOTO: IVO KRUUSAMAGI . CC BY-SA 4.0', 540, 1470, 18, GREY, 'c')


def frame4(c):  # data panel
    paper(c)
    caption(c, 'UK GOVERNMENT STUDY', LX, 300, col=CCYN, size=30)
    text(c, 'One week without GPS', 90, 480, 'blk', 72, KINK)
    title(c, '£7.6 BILLION', 90, 640, 140, CRED, rot=-2)
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 600), paint(PAPER))
        bars(cc, 70, 120, 760, 340, [('EMERGENCY', 3.5, '£3.5BN', CRED), ('ROAD', 1.7, '£1.7BN', CYEL), ('SHIPS', 1.5, '£1.5BN', CBLU)], 1.0, 3.9)
    panel(c, 90, 760, 900, 600, rot=1.2, draw=dr)
    burst(c, 860, 760, 130, 'OUCH!', col=CYEL, txt=CRED, size=56, rot=-10)


for i, fn in enumerate((frame1, frame2, frame3, frame4)):
    s = skia.Surface(W, H); fn(s.getCanvas()); s.makeImageSnapshot().save(os.path.join(OUT, 'f%d.png' % (i + 1)), skia.kPNG)
from PIL import Image
ims = [Image.open(os.path.join(OUT, 'f%d.png' % (i + 1))).convert('RGB').resize((540, 960)) for i in range(4)]
sh = Image.new('RGB', (540 * 4 + 60, 960), 'white')
for i, im in enumerate(ims): sh.paste(im, (i * 560, 0))
sh.save(os.path.join(OUT, 'comic_style_test.png'))
print('ok')
