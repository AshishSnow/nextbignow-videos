# ================= shots: FreshNestHub 24 — "Does the viral iodine test catch fake paneer?" (Chubby INK, ep 8 of the ink look) ===
# COLOUR SCRIPT: STARCH BLUE = the reaction, titles, chips. AMBER = iodine + oil: it means 'nothing happened'. Warm places for the story, paper + blue panels for the chemistry.
# THE IDEA: iodine is a door guard with ONE photo on the wall. Everything that isn't starch walks right in. The hero craft: SPEED RAMPS (the drop falls in slow motion, on its way to an answer that surprises you).
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Youve") - 0.15, "whip"), ("S1b", T("i2", "One") - 0.12, "zoom"), ("S1c", T("i2", "and") - 0.1, "punch"), ("S2", T("i3", "Its") - 0.2, "flash"), ("S2b", T("i3", "It") - 0.12, "focus"),
    ("S3", T("a1", "Start") - 0.2, "whip"), ("S3b", T("a1", "Puneer") - 0.1, "punch"), ("S4", T("a2", "The") - 0.12, "zoom"), ("S4b", T("a2", "like") - 0.08, "punch"), ("S5", T("a3", "Drain") - 0.12, "whip"), ("S5b", T("a3", "press") - 0.08, "punch"), ("S6", T("a4", "Indias") - 0.12, "flash"), ("S6b", T("a4", "No") - 0.08, "punch"),
    ("S7", T("b1", "But") - 0.2, "whip"), ("S8", T("b2", "So") - 0.2, "flash"), ("S8b", T("b2", "Out") - 0.1, "whip"), ("S8c", T("b2", "and") - 0.08, "punch"), ("S9", T("b3", "And") - 0.15, "flash"), ("S10", T("b4", "The") - 0.15, "whip"), ("S10b", T("b4", "A") - 0.08, "zoom"),
    ("S11", T("c1", "So") - 0.2, "flash"), ("S12", T("c2", "Starch") - 0.12, "focus"), ("S12b", T("c2", "Iodine") - 0.1, "zoom"), ("S13", T("c3", "Lined") - 0.1, "punch"), ("S13b", T("c3", "and") - 0.08, "flash"), ("S14", T("c4", "Milks") - 0.12, "whip"), ("S15", T("c5", "Think") - 0.2, "focus"), ("S15b", T("c5", "Anybody") - 0.1, "whip"),
    ("S16", T("d1", "Quick") - 0.2, "flash"), ("S16b", T("d1", "What") - 0.1, "punch"), ("S17", T("d2", "Brown") - 0.25, "cut"), ("S18", T("d3", "The") - 0.15, "whip"), ("S18b", T("d3", "and") - 0.08, "punch"), ("S19", T("d4", "It") - 0.15, "whip"), ("S19b", T("d4", "Real") - 0.1, "zoom"), ("S19c", T("d4", "and") - 0.08, "punch"), ("S20", T("d5", "So") - 0.2, "flash"), ("S20b", T("d5", "Its", 1) - 0.1, "punch"),
    ("S21", T("e1", "What") - 0.2, "whip"), ("S22", T("e2", "Puneer") - 0.12, "punch"), ("S24", T("e4", "Theres") - 0.15, "focus"), ("S24b", T("e4", "Telling") - 0.1, "whip"),
    ("S25", T("f1", "So") - 0.2, "flash"), ("S26", T("f2", "On") - 0.12, "whip"), ("S26b", T("f2", "If") - 0.08, "zoom"), ("S27", T("f3", "Eating") - 0.12, "whip"), ("S27b", T("f3", "Maharashtra") - 0.1, "zoom"), ("S28", T("f4", "And") - 0.15, "whip"), ("S29", T("f5", "Still") - 0.15, "flash"), ("S29b", T("f5", "Boil") - 0.08, "punch"), ("S29c", T("f5", "Just") - 0.1, "whip"), ("S30", T("f6", "In") - 0.15, "flash"), ("S30b", T("f6", "Its") - 0.08, "punch"),
    ("S31", T("g1", "So") - 0.2, "cut"), ("S32", T("g2", "Now") - 0.15, "whip"),
]


SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}

