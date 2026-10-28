#!/usr/bin/env python3
"""Story check — measure a script's structure before any audio or video is made.

Usage:
  python3 studio/tools/story_check.py <project_or_vo_lines.py> [--len SECONDS] [--json]
  python3 studio/tools/story_check.py --all studio/examples        # table for every example script

Reads LINES from scripts/vo_lines.py (same tuple format as the template). If the project has work/align.json, real line
times are used; otherwise times are estimated (0.40 s per word incl. pauses — fits the 27 Oct VOs within ±5 %:
gas 80.6 s, airline 100.9 s, De Beers 117.7 s, Monopoly 133 s) and scaled to --len if given.

Rules (7 gates; evidence + our own data in lab/story/NOTES.md and PLAYBOOK §4 "Story rules"; R&D Story run 27 Oct 2026):
  R1 hook      i1 ≤ 16 words and a question; the core claim (number or question) lands by ~6.5 s
  R2 loops     a question / teaser / turn / item label at least every 25 s — curiosity gaps (Loewenstein 1994; Kang 2009)
  R4 causal    no "and then" chains (≤ 1 "and then"/"then" opener) — causal links are recalled better (Trabasso & van den Broek 1985)
  R5 load      ≤ 1 figure per sentence, ≤ 18 words per sentence (spoken load, Lang LC4MP — thresholds are heuristics)
  R6 novelty   no recap lines (content-word overlap with the previous 2 lines ≤ 0.5) — "speed" (Toubia, Berger & Eliashberg 2021)
  R7 ending    usable takeaway, CTA names a specific friend, ≤ 18 s from the twist line (first t* line) to the end
  R8 roadmap   a count promised in the first 4 lines ("…in three moves") or ≥ 2 labelled items ("Move one…") — OUR DATA:
               the 4 scripts with one held 29–34 % of their length on Instagram, the 2 without 19–24 % (n = 6, 25–26 Oct;
               item labels rho +0.93 with avg-watch %). Small sample — re-test as rows return (PERFORMANCE insight K).
Info only (not gates — our n = 6 data ran the other way): turns_per_min (rho −0.60), causal_openers_pct (rho −0.72).
"""
import json, os, re, runpy, sys

SEC_PER_WORD = 0.40
NUMW = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
           "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion trillion "
           "point percent half quarter oh dozen cents cent dollars dollar pounds".split())
NUM_CORE = NUMW - {"point", "percent", "cents", "cent", "dollars", "dollar", "pounds", "oh"}
TURN_RE = re.compile(r"\b(but|yet|instead|until|except|however|turns out|actually|still|only|never|even|wrong|backfire\w*|flipped|twist|isn't|wasn't|real)\b", re.I)
TEASE_RE = re.compile(r"(\?|here's|guess|wait|the twist|sneakiest|the real|what happened|the catch|watch|the problem|plot twist|that's when|here are|the last one|(secret|trick|step|reason|rule|move|door|layer) (one|two|three|four|five))", re.I)
CAUSAL_START = re.compile(r"^(but|so|because|that's why|which means|therefore|yet|instead|until|except|still|now|except)\b", re.I)
ANDTHEN_START = re.compile(r"^(and then|then|next|after that)\b", re.I)
LABEL_RE = re.compile(r"^(and\s+)?(step|secret|trick|move|reason|rule|trap|clue|mistake|moment|lie|door|layer)\s+(one|two|three|four|five|\d)\b", re.I)
STOP = set("the a an and or but so of to in on at for with is was are were be it its it's this that he she they you your we our his her "
           "their them as by from not no do did does just than then there here what who how why when which one".split())


def load_lines(path):
    if os.path.isdir(path):
        for c in ("scripts/vo_lines.py", "vo_lines.py"):
            if os.path.exists(os.path.join(path, c)):
                return load_lines(os.path.join(path, c))
        raise SystemExit(f"no vo_lines.py in {path}")
    return runpy.run_path(path)["LINES"], os.path.dirname(os.path.dirname(os.path.abspath(path)))


def words(t):
    return re.findall(r"[A-Za-z0-9$£€%']+", t.replace("-", " "))


def count_numbers(sentence):
    """Count number expressions: a run of number words / digits counts once."""
    n, inrun = 0, False
    W = words(sentence.lower())
    for k, w in enumerate(W):
        nxt = W[k + 1] if k + 1 < len(W) else ""
        isnum = w.strip("$£€%").replace(",", "").replace(".", "").isdigit() or w in NUM_CORE
        prv = W[k - 1] if k else ""
        if w == "one" and not inrun and not (nxt in NUMW or nxt in ("in", "of")):
            isnum = False          # "the crushing one" → pronoun, not a figure
        if prv in ("year", "day", "week", "month", "step", "secret", "trick", "move", "part", "number", "round", "level"):
            isnum = False          # "in year two", "move three" → a label, not a figure
        if isnum and not inrun:
            n += 1
        inrun = isnum or (inrun and (w in ("point", "and", "a", "oh", "percent", "cents", "dollars")
                                     or (w in ("in", "out", "of") and nxt in NUM_CORE)))   # "four in ten" = one figure
    return n


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.?!…])\s+", t) if len(words(s)) > 0]


