"""work/align.json -> work/timeline.json — FreshNestHub 'red lipstick made of bugs' (carmine), host NESSA."""
import json, sys, re
sys.path.insert(0, "/home/claude/reel-kit/english/scripts")
from vo_lines import LINES

S = "/home/claude/reel-kit/english"
AL = json.load(open(f"{S}/work/align.json"))
LEAD = 0.25
WD = {}
for w in AL["words"]:
    WD.setdefault(w["line"], []).append(dict(w=w["w"], t=round(w["t"] + LEAD, 3)))
lines = {lid: dict(start=round(AL["lines"][lid]["start"] + LEAD, 3), end=round(AL["lines"][lid]["end"] + LEAD, 3)) for lid, _ in LINES}
END = round(lines["loop"]["end"] + 0.45, 3)


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def F(lid, sub, nth=0):
    return [x["t"] for x in WD[lid] if norm(sub) == norm(x["w"])][nth]


ev = dev = dict(
    t_doyou=F("intro", "Do"), t_red0=F("intro", "red"), t_lipstick0=F("intro", "lipstick"), t_might=F("intro", "might"), t_made=F("intro", "made"),
    t_bugs0=F("intro", "BUGS?"),
    t_called=F("name", "called"), t_carmine=F("name", "carmine…"), t_comes=F("name", "comes"), t_tiny=F("name", "tiny"), t_insects=F("name", "insects"),
    t_cochineal=F("name", "cochineal!"),
    t_live=F("cactus", "live"), t_prickly=F("cactus", "prickly"), t_cactus=F("cactus", "cactus…"), t_mostly=F("cactus", "mostly"), t_peru=F("cactus", "Peru."),
    t_only=F("crush", "Only"), t_females=F("crush", "females"), t_used=F("crush", "used…"), t_dried=F("crush", "dried…"), t_and=F("crush", "and"),
    t_crushed=F("crush", "crushed."),
    t_seventy=F("count", "Seventy"), t_thousand=F("count", "THOUSAND"), t_bugs=F("count", "bugs…"), t_just=F("count", "just"), t_one=F("count", "ONE"),
    t_pound=F("count", "pound"), t_dye=F("count", "dye!"),
    t_but=F("wait", "But"), t_wait=F("wait", "wait…"), t_not=F("wait", "not"), t_lip2=F("wait", "lipstick."), t_its=F("wait", "It's", 1),
    t_yogurt=F("wait", "yogurt,"), t_candy=F("wait", "candy"), t_ice=F("wait", "ice"), t_too=F("wait", "too!"),
    t_few=F("allergy", "few"), t_people=F("allergy", "people…"), t_cause=F("allergy", "cause"), t_allergic=F("allergy", "allergic"),
    t_reactions=F("allergy", "reactions."),
    t_check=F("tip", "check"), t_label=F("tip", "label"), t_carmine2=F("tip", "carmine,"), t_coch2=F("tip", "cochineal"), t_extract=F("tip", "extract,"),
    t_e=F("tip", "E"), t_twenty=F("tip", "twenty."),
    t_next=F("loop", "next"), t_put=F("loop", "put"), t_redl=F("loop", "red"), t_lip3=F("loop", "lipstick…"), t_ask=F("loop", "ask"),
    t_yourself=F("loop", "yourself…"),
)

b = {}
b["H1"] = 0.0
b["NM"] = lines["name"]["start"] - 0.12
b["CA"] = lines["cactus"]["start"] - 0.12
b["CR"] = lines["crush"]["start"] - 0.15
b["CS"] = ev["t_dried"] + 0.55
b["CT"] = lines["count"]["start"] - 0.12
b["WT"] = lines["wait"]["start"] - 0.10
b["FD"] = ev["t_its"] - 0.15
b["AL"] = lines["allergy"]["start"] - 0.12
b["LB"] = lines["tip"]["start"] - 0.12
b["TC"] = ev["t_coch2"] - 0.15
b["LP"] = lines["loop"]["start"] - 0.15
b["LQ"] = ev["t_ask"] - 0.2
ORDER = ["H1", "NM", "CA", "CR", "CS", "CT", "WT", "FD", "AL", "LB", "TC", "LP", "LQ"]
TRANS = {"NM": "whip", "CA": "zoomblur", "CR": "dip", "CS": "punch", "CT": "flash", "WT": "pop", "FD": "whip", "AL": "zoomblur",
         "LB": "pop", "TC": "whip", "LP": "dip", "LQ": "punch"}
shots = [dict(id=k, start=round(b[k], 3), end=round(b[ORDER[i + 1]], 3) if i + 1 < len(ORDER) else END, trans=TRANS.get(k, "cut"))
         for i, k in enumerate(ORDER)]
json.dump(dict(lines=lines, words=WD, shots=shots, events=ev, END=END, LEAD=LEAD), open(f"{S}/work/timeline.json", "w"), indent=1)
print("END", END)
for s in shots:
    print(f"{s['id']:4s} {s['start']:6.2f} -> {s['end']:6.2f} ({s['end'] - s['start']:.2f}s) in:{s['trans']}")