def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC_S, size=150, y=440, out=None, tail="", dark=False):
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def t3(f, text, y, t, t0, size=230, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def cc(f, text, x, y, t, t0, bg=None, fg=None, size=34):
    if t >= t0: comp(f, chip(text, bg or INKC, fg or MILK, size), x, y, scale=pin(t, t0))


def plate_block(f, x, y, s, mood=None, look=(0, 0), blue=0.0, oil=False, stache=False, scale=1.0):
    comp(f, scale_el(paneer_el(mood, look, blue, oil, stache), s), x, y, scale=scale)


def bite_hand_dropper(f, hx, hy, tipx, t, s=1.0, squeeze=0.0, fill=0.7):
    """an arm from the top right holding the dropper: the 'video hand'."""
    cv2.line(f, (1130, int(hy - 240)), (int(hx), int(hy)), C(INKC), 76, cv2.LINE_AA); cv2.line(f, (1130, int(hy - 240)), (int(hx), int(hy)), C(INK_MINT), 62, cv2.LINE_AA)
    dropper_at(f, tipx, hy + 310 * s, s, squeeze, fill)
    grip_hand(f, hx, hy, 0.95)


def drop_scene(f, t, t0, land, x=560, y0=800, y1=1188, keys=None, s=1.0, col=None):
    """the falling drop on a speed ramp: story time drives gravity. Returns True once it has landed."""
    keys = keys or [(t0, 0.35), (t0 + 0.35, 0.14), (land - 0.65, 0.14), (land - 0.2, 1.0)]
    sl = speed_ramp(land, keys) - speed_ramp(t0, keys); g = 2 * (y1 - y0) / max(1e-3, sl * sl); q = speed_ramp(t, keys) - speed_ramp(t0, keys)
    if t < land:
        yy = y0 + 0.5 * g * q * q; comp(f, scale_el(iod_drop_el(None, col=col), s), x, yy)
        return False
    return True


SRC_T = "Source: FSSAI method via Hyderabad Mail · WebExhibits"
SRC_B = "Source: Business Today, 6 Aug 2026"
SRC_C = "Source: Civilsdaily on the FSSAI draft, 25 Sep 2026"
SRC_TT = "Source: Telangana Today, 12 Jun 2026"
SRC_J = "Source: A. Jana, Technology of Paneer (INFLIBNET) · NIFTEM"
RED_I = (176, 52, 44)
TOP = 1330
TP = T("i1", "pass") - 0.04


# ---- S0: HOOK: frame 0, a drop already falling in SLOW MOTION toward a paneer block; on 'pass' it lands: brown, no blue. PASS slams, the block grows a moustache. Chubby: take + jaw ----
def shot_S0(t, n):
    f = set_worktop(t); land = TP
    rr = t >= land; tk = take(t, land + 0.02)
    chub(f, 190, 1500 + (tk["dy"] if rr else 0), 1.02, t=t, la=(24, 14), ra=(112, 160) if rr else (40, 30), mouth=("jaw" if land + 0.05 < t < land + 0.8 else talk(t)), expr=tk["expr"] if rr else "sus", brow=tk["brow"] if rr else "up", look=(1, 0.4 if rr else -0.3 + 0.7 * t / max(land, 0.1)), lean=tk["lean"] if rr else 5, squash=tk["squash"] if rr else 0, turn=0.5)
    worktop_front(f, TOP)
    comp(f, scale_el(plate_el(), 1.2), 590, 1330)
    bx, by, s_ = 590, 1250, 1.5; tx, ty, rx, ry = top_of(bx, by, s_)
    plate_block(f, bx, by, s_, "n" if not rr else "happy", (0, -0.6) if not rr else (0, 0), stache=rr)
    if rr: stain(f, tx, ty, rx * 0.5, ry * 0.6, ramp(t, land, 0.5), IOD, 3, core=IOD_S)
    bite_hand_dropper(f, 590, 540, 590, t, 0.92, 0.6 if t < 0.25 else 0.0)
    drop_scene(f, t, 0.0, land, 590, 840, ty, keys=[(0.0, 0.45), (0.3, 0.14), (land - 0.6, 0.14), (land - 0.18, 1.0)], s=1.0)
    if land - 0.0 < t < land + 0.4:
        rs_ = (t - land) / 0.4; cv2.ellipse(f, (int(tx), int(ty)), (int(40 + 200 * rs_), int(14 + 70 * rs_)), 0, 0, 360, C(IOD), max(1, int(9 * (1 - rs_))), cv2.LINE_AA)
    if rr: slam(f, stamp_el("PASS", GOOD, 100), 770, 980, -7, t, land + 0.05)
    if rr: cc(f, "NO BLUE", 350, 1060, t, land + 0.3, IOD_S, MILK, 40)
    slowmo_frame(f, t, 1.0 - ramp(t, land - 0.2, 0.2))
    icap(f, "do you know the blue test", "can [PASS] a fake?", t, 0.04, size=112, y=330)
    return finish(f, n, look="warm")


# ---- S1: 'You've seen the video.' a phone: hands, a paneer cube, hearts floating up ----
def shot_S1(t, n):
    f = set_droom(t, dim=0.15); t0 = st_("S1")
    x0, y0, x1, y1 = phone_frame(f, 610, 900, 560, 1000)
    pk = pin(t, t0 + 0.02)
    plate_block(f, (x0 + x1) // 2, y1 - 300, 1.1, None)
    cc(f, "FAKE OR REAL?", (x0 + x1) // 2, y0 + 110, t, t0 + 0.05, RED_I, MILK, 44)
    for j in range(6):
        p = ((t - t0) * 0.5 + j * 0.17) % 1
        comp(f, scale_el(heart_el(), 0.7), x1 - 50 + 18 * math.sin(p * 8 + j), y1 - 90 - p * 460, op=clamp(3 * (1 - p)))
    chub(f, 200, 1500, 1.02, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="smirk", brow="up", look=(1, -0.1), hand_r="point", turn=0.5)
    table_front(f, TOP + 80)
    icap(f, "you've seen", "the [VIDEO]", t, t0 + 0.04, size=120, y=320)
    return finish(f, n, look="warm")


# ---- S1b: 'One drop of iodine, it turns blue': inside the phone's picture: the stain BLOOMS, speed-ramped: fast then slow ----
def shot_S1b(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1040, 560); t0 = st_("S1b"); tb = T("i2", "blue") - 0.3; ti = T("i2", "iodine") - 0.1
    bx, by, s_ = 540, 1190, 2.4; tx, ty, rx, ry = top_of(bx, by, s_)
    comp(f, scale_el(paneer_el(), s_), bx, by)
    dropper_at(f, 540, 850 if t < tb else 850 - 900 * ramp(t, tb, 0.25), 1.0, 0.0)
    if t < tb: drop_scene(f, t, t0, tb, 540, 860, ty, keys=[(t0, 1.0), (tb, 1.0)], s=0.9)
    else:
        k = speed_ramp(t, [(tb, 2.4), (tb + 0.35, 0.4), (tb + 1.4, 0.15)]) - speed_ramp(tb, [(tb, 2.4), (tb + 0.35, 0.4), (tb + 1.4, 0.15)])
        stain(f, tx, ty, rx * 0.95, ry * 0.95, clamp(k * 1.05), ACC_S, 3)
    if t >= ti: cc(f, "IODINE", 800, 720, t, ti, IOD_S, MILK, 48)
    if t >= tb: t3(f, "BLUE", 420, t, tb, 220)
    else: icap(f, "one", "[DROP]", t, t0 + 0.03, acc=IOD_S, size=130, y=360)
    return finish(f, n, look="fresh")


# ---- S1c: 'everybody screams fake': a row of three faces, jaws down, FAKE slams ----
def shot_S1c(t, n):
    f = set_droom(t); t0 = st_("S1c"); tf = T("i2", "fake") - 0.15
    for i, (x, kind, shirt, s_, seed) in enumerate(((210, "aunty", (230, 70, 130), 0.92, 1), (540, None, None, 1.1, 2), (870, "cousin", (70, 130, 190), 0.92, 3))):
        kw = dict(shirt=shirt) if shirt else {}
        w_ = 6 * math.sin(t * 15 + i)
        chub(f, x, 1500, s_, t=t, la=(112, 150 + w_), ra=(112, 150 - w_), mouth="jaw", expr="wow", brow="up", look=(0.0, 0.3), lean=w_ * 0.6, **kw)
        if kind: dress(f, x, 1500, s_, kind, w_ * 0.6)
    comp(f, scale_el(paneer_el("sad", blue=1.0), 0.8), 540, 1340 - 10 * math.sin(t * 9))
    if t >= tf: slam(f, burst_el("FAKE!", (255, 220, 90), RED_I, 96), 540, 680, -6, t, tf)
    return finish(f, n, look="warm")


# ---- S2: 'It's a real test.' Chubby in a lab coat, a calm nod, REAL TEST; S2b: 'It just isn't testing what you think it's testing.' a magnifier on the label: a big question mark ----
def shot_S2(t, n):
    f = set_worktop(t); t0 = st_("S2"); tr = T("i3", "real") - 0.15
    chub(f, 300, 1500, 1.04, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.1), turn=0.45, lean=2 * math.sin(t * 2))
    worktop_front(f, TOP)
    comp(f, scale_el(bottle_el(), 0.74), 760, 1120, scale=pin(t, t0 + 0.05))
    if t >= tr: t3(f, "REAL TEST", 480, t, tr, 170)
    return finish(f, n, look="fresh")


def shot_S2b(t, n):
    f = set_worktop(t, blur=6); t0 = st_("S2b"); tt = T("i3", "think") - 0.15
    f = f * 0.55 + 0.45 * np.array(C((230, 232, 250)), np.float32)
    chub(f, 300, 1500, 1.3, t=t, **nolean(POSE["whisper"]), mouth=talk(t), expr="smirk", brow="up", look=(1, -0.2), turn=0.5)
    comp(f, scale_el(bottle_el(), 0.86), 790, 1260)
    if t >= tt:
        t3(f, "?", 860, t, tt, 300, x=790)
    icap(f, "it isn't testing what", "you [THINK]", t, t0 + 0.04, size=120, y=400)
    return finish(f, n, look="cool")


# ---- S3: 'Start with the real stuff.' a pot of milk on the stove; S3b: 'hot milk and something sour': he squeezes a lemon, drip ----
def shot_S3(t, n):
    f = set_stove(t, on=0.8, flame_w=300); f = inkify(f, 0.1); t0 = st_("S3")
    comp(f, scale_el(pot_el("steel", 0.66), 1.0), 590, 1300 - 225 + 8); side_flames(f, 590, 1298, t, 300, 0.8); steam_wisps(f, 590, 880, t, 4, 180, 160)
    chub(f, 190, 1500, 0.98, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy", brow="up", look=(1, 0.2), hand_r="point", turn=0.5)
    icap(f, "start with the", "[REAL] stuff", t, t0 + 0.04, size=120, y=360)
    return finish(f, n, look="warm")


def shot_S3b(t, n):
    f = set_stove(t, on=0.8, flame_w=300); f = inkify(f, 0.1); t0 = st_("S3b"); tm = T("a1", "milk") - 0.1; ts = T("a1", "sour") - 0.2
    comp(f, scale_el(pot_el("steel", 0.66), 1.0), 590, 1083); side_flames(f, 590, 1298, t, 300, 0.8); steam_wisps(f, 590, 880, t, 3, 150, 140)
    sq = t > ts; hs = chub(f, 215, 1500, 1.02, t=t, la=(24, 14), ra=(120, 150), mouth=talk(t), expr="smirk" if sq else "happy", brow="up", look=(1, 0.1), hand_r="grip", turn=0.5)
    hx, hy = hs[1]; rot_comp(f, scale_el(lemon_ink_el(True), 0.72 - (0.05 if sq else 0)), hx + 56, hy + 6, 30, 1.0, 1.0, 0)
    if sq:
        for j in range(3):
            p = ((t - ts) * 2.2 + j * 0.33) % 1; comp(f, scale_el(iod_drop_el(None, col=(230, 230, 110)), 0.34), hx + 74, hy + 60 + 180 * p * p)
    cc(f, "HOT MILK", 720, 660, t, tm, ACC_S, MILK, 50); 
    if t >= ts: cc(f, "+ SOMETHING SOUR", 720, 750, t, ts, INKC, MILK, 44)
    return finish(f, n, look="warm")


# ---- S4: 'The sour makes the milk protein clump together, and those clumps catch the fat' — the net forms; S4b: 'like a net catching fish' — the balls of fat become fish ----
def shot_S4(t, n):
    f = ink_set("amberp", (255, 250, 230), 540, 1000, 520); t0 = st_("S4"); tc = T("a2", "clump") - 0.15; ta = T("a2", "catch") - 0.1
    k = ramp(t, tc, ta - tc + 0.4)
    net_catch(f, 540, 1040, 860, 700, k, t)
    cc(f, "MILK PROTEIN", 330, 610, t, T("a2", "protein") - 0.15, INKC, MILK, 34)
    if t >= ta: cc(f, "FAT", 760, 610, t, ta, OIL_S, MILK, 40)
    icap(f, "the protein", "[CLUMPS]", t, t0 + 0.04, size=120, y=400)
    return finish(f, n, look="warm")


def shot_S4b(t, n):
    f = ink_set("amberp", (255, 250, 230), 540, 1000, 520); t0 = st_("S4b")
    net_catch(f, 540, 1040, 860, 700, 1.0, t, fish=True)
    icap(f, "like a net catching", "[FISH]", t, t0 + 0.04, size=140, y=400)
    return finish(f, n, look="warm")


# ---- S5: 'Drain off the watery part' a muslin bundle drips; S5b: 'press it, and that's your block' a weight slams, a happy block ----
def shot_S5(t, n):
    f = set_worktop(t); t0 = st_("S5")
    worktop_front(f, TOP)
    comp(f, scale_el(bowl_el(0.3 + 0.3 * ramp(t, t0, 1.2), (222, 228, 180)), 1.5), 600, 1210)
    comp(f, scale_el(muslin_el(), 1.0), 600, 800 + 8 * math.sin(t * 2))
    for j in range(4):
        p = ((t - t0) * 1.5 + j * 0.25) % 1; comp(f, scale_el(iod_drop_el(None, col=(214, 224, 170)), 0.42), 560 + j * 28, 985 + 170 * p * p)
    cv2.line(f, (500, 480), (700, 480), C(INKC), 12, cv2.LINE_AA); cv2.line(f, (600, 480), (600, 625), C(INKC), 7, cv2.LINE_AA)
    chub(f, 190, 1500, 0.96, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="n", brow="up", look=(1, -0.2), turn=0.5)
    icap(f, "drain the", "[WATERY] part", t, t0 + 0.04, size=110, y=350, acc=(120, 140, 70))
    return finish(f, n, look="fresh")


def shot_S5b(t, n):
    f = set_worktop(t); t0 = st_("S5b"); tb = T("a3", "block") - 0.2
    worktop_front(f, TOP)
    hit = t >= t0 + 0.12; yw = drop_land(t, t0, 300, 900, 0.14)[0]
    sq = 0.84 if hit else 1.0
    el = scale_xy(scale_el(paneer_el("happy" if t > tb else "wow"), 1.85), 1 + (1 - sq), sq) if hit else scale_el(paneer_el("wow"), 1.85)
    comp(f, el, 560, 1210)
    if t < tb: comp(f, scale_el(weight_el(""), 1.2), 560, yw)
    if t >= tb: t3(f, "PANEER", 660, t, tb, 220, PAN, IOD)
    chub(f, 190, 1500, 0.92, t=t, **nolean(POSE["tada"] if t > tb else POSE["point"]), mouth=talk(t), expr="happy", brow="up", look=(1, 0.1), turn=0.4)
    worktop_front(f, TOP + 60)
    return finish(f, n, look="warm")


# ---- S6: 'India's food rules say it can only come from milk' a scroll, a can with a tick; S6b: 'No vegetable oil.' an oil bottle, a stamp ----
def shot_S6(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 500); t0 = st_("S6"); to = T("a4", "only") - 0.15
    scroll(f, 300, 570, 420, 780, ramp(t, t0, 0.7), t)
    cc(f, "FOOD RULES", 300, 620, t, t0 + 0.2, INKC, MILK, 34)
    if t > t0 + 0.4: 
        for j, x1 in enumerate((440, 420, 460, 400)): cv2.line(f, (170, 760 + j * 66), (x1, 760 + j * 66), C((170, 160, 140)), 7, cv2.LINE_AA)
    comp(f, scale_el(milk_can_el("happy"), 1.1), 760, 1090, scale=pin(t, to))
    if t >= to: comp(f, check_el(70, True), 900, 830, scale=pin(t, to + 0.1)); icap(f, "only from", "[MILK]", t, to, size=130, y=400)
    src(f, SRC_C, t, t0 + 0.4, 1440)
    return finish(f, n, look="warm")


def shot_S6b(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 500); t0 = st_("S6b")
    comp(f, scale_el(oil_bottle_el(), 1.2), 540, 1040)
    slam(f, stamp_el("NOT ALLOWED", RED_I, 84), 540, 1120, -8, t, t0 + 0.14)
    icap(f, "no", "[VEGETABLE OIL]", t, t0 + 0.02, acc=OIL_S, size=100, y=500)
    return finish(f, n, look="warm")


# ---- S7: 'But milk's expensive, and vegetable oil isn't.' a seesaw of coins ----
def shot_S7(t, n):
    f = ink_set("amberp", (255, 250, 230), 540, 1000, 500); t0 = st_("S7"); te = T("b1", "vegetable") - 0.1
    tilt = 11 * ramp(t, t0 + 0.1, 0.4)
    a = math.radians(tilt); cx, cy = 540, 1260; L = 380; dx, dy = L * math.cos(a), L * math.sin(a)
    cv2.line(f, (int(cx - dx), int(cy - dy * -1)), (int(cx + dx), int(cy + dy * -1)), C(INKC), 30, cv2.LINE_AA); cv2.line(f, (int(cx - dx), int(cy + dy)), (int(cx + dx), int(cy - dy)), C((180, 130, 80)), 16, cv2.LINE_AA)
    P = np.array([(cx, cy + 10), (cx - 60, cy + 150), (cx + 60, cy + 150)], np.int32); cv2.fillPoly(f, [P], C((120, 90, 60)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 7, cv2.LINE_AA)
    lx, ly = cx - dx * 0.8, cy + dy * 0.8; rx_, ry_ = cx + dx * 0.8, cy - dy * 0.8
    comp(f, scale_el(milk_can_el("wow"), 0.82), lx, ly - 170)
    for j in range(6): comp(f, scale_el(coin_el(44), 1.0), lx + 104 + (j % 2) * 8, ly - 26 - j * 26)
    comp(f, scale_el(oil_bottle_el(), 0.74), rx_, ry_ - 190)
    if t >= te: comp(f, scale_el(coin_el(44), 1.0), rx_ - 110, ry_ - 26, scale=pin(t, te))
    icap(f, "milk is", "[EXPENSIVE]", t, t0 + 0.04, size=120, y=400, acc=IOD_S, out=te)
    if t >= te: icap(f, "vegetable oil", "[ISN'T]", t, te, size=130, y=400, acc=OIL_S)
    return finish(f, n, look="golden")


# ---- S8: 'So there's a lookalike called analogue paneer.' two blocks; one puts on a moustache. S8b: 'Out goes the milk fat, in goes vegetable oil, maybe some starch' — cut-away block. S8c: 'it can cost about half.' ----
def shot_S8(t, n):
    f = set_worktop(t); t0 = st_("S8"); ta = T("b2", "analogue") - 0.15
    worktop_front(f, TOP)
    plate_block(f, 300, 1220, 1.5, "n", (1, 0)); cc(f, "MILK PANEER", 300, 1420, t, t0 + 0.08, INKC, MILK, 32)
    st = t >= ta
    plate_block(f, 770, 1220, 1.5, "smirk" if st else "n", (-1, 0), stache=st, oil=st)
    if st: cc(f, "ANALOGUE PANEER", 770, 1420, t, ta, ACC_S, MILK, 32)
    if st: t3(f, "LOOKALIKE", 620, t, ta, 150)
    else: icap(f, "there's a", "[LOOKALIKE]", t, t0 + 0.04, size=120, y=620)
    src(f, SRC_B, t, ta + 0.3, 1492)
    return finish(f, n, look="fresh")


def shot_S8b(t, n):
    f = ink_set("amberp", (255, 250, 230), 540, 1000, 500); t0 = st_("S8b"); ti = T("b2", "in") - 0.1; ts = T("b2", "maybe") - 0.1
    plate_block(f, 540, 1190, 2.2, "wow" if t > ti else "n", (0, -0.5), oil=t > ti + 0.3, stache=t > ts + 0.2)
    k = ramp(t, t0 + 0.05, 0.6); comp(f, scale_el(milkfat_el(), 1.9), 300 - 150 * k, 880 - 60 * k); cc(f, "MILK FAT: OUT", 300, 680, t, t0 + 0.05, IOD_S, MILK, 36)
    if t >= ti:
        k2 = ramp(t, ti, 0.4); comp(f, scale_el(oil_drop_el("happy"), 0.9), 620 + 200 * (1 - k2), 880 - 120 * (1 - k2)); cc(f, "VEG OIL: IN", 790, 680, t, ti, OIL_S, MILK, 36)
    if t >= ts:
        comp(f, scale_el(starch_guy_el("smirk" if False else "sus"), 0.5), 850, 1020, scale=pin(t, ts)); cc(f, "MAYBE STARCH", 840, 1230, t, ts, ACC_S, MILK, 32)
    return finish(f, n, look="golden")


def shot_S8c(t, n):
    f = set_worktop(t); t0 = st_("S8c"); th = T("b2", "half") - 0.2
    worktop_front(f, TOP)
    comp(f, scale_el(tag_el2(), 1.5), 620, 900, scale=pin(t, t0))
    cc(f, "PRICE", 620, 860, t, t0 + 0.05, INKC, MILK, 40)
    if t >= th: t3(f, "ABOUT 1/2", 480, t, th, 170)
    if t >= th: comp(f, chip("50-60 % CHEAPER", ACC_S, MILK, 44), 630, 950, scale=pin(t, th))
    plate_block(f, 620, 1240, 1.15, "smirk", (-0.8, 0), stache=True, oil=True)
    chub(f, 200, 1500, 0.94, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.1), turn=0.5)
    worktop_front(f, TOP + 70)
    src(f, SRC_TT, t, th, 1492)
    return finish(f, n, look="fresh")


# ---- S9: 'And the surprise is that it's legal, as long as the label says what it is.' double take, a packet with the word on it ----
def shot_S9(t, n):
    f = set_worktop(t); t0 = st_("S9"); tg = T("b3", "legal") - 0.15; tl = T("b3", "label") - 0.15
    lk, le, ex, br = double_take(t, t0 + 0.1)
    chub(f, 215, 1500, 1.02, t=t, **nolean(POSE["cheek"]), mouth=talk(t), expr=ex, brow=br, look=lk if t < t0 + 0.8 else (1, 0), lean=le, turn=0.5)
    worktop_front(f, TOP)
    comp(f, scale_el(packet_el(), 1.25), 730, 1020, scale=pin(t, t0 + 0.05))
    cc(f, "PANEER-LIKE", 730, 850, t, t0 + 0.1, INKC, MILK, 36)
    if t >= tl:
        cc(f, "ANALOGUE", 730, 1040, t, tl, ACC_S, MILK, 70); 
    if t >= tg: t3(f, "LEGAL", 490, t, tg, 200, (190, 230, 200), GOOD)
    else: icap(f, "the", "[SURPRISE]?", t, t0 + 0.04, size=130, y=490)
    src(f, SRC_B, t, tl, 1492)
    return finish(f, n, look="fresh")


# ---- S10: 'The trouble is your plate.' the diner: a plate lands; S10b: 'A paneer tikka doesn't come with a label.' he looks under the plate with a magnifier ----
def shot_S10(t, n):
    f = set_diner(t); t0 = st_("S10"); tp = T("b4", "plate") - 0.2
    chub(f, 540, 1500, 1.08, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(0, 0.3))
    diner_front(f, TOP)
    if t >= tp:
        y_ = drop_land(t, tp, 800, 1320, 0.2)[0]; comp(f, scale_el(tikka_el(), 1.25), 540, y_)
    icap(f, "the trouble is your", "[PLATE]", t, t0 + 0.04, size=130, y=420, dark=True, acc=(255, 232, 150))
    return finish(f, n, look="warm")


def shot_S10b(t, n):
    f = set_diner(t); t0 = st_("S10b"); tl = T("b4", "label") - 0.15
    hs = chub(f, 240, 1500, 1.04, t=t, la=(24, 14), ra=(96, 80 + 16 * math.sin(t * 7)), mouth=talk(t), expr="sus", brow="sus", look=(1, 0.5), turn=0.5, hand_r="grip", lean=8)
    diner_front(f, TOP)
    comp(f, scale_el(tikka_el(), 1.25), 640, 1300)
    hx, hy = hs[1]; rot_comp(f, scale_el(magnifier_ink_el(), 0.8), hx + 170 + 120 * math.sin(t * 3), hy - 70, -30, 1.0, 1.0, 0)
    if t >= tl: slam(f, chip("NO LABEL", RED_I, MILK, 84), 620, 860, -5, t, tl)
    return finish(f, n, look="warm")


# ---- S11: re-hook 'So where does the blue come from?' a blue blot fills the frame, Chubby in it, head scratch ----
def shot_S11(t, n):
    f = ink_set("bluep", (255, 255, 255), 540, 1000, 520); t0 = st_("S11"); tb = T("c1", "blue") - 0.15
    stain(f, 540, 1010, 460, 420, ramp(t, t0, 0.5), ACC, 7, op=0.9, core=ACC_S)
    chub(f, 540, 1500, 1.15, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="sus", brow="sus", look=(0.2, -0.5), lean=3 * math.sin(t * 3))
    if t >= tb: t3(f, "BLUE?", 470, t, tb, 220)
    return finish(f, n, look="cool")


# ---- S12: 'Starch has a long chain in it that coils up like a spring.' the chain coils; S12b: 'Iodine gets stuck inside that coil, in a straight line.' the amber beads fly in ----
def shot_S12(t, n):
    f = ink_set("bluep", (255, 255, 255), 540, 980, 500); t0 = st_("S12"); tc = T("c2", "coils") - 0.1; 
    coil = ramp(t, tc, 0.8)
    helix(f, 540, 1000, 780, coil, t)
    cc(f, "STARCH CHAIN", 540, 1260, t, t0 + 0.2, INKC, MILK, 34)
    if t >= T("c2", "spring") - 0.2: icap(f, "coils up like a", "[SPRING]", t, T("c2", "spring") - 0.2, size=130, y=420)
    else: icap(f, "inside", "[STARCH]", t, t0 + 0.04, size=130, y=420)
    src(f, "Source: WebExhibits, Causes of Color", t, t0 + 0.4, 1462)
    return finish(f, n, look="fresh")


def shot_S12b(t, n):
    f = ink_set("bluep", (255, 255, 255), 540, 980, 500); t0 = st_("S12b"); ts = T("c2", "straight") - 0.1
    helix(f, 540, 1000, 780, 1.0, t, 0.0, ramp(t, t0, en_("S12b") - t0 - 0.2))
    cc(f, "IODINE", 820, 780, t, t0 + 0.05, IOD_S, MILK, 40)
    chub_head_only(f, 170, 1400, 0.8, t=t, mouth=talk(t), expr="wow", brow="up", look=(1, -0.7), turn=0.5)
    if t >= ts: draw_arrow(f, 160, 1000, 930, 1000, 1.0, INKC, 6, 30, 0.0) if False else None; cc(f, "IN A STRAIGHT LINE", 540, 1260, t, ts, IOD_S, MILK, 44)
    icap(f, "iodine gets", "[STUCK]", t, t0 + 0.04, acc=IOD_S, size=130, y=420)
    return finish(f, n, look="fresh")


# ---- S13: 'Lined up like that, it soaks up light differently' — colours go in; S13b: 'and you see blue black.' the spring goes dark, one blue beam out ----
def shot_S13(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 520); t0 = st_("S13")
    helix(f, 540, 1020, 500, 1.0, t, 0.3, 1.0, R=110, turns=3.0, nb=5)
    light_in_out(f, 540, 1020, t, ramp(t, t0, 0.5), 0.0)
    cc(f, "LIGHT", 170, 830, t, t0 + 0.1, INKC, MILK, 40)
    icap(f, "it soaks up", "[LIGHT]", t, t0 + 0.04, size=130, y=420)
    return finish(f, n, look="fresh")


def shot_S13b(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 520); t0 = st_("S13b"); tb = T("c3", "blue") - 0.15
    k = ramp(t, t0, 0.4)
    helix(f, 540, 1020, 500, 1.0, t, 0.3 + 0.7 * k, 1.0, R=110, turns=3.0, nb=5)
    light_in_out(f, 540, 1020, t, 1.0, ramp(t, tb - 0.1, 0.3))
    if t >= tb: t3(f, "BLUE-BLACK", 470, t, tb, 150)
    chub_head_only(f, 910, 1400, 0.8, t=t, mouth=talk(t), expr="happy", brow="up", look=(-1, -0.6), turn=-0.5)
    return finish(f, n, look="cool")


# ---- S14: 'Milk's got no starch, so iodine in milk just stays brown.' a glass of milk, a drop, nothing happens; Chubby deadpan ----
def shot_S14(t, n):
    f = set_worktop(t); t0 = st_("S14"); tb = T("c4", "brown") - 0.2; tl = t0 + 0.5
    chub(f, 210, 1500, 1.0, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="n", brow="up", look=(1, 0.1), turn=0.5)
    worktop_front(f, TOP)
    comp(f, scale_el(glass2_el(), 1.0), 680, 1180)
    dropper_at(f, 680, 760 if t < tl + 0.1 else 760 - 900 * ramp(t, tl + 0.1, 0.25), 0.8)
    if not drop_scene(f, t, t0, tl, 680, 770, 1095, keys=[(t0, 1.0), (tl, 1.0)], s=0.7):
        stain(f, 680, 1100, 56, 14, ramp(t, tl, 0.4), IOD, 4, core=IOD_S)
    cc(f, "NO STARCH", 860, 930, t, T("c4", "no") - 0.1, ACC_S, MILK, 40)
    if t >= tb: t3(f, "BROWN", 470, t, tb, 200, IOD_L, IOD_S)
    return finish(f, n, look="fresh")


# ---- S15: 'Think of iodine as a guard with one photo on the wall. Starch.' S15b: 'Anybody else walks right in.' ----
WALL = (232, 218, 196)
def corridor_wall(t):
    f = ink_set("paper", (255, 255, 255), 540, 900, 700)
    cv2.rectangle(f, (0, 1380), (W, H), C((176, 134, 96)), -1); cv2.line(f, (0, 1380), (W, 1380), C(INKC), 8, cv2.LINE_AA)
    return f


def shot_S15(t, n):
    f = corridor_wall(t); t0 = st_("S15"); to = T("c5", "one") - 0.1; ts = T("c5", "Starch") - 0.1
    guard_post(f, t, "n" if t < ts else "angry", (-0.8, -0.3), photo=t >= to)
    chub(f, 130, 1480, 0.78, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.4), hand_r="point", turn=0.5)
    if t >= to: cc(f, "ONE PHOTO", 300, 1060, t, to, INKC, MILK, 40)
    if t >= ts: t3(f, "STARCH", 480, t, ts, 180)
    else: icap(f, "iodine is a", "[GUARD]", t, t0 + 0.04, acc=IOD_S, size=130, y=480)
    return finish(f, n, look="warm")


def shot_S15b(t, n):
    f = corridor_wall(t); t0 = st_("S15b"); d_ = en_("S15b") - t0
    guard_post(f, t, "happy", (-0.6, 0), door_open=1.0)
    els = (scale_el(drop_el("happy"), 1.4), scale_el(oil_drop_el("happy"), 1.2), scale_el(milk_can_el("happy"), 0.7))
    for j, el in enumerate(els):
        p = clamp((t - t0 - j * 0.28) / max(0.5, d_ - 0.5))
        x = -80 + 1050 * p; y = 1290 - abs(math.sin(p * 14)) * 22
        if p < 1: comp(f, el, x, y)
    icap(f, "anybody else", "[WALKS RIGHT IN]", t, t0 + 0.04, size=92, y=480, acc=GOOD)
    return finish(f, n, look="warm")


# ---- S16: 'Quick guess, then. A lookalike block, made with vegetable oil and no starch.' he tiptoes to the door; S16b: 'What colour does it go?' + a HELD comic pause: ticks + a freeze ----
def shot_S16(t, n):
    f = corridor_wall(t); t0 = st_("S16"); d_ = en_("S16") - t0
    guard_post(f, t, "sus", (-1, 0))
    p = clamp((t - t0) / d_); x = 130 + 170 * p; y = 1290 - abs(math.sin(p * 10)) * 18
    plate_block(f, x, y, 1.1, "smirk", (1, 0), oil=True, stache=True)
    cc(f, "VEG OIL", x, y - 150, t, T("d1", "vegetable") - 0.1, OIL_S, MILK, 34)
    if t >= T("d1", "no") - 0.1: cc(f, "NO STARCH", x, y - 205, t, T("d1", "no") - 0.1, INKC, MILK, 34)
    icap(f, "quick", "[GUESS]", t, t0 + 0.04, size=140, y=480)
    return finish(f, n, look="warm")


def shot_S16b(t, n):
    f = corridor_wall(t); t0 = st_("S16b")
    guard_post(f, t, "sus", (-1, 0), photo=False)
    plate_block(f, 340, 1290, 1.1, "wow", (1, 0), oil=True, stache=True)
    chub(f, 110, 1480, 0.76, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.1), turn=0.5, lean=3 * math.sin(t * 2))
    comp(f, chip("BLUE?", ACC_S, MILK, 80), 330, 660, scale=pin(t, t0 + 0.05)); comp(f, chip("BROWN?", IOD_S, MILK, 80), 760, 660, scale=pin(t, t0 + 0.25))
    kk = clamp((t - t0) / max(0.2, en_("S16b") - t0))
    cv2.circle(f, (540, 900), 60, C((254, 248, 230)), -1, cv2.LINE_AA); cv2.circle(f, (540, 900), 60, C(INKC), 7, cv2.LINE_AA)
    a = 2 * math.pi * kk * 2 - math.pi / 2; cv2.line(f, (540, 900), (int(540 + 46 * math.cos(a)), int(900 + 46 * math.sin(a))), C(RED_I), 6, cv2.LINE_AA)
    icap(f, "what", "[COLOUR]?", t, t0 + 0.04, size=130, y=480)
    return finish(f, n, look="cool")


# ---- S17: 'Brown. It passes.' a drop on the fake, slow motion, brown; the guard salutes; PASS; door open ----
def shot_S17(t, n):
    f = corridor_wall(t); t0 = st_("S17"); tb = T("d2", "Brown") - 0.05; tp = T("d2", "passes") - 0.1
    guard_post(f, t, "happy" if t > tb else "n", (-1, 0), door_open=1.0 if t > tp else 0.0, photo=False)
    tk = take(t, tb); chub(f, 110, 1480 + tk["dy"], 0.76, t=t, la=(112, 160), ra=(112, 160), mouth=("jaw" if t > tb else talk(t)), expr=tk["expr"], brow=tk["brow"], look=(1, 0.1), lean=tk["lean"], squash=tk["squash"], turn=0.5)
    bx = 340 + 560 * ramp(t, tp + 0.2, 0.7); by = 1290 - abs(math.sin((t - tp) * 12)) * 16 * (1 if t > tp else 0)
    plate_block(f, bx, by, 1.1, "happy", (1, 0), oil=True, stache=True)
    tx, ty, rx, ry = top_of(bx, by, 1.1)
    if t >= t0 + 0.1: stain(f, tx, ty, rx * 0.55, ry * 0.6, ramp(t, t0 + 0.1, 0.25), IOD, 3, core=IOD_S)
    if t >= tb: t3(f, "BROWN", 490, t, tb, 220, IOD_L, IOD_S)
    if t >= tp: slam(f, stamp_el("PASS", GOOD, 130), 330, 880, -8, t, tp)
    return finish(f, n, look="warm")


# ---- S18: 'The oil's invisible to the guard' — he looks straight through a ghost oil drop; S18b: 'and so is anything else that isn't starch.' a parade of question-mark ghosts ----
def shot_S18(t, n):
    f = corridor_wall(t); t0 = st_("S18")
    guard_post(f, t, "n", (-1, 0), door_open=1.0)
    x = 180 + 330 * clamp((t - t0) / max(0.3, en_("S18") - t0)); yy = 1130 + 14 * math.sin(t * 5)
    comp(f, scale_el(oil_drop_el("happy", ghost=True), 1.4), x, yy)
    cc(f, "OIL", x, yy - 170, t, t0 + 0.05, OIL_S, MILK, 36)
    icap(f, "the oil is", "[INVISIBLE]", t, t0 + 0.04, size=120, y=480, acc=OIL_S)
    return finish(f, n, look="warm")


def shot_S18b(t, n):
    f = corridor_wall(t); t0 = st_("S18b")
    guard_post(f, t, "n", (-1, 0), door_open=1.0)
    for j in range(5):
        p = ((t - t0) * 0.6 + j * 0.2) % 1; x = 60 + 760 * p; yy = 1150 + 16 * math.sin(t * 5 + j)
        comp(f, scale_el(oil_drop_el("happy", ghost=True), 0.8), x, yy, op=clamp(4 * min(p, 1 - p)))
        comp(f, ed_el("?", "", lead_col=(150, 120, 60), lead_size=54), x, yy - 12, op=clamp(4 * min(p, 1 - p)))
    icap(f, "anything that", "isn't [STARCH]", t, t0 + 0.04, size=120, y=480)
    return finish(f, n, look="warm")


# ---- S19: 'It can go wrong the other way too.' whip back; S19b: 'Real paneer that's touched a fried coating or a thick gravy can pick up starch' a happy real block in the gravy; S19c: 'and turn blue.' FAKE stamp on an innocent block ----
def shot_S19(t, n):
    f = set_diner(t); t0 = st_("S19")
    chub(f, 540, 1500, 1.1, t=t, **nolean(POSE["stop"]), mouth=talk(t), expr="sus", brow="up", look=(0, 0), hand_r="open")
    diner_front(f, TOP)
    t3(f, "THE OTHER WAY", 480, t, t0 + 0.08, 120)
    return finish(f, n, look="warm")


def shot_S19b(t, n):
    f = set_diner(t); t0 = st_("S19b"); tc = T("d4", "fried") - 0.1; tg = T("d4", "gravy") - 0.1; ts = T("d4", "starch") - 0.15
    diner_front(f, TOP - 60)
    comp(f, scale_el(bowl_el(0.7, (200, 90, 40)), 1.8), 540, 1190)
    plate_block(f, 540, 1060 + 90 * ramp(t, tg, 0.3), 1.35, "happy", (0, 0))
    cc(f, "REAL PANEER", 540, 830, t, t0 + 0.04, GOOD, MILK, 44)
    if t >= tc: cc(f, "FRIED COATING", 270, 700, t, tc, INKC, MILK, 36)
    if t >= tg: cc(f, "THICK GRAVY", 800, 700, t, tg, INKC, MILK, 36)
    if t >= ts:
        rng = np.random.default_rng(3)
        for j in range(16):
            x = 540 + rng.uniform(-150, 150); y = 1040 + rng.uniform(-60, 80); cv2.circle(f, (int(x), int(y)), 11, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 7, C(ACC_XL), -1, cv2.LINE_AA)
        icap(f, "picks up", "[STARCH]", t, ts, size=120, y=480, dark=True, acc=(255, 232, 150))
    return finish(f, n, look="warm")


def shot_S19c(t, n):
    f = set_diner(t); t0 = st_("S19c"); tb = T("d4", "blue") - 0.15
    diner_front(f, TOP - 60)
    bx, by, s_ = 540, 1140, 1.7; tx, ty, rx, ry = top_of(bx, by, s_)
    plate_block(f, bx, by, s_, "sad", (0, -0.5))
    stain(f, tx, ty, rx * 0.95, ry * 0.95, ramp(t, t0, 0.5), ACC_S, 5)
    if t >= tb: slam(f, chip("FAKE?", RED_I, MILK, 110), 540, 760, -6, t, tb)
    cc(f, "STILL REAL MILK", 540, 1400, t, tb, GOOD, MILK, 44)
    return finish(f, n, look="night")


# ---- S20: 'So it's not a fake detector.' the label on the bottle: X; S20b: 'It's a starch detector.' a new sign slams on. Screenshot moment ----
def shot_S20(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 540); t0 = st_("S20"); tn = T("d5", "fake") - 0.1
    comp(f, scale_el(bottle_el("sad"), 1.2), 540, 1130)
    t3(f, "FAKE", 520, t, tn, 180, (240, 190, 180), RED_I)
    t3(f, "DETECTOR", 690, t, tn + 0.05, 130, (240, 190, 180), RED_I)
    if t >= tn + 0.25:
        k = pin(t, tn + 0.25, 0.14); cv2.line(f, (150, 760), (int(150 + 780 * k), int(760 - 340 * k)), C(RED_I), 24, cv2.LINE_AA)
    return finish(f, n, look="warm")


def shot_S20b(t, n):
    f = ink_set("bluep", (255, 255, 255), 540, 1000, 540); t0 = st_("S20b"); ts = T("d5", "starch") - 0.1
    comp(f, scale_el(bottle_el("happy"), 1.2), 540, 1130)
    if t >= ts: t3(f, "STARCH", 520, t, ts, 200); t3(f, "DETECTOR", 690, t, ts + 0.05, 130)
    return finish(f, n, look="fresh")


# ---- S21: 'What about the other tricks, like if it's rubbery, it's fake?' he bends a block: boing; S22: 'Paneer from buffalo milk is naturally firm and rubbery.' a buffalo, a proud block bouncing ----
def shot_S21(t, n):
    f = set_worktop(t); t0 = st_("S21"); tr = T("e1", "rubbery") - 0.15
    bend = 0.18 * math.sin((t - tr) * 9) if t > tr else 0
    hs = chub(f, 540, 1500, 1.15, t=t, la=(96, 118), ra=(96, 118), mouth=talk(t), expr="sus", brow="sus", look=(0, 0.3), hand_r="grip", hand_l="grip", lean=2 * math.sin(t * 2))
    el = scale_xy(scale_el(paneer_el("wow"), 0.9), 1 + bend, 1 - bend)
    comp(f, el, 540, 1262)
    worktop_front(f, TOP + 100)
    if t >= tr: t3(f, "RUBBERY?", 490, t, tr, 170)
    else: icap(f, "the other", "[TRICKS]", t, t0 + 0.04, size=130, y=490)
    return finish(f, n, look="fresh")


def shot_S22(t, n):
    f = set_dusk(t); f = inkify(f, 0.15); t0 = st_("S22"); tr = T("e2", "rubbery") - 0.15
    comp(f, scale_el(buffalo_el(), 1.2), 320, 1120, scale=pin(t, t0))
    b_ = abs(math.sin((t - t0) * 6)); plate_block(f, 760, 1360 - 90 * b_, 1.4, "happy", (-0.6, 0))
    cc(f, "BUFFALO MILK", 320, 860, t, t0 + 0.05, INKC, MILK, 40)
    if t >= tr: cc(f, "REAL + RUBBERY", 720, 1140, t, tr, GOOD, MILK, 44)
    icap(f, "naturally", "[FIRM]", t, t0 + 0.05, size=130, y=470, dark=True, acc=(255, 232, 150))
    src(f, SRC_J, t, t0 + 0.3, 1490)
    return finish(f, n, look="golden")


# ---- S24: 'There's no home test that can settle it.' a house + a big X; S24b: 'Telling one fat from another takes a lab.' Chubby in a lab coat at a microscope, two fat drops ----
def shot_S24(t, n):
    f = set_droom(t); t0 = st_("S24"); tn = T("e4", "no") - 0.1
    chub(f, 220, 1500, 1.0, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="sad", brow="sad", look=(1, 0), turn=0.5)
    table_front(f, TOP)
    for j, (el, x) in enumerate(((scale_el(bottle_el(), 0.45), 520), (scale_el(glass2_el((226, 214, 170), 0.7), 0.66), 670), (scale_el(paneer_el(), 0.7), 840))):
        comp(f, el, x, 1250, scale=pin(t, t0 + j * 0.07))
    if t >= tn: t3(f, "NO HOME TEST", 660, t, tn, 130, ACC_L, ACC_S)
    if t >= tn + 0.4: comp(f, chip("CAN SETTLE IT", INKC, MILK, 46), 540, 800, scale=pin(t, tn + 0.4))
    src(f, SRC_B, t, tn + 0.4, 1490)
    return finish(f, n, look="warm")


def shot_S24b(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 1000, 540); t0 = st_("S24b"); tl = T("e4", "lab") - 0.15
    chub(f, 250, 1500, 1.0, t=t, la=(24, 14), ra=(90, 60), mouth=talk(t), expr="sus", brow="up", look=(1, 0.3), shirt=(246, 248, 248), hand_r="grip", turn=0.5)
    comp(f, scale_el(microscope_el(), 1.0), 660, 1260)
    comp(f, scale_el(flask_el(), 0.8), 930, 1360)
    comp(f, scale_el(milkfat_el(), 1.6), 620, 800, scale=pin(t, t0 + 0.05)); comp(f, scale_el(oil_drop_el(None), 0.76), 840, 800, scale=pin(t, t0 + 0.2))
    cc(f, "MILK FAT", 620, 660, t, t0 + 0.05, IOD_S, MILK, 32); cc(f, "VEG OIL", 840, 660, t, t0 + 0.2, OIL_S, MILK, 32)
    if t >= tl: icap(f, "that takes a", "[LAB]", t, tl, size=140, y=420)
    src(f, SRC_C, t, t0 + 0.4, 1490)
    return finish(f, n, look="fresh")


# ---- S25: 'So what can you do before Diwali dinner? Three easy things.' Diwali table, three cards ----
def shot_S25(t, n):
    f = set_droom(t); t0 = st_("S25"); tt = T("f1", "Three") - 0.12
    chub(f, 540, 1500, 1.12, t=t, **nolean(POSE["tada"]) if t > tt else nolean(POSE["think"]), mouth=talk(t), expr="happy", brow="up", look=(0, 0))
    table_front(f, TOP)
    if t >= tt:
        for j, lab in enumerate(("LABEL", "ASK", "PRICE")):
            comp(f, chip(f"{j + 1}  {lab}", ACC_S, MILK, 50), 205 + j * 320, 640, scale=pin(t, tt + j * 0.12))
    icap(f, "before Diwali", "[DINNER]", t, t0 + 0.04, size=130, y=430)
    return finish(f, n, look="warm")


# ---- S26: 'On a packet, read the label.' zoom on small print with a magnifier; S26b: 'If it says analogue, it isn't milk paneer.' ----
def shot_S26(t, n):
    f = set_worktop(t); t0 = st_("S26")
    hs = chub(f, 200, 1500, 1.0, t=t, la=(24, 14), ra=(96, 80), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.1), turn=0.5, hand_r="grip")
    comp(f, chip("1", ACC_S, MILK, 70), 200, 720, scale=pin(t, t0))
    worktop_front(f, TOP)
    comp(f, scale_el(packet_el(), 1.3), 710, 1030)
    for j, x1 in enumerate((870, 840, 860)): cv2.line(f, (560, 1040 + j * 40), (x1, 1040 + j * 40), C((130, 124, 116)), 8, cv2.LINE_AA)
    cc(f, "PANEER-LIKE", 710, 880, t, t0, INKC, MILK, 36)
    icap(f, "read the", "[LABEL]", t, t0 + 0.04, size=130, y=430)
    return finish(f, n, look="fresh")


