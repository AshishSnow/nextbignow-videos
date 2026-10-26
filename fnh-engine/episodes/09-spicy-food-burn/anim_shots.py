# ================= shots: FreshNestHub 09 — "Spicy food doesn't burn you — it tricks your brain" =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Your") - 0.15, "punch"), ("S1b", T("i2", "But") - 0.15, "focus"),
    ("S2", T("a1", "The") - 0.2, "whip"), ("S2b", T("a1", "called") - 0.2, "zoom"),
    ("S3", T("a2", "Your") - 0.2, "whip"), ("S3b", T("a2", "Think") - 0.2, "zoom"),
    ("S4", T("a3", "And") - 0.2, "zoom"), ("S5", T("a4", "Normally,") - 0.2, "whip"), ("S5b", T("a4", "like") - 0.15, "punch"),
    ("S6", T("a5", "But") - 0.2, "whip"), ("S6b", T("a5", "Like") - 0.15, "flash"),
    ("S7", T("a6", "Click!") - 0.15, "punch"), ("S7b", T("a6", "your") - 0.1, "zoom"),
    ("S8", T("a7", "Your") - 0.2, "whip"), ("S8b", T("a7", "So") - 0.1, "focus"),
    ("S9", T("b1", "Finding") - 0.2, "zoom"), ("S9b", T("b1", "it") - 0.15, "flash"),
    ("S10", T("c1", "So") - 0.2, "whip"), ("S11", T("c2", "Scientists") - 0.2, "whip"), ("S11b", T("c2", "seventy-two") - 0.15, "punch"),
    ("S12", T("c3", "Water") - 0.2, "whip"), ("S12b", T("c3", "And") - 0.15, "flash"),
    ("S13", T("c4", "Even") - 0.2, "whip"), ("S13b", T("c4", "Scientists") - 0.2, "zoom"),
    ("S14", T("d1", "Now") - 0.2, "focus"), ("S14b", T("d1", "Birds") - 0.15, "punch"),
    ("S15", T("d2", "They") - 0.2, "whip"), ("S15b", T("d2", "then") - 0.15, "whip"),
    ("S16", T("d3", "But") - 0.2, "zoom"), ("S16b", T("d3", "So") - 0.1, "punch"),
    ("S17", T("d4", "Scientists") - 0.2, "whip"), ("S17b", T("d4", "To") - 0.15, "punch"),
    ("S18", T("e1", "So") - 0.2, "focus"), ("S19", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
HOT = (255, 120, 40); MINT = (150, 255, 200); SKYB = (120, 210, 255)


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


def ring(f, x, y, r, col, th=8, op=1.0):
    ov = f.copy(); cv2.circle(ov, (int(x), int(y)), int(r), C(col), th, cv2.LINE_AA); f[:] = f * (1 - op) + ov * op


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / d))


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def st_(sid): return SHOT[sid]["start"]


def mouth_xy(x, y, s): return x, y - 372 * s


# ---------- shared diagram pieces ----------
def surface(f, y0, y1, t, x0=0, x1=W):
    """tongue cross-section: pink tissue from y0 down to y1 with bumpy papillae on top."""
    g = np.linspace(0, 1, int(y1 - y0))[:, None, None]
    f[int(y0):int(y1), x0:x1] = np.array(C((255, 150, 166)), np.float32) * (1 - g) + np.array(C(TONG_D), np.float32) * g
    for i in range(int((x1 - x0) / 60) + 2):
        px = x0 + i * 60
        cv2.ellipse(f, (int(px), int(y0 + 2)), (30, 26), 0, 180, 360, C((255, 170, 186)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(px), int(y0 + 2)), (30, 26), 0, 180, 360, C(TONG_D), 4, cv2.LINE_AA)


def wire(f, pts, col=NERVE, th=16, lit=0.0):
    P = np.asarray(pts, np.int32)
    cv2.polylines(f, [P], False, C(INK), th + 10, cv2.LINE_AA)
    c = tuple(int(a + (255 - a) * lit) for a in col)
    cv2.polylines(f, [P], False, C(c), th, cv2.LINE_AA)


def nerve_xsec(f, t, alarms=False, ring_k=0.0, keys=False, y_s=760, xs=(220, 540, 860), bot=1500, s=0.6):
    surface(f, y_s, y_s + 260, t)
    for i, x in enumerate(xs):
        pts = [(x + 30 * math.sin(i), bot), (x - 20, y_s + 420), (x, y_s + 150)]
        wire(f, pts, lit=ring_k * 0.6)
        if alarms: alarm(f, x, y_s + 110, s, t + i, ring=ring_k, key_in=keys)
        else:
            cv2.circle(f, (int(x), int(y_s + 140)), 26, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y_s + 140)), 18, C(NERVE), -1, cv2.LINE_AA)


# ---- S0: hook — Chubby munches a chili... and breathes FIRE ----
TF0 = T("i1", "food...") - 0.1


