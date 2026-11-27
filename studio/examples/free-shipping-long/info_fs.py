"""BUSINESS TRICKS · EP 02 (YouTube 16:9) — Free shipping isn't free; buy now, pay later. PAPER wide look."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
os.environ.setdefault('OMB_WIDE', '1')
from wide_props import *

ASSETS = {'boxes': ('boxes.bin',)}
RED = (232, 70, 60); BLU = (70, 130, 220)
L, R_, CX = 600, 1340, 960


def scenes(S):
    P, D, H = S.PAPER, S.DARK, S.HERO
    return [
        dict(at=0.0, bg=PAPER_C, props=[(D_phone('checkout', accent=RED, label=[('SUBTOTAL', '$28.00'), ('SHIPPING', '$6.00'), ('FREE OVER', '$35.00')]), L, 560, 330, 640, -4, 0.0)],
             words=[('+9%', R_, 520, 260, RED, 'nine percent')], cap=(930, 50, INK, 'harvard')),
        dict(at='harvard', bg=P, photos=[('boxes', R_, 560, 600, 4, None)], props=[(D_text('2M+', 200, INK, sub='ORDERS STUDIED'), L, 540, 560, 360, -3, 'two million')],
             cap=(950, 46, CREAM, None)),
        dict(at="free shipping isn't free", bg=D, words=[("FREE SHIPPING", CX, 400, 150, CREAM, None), ("ISN'T FREE.", CX, 560, 170, H, "isn't free")], shake="isn't free",
             cap=(900, 46, CREAM, None)),
        dict(at='one is the free', bg=P, labels=[('TRICK: THE LINE', L, 520, 80, -3, 'the free shipping line', H), ('TRICK: 4 EASY PAYMENTS', R_, 560, 80, 3, 'four easy')]),
        dict(at="let's start", bg=D, chapter=('TRICK 1', 'The free-shipping line')),
        dict(at="you're buying", bg=PAPER_C, props=[(D_receipt([('Item', '$28.00'), ('Shipping', '$6.00')], '$34.00'), L, 560, 460, 360, -3, None),
                                                   (D_receipt([('Item', '$28.00'), ('+ one more thing', '$9.00'), ('Shipping', 'FREE')], '$37.00'), R_, 560, 460, 420, 3, 'add one more')]),
        dict(at='lots of people', bg=P, words=[('THEY OVERSHOOT.', CX, 420, 150, H, 'overshoot')], cap=(860, 46, CREAM, None)),
        dict(at='and the store wins', bg=PAPER_C, props=[(D_chart([100, 93.6], ['NO MINIMUM', 'WITH MINIMUM'], [(200, 190, 210), RED], title='NUMBER OF ORDERS', source='Ngwe & Chen, HBS'), L, 560, 640, 560, -2, 'six percent'),
                                                         (D_text('PROFIT ↑', 140, RED, sub='BIGGER BASKETS'), R_, 520, 560, 300, 3, 'profit')], cap=(990, 40, INK, None)),
        dict(at='trick number two', bg=D, chapter=('TRICK 2', 'Move the line')),
        dict(at='in twenty thirteen', bg=PAPER_C, props=[(D_beforeafter([('2013', '$25', '$35'), ('2016 (no Prime)', '$35', '$49')], head=('FREE SHIPPING MINIMUM', 'RAISED TO')), CX, 520, 1000, 360, 0, None)],
             labels=[('PRIME: $99/YR, NO MINIMUM', CX, 820, 60, -2, 'ninety nine', RED, (255, 250, 240))]),
        dict(at='the message was', bg=P, words=[('STOP DOING THE MATH.', CX, 420, 120, CREAM, 'stop doing'), ('JUST JOIN.', CX, 580, 150, H, 'just join')], shake='just join'),
        dict(at='trick number three', bg=D, chapter=('TRICK 3', 'The membership')),
        dict(at="once you've", bg=P, photos=[('boxes', L, 560, 560, -4, None)], words=[('EVERY ORDER', R_, 460, 100, CREAM, 'every order'), ('FEELS FREE.', R_, 590, 110, H, 'feels free')]),
        dict(at='one research firm', bg=PAPER_C, props=[(D_chart([700, 1300], ['NON-MEMBERS', 'PRIME MEMBERS'], [(200, 190, 210), RED], title='SPENT ON AMAZON PER YEAR ($)', source='CIRP estimate, 2017'), CX, 580, 820, 560, 0, 'thirteen hundred')]),
        dict(at="that's the shipping", bg=D, props=[(D_text('$200', 180, INK, sub='THE JACKET'), L, 540, 520, 320, -3, 'two hundred'),
                                                    (D_text('4 x $50', 160, RED, sub='HOW IT FEELS'), R_, 540, 560, 320, 3, 'fifty dollar')], cap=(900, 46, CREAM, None)),
        dict(at='pay in four', bg=P, chapter=('TRICK 4', 'Pay in four')),
        dict(at='no interest', bg=PAPER_C, props=[(D_phone('checkout', accent=(160, 92, 240), label=[('JACKET', '$200'), ('PAY IN 4', '$50'), ('INTEREST', '$0')]), L, 560, 330, 640, -4, None)], words=[('WHO PAYS?', R_, 420, 120, RED, "who's paying"), ('THE STORE.', R_, 560, 120, INK, 'the store is')],
             labels=[('UP TO 3x A CARD FEE', R_, 740, 60, -3, 'three times', RED, (255, 250, 240))]),
        dict(at='so why would', bg=D, props=[(D_text('+14%', 220, INK, sub='REVENUE (UP TO), STRIPE TEST, 150K+ CHECKOUTS'), L, 540, 720, 380, -3, 'fourteen percent'),
                                             (D_text('2/3', 220, RED, sub='OF PAY-LATER SPENDING WAS NEW'), R_, 560, 600, 380, 3, 'two thirds')]),
        dict(at='trick number five', bg=P, chapter=('TRICK 5', 'Future you pays')),
        dict(at='in a lendingtree', bg=PAPER_C, props=[(D_text('~70%', 190, INK, sub='SPEND MORE THAN IF PAYING UP FRONT'), 420, 540, 560, 340, -3, 'seventy percent'),
                                                       (D_text('42%', 190, RED, sub='PAID LATE AT LEAST ONCE'), 960, 560, 520, 340, 2, 'forty two'),
                                                       (D_text('55%', 190, INK, sub='"ONLY WAY I COULD AFFORD IT"'), 1500, 540, 560, 340, -2, 'only way')], cap=(960, 40, INK, None)),
        dict(at='the federal reserve also', bg=D, props=[(D_chart([0.54, 1.82], ['NON-USERS', 'PAY-LATER USERS'], [(200, 190, 210), RED], title='ACCOUNTS LATE OR IN COLLECTIONS (AVG)', source='Federal Reserve, 2024'), CX, 560, 820, 560, 0, 'three times')],
             cap=(990, 40, CREAM, None)),
        dict(at='so what do you do', bg=P, words=[('PLAY THE GAME', CX, 440, 140, CREAM, None), ('BETTER.', CX, 600, 160, H, 'better')]),
        dict(at="when you're short", bg=PAPER_C, labels=[('ONLY ADD WHAT YOU WERE BUYING ANYWAY', CX, 360, 58, -2, 'only add'), ('OR JUST PAY THE SHIPPING', CX, 500, 64, 2, 'pay the shipping', RED, (255, 250, 240)),
                                                         ('CHECK YOUR MEMBERSHIP ONCE A YEAR', CX, 660, 58, -2, 'once a year'), ('PAY IN 4 = A LOAN', CX, 800, 70, 2, 'a loan', H)]),
        dict(at='free shipping and four', bg=D, photos=[('boxes', L, 560, 520, -4, None)], words=[('A DEAL FOR THE', R_, 460, 90, CREAM, 'deal for the'), ('STORE FIRST.', R_, 580, 110, H, 'store first')]),
        dict(at='we break down', bg=PAPER_C, cap=(930, 46, (40, 20, 60), None)),
    ]


S = WideStory(HERE, 'BUSINESS TRICKS', 'EP 02', scenes, ASSETS, cover_at=lambda S: S.ph("isn't free") + 0.6)
SCENES, DUR, END, ph = S.SCENES, S.DUR, S.END, S.ph
if __name__ == '__main__': S.run()
