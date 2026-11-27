
# ================= v2 motion pass: heat-vision hook, 3D particle burst, zoom-into-plastic, microscope, camera + transitions
def thermal_inner(c, T, t, scan):
    """inside the microwave window: normal view, and a heat-vision view revealed left of the scan line"""
    sw = 22 * math.sin(T * 2.2); bx, by = -80 + sw, 40
    tiffin(c, bx, by, .72, 0)
    if scan <= 0: return
    xs = -290 + 420 * scan
    c.save(); c.rectangle(-290, -160, xs + 290, 320); c.clip()
    c.rectangle(-290, -160, 420, 320); c.set_source_rgba(*hx('12062E')); c.fill()
    g = cairo.RadialGradient(bx, by + 10, 10, bx, by + 10, 190)
    g.add_color_stop_rgba(0, 1, 1, .85, 1); g.add_color_stop_rgba(.35, 1, .78, .1, 1); g.add_color_stop_rgba(.7, .92, .15, .2, .9); g.add_color_stop_rgba(1, .35, .05, .5, 0)
    c.arc(bx, by + 10, 190, 0, 2 * math.pi); c.set_source(g); c.fill()
    rng = np.random.default_rng(9)
    for k in range(140):
        ang = rng.random() * 2 * math.pi; ph = (rng.random() + T * (.3 + .4 * rng.random())) % 1
        r = 60 + 230 * ph; x = bx + math.cos(ang) * r; y = by + math.sin(ang) * r * .75
        c.arc(x, y, 2 + 4 * rng.random(), 0, 2 * math.pi); c.set_source_rgba(1, 1, .6, .95 * (1 - ph)); c.fill()
    c.restore()
    if scan < 1:
        c.rectangle(xs - 3, -160, 6, 320); c.set_source_rgba(.6, 1, .9, 1); c.fill()
        lg = cairo.LinearGradient(xs - 60, 0, xs, 0); lg.add_color_stop_rgba(0, .6, 1, .9, 0); lg.add_color_stop_rgba(1, .6, 1, .9, .45)
        c.rectangle(xs - 60, -160, 60, 320); c.set_source(lg); c.fill()

def sc_h1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 2.6 if thumb else t
    ebg(fr, 'cream', T)
    k = ease(clamp((tt - .15) / 1.05))                      # pull back from the window to the whole microwave
    s = lerp(2.75, 1.12, k)
    wx, wy = lerp(CX + 80 * 2.75 + 0, CX, k), lerp(1060, 1100, k)   # window centre (-80,0 local) starts at screen centre
    scan = clamp((tt - 1.35) / .9)
    overlay(fr, cairo_layer(lambda c: microwave(c, wx, wy, s, T, True, lambda c2: thermal_inner(c2, T, tt, scan))))
    if k > .85: timer_txt(fr, wx + s * 230, wy - s * 115, 180 - tt * 30 if not thumb else 180)
    title_line(fr, [('प्लास्टिक डिब्बा', 0)], 380, tt + 1.0, 108)
    title_line(fr, [('माइक्रोवेव में?', 3)], 548, tt + 1.0, 120)
    if scan > .4 or thumb: note(fr, 'हीट विज़न में देखो', 790, 1430 - 60, 1.0 if thumb else tt - 1.75, 46, YL, -4)

def sc_h2(fr, T, t, l):
    ebg(fr, 'black', T)
    p = back(clamp(t / .35)); b = clamp((t - 1.9) / .25)
    def dr(c):
        if b > 0:
            g = cairo.RadialGradient(CX, 1060, 30, CX, 1060, 600); g.add_color_stop_rgba(0, .9, .22, .27, .5 * b); g.add_color_stop_rgba(1, .9, .22, .27, 0)
            c.arc(CX, 1060, 600, 0, 2 * math.pi); c.set_source(g); c.fill()
        tiffin(c, CX, 1060, 1.5 * p, -.05 + .04 * math.sin(T * 11) * b)
        if b > 0:                                           # particles fly out of the box TOWARD the camera
            rng = np.random.default_rng(21); u = t - 1.9
            for k in range(260):
                ang = rng.random() * 2 * math.pi; spd = .5 + rng.random(); d0 = rng.random() * .9
                z = 1.0 / (1 + max(0, (u * spd * .9 + d0 * (u > .4)) % 1.6) * 3.2)       # 1 far -> small = near
                r = (1 / z - 1) * 120
                x = CX + math.cos(ang) * r; y = 1060 + math.sin(ang) * r
                if not (-50 < x < W + 50 and 820 < y < H): continue
                sz = 2 + 5 / z * (.4 + rng.random() * .6)
                c.arc(x, y, min(sz, 34), 0, 2 * math.pi); c.set_source_rgba(*hx(RED if k % 3 else 'FFFFFF', min(1, .35 + .25 / z))); c.fill()
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('3 मिनट में', 0)], 400, t, 124)
    title_line(fr, [('अरबों कण', 3)], 580, t - 1.95, 136)
    timer_txt(fr, CX, 820, 180 - clamp(t / 1.9) * 180, YL, 90)
    note(fr, 'आँख से दिखते नहीं', CX, 1340, t - 2.9, 50, YL, -3)

