"""NextBigNow ep 65, CINEMATIC style: full-bleed graded photos, camera moves, parallax cut-outs, grain, light leaks, hard cuts.
Story: Juliane Koepcke, LANSA Flight 508 (Dec 24, 1971): lightning broke the Lockheed Electra apart ~10,000 ft over the Peruvian Amazon;
she fell still strapped to her seat row, broken collarbone, one shoe, a bag of sweets; followed a stream (her father's advice);
maggots in her wounds; on day 10 found a boat and an empty hut; local workers found her the next day; 92 aboard, sole survivor.
Sources: Amusing Planet, ExplorersWeb, The Line Up. Photos: Wikimedia Commons, see juliane credits.json. No photos of real people."""
import sys, os, math, re, json, random
import numpy as np, skia
from PIL import Image, ImageEnhance, ImageFilter
from toon import W, H, R, paint, stroke, lin, argb, eo, eio, eback, pr, cl, lerp
from edkit import mono, PAPER
import photokit as PK
from photokit import img, cover, place
from comickit import font, width, CRED, CYEL, KINK, sub_chunks, sub_tokens
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('JU_DIR', 'juliane'))
PK.IMG = os.path.join(HERE, 'jungle', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))
PLAT = os.environ.get('PLAT', 'ig')
SUBY = 1500 if PLAT == 'yt' else 1440
FD = '/usr/share/fonts/opentype/inter/'
FX = os.path.join(HERE, '..', 'fonts')
ANTON = os.path.join(FX, 'Anton.ttf'); SERIF = os.path.join(FX, 'Cormorant-MediumItalic.ttf')
YEL = (255, 214, 64); WHITE = (255, 255, 255)


def F(path, size):
    f = skia.Font(skia.Typeface.MakeFromFile(path), size); f.setEdging(skia.Font.Edging.kAntiAlias); return f


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z0-9']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.5
DURATION = END + 2.2


def has(key):
    return any(os.path.getsize(os.path.join(PK.IMG, p)) > 5000 for p in os.listdir(PK.IMG) if p.startswith(key + '.'))


def src(key):
    for p in os.listdir(PK.IMG):
        if p.startswith(key + '.') and p.split('.')[-1].lower() in ('jpg', 'jpeg', 'png') and os.path.getsize(os.path.join(PK.IMG, p)) > 5000:
            return os.path.join(PK.IMG, p)


def grade(key, look='cine'):
    """natural film grade: lifted contrast, warm highlights / cool shadows, rich but not neon."""
    out = os.path.join(PK.IMG, '%s__g_%s.png' % (key, look))
    if not os.path.exists(out):
        im = Image.open(src(key)).convert('RGB'); im.thumbnail((2000, 3000))
        a = np.asarray(im).astype(np.float32) / 255
        a = np.clip((a - 0.5) * 1.12 + 0.5, 0, 1)
        lum = a.mean(2, keepdims=True)
        warm = np.array([1.05, 1.0, 0.9]); cool = np.array([0.92, 1.0, 1.06])
        if look == 'night': warm = np.array([0.95, 1.0, 1.08]); a = a * 0.8
        if look == 'jungle': warm = np.array([1.02, 1.06, 0.88]); cool = np.array([0.9, 1.04, 0.98])
        a = a * (lum * warm + (1 - lum) * cool)
        im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
        im = ImageEnhance.Color(im).enhance(1.25 if look != 'night' else 1.05)
        im.save(out)
    return os.path.basename(out)


def shot(c, key, t, t0, t1, look='cine', z0=1.06, z1=1.18, fx0=0.5, fx1=0.5, fy0=0.5, fy1=0.5):
    """full-bleed photo with a continuous camera move across the shot (never static)."""
    k = cl((t - t0) / max(0.01, t1 - t0)); k = 0.5 - 0.5 * math.cos(math.pi * k) * 0.0 + k * 0.5 if False else k
    cover(c, img(grade(key, look)), 0, 0, W, H, lerp(z0, z1, k), lerp(fx0, fx1, k), lerp(fy0, fy1, k))


