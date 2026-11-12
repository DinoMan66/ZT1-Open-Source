"""calleescan.py - list unwritten functions whose callees are all known (cheap targets).

A function that only calls functions we already wrote (Notes\\zoo.map) or reference by address
(Notes\\symbols.map, with --symbols) is usually a thin wrapper: `g = true; handler(0);`,
`a(x); b(x); c();` or `control = find...; if (control) control->slot();`. Writing them is cheap
and every new match makes more functions qualify, so run it again after each scored round.

Usage (from the project folder, with Original\\zoo.exe and Notes\\inventory.csv):
    python3 -I Tools/calleescan.py [--min 8] [--max 90] [--blocks 4] [--symbols] [--skip-lib]
Output: one line per function on screen: size, address, the callee names (first three).
It only suggests; whether a function matches is decided by verdict.py and the anti-cheat.
Needs Tools\\dis.py (capstone or objdump).
"""
import argparse
import csv
import re
import subprocess
import sys


def load_map(path, into):
    try:
        lines = open(path, errors="ignore").read().splitlines()
    except OSError:
        return
    for line in lines:
        m = re.match(r"(\S+)\s*=\s*0x([0-9A-Fa-f]+)", line)
        if m:
            into.setdefault(int(m.group(2), 16), m.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=8)
    ap.add_argument("--max", type=int, default=90)
    ap.add_argument("--blocks", type=int, default=4)
    ap.add_argument("--symbols", action="store_true", help="also accept callees only listed in symbols.map")
    ap.add_argument("--skip-lib", action="store_true", help="hide operator new/delete, allocator and ZTAction constructor callers")
    ap.add_argument("--exe", default="Original/zoo.exe")
    args = ap.parse_args()

    written = {}
    load_map("Notes/zoo.map", written)
    known = dict(written)
    if args.symbols:
        load_map("Notes/symbols.map", known)

    cands = []
    for row in csv.reader(open("Notes/inventory.csv")):
        try:
            va, size, blocks = int(row[0], 16), int(row[1]), int(row[2])
        except (ValueError, IndexError):
            continue
        if va in written or not args.min <= size <= args.max or blocks > args.blocks:
            continue
        cands.append((va, size))

    found = []
    for va, size in cands:
        out = subprocess.run([sys.executable, "-I", "Tools/dis.py", args.exe, hex(va)],
                             capture_output=True, text=True).stdout
        body = out.split("---- block")[0]
        calls = [int(c, 16) for c in re.findall(r"call\s+0x([0-9a-f]+)", body)]
        if not calls or not all(c in known for c in calls):
            continue
        names = [known[c] for c in calls]
        if args.skip_lib and any(n.startswith(("??2@", "??3@", "?allocate@", "?deallocate@", "??0ZTAction")) for n in names):
            continue
        found.append((size, hex(va), [n[:40] for n in names[:3]]))
    for item in sorted(found):
        print(item)


if __name__ == "__main__":
    main()
