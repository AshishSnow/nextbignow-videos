#!/bin/bash
# One-time setup of the OopsMyBusiness video studio in a fresh workspace (idempotent).
# Usage: bash studio/setup.sh            -> installs into $STUDIO (default /home/claude/studio)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
STUDIO=${STUDIO:-/home/claude/studio}
mkdir -p "$STUDIO"/{models/kokoro,assets/sf/gugs,fonts,lib,projects}
cp -f "$HERE"/lib/*.py "$STUDIO/lib/"
mkdir -p "$STUDIO/voices" && cp -f "$HERE"/voices/*.npz "$HERE"/voices/*.wav "$STUDIO/voices/" 2>/dev/null || true
mkdir -p "$STUDIO/models/utmos"

dl() { [ -s "$2" ] || { echo "downloading $(basename "$2")"; curl -sSL --retry 3 -o "$2.part" "$1" && mv "$2.part" "$2"; }; }
dl https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx "$STUDIO/models/kokoro/kokoro-v1.0.onnx"
dl https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin "$STUDIO/models/kokoro/voices-v1.0.bin"
dl https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2 "$STUDIO/assets/sf/gugs/GeneralUser-GS.sf2"
# naturalness scorer for voice A/B tests: UTMOS22 strong (MIT, tarepan/SpeechMOS) exported to ONNX -> runs on onnxruntime, no torch.
# Hosted in this repo's `models` branch in <100 MB parts.
U="$STUDIO/models/utmos/utmos22.onnx"
if [ ! -s "$U" ]; then
  RAW=https://raw.githubusercontent.com/AshishSnow/nextbignow-videos/models
  for i in 00 01 02 03 04; do dl "$RAW/utmos22.onnx.part$i" "$STUDIO/models/utmos/utmos22.onnx.part$i"; done
  cat "$STUDIO"/models/utmos/utmos22.onnx.part0? > "$U.tmp"
  if [ "$(sha256sum "$U.tmp" | cut -d' ' -f1)" = "e99bfcb15cd08aea5ee6fccfc274aeecf7d3dfd93690cd5cbfa9fdf74695f54d" ]; then
    mv "$U.tmp" "$U"; rm -f "$STUDIO"/models/utmos/utmos22.onnx.part0?
  else echo "WARNING: utmos22.onnx checksum mismatch -> voice_report.py will skip UTMOS"; rm -f "$U.tmp"; fi
fi
P=sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
if [ ! -s "$STUDIO/models/$P/encoder.int8.onnx" ]; then
  dl https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/$P.tar.bz2 "$STUDIO/models/$P.tar.bz2"
  tar -xjf "$STUDIO/models/$P.tar.bz2" -C "$STUDIO/models" && rm -f "$STUDIO/models/$P.tar.bz2"
fi

# Chatterbox-Turbo (MIT, ResembleAI/chatterbox-turbo-ONNX): fp32 token embeddings + decoder, q4 language model (~1.2 GB).
# Speaker conditioning ships precomputed in studio/voices/*.cbcond.npz, so the 1 GB speech encoder is not needed.
CB="$STUDIO/models/cbturbo"; mkdir -p "$CB"; HF=https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX/resolve/main
for f in embed_tokens language_model_q4 conditional_decoder; do dl "$HF/onnx/$f.onnx" "$CB/$f.onnx"; dl "$HF/onnx/$f.onnx_data" "$CB/$f.onnx_data"; done
dl "$HF/tokenizer.json" "$CB/tokenizer.json"

# fonts (npm registry)
font() { [ -d "$STUDIO/fonts/$1/package" ] || { mkdir -p "$STUDIO/fonts/$1"; (cd "$STUDIO/fonts/$1" && npm pack -s "$2" >/dev/null && tar -xzf *.tgz && rm -f *.tgz); }; }
font lilita @fontsource/lilita-one@5.2.5
font anton @fontsource/anton@5.3.0
font playfair @fontsource/playfair-display@5.1.0

# python packages (tinysoundfont without its pyaudio dependency — we only render offline)
need() { python3 -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('$1') else 1)"; }
pipi() { pip install -q --break-system-packages "$@" 2>&1 | grep -v -i "warning" || true; }
need kokoro_onnx || pipi kokoro-onnx==0.6.1
need sherpa_onnx || pipi sherpa-onnx==1.13.8
need parselmouth || pipi praat-parselmouth==0.4.7
need pedalboard || pipi pedalboard==0.9.26
need tinysoundfont || pipi --no-deps tinysoundfont==0.3.7
need num2words || pipi num2words
need soundfile || pipi soundfile
need cv2 || pipi opencv-python-headless
need PIL || pipi pillow
need scipy || pipi scipy
need tokenizers || pipi tokenizers
for m in tokenizers kokoro_onnx sherpa_onnx parselmouth pedalboard tinysoundfont num2words soundfile cv2 PIL scipy; do need $m || echo "MISSING python module: $m"; done
[ -s "$STUDIO/models/utmos/utmos22.onnx" ] || echo "NOTE: UTMOS model missing -> voice_report.py reports pitch/pace/ASR only"
[ -f /usr/share/fonts/opentype/inter/InterDisplay-Black.otf ] || echo "WARNING: Inter Display fonts missing (/usr/share/fonts/opentype/inter) — install fonts-inter"
which ffmpeg >/dev/null || echo "WARNING: ffmpeg missing"
echo "STUDIO READY at $STUDIO"
