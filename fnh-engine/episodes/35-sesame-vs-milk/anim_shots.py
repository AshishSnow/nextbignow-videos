# ================= shots: FreshNestHub 35 — "Does sesame have more calcium than milk?" (Chubby INK; 35-50 s rule; ONE takeaway) ===
# COLOUR SCRIPT: SESAME GOLD (ACC) = sesame / calcium ON PAPER only (the seed, the tall bar, the skin band, the third of the glass). Milk = cream + blue gloves.
# Oxalate = cold steel grey (the handcuffs). Story = THE BOXING RING (new place, spotlit arena) + the morning worktop; every explanation = the white BOARD.
# METAPHOR: a boxing match. On paper sesame wins by a knockout (8x per 100 g); oxalate HANDCUFFS its gloves (calcium locked in the skin), so your gut
# only pulls out a little; and you eat a spoon, not 100 g. Takeaway: til is a bonus, not a swap for your milk.
# Craft skill: SECONDARY ACTION — one small supporting behaviour per shot (the boxers' bounce + glove taps, Chubby's free hand gesturing on the mic, the ropes
# wobbling after a hit, the cuffed seed struggling), always subordinate to the main action and dropped in the fast beats.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "calcium") - 0.1, "punch"),
    ("S1", T("i2", "Per") - 0.12, "erase"),
    ("S2", T("i2", "On") - 0.1, "whip"),
    ("S3", T("a1", "But") - 0.12, "erase"), ("S3b", T("a1", "and") - 0.1, "cut"),
    ("S4", T("a2", "Oxalate") - 0.1, "whip"), ("S4b", T("a2", "so") - 0.1, "erase"),
    ("S5", T("b1", "And") - 0.1, "whip"), ("S5b", T("b1", "You") - 0.1, "punch"),
    ("S6", T("b2", "That") - 0.1, "erase"),
    ("S7", T("c1", "So") - 0.1, "whip"), ("S7b", T("c1", "It") - 0.1, "erase"),
    ("S8", T("c2", "Send") - 0.1, "whip"),
    ("S9", LINES["c2"]["end"] + 0.12, "punch"), ("S10", LINES["c2"]["end"] + 0.85, "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """phone-size hand lettering (ep 27: the kit default reads too small)."""
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def el_at(f, el, x, y, s=1.0, t=None, t0=None, rot=0.0, op=1.0):
    k = 1.0 if t0 is None else (snap(t, t0, 4) if t >= t0 else 0.0)
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, rot, k, op, 0.0)


def stamp_x(f, x, y, r, k, col=(176, 40, 44), w=22):
    if k <= 0: return
    for sg in (-1, 1): cv2.line(f, (int(x - r * k), int(y - sg * r * k)), (int(x + r * k), int(y + sg * r * k)), C(col), w, cv2.LINE_AA)


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


# ---- the ring cast ----
SX, MX, FY, BS = 470, 840, 1590, 1.2        # seed boxer x, milk boxer x, feet y, boxer scale
AX, AY, AS = 170, 1930, 1.42                 # Chubby the ringside commentator (FOREGROUND left, outside the ropes)
KO_T = T("i2", "knockout") - 0.12
CUFF_T = T("a2", "handcuffs") - 0.1
HITS = [KO_T + 0.06, CUFF_T]


def announcer(f, t, expr="happy", brow="up", look=(0.8, -0.1), mouth=None, lean=0.0, dy=0.0, squash=0.0, gesture=True):
    """Chubby as the ringside commentator (foreground, the ring behind him): mic in the right hand, bow tie; SECONDARY ACTION: the free left hand gestures
    in little beats while he talks."""
    g = sec_tap(t, 1.6, 0.3) if gesture else 0.0
    la = (40 + 50 * g, 30 + 60 * g)
    chub(f, AX, AY + dy, AS, t=t, la=la, ra=(150, -128), hold=scale_el(mic_el(), 0.62), hold_off=(-4, -30), hold_front=True, hand_r="grip",
         mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow, look=look, lean=lean, squash=squash, turn=0.45)
    bowtie(f, AX, AY + dy, AS, t, lean)


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0)."""
    kw(f, "DO YOU KNOW", 540, 320, t, t0, "pop", 70, col=MILK, op=op)
    kw(f, "SESAME", 280, 455, t, t0, "shake", 104, col=ACC, amp=0.35, op=op)
    kw(f, "vs", 565, 462, t, t0, "pop", 70, col=MILK, op=op)
    kw(f, "MILK", 800, 455, t, t0, "shake", 118, col=(150, 190, 240), amp=0.35, op=op)
    kw(f, "MORE CALCIUM?", 540, 600, t, t0, "pop", 92, col=MILK, op=op)


def ring_scene(f, t, seed_kw=None, milk_kw=None, ann=None, hits=HITS):
    boxer_kw = dict(kind="seed", mood="angry", look=(1, 0)); boxer_kw.update(seed_kw or {})
    milk_k = dict(kind="milk", mood="n", look=(-1, 0), ph=0.45); milk_k.update(milk_kw or {})
    a = dict(); a.update(ann or {})
    show = a.pop("show", True)
    boxer(f, milk_k.pop("x", MX), FY, BS, t, **milk_k)
    boxer(f, boxer_kw.pop("x", SX), FY, BS, t, **boxer_kw)
    ring_front(f, t, hits)
    if show: announcer(f, t, **a)


# ---- S0: HOOK at frame 0: the ring, both boxers already bouncing, Chubby announcing into the mic; the question on screen ----
def shot_S0(t, n):
    f = set_ring(t)
    ring_scene(f, t, ann=dict(expr="happy", brow="up"))
    hook_words(f, t)
    return finish(f, n, look="night")


# ---- S0b: '...calcium than milk?' FACE-OFF close-up: the seed and the glass nose to nose, gloves up ----
def shot_S0b(t, n):
    f = set_ring(t, blur=10); t0 = st_("S0b")
    f = dof(f, 3)
    boxer(f, 750, 1720, 1.55, t, kind="milk", mood="angry", look=(-1, 0), ph=0.45)
    boxer(f, 330, 1720, 1.55, t, kind="seed", mood="angry", look=(1, 0))
    for k_ in range(3):                                                              # sparks of rivalry between them
        u = (t * 2.2 + k_ / 3) % 1
        glow(f, 540, 1050 - 60 * u, 30, (255, 220, 150), 0.5 * (1 - u))
    hook_words(f, t)
    return finish(f, n, look="night")


# ---- S1: 'Per hundred grams, whole sesame seeds have over... eight times more.' BOARD: 100 g of each, the bars grow, 975 vs 113 mg, OVER 8x ----
BASE_Y = 1040; PXMG = 0.42


def shot_S1(t, n):
    f = board_bg(); t0 = st_("S1"); th = T("i2", "hundred") - 0.1; ts = T("i2", "sesame") - 0.1; te = T("i2", "eight") - 0.1
    draw_on(f, [(120, BASE_Y), (960, BASE_Y)], ramp(t, t0, 0.3), BP_INK, 6, seed=3, tip=False)
    el_at(f, til_bowl_el(label=None), 310, BASE_Y + 130, 0.8, t, t0 + 0.05)
    el_at(f, milkglass_el(None), 770, BASE_Y + 130, 0.75, t, t0 + 0.15)
    write_on(f, "100 g", 310, BASE_Y + 290, t, th, 50, BP_INK)
    write_on(f, "100 g", 770, BASE_Y + 290, t, th + 0.15, 50, BP_INK)
    km = ramp(t, th + 0.3, 0.6); hm = 113 * PXMG * km                                # milk bar
    if km > 0:
        P = [(690, BASE_Y), (690, BASE_Y - hm), (850, BASE_Y - hm), (850, BASE_Y)]
        cv2.fillPoly(f, [np.array(P, np.int32)], C((226, 236, 250)), cv2.LINE_AA); draw_on(f, P, 1.0, BP_INK, 6, seed=5, tip=False)
        write_on(f, f"{int(count_up(t, th + 0.3, 113, 0.6))} mg", 770, BASE_Y - hm - 50, t, th + 0.3, 46, BP_INK, 99)
    ks = ramp(t, ts, te - ts + 0.2); hs = 975 * PXMG * ks                            # sesame bar grows on 'sesame' up to 'eight'
    if ks > 0:
        P = [(230, BASE_Y), (230, BASE_Y - hs), (390, BASE_Y - hs), (390, BASE_Y)]
        cv2.fillPoly(f, [np.array(P, np.int32)], C(ACC_XL), cv2.LINE_AA)
        hatch_on(f, P, 1.0, ACC, gap=18)
        draw_on(f, P, 1.0, BP_INK, 6, seed=6, tip=False)
        write_on(f, f"{int(count_up(t, ts, 975, te - ts + 0.2))} mg", 310, BASE_Y - hs - 50, t, ts, 46, ACC_S, 99)
    if t > te:
        kw(f, "OVER 8x", 610, 470, t, te, "shake", 120, col=ACC, amp=0.4)
        draw_arrow_on(f, (700, 520), (420, 560), ramp(t, te + 0.15, 0.25), ACC_S, 6, 24, bend=-0.25)
    src(f, SRC_US, t, t0 + 0.4)
    return finish(f, n, look="fresh")


# ---- S2: 'On paper, that's a knockout.' the ring: an ON PAPER slip, the seed's punch, the glass flies into the ropes, K.O.! ----
def shot_S2(t, n):
    f = set_ring(t); t0 = st_("S2"); tp = T("i2", "paper") - 0.15
    punch = snap(t, KO_T - 0.08, 3) if t > KO_T - 0.08 else 0.0
    ko = ramp(t, KO_T, 0.3)
    k = take(t, KO_T)
    ring_scene(f, t, seed_kw=dict(punch=min(1.0, punch), mood="angry", bounce=t < KO_T - 0.3),
               milk_kw=dict(ko=ko, mood="wow" if t < KO_T else "ouch", x=MX + 80 * ko, slosh=-ko),
               ann=dict(expr=k["expr"] if t > KO_T else "sus", brow=k["brow"] if t > KO_T else "sus", look=k["look"] if t > KO_T else (0.6, 0.3),
                        mouth="jaw" if t > KO_T else None, dy=k["dy"], squash=k["squash"], gesture=False))
    if t > KO_T:                                                                     # impact star
        q = ramp(t, KO_T, 0.25)
        for j in range(8):
            a = 2 * math.pi * j / 8; r0 = 40 + 110 * q
            cv2.line(f, (int(790 + r0 * math.cos(a)), int(1160 + r0 * math.sin(a))), (int(790 + (r0 + 40) * math.cos(a)), int(1160 + (r0 + 40) * math.sin(a))),
                     C(ACC_L), 8, cv2.LINE_AA)
    if t > tp:
        q = snap(t, tp, 3)
        rot_comp(f, scale_el(vstamp_el("ON PAPER", ACC_S, 70), 1.0), 540, 360, -5, 1.4 - 0.4 * q, 1.0, 0.3)
    if t > KO_T: kw(f, "K.O.!", 540, 560, t, KO_T, "shake", 170, col=ACC, amp=0.8)
    return finish(f, n, look="night")


# ---- the BOARD seed: a big cut-away sesame seed; the thin SKIN band (the hull) holds most of the calcium pebbles ----
SEED_C = (540, 930); SEED_R = (300, 400)
OUT_P = _seed_pts(SEED_C[0], SEED_C[1], SEED_R[0], SEED_R[1], 40)
IN_P = _seed_pts(SEED_C[0], SEED_C[1] + 12, SEED_R[0] - 48, SEED_R[1] - 60, 40)
CA_SKIN = [OUT_P[i] for i in (2, 6, 10, 14, 19, 23, 27, 31, 35, 38)]
CA_SKIN = [((x + SEED_C[0] * 0.12) / 1.12, (y + (SEED_C[1] + 12) * 0.12) / 1.12) for x, y in CA_SKIN]   # nudge into the band
CA_CORE = [(470, 1040), (610, 900)]
CUFFED = (0, 1, 3, 4, 6, 7, 9)


def board_seed(f, t, t0, kd=None, ca_t=None, skin_t=None, cuff_t=None):
    k = ramp(t, t0, 0.55) if kd is None else kd
    if skin_t is not None and t > skin_t:
        cv2.fillPoly(f, [np.array(OUT_P, np.int32)], C(ACC_XL), cv2.LINE_AA)
        hatch_on(f, OUT_P, ramp(t, skin_t, 0.4), ACC, gap=18)
        cv2.fillPoly(f, [np.array(IN_P, np.int32)], C((253, 250, 240)), cv2.LINE_AA)
    draw_on(f, OUT_P, k, BP_INK, 8, seed=31, tip=k < 1, closed=True)
    if k > 0.5: draw_on(f, IN_P, clamp((k - 0.5) / 0.5), BP_INK, 4, seed=32, tip=False, closed=True)
    if ca_t is not None and t > ca_t:
        for i, (x, y) in enumerate(CA_SKIN + CA_CORE):
            ti = ca_t + 0.05 * i
            if t > ti:
                cuff = cuff_t is not None and i in CUFFED and t > cuff_t + 0.07 * CUFFED.index(i)
                el_at(f, ca_el(cuffed=cuff), x, y, 0.9 if i < len(CA_SKIN) else 0.7, t, ti)


# ---- S3: 'But most of that calcium sits in the seed's thin skin,' BOARD: the seed draws on, Ca pebbles appear, the skin band lights up gold ----
def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3"); tc = T("a1", "calcium") - 0.1; tk = T("a1", "skin") - 0.3
    board_seed(f, t, t0, ca_t=tc, skin_t=tk)
    write_on(f, "a sesame seed, cut open", 540, 330, t, t0 + 0.1, 46, BP_INK, 40)
    if t > tk:
        write_on(f, "thin skin (hull)", 830, 1400, t, tk, 46, ACC_S, 40)
        draw_arrow_on(f, (800, 1350), (760, 1190), ramp(t, tk + 0.1, 0.3), ACC_S, 6, 24)
    peek(f, t, 170, 1400, 0.5, expr="sus", look=(0.6, -0.4))
    return finish(f, n, look="fresh")


# ---- S3b: '...and a lot of it is stuck to something called oxalate.' BOARD: steel cuffs snap round most skin pebbles; 'oxalate' labels them ----
def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); ts = T("a1", "stuck") - 0.1; to = T("a1", "oxalate", 0) - 0.15
    board_seed(f, t, t0, kd=1.0, ca_t=-9, skin_t=-9, cuff_t=ts)
    write_on(f, "thin skin (hull)", 830, 1400, 99, 0, 46, ACC_S, 40)
    if t > to:
        write_on(f, "oxalate", 540, 330, t, to, 66, (90, 100, 116), 30)
        x0, y0 = CA_SKIN[1]; draw_arrow_on(f, (560, 380), (x0 + 30, y0 - 50), ramp(t, to + 0.2, 0.3), (90, 100, 116), 6, 24, bend=0.2)
    peek(f, t, 170, 1400, 0.5, expr="sad" if t > ts else "sus", look=(0.6, -0.4))
    return finish(f, n, look="fresh")


