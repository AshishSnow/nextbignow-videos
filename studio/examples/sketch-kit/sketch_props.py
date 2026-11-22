# shared sketch-look helpers (bars2 from mcd, headline from ikea)
def bars2(c, t, kA, kB, labA, labB, valA, valB, hA, hB, colA=(255, 120, 60), colB=(40, 190, 110), cmp_k=0, cmp_txt=''):
    base = 1180
    def col(x, val, h, rgb, lab, k):
        if k <= 0: return
        hh = h * eo(k)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, base - hh, 300, hh), 18, 18)
        c.drawRRect(r.makeOffset(10, 12), P(INK, 0.25, 6)); inked(c, r, LG((x, base - hh), (x, base), [tuple(min(255, v + 60) for v in rgb), rgb]), 7)
        neon_text(c, val, x + 150, base - hh - 30, 70, rgb, cl(k * 2))
        neon_text(c, lab, x + 150, base + 70, 38, (255, 255, 255))
    inked(c, skia.Rect.MakeXYWH(60, base, 960, 14), P((255, 255, 255)), 5)
    col(140, valA, hA, colA, labA, kA); col(640, valB, hB, colB, labB, kB)
    if cmp_k > 0:
        pop(c, cmp_k, 540, 1610, lambda: (board(c, 250, 1550, 580, 110, (255, 236, 90)), neon_text(c, cmp_txt, 540, 1628, 64, (255, 70, 90))))



def headline(c, t, lines, tag, sub):
    c.save(); c.translate(540, 235); c.rotate(-2); c.drawRect(skia.Rect.MakeXYWH(-190, -42, 380, 76), P((212, 160, 46))); f = serif(44, 400, True); tw = f.measureText(tag); c.drawString(tag, -tw / 2, 14, f, P((34, 32, 30))); c.restore()
    for i, (txt, it, col, sz) in enumerate(lines):
        f = serif(sz, 700 if not it else 500, it); tw = f.measureText(txt)
        while tw > 940: f = serif(f.getSize() * 0.95, 700 if not it else 500, it); tw = f.measureText(txt)
        c.drawString(txt, 540 - tw / 2, 385 + i * 112, f, P(col, pr(t, i * 0.25, 0.3)))
    f = serif(40, 400); c.drawString(sub, 540 - f.measureText(sub) / 2, 385 + len(lines) * 112 - 40, f, P((90, 86, 80), pr(t, 0.8, 0.3)))


