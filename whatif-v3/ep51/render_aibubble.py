"""NextBigNow ep 51 (vintage comic + editorial, small subtitles, v5 voice): What happens if the AI bubble pops?
Facts: AP (5 Nov 2026) - S&P 500 -4.4% (worst since Apr 2025 tariffs), Dow -1,833, Nasdaq -5.5%; AMD -17.3%, Nvidia -9.3%; trigger: fears
AI data-center building slows (higher borrowing costs; midterm results; voters wary of AI and higher power bills). 2025 deals: Nvidia
said it would invest up to $100B in OpenAI (Sep 2025), OpenAI buys Nvidia systems; AMD-OpenAI (Oct 2025): warrants for up to ~10% of AMD,
OpenAI buys AMD GPUs. Dot-com: Nasdaq peak 5,048 (10 Mar 2000) to 1,114 (Oct 2002) = -78%; Cisco most valuable company Mar 2000, fell ~86%;
Pets.com Super Bowl ad Jan 2000, shut Nov 2000; Amazon fell >90% (1999-2001). Not financial advice.
Photos (Wikimedia Commons): see aibubble/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('AB_DIR', 'aibubble'))
PK.IMG = os.path.join(HERE, 'aibubble', 'img')
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


def bubble_ai(c, x, y, r, k=1.0, pop=0.0, t=0.0, label='AI'):
    if k <= 0: return
    if pop > 0:
        for i in range(14):
            a = i / 14 * math.tau + 0.2; d0 = r * 0.8; d1 = r * (0.9 + 0.8 * eo(pop))
            c.drawLine(x + math.cos(a) * d0, y + math.sin(a) * d0, x + math.cos(a) * d1, y + math.sin(a) * d1, stroke(KINK, 10 * (1 - pop)))
        burst(c, x, y, r * 0.75, 'POP!', 1.0 - 0.0 * pop, col=CYEL, txt=CRED, size=r * 0.42, rot=-6)
        return
    s = eback(cl(k), 1.6) * (1 + 0.02 * math.sin(t * 3))
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(12, 12, r, paint(KINK))
    c.drawCircle(0, 0, r, paint(shader=skia.GradientShader.MakeRadial((-r * 0.3, -r * 0.35), r * 1.3, [argb((210, 245, 255)), argb((120, 190, 240)), argb((60, 120, 210))])))
    dots(c, (-r, -r, 2 * r, 2 * r), (40, 90, 180), cell=16, rmax=4, grad=(0.5, 1.0), a=0.5)
    c.drawCircle(0, 0, r, stroke(KINK, 9))
    p = skia.Path(); p.addArc(R.MakeXYWH(-r * 0.75, -r * 0.75, r * 1.5, r * 1.5), 200, 50)
    c.drawPath(p, stroke(PAPER, r * 0.09))
    c.restore()
    title(c, label, x, y + r * 0.2 * s, r * 0.62 * s, CRED, 1.0, 'c', shadow=6)


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


# ================================================================== scenes
def sc_hook(c, t, S):
    ta = ph('two letters'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'NOVEMBER 5, 2026', LX, 340, 1.0, col=CRED, size=30)
        title(c, 'TRILLIONS', 80, 540, 170, CRED, 1.0, rot=-2)
        title(c, 'GONE. IN 1 DAY.', 90, 680, 104, CBLU, 1.0)
        def dr(cc):
            cover(cc, img('B1_nyse_comic.png'), 0, 0, 900, 560, 1.1 + 0.01 * t, 0.5, 0.35)
            cc.drawRect(R.MakeWH(900, 560), paint(KINK, 0.25))
            k = pr(t, 0.2, 2.0)
            pts = [(0, 90), (0.2, 92), (0.35, 86), (0.5, 88), (0.65, 70), (0.8, 55), (1.0, 30)]
            p = skia.Path(); first = True
            for fx, v in pts:
                if fx > k: break
                X, Y = 60 + fx * 780, 560 - v * 5.2; (p.moveTo if first else p.lineTo)(X, Y); first = False
            cc.drawPath(p, stroke(KINK, 22)); cc.drawPath(p, stroke(CRED, 12))
        panel(c, 90, 760, 900, 560, rot=1.2, k=1.0, draw=dr)
        if t > ta - 0.2: burst(c, 820, 800, 120, 'A.I.', pr(t, ta, 0.35), size=60, rot=8)
        credit(c, 'B1_nyse')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF THE', 90, 540, 130, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'AI BUBBLE', 90, 690, 150, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'POPS?', 90, 840, 150, PAPER, pr(t, tq + 0.45, 0.4))
    pop = pr(t, ph('pops') + 0.5, 0.5) if t > ph('pops') + 0.5 else 0.0
    bubble_ai(c, 600, 1150, 220, pr(t, tq + 0.3, 0.6), pop=pop, t=t)


def sc_what(c, t, S):
    ts = ph('the s and p') if False else S['t0'] + 0.6; tn = ph('nasdaq fell'); ta = ph('amd dropped'); tv = ph('nvidia the king'); tw = ph('investors got scared'); tb = ph('borrowing got'); tp = ph('power bills')
    paper(c, t)
    caption(c, "HERE'S WHAT HAPPENED", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tw - 0.3:
        title(c, 'RED EVERYWHERE.', 90, 520, 116, CRED, pr(t, S['t0'] + 0.3, 0.4))
        mini(c, 90, 600, 430, 300, -2, pr(t, ts, 0.4), 'S&P 500', '-4.4%', CRED)
        mini(c, 560, 615, 430, 300, 1.5, pr(t, tn - 0.2, 0.4), 'NASDAQ', '-5.5%', CBLU)
        mini(c, 90, 950, 430, 300, 1.2, pr(t, ta - 0.2, 0.4), 'AMD', '-17%', CYEL, txtc=CRED)
        mini(c, 560, 965, 430, 300, -1.5, pr(t, tv - 0.2, 0.4), 'NVIDIA', '-9%', CRED)
        return
    title(c, 'WHY THE PANIC?', 90, 520, 116, CBLU, pr(t, tw - 0.3, 0.4))
    photo_panel(c, 'B6_chip', 90, 610, 900, 520, 1.2, pr(t, tw - 0.1, 0.5), t=t - tw)
    caption(c, 'AI DATA CENTERS COULD SLOW', 130, 650, pr(t, ph('could slow') - 0.2, 0.3), col=CYEL, size=30, rot=-2)
    caption(c, 'BORROWING GOT EXPENSIVE', 230, 1150, pr(t, tb - 0.2, 0.3), col=PAPER, size=30, rot=1.5)
    caption(c, 'VOTERS ANGRY ABOUT POWER BILLS', 120, 1270, pr(t, tp - 0.4, 0.3), col=CCYN, size=28, rot=-1)
    credit(c, 'B6_chip')


def node(c, x, y, s, k, col, txtc=PAPER):
    if k <= 0: return
    sc = eback(cl(k), 2)
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-140 + 8, -60 + 8, 280, 120), 20, 20), paint(KINK))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-140, -60, 280, 120), 20, 20), paint(col))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-140, -60, 280, 120), 20, 20), stroke(KINK, 6))
    c.restore()
    title(c, s, x, y + 22 * sc, 56 * sc, txtc, 1.0, 'c', shadow=4)


def arc_arrow(c, x0, y0, x1, y1, bend, k, col, t, lab=None, labk=0):
    if k <= 0: return
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny); nx, ny = nx / L * bend, ny / L * bend
    p = skia.Path(); p.moveTo(x0, y0); p.quadTo(mx + nx, my + ny, x1, y1)
    meas = skia.PathMeasure(p, False); Lp = meas.getLength()
    seg = skia.Path(); meas.getSegment(0, Lp * eo(cl(k)), seg, True)
    c.drawPath(seg, stroke(KINK, 16)); c.drawPath(seg, stroke(col, 9))
    for j in range(4):
        d = ((t * 0.5 + j / 4) % 1) * Lp * eo(cl(k))
        pos = meas.getPosTan(d)[0]
        c.drawCircle(pos.x(), pos.y(), 11, paint(CYEL)); c.drawCircle(pos.x(), pos.y(), 11, stroke(KINK, 4))
    if k >= 1:
        pos, tan = meas.getPosTan(Lp)
        a = math.atan2(tan.y(), tan.x())
        c.save(); c.translate(pos.x(), pos.y()); c.rotate(math.degrees(a))
        c.drawPath(poly([(0, 0), (-34, -20), (-34, 20)], True), paint(col)); c.drawPath(poly([(0, 0), (-34, -20), (-34, 20)], True), stroke(KINK, 5))
        c.restore()
    if lab and labk > 0:
        caption(c, lab, mx + nx * 0.6 - 150, my + ny * 0.6 - 34, labk, col=PAPER, size=30, rot=0)


def sc_circle(c, t, S):
    tn = ph('nvidia said it would'); to = ph('and openai buys nvidia'); ta = ph('amd gave openai'); tb = ph('and openai buys amd'); tc = ph('around in a circle')
    paper(c, t)
    caption(c, 'WHY PEOPLE SAY "BUBBLE"', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'FOLLOW THE MONEY.', 90, 520, 92, CRED, pr(t, S['t0'] + 0.3, 0.4))
    arc_arrow(c, 380, 760, 700, 930, 90, pr(t, tn, 0.6), (80, 200, 120), t, '$100B INVEST', pr(t, ph('hundred billion') - 0.1, 0.3))
    arc_arrow(c, 700, 1010, 380, 820, 60, pr(t, to, 0.6), CBLU, t, 'BUYS CHIPS', pr(t, to + 0.3, 0.3))
    arc_arrow(c, 380, 1210, 700, 1040, -80, pr(t, ta + 0.2, 0.6), (80, 200, 120), t, 'UP TO 10% STAKE', pr(t, ph('ten percent') - 0.1, 0.3))
    arc_arrow(c, 720, 1060, 380, 1260, -40, pr(t, tb, 0.6), CBLU, t, 'BUYS CHIPS', pr(t, tb + 0.3, 0.3))
    for (x, y, s, kk, col, tc_) in ((280, 720, 'NVIDIA', pr(t, tn - 0.3, 0.35), CYEL, CRED), (800, 980, 'OPENAI', pr(t, tn + 0.3, 0.35), PAPER, KINK), (280, 1240, 'AMD', pr(t, ta - 0.3, 0.35), CRED, PAPER)):
        node(c, x, y, s, kk, col, tc_)
    if t > tc - 0.3: burst(c, 820, 1300, 110, 'LOOP?!', pr(t, tc - 0.3, 0.35), size=44, rot=8)


def sc_dotcom(c, t, S):
    tci = ph('cisco the company'); tp = ph('the bubble popped'); tn = ph('nasdaq lost'); tcl = ph('cisco lost'); tpe = ph('and pets')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN THIS MOVIE...", LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < tp - 0.3:
        title(c, 'MARCH 2000', 90, 540, 150, CRED, pr(t, S['t0'] + 0.3, 0.4), rot=-2)
        photo_panel(c, 'B2_wall2000', 90, 630, 900, 600, -1.2, pr(t, S['t0'] + 0.5, 0.5), fx=0.45, fy=0.4, t=t - S['t0'])
        if t > tci - 0.2: caption(c, 'CISCO: MOST VALUABLE COMPANY ON EARTH', 110, 1180, pr(t, tci, 0.3), col=CYEL, size=26)
        caption(c, '"THE INTERNET IS THE FUTURE!"', 300, 680, pr(t, ph('internet was the future') - 0.2, 0.3), col=PAPER, size=28, rot=3)
        credit(c, 'B2_wall2000')
        return
    title(c, 'POP.', 90, 540, 170, CRED, pr(t, tp - 0.3, 0.4), rot=-3)
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 480), paint(PAPER))
        down_chart(cc, 900, 480, pr(t, tp, 2.0), [(0, 5048), (0.08, 4200), (0.2, 3700), (0.35, 2400), (0.5, 2000), (0.65, 1800), (0.8, 1300), (1.0, 1114)], labels=((0.0, 'MAR 2000'), (1.0, 'OCT 2002')))
        cc.drawString('NASDAQ', 70, 40, font('SpecialElite.ttf', 26), paint(KINK))
    panel(c, 90, 620, 900, 480, rot=1.0, k=pr(t, tp - 0.1, 0.5), draw=dr)
    if t > tn - 0.2: burst(c, 820, 650, 120, '-78%', pr(t, ph('seventy eight') - 0.2, 0.35), size=56, rot=8)
    mini(c, 90, 1150, 410, 230, -2, pr(t, tcl - 0.2, 0.4), 'CISCO', '-86%', CBLU, bigsize=50)
    mini(c, 560, 1160, 430, 230, 1.5, pr(t, tpe - 0.2, 0.4), 'PETS.COM', 'GONE IN <1 YR', CRED, bigsize=40)


def sc_twist(c, t, S):
    ta = ph("amazon's stock"); tb = ph('one of the biggest'); tw = ph('the technology won')
    paper(c, t)
    caption(c, 'BUT HERE IS THE PART PEOPLE FORGET', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=26)
    title(c, "THE INTERNET", 90, 530, 128, CBLU, pr(t, S['t0'] + 0.4, 0.4))
    title(c, "DIDN'T DIE.", 90, 670, 140, CRED, pr(t, S['t0'] + 0.7, 0.4))
    mini(c, 90, 760, 430, 380, -2, pr(t, ta - 0.2, 0.4), 'AMAZON, 1999-2001', '-90%+', CRED, bigsize=70)
    mini(c, 560, 780, 430, 380, 1.5, pr(t, tb - 0.2, 0.4), 'LATER', 'GIANT', (80, 200, 120), bigsize=70)
    if t > tw - 0.4: burst(c, 540, 1270, 150, 'TECH WON', pr(t, tw - 0.4, 0.35), col=CYEL, txt=CRED, size=50, rot=-4)


def sc_predict(c, t, S):
    tn = ph('not every company'); tm = ph('money gets tighter'); tbo = ph('borrowing billions'); tpr = ph('prices fall'); tw = ph('a few winners'); tf = ph("isn't financial advice")
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    title(c, 'AI IS REAL.', 90, 540, 150, CYEL, pr(t, S['t0'] + 0.3, 0.4))
    title(c, 'NOT ALL WILL LIVE.', 90, 680, 96, PAPER, pr(t, tn - 0.2, 0.4))
    caption(c, 'DEBT-FUNDED DATA CENTERS HIT FIRST', 110, 830, pr(t, tbo - 0.3, 0.3), col=CYEL, size=30, rot=-2)
    caption(c, 'PRICES FALL. SOME NAMES DISAPPEAR.', 140, 970, pr(t, tpr - 0.2, 0.3), col=PAPER, size=30, rot=1.5)
    caption(c, 'A FEW WINNERS GET WAY BIGGER', 120, 1110, pr(t, tw - 0.2, 0.3), col=CCYN, size=30, rot=-1)
    if t > tf - 0.4: caption(c, 'NOT FINANCIAL ADVICE', 330, 1260, pr(t, tf - 0.4, 0.3), col=PAPER, size=26)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'IS AI A', 90, 530, 140, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'BUBBLE?', 90, 680, 160, CRED, pr(t, S['t0'] + 0.3, 0.4))
    bubble_ai(c, 540, 1000, 200, pr(t, S['t0'] + 0.4, 0.6), t=t)
    burst(c, 260, 1260, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=(80, 210, 120), txt=PAPER, size=56)
    burst(c, 820, 1260, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(k2), paint(CRED))


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='what', t0=ph("here's what happened") - 0.2, fn=with_subs(sc_what), tin='whip'),
    dict(k='circle', t0=ph("and here's why people") - 0.2, fn=with_subs(sc_circle), tin='zoom'),
    dict(k='dotcom', t0=ph("we've seen this movie") - 0.2, fn=with_subs(sc_dotcom), tin='wipe', col=SEPIA),
    dict(k='twist', t0=ph("but here's the part") - 0.2, fn=with_subs(sc_twist), tin='whip'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('single day'), 10, 0.3)
EP.shk(ph('the bubble popped'), 12, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