def shot_S26b(t, n):
    f = set_worktop(t); t0 = st_("S26b"); ta = T("f2", "analogue") - 0.15
    f = f * 0.5 + 0.5 * np.array(C((238, 240, 252)), np.float32)
    comp(f, scale_el(packet_el(), 2.1), 540, 1080)
    if t >= ta:
        comp(f, chip("ANALOGUE", ACC_S, MILK, 110), 540, 1010, scale=pin(t, ta))
        cc(f, "NOT MILK PANEER", 540, 1200, t, ta + 0.3, RED_I, MILK, 56)
    src(f, SRC_B, t, ta + 0.3, 1490)
    return finish(f, n, look="fresh")


# ---- S27: 'Eating out, just ask. Dairy or analogue?' Chubby + the waiter; S27b: 'Maharashtra already makes restaurants say so on the menu.' the menu fills the frame ----
def shot_S27(t, n):
    f = set_diner(t); t0 = st_("S27"); td = T("f3", "Dairy") - 0.15
    chub(f, 250, 1500, 1.0, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="smirk", brow="up", look=(1, -0.2), hand_r="point", turn=0.5)
    waiter(f, 800, 1500, 1.0, t=t, la=(24, 14), ra=(100, 70), mouth=0, expr="wow" if t > td + 0.5 else "n", brow="up", look=(-1, 0), turn=-0.5)
    diner_front(f, TOP + 40)
    comp(f, chip("2", ACC_S, MILK, 70), 250, 780, scale=pin(t, t0))
    if t >= td: comp(f, chip("DAIRY OR ANALOGUE?", WHITE, INKC, 56), 540, 620, scale=pin(t, td))
    else: icap(f, "just", "[ASK]", t, t0 + 0.04, size=150, y=430, dark=True, acc=(255, 232, 150))
    src(f, SRC_B, t, td + 0.2, 1490)
    return finish(f, n, look="warm")