# ---- S4: 'Oxalate locks onto calcium like handcuffs,' the ring: cuffs fly in and snap round the seed's gloves; it struggles (secondary action) ----
def shot_S4(t, n):
    f = set_ring(t); t0 = st_("S4"); tl = T("a2", "locks") - 0.15
    cuff = ramp(t, CUFF_T - 0.12, 0.12) if t > CUFF_T - 0.12 else 0.0
    ring_scene(f, t, seed_kw=dict(x=SX, cuff=cuff, struggle=1.0 if t > CUFF_T + 0.2 else 0.0, mood="angry" if cuff < 0.5 else "ouch",
                                  look=(1, 0) if cuff < 0.5 else (0, 1), bounce=cuff < 0.5),
               milk_kw=dict(mood="sus", look=(-1, 0.3)),
               ann=dict(expr="sus" if t < CUFF_T else "wow", brow="sus" if t < CUFF_T else "up", look=(-0.7, 0.3), gesture=t < tl))
    if tl < t < CUFF_T:                                                              # the cuffs fly in from the top on an arc
        u = eio(clamp((t - tl) / max(0.1, CUFF_T - tl)))
        x = 900 + (SX + 100 - 900) * u; y = 300 + (1250 - 300) * u - 260 * math.sin(math.pi * u)
        rot_comp(f, scale_el(cuff_el(), 0.7), x, y, 360 * u, 1.0, 1.0, 0.0)
    if t > CUFF_T:
        kw(f, "HANDCUFFED!", 540, 420, t, CUFF_T, "shake", 120, col=(214, 220, 230), amp=0.5)
    else:
        write_on(f, "oxalate", 540, 380, t, tl, 60, MILK, 30)
    return finish(f, n, look="night")


