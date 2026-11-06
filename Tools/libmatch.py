#!/usr/bin/env python3
"""
libmatch.py - find the static library functions (CRT, ...) inside zoo.exe by comparing every function
of every member object of a .lib against the inventory, with the same BBT-aware comparison as compare.py.

Usage:  python libmatch.py Original/zoo.exe Tools/lib/LIBC_cd.LIB [more.lib] --out Notes/libmatch.csv

Candidates are found by the masked first bytes (relocated fields ignored); each candidate is then
compared in full. Output columns: va, name, lib, member, status.
"""
import argparse, csv, os, struct, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare
from compare import PE, Disasm, OrigCode, Obj, compare_function, Mismatch

def members(path):
    d = open(path, "rb").read()
    assert d[:8] == b"!<arch>\n", "not a COFF archive"
    pos, longnames = 8, b""
    while pos + 60 <= len(d):
        h = d[pos:pos + 60]; name = h[:16].decode("latin1").strip(); size = int(h[48:58])
        body = d[pos + 60:pos + 60 + size]
        if name == "//":
            longnames = body
        elif name.startswith("/") and name[1:].isdigit():
            o = int(name[1:]); yield longnames[o:longnames.index(b"\0", o) if b"\0" in longnames[o:] else None].decode("latin1").rstrip("/\n"), body
        elif name != "/":
            yield name.rstrip("/"), body
        pos += 60 + size + (size & 1)

class MemObj(Obj):
    def __init__(self, data, name):
        import tempfile
        self.tmp = tempfile.NamedTemporaryFile(suffix=".obj", delete=False)
        self.tmp.write(data); self.tmp.close()
        super().__init__(self.tmp.name); self.member = name
        os.unlink(self.tmp.name)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe"); ap.add_argument("libs", nargs="+")
    ap.add_argument("--inventory", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Notes", "inventory.csv"))
    ap.add_argument("--out", required=True); ap.add_argument("--prefix", type=int, default=12)
    a = ap.parse_args()
    pe = PE(a.exe); dis = Disasm(); orig = OrigCode(pe, dis)
    inv = {int(r["va"], 16): int(r["size"]) for r in csv.DictReader(open(a.inventory))}
    claimed = set()                       # already matched elsewhere: zoo.map and Notes/instances_*.csv
    notes = os.path.dirname(a.inventory)
    for ln in open(os.path.join(notes, "zoo.map"), errors="replace"):
        ln = ln.split("#", 1)[0]
        if "=" in ln: claimed.add(int(ln.rsplit("=", 1)[1], 0))
    import glob as G
    for f in G.glob(os.path.join(notes, "instances_*.csv")):
        claimed.update(int(r["va"], 16) for r in csv.DictReader(open(f)) if r.get("status") == "MATCH")
    starts = [v for v in inv if v not in claimed]
    rows, seen_va = [], {}
    loaded = []
    for lib in a.libs:                                # load everything first: BBT inlined calls
        for mname, data in members(lib):              # across objects, so callees must be known
            if data[:2] != b"\x4c\x01": continue
            try: obj = MemObj(data, mname)
            except Exception: continue
            compare.register_obj(obj); loaded.append((lib, mname, obj))
    for lib in a.libs:
        n_obj = n_fn = 0
        for lb, mname, obj in loaded:
            if lb != lib: continue
            n_obj += 1
            for k, (sec, val, name) in enumerate(obj.funcs):
                s, st, en = obj.func_bytes(k)
                raw = obj.sections[s]["raw"]; rel = obj.sections[s]["rels"]
                # prefix = leading instructions up to the first branch/call (BBT rewrites those)
                L = 0
                for ad, (ln, t) in sorted(dis.lengths(raw[st:en], st).items()):
                    if compare.classify(ad, raw[ad:ad + ln])[0] != "other" or L + ln > a.prefix: break
                    L += ln
                if L < 2: L = min(2, en - st)
                if en - st < 3: continue
                mask = set()
                for va in rel:
                    if st <= va < st + L + 4: mask.update(range(va - st, va - st + 4))
                pre = raw[st:st + L]
                for v in starts:
                    b = pe.read(v, L)
                    if b is None or any(b[i] != pre[i] for i in range(L) if i not in mask): continue
                    try:
                        compare_function(obj, k, v, orig, dis)
                    except Exception:
                        continue
                    n_fn += 1
                    rows.append((v, name, os.path.basename(lib), mname))
        print(f"{os.path.basename(lib)}: {n_obj} objects, {n_fn} candidate hits")
    # resolve: a library function lives once in the exe. Unique hit -> MATCH. Several hits of a
    # function of 32+ bytes -> identical code under several names/places (memcpy = memmove, template
    # instantiations): MATCH-SHAPE. Small functions with several hits are too generic -> dropped.
    hits = collections.defaultdict(set)
    for v, name, lib, m in rows: hits[(lib, m, name)].add(v)
    names_at = collections.defaultdict(list)
    for (lib, m, name), vs in hits.items():
        if len(vs) == 1: st = "MATCH"
        elif min(inv[v] for v in vs) >= 32: st = "MATCH-SHAPE"
        else: continue
        for v in vs: names_at[v].append((st, name, lib, m))
    out = []
    for v, lst in sorted(names_at.items()):
        st = "MATCH" if any(x[0] == "MATCH" for x in lst) else "MATCH-SHAPE"
        if inv[v] < 8: continue                                  # too generic to trust
        if all(x[1].startswith("_$E") for x in lst): continue    # generic static-init wrappers, not library code
        if len({x[1] for x in lst}) > 1 and inv[v] < 32: continue   # several unrelated names fit
        out.append([f"{v:#x}", " / ".join(sorted({x[1] for x in lst})), lst[0][2], lst[0][3], inv[v], st])
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["va", "name", "lib", "member", "size", "status"]); w.writerows(out)
    c = collections.Counter(r[5] for r in out)
    print(f"{len(out)} functions ({dict(c)}), {sum(r[4] for r in out)} bytes -> {a.out}")

if __name__ == "__main__":
    main()
