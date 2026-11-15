"""NextBigNow ep 55 (vintage comic + editorial, small subtitles, v5 voice): What if the cloud goes down for a week?
Facts: TIME (13 Nov 2026) / Al Jazeera (13 Nov 2026) - Microsoft 365 outage began Thu 12 Nov 2026 (~1pm ET); Outlook, Teams, Copilot; nearly 130,000
Downdetector reports for Outlook; ~24h to sustained recovery; hit US House of Representatives, UK government and parts of NHS, Japan government IT
(traders switched to fax), Australia ASIO + AFP, Philippines Supreme Court; Microsoft: not cyber, a problem from a network capacity upgrade / network change.
CrowdStrike 19 Jul 2024: faulty update crashed ~8.5M Windows devices (Microsoft est.); airlines/airports disrupted, some handwritten boarding passes;
Delta cancelled ~7,000 flights over several days; Parametrix est. ~$5.4B direct losses to US Fortune 500 (ex-Microsoft).
Photos (Wikimedia Commons): see cloud/img/credits.json. Brand marks covered."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('CL_DIR', 'cloud'))
PK.IMG = os.path.join(HERE, 'cloud', 'img')
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



def cloud_shape(c, x, y, w, col, k, label, lsize=40):
    if k <= 0: return
    c.save(); c.translate(x, y); s = eback(cl(k), 1.6); c.scale(s, s)
    p = skia.Path()
    for cx_, cy_, r_ in ((-0.28, 0.05, 0.22), (0.0, -0.1, 0.3), (0.28, 0.05, 0.22), (0.0, 0.12, 0.24)):
        p.addCircle(cx_ * w, cy_ * w, r_ * w)
    p2 = skia.Path(p); c.translate(8, 8); c.drawPath(p2, paint(KINK)); c.translate(-8, -8)
    c.drawPath(p, paint(col)); dots(c, (-w / 2, -w / 2, w, w), KINK, cell=16, rmax=3, grad=(0.4, 1.0), a=0.2)
    c.drawPath(p, stroke(KINK, 7))
    title(c, label, 0, 0.12 * w + 14, lsize, PAPER, 1.0, 'c', shadow=4)
    c.restore()


def sc_hook(c, t, S):
    tf = ph('fax machines'); tq = ph('so what happens'); td = ph('almost a full day')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'NOVEMBER 12, 2026', LX, 340, 1.0, col=CRED, size=30)
        title(c, 'EMAIL DOWN.', 80, 540, 150, CRED, 1.0, rot=-2)
        title(c, 'WORLDWIDE.', 90, 690, 140, CBLU, 1.0)
        photo_panel(c, 'C3_servers', 90, 770, 900, 540, 1.2, 1.0, t=t)
        if t > td - 0.2: caption(c, 'FOR ALMOST A FULL DAY', 140, 1250, pr(t, td - 0.2, 0.3), col=CYEL, size=30, rot=-2)
        if t > tf - 0.3:
            kf = pr(t, tf - 0.3, 0.5)
            place(c, 'C2_fax_comic.png', 640, 1080, 560 * eback(cl(kf), 1.6), rot=6, a=kf, shadow=True)
            burst(c, 300, 1000, 110, 'FAX?!', pr(t, tf, 0.35), size=56, rot=-8)
            credit(c, 'C2_fax')
        else:
            credit(c, 'C3_servers')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF THE', 90, 540, 130, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'CLOUD DIES', 90, 680, 140, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'FOR A WEEK?', 90, 820, 130, PAPER, pr(t, tq + 0.45, 0.4))
    kk = pr(t, tq + 0.5, 0.5); dk = pr(t, tq + 1.2, 1.2)
    def dr(cc):
        cover(cc, img('C3_servers_comic.png'), 0, 0, 800, 400, 1.1, 0.5, 0.5)
        cc.drawRect(R.MakeWH(800, 400), paint(KINK, 0.85 * dk))
        if dk > 0.6: title(cc, 'OFFLINE', 400, 230, 90, CRED, pr(t, tq + 2.0, 0.3), 'c', shadow=5)
    panel(c, 140, 920, 800, 400, rot=-2, k=kk, draw=dr)


def sc_what(c, t, S):
    t13 = ph('hundred and thirty thousand'); th = ph('house of representatives'); tb = ph("britain's health service"); tj = ph('japan and australia'); tc = ph("wasn't a cyberattack"); tn = ph('network change')
    paper(c, t)
    caption(c, "HERE'S WHAT HAPPENED", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tc - 0.3:
        title(c, '130,000', 80, 540, 150, CRED, pr(t, S['t0'] + 0.2, 0.4), rot=-2)
        title(c, 'OUTAGE REPORTS.', 90, 680, 110, CBLU, pr(t, S['t0'] + 0.5, 0.4))
        caption(c, 'OUTLOOK . TEAMS . COPILOT', 120, 780, pr(t, S['t0'] + 0.6, 0.3), col=CYEL, size=28, rot=-1.5)
        mini(c, 90, 860, 430, 220, -2, pr(t, th - 0.4, 0.4), 'USA', 'US HOUSE', CBLU, bigsize=52)
        mini(c, 560, 870, 430, 220, 1.5, pr(t, tb - 0.4, 0.4), 'UK', 'HEALTH SERVICE', CRED, bigsize=40)
        mini(c, 260, 1120, 560, 220, -1, pr(t, tj - 0.4, 0.4), 'GOVERNMENTS', 'JAPAN + AUSTRALIA', CYEL, txtc=CRED, bigsize=42)
        return
    title(c, 'NOT A HACK.', 90, 540, 140, GRN, pr(t, tc - 0.3, 0.4))
    title(c, 'A NETWORK', 90, 690, 140, CRED, pr(t, tn - 0.4, 0.4))
    title(c, 'CHANGE.', 90, 830, 140, CRED, pr(t, tn, 0.4), rot=-2)
    photo_panel(c, 'C3_servers', 140, 900, 800, 420, 1.5, pr(t, tc, 0.5), zoom=1.3, t=t - tc)
    credit(c, 'C3_servers')


def sc_scary(c, t, S):
    th = ph('no hacker'); tb = ph('no bomb'); tj = ph('just one bad change'); tm = ph('millions of companies'); tms = ph('microsoft amazon'); tsn = ph('one of them sneezes')
    paper(c, t)
    caption(c, "THAT'S THE SCARY PART", LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tm - 0.3:
        title(c, 'NO HACKER.', 90, 560, 140, CBLU, pr(t, th - 0.2, 0.4))
        title(c, 'NO BOMB.', 90, 710, 140, CBLU, pr(t, tb - 0.2, 0.4))
        title(c, 'JUST ONE', 90, 900, 150, CRED, pr(t, tj - 0.2, 0.4), rot=-2)
        title(c, 'BAD CHANGE.', 90, 1050, 140, CRED, pr(t, tj + 0.3, 0.4), rot=-2)
        return
    title(c, 'MILLIONS OF', 90, 530, 120, CBLU, pr(t, tm - 0.3, 0.4))
    title(c, 'COMPANIES...', 90, 660, 120, CBLU, pr(t, tm, 0.4))
    clouds = [(270, 900, CBLU, 'MICROSOFT', tms - 0.3), (720, 920, CRED, 'AMAZON', tms + 0.4), (500, 1180, GRN, 'GOOGLE', tms + 1.0)]
    # companies hanging off the clouds
    for i in range(36):
        cx_, cy_, col, _, t0 = clouds[i % 3]
        a = hsh(i, 7) * 6.28; r = 210 + 60 * hsh(i, 8)
        px, py = cx_ + r * math.cos(a), cy_ + r * 0.6 * math.sin(a)
        if py < 760 or py > 1360 or px < 80 or px > 950: continue
        kk = min(pr(t, tm + 0.05 * i, 0.3), pr(t, t0, 0.3))
        if kk <= 0: continue
        c.drawLine(cx_, cy_, px, py, stroke(KINK, 2, a=0.5 * kk))
        c.drawRect(R.MakeXYWH(px - 12, py - 12, 24, 24), paint(KINK, kk)); c.drawRect(R.MakeXYWH(px - 9, py - 9, 18, 18), paint(PAPER, kk))
    for cx_, cy_, col, lab, t0 in clouds:
        shake = 8 * math.sin(t * 40) * pr(t, tsn, 0.2) * (1 - pr(t, tsn + 0.8, 0.4)) if lab == 'MICROSOFT' else 0
        cloud_shape(c, cx_ + shake, cy_, 300, col, pr(t, t0, 0.4), lab, lsize=36)
    if t > tsn - 0.2: burst(c, 820, 1260, 120, 'ACHOO!', pr(t, tsn + 0.3, 0.35), size=48, rot=8)


def sc_crowd(c, t, S):
    tj = ph('in july twenty twenty four'); tu = ph('one faulty update'); t85 = ph('eight and a half million'); tbs = ph('blue screen of death')
    th = ph('handwritten boarding passes'); td = ph('delta alone'); t5 = ph('more than five billion'); tfx = ph('the bug was fixed'); tcl = ph('the cleanup took')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN HOW BAD IT GETS", LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < th - 0.4:
        title(c, 'JULY 2024:', 90, 530, 130, CBLU, pr(t, tj - 0.2, 0.4))
        title(c, 'ONE BAD UPDATE.', 80, 680, 110, CRED, pr(t, tu - 0.2, 0.4), rot=-2)
        photo_panel(c, 'C1_bsod', 90, 760, 900, 580, 1.2, pr(t, S['t0'] + 0.4, 0.5), fx=0.3, t=t - S['t0'])
        if t > t85 - 0.2: burst(c, 820, 830, 125, '8.5M PCs', pr(t, t85, 0.35), size=42, rot=8)
        if t > tbs - 0.2: caption(c, 'BLUE SCREENS AT LAGUARDIA AIRPORT, NYC', 150, 1290, pr(t, tbs - 0.2, 0.3), col=CYEL, size=24)
        credit(c, 'C1_bsod')
        return
    if t < tfx - 0.3:
        title(c, 'THE DAMAGE:', 90, 540, 140, CRED, pr(t, th - 0.4, 0.4))
        mini(c, 90, 640, 430, 300, -2, pr(t, th - 0.3, 0.4), 'SOME AIRPORTS', 'HAND-WRITTEN PASSES', CBLU, bigsize=38)
        mini(c, 560, 660, 430, 300, 1.5, pr(t, td - 0.2, 0.4), 'DELTA CANCELED', 'THOUSANDS OF FLIGHTS', CRED, bigsize=36)
        mini(c, 260, 1010, 560, 300, -1, pr(t, t5 - 0.3, 0.4), 'BIG US COMPANIES LOST (EST.)', '$5 BILLION+', CYEL, txtc=CRED, bigsize=70)
        return
    title(c, 'FIX: HOURS.', 90, 560, 140, GRN, pr(t, tfx - 0.3, 0.4))
    title(c, 'CLEANUP: DAYS.', 80, 720, 120, CRED, pr(t, tcl - 0.3, 0.4), rot=-2)
    kb = pr(t, tfx, 0.5)
    place(c, 'C1_bsod_comic.png', 540, 1100, 620 * eback(cl(kb), 1.4), rot=-4, a=kb, shadow=True)


def sc_predict(c, t, S):
    tu = ph('full week offline'); tb = ph('backups for their backups'); tk = ph('big outages keep'); ts = ph('stop trusting'); tsc = ph('second cloud'); to = ph('old school offline'); tf = ph('even the fax')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < ts - 0.3:
        title(c, 'A FULL WEEK?', 90, 540, 130, PAPER, pr(t, tu - 0.3, 0.4))
        title(c, 'UNLIKELY.', 90, 690, 150, CYEL, pr(t, tu + 0.4, 0.4))
        caption(c, 'BACKUPS FOR THEIR BACKUPS', 120, 860, pr(t, tb - 0.2, 0.3), col=PAPER, size=32, rot=-2)
        if t > tk - 0.2: caption(c, 'BUT BIG OUTAGES KEEP COMING', 160, 1000, pr(t, tk - 0.2, 0.3), col=CYEL, size=32, rot=1.5)
        photo_panel(c, 'C3_servers', 140, 1080, 800, 280, 1.5, pr(t, tb, 0.5), t=t - tb)
        return
    title(c, 'ONE CLOUD', 90, 540, 150, PAPER, pr(t, ts - 0.3, 0.4))
    title(c, '= ONE RISK.', 90, 690, 140, CYEL, pr(t, ts, 0.4))
    caption(c, 'PLAN B: A SECOND CLOUD', 120, 850, pr(t, tsc - 0.2, 0.3), col=PAPER, size=32, rot=-2)
    caption(c, 'PLAN C: OFFLINE TOOLS', 160, 970, pr(t, to - 0.2, 0.3), col=CYEL, size=32, rot=1.5)
    if t > tf - 0.4:
        kf = pr(t, tf - 0.4, 0.5)
        place(c, 'C2_fax_comic.png', 620, 1200, 460 * eback(cl(kf), 1.6), rot=-6, a=kf, shadow=True)
        burst(c, 300, 1220, 100, 'FAX!', pr(t, tf, 0.35), size=52, col=CYEL, txt=CRED, rot=-8)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'DID THE OUTAGE', 80, 530, 110, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'HIT YOU?', 90, 670, 150, CRED, pr(t, S['t0'] + 0.3, 0.4))
    photo_panel(c, 'C3_servers', 120, 740, 840, 420, -1.5, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
    burst(c, 260, 1260, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 820, 1260, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    credit(c, 'C3_servers')
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
    dict(k='scary', t0=ph("and that's the scary") - 0.2, fn=with_subs(sc_scary), tin='zoom'),
    dict(k='crowd', t0=ph("we've seen how bad") - 0.2, fn=with_subs(sc_crowd), tin='wipe', col=SEPIA),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('blue screen of death'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
