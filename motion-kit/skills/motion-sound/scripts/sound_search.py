"""Search the sound library index (sound/index.json). Pure stdlib.

    python3 scripts/sound_search.py papier                      words match tags/description/category/file name
    python3 scripts/sound_search.py whoosh --max-dur 0.6 --attack fast
    python3 scripts/sound_search.py --cat impact --dark -n 5
    python3 scripts/sound_search.py --music --mood ruhig --bpm 90-110
    python3 scripts/sound_search.py klick --json                full entries for scripting
    python3 scripts/sound_search.py --stats                     categories and counts

Words are ANDed; --not WORD excludes (repeatable: "glas --not breaking"). Results are ranked by match quality,
then by how "clean" the sound is (short leading silence). Listen before choosing: the index measures,
it does not hear. Licence column: CC0 / Pixabay. Never use a file marked UNBEKANNT.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("MOTION_SOUND_ROOT", Path.cwd() / "sound")).resolve()  # Bibliothek im Projekt, nicht im Plugin


def load() -> list[dict]:
    p = ROOT / "index.json"
    if not p.exists():
        sys.exit("sound/index.json fehlt: erst `uv run scripts/sound_index.py` ausführen")
    return json.loads(p.read_text())["files"]


# Deutsche Suchwörter -> englische Tags der Quellpakete (Kenney, OpenGameArt, Pixabay sind englisch verschlagwortet).
DE = {
    "klick": "click", "klicken": "click", "schlag": "hit", "treffer": "hit", "aufprall": "impact", "einschlag": "impact",
    "wusch": "whoosh", "zisch": "swoosh", "schwung": "swoosh", "übergang": "transition", "anstieg": "riser",
    "glitzer": "shimmer", "schimmer": "shimmer", "funkeln": "sparkle", "glocke": "bell", "gong": "gong",
    "papier": "paper", "blatt": "paper", "stift": "pencil", "bleistift": "pencil", "kritzeln": "scribble",
    "schreiben": "write", "tippen": "typing", "tastatur": "keyboard", "maus": "mouse", "knopf": "button",
    "glas": "glass", "metall": "metal", "holz": "wood", "stein": "stone", "wasser": "water", "luft": "air",
    "plopp": "pop", "blase": "bubble", "fehler": "error", "erfolg": "success", "hinweis": "notification",
    "pieps": "beep", "piepen": "beep", "rauschen": "noise", "knistern": "crackle", "explosion": "explosion",
    "rakete": "rocket", "motor": "engine", "laser": "laser", "tief": "low", "hoch": "high", "trommel": "drum",
    "schnell": "fast", "langsam": "slow", "weich": "soft", "hart": "hard", "hell": "bright", "dunkel": "dark",
    "zauber": "magic", "mechanisch": "mechanical", "schalter": "switch", "tür": "door", "schritt": "step",
}


def score(e: dict, words: list[str]) -> int:
    hay_tags = " ".join(e.get("tags", [])).lower()
    hay = " ".join([e["path"], e.get("description", ""), e.get("category", ""), e.get("mood", ""), e.get("use", "")]).lower()
    s = 0
    for w in words:
        neg = w.startswith("!")
        w = w.lstrip("!").lower()
        hit = 0
        for v in {w, DE.get(w, w)}:
            hit = max(hit, 3 if v in hay_tags.split() else 2 if v in hay_tags else 1 if v in hay else 0)
        if neg and hit:
            return -1
        if not neg and not hit:
            return -1
        s += hit
    return s


def in_range(v, spec: str | None) -> bool:
    if spec is None:
        return True
    if v is None:
        return False
    lo, _, hi = spec.partition("-")
    lo = float(lo) if lo else float("-inf")
    hi = float(hi) if hi else (lo if _ == "" else float("inf"))
    if _ == "":  # single value: +-5 %
        return abs(v - lo) <= lo * 0.05
    return lo <= v <= hi


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words", nargs="*")
    ap.add_argument("--cat", help="category: whoosh riser impact glitch click pop chime typing paper ui drone foley jingle music")
    ap.add_argument("--music", action="store_true", help="only music tracks")
    ap.add_argument("--min-dur", type=float)
    ap.add_argument("--max-dur", type=float)
    ap.add_argument("--bright", action="store_true", help="brightness hell")
    ap.add_argument("--dark", action="store_true", help="brightness dunkel")
    ap.add_argument("--attack", choices=["fast", "slow"], help="fast: <=15 ms to peak, slow: >60 ms")
    ap.add_argument("--bpm", help="e.g. 120 (+-5 %%) or 90-110")
    ap.add_argument("--mood", help="substring of the mood text (music)")
    ap.add_argument("--license", help="substring, e.g. CC0")
    ap.add_argument("--not", dest="exclude", action="append", default=[], help="exclude word (repeatable)")
    ap.add_argument("-n", type=int, default=12)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()

    files = load()
    if a.stats:
        cats: dict[str, int] = {}
        for e in files:
            cats[e["category"]] = cats.get(e["category"], 0) + 1
        print(json.dumps({"count": len(files), "categories": cats}, ensure_ascii=False, indent=1))
        return
    out = []
    for e in files:
        if a.music and e["category"] != "music":
            continue
        if a.cat and e["category"] != a.cat:
            continue
        d = e.get("duration") or 0
        if a.min_dur is not None and d < a.min_dur or a.max_dur is not None and d > a.max_dur:
            continue
        if a.bright and e.get("brightness") != "hell" or a.dark and e.get("brightness") != "dunkel":
            continue
        att = e.get("attack_ms")
        if a.attack == "fast" and (att is None or att > 15) or a.attack == "slow" and (att is None or att <= 60):
            continue
        if a.bpm and not in_range(e.get("bpm"), a.bpm):
            continue
        if a.mood and a.mood.lower() not in (e.get("mood") or "").lower():
            continue
        if a.license and a.license.lower() not in (e.get("license") or "").lower():
            continue
        terms = a.words + ["!" + x for x in a.exclude]
        s = score(e, terms) if terms else 1
        if s < 0:
            continue
        out.append((s, -(e.get("onset_ms") or 0), e))
    out.sort(key=lambda t: (-t[0], -t[1], t[2]["path"]))
    out = [e for _, _, e in out[: a.n]]
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    if not out:
        print("keine Treffer (Wörter lockern, --stats zeigt Kategorien)")
        return
    for e in out:
        extra = f"  {e['bpm']:.0f} BPM  LRA {e.get('lra')} LU" if e.get("bpm") else ""
        lic = "CC0" if "CC0" in (e.get("license") or "") else (e.get("license") or "?")[:12]
        print(f"sound/{e['path']}\n    {e['category']:<7} {e['duration']:>6.2f}s  {e.get('lufs')!s:>6} LUFS  TP {e.get('true_peak')!s:>5}"
              + ("" if e["category"] == "music" else f"  Angriff {e.get('attack_ms')!s:>4} ms  Spitze @{e.get('peak_ms')} ms")
              + f"  {e.get('brightness')}  {lic}{extra}\n"
              f"    {e.get('description', '')}")


if __name__ == "__main__":
    main()
