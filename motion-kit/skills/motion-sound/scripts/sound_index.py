# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "librosa"]
# ///
"""Index the local sound library: measure every file and write sound/index.json.

    uv run scripts/sound_index.py                    rebuild sound/index.json (incremental: unchanged files are reused)
    uv run scripts/sound_index.py --full             re-measure everything
    uv run scripts/sound_index.py --probe a.mp3 ...  measure files anywhere, print JSON (e.g. before adding them)

Per file: path, category, tags, description, duration, LUFS (integrated; ungated for clips < 0.4 s),
true peak (dBTP), sample peak, onset/peak/attack/tail (ms), brightness (spectral centroid Hz + label),
license/source/author (from sound/sources.json, longest path prefix wins).
Music (sound/music/): + BPM (librosa, check by ear), LRA, energy curve (10 segments, LU relative to integrated),
mood/use from sources.json.

Adding sounds: put files under sound/sfx/<pack>/ or sound/music/, add a sources.json entry with the licence,
run this script. Files without a sources.json entry are indexed with license "UNBEKANNT" and must not be used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import soundlib as sl  # noqa: E402

ROOT = Path(os.environ.get("MOTION_SOUND_ROOT", Path.cwd() / "sound")).resolve()  # Bibliothek im Projekt, nicht im Plugin
STOP = {"audio", "sounds", "sfx", "cc0", "wav", "ogg"}
EXT = {".ogg", ".wav", ".mp3", ".flac", ".aif", ".aiff", ".m4a"}
SKIP = re.compile(r"(^|/)(_dl|selftest)/|/preview\.ogg$|desktop\.ini", re.I)

# category rules: first match wins (on lower-case relative path)
CATS = [
    ("jingle", r"jingles_"),
    ("foley", r"footstep|door|creak|wooded_box|key_open"),
    ("whoosh", r"whoosh|swish|whip|swoosh"),
    ("typing", r"typing|key-press"),
    ("riser", r"riser|powerup|phaserup|highup|zapthreetoneup"),
    ("paper", r"paper|book|page-turn|map-(open|close)|card-|cards-"),
    ("glitch", r"glitch|zap|laser|phaser|computernoise|lowrandom|spacetrash|phasejump|/noise_|weird|highdown|lowdown"),
    ("impact", r"impact|/hit|_hit|slam|punch|explosion|bass|gong|shot_|breaking|falling|chop|lowfrequency"),
    ("chime", r"chime|ding|bell|ping|sparkle|notification|confirmation|/glass_"),
    ("click", r"click|tick|toggle|switch|select|scroll|mouserelease|rollover|latch|shutter|equipment"),
    ("pop", r"pop|plop|pluck|drop|bong|tone|pepsound|spring|place|chip-lay|lay_"),
    ("ui", r"error|question|back|open|close|maximize|minimize|scratch"),
    ("drone", r"engine|thruster|forcefield|slime|machine"),
    ("foley", r"footstep|cloth|belt|leather|coins|knife|creak|dice|die-|chips|wood|metal|rock|tools|pot|dishes|door|glass|key_|splash|other"),
]
CAT_DE = {
    "whoosh": ("Whoosh/Luftzug", ["luft", "übergang", "swoosh", "bewegung", "wisch"]),
    "riser": ("Riser/Anstieg", ["aufbau", "spannung", "anstieg", "steigend"]),
    "impact": ("Einschlag/Hit", ["schlag", "treffer", "hit", "boom", "aufprall", "landung"]),
    "glitch": ("Digital/Glitch", ["digital", "störung", "glitch", "elektronisch", "sci-fi"]),
    "click": ("Klick", ["klick", "ui", "tap", "taste", "schalter"]),
    "pop": ("Pop/Tupfer", ["pop", "erscheinen", "tupfer", "weich", "blase"]),
    "chime": ("Klang/Ding", ["ding", "glocke", "erfolg", "hell", "klang"]),
    "typing": ("Tippen", ["tastatur", "tippen", "schreiben", "keyboard"]),
    "paper": ("Papier", ["papier", "blatt", "seite", "buch", "karte"]),
    "ui": ("UI-Geräusch", ["oberfläche", "interface", "ui"]),
    "drone": ("Brummen/Fläche", ["brummen", "fläche", "maschine", "atmo"]),
    "foley": ("Foley/Material", ["material", "geräusch", "foley"]),
    "jingle": ("Jingle/Sting", ["musik", "sting", "jingle", "kurz"]),
    "music": ("Musik", ["musik", "track", "bett"]),
    "misc": ("Sonstiges", []),
}
WORD_DE = {"wood": "holz", "wooden": "holz", "metal": "metall", "glass": "glas", "rock": "stein", "paper": "papier",
           "cloth": "stoff", "heavy": "schwer", "light": "leicht", "soft": "weich", "medium": "mittel", "door": "tür",
           "book": "buch", "flip": "blättern", "open": "öffnen", "close": "schließen", "footstep": "schritt",
           "coins": "münzen", "card": "karte", "cards": "karten", "breaking": "zerbrechen", "falling": "fallen",
           "bell": "glocke", "shutter": "auslöser", "switch": "schalter", "low": "tief", "high": "hoch",
           "up": "hoch", "down": "runter", "spring": "feder", "slam": "zuschlagen", "map": "landkarte",
           "engine": "motor", "laser": "laser", "explosion": "explosion", "punch": "schlag", "plate": "teller"}


def sources() -> list[dict]:
    p = ROOT / "sources.json"
    return json.loads(p.read_text()) if p.exists() else []


def source_for(rel: str, srcs: list[dict]) -> dict:
    best = None
    for s in srcs:
        if rel.startswith(s["prefix"]) and (best is None or len(s["prefix"]) > len(best["prefix"])):
            best = s
    return best or {"license": "UNBEKANNT", "source": None, "author": None}


def category(rel: str) -> str:
    if rel.startswith("music/"):
        return "music"
    low = rel.lower()
    name = "/" + low.rsplit("/", 1)[-1]
    for text in (name, low):  # file name decides first, pack/folder name only as fallback
        for cat, rx in CATS:
            if re.search(rx, text):
                return cat
    return "misc"


def tokens(rel: str) -> list[str]:
    stem = Path(rel).stem
    stem = re.sub(r"([a-z])([A-Z])", r"\1 \2", stem)
    words = [w.lower() for w in re.split(r"[^A-Za-z]+", stem) if len(w) > 1 and w.lower() not in STOP]
    parts = [x for x in rel.split("/")[:-1] if x.lower() not in ("audio", "sfx", "music")]
    pack = parts[-1] if parts else ""
    return words + [w for w in re.split(r"[^a-z]+", pack.lower()) if len(w) > 2 and w not in STOP]


def describe(e: dict, extra: str | None) -> str:
    if extra:
        return extra
    lab = CAT_DE[e["category"]][0]
    d = e["duration"]
    length = "sehr kurz" if d < 0.25 else "kurz" if d < 0.8 else "mittel" if d < 2.5 else "lang"
    att = e.get("attack_ms")
    hit = "harter Einsatz" if att is not None and att <= 15 else "weicher Einsatz" if att is not None and att > 60 else "mittlerer Einsatz"
    br = e.get("brightness") or "?"
    name = " ".join(tokens(e["path"])[:4])
    return f"{lab}: {name} ({length}, {br}, {hit})"


def measure(path: Path, music: bool) -> dict:
    x = sl.decode(str(path))
    dur = len(x) / sl.SR
    out = {"duration": round(dur, 3)}
    out.update(sl.loudness(x))
    out["true_peak"] = sl.true_peak_db(x)
    out["sample_peak"] = sl.sample_peak_db(x)
    out.update(sl.shape(x))
    out["centroid_hz"] = sl.centroid_hz(x)
    out["brightness"] = sl.brightness_label(out["centroid_hz"])
    if music and dur > 5:
        out.update(music_features(x, out.get("lufs")))
    return out


def music_features(x: np.ndarray, integ: float | None) -> dict:
    import librosa
    mono = x.mean(axis=1)
    y = librosa.resample(mono[: int(120 * sl.SR)], orig_sr=sl.SR, target_sr=22050)
    tempo, beats = librosa.beat.beat_track(y=y, sr=22050)
    bpm = float(np.atleast_1d(tempo)[0])
    # energy curve: loudness of 10 equal segments relative to the integrated value
    seg = len(x) // 10
    curve = []
    for i in range(10):
        v = sl.loudness(x[i * seg:(i + 1) * seg])["lufs"]
        curve.append(None if v is None or integ is None else round(v - integ, 1))
    return {"bpm": round(bpm, 1), "beats_found": int(len(beats)), "energy_curve": curve}


def build(full: bool) -> None:
    srcs = sources()
    idx_path = ROOT / "index.json"
    old = {}
    if idx_path.exists() and not full:
        for e in json.loads(idx_path.read_text()).get("files", []):
            old[e["path"]] = e
    files, seen, dups = [], {}, {}
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT).as_posix()
        if p.suffix.lower() not in EXT or SKIP.search("/" + rel):
            continue
        src = source_for(rel, srcs)
        if src.get("exclude"):
            continue
        st = p.stat()
        digest = hashlib.md5(p.read_bytes()).hexdigest()
        if digest in seen:  # identical content under another name (upstream duplicates): index once
            dups[rel] = seen[digest]
            continue
        seen[digest] = rel
        prev = old.get(rel)
        if prev and prev.get("_mtime") == int(st.st_mtime) and prev.get("_size") == st.st_size:
            m = {k: v for k, v in prev.items()}
        else:
            print("measure", rel, file=sys.stderr)
            try:
                m = measure(p, rel.startswith("music/"))
            except Exception as ex:  # unreadable file: report, keep going
                print("  FEHLER", ex, file=sys.stderr)
                continue
        e = {"path": rel, "category": category(rel)}
        e.update({k: v for k, v in m.items() if k not in ("path", "category", "tags", "description", "license",
                                                          "source", "author", "license_url")})
        info = (src.get("files") or {}).get(Path(rel).name, {})
        words = tokens(rel)
        tags = set(words) | set(CAT_DE[e["category"]][1]) | {WORD_DE[w] for w in words if w in WORD_DE}
        tags |= set(info.get("tags", [])) | set(src.get("tags", []))
        e["tags"] = sorted(tags)
        if info.get("title") and not info.get("description"):
            info = {**info, "description": f"{info['title']} ({info.get('artist')}): {info.get('mood')}. Einsatz: {info.get('use')}"}
        e["description"] = describe(e, info.get("description"))
        for k in ("mood", "use", "title", "artist"):
            if info.get(k):
                e[k] = info[k]
        if info.get("bpm"):  # hand-checked BPM beats the detector
            e["bpm_detected"], e["bpm"] = e.get("bpm"), info["bpm"]
        e["license"] = src.get("license")
        e["license_url"] = src.get("license_url")
        e["source"] = info.get("url") or src.get("url")
        e["author"] = info.get("artist") or src.get("author")
        e["_mtime"], e["_size"] = int(st.st_mtime), st.st_size
        files.append(e)
    cats = {}
    for e in files:
        cats[e["category"]] = cats.get(e["category"], 0) + 1
    unknown = [e["path"] for e in files if e["license"] == "UNBEKANNT"]
    data = {"note": "Erzeugt von scripts/sound_index.py. Nicht von Hand bearbeiten; Lizenzen/Beschreibungen in sources.json.",
            "count": len(files), "categories": dict(sorted(cats.items())), "unlicensed": unknown,
            "duplicates": dups, "files": files}
    idx_path.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(json.dumps({"count": len(files), "categories": data["categories"], "unlicensed": len(unknown)}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--probe", nargs="+")
    a = ap.parse_args()
    if a.probe:
        for f in a.probe:
            m = measure(Path(f), music=True)
            print(json.dumps({"file": os.path.basename(f), **m}, ensure_ascii=False))
        return
    build(a.full)


if __name__ == "__main__":
    main()
