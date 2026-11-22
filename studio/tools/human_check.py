#!/usr/bin/env python3
"""HUMAN check — does the script sound like a person talking, not like AI text? (owner, 6 Nov 2026: "research how to write like a human")
Rules + sources: studio/WRITING.md. Usage: human_check.py <vo_lines.py> [--strict]   exit 1 if a gate fails.
Notes (not gates): stress words that aren't in their line, digits/symbols in spoken text (R&D 7 Nov 2026).
Gates (H1–H6):
  H1 tells      ≤ 1 AI-tell / house-cliché hit per 150 words (Wikipedia "Signs of AI writing"; Kobak 2024; Reinhart 2025 PNAS)
  H2 openers    no single first word opens > 15 % of sentences; But/So/And together ≤ 20 %
  H3 templates  no sentence skeleton (numbers + first 2 words) used > 3 times ("Slice one. … Slice two. …")
  H4 rhythm     sentence-length CV ≥ 0.45; no run of 4 sentences within ±2 words; no sentence > 18 words (Provost; NPR; UF/IFAS)
  H5 talk       contraction rate ≥ 0.9 (NPR; UF/IFAS); ≤ 3 abstract nouns per 100 words; no ", verb-ing …" tail clause (Reinhart 2025)
  H6 person     the narrator has a point of view at least once: an "I"/"I'd"/"me"/"honestly"/"my" line or a plain opinion ("that's wild", "fair?")
Extra gates in --strict (printed separately, so the H-score stays /6):
  LENGTH        estimated voice > 90 s (owner 15 Nov 2026)
  STALL         a 'stall' line in the 3rd line … ~16 s window: a statistic, a named source ("Circana says"), or a date/place/"Meet X"
                opener (R&D 22 Nov 2026: on 4 of 6 posted Shorts-length doodles the average viewer left during exactly that
                trend-stat / "Place, year." block, 9-17 s in — WRITING.md rule 57). Move the trend after the result, put place + year
                on the tape label, start the story on an action.
"""
import re, sys, ast, math, statistics as st

AI_TELLS = [
    "delve", "delves", "underscore", "underscores", "showcase", "showcasing", "crucial", "pivotal", "intricate", "tapestry", "testament",
    "vibrant", "landscape", "foster", "fostering", "garner", "bolster", "interplay", "meticulous", "meticulously", "enhance", "enhancing",
    "additionally", "moreover", "furthermore", "notably", "comprehensive", "valuable insights", "align with", "resonate with", "boasts",
    "nestled", "in the heart of", "groundbreaking", "renowned", "serves as", "stands as", r"plays a (vital|crucial|key|significant) role",
    r"it'?s important to note", "it is worth noting", "in conclusion", "overall,", r"not only .* but also", r"\bit'?s not (just )?\w+[^.]*, it'?s\b",
    r"not just .* but", r"despite (these|the) challenges", "evolving landscape", r"game[- ]changer", r"experts (say|argue)", "studies show",
    "industry reports", r", (highlighting|underscoring|emphasizing|ensuring|reflecting|showcasing|fostering) ",
    # house clichés (our own list: they were in every script)
    "picture this", r"here'?s the catch", r"here'?s why", r"here'?s the thing", r"let'?s dive in", "buckle up", "let that sink in", "ever wondered",
    "imagine this", "the truth is", r"but here'?s", "plot twist", "spoiler", "game changer", "unlock", "secret sauce",
]
EXPANDABLE = [r"\bdo not\b", r"\bdoes not\b", r"\bdid not\b", r"\bis not\b", r"\bare not\b", r"\bwas not\b", r"\bwere not\b", r"\bcannot\b",
              r"\bcan not\b", r"\bwill not\b", r"\bwould not\b", r"\bit is\b", r"\bthat is\b", r"\bthere is\b", r"\byou are\b", r"\bwe are\b",
              r"\bthey are\b", r"\bi am\b", r"\byou will\b", r"\bhave not\b", r"\bhas not\b", r"\bwhat is\b", r"\bhere is\b"]