def vignette(c, a=0.6):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial((W / 2, H * 0.45), H * 0.75, [argb((0, 0, 0), 0.0), argb((0, 0, 0), 0.0), argb((0, 0, 0), a)], [0.0, 0.5, 1.0]))
    c.drawRect(R.MakeWH(W, H), p)


def band(c, y0, y1, a=0.75):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([(0, y0), (0, y1)], [argb((0, 0, 0), 0.0), argb((0, 0, 0), a)]))
    c.drawRect(R.MakeLTRB(0, y0, W, y1), p)


def grain(c, t, a=0.07):
    rnd = random.Random(int(t * 30))
    for i in range(1600):
        c.drawRect(R.MakeXYWH(rnd.random() * W, rnd.random() * H, 2, 2), paint(WHITE if rnd.random() < 0.5 else (0, 0, 0), a))


def leak(c, k, x=W, y=300, col=(255, 140, 40)):
    if k <= 0: return
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial((x, y), 900, [argb(col, 0.55 * k), argb(col, 0.0)], [0.0, 1.0]))
    c.drawRect(R.MakeWH(W, H), p)


def flash(c, k):
    if k > 0: c.drawRect(R.MakeWH(W, H), paint(WHITE, k))


def tag(c, s, k=1.0, x=90, y=330):
    if k <= 0: return
    f = F(FD + 'Inter-Bold.otf', 30); w = f.measureText(s) + 40
    c.drawRect(R.MakeXYWH(x, y - 40, w * eo(cl(k)), 56), paint(CRED))
    c.save(); c.clipRect(R.MakeXYWH(x, y - 40, w * eo(cl(k)), 56)); c.drawString(s, x + 20, y - 2, f, paint(WHITE)); c.restore()


def big(c, small, bigt, k, y=1250, col=YEL, size=150, sk=None):
    """two-tier cinematic title, truly centred: small Inter line + big Anton line (yellow keyword)."""
    if k <= 0: return
    a = cl(k * 1.6); dy = 30 * (1 - eo(cl(k)))
    if small:
        f = F(FD + 'InterDisplay-Black.otf', 48); s = small
        x = W / 2 - f.measureText(s) / 2
        c.drawString(s, x + 3, y - size - 10 + dy + 3, f, paint((0, 0, 0), 0.6 * a)); c.drawString(s, x, y - size - 10 + dy, f, paint(WHITE, a))
    f = F(ANTON, size); x = W / 2 - f.measureText(bigt) / 2
    c.drawString(bigt, x + 6, y + dy + 6, f, paint((0, 0, 0), 0.65 * a)); c.drawString(bigt, x, y + dy, f, paint(col, a))


def quote(c, s1, s2, k, y=900):
    if k <= 0: return
    a = cl(k * 1.5)
    for i, s in enumerate((s1, s2)):
        f = F(SERIF, 96); x = W / 2 - f.measureText(s) / 2
        c.drawString(s, x + 3, y + i * 110 + 3, f, paint((0, 0, 0), 0.6 * a)); c.drawString(s, x, y + i * 110, f, paint(WHITE if i == 0 else YEL, a * cl(k * 1.5 - i * 0.6)))


def cine_sub(c, t):
    """small clean subtitle: white words, current word yellow, soft shadow."""
    cur = None
    for i, (a, b, ws) in enumerate(SUBS):
        nb = SUBS[i + 1][0] if i + 1 < len(SUBS) else b + 0.6
        if a - 0.05 <= t < min(nb, b + 0.6): cur = ws; break
    if not cur: return
    f = F(FD + 'InterDisplay-Bold.otf', 38); sp = f.measureText(' ')
    ws = [w.upper() for w, _, _ in cur]; tw = sum(f.measureText(w) for w in ws) + sp * (len(ws) - 1)
    x = W / 2 - tw / 2
    for (w, wa, wb), wu in zip(cur, ws):
        on = wa - 0.03 <= t < wb + 0.05
        c.drawString(wu, x + 2, SUBY + 3, f, paint((0, 0, 0), 0.8))
        c.drawString(wu, x, SUBY, f, paint(YEL if on else WHITE, 1.0 if t >= wa - 0.03 else 0.55))
        x += f.measureText(wu) + sp


