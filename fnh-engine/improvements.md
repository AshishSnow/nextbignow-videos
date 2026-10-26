# FreshNestHub — continuous improvement (read + update EVERY run)

**Owner, 26 Oct 22:59: "It's not about views or post numbers — just learn new things and keep improving, every day,
every run, voice AND visuals AND topics."** Numbers are only a compass; the goal is to get better at the craft every
single run, and to never stop learning. Never write "nothing to improve".

The owner's standing order (26 Oct 2026): "Don't settle. With every video improve: more natural voice, better video.
Understand the new algorithm and act on it — I shouldn't have to tell you every time." Growth takes time; quality and
learning beat speed. Every run must leave the channel a little better than it found it.

## A. Algorithm notes (re-check EVERY DAY: the first run of each IST day, i.e. when "Last checked" is not today; record what changed)
Last checked: 2026-10-26. Sources: Kompozy (Sep 2026, Mosseri signals), Creator Lane (2026), Gyre (2026),
Socialync (2026), Android Headlines / TechCrunch (Jul 2026, YouTube monetization rules).
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
- Last trend scan: (none yet)

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
- [ ] Per-line speed variety: questions/reveals 0.96–0.98, fast lists 1.04, punchlines slower; never all 1.0.
- [ ] Write for the ear: contractions, short words, "you" talk; split lines > 14 words; punctuation for natural pauses.
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
- 2026-10-26: realistic-looking hooks held 60–71 % past 3 s vs 56–58 % for our first animated style and 5–16 % for
  static openings; ambergris (money stakes + story) had the longest avg watch (37.9 s). Broad "is your X fake / how
  much water" topics got the biggest reach (4.7–5.6k).

## E. Changelog (one line per video)
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
- [ ] Arcs: move props and limbs along curves, not straight lines
- [ ] Timing & spacing: hold key poses 6–10 frames, fast in-betweens (snappy cartoon timing)
- [ ] Exaggeration: bigger expressions at reveals (eyes pop, jaw drop, double take)
- [ ] Character acting: eye direction leads action, blinks on cuts, reaction shots
- [ ] Simple lip-sync visemes for Chubby when he talks (mouth shapes from the VO envelope + vowels)
- [ ] Camera language: push-in on reveals, whip pans between ideas, low/high angles, rack focus (`cam_keys`, `push_in`)
- [ ] Depth: parallax background layers, foreground elements passing the camera, atmospheric perspective
- [ ] Lighting: rim light and soft ambient-occlusion shadows on props; light rays on reveals
- [ ] Colour script: plan the colour arc of the video (calm -> tension -> payoff) instead of random schemes
- [ ] Kinetic typography for key numbers (count-ups, slams, words that react to the action)
- [ ] Match cuts and morph transitions (shape of one object becomes the next)
- [ ] Texture & detail: gradients, highlights, subtle grain on the hero prop of each video
- [ ] Inside-the-body worlds: cell/organ scenes with scale cues (Kurzgesagt-style clarity)
Voice (always voice A — refine, never swap):
- [x] Calmer pace + real pauses (A4, UTMOS 4.36)
- [ ] Ear-writing: rhythm, short-long sentence contrast, rule of three, contractions
- [ ] Pause before the payoff word; lift on questions; settle on statements
- [ ] Per-line speed variety and stress placement tested with voice_report
- [ ] Mic-like polish: gentle de-ess, presence EQ, no harshness (check with voice_report + spectrum)
Sound:
- [ ] Foley that matches the action (crunch, fizz, squelch, sizzle) synthesized per video
- [ ] Music that follows the story (build -> drop on the reveal -> soft under explanations), stems ducking
- [ ] A signature 1-second FreshNestHub audio logo
Explaining (the owner's #1 priority — people must understand what they watch):
- [ ] Mayer's multimedia principles: signalling (highlight what matters), segmenting (one step per shot), coherence
      (no decoration that distracts), no redundant on-screen paragraphs (picture + short label, voice explains)
- [ ] Analogies and visual metaphors for invisible things (enzymes as scissors, receptors as doorbells…)
- [ ] Define-on-sight: every new term appears with its picture and a 2–4 word label the moment it is spoken
- [ ] Step diagrams that build up piece by piece (1 -> 2 -> 3) and a 5-second visual recap at the end
- [ ] Scale cues (hand, coin, Chubby next to the thing) so viewers know how big/small it is
- [ ] Mute test: watch the test-frame sheet without audio — can you follow the story? If not, fix the visuals
- [ ] Structure for 2–3 min videos: chapters + re-hooks every 20–30 s + open loops paid off in order
Story & topics:
- [ ] Curiosity gap + open loop in the first line, payoff placed at ~70 % of the video
- [ ] STEPPS (Jonah Berger) for shareability: social currency, triggers, emotion, practical value, stories
- [ ] Concrete comparisons people can picture ("as heavy as…", "the size of…")
- [ ] One-sentence takeaway people can use today

### Journal (newest first: date | skill | what I learned (source) | used in | kept?)
- 2026-10-26 | Squash & stretch, anticipation, slow in/out, smear, particles | 12 principles of animation (Thomas & Johnston,
  "The Illusion of Life") turned into code helpers | anim_fx.py seed, to be used from ep 09 | yes
