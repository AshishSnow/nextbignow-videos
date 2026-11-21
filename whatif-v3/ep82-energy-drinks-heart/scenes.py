import sys, os, json, math
sys.path.insert(0, '/home/claude/energy')
from kit import *
D = '/home/claude/energy'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 1.6
def wt(i, frac): return S[i] + L[i]['dur'] * frac
def wfind(i, word):
    tx = L[i]['text'].lower(); k = tx.find(word.lower()); return wt(i, k / max(1, len(tx)))
def st(name, **kw):
    return load_st(name, **kw) if os.path.exists(f'{D}/st/{name}.png') else None
PHOTO = {}
def photo(name, w, h, focus=(.5, .5)):
    k = (name, w, h, focus)
    if k not in PHOTO:
        p = f'{D}/ph/{name}.jpg'
        PHOTO[k] = panel_img(comic_photo(p, w, h, focus)) if os.path.exists(p) else None
    return PHOTO[k]
exec(open(D + '/common_part.py').read())
def chip(fr, txt, cx, cy, t, col=CYAN, size=40, rot=0): tape(fr, txt, cx, cy, t, col=col, size=size, font=INTER, rot=rot)
def sk(fr, im, x, y, T, k, sc, rot=0, t=1.0):
    if im is not None: sticker(fr, im, x, y, T, k, sc, rot, t)
def stat(fr, big, small, cx, cy, t, col=RED, rot=-3, size=130):
    if t <= 0: return
    title(fr, big, cy, t, size=size, fill='FFFFFF' if col == RED else YEL, rot=rot, cx=cx)
    tape(fr, small, cx, cy + size * .8, t - .1, col=col, size=40, font=LUCKY, rot=rot + 1, tcol='FFFFFF' if col == RED else '1C1614')


def bg(fr, T, tint='F2E6CF', m=.55): fr[:] = paper(tint, m)

def drawn_can(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); w, h = 150 * s, 290 * s
    c.rectangle(-w / 2 + 10, -h / 2 + 12, w, h); c.set_source_rgba(0, 0, 0, .3); c.fill()
    g = cairo.LinearGradient(-w / 2, 0, w / 2, 0)
    for o, col in ((0, '7A1010'), (.35, 'E23B3B'), (.5, 'FF8A8A'), (.7, 'D42A2A'), (1, '5E0B0B')): g.add_color_stop_rgb(o, *rgb(col)[:3] if False else [v / 255 for v in rgb(col)])
    c.rectangle(-w / 2, -h / 2, w, h); c.set_source(g); c.fill()
    for yy in (-h / 2, h / 2 - 22 * s):
        c.rectangle(-w / 2, yy, w, 22 * s); c.set_source_rgba(.82, .84, .86, 1); c.fill()
    c.save(); c.rotate(-math.pi / 2); c.select_font_face('Luckiest Guy'); c.set_font_size(64 * s)
    ext = c.text_extents('ENERGY'); c.move_to(-ext.width / 2, 22 * s); c.set_source_rgba(1, .85, .2, 1); c.show_text('ENERGY'); c.restore()
    c.rectangle(-w / 2, -h / 2, w, h); c.set_source_rgba(*hx('1C1614')); c.set_line_width(7); c.stroke()
    c.restore()

def can(fr, x, y, T, s=1.0, rot=0.0, t=1.0):
    sc = back(clamp(t / .35))
    if sc <= 0: return
    overlay(fr, cairo_layer(lambda c: drawn_can(c, x, y + 6 * math.sin(T * 2), s * sc, rot)))

def ecg(fr, T, y=1500, flat_at=None, col=GREEN, alpha=1.0):
    def dr(c):
        c.rectangle(60, y - 60, W - 120, 120); c.set_source_rgba(.07, .09, .1, .85 * alpha); c.fill()
        x0 = 70; ph = T * 220
        c.move_to(x0, y)
        for x in range(x0, W - 70, 4):
            u = ((x + ph) % 260) / 260
            v = 0
            if flat_at is None or T < flat_at or x < 70 + (W - 140) * clamp((T - flat_at) / .2) * 0:
                if .40 < u < .43: v = -15
                elif .45 < u < .47: v = 45
                elif .47 < u < .50: v = -50
                elif .50 < u < .52: v = 20
            c.line_to(x, y + v)
        c.set_source_rgba(*hx(col if flat_at is None or T < flat_at else RED)); c.set_line_width(5); c.stroke()
    overlay(fr, cairo_layer(dr))

def bars(fr, T, items, t0s, cy=1080, mx=11.0):
    def dr(c):
        base = cy + 240; h0 = 380
        for k, (lab, v, col) in enumerate(items):
            if T < t0s[k]: continue
            u = eout(clamp((T - t0s[k]) / .8)); x = 200 + k * 340; hh = h0 * v / mx * u
            c.rectangle(x - 90 + 10, base - hh + 10, 180, hh); c.set_source_rgba(0, 0, 0, .3); c.fill()
            c.rectangle(x - 90, base - hh, 180, hh); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
        c.move_to(80, base); c.line_to(W - 80, base); ink(c, 7); c.stroke()
    overlay(fr, cairo_layer(dr))
    for k, (lab, v, col) in enumerate(items):
        if T < t0s[k]: continue
        u = eout(clamp((T - t0s[k]) / .8)); x = 200 + k * 340
        chip(fr, lab, x, cy + 295, T - t0s[k], 'FFFFFF', 30, 0)
        title(fr, f'{v * u:.1f}x' if v % 1 else f'{int(v * u)}x', cy + 240 - 380 * v / mx * u - 55, T - t0s[k], size=70, fill=YEL, cx=x)

