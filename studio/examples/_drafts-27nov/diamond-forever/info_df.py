"""CASE STUDY N° 06 — your engagement ring was an ad campaign ('A Diamond Is Forever'). PAPER look (paper_story)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from paper_story import *

ASSETS = {'ring': ('ring.bin',), 'ring2': ('ring2.bin',), 'rough': ('rough2.bin',), 'bride': ('bride.bin', 'sepia'),
          'mine': ('mine.bin', 'sepia', (0.25, 0.62, 0.73, 0.81)), 'type': ('type.bin', 'sepia')}


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, photos=[('ring', 540, 1060, 720, -4, 0.0)], cap=(560, 70, INK, 'was an'), arrow=(250, 640, 420, 860, 0.3)),
        dict(at='was an ad', bg=P, photos=[('ring', 540, 1140, 560, 5, None)], words=[('AN AD', 540, 560, 200, CREAM, None), ('CAMPAIGN.', 540, 760, 190, H, 'campaign')],
             shake='campaign'),
        dict(at='before world', bg=D, photos=[('bride', 540, 1080, 760, -3, None)], cap=(560, 62, CREAM, 'only about')),
        dict(at='only about', bg=P, props=[(D_text('1 IN 10', 230, INK, sub='ENGAGEMENT RINGS HAD A DIAMOND'), 540, 1080, 760, 420, -3, 'one in ten')],
             cap=(560, 62, CREAM, 'one in ten')),
        dict(at='diamond sales', bg=P, photos=[('rough', 540, 1120, 720, 4, None)], words=[('FALLING.', 540, 640, 190, H, 'falling')]),
        dict(at='so the diamond', bg=D, photos=[('mine', 540, 1100, 800, -3, None)], cap=(560, 60, CREAM, 'with one'),
             labels=[('A PHILADELPHIA AD AGENCY', 540, 1440, 62, 3, 'philadelphia', H)]),
        dict(at='make diamonds', bg=P, photos=[('ring2', 540, 1180, 600, -4, None)], words=[('MAKE DIAMONDS', 540, 560, 118, CREAM, None), ('FEEL LIKE LOVE.', 540, 710, 118, H, 'feel like')]),
        dict(at='then one late', bg=D, photos=[('type', 540, 1100, 760, 3, None)], cap=(560, 62, CREAM, 'a diamond is'),
             labels=[('FRANCES GERETY, COPYWRITER', 540, 1440, 58, -3, 'frances', H)]),
        dict(at='a diamond is', bg=PAPER_C, big=[('A diamond', 540, 880, 190, 'serif', INK, None), ('is forever.', 540, 1080, 190, 'serif', P, 'forever')],
             labels=[('4 WORDS', 540, 1300, 70, -4, 'forever', H)]),
        dict(at='forever so', bg=P, photos=[('ring', 540, 1160, 600, 4, 'so you keep')], words=[('FOREVER.', 540, 600, 200, H, None)],
             cap=(1440, 60, CREAM, None)),
        dict(at='within a few', bg=D, photos=[('bride', 330, 1000, 500, -5, None)],
             props=[(D_text('8 IN 10', 170, INK, sub='AMERICAN BRIDES'), 720, 1320, 560, 330, 4, 'eight in ten')], cap=(560, 60, CREAM, 'advertising age')),
        dict(at='advertising age', bg=P, words=[('SLOGAN OF', 540, 820, 170, CREAM, 'slogan'), ('THE CENTURY.', 540, 1000, 150, H, 'century')],
             cap=(560, 58, CREAM, 'slogan'), shake='century'),
        dict(at='we think', bg=D, photos=[('ring2', 540, 1120, 620, -3, None)], cap=(560, 64, CREAM, 'the ring was'),
             words=[('CHOSEN', 540, 620, 180, H, 'chosen'), ('FOR US.', 540, 800, 180, CREAM, 'for us')]),
        dict(at='send this', bg=PAPER_C, photos=[('ring', 540, 800, 560, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'CASE STUDY', 'N° 06', scenes, ASSETS, cover_at=lambda S: S.ph('campaign') + 0.6)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
