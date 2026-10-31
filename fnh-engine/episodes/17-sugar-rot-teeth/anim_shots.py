# ================= shots: FreshNestHub 17 — "Does sugar rot your teeth?" (first Chubby INK episode) =================
# COLOUR SCRIPT (ep 17, 5-colour ink palette + ONE accent): paper white = the tooth / enamel; VIOLET accent = sugar, the bacteria city,
# acid (the whole threat is one colour); MINT = saliva, repair, the healthy fix; ink + paper everywhere else. Places are lit but softened
# toward paper (inkify): Halloween porch (hook, plan), bathroom mirror (plaque, brushing), kitchen (eating), paper stages for diagrams.
# CRAFT (ep 17): STAGING + SILHOUETTE - every Chubby pose was checked as a black shape (tools/ink_sheet.py): arms clear of the body,
# asymmetry, a lean; one focal point per shot (spotlight / lights-drop when the voice confides); acting kit: double_take, flinch, POSE.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Something") - 0.2, "punch"), ("S1b", T("i2", "living") - 0.2, "zoom"),
    ("S2", T("i3", "Stick") - 0.2, "whip"),
    ("S3", T("a1", "So") - 0.2, "whip"), ("S3b", T("a1", "Your") - 0.15, "zoom"), ("S4", T("a2", "Plaque") - 0.2, "iris"),
    ("S5", T("a3", "They") - 0.2, "whip"), ("S5b", T("a3", "But") - 0.15, "punch"),
    ("S6", T("a4", "You") - 0.2, "flash"), ("S6b", T("a4", "And") - 0.15, "zoom"),
    ("S7", T("a5", "That") - 0.2, "whip"), ("S7b", T("a5", "Enamel") - 0.15, "focus"),
    ("S8", T("a6", "Lose") - 0.2, "whip"), ("S8b", T("a6", "That") - 0.15, "punch"),
    ("S9", T("b1", "But") - 0.2, "flash"), ("S10", T("b2", "It's") - 0.2, "whip"),
    ("S11", T("b3", "Saliva") - 0.2, "whip"), ("S11b", T("b3", "carries") - 0.15, "zoom"),
    ("S12", T("b4", "So") - 0.2, "whip"), ("S12b", T("b4", "The") - 0.15, "punch"),
    ("S13", T("b5", "An") - 0.2, "flash"),
    ("S14", T("c1", "Which") - 0.2, "focus"), ("S14b", T("c1", "The") - 0.15, "punch"),
    ("S15", T("c2", "Every") - 0.2, "whip"), ("S16", T("c3", "One") - 0.2, "whip"), ("S17", T("c4", "Three") - 0.2, "punch"),
    ("S18", T("c5", "But") - 0.2, "flash"), ("S18b", T("c5", "Your") - 0.15, "zoom"),
    ("S19", T("c6", "So") - 0.2, "whip"), ("S19b", T("c6", "Dentists") - 0.15, "punch"),
    ("S20", T("d1", "Okay.") - 0.2, "flash"), ("S21", T("d2", "Chewy") - 0.2, "whip"), ("S21b", T("d2", "So") - 0.15, "zoom"),
    ("S22", T("d3", "Sour") - 0.2, "whip"), ("S23", T("d4", "And") - 0.2, "whip"), ("S23b", T("d4", "Dentists") - 0.15, "punch"),
    ("S24", T("e1", "So,") - 0.2, "flash"), ("S25", T("e2", "Eat") - 0.2, "whip"), ("S25b", T("e2", "Then") - 0.15, "zoom"),
    ("S26", T("e3", "If") - 0.2, "whip"), ("S26b", T("e3", "The") - 0.15, "focus"),
    ("S27", T("e4", "Brush") - 0.2, "whip"), ("S27b", T("e4", "And") - 0.15, "punch"),
    ("S28", T("f1", "Quick") - 0.2, "flash"), ("S29", T("f2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {"S4": (540, 1000)}
SRC_T = "Source: Temple University · California Dental Association"
SRC_N = "Source: NIDCR (NIH) · NHS"


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC, size=170, y=470, out=None, tail="", dark=False):
    """ink caption: warm-ink text on paper sets, white with shadow on dark sets."""
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def ichip(text, size=26, inv=False): return chip(text, INKC if not inv else TOOTHW, TOOTHW if not inv else INKC, size)


def t3(f, text, y, t, t0, size=260, face=ACC_L, side=ACC_S, x=540):
    """3D title in the accent (drawn BEFORE Chubby / the hero)."""
    if t >= t0: title3d(f, text, y, t, t0, size=size, face=face, side=side, depth=22, x=x)


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def crumbs(f, x, y, t, t0, n=8, seed=3, dur=0.9, dx=0.0, dy=260.0):
    """violet sugar crumbs falling from (x, y) with gravity."""
    q = t - t0
    if q < 0 or q > dur: return
    rng = np.random.default_rng(seed)
    for i in range(n):
        k = clamp((q - i * 0.05) / (dur - i * 0.05 + 1e-3))
        if k <= 0: continue
        px = x + rng.uniform(-40, 40) + dx * k; py = y + dy * k * k + 20 * k
        cv2.circle(f, (int(px), int(py)), 7, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (int(px), int(py)), 7, C(INKC), 2, cv2.LINE_AA)


def sweat_drops(f, x, y, t, n=3):
    for i in range(n):
        q = (t * 1.6 + i * 0.37) % 1.0
        cv2.ellipse(f, (int(x + 40 + 16 * i), int(y - 30 + 60 * q)), (8, 13), 0, 0, 360, C((150, 210, 240)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x + 40 + 16 * i), int(y - 30 + 60 * q)), (8, 13), 0, 0, 360, C(INKC), 2, cv2.LINE_AA)


TOOTH_BIG = 1.35
TBITE = T("i1", "sugar") - 0.05; TROT = T("i1", "rot") - 0.08; TQ = T("i1", "teeth?") + 0.1


# ---- S0: HOOK — Halloween porch, Chubby bites a sweet (already moving at frame 0); a big tooth beside him CRACKS on 'rot' ----
def shot_S0(t, n):
    f = set_porch(t)
    crack = ramp(t, TROT, 0.35)
    t3(f, "ROT?", 640, t, TROT, 300, ACC_L, ACC_S)
    comp(f, scale_el(pail_el(), 0.85), 250, 1420 + 3 * math.sin(t * 3))
    m, c = munch(t, 0.4)
    if t < TBITE:
        chub(f, 440, 1500, 1.1, t=t, la=(40, 30), ra=(140, -128), mouth="o", expr="happy", brow="up", look=(0.6, 0.4),
             hold=scale_el(candy_el("wrap"), 0.55), hold_off=(-10, -50), hold_front=True)
    elif t < TROT:
        chub(f, 440, 1500, 1.1, t=t, la=(40, 30), ra=(60, 40), mouth=m, expr="happy", brow="up", look=(0.8, 0.1), bob=3 * math.sin(t * 14))
        crumbs(f, 480, 1050, t, TBITE + 0.05, 7, 3, 0.8, 200, 300)
    else:
        lean, sq = flinch(t, TROT, 0.8)
        chub(f, 440, 1500, 1.1, t=t, **POSE["shock"], mouth="o", expr="wow", brow="up", look=(0.9, 0.0), squash=sq)
    tooth = tooth_el("happy" if t < TROT - 0.1 else "ouch", 0.0, crack, False, False, False, (-0.6, 0.0))
    rot_comp(f, tooth, 790, 1150, 4 * math.sin(t * 2) if t < TROT else 10 * settle(t, TROT, 1.0, 14, 5), TOOTH_BIG, 1.0, 0.35)
    if t >= TROT:
        for i in range(4):
            q = t - TROT - 0.1 * i
            if 0 < q < 0.8: comp(f, scale_el(acid_drop_el(), 0.5), 790 - 60 + 40 * i, 1060 + 260 * q * q)
    if TBITE <= t < TROT: comp(f, ichip("SUGAR", 30), 640, 980, scale=pin(t, TBITE, 0.25))
    icap(f, "sugar doesn't actually", "[ROT] your teeth?", t, 0.12, acc=ACC, size=150, dark=True, out=TROT - 0.05)
    icap(f, "", "ROT YOUR TEETH?", t, TQ, acc=ACC, size=130, dark=True) if t >= TQ else None
    f = cam(f, 1 + 0.025 * clamp(t / 3.5), 600, 1150)
    return finish(f, n, look="warm")


