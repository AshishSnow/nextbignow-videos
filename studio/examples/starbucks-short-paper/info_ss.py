"""MONEY TIPS N° 01 — Starbucks' off-menu 'short' size. PAPER look."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from reel_props import *

ASSETS = {'cups': ('cups.bin', 'warm', (0.3, 0.0, 1.0, 1.0))}
RED = (232, 70, 60)


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, props=[(D_cups(hide=0), 540, 1000, 900, 560, -2, 0.0)], words=[('THE SIZE', 540, 440, 150, INK, 0.0), ('THEY HIDE.', 540, 590, 150, RED, 'menu')], shake='menu'),
        dict(at="it's called", bg=P, props=[(D_cups(sizes=(('SHORT', 8),), hi=0), 540, 1080, 400, 560, -3, None)], words=[('SHORT.', 540, 560, 200, H, 'short'), ('8 OZ', 540, 740, 120, CREAM, 'eight')]),
        dict(at='stores keep', bg=D, photos=[('cups', 540, 1060, 760, -3, None)], words=[('JUST ASK.', 540, 560, 160, H, 'ask')]),
        dict(at='starbucks started', bg=PAPER_C, props=[(D_cups(sizes=(('SHORT', 8), ('TALL', 12))), 540, 1040, 600, 560, -2, None)], labels=[('THE ORIGINAL MENU', 540, 540, 70, -3, None, (255, 214, 64))]),
        dict(at='when grande', bg=P, props=[(D_cups(hide=None), 540, 1040, 900, 560, 2, None)], words=[('+ GRANDE + VENTI', 540, 520, 100, CREAM, 'grande')]),
        dict(at='short came', bg=D, props=[(D_cups(hide=0), 540, 1040, 900, 560, -2, None)], words=[('SHORT: OFF THE BOARD', 540, 540, 96, H, 'off the board')], shake='off the board'),
        dict(at='so now', bg=PAPER_C, props=[(D_cups(sizes=(('TALL', 12), ('GRANDE', 16), ('VENTI', 20)), hi=0), 540, 1060, 700, 560, -2, None)],
             words=[('SMALLEST YOU SEE:', 540, 460, 100, INK, None), ('TALL. 12 OZ.', 540, 590, 120, RED, 'twelve')]),
        dict(at='hide the small', bg=P, words=[('HIDE THE SMALL,', 540, 620, 130, CREAM, 'hide'), ('THE MEDIUM', 540, 800, 150, H, 'medium'), ('BECOMES YOUR SMALL.', 540, 960, 96, CREAM, 'your small')], shake='your small'),
        dict(at='ask for', bg=PAPER_C, props=[(D_cups(sizes=(('SHORT', 8),), hi=0), 540, 1080, 400, 560, 3, None)], words=[('ASK FOR A SHORT', 540, 500, 120, INK, 'ask for'), ('(HOT DRINKS)', 540, 620, 70, RED, 'hot drink')]),
        dict(at='save this', bg=PAPER_C, photos=[('cups', 540, 860, 600, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'MONEY TIPS', 'N° 01', scenes, ASSETS, cover_at=lambda S: 1.2)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
