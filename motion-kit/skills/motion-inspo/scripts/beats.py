# /// script
# requires-python = ">=3.10"
# dependencies = ["librosa", "numpy", "soundfile", "matplotlib"]
# ///
"""Beat grid for timing motion to music.

    uv run scripts/beats.py <music.wav|mp3> --out <projekt>/beats.json [--fps 30]  measure BPM, beats, bars from the track
    uv run scripts/beats.py --bpm 120 --dur 40 --out <projekt>/beats.json [--fps 30]  pure grid without music

beats.json: {bpm, fps, beats: [{t, frame, bar, beat}], bars: [t...], downbeats_frames: [...]}
Key events (logo hit, cut, word slam) go on downbeats; secondary moves on beats; nothing important off-grid.
Measured mode assumes 4/4 and takes the strongest-onset beat of the first bars as beat 1; check by ear.

Off-beat-Prüfung (immer im Messmodus): librosa rastet manchmal auf den Off-Beat ein (Raster um eine halbe
Zählzeit, z. B. 0,22 s, verschoben). Das Skript misst die Kick-Energie unter 120 Hz, sucht die Verschiebung des
ganzen Rasters, bei der die Schläge auf den Kicks liegen, und verschiebt das Raster automatisch (--no-shift
schaltet das ab). `--plot <png>` zeichnet Kick-Hüllkurve gegen Raster für 4 Takte: ansehen, ob die Linien auf den
Spitzen sitzen.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def grid(bpm: float, dur: float, offset: float = 0.0) -> list[float]:
    step = 60.0 / bpm
    return [round(offset + i * step, 4) for i in range(int((dur - offset) / step) + 1)]


def measure(path: str) -> tuple[float, list[float], int]:
    import librosa
    y, sr = librosa.load(path, sr=22050, mono=True)
    tempo, frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
    times = librosa.frames_to_time(frames, sr=sr)
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    strength = [float(onset[min(f, len(onset) - 1)]) for f in frames]
    # beat 1 = phase (0..3) whose beats are strongest on average
    phase = int(np.argmax([np.mean(strength[p::4]) if strength[p::4] else 0 for p in range(4)]))
    bpm = float(np.atleast_1d(tempo)[0])
    return bpm, [round(float(t), 4) for t in times], phase


def kick_check(path: str, times: list[float], bpm: float, plot: str | None) -> float:
    """Best whole-grid shift (s) that puts beats on kick energy below 120 Hz."""
    import librosa
    y, sr = librosa.load(path, sr=22050, mono=True)
    hop = 256
    env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop, fmax=120, n_mels=16)
    t_env = librosa.frames_to_time(np.arange(len(env)), sr=sr, hop_length=hop)
    period = 60.0 / bpm
    tb = np.array(times)
    shifts = np.arange(-period / 2, period / 2, 0.005)
    score = [np.interp(tb + d, t_env, env).mean() for d in shifts]
    best = float(shifts[int(np.argmax(score))])
    if plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        t0 = tb[min(4, len(tb) - 1)]
        t1 = t0 + 16 * period
        m = (t_env >= t0) & (t_env <= t1)
        fig, ax = plt.subplots(figsize=(14, 3))
        ax.plot(t_env[m], env[m], color="k", lw=0.8, label="Kick < 120 Hz")
        for b in tb[(tb >= t0) & (tb <= t1)]:
            ax.axvline(b, color="r", lw=0.6)
            ax.axvline(b + best, color="g", lw=0.6, ls="--")
        ax.set_title(f"rot = librosa-Raster, grün = verschoben um {best * 1000:+.0f} ms")
        fig.tight_layout()
        fig.savefig(plot, dpi=110)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio", nargs="?")
    ap.add_argument("--bpm", type=float)
    ap.add_argument("--dur", type=float)
    ap.add_argument("--offset", type=float, default=0.0, help="grid mode: time of the first downbeat")
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--no-shift", action="store_true", help="Off-Beat-Korrektur nicht anwenden, nur melden")
    ap.add_argument("--plot", help="PNG: Kick-Hüllkurve gegen Raster (4 Takte)")
    ap.add_argument("--out", required=True, help="Zieldatei im Projektordner (nie ins aktuelle Verzeichnis raten)")
    a = ap.parse_args()
    if a.audio:
        bpm, times, phase = measure(a.audio)
        shift = kick_check(a.audio, times, bpm, a.plot)
        if abs(shift) > 0.03:
            print(f"WARNUNG: Raster liegt {shift * 1000:+.0f} ms neben den Kicks (< 120 Hz)"
                  + ("" if a.no_shift else " -> ganzes Raster verschoben"))
            if not a.no_shift:
                times = [round(t + shift, 4) for t in times]
        else:
            print(f"Kick-Prüfung ok (Abweichung {shift * 1000:+.0f} ms)")
    elif a.bpm and a.dur:
        bpm, times, phase = a.bpm, grid(a.bpm, a.dur, a.offset), 0
    else:
        ap.error("give an audio file or --bpm and --dur")
    beats = []
    for i, t in enumerate(times):
        k = i - phase
        beats.append({"t": t, "frame": int(round(t * a.fps)), "bar": k // 4 + 1 if k >= 0 else 0, "beat": k % 4 + 1})
    bars = [b["t"] for b in beats if b["beat"] == 1 and b["bar"] > 0]
    out = {"bpm": round(bpm, 2), "fps": a.fps, "source": a.audio or "grid", "beats": beats, "bars": bars,
           "downbeats_frames": [int(round(t * a.fps)) for t in bars]}
    Path(a.out).write_text(json.dumps(out, indent=1))
    print(f"{out['bpm']} BPM, {len(beats)} beats, {len(bars)} bars -> {a.out}")
    print("first downbeats (s):", bars[:8])


if __name__ == "__main__":
    main()