def shot_S27b(t, n):
    f = set_diner(t, dim=0.25); t0 = st_("S27b"); tm = T("f3", "menu") - 0.3
    comp(f, scale_el(menu_el(), 1.25), 540, 1010)
    comp(f, chip("MENU", (180, 90, 60), MILK, 48), 540, 660, scale=pin(t, t0 + 0.05))
    cv2.line(f, (250, 780), (830, 780), C((170, 160, 140)), 8, cv2.LINE_AA); cv2.line(f, (250, 1240), (780, 1240), C((170, 160, 140)), 8, cv2.LINE_AA); cv2.line(f, (250, 1320), (820, 1320), C((170, 160, 140)), 8, cv2.LINE_AA)
    comp(f, ed_el("Paneer tikka", "", lead_col=INKC, lead_size=64), 540, 900, scale=pin(t, t0 + 0.1))
    if t >= tm: comp(f, chip("(ANALOGUE)", ACC_S, MILK, 70), 540, 1050, scale=pin(t, tm))
    icap(f, "in", "[MAHARASHTRA]", t, t0 + 0.04, size=100, y=430, dark=True, acc=(255, 232, 150))
    src(f, SRC_TT, t, t0 + 0.4, 1490)
    return finish(f, n, look="warm")


# ---- S28: 'And if the price looks too good, ask why.' a shop tag dropping; Chubby one eyebrow ----
def shot_S28(t, n):
    f = set_shop(t); t0 = st_("S28"); tw = T("f4", "why") - 0.15
    chub(f, 280, 1500, 1.1, t=t, **nolean(POSE["cheek"]), mouth=talk(t), expr="sus", brow="sus", look=(1, 0.1), turn=0.5)
    comp(f, chip("3", ACC_S, MILK, 70), 150, 800, scale=pin(t, t0))
    shop_front(f, 1250)
    plate_block(f, 700, 1150, 1.2, "smirk", (-0.8, 0), stache=True)
    comp(f, scale_el(tag_el2(), 1.0), 700, 880, scale=pin(t, t0 + 0.05))
    comp(f, chip("SO CHEAP!", RED_I, MILK, 44), 712, 880, scale=pin(t, t0 + 0.1))
    if t >= tw: t3(f, "WHY?", 500, t, tw, 240)
    else: icap(f, "too", "[GOOD]?", t, t0 + 0.04, size=150, y=480)
    return finish(f, n, look="warm")