def shot_S0(t, n):
    f = stage("orange", (255, 220, 120), 540, 960, 430)
    for i, (px, py, r) in enumerate(((180, 1470, -30), (900, 1480, 30), (300, 1520, 70))):
        rot_comp(f, scale_el(chili_el(), 0.34), px, py, r + 8 * math.sin(t * 2 + i), 1.0, 1.0, 0.25)
    if t < TF0:
        m, c = munch(t, 0.32)
        chub(f, 470, 1460, 1.12, la=(20, 10), ra=(148, -130), mouth=m, brow="up", expr="happy", hold=chili_side(0.42, c % 2 == 1),
             hold_off=(-30, -10), hold_front=True, bob=4 * math.sin(t * 18))
    else:
        k = ramp(t, TF0, 0.18); q = t - TF0
        rays(f, 700, 900, 760, (255, 230, 120), 0.5 * k, t)
        sh = 8 * math.sin(t * 50) * math.exp(-q * 2)
        chub(f, 400 + sh, 1460, 1.12, la=(150, 175), ra=(150, 175), mouth="o", brow="up", expr="wow", look=(1, -1), lean=-6 * k, squash=-0.4 * k)
        mx, my = mouth_xy(400 + sh - 10, 1460, 1.12)
        fire_cone(f, mx + 70, my - 10, -28, 600 * eo(clamp(q / 0.25)), 300, t)
        sweat(f, 400, 1460 - 600, t, 3, 1.0)
    ui_word(f, "do you know", "SPICY FOOD", 470, t, 0.2, col=WHITE, acc=YEL_, size=190, shadow=0.5, lead_col=WHITE, out=T("i1", "doesn't") - 0.05)
    ui_word(f, "doesn't actually", "[BURN] YOU?", 470, t, T("i1", "doesn't"), col=WHITE, acc=YEL_, size=200, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S1: your mouth feels on fire ----
def shot_S1(t, n):
    f = stage("red", (255, 200, 90), 540, 980, 440); u = lt(t, "S1")
    z = 2.0 + 0.1 * eo(clamp(u / 1.6))
    chub_head_only(f, 380, 1010, z, t, mouth=3, expr="wow", brow="up", look=(1, 0), blink=False)
    fire_cone(f, 380 + 40, 1010 + 48 * z, 12, 620, 300, t)
    sweat(f, 380, 1010 - 130 * z, t, 3, 1.4)
    ui_word(f, "your mouth feels on", "[FIRE]", 470, t, st_("S1") + 0.15, col=WHITE, acc=YEL_, size=240, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S1b: but nothing is really burning — it's a trick ----
def shot_S1b(t, n):
    f = stage("purple", (255, 200, 90), 540, 980, 440); u = lt(t, "S1b")
    tn = T("i2", "nothing") - 0.1; tt = T("i2", "trick!") - 0.15
    fade = ramp(t, tn, 0.5)
    chub_head_only(f, 380, 1010, 2.1, t, mouth=talk(t) if t < tt else "o", expr="sus" if t < tt else "wow", brow="sus" if t < tt else "up", look=(1, 0))
    fire_cone(f, 420, 1111, 12, 620, 300, t, op=1 - 0.8 * fade)
    if t >= tn: slam(f, stamp_el("NOT REAL FIRE", WHITE, 58), 740, 1130, -8, t, tn + 0.15)
    if t >= tt:
        q = clamp((t - tt) / 0.35)
        caps(f, 740, 1420 - 140 * eo(q), 0.95, t, "sly", rot=-10)
        comp(f, burst_el("TRICK!", YEL_, INK, 62), 820, 760, scale=pin(t, tt + 0.05, 0.25))
    ui_word(f, "but nothing is", "[REALLY BURNING]", 470, t, tn, col=WHITE, acc=YEL_, size=150, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S2: the trickster: a chemical in chili peppers ----
def shot_S2(t, n):
    f = stage("teal", (255, 236, 160), 540, 1060, 430); u = lt(t, "S2")
    tc = T("a1", "chemical") - 0.15
    rot_comp(f, chili_el(), 470, 1080 + 8 * math.sin(t * 2.4), 6 * math.sin(t * 1.6), 1.25 * pin(t, st_("S2") + 0.02, 0.3), 1.0, 0.35)
    if t >= tc:
        k = ramp(t, tc, 0.5); mx, my = 760 - 250 * k, 1260 - 220 * k
        comp(f, magnifier_el(), mx, my + 80)
        for j in range(2):
            caps(f, mx - 40 + 70 * j, my - 50 + 80 * j, 0.36, t + j, "sly", rot=-15 + 30 * j)
        if k > 0.9: label_at(f, "CHEMICAL INSIDE", 800, 760, t, tc + 0.5, mx + 70, my - 90, bg=INK)
    ui_word(f, "the trickster hides in", "[CHILI PEPPERS]", 470, t, st_("S2") + 0.1, col=WHITE, acc=(255, 120, 110), size=150, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S2b: name card: CAPSAICIN ----
def shot_S2b(t, n):
    f = stage("sky", (255, 236, 160), 540, 1020, 440); u = lt(t, "S2b")
    s_ = 1.75 * pin(t, st_("S2b") + 0.05, 0.3)
    caps(f, 540, 1020, s_, t, "sly", rot=-6)
    rot_comp(f, scale_el(chili_el(face=True, mood="sly"), 0.42), 200, 1330, 12, 1.0, 1.0, 0.3)
    comp(f, chip("the chemical that makes chilis hot", INK, WHITE, 30), 560, 1330, op=clamp((u - 0.4) / 0.3))
    ui_word(f, "it's called", "[CAPSAICIN]", 470, t, T("a1", "capsaicin.") - 0.1, col=WHITE, acc=YEL_, size=180, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S3: your tongue is packed with nerve endings (magnified inset) ----
def shot_S3(t, n):
    f = stage("pink", (255, 236, 200), 540, 1000, 430); u = lt(t, "S3")
    comp(f, tongue_el(), 470, 1060, scale=0.9 * pin(t, st_("S3") + 0.03, 0.3))
    tn = T("a2", "nerve") - 0.2
    k = ramp(t, tn - 0.3, 0.35)
    def close(g):
        g[:] = np.array(C((40, 20, 60)), np.float32)
        nerve_xsec(g, t, y_s=640, xs=(620, 760, 900), bot=1200)
    if k > 0.01:
        draw_arrow(f, 420, 900, 610, 860, k, WHITE, 8, 26)
        inset(f, 760, 860, 230, close, k)
        label_at(f, "NERVE ENDINGS", 760, 1160, t, tn + 0.1)
    ui_word(f, "your tongue is packed with tiny", "[NERVE ENDINGS]", 470, t, tn, col=WHITE, acc=YEL_, size=130, shadow=0.5, lead_col=WHITE) if t >= tn else \
        ui_word(f, "your", "[TONGUE]", 470, t, st_("S3") + 0.1, col=WHITE, acc=YEL_, size=220, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S3b: think of them as wires to your brain ----
BR_Y = 720


def wires_to_brain(f, t, ring_k=0.0, t_pulse=None, lit=0.0, bx=540, by=BR_Y, tongue_y=1320):
    comp(f, scale_el(tongue_el(), 0.42), bx, tongue_y)
    paths = []
    for j, ox in enumerate((-100, 0, 100)):
        P = [(bx + ox, tongue_y - 80), (bx + ox * 0.9 + 30 * math.sin(j), (tongue_y + by) / 2 + 60), (bx + ox * 0.4, by + 130)]
        wire(f, P, lit=lit); paths.append(P)
    comp(f, scale_el(brain_el(face=True, mood="shout" if lit > 0.5 else "n", alarm_lit=lit > 0.5), 1.05), bx, by)
    if t_pulse is not None:
        for j, P in enumerate(paths): pulse_path(f, P, t, t_pulse + 0.08 * j, 0.55, n=3, gap=0.3)
    return paths


def shot_S3b(t, n):
    f = stage("emerald", (255, 236, 200), 540, 980, 440); u = lt(t, "S3b")
    tw = T("a2", "wires") - 0.15
    wires_to_brain(f, t, t_pulse=tw)
    label_at(f, "NERVES = WIRES", 820, 1040, t, tw, 620, 1020)
    label_at(f, "BRAIN", 860, 600, t, T("a2", "brain.") - 0.15, 740, 680)
    return finish(f, n)


# ---- S4: on those nerves sit little heat alarms ----
def shot_S4(t, n):
    f = stage("purple", (255, 236, 200), 540, 1000, 420); u = lt(t, "S4")
    ta = T("a3", "heat") - 0.2
    surface(f, 640, 1500, t)
    for i, (x, s_) in enumerate(((220, 0.6), (540, 1.15), (860, 0.6))):
        wire(f, [(x, 1500), (x - 20, 1200), (x, 900 + (40 if i != 1 else 90))])
        if t >= ta + 0.12 * abs(i - 1): alarm(f, x, 860 + (0 if i != 1 else 60), s_ * pin(t, ta + 0.12 * abs(i - 1), 0.3), t + i)
    label_at(f, "HEAT ALARM", 800, 1190, t, ta + 0.3, 610, 990)
    comp(f, chip("scientists call it TRPV1", INK, WHITE, 26), 540, 1430, op=clamp((t - ta - 0.6) / 0.3))
    ui_word(f, "and on those nerves sit little", "[HEAT ALARMS]", 470, t, st_("S4") + 0.1, col=WHITE, acc=(255, 110, 90), size=150, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S5: they only go off for PAINFUL heat ----
def shot_S5(t, n):
    f = stage("cream", (255, 214, 160), 540, 1000, 420); u = lt(t, "S5")
    tp = T("a4", "painful") - 0.1
    k = 0.25 + 0.75 * ramp(t, st_("S5") + 0.2, tp - st_("S5") - 0.1)
    thermo(f, 300, 1400, k, 720, (230, 40, 40))
    r_ = 1.0 if t >= tp else 0.0
    alarm(f, 720, 1060, 1.35, t, ring=r_)
    if t < tp: comp(f, chip("warm: silent", INK, WHITE, 30), 720, 1300, op=clamp((u - 0.3) / 0.3))
    else: slam(f, stamp_el("PAINFUL HEAT: RING!", RED_, 44), 720, 1320, -4, t, tp)
    ui_word(f, "they only go off for", "[PAINFUL HEAT]", 470, t, st_("S5") + 0.1, col=INK, acc=RED_, size=160)
    return finish(f, n)


# ---- S5b: like a scalding sip of tea ----
def shot_S5b(t, n):
    f = stage("sky", (255, 236, 180), 540, 1000, 430); u = lt(t, "S5b")
    ts = T("a4", "scalding") - 0.1
    hot = t >= ts + 0.3
    chub(f, 470, 1460, 1.05, la=(20, 10) if not hot else (150, 175), ra=(148, -130) if not hot else (60, 40), mouth=0 if not hot else "o",
         expr="happy" if not hot else "wow", brow="up", look=(0.5, -0.5), hold=scale_el(teacup_el(), 0.55), hold_off=(-40, 0) if not hot else (30, 40), hold_front=True,
         bob=0 if not hot else 10 * math.sin(t * 30))
    steam(f, 420 if not hot else 560, 960 if not hot else 1150, t, 1.0, 0.6)
    if hot:
        alarm(f, 820, 760, 0.8, t, ring=1.0)
        comp(f, burst_el("OUCH!", YEL_, INK, 50), 230, 760, scale=pin(t, ts + 0.3, 0.22))
    ui_word(f, "like a scalding sip of", "[TEA]", 470, t, st_("S5b") + 0.05, col=WHITE, acc=YEL_, size=220, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S6: capsaicin fits those alarms perfectly ----
AX, AY, AS = 700, 1080, 1.4


def shot_S6(t, n):
    f = stage("teal", (255, 236, 180), AX, AY, 380); u = lt(t, "S6")
    tf = T("a5", "perfectly.") - 0.25
    surface(f, AY + 140, 1540, t, 0, W)
    wire(f, [(AX, 1520), (AX, AY + 120)])
    inn = t >= tf
    alarm(f, AX, AY, AS, t, key_in=inn)
    k = eio(clamp((t - st_("S6") - 0.1) / (tf - st_("S6") - 0.1)))
    sx, sy = 200, 760; ex, ey = AX - 150 * 0.8 - 10, AY + 10
    cx_ = sx + (ex - sx) * k; cy_ = sy + (ey - sy) * k - 160 * math.sin(math.pi * k)
    caps(f, cx_, cy_, 0.8, t, "sly" if not inn else "happy", rot=0, wig=not inn)
    if inn:
        sparkles(f, AX, AY, t, tf, 12, 200)
        comp(f, check_el(46, True), AX + 190, AY - 150, scale=pin(t, tf + 0.1, 0.25))
    ui_word(f, "capsaicin fits those alarms", "[PERFECTLY]", 470, t, st_("S6") + 0.1, col=WHITE, acc=YEL_, size=170, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S6b: like a key in a lock (analogy, split screen) ----
def shot_S6b(t, n):
    f = stage("yellow"); u = lt(t, "S6b")
    f[960:1500] = f[960:1500] * 0.82 + np.array(C((255, 120, 40)), np.float32) * 0.18
    cv2.line(f, (60, 960), (960, 960), C(INK), 6, cv2.LINE_AA)
    k = ramp(t, st_("S6b") + 0.2, 0.6)
    comp(f, padlock_el(k >= 1), 720, 760, scale=0.75)
    rot_comp(f, scale_el(key_el(), 0.8), 260 + 260 * k, 812, 0, 1.0, 1.0, 0.2)
    comp(f, chip("KEY", INK, WHITE, 34), 230, 640); comp(f, chip("LOCK", INK, WHITE, 34), 720, 600)
    k2 = ramp(t, st_("S6b") + 0.5, 0.6)
    alarm(f, 720, 1240, 0.95, t, key_in=k2 >= 1, ring=1.0 if k2 >= 1 else 0)
    if k2 < 1: caps(f, 240 + 260 * k2, 1250, 0.6, t, "sly", wig=False)
    comp(f, chip("CAPSAICIN", INK, WHITE, 34), 240, 1120, op=clamp((u - 0.3) / 0.3)); comp(f, chip("HEAT ALARM", INK, WHITE, 34), 720, 1410, op=clamp((u - 0.3) / 0.3))
    if u > 0.4:
        cv2.circle(f, (540, 960), 58, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (540, 960), 50, (1, 1, 1), -1, cv2.LINE_AA)
        comp(f, ed_el("", "=", "", big_col=INK, big_size=90), 540, 962, scale=pin(t, st_("S6b") + 0.4, 0.25))
    ui_word(f, "like a", "[KEY] IN A [LOCK]", 400, t, st_("S6b") + 0.05, col=INK, acc=RED_, size=120)
    return finish(f, n)


# ---- S7: CLICK! the alarm rings ----
def shot_S7(t, n):
    f = stage("red", (255, 220, 120), 540, 1040, 470); u = lt(t, "S7")
    tc = st_("S7") + 0.1
    turn = ramp(t, tc, 0.15)
    rays(f, 540, 1040, 760, (255, 230, 120), 0.4 * turn, t)
    surface(f, 1240, 1560, t)
    alarm(f, 540, 1080, 2.1, t, ring=turn, key_in=True)
    caps(f, 540 - 150 * 1.0 - 20, 1100 - 30 * turn, 1.0, t, "happy", rot=-25 * turn, wig=False)
    comp(f, burst_el("CLICK!", YEL_, INK, 70), 800, 700, scale=pin(t, tc, 0.22))
    ui_word(f, "the alarm", "[RINGS]", 470, t, T("a6", "rings,") - 0.15, col=WHITE, acc=YEL_, size=200, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S7b: your nerves shout to your brain... FIRE! ----
def shot_S7b(t, n):
    tF = T("a6", "FIRE!") - 0.15
    lit = 1.0 if t >= tF else 0.0
    f = stage("purple" if not lit else "orange", (255, 220, 120) if lit else None, 540, 760, 380)
    if lit: flames_row(f, 540, 900, 760, t, 260, 0.9)
    wires_to_brain(f, t, t_pulse=st_("S7b") + 0.05, lit=lit, by=800)
    alarm(f, 540, 1210, 0.6, t, ring=1.0, key_in=True)
    if lit: comp(f, burst_el("FIRE!", YEL_, RED_, 74), 820, 1000, scale=pin(t, tF, 0.22))
    else: label_at(f, "SIGNAL", 810, 1060, t, st_("S7b") + 0.2, 620, 1020)
    ui_word(f, "your nerves shout to your", "[BRAIN]", 430, t, st_("S7b") + 0.1, col=WHITE, acc=YEL_, size=150, shadow=0.5, lead_col=WHITE, out=tF - 0.05)
    return finish(f, n)


# ---- S8: your brain believes it ----
def shot_S8(t, n):
    f = stage("orange", (255, 220, 120), 540, 900, 420); u = lt(t, "S8")
    flames_row(f, 540, 1060, 900, t, 200, 0.85)
    rot_comp(f, brain_el(face=True, mood="worried", alarm_lit=True), 540, 860 + 10 * math.sin(t * 9), 3 * math.sin(t * 7), 1.05, 1.0, 0.3)
    chub(f, 830, 1480, 0.62, la=(150, 175), ra=(150, 175), mouth="o", expr="wow", brow="up", look=(-1, -1), bob=-10 * abs(math.sin(t * 14)))
    sweat(f, 830, 1480 - 400, t, 3, 0.7)
    ui_word(f, "your brain", "[BELIEVES IT]", 470, t, st_("S8") + 0.1, col=WHITE, acc=YEL_, size=180, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S8b: what you feel vs what's really there ----
def shot_S8b(t, n):
    f = stage("sky"); u = lt(t, "S8b")
    f[620:1500, 540:1020] = f[620:1500, 540:1020] * 0.75 + np.array(C((20, 160, 140)), np.float32) * 0.25
    f[620:1500, 60:540] = f[620:1500, 60:540] * 0.75 + np.array(C((230, 60, 30)), np.float32) * 0.25
    cv2.line(f, (540, 620), (540, 1500), C(INK), 8, cv2.LINE_AA)
    comp(f, scale_el(tongue_el(), 0.5), 300, 1150); comp(f, scale_el(tongue_el(), 0.5), 780, 1150)
    flames_row(f, 300, 1100, 360, t, 300, 0.95)
    for j, (x, y) in enumerate(((700, 1080), (860, 1160), (760, 1260))):
        caps(f, x, y, 0.32, t + j, "sly")
    tr = T("a7", "no") - 0.15
    comp(f, chip("WHAT YOU FEEL", INK, WHITE, 30), 300, 690); comp(f, chip("WHAT'S REALLY THERE", INK, WHITE, 30), 780, 690, op=clamp((t - st_("S8b") - 0.4) / 0.3))
    if t >= tr: comp(f, check_el(44, True), 780, 880, scale=pin(t, tr, 0.25)); comp(f, chip("no real burn", (20, 140, 90), WHITE, 28), 780, 1440, op=clamp((t - tr) / 0.3))
    ui_word(f, "you feel burning, but", "[NO REAL FIRE]", 470, t, T("a7", "with") - 0.2, col=WHITE, acc=YEL_, size=150, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S9: finding these alarms was a big deal ----
def shot_S9(t, n):
    f = stage("emerald", (255, 236, 160), 680, 980, 320); u = lt(t, "S9")
    alarm(f, 700, 1000, 1.2, t, ring=0.5 + 0.5 * math.sin(t * 3) ** 2)
    sparkles(f, 700, 980, t, st_("S9") + 0.2, 12, 260, seed=4, dur=1.2)
    chub(f, 300, 1470, 0.95, la=(20, 10), ra=(95, 60), mouth=talk(t), expr="wow" if talk(t) == 0 else "n", brow="up", look=(1, -1),
         hold=scale_el(magnifier_el(), 0.55), hold_off=(40, -60), hold_front=True)
    spotlight(f, 640, 1050, 330, 0.45 * ramp(t, st_("S9") + 0.1, 0.4))
    ui_word(f, "finding these alarms was a", "[BIG DEAL]", 470, t, T("b1", "big") - 0.2, col=WHITE, acc=YEL_, size=190, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S9b: it helped win a Nobel Prize in 2021 ----
def shot_S9b(t, n):
    f = stage("purple", (255, 214, 100), 540, 980, 430); u = lt(t, "S9b")
    tn = T("b1", "Nobel") - 0.15
    rays(f, 540, 980, 820, (255, 220, 120), 0.45 * ramp(t, tn, 0.3), t)
    if t >= tn: slam(f, medal_el("2021"), 540, 1000, 6 * math.sin(t * 2), t, tn, 1.15)
    confetti(f, t, tn, 50)
    chub(f, 860, 1480, 0.6, la=(150, 170), ra=(150, 175), mouth=2, expr="happy", brow="up", bob=-12 * abs(math.sin(t * 9)))
    comp(f, chip("Source: NobelPrize.org, 2021 (David Julius)", INK, WHITE, 22), 540, 1462, op=clamp((t - tn - 0.4) / 0.3))
    ui_word(f, "it helped win a", "[NOBEL PRIZE]", 470, t, tn - 0.3, col=WHITE, acc=YEL_, size=170, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S10: so how do you put out a fake fire? ----
def shot_S10(t, n):
    f = stage("orange", (255, 220, 120), 540, 980, 430); u = lt(t, "S10")
    chub(f, 380, 1460, 1.05, la=(-150, -150), ra=(60, 30), mouth="o", expr="wow", brow="sad", look=(1, -1))
    mx, my = mouth_xy(380, 1460, 1.05)
    fire_cone(f, mx + 20, my, -10, 430, 220, t, op=0.9)
    comp(f, bubble_el("HOW?", 60), 800, 760, scale=pin(t, T("c1", "how") - 0.1, 0.3))
    ui_word(f, "how do you put out a", "[FAKE FIRE?]", 470, t, st_("S10") + 0.15, col=WHITE, acc=YEL_, size=180, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S11: scientists tested seven drinks ----
DK = ["water", "cola", "sweet", "seltzer", "beer", "skim", "whole"]
DL = ["WATER", "COLA", "SWEET", "SELTZER", "0% BEER", "SKIM MILK", "WHOLE MILK"]
DX = [180 + 120 * i for i in range(7)]
GX = [(240, 880), (420, 880), (600, 880), (780, 880), (330, 1230), (510, 1230), (690, 1230)]


def glasses(f, t, t0, s=0.72, dt=0.09):
    for i, (k, (x, y)) in enumerate(zip(DK, GX)):
        if t < t0 + i * dt: continue
        rot_comp(f, scale_el(drink_el(k), s), x, y + 6 * math.sin(t * 3 + i), 0, pin(t, t0 + i * dt, 0.25), 1.0, 0.25)
        comp(f, chip(DL[i], INK, WHITE, 22), x, y + 138, op=clamp((t - t0 - i * dt) / 0.2))
        comp(f, ed_el("", str(i + 1), "", big_col=WHITE, big_size=46, shadow=0.4), x, y - 150, op=clamp((t - t0 - i * dt) / 0.15))


def shot_S11(t, n):
    f = stage("sky", (255, 255, 255), 540, 1050, 420); u = lt(t, "S11")
    glasses(f, t, st_("S11") + 0.15, dt=(T("c2", "drinks") - st_("S11") - 0.1) / 7)
    ui_word(f, "scientists tested", "[7 DRINKS]", 470, t, st_("S11") + 0.15, col=WHITE, acc=YEL_, size=200, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S11b: on 72 people eating spicy sauce (count-up + crowd) ----
def shot_S11b(t, n):
    f = stage("teal"); u = lt(t, "S11b")
    t0 = st_("S11b") + 0.05
    nshow = count_up(t, t0, 72, 0.9)
    hd = scale_el(chub_head_el(0, False, "n", 0, 0, "happy"), 0.24)
    for i in range(nshow):
        r_, c_ = divmod(i, 9)
        comp(f, hd, 220 + c_ * 80, 760 + r_ * 72 + 3 * math.sin(t * 6 + i))
    ui_word(f, "on", f"[{nshow}] PEOPLE", 470, t, t0, col=WHITE, acc=YEL_, size=200, shadow=0.5, lead_col=WHITE)
    comp(f, chip("eating spicy sauce · Penn State, 2019", INK, WHITE, 26), 540, 1400, op=clamp((t - T("c2", "spicy") + 0.1) / 0.3))
    return finish(f, n)


# ---- S12: burn meters — water helped a little, fizzy drinks did badly ----
BURN0 = 480


def burn_bars(f, t, tw, tz, tm, base=1250):
    drop = {"water": 0.25 * ramp(t, tw, 0.4), "cola": 0.08 * ramp(t, tz, 0.4), "seltzer": 0.07 * ramp(t, tz, 0.4), "beer": 0.06 * ramp(t, tz, 0.4),
            "sweet": 0.5 * ramp(t, tm, 0.5), "skim": 0.6 * ramp(t, tm, 0.5), "whole": 0.62 * ramp(t, tm, 0.5)}
    for i, (k, x) in enumerate(zip(DK, DX)):
        hv = BURN0 * (1 - drop[k]); top = int(base - hv); base = int(base)
        g = np.linspace(0, 1, max(1, base - top))[:, None, None]
        f[int(top) + 10:int(base) + 10, int(x - 44) + 10:int(x + 44) + 10] *= 0.72
        f[int(top):int(base), int(x - 44):int(x + 44)] = np.array(C((255, 230, 80)), np.float32) * (1 - g) + np.array(C((230, 40, 30)), np.float32) * g
        cv2.rectangle(f, (int(x - 44), int(top)), (int(x + 44), int(base)), C(INK), 5, cv2.LINE_AA)
        rot_comp(f, scale_el(drink_el(k), 0.42), x, base + 90, 0, 1.0, 1.0, 0.2)
    comp(f, chip("BURN LEFT AFTER EACH DRINK (simplified)", INK, WHITE, 24), 540, 700)


def shot_S12(t, n):
    f = stage("cream"); u = lt(t, "S12")
    tw = T("c3", "Water"); tz = T("c3", "Fizzy")
    burn_bars(f, t, tw, tz, 1e9)
    if t >= tz:
        for x in (DX[1], DX[3], DX[4]): comp(f, check_el(30, False), x, 760 + 30, scale=pin(t, tz + 0.15, 0.2))
    ui_word(f, "water", "[A LITTLE]", 470, t, tw - 0.1, col=INK, acc=(40, 120, 230), size=170, out=tz - 0.1)
    ui_word(f, "fizzy drinks did", "[BADLY]", 470, t, tz - 0.05, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S12b: and the winner... milk! ----
def shot_S12b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 980, 440); u = lt(t, "S12b")
    tm = T("c3", "milk!") - 0.15
    if t < tm:
        burn_bars(f, t, -1, -1, 1e9)
        spotlight(f, 860, 1100, 160, 0.5 * ramp(t, st_("S12b"), 0.3))
    else:
        rays(f, 540, 1000, 800, (255, 255, 255), 0.5, t)
        cv2.rectangle(f, (300, 1250), (780, 1460), C(INK), -1, cv2.LINE_AA); cv2.rectangle(f, (310, 1260), (770, 1450), C((255, 200, 40)), -1, cv2.LINE_AA)
        comp(f, ed_el("", "1", "", big_col=INK, big_size=120), 540, 1350)
        rot_comp(f, scale_el(drink_el("whole"), 1.35), 540, 1040, 4 * math.sin(t * 3), pin(t, tm, 0.25), 1.0, 0.3)
        confetti(f, t, tm, 50)
        comp(f, chip("Source: Penn State, Physiology & Behavior, 2019", INK, WHITE, 22), 540, 1490 - 28, op=clamp((t - tm - 0.4) / 0.3))
    ui_word(f, "and the winner...", "[MILK!]" if t >= tm else "?", 470, t, st_("S12b") + 0.05 if t < tm else tm, col=INK, acc=(40, 120, 230), size=230)
    return finish(f, n)


# ---- S13: even skim milk worked almost as well as whole ----
def shot_S13(t, n):
    f = stage("sky"); u = lt(t, "S13")
    tsk = T("c4", "skim") - 0.15; twh = T("c4", "whole") - 0.15
    if t >= tsk: rot_comp(f, scale_el(drink_el("skim"), 1.15), 300, 1060, -4, pin(t, tsk, 0.25), 1.0, 0.3); comp(f, chip("SKIM: no fat", INK, WHITE, 30), 300, 1290)
    if t >= twh: rot_comp(f, scale_el(drink_el("whole"), 1.15), 780, 1060, 4, pin(t, twh, 0.25), 1.0, 0.3); comp(f, chip("WHOLE: full fat", INK, WHITE, 30), 780, 1290)
    if t >= twh + 0.2: comp(f, ed_el("", "≈", "", big_col=INK, big_size=150), 540, 1040, scale=pin(t, twh + 0.2, 0.25))
    ui_word(f, "even skim milk worked", "[ALMOST AS WELL]", 470, t, st_("S13") + 0.1, col=WHITE, acc=YEL_, size=140, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S13b: scientists think milk's proteins help (pull capsaicin out of the alarms) ----
def shot_S13b(t, n):
    f = stage("emerald"); u = lt(t, "S13b")
    tp = T("c4", "proteins") - 0.2
    surface(f, 1240, 1560, t)
    for j, x in enumerate((240, 540, 840)):
        q = clamp((t - tp - 0.15 * j) / 0.7)
        alarm(f, x, 1170, 0.8, t + j, ring=1.0 - clamp(q * 1.6), key_in=q < 0.25)
        px = x + 30 - 300 * (1 - clamp((t - st_("S13b") - 0.1 * j) / 0.5)) if q <= 0 else x + 40 + 120 * q
        py = 940 - 30 * j if q <= 0 else 1100 - 280 * q
        if q > 0.25: caps(f, px - 60, py + 50, 0.4, t + j, "o" if q < 1 else "sly", rot=40 * q)
        rot_comp(f, scale_el(protein_el(), 0.95), px, py, 10 * math.sin(t * 4 + j), 1.0, 1.0, 0.25)
    label_at(f, "MILK PROTEINS", 540, 660, t, st_("S13b") + 0.4)
    comp(f, chip("scientists are still testing why", INK, WHITE, 24), 540, 1440, op=clamp((u - 0.5) / 0.3))
    ui_word(f, "scientists think milk's", "[PROTEINS] HELP", 470, t, st_("S13b") + 0.1, col=WHITE, acc=YEL_, size=140, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S14: now here's the weirdest part (double take) ----
def shot_S14(t, n):
    f = stage("pink", (255, 236, 200), 540, 1000, 430); u = lt(t, "S14")
    snap = u > 0.7
    chub(f, 540, 1460, 1.1, la=(20, 10) if not snap else (150, 175), ra=(20, 10) if not snap else (150, 175), mouth=talk(t) if not snap else "o",
         expr="n" if not snap else "wow", brow="n" if not snap else "up", look=(1, 0) if not snap else (0, -1), lean=0 if not snap else -4, squash=0 if not snap else -0.4)
    if snap: comp(f, burst_el("?!", YEL_, INK, 90), 840, 760, scale=pin(t, st_("S14") + 0.7, 0.22))
    ui_word(f, "here's the", "[WEIRDEST PART]", 470, t, st_("S14") + 0.1, col=WHITE, acc=YEL_, size=170, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S14b: birds can't feel the burn at all ----
def shot_S14b(t, n):
    f = stage("emerald"); u = lt(t, "S14b")
    m, c = munch(t, 0.3)
    rot_comp(f, scale_el(bird_el(0, m == 2, True), 1.2), 330, 1180 + 6 * math.sin(t * 9), 0, pin(t, st_("S14b") + 0.05, 0.3), 1.0, 0.3)
    rot_comp(f, scale_el(chili_el(), 0.32), 520 - (20 if m == 2 else 0), 1150, -80, 1.0, 1.0, 0.2)
    comp(f, check_el(44, True), 330, 900, scale=pin(t, T("d1", "feel") - 0.1, 0.25))
    chub(f, 820, 1470, 0.72, la=(150, 175), ra=(150, 175), mouth="o", expr="wow", brow="up", look=(-1, 0))
    mx, my = mouth_xy(820, 1470, 0.72); fire_cone(f, mx - 30, my, -150, 240, 130, t)
    comp(f, chip("Source: Tewksbury & Nabhan, Nature 2001", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    ui_word(f, "birds can't feel the", "[BURN] AT ALL", 470, t, st_("S14b") + 0.1, col=WHITE, acc=YEL_, size=170, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S15: they happily eat hot chili peppers ----
def shot_S15(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S15")
    cyc = (u * 1.6) % 1.0; idx = int(u * 1.6)
    x = 920 - 230 * eio(clamp(cyc / 0.6)); y = 1000 + 50 * clamp(cyc / 0.6) - 40 * math.sin(math.pi * clamp(cyc / 0.6))
    if cyc < 0.62: rot_comp(f, scale_el(chili_el(), 0.34), x, y, -80 + 20 * cyc, 1.0, 1.0, 0.2)
    rot_comp(f, scale_el(bird_el(0, 0.45 < cyc < 0.75, cyc > 0.75), 1.7), 420, 1100 + 8 * math.sin(t * 8), 0, 1.0, 1.0, 0.35)
    for j in range(min(idx, 4)): comp(f, chip("GULP", INK, WHITE, 22), 300 + 120 * j, 1440)
    ui_word(f, "they happily eat", "[HOT CHILIS]", 470, t, st_("S15") + 0.1, col=INK, acc=RED_, size=180)
    return finish(f, n)


# ---- S15b: then drop the seeds somewhere new, ready to grow ----
def shot_S15b(t, n):
    f = stage("sky", (255, 255, 230), 860, 700, 130); u = lt(t, "S15b")
    f[1330:1500] = np.array(C((90, 180, 80)), np.float32); cv2.line(f, (0, 1330), (W, 1330), C(INK), 6, cv2.LINE_AA)
    k = clamp(u / 1.6); bx = 120 + 820 * k; by = 760 + 40 * math.sin(u * 6)
    flap = int(u * 10) % 3
    if u < 2.2: rot_comp(f, scale_el(bird_el(flap if flap != 2 else 1, False, True), 0.8), bx, by, 0, 1.0, 1.0, 0.0)
    td = st_("S15b") + 0.6
    q = clamp((t - td) / 0.6)
    if t >= td: seeds(f, [(560 + 20 * j, 820 + (1320 - 820) * q * q - 10 * j) for j in range(3)], 1.2)
    plant(f, 590, 1330, 0.95, clamp((t - td - 0.6) / 1.2), t)
    if t >= T("d2", "grow.") - 0.1: sparkles(f, 590, 1100, t, T("d2", "grow.") - 0.1, 10, 200)
    ui_word(f, "then drop the seeds", "[SOMEWHERE NEW]", 470, t, st_("S15b") + 0.1, col=WHITE, acc=YEL_, size=150, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S16: but mice chew the seeds to bits ----
def shot_S16(t, n):
    f = stage("cream", (230, 200, 160), 540, 1000, 430); u = lt(t, "S16")
    m, c = munch(t, 0.22)
    rot_comp(f, scale_el(mouse_el(m == 2), 1.5), 600, 1200 + (4 if m else 0), 0, 1.0, 1.0, 0.35)
    seeds(f, [(330, 1300), (290, 1320)], 1.3)
    rng = np.random.default_rng(int(t * 12))
    for j in range(8):
        ph = (t * 2 + j / 8) % 1.0
        cv2.circle(f, (int(380 - 160 * ph + rng.uniform(-30, 30)), int(1250 - 120 * ph + 300 * ph * ph)), 6, C((255, 236, 170)), -1, cv2.LINE_AA)
    comp(f, check_el(40, False), 330, 1160, scale=pin(t, T("d3", "bits.") - 0.2, 0.25))
    ui_word(f, "mice chew the seeds", "[TO BITS]", 470, t, st_("S16") + 0.1, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S16b: so the burn keeps them away ----
def shot_S16b(t, n):
    f = stage("red", (255, 200, 120), 540, 1000, 420); u = lt(t, "S16b")
    tb = st_("S16b") + 0.35
    rot_comp(f, scale_el(chili_el(face=True, mood="sly"), 0.7), 330, 1180, 0, 1.0, 1.0, 0.3)
    if t < tb:
        rot_comp(f, scale_el(mouse_el(False), 1.2), 620, 1260, 0, 1.0, 1.0, 0.3)
    else:
        q = t - tb; x = 640 + 900 * clamp((q - 0.5) / 0.9) ** 2
        rot_comp(f, scale_el(mouse_el(False, True), 1.2), x, 1260 - 30 * abs(math.sin(q * 20)), 0, 1.0, 1.0, 0.3)
        if q < 0.9: fire_cone(f, x - 175, 1290, 180, 240 * eo(clamp(q / 0.2)), 120, t)
        if q > 0.5: speed_lines(f, t, 0.8, 1150, 1350, 10)
    ui_word(f, "so the burn", "[KEEPS THEM AWAY]", 470, t, st_("S16b") + 0.08, col=WHITE, acc=YEL_, size=150, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S17: scientists think that's why chilis are spicy ----
def shot_S17(t, n):
    f = stage("emerald", (255, 236, 170), 540, 1000, 430); u = lt(t, "S17")
    plant(f, 540, 1440, 1.6, 1.0, t)
    rot_comp(f, scale_el(chili_el(face=True, mood="happy"), 0.75), 540, 1050, 4 * math.sin(t * 2), 1.0, 1.0, 0.35)
    comp(f, chip("a 2001 field study in Arizona", INK, WHITE, 24), 540, 1462, op=clamp((u - 0.5) / 0.3))
    ui_word(f, "scientists think that's why chilis are", "[SPICY]", 470, t, st_("S17") + 0.1, col=WHITE, acc=(255, 110, 100), size=220, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S17b: to pick who eats them (chili bouncer) ----
def shot_S17b(t, n):
    f = stage("purple"); u = lt(t, "S17b")
    for x in (180, 900):
        cv2.rectangle(f, (x - 14, 1100), (x + 14, 1400), C(GOLD), -1, cv2.LINE_AA); cv2.circle(f, (x, 1100), 26, C(GOLD), -1, cv2.LINE_AA)
    rot_comp(f, scale_el(chili_el(face=True, mood="sly"), 0.95), 540, 1120, 3 * math.sin(t * 3), 1.0, 1.0, 0.35)
    kb = clamp(u / 1.2)
    rot_comp(f, scale_el(bird_el(int(u * 10) % 2, False, True), 0.75), 160 + 400 * kb, 780 - 60 * math.sin(math.pi * kb), 0, 1.0, 1.0, 0.0)
    comp(f, check_el(40, True), 300, 650, scale=pin(t, st_("S17b") + 0.3, 0.25))
    rope = [(180, 1150), (360, 1230), (540, 1250), (720, 1230), (900, 1150)]
    cv2.polylines(f, [np.array(rope, np.int32)], False, C(INK), 22, cv2.LINE_AA); cv2.polylines(f, [np.array(rope, np.int32)], False, C((200, 20, 50)), 14, cv2.LINE_AA)
    rot_comp(f, scale_el(mouse_el(False, u > 0.8), 0.9), 780, 1390, 0, 1.0, 1.0, 0.3)
    if u > 0.8: comp(f, check_el(40, False), 780, 1250, scale=pin(t, st_("S17b") + 0.8, 0.25))
    comp(f, chip("BIRDS: YES   MICE: NO", INK, WHITE, 28), 540, 1462, op=clamp((u - 0.3) / 0.3))
    ui_word(f, "to pick", "[WHO EATS THEM]", 470, t, st_("S17b") + 0.05, col=WHITE, acc=YEL_, size=170, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S18: visual recap ----
def shot_S18(t, n):
    f = stage("cream"); u = lt(t, "S18")
    t0 = st_("S18") + 0.2
    items = [(scale_el(caps_el("sly"), 0.55), "CAPSAICIN"), (scale_el(alarm_el(True, True), 0.9), "ALARM RINGS"), (scale_el(brain_el(True, "shout", True), 0.52), "BRAIN: FIRE!")]
    recap_steps(f, items, 860, t, [t0, t0 + 0.35, t0 + 0.7], 300)
    tb = T("e1", "burn.") - 0.2
    if t >= tb: slam(f, stamp_el("A TRICK, NOT A BURN", RED_, 50), 540, 1130, -4, t, tb)
    tm = T("e1", "milk") - 0.15
    if t >= tm:
        rot_comp(f, scale_el(drink_el("whole"), 0.6), 380, 1340, 0, pin(t, tm, 0.25), 1.0, 0.25)
        comp(f, ed_el("", ">", "", big_col=INK, big_size=110), 540, 1330, op=clamp((t - tm - 0.2) / 0.2))
        rot_comp(f, scale_el(drink_el("water"), 0.6), 700, 1340, 0, pin(t, tm + 0.25, 0.25), 1.0, 0.25)
    ui_word(f, "so remember", "[RECAP]", 470, t, st_("S18") + 0.05, col=INK, acc=RED_, size=170)
    return finish(f, n)


# ---- S19: send it + FreshNestHub sting ----
def shot_S19(t, n):
    f = stage("yellow", (255, 255, 255), 540, 880, 420); u = lt(t, "S19")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("curry night tonight?", "brb chugging all the water", pr), 0.82), 640, 950, scale=pin(t, st_("S19")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (640, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 250, 1480, 0.8, la=(20, 10), ra=(148, -130), mouth="o", expr="wow", brow="up", look=(1, 0),
             hold=scale_el(drink_el("water", 0.6), 0.42), hold_off=(-30, -8), hold_front=True)
        sweat(f, 250, 1480 - 420, t, 3, 0.8)
        ui_word(f, "send to the friend who chugs", "[WATER]", 420, t, T("e2", "friend") - 0.1, col=INK, acc=(40, 120, 230), size=190, tail="after every spicy bite")
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INK, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1480, 0.7, la=(20, 10), ra=(148, -130), mouth=2, expr="happy", brow="up", hold=scale_el(drink_el("whole", 0.5), 0.4), hold_off=(-30, -8), hold_front=True)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TF0, 0.5, 22), (st_("S1") + 0.02, 0.3, 12), (T("i2", "trick!") - 0.15, 0.35, 16), (T("a1", "capsaicin.") - 0.1, 0.25, 10),
           (T("a3", "heat") - 0.2, 0.25, 10), (T("a4", "painful") - 0.1, 0.35, 16), (T("a4", "scalding") + 0.2, 0.35, 16),
           (T("a5", "perfectly.") - 0.25, 0.25, 10), (st_("S7") + 0.1, 0.45, 22), (T("a6", "FIRE!") - 0.15, 0.5, 24),
           (T("b1", "Nobel") - 0.15, 0.35, 16), (T("c2", "seven") - 0.2, 0.2, 8), (T("c3", "badly.") - 0.2, 0.3, 12),
           (T("c3", "milk!") - 0.15, 0.4, 18), (st_("S14") + 0.7, 0.35, 16), (T("d3", "bits.") - 0.2, 0.25, 10),
           (st_("S16b") + 0.35, 0.35, 14), (T("d4", "spicy.") - 0.2, 0.25, 10), (T("e1", "burn.") - 0.2, 0.3, 12)]


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
