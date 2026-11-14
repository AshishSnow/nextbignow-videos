"""NextBigNow ep 54 (vintage comic + editorial, small subtitles, v5 voice): What if bird flu starts spreading between people?
Facts: ContagionLive (2 Nov 2026) - Yakima County WA adult died 1 Nov 2026 of avian flu after exposure to infected dairy cattle; first US death of
2026, 3rd US death overall; CDC: 71 human H5 cases since 2024 (41 dairy, 24 poultry, 3 other animals, 3 unknown); cattle detections in 19 states;
no evidence of human-to-human spread; local health officer: risk to public remains low. USDA: >150M US birds affected since 2022.
BLS: US average Grade A large eggs hit a record ~$6.23/dozen (Mar 2025). 2009 H1N1: identified Apr 2009 (Mexico/US); WHO pandemic declared
11 Jun 2009; CDC est. ~60.8M US cases Apr 2009-Apr 2010; vaccine available from Oct 2009. H5 vaccine candidates exist; some countries stockpiled.
Photos (Wikimedia Commons, public domain / CC0): see flu/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('FL_DIR', 'flu'))
PK.IMG = os.path.join(HERE, 'flu', 'img')
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



def timeline(c, x, y, w, k, t, pts):
    """horizontal ink timeline; pts = [(frac, top, bottom, col, t0)]"""
    c.drawLine(x, y, x + w * eo(k), y, stroke(KINK, 10))
    for fx, top, bot, col, t0 in pts:
        kk = pr(t, t0 - 0.2, 0.35)
        if kk <= 0: continue
        px = x + fx * w
        c.drawCircle(px, y, 26 * eback(kk, 1.6), paint(KINK)); c.drawCircle(px, y, 18 * eback(kk, 1.6), paint(col))
        title(c, top, px, y - 50, 56, col, kk, 'c', shadow=4)
        tw_ = width(bot, 'SpecialElite.ttf', 26)
        c.drawString(bot, px - tw_ / 2, y + 70, font('SpecialElite.ttf', 26), paint(KINK, kk))


def sc_hook(c, t, S):
    tc = ph('infected dairy cows'); t3 = ph('three americans'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'WASHINGTON STATE . NOV 1, 2026', LX, 340, 1.0, col=CYEL, size=30)
        title(c, 'BIRD FLU...', 80, 540, 150, CRED, 1.0, rot=-2)
        title(c, 'FROM A COW?', 90, 690, 130, CBLU, pr(t, tc - 0.3, 0.4))
        photo_panel(c, 'F2_cows', 90, 770, 900, 560, 1.2, 1.0, fy=0.6, t=t)
        if t > t3 - 0.2: burst(c, 820, 820, 125, '3 US DEATHS', pr(t, t3 - 0.2, 0.35), size=34, rot=8)
        credit(c, 'F2_cows')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF IT', 90, 540, 140, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'SPREADS PERSON', 90, 680, 110, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'TO PERSON?', 90, 810, 130, PAPER, pr(t, tq + 0.45, 0.4))
    photo_panel(c, 'F1_virus', 140, 900, 800, 440, -2, pr(t, tq + 0.5, 0.5), t=t - tq)
    caption(c, 'H5N1 BIRD FLU, UNDER A MICROSCOPE', 200, 1300, pr(t, tq + 0.9, 0.3), col=CYEL, size=24)
    credit(c, 'F1_virus', col=PAPER)


def sc_now(c, t, S):
    tn = ph('does not spread'); t70 = ph('about seventy americans'); tl = ph('risk to the public'); te = ph('the virus is everywhere')
    t19 = ph('nineteen states'); t150 = ph('hundred and fifty million'); teg = ph('remember when eggs')
    paper(c, t)
    if t < te - 0.3:
        caption(c, 'FIRST, THE GOOD NEWS', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
        title(c, 'NOT PERSON', 90, 530, 140, GRN, pr(t, tn - 0.3, 0.4))
        title(c, 'TO PERSON.', 90, 680, 140, CBLU, pr(t, tn, 0.4))
        mini(c, 90, 780, 430, 290, -2, pr(t, t70 - 0.2, 0.4), 'US CASES SINCE 2024', '~70', CBLU, bigsize=90)
        mini(c, 560, 800, 430, 290, 1.5, pr(t, t70 + 2.0, 0.4), 'HOW THEY CAUGHT IT', 'SICK ANIMALS', CYEL, txtc=CRED, bigsize=44)
        mini(c, 260, 1110, 560, 230, -1, pr(t, tl - 0.2, 0.4), 'RISK TO THE PUBLIC', 'LOW', GRN, bigsize=80)
        return
    caption(c, 'BUT...', LX, 340, pr(t, te - 0.3, 0.3), col=CRED, size=30)
    if t < teg - 0.3:
        title(c, "IT'S", 90, 530, 140, CRED, pr(t, te - 0.3, 0.4))
        title(c, 'EVERYWHERE.', 90, 680, 140, CRED, pr(t, te, 0.4), rot=-2)
        mini(c, 90, 780, 430, 290, -2, pr(t, t19 - 0.6, 0.4), 'FOUND IN DAIRY COWS IN', '19 STATES', CBLU, bigsize=60)
        mini(c, 560, 800, 430, 290, 1.5, pr(t, t150 - 0.4, 0.4), 'US BIRDS LOST SINCE 2022', '150M+', CRED, bigsize=84)
        photo_panel(c, 'F4_hens', 260, 1110, 560, 250, -1, pr(t, t150, 0.5), fy=0.6, t=t - t150)
        credit(c, 'F4_hens')
        return
    title(c, 'REMEMBER', 90, 530, 140, CBLU, pr(t, teg - 0.3, 0.4))
    title(c, '$6 EGGS?', 90, 680, 150, CRED, pr(t, teg + 0.2, 0.4), rot=-2)
    photo_panel(c, 'F3_eggs', 90, 770, 900, 560, 1.2, pr(t, teg, 0.5), t=t - teg)
    if t > ph("that's why") - 0.2: burst(c, 820, 820, 120, "THAT'S WHY", pr(t, ph("that's why") - 0.2, 0.35), size=36, rot=8)
    credit(c, 'F3_eggs')


def sc_why(c, t, S):
    tm = ph('infects a mammal'); tch = ph('another chance to change'); tf = ph('a few small changes'); tj = ph('jumping from person')
    paper(c, t)
    caption(c, 'WHY SCIENTISTS ARE NERVOUS', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'EVERY', 90, 530, 140, CBLU, pr(t, S['t0'] + 0.3, 0.4))
    title(c, 'INFECTION', 90, 680, 140, CRED, pr(t, S['t0'] + 0.6, 0.4))
    title(c, '= A NEW CHANCE', 90, 820, 100, CBLU, pr(t, tch - 0.2, 0.4))
    photo_panel(c, 'F1_virus', 90, 880, 900, 460, 1.2, pr(t, tm - 0.4, 0.5), zoom=1.4, t=t - tm)
    if t > tf - 0.2: caption(c, 'A FEW SMALL CHANGES...', 140, 1000, pr(t, tf - 0.2, 0.3), col=CYEL, size=34, rot=-3)
    if t > tj - 0.2: burst(c, 760, 1220, 130, 'PERSON TO PERSON?', pr(t, tj - 0.2, 0.35), size=30, rot=6)
    credit(c, 'F1_virus')


def sc_2009(c, t, S):
    ta = ph('in april two thousand'); tw = ph('within two months'); t60 = ph('sixty million'); tv = ph('the vaccine'); to = ph('until october'); ts = ph('six months after')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN THIS BEFORE", LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, '2009:', 90, 540, 150, CBLU, pr(t, S['t0'] + 0.2, 0.4))
    title(c, 'SWINE FLU.', 90, 690, 140, CRED, pr(t, ta + 0.6, 0.4), rot=-2)
    timeline(c, 170, 900, 700, pr(t, ta, 0.8), t, [(0.0, 'APR', 'NEW VIRUS', CBLU, ta + 0.4), (0.4, 'JUN', 'PANDEMIC', CRED, tw), (1.0, 'OCT', 'VACCINE', GRN, to)])
    if t > t60 - 0.3 and t < tv - 0.2:
        mini(c, 260, 1060, 560, 260, -1.5, pr(t, t60 - 0.3, 0.4), 'AMERICANS SICK, FIRST YEAR (CDC EST.)', '~60 MILLION', CRED, bigsize=60)
    if t > tv - 0.2:
        caption(c, 'VACCINE: 6 MONTHS LATE', 220, 1120, pr(t, tv - 0.2, 0.3), col=CYEL, size=36, rot=-2)
        if t > ts - 0.2: burst(c, 780, 1240, 110, '6 MONTHS', pr(t, ts - 0.2, 0.35), size=36, rot=8)


def sc_diff(c, t, S):
    tw = ph('we are watching early'); tv = ph('bird flu vaccines'); ts = ph('stockpiling doses')
    paper(c, t)
    caption(c, 'BUT THIS TIME...', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    title(c, "WE'RE", 90, 530, 140, CBLU, pr(t, tw - 0.3, 0.4))
    title(c, 'WATCHING EARLY.', 90, 680, 102, GRN, pr(t, tw, 0.4))
    mini(c, 90, 780, 430, 290, -2, pr(t, tv - 0.2, 0.4), 'BIRD FLU VACCINES', 'READY TO SCALE', GRN, bigsize=44)
    mini(c, 560, 800, 430, 290, 1.5, pr(t, ts - 0.4, 0.4), 'SOME COUNTRIES', 'STOCKPILING', CBLU, bigsize=50)


def sc_predict(c, t, S):
    tn = ph('not the next pandemic'); tl = ph('the longer it spreads'); tw = ph('the winners'); tt = ph('test fast'); tva = ph('vaccinate fast'); tm = ph('medical advice'); tr = ph('raw milk')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < tw - 0.3:
        title(c, 'NOT', 90, 540, 150, PAPER, pr(t, tn - 0.3, 0.4))
        title(c, 'TOMORROW.', 90, 690, 150, CYEL, pr(t, tn, 0.4))
        caption(c, 'MORE COWS INFECTED = MORE CHANCES', 110, 860, pr(t, tl - 0.2, 0.3), col=PAPER, size=30, rot=-2)
        photo_panel(c, 'F2_cows', 140, 960, 800, 380, 1.5, pr(t, tl, 0.5), fy=0.6, t=t - tl)
        return
    title(c, 'TEST FAST.', 90, 560, 150, PAPER, pr(t, tt - 0.3, 0.4))
    title(c, 'VACCINATE', 90, 710, 150, CYEL, pr(t, tva - 0.3, 0.4))
    title(c, 'FAST.', 90, 850, 150, CYEL, pr(t, tva, 0.4))
    if t > tm - 0.4: caption(c, 'NOT MEDICAL ADVICE', 140, 1000, pr(t, tm - 0.4, 0.3), col=PAPER, size=28, rot=-2)
    if t > tr - 0.4: burst(c, 700, 1200, 140, 'SKIP RAW MILK', pr(t, tr - 0.4, 0.35), col=CYEL, txt=CRED, size=32, rot=6)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'DID YOU KNOW', 90, 530, 120, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, "IT'S IN COWS?", 90, 670, 120, CRED, pr(t, S['t0'] + 0.3, 0.4))
    photo_panel(c, 'F2_cows', 120, 740, 840, 420, -1.5, pr(t, S['t0'] + 0.3, 0.5), fy=0.6, t=t - S['t0'])
    burst(c, 260, 1260, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 820, 1260, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    credit(c, 'F2_cows')
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
    dict(k='now', t0=ph('first the good news') - 0.2, fn=with_subs(sc_now), tin='whip'),
    dict(k='why', t0=ph('so why are scientists') - 0.2, fn=with_subs(sc_why), tin='zoom'),
    dict(k='y2009', t0=ph("we've seen a brand") - 0.2, fn=with_subs(sc_2009), tin='wipe', col=SEPIA),
    dict(k='diff', t0=ph('but this time') - 0.2, fn=with_subs(sc_diff), tin='whip'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('within two months'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