# ---- S4b: '...so your gut can only pull out a small part of it.' BOARD: a gut tube; Ca pebbles ride through; only the free ones get pulled out ----
def shot_S4b(t, n):
    f = board_bg(); t0 = st_("S4b"); tg = T("a2", "gut") - 0.15; tp = T("a2", "pull") - 0.15; tsm = T("a2", "small") - 0.15
    k = ramp(t, t0, 0.4)
    top = [(80, 760), (300, 720), (540, 770), (780, 720), (1000, 760)]; bot = [(x, y + 230) for x, y in top]
    draw_on(f, top, k, BP_INK, 8, seed=41, tip=False); draw_on(f, bot, k, BP_INK, 8, seed=42, tip=False)
    write_on(f, "your gut", 540, 620, t, tg, 56, BP_INK)
    ride = (t - t0) * 120
    for i in range(8):                                                               # pebbles ride left -> right through the tube
        free = i in (2, 5)
        x = 60 + (i * 130 + ride) % 1000; y = 870 + 14 * math.sin(x / 90 + i)
        if free and t > tp:
            q = ramp(t, tp + 0.1 * (i == 5), 0.6)
            x = 60 + (i * 130 + (tp - t0) * 120) % 1000; y = y + 420 * q
            if q > 0.05: draw_arrow_on(f, (x, 1010), (x, 1010 + 330 * q), 1.0, INK_MINT_S, 6, 22)
        el_at(f, ca_el(cuffed=not free, free=free and t > tp), x, y, 0.85)
    if t > tp:
        draw_on(f, [(120, 1360), (960, 1360)], ramp(t, tp, 0.4), INK_MINT_S, 5, seed=43, tip=False)
        write_on(f, "into you", 230, 1410, t, tp + 0.3, 44, INK_MINT_S)
    if t > tsm:
        kw(f, "ONLY A LITTLE", 540, 400, t, tsm, "pop", 100, col=INK_MINT_S)
    src(f, SRC_OX, t, t0 + 0.4)
    return finish(f, n, look="fresh")


