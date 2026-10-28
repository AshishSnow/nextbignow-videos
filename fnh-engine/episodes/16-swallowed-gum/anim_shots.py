# ================= shots: FreshNestHub 16 — "Does swallowed gum stay in your stomach for 7 years?" =================
# COLOUR SCRIPT (ep 16): warm lamp-gold ROOM/KITCHEN = everyday life (story moments); bubble-gum PINK = the gum itself (diagrams);
# living RED-CORAL tunnel lit from deep inside = INSIDE YOUR GUT (new place set_gut: backlit translucent folds, wet highlights,
# depth fog); X-RAY blue = the route map through the body; night purple = the myth / the catch; GOLDEN dusk = the Stone-Age twist;
# museum spotlight = the open loop (shown at 9 s, paid at 135 s).
# CRAFT (ep 16): INSIDE-THE-BODY WORLD (anim_cine.set_gut) + a SIDE-VIEW peristalsis tube (anim_cine.peri_tube) + a METRO-MAP
# route through the body with a travelling token and hour stamps (anim_fx.route_map).
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "You've") - 0.2, "punch"),
    ("S2", T("i3", "That's") - 0.2, "flash"), ("S2b", T("i3", "And") - 0.15, "whip"), ("S2c", T("i3", "almost") - 0.15, "zoom"),
    ("S3", T("a1", "First,") - 0.2, "whip"), ("S4", T("a2", "The") - 0.2, "focus"), ("S5", T("a3", "But") - 0.2, "whip"),
    ("S6", T("a4", "It's") - 0.2, "zoom"), ("S6b", T("a4", "made") - 0.25, "whip"),
    ("S7", T("a5", "And") - 0.2, "punch"), ("S7b", T("a5", "Enzymes") - 0.15, "whip"), ("S8", T("a6", "So") - 0.2, "iris"),
    ("S9", T("b1", "So") - 0.2, "flash"), ("S10", T("b2", "Here's") - 0.2, "focus"), ("S11", T("b3", "Your") - 0.2, "whip"),
    ("S11b", T("b3", "It") - 0.15, "zoom"), ("S12", T("b4", "That") - 0.2, "whip"), ("S12b", T("b4", "It's") - 0.2, "punch"),
    ("S13", T("b5", "It's") - 0.2, "whip"), ("S14", T("b6", "And") - 0.2, "focus"), ("S14b", T("b6", "about") - 0.2, "whip"),
    ("S15", T("b7", "Scientists") - 0.2, "whip"), ("S15b", T("b7", "It", 1) - 0.15, "zoom"),
    ("S16", T("b8", "Bonus") - 0.2, "flash"), ("S16b", T("b8", "your") - 0.15, "punch"),
    ("S17", T("c1", "So") - 0.2, "flash"), ("S18", T("c2", "Corn") - 0.2, "iris"), ("S19", T("c3", "Experts") - 0.2, "whip"),
    ("S19b", T("c3", "A") - 0.15, "whip"), ("S20", T("c4", "Seven") - 0.2, "punch"), ("S20b", T("c4", "The") - 0.2, "zoom"),
    ("S21", T("d1", "Now,") - 0.2, "flash"), ("S22", T("d2", "Swallowing") - 0.2, "whip"), ("S23", T("d3", "Doctors") - 0.2, "focus"),
    ("S23b", T("d3", "Mostly") - 0.2, "whip"), ("S24", T("d4", "So") - 0.2, "whip"), ("S24b", T("d4", "And") - 0.2, "focus"),
    ("S25", T("e1", "Now,") - 0.2, "flash"), ("S26", T("e2", "In") - 0.2, "whip"), ("S26b", T("e2", "It's") - 0.2, "punch"),
    ("S27", T("e3", "From") - 0.2, "iris"), ("S27b", T("e3", "they") - 0.15, "focus"), ("S28", T("e4", "Now") - 0.2, "whip"),
    ("S29", T("f1", "Remember:") - 0.2, "flash"), ("S30", T("f2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {"S8": (560, 1000), "S18": (540, 980), "S27": (540, 1000)}


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, acc=YEL_, size=170, y=470, out=None, tail=""):   # white caption on dark/colour sets
    ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


GUMC = (255, 150, 190); CTR = 1330


def WAD(s=1.0, seed=1): return scale_el(gum_wad_el(seed), s)


def lit_wad(f, x, y, s, t, col=(255, 190, 160), rot=0.0, seed=1):
    el = WAD(s, seed); rot_comp(f, el, x, y, rot, 1.0, 1.0, 0.3); light_wrap(f, el, x, y, col, 0.55)


def glass_water(f, x, y, w=300, h=380, t=0.0):
    ov = f.copy()
    cv2.rectangle(ov, (int(x - w / 2), int(y - h * 0.75)), (int(x + w / 2), int(y)), C((150, 210, 250)), -1, cv2.LINE_AA)
    f[:] = f * 0.6 + ov * 0.4
    for i in range(6):
        by = y - ((t * 120 + i * 60) % (h * 0.7)); bx = x - w / 3 + (i * 53) % (w * 0.66)
        cv2.circle(f, (int(bx), int(by)), 7, C((235, 248, 255)), 2, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w / 2), int(y - h)), (int(x + w / 2), int(y)), C((235, 248, 255)), 6, cv2.LINE_AA)
    cv2.line(f, (int(x - w / 2 + 26), int(y - h + 30)), (int(x - w / 2 + 26), int(y - 40)), C(WHITE), 8, cv2.LINE_AA)


def growl_waves(f, x, y, t, t0, n=3, col=(255, 230, 160)):
    if t < t0: return
    for i in range(n):
        r = 60 + ((t - t0) * 260 + i * 70) % 220
        a = clamp(1 - (r - 60) / 220)
        for sg in (-1, 1):
            cv2.ellipse(f, (int(x), int(y)), (int(r), int(r * 0.8)), 0, -40 if sg > 0 else 140, 40 if sg > 0 else 220, C(col), max(2, int(8 * a)), cv2.LINE_AA)


def museum(t, dim=0.45):
    f = set_room(t) * dim
    mood(f, (90, 60, 140), 0.25)
    return f


ROUTE_P = body_route_pts(540, 610, 0.88)
ROUTE = [(x, y, nm) for (x, y), nm in zip(ROUTE_P, ROUTE_NAMES)]


def route_xy(k):
    k = clamp(k, 0, len(ROUTE_P) - 1); i = min(int(k), len(ROUTE_P) - 2); fr = k - i
    return ROUTE_P[i][0] + (ROUTE_P[i + 1][0] - ROUTE_P[i][0]) * fr, ROUTE_P[i][1] + (ROUTE_P[i + 1][1] - ROUTE_P[i][1]) * fr


def xray_body(t, op=0.28):
    f = stage("xray")
    chub(f, 540, 1580, 2.42, op=op, shadow=False, look=(0, 0), mouth=0)
    glow(f, 540, 1000, 600, (80, 160, 255), 0.15)
    return f


# ---- S0: HOOK — Chubby blows a giant bubble (already growing at frame 0) -> POP onto his face -> he slurps it in -> GULP ----
TPOP = T("i1", "gum") - 0.05; TGULP = T("i1", "swallow") + 0.05