VOICE = [r"\bi\b", r"\bi'd\b", r"\bi'm\b", r"\bme\b", r"\bmy\b", r"\bhonestly\b", r"\bwild\b", r"\bfair\?", r"\bweird\b", r"\bsneaky\b",
         r"\bclever\b", r"\bkind of\b", r"\bto be fair\b", r"\bi know\b", r"\byeah\b", r"\bnope\b", r"\bokay\b", r"\bseriously\b"]
NUMW = set("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion percent".split())


def load(path):
    src = open(path).read(); tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "LINES" for t in node.targets):
            return [(x[0], x[1]) for x in ast.literal_eval(node.value)]
    raise SystemExit("no LINES in " + path)


def sentences(text):
    parts = re.split(r"(?<=[.!?…])\s+", text.strip())
    return [p for p in parts if re.search(r"[A-Za-z0-9]", p)]


def words(s): return re.findall(r"[A-Za-z0-9$%']+", s)


def skeleton(s):
    w = [x.lower() for x in words(s)]
    w = ["#" if (x in NUMW or re.match(r"^[\d$%,.]+$", x)) else x for x in w]
    return " ".join(w[:2]) + (" #" if "#" in w else "")


AMBIG_CAPS = {"us", "it", "am", "in", "on", "or", "no", "so", "do", "go", "me", "we", "he", "is", "as", "at", "an", "id", "ok", "hi", "who", "can", "con", "sat", "act", "aid", "art", "ban", "bar", "pet", "tax", "via"}


def voice_notes(path):
    """Not gates (R&D 7 Nov 2026, from two fresh-eyes reviews): things the TTS pipeline silently gets wrong.
    stress: a stressed_words entry (field 7, ':dn' suffix allowed) that isn't a token of its line — the emphasis is dropped.
    symbols: digits / $ % £ € & / in spoken text — WRITING rule 19 (spell numbers out)."""
    src = open(path).read(); tree = ast.parse(src); out = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "LINES" for t in node.targets):
            for row in ast.literal_eval(node.value):
                lid, text = row[0], row[1]; norm = lambda w: re.sub(r"\W", "", w.lower()); toks = {norm(w) for w in text.split()} | {norm(w) for w in re.split(r"[\s\-–—]+", text)}
                stress = row[6] if len(row) > 6 and isinstance(row[6], (list, tuple)) else []
                miss = [w for w in stress if norm(w.split(":")[0]) not in toks]   # make_vo.py matches the same way
                if miss: out.append(f"stress {lid}: {miss} not in the line's words (make_vo matches whole words, case/punctuation ignored)")
                sym = re.findall(r"[0-9$%£€&/]", text)
                if sym: out.append(f"symbols {lid}: {''.join(sorted(set(sym)))} in spoken text — spell it out (rule 19)")
                # 8 Nov (fresh-eyes review, cash rewards): an all-caps acronym that is also a word ("US" -> "us") gets read as the word
                amb = [w for w in re.findall(r"\b[A-Z]{2,4}\b", text) if w.lower() in AMBIG_CAPS]
                if amb: out.append(f"caps {lid}: {sorted(set(amb))} can be read as a word ('US' -> 'us') — say 'American' / 'in America', or listen to the take (rule 26)")
                # 9 Nov (fresh-eyes review, childminding): a narrator reaction told as a past discovery ("I didn't see that coming",
                # "when I found out…") gives the narrator a life it doesn't have (rule 15); say it as an opinion or a hypothetical instead
                mem = re.search(r"\bI (didn't|did not|never) (see|expect|know|realise|realize|think)\b|\bI (found out|learned|discovered|remember|used to)\b|\bwhen I\b|\bmy (mum|mom|dad|friend|wife|husband|kids?)\b", text, re.I)
                if mem: out.append(f"memory {lid}: '{mem.group(0)}' reads as the narrator's own past — use a present opinion or a hypothetical ('That's the one I'd have missed.') (rule 15/29)")
                # 12 Nov (fresh-eyes review, overbooking): the narrator is American (usa_narr) -> no British 'and' inside a number
                # ("one thousand and seventy-five"); a year or "a hundred and fifty" said as a round amount is still flagged: listen.
                brit = re.findall(r"\b(?:hundred|thousand|million|billion) and (?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\w+teen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)\b", text, re.I)
                if brit: out.append(f"number {lid}: {brit} — British 'and' inside a number; the American narrator says 'one thousand seventy-five' (rule 39)")
                # 14 Nov (fresh-eyes review, ZIP code): British everyday words in an American narrator's mouth ('at the till' can be heard
                # as 'until'; 'loads of', 'puts it down to'); a UK-set line may keep them — listen. Note only, not a gate.
                ukw = re.findall(r"\b(?:till|tills|loads of|petrol|queue|queues|queueing|fortnight|whilst|trolley|motorway|mobile phone|chemist|put it down to|puts it down to|high street|cashpoint|car park)\b", text, re.I)
                if ukw: out.append(f"british {lid}: {sorted(set(w.lower() for w in ukw))} — the narrator is American: 'register / checkout', 'lots of', 'credits' (rule 42)")
    return out