def credit(c, key, a=0.8):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s' % (cr['author'], cr['license'])).upper()[:70]
    c.save(); c.translate(70, 1360); c.rotate(-90); mono(c, s, 0, 0, 17, (230, 230, 230), a=a); c.restore()


def plane(c, x, y, w, rot, a=1.0):
    if os.path.exists(os.path.join(PK.IMG, 'J4_cut.png')): place(c, 'J4_cut.png', x, y, w, rot=rot, a=a, shadow=True)


def seat(c, x, y, w, rot):
    if os.path.exists(os.path.join(PK.IMG, 'J12_cut.png')): place(c, 'J12_cut.png', x, y, w, rot=rot, shadow=True)


def K(t, t0, d=0.35): return pr(t, t0, d)


# ---------------------------------------------------------------- shots
def s_title(c, t, S):
    ta = ph('and lived'); t1 = S['t1']
    shot(c, 'J3_storm', t, 0, t1, 'night', 1.25, 1.05, 0.5, 0.5, 0.45, 0.5)
    plane(c, lerp(760, 520, eo(K(t, 0, t1))), lerp(420, 760, eo(K(t, 0, t1))), 520, -18 - 20 * K(t, 0, t1), 1.0)
    vignette(c, 0.7); band(c, 950, 1500, 0.8)
    big(c, 'SHE FELL FROM THE SKY', '2 MILES', K(t, 0.0, 0.3), y=1190, size=210, col=WHITE)
    big(c, None, '...AND LIVED.', K(t, ta - 0.1, 0.3), y=1340, size=120, col=YEL)
    flash(c, 0.9 * (1 - K(t, 0.0, 0.25)))
    credit(c, 'J3_storm')


def s_saved(c, t, S):
    tw = ph('what saved her'); tif = ph("if you're ever lost"); tfw = ph('find water'); tfo = ph('and follow it')
    key = 'J8_river' if has('J8_river') else 'J2_river'
    shot(c, key, t, S['t0'], S['t1'], 'jungle', 1.08, 1.22, 0.4, 0.6, 0.5, 0.5)
    vignette(c, 0.6); band(c, 700, 1500, 0.75)
    if t < tif - 0.2:
        big(c, 'WHAT SAVED HER?', 'ONE SENTENCE.', K(t, tw - 0.1), y=1250, size=140)
    else:
        quote(c, '"If you\'re ever lost,', 'find water. Follow it."', K(t, tif - 0.1, 0.5), y=1080)
        tag(c, 'WHAT HER DAD TOLD HER', K(t, tif))
    credit(c, key)


def s_1971(c, t, S):
    tj = ph('juliane koepcke'); tf = ph('flying over the amazon')
    key = 'J7_jungle' if has('J7_jungle') else 'J1_jungle'
    shot(c, key, t, S['t0'], S['t1'], 'jungle', 1.05, 1.25, 0.5, 0.5, 0.55, 0.45)
    k = K(t, tf - 0.4, 3.0)
    plane(c, lerp(1250, -150, k), lerp(520, 420, k), 620, -6, 1.0)
    vignette(c, 0.55); band(c, 1000, 1500, 0.7)
    tag(c, 'DEC 24, 1971 . OVER THE PERUVIAN AMAZON', K(t, S['t0'] + 0.1))
    big(c, 'JULIANE KOEPCKE', 'AGE 17', K(t, tj - 0.1), y=1290, size=150, col=YEL)
    credit(c, key)


