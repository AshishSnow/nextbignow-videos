import sys, os, json, math
sys.path.insert(0, '/home/claude/vortex')
from kit import *
D = '/home/claude/vortex'
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


def bg(fr, T, tint='D6E9F5', m=.55): fr[:] = paper(tint, m)

def vortex(c, cx, cy, T, R=330, brk=0.0, col=CYAN):
    # spinning arrows ring; brk 0..1 = how broken (segments drift apart, wobble)
    n = 10
    for k in range(n):
        a0 = k / n * 2 * math.pi + T * 1.6 * (1 - .7 * brk); span = 2 * math.pi / n * .72
        off = brk * (40 + 30 * math.sin(k * 2.3)); rr = R + off * math.sin(k * 1.7 + T)
        dx = brk * 90 * math.cos(k * 1.9); dy = brk * 90 * math.sin(k * 2.7)
        c.save(); c.translate(cx + dx, cy + dy)
        c.arc(0, 0, rr, a0, a0 + span); c.set_source_rgba(*hx('1C1614')); c.set_line_width(34); c.stroke()
        c.arc(0, 0, rr, a0, a0 + span); c.set_source_rgba(*hx(col)); c.set_line_width(22); c.stroke()
        ae = a0 + span; x, y = rr * math.cos(ae), rr * math.sin(ae)
        c.move_to(x + 30 * math.cos(ae + math.pi / 2), y + 30 * math.sin(ae + math.pi / 2))
        c.line_to(x + 26 * math.cos(ae), y + 26 * math.sin(ae)); c.line_to(x - 26 * math.cos(ae), y - 26 * math.sin(ae)); c.close_path()
        c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 4); c.stroke()
        c.restore()

def earth_top(fr, x, y, w, t=1.0):
    sc = back(clamp(t / .35))
    if sc <= 0: return
    def dr(c):
        r = w / 2 * sc; rng = np.random.default_rng(5)
        c.arc(x + 10, y + 14, r, 0, 2 * math.pi); c.set_source_rgba(0, 0, 0, .35); c.fill()
        g = cairo.RadialGradient(x - r * .3, y - r * .3, r * .1, x, y, r)
        g.add_color_stop_rgb(0, .35, .65, .95); g.add_color_stop_rgb(1, .05, .25, .55)
        c.arc(x, y, r, 0, 2 * math.pi); c.set_source(g); c.fill()
        c.save(); c.arc(x, y, r, 0, 2 * math.pi); c.clip()
        for k in range(7):
            a = k / 7 * 2 * math.pi + .3
            cx_, cy_ = x + r * .9 * math.cos(a), y + r * .9 * math.sin(a)
            c.save(); c.translate(cx_, cy_); c.rotate(a); c.scale(1.0, .55); c.arc(0, 0, r * (.32 + .08 * math.sin(k * 3)), 0, 2 * math.pi); c.restore()
            c.set_source_rgba(.42, .62, .3, 1); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(3); c.stroke()
        pts = []
        for k in range(24):
            a = k / 24 * 2 * math.pi; rr = r * (.42 + .1 * math.sin(k * 2.7) + .05 * math.cos(k * 5.1))
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        c.move_to(*pts[0]); [c.line_to(*p_) for p_ in pts[1:]]; c.close_path()
        c.set_source_rgba(.97, .99, 1, 1); c.fill_preserve(); c.set_source_rgba(.6, .8, .95, 1); c.set_line_width(4); c.stroke()
        c.restore()
        c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.set_line_width(8); c.stroke()
        c.select_font_face('Luckiest Guy'); c.set_font_size(30 * sc); e = c.text_extents('N. POLE'); c.move_to(x - e.width / 2, y + 10); c.set_source_rgba(.2, .3, .45, 1); c.show_text('N. POLE')
    overlay(fr, cairo_layer(dr))