STALL_STAT = re.compile(r"\b(percent|times (faster|more|bigger)|a record|according to|tracker|survey|study|data shows?)\b|\b[A-Z][A-Za-z]+ (says|said|reports)\b(?! no\b)")
STALL_OPEN = re.compile(r"^(rewind|meet\b|it'?s (nineteen|two thousand|twenty)|in (nineteen|two thousand)|(early|mid|late)[- ](nineteen|twenty|\w+ties)|"
                        r"[A-Z][a-z]+(?: [A-Z][a-z]+)?(?:, [A-Z][a-z]+)?, (nineteen|two thousand|twenty)\w*)|\bmeet [A-Z]", re.I)


def stall_lines(L, window=16.0):
    """R&D 22 Nov 2026 (lab/story/shorts_leak_audit.py): lines that start inside the early window (after the 2 hook lines) and stall the story."""
    out, t = [], 0.0
    for k, (i, txt) in enumerate(L):
        if k >= 2 and t < window:
            why = []
            if STALL_STAT.search(txt) or (re.search(r"\b(grew|grow|grows|rose|jumped|fell|doubled|tripled)\b", txt, re.I)
                                          and any(w.lower() in NUMW or w.lower() == "half" for w in words(txt))):
                why.append("statistic / named source")
            if STALL_OPEN.search(txt.strip()): why.append("date / place / 'Meet X' opener")
            if why: out.append((i, round(t, 1), " + ".join(why), txt))
        t += len(words(txt)) * 0.335 + 0.15
    return out


