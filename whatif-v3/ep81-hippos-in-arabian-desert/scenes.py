import sys, os, json, math
sys.path.insert(0, '/home/claude/hippo')
from kit import *
D = '/home/claude/hippo'
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


def sky(fr, T, wet=0.0):
    top = np.array(rgb('F6C46A'), np.float32) * (1 - wet) + np.array(rgb('8FD0E8'), np.float32) * wet
    bot = np.array(rgb('F9E3B0'), np.float32) * (1 - wet) + np.array(rgb('DFF3E4'), np.float32) * wet
    yy = np.linspace(0, 1, H)[:, None, None]; fr[:] = np.broadcast_to(top * (1 - yy) + bot * yy, (H, W, 3)).astype(np.uint8)
    fr[:] = (fr.astype(np.float32) * .55 + paper(None).astype(np.float32) * .45).astype(np.uint8)

def land(fr, T, wet=0.0, y0=1180):
    def dr(c):
        c.arc(820, 760, 90, 0, 2 * math.pi); c.set_source_rgba(1, .92, .5, .9 - .3 * wet); c.fill()
        if wet > 0:
            c.rectangle(0, y0 - 10, W, 90 * wet + 10); c.set_source_rgba(*hx('3A8FC2', .95)); c.fill()
            for k in range(6):
                c.move_to(60 + k * 170 + 20 * math.sin(T * 2 + k), y0 + 20 * wet); c.rel_line_to(70, 0); c.set_source_rgba(1, 1, 1, .6 * wet); c.set_line_width(5); c.stroke()
            for k in range(7):
                x = 80 + k * 150; c.move_to(x, y0); c.line_to(x - 20, y0 - 90 * wet); c.move_to(x, y0); c.line_to(x + 18, y0 - 80 * wet)
                c.set_source_rgba(*hx('3F7D3A', wet)); c.set_line_width(8); c.stroke()
        for k, (cx, h, col, dy) in enumerate(((150, 120, 'E9BE73', 0), (820, 150, 'E2AE5A', 30), (420, 110, 'D69A45', 140))):
            yb = y0 + 90 * wet + dy; hh = h * (1 - .6 * wet)
            c.move_to(cx - 700, yb + 60); c.curve_to(cx - 300, yb - hh, cx + 200, yb - hh, cx + 700, yb + 60)
            c.line_to(cx + 700, H); c.line_to(cx - 700, H); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    overlay(fr, cairo_layer(dr))

def card(fr, items, T, t0, cx=CX, cy=1020):
    def dr(c):
        c.save(); c.translate(cx, cy); c.rotate(-.03)
        c.rectangle(-300 + 12, -330 + 14, 600, 660); c.set_source_rgba(0, 0, 0, .35); c.fill()
        c.rectangle(-300, -330, 600, 660); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 7); c.stroke()
        c.restore()
    overlay(fr, cairo_layer(dr))
    title(fr, 'MENU', cy - 260, 1.0, size=80, fill=RED, rot=-2, cx=cx)
    for k, (w_, name, img) in enumerate(items):
        tk = t0[k]
        if T > tk:
            y = cy - 170 + k * 118
            tape(fr, name, cx + 60, y, T - tk, col=[YEL, 'FFFFFF', CYAN, 'FFFFFF', YEL][k], size=40, font=LUCKY, rot=[-2, 1, -1, 2, -2][k])
            s_ = st(img, h=105)
            if s_ is not None: put_rgba(fr, s_, cx - 200, y, back(clamp((T - tk) / .3)), 1.0, 0)

