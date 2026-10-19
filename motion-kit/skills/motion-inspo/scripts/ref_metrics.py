# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pillow", "ocrmac; sys_platform == 'darwin'"]
# ///
"""Messbare Grammatik eines Films: Referenz und eigener Render mit derselben Messung nebeneinander.

    uv run scripts/ref_metrics.py <video> [<video> ...] [--ref REF.mp4] [--out DIR] [--no-ocr] [--json]

Misst je Film: Einstellungen und Schnitte pro 10 s (adaptiver Schnitt-Detektor, findet auch Schnitte zwischen
ähnlichen Bildern, die ffmpeg `scene` übersieht), Ø/Median-Einstellungslänge, Anteil Bilder mit Text (OCR aus
motion_check, Apple Vision), Anteil (fast) leerer/einfarbiger Bilder und längste leere Strecke, Kamerabewegung grob
(Phasenkorrelation = Verschiebung, Bilddifferenz = Änderung, Anteil „Kamera steht"), Helligkeit, Kontrast, Sättigung,
Farbspanne, dazu dieselben Werte für den Einstieg (erste 2 s).

Mit --ref wird jeder andere Film gegen die Referenz geprüft (Ziele aus motion-director/references/inspiration.md):
Schnittdichte >= 80 % der Referenz, Textanteil <= Referenz + 10 Punkte, keine leere Strecke > 0,3 s,
Einstieg: in den ersten 2 s mindestens so viel Bewegung wie die Referenz (>= 80 %) und kein leeres Bild.
Schreibt <out>/metrics.json und <out>/metrics.md, wenn --out gesetzt ist.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from motion_check import probe  # noqa: E402  (gleiche ffprobe-Logik)

W, H = 96, 54          # Analyse-Auflösung
MAX_FPS = 30.0         # Schnitt-Detektion je Bild (bis 30 fps)
EMPTY_STD = 7.0        # Luma-Standardabweichung (0..255) darunter = (fast) einfarbig
EMPTY_EDGE = 1.2       # mittlere Kantenstärke darunter = keine Struktur
VIEW_DIFF = 28.0       # Luma-Differenz (0..255) zum Bild 0,5 s davor ab der eine neue Ansicht zählt
STILL_DIFF = 0.6       # Bilddifferenz (0..255) darunter = Bild steht
STILL_SHIFT = 0.0015   # Verschiebung (Anteil Bildbreite/Bild) darunter = Kamera steht
TEXT_H = 0.022         # OCR-Zeilenhöhe (Anteil Bildhöhe) ab der Text zählt (~24 px @1080p)
BIG_H = 0.04           # große Schrift (Titel)


def frames_rgb(path: Path, fps: float) -> np.ndarray:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={W}:{H}:flags=area",
                        "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = a.size // (W * H * 3)
    return a[: n * W * H * 3].reshape(n, H, W, 3).astype(np.float32)


def luma(fr: np.ndarray) -> np.ndarray:
    return fr[..., 0] * 0.299 + fr[..., 1] * 0.587 + fr[..., 2] * 0.114


def hist(fr: np.ndarray, bins=6) -> np.ndarray:
    q = np.clip((fr / 256 * bins).astype(np.int32), 0, bins - 1)
    idx = q[..., 0] * bins * bins + q[..., 1] * bins + q[..., 2]
    out = np.stack([np.bincount(i.ravel(), minlength=bins ** 3) for i in idx]).astype(np.float32)
    return out / out.sum(axis=1, keepdims=True)


def detect_cuts(fr: np.ndarray, fps: float) -> tuple[list[int], np.ndarray]:
    """Adaptiver Schnitt-Detektor: Sprung in Farbhistogramm + Pixeldifferenz, verglichen mit der Umgebung (±0,5 s)."""
    if len(fr) < 3:
        return [], np.zeros(0)
    h = hist(fr)
    dh = 0.5 * np.abs(h[1:] - h[:-1]).sum(axis=1)                 # 0..1
    dp = np.abs(fr[1:] - fr[:-1]).mean(axis=(1, 2, 3)) / 255.0     # 0..1
    s = 0.5 * dh + 0.5 * np.minimum(1.0, dp * 4)
    win = max(2, int(round(fps * 0.5)))
    cuts, min_gap = [], max(2, int(round(fps * 0.2)))
    for i in range(len(s)):
        lo, hi = max(0, i - win), min(len(s), i + win + 1)
        nb = np.concatenate([s[lo:max(lo, i - 1)], s[min(hi, i + 2):hi]])
        base = float(np.median(nb)) if nb.size else 0.0
        if s[i] > 0.12 and s[i] > 3.0 * base + 0.04 and s[i] == s[max(0, i - 1):i + 2].max():
            if not cuts or i + 1 - cuts[-1] >= min_gap:
                cuts.append(i + 1)  # Index des ersten Bildes der neuen Einstellung
    return cuts, s


def view_changes(lu: np.ndarray, fps: float, cuts: list[int], thresh=VIEW_DIFF) -> list[int]:
    """Neue Ansicht ohne harten Schnitt (schnelle Kamerafahrt, Schwenk, Verwandlung): das Bild unterscheidet sich stark
    von dem 0,5 s davor; Spitze der Differenz, nicht näher als 0,5 s an einem Schnitt oder einer anderen Änderung."""
    L = max(2, int(round(fps * 0.5)))
    if len(lu) <= L:
        return []
    d = np.abs(lu[L:] - lu[:-L]).mean(axis=(1, 2))
    out = []
    for i in range(len(d)):
        lo, hi = max(0, i - L), min(len(d), i + L + 1)
        if d[i] < thresh or d[i] < d[lo:hi].max():
            continue
        f = i + L // 2 + 1  # Mitte des Vergleichsfensters
        if any(abs(f - c) < L for c in cuts) or (out and f - out[-1] < L):
            continue
        # das Fenster darf keinen harten Schnitt enthalten (sonst misst es den Schnitt)
        if any(i <= c <= i + L for c in cuts):
            continue
        out.append(f)
    return out


def phase_shift(a: np.ndarray, b: np.ndarray) -> float:
    """Globale Verschiebung zwischen zwei Luma-Bildern (Anteil Bildbreite), Phasenkorrelation."""
    win = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1]))
    A, B = np.fft.fft2(a * win), np.fft.fft2(b * win)
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-6
    c = np.abs(np.fft.ifft2(R))
    y, x = np.unravel_index(np.argmax(c), c.shape)
    hh, ww = c.shape

    def sub(m, p, n):  # parabolische Unterpixel-Lage des Maximums
        den = m - 2 * p + n
        return 0.0 if abs(den) < 1e-9 else 0.5 * (m - n) / den
    fy = y + sub(c[(y - 1) % hh, x], c[y, x], c[(y + 1) % hh, x])
    fx = x + sub(c[y, (x - 1) % ww], c[y, x], c[y, (x + 1) % ww])
    if fy > hh / 2:
        fy -= hh
    if fx > ww / 2:
        fx -= ww
    return float(np.hypot(fx / ww, fy / hh))


def edge(lu: np.ndarray) -> np.ndarray:
    gx = np.abs(np.diff(lu, axis=2)).mean(axis=(1, 2))
    gy = np.abs(np.diff(lu, axis=1)).mean(axis=(1, 2))
    return gx + gy


def saturation(fr: np.ndarray) -> np.ndarray:
    mx, mn = fr.max(axis=3), fr.min(axis=3)
    return np.where(mx > 1, (mx - mn) / np.maximum(mx, 1), 0)


def hue_spread(fr: np.ndarray) -> float:
    """Farbspanne: wie viele 30°-Farbtonsektoren tragen nennenswert (gesättigte Pixel) bei (0..12)."""
    r, g, b = fr[..., 0], fr[..., 1], fr[..., 2]
    mx, mn = fr.max(axis=3), fr.min(axis=3)
    sat = (mx - mn) / np.maximum(mx, 1)
    m = (sat > 0.25) & (mx > 40)
    if m.sum() < 50:
        return 0.0
    d = np.maximum(mx - mn, 1e-3)
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    hh = np.bincount((hue[m] // 30).astype(int) % 12, minlength=12) / m.sum()
    return float((hh > 0.03).sum())


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    out, st = [], None
    for i, v in enumerate(list(mask) + [False]):
        if v and st is None:
            st = i
        elif not v and st is not None:
            out.append((st, i)); st = None
    return out


def ocr_share(path: Path, dur: float, first: float = 2.0) -> dict:
    try:
        from motion_check import ocr_frames
    except Exception:  # noqa: BLE001
        return {}
    with tempfile.TemporaryDirectory() as td:
        samples = ocr_frames(path, 0.0, dur, Path(td))
    has = [(t, any(l.h >= TEXT_H for l in ls), any(l.h >= BIG_H for l in ls), sum(len(l.text.split()) for l in ls if l.h >= TEXT_H))
           for t, ls in samples]
    if not has:
        return {}
    n = len(has)
    f = [x for x in has if x[0] < first]
    return {"text_share": round(sum(x[1] for x in has) / n, 3), "big_text_share": round(sum(x[2] for x in has) / n, 3),
            "words_per_text_frame": round(np.mean([x[3] for x in has if x[1]]) if any(x[1] for x in has) else 0.0, 1),
            "first2_text_share": round(sum(x[1] for x in f) / max(1, len(f)), 3)}


def measure(path: Path, use_ocr=True) -> dict:
    m = probe(path)
    dur, fps = m["duration"], min(MAX_FPS, m["fps"])
    fr = frames_rgb(path, fps)
    n = len(fr)
    lu = luma(fr)
    cuts, _ = detect_cuts(fr, fps)
    views = view_changes(lu, fps, cuts)
    bounds = [0] + cuts + [n]
    shots = [(b - a) / fps for a, b in zip(bounds, bounds[1:]) if b > a]
    # Bewegung innerhalb der Einstellungen (Schnittbilder ausgenommen)
    cutset = set(cuts)
    diffs, shifts = [], []
    for i in range(1, n):
        if i in cutset:
            continue
        diffs.append(float(np.abs(lu[i] - lu[i - 1]).mean()))
        shifts.append(phase_shift(lu[i - 1], lu[i]))
    diffs, shifts = np.array(diffs or [0.0]), np.array(shifts or [0.0])
    still = (diffs < STILL_DIFF) & (shifts < STILL_SHIFT)
    # leere Bilder
    std = lu.reshape(n, -1).std(axis=1)
    ed = edge(lu)
    empty = (std < EMPTY_STD) | (ed < EMPTY_EDGE)
    black = lu.reshape(n, -1).mean(axis=1) < 14
    empty_runs = [((b - a) / fps, a / fps) for a, b in runs(empty)]
    longest_empty = max(empty_runs, default=(0.0, 0.0))
    sat = saturation(fr).reshape(n, -1).mean(axis=1)
    mean_l = lu.reshape(n, -1).mean(axis=1)
    k2 = int(round(2.0 * fps))
    first_cuts = [c for c in cuts if c < k2]
    first_diffs = [float(np.abs(lu[i] - lu[i - 1]).mean()) for i in range(1, min(n, k2)) if i not in cutset]
    sample = fr[:: max(1, int(fps // 2))]
    out = {
        "file": str(path), "duration": round(dur, 2), "fps": round(m["fps"], 2), "res": f'{m["w"]}x{m["h"]}',
        "shots": len(shots), "cuts_per_10s": round(len(cuts) / dur * 10, 2),
        "shot_mean": round(float(np.mean(shots)), 2), "shot_median": round(float(np.median(shots)), 2),
        "shot_max": round(float(np.max(shots)), 2),
        "cut_times": [round(c / fps, 2) for c in cuts],
        "view_changes_per_10s": round((len(cuts) + len(views)) / dur * 10, 2),   # harte Schnitte + neue Ansichten
        "view_times": [round(v / fps, 2) for v in views],
        "motion_diff": round(float(np.mean(diffs)), 2),                     # mittlere Bildänderung je Bild (0..255)
        "camera_shift_pct_s": round(float(np.median(shifts)) * fps * 100, 1),  # Verschiebung, % Bildbreite pro s (Median)
        "still_share": round(float(still.mean()), 3),                      # Anteil Bilder, in denen nichts passiert
        "empty_share": round(float(empty.mean()), 3), "black_share": round(float(black.mean()), 3),
        "longest_empty_s": round(longest_empty[0], 2), "longest_empty_at": round(longest_empty[1], 2),
        "empty_runs_over_0_3s": [[round(a, 2), round(d, 2)] for d, a in empty_runs if d > 0.3],
        "brightness": round(float(mean_l.mean()), 1), "bright_share": round(float((mean_l > 128).mean()), 3),
        "contrast": round(float(std.mean()), 1), "saturation": round(float(sat.mean()), 3),
        "hue_sectors": round(float(np.mean([hue_spread(s[None]) for s in sample])), 1),
        "first2": {"cuts": len(first_cuts), "motion_diff": round(float(np.mean(first_diffs or [0])), 2),
                   "empty_share": round(float(empty[:k2].mean()), 3), "brightness": round(float(mean_l[:k2].mean()), 1)},
    }
    if use_ocr:
        out.update(ocr_share(path, dur))
    return out


ROWS = [
    ("Dauer s", "duration"), ("Einstellungen", "shots"), ("Schnitte/10 s", "cuts_per_10s"),
    ("neue Ansichten/10 s", "view_changes_per_10s"), ("Ø Einstellung s", "shot_mean"), ("Median Einst. s", "shot_median"), ("längste Einst. s", "shot_max"),
    ("Text-Anteil", "text_share"), ("große Schrift", "big_text_share"), ("leer/einfarbig", "empty_share"),
    ("längste Leere s", "longest_empty_s"), ("Bildänderung", "motion_diff"), ("Kamera %/s", "camera_shift_pct_s"),
    ("steht-Anteil", "still_share"), ("Helligkeit", "brightness"), ("hell-Anteil", "bright_share"),
    ("Kontrast", "contrast"), ("Sättigung", "saturation"), ("Farbsektoren", "hue_sectors"),
    ("Einstieg: Schnitte 0–2 s", ("first2", "cuts")), ("Einstieg: Bildänderung", ("first2", "motion_diff")),
    ("Einstieg: leer", ("first2", "empty_share")), ("Einstieg: Text", "first2_text_share"),
]


def get(d, k):
    if isinstance(k, tuple):
        return d.get(k[0], {}).get(k[1], "–")
    return d.get(k, "–")


def targets(ref: dict, f: dict) -> list[tuple[str, bool, str]]:
    out = []
    out.append(("Schnittdichte ≥ 80 % Referenz", f["cuts_per_10s"] >= 0.8 * ref["cuts_per_10s"],
                f'{f["cuts_per_10s"]} vs Ziel ≥ {0.8 * ref["cuts_per_10s"]:.2f}'))
    out.append(("neue Ansichten ≥ 80 % Referenz", f["view_changes_per_10s"] >= 0.8 * ref["view_changes_per_10s"],
                f'{f["view_changes_per_10s"]} vs Ziel ≥ {0.8 * ref["view_changes_per_10s"]:.2f}'))
    if "text_share" in f and "text_share" in ref:
        out.append(("Textanteil ≤ Referenz + 10 Pkt", f["text_share"] <= ref["text_share"] + 0.10,
                    f'{f["text_share"]:.0%} vs Ziel ≤ {ref["text_share"] + 0.10:.0%}'))
    out.append(("keine leere Strecke > 0,3 s", not f["empty_runs_over_0_3s"],
                ", ".join(f"{a}s ({d}s)" for a, d in f["empty_runs_over_0_3s"]) or "frei"))
    out.append(("Einstieg bewegt ≥ 80 % Referenz", f["first2"]["motion_diff"] >= 0.8 * ref["first2"]["motion_diff"],
                f'{f["first2"]["motion_diff"]} vs Ziel ≥ {0.8 * ref["first2"]["motion_diff"]:.2f}'))
    out.append(("Einstieg ohne Leere", f["first2"]["empty_share"] == 0, f'{f["first2"]["empty_share"]:.0%}'))
    out.append(("Kamera steht nicht öfter als Referenz + 15 Pkt", f["still_share"] <= ref["still_share"] + 0.15,
                f'{f["still_share"]:.0%} vs Ziel ≤ {ref["still_share"] + 0.15:.0%}'))
    return out


def table(res: list[dict]) -> str:
    names = [Path(r["file"]).stem[:22] for r in res]
    lines = ["| Messung | " + " | ".join(names) + " |", "|---|" + "---|" * len(res)]
    for label, k in ROWS:
        vals = []
        for r in res:
            v = get(r, k)
            if isinstance(v, float) and k in ("text_share", "big_text_share", "empty_share", "still_share", "bright_share", "first2_text_share") or (isinstance(k, tuple) and k[1] == "empty_share"):
                v = f"{v:.0%}" if isinstance(v, (int, float)) else v
            vals.append(str(v))
        lines.append(f"| {label} | " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--ref", help="Referenzfilm: alle anderen werden gegen ihn geprüft")
    ap.add_argument("--out", help="Ordner für metrics.json + metrics.md")
    ap.add_argument("--no-ocr", action="store_true")
    ap.add_argument("--json", action="store_true", help="nur JSON auf stdout")
    a = ap.parse_args()
    paths = ([Path(a.ref)] if a.ref else []) + [Path(v) for v in a.videos if not a.ref or Path(v).resolve() != Path(a.ref).resolve()]
    res = [measure(p.resolve(), use_ocr=not a.no_ocr) for p in paths]
    md = ["# ref_metrics", "", table(res), ""]
    if a.ref:
        ref = res[0]
        for f in res[1:]:
            md += [f"## {Path(f['file']).stem} gegen {Path(ref['file']).stem}", ""]
            for name, ok, detail in targets(ref, f):
                md.append(f"- {'✓' if ok else '✗'} {name}: {detail}")
            md.append("")
    md += ["Schnitte | neue Ansichten ohne Schnitt (s):", ""] + [f"- {Path(r['file']).stem}: {r['cut_times']} | {r['view_times']}" for r in res]
    text = "\n".join(md)
    if a.out:
        o = Path(a.out); o.mkdir(parents=True, exist_ok=True)
        (o / "metrics.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
        (o / "metrics.md").write_text(text + "\n")
    print(json.dumps(res, indent=1, ensure_ascii=False) if a.json else text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
