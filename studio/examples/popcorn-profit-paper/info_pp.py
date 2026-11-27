"""MONEY EXPLAINED N° 05 — your movie ticket barely pays the theater; the popcorn does. PAPER look (paper_story)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from paper_story import *

ASSETS = {'pop': ('pop.bin',), 'pop2': ('stand.bin',), 'theater': ('theater.bin',), 'ticket': ('stubs.bin', 'sepia'),
          'stand': ('stand.bin',), 'proj': ('proj.bin', 'sepia')}


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, photos=[('ticket', 540, 1060, 700, -4, 0.0)], cap=(560, 70, INK, 'barely')),
        dict(at='barely', bg=P, photos=[('ticket', 540, 1120, 560, 5, None)], words=[('BARELY PAYS', 540, 640, 150, H, None)],
             labels=[('THE THEATER', 540, 790, 70, -3, 'the theater')]),
        dict(at='the popcorn', bg=D, photos=[('pop', 540, 1080, 820, -3, None)], words=[('THE POPCORN', 540, 600, 150, CREAM, None), ('DOES.', 540, 1450, 200, H, 'does')],
             shake='does'),
        dict(at='when you buy', bg=P, photos=[('theater', 540, 1060, 860, -2, None)], cap=(560, 62, CREAM, 'the studio')),
        dict(at='the studio', bg=P, photos=[('proj', 540, 1080, 700, 3, None)], labels=[('THE STUDIO', 540, 600, 80, -3, None, H)],
             cap=(1420, 60, CREAM, 'on average')),
        dict(at='on average', bg=D, props=[(D_pie(0.70, RED_, txt='TO THE STUDIO'), 540, 1100, 560, 560, -3, None)],
             words=[('~70%', 540, 650, 260, H, 'seventy')]),
        dict(at='but the studio', bg=P, photos=[('stand', 540, 1080, 800, 3, None)], words=[('SNACK BAR', 540, 620, 150, CREAM, 'snack bar')],
             labels=[('STUDIO GETS $0', 540, 1440, 72, -3, 'nothing', H)]),
        dict(at='every dollar', bg=D, photos=[('pop2', 540, 1100, 760, -4, None)], cap=(560, 64, CREAM, None)),
        dict(at='and popcorn is', bg=P, photos=[('pop', 540, 1180, 600, 4, None)], cap=(560, 64, CREAM, 'snacks run'),
             words=[('CHEAP', 540, 800, 180, H, 'cheap')]),
        dict(at='snacks run', bg=D, props=[(D_text('85%', 260, INK, sub='PROFIT MARGIN ON SNACKS'), 540, 1060, 700, 420, -3, 'eighty five')],
             cap=(560, 64, CREAM, 'eighty five'), shake='eighty five'),
        dict(at="that's why", bg=P, props=[(D_pie(0.45, YEL, txt='OF THE PROFIT'), 540, 1120, 560, 560, 3, 'almost half')],
             cap=(560, 64, CREAM, 'almost half'), words=[('ALMOST HALF', 540, 640, 150, H, 'almost half')]),
        dict(at='the movie gets', bg=D, photos=[('theater', 330, 800, 460, -6, None), ('pop', 740, 1060, 460, 6, 'the popcorn pays')],
             words=[('GETS YOU IN.', 540, 560, 130, CREAM, 'gets you'), ('PAYS FOR', 540, 1330, 130, H, 'pays for'), ('THE SEAT.', 540, 1460, 130, H, 'the seat')]),
        dict(at='send this', bg=PAPER_C, photos=[('pop2', 540, 800, 560, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'MONEY EXPLAINED', 'N° 05', scenes, ASSETS, cover_at=lambda S: S.ph('does') + 0.6)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