def content(t):
    return {w.lower().strip("'") for w in words(t) if w.lower() not in STOP and w.lower() not in NUMW and len(w) > 2}


def timeline(lines, proj, target_len):
    al = os.path.join(proj, "work", "align.json") if proj else ""
    if al and os.path.exists(al):
        try:
            A = json.load(open(al))
            seg = A.get("lines") or A.get("segments") or {}
            if isinstance(seg, dict) and all(l[0] in seg for l in lines):
                return [(seg[l[0]]["start"], seg[l[0]]["end"]) for l in lines], "align.json"
        except Exception:
            pass
    t, out = 0.0, []
    for l in lines:
        d = len(words(l[1])) * SEC_PER_WORD
        out.append((t, t + d))
        t += d
    if target_len:
        k = target_len / t
        out = [(a * k, b * k) for a, b in out]
    return out, "estimated"


def check(path, target_len=None):
    lines, proj = load_lines(path)
    tl, src = timeline(lines, proj, target_len)
    total = tl[-1][1]
    R, flags = {}, []

    # R1 hook
    i1 = lines[0][1]
    hw = len(words(i1))
    hook_q = i1.strip().endswith("?")
    hook_num = count_numbers(i1) > 0
    # time to the core claim: end of the first line containing a number or the hook question
    claim_t = next((tl[k][1] for k, l in enumerate(lines[:3]) if count_numbers(l[1]) or "?" in l[1]), tl[0][1])
    R["hook_words"] = hw
    R["hook_question"] = hook_q
    R["hook_number"] = hook_num
    R["claim_by_s"] = round(claim_t, 1)
    R["R1_hook"] = hw <= 16 and hook_q and claim_t <= 6.5
    if hw > 16: flags.append(f"R1 hook is {hw} words (≤ 16): {i1!r}")
    if claim_t > 6.5: flags.append(f"R1 core claim lands at {claim_t:.1f} s (≤ 6.5)")
    if not hook_q: flags.append("R1 hook is not a question")

    # R2 loops: events = questions/teasers/turn markers; gap measured between event line starts (and from 0 / to end)
    ev = [tl[k][0] for k, l in enumerate(lines) if TEASE_RE.search(l[1]) or TURN_RE.search(l[1]) or LABEL_RE.match(l[1].strip())]
    pts = [0.0] + ev + [total]
    gaps = [(b - a, a) for a, b in zip(pts, pts[1:])]
    mg, at = max(gaps)
    R["loop_events"] = len(ev)
    R["max_gap_s"] = round(mg, 1)
    R["gaps_over_20s"] = sum(1 for g, _ in gaps if g > 20)
    R["R2_loops"] = mg <= 25
    if mg > 25: flags.append(f"R2 {mg:.0f} s with no question/teaser/turn starting at ~{at:.0f} s")

    # R3 turns per minute
    turns = sum(len(TURN_RE.findall(l[1])) for l in lines)
    R["turns_per_min"] = round(turns / (total / 60), 2)
    R["info_turns_ok"] = R["turns_per_min"] >= 3   # info only: NOT a gate (our n=6 data: rho −0.60 with avg-watch %)

    # R4 causal openers
    beat = [l for l in lines if not l[0].startswith(("i", "e"))]
    starts = [re.sub(r"^[\"'(]+", "", l[1]).strip() for l in beat]
    causal = sum(1 for s in starts if CAUSAL_START.match(s))
    andthen = [l[0] for l, s in zip(beat, starts) if ANDTHEN_START.match(s) or s.lower().startswith("and then")]
    R["causal_openers_pct"] = round(100 * causal / max(1, len(beat)))
    R["and_then"] = len(andthen)
    R["R4_causal"] = len(andthen) <= 1      # gate = no "and then" chains; causal_openers_pct itself is info only
    if len(andthen) > 1: flags.append(f"R4 'and then'-style openers: {andthen}")

    # R5 load
    S = [(l[0], s) for l in lines for s in sentences(l[1])]
    wps = [len(words(s)) for _, s in S]
    multi = [(i, s) for i, s in S if count_numbers(s) >= 2]
    longs = [(i, s) for i, s in S if len(words(s)) > 18]
    R["words_per_sentence"] = round(sum(wps) / len(wps), 1)
    R["max_sentence_words"] = max(wps)
    R["multi_number_sentences"] = len(multi)
    R["long_sentences"] = len(longs)
    R["R5_load"] = not multi and not longs
    for i, s in multi: flags.append(f"R5 {i}: {count_numbers(s)} numbers in one sentence: {s!r}")
    for i, s in longs: flags.append(f"R5 {i}: {len(words(s))} words: {s!r}")

    # R6 novelty
    rec = []
    for k in range(1, len(lines)):
        c = content(lines[k][1])
        prev = content(" ".join(l[1] for l in lines[max(0, k - 2):k]))
        if len(c) >= 3:
            ov = len(c & prev) / len(c)
            if ov > 0.5 and not lines[k][0].startswith(("e", "t")):
                rec.append((lines[k][0], round(ov, 2)))
    R["recap_lines"] = len(rec)
    R["R6_novelty"] = not rec
    for i, ov in rec: flags.append(f"R6 {i} repeats {int(ov*100)} % of the previous lines' content words")

    # R7 ending
    low = [l[1].lower() for l in lines]
    take = any(("takeaway" in x or re.search(r"\b(next time|check|round|ask|look|try|pay|compare|read)\b", x)) for x in low[-5:])
    cta = any("send this to" in x and "who" in x for x in low[-2:])
    twist_k = next((k for k, l in enumerate(lines) if l[0].startswith("t")), max(0, len(lines) - 3))
    tail = total - tl[twist_k][0]
    comment_q = any("?" in l[1] and "send this" not in l[1].lower() and "takeaway?" not in l[1].lower() for l in lines[-3:])
    R["takeaway"] = take
    R["cta_friend"] = cta
    R["comment_prompt"] = comment_q
    R["twist_to_end_s"] = round(tail, 1)
    R["R7_ending"] = take and cta and tail <= 18
    if tail > 18: flags.append(f"R7 {tail:.0f} s from the twist line to the end (≤ 18)")
    if not take: flags.append("R7 no usable takeaway in the last 5 lines")
    if not cta: flags.append("R7 CTA doesn't name a specific friend ('Send this to the friend who…')")

    # R8 roadmap: an explicit count promise in the first 4 lines ("four secrets", "in three moves") or labelled items
    # ("Step one", "Secret one") — 27 Oct data: roadmap scripts held 29–34 % of their length on Instagram (Costco, printer
    # ink, Planet Fitness, Starbucks, + restaurant tricks), the two without one 19–24 % (Amazon, Chick-fil-A)
    head = " ".join(l[1] for l in lines[:4]).lower()
    count_promise = bool(re.search(r"\b(two|three|four|five|seven|\d)\s+(\w+\s+)?(secrets|steps|tricks|moves|reasons|rules|traps|things|mistakes|moments|clues|lies|times|doors|layers)\b", head))
    labels = sum(1 for l in lines if LABEL_RE.match(l[1].strip()))
    R["count_promise"] = count_promise
    R["item_labels"] = labels
    R["R8_roadmap"] = count_promise or labels >= 2
    if not R["R8_roadmap"]:
        flags.append("R8 no roadmap: promise a count up front ('…in three moves', 'four secrets, the last one is the wildest') and label the items")

    R["length_s"] = round(total, 1)
    R["timing"] = src
    R["rules_passed"] = sum(1 for k, v in R.items() if k.startswith("R") and k[1].isdigit() and v)
    return R, flags


