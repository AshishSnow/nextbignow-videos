"""NextBigNow ep 57 (vintage comic + editorial, small subtitles, v5 voice): What happens when a company loses its legend?
Facts: Nvidia 8-K (12 Nov 2026) - Jensen Huang resigned as President, CEO and director effective immediately; no reason given; CFO Colette
Kress interim CEO (remains CFO); Harvey C. Jones first board chair. Al Jazeera (12 Nov 2026) - board launched independent investigation;
shares fell more than 14% at one point; Huang co-founded Nvidia 1993, CEO 33 years; Kress CFO since Sept 2013, revenue $4.13B (FY2014) ->
$215.9B (FY2026). InformationWeek: Q3 FY2027 results on 17 Nov. Apple: Jobs resigned as CEO 24 Aug 2011; Tim Cook CEO; Apple first US
public company to hit $1T market value, 2 Aug 2018. Scandal details deliberately not described (allegations about third parties).
Photos (Wikimedia Commons): see ceo/img/credits.json. No people pictured."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('CE_DIR', 'ceo'))
PK.IMG = os.path.join(HERE, 'ceo', 'img')
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



def sc_hook(c, t, S):
    tw = ph('walked out the door'); te = ph('effective immediately'); t33 = ph('thirty three years'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'NVIDIA . NOVEMBER 12, 2026', LX, 340, 1.0, col=CYEL, size=30)
        title(c, 'THE CEO', 80, 540, 160, CBLU, 1.0, rot=-2)
        title(c, 'CHAIR IS EMPTY.', 80, 690, 110, CRED, pr(t, tw - 0.3, 0.4))
        k = pr(t, 0.0, 0.6)
        place(c, 'N2_chair_comic.png', 540, 1070 + 6 * math.sin(t * 2), 430 * eback(cl(k), 1.4), rot=-3 + 2 * math.sin(t), a=k, shadow=True)
        if t > te - 0.2: caption(c, 'EFFECTIVE IMMEDIATELY', 560, 820, pr(t, te - 0.2, 0.3), col=PAPER, size=26, rot=4)
        if t > t33 - 0.2: burst(c, 230, 1220, 115, '33 YEARS', pr(t, t33 - 0.2, 0.35), size=44, rot=-8)
        credit(c, 'N2_chairs')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT HAPPENS', 90, 540, 130, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'WHEN THE LEGEND', 80, 680, 110, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'LEAVES?', 90, 820, 150, PAPER, pr(t, tq + 0.45, 0.4))
    kk = pr(t, tq + 0.5, 0.5)
    place(c, 'N2_chair_comic.png', 540, 1150, 360 * eback(cl(kk), 1.5), rot=8 * math.sin(t * 1.5), a=kk, shadow=False)


def sc_know(c, t, S):
    tr = ph('resigned as'); tb = ph('left its board'); tn = ph("didn't give a reason"); ts = ph('personal scandal'); ti = ph('independent investigation'); t14 = ph('fourteen percent')
    paper(c, t)
    caption(c, "HERE'S WHAT WE KNOW", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < t14 - 1.2:
        title(c, 'RESIGNED.', 90, 540, 160, CRED, pr(t, tr - 0.2, 0.4), rot=-2)
        title(c, 'NO REASON GIVEN.', 80, 680, 106, CBLU, pr(t, tn - 0.2, 0.4))
        mini(c, 90, 770, 430, 260, -2, pr(t, tr + 0.4, 0.4), 'JENSEN HUANG', 'OUT AS CEO', CRED, bigsize=54)
        mini(c, 560, 790, 430, 260, 1.5, pr(t, tb - 0.2, 0.4), 'ALSO LEFT', 'THE BOARD', CBLU, bigsize=60)
        mini(c, 200, 1080, 680, 250, -1, pr(t, ti - 0.4, 0.4), 'THE BOARD LAUNCHED AN', 'INVESTIGATION', CYEL, txtc=CRED, bigsize=60)
        return
    title(c, 'THE STOCK:', 90, 540, 150, CBLU, pr(t, t14 - 1.2, 0.4))
    title(c, '-14%', 90, 730, 210, CRED, pr(t, t14 - 0.3, 0.4), rot=-3)
    photo_panel(c, 'N3_tickers', 90, 790, 900, 540, 1.2, pr(t, t14 - 0.9, 0.5), t=t - t14)
    burst(c, 820, 840, 120, 'IN ONE DAY', pr(t, t14 + 0.6, 0.35), size=38, rot=8)
    credit(c, 'N3_tickers')


def sc_why(c, t, S):
    tc = ph('makes the chips'); t93 = ph('nineteen ninety three'); tw = ph('he was nvidia'); tk = ph('colette kress'); tr = ph('yearly revenue'); t4 = ph('four billion'); t200 = ph('two hundred billion')
    paper(c, t)
    caption(c, 'WHY THIS IS HUGE', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tk - 0.3:
        title(c, 'THE CHIPS', 90, 540, 150, CBLU, pr(t, tc - 0.2, 0.4))
        title(c, 'BEHIND AI.', 90, 690, 150, CRED, pr(t, tc + 0.4, 0.4), rot=-2)
        photo_panel(c, 'N4_servers', 90, 770, 900, 520, 1.2, pr(t, tc, 0.5), t=t - tc)
        if t > t93 - 0.2: burst(c, 260, 850, 110, 'SINCE 1993', pr(t, t93 - 0.2, 0.35), size=36, col=CYEL, txt=CRED, rot=-8)
        if t > tw - 0.3: caption(c, '"HE WAS NVIDIA."', 520, 1250, pr(t, tw - 0.3, 0.3), col=CYEL, size=36, rot=-2)
        credit(c, 'N4_servers')
        return
    title(c, 'NEW BOSS:', 90, 540, 150, CBLU, pr(t, tk - 0.3, 0.4))
    title(c, 'THE MONEY CHIEF.', 80, 680, 104, CRED, pr(t, tk + 0.4, 0.4), rot=-2)
    caption(c, 'COLETTE KRESS . CFO SINCE 2013 . NOW INTERIM CEO', 100, 770, pr(t, tk, 0.3), col=CYEL, size=22, rot=-1)
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 520), paint(PAPER))
        bars(cc, 140, 110, 620, 300, [('FY2014', 4.13, '$4B', CCYN), ('FY2026', 215.9, '$216B', GRN)], pr(t, t4 - 0.3, (t200 + 0.6) - (t4 - 0.3)), 240)
        cc.drawString('NVIDIA YEARLY REVENUE', 30, 500, font('SpecialElite.ttf', 22), paint(KINK))
    panel(c, 90, 830, 900, 520, rot=1.0, k=pr(t, tr - 0.4, 0.5), draw=dr)


def sc_apple(c, t, S):
    ta = ph('in august twenty eleven'); tf = ph('apple was finished'); tc = ph('tim cook'); t7 = ph('seven years later'); tt = ph('trillion dollars'); tl = ph('the lesson')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN THIS BEFORE", LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < t7 - 0.3:
        title(c, 'AUG 2011:', 90, 540, 150, CBLU, pr(t, ta - 0.2, 0.4))
        title(c, 'JOBS STEPS DOWN.', 80, 690, 104, CRED, pr(t, ta + 0.6, 0.4), rot=-2)
        if t > tf - 0.3: caption(c, '"APPLE IS FINISHED."', 140, 840, pr(t, tf - 0.3, 0.3), col=PAPER, size=40, rot=-3)
        if t > tc - 0.2: mini(c, 260, 950, 560, 300, -1, pr(t, tc - 0.2, 0.4), 'NEW CEO', 'TIM COOK', CBLU, bigsize=80)
        return
    if t < tl - 0.3:
        title(c, '7 YEARS LATER:', 80, 540, 120, CBLU, pr(t, t7 - 0.3, 0.4))
        title(c, '$1 TRILLION.', 80, 690, 130, GRN, pr(t, tt - 0.3, 0.4), rot=-2)
        photo_panel(c, 'N1_applepark', 90, 770, 900, 540, 1.2, pr(t, t7, 0.5), t=t - t7)
        burst(c, 820, 830, 120, 'FIRST IN THE US', pr(t, tt + 0.3, 0.35), size=30, rot=8)
        caption(c, 'APPLE PARK, CUPERTINO', 200, 1260, pr(t, t7 + 0.5, 0.3), col=CYEL, size=24)
        credit(c, 'N1_applepark')
        return
    title(c, 'BUILD A', 90, 560, 150, CBLU, pr(t, tl - 0.3, 0.4))
    title(c, 'MACHINE,', 90, 710, 150, GRN, pr(t, tl + 0.4, 0.4), rot=-2)
    title(c, 'NOT A MYTH.', 90, 860, 140, CRED, pr(t, tl + 1.2, 0.4))


def sc_predict(c, t, S):
    tn = ph("nvidia doesn't collapse"); tw = ph('still needs its chips'); tp = ph('picking the next'); t17 = ph('november seventeenth'); ts = ph('numbers are strong'); twk = ph("if they're weak"); te = ph('empty chair'); tf = ph('financial advice')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < t17 - 0.3:
        title(c, 'NO', 90, 540, 150, PAPER, pr(t, tn - 0.2, 0.4))
        title(c, 'COLLAPSE.', 90, 690, 150, CYEL, pr(t, tn + 0.3, 0.4))
        caption(c, 'THE WORLD STILL NEEDS THE CHIPS', 110, 860, pr(t, tw - 0.2, 0.3), col=PAPER, size=30, rot=-2)
        if t > tp - 0.2: caption(c, 'BUT THE NEXT CEO PICK IS HUGE', 160, 980, pr(t, tp - 0.2, 0.3), col=CYEL, size=30, rot=1.5)
        return
    title(c, 'TEST DAY:', 90, 540, 150, PAPER, pr(t, t17 - 0.3, 0.4))
    title(c, 'NOV 17.', 90, 690, 160, CYEL, pr(t, t17 + 0.2, 0.4), rot=-2)
    caption(c, 'STRONG NUMBERS = A FOOTNOTE', 120, 860, pr(t, ts - 0.2, 0.3), col=PAPER, size=32, rot=-2)
    caption(c, 'WEAK NUMBERS = BLAME THE CHAIR', 150, 980, pr(t, twk - 0.2, 0.3), col=CYEL, size=32, rot=1.5)
    if t > te - 0.4:
        kc = pr(t, te - 0.4, 0.5)
        place(c, 'N2_chair_comic.png', 800, 1230, 220 * eback(cl(kc), 1.5), rot=8, a=kc, shadow=False)
    if t > tf - 0.6: caption(c, 'NOT FINANCIAL ADVICE', 120, 1330, pr(t, tf - 0.6, 0.3), col=PAPER, size=24)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'CAN NVIDIA', 90, 530, 130, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'STAY ON TOP?', 80, 680, 124, CRED, pr(t, S['t0'] + 0.3, 0.4))
    kc = pr(t, S['t0'] + 0.3, 0.5)
    place(c, 'N2_chair_comic.png', 540, 1010 + 6 * math.sin(t * 2), 330 * eback(cl(kc), 1.5), rot=-3, a=kc, shadow=True)
    burst(c, 230, 1250, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 850, 1250, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    credit(c, 'N2_chairs')
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
    dict(k='know', t0=ph("here's what we know") - 0.2, fn=with_subs(sc_know), tin='whip'),
    dict(k='why', t0=ph('why does this matter') - 0.2, fn=with_subs(sc_why), tin='zoom'),
    dict(k='apple', t0=ph("we've seen a legend") - 0.2, fn=with_subs(sc_apple), tin='wipe', col=SEPIA),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('fourteen percent'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
