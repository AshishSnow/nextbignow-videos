# STORY.md — the OopsMyBusiness story engine (source of truth for *what* we tell and *how*)

Owner, 30 Oct 2026: "My character is good, but the storyline and everything need to be good, and the topic. Everything is
allowed. Keep in mind that later I want brand deals — so think more."

**Why this exists (our data, Metricool pull 31 Oct 00:30 IST, 16 animated reels):** the story-shaped videos hold people
longest (Monopoly 31.2 s avg watch = channel best, airline miles 28.5 s), but across all of them saves ≈ 0, comments ≈ 0 and only
a handful of shares, and reach per reel fell from ~1,300 (25–26 Oct) to ~150 (27–28 Oct). We were making *explainers that
happen to have a cartoon*. Brands pay for an audience that **reacts** (comments, shares, saves, follows) to a **recognisable
format** with a **recurring character**. So every video is now a *story the viewer lives*, inside a named series, ending on a
question they want to answer.

Read with: PLAYBOOK.md (craft, voice, visuals, QA, posting), BRAND.md (brand-deal rules), `studio/episodes/` (the writers' room).

---------------------------------------------------------------------------------------------------------------------------
## 1. The channel promise
**"Live the wildest true business moments — then make the call."**
Instagram/YouTube bio line: `True business stories. You make the call. New episode daily.`

## 2. The hero (character bible)
- **Who:** the orange-hoodie guy (`person(..., "hero")`, `guy()`) **is YOU** — the viewer's avatar. Every story puts him in the
  seat of the person facing the big decision (a student, an inventor, a CEO, a shopper). He "plays the role"; he is never drawn
  as the real person's likeness. Real people appear as generic cast characters with an on-screen role label ("PEPSI'S LAWYERS",
  "JUDGE, 1999"), companies as plain-text names — no logos, no trade dress.
- **Personality:** curious, quick, a little cheeky, never mean. He reacts with his face (wow/sus/smirk/sweat) on every reveal.
- **Wardrobe:** the hoodie by default; dress him for the era/role when it helps (`who={"base": "hero", "outfit": "suit"}` for a
  CEO seat, a 1990s jacket, a work apron). The face and orange colour stay — that's the recognisable IP.
- **Narration:** second person, present tense — "You're twenty-one. You open the catalog. You do the maths." It puts the viewer
  inside the story (immersion is what makes POV formats work) and makes the closing question personal.
