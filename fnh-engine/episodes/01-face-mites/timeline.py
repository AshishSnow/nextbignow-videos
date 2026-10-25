"""work/align.json -> work/timeline.json — FreshNestHub 'Tiny bugs live inside your face' (Demodex), host NESSA."""
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


ev = dict(
    t_tiny=F("hook", "tiny"), t_bugs=F("hook", "bugs…"), t_living=F("hook", "living"), t_inside=F("hook", "INSIDE"), t_face0=F("hook", "face."),
    t_right=F("hook", "Right"), t_now=F("hook", "now."),
    t_called=F("name", "called"), t_demodex=F("name", "Demodex"), t_mites=F("name", "mites…"), t_almost=F("name", "almost"), t_every=F("name", "EVERY"),
    t_adult=F("name", "adult"), t_them=F("name", "them!"),
    t_allday=F("day", "All"), t_hide=F("day", "hide"), t_headdown=F("day", "head-down"), t_pores=F("day", "pores…"), t_eating=F("day", "eating"),
    t_oil=F("day", "oil."),
    t_night=F("night", "night…"), t_while=F("night", "while"), t_sleep=F("night", "sleep…"), t_crawl=F("night", "crawl"), t_out=F("night", "out…"),
    t_to=F("mate", "to"), t_mate=F("mate", "MATE."), t_on=F("mate", "On"), t_face=F("mate", "FACE!"),
    t_even=F("party", "even"), t_hormone=F("party", "hormone"), t_skin=F("party", "skin"), t_atnight=F("party", "night…"), t_party=F("party", "party"),
    t_morning=F("party", "morning."),
    t_second=F("wake", "second"), t_wake=F("wake", "wake"), t_dive=F("wake", "dive"), t_back=F("wake", "back"), t_in=F("wake", "in."),
    t_got=F("mom", "got"), t_from=F("mom", "from"), t_mom=F("mom", "MOM!"),
    t_many=F("itchy", "many"), t_red=F("itchy", "Red,"), t_itchy=F("itchy", "itchy"),
    t_love=F("lashes", "LOVE"), t_lashes=F("lashes", "eyelashes…"), t_always=F("lashes", "always"), t_makeup=F("lashes", "makeup"),
    t_off=F("lashes", "off"), t_bed=F("lashes", "bed."),
    t_because=F("loop", "Because"), t_tonight=F("loop", "tonight…"), t_not=F("loop", "not"), t_sleeping=F("loop", "sleeping"),
    t_alone=F("loop", "alone."),
)

b = {}
b["H1"] = 0.0
b["NM"] = lines["name"]["start"] - 0.12
b["EV"] = ev["t_almost"] - 0.12
b["DY"] = lines["day"]["start"] - 0.12
b["NT"] = lines["night"]["start"] - 0.15
b["MT"] = ev["t_to"] - 0.10
b["PT"] = lines["party"]["start"] - 0.12
b["WK"] = lines["wake"]["start"] - 0.12
b["MO"] = lines["mom"]["start"] - 0.12
b["IT"] = lines["itchy"]["start"] - 0.12
b["LS"] = lines["lashes"]["start"] - 0.12
b["MK"] = ev["t_always"] - 0.30
b["LP"] = lines["loop"]["start"] - 0.15
ORDER = ["H1", "NM", "EV", "DY", "NT", "MT", "PT", "WK", "MO", "IT", "LS", "MK", "LP"]
TRANS = {"NM": "whip", "EV": "pop", "DY": "zoomblur", "NT": "dip", "MT": "punch", "PT": "flashp", "WK": "flash", "MO": "whip", "IT": "zoomblur",
         "LS": "whip", "MK": "pop", "LP": "dip"}
shots = [dict(id=k, start=round(b[k], 3), end=round(b[ORDER[i + 1]], 3) if i + 1 < len(ORDER) else END, trans=TRANS.get(k, "cut"))
         for i, k in enumerate(ORDER)]
json.dump(dict(lines=lines, words=WD, shots=shots, events=ev, END=END, LEAD=LEAD), open(f"{S}/work/timeline.json", "w"), indent=1)
print("END", END)
for s in shots:
    print(f"{s['id']:4s} {s['start']:6.2f} -> {s['end']:6.2f} ({s['end'] - s['start']:.2f}s) in:{s['trans']}")
