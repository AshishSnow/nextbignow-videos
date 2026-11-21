import sys, os, json, math
sys.path.insert(0, '/home/claude/nod')
from kit import *
D = '/home/claude/nod'
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


def deep(fr, T, top='0E3A5C', bot='020A18'):
    yy = np.linspace(0, 1, H)[:, None, None]; a = np.array(rgb(top), np.float32); b = np.array(rgb(bot), np.float32)
    fr[:] = np.broadcast_to((a * (1 - yy) + b * yy), (H, W, 3)).astype(np.uint8)
    def dr(c):
        for k in range(5):
            x = 150 + k * 210 + 40 * math.sin(T * .3 + k); c.move_to(x - 40, 0); c.line_to(x + 40, 0); c.line_to(x + 160, H); c.line_to(x - 60, H); c.close_path()
            c.set_source_rgba(.6, .85, 1, .035); c.fill()
        rng = np.random.default_rng(3)
        for k in range(90):
            x0, y0, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1.5, 4.5)
            y = (y0 + T * 25 * r) % H; x = x0 + 8 * math.sin(T + k)
            c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(.9, .95, 1, .35); c.fill()
    overlay(fr, cairo_layer(dr))

def critter(c, x, y, T, k, s=1.0, col=None):
    col = col or ['FFD84D', 'FF8FA3', '7FFFD4', 'FFFFFF'][k % 4]; w = math.sin(T * 6 + k)
    if k % 2 == 0:  # worm
        c.move_to(x - 16 * s, y)
        c.curve_to(x - 6 * s, y - 10 * s * w, x + 6 * s, y + 10 * s * w, x + 16 * s, y)
        c.set_source_rgba(*hx('1C1614')); c.set_line_width(9 * s); c.stroke()
        c.move_to(x - 16 * s, y); c.curve_to(x - 6 * s, y - 10 * s * w, x + 6 * s, y + 10 * s * w, x + 16 * s, y)
        c.set_source_rgba(*hx(col)); c.set_line_width(5 * s); c.stroke()
    else:  # copepod
        for lg in (-1, 1):
            c.move_to(x, y); c.line_to(x + lg * 16 * s, y - (12 + 4 * w) * s); c.set_source_rgba(*hx(col)); c.set_line_width(2.5 * s); c.stroke()
        c.save(); c.translate(x, y); c.scale(1, .6); c.arc(0, 0, 9 * s, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(*hx(col)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(2); c.stroke()

def xsection(c, x, y, R, T, n=40, open_=1.0, cols=None):
    rng = np.random.default_rng(7)
    def blob(r, j):
        pts = []
        for a in range(36):
            ang = a / 36 * 2 * math.pi; rr = r * (1 + .08 * math.sin(ang * 3 + j) + .05 * math.cos(ang * 5 + j * 2))
            pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr * .85))
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path()
    blob(R + 12, 0); c.set_source_rgba(*hx('1C1614')); c.fill()
    for j in range(7):
        blob(R * (1 - j * .13), j); c.set_source_rgba(*hx(['3B2A1E', '5A3E28', '2E2218', '6B4A2F', '3B2A1E', '4F3624', '2A1E15'][j])); c.fill()
    for k in range(int(n * open_)):
        a = rng.uniform(0, 2 * math.pi); rr = R * math.sqrt(rng.uniform(.02, .85))
        critter(c, x + math.cos(a) * rr, y + math.sin(a) * rr * .85, T, k, R / 190, None if cols is None else cols[k % len(cols)])

def counter(fr, T, t0, dur, n0, n1, cy, size=150, fill=YEL, suffix=''):
    if T < t0: return
    v = int(n0 + (n1 - n0) * eout(clamp((T - t0) / dur))); title(fr, f'{v:,}{suffix}', cy, T - t0, size=size, fill=fill)

