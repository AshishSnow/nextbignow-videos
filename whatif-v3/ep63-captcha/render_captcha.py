"""NextBigNow ep 63 (red/cream comic, photo cut-outs, small subtitles, v5 voice, logo watermark): the fake "I'm not a robot" (ClickFix) scam.
Facts: FTC consumer alert (June 2026): fake CAPTCHA "security verification" asks Windows+R, Ctrl+V, Enter -> runs hidden malware that steals
email and banking credentials; real CAPTCHAs never ask you to run commands; if it happened: disconnect, run a security scan, change passwords and
turn on 2FA from a different device, report at ReportFraud.ftc.gov. Techlicious: site loads a command into the clipboard; PowerShell downloads
the malware; steals saved passwords, banking credentials, crypto wallets, cookies; Mac version since May 2025.
The Hacker News (Sep 24, 2026): ClickFix = 47% of initial-access cases handled by Microsoft Defender Experts in 2025 (more than phishing);
CTM360 found 17,000+ infected URLs serving fake verification pages. UI drawn generically (no real brand logos)."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('CP_DIR', 'captcha'))
PK.IMG = os.path.join(HERE, 'captcha', 'img')
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
MONO = 'SpecialElite.ttf'
SCREEN = (245, 247, 250)


def credit(c, key, a=1.0, col=(120, 100, 70), y=1360):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s' % (cr['author'], cr['license'])).upper()[:70]
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0):
    def dr(cc): cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.01 * t, fx, fy)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def browser(c, x, y, w, h, k, rot, body, url='totally-normal-site.example'):
    """a generic comic browser window; body(cc, w, h) draws the page."""
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(SCREEN))
        cc.drawRect(R.MakeWH(w, 70), paint((215, 220, 228)))
        for i, col in enumerate((CRED, CYEL, GRN)):
            cc.drawCircle(34 + i * 34, 35, 11, paint(col)); cc.drawCircle(34 + i * 34, 35, 11, stroke(KINK, 3))
        rr = skia.RRect.MakeRectXY(R.MakeXYWH(140, 16, w - 170, 38), 19, 19)
        cc.drawRRect(rr, paint(PAPER)); cc.drawRRect(rr, stroke(KINK, 3))
        cc.drawString(url, 162, 44, font(MONO, 24), paint(KINK))
        cc.save(); cc.translate(0, 70); body(cc, w, h - 70); cc.restore()
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=12)


def verify_box(cc, x, y, w, h, t, tick_t=None, steps=None):
    """fake 'verify you are human' card. steps: list of (t_on, text)."""
    cc.drawRect(R.MakeXYWH(x + 6, y + 6, w, h), paint(KINK, 0.25))
    cc.drawRect(R.MakeXYWH(x, y, w, h), paint(PAPER)); cc.drawRect(R.MakeXYWH(x, y, w, h), stroke(KINK, 5))
    bx, by = x + 34, y + 40
    cc.drawRect(R.MakeXYWH(bx, by, 64, 64), paint((255, 255, 255))); cc.drawRect(R.MakeXYWH(bx, by, 64, 64), stroke(KINK, 5))
    if tick_t is not None and t > tick_t:
        k = pr(t, tick_t, 0.25)
        p = skia.Path(); p.moveTo(bx + 12, by + 34); p.lineTo(bx + 28, by + 50); p.lineTo(lerp(bx + 28, bx + 56, k), lerp(by + 50, by + 14, k))
        cc.drawPath(p, stroke(GRN, 10))
    cc.drawString("I'm not a robot", bx + 90, by + 44, font(MONO, 36), paint(KINK))
    if steps:
        yy = y + 150
        cc.drawString('VERIFICATION STEPS:', x + 34, yy, font(MONO, 26), paint(CRED)); yy += 50
        for t0, s in steps:
            k = pr(t, t0 - 0.2, 0.3)
            if k <= 0: continue
            cc.drawString(s, x + 34, yy, font(MONO, 30), paint(KINK, k)); yy += 48


def keycap(c, x, y, s, k, down=0.0, col=PAPER, w=None):
    if k <= 0: return
    w = w or max(130, width(s, MONO, 44) + 60); h = 120
    sc = eback(cl(k), 1.5)
    c.save(); c.translate(x, y); c.scale(sc, sc)
    dy = 12 * down
    rr0 = skia.RRect.MakeRectXY(R.MakeXYWH(-w / 2, -h / 2 + 16, w, h), 18, 18); c.drawRRect(rr0, paint(KINK))
    rr = skia.RRect.MakeRectXY(R.MakeXYWH(-w / 2, -h / 2 + dy, w, h), 18, 18)
    c.drawRRect(rr, paint(CYEL if down > 0.5 else col)); c.drawRRect(rr, stroke(KINK, 7))
    title(c, s, 0, 16 + dy, 50, KINK, 1.0, 'c', shadow=0, outline=0.01)
    c.restore()


def keys_row(c, y, t, tw, tc, te, labels=(('WIN', '+', 'R'), ('CTRL', '+', 'V'), ('ENTER',))):
    for row, (t0, keys) in enumerate(zip((tw, tc, te), labels)):
        k = pr(t, t0 - 0.3, 0.35)
        if k <= 0: continue
        down = 1.0 if (t > t0 + 0.3 and t < t0 + 0.6) else 0.0
        if len(keys) == 1:
            keycap(c, 540, y + row * 165, keys[0], k, down, w=320)
        else:
            keycap(c, 380, y + row * 165, keys[0], k, down, w=220)
            title(c, '+', 540, y + row * 165 + 22, 70, KINK, k, 'c', shadow=0)
            keycap(c, 700, y + row * 165, keys[2], k, down)
        title(c, str(row + 1), 140, y + row * 165 + 22, 70, CRED, k, 'c', shadow=4)


def run_box(cc, x, y, w, h, t, t_paste, t_enter):
    cc.drawRect(R.MakeXYWH(x + 8, y + 8, w, h), paint(KINK))
    cc.drawRect(R.MakeXYWH(x, y, w, h), paint(SCREEN)); cc.drawRect(R.MakeXYWH(x, y, w, h), stroke(KINK, 6))
    cc.drawRect(R.MakeXYWH(x, y, w, 56), paint((215, 220, 228))); cc.drawRect(R.MakeXYWH(x, y, w, 56), stroke(KINK, 4))
    cc.drawString('Run', x + 24, y + 40, font(MONO, 30), paint(KINK))
    cc.drawString('Open:', x + 24, y + 120, font(MONO, 28), paint(KINK))
    fx = x + 130; fw = w - 160
    cc.drawRect(R.MakeXYWH(fx, y + 86, fw, 52), paint((255, 255, 255))); cc.drawRect(R.MakeXYWH(fx, y + 86, fw, 52), stroke(KINK, 4))
    if t > t_paste:
        s = 'powershell -w hidden -c "iwr ...|iex"'
        n = int(len(s) * cl((t - t_paste) / 0.35))
        cc.drawString(s[:n], fx + 12, y + 122, font(MONO, 22), paint(CRED))
    bcol = CYEL if t > t_enter else PAPER
    cc.drawRect(R.MakeXYWH(x + w - 190, y + h - 76, 160, 56), paint(bcol)); cc.drawRect(R.MakeXYWH(x + w - 190, y + h - 76, 160, 56), stroke(KINK, 4))
    cc.drawString('OK', x + w - 132, y + h - 36, font(MONO, 30), paint(KINK))


def clipboard(c, x, y, s, k, rot=-6, txt=None):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); sc = s * eback(cl(k), 1.4); c.scale(sc, sc)
    c.drawRect(R.MakeXYWH(-110 + 10, -140 + 10, 220, 280), paint(KINK))
    c.drawRect(R.MakeXYWH(-110, -140, 220, 280), paint((190, 140, 80))); c.drawRect(R.MakeXYWH(-110, -140, 220, 280), stroke(KINK, 7))
    c.drawRect(R.MakeXYWH(-85, -105, 170, 225), paint(PAPER)); c.drawRect(R.MakeXYWH(-85, -105, 170, 225), stroke(KINK, 4))
    c.drawRect(R.MakeXYWH(-45, -160, 90, 50), paint(GREY)); c.drawRect(R.MakeXYWH(-45, -160, 90, 50), stroke(KINK, 6))
    for i in range(5): c.drawLine(-65, -70 + i * 36, 65 - (i % 2) * 30, -70 + i * 36, stroke(CRED if txt else KINK, 6))
    c.restore()


def loot(c, x, y, s, k, col, rot):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); sc = eback(cl(k), 1.5); c.scale(sc, sc)
    tw_ = width(s, MONO, 34) + 50
    c.drawRect(R.MakeXYWH(-tw_ / 2 + 8, -38 + 8, tw_, 76), paint(KINK))
    c.drawRect(R.MakeXYWH(-tw_ / 2, -38, tw_, 76), paint(col)); c.drawRect(R.MakeXYWH(-tw_ / 2, -38, tw_, 76), stroke(KINK, 6))
    c.drawString(s, -tw_ / 2 + 25, 12, font(MONO, 34), paint(PAPER if col in (CRED, CBLU, KINK) else KINK))
    c.restore()


def sc_hook(c, t, S):
    tn = ph('not a robot'); th = ph('handed a hacker'); tb = ph('bank password')
    paper(c, t)
    def body(cc, w, h):
        cc.drawRect(R.MakeWH(w, h), paint((230, 234, 240)))
        verify_box(cc, 70, 120, w - 140, 150, t, tick_t=tn + 0.2)
    browser(c, 110, 380, 860, 520, pr(t, 0.0, 0.4), -1.5, body)
    # the click: a cursor arrow moving onto the checkbox
    k = pr(t, 0.2, max(0.4, tn + 0.1))
    cx, cy = lerp(780, 270, eo(k)), lerp(1050, 690, eo(k))
    p = skia.Path(); p.moveTo(cx, cy); p.lineTo(cx, cy + 70); p.lineTo(cx + 18, cy + 54); p.lineTo(cx + 34, cy + 86); p.lineTo(cx + 46, cy + 80); p.lineTo(cx + 30, cy + 48); p.lineTo(cx + 54, cy + 48); p.close()
    c.drawPath(p, paint(PAPER)); c.drawPath(p, stroke(KINK, 6))
    if t > th - 0.3:
        loot(c, 540, 1080, 'BANK PASSWORD: ********', pr(t, tb - 0.3, 0.35), CRED, -3)
        burst(c, 820, 330, 120, 'HACKED?', pr(t, th - 0.3, 0.35), size=42, rot=8)


def sc_how(c, t, S):
    tc = ph("it's called clickfix"); tn = ph('normal looking website'); tv = ph('verify you are human'); tl = ph('traffic lights'); t3 = ph('three easy steps')
    tw = ph('press windows and r'); tcv = ph('press control and v'); te = ph('press enter')
    paper(c, t)
    caption(c, "IT'S REAL. IT'S EVERYWHERE.", LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tw - 0.6:
        title(c, 'THE "CLICKFIX"', 90, 540, 120, CBLU, pr(t, tc - 0.2, 0.4))
        title(c, 'SCAM', 90, 690, 150, CRED, pr(t, tc + 0.3, 0.4), rot=-2)
        def body(cc, w, h):
            cc.drawRect(R.MakeWH(w, h), paint((230, 234, 240)))
            if t > tv - 0.3:
                verify_box(cc, 50, 40, w - 100, h - 80, t, steps=[(t3, 'Press these keys:')])
            if t > tl - 0.2 and t < t3:
                caption(cc, 'NO TRAFFIC LIGHTS?', 300, h - 30, pr(t, tl - 0.2, 0.3), col=CYEL, size=26)
        browser(c, 110, 760, 860, 480, pr(t, tn - 0.3, 0.45), 1.2, body)
        return
    title(c, '3 "EASY" STEPS', 90, 540, 120, CBLU, pr(t, tw - 0.6, 0.4))
    keys_row(c, 760, t, tw, tcv, te)


def sc_hacked(c, t, S):
    ty = ph('you just hacked yourself')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, "THAT'S IT.", LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=34)
    title(c, 'YOU JUST', 540, 700, 150, PAPER, pr(t, S['t0'] + 0.3, 0.4), 'c')
    title(c, 'HACKED', 540, 880, 190, CYEL, pr(t, ty + 0.1, 0.4), 'c', rot=-3)
    title(c, 'YOURSELF.', 540, 1040, 150, PAPER, pr(t, ty + 0.4, 0.4), 'c')


def sc_trick(c, t, S):
    tsc = ph('secretly copied a command'); tw = ph('windows plus r opens'); tcv = ph('control v pastes'); te = ph('enter runs it'); ts = ph('in seconds')
    tp = ph('saved passwords'); tb = ph('banking logins'); tcr = ph('even your crypto')
    paper(c, t)
    caption(c, "HERE'S THE TRICK", LX, 340, pr(t, S['t0'], 0.3), col=CBLU, size=30)
    if t < tw - 0.3:
        title(c, 'IT SECRETLY', 90, 540, 130, CBLU, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'COPIES CODE', 90, 690, 130, CRED, pr(t, S['t0'] + 0.7, 0.4), rot=-2)
        kl = pr(t, S['t0'] + 0.3, 0.5)
        place(c, 'C2_cut_comic.png', 380, 1010, 540 * eback(cl(kl), 1.3), rot=-3, a=kl, shadow=True)
        credit(c, 'C2_laptop')
        if kl >= 1:
            c.save(); c.translate(380, 1010); c.rotate(-3)
            c.drawRect(R.MakeXYWH(-150, -180, 280, 70), paint(PAPER)); c.drawRect(R.MakeXYWH(-150, -180, 280, 70), stroke(KINK, 4))
            c.drawRect(R.MakeXYWH(-135, -165, 40, 40), stroke(KINK, 4))
            c.drawString('not a robot', -85, -133, font(MONO, 24), paint(KINK))
            c.restore()
        if t > tsc:
            p_ = stroke(CRED, 10); p_.setPathEffect(skia.DashPathEffect.Make([22, 14], 0))
            c.drawLine(520, 900, lerp(520, 680, pr(t, tsc, 0.4)), lerp(900, 980, pr(t, tsc, 0.4)), p_)
        clipboard(c, 810, 1040, 1.0, pr(t, tsc + 0.2, 0.5), txt=True)
        if t > tsc + 0.3: caption(c, 'YOUR CLIPBOARD, NOW LOADED', 200, 1270, pr(t, tsc + 0.3, 0.3), col=CYEL, size=28, rot=-1.5)
        return
    if t < ts - 0.3:
        title(c, 'PASTE. RUN.', 90, 560, 140, CRED, pr(t, tw - 0.3, 0.4))
        def dr(cc):
            cc.drawRect(R.MakeWH(880, 400), paint((40, 44, 60)))
            run_box(cc, 40, 50, 800, 300, t, tcv, te)
        panel(c, 100, 680, 880, 400, rot=1.0, k=pr(t, tw - 0.1, 0.45), draw=dr, border=7, shadow=12)
        keycap(c, 300, 1220, 'WIN+R', pr(t, tw, 0.3), 1.0 if tw + 0.3 < t < tw + 0.6 else 0.0, w=260)
        keycap(c, 560, 1220, 'CTRL+V', pr(t, tcv, 0.3), 1.0 if tcv + 0.3 < t < tcv + 0.6 else 0.0, w=260)
        keycap(c, 820, 1220, 'ENTER', pr(t, te, 0.3), 1.0 if te + 0.3 < t < te + 0.6 else 0.0, w=240)
        return
    title(c, 'IN SECONDS,', 90, 540, 130, CBLU, pr(t, ts - 0.3, 0.4))
    title(c, 'IT TAKES:', 90, 690, 140, CRED, pr(t, ts + 0.2, 0.4), rot=-2)
    place(c, 'C2_cut_comic.png', 540, 1000, 640 * eback(cl(pr(t, ts - 0.1, 0.5)), 1.3), rot=-3, a=pr(t, ts - 0.1, 0.5), shadow=True)
    credit(c, 'C2_laptop')
    if t > ts + 0.4:
        c.save(); c.translate(540, 1000); c.rotate(-3); c.translate(-540, -1000)
        c.drawString('SENDING...', 345, 840, font(MONO, 40), paint(CRED))
        kk = cl((t - ts - 0.4) / 2.5)
        c.drawRect(R.MakeXYWH(345, 870, 280 * kk, 34), paint(GRN)); c.drawRect(R.MakeXYWH(345, 870, 280, 34), stroke(PAPER, 4))
        c.restore()
    for i, (t0, s, col) in enumerate(((tp, 'SAVED PASSWORDS', CRED), (tb, 'BANK LOGINS', CBLU), (tcr, 'CRYPTO WALLETS', CYEL))):
        k = pr(t, t0 - 0.2, 0.4)
        loot(c, lerp(540, (300, 760, 560)[i], eo(k)), lerp(1000, (880, 1120, 1300)[i], eo(k)), s, k, col, (-6, 5, -3)[i])


def sc_stats(c, t, S):
    tm = ph('microsoft says'); t47 = ph('forty seven percent'); tp = ph('regular phishing emails'); t17 = ph('seventeen thousand')
    paper(c, t)
    caption(c, 'IT WORKS WAY TOO WELL', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < t17 - 0.4:
        title(c, '47%', 540, 720, 300, CRED, pr(t, t47 - 0.3, 0.4), 'c', rot=-3)
        caption(c, 'OF ATTACKS MICROSOFT EXPERTS HANDLED IN 2025', 130, 820, pr(t, t47 + 0.4, 0.3), size=26)
        def dr(cc):
            cc.drawRect(R.MakeWH(860, 300), paint(PAPER))
            k = pr(t, t47, 0.8)
            for i, (lab, v, col) in enumerate((('FAKE "VERIFY" TRICK', 47, CRED), ('EVERYTHING ELSE', 53, GREY))):
                y = 60 + i * 120
                cc.drawString(lab, 30, y, font(MONO, 28), paint(KINK))
                cc.drawRect(R.MakeXYWH(30, y + 14, 780 * v / 100 * eo(k), 60), paint(col)); cc.drawRect(R.MakeXYWH(30, y + 14, 780 * v / 100 * eo(k), 60), stroke(KINK, 5))
        panel(c, 110, 900, 860, 300, rot=1.2, k=pr(t, tm, 0.5), draw=dr)
        if t > tp - 0.3: burst(c, 840, 520, 110, 'MORE THAN PHISHING', pr(t, tp - 0.3, 0.35), size=24, col=CYEL, txt=CRED, rot=8)
        return
    title(c, '17,000+', 540, 700, 220, CBLU, pr(t, t17 - 0.4, 0.4), 'c', rot=-2)
    caption(c, 'INFECTED WEBSITES SHOWING THE FAKE CHECK', 150, 800, pr(t, t17 + 0.2, 0.3), size=26)
    photo_panel(c, 'C3_server', 110, 880, 860, 400, -1.2, pr(t, t17, 0.5), t=t - t17)
    credit(c, 'C3_server')


def sc_rule(c, t, S):
    tr = ph("so here's the rule"); tnv = ph('will never ask you'); te = ph('ever'); tc = ph('close the tab')
    paper(c, t)
    caption(c, 'THE ONE RULE', LX, 340, pr(t, S['t0'], 0.3), col=GRN if False else CBLU, size=30)
    def card(cc, w, h, real):
        cc.drawRect(R.MakeWH(w, h), paint(PAPER))
        cc.drawRect(R.MakeWH(w, 70), paint(GRN if real else CRED))
        title(cc, 'REAL' if real else 'FAKE', w / 2, 56, 50, PAPER, 1.0, 'c', shadow=3)
        lines = ('CLICK A BOX', 'PICK THE PICTURES', 'TYPE THE LETTERS') if real else ('PRESS WIN + R', 'PRESS CTRL + V', 'PRESS ENTER')
        for i, s in enumerate(lines):
            cc.drawString(s, 24, 140 + i * 64, font(MONO, 30), paint(KINK))
    panel(c, 90, 520, 440, 360, rot=-2, k=pr(t, tr, 0.45), draw=lambda cc: card(cc, 440, 360, True))
    panel(c, 550, 540, 440, 360, rot=2, k=pr(t, tr + 0.3, 0.45), draw=lambda cc: card(cc, 440, 360, False))
    if t > tnv - 0.2:
        title(c, 'KEYS OR PASTE?', 540, 1040, 110, CBLU, pr(t, tnv - 0.2, 0.4), 'c')
        title(c, "IT'S A SCAM.", 540, 1180, 130, CRED, pr(t, te - 0.2, 0.4), 'c', rot=-2)
    if t > tc - 0.3: burst(c, 830, 470, 120, 'CLOSE THE TAB', pr(t, tc - 0.3, 0.35), size=30, col=CYEL, txt=CRED, rot=8)


def sc_fix(c, t, S):
    td = ph('disconnect from the internet'); ts = ph('security scan'); tc = ph('change your passwords')
    paper(c, t)
    caption(c, 'ALREADY DID IT?', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    title(c, 'DO THIS NOW:', 90, 560, 140, CBLU, pr(t, S['t0'] + 0.2, 0.4))
    for i, (t0, s, col) in enumerate(((td, 'GO OFFLINE', CRED), (ts, 'RUN A SECURITY SCAN', CBLU), (tc, 'NEW PASSWORDS (OTHER DEVICE)', GRN))):
        k = pr(t, t0 - 0.3, 0.35)
        if k <= 0: continue
        def dr(cc, s=s, col=col, i=i):
            cc.drawRect(R.MakeWH(860, 150), paint(PAPER)); cc.drawRect(R.MakeXYWH(0, 0, 24, 150), paint(col))
            title(cc, str(i + 1), 80, 110, 90, col, 1.0, 'c', shadow=4)
            title(cc, s, 150, 96, 48, KINK, 1.0, shadow=0, outline=0.01)
        panel(c, 110, 700 + i * 190, 860, 150, rot=(-1.5, 1, -1)[i], k=k, draw=dr, border=6, shadow=8)


def sc_ask(c, t, S):
    ty = ph('yes or no'); tsd = ph('send this to')
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'WOULD YOU HAVE', 90, 540, 110, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'FALLEN FOR IT?', 80, 680, 120, CRED, pr(t, S['t0'] + 0.4, 0.4), rot=-2)
    def body(cc, w, h):
        cc.drawRect(R.MakeWH(w, h), paint((230, 234, 240)))
        verify_box(cc, 50, 40, w - 100, 150, t, tick_t=S['t0'] + 0.8)
    browser(c, 190, 760, 700, 330, pr(t, S['t0'] + 0.3, 0.45), 1.5, body)
    burst(c, 230, 1220, 100, 'YES', pr(t, ty - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 850, 1220, 100, 'NO', pr(t, ty + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    cta = 'SUBSCRIBE FOR DAILY WHAT IFS' if PLAT == 'yt' else 'SEND THIS TO YOUR FAMILY GROUP'
    caption(c, cta, 230, 1375, pr(t, tsd, 0.3), col=CYEL, size=28, rot=-1.5)
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
    dict(k='how', t0=ph('this is real') - 0.15, fn=with_subs(sc_how), tin='whip'),
    dict(k='hacked', t0=ph("that's it") - 0.15, fn=with_subs(sc_hacked), tin='flash'),
    dict(k='trick', t0=ph("here's the trick") - 0.2, fn=with_subs(sc_trick), tin='zoom'),
    dict(k='stats', t0=ph('and it works way') - 0.2, fn=with_subs(sc_stats), tin='whip'),
    dict(k='rule', t0=ph("so here's the rule") - 0.2, fn=with_subs(sc_rule), tin='zoom'),
    dict(k='fix', t0=ph('already did it') - 0.2, fn=with_subs(sc_fix), tin='whip'),
    dict(k='ask', t0=ph('would you have fallen') - 0.2, fn=with_subs(sc_ask), tin='flash'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('you just hacked yourself'), 12, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
