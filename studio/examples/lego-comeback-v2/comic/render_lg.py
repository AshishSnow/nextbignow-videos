"""OopsMyBusiness Short v2 format — Lego's comeback (2003-04 losses -> 2025 record). CREAM comic paper + black/yellow accents, real cut-outs in
every scene, always moving (owner 17 Nov). Facts: ../SOURCES.md. Photos: lg/img/credits.json. No logos/trade dress; no likenesses."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, 'lg')
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


def sc_hook(c, t, S):
    tl = ph('three hundred million'); tb = ph('almost went broke'); tp = ph('two and a half billion'); ts = ph('true story')
    bgp(c, t)
    caption(c, 'TRUE STORY', LX, 300, 1.0, col=YEL, size=36)
    two(c, 'LEGO ALMOST', 'WENT BROKE', 470, 1.0, 1.0, 120, 140)
    c.drawCircle(540, 960, 320 + 8 * math.sin(t * 2), paint(YEL))
    dots(c, (220, 640, 640, 640), (230, 180, 0), cell=18, rmax=5, a=0.5)
    shake = 6 * math.sin(t * 40) * pr(t, tb, 0.2) * (1 - pr(t, tb + 0.2, 0.4))
    stick(c, 'brick', 540 + shake, 960, 640, 1.0, t, rot=-6)
    if t > tl - 0.2: burst(c, 830, 720, 160, '-$300M', pr(t, tl - 0.2, 0.35), size=56, col=KINK, txt=YEL, rot=10)
    if t > tp - 0.3: burst(c, 300, 1220, 175, '+$2.5B', pr(t, tp - 0.3, 0.35), size=62, col=YEL, txt=CREAM, rot=-8)
    if t > tp + 0.3: caption(c, 'PROFIT, 2025', 560, 1300, pr(t, tp + 0.3, 0.3), col=CREAM, size=30, rot=2)
    credit(c, 'brick')


def sc_focus(c, t, S):
    t0 = S['t0']; ts = ph('stop focusing'); tp = ph('theme parks'); tv = ph('video games'); tc = ph('even clothes'); tf = ph('twenty-five percent')
    bgp(c, t)
    caption(c, 'HOW DO YOU BREAK A BRICK COMPANY?', LX, 300, pr(t, t0, 0.3), col=YEL, size=32)
    # brick shrinks into the corner as distractions take over
    kb = pr(t, ts, 0.8)
    stick(c, 'brick', lerp(540, 220, kb), lerp(760, 1180, kb), lerp(560, 230, kb), 1.0, t, rot=-6)
    if t < tp - 0.3:
        two(c, 'YOU STOP', 'FOCUSING ON IT', 470, pr(t, ts - 0.2, 0.35), pr(t, ts + 0.1, 0.35), 96, 96)
    if t > tp - 0.3: stick(c, 'coaster', 680, 720, 400, pr(t, tp - 0.3, 0.4), t, rot=4)
    if t > tp: caption(c, 'THEME PARKS', 560, 830, pr(t, tp, 0.3), col=CREAM, size=30, rot=-2)
    if t > tv - 0.3: stick(c, 'controller', 440, 980, 420, pr(t, tv - 0.3, 0.4), t, rot=-10)
    if t > tv: caption(c, 'VIDEO GAMES', 260, 1110, pr(t, tv, 0.3), col=CREAM, size=30, rot=2)
    if t > tc - 0.3: tag(c, 600, 1050, 'CLOTHES', pr(t, tc - 0.3, 0.4), t, rot=6, col=CREAM, size=70)
    if t > tf - 0.3:
        burst(c, 800, 1250, 150, '-25%', pr(t, tf - 0.3, 0.35), size=80, col=KINK, txt=YEL, rot=-8)
        caption(c, 'SALES, 2003', 700, 1390, pr(t, tf, 0.3), col=YEL, size=28, rot=2)
    for k_ in ('coaster', 'controller'):
        if (k_ == 'coaster' and t > tp) or (k_ == 'controller' and t > tv): credit(c, k_)


def sc_loss(c, t, S):
    t0 = S['t0']; tb = ph('biggest loss')
    bgp(c, t)
    caption(c, '2004', LX, 300, pr(t, t0, 0.3), col=YEL, size=40)
    def dr(cc):
        line_chart(cc, 860, 620, [(0, .8), (.25, .7), (.5, .45), (.75, .25), (1, .06)], pr(t, t0 + 0.2, 1.6), (205, 40, 40), 'LEGO RESULTS, 2002-2004 (ILLUSTRATIVE LINE)')
    panel(c, 110, 400, 860, 620, rot=-1.2, k=pr(t, t0, 0.4), draw=dr)
    stamp(c, 'BIGGEST LOSS EVER', 540, 1170, pr(t, tb - 0.2, 0.35), rot=-8, size=78)
    stick(c, 'brick', 860, 520, 220, pr(t, t0 + 0.3, 0.4), t, rot=20, amp=14)


def sc_cut(c, t, S):
    t0 = S['t0']; tc = ph('cut its costs'); tf = ph('a fifth'); tp = ph('legoland parks'); tb = ph('the brick', after=t0)
    bgp(c, t)
    caption(c, 'SO LEGO DID SOMETHING BRUTAL', LX, 300, pr(t, t0, 0.3), col=YEL, size=34)
    if t < tb - 0.6:
        kc = pr(t, tc - 0.2, 0.5)
        # distractions get sliced and fall away
        fall = pr(t, tp + 0.3, 1.2)
        stick(c, 'coaster', 640, 760 + 900 * eio(fall), 400, 1.0 - fall * 0.2, t, rot=4 + 40 * fall)
        stick(c, 'controller', 380, 960 + 900 * eio(pr(t, tf + 0.2, 1.2)), 380, 1.0, t, rot=-10 - 50 * pr(t, tf + 0.2, 1.2))
        if kc > 0:
            c.save(); c.drawLine(80, 1150 - 760 * kc, 80 + 920 * kc, 1150 - 760 * kc + 380 * kc, stroke(CHAR, 6)); c.restore()
        if t > tf - 0.3: tag(c, 230, 1180, 'COSTS -20%', pr(t, tf - 0.3, 0.35), t, rot=-6, size=82)
        if t > tp - 0.4: stamp(c, '4 PARKS: SOLD', 560, 560, pr(t, tp - 0.4, 0.35), rot=-10, size=80)
        credit(c, 'coaster')
        return
    two(c, 'BACK TO', 'THE BRICK.', 470, pr(t, tb - 0.6, 0.35), pr(t, tb - 0.2, 0.35), 110, 150)
    c.drawCircle(540, 980, 330 + 10 * math.sin(t * 2), paint(YEL, pr(t, tb - 0.6, 0.4)))
    stick(c, 'brick', 540, 990, 680, pr(t, tb - 0.5, 0.45), t, rot=-4)
    credit(c, 'brick')


def sc_back(c, t, S):
    t0 = S['t0']; tp = ph('profitable again'); ts = ph('sixteen percent'); tm = ph('grew seven'); tr = ph('twelve billion')
    bgp(c, t)
    caption(c, 'IT WORKED FAST', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    if t < ts - 0.4:
        def dr(cc):
            line_chart(cc, 860, 560, [(0, .1), (.25, .3), (.5, .48), (.75, .7), (1, .95)], pr(t, t0 + 0.2, 1.6), (40, 160, 70), 'BACK IN PROFIT FROM 2005 (ILLUSTRATIVE LINE)')
        panel(c, 110, 420, 860, 560, rot=1.2, k=pr(t, t0, 0.4), draw=dr)
        stamp(c, 'PROFIT AGAIN: 2005', 540, 1130, pr(t, tp - 0.2, 0.35), rot=-6, size=70)
        stick(c, 'brick', 880, 440, 220, pr(t, t0 + 0.3, 0.4), t, rot=-18, amp=14)
        return
    two(c, 'LAST YEAR', 'SALES GROWTH', 470, pr(t, ts - 0.4, 0.35), pr(t, ts - 0.2, 0.35), 96, 110)
    def dr(cc):
        cc.drawRect(R.MakeWH(860, 520), paint(CREAM))
        bars(cc, 140, 50, 580, 360, [('LEGO', 16, '+16%', YEL), ('TOY MARKET', 7, '+7%', (150, 150, 160))], pr(t, ts - 0.3, 1.2), 19)
        cc.drawString('CONSUMER SALES 2025 (LEGO GROUP, MAR 2026)', 50, 495, font('SpecialElite.ttf', 22), paint(GREY))
    panel(c, 110, 640, 860, 520, rot=-1, k=pr(t, ts - 0.4, 0.4), draw=dr)
    if t > tr - 0.3: tag(c, 330, 1230, 'REVENUE $12B+', pr(t, tr - 0.3, 0.35), t, rot=-6, size=80)


def sc_end(c, t, S):
    t0 = S['t0']; tl = ph('doing less'); tw = ph('what would you cut')
    bgp(c, t)
    caption(c, 'SAVED BY DOING LESS', LX, 300, pr(t, t0, 0.3), col=YEL, size=34)
    two(c, 'WHAT WOULD', 'YOU CUT?', 470, pr(t, tw - 0.3, 0.35), pr(t, tw, 0.35), 110, 150)
    c.drawCircle(540, 1020, 300 + 8 * math.sin(t * 2), paint(YEL))
    stick(c, 'brick', 540, 1030, 600, pr(t, t0 + 0.2, 0.4), t, rot=8)
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
    dict(k='focus', t0=ph('how do you break') - 0.2, fn=with_subs(sc_focus), tin='whip', col=CR),
    dict(k='loss', t0=ph('a year later') - 0.2, fn=with_subs(sc_loss), tin='zoom', col=CR),
    dict(k='cut', t0=ph('so lego did') - 0.2, fn=with_subs(sc_cut), tin='whip', col=CR),
    dict(k='back', t0=ph('it worked fast') - 0.2, fn=with_subs(sc_back), tin='wipe', col=CR),
    dict(k='end', t0=ph('lego got saved') - 0.2, fn=with_subs(sc_end), tin='flash', col=CR),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('almost went broke'), 12, 0.35)
EP.shk(ph('twenty-five percent'), 8, 0.3)
EP.shk(ph('biggest loss'), 10, 0.3)
EP.shk(ph('legoland parks'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
