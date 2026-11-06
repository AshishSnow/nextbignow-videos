# WRITING.md — write like a person talking (owner, 6 Nov 2026: "research how to write like a human")

Every script passes `python3 studio/tools/human_check.py <vo_lines.py> --strict` (6/6 gates) **before** `make_vo.py`, on top of
story_check (R/S gates). The first credit-score script (shipped 6 Nov) scored **1/6**: it had perfect contractions and varied sentence
length, and still sounded like AI because of *templates* ("Slice one. … Slice two. …"), *stock signposts* ("Picture this", "here's the
catch", "here's why"), *forced connectors* (27 % of sentences opened with But/So/And) and *no person behind the voice*.

## The rules (source in brackets; strength noted)
1. **Talk, don't write.** Write it the way you'd tell a friend at a table, then cut it in half. Plain words: "now", not "at this point";
   "because", not "due to". (Zinsser, *On Writing Well*)
2. **One idea per sentence, ≤ 18 words**, so the narrator can breathe. (NPR script tips 2023; UF/IFAS writing for broadcast)
3. **Make the rhythm uneven on purpose.** Fragments next to a longer line. Never four sentences of the same length in a row. (Gary Provost)
4. **Contractions always**: don't, it's, you're, won't. (NPR; UF/IFAS)
5. **Source first, claim second**: "Experian says your card can look maxed out." Not "…, Experian says." (UF/IFAS)
6. **No appositives.** "FICO, a major credit score, doesn't…" becomes "FICO's one of the big scores. And it skips your pay." (UF/IFAS)
7. **Verbs over abstract nouns.** "how much of your card you use", not "utilization". (Reinhart et al., PNAS 2025: LLMs use them 1.5–2× more)
8. **No ", highlighting / ensuring / reflecting …" tail clauses.** (Reinhart 2025: 2–5× more frequent in LLM text; Wikipedia "Signs of AI writing")
9. **Ration the contrasts**: at most one "it's not X, it's Y" per script. **No reflex lists of three**: use two, four, or the real number. (Wikipedia guide via summaries)
10. **No recap or "overall" lines.** (Wikipedia guide; already story rule R6)
11. **Name who said it.** Never "experts say" / "studies show". (Wikipedia guide)
12. **Kill the stock signposts**: picture this, here's the catch, here's why, here's the thing, let's dive in, buckle up, let that sink in,
    ever wondered, plot twist, the truth is. Find the real turn instead ("Except it's not."; "Then the bill comes."). (our own list — they were in every script)
13. **Vary the openers.** No one first word on > 15 % of sentences; But/So/And together ≤ 20 %. Most turns don't need a connector at all.
14. **Never repeat a sentence skeleton more than 3 times.** Count-downs ("Slice one… Slice two…") are fine as *pictures* (the pill says SLICE 2 OF 5);
    the voice says something different each time ("Next: how many cards you've opened lately.").
15. **A person is talking.** At least one honest reaction or opinion per script — "Honestly? That's wild.", "Fair?", "I'd check mine tonight." —
    never a fake personal story or a fake memory (no "when I bought my car…": the narrator has no life). (creator practice; owner's brief)
16. **Hook = the payoff's promise, paid quickly.** The "Do you know…?" question must be answered inside the video and the answer must
    surprise. (Jenny Hoyos via vidIQ — creator advice, not research; MrBeast production memo)
17. **Say it in fewer words, not faster.** Pause after a dense number. Target 165–180 wpm. (Hoyos; VOICE.md research)
18. **Picture = words.** Draw exactly what the voice says at that moment: people remember more of the audio when the picture repeats it.
    (Drew & Grimes 1987, TV-news recall)
19. **For our TTS**: spell numbers out ("twenty-four", "thirty-five percent"), no symbols or unexplained acronyms, "dot com" for URLs; a full
    stop is the most reliable pause; listen to any "…" line before keeping it. (ElevenLabs docs on numbers/pauses apply to any TTS; VOICE.md)
20. **Round numbers** unless the exact figure is the point ("about one in five"). (UF/IFAS)
21. **Read it aloud, then read it again over the narrator.** Keep what sounds like you talking; cut what sounds like a brochure. (NPR)

## Before → after (from the 6 Nov credit script; facts unchanged)
- "But FICO, a major credit score, doesn't count your pay, your job or your age." → "FICO's one of the big credit scores. And it skips your pay. Your job too. Even how old you are."
- "But card companies usually report your balance when each monthly statement ends. That can be before you pay." → "Your card company usually reports your balance the day your statement closes. Sometimes that's before you've paid it."
- "So Experian says your card can look heavily used, even when you pay in full." → "Experian says that can make your card look heavily used. Even when you pay in full."
- "Slice two. Your mix of cards and loans. Ten percent again." → "Next: the mix. Cards, a car loan, maybe a mortgage. Another ten percent."

## The checker (`tools/human_check.py`)
H1 tells ≤ 1 per 150 words · H2 openers (top ≤ 15 %, But/So/And ≤ 20 %) · H3 no skeleton > 3× · H4 sentence-length CV ≥ 0.45, no flat run of 4,
nothing > 18 words · H5 contractions ≥ 0.9, abstract nouns ≤ 3 per 100 words, no "-ing" tails · H6 one human reaction. Thresholds are style
heuristics, not AI detectors (GPTZero itself dropped "burstiness" as a detection signal in 2023): a script can pass and still sound stiff —
**the read-aloud test (rule 21) is the real gate.** Wikipedia's editors stress that one tell proves nothing; clusters do.

## Sources
Wikipedia: Signs of AI writing (WikiProject AI Cleanup) · Kobak et al. 2024, arXiv 2406.07016 (excess vocabulary) · Reinhart et al., PNAS 2025
(CMU news release) · GPTZero help: burstiness/perplexity · Gary Provost, "This sentence has five words" · Zinsser, *On Writing Well* ("Clutter") ·
NPR, "7 tips for writing a script" (17 Feb 2023) · UF/IFAS EDIS WC193, writing for broadcast · Jenny Hoyos via vidIQ · MrBeast production memo
(Simon Willison excerpts, Sep 2024) · Drew & Grimes 1987, *Communication Research* 14(4) · ElevenLabs docs: numbers/symbols, pauses.
Research run 6 Nov 2026; full links in the RND.md log line of that date.
