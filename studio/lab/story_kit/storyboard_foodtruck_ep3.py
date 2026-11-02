# Food-truck kit demo (R&D run, 2 Nov 2026): renders storyboard frames of HOW TO START EP 3 (episodes/queue/06-food-truck-nyc)
# + the 1950 variant for the nickel-Coke board, each also with the PLAYBOOK §6 safe-zone guides. Usage: python3 storyboard_vending_ep2.py <out_dir>
import os, sys, json, time
TPL_ = "/home/claude/nextbignow-videos/studio/template/scripts"
OUT = sys.argv[1]; os.makedirs(f"{OUT}/work", exist_ok=True)
if not os.path.exists(f"{OUT}/work/align.json"):
    json.dump(dict(lines={"i1": dict(start=0.0, end=3.0)}, words=[dict(line="i1", w="before", t=0.3)], dur=4.0, LEAD=0.0, fake=True), open(f"{OUT}/work/align.json", "w"))
if not os.path.exists(f"{OUT}/work/vo.wav"):
    import numpy as _np, soundfile as _sf; _sf.write(f"{OUT}/work/vo.wav", 0.02 * _np.sin(_np.arange(48000 * 4) * 0.05).astype(_np.float32), 48000)
os.environ["PROJ"] = OUT
for _p in ("anim_base.py", "anim_cine.py", "anim_mascot3d.py", "anim_stick.py", "anim_sets.py", "anim_props.py", "anim_props2.py", "anim_props3.py", "anim_story.py", "anim_story2.py", "anim_props4.py", "anim_props5.py"):
    exec(open(f"{TPL_}/{_p}").read())
out, names, costs = [], [], []
T0 = [time.time()]
def start(): T0[0] = time.time()
def fin(f, n, name): costs.append(time.time() - T0[0]); out.append(cine_grade(f, n)); names.append(name)
SELLER = {"base": "exec", "col": (150, 152, 160)}

# i1 — frame 1
start(); f = set_view("store", 0.0)
comp(f, vending_el(640), 540, 1300)
person(f, 300, 1840, 1.0, "hero", la=(20, 10), ra=(60, 30), expr="sus", brow="sus", look=(1, -1))
HOLDER = {"base": "exec", "tie": (150, 152, 160)}
MENTOR = {"base": "girl", "shirt": (0, 150, 140), "hair": (40, 30, 30)}
HERO_CAP = {"base": "hero", "cap": (255, 255, 255)}

# i1 — frame 1
start(); f = set_view("street", 0.0)
comp(f, foodtruck_el(860, open_=False, permit=False), 520, 1420)
comp(f, tag_el("$$$$$"), 760, 760)
comp(f, permit_el(300), 800, 1060)
person(f, 260, 1840, 1.0, "hero", la=(20, 10), ra=(60, 30), expr="sus", brow="sus", look=(1, -1))
person(f, 820, 1840, 0.95, HOLDER, la=(30, 60), ra=(120, 150))
cold_open(f, "2026", "NEW YORK CITY", "YOU: FIRST-TIME OWNER")
say(f, "$200 PERMIT", y=560, size=130); say(f, "RENTED FOR $$$$$?", y=680, size=110)
fin(f, 1, "i1 frame 1")
# b1 — commissary
start(); f = set_view("commissary", 0.3)
comp(f, foodtruck_el(620, open_=True, menu="TACOS"), 560, 1390)
person(f, 230, 1840, 1.0, MENTOR, la=(30, 70), ra=(120, 40), mouth=2)
person(f, 880, 1840, 0.95, HERO_CAP, la=(20, 40), ra=(40, 80), expr="wow")
cold_open(f, "STEP 2", "FIND A BASE", "THE COMMISSARY")
fin(f, 2, "b1 commissary")
# e1 — permit CU
start(); f = set_view("office", 0.5, zoom=1.1)
comp(f, permit_el(700), 540, 1000)
person(f, 300, 1840, 1.0, "hero", la=(20, 40), ra=(40, 80), brow="up")
cold_open(f, "STEP 4", "THE TRUCK PERMIT", "THE HARD ONE")
fin(f, 3, "e1 permit")
# e3 — the line of trucks
start(); f = set_view("street", 0.7)
for i in range(5): comp(f, foodtruck_el(300, open_=False, permit=False, col=[(255, 196, 40), (80, 170, 240), (240, 110, 90), (120, 200, 110), (200, 140, 230)][i]), 140 + i * 220, 1240 + i * 20)
comp(f, calendar_el("LIST", "2022"), 820, 620)
person(f, 300, 1840, 1.0, "hero", la=(20, 40), ra=(40, 80), expr="sweat", sweat=True)
say(f, "2022 LISTS FIRST", y=900)
fin(f, 4, "e3 truck line")
# t2 — work a truck first
start(); f = set_view("street", 0.2)
comp(f, foodtruck_el(860, open_=True, menu="TACOS", permit=True), 540, 1320)
person(f, 300, 1840, 1.0, HERO_CAP, la=(20, 40), ra=(40, 80), expr="smirk")
person(f, 800, 1840, 0.95, MENTOR, la=(30, 70), ra=(120, 40), mouth=2)
hud_rule(f, 4, "NO SPOT? WORK ONE FIRST")
fin(f, 5, "t2 work a truck")
# z1 — end card
start(); f = set_view("street", 0.0)
comp(f, foodtruck_el(640, open_=True, menu="TACOS"), 540, 1060)
choice_card(f, "STILL NYC?", "STAY", "MOVE")
fin(f, 6, "z1 end card")
import numpy as np, cv2
def guides(img):
    g = img.copy(); H_, W_ = g.shape[:2]
    for (x0, y0, x1, y1) in ((0, 0, W_, 220), (0, H_ - 420, W_, H_), (W_ - 140, 0, W_, H_)):
        sub = g[y0:y1, x0:x1].astype(np.float32); g[y0:y1, x0:x1] = (sub * 0.6 + np.array([0, 0, 255]) * 0.4).astype(np.uint8)
    return g
tiles = []
for img in out:
    a = (np.clip(img, 0, 1) * 255).astype(np.uint8)[..., ::-1] if img.dtype != np.uint8 else img[..., ::-1]
    tiles.append(np.hstack([cv2.resize(a, (360, 640)), cv2.resize(guides(a), (360, 640))]))
sheet = np.vstack([np.hstack(tiles[i:i + 2]) if i + 1 < len(tiles) else np.hstack([tiles[i], np.zeros_like(tiles[i])]) for i in range(0, len(tiles), 2)])
cv2.imwrite(f"{OUT}/storyboard_foodtruck_ep3.jpg", sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
print("frames", names, "s/frame", [round(c, 2) for c in costs])