# ---- S1: 'Something else does' — three bugs peek out from behind the cracked tooth (one holds an acid drop) ----
def shot_S1(t, n):
    f = set_porch(t); u = lt(t, "S1")
    f = cam(f, 1.35, 790, 1100)
    tooth = tooth_el("sus", 0.0, 1.0, False, False, False, (0.6, 0.3))
    rot_comp(f, tooth, 560, 1060, 0, 1.7, 1.0, 0.35)
    for i, (dx, dy, md) in enumerate(((250, -40, "happy"), (-260, 40, "hungry"), (210, 190, "love"))):
        k = pin(t, st_("S1") + 0.1 + 0.18 * i, 0.3)
        comp(f, scale_el(bug_el(md, (-0.6 if dx > 0 else 0.6, 0), 1 + i), 1.05), 560 + dx * (0.55 + 0.45 * k), 1060 + dy + 5 * math.sin(t * 6 + i), scale=k)
    comp(f, scale_el(acid_drop_el(), 0.6), 840, 1180, scale=pin(t, st_("S1") + 0.6, 0.3))
    icap(f, "something", "[ELSE] does", t, st_("S1") + 0.08, acc=ACC, size=190, dark=True)
    return finish(f, n, look="warm")


# ---- S1b: '...living in your mouth right now' — Chubby face close-up, mouth open, bugs waving from inside ----
def shot_S1b(t, n):
    f = ink_set("violet", (230, 210, 250), 540, 980, 420)
    tr = T("i2", "right") - 0.1
    t3(f, "RIGHT NOW", 1360, t, tr, 200, ACC_L, ACC_S)
    chub_head_only(f, 540, 820, 2.6, t, mouth="o", expr="wow", brow="up", look=(0, 0.6))
    my = 820 + 71 * 2.6
    for i, (dx, md) in enumerate(((-22, "happy"), (18, "love"), (0, "hungry"))):
        k = pin(t, st_("S1b") + 0.15 + 0.12 * i, 0.3)
        comp(f, scale_el(bug_el(md, (0, -0.5), 2 + i), 0.5 * k), 540 + dx * 2.6 * 0.5, my + 6 - 10 * k + 3 * math.sin(t * 7 + i))
    icap(f, "it's living in your mouth", "[RIGHT NOW]", t, st_("S1b") + 0.05, acc=ACC_XL, size=130, dark=True, out=tr - 0.05)
    return finish(f, n, look="night")


# ---- S2: OPEN LOOP — three covered lumps on a podium under a spotlight; 'the kindest candy is the one you'd guess is worst' ----
def shot_S2(t, n):
    f = ink_set("dusk_v", None); f *= 0.75
    podium(f, 620, 1250, 560, 110, t)
    for i, x in enumerate((470, 620, 770)): cloth(f, x, 1250, 130, 110 + 30 * (i % 2), t + i, 0.0)
    spotlight(f, 620, 1150, 330, 0.55, 200)
    god_rays(f, 620, 250, t, (240, 220, 255), 0.22, 7, 1000, 0.5, 1.57, 3)
    tk = T("i3", "kindest") - 0.1; tw = T("i3", "worst.") - 0.15
    chub(f, 230, 1500, 0.95, t=t, **POSE["think"], mouth=talk(t), expr="sus", brow="sus", look=(1, -0.2))
    comp(f, ichip("COMING UP", 32), 620, 900, scale=pin(t, st_("S2") + 0.3, 0.25))
    if t >= tk: comp(f, chip("KINDEST", INK_MINT, TOOTHW, 30), 470, 1060, scale=pin(t, tk, 0.25))
    if t >= tw: comp(f, chip("WORST?", ACC, TOOTHW, 30), 770, 1060, scale=pin(t, tw, 0.25))
    icap(f, "stick around for the candy that's", "[KINDEST] to your teeth", t, st_("S2") + 0.1, acc=INK_MINT, size=120, dark=True)
    return finish(f, n, look="night")


# ---- S3: PART 1 — bathroom mirror: 'who's the real culprit?' Chubby points at his own teeth ----
def shot_S3(t, n):
    f = set_bathroom(t)
    chub(f, 540, 1500, 1.1, t=t, la=(30, 16), ra=(150, -118), mouth=talk(t), expr="sus", brow="sus", look=(0.2, -0.5), lean=4)
    comp(f, ichip("?", 48), 760, 760, scale=pin(t, st_("S3") + 0.2, 0.3) * (1 + 0.05 * math.sin(t * 6)))
    chapter_card(f, t, st_("S3") + 0.05, 1, "THE CULPRIT", y=1440, dur=1.6, col=ACC_L)
    icap(f, "so who's the real", "[CULPRIT]?", t, st_("S3") + 0.08, acc=ACC, size=190)
    return finish(f, n, look="fresh")


# ---- S3b: inside the mouth — a row of teeth; a sticky violet film creeps over them -> PLAQUE ----
def shot_S3b(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440)
    tf = T("a1", "film") - 0.15; tp = T("a1", "plaque.") - 0.15
    k = ramp(t, tf, max(0.4, tp - tf))
    t3(f, "PLAQUE", 640, t, tp, 260, ACC_L, ACC_S)
    teeth_row(f, 540, 1150, 5, 0.75, k, t)
    if t >= tp: label_at(f, "PLAQUE = a sticky film of bacteria", 540, 1420, t, tp, 600, 1120, bg=ACC_S, fg=TOOTHW, size=28)
    icap(f, "your teeth wear a thin, sticky", "[FILM]", t, st_("S3b") + 0.05, acc=ACC, size=200, out=tp - 0.05)
    return finish(f, n, look="fresh")


# ---- S4: 'a tiny city of bacteria' — iris into the film: a crowd of bugs with tiny ink houses ----
def shot_S4(t, n):
    f = ink_set("violet", (230, 210, 250), 540, 1000, 440)
    tc = T("a2", "city") - 0.1
    t3(f, "TINY CITY", 640, t, tc, 230, ACC_L, ACC_S)
    for i, (x, y, w_, h_) in enumerate(((200, 1180, 120, 140), (420, 1210, 150, 170), (700, 1190, 130, 150), (900, 1220, 110, 130))):   # ink houses
        pts = np.array([(x - w_ / 2, y), (x - w_ / 2, y - h_), (x, y - h_ - 60), (x + w_ / 2, y - h_), (x + w_ / 2, y)], np.int32)
        cv2.fillPoly(f, [pts], C(ACC_XL), cv2.LINE_AA); cv2.polylines(f, [pts], True, C(INKC), 6, cv2.LINE_AA)
        cv2.rectangle(f, (int(x - 18), int(y - 60)), (int(x + 18), int(y)), C(ACC_S), -1, cv2.LINE_AA)
    bug_crowd(f, 540, 1100, t, 12, 0.7, "n", 420, 5, (0, 0))
    comp(f, ichip("BACTERIA", 34), 540, 1400, scale=pin(t, st_("S4") + 0.4, 0.3))
    icap(f, "plaque is basically a", "[TINY CITY]", t, st_("S4") + 0.05, acc=ACC_XL, size=150, dark=True, out=tc - 0.05)
    return finish(f, n, look="night")


# ---- S5: 'they can't chew through your teeth' — two bugs bounce off the tooth (clang), the tooth smirks ----
def shot_S5(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440); u = lt(t, "S5")
    tooth = tooth_el("smirk" if u > 0.5 else "n", 0.0, 0.0, False, False, False, (0, 0))
    comp(f, tooth, 540, 1060, scale=TOOTH_BIG)
    for i, (sgn, ph) in enumerate(((-1, 0.0), (1, 0.4))):
        q = ((u + ph) * 1.6) % 1.0
        x = 540 + sgn * (330 - 180 * math.sin(math.pi * q)); y = 1120 + 20 * (i - 0.5)
        hit = q > 0.45 and q < 0.55
        comp(f, scale_el(bug_el("angry" if not hit else "ouch", (-sgn, 0), 1 + i), 0.9), x, y, scale=1 + 0.2 * (1 if hit else 0))
        if hit: sparkles(f, x + sgn * -40, y - 40, t, t - 0.01, 6, 70, (255, 240, 160))
    comp(f, chip("CAN'T", (200, 60, 60), TOOTHW, 36), 540, 760, scale=pin(t, T("a3", "can't") - 0.1, 0.25))
    icap(f, "they can't chew through", "[YOUR TEETH]", t, st_("S5") + 0.05, acc=ACC, size=150)
    return finish(f, n, look="fresh")


