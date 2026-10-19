#!/usr/bin/env python3
"""Ton-Endkontrolle am EXPORTIERTEN Film (nicht am WAV). Pure stdlib + ffmpeg.

    python3 motion-sound/scripts/sound_verify.py <film.mp4> <cues.json> --out <projekt>/check/sound

Misst, was nach AAC-Kodierung wirklich im Film steckt, und bereitet das Hören vor:
1. Lautheit des MP4 mit ffmpeg ebur128: integriert (Ziel −14 LUFS ± 1), True Peak (Ziel ≤ −1,5 dBTP: AAC erzeugt
   neue Spitzen, die im WAV nicht da waren), LRA.
2. Mono-Probe (Handy-Lautsprecher): Mono-Summe auf beiden Kanälen gegen Stereo. Gleiche Kanäle = 0 LU, ganz
   unkorrelierte = −3 LU; fällt sie um mehr als 4 LU, löschen sich Spuren aus (Phase, oft breite Stereo-Whooshes).
3. Je Cue ein Bild 2 Frames vor und 2 Frames nach dem Cue (`cue_<nr>_vor.jpg` / `_nach.jpg`): sieht man den Grund
   für den Ton? Plus `waveform.png` des fertigen Films.
4. Fünf Zeitstempel für die Kopfhörer-Probe (`HOEREN.md`): die lautesten Cues, der erste Cue, die Stelle vor
   der Endkarte. Nie „klingt gut" behaupten: du hörst nicht, du misst.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def ebur(path: str, mono: bool = False) -> dict:
    af = ("pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1," if mono else "") + "ebur128=peak=true"
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", path, "-vn", "-af", af, "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    tail = err[err.rfind("Summary:"):]

    def num(key):
        m = re.search(key + r":\s+(-?[\d.]+|-inf)", tail)
        return float(m.group(1)) if m and m.group(1) != "-inf" else None
    return {"I": num(r"\bI"), "LRA": num(r"\bLRA"), "TP": num(r"Peak")}


def frame(video: str, t: float, out: Path) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(t, 0):.3f}", "-i", video, "-frames:v", "1",
                    "-vf", "scale=640:-2", str(out)], check=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("cues")
    ap.add_argument("--out", required=True)
    ap.add_argument("--target", type=float, default=-14.0)
    ap.add_argument("--max-tp", type=float, default=-1.5)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    spec = json.loads(Path(a.cues).read_text())
    cues = sorted(spec.get("cues", spec if isinstance(spec, list) else []), key=lambda c: float(str(c["t"]).lstrip("f")))
    fps = float(spec.get("fps", 30)) if isinstance(spec, dict) else 30.0

    def sec(c):
        t = str(c["t"])
        return float(t[1:]) / fps if t.startswith("f") else float(t)

    st, mo = ebur(a.video), ebur(a.video, mono=True)
    problems = []
    if st["I"] is None:
        print("keine Tonspur gefunden", file=sys.stderr)
        return 2
    if abs(st["I"] - a.target) > 1.0:
        problems.append(f"Lautheit {st['I']} LUFS, Ziel {a.target} ± 1")
    if st["TP"] is not None and st["TP"] > a.max_tp:
        problems.append(f"True Peak {st['TP']} dBTP im MP4 > {a.max_tp} (AAC-Spitzen): Master-Limiter tiefer")
    mono_drop = round(st["I"] - mo["I"], 1) if mo["I"] is not None else None
    if mono_drop is not None and mono_drop > 4.0:
        problems.append(f"Mono {mono_drop} LU leiser als Stereo: Phasenauslöschung, breite Stereo-Cues prüfen")

    d = 2 / fps
    for i, c in enumerate(cues, 1):
        frame(a.video, sec(c) - d, out / f"cue_{i:02d}_vor.jpg")
        frame(a.video, sec(c) + d, out / f"cue_{i:02d}_nach.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-filter_complex",
                    "aformat=channel_layouts=mono,showwavespic=s=1800x240:colors=black", "-frames:v", "1",
                    str(out / "waveform.png")], check=False)

    picks = []
    if cues:
        picks.append((sec(cues[0]), "erster Ton: setzt er sauber ein?"))
        loud = sorted(cues, key=lambda c: c.get("gain_db", -99), reverse=True)[:3]
        picks += [(sec(c), f"lautester Cue ({c.get('note') or Path(c['file']).name}): zu laut, verzerrt?") for c in loud]
    dur = float(spec.get("duration", 0) or 0) if isinstance(spec, dict) else 0
    if dur:
        picks.append((max(dur - 4.0, 0), "vor der Endkarte: Stille/Ausklang richtig?"))
    seen, lines = set(), []
    for t, why in picks:
        k = round(t, 1)
        if k not in seen and len(lines) < 5:
            seen.add(k)
            lines.append(f"- **{int(t // 60)}:{t % 60:05.2f}** – {why}")
    report = {"stereo": st, "mono": mo, "mono_drop_lu": mono_drop, "problems": problems, "cues": len(cues)}
    (out / "sound_verify.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    (out / "HOEREN.md").write_text("# Kopfhörer-Probe\n\nGemessen, nicht gehört. Bitte diese Stellen mit "
                                   "Kopfhörern prüfen:\n\n" + "\n".join(lines) + "\n")
    print(f"MP4: {st['I']} LUFS, TP {st['TP']} dBTP, LRA {st['LRA']} LU · Mono −{mono_drop} LU · {len(cues)} Cues")
    for p in problems:
        print("PROBLEM:", p)
    print(f"Bilder je Cue, waveform.png, HOEREN.md -> {out}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
