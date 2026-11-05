# lab frames: HOW TO START EP 5 (reselling) + HOW IT WORKS EP 3 (Shorts money), real NBN kit, safe-zone guides. R&D 5 Nov 2026.
import sys, os, math
_LAB = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(_LAB, "..", "..", "template", "scripts"))
from nbnkit import *
from nbnkit import _rot_stick
import skia
from PIL import Image
S2 = lambda c, small, big, col=WHITE, size=240: two_tier(c, 9, 0, small, big, y=650, big_size=size, big_col=col, small_col=(240, 232, 255), shadow=True, maxw=800)
F = lambda c, s: src_chip(c, s, 1.0, y=1466)
P = lambda c: pill(c, "OOPSMYBUSINESS", y=288)
t = 9.0
INC = ((60, 28, 92), (150, 60, 120)); NAVY = ((16, 28, 80), (40, 70, 150)); TEA = ((10, 70, 80), (30, 140, 130)); WARM = ((90, 40, 30), (190, 100, 50)); VIO = ((44, 28, 110), (110, 60, 170))
def i1(c):
    pack_room(c, t); jacket(c, 300, 760, 300); jacket(c, 780, 760, 300, col=(200, 80, 70))
    stamp(c, 300, 960, "NO TAX", GRN); stamp(c, 780, 960, "TAX?", RED_C, tilt=8)
    hero(c, 540, FLOOR, 1.1, POSES["shrug"], Face("open", "smile", look=(1, -1)), t); top_shade(c, 0.5); P(c); S2(c, "both sold online", "TWO JACKETS", YEL, 200)
def i3(c):
    pack_room(c, t); jacket(c, 720, 780, 320, worn=1); price_tag(c, 760, 900, "$80", tilt=-8); price_tag(c, 760, 1050, "$20", tilt=4); stamp(c, 720, 1190, "NO TAX", GRN)
    hero(c, 290, FLOOR, 1.15, POSES["hold"], Face("open", "grin", look=(1, 0)), t); top_shade(c, 0.5); P(c); S2(c, "you lost money, so", "NO TAX", GRN); F(c, "MADE-UP NUMBERS · A GAIN IS TAXABLE, SAYS THE IRS")
def i4(c):
    diagram_bg(c, *WARM, disc=(255, 190, 90), cx=540, cy=1080, r=400); jacket(c, 540, 800, 360, col=(60, 160, 120)); price_tag(c, 300, 1180, "$5"); price_tag(c, 790, 1180, "$30", tilt=5, col=(30, 140, 90)); parcel(c, 540, 1430, 180)
    top_shade(c, 0.4); P(c); S2(c, "bought to sell", "$5, THEN $30", WHITE, 240); F(c, "MADE-UP NUMBERS")
def a2(c):
    diagram_bg(c, *VIO, disc=(255, 210, 120), cx=540, cy=1080, r=390); listing_card(c, 300, 1090, 360, "$100", "ASKING", tilt=-4); listing_card(c, 780, 1080, 380, "$30", "SOLD", tilt=3)
    top_shade(c, 0.4); P(c); S2(c, "search finished sales", "NOT ASKING", YEL, 220); F(c, 'ON EBAY: SEARCH, THEN FILTER "SOLD ITEMS"')
def b4(c):
    diagram_bg(c, *TEA, disc=(255, 220, 130), cx=540, cy=1080, r=390); receipt(c, 540, 1080, 620, [("SOLD", "$30"), ("FEES, ABOUT", "-$5"), ("JACKET", "-$5")], total=("KEEP, ABOUT", "$20"))
    top_shade(c, 0.4); P(c); S2(c, "postage still to come", "ABOUT $20", WHITE); F(c, "MADE-UP SALE · EBAY MOST CATEGORIES, NOV 2026")
def c2(c):
    pack_room(c, t); line_tally(c, 620, 1040, 720, [("$5", "$30", "$4.48"), ("$12", "$40", "$5.84"), ("$3", "$18", "$2.85")]); girl(c, 150, FLOOR, 1.0, POSES["point"], Face("open", "smile", look=(1, -1)), t)
    top_shade(c, 0.5); P(c); S2(c, "one simple list", "PAID · SOLD · FEES", YEL, 170); F(c, 'IRS: "SAVE RECEIPTS OF YOUR EXPENSES"')
def d3(c):
    diagram_bg(c, *NAVY, disc=(120, 170, 255), cx=540, cy=1080, r=390); tax_form(c, 330, 1090, 380, ghost=True); stamp(c, 740, 1060, "REPORT IT ALL", RED_C, size=60)
    girl(c, 800, FLOOR, 1.0, POSES["stand"], Face("open", "smile"), t); top_shade(c, 0.4); P(c); S2(c, "the irs says", "NO FORM? STILL", WHITE, 170); F(c, "IRS, 2026")
def t1(c):
    diagram_bg(c, *NAVY, floor=None); c.drawRect(R.MakeLTRB(540, 0, W, H), paint(TEAL_C, 0.45))
    tax_form(c, 280, 1090, 320); stamp(c, 280, 1090, "NO TAX", GRN); tax_form(c, 800, 1090, 320, ghost=True); stamp(c, 800, 1200, "TAX", RED_C)
    hero(c, 540, FLOOR, 1.0, POSES["shrug"], Face("wide", "o"), t); top_shade(c, 0.4); P(c); S2(c, "a form doesn't mean", "YOU OWE", YEL, 240)