def s_strike(c, t, S):
    tl = ph('lightning hits'); tb = ph('breaks apart'); tf = ph('she falls ten thousand'); ts = ph('still strapped')
    if t < tf - 0.2:
        shot(c, 'J3_storm', t, S['t0'], tf, 'night', 1.12, 1.3, 0.5, 0.45, 0.5, 0.4)
        kb = K(t, tb, 1.2)
        if os.path.exists(os.path.join(PK.IMG, 'J4_cut.png')):
            im = img('J4_cut.png', 1600); w = 760; h = w * im.height() / im.width()
            for side in (0, 1):  # the plane splits in two
                c.save(); c.translate(540 + (-1 if side == 0 else 1) * 90 * eo(kb), 760 + 80 * eo(kb) * (1 if side else 0.4))
                c.rotate(-14 + (-10 if side == 0 else 16) * eo(kb))
                c.clipRect(R.MakeXYWH(-w / 2 if side == 0 else -w * 0.02, -h, w * 0.52, 2 * h))
                place(c, 'J4_cut.png', 0, 0, w, rot=0, shadow=False); c.restore()
        if t > tb - 0.1:
            rnd = random.Random(7); u = t - tb + 0.1
            for i in range(40):
                a = rnd.uniform(0, 2 * math.pi); v = rnd.uniform(250, 900); sz = rnd.uniform(8, 34)
                x = 540 + math.cos(a) * v * u; y = 640 + math.sin(a) * v * u + 400 * u * u
                c.save(); c.translate(x, y); c.rotate(u * rnd.uniform(-400, 400))
                col = (255, rnd.randint(120, 200), 40) if i % 3 == 0 else (30, 30, 34)
                c.drawRect(R.MakeXYWH(-sz / 2, -sz / 4, sz, sz / 2), paint(col, max(0, 1 - u / 2.5))); c.restore()
            g = skia.Paint(AntiAlias=True)
            g.setShader(skia.GradientShader.MakeRadial((540, 640), 420, [argb((255, 160, 40), 0.7 * max(0, 1 - u / 1.5)), argb((255, 80, 20), 0.0)], [0.0, 1.0]))
            c.drawRect(R.MakeWH(W, H), g)
        vignette(c, 0.7); band(c, 1000, 1500, 0.8)
        flash(c, 0.95 * (1 - K(t, tl + 0.05, 0.3)) if t > tl else 0)
        if t < tb - 0.1: big(c, 'LIGHTNING HITS', 'THE PLANE', K(t, tl), y=1300, size=160)
        else: big(c, 'IN THE AIR,', 'IT BREAKS APART', K(t, tb - 0.1), y=1300, size=118, col=WHITE)
        credit(c, 'J3_storm')
        return
    # the fall: clouds rush past, seat tumbles
    key = 'J13_storm2' if has('J13_storm2') else 'J3_storm'
    shot(c, key, t, tf, S['t1'], 'night', 1.4, 1.1, 0.5, 0.5, 0.3, 0.7)
    for i in range(14):
        y = (i * 173 + (t - tf) * 2600) % (H + 400) - 200; x = 120 + (i * 331) % 860
        c.drawLine(x, H - y, x, H - y - 220, stroke(WHITE, 4, a=0.35))
    rnd = random.Random(11)
    for i in range(24):
        x = rnd.uniform(150, 930) + 40 * math.sin(t * 2 + i); y = (rnd.uniform(0, H) - (t - tf) * rnd.uniform(500, 1100)) % H
        c.save(); c.translate(x, y); c.rotate(t * rnd.uniform(-300, 300)); sz = rnd.uniform(10, 26)
        c.drawRect(R.MakeXYWH(-sz / 2, -sz / 4, sz, sz / 2), paint((25, 25, 28), 0.9)); c.restore()
    vignette(c, 0.7); band(c, 1000, 1500, 0.8)
    big(c, 'SHE FALLS', '10,000 FEET', K(t, tf - 0.1), y=1190, size=170)
    if t > ts - 0.2: big(c, None, 'STILL STRAPPED TO HER SEAT', K(t, ts - 0.2), y=1320, size=66, col=WHITE)


