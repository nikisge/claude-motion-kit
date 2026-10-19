# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "pillow"]
# ///
"""Render a sound designer's cue list into a mastered mix. The script decides nothing creative:
which sound, where, how loud and whether at all is in cues.json (written by the designer).

    uv run scripts/sound_place.py cues.json --video film.mp4 --out mix.wav [--mux film_sound.mp4] [--png mix.png]

cues.json (all times: seconds 1.25 | frames "f30" (uses fps) | "0:01.25"; paths relative to cues.json,
motion-studio/ or motion-studio/sound/):
{
  "fps": 30, "duration": 10.0,                     # duration optional: video length or last cue end
  "master": {"lufs": -14, "true_peak": -2.0},      # defaults (−2 im WAV, damit nach AAC ≤ −1,5 bleibt)
  "voice": {"file": "@video", "gain_db": 0},       # optional; "@video" = the video's own audio; ducks music
  "music": [{"file": "sound/music/beat-work.mp3", "t": 0, "src_in": 12.0, "src_out": 22.5,
             "gain_db": -10, "fade_in": 0.4, "fade_out": 1.5, "duck_db": -12}],
  "cues": [{"t": "f45", "file": "sound/sfx/...ogg", "align": "peak", "gain_db": -9, "pan": -0.3,
            "rate": 1.02, "trim": [0, 0.6], "fade_out": 0.05, "hpf": 300, "lpf": 9000, "reverb": 0.15,
            "duck_music_db": -4, "vary": true, "note": "Logo landet"}]
}
align: onset (default, first audible sample on t) | start | peak (loudest moment on t) | end (file ends on t).
vary: deterministic +-2 dB / rate 0.96-1.04 so repeats never sound identical.
pan -1..1 (constant power); pan_path [[film_t, p], ...] moves it over time (sound follows an object across the
frame). gain_path [[film_t, dB], ...] automates volume on top of gain_db (cues and music, linear in dB).
reverb = wet share 0..1 (small synthetic room). duck_music_db dips the music around this cue
(onset-0.05 s .. peak+0.3 s). music entries also take hpf/lpf (Hz), e.g. muffled music that "opens" on a reveal.

Master: gain to target LUFS, true-peak limiter (4x oversampled, 1 ms lookahead blocks), iterate until
LUFS within 0.5 LU and TP <= target; verified independently with ffmpeg ebur128. Writes <out>.report.json
(placements, levels, warnings) and a waveform PNG with cue markers (and film frames when --video).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import soundlib as sl  # noqa: E402

SOUND = Path(os.environ.get("MOTION_SOUND_ROOT", Path.cwd() / "sound")).resolve()
MS = SOUND.parent  # Pfade wie "sound/sfx/..." relativ zum Arbeitsordner
SR = sl.SR


# ---------- parsing ----------
def tsec(v, fps: float) -> float:
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s.startswith("f"):
        return float(s[1:]) / fps
    if ":" in s:
        m, sec = s.split(":", 1)
        return int(m) * 60 + float(sec)
    return float(s)


def resolve(path: str, base: Path) -> Path:
    for root in (base, MS, SOUND):
        p = (root / path).resolve()
        if p.exists():
            return p
    raise SystemExit(f"Datei nicht gefunden: {path}")


def probe_duration(path: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


# ---------- dsp ----------
def db(g: float) -> float:
    return 10 ** (g / 20)


def change_rate(x: np.ndarray, rate: float) -> np.ndarray:
    if abs(rate - 1) < 1e-4:
        return x
    n = int(len(x) / rate)
    src = np.arange(n) * rate
    idx = np.arange(len(x))
    return np.stack([np.interp(src, idx, x[:, c]) for c in range(2)], axis=1).astype(np.float32)


def filt(x: np.ndarray, hpf: float | None, lpf: float | None) -> np.ndarray:
    from scipy.signal import butter, sosfilt
    if hpf:
        x = sosfilt(butter(2, hpf, "highpass", fs=SR, output="sos"), x, axis=0)
    if lpf:
        x = sosfilt(butter(2, lpf, "lowpass", fs=SR, output="sos"), x, axis=0)
    return x.astype(np.float32)


_IR = None


def reverb(x: np.ndarray, wet: float) -> np.ndarray:
    """Small room: 0.7 s decorrelated exponential noise tail, deterministic."""
    global _IR
    from scipy.signal import fftconvolve
    if wet <= 0:
        return x
    if _IR is None:
        rng = np.random.default_rng(7)
        n = int(0.7 * SR)
        env = np.exp(-np.arange(n) / (0.18 * SR))
        ir = rng.standard_normal((n, 2)) * env[:, None]
        ir[: int(0.012 * SR)] = 0  # pre-delay 12 ms
        _IR = (ir / np.sqrt((ir ** 2).sum(axis=0))).astype(np.float32)
    tail = np.zeros((len(x) + len(_IR) - 1, 2), np.float32)
    for c in range(2):
        tail[:, c] = fftconvolve(x[:, c], _IR[:, c])
    dry = np.zeros_like(tail)
    dry[: len(x)] = x
    return (dry * (1 - wet) + tail * wet).astype(np.float32)


def pan(x: np.ndarray, p: float, path: list | None = None, start: float = 0.0) -> np.ndarray:
    """Constant-power pan. path = [[film_t, p], ...] moves the pan over time (linear, held at the ends)."""
    if path:
        pts = sorted((float(t), float(v)) for t, v in path)
        ts = start + np.arange(len(x)) / SR
        ps = np.clip(np.interp(ts, [q[0] for q in pts], [q[1] for q in pts]), -1, 1)
        a = (ps + 1) * np.pi / 4
        return (x * np.stack([np.cos(a), np.sin(a)], axis=1) * np.sqrt(2)).astype(np.float32)
    if not p:
        return x
    a = (np.clip(p, -1, 1) + 1) * np.pi / 4
    return (x * np.array([np.cos(a), np.sin(a)]) * np.sqrt(2)).astype(np.float32)


def gain_path(x: np.ndarray, path: list | None, start: float) -> np.ndarray:
    """Volume automation: path = [[film_t, dB], ...] (linear in dB, held at the ends), on top of gain_db."""
    if not path:
        return x
    pts = sorted((float(t), float(v)) for t, v in path)
    ts = start + np.arange(len(x)) / SR
    g = 10 ** (np.interp(ts, [q[0] for q in pts], [q[1] for q in pts]) / 20)
    return (x * g[:, None]).astype(np.float32)


def fades(x: np.ndarray, fi: float, fo: float) -> np.ndarray:
    n = len(x)
    if fi and fi > 0:
        k = min(n, int(fi * SR))
        x[:k] *= np.sin(np.linspace(0, np.pi / 2, k))[:, None] ** 2
    if fo and fo > 0:
        k = min(n, int(fo * SR))
        x[n - k:] *= np.cos(np.linspace(0, np.pi / 2, k))[:, None] ** 2
    return x


def add(bus: np.ndarray, x: np.ndarray, start: float) -> tuple[int, int]:
    i = int(round(start * SR))
    j0 = max(0, -i)
    i = max(0, i)
    k = min(len(bus) - i, len(x) - j0)
    if k > 0:
        bus[i:i + k] += x[j0:j0 + k]
    return i, k


def smooth_gain(target_db: np.ndarray, block_s: float, attack: float, release: float, hold: float) -> np.ndarray:
    """target_db per control block (<=0). Attack toward lower gain, hold, release toward higher."""
    out = np.zeros_like(target_db)
    a_att = 1 - np.exp(-block_s / max(attack, 1e-3))
    a_rel = 1 - np.exp(-block_s / max(release, 1e-3))
    hold_n = int(hold / block_s)
    g, held = 0.0, 0
    for i, t in enumerate(target_db):
        if t < g:
            g += (t - g) * a_att
            held = hold_n
        elif held > 0:
            held -= 1
        else:
            g += (t - g) * a_rel
        out[i] = g
    return out


def limiter(x: np.ndarray, ceiling_db: float) -> np.ndarray:
    """True-peak-aware lookahead limiter on 1 ms control blocks."""
    from scipy.ndimage import minimum_filter1d
    from scipy.signal import resample_poly
    ceil = db(ceiling_db)
    up = np.abs(resample_poly(x.astype(np.float64), 4, 1, axis=0)).max(axis=1)
    blk = SR // 1000
    nb = int(np.ceil(len(x) / blk))
    pk = np.zeros(nb)
    upb = blk * 4
    for b in range(nb):  # block peak of the oversampled signal
        seg = up[b * upb:(b + 1) * upb]
        pk[b] = seg.max() if seg.size else 0
    req = np.minimum(1.0, ceil / np.maximum(pk, 1e-9))
    req = minimum_filter1d(req, size=5)  # +-2 ms lookahead, keeps interpolation below every block's need
    g = np.empty(nb)
    cur = 1.0
    a_rel = 1 - np.exp(-1 / 60.0)  # ~60 ms release
    for b in range(nb):
        cur = req[b] if req[b] < cur else cur + (req[b] - cur) * a_rel
        g[b] = cur
    centers = (np.arange(nb) + 0.5) * blk
    gs = np.interp(np.arange(len(x)), centers, g)
    return (x * gs[:, None]).astype(np.float32)


def ffmpeg_r128(path: str) -> dict:
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", path, "-filter_complex", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary:"):]
    def g(rx):
        m = re.search(rx, s)
        return float(m.group(1)) if m else None
    return {"lufs": g(r"I:\s+(-?[\d.]+) LUFS"), "lra": g(r"LRA:\s+(-?[\d.]+) LU"), "true_peak": g(r"Peak:\s+(-?[\d.]+) dBFS")}


# ---------- main ----------
def load_index() -> dict:
    p = SOUND / "index.json"
    if not p.exists():
        return {}
    return {(SOUND / e["path"]).resolve().as_posix(): e for e in json.loads(p.read_text())["files"]}


def render(spec: dict, base: Path, video: str | None) -> tuple[np.ndarray, dict]:
    fps = float(spec.get("fps", 30))
    master = {"lufs": -14.0, "true_peak": -2.0, **spec.get("master", {})}
    index = load_index()
    warn: list[str] = []
    dur = spec.get("duration")
    if dur is None and video:
        dur = probe_duration(video)
    cues = spec.get("cues", [])
    musics = spec.get("music", [])
    voice = spec.get("voice")
    if dur is None:
        dur = max([tsec(c["t"], fps) + 3 for c in cues] + [5.0])
    dur = float(dur)
    n = int(dur * SR)
    sfx_bus = np.zeros((n, 2), np.float32)
    mus_bus = np.zeros((n, 2), np.float32)
    voc_bus = np.zeros((n, 2), np.float32)
    block = 0.01
    nblk = int(np.ceil(dur / block)) + 1
    cue_duck = np.zeros(nblk)
    placed = []

    def lic_check(p: Path):
        e = index.get(p.resolve().as_posix())
        if e is None:
            warn.append(f"nicht im Index (Lizenz ungeprüft): {p}")
            return None
        if e.get("license") in (None, "UNBEKANNT"):
            warn.append(f"Lizenz UNBEKANNT: {p}")
        return e.get("license")

    # voice
    if voice:
        vpath = video if voice.get("file") == "@video" else str(resolve(voice["file"], base))
        if vpath is None:
            raise SystemExit("voice @video braucht --video")
        v = sl.decode(vpath) * db(voice.get("gain_db", 0))
        add(voc_bus, v, tsec(voice.get("t", 0), fps))

    # sfx
    last_file = None
    for k, c in enumerate(sorted(cues, key=lambda c: tsec(c["t"], fps))):
        p = resolve(c["file"], base)
        lic = lic_check(p)
        x = sl.decode(str(p))
        if c.get("trim"):
            a, b = c["trim"]
            x = x[int(a * SR): int(b * SR) if b else None]
        gain, rate = c.get("gain_db", -10.0), c.get("rate", 1.0)
        if c.get("vary"):
            rng = np.random.default_rng(1000 + k)
            gain += float(rng.uniform(-2, 2))
            rate *= float(rng.uniform(0.96, 1.04))
        x = change_rate(x, rate)
        x = filt(x, c.get("hpf"), c.get("lpf"))
        x = fades(x.copy(), c.get("fade_in", 0), c.get("fade_out", 0.01))
        shp = sl.shape(x)
        x = reverb(x, c.get("reverb", 0)) * db(gain)
        t = tsec(c["t"], fps)
        align = c.get("align", "onset")
        off = {"start": 0, "onset": shp["onset_ms"] / 1000, "peak": shp["peak_ms"] / 1000,
               "end": len(x) / SR}[align]
        start = t - off
        x = pan(x, c.get("pan", 0), c.get("pan_path"), start)
        x = gain_path(x, c.get("gain_path"), start)
        add(sfx_bus, x, start)
        if start + shp["onset_ms"] / 1000 < -0.01 or start + len(x) / SR > dur + 0.5:
            warn.append(f"Cue {k} ({p.name}) ragt aus dem Film ({start:.2f} s)")
        if last_file == p.name and not c.get("vary"):
            warn.append(f"Cue {k}: gleiche Datei zweimal hintereinander ({p.name}); andere Variante oder vary")
        last_file = p.name
        peak_t = start + shp["peak_ms"] / 1000
        if c.get("duck_music_db"):
            a0, a1 = int((start + shp["onset_ms"] / 1000 - 0.05) / block), int((peak_t + 0.3) / block)
            cue_duck[max(0, a0):max(0, a1)] = np.minimum(cue_duck[max(0, a0):max(0, a1)], c["duck_music_db"])
        placed.append({"i": k, "file": c["file"], "note": c.get("note", ""), "t": round(t, 3), "align": align,
                       "start": round(start, 3), "peak": round(peak_t, 3), "frame": int(round(t * fps)),
                       "gain_db": round(gain, 2), "rate": round(rate, 3), "pan": c.get("pan_path") or c.get("pan", 0),
                       "license": lic})

    # music
    mus_info = []
    for m in musics:
        p = resolve(m["file"], base)
        lic_check(p)
        si, so = m.get("src_in", 0.0), m.get("src_out")
        x = sl.decode(str(p), start=si, dur=(so - si) if so else None)
        t = tsec(m.get("t", 0), fps)
        x = x[: max(0, int((dur - t) * SR))]
        x = filt(x, m.get("hpf"), m.get("lpf"))  # optional: e.g. muffled music before it "opens"
        x = fades(x.copy(), m.get("fade_in", 0.3), m.get("fade_out", 1.0)) * db(m.get("gain_db", -10))
        x = gain_path(x, m.get("gain_path"), t)  # optional: e.g. a crescendo into the climax
        add(mus_bus, x, t)
        mus_info.append({"file": m["file"], "t": t, "end": round(t + len(x) / SR, 3), "src_in": si, "src_out": so,
                         "duck_db": m.get("duck_db", -12)})

    # ducking (music only): voice sidechain + cue dips
    duck_db = min([mi["duck_db"] for mi in mus_info] or [-12])
    target = cue_duck.copy()
    if voice and np.any(voc_bus):
        env = sl.envelope_db(voc_bus, SR, hop_ms=block * 1000)
        act = env > -40
        target[: len(act)] = np.minimum(target[: len(act)], np.where(act, duck_db, 0)[: len(target)])
    gcurve = smooth_gain(target, block, attack=0.2, release=0.8, hold=0.3)
    if np.any(gcurve < -0.01):
        gs = np.interp(np.arange(n) / SR, np.arange(len(gcurve)) * block, gcurve)
        mus_bus *= (10 ** (gs / 20))[:, None].astype(np.float32)

    mix = sfx_bus + mus_bus + voc_bus
    # master: loudness + true peak, iterate
    lufs0 = sl.loudness(mix)["lufs"]
    if lufs0 is None:
        raise SystemExit("Mix ist stumm")
    gain = master["lufs"] - lufs0
    ceiling = master["true_peak"] - 0.3
    out = mix
    for _ in range(5):
        out = limiter(mix * db(gain), ceiling)
        L, tp = sl.loudness(out)["lufs"], sl.true_peak_db(out)
        if tp is not None and tp > master["true_peak"]:
            ceiling -= tp - master["true_peak"] + 0.05
            continue
        if abs(L - master["lufs"]) <= 0.5:
            break
        gain += master["lufs"] - L
    stems = {name: sl.loudness(b * db(gain))["lufs"] for name, b in
             (("sfx", sfx_bus), ("music", mus_bus), ("voice", voc_bus)) if np.any(b)}
    gr = 20 * np.log10(np.maximum(np.abs(out).max(axis=1), 1e-9)) - 20 * np.log10(np.maximum(np.abs(mix * db(gain)).max(axis=1), 1e-9))
    meas = sl.loudness(out)
    report = {"duration": dur, "fps": fps, "target": master, "lufs": meas["lufs"], "lra": meas["lra"],
              "true_peak": sl.true_peak_db(out), "master_gain_db": round(gain, 2),
              "limiter_max_reduction_db": round(float(-gr.min()), 2) if len(gr) else 0,
              "stems_lufs_after_gain": stems, "cues_per_10s": round(len(placed) / dur * 10, 2),
              "cues": placed, "music": mus_info, "warnings": warn,
              "_duck_curve": gcurve.round(2).tolist()}
    if report["limiter_max_reduction_db"] > 6:
        warn.append(f"Limiter greift bis {report['limiter_max_reduction_db']} dB: einzelne Cues leiser statt Master quetschen")
    if "music" in stems and "voice" in stems and stems["voice"] - stems["music"] < 12:
        warn.append(f"Musik nur {stems['voice'] - stems['music']:.1f} LU unter Stimme (Ziel 16-22)")
    return out, report


def waveform_png(path: str, mix: np.ndarray, rep: dict, video: str | None, strip: bool) -> None:
    from PIL import Image, ImageDraw, ImageFont
    W, H, top = 1800, 360, 70
    strip_h = 100 if (video and strip) else 0
    img = Image.new("RGB", (W, top + H + strip_h + 60), (18, 18, 20))
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
        fb = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    except OSError:
        f = fb = ImageFont.load_default()
    dur = rep["duration"]
    X = lambda t: int(t / dur * (W - 40)) + 20  # noqa: E731
    d.text((20, 12), f"LUFS {rep['lufs']}  (Ziel {rep['target']['lufs']})   True Peak {rep['true_peak']} dBTP"
           f" (Ziel <= {rep['target']['true_peak']})   LRA {rep['lra']} LU   Cues {len(rep['cues'])}"
           f" ({rep['cues_per_10s']}/10 s)   Limiter max -{rep['limiter_max_reduction_db']} dB", font=fb, fill=(235, 235, 235))
    mid = top + H // 2
    for m in rep["music"]:  # music regions
        d.rectangle([X(m["t"]), top, X(min(m["end"], dur)), top + 8], fill=(60, 110, 200))
        d.text((X(m["t"]) + 4, top + 10), "Musik " + Path(m["file"]).stem, font=f, fill=(120, 160, 230))
    mono = np.abs(mix).max(axis=1)
    cols = W - 40
    per = max(1, len(mono) // cols)
    for i in range(cols):
        seg = mono[i * per:(i + 1) * per]
        if seg.size:
            v = float(seg.max())
            h = int(v * (H / 2 - 10))
            d.line([(20 + i, mid - h), (20 + i, mid + h)], fill=(110, 200, 150))
    dc = rep.get("_duck_curve") or []
    if dc and min(dc) < -0.01:  # ducking curve (0 dB at top line, -24 dB at bottom)
        pts = [(X(i * 0.01), top + 20 + int(-v / 24 * (H - 40))) for i, v in enumerate(dc) if i * 0.01 <= dur]
        d.line(pts, fill=(230, 160, 60), width=2)
    for s in range(int(dur) + 1):  # ruler
        d.line([(X(s), top + H), (X(s), top + H + 8)], fill=(200, 200, 200))
        d.text((X(s) + 2, top + H + 8), f"{s}s", font=f, fill=(170, 170, 170))
    for j, c in enumerate(rep["cues"]):
        x = X(c["peak"] if c["align"] == "peak" else c["t"])
        d.line([(x, top + 24), (x, top + H)], fill=(240, 90, 90), width=1)
        label = (c["note"] or Path(c["file"]).stem)[:22]
        d.text((x + 3, top + 24 + (j % 6) * 18), label, font=f, fill=(250, 140, 140))
    if strip_h:
        n = 12
        th_w = (W - 40) // n
        for k in range(n):
            t = (k + 0.5) * dur / n
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                                  "-vf", f"scale={th_w}:{strip_h}:force_original_aspect_ratio=decrease",
                                  "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            if raw:
                import io
                im = Image.open(io.BytesIO(raw))
                img.paste(im, (20 + k * th_w, top + H + 30))
    img.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cues")
    ap.add_argument("--video")
    ap.add_argument("--out", required=True, help="mix.wav (48 kHz, 24 bit)")
    ap.add_argument("--mux", help="write video + mix as .mp4 (video stream copied, AAC 320k)")
    ap.add_argument("--png", help="waveform image (default: <out>.png)")
    ap.add_argument("--no-strip", action="store_true", help="no film frames under the waveform")
    a = ap.parse_args()
    cpath = Path(a.cues).resolve()
    spec = json.loads(cpath.read_text())
    video = str(Path(a.video).resolve()) if a.video else None
    mix, rep = render(spec, cpath.parent, video)
    sl.write_wav(a.out, mix)
    rep["ffmpeg_ebur128"] = ffmpeg_r128(a.out)
    png = a.png or str(Path(a.out).with_suffix(".png"))
    waveform_png(png, mix, rep, video, not a.no_strip)
    if a.mux:
        if not video:
            raise SystemExit("--mux braucht --video")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", a.out, "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", a.mux], check=True)
    rep.pop("_duck_curve", None)
    rpath = str(Path(a.out).with_suffix(".report.json"))
    Path(rpath).write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    short = {k: rep[k] for k in ("lufs", "true_peak", "lra", "master_gain_db", "limiter_max_reduction_db", "cues_per_10s")}
    short["ffmpeg_ebur128"] = rep["ffmpeg_ebur128"]
    print(json.dumps(short, ensure_ascii=False))
    for w in rep["warnings"]:
        print("WARNUNG:", w)
    print("report:", rpath, "| png:", png, "| mux:", a.mux or "-")


if __name__ == "__main__":
    main()
