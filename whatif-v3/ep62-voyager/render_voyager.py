"""NextBigNow ep 62 (red/cream comic, real NASA photo cut-outs, small subtitles, v5 voice, logo watermark): Voyager 1 reaches one light-day.
Facts: NASA/JPL via EarthSky & IFLScience: 1 light-day (~16.1 billion mi / 25.9 billion km) at 10:16:07 UTC Nov 18, 2026; launched Sep 5, 1977;
interstellar space 2012; most instruments off to save power (LECP off April 2026); golden record (greetings in 55 languages);
~40,000 yrs: within 1.7 ly of Gliese 445. FDS memory chip failure Nov 2023 -> gibberish; fixed by moving code, readable data again April 2024
(one-way light time then ~22.5 h, round trip ~45 h; distance ~15 billion mi). Transmitter ~22 W. DSN 70 m dishes.
Photos: NASA / JPL (public domain) via Wikimedia Commons, see voyager/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('VY_DIR', 'voyager'))
PK.IMG = os.path.join(HERE, 'voyager', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))
PLAT = os.environ.get('PLAT', 'ig')
SUBY = 1530 if PLAT == 'yt' else 1442


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z0-9']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
LX = 90
SEPIA = (240, 222, 186)
GRN = (80, 200, 120)
MONO = 'SpecialElite.ttf'


def credit(c, key, a=1.0, col=(120, 100, 70), y=1360):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s' % (cr['author'], cr['license'])).upper()[:70]
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0):
    def dr(cc): cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.01 * t, fx, fy)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def probe(c, x, y, w, t, k=1.0, rot0=0.0):
    if k <= 0: return
    place(c, 'Y1_cut_comic.png', x, y, w * eback(cl(k), 1.4), rot=rot0 + 3 * math.sin(t * 0.9), a=cl(k * 2), shadow=True)


def earth(c, x, y, r, a=1.0):
    c.drawCircle(x + 5, y + 5, r, paint(KINK, a))
    c.drawCircle(x, y, r, paint(CBLU, a))
    c.drawCircle(x - r * 0.3, y - r * 0.2, r * 0.45, paint(GRN, a))
    c.drawCircle(x, y, r, stroke(KINK, max(3, r * 0.12), a=a))


def beam(c, x0, y0, x1, y1, k, col=CYEL):
    """a light pulse travelling from Earth outward (dashed comic beam + glowing head)."""
    if k <= 0: return
    kk = cl(k)
    xe, ye = lerp(x0, x1, kk), lerp(y0, y1, kk)
    p = stroke(KINK, 16); c.drawLine(x0, y0, xe, ye, p)
    p2 = stroke(col, 8); p2.setPathEffect(skia.DashPathEffect.Make([26, 16], 0)); c.drawLine(x0, y0, xe, ye, p2)
    c.drawCircle(xe, ye, 20, paint(KINK)); c.drawCircle(xe, ye, 14, paint(col))


def ruler(cc, w, h, k, t):
    """distance ruler: Moon / Neptune / Voyager. log-ish visual placement."""
    y = h * 0.55
    cc.drawLine(40, y, w - 40, y, stroke(KINK, 8))
    marks = [(0.04, 'EARTH', CBLU), (0.18, 'MOON', GREY), (0.52, 'NEPTUNE', CCYN), (0.93, 'VOYAGER 1', CRED)]
    for i, (fx, lab, col) in enumerate(marks):
        kk = pr(k, i * 0.22, 0.25)
        if kk <= 0: continue
        X = 40 + (w - 80) * fx
        cc.drawLine(X, y - 30, X, y + 30, stroke(KINK, 7))
        cc.drawCircle(X, y, 16 * eback(kk, 1.6), paint(col)); cc.drawCircle(X, y, 16 * eback(kk, 1.6), stroke(KINK, 5))
        s = lab; f = font(MONO, 34)
        cc.drawString(s, X - width(s, MONO, 34) / 2 if i < 3 else X - width(s, MONO, 34) + 30 if i else X - 10, y - 50 if i % 2 else y + 76, f, paint(KINK, kk))


def bulb(c, x, y, s, k, on=1.0):
    if k <= 0: return
    c.save(); c.translate(x, y); sc = s * eback(cl(k), 1.5); c.scale(sc, sc)
    if on > 0:
        for i in range(10):
            a = i * math.pi / 5
            c.drawLine(math.cos(a) * 70, -20 + math.sin(a) * 70, math.cos(a) * 100, -20 + math.sin(a) * 100, stroke(CYEL, 10, a=on))
    c.drawCircle(4, -16, 56, paint(KINK)); c.drawCircle(0, -20, 56, paint(lerp_col(PAPER, CYEL, on)))
    c.drawCircle(0, -20, 56, stroke(KINK, 7))
    c.drawRect(R.MakeXYWH(-26, 28, 52, 44), paint(GREY)); c.drawRect(R.MakeXYWH(-26, 28, 52, 44), stroke(KINK, 6))
    for yy in (40, 52, 64): c.drawLine(-26, yy, 26, yy, stroke(KINK, 4))
    c.restore()


def lerp_col(a, b, k):
    return tuple(int(lerp(a[i], b[i], k)) for i in range(3))


def terminal(cc, w, h, t, t_bad, t_fix):
    """1970s green-screen: clean telemetry -> gibberish -> fixed."""
    cc.drawRect(R.MakeWH(w, h), paint((20, 28, 22)))
    f = font(MONO, 30)
    good = ['FDS  OK', 'TLM  NOMINAL', 'MAG  14.2 nT', 'PWS  OK']
    for i in range(6):
        y = 70 + i * 52
        if t < t_bad or t > t_fix:
            s = good[i % 4] if i < 4 else ('ENGINEERING DATA RESTORED' if t > t_fix and i == 5 else '')
            col = (90, 240, 120)
        else:
            rnd = int(t * 12) * 7 + i * 13
            s = ''.join('01#%&X?@$*'[(rnd * (j + 3) + j * j) % 10] for j in range(18))
            col = (240, 90, 80) if i % 2 else (90, 240, 120)
        cc.drawString(s, 40, y, f, paint(col))
    # scanlines
    for yy in range(0, int(h), 6): cc.drawLine(0, yy, w, yy, stroke((0, 0, 0), 2, a=0.25))


def battery(cc, w, h, k):
    x0, y0, bw, bh = 60, 70, w - 160, 150
    cc.drawRect(R.MakeXYWH(x0 + 8, y0 + 8, bw, bh), paint(KINK))
    cc.drawRect(R.MakeXYWH(x0, y0, bw, bh), paint(PAPER))
    lvl = lerp(0.9, 0.12, eio(cl(k)))
    col = CRED if lvl < 0.3 else CYEL
    cc.drawRect(R.MakeXYWH(x0 + 12, y0 + 12, (bw - 24) * lvl, bh - 24), paint(col))
    cc.drawRect(R.MakeXYWH(x0, y0, bw, bh), stroke(KINK, 8))
    cc.drawRect(R.MakeXYWH(x0 + bw, y0 + 45, 30, 60), paint(KINK))
    inst = ['CAMERAS', 'IR SPECTROMETER', 'PLASMA', 'LOW-ENERGY PARTICLES', 'MAGNETOMETER']
    for i, s in enumerate(inst):
        y = y0 + bh + 70 + i * 52
        off = k > 0.15 + 0.17 * i and i < 4
        cc.drawCircle(x0 + 16, y - 10, 14, paint(CRED if off else GRN)); cc.drawCircle(x0 + 16, y - 10, 14, stroke(KINK, 4))
        cc.drawString(s + ('  OFF' if off else '  ON'), x0 + 46, y, font(MONO, 28), paint(KINK))


def sc_hook(c, t, S):
    tl = ph('this little machine'); t77 = ph('nineteen seventy seven'); tw = ph('and on wednesday'); tf = ph('a full day')
    paper(c, t, tint=SEPIA)
    # visual first: the real launch
    photo_panel(c, 'Y5_launch', 190, 320, 700, 640, -1.5, pr(t, 0.0, 0.45), fy=0.35, t=t)
    credit(c, 'Y5_launch')
    if t > t77 - 0.3: burst(c, 820, 420, 120, 'SEPT 5, 1977', pr(t, t77 - 0.3, 0.35), size=32, rot=8)
    probe(c, 520 + 140 * eo(pr(t, tw, 2.0)), 1160 - 50 * eo(pr(t, tw, 2.0)), 470, t, pr(t, tl + 0.4, 0.5), rot0=-10)
    if t > tf - 0.5:
        caption(c, 'LIGHT NEEDS A FULL DAY TO REACH IT', 150, 1360, pr(t, tf - 0.5, 0.3), col=CYEL, size=28, rot=-1.5)


def sc_far(c, t, S):
    tv = ph('this is voyager one'); tn = ph('november eighteenth'); ts = ph('sixteen billion miles'); tno = ph('no human made object')
    paper(c, t)
    caption(c, 'NOVEMBER 18, 2026', LX, 340, pr(t, tn - 0.2, 0.3), col=CRED, size=30)
    title(c, 'VOYAGER 1', 90, 540, 150, CBLU, pr(t, tv, 0.4))
    title(c, '1 LIGHT-DAY', 90, 700, 140, CRED, pr(t, tn + 0.3, 0.4), rot=-2)
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 360), paint(PAPER))
        ruler(cc, 900, 360, pr(t, tn, 2.4), t)
    panel(c, 90, 780, 900, 360, rot=1.0, k=pr(t, tv + 0.3, 0.5), draw=dr)
    if t > ts - 0.3:
        title(c, '16,000,000,000', 540, 1270, 92, CYEL, pr(t, ts - 0.3, 0.4), 'c', rot=-1.5)
        caption(c, 'MILES FROM EARTH', 380, 1330, pr(t, ts + 0.3, 0.3), size=26)
    if t > tno - 0.3: burst(c, 890, 600, 95, 'FARTHEST EVER', pr(t, tno - 0.3, 0.35), size=28, col=CRED, txt=CYEL, rot=7)


def sc_radio(c, t, S):
    tst = ph('still talking to us'); t20 = ph('twenty watts'); tb = ph('the bulb in your fridge'); tw_ = ph('that whisper'); td = ph('dishes the size')
    paper(c, t)
    caption(c, 'IT STILL TALKS TO US', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tw_ - 0.3:
        title(c, 'ITS RADIO:', 90, 530, 120, CBLU, pr(t, S['t0'] + 0.4, 0.4))
        title(c, '~20 WATTS', 90, 700, 170, CRED, pr(t, t20 - 0.3, 0.4), rot=-2)
        probe(c, 330, 1030, 420, t, pr(t, S['t0'] + 0.2, 0.5), rot0=-8)
        bulb(c, 790, 1020, 1.6, pr(t, tb - 0.3, 0.5), on=0.5 + 0.5 * abs(math.sin(t * 3)))
        if t > tb: caption(c, '= A FRIDGE BULB', 640, 1230, pr(t, tb, 0.3), col=CYEL, size=30, rot=-2)
        return
    title(c, 'TO HEAR IT:', 90, 540, 130, CBLU, pr(t, tw_ - 0.3, 0.4))
    title(c, 'GIANT DISHES', 90, 690, 130, CRED, pr(t, td - 0.3, 0.4), rot=-2)
    photo_panel(c, 'Y4_dish', 90, 770, 900, 560, 1.2, pr(t, tw_, 0.5), t=t - tw_)
    credit(c, 'Y4_dish')
    if t > td: burst(c, 820, 840, 120, '70 METERS', pr(t, td, 0.35), size=40, rot=8)


def sc_glitch(c, t, S):
    tc = ph('crazy part'); tg = ph('gibberish'); tm = ph('memory chip had died'); te = ph('so engineers took'); tn = ph('two days of waiting'); tr = ph('rewrote its code'); ta = ph('in april'); tsp = ph('it spoke again')
    if t < te - 0.2:
        bg_flat(c, CRED, (190, 20, 30))
        caption(c, 'LATE 2023', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
        title(c, 'IT STARTED', 90, 540, 140, PAPER, pr(t, tc, 0.4))
        title(c, 'SPEAKING NONSENSE', 80, 680, 96, CYEL, pr(t, tg - 0.4, 0.4), rot=-2)
        def dr(cc): terminal(cc, 900, 380, t, tg - 0.3, 1e9)
        panel(c, 90, 780, 900, 380, rot=-1.0, k=pr(t, tc + 0.3, 0.5), draw=dr)
        if t > tm - 0.3: burst(c, 800, 1230, 130, '1 CHIP DIED', pr(t, tm - 0.3, 0.35), size=38, col=CYEL, txt=CRED, rot=-6)
        return
    paper(c, t)
    caption(c, 'THE FIX', LX, 340, pr(t, te - 0.2, 0.3), col=CBLU, size=30)
    title(c, 'NEW CODE,', 90, 540, 140, CBLU, pr(t, te, 0.4))
    title(c, '15 BILLION MI AWAY', 80, 680, 92, CRED, pr(t, tr - 0.3, 0.4), rot=-2)
    # ping: Earth -> probe and back (45 h round trip)
    earth(c, 180, 900, 60)
    probe(c, 860, 880, 260, t, pr(t, te + 0.2, 0.5), rot0=10)
    k1 = pr(t, tn - 0.4, 1.2); k2 = pr(t, tn + 0.9, 1.2)
    if k2 <= 0: beam(c, 250, 900, 760, 890, k1)
    else: beam(c, 760, 890, 250, 900, k2, col=GRN)
    tc70 = ph('computer from the seventies'); tsp_ = ph('no spare parts')
    if t > tc70 - 0.2 and t < tn - 0.4: caption(c, 'A COMPUTER FROM 1977', 300, 1100, pr(t, tc70 - 0.2, 0.3), col=PAPER, size=34, rot=-1.5)
    if t > tsp_ - 0.2 and t < tn - 0.4: burst(c, 540, 1260, 120, 'NO SPARE PARTS', pr(t, tsp_ - 0.2, 0.35), size=32, col=CRED, txt=CYEL, rot=-5)
    if t > tn: caption(c, '~45 HOURS FOR EVERY REPLY', 220, 1040, pr(t, tn, 0.3), col=CYEL, size=30, rot=-1.5)
    if t > ta - 0.3:
        def dr(cc): terminal(cc, 760, 330, t, -1, ta - 0.3)
        panel(c, 160, 1080, 760, 330, rot=1.0, k=pr(t, ta - 0.3, 0.5), draw=dr)
    if t > tsp - 0.2: burst(c, 830, 1100, 120, 'APRIL 2024: IT SPOKE!', pr(t, tsp - 0.2, 0.35), size=26, col=GRN, txt=PAPER, rot=7)


def sc_power(c, t, S):
    tp = ph('power is running out'); ti = ph('most of its instruments'); tq = ph('go quiet forever'); tg = ph('golden record'); th = ph('fifty five languages')
    if t < tq - 0.2:
        paper(c, t)
        caption(c, 'THE BATTERY IS FADING', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
        title(c, 'SWITCHING OFF', 90, 540, 130, CRED, pr(t, ti - 0.3, 0.4))
        title(c, 'ONE BY ONE', 90, 680, 130, CBLU, pr(t, ti + 0.3, 0.4), rot=-2)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 560), paint(PAPER)); battery(cc, 900, 560, pr(t, tp - 0.3, (tq - tp) + 0.2))
        panel(c, 90, 760, 900, 560, rot=1.0, k=pr(t, S['t0'] + 0.2, 0.5), draw=dr)
        return
    bg_flat(c, KINK, (40, 36, 30))
    caption(c, 'ITS LAST MESSAGE TO THE STARS', LX, 340, pr(t, tq - 0.2, 0.3), col=CYEL, size=30)
    title(c, 'THE GOLDEN', 90, 540, 140, CYEL, pr(t, tg - 0.4, 0.4))
    title(c, 'RECORD', 90, 690, 150, PAPER, pr(t, tg, 0.4), rot=-2)
    k = pr(t, tq, 0.6)
    place(c, 'Y2_cut_comic.png', 540, 1040, 560 * eback(cl(k), 1.3), rot=(t - tq) * 25, a=cl(k * 2), shadow=True)
    credit(c, 'Y2_record', col=PAPER)
    if t > th - 0.3: burst(c, 830, 1290, 110, 'HELLO x55', pr(t, th - 0.3, 0.35), size=40, rot=8)


def sc_star(c, t, S):
    tf = ph('forty thousand years'); ts = ph('another star')
    bg_flat(c, KINK, (40, 36, 30))
    caption(c, 'THE YEAR 42,000', LX, 340, pr(t, S['t0'], 0.3), col=CYEL, size=30)
    title(c, '40,000', 540, 600, 200, CYEL, pr(t, tf - 0.2, 0.4), 'c', rot=-2)
    title(c, 'YEARS FROM NOW', 540, 720, 80, PAPER, pr(t, tf + 0.3, 0.4), 'c')
    k = pr(t, ts - 0.3, 0.6)
    if k > 0:
        c.drawCircle(780, 1060, 120 * eback(k, 1.4), paint(CYEL)); c.drawCircle(780, 1060, 120 * eback(k, 1.4), stroke(KINK, 8))
        for i in range(8):
            a = i * math.pi / 4 + t * 0.4
            c.drawLine(780 + math.cos(a) * 150, 1060 + math.sin(a) * 150, 780 + math.cos(a) * 200 * k, 1060 + math.sin(a) * 200 * k, stroke(CYEL, 10))
        caption(c, 'GLIESE 445', 690, 1250, k, col=PAPER, size=26)
    probe(c, 260 + 160 * pr(t, S['t0'], 4.0), 1080, 300, t, pr(t, S['t0'] + 0.2, 0.5), rot0=-6)


def sc_ask(c, t, S):
    ty = ph('yes or no')
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'IF ALIENS FIND IT,', 80, 530, 100, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'GOOD IDEA?', 80, 670, 140, CRED, pr(t, S['t0'] + 0.5, 0.4), rot=-2)
    kb = pr(t, S['t0'] + 0.3, 0.5)
    photo_panel(c, 'Y3_bluedot', 240, 760, 600, 420, 0.0, kb, zoom=1.6, fx=0.594, fy=0.519)
    kc = pr(t, S['t0'] + 0.9, 0.4)
    if kc > 0:
        c.drawCircle(540, 970, 46 * eback(kc, 1.6), stroke(KINK, 12)); c.drawCircle(540, 970, 46 * eback(kc, 1.6), stroke(CRED, 7))
        caption(c, 'EARTH', 600, 900, kc, col=CRED, size=26)
    caption(c, 'US, FROM VOYAGER, 1990', 300, 1150, pr(t, S['t0'] + 0.8, 0.3), col=CYEL, size=24)
    credit(c, 'Y3_bluedot')
    burst(c, 230, 1260, 100, 'YES', pr(t, ty - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 850, 1260, 100, 'NO', pr(t, ty + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    cta = 'SUBSCRIBE FOR DAILY WHAT IFS' if PLAT == 'yt' else 'SEND THIS TO A SPACE NERD'
    caption(c, cta, 250, 1375, pr(t, ty + 0.6, 0.3), col=CYEL, size=28, rot=-1.5)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(k2), paint(CRED))


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS, y=SUBY)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='far', t0=ph('this is voyager one') - 0.15, fn=with_subs(sc_far), tin='whip'),
    dict(k='radio', t0=ph('and it is still talking') - 0.2, fn=with_subs(sc_radio), tin='zoom'),
    dict(k='glitch', t0=ph("now here's the crazy") - 0.2, fn=with_subs(sc_glitch), tin='flash'),
    dict(k='power', t0=ph('but its power') - 0.2, fn=with_subs(sc_power), tin='whip'),
    dict(k='star', t0=ph('in forty thousand') - 0.2, fn=with_subs(sc_star), tin='zoom'),
    dict(k='ask', t0=ph('so what if someone') - 0.2, fn=with_subs(sc_ask), tin='flash'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(0.2, 10, 0.35)
EP.shk(ph('gibberish'), 9, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
