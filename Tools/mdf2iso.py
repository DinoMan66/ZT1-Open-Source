#!/usr/bin/env python3
"""
mdf2iso.py - convert a raw Alcohol 120% .mdf (2352- or 2448-byte sectors) into a plain .iso
(2048-byte user data per sector) that VirtualBox can mount.

Usage:  py Tools\\mdf2iso.py "2000-08_X05-86594_X05-86829_vs6sp4\\image\\vs6sp4.mdf" vs6sp4.iso
"""
import os, sys

def main():
    src, dst = sys.argv[1], sys.argv[2]
    size = os.path.getsize(src)
    for ss in (2448, 2352, 2048):
        if size % ss == 0:
            break
    else:
        sys.exit(f"unknown sector size for {size} bytes")
    n = size // ss
    print(f"{src}: {n} sectors of {ss} bytes")
    if ss == 2048:
        sys.exit("already 2048-byte sectors: just rename it to .iso")
    with open(src, "rb") as f, open(dst, "wb") as o:
        for i in range(n):
            s = f.read(ss)
            mode = s[15]
            if mode == 1:
                o.write(s[16:16 + 2048])
            elif mode == 2:
                o.write(s[24:24 + 2048])          # Mode 2 Form 1
            else:
                o.write(b"\0" * 2048)
            if i % 20000 == 0:
                print(f"  {i}/{n}")
    with open(dst, "rb") as f:
        f.seek(16 * 2048 + 1)
        ok = f.read(5) == b"CD001"
    print(f"wrote {dst} ({n * 2048} bytes) - ISO 9660 header {'found' if ok else 'NOT found'}")

if __name__ == "__main__":
    main()
