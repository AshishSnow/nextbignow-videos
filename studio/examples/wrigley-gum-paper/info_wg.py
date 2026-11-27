"""BUSINESS IDEA N° 05 — Wrigley's gum started as a free gift. PAPER look (paper_story)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from paper_story import *

ASSETS = {'gum': ('gum.bin',), 'gum2': ('gum2.bin',), 'soap': ('soap.bin',), 'powder': ('powder.bin', 'sepia'), 'chicago': ('chicago.bin', 'sepia'),
          'phone': ('phone.bin',)}


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, photos=[('gum', 540, 1070, 700, -4, 0.0)], cap=(560, 70, INK, 'started as'), arrow=(240, 650, 400, 880, 0.3)),
        dict(at='started as', bg=P, photos=[('gum', 540, 1150, 560, 5, None)], words=[('A FREE', 540, 560, 190, CREAM, 'a free'), ('GIFT.', 540, 760, 220, H, 'gift')], shake='gift'),
        dict(at='in eighteen', bg=D, photos=[('chicago', 540, 1060, 780, -3, None)], cap=(560, 60, CREAM, 'to get'),
             labels=[('1891, CHICAGO', 330, 1420, 66, -4, None, H), ('SELLING SOAP', 720, 1440, 62, 4, 'soap')]),
        dict(at='to get stores', bg=P, photos=[('soap', 340, 980, 460, -5, None), ('powder', 740, 1160, 440, 5, 'free baking')], cap=(560, 60, CREAM, None),
             labels=[('+ FREE', 740, 1420, 70, 3, 'free baking', H)]),
        dict(at='the baking powder sold', bg=D, photos=[('powder', 540, 1150, 600, -3, None)], words=[('SOLD BETTER', 540, 580, 160, H, 'sold better'), ('THAN THE SOAP.', 540, 750, 120, CREAM, 'than the soap')]),
        dict(at='so he switched', bg=P, photos=[('powder', 340, 1000, 440, -5, None), ('gum2', 740, 1160, 440, 5, 'free gum')], cap=(560, 60, CREAM, None),
             labels=[('+ FREE GUM', 740, 1420, 70, 3, 'free gum', H)]),
        dict(at='then people wanted', bg=D, photos=[('gum2', 540, 1130, 600, 4, None)], cap=(560, 64, CREAM, 'so he dropped'),
             words=[('DROPPED BOTH.', 540, 760, 150, CREAM, 'dropped'), ('JUST GUM.', 540, 1460, 160, H, 'sold gum')]),
        dict(at='then he mailed', bg=P, photos=[('phone', 540, 1180, 560, -3, None)], cap=(560, 60, CREAM, 'one and a half'),
             props=[(D_text('~1.5M', 200, INK, sub='HOMES GOT FREE GUM'), 540, 820, 600, 330, 3, 'one and a half')]),
        dict(at='in two thousand', bg=D, props=[(D_text('$23B', 260, INK, sub='MARS BUYS WRIGLEY, 2008'), 540, 1060, 700, 420, -3, 'twenty three')],
             cap=(560, 60, CREAM, None), shake='twenty three'),
        dict(at='he never picked', bg=P, photos=[('gum', 540, 1220, 500, 4, None)], words=[('HE NEVER', 540, 560, 170, CREAM, None), ('PICKED GUM.', 540, 740, 170, CREAM, 'picked gum'),
                                                                                    ('HIS CUSTOMERS DID.', 540, 1520 - 80, 110, H, 'his customers')]),
        dict(at='send this', bg=PAPER_C, photos=[('gum2', 540, 800, 560, -3, None)], cap=(1180, 64, (40, 20, 60), None)),
    ]


S = Story(HERE, 'BUSINESS IDEA', 'N° 05', scenes, ASSETS, cover_at=lambda S: S.ph('gift') + 0.6)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
