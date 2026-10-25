#!/bin/bash
# FreshNestHub reel engine — one-time setup per session (PyPI + GitHub downloads only).
# Installs the kit to /home/claude/reel-kit (all scripts use absolute paths there).
set -e
R=$(cd "$(dirname "$0")" && pwd)
K=/home/claude/reel-kit
mkdir -p $K/english/scripts $K/english/work $K/english/frames $K/assets $K/models/kokoro /home/claude/outputs
cp -r $R/kit/english/scripts/. $K/english/scripts/
cp -r $R/kit/assets/fonts_plate $K/assets/
if [ ! -f /usr/share/fonts/opentype/inter/Inter-Black.otf ]; then
  mkdir -p /usr/share/fonts/opentype/inter && cp $R/kit/assets/fonts_inter/*.otf /usr/share/fonts/opentype/inter/
fi
pip install --break-system-packages -q numpy scipy pillow soundfile opencv-python-headless num2words onnxruntime sherpa-onnx kokoro-onnx
pip install --break-system-packages -q --no-deps tinysoundfont
# soundfont for the score
[ -f $K/assets/sf/gugs/GeneralUser-GS.sf2 ] || git clone -q --depth 1 https://github.com/mrbumpy409/GeneralUser-GS.git $K/assets/sf/gugs
# parakeet ASR (English word alignment)
if [ ! -f $K/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8/encoder.int8.onnx ]; then
  curl -sSL -o /tmp/pk.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2
  tar xjf /tmp/pk.tar.bz2 -C $K/models && rm /tmp/pk.tar.bz2
fi
# Kokoro voice model (Nessa's voice is built from af_heart / af_bella / af_nicole / af_sarah blends)
[ -f $K/models/kokoro/kokoro-v1.0.onnx ] || curl -sSL -o $K/models/kokoro/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f $K/models/kokoro/voices-v1.0.bin ] || curl -sSL -o $K/models/kokoro/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
ffmpeg -hide_banner -filters 2>/dev/null | grep -q rubberband || echo "WARNING: ffmpeg has no rubberband filter (voice pitch moods will fail)"
python3 -c "import kokoro_onnx, sherpa_onnx, tinysoundfont, cv2, scipy; print('python deps ok')"
echo "fnh engine ready"