# ---- S5b: 'but they absolutely LOVE sugar' — a sweet drops in; every bug turns with heart eyes; 3D SUGAR ----
def shot_S5b(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440); u = lt(t, "S5b")
    tl = T("a3", "love") - 0.1
    t3(f, "SUGAR", 640, t, tl, 300, ACC_L, ACC_S)
    y, sx, sy = drop_land(t, st_("S5b"), 500, 1000, 0.4)
    comp(f, scale_xy(scale_el(candy_el("wrap"), 1.3), sx, sy), 540, y)
    for i in range(6):
        a = i / 6 * 2 * math.pi; r_ = 260 + 10 * math.sin(t * 5 + i)
        md = "love" if t >= tl else "wow"
        comp(f, scale_el(bug_el(md, (-math.cos(a), -math.sin(a) * 0.6), 1 + i % 4), 0.95), 540 + r_ * math.cos(a), 1040 + r_ * math.sin(a) * 0.7 + 4 * math.sin(t * 7 + i))
    if t >= tl: sparkles(f, 540, 1000, t, tl, 14, 260, ACC_L, 2, 1.0)
    icap(f, "but they absolutely", "[LOVE] sugar", t, st_("S5b") + 0.05, acc=ACC, size=180, out=tl - 0.05)
    return finish(f, n, look="fresh")


# ---- S6: 'You eat a sweet. They eat the leftovers.' — Chubby munches (top), crumbs fall to the tooth where bugs feast (bottom) ----
def shot_S6(t, n):
    f = set_kitchen(t); f = inkify(f)
    tl = T("a4", "leftovers.") - 0.2
    m, c = munch(t, 0.38)
    chub_head_only(f, 320, 740, 1.3, t, mouth=m, expr="happy", brow="up", look=(0.6, 0.6))
    crumbs(f, 330, 840, t, st_("S6") + 0.3, 10, 7, 1.0, 170, 240)
    crumbs(f, 330, 840, t, st_("S6") + 1.0, 10, 8, 1.0, 170, 240)
    comp(f, tooth_el("n", 0.3), 560, 1130, scale=1.1)
    for i, (dx, dy) in enumerate(((-150, 40), (160, 20), (-40, 120))):
        comp(f, scale_el(bug_el("munch" if t >= tl else "hungry", (0, -0.5), 1 + i), 0.85), 560 + dx, 1130 + dy + 4 * math.sin(t * 8 + i))
    if t >= tl: label_at(f, "LEFTOVERS", 820, 900, t, tl, 600, 1040, bg=ACC_S, fg=TOOTHW, size=28)
    counter_front(f, 1330)
    icap(f, "you eat a sweet,", "[THEY] eat the leftovers", t, st_("S6") + 0.05, acc=ACC, size=110)
    return finish(f, n, look="warm")


# ---- S6b: '...and what comes out of them is ACID' — bugs with full bellies, violet drops come out; 3D ACID ----
def shot_S6b(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440)
    ta = T("a4", "acid.") - 0.15
    t3(f, "ACID", 640, t, ta, 320, ACC_L, ACC_S)
    comp(f, tooth_el("sus", 0.0, 0.0, False, False, False, (0, 0.6)), 540, 1180, scale=1.2)
    for i, dx in enumerate((-220, 0, 220)):
        x = 540 + dx; y = 920 + 6 * math.sin(t * 6 + i)
        comp(f, scale_el(bug_el("happy", (0, 0.3), 1 + i), 1.0), x, y, scale=1 + 0.08 * math.sin(t * 9 + i))
        q = t - ta - 0.1 * i
        if q > 0:
            dy = 180 * clamp(q / 0.5) ** 2
            comp(f, scale_el(acid_drop_el(1, "angry" if q > 0.3 else None), 0.6), x + 10, y + 50 + dy)
            if q > 0.5: acid_pool(f, 540, 1070, 520, 70, t, clamp((q - 0.5) / 0.6), 0.7)
    if t >= ta: comp(f, chip("= ACID", ACC_S, TOOTHW, 36), 540, 1400, scale=pin(t, ta, 0.25))
    icap(f, "and what comes out of them...", "", t, st_("S6b") + 0.05, acc=ACC, size=150, out=ta - 0.05)
    return finish(f, n, look="fresh")


# ---- S7: 'acid pulls minerals out of your enamel' — drops hit the crown, white mineral dots are pulled out and drift away ----
def shot_S7(t, n):
    f = ink_set("violet", (230, 210, 250), 540, 1000, 440); u = lt(t, "S7")
    tm = T("a5", "minerals") - 0.1
    comp(f, tooth_el("sad", 0.0, 0.3), 540, 1080, scale=1.5)
    for i in range(5):
        q = ((u * 0.9) + i * 0.2) % 1.0
        comp(f, scale_el(acid_drop_el(), 0.55), 400 + i * 70, 700 + 260 * q * q)
    if t >= tm:
        pts = []
        for i in range(14):
            q = ((t - tm) * 0.5 + i / 14) % 1.0; a = i * 2.4
            pts.append((540 + (120 + 420 * q) * math.cos(a), 1000 + (80 + 300 * q) * math.sin(a) * 0.8))
        minerals(f, pts, 10)
        label_at(f, "MINERALS", 230, 1400, t, tm, 420, 1180, bg=INKC, fg=TOOTHW, size=28)
    icap(f, "that acid pulls", "[MINERALS] out", t, st_("S7") + 0.05, acc=TOOTHW, size=150, dark=True)
    return finish(f, n, look="night")


# ---- S7b: 'Enamel is the hard, shiny shell' — label on the shell with a leader arrow; shine sweep ----
def shot_S7b(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440); u = lt(t, "S7b")
    te = T("a5", "shell") - 0.1
    comp(f, tooth_el("happy", 0.0, 0.0), 540, 1080, scale=1.6)
    ov = f.copy(); cv2.polylines(ov, [np.array([(x * 1.6 + 540 - 240, y * 1.6 + 1080 - 256) for x, y in MOLAR[:9]], np.int32)], False, C(INK_MINT), 22, cv2.LINE_AA)
    k = ramp(t, st_("S7b") + 0.1, 0.6); f[:] = f * (1 - 0.8 * k) + ov * 0.8 * k
    sh = (u * 0.7) % 1.0; cv2.ellipse(f, (int(380 + 320 * sh), int(840 + 40 * sh)), (26, 60), -30, 0, 360, C(WHITE), -1, cv2.LINE_AA)
    label_at(f, "ENAMEL", 240, 760, t, st_("S7b") + 0.1, 420, 860, bg=INK_MINT_S, fg=TOOTHW, size=32)
    if t >= te: comp(f, ichip("the hard, shiny shell", 30), 540, 1400, scale=pin(t, te, 0.25))
    icap(f, "", "[ENAMEL]", t, st_("S7b") + 0.05, acc=INK_MINT_S, size=220)
    return finish(f, n, look="fresh")


# ---- S8: 'lose enough minerals and the shell breaks' — crack grows, minerals leave; BREAKS on the word ----
def shot_S8(t, n):
    f = ink_set("dusk_v", None); f *= 0.8
    tb = T("a6", "breaks.") - 0.1
    k = ramp(t, st_("S8"), max(0.5, tb - st_("S8")))
    hole = t >= tb
    lean_, sq = flinch(t, tb, 1.0)
    rot_comp(f, tooth_el("ouch" if t >= tb - 0.3 else "sad", 0.0, k, hole), 540, 1080, 8 * settle(t, tb, 1.0, 16, 6), 1.5, 1.0, 0.35)
    for i in range(10):
        q = clamp((t - st_("S8") - i * 0.12) / 1.2); a = i * 2.4
        if 0 < q < 1: minerals(f, [(540 + (100 + 380 * q) * math.cos(a), 1000 + (60 + 260 * q) * math.sin(a) * 0.8)], 9)
    spotlight(f, 540, 1050, 420, 0.4, 220)
    if hole: comp(f, burst_el("CRACK!", ACC_L, INKC, 58), 820, 760, scale=pin(t, tb, 0.2))
    icap(f, "lose enough minerals and the shell", "[BREAKS]", t, st_("S8") + 0.05, acc=ACC_L, size=170, dark=True)
    return finish(f, n, look="night")


