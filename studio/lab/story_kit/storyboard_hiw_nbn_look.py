# HOW IT WORKS kit demo (R&D run, 4 Nov 2026): storyboard frames for EP 1 (Spotify) and EP 2 (credit score), props kit 8 + clean sets. Usage: python3 storyboard_hiw_ep1_ep2.py <out_dir>
import os, sys, json
TPL_ = "/home/claude/nextbignow-videos/studio/template/scripts"
OUT = sys.argv[1]; os.makedirs(f"{OUT}/work", exist_ok=True)
if not os.path.exists(f"{OUT}/work/align.json"):
    json.dump(dict(lines={"i1": dict(start=0.0, end=3.0)}, words=[dict(line="i1", w="before", t=0.3)], dur=4.0, LEAD=0.0, fake=True), open(f"{OUT}/work/align.json", "w"))
if not os.path.exists(f"{OUT}/work/vo.wav"):
    import numpy as _np, soundfile as _sf; _sf.write(f"{OUT}/work/vo.wav", 0.02 * _np.sin(_np.arange(48000 * 4) * 0.05).astype(_np.float32), 48000)
os.environ["PROJ"] = OUT
for _p in ("anim_base.py", "anim_cine.py", "anim_mascot3d.py", "anim_stick.py", "anim_sets.py", "anim_props.py", "anim_props2.py", "anim_props3.py", "anim_story.py", "anim_story2.py", "anim_props4.py", "anim_props5.py", "anim_props6.py", "anim_props7.py", "anim_props8.py", "anim_clean.py", "anim_nbn.py"):
    exec(open(f"{TPL_}/{_p}").read())
out, names = [], []
def fin(f, name): out.append(finish(f, len(out))); names.append(name)
LENDER = {"base": "lady", "shirt": (40, 60, 130)}
S1 = "EP 1 · 999 PLAYS"; S2 = "EP 2 · YOUR SCORE"

