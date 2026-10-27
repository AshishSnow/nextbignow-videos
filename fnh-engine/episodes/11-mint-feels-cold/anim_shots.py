# ================= shots: FreshNestHub 11 — "Mint doesn't make your mouth cold — it flips your cold alarm" =================
# COLOUR SCRIPT (ep 11): warm sets (orange / yellow / cream / pink) whenever the story is about REAL temperature or warmth,
# icy sets (ice / deepice / sky) whenever the brain FEELS cold, purple for the brain, mint-green for menthol itself.
# The colour flips at the exact word where feeling and reality split, so the colour itself tells the story on mute.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Chew") - 0.15, "punch"), ("S2", T("i3", "But") - 0.15, "focus"), ("S3", T("i4", "And") - 0.15, "whip"),
    ("S4", T("a1", "Meet") - 0.2, "zoom"), ("S4b", T("a1", "It's") - 0.1, "punch"),
    ("S5", T("a2", "Your") - 0.2, "whip"), ("S5b", T("a2", "They're") - 0.15, "zoom"),
    ("S6", T("a3", "And") - 0.2, "zoom"), ("S7", T("a4", "Normally,") - 0.2, "whip"),
    ("S7b", T("a5", "Your") - 0.2, "whip"), ("S7c", T("a5", "Ding!") - 0.15, "punch"),
    ("S8", T("a6", "But") - 0.2, "whip"), ("S8b", T("a6", "like") - 0.15, "flash"),
    ("S9", T("a7", "Click!") - 0.15, "punch"), ("S9b", T("a7", "Your") - 0.1, "zoom"),
    ("S10", T("a8", "Your") - 0.2, "focus"), ("S10b", T("a8", "But") - 0.1, "whip"),
    ("S11", T("b1", "So") - 0.2, "whip"), ("S12", T("b2", "Menthol") - 0.2, "zoom"), ("S12b", T("b2", "Now") - 0.1, "punch"),
    ("S13", T("b3", "It's") - 0.2, "whip"), ("S13b", T("b3", "So") - 0.1, "punch"), ("S14", T("b4", "That's") - 0.2, "whip"),
    ("S15", T("c1", "Scientists") - 0.2, "zoom"), ("S16", T("c2", "Then") - 0.2, "whip"), ("S16b", T("c3", "Those") - 0.2, "punch"),
    ("S17", T("c4", "These") - 0.2, "flash"), ("S17b", T("c5", "Same") - 0.2, "whip"), ("S17c", T("c5", "Chili") - 0.1, "punch"),
    ("S18", T("d1", "Now,") - 0.2, "focus"), ("S19", T("d2", "Scientists") - 0.2, "whip"), ("S20", T("d3", "Within") - 0.2, "zoom"),
    ("S21", T("d4", "But") - 0.2, "whip"), ("S21b", T("d5", "Scientists") - 0.2, "zoom"),
    ("S22", T("e1", "So") - 0.2, "focus"), ("S23", T("e2", "Remember:") - 0.2, "whip"), ("S24", T("e3", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
ICY = (150, 225, 255)


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, acc=YEL_, size=170, y=470, out=None, tail=""):   # white caption on dark/colour sets
    ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.5, lead_col=WHITE, out=out, tail=tail)


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / d))


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def st_(sid): return SHOT[sid]["start"]


def shiver(t, amt=1.0): return amt * 7 * math.sin(t * 61), amt * 3 * math.sin(t * 47)


def mouth_xy(x, y, s): return x, y - 372 * s


# ---------- shared diagram pieces (tongue tissue, nerve wires, wires to brain) ----------
def surface(f, y0, y1, t, x0=0, x1=W):
    g = np.linspace(0, 1, int(y1 - y0))[:, None, None]
    f[int(y0):int(y1), x0:x1] = np.array(C((255, 150, 166)), np.float32) * (1 - g) + np.array(C(TONG_D), np.float32) * g
    for i in range(int((x1 - x0) / 60) + 2):
        px = x0 + i * 60
        cv2.ellipse(f, (int(px), int(y0 + 2)), (30, 26), 0, 180, 360, C((255, 170, 186)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(px), int(y0 + 2)), (30, 26), 0, 180, 360, C(TONG_D), 4, cv2.LINE_AA)


def wire(f, pts, col=NERVE, th=16, lit=0.0, lit_col=(200, 245, 255)):
    P = np.asarray(pts, np.int32)
    cv2.polylines(f, [P], False, C(INK), th + 10, cv2.LINE_AA)
    c = tuple(int(a + (b - a) * lit) for a, b in zip(col, lit_col))
    cv2.polylines(f, [P], False, C(c), th, cv2.LINE_AA)


def frozen_brain(f, x, y, s, t, mood="shout", ice=1.0, shake=0.0):
    sx = shake * 6 * math.sin(t * 57)
    comp(f, scale_el(brain_el(face=True, mood=mood), s), x + sx, y)
    if ice > 0.01:
        glow(f, x, y, 200 * s, (120, 200, 255), 0.5 * ice)
        icicles(f, x + sx, y + 120 * s, 300 * s, ice, 7, s)


def wires_to_brain(f, t, t_pulse=None, lit=0.0, bx=540, by=720, tongue_y=1320, cold=False):
    comp(f, scale_el(tongue_el(), 0.42), bx, tongue_y)
    paths = []
    for j, ox in enumerate((-100, 0, 100)):
        P = [(bx + ox, tongue_y - 80), (bx + ox * 0.9 + 30 * math.sin(j), (tongue_y + by) / 2 + 60), (bx + ox * 0.4, by + 130)]
        wire(f, P, lit=lit); paths.append(P)
    if cold: frozen_brain(f, bx, by, 1.05, t, "shout", lit, lit)
    else: comp(f, scale_el(brain_el(face=True, mood="n"), 1.05), bx, by)
    if t_pulse is not None:
        for j, P in enumerate(paths): pulse_path(f, P, t, t_pulse + 0.08 * j, 0.55, (200, 245, 255) if cold else (255, 236, 110), n=3, gap=0.3)
    return paths


def ladder_items():
    return [(scale_el(chub_head_el(2, False, "up", 0, 0, "happy"), 0.55), "YOU", None),
            (scale_el(tongue_el(), 0.17), "TONGUE", "x5"),
            (scale_el(nerve_icon_el(), 0.55), "NERVE", "x100"),
            (scale_el(calarm_el(False), 0.5), "COLD ALARM", "x1000")]


# ---- S0: HOOK — Chubby sips ice water after gum... and FREEZES into a block of ice ----
TF0 = T("i1", "mint...") + 0.05


