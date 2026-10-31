"""OopsMyBusiness — 4 tricks restaurants use on you (fully animated). Usage: anim.py OUT.mp4 [frames|a:b]"""
import sys, subprocess, os
_D = os.path.dirname(os.path.abspath(__file__))
for _p in ("anim_base.py", "anim_cine.py", "anim_mascot3d.py", "anim_sets.py", "anim_props.py", "anim_props2.py", "anim_props3.py", "anim_story.py", "anim_story2.py", "anim_shots.py"):
    exec(open(f"{_D}/{_p}").read())

N = int(round(END * FPS))


def main():
    OUT = sys.argv[1]; ARG = sys.argv[2] if len(sys.argv) > 2 else None
    if ARG and ":" not in ARG:
        for n in [int(x) for x in ARG.split(",")]:
            cv2.imwrite(f"{B}/frames/r_{n:04d}.jpg", cv2.cvtColor(compose(n), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
        return
    a, b2 = (int(x) for x in ARG.split(":")) if ARG else (0, N)
    b2 = min(b2, N)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "14", "-maxrate", "16M", "-bufsize", "32M", "-tune", "animation", "-profile:v", "high",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                            "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for n in range(a, b2):
        enc.stdin.write(compose(n).tobytes())
        if (n - a) % 120 == 0: print(f"frame {n}/{b2}", flush=True)
    enc.stdin.close(); enc.wait(); print("done", OUT, a, b2)


if __name__ == "__main__":
    main()
