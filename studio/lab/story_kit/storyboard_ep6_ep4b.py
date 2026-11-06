# Lab sheet, 6 Nov 2026 (R&D): HOW TO START EP 6 home bakery + HOW IT WORKS EP 4 hotel fees. Rows from shots.md, safe-zone guides on.
import os, sys
_LAB = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(_LAB, "..", "..", "template", "scripts"))
from nbnkit import *
import skia
from PIL import Image
S2 = lambda c, small, big, col=WHITE, size=240: two_tier(c, 9, 0, small, big, y=650, big_size=size, big_col=col, small_col=(240, 232, 255), shadow=True, maxw=800)
F = lambda c, s: src_chip(c, s, 1.0, y=1466)
P = lambda c, s="OOPSMYBUSINESS · HOW TO START": pill(c, s, y=288)
t = 9.0
WARM = ((90, 40, 30), (190, 100, 50)); VIO = ((44, 28, 110), (110, 60, 170)); NAVY = ((16, 28, 80), (40, 70, 150)); TEA = ((10, 70, 80), (30, 140, 130)); PLUM = ((70, 26, 60), (170, 70, 110))
def bk_i1(c):
    home_kitchen(c, t); oven(c, 760, FLOOR, 340); cookie_tray(c, 760, 1160, 300, 3, 2); price_tag(c, 760, 1040, "$?", tilt=6)
    hero(c, 290, FLOOR, 1.1, POSES["hold"], Face("wide", "o", look=(1, -1)), t, prop=None); top_shade(c, 0.5); P(c); S2(c, "home-baked cookies used to risk", "JAIL", RED_C)
def bk_i3(c):
    diagram_bg(c, *NAVY, disc=(120, 170, 255), cx=540, cy=1060, r=390); muffin(c, 540, 1240, 300); cell_bars(c, 330, 860, 750, 1270); price_tag(c, 790, 1110, "$1,000", tilt=6, size=54)
    top_shade(c, 0.4); P(c); S2(c, "one muffin, up to", "$1,000", YEL); F(c, "WISCONSIN, UNTIL A 2017 COURT RULING · AP VIA NBC")
def bk_i4(c):
    home_kitchen(c, t); line_meter(c, 540, 980, 760, 0.0, "LEGAL LIMIT", need="$150K"); cookie_tray(c, 760, 1240, 280, 3, 2); girl(c, 280, FLOOR, 1.1, POSES["point"], Face("open", "grin", look=(1, -1)), t)
    top_shade(c, 0.5); P(c); S2(c, "texas legal limit, a year", "$150,000", GRN, 220); F(c, "A LEGAL CAP, NOT AN INCOME · TEXAS DSHS")
def bk_a3(c):
    home_kitchen(c, t); cookie_tray(c, 300, 1100, 300, 3, 2); muffin(c, 300, 1330, 140)
    for i, s in enumerate(("MEAT", "SEAFOOD", "ICE CREAM")): label_card(c, 700, 900 + i * 170, s, 56); stamp(c, 950, 900 + i * 170, "NO", RED_C, size=60, tilt=-8)
    top_shade(c, 0.5); P(c, "OOPSMYBUSINESS · HOW TO START · STEP 1 OF 4"); S2(c, "in texas", "ALMOST ANYTHING", YEL, 170); F(c, "FULL LIST + FRIDGE FOODS: TEXAS DSHS")
def bk_a5(c):
    diagram_bg(c, *TEA, disc=(255, 220, 130), cx=540, cy=1060, r=390); calendar(c, 330, 1120, 1.3, "DAYS", "28"); label_card(c, 760, 1040, "FREE", 90); stamp(c, 760, 1240, "CAN'T REFUSE", GRN, size=54)
    top_shade(c, 0.4); P(c, "OOPSMYBUSINESS · HOW TO START · STEP 1 OF 4"); S2(c, "england, before you start", "28 DAYS", WHITE); F(c, "ALSO WALES + N. IRELAND · FOOD STANDARDS AGENCY")
def bk_c3(c):
    diagram_bg(c, *PLUM, disc=(255, 200, 120), cx=540, cy=1060, r=390); receipt(c, 540, 1110, 620, [("SOLD", "$18"), ("INGREDIENTS", "-$9"), ("2 HOURS", "$9 LEFT")], total=("PER HOUR", "$4.50"))
    top_shade(c, 0.4); P(c, "OOPSMYBUSINESS · HOW TO START · STEP 3 OF 4"); S2(c, "you just paid yourself", "$4.50", RED_C); F(c, "MADE-UP NUMBERS")
