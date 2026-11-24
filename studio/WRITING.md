# WRITING.md — write like a person talking (owner, 6 Nov 2026: "research how to write like a human")

> **Read SCRIPT_FEEL.md first (18 Nov 2026):** story *shape* (but/therefore, one open loop, picture per line, build-up + reveal, callback ending). This file is the sentence-level layer.

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

34. **A takeaway needs a result on record.** If the lesson is "watch what your partner learns", the story must *say* the partner overtook you (a count, a profit, a year) before the lesson — otherwise the viewer infers a cause the sources don't show. And check the order of events: a rescue agreed *before* a bankruptcy isn't "guess who walks in" after it. (11 Nov, 7-Eleven fresh-eyes review.)
35. **Don't frame a cost as a skim.** The price of the product (a blank shirt + printing) isn't money that "never reaches" the seller; say what's *left*. Print companies, shops, banks and apps are our likeliest sponsors — describe their fees neutrally, with their own numbers. (11 Nov, print-on-demand review.)
36. **One word, one meaning per script.** "A quarter" (25¢) next to "a quarter of the price"; "share" as a comment word next to the share button. And make spoken numbers add up for a listener: if the voice says about twelve + about five + fees, say the fee total aloud too. (11 Nov, both reviews.)

37. **Small words before a noun fuse on the American narrator too.** "…of card sales in fees" came back "and fees"; "pass the whole fee on"
    came back "the whole fiance" (12 Nov, usa_narr). Put the noun last or use a clearer joiner: "…of card sales as fees", "pass on the whole fee".

38. **Say who found it, one level down.** A government report quoting a textbook is "auditors cite the research", not "auditors say" — open the
    footnote before you attribute (12 Nov, GAO no-show rate). And a rule's floor isn't its price: if the law sets a *minimum* and lets the company
    pay more, say "sets the minimum", and don't say "no cap" next to a company's own cap ("the law sets no limit" + the memo's limit). (12 Nov,
    overbooking fresh-eyes review: both were must-fixes no gate catches.)
39. **American narrator, American numbers** (`human_check` prints a `note number …` line; 12 Nov audit of the queue: 9 hits in 7 scripts, 7-Eleven d1 fixed, a UK-money line like "a hundred and three" pounds may stay — listen). Write "one thousand seventy-five", not "one thousand and seventy-five" (British "and"), and spell out
    agencies that read as words ("The Associated Press", not "the AP"). (12 Nov review.)

40. **A pronoun after a seat line points at the seat.** After "You want those American stores… Three moves take you…", "Where did *they* start?" reads as the Tokyo side, not the stores. Name the thing again ("Where did the stores start?"). (13 Nov, 7-Eleven build read-aloud.)

41. **Say a penalty in the law's own order.** "You can be fined. Ignore a notice and it's an offence" sounds like two penalties; the Childcare Act makes it one chain (a notice first, then the offence, then the fine). Read the section, then say the chain: "Ofsted can send you a notice to stop. Keep going after that, and it's a criminal offence. With a fine." (14 Nov, childminding build fact-check.)

42. **British everyday words don't belong to the American narrator.** "At the till" can be heard as "until", "loads of" and "puts it down to"
    read British. Say "at the register / checkout", "lots of", "credits". `human_check.py` prints a `note british …` line (14 Nov, ZIP review;
    0 hits in the other 26 queued + done scripts). A line set in the UK may keep a UK word — listen.
43. **A court's ruling isn't a verdict on the story.** On an appeal from a demurrer the court rules on the *law* and takes the shopper's claim as
    true. Don't say "Who was right? The court sided with her" — say the question it answered: "The question for the court: is a ZIP code
    personal information? … said yes." And keep each exception to the state that has it ("California lets the store ask"). (14 Nov, ZIP review.)
