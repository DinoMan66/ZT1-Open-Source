#!/usr/bin/env python3
"""
shapescan.py - find every not-yet-matched function in zoo.exe whose code is one of our compiled
functions (compiler-generated code repeated per translation unit: static initialisers, atexit stubs,
template instantiations). Appends the hits to an instances list that Tools/instances.py re-checks.

Usage:  python shapescan.py Original/zoo.exe <obj> --func '_$E33=locale-ids' [--func ...]
                            --list Notes/instances_static_init.csv [--max-size 400]
--func NAME=SHAPE : a function of <obj> and a label. The list's 'key' column gets a text from that
function's relocations that picks it out again (instances.py tries every function referencing it).
"""
import argparse, csv, glob, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import PE, Disasm, OrigCode, Obj, compare_function, Mismatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def claimed_set():
    c = set()
    for ln in open(os.path.join(ROOT, "Notes", "zoo.map"), errors="replace"):
        ln = ln.split("#", 1)[0]
        if "=" in ln: c.add(int(ln.rsplit("=", 1)[1], 0))
    for f in glob.glob(os.path.join(ROOT, "Notes", "instances_*.csv")) + [os.path.join(ROOT, "Notes", "libmatch.csv")]:
        if os.path.exists(f):
            c.update(int(r["va"], 16) for r in csv.DictReader(open(f)) if r.get("status", "").startswith("MATCH"))
    return c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe"); ap.add_argument("obj")
    ap.add_argument("--func", action="append", default=[]); ap.add_argument("--list", required=True)
    ap.add_argument("--all", metavar="LABEL", help="use every function of obj (label = LABEL:<name>)")
    ap.add_argument("--max-size", type=int, default=400)
    ap.add_argument("--min-size", type=int, default=24, help="with --all: ignore our functions shorter than this (too generic)")
    a = ap.parse_args()
    pe = PE(a.exe); dis = Disasm(); orig = OrigCode(pe, dis); obj = Obj(a.obj)
    USERS = collections.Counter()
    for j, (sc, v, nm) in enumerate(obj.funcs):
        _, s2, e2 = obj.func_bytes(j)
        USERS.update({obj.syms.get(si, ("",))[0] for va, (si, t) in obj.sections[sc]["rels"].items() if s2 <= va < e2})
    shapes = []
    if a.all:
        a.func += [f"{f[2]}={a.all}:{f[2]}" for k, f in enumerate(obj.funcs)
                   if (lambda b: b[2] - b[1])(obj.func_bytes(k)) >= a.min_size]
    for spec in a.func:
        name, label = spec.split("=", 1)
        k = next((i for i, f in enumerate(obj.funcs) if f[2] == name), None)
        if k is None:
            print("not in object:", name); continue
        sec, s, e = obj.func_bytes(k)
        refs = sorted({obj.syms.get(si, ("",))[0] for va, (si, t) in obj.sections[sec]["rels"].items() if s <= va < e})
        # the key: the reloc name that the fewest other functions of obj reference
        key = min(refs, key=lambda r: USERS[r]) if refs else name
        if not refs or USERS[key] > 1:
            key = "@self:" + name            # instances.py: match this function by its own name
        shapes.append((k, label, key))
    claimed = claimed_set()
    inv = [(int(r["va"], 16), int(r["size"])) for r in csv.DictReader(open(os.path.join(ROOT, "Notes", "inventory.csv")))]
    import compare as C
    def prefix(k):
        sec, st, en = obj.func_bytes(k); raw = obj.sections[sec]["raw"]; rel = obj.sections[sec]["rels"]
        L = 0
        for ad, (ln, t) in sorted(dis.lengths(raw[st:en], st).items()):
            if C.classify(ad, raw[ad:ad + ln])[0] != "other" or L + ln > 12: break
            L += ln
        L = max(L, min(2, en - st))
        mask = set()
        for va in rel:
            if st - 3 <= va < st + L: mask.update(range(va - st, va - st + 4))
        return [(i, raw[st + i]) for i in range(L) if i not in mask]
    pref = {k: prefix(k) for k, l, kk in shapes}
    hits = []; tally = collections.Counter()
    for va, size in inv:
        if va in claimed or size > a.max_size: continue
        head = pe.read(va, 16) or b""
        for k, label, key in shapes:
            if any(i >= len(head) or head[i] != b for i, b in pref[k]): continue
            try:
                compare_function(obj, k, va, orig, dis)
            except Exception:
                continue
            hits.append((va, key, label)); tally[label] += 1; break
    rows = list(csv.DictReader(open(a.list))) if os.path.exists(a.list) else []
    fields = list(rows[0].keys()) if rows else ["va", "key", "shape", "status"]
    have = {int(r["va"], 16) for r in rows}
    for va, key, label in hits:
        if va in have: continue
        r = {f: "" for f in fields}; r.update(va=f"{va:#x}", key=key, status="MATCH")
        if "shape" in fields: r["shape"] = label
        rows.append(r)
    rows.sort(key=lambda r: int(r["va"], 16))
    with open(a.list, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"{sum(tally.values())} new matches from {len(tally)} of our functions -> {a.list} ({len(rows)} rows)")
    for label, n in tally.most_common(8):
        print(f"  {n:4d}  {label[:110]}")

if __name__ == "__main__":
    main()
