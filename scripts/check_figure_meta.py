#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse
from PIL import Image

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path, required=True, help="Caminho do PNG a inspecionar")
    args = ap.parse_args()
    p = args.path
    im = Image.open(p)
    print({
        "path": str(p),
        "size_px": im.size,
        "dpi": im.info.get("dpi", None),
        "mode": im.mode,
        "format": im.format,
    })

if __name__ == "__main__":
    main()
