# ================= shots: FreshNestHub — "Too many carrots can turn your skin orange" (carotenemia) =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "Like,") - 0.15, "punch"), ("S1", T("a1", "It's") - 0.2, "whip"),
    ("S2", T("a2", "Your") - 0.2, "flash"), ("S3", T("a3", "The") - 0.2, "whip"), ("S3b", T("a3", "then") - 0.12, "zoom"),
    ("S4a", T("b1", "Thick") - 0.2, "flash"), ("S4b", T("b1", "So") - 0.12, "punch"), ("S4c", T("b1", "Then") - 0.1, "whip"),
    ("S4d", T("b1", "even") - 0.12, "zoom"), ("S5", T("c1", "How") - 0.2, "flash"), ("S6", T("c2", "And") - 0.15, "whip"),
    ("S7", T("d1", "The") - 0.2, "punch"), ("S8", T("d2", "One") - 0.2, "whip"), ("S8b", T("d2", "If") - 0.12, "punch"),
    ("S9", T("f1", "And") - 0.2, "flash"), ("S10", T("f2", "Britain") - 0.2, "whip"), ("S10b", T("f2", "The") - 0.12, "zoom"),
    ("S11", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_CC = "Sources: Cleveland Clinic · NIH StatPearls · UAMS Health"
ORG = (255, 140, 30)


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


# ---- S0: hook — Chubby munches carrots... and turns ORANGE ----
TO0 = T("i1", "orange?") - 0.25


def shot_S0(t, n):
    f = stage("sky", (255, 214, 120), 540, 980, 440)
    orange = t >= TO0; k = ramp(t, TO0, 0.3)
    if orange: rays(f, 540, 1080, 760, (255, 200, 120), 0.55 * k, t)
    npile = min(7, 4 + int(t / 0.42))
    for i in range(npile):
        px = [210, 870, 300, 780, 160, 920, 420][i]; py = [1470, 1480, 1500, 1495, 1430, 1440, 1515][i]
        rot_comp(f, scale_el(carrot_el(0), 0.4), px, py, 70 + 33 * i, pin(t, max(0, i - 3) * 0.42, 0.2), 1.0, 0.2)
    m, c = munch(t)
    if not orange:
        chub(f, 540, 1440, 1.15, la=(20, 10), ra=(148, -130), mouth=m, blink=False, brow="up", expr="happy",
             hold=carrot_side(0, 0.5), hold_off=(-30 - 6 * (c % 3), 0), bob=4 * math.sin(t * 15), hold_front=True)
    else:
        chub(f, 540, 1440, 1.15, la=(150, 170), ra=(150, 170), mouth="o", brow="up", expr="wow", tint=k, look=(0, -1))
        comp(f, burst_el("ORANGE?!", YEL_, INK, 52), 790, 830, scale=pin(t, TO0 + 0.1, 0.25))
    ui_word(f, "eating too many", "CARROTS", 470, t, T("i1", "eating") - 0.1, col=WHITE, acc=ORG, size=170, shadow=0.45, lead_col=WHITE, out=TO0 - 0.05)
    ui_word(f, "can turn your skin", "[ORANGE]", 470, t, TO0, col=WHITE, acc=ORG, size=200, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S0b: actually orange — and it's real ----
def shot_S0b(t, n):
    f = stage("purple", (255, 214, 120), 540, 1000, 430); u = lt(t, "S0b")
    tr = T("i2", "real.") - 0.2
    chub(f, 450, 1470, 1.05, la=(20, 10), ra=(-120, -120), mouth=talk(t) if t < tr else "o", brow="up", expr="wow", tint=1.0, look=(1, 0))
    rot_comp(f, scale_el(mirror_el(), 0.75), 760, 1060 + 8 * math.sin(t * 4), -14, pin(t, SHOT["S0b"]["start"] + 0.05, 0.3), 1.0, 0.35)
    comp(f, scale_el(chub_head_el(0, False, "up", -1, 0, "wow", 1.0), 0.62), 748, 1010 + 8 * math.sin(t * 4), op=0.85)
    if t >= tr:
        slam(f, stamp_el("100% REAL", GRN_, 70), 540, 760, -8, t, tr)
        comp(f, chip("doctors call it carotenemia", INK, WHITE, 32), 540, 1462, scale=pin(t, tr + 0.2, 0.25))
    ui_word(f, "like,", "ACTUALLY ORANGE", 470, t, SHOT["S0b"]["start"] + 0.08, col=WHITE, acc=ORG, size=150, shadow=0.45, lead_col=WHITE, out=T("i2", "And") - 0.1)
    ui_word(f, "and yes, it's", "REAL", 470, t, T("i2", "And") - 0.1, col=(90, 230, 120), size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S1: beta-carotene — the orange pigment in carrots ----
def shot_S1(t, n):
    f = stage("emerald", (255, 214, 120), 540, 1000, 430); u = lt(t, "S1")
    tb = T("a1", "beta-carotene.") - 0.2; tp = T("a1", "The") - 0.1
    rot_comp(f, carrot_el(), 520, 1040 + 8 * math.sin(t * 2.5), -18, 1.45 * pin(t, SHOT["S1"]["start"] + 0.05, 0.35), 1.0, 0.35)
    if t >= tb:
        pts = []
        for i in range(22):
            ph = ((t - tb) * 0.55 + i / 22) % 1.0; a = i * 2.39996
            r_ = 120 + 360 * ph; pts.append((540 + r_ * math.cos(a), 1020 + r_ * math.sin(a) * 0.85))
        dots(f, pts, 13)
        rot_comp(f, tag_el("BETA-CAROTENE", YEL_, INK, 56), 560, 1420, -4, pin(t, tb + 0.1, 0.25), 1.0, 0.35)
    ui_word(f, "it's all because of", "BETA-CAROTENE", 470, t, SHOT["S1"]["start"] + 0.1, col=WHITE, acc=ORG, size=140, shadow=0.45, lead_col=WHITE, out=tp - 0.05)
    ui_word(f, "the orange", "PIGMENT", 470, t, tp, col=(255, 170, 60), size=220, shadow=0.45, lead_col=WHITE, tail="in carrots")
    return finish(f, n)


# ---- S2: body turns it into vitamin A — up to a limit ----
def shot_S2(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S2")
    tv = T("a2", "vitamin") - 0.15; tl = T("a2", "limit.") - 0.2
    comp(f, machine_el(), 430, 1090, scale=0.86 * pin(t, SHOT["S2"]["start"] + 0.03, 0.3))
    full = t >= tl
    pts = []
    for i in range(10):
        ph = ((u * 0.9 + i / 10) % 1.0)
        pts.append((430 + 50 * math.sin(i * 1.7), 640 + 220 * ph))
    dots(f, pts, 12)
    if full:
        rng = np.random.default_rng(4)
        pile = [(430 + rng.uniform(-110, 110), 840 - rng.uniform(0, 70) * clamp((t - tl) / 0.8)) for _ in range(int(16 * clamp((t - tl) / 0.8)) + 3)]
        dots(f, pile, 12)
    if t >= tv:
        for i in range(4):
            q = (t - tv) * 0.9 - i * 0.28
            if q > 0: comp(f, scale_el(capsule_el(), 0.8), 640 + 160 * min(q, 1.0), 1340 - 26 * i)
    lv = 0.8 * clamp((t - tv + 0.2) / max(0.4, tl - tv + 0.2))
    gauge_tube(f, 895, 760, 1300, lv + (0.03 * math.sin(t * 30) if full else 0))
    if full: slam(f, stamp_el("FULL!", RED_, 60), 880, 690, 8, t, tl + 0.05)
    ui_word(f, "your body turns it into", "VITAMIN A", 470, t, SHOT["S2"]["start"] + 0.1, col=INK, size=190, out=tl - 0.05)
    ui_word(f, "but only up to a", "LIMIT", 470, t, tl, col=RED_, size=230)
    return finish(f, n)


# ---- S3: the extra floats in your blood ----
def shot_S3(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 430); u = lt(t, "S3")
    vessel(f, 30, 1050, 1030, 150, t, 260, 12, 16 if u > 0.3 else int(16 * u / 0.3), 3)
    comp(f, chip("BLOOD VESSEL", INK, WHITE, 30), 540, 1260, scale=pin(t, SHOT["S3"]["start"] + 0.2, 0.25))
    comp(f, chip("extra beta-carotene", ORG, INK, 30), 540, 790, scale=pin(t, T("a3", "extra") + 0.1, 0.25))
    ui_word(f, "the extra floats in your", "BLOOD", 470, t, SHOT["S3"]["start"] + 0.1, col=RED_, size=230)
    return finish(f, n)


# ---- S3b: settles in the outer layer of your skin ----
def shot_S3b(t, n):
    f = stage("pink", (255, 236, 160), 540, 1000, 430); u = lt(t, "S3b")
    ts = T("a3", "settles") - 0.1
    k = ramp(t, ts, max(0.4, T("a3", "skin.") - ts))
    yb = skin_block(f, 540, 860, 760, k, 1.0)
    for i in range(10):
        q = (t - ts) * 1.2 - i * 0.1
        if 0 < q < 1: dots(f, [(220 + i * 66, 700 + (yb - 40 - 700) * eo(q))], 12)
    comp(f, chip("OUTER LAYER", INK, WHITE, 32), 540, 1380, scale=pin(t, T("a3", "outer") - 0.1, 0.25))
    cv2.arrowedLine(f, (540, 1350), (540, int(yb + 10)), C(INK), 8, cv2.LINE_AA, tipLength=0.08) if t >= T("a3", "outer") else None
    ui_word(f, "then it settles in your skin's", "OUTER LAYER", 470, t, SHOT["S3b"]["start"] + 0.1, col=WHITE, acc=ORG, size=160, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S4a: thick skin holds the most ----
def shot_S4a(t, n):
    f = stage("teal", (255, 214, 120), 540, 1000, 430); u = lt(t, "S4a")
    k = ramp(t, SHOT["S4a"]["start"] + 0.2, 0.7)
    skin_block(f, 300, 860, 330, 0.35 * k, 0.25)
    skin_block(f, 780, 860, 330, k, 1.4)
    comp(f, chip("THIN SKIN", INK, WHITE, 30), 300, 1340); comp(f, chip("THICK SKIN", ORG, INK, 30), 780, 1340)
    ui_word(f, "thick skin holds the", "MOST", 470, t, SHOT["S4a"]["start"] + 0.1, col=WHITE, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S4b: palms first ----
def shot_S4b(t, n):
    f = stage("purple", (255, 214, 120), 540, 1000, 430); u = lt(t, "S4b")
    tp = T("b1", "palms") - 0.1; k = ramp(t, tp, 0.6)
    if t >= tp: rays(f, 540, 1060, 700, (255, 190, 100), 0.4 * k, t)
    rot_comp(f, palm_el(k), 540, 1070, 4 * math.sin(t * 3), 1.12 * pin(t, SHOT["S4b"]["start"] + 0.02, 0.3), 1.0, 0.3)
    comp(f, chip("#1 PALMS", ORG, INK, 40), 540, 1462, scale=pin(t, tp + 0.2, 0.25))
    ui_word(f, "first, your", "PALMS", 470, t, SHOT["S4b"]["start"] + 0.08, col=WHITE, acc=ORG, size=230, shadow=0.45, lead_col=WHITE, tail="turn orange")
    return finish(f, n)


# ---- S4c: then your feet ----
def shot_S4c(t, n):
    f = stage("sky", (255, 214, 120), 540, 1000, 430); u = lt(t, "S4c")
    k = ramp(t, SHOT["S4c"]["start"] + 0.15, 0.5)
    rot_comp(f, sole_el(k), 420, 1060, -8, 1.0 * pin(t, SHOT["S4c"]["start"], 0.25), 1.0, 0.3)
    rot_comp(f, sole_el(k), 690, 1080, 8, 0.95 * pin(t, SHOT["S4c"]["start"] + 0.06, 0.25), 1.0, 0.3)
    comp(f, chip("#2 FEET", ORG, INK, 40), 540, 1462, scale=pin(t, SHOT["S4c"]["start"] + 0.3, 0.25))
    ui_word(f, "then your", "FEET", 470, t, SHOT["S4c"]["start"] + 0.05, col=WHITE, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S4d: even the tip of your nose ----
def shot_S4d(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S4d")
    tn = T("b1", "nose!") - 0.15; k = ramp(t, tn, 0.4)
    z = 2.3 + 0.15 * eo(clamp(u / 1.5))
    chub_head_only(f, 540, 1060, z, t, mouth=0 if t < tn else "o", expr="n" if t < tn else "wow", brow="up", look=(0, 1), tint=0.35, nose=k, blink=False)
    if t >= tn: ring(f, 540, 1060 + 25 * z, 60 + 30 * math.sin((t - tn) * 10), RED2, 9, clamp((t - tn) / 0.2))
    comp(f, chip("#3 NOSE", ORG, INK, 40), 540, 1462, scale=pin(t, tn + 0.15, 0.25))
    ui_word(f, "even the tip of your", "NOSE", 470, t, SHOT["S4d"]["start"] + 0.08, col=INK, acc=ORG, size=230)
    return finish(f, n)


# ---- S5: how many? about ten a day, for a few weeks ----
def shot_S5(t, n):
    f = stage("emerald", (255, 214, 120), 540, 1000, 430); u = lt(t, "S5")
    tt = T("c1", "ten") - 0.15; tw = T("c1", "weeks.") - 0.25
    if t < tt:
        chub(f, 540, 1460, 1.05, la=(20, 10), ra=(-150, -150), mouth=talk(t), brow="sus", expr="n", look=(1, -1), tint=0.2)
        comp(f, bubble_el("HOW MANY?", 50), 780, 820, scale=pin(t, SHOT["S5"]["start"] + 0.2, 0.3))
    else:
        chub(f, 230, 1460, 0.8, la=(20, 10), ra=(60, 40), mouth=talk(t), brow="up", expr="wow" if talk(t) == 0 else "n", look=(1, 0), tint=0.5)
        for i in range(10):
            c_, r_ = divmod(i, 5); x = 560 + c_ * 250; y = 760 + r_ * 110
            q = t - tt - 0.05 * i
            if q > 0: rot_comp(f, scale_el(carrot_el(), 0.38), x, y, 90, pin(t, tt + 0.05 * i, 0.2), 1.0, 0.2)
        if t >= tw: rot_comp(f, tag_el("FOR A FEW WEEKS", YEL_, INK, 46), 640, 1250, -4, pin(t, tw, 0.25), 1.0, 0.35)
    comp(f, chip("1 carrot ≈ 4 mg beta-carotene · Source: Cleveland Clinic", INK, WHITE, 22), 540, 1462, op=clamp((t - tt - 0.4) / 0.3))
    ui_word(f, "how many", "CARROTS?", 470, t, SHOT["S5"]["start"] + 0.1, col=WHITE, acc=ORG, size=210, shadow=0.45, lead_col=WHITE, out=tt - 0.05)
    ui_word(f, "doctors say about", "10 A DAY", 470, t, tt, col=YEL_, size=220, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S6: babies get it the most (mashed carrot) ----
def shot_S6(t, n):
    f = stage("sky", (255, 230, 150), 540, 1000, 430); u = lt(t, "S6")
    k = ramp(t, SHOT["S6"]["start"] + 0.4, 2.2)
    ph = (u / 0.9) % 1.0
    m = 2 if 0.45 < ph < 0.75 else 0
    baby(f, 540, 1440, 1.0, t, 0.85 * k, m, "happy")
    sx = 900 - 250 * math.sin(math.pi * min(ph / 0.6, 1.0)); sy = 1020 - 30 * math.sin(math.pi * min(ph / 0.6, 1.0))
    rot_comp(f, spoon_el(), sx, sy, 10, 0.8)
    comp(f, bowl_el(), 540, 1180, scale=0.62)
    ui_word(f, "babies get it", "THE MOST", 470, t, SHOT["S6"]["start"] + 0.1, col=WHITE, acc=ORG, size=210, shadow=0.45, lead_col=WHITE, tail="from mashed carrot")
    return finish(f, n)


# ---- S7: harmless — eat fewer and it fades ----
def shot_S7(t, n):
    f = stage("emerald", (255, 255, 255), 540, 1000, 430); u = lt(t, "S7")
    th = T("d1", "harmless.") - 0.2; te = T("d1", "Eat") - 0.1; tf = T("d1", "fades.") + 0.2
    fade = clamp((t - te) / max(0.5, tf - te))
    chub(f, 540, 1460, 1.05, la=(150, 170) if t < te else (20, 10), ra=(150, 170) if t < te else (60, 30), mouth=talk(t),
         brow="up", expr="happy" if talk(t) == 0 else "n", tint=1.0 - fade)
    if th <= t < te:
        comp(f, check_el(70, True), 540, 760, scale=pin(t, th, 0.25))
    if t >= te:
        for i in range(3):
            x = 220 + i * 60; y = 1430 - i * 30
            rot_comp(f, scale_el(carrot_el(), 0.32), x, y, 60, 1.0, 1.0 - 0.6 * fade, 0.2)
        cv2.line(f, (160, 1300), (360, 1500), C(RED2), 14, cv2.LINE_AA)
        comp(f, chip("weeks to months", INK, WHITE, 30), 820, 1000, scale=pin(t, te + 0.4, 0.25))
    ui_word(f, "the good news? it's", "HARMLESS", 470, t, SHOT["S7"]["start"] + 0.1, col=WHITE, acc=ORG, size=190, shadow=0.45, lead_col=WHITE, out=te - 0.05)
    ui_word(f, "eat fewer and the orange", "FADES", 470, t, te, col=YEL_, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S8: whites of the eyes stay white ----
def shot_S8(t, n):
    f = stage("purple", (255, 255, 255), 540, 1000, 430); u = lt(t, "S8")
    comp(f, eye2_el((255, 255, 255), CH_ORANGE), 540, 1040, scale=1.35 * pin(t, SHOT["S8"]["start"] + 0.03, 0.3))
    tw = T("d2", "whites") - 0.1
    if t >= tw:
        comp(f, check_el(56, True), 860, 820, scale=pin(t, tw, 0.25))
        comp(f, chip("whites stay WHITE", GRN_, WHITE, 34), 540, 1380, scale=pin(t, tw + 0.15, 0.25))
    ui_word(f, "carrots never turn your", "EYES YELLOW", 470, t, SHOT["S8"]["start"] + 0.12, col=WHITE, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S8b: yellow eyes? see a doctor ----
def shot_S8b(t, n):
    f = stage("red", (255, 230, 150), 540, 1000, 430); u = lt(t, "S8b")
    comp(f, eye2_el((250, 214, 40)), 540, 1030, scale=1.25 * pin(t, SHOT["S8b"]["start"] + 0.03, 0.3))
    td = T("d2", "see") - 0.15
    if t >= td: slam(f, stamp_el("SEE A DOCTOR", WHITE, 64), 540, 1330, -6, t, td)
    comp(f, chip("yellow eyes are a different problem, not carrots", INK, WHITE, 26), 540, 1462, op=clamp((u - 0.5) / 0.3))
    ui_word(f, "yellow eyes?", "SEE A DOCTOR", 470, t, SHOT["S8b"]["start"] + 0.1, col=YEL_, size=150, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S9: do carrots help you see in the dark? NOPE — a WWII story ----
def shot_S9(t, n):
    f = stage("purple"); u = lt(t, "S9")
    f *= 0.55; zzz_moon(f, t); moon(f, 800, 700, 130)
    tn = T("f1", "Nope!") - 0.15; tw = T("f1", "World") - 0.15
    sweep = 25 * math.sin(t * 2.2)
    chub(f, 520, 1460, 1.05, la=(20, 10), ra=(150, 175), mouth=0, brow="sus", expr="sus" if t < tn else "sad", look=(1, -1), tint=0.0,
         hold=scale_el(carrot_el(0), 0.45), hold_off=(0, -90), lean=sweep * 0.1, hold_front=True)
    if t >= tn:
        k = clamp((t - tn) / 0.12); ov = f.copy()
        cv2.line(ov, (300, 760), (780, 1400), C(RED2), 34, cv2.LINE_AA); cv2.line(ov, (780, 760), (300, 1400), C(RED2), 34, cv2.LINE_AA)
        f[:] = f * (1 - k) + ov * k
    if t >= tw: comp(f, chip("1940s", YEL_, INK, 40), 540, 1462, scale=pin(t, tw, 0.25))
    ui_word(f, "do carrots help you see in the", "DARK?", 470, t, SHOT["S9"]["start"] + 0.1, col=WHITE, size=220, shadow=0.45, lead_col=WHITE, out=tn - 0.05)
    ui_word(f, "", "NOPE!", 470, t, tn, col=RED_, size=250, shadow=0.45, out=tw - 0.05)
    ui_word(f, "it's a world war two", "STORY", 470, t, tw, col=YEL_, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S10: Britain said its night pilots ate loads of carrots ----
def shot_S10(t, n):
    f = stage("purple"); u = lt(t, "S10")
    f *= 0.6; zzz_moon(f, t); moon(f, 820, 720, 120)
    px = 400 + 140 * eo(clamp(u / 2.6)); py = 1080 + 14 * math.sin(t * 3)
    m, c = munch(t, 0.36)
    chub_head_only(f, px + 115, py - 160, 0.62, t, mouth=m, expr="happy", brow="up", cap=True)
    rot_comp(f, plane_el(), px, py, 0, 1.1, 1.0, 0.3)
    prop_disc(f, px + 400 * 1.1 - 2, py - 4, 120, t)
    tl = T("f2", "loads") - 0.15
    if t >= tl:
        for i in range(6):
            q = t - tl - 0.08 * i
            if q > 0:
                a = i * 1.05; rr = 250 + 40 * math.sin(t * 2 + i)
                rot_comp(f, scale_el(carrot_el(), 0.3), px + rr * math.cos(a), py - 100 + rr * math.sin(a) * 0.7, 40 * i + 50 * t, pin(t, tl + 0.08 * i, 0.2), 1.0, 0.2)
    ui_word(f, "britain said its night pilots ate", "LOADS OF CARROTS", 470, t, SHOT["S10"]["start"] + 0.1, col=WHITE, acc=ORG, size=130, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S10b: the real secret? RADAR ----
def shot_S10b(t, n):
    f = stage("emerald", (120, 255, 160), 540, 1050, 430); u = lt(t, "S10b")
    f *= 0.7
    tr = T("f2", "Radar!") - 0.2
    radar_screen(f, 540, 1050, 300 * pin(t, SHOT["S10b"]["start"] + 0.02, 0.3), t, t >= tr)
    if t >= tr: slam(f, stamp_el("TOP SECRET", RED_, 56), 540, 1430, -6, t, tr + 0.1)
    comp(f, chip("Source: Smithsonian Magazine", INK, WHITE, 22), 540, 1495 - 33, op=clamp((u - 0.3) / 0.3)) if t < tr + 0.1 else None
    ui_word(f, "the real secret?", "RADAR", 470, t, tr, col=(120, 255, 160), size=240, shadow=0.45, lead_col=WHITE)
    if t < tr: ui_word(f, "the real", "SECRET?", 470, t, SHOT["S10b"]["start"] + 0.08, col=WHITE, size=220, shadow=0.45, lead_col=WHITE, out=tr - 0.05)
    return finish(f, n)


# ---- S11: send it + FreshNestHub sting ----
def shot_S11(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S11")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("how many carrots today??", "only 12 lol", pr), 0.82), 620, 950, scale=pin(t, SHOT["S11"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (620, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        m, c = munch(t, 0.4)
        chub(f, 250, 1480, 0.8, la=(20, 10), ra=(148, -130), mouth=m, expr="happy", brow="up", tint=1.0,
             hold=carrot_side(0, 0.4), hold_off=(-30, 0), hold_front=True)
        ui_word(f, "send to the friend who eats carrots like a", "RABBIT", 400, t, T("e2", "friend") - 0.1, col=WHITE, acc=ORG, size=170, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=WHITE, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1480, 0.7, la=(20, 10), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="happy", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TO0, 0.4, 18), (T("i2", "real.") - 0.2, 0.3, 14), (T("a1", "beta-carotene.") - 0.2, 0.25, 10),
           (T("a2", "limit.") - 0.15, 0.35, 16), (T("a3", "settles") - 0.1, 0.2, 8), (T("b1", "palms") - 0.1, 0.3, 12),
           (T("b1", "nose!") - 0.15, 0.3, 14), (T("c1", "ten") - 0.15, 0.3, 14), (T("d1", "harmless.") - 0.2, 0.25, 10),
           (T("d2", "see") - 0.15, 0.3, 14), (T("f1", "Nope!") - 0.15, 0.4, 18), (T("f2", "Radar!") - 0.15, 0.4, 18)]


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
