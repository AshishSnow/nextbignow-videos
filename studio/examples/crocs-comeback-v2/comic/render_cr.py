"""OopsMyBusiness Short v2 format — Crocs comeback ($1 stock in 2008 -> $3.3B brand). CREAM comic paper + black/yellow accents, real cut-outs in
every scene, always moving (owner 17 Nov). Facts: ../SOURCES.md. Photos: cr/img/credits.json. No logos/trade dress; no likenesses."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, 'cr')
PK.IMG = os.path.join(D, 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))
YEL = (255, 214, 0); CHAR = (26, 26, 30); CHAR_D = (48, 48, 56); CREAM = (252, 241, 210)


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z0-9']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 1.6
LX = 90


PLAT = os.environ.get('OMB_PLAT', 'ig')   # 'ig' = Instagram Reels, 'yt' = YouTube Shorts
# YouTube Shorts covers more of the frame (owner's screenshot 15 Nov: channel row/title/Promote pill start ~y1380-1530 of 1920,
# right action column from ~y950 at x>900, phones crop ~60 px per side). So the YT cut scales the whole layout into the safe box.
if PLAT == 'yt':
    LAY = skia.Matrix(); LAY.setScaleTranslate(0.85, 0.85, 450 - 450 * 0.85, 250 - 250 * 0.85); SUB_Y = 1320
else:
    LAY = skia.Matrix(); SUB_Y = 1442
LAY_INV = skia.Matrix(); LAY.invert(LAY_INV)


def full(c, fn):
    """draw a background in frame space, cancelling the platform layout scale."""
    c.save(); c.concat(LAY_INV); fn(); c.restore()


def credit(c, key, a=1.0, y=1400):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s . WIKIMEDIA COMMONS' % (cr['author'], cr['license'])).upper()[:78]
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, (150, 150, 150), a=a * 0.9); c.restore()


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0, after=None):
    def dr(cc):
        cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.012 * t, fx, fy)
        if after: after(cc)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def mini(c, x, y, w, h, rot, k, head, big, col, txtc=KINK, bigsize=54, headc=KINK):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(col)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=3.2, grad=(0.3, 1.0), a=0.18)
        cc.drawString(head, 22, 44, font('SpecialElite.ttf', 26), paint(headc))
        title(cc, big, 22, h - 36, bigsize, txtc, 1.0, shadow=4)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)


def tv(c, x, y, w, h, k, t, key=None, rot=-2, screen=None):
    """boxy vintage TV (drawn) with a photo or drawing on its screen."""
    if k <= 0: return
    sc = eback(cl(k), 2.0)
    c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(rot); c.scale(sc, sc); c.translate(-w / 2, -h / 2)
    body = skia.RRect.MakeRectXY(R.MakeXYWH(0, 0, w, h), 40, 40)
    c.save(); c.translate(16, 16); c.drawRRect(body, paint(KINK)); c.restore()
    c.drawRRect(body, paint((70, 58, 48))); dots(c, (0, 0, w, h), KINK, cell=16, rmax=3, a=0.3); c.drawRRect(body, stroke(KINK, 10))
    sw, sh = w - 220, h - 80
    scr = skia.RRect.MakeRectXY(R.MakeXYWH(40, 40, sw, sh), 50, 50)
    c.save(); c.clipRRect(scr, doAntiAlias=True)
    c.drawRect(R.MakeXYWH(40, 40, sw, sh), paint((40, 44, 40)))
    if key: cover(c, img(key + '_comic.png'), 40, 40, sw, sh, 1.08 + 0.01 * t, 0.5, 0.5)
    if screen: c.save(); c.translate(40, 40); screen(c, sw, sh); c.restore()
    for i in range(0, int(sh), 8): c.drawRect(R.MakeXYWH(40, 40 + i, sw, 3), paint((0, 0, 0), 0.12))
    c.restore(); c.drawRRect(scr, stroke(KINK, 10))
    for i, yy in enumerate((h * 0.3, h * 0.55)):
        c.drawCircle(w - 90, yy, 34, paint(YEL)); c.drawCircle(w - 90, yy, 34, stroke(KINK, 7))
        c.drawLine(w - 90, yy, w - 90 + 24 * math.cos(t * 2 + i), yy + 24 * math.sin(t * 2 + i), stroke(KINK, 6))
    for i in range(5): c.drawLine(w - 130, h * 0.72 + i * 16, w - 50, h * 0.72 + i * 16, stroke(KINK, 5))
    c.drawLine(w * 0.25, h, w * 0.18, h + 60, stroke(KINK, 12)); c.drawLine(w * 0.75, h, w * 0.82, h + 60, stroke(KINK, 12))
    c.drawLine(w * 0.35, 0, w * 0.22, -90, stroke(KINK, 7)); c.drawLine(w * 0.45, 0, w * 0.58, -100, stroke(KINK, 7))
    c.restore()


def quote(c, x, y, w, h, rot, k, lines, who):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(CREAM))
        title(cc, '“', 18, 110, 120, YEL, 1.0, shadow=4)
        for i, s in enumerate(lines): cc.drawString(s, 70, 80 + i * 56, font('SpecialElite.ttf', 40), paint(KINK))
        cc.drawString(who, 70, h - 30, font('SpecialElite.ttf', 24), paint((110, 100, 90)))
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def bgp(c, t=0.0):
    full(c, lambda: paper(c, t))


def floaty(t, sp=1.0, amp=10):
    return amp * math.sin(t * 1.6 * sp), 2.0 * math.sin(t * 1.1 * sp + 1)


def stick(c, key, cx, cy, w, k, t, rot=0.0, sp=1.0, amp=10, shadow=True):
    """sticker cut-out that pops in (k) and keeps floating."""
    if k <= 0: return
    dy, dr = floaty(t, sp, amp)
    s = eback(cl(k), 2.2)
    place(c, key + '_cut.png', cx, cy + dy + 60 * (1 - eo(cl(k))), w * s, rot + dr, a=cl(k * 1.6), shadow=shadow)


def tag(c, x, y, s, k, t, rot=-8, col=YEL, txt=KINK, size=110, sub=None, swing=True):
    """swinging yellow price tag with a string."""
    if k <= 0: return
    f = font('LuckiestGuy.ttf', size); w = f.measureText(s) + 110; h = size * 1.5
    sc = eback(cl(k), 2.2)
    c.save(); c.translate(x, y); c.rotate(rot + (4 * math.sin(t * 2.2) if swing else 0)); c.scale(sc, sc)
    p = poly([(0, 0), (60, -h / 2), (w, -h / 2), (w, h / 2), (60, h / 2)])
    c.save(); c.translate(12, 12); c.drawPath(p, paint(KINK)); c.restore()
    c.drawPath(p, paint(col)); dots(c, (0, -h / 2, w, h), KINK, cell=14, rmax=3, a=0.15); c.drawPath(p, stroke(KINK, 8))
    c.drawCircle(42, 0, 13, paint(CREAM)); c.drawCircle(42, 0, 13, stroke(KINK, 6))
    c.drawString(s, 80, size * 0.36, f, paint(txt))
    if sub: c.drawString(sub, 82, h / 2 - 14, font('SpecialElite.ttf', 26), paint(KINK))
    c.restore()


def two(c, a1, a2, y, k1, k2, s1=118, s2=128, rot=-2):
    title(c, a1, 540, y, s1, CHAR, k1, 'c', outline=0.01, shadow=0, rot=rot)
    title(c, a2, 540, y + s2 * 1.1, s2, YEL, k2, 'c', rot=rot)


# ------------------------------------------------------------------ scenes
def stamp(c, s, x, y, k, rot=-12, size=74, col=None):
    if k <= 0: return
    col = col or CHAR
    c.save(); c.translate(x, y); c.rotate(rot); sc = 1.6 - 0.6 * eback(cl(k), 2.0); c.scale(sc, sc)
    f = font('LuckiestGuy.ttf', size); tw = f.measureText(s)
    c.drawRect(R.MakeXYWH(-tw / 2 - 22, -size * 0.95, tw + 44, size * 1.35), stroke(col, 10)); c.drawString(s, -tw / 2, size * 0.18, f, paint(col)); c.restore()


def line_chart(cc, w, h, pts, k, col=YEL, lab=None):
    cc.drawRect(R.MakeWH(w, h), paint(CREAM))
    x0, y0, cw, ch = 60, 40, w - 120, h - 110
    cc.drawLine(x0, y0 + ch, x0 + cw, y0 + ch, stroke(KINK, 5)); cc.drawLine(x0, y0, x0, y0 + ch, stroke(KINK, 5))
    p = skia.Path(); first = True
    for fx, v in pts:
        if fx > k: break
        (p.moveTo if first else p.lineTo)(x0 + fx * cw, y0 + ch - v * ch); first = False
    cc.drawPath(p, stroke(KINK, 18)); cc.drawPath(p, stroke(col, 10))
    if lab: cc.drawString(lab, 60, h - 26, font('SpecialElite.ttf', 24), paint(GREY))


def charm(c, x, y, r, k, col, t, i=0):
    """little Jibbitz-style charm: coloured disc with a simple icon."""
    if k <= 0: return
    s = eback(cl(k), 2.2); dy = 6 * math.sin(t * 3 + i)
    c.save(); c.translate(x, y + dy); c.scale(s, s)
    c.drawCircle(6, 6, r, paint(KINK)); c.drawCircle(0, 0, r, paint(col)); c.drawCircle(0, 0, r, stroke(KINK, 6))
    ic = i % 3
    if ic == 0:
        p = skia.Path(); [p.lineTo(*(r * 0.55 * math.cos(math.radians(-90 + j * 36)) * (1 if j % 2 == 0 else 0.45), r * 0.55 * math.sin(math.radians(-90 + j * 36)) * (1 if j % 2 == 0 else 0.45))) if j else p.moveTo(0, -r * 0.55) for j in range(10)]; p.close(); c.drawPath(p, paint(CREAM))
    elif ic == 1:
        c.drawCircle(-r * .2, -r * .1, r * .28, paint(CREAM)); c.drawCircle(r * .2, -r * .1, r * .28, paint(CREAM))
        c.drawPath(poly([(-r * .45, 0), (r * .45, 0), (0, r * .5)]), paint(CREAM))
    else:
        c.drawCircle(0, 0, r * .45, paint(CREAM)); c.drawCircle(-r * .15, -r * .1, r * .07, paint(KINK)); c.drawCircle(r * .15, -r * .1, r * .07, paint(KINK))
        a = skia.Path(); a.addArc(R.MakeXYWH(-r * .25, -r * .1, r * .5, r * .35), 20, 140); c.drawPath(a, stroke(KINK, 5))
    c.restore()


CHC = [(230, 60, 60), (40, 150, 230), (60, 180, 90), (240, 150, 30), (160, 80, 200)]


def sc_hook(c, t, S):
    ta = ph('short answer'); tw = ph('whole business')
    bgp(c, t)
    caption(c, 'TRUE STORY', LX, 300, 1.0, col=YEL, size=36)
    two(c, 'HOW THE UGLIEST SHOE', 'CAME BACK FROM $1', 470, 1.0, 1.0, 84, 110)
    c.drawCircle(540, 960, 320 + 8 * math.sin(t * 2), paint(YEL))
    dots(c, (220, 640, 640, 640), (230, 180, 0), cell=18, rmax=5, a=0.5)
    stick(c, 'clog', 540, 960, 660, 1.0, t, rot=-8)
    tag(c, 620, 1220, '$1', 1.0, t, rot=-10, size=96)
    if t > ta - 0.2:
        stamp(c, 'ALL IN ON THE CLOG', 540, 1350, pr(t, tw - 0.6, 0.35), rot=-6, size=64)
    credit(c, 'clog')


def sc_crash(c, t, S):
    t0 = S['t0']; ts = ph('seventy dollars'); tl = ph('about one dollar'); tm = ph('eighty-five million')
    bgp(c, t)
    caption(c, 'CROCS STOCK', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    def dr(cc):
        line_chart(cc, 860, 620, [(0, .3), (.3, .75), (.45, .95), (.7, .35), (1, .03)], pr(t, t0 + 0.2, (tl - t0) + 0.2), (205, 40, 40), 'CROCS SHARE PRICE 2006-2008 (ILLUSTRATIVE LINE)')
    panel(c, 110, 400, 860, 620, rot=-1.2, k=pr(t, t0, 0.4), draw=dr)
    if t > ts - 0.3: tag(c, 420, 520, '$70', pr(t, ts - 0.3, 0.35), t, rot=-6, size=80, sub='2007')
    if t > tl - 0.3: tag(c, 640, 960, '$1', pr(t, tl - 0.3, 0.35), t, rot=8, size=96, sub='2008')
    if t > tm - 0.3: burst(c, 330, 1220, 170, '-$185M', pr(t, tm - 0.3, 0.35), size=60, col=KINK, txt=YEL, rot=-8)
    if t > tm + 0.2: caption(c, 'LOST IN 2008', 560, 1300, pr(t, tm + 0.2, 0.3), col=CREAM, size=30, rot=2)


def sc_tried(c, t, S):
    t0 = S['t0']; td = ph('dress shoes'); tg = ph('golf shoes'); th = ph('high heels'); tj = ph('become a joke')
    bgp(c, t)
    caption(c, 'IT TRIED EVERYTHING', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    if t > td - 0.3: tag(c, 140, 520, 'DRESS SHOES', pr(t, td - 0.3, 0.35), t, rot=-6, col=CREAM, size=64)
    if t > tg - 0.3: tag(c, 560, 640, 'GOLF SHOES', pr(t, tg - 0.3, 0.35), t, rot=6, col=CREAM, size=64)
    if t > th - 0.3: stick(c, 'heels', 330, 820, 380, pr(t, th - 0.3, 0.4), t, rot=-10)
    stick(c, 'clog', 640, 1080, 440, pr(t, t0 + 0.2, 0.4), t, rot=6)
    if t > tj - 0.3:
        stamp(c, 'A JOKE', 640, 1100, pr(t, tj - 0.2, 0.35), rot=-14, size=110, col=(205, 40, 40))
    if t > th: credit(c, 'heels')


def sc_cut(c, t, S):
    t0 = S['t0']; ta = ph('all in'); td = ph('decorate it'); tj = ph('called jibbitz'); tc = ph('seventy-one million')
    bgp(c, t)
    caption(c, 'SO CROCS CUT THE EXTRAS', LX, 300, pr(t, t0, 0.3), col=YEL, size=34)
    fall = pr(t, t0 + 0.2, 1.1)
    tag(c, 560, 640 + 1700 * eio(fall), 'GOLF SHOES', 1.0, t, rot=6 + 40 * fall, col=CREAM, size=60, swing=False)
    tag(c, 120, 560 + 1700 * eio(pr(t, t0 + 0.35, 1.1)), 'DRESS SHOES', 1.0, t, rot=-6 - 40 * pr(t, t0 + 0.35, 1.1), col=CREAM, size=60, swing=False)
    stick(c, 'heels', 330, 760 + 1700 * eio(pr(t, t0 + 0.5, 1.1)), 340, 1.0, t, rot=-10 - 50 * pr(t, t0 + 0.5, 1.1))
    kc = pr(t, ta - 0.3, 0.5)
    c.drawCircle(540, 900, (300 + 8 * math.sin(t * 2)) * eo(kc), paint(YEL))
    stick(c, 'clog', 540, 900, 380 + 260 * eo(kc), max(kc, 0.01), t, rot=-6)
    if t > ta: two(c, 'ALL IN', 'ON THE CLOG', 470, pr(t, ta, 0.35), pr(t, ta + 0.2, 0.35), 100, 110)
    pos = [(250, 700), (840, 720), (220, 1080), (860, 1100), (540, 1240)]
    for i, (x, y) in enumerate(pos):
        if t > td - 0.2 + i * 0.25: charm(c, x, y, 62, pr(t, td - 0.2 + i * 0.25, 0.35), CHC[i], t, i)
    if t > tj - 0.2: caption(c, 'CHARMS: "JIBBITZ"', 150, 1330, pr(t, tj - 0.2, 0.3), col=CREAM, size=30, rot=-2)
    if t > tc - 0.4: burst(c, 820, 1300, 165, '$271M', pr(t, tc - 0.4, 0.35), size=62, col=KINK, txt=YEL, rot=-8)
    credit(c, 'clog')


def sc_now(c, t, S):
    t0 = S['t0']; tb = ph('three point three')
    bgp(c, t)
    caption(c, 'LAST YEAR', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    kr = pr(t, t0 + 0.1, 2.4)
    for j in range(int(18 * kr)):
        x = 140 + (j * 223) % 820; y0 = 560 + ((j * 137) % 5) * 170
        kk = pr(t, t0 + 0.1 + j * 0.12, 0.4)
        place(c, 'clog_cut.png', x, y0 - 300 * (1 - eo(kk)), 230, rot=(j * 37) % 40 - 20, a=kk, shadow=False)
    if t > tb - 0.5:
        k = pr(t, tb - 0.5, 0.4)
        c.save(); c.translate(540, 900); c.rotate(-3); sc = eback(cl(k), 2); c.scale(sc, sc)
        c.drawRect(R.MakeXYWH(-430 + 14, -200 + 14, 860, 330), paint(KINK)); c.drawRect(R.MakeXYWH(-430, -200, 860, 330), paint(CREAM)); c.drawRect(R.MakeXYWH(-430, -200, 860, 330), stroke(KINK, 9))
        title(c, '$3.3 BILLION', 0, -40, 130, YEL, 1.0, 'c')
        title(c, 'CROCS BRAND SALES, 2025', 0, 80, 56, CHAR, 1.0, 'c', outline=0.01, shadow=0)
        c.restore()


def sc_end(c, t, S):
    t0 = S['t0']; tw = ph('would you wear')
    bgp(c, t)
    caption(c, 'THEY LEANED INTO THE JOKE', LX, 300, pr(t, t0, 0.3), col=YEL, size=34)
    two(c, 'WOULD YOU', 'WEAR THEM?', 470, pr(t, tw - 0.3, 0.35), pr(t, tw, 0.35), 110, 140)
    c.drawCircle(540, 1020, 300 + 8 * math.sin(t * 2), paint(YEL))
    stick(c, 'clog', 540, 1030, 620, pr(t, t0 + 0.2, 0.4), t, rot=8)
    for i, (x, y) in enumerate([(300, 860), (790, 900), (330, 1200), (770, 1210)]):
        charm(c, x, y, 50, pr(t, t0 + 0.4 + i * 0.15, 0.3), CHC[i], t, i)
    if t > END:
        full(c, lambda: c.drawCircle(540, 900, 1400 * eio(pr(t, END, 0.8)), paint(CHAR)))


def with_subs(fn):
    def f(c, t, S):
        c.save(); c.concat(LAY); fn(c, t, S); c.restore()
        if 0.35 < t < END + 0.2: subtitle(c, t, SUBS, y=SUB_Y)
    return f


CR = (252, 241, 210)
SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook), col=CR),
    dict(k='crash', t0=ph('in two thousand seven') - 0.2, fn=with_subs(sc_crash), tin='whip', col=CR),
    dict(k='tried', t0=ph('it had tried') - 0.2, fn=with_subs(sc_tried), tin='wipe', col=CR),
    dict(k='cut', t0=ph('so crocs cut') - 0.2, fn=with_subs(sc_cut), tin='whip', col=CR),
    dict(k='now', t0=ph('last year') - 0.2, fn=with_subs(sc_now), tin='zoom', col=CR),
    dict(k='end', t0=ph('crocs won') - 0.2, fn=with_subs(sc_end), tin='flash', col=CR),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('about one dollar'), 12, 0.35)
EP.shk(ph('eighty-five million'), 10, 0.3)
EP.shk(ph('become a joke'), 8, 0.3)
EP.shk(ph('three point three'), 12, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