def main():
    a = sys.argv[1:]
    js = "--json" in a
    a = [x for x in a if x != "--json"]
    L = None
    if "--len" in a:
        i = a.index("--len"); L = float(a[i + 1]); del a[i:i + 2]
    if a and a[0] == "--all":
        root = a[1]
        rows = {}
        for d in sorted(os.listdir(root)):
            p = os.path.join(root, d)
            if os.path.isdir(p) and os.path.exists(os.path.join(p, "vo_lines.py")):
                rows[d] = check(os.path.join(p, "vo_lines.py"))[0]
        if js:
            print(json.dumps(rows, indent=1)); return
        cols = ["length_s", "hook_words", "claim_by_s", "max_gap_s", "turns_per_min", "causal_openers_pct", "and_then",
                "words_per_sentence", "multi_number_sentences", "long_sentences", "recap_lines", "twist_to_end_s", "rules_passed"]
        print("script".ljust(15) + " ".join(c[:9].rjust(9) for c in cols))
        for d, r in rows.items():
            print(d[:14].ljust(15) + " ".join(str(r[c]).rjust(9) for c in cols))
        return
    R, flags = check(a[0], L)
    if js:
        print(json.dumps({"metrics": R, "flags": flags}, indent=1)); return
    for k, v in R.items():
        print(f"{k:24s} {v}")
    print(f"\n{R['rules_passed']}/7 story rules passed (R1 R2 R4 R5 R6 R7 R8)")
    for f in flags:
        print(" -", f)


if __name__ == "__main__":
    main()