- **Signature beats (same every episode = brand memory):**
  1. **Cold-open card** in frame 1: `cold_open(f, "1996", "SEATTLE", "YOU: STUDENT, 21")` — year · place · your role.
     (Story kit = `template/scripts/anim_story.py`: cold_open, series_badge, oops_beat, quote_card, choice_card, set_front,
     plus the sets bedroom90s / schoolyard / courtroom and props jumpjet_el, crt_tv_el, mailbox_el, coupon_el, catalog_el.)
  2. **The "Oops." beat** — at the exact moment the blunder becomes clear, the hero turns to camera and says (VO) *"Oops."*;
     `oops_beat(f, t, t0)` stamp + one sting SFX. It is the hero's reaction, never the narrator's verdict on a real company. **Max once per video**, only where a real blunder exists (it's the channel name — keep it special).
  3. **"Your move" end card** — `choice_card(f, "YOUR MOVE", "FIGHT", "FOLD")`: the question + two pills. Same look every episode.

## 2b. Look (owner, 31 Oct → 1 Nov 2026: "use colourful stick men and girls" → then a reference: "use this type of character; change the dress colour like the tie colour, or sometimes the hair")
The cast is **white line-art cartoon people** (`template/scripts/anim_stick.py`, default on): white body, thick black ink outline, big
round head with ears, big eyes with pupils glancing sideways, wide grin, slim outlined limbs, black shoes, a short ground line under the
feet. **Colour lives only in the accents:** tie, shirt/dress, jacket, hair, cap. The hero = spiky white hair + **orange tie** (channel
face). Looks: hero, friend, girl, girl2, lady, inventor, exec, creator, worker, oldman, kid, mystery, judge; change accents per story with
`who={"base": "exec", "tie": (0, 170, 90)}`, `{"base": "girl", "shirt": (255, 200, 0), "hair": (200, 60, 40)}`. Mix men and girls in
every episode. Our own design inspired by the reference — never a copy of an artist's character. 
**Clean look (owner, 3 Nov 2026: "it's not clean like you are doing for NextBigNow")** — `template/scripts/anim_clean.py`, default on
(`CLEAN=0` = old look). Every set name now renders as a **flat, deep, saturated two-colour gradient + one soft light spot + one simple
flat silhouette layer (houses / skyline / trees / shelves / window / counter) + a flat floor band** — no bricks, textures or busy rooms.
No film grain, no bloom haze, no warm cast: whites stay white. `stage()` = clean gradient + one flat circle. **Captions live in the top
band** (`say()` → y≈560, never on faces; `keep=True` only for a deliberate exception). One idea per frame, lots of empty space, the cast
and the one prop in the lower half. New sets: add a palette + silhouette row to `CLEAN_SETS` instead of drawing a detailed room.

## 3. Series — every video belongs to exactly one (badge + title + CTA)
| Series | Share of videos | What it is | Types (PLAYBOOK §2) | Ends with |
|---|---|---|---|---|
| **YOUR MOVE** (flagship) | ~20 % | POV true story at a decision point | A, D, C (any story with a person deciding) | a two-option question: "Comment FIGHT or FOLD IT" |
| **SPOT THE TRICK** | ~15 % | the hero walks into an everyday place (shop, app, airport, cinema) and catches the tricks one by one | E, B, F | "Save this before your next …" + share line |
| **HOW TO START** (new, owner 31 Oct: "informative, like how to start a drone business") | ~35 % | a practical, verified step-by-step guide to starting a real small business (drone services, food truck, vending machines, print-on-demand…): what it is, licences/rules, gear + startup cost, what clients pay, first customers, the mistake that sinks beginners | E / F (how-to) | "Save this before you start" + "Comment your city/question" |
| **HOW IT WORKS** (new, owner 3 Nov: "find topics which are informative, interesting") | ~25 % | an explainer of a money machine everyone touches but nobody sees: who gets paid when you stream a song, what's inside your credit score, where the 30 % app cut goes, why takeout costs more. Hook = a surprising number about the viewer's own life; 4–5 beats, each one picture (a pot, pipes, a sliced burger, a pie); one practical takeaway | E (explainer) | "Send this to someone who …" or "Save this" + a comment question |
| **WHO REALLY OWNS IT** | ~5 % | follow the money through doors to the hidden giant | C | "Tag someone who buys from them" |

- Badge: `part_badge(f, "YOUR MOVE", "EP 7 · THE PEPSI JET")` style, top right, first 2 s and on the end card.
- Post title format (YouTube ≤ 50 chars, keyword first): `<keyword hook> | Your Move` / `… | Spot the Trick`.
- Number episodes per series (`episodes/README.md` keeps the counter).
- **Two-part episodes** (YOUR MOVE only, max 1 in 4 videos): when the true story has a natural cliffhanger *at the decision*.
  Part 1 ends on the choice with no answer + "Part two tomorrow — follow so you don't miss it". Part 2 is built by the **next**
  video run after Part 1 (the task fires once a day; ≈ 24 h later, same IST slot), opens with the PART 2 badge and a ≤ 6-s recap inside the hook question,
  and must make sense on its own. Say "MOST OF YOU SAID …" **only** with real comment counts from Metricool/the app — never invent it.

## 4. Beat sheet — YOUR MOVE (single episode 75–110 s; Part 1 ≈ 70–85 s, Part 2 ≈ 60–80 s)
| # | Beat | Time | What happens | Tools |
|---|---|---|---|---|
| 0 | **Cold open** | 0–3 s | Frame 1 = the most extreme true image, mid-action (the jet over the school). Hook question with stakes in ≤ 16 words. | set + hero + `hud_clock` card |
| 1 | **Your seat** | 3–12 s | "You're …" — who you are, what you want, and **the rule of the game** in one sentence. | `hud_rule(f, 1, "...")` |
| 2 | **The insight** | 12–35 s | The clever move or the hidden flaw, with one everyday comparison. Promise a roadmap: "Three problems stand between you and that jet." | close-up, prop, `say()` on the key number |
| 3 | **Escalation** | 35–75 s | One scene per problem (place + want + obstacle + outcome). A win, then a blow. Re-hook every 20–30 s ("Then Pepsi writes back."). The **Oops.** beat lands here if the blunder is the company's. | new set or shot size every 2–3 s |
| 4 | **The decision** | 60–90 s | The moment someone has to choose. Part 1 of a two-parter **stops here**. | close-up + `hud_timer` if time pressure is real |
| 5 | **Outcome + twist** | ≤ 18 s to end | What really happened, then the detail nobody expects. | quote card with source chip |
| 6 | **Takeaway** | 1 line | Something the viewer can use tomorrow (save-worthy). | `say()` |
| 7 | **Your move** | last 4–6 s | Two-option question with no obvious right answer, one-word answers; then "Send this to the friend who …". | end card (`hud_choice` pills) |

**SPOT THE TRICK beat sheet:** cold open in the place with trick #N already visible → "This shop tricks you N times before you
pay. The last one is the sneakiest." → TRICK #1…#N (`hud_rule`-style pills): show it happening to the hero → why it works (one
study or filing, source chip) → how to beat it (one concrete action) → strongest trick last → "Save this before your next shop" +
"Send this to the friend who …". The hero is the shopper; the store staff/system are the antagonist (generic, no real logos).

