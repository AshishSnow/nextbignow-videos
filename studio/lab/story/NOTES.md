# Story lab — R&D run 27 Oct 2026 (focus: Story)

**Hypothesis.** Avg watch is stuck at 13–23 s whatever the length (55–133 s), so the middle leaks. If script structure matters,
measurable features of our own scripts (hook, open loops, turns, connectors, load, roadmap, ending) should line up with the
Instagram retention we already have, and a script that fixes the weak features should be checkable before any audio is made.

**Method.** (1) Research on story structure, curiosity and short-form retention (primary sources, below). (2) Built
`tools/story_check.py` (reads `vo_lines.py`, no audio needed; timings from `work/align.json` or 0.40 s/word, which fits the
27 Oct VOs within ±5 %). (3) Ran it on all 13 example scripts and rank-correlated each metric with the 6 animated reels that have
Instagram rows (Costco, Starbucks #2, Amazon, Chick-fil-A, Planet Fitness, printer ink; real lengths). (4) Re-wrote the newest
script (Monopoly) with the surviving rules and measured before/after.

## Result 1 — what our own data says (n = 6, Spearman rho; small sample, treat as direction only)
| Metric | rho vs avg-watch % of length | rho vs avg watch (s) | rho vs 3-s rate | Verdict |
|---|---|---|---|---|
| item labels ("Step one", "Secret two"…) | **+0.93** | +0.77 | +0.80 | **adopt (R8 roadmap)** |
| count promised up front ("four secrets") | +0.41 | +0.62 | +0.83 | part of R8 |
| hook words | +0.77 | +0.71 | +0.37 | no rule (long hooks were not punished; likely confounded) |
| max gap without a question/teaser/turn | −0.09 | −0.31 | −0.20 | right direction, weak → R2 at 25 s |
| reversal words per minute ("but/yet/only…") | −0.60 | −0.37 | −0.83 | **not a gate** (keyword proxy ≠ real reversals) |
| causal openers % ("But/So/Because…") | −0.72 | −0.81 | −0.75 | **not a gate**; only ban "and then" chains |
| figures per sentence | +0.09 | −0.15 | −0.35 | keep as load hygiene (research), not data-backed |
| twist → end seconds | −0.31 | −0.09 | +0.14 | R7 ≤ 18 s |

Roadmap split (R8): Costco 34 %, Starbucks 31 %, Planet Fitness 30 %, printer ink 29 % (+ restaurant tricks 33 %, script not in
repo: "4 tricks… #4 is the sneakiest") vs Amazon 19 %, Chick-fil-A 24 % — perfect separation. Not just topic type: Starbucks and
Planet Fitness are type F and still held 30–31 %. Caveat: labels also correlate with the 3-s rate, which they can't cause → part
of this is "better videos overall". **The autopilot drifted away from roadmaps exactly when the stats froze:** Visa, Duolingo, gas
station, airline miles and Monopoly have none (only De Beers and popcorn do) → falsifiable prediction in PERFORMANCE.md insight K.

## Result 2 — before/after on the same material (Monopoly, same facts)
| | rules passed | max gap | twist→end | figures/sentence > 1 | roadmap |
|---|---|---|---|---|---|
| shipped script (`examples/monopoly`) | 4/7 | 38 s (46–84 s: "the game escaped… Darrow got rich") | 22 s | 0 | no |
| `monopoly_v2_vo_lines.py` | **6/7** | 25 s | 17 s | 0 | **"three moves… the last one is the cruelest"**, Move one/two/three |
Edits: count promise in i3, labels at a1/c1/d1, "But here's the clever part" (b1), "But…" at c3/f1, teaser "So what did Lizzie
get?" before move three, c6 split to one figure per sentence, loop line before the takeaway, shorter takeaway. +3 s (136 s est.).
Real validation = retention of the next videos (roadmap vs none), not this tool's score.

## Research (dated; S strong, M moderate, W weak)
- Curiosity gap → reward + willingness to wait for the answer + better memory: Kang et al. 2009, Psychological Science (S);
  Loewenstein 1994 (theory, M). **Zeigarnik "unfinished tasks are remembered better" does not replicate** (Ghibellini & Meier 2025
  meta-analysis, HSS Communications 12:962, ratio 0.99) — justify open loops with curiosity, not Zeigarnik.
- Suspense/surprise model: keep uncertainty high, twists larger and rarer, resolve at the end (Ely, Frankel & Kamenica 2015, JPE; theory).
- Emotional volatility (alternating good/bad beats) raises liking and continued reading — reordering the same scenes so they
  alternate raised liking 3.41 → 4.01 (7-pt scale) (Berger, Kim & Meyer 2021, JCR 48(2), S); narrative reversals predict success in ~32.8k stories
  (Knight, Rocklage & Bart 2024, Science Advances, S, correlational). Our keyword proxy for this did NOT track retention → write
  real good/bad swings, don't sprinkle "but".
- Story speed (semantic distance between chunks) helps films/TV, small effect (Toubia, Berger & Eliashberg 2021, PNAS) → no recaps.
- Causally linked events are recalled and rated more important (Trabasso & van den Broek 1985; Fletcher & Bloom 1988) — the
  "but/therefore, never and-then" rule (Parker & Stone, NYU 2011) is a craft rule, untested on retention.
- Limited capacity (Lang 2000 LC4MP; Fox, Park & Lang 2007): dense audio + complex visuals overload memory → one figure per sentence.
- Sharing: awe/anger/anxiety and practical value raise sharing, sadness lowers it (Berger & Milkman 2012, JMR, S).
  Questions in brand posts lift comments (de Vries et al. 2012, M); no study on "A or B?" in video (W).
- Platforms: no ideal Shorts length (YouTube: "as long as it needs to be"); since 31 Mar 2025 every start/replay is a view,
  engaged views separate; Instagram top signals watch time, likes, sends per reach (Mosseri, Jan 2025).
- MrBeast production handbook (leaked Sep 2024, long-form, W–M): show don't announce, no dull moments, strong payoff at the end,
  "don't ever signal the end".
- Myths: the "8-second / goldfish attention span" (Microsoft Canada 2015 deck, no study — BBC More or Less 2017); "start slow then
  speed up" is not what the PNAS paper found; no universal ideal Shorts length.

Sources: https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/How-Quantifying-the-Shapes-of-Stories-Predicts-their-Success.pdf ·
https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/Emotional-Volatility-1.pdf ·
https://www.psypost.org/this-simple-narrative-element-can-predict-a-storys-popularity-study-finds/ ·
https://neuroecon.berkeley.edu/papers/papers_files/Kang_PsychSci_2009.html · https://www.nature.com/articles/s41599-025-05000-w.pdf ·
https://www.wiwi.uni-bonn.de/kraehmer/Lehre/TopicsSS14/ElyEtAl-SurpriseSuspense.pdf · https://www.cl.cam.ac.uk/teaching/1516/R216/Fletcher.pdf ·
https://faculty.wharton.upenn.edu/wp-content/uploads/2011/11/Virality.pdf · https://support.google.com/youtube/answer/15424877 ·
https://www.tubefilter.com/2025/03/26/youtube-shorts-views-counting-stats/ · https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf ·
https://scienceblog.com/t-humans-eight-second-attention-span-goldfish-myth/

## Next
- When Metricool rows return: tag every post roadmap yes/no and re-run `python3 lab/story/corr.py` (add the rows to its `D` table) with n ≥ 10; drop R8 if the gap closes.
- Real reversal detection (good/bad polarity per line) instead of keywords — e.g. a tiny sentiment lexicon, or hand-tag `+`/`−`.
- Two-part story + choice CTA (owner's references) — needs comment data to judge.
