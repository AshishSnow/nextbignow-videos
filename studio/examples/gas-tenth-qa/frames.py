import sys, os, skia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa import *
from neon import person
def F(name, fn):
    s = skia.Surface(W, H); c = s.getCanvas(); fn(c); c.drawRect(skia.Rect.MakeXYWH(14, 14, W - 28, H - 28), S((255, 255, 255), 28)); c.drawRect(skia.Rect.MakeXYWH(28, 28, W - 56, H - 56), S(INK, 8))
    s.makeImageSnapshot().save('lab_%s.png' % name, skia.kPNG)
t = 1.0
def f1(c):
    sunburst(c, 'red', t); logo(c); headline(c, 'WHY IS GAS ALWAYS', '$2.99 AND 9/10?')
    polaroid(c, 540, 940, 640, 600, -3, 1, lambda cc, w, h: pic_station(cc, w, h, t))
    burst(c, 830, 700, 120, '9/10\n¢?', 1, rot=10)
    subpill(c, [('Why', 0, 0.3), ('is', 0.3, 0.5), ('gas', 0.5, 1.2)], 0.8)
def f2(c):
    sunburst(c, 'purple', t); logo(c); headline(c, 'HOW DID', 'IT START?')
    polaroid(c, 540, 930, 560, 620, 3, 1, lambda cc, w, h: pic_old(cc, w, h, t))
    label(c, 'GAS TAX CAME IN FRACTIONS', 540, 1320, 1)
    subpill(c, [('in', 0, 0.3), ('the', 0.3, 0.5), ('thirties', 0.5, 1.2)], 0.8)
def f3(c):
    sunburst(c, 'orange', t); logo(c); headline(c, 'BUT...', None, y=440, s1=110)
    polaroid(c, 540, 930, 640, 520, -2, 1, lambda cc, w, h: pic_profit(cc, w, h, t, 1))
    burst(c, 820, 1250, 150, 'UP TO\n10% OF\nPROFIT', 1, col=(255, 255, 255), rot=8)
    subpill(c, [('ten', 0, 0.3), ('percent', 0.3, 1.2)], 0.8)
def f4(c):
    sunburst(c, 'green', t); logo(c); headline(c, 'STRAIGHT', 'ANSWER')
    burst(c, 540, 820, 230, 'A 1930s\nPRICE\nTRICK', 1, rot=-6)
    person(c, 540, 1560, 0.5, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.5), t=t, arm_r=(80, -200), arm_l=(-30, 230))
    label(c, 'THAT NEVER WENT AWAY', 540, 1100, 1, rot=2, bg=(255, 214, 40))
    subpill(c, [('never', 0, 0.3), ('left.', 0.3, 1.2)], 0.8)
for n, fn in (('q', f1), ('why', f2), ('but', f3), ('ans', f4)): F(n, fn)
from PIL import Image
ims = [Image.open('lab_%s.png' % n).convert('RGB').resize((540, 960)) for n in ('q', 'why', 'but', 'ans')]
s = Image.new('RGB', (540 * 4, 960)); [s.paste(im, (i * 540, 0)) for i, im in enumerate(ims)]; s.save('style_frames_gas.jpg', quality=90)