# ---- S5: 'And let's be honest, nobody eats a hundred grams of til.' the worktop: a HUGE bowl of til marked 100 g; Chubby laughs and shakes his head ----
CX5, CY5, CS5 = 330, 1500, 1.05


def shot_S5(t, n):
    f = set_worktop(t); t0 = st_("S5"); tn = T("b1", "nobody") - 0.15
    shake = math.sin((t - tn) * 18) * ramp(t, tn, 0.15) * (1 - ramp(t, tn + 0.9, 0.3)) if t > tn else 0
    pose = nolean(POSE["shrug"]) if t > tn else dict(la=(28, 14), ra=(60, 50))
    chub(f, CX5, CY5, CS5, t=t, **pose, mouth=talk(t), expr="happy" if t > tn else "sus", brow="up", look=(0.8 * (1 - abs(shake)) + shake, 0.2),
         turn=0.4 + 0.4 * shake, lean=6 * shake)
    worktop_front(f, 1330)
    el_at(f, til_bowl_el(), 760, 1250, 1.0, t, t0 + 0.05)
    kw(f, "100 g OF TIL?", 540, 380, t, t0 + 0.1, "pop", 100, col=INKC)
    if t > tn: kw(f, "NOBODY.", 540, 545, t, tn, "shake", 120, col=ACC_S, amp=0.4)
    return finish(f, n, look="golden")


