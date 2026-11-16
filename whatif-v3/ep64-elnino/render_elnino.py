"""NextBigNow ep 64 (red/cream comic, FLOW style: every scene on a living colour set, cut-outs always moving, no blank frames): super El Nino.
Facts: NOAA CPC via NPR (Oct 5, 2026) and Watchers (Nov 10, 2026): very strong El Nino, RONI ~+2.0 C Aug-Oct 2026, strongest on record for
the season so far (second only to 1997-98 on RONI for Aug-Oct; traditional ONI +2.46 C above 1997 and 2015); peak expected Nov-Dec; persists
into early 2027. As of early Nov 2026 the Atlantic had produced only one hurricane, the fewest since 1925. WFP: El Nino could push at least
49 million more people into acute food insecurity by end of 2027. 1997-98: floods in Peru and California, Indonesian fires; 1998 became the
hottest year on record at that time. Possible effects: wetter US South, weaker rains India/Australia, higher food prices; 2027 may set a heat record.
Photos: NASA, NOAA, ESA and Wikimedia Commons contributors, see elnino/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('EN_DIR', 'elnino'))
PK.IMG = os.path.join(HERE, 'elnino', 'img')
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
GRN = (80, 200, 120)
ORG = (245, 130, 40)
MONO = 'SpecialElite.ttf'


def credit(c, key, a=1.0, col=(120, 100, 70), y=1360):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s' % (cr['author'], cr['license'])).upper()[:70]
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def has(key):
    return os.path.exists(os.path.join(PK.IMG, key))


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0):
    if not has(key + '_comic.png'): return
    def dr(cc): cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.012 * t, fx, fy)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def cut(c, name, x, y, w, k, rot=0.0, t=0.0, bob=10, spin=0.0):
    """a cut-out that pops in and keeps floating."""
    if k <= 0 or not has(name): return
    place(c, name, x, y + bob * math.sin(t * 1.6 + x * 0.01), w * eback(cl(k), 1.4), rot=rot + spin * t + 2 * math.sin(t * 1.1), a=cl(k * 2), shadow=True)


def flow_bg(c, t, col, cx=540, cy=980, r0=520):
    """living set: cream paper + big breathing colour circle + slow rays. never a blank frame."""
    paper(c, t)
    c.save(); c.translate(cx, cy); c.rotate(t * 6)
    for i in range(16):
        a0 = i * math.pi / 8
        p = skia.Path(); p.moveTo(0, 0)
        p.lineTo(math.cos(a0) * 1500, math.sin(a0) * 1500); p.lineTo(math.cos(a0 + 0.13) * 1500, math.sin(a0 + 0.13) * 1500); p.close()
        c.drawPath(p, paint(col, 0.10))
    c.restore()
    r = r0 + 18 * math.sin(t * 1.3)
    c.drawCircle(cx + 12, cy + 12, r, paint(KINK, 0.9))
    c.drawCircle(cx, cy, r, paint(col))
    dots(c, (cx - r, cy - r, 2 * r, 2 * r), KINK, cell=18, rmax=3.4, grad=(0.2, 1.0), a=0.16)
    c.drawCircle(cx, cy, r, stroke(KINK, 9))


def drift(c, t, S):
    """slow camera push on every scene so nothing ever sits still."""
    s = 1.0 + 0.012 * (t - S['t0'])
    c.translate(540, 960); c.scale(s, s); c.translate(-540, -960)


def thermo(c, x, y, h, lvl, k, t):
    if k <= 0: return
    c.save(); c.translate(x, y + 8 * math.sin(t * 1.5)); sc = eback(cl(k), 1.4); c.scale(sc, sc)
    w = 70
    rr = skia.RRect.MakeRectXY(R.MakeXYWH(-w / 2, -h, w, h), w / 2, w / 2)
    c.drawRRect(rr, paint(KINK)); c.drawCircle(0, 30, 70, paint(KINK))
    rr2 = skia.RRect.MakeRectXY(R.MakeXYWH(-w / 2 + 10, -h + 10, w - 20, h - 10), 25, 25); c.drawRRect(rr2, paint(PAPER))
    fill = (h - 30) * cl(lvl)
    c.drawRect(R.MakeXYWH(-14, -fill, 28, fill + 10), paint(CRED)); c.drawCircle(0, 30, 56, paint(CRED))
    for i in range(6): c.drawLine(w / 2 - 6, -40 - i * (h - 60) / 6, w / 2 + 18, -40 - i * (h - 60) / 6, stroke(KINK, 5))
    c.restore()


def pin(c, x, y, lab, k, col=CRED):
    if k <= 0: return
    sc = eback(cl(k), 1.6)
    c.save(); c.translate(x, y); c.scale(sc, sc)
    p = skia.Path(); p.moveTo(0, 0); p.lineTo(-26, -50); p.lineTo(26, -50); p.close()
    c.drawCircle(4, -70, 34, paint(KINK)); c.drawPath(p, paint(KINK))
    c.drawCircle(0, -74, 34, paint(col)); c.drawCircle(0, -74, 34, stroke(KINK, 6)); c.drawCircle(0, -74, 12, paint(PAPER))
    c.restore()
    caption(c, lab, x - 10, y + 40, k, col=CYEL, size=22, rot=-2)


def sc_hook(c, t, S):
    ts = ph('so hot'); tc = ph('changing the weather'); to = ph('other side of the planet')
    drift(c, t, S)
    flow_bg(c, t, CBLU, r0=500)
    caption(c, 'RIGHT NOW . PACIFIC OCEAN', LX, 340, pr(t, 0.1, 0.3), col=CYEL, size=28)
    cut(c, 'E1_cut_comic.png', 540, 960, 760, pr(t, 0.0, 0.45), rot=-6, t=t, spin=-1.5)
    # heat glow spreading over the globe
    k = pr(t, 0.6, max(0.5, ts))
    if k > 0:
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial((430, 1000), 380 * eo(k), [argb(CRED, 0.75), argb(ORG, 0.4), argb(ORG, 0.0)], [0.0, 0.55, 1.0]))
        c.drawCircle(430, 1000, 380 * eo(k), g)
    thermo(c, 880, 1240, 360, pr(t, ts - 0.2, 1.2), pr(t, ts - 0.4, 0.4), t)
    if t > tc - 0.3: burst(c, 220, 560, 110, 'HOT!', pr(t, tc - 0.3, 0.35), size=54, col=CYEL, txt=CRED, rot=-8)
    if t > to - 0.3: caption(c, '...AND IT REACHES THE WHOLE PLANET', 150, 1370, pr(t, to - 0.3, 0.3), col=PAPER, size=28, rot=-1.5)
    credit(c, 'E1_globe', col=PAPER)


def sc_what(c, t, S):
    tc = ph('called el nino'); tw = ph('warm water builds up'); tsa = ph('near south america'); tsu = ph('super el nino'); t2 = ph('two degrees celsius'); tst = ph('strongest ever measured')
    drift(c, t, S)
    flow_bg(c, t, ORG, cy=1020, r0=480)
    caption(c, 'MEET EL NINO', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    title(c, 'EL NINO', 90, 540, 160, CRED, pr(t, S['t0'] - 0.2, 0.3))
    if t < tsu - 0.3:
        photo_panel(c, 'E2_sst', 110, 640, 860, 430, -1.5, pr(t, S['t0'] - 0.3, 0.35), t=t - S['t0'])
        if t > tw - 0.3:
            caption(c, 'WARM WATER PILES UP', 150, 1120, pr(t, tw - 0.3, 0.3), col=CYEL, size=30, rot=-1.5)
            for i in range(4):
                kk = pr(t, tw - 0.2 + 0.15 * i, 0.4)
                x0 = 200 + i * 150; c.drawLine(x0, 860, x0 + 110 * eo(kk), 860, stroke(KINK, 16)); c.drawLine(x0, 860, x0 + 110 * eo(kk), 860, stroke(PAPER, 8))
        if t > tsa - 0.2: pin(c, 860, 870, 'SOUTH AMERICA', pr(t, tsa - 0.2, 0.4))
        cut(c, 'E1_cut_comic.png', 830, 1230, 280, pr(t, S['t0'] + 0.3, 0.5), t=t, spin=-2)
        caption(c, 'SATELLITE MAP, 1997 EL NINO', 160, 1170 if t < tw - 0.3 else 1060, pr(t, S['t0'], 0.3), col=PAPER, size=22) if t < tw - 0.3 else None
        credit(c, 'E2_sst')
        return
    title(c, '= SUPER', 90, 690, 150, CBLU, pr(t, tsu - 0.35, 0.25), rot=-2)
    thermo(c, 300, 1250, 420, 0.3 + 0.7 * pr(t, t2 - 0.3, 1.0), pr(t, tsu - 0.35, 0.25), t)
    cut(c, 'E1_cut_comic.png', 760, 1000, 300, pr(t, tsu - 0.3, 0.3) * (1 - pr(t, t2 - 0.5, 0.3)), t=t, spin=-2)
    if t > t2 - 0.3: title(c, '+2 C', 520, 1010, 190, CRED, pr(t, t2 - 0.3, 0.4), rot=-3)
    if t > t2 + 0.3: caption(c, 'HOTTER THAN NORMAL', 540, 1080, pr(t, t2 + 0.3, 0.3), col=PAPER, size=28)
    if t > tst - 0.4:
        def dr(cc):
            cc.drawRect(R.MakeWH(520, 190), paint(CYEL))
            title(cc, 'STRONGEST EVER', 260, 80, 52, CRED, 1.0, 'c', shadow=3)
            cc.drawString('FOR THIS TIME OF YEAR (NOAA)', 30, 150, font(MONO, 26), paint(KINK))
        panel(c, 500, 1150, 520, 190, rot=2, k=pr(t, tst - 0.4, 0.45), draw=dr)


def sc_1997(c, t, S):
    t97 = ph('nineteen ninety seven'); tf = ph('floods hit peru'); tfi = ph('fires burned across'); tn = ph('the very next year'); th = ph('hottest ever recorded')
    drift(c, t, S)
    flow_bg(c, t, CRED, r0=500)
    caption(c, 'THE LAST TIME IT GOT THIS STRONG', LX, 340, pr(t, S['t0'], 0.3), col=CYEL, size=28)
    title(c, '1997', 540, 600, 230, CYEL, pr(t, S['t0'] - 0.2, 0.3), 'c', rot=-3)
    kE = pr(t, S['t0'] - 0.2, 0.35) * (1 - pr(t, ph('floods hit peru') - 0.4, 0.4))
    if kE > 0:
        photo_panel(c, 'E6_esa', 90, 760, 900, 320, -1.5, kE, t=t - S['t0'])
        caption(c, 'THE 1997 SUPER EL NINO, MAPPED FROM SPACE', 130, 1130, kE, col=PAPER, size=24)
        cut(c, 'E1_cut_comic.png', 820, 1260, 260, kE, t=t, spin=-2)
    cards = ((tf, 'E13_flood', 'FLOODS: PERU, CALIFORNIA', -6, 120), (tfi, 'E7_fire', 'FIRES: INDONESIA', 4, 400), (tn, 'E11_drycrack', '1998: HOTTEST YEAR YET', -3, 680))
    for i, (t0, key, lab, rot, y) in enumerate(cards):
        k = pr(t, t0 - 0.3, 0.45)
        if k <= 0: continue
        x = (130, 470, 250)[i]
        photo_panel(c, key, x, 650 + i * 230, 480, 300, rot, k, t=t - t0)
        caption(c, lab, x + 20, 650 + i * 230 + 330, k, col=PAPER, size=24, rot=rot * 0.3)
    if t > th - 0.2: burst(c, 850, 1250, 110, 'RECORD HEAT', pr(t, th - 0.2, 0.35), size=30, col=CYEL, txt=CRED, rot=8)
    cut(c, 'E8_cut_comic.png', 880, 520, 260, pr(t, tn, 0.5), t=t, spin=4)


def sc_storm(c, t, S):
    to = ph('just one hurricane'); tf = ph('fewest since'); tr = ph('rip storms apart')
    drift(c, t, S)
    flow_bg(c, t, CCYN, r0=500)
    caption(c, "AND IT'S ALREADY STARTED", LX, 340, pr(t, S['t0'], 0.3), col=CBLU, size=30)
    title(c, '2026 ATLANTIC:', 90, 540, 110, CBLU, pr(t, S['t0'] - 0.2, 0.3))
    title(c, '1 HURRICANE', 90, 690, 140, CRED, pr(t, to - 0.3, 0.4), rot=-2)
    kr = pr(t, tr - 0.1, 1.0)
    if kr <= 0:
        cut(c, 'E4_cut_comic.png', 540, 1050, 620, pr(t, S['t0'] - 0.25, 0.3), t=t, spin=-25, bob=6)
    else:
        # the storm gets torn into 4 pieces by the wind
        for i in range(4):
            a = i * math.pi / 2 + math.pi / 4
            c.save(); c.translate(540 + math.cos(a) * 260 * eo(kr), 1050 + math.sin(a) * 200 * eo(kr))
            c.clipRect(R.MakeXYWH(-310 if math.cos(a) < 0 else 0, -310 if math.sin(a) < 0 else 0, 310, 310))
            place(c, 'E4_cut_comic.png', 0, 0, 620, rot=-25 * t, a=1 - 0.6 * kr, shadow=False)
            c.restore()
        for i in range(5):
            y = 860 + i * 90; x0 = -200 + 1400 * ((t * 0.9 + i * 0.23) % 1.0)
            c.drawLine(x0, y, x0 + 260, y, stroke(PAPER, 10)); c.drawLine(x0 + 300, y, x0 + 360, y, stroke(PAPER, 10))
    if t > tf - 0.3: burst(c, 830, 820, 120, 'FEWEST SINCE 1925', pr(t, tf - 0.3, 0.35), size=26, col=CYEL, txt=CRED, rot=8)
    if t > tr - 0.3: caption(c, 'EL NINO WINDS SHRED THE STORMS', 180, 1360, pr(t, tr - 0.3, 0.3), col=PAPER, size=30, rot=-1.5)
    credit(c, 'E4_hurricane')


def sc_catch(c, t, S):
    ts = ph('american south'); ti = ph('weaker rains to india'); tf = ph('higher food prices'); tw = ph('world food programme'); t49 = ph('forty nine million'); th = ph('into hunger')
    drift(c, t, S)
    if t < tw - 0.3:
        flow_bg(c, t, CBLU, cy=1020, r0=480)
        caption(c, "HERE'S THE CATCH", LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
        title(c, 'ONE OCEAN.', 90, 540, 140, CBLU, pr(t, S['t0'] + 0.1, 0.4))
        title(c, 'WORLDWIDE.', 90, 690, 140, CRED, pr(t, S['t0'] + 0.4, 0.4), rot=-2)
        cut(c, 'E1_cut_comic.png', 540, 1040, 560, pr(t, S['t0'] + 0.2, 0.5), t=t, spin=-1.5)
        for i, (t0, key, lab, x, y, rot) in enumerate(((ts, 'E13_flood', 'US SOUTH: FLOODS', 140, 820, -5), (ti, 'E11_drycrack', 'INDIA & AUSTRALIA: LESS RAIN', 560, 900, 4), (tf, 'E9_rice', 'FOOD PRICES UP', 300, 1150, -3))):
            k = pr(t, t0 - 0.3, 0.45)
            if k <= 0: continue
            photo_panel(c, key, x, y, 380, 240, rot, k, t=t - t0)
            caption(c, lab, x + 10, y + 270, k, col=CYEL, size=22, rot=rot * 0.3)
        if t > tf: cut(c, 'E10_cut_comic.png', 880, 1300, 260, pr(t, tf, 0.5), t=t)
        return
    flow_bg(c, t, CRED, r0=520)
    caption(c, 'UN WORLD FOOD PROGRAMME', LX, 340, pr(t, tw - 0.3, 0.3), col=CYEL, size=30)
    if t < t49 - 0.3: title(c, 'UN WARNING:', 540, 640, 140, PAPER, pr(t, tw - 0.4, 0.3), 'c', rot=-2)
    cut(c, 'E10_cut_comic.png', 770, 1260, 220, pr(t, tw - 0.2, 0.4), t=t)
    title(c, '49 MILLION', 540, 640, 170, PAPER, pr(t, t49 - 0.3, 0.4), 'c', rot=-2)
    title(c, 'MORE PEOPLE', 540, 760, 100, CYEL, pr(t, t49 + 0.3, 0.4), 'c')
    photo_panel(c, 'E9_rice', 190, 840, 700, 380, 1.5, pr(t, tw - 0.4, 0.35), t=t - tw)
    if t > th - 0.3: caption(c, 'COULD FACE HUNGER BY END OF 2027', 200, 1290, pr(t, th - 0.3, 0.3), col=PAPER, size=30, rot=-1.5)
    credit(c, 'E9_rice', col=PAPER)


def sc_peak(c, t, S):
    tp = ph('expect it to peak'); tn = ph('next few weeks'); t27 = ph('twenty twenty seven could'); th = ph('hottest year ever measured')
    drift(c, t, S)
    flow_bg(c, t, ORG, r0=520)
    caption(c, 'WHAT COMES NEXT', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    title(c, 'PEAK:', 90, 540, 150, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'WEEKS AWAY', 90, 690, 140, CRED, pr(t, tn - 0.3, 0.4), rot=-2)
    k = pr(t, S['t0'] + 0.2, 0.5)
    cut(c, 'E8_cut_comic.png', 540, 1060, 420 + 220 * pr(t, t27, 2.0), k, t=t, spin=5)
    if t > t27 - 0.3:
        title(c, '2027:', 160, 1300, 120, PAPER, pr(t, t27 - 0.3, 0.4), rot=-3)
        title(c, 'HOTTEST YEAR?', 420, 1300, 90, CYEL, pr(t, th - 0.3, 0.4), rot=-3)
    credit(c, 'E8_sun')


def sc_ask(c, t, S):
    ty = ph('yes or no')
    drift(c, t, S)
    flow_bg(c, t, CRED, r0=480)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), col=CYEL, size=30)
    title(c, 'HOTTEST SUMMER', 80, 540, 110, PAPER, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'EVER. READY?', 80, 680, 130, CYEL, pr(t, S['t0'] + 0.4, 0.4), rot=-2)
    cut(c, 'E8_cut_comic.png', 540, 1000, 440, pr(t, S['t0'] + 0.2, 0.5), t=t, spin=5)
    thermo(c, 860, 1180, 360, 0.95, pr(t, S['t0'] + 0.5, 0.4), t)
    burst(c, 230, 1230, 100, 'YES', pr(t, ty - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 560, 1250, 100, 'NO', pr(t, ty + 0.2, 0.35), col=CBLU, txt=CYEL, size=60)
    cta = 'SUBSCRIBE FOR DAILY WHAT IFS' if PLAT == 'yt' else 'SEND THIS TO SOMEONE WHO HATES THE HEAT'
    caption(c, cta, 160, 1375, pr(t, ty + 0.6, 0.3), col=CYEL, size=28, rot=-1.5)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(k2), paint(CRED))


def with_subs(fn):
    def f(c, t, S):
        c.save(); fn(c, t, S); c.restore()
        if t < END + 0.2: subtitle(c, t, SUBS, y=SUBY)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='what', t0=ph('called el nino') - 0.45, fn=with_subs(sc_what), tin='zoom'),
    dict(k='y1997', t0=ph('so what can one') - 0.2, fn=with_subs(sc_1997), tin='whip'),
    dict(k='storm', t0=ph("and it's already started") - 0.2, fn=with_subs(sc_storm), tin='zoom'),
    dict(k='catch', t0=ph("but here's the catch") - 0.2, fn=with_subs(sc_catch), tin='whip'),
    dict(k='peak', t0=ph('scientists expect') - 0.2, fn=with_subs(sc_peak), tin='zoom'),
    dict(k='ask', t0=ph('so what if next summer') - 0.2, fn=with_subs(sc_ask), tin='whip'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('rip storms apart'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
