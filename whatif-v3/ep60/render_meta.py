"""NextBigNow ep 60 (classic red/cream comic, real photo cut-outs, small subtitles, v5 voice, logo watermark): What if apps can see every photo on your phone?
Facts: The Hacker News / Reuters (Nov 2026) - Italy's Garante fined Meta EUR 805M (~$890M+) over Facebook for Android gallery-suggestion feature (since 2023,
on by default) accessing photos, videos and metadata without explicit consent (Art. 122 Privacy Code / ePrivacy); ~20M Android users in Italy; ~0.47% of
Meta global revenue; within 60 days separate consent, off by default; Meta to appeal, calls fine disproportionate. Cambridge Analytica (2018): up to 87M
users' data; FTC $5B penalty (July 2019), largest privacy penalty at the time.
Photos (Wikimedia Commons): see meta/img/credits.json. No brand logos shown."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('MT_DIR', 'meta'))
PK.IMG = os.path.join(HERE, 'meta', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))


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
GOLD = (245, 180, 40)


def credit(c, key, a=1.0, col=(120, 100, 70), y=1360):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s' % (cr['author'], cr['license'])).upper()[:70]
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0):
    def dr(cc): cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.01 * t, fx, fy)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def mini(c, x, y, w, h, rot, k, head, big, col, txtc=PAPER, bigsize=54):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(col)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=3.2, grad=(0.3, 1.0), a=0.25)
        cc.drawString(head, 22, 44, font('SpecialElite.ttf', 26), paint(PAPER if col in (CRED, CBLU) else KINK))
        title(cc, big, 22, h - 36, bigsize, txtc, 1.0, shadow=4)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)


def down_chart(cc, w, h, k, pts, color=CRED, labels=()):
    x0, y0, cw, ch = 60, 50, w - 110, h - 130
    vmax = max(v for _, v in pts); vmin = 0
    yv = lambda v: y0 + ch - (v - vmin) / (vmax - vmin) * ch
    cc.drawLine(x0, y0 + ch, x0 + cw, y0 + ch, stroke(KINK, 5)); cc.drawLine(x0, y0, x0, y0 + ch, stroke(KINK, 5))
    p = skia.Path(); first = True
    for fx, v in pts:
        if fx > k: break
        (p.moveTo if first else p.lineTo)(x0 + fx * cw, yv(v)); first = False
    cc.drawPath(p, stroke(KINK, 16)); cc.drawPath(p, stroke(color, 9))
    for fx, s in labels:
        cc.drawString(s, x0 + fx * cw - 30, y0 + ch + 44, font('SpecialElite.ttf', 24), paint(KINK))


def coin(c, x, y, w, rot=0.0, a=1.0, crack=0.0, split=0.0):
    """the gold coin sticker; crack draws a zig-zag ink line, split pulls the halves apart."""
    if split <= 0:
        place(c, 'K1_coin_comic.png', x, y, w, rot=rot, a=a, shadow=True)
    else:
        for sgn in (-1, 1):
            c.save()
            c.clipRect(R.MakeLTRB(x - w if sgn < 0 else x, y - w, x if sgn < 0 else x + w, y + w))
            place(c, 'K1_coin_comic.png', x + sgn * 60 * split, y + 30 * split * sgn, w, rot=rot + sgn * 10 * split, a=a, shadow=True)
            c.restore()
    if crack > 0 and split <= 0:
        pts = [(0, -0.5), (-0.06, -0.3), (0.05, -0.12), (-0.04, 0.05), (0.06, 0.22), (-0.03, 0.38), (0.02, 0.5)]
        n = max(2, int(len(pts) * crack + 0.999))
        p = skia.Path()
        for i, (fx, fy) in enumerate(pts[:n]):
            (p.moveTo if i == 0 else p.lineTo)(x + fx * w, y + fy * w)
        c.drawPath(p, stroke(KINK, 14 * a)); c.drawPath(p, stroke(PAPER, 4 * a))



GAL = ['M2_photographer', 'M3_camera', 'M4_rome', 'M5_servers']


def phone(c, cx, cy, w, k, t, scan=0.0, rot=0.0):
    """comic phone frame showing a gallery grid of REAL photo thumbnails."""
    if k <= 0: return
    h = w * 2.0
    c.save(); c.translate(cx, cy); c.rotate(rot); s_ = eback(cl(k), 1.4); c.scale(s_, s_)
    rr = skia.RRect.MakeRectXY(R.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.12, w * 0.12)
    c.save(); c.translate(14, 14); c.drawRRect(rr, paint(KINK)); c.restore()
    c.drawRRect(rr, paint((30, 30, 34)))
    m = w * 0.06; sx, sy, sw, sh = -w / 2 + m, -h / 2 + m * 2.2, w - 2 * m, h - m * 4.4
    c.drawRect(R.MakeXYWH(sx, sy, sw, sh), paint(PAPER))
    cols, gap = 2, 10
    tw = (sw - gap * (cols + 1)) / cols; th = tw
    i = 0
    for r in range(4):
        for col in range(cols):
            x = sx + gap + col * (tw + gap); y = sy + gap + r * (th + gap)
            if y + th > sy + sh: break
            c.save(); c.clipRect(R.MakeXYWH(x, y, tw, th))
            cover(c, img(GAL[i % len(GAL)] + '_comic.png'), x, y, tw, th, 1.3, 0.5, 0.5)
            c.restore(); c.drawRect(R.MakeXYWH(x, y, tw, th), stroke(KINK, 3))
            i += 1
    if scan > 0:
        yy = sy + sh * ((t * 0.6) % 1)
        c.drawRect(R.MakeXYWH(sx, yy - 8, sw, 16), paint(CRED, 0.75 * scan))
        c.drawRect(R.MakeXYWH(sx, sy, sw, sh), paint(CRED, 0.12 * scan))
    c.drawRRect(rr, stroke(KINK, 9))
    c.drawCircle(0, -h / 2 + m * 1.1, m * 0.35, paint(KINK))
    c.restore()


def fly_card(c, key, x, y, w, rot, k):
    if k <= 0: return
    def dr(cc): cover(cc, img(key + '_comic.png'), 0, 0, w, w * 0.75, 1.1, 0.5, 0.5)
    panel(c, x, y, w, w * 0.75, rot=rot, k=k, draw=dr, border=6, shadow=8)


def sc_hook(c, t, S):
    tf = ph('eight hundred and five'); tn = ph('nine hundred million'); tl = ph('looking at the photos'); te = ph('never posted'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'ITALY . NOVEMBER 2026', LX, 340, 1.0, col=CYEL, size=30)
        title(c, 'EUR 805M', 80, 540, 170, CRED, 1.0, rot=-2)
        title(c, 'FINE.', 90, 690, 150, CBLU, pr(t, tf + 0.6, 0.4))
        phone(c, 400, 1080, 330, pr(t, 0, 0.6), t, scan=pr(t, tl - 0.2, 0.4), rot=-6)
        for i, (key, x, y, r_) in enumerate((('M3_camera', 640, 820, 8), ('M4_rome', 680, 1050, -6))):
            kk = pr(t, tl + 0.3 * i, 0.4)
            fly_card(c, key, x + 40 * (1 - kk), y, 300, r_, kk)
        if t > tn - 0.2: caption(c, '~$900 MILLION', 600, 760, pr(t, tn - 0.2, 0.3), col=PAPER, size=30, rot=4)
        if t > te - 0.2: burst(c, 820, 1290, 115, 'NEVER POSTED!', pr(t, te - 0.2, 0.35), size=28, rot=8)
        credit(c, 'M3_camera')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF APPS', 90, 540, 130, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'SEE EVERY', 90, 680, 140, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'PHOTO?', 90, 830, 160, PAPER, pr(t, tq + 0.45, 0.4))
    phone(c, 760, 1150, 250, pr(t, tq + 0.5, 0.6), t, scan=1.0, rot=8)


def sc_what(c, t, S):
    ts = ph('since twenty twenty three'); tsug = ph('suggested photos'); td = ph('on by default'); tw = ph('privacy watchdog'); th = ph('hidden data'); t20 = ph('twenty million android')
    paper(c, t)
    caption(c, "HERE'S WHAT HAPPENED", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tw - 0.3:
        title(c, 'A FEATURE', 90, 540, 150, CBLU, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'IN THE APP.', 90, 690, 130, CRED, pr(t, tsug - 0.2, 0.4), rot=-2)
        mini(c, 90, 790, 430, 260, -2, pr(t, ts - 0.3, 0.4), 'ON ANDROID SINCE', '2023', CBLU, bigsize=90)
        mini(c, 560, 810, 430, 260, 1.5, pr(t, td - 0.4, 0.4), 'SETTING', 'ON BY DEFAULT', CRED, bigsize=42)
        photo_panel(c, 'M2_photographer', 220, 1100, 640, 250, -1, pr(t, tsug, 0.5), fy=0.4, t=t - tsug)
        credit(c, 'M2_photographer')
        return
    title(c, 'ITALY SAYS:', 90, 540, 140, CBLU, pr(t, tw - 0.3, 0.4))
    title(c, 'NO CLEAR OK.', 80, 690, 120, CRED, pr(t, th - 0.4, 0.4), rot=-2)
    photo_panel(c, 'M4_rome', 90, 780, 900, 520, 1.2, pr(t, tw, 0.5), t=t - tw)
    if t > t20 - 0.3: burst(c, 800, 840, 125, '20M USERS', pr(t, t20 - 0.3, 0.35), size=40, rot=8)
    caption(c, 'ROME, ITALY', 200, 1250, pr(t, tw + 0.5, 0.3), col=CYEL, size=26)
    credit(c, 'M4_rome')


def sc_hidden(c, t, S):
    tp = ph("photo isn't just"); tt = ph('time it was taken'); tph = ph('the phone that took'); tl = ph('exact location'); tw = ph('where you live')
    paper(c, t)
    caption(c, 'THE HIDDEN DATA', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    title(c, 'A PHOTO IS', 90, 540, 140, CBLU, pr(t, tp - 0.3, 0.4))
    title(c, 'MORE THAN...', 90, 690, 130, CRED, pr(t, tp + 0.3, 0.4), rot=-2)
    fly_card(c, 'M3_camera', 120, 790, 520, -4, pr(t, tp, 0.5))
    tags = ((tt, 'TIME: 18:42', CBLU), (tph, 'PHONE MODEL', CYEL), (tl, 'GPS: YOUR STREET', CRED))
    for i, (t0, s_, col) in enumerate(tags):
        caption(c, s_, 600 - 20 * i, 860 + i * 130, pr(t, t0 - 0.2, 0.3), col=col, size=34, rot=(3, -2, 2)[i])
    if t > tw - 0.3: burst(c, 760, 1290, 120, 'YOUR HOME!', pr(t, tw - 0.3, 0.35), size=38, rot=8)
    credit(c, 'M3_camera')


def sc_meta(c, t, S):
    td = ph('disproportionate'); ta = ph('plans to appeal'); tp = ph('give permission'); ts = ph('switch it off'); to = ph('one tap'); tc = ph('consent for every use')
    paper(c, t)
    caption(c, 'BOTH SIDES', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    title(c, 'META:', 90, 540, 150, CBLU, pr(t, S['t0'] + 0.2, 0.4))
    bubble(c, 540, 760, 820, 220, 'DISPROPORTIONATE!', (300, 900), pr(t, td - 0.3, 0.4), size=48)
    if t > tp - 0.3: caption(c, 'USERS GAVE PERMISSION + CAN SWITCH IT OFF', 110, 960, pr(t, tp - 0.3, 0.3), col=CBLU, size=26, rot=-1.5)
    if t > to - 0.4:
        title(c, 'ITALY:', 90, 1110, 130, CRED, pr(t, to - 0.4, 0.4))
        caption(c, '1 TAP =/= CONSENT FOR EVERYTHING', 120, 1230, pr(t, to, 0.3), col=CRED, size=32, rot=1.5)


def sc_ca(c, t, S):
    t18 = ph('in twenty eighteen'); tca = ph('cambridge analytica'); t87 = ph('eighty seven million'); tn = ph('never agreed'); tf = ph('federal trade commission'); t5 = ph('five billion dollars'); tb = ph('biggest privacy fine')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN THIS BEFORE", LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < tf - 0.3:
        title(c, '2018:', 90, 540, 160, CBLU, pr(t, t18 - 0.2, 0.4))
        title(c, 'THE BIG LEAK.', 80, 690, 130, CRED, pr(t, tca - 0.2, 0.4), rot=-2)
        mini(c, 90, 790, 430, 300, -2, pr(t, t87 - 0.3, 0.4), 'FACEBOOK USERS', 'UP TO 87M', CRED, bigsize=64)
        mini(c, 560, 810, 430, 300, 1.5, pr(t, tn - 0.3, 0.4), 'HOW MANY AGREED?', 'MOST: NO', CBLU, bigsize=60)
        caption(c, 'CAMBRIDGE ANALYTICA', 220, 1180, pr(t, tca, 0.3), col=CYEL, size=32, rot=-1.5)
        return
    title(c, '2019 FINE:', 90, 540, 150, CBLU, pr(t, tf - 0.3, 0.4))
    title(c, '$5 BILLION', 80, 700, 160, CRED, pr(t, t5 - 0.3, 0.4), rot=-2)
    k = pr(t, t5, 0.5)
    for i in range(4):
        kk = pr(t, t5 + 0.15 * i, 0.4)
        if kk > 0: place(c, 'D4_dollar_comic.png', 300 + 160 * i, 1250 - 30 * i, 420 * eback(cl(kk), 1.5), rot=-12 + 8 * i, a=kk, shadow=True)
    if t > tb - 0.3: burst(c, 540, 1050, 190, 'RECORD AT THE TIME', pr(t, tb - 0.3, 0.35), size=36, col=CYEL, txt=CRED, rot=-4)
    caption(c, 'U.S. FEDERAL TRADE COMMISSION', 160, 830, pr(t, tf, 0.3), col=PAPER, size=28, rot=-1.5)


def sc_predict(c, t, S):
    tfa = ph("fines alone won't"); th = ph('half a percent'); to = ph('the order that comes'); t60 = ph('sixty days'); tc = ph('copy that rule'); tfix = ph('the simple fix'); tsel = ph('selected photos only')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < tfix - 0.3:
        title(c, 'THE FINE?', 90, 540, 150, PAPER, pr(t, tfa - 0.2, 0.4))
        title(c, '< 0.5% OF SALES', 80, 690, 110, CYEL, pr(t, th - 0.3, 0.4))
        caption(c, 'THE REAL CHANGE: THE NEW RULE', 110, 860, pr(t, to - 0.2, 0.3), col=PAPER, size=30, rot=-2)
        if t > t60 - 0.3: caption(c, '60 DAYS: ASK FIRST. OFF BY DEFAULT.', 140, 980, pr(t, t60 - 0.3, 0.3), col=CYEL, size=30, rot=1.5)
        if t > tc - 0.3: burst(c, 760, 1250, 130, 'MORE COUNTRIES', pr(t, tc - 0.3, 0.35), size=32, col=CYEL, txt=CRED, rot=8)
        return
    title(c, 'YOUR FIX:', 90, 560, 160, PAPER, pr(t, tfix - 0.3, 0.4))
    caption(c, 'SETTINGS > APPS > PHOTOS', 120, 740, pr(t, tfix + 0.6, 0.3), col=CYEL, size=36, rot=-2)
    caption(c, '"SELECTED PHOTOS ONLY"', 160, 870, pr(t, tsel - 0.3, 0.3), col=PAPER, size=40, rot=1.5)
    phone(c, 540, 1180, 200, pr(t, tfix, 0.6), t, scan=0.0, rot=-4)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'DO APPS SEE', 90, 530, 130, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'ALL YOUR PHOTOS?', 70, 670, 104, CRED, pr(t, S['t0'] + 0.3, 0.4))
    phone(c, 540, 1010, 210, pr(t, S['t0'] + 0.3, 0.6), t, scan=1.0, rot=4)
    burst(c, 230, 1250, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 850, 1250, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    cta = 'SUBSCRIBE FOR DAILY WHAT IFS' if PLAT == 'yt' else 'SEND THIS TO A FRIEND WHO SAID YES'
    caption(c, cta, 190, 1375, pr(t, ph('yes or no') + 0.6, 0.3), col=CYEL, size=30, rot=-1.5)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(k2), paint(CRED))


PLAT = os.environ.get('PLAT', 'ig')
SUBY = 1530 if PLAT == 'yt' else 1442


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS, y=SUBY)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='what', t0=ph("here's what happened") - 0.2, fn=with_subs(sc_what), tin='whip'),
    dict(k='hidden', t0=ph('and that hidden data') - 0.2, fn=with_subs(sc_hidden), tin='zoom'),
    dict(k='meta', t0=ph('meta says the fine') - 0.2, fn=with_subs(sc_meta), tin='whip'),
    dict(k='ca', t0=ph("and we've seen this") - 0.2, fn=with_subs(sc_ca), tin='wipe', col=SEPIA),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('eight hundred and five'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
