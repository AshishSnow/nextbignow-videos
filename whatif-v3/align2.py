import sys, wave, re, json
from pocketsphinx import Decoder
wav, txt, out = sys.argv[1:4]
words = re.findall(r"[a-zA-Z']+", open(txt).read().lower())
d = Decoder(samprate=16000, bestpath=False)
extra = {"chatgpt": "CH AE T JH IY P IY T IY", "anthropic": "AE N TH R AA P IH K", "api": "EY P IY AY",
         "openai": "OW P AH N EY AY", "chatbot": "CH AE T B AA T", "claude": "K L AO D", "token": "T OW K AH N",
         "ai": "EY AY", "apps": "AE P S", "subscriptions": "S AH B S K R IH P SH AH N Z", "dna": "D IY EH N EY", "mammoth's": "M AE M AH TH S", "wanna": "W AA N AH", "dunnart": "D AH N ER T", "megalodon": "M EH G AH L AH D AA N", "megalodons": "M EH G AH L AH D AA N Z", "kolkata": "K OW L K AA T AH", "meteorites": "M IY T IY ER AY T S", "sylacauga": "S IH L AH K AA G AH", "grabby": "G R AE B IY", "mudflat": "M AH D F L AE T", "hic": "HH IH K", "hiccuped": "HH IH K AH P T", "hiccuping": "HH IH K AH P IH NG", "misfires": "M IH S F AY ER Z", "resetting": "R IY S EH T IH NG", "maxes": "M AE K S IH Z", "chyo": "CH Y OW", "crewmate": "K R UW M EY T", "seabirds": "S IY B ER D Z", "smoothie": "S M UW DH IY", "mumbai": "M UH M B AY", "shanghai": "SH AE NG HH AY", "snailfish": "S N EY L F IH SH", "mariana": "M EH R IY AA N AH", "tambora": "T AE M B AO R AH", "seafloor": "S IY F L AO R", "dimorphos": "D AY M AO R F AH S", "atms": "EY T IY EH M Z", "olympus": "AH L IH M P AH S", "mons": "M AA N Z", "uranus": "Y UH R AH N AH S", "venera": "V EH N EH R AH", "windiest": "W IH N D IY AH S T", "spaghettification": "S P AH G EH T AH F AH K EY SH AH N", "quintillion": "K W IH N T IH L Y AH N", "midges": "M IH JH AH Z", "pollinators": "P AA L AH N EY T ER Z", "pollinate": "P AA L AH N EY T", "dinosauroid": "D AY N AH S AO R OY D", "rex": "R EH K S", "microsleeps": "M AY K R OW S L IY P S", "phytoplankton": "F AY T OW P L AE NG K T AH N", "shrews": "SH R UW Z", "leblanc": "L AH B L AA NG K", "kola": "K OW L AH", "superdeep": "S UW P ER D IY P", "borehole": "B AO R HH OW L", "lichtenberg": "L IH K T AH N B ER G", "cpr": "S IY P IY AA R", "photosphere": "F OW T AH S F IH R", "corona": "K ER OW N AH", "reticulated": "R IH T IH K Y AH L EY T IH D", "humpbacks": "HH AH M P B AE K S", "humpback's": "HH AH M P B AE K S", "otis": "OW T IH S", "elisha": "IH L AY SH AH", "juliane": "JH UW L IY AA N", "koepcke": "K EH P K AH", "lumberjacks": "L AH M B ER JH AE K S", "vulovic": "V UW L AH V IH CH", "nightlight": "N AY T L AY T", "io": "AY OW", "phobos": "F OW B OW S", "mars's": "M AA R Z IH Z", "fingernails": "F IH NG G ER N EY L Z", "saturn's": "S AE T ER N Z", "jupiter's": "JH UW P IH T ER Z", "apollo": "AH P AA L OW"}
for w, p in extra.items():
    if d.lookup_word(w) is None:
        d.add_word(w, p, True)
print("missing:", [w for w in set(words) if d.lookup_word(w) is None])
d.set_align_text(" ".join(words))
w = wave.open(wav, 'rb'); data = w.readframes(w.getnframes())
d.start_utt(); d.process_raw(data, full_utt=True); d.end_utt()
segs = [(s.word, s.start_frame / 100.0, (s.end_frame + 1) / 100.0) for s in d.seg()]
json.dump(segs, open(out, 'w'))
print(len([s for s in segs if s[0] not in ('<s>', '</s>', '<sil>')]), "aligned of", len(words))