def s_hook(fr, T):
    fr[:] = paper('0B1730', .9)
    tb = wfind(0, 'broke')
    brk = eout(clamp((T - tb + .2) / .8)) if T > tb - .2 else 0
    earth_top(fr, CX, 1060, 520, T + .4)
    overlay(fr, cairo_layer(lambda c: vortex(c, CX, 1060, T, 360, brk)))
    tape(fr, 'ABOVE THE NORTH POLE', CX, 470, T, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    if T > tb - .2: title(fr, 'IT JUST BROKE', 610, T - tb + .2, size=120, fill=YEL)

def s_record(fr, T):
    lt = T - S[1]; fr[:] = paper('0B1730', .9)
    earth_top(fr, CX, 1060, 520)
    overlay(fr, cairo_layer(lambda c: vortex(c, CX, 1060, T, 360, 1.0)))
    title(fr, 'EARLIER THAN', 470, lt, size=110, fill='FFFFFF'); title(fr, 'EVER RECORDED', 610, lt - .15, size=110, fill=YEL)

def s_fence(fr, T):
    lt = T - S[2]; bg(fr, T, 'D6E9F5')
    earth_top(fr, CX, 1060, 480, lt)
    overlay(fr, cairo_layer(lambda c: vortex(c, CX, 1060, T, 330, 0)))
    def cold(c):
        for k in range(14):
            a = k / 14 * 2 * math.pi + T * .3; r = 120 + 60 * math.sin(T * 2 + k)
            x, y = CX + r * math.cos(a), 1060 + r * math.sin(a)
            c.arc(x, y, 16, 0, 2 * math.pi); c.set_source_rgba(*hx('FFFFFF')); c.fill_preserve(); c.set_source_rgba(*hx('3A7BD5')); c.set_line_width(4); c.stroke()
    if T > wfind(2, 'freezing'): overlay(fr, cairo_layer(cold))
    tape(fr, 'THE POLAR VORTEX', CX, 470, lt, col=RED, size=64, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(2, 'fence'): chip(fr, 'A SPINNING FENCE OF WIND', CX, 640, T - wfind(2, 'fence'), YEL, 44, 2)
    if T > wfind(2, 'locked'): chip(fr, 'COLD LOCKED INSIDE', CX, 1450 - 60, T - wfind(2, 'locked'), 'FFFFFF', 40, -2)

def s_flip(fr, T):
    lt = T - S[3]; bg(fr, T, 'E8E1D0'); rays(fr, T, 'FFFFFF', .08)
    tn = wfind(3, 'november')
    def cal(c):
        x, y = 290, 1000; u = back(clamp(lt / .4))
        c.save(); c.translate(x, y); c.scale(u, u); c.rotate(-.05)
        c.rectangle(-170 + 10, -190 + 12, 340, 380); c.set_source_rgba(0, 0, 0, .3); c.fill()
        c.rectangle(-170, -190, 340, 380); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 7); c.stroke()
        c.rectangle(-170, -190, 340, 100); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 7); c.stroke()
        c.restore()
    overlay(fr, cairo_layer(cal))
    if lt > .2:
        title(fr, 'NOV', 860, lt - .2, size=70, fill='FFFFFF', cx=290); title(fr, '10', 1050, lt - .2, size=170, fill=RED, cx=290)
    def arrows(c):
        flip = clamp((T - wfind(3, 'flipped')) / .6) if T > wfind(3, 'flipped') else 0
        for k in range(3):
            y = 860 + k * 150; d = 1 - 2 * flip
            c.save(); c.translate(790, y); c.scale(d, 1)
            c.move_to(-150, 0); c.line_to(110, 0); c.set_source_rgba(*hx(CYAN if flip < .5 else RED)); c.set_line_width(26); c.stroke()
            c.move_to(150, 0); c.line_to(90, -50); c.line_to(90, 50); c.close_path(); c.fill(); c.restore()
    overlay(fr, cairo_layer(arrows))
    tape(fr, 'THE WINDS FLIPPED', CX, 470, lt, col='FFFFFF', size=62, font=LUCKY, rot=-2)
    tr = wfind(3, 'earliest')
    if T > tr: stat(fr, '3 WEEKS', 'EARLIER THAN 1958 RECORD', CX, 640, T - tr, YEL, -3, 110)