def sc_p1(fr, T, t, l):
    ebg(fr, 'cream', T)
    title_line(fr, [('2023, ', 1), ('अमेरिका', 0)], 380, t, 120)
    if t > 3.3: title_line(fr, [('बच्चों के ', 0), ('खाने के डिब्बे', 1)], 560, t - 3.3, 100)
    k = ease(clamp((t - .15) / .55)); hl = 1 if t > 3.6 else 0
    if t > 5.5: hl = 2
    put_rgba(fr, mw_card(hl), CX + 700 * (1 - k), 990 + 60 * (1 - k), .82 * lerp(.7, 1, k), 1.0, lerp(18, -3, k) + .8 * math.sin(T * 1.3))
    source_tag(fr, 'Environmental Science & Technology, 2023', 100, 1238, t - 1.2)

def sc_p2(fr, T, t, l):
    ebg(fr, 'black', T)
    _p2body(fr, T, t)
    title_line(fr, [('हर ', 0), ('1 सेंटीमीटर', 1), (' से', 0)], 400, t, 112)
    if t > 2.8: title_line(fr, [('200 करोड़+ कण', 3)], 580, t - 2.8, 124)

def _p2body(fr, T, t):
    S = 420; x0, y0 = CX - S / 2, 820
    if t < .75:                                             # dive into the plastic wall of the box
        z = ease(clamp(t / .75)); s = lerp(1.5, 11, z)
        def dive(c):
            tiffin(c, CX - 60 * s, 1030 - 40 * s, s, 0)
            c.rectangle(CX - S / 2 * (s / 11), 1030 - S / 2 * (s / 11), S * s / 11, S * s / 11); c.set_source_rgba(*hx(YL)); c.set_line_width(6); c.stroke()
            c.rectangle(0, 0, W, H); c.set_source_rgba(.086, .086, .086, clamp((t - .45) / .3)); c.fill()
        overlay(fr, cairo_layer(dive))
        return
    p = ease(clamp((t - .75) / .3))
    def dr(c):
        c.rectangle(x0, y0, S * p, S * p); c.set_source_rgba(*hx('F3F6FA', .14)); c.fill_preserve(); c.set_source_rgba(*hx(YL)); c.set_line_width(6); c.stroke()
        if p >= 1:
            n = int(clamp((t - 1.0) / 2.0) ** 1.6 * 900); rng = np.random.default_rng(11)
            pts = rng.random((900, 3))
            for i in range(n):
                px, py, s_ = pts[i]; jx = 2 * math.sin(T * 7 + i); jy = 2 * math.cos(T * 6 + i * 1.3)
                c.arc(x0 + 8 + px * (S - 16) + jx, y0 + 8 + py * (S - 16) + jy, 2 + s_ * 4, 0, 2 * math.pi)
                c.set_source_rgba(*hx(RED if i % 4 else 'FFFFFF', .9)); c.fill()
            for i in range(11):
                c.move_to(x0 + i * S / 10, y0 - 14 - (10 if i % 5 == 0 else 0)); c.line_to(x0 + i * S / 10, y0 - 4)
                c.move_to(x0 - 14 - (10 if i % 5 == 0 else 0), y0 + i * S / 10); c.line_to(x0 - 4, y0 + i * S / 10)
            c.set_source_rgba(1, 1, 1, .9); c.set_line_width(3); c.stroke()
    overlay(fr, cairo_layer(dr))
    if p >= 1:
        put_rgba(fr, htext('1 cm', 40, 'FFFFFF', HI_B), CX, y0 - 58, 1.0, 1.0, 0)
        put_rgba(fr, htext('1 cm', 40, 'FFFFFF', HI_B), x0 - 80, y0 + S / 2, 1.0, 1.0, 90)
    note(fr, 'बस इतनी सी जगह', 760, 1330, t - 1.4, 48, YL, -4, 720, 1200)