# ---- S29: 'Still want to try the drop?' he holds it up; S29b: 'Boil a little in water, cool it, and add a few drops.' 3 panels; S29c: 'Just don't eat that piece. Iodine isn't food.' he goes to bite, STOP ----
def shot_S29(t, n):
    f = set_worktop(t); t0 = st_("S29")
    hs = chub(f, 540, 1500, 1.2, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="smirk", brow="up", look=(0.4, -0.4), hand_r="grip", lean=4)
    hx, hy = hs[1]; dropper_at(f, hx + 10, hy + 240, 0.7)
    worktop_front(f, TOP + 80)
    icap(f, "still want to try", "the [DROP]?", t, t0 + 0.04, size=120, y=430, acc=IOD_S)
    return finish(f, n, look="fresh")


def shot_S29b(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 540); t0 = st_("S29b"); ts = [T("f5", "Boil") - 0.1, T("f5", "cool") - 0.1, T("f5", "add") - 0.1]
    ys = (690, 990, 1290)
    for j, (yy, tt_, lab) in enumerate(zip(ys, ts, ("BOIL A LITTLE", "COOL IT", "ADD A FEW DROPS"))):
        if t < tt_: continue
        k = pin(t, tt_); cv2.rectangle(f, (80, yy - 130), (950, yy + 130), C((254, 250, 240)), -1, cv2.LINE_AA); cv2.rectangle(f, (80, yy - 130), (950, yy + 130), C(INKC), 6, cv2.LINE_AA)
        comp(f, chip(str(j + 1), ACC_S, MILK, 60), 150, yy - 70, scale=k)
        if j == 0: comp(f, scale_el(pot_el("water", 0.6), 0.42), 300, yy); side_flames(f, 300, yy + 96, t, 130, 0.5, 3, 40)
        if j == 1: comp(f, scale_el(glass2_el((226, 214, 170), 0.7), 0.7), 300, yy)
        if j == 2: dropper_at(f, 300, yy + 10, 0.42); comp(f, scale_el(paneer_el(), 0.5), 300, yy + 70)
        comp(f, chip(lab, INKC, MILK, 50), 640, yy, scale=k)
    if t >= ts[0]: comp(f, chip("BLUE = STARCH. THAT'S ALL.", ACC_S, MILK, 40), 540, 1460, op=clamp((t - ts[2]) / 0.3))
    icap(f, "the", "[TEST]", t, t0 + 0.02, size=110, y=420, acc=IOD_S)
    src(f, SRC_T, t, ts[0] + 0.2, 1490) if False else None
    return finish(f, n, look="fresh")


