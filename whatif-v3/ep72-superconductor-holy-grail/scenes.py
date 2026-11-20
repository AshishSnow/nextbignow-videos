import sys, os, json, math
sys.path.insert(0, '/home/claude/super')
from kit import *
D = '/home/claude/super'
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

MAG = st('levitate', w=560); BULB = st('bulb', h=520); METER = st('meter', h=460)

def wire(c, y, T, leak=0.0, x0=60, x1=1020, col=YEL):
    for lw, cc in ((30, '1C1614'), (18, 'B87333')):
        c.move_to(x0, y); c.line_to(x1, y); c.set_source_rgba(*hx(cc)); c.set_line_width(lw); c.stroke()
    for k in range(14):
        x = x0 + ((T * 260 + k * 70) % (x1 - x0)); c.arc(x, y, 9, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill()
    if leak > 0:
        rng = np.random.default_rng(int(T * 8))
        for k in range(int(10 * leak)):
            x = rng.uniform(x0, x1); ph = (T * 2 + k * .37) % 1
            c.move_to(x, y - 20 - ph * 120); c.line_to(x + 14, y - 40 - ph * 120); c.line_to(x - 6, y - 50 - ph * 120); c.line_to(x + 10, y - 75 - ph * 120)
            c.set_source_rgba(*hx('FF5A1F', 1 - ph)); c.set_line_width(6); c.stroke()

def bolt(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, dy, col in ((12, 14, '1C1614'), (0, 0, YEL)):
        c.move_to(20 + dx, -200 + dy); c.line_to(-80 + dx, 20 + dy); c.line_to(0 + dx, 20 + dy); c.line_to(-40 + dx, 200 + dy); c.line_to(90 + dx, -40 + dy); c.line_to(10 + dx, -40 + dy); c.line_to(60 + dx, -200 + dy); c.close_path()
        c.set_source_rgba(*hx(col)); c.fill_preserve()
        if dx == 0: ink(c, 8); c.stroke()
        else: c.new_path()
    c.restore()

def thermo(c, x, y, s, val):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-46 + 12, -420 + 14, 92, 700); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-46, -420, 92, 700); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 9); c.stroke()
    col = BLUE if val < 0 else RED
    c.arc(0, 320, 90, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 9); c.stroke()
    frac = clamp((val + 273) / 320); top = 280 - frac * 680
    c.rectangle(-24, top, 48, 300 - top); c.set_source_rgba(*hx(col)); c.fill(); c.restore()