def s_hook(fr, T):
    wet = ease(clamp((T - 1.2) / 1.2)); sky(fr, T, wet); land(fr, T, wet)
    tape(fr, 'THE ARABIAN DESERT', CX, 470, T, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    th = wfind(0, 'hippos')
    if T < th: sk(fr, st('camel', w=420), 380, 1020, T, 0, 1.0, 3, T)
    if T > th:
        title(fr, 'HAD HIPPOS', 600, T - th, size=130, fill=YEL)
        sk(fr, st('hippo', w=520), 600, 1050, T, 0, 1.0, -4, T - th)
    if T > wfind(0, 'hunting'): burst(fr, 'HUNTED!', 230, 860, T - wfind(0, 'hunting'), r=110, col=RED, size=44, rot=-8)

def s_question(fr, T):
    lt = T - S[1]; sky(fr, T); land(fr, T)
    sk(fr, st('hippo', w=420), CX, 1020, T, 0, 1.0, 6, lt)
    title(fr, 'HIPPOS?', 470, lt, size=150, fill='FFFFFF', rot=-3)
    if T > wfind(1, 'saudi'): title(fr, 'IN SAUDI ARABIA?', 640, T - wfind(1, 'saudi'), size=96, fill=YEL)
    burst(fr, '?!', 860, 1300, lt - .3, r=90, col=RED, size=80)

def s_lake(fr, T):
    lt = T - S[2]; wet = ease(clamp((lt - .6) / 2.0)); sky(fr, T, wet); land(fr, T, wet)
    counter_t = wfind(2, 'hundred')
    if T > counter_t:
        v = int(125000 * eout(clamp((T - counter_t) / 1.2))); title(fr, f'{v:,} YEARS AGO', 470, T - counter_t, size=88, fill='FFFFFF', rot=-2)
    if T > wfind(2, 'lake shore'): title(fr, 'A LAKE SHORE', 610, T - wfind(2, 'lake shore'), size=110, fill=YEL)
    if T > wfind(2, 'mundafan'): chip(fr, 'LAKE MUNDAFAN', CX, 1320, T - wfind(2, 'mundafan'), CYAN, 46, -2)

def s_camp(fr, T):
    lt = T - S[3]; sky(fr, T, .6); land(fr, T, .6, 1300)
    sk(fr, st('point', w=300), 300, 1000, T, 0, 1.0, -12, lt - .2)
    sk(fr, st('point', w=260), 560, 1060, T, 1, 1.0, 18, lt - .4)
    sk(fr, st('point', w=280), 810, 990, T, 2, 1.0, -4, lt - .6)
    tape(fr, 'AN ANCIENT CAMPSITE', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    tf = wfind(3, 'five thousand')
    if T > tf:
        v = int(5511 * eout(clamp((T - tf) / 1.0))); title(fr, f'{v:,} STONE TOOLS', 610, T - tf, size=96, fill=YEL)

def s_menu(fr, T):
    lt = T - S[4]; fr[:] = paper('E8C9A0', .6); rays(fr, T, 'FFFFFF', .1)
    items = [('hippos', 'HIPPOS', 'hippo'), ('ostriches', 'OSTRICHES', 'ostrich'), ('camels', 'CAMELS', 'camel'), ('gazelles', 'GAZELLES', 'gazelle'), ('buffalo', 'BUFFALO', 'buffalo')]
    card(fr, items, T, [wfind(4, w_) - .1 for w_, _, _ in items])
    tape(fr, "WHAT WAS ON THE MENU", CX, 470, lt, col=RED, size=58, font=LUCKY, rot=-2, tcol='FFFFFF')

def s_poison(fr, T):
    lt = T - S[5]; fr[:] = paper('C9E4B4', .55); rays(fr, T, 'FFFFFF', .1)
    tape(fr, "BUT HERE'S THE TWIST", CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    sk(fr, st('point', w=340), 330, 960, T, 0, 1.0, -30, lt - .3)
    tp = wfind(5, 'plant')
    if T > tp:
        ph = photo('acok', 420, 420, (.5, .5))
        if ph is not None: put_rgba(fr, ph, 780, 980, back(clamp((T - tp) / .3)), 1.0, 4)
    if T > wfind(5, 'poison'):
        title(fr, 'ARROW POISON', 620, T - wfind(5, 'poison'), size=116, fill=YEL)
        def drip(c):
            for k in range(4):
                f = ((T - wfind(5, 'poison')) * .9 + k / 4) % 1; x = 380 + 30 * k - 40; y = 1180 + f * 200
                c.arc(x, y, 14 * (1 - f * .4), 0, 2 * math.pi); c.set_source_rgba(*hx(GREEN, 1 - f)); c.fill()
        overlay(fr, cairo_layer(drip))
    chip(fr, 'TRACES ON SPEAR POINTS', CX, 1330, T - wfind(5, 'spear'), 'FFFFFF', 40, 2)

def s_proof(fr, T):
    lt = T - S[6]; fr[:] = paper('E8DCC0', .5)
    sk(fr, st('point', w=380), CX, 1030, T, 0, 1.0, -20, lt)
    tape(fr, 'NO PROOF OF A POISON KILL... YET', CX, 470, lt, col='FFFFFF', size=46, font=LUCKY, rot=-2)
    tw = wfind(6, 'hundred')
    if T > tw: stat(fr, '125,000', 'YEARS AGO', CX, 640, T - tw, RED, -3, 140)

def s_hall(fr, T):
    lt = T - S[7]; rain = clamp((T - wfind(7, 'rained')) / .5) if T > wfind(7, 'rained') else 0
    sky(fr, T, .2 + .6 * rain); land(fr, T, .8 * rain)
    def corridor(c):
        a = 1 - rain
        c.set_dash([30, 20]); c.move_to(80, 900); c.line_to(1000, 900); c.set_source_rgba(*hx('1C1614', .7 * a)); c.set_line_width(10); c.stroke(); c.set_dash([])
        if a > 0:
            c.move_to(1000, 900); c.line_to(960, 870); c.line_to(960, 930); c.close_path(); c.set_source_rgba(*hx('1C1614', .7 * a)); c.fill()
        if rain > 0:
            for k in range(60):
                rng = np.random.default_rng(k); x = rng.uniform(0, W); y = (rng.uniform(0, H) + T * 900) % 1100 + 200
                c.move_to(x, y); c.rel_line_to(-8, 34); c.set_source_rgba(.3, .5, .9, .6 * rain); c.set_line_width(4); c.stroke()
    overlay(fr, cairo_layer(corridor))
    tape(fr, 'NOT JUST A HALLWAY', CX, 470, lt, col='FFFFFF', size=60, font=LUCKY, rot=-2)
    if T > wfind(7, 'rained'): title(fr, 'PEOPLE LIVED HERE', 610, T - wfind(7, 'rained'), size=100, fill=YEL)

def s_next(fr, T):
    lt = T - S[8]; fr[:] = paper(RED, .8); rays(fr, T, 'FFFFFF', .14)
    title(fr, 'SO WHAT', 860, lt, size=170, fill='FFFFFF'); title(fr, 'HAPPENS NEXT?', 1060, lt - .15, size=130, fill=YEL)

def s_space(fr, T):
    lt = T - S[9]; fr[:] = paper('0B1026', .9)
    ph = photo('sat', 820, 820, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1040, back(clamp(lt / .35)), 1.0, -2)
    def dots(c):
        rng = np.random.default_rng(4)
        for k in range(int(clamp((lt - .8) / 2.5) * 60)):
            x, y = rng.uniform(260, 820), rng.uniform(760, 1320); c.arc(x, y, 9, 0, 2 * math.pi)
            c.set_source_rgba(*hx(CYAN)); c.fill_preserve(); ink(c, 3); c.stroke()
    overlay(fr, cairo_layer(dots))
    tape(fr, 'SPOTTED FROM SPACE', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    if T > wfind(9, 'thousands'): title(fr, 'THOUSANDS OF OLD LAKES', 610, T - wfind(9, 'thousands'), size=86, fill=YEL)

def s_hidden(fr, T):
    lt = T - S[10]; sky(fr, T); land(fr, T, 0, 1000)
    def dig(c):
        c.save(); c.rectangle(0, 1100, W, 500); c.clip()
        u = clamp(lt / 2.0); c.arc(CX, 1260, 210 * u + 1, 0, 2 * math.pi); c.set_source_rgba(*hx('8A5A2B')); c.fill(); c.restore()
    overlay(fr, cairo_layer(dig))
    if lt > .8: sk(fr, st('point', w=200), CX - 60, 1260, T, 0, 1.0, -30, lt - .8)
    if lt > 1.1: sk(fr, st('point', w=170), CX + 80, 1290, T, 1, 1.0, 25, lt - 1.1)
    tape(fr, 'EACH ONE COULD HIDE A CAMP', CX, 470, lt, col='FFFFFF', size=52, font=LUCKY, rot=-2)
    if T > wfind(10, 'sand'): title(fr, 'UNDER THE SAND', 610, T - wfind(10, 'sand'), size=110, fill=YEL)

def s_end(fr, T):
    lt = T - S[11]; sky(fr, T, .5); land(fr, T, .5)
    sk(fr, st('hippo', w=380), CX, 1000, T, 0, 1.0, -4)
    title(fr, 'WOULD YOU DIG?', 560, lt, size=110, fill=YEL)
    if T > S[12]:
        burst(fr, 'YES', 230, 1330, T - S[12], r=100, col=GREEN, size=54, rot=-8)
        burst(fr, 'NO', 850, 1330, T - S[12] - .15, r=100, col=RED, size=54, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_question), (S[3], s_lake), (S[4], s_camp), (S[5], s_menu), (S[6], s_poison), (S[7], s_proof), (S[8], s_hall),
           (S[9], s_next), (S[10], s_space), (S[11], s_hidden), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'hippos'), wfind(5, 'twist'), wfind(5, 'poison')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