# ---- S5b: 'You eat a spoonful.' close: Chubby holds up one little spoon of til, deadpan; the giant bowl blurs behind ----
def shot_S5b(t, n):
    f = set_worktop(t, blur=9); t0 = st_("S5b"); ts = T("b1", "spoonful") - 0.15
    el_at(f, til_bowl_el(), 860, 1180, 1.25, op=0.85)
    f = dof(f, 3)
    chub(f, 470, 1960, 2.0, t=t, la=(26, 12), ra=(118, 150) if t > ts - 0.2 else (60, 40), hold=scale_el(spoon_til_el(), 0.95), hold_off=(10, -20), hold_front=True,
         hand_r="pinch", mouth=talk(t), expr="n", brow="n", look=(0.6, -0.3), turn=0.3)
    if t > ts: kw(f, "A SPOONFUL.", 540, 400, t, ts, "drop", 116, col=ACC_S, t1=ts + 1.2)
    return finish(f, n, look="golden")


# ---- S6: 'That spoonful has about a third of the calcium in one glass of milk.' BOARD: spoon = one third of a glass; 88 mg vs 276 mg ----
GL = [(600, 600), (940, 600), (910, 1250), (630, 1250)]


def shot_S6(t, n):
    f = board_bg(); t0 = st_("S6"); tt = T("b2", "third") - 0.15; tgl = T("b2", "glass") - 0.15
    el_at(f, spoon_til_el(), 260, 980, 1.0, t, t0 + 0.05)
    write_on(f, "1 spoon", 260, 1110, t, t0 + 0.2, 50, BP_INK)
    write_on(f, "=", 480, 960, t, t0 + 0.4, 80, BP_INK)
    k = ramp(t, t0 + 0.2, 0.5)
    cv2.fillPoly(f, [np.array(GL, np.int32)], C(_mix((253, 252, 248), MILK, k)), cv2.LINE_AA)
    for v in (1 / 3, 2 / 3):                                                         # thirds
        y = 1250 - v * 650; xl = 630 - v * 30; xr = 910 + v * 30
        draw_on(f, [(xl, y), (xr, y)], ramp(t, t0 + 0.5, 0.3), BP_INK, 3, seed=50 + int(v * 9), tip=False)
    if t > tt:
        P3 = [(630, 1250), (910, 1250), (920, 1250 - 650 / 3), (620, 1250 - 650 / 3)]
        hatch_on(f, P3, ramp(t, tt, 0.4), ACC, gap=16)
        kw(f, "1/3", 770, 1120, t, tt, "pop", 110, col=ACC_S)
    draw_on(f, GL, k, BP_INK, 8, seed=49, tip=False, closed=False)
    if t > tgl: write_on(f, "1 glass of milk", 740, 1340, t, tgl, 50, BP_INK)
    write_on(f, "about 88 mg", 260, 1200, t, tt + 0.3, 40, ACC_S)
    write_on(f, "276 mg", 770, 540, t, tgl + 0.2, 40, BP_INK)
    peek(f, t, 260, 640, 0.5, expr="sus", look=(0.5, 0.4))
    src(f, SRC_US, t, t0 + 0.6)
    return finish(f, n, look="fresh")


