# Pepsi pilot in the CURRENT line-art cast (R&D 3 Nov 2026): the only earlier lab sheet (31 Oct) predates the stick cast and loaded mascot3d only.
# Tonight's build is the first YOUR MOVE in the new look. Usage: python3 storyboard_pepsi_lineart_nov3.py <out_dir>
import os, sys, json, time
TPL_ = "/home/claude/nextbignow-videos/studio/template/scripts"
OUT = sys.argv[1]; os.makedirs(f"{OUT}/work", exist_ok=True)
if not os.path.exists(f"{OUT}/work/align.json"):
    json.dump(dict(lines={"i1": dict(start=0.0, end=3.0)}, words=[dict(line="i1", w="could", t=0.3)], dur=4.0, LEAD=0.0, fake=True), open(f"{OUT}/work/align.json", "w"))
if not os.path.exists(f"{OUT}/work/vo.wav"):
    import numpy as _np, soundfile as _sf; _sf.write(f"{OUT}/work/vo.wav", 0.02 * _np.sin(_np.arange(48000 * 4) * 0.05).astype(_np.float32), 48000)
os.environ["PROJ"] = OUT
for _p in ("anim_base.py", "anim_cine.py", "anim_mascot3d.py", "anim_stick.py", "anim_sets.py", "anim_props.py", "anim_props2.py", "anim_props3.py", "anim_story.py", "anim_story2.py", "anim_props4.py", "anim_props5.py", "anim_props6.py"):
    exec(open(f"{TPL_}/{_p}").read())
out, names, costs = [], [], []; T0 = [time.time()]
def start(): T0[0] = time.time()
def fin(f, n, name): costs.append(time.time() - T0[0]); out.append(cine_grade(f, n)); names.append(name)
HERO96 = {"base": "hero", "top": (60, 110, 170)}
INV = [{"base": "exec", "tie": (0, 170, 90)}, {"base": "girl", "shirt": (255, 200, 0), "hair": (200, 60, 40)}, {"base": "oldman"}, {"base": "girl2", "shirt": (120, 90, 220)}, {"base": "creator"}]
LAW = {"base": "exec", "tie": (150, 152, 160)}
# i1 frame 1
start(); f = set_view("schoolyard", 1.0)
comp(f, jumpjet_el(820, nozzle=95), 560, 760)
for i, (x, y) in enumerate(((190, 1040), (360, 1130), (760, 1060), (880, 1180), (560, 1090))): rot_comp(f, bottlecap_el("COLA"), x, y, i * 37, scale=0.26)
person(f, 300, 1840, 1.0, HERO96, la=(14, 8), ra=(150, 170), expr="wow", look=(1, -1))
series_badge(f, "YOUR MOVE", "EP 1 · THE PEPSI JET")
say(f, "A JET FOR POINTS?", y=1250, size=110)
fin(f, 1, "i1 frame 1")
# i2 bedroom + cold open
start(); f = set_view("bedroom90s", 0.5, zoom=1.05)
person(f, 420, 1830, 1.0, HERO96, la=(30, 60), ra=(40, 80), expr="smirk", look=(1, 0))
comp(f, crt_tv_el(420, screen=jumpjet_el(500, nozzle=95)), 800, 1010)
cold_open(f, "1996", "NEAR SEATTLE", "YOU: STUDENT, 21")
fin(f, 2, "i2 bedroom")
# a1 prizes pop out of the TV
start(); f = set_view("bedroom90s", 0.8, zoom=1.2, blur=3)
comp(f, crt_tv_el(620), 540, 1140)
comp(f, tee_el(230), 220, 760); comp(f, jacket_el(240), 540, 660); comp(f, glasses_el(260, style="round"), 860, 780)
fin(f, 3, "a1 prizes")
# a4 padlocks roadmap
start(); f = set_view("bedroom90s", 1.1)
for i in range(3): comp(f, padlock_el(190, i + 1), 240 + i * 300, 640)
person(f, 540, 1840, 1.05, HERO96, la=(10, 10), ra=(60, 30), brow="sus", look=(0, -1))
say(f, "3 PROBLEMS", y=900, size=120)
fin(f, 4, "a4 locks")
# b1 can pile
start(); f = set_view("bedroom90s", 1.4)
person(f, 540, 1500, 1.0, HERO96, la=(150, 170), ra=(150, 170), expr="sweat", sweat=True)
can_pile(f, 540, 1860, w=900, rows=5)
comp(f, padlock_el(170, 1, open_=True), 880, 560)
say(f, "PROBLEM 1", y=700, size=120)
fin(f, 5, "b1 cans")
# b4 calculator CU
start(); f = set_view("bedroom90s", 1.7, zoom=1.7, cx=540, cy=820, blur=7)
person_head_at(f, 400, 1020, 1.6, HERO96, expr="smirk", brow="up", mouth=0)
comp(f, calculator_el(300, "700,000"), 800, 1140)
say(f, "$700,000", y=560, size=170)
fin(f, 6, "b4 calculator")
# b5 split bag vs jet
start(); f = set_view("schoolyard", 2.0, blur=2)
comp(f, moneybag_el(250, "$700K"), 240, 1200); comp(f, jumpjet_el(620, nozzle=95), 680, 960)
say(f, "×30+", y=620, size=170)
fin(f, 7, "b5 split")
# b6 Oops
start(); f = set_view("bedroom90s", 1.9, zoom=1.7, cx=540, cy=820, blur=7)
person_head_at(f, 540, 1040, 1.7, HERO96, expr="smirk", brow="up", mouth=2)
oops_beat(f, 1.0, 0.0, x=540, y=520)
fin(f, 8, "b6 oops")
# c2 investors
start(); f = set_view("office", 0.3, zoom=1.05)
for i, (x, y) in enumerate(((150, 1620), (340, 1660), (540, 1600), (740, 1660), (930, 1620))):
    person(f, x, y, 0.72, INV[i], brow="up", look=(-1 if x > 540 else 1, 0))