def shot_S29c(t, n):
    f = set_worktop(t); t0 = st_("S29c"); tf = T("f5", "food") - 0.25
    bk = t < t0 + 0.55
    hs = chub(f, 300, 1500, 1.1, t=t, la=(24, 14), ra=(148, -130) if bk else (70, 30), mouth="jaw" if bk else talk(t), expr="happy" if bk else "wow", brow="up", look=(0.2, 0.2), hold=(scale_el(paneer_el(blue=1.0), 0.4) if bk else None), hold_off=(26, -30), hold_front=True, lean=4 if bk else -8)
    worktop_front(f, TOP)
    if not bk:
        comp(f, scale_el(bin_ink_el(0.8), 1.0), 760, 1290); comp(f, scale_el(paneer_el(blue=1.0), 0.5), 760, 1170 + 40 * ramp(t, t0 + 0.6, 0.3))
    slam(f, stamp_el("DON'T EAT IT", RED_I, 84), 540, 640, -5, t, T("f5", "dont") - 0.1)
    if t >= tf: comp(f, chip("IODINE ISN'T FOOD", INKC, MILK, 54), 540, 780, scale=pin(t, tf))
    src(f, "Source: WebExhibits, Causes of Color", t, tf, 1490)
    return finish(f, n, look="fresh")