def s_alone(c, t, S):
    ta = ph('alone in the jungle'); tb = ph('broken collarbone'); to = ph('one shoe'); tc = ph('bag of candy')
    key = 'J14_maggot' if has('J14_maggot') else ('J7_jungle' if has('J7_jungle') else 'J1_jungle')
    shot(c, key, t, S['t0'], S['t1'], 'jungle', 2.6, 2.2, 0.6, 0.55, 0.8, 0.75)
    vignette(c, 0.7); band(c, 950, 1500, 0.8)
    if t < tb - 0.2:
        big(c, 'SHE WAKES UP', 'ALONE.', K(t, ta - 0.1), y=1290, size=190)
    else:
        items = ((tb, 'BROKEN COLLARBONE'), (to, 'ONE SHOE'), (tc, 'A BAG OF CANDY'))
        for i, (t0, s) in enumerate(items):
            k = K(t, t0 - 0.1)
            if k <= 0: continue
            f = F(ANTON, 96); x = W / 2 - f.measureText(s) / 2; y = 1000 + i * 115
            c.drawString(s, x + 5, y + 5, f, paint((0, 0, 0), 0.6 * k)); c.drawString(s, x, y, f, paint(YEL if i == 2 else WHITE, k))
        if has('J9_shoe'):
            if not os.path.exists(os.path.join(PK.IMG, 'J9_cut.png')): pass
            else: place(c, 'J9_cut.png', 780, 640, 380 * eback(cl(K(t, to - 0.1)), 1.4), rot=-10, a=K(t, to - 0.1), shadow=True)
    credit(c, key)


def s_stream(c, t, S):
    tf = ph('finds a stream'); t10 = ph('for ten days'); tm = ph('maggots')
    key = 'J8_river' if has('J8_river') else 'J2_river'
    if t < tm - 0.3:
        shot(c, key, t, S['t0'], tm, 'jungle', 1.9, 2.2, 0.25, 0.45, 0.85, 0.8)
        vignette(c, 0.55); band(c, 950, 1500, 0.75)
        d = 1 + int(9 * cl((t - t10) / 1.2)) if t > t10 else 1
        tag(c, 'DAY %d' % d, K(t, tf))
        big(c, 'SHE FOLLOWS THE WATER', 'FOR 10 DAYS', K(t, tf - 0.1), y=1290, size=150)
        credit(c, key)
        return
    key2 = 'J7_jungle' if has('J7_jungle') else 'J1_jungle'
    shot(c, key2, t, tm - 0.3, S['t1'], 'jungle', 2.4, 2.7, 0.25, 0.3, 0.75, 0.8)
    c.drawRect(R.MakeWH(W, H), paint((40, 60, 20), 0.35))
    vignette(c, 0.85); band(c, 950, 1500, 0.8)
    big(c, 'HER WOUNDS', 'FILL WITH MAGGOTS', K(t, tm - 0.25), y=1290, size=112, col=WHITE)


def s_boat(c, t, S):
    tb = ph('finds a boat'); th = ph('empty hut'); tn = ph('the next day'); tf = ph('and find her')
    if t < tn - 0.2:
        key = 'J8_river' if has('J8_river') else 'J2_river'
        shot(c, key, t, S['t0'], tn, 'cine', 2.0, 1.7, 0.85, 0.8, 0.7, 0.65)
        if os.path.exists(os.path.join(PK.IMG, 'J5_cut.png')): place(c, 'J5_cut.png', 560, 980, 640 * eback(cl(K(t, tb - 0.1)), 1.3), rot=-4, a=K(t, tb - 0.1), shadow=True)
        vignette(c, 0.55); band(c, 1000, 1500, 0.75)
        tag(c, 'DAY 10', K(t, S['t0']))
        big(c, 'A BOAT.', 'AN EMPTY HUT.', K(t, tb - 0.1), y=1300, size=150)
        credit(c, key)
        return
    key = 'J6_hut' if has('J6_hut') else 'J7_jungle'
    shot(c, key, t, tn - 0.2, S['t1'], 'cine', 2.2, 2.5, 0.8, 0.75, 0.45, 0.4)
    leak(c, K(t, tf - 0.2, 0.8), x=200, y=500, col=(255, 170, 60))
    vignette(c, 0.55); band(c, 1000, 1500, 0.75)
    tag(c, 'DAY 11', K(t, tn))
    big(c, 'THE NEXT DAY...', 'THEY FIND HER.', K(t, tf - 0.3), y=1300, size=150)
    credit(c, key)


