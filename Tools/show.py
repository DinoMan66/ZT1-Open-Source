#!/usr/bin/env python3
"""
show.py - everything about one function: inventory row, Ghidra's C, and the full disassembly
(cold blocks included).   Usage:  python show.py 0x4ADACF [--asm-only | --c-only]
Run from the project folder (reads Original\\zoo.exe, Notes\\inventory.csv, decompiled\\zoo.exe.c).
"""
import os, re, sys, csv, subprocess
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
va = int(sys.argv[1], 0); opts = sys.argv[2:]
for r in csv.DictReader(open(os.path.join(root, "Notes", "inventory.csv"), encoding="utf-8")):
    if int(r["va"], 16) == va:
        print("inventory:", dict(r)); break
if "--asm-only" not in opts:
    cfile = os.path.join(root, "decompiled", "zoo.exe.c")
    if os.path.exists(cfile):
        txt = open(cfile, encoding="utf-8", errors="replace").read()
        m = re.search(r"\n// ==== 0*%x  .*\n" % va, txt, re.I)
        if m:
            end = txt.find("\n// ==== ", m.end())
            print(txt[m.start():end if end > 0 else None])
        else:
            print(f"(Ghidra has no function at {va:#x} - run Tools\\export_more.bat)")
if "--c-only" not in opts:
    sys.stdout.flush()
    subprocess.run([sys.executable, os.path.join(here, "dis.py"), os.path.join(root, "Original", "zoo.exe"), hex(va)])
