#!/bin/bash
# One-time setup of the OopsMyBusiness video studio in a fresh workspace (idempotent).
# Usage: bash studio/setup.sh            -> installs into $STUDIO (default /home/claude/studio)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
STUDIO=${STUDIO:-/home/claude/studio}
mkdir -p "$STUDIO"/{models/kokoro,assets/sf/gugs,fonts,lib,projects}
cp -f "$HERE"/lib/*.py "$STUDIO/lib/"
mkdir -p "$STUDIO/lib/speechmos_pkg" "$STUDIO/models/utmos" && cp -rf "$HERE"/lib/speechmos_pkg/* "$STUDIO/lib/speechmos_pkg/"

dl() { [ -s "$2" ] || { echo "downloading $(basename "$2")"; curl -sSL --retry 3 -o "$2.part" "$1" && mv "$2.part" "$2"; }; }
dl https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx "$STUDIO/models/kokoro/kokoro-v1.0.onnx"
dl https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin "$STUDIO/models/kokoro/voices-v1.0.bin"
dl https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2 "$STUDIO/assets/sf/gugs/GeneralUser-GS.sf2"
# naturalness scorer (UTMOS22 strong, MIT) for voice A/B tests — needs torch
dl https://github.com/tarepan/SpeechMOS/releases/download/v1.0.0/utmos22_strong_step7459_v1.pt "$STUDIO/models/utmos/utmos22_strong.pt"
P=sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
if [ ! -s "$STUDIO/models/$P/encoder.int8.onnx" ]; then
  dl https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/$P.tar.bz2 "$STUDIO/models/$P.tar.bz2"
  tar -xjf "$STUDIO/models/$P.tar.bz2" -C "$STUDIO/models" && rm -f "$STUDIO/models/$P.tar.bz2"
fi

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
for m in kokoro_onnx sherpa_onnx parselmouth pedalboard tinysoundfont num2words soundfile cv2 PIL scipy; do need $m || echo "MISSING python module: $m"; done
need torch || echo "NOTE: torch missing -> UTMOS naturalness score unavailable (voice_report.py still reports pitch/pace/ASR)"
[ -f /usr/share/fonts/opentype/inter/InterDisplay-Black.otf ] || echo "WARNING: Inter Display fonts missing (/usr/share/fonts/opentype/inter) — install fonts-inter"
which ffmpeg >/dev/null || echo "WARNING: ffmpeg missing"
echo "STUDIO READY at $STUDIO"
