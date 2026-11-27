"""MONEY EXPLAINED N° 06 — Toblerone made the gaps bigger (2016, UK). PAPER look."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from reel_props import *

ASSETS = {'matterhorn': ('matterhorn.bin',)}
RED = (232, 70, 60)


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, props=[(D_bar(1.0, label='BEFORE'), 540, 880, 820, 320, -3, 0.0), (D_bar(4.0, label='AFTER'), 540, 1240, 820, 320, 3, 0.9)],
             words=[('THE GAPS', 540, 440, 150, INK, 0.0), ('GOT BIGGER.', 540, 590, 150, RED, 0.3)], shake='bigger'),
        dict(at='in twenty', bg=D, photos=[('matterhorn', 540, 1100, 700, -3, None)], labels=[('2016 · UK', 540, 560, 80, -3, None, H)], cap=(1440 - 40, 54, CREAM, None)),
        dict(at='the four hundred', bg=P, props=[(D_text('400g → 360g', 150, INK, sub='THE BIG BAR'), 540, 760, 820, 300, -3, 'four hundred'),
                                                  (D_text('170g → 150g', 150, RED, sub='THE EVERYDAY BAR'), 540, 1140, 820, 300, 3, 'one seventy')]),
        dict(at='same length', bg=PAPER_C, props=[(D_bar(1.0, label='BEFORE'), 540, 860, 820, 320, -2, None), (D_bar(4.0, label='AFTER'), 540, 1230, 820, 320, 2, 'wider')],
             words=[('SAME LENGTH.', 540, 470, 100, INK, 'same length'), ('SAME BOX. SAME PRICE.', 540, 590, 84, RED, 'same price')]),
        dict(at='mondelez', bg=D, words=[('"HIGHER', 540, 640, 150, CREAM, 'higher'), ('INGREDIENT COSTS"', 540, 800, 96, H, 'ingredient')], cap=(1000, 56, CREAM, None)),
        dict(at="that's shrinkflation", bg=P, words=[('SHRINK', 540, 640, 200, CREAM, 'shrinkflation'), ('FLATION.', 540, 840, 200, H, 'shrinkflation')], shake='shrinkflation'),
        dict(at='the price stays', bg=PAPER_C, props=[(D_text('PRICE: SAME', 140, INK), 540, 700, 760, 220, -3, 'price stays'), (D_text('PRODUCT: LESS', 120, RED), 540, 1000, 760, 220, 3, 'product shrinks')]),
        dict(at='so check', bg=D, props=[(D_bar(4.0), 540, 1150, 760, 280, -3, None)], words=[('CHECK THE WEIGHT,', 540, 560, 110, CREAM, 'weight'), ('NOT THE PRICE.', 540, 720, 130, H, 'not the price')]),
        dict(at='send this', bg=PAPER_C, photos=[('matterhorn', 540, 860, 600, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'MONEY EXPLAINED', 'N° 06', scenes, ASSETS, cover_at=lambda S: 1.4)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