def jet(c, T, amp, y0=1020, col=RED):
    c.move_to(80, y0)
    for x in range(80, W - 79, 8):
        c.line_to(x, y0 + amp * math.sin((x / W) * 2 * math.pi * 1.5 + T * 1.2))
    c.set_source_rgba(*hx('1C1614')); c.set_line_width(30); c.stroke_preserve(); c.set_source_rgba(*hx(col)); c.set_line_width(18); c.stroke()

def s_jet(fr, T):
    lt = T - S[4]; bg(fr, T, 'D6E9F5')
    amp = 60 + 220 * eout(clamp((T - wfind(4, 'bends')) / 1.0)) if T > wfind(4, 'bends') else 60
    def dr(c):
        c.rectangle(80, 720, W - 160, 600); c.set_source_rgba(*hx('B9D8EE')); c.fill_preserve(); ink(c, 6); c.stroke()
        c.save(); c.rectangle(80, 720, W - 160, 600); c.clip(); jet(c, T, amp)
        for k in range(10):
            x = 140 + k * 90; yy = 760 + (T * 60 + k * 37) % 520
            if yy < 1020 + amp * math.sin((x / W) * 2 * math.pi * 1.5 + T * 1.2):
                c.arc(x, yy, 14, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .95); c.fill()
        c.restore()
    overlay(fr, cairo_layer(dr))
    chip(fr, 'ARCTIC AIR', 250, 780, lt, 'FFFFFF', 34, -3)
    chip(fr, 'JET STREAM', 830, 1270, lt - .3, RED, 34, 3)
    tape(fr, 'WHERE DOES THE COLD GO?', CX, 470, lt, col='FFFFFF', size=56, font=LUCKY, rot=-2)
    if T > wfind(4, 'bends'): title(fr, 'WHEREVER IT BENDS', 610, T - wfind(4, 'bends'), size=96, fill=YEL)

def s_where(fr, T):
    lt = T - S[5]; bg(fr, T, 'C9DDF0')
    overlay(fr, cairo_layer(lambda c: jet(c, T, 260, 1040, CYAN)))
    tape(fr, 'AFTER PAST BREAKDOWNS', CX, 470, lt, col='FFFFFF', size=58, font=LUCKY, rot=-2)
    places = [('eastern', 'EASTERN U.S.', 'snow'), ('northern', 'NORTHERN EUROPE', 'icicle'), ('asia', 'ASIA', 'thermo')]
    for k, (w_, lab, img) in enumerate(places):
        tk = wfind(5, w_)
        if T > tk:
            x = [270, 810, 540][k]; y = [880, 880, 1200][k]
            ph = photo(img, 430, 290, (.5, .5))
            if ph is not None: put_rgba(fr, ph, x, y, back(clamp((T - tk) / .3)), 1.0, [-3, 3, -2][k])
            chip(fr, lab, x, y + 170, T - tk - .1, [YEL, CYAN, 'FFFFFF'][k], 34, [-3, 3, -2][k])
    if T > wfind(5, 'colder'): burst(fr, 'COLDER', 860, 1260, T - wfind(5, 'colder'), r=115, col=CYAN, size=44, rot=8)

