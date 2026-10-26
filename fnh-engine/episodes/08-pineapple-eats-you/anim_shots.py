# ================= shots: FreshNestHub — "Pineapple is eating you back" (bromelain) =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "That") - 0.15, "punch"), ("S2", T("a1", "Pineapple") - 0.2, "whip"),
    ("S2b", T("a1", "break") - 0.15, "zoom"), ("S3", T("a2", "Your") - 0.2, "flash"), ("S3b", T("a2", "and") - 0.12, "punch"),
    ("S4", T("a3", "Then") - 0.2, "whip"), ("S4b", T("a3", "Ouch!") - 0.2, "flash"), ("S5", T("a4", "the", 1) - 0.12, "punch"),
    ("S6", T("b1", "This") - 0.2, "whip"), ("S7", T("c1", "But") - 0.2, "focus"), ("S8", T("d1", "Want") - 0.2, "whip"),
    ("S8b", T("d1", "Heat") - 0.15, "flash"), ("S9", T("d2", "That's") - 0.2, "whip"), ("S10", T("f1", "And") - 0.2, "zoom"),
    ("S10b", T("f2", "Gelatin") - 0.2, "whip"), ("S10c", T("f2", "and") - 0.12, "punch"), ("S11", T("f3", "Use") - 0.2, "whip"),
    ("S12", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
PY = (255, 214, 40)   # pineapple yellow accent
LIME = (150, 255, 120)


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


# ---- S0: hook — Chubby munches a pineapple wedge... the wedge grows teeth and bites back ----
TB0 = T("i1", "it's") - 0.15


def shot_S0(t, n):
    f = stage("sky", (255, 230, 120), 540, 980, 440)
    back = t >= TB0; k = ramp(t, TB0, 0.25)
    for i, (px, py, r) in enumerate(((190, 1450, -20), (890, 1460, 25), (300, 1500, 10), (790, 1505, -12))):
        rot_comp(f, scale_el(pine_ring_el(), 0.42), px, py, r + 20 * math.sin(t + i), 1.0, 1.0, 0.25)
    if not back:
        m, c = munch(t)
        chub(f, 540, 1440, 1.15, la=(20, 10), ra=(148, -130), mouth=m, brow="up", expr="happy",
             hold=scale_el(pine_wedge_el(False, 0, c % 2 == 1), 0.5), hold_off=(-34 - 6 * (c % 3), -10), bob=4 * math.sin(t * 15), hold_front=True)
    else:
        rays(f, 540, 1000, 760, (255, 240, 160), 0.5 * k, t)
        ch = 0.5 + 0.5 * math.sin((t - TB0) * 22)
        lunge = 30 * ch
        chub(f, 400 - 30 * k, 1440, 1.15, la=(150, 170), ra=(85, 60), mouth="o", brow="up", expr="wow", look=(1, 0), lean=-8 * k)
        rot_comp(f, pine_wedge_el(True, ch), 740 - lunge, 960, 10 - 14 * ch, 1.3 * pin(t, TB0, 0.22), 1.0, 0.35)
        comp(f, burst_el("CHOMP!", YEL_, INK, 52), 800, 720, scale=pin(t, TB0 + 0.08, 0.25))
    ui_word(f, "while you eat a", "PINEAPPLE", 470, t, T("i1", "eating") - 0.1, col=WHITE, acc=PY, size=180, shadow=0.45, lead_col=WHITE, out=TB0 - 0.05)
    ui_word(f, "it's eating you", "[BACK?!]", 470, t, TB0, col=WHITE, acc=PY, size=220, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S1: that stingy, tingly feeling — it's real ----
def shot_S1(t, n):
    f = stage("teal", (255, 230, 120), 540, 1000, 440); u = lt(t, "S1")
    tr = T("i2", "real!") - 0.2; tt = T("i2", "tingly") - 0.1
    z = 2.15 + 0.12 * eo(clamp(u / 2.5))
    chub_head_only(f, 540, 1080, z, t, mouth="o" if t > tr else talk(t), expr="wow" if t > tt else "n", brow="up", look=(0, 1), blink=False)
    zaps(f, 540, 1080, 112 * z + 30 * math.sin(t * 9), t, 10, amt=ramp(t, tt, 0.2))
    if t >= tr:
        slam(f, stamp_el("100% REAL", RED_, 70), 540, 1430, -6, t, tr)
    ui_word(f, "that stingy,", "TINGLY", 470, t, st_("S1") + 0.08, col=YEL_, size=220, shadow=0.45, lead_col=WHITE, tail="feeling in your mouth?", out=tr - 0.05)
    ui_word(f, "it's", "REAL!", 470, t, tr, col=WHITE, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2: pineapple is packed with bromelain — enzymes ----
def shot_S2(t, n):
    f = stage("purple", (120, 220, 255), 540, 1040, 450); u = lt(t, "S2")
    tb = T("a1", "bromelain.") - 0.2; te = T("a1", "enzymes") - 0.1
    sc = 0.95 * pin(t, st_("S2") + 0.03, 0.35)
    rot_comp(f, pineapple_el(), 540, 1080 + 8 * math.sin(t * 2.5), 3 * math.sin(t * 2), sc, 1.0, 0.35)
    if t >= tb:
        for i in range(8):
            q = clamp((t - tb - 0.06 * i) / 0.45)
            if q <= 0: continue
            a = i * 2 * math.pi / 8 + 0.4 * (t - tb)
            rr = 120 + 290 * eo(q)
            enzyme(f, 540 + rr * math.cos(a), 1080 + rr * math.sin(a) * 0.9, 0.62, t + i * 0.13, flip=math.cos(a) < 0, op=clamp(q * 3))
    if t >= te: rot_comp(f, tag_el("ENZYMES", ENZ, WHITE, 56), 560, 1450, -4, pin(t, te, 0.25), 1.0, 0.35)
    ui_word(f, "pineapple is packed with", "BROMELAIN", 470, t, st_("S2") + 0.1, col=YEL_, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2b: they break down protein ----
def shot_S2b(t, n):
    f = stage("emerald", (255, 230, 120), 540, 1000, 430); u = lt(t, "S2b")
    pts = [(120 + i * 84, 1020 + 40 * math.sin(i * 0.9 + t * 3)) for i in range(11)]
    tc = st_("S2b") + 0.35
    cuts = [2, 5, 8]
    # pieces drift apart after each cut
    segs = [(0, 2), (3, 5), (6, 8), (9, 10)]
    for si, (a, b) in enumerate(segs):
        k = clamp((t - tc - 0.25 * min(si, 2)) / 0.4)
        dx = (si - 1.5) * 60 * eo(k); dy = (si % 2 * 2 - 1) * 70 * eo(k)
        chain(f, [(p[0] + dx, p[1] + dy) for p in pts[a:b + 1]], 26, True, seed=a)
    for j, ci in enumerate(cuts):
        x = (pts[ci][0] + pts[ci + 1][0]) / 2; y = 1020
        app = clamp((t - st_("S2b") - 0.05 * j) / 0.25)
        enzyme(f, x, y - 150 + 30 * (1 - app), 0.7, t * 1.6 + j, op=app, rot=-90 if j % 2 else -70)
    if t >= tc: comp(f, burst_el("SNIP!", YEL_, INK, 44), 860, 760, scale=pin(t, tc, 0.22))
    comp(f, chip("PROTEIN = a chain of building blocks", INK, WHITE, 28), 540, 1300, op=clamp((u - 0.2) / 0.3))
    ui_word(f, "enzymes that break down", "PROTEIN", 470, t, st_("S2b") + 0.06, col=WHITE, acc=PY, size=220, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S3: your mouth's slimy mucus shield ----
def shot_S3(t, n):
    f = stage("sky", (255, 230, 150), 540, 1000, 430); u = lt(t, "S3")
    tissue(f, 540, 760, 900, t, 0.0, mh=80, th=330)
    ts = T("a2", "slimy") - 0.1
    if t >= ts:
        comp(f, chip("MUCUS SHIELD", (30, 150, 100), WHITE, 34), 540, 700, scale=pin(t, ts, 0.25))
        sparkles(f, [(160, 790), (470, 800), (860, 785)], t, 0.9)
    comp(f, chip("YOUR MOUTH", INK, WHITE, 30), 760, 1060, scale=pin(t, st_("S3") + 0.3, 0.25))
    chub(f, 230, 1470, 0.62, la=(20, 10), ra=(150, 175), mouth=talk(t), brow="up", expr="n", look=(1, -1))
    ui_word(f, "your mouth has a slimy layer of", "MUCUS", 470, t, st_("S3") + 0.1, col=LIME, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S3b: bromelain chews through it ----
def shot_S3b(t, n):
    f = stage("purple", (255, 230, 150), 540, 1000, 430); u = lt(t, "S3b")
    tc = T("a2", "chewing") - 0.25
    k = ramp(t, tc - 0.4, max(0.5, st_("S4") - tc + 0.2))
    gaps = tissue(f, 540, 760, 900, t, k, mh=80, th=330)
    for j, (hx, hs) in enumerate(HOLES):
        x = 540 - 450 + hx * 900
        app = clamp((t - st_("S3b") - 0.1 * j) / 0.3)
        enzyme(f, x + 8 * math.sin(t * 9 + j), 720 - 60 * (1 - app) + 30 * k, 0.6, t * 1.5 + j * 0.2, rot=-60 - 10 * math.sin(t * 6 + j), op=app)
    if k > 0.2:
        for j in range(6):
            ph = (t * 1.3 + j / 6) % 1.0
            cv2.circle(f, (int(140 + j * 160 + 30 * ph), int(700 - 160 * ph)), int(10 * (1 - ph)) + 2, C(MUCUS), -1, cv2.LINE_AA)
    ui_word(f, "and bromelain starts", "CHEWING", 470, t, st_("S3b") + 0.08, col=ENZ, size=210, shadow=0.45, lead_col=WHITE, tail="right through it")
    comp(f, chip("it breaks down the mouth's protective mucus", INK, WHITE, 26), 540, 1300, op=clamp((u - 0.6) / 0.3))
    return finish(f, n)


# ---- S4: then the acid hits the bare spots ----
def shot_S4(t, n):
    f = stage("teal", (255, 230, 150), 540, 1000, 430); u = lt(t, "S4")
    ta = T("a3", "acid") - 0.2; tb = T("a3", "bare") - 0.1
    sore = ramp(t, tb, 0.3)
    gaps = tissue(f, 540, 760, 900, t, 1.0, sore=sore, mh=80, th=330)
    for j, (hx, hs) in enumerate(HOLES):
        q = clamp((t - ta - 0.14 * j) / 0.6)
        if 0 < q < 1:
            x = 540 - 450 + hx * 900; y = 560 + 230 * q * q
            comp(f, scale_el(drop_el(), 0.95), x, y)
        if q >= 1:
            sp = clamp((t - ta - 0.14 * j - 0.6) / 0.4)
            if sp < 1: ring(f, 540 - 450 + hx * 900, 800, 30 + 60 * sp, (200, 240, 60), 6, 1 - sp)
    if t >= ta: comp(f, chip("pineapple juice: pH 3 to 4 (acidic) · Source: Live Science", INK, WHITE, 22), 540, 1462, op=clamp((t - ta) / 0.3))
    ui_word(f, "then the pineapple's", "ACID", 470, t, st_("S4") + 0.08, col=(200, 250, 70), size=240, shadow=0.45, lead_col=WHITE, tail="hits the bare spots")
    return finish(f, n)


# ---- S4b: OUCH! ...so while you chew the pineapple ----
def shot_S4b(t, n):
    f = stage("red", (255, 200, 120), 540, 1000, 440); u = lt(t, "S4b")
    tw = T("a4", "So") - 0.1
    if t < tw:
        hop = abs(math.sin(u * 9)) * 40
        chub(f, 540, 1450 - hop, 1.1, la=(148, -130), ra=(148, -130), mouth="o", brow="sad", expr="wow", look=(0, -1), squash=-0.5 + hop / 40)
        zaps(f, 540, 1450 - hop - 462, 190, t, 9, amt=1.0, col=(255, 250, 120), upper=True)
        comp(f, burst_el("OUCH!", YEL_, INK, 70), 540, 760, scale=pin(t, st_("S4b") + 0.05, 0.22))
    else:
        m, c = munch(t, 0.5)
        chub(f, 540, 1450, 1.1, la=(20, 10), ra=(148, -130), mouth=m, brow="sad", expr="sus" if m == 0 else "n", look=(1, 0),
             hold=scale_el(pine_wedge_el(False, 0, c % 2 == 1), 0.5), hold_off=(-34, -10), hold_front=True)
        zaps(f, 540, 1450 - 462, 180, t, 6, amt=0.7, upper=True)
        ui_word(f, "so while you chew the", "PINEAPPLE", 470, t, tw, col=WHITE, acc=PY, size=180, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S5: role reversal — the pineapple chews YOU ----
def shot_S5(t, n):
    f = stage("orange", (255, 236, 160), 540, 1000, 440); u = lt(t, "S5")
    ch = 0.5 + 0.5 * math.sin(u * 20)
    sh = 6 * math.sin(t * 40)
    rot_comp(f, pineapple_el(True, ch), 720 + sh, 1080, 4 * math.sin(t * 8), 1.02 * pin(t, st_("S5") + 0.02, 0.25), 1.0, 0.35)
    run = 30 * math.sin(t * 18)
    chub(f, 250 - 40 * eo(clamp(u / 1.5)), 1470, 0.62, la=(150, 175), ra=(150, 175), ll=6 + run, rl=6 - run, mouth="o", brow="up", expr="wow", look=(1, 0), bob=-10 * abs(math.sin(t * 18)))
    ui_word(f, "the pineapple", "[CHEWS YOU!]", 470, t, st_("S5") + 0.05, col=WHITE, acc=YEL_, size=200, shadow=0.5, lead_col=WHITE)
    return finish(f, n)


# ---- S6: so strong it tenderizes tough meat ----
def shot_S6(t, n):
    f = stage("cream", (255, 214, 120), 540, 1000, 430); u = lt(t, "S6")
    ts = T("b1", "strong,") - 0.15; tg = T("b1", "tough") - 0.15; tt = T("b1", "tender.") - 0.2
    wob = ramp(t, tt, 0.3)
    sx = 1 + 0.05 * wob * math.sin(t * 18); sy = 1 - 0.05 * wob * math.sin(t * 18)
    pm, a = steak_el(False); hh, ww = a.shape; s_ = 1.45 * pin(t, st_("S6") + 0.03, 0.3)
    el = (cv2.resize(pm, (max(2, int(ww * s_ * sx)), max(2, int(hh * s_ * sy)))), cv2.resize(a, (max(2, int(ww * s_ * sx)), max(2, int(hh * s_ * sy)))))
    comp(f, el, 480, 1060)
    for j in range(2): rot_comp(f, scale_el(pine_ring_el(), 0.42), 380 + 190 * j, 980 + 10 * j, 15 * j, pin(t, st_("S6") + 0.2 + 0.1 * j, 0.25), 1.0, 0.3)
    for j in range(4):
        app = clamp((t - ts - 0.08 * j) / 0.25)
        enzyme(f, 300 + 120 * j, 1080 + 20 * math.sin(j), 0.5, t * 1.4 + j, rot=-30 + 20 * j, op=app)
    chub(f, 880, 1480, 0.62, la=(150, 170) if t >= ts else (20, 10), ra=(150, 170) if t >= ts else (60, 30), mouth=talk(t), brow="up", expr="happy" if talk(t) == 0 else "n")
    if tg <= t < tt: slam(f, stamp_el("TOUGH", (120, 70, 40), 60), 480, 1300, -6, t, tg)
    if t >= tt:
        slam(f, stamp_el("TENDER!", GRN_, 64), 480, 1300, -6, t, tt)
        sparkles(f, [(300, 960), (640, 930), (520, 1150)], t)
    comp(f, chip("Sources: Live Science · Institute of Food Technologists", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.4) / 0.3))
    ui_word(f, "this enzyme is so", "STRONG", 470, t, st_("S6") + 0.1, col=RED_, size=220, out=tg - 0.05)
    ui_word(f, "it's used to make tough meat", "TENDER", 470, t, tg, col=GRN_, size=220)
    return finish(f, n)


# ---- S7: don't panic — your mouth fixes itself fast ----
def shot_S7(t, n):
    f = stage("emerald", (255, 230, 150), 540, 1000, 430); u = lt(t, "S7")
    tfx = T("c1", "fixes") - 0.15; tfd = T("c1", "fades") - 0.15
    heal = ramp(t, tfx, max(0.6, tfd - tfx + 0.2))
    tissue(f, 540, 790, 900, t, 1.0, sore=1 - heal, heal=heal, mh=80, th=250)
    if t >= tfx:
        sparkles(f, [(540 - 450 + hx * 900, 810) for hx, _ in HOLES], t, 0.9)
    if t >= tfd: comp(f, check_el(56, True), 900, 1180, scale=pin(t, tfd, 0.25))
    calm = t >= tfx
    chub(f, 420, 1470, 0.78, la=(20, 10) if calm else (150, 175), ra=(150, 170) if calm else (150, 175), mouth=talk(t), brow="up" if calm else "sad",
         expr="happy" if calm and talk(t) == 0 else ("n" if calm else "wow"), look=(1, -1))
    ui_word(f, "but don't", "PANIC", 470, t, st_("S7") + 0.15, col=WHITE, size=230, shadow=0.45, lead_col=WHITE, out=tfx - 0.05)
    ui_word(f, "your mouth fixes itself", "FAST", 470, t, tfx, col=YEL_, size=240, shadow=0.45, lead_col=WHITE, out=tfd - 0.05)
    ui_word(f, "and the sting", "FADES", 470, t, tfd, col=LIME, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S8: want pineapple with no sting? ----
def shot_S8(t, n):
    f = stage("sky", (255, 230, 120), 540, 1000, 430); u = lt(t, "S8")
    chub(f, 470, 1470, 1.05, la=(20, 10), ra=(-150, -150), mouth=talk(t), brow="sus", expr="n", look=(1, -1),
         hold_l=scale_el(pine_ring_el(), 0.45), hold_off=(0, 0))
    comp(f, bubble_el("HOW?", 56), 800, 830, scale=pin(t, st_("S8") + 0.25, 0.3))
    ui_word(f, "want pineapple with", "NO STING?", 470, t, st_("S8") + 0.1, col=WHITE, acc=PY, size=200, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S8b: heat switches bromelain off ----
def shot_S8b(t, n):
    f = stage("purple", (255, 150, 60), 540, 1050, 430); u = lt(t, "S8b")
    to = T("d1", "off.") - 0.25
    grill(f, 540, 1150, 640, t)
    rot_comp(f, scale_el(pine_ring_el(t >= to), 1.0), 540, 1080, 0, 1.0, 1.0, 0.0)
    steam(f, 540, 980, t, 1.1, 0.5)
    for j in range(4):
        x = 400 + 95 * j
        if t < to:
            enzyme(f, x, 940 + 10 * math.sin(t * 12 + j), 0.5, t * 2 + j, rot=-90, flip=j % 2 == 1)
        else:
            q = clamp((t - to - 0.06 * j) / 0.7)
            rot_comp(f, scale_el(enzyme_el(0, True), 0.5), x + (j - 1.5) * 120 * q, 940 - 120 * q + 520 * q * q, 200 * q * (1 if j % 2 else -1), 1.0, 1 - clamp((q - 0.7) / 0.3), 0.2)
    if t >= to: slam(f, stamp_el("SWITCHED OFF", WHITE, 56), 540, 1430, -5, t, to)
    ui_word(f, "heat switches bromelain", "OFF", 470, t, st_("S8b") + 0.06, col=(255, 150, 60), size=250, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S9: grilled or canned pineapple feels fine ----
def shot_S9(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S9")
    tg = T("d2", "grilled") - 0.15; tc = T("d2", "canned") - 0.15; tf = T("d2", "totally") - 0.15
    if t >= tg: rot_comp(f, scale_el(pine_ring_el(True), 0.85), 260, 820, 8 * math.sin(t * 2), pin(t, tg, 0.25), 1.0, 0.35)
    if t >= tg: comp(f, chip("GRILLED", INK, WHITE, 34), 260, 990, scale=pin(t, tg + 0.1, 0.25))
    if t >= tc: rot_comp(f, can_el(), 830, 830, -6 * math.sin(t * 2), 0.8 * pin(t, tc, 0.25), 1.0, 0.35)
    if t >= tc: comp(f, chip("CANNED", INK, WHITE, 34), 830, 1010, scale=pin(t, tc + 0.1, 0.25))
    m, c = munch(t, 0.42)
    chub(f, 540, 1470, 0.95, la=(20, 10), ra=(148, -130), mouth=m, brow="up", expr="happy",
         hold=scale_el(pine_wedge_el(False, 0, c % 2 == 1), 0.48), hold_off=(-30, -10), hold_front=True)
    if t >= tf: comp(f, check_el(60, True), 760, 1150, scale=pin(t, tf, 0.25))
    if t < tf: ui_word(f, "that's why grilled or", "CANNED", 470, t, st_("S9") + 0.1, col=INK, acc=RED_, size=220, out=tf - 0.05)
    ui_word(f, "they feel", "TOTALLY FINE", 470, t, tf, col=GRN_, size=180)
    return finish(f, n)


# ---- S10: weird bonus — fresh pineapple ruins jelly ----
def shot_S10(t, n):
    f = stage("pink", (255, 236, 170), 540, 1000, 430); u = lt(t, "S10")
    tfr = T("f1", "fresh") - 0.15; tr = T("f1", "ruins") - 0.2
    melt = ramp(t, tr, 0.9)
    jelly(f, 600, 1260, 1.0, t, wob=1.0 - melt, melt=melt)
    for j in range(3):
        q = clamp((t - tfr - 0.12 * j) / 0.5)
        if 0 < q:
            x = 500 + 100 * j; y = 640 + (1000 + 40 * j - 640) * q * q
            rot_comp(f, scale_el(pine_wedge_el(), 0.3), x, y if q < 1 else 1000 + 40 * j + (1225 - 1000 - 40 * j) * melt, 40 * j + 200 * q, 1.0, 1.0, 0.2)
    chub(f, 200, 1480, 0.62, la=(20, 10) if t < tr else (150, 175), ra=(60, 30) if t < tr else (150, 175), mouth=talk(t) if t < tr else "o",
         brow="up", expr="happy" if t < tr else "wow", look=(1, 0))
    ui_word(f, "here's a weird", "BONUS", 470, t, st_("S10") + 0.08, col=WHITE, acc=PY, size=230, shadow=0.45, lead_col=WHITE, out=tfr - 0.05)
    ui_word(f, "fresh pineapple ruins", "JELLY", 470, t, tfr, col=WHITE, acc=PY, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S10b: gelatin is a protein too — bromelain cuts the net ----
def shot_S10b(t, n):
    f = stage("teal", (255, 236, 170), 540, 1000, 430); u = lt(t, "S10b")
    tb = T("f2", "breaks") - 0.2
    cut = ramp(t, tb, 0.7)
    gel_net(f, 540, 1000, 760, 520, t, cut)
    for j in range(4):
        x = 280 + 170 * j + 30 * math.sin(t * 3 + j); y = 800 + 120 * (j % 2) + 30 * math.cos(t * 2.5 + j)
        app = clamp((t - st_("S10b") - 0.3 - 0.1 * j) / 0.3)
        enzyme(f, x, y, 0.62, t * 1.6 + j, rot=20 * math.sin(t * 4 + j), flip=j % 2 == 1, op=app)
    comp(f, chip("GELATIN = PROTEIN STRANDS", INK, WHITE, 30), 540, 1350, scale=pin(t, st_("S10b") + 0.25, 0.25))
    ui_word(f, "gelatin is a", "PROTEIN TOO", 470, t, st_("S10b") + 0.08, col=WHITE, acc=PY, size=180, shadow=0.45, lead_col=WHITE, out=tb - 0.05)
    ui_word(f, "so bromelain", "BREAKS IT", 470, t, tb, col=ENZ, size=200, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S10c: the jelly never sets ----
def shot_S10c(t, n):
    f = stage("sky", (255, 236, 170), 540, 1000, 430); u = lt(t, "S10c")
    jelly(f, 600, 1260, 1.0, t, 0, 1.0)
    for j in range(3): rot_comp(f, scale_el(pine_wedge_el(), 0.3), 500 + 100 * j, 1225, 40 * j, 1.0, 1.0, 0.0)
    tn = T("f2", "never") - 0.15
    drip = (u * 1.3) % 1.0
    chub(f, 230, 1480, 0.7, la=(20, 10), ra=(70, 40), mouth=talk(t), brow="sad", expr="sad", look=(1, 1),
         hold=scale_el(spoon_el(), 0.55), hold_off=(60, 0))
    cv2.circle(f, (int(370), int(1150 + 200 * drip)), 9, C(JELLY), -1, cv2.LINE_AA)
    if t >= tn: slam(f, stamp_el("NEVER SETS", RED_, 64), 620, 980, -6, t, tn)
    ui_word(f, "and the jelly", "NEVER SETS", 470, t, st_("S10c") + 0.06, col=WHITE, acc=PY, size=200, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S11: canned pineapple -> it wobbles perfectly ----
def shot_S11(t, n):
    f = stage("emerald", (255, 236, 170), 540, 1000, 430); u = lt(t, "S11")
    tw = T("f3", "wobbles") - 0.2
    rot_comp(f, can_el(), 230, 950, -8, 0.7 * pin(t, st_("S11") + 0.05, 0.25), 1.0, 0.35)
    wob = 0.3 + 1.4 * math.exp(-max(0, t - tw) * 2.2) if t >= tw else 0.3
    jelly(f, 640, 1250, 0.95, t, wob=wob, melt=0.0, rings=True)
    poke = t >= tw and t < tw + 0.3
    chub(f, 870, 1480, 0.62, la=(70 if poke else 30, 40 if poke else 20), ra=(150, 170), mouth="o" if poke else talk(t), brow="up", expr="happy", look=(-1, 0))
    if t >= tw: sparkles(f, [(500, 960), (780, 1000), (640, 900)], t)
    ui_word(f, "use", "CANNED", 470, t, st_("S11") + 0.08, col=YEL_, size=230, shadow=0.45, lead_col=WHITE, tail="pineapple instead", out=tw - 0.05)
    ui_word(f, "and it", "WOBBLES!", 470, t, tw, col=WHITE, acc=PY, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S12: send it + FreshNestHub sting ----
def shot_S12(t, n):
    f = stage("yellow", (255, 255, 255), 540, 880, 420); u = lt(t, "S12")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("pineapple for dessert?", "my tongue is STILL tingling", pr), 0.82), 620, 950, scale=pin(t, st_("S12")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (620, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        m, c = munch(t, 0.45)
        chub(f, 250, 1480, 0.8, la=(20, 10), ra=(148, -130), mouth=m, expr="happy", brow="up",
             hold=scale_el(pine_wedge_el(False, 0, c % 2 == 1), 0.42), hold_off=(-30, -8), hold_front=True)
        zaps(f, 250, 1480 - 336, 150, t, 6, amt=0.6, upper=True)
        ui_word(f, "send to the friend whose mouth", "HURTS", 420, t, T("e2", "friend") - 0.1, col=RED_, size=190, tail="after every pineapple")
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INK, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1480, 0.7, la=(20, 10), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="happy", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TB0, 0.45, 20), (T("i2", "tingly") - 0.1, 0.25, 10), (T("i2", "real!") - 0.2, 0.3, 14), (T("a1", "bromelain.") - 0.2, 0.3, 12),
           (T("a1", "break") + 0.2, 0.25, 10), (T("a2", "chewing") - 0.25, 0.3, 12), (T("a3", "bare") - 0.1, 0.3, 12),
           (T("a3", "Ouch!") - 0.15, 0.45, 22), (T("a4", "chews") - 0.15, 0.4, 18), (T("b1", "strong,") - 0.15, 0.25, 10),
           (T("b1", "tender.") - 0.2, 0.3, 14), (T("c1", "fades") - 0.15, 0.2, 8), (T("d1", "Heat") - 0.15, 0.3, 12),
           (T("d1", "off.") - 0.25, 0.35, 16), (T("d2", "totally") - 0.15, 0.2, 8), (T("f1", "ruins") - 0.2, 0.4, 18),
           (T("f2", "breaks") - 0.2, 0.3, 14), (T("f2", "never") - 0.15, 0.35, 16), (T("f3", "wobbles") - 0.2, 0.3, 12)]


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
