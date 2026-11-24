import sys, os, json, math
sys.path.insert(0, '/home/claude/gap')
from kit import *
D = '/home/claude/gap'
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

sys.path.insert(0, '/home/claude/samples')
import essay as ES

def bg(fr, T, tint='F3E3B3', m=.55): fr[:] = paper(tint, m)
def essay_slide(T, lines, t0s, size=128):
    fr = ES.base(True); ES.headline(fr, lines, T, t0s, y=400, dark=True, size=size); return fr






def bird(c, x, y, s, T, fly=0.0, flip=False, col='8A93A6'):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    flap = math.sin(T * 22) if fly > 0 else 0
    c.save(); c.scale(1.4, 1); c.arc(0, 0, 80, 0, 6.29); c.restore(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.move_to(100, -10); c.line_to(170, -40); c.line_to(160, 30); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(-95, -60, 50, 0, 6.29); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(-80, -30, 34, .5, 2.6); c.set_source_rgba(*hx('6FB39A', .8)); c.set_line_width(10); c.stroke()
    c.move_to(-140, -65); c.line_to(-175, -55); c.line_to(-140, -48); c.close_path(); c.set_source_rgba(*hx(YEL)); c.fill_preserve(); ink(c, 4); c.stroke()
    c.arc(-108, -70, 9, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    wy = -60 * fly * (1 + flap)
    c.move_to(-20, -20); c.curve_to(10, -60 + wy, 70, -60 + wy, 90, -30 + wy * .6); c.curve_to(60, 0, 20, 10, -20, -20); c.set_source_rgba(*hx('6D7587')); c.fill_preserve(); ink(c, 6); c.stroke()
    if fly < .5:
        for lx in (-20, 20): c.move_to(lx, 75); c.line_to(lx, 120); c.set_source_rgba(*hx('E07A5F')); c.set_line_width(8); c.stroke()
    c.restore()

def person(c, x, y, s, T, walk=0.0, hair=False, col=BLUE, flip=False):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    sw = 25 * math.sin(T * 8) * walk
    for d in (-1, 1):
        c.move_to(-15 * d, 120); c.line_to(-15 * d + sw * d, 300); c.set_source_rgba(*hx('2B2B33')); c.set_line_width(30); c.set_line_cap(1); c.stroke()
    c.move_to(-70, -60); c.curve_to(-80, 60, -60, 130, 0, 130); c.curve_to(60, 130, 80, 60, 70, -60); c.curve_to(40, -80, -40, -80, -70, -60)
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
    if hair:
        c.move_to(-62, -150); c.curve_to(-90, -60, -70, -20, -40, -30); c.line_to(40, -30); c.curve_to(70, -20, 90, -60, 62, -150); c.close_path(); c.set_source_rgba(*hx('6B3E26')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.arc(0, -135, 58, 0, 6.29); c.set_source_rgba(*hx('F2C9A0')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, -168, 58, 3.3, 6.1); c.set_source_rgba(*hx('6B3E26' if hair else '3A2A20')); c.fill()
    for ex in (-20, 20): c.arc(ex, -130, 7, 0, 6.29); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()



LAY = ['C46A3C', 'E0A458', 'B5523B', 'E8C07A', 'A34A2E', 'D98B4E', 'C9A66B']

def strata(c, x0, y0, w, n, hh, T, missing=None, gone=0.0, granite_h=0, wavy=True):
    y = y0
    if granite_h:
        c.rectangle(x0, y, w, granite_h); c.set_source_rgba(*hx('8C7F8E')); c.fill_preserve(); ink(c, 6); c.stroke()
        rng = np.random.default_rng(2)
        for k in range(40):
            c.arc(x0 + rng.uniform(10, w - 10), y + rng.uniform(10, granite_h - 10), rng.uniform(4, 10), 0, 6.29); c.set_source_rgba(*hx(['F2EDE4', '3A3540', 'D9A1A8'][k % 3])); c.fill()
    for k in range(n):
        y -= hh
        al = 1.0
        if missing and missing[0] <= k < missing[1]: al = 1 - gone
        if al <= 0.02: continue
        c.move_to(x0, y + hh)
        for i in range(0, int(w) + 1, 30): c.line_to(x0 + i, y + 8 * math.sin(i / 60 + k) * wavy)
        c.line_to(x0 + w, y + hh); c.close_path()
        col = hx(LAY[k % len(LAY)]); c.set_source_rgba(col[0], col[1], col[2], al); c.fill_preserve(); ink(c, 5, al); c.stroke()

def globe(c, x, y, r, T, dots=0.0):
    c.arc(x + 10, y + 12, r, 0, 6.29); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.arc(x, y, r, 0, 6.29); c.set_source_rgba(*hx('2D6CDF')); c.fill()
    for dx, dy, rr in ((-.35, -.25, .35), (.3, -.1, .28), (.05, .4, .25), (.5, .45, .15)):
        c.arc(x + dx * r, y + dy * r, rr * r, 0, 6.29); c.set_source_rgba(*hx('3FAE5A')); c.fill()
    c.arc(x, y, r, 0, 6.29); ink(c, 8); c.stroke()
    for k, (dx, dy) in enumerate(((-.4, -.3), (.3, -.15), (.05, .35), (.5, .45), (-.2, -.05))):
        if dots > k * .2:
            c.arc(x + dx * r, y + dy * r, 22, 0, 6.29); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 5); c.stroke()

def book(c, x, y, s, T, torn=0.0):
    if s < .01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-260 + 12, -170 + 14, 520, 340); c.set_source_rgba(0, 0, 0, .25); c.fill()
    for side in (-1, 1):
        c.rectangle(0 if side > 0 else -260, -170, 260, 340); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
        for k in range(7):
            yy = -120 + k * 40; c.move_to(side * 30, yy); c.line_to(side * 220, yy); c.set_source_rgba(*hx('1C1614', .3)); c.set_line_width(5); c.stroke()
    if torn > 0:
        c.move_to(30, -170); 
        for k in range(10): c.line_to(30 + (20 if k % 2 else 0), -170 + k * 34)
        c.line_to(260, 170); c.line_to(260, -170); c.close_path(); c.set_source_rgba(*hx('F3E3B3', torn)); c.fill()
    c.restore()

def mantle(c, T, y0, amp, push):
    c.rectangle(0, y0, W, H - y0); c.set_source_rgba(*hx('E2572B')); c.fill()
    for k in range(4):
        cx = 140 + k * 270; cy = y0 + 230
        a = T * 1.2 * (1 if k % 2 else -1)
        for j in range(3):
            aa = a + j * 2.09; c.arc(cx + 90 * math.cos(aa), cy + 60 * math.sin(aa), 26, 0, 6.29); c.set_source_rgba(*hx(YEL, .8)); c.fill()
        c.save(); c.translate(cx, cy); c.scale(1.5, 1); c.arc(0, 0, 70, 0, 6.29); c.restore(); c.set_source_rgba(1, 1, 1, .3); c.set_line_width(5); c.stroke()

def L_(fn): return cairo_layer(fn)

def s_hook(fr, T):
    bg(fr, T, 'F3E3B3'); rays(fr, T, 'FFFFFF', .14)
    g = clamp((T - 1.2) / .8) if T > 1.2 else 0
    overlay(fr, L_(lambda c: strata(c, 100, 1380, 880, 9, 70, T, (2, 7), g, 140)))
    if T > 1.6: burst(fr, '???', 820, 1060, T - 1.6, r=110, col=YEL, size=60, rot=10)
    tape(fr, '1 BILLION YEARS', CX, 470, T + .3, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    title(fr, "EARTH'S MISSING PAGES", 600, T + .3, size=96, fill=YEL, rot=-2)

def s_missing(fr, T):
    fr[:] = essay_slide(T, [('NOT HIDDEN.', 'grey'), ('MISSING.', 'hl')], [S[1], wfind(1, 'missing')], size=128)
    lt = T - S[1]
    if T > wfind(1, 'canyon'): chip(fr, 'SEE IT IN THE GRAND CANYON', CX, 1150, T - wfind(1, 'canyon'), YEL, 38, -2)

def s_book(fr, T):
    lt = T - S[2]; bg(fr, T, 'F7E3C8'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'ROCKS = A BOOK', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    def dr(c):
        book(c, CX, 860, 1.0 * back(clamp(lt / .35)), T)
        strata(c, 200, 1380, 680, 5, 60, T, None, 0, 0)
    overlay(fr, L_(dr))
    if T > wfind(2, 'oldest'): chip(fr, 'OLDEST AT THE BOTTOM', CX, 1340, T - wfind(2, 'oldest'), YEL, 38, -2)

def s_granite(fr, T):
    lt = T - S[3]; bg(fr, T, 'F6D5DA'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'GRAND CANYON', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: strata(c, 100, 1380, 880, 4, 80, T, None, 0, 300)))
    chip(fr, 'YOUNG LAYERS: ~540 MILLION YRS', CX, 860, lt - .3, 'FFFFFF', 30, -2)
    if T > wfind(3, 'granite'): chip(fr, 'GRANITE: 1+ BILLION YRS', CX, 1240, T - wfind(3, 'granite'), YEL, 34, 2)
    if T > wfind(3, 'billion'):
        overlay(fr, L_(lambda c: (c.move_to(100, 1080), c.line_to(980, 1080), c.set_source_rgba(*hx(RED)), c.set_line_width(12), c.set_dash([26, 14]), c.stroke(), c.set_dash([]))))
        title(fr, 'RIGHT ON TOP', 600, T - wfind(3, 'billion'), size=110, fill=YEL)

def s_gone(fr, T):
    fr[:] = essay_slide(T, [('EVERYTHING IN BETWEEN?', 'grey'), ('GONE.', 'hl')], [S[4], wfind(4, 'gone')], size=90)
    overlay(fr, L_(lambda c: book(c, CX, 1150, .7, T, clamp((T - wfind(4, 'gone')) / .4) if T > wfind(4, 'gone') else 0)))

def s_world(fr, T):
    lt = T - S[5]; bg(fr, T, 'D6EEF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'NOT JUST ARIZONA', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    t1 = wfind(5, 'world')
    overlay(fr, L_(lambda c: globe(c, CX, 1030, 320 * back(clamp(lt / .35)) + .01, T, clamp((T - wfind(5, 'same')) / 1.5) if T > wfind(5, 'same') else 0)))
    if T > t1: title(fr, 'WORLDWIDE GAP', 600, T - t1, size=110, fill=YEL)
    chip(fr, 'EUROPE  AFRICA  ASIA  AUSTRALIA', CX, 1390, T - wfind(5, 'same') - .4, YEL, 30, -2)

def s_model(fr, T):
    lt = T - S[6]; bg(fr, T, 'E4DCEF'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THE NEW IDEA', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    overlay(fr, L_(lambda c: (mantle(c, T, 1040, 0, 0), strata(c, 100, 1040, 880, 3, 70, T, None, 0, 0))))
    if T > wfind(6, 'pages'): burst(fr, 'WHO DID IT?', 800, 780, T - wfind(6, 'pages'), r=120, col=YEL, size=34, rot=8)
    if T > wfind(6, 'hot'): title(fr, 'HOT ROCK BELOW', 600, T - wfind(6, 'hot'), size=104, fill=YEL); chip(fr, 'MANTLE', 300, 1300, T - wfind(6, 'hot'), 'FFFFFF', 44, -3)
    if T > wfind(6, 'australian'): chip(fr, 'UNIV. OF WOLLONGONG', 300, 800, T - wfind(6, 'australian'), CYAN, 32, -4)

def s_up(fr, T):
    lt = T - S[7]; bg(fr, T, 'C9DDF0'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'UP... AND SCRAPED', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    lift = 160 * eout(clamp(lt / 1.5)); t2 = wfind(7, 'scraped')
    g = clamp((T - t2) / 1.2) if T > t2 else 0
    def dr(c):
        mantle(c, T, 1240, 0, 0)
        c.save(); c.translate(0, -lift); strata(c, 160, 1240, 760, 6, 60, T, (3, 6), g, 0)
        c.restore()
        if T > t2:
            for k in range(6):
                u = (T * 1.2 + k / 6) % 1; c.move_to(100 + 880 * u, 800 + 40 * k % 120); c.line_to(140 + 880 * u, 820 + 40 * k % 120); c.set_source_rgba(*hx(CYAN, 1 - u)); c.set_line_width(8); c.stroke()
    overlay(fr, L_(dr))
    if T > wfind(7, 'continents'): title(fr, 'CONTINENTS PUSHED UP', 600, T - wfind(7, 'continents'), size=88, fill=YEL)
    if T > t2: chip(fr, 'WIND + RAIN', 800, 760, T - t2, YEL, 40, 4)

def s_sink(fr, T):
    lt = T - S[8]; bg(fr, T, 'DCE8C2'); rays(fr, T, 'FFFFFF', .1)
    tape(fr, 'THEN IT SANK', CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    sea_u = clamp((T - wfind(8, 'sea')) / 1) if T > wfind(8, 'sea') else 0
    nl = clamp((T - wfind(8, 'new')) / 1.2) if T > wfind(8, 'new') else 0
    def dr(c):
        strata(c, 100, 1380, 880, 3, 70, T, None, 0, 140)
        if sea_u > 0:
            c.rectangle(100, 1170 - 260 * sea_u, 880, 260 * sea_u); c.set_source_rgba(*hx('5FB0E0', .7)); c.fill()
        if nl > 0:
            for k in range(3):
                if nl > k / 3:
                    y = 1170 - (k + 1) * 50; c.rectangle(100, y, 880, 50); col = hx(['E8C07A', 'D98B4E', 'C9A66B'][k]); c.set_source_rgba(*col); c.fill_preserve(); ink(c, 5); c.stroke()
        c.move_to(100, 1170); c.line_to(980, 1170); c.set_source_rgba(*hx(RED)); c.set_line_width(10); c.set_dash([24, 14]); c.stroke(); c.set_dash([])
    overlay(fr, L_(dr))
    if T > wfind(8, 'scar'): chip(fr, 'THE SCAR = THE GAP', 700, 1300, T - wfind(8, 'scar'), YEL, 36, 3)

def s_end(fr, T):
    fr[:] = essay_slide(T, [('A MODEL, NOT PROOF.', 'grey'), ('NOT LOST BY CHANCE.', 'hl')], [S[9], wfind(9, 'pages')], size=104)
    overlay(fr, L_(lambda c: strata(c, 240, 1340, 600, 6, 50, T, (2, 4), 1.0, 100)))
    chip(fr, 'NATURE, 2026', CX, 870, T - S[9] - .3, YEL, 34, -2)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_missing), (S[3], s_book), (S[4], s_granite), (S[5], s_gone), (S[6], s_world), (S[7], s_model), (S[8], s_up), (S[9], s_sink), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (1.2, wfind(4, 'gone'), wfind(7, 'scraped')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Illustrations. Study: Dhungana & Flament, Nature (2026)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
