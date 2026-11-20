"""OMB gas 9/10 cent Short in the FreshNestHub Q&A-burst look (qa.py). One pass writes IG + YT cuts.
usage: python3 render_gas.py still t1 t2 ... | nframes | range f0 f1"""
import sys, os, math, re, json, random, subprocess
import numpy as np
import skia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa import *
from neon import person, coin, car

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'comic', 'cd')
FPS = 30
AL = [x for x in json.load(open(os.path.join(D, 'align.json')))]
TOK = [(w.lower().strip("'"), a, b) for w, a, b in AL]


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z0-9']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))): return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = TOK[-1][2] + 0.4
DUR = END + 0.9


def cl(x): return max(0.0, min(1.0, x))
def pr(t, t0, d): return cl((t - t0) / d)
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 3 * x * x - 2 * x * x * x
def blinking(t, seed=0): return ((t + seed * 1.7) % 3.3) < 0.12


def comment_bubble(c, x, y, k):
    if k <= 0: return
    s = min(1, k * 1.5); c.save(); c.translate(x, y); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-180, -90, 360, 160), 40, 40); c.drawRRect(r.makeOffset(8, 10) if hasattr(r, 'makeOffset') else r, P(INK, 0.4)); inked(c, r, P((255, 255, 255)), 6)
    c.drawPath(path([(-90, 68), (-120, 140), (-30, 68)]), P((255, 255, 255))); c.drawPath(path([(-90, 70), (-120, 140), (-30, 70)], close=False), S(INK, 6))
    for i in range(3): c.drawCircle(-70 + i * 70, -10, 18, P((235, 50, 60)))
    c.restore()


def price_card(c, w, h, txt, frac, good):
    c.drawRect(skia.Rect.MakeWH(w, h), P((30, 32, 44)))
    f = font('Anton.ttf', h * 0.5); tw = f.measureText(txt); x0 = w / 2 - tw / 2 - (w * 0.06 if frac else 0)
    c.drawString(txt, x0, h * 0.68, f, P((255, 214, 40)))
    if frac:
        f3 = font('Anton.ttf', h * 0.2); c.drawString('9', x0 + tw + 8, h * 0.38, f3, P((255, 214, 40))); c.drawLine(x0 + tw + 6, h * 0.43, x0 + tw + 44, h * 0.43, S((255, 214, 40), 4))
        c.drawString('10', x0 + tw + 2, h * 0.64, f3, P((255, 214, 40)))


def check(c, x, y, k, good=True):
    if k <= 0: return
    s = min(1, k * 1.6); c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 62, P(INK)); c.drawCircle(0, 0, 54, P((60, 200, 110) if good else (235, 60, 60)))
    if good: c.drawPath(path([(-26, 2), (-6, 24), (30, -20)], close=False), S((255, 255, 255), 14))
    else: c.drawLine(-22, -22, 22, 22, S((255, 255, 255), 14)); c.drawLine(22, -22, -22, 22, S((255, 255, 255), 14))
    c.restore()


# ------------------------------------------------------------------ scenes
def s_q(c, t):
    th2 = ph('short answer')
    sunburst(c, 'red', t); logo(c); headline(c, 'WHY IS GAS ALWAYS', '$2.99 AND 9/10?')
    polaroid(c, 540, 940, 640, 600, -3 + 1.5 * math.sin(t * 1.2), 1, lambda cc, w, h: pic_station(cc, w, h, t))
    if t < th2 - 0.1: burst(c, 830, 700, 120, '9/10\n¢?', 1, rot=10 + 4 * math.sin(t * 3))
    else:
        burst(c, 820, 690, 140, 'LOOKS\nCHEAPER', pr(t, th2 + 0.3, 0.3), rot=8)
        label(c, 'AND IT PAYS THE STATION', 540, 1330, pr(t, ph('pays the station') - 0.2, 0.3), bg=(255, 214, 40))


def s_why(c, t):
    t0 = ph('it started back')
    sunburst(c, 'purple', t); logo(c); headline(c, 'HOW DID', 'IT START?', pr(t, t0 - 0.15, 0.3))
    polaroid(c, 540, 930, 560, 620, 3 - 1.5 * math.sin(t * 1.1), pr(t, t0, 0.35), lambda cc, w, h: pic_old(cc, w, h, t))
    label(c, 'GAS TAX CAME IN FRACTIONS', 540, 1320, pr(t, ph('gas taxes') - 0.2, 0.3))
    burst(c, 840, 640, 110, '1930s', pr(t, ph('nineteen thirties') - 0.1, 0.3), rot=12)