# ---- S8b: 'that hole has a name: a CAVITY' — 3D title, Chubby holds his cheek ----
def shot_S8b(t, n):
    f = set_bathroom(t) * 0.85
    tc = T("a6", "cavity.") - 0.15
    t3(f, "CAVITY", 640, t, tc, 280, ACC_L, ACC_S)
    comp(f, tooth_el("ouch", 0.0, 0.0, True), 780, 1040 + 4 * math.sin(t * 3), scale=1.1)
    lean_, sq = flinch(t, tc, 0.6)
    chub(f, 320, 1500, 1.05, t=t, **POSE["cheek"], mouth="o" if t >= tc else talk(t), expr="sad" if t < tc else "wow", brow="sad", look=(1, -0.3), squash=sq)
    sweat_drops(f, 380, 980, t)
    icap(f, "that hole has a name:", "", t, st_("S8b") + 0.05, acc=ACC, size=150, out=tc - 0.05)
    return finish(f, n, look="cool")


# ---- S9: 'But WAIT. Your mouth has a rescue team.' — double take, mint spotlight, RESCUE TEAM chip ----
def shot_S9(t, n):
    f = set_porch(t)
    tw = T("b1", "wait.") - 0.2; tr = T("b1", "rescue") - 0.1
    look, lean, expr, brow = double_take(t, tw)
    if t >= tr: mood(f, (120, 220, 170), 0.3)
    chub(f, 540, 1500, 1.15, t=t, la=(40, 30) if t < tr else (150, 170), ra=(72, 42) if t < tr else (150, 170), mouth=talk(t), expr=expr if t < tr else "happy", brow=brow if t < tr else "up", look=look, lean=lean)
    if t >= tr:
        rays(f, 540, 1000, 700, (170, 240, 210), 0.45 * ramp(t, tr, 0.3), t)
        slam(f, chip("RESCUE TEAM", INK_MINT, TOOTHW, 48), 540, 760, -4, t, tr)
    icap(f, "", "BUT WAIT.", t, tw, acc=ACC, size=200, dark=True, out=tr - 0.05)
    return finish(f, n, look="warm")


# ---- S10: 'It's your spit. No, really.' — the saliva hero drops onto the podium (cape), Chubby deadpans to camera ----
def shot_S10(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440)
    tn = T("b2", "No,") - 0.1
    podium(f, 640, 1250, 420, 100, t)
    y, sx, sy = drop_land(t, st_("S10") + 0.1, 500, 1230, 0.45)
    comp(f, scale_xy(scale_el(spit_hero_el("happy"), 1.2), sx, sy), 640, y - 110)
    if t >= st_("S10") + 0.55: dust_puff(f, 640, 1250, t, st_("S10") + 0.55)
    chub(f, 240, 1500, 0.95, t=t, **POSE["present"], mouth=talk(t), expr="smirk" if t >= tn else "happy", brow="n", look=(0, 0) if t >= tn else (1, -0.2))
    comp(f, ichip("SALIVA", 34), 640, 1400, scale=pin(t, st_("S10") + 0.7, 0.25))
    icap(f, "it's your", "[SPIT]", t, st_("S10") + 0.05, acc=INK_MINT_S, size=220, out=tn - 0.05)
    icap(f, "no,", "REALLY.", t, tn, acc=INK_MINT_S, size=200) if t >= tn else None
    return finish(f, n, look="fresh")


# ---- S11: 'Saliva washes the acid away' — a mint wave rolls over the tooth and the acid pool is gone ----
def shot_S11(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440); u = lt(t, "S11")
    tw = T("b3", "washes") - 0.1
    k = ramp(t, tw, 0.9)
    acid_pool(f, 540, 1180, 560, 70, t, 1.0 - k, 0.7)
    comp(f, tooth_el("happy" if k > 0.6 else "sad", 0.0, 0.0), 540, 1080, scale=1.4)
    saliva_wave(f, 540, 1150, 900, t, k, 110, 0.7)
    if t >= tw: comp(f, chip("WASHED AWAY", INK_MINT, TOOTHW, 34), 540, 760, scale=pin(t, tw + 0.5, 0.25))
    icap(f, "saliva", "[WASHES] the acid away", t, st_("S11") + 0.05, acc=INK_MINT_S, size=120)
    return finish(f, n, look="fresh")


