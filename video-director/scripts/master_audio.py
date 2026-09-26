#!/usr/bin/env python3
"""Master a rendered video's soundtrack to the delivery loudness, leaving the picture untouched.

Usage:
  python3 master_audio.py IN.mp4 OUT.mp4 [--lufs -14] [--tp -1.5]

Two-pass ffmpeg loudnorm (measure, then apply linearly with the measured values). The video stream
is copied bit for bit; only the audio is re-encoded (AAC-LC 320 kbps, 48 kHz). The true-peak target
defaults to -1.5 dBTP, so the AAC encode still lands under the -1.0 dBTP gate. Re-run
audit_video.py on OUT to confirm.
"""
import argparse
import json
import re
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-1.5)
    a = ap.parse_args()
    target = f"I={a.lufs}:TP={a.tp}:LRA=11"
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.src, "-vn",
                         "-af", f"loudnorm={target}:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p1.stderr)
    if p1.returncode != 0 or not m:
        print("loudness measurement failed:\n" + p1.stderr[-600:], file=sys.stderr)
        return 1
    ms = json.loads(m.group(0))
    af = (f"loudnorm={target}:measured_I={ms['input_i']}:measured_TP={ms['input_tp']}"
          f":measured_LRA={ms['input_lra']}:measured_thresh={ms['input_thresh']}"
          f":offset={ms['target_offset']}:linear=true")
    p2 = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", a.src, "-map", "0:v?", "-map", "0:a:0",
                         "-c:v", "copy", "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "320k",
                         "-movflags", "+faststart", a.dst], capture_output=True, text=True)
    if p2.returncode != 0:
        print("mastering failed:\n" + p2.stderr[-600:], file=sys.stderr)
        return 1
    print(f"input {ms['input_i']} LUFS / {ms['input_tp']} dBTP -> target {a.lufs} LUFS / {a.tp} dBTP: {a.dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