# microscope eyepiece with organic cells
MC = (CX, 1065); MR = 300
def _cellpts():
    rng = np.random.default_rng(14); pts = []
    for _ in range(20000):
        if len(pts) >= 16: break
        a = rng.random() * 2 * math.pi; r = math.sqrt(rng.random()) * (MR - 55)
        p = (MC[0] + r * math.cos(a), MC[1] + r * math.sin(a))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 100 ** 2 for q in pts): pts.append(p)
    return pts
CELLS = _cellpts()
DEAD_ORDER = list(np.random.default_rng(2).permutation(16))
def cell2(c, x, y, r, dead, T, sd):
    r = r * (1 - .25 * dead); n = 28
    for i in range(n + 1):
        a = i / n * 2 * math.pi; rr = r * (1 + .07 * math.sin(3 * a + T * 2.4 + sd) + .04 * math.sin(5 * a - T * 1.7 + sd))
        (c.move_to if i == 0 else c.line_to)(x + rr * math.cos(a), y + rr * math.sin(a))
    c.close_path()
    al = 1 - dead
    g = cairo.RadialGradient(x - r * .3, y - r * .3, 2, x, y, r)
    g.add_color_stop_rgb(0, lerp(.7, 1, al), lerp(.7, .86, al), lerp(.7, .9, al)); g.add_color_stop_rgb(1, lerp(.42, .95, al), lerp(.42, .52, al), lerp(.44, .68, al))
    c.set_source(g); c.fill_preserve()
    if dead > .5: c.set_dash([10, 8])
    c.set_source_rgba(*hx('3A1030' if dead < .5 else '2A2A2A')); c.set_line_width(4); c.stroke(); c.set_dash([])
    c.arc(x + r * .12, y - r * .05, r * .36, 0, 2 * math.pi); c.set_source_rgba(lerp(.3, .62, al), lerp(.3, .2, al), lerp(.32, .5, al), 1); c.fill()

def sc_k1(fr, T, t, l):
    ebg(fr, 'black', T)
    title_line(fr, [('लैब: ', 0), ('किडनी', 1), (' कोशिकाएँ', 0)], 400, t, 108)
    if t > 5.6: title_line(fr, [('75% मर गईं', 3)], 580, t - 5.6, 132)
    dead_n = int(clamp((t - 5.7) / .9) * 12)
    open_ = ease(clamp(t / .45))
    def dr(c):
        R = MR * open_
        if R < 2: return
        c.save(); c.arc(*MC, R, 0, 2 * math.pi); c.clip()
        g = cairo.RadialGradient(MC[0], MC[1], 20, MC[0], MC[1], MR); g.add_color_stop_rgb(0, 1, .96, .9); g.add_color_stop_rgb(1, .93, .8, .78)
        c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
        for i, (x, y) in enumerate(CELLS):
            dead = 1.0 if DEAD_ORDER.index(i) < dead_n else 0.0
            cell2(c, x + 5 * math.sin(T * .9 + i), y + 5 * math.cos(T * .8 + i), 42, dead, T, i)
        if 1.0 < t < 6.2:                                     # plastic particles drifting in, sticking to cells
            rng = np.random.default_rng(5)
            for j in range(120):
                x0, y0 = CELLS[j % 16]; a = rng.random() * 2 * math.pi
                ph = clamp((t - 1.0 - rng.random() * 2.5) / 1.6)
                d = lerp(320, 30 + rng.random() * 20, ease(ph))
                c.arc(x0 + d * math.cos(a), y0 + d * math.sin(a), 3 + 3 * rng.random(), 0, 2 * math.pi)
                c.set_source_rgba(*hx('F2B705', .9 * (ph > 0))); c.fill()
        vg = cairo.RadialGradient(MC[0], MC[1], MR * .6, MC[0], MC[1], MR)
        vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0, .55); c.rectangle(0, 0, W, H); c.set_source(vg); c.fill()
        c.restore()
        c.arc(*MC, R + 10, 0, 2 * math.pi); c.set_source_rgba(.75, .75, .8, 1); c.set_line_width(20); c.stroke()
        c.arc(*MC, R + 22, 0, 2 * math.pi); c.set_source_rgba(.2, .2, .24, 1); c.set_line_width(8); c.stroke()
    overlay(fr, cairo_layer(dr))
    note(fr, 'सबसे ज़्यादा मात्रा पर', 215, 1365, t - 3.0, 36, YL, -5)
    note(fr, '2 दिन में', 885, 1365, t - 4.7, 44, YL, 5)