def pairs(c, T, sync=0.0, n=12, cx=CX, cy=1030, w=760, h=420, col=CYAN, a=1.0):
    rng = np.random.default_rng(5)
    base = rng.uniform(0, 1, (n, 2)); phs = rng.uniform(0, 2 * math.pi, n)
    for k in range(n):
        bx = cx - w / 2 + (k % 4) * w / 3; by = cy - h / 2 + (k // 4) * h / 2
        jx = (1 - sync) * 40 * math.sin(T * 7 + phs[k]); jy = (1 - sync) * 40 * math.cos(T * 5.3 + phs[k] * 1.7)
        wave = sync * 50 * math.sin(T * 4 + (k % 4) * .9)
        x, y = bx + jx, by + jy + wave; ang = (1 - sync) * (T * 3 + phs[k]) + sync * .0
        dx, dy = math.cos(ang) * 38, math.sin(ang) * 38
        c.move_to(x - dx, y - dy); c.line_to(x + dx, y + dy); ink(c, 6, a); c.stroke()
        for sx in (-1, 1):
            c.arc(x + sx * dx + 4, y + sx * dy + 5, 24, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614', a)); c.fill()
            c.arc(x + sx * dx, y + sx * dy, 24, 0, 2 * math.pi); c.set_source_rgba(*hx(col if sync < .5 else YEL, a)); c.fill_preserve(); ink(c, 5, a); c.stroke()

def s_hook(fr, T):
    fr[:] = paper('1B2A6B', .82); rays(fr, T, YEL, .12, cy=1060)
    ph = photo('pylon', 760, 640, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1050, 1.0 + .02 * T, 1.0, -2)
    overlay(fr, cairo_layer(lambda c: bolt(c, 830, 1150, .9 + .05 * math.sin(T * 8))))
    tape(fr, 'THE HOLY GRAIL', CX, 470, 1.0, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    title(fr, 'OF ELECTRICITY', 600, 1.0, size=118, fill=YEL, rot=-3)

def s_question(fr, T):
    lt = T - S[1]; fr[:] = paper(BLUE, .68); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: wire(c, 1080, T, 1.0)))
    tape(fr, 'WHAT IF WIRES', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    title(fr, 'STOPPED WASTING POWER?', 590, lt - .15, size=80, fill=YEL)

def s_lost(fr, T):
    lt = T - S[2]; fr[:] = paper(RED, .74); rays(fr, T, 'FFFFFF', .1)
    ph = photo('pylon', 700, 480, (.5, .4))
    if ph is not None: put_rgba(fr, ph, CX, 960, back(clamp(lt / .35)), 1.0, 2)
    overlay(fr, cairo_layer(lambda c: wire(c, 1290, T, 1.0)))
    t5 = wfind(2, 'five')
    if T > t5: stat(fr, '~5%', "OF AMERICA'S POWER", CX, 560, T - t5, YEL, -3, 150)
    if T > wfind(2, 'lost'): chip(fr, 'LOST IN THE LINES', CX, 1180, T - wfind(2, 'lost'), 'FFFFFF', 44, 2)

def s_fix(fr, T):
    lt = T - S[3]; fr[:] = paper(CYAN, .55); rays(fr, T, 'FFFFFF', .14)
    lev = 40 * math.sin(T * 2.5)
    def base(c):
        c.rectangle(CX - 260 + 12, 1260 + 14, 520, 90); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(CX - 260, 1260, 520, 90); c.set_source_rgba(*hx('A0AEC0')); c.fill_preserve(); ink(c, 8); c.stroke()
        for k in range(5):
            c.move_to(CX - 200 + k * 100, 1230); c.curve_to(CX - 220 + k * 100, 1180, CX - 180 + k * 100, 1150, CX - 200 + k * 100, 1110); c.set_source_rgba(*hx('FFFFFF', .7)); c.set_line_width(6); c.stroke()
    ph = photo('levitate', 760, 560, (.5, .45))
    if ph is not None: put_rgba(fr, ph, CX, 1000, back(clamp(lt / .35)) * (1 + .015 * math.sin(T * 2.5)), 1.0, -2)
    tape(fr, 'SUPERCONDUCTORS', CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    chip(fr, 'ZERO RESISTANCE', 300, 640, T - wfind(3, 'resistance') + .3, YEL, 42, -3)
    chip(fr, 'ZERO WASTE', 800, 640, T - wfind(3, 'waste') + .2, 'FFFFFF', 42, 3)

def s_cold(fr, T):
    lt = T - S[4]; fr[:] = paper('8EC5FF', .6); rays(fr, T, 'FFFFFF', .16)
    val = lerp(20, -260, eout((T - wfind(4, 'minus')) / 1.2))
    overlay(fr, cairo_layer(lambda c: thermo(c, 780, 960, .85, val)))
    ph = photo('nitrogen', 420, 520, (.5, .5))
    if ph is not None: put_rgba(fr, ph, 330, 1040, back(clamp(lt / .35)), 1.0, -4)
    tape(fr, 'THE PROBLEM?', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    if T > wfind(4, 'minus'): title(fr, f'{int(round(val))}°C', 600, T - wfind(4, 'minus'), size=140, fill='FFFFFF', rot=-3)

def s_tool(fr, T):
    lt = T - S[5]; fr[:] = paper(None); rays(fr, T, YEL, .16)
    def dr(c):
        for i in range(9):
            for j in range(5):
                x = 200 + i * 85; y = 1000 + j * 70 + 10 * math.sin(T * 3 + i)
                c.arc(x, y, 18, 0, 2 * math.pi); c.set_source_rgba(*hx('9AA5B1')); c.fill_preserve(); ink(c, 3); c.stroke()
        px = CX + 280 * math.sin(T * 1.5)
        c.move_to(px - 70, 700); c.line_to(px + 70, 700); c.line_to(px, 950); c.close_path(); c.set_source_rgba(*hx('6B7280')); c.fill_preserve(); ink(c, 8); c.stroke()
        c.rectangle(px - 110, 620, 220, 90); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 8); c.stroke()
    overlay(fr, cairo_layer(dr))
    tape(fr, 'SCIENTISTS IN EUROPE', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    chip(fr, 'NEW MEASURING TOOL', CX, 1420 - 120, lt - .5, YEL, 44, -2)

def s_pairs(fr, T):
    lt = T - S[6]; fr[:] = paper(GREEN, .55); rays(fr, T, 'FFFFFF', .12)
    overlay(fr, cairo_layer(lambda c: pairs(c, T, 0.0, a=clamp(lt / .5))))
    tape(fr, 'ELECTRON PAIRS', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    tr = wfind(6, 'room')
    if T > tr: title(fr, 'SURVIVE AT ROOM TEMP', 600, T - tr, size=84, fill=YEL)

def s_why(fr, T):
    lt = T - S[7]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, "SO WHY DON'T", 860, lt, size=130, fill='FFFFFF'); title(fr, 'THEY WORK?', 1050, lt - .12, size=150, fill=YEL)

def s_rhythm(fr, T):
    lt = T - S[8]; fr[:] = paper(PINK, .55); rays(fr, T, 'FFFFFF', .1)
    overlay(fr, cairo_layer(lambda c: pairs(c, T, 0.0)))
    tape(fr, "THEY DON'T MOVE TOGETHER", CX, 470, lt, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    if T > wfind(8, 'rhythm') - .3: burst(fr, 'NO RHYTHM!', 820, 1360 - 60, T - wfind(8, 'rhythm') + .3, r=130, col=RED, size=40)

def s_sync(fr, T):
    lt = T - S[9]; fr[:] = paper(YEL, .5); rays(fr, T, 'FFFFFF', .14)
    sy = eout(lt / 1.2)
    overlay(fr, cairo_layer(lambda c: pairs(c, T, sy)))
    tape(fr, 'GET THEM IN SYNC...', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    tr = wfind(9, 'room')
    if T > tr: title(fr, 'ROOM-TEMP SUPERCONDUCTORS?', 600, T - tr, size=70, fill=RED)

def s_next(fr, T):
    lt = T - S[10]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_uses(fr, T):
    lt = T - S[11]; fr[:] = paper(BLUE, .62); rays(fr, T, 'FFFFFF', .1)
    items = (('pylon', 'ZERO-WASTE POWER', 'zero', 300, 760), ('maglev', 'FLOATING TRAINS', 'floating', 780, 760), ('mri', 'CHEAPER MRI', 'mri', 300, 1110), ('quantum', 'QUANTUM COMPUTERS', 'quantum', 780, 1110))
    for k, (ph_, lab, w, x, y) in enumerate(items):
        tw = wfind(11, w); ph = photo(ph_, 400, 300)
        if T > tw - .1:
            if ph is not None: put_rgba(fr, ph, x, y, back(clamp((T - tw + .1) / .3)), 1.0, (-3, 3, 2, -2)[k])
            chip(fr, lab, x, y + 165, T - tw, (YEL, 'FFFFFF', CYAN, GREEN)[k], 34, (-2, 2, -2, 2)[k])
    tape(fr, 'IF THEY CRACK IT', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)

def s_look(fr, T):
    lt = T - S[12]; fr[:] = paper(None); rays(fr, T, RED, .1)
    def dr(c):
        c.arc(CX - 40 + 12, 980 + 14, 190, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.arc(CX - 40, 980, 190, 0, 2 * math.pi); c.set_source_rgba(*hx('DFF4FF')); c.fill_preserve(); ink(c, 14); c.stroke()
        c.move_to(CX + 100, 1120); c.line_to(CX + 260, 1300); ink(c, 46); c.stroke()
        pairs(c, T, eout(clamp((T - S[12] - 2) / 1.2)), n=4, cx=CX - 40, cy=980, w=260, h=180)
    overlay(fr, cairo_layer(dr))
    tape(fr, 'NOT SOLVED YET', CX, 470, lt, col=RED, size=60, font=LUCKY, rot=-2, tcol='FFFFFF')
    tk = wfind(12, 'know')
    if T > tk: title(fr, 'BUT NOW THEY KNOW WHERE', 600, T - tk, size=66, fill=YEL)

def s_end(fr, T):
    lt = T - S[13]; fr[:] = paper('1B2A6B', .8); rays(fr, T, YEL, .12)
    overlay(fr, cairo_layer(lambda c: bolt(c, CX, 1050, 1.3)))
    tape(fr, 'BIGGER THAN AI?', CX, 470, lt, col='FFFFFF', size=64, font=LUCKY, rot=-2)
    if T > S[14]:
        burst(fr, 'YES', 260, 1250, T - S[14], r=110, col=GREEN, size=60, rot=-8)
        burst(fr, 'NO', 820, 1250, T - S[14] - .15, r=110, col=RED, size=60, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_lost), (S[4], s_fix), (S[5], s_cold), (S[6], s_tool), (S[7], s_pairs), (S[8], s_why),
           (S[9], s_rhythm), (S[10], s_sync), (S[11], s_next), (S[12], s_uses), (S[13], s_look), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(2, 'five'), wfind(4, 'minus') + 1.2, wfind(6, 'room'), wfind(9, 'room')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Photos: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
