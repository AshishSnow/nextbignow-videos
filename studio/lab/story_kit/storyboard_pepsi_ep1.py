# Story-kit demo (31 Oct 2026): renders 7 storyboard frames of YOUR MOVE EP 1 with the template scripts.
# Usage: cd <any project>/scripts && python3 storyboard_pepsi_ep1.py <out_dir>   (needs PROJ with work/align.json — any built project)
import os, sys, math
TPL_ = "/home/claude/nextbignow-videos/studio/template/scripts"
os.environ["PROJ"] = "/home/claude/studio/projects/texlab"
for _p in ("anim_base.py", "anim_cine.py", "anim_mascot3d.py", "anim_sets.py", "anim_props.py", "anim_props2.py", "anim_props3.py", "anim_story.py"):
    exec(open(f"{TPL_}/{_p}").read())
OUT = sys.argv[1]; out = []
def fin(f, n): return cine_grade(f, n)
# 1 cold open: jet over the school yard at dusk
f = set_view("schoolyard", 1.0)
jet = jumpjet_el(820, nozzle=95)

comp(f, jet, 560, 760)
embers(f, 1.0, n=30, col=(255, 210, 160), y0=900, y1=1500, size=3)
person(f, 300, 1700, 0.95, "hero", la=(14, 8), ra=(150, 170), expr="wow", look=(1, -1))
cold_open(f, "1996", "NEAR SEATTLE", "YOU: STUDENT, 21")
series_badge(f, "YOUR MOVE", "EP 1 · THE PEPSI JET")
out.append(fin(f, 1))
# 2 bedroom, the ad on the CRT, rule #1
f = set_view("bedroom90s", 0.5, zoom=1.1, cx=540, cy=1100)
tv = crt_tv_el(500, screen=jumpjet_el(600, nozzle=95))
comp(f, tv, 820, 760)
person(f, 300, 1260, 1.15, "hero", sit=True, la=(30, 60), ra=(40, 80), expr="wow", look=(1, 0))
hud_rule(f, 1, "7,000,000 POINTS = 1 JET", y=430)
out.append(fin(f, 2))
# 3 close-up: the maths + the Oops beat
f = set_view("bedroom90s", 0.5, zoom=1.7, cx=540, cy=820, blur=7)
person_head_at(f, 540, 860, 2.6, "hero", expr="smirk", brow="up", mouth=0, ra=(30, 50))
say(f, "$700,000", y=1380, size=190)
oops_beat(f, 1.0, 0.0, x=540, y=520)
out.append(fin(f, 3))
# 4 the pitch: five investors
f = set_view("office", 0.3, zoom=1.12, cx=540, cy=1150, blur=2.5)
for i, (who, x) in enumerate((("exec", 170), ("lady", 380), ("oldman", 700), ("creator", 900))):
    person(f, x, 1560 + (i % 2) * 40, 0.85, who, brow="up" if i % 2 else "n", look=(-1 if x > 540 else 1, 0))
person(f, 540, 1820, 1.3, "hero", la=(14, 8), ra=(100, 140), mouth=2, brow="up")
say(f, "5 INVESTORS", y=1010, size=130)
out.append(fin(f, 4))
# 5 the reply: quote card + coupons
f = set_view("street", 2.0, zoom=1.3, cx=540, cy=1000, blur=5)
person_head_at(f, 540, 1140, 2.2, "hero", expr="sad", brow="sad", sweat=True)
quote_card(f, "fanciful… simply included to create a humorous and entertaining ad", "PepsiCo's letter, 1996 · via Seattle Times", y=520)
for i, (x, y, r) in enumerate(((240, 1300, -14), (820, 1420, 12), (520, 1560, -4))):
    rot_comp(f, coupon_el("FREE COLA", 300), x, y, r)
out.append(fin(f, 5))
# 6 end card: your move
f = set_view("schoolyard", 3.0, zoom=1.05, cx=540, cy=1000, blur=3)
comp(f, jumpjet_el(520, nozzle=95), 230, 860)
rot_comp(f, coupon_el("FREE COLA", 260), 850, 900, 10)
person(f, 540, 1660, 1.0, "hero", la=(30, 40), ra=(30, 40), mouth=1, brow="up", look=(0, 0))
choice_card(f, "YOUR MOVE", "FIGHT", "FOLD", y=1410)
series_badge(f, "PART 2", "TOMORROW")
out.append(fin(f, 6))
# 7 part 2: the courtroom
f = set_view("courtroom", 0.0, zoom=1.0)
person(f, 540, 930, 1.1, {"base": "lady", "top": (28, 26, 32), "outfit": "coat"}, brow="up", look=(0, 1), shadow=False)
set_front(f, "courtroom", (176, 606, 904, 1004))
person(f, 250, 1720, 1.15, "hero", back=True, shadow=False)
person(f, 830, 1640, 1.0, "exec", brow="sus", expr="smirk", look=(-1, 0))
quote_card(f, "exaggerated adolescent fantasy", "Leonard v. PepsiCo (S.D.N.Y. 1999)", y=1300)
cold_open(f, "AUG 1999", "NEW YORK", "THE RULING")
out.append(fin(f, 7))
ims = [cv2.resize((np.clip(x, 0, 1) * 255).astype(np.uint8), (432, 768), interpolation=cv2.INTER_AREA) for x in out]
gap = np.full((768, 10, 3), 255, np.uint8)
row = [ims[0]]
for im in ims[1:]: row += [gap, im]
cv2.imwrite(f"{OUT}/storyboard_pilot.jpg", cv2.cvtColor(np.hstack(row), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
for i, x in enumerate(out): cv2.imwrite(f"{OUT}/sb_{i+1}.jpg", cv2.cvtColor((np.clip(x, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("ok")