# ---- S30: 'In September, the regulator proposed taking the word paneer off these lookalikes.' the word peels off a pack; S30b: 'It's still only a draft.' a pencil-grey DRAFT stamp ----
def shot_S30(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 1000, 500); t0 = st_("S30"); tw = T("f6", "word") - 0.1
    comp(f, scale_el(packet_el(), 1.6), 540, 1040)
    plate_block(f, 540, 1280, 0.9, "sad", (0, -0.5), stache=True, oil=True)
    k = ramp(t, tw, 0.8)
    comp(f, chip("PANEER", RED_I if k > 0 else ACC_S, MILK, 84), 540 + 300 * k, 930 - 330 * k, op=1 - 0.7 * k * k)
    cc(f, "SEPT 2026", 200, 640, t, t0 + 0.05, INKC, MILK, 36)
    cc(f, "FSSAI DRAFT", 540, 640, t, T("f6", "regulator") - 0.1, ACC_S, MILK, 36) if False else None
    icap(f, "the regulator", "[PROPOSED]", t, t0 + 0.04, size=110, y=430)
    src(f, "Source: Business Today, 24 Sep 2026", t, t0 + 0.4, 1490)
    return finish(f, n, look="fresh")


def shot_S30b(t, n):
    f = ink_set("coldp", (255, 255, 255), 540, 1000, 500); t0 = st_("S30b"); td = T("f6", "draft") - 0.2
    scroll(f, 540, 620, 560, 740, 1.0, t)
    for j, x1 in enumerate((760, 720, 780, 690)): cv2.line(f, (340, 800 + j * 80), (x1, 800 + j * 80), C((170, 160, 140)), 8, cv2.LINE_AA)
    if t >= td: slam(f, stamp_el("ONLY A DRAFT", (110, 112, 120), 90), 540, 1020, -8, t, td)
    return finish(f, n, look="fresh")