def main():
    path = sys.argv[1]; strict = "--strict" in sys.argv
    L = load(path); text = " ".join(t for _, t in L); low = text.lower()
    S = [s for _, t in L for s in sentences(t)]; nW = len(words(text)); flags = []; G = {}
    # H1
    hits = []
    for pat in AI_TELLS:
        for m in re.finditer(r"\b" + pat if pat[0].isalpha() else pat, low): hits.append(m.group(0))
    per150 = len(hits) * 150 / max(1, nW)
    G["H1_tells"] = per150 <= 1.0
    if hits: flags.append(f"H1 AI-tell / cliché hits ({per150:.1f} per 150 words): {hits}")
    # H2
    firsts = [words(s)[0].lower() for s in S if words(s)]
    top = max(set(firsts), key=firsts.count); topr = firsts.count(top) / len(firsts)
    bsa = sum(f in ("but", "so", "and") for f in firsts) / len(firsts)
    G["H2_openers"] = topr <= 0.15 and bsa <= 0.20
    if not G["H2_openers"]: flags.append(f"H2 openers: '{top}' opens {topr:.0%} of sentences; But/So/And open {bsa:.0%} (≤ 20 %)")
    # H3
    sk = {}
    for s in S: sk.setdefault(skeleton(s), []).append(s)
    rep = {k: v for k, v in sk.items() if len(v) > 3 and len(k.split()) >= 2}
    G["H3_templates"] = not rep
    for k, v in rep.items(): flags.append(f"H3 template '{k}…' used {len(v)}×: {v[:4]}")
    # H4
    lens = [len(words(s)) for s in S]; cv = st.pstdev(lens) / max(1e-9, st.mean(lens))
    runs = [i for i in range(len(lens) - 3) if max(lens[i:i + 4]) - min(lens[i:i + 4]) <= 2]
    longs = [s for s, n in zip(S, lens) if n > 18]
    G["H4_rhythm"] = cv >= 0.45 and not runs and not longs
    if cv < 0.45: flags.append(f"H4 sentence-length CV {cv:.2f} (≥ 0.45): sentences all the same length")
    if runs: flags.append(f"H4 flat run of 4 same-length sentences from: {S[runs[0]]!r}")
    for s in longs: flags.append(f"H4 > 18 words: {s!r}")
    # H5
    contr = len(re.findall(r"\b\w+'(s|t|re|ll|ve|d|m)\b", low)); full = sum(len(re.findall(p, low)) for p in EXPANDABLE)
    crate = contr / max(1, contr + full)
    absn = [w for w in re.findall(r"[a-z]+", low) if re.search(r"(tion|ment|ness|ity|ance|ence)$", w) and len(w) > 6]
    tails = re.findall(r", \w+ing\b[^.?!]*[.?!]", low)
    tails = [x for x in tails if not re.match(r", (something|anything|nothing|everything|morning|evening|king|thing|spring|bring|during)", x)]
    G["H5_talk"] = crate >= 0.9 and len(absn) * 100 / max(1, nW) <= 3 and not tails
    if crate < 0.9: flags.append(f"H5 contraction rate {crate:.2f} (≥ 0.9): write 'don't', 'it's', 'you're'")
    if len(absn) * 100 / max(1, nW) > 3: flags.append(f"H5 abstract nouns {len(absn)} in {nW} words: {sorted(set(absn))}")
    for x in tails: flags.append(f"H5 trailing '-ing' clause: {x!r}")
    # H6
    vh = [p for p in VOICE if re.search(p, low)]
    G["H6_person"] = bool(vh)
    if not vh: flags.append("H6 the narrator never sounds like a person: add one honest reaction or opinion ('Honestly? That's wild.', 'Fair?')")
    for k, v in G.items(): print(f"{k:14s} {v}")
    print(f"\nstats: {nW} words, {len(S)} sentences, CV {cv:.2f}, contractions {crate:.2f}, tells/150w {per150:.1f}, top opener '{top}' {topr:.0%}, But/So/And {bsa:.0%}")
    for f in flags: print("  - " + f)
    for n in voice_notes(path): print("  note " + n)
    # Shorts length gate (owner 15 Nov 2026: "make it according to shorts") + Chatterbox line limits (16 Nov R&D run)
    est = nW * 0.335 + 0.15 * len(L)         # calibrated 16 Nov on the Febreze Short: 226 words, 20 lines -> 78.7 s real usa_narr VO (story_check 0.40 s/word runs ~15 % long)
    for i, t in L:
        n = len(words(t)); ns = len(sentences(t))
        if n > 14 or ns > 2: print(f"  note line {i}: {n} words / {ns} sentences — Chatterbox can truncate lines over ~14 words or 2 sentences; split it")
    long_fail = est > 90
    print(f"  length ~{est:.0f} s estimated ({nW} words, {len(L)} lines) — Shorts target 50-75 s, hard cap 90 s" + ("  ** OVER THE CAP **" if long_fail else ""))
    stalls = stall_lines(L)
    for i, t0, why, txt in stalls: print(f"  STALL line {i} (~{t0:.0f} s): {why}: {txt!r} — WRITING rule 57: move the trend after the result; place/year on the tape, not spoken first")
    ok = sum(G.values()); print(f"\n{ok}/{len(G)} human-voice gates passed (H1–H6) — studio/WRITING.md" + (f"; STALL gate: {len(stalls)} line(s)" if stalls else "; STALL gate PASS"))
    if stalls and strict and "--stall-ok" not in sys.argv:
        print("STALL GATE FAIL: a stat / source / date-place line in the first ~16 s (rule 57) — reorder; --stall-ok only for an owner-approved exception")
        sys.exit(1)
    if long_fail and strict and "--long-ok" not in sys.argv:
        print("LENGTH GATE FAIL: estimated > 90 s — cut lines (WRITING.md 'Length'); pass --long-ok only for an owner-approved long-form script")
        sys.exit(1)
    sys.exit(0 if ok == len(G) or not strict else 1)


if __name__ == "__main__":
    main()
