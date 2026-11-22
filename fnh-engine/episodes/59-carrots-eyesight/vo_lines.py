# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 59 — "Do carrots improve your eyesight?" (35-50 s rule; ONE takeaway: carrots don't give you better or night vision - the
# 'see in the dark' story was a WWII cover for radar; vitamin A only helps if you're short of it).
# Shape: elder-said myth (mom) -> the ORIGIN STORY twist (first history reveal on the channel) as the payoff at ~40 %, then the honest part
# (carrots -> vitamin A -> dim-light vision, only fixes a shortage), safe tip, send line calls back to mom.
# VOICE upgrade (ep 59): QUOTE REGISTER - reported speech ('the papers said, ...') on its own LINKED line (pause 0.1 before it) at a higher
# base + wider range, like a person doing a voice; A/B vs the merged line.
# Facts (verified 22 Nov 2026):
# - Smithsonian Magazine (A WWII propaganda campaign popularized the myth that carrots help you see in the dark): 'In 1940, RAF fighter ace
#   John Cunningham, nicknamed "Cat's Eyes," became the first British pilot to shoot down an enemy plane with A.I. radar'; 'The government told
#   newspapers that the reason for the RAF's success was the fact that pilots like Cunningham ate an excess of carrots'; posters said carrots
#   'help you to see' during blackouts; beta carotene -> vitamin A; lacking it 'can cause night blindness'; vitamin A 'can reverse poor vision
#   caused by a deficiency, it will not strengthen eyesight ... in people who are healthy'.
# - Scientific American 'Fact or Fiction?: Carrots Improve Your Vision': the RAF 'pushed that message as a cover-up for the recently adopted radar
#   technology'; vitamin A 'helps the eye convert light into a signal ... under conditions of low light'; 'Binging on carrots would also not improve
#   most Americans' eyesight'; most eye problems (genetics, aging, diabetes) 'cannot be aided with an infusion of beta-carotene'.
# - Live Science 'Can carrots give you night vision?': radar 'gave them the edge, not the airman's diet'; carrots 'can help to improve vision for
#   someone who is lacking in vitamin A, but it won't help people who already have adequate vitamin A levels achieve better vision.'
# - UT Austin 'Think Twice' (2022): vitamin A is part of rhodopsin in the rod cells; it does 'not improve sight in individuals that have sufficient vitamin A.'
LINES = [
    ("i1", "Do you know if eating carrots can actually make you see better?", 0.97, 0.25, +1.0, 1.55, ["better?"], "q"),
    ("i2", "Your mom says yes, even in the dark. But that story started as a wartime cover-up.", 1.0, 0.35, +0.8, 1.55, ["cover-up.:dn"], "low"),
    ("a1", "In nineteen-forty, British pilots kept shooting down planes at night.", 1.02, 0.1, +0.6, 1.5, ["night."], "low"),
    ("a1q", "And the papers said, they eat loads of carrots!", 1.0, 0.35, +1.4, 1.65, ["carrots!"], "low"),
    ("a2", "The real secret was a brand-new radar in the plane. The carrots? Just a cover story.", 0.98, 0.35, +1.2, 1.6, ["radar"], "low"),
    ("b1", "Carrots do help a bit. Your body turns them into vitamin A, and your eyes need it to see in dim light.", 1.02, 0.3, +0.6, 1.5, ["vitamin"], "low"),
    ("b2", "But extra carrots won't give you night vision. They only help if you're short on vitamin A.", 1.0, 0.3, +0.8, 1.55, ["night"], "low"),
    ("c1", "And if things still look blurry, carrots won't fix that. It's time to get your eyes checked.", 1.0, 0.3, -0.3, 1.35, ["checked.:dn"], "low"),
    ("c2", "Send this to the mom who still says, eat your carrots, you'll see in the dark!", 1.02, 0.0, +0.8, 1.45, ["dark!"], "low"),
]