def s_hook(fr, T):
    bg(fr, T, 'F7D9C4'); rays(fr, T, 'FFFFFF', .14)
    s_ = st('can', h=620)
    if s_ is not None: put_rgba(fr, s_, CX, 1030, back(clamp(T / .35)), 1.0, -6 + 2 * math.sin(T * 2))
    else: can(fr, CX, 1030, T, 1.8, -.1, T)
    tape(fr, 'THE ENERGY DRINK IN YOUR HAND', CX, 470, T, col='FFFFFF', size=48, font=LUCKY, rot=-2)
    tf = wfind(0, 'flagged')
    if T > tf - .2: xstamp(fr, CX, 1030, T - tf + .2, 1.1); title(fr, 'FLAGGED', 620, T - tf + .2, size=140, fill=RED)

def s_heart(fr, T):
    lt = T - S[1]; bg(fr, T, 'F2C4B8')
    chip(fr, 'SUGAR', 280, 720, lt, 'FFFFFF', 54, -4)
    if lt > .3: xstamp(fr, 280, 720, lt - .3, .6)
    s_ = st('heart', w=560)
    th = wfind(1, 'heart')
    if s_ is not None and lt > .2: put_rgba(fr, s_, 640, 1080, back(clamp((lt - .2) / .3)) * (1 + .04 * math.sin(T * 9)), 1.0, 4)
    if T > th - .3: title(fr, 'YOUR HEART', 600, T - th + .3, size=120, fill=YEL)
    ecg(fr, T, 1330, alpha=.9)

def s_reports(fr, T):
    lt = T - S[2]; bg(fr, T, 'E8E1D0')
    def papers(c):
        for k in range(14):
            t_ = lt - k * .12
            if t_ < 0: continue
            u = eout(clamp(t_ / .4)); x = CX + (k % 5 - 2) * 60 + 20 * math.sin(k); y = lerp(-200, 1050 - k * 12, u)
            c.save(); c.translate(x, y); c.rotate(.2 * math.sin(k * 3))
            c.rectangle(-170 + 8, -220 + 10, 340, 440); c.set_source_rgba(0, 0, 0, .25); c.fill()
            c.rectangle(-170, -220, 340, 440); c.set_source_rgba(*hx('FFFDF5')); c.fill_preserve(); ink(c, 5); c.stroke()
            for r in range(8):
                c.rectangle(-130, -160 + r * 42, 260 - (r % 3) * 50, 12); c.set_source_rgba(*hx('1C1614', .22)); c.fill()
            c.rectangle(-130, -200, 120, 22); c.set_source_rgba(*hx(RED)); c.fill(); c.restore()
    overlay(fr, cairo_layer(papers))
    tape(fr, 'FDA SAFETY REPORTS', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    if T > wfind(2, 'nine'): chip(fr, '9 YEARS: 2017-2025', CX, 720, T - wfind(2, 'nine'), CYAN, 42, 2)
    tw = wfind(2, 'twenty')
    if T > tw:
        v = int(28345 * eout(clamp((T - tw) / 1.0))); title(fr, f'{v:,}', 600, T - tw, size=140, fill=YEL)

def s_bars(fr, T):
    lt = T - S[3]; bg(fr, T, 'F2E6CF'); rays(fr, T, 'FFFFFF', .08)
    tape(fr, 'ENERGY DRINKS + STIMULANTS', CX, 470, T - S[3], col=RED, size=50, font=LUCKY, rot=-2, tcol='FFFFFF')
    t1 = wfind(3, 'heart attacks'); t2 = wfind(4, 'eleven')
    items = [('OTHER FOODS', 1, 'CCCCCC'), ('HEART ATTACK', 4.5, YEL), ('CARDIAC ARREST', 11, RED)]
    bars(fr, T, items, [S[3] + .3, t1, t2], cy=1040)
    if T > S[4]:
        title(fr, 'CARDIAC ARREST?', 600, T - S[4], size=104, fill='FFFFFF')
    ts = wfind(4, 'stops')
    ecg(fr, T, 745, flat_at=ts)
    if T > ts:
        a = clamp((T - ts) / .25) * .45
        fr[:] = (fr.astype(np.float32) * (1 - a)).astype(np.uint8)
        title(fr, 'STOPS.', 1000, T - ts, size=170, fill=RED)

def s_age(fr, T):
    lt = T - S[5]; bg(fr, T, 'C9DDF0')
    def pie(c):
        u = eout(clamp((lt - .3) / 1.0)); x, y, r = CX, 1050, 300
        c.arc(x + 10, y + 12, r, 0, 2 * math.pi); c.set_source_rgba(0, 0, 0, .3); c.fill()
        c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(*hx('FFFFFF')); c.fill()
        c.move_to(x, y); c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * .45 * u); c.close_path(); c.set_source_rgba(*hx(RED)); c.fill()
        c.arc(x, y, r, 0, 2 * math.pi); ink(c, 8); c.stroke()
    overlay(fr, cairo_layer(pie))
    tape(fr, 'ALMOST HALF THE HEART REPORTS', CX, 470, lt, col='FFFFFF', size=48, font=LUCKY, rot=-2)
    te = wfind(5, 'eighteen')
    if T > te: title(fr, 'AGES 18-34', 620, T - te, size=120, fill=YEL); burst(fr, '45%', 800, 1300, T - te - .2, r=115, col=YEL, size=60, rot=8)