def bk_c4(c):
    diagram_bg(c, *WARM, disc=(255, 200, 110), cx=540, cy=1050, r=400); cookie_grid(c, 540, 1060, 80, 10, 760)
    top_shade(c, 0.4); P(c, "OOPSMYBUSINESS · HOW TO START · STEP 3 OF 4"); S2(c, "dozen, every week", "80", YEL); F(c, "$150,000 ÷ $36 ÷ 52 · OUR MATHS, MADE-UP PRICE")
def bk_d4(c):
    home_kitchen(c, t, lamp_a=0.3); cake_box(c, 540, FLOOR - 10, 740, ["THIS PRODUCT WAS PRODUCED IN A", "PRIVATE RESIDENCE THAT IS NOT", "SUBJECT TO GOVERNMENTAL", "LICENSING OR INSPECTION."], size=46, title=None)
    top_shade(c, 0.5); P(c, "OOPSMYBUSINESS · HOW TO START · STEP 4 OF 4"); S2(c, "word for word, in texas", "THE LABEL", YEL); F(c, "TEXAS DSHS")
def bk_z1(c):
    home_kitchen(c, t); cake_box(c, 540, 1180, 300); 
    hero(c, 240, FLOOR, 1.0, POSES["shrug"], Face("open", "smile"), t); girl(c, 840, FLOOR, 1.0, POSES["point"], Face("open", "grin", look=(-1, -1)), t)
    label_card(c, 330, 1290, "YES", 64, col=GRN); label_card(c, 750, 1290, "NO", 64, col=RED_C)
    top_shade(c, 0.5); P(c); S2(c, "a kitchen nobody inspects", "WOULD YOU?", WHITE, 220)
EP6 = [bk_i1, bk_i3, bk_i4, bk_a3, bk_a5, bk_c3, bk_c4, bk_d4, bk_z1]
Ph = lambda c, s="OOPSMYBUSINESS · HOW IT WORKS": pill(c, s, y=288)
def ho_i1(c):
    hotel_lobby(c, t); elevator(c, 700, FLOOR, 400, "$199"); room_key(c, 330, 1150, 200)
    hero(c, 280, FLOOR, 1.1, POSES["hold"], Face("wide", "o", look=(1, -1)), t); top_shade(c, 0.5); Ph(c); S2(c, "a night, the room says $199", "YOU PAY $238", RED_C, 210); F(c, "THE FTC'S OWN MADE-UP EXAMPLE, BEFORE TAX")
def ho_i4(c):
    hotel_lobby(c, t); elevator(c, 540, FLOOR, 400, "$199", floor_=0); hero(c, 170, FLOOR, 1.0, POSES["point"], Face("open", "smile", look=(1, -1)), t)
    top_shade(c, 0.5); Ph(c); S2(c, "the fee rides up", "4 FLOORS", YEL)
def ho_a2(c):
    diagram_bg(c, *NAVY, disc=(120, 170, 255), cx=540, cy=1060, r=400); hotel_card(c, 540, 900, 760, "$199", "HOTEL A", note="+ fee, later", hl=False); hotel_card(c, 540, 1160, 760, "$229", "HOTEL B", note="no fee", hl=False)
    top_shade(c, 0.4); Ph(c, "OOPSMYBUSINESS · HOW IT WORKS · FLOOR 1 OF 4"); S2(c, "before the rule, shown without", "THE FEE", YEL, 240); F(c, "MADE-UP HOTELS · FTC ECONOMIC PAPER, 2017")
def ho_a3(c):
    diagram_bg(c, *NAVY, disc=(120, 170, 255), cx=540, cy=1060, r=400); hotel_card(c, 540, 900, 760, "$238", "HOTEL A", note="total", hl=True); hotel_card(c, 540, 1160, 760, "$229", "HOTEL B", note="total")
    top_shade(c, 0.4); Ph(c, "OOPSMYBUSINESS · HOW IT WORKS · FLOOR 1 OF 4"); S2(c, "looked cheaper", "WASN'T", RED_C, 240); F(c, "MADE-UP HOTELS")
