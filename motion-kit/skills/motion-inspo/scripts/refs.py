"""Reference library: find launch/motion videos, fetch them locally, cut them into study material.

    python3 scripts/refs.py search <words...> [--n 15]        whatships (~2.500 X launch videos) + flowjam (55 curated)
    python3 scripts/refs.py get <url> [--name slug]            x.com status | whatships page | youtube | vimeo -> refs/clips/
    python3 scripts/refs.py study <slug|file.mp4> [--every 0.5]  frames, sheet with time stamps, cuts, tempo -> refs/study/<slug>/

Clips belong to their makers: private study only, never re-upload, never put them in the repo (refs/clips is gitignored).
Cite the original post. "Take the grammar, never the content."
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

# Clips und Studien landen im aktuellen Projektordner (oder in $MOTION_REFS_ROOT), nie im Plugin-Ordner.
ROOT = Path(os.environ.get("MOTION_REFS_ROOT", Path.cwd())).resolve()
CLIPS = ROOT / "refs" / "clips"
STUDY = ROOT / "refs" / "study"
CACHE = ROOT / "refs" / ".cache"
UA = {"User-Agent": "claude-motion-kit-refs/0.1"}


def fetch(url: str, headers: dict | None = None) -> str:
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def cached(name: str, url: str, max_age_h=24) -> str:
    import time
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / name
    if not p.exists() or time.time() - p.stat().st_mtime > max_age_h * 3600:
        p.write_text(fetch(url))
    return p.read_text()


# ------------------------------------------------------------------ search
def catalog() -> list[dict]:
    items = []
    for it in json.loads(cached("whatships.json", "https://whatships.com/search-index.json")):
        if it.get("kind") == "video":
            items.append({"src": "whatships", "title": it["name"], "meta": it.get("meta", ""),
                          "url": "https://whatships.com" + it["href"], "text": it.get("searchText", "")})
    html = cached("flowjam.html", "https://flowjam.com/library")
    for title, emb in re.findall(r'<h3 class="videotitle">(.*?)</h3>.*?data-lv="([^"]+)"', html, re.S):
        emb = emb.replace("&amp;", "&")
        m = re.search(r"youtube(?:-nocookie)?\.com/embed/([\w-]+)", emb)
        url = f"https://www.youtube.com/watch?v={m.group(1)}" if m else emb.split("?")[0]
        items.append({"src": "flowjam", "title": re.sub("<.*?>", "", title), "meta": "curated launch", "url": url,
                      "text": title.lower()})
    return items


def search(words: list[str], n=15):
    ws = [w.lower() for w in words]
    hits = [it for it in catalog() if all(w in (it["title"] + " " + it["meta"] + " " + it["text"]).lower() for w in ws)]
    for it in hits[:n]:
        print(f"[{it['src']}] {it['title'][:70]} · {it['meta']}\n    {it['url']}")
    print(f"{len(hits)} hits" + (f" (showing {n})" if len(hits) > n else ""))


# ------------------------------------------------------------------ get
def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "clip"


def x_video(status_id: str) -> tuple[str, dict]:
    raw = fetch(f"https://api.fxtwitter.com/2/thread/{status_id}")
    urls = set(re.findall(r'https://video\.twimg\.com/[^"\\]+?\.mp4[^"\\]*', raw))
    if not urls:
        raise SystemExit(f"no video in X post {status_id}")

    def area(u):
        m = re.search(r"/(\d+)x(\d+)/", u)
        return int(m.group(1)) * int(m.group(2)) if m else 0
    best = max(urls, key=area)
    j = json.loads(raw)
    st = j.get("status") or {}
    meta = {"x_post": f"https://x.com/i/status/{status_id}", "author": (st.get("author") or {}).get("screen_name"),
            "text": st.get("text"), "views": st.get("views"), "likes": st.get("likes"), "video_url": best}
    return best, meta


def get(url: str, name: str | None = None) -> Path:
    CLIPS.mkdir(parents=True, exist_ok=True)
    meta: dict = {"source_url": url}
    if "whatships.com/videos/" in url:
        md = fetch(url, {"Accept": "text/markdown"})
        m = re.search(r"Original X post:\s*(https://x\.com/\S+/status/(\d+))", md)
        if not m:
            raise SystemExit("whatships page without original X post link")
        meta["whatships"] = url
        name = name or slugify(url.rstrip("/").rsplit("/", 1)[-1])
        url = m.group(1)
    m = re.search(r"(?:x|twitter)\.com/[^/]+/status/(\d+)", url)
    if m:
        video, xm = x_video(m.group(1))
        meta.update(xm)
        name = name or slugify(f"{xm.get('author') or 'x'}-{m.group(1)[-6:]}")
        out = CLIPS / f"{name}.mp4"
        subprocess.run(["curl", "-sL", "-o", str(out), video], check=True)
    else:
        name = name or slugify(url.rstrip("/").rsplit("/", 1)[-1].replace("watch?v=", ""))
        out = CLIPS / f"{name}.mp4"
        cmd = ["uvx", "yt-dlp", "-f", "bv*[height<=1080]+ba/b[height<=1080]", "--merge-output-format", "mp4",
               "-o", str(out), url]
        if "vimeo" in url:
            cmd[2:2] = ["--referer", "https://flowjam.com/"]
        subprocess.run(cmd, check=True)
    (CLIPS / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print(out)
    return out


# ------------------------------------------------------------------ study
def study(target: str, every=0.5) -> Path:
    clip = Path(target) if target.endswith(".mp4") else CLIPS / f"{target}.mp4"
    slug = clip.stem
    d = STUDY / slug
    (d / "frames").mkdir(parents=True, exist_ok=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clip)],
                               capture_output=True, text=True, check=True).stdout)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf", f"fps={1 / every},scale=960:-2",
                    str(d / "frames" / "f_%04d.jpg")], check=True)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from sheet import sheets
    sheets(str(clip), str(d / "sheet"), every=every)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(clip), "-vf", "select='gt(scene,0.3)',showinfo", "-an", "-f",
                        "null", "-"], capture_output=True, text=True)
    cuts = [round(float(t), 2) for t in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    shots = [round(b - a, 2) for a, b in zip([0.0] + cuts, cuts + [dur])]
    meta = {}
    if (CLIPS / f"{slug}.json").exists():
        meta = json.loads((CLIPS / f"{slug}.json").read_text())
    md = [f"# Studie: {slug}", "", f"Quelle: {meta.get('x_post') or meta.get('source_url') or clip}",
          f"Dauer {dur:.1f} s · {len(cuts)} harte Schnitte · Ø Einstellung {sum(shots) / len(shots):.2f} s",
          f"Schnitte (s): {cuts}", "", "Kontaktbögen: " + ", ".join(sorted(p.name for p in d.glob('sheet_*.jpg'))),
          "", "## Grammatik (ausfüllen, nach Ansehen der Bögen und Einzelbilder)", "",
          "Stil in drei Wörtern benennen (nicht beschreiben):", "",
          "| Zeit | Was passiert (Bild) | Bewegung + Auslöser | Kamera | Übergang (Objekt?) | Typo | Ton |",
          "|---|---|---|---|---|---|---|", "", "Dramaturgie (Versprechen / Fall / Beweis / Auflösung):", "",
          "Was übernehmen wir (Mechanik, nie Inhalt)?", ""]
    (d / "study.md").write_text("\n".join(md) + "\n")
    print(d / "study.md")
    return d


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(1)

    def opt(flag, default):
        if flag in a:
            i = a.index(flag)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return default
    if a[0] == "search":
        n = int(opt("--n", 15))
        search(a[1:], n)
    elif a[0] == "get":
        name = opt("--name", None)
        get(a[1], name)
    elif a[0] == "study":
        every = float(opt("--every", 0.5))
        study(a[1], every)
    else:
        print(__doc__)
        sys.exit(1)
