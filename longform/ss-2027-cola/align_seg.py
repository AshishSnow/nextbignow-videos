"""Segment-wise forced alignment for long voiceovers: align each segments.json chunk separately, then offset."""
import sys, wave, re, json
from pocketsphinx import Decoder
sys.argv = sys.argv  # wav, segments.json, out
wav, segf, out = sys.argv[1:4]
src = open(__file__.replace('align_seg.py', 'align2.py')).read()
extra = eval(re.search(r"extra = (\{.*?\})\n", src, re.S).group(1))
segs_in = json.load(open(segf))
w = wave.open(wav, 'rb'); sr = w.getframerate(); data = w.readframes(w.getnframes()); bps = 2
res = []; tot = 0; miss = 0
for S in segs_in:
    words = re.findall(r"[a-zA-Z']+", S['text'].lower())
    d = Decoder(samprate=16000, bestpath=False)
    for k, p in extra.items():
        if d.lookup_word(k) is None: d.add_word(k, p, True)
    seg = None
    for pad in (0.15, 0.4, 0.05, 0.7):
        a = max(0.0, S['t0'] - pad); b = S['t1'] + pad
        chunk = data[int(a * sr) * bps:int(b * sr) * bps]
        d.set_align_text(" ".join(words))
        d.start_utt(); d.process_raw(chunk, full_utt=True); d.end_utt()
        seg = d.seg()
        if seg is not None: break
    if seg is None:
        # proportional fallback by character length
        print('FALLBACK segment', S['text'][:40])
        sents = [x for x in re.split(r'(?<=[.?!])\s+', S['text']) if re.findall(r"[a-zA-Z']+", x)]
        L = sum(len(x) for x in sents); t = S['t0']; span = S['t1'] - S['t0']
        for sn in sents:
            sw = re.findall(r"[a-zA-Z']+", sn.lower()); dt = span * len(sn) / L
            ok = None
            for pad in (0.5, 0.8, 1.2):
                a = max(0.0, t - pad); b = t + dt + pad
                d2 = Decoder(samprate=16000, bestpath=False)
                for k, p_ in extra.items():
                    if d2.lookup_word(k) is None: d2.add_word(k, p_, True)
                d2.set_align_text(" ".join(sw)); d2.start_utt(); d2.process_raw(data[int(a * sr) * bps:int(b * sr) * bps], full_utt=True); d2.end_utt()
                ok = d2.seg()
                if ok is not None:
                    res += [(g.word, a + g.start_frame / 100.0, a + (g.end_frame + 1) / 100.0) for g in ok]; break
            if ok is None:
                print('  prop', sn[:30]); tt = t
                for x in sw:
                    d_ = dt * (len(x) + 1) / sum(len(y) + 1 for y in sw); res.append((x, tt, tt + d_ * 0.9)); tt += d_
            t += dt
        tot += len(words); continue
    got = [(s.word, a + s.start_frame / 100.0, a + (s.end_frame + 1) / 100.0) for s in seg]
    n = len([g for g in got if g[0] not in ('<s>', '</s>', '<sil>')])
    tot += n; res += got
json.dump(res, open(out, 'w'))
print(tot, 'aligned', miss, 'missed')