def shot_S0(t, n):
    frozen = t >= TF0; q = t - TF0
    f = stage("sky" if not frozen else "ice", (255, 236, 160) if not frozen else (235, 250, 255), 540, 900, 440)
    if frozen: rays(f, 540, 900, 760, (230, 250, 255), 0.45 * ramp(t, TF0, 0.2), t)
    gl = scale_el(ice_glass_el(0.7), 0.42)
    if not frozen:
        m, c = munch(t, 0.3)
        chub(f, 540, 1460, 1.12, la=(20, 10), ra=(148, -130), mouth=m, brow="up", expr="happy", hold=gl, hold_off=(-36, -20), hold_front=True,
             bob=5 * math.sin(t * 16), lean=-3 * math.sin(t * 8))
    else:
        dx, dy = shiver(t, 0.6 + 0.4 * math.exp(-q * 3))
        chub(f, 540 + dx, 1460 + dy, 1.12, la=(20, 10), ra=(148, -130), mouth="o", brow="up", expr="wow", look=(0, -0.6), hold=gl, hold_off=(-36, -20), hold_front=True, squash=0.3 * math.exp(-q * 6))
        hx, hy = head_pos(540 + dx, 1460 + dy, 1.12)
        icicles(f, hx, hy + 96, 180, ramp(t, TF0 + 0.2, 0.4), 6, 1.0)
        ice_block(f, 290, 880, 790, 1490, clamp(q / 0.28), t)
        frost(f, 0.7 * ramp(t, TF0, 0.5)); snow(f, t, ramp(t, TF0 + 0.2, 0.5), 40)
        breath(f, hx + 60, hy + 70, t, TF0 + 0.5, 1, 1.0, 1.4)
        comp(f, burst_el("FREEZE!", ICY, INK, 60), 860, 760, scale=pin(t, TF0 + 0.05, 0.22) * (1 - clamp((t - T("i1", "doesn't")) / 0.2)))
    ui_word(f, "do you know", "[MINT]", 470, t, 0.15, col=INK, acc=(10, 150, 100), size=230, out=T("i1", "doesn't") - 0.05)
    ui_word(f, "doesn't make your mouth", "[COLD]?", 470, t, T("i1", "doesn't"), col=INK, acc=COLDB_D, size=220, tail="at all")
    return finish(f, n)


# ---- S1: chew -> sip -> FREEZING (step strip) ----
def shot_S1(t, n):
    f = stage("deepice", (200, 240, 255), 540, 980, 300); u = lt(t, "S1")
    tw = T("i2", "whoa,") - 0.1
    items = [(scale_el(gum_el(), 0.5), "CHEW GUM"), (scale_el(ice_glass_el(0.7), 0.6), "SIP WATER"),
             (scale_el(chub_head_el("o", False, "up", 0, -0.5, "wow"), 0.85), "FREEZING!")]
    recap_steps(f, items, 780, t, [T("i2", "Chew") - 0.05, T("i2", "sip") - 0.05, tw], 320)
    fr = ramp(t, tw, 0.3)
    dx, dy = shiver(t, fr)
    chub(f, 540 + dx, 1490, 0.72, la=(150, 175) if fr > 0.5 else (20, 10), ra=(150, 175) if fr > 0.5 else (148, -130), mouth="o" if fr > 0.5 else munch(t, 0.3)[0],
         expr="wow" if fr > 0.5 else "happy", brow="up", hold=None if fr > 0.5 else scale_el(gum_el(), 0.18), hold_off=(-20, -10), hold_front=True)
    snow(f, t, fr, 50); frost(f, 0.6 * fr, 3)
    if fr > 0: comp(f, burst_el("BRRR!", ICY, INK, 56), 820, 1240, scale=pin(t, tw + 0.1, 0.22))
    return finish(f, n)


