#!/usr/bin/env python3
"""Audit a rendered video (or a music file) against the video-director gates.

Usage:
  python3 audit_video.py VIDEO_OR_AUDIO [--out DIR] [--kind product|motion] [--target SECONDS]
                        [--reference QUALITY_BAR.mp4]

--kind product (default) applies the product-video gates (empty-stage share, first product frame).
--kind motion skips them (typographic motion pieces are mostly "sparse" by design).
--target is the brief's length in seconds; the length gate is skipped without it.
--reference measures the quality-bar video too and adds a side-by-side table (rules/quality-bar.md).

Needs ffmpeg + ffprobe on PATH and Python 3 with numpy and Pillow.
Writes DIR/audit.md, DIR/audit.json, DIR/timeline.png, DIR/contact_NN.png, DIR/phone.png.
Exit code: 0 = no fail-level gate failed, 1 = at least one failed, 2 = the file could not be read.
Gate thresholds live in ../gates.json (single source of truth).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
GATES = json.loads((HERE.parent / "gates.json").read_text())

# Frame analysis constants (calibrated on a light-stage product cut, 2026-09-26:
# text cards cover <= 0.14 of the 16x9 tile grid, product shots >= 0.43).
TILE_RANGE = 10       # a 12x12 px tile (on a 192x108 frame) is "busy" if its luma range exceeds this
SPARSE_BELOW = 0.25   # a frame is "sparse" (text/logo on an empty stage, or blank) below this coverage
STILL_BELOW = 0.3     # mean abs luma diff between frames at 10 fps below this = nothing moved
CHANGE_ABOVE = 5.0    # mean abs luma diff over 0.5 s above this (local peak) = a scene change, soft cuts included
FPS = 10


def jsonable(o):
    """json.dumps default: numpy scalars to plain Python numbers."""
    return o.item() if hasattr(o, "item") else str(o)


def sh(cmd, binary=False):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {r.stderr.decode(errors='replace')[-400:]}")
    return r.stdout if binary else r.stdout.decode(errors="replace") + r.stderr.decode(errors="replace")


def font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def probe(path):
    info = json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json",
                          "-show_format", "-show_streams", str(path)]))
    fmt = info.get("format", {})
    v = next((s for s in info["streams"] if s["codec_type"] == "video"
              and s.get("disposition", {}).get("attached_pic", 0) == 0), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    out = {"duration_s": float(fmt.get("duration", 0) or 0), "size_mb": int(fmt.get("size", 0)) / 1e6}
    if v:
        num, den = (v.get("r_frame_rate") or "0/1").split("/")
        vbr = v.get("bit_rate")
        if not vbr:  # some containers only report the total; subtract the audio stream
            vbr = int(fmt.get("bit_rate", 0)) - int((a or {}).get("bit_rate", 0) or 0)
        out.update(width=v["width"], height=v["height"], fps=round(int(num) / max(int(den), 1), 3),
                   video_codec=f"{v['codec_name']} {v.get('profile', '')}".strip(),
                   video_mbps=round(int(vbr) / 1e6, 3))
    if a:
        out.update(audio_codec=a["codec_name"], sample_rate=int(a.get("sample_rate", 0)),
                   channels=a.get("channels"), audio_kbps=round(int(a.get("bit_rate", 0) or 0) / 1e3))
    return out, v is not None, a is not None


def loudness(path):
    txt = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vn",
              "-af", "ebur128=peak=true:framelog=info", "-f", "null", "-"])
    s = txt[txt.rfind("Summary:"):]
    g = lambda pat: float(re.search(pat, s).group(1)) if re.search(pat, s) else None
    out = {"integrated_lufs": g(r"I:\s+(-?[\d.]+) LUFS"), "lra_lu": g(r"LRA:\s+(-?[\d.]+) LU"),
           "true_peak_dbtp": g(r"Peak:\s+(-?[\d.]+) dBFS")}
    # momentary loudness (400 ms windows): how far the loudest moment (a boom, a hit) rises above the film
    moments = [(float(t), float(m)) for t, m in re.findall(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)", txt)]
    if moments and out["integrated_lufs"] is not None:
        t, m = max(moments, key=lambda x: x[1])
        out.update(loudest_moment_lu=round(m - out["integrated_lufs"], 1), loudest_moment_at_s=t)
    return out


def audio_stats(path):
    raw = sh(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "2", "-ar", "48000",
              "-f", "f32le", "-"], binary=True)
    x = np.frombuffer(raw, np.float32).reshape(-1, 2)
    sr, m, side = 48000, x.mean(axis=1), (x[:, 0] - x[:, 1]) / 2
    db = lambda v: float(10 * np.log10(v + 1e-20))
    n = 8192
    fr = m[: len(m) // n * n].reshape(-1, n) * np.hanning(n)
    P = (np.abs(np.fft.rfft(fr, axis=1)) ** 2).mean(0)
    f = np.fft.rfftfreq(n, 1 / sr)
    tot = P.sum()
    bands = {f"{lo}-{hi}": round(db(P[(f >= lo) & (f < hi)].sum() / tot), 1)
             for lo, hi in [(0, 150), (150, 500), (500, 2000), (2000, 8000), (8000, 16000)]}
    per5 = []
    for s0 in range(0, int(len(m) / sr), 5):
        seg, seg2 = m[s0 * sr:(s0 + 5) * sr], x[s0 * sr:(s0 + 5) * sr]
        if len(seg) < sr:
            break
        rms, pk = np.sqrt((seg ** 2).mean()) + 1e-12, np.abs(seg).max() + 1e-12
        k = 4096
        fk = seg[: len(seg) // k * k].reshape(-1, k) * np.hanning(k)
        S = np.abs(np.fft.rfft(fk, axis=1)) + 1e-12
        fq = np.fft.rfftfreq(k, 1 / sr)
        Pk = S ** 2
        per5.append({"t": s0, "rms_db": round(20 * np.log10(rms), 1), "peak_db": round(20 * np.log10(pk), 1),
                     "crest": round(float(pk / rms), 1), "clipped": int((np.abs(seg2) >= 0.999).sum()),
                     "centroid_hz": int(np.median((Pk * fq).sum(1) / Pk.sum(1))),
                     "flatness": round(float(np.median(np.exp(np.log(S).mean(1)) / S.mean(1))), 3),
                     "air_db": round(db(Pk[:, (fq >= 8000) & (fq < 16000)].sum() / Pk.sum()), 1)})
    return {"sample_peak_dbfs": round(20 * np.log10(np.abs(x).max() + 1e-12), 2),
            "clipped_samples": int((np.abs(x) >= 0.999).sum()),
            "stereo_width": round(float(np.sqrt((side ** 2).mean()) / (np.sqrt((m ** 2).mean()) + 1e-12)), 3),
            "bands_db": bands, "air_db": bands["8000-16000"], "per_5s": per5}


def frames(path):
    raw = sh(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={FPS},scale=192:108",
              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], binary=True)
    return np.frombuffer(raw, np.uint8).reshape(-1, 108, 192, 3)


def runs_of(mask):
    out, start = [], 0
    for i in range(1, len(mask) + 1):
        if i == len(mask) or mask[i] != mask[start]:
            out.append((bool(mask[start]), start / FPS, i / FPS))
            start = i
    return out


def visual_stats(fr):
    Y = fr.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
    n = len(Y)
    tiles = Y.reshape(n, 9, 12, 16, 12).transpose(0, 1, 3, 2, 4).reshape(n, 9, 16, 144)
    cov = ((tiles.max(-1) - tiles.min(-1)) > TILE_RANGE).mean(axis=(1, 2))
    sparse = cov < SPARSE_BELOW
    diff = np.r_[0.0, np.abs(np.diff(Y, axis=0)).mean(axis=(1, 2))]
    still = diff < STILL_BELOW
    sr = [r for r in runs_of(sparse) if r[2] - r[1] >= 0.3]
    rich = [b - a for s, a, b in sr if not s]
    switches = sum(1 for i in range(1, len(sr)) if sr[i][0] != sr[i - 1][0])
    stills = [(b - a, a) for s, a, b in runs_of(still) if s]
    longest_still = max(stills, default=(0.0, 0.0))
    first_rich = next((i / FPS for i, s in enumerate(sparse) if not s), None)
    lag = FPS // 2
    dl = np.zeros(n)
    dl[lag:] = np.abs(Y[lag:] - Y[:-lag]).mean(axis=(1, 2))
    changes = sum(1 for i in range(n) if dl[i] > CHANGE_ABOVE and dl[i] == dl[max(0, i - 8):i + 9].max())
    dur = n / FPS
    return {"sparse_share": round(float(sparse.mean()), 3), "first_rich_s": first_rich,
            "sparse_rich_switches": switches, "longest_rich_s": round(max(rich, default=0.0), 1),
            "longest_still_s": round(longest_still[0], 1), "longest_still_at_s": round(longest_still[1], 1),
            "scene_changes": changes, "avg_scene_s": round(dur / (changes + 1), 1)}, cov, sparse


def gate_results(meas, kind, target):
    res = []

    def check(name, value, label=None):
        g = GATES[name]
        if value is None:
            return
        ok = (g.get("min") is None or value >= g["min"]) and (g.get("max") is None or value <= g["max"])
        res.append({"gate": label or name, "value": value, "min": g.get("min"), "max": g.get("max"),
                    "status": "PASS" if ok else g["level"].upper(), "why": g["why"]})

    if "integrated_lufs" in meas:
        check("integrated_lufs", meas["integrated_lufs"])
        check("true_peak_dbtp", meas["true_peak_dbtp"])
        check("clipped_samples", meas["clipped_samples"])
        check("loudest_moment_lu", meas.get("loudest_moment_lu"))
        check("stereo_width", meas["stereo_width"])
        check("air_db", meas["air_db"])
    if "height" in meas:
        check("video_mbps_2160p" if meas["height"] >= 2000 else "video_mbps_1080p", meas["video_mbps"])
        if kind == "product":
            check("sparse_share", meas["sparse_share"])
            check("first_rich_s", meas["first_rich_s"])
        check("longest_still_s", meas["longest_still_s"])
    if target:
        check("length_off", round(abs(meas["duration_s"] - target) / target, 3), "length_off (share of target)")
    return res


def sheets(path, out, dur, cov, width, height):
    f18, f14 = font(18), font(14)
    # contact sheets: 1 frame/s, 6x5 per sheet
    raw = sh(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "fps=1,scale=320:180",
              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], binary=True)
    th = np.frombuffer(raw, np.uint8).reshape(-1, 180, 320, 3)
    paths = []
    for s in range(0, len(th), 30):
        sheet = Image.new("RGB", (6 * 320, 5 * 180), "black")
        for i, t in enumerate(th[s:s + 30]):
            im = Image.fromarray(t)
            d = ImageDraw.Draw(im)
            d.rectangle([2, 2, 62, 24], fill="white")
            d.text((6, 4), f"{s + i + 0.5:.0f}s", fill=(200, 0, 0), font=f18)
            sheet.paste(im, ((i % 6) * 320, (i // 6) * 180))
        p = out / f"contact_{s // 30 + 1:02d}.png"
        sheet.save(p)
        paths.append(p.name)
    # phone sheet: what a viewer sees inline on a phone (390 pt wide), one frame every 5 s
    h = int(round(390 * height / width / 2) * 2)
    raw = sh(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps=1/5,scale=390:{h}",
              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], binary=True)
    ph = np.frombuffer(raw, np.uint8).reshape(-1, h, 390, 3)
    rows = (len(ph) + 2) // 3
    sheet = Image.new("RGB", (3 * 400, rows * (h + 26)), "white")
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(ph):
        x, y = (i % 3) * 400, (i // 3) * (h + 26)
        sheet.paste(Image.fromarray(t), (x, y + 22))
        d.text((x + 2, y + 2), f"{i * 5 + 2.5:.1f}s  (phone size)", fill=(60, 60, 60), font=f14)
    sheet.save(out / "phone.png")
    # timeline strip: green = product/rich frames, grey = text/logo on an empty stage or blank
    W, X0, X1 = 1600, 30, 1570
    im = Image.new("RGB", (W, 120), "white")
    d = ImageDraw.Draw(im)
    for i, c in enumerate(cov):
        x0 = X0 + (X1 - X0) * i / len(cov)
        x1 = X0 + (X1 - X0) * (i + 1) / len(cov)
        d.rectangle([x0, 20, x1, 70], fill=(148, 153, 163) if c < SPARSE_BELOW else (22, 163, 74))
    for t in range(0, int(dur) + 1, 10):
        x = X0 + (X1 - X0) * t / dur
        d.line([x, 70, x, 76], fill=(80, 80, 80))
        d.text((x - 8, 80), f"{t}s", fill=(80, 80, 80), font=f14)
    d.text((X0, 0), "green = rich frames (product / footage)   grey = text or logo on an empty stage, or blank",
           fill=(40, 40, 40), font=f14)
    im.save(out / "timeline.png")
    return paths


def write_md(out, path, meas, gates, audio, vis_paths, compare=()):
    L = [f"# Audit — {path.name}", ""]
    fails = [g for g in gates if g["status"] == "FAIL"]
    warns = [g for g in gates if g["status"] == "WARN"]
    L += [f"**Gates:** {len(gates) - len(fails) - len(warns)} pass · {len(warns)} warn · {len(fails)} fail", ""]
    L += ["| Gate | Value | Target | Status | Why |", "|---|---|---|---|---|"]
    for g in gates:
        tgt = " ".join(x for x in [f"≥ {g['min']}" if g["min"] is not None else "",
                                    f"≤ {g['max']}" if g["max"] is not None else ""] if x)
        L.append(f"| {g['gate']} | {g['value']} | {tgt} | {g['status']} | {g['why']} |")
    L += ["", "## Measurements", "", "```json", json.dumps({k: v for k, v in meas.items()
                                                           if k not in ("per_5s", "bands_db")}, indent=1, default=jsonable), "```"]
    if audio:
        L += ["", "## Audio across the whole length (per 5 s)", "",
              f"Bands (share of total energy, dB): {audio['bands_db']}", "",
              "| t (s) | RMS dB | peak dB | crest | clipped | centroid Hz | flatness | air dB |",
              "|---|---|---|---|---|---|---|---|"]
        L += [f"| {r['t']} | {r['rms_db']} | {r['peak_db']} | {r['crest']} | {r['clipped']} | "
              f"{r['centroid_hz']} | {r['flatness']} | {r['air_db']} |" for r in audio["per_5s"]]
    if vis_paths:
        L += ["", "## Look at these", "", "- `timeline.png` — where the seconds go",
              "- `phone.png` — can the key words and numbers be read at phone size?"]
        L += [f"- `{p}` — 1 frame per second" for p in vis_paths]
    L += list(compare)
    L += ["", "## Manual checks (the audit cannot see these)", ""]
    L += [f"- [ ] {c}" for c in GATES["_manual_checks"]]
    (out / "audit.md").write_text("\n".join(L) + "\n")


COMPARE = ["duration_s", "video_mbps", "integrated_lufs", "true_peak_dbtp", "loudest_moment_lu", "stereo_width", "air_db",
           "sparse_share", "first_rich_s", "scene_changes", "avg_scene_s", "longest_rich_s", "longest_still_s"]


def measure(path, out):
    """Probe, loudness, audio and frame stats for one file; writes its sheets into out."""
    meas, has_v, has_a = probe(path)
    audio, vis_paths = None, []
    if has_a:
        meas.update(loudness(path))
        audio = audio_stats(path)
        meas.update({k: v for k, v in audio.items() if k != "per_5s"})
    if has_v:
        vstats, cov, _ = visual_stats(frames(path))
        meas.update(vstats)
        vis_paths = sheets(path, out, meas["duration_s"], cov, meas["width"], meas["height"])
    return meas, has_v, has_a, audio, vis_paths


def compare_md(meas, ref, ref_path):
    L = ["", f"## Compared with the quality-bar reference ({ref_path.name})", "",
         "Contact sheets for the reference are in `reference/`; compare them scene by scene.", "",
         "| Metric | This video | Reference |", "|---|---|---|"]
    L += [f"| {k} | {meas.get(k, '—')} | {ref.get(k, '—')} |" for k in COMPARE]
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out", default=None)
    ap.add_argument("--kind", choices=["product", "motion"], default="product")
    ap.add_argument("--target", type=float, default=None, help="brief length in seconds")
    ap.add_argument("--reference", default=None, help="quality-bar video to measure side by side")
    a = ap.parse_args()
    path = Path(a.file).expanduser().resolve()
    out = Path(a.out or f"{path.stem}-audit").expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    try:
        meas, has_v, has_a, audio, vis_paths = measure(path, out)
    except Exception as e:  # unreadable input
        print(f"cannot read {path}: {e}", file=sys.stderr)
        return 2
    ref = None
    if a.reference:
        ref_path = Path(a.reference).expanduser().resolve()
        (out / "reference").mkdir(exist_ok=True)
        ref = measure(ref_path, out / "reference")[0]
    gates = gate_results(meas, a.kind, a.target)
    if has_v and not has_a:
        gates.append({"gate": "audio track", "value": "none", "min": None, "max": None, "status": "WARN",
                      "why": "A published video needs a mixed soundtrack (music bed + UI sounds)."})
    (out / "audit.json").write_text(json.dumps({"file": str(path), "measurements": meas, "reference": ref,
                                                "gates": gates, "audio_per_5s": (audio or {}).get("per_5s")},
                                               indent=1, default=jsonable))
    write_md(out, path, meas, gates, audio, vis_paths, compare_md(meas, ref, ref_path) if ref else [])
    for g in gates:
        print(f"{g['status']:4}  {g['gate']}: {g['value']}")
    if ref:
        for k in COMPARE:
            print(f"      {k}: {meas.get(k, '-')}  (reference {ref.get(k, '-')})")
    print(f"report: {out / 'audit.md'}")
    return 1 if any(g["status"] == "FAIL" for g in gates) else 0


if __name__ == "__main__":
    sys.exit(main())