# ---- S11b: '...and carries minerals BACK into the enamel' — mineral dots flow back in along pulse paths ----
def shot_S11b(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S11b")
    tb = T("b3", "back") - 0.1
    comp(f, tooth_el("happy", 0.0, 0.0), 540, 1080, scale=1.5)
    for i in range(6):
        a = i / 6 * 2 * math.pi + 0.3; p0 = (540 + 430 * math.cos(a), 1000 + 330 * math.sin(a) * 0.8); p1 = (540 + 150 * math.cos(a), 1020 + 120 * math.sin(a) * 0.8)
        pulse_path(f, [p0, p1], t, st_("S11b") + 0.1 + 0.1 * i, 0.9, TOOTHW, 14, 2, 0.5, 6)
        q = ((u * 0.8) + i * 0.17) % 1.0
        minerals(f, [(p0[0] + (p1[0] - p0[0]) * q, p0[1] + (p1[1] - p0[1]) * q)], 10)
    if t >= tb: label_at(f, "MINERALS BACK IN", 540, 1420, t, tb, 540, 1200, bg=INK_MINT_S, fg=TOOTHW, size=30)
    icap(f, "and carries minerals", "[BACK] in", t, st_("S11b") + 0.05, acc=INK_MINT_S, size=170)
    return finish(f, n, look="fresh")


# ---- S12: 'your teeth quietly patch themselves up' — the crack heals (crack 1 -> 0), a check mark ----
def shot_S12(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440)
    tp = T("b4", "patch") - 0.1
    k = ramp(t, tp, 1.0)
    comp(f, tooth_el("happy" if k > 0.7 else "n", 0.0, 1.0 - k), 540, 1080, scale=1.5)
    for i in range(5):
        q = ((lt(t, "S12") * 0.7) + i * 0.2) % 1.0
        minerals(f, [(380 + i * 80, 1360 - 340 * q)], 8)
    if k > 0.9: comp(f, check_el(60, True), 800, 820, scale=pin(t, tp + 0.9, 0.25)); sparkles(f, 540, 1000, t, tp + 0.9, 10, 220, (255, 250, 220))
    icap(f, "your teeth quietly", "[PATCH] themselves up", t, st_("S12") + 0.05, acc=INK_MINT_S, size=120)
    return finish(f, n, look="fresh")


# ---- S12b: 'the fluoride in toothpaste helps them do it' — bathroom shelf: paste tube + brush slide in ----
def shot_S12b(t, n):
    f = set_bathroom(t)
    tf = T("b4", "fluoride") - 0.1
    k = pin(t, st_("S12b") + 0.05, 0.35)
    chub(f, 300, 1500, 1.0, t=t, **POSE["hold_up"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.4), hold=scale_el(brush_el(), 0.7), hold_off=(60, -80), hold_front=True)
    comp(f, scale_el(paste_el(), 1.2), 720, 1050 + 4 * math.sin(t * 3), scale=k)
    if t >= tf: label_at(f, "FLUORIDE", 760, 800, t, tf, 720, 1000, bg=INK_MINT_S, fg=TOOTHW, size=32)
    comp(f, ichip(SRC_N, 22), 540, 1462, op=clamp((lt(t, "S12b") - 0.4) / 0.3))
    icap(f, "the fluoride in toothpaste", "[HELPS]", t, st_("S12b") + 0.05, acc=INK_MINT_S, size=180)
    return finish(f, n, look="fresh")


# ---- S13: 'an early cavity, a white spot, can heal. A real hole can't.' — split: WHITE SPOT (heals) vs HOLE (can't) ----
def shot_S13(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440)
    th = T("b5", "heal.") - 0.15; tc = T("b5", "can't.") - 0.15; tr = T("b5", "A", 1) - 0.2
    def L(g):
        comp(g, tooth_el("happy" if t >= th else "n", 0.0, 0.0, False, True), 330, 1030, scale=1.0)
        if t >= th: comp(g, check_el(50, True), 420, 860, scale=pin(t, th, 0.25)); comp(g, chip("CAN HEAL", INK_MINT, TOOTHW, 28), 330, 1300, scale=pin(t, th, 0.25))
    def R(g):
        comp(g, tooth_el("ouch", 0.0, 0.0, True), 750, 1030, scale=1.0)
        if t >= tc: comp(g, check_el(50, False), 840, 860, scale=pin(t, tc, 0.25)); comp(g, chip("CAN'T", (200, 60, 60), TOOTHW, 28), 750, 1300, scale=pin(t, tc, 0.25))
    split_contrast(f, t, st_("S13") + 0.05, L, R, "WHITE SPOT", "A REAL HOLE", INK_MINT, ACC, 640, 1420, 0.35, tr)
    icap(f, "an early cavity", "[CAN HEAL]", t, st_("S13") + 0.05, acc=INK_MINT_S, size=170, out=tr - 0.05)
    icap(f, "a real hole", "[CAN'T]", t, tr, acc=ACC, size=200) if t >= tr else None
    return finish(f, n, look="fresh")


# ---- S14: PART 2 — lights drop, Chubby whispers 'the thing nobody tells you' (one focal point: the spotlight) ----
def shot_S14(t, n):
    f = set_porch(t) * 0.5
    mood(f, (90, 60, 140), 0.3)
    chub(f, 540, 1500, 1.15, t=t, **POSE["whisper"], mouth=talk(t), expr="sus", brow="sus", look=(0, -0.3))
    spotlight(f, 540, 1000, 380, 0.6, 220)
    chapter_card(f, t, st_("S14") + 0.05, 2, "THE TIMER", y=1440, dur=1.6, col=ACC_L)
    icap(f, "the thing", "[NOBODY] tells you", t, st_("S14") + 0.05, acc=ACC_L, size=150, dark=True)
    return finish(f, n, look="night")


# ---- S14b: 'The TIMER.' — a big ink timer slams in ----
def shot_S14b(t, n):
    f = ink_set("dusk_v", None); f *= 0.8
    slam(f, timer_el(0.0, None, 170), 540, 1040, -6, t, st_("S14b") + 0.02, 1.0)
    spotlight(f, 540, 1040, 360, 0.45, 200)
    icap(f, "", "THE TIMER", t, st_("S14b") + 0.05, acc=ACC_L, size=210, dark=True)
    return finish(f, n, look="night")


# ---- S15: 'the acid hangs around for about 30 to 60 minutes' — the dial fills violet while the tooth sits in acid ----
def shot_S15(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 980, 440)
    t3_ = T("c2", "thirty") - 0.15; ts = T("c2", "sixty") - 0.1
    k = ramp(t, st_("S15") + 0.3, max(0.8, ts - st_("S15")))
    comp(f, timer_el(k * 0.9, "30-60 MIN" if t >= t3_ else None, 150), 540, 760)
    acid_pool(f, 540, 1300, 620, 80, t, 1.0, 0.7)
    comp(f, tooth_el("sad", 0.0, 0.0), 540, 1180, scale=1.1)
    comp(f, ichip(SRC_T, 22), 540, 1462, op=clamp((lt(t, "S15") - 0.6) / 0.3))
    if t >= t3_: icap(f, "every sweet = acid for", "[30-60] minutes", t, t3_, acc=ACC, size=150)
    else: icap(f, "every time you eat something sweet,", "", t, st_("S15") + 0.05, acc=ACC, size=150, out=t3_ - 0.05)
    return finish(f, n, look="fresh")


# ---- S16: 'One sweet? Half an hour to an hour of acid.' — one candy + one dial ----
def shot_S16(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 980, 440); u = lt(t, "S16")
    comp(f, scale_el(candy_el("wrap"), 1.2), 300, 760 + 6 * math.sin(t * 3), scale=pin(t, st_("S16"), 0.3))
    draw_arrow(f, 420, 760, 560, 760, ramp(t, st_("S16") + 0.3, 0.3), INKC, 8, 26)
    comp(f, timer_el(0.9 * ramp(t, st_("S16") + 0.5, 1.2), "~1 HOUR", 120), 740, 760, scale=pin(t, st_("S16") + 0.4, 0.3))
    chub(f, 300, 1500, 1.0, t=t, la=(30, 16), ra=(150, 175), mouth=talk(t), expr="n", brow="up", look=(1, -0.4), lean=4)
    acid_pool(f, 700, 1280, 420, 60, t, ramp(t, st_("S16") + 0.5, 1.0), 0.6)
    comp(f, tooth_el("sad", 0.0, 0.0), 700, 1180, scale=0.9)
    icap(f, "one sweet?", "[1 HOUR] of acid", t, st_("S16") + 0.05, acc=ACC, size=150)
    return finish(f, n, look="fresh")


# ---- S17: 'Three sweets at once? STILL half an hour to an hour.' — three candies, SAME dial; Chubby surprised ----
def shot_S17(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 980, 440); u = lt(t, "S17")
    ts = T("c4", "Still") - 0.1
    for i, k in enumerate(("wrap", "gummy", "lolly")): comp(f, scale_el(candy_el(k), 0.9), 220 + i * 110, 760 + 6 * math.sin(t * 3 + i), scale=pin(t, st_("S17") + 0.1 * i, 0.3))
    draw_arrow(f, 460, 760, 580, 760, ramp(t, st_("S17") + 0.4, 0.3), INKC, 8, 26)
    comp(f, timer_el(0.9, "STILL ~1 HOUR" if t >= ts else "~1 HOUR", 120), 760, 760, scale=pin(t, st_("S17") + 0.5, 0.3))
    look, lean, expr, brow = double_take(t, ts - 0.2)
    chub(f, 300, 1500, 1.0, t=t, **POSE["shrug"], mouth=talk(t), expr=expr, brow=brow, look=look, lean=lean)
    acid_pool(f, 700, 1280, 420, 60, t, 1.0, 0.6)
    comp(f, tooth_el("sad", 0.0, 0.0), 700, 1180, scale=0.9)
    if t >= ts: comp(f, chip("SAME TIME", ACC, TOOTHW, 34), 760, 960, scale=pin(t, ts, 0.25))
    icap(f, "three at once?", "[STILL] ~1 hour", t, st_("S17") + 0.05, acc=ACC, size=150)
    return finish(f, n, look="fresh")


# ---- S18: 'one sweet every hour, all afternoon' — a day strip: a candy at every hour, violet acid blocks join into one long bar ----
def day_strip(f, t, t0, hours=6, x0=120, x1=960, y=1000):
    gap = (x1 - x0) / (hours - 1)
    cv2.line(f, (x0, y + 60), (x1, y + 60), C(INKC), 6, cv2.LINE_AA)
    for i in range(hours):
        x = int(x0 + i * gap); cv2.line(f, (x, y + 60), (x, y + 76), C(INKC), 5, cv2.LINE_AA)
        comp(f, ichip(f"{1 + i} PM", 22), x, y + 110)
        ti = t0 + 0.35 * i
        if t < ti: continue
        k = pin(t, ti, 0.3)
        comp(f, scale_el(candy_el(("wrap", "gummy", "lolly")[i % 3]), 0.7), x, y - 90, scale=k)
        w_ = gap * 1.05 * clamp((t - ti) / 0.5)
        ov = f.copy(); cv2.rectangle(ov, (int(x - 10), int(y - 10)), (int(x + w_), int(y + 40)), C(ACC), -1, cv2.LINE_AA); f[:] = f * 0.3 + ov * 0.7
        cv2.rectangle(f, (int(x - 10), int(y - 10)), (int(x + w_), int(y + 40)), C(INKC), 4, cv2.LINE_AA)
    return t0 + 0.35 * (hours - 1)


def shot_S18(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 980, 440)
    tend = day_strip(f, t, st_("S18") + 0.2)
    comp(f, ichip("ACID", 30), 540, 1180, scale=pin(t, st_("S18") + 0.6, 0.25))
    chub(f, 170, 1500, 0.72, t=t, **POSE["point"], mouth=talk(t), expr="sus", brow="sus", look=(1, -0.5))
    icap(f, "one sweet", "[EVERY HOUR]", t, st_("S18") + 0.05, acc=ACC, size=160)
    return finish(f, n, look="fresh")


# ---- S18b: 'Your teeth sit in acid the whole day. No time to repair.' — the strip stays, tooth drowning, NO TIME TO REPAIR ----
def shot_S18b(t, n):
    f = ink_set("violet", (230, 210, 250), 540, 980, 440)
    tn = T("c5", "No") - 0.1
    day_strip(f, t, st_("S18") + 0.2)
    acid_pool(f, 540, 1380, 760, 90, t, 1.0, 0.75)
    comp(f, tooth_el("ouch", 0.0, 0.5), 540, 1290, scale=1.0)
    sweat_drops(f, 560, 1200, t)
    if t >= tn: slam(f, chip("NO TIME TO REPAIR", (200, 60, 60), TOOTHW, 40), 540, 1180, -4, t, tn)
    icap(f, "your teeth sit in acid", "[THE WHOLE DAY]", t, st_("S18b") + 0.05, acc=ACC_XL, size=130, dark=True)
    return finish(f, n, look="night")


# ---- S19: 'it's not HOW MUCH. It's HOW OFTEN.' — HOW MUCH stamped out, 3D HOW OFTEN; pile vs row ----
def shot_S19(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 980, 440)
    to = T("c6", "often.") - 0.15; tm = T("c6", "much") - 0.1
    t3(f, "HOW OFTEN", 640, t, to, 220, ACC_L, ACC_S)
    def L(g):
        for i in range(7): comp(g, scale_el(candy_el(("wrap", "gummy", "lolly", "caramel")[i % 4]), 0.7), 320 + 50 * math.cos(i * 1.7), 1030 - 26 * i + 12 * math.sin(i))
        comp(g, timer_el(0.9, "1 HR", 70), 330, 1260)
    def R(g):
        for i in range(5): comp(g, scale_el(candy_el(("wrap", "gummy", "lolly")[i % 3]), 0.55), 600 + i * 72, 980)
        ov = g.copy(); cv2.rectangle(ov, (575, 1060), (925, 1130), C(ACC), -1, cv2.LINE_AA); g[:] = g * 0.3 + ov * 0.7
        cv2.rectangle(g, (575, 1060), (925, 1130), C(INKC), 4, cv2.LINE_AA)
        comp(g, chip("ACID ALL DAY", ACC_S, TOOTHW, 26), 750, 1260)
    if t < to - 0.05:
        split_contrast(f, t, st_("S19") + 0.05, L, R, "HOW MUCH", "HOW OFTEN", INKC, ACC, 760, 1380, 0.35, st_("S19") + 0.5)
        if t >= tm: myth_tag(f, 330, 760, t, tm, tm + 0.25, 50, "HOW MUCH")
    else:
        for i in range(5): comp(f, scale_el(candy_el(("wrap", "gummy", "lolly")[i % 3]), 0.6), 300 + i * 120, 1120 + 6 * math.sin(t * 3 + i))
    if t >= to: icap(f, "it's not how much.", "it's [HOW OFTEN]", t, to, acc=ACC, size=130)
    return finish(f, n, look="fresh")


# ---- S19b: 'Dentists have been saying this for years' — source chip, Chubby nods ----
def shot_S19b(t, n):
    f = set_bathroom(t)
    chub(f, 540, 1500, 1.1, t=t, **POSE["arms_out"], mouth=talk(t), expr="happy", brow="up", look=(0, -0.2), lean=3 * math.sin(t * 3))
    comp(f, chip(SRC_T, INKC, TOOTHW, 26), 540, 860, scale=pin(t, st_("S19b") + 0.2, 0.3))
    comp(f, chip("2010 · 2023", ACC, TOOTHW, 26), 540, 930, scale=pin(t, st_("S19b") + 0.5, 0.3))
    icap(f, "dentists have said this", "[FOR YEARS]", t, st_("S19b") + 0.05, acc=ACC, size=160)
    return finish(f, n, look="fresh")


# ---- S20: PART 3 — 'the candy ranking': the three cloths lift off the podium (open loop starts paying off) ----
def shot_S20(t, n):
    f = ink_set("dusk_v", None); f *= 0.8
    tr = T("d1", "ranking.") - 0.15
    podium(f, 620, 1250, 560, 110, t)
    for i, (x, k) in enumerate(((470, "gummy"), (620, "sour"), (770, "choc"))):
        comp(f, scale_el(candy_el(k), 0.8), x, 1150 + 6 * math.sin(t * 3 + i))
        cloth(f, x, 1250, 130, 110 + 30 * (i % 2), t + i, ramp(t, tr + 0.15 * i, 0.5))
    spotlight(f, 620, 1150, 330, 0.5, 200)
    god_rays(f, 620, 250, t, (240, 220, 255), 0.22, 7, 1000, 0.5, 1.57, 3)
    chub(f, 230, 1500, 0.95, t=t, **POSE["tada"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    chapter_card(f, t, st_("S20") + 0.05, 3, "CANDY RANKING", y=1440, dur=1.6, col=ACC_L)
    icap(f, "okay. time for the", "[CANDY RANKING]", t, st_("S20") + 0.05, acc=ACC_L, size=130, dark=True)
    return finish(f, n, look="night")


def sticky_strings(f, x0, y0, x1, y1, t, n=4):
    for i in range(n):
        q = i / (n - 1) - 0.5
        pts = [(x0 + (x1 - x0) * u + 30 * q * math.sin(math.pi * u), y0 + (y1 - y0) * u + 18 * math.sin(math.pi * u + t * 3 + i)) for u in np.linspace(0, 1, 12)]
        cv2.polylines(f, [np.array(pts, np.int32)], False, C(INKC), 7, cv2.LINE_AA); cv2.polylines(f, [np.array(pts, np.int32)], False, C(ACC_L), 4, cv2.LINE_AA)


# ---- S21: 'chewy caramels and gummies STICK to your teeth' — gummy + caramel glued to the tooth with stretching strings ----
def shot_S21(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440); u = lt(t, "S21")
    ts = T("d2", "stick") - 0.1
    comp(f, tooth_el("sus", 0.0, 0.0, False, False, False, (-0.4, -0.5)), 540, 1080, scale=1.5)
    for i, (k, x, y) in enumerate((("caramel", 380, 880), ("gummy", 700, 900))):
        q = pin(t, st_("S21") + 0.1 + 0.25 * i, 0.35)
        if t >= ts: sticky_strings(f, x, y + 40, 540 + (x - 540) * 0.3, 1000, t, 4)
        comp(f, scale_el(candy_el(k), 1.15), x, y + 4 * math.sin(t * 4 + i), scale=q)
    if t >= ts: slam(f, chip("STUCK", ACC, TOOTHW, 40), 540, 1400, -5, t, ts)
    icap(f, "chewy caramels and gummies", "[STICK]", t, st_("S21") + 0.05, acc=ACC, size=200)
    return finish(f, n, look="fresh")


# ---- S21b: 'so the bacteria get a LONGER meal' — bugs feasting at the stuck sweet with a timer running long ----
def shot_S21b(t, n):
    f = ink_set("violet", (230, 210, 250), 540, 1000, 440); u = lt(t, "S21b")
    tl = T("d2", "longer") - 0.1
    comp(f, tooth_el("sad", 0.2, 0.0), 540, 1120, scale=1.3)
    comp(f, scale_el(candy_el("gummy"), 0.8), 600, 940)
    sticky_strings(f, 600, 980, 560, 1040, t, 3)
    for i, (dx, dy) in enumerate(((-170, -40), (160, -30), (-60, 60), (90, 80))):
        comp(f, scale_el(bug_el("munch", (0, -0.4), 1 + i), 0.8), 600 + dx, 980 + dy + 4 * math.sin(t * 8 + i))
    comp(f, timer_el(clamp(u / 2.0), "LONGER", 90), 860, 760, scale=pin(t, st_("S21b") + 0.1, 0.3))
    if t >= tl: label_at(f, "LONGER MEAL", 240, 1400, t, tl, 440, 1060, bg=ACC_S, fg=TOOTHW, size=30)
    icap(f, "the bacteria get a", "[LONGER] meal", t, st_("S21b") + 0.05, acc=ACC_XL, size=150, dark=True)
    return finish(f, n, look="night")


# ---- S22: 'Sour sweets? They bring their own acid along.' — a sour drop fizzes its own acid at the tooth; the tooth flinches ----
def shot_S22(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440); u = lt(t, "S22")
    ta = T("d3", "own") - 0.1
    lean_, sq = flinch(t, ta, 1.0)
    rot_comp(f, tooth_el("ouch" if t >= ta else "sus", 0.0, 0.0, False, False, False, (-0.7, 0)), 720, 1100, lean_ * 0.5, 1.3, 1.0, 0.35)
    comp(f, scale_el(candy_el("sour"), 1.5), 300, 1060 + 5 * math.sin(t * 5), scale=pin(t, st_("S22"), 0.3))
    if t >= ta:
        for i in range(6):
            q = ((t - ta) * 1.4 + i * 0.17) % 1.0
            comp(f, scale_el(acid_drop_el(), 0.45), 380 + 260 * q, 1000 + 40 * math.sin(i) - 120 * math.sin(math.pi * q))
        slam(f, chip("ITS OWN ACID", ACC_S, TOOTHW, 36), 540, 1400, 4, t, ta)
    comp(f, ichip("SOUR", 34), 300, 860, scale=pin(t, st_("S22") + 0.2, 0.25))
    icap(f, "sour sweets bring", "[THEIR OWN] acid", t, st_("S22") + 0.05, acc=ACC, size=140)
    return finish(f, n, look="fresh")


# ---- S23: 'And chocolate? It melts and washes off fast.' — the square melts off the tooth, the saliva wave takes it; bugs get nothing ----
def shot_S23(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S23")
    tm = T("d4", "melts") - 0.1; tw = T("d4", "washes") - 0.1
    km = ramp(t, tm, 0.8); kw = ramp(t, tw, 0.8)
    comp(f, tooth_el("happy" if kw > 0.5 else "n", 0.0, 0.0), 540, 1080, scale=1.5)
    el = scale_xy(scale_el(candy_el("choc"), 1.1), 1 + 0.5 * km, 1 - 0.6 * km)
    comp(f, el, 540 + 330 * kw, 900 + 110 * km, op=1 - 0.7 * kw)
    saliva_wave(f, 540, 1000, 820, t, kw, 90, 0.6)
    for i, (dx, dy) in enumerate(((-300, 160), (320, 180))):
        comp(f, scale_el(bug_el("sad", (-dx / 300, -0.4), 1 + i), 0.8), 540 + dx, 1100 + dy + 3 * math.sin(t * 6 + i))
    if t >= tw: comp(f, chip("WASHED OFF", INK_MINT, TOOTHW, 34), 540, 1400, scale=pin(t, tw + 0.3, 0.25))
    icap(f, "and chocolate?", "[MELTS] + washes off", t, st_("S23") + 0.05, acc=INK_MINT_S, size=120)
    return finish(f, n, look="fresh")


# ---- S23b: 'Dentists call it one of the better picks. Told you.' — open loop PAID: chocolate on the podium, Chubby smirks to camera ----
def shot_S23b(t, n):
    f = ink_set("dusk_v", None); f *= 0.85
    tt = T("d4", "Told") - 0.1
    t3(f, "BETTER PICK", 640, t, st_("S23b") + 0.1, 190, (200, 240, 220), INK_MINT_S)
    podium(f, 640, 1250, 420, 100, t)
    comp(f, scale_el(candy_el("choc"), 1.8), 640, 1120 + 5 * math.sin(t * 3))
    comp(f, check_el(50, True), 760, 1040, scale=pin(t, st_("S23b") + 0.3, 0.25))
    spotlight(f, 640, 1130, 300, 0.45, 180)
    god_rays(f, 640, 250, t, (220, 255, 235), 0.2, 7, 1000, 0.5, 1.57, 3)
    chub(f, 250, 1500, 0.95, t=t, **POSE["hold_up"], mouth=talk(t) if t < tt else 0, expr="smirk" if t >= tt else "happy", brow="n" if t >= tt else "up", look=(0, 0) if t >= tt else (1, -0.3))
    if t >= tt: comp(f, burst_el("TOLD YOU", INK_MINT, TOOTHW, 48), 300, 760, scale=pin(t, tt, 0.25))
    comp(f, chip("Source: California Dental Association", INKC, TOOTHW, 22), 540, 1462, op=clamp((lt(t, "S23b") - 0.3) / 0.3))
    return finish(f, n, look="night")


# ---- S24: PART 4 — 'So, your plan for tonight.' — Halloween porch again, Chubby with the pail ----
def shot_S24(t, n):
    f = set_porch(t)
    chub(f, 540, 1500, 1.15, t=t, **POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(0.3, -0.2),
         hold=scale_el(pail_el(), 0.5), hold_off=(40, 20), hold_front=True)
    chapter_card(f, t, st_("S24") + 0.05, 4, "TONIGHT'S PLAN", y=1440, dur=1.6, col=INK_MINT)
    icap(f, "so, your plan for", "[TONIGHT]", t, st_("S24") + 0.05, acc=ACC_L, size=190, dark=True)
    return finish(f, n, look="warm")


# ---- S25: 'eat your candy in one go, with a meal, when your mouth is full of saliva' — plate + candy, saliva meter rising ----
def shot_S25(t, n):
    f = set_kitchen(t); f = inkify(f)
    to = T("e2", "one") - 0.1; tm = T("e2", "meal,") - 0.1; tsal = T("e2", "saliva.") - 0.15
    comp(f, scale_el(plate_el(), 1.1), 560, 1250, scale=pin(t, st_("S25") + 0.05, 0.3))
    for i, k in enumerate(("wrap", "gummy", "lolly")): comp(f, scale_el(candy_el(k), 0.55), 300 + i * 70, 1180 + 10 * (i % 2), scale=pin(t, to + 0.1 * i, 0.3))
    if t >= tm: comp(f, chip("WITH A MEAL", INK_MINT, TOOTHW, 32), 560, 1060, scale=pin(t, tm, 0.25))
    ks = ramp(t, tsal, 0.8)
    if t >= tsal - 0.2:
        comp(f, spit_hero_el("happy"), 860, 800 + 6 * math.sin(t * 4), scale=0.9 * pin(t, tsal - 0.2, 0.3))
        comp(f, chip("LOTS OF SALIVA", INK_MINT, TOOTHW, 26), 860, 980, scale=pin(t, tsal, 0.25))
    counter_front(f, 1330)
    chub(f, 200, 1500, 0.8, t=t, **POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(1, 0))
    icap(f, "eat your candy", "[IN ONE GO]", t, st_("S25") + 0.05, acc=INK_MINT_S, size=150)
    return finish(f, n, look="warm")


# ---- S25b: 'Then a glass of water.' — Chubby drinks; the wave rinses ----
def shot_S25b(t, n):
    f = set_kitchen(t); f = inkify(f)
    k = ramp(t, st_("S25b") + 0.2, 0.9)
    chub(f, 540, 1500, 1.1, t=t, la=(40, 30), ra=(148, -126), mouth="o", expr="happy", brow="up", look=(0, -0.5), lean=-4 * k,
         hold=glass_el(1.0 - 0.75 * k), hold_off=(-10, -40), hold_front=True)
    counter_front(f, 1330)
    comp(f, glass_el(1.0), 820, 1240, scale=pin(t, st_("S25b"), 0.3))
    icap(f, "then a glass of", "[WATER]", t, st_("S25b") + 0.05, acc=INK_MINT_S, size=200)
    return finish(f, n, look="warm")


# ---- S26: 'if you had sour stuff, wait an hour before you brush' — sour sweet, a timer at 60, the brush waits behind a WAIT sign ----
def shot_S26(t, n):
    f = set_bathroom(t)
    tw = T("e3", "wait") - 0.1; tb = T("e3", "brush.") - 0.1
    comp(f, scale_el(candy_el("sour"), 1.0), 250, 760 + 5 * math.sin(t * 4), scale=pin(t, st_("S26"), 0.3))
    draw_arrow(f, 350, 760, 440, 760, ramp(t, st_("S26") + 0.3, 0.3), INKC, 8, 26)
    comp(f, timer_el(0.9 * ramp(t, tw, 1.0), "60 MIN", 110), 580, 760, scale=pin(t, tw - 0.1, 0.3))
    draw_arrow(f, 700, 760, 790, 760, ramp(t, tb - 0.3, 0.3), INKC, 8, 26)
    rot_comp(f, scale_el(brush_el(), 0.55), 880, 780, -70, pin(t, tb - 0.2, 0.3), 1.0, 0.3)
    if t >= tw: slam(f, chip("WAIT AN HOUR", ACC, TOOTHW, 38), 540, 920, -4, t, tw)
    chub(f, 540, 1500, 0.9, t=t, la=(60, 40), ra=(150, 175), mouth=talk(t), expr="n", brow="up", look=(0.3, -0.6), lean=3)
    icap(f, "after sour stuff,", "[WAIT] an hour", t, st_("S26") + 0.05, acc=ACC, size=160)
    return finish(f, n, look="fresh")


# ---- S26b: 'the acid softens enamel, and you don't want to scrub it' — a soft, wobbly tooth; the brush shakes 'no' ----
def shot_S26b(t, n):
    f = ink_set("violet", (230, 210, 250), 540, 1000, 440); u = lt(t, "S26b")
    ts = T("e3", "scrub") - 0.1
    el = tooth_el("sad", 0.0, 0.0, False, False, True, (0, 0))
    comp(f, scale_xy(scale_el(el, 1.4), 1 + 0.04 * math.sin(u * 7), 1 - 0.04 * math.sin(u * 7)), 540, 1080)
    acid_pool(f, 540, 1300, 560, 70, t, 1.0, 0.6)
    comp(f, chip("SOFT", ACC_XL, INKC, 32), 540, 760, scale=pin(t, st_("S26b") + 0.1, 0.25))
    if t >= ts:
        rot_comp(f, scale_el(brush_el(), 0.7), 840, 900, -60 + 14 * math.sin((t - ts) * 20), 1.0, 1.0, 0.3)
        comp(f, check_el(44, False), 860, 760, scale=pin(t, ts, 0.25))
    icap(f, "acid softens enamel, so don't", "[SCRUB] it yet", t, st_("S26b") + 0.05, acc=ACC_XL, size=130, dark=True)
    return finish(f, n, look="night")


# ---- S27: 'Brush twice a day with fluoride toothpaste' — Chubby brushes at the mirror (arm IK on the brush grip) ----
def shot_S27(t, n):
    f = set_bathroom(t); u = lt(t, "S27")
    tt = T("e4", "twice") - 0.1
    x, y, s = 540, 1500, 1.1
    mx, my = x + 10, y - 420 * s + 71 * s
    wig = 18 * math.sin(u * 14)
    gx = mx + 290 + wig; gy = my + 36
    sh = (x + 118 * s, y - 261 * s)
    a1, a2 = arm_ik(sh, (gx, gy), 76 * s, 70 * s)
    chub(f, x, y, s, t=t, la=(30, 16), ra=(a1, a2), mouth=1, expr="happy", brow="up", look=(0, -0.6))
    rot_comp(f, scale_el(brush_el(), 0.8), mx + 150 + wig, my + 30, 172 - 3 * math.sin(u * 14), 1.0, 1.0, 0.2)
    grip_hand(f, gx, gy, s * 0.9)
    for i in range(3): cv2.circle(f, (int(x - 30 + 20 * i + 6 * math.sin(u * 9 + i)), int(gy - 70 - 20 * i)), 8 + i * 2, C(WHITE), -1, cv2.LINE_AA)
    if t >= tt: slam(f, chip("2x A DAY · FLUORIDE", INK_MINT, TOOTHW, 36), 540, 760, -4, t, tt)
    comp(f, ichip(SRC_N, 22), 540, 1462, op=clamp((u - 0.4) / 0.3))
    icap(f, "brush", "[TWICE] a day", t, st_("S27") + 0.05, acc=INK_MINT_S, size=170)
    return finish(f, n, look="fresh")


# ---- S27b: 'if a tooth hurts, or you spot a white or brown patch, see a dentist' — tooth under the ink magnifier + chip ----
def shot_S27b(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440); u = lt(t, "S27b")
    th = T("e4", "hurts,") - 0.1; tp = T("e4", "patch,") - 0.1; td = T("e4", "dentist.") - 0.15
    el = tooth_el("ouch" if t >= th else "n", 0.0, 0.0, False, t >= tp)
    comp(f, el, 540, 1080, scale=1.4)
    if t >= tp: cv2.ellipse(f, (600, 1110), (26, 20), 0, 0, 360, C((120, 80, 50)), -1, cv2.LINE_AA)
    if t >= th: sweat_drops(f, 600, 900, t)
    rot_comp(f, scale_el(magnifier_ink_el(), 1.0), 700 + 20 * math.sin(u * 2), 940, -10, pin(t, st_("S27b") + 0.1, 0.3), 1.0, 0.3)
    if t >= td: slam(f, chip("SEE A DENTIST", INKC, TOOTHW, 44), 540, 1400, -4, t, td)
    icap(f, "a sore tooth or a white / brown patch?", "[SEE A DENTIST]", t, st_("S27b") + 0.05, acc=ACC, size=110)
    return finish(f, n, look="fresh")


# ---- S28: RECAP — bacteria eat the sugar -> acid -> spit repairs -> HOW OFTEN ----
def shot_S28(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440)
    items = [(scale_el(bug_el("munch"), 1.3), "BUGS EAT SUGAR"), (scale_el(acid_drop_el(1, "angry"), 1.5), "MAKE ACID"),
             (scale_el(spit_hero_el("happy"), 0.9), "SPIT REPAIRS"), (timer_el(0.9, None, 80), "HOW OFTEN")]
    ts = [T("f1", "bacteria") - 0.15, T("f1", "acid,") - 0.15, T("f1", "spit") - 0.15, T("f1", "often") - 0.15]
    recap_steps(f, items, 1000, t, ts, 262, 0.95)
    icap(f, "", "[REMEMBER]", t, st_("S28") + 0.05, acc=ACC, size=200)
    return finish(f, n, look="fresh")


# ---- S29: send it + FreshNestHub sting ----
def shot_S29(t, n):
    f = set_porch(t) * 0.9
    vend = LINES["f2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("f2", "Send") + 0.3
        comp(f, scale_el(phone2_el("one sweet an hour is fine right??", "nope. that's acid all day!", pr), 0.82), 680, 950, scale=pin(t, st_("S29")))
        if pr and t < T("f2", "Send") + 0.75:
            rr = (t - T("f2", "Send") - 0.3) / 0.45
            cv2.circle(f, (680, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 250, 1500, 0.9, t=t, **POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(1, 0))
        ui_word(f, "send to the friend who nibbles", "[ONE SWEET AN HOUR]", 420, t, T("f2", "friend") - 0.1, col=WHITE, acc=ACC_L, size=100, shadow=0.6, lead_col=WHITE)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=WHITE, lead_size=42, shadow=0.6), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 420, 1520, 0.75, t=t, **POSE["cheer"], mouth=3, expr="happy", brow="up")
        comp(f, tooth_el("happy", 0.0, 0.0), 700, 1380, scale=0.6 * k)
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TROT, 0.4, 18), (T("i2", "right") - 0.1, 0.3, 12), (T("a1", "plaque.") - 0.15, 0.3, 12), (T("a2", "city") - 0.1, 0.3, 10),
           (T("a3", "love") - 0.1, 0.35, 14), (T("a4", "acid.") - 0.15, 0.4, 18), (T("a5", "minerals") - 0.1, 0.25, 8),
           (T("a6", "breaks.") - 0.1, 0.45, 20), (T("a6", "cavity.") - 0.15, 0.35, 14), (T("b1", "rescue") - 0.1, 0.35, 14),
           (st_("S10") + 0.55, 0.3, 12), (T("b3", "washes") - 0.1, 0.25, 8), (T("b4", "patch") + 0.9, 0.25, 8),
           (T("b5", "can't.") - 0.15, 0.3, 12), (st_("S14b") + 0.02, 0.4, 18), (T("c2", "thirty") - 0.15, 0.25, 10),
           (T("c4", "Still") - 0.1, 0.35, 14), (T("c5", "No") - 0.1, 0.4, 16), (T("c6", "much") - 0.1, 0.3, 12), (T("c6", "often.") - 0.15, 0.4, 18),
           (T("d1", "ranking.") - 0.15, 0.3, 12), (T("d2", "stick") - 0.1, 0.35, 14), (T("d3", "own") - 0.1, 0.35, 14),
           (T("d4", "Told") - 0.1, 0.3, 12), (T("e2", "meal,") - 0.1, 0.2, 8), (T("e3", "wait") - 0.1, 0.3, 12),
           (T("e4", "twice") - 0.1, 0.3, 12), (T("e4", "dentist.") - 0.15, 0.3, 12), (T("f2", "Send") + 0.3, 0.2, 8)]


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
        elif k == "iris" and dt < 0.42:
            cx, cy = IRIS.get(sh["id"], (540, 1000))
            f = iris_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, cx, cy)
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
