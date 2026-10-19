# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pillow", "ocrmac; sys_platform == 'darwin'"]
# ///
"""Mechanical slop check for a rendered motion piece. Catches what reviewers keep missing by eye:
slide layouts (headline top-left + picture below), sentences standing still, on-screen text that repeats the
voice-over, frozen time, overlong shots, text walls and summary grids.

    uv run scripts/motion_check.py <video> [--out DIR] [--script transcript.txt] [--max-shot 3.5] [--long-shots 1]
                                 [--end-hold 2.0] [--strict-shots] [--from S --to S]

Writes <out>/check.md, <out>/check.json, <out>/sheet_*.jpg (1 frame/s with time stamps) and <out>/flags/*.jpg.
Exit code 1 if any HARD flag fired. The check is a gate, not a taste judge: passing it means "no known slop
shape found", the critic still has to look at the frames.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np

OCR_FPS = 2.0      # OCR samples per second
DIFF_FPS = 8.0     # frame-difference samples per second
BIG_H = 0.04       # line height (fraction of frame height) that counts as display type, ~43 px at 1080p
MID_H = 0.028      # still clearly readable display/body type, above typical UI text
FROZEN_DIFF = 0.35 # mean abs luma diff (0..255) between samples below which time counts as frozen
CHANGE_DIFF = 18.0 # mean abs luma diff vs. 1 s earlier that counts as a new picture (soft transition)
DENSE_LINES = 8    # more text lines than this in a frame = UI/document screen, not display typography


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def probe(path: Path) -> dict:
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(path)], text=True)
    j = json.loads(r.stdout)
    st = j["streams"][0]
    num, den = st["r_frame_rate"].split("/")
    return {"w": int(st["width"]), "h": int(st["height"]), "fps": float(num) / float(den),
            "duration": float(j["format"]["duration"])}


def norm_text(s: str) -> str:
    return re.sub(r"[^0-9a-zäöüß]+", "", s.lower())


def words(s: str) -> int:
    return len([w for w in re.split(r"\s+", s.strip()) if w])


# ------------------------------------------------------------------ shots + motion
def scene_cuts(path: Path, t0: float, t1: float, thresh=0.30) -> list[float]:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", str(t0), "-to", str(t1), "-i", str(path), "-vf",
                        f"select='gt(scene,{thresh})',showinfo", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    return sorted(t0 + float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr))


def gray_frames(path: Path, t0: float, t1: float) -> np.ndarray:
    w, h = 160, 90
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-to", str(t1), "-i", str(path), "-vf",
                        f"fps={DIFF_FPS},scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True)
    fr = np.frombuffer(r.stdout, np.uint8)
    n = fr.size // (w * h)
    return fr[: n * w * h].reshape(n, h, w).astype(np.float32)


def soft_changes(fr: np.ndarray, t0: float, thresh=CHANGE_DIFF) -> list[float]:
    """Picture changes without a hard cut (cross-fades, wipes, whip-pans): the frame differs strongly from the one
    a second earlier, taken at the local maximum of that difference."""
    k = int(DIFF_FPS)
    if len(fr) <= k:
        return []
    d = np.abs(fr[k:] - fr[:-k]).mean(axis=(1, 2))
    out = []
    for i in range(len(d)):
        lo, hi = max(0, i - k // 2), min(len(d), i + k // 2 + 1)
        if d[i] > thresh and d[i] == d[lo:hi].max():
            out.append(t0 + (i + k / 2) / DIFF_FPS)
    return out


def runs(mask: np.ndarray, step: float, t0: float) -> list[tuple[float, float]]:
    out, start = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and start is None:
            start = i
        elif not m and start is not None:
            out.append((t0 + start * step, t0 + i * step))
            start = None
    return out


# ------------------------------------------------------------------ OCR
@dataclass
class Line:
    text: str
    conf: float
    x: float      # left, 0..1
    top: float    # top, 0..1 (origin top-left)
    w: float
    h: float

    @property
    def cx(self):
        return self.x + self.w / 2


def ocr_frames(path: Path, t0: float, t1: float, tmp: Path) -> list[tuple[float, list[Line]]]:
    try:
        from ocrmac import ocrmac
    except ImportError:
        print("[motion_check] OCR nicht verfügbar (ocrmac läuft nur auf macOS): Text-Prüfungen werden übersprungen.", file=sys.stderr)
        return []
    sh(["ffmpeg", "-v", "error", "-ss", str(t0), "-to", str(t1), "-i", str(path), "-vf",
        f"fps={OCR_FPS},scale=1280:-2", str(tmp / "o_%05d.png")])
    res = []
    for i, p in enumerate(sorted(tmp.glob("o_*.png"))):
        t = t0 + (i + 0.5) / OCR_FPS
        lines = []
        for text, conf, (x, y, w, h) in ocrmac.OCR(str(p), recognition_level="accurate",
                                                    language_preference=["de-DE", "en-US"]).recognize():
            if conf < 0.4 or len(text.strip()) < 2:
                continue
            lines.append(Line(text.strip(), round(conf, 2), x, 1 - (y + h), w, h))
        res.append((t, lines))
    return res


def persistent_lines(samples, min_h: float) -> list[dict]:
    """Group identical text at a stable position across consecutive samples -> spans with duration."""
    open_spans: dict[str, dict] = {}
    done = []
    step = 1 / OCR_FPS
    for t, lines in samples:
        seen = set()
        for ln in lines:
            if ln.h < min_h:
                continue
            key = norm_text(ln.text)
            if len(key) < 3:
                continue
            sp = open_spans.get(key)
            if sp and abs(sp["x"] - ln.x) < 0.02 and abs(sp["top"] - ln.top) < 0.02 and abs(sp["h"] - ln.h) < 0.01:
                sp["t1"] = t
            else:
                if sp:
                    done.append(sp)
                open_spans[key] = {"text": ln.text, "t0": t, "t1": t, "x": ln.x, "top": ln.top, "w": ln.w, "h": ln.h}
            seen.add(key)
        for key in [k for k in open_spans if k not in seen]:
            done.append(open_spans.pop(key))
    done.extend(open_spans.values())
    for sp in done:
        sp["dur"] = round(sp["t1"] - sp["t0"] + step, 2)
    return done


def grid_frames(samples) -> list[float]:
    """Frames with 4..10 mid-size text blocks laid out in >=2 rows and >=2 columns (summary-card grids)."""
    hits = []
    for t, lines in samples:
        mids = [ln for ln in lines if MID_H * 0.75 <= ln.h < BIG_H * 1.6]
        if not 4 <= len(mids) <= 10 or len(lines) > DENSE_LINES + 2:
            continue
        cols = sorted({round(ln.x, 1) for ln in mids})
        rows = sorted({round(ln.top, 1) for ln in mids})
        if len(cols) >= 2 and len(rows) >= 2:
            hits.append(t)
    return hits


# ------------------------------------------------------------------ main
@dataclass
class Flag:
    kind: str
    hard: bool
    t0: float
    t1: float
    detail: str


@dataclass
class Report:
    video: str
    meta: dict
    stats: dict = field(default_factory=dict)
    flags: list[Flag] = field(default_factory=list)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out")
    ap.add_argument("--script", help="spoken text / transcript (txt) for echo detection")
    ap.add_argument("--max-shot", type=float, default=3.5)
    ap.add_argument("--long-shots", type=int, default=1, help="shots allowed above --max-shot (the one long move)")
    ap.add_argument("--strict-shots", action="store_true", help="overlong shots become HARD flags")
    ap.add_argument("--end-card", type=float, default=4.0, help="last seconds exempt from frozen/static checks (logo, URL)")
    ap.add_argument("--min-tempo", type=float, default=3.0, help="picture changes per 10 s below this = soft flag")
    ap.add_argument("--from", dest="t_from", type=float, default=0.0)
    ap.add_argument("--to", dest="t_to", type=float)
    a = ap.parse_args()

    vid = Path(a.video).resolve()
    meta = probe(vid)
    t0, t1 = a.t_from, a.t_to or meta["duration"]
    out = Path(a.out or vid.with_suffix("").as_posix() + "_check").resolve()
    (out / "flags").mkdir(parents=True, exist_ok=True)
    rep = Report(str(vid), meta)
    F = rep.flags.append

    # shots: hard cuts + soft picture changes
    cuts = scene_cuts(vid, t0, t1)
    fr = gray_frames(vid, t0, t1)
    changes = [c for c in soft_changes(fr, t0) if all(abs(c - x) > 0.75 for x in cuts)]
    bounds = [t0] + sorted(cuts + changes) + [t1]
    shots = [round(b - a_, 2) for a_, b in zip(bounds, bounds[1:]) if b - a_ > 0.05]
    long_ = sorted([(b - a_, a_, b) for a_, b in zip(bounds, bounds[1:]) if b - a_ > a.max_shot], reverse=True)
    for i, (d, s0, s1) in enumerate(long_):
        if i >= a.long_shots:
            F(Flag("long_shot", a.strict_shots, round(s0, 2), round(s1, 2),
                   f"{d:.1f} s ohne Schnitt (erlaubt: {a.long_shots} Einstellung(en) über {a.max_shot} s)"))

    # frozen time
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)) if len(fr) > 1 else np.zeros(0)
    step = 1 / DIFF_FPS
    end_card = t1 - a.end_card
    frozen_total = 0.0
    for r0, r1 in runs(d < FROZEN_DIFF, step, t0):
        r1 = min(r1, end_card)
        if r1 - r0 >= 1.0:
            frozen_total += r1 - r0
            F(Flag("frozen", True, round(r0, 2), round(r1, 2), f"{r1 - r0:.1f} s ohne sichtbare Bewegung"))

    # OCR-based checks
    with tempfile.TemporaryDirectory() as td:
        samples = ocr_frames(vid, t0, t1, Path(td))
    dense = {round(t, 2) for t, ls in samples if len(ls) > DENSE_LINES}
    step_o = 1 / OCR_FPS

    def on_ui(sp):  # most samples of the span are dense UI/document screens
        ts = [round(sp["t0"] + i * step_o, 2) for i in range(int(round((sp["t1"] - sp["t0"]) * OCR_FPS)) + 1)]
        return sum(t in dense for t in ts) > len(ts) / 2

    def in_end_card(sp):
        return sp["t0"] >= end_card
    spans_big = [sp for sp in persistent_lines(samples, BIG_H) if not in_end_card(sp)]
    spans_mid = [sp for sp in persistent_lines(samples, MID_H) if not in_end_card(sp)]
    for sp in spans_big:
        n = words(sp["text"])
        if sp["dur"] >= 1.5 and (n >= 2 or len(norm_text(sp["text"])) >= 10) and sp["x"] < 0.2 and sp["top"] < 0.35:
            F(Flag("headline_slide", True, sp["t0"], sp["t1"],
                   f"Überschrift oben links „{sp['text']}“ steht {sp['dur']} s (Folienraster)"))
    for sp in spans_mid:
        n = words(sp["text"])
        if sp["dur"] >= 2.5 and (n >= 3 or len(norm_text(sp["text"])) >= 18):
            if on_ui(sp):
                continue  # UI/document text: frozen + long_shot cover a static screen
            F(Flag("static_sentence", True, sp["t0"], sp["t1"],
                   f"Satz „{sp['text']}“ steht {sp['dur']} s still"))
    if a.script:
        script = norm_text(Path(a.script).read_text())
        seen = set()
        for sp in spans_mid:
            key = norm_text(sp["text"])
            if len(key) >= 12 and key in script and key not in seen:
                seen.add(key)
                F(Flag("echo", True, sp["t0"], sp["t1"], f"wiederholt Gesprochenes: „{sp['text']}“"))
    # text load + grids
    heavy = []
    for t, lines in samples:
        n = sum(words(ln.text) for ln in lines if ln.h >= MID_H)
        if n > 8 and len(lines) <= DENSE_LINES:
            heavy.append(t)
    for r0, r1 in runs(np.isin(np.arange(len(samples)), [int(round((t - t0) * OCR_FPS - 0.5)) for t in heavy]),
                       1 / OCR_FPS, t0):
        if r1 - r0 >= 1.0:
            F(Flag("text_wall", False, round(r0, 2), round(r1, 2), "mehr als 8 große Wörter gleichzeitig im Bild"))
    g = grid_frames(samples)
    for r0, r1 in runs(np.isin(np.arange(len(samples)), [int(round((t - t0) * OCR_FPS - 0.5)) for t in g]),
                       1 / OCR_FPS, t0):
        if r1 - r0 >= 1.0:
            F(Flag("grid", False, round(r0, 2), round(r1, 2), "Textblöcke im Raster (Zusammenfassungs-Karten?)"))

    text_time = sum(1 for _, ls in samples if any(ln.h >= MID_H for ln in ls)) / OCR_FPS
    dur = t1 - t0
    rep.stats = {
        "duration_s": round(dur, 2), "shots": len(shots), "avg_shot_s": round(float(np.mean(shots)), 2) if shots else None,
        "median_shot_s": round(float(np.median(shots)), 2) if shots else None,
        "longest_shot_s": round(max(shots), 2) if shots else None, "hard_cuts": len(cuts), "soft_changes": len(changes),
        "picture_changes_per_10s": round((len(cuts) + len(changes)) / dur * 10, 2),
        "frozen_s": round(frozen_total, 2), "motion_mean": round(float(d.mean()), 2) if d.size else 0,
        "display_text_on_screen_pct": round(100 * text_time / dur, 1),
        "motion_per_second": [round(float(d[int(i * DIFF_FPS):int((i + 1) * DIFF_FPS)].mean()), 2)
                              for i in range(int(dur)) if d[int(i * DIFF_FPS):int((i + 1) * DIFF_FPS)].size],
    }
    pc = rep.stats["picture_changes_per_10s"]
    if pc < a.min_tempo:
        F(Flag("tempo", False, round(t0, 2), round(t1, 2),
               f"{pc} Bildwechsel pro 10 s (Profi-Launchfilme im Test: 3,5–7,5; Ziel ≥ {a.min_tempo})"))
    rep.flags.sort(key=lambda f: f.t0)

    # sheet + flag frames
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from sheet import sheets
    sheets(str(vid), str(out / "sheet"), every=1.0, t0=t0, t1=t1, cols=6 if meta["w"] >= meta["h"] else 8)
    for i, f in enumerate(rep.flags[:16]):
        tm = (f.t0 + f.t1) / 2
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{tm:.2f}", "-i", str(vid), "-frames:v", "1", "-vf",
                        "scale=960:-2", str(out / "flags" / f"{i:02d}_{f.kind}_{tm:.1f}s.jpg")])

    (out / "check.json").write_text(json.dumps({**asdict(rep)}, ensure_ascii=False, indent=1))
    hard = [f for f in rep.flags if f.hard]
    md = [f"# motion_check: {vid.name}", "",
          f"**{'DURCHGEFALLEN' if hard else 'BESTANDEN'}**: {len(hard)} harte, {len(rep.flags) - len(hard)} weiche Flags", "",
          "| Wert | |", "|---|---|"]
    for k, v in rep.stats.items():
        if k != "motion_per_second":
            md.append(f"| {k} | {v} |")
    md += ["", "| Zeit | Art | hart | Befund |", "|---|---|---|---|"]
    for f in rep.flags:
        md.append(f"| {f.t0:.1f}–{f.t1:.1f} s | {f.kind} | {'ja' if f.hard else ''} | {f.detail} |")
    md += ["", "Kontaktbögen: `sheet_*.jpg` (1 Bild/s), Flag-Bilder: `flags/`. Bestanden heißt nur: keine bekannte",
           "Slop-Form gefunden. Geschmack prüft der Critic an den Bildern."]
    (out / "check.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
