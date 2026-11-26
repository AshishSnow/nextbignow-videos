import sys, os, json, math
sys.path.insert(0, '/home/claude/docu')
from kit import *
import cv2
D = '/home/claude/docu'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.35; TOTAL = END + 1.8
def wt(i, frac): return S[i] + L[i]['dur'] * frac
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); return wt(i, k / max(1, len(tx)))
exec(open(D + '/common_part.py').read())

MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
OFF = (240, 238, 233); REDc = rgb(RED)

# ---------------------------------------------------------------- photo engine
PH = {}
def graded(name):
    """cover-crop to 1.3x frame, documentary grade: lower sat, teal shadows / warm highlights, contrast."""
    if name in PH: return PH[name]
    im = Image.open(f'{D}/ph/{name}.jpg').convert('RGB')
    tw, th = int(W * 1.3), int(H * 1.3); fx, fy = FOCUS.get(name, (.5, .5))
    s = max(tw / im.width, th / im.height); im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x0 = int((im.width - tw) * fx); y0 = int((im.height - th) * fy); im = im.crop((x0, y0, x0 + tw, y0 + th))
    a = np.asarray(im).astype(np.float32) / 255
    g = a.mean(2, keepdims=True); a = g + (a - g) * .88
    a = np.clip((a - .5) * 1.14 + .5, 0, 1)
    lum = a.mean(2, keepdims=True)
    a = a + (1 - lum) * np.array([-.02, .015, .035]) * 1.0 + lum * np.array([.035, .012, -.03])
    a = np.clip(a * .97 + .015, 0, 1)
    PH[name] = (a * 255).astype(np.uint8); return PH[name]

def shot(fr, name, lt, dur, z0=1.0, z1=1.12, px=0.0, py=0.0, dim=0.0):
    """Ken-Burns push. lt = local time, z = zoom, px/py = pan in px over the shot."""
    src = graded(name); u = ease(clamp(lt / max(dur, .01))) * .8 + clamp(lt / max(dur, .01)) * .2
    z = lerp(z0, z1, u); h, w = src.shape[:2]
    cw, ch = w / (1.3 * z), h / (1.3 * z)
    cx = w / 2 + px * u; cy = h / 2 + py * u
    x0 = clamp(cx - cw / 2, 0, w - cw); y0 = clamp(cy - ch / 2, 0, h - ch)
    M = np.float32([[W / cw, 0, -x0 * W / cw], [0, H / ch, -y0 * H / ch]])
    fr[:] = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if dim: fr[:] = (fr * (1 - dim)).astype(np.uint8)

def card(fr, name, cx, cy, w, h, t, rot=0.0, z=1.0):
    """small photo card with soft shadow (paper-slide style)."""
    if t <= 0: return
    src = graded(name); s = max(w / src.shape[1], h / src.shape[0]) * 1.02
    im = cv2.resize(src, (int(src.shape[1] * s), int(src.shape[0] * s)), interpolation=cv2.INTER_AREA)
    y0 = (im.shape[0] - h) // 2; x0 = (im.shape[1] - w) // 2; im = im[y0:y0 + h, x0:x0 + w]
    pad = 40; rg = np.zeros((h + pad * 2, w + pad * 2, 4), np.uint8)
    sh = np.zeros((h + pad * 2, w + pad * 2), np.uint8); sh[pad + 14:pad + h + 14, pad + 6:pad + w + 6] = 120
    sh = cv2.GaussianBlur(sh, (0, 0), 14); rg[..., 3] = sh
    rg[pad:pad + h, pad:pad + w, :3] = im; rg[pad:pad + h, pad:pad + w, 3] = 255
    p = eout(clamp(t / .35)); put_rgba(fr, rg, cx, cy + 40 * (1 - p), z * (.92 + .08 * p), p, rot)