def shot_S0(t, n):
    f = set_room(t)
    lamp_glow(f, 860, 520, 380, (255, 200, 130), 0.25)
    if t >= TGULP: title3d(f, "GULP!", 640, t, TGULP, size=330, face=GUMC, side=(140, 40, 80), depth=28)
    hx, hy = 470, 1500 - 420 * 1.15
    if t < TPOP:
        chub(f, 470, 1500, 1.15, la=(30, 20), ra=(40, 30), mouth="o", expr="happy", brow="up", look=(0, 0.2), bob=2 * math.sin(t * 4))
        r = 90 + 150 * ramp(t, 0.0, TPOP) + 6 * math.sin(t * 9)
        comp(f, bubble_el(int(r)), hx, hy + 70 + r * 0.55)
    elif t < TGULP:
        chub(f, 470, 1500, 1.15, la=(150, 150), ra=(150, 160), mouth="o", expr="wow", brow="up", look=(0, 0))
        splat(f, hx, hy + 60, 1.0 - 0.6 * ramp(t, TPOP + 0.3, TGULP - TPOP - 0.3), t, TPOP)
        comp(f, burst_el("POP!", GUMC, INK, 60), 760, 760, scale=pin(t, TPOP, 0.2) * (1 - clamp((t - TPOP - 0.5) / 0.15)))
    else:
        k = ramp(t, TGULP, 0.5)
        chub(f, 470, 1500, 1.15, la=(20, 10), ra=(148, -128), mouth=0, expr="wow", brow="up", look=(0.5, 0.5), squash=0.3 * (1 - k))
        lit_wad(f, hx + 6, hy + 150 + 200 * k, 0.28 * (1 - 0.5 * k), t)                       # the lump slides down the throat
        comp(f, burst_el("GULP!", YEL_, INK, 56), 790, 820, scale=pin(t, TGULP, 0.2))
    f = cam(f, 1 + 0.02 * t, 540, 1100)
    f = np.ascontiguousarray(f, np.float32)
    wui(f, "what really happens when you", "[SWALLOW] gum?", t, 0.1, acc=GUMC, size=150, out=TGULP - 0.05)
    return finish(f, n, look="warm")


# ---- S1: the MYTH — the gum sits in a dark stomach 'cell' while the calendar flips to 7 YEARS ----
def shot_S1(t, n):
    f = stage("night", (120, 60, 140), 540, 980, 420); t7 = T("i2", "seven") - 0.1
    if t >= t7: title3d(f, "7 YEARS?", 640, t, t7, size=250, face=(220, 200, 255), side=(70, 40, 120), depth=24)
    comp(f, stomach3_el(), 540, 1060, scale=1.25)
    lit_wad(f, 540, 1110, 0.55, t, (200, 160, 255))
    for k in range(3):                                                    # cobweb = 'stuck for years'
        cv2.line(f, (380, 990), (int(470 + 40 * k), int(1060 + 20 * k)), C((230, 230, 240)), 2, cv2.LINE_AA)
    yr = 1 + min(6, int(max(0.0, t - st_("S1") - 0.3) / max(0.2, (t7 - st_("S1") - 0.3) / 6)))
    rot_comp(f, scale_el(calendar_el("YEAR", str(yr)), 0.5), 860, 760, 6, 1.0, 1.0, 0.25)
    chub_head_only(f, 210, 1380, 0.75, t, mouth="o", expr="sus", brow="sad", look=(1, -0.5))
    if t < t7: wui(f, "it sits in your", "[STOMACH]...", t, st_("S1") + 0.1, acc=(220, 200, 255), size=170)
    return finish(f, n, look="night")


# ---- S2: MYTH -> BUSTED (bright pink set, Chubby smirks, stamp) ----
def shot_S2(t, n):
    f = stage("gumpink", (255, 240, 246), 540, 980, 380); tm = T("i3", "myth.") - 0.05
    rot_comp(f, scale_el(calendar_el("YEARS", "7"), 0.7), 620, 1000, -4, 1.0, 1.0, 0.3)
    chub(f, 250, 1500, 0.9, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="smirk", brow="sus", look=(1, -0.2))
    myth_tag(f, 640, 760, t, st_("S2") + 0.05, tm, 54, "7 YEARS?")
    return finish(f, n, look="fresh")


# ---- S2b: open loop — a covered museum exhibit under a spotlight; Chubby peeks ----
def shot_S2b(t, n):
    f = museum(t)
    pedestal(f, 640, 1110, t)
    cv2.ellipse(f, (640, 1050), (150, 90), 0, 180, 360, C((110, 30, 50)), -1, cv2.LINE_AA)       # the cloth over the exhibit
    cv2.rectangle(f, (490, 1050), (790, 1110), C((110, 30, 50)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (600, 1010), (60, 22), -15, 0, 360, C((150, 50, 74)), -1, cv2.LINE_AA)
    spotlight(f, 640, 1050, 330, 0.6, 200)
    god_rays(f, 640, 250, t, (255, 230, 190), 0.25, 7, 1000, 0.5, 1.57, 3)
    chub(f, 250, 1500, 0.9, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="sus", brow="up", look=(1, -0.3), lean=8)
    comp(f, chip("COMING UP", INK, YEL_, 34), 640, 820, scale=pin(t, st_("S2b") + 0.3, 0.25))
    wui(f, "stick around for the", "[OLDEST] gum", t, st_("S2b") + 0.1, acc=(255, 214, 150), size=170)
    return finish(f, n, look="night")


# ---- S2c: ...a piece of gum almost 6,000 years old (silhouette in the glass case, giant 3D number behind) ----
def shot_S2c(t, n):
    f = museum(t, 0.38); t6 = T("i3", "six") - 0.15
    if t >= t6: title3d(f, "6,000 YEARS", 760, t, t6, size=200, face=(255, 214, 150), side=(110, 60, 20), depth=22)
    pedestal(f, 540, 1200, t)
    el = scale_el(tar_el(), 1.0); comp(f, (el[0] * 0.15, el[1]), 540, 1110)
    glass_case(f, 540, 1195, 360, 300)
    spotlight(f, 540, 1080, 300, 0.55, 180)
    comp(f, chip("?", INK, YEL_, 60), 540, 1110, op=0.9)
    return finish(f, n, look="night")


# ---- S3: PART 1 — what is gum made of? (kitchen, Chubby turns a stick of gum over, 3D 'MADE OF?') ----
def shot_S3(t, n):
    f = set_kitchen(t); tm = T("a1", "made") - 0.15
    if t >= tm: title3d(f, "MADE OF?", 640, t, tm, size=260, face=GUMC, side=(140, 40, 80), depth=24)
    chub(f, 330, 1500, 1.05, la=(-150, -150), ra=(118, 120), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.3),
         hold=scale_el(gum_el(), 0.5), hold_off=(90, -30), hold_front=True)
    counter_front(f, CTR)
    chapter_card(f, t, st_("S3") + 0.05, 1, "WHAT'S IN GUM", y=1440, dur=1.4, col=GUMC)
    return finish(f, n, look="warm")


# ---- S4: exploded view: SUGAR + FLAVOUR (digested, sparkle away) vs the GUM BASE that stays ----
def shot_S4(t, n):
    f = stage("mintg", (220, 255, 236), 540, 1000, 400); td = T("a2", "digests") - 0.1; ts = st_("S4")
    comp(f, scale_el(gum_el(), 0.8), 540, 700, scale=pin(t, ts, 0.3))
    parts = [(220, 1080, "SUGAR"), (540, 1080, "FLAVOUR"), (860, 1080, "GUM BASE")]
    for i, (x, y, nm) in enumerate(parts):
        ti = ts + 0.2 + 0.25 * i
        if t < ti: continue
        k = pin(t, ti, 0.3)
        op = 1 - ramp(t, td + 0.4, 0.5) if i < 2 else 1.0
        if i == 0:
            for j in range(3): rot_comp(f, scale_el(sugar_el("happy"), 0.5), x - 70 + 70 * j, y + 30 * (j % 2), 0, k, op, 0.2)
        elif i == 1: rot_comp(f, scale_el(mint_leaf_el(), 0.9), x, y, -10, k, op, 0.2)
        else: lit_wad(f, x, y, 0.75 * k, t, (220, 255, 236))
        draw_arrow(f, 540, 790, x, y - 110, clamp((t - ti) / 0.3), WHITE, 8, 26, op=max(0.0, op))
        comp(f, chip(nm, INK, WHITE, 30), x, y + 150, op=max(0.0, op) if i < 2 else 1.0)
        if i < 2 and t >= td:
            sparkles(f, x, y, t, td + 0.3, 12, 160, (255, 255, 230))
            if op > 0.02: comp(f, check_el(34, True), x + 70, y - 70, scale=pin(t, td, 0.25), op=op)
    if t >= td + 0.6: comp(f, chip("DIGESTED", (20, 120, 80), WHITE, 34), 380, 1340, scale=pin(t, td + 0.6, 0.25))
    if t >= td - 0.6: wui(f, "your body digests", "[SUGAR] + [FLAVOUR]", t, td - 0.6, acc=(255, 240, 150), size=110)
    else: wui(f, "what's inside", "[GUM]?", t, ts + 0.1, acc=GUMC, size=160, out=td - 0.65)
    return finish(f, n, look="fresh")


