


# ======================= second half of the story =======================
def wat(word, after=0.0):
    for w in WORDS:
        if w[1] >= after - 0.01 and w[0].lower().strip(".,?'") == word: return w[1]
    return 1e9


def goat(c, x, y, s, t, a=1.0, cc=(45, 25, 30)):
    ph = math.sin(t * 6 + x * 0.01)
    c.save(); c.translate(x, y); c.scale(s, s); p = P(cc, a)
    c.drawOval(skia.Rect.MakeXYWH(-26, -40, 52, 24), p)
    c.drawOval(skia.Rect.MakeXYWH(18, -54, 18, 14), p)
    st = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, StrokeCap=skia.Paint.kRound_Cap); st.setColor(col(cc, a))
    c.drawLine(28, -54, 22, -66, st); c.drawLine(-24, -32, -30, -40, st)
    for lx, sgn in ((-16, 1), (-8, -1), (10, 1), (18, -1)):
        c.drawLine(lx, -18, lx + 4 * ph * sgn, 0, st)
    c.restore()


def girl(c, x, y, s, t, walking, a=1.0, cc=(45, 25, 30)):
    ph = math.sin(t * 6) * walking
    c.save(); c.translate(x, y); c.scale(s, s); p = P(cc, a)
    st = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap); st.setColor(col(cc, a))
    c.drawCircle(0, -70, 9, p)
    d = skia.Path(); d.moveTo(-4, -60); d.lineTo(4, -60); d.lineTo(14, -22); d.lineTo(-14, -22); d.close(); c.drawPath(d, p)
    c.drawLine(-5, -22, -5 + 8 * ph, 0, st); c.drawLine(5, -22, 5 - 8 * ph, 0, st)
    c.drawLine(4, -54, 26, -78 + 10 * (1 - walking), st)  # stick / pointing arm
    c.restore()


