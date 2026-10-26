# FreshNestHub — continuous improvement (read + update EVERY run)

The owner's standing order (26 Oct 2026): "Don't settle. With every video improve: more natural voice, better video.
Understand the new algorithm and act on it — I shouldn't have to tell you every time." Growth takes time; quality and
learning beat speed. Every run must leave the channel a little better than it found it.

## A. Algorithm notes (re-check with WebSearch when "last checked" is older than 7 days; record what changed)
Last checked: 2026-10-26. Sources: Kompozy (Sep 2026, Mosseri signals), Creator Lane (2026), Gyre (2026),
Socialync (2026), Android Headlines / TechCrunch (Jul 2026, YouTube monetization rules).
1. **First 2–3 seconds decide distribution.** Instagram: watch time, likes per reach and **sends per reach** are the
   top signals (Mosseri); reels holding > 60 % of viewers past 3 s reportedly get several times the reach.
   YouTube Shorts: "viewed vs swiped away" in the feed, then completion/average % viewed decides how far it travels.
   => Frame 0 already moving, Chubby + the object + the question on screen inside 1.5 s; no slow build-up.
2. **Retention/completion is the main Shorts signal.** Third-party guides: 30–60 s Shorts want ≈ 50 %+ average view;
   cut or change the picture every 2–4 s (nothing static > 4 s); an ending that flows back into the opening helps loops.
   => Keep videos 40–55 s unless our own data says longer holds; tease the best fact early ("and the last one is wild").
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

## B. Per-run improvement protocol (mandatory)
1. Refresh performance.md (step 1 of PLAYBOOK). Compare the last 3–5 CHUBBY videos on 3-s hold, avg watch %, shares
   and saves per 1k reach. Write 1–2 dated learnings in section D (what worked / what didn't, with numbers).
2. Pick **at least 2 upgrades** for this video — one VOICE, one VISUAL/EDIT — from the backlog (section C) or from
   the learnings. Prefer the item most likely to raise 3-s hold or watch %. Keep each change small and testable.
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
Visual / edit:
- [ ] Chubby is often small in a corner — make him the actor (big, in the middle of the action, interacting with props).
- [ ] Break the "big circle + prop" sameness: full-bleed scenes, split screens, close-ups, top-down tables, inside-the-body
      worlds, camera push-ins/pans, parallax layers. No two consecutive shots with the same layout.
- [ ] Frame 0 hook: motion already happening at t=0 (no pop-in from empty), cover frame = Chubby + object + question.
- [ ] Secondary motion everywhere (bob, squash on impacts, blinking, props wobble) so nothing is static > 2 s.
- [ ] Kinetic numbers: count-ups / slams for key numbers; consistent sources chip.
- [ ] Better diagrams: more detail and texture (highlights, rim light, subtle 3D shadows) on the main prop each video.
- [ ] Sound design: a signature 1-s FreshNestHub sting; foley that matches the action (squelch, fizz, sizzle).
Script / packaging:
- [ ] Hook with stakes in < 2 s; tease the best fact early; loop the last line into the first.
- [ ] Practical takeaway line in every video (what to do with this fact) — boosts saves/shares.
- [ ] Comment question in caption + firstCommentText.

## D. Learnings (newest first, dated, with numbers)
- 2026-10-26: realistic-looking hooks held 60–71 % past 3 s vs 56–58 % for our first animated style and 5–16 % for
  static openings; ambergris (money stakes + story) had the longest avg watch (37.9 s). Broad "is your X fake / how
  much water" topics got the biggest reach (4.7–5.6k).

## E. Changelog (one line per video)
- 07 carrots (26 Oct, interactive): new CHUBBY v4 style baseline (owner approved). Voice A, 19 shots, food-funk score.
- 08 pineapple (26 Oct, auto run): same style; calypso score. Review: good consistency, but Chubby small in corners in
  ~half the shots and many "big circle + prop" layouts — next runs: make Chubby the actor + vary layouts.