44. **The seat's year must come before the work it watches.** If a move took "about two years" and ended in Dec 2009, a seat that opens in 2009
    makes the years not add up for a listener: open the seat in 2008 and say the bad year in present tense ("This year, its stores are selling
    about five percent less"). And "the same American stores" points at nothing if no stores were named — say "its American stores" and let the
    chip carry the jargon (same-store sales). (14 Nov, Domino's review.)
45. **"Do you know your X…" can sound finished halfway.** "Do you know your ZIP code…" is heard as "do you know what your ZIP is?" before the
    turn. Put a verb in front of the noun: "Do you know *typing* your ZIP at checkout can lead a store to your door?" (14 Nov, ZIP review.)

46. **A case-study 'move' must be something the protagonist *did*.** If the beat is a discovery (the nine-cat house, the Scottsdale visit), call it a clue, not a move —
    'Move one: the mid nineties' promised action and delivered backstory (15 Nov, Febreze review). And a list of moves that 'turn it around' must contain the turn.
47. **Don't let a joke carry an unsourced fact.** An object character's line is still heard as true: 'One take' (Dollar Shave Club) and 'lives behind locked plastic' are
    the kind of detail a viewer repeats. If the source doesn't say it, make the joke about attitude ('Premium, dear'), not about facts. (15 Nov, DSC review.)
48. **Say whose number it is when the company is the only source.** '12,000 sign-ups in two days' was the company's own figure *to* the WSJ, not a WSJ count:
    'The company told The Wall Street Journal…'. Same for 'reported' deal prices (15 Nov, DSC review). And check who was *visited* vs *filmed* in a reported story (Febreze).

## Before → after (from the 6 Nov credit script; facts unchanged)
- (15 Nov, Febreze) "Same liquid. They just changed when you use it." → "Same spray, a little more perfume. Mostly, they changed when you use it." (rule 31: don't contradict the story)
- (15 Nov, DSC) "And it sold razors by the million." → "Four million people watched it in about a month." (a real, sourced number beats a loose big one)
- (14 Nov, ZIP) "Who was right? In twenty eleven, California's top court sided with her." → "The question for the court: is a ZIP code personal information? In twenty eleven, California's top court said yes." (rule 43)
- (14 Nov, Domino's) "Then Patrick Doyle, who runs the American stores, looks into the lens." → "Then the boss of its American stores speaks. Patrick Doyle." (rule 6; and "looks into the lens" wasn't in any source)
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

49. **A settlement isn't a payment, and a lawsuit's subject isn't your adjective.** A *preliminary* approval is "agreed to pay … to settle", never "paid" or
    "settled for"; say "denied liability" (the order's words) next to the amount. And don't praise the very claim that was sued over — "gut-friendly
    soda" right before "buyers sued over the gut-health claims" contradicts itself and repeats the claim; say the category ("prebiotic soda"). (16 Nov, Poppi review.)
50. **"Before it existed" vs "before it was on sale".** A 3D render and a video before launch don't prove no product had been made; say what the source says
    ("before you could buy a can"). Same for "sold" vs "made": the cover "he SOLD the ad before the water" was false — nothing was sold. (16 Nov, Liquid Death review.)
51. **A catch must carry the company's stated reason.** "Loud brands stumble too" blamed the marketing for a market exit the company put down to moving all
    production home; give the exit, its full scope ("outside America, Britain too") and their reason in one short line. And a "move" that the founder
    never made (pre-orders) is advice wearing the story's clothes — swap it for something he did (counting who asked where to buy). (16 Nov, Liquid Death review.)
52. **Don't add a time of day, a vehicle or a word like 'record' the source doesn't have.** "A hundred days of sales, before lunch" (no time in the sources),
    a pizza *bike* (nobody says how he delivered), "record" profit year (the source says 13th straight year of growth). The everyday-math line can be ours;
    the scenery around it can't. And a US voice saying "three hundred pounds" can sound like weight: say "British pounds" once. (16 Nov, Gymshark review.)
53. **Line limits for Chatterbox are now printed.** `human_check.py` notes every line over 14 words or over 2 sentences (questions count: "Did it work? Over a
    million views. Before…" is 3), and prints an estimated length (0.335 s/word + 0.15 s/line, calibrated on Febreze: 226 words / 20 lines → 78.7 s real VO).
    `--strict` FAILS above 90 s (`--long-ok` only for an owner-approved long-form). Aim for 130–190 words (≤ ~200 lands near 70 s).
54. **Timing isn't motive, and a cottage-food rule is about selling.** "The surprising move: go thick while everyone goes thin" made Hoka's sole a reaction to the barefoot craze; the founders said it wasn't. Say it as timing ("The odd timing? Thin shoes were the big craze."). And "some states ban hot sauce from home kitchens" overstated a rule that only stops you *selling* it as a cottage food. Also: "his longtime pepper farm" sounded like he owned it — it was a supplier. (17 Nov, Hoka + Sriracha reviews.)
55. **Name who got paid, and don't say a date that will go stale.** After a founder sells, "another buyer pays $1.75B" and "its owner said…" read as money/news about the founder: name the owner ("Owner Newell…") and add "Not to Mike." if it's a later sale. In seasonal scripts that may post weeks later, never say "last December" — keep the date on the tape. And put "The surprising move?" on the beat that is actually counter-intuitive (no seller fees), not the expected one (layoffs). Write ≤ ~225 words: `story_check.py`'s length estimate runs ~11 s above human_check's, and its 90-s cap is the one that binds. (19 Nov, Yankee Candle + Vinted reviews.)

56. **Check who said the quote and what the brag really was.** "Target, we're in produce…" was the brand's first employee, not the founder; "I own my own sneaker
    line" was a joke about a co-branded shoe (say "he joked"); "I don't even like chicken" is a cofounder *recalling* the chef ("a friend recalls"). A
    detail from today's menu (a waiver for the hottest level) can't sit in the 2017 scene — tag it TODAY. And a rule's timing is its own: acidified-food
    makers file the process before they *pack*, not "before the first sale"; a pop-up permit can be city *or* county. (21 Nov, Grillo's + Dave's reviews.)

57. **No stall in seconds 5–16: the story starts on an action, the trend comes after the result.** On 4 of 6 posted Shorts-length doodles
    (Liquid Death, Hoka, Sriracha, Yankee; avg watch 12–15 s of ~80 s — Vinted lost them earlier on an abstract hook, Febreze later) the
    *average* viewer left during exactly the block we always put third: a trend statistic with a named source ("Gallup says…", "One menu tracker says…") and/or a "Place, year." / "Meet X." / "Rewind." line
    (estimated start 9–17 s). The doodles that held 18–47 s (Airbnb $40 cereal, $5 nothing, Spanx, Stanley) went from hook straight into a person
    doing something. Kallaway's rule says the same: join beats with "but"/"therefore", never "and then" — a stat between the hook and the
    story is an "and then". So: (1) after the 2–3 hook lines, the next line is the protagonist *doing* something ("No Nike job? So Travis grabs
    grandpa's recipe…"), place + year go on the tape label; (2) the trend line moves to after the result as the "why now" bridge into YOUR moves
    ("So why start yours now? Gym memberships just hit a record."); (3) source names stay on the chip/caption. `human_check.py --strict` now
    FAILS a stat / named-source / date-place line starting in the first ~16 s (STALL gate; `--stall-ok` only for an owner-approved exception).
    Evidence is n = 6 and confounded with length — the test is Poppi/Gymshark/Grillo's avg watch vs the short-doodle median ~14 s (22 Nov R&D,
    `lab/story/shorts_leak_audit.py`).

58. **Order the beats by the company's own timeline, and never invent the comeback moment.** The Scrub Daddy draft said "it sits in that box for
    years… one day he scrubs his hands with it" — but the hand scrubber came *first* (2006), the "no" from body shops (2007) put it in the scrap
    box, and the real comeback was lawn furniture in fall 2011 (scrubdaddy.com/about + Fortune). Open the "our story"/"about" page and line the
    beats up by year before writing; a spoken "no" from customers is the low point most founder stories already have. And use a name exactly as
    the source gives it ("Raising Cane", not "Cane"). (23 Nov, both fresh-eyes reviews.)

59. **"Did it work?" claims a cause; a place must look like the source says.** After a list of store experiences, "Did it work? Sales doubled"
    credits the experiences with growth no source attributes to them — say "And sales? They more than doubled." And describe a venue the way
    its own page does: Jellycat's Harrods "airline" *is* a plane cabin (a display) with check-in desks, so "No plane" was false. Same family:
    "their **own** stores" when a brand already sold through other shops (Bombas via Dick's/Nordstrom), "most-requested **clothing**" not
    "what shelters ask for most", and one name for one speaker ("Their CEO" twice, never "their boss" then "He"). (24 Nov, Jellycat + Bombas reviews.)

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

## Learned from the owner's reference reel (15 Nov 2026 — doodle tech-news explainer he sent: "see their animation style and story writing, learn")
Script moves that make it feel human and keep people watching:
1. **News hook + personal stake in 2 lines.** Line 1 = the surprising fact ("Microsoft just patented a way to train its AI on your gaming PC while you're not using it. And the patent just got approved."). Line 2 = the viewer's own question ("So, is your graphics card about to start working for Microsoft?").
2. **"Here's how it works:"** — the mechanism in 2-3 tiny steps, before any opinion.
3. **Ask the viewer's questions out loud, one by one, and answer each in one or two short lines** ("Will Windows just switch this on by itself? Nothing says so." / "Will you get paid? Maybe."). Honest uncertainty ("nothing says so", "no number given") sounds human and builds trust.
4. **Do the math for them with everyday units** ("an extra 250 watts, 4 hours a day, is about $5.50 a month on your power bill").
5. **"The upside? … The catch? …"** — one line each, balanced.
6. **Real reactions** — quote 1-2 real people (from documents/comments you can source) for humour.
7. **Kill the obvious myth** ("And no, it's not behind yesterday's outage.").
8. **Callback ending** that returns to line 2 ("So tonight, your graphics card still works for just one person: you."), then a short CTA.
Animation moves:
- **One set per section that evolves beat by beat** (same piggy bank stays while dollars fly in, a claims list appears, "0 $" is stamped) instead of a hard cut on every line; a new prop or annotation every 1-2 s.
- **A recurring plain "you" character** (stick person) who reacts.
- **Red-marker annotations** drawn on the scene: strike-throughs, circles, ticks, question marks.
- **Subtitles: small torn strip, 2-5 words at a time, uppercase typewriter, key word under a yellow highlighter** (doodlekit.strip_chunk + anim_shots.chunk_now; highlight = the line's stressed words + any number).

## Length (owner, 15 Nov 2026: "don't make too much length, make it according to shorts")
- Target 50-75 s of voice, hard cap 90 s. Roughly 130-190 spoken words, ~16-22 short lines. (Measured 16 Nov: the real usa_narr pace is ~0.35 s/word incl. pauses — Febreze's 226 words ran 78.7 s — so ~200 words still lands near 70 s; `human_check.py --strict` prints the estimate and fails above 90 s, rule 53.)
- Shape: hook + viewer's question (2 lines) -> the story's 4-5 key beats (problem, surprising move, chaos/low point, result) -> 2-3 quick moves (one line each) -> CTA (1-2 lines).
- Keep the reference-reel tricks but pick only the 2-3 that fit (e.g. one "Did it work?" Q&A, one everyday-math line, the callback ending). Cut side details, object-character lines to 1, and never repeat a number.