# ---- S7: 'So til is a lovely bonus.' the worktop: Chubby sprinkles til on a bowl, a glass of milk beside it; BONUS + sparkles ----
def shot_S7(t, n):
    f = set_worktop(t); t0 = st_("S7"); tb = T("c1", "bonus") - 0.15
    tilt = 0.5 + 0.5 * math.sin((t - t0) * 7)                                          # the shake of the spoon (main action)
    chub(f, 360, 1500, 1.05, t=t, la=(28, 14), ra=(100 + 10 * tilt, 80 + 8 * tilt), hold=scale_el(spoon_til_el(), 0.55), hold_off=(20, 0), hold_front=True,
         hand_r="grip", mouth=talk(t), expr="happy", brow="up", look=(0.8, 0.5), turn=0.4, lean=3 * math.sin(t * 2.2))   # secondary: a little sway (humming)
    for j in range(12):                                                              # falling seeds
        u = ((t - t0) * 1.6 + j / 12) % 1
        x = 640 + 30 * math.sin(j * 2.3) + 10 * u; y = 1130 + 150 * u
        cv2.ellipse(f, (int(x), int(y)), (7, 4), 30 * j, 0, 360, C(SES), -1, cv2.LINE_AA)
    worktop_front(f, 1330)
    el_at(f, bowl_el(0.7, (250, 246, 236)), 650, 1300, 0.9)
    el_at(f, milkglass_el(None), 880, 1250, 0.62)
    if t > tb:
        kw(f, "BONUS", 540, 420, t, tb, "pop", 150, col=ACC)
        for j in range(6):
            u = ((t - tb) * 1.4 + j / 6) % 1; a = 2 * math.pi * j / 6
            cv2.circle(f, (int(540 + (180 + 60 * u) * math.cos(a)), int(420 + (90 + 30 * u) * math.sin(a))), int(9 * (1 - u)), C(ACC_L), -1, cv2.LINE_AA)
    return finish(f, n, look="golden")


