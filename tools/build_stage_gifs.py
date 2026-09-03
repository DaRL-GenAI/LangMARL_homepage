#!/usr/bin/env python3
"""Render the stage-reveal pipeline animations to WebP (+ GIF fallback).

Each source page (tools/<name>_stages.html) draws four stage columns and reads
?stage=N to decide how many are visible. We screenshot N=1..4 with headless
Chrome and assemble the frames into a looping GIF, matching the cadence of the
reference animation (3s per reveal, 10s on the completed diagram).

Usage:
    python3 tools/build_stage_gifs.py            # serves the repo itself
    python3 tools/build_stage_gifs.py --port 8080  # reuse a running server
"""

import argparse
import functools
import http.server
import os
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]

WIDTH, HEIGHT = 1600, 900
FRAME_MS = [3000, 3000, 3000, 10000]

# Chrome renders the same CSS layout at this device pixel ratio, so the frames
# come out at WIDTH*DPR x HEIGHT*DPR with identical typography — that headroom is
# what keeps the animation sharp on retina displays.
DPR = 2

JOBS = [
    ("tools/langmarl_stages.html", "static/images/langmarl/pipeline_stages"),
    ("tools/maskills_stages.html", "static/images/maskills/pipeline_stages"),
]


def find_chrome():
    for path in CHROME_CANDIDATES:
        if path and os.path.exists(path):
            return path
    sys.exit("Could not find Chrome. Install Google Chrome or pass --chrome.")


def serve(directory):
    """Start a background HTTP server on a free port; return (port, shutdown)."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port, httpd.shutdown


def shoot(chrome, url, out_png):
    subprocess.run(
        [
            chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
            f"--window-size={WIDTH},{HEIGHT}",
            f"--force-device-scale-factor={DPR}",
            "--virtual-time-budget=9000",
            f"--screenshot={out_png}", url,
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if not os.path.exists(out_png):
        raise RuntimeError(f"Chrome produced no screenshot for {url}")


def load_frames(paths, scale=1.0):
    imgs = []
    for png in paths:
        im = Image.open(png).convert("RGB")
        if scale != 1.0:
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        imgs.append(im)
    return imgs


def build_webp(imgs, out_path):
    """Primary format: full 24-bit colour, so antialiased text stays clean."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    imgs[0].save(
        out_path, format="WEBP", save_all=True, append_images=imgs[1:],
        duration=FRAME_MS, loop=0, quality=92, method=6,
    )


def build_gif(imgs, out_path):
    """Fallback format: capped at 256 colours, so halve the resolution and
    dither — a full-size GIF would be large without looking any better."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    half = [im.resize((im.width // 2, im.height // 2), Image.LANCZOS) for im in imgs]
    # One shared palette across frames avoids colour flicker between stages.
    base = half[0].quantize(colors=255, method=Image.MEDIANCUT)
    quant = [im.quantize(palette=base, dither=Image.FLOYDSTEINBERG) for im in half]
    quant[0].save(
        out_path, save_all=True, append_images=quant[1:],
        duration=FRAME_MS, loop=0, optimize=True, disposal=2,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--port", type=int, default=None,
                    help="Reuse a server already serving the repo root.")
    ap.add_argument("--scale", type=float, default=1.0,
                    help="Extra scale applied to the rendered frames (1.0 = 3200x1800).")
    args = ap.parse_args()

    chrome = args.chrome or find_chrome()
    if args.port:
        port, shutdown = args.port, lambda: None
    else:
        port, shutdown = serve(ROOT)

    try:
        with tempfile.TemporaryDirectory() as tmp:
            for src, stem in JOBS:
                paths = []
                for stage in range(1, len(FRAME_MS) + 1):
                    png = os.path.join(tmp, f"{os.path.basename(src)}.{stage}.png")
                    shoot(chrome, f"http://127.0.0.1:{port}/{src}?stage={stage}", png)
                    paths.append(png)

                imgs = load_frames(paths, scale=args.scale)
                print(f"  frames rendered at {imgs[0].width}x{imgs[0].height}")
                for ext, fn in (("webp", build_webp), ("gif", build_gif)):
                    out = os.path.join(ROOT, f"{stem}.{ext}")
                    fn(imgs, out)
                    print(f"{stem}.{ext}  {os.path.getsize(out)/1024:.0f} KB")
    finally:
        shutdown()


if __name__ == "__main__":
    main()
