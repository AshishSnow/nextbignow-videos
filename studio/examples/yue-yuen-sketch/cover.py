"""Cover v3 (22 Nov): built for the IG profile grid (3:4 center crop = y 240..1680) and the YT first frame.
Cream paper, giant 2-line serif headline (ink + deep-red italic), big gold sunburst disc behind ONE hero prop, giant shocked mascot face, red hand-drawn underline.
usage: python3 cover.py <project_dir> <render_module> <line1> <line2> <prop_code> <out.png>
prop_code: python using R (render module) and c (canvas) to draw the hero prop roughly centered at (430, 1150)."""
import sys, os, math, importlib, numpy as np, skia
P, MOD, L1, L2, PROP, OUT = sys.argv[1:7]
os.chdir(P); sys.path.insert(0, P)
R = importlib.import_module(MOD)
W, H = 1080, 1920
s = skia.Surface(W, H); c = s.getCanvas()
c.drawRect(skia.Rect.MakeWH(W, H), R.P((252, 250, 244)))
# sunburst disc
cx, cy = 470, 1170
for i in range(24):
    a = i * math.pi / 12
    c.drawPath(R.path([(cx, cy), (cx + 900 * math.cos(a - 0.06), cy + 900 * math.sin(a - 0.06)), (cx + 900 * math.cos(a + 0.06), cy + 900 * math.sin(a + 0.06))]), R.P((236, 226, 200)))
c.drawCircle(cx, cy, 360, R.P((240, 200, 90))); c.drawCircle(cx, cy, 360, R.S((34, 32, 30), 8))
exec(PROP)
R.head(c, 900, 1560, 110, (255, 140, 40), 'shock', (-0.6, -0.4), 3, 0.35)   # small mascot (owner 23 Nov: keep the character small, explainer centred)
raw = s.makeImageSnapshot(); arr = raw.toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]
sk = R._ink(np.ascontiguousarray(arr))
img = skia.Image.fromarray(np.ascontiguousarray(np.dstack([sk, np.full(sk.shape[:2], 255, np.uint8)])), colorType=skia.kRGBA_8888_ColorType)
s2 = skia.Surface(W, H); c = s2.getCanvas(); c.drawImage(img, 0, 0)
# gold tag
c.save(); c.translate(540, 300); c.rotate(-2); c.drawRect(skia.Rect.MakeXYWH(-230, -40, 460, 74), R.P((212, 160, 46)))
f = R.serif(40, 500, True); t = 'oops, my business'; c.drawString(t, -f.measureText(t) / 2, 14, f, R.P((34, 32, 30))); c.restore()
def fit(txt, size, w, it):
    f = R.serif(size, 700 if not it else 600, it)
    while f.measureText(txt) > w: f = R.serif(f.getSize() * 0.96, 700 if not it else 600, it)
    return f
f1 = fit(L1, 150, 980, False); f2 = fit(L2, 160, 1000, True)
for txt, f, y, col in ((L1, f1, 500, (34, 32, 30)), (L2, f2, 670, (150, 22, 34))):
    tw = f.measureText(txt); x = 540 - tw / 2
    c.drawString(txt, x + 5, y + 6, f, R.P((212, 160, 46), 0.9))     # gold offset shadow
    c.drawString(txt, x, y, f, R.P(col))
# hand-drawn red underline under line 2
tw = f2.measureText(L2); p = skia.Path(); p.moveTo(540 - tw / 2, 705); p.cubicTo(540 - tw / 4, 690, 540 + tw / 4, 722, 540 + tw / 2, 700)
c.drawPath(p, R.S((150, 22, 34), 10))
s2.makeImageSnapshot().save(OUT, skia.kPNG); print('cover ok', OUT)