# ---- EP 1 ----
f = set_view("gatehall", 0.0); comp(f, gate_el(780, "999", False), 560, 1090)
comp(f, mic_el(110), 170, 1500); person(f, 300, 1840, 1.0, "hero", la=(20, 40), ra=(60, 30), expr="sweat", sweat=True, look=(1, -1))
mini_card(f, "HOW IT WORKS", "YOUR SONG"); series_badge(f, "HOW IT WORKS", S1); say(f, "999 PLAYS", y=560, size=130); fin(f, "i1 frame 1")
f = stage("blue") if False else set_view("gatehall", 0.3); comp(f, pot_el(760, 0.62), 540, 1190); coin_rain(f, 0.6, 0.0, 540, 800, n=8)
mini_card(f, "GATE 1 OF 4", "THE POT"); say(f, "SUBSCRIPTIONS + ADS", y=560, size=100); fin(f, "a2 pot")
f = set_view("recording", 0.4); plays_grid(f, 540, 1000, 100, 5, w=720)
comp(f, tag_el("YOU: $5"), 540, 1500); say(f, "5 OF 100", y=560, size=130); comp(f, chip("MADE-UP NUMBERS · $100 POT", (20, 20, 26), WHITE, 26), 540, 700); fin(f, "b4 slice")
f = set_view("recording", 0.5); plays_grid(f, 540, 1000, 200, 5, w=720)
comp(f, tag_el("YOU: $2.50"), 540, 1500); say(f, "HALF", y=560, size=150); comp(f, chip("MADE-UP NUMBERS · SAME $100 · NOT ONE FAN LOST", (20, 20, 26), WHITE, 26), 540, 700); fin(f, "b6 half")
f = set_view("gatehall", 0.6); comp(f, gate_el(780, "1,000", True), 560, 1090); person(f, 240, 1840, 1.0, "hero", la=(120, 40), ra=(60, 30), expr="wow", look=(1, -1))
mini_card(f, "GATE 3 OF 4", "THE LINE"); say(f, "1,000 A YEAR", y=560, size=120); comp(f, chip("SINCE APRIL 2024 · RECORDING ROYALTIES", (20, 20, 26), WHITE, 26), 540, 700); fin(f, "c2 open")
f = set_view("gatehall", 0.7); comp(f, booth_el(640, "LABEL OR DISTRIBUTOR"), 640, 1120); coin_rain(f, 0.8, 0.0, 860, 760, n=6)
person(f, 220, 1840, 1.0, "hero", la=(100, 80), ra=(30, 20), expr="sweat", sweat=True, look=(1, -1)); mini_card(f, "GATE 4 OF 4", "THE MIDDLEMAN"); say(f, "NOT TO YOU", y=560, size=130); fin(f, "d2 middleman")
f = set_view("subscriber", 0.8); comp(f, sign_el("ONE BAND"), 780, 1120); comp(f, phone_el(), 300, 1240, scale=0.6)
person(f, 340, 1840, 1.0, "hero", la=(60, 80), ra=(30, 20), expr="smirk"); mini_card(f, "SWITCH SEATS", "SUBSCRIBER"); say(f, "IT GOES IN THE POT", y=560, size=110); comp(f, pot_el(320, 0.7), 800, 1540); fin(f, "e2 subscriber")
f = set_view("gatehall", 0.9); comp(f, pot_el(300, 0.8), 190, 880); comp(f, gate_el(420, "999", False), 830, 880)
person(f, 300, 1840, 1.0, "hero", la=(120, 90), ra=(30, 20), expr="smirk"); person(f, 780, 1840, 0.95, {"base": "girl", "shirt": (0, 150, 140)}, la=(120, 150), ra=(20, 20))
say(f, "SAVE THIS", y=560, size=130); choice_card(f, "ONLY THE ARTISTS YOU PLAY?", "YES", "NO", y=1120); series_badge(f, "HOW IT WORKS", S1); fin(f, "z1 end")
# ---- EP 2 ----
PIE = (10, 10, 15, 35, 30)
f = set_view("carlot", 0.0); comp(f, car_el(800), 560, 1250); comp(f, gauge_el(520, 0.42), 560, 880); comp(f, form_el(220, "SALARY"), 880, 1560)
person(f, 300, 1840, 1.0, "hero", la=(120, 60), ra=(20, 20), expr="sus")
mini_card(f, "HOW IT WORKS", "YOUR SCORE"); series_badge(f, "HOW IT WORKS", S2); say(f, "IT DOESN'T KNOW", y=560, size=110); fin(f, "i1 frame 1")
f = set_view("lenderdesk", 0.3); [(comp(f, tag_el(t), 420, y), comp(f, stamp_el("NOT IN IT", size=44), 780, y)) for t, y in (("PAY", 820), ("JOB", 960), ("AGE", 1100))]
person(f, 300, 1840, 1.0, "hero", expr="wow"); person(f, 800, 1840, 0.95, LENDER); say(f, "NOT IN YOUR SCORE", y=560, size=110); comp(f, chip("myFICO, OCT 2026", (20, 20, 26), WHITE, 26), 540, 680); fin(f, "i3 stamp")
f = set_view("gatehall", 0.5); score_pie(f, 540, 1120, 340, PIE, k=(1, 0, 0, 0, 0)); mini_card(f, "SLICE 1", "NEW CREDIT"); say(f, "10%", y=560, size=150); fin(f, "a1 first slice")
f = set_view("gatehall", 0.6); score_pie(f, 540, 1120, 340, PIE, k=(1, 1, 1, 0, 0)); say(f, "WHERE'S THE REST?", y=560, size=110); fin(f, "c3 rest")
f = set_view("gatehall", 0.7); score_pie(f, 540, 1120, 340, PIE, k=(1, 1, 1, 1, 0), hl=3); mini_card(f, "SLICE 4", "ON TIME"); say(f, "35%: THE BIGGEST", y=560, size=110); fin(f, "d1 biggest")
f = set_view("homedesk", 0.6); comp(f, cycle_el(900, 3), 540, 1080); comp(f, tag_el("LOOKS USED"), 560, 880); person(f, 300, 1840, 1.0, "hero", expr="sweat", sweat=True)
mini_card(f, "SLICE 5", "HOW MUCH YOU OWE"); say(f, "USED, EVEN IF PAID", y=560, size=110); comp(f, chip("EVEN WHEN YOU PAY IN FULL · Experian", (20, 20, 26), WHITE, 26), 540, 700); fin(f, "e4 cycle")
f = set_view("homedesk", 0.8); comp(f, report_el(500, True), 640, 1140); person(f, 240, 1840, 1.0, "hero", expr="sus", look=(1, -1)); say(f, "1 IN 5", y=560, size=150); comp(f, chip("AN ERROR ON AT LEAST ONE REPORT · FTC 2013", (20, 20, 26), WHITE, 26), 540, 700); fin(f, "f2 error")
f = set_view("carlot", 0.9); score_pie(f, 860, 880, 150, PIE, labels=[""] * 5); comp(f, car_el(520), 330, 880)
person(f, 240, 1840, 1.0, "hero", la=(120, 90), ra=(20, 20), expr="smirk"); say(f, "SAVE THIS", y=560, size=130); choice_card(f, "SHOULD YOUR SALARY COUNT?", "YES", "NO", y=1120); series_badge(f, "HOW IT WORKS", S2); fin(f, "z1 end")

from PIL import Image as _I, ImageDraw as _D
cols = 6; tw, th = 360, 640; rows = (len(out) + cols - 1) // cols; sh = _I.new("RGB", (cols * tw, rows * th), (16, 16, 20))
for i, (a, n) in enumerate(zip(out, names)):
    im = _I.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)[..., ::-1] if False else (np.clip(a, 0, 1) * 255).astype(np.uint8)).resize((tw - 6, th - 6)); sh.paste(im, ((i % cols) * tw + 3, (i // cols) * th + 3))
    _D.Draw(sh).text(((i % cols) * tw + 10, (i // cols) * th + 8), n, fill=(255, 255, 0))
sh.save(f"{OUT}/sheet.jpg", quality=86)
print("frames", len(out), f"{OUT}/sheet.jpg")
