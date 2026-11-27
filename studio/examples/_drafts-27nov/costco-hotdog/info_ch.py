"""FOUNDER MINDSET N° 05 — Costco's $1.50 hot dog and the cofounder who refused to raise it. PAPER look (paper_story)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from paper_story import *

ASSETS = {'dog': ('dog.bin',), 'dog2': ('dog2.bin',), 'aisle': ('aisle.bin',), 'cart': ('cart.bin',), 'door': ('door.bin',)}
INKQ = (40, 20, 10)


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, photos=[('dog', 540, 1080, 740, -4, 0.0)], cap=(560, 70, INK, 'a dollar'), arrow=(240, 640, 400, 880, 0.3)),
        dict(at='a dollar fifty', bg=P, props=[(D_text('$1.50', 260, INK), 540, 1040, 760, 380, -4, None)], shake='fifty',
             words=[('STILL.', 540, 620, 170, CREAM, 'fifty')]),
        dict(at='the same price', bg=D, photos=[('dog2', 540, 1120, 720, 3, None)], words=[('SAME PRICE', 540, 560, 150, CREAM, None), ('SINCE THE MID-80s', 540, 720, 110, H, 'mid')]),
        dict(at='and one founder', bg=P, cap=(560, 64, CREAM, None), labels=[('ONE FOUNDER', 540, 1000, 120, -3, 'founder', H)],
             photos=[('dog', 540, 1380, 420, 5, 'made sure')]),
        dict(at='everything got', bg=D, photos=[('aisle', 540, 1200, 520, -3, None)], words=[('EVERYTHING', 540, 560, 160, CREAM, None), ('GOT PRICIER.', 540, 730, 150, H, 'expensive')]),
        dict(at='so the ceo', bg=P, labels=[('THE CEO', 330, 760, 90, -5, 'the ceo'), ('JIM SINEGAL, COFOUNDER', 560, 960, 66, 3, 'jim', H)],
             cap=(1400, 62, CREAM, 'raise the price'), words=[('RAISE THE PRICE?', 540, 1300, 120, H, 'raise the price')]),
        dict(at='his answer', bg=D, cap=(560, 70, CREAM, 'if you'),
             big=[('"If you raise', 540, 860, 130, 'serif', CREAM, 'if you'), ('the effing hot dog,', 540, 1010, 112, 'serif', CREAM, 'effing'),
                  ('I will kill you."', 540, 1200, 130, 'serif', H, 'i will')],
             labels=[('JIM SINEGAL', 540, 1420, 56, -3, 'kill')], shake='kill'),
        dict(at='why protect', bg=P, photos=[('dog2', 540, 1180, 640, -4, None)], words=[('WHY PROTECT', 540, 560, 150, CREAM, None), ('A HOT DOG?', 540, 730, 160, H, 'a hot dog')]),
        dict(at="because it's", bg=D, photos=[('door', 540, 1020, 720, 3, None)], cap=(560, 62, CREAM, 'and nobody'), words=[('THE DOOR.', 540, 1450, 140, H, 'door')]),
        dict(at='and nobody leaves', bg=P, photos=[('cart', 540, 1180, 700, -3, None)], words=[('NOBODY LEAVES WITH', 540, 560, 96, CREAM, None), ('JUST A HOT DOG.', 540, 720, 130, H, 'just a hot')]),
        dict(at='today they', bg=D, props=[(D_text('100M+', 250, INK, sub='SOLD EVERY YEAR'), 540, 1060, 760, 420, -3, 'hundred million')],
             cap=(560, 62, CREAM, None), shake='hundred million'),
        dict(at='most companies', bg=P, cap=(560, 62, CREAM, 'costco keeps'), words=[('RAISE PRICES', 540, 1000, 160, H, 'raise prices')]),
        dict(at='costco keeps', bg=D, photos=[('dog', 540, 1180, 600, 4, None)], words=[('ONE PRICE', 540, 560, 170, H, 'one price'), ('= TRUST', 540, 740, 150, CREAM, 'trust')]),
        dict(at='send this', bg=PAPER_C, photos=[('dog2', 540, 800, 560, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'FOUNDER MINDSET', 'N° 05', scenes, ASSETS, cover_at=lambda S: S.ph('kill') + 0.7)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