def s_hook(fr, T):
    deep(fr, T)
    tc = wfind(0, 'found')
    op = ease(clamp((T - tc + .6) / .8))
    nd = st('nodule', w=460)
    if op < 1 and nd is not None:
        put_rgba(fr, nd, CX + 8 * math.sin(T * 30) * (op > 0), 1080, 1.0 + .5 * op, 1.0 - op, 3 * math.sin(T * 2))
    if op > 0: overlay(fr, cairo_layer(lambda c: xsection(c, CX, 1080, 300 * op + 1, T, 60, op)))
    tape(fr, 'A ROCK FROM THE OCEAN FLOOR', CX, 470, T, col='FFFFFF', size=50, font=LUCKY, rot=-2)
    tw = wfind(0, 'two hundred')
    if T > tw: counter(fr, T, tw, 1.2, 0, 245, 610, 130, YEL, ' ANIMALS')
    if T > wfind(0, 'inside'): burst(fr, 'INSIDE!', 840, 1380, T - wfind(0, 'inside'), r=105, col=RED, size=46)

def s_question(fr, T):
    lt = T - S[1]; deep(fr, T)
    ph = photo('seafloor', 820, 560, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1020, back(clamp(lt / .35)), 1.0, -2)
    tape(fr, 'MINING COMPANIES WANT', CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(1, 'billions'): title(fr, 'BILLIONS OF THEM', 600, T - wfind(1, 'billions'), size=112, fill=YEL)

def s_nodule(fr, T):
    lt = T - S[2]; deep(fr, T, '0A2E4C', '01060F')
    sk(fr, st('nodule', w=520), 440, 1050, T, 0, 1.0, -4, lt)
    tape(fr, "THEY'RE CALLED NODULES", CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    if T > wfind(2, 'potato'): chip(fr, 'POTATO-SIZED', 440, 1340, T - wfind(2, 'potato'), YEL, 44, -3)
    td = wfind(2, 'four miles')
    def gauge(c):
        x = 900; c.rectangle(x - 14, 760, 28, 640); c.set_source_rgba(*hx('FFFFFF', .2)); c.fill()
        u = clamp((T - td + 1) / 1.5); c.rectangle(x - 14, 700, 28, 700 * u); c.set_source_rgba(*hx(CYAN)); c.fill()
        c.rectangle(x - 14, 700, 28, 700); ink(c, 5); c.stroke()
    overlay(fr, cairo_layer(gauge))
    if T > td: stat(fr, '4 MILES', 'DOWN', 800, 620, T - td, RED, 3, 110)

def s_slow(fr, T):
    lt = T - S[3]; deep(fr, T)
    g = clamp(lt / 3.5)
    overlay(fr, cairo_layer(lambda c: xsection(c, CX, 1060, 80 + 240 * g, T, 0, 0)))
    tape(fr, 'THEY GROW SO SLOWLY', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    if T > wfind(3, 'millions'): title(fr, 'MILLIONS OF YEARS', 600, T - wfind(3, 'millions'), size=100, fill=YEL)
    sk(fr, st('nodcut', w=300), 820, 1220, T, 2, 1.0, 6, lt - 1.2)
    chip(fr, 'REAL ONE, CUT IN HALF', 760, 1540, lt - 1.4, CYAN, 32, 2)
    chip(fr, 'LAYER BY LAYER', CX, 720, lt - 1.0, 'FFFFFF', 40, -2)

def s_study(fr, T):
    lt = T - S[4]; deep(fr, T, '12385A', '030B19')
    def dr(c):
        for k in range(244):
            r_, q = divmod(k, 16); x = 120 + q * 56; y = 760 + r_ * 50
            on = clamp((lt - .2 - k * .006) / .1)
            if on <= 0: continue
            c.save(); c.translate(x, y); c.scale(on, on * .8); c.arc(0, 0, 20, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(*hx('3B2A1E')); c.fill_preserve(); ink(c, 3); c.stroke()
        ti = wfind(4, 'inside')
        if T > ti:
            for k in range(int(clamp((T - ti) / 2) * 120)):
                rng = np.random.default_rng(k); critter(c, rng.uniform(100, 980), rng.uniform(740, 1520), T, k, .8)
    overlay(fr, cairo_layer(dr))
    tape(fr, 'RESEARCHERS OPENED', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    ti = wfind(4, 'inside')
    if T < ti: counter(fr, T, wfind(4, 'two hundred'), 1.0, 0, 244, 600, 120, YEL, ' NODULES')
    else: counter(fr, T, ti, 1.4, 0, 4139, 600, 120, YEL, ' ANIMALS')

def s_city(fr, T):
    lt = T - S[5]; deep(fr, T)
    overlay(fr, cairo_layer(lambda c: xsection(c, CX, 1060, 360, T, 80, clamp(lt / 1.5))))
    title(fr, 'ONE ROCK: 245', 470, lt, size=110, fill='FFFFFF', rot=-2)
    if T > wfind(5, 'city'): title(fr, 'A HIDDEN CITY', 600, T - wfind(5, 'city'), size=110, fill=YEL)
    if T > wfind(5, 'city'): burst(fr, 'WOW', 860, 1380, T - wfind(5, 'city') - .3, r=95, col=RED, size=50)

def s_diff(fr, T):
    lt = T - S[6]; deep(fr, T)
    def dr(c):
        c.rectangle(80, 760, 430, 560); c.set_source_rgba(*hx('7A5C3E')); c.fill_preserve(); ink(c, 6); c.stroke()
        for k in range(14):
            rng = np.random.default_rng(100 + k); critter(c, rng.uniform(120, 470), rng.uniform(800, 1280), T, k, 1.4, 'C9C9C9')
        xsection(c, 790, 1040, 220, T, 24, 1.0, ['FFD84D', 'FF8FA3', '7FFFD4'])
    overlay(fr, cairo_layer(dr))
    chip(fr, 'MUD', 295, 1380, lt, 'FFFFFF', 44, -3); chip(fr, 'NODULE', 790, 1380, lt - .2, YEL, 44, 3)
    tape(fr, 'DIFFERENT ANIMALS', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(6, 'same'): burst(fr, 'NOT THE SAME', CX, 660, T - wfind(6, 'same'), r=150, col=YEL, size=40, rot=-4)

def s_metals(fr, T):
    lt = T - S[7]; deep(fr, T, '1B2A4C', '05070F')
    tb = wfind(7, 'packed')
    sk(fr, st('nodule', w=300), 250, 1060, T, 0, 1.0, -6, lt)
    def bat(c):
        u = ease(clamp((T - tb) / 1.6)); x, y, w, h = 520, 860, 420, 380
        c.rectangle(x + 12, y + 14, w, h); c.set_source_rgba(0, 0, 0, .4); c.fill()
        c.rectangle(x + w, y + h / 2 - 50, 40, 100); c.set_source_rgba(*hx('DDDDDD')); c.fill_preserve(); ink(c, 6); c.stroke()
        c.rectangle(x, y, w, h); c.set_source_rgba(*hx('20283A')); c.fill()
        c.rectangle(x + 20, y + 20, (w - 40) * u, h - 40); c.set_source_rgba(*hx(GREEN)); c.fill()
        c.rectangle(x, y, w, h); ink(c, 9); c.stroke()
        c.move_to(x + w / 2 + 20, y + 80); c.line_to(x + w / 2 - 40, y + h / 2 + 10); c.line_to(x + w / 2 + 10, y + h / 2 + 10); c.line_to(x + w / 2 - 20, y + h - 80)
        c.line_to(x + w / 2 + 60, y + h / 2 - 20); c.line_to(x + w / 2 + 10, y + h / 2 - 20); c.close_path(); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 5); c.stroke()
        if T > tb:
            for k in range(6):
                f = ((T - tb) * .8 + k / 6) % 1; c.arc(lerp(330, 520, f), 1050 - 60 * math.sin(f * math.pi), 12, 0, 2 * math.pi); c.set_source_rgba(*hx(CYAN, 1 - f * .5)); c.fill()
    overlay(fr, cairo_layer(bat))
    tape(fr, 'WHY DOES THAT MATTER?', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    if T > tb: title(fr, 'BATTERY METALS', 600, T - tb, size=110, fill=YEL)
    for k, m in enumerate(('NICKEL', 'COBALT', 'MANGANESE')):
        tk = wfind(7, 'batteries') + k * .25
        if T > tk: chip(fr, m, [230, CX, 850][k], 1340 + (k % 2) * 60, T - tk, [CYAN, 'FFFFFF', YEL][k], 38, [-4, 2, -2][k])

def s_next(fr, T):
    lt = T - S[8]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_permit(fr, T):
    lt = T - S[9]; fr[:] = paper('E8DCC0', .5); rays(fr, T, 'FFFFFF', .1)
    def doc(c):
        c.save(); c.translate(CX, 1060); c.rotate(-.05)
        c.rectangle(-270 + 12, -340 + 14, 540, 680); c.set_source_rgba(0, 0, 0, .35); c.fill()
        c.rectangle(-270, -340, 540, 680); c.set_source_rgba(*hx('FFFDF5')); c.fill_preserve(); ink(c, 7); c.stroke()
        for k in range(9):
            c.rectangle(-210, -230 + k * 56, 420 - (k % 3) * 70, 14); c.set_source_rgba(*hx('1C1614', .25)); c.fill()
        c.restore()
    overlay(fr, cairo_layer(doc))
    tape(fr, 'DEEP-SEA MINING PERMIT', CX, 760, lt, col='FFFFFF', size=50, font=LUCKY, rot=-4)
    tape(fr, 'THE U.S. COULD CERTIFY', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    if T > wfind(9, 'first'): title(fr, 'ITS FIRST ONE', 600, T - wfind(9, 'first'), size=112, fill=YEL)
    td = wfind(9, 'december')
    if T > td: burst(fr, 'DEC?', 780, 1260, T - td, r=130, col=RED, size=60, rot=-8)

def s_scoop(fr, T):
    lt = T - S[10]; deep(fr, T)
    u = clamp(lt / max(1, L[10]['dur']))
    cx_ = lerp(-150, W + 150, u)
    def dr(c):
        c.rectangle(0, 1230, W, 400); c.set_source_rgba(*hx('4A3A2A')); c.fill()
        for k in range(14):
            x = 60 + k * 75
            if x > cx_ - 60:
                c.save(); c.translate(x, 1235); c.scale(1, .7); c.arc(0, 0, 26, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('2A1E15')); c.fill_preserve(); ink(c, 3); c.stroke()
                critter(c, x, 1180 + 10 * math.sin(T * 3 + k), T, k, .7)
        c.rectangle(0, 1230, max(0, cx_ - 60), 40); c.set_source_rgba(*hx('6B5A47')); c.fill()
        c.rectangle(cx_ - 160, 1060, 320, 170); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 7); c.stroke()
        for w_ in (-110, 0, 110):
            c.arc(cx_ + w_, 1230, 34, 0, 2 * math.pi); c.set_source_rgba(*hx('333333')); c.fill_preserve(); ink(c, 5); c.stroke()
        c.move_to(cx_, 1060); c.line_to(cx_ - 60, 640); c.set_source_rgba(*hx('1C1614')); c.set_line_width(10); c.stroke()
    overlay(fr, cairo_layer(dr))
    tape(fr, 'SCOOPED UP...', CX, 470, lt, col=RED, size=64, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(10, 'before'): title(fr, 'BEFORE WE KNOW', 600, T - wfind(10, 'before'), size=104, fill=YEL)
    if T > wfind(10, 'lives'): chip(fr, 'WHAT LIVES THERE', CX, 1440 - 640 + 60, T - wfind(10, 'lives'), 'FFFFFF', 44, 2)

def s_end(fr, T):
    lt = T - S[11]; deep(fr, T)
    overlay(fr, cairo_layer(lambda c: xsection(c, CX, 1040, 260, T, 40, 1.0)))
    title(fr, 'MINE THE DEEP SEA?', 560, lt, size=96, fill=YEL)
    if T > S[12]:
        burst(fr, 'YES', 230, 1330, T - S[12], r=100, col=GREEN, size=54, rot=-8)
        burst(fr, 'NO', 850, 1330, T - S[12] - .15, r=100, col=RED, size=54, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_nodule), (S[4], s_slow), (S[5], s_study), (S[6], s_city), (S[7], s_diff), (S[8], s_metals),
           (S[9], s_next), (S[10], s_permit), (S[11], s_scoop), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'found'), wfind(5, 'city'), wfind(9, 'december')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