# ---- S2: but nothing got colder — it's a trick ----
def shot_S2(t, n):
    tn = T("i3", "nothing") - 0.1; tt = T("i3", "trick!") - 0.15
    f = stage("cream", (255, 210, 150), 540, 980, 420); u = lt(t, "S2")
    dx, dy = shiver(t, 0.5 * (1 - ramp(t, tt, 0.4)))
    chub(f, 330 + dx, 1470, 0.95, la=(20, 10), ra=(60, 40), mouth="o" if t < tt else 2, expr="wow" if t < tt else "sus", brow="up" if t < tt else "sus", look=(1, 0))
    thermo_c(f, 760, 1360, 0.74, 520, (255, 110, 70), labels=((0, "0"), (0.5, "25"), (1.0, "50")))
    if t >= tn:
        slam(f, stamp_el("NO COLDER", RED_, 50), 760, 760, -6, t, tn + 0.1)
        label_at(f, "MOUTH TEMP: SAME", 560, 650, t, tn + 0.4)
    if t >= tt:
        q = clamp((t - tt) / 0.35)
        mx, my = mouth_xy(330, 1470, 0.95)
        menthol(f, mx + 230 * eo(q), my - 120 * eo(q), 0.75, t, "sly", rot=-10)
        comp(f, burst_el("TRICK!", (120, 255, 190), INK, 62), 300, 760, scale=pin(t, tt + 0.05, 0.25))
    ui_word(f, "but nothing got", "[COLDER]", 470, t, tn, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S3: open loop — it even fools your nose (teaser) ----
def shot_S3(t, n):
    f = stage("mintg", (220, 255, 235), 540, 980, 430); u = lt(t, "S3")
    z = 2.0 + 0.25 * eo(clamp(u / 2.0))
    tn = T("i4", "nose.") - 0.15
    chub_head_only(f, 540, 1040, z, t, mouth=talk(t) if t < tn else "o", expr="n" if t < tn else "wow", brow="up", look=(0, 0.6), nose=0.0)
    if t >= tn:
        for j in range(3):
            ph = (t * 1.6 + j / 3) % 1.0
            ov = f.copy(); cv2.ellipse(ov, (540, int(1130 + 30 * ph)), (int(60 + 110 * ph), int(26 + 40 * ph)), 0, 0, 360, C(ICY), 8, cv2.LINE_AA)
            a = 0.8 * (1 - ph); f[:] = f * (1 - a) + ov * a
        menthol(f, 840, 860, 0.55, t, "sly", rot=12)
        comp(f, chip("COMING UP: THE NOSE TRICK", INK, YEL_, 30), 540, 1430, op=clamp((t - tn - 0.2) / 0.3))
    wui(f, "and it even fools your", "[NOSE]", t, st_("S3") + 0.1, acc=YEL_, size=220)
    return finish(f, n)


# ---- S4: PART 1 — meet the trickster (mint leaves, magnifier finds the chemical) ----
def shot_S4(t, n):
    f = stage("yellow", (255, 255, 220), 540, 1000, 420); u = lt(t, "S4")
    for i, (px, py, r, s_) in enumerate(((380, 1060, -22, 0.95), (620, 1000, 18, 1.05), (500, 1190, 4, 0.9))):
        rot_comp(f, scale_el(mint_leaf_el(i == 1, "sly"), s_), px, py + 6 * math.sin(t * 2 + i), r + 4 * math.sin(t * 1.5 + i), pin(t, st_("S4") + 0.05 * i, 0.3), 1.0, 0.3)
    tm = st_("S4") + 0.6
    if t >= tm:
        k = ramp(t, tm, 0.5); mx, my = 820 - 200 * k, 1300 - 230 * k
        comp(f, magnifier_el(), mx, my + 80)
        for j in range(2): menthol(f, mx - 50 + 80 * j, my - 40 + 60 * j, 0.32, t + j, "sly", rot=-12 + 24 * j)
    chapter_card(f, t, st_("S4") + 0.05, 1, "THE COLD ALARM", y=1400, dur=1.6, col=(120, 255, 190))
    ui_word(f, "meet the", "[TRICKSTER]", 470, t, st_("S4") + 0.1, col=INK, acc=(10, 140, 100), size=200)
    return finish(f, n)


# ---- S4b: name card — MENTHOL ----
def shot_S4b(t, n):
    f = stage("ice", (240, 252, 255), 540, 1000, 440); u = lt(t, "S4b")
    menthol(f, 540, 1010, 1.55 * pin(t, st_("S4b") + 0.05, 0.3), t, "sly", rot=-6)
    rot_comp(f, scale_el(mint_leaf_el(True, "happy"), 0.5), 210, 1330, -14, 1.0, 1.0, 0.3)
    comp(f, chip("a chemical in mint leaves", INK, WHITE, 32), 600, 1330, op=clamp((t - T("a1", "chemical") + 0.1) / 0.3))
    label_at(f, "RING SHAPE", 840, 760, t, st_("S4b") + 0.6, 450, 900, bg=COLDB_D)
    wui(f, "it's called", "[MENTHOL]", t, T("a1", "menthol,") - 0.1, acc=(30, 120, 210), size=200)
    return finish(f, n)


# ---- S5: POWERS OF TEN zoom — you -> tongue -> nerve endings (scale ladder mini-map) ----
def _s5_far(t):
    f = stage("pink", (255, 230, 210), 540, 960, 430)
    chub_head_only(f, 540, 900, 2.4, t, mouth=3, expr="happy", brow="up")
    return f


def _s5_near(t, kin):
    f = stage("pink", (255, 236, 220), 540, 980, 430)
    comp(f, tongue_el(), 460, 1000, scale=0.95)
    if kin > 0.01:
        def close(g):
            g[:] = np.array(C((40, 20, 60)), np.float32)
            surface(g, 640, 900, t, 520, 1000)
            for i, x in enumerate((640, 760, 880)):
                wire(g, [(x + 20 * math.sin(i), 1200), (x - 15, 1010), (x, 790)])
                cv2.circle(g, (x, 780), 24, C(INK), -1, cv2.LINE_AA); cv2.circle(g, (x, 780), 16, C(NERVE), -1, cv2.LINE_AA)
        draw_arrow(f, 430, 880, 600, 860, kin, WHITE, 8, 26)
        inset(f, 760, 900, 230, close, kin)
    return f


def shot_S5(t, n):
    u = lt(t, "S5"); tz = st_("S5") + 0.15; tn = T("a2", "nerve") - 0.25
    kin = ramp(t, tn - 0.2, 0.35)
    f = zoom_through(t, tz, 1.0, lambda: _s5_far(t), lambda: _s5_near(t, kin), 540, 1015, 5.0).astype(np.float32)
    items = ladder_items()
    cur = 0 if t < tz + 0.6 else (1 if t < tn else 2)
    tc = st_("S5") if cur == 0 else (tz + 0.6 if cur == 1 else tn)
    scale_ladder(f, items, cur, t, tc, y=1395, gap=200, s=0.5)
    if t >= tn: label_at(f, "NERVE ENDINGS", 760, 1190, t, tn + 0.15, bg=INK)
    if t >= tn: wui(f, "full of tiny", "[NERVE ENDINGS]", t, tn, acc=YEL_, size=130)
    else: wui(f, "your", "[TONGUE]", t, st_("S5") + 0.1, acc=YEL_, size=220)
    return finish(f, n)


# ---- S5b: nerves = wires to your brain ----
def shot_S5b(t, n):
    f = stage("emerald", (255, 236, 200), 540, 980, 440); u = lt(t, "S5b")
    tw = T("a2", "wires") - 0.15
    wires_to_brain(f, t, t_pulse=tw)
    label_at(f, "NERVES = WIRES", 820, 1040, t, tw, 620, 1020)
    label_at(f, "BRAIN", 860, 600, t, T("a2", "brain.") - 0.15, 740, 680)
    return finish(f, n)


# ---- S6: on those wires sit little COLD ALARMS (ladder level 4) ----
def shot_S6(t, n):
    f = stage("deepice", (200, 240, 255), 540, 1000, 380); u = lt(t, "S6")
    ta = T("a3", "cold") - 0.2
    surface(f, 640, 1290, t)
    for i, (x, s_) in enumerate(((220, 0.6), (540, 1.15), (860, 0.6))):
        wire(f, [(x, 1290), (x - 20, 1150), (x, 900 + (40 if i != 1 else 90))])
        if t >= ta + 0.12 * abs(i - 1): calarm(f, x, 860 + (0 if i != 1 else 60), s_ * pin(t, ta + 0.12 * abs(i - 1), 0.3), t + i)
    label_at(f, "COLD ALARM", 800, 1170, t, ta + 0.3, 620, 990, bg=COLDB_D)
    comp(f, chip("scientists call it TRPM8", INK, WHITE, 26), 540, 1240, op=clamp((t - ta - 0.6) / 0.3))
    scale_ladder(f, ladder_items(), 3, t, ta, y=1395, gap=200, s=0.5)
    wui(f, "on those wires sit little", "[COLD ALARMS]", t, st_("S6") + 0.1, acc=ICY, size=150)
    return finish(f, n)


# ---- S7: they only ring below about 25 degrees (thermometer + alarm line; the set turns icy when it rings) ----
def shot_S7(t, n):
    t25 = T("a4", "twenty-five") - 0.1
    u = lt(t, "S7"); dd = max(0.5, t25 + 0.3 - st_("S7") - 0.3)
    k = 0.8 - 0.42 * ramp(t, st_("S7") + 0.3, dd)
    cold = k < 0.5
    f = stage("ice" if cold else "orange", (235, 250, 255) if cold else (255, 220, 140), 700, 1000, 380)
    thermo_c(f, 300, 1400, k, 640, (60, 150, 255) if cold else (255, 90, 60), trig=0.5, trig_lab="ALARM LINE")
    calarm(f, 740, 1040, 1.35, t, ring=1.0 if cold else 0.0)
    if not cold: comp(f, chip("warm: silent", INK, WHITE, 30), 740, 1280, op=clamp((u - 0.3) / 0.3))
    else: slam(f, stamp_el("COOL: RING!", COLDB_D, 48), 740, 1300, -4, t, st_("S7") + 0.3 + dd * 0.72)
    if t >= t25: ui_word(f, "below about", "[25°C]", 470, t, t25, col=INK, acc=COLDB_D, size=200)
    else: ui_word(f, "they only ring when things get", "[COOL]", 470, t, st_("S7") + 0.1, col=INK, acc=COLDB_D, size=200)
    return finish(f, n)


# ---- S7b: your mouth is warmer than that... so ice water? ----
def shot_S7b(t, n):
    f = stage("yellow", (255, 240, 200), 540, 980, 420); u = lt(t, "S7b")
    ti = T("a5", "ice") - 0.2
    up = ramp(t, ti, 0.35)
    chub(f, 400, 1470, 1.0, la=(20, 10), ra=(148 * up + 20 * (1 - up), -130 * up + 10 * (1 - up)), mouth=talk(t) if up < 0.5 else "o", expr="happy" if up < 0.5 else "wow", brow="up",
         hold=scale_el(ice_glass_el(0.75), 0.42), hold_off=(-36, -20), hold_front=True, look=(0.6, -0.3))
    hx, hy = head_pos(400, 1470, 1.0)
    label_at(f, "WARM MOUTH", 760, 700, t, st_("S7b") + 0.25, hx + 50, hy + 50, bg=(214, 80, 40))
    calarm(f, 800, 1150, 0.85, t, ring=0.0)
    if up < 0.5: comp(f, ed_el("", "z z", "", big_col=INK, big_size=60), 880, 1010 - 10 * math.sin(t * 3))
    ui_word(f, "your mouth is", "[WARMER]", 470, t, st_("S7b") + 0.1, col=INK, acc=RED_, size=200, out=ti - 0.05)
    if t >= ti: ui_word(f, "so", "[ICE WATER]?", 470, t, ti, col=INK, acc=COLDB_D, size=180)
    return finish(f, n)


# ---- S7c: DING! cold alarm ----
def shot_S7c(t, n):
    f = stage("ice", (240, 252, 255), 540, 1000, 450); u = lt(t, "S7c")
    rays(f, 540, 1000, 760, (230, 250, 255), 0.4, t)
    calarm(f, 540, 1080, 2.0, t, ring=1.0)
    frost(f, 0.55 * ramp(t, st_("S7c"), 0.4)); snow(f, t, 0.6, 26)
    comp(f, burst_el("DING!", WHITE, COLDB_D, 74), 790, 720, scale=pin(t, st_("S7c") + 0.05, 0.22))
    wui(f, "", "[COLD ALARM!]", t, T("a5", "Cold") - 0.1, acc=COLDB_D, size=170, y=1360)
    return finish(f, n)


# ---- S8: but menthol fits the cold alarm (arc flight into the keyhole) ----
AX, AY, AS = 700, 1080, 1.4


def shot_S8(t, n):
    f = stage("teal", (220, 250, 240), AX, AY, 380); u = lt(t, "S8")
    tf = T("a6", "fits") - 0.05
    surface(f, AY + 140, 1540, t, 0, W)
    wire(f, [(AX, 1520), (AX, AY + 120)])
    inn = t >= tf
    calarm(f, AX, AY, AS, t, key_in=inn)
    k = eio(clamp((t - st_("S8") - 0.1) / max(0.2, tf - st_("S8") - 0.1)))
    sx, sy = 200, 780; ex, ey = AX - 150 * 0.8 - 30, AY + 10
    cx_ = sx + (ex - sx) * k; cy_ = sy + (ey - sy) * k - 170 * math.sin(math.pi * k)
    if not inn:
        if 0.2 < k < 0.9: smear(f, scale_el(menthol_el("sly"), 0.7), cx_ - 40, cy_ + 20, cx_, cy_, 4, 0.25)
        else: menthol(f, cx_, cy_, 0.7, t, "sly")
    else:
        menthol(f, cx_, cy_, 0.7, t, "happy", wig=False)
        sparkles(f, AX, AY, t, tf, 12, 200, (220, 250, 255))
        comp(f, check_el(46, True), AX + 190, AY - 150, scale=pin(t, tf + 0.1, 0.25))
    wui(f, "menthol", "[FITS] the cold alarm", t, st_("S8") + 0.1, acc=YEL_, size=130)
    return finish(f, n)


# ---- S8b: like a key fits a lock (side-by-side analogy) ----
def shot_S8b(t, n):
    f = stage("yellow"); u = lt(t, "S8b")
    k = ramp(t, st_("S8b") + 0.15, 0.55)
    comp(f, padlock_el(k >= 1), 290, 1060, scale=0.95)
    rot_comp(f, scale_el(key_el(), 0.8), 290 - 360 + 330 * k, 1120, 0, 1.0, 1.0, 0.2)
    calarm(f, 790, 1060, 1.45, t, key_in=k >= 1, ring=1.0 if k >= 1 else 0)
    if k < 1: menthol(f, 790 - 380 + 160 * k, 1085, 0.72, t, "sly", wig=False)
    comp(f, chip("KEY + LOCK", INK, WHITE, 32), 290, 1330); comp(f, chip("MENTHOL + ALARM", INK, WHITE, 32), 790, 1330)
    cv2.circle(f, (540, 1060), 58, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (540, 1060), 50, (1, 1, 1), -1, cv2.LINE_AA)
    comp(f, ed_el("", "=", "", big_col=INK, big_size=90), 540, 1062, scale=pin(t, st_("S8b") + 0.3, 0.25))
    ui_word(f, "like a", "[KEY] fits a [LOCK]", 470, t, st_("S8b") + 0.05, col=INK, acc=RED_, size=130)
    return finish(f, n)


# ---- S9: CLICK! the alarm rings ----
def shot_S9(t, n):
    f = stage("deepice", (200, 240, 255), 540, 1040, 470); u = lt(t, "S9")
    tc = st_("S9") + 0.1; turn = ramp(t, tc, 0.15)
    rays(f, 540, 1040, 760, (200, 240, 255), 0.45 * turn, t)
    surface(f, 1240, 1560, t)
    calarm(f, 540, 1080, 2.1, t, ring=turn, key_in=True)
    menthol(f, 540 - 150 - 60, 1100 - 30 * turn, 0.95, t, "happy", rot=-25 * turn, wig=False)
    comp(f, burst_el("CLICK!", WHITE, COLDB_D, 70), 800, 700, scale=pin(t, tc, 0.22))
    wui(f, "the alarm", "[RINGS]", t, T("a7", "rings.") - 0.15, acc=ICY, size=200)
    return finish(f, n)


# ---- S9b: nerves tell your brain... it's COLD! (brain freezes) ----
def shot_S9b(t, n):
    tC = T("a7", "COLD!") - 0.15; lit = 1.0 if t >= tC else 0.0
    f = stage("purple" if not lit else "ice", (220, 245, 255) if lit else None, 540, 760, 380)
    if lit: snow(f, t, 0.8, 40); frost(f, 0.5)
    wires_to_brain(f, t, t_pulse=st_("S9b") + 0.05, lit=lit, by=800, cold=True)
    calarm(f, 540, 1210, 0.6, t, ring=1.0, key_in=True)
    if lit: comp(f, burst_el("COLD!", WHITE, COLDB_D, 74), 820, 1000, scale=pin(t, tC, 0.22))
    else: label_at(f, "SIGNAL", 810, 1060, t, st_("S9b") + 0.2, 620, 1020)
    wui(f, "your nerves tell your", "[BRAIN]", t, st_("S9b") + 0.1, acc=YEL_, size=150, y=430, out=tC - 0.05)
    return finish(f, n)


# ---- S10: your brain believes it (shivering brain with icicles) ----
def shot_S10(t, n):
    f = stage("purple", (200, 230, 255), 540, 980, 420); u = lt(t, "S10")
    frozen_brain(f, 540, 1040, 1.5, t, "worried", 1.0, 1.0)
    snow(f, t, 0.7, 30)
    comp(f, think_el("IT'S FREEZING!", 40), 700, 700, scale=pin(t, T("a8", "believes") - 0.1, 0.3))
    wui(f, "your brain", "[BELIEVES] it", t, st_("S10") + 0.1, acc=ICY, size=160, y=470, out=T("a8", "believes") + 0.25)
    return finish(f, n)


# ---- S10b: what you feel vs the real temperature (contrast panels) ----
def shot_S10b(t, n):
    f = stage("cream"); u = lt(t, "S10b")
    td = T("a8", "didn't") - 0.1
    def left(g):
        dx, dy = shiver(t, 0.8)
        chub(g, 330 + dx, 1400, 0.7, la=(150, 175), ra=(150, 175), mouth="o", expr="wow", brow="up")
        hx, hy = head_pos(330 + dx, 1400, 0.7); icicles(g, hx, hy + 60, 120, 1.0, 5, 0.7)
        snow(g, t, 0.8, 26, 9, 620, 1500)
    def right(g):
        thermo_c(g, 750, 1380, 0.74, 560, (255, 110, 70), labels=((0, "0"), (0.5, "25"), (1.0, "50")))
        if t >= td: slam(g, stamp_el("SAME", RED_, 58), 750, 762, -6, t, td + 0.1)
    split_contrast(f, t, st_("S10b") + 0.02, left, right, "WHAT YOU FEEL", "REAL TEMPERATURE", (60, 150, 255), (255, 120, 60), y0=620, y1=1500, t_r=st_("S10b") + 0.35)
    ui_word(f, "the temperature", "[DIDN'T CHANGE]", 470, t, td, col=INK, acc=RED_, size=150)
    return finish(f, n)


# ---- S11: PART 2 — why does water feel like ice after mint? ----
def shot_S11(t, n):
    f = stage("sky", (240, 250, 255), 540, 980, 430); u = lt(t, "S11")
    m, c = munch(t, 0.32)
    chub(f, 540, 1470, 1.05, la=(-150, -150), ra=(148, -130), mouth=m, brow="sus", expr="sus", look=(0.4, -0.6), hold=scale_el(ice_glass_el(0.75), 0.44), hold_off=(-36, -20), hold_front=True)
    comp(f, burst_el("?", WHITE, COLDB_D, 90), 820, 820, scale=pin(t, st_("S11") + 0.3, 0.25) * (1 + 0.05 * math.sin(t * 6)))
    chapter_card(f, t, st_("S11") + 0.02, 2, "WHY WATER FEELS ICY", y=1400, dur=1.7, col=ICY)
    wui(f, "why does water feel like", "[ICE] after mint?", t, st_("S11") + 0.1, acc=YEL_, size=140)
    return finish(f, n)


# ---- S12: menthol makes the alarm JUMPY ----
def shot_S12(t, n):
    f = stage("mintg", (220, 255, 235), 540, 1000, 430); u = lt(t, "S12")
    tj = T("b2", "jumpy.") - 0.15
    jm = ramp(t, tj, 0.3)
    calarm(f, 540, 1080, 2.0, t, ring=0.2 * jm, key_in=True, jumpy=jm)
    menthol(f, 540 - 300, 1110, 0.95, t, "sly", rot=-20, wig=False)
    if jm > 0:
        sweat(f, 540, 820, t, 3, 1.1); comp(f, burst_el("JUMPY!", YEL_, INK, 60), 820, 760, scale=pin(t, tj + 0.05, 0.22))
    wui(f, "menthol makes the alarm", "[JUMPY]", t, st_("S12") + 0.1, acc=YEL_, size=200)
    return finish(f, n)


# ---- S12b: now it rings even when it's warmer (the trigger line moves UP) ----
def shot_S12b(t, n):
    f = stage("cream", (230, 250, 240), 600, 1000, 380); u = lt(t, "S12b")
    tw = T("b2", "warmer") - 0.2
    trig = 0.5 + 0.13 * ramp(t, tw, 0.6)
    thermo_c(f, 300, 1340, 0.58, 600, (255, 160, 60), trig=trig, trig_lab="WITH MENTHOL" if t >= tw else "ALARM LINE")
    yn = 1340 - 20 - 560 * 0.5
    if t >= tw:
        for xx in range(250, 560, 26): cv2.line(f, (xx, int(yn)), (xx + 14, int(yn)), C((150, 150, 160)), 5, cv2.LINE_AA)
        comp(f, chip("normal", (150, 150, 160), WHITE, 22), 620, yn + 4)
        draw_arrow(f, 470, yn - 10, 470, 1340 - 20 - 560 * trig + 14, ramp(t, tw, 0.4), COLDB_D, 9, 26)
    calarm(f, 780, 1100, 1.2, t, ring=1.0 if t >= tw + 0.45 else 0.0, key_in=True, jumpy=0.6)
    if t >= tw + 0.45: comp(f, chip("rings while it's still warm", COLDB_D, WHITE, 28), 780, 1330, op=clamp((t - tw - 0.45) / 0.25))
    ui_word(f, "it rings even when it's", "[WARMER]", 470, t, st_("S12b") + 0.05, col=INK, acc=(230, 90, 30), size=190)
    comp(f, chip("Source: McKemy, Neuhausser & Julius, Nature 2002", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    return finish(f, n)


# ---- S13: it's already HALF ringing ----
def shot_S13(t, n):
    f = stage("ice", (240, 252, 255), 600, 1000, 400); u = lt(t, "S13")
    th = T("b3", "half") - 0.1
    kk = 0.5 * ramp(t, th, 0.5)
    gauge_tube(f, 260, 760, 1360, kk, 1.0, 90, (90, 180, 255), "")
    comp(f, chip("ALARM LEVEL", INK, WHITE, 26), 260, 700)
    if kk > 0.1: comp(f, chip("HALF!", COLDB_D, WHITE, 30), 260, 1420, op=clamp((t - th) / 0.3))
    calarm(f, 690, 1100, 1.6, t, ring=0.4 * ramp(t, th, 0.4), key_in=True, jumpy=0.5)
    menthol(f, 690 - 240, 1130, 0.7, t, "sly", wig=False, rot=-20)
    wui(f, "it's already", "[HALF RINGING]", t, st_("S13") + 0.1, acc=COLDB_D, size=150)
    return finish(f, n)


# ---- S13b: cool water hits... it SCREAMS ----
def shot_S13b(t, n):
    ts = T("b3", "screams!") - 0.15; tw = T("b3", "water") - 0.15
    f = stage("deepice" if t >= ts else "ice", (220, 245, 255), 600, 1000, 400); u = lt(t, "S13b")
    kk = 0.5 + 0.5 * ramp(t, ts, 0.2)
    gauge_tube(f, 260, 760, 1360, kk, 1.0, 90, (90, 180, 255) if kk < 0.9 else (255, 255, 255), "")
    comp(f, chip("ALARM LEVEL", INK, WHITE, 26), 260, 700)
    if t >= tw:
        k = ramp(t, tw, 0.25)
        rot_comp(f, scale_el(ice_glass_el(0.75), 0.6), 760 - 40 * k, 620 + 60 * k, 130 * k, 1.0, 1.0, 0.2)
        splash(f, 690, 900, t, tw + 0.2, 1.0, 50, 6, 1.2)
    big = kk > 0.9
    calarm(f, 690, 1150, 1.8 if big else 1.6, t, ring=1.0 if big else 0.4, key_in=True)
    if t >= ts:
        frost(f, 0.7); comp(f, burst_el("SCREAMS!", WHITE, COLDB_D, 64), 690, 800, scale=pin(t, ts, 0.22))
        comp(f, chip("FULL BLAST", INK, WHITE, 30), 260, 1420)
    wui(f, "then cool water", "[HITS]", t, st_("S13b") + 0.05, acc=YEL_, size=190, out=ts - 0.05)
    return finish(f, n)


# ---- S14: even a HOT drink feels weirdly cool ----
def shot_S14(t, n):
    f = stage("orange", (255, 220, 140), 540, 980, 430); u = lt(t, "S14")
    tc = T("b4", "cool") - 0.15
    cool = ramp(t, tc, 0.4)
    chub(f, 470, 1470, 1.05, la=(20, 10), ra=(148, -130), mouth=0 if cool < 0.5 else "o", expr="happy" if cool < 0.5 else "wow", brow="up", look=(0.5, -0.4),
         hold=scale_el(teacup_el(), 0.5), hold_off=(-40, 0), hold_front=True)
    steam(f, 430, 960, t, 1.0, 0.6)
    label_at(f, "HOT DRINK", 820, 1250, t, T("b4", "hot") - 0.1, 560, 1110, bg=(214, 60, 30))
    if cool > 0:
        hx, hy = head_pos(470, 1470, 1.05)
        icicles(f, hx, hy + 92, 170, cool, 6, 1.0); snow(f, t, cool * 0.7, 26, 2, 600, 1300)
        breath(f, hx + 70, hy + 60, t, tc + 0.1, 1, 1.0, 1.2)
        comp(f, burst_el("COOL?!", ICY, INK, 56), 830, 820, scale=pin(t, tc + 0.05, 0.22))
    ui_word(f, "even a hot drink feels weirdly", "[COOL]", 470, t, st_("S14") + 0.1, col=WHITE, acc=ICY, size=200, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S15: PART 3 — the proof: found in 2002 ----
def shot_S15(t, n):
    f = stage("cream", (255, 236, 200), 540, 1000, 400); u = lt(t, "S15")
    scientist(f, 220, 1470, 0.72, la=(70, 40), ra=(20, 10), mouth=talk(t), expr="happy", brow="up", look=(1, 0))
    scientist(f, 860, 1470, 0.72, la=(20, 10), ra=(70, 40), mouth=0, expr="wow", brow="up", look=(-1, 0), bob=4 * math.sin(t * 3))
    calarm(f, 540, 1150, 1.1, t, ring=0.6)
    comp(f, magnifier_el(), 600 + 20 * math.sin(t * 2), 1240, scale=0.8)
    ty = T("c1", "two") - 0.1
    if t >= ty: slam(f, calendar_el("FOUND IN", "2002"), 540, 780, -4, t, ty, 0.62)
    chapter_card(f, t, st_("S15") + 0.02, 3, "THE PROOF", y=1400, dur=1.5, col=YEL_)
    ui_word(f, "scientists", "[FOUND] it", 470, t, st_("S15") + 0.1, col=INK, acc=RED_, size=180, out=ty - 0.05)
    return finish(f, n)


# ---- S16: mice born WITHOUT the cold alarm ----
def shot_S16(t, n):
    f = stage("lime", (240, 255, 210), 540, 1000, 400); u = lt(t, "S16")
    tw = T("c2", "without") - 0.15
    for i, (x, has) in enumerate(((300, True), (780, False))):
        rot_comp(f, scale_el(mouse_el(False, False), 1.0), x, 1240 + 6 * math.sin(t * 3 + i), 0, pin(t, st_("S16") + 0.1 + 0.2 * i, 0.3), 1.0, 0.3)
        calarm(f, x, 960, 0.75, t)
        if not has and t >= tw:
            k = clamp((t - tw) / 0.18)
            for sg in (-1, 1):
                cv2.line(f, (int(x - 90), int(960 - sg * 90)), (int(x - 90 + 180 * k), int(960 - sg * 90 + sg * 180 * k)), C(INK), 30, cv2.LINE_AA)
                cv2.line(f, (int(x - 90), int(960 - sg * 90)), (int(x - 90 + 180 * k), int(960 - sg * 90 + sg * 180 * k)), C(RED_), 18, cv2.LINE_AA)
        comp(f, chip("NORMAL MOUSE" if has else "NO COLD ALARM", INK, WHITE, 28), x, 1400, op=clamp((u - 0.3) / 0.3) if has else clamp((t - tw) / 0.3))
    wui(f, "mice born", "[WITHOUT] it", t, st_("S16") + 0.1, acc=YEL_, size=180)
    return finish(f, n)


# ---- S16b: on a cool floor — normal mouse hops about, no-alarm mouse just sits ----
def shot_S16b(t, n):
    f = stage("sky", (240, 250, 255), 540, 1000, 400); u = lt(t, "S16b")
    ice_floor(f, 120, 520, 1300); ice_floor(f, 560, 960, 1300)
    hop = abs(math.sin(t * 7)) * 60
    dx, dy = shiver(t, 1.0)
    rot_comp(f, scale_el(mouse_el(False, True), 1.25), 320 + dx, 1215 - hop, 6 * math.sin(t * 7), 1.0, 1.0, 0.0)
    snow(f, t, 0.6, 16, 4, 620, 1290)
    rot_comp(f, scale_el(mouse_el(False, False), 1.25), 760, 1218, 0, 1.0, 1.0, 0.3)
    comp(f, ed_el("", "z z", "", big_col=INK, big_size=60), 880, 1060 - 8 * math.sin(t * 3))
    comp(f, chip("NORMAL: BRRR!", INK, WHITE, 26), 320, 1400); comp(f, chip("NO ALARM: CHILL", INK, WHITE, 26), 760, 1400)
    tg = T("c3", "gone!") - 0.15
    if t >= tg: slam(f, stamp_el("ALARM GONE", RED_, 48), 760, 860, -6, t, tg)
    ui_word(f, "they hardly reacted to", "[COOL]", 470, t, st_("S16b") + 0.1, col=INK, acc=COLDB_D, size=190)
    comp(f, chip("Source: Bautista et al., Nature 2007", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    return finish(f, n)


# ---- S17: a Nobel Prize ----
def shot_S17(t, n):
    f = stage("purple", (255, 230, 150), 540, 980, 420); u = lt(t, "S17")
    tn = T("c4", "Nobel") - 0.15
    rays(f, 540, 980, 760, (255, 230, 150), 0.35 * ramp(t, tn, 0.3), t)
    sp = math.cos(clamp((t - st_("S17")) / 0.8) * math.pi * 3)
    if t >= st_("S17") + 0.8: rot_comp(f, scale_el(medal_el("2021"), 1.0), 540, 1030 + 10 * math.sin(t * 2), 0, 1.0, 1.0, 0.3)
    else: comp(f, scale_xy(scale_el(medal_el("2021"), 1.0), max(0.08, abs(sp)), 1.0), 540, 1030)
    sparkles(f, 540, 1000, t, tn, 14, 300); confetti(f, t, tn, 36, 7)
    calarm(f, 280, 1380, 0.55, t, ring=0.4); alarm(f, 800, 1380, 0.55, t, ring=0.4)
    wui(f, "helped win the 2021", "[NOBEL PRIZE]", t, st_("S17") + 0.1, acc=YEL_, size=160)
    return finish(f, n)


# ---- S17b: same prize as our spicy video (callback in a frame) ----
def shot_S17b(t, n):
    f = stage("orange", (255, 220, 120), 540, 980, 420); u = lt(t, "S17b")
    x0, y0, x1, y1 = 290, 640, 790, 1340
    cv2.rectangle(f, (x0 - 20, y0 - 20), (x1 + 20, y1 + 20), C(INK), -1, cv2.LINE_AA)
    g = stage("red", (255, 200, 90), 540, 980, 300)
    chub(g, 500, 1250, 0.9, la=(150, 175), ra=(150, 175), mouth="o", expr="wow", brow="up", look=(1, -1))
    mx, my = mouth_xy(490, 1250, 0.9); fire_cone(g, mx + 60, my - 10, -28, 330, 180, t)
    f[y0:y1, x0:x1] = g[y0:y1, x0:x1]
    comp(f, chip("SPICY FOOD EPISODE", INK, YEL_, 28), 540, y1 + 70, op=clamp((u - 0.2) / 0.3))
    comp(f, burst_el("SAME PRIZE!", YEL_, INK, 50), 820, 700, scale=pin(t, st_("S17b") + 0.4, 0.22))
    wui(f, "same prize as our", "[SPICY] video", t, st_("S17b") + 0.1, acc=YEL_, size=170)
    return finish(f, n)


# ---- S17c: chili rings the HEAT alarm, mint rings the COLD one — same trick ----
def shot_S17c(t, n):
    f = stage("cream"); u = lt(t, "S17c")
    tm = T("c5", "Mint") - 0.1
    def left(g):
        alarm(g, 330, 1080, 1.0, t, ring=1.0, key_in=True)
        rot_comp(g, scale_el(chili_el(face=True, mood="sly"), 0.42), 330, 1370, 8 * math.sin(t * 3), 1.0, 1.0, 0.3)
        flames_row(g, 330, 1500, 380, t, 90, 0.7)
    def right(g):
        calarm(g, 750, 1080, 1.0, t, ring=1.0, key_in=True)
        rot_comp(g, scale_el(mint_leaf_el(True, "sly"), 0.5), 750, 1370, -8 * math.sin(t * 3), 1.0, 1.0, 0.3)
        snow(g, t, 0.7, 18, 4, 640, 1490)
    split_contrast(f, t, st_("S17c") + 0.02, left, right, "CHILI: HEAT ALARM", "MINT: COLD ALARM", (255, 90, 40), (60, 150, 255), y0=620, y1=1500, t_r=tm)
    te = LINES["c5"]["end"] - 0.35
    if t >= te: slam(f, stamp_el("SAME TRICK!", INK, 60), 540, 1205, -5, t, te)
    ui_word(f, "chili and mint use the", "[SAME TRICK]", 470, t, st_("S17c") + 0.1, col=INK, acc=RED_, size=160)
    return finish(f, n)


# ---- S18: PART 4 — the nose trick (stuffy Chubby) ----
def shot_S18(t, n):
    f = stage("pink", (255, 236, 220), 540, 1000, 430); u = lt(t, "S18")
    chub_head_only(f, 540, 1030, 2.2, t, mouth=talk(t), expr="sad", brow="sad", look=(0, 0.3), nose=1.0)
    comp(f, chip("STUFFY NOSE", INK, WHITE, 32), 540, 1360, op=clamp((u - 0.3) / 0.3))
    chapter_card(f, t, st_("S18") + 0.02, 4, "THE NOSE TRICK", y=1440, dur=1.7, col=(120, 255, 190))
    wui(f, "now, the", "[NOSE] trick", t, st_("S18") + 0.1, acc=YEL_, size=190)
    return finish(f, n)


# ---- S19: two groups — menthol candy or plain candy ----
def shot_S19(t, n):
    f = stage("sky", (240, 250, 255), 540, 1000, 420); u = lt(t, "S19")
    tm = T("d2", "menthol") - 0.15; tp = T("d2", "plain") - 0.15
    for i, (x, tt, col, lab, who) in enumerate(((300, tm, (60, 210, 140), "MENTHOL CANDY", "chub"), (780, tp, (255, 110, 150), "PLAIN CANDY", "mom"))):
        kk = ramp(t, tt, 0.35)
        kw = dict(la=(20, 10), ra=(60, 40), mouth=0, expr="sad", brow="sad", nose=1.0, look=(0, -0.5))
        (chub if who == "chub" else mom)(f, x, 1470, 0.78, **kw)
        if t >= tt:
            comp(f, scale_el(candy_el(col), 0.7), x, 720 + 260 * eo(kk))
            comp(f, chip(lab, INK, WHITE, 26), x, 640, op=clamp((t - tt) / 0.25))
    wui(f, "a menthol candy... or a", "[PLAIN] one", t, st_("S19") + 0.1, acc=YEL_, size=150, y=470)
    return finish(f, n)


# ---- S20: within 10 minutes the menthol group felt clearer ----
def shot_S20(t, n):
    f = stage("yellow", (255, 250, 220), 540, 1000, 400); u = lt(t, "S20")
    tc = T("d3", "clearer.") - 0.2
    mm = int(10 * ramp(t, st_("S20") + 0.2, 1.2))
    comp(f, scale_el(clock_el(10, mm * 6 % 60), 1.0), 540, 800)
    comp(f, chip(f"+{mm} MIN", INK, WHITE, 30), 540, 990)
    ok = t >= tc
    chub(f, 300, 1470, 0.72, la=(150, 175) if ok else (20, 10), ra=(150, 175) if ok else (20, 10), mouth=2 if ok else 0, expr="happy" if ok else "sad", brow="up", nose=1.0 - 0.6 * ramp(t, tc, 0.3))
    mom(f, 780, 1470, 0.72, la=(20, 10), ra=(20, 10), mouth=0, expr="sad", brow="sad", nose=1.0)
    if ok:
        comp(f, think_el("CLEARER!", 36), 360, 1010, scale=pin(t, tc, 0.25))
        comp(f, chip("MENTHOL", INK, (120, 255, 190), 24), 300, 1480); comp(f, chip("PLAIN", INK, (255, 160, 190), 24), 780, 1480)
    ui_word(f, "within", "[10 MINUTES]", 470, t, st_("S20") + 0.1, col=INK, acc=RED_, size=180)
    comp(f, chip("Source: Eccles et al., J Pharm Pharmacol 1990", INK, WHITE, 22), 540, 1110, op=clamp((u - 0.6) / 0.3) * (1 - clamp((t - tc) / 0.2)))
    return finish(f, n)


# ---- S21: but the machine measured the airflow — no better ----
def shot_S21(t, n):
    f = stage("teal", (220, 250, 240), 540, 1000, 400); u = lt(t, "S21")
    tm = T("d4", "machine") - 0.15; tn = T("d4", "no") - 0.15
    v = 0.36 * ramp(t, tm + 0.2, 0.8)
    airmeter(f, 300, 1000, 1.05, v, "MENTHOL", t); airmeter(f, 780, 1000, 1.05, v, "PLAIN", t + 1)
    for x in (300, 780):
        for j in range(3):
            ph = (t * 1.2 + j / 3) % 1.0
            draw_arrow(f, x - 120 + 160 * ph, 1250, x - 60 + 160 * ph, 1250, 1.0, WHITE, 8, 22, op=0.8 * math.sin(math.pi * ph))
        comp(f, chip("AIRFLOW", INK, WHITE, 24), x, 1310)
    if t >= tn: slam(f, stamp_el("NO BETTER!", RED_, 60), 540, 760, -5, t, tn)
    wui(f, "a machine measured the", "[AIRFLOW]", t, st_("S21") + 0.1, acc=YEL_, size=180)
    return finish(f, n)


# ---- S21b: the cool feeling tells the brain... I can breathe! ----
def shot_S21b(t, n):
    f = stage("purple", (200, 230, 255), 540, 980, 400); u = lt(t, "S21b")
    tb = T("d5", "breathe!") - 0.2
    chub_head_only(f, 330, 1130, 1.9, t, mouth="o", expr="sad", brow="sad", look=(-0.6, 0), nose=0.8)
    calarm(f, 560, 1270, 0.5, t, ring=1.0)
    label_at(f, "NOSE COLD ALARM", 560, 1400, t, st_("S21b") + 0.3, bg=COLDB_D)
    for j in range(5):
        ph = (t * 0.9 + j / 5) % 1.0
        ov = f.copy(); cv2.circle(ov, (int(80 + 220 * ph), int(1170 + 8 * math.sin(j))), 13, C(ICY), -1, cv2.LINE_AA); a = math.sin(math.pi * ph); f[:] = f * (1 - a) + ov * a
    P = [(570, 1210), (620, 980), (720, 870)]
    pulse_path(f, P, t, st_("S21b") + 0.3, 0.6, (200, 245, 255), n=3, gap=0.3, wire=(120, 200, 255))
    comp(f, scale_el(brain_el(face=True, mood="shout" if t >= tb else "n"), 0.85), 760, 780)
    if t >= tb: comp(f, think_el("I CAN BREATHE!", 34), 760, 1060, scale=pin(t, tb, 0.25))
    comp(f, chip("REAL AIRFLOW: SAME", RED_, WHITE, 28), 330, 1462, op=clamp((u - 0.5) / 0.3))
    wui(f, "the cool feeling tells the", "[BRAIN]", t, st_("S21b") + 0.1, acc=ICY, size=170, out=tb - 0.05)
    return finish(f, n)


# ---- S22: takeaway — temperature same, feeling changed (stacked rows, not side panels) ----
def shot_S22(t, n):
    f = stage("cream", (255, 236, 210), 540, 1000, 380); u = lt(t, "S22")
    tt = T("e1", "temperature.") - 0.2; tf = T("e1", "feel.") - 0.2
    if t >= tt:
        k = pin(t, tt, 0.3)
        cv2.rectangle(f, (120, 640), (960, 980), C(WHITE), -1, cv2.LINE_AA); cv2.rectangle(f, (120, 640), (960, 980), C(INK), 6, cv2.LINE_AA)
        thermo_c(f, 260, 940, 0.74, 260, (255, 110, 70), labels=())
        comp(f, ed_el("TEMPERATURE", "SAME", "", big_col=INK, big_size=110, lead_size=40), 620, 810, scale=k)
        comp(f, check_el(36, True), 880, 700, scale=k)
    if t >= tf:
        k = pin(t, tf, 0.3)
        cv2.rectangle(f, (120, 1040), (960, 1380), C((210, 238, 255)), -1, cv2.LINE_AA); cv2.rectangle(f, (120, 1040), (960, 1380), C(INK), 6, cv2.LINE_AA)
        chub_head_only(f, 270, 1210, 0.95, t, mouth="o", expr="wow", brow="up")
        icicles(f, 270, 1300, 120, 1.0, 5, 0.6); snow(f, t, 0.6, 14, 6, 1050, 1370)
        comp(f, ed_el("FEELING", "COLD!", "", big_col=COLDB_D, big_size=110, lead_size=40), 620, 1210, scale=k)
    ui_word(f, "mint changes what you", "[FEEL]", 470, t, st_("S22") + 0.1, col=INK, acc=COLDB_D, size=200)
    return finish(f, n)


# ---- S23: visual recap 1-2-3-4 ----
def shot_S23(t, n):
    f = stage("mintg", (230, 255, 240), 540, 1000, 380); u = lt(t, "S23")
    items = [(scale_el(menthol_el("happy"), 0.58), "MENTHOL"), (scale_el(calarm_el(True, True), 0.95), "ALARM RINGS"),
             (scale_el(calarm_el(False, True), 0.95), "JUMPY ALARM"), (scale_el(chub_head_el(2, False, "up", 0, 0, "happy", 0.0, 0.5), 0.78), "NOSE FOOLED")]
    ts = [st_("S23") + 0.25, T("e2", "rings") - 0.15, T("e2", "jumpy,") - 0.15, T("e2", "nose.") - 0.15]
    recap_steps(f, items, 960, t, ts, 235, 0.95)
    if t >= ts[2]:
        x2 = 540 - 235 * 1.5 + 235 * 2
        for sg in (-1, 1): cv2.line(f, (int(x2 + sg * 70), 870), (int(x2 + sg * 92), 845), C(INK), 6, cv2.LINE_AA)
    wui(f, "so", "[REMEMBER]", t, st_("S23") + 0.05, acc=YEL_, size=190)
    return finish(f, n)


# ---- S24: send it + FreshNestHub sting ----
def shot_S24(t, n):
    f = stage("ice", (255, 255, 255), 540, 880, 420); u = lt(t, "S24")
    vend = LINES["e3"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e3", "Send") + 0.3
        comp(f, scale_el(phone2_el("gum then ice water?", "my teeth are FROZEN", pr), 0.82), 650, 950, scale=pin(t, st_("S24")))
        if pr and t < T("e3", "Send") + 0.75:
            rr = (t - T("e3", "Send") - 0.3) / 0.45
            cv2.circle(f, (650, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        dx, dy = shiver(t, 0.6)
        chub(f, 250 + dx, 1480, 0.8, la=(20, 10), ra=(148, -130), mouth="o", expr="wow", brow="up", look=(1, 0),
             hold=scale_el(ice_glass_el(0.6), 0.36), hold_off=(-30, -16), hold_front=True)
        hx, hy = head_pos(250 + dx, 1480, 0.8); icicles(f, hx, hy + 70, 130, 1.0, 5, 0.7)
        ui_word(f, "send to the friend who drinks", "[ICE WATER]", 420, t, T("e3", "friend") - 0.1, col=INK, acc=COLDB_D, size=170, tail="right after gum")
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INK, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1480, 0.7, la=(20, 10), ra=(148, -130), mouth=munch(t, 0.3)[0], expr="happy", brow="up", hold=scale_el(mint_leaf_el(False), 0.3), hold_off=(-20, -10), hold_front=True)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TF0, 0.5, 22), (T("i2", "whoa,") - 0.1, 0.4, 16), (T("i3", "nothing") + 0.0, 0.3, 12), (T("i3", "trick!") - 0.15, 0.35, 16),
           (T("a1", "menthol,") - 0.1, 0.25, 10), (T("a3", "cold") - 0.2, 0.25, 10), (T("a4", "twenty-five") - 0.1, 0.3, 12),
           (st_("S7c") + 0.05, 0.45, 20), (T("a6", "fits") - 0.05, 0.25, 10), (st_("S9") + 0.1, 0.45, 22), (T("a7", "COLD!") - 0.15, 0.5, 24),
           (T("a8", "didn't") + 0.0, 0.3, 14), (T("b2", "jumpy.") - 0.1, 0.3, 12), (T("b3", "screams!") - 0.15, 0.55, 26),
           (T("b4", "cool") - 0.1, 0.3, 12), (T("c1", "two") - 0.1, 0.3, 14), (T("c2", "without") - 0.15, 0.25, 10),
           (T("c3", "gone!") - 0.15, 0.3, 14), (T("c4", "Nobel") - 0.15, 0.35, 16), (LINES["c5"]["end"] - 0.35, 0.35, 16),
           (T("d4", "no") - 0.15, 0.4, 18), (T("d5", "breathe!") - 0.2, 0.3, 12), (T("e1", "feel.") - 0.2, 0.25, 10)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


def _bl(x, s_):
    if s_ < 0.5: return x
    sm = cv2.resize(x, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), s_ / 4), (W, H), interpolation=cv2.INTER_LINEAR)


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "focus" and dt < 0.34:
            p = dt / 0.34; prv = rs(SHOTS[i - 1]["id"], t, n); m = eio(p)
            f = _bl(prv, 40 * m) * (1 - m) + _bl(f, 40 * (1 - m)) * m
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "zoom" and dt < 0.2:
            p = 1 - dt / 0.2; acc = np.zeros_like(f)
            for q in range(5): acc += cam(f, 1 + 0.06 * q * p)
            f = acc / 5
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
