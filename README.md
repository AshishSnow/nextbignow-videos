Model files for studio/setup.sh (not code).
utmos22.onnx = UTMOS22 strong (MIT licence, tarepan/SpeechMOS weights utmos22_strong_step7459_v1) exported to ONNX (fp32, dynamic length; feed 16 kHz audio trimmed to an even frame count).
Rebuild: cat utmos22.onnx.part* > utmos22.onnx && sha256sum -c utmos22.onnx.sha256
