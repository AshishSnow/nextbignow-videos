# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 27 — "Why do you feel sleepy after a big meal?" Facts (verified 7 Nov 2026):
# - Blood-away-from-the-brain idea: 'At one time, researchers believed that blood flowing away from your brain after a meal led to a food coma. Now, they know this isn't accurate.' (Cleveland Clinic, Food coma, 2025); 'scientific evidence has debunked this myth' (Sleep Foundation, Oct 2025); Healthline 2022: 'unlikely'.
# - Body clock dip: early afternoon (Cleveland Clinic; Sleep Foundation 'circadian wake signals tend to decrease in the early afternoon'); 'around 2-4 p.m.' (Healthline); 'you may still experience the post-lunch dip even if you skip lunch' (Sleep Foundation); meals lengthened an afternoon nap but did not induce it (older study via Healthline).
# - Meal signals: 'signals from your gut', 'changes in blood metabolites like glucose and amino acids', 'shifts in your brain's arousal pathways' (Cleveland Clinic); orexin 'is inhibited after you eat' (Healthline); glucose 'switches off the neurons' for orexin (ScienceABC); 'drop in hormones that maintain alertness' (Sleep Foundation).
# - Bigger meal = stronger: 'stronger after larger, higher-energy meals' (Cleveland Clinic); 'A lighter meal with fewer calories will likely lead to less sleepiness' (Sleep Foundation); Healthline.
# - Pizza study: 'eat until you cannot manage another bite' vs 'comfortably full'; 'almost twice as much pizza'; 'Four hours after eating maximally, the participants felt sleepy/lethargic' (University of Bath 2020 + ScienceDaily; Br J Nutr; also via Healthline).
# - Not fully understood: Cleveland Clinic 'Researchers still aren't clear'; Healthline 'scientists don't yet fully understand'; ScienceABC.
# - Fixes: smaller meals (Cleveland Clinic, Sleep Foundation, Healthline); a 10-15 min walk (Cleveland Clinic Health Essentials; Cleveland Clinic 10-30 min); sleep (Cleveland Clinic, Sleep Foundation, Healthline); don't drive sleepy after a meal (Cleveland Clinic; Healthline driving study).
# - Doctor: frequent/severe sleepiness or diabetes symptoms (Cleveland Clinic); tired after eating along with thirst, frequent urination (Healthline).
# VOICE upgrade (ep 27): WIDE-RANGE REVEALS: the 5 payoff lines (i3, a1, b1, b5, c2) get range_expand 1.55-1.6 + base +1.0-1.2 so the f0 range climbs back from ep 25's 15.7 st.
LINES = [
    ("i1", "Do you know that sleepy feeling after a big meal isn't your blood leaving your brain?", 1.00, 0.3, +1.0, 1.5, ["sleepy", "brain?"], "q"),
    ("i2", "That's the story we all grew up with. Your stomach steals the blood, your brain runs dry, and you're out.", 1.07, 0.25, +0.4, 1.45, ["steals", "out.:dn"], "low"),
    ("i3", "Scientists checked. It's a myth.", 1.0, 0.25, +1.2, 1.6, ["myth.:dn"], "low"),
    ("i4", "So tomorrow's Diwali lunch nap is going to need a new excuse.", 1.02, 0.45, -0.6, 1.4, ["new"], "low"),
    ("a0", "What's really going on is two things, and one of them happens even if you skip lunch.", 1.06, 0.4, +0.8, 1.5, ["two", "skip"], "low"),
    ("a1", "Thing one is your body clock.", 1.0, 0.2, +1.0, 1.55, ["clock."], "low"),
    ("a2", "It runs your day in waves, and in the early afternoon, around two to four, there's a little dip.", 1.07, 0.1, +0.4, 1.45, ["waves,", "dip.:dn"], "low"),
    ("a3", "Your wake-up signals ease off. Skip lunch completely, and the dip still shows up.", 1.06, 0.3, +0.4, 1.45, ["still"], "low"),
    ("a4", "So lunch doesn't start the slump. It just lands right on top of it.", 1.03, 0.45, -0.6, 1.4, ["start", "top"], "low"),
    ("b1", "Thing two is the meal itself.", 1.0, 0.2, +1.0, 1.55, ["meal"], "low"),
    ("b2", "As food arrives, your gut starts sending messages up to your brain, and your blood sugar shifts too.", 1.08, 0.1, +0.4, 1.45, ["messages"], "low"),
    ("b3", "One of the chemicals that keeps you awake is called orexin, and after you eat, it gets turned down.", 1.07, 0.3, +0.4, 1.45, ["awake", "down.:dn"], "low"),
    ("b4", "Think of it like a dimmer switch on how alert you feel. A meal nudges it down.", 1.04, 0.25, +0.4, 1.45, ["dimmer"], "low"),
    ("b5", "And the bigger the meal, the further it goes.", 1.0, 0.45, +1.2, 1.6, ["bigger", "further"], "low"),
    ("c1", "In one study, men ate pizza until they couldn't manage another bite. Almost twice as much as normal.", 1.07, 0.25, +0.8, 1.45, ["another", "twice"], "low"),
    ("c2", "Four hours later? Still sleepy.", 1.0, 0.45, +0.4, 1.6, ["Four", "sleepy.:dn"], "low"),
    ("c3", "To be fair, scientists still don't know every piece of this. But the blood part? That one's settled.", 1.05, 0.5, -0.6, 1.4, ["every", "settled.:dn"], "low"),
    ("d0", "So, Diwali lunch tomorrow. How do you stay awake?", 1.0, 0.3, +1.0, 1.5, ["awake?"], "q"),
    ("d1", "One, a smaller plate. You can always go back for seconds later.", 1.04, 0.25, +0.8, 1.45, ["smaller", "later.:dn"], "low"),
    ("d2", "Two, walk it off. Ten or fifteen minutes, right after you eat.", 1.04, 0.25, +0.8, 1.45, ["walk", "after"], "low"),
    ("d3", "Three, get a proper night's sleep tonight.", 1.02, 0.25, +0.8, 1.45, ["proper"], "low"),
    ("d4", "And if your eyes feel heavy, don't drive. Hand someone else the keys.", 1.03, 0.4, -0.3, 1.35, ["drive.", "keys.:dn"], "low"),
    ("e1", "If you're wiped out after nearly every meal, or you're always thirsty too, it's worth seeing a doctor.", 1.06, 0.45, -0.3, 1.35, ["every", "doctor.:dn"], "low"),
    ("f1", "So it's your body clock, plus a dimmer switch. Not your blood running away.", 1.02, 0.3, +0.8, 1.5, ["clock,", "dimmer", "away.:dn"], "low"),
    ("f2", "Send this to whoever's planning a nap right after Diwali lunch.", 1.03, 0.0, +0.8, 1.45, ["nap"], "low"),
]