# ---- S5: the CHEWY part = GUM BASE (Chubby stretches a long pink string between his hands; 3D title behind) ----
def shot_S5(t, n):
    f = set_kitchen(t); tg = T("a3", "called") - 0.1
    if t >= tg: title3d(f, "GUM BASE", 640, t, tg, size=270, face=GUMC, side=(140, 40, 80), depth=26)
    k = 0.5 + 0.5 * math.sin(lt(t, "S5") * 2.4 - 1.5)
    hands = chub(f, 540, 1500, 1.05, la=(70 + 40 * k, 60 - 30 * k), ra=(70 + 40 * k, 60 - 30 * k), mouth=talk(t), expr="happy", brow="up", look=(0, -0.2))
    (lx, ly), (rx, ry) = hands[-1], hands[1]
    pts = [(lx + (rx - lx) * u, ly + (ry - ly) * u + 70 * math.sin(math.pi * u) * (1.2 - k)) for u in np.linspace(0, 1, 30)]
    a = np.array(pts, np.int32)
    cv2.polylines(f, [a], False, C(GUM_D), 22, cv2.LINE_AA); cv2.polylines(f, [a], False, C(GUM), 15, cv2.LINE_AA)
    cv2.polylines(f, [a + np.array([0, -4], np.int32)], False, C(GUM_H), 4, cv2.LINE_AA)
    for (x, y) in ((lx, ly), (rx, ry)): lit_wad(f, x, y, 0.32, t)
    counter_front(f, CTR)
    if t < tg: wui(f, "but the", "[CHEWY] part", t, st_("S5") + 0.1, acc=GUMC, size=200, out=tg - 0.05)
    return finish(f, n, look="warm")


# ---- S6: close-up of gum base: rubbery RESINS + SOFTENERS (labels on the stretching blob) ----
def shot_S6(t, n):
    f = stage("gumpink", (255, 250, 252), 540, 1020, 420); tr = T("a4", "rubbery") - 0.1; tso = T("a4", "softeners.") - 0.1
    q = math.sin(lt(t, "S6") * 3.0)
    el = scale_xy(WAD(1.6, 3), 1 + 0.12 * q, 1 - 0.08 * q)
    rot_comp(f, el, 540, 1040, 3 * q, 1.0, 1.0, 0.35)
    if t >= tr: label_at(f, "RESINS", 260, 1340, t, tr, 420, 1110, bg=(150, 40, 90))
    if t >= tso: label_at(f, "SOFTENERS", 800, 1360, t, tso, 650, 1120, bg=(150, 40, 90))
    ui_word(f, "a mix of", "[RUBBERY] stuff", 470, t, st_("S6") + 0.1, col=INK, acc=(200, 40, 100), size=150)
    return finish(f, n, look="fresh")


# ---- S6b: made to stay chewy, NOT to dissolve (drop it in water: it stays whole) ----
def shot_S6b(t, n):
    f = stage("sky", (220, 240, 255), 540, 1050, 400); tdi = T("a4", "dissolve.") - 0.1; t0 = st_("S6b") + 0.2
    k = clamp((t - t0) / 0.5)
    y = 700 + 480 * eio(k) + (8 * math.sin(t * 4) if k >= 1 else 0)
    lit_wad(f, 540, y, 0.65, t, (200, 230, 255), rot=40 * k)
    glass_water(f, 540, 1350, 380, 460, t)
    if t >= tdi: comp(f, stamp_el("WON'T DISSOLVE", (40, 110, 200), 54), 540, 1450, scale=pin(t, tdi, 0.25))
    ui_word(f, "made to stay chewy, not to", "[DISSOLVE]", 470, t, st_("S6b") + 0.05, col=INK, acc=(40, 110, 200), size=160)
    return finish(f, n, look="cool")


# ---- S7: an ENZYME (tiny helper) tries to bite the gum: teeth bounce, BOING, dizzy ----
def shot_S7(t, n):
    f = stage("flesh", (255, 170, 160), 540, 1000, 420); tb = T("a5", "break") - 0.15; td = T("a5", "down.") - 0.05
    lit_wad(f, 700, 1050, 1.1, t)
    if t < tb:
        x = 200 + 200 * ramp(t, st_("S7") + 0.2, tb - st_("S7") - 0.2)
        comp(f, scale_el(enz_el(1, chomp(t), "n", (1, 0)), 1.0), x, 1050)
    else:
        bx = 400 - 160 * eo(clamp((t - tb) / 0.4)); rot = 30 * math.sin((t - tb) * 18) * math.exp(-(t - tb) * 3)
        rot_comp(f, scale_el(enz_el(1, 0.3, "dizzy"), 1.0), bx, 1050 - 60 * math.sin(math.pi * clamp((t - tb) / 0.4)), rot, 1.0, 1.0, 0.3)
        comp(f, burst_el("BOING!", YEL_, INK, 52), 560, 800, scale=pin(t, tb, 0.2) * (1 - clamp((t - tb - 0.8) / 0.2)))
    label_at(f, "ENZYME", 240, 1350, t, st_("S7") + 0.3, 260, 1150, bg=(40, 90, 170))
    if t >= td: slam(f, stamp_el("CAN'T CUT IT", RED_, 56), 700, 1400, -5, t, td)
    wui(f, "your body has", "[NO] enzymes for it", t, st_("S7") + 0.1, acc=(255, 200, 120), size=140)
    return finish(f, n)


# ---- S7b: define it: enzymes = TINY HELPERS that cut food into pieces (they snip a carrot into chunks) ----
def shot_S7b(t, n):
    f = stage("cream", (255, 230, 200), 540, 1000, 420); tc = T("a5", "cut") - 0.1
    cuts = int(clamp((t - tc) / 1.0) * 4) if t >= tc else 0
    if not cuts: rot_comp(f, scale_el(carrot_side(0, 0.5), 2.2), 540, 1050, 0, 1.0, 1.0, 0.3)
    else:
        for j in range(cuts + 1):
            dx = (j - cuts / 2) * 170
            rot_comp(f, scale_el(carrot_side(0, 0.5), 2.2 / (cuts + 1)), 540 + dx * 0.9, 1050, 12 * j, 1.0, 1.0, 0.25)
    for j, (x, y) in enumerate(((240, 860), (840, 880), (540, 1270))):
        comp(f, scale_el(enz_el(1, chomp(t + 0.1 * j), "happy", (0.5, 0)), 0.65), x + 10 * math.sin(t * 3 + j), y)
    th = T("a5", "helpers") - 0.15
    if t >= th: label_at(f, "TINY HELPERS", 260, 1440, t, th, 240, 940, bg=(40, 90, 170))
    if t >= tc: comp(f, chip("CUT FOOD INTO PIECES", INK, WHITE, 32), 680, 1440, scale=pin(t, tc, 0.25))
    ui_word(f, "enzymes are", "[TINY HELPERS]", 470, t, st_("S7b") + 0.05, col=INK, acc=(40, 90, 170), size=150)
    return finish(f, n)


# ---- S8: INSIDE YOUR GUT (new place): the gum floats through the living tunnel, still in ONE PIECE ----
def shot_S8(t, n):
    u = lt(t, "S8"); f = set_gut(t)
    k = clamp(u / (en_("S8") - st_("S8")))
    x, y, s = 560 - 40 * k, 1180 - 220 * k, 1.5 - 0.7 * k
    to = T("a6", "one") - 0.15
    if t >= to: title3d(f, "ONE PIECE", 560, t, to, size=250, face=GUMC, side=(140, 40, 80), depth=24)
    lit_wad(f, x, y, s, t, (255, 190, 150), rot=20 * u)
    comp(f, chip("INSIDE YOUR GUT", INK, WHITE, 30), 540, 1440, op=clamp(u / 0.3))
    return finish(f, n, look="warm")


