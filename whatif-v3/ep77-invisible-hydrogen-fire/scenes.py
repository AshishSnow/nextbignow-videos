import sys, os, json, math
sys.path.insert(0, '/home/claude/hflame')
from kit import *
D = '/home/claude/hflame'
L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + 0.3; TOTAL = END + 2.6
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

POT = st('pot', w=520)

def burner(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.translate(12, 14); c.scale(1, .35); c.arc(0, 0, 230, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.save(); c.scale(1, .35); c.arc(0, 0, 230, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('4A5568')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.save(); c.scale(1, .35); c.arc(0, 0, 130, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('2D3748')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def hflame(c, x, y, s, T, glow=1.0, col='FF8C1A'):
    """ring of flame tongues; glow 0..1 sets visibility."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(12):
        a = k / 12 * 2 * math.pi; fx = math.cos(a) * 130; fy = math.sin(a) * 45
        h = 120 + 30 * math.sin(T * 11 + k * 1.7)
        c.move_to(fx - 24, fy); c.curve_to(fx - 30, fy - h * .5, fx - 6, fy - h * .8, fx + 2 * math.sin(T * 7 + k), fy - h)
        c.curve_to(fx + 8, fy - h * .8, fx + 30, fy - h * .5, fx + 24, fy); c.close_path()
        c.set_source_rgba(*hx(col, .9 * glow)); c.fill()
        c.move_to(fx - 10, fy); c.curve_to(fx - 12, fy - h * .3, fx, fy - h * .45, fx, fy - h * .55); c.curve_to(fx, fy - h * .45, fx + 12, fy - h * .3, fx + 10, fy); c.close_path()
        c.set_source_rgba(*hx('7FB3FF', .35 + .4 * glow)); c.fill()
    c.restore()

def wind(c, T, x0, x1, y0, y1, salt=1.0, rtl=False):
    rng = np.random.default_rng(4)
    for k in range(18):
        yy = rng.uniform(y0, y1); ph = (T * .5 + k / 18) % 1; x = lerp(x0, x1, ph)
        if rtl: x = lerp(x1, x0, ph)
        c.move_to(x - 70, yy); c.curve_to(x - 35, yy - 18, x - 10, yy + 18, x + 30, yy); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(7); c.stroke()
        if rng.uniform() < salt:
            c.rectangle(x + 40, yy - 8, 14, 14); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 3); c.stroke()

def s_hook(fr, T):
    fr[:] = paper('1B2A6B', .82); rays(fr, T, 'FF8C1A', .1, cy=1100)
    g = .15 + .1 * math.sin(T * 3)
    overlay(fr, cairo_layer(lambda c: (burner(c, CX, 1200, 1.4), hflame(c, CX, 1185, 1.4, T, g))))
    burst(fr, 'HOT!', 830, 880, T - 1.4, r=110, col=RED, size=60)
    tape(fr, "A FIRE YOU CAN'T SEE", CX, 470, 1.0, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'ON YOUR STOVE', 600, 1.0, size=118, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .68); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: (burner(c, CX, 1220, 1.3), hflame(c, CX, 1205, 1.3, T, .35))))
    ph = photo('h2', 520, 340)
    if ph is not None: put_rgba(fr, ph, 300, 860, back(clamp(lt / .35)), 1.0, -4)
    chip(fr, 'GAS TODAY', 300, 1000, lt - .3, 'FFFFFF', 34, -3)
    put_rgba(fr, ttext('H2?', 120, LUCKY, CYAN), 800, 860, back(clamp((lt - .5) / .3)), 1.0, 6)
    tape(fr, 'WHAT IF YOUR STOVE', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'RAN ON HYDROGEN?', 590, lt - .15, size=100, fill=YEL)

def s_clean(fr, T):
    lt = T - S[2]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .14)
    tw = wfind(2, 'water')
    def dr(c):
        burner(c, CX, 1250, 1.1); hflame(c, CX, 1235, 1.1, T, .6)
        if T > tw:
            for k in range(6):
                ph = ((T - tw) * .8 + k / 6) % 1; x = CX - 150 + k * 60; y = 1050 - ph * 300
                c.move_to(x, y - 30); c.curve_to(x + 22, y, x + 22, y + 20, x, y + 22); c.curve_to(x - 22, y + 20, x - 22, y, x, y - 30)
                c.set_source_rgba(*hx('3B82F6', 1 - ph)); c.fill()
    overlay(fr, cairo_layer(dr))
    tape(fr, 'THE CLEAN FUEL', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    if T > tw: title(fr, 'IT BURNS INTO WATER', 600, T - tw, size=92, fill=BLUE)

def s_invis(fr, T):
    lt = T - S[3]; fr[:] = paper('2A2F5A', .85); rays(fr, T, 'FFFFFF', .05)
    g = max(0.0, .7 - .7 * eout(lt / 1.6))
    overlay(fr, cairo_layer(lambda c: (burner(c, CX, 1220, 1.4), hflame(c, CX, 1205, 1.4, T, g))))
    tape(fr, 'A PURE HYDROGEN FLAME', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    if T > wfind(3, 'invisible'): title(fr, 'ALMOST INVISIBLE', 600, T - wfind(3, 'invisible'), size=110, fill=YEL)

def s_why(fr, T):
    lt = T - S[4]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    overlay(fr, cairo_layer(lambda c: hflame(c, CX, 1250, 1.2, T, 1.0)))
    title(fr, 'SO WHY', 760, lt, size=170, fill='FFFFFF'); title(fr, 'IS IT ORANGE?', 950, lt - .12, size=130, fill=YEL)

def s_salt(fr, T):
    lt = T - S[5]; fr[:] = paper('8EC5FF', .6); rays(fr, T, 'FFFFFF', .12)
    ph = photo('ocean', 480, 600, (.5, .5))
    if ph is not None: put_rgba(fr, ph, 260, 1050, back(clamp(lt / .35)), 1.0, -3)
    overlay(fr, cairo_layer(lambda c: (wind(c, T, 420, 760, 900, 1250), burner(c, 840, 1250, .7), hflame(c, 840, 1240, .7, T, 1.0))))
    tape(fr, "IT'S SALT", CX, 470, lt, col='FFFFFF', size=70, font=LUCKY, rot=-2)
    chip(fr, 'SEA SALT IN THE WIND', CX, 600, T - wfind(5, 'sea'), YEL, 44, 2)

def s_test(fr, T):
    lt = T - S[6]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    def cal(c):
        for k in range(14):
            x = 230 + (k % 7) * 105; y = 950 + (k // 7) * 130; on = clamp((lt - .5 - k * .15) / .2)
            c.rectangle(x - 45 + 6, y - 50 + 8, 90, 100); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(x - 45, y - 50, 90, 100); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 5); c.stroke()
            if on > 0: hflame(c, x, y + 30, .2, T + k, .4 + .6 * abs(math.sin(k * 1.9)) * on)
    overlay(fr, cairo_layer(cal))
    tape(fr, 'SCIENTISTS IN AUSTRALIA', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    chip(fr, '2 WEEKS. SAME SETTINGS.', CX, 600, T - wfind(6, 'two weeks'), YEL, 44, 2)

def s_28x(fr, T):
    lt = T - S[7]; fr[:] = paper('FF8C1A', .7); rays(fr, T, 'FFFFFF', .14)
    base = 1300
    def dr(c):
        ink(c, 8); c.move_to(200, base); c.line_to(880, base); c.stroke()
        for j, (h, col) in enumerate(((20, '7FB3FF'), (560, YEL))):
            p = eout((lt - .2 - j * .6) / .7); x = 380 + j * 320; hh = h * p
            c.rectangle(x - 100 + 12, base - hh + 14, 200, hh); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(x - 100, base - hh, 200, hh); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    overlay(fr, cairo_layer(dr))
    tape(fr, 'DIMMEST DAY', 380, base + 60, lt - .2, col='FFFFFF', size=32, font=ELITE, rot=-2); tape(fr, 'BRIGHTEST DAY', 700, base + 60, lt - .8, col=YEL, size=32, font=ELITE, rot=2)
    tape(fr, 'THE ORANGE GLOW CHANGED', CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    t28 = wfind(7, 'twenty')
    if T > t28: title(fr, '28X', 640, T - t28, size=180, fill=RED)

def s_wind(fr, T):
    lt = T - S[8]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .12)
    ti = wfind(8, 'inland'); inland = T > ti - .3
    overlay(fr, cairo_layer(lambda c: (wind(c, T, 100, 600, 820, 1150, salt=0.0 if inland else 1.0, rtl=inland), burner(c, 790, 1220, .9), hflame(c, 790, 1205, .9, T, .15 if inland else 1.0))))
    tape(fr, 'WIND FROM THE SEA' if not inland else 'WIND FROM INLAND', CX, 470, 1.0, col=BLUE if not inland else '6B7280', size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, 'BRIGHT FLAME' if not inland else 'BARELY THERE', 600, (T - wfind(8, 'bright')) if not inland else (T - ti + .3), size=110, fill=YEL if not inland else 'FFFFFF')

def s_compare(fr, T):
    lt = T - S[9]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .12)
    overlay(fr, cairo_layer(lambda c: (burner(c, 300, 1180, .9), hflame(c, 300, 1165, .9, T, .35), burner(c, 790, 1180, .9), hflame(c, 790, 1165, .9, T, 1.0, '3B82F6'))))
    chip(fr, 'HYDROGEN', 300, 860, lt - .3, CYAN, 42, -3); chip(fr, 'NORMAL GAS', 790, 860, lt - .5, 'FFFFFF', 42, 3)
    tape(fr, 'HYDROGEN = LESS LIGHT', CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(9, 'good day'): chip(fr, 'EVEN ON A GOOD DAY', CX, 600, T - wfind(9, 'good day'), YEL, 44, 2)

def s_next(fr, T):
    lt = T - S[10]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_eyes(fr, T):
    lt = T - S[11]; fr[:] = paper(YEL, .55); rays(fr, T, 'FFFFFF', .12)
    def eye(c):
        c.save(); c.translate(CX, 1050); c.scale(1, .55); c.arc(0, 0, 260, 0, 2 * math.pi); c.restore(); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 10); c.stroke()
        c.arc(CX, 1050, 100, 0, 2 * math.pi); c.set_source_rgba(*hx(BLUE)); c.fill(); c.arc(CX, 1050, 45, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    overlay(fr, cairo_layer(eye)); xstamp(fr, CX, 1050, lt - .8, 1.2)
    tape(fr, "CAN'T COUNT ON YOUR EYES", CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)

def s_sensor(fr, T):
    lt = T - S[12]; fr[:] = paper('1B2A6B', .82); rays(fr, T, CYAN, .12)
    ph = photo('thermal', 760, 520, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1000, back(clamp((T - wfind(12, 'heat')) / .35)), 1.0, -2)
    else: overlay(fr, cairo_layer(lambda c: (burner(c, CX, 1220, 1.3), hflame(c, CX, 1205, 1.3, T, 1.0, 'FF3B1F'))))
    tape(fr, 'NEW SENSORS', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    chip(fr, 'SEE HEAT', 300, 600, T - wfind(12, 'heat'), RED, 44, -3); chip(fr, 'SEE ULTRAVIOLET', 760, 600, T - wfind(12, 'ultraviolet'), CYAN, 40, 3)
    if T > wfind(12, 'nobody'): burst(fr, 'SAFE!', 840, 1290, T - wfind(12, 'nobody'), r=110, col=GREEN, size=54)

def s_end(fr, T):
    lt = T - S[13]; fr[:] = paper('2A2F5A', .85); rays(fr, T, 'FF8C1A', .1)
    overlay(fr, cairo_layer(lambda c: (burner(c, CX, 1200, 1.3), hflame(c, CX, 1185, 1.3, T, .2))))
    title(fr, "COOK ON A FLAME", 520, lt, size=100, fill='FFFFFF'); title(fr, "YOU CAN'T SEE?", 680, lt - .12, size=110, fill=YEL)
    if T > S[14]:
        burst(fr, 'YES', 230, 920, T - S[14], r=100, col=GREEN, size=54, rot=-8)
        burst(fr, 'NO', 850, 920, T - S[14] - .15, r=100, col=RED, size=54, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_clean), (S[4], s_invis), (S[5], s_why), (S[6], s_salt), (S[7], s_test), (S[8], s_28x),
           (S[9], s_wind), (S[10], s_compare), (S[11], s_next), (S[12], s_eyes), (S[13], s_sensor), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(7, 'twenty'), wfind(8, 'inland'), wfind(3, 'invisible')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Photos: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