**HOW TO START beat sheet (75–120 s):** cold open: the hero doing the job with money landing (frame 1) + hook question ("Could you
start a drone business with one drone?") → "Here's the whole plan in N steps — step N is where beginners lose money" → STEP 1…N
(`cold_open(f, "STEP 1", "GET LICENSED", "PART 107")` card each): rule/licence with its real cost and source; gear + total startup
cost; what clients really pay (source chip); how to get the first 3 clients; the costly mistake → realistic takeaway (no income
promises: "typical rates", "can", never "you will make") → "Save this before you start. Comment your country and I'll…" (no promises
we can't keep — "comment your question"). A girl character as the expert/mentor and the hero as the beginner works well.
Brand note: this series is the most sponsor-friendly (tools, insurance, website builders, courses) — keep it neutral, no affiliate claims.

**HOW IT WORKS beat sheet (aim 90–120 s, R&D 4 Nov):** frame 1 = the surprising number already on a physical object, and name the subject in line 1 → seat ("You're the singer") → a count of named stations you can draw ("four gates", "five slices"), strongest catch last → one picture per station, the same object growing through the video (a pot, a pie) → one worked example with labelled made-up numbers, checked against its own logic → **answer the hook aloud** → switch seats or a practical check the viewer can do today → a YES/NO comment question the facts don't settle + "Save this" + "Send this to the friend who…". Say the qualifier in the voice if the voice would mislead without it; a chip is only a footnote.

**WHO REALLY OWNS IT beat sheet:** cold open on a street of "competing" shops → "You think you're choosing. Count the doors." →
DOOR #1…#N, each opens to the same owner → the twist (scale/number) → what it means for your wallet → "Tag someone who…".

## 5. Writing rules (craft — the story_check S-gates measure some of them)
1. **Second person, present tense, short lines.** One idea per line, ≤ 18 words per sentence, one figure per sentence (R5).
2. **But / so, never "and then."** Each beat must cause the next (R4). If you can't connect two beats with *but* or *so*, cut one.
3. **Stakes in numbers *and* feelings** by ~15 s: what you can win or lose, whose money it is ("your friends' money").
4. **Scenes, not facts.** Each beat is a place + a want + an obstacle + an outcome. If a line could be a slide, rewrite it as
   something happening to "you".
5. **Show it.** The picture carries the information; captions (`say`) only on key words and numbers. Mute test: can you follow the
   story from the frames alone?
6. **Real words only for real people.** Quotes from documents (court opinions, letters, filings, interviews) go on a quote card with
   the source chip. Invented lines are allowed only for "you" (your thoughts) or unnamed extras ("a cashier"), and never claim a real
   person said them.
7. **The choice must be honestly debatable** — both answers defensible, one word each ("FIGHT / FOLD", "SELL / KEEP", "JOKE / DEAL").
   Not "Would you like free money?". Put it as a comment prompt *and* in the end card pills.
8. **Takeaway = an action**, not a moral: "Read the small print — it's where the real price hides."
9. **Respect.** Curious, not cruel: no mocking real private people, no "evil company" framing, no punching down. Blunders are
   told as true events with what courts/regulators found, stated as such. (Brand-safety rules: BRAND.md §3.)
10. Keep the 27 Oct story rules (PLAYBOOK §4): roadmap promise (R8), an open loop every ≤ 25 s (R2), no recap lines (R6),
    twist → end ≤ 18 s (R7).

## 6. What makes a topic a good episode (on top of the interest test)
- **A seat:** someone the viewer can *be* at a moment of decision (ordinary people beat CEOs; CEOs work when the stakes are huge).
- **A real decision** with two defensible options — or for SPOT THE TRICK, ≥ 3 tricks the viewer can spot tomorrow.
- **An arc:** want → obstacle → turn → outcome, all verifiable.
- **Brand-safe** (BRAND.md §3) and ideally in a theme sponsors care about: money, shopping, work, starting a business, tech.
- **What our data says about openings (3 Nov, n = 18 animated reels, `lab/story/hook_length_audit.py`, PERFORMANCE insight X):** hook wording does not predict the
  3-s rate (words, "you", ellipsis: all |rho| ≤ 0.24, p ≥ 0.3), so don't polish wording by rule. The one split that separates is what the video is *about*: something
  the viewer pays for or could do themselves (how-tos, gas, printer ink, gym, hot dog) 64–76 %, everything else 24–64 %. Post-hoc tags, n small: use it to choose topics, not as proof.
- **AI readers can't judge watchability.** A blind panel of 5 simulated viewers scored 0.00 against our real 3-s rates and ranked our two best how-tos near the bottom. Use
  fresh-eyes subagents for accuracy, clarity, logic and brand safety; never let them kill or pick a topic or hook on "people won't watch this".

## 7. Checklist before `make_vo.py`
- `SERIES = "YOUR MOVE"` (or `"SPOT THE TRICK"` / `"WHO REALLY OWNS IT"`), `PART = 0/1/2`, `EP = n` at the top of `vo_lines.py`.
- `python3 studio/tools/story_check.py $P` → 7/7 R-gates **and** all S-gates (seat, stakes, choice/save CTA, Oops ≤ 1, part logic).
- `python3 studio/tools/board_check.py episodes/queue/<NN-slug>` → 0 failures (rows ↔ lines, signature beats), no `say()` caption
  below 60 % size, and its BUILD BRIEF read: every missing set/prop/look is written before the first test frame (`--strict` must pass).
- Storyboard: one frame per beat rendered with safe-zone guides and looked at; the mute test passes.
- Facts: every number re-verified today (PLAYBOOK §3); every quote has a document behind it.

## 8. The writers' room (`studio/episodes/`)
Scripts are written **ahead** and reviewed with fresh eyes before anyone renders. The R&D runs keep `episodes/queue/` stocked
with 2–3 REVIEWED scripts (vo_lines.py + shots.md storyboard + SOURCES.md); a video run builds the top REVIEWED one (re-verifying
every number) unless a two-part Part 2 is due. Pilot: `episodes/queue/01-pepsi-jet-p1` and `-p2` (Your Move, Ep 1).
