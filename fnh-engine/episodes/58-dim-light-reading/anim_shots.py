# ================= shots: FreshNestHub 58 — "Does reading in dim light ruin your eyes?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: a POWER CUT at the study desk, lit ONLY by a candle (warm orange pool that shivers with the flame, everything else deep navy) for the
# myth + the strain; the white board + blue ink for the eye; then the CURTAINS FLY OPEN and the video turns to DAYLIGHT (sunshine-yellow accent, a
# noon park) for the real answer. ONE accent = SUNSHINE YELLOW (the sun, the question words, the focus effort). Red only on 'too long' + the myth stamp.
# Story: frame 0 = Chubby squinting into a book by a candle, mom already in the doorway yelling -> the question. Mom says yes, eye doctors say no
# (MYTH) + the macro loop ('the real risk is hiding somewhere else' = a shut curtain). Why it aches: the focus muscle works harder + fewer blinks = dry
# = eye strain, and it goes away with rest (he blows the candle out: smoke; sleeps). The real risk: too little sunlight (the curtains fly open).
# Kids outside 1-2 h a day -> less nearsighted (defined on sight: far things blurry). Experts think daylight stops the eyeball growing too long (board).
# Safe tip: still blurry in good light -> eye check. Send line = the mom; the tail rebuilds frame 0 (loop).
# CRAFT (ep 58) = FLAME + SMOKE effects animation (lib58 candle_flame / flick / smoke_wisp) + candle_light(): the flame's flicker drives a MULTIPLY light
# layer over the whole set + characters (the 'environment' layer of the fire tutorials), so the room breathes with the flame.
END = round(LINES["c2"]["end"] + 0.9, 3)               # 0.05 s air + 0.4 s logo + 0.45 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "ruin") - 0.12, "punch"),
    ("S1", T("i2", "Your") - 0.12, "whip"), ("S1b", T("i2", "But") - 0.1, "cut"), ("S1c", T("i2", "The") - 0.1, "punch"),
    ("S2", T("a1", "So") - 0.12, "erase"), ("S2b", T("a1", "In") - 0.1, "cut"),
    ("S3", T("a2", "And") - 0.12, "whip"), ("S3b", T("a2", "That's") - 0.1, "punch"), ("S3c", T("a2", "goes") - 0.1, "cut"),
    ("S4", T("b1", "So") - 0.12, "punch"), ("S4b", T("b1", "sunlight.") - 0.3, "flash"),
    ("S5", T("b2", "Kids") - 0.12, "whip"), ("S5b", T("b2", "less") - 0.1, "cut"),
    ("S6", T("b3", "Experts") - 0.12, "erase"),
    ("S7", T("c1", "But") - 0.12, "whip"), ("S7b", T("c1", "time") - 0.1, "cut"),
    ("S8", T("c2", "Send") - 0.1, "whip"),
    ("S9", LINES["c2"]["end"] + 0.05, "punch"), ("S10", round(LINES["c2"]["end"] + 0.45, 3), "cut"),
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


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, PAPER, 22), 540, y, op=clamp((t - t0) / 0.2))


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def el_at(f, el, x, y, s=1.0, t=None, t0=None, rot=0.0, op=1.0):
    k = 1.0 if t0 is None else (snap(t, t0, 4) if t >= t0 else 0.0)
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, rot, k, op, 0.0)


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None, blink=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look,
                   turn=clamp(look[0]) * 0.5, blink=blink)


def hook_band(f, y0=228, y1=700, a=0.72, col=None):
    if a <= 0: return
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(col or PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0)."""
    kw(f, "DO YOU KNOW IF", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "READING IN DIM LIGHT", 540, 425, t, t0, "pop", 80, col=BP_INK, op=op)
    kw(f, "= RUINED EYES?", 540, 590, t, t0, "shake", 124, col=ACC_S, amp=0.35, op=op)


_GX = np.arange(0, W, 8, dtype=np.float32)[None, :]; _GY = np.arange(0, H, 8, dtype=np.float32)[:, None]


def candle_light(f, x, y, lv, r=560, amb=0.34):
    """the flame's light as a MULTIPLY layer over everything drawn so far: a warm pool round (x, y) that breathes with lv, cool ambient elsewhere."""
    rr = r * (0.92 + 0.08 * lv)
    g = np.exp(-((_GX - x) ** 2 + (_GY - y) ** 2) / (2 * rr ** 2)).astype(np.float32)
    g = cv2.resize(g, (W, H))[..., None]
    warm = np.array([1.0, 0.84, 0.64], np.float32); cool = np.array([0.66, 0.72, 0.98], np.float32)
    m = amb * cool + (1 - amb) * g * min(lv, 1.15) * warm * 1.08
    f[:] = f * np.clip(m, 0, 1.2)


