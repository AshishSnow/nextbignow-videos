# Storyboard — YOUR MOVE · EP 1 · Part 2 (Pepsi jet: the court case). Same look and music family as Part 1 (a variation, not the same cue).
New template asset: `set_view("courtroom")` (wood panels, bench, two tables, gallery rows; warm light). Judge look:
`who={"base": "lady", "top": (28, 26, 32), "outfit": "coat"}` (black robe). Lawyers: `exec` looks. The ad is shown only as our own
cartoon re-staging inside a TV frame — never real footage. Quotes from the opinion go on quote cards with "Leonard v. PepsiCo (S.D.N.Y. 1999)".

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX / camera |
|---|---|---|---|---|
| i1 "Part two. You mailed Pepsi a check for a jet. Will a judge make them deliver?" | courtroom WIDE, jet visible through a tall window (dusk) | hero at the plaintiff table, judge's bench above | `part_badge("PART 2", "EP 1 · THE PEPSI JET")` in frame 1 | gavel echo |
| i2 recap: raised $700,000; jet worth over $20M | quick 2-panel recap: money bags → jet | — | `say("$700,000")` then `say("$20M+ JET")` | whoosh ×2 |
| a1 "Here's what really happened. You don't drop it. You sue." | hero slams a folder on the table | determined | `say("YOU SUE")` | slam + small shake |
| a2 "But Pepsi moves too…owes you nothing." | opposing table: three lawyers stand up in sync | lawyers `brow="sus"` | stamp "COURT FILING" on a document | papers |
| a3 "Three questions will decide who wins." | judge CU, low angle | — | three question pills appear (roadmap) | ding ×3 |
| b1 "Question one. Was the ad a real offer?" | TV on a cart in court, our re-staged ad | — | pill 1 lit | — |
| b2 "Usually, an ad isn't a promise. It's an invitation to come and buy." | street shop window with a SALE poster | hero shrugs | `say("AD ≠ PROMISE")` | — |
| b3 "And the jet isn't even in the prize catalog." | catalog CU, page flips — no jet | — | red ✕ over an empty catalog slot | page flip, buzzer |
| c1 "Question two. Would a normal person believe it?" | gallery rows of generic people | crowd looks at each other | pill 2 lit | murmur |
| c2 "The judge watches the ad. A teen flies a fighter jet to school." | judge watching the TV, jet on screen | judge `brow="up"` | — | tiny jet sound from TV |
| c3 "She calls it an exaggerated adolescent fantasy." | quote card over the judge CU | — | **quote card**: "exaggerated adolescent fantasy" + source chip | — |
| d1 "Question three. Where's the signed contract?" | table top: empty space where a contract should be | hero searching | pill 3 lit | — |
| d2 "A deal this big needs one in writing. There isn't one." | empty signature line CU | — | `say("NO SIGNED DEAL")` | pen click |
| d3 "August 1999. The ruling: no objective person could think…" | judge CU → gavel slam | — | `hud_clock(f, "AUG 1999", "NEW YORK", "THE RULING")`; quote card with the exact quote | **gavel**, shake |
| d4 "You appeal. You lose again. No jet." | hero walks down courthouse steps, rain | sad | stamp "APPEAL DENIED (2000)" | rain |
| d5 "…the Pentagon said that jet isn't sold to civilians unless it's demilitarized." | the jet in a hangar, a "NOT FOR CIVILIANS" tag | — | caption "demilitarized = weapons and military parts removed" (small, explains the word) | hangar echo |
| t1 "But Pepsi changed the ad: seven hundred million points… just kidding." | TV CU: the re-staged ad's last frame now shows 700,000,000 + "JUST KIDDING" | hero stares | number rolls 7,000,000 → 700,000,000 | number roll |
| t2 **"Oops."** | hero turns to camera | smirk | OOPS stamp | **Oops sting** |
| e1 "The takeaway? Price every joke like someone will pay it." | marketing desk with a price tag on a toy jet | — | `say("PRICE EVERY JOKE")` | — |
| e2 "Was the judge right? Comment FAIR or ROBBED." | **end card** | hero to camera | `hud_choice(f, "WAS THE JUDGE RIGHT?", "FAIR  or  ROBBED", y≈1450)` | choice whoosh |
| e3 "Send this to the friend who'd mail that check." | end card holds, cheque flutters across | hero waves the cheque | series badge | — |

Loop: end on the courtroom window with the jet outside (frame 1 composition).
Post copy: first line "A judge decided if Pepsi owed a 21-year-old a fighter jet." · "Your Move · Ep 1 · Part 2" · firstCommentText "FAIR or ROBBED?"
YouTube title "Did Pepsi Owe Him a Fighter Jet? | Your Move" (≤ 50 chars).