person(f, 540, 1860, 1.0, HERO96, la=(14, 8), ra=(100, 140), mouth=2, brow="up")
say(f, "5 INVESTORS", y=800, size=130)
for i in range(5): comp(f, moneybag_el(110, "$"), 240 + i * 150, 1000)
fin(f, 9, "c2 investors")
# t1 quote
start(); f = set_view("street", 2.0, zoom=1.3, cx=540, cy=1000, blur=5)
person_head_at(f, 540, 1200, 1.7, HERO96, expr="sad", brow="sad", sweat=True)
quote_card(f, "fanciful… simply included to create a humorous and entertaining ad", "PepsiCo's letter, 1996 · via Seattle Times", y=520)
fin(f, 10, "t1 quote")
# t3 lawyers
start(); f = set_view("courtroom", 0.0)
for x in (360, 540, 720): person(f, x, 1500, 0.8, LAW, brow="sus", look=(0, 1))
person(f, 200, 1840, 1.1, HERO96, la=(10, 10), ra=(150, 170), expr="sweat", sweat=True, look=(1, -1))
say(f, "COURT PAPERS", y=620, size=120)
fin(f, 11, "t3 lawyers")
# e1 end card
start(); f = set_view("schoolyard", 3.0, zoom=1.05, cx=540, cy=1000, blur=3)
comp(f, jumpjet_el(420, nozzle=95), 300, 860); rot_comp(f, coupon_el("FREE COLA", 260), 850, 900, 10)
person(f, 540, 1340, 0.95, HERO96, la=(30, 40), ra=(30, 40), mouth=1, brow="up")
choice_card(f, "YOUR MOVE", "FIGHT", "FOLD", y=1410)
series_badge(f, "PART 2", "TOMORROW")
fin(f, 12, "e1 end card")
import numpy as np, cv2
def guides(img):
    g = img.copy(); H_, W_ = g.shape[:2]
    for (x0, y0, x1, y1) in ((0, 0, W_, 250), (0, H_ - 420, W_, H_), (W_ - 120, 0, W_, H_), (0, 0, 60, H_)):
        sub = g[y0:y1, x0:x1].astype(np.float32); g[y0:y1, x0:x1] = (sub * 0.6 + np.array([0, 0, 255]) * 0.4).astype(np.uint8)
    return g
tiles = []
for img in out:
    a = (np.clip(img, 0, 1) * 255).astype(np.uint8)[..., ::-1] if img.dtype != np.uint8 else img[..., ::-1]
    tiles.append(cv2.resize(guides(a), (360, 640)))
rows = [np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]
cv2.imwrite(f"{OUT}/storyboard_pepsi_lineart.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 82])
print("frames", names, "s/frame", [round(c, 2) for c in costs])