# ---- S7b: 'It just isn't a swap for your milk.' BOARD: spoon <-> glass with a swap arrow, crossed out: NOT A SWAP ----
def shot_S7b(t, n):
    f = board_bg(); t0 = st_("S7b"); tsw = T("c1", "swap") - 0.15
    el_at(f, spoon_til_el(), 260, 900, 1.0, t, t0 + 0.05)
    el_at(f, milkglass_el("happy"), 800, 880, 0.9, t, t0 + 0.15)
    draw_arrow_on(f, (420, 820), (650, 820), ramp(t, t0 + 0.3, 0.3), BP_INK, 7, 28, bend=-0.3)
    draw_arrow_on(f, (650, 980), (420, 980), ramp(t, t0 + 0.5, 0.3), BP_INK, 7, 28, bend=-0.3)
    stamp_x(f, 535, 900, 150, snap(t, tsw, 3) if t > tsw else 0)
    if t > tsw: kw(f, "NOT A SWAP", 540, 420, t, tsw, "shake", 116, col=(176, 40, 44), amp=0.4)
    write_on(f, "til = a bonus", 540, 1250, t, t0 + 0.2, 52, ACC_S)
    return finish(f, n, look="fresh")


# ---- S8: 'Send this to the friend who thinks one til laddoo beats a glass of milk.' the ring: the friend holds a til laddoo up like a title; Chubby holds the milk ----
FRIEND = (236, 150, 110)


def shot_S8(t, n):
    f = set_ring(t); t0 = st_("S8"); tl = T("c2", "luddoo") - 0.2; tb = T("c2", "beats") - 0.1
    chub(f, 300, 1560, 1.15, t=t, la=(30, 14), ra=(70, 60), hold=scale_el(milkglass_el(None), 0.62), hold_off=(0, -10), hold_front=True, hand_r="grip",
         mouth=talk(t), expr="sus", brow="sus", look=(1, 0), turn=0.5)
    bowtie(f, 300, 1560, 1.15, t)
    up = snap(t, tl, 4) if t > tl else 0.0
    fx = 790; fs = 1.15
    chub(f, fx, 1560, fs, t=t, shirt=FRIEND, la=(30, 14), ra=(40 + 115 * up, 20 + 155 * up), hold=scale_el(laddoo_el("happy"), 1.0), hold_front=True,
         mouth="o" if up > 0.5 else 0, expr="happy", brow="up", look=(0, -0.6 * up), turn=-0.3)
    dress(f, fx, 1560, fs, "cousin")
    if t > tb: el_at(f, belt_el(), fx, 1560 - 250 * fs, 0.7, t, tb)
    ring_front(f, t, [tl])
    ui_word(f, "send this to the friend who thinks", "[LADDOO] WINS", 420, t, T("c2", "Send") - 0.05, col=MILK, acc=ACC, size=124, lead_col=MILK)
    return finish(f, n, look="night")


# ---- S9: the logo beat (0.7 s) ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_ring(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.3) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.15) / 0.2))
    return finish(f, n, look="golden")


# ---- S10: the LOOP TAIL: back in the ring exactly like frame 0 (no caption); loop_seam blends into frame 0 ----
def shot_S10(t, n):
    f = set_ring(t)
    ring_scene(f, t, ann=dict(expr="happy", brow="up", mouth=0))
    return finish(f, n, look="night")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "more") - 0.1, 0.25, 8), (T("i1", "milk") - 0.1, 0.25, 8), (T("i2", "eight") - 0.1, 0.35, 12), (T("i2", "paper") - 0.15, 0.25, 8),
           (KO_T, 0.5, 20), (T("a1", "skin") - 0.3, 0.25, 8), (T("a1", "stuck") - 0.1, 0.3, 10), (CUFF_T, 0.45, 16), (T("a2", "small") - 0.15, 0.3, 10),
           (T("b1", "nobody") - 0.15, 0.3, 10), (T("b1", "spoonful") - 0.15, 0.3, 10), (T("b2", "third") - 0.15, 0.35, 12), (T("c1", "bonus") - 0.15, 0.25, 8),
           (T("c1", "swap") - 0.15, 0.35, 12), (T("c2", "luddoo") - 0.2, 0.3, 10)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


_FIRST = {}


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "erase" and dt < 0.42:
            f = erase_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42)
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    if i == len(SHOTS) - 1:                                                     # the LOOP SEAM: the tail melts into frame 0
        if "f0" not in _FIRST: _FIRST["f0"] = rs(SHOTS[0]["id"], 0.0, 0)
        f = loop_seam(f, _FIRST["f0"], t, END, 0.33)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
