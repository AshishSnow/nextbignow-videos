# Lab sheet, 6 Nov 2026 (R&D): HOW IT WORKS EP 2 credit score redrawn in Skia, rows from its shots.md, so the build run starts on nbnkit.
import os, sys
_LAB = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(_LAB, "..", "..", "template", "scripts"))
from nbnkit import *
import skia
from PIL import Image
S2 = lambda c, small, big, col=WHITE, size=240: two_tier(c, 9, 0, small, big, y=650, big_size=size, big_col=col, small_col=(240, 232, 255), shadow=True, maxw=800)
F = lambda c, s: src_chip(c, s, 1.0, y=1466)
P = lambda c, s="OOPSMYBUSINESS · HOW IT WORKS": pill(c, s, y=288)
t = 9.0
NAVY = ((16, 28, 80), (40, 70, 150)); PLUM = ((70, 26, 60), (170, 70, 110)); TEA = ((10, 70, 80), (30, 140, 130))
def i1(c):
    car_lot(c, t); car(c, 680, FLOOR, 620, tag="RATE?"); gauge(c, 680, 1060, 300, 0.62); hero(c, 200, FLOOR, 1.05, POSES["hold"], Face("wide", "o", look=(1, -1)), t); top_shade(c, 0.5); P(c); S2(c, "your credit score doesn't know", "YOUR SALARY", YEL, 210)
def i5(c):
    diagram_bg(c, *NAVY); score_slices(c, 540, 1100, 320, k=(0, 0, 0, 0, 0)); top_shade(c, 0.4); P(c); S2(c, "what's inside", "5 SLICES", WHITE)
def d1(c):
    diagram_bg(c, *NAVY); score_slices(c, 540, 1100, 320, k=(1, 1, 1, 1, 0), hl=3, labels=("10%", "10%", "15%", "35%", "")); top_shade(c, 0.4); P(c, "OOPSMYBUSINESS · HOW IT WORKS · SLICE 4 OF 5"); S2(c, "paying on time", "35%", ORANGE); F(c, "THE FIRST THING LENDERS WANT TO KNOW · myFICO")
def e1(c):
    diagram_bg(c, *NAVY); score_slices(c, 540, 1100, 320, labels=("10%", "10%", "15%", "35%", "30%")); top_shade(c, 0.4); P(c, "OOPSMYBUSINESS · HOW IT WORKS · SLICE 5 OF 5"); S2(c, "what you owe", "THE CATCH", YEL)
def e3(c):
    diagram_bg(c, *TEA); cycle_strip(c, 540, 1060, 860, 3); top_shade(c, 0.4); P(c, "OOPSMYBUSINESS · HOW IT WORKS · SLICE 5 OF 5"); S2(c, "your balance gets", "REPORTED", WHITE); F(c, "WHEN THE MONTHLY STATEMENT ENDS · Experian")
def e5(c):
    diagram_bg(c, *TEA); cycle_strip(c, 540, 1060, 860, 3, pay=1.0); top_shade(c, 0.4); P(c, "OOPSMYBUSINESS · HOW IT WORKS · SLICE 5 OF 5"); S2(c, "pay before it", "ENDS", GRN); F(c, "MAY LOWER WHAT'S REPORTED · NOT FINANCIAL ADVICE")
def f2(c):
    diagram_bg(c, *PLUM, disc=(255, 200, 120), cx=540, cy=1080, r=400); credit_report(c, 540, 1090, 420, err=True); top_shade(c, 0.4); P(c); S2(c, "an error, on at least one report", "1 IN 5", YEL); F(c, "FTC, 2013")
def z1(c):
    car_lot(c, t); score_slices(c, 540, 1120, 170, labels=None); label_card(c, 280, 1330, "YES", 64, col=GRN); label_card(c, 800, 1330, "NO", 64, col=RED_C); top_shade(c, 0.5); P(c); S2(c, "should your salary count?", "YES OR NO", WHITE, 220)
tiles = []
for fn in (i1, i5, d1, e1, e3, e5, f2, z1):
    s = surface(); c = s.getCanvas(); fn(c)
    c.drawRect(R.MakeLTRB(60, 250, W - 120, H - 420), stroke((0, 255, 120), 3, 0.65))
    a = to_rgb(s); a = a if a.dtype == "uint8" else (a * 255).astype("uint8"); tiles.append(Image.fromarray(a).resize((270, 480)))
sheet = Image.new("RGB", (270 * 8, 480))
for i, im in enumerate(tiles): sheet.paste(im, (270 * i, 0))
OUT = os.path.join(_LAB, "storyboard_ep2_skia.jpg"); sheet.save(OUT, quality=84); print(OUT)