def plane_top(c, x, y, s, rot, a):
    """top-down plane SHADOW passing over the sand."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = P((60, 30, 20), a); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
    b = skia.Path(); b.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-14, -110, 28, 220), 14, 14)); c.drawPath(b, p)
    w = skia.Path(); w.moveTo(0, -20); w.lineTo(150, 30); w.lineTo(150, 50); w.lineTo(0, 20); w.lineTo(-150, 50); w.lineTo(-150, 30); w.close(); c.drawPath(w, p)
    tl = skia.Path(); tl.moveTo(0, 80); tl.lineTo(50, 110); tl.lineTo(50, 120); tl.lineTo(0, 105); tl.lineTo(-50, 120); tl.lineTo(-50, 110); tl.close(); c.drawPath(tl, p)
    c.restore()


def big_center(c, small, bigt, k, y, cc=(255, 236, 200), size=190):
    if k <= 0: return
    a = ss(0, 1, k); dy = 24 * (1 - a)
    f = F(os.path.join(FX, 'Cormorant-Bold.ttf'), size)
    if small:
        x = W / 2 - SMALL.measureText(small) / 2; c.drawString(small, x, y - size * 0.95 + dy, SMALL, P(cc, a * 0.9))
    x = W / 2 - f.measureText(bigt) / 2
    sh = P((0, 0, 0), 0.35 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
    c.drawString(bigt, x, y + 8 + dy, f, sh); c.drawString(bigt, x, y + dy, f, P(cc, a))


def frame2(c, t):
    L = T
    s5, s6, s7, s8, s9, s10 = (L[5][0] - 0.3, L[8][0] - 0.3, L[10][0] - 0.3, L[11][0] - 0.3, L[13][0] - 0.3, L[14][0] - 0.25)
    fin = ss(s5, s5 + 0.35, t)          # every cut fades in from the previous shot's colour, never pops
    # ---------- shot 5: noon shrine, then inside with the bats ----------
    if t < s6:
        u = t - s5; inside = ss(L[6][0] - 0.35, L[6][0] + 0.15, t)
        vgrad(c, None, None, 0, 1400, [0, .6, 1], [col((250, 225, 180)), col((250, 200, 140)), col((240, 170, 110))])
        glow(c, 540, 300, 520, (255, 250, 220), 0.7); c.drawCircle(540, 300, 90, P((255, 252, 235)))
        fill_dune(c, dune(9, 1150, 110, u * 12), (240, 175, 110), (215, 140, 90), haze=(255, 230, 190), haze_a=0.35)
        nd = dune(10, 1400, 150, u * 30 + 400)
        sx = 520; sy = min(nd, key=lambda q: abs(q[0] - sx))[1] + 40
        sh = skia.Path(); sh.moveTo(sx + 112, sy); sh.lineTo(sx + 112, sy - 150); sh.lineTo(sx + 420, sy + 10); sh.lineTo(sx + 300, sy + 30); sh.close()
        fill_dune(c, nd, (225, 145, 85), (150, 70, 45), rim=(255, 240, 200), rim_a=0.8)
        c.drawPath(sh, P((120, 50, 40), 0.35))
        shrine(c, sx, sy, 1.6, 0.0)
        walker(c, sx + 150, sy + 4, 1.0, 0, a=1.0)          # resting in the shade (still)
        for i in range(6):
            y = 1000 + i * 26; a = 0.05 + 0.03 * math.sin(u * 3 + i)
            c.drawLine(0, y + 5 * math.sin(u * 4 + i), W, y, skia.Paint(AntiAlias=True, StrokeWidth=3, Color=col((255, 240, 200), a)))
        big_center(c, 'DAY 3', 'Shade.', ss(L[5][0] + 0.6, L[5][0] + 1.2, t) * (1 - inside), 700, cc=(110, 40, 30))
        if inside > 0:   # inside the dome: dark, a shaft of light, bats hanging
            c.save(); c.drawRect(skia.Rect.MakeWH(W, H), P((28, 18, 22), inside))
            shaft = skia.Path(); shaft.moveTo(380, 1700); shaft.lineTo(700, 1700); shaft.lineTo(620, 1100); shaft.lineTo(460, 1100); shaft.close()
            sp = skia.Paint(AntiAlias=True)
            sp.setShader(skia.GradientShader.MakeLinear([(0, 1100), (0, 1700)], [col((255, 200, 120), 0.0), col((255, 200, 120), 0.45 * inside)]))
            c.drawPath(shaft, sp)
            arc = skia.Path(); arc.moveTo(60, 900); arc.cubicTo(60, 200, 1020, 200, 1020, 900)
            ap = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=10); ap.setColor(col((80, 55, 50), inside)); c.drawPath(arc, ap)
            rnd = random.Random(12)
            for i in range(14):
                bx = 180 + i * 52 + rnd.uniform(-10, 10); by = 420 + abs(bx - 540) * 0.55 + rnd.uniform(-8, 8)
                sw = 3 * math.sin(t * 2 + i)
                c.save(); c.translate(bx, by); c.rotate(sw)
                c.drawLine(0, -18, 0, 0, skia.Paint(AntiAlias=True, StrokeWidth=2, Color=col((60, 40, 40), inside)))
                body = skia.Path(); body.moveTo(0, 0); body.cubicTo(-14, 6, -12, 44, 0, 50); body.cubicTo(12, 44, 14, 6, 0, 0)
                c.drawPath(body, P((15, 10, 14), inside)); c.drawCircle(-4, 42, 1.6, P((255, 200, 120), inside)); c.drawCircle(4, 42, 1.6, P((255, 200, 120), inside))
                c.restore()
            glow(c, 540, 1400, 500, (255, 170, 80), 0.25 * inside)
            c.restore()
            line_i(c, 'Bats live in the roof.', ss(L[6][0], L[6][0] + 0.5, t) * (1 - ss(L[7][0] - 0.3, L[7][0], t)), 1100, cc=(255, 220, 170))
            big_center(c, 'SO HE EATS THEM', 'Raw.', ss(wat('raw', L[7][0]) - 0.15, wat('raw', L[7][0]) + 0.3, t), 1150, cc=(255, 214, 120), size=220)
        out_k = ss(s6 - 0.3, s6, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((235, 190, 135), out_k))
        if fin < 1: c.drawRect(skia.Rect.MakeWH(W, H), P((255, 236, 200), 1 - fin))
        return
    # ---------- shot 6: SOS in the sand from above, plane shadows miss him ----------
    if t < s7:
        u = t - s6
        z = 1.0 + 0.04 * u
        c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        vgrad(c, None, None, 0, H, [0, 1], [col((238, 186, 128)), col((214, 150, 95))])
        for i in range(40):   # wind ripples
            y = i * 52 + 10 * math.sin(i)
            path = skia.Path(); path.moveTo(-50, y)
            for xx in range(0, W + 100, 60): path.lineTo(xx, y + 10 * math.sin(xx * 0.012 + i * 0.7))
            rp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3); rp.setColor(col((190, 120, 70), 0.35)); c.drawPath(path, rp)
        sos_k = ss(L[8][0] + 0.2, L[8][1] + 0.2, t)
        fs = F(os.path.join(FX, 'Anton.ttf'), 420); tw = fs.measureText('SOS'); x0 = W / 2 - tw / 2
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x0 - 20, 0, (tw + 40) * sos_k, H))
        dp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=26, StrokeJoin=skia.Paint.kRound_Join); dp.setColor(col((150, 80, 45)))
        c.drawString('SOS', x0, 1050, fs, dp)
        hp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=8); hp.setColor(col((255, 225, 170), 0.8))
        c.drawString('SOS', x0 - 6, 1044, fs, hp)
        c.restore()
        walker(c, W / 2 + 330, 1150, 0.9, 0)
        tp = wat('planes', L[9][0])
        for j in range(2):
            k = cl((t - tp - j * 0.9) / 1.6)
            if 0 < k < 1: plane_top(c, lerp_ := (-300 + 1700 * k), 300 + 1200 * k + j * 200, 1.4 - j * 0.3, 145, 0.5 * math.sin(math.pi * k))
        c.restore()
        line_i(c, '...and miss him.', ss(wat('miss', L[9][0]) - 0.1, wat('miss', L[9][0]) + 0.4, t), 560, cc=(90, 35, 25))
        out_k = ss(s7 - 0.3, s7, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((250, 190, 170), out_k))
        return
    # ---------- shot 7: dawn, a girl with goats spots him ----------
    if t < s8:
        u = t - s7
        vgrad(c, None, None, 0, 1400, [0, .5, 1], [col((90, 90, 160)), col((240, 150, 150)), col((255, 205, 160))])
        glow(c, 760, 1060, 600, (255, 210, 160), 0.6); c.drawCircle(760, 1060, 110, P((255, 230, 190)))
        fill_dune(c, dune(11, 1150, 120, u * 10), (220, 140, 130), (180, 100, 100), haze=(255, 200, 180), haze_a=0.3)
        nd = dune(12, 1380, 170, u * 25 + 600)
        fill_dune(c, nd, (170, 85, 80), (70, 35, 45), rim=(255, 210, 180), rim_a=0.9)
        def gy(x): return min(nd, key=lambda q: abs(q[0] - x))[1] + 3
        spot = ss(wat('spots', L[10][0]) - 0.2, wat('spots', L[10][0]) + 0.3, t)
        for i in range(5):
            gx = 120 + i * 85 + 40 * u * (1 - spot * 0.7); goat(c, gx, gy(gx), 1.0 + 0.1 * (i % 2), t)
        gx = 560 + 40 * u * (1 - spot); girl(c, gx, gy(gx), 1.15, t, 1 - spot)
        rx = 930; c.save(); c.translate(rx, gy(rx)); c.rotate(-80)  # him, lying exhausted on the far crest
        walker(c, 0, 0, 0.9, 0); c.restore()
        if spot > 0: glow(c, rx - 10, gy(rx) - 30, 120, (255, 230, 170), 0.5 * spot)
        big_center(c, 'DAY 9', 'Found.', ss(wat('spots', L[10][0]), wat('spots', L[10][0]) + 0.5, t), 700, cc=(255, 240, 220))
        out_k = ss(s8 - 0.3, s8, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((236, 214, 175), out_k))
        return
    # ---------- shot 8: painted map, 180 miles into Algeria, -33 lb ----------
    if t < s9:
        u = t - s8
        vgrad(c, None, None, 0, H, [0, 1], [col((240, 222, 186)), col((225, 200, 160))])
        mor = skia.Path(); mor.moveTo(-50, 300); mor.lineTo(520, 380); mor.lineTo(600, 760); mor.lineTo(480, 1350); mor.lineTo(-50, 1500); mor.close()
        alg = skia.Path(); alg.moveTo(520, 380); alg.lineTo(1150, 300); alg.lineTo(1150, 1600); alg.lineTo(480, 1350); alg.lineTo(600, 760); alg.close()
        c.drawPath(mor, P((228, 170, 120))); c.drawPath(alg, P((214, 150, 105)))
        bp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5); bp.setColor(col((120, 70, 50), 0.7)); bp.setPathEffect(skia.DashPathEffect.Make([18, 12], 0))
        b = skia.Path(); b.moveTo(520, 380); b.lineTo(600, 760); b.lineTo(480, 1350); c.drawPath(b, bp)
        lf = F(FD + 'Inter-Bold.otf', 34)
        c.drawString('MOROCCO', 120, 980, lf, P((120, 60, 40), 0.8)); c.drawString('ALGERIA', 760, 1180, lf, P((110, 55, 40), 0.8))
        pts = [(260, 880), (360, 820), (430, 900), (560, 880), (650, 960), (720, 900), (820, 1000)]
        k = ss(L[11][0], L[11][1] - 0.2, t); n = 1 + k * (len(pts) - 1)
        rp = skia.Path(); rp.moveTo(*pts[0])
        for i in range(1, int(n) + 1): rp.lineTo(*pts[i])
        if n % 1 > 0 and int(n) + 1 < len(pts):
            a_, b_ = pts[int(n)], pts[int(n) + 1]; f_ = n % 1; rp.lineTo(a_[0] + (b_[0] - a_[0]) * f_, a_[1] + (b_[1] - a_[1]) * f_)
        rr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, StrokeCap=skia.Paint.kRound_Cap); rr.setColor(col(CRED_ if False else (200, 40, 50)))
        rr.setPathEffect(skia.DashPathEffect.Make([4, 18], 0)); c.drawPath(rp, rr)
        c.drawCircle(*pts[0], 14, P((40, 30, 30)))
        c.drawString('RACE', pts[0][0] - 40, pts[0][1] + 50, SMALL, P((60, 30, 25)))
        big_center(c, 'HE WANDERED', '180 Miles', ss(wat('hundred', L[11][0]) - 0.1, wat('hundred', L[11][0]) + 0.4, t) * (1 - ss(L[12][0] - 0.3, L[12][0], t)), 620, cc=(110, 40, 30))
        big_center(c, 'HE LOST', '33 lbs', ss(L[12][0], L[12][0] + 0.4, t), 620, cc=(170, 35, 40))
        out_k = ss(s9 - 0.3, s9, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((255, 225, 170), out_k))
        return
    # ---------- shot 9: he ran that race again ----------
    if t < s10:
        u = t - s9
        vgrad(c, None, None, 0, 1400, [0, .65, 1], [col((110, 170, 230)), col((240, 210, 170)), col((255, 220, 170))])
        glow(c, 820, 420, 300, (255, 250, 220), 0.6); c.drawCircle(820, 420, 70, P((255, 250, 230)))
        fill_dune(c, dune(13, 1150, 120, u * 20), (240, 180, 120), (215, 150, 100), haze=(255, 230, 190), haze_a=0.3)
        nd = dune(14, 1370, 160, u * 60 + 900)
        fill_dune(c, nd, (225, 140, 80), (140, 60, 40), rim=(255, 240, 200), rim_a=0.9)
        for i in range(7):
            x = (100 + i * 150 + u * 70) % 1180 - 50
            walker(c, x, min(nd, key=lambda q: abs(q[0] - x))[1] + 2, 1.0, t + i * 0.37, a=1.0 if i == 3 else 0.75)
        big_center(c, 'HE RAN IT AGAIN', '6 More Times', ss(wat('six', L[13][0]) - 0.15, wat('six', L[13][0]) + 0.4, t), 700, cc=(110, 40, 30), size=170)
        out_k = ss(s10 - 0.3, s10, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((60, 30, 50), out_k))
        return
    # ---------- shot 10: the question ----------
    u = t - s10
    vgrad(c, None, None, 0, 1400, [0, .5, .85, 1], [col((30, 24, 60)), col((130, 55, 75)), col((235, 120, 70)), col((255, 180, 110))])
    stars(c, 0.5)
    glow(c, 540, 1080, 460, (255, 170, 100), 0.5); c.drawCircle(540, 1080, 95, P((255, 205, 150)))
    fill_dune(c, dune(15, 1200, 130, u * 15), (180, 85, 70), (120, 50, 55), haze=(240, 140, 110), haze_a=0.3)
    nd = dune(16, 1390, 180, u * 30 + 100)
    fill_dune(c, nd, (110, 45, 40), (40, 18, 25), rim=(255, 170, 110), rim_a=0.9)
    wx = 540 + 10 * u; walker(c, wx, min(nd, key=lambda q: abs(q[0] - wx))[1] + 2, 1.1, t)
    big_center(c, 'SO...', 'Would you', ss(s10 + 0.3, s10 + 0.8, t), 560, cc=(255, 236, 200), size=170)
    big_center(c, None, 'have survived?', ss(s10 + 0.6, s10 + 1.1, t), 730, cc=(255, 214, 120), size=150)
    cta = 'SUBSCRIBE FOR MORE TRUE STORIES' if PLAT == 'yt' else "SEND THIS TO SOMEONE WHO'D MAKE IT"
    k = ss(T[-1][1] - 0.2, T[-1][1] + 0.4, t)
    if k > 0:
        cf = F(FD + 'Inter-Bold.otf', 32); c.drawString(cta, W / 2 - cf.measureText(cta) / 2, 840, cf, P((255, 255, 255), k))
    fade = ss(DUR - 0.6, DUR, t)
    if fade > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), fade))
