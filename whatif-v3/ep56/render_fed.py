"""NextBigNow ep 56 (vintage comic + editorial, small subtitles, v5 voice): What if the Fed starts hiking again?
Facts: Forbes (14 Nov 2026) - 10-yr Treasury 5.15%, up 35bp in a week; core CPI +0.3% Oct, 3rd straight above-forecast gain; oil cited;
Gov. Waller (10 Nov) opened door to a half-point move if inflation keeps accelerating. FOMC 28 Oct 2026 held at 3.75%-4.00%.
Volcker era: CPI inflation peaked ~14.8% (Mar 1980); fed funds ~20% (1980-81); 30-yr mortgage peaked 18.45% (Oct 1981, Freddie Mac);
builders mailed 2x4s in protest; unemployment 10.8% (late 1982); inflation ~3.2% in 1983.
Photos (Wikimedia Commons): see fed/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('FD_DIR', 'fed'))
PK.IMG = os.path.join(HERE, 'fed', 'img')
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



def up_chart(cc, w, h, k, pts, color=CRED, labels=()):
    down_chart(cc, w, h, k, pts, color, labels)


def sc_hook(c, t, S):
    t5 = ph('above five percent'); tq = ph('so what happens'); tn = ph('not cut them')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'WALL STREET . THIS WEEK', LX, 340, 1.0, col=CYEL, size=30)
        title(c, 'RATE HIKES', 80, 540, 150, CRED, 1.0, rot=-2)
        title(c, 'ARE BACK?', 90, 690, 140, CBLU, 1.0)
        photo_panel(c, 'E1_fed', 90, 770, 900, 560, 1.2, 1.0, fy=0.6, t=t)
        caption(c, 'THE FEDERAL RESERVE, WASHINGTON', 180, 1280, 1.0, col=CYEL, size=24)
        if t > tn - 0.2: burst(c, 230, 860, 105, 'NOT CUTS', pr(t, tn - 0.2, 0.35), size=34, col=CYEL, txt=CRED, rot=-8)
        if t > t5 - 0.2: burst(c, 830, 860, 125, '10-YR: 5%+', pr(t, t5, 0.35), size=36, rot=8)
        credit(c, 'E1_fed')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF THE FED', 80, 540, 116, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'STARTS HIKING', 90, 680, 120, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'AGAIN?', 90, 820, 150, PAPER, pr(t, tq + 0.45, 0.4))
    def dr(cc):
        cc.drawRect(R.MakeWH(800, 420), paint(PAPER))
        up_chart(cc, 800, 420, pr(t, tq + 0.6, 1.6), [(0, 3.9), (0.3, 3.9), (0.55, 3.9), (0.7, 4.4), (0.85, 4.9), (1.0, 5.4)], labels=((0.0, 'NOW'), (0.9, '???')))
        cc.drawString('FED RATE (ILLUSTRATIVE)', 520, 40, font('SpecialElite.ttf', 20), paint(KINK))
    panel(c, 140, 920, 800, 420, rot=-2, k=pr(t, tq + 0.5, 0.5), draw=dr)


def sc_now(c, t, S):
    tc = ph('core prices'); to = ph('oil is pushing'); tr = ph("fed's rate sits"); tg = ph('one fed governor'); th = ph('half point hike')
    paper(c, t)
    caption(c, "HERE'S WHAT'S GOING ON", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tr - 0.3:
        title(c, 'INFLATION', 90, 530, 150, CRED, pr(t, S['t0'] + 0.3, 0.4))
        title(c, "WON'T COOL.", 90, 680, 140, CBLU, pr(t, S['t0'] + 0.6, 0.4))
        mini(c, 90, 780, 430, 290, -2, pr(t, tc - 0.2, 0.4), 'CORE PRICES, OCTOBER', 'HOTTER', CRED, bigsize=70)
        mini(c, 560, 800, 430, 290, 1.5, pr(t, tc + 1.6, 0.4), 'ABOVE FORECAST', '3 IN A ROW', CBLU, bigsize=56)
        mini(c, 260, 1110, 560, 230, -1, pr(t, to - 0.2, 0.4), 'OIL', 'PUSHING COSTS UP', CYEL, txtc=CRED, bigsize=48)
        return
    title(c, 'FED RATE NOW:', 90, 540, 120, CBLU, pr(t, tr - 0.3, 0.4))
    title(c, '3.75-4%', 90, 720, 190, CRED, pr(t, tr + 0.3, 0.4), rot=-2)
    if t > tg - 0.2:
        caption(c, 'ONE FED GOVERNOR:', 120, 880, pr(t, tg - 0.2, 0.3), col=CYEL, size=32, rot=-2)
        caption(c, 'A BIG HALF-POINT HIKE?', 180, 990, pr(t, th - 0.3, 0.3), col=CRED, size=40, rot=1.5)
    if t > th: burst(c, 760, 1220, 130, '+0.5%?', pr(t, th + 0.2, 0.35), size=56, rot=8)


def sc_care(c, t, S):
    tl = ph('almost every loan'); tm = ph('mortgages car loans'); tcar = ph('car loans'); tcc = ph('credit cards'); tt = ph('when the ten year'); th = ph('a house you could'); thu = ph('hundreds more')
    paper(c, t)
    caption(c, 'WHY YOU SHOULD CARE', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tt - 0.3:
        title(c, 'EVERY LOAN', 90, 540, 150, CBLU, pr(t, tl - 0.2, 0.4))
        title(c, 'FOLLOWS.', 90, 690, 150, CRED, pr(t, tl + 0.4, 0.4))
        mini(c, 90, 790, 430, 260, -2, pr(t, tm - 0.2, 0.4), 'YOUR', 'MORTGAGE', CBLU, bigsize=60)
        mini(c, 560, 810, 430, 260, 1.5, pr(t, tcar - 0.1, 0.4), 'YOUR', 'CAR LOAN', CRED, bigsize=60)
        mini(c, 260, 1100, 560, 240, -1, pr(t, tcc - 0.1, 0.4), 'YOUR', 'CREDIT CARD', CYEL, txtc=CRED, bigsize=60)
        return
    title(c, '10-YR UP =', 90, 540, 140, CBLU, pr(t, tt - 0.3, 0.4))
    title(c, 'MORTGAGE UP.', 90, 690, 130, CRED, pr(t, tt + 0.5, 0.4), rot=-2)
    photo_panel(c, 'E3_framing', 90, 770, 900, 560, 1.2, pr(t, th - 0.4, 0.5), fy=0.45, t=t - th)
    if t > thu - 0.2: burst(c, 800, 830, 135, '+$100s A MONTH', pr(t, thu - 0.2, 0.35), size=30, rot=8)
    credit(c, 'E3_framing')


def sc_volcker(c, t, S):
    t80 = ph('in nineteen eighty'); t15 = ph('almost fifteen percent'); tv = ph('paul volcker'); t20 = ph('around twenty percent'); t18 = ph('above eighteen percent')
    tw = ph('pieces of wood'); tr = ph('deep recession'); tu = ph('almost eleven percent'); tit = ph('but it worked'); t83 = ph('around three percent')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN THE EXTREME VERSION", LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < tw - 0.4:
        title(c, '1980:', 90, 540, 150, CBLU, pr(t, t80 - 0.2, 0.4))
        title(c, 'PRICES ON FIRE.', 80, 690, 112, CRED, pr(t, t15 - 0.3, 0.4), rot=-2)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 560), paint(PAPER))
            bars(cc, 70, 120, 760, 320, [('INFLATION', 14.8, '~15%', CRED), ('FED RATE', 20, '~20%', CBLU), ('MORTGAGES', 18.45, '18%+', CYEL)], pr(t, t15, (t18 + 0.8) - t15), 23)
            cc.drawString('USA, 1980-81 (PEAKS, APPROX.)', 30, 540, font('SpecialElite.ttf', 22), paint(KINK))
        panel(c, 90, 770, 900, 560, rot=1.0, k=pr(t, t15, 0.5), draw=dr)
        if t > tv - 0.2: caption(c, 'FED CHAIR PAUL VOLCKER', 560, 800, pr(t, tv - 0.2, 0.3), col=CYEL, size=26, rot=3)
        return
    if t < tit - 0.3:
        title(c, 'BUILDERS MAILED', 80, 540, 104, CRED, pr(t, tw - 0.4, 0.4))
        title(c, 'HIM WOOD.', 90, 680, 140, CBLU, pr(t, tw, 0.4), rot=-2)
        photo_panel(c, 'E3_framing', 90, 760, 900, 380, 1.2, pr(t, tw - 0.2, 0.5), fy=0.5, zoom=1.4, t=t - tw)
        mini(c, 90, 1150, 430, 200, -2, pr(t, tr - 0.2, 0.4), 'THE ECONOMY', 'RECESSION', CRED, bigsize=48)
        mini(c, 560, 1160, 430, 200, 1.5, pr(t, tu - 0.3, 0.4), 'UNEMPLOYMENT', '~11%', CBLU, bigsize=70)
        credit(c, 'E3_framing')
        return
    title(c, 'BUT IT', 90, 540, 150, GRN, pr(t, tit - 0.3, 0.4))
    title(c, 'WORKED.', 90, 690, 150, GRN, pr(t, tit, 0.4), rot=-2)
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 520), paint(PAPER))
        bars(cc, 140, 110, 620, 300, [('1980', 14.8, '~15%', CRED), ('1983', 3.2, '~3%', GRN)], pr(t, tit + 0.3, 1.8), 17)
        cc.drawString('US INFLATION (APPROX.)', 30, 500, font('SpecialElite.ttf', 22), paint(KINK))
    panel(c, 90, 790, 900, 520, rot=1.0, k=pr(t, tit + 0.2, 0.5), draw=dr)


def sc_predict(c, t, S):
    tn = ph('nobody is going'); to = ph('once or twice'); td = ph('cheap money'); tm = ph('mortgages stay'); ts = ph('stocks get shaky'); tsv = ph('saving finally pays'); tv = ph('variable rate'); tf = ph('financial advice')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < tm - 0.3:
        title(c, 'NOT 20%.', 90, 540, 160, PAPER, pr(t, tn - 0.2, 0.4))
        title(c, 'NOT EVEN CLOSE.', 80, 690, 110, CYEL, pr(t, tn + 0.5, 0.4))
        caption(c, 'BUT 1 OR 2 HIKES...', 120, 860, pr(t, to - 0.3, 0.3), col=PAPER, size=34, rot=-2)
        if t > td - 0.3: burst(c, 640, 1100, 170, 'CHEAP MONEY: OVER', pr(t, td - 0.3, 0.35), size=32, col=CYEL, txt=CRED, rot=6)
        return
    title(c, 'WHAT', 90, 540, 150, PAPER, pr(t, tm - 0.3, 0.4))
    title(c, 'CHANGES:', 90, 690, 150, CYEL, pr(t, tm, 0.4))
    for i, (t0, s_, col) in enumerate(((tm, 'MORTGAGES STAY PAINFUL', PAPER), (ts, 'STOCKS GET SHAKY', CYEL), (tsv, 'SAVING FINALLY PAYS', CCYN))):
        caption(c, s_, 120 + (i % 2) * 60, 840 + i * 120, pr(t, t0 - 0.2, 0.3), col=col, size=34, rot=(-2, 1.5, -1)[i])
    if t > tv - 0.4: caption(c, 'VARIABLE-RATE DEBT? CHECK IT.', 140, 1220, pr(t, tv - 0.4, 0.3), col=CYEL, size=32, rot=-1)
    if t > tf - 0.6: caption(c, 'NOT FINANCIAL ADVICE', 330, 1330, pr(t, tf - 0.6, 0.3), col=PAPER, size=24)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'SHOULD THE FED', 80, 530, 112, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'RAISE RATES?', 90, 670, 130, CRED, pr(t, S['t0'] + 0.3, 0.4))
    photo_panel(c, 'E1_fed', 120, 740, 840, 420, -1.5, pr(t, S['t0'] + 0.3, 0.5), fy=0.6, t=t - S['t0'])
    burst(c, 260, 1260, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 820, 1260, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    credit(c, 'E1_fed')
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
    dict(k='now', t0=ph("here's what's going") - 0.2, fn=with_subs(sc_now), tin='whip'),
    dict(k='care', t0=ph('why should you care') - 0.2, fn=with_subs(sc_care), tin='zoom'),
    dict(k='volcker', t0=ph("we've seen the extreme") - 0.2, fn=with_subs(sc_volcker), tin='wipe', col=SEPIA),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('around twenty percent'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