# ---------------------------------------------------------------- type
def txt_img(s, font, size, fill=(255, 255, 255), shadow=True, track=0, var=None):
    f = ImageFont.truetype(font, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] if ch != ' ' else size * .28 for ch in s]
    bb = f.getbbox(s); tw = int(sum(widths) + track * (len(s) - 1) + 20) if track else bb[2] - bb[0] + 20
    th = int(size * 1.4); pad = 30
    im = Image.new('RGBA', (tw + pad * 2, th + pad * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if track:
        x = pad
        for ch, wd in zip(s, widths):
            if shadow: d.text((x + 3, pad + 4), ch, font=f, fill=(0, 0, 0, 150))
            d.text((x, pad), ch, font=f, fill=fill); x += wd + track
    else:
        if shadow: d.text((pad - bb[0] + 3, pad + 4), s, font=f, fill=(0, 0, 0, 150))
        d.text((pad - bb[0], pad), s, font=f, fill=fill)
    a = np.array(im)
    if shadow: a[..., 3] = np.maximum(a[..., 3], (cv2.GaussianBlur(a[..., 3], (0, 0), 6) * .5).astype(np.uint8))
    return a

TI = {}
def word(fr, s, cx, cy, size=46, font=INTER, fill=(255, 255, 255), shadow=True, a=1.0, sc=1.0, var='Medium', rot=0.0):
    k = (s, size, font, fill, shadow, var)
    if k not in TI: TI[k] = txt_img(s, font, size, fill, shadow, var=var)
    put_rgba(fr, TI[k], cx, cy, sc, a, rot)

def hero(fr, s, cx, cy, t, size=230, fill=(255, 255, 255), shadow=True, rot=0.0):
    """big condensed word: punches in from 1.25x with a fast fade (ref: 'COLLAPSE', 'EARTH')."""
    if t <= 0: return
    p = eout(clamp(t / .18)); word(fr, s, cx, cy, size, ANTON, fill, shadow, p, 1.25 - .25 * p, None, rot)

def capword(fr, T, y=1250, dark=False, lines=None):
    """ONE word at a time, small, centred - the reference's signature caption."""
    for i, l in enumerate(L):
        if lines is not None and i not in lines: continue
        if S[i] - .02 <= T < E[i] + .05:
            tx = l['text']; ws = tx.split(); p = 0; cur = None
            for w_ in ws:
                k = tx.find(w_, p); p = k + len(w_)
                if wt(i, k / len(tx)) - .03 <= T: cur = w_
            if cur:
                cur = cur.strip('.,?')
                word(fr, cur, CX, y, 50, INTER, (20, 20, 20) if dark else (255, 255, 255), not dark, 1.0, 1.0, 'Medium')
            return

def typewriter(fr, s, cx, cy, t, cps=16, size=50, col=(235, 235, 235), cursor=True):
    """mono text typed char by char + blinking block cursor (ref: 'Got bailed out', '15 years later...|')."""
    if t <= 0: return
    n = int(clamp(t * cps, 0, len(s))); sub = s[:n]
    f = ImageFont.truetype(MONO, size); cw = f.getbbox('M')[2]
    x0 = cx - cw * len(s) / 2
    if sub: word(fr, sub, int(x0 + cw * len(sub) / 2), cy, size, MONO, col, False, 1.0, 1.0, None)
    if cursor and (n < len(s) or int(t * 2.2) % 2 == 0):
        xx = int(x0 + cw * n + 6); fr[cy - size // 2:cy + size // 2 + 4, xx:xx + 6] = col

def tag(fr, s, cx, cy, t, bgc=REDc, fg=(255, 255, 255), size=40):
    """red name/location strap (ref: 'JAMIE DIMON')."""
    if t <= 0: return
    f = ImageFont.truetype(ANTON, size); bb = f.getbbox(s); w = bb[2] - bb[0] + 44; h = int(size * 1.45)
    p = eout(clamp(t / .25)); ww = max(2, int(w * p))
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rectangle((0, 0, ww, h), fill=bgc + (255,))
    if p > .6: d.text((22 - bb[0], h / 2), s, font=f, fill=fg + (255,), anchor='lm')
    put_rgba(fr, np.array(im), cx, cy, 1.0, 1.0, 0)

def paper_bg(fr, T):
    fr[:] = OFF; g = GRAIN[int(T * 24) % len(GRAIN)] * .5
    fr[:] = np.clip(fr.astype(np.int16) + (g[..., None] * .5).astype(np.int16), 0, 255).astype(np.uint8)

def black_bg(fr, T, name=None, dim=.82, lt=0, dur=3):
    if name: shot(fr, name, lt, dur, 1.05, 1.1, dim=dim)
    else: fr[:] = 12

def highlight_doc(fr, T, t0, lines, hl, hl_t):
    """typed case-file card on paper, yellow marker sweeps across one line (ref: 'fortress balance sheet')."""
    paper_bg(fr, T); f = ImageFont.truetype(MONO, 40)
    im = Image.new('RGBA', (900, 120 + 70 * len(lines)), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    for k, s in enumerate(lines):
        y = 60 + 70 * k
        if k == hl:
            w = f.getbbox(s)[2] + 24; pp = ease(clamp((T - hl_t) / .5))
            if pp > 0: d.rectangle((40, y - 6, 40 + w * pp, y + 50), fill=(255, 214, 10, 255))
        d.text((52, y), s, font=f, fill=(25, 25, 25, 255))
    a = np.array(im); sh = np.zeros((a.shape[0] + 80, a.shape[1] + 80, 4), np.uint8)
    sh[40 + 14:40 + 14 + a.shape[0], 40 + 6:40 + 6 + a.shape[1], 3] = 90; sh[..., 3] = cv2.GaussianBlur(sh[..., 3], (0, 0), 16)
    sh[40:40 + a.shape[0], 40:40 + a.shape[1]] = a
    p = eout(clamp((T - t0) / .4)); put_rgba(fr, sh, CX, 900 + 60 * (1 - p), 1.0 + .03 * (T - t0), p, -1.5)

def flip_counter(fr, T, t0, a, b, cy=900, dur=.9):
    """flip-clock style year roll (ref: 1997 / 2004 / 2007)."""
    if T < t0: return
    u = clamp((T - t0) / dur); val = int(round(lerp(a, b, ease(u))))
    w, h = 700, 380; im = np.full((h, w, 3), (232, 232, 228), np.uint8)
    cv2.line(im, (0, h // 2), (w, h // 2), (150, 150, 150), 4)
    blur = 1 - u
    t_ = txt_img(str(val), ANTON, 300, (24, 24, 24), False)
    canvas = np.zeros((h, w, 4), np.uint8); canvas[..., :3] = im; canvas[..., 3] = 255
    th, tw = t_.shape[:2]; y0 = (h - th) // 2 + 10; x0 = (w - tw) // 2
    reg = canvas[max(0, y0):y0 + th, max(0, x0):x0 + tw]; tt = t_[:reg.shape[0], :reg.shape[1]]
    al = tt[..., 3:4] / 255; reg[..., :3] = (reg[..., :3] * (1 - al) + tt[..., :3] * al).astype(np.uint8)
    if blur > .05: canvas[..., :3] = cv2.GaussianBlur(canvas[..., :3], (1, int(blur * 40) * 2 + 1), 0)
    for xx in (180, 520): cv2.rectangle(canvas, (xx - 14, h - 30), (xx + 14, h + 10), (30, 30, 30, 255), -1)
    put_rgba(fr, canvas, CX, cy, 1.0, eout(clamp((T - t0) / .2)), 0)

# ---------------------------------------------------------------- transitions / finish
GRAIN = [(np.random.RandomState(k).randn(H // 2, W // 2) * 4.5).repeat(2, 0).repeat(2, 1).astype(np.float32) for k in range(6)]
VIG = None
def finish(fr, T, strength=1.0):
    global VIG
    if VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - CX) / W) ** 2 + ((yy - H / 2) / H) ** 2 * .8)
        VIG = np.clip(1 - (r - .28) * 1.1, .45, 1).astype(np.float32)[..., None]
    g = GRAIN[int(T * 8) % len(GRAIN)][..., None]
    fr[:] = np.clip(fr * VIG + g * strength, 0, 255).astype(np.uint8)

def whip(fr, k, dx=1):
    """horizontal motion-blur smear at a cut."""
    if k <= 0: return
    n = int(10 + 90 * k) | 1; ker = np.zeros((1, n), np.float32); ker[0] = 1 / n
    fr[:] = cv2.filter2D(fr, -1, ker); fr[:] = np.roll(fr, int(dx * 120 * k), 1)

def glitch(fr, T, k):
    """RGB split + slice offsets (ref glitch cuts)."""
    if k <= 0: return
    o = int(24 * k); r = np.roll(fr[..., 0], o, 1); b = np.roll(fr[..., 2], -o, 1); fr[..., 0] = r; fr[..., 2] = b
    rs = np.random.RandomState(int(T * 60))
    for _ in range(int(6 * k)):
        y = rs.randint(0, H - 80); h = rs.randint(10, 80); fr[y:y + h] = np.roll(fr[y:y + h], rs.randint(-90, 90), 1)

CUTS = []  # (time, kind)
def trans(fr, T):
    for t, kind in CUTS:
        d = T - t
        if -.1 < d < .1:
            k = 1 - abs(d) / .1
            if kind == 'whip': whip(fr, k, 1 if d < 0 else 1)
            elif kind == 'glitch': glitch(fr, T, k)
            elif kind == 'flash': fr[:] = np.clip(fr + 255 * k * .8, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------- timeline
FOCUS = {'hull2': (.15, .65), 'wreck': (.5, .6), 'coast2': (.8, .5)}
def T_(i, w): return wfind(i, w)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8); cap = True; dark = False
    if T < S[1]:                                         # L0 hook: wreck photo + text hook from frame 1
        shot(fr, 'wreck', T, S[1], 1.18, 1.3, 0, 40)
        t1 = T + .5
        hero(fr, 'ITS TAR KEPT', CX, 640, t1, 150)
        p = eout(clamp(t1 / .25)); fr[738:900, 210:870] = (fr[738:900, 210:870] * (1 - p) + np.array(REDc) * p).astype(np.uint8)
        hero(fr, 'A SECRET', CX, 812, t1, 150)
        tag(fr, 'SANK ~2,200 YEARS AGO', CX, 1010, T - T_(0, 'twenty') + .1, size=38)
    elif T < S[2]:                                       # L1 paper slide, sparse words + photo card
        paper_bg(fr, T); lt = T - S[1]; dark = True; cap = False
        card(fr, 'hull', CX, 960, 430, 300, lt - .05, -2)
        for w_, x, y in (('its', 250, 700), ('tar', 830, 700), ('remembers', 330, 1220), ('where', 790, 1220)):
            if T > T_(1, w_) - .03: word(fr, w_, x, y, 58, INTER, (25, 25, 25), False, 1.0, 1.0, 'Medium')
        if T > T_(1, 'fixed') - .05: hero(fr, 'FIXED.', CX, 1420, T - T_(1, 'fixed') + .05, 170, (25, 25, 25), False)
    elif T < S[3]:                                       # L2 typewriter -> coast -> flip year
        lt = T - S[2]; tc = T_(2, 'wreck') - .1
        if T < T_(2, 'off') - .05:
            black_bg(fr, T); typewriter(fr, 'divers found the wreck...', CX, 960, lt, 22, 52); cap = False
        else:
            shot(fr, 'coast', T - T_(2, 'off'), 3.0, 1.0, 1.12, 50, 0)
            tag(fr, 'ADRIATIC SEA  /  CROATIA', CX, 760, T - T_(2, 'croatia'), size=40)
            flip_counter(fr, T, T_(2, '2016') - .35, 1987, 2016, 1000, .8)
    elif T < S[4]:                                       # L3 split screen: hull / resin -> beeswax
        lt = T - S[3]; top = np.zeros_like(fr); bot = np.zeros_like(fr)
        shot(top, 'hull2', lt, 6, 1.3, 1.45, -40, 0); shot(bot, 'wax' if T > T_(3, 'beeswax') - .05 else 'resin', lt, 6, 1.0, 1.15, 40, 0)
        sp = eout(clamp(lt / .35)); half = H // 2
        fr[:half] = top[H // 4:H // 4 + half]; fr[half:] = bot[H // 4:H // 4 + half]
        fr[half - 6:half + 6] = OFF
        if sp < 1: fr[:] = np.roll(fr, int((1 - sp) * W), 1) if False else fr
        if T > T_(3, 'pine'): hero(fr, 'PINE TAR', CX, half - 170, T - T_(3, 'pine'), 190)
        if T > T_(3, 'beeswax'): hero(fr, '+ BEESWAX', CX, half + 230, T - T_(3, 'beeswax'), 170, rgb(YEL))
    elif T < S[5]:                                       # L4 pollen SEM, strong push + red hero
        lt = T - S[4]; shot(fr, 'pollen', lt, S[5] - S[4], 1.0, 1.4)
        if T > T_(4, 'pollen'): hero(fr, 'POLLEN', CX, 800, T - T_(4, 'pollen'), 260, REDc)
        if T < T_(4, 'tiny') - .05: fr[:] = (fr * .35).astype(np.uint8); typewriter(fr, 'stuck inside?', CX, 960, lt, 18, 52); cap = False
    elif T < S[6]:                                       # L5 share moment: paper + typewriter
        paper_bg(fr, T); lt = T - S[5]; dark = True; cap = False
        hero(fr, 'TAG', CX, 760, lt + .05, 280, (25, 25, 25), False)
        typewriter(fr, 'the friend who leaves', CX, 1000, T - T_(5, 'friend') + .2, 26, 46, (25, 25, 25))
        typewriter(fr, 'fingerprints on everything', CX, 1080, T - T_(5, 'fingerprints'), 26, 46, (25, 25, 25))
    elif T < S[7]:                                       # L6 highlighted case file -> Italy / Croatia split
        lt = T - S[6]; ti = T_(6, 'some near italy') - .05
        if T < ti:
            highlight_doc(fr, T, S[6] - .05, ['WRECK: ILOVIK-PARZINE 1', 'COATING SAMPLES: 10', 'MAIN: PINE TAR (+BEESWAX)', 'BATCHES: 4 OR 5'], 3, T_(6, 'four'))
            dark = True
        else:
            top = np.zeros_like(fr); bot = np.zeros_like(fr); half = H // 2
            shot(top, 'brindisi', T - ti, 4, 1.05, 1.15, 30, 0); fr[:half] = top[H // 4:H // 4 + half]
            tag(fr, 'NEAR ITALY', CX, 620, T - ti, size=46)
            tc = T_(6, 'some near croatia') - .05
            if T > tc:
                shot(bot, 'coast2', T - tc, 3, 1.05, 1.15, -30, 0); fr[half:] = bot[H // 4:H // 4 + half]; fr[half - 6:half + 6] = OFF
                tag(fr, 'NEAR CROATIA', CX, 1110, T - tc, size=46)
            else: fr[half:] = 12
    elif T < S[8]:                                       # L7 black typewriter
        black_bg(fr, T); typewriter(fr, 'exact spots:', CX, 900, T - S[7], 20, 56); cap = False
        typewriter(fr, 'still a mystery.', CX, 990, T - T_(7, 'still'), 20, 56, rgb(RED))
    elif T < END:                                        # L8 payoff: mosaic ship, push in
        lt = T - S[8]; shot(fr, 'mosaic', lt, END - S[8], 1.0, 1.2, 0, 40)
        if T > T_(8, 'gone'): fr[:] = (fr * (1 - .35 * clamp((T - T_(8, 'gone')) / .4))).astype(np.uint8)
        if T > T_(8, 'repair'):
            hero(fr, 'REPAIR', CX, 700, T - T_(8, 'repair'), 210)
            hero(fr, 'RECEIPTS', CX, 890, T - T_(8, 'receipts'), 230, rgb(YEL))
        if T > T_(8, 'survived'): tag(fr, 'STILL SEALED IN THE TAR', CX, 1060, T - T_(8, 'survived'), size=40)
    else:                                                # end card
        paper_bg(fr, T); lt = T - END; cap = False
        big = Image.open('/home/claude/nextbignow-videos/NextBigNow_logo_transparent.png').convert('RGBA'); big.thumbnail((360, 360))
        put_rgba(fr, np.array(big), CX, 820, eout(clamp(lt / .3)), 1.0, 0)
        if plat == 'ig':
            typewriter(fr, 'send this to someone', CX, 1100, lt - .2, 30, 46, (25, 25, 25), False)
            typewriter(fr, 'who loves history.', CX, 1170, lt - .6, 30, 46, rgb(RED))
        else:
            typewriter(fr, 'subscribe for', CX, 1100, lt - .2, 30, 46, (25, 25, 25), False)
            typewriter(fr, 'what happens next.', CX, 1170, lt - .6, 30, 46, rgb(RED))
        finish(fr, T, .6); return fr
    if cap: capword(fr, T, 1300, dark)
    trans(fr, T)
    finish(fr, T, .6 if dark else 1.0)
    if T < END: credit(fr, CREDIT)
    logo(fr)
    return fr

CREDIT = 'Research: Charrie-Duhaut et al., Frontiers in Materials (2026). Photos: Wikimedia Commons (see caption).'
def setup_cuts():
    CUTS[:] = [(S[1], 'whip'), (S[2], 'glitch'), (T_(2, 'off') - .05, 'flash'), (S[3], 'whip'), (T_(3, 'beeswax') - .05, 'glitch'),
               (S[4], 'glitch'), (T_(4, 'tiny') - .05, 'flash'), (S[5], 'whip'), (S[6], 'whip'), (T_(6, 'some near italy') - .05, 'glitch'),
               (S[7], 'glitch'), (S[8], 'whip'), (END, 'flash')]
setup_cuts()

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