# ---- S31: recap card: 'So remember. Blue means starch. And no blue doesn't mean real.' a clean card to screenshot ----
def shot_S31(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 560); t0 = st_("S31"); tb = T("g1", "Blue") - 0.12; tn = T("g1", "no") - 0.12
    cv2.rectangle(f, (70, 480), (950, 1440), C((254, 250, 240)), -1, cv2.LINE_AA); cv2.rectangle(f, (70, 480), (950, 1440), C(INKC), 7, cv2.LINE_AA)
    cv2.line(f, (110, 960), (910, 960), C(INKC), 4, cv2.LINE_AA)
    if t >= tb:
        plate_block(f, 250, 760, 1.05, None, blue=1.0, scale=pin(t, tb))
        t3(f, "BLUE =", 650, t, tb, 96, x=650); t3(f, "STARCH", 790, t, tb + 0.1, 100, x=650)
    if t >= tn:
        plate_block(f, 250, 1200, 1.05, None, scale=pin(t, tn)); tx, ty, rx, ry = top_of(250, 1200, 1.05); stain(f, tx, ty, rx * 0.55, ry * 0.6, 1.0, IOD, 3, core=IOD_S)
        t3(f, "NO BLUE", 1090, t, tn, 88, IOD_L, IOD_S, x=650); comp(f, chip("DOESN'T MEAN REAL", INKC, MILK, 40), 650, 1240, scale=pin(t, tn + 0.3))
    ui_word(f, "remember", "[THIS]", 370, t, t0 + 0.02, col=INKC, acc=ACC_S, size=100)
    src(f, "No home test settles it. Read the label, and ask.", t, tn + 0.3, 1480)
    return finish(f, n, look="warm")


# ---- S32: 'Now send this to the friend who sent you that video.' reply on a phone; then logo ----
def shot_S32(t, n):
    t0 = st_("S32"); f = set_droom(t); vend = LINES["g2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("g2", "send") + 0.25
        comp(f, scale_el(phone2_el("this video you sent me...", "blue = starch. that's all", pr), 0.82), 760, 960, scale=pin(t, t0))
        if pr and t < T("g2", "send") + 0.7:
            rr = (t - T("g2", "send") - 0.25) / 0.45; cv2.circle(f, (760, 1230), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 300, 1500, 1.05, t=t, la=(20, 12), ra=(70, 40), mouth=talk(t), expr="smirk", brow="up", hand_r="point", look=(1, -0.1), turn=0.5)
        ui_word(f, "send this to whoever sent you", "THAT [VIDEO]", 440, t, T("g2", "send") - 0.05, col=INKC, acc=ACC_S, size=100)
    else:
        k = pin(t, vend + 0.2, 0.4); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 1030, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1500, 0.7, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up")
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TP, 0.45, 18), (T("i2", "blue") - 0.3, 0.3, 10), (T("i2", "fake") - 0.15, 0.4, 16), (T("i3", "real") - 0.15, 0.25, 8), (T("a1", "sour") - 0.2, 0.2, 6), (T("a3", "press") + 0.04, 0.4, 16), (T("a3", "block") - 0.2, 0.25, 8), (T("a4", "No") + 0.05, 0.35, 14), (T("b2", "analogue") - 0.15, 0.3, 10), (T("b2", "half") - 0.2, 0.25, 8), (T("b3", "legal") - 0.15, 0.35, 12), (T("b4", "plate") + 0.0, 0.3, 12), (T("b4", "label") - 0.15, 0.35, 12),
           (T("c1", "blue") - 0.15, 0.3, 10), (T("c3", "blue") - 0.15, 0.3, 10), (T("c4", "brown") - 0.2, 0.25, 8), (T("c5", "Starch") - 0.1, 0.3, 12), (T("d2", "Brown") - 0.05, 0.35, 14), (T("d2", "passes") - 0.1, 0.4, 16), (T("d4", "blue") - 0.15, 0.35, 14), (T("d5", "fake") + 0.15, 0.3, 12), (T("d5", "starch") - 0.1, 0.4, 16),
           (T("e1", "rubbery") - 0.15, 0.25, 8), (T("e4", "no") - 0.1, 0.3, 12), (T("e4", "lab") - 0.15, 0.25, 8), (T("f1", "Three") - 0.12, 0.25, 8), (T("f2", "analogue") - 0.15, 0.3, 12), (T("f3", "Dairy") - 0.15, 0.25, 8), (T("f4", "why") - 0.15, 0.3, 12), (T("f5", "dont") - 0.1, 0.35, 14), (T("f6", "draft") - 0.2, 0.3, 12), (T("g2", "send") + 0.25, 0.2, 8)]


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
