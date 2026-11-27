"""BUSINESS TRICKS · EP 03 (YouTube 16:9) — Why hotels hide the real price. PAPER wide look."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
os.environ.setdefault('OMB_WIDE', '1')
from wide_props import *

ASSETS = {'room': ('room.bin',), 'vegas': ('vegas.bin',), 'minibar': ('minibar.bin',), 'lobby': ('lobby.bin',), 'crowd': ('crowd.bin',)}
RED = (232, 70, 60)
L, R_, CX = 600, 1340, 960


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, photos=[('crowd', L, 560, 600, -4, 0.0)], words=[('+21%', R_, 520, 280, RED, 'twenty one')], cap=(930, 50, INK, 'same tickets')),
        dict(at='same tickets', bg=P, words=[('SAME SEATS.', CX, 400, 140, CREAM, 'same seats'), ('LATER PRICE.', CX, 560, 150, H, 'the real price')], cap=(900, 46, CREAM, None)),
        dict(at='economists ran', bg=D, photos=[('room', R_, 560, 620, 4, 'hotels')], words=[('HOTELS.', L, 520, 180, H, 'hotels')], cap=(930, 46, CREAM, None), shake='hotels'),
        dict(at='trick number one', bg=P, chapter=('TRICK 1', 'The headline price')),
        dict(at="here's how", bg=PAPER_C, props=[(D_phone('checkout', accent=(150, 150, 160), label=[('TICKETS', '$100'), ('FEES', '$20'), ('TOTAL', '$120')]), L, 560, 330, 640, -3, 'half of'),
                                               (D_phone('checkout', accent=RED, label=[('TICKETS', '$100'), ('', ''), ('FEES LATER', '...')]), R_, 560, 330, 640, 3, 'the other half')],
             labels=[('GROUP A: ALL-IN PRICE', L, 160, 50, -2, 'half of'), ('GROUP B: FEES AT THE END', R_, 160, 50, 2, 'the other half', RED, (255, 250, 240))]),
        dict(at='the second group', bg=D, props=[(D_text('+14%', 200, INK, sub='MORE LIKELY TO BUY'), L, 520, 560, 360, -3, 'fourteen'),
                                                 (D_text('+21%', 200, RED, sub='MORE MONEY SPENT'), R_, 540, 560, 360, 3, 'twenty one')], cap=(930, 44, CREAM, "once you've")),
        dict(at='one of the economists', bg=PAPER_C, props=[(D_quote(['"I can\'t think of a good reason', 'to allow this practice', 'in any country."'], 'STEVEN TADELIS, UC BERKELEY', size=78), CX, 520, 1300, 600, 0, None)]),
        dict(at='trick number two', bg=P, chapter=('TRICK 2', 'The resort fee')),
        dict(at='you find a room', bg=PAPER_C, photos=[('room', L, 560, 600, -4, None)], labels=[('RESORT FEE', R_, 380, 80, -3, 'resort fee', RED, (255, 250, 240)),
                                                                                         ('DESTINATION FEE', R_, 540, 70, 3, 'destination'), ('AMENITY FEE', R_, 690, 70, -2, 'amenity')]),
        dict(at='on the las vegas', bg=D, photos=[('vegas', L, 540, 560, -4, None)], props=[(D_text('$44–$57', 150, INK, sub='PER NIGHT, LAS VEGAS STRIP'), R_, 420, 620, 300, 3, 'forty four'),
                                                                                         (D_text('~$33', 150, RED, sub='AVERAGE, 160 HOTELS (NERDWALLET)'), R_, 760, 560, 300, -2, 'thirty three')]),
        dict(at='do the math', bg=PAPER_C, props=[(D_receipt([('3 nights x $99', '$297'), ('Resort fee x 3', '$150')], '$447 + tax'), CX, 540, 560, 420, -2, 'add a fifty')],
             words=[('$99?', 440, 460, 160, (150, 150, 160), 'ninety nine'), ('+$150', 1480, 600, 170, RED, 'a hundred and fifty')]),
        dict(at='hotels say', bg=D, photos=[('lobby', L, 560, 560, -4, None)], words=[('"AN UNDERHANDED WAY', R_, 520, 72, H, 'underhanded'), ('TO RAISE RATES."', R_, 620, 72, H, 'raise rates')],
             cap=(940, 42, CREAM, 'one traveler')),
        dict(at='trick number three', bg=P, chapter=('TRICK 3', 'The sort order')),
        dict(at='before the new rules', bg=PAPER_C, props=[(D_chart([99, 129], ['HIDES $50 FEE', 'HONEST PRICE'], [RED, (200, 190, 210)], title='EXAMPLE: SORTED BY PRICE, WHO LOOKS CHEAPER?', unit=''), CX, 580, 820, 560, 0, 'showed up higher')]),
        dict(at="that's why this trick", bg=D, words=[('LOOK $50', CX, 420, 140, CREAM, 'fifty dollars more'), ('MORE EXPENSIVE.', CX, 580, 140, H, 'more expensive')], cap=(860, 44, CREAM, None)),
        dict(at='trick number four', bg=P, chapter=('TRICK 4', 'The minibar sensor')),
        dict(at='many hotels', bg=PAPER_C, photos=[('minibar', L, 560, 560, -4, None)], words=[('PICK IT UP =', R_, 440, 110, INK, 'pick something'), ('PAY FOR IT.', R_, 580, 120, RED, 'your bill')],
             labels=[('60 SECONDS', R_, 760, 70, -3, 'sixty seconds', H)]),
        dict(at='one reporter', bg=D, props=[(D_receipt([('Minibar', '$6.06'), ('4 more charges', '...'), ('Minibar', '$7.72')], '6 CHARGES'), L, 560, 460, 520, -3, 'six minibar')],
             words=[('ATE NOTHING.', R_, 460, 110, CREAM, "hadn't eaten"), ('"UP TO 90%', R_, 610, 100, H, 'ninety percent'), ('ARE MISTAKES"', R_, 720, 90, H, 'mistakes')]),
        dict(at='and then, the rules', bg=P, chapter=('TRICK 5', 'The law catches up')),
        dict(at='pennsylvania sued', bg=PAPER_C, photos=[('lobby', L, 560, 520, -4, None)], labels=[('PENNSYLVANIA vs MARRIOTT', R_, 420, 66, -3, 'pennsylvania'), ('RESORT FEES IN THE SHOWN PRICE', R_, 560, 56, 3, 'include them', RED, (255, 250, 240))]),
        dict(at='in may', bg=D, props=[(D_text('MAY 12, 2025', 130, INK, sub='FTC: SHOW THE TOTAL PRICE UP FRONT'), CX, 480, 900, 320, -2, None)], cap=(860, 44, CREAM, None)),
        dict(at='but read that', bg=P, words=[("THE FEE DIDN'T GO AWAY.", CX, 420, 110, CREAM, "doesn't ban"), ("IT JUST CAN'T HIDE.", CX, 580, 120, H, "can't hide")]),
        dict(at="so here's how", bg=D, words=[('HOW TO BEAT IT', CX, 500, 150, H, None)]),
        dict(at='compare the total', bg=PAPER_C, labels=[('COMPARE THE WHOLE-STAY TOTAL', CX, 330, 60, -2, 'compare'), ('POINTS STAYS: HILTON & HYATT WAIVE IT', CX, 460, 54, 2, 'hilton'),
                                                         ('SURPRISE FEE? COMPLAIN EARLY', CX, 590, 60, -2, 'complain', RED, (255, 250, 240)), ('QUOTED LOWER? DISPUTE IT', CX, 720, 60, 2, 'dispute')]),
        dict(at='and the minibar', bg=P, photos=[('minibar', L, 560, 520, -4, None)], words=[("DON'T TOUCH IT.", R_, 520, 120, H, "don't touch")]),
        dict(at='the cheapest looking', bg=D, words=[('THE TOTAL', CX, 420, 160, CREAM, 'the total'), ('IS THE PRICE.', CX, 580, 160, H, 'is the price')]),
        dict(at='we break down', bg=PAPER_C, cap=(930, 46, (40, 20, 60), None)),
    ]


S = WideStory(HERE, 'BUSINESS TRICKS', 'EP 03', scenes, ASSETS, cover_at=lambda S: S.ph('do the math') - 0.3)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
