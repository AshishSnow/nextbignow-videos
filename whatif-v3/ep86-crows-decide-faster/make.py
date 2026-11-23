import sys; sys.path.insert(0, '/home/claude/samples'); from essay import *
D = '/home/claude/crow'; cx = Ctx(D, 86, 9); S = cx.S
from PIL import Image as _I
def ldst(p, w):
    if not os.path.exists(p): return None
    im = _I.open(p).convert('RGBA'); r = w / im.width; return np.array(im.resize((w, int(im.height * r)), _I.LANCZOS))
CROW = ldst(D + '/st/crow.png', 720); HEAD = ldst(D + '/st/crowhead.png', 760); CROWS = ldst(D + '/st/crow.png', 360); CROWM = ldst(D + '/st/crow.png', 520)
def eye(c, x, y, T, t0, s=1.0):
    k = (T - t0) % 1.6; close = 1 - min(1, abs(k - .2) / .12) if k < .4 else 0
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-120, 0); c.curve_to(-60, -80, 60, -80, 120, 0); c.curve_to(60, 80, -60, 80, -120, 0); c.close_path()
    c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, 0, 40, 0, 6.29); c.set_source_rgba(*hx('3A7BD5')); c.fill(); c.arc(0, 0, 18, 0, 6.29); c.set_source_rgba(0, 0, 0, 1); c.fill()
    if close > 0:
        c.move_to(-122, 0); c.curve_to(-60, -80, 60, -80, 122, 0); c.line_to(122, 0 - 80 + 80 * (1 - close) + 0)
        c.curve_to(60, -80 + 160 * close, -60, -80 + 160 * close, -122, 0); c.close_path(); c.set_source_rgba(*hx('E8B89A')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()
def screen(c, x, y, T, w=560, h=400):
    c.rectangle(x - w / 2 + 12, y - h / 2 + 14, w, h); c.set_source_rgba(0, 0, 0, .3); c.fill()
    c.rectangle(x - w / 2 - 22, y - h / 2 - 22, w + 44, h + 44); c.set_source_rgba(*hx('2A2A2E')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.rectangle(x - w / 2, y - h / 2, w, h); c.set_source_rgba(.06, .07, .09, 1); c.fill()
    rng = np.random.default_rng(7)
    for k in range(60):
        x0, y0 = rng.uniform(-w / 2 + 20, w / 2 - 20), rng.uniform(-h / 2 + 20, h / 2 - 20)
        right = k % 10 < 7; vx = 120 if right else rng.uniform(-120, 120); vy = 0 if right else rng.uniform(-120, 120)
        px = x + ((x0 + vx * T + w / 2) % (w - 30)) - w / 2 + 15; py = y + ((y0 + vy * T + h / 2) % (h - 30)) - h / 2 + 15
        c.arc(px, py, 6, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill()
    for sx, col in ((-1, '888888'), (1, RED)):
        c.arc(x + sx * (w / 2 + 70), y, 34, 0, 6.29); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()
def race(fr, T, t1, t2, y0=900):
    def dr(c):
        for k, (lab, ms, col, t0) in enumerate((('CROW', 235, RED, t1), ('PEOPLE', 470, '8C847A', t2))):
            if T < t0: continue
            u = eout(clamp((T - t0) / (.5 + .5 * k))); y = y0 + k * 220; w_ = 820 * ms / 470 * u
            c.rectangle(130 + 8, y + 8, w_, 120); c.set_source_rgba(0, 0, 0, .25); c.fill()
            c.rectangle(130, y, w_, 120); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    overlay(fr, cairo_layer(dr))
    for k, (lab, ms, t0) in enumerate((('CROW  ~235 ms', 235, t1), ('PEOPLE  ~2x longer', 470, t2))):
        small(fr, lab, 130, y0 + k * 220 + 135, T, t0 + .3, size=34)
def neurons(c, T, t0, x=CX, y=1080):
    for r in range(8):
        yy = y - 220 + r * 62
        c.move_to(140, yy); c.line_to(940, yy); c.set_source_rgba(*hx('FFFFFF', .2)); c.set_line_width(2); c.stroke()
        rng = np.random.default_rng(r)
        for k in range(40):
            tt = rng.uniform(0, 1.2); xx = 140 + tt / 1.2 * 800
            if T - t0 < tt: continue
            hot = tt > .25 and r % 2 == 0
            c.move_to(xx, yy - 22); c.line_to(xx, yy + 22); c.set_source_rgba(*hx(RED if hot else 'BBBBBB')); c.set_line_width(4 if hot else 3); c.stroke()
    xm = 140 + 70 / 1200 * 800 * 4.0
    if T - t0 > .5:
        c.set_dash([14, 10]); c.move_to(xm, y - 260); c.line_to(xm, y + 260); c.set_source_rgba(*hx(YEL)); c.set_line_width(5); c.stroke(); c.set_dash([])
def frame(T):
    dark = False
    if T < S[1]:
        fr = base(False); header(fr, cx, 1, T, False)
        headline(fr, [('FASTER THAN', 'main'), ('YOU CAN BLINK.', 'hl')], T, [0, cx.wf(0, 'blink') - .3])
        cut(fr, CROW, 430, 1110, T, 0, 1.0, -3, glow=True)
        overlay(fr, cairo_layer(lambda c: eye(c, 830, 820, T, .6, .8)))
    elif T < S[2]:
        fr = base(True); header(fr, cx, 2, T, True); dark = True
        headline(fr, [('TWICE AS FAST', 'hl'), ('AS YOU.', 'main')], T, [S[1], cx.wf(1, 'you')], dark=True)
        cut(fr, CROWM, CX, 1120, T, S[1] + .1, 1.0, 4, glow=True)
        burst(fr, '2X', 840, 1250, T - cx.wf(1, 'twice'), r=110, col=YEL, size=80, rot=8)
    elif T < S[4]:
        fr = base(False); header(fr, cx, 3, T, False)
        headline(fr, [('THE TEST:', 'grey'), ('WHICH WAY?', 'hl')], T, [S[2], cx.wf(3, 'which')])
        overlay(fr, cairo_layer(lambda c: screen(c, 480, 1000, T)))
        cut(fr, CROWS, 860, 1270, T, S[2] + .3, 1.0, -8)
        if T > cx.wf(3, 'peck'):
            def arr(c): arrow(c, 760, 760, 860, 950, RED, 22)
            overlay(fr, cairo_layer(arr)); small(fr, 'PECK THAT SIDE', 700, 690, T, cx.wf(3, 'peck'), col=rgb(RED), size=34)
        small(fr, 'Most dots move one way', 200, 1260, T, S[2] + 1.0, size=32)
    elif T < S[5]:
        fr = base(True); header(fr, cx, 4, T, True); dark = True
        tq = cx.wf(4, 'quarter')
        headline(fr, [('A QUARTER', 'main'), ('OF A SECOND.', 'hl')], T, [S[4], tq], dark=True)
        def watch(c):
            x, y = CX, 1080; c.arc(x, y, 230, 0, 6.29); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 10); c.stroke()
            c.rectangle(x - 30, y - 290, 60, 50); c.set_source_rgba(*hx(RED)); c.fill_preserve(); ink(c, 6); c.stroke()
            u = clamp((T - S[4]) / 1.6) * .25
            c.move_to(x, y); c.arc(x, y, 210, -math.pi / 2, -math.pi / 2 + 6.283 * u); c.close_path(); c.set_source_rgba(*hx(RED)); c.fill()
            c.arc(x, y, 230, 0, 6.29); ink(c, 10); c.stroke()
        overlay(fr, cairo_layer(watch))
        if T > tq: burst(fr, '0.235 SEC', 830, 1330, T - tq, r=125, col=YEL, size=38, rot=8)
    elif T < S[6]:
        fr = base(False); header(fr, cx, 5, T, False)
        headline(fr, [('PEOPLE?', 'main'), ('TWICE AS LONG.', 'hl')], T, [S[5], cx.wf(5, 'twice')])
        race(fr, T, S[5] + .3, cx.wf(5, 'twice'))
    elif T < S[7]:
        fr = base(True); header(fr, cx, 6, T, True); dark = True
        headline(fr, [('THE WILD PART:', 'grey'), ('70 MILLISECONDS.', 'hl')], T, [S[6], cx.wf(6, 'seventy')], dark=True, size=116)
        overlay(fr, cairo_layer(lambda c: neurons(c, T, cx.wf(6, 'brain'))))
        small(fr, 'Brain cells already "chose" the answer', CX, 1370, T, cx.wf(6, 'answer'), True, col=rgb(YEL), size=32, center=True)
    elif T < S[8]:
        fr = base(False); header(fr, cx, 7, T, False)
        headline(fr, [('NO HUMAN-STYLE', 'main'), ('BRAIN LAYER.', 'hl')], T, [S[7], cx.wf(7, 'layer')])
        cut(fr, CROWM, CX, 1130, T, S[7] + .1, 1.0, -4, glow=True)
        if T > cx.wf(7, 'layer'): burst(fr, 'STILL FASTER', 830, 1330, T - cx.wf(7, 'layer') - .2, r=125, col=YEL, size=34, rot=8)
    elif T < S[9]:
        fr = base(True); header(fr, cx, 8, T, True); dark = True
        headline(fr, [('ONLY 2 CROWS.', 'hl'), ('MORE TESTS NEEDED.', 'grey')], T, [S[8], cx.wf(8, 'more')], dark=True, size=112)
        for k in range(2): cut(fr, CROWS, 330 + k * 420, 1110, T, S[8] + .2 + k * .2, 1.0, [-6, 6][k], glow=True)
    else:
        fr = base(False); header(fr, cx, 9, T, False)
        headline(fr, [('IT ALREADY', 'main'), ('DECIDED.', 'hl')], T, [S[9], cx.wf(9, 'decided')])
        cut(fr, HEAD, CX, 1120, T, S[9], 1.0 + .08 * clamp((T - S[9]) / 3), -2, glow=True)
    pill(fr, cx, T, dark)
    for at in (cx.wf(1, 'twice'), cx.wf(6, 'seventy')):
        a, b = shake(T, at)
        if a or b: fr[:] = cv2.warpAffine(fr, np.float32([[1, 0, a], [0, 1, b]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    return fr
EV = [(0.05, '2604', .35), (.6, '2364', .3), (S[1] - .05, '2627', .4), (cx.wf(1, 'twice'), '788', .5), (S[2] - .1, '1461', .4)] + \
     [(S[2] + .3 + k * .12, '2354', .08) for k in range(14)] + [(cx.wf(3, 'peck'), '2357', .45), (S[4] - .1, '2627', .4)] + \
     [(S[4] + k * .2, '2354', .25) for k in range(8)] + [(cx.wf(4, 'quarter'), '788', .45), (S[5] - .1, '1461', .4), (S[5] + .3, '2604', .35), (cx.wf(5, 'twice'), '2357', .4),
     (S[6] - .1, '2627', .4), (cx.wf(6, 'seventy'), '1143', .55), (S[7] - .1, '1461', .4), (cx.wf(7, 'layer'), '2357', .4), (S[8] - .1, '2627', .4),
     (S[9] - .1, '1202', .4), (cx.wf(9, 'decided'), '788', .45), (cx.END, '1471', .5)]
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for t in sys.argv[2:]: Image.fromarray(frame(float(t))).save(f'{D}/st_{t}.jpg', quality=88)
    else:
        th = thumb(D + '/thumb_crow.jpg', [('CROWS THINK', 'main'), ('2X FASTER?!', 'hl')], ldst(D + '/st/crow.png', 860), (CX, 1250), 'FASTER THAN YOU')
        sfx_mix(D, EV, cx.END + 1.6)
        plat = sys.argv[1]
        render2(D, frame, cx, plat, f'{D}/crow_{plat}.mp4', th if plat == 'yt' else None, ig_line='A BIRD NERD.')
        print('done', plat)
