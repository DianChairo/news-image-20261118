#!/usr/bin/env python3
"""Copy entry.png to the make.fun output directory (stdlib only).

Writes to $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png when the
variable is unset. Deterministic byte-for-byte copy."""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