EP5 = [i1, i3, i4, a2, b4, c2, d3, t1]
def h1(c):
    waterworks(c, t); feed_phone(c, 690, 1090, 340, t=t); pipe(c, [(580, 1200), (380, 1200), (380, 1040)], w=26, flow=0.3, t=t); coin(c, 300, 1100, 28)
    hero(c, 250, FLOOR, 1.12, POSES["hold"], Face("wide", "o", look=(1, -1)), t); top_shade(c, 0.5); P(c); S2(c, "your youtube short", "1,000,000 VIEWS", YEL, 170); F(c, "CAN PAY $200 OR LESS · ONE COMPANY'S DATA")
def h3(c):
    waterworks(c, t); tank(c, 660, FLOOR, 520, 0.55, t=t); feed_phone(c, 250, 920, 170, t=t); pipe(c, [(340, 900), (560, 900)], w=30, flow=0.9, t=t)
    hero(c, 240, FLOOR, 1.05, POSES["point_up"] if "point_up" in POSES else POSES["point"], Face("open", "o", look=(1, -1)), t); top_shade(c, 0.5); P(c); S2(c, "not paid per ad", "ADDED UP FIRST", WHITE, 170); F(c, "ADS BETWEEN SHORTS, EACH MONTH · YOUTUBE HELP")
def h_a3(c):
    diagram_bg(c, *TEA, disc=(255, 214, 110), cx=540, cy=1040, r=400); tank(c, 330, 1420, 400, 0.5, t=t, label="POOL"); pipe(c, [(540, 900), (800, 900), (800, 1120)], w=38, flow=0.8, t=t); valve(c, 650, 900, 74, turn=0.5); label_card(c, 800, 1200, "MUSIC", 62)
    top_shade(c, 0.4); P(c); S2(c, "one song", "HALF", YEL); F(c, "OF THE MONEY TIED TO THAT SHORT'S VIEWS")
def h_a4(c):
    waterworks(c, t); pie_wedge(c, 300, 960, 120, 0.2); pie_wedge(c, 760, 960, 120, 0.2); notes(c, 300, 820, t, n=3)
    hero(c, 300, FLOOR, 1.05, POSES["stand"], Face("open", "smile", look=(1, 0)), t); girl(c, 760, FLOOR, 1.05, POSES["stand"], Face("open", "smile", look=(-1, 0)), t)
    top_shade(c, 0.5); P(c); S2(c, "song or no song", "SAME SHARE", WHITE); F(c, "YOUTUBE HELP")
def h_b3(c):
    diagram_bg(c, *VIO, disc=(255, 214, 110), cx=540, cy=1080, r=380); dot_grid(c, 540, 1080, 100, mine=1, w=620, flash=0.8, cols=10)
    top_shade(c, 0.4); P(c); S2(c, "you get", "1 MILLION VIEWS", YEL, 200); F(c, "YOUTUBE'S OWN MADE-UP EXAMPLE")
def h_c2(c):
    diagram_bg(c, *WARM, disc=(255, 214, 110), cx=540, cy=1080, r=380); split_bar(c, 540, 1000, 800, 0.45, "YOU 45%", "NOT YOU 55%", k=1); price_tag(c, 540, 1220, "NOW $405", size=72, tilt=-3)
    top_shade(c, 0.4); P(c); S2(c, "creators keep", "45%", WHITE); F(c, "LONG VIDEOS: 55% · MUSIC OR NOT, SAME 45%")
def h_d2(c):
    waterworks(c, t, lamp_a=0.3); calendar(c, 230, 860, 1.0, "FEB", "2027"); line_meter(c, 540, 1040, 760, 0.1, "", k=1)
    hero(c, 280, FLOOR, 1.0, POSES["stand"], Face("wide", "o", look=(1, -1)), t); top_shade(c, 0.5); P(c); S2(c, "the new target", "10 MILLION", RED_C, 240); F(c, "IN THE LAST 90 DAYS · YOUTUBE, AUG 2026")
def h_e4(c):
    waterworks(c, t); feed_phone(c, 690, 1090, 340, t=t, ad=True); hero(c, 300, FLOOR, 1.15, POSES["shrug"], Face("open", "smile", look=(0, 0)), t)
    top_shade(c, 0.5); P(c); S2(c, "on youtube, this channel", "NOT IN YET", YEL, 220)
EP3 = [h1, h3, h_a3, h_a4, h_b3, h_c2, h_d2, h_e4]
OUT = os.path.join(_LAB, "storyboard_ep5_ep3b.jpg")
tiles = []
for fn in EP5 + EP3:
    s = surface(); c = s.getCanvas(); fn(c)
    c.drawRect(R.MakeLTRB(60, 250, W - 120, H - 420), stroke((0, 255, 120), 3, 0.65))
    arr = (to_rgb(s) * 255).astype("uint8"); tiles.append(Image.fromarray(arr).resize((270, 480)))
sheet = Image.new("RGB", (270 * 8, 480 * 2))
for i, im in enumerate(tiles): sheet.paste(im, (270 * (i % 8), 480 * (i // 8)))
sheet.save(OUT, quality=82); print(OUT)
