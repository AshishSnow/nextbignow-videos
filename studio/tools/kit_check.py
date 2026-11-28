#!/usr/bin/env python3
"""kit_check — doodle pre-flight: does template/scripts/doodlekit.py have every asset a doodle shots.md asks for?
(board_check.py is whiteboard-only; R&D 28 Nov 2026.) Reads the 'NEW kit assets:' and 'Existing:' paragraphs of shots.md,
takes every `backticked` name and bare word before '(' / ',' in 'Existing:', and checks it against the kit's defs + char() kinds.
Usage: python3 studio/tools/kit_check.py studio/episodes/queue/<NN-slug> [...]   (exit 1 if anything is missing)"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.join(HERE, "../template/scripts/doodlekit.py")
# names a storyboard uses for something the kit already draws under another name
ALIAS = {"tiktok_phone": "phone_video", "census_pie": "pie", "cockroach_doodle": "cockroach", "storefront_plain": "store",
         "fryer_basket": "fryer", "receipt": "receipt_printer", "chart arrow": "arrow",
         "gavel": "gavel", "you": "char"}


def kit_names():
    src = open(KIT).read()
    defs = set(re.findall(r"^def (\w+)\(", src, re.M))
    kinds = set(re.findall(r'"(\w+)": _\w+', src.split("def char(")[1].split("\n\n")[0]))
    return defs, kinds


def asked(shots):
    txt = open(shots).read().split("| Line |")[0]
    m = re.search(r"NEW kit assets[^:]*:(.*?)(?:\n\n|\n\|)", txt, re.S)
    new = re.findall(r"`([\w ]+?)(?:\(\))?`", m.group(1)) if m else []
    ex = re.search(r"Existing:(.*?)(?:\n\n|\n\||$)", txt, re.S)
    old = [w.strip().split("(")[0].strip() for w in re.split(r",|\.", ex.group(1)) if w.strip()] if ex else []
    return new, [o for o in old if o and len(o) < 30]


def check(ep):
    shots = os.path.join(ep, "shots.md"); defs, kinds = kit_names(); miss = []
    new, old = asked(shots)
    for n in new + old:
        key = n.strip().lower().replace(" ", "_")
        key = ALIAS.get(n.strip().lower(), ALIAS.get(key, key))
        ok = key in defs or key.lstrip("_") in kinds or ("_" + key.lstrip("_")) in defs
        if not ok: miss.append(n)
    print(f"{os.path.basename(ep.rstrip('/'))}: {len(new)} new + {len(old)} existing asked, missing {len(miss)}" + (f" -> {', '.join(miss)}" if miss else " — READY"))
    return not miss


if __name__ == "__main__":
    ok = all([check(a) for a in sys.argv[1:]])
    sys.exit(0 if ok else 1)