def s_92(c, t, S):
    t92 = ph('ninety two people'); to = ph('only survivor')
    c.drawRect(R.MakeWH(W, H), paint((10, 10, 12)))
    leak(c, 0.35, x=W / 2, y=760, col=(255, 200, 80))
    cols, sp = 10, 74; x0 = W / 2 - (cols - 1) * sp / 2; y0 = 420
    lit = 47
    for i in range(92):
        k = K(t, t92 - 0.2 + i * 0.012, 0.2)
        if k <= 0: continue
        x = x0 + (i % cols) * sp; y = y0 + (i // cols) * sp
        dim = t > to - 0.3 and i != lit
        col = (70, 70, 70) if dim else (WHITE if i != lit else YEL)
        r = 22 if i != lit or t < to - 0.3 else 22 + 10 * K(t, to - 0.3, 0.4)
        c.drawCircle(x, y, r * eback(k, 1.5), paint(col))
    big(c, None, '92 ON BOARD.', K(t, t92), y=1200, size=140, col=WHITE)
    if t > to - 0.4: big(c, None, '1 SURVIVOR.', K(t, to - 0.4), y=1350, size=140, col=YEL)


def s_ask(c, t, S):
    key = 'J7_jungle' if has('J7_jungle') else 'J1_jungle'
    shot(c, key, t, S['t0'], DURATION, 'night', 1.1, 1.35, 0.5, 0.5, 0.5, 0.5)
    vignette(c, 0.85); band(c, 900, 1500, 0.85)
    big(c, 'WOULD YOU HAVE', 'MADE IT OUT?', K(t, S['t0'] + 0.1), y=1260, size=160)
    cta = 'SUBSCRIBE FOR MORE TRUE STORIES' if PLAT == 'yt' else 'SEND THIS TO SOMEONE WHO WOULD SURVIVE'
    f = F(FD + 'Inter-Bold.otf', 34); c.drawString(cta, W / 2 - f.measureText(cta) / 2, 1360, f, paint(WHITE, K(t, END - 0.6)))
    if t > END + 0.4: c.drawRect(R.MakeWH(W, H), paint((0, 0, 0), K(t, END + 0.4, 1.0)))


def wrap(fn):
    def f(c, t, S):
        fn(c, t, S)
        grain(c, t)
        if t < END + 0.2: cine_sub(c, t)
    return f


def _sc():
    raw = [('title', 0.0, s_title), ('saved', ph('and what saved her') - 0.1, s_saved), ('1971', ph('christmas eve') - 0.1, s_1971),
           ('strike', ph('when lightning hits') - 0.15, s_strike), ('alone', ph('she wakes up') - 0.1, s_alone),
           ('stream', ph('so she finds a stream') - 0.1, s_stream), ('boat', ph('on day ten') - 0.1, s_boat),
           ('n92', ph('ninety two people') - 0.15, s_92), ('ask', ph('would you have made') - 0.1, s_ask)]
    out = []
    for i, (k, t0, fn) in enumerate(raw):
        t1 = raw[i + 1][1] if i + 1 < len(raw) else DURATION
        out.append(dict(k=k, t0=t0, t1=t1, fn=wrap(fn)))
    return out


SCENES = _sc()
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('lightning hits'), 16, 0.4)
EP.shk(ph('breaks apart'), 10, 0.35)
EP.shk(ph('she falls ten thousand'), 8, 0.6)

if __name__ == '__main__':
    EP.main(sys.argv)
