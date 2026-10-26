# ================= shots: FreshNestHub — "The man who survived 46 G" (John Paul Stapp, 10 Dec 1954) =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "On") - 0.15, "punch"), ("S1", T("a1", "Meet") - 0.2, "whip"),
    ("S1b", T("a1", "who") - 0.12, "zoom"), ("S2", T("a2", "Back") - 0.2, "flash"), ("S2b", T("a3", "Stapp") - 0.2, "whip"),
    ("S2c", T("a3", "So") - 0.12, "punch"), ("S3a", T("b1", "Nineteen") - 0.2, "whip"), ("S3b", T("b1", "Nine") - 0.15, "zoom"),
    ("S4", T("b2", "In") - 0.2, "flash"), ("S5", T("b3", "Then") - 0.15, "whip"), ("S6", T("c1", "That's") - 0.15, "punch"),
    ("S7", T("c2", "For") - 0.2, "focus"), ("S8", T("c3", "Tiny") - 0.2, "zoom"), ("S9", T("c4", "He") - 0.2, "whip"),
    ("S10", T("d1", "But") - 0.2, "focus"), ("S11a", T("e1", "So") - 0.2, "whip"), ("S11b", T("e1", "Then") - 0.12, "punch"),
    ("S12", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_RUN = "Sources: Smithsonian Air & Space · NM Museum of Space History · U.S. Air Force"
SRC_EYE = "Source: NM Museum of Space History · Airman magazine (USAF)"


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


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


def scroll_stop(t, t_go, ts, v, dec):
    if t < t_go: return 0.0
    if t < ts: return v * (t - t_go)
    u = min(t - ts, dec); return v * (ts - t_go) + v * (u - u * u / (2 * dec))


def speed_at(t, t_go, ts, v, dec):
    if t < t_go: return 0.0
    if t < ts: return v
    return v * max(0.0, 1 - (t - ts) / dec)


def ring(f, x, y, r, col, th=8, op=1.0):
    ov = f.copy(); cv2.circle(ov, (int(x), int(y)), int(r), C(col), th, cv2.LINE_AA); f[:] = f * (1 - op) + ov * op


def dummy(f, x, y, s, t, op=1.0):
    guy(f, x, y, s, la=(16, 6), ra=(16, 6), mouth=0, expr="n", brow="n", blink=True, op=op)
    hy = y - (178 + 168 + 76) * s
    for k in range(4):
        cv2.ellipse(f, (int(x), int(hy - 52 * s)), (int(22 * s), int(22 * s)), 0, k * 90, k * 90 + 90, C(YEL_ if k % 2 else INK), -1, cv2.LINE_AA)


# ---- S0: hook — rocket sled screams across the desert, then slams to a stop ----
TS0 = T("i1", "stopped") - 0.12


def shot_S0(t, n):
    f = stage("orange", (255, 214, 120), 540, 900, 430)
    off = scroll_stop(t, 0.2, TS0, 2600, 0.45); sp = speed_at(t, 0.2, TS0, 2600, 0.45)
    desert(f, t, scroll=off + 1.0, track_y=1300, water_from=(860 if t >= TS0 - 0.25 else None))
    speed_lines(f, t, clamp(sp / 2600), 640, 1250, 18, 1)
    x = -500 + 1090 * eo(clamp(t / 0.45))
    lurch = 36 * math.sin(math.pi * clamp((t - TS0) / 0.35)) if t >= TS0 else 0.0
    fire = (1.0 if t < TS0 else clamp(1 - (t - TS0) / 0.12)) * clamp(t / 0.2)
    stop = t >= TS0
    sled(f, x + lurch, 1176 + (6 * math.sin(t * 60) if not stop else 0), 0.95, t, fire, "wow" if stop else "n",
         mouth=("o" if stop else 0), brow="up" if stop else "sus", look=(1, 0))
    if stop: splash(f, x + lurch + 380 * 0.95, 1310, t, TS0, 1.0, 80, 4, 1.8)
    tsw = T("i1", "seconds?") - 0.3
    if t >= tsw: rot_comp(f, scale_el(stopwatch_el("1.4"), 0.62), 800, 830, 8, pin(t, tsw, 0.25), 1.0, 0.35)
    ui_word(f, "a man once hit", "632 MPH", 470, t, T("i1", "six") - 0.15, col=WHITE, size=200, shadow=0.45, lead_col=WHITE, out=TS0 - 0.05)
    ui_word(f, "then stopped in", "1.4 SECONDS", 470, t, TS0, col=YEL_, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S0b: on purpose! — and here's what it did to his body ----
def shot_S0b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S0b")
    tb = T("i2", "And") - 0.1
    rays(f, 540, 1060, 700, (255, 255, 255), 0.3, t)
    if t < tb:
        guy(f, 540, 1490, 1.05, la=(18, 8), ra=(150, 175), mouth=talk(t), blink=blink_at(t, 1), brow="up", expr="smirk", hat=helmet_el())
        slam(f, stamp_el("ON PURPOSE!", RED_, 70), 540, 1300, -8, t, T("i2", "purpose!") - 0.15)
    else:
        guy(f, 540, 1490, 1.05, la=(18, 8), ra=(18, 8), mouth=0, blink=False, brow="n", expr="n", hat=helmet_el())
        ms = [(540, 1047), (540, 1250), (498, 1329)]
        for i, (mx, my) in enumerate(ms):
            q = t - tb - 0.18 * i
            if q > 0:
                ring(f, mx, my, 70 + 14 * math.sin(q * 9), RED2, 9, clamp(q / 0.2))
                comp(f, chip("?", RED2, WHITE, 40), mx + 92, my - 60, scale=pin(t, tb + 0.18 * i, 0.25))
        sx = 540 + 260 * math.sin(clamp((t - tb) / 1.3) * math.pi - math.pi / 2)
        comp(f, scale_el(magnifier_el(), 0.6), sx, 1080 + 20 * math.cos(t * 3))
    ui_word(f, "he did it", "ON PURPOSE", 470, t, SHOT["S0b"]["start"] + 0.05, col=INK, size=190, out=tb - 0.05)
    ui_word(f, "here's what it did to his", "BODY", 470, t, tb, col=RED_, size=230)
    return finish(f, n)


# ---- S1: meet John Paul Stapp, Air Force doctor ----
def shot_S1(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 430); u = lt(t, "S1")
    rot_comp(f, scale_el(dossier_el(), 1.16), 540, 1020 + 6 * math.sin(t * 2), -3, pin(t, SHOT["S1"]["start"] + 0.05, 0.35), 1.0, 0.3)
    ta = T("a1", "Air") - 0.15
    if t >= ta: comp(f, chip("nicknamed “the fastest man on Earth”", INK, WHITE, 30), 540, 1400, scale=pin(t, ta + 0.2, 0.25))
    ui_word(f, "meet", "JOHN PAUL STAPP", 470, t, SHOT["S1"]["start"] + 0.1, col=INK, size=140, out=ta - 0.05)
    ui_word(f, "an air force", "DOCTOR", 470, t, ta, col=NAVY2, size=210)
    return finish(cam(f, 1.03 - 0.03 * eo(clamp(u / 1.5)), W / 2, 1000), n)


# ---- S1b: who tested crashes... on himself ----
def shot_S1b(t, n):
    f = stage("red", YEL_, 540, 1000, 430); u = lt(t, "S1b")
    th = T("a1", "himself!") - 0.2
    dummy(f, 300, 1450, 0.85, t, 1.0)
    if t >= th:
        k = clamp((t - th) / 0.2); ov = f.copy()
        cv2.line(ov, (180, 900), (420, 1440), C(INK), 26, cv2.LINE_AA); cv2.line(ov, (420, 900), (180, 1440), C(INK), 26, cv2.LINE_AA)
        f[:] = f * (1 - k) + ov * k
    comp(f, chip("CRASH DUMMY", INK, WHITE, 28), 300, 1480)
    guy(f, 760, 1450, 0.95, la=(18, 8), ra=(70, 150) if t >= th else (30, 20), mouth=talk(t), blink=blink_at(t, 3), brow="up",
        expr="smirk" if talk(t) == 0 else "n", hat=helmet_el(), look=(-1, 0))
    if t >= th: slam(f, stamp_el("TEST SUBJECT: ME", WHITE, 50), 760, 760, 6, t, th + 0.05)
    ui_word(f, "who tested crashes", "ON HIMSELF", 470, t, SHOT["S1b"]["start"] + 0.1, col=WHITE, size=180, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S2: scientists thought 18 G would kill you ----
def shot_S2(t, n):
    f = stage("purple", (0, 200, 255), 540, 1000, 430); u = lt(t, "S2")
    tg = T("a2", "times") - 0.2; tk = T("a2", "kill") - 0.15
    wy = 700 + 70 * eo(clamp((t - tg) / 0.5)) + (50 * eback(clamp((t - tk) / 0.25)) if t >= tk else 0)
    scared = t >= tg
    guy(f, 540, 1490, 1.0, la=(150, 170) if scared else (18, 8), ra=(150, 170) if scared else (18, 8), mouth=talk(t),
        blink=False if scared else blink_at(t, 1), brow="sad" if scared else "n", expr="wow" if scared and talk(t) == 0 else "n", look=(0, -1))
    if t >= T("a2", "eighteen") - 0.15:
        rot_comp(f, scale_el(weight_el("x18"), 0.72), 540, wy, 4 * math.sin(t * 3), pin(t, T("a2", "eighteen") - 0.15, 0.3), 1.0, 0.4)
    if t >= tg: comp(f, chip("1 G = your normal weight", INK, WHITE, 30), 790, 1100, scale=pin(t, tg + 0.1, 0.25))
    if t >= tk: slam(f, stamp_el("DEADLY?", RED_, 64), 800, 1250, -10, t, tk + 0.05)
    ui_word(f, "some scientists thought", "18 G", 470, t, SHOT["S2"]["start"] + 0.15, col=WHITE, size=220, shadow=0.45, lead_col=WHITE,
            tail="18 × gravity", out=tk - 0.05)
    ui_word(f, "would", "KILL YOU", 470, t, tk, col=YEL_, size=200, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2b: Stapp thought they were wrong ----
def shot_S2b(t, n):
    f = stage("teal", (255, 214, 120), 540, 1000, 430); u = lt(t, "S2b")
    tw = T("a3", "wrong.") - 0.2
    comp(f, sign_el("18 G LIMIT", YEL_, INK, 70), 330, 1260, scale=pin(t, SHOT["S2b"]["start"] + 0.03, 0.3))
    guy(f, 790, 1480, 0.95, la=(40, 120), ra=(40, 120), mouth=talk(t), blink=blink_at(t, 2), brow="sus", expr="sus" if talk(t) == 0 else "n",
        hat=helmet_el(), look=(-1, 0), bob=6 * math.sin(t * 14) if t >= tw else 0)
    if t >= tw: slam(f, stamp_el("WRONG", RED_, 90), 330, 1110, -12, t, tw)
    ui_word(f, "stapp thought they were", "WRONG", 470, t, SHOT["S2b"]["start"] + 0.1, col=WHITE, size=220, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2c: so he strapped himself to a rocket sled ----
def shot_S2c(t, n):
    f = stage("pink", (255, 230, 120), 540, 1000, 430); u = lt(t, "S2c")
    ts = T("a3", "strapped") - 0.1; tr = T("a3", "rocket") - 0.2
    gy = 1290
    f[gy:H] = f[gy:H] * 0.6 + np.array(C((150, 40, 100)), np.float32) * 0.4
    cv2.line(f, (0, gy - 2), (W, gy - 2), C((90, 96, 110)), 12, cv2.LINE_AA)
    z = 1.25 - 0.18 * eo(clamp(u / 0.8))
    sled(f, 520, 1140, z, t, 0.0, "smirk" if t < tr else "n", mouth=talk(t), brow="up", look=(1, 0), straps=clamp((t - ts) / 0.35))
    if t >= tr: rot_comp(f, tag_el("ROCKET SLED", YEL_, INK, 64), 520, 1430, -4, pin(t, tr, 0.25), 1.0, 0.35)
    ui_word(f, "so he strapped himself to a", "ROCKET SLED", 470, t, SHOT["S2c"]["start"] + 0.12, col=INK, size=170)
    return finish(f, n)


# ---- S3a: 1954, New Mexico ----
def shot_S3a(t, n):
    f = stage("cream", (255, 170, 80), 540, 980, 430); u = lt(t, "S3a")
    tn = T("b1", "New") - 0.15
    comp(f, scale_el(mesa_el(5, (230, 140, 90)), 1.2), 540, 1290, op=0.9)
    rot_comp(f, scale_el(calendar_el("DEC 10", "1954"), 0.85), 360 if t >= tn else 540, 1020, -4, pin(t, SHOT["S3a"]["start"] + 0.05, 0.3), 1.0, 0.35)
    if t >= tn:
        comp(f, sign_el("NEW MEXICO", NAVY2, WHITE, 54), 780, 1200, scale=pin(t, tn, 0.3))
    comp(f, scale_el(cactus_el(), 0.6), 160, 1360); comp(f, scale_el(cactus_el(), 0.45), 930, 1400)
    ui_word(f, "december 10", "1954", 470, t, SHOT["S3a"]["start"] + 0.1, col=INK, size=220, out=tn - 0.05)
    ui_word(f, "holloman air force base", "NEW MEXICO", 470, t, tn, col=RED_, size=170)
    return finish(f, n)


# ---- S3b: nine rockets — fire! ----
def shot_S3b(t, n):
    f = stage("purple", (255, 120, 40), 540, 1040, 430); u = lt(t, "S3b")
    t9 = T("b1", "Nine") - 0.05; tf = T("b1", "fire!") - 0.15
    lit = 0 if t < t9 else min(9, 1 + int((t - t9) / 0.065))
    fire = t >= tf
    if fire:
        rays(f, 540, 1050, 760, (255, 200, 90), 0.7 * clamp((t - tf) / 0.15), t)
        glow(f, 540, 1050, 420, (255, 150, 40), 0.5)
    sc_ = 1.25 + (0.05 * math.sin(t * 50) if fire else 0)
    comp(f, scale_el(sled_rear_el(lit), sc_), 540, 1050, scale=pin(t, SHOT["S3b"]["start"] + 0.02, 0.3))
    if fire:
        for i in range(9):
            r_, c_ = divmod(i, 3); cx, cy = 540 + (c_ - 1) * 147 * sc_, 1050 + ((r_ - 1) * 136 + 2) * sc_
            glow(f, cx, cy, 70 + 10 * math.sin(t * 40 + i), (255, 230, 150), 0.35)
    if lit and not fire: comp(f, readout_el(str(lit), YEL_, INK, 70), 540, 1470)
    ui_word(f, "nine", "ROCKETS", 470, t, t9, col=WHITE, size=210, shadow=0.45, lead_col=WHITE, out=tf - 0.05)
    ui_word(f, "", "FIRE!", 470, t, tf, col=YEL_, size=260, shadow=0.5)
    return finish(f, n)


# ---- S4: 5 seconds -> 632 mph ----
def shot_S4(t, n):
    f = stage("orange", (255, 214, 120), 540, 820, 380); u = lt(t, "S4")
    t0 = SHOT["S4"]["start"] + 0.15; t1 = T("b2", "six") + 0.25
    k = clamp((t - t0) / (t1 - t0)); v = 632 * (k ** 1.6)
    off = 300 * u + 2600 * max(0.0, u - 0.3) * clamp(k + 0.3)
    desert(f, t, scroll=off, track_y=1350)
    speed_lines(f, t, clamp(k * 1.2), 1100, 1340, 12, 2)
    sled(f, 540, 1262, 0.66, t, 0.6 + 0.4 * k, "wow" if k > 0.6 else "n", mouth="o" if k > 0.6 else 0, brow="up", look=(1, 0))
    dial(f, 540, 880, 0.82, "mph", v, f"{int(round(v))} MPH", shake=clamp(k * 2 - 1), t=t)
    if t >= t1: rot_comp(f, tag_el("LAND SPEED RECORD", YEL_, INK, 50), 560, 1120, -4, pin(t, t1 + 0.1, 0.25), 1.0, 0.35)
    if t >= t1 + 0.3: comp(f, chip("≈ 1,017 km/h", INK, WHITE, 30), 540, 1462, op=clamp((t - t1 - 0.3) / 0.3))
    ui_word(f, "in just", "5 SECONDS", 470, t, SHOT["S4"]["start"] + 0.1, col=WHITE, size=200, shadow=0.45, lead_col=WHITE, out=T("b2", "six") - 0.2)
    ui_word(f, "he hits", "632 MPH", 470, t, T("b2", "six") - 0.15, col=YEL_, size=210, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S5: water brakes — stopped in 1.4 seconds ----
TS5 = T("b3", "stop") - 0.1


def shot_S5(t, n):
    f = stage("teal", (120, 220, 255), 540, 860, 400); u = lt(t, "S5")
    off = scroll_stop(t, SHOT["S5"]["start"], TS5, 2600, 0.9); sp = speed_at(t, SHOT["S5"]["start"], TS5, 2600, 0.9)
    desert(f, t, scroll=off + 400, track_y=1330, water_from=max(-10.0, 980 - 2600 * max(0.0, TS5 - t)) if t > TS5 - 0.6 else None)
    speed_lines(f, t, clamp(sp / 2600), 1000, 1300, 12, 3)
    stop = t >= TS5
    lurch = 50 * math.sin(math.pi * clamp((t - TS5) / 0.5)) if stop else 0
    sled(f, 470 + lurch, 1190, 1.0, t, 0.0, "wow" if stop else "n", mouth="o" if stop else 0, brow="up" if stop else "n", look=(1, 0))
    if stop:
        splash(f, 470 + lurch + 360, 1330, t, TS5, 1.15, 90, 7, 2.2)
        q = clamp((t - TS5) / max(0.2, T("b3", "seconds.") - TS5)); val = f"{1.4 * q:.1f}"
        rot_comp(f, scale_el(stopwatch_el(val, RED2 if q >= 1 else INK), 0.7), 540, 820, -4, pin(t, TS5, 0.25), 1.0, 0.35)
    comp(f, chip(SRC_RUN, INK, WHITE, 21), 540, 1462, op=clamp((u - 1.4) / 0.3))
    ui_word(f, "then water brakes", "STOP HIM", 470, t, SHOT["S5"]["start"] + 0.12, col=WHITE, size=200, shadow=0.45, lead_col=WHITE, out=T("b3", "in") - 0.05)
    ui_word(f, "in just", "1.4 SECONDS", 470, t, T("b3", "in") - 0.05, col=YEL_, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S6: that's 46.2 G ----
def shot_S6(t, n):
    f = stage("purple", (255, 60, 80), 540, 1010, 430); u = lt(t, "S6")
    tg = T("c1", "forty-six") - 0.12
    k = clamp((t - tg) / 0.35); v = 46.2 * (eback(k) if k < 1 else 1.0)
    if t >= tg: rays(f, 540, 1010, 760, (255, 120, 120), 0.45 * clamp((t - tg) / 0.2), t)
    dial(f, 540, 1010, 1.1, "g", min(50, v), f"{min(v, 46.2):.1f} G" if t >= tg else "0 G", shake=1.0 if k >= 1 else 0.0, mark=18, t=t)
    a = _ang(18, 50); comp(f, chip("“LIMIT”: 18 G", YEL_, INK, 30), 540 + 330 * math.cos(a) - 30, 1010 - 330 * math.sin(a) - 10, scale=pin(t, SHOT["S6"]["start"] + 0.1, 0.25))
    ui_word(f, "that's", "46.2 G", 470, t, tg, col=YEL_, size=250, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S7: his body weighed 6,800 lb ----
def shot_S7(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S7")
    tw = T("c2", "weighed") - 0.1; tt = T("c2", "thousand") + 0.2
    k = clamp((t - tw) / (tt - tw)); lb = 170 + (6800 - 170) * (k ** 2.2)
    sq = k >= 1
    jit = (4 * math.sin(t * 70)) if sq else 0
    comp(f, bscale_el(clamp((t - tt) / 0.3)), 540 + jit, 1420)
    guy(f, 540 + jit, 1345, 1.0, la=(60, 150) if sq else (18, 8), ra=(60, 150) if sq else (18, 8), ll=14 if sq else 7, rl=14 if sq else 7,
        mouth=talk(t) if not sq else "o", blink=False, brow="up" if sq else "n", expr="wow" if sq else "n", hat=helmet_el(), shadow=False)
    comp(f, readout_el(f"{int(round(lb / 10) * 10):,} LB", (255, 70, 70), (30, 34, 40), 30), 540 + jit, 1420 - 25)
    if sq:
        for i in range(3):
            q = (t - tt) * 1.5 + i * 0.33; yy = 900 + 120 * (q % 1.0)
            cv2.circle(f, (int(420 + i * 120), int(yy)), 10, C((120, 200, 255)), -1, cv2.LINE_AA)
        comp(f, chip("≈ 3,000 kg", INK, WHITE, 32), 830, 1180, scale=pin(t, tt + 0.1, 0.25))
    ui_word(f, "for a split second", "HE WEIGHED", 470, t, SHOT["S7"]["start"] + 0.12, col=INK, size=180, out=T("c2", "six") - 0.15)
    ui_word(f, "his body weighed", "6,800 LB", 470, t, T("c2", "six") - 0.15, col=RED_, size=220)
    return finish(f, n)


# ---- S8: blood vessels in his eyes burst — he couldn't see ----
def shot_S8(t, n):
    f = stage("pink", (255, 236, 160), 540, 1000, 430); u = lt(t, "S8")
    tb = T("c3", "burst.") - 0.25; tf = T("c3", "filled") - 0.1; tc = T("c3", "couldn't") - 0.1
    vess = clamp((t - (SHOT["S8"]["start"] + 0.4)) / max(0.3, tb + 0.15 - SHOT["S8"]["start"] - 0.4))
    blood = clamp((t - tf) / 0.6)
    pup = 1.0 + 0.25 * clamp((t - tc) / 0.4)
    comp(f, eye_el(vess, blood, pup), 540, 1030 + (5 * math.sin(t * 60) if tb <= t < tb + 0.3 else 0), scale=1.05)
    if t >= tb: comp(f, chip("blood vessels burst", RED2, WHITE, 30), 540, 1380, scale=pin(t, tb, 0.2))
    if t >= tc:
        d_ = clamp((t - tc) / 0.45)
        f = f * (1 - 0.82 * d_)
    if t < tc: comp(f, chip(SRC_EYE, INK, WHITE, 21), 540, 1462, op=clamp((u - 0.8) / 0.3))
    ui_word(f, "tiny blood vessels in his eyes", "BURST", 470, t, tb, col=RED_, size=230, out=tf - 0.05)
    ui_word(f, "his eyes filled with", "BLOOD", 470, t, tf, col=RED_, size=230, out=tc - 0.05)
    if t < tb: ui_word(f, "tiny blood vessels in his", "EYES", 470, t, SHOT["S8"]["start"] + 0.12, col=INK, size=230, out=tb - 0.05)
    ui_word(f, "and he couldn't", "SEE", 470, t, tc, col=WHITE, size=250, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S9: like getting a tooth pulled... with no anesthetic ----
def shot_S9(t, n):
    f = stage("teal", (255, 214, 120), 540, 1000, 430); u = lt(t, "S9")
    tt = T("c4", "tooth") - 0.15; tp = T("c4", "pulled...") - 0.05; tn = T("c4", "no") - 0.15
    yank = eo(clamp((t - tp) / 0.25)) if t >= tp else 0.0
    comp(f, gum_el(), 470, 1330, scale=0.95)
    tx, ty = 470, 1180 - 150 * yank; rot = -14 * yank
    drop = 1 - eo(clamp((t - SHOT["S9"]["start"] - 0.1) / 0.5))
    rot_comp(f, molar_el(), tx, ty, rot, 0.95)
    rot_comp(f, forceps_el(0.0 if t >= tt else 0.75), tx + 6, ty - 175 - 300 * drop, rot, 0.8)
    if t >= tp: comp(f, burst_el("YANK!", YEL_, INK, 56), 270, 860, scale=pin(t, tp, 0.25))
    guy(f, 830, 1470, 0.72, la=(18, 8), ra=(150, 160), mouth=talk(t) if t < tp else 3, blink=t >= tp, brow="sad", expr="sad", hat=helmet_el(), look=(-1, 0))
    if t >= tn: slam(f, stamp_el("NO ANESTHETIC", RED_, 54), 470, 1330, -6, t, tn)
    comp(f, chip("his words: “like the extraction of a molar without anesthetic”", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.4) / 0.3))
    ui_word(f, "it felt like getting a", "TOOTH PULLED", 470, t, SHOT["S9"]["start"] + 0.12, col=WHITE, size=170, shadow=0.45, lead_col=WHITE, out=tn - 0.05)
    ui_word(f, "with", "NO ANESTHETIC", 470, t, tn, col=YEL_, size=150, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S10: the next day, his sight came back ----
def shot_S10(t, n):
    f = stage("sky", (255, 255, 200), 540, 1000, 430); u = lt(t, "S10")
    ts = T("d1", "sight") - 0.1
    k = clamp((t - SHOT["S10"]["start"]) / max(0.4, ts + 0.3 - SHOT["S10"]["start"]))
    rays(f, 540, 1000, 760, (255, 255, 230), 0.45 * k, t)
    comp(f, eye_el(0.35, 0.0, 1.0), 540, 1030, scale=1.0)
    if k < 1: f = _bl(f, 30 * (1 - k)) * (0.25 + 0.75 * k)
    if t >= ts + 0.2:
        for i, (gx, gy) in enumerate(((780, 860), (330, 880), (820, 1180))):
            q = (t - ts - 0.2 - 0.12 * i)
            if q > 0: comp(f, burst_el("", (255, 255, 255), INK, 20, 4), gx, gy, scale=0.5 + 0.2 * math.sin(q * 8))
        comp(f, chip("but his eyesight was never quite the same", INK, WHITE, 28), 540, 1420, scale=pin(t, ts + 0.4, 0.25))
    ui_word(f, "the next day", "HE COULD SEE", 470, t, SHOT["S10"]["start"] + 0.12, col=GRN_, size=180)
    return finish(f, n)


# ---- S11a: so much for 18 G — they thought vs he survived ----
def shot_S11a(t, n):
    f = stage("emerald", GOLD, 540, 1000, 430); u = lt(t, "S11a")
    base = 1420; k = eo(clamp((u - 0.05) / 0.6))
    cv2.line(f, (160, base), (920, base), C(INK), 8, cv2.LINE_AA)
    bars2(f, base, [(330, 18 * 13, (150, 156, 176), "THEY THOUGHT: 18 G"), (750, 46.2 * 13, RED2, "HE TOOK: 46.2 G")], k, t)
    tb = T("e1", "G.") - 0.25
    if t >= tb: slam(f, stamp_el("MYTH", WHITE, 80), 330, 1260, -10, t, tb)
    ui_word(f, "so much for", "18 G", 470, t, SHOT["S11a"]["start"] + 0.1, col=WHITE, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S11b: then he pushed for seat belts in everyday cars ----
def shot_S11b(t, n):
    f = stage("red", (255, 214, 120), 540, 1000, 430); u = lt(t, "S11b")
    ts = T("e1", "seat") - 0.35; tb = T("e1", "belts") - 0.05
    k = clamp((t - ts) / max(0.2, tb - ts)); clicked = t >= tb
    comp(f, seat_el(), 540, 1100)
    guy(f, 540, 1210, 1.0, sit=True, la=(40, 40), ra=(40, 40), mouth=talk(t), blink=blink_at(t, 4), brow="up", expr="smirk" if clicked else "n")
    belt_draw(f, 540, 1210, 1.0, k, clicked)
    comp(f, wheel_el(), 540, 1420)
    if clicked: comp(f, burst_el("CLICK!", YEL_, INK, 50), 820, 1000, scale=pin(t, tb, 0.25))
    comp(f, chip("he attended the 1966 U.S. Highway Safety Act signing", INK, WHITE, 24), 540, 1462, op=clamp((u - 0.8) / 0.3))
    ui_word(f, "then he pushed for", "SEAT BELTS", 470, t, SHOT["S11b"]["start"] + 0.1, col=WHITE, size=200, shadow=0.45, lead_col=WHITE, tail="in everyday cars")
    return finish(f, n)


# ---- S12: send it + FreshNestHub sting ----
def shot_S12(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S12")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("bro... seat belt??", "ok ok buckling up", pr), 0.82), 600, 950, scale=pin(t, SHOT["S12"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up")
        ui_word(f, "send to the friend who never", "BUCKLES UP", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=150, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.0)
        comp(f, ed_el("follow for more body secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "six") - 0.1, 0.25, 10), (TS0, 0.5, 22), (T("i2", "purpose!") - 0.15, 0.25, 10), (T("i2", "And") - 0.1, 0.2, 8),
           (T("a1", "himself!") - 0.15, 0.3, 12), (T("a2", "kill") - 0.1, 0.35, 16), (T("a3", "wrong.") - 0.15, 0.3, 14),
           (T("a3", "rocket") - 0.2, 0.25, 10), (T("b1", "fire!") - 0.15, 0.6, 22), (T("b2", "six") - 0.1, 0.3, 14),
           (TS5, 0.6, 22), (T("c1", "forty-six") - 0.1, 0.5, 20), (T("c2", "thousand") + 0.2, 0.4, 16),
           (T("c3", "burst.") - 0.2, 0.3, 14), (T("c4", "pulled...") - 0.05, 0.3, 14), (T("c4", "no") - 0.1, 0.25, 10),
           (T("e1", "G.") - 0.2, 0.3, 12), (T("e1", "belts") - 0.05, 0.25, 10)]


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