# ---- S9: PART 2 — so why doesn't it get STUCK? (night room, Chubby worried, thought bubble) ----
def shot_S9(t, n):
    f = set_room(t) * 0.5; ts = T("b1", "stuck") - 0.15
    mood(f, (110, 70, 170), 0.3)
    if t >= ts: title3d(f, "STUCK?", 650, t, ts, size=300, face=(220, 200, 255), side=(70, 40, 120), depth=26)
    chub(f, 330, 1500, 1.05, la=(150, -150), ra=(20, 10), mouth=talk(t), expr="sus", brow="sad", look=(1, -0.6))
    rot_comp(f, scale_el(think_el("7 YEARS?"), 0.9), 760, 1060, 0, pin(t, st_("S9") + 0.3, 0.3), 1.0, 0.2)
    chapter_card(f, t, st_("S9") + 0.05, 2, "HOW IT MOVES", y=1440, dur=1.5, col=(220, 200, 255))
    return finish(f, n, look="night")


# ---- S10: no need to digest it to MOVE it (a squeeze ring rushes toward camera, carrying the gum) ----
def shot_S10(t, n):
    u = lt(t, "S10"); D = en_("S10") - st_("S10"); k = clamp(u / D)
    f = set_gut(t, squeeze=0.95 - 0.9 * k)
    s = 0.35 + 1.3 * k ** 1.6
    lit_wad(f, 600 - 60 * k, 860 + 300 * k ** 1.5, s, t, (255, 190, 150), rot=60 * u)
    tm = T("b2", "move") - 0.5
    if t >= tm: wui(f, "it doesn't have to digest it to", "[MOVE] it", t, tm, acc=(255, 220, 120), size=190)
    else: wui(f, "here's the", "[THING]", t, st_("S10") + 0.1, acc=(255, 220, 120), size=190, out=tm - 0.05)
    return finish(f, n, look="warm")


# ---- S11: your gut = a LONG TUBE made of MUSCLE (x-ray Chubby, the route lights up mouth -> out) ----
def shot_S11(t, n):
    f = xray_body(t); tmu = T("b3", "muscle.") - 0.1
    k = 8 * ramp(t, st_("S11") + 0.2, tmu - st_("S11"))
    route_map(f, [(x, y, "") for x, y, _ in ROUTE], k, t, col=(255, 120, 140), dim=0.3)
    if t >= tmu: comp(f, chip("ONE LONG MUSCLE TUBE", (200, 40, 70), WHITE, 34), 540, 1460, scale=pin(t, tmu, 0.25))
    wui(f, "your gut is a long", "[TUBE]", t, st_("S11") + 0.1, acc=(255, 140, 160), size=200)
    return finish(f, n, look="cool")


