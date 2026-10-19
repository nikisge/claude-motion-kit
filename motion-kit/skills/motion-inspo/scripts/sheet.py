"""Contact sheets with time stamps (PIL; this ffmpeg build has no drawtext).

    python3 scripts/sheet.py <video> <out_prefix> [--every 1.0] [--from S --to S] [--cols 6] [--w 320]
    -> <out_prefix>_00.jpg, _01.jpg ... (36 frames per sheet)
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONTS = ["/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Helvetica.ttc"]


def _font(size=15):
    for f in FONTS:
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def sheets(video: str, out_prefix: str, every=1.0, t0=0.0, t1: float | None = None, cols=6, w=320, per=36) -> list[Path]:
    with tempfile.TemporaryDirectory() as td:
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(t0)]
        if t1 is not None:
            cmd += ["-to", str(t1)]
        cmd += ["-i", str(video), "-vf", f"fps={1 / every},scale={w}:-2", str(Path(td) / "s_%05d.jpg")]
        subprocess.run(cmd, check=True)
        frames = sorted(Path(td).glob("s_*.jpg"))
        font, out = _font(), []
        for k in range(0, len(frames), per):
            chunk = frames[k:k + per]
            ims = [Image.open(p).convert("RGB") for p in chunk]
            tw, th = ims[0].size
            rows = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * (tw + 4) + 4, rows * (th + 4) + 4), (20, 20, 20))
            d = ImageDraw.Draw(sheet)
            for i, im in enumerate(ims):
                x, y = 4 + (i % cols) * (tw + 4), 4 + (i // cols) * (th + 4)
                sheet.paste(im, (x, y))
                t = t0 + (k + i + 0.5) * every
                label = f"{int(t // 60)}:{t % 60:05.2f}"
                bx = d.textbbox((x + 5, y + 4), label, font=font)
                d.rectangle([bx[0] - 3, bx[1] - 2, bx[2] + 3, bx[3] + 2], fill=(0, 0, 0))
                d.text((x + 5, y + 4), label, fill=(255, 255, 255), font=font)
            p = Path(f"{out_prefix}_{k // per:02d}.jpg")
            p.parent.mkdir(parents=True, exist_ok=True)
            sheet.save(p, quality=85)
            out.append(p)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]

    def opt(flag, default):
        return float(a[a.index(flag) + 1]) if flag in a else default
    to = opt("--to", None)
    for p in sheets(a[0], a[1], opt("--every", 1.0), opt("--from", 0.0), to, int(opt("--cols", 6)), int(opt("--w", 320))):
        print(p)