def candle_at(f, x, y, s, t, on=1.0, gust=0.0, seed=0, melt=0.0):
    """the candle element + where its wick top is; returns (wick top, light level). Draw the flame AFTER candle_light so it stays bright."""
    comp(f, scale_el(candle_el(melt), s), x, y)
    wx, wy = x, y - (WICK_DY - 60 * round(clamp(melt) * 4) / 4) * s
    return (wx, wy), (flick(t, seed) * on if on > 0.02 else 0.0)


def flame_only(f, x, y, s, t, on=1.0, gust=0.0, seed=0):
    lv = candle_flame(f, x, y, t, s, on, gust, seed)
    glow(f, x, y - 40 * s, 90 * s, (255, 220, 150), 0.25 * lv * on)
    return lv


def doctor58(f, x, y, s, t, shake=0.0):
    chub(f, x, y, s, t=t, shirt=COAT, la=(26, 14), ra=(60, 40), hand_r="point", mouth=talk(t), expr="smirk", brow="up", look=(0.3 * shake, 0), turn=0.3 * shake)
    hx2, hy2 = x + 0.3 * shake * 14 * s, y - 420 * s                                         # head mirror = 'doctor' at a glance
    cv2.line(f, (int(hx2 - 96 * s), int(hy2 - 62 * s)), (int(hx2 + 96 * s), int(hy2 - 62 * s)), C(INKC), max(3, int(8 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C((214, 222, 230)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(9 * s), C(INKC), -1, cv2.LINE_AA)
    el_at(f, steth_el(), x - 10 * s, y - 280 * s, 0.6 * s / 1.5)


CX, CY, CS = 470, 2080, 2.0           # Chubby at the desk (desk top 1560), leaning in toward the book
NX, NY, NS_ = 930, 1880, 1.4         # mom in the dark doorway
CAN_X, CAN_Y, CAN_S = 150, DESK_TOP - 150, 1.0


def reader(f, t, lean_in=1.0, mouth=None, expr="sus"):
    """Chubby squinting into a book held close to his face (the book drawn between his hands)."""
    rock = 4 * math.sin(t * 1.7)
    hd = chub(f, CX, CY, CS, t=t, la=(-60, -150), ra=(-60, -150), hand_l="grip", hand_r="grip", mouth=mouth if mouth is not None else 0,
              expr=expr, brow="sus", look=(-0.1, 0.5), lean=-6 * lean_in + rock * 0.3)
    bx = (hd[1][0] + hd[-1][0]) / 2; by = min(hd[1][1], hd[-1][1]) + 10
    comp(f, scale_el(book_el(), 1.25), bx, by)
    return hd


# ---- S0: HOOK at frame 0 = the POWER CUT: Chubby squinting into a book by a candle, mom in the doorway mid-yell ----
def scene0(f, t):
    mom58(f, NX, NY, NS_, t, la=(30, 20), ra=(120 + 10 * math.sin(t * 12), 150), hand_r="point", mouth="jaw" if t % 1.2 < 0.8 else 2,
          expr="angry", brow="sus", look=(-1, 0.1), turn=-0.5, lean=-4)
    reader(f, t)
    desk_front(f, DESK_TOP, t, lamp=True)
    (wx, wy), lv = candle_at(f, CAN_X, CAN_Y, CAN_S, t, seed=1)
    candle_light(f, wx, wy - 40, lv)
    candle_flame(f, wx, wy, t, CAN_S, 1.0, 0.0, 1)                                       # the flame itself is never darkened
    return lv


def shot_S0(t, n):
    f = set_desk(t, door=0.0)
    scene0(f, t)
    hook_band(f, a=0.62); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S0b: '...ruin your eyes?' THE FACE close-up: squint, eyes inches from the page, the flame big in the foreground (left) ----
def shot_S0b(t, n):
    f = set_desk(t, 9, door=0.0); f = dof(f, 3)
    peek(f, t, 640, 1180, 1.25, expr="sus", look=(-0.6, 0.5), mouth=0)
    comp(f, scale_el(book_el(), 2.3), 640, 1560)
    candle_light(f, 180, 1180, flick(t, 1), r=620, amb=0.3)
    comp(f, scale_el(candle_el(), 2.1), 180, 1560)
    flame_only(f, 180, 1560 - WICK_DY * 2.1, 2.1, t, seed=1)
    hook_band(f, a=0.62); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S1: 'Your mom says yes.' MOM close in the candlelit doorway: finger wag, YES! ----
def shot_S1(t, n):
    f = set_desk(t, 9, door=0.0); f = dof(f, 2); ty = T("i2", "yes.") - 0.1
    wag = 12 * math.sin(t * 13)
    mom58(f, 620, 2080, 2.2, t, la=(30, 20), ra=(120 + wag, 150), hand_r="point", mouth=talk(t) if t < ty else "jaw", expr="angry", brow="sus",
          look=(-0.5, 0), turn=-0.2, lean=wag * 0.1)
    candle_light(f, 120, 1300, flick(t, 1), r=720, amb=0.36)
    hook_band(f, 250, 640, 0.7)
    kw(f, "MOM SAYS:", 540, 330, t, T("i2", "mom") - 0.2, "pop", 96, col=INKC)
    if t > ty: kw(f, "YES!", 540, 520, t, ty, "shake", 170, col=RED, amp=0.4)
    return finish(f, n, look="night")


# ---- S1b: 'But eye doctors say... no.' the eye doctor in front of an eye chart, a calm head shake, NO. + MYTH stamp ----
def shot_S1b(t, n):
    f = board_bg(); t0 = st_("S1b"); tno = T("i2", "no.") - 0.12
    el_at(f, eye_chart_el(), 830, 1120, 1.0)
    sh = math.sin((t - tno) * 14) * math.exp(-(t - tno) * 3) if t > tno else 0.0
    doctor58(f, 400, 1680, 1.5, t, shake=sh)
    kw(f, "EYE DOCTORS:", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > tno:
        kw(f, "NO.", 540, 520, t, tno, "pop", 190, col=ACC_S)
        el_at(f, vstamp_el("MYTH", RED, 90), 830, 760, 1.0, t, tno + 0.2, rot=8)
    src(f, SRC_HOP, t, t0 + 0.3, y=1560)
    return finish(f, n, look="fresh")


# ---- S1c: 'The real risk is hiding somewhere else.' THE SHUT CURTAIN as a dark shape with a line of daylight + a big '?' (the macro loop) ----
def dark_room(col=(40, 42, 62)):
    f = np.ones((H, W, 3), np.float32) * np.array(C(col), np.float32)
    f[1380:] = np.array(C((30, 30, 44)), np.float32)
    return f


def shot_S1c(t, n):
    f = dark_room(); t0 = st_("S1c")
    curtain_window(f, 260, 640, 820, 1260, 0.0, t, sun=1.0, dark=0.6)
    gl = 0.5 + 0.5 * math.sin(t * 3)
    cv2.line(f, (540, 600), (540, 1310), C((255, 236, 170)), 6 + int(4 * gl), cv2.LINE_AA)          # a line of sun at the gap
    glow(f, 540, 950, 220, (255, 220, 140), 0.18 + 0.06 * gl)
    kw(f, "THE REAL RISK", 540, 330, t, T("i2", "real") - 0.15, "pop", 100, col=(250, 244, 230))
    kw(f, "IS HIDING...", 540, 470, t, T("i2", "hiding") - 0.1, "sneak", 86, col=ACC)
    kw(f, "?", 540, 1450, t, T("i2", "else.") - 0.2, "shake", 220, col=ACC, amp=0.4)
    peek(f, t, 860, 1500, 0.5, expr="sus", look=(-0.8, -0.4))
    return finish(f, n, look="night")


# ---- S2: 'So why do your eyes ache?' the EYE draws itself on the board (side view) ----
EX, EY = 580, 1000


def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); ta = T("a1", "ache?") - 0.1
    k = ramp(t, t0, 0.9)
    eye_board(f, EX, EY, t, k=k, R=300)
    kw(f, "WHY DO THEY", 540, 330, t, t0 + 0.1, "pop", 92, col=BP_INK)
    if t > ta: kw(f, "ACHE?", 540, 1440, t, ta, "shake", 170, col=ACC_S, amp=0.4)
    if t > t0 + 0.6: write_on(f, "your eye, from the side", 540, 1290, t, t0 + 0.6, 34, BP_INK, cps=40)
    peek(f, t, 900, 560, 0.42, expr="sad", look=(-0.8, 0.5))
    return finish(f, n, look="fresh")


# ---- S2b: 'In dim light, they have to work extra hard to focus.' little light in -> the pupil opens wide, the FOCUS MUSCLE squeezes + sweats ----
def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); td = T("a1", "dim") - 0.1; tw = T("a1", "work") - 0.1
    pup = 0.35 + 0.6 * ramp(t, td + 0.1, 0.5)
    sq = ramp(t, tw, 0.4) * (0.75 + 0.25 * math.sin(t * 9)) if t > tw else 0.0
    out = eye_board(f, EX, EY, t, k=1.0, pupil=pup, squeeze=sq, sweat=1.0 if t > tw + 0.2 else 0.0, rays=ramp(t, t0, 0.6), light_amt=0.25, R=300)
    comp(f, scale_el(candle_el(), 0.6), 120, EY + 60)
    flame_only(f, 120, EY + 60 - WICK_DY * 0.6, 0.6, t, seed=2)
    kw(f, "DIM LIGHT", 540, 320, t, td, "pop", 104, col=INKC)
    if t > td + 0.3:
        lx = out["front"] + 46
        draw_arrow_on(f, (lx - 60, EY - 360), (lx - 4, EY - 120), ramp(t, td + 0.3, 0.25), BP_INK, 6, 22)
        write_on(f, "pupil opens wide", 470, EY - 410, t, td + 0.3, 32, BP_INK, cps=40)
    if t > tw:
        lc = out["lens"]
        draw_arrow_on(f, (lc[0] + 240, EY + 360), (lc[0] + 40, EY + 120), ramp(t, tw, 0.25), ACC_S, 7, 24)
        write_on(f, "focus muscle", lc[0] + 200, EY + 410, t, tw, 34, ACC_S, cps=40)
        kw(f, "WORKS HARDER", 540, 1500, t, tw, "shake", 110, col=ACC_S, amp=0.3)
    return finish(f, n, look="fresh")


# ---- S3: 'And you blink less, so they dry out.' face close-up by the candle: a wide unblinking stare, a BLINK tally that thins; DRY parches ----
def shot_S3(t, n):
    f = set_desk(t, 9, door=0.0); f = dof(f, 3); t0 = st_("S3"); tb = T("a2", "blink") - 0.1; tdr = T("a2", "dry") - 0.1
    blinks = [t0 + 0.15, t0 + 0.55]                                                     # blinks get rarer, then stop
    bl = any(b <= t < b + 0.12 for b in blinks)
    peek(f, t, 600, 1150, 1.3, expr="wow" if t > tb else "sus", look=(0, 0.5), mouth=0, blink=bl)
    candle_light(f, 140, 1300, flick(t, 1), r=700, amb=0.32)
    comp(f, scale_el(candle_el(), 1.8), 130, 1660)
    flame_only(f, 130, 1660 - WICK_DY * 1.8, 1.8, t, seed=1)
    hook_band(f, 250, 560, 0.7)
    kw(f, "BLINKS", 540, 330, t, tb, "pop", 96, col=INKC)
    if t > tb:                                                                            # tally marks: fewer as time passes
        left = 6 - int(clamp((t - tb) / 1.0) * 5)
        for j in range(left):
            cv2.line(f, (int(380 + 56 * j), 430), (int(370 + 56 * j), 510), C(INKC), 9, cv2.LINE_AA)
        draw_arrow_on(f, (760, 420), (760, 520), ramp(t, tb + 0.2, 0.2), RED, 9, 26)
    if t > tdr:
        hook_band(f, 1330, 1490, 0.75)
        kw(f, "DRY", 540, 1410, t, tdr, "parch", 160, col=ACC_S, t1=tdr + 0.3)
    return finish(f, n, look="night")


# ---- S3b: 'That's eye strain,' Chubby rubs his eyes at the desk; EYE STRAIN + the three symptoms write on ----
def shot_S3b(t, n):
    f = set_desk(t, door=0.0); ts = T("a2", "strain,") - 0.1
    rub = 10 * math.sin(t * 16)
    chub(f, CX, CY, CS, t=t, la=(-150 + rub, -150), ra=(-150 - rub, -150), hand_l="grip", hand_r="grip", mouth="wavy", expr="gross", brow="sad", lean=4)
    desk_front(f, DESK_TOP, t)
    comp(f, scale_el(book_el(), 1.1), 800, DESK_TOP - 30)
    (wx, wy), lv = candle_at(f, CAN_X, CAN_Y, CAN_S, t, seed=1)
    candle_light(f, wx, wy - 40, lv)
    candle_flame(f, wx, wy, t, CAN_S, 1.0, 0.0, 1)
    hook_band(f, 250, 640, 0.7)
    kw(f, "EYE STRAIN", 540, 330, t, ts, "shake", 118, col=ACC_S, amp=0.25)
    write_on(f, "tired eyes, headache, blur", 540, 510, t, ts + 0.25, 36, INKC, cps=40)
    src(f, SRC_STRAIN, t, ts + 0.4, y=1490)
    return finish(f, n, look="night")


# ---- S3c: '...and it goes away once you rest.' he BLOWS the candle out (smoke curls up), lays his head down -> morning light, TEMPORARY + tick ----
def shot_S3c(t, n):
    t0 = st_("S3c"); tbo = t0 + 0.35; tr = T("a2", "rest.") - 0.1
    morning = ramp(t, tr + 0.15, 0.5)
    f = set_desk(t, door=0.0)
    sleepy = tbo + 0.45 < t and morning < 0.5
    blow = t < tbo + 0.1
    if sleepy:
        chub(f, CX, CY + 60, CS, t=t, la=(-100, -160), ra=(-100, -160), mouth=0, expr="sleepy", brow="n", blink=True, lean=14, squash=0.15)
    else:
        chub(f, CX, CY, CS, t=t, la=(-40, -150) if blow else (30, 20), ra=(150, 170) if morning > 0.5 else (30, 20), mouth="o" if blow else 3,
             expr="happy" if morning > 0.5 else "n", brow="up", lean=-8 if blow else 0)
    desk_front(f, DESK_TOP, t)
    on = 1.0 if t < tbo else 0.0
    gust = -16 * ramp(t, t0, 0.3) if t < tbo else 0.0
    (wx, wy), lv = candle_at(f, CAN_X, CAN_Y, CAN_S, t, on=on, gust=gust, seed=1, melt=0.25)
    if morning < 1:
        g = f.copy(); candle_light(g, wx, wy - 40, lv if t < tbo else 0.3, amb=0.34 if t < tbo else 0.5)
        f[:] = g * (1 - morning) + f * morning
    if morning > 0:
        f[:] = f * (1 - 0.25 * morning) + np.array(C((255, 238, 200)), np.float32) * 0.25 * morning
        god_rays(f, 160, 420, t, (255, 236, 170), 0.2 * morning, 7, 1400, 1.0, 1.0, 2)
    if t < tbo: candle_flame(f, wx, wy, t, CAN_S, on, gust, 1)
    smoke_wisp(f, wx, wy, t, tbo, 2.4, 1.4, seed=3, col=(236, 236, 244))
    if sleepy: kw(f, "Z z z", 780, 1220, t, tbo + 0.55, "breathe", 80, col=(230, 230, 250))
    hook_band(f, 250, 560, 0.7)
    kw(f, "REST...", 540, 330, t, T("a2", "goes") - 0.05, "pop", 96, col=INKC)
    if t > tr:
        kw(f, "TEMPORARY", 540, 480, t, tr, "pop", 120, col=OKG)
    return finish(f, n, look="night" if morning < 0.5 else "warm")


# ---- S4: 'So where's the real risk? It's not the dim light.' the shut curtain again (callback); the candle gets a red X ----
def shot_S4(t, n):
    f = dark_room((52, 54, 76)); t0 = st_("S4"); tn = T("b1", "not") - 0.1
    curtain_window(f, 260, 640, 820, 1260, 0.0, t, sun=1.0, dark=0.55)
    cv2.line(f, (540, 600), (540, 1310), C((255, 236, 170)), 8, cv2.LINE_AA)
    glow(f, 540, 950, 220, (255, 220, 140), 0.2)
    kw(f, "WHERE'S THE", 540, 300, t, t0 + 0.05, "pop", 84, col=(250, 244, 230))
    kw(f, "REAL RISK?", 540, 430, t, t0 + 0.3, "shake", 110, col=ACC, amp=0.3)
    comp(f, scale_el(candle_el(), 0.9), 200, 1440)
    flame_only(f, 200, 1440 - WICK_DY * 0.9, 0.9, t, seed=4)
    if t > tn:
        draw_on(f, [(100, 1250), (300, 1500)], ramp(t, tn, 0.25), RED, 16, seed=593, tip=False)
        draw_on(f, [(300, 1250), (100, 1500)], ramp(t, tn + 0.12, 0.25), RED, 16, seed=594, tip=False)
        kw(f, "NOT DIM LIGHT", 650, 1440, t, tn + 0.1, "drop", 70, col=(250, 244, 230), t1=tn + 1.0)
    peek(f, t, 880, 1150, 0.5, expr="sus", look=(-0.8, -0.3))
    return finish(f, n, look="night")


# ---- S4b: 'It's too little sunlight.' THE CURTAINS FLY OPEN: daylight floods the room (the lighting beat), Chubby squints, then grins ----
def shot_S4b(t, n):
    t0 = st_("S4b"); to = t0 + 0.12
    k = clamp(snap(t, to, 6)) if t > to else 0.0
    f = dark_room(_mix((52, 54, 76), (250, 240, 214), k))
    if k > 0: f[1380:] = f[1380:] * (1 - k) + np.array(C((214, 190, 150)), np.float32) * k
    curtain_window(f, 260, 560, 820, 1180, k, t, sun=1.0, dark=0.55 * (1 - k))
    if k > 0:
        god_rays(f, 720, 680, t, (255, 236, 170), 0.32 * k, 9, 1500, 1.2, 2.0, 3)
        glow(f, 540, 900, 420, (255, 236, 170), 0.25 * k)
    tk = take(t, to, 1.0)
    happy = t > to + 0.6
    chub(f, 540, 2050 + tk["dy"], 1.7, t=t, la=(150, 160) if happy else (-140, -160), ra=(150, 160) if happy else (40, 20),
         mouth=3 if happy else "o", expr="happy" if happy else tk["expr"], brow=tk["brow"], squash=tk["squash"], look=(0.3, -0.4))
    kw(f, "TOO LITTLE", 540, 300, t, t0 + 0.02, "pop", 90, col=INKC if k > 0.5 else (250, 244, 230))
    kw(f, "SUNLIGHT", 540, 430, t, to, "pop", 150, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S5: 'Kids who play outside for one to two hours a day...' NEW PLACE the NOON PARK: Chubby runs with a ball, a kid jumps, a kid cheers ----
def shot_S5(t, n):
    f = set_park(t); t0 = st_("S5"); th = T("b2", "one") - 0.1
    j = abs(math.sin((t - t0) * 5.2)) * 40
    kid58(f, 860, 1600 - j, 1.0, t, shirt=(236, 120, 70), la=(150, 170), ra=(150, 170), mouth=3, expr="happy")
    kid58(f, 170, 1600, 0.95, t, shirt=(120, 130, 220), cap=False, la=(40, 30), ra=(150, 170), mouth=3, expr="happy")
    w = walk(t, 300, 1760, 1.25, speed=140, dir=1, period=0.62, t0=t0, lift=40)
    chub(f, s=1.25, t=t, mouth=3, expr="happy", brow="up", **w)
    bxp = w["x"] + 130
    by_ = 1730 - abs(math.sin(t * 9)) * 60
    cv2.circle(f, (int(bxp), int(by_)), 34, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (int(bxp), int(by_)), 34, C(INKC), 6, cv2.LINE_AA)
    cv2.ellipse(f, (int(bxp), int(by_)), (34, 12), 20, 0, 360, C(INKC), 3, cv2.LINE_AA)
    park_front(f, 1760)
    hook_band(f, 250, 660, 0.55)
    kw(f, "PLAY OUTSIDE", 540, 330, t, T("b2", "outside") - 0.15, "pop", 104, col=INKC)
    if t > th:
        kw(f, "1-2 HOURS", 540, 470, t, th, "pop", 120, col=ACC_S)
        kw(f, "A DAY", 540, 590, t, T("b2", "day") - 0.1, "pop", 80, col=INKC)
    src(f, SRC_OUT, t, t0 + 0.4, y=1480)
    return finish(f, n, look="fresh")


# ---- S5b: '...are less likely to become nearsighted.' DEFINE ON SIGHT: the book stays sharp, the whole far park goes blurry = NEARSIGHTED ----
def shot_S5b(t, n):
    t0 = st_("S5b"); tn = T("b2", "nearsighted.") - 0.1
    f = set_park(t, blur=4)
    if t > tn: f = cv2.GaussianBlur(f, (0, 0), 3 + 9 * ramp(t, tn, 0.5))
    comp(f, scale_el(book_el(), 1.6), 540, 1300)
    peek(f, t, 860, 1150, 0.5, expr="sus" if t > tn else "happy", look=(-0.5, -0.6))
    hook_band(f, 250, 680, 0.72)
    kw(f, "LESS LIKELY", 540, 320, t, T("b2", "less") - 0.05, "pop", 96, col=INKC)
    if t > tn:
        kw(f, "NEARSIGHTED", 540, 470, t, tn, "pop", 118, col=ACC_S)
        write_on(f, "near = sharp, far = blurry", 540, 600, t, tn + 0.25, 36, INKC, cps=40)
    return finish(f, n, look="fresh")


# ---- S6: 'Experts think all that bright daylight helps stop the eyeball from growing too long.' the board eye keeps trying to stretch; the SUN
# draws and STOP; then the ghost of a TOO-LONG eye (focus lands in front of the retina) in red below ----
def shot_S6(t, n):
    f = board_bg(); t0 = st_("S6"); tb = T("b3", "bright") - 0.1; tst = T("b3", "stop") - 0.1; tg = T("b3", "growing") - 0.1; tl = T("b3", "long.") - 0.1
    write_on(f, "experts think", 540, 300, t, t0 + 0.05, 40, BP_INK, cps=40)
    tries = 0.35 * (0.5 - 0.5 * math.cos((t - t0) * 4.0)) * (1 - ramp(t, tst, 0.4))        # it keeps trying to stretch... until the light stops it
    up = ramp(t, tg, 0.4)
    yo = -120 * up
    sc_ = 1.0 - 0.25 * up
    eye_board(f, EX, EY + yo, t, k=ramp(t, t0, 0.5), R=230 * sc_, length=tries, rays=ramp(t, t0 + 0.2, 0.5), light_amt=1.0, seed=590)
    if t > tg:                                                                            # the ghost below: what TOO LONG looks like
        g2 = f.copy(); eye_board(g2, EX + 40, EY + 300, t, k=1.0, R=130, length=1.0, rays=1.0, seed=600)
        f[:] = f * (1 - 0.8 * up) + g2 * 0.8 * up
        kw(f, "TOO LONG", 540, 1470, t, tl, "shake", 96, col=RED, amp=0.3)
        write_on(f, "= nearsighted", 250, 1270, t, tl + 0.15, 30, RED, cps=40)
    if t > tb:
        sk = ramp(t, tb, 0.5)
        draw_ell_on(f, 150, 560, 66, 66, sk, ACC_S, 9, seed=601)
        if sk >= 1:
            cv2.circle(f, (150, 560), 60, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (150, 560), 60, C(ACC_S), 6, cv2.LINE_AA)
        for i in range(8):
            a = i * math.pi / 4 + 0.2
            draw_on(f, [(150 + 82 * math.cos(a), 560 + 82 * math.sin(a)), (150 + 112 * math.cos(a), 560 + 112 * math.sin(a))], clamp(sk * 2 - 1), ACC_S, 6, seed=602 + i, tip=False)
        kw(f, "BRIGHT DAYLIGHT", 600, 430, t, tb, "pop", 74, col=ACC_S)
    if t > tst and t < tg + 0.2:
        kw(f, "STOP", 860, 620, t, tst, "shake", 100, col=ACC_S, amp=0.3)
    src(f, SRC_LONG, t, t0 + 0.4, y=1560)
    return finish(f, n, look="fresh")


# ---- S7: 'But if the words still look blurry in good light,' a bright room: Chubby squints at a page that stays blurry ----
def shot_S7(t, n):
    tbl = T("c1", "blurry") - 0.1
    f = set_desk(t, door=1.0)
    f = f * 0.55 + np.array(C((255, 246, 222)), np.float32) * 0.45                       # good light: the room is bright now
    god_rays(f, 200, 400, t, (255, 236, 170), 0.18, 7, 1400, 1.0, 1.0, 2)
    reader(f, t, lean_in=1.2, mouth=0, expr="sus")
    desk_front(f, DESK_TOP, t)
    hook_band(f, 250, 860, 0.75)
    page = np.ones((300, 620, 3), np.float32) * np.array(C((252, 248, 236)), np.float32)
    for j in range(5): cv2.line(page, (40, 60 + 50 * j), (580, 60 + 50 * j), C(INKC), 10, cv2.LINE_AA)
    if t > tbl: page = cv2.GaussianBlur(page, (0, 0), 2 + 6 * ramp(t, tbl, 0.4))
    f[300:600, 230:850] = page
    cv2.rectangle(f, (230, 300), (850, 600), C(INKC), 6, cv2.LINE_AA)
    if t > tbl: kw(f, "STILL BLURRY?", 540, 730, t, tbl, "shake", 96, col=RED, amp=0.3)
    return finish(f, n, look="warm")


# ---- S7b: '...it's time to get your eyes checked.' the eye doctor points at the chart; GET YOUR EYES CHECKED ----
def shot_S7b(t, n):
    f = board_bg(); t0 = st_("S7b"); tc = T("c1", "checked.") - 0.1
    el_at(f, eye_chart_el(), 780, 1060, 1.15)
    doctor58(f, 360, 1700, 1.5, t)
    kw(f, "GET YOUR EYES", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > tc: kw(f, "CHECKED", 540, 470, t, tc, "pop", 140, col=ACC_S)
    src(f, SRC_CHECK, t, t0 + 0.3, y=1560)
    return finish(f, n, look="fresh")


# ---- S8: 'Send this to the mom who still yells, you'll ruin your eyes!' back in the power cut: mom yells from the door, Chubby points at us ----
def shot_S8(t, n):
    f = set_desk(t, door=0.0); tm = T("c2", "yells,") - 0.1
    mom58(f, NX, NY, NS_, t, la=(30, 20), ra=(120 + 10 * math.sin(t * 12), 150), hand_r="point", mouth="jaw" if t > tm else 0,
          expr="angry", brow="sus", look=(-1, 0.1), turn=-0.5, lean=-4)
    chub(f, CX - 80, CY, CS, t=t, la=(26, 14), ra=(110, 110), hand_r="point", mouth=talk(t), expr="smirk", brow="up", look=(0, 0.2))
    desk_front(f, DESK_TOP, t)
    (wx, wy), lv = candle_at(f, CAN_X - 60, CAN_Y, CAN_S, t, seed=1)
    candle_light(f, wx, wy - 40, lv, r=640, amb=0.4)
    candle_flame(f, wx, wy, t, CAN_S, 1.0, 0.0, 1)
    hook_band(f, 250, 600, 0.78)
    ui_word(f, "send this to the mom who still yells", "[RUIN YOUR EYES!]", 420, t, T("c2", "Send") - 0.05, col=INKC, acc=ACC_S, size=96, lead_col=INKC)
    return finish(f, n, look="night")


# ---- S9: the logo beat (0.4 s) ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_desk(t, door=0.0); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S10: the LOOP TAIL: replays the run-up to frame 0 so the seam lands on the same pose ----
def shot_S10(t, n):
    f = set_desk(t - END, door=0.0)
    scene0(f, t - END)
    hook_band(f, a=0.62)
    return finish(f, n, look="night")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "ruin") - 0.12, 0.3, 12), (T("i2", "yes.") - 0.1, 0.3, 10), (T("i2", "no.") - 0.12, 0.35, 12),
           (T("a1", "ache?") - 0.1, 0.3, 10), (T("a1", "work") - 0.1, 0.3, 10), (T("a2", "dry") - 0.1, 0.3, 10),
           (T("b1", "not") - 0.1, 0.3, 10), (T("b1", "sunlight.") - 0.18, 0.4, 16), (T("b2", "nearsighted.") - 0.1, 0.3, 10),
           (T("b3", "growing") - 0.1, 0.3, 12), (T("c1", "blurry") - 0.1, 0.3, 10)]


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
        elif k == "morph" and dt < 0.42:
            a, b = MORPH[sh["id"]]; f = morph_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, a, b)
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    if i == len(SHOTS) - 1:
        if "f0" not in _FIRST: _FIRST["f0"] = rs(SHOTS[0]["id"], 0.0, 0)
        f = loop_seam(f, _FIRST["f0"], t, END, 0.33)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