def s_digits(c, t):
    t0 = ph('then stations'); tf = ph('first digits'); t3 = ph('two ninety nine')
    sunburst(c, 'blue', t); logo(c)
    if t < t3 - 0.2:
        headline(c, 'DRIVERS READ', 'THE FIRST DIGITS', pr(t, t0 - 0.15, 0.3))
        def pic(cc, w, h):
            pic_station(cc, w, h, t)
            k = pr(t, tf - 0.3, 0.5)
            if k > 0:
                cc.drawRect(skia.Rect.MakeXYWH(w * 0.2, h * 0.17, w * 0.24, h * 0.22), S((255, 60, 60), 8, k))
        polaroid(c, 540, 940, 640, 600, -2, pr(t, t0, 0.35), pic)
    else:
        headline(c, 'WHICH LOOKS', 'CHEAPER?', 1)
        polaroid(c, 540, 760, 560, 230, -3, pr(t, t3 - 0.2, 0.3), lambda cc, w, h: price_card(cc, w, h, '$2.99', True, True))
        polaroid(c, 540, 1130, 560, 230, 3, pr(t, t3 + 0.6, 0.3), lambda cc, w, h: price_card(cc, w, h, '$3.00', False, False))
        check(c, 850, 700, pr(t, ph('way cheaper') - 0.1, 0.3), True); check(c, 860, 1080, pr(t, ph('three dollars') - 0.1, 0.3), False)


def s_but(c, t):
    t0 = ph('but that tiny'); tb = ph('ten to fifteen'); t10 = ph('ten percent')
    sunburst(c, 'orange', t); logo(c); headline(c, 'BUT...', None, pr(t, t0 - 0.15, 0.3), y=440, s1=110)
    if t < tb - 0.4:
        kt = pr(t, ph("isn't tiny") - 0.2, 0.6)
        burst(c, 540, 900, 70 + 150 * eo(kt), '9/10¢', 1.0, rot=-6 + 4 * math.sin(t * 3), size=(70 + 150 * eo(kt)) * 0.42)
        label(c, "THAT FRACTION ISN'T TINY", 540, 1330, pr(t, ph("isn't tiny") - 0.2, 0.3))
    polaroid(c, 540, 930, 640, 520, -2, pr(t, tb - 0.5, 0.35), lambda cc, w, h: pic_profit(cc, w, h, t, pr(t, tb - 0.2, 0.8)))
    burst(c, 820, 1250, 150, 'UP TO\n10% OF\nPROFIT', pr(t, t10 - 0.2, 0.3), col=(255, 255, 255), rot=8)
    if t > tb - 0.4: label(c, 'NACS, CONVENIENCE STORE INDUSTRY', 470, 1225, pr(t, tb, 0.3), size=24, rot=-2)


def s_proof(c, t):
    t0 = ph('one station owner'); td = ph('dropped it'); t23 = ph('twenty three dollars')
    sunburst(c, 'teal', t); logo(c); headline(c, 'ONE OWNER', 'TRIED IT', pr(t, t0 - 0.15, 0.3))
    polaroid(c, 540, 930, 640, 600, 2, pr(t, t0, 0.35), lambda cc, w, h: pic_station(cc, w, h, t, price_frac=t < td + 0.3))
    label(c, "JIM'S TEXACO, 2006", 540, 1330, pr(t, ph('two thousand six') - 0.2, 0.3))
    burst(c, 820, 700, 140, '-$23\nA DAY', pr(t, t23 - 0.2, 0.3), col=(235, 60, 60), tc=(255, 255, 255), rot=-8)


def s_ans(c, t):
    t0 = ph('so that fraction'); tq = ph('did you ever')
    sunburst(c, 'green', t); logo(c); headline(c, 'STRAIGHT', 'ANSWER', pr(t, t0 - 0.15, 0.3))
    if t < tq - 0.2:
        burst(c, 540, 820, 230, 'A 1930s\nPRICE\nTRICK', pr(t, ph('price trick') - 0.3, 0.3), rot=-6 + 3 * math.sin(t * 2))
        label(c, 'THAT NEVER WENT AWAY', 540, 1100, pr(t, ph('never left') - 0.2, 0.3), rot=2, bg=(255, 214, 40))
    else:
        label(c, 'DID YOU EVER NOTICE IT?', 540, 760, pr(t, tq - 0.1, 0.3), size=44, bg=(255, 214, 40))
        comment_bubble(c, 560, 1000, pr(t, ph('comments') - 0.3, 0.3))
    person(c, 540, 1560 + 10 * math.sin(t * 2), 0.5, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.5), t=t, arm_r=(80, -200 + 20 * math.sin(t * 6)), arm_l=(-30, 230), blink=blinking(t))


