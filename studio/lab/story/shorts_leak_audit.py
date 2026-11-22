#!/usr/bin/env python3
"""R&D 22 Nov 2026 — where does the average viewer leave a Shorts-length doodle?
Estimates each line's start (0.335 s/word + 0.15 s + pause, human_check calibration) and finds the line playing at the
IG average watch time (Metricool IGRE24, pulled 22 Nov ~08:15 IST). Result: 4 of 6 leave during (Vinted earlier, at its abstract hook; Febreze later) the trend stat (a1) or the
'Place, year.' line (b1). Caveat: avg watch is a mean, not the retention curve; n = 6. Run from studio/."""
import ast, re
DATA = {  # IG views, avg watch s, 3-s %
    'febreze-cats-doodle': (155, 27.958, 40.3), 'liquid-death-doodle': (147, 14.48, 56.4), 'hoka-clown-doodle': (271, 15.075, 60.7),
    'sriracha-doodle': (165, 12.36, 60.1), 'vinted-closet-doodle': (625, 5.963, 31.0), 'yankee-candle-doodle': (143, 14.19, 59.8)}
W = lambda s: re.findall(r"[A-Za-z0-9$%']+", s)
for d, (v, aw, r3) in DATA.items():
    tree = ast.parse(open(f'examples/{d}/vo_lines.py').read())
    L = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(getattr(t, 'id', '') == 'LINES' for t in n.targets))
    t, at, marks = 0.0, '?', []
    for x in L:
        dur = len(W(x[1])) * 0.335 + 0.15 + x[3]
        if t <= aw < t + dur: at = f"{x[0]} {x[1]!r}"
        if x[0] in ('a1', 'b1'): marks.append(f"{x[0]}@{t:.1f}s")
        t += dur
    print(f"{d:22s} ~{t:.0f}s avg {aw:5.1f}s 3s {r3:4.1f}% views {v:4d} | {' '.join(marks)} | leave during {at}")
