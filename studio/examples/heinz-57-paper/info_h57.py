"""MIND TRICKS N° 09 — The 57 on Heinz ketchup means nothing. PAPER look."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from reel_props import *

ASSETS = {}
RED = (232, 70, 60)


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, props=[(D_bottle('57'), 540, 1060, 360, 720, -5, 0.0)], words=[('57 MEANS', 540, 440, 160, INK, 0.0), ('NOTHING.', 540, 600, 170, RED, 0.3)], shake=0.5),
        dict(at='in eighteen', bg=D, labels=[('1892', 540, 560, 110, -3, None, H)], props=[(D_text('"21 STYLES"', 140, INK, sub='A SHOE AD HE SAW ON A TRAIN'), 540, 980, 800, 300, 2, 'twenty one')]),
        dict(at='his own', bg=P, props=[(D_bottle('?'), 540, 1060, 320, 640, 4, None)], words=[('HE WANTED', 540, 520, 120, CREAM, None), ('HIS OWN NUMBER.', 540, 660, 120, H, 'number')]),
        dict(at='his company', bg=PAPER_C, props=[(D_text('60+', 260, RED, sub='PRODUCTS HE ALREADY SOLD'), 540, 900, 760, 460, -3, 'sixty')], words=[('ALREADY SELLING:', 540, 500, 110, INK, None)], shake='sixty'),
        dict(at='so he picked', bg=D, props=[(D_text('5', 300, INK, sub='HIS LUCKY NUMBER'), 330, 900, 400, 460, -4, 'five'), (D_text('7', 300, RED, sub="HIS WIFE'S"), 750, 940, 400, 460, 4, 'seven')],
             words=[('THE MATH:', 540, 520, 120, CREAM, None)]),
        dict(at='fifty seven varieties', bg=P, props=[(D_bottle('57'), 330, 1060, 260, 520, -6, None), (D_bottle('57', col=(240, 170, 40)), 750, 1080, 260, 520, 6, None)],
             words=[('57 VARIETIES.', 540, 520, 130, CREAM, 'varieties'), ('ON EVERYTHING.', 540, 660, 120, H, 'everything')]),
        dict(at='a specific', bg=D, words=[('A SPECIFIC NUMBER', 540, 700, 104, CREAM, 'specific'), ('SOUNDS TRUE.', 540, 880, 170, H, 'true')], shake='true'),
        dict(at='go check', bg=PAPER_C, props=[(D_bottle('57'), 540, 1060, 340, 680, -3, None)], words=[('GO CHECK', 540, 470, 140, INK, None), ('YOUR FRIDGE.', 540, 620, 140, RED, 'fridge')]),
        dict(at='send this', bg=PAPER_C, props=[(D_bottle('57'), 540, 820, 240, 480, -3, None)], cap=(1180, 48, (40, 20, 60), None)),
    ]


S = Story(HERE, 'MIND TRICKS', 'N° 09', scenes, ASSETS, cover_at=lambda S: 0.9)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
