"""FOUNDER MINDSET N° 05 — the world's most famous restaurant award was invented by a tire company. PAPER look (paper_story)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from paper_story import *
ST = S

ASSETS = {'dine': ('dine.bin',), 'chef': ('chef.bin',), 'tire': ('car.bin', 'sepia'), 'car': ('car2.bin', 'sepia'), 'road': ('road.bin',)}


def D_book(c):
    """plain guidebook (no trade dress): cloth cover, three lines inside"""
    c.drawRRect(rr(-200, -250, 400, 500, 18), P((60, 70, 90))); c.drawRRect(rr(-200, -250, 400, 500, 18), ST(INK, 5))
    c.drawRect(skia.Rect.MakeXYWH(-160, -200, 320, 400), P((246, 238, 220)))
    f = cond(44); g = serif(40)
    c.drawString('GUIDE', -f.measureText('GUIDE') / 2, -130, f, P(INK))
    for i, s in enumerate(('where to eat', 'where to sleep', 'fix your car')): c.drawString(s, -g.measureText(s) / 2, -40 + i * 70, g, P((150, 60, 30)))
    c.drawString('FREE', -f.measureText('FREE') / 2, 175, f, P((200, 60, 40)))


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, photos=[('dine', 540, 1070, 720, -4, 0.0)], cap=(560, 64, INK, 'was invented'), arrow=(240, 650, 400, 880, 0.3)),
        dict(at='was invented', bg=P, photos=[('tire', 540, 1150, 560, 5, None)], words=[('A TIRE', 540, 560, 200, CREAM, 'a tire'), ('COMPANY.', 540, 760, 200, H, 'company')], shake='company'),
        dict(at='in nineteen hundred', bg=D, photos=[('car', 540, 1180, 600, -3, None)], cap=(560, 60, CREAM, 'fewer'),
             props=[(D_text('<3,000', 200, INK, sub='CARS IN ALL OF FRANCE'), 540, 760, 620, 320, 3, 'fewer')]),
        dict(at='so brothers', bg=P, photos=[('road', 540, 1150, 640, -3, None)], cap=(560, 60, CREAM, 'nobody was'),
             words=[('NOBODY DRIVING.', 540, 700, 120, CREAM, 'nobody was'), ('NO TIRES SOLD.', 540, 1460, 120, H, 'nobody needed')]),
        dict(at='their fix', bg=D, props=[(D_book, 540, 1100, 480, 580, -3, 'a free')], words=[('A FREE GUIDE.', 540, 600, 150, H, 'a free')]),
        dict(at='where to eat', bg=P, photos=[('dine', 540, 1120, 640, 4, None)],
             labels=[('EAT', 300, 620, 80, -5, 'eat'), ('SLEEP', 560, 720, 80, 3, 'sleep'), ('FIX YOUR CAR', 760, 600, 64, 5, 'fix your', H)]),
        dict(at='thirty five', bg=D, props=[(D_text('35,000', 220, INK, sub='COPIES, GIVEN AWAY FREE'), 540, 1040, 720, 420, -3, None)], shake='given away',
             words=[('FREE.', 540, 1440, 160, H, 'given away')]),
        dict(at='later they added', bg=P, photos=[('chef', 540, 1180, 560, -3, None)], cap=(560, 60, CREAM, 'two stars'),
             labels=[('2 STARS = WORTH A DETOUR', 540, 700, 62, -3, 'two stars'), ('3 STARS = WORTH A SPECIAL JOURNEY', 540, 830, 52, 3, 'three stars', H)]),
        dict(at='a journey means', bg=D, photos=[('car', 330, 1000, 440, -6, None), ('tire', 740, 1180, 420, 6, 'driving means')],
             words=[('JOURNEY = DRIVING.', 540, 600, 120, CREAM, None), ('DRIVING = TIRES.', 540, 1460, 120, H, 'driving means')]),
        dict(at="they didn't", bg=P, photos=[('tire', 540, 1150, 520, -4, None)], words=[("THEY DIDN'T", 540, 560, 160, CREAM, None), ('SELL TIRES.', 540, 740, 160, CREAM, 'sell tires')],
             labels=[('THEY SOLD A REASON TO DRIVE.', 540, 1440, 58, -3, 'a reason', H)]),
        dict(at='send this', bg=PAPER_C, photos=[('dine', 540, 800, 560, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'FOUNDER MINDSET', 'N° 05', scenes, ASSETS, cover_at=lambda S: S.ph('company') + 0.6)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