def ho_b2(c):
    diagram_bg(c, *TEA, disc=(255, 220, 130), cx=540, cy=1060, r=390); split_bar(c, 540, 960, 800, 0.84, "ROOM", "SITE'S CUT", rc=(235, 70, 60)); label_card(c, 540, 1200, "RESORT FEE", 66); stamp(c, 540, 1320, "OFTEN NO CUT", GRN, size=52)
    top_shade(c, 0.4); Ph(c, "OOPSMYBUSINESS · HOW IT WORKS · FLOOR 2 OF 4"); S2(c, "booking sites take", "A CUT", WHITE); F(c, "ILLUSTRATION, CUT SIZE VARIES · SOME SITES NOW CHARGE IT")
def ho_c3(c):
    diagram_bg(c, *VIO, disc=(255, 210, 120), cx=540, cy=1060, r=390); ticket(c, 300, 1000, 330, tilt=-6, label="ALL IN"); ticket(c, 780, 1000, 330, tilt=6, label="+ FEES"); 
    extra(c, 300, FLOOR, 0.9, POSES["stand"], Face("open", "smile"), t); girl(c, 780, FLOOR, 0.9, POSES["stand"], Face("wide", "o"), t)
    top_shade(c, 0.4); Ph(c, "OOPSMYBUSINESS · HOW IT WORKS · FLOOR 3 OF 4"); S2(c, "half saw fees only at", "CHECKOUT", YEL, 230); F(c, "STUBHUB EXPERIMENT, 2015 · BERKELEY HAAS")
def ho_c4(c):
    diagram_bg(c, *VIO, disc=(255, 210, 120), cx=540, cy=1060, r=390); ticket(c, 540, 1060, 480, tilt=-4, label="+ FEES")
    top_shade(c, 0.4); Ph(c, "OOPSMYBUSINESS · HOW IT WORKS · FLOOR 3 OF 4"); S2(c, "the checkout group spent", "21% MORE", RED_C, 220); F(c, "AND 14% MORE LIKELY TO BUY · TICKETS, NOT HOTELS")
def ho_d2(c):
    hotel_lobby(c, t); elevator(c, 540, FLOOR, 400, "$238", floor_=4, open_=0.3); calendar(c, 180, 1100, 1.0, "MAY", "2025"); top_shade(c, 0.5); Ph(c, "OOPSMYBUSINESS · HOW IT WORKS · FLOOR 4 OF 4"); S2(c, "up front, fee inside", "THE TOTAL", GRN); F(c, "US FEDERAL RULE, FTC · HOTELS + TICKETS")
def ho_d5(c):
    hotel_lobby(c, t); front_desk(c, 540, FLOOR, 760); extra(c, 760, FLOOR - 120, 0.9, POSES["stand"], Face("open", "flat"), t); hero(c, 230, FLOOR, 1.1, POSES["hold"], Face("wide", "o", look=(1, 0)), t); top_shade(c, 0.5); Ph(c, "OOPSMYBUSINESS · HOW IT WORKS · FLOOR 4 OF 4"); S2(c, "a surprise at the desk?", "SCREENSHOT", YEL, 200); F(c, "FTC: A FEE AT CHECK-IN BELONGS IN THE TOTAL")
def ho_t1(c):
    hotel_lobby(c, t); elevator(c, 540, FLOOR, 400, "$238", floor_=4); stamp(c, 540, 1060, "NOT BANNED", RED_C, size=74); top_shade(c, 0.5); Ph(c); S2(c, "the rule doesn't", "BAN THE FEE", WHITE, 210); F(c, "FTC: \"DOES NOT PROHIBIT ANY TYPE OR AMOUNT OF FEE\"")
HO = [ho_i1, ho_i4, ho_a2, ho_a3, ho_b2, ho_c3, ho_c4, ho_d2, ho_d5, ho_t1]
OUT = os.path.join(_LAB, "storyboard_ep6_ep4b.jpg")
tiles = []
for fn in EP6 + HO:
    s = surface(); c = s.getCanvas(); fn(c)
    c.drawRect(R.MakeLTRB(60, 250, W - 120, H - 420), stroke((0, 255, 120), 3, 0.65))
    a = to_rgb(s); a = a if a.dtype == "uint8" else (a * 255).astype("uint8")
    tiles.append(Image.fromarray(a).resize((270, 480)))
sheet = Image.new("RGB", (270 * 10, 480 * 2))
for i, im in enumerate(tiles): sheet.paste(im, (270 * (i % 10), 480 * (i // 10)))
sheet.save(OUT, quality=84); print(OUT)
