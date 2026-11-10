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
21. **Read it aloud, then read it again over the narrator.** (7 Nov: two of our own TTS misreads came from capitals and one rare adjective: 'Comment LOCAL or GLOBAL' read 'El Col', 'Plain candles' read 'Playing candles'. Write the comment words in lower case in vo_lines.py, caps only on screen.) Keep what sounds like you talking; cut what sounds like a brochure. (NPR)
22. **Tense matches the record.** A practice that ended gets past tense and a time stamp ("Back then, the button said…", "On a computer,
    that meant four pages"). A claim the company disputes is said as theirs, and a regulator's general study is never placed so it sounds like
    it's about the company in the story ("That's Instacart's side. Separately, America's consumer watchdog…"). (7 Nov: both fresh-eyes reviews
    caught a present-tense or run-together claim that the sources didn't support.)
23. **Attribute to the right document.** A word in a press statement isn't in the blog post; a gloss in a complaint ("Fittingly…") isn't the
    company's reason. Say whose words they are, or say less. (7 Nov: "negligible" was in Instacart's statement to Consumer Reports, not its blog.)
24. **Stressed words must be words of the line.** `make_vo.py` matches `stressed_words` to the aligned words (case and punctuation ignored); a
    word that isn't there silently loses its emphasis. `human_check.py` now prints a `note stress …` line for each miss (7 Nov audit of 40
    scripts: 1 real miss, home bakery a5 'refuse' vs 'refused', fixed; our 2 new scripts had 4 after rewrites, fixed).
25. **Watch for words that run together.** Read fast, "That's a maze" became "That's amazing" and "one internal comment it quotes" became "commented quotes" in the ASR read-back of both takes (8 Nov, Prime). If two short words can fuse into a real word, add a word between them ("Feels like a maze, and you're the one stuck in the middle of it.") or put the source first ("The FTC quotes one internal comment: …").
26. **Acronyms that are also words get read as the word.** "US shops paid…" can come out "us shops". Write "American" / "in America"
    in vo_lines.py (UK, EU, FTC are fine). `human_check.py` prints a `note caps …` line for US / IT / AM / OK etc. (8 Nov fresh-eyes review,
    cash rewards; the room's audit found 5 such lines in older scripts: 11 ×2, 12, 13, 17.)
27. **Use the study's own definitions, out loud.** A paper's "cash" can mean "everything except credit cards, debit included"; its
    numbers can be 2007 data published in 2010. If the everyday word means something narrower, say the paper's meaning in one short line
    ("Debit counted as cash.") and put the data year on screen. And a rebuttal must answer the same claim: an industry group's point about
    cardholders isn't a reply to a number about cash payers ("Card groups push back…", not "The card side calls that wrong"). (8 Nov, both
    fresh-eyes reviews: the biggest catches were definitions and scope, again not voice.)

28. **Read the ASR notes before rewriting.** voice_report flags a line when the read-back spells a word differently: "dropshipping" comes back "drop shipping" and "lamp's" comes back "lamps" — those are spelling, not misreads (9 Nov, dropship: 3 of 4 flags were this). Real misreads change the word ("come in one word"); fix those, note the rest in the run log. And `story_check` R7 on *estimated* timing runs long: the dropship script showed 18.x s before voicing and 15.0 s after (with the tighter trim_gaps).

29. **A reaction is an opinion now, never a memory.** "I didn't see that coming" / "I didn't expect…" tells the listener the narrator found
    something out once — a life it doesn't have (rule 15). Say it as a present opinion or a hypothetical: "Who knew a coffee worked like that?",
    "That's the one I'd have missed.", "I'd have scrapped it too." `human_check.py` prints a `note memory …` line (9 Nov: 1 hit in the queue, fixed).
30. **The hook's line must survive its own exceptions.** If the rule has a carve-out that hits the very person in your seat (a *friend* gets three
    hours, not two), make the seat someone the rule fits ("a family down the road") and say the carve-out in one short line. And say the period
    a number really covers ("July to September"), not a rounder word ("one summer"). (9 Nov, both fresh-eyes reviews.)
31. **Don't contradict the story you just told.** After showing a company backing down on one thing, "most bosses would back down" reads as a
    mistake. Name the thing: "I'd have scrapped the price split too." (9 Nov, Netflix review.)
32. **Paraphrase in the source's own order, and say it's theirs.** "Its words: same store, same items, same prices" put words in Instacart's mouth; the blog's sentence ran items → time → store. Say "Instacart's promise now? Same items, same time, same store, same price." and put the real quote on the chip. And avoid "Its + noun?" openers: ASR heard "It's promised" in 4 of 4 takes. (10 Nov, same cart.)

33. **A line the TTS reads weakly gets rewritten, not re-rolled.** Chatterbox Turbo decodes greedily, so the same text gives the same read; only a
    new wording changes it. 11 Nov (Netflix): z1 "Keep or split, in the comments." 3.85 → "Tell me in the comments. Keep, or split?" 4.26;
    "Qwikster." 4.06 → "Qwikster!" 4.25. One-word lines ("Oops!") score ~3.4–3.5 whatever you do — judge them by ear.

## Before → after (from the 6 Nov credit script; facts unchanged)
- (9 Nov, childminding) "Honestly? I didn't see that coming." → "Honestly? That's the one I'd have missed." (rule 29)
- (9 Nov, Netflix) "Members are furious." → "Members start cancelling." (say what the record shows, and it sets up the count)
- (8 Nov, cash rewards) "Each cash-paying household sent about a hundred and fifty dollars a year to card users." → "Debit counted as cash. … A home with no credit card paid credit card users about a hundred and fifty dollars a year." (rule 27)
- (8 Nov, dropship) "Selling in the UK? Thirty days there too." → "Selling in the UK? Thirty days to deliver it, not just ship it." (US = ship, UK = deliver)
- (7 Nov, Prime) "To skip it, the button read: no, I don't want free shipping." → "Back then, the button to skip it said: no, I don't want free shipping." (rule 22)
- (7 Nov, same cart) "Instacart says these were price tests. Run at random, for a handful of its stores." → "Instacart's answer? A coin toss. It says shoppers were put into price test groups at random." (the source: random *shoppers*, ten retail partners)
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
