"""MIND TRICKS N° 08 — Movie villains can't use iPhones. PAPER look."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from reel_props import *

ASSETS = {'cinema': ('cinema.bin',), 'clapper': ('clapper.bin', 'warm', (0.3, 0.0, 1.0, 0.62))}
RED = (232, 70, 60)


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, props=[(D_phone(txt=['VILLAIN?', 'NO.'], accent=RED), 540, 1000, 340, 680, -6, 0.0)],
             words=[("VILLAINS CAN'T", 540, 470, 120, INK, 0.0), ('HAVE iPHONES', 540, 600, 120, RED, 0.3)], shake=0.4),
        dict(at='knives', bg=D, photos=[('clapper', 540, 1030, 760, -3, None)], labels=[('RIAN JOHNSON, 2020', 540, 640, 66, -3, 'rian', H)], cap=(1440 - 60, 54, CREAM, None)),
        dict(at='apple lets', bg=P, props=[(D_phone(txt=['HERO', 'OK'], accent=(70, 160, 90)), 540, 1050, 300, 600, 4, None)], words=[('HEROES: YES.', 540, 560, 140, CREAM, 'apple lets')]),
        dict(at='quote', bg=D, words=[('"BAD GUYS', 540, 560, 150, CREAM, 'bad guys'), ('CANNOT HAVE', 540, 730, 150, CREAM, 'cannot'), ('IPHONES', 540, 900, 170, H, 'iphones'),
                                       ('ON CAMERA."', 540, 1070, 150, CREAM, 'on camera')], shake='cannot'),
        dict(at='so why', bg=PAPER_C, photos=[('cinema', 540, 1060, 820, 3, None)], words=[('WHY WOULD APPLE CARE?', 540, 520, 84, INK, 'so why')]),
        dict(at='because', bg=P, photos=[('cinema', 540, 1120, 640, -4, None)], words=[('A MOVIE IS AN AD', 540, 520, 120, CREAM, 'because'), ("YOU CAN'T SKIP.", 540, 680, 130, H, 'skip')]),
        dict(at='every hero', bg=D, props=[(D_phone(txt=['GOOD', 'GUYS'], accent=(70, 160, 90)), 330, 1040, 260, 520, -6, None), (D_phone(txt=['?'], accent=RED), 760, 1080, 260, 520, 6, 'who the good')],
             words=[('EVERY HERO', 540, 480, 110, CREAM, 'every hero'), ('HAS ONE.', 540, 620, 130, H, 'iphone')]),
        dict(at='apple has', bg=PAPER_C, labels=[('APPLE HAS NEVER CONFIRMED IT', 540, 760, 66, -3, 'never confirmed', RED, (255, 250, 240))], words=[('THE RULE?', 540, 560, 150, INK, None)]),
        dict(at='but now', bg=P, props=[(D_phone(txt=['CHECK', 'THE', 'PHONE'], accent=RED), 540, 1080, 320, 640, -3, None)], words=[("NOW YOU'LL CHECK", 540, 520, 110, CREAM, 'check'), ('EVERY VILLAIN.', 540, 660, 120, H, 'villain')]),
        dict(at='send this', bg=PAPER_C, photos=[('cinema', 540, 860, 600, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'MIND TRICKS', 'N° 08', scenes, ASSETS, cover_at=lambda S: 0.8)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