SCENES = [(0.0, s_q), (ph('it started back') - 0.12, s_why), (ph('then stations') - 0.12, s_digits), (ph('but that tiny') - 0.12, s_but),
          (ph('one station owner') - 0.12, s_proof), (ph('so that fraction') - 0.12, s_ans)]
SHAKES = [(ph('way cheaper'), 8, 0.3), (ph('ten percent'), 16, 0.4), (ph('twenty three dollars'), 10, 0.35), (ph('price trick'), 10, 0.3)]
TR = 0.22


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas()
    sx = sy = 0.0
    for (ts, a, d) in SHAKES:
        if ts <= t < ts + d:
            k = 1 - (t - ts) / d; sx += a * k * math.sin(t * 90); sy += a * k * math.cos(t * 77)
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0)
    t0 = SCENES[i][0]; t1 = SCENES[i + 1][0] if i + 1 < len(SCENES) else DUR
    u = cl((t - t0) / max(0.1, t1 - t0)); z = 1.0 + 0.04 * u
    kin = pr(t, t0, TR) if i > 0 else 1.0; z *= 1.0 + 0.08 * (1 - eo(kin))
    c.save(); c.translate(540 + sx, 960 + sy); c.scale(z, z); c.translate(-540, -960); SCENES[i][1](c, t); c.restore()
    if i > 0 and kin < 1: c.drawRect(skia.Rect.MakeWH(W, H), P((255, 255, 255), 0.7 * (1 - kin)))
    if t > END: c.drawRect(skia.Rect.MakeWH(W, H), P((255, 255, 255), eio(pr(t, END, 0.5))))
    return s


SUBW = []
_k = 0
for wd in open(os.path.join(D, 'script.txt')).read().split():
    n = len(re.findall(r"[A-Za-z0-9'%]+", wd))
    if n == 0: continue
    seg = AL[_k:_k + n]; _k += n
    if seg: SUBW.append((wd, seg[0][1], seg[-1][2]))
CH = []; cur = []
for w in SUBW:
    cur.append(w)
    if len(cur) >= 3 or w[0][-1] in '.,?!': CH.append(cur); cur = []
if cur: CH.append(cur)


def subs(c, t, y):
    for ch in CH:
        if ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.15: subpill(c, ch, t, y); return


def both(t):
    base = frame(t).makeImageSnapshot()
    ig = skia.Surface(W, H); c = ig.getCanvas(); c.drawImage(base, 0, 0)
    if 0.1 < t < END: subs(c, t, 1442)
    yt = skia.Surface(W, H); c = yt.getCanvas()
    bp = skia.Paint(); bp.setImageFilter(skia.ImageFilters.Blur(40, 40)); c.drawImage(base, 0, 0, skia.SamplingOptions(), bp)
    c.save(); c.translate(450 - 450 * 0.85, 250 - 250 * 0.85); c.scale(0.85, 0.85); c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 0.5, 30)); c.drawImage(base, 0, 0); c.restore()
    if 0.1 < t < END: subs(c, t, 1320)
    return ig.makeImageSnapshot(), yt.makeImageSnapshot()


def to_np(img): return img.toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]


if __name__ == '__main__':
    out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
    if sys.argv[1] == 'still':
        for v in sys.argv[2:]:
            ig, yt = both(float(v)); ig.save(os.path.join(out, 'ig_%06.2f.png' % float(v)), skia.kPNG); yt.save(os.path.join(out, 'yt_%06.2f.png' % float(v)), skia.kPNG)
    elif sys.argv[1] == 'nframes':
        print(int(DUR * FPS))
    elif sys.argv[1] == 'range':
        f0, f1 = int(sys.argv[2]), int(sys.argv[3])
        enc = lambda name: subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                                             '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', os.path.join(out, name)], stdin=subprocess.PIPE)
        pi, py = enc('ig_%05d.mp4' % f0), enc('yt_%05d.mp4' % f0)
        for fi in range(f0, f1):
            ig, yt = both(fi / FPS)
            pi.stdin.write(np.ascontiguousarray(to_np(ig)).tobytes()); py.stdin.write(np.ascontiguousarray(to_np(yt)).tobytes())
        pi.stdin.close(); py.stdin.close(); pi.wait(); py.wait()