def s_proof(fr, T):
    lt = T - S[6]; bg(fr, T, 'E8E1D0')
    can(fr, 330, 1050, T, 1.4, -.12, lt)
    s_ = st('heart', w=380)
    if s_ is not None: put_rgba(fr, s_, 760, 1050, back(clamp(lt / .35)), 1.0, 6)
    def q(c):
        u = clamp((lt - .5) / .6); c.set_dash([22, 16]); c.move_to(450, 1050); c.line_to(450 + 160 * u, 1050)
        c.set_source_rgba(*hx('1C1614')); c.set_line_width(8); c.stroke(); c.set_dash([])
    overlay(fr, cairo_layer(q))
    burst(fr, '?', 540, 900, lt - 1.0, r=80, col=YEL, size=90)
    tape(fr, "REPORTS AREN'T PROOF", CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(6, 'nobody'): title(fr, 'A LINK, NOT A CAUSE', 610, T - wfind(6, 'nobody'), size=96, fill=YEL)

def s_caff(fr, T):
    lt = T - S[7]; bg(fr, T, 'F7D9C4'); rays(fr, T, 'FFFFFF', .1)
    can(fr, 250, 1080, T, 1.3, -.08, lt)
    tc = wfind(7, 'three hundred'); tl = wfind(7, 'limit')
    def gauge(c):
        x, y0, hh = 640, 1360, 620
        c.rectangle(x - 80 + 10, y0 - hh + 10, 160, hh); c.set_source_rgba(0, 0, 0, .3); c.fill()
        c.rectangle(x - 80, y0 - hh, 160, hh); c.set_source_rgba(1, 1, 1, 1); c.fill()
        u = eout(clamp((T - tc) / 1.0)) if T > tc else 0
        c.rectangle(x - 80, y0 - hh * .75 * u, 160, hh * .75 * u); c.set_source_rgba(*hx(RED)); c.fill()
        c.rectangle(x - 80, y0 - hh, 160, hh); ink(c, 7); c.stroke()
        if T > tl:
            c.set_dash([20, 12]); c.move_to(x - 140, y0 - hh); c.line_to(x + 140, y0 - hh); c.set_source_rgba(*hx('1C1614')); c.set_line_width(7); c.stroke(); c.set_dash([])
    overlay(fr, cairo_layer(gauge))
    tape(fr, 'CAFFEINE IN ONE CAN', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    if T > tc: stat(fr, '300 MG', 'IN SOME CANS', 870, 1000, T - tc, RED, 4, 96)
    if T > tl: stat(fr, '400 MG', 'DAILY LIMIT, MOST ADULTS', 870, 690, T - tl, YEL, -3, 96)

def s_next(fr, T):
    lt = T - S[8]; bg(fr, T, 'C9E4B4')
    s_ = st('ecg', w=520)
    ph = photo('ecg', 800, 520, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 960, back(clamp(lt / .35)), 1.0, -2)
    tape(fr, 'WHAT HAPPENS NEXT', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(8, 'bigger'): chip(fr, 'BIGGER STUDIES', CX, 640, T - wfind(8, 'bigger'), CYAN, 46, 2)
    ta = wfind(8, 'age limit')
    if T > ta - .3: burst(fr, 'NO AGE LIMIT', CX, 1330, T - ta + .3, r=150, col=YEL, size=42, rot=-5)

def s_look(fr, T):
    lt = T - S[9]; bg(fr, T, 'F7D9C4'); rays(fr, T, 'FFFFFF', .14)
    s_ = st('can', h=620)
    if s_ is not None: put_rgba(fr, s_, CX, 1030, 1.0 + .25 * eout(clamp(lt / 3)), 1.0, -6)
    else: can(fr, CX, 1030, T, 1.8 + .4 * eout(clamp(lt / 3)), -.1)
    tape(fr, 'BEFORE THE NEXT ONE...', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    if T > wfind(9, 'look'): title(fr, 'TAKE A LOOK', 620, T - wfind(9, 'look'), size=130, fill=YEL)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_heart), (S[3], s_reports), (S[5] + .45, s_bars), (S[6], s_age), (S[7], s_proof), (S[8], s_caff), (S[9], s_next), (END, s_look)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'flagged'), wfind(4, 'eleven'), wfind(8, 'age limit')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