def s_timer(fr, T):
    lt = T - S[6]; bg(fr, T, 'F2E6CF'); rays(fr, T, 'FFFFFF', .08)
    tape(fr, 'HOW LONG UNTIL IT HITS?', CX, 470, lt, col=RED, size=56, font=LUCKY, rot=-2, tcol='FFFFFF')
    tw = wfind(6, 'two')
    def bar(c):
        x0, x1, y = 120, 960, 1000
        c.rectangle(x0, y - 40, x1 - x0, 80); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 7); c.stroke()
        u = clamp((T - tw) / 1.0) if T > tw else 0
        c.rectangle(x0 + (x1 - x0) * .33, y - 40, (x1 - x0) * .67 * u, 80); c.set_source_rgba(*hx(CYAN)); c.fill()
        c.rectangle(x0, y - 40, x1 - x0, 80); ink(c, 7); c.stroke()
        tn = wfind(6, 'now')
        if T > tn:
            xx = x0 + (x1 - x0) * .4; c.move_to(xx, y - 80); c.line_to(xx, y + 80); c.set_source_rgba(*hx(RED)); c.set_line_width(10); c.stroke()
    overlay(fr, cairo_layer(bar))
    chip(fr, 'NOV 10', 140, 1100, lt - .2, 'FFFFFF', 32, -3)
    if T > tw: stat(fr, '2-6 WEEKS', 'TO REACH THE GROUND', CX, 650, T - tw, YEL, -3, 110)
    if T > wfind(6, 'now'): chip(fr, 'YOU ARE HERE', 460, 1110, T - wfind(6, 'now'), RED, 34, 2)
    if T > wfind(6, 'december'): chip(fr, 'DECEMBER', 820, 1110, T - wfind(6, 'december'), CYAN, 34, 3)

def s_maybe(fr, T):
    lt = T - S[7]; bg(fr, T, 'E8E1D0')
    ph = photo('plow', 760, 520, (.5, .5))
    if ph is not None: put_rgba(fr, ph, CX, 1020, back(clamp(lt / .35)), 1.0, -2)
    tape(fr, "IT'S NOT A PROMISE", CX, 470, lt, col=RED, size=62, font=LUCKY, rot=-2, tcol='FFFFFF')
    if T > wfind(7, 'barely'): title(fr, 'SOMETIMES: NOTHING', 610, T - wfind(7, 'barely'), size=96, fill=YEL); xstamp(fr, CX, 1020, T - wfind(7, 'barely') - .2, 1.1)

def s_end(fr, T):
    lt = T - S[8]; fr[:] = paper('0B1730', .9)
    earth_top(fr, CX, 1060, 520)
    overlay(fr, cairo_layer(lambda c: vortex(c, CX, 1060, T, 360, .7)))
    tape(fr, 'IF DECEMBER GETS BRUTAL...', CX, 470, lt, col='FFFFFF', size=54, font=LUCKY, rot=-2)
    if T > wfind(8, 'blame'): title(fr, 'BLAME THE WIND', 610, T - wfind(8, 'blame'), size=116, fill=YEL)
    if T > wfind(8, 'nineteen'): burst(fr, '19 MILES UP', 830, 1340, T - wfind(8, 'nineteen'), r=125, col=CYAN, size=36, rot=8)

def frame(T, plat='ig'):
    fr = np.zeros((H, W, 3), np.uint8)
    seq = [(S[1], s_hook), (S[2], s_record), (S[3], s_fence), (S[4], s_flip), (S[5], s_jet), (S[6], s_where), (S[7], s_timer), (S[8], s_maybe), (END, s_end)]
    for t1, fn in seq:
        if T < t1: fn(fr, T); break
    else:
        s_cta(fr, T, plat); return fr
    dx = dy = 0
    for at in (wfind(0, 'broke'), wfind(3, 'flipped'), wfind(6, 'now')):
        a, b = shake(T, at); dx += a; dy += b
    if dx or dy: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    if T < END: credit(fr, 'Images: Wikimedia Commons (credits in description)')
    subs(fr, T); logo(fr)
    return fr

if __name__ == '__main__':
    for a in sys.argv[2:]:
        Image.fromarray(frame(float(a))).save(f'{D}/out/st_{a}.jpg', quality=90); print(a)
