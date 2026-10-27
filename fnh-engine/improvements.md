# FreshNestHub — continuous improvement (read + update EVERY run)

**Owner, 26 Oct 22:59: "It's not about views or post numbers — just learn new things and keep improving, every day,
every run, voice AND visuals AND topics."** Numbers are only a compass; the goal is to get better at the craft every
single run, and to never stop learning. Never write "nothing to improve".

The owner's standing order (26 Oct 2026): "Don't settle. With every video improve: more natural voice, better video.
Understand the new algorithm and act on it — I shouldn't have to tell you every time." Growth takes time; quality and
learning beat speed. Every run must leave the channel a little better than it found it.

## A. Algorithm notes (re-check EVERY DAY: the first run of each IST day, i.e. when "Last checked" is not today; record what changed)
Last checked: 2026-10-27 (02:00 IST run; 06:00 run = same IST day, no re-check needed). Sources: Kompozy (Sep 2026, Mosseri signals), Creator Lane (2026), Gyre (2026),
Socialync (2026), Android Headlines / TechCrunch (Jul 2026, YouTube monetization rules); 27 Oct: Les Gens d'Internet
(2 Oct 2026, YouTube Shorts originality update), OutlierKit (YouTube Shorts algorithm in YouTube's words, 2026),
SocialPilot (Instagram Reels algorithm changelog 2025-2026).
27 Oct changes: (a) 1 Oct 2026 YouTube said Shorts will "further prioritize original content" and cut reach for
re-uploads with nothing added; it rewards own voice/editing/storytelling -> our fully original animation + own narration
is the right side of this; never reuse clips. (b) YouTube: "engaged views" (watched past the first seconds) became the
qualifying metric (24 Aug 2026); Shorts can be grouped into series + custom thumbnails -> consider a "How your body
reacts to food" series later. (c) Instagram: non-follower recommendations still capped at 3 min; keyword captions matter
more since users can edit their "Your Algorithm" topics (topic matching) -> first caption line = exact search question
+ topic keywords (spicy food, capsaicin, milk). Auto-translation of captions/audio (EN/HI/PT/ES) helps Indian reach.
1. **First 2–3 seconds decide distribution.** Instagram: watch time, likes per reach and **sends per reach** are the
   top signals (Mosseri); reels holding > 60 % of viewers past 3 s reportedly get several times the reach.
   YouTube Shorts: "viewed vs swiped away" in the feed, then completion/average % viewed decides how far it travels.
   => Frame 0 already moving, Chubby + the object + the question on screen inside 1.5 s; no slow build-up.
2. **Retention/completion is the main Shorts signal.** Third-party guides: 30–60 s Shorts want ≈ 50 %+ average view;
   cut or change the picture every 2–4 s (nothing static > 4 s); an ending that flows back into the opening helps loops.
   => OWNER PRIORITY (26 Oct 23:25): understanding beats length — videos may run 2–3 min when the topic needs it.
   Keep retention with re-hooks every 20–30 s, a clear step-by-step structure and constant visual change; tease the
   best fact early ("and the last one is wild"). Compare watch % of short vs long videos in performance.md.
3. **Sends/shares are the strongest signal for reaching non-followers (Instagram).** => Every video needs a
   share trigger: a surprising fact + a practical takeaway + "Send this to the friend who…".
4. **Originality / no mass-produced feel.** Instagram excludes repost/aggregator accounts from recommendations;
   YouTube (2025–2026) demonetises mass-produced, repetitive, template-based AI content without a unique narrative
   arc, and AI human-like hosts giving health advice. => Every video needs its own story shape, opening, layouts,
   props, music genre and Chubby actions; real cited facts; Chubby is a cartoon and never gives medical advice.
5. **Search/SEO:** captions and titles are read for search more than hashtags. => First caption line = the exact
   question people type; ≤ 5 IG hashtags, 3 on YouTube; a specific question to drive comments (comments weigh more
   than subs on Shorts per guides). Put the comment question as the Instagram `firstCommentText` too.
6. **Consistency beats bursts**; quality over volume (guides suggest 1–2 Shorts/day; owner chose every 5 h — keep it
   unless data shows over-posting hurts reach; then tell the owner).
7. Mute viewing is common => every key moment readable without sound (short key-moment captions + clear visuals).

## A2. Daily trend + topic scan (first run of each IST day)
- WebSearch what people are asking/sharing this week about food + health (viral food myths, seasonal foods/festivals,
  news about everyday foods/drinks, "why does…" questions). Add 3–5 fresh candidates to the TOP of topic_ideas.md
  UP NEXT (with the angle + 2 likely sources), ranked by: broad appeal (everyone eats/does it) > surprise > share-worthy
  takeaway > visual potential. Drop/stale-mark ideas that the data says are too niche. Record the date here:
- Last trend scan: 2026-10-27 — Halloween week (31 Oct: candy, sugar), Diwali (8 Nov: sweets, silver leaf), and
  sequels to strong science hooks (mint = cold sensor, the twin of today's spicy video). Added to topic_ideas.md.

## B. Per-run improvement protocol (mandatory)
1. Refresh performance.md (step 1 of PLAYBOOK). Compare the last 3–5 CHUBBY videos on 3-s hold, avg watch %, shares
   and saves per 1k reach. Write 1–2 dated learnings in section D (what worked / what didn't, with numbers).
2. Pick **at least 3 upgrades** for this video — one VOICE, one VISUAL/EDIT, one TOPIC/SCRIPT — from the backlog
   (section C), the daily scans or the learnings. Prefer what most likely raises 3-s hold, watch % or shares.
   Keep each change small and testable. VOICE changes must pass `engine/tools/voice_report.py` on this episode:
   UTMOS not lower than the last episode's by > 0.05 (aim higher), no ASR bad lines, pitch range >= 15 st,
   speaking pace 180–200 wpm. Record the voice_report numbers in section F.
3. Implement it; check it in the test frames / ASR read-back; if it's reusable, put it in fnh-engine/template/ or
   engine/ so all future videos get it (and note it in the PLAYBOOK if it changes the method).
4. Log it in section E: `ep | change | why | metric to watch`. After 48 h, look at the metric; keep or revert
   (write the verdict next to the entry). Never repeat an idea that the data says hurt.

## C. Backlog (take from the top; add new ideas as you find them)
Voice (make it sound more like a real, excited young guy — never robotic):
- [x] 26 Oct 22:19 IST: owner listened to options A/B/C/D and PICKED A (the current voice in voice.env). Keep A's character
      (am_eric/am_fenrir blend, lifted ~165 Hz register, energetic young guy). Voice upgrades = refine A (pacing, stresses,
      pauses, phrasing, cleanliness) — never swap to another blend or a deeper/older voice.
- [x] 27 Oct (ep 09): per-line speed variety (questions/reveals 0.96–0.97, quick facts 1.02–1.03) — same-script A/B:
      UTMOS 4.06 (all 1.0) -> 4.19 / 4.28 (varied). Now the PLAYBOOK default (step 4).
- [x] 27 Oct (ep 09): wh-questions still need the "q" rise in our pipeline: c1 "how do you put out a fake fire?" scored
      3.96 without it vs 4.11–4.26 with it.
- [x] 27 Oct (ep 10): write for the ear: contractions, short words, "you" talk; lines <= 12 words where possible; punctuation
      for natural pauses. Result on a 1:58 script: chunk20 4.366 / line mean 4.356 (ep 09 4.408 / 4.332), ASR clean.
- [x] 27 Oct (ep 10): fix weak lines by re-ordering the sentence, not only speed: b2 "an organ behind your stomach wakes up.
      The pancreas." 3.99 -> "your pancreas wakes up. It's an organ behind your stomach." 4.35 (name first, then define).
      voice_report now prints utmos_lines (per-line) so weak lines can be found and rewritten.
- [ ] Less audible pitch processing (EXS 0.4, BMP 0.7) if the voice sounds "processed"; keep stresses on 1–2 words/line.
- [ ] Emphasis words: real stress (slightly louder + longer), not every line; question endings rise, statements settle.
- [ ] Natural micro-pauses before the payoff word ("...it's eating you BACK").
- [x] 26 Oct: calmer pacing for A (SPD 0.88, PZ 1.6, PMIN 0.3) — UTMOS 4.27 -> 4.36 (see F). Now default in voice.env.
- [ ] Next voice ideas to lab-test with voice_report: per-line SPD variety, EXS 0.6, STR 1.2 on payoff words, shorter
      lines (<= 12 words), commas for breath points. Keep the A blend + ~165 Hz lift.
Visual / edit:
- [ ] Chubby is often small in a corner — make him the actor (big, in the middle of the action, interacting with props).
- [ ] Break the "big circle + prop" sameness: full-bleed scenes, split screens, close-ups, top-down tables, inside-the-body
      worlds, camera push-ins/pans, parallax layers. No two consecutive shots with the same layout.
- [ ] Frame 0 hook: motion already happening at t=0 (no pop-in from empty), cover frame = Chubby + object + question.
- [ ] Secondary motion everywhere (bob, squash on impacts, blinking, props wobble) so nothing is static > 2 s.
- [ ] Kinetic numbers: count-ups / slams for key numbers; consistent sources chip.
- [ ] Better diagrams: more detail and texture (highlights, rim light, subtle 3D shadows) on the main prop each video.
- [ ] Sound design: a signature 1-s FreshNestHub sting; foley that matches the action (squelch, fizz, sizzle).
Topic:
- [ ] Prefer universal kitchen/daily-habit topics (biggest reach so far); use the daily trend scan for timely ones.
- [ ] Every topic must have a "wait, what?" fact in the first line + a takeaway people can use today.
Script / packaging:
- [ ] Hook with stakes in < 2 s; tease the best fact early; loop the last line into the first.
- [ ] Practical takeaway line in every video (what to do with this fact) — boosts saves/shares.
- [ ] Comment question in caption + firstCommentText.

## D. Learnings (newest first, dated, with numbers)
- 2026-10-27 16:00: spicy (03:25), sugar rush (07:55) and mint (12:25) are PUBLISHED on Instagram but still absent from
  Metricool reel analytics 8-13 h later (pineapple showed up after ~7.5 h); carrots/pineapple numbers unchanged again
  (133 / 86 reach). YouTube rows still only go to 25 Oct (face mites, 1 view). => reel analytics lag grows with the
  number of fresh posts; never judge a video before its row exists, and keep the 48-h rule. The honey "label ka sach"
  reel (Indian food purity, 5.5k reach) is still our biggest reach -> ep 12 tests an Indian-food-purity topic (silver
  vark, Diwali-timely) in the CHUBBY style.
- 2026-10-27 16:30 (voice A/B, same silver script): the per-line prosody gate (PGATE 0.15, ported from the studio R&D)
  lifted the take from chunk20 4.350 / line mean 4.292 to 4.412 / 4.339 at the same 186 wpm; SPLIT (per-sentence TTS
  calls) did not help our blend and slowed speech to 170-173 wpm. A second take of nearly the same script scored
  4.369 / 4.330 -> the take-to-take noise is about +-0.04 on chunk20; render 2 takes when a take is near the gate.
- 2026-10-27 11:00: Instagram numbers for carrots (133 reach / 155 views) and pineapple (86 / 127) are IDENTICAL to the
  06:00 snapshot — reach has fully stopped at 12–17 h; spicy (03:25) and sugar rush (07:55) are not in Metricool analytics
  yet. YouTube rows started flowing for the first time (only the 25 Oct face-mites row so far). => keep judging at 48 h;
  ep 11 is a direct SEQUEL to the spicy video (series hook "same prize as our spicy video") to test whether a linked pair
  lifts both. Watch spicy + mint reach together at 48 h.
- 2026-10-27 11:00 (voice A/B, same script): ending every explaining statement with a "settle" (low) fall scored the same
  as the old pattern (chunk20 4.410 vs 4.407, line mean 4.350 vs 4.351) — UTMOS does not reward intonation-only changes.
  Rewriting the weakest lines DID move them (b2 4.11 -> 4.41, b3 4.13 -> 4.31). => rewrite > retune.
- 2026-10-27 06:00: CHUBBY reach is flat after 8–12 h (carrots 133 reach / 155 views, pineapple 86 / 127) while 3-s hold
  stays high (58–72 %). The Nessa dandruff reel had 1.29k reach at a similar age. So the hook works for people who
  see it; the problem is how many get shown it (topic pull / non-follower distribution). => ep 10 tests a broad,
  timely topic everyone has an opinion on (Halloween sugar rush) + a debate-style comment question. Judge at 48 h.
- 2026-10-27 06:00: YouTube analytics still null in Metricool (YTVP* for every video) — 3rd check in a row.
- 2026-10-27: first CHUBBY numbers (posts < 9 h old, judge again at 48 h): pineapple (food bites back at frame 0)
  held 72.2 % past 3 s — our best hold ever, equal to the realistic Nessa-era tattoo reel (72.8 %); carrots held 58.3 %.
  The difference: pineapple's hook had an absurd ACTION in the first second (the food attacks), carrots built up to
  a colour change. => Keep a physical, surprising action at t < 1.5 s (ep 09: Chubby breathes fire).
- 2026-10-27: avg watch is still short (pineapple 17.5 s of 56 s = 31 %, carrots 10.3 s of 57 s = 18 %); the Nessa
  dandruff reel got 10 shares from 1.3k reach with a practical scalp takeaway. => ep 09 tests a re-hook every
  20–30 s + a 5-s visual recap + a practical takeaway (milk beats water) to lift watch % and shares on a 1:36 video.
- 2026-10-26: realistic-looking hooks held 60–71 % past 3 s vs 56–58 % for our first animated style and 5–16 % for
  static openings; ambergris (money stakes + story) had the longest avg watch (37.9 s). Broad "is your X fake / how
  much water" topics got the biggest reach (4.7–5.6k).

## E. Changelog (one line per video)
- 12 silver leaf on sweets (27 Oct, auto run, ~2:04): VOICE per-line prosody gate (PGATE 0.15) ported into the FNH make_vo
  + voice.env (SPLIT tested and rejected), weak lines rewritten (a1 name-first, a6 shorter); chunk20 4.412 / line mean
  4.339 (ep 11 4.427 / 4.359, within gate) | VISUAL pre-training cast card (MEET THE CAST: silver bits / thin sheets /
  hammer with their states) before the process, iris match cuts from a round object into the next scene (sweet -> leaf,
  scale -> hair close-up, leaf -> magnified specks), hammer swung on an arc with anticipation + 2-bone arm IK so Chubby
  really holds it, metal-detector hook at frame 0, element tiles (Ag/Al/Pb/Ni) to define metals on sight, festive
  colour script (festive warm / steel truth / dark secrets), prop lib12 + foley (clang, rustle, detector beeps) |
  SCRIPT/TOPIC Diwali-timely Indian food-purity topic (like the 5.5k-reach honey reel), concrete comparison (1 m2 of
  paper 80 g vs silver leaf < 3 g), open loop "some might not be silver" at 6 s paid at ~65 %, 5 chapters, honest
  EFSA "not enough data" catch, Bollywood-festive score (dhol on taiko, sitar, shehnai) | metric: reach at 48 h vs
  honey reel + CHUBBY eps, 3-s hold, shares/1k, comments on "peel it or eat it".
- 11 mint feels cold (27 Oct, auto run, 2:05): VOICE weakest lines rewritten shorter (b2 4.11 -> 4.41, b3 4.13 -> 4.31),
  plain lines 1.02–1.03 to reach 181 wpm, statement-settle A/B (neutral, kept for naturalness); chunk20 4.427 / line mean
  4.359 (ep 10 4.366 / 4.356) | VISUAL scale cues: powers-of-ten zoom_through (Chubby's face -> tongue -> nerve ending) +
  scale_ladder "you are here" mini-map (YOU -> TONGUE x5 -> NERVE x100 -> COLD ALARM x1000); a COLOUR SCRIPT (warm sets =
  real temperature, icy sets = what the brain feels, flipping on the exact word); freeze-into-an-ice-block hook at 0.8 s;
  new prop lib11 (menthol key-molecule with menthol's ring, cold alarm + jumpy mode, frost creep, snow, icicles, breath,
  thermometer with an alarm trigger line that moves up) | SCRIPT/TOPIC sequel to ep 09 (same Nobel, heat alarm vs cold
  alarm), open loop in the first 5 s ("it even fools your nose") paid off at 70 % (85 s), 4 chapters, cool-jazz score,
  new foley (ice crack, sip, teeth chatter, wind) | metric: spicy+mint reach at 48 h, 3-s hold, avg watch % on 2:05.
- 10 sugar rush (27 Oct, auto run, 1:58): VOICE ear-writing (<= 12-word lines, contractions) + rewrite weakest line by
  name-then-define order (b2 3.99 -> 4.35); chunk20 4.366 / line mean 4.356 | VISUAL refutation kit: myth_tag (MYTH ->
  red X + BUSTED), split_contrast panels (sugar vs sweetener, told-sugar vs told-no-sugar, "what moms saw vs what was
  really there"), chapter_card PART 2 / PART 3 at the re-hooks; freeze-frame record-scratch opening; x-ray belly with
  pancreas waking; cell with a locked door that the insulin key opens; new Chubby cast (mom with hair bun, scientist with
  lab coat + goggles, blindfolds) | SCRIPT/TOPIC timely Halloween myth, refutation structure (myth -> busted -> how the
  body works -> blind tests -> parent twist -> real cause -> honest catch -> recap), spooky surf-rock score, new foley
  (record scratch, wrapper crinkle, boing, key jingle) | metric: reach at 48 h vs carrots/pineapple, comments, shares/1k.
- 09 spicy (27 Oct, auto run, 1:36): VOICE per-line speed variety + wh-question rise (UTMOS chunk20 4.41 vs ep08 4.45,
  same-script A/B +0.2 over flat) | VISUAL Mayer explaining kit (spotlight, label_at leader labels, inset magnifier,
  pulse_path nerve signals, recap_steps, count_up) + Chubby breathes fire at t=1.4 s + full-tissue diagrams |
  SCRIPT longer how-it-works (36 shots), key-in-a-lock analogy, re-hooks at 41 s (Nobel) / 66 s (birds), 5-s recap,
  mariachi ranchera score with thin bed under explanations | metric: 3-s hold vs pineapple, avg watch %, shares/1k.
- 26 Oct 23:25 (between runs): length cap removed — 45 s to 3 min, whatever gives full understanding; explaining skills
  added to the curriculum; build keeps files < 95 MB for long videos.
- 26 Oct 22:50 (between runs): voice A pace refined (A4 above) + UTMOS gate added; daily algorithm + trend scans.
- 07 carrots (26 Oct, interactive): new CHUBBY v4 style baseline (owner approved). Voice A, 19 shots, food-funk score.
- 08 pineapple (26 Oct, auto run): same style; calypso score. Review: good consistency, but Chubby small in corners in
  ~half the shots and many "big circle + prop" layouts — next runs: make Chubby the actor + vary layouts.

## F. Voice benchmarks (UTMOS 1–5, higher = more natural; carrot script unless noted)
| date | settings (A blend + 165 Hz lift unless noted) | UTMOS | wpm speaking | pause ratio | f0 range st | ASR bad |
|---|---|---|---|---|---|---|
| 26 Oct | A0 baseline SPD 1.0 PZ 1.0 | 4.27 | 213 | 0.09 | 17.3 | 0 |
| 26 Oct | A1 SPD 0.94 PZ 1.3 PMIN 0.3 | 4.05 | 206 | 0.11 | 17.5 | 0 |
| 26 Oct | A2 SPD 0.90 PZ 1.5 PMIN 0.35 | 4.33 | 200 | 0.12 | 17.4 | 0 |
| 26 Oct | A3 SPD 0.94 PZ 1.3 PMIN 0.3 EXS 0.7 BMP 1.0 | 4.14 | 206 | 0.11 | 18.9 | 0 |
| 26 Oct | **A4 SPD 0.88 PZ 1.6 PMIN 0.3 (adopted)** | **4.36** | 197 | 0.13 | 17.4 | 0 |
| 26 Oct | A5 = A2 with GT 160 | 4.34 | 200 | 0.12 | 17.4 | 0 |
| 26 Oct | A6 SPD 0.86 PZ 1.5 PMIN 0.35 | 4.31 | 193 | 0.12 | 17.4 | 0 |
| 27 Oct | ep 08 pineapple script, A4 (reference re-render) | 4.407 (chunk20 4.448, line mean 4.374) | 176 | 0.14 | 17.7 | 0 |
| 27 Oct | ep 09 spicy, A4, all lines speed 1.0 | 4.061 | 187 | 0.14 | 17.3 | 1 ("2021" norm) |
| 27 Oct | **ep 09 spicy, A4 + per-line speed variety (shipped)** | **4.276 (chunk20 4.408, line mean 4.332)** | 183 | 0.13 | 17.1 | 0 |
| 27 Oct | ep 10 sugar rush, A4 + ear-writing, first take | 4.135* (chunk20 4.337, line mean 4.342) | 182 | 0.14 | 17.5 | 0 (after year fix) |
| 27 Oct | **ep 10 sugar rush, + b2 reordered, i2 0.98, g2 0.97 (shipped)** | **4.225* (chunk20 4.366, line mean 4.356)** | 182 | 0.14 | 17.5 | 0 |
| 27 Oct | ep 11 mint, A4 + 'settle' endings (A/B: old endings 4.407 / 4.351) | 4.191* (chunk20 4.410, line mean 4.350) | 180 | 0.15 | 17.5 | 0 |
| 27 Oct | **ep 11 mint, + weak lines rewritten, plain lines 1.02–1.03 (shipped)** | **4.228* (chunk20 4.427, line mean 4.359)** | 182 | 0.15 | 17.5 | 0 |
| 27 Oct | ep 12 silver, old make_vo (no gate), first script | 4.058* (chunk20 4.350, line mean 4.292) | 186 | 0.15 | 17.2 | 0 |
| 27 Oct | ep 12 silver, SPLIT 0.12 + PGATE 0.15 | 4.136* (chunk20 4.365, line mean 4.315) | 170 (fails pace) | 0.14 | 17.4 | 0 |
| 27 Oct | ep 12 silver, SPLIT 0.06 + PGATE 0.15 + rewrites | 4.148* (chunk20 4.362, line mean 4.325) | 173 (fails pace) | 0.14 | 17.4 | 0 |
| 27 Oct | **ep 12 silver, PGATE 0.15 + a1/a6 rewrites (shipped; now voice.env default)** | **4.245* (chunk20 4.412, line mean 4.339)** | 186 | 0.15 | 17.1 | 0 |
| 27 Oct | ep 12 silver, same + a4 shortened (2nd take, not used) | 4.096* (chunk20 4.369, line mean 4.330) | 187 | 0.15 | 17.1 | 0 |
*ep 10: whole-file UTMOS now scores only the first 100 s (a 118-s whole-file pass ran out of RAM on the 8 GB box).
Note (27 Oct): whole-file UTMOS is length-biased (94 s file 4.28 vs its own 20-s chunks 4.41), so voice_report now
also prints utmos_chunk20 + utmos_line_mean; gate on those when lengths differ (ep 09 vs ep 08: -0.04 / -0.04, pass).
Per-line UTMOS has about ±0.1 run-to-run noise on single lines — judge on means, not one line.
Note: the calmer pace makes the same script ~13 % longer (~155 words per minute). Length now follows the topic (45 s–3 min).

## G. Craft learning — one NEW skill every run (mandatory; this is the heart of improving)
Every run: take the next unchecked skill below (or a better one you discover), research it for ~5 minutes
(WebSearch: animation/motion-design/voice-over/sound-design/storytelling guides, breakdowns of great animated
explainers), write 3–5 lines in the journal (what you learned + source), USE it in this video, and if it works,
add it to `template/anim_fx.py` (or voice.env / make_vo / mix helpers) with a one-line note so every future
video has it. Add newly discovered skills to the curriculum. Skills compound — the library must keep growing.

### Curriculum (tick when learned + applied; add more as you discover them)
Animation & visuals:
- [x] Squash & stretch, slow in/out, overshoot, anticipation, smear trails, sparkles/confetti/dust (anim_fx.py seed, 26 Oct)
- [ ] Staging: one clear focal point per shot; silhouette test for Chubby's poses
- [ ] Follow-through & overlapping action (hair curl, belly jiggle, props settling with `settle()`)
- [~] Arcs: move props and limbs along curves, not straight lines (ep 12: hammer_swing on an arc + arm IK)
- [ ] Timing & spacing: hold key poses 6–10 frames, fast in-betweens (snappy cartoon timing)
- [ ] Exaggeration: bigger expressions at reveals (eyes pop, jaw drop, double take)
- [ ] Character acting: eye direction leads action, blinks on cuts, reaction shots
- [ ] Simple lip-sync visemes for Chubby when he talks (mouth shapes from the VO envelope + vowels)
- [ ] Camera language: push-in on reveals, whip pans between ideas, low/high angles, rack focus (`cam_keys`, `push_in`)
- [ ] Depth: parallax background layers, foreground elements passing the camera, atmospheric perspective
- [ ] Lighting: rim light and soft ambient-occlusion shadows on props; light rays on reveals
- [x] Colour script: plan the colour arc of the video (ep 11: warm = real temperature, icy = what the brain feels)
- [~] Kinetic typography for key numbers (count-ups, slams, words that react to the action)
- [~] Match cuts and morph transitions (shape of one object becomes the next) (ep 12: iris_mix iris-in from a round object)
- [ ] Texture & detail: gradients, highlights, subtle grain on the hero prop of each video
- [ ] Inside-the-body worlds: cell/organ scenes with scale cues (Kurzgesagt-style clarity)
Voice (always voice A — refine, never swap):
- [x] Calmer pace + real pauses (A4, UTMOS 4.36)
- [x] Ear-writing: rhythm, short-long sentence contrast, rule of three, contractions (ep 10)
- [~] Pause before the payoff word; lift on questions; settle on statements (ep 11 A/B: settle is UTMOS-neutral)
- [x] Per-line speed variety and stress placement tested with voice_report (ep 09)
- [x] Ear-writing + name-then-define sentence order for weak lines (ep 10, per-line UTMOS in voice_report)
- [ ] Mic-like polish: gentle de-ess, presence EQ, no harshness (check with voice_report + spectrum)
Sound:
- [~] Foley that matches the action (crunch, fizz, squelch, sizzle) synthesized per video (ep 10: record scratch, wrapper crinkle, boing, key jingle)
- [ ] Music that follows the story (build -> drop on the reveal -> soft under explanations), stems ducking
- [ ] A signature 1-second FreshNestHub audio logo
Explaining (the owner's #1 priority — people must understand what they watch):
- [x] Mayer's multimedia principles: signalling (highlight what matters), segmenting (one step per shot), coherence
      (no decoration that distracts), no redundant on-screen paragraphs (picture + short label, voice explains)
- [x] Analogies and visual metaphors for invisible things (enzymes as scissors, receptors as doorbells…)
- [x] Define-on-sight: every new term appears with its picture and a 2–4 word label the moment it is spoken
- [ ] Step diagrams that build up piece by piece (1 -> 2 -> 3) and a 5-second visual recap at the end
- [x] Scale cues: chained reference objects + powers-of-ten zoom + 'you are here' mini-map (ep 11: zoom_through, scale_ladder)
- [x] Mute test: watch the test-frame sheet without audio — can you follow the story? If not, fix the visuals
- [~] Structure for 2–3 min videos: chapters + re-hooks every 20–30 s + open loops paid off in order (ep 10: chapter_card PART 2/3)
- [x] Pre-training shot: a 3-second "cast of parts" (name the 2-3 parts with pictures) before any process explanation (ep 12: cast_card)
- [x] Worked-example contrast: "what you feel vs what's really there" split screens for every illusion/myth topic (ep 10: split_contrast)
- [x] Refutation structure for myth topics: state the myth, bust it on screen, then explain (ep 10: myth_tag)
Story & topics:
- [x] Curiosity gap + open loop in the first line, payoff placed at ~70 % of the video (ep 11: nose teaser at 5 s, paid at 85 s)
- [ ] STEPPS (Jonah Berger) for shareability: social currency, triggers, emotion, practical value, stories
- [x] Concrete comparisons people can picture ("as heavy as…", "the size of…") (ep 12: 1 m2 paper 80 g vs silver leaf < 3 g)
- [ ] One-sentence takeaway people can use today

### Journal (newest first: date | skill | what I learned (source) | used in | kept?)
- 2026-10-27 | Pre-training (explaining a PROCESS) | Mayer's pre-training principle (Multimedia Learning, ch. 10; Cambridge
  UP): people learn more deeply from a fast narrated process when they already know the NAMES and possible STATES of its
  key parts (5 of 5 tests, median d = 0.85) - e.g. a brake-system animation preceded by a tour of piston, tubes and wheel
  cylinders. Reason: the viewer otherwise has to build "what is each part" and "how they interact" at the same time.
  Turned into anim_fx.cast_card(items=[(el, NAME, STATE)]): white panels pop in one by one under a MEET THE CAST chip,
  each with its name and a state chip (LUMP > LEAF, HOLD IT, BEATS IT); the process shots after it never stop to name
  parts. Also added iris_mix() (cartoon iris-in used as a shape match cut) | ep 12 (S6 before the hammering) | yes
- 2026-10-27 | Scale cues (explaining tiny things) | Viewers can't picture "a nerve ending on your tongue" unless they
  travel there from something familiar. Explainers chain reference objects (you -> tongue -> nerve -> sensor), use one
  continuous "powers of ten" zoom with a magnification overlay, and keep a mini-map of the levels so nobody gets lost
  (Eames, "Powers of Ten" 1977; advids.co "Visualizing scale and scope" guide: chained reference objects, continuous zoom
  with a graphical scale overlay, comparative juxtaposition). Turned into anim_fx helpers: zoom_through(far, near, cx, cy)
  (push into a point, hand over to the close-up) and scale_ladder(items, cur) (row of the levels with x5/x100/x1000 chips,
  current level ringed). Paired with a colour script (warm = real, icy = felt) | ep 11 (S5 zoom + ladder S5/S6) | yes
- 2026-10-27 | Refutation text + contrasting cases (explaining a MYTH) | A refutation text states the common misconception,
  refutes it explicitly, then explains the correct idea; because the myth and the fix are active in memory at the same
  time, the new idea can win (KReC framework; "Refutation texts..." Educ Psychol Rev 2021, link.springer.com/article/
  10.1007/s10648-021-09656-z). Misconceptions are suppressed, not erased, so repeat the fix in the recap. Contrasting
  cases (Schwartz & Bransford 1998): side-by-side "belief vs reality" panels make the difference the thing you notice.
  Turned into anim_fx helpers: myth_tag() (MYTH tag -> red X + BUSTED stamp), split_contrast() (two tinted panels inside
  the safe zone, divider wipe, titled), chapter_card() (PART n signposting at re-hooks) | ep 10 (myth named at 12 s,
  busted at 16 s, explained 19–43 s, tests 43–90 s, recap re-busts it at 113 s) | yes
- 2026-10-27 | Mayer's multimedia principles (explaining) | 9 rules from Mayer's research (Ohio State multimedia-learning
  guide, u.osu.edu/multimedialearning; Mayer 2020): signalling (arrows/highlights to what matters), segmenting (short
  chunks), coherence (cut decoration + extra sound), redundancy (no on-screen text repeating narration), spatial
  contiguity (labels ON the part), temporal contiguity (picture with the word), pre-training (name parts first),
  personalization ("you"), voice. Turned into anim_fx helpers: spotlight(), label_at() with leader arrows,
  pulse_path() for signals, inset() magnifier close-ups, recap_steps(), count_up(); music drops to bass+strum under
  explanation lines | ep 09 (pre-trained: nerve -> alarm -> brain before the 'key in a lock' process) | yes
- 2026-10-26 | Squash & stretch, anticipation, slow in/out, smear, particles | 12 principles of animation (Thomas & Johnston,
  "The Illusion of Life") turned into code helpers | anim_fx.py seed, to be used from ep 09 | yes
