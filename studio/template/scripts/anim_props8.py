# ================= props kit 8 (exec'd after anim_props7.py) — HOW IT WORKS EP 1 + EP 2 (R&D writers' room, 4 Nov 2026) =================
# Clean, flat, logo-free: one idea per frame. pot_el = coin pot with a fill level; gate_el = barrier gate with a counter; plays_grid = dots where YOUR plays
# stay the same while everybody's grow (share shrinks on screen); mic_el = stand mic; booth_el = plain middleman counter; score_pie = five-slice pie that fills
# slice by slice; gauge_el = score gauge; car_el = flat side-view car; cycle_el = card-bill month strip (spend → reported → you pay); report_el = credit report sheet.
_PIE_COLS = [(90, 170, 255), (180, 120, 250), (60, 210, 170), (255, 120, 90), (255, 200, 50)]


def pot_el(w=620, fill=0.6, label=None, col=(44, 48, 66)):
    fl = round(float(clamp(fill)), 2)
    def mk():
        h = int(w * 0.86); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.ellipse(S(w * 0.02, h * 0.34, w * 0.14, h * 0.50), outline=o, width=9 * sc); d.ellipse(S(w * 0.86, h * 0.34, w * 0.98, h * 0.50), outline=o, width=9 * sc)
        d.rounded_rectangle(S(w * 0.08, h * 0.16, w * 0.92, h * 0.98), 60 * sc, fill=tuple(col) + (255,), outline=o, width=7 * sc)
        top = h * (0.92 - 0.66 * fl)
        if fl > 0.01:
            d.rounded_rectangle(S(w * 0.13, top, w * 0.87, h * 0.93), 44 * sc, fill=(255, 205, 50, 255))
            r = np.random.default_rng(8)
            for _ in range(int(14 + 40 * fl)):
                x = r.uniform(w * 0.17, w * 0.83); y = r.uniform(top + 20, h * 0.88); rr = w * 0.032
                d.ellipse(S(x - rr, y - rr, x + rr, y + rr), fill=(255, 226, 110, 255), outline=(190, 130, 20, 255), width=2 * sc)
        d.rounded_rectangle(S(w * 0.02, h * 0.10, w * 0.98, h * 0.22), 24 * sc, fill=(72, 78, 104, 255), outline=o, width=7 * sc)
        if label:
            fn = font(F_ANTON, int(w * 0.13 * sc)); d.text(S(w / 2, h * 0.62), label, font=fn, fill=(26, 22, 34, 255) if fl > 0.5 else (255, 255, 255, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("pot8", w, fl, label, tuple(col)), mk)


def gate_el(w=760, count="999", open_=False, need="1,000"):
    """two posts, a barrier arm (red + down when closed, green + up when open), and a big counter above it"""
    def mk():
        h = int(w * 0.95); im, d, S = _im4(w, h); o = _O4; sc = 2
        for x in (w * 0.05, w * 0.85):
            d.rounded_rectangle(S(x, h * 0.30, x + w * 0.10, h * 0.98), 14 * sc, fill=(232, 236, 246, 255), outline=o, width=6 * sc)
        d.rounded_rectangle(S(w * 0.18, h * 0.02, w * 0.82, h * 0.26), 22 * sc, fill=(26, 28, 40, 255), outline=o, width=6 * sc)
        d.text(S(w / 2, h * 0.14), str(count), font=font(F_ANTON, int(w * 0.16 * sc)), fill=(90, 240, 150, 255) if open_ else (255, 90, 80, 255), anchor="mm")
        col = (50, 200, 110, 255) if open_ else (235, 60, 56, 255); y = h * 0.42 if open_ else h * 0.62
        d.rounded_rectangle(S(w * 0.12, y, w * 0.88, y + h * 0.075), 16 * sc, fill=col, outline=o, width=6 * sc)
        d.text(S(w / 2, y + h * 0.0375), f"NEED {need}", font=font(F_ANTON, int(w * 0.046 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("gate8", w, str(count), open_, need), mk)


def plays_grid(f, cx, cy, total, mine=5, w=760, k=1.0, col=(226, 232, 246), mine_col=(255, 140, 40)):
    """a grid of dots: mine orange, everybody else pale. Double `total` and the orange share shrinks on screen."""
    n = int(round(total * clamp(k))); cols = int(math.ceil(math.sqrt(total * 1.6))); gap = w / cols; r = int(gap * 0.36)
    rows = int(math.ceil(total / cols)); x0 = cx - w / 2 + gap / 2; y0 = cy - rows * gap / 2 + gap / 2
    for i in range(n):
        x = int(x0 + (i % cols) * gap); y = int(y0 + (i // cols) * gap)
        cv2.circle(f, (x, y), r, C(mine_col if i < mine else col), -1, cv2.LINE_AA); cv2.circle(f, (x, y), r, C((20, 20, 26)), max(2, r // 7), cv2.LINE_AA)


def mic_el(w=170, col=(70, 76, 96)):
    def mk():
        h = int(w * 3.6); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rounded_rectangle(S(w * 0.46, h * 0.20, w * 0.54, h * 0.94), 6 * sc, fill=tuple(col) + (255,), outline=o, width=3 * sc)
        d.rounded_rectangle(S(w * 0.14, h * 0.92, w * 0.86, h * 0.985), 10 * sc, fill=tuple(col) + (255,), outline=o, width=5 * sc)
        d.rounded_rectangle(S(w * 0.26, h * 0.01, w * 0.74, h * 0.20), 40 * sc, fill=(226, 230, 240, 255), outline=o, width=6 * sc)
        for yy in (0.06, 0.10, 0.14): d.line(S(w * 0.30, h * yy, w * 0.70, h * yy), fill=(120, 126, 150, 255), width=3 * sc)
        return _el4(im, w, h)
    return gcache(("mic8", w, col), mk)


def booth_el(w=620, text="DISTRIBUTOR", col=(255, 196, 60)):
    def mk():
        h = int(w * 0.92); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rectangle(S(w * 0.08, h * 0.26, w * 0.92, h * 0.98), fill=(238, 240, 248, 255), outline=o, width=6 * sc)
        d.rectangle(S(w * 0.18, h * 0.36, w * 0.82, h * 0.66), fill=(40, 46, 70, 255), outline=o, width=5 * sc)
        d.rectangle(S(w * 0.04, h * 0.66, w * 0.96, h * 0.73), fill=tuple(col) + (255,), outline=o, width=5 * sc)
        d.rounded_rectangle(S(w * 0.03, h * 0.04, w * 0.97, h * 0.26), 14 * sc, fill=tuple(col) + (255,), outline=o, width=6 * sc)
        fs = int(min(w * 0.13, w * 1.5 / max(len(text), 1)) * sc)
        d.text(S(w / 2, h * 0.15), text, font=font(F_ANTON, fs), fill=(26, 22, 34, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("booth8", w, text, col), mk)


def score_pie(f, cx, cy, r, vals=(10, 10, 15, 35, 30), k=(1, 1, 1, 1, 1), hl=None, labels=None, cols=None):
    """the pie fills slice by slice: k[i] = 0..1 per slice; hl = slice index that pops out + brightens; dark empty base so the unfilled rest reads as 'still missing'"""
    cols = cols or _PIE_COLS; total = float(sum(vals)); a0 = -90.0
    cv2.circle(f, (cx + 8, cy + 12), r, (0, 0, 0), -1, cv2.LINE_AA); cv2.circle(f, (cx, cy), r, C((34, 36, 54)), -1, cv2.LINE_AA)
    for i, v in enumerate(vals):
        sweep = 360.0 * v / total; kk = clamp(k[i]) if i < len(k) else 0.0
        if kk > 0.005:
            mid = math.radians(a0 + sweep / 2); off = int(r * 0.09) if hl == i else 0
            c0 = (int(cx + off * math.cos(mid)), int(cy + off * math.sin(mid)))
            cv2.ellipse(f, c0, (r, r), 0, a0, a0 + sweep * kk, C(cols[i % len(cols)]), -1, cv2.LINE_AA)
            cv2.ellipse(f, c0, (r, r), 0, a0, a0 + sweep * kk, C((20, 20, 26)), 7, cv2.LINE_AA)
            for ang in (a0, a0 + sweep * kk):
                e = (int(c0[0] + r * math.cos(math.radians(ang))), int(c0[1] + r * math.sin(math.radians(ang)))); cv2.line(f, c0, e, C((20, 20, 26)), 7, cv2.LINE_AA)
            if kk >= 0.99:
                txt = (labels[i] if labels else f"{v}%"); lr = r * (0.62 if v >= 15 else 0.70)
                comp(f, ed_el("", txt, "", big_col=(20, 20, 26), big_size=int(r * 0.17), maxw=int(r * 0.7)), int(c0[0] + lr * math.cos(mid)), int(c0[1] + lr * math.sin(mid)))
        a0 += sweep
    cv2.circle(f, (cx, cy), r, C((20, 20, 26)), 9, cv2.LINE_AA)


def gauge_el(w=620, frac=0.5, lo="300", hi="850"):
    fr = round(float(clamp(frac)), 2)
    def mk():
        h = int(w * 0.66); im, d, S = _im4(w, h); o = _O4; sc = 2; cx, cy, R_ = w / 2, h * 0.84, w * 0.46
        segs = [(226, 60, 56), (246, 150, 50), (250, 210, 60), (120, 210, 90), (40, 180, 110)]
        for i, c_ in enumerate(segs):
            d.arc(S(cx - R_, cy - R_, cx + R_, cy + R_), 180 + i * 36, 180 + (i + 1) * 36, fill=c_ + (255,), width=int(w * 0.11 * sc))
        ang = math.radians(180 + 180 * fr)
        d.line(S(cx, cy, cx + (R_ - w * 0.14) * math.cos(ang), cy + (R_ - w * 0.14) * math.sin(ang)), fill=(255, 255, 255, 255), width=12 * sc)
        d.ellipse(S(cx - 24, cy - 24, cx + 24, cy + 24), fill=(255, 255, 255, 255), outline=o, width=5 * sc)
        fn = font(F_ANTON, int(w * 0.07 * sc)); d.text(S(w * 0.10, h * 0.94), lo, font=fn, fill=(255, 255, 255, 255), anchor="mm"); d.text(S(w * 0.90, h * 0.94), hi, font=fn, fill=(255, 255, 255, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("gauge8", w, fr, lo, hi), mk)


def car_el(w=680, col=(70, 150, 240), tag=None):
    def mk():
        h = int(w * 0.46); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.polygon(S(w * 0.22, h * 0.48, w * 0.32, h * 0.10, w * 0.68, h * 0.10, w * 0.82, h * 0.48), fill=tuple(col) + (255,), outline=o, width=6 * sc)
        d.polygon(S(w * 0.28, h * 0.46, w * 0.35, h * 0.17, w * 0.49, h * 0.17, w * 0.49, h * 0.46), fill=(190, 226, 250, 255), outline=o, width=4 * sc)
        d.polygon(S(w * 0.52, h * 0.46, w * 0.52, h * 0.17, w * 0.66, h * 0.17, w * 0.75, h * 0.46), fill=(190, 226, 250, 255), outline=o, width=4 * sc)
        d.rounded_rectangle(S(w * 0.03, h * 0.46, w * 0.97, h * 0.82), 36 * sc, fill=tuple(col) + (255,), outline=o, width=6 * sc)
        for x in (w * 0.24, w * 0.76):
            d.ellipse(S(x - w * 0.09, h * 0.62, x + w * 0.09, h * 0.62 + w * 0.18), fill=(26, 28, 40, 255), outline=o, width=5 * sc)
            d.ellipse(S(x - w * 0.04, h * 0.62 + w * 0.05, x + w * 0.04, h * 0.62 + w * 0.13), fill=(216, 220, 232, 255))
        if tag: d.text(S(w / 2, h * 0.64), tag, font=font(F_ANTON, int(w * 0.07 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("car8", w, col, tag), mk)


def cycle_el(w=880, k=3):
    """one billing month as a strip with 3 markers revealed in order: 1 YOU SPEND, 2 BALANCE REPORTED, 3 YOU PAY IN FULL"""
    kk = int(k)
    def mk():
        h = int(w * 0.46); im, d, S = _im4(w, h); o = _O4; sc = 2; y = h * 0.42
        d.rounded_rectangle(S(w * 0.03, y - 16, w * 0.97, y + 16), 14 * sc, fill=(232, 236, 246, 255), outline=o, width=5 * sc)
        rows = [(0.15, "YOU SPEND", (90, 170, 255)), (0.52, "REPORTED", (255, 90, 80)), (0.86, "YOU PAY", (70, 210, 120))]
        for i, (fx, txt, c_) in enumerate(rows):
            if kk <= i: continue
            x = w * fx; d.ellipse(S(x - 34, y - 34, x + 34, y + 34), fill=c_ + (255,), outline=o, width=6 * sc)
            d.text(S(x, y + 92), txt, font=font(F_ANTON, int(w * 0.058 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("cycle8", w, kk), mk)


def report_el(w=520, err=False, title="CREDIT REPORT"):
    def mk():
        h = int(w * 1.28); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rounded_rectangle(S(w * 0.03, h * 0.02, w * 0.97, h * 0.98), 20 * sc, fill=(248, 250, 255, 255), outline=o, width=7 * sc)
        d.text(S(w / 2, h * 0.11), title, font=font(F_ANTON, int(w * 0.095 * sc)), fill=(26, 22, 34, 255), anchor="mm")
        for i, yy in enumerate(np.linspace(0.24, 0.88, 7)):
            d.rounded_rectangle(S(w * 0.12, h * yy, w * (0.86 if i % 3 else 0.72), h * yy + 16), 6 * sc, fill=(186, 192, 210, 255))
        if err:
            yy = np.linspace(0.24, 0.88, 7)[3]
            d.rounded_rectangle(S(w * 0.12, h * yy, w * 0.72, h * yy + 16), 6 * sc, fill=(235, 60, 56, 255))
            d.ellipse(S(w * 0.04, h * yy - 40, w * 0.86, h * yy + 56), outline=(235, 60, 56, 255), width=9 * sc)
        return _el4(im, w, h)
    return gcache(("report8", w, err, title), mk)


def contract_el(w=420, title="YOUR DEAL", col=(250, 246, 236)):
    def mk():
        h = int(w * 1.3); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rounded_rectangle(S(w * 0.03, h * 0.02, w * 0.97, h * 0.98), 16 * sc, fill=tuple(col) + (255,), outline=o, width=7 * sc)
        d.text(S(w / 2, h * 0.13), title, font=font(F_ANTON, int(w * 0.11 * sc)), fill=(26, 22, 34, 255), anchor="mm")
        for yy in np.linspace(0.27, 0.70, 5): d.rounded_rectangle(S(w * 0.12, h * yy, w * 0.88, h * yy + 13), 5 * sc, fill=(186, 186, 196, 255))
        d.line(S(w * 0.14, h * 0.88, w * 0.62, h * 0.88), fill=o, width=4 * sc)
        return _el4(im, w, h)
    return gcache(("contract8", w, title, col), mk)
