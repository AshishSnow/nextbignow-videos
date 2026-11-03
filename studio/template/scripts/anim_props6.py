# ================= props kit 6 (exec'd after anim_props5.py) — YOUR MOVE EP 1: the Pepsi jet (R&D run, 3 Nov 2026) =================
# The pilot board named these in prose only, so board_check could not see they did not exist. Generic and logo-free, in the line-art style:
#   can_el(w, band, tilt_label)       plain silver cola can with a green band (never any real can design)
#   can_pile(f, cx, base_y, w, rows)  a heap of cans on the floor, widest row first (the "ocean of Pepsi")
#   padlock_el(w, n, open_)           numbered roadmap padlock; open_=True swings the shackle up and turns the body green
#   calculator_el(w, display)         pocket calculator with a readable display
#   moneybag_el(w, label)             sack with a plain label ("$700K")
#   tee_el(w, col), jacket_el(w, col) prize-catalog clothing icons
#   envelope_el(w, label)             sealed envelope; label is optional
import random
def can_el(w=180, band=(60, 170, 90)):
    def mk():
        h = int(w * 1.75); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rounded_rectangle(S(w * 0.08, h * 0.08, w * 0.92, h * 0.94), 16 * sc, fill=(214, 218, 226, 255), outline=o, width=5 * sc)
        d.rectangle(S(w * 0.08, h * 0.38, w * 0.92, h * 0.68), fill=tuple(band) + (255,))
        d.rectangle(S(w * 0.18, h * 0.10, w * 0.30, h * 0.92), fill=(245, 247, 250, 150))                       # highlight
        d.rounded_rectangle(S(w * 0.08, h * 0.08, w * 0.92, h * 0.94), 16 * sc, outline=o, width=5 * sc)
        d.polygon(S(w * 0.18, h * 0.08, w * 0.82, h * 0.08, w * 0.72, h * 0.02, w * 0.28, h * 0.02), fill=(180, 184, 192, 255), outline=o, width=4 * sc)
        d.text(S(w * 0.5, h * 0.53), "COLA", font=font(F_ANTON, int(w * 0.22 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("can6", int(w), tuple(band)), mk)


def can_pile(f, cx, base_y, w=720, rows=5, can_w=120, seed=7):
    """heap of cans: rows narrow towards the top, slight random tilt; stable between frames for a given seed"""
    rnd = random.Random(seed); ch = can_w * 1.75; n0 = max(1, int(w / (can_w * 0.92)))
    for r in range(rows):
        n = max(1, n0 - r * 2); y = base_y - ch * 0.5 - r * ch * 0.62
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * can_w * 0.92 + rnd.uniform(-8, 8)
            rot_comp(f, can_el(can_w), x, y + rnd.uniform(-6, 6), rnd.uniform(-16, 16))


def padlock_el(w=200, n=None, open_=False):
    def mk():
        h = int(w * 1.3); im, d, S = _im4(w, h); o = _O4; sc = 2
        lift = h * 0.10 if open_ else 0
        d.arc(S(w * 0.24, h * 0.06 - lift, w * 0.76, h * 0.62 - lift), 180, 360, fill=(120, 124, 136, 255), width=int(w * 0.09 * sc))
        d.line(S(w * 0.28, h * 0.34 - lift, w * 0.28, h * 0.46 - lift * 0.4), fill=(120, 124, 136, 255), width=int(w * 0.09 * sc))
        if not open_: d.line(S(w * 0.72, h * 0.34, w * 0.72, h * 0.46), fill=(120, 124, 136, 255), width=int(w * 0.09 * sc))
        col = (60, 180, 100, 255) if open_ else (255, 196, 40, 255)
        d.rounded_rectangle(S(w * 0.08, h * 0.42, w * 0.92, h * 0.96), 14 * sc, fill=col, outline=o, width=6 * sc)
        if n is not None: d.text(S(w * 0.5, h * 0.69), str(n), font=font(F_ANTON, int(h * 0.32 * sc)), fill=(30, 26, 36, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("padlock6", int(w), n, bool(open_)), mk)


def calculator_el(w=300, display="700,000"):
    def mk():
        h = int(w * 1.45); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rounded_rectangle(S(6, 6, w - 6, h - 6), 20 * sc, fill=(66, 72, 88, 255), outline=o, width=6 * sc)
        d.rounded_rectangle(S(w * 0.10, h * 0.08, w * 0.90, h * 0.30), 8 * sc, fill=(190, 216, 170, 255), outline=o, width=4 * sc)
        txt = str(display); fs = int(h * 0.15 * sc)
        while fs > 10 and font(F_ANTON, fs).getlength(txt) > w * 0.72 * sc: fs -= 2
        d.text(S(w * 0.86, h * 0.19), txt, font=font(F_ANTON, fs), fill=(30, 40, 30, 255), anchor="rm")
        for r in range(4):
            for c in range(4):
                x0 = w * (0.10 + c * 0.205); y0 = h * (0.36 + r * 0.15)
                d.rounded_rectangle(S(x0, y0, x0 + w * 0.17, y0 + h * 0.115), 6 * sc, fill=(255, 150, 60, 255) if c == 3 else (232, 234, 240, 255), outline=o, width=3 * sc)
        return _el4(im, w, h)
    return gcache(("calc6", int(w), str(display)), mk)


def moneybag_el(w=300, label="$"):
    def mk():
        h = int(w * 1.15); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.ellipse(S(w * 0.08, h * 0.28, w * 0.92, h * 0.98), fill=(214, 180, 120, 255), outline=o, width=6 * sc)
        d.polygon(S(w * 0.34, h * 0.32, w * 0.66, h * 0.32, w * 0.76, h * 0.06, w * 0.24, h * 0.06), fill=(214, 180, 120, 255), outline=o, width=5 * sc)
        d.line(S(w * 0.32, h * 0.30, w * 0.68, h * 0.30), fill=(190, 60, 50, 255), width=8 * sc)
        txt = str(label); fs = int(h * 0.26 * sc)
        while fs > 10 and font(F_ANTON, fs).getlength(txt) > w * 0.66 * sc: fs -= 2
        d.text(S(w * 0.5, h * 0.64), txt, font=font(F_ANTON, fs), fill=(40, 90, 50, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("bag6", int(w), str(label)), mk)


def tee_el(w=260, col=(240, 80, 70)):
    def mk():
        h = int(w * 0.95); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.polygon(S(w * .30, h * .06, w * .42, h * .13, w * .58, h * .13, w * .70, h * .06, w * .97, h * .28, w * .82, h * .44, w * .74, h * .36, w * .74, h * .95,
                    w * .26, h * .95, w * .26, h * .36, w * .18, h * .44, w * .03, h * .28), fill=tuple(col) + (255,), outline=o, width=6 * sc)
        return _el4(im, w, h)
    return gcache(("tee6", int(w), tuple(col)), mk)


def jacket_el(w=280, col=(50, 90, 170)):
    def mk():
        h = int(w * 1.05); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.polygon(S(w * .30, h * .05, w * .70, h * .05, w * .97, h * .22, w * .94, h * .92, w * .78, h * .92, w * .75, h * .40, w * .75, h * .96,
                    w * .25, h * .96, w * .25, h * .40, w * .22, h * .92, w * .06, h * .92, w * .03, h * .22), fill=tuple(col) + (255,), outline=o, width=6 * sc)
        d.line(S(w * .5, h * .12, w * .5, h * .96), fill=o, width=5 * sc)
        d.polygon(S(w * .40, h * .05, w * .60, h * .05, w * .5, h * .18), fill=(245, 245, 245, 255), outline=o, width=4 * sc)
        return _el4(im, w, h)
    return gcache(("jacket6", int(w), tuple(col)), mk)


def envelope_el(w=340, label=None):
    def mk():
        h = int(w * 0.62); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rounded_rectangle(S(6, 6, w - 6, h - 6), 8 * sc, fill=(250, 246, 232, 255), outline=o, width=5 * sc)
        d.polygon(S(6, 6, w - 6, 6, w * .5, h * .56), fill=(236, 228, 206, 255), outline=o, width=5 * sc)
        if label: d.text(S(w * .5, h * .78), str(label), font=font(F_ANTON, int(h * .15 * sc)), fill=(30, 26, 36, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("env6", int(w), label), mk)