def sc_w1(fr, T, t, l):
    ebg(fr, 'cream', T)
    title_line(fr, [('खाना गर्म करो', 0)], 380, t, 112)
    title_line(fr, [('काँच', 1), (' या ', 0), ('स्टील', 1), (' में', 0)], 560, t - .7, 116)
    k1 = ease(clamp((t - .6) / .4)); k2 = ease(clamp((t - 1.3) / .4))
    def dr(c):
        if k1 > 0: bowl(c, lerp(-200, 300, k1), 1080, 1.05, 'glass', T)
        if k2 > 0: bowl(c, lerp(W + 200, 780, k2), 1080, 1.05, 'steel', T)
        tick_ring(c, 300, 1250, 46, back(clamp((t - 1.0) / .3)), True)
        tick_ring(c, 780, 1250, 46, back(clamp((t - 1.7) / .3)), True)
    overlay(fr, cairo_layer(dr))

SCENES = dict(h1=sc_h1, h2=sc_h2, p1=sc_p1, p2=sc_p2, a1=sc_a1, k1=sc_k1, w1=sc_w1, w2=sc_w2, e1=sc_e1)

# ---------------- camera + transitions (applied to the scene layer, before subtitles and logo)
SHAKES = [(2.92, 10), (4.85, 30), (17.3, 26), (21.25, 22), (28.1, 30)]
FOCUS = dict(h2=1060, p1=990, p2=1030, a1=1080, k1=1065, w1=1080, w2=1080)
def camera(fr, l, t, T):
    z = 1.0; dx = dy = 0.0; ch = 0
    if l['id'] in FOCUS: z += .05 * ease(clamp(t / l['dur']))
    for ts, amp in SHAKES:
        d = T - ts
        if 0 <= d < .45:
            e = (1 - d / .45) ** 2; dx += amp * e * math.sin(d * 95); dy += amp * e * math.cos(d * 71); z += .0025 * amp * e
            if d < .16 and amp >= 20: ch = int(9 * (1 - d / .16))
    if z != 1.0 or dx or dy:
        fy = FOCUS.get(l['id'], 1000)
        M = np.float32([[z, 0, (1 - z) * CX + dx], [0, z, (1 - z) * fy + dy]])
        fr[:] = cv2.warpAffine(fr, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    if ch:
        fr[..., 0] = np.roll(fr[..., 0], ch, 1); fr[..., 2] = np.roll(fr[..., 2], -ch, 1)

TR = .15
def transition(fr, T):
    for i, x in enumerate(TL[1:]):
        u = T - x['start']
        if -TR < u < TR:
            p = 1 - abs(u) / TR; p2 = p * p
            if x['id'] == 'e1':
                fr[:] = (fr * (1 - .7 * p2) + 255 * .7 * p2).astype(np.uint8); return
            if i % 2 == 0:                                   # whip pan
                dirn = 1 if i % 4 == 0 else -1
                off = int(dirn * p2 * 560 * (1 if u < 0 else -1))
                fr[:] = np.roll(fr, off, 1); k = int(8 + 110 * p2); fr[:] = cv2.blur(fr, (k, 1))
            else:                                            # zoom punch-through
                z = 1 + (.32 if u < 0 else .22) * p2
                M = np.float32([[z, 0, (1 - z) * CX], [0, z, (1 - z) * 1000]])
                fr[:] = cv2.warpAffine(fr, M, (W, H), borderMode=cv2.BORDER_REFLECT)
                s = 1 + 9 * p2; fr[:] = cv2.GaussianBlur(fr, (0, 0), s)
            return

def frame(T):
    fr = np.zeros((H, W, 3), np.uint8)
    l = TL[0]
    for x in TL:
        if x['start'] <= T: l = x
    t = T - l['start']
    SCENES[l['id']](fr, T, t, l)
    camera(fr, l, t, T)
    if V != 'thumb': transition(fr, T)
    if V != 'thumb': subtitle(fr, T)
    overlay(fr, LOGO)
    put_rgba(fr, logo_word(), 318, 316, 1.0, 1.0, -2)
    return fr
