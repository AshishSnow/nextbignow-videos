"""Original Chatterbox (supports exaggeration/cfg) chunk generator. usage: cb_orig_chunks.py <chunks.json> <outdir> <ref.wav> [seed]
env CB_EX (exaggeration, default 0.7), CB_CFG (cfg_weight, default 0.3), CB_T (temperature, default 0.8)."""
import sys, json, os, time, torch, torchaudio as ta
torch.set_num_threads(4)
chunks = json.load(open(sys.argv[1])); od = sys.argv[2]; ref = sys.argv[3]; seed = int(sys.argv[4]) if len(sys.argv) > 4 else 11
EX = float(os.environ.get('CB_EX', '0.7')); CFG = float(os.environ.get('CB_CFG', '0.3')); TT = float(os.environ.get('CB_T', '0.8'))
from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device='cpu')
m.prepare_conditionals(ref, exaggeration=EX)
os.makedirs(od, exist_ok=True)
for i, txt in enumerate(chunks):
    t0 = time.time()
    torch.manual_seed(seed + i)
    wav = m.generate(txt, exaggeration=EX, cfg_weight=CFG, temperature=TT)
    ta.save(os.path.join(od, 'c_%03d.wav' % i), wav, m.sr)
    print('chunk %d %.1fs %s' % (i, time.time() - t0, txt[:40]), flush=True)