# ---- S11b: SQUEEZE behind, RELAX in front (side view of the tube, the squeeze pushes the gum along) ----
def shot_S11b(t, n):
    f = stage("flesh", (255, 190, 170), 540, 1000, 200); u = lt(t, "S11b"); D = en_("S11b") - st_("S11b")
    xs = 120 + 600 * clamp(u / D)
    peri_tube(f, 60, 1020, 1000, 120, xs, t, 0.6, cargo=WAD(0.62), label=False)
    tsq = T("b3", "squeezes") - 0.1; trl = T("b3", "relaxes") - 0.1
    if t >= tsq: label_at(f, "SQUEEZE", max(170, xs - 40), 720, t, tsq, xs, 900, bg=(200, 40, 50))
    if t >= trl: label_at(f, "RELAX", min(880, xs + 250), 1320, t, trl, xs + 240, 1110, bg=(60, 130, 200))
    ui_word(f, "squeeze behind, relax", "[IN FRONT]", 470, t, st_("S11b") + 0.05, col=WHITE, acc=(255, 210, 120), size=150, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S12: it rolls along like a WAVE (two squeezes roll down two tube segments, with ghost trails) ----
def shot_S12(t, n):
    f = stage("flesh", (255, 190, 170), 540, 1000, 200); u = lt(t, "S12"); tw = T("b4", "wave.") - 0.15
    for row, (y, off) in enumerate(((820, 0.0), (1200, 0.5))):
        xs = 60 + ((u * 260 + off * 960) % 960)
        peri_tube(f, 40, 1040, y, 100, xs, t + row, 0.6, cargo=WAD(0.5, 1 + row) if row == 0 else None, label=False, wall=40)
        for g in range(1, 4):                                              # ghost trail of where the squeeze was
            gx = xs - 70 * g
            if gx > 60: cv2.circle(f, (int(gx), int(y - 100 - 46)), 9 - 2 * g, C((255, 220, 200)), -1, cv2.LINE_AA)
    wui(f, "the squeeze rolls along like a", "[WAVE]", t, st_("S12") + 0.05, acc=(255, 220, 160), size=200)
    return finish(f, n)


# ---- S12b: it's called PERISTALSIS (giant 3D word inside the glowing tunnel, the squeeze ring passes the camera) ----
def shot_S12b(t, n):
    u = lt(t, "S12b"); f = set_gut(t, squeeze=0.8 - 0.75 * clamp(u / 2.2))
    tp = T("b4", "peristalsis.") - 0.2
    if t >= tp: title3d(f, "PERISTALSIS", 900, t, tp, size=210, face=(255, 236, 214), side=(140, 40, 60), depth=24)
    lit_wad(f, 560, 1180, 0.5, t, (255, 190, 150), rot=30 * u)
    if t >= tp + 0.7: comp(f, chip("= THE SQUEEZE WAVE", INK, WHITE, 34), 540, 1440, scale=pin(t, tp + 0.7, 0.25))
    if t < tp: wui(f, "it's called", "...", t, st_("S12b") + 0.05, acc=(255, 236, 214), size=200)
    return finish(f, n, look="warm")


# ---- S13: like squeezing TOOTHPASTE (split: tube of paste vs your gut, the same move) ----
def shot_S13(t, n):
    f = set_room(t) * 0.8; tt = T("b5", "toothpaste") - 0.2
    k = clamp((t - tt) / 1.4)

    def L(g):
        comp(g, scale_el(toothpaste_el(k), 0.62), 300, 1060)
        paste_ribbon(g, 450, 1062, 40 + 60 * k, t)
        if k > 0: comp(g, chip("SQUEEZE", (200, 40, 50), WHITE, 26), 230, 1200)

    def R(g):
        peri_tube(g, 570, 1010, 1060, 70, 600 + 260 * k, t, 0.6, cargo=WAD(0.38), cargo_dx=80, label=False, wall=30)
    split_contrast(f, t, st_("S13") + 0.02, L, R, "TOOTHPASTE", "YOUR GUT", (60, 140, 220), (200, 50, 80), y0=640, y1=1480, t_r=st_("S13") + 0.3)
    wui(f, "like squeezing", "[TOOTHPASTE]", t, st_("S13") + 0.1, acc=(170, 230, 210), size=170)
    return finish(f, n, look="warm")


# ---- S14: between meals a STRONGER wave (huge squeeze ring sweeps crumbs, a kernel and the gum toward us) ----
def shot_S14(t, n):
    u = lt(t, "S14"); D = en_("S14") - st_("S14"); k = clamp(u / D)
    f = set_gut(t, squeeze=0.9 - 0.85 * k, pal=dict(rim=(255, 130, 110)))
    stuff = [("c", 380, 0.0), ("w", 600, 0.15), ("s", 720, 0.3), ("c", 470, 0.45), ("s", 520, 0.6)]
    for kind, x0, d0 in stuff:
        kk = clamp(k * 1.2 - d0 * 0.3)
        x = 540 + (x0 - 540) * (0.5 + kk); y = 880 + 520 * kk ** 1.5; s = 0.2 + 0.8 * kk ** 1.6
        if kind == "w": lit_wad(f, x, y, s * 0.8, t, rot=50 * u)
        elif kind == "c": rot_comp(f, scale_el(corn_el(), s * 1.2), x, y, 40 * u, 1.0, 1.0, 0.2)
        else: rot_comp(f, scale_el(seed_el(), s * 1.1), x, y, 60 * u, 1.0, 1.0, 0.2)
    mood(f, (255, 90, 90), 0.15)
    wui(f, "between meals, a", "[STRONGER] wave", t, st_("S14") + 0.1, acc=(255, 210, 120), size=170)
    return finish(f, n, look="warm")


# ---- S14b: WHEN? a day timeline: meals = plates; between them, big sweeps every 90 min - 2 h ----
def shot_S14b(t, n):
    f = stage("cream", (255, 236, 214), 540, 1000, 300)
    x0, x1, y0 = 120, 960, 1080
    X = lambda h: x0 + (x1 - x0) * (h - 7) / 16.0
    cv2.line(f, (x0, y0), (x1, y0), C(INK), 8, cv2.LINE_AA)
    for h, lab in ((8, "8 AM"), (13, "1 PM"), (20, "8 PM")):
        comp(f, scale_el(plate_el(), 0.18), X(h), y0 - 40); comp(f, chip(lab, INK, WHITE, 24), X(h), y0 + 50)
    sweeps = [9.7, 11.4, 14.7, 16.4, 18.1, 21.7]
    tn = T("b6", "ninety") - 0.2; k = ramp(t, st_("S14b") + 0.1, 1.6)
    for j, h in enumerate(sweeps):
        if (j + 1) / len(sweeps) > k + 0.01: break
        x = X(h); amp = 120 + 10 * math.sin(t * 6 + j)
        pts = [(x + dx, y0 - amp * math.exp(-(dx / 30) ** 2)) for dx in range(-70, 71, 6)]
        cv2.polylines(f, [np.array(pts, np.int32)], False, C((200, 40, 70)), 10, cv2.LINE_AA)
    if t >= tn:
        a, b = X(sweeps[2]), X(sweeps[3])
        cv2.line(f, (int(a), 860), (int(b), 860), C((200, 40, 70)), 6, cv2.LINE_AA)
        for xx in (a, b): cv2.line(f, (int(xx), 845), (int(xx), 875), C((200, 40, 70)), 6, cv2.LINE_AA)
        comp(f, chip("EVERY 90 MIN - 2 H", (200, 40, 70), WHITE, 34), (a + b) / 2, 790, scale=pin(t, tn, 0.25))
    comp(f, chip("BIG SWEEP WAVES BETWEEN MEALS", INK, WHITE, 28), 540, 1300, op=clamp((t - st_("S14b") - 0.3) / 0.3))
    comp(f, chip("Source: Colorado State University (VIVO Pathophysiology)", INK, WHITE, 22), 540, 1462)
    ui_word(f, "a big sweep about every", "[90 MIN] to [2 H]", 470, t, st_("S14b") + 0.1, col=INK, acc=(200, 40, 70), size=140)
    return finish(f, n)


# ---- S15: scientists call it a HOUSEKEEPING wave (Chubby the housekeeper sweeps with a broom; giant 3D title) ----
def shot_S15(t, n):
    f = set_room(t); th = T("b7", "housekeeping") - 0.15
    if t >= th: title3d(f, "HOUSEKEEPING", 640, t, th, size=200, face=(255, 226, 150), side=(110, 70, 20), depth=24)
    sw = math.sin(lt(t, "S15") * 6)
    chub(f, 440, 1500, 1.05, la=(40 + 15 * sw, 50), ra=(60 + 15 * sw, 40), mouth=talk(t), expr="happy", brow="up", look=(1, 0.4),
         hold=scale_el(broom_el(), 0.75), hold_off=(20 + 30 * sw, 60), hold_front=True)
    dust_puff(f, 640 + 40 * sw, 1480, t, st_("S15") + 0.3 + 0.5 * int(lt(t, "S15") / 0.5), 6, 0.4)
    for j in range(5): rot_comp(f, scale_el(corn_el(), 0.35), 720 + 60 * j + 30 * sw, 1480 - 6 * (j % 2), 20 * j, 1.0, 1.0, 0.2)
    if t < th: wui(f, "scientists call it a", "[HOUSEKEEPING] wave", t, st_("S15") + 0.1, acc=(255, 226, 150), size=120, out=th - 0.05)
    return finish(f, n, look="golden")


# ---- S15b: it sweeps leftovers out of your STOMACH and SMALL INTESTINE (cutaway, leftovers pulse along the route) ----
def shot_S15b(t, n):
    f = stage("flesh", (255, 190, 170), 540, 900, 260); u = lt(t, "S15b")
    comp(f, stomach3_el(), 360, 900, scale=1.0)
    pts = [(470, 1050), (560, 1120), (700, 1080), (840, 1150), (760, 1260), (600, 1250), (480, 1330), (640, 1400), (860, 1380)]
    a = np.array(pts, np.int32)
    cv2.polylines(f, [a], False, C(OUT3), 64, cv2.LINE_AA); cv2.polylines(f, [a], False, C((230, 100, 120)), 52, cv2.LINE_AA)
    cv2.polylines(f, [a], False, C((150, 30, 60)), 24, cv2.LINE_AA)
    allp = [(330, 920), (420, 980)] + pts
    for j in range(5):
        k = (u * 0.45 + j * 0.12) % 1.2
        if k > 1: continue
        px, py = path_point(allp, k)
        if j == 2: lit_wad(f, px, py, 0.22, t)
        elif j == 4: rot_comp(f, scale_el(corn_el(), 0.32), px, py, 30 * u, 1.0, 1.0, 0.2)
        else: cv2.circle(f, (int(px), int(py)), 12, C((250, 220, 160)), -1, cv2.LINE_AA)
    label_at(f, "STOMACH", 300, 690, t, T("b7", "stomach") - 0.2, 340, 790, bg=(150, 40, 70))
    label_at(f, "SMALL INTESTINE", 700, 1470, t, T("b7", "small") - 0.2, 760, 1300, bg=(150, 40, 70))
    ui_word(f, "it sweeps out the", "[LEFTOVERS]", 470, t, st_("S15b") + 0.05, col=WHITE, acc=(255, 220, 160), size=180, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S16: BONUS FACT (midnight, dark kitchen lit only by the open fridge) ----
def shot_S16(t, n):
    f = set_fridge_night(t)
    chub(f, 300, 1500, 1.0, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", look=(1, -0.2))
    mood(f, (120, 170, 255), 0.2)
    comp(f, burst_el("BONUS FACT", YEL_, INK, 60), 560, 800, scale=pin(t, st_("S16") + 0.1, 0.3))
    return finish(f, n, look="cool")


# ---- S16b: ...that wave is why your stomach GROWLS when it's empty (sound rings from his belly, 3D GRRR) ----
def shot_S16b(t, n):
    f = set_fridge_night(t); tg = T("b8", "growls") - 0.15
    if t >= tg: title3d(f, "GRRR!", 640, t, tg, size=320, face=(255, 214, 120), side=(110, 60, 20), depth=28)
    chub(f, 420, 1500, 1.1, la=(40, -60), ra=(40, -60), mouth="o" if t >= tg else talk(t), expr="wow" if t >= tg else "sus", brow="up", look=(0, 0.6),
         squash=0.15 * math.sin(t * 30) if t >= tg else 0.0)
    growl_waves(f, 420, 1260, t, tg)
    comp(f, scale_el(plate_el(), 0.35), 820, 1420)
    comp(f, chip("EMPTY", INK, WHITE, 28), 820, 1330)
    if t < tg: wui(f, "why your stomach", "[GROWLS]", t, st_("S16b") + 0.1, acc=(255, 214, 120), size=200, out=tg - 0.05)
    return finish(f, n, look="cool")


# ---- S17: PART 3 — where does the gum GO? (x-ray route: the gum rides mouth -> stomach -> small intestine with food) ----
def shot_S17(t, n):
    f = xray_body(t); k = 3.2 * ramp(t, st_("S17") + 0.5, en_("S17") - st_("S17") - 0.5)
    route_map(f, ROUTE, k, t, token=WAD(0.3), col=(255, 160, 200))
    for j, el in enumerate((scale_el(corn_el(), 0.3), scale_el(seed_el(), 0.3))):
        px, py = route_xy(max(0.0, k - 0.35 * (j + 1)))
        comp(f, el, px - 40 + 80 * j, py - 30)
    chapter_card(f, t, st_("S17") + 0.05, 3, "THE WAY OUT", y=1440, dur=1.4, col=(255, 160, 200))
    wui(f, "so where does the gum", "[GO]?", t, st_("S17") + 0.1, acc=(255, 160, 200), size=200)
    return finish(f, n, look="cool")


# ---- S18: corn kernels and seeds come out WHOLE too (they float through the tunnel with the gum, labelled) ----
def shot_S18(t, n):
    f = set_gut(t, squeeze=None)
    items = [(scale_el(corn_el(), 0.9), 300, 1080, "CORN", T("c2", "Corn")), (scale_el(seed_el(), 0.9), 780, 1000, "SEEDS", T("c2", "seeds")),
             (WAD(0.7), 560, 1260, "GUM", T("c2", "whole"))]
    for j, (el, x, y, nm, tw) in enumerate(items):
        yy = y + 20 * math.sin(t * 2 + j); rot_comp(f, el, x, yy, 15 * math.sin(t + j), pin(t, st_("S18") + 0.1 * j, 0.3), 1.0, 0.25)
        light_wrap(f, el, x, yy, (255, 190, 150), 0.5)
        if t >= tw - 0.15: label_at(f, nm, x, yy - 190, t, tw - 0.15, x, yy - 70, bg=(120, 20, 50))
    tw_ = T("c2", "whole") - 0.15
    if t >= tw_: comp(f, chip("COME OUT WHOLE", INK, WHITE, 34), 540, 1440, scale=pin(t, tw_, 0.25))
    return finish(f, n, look="warm")


# ---- S19: out in about FORTY HOURS (the token reaches OUT; an hour counter runs 0 -> 40) ----
def shot_S19(t, n):
    f = xray_body(t); t40 = T("c3", "forty") - 0.2
    k = 3.2 + 4.8 * ramp(t, st_("S19") + 0.2, t40 + 0.6 - st_("S19") - 0.2)
    times = ["0 H", "", "", "", "", "", "", "", "~40 H" if k > 7.9 else ""]
    route_map(f, ROUTE, k, t, token=WAD(0.3), col=(255, 160, 200), times=times)
    hrs = int(round(40 * clamp((k - 3.2) / 4.8)))
    wui(f, "out in about", f"[{hrs} HOURS]", t, st_("S19") + 0.1, acc=(255, 160, 200), size=170)
    comp(f, chip("Source: Cleveland Clinic; Mayo Clinic", INK, WHITE, 22), 540, 1462)
    return finish(f, n, look="cool")


# ---- S19b: a DAY OR TWO (bright room, Chubby relaxed with a calendar flipping 1 -> 2) ----
def shot_S19b(t, n):
    f = set_room(t); d = 1 if lt(t, "S19b") < 0.6 else 2
    chub(f, 330, 1500, 1.05, la=(20, 10), ra=(150, 170), mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    rot_comp(f, scale_el(calendar_el("DAY", str(d)), 0.6), 760, 1060, -5, 1.0, 1.0, 0.3)
    wui(f, "a day", "[OR TWO]", t, st_("S19b") + 0.05, acc=(255, 214, 150), size=200)
    return finish(f, n, look="golden")


# ---- S20: 7 years = over 60,000 HOURS (a bar shoots up past the top of the frame, counter spins) ----
def shot_S20(t, n):
    f = stage("cream", (255, 230, 220), 540, 1000, 300); ts = T("c4", "sixty") - 0.2
    k = ramp(t, st_("S20") + 0.2, 1.4)
    hb = int(1380 - 1300 * k)
    f[max(0, hb):1380, 330:530] = np.array(C((150, 110, 220)), np.float32)
    cv2.rectangle(f, (330, max(0, hb)), (530, 1380), C(INK), 6, cv2.LINE_AA)
    comp(f, chip("7 YEARS", INK, WHITE, 30), 430, 1430)
    f[1370:1380, 650:850] = np.array(C(GUMC), np.float32); cv2.rectangle(f, (650, 1368), (850, 1380), C(INK), 4, cv2.LINE_AA)
    comp(f, chip("40 H", INK, WHITE, 26), 750, 1430)
    if t >= ts:
        v = int(count_up(t, ts, 61320, 0.9))
        ui_word(f, "over", f"[{v:,}] hours", 470, t, ts, col=INK, acc=(230, 90, 30), size=140)
    else: ui_word(f, "seven", "[YEARS]", 470, t, st_("S20") + 0.05, col=INK, acc=(120, 70, 200), size=200, out=ts - 0.05)
    f = cam(f, 1.0 + 0.04 * k, 540, 900)
    return finish(f, n)


# ---- S20b: the REAL number? About 40 (a tiny bar; 3D '40 HOURS'; Chubby laughs) ----
def shot_S20b(t, n):
    f = stage("gumpink", (255, 240, 246), 540, 1000, 380); tf = T("c4", "forty.") - 0.2
    if t >= tf: title3d(f, "40 HOURS", 640, t, tf, size=280, face=(255, 255, 255), side=(170, 60, 110), depth=28)
    chub(f, 300, 1500, 1.0, la=(20, 10), ra=(70, 40), mouth=3 if t >= tf else talk(t), expr="happy", brow="up", look=(1, 0.3), bob=4 * math.sin(t * 10) if t >= tf else 0)
    f[1380:1400, 640:840] = np.array(C((200, 40, 100)), np.float32); cv2.rectangle(f, (640, 1378), (840, 1400), C(INK), 4, cv2.LINE_AA)
    lit_wad(f, 740, 1330, 0.35, t)
    if t < tf: wui(f, "the real", "[NUMBER]?", t, st_("S20b") + 0.05, acc=(255, 255, 255), size=200)
    return finish(f, n, look="fresh")


# ---- S21: PART 4 — one honest CATCH (lights drop, red rim) ----
def shot_S21(t, n):
    f = set_room(t) * 0.35
    mood(f, (255, 60, 60), 0.35)
    chub(f, 540, 1500, 1.1, la=(20, 10), ra=(20, 10), mouth=talk(t), expr="n", brow="sus", look=(0, 0))
    spotlight(f, 540, 1100, 360, 0.5, 200)
    chapter_card(f, t, st_("S21") + 0.05, 4, "THE CATCH", y=1440, dur=1.6, col=(255, 140, 120))
    wui(f, "one honest", "[CATCH]", t, st_("S21") + 0.1, acc=(255, 140, 120), size=220)
    return finish(f, n, look="night")


# ---- S22: LOTS of gum, EVERY single DAY (days flip, the pile of swallowed wads grows) ----
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def shot_S22(t, n):
    f = stage("night", (180, 80, 120), 540, 1050, 380); u = lt(t, "S22"); D = en_("S22") - st_("S22")
    d = min(6, int(u / (D / 7)))
    rot_comp(f, scale_el(calendar_el("DAY", DAYS[d]), 0.55), 820, 760, 6, 1.0, 1.0, 0.25)
    comp(f, scale_el(plate_el(), 0.7), 480, 1330)
    rng = np.random.default_rng(4)
    for j in range(3 * (d + 1)):
        x = 480 + rng.uniform(-150, 150) * (1 - j / 30); y = 1290 - 26 * (j // 5) + rng.uniform(-10, 10)
        lit_wad(f, x, y, 0.32, t, (255, 170, 200), rot=rng.uniform(-40, 40), seed=1 + j % 4)
    wui(f, "lots of gum,", "[EVERY] day", t, st_("S22") + 0.1, acc=(255, 170, 200), size=190)
    return finish(f, n, look="night")


# ---- S23: it can CLUMP into a lump that BLOCKS the gut (wads drift together in a red-lit tunnel; BLOCKED) ----
def shot_S23(t, n):
    u = lt(t, "S23"); f = set_gut(t, squeeze=None, pal=dict(glow=(255, 120, 110)))
    mood(f, (255, 40, 40), 0.3)
    tc = T("d3", "clump") - 0.15; tb = T("d3", "blocks") - 0.15
    k = ramp(t, tc, tb - tc + 0.3)
    rng = np.random.default_rng(9)
    for j in range(9):
        a = j / 9 * 2 * math.pi; r0 = 360 * (1 - k) + 60
        x = 560 + r0 * math.cos(a + 0.3 * u) * (1 if j % 2 else 0.8); y = 1000 + r0 * math.sin(a + 0.3 * u) * 0.8
        lit_wad(f, x, y, 0.45 + 0.25 * k, t, (255, 150, 140), rot=rng.uniform(0, 360), seed=1 + j % 4)
    if t >= tb: slam(f, stamp_el("BLOCKED", RED_, 70), 540, 1400, -6, t, tb)
    wui(f, "it can", "[CLUMP]", t, st_("S23") + 0.1, acc=(255, 160, 150), size=210)
    return finish(f, n, look="warm")


# ---- S23b: mostly in YOUNG KIDS (a little Chubby with a pile of gum packs, worried) ----
def shot_S23b(t, n):
    f = set_room(t) * 0.8
    chub(f, 420, 1500, 0.72, la=(20, 10), ra=(118, 120), mouth="o", expr="sus", brow="sad", look=(1, -0.3),
         hold=scale_el(gum_el(), 0.35), hold_off=(60, -20), hold_front=True)
    for j in range(5): rot_comp(f, scale_el(gum_el(), 0.35), 720 + 40 * (j % 3), 1460 - 40 * j, -10 + 8 * j, 1.0, 1.0, 0.2)
    wui(f, "mostly in", "[YOUNG KIDS]", t, st_("S23b") + 0.05, acc=(255, 180, 160), size=180)
    return finish(f, n, look="warm")


# ---- S24: SPIT IT IN THE BIN (kitchen; the gum flies in an arc into the bin; 3D 'BIN IT') ----
def shot_S24(t, n):
    f = set_kitchen(t); tb = T("d4", "bin.") - 0.15; ts = T("d4", "spit") - 0.05
    if t >= tb: title3d(f, "BIN IT", 640, t, tb, size=320, face=(150, 230, 200), side=(30, 100, 80), depth=28)
    sp = ts <= t < ts + 0.4
    chub(f, 300, 1500, 1.05, la=(20, 10), ra=(20, 10), mouth="o" if sp else talk(t), expr="happy", brow="up", look=(1, 0.2), lean=6 if sp else 0)
    counter_front(f, CTR)
    comp(f, bin_el(1.0 if ts <= t < tb + 0.4 else 0.0), 800, CTR - 110, scale=0.85)
    if ts <= t < tb + 0.1:
        k = clamp((t - ts) / max(0.2, tb - ts))
        x = 330 + 470 * k; y = 1030 - 260 * math.sin(math.pi * k) + 200 * k
        lit_wad(f, x, y, 0.2, t, rot=400 * k)
    if t >= tb: comp(f, check_el(50, True), 940, 1000, scale=pin(t, tb, 0.25))
    if t < tb: wui(f, "spit your gum in the", "[BIN]", t, st_("S24") + 0.1, acc=(150, 230, 200), size=200, out=tb - 0.05)
    return finish(f, n, look="warm")


# ---- S24b: the one safe tip: a child swallowed a lot + tummy pain or throwing up -> SEE A DOCTOR ----
def shot_S24b(t, n):
    f = stage("cream", (255, 236, 214), 540, 1000, 300)
    steps = [(T("d4", "child") - 0.1, "A CHILD SWALLOWED A LOT", 760), (T("d4", "tummy") - 0.1, "+ TUMMY PAIN", 900), (T("d4", "throwing") - 0.1, "OR THROWING UP", 1020)]
    for tt, lab, y in steps:
        if t >= tt: comp(f, chip(lab, INK, WHITE, 40), 540, y, scale=pin(t, tt, 0.25))
    td = T("d4", "doctor.") - 0.25
    if t >= td:
        draw_arrow(f, 540, 1080, 540, 1190, clamp((t - td) / 0.25), INK, 10, 30)
        comp(f, chip("SEE A DOCTOR", (200, 40, 50), WHITE, 56), 540, 1290, scale=pin(t, td + 0.1, 0.3))
    for j in range(4): lit_wad(f, 150 + 45 * j, 1200 - 30 * (j % 2), 0.32, t, seed=1 + j % 4)
    chub_head_only(f, 900, 1180, 0.55, t, mouth="o", expr="sus", brow="sad", look=(-0.6, 0))
    ui_word(f, "", "[SAFETY] tip", 470, t, st_("S24b") + 0.1, col=INK, acc=(200, 40, 50), size=170)
    return finish(f, n)


# ---- S25: remember that ANCIENT gum? (museum: the cloth slides off, the lump glows in the case) ----
def shot_S25(t, n):
    f = museum(t, 0.5); k = ramp(t, st_("S25") + 0.4, 0.8)
    pedestal(f, 540, 1200, t)
    comp(f, scale_el(tar_el(), 1.0), 540, 1110)
    glass_case(f, 540, 1195, 360, 300)
    if k < 1:
        cv2.ellipse(f, (int(540 + 500 * k), 1100), (190, 120), int(30 * k), 180, 360, C((110, 30, 50)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(350 + 500 * k), 1100), (int(730 + 500 * k), 1200), C((110, 30, 50)), -1, cv2.LINE_AA)
    spotlight(f, 540, 1080, 320, 0.5, 180)
    god_rays(f, 540, 250, t, (255, 230, 190), 0.3, 7, 1000, 0.5, 1.57, 3)
    if k >= 1: sparkles(f, 540, 1090, t, st_("S25") + 1.2, 10, 220, (255, 230, 180))
    chub(f, 190, 1500, 0.8, la=(150, 170), ra=(20, 10), mouth=talk(t), expr="wow", brow="up", look=(1, -0.4))
    wui(f, "remember that", "[ANCIENT] gum?", t, st_("S25") + 0.1, acc=(255, 214, 150), size=170)
    return finish(f, n, look="golden")


# ---- S26: DENMARK, golden-hour dig: Chubby the explorer holds up a chewed lump of BIRCH TAR ----
def shot_S26(t, n):
    f = set_dusk(t); tb = T("e2", "birch") - 0.15
    birch(f, 140, 1260, 1.0, t); birch(f, 960, 1240, 0.8, t + 1)
    cast_shadow(f, 380, 1482, 230, 420, 0.05, 0.35)
    chub(f, 380, 1480, 1.0, la=(20, 10), ra=(120, 150), mouth=talk(t), expr="wow", brow="up", look=(1, -0.3), shirt=(180, 140, 90),
         hold=scale_el(tar_el(), 0.45), hold_off=(80, -60), hold_front=True)
    comp(f, chip("DENMARK", INK, WHITE, 32), 760, 1380, scale=pin(t, st_("S26") + 0.2, 0.25))
    if t >= tb: label_at(f, "CHEWED BIRCH TAR", 720, 700, t, tb, 560, 880, bg=(110, 60, 30))
    wui(f, "scientists found a chewed lump of", "[BIRCH TAR]", t, st_("S26") + 0.1, acc=(255, 214, 150), size=130)
    return finish(f, n, look="golden")


# ---- S26b: about 5,700 YEARS old (counter spins; giant 3D number behind the glowing lump) ----
def shot_S26b(t, n):
    f = stage("orange", (255, 214, 150), 540, 1000, 420); ty = T("e2", "years") - 0.2
    if t >= ty: title3d(f, "5,700 YEARS", 680, t, ty, size=210, face=(255, 236, 190), side=(120, 50, 10), depth=24)
    el = scale_el(tar_el(), 1.4); rot_comp(f, el, 540, 1080, 5 * math.sin(t), 1.0, 1.0, 0.35); light_wrap(f, el, 540, 1080, (255, 214, 150), 0.6)
    if t < ty:
        v = int(count_up(t, st_("S26b") + 0.2, 5700, 1.0)) if t >= st_("S26b") + 0.2 else 0
        wui(f, "about", f"[{v:,}] years old", t, st_("S26b") + 0.1, acc=(255, 236, 190), size=150)
    comp(f, chip("Source: University of Copenhagen, Nature Communications 2019", INK, WHITE, 22), 540, 1462)
    return finish(f, n, look="golden")


# ---- S27: from the SPIT trapped inside (magnifier: tiny DNA strands inside the lump) ----
def shot_S27(t, n):
    f = stage("orange", (255, 214, 150), 540, 1100, 300)
    comp(f, scale_el(tar_el(), 1.1), 540, 1260)

    def close(g):
        g[:] = stage("cocoa")
        for j in range(4): helix(g, 380 + 110 * j, 960 + 40 * math.sin(j), 230, t + j, gene=(0, 0), w_=60)
    inset(f, 540, 940, 290, close, pin(t, st_("S27") + 0.1, 0.3))
    ts = T("e3", "spit") - 0.1
    if t >= ts: label_at(f, "SPIT = DNA", 540, 1460, t, ts, 540, 1300, bg=(110, 60, 30))
    wui(f, "from the", "[SPIT] inside it", t, st_("S27") + 0.05, acc=(255, 236, 190), size=170)
    return finish(f, n, look="golden")


# ---- S27b: they read the COMPLETE DNA of the WOMAN who chewed it (golden dusk, her figure + the helix) ----
def shot_S27b(t, n):
    f = set_dusk(t); tw = T("e3", "woman") - 0.15; tc = T("e3", "complete") - 0.15
    birch(f, 960, 1240, 0.8, t)
    helix(f, 780, 920, 520, t, gene=(0.0, 1.0), gene_col=(255, 200, 80))
    if t >= tc: label_at(f, "COMPLETE DNA", 780, 600, t, tc, 780, 680, bg=(110, 60, 30))
    if t >= tw:
        stone_woman(f, 330, 1480, 1.05, la=(20, 10), ra=(20, 10), mouth=0, expr="happy", brow="up", look=(1, 0), op=ramp(t, tw, 0.5))
    wui(f, "they read her", "[COMPLETE DNA]", t, st_("S27b") + 0.05, acc=(255, 214, 150), size=140)
    return finish(f, n, look="golden")


# ---- S28: now THAT's gum that really STUCK AROUND (museum, Chubby laughs at the case) ----
def shot_S28(t, n):
    f = museum(t, 0.6); ts = T("e4", "stuck") - 0.15
    if t >= ts: title3d(f, "STUCK AROUND", 640, t, ts, size=200, face=GUMC, side=(140, 40, 80), depth=24)
    pedestal(f, 760, 1200, t); comp(f, scale_el(tar_el(), 0.8), 760, 1130); glass_case(f, 760, 1195, 300, 260)
    spotlight(f, 760, 1080, 280, 0.4, 160)
    chub(f, 300, 1500, 1.0, la=(20, 10), ra=(70, 40), mouth=3 if t >= ts else talk(t), expr="happy", brow="up", look=(1, -0.2), bob=4 * math.sin(t * 9) if t >= ts else 0)
    return finish(f, n, look="golden")


# ---- S29: RECAP — can't digest it -> the gut squeezes it along -> out in about 2 days ----
def _tube_icon():
    g = np.zeros((H, W, 3), np.float32) + np.array(C((255, 236, 244)), np.float32)
    peri_tube(g, 300, 780, 960, 70, 470, 0.0, 0.6, cargo=WAD(0.4), cargo_dx=90, label=False, wall=30)
    crop = np.ascontiguousarray(g[840:1080, 290:790]); a = np.ones(crop.shape[:2], np.float32)
    return scale_el((crop, a), 0.6)


def shot_S29(t, n):
    f = stage("gumpink", (255, 236, 244), 540, 1000, 420)
    tube = gcache("recap_tube", _tube_icon)
    items = [(WAD(0.9), "CAN'T DIGEST IT"), (tube, "GUT SQUEEZES IT"), (scale_el(calendar_el("DAYS", "2"), 0.45), "OUT IN ~2 DAYS")]
    ts = [T("f1", "can't") - 0.15, T("f1", "moves") - 0.15, T("f1", "two") - 0.15]
    recap_steps(f, items, 1000, t, ts, 300, 1.0)
    ui_word(f, "", "[REMEMBER]", 470, t, st_("S29") + 0.05, col=INK, acc=(200, 40, 100), size=200)
    return finish(f, n, look="fresh")


# ---- S30: send it + FreshNestHub sting ----
def shot_S30(t, n):
    f = set_room(t) * 0.8
    vend = LINES["f2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("f2", "Send") + 0.3
        comp(f, scale_el(phone2_el("gum stays 7 years right??", "nope. about 2 days!", pr), 0.82), 680, 950, scale=pin(t, st_("S30")))
        if pr and t < T("f2", "Send") + 0.75:
            rr = (t - T("f2", "Send") - 0.3) / 0.45
            cv2.circle(f, (680, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 250, 1500, 0.85, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", look=(1, 0))
        ui_word(f, "send to the friend who believes the", "[7 YEAR RULE]", 420, t, T("f2", "friend") - 0.1, col=WHITE, acc=GUMC, size=110, shadow=0.6, lead_col=WHITE)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=WHITE, lead_size=42, shadow=0.6), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 400, 1520, 0.75, la=(30, 20), ra=(40, 30), mouth="o", expr="happy", brow="up")
        r = 30 + 45 * ramp(t, vend + 0.3, 1.5)
        comp(f, bubble_el(int(r)), 400, 1520 - 420 * 0.75 + 50 + r * 0.35)
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TPOP, 0.35, 18), (TGULP, 0.35, 14), (T("i2", "seven") - 0.1, 0.3, 12), (T("i3", "myth.") - 0.05, 0.4, 18),
           (T("i3", "six") - 0.15, 0.3, 12), (T("a1", "made") - 0.15, 0.25, 8), (T("a2", "digests") - 0.1, 0.25, 8),
           (T("a3", "called") - 0.1, 0.3, 12), (T("a4", "dissolve.") - 0.1, 0.3, 12), (T("a5", "break") - 0.15, 0.4, 16),
           (T("a5", "down.") - 0.05, 0.3, 12), (T("a6", "one") - 0.15, 0.3, 10), (T("b1", "stuck") - 0.15, 0.35, 14),
           (T("b2", "move") - 0.2, 0.3, 10), (T("b4", "peristalsis.") - 0.2, 0.35, 14), (T("b6", "stronger") - 0.1, 0.35, 14),
           (T("b7", "housekeeping") - 0.15, 0.3, 12), (T("b8", "growls") - 0.15, 0.45, 18), (T("c3", "forty") - 0.2, 0.3, 12),
           (T("c4", "sixty") - 0.2, 0.35, 14), (T("c4", "forty.") - 0.2, 0.4, 18), (T("d1", "catch.") - 0.15, 0.3, 12),
           (T("d3", "blocks") - 0.15, 0.4, 18), (T("d4", "bin.") - 0.15, 0.35, 14), (T("d4", "doctor.") - 0.15, 0.25, 8),
           (T("e2", "years") - 0.2, 0.35, 14), (T("e3", "complete") - 0.15, 0.25, 10), (T("e4", "stuck") - 0.15, 0.35, 14),
           (T("f2", "Send") + 0.3, 0.2, 8)]


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
