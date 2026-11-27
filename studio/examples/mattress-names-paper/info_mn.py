"""CASE STUDY N° 07 — Same mattress, a different name at every store. PAPER look."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from reel_props import *

ASSETS = {}
RED = (232, 70, 60)


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, props=[(D_mattress('STORE A: "CLOUD LUXE"', '$1,299'), 540, 820, 760, 320, -3, 0.0), (D_mattress('STORE B: "DREAM ROYALE"', '$999', tag=(255, 170, 160)), 540, 1180, 760, 320, 3, 0.5)],
             words=[('SAME BED.', 540, 420, 140, INK, 0.0), ('NEW NAME.', 540, 560, 140, RED, 'different name')], shake='different name'),
        dict(at='serta says', bg=D, props=[(D_text('"WE ALLOW RETAILERS', 76, INK), 540, 740, 860, 150, -2, 'we allow'), (D_text('TO CHOOSE AND ADD', 76, INK), 540, 920, 860, 150, 2, 'choose'),
                                           (D_text('A DIFFERENT SHOWROOM NAME."', 64, RED, sub='SERTA HELP CENTER'), 540, 1120, 860, 200, -2, 'showroom')], words=[('THE MAKER SAYS IT:', 540, 520, 90, CREAM, None)]),
        dict(at="so you can't", bg=P, props=[(D_phone(txt=['NO', 'RESULTS'], accent=RED), 540, 1060, 320, 640, -4, None)], words=[("SEARCH THE NAME?", 540, 520, 120, CREAM, 'search'), ('NOTHING.', 540, 660, 140, H, 'cheaper')]),
        dict(at="consumers'", bg=D, words=[('"CAREFULLY CREATED', 540, 600, 92, CREAM, 'carefully'), ('A SYSTEM THAT MAKES IT', 540, 740, 90, CREAM, 'system'),
                                           ('IMPOSSIBLE', 540, 900, 170, H, 'impossible'), ('TO SHOP AROUND."', 540, 1060, 110, CREAM, 'shop around')], labels=[("CONSUMERS' CHECKBOOK", 540, 1260, 56, -2, "consumers'", (255, 214, 64))], shake='impossible'),
        dict(at='so compare', bg=PAPER_C, labels=[('BRAND LINE', 540, 700, 100, -3, 'brand line', (255, 214, 64)), ('COMFORT LEVEL', 540, 880, 100, 3, 'comfort', (255, 214, 64)),
                                                   ('NOT THE NAME', 540, 1080, 100, -2, 'not the name', RED, (255, 250, 240))], words=[('COMPARE:', 540, 500, 130, INK, None)]),
        dict(at='send this', bg=PAPER_C, props=[(D_mattress('SAME BED'), 540, 820, 680, 300, -3, None)], cap=(1180, 54, (40, 20, 60), None)),
    ]


S = Story(HERE, 'CASE STUDY', 'N° 07', scenes, ASSETS, cover_at=lambda S: 1.4)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
