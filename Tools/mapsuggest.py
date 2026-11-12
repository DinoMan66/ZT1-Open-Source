#!/usr/bin/env python3
"""
mapsuggest.py - addresses for the references the anti-cheat could not check. Free tool (Tools\\TOOLS.md), both projects.

VERIFIED_PROGRESS.md counts "matched functions with unverified references": a call or a global whose address is
not in the maps yet, so the anti-cheat could not check that ours points to the same place as the original. The
matched functions themselves show where the original points: this tool re-compares them (the same comparison
as the anti-cheat), collects the original's target for every reference whose address is unknown, and proposes map
entries.

    python3 -I Tools/mapsuggest.py                      report: Notes\\map_suggestions.md   (py Tools\\mapsuggest.py on the PC)
    python3 -I Tools/mapsuggest.py --results <dir>      another build (JPOG: a folder with ALL.txt or unbundled files)
    python3 -I Tools/mapsuggest.py --write              also add the CONFIRMED entries to the maps
                                                        (Zoo: Notes\\symbols.map; JPOG: Notes\\<Dll>.map)

Confirmed = at least two different matched functions reference the symbol and all of them point to the same
address. Only then is the entry evidence: from then on the anti-cheat checks every other use of the symbol against
it (a single reference proves nothing - its own check would pass by construction). Single references and symbols
seen at several addresses (template or inline copies) are listed for a look, never written.
Needs capstone or GNU objdump for Zoo, like compare.py.
"""
import os as _os, sys as _sys
# Run as `py Tools\\x.py`, Python puts Tools\\ first on the path, and the project's own Tools\\dis.py then hides the
# standard 'dis' module: capstone (through inspect) fails to load and the tool falls back to objdump. Load the
# standard modules before Tools\\ can shadow them.
_sys.path[:] = [_p for _p in _sys.path if _os.path.abspath(_p or ".") != _os.path.dirname(_os.path.abspath(__file__))]
import inspect, dis  # noqa: E401,F401
try:
    import capstone  # noqa: F401
except Exception:
    pass
import argparse, collections, csv, glob, os, re, struct, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))
SEEN = collections.defaultdict(lambda: collections.defaultdict(set))   # symbol -> target -> {function va}
CURRENT = [None]


def tools():
    import inspect, dis                                  # the standard 'dis' first: Zoo has a Tools\dis.py of its own
    sys.path.insert(0, HERE)
    import compare as C, symcheck as SC
    real = SC.check
    def recording(res, sym, rtype, addend, field_va, orig_field, our_data=None, orig_target=None):
        st, msg = real(res, sym, rtype, addend, field_va, orig_field, our_data, orig_target)
        if st == "unverified" and msg.endswith("address unknown") and CURRENT[0] is not None:
            target = None
            if orig_target is not None and rtype == SC.TYPE_REL32:
                target = orig_target
            elif len(orig_field) == 4:
                v = struct.unpack("<I", orig_field)[0]
                if rtype == SC.TYPE_REL32: target = (field_va + 4 + v) & 0xFFFFFFFF
                elif rtype == SC.TYPE_DIR32: target = (v - addend) & 0xFFFFFFFF
            if target is not None and res.pe.in_image(target):
                SEEN[sym][target].add(CURRENT[0])
        return st, msg
    SC.check = recording
    return C, SC


def read_map(path, base):
    out = []
    if os.path.exists(path):
        for ln in open(path, errors="replace"):
            ln = ln.split("#", 1)[0].strip()
            if "=" in ln:
                k, v = ln.rsplit("=", 1)
                try: v = int(v.strip(), 0)
                except ValueError: continue
                out.append((k.strip(), v if v >= base else v + base))
    return out


def verified(kind=None):
    p = os.path.join(ROOT, "Notes", "verified_functions.csv")
    if not os.path.exists(p): sys.exit("no Notes/verified_functions.csv - run the anti-cheat once first")
    return [r for r in csv.DictReader(open(p, newline="", encoding="utf-8", errors="replace"))
            if r["status"] == "MATCH" and (kind is None or r["kind"] in kind) and r.get("unverified_refs") not in ("", "0")]


# ------------------------------------------------------------------------------------------- Zoo Tycoon
def reference_objects(listname):
    """the built object(s) an instances_*.csv list is checked against - the same table as the anti-cheat's"""
    n = listname[len("instances_"):-len(".csv")]
    fixed = {"registrars": ["reg.reg_all"], "static_init": ["reg.static_shapes"], "locale": ["reg.static_locale"],
             "misc": ["reg.static_misc"], "member": ["reg.static_member"], "actions": ["misc.ztaction"],
             "refdata": ["misc.bfrefdata"], "forwarders": ["snd.dx8sound"], "ownerdtor": ["misc.ownerdtor"],
             "globals": ["reg.static_globals"]}
    if n in fixed: return fixed[n]
    for rx, fmt in ((r"stl_(\w+)$", "stl.stl_{}"), (r"stl(\d+)$", "reg.stl_inst{}"), (r"globals(\d+)$", "reg.static_globals{}")):
        m = re.match(rx, n)
        if m: return [fmt.format(m.group(1))]
    return []


def zoo(resdir):
    C, SC = tools()
    exe = os.path.join(ROOT, "Original", "zoo.exe"); mp = os.path.join(ROOT, "Notes", "zoo.map")
    dis = C.Disasm(); pe = C.PE(exe); orig = C.OrigCode(pe, dis)
    C.enable_symcheck(exe, mp)
    chk = C.SYMCHECK
    real_tail = chk.tail
    def tail(obj, sec, oi, g):
        rel = obj.sections[sec]["rels"].get(oi.addr + 1)
        if rel is not None and CURRENT[0] is not None:
            name = obj.syms.get(rel[0], ("?",))[0]
            if chk.res.address(name) is None: SEEN[name][g].add(CURRENT[0])
        return real_tail(obj, sec, oi, g)
    chk.tail = tail
    objs = {}
    for p in sorted(glob.glob(os.path.join(resdir, "*.obj"))) + glob.glob(os.path.join(HERE, "lib", "*.obj")):
        if ".Var" in os.path.basename(p) or os.path.basename(p).startswith("zzperm."): continue
        try: objs[os.path.basename(p)] = C.Obj(p)
        except Exception: pass
    for o in objs.values(): C.register_obj(o)
    funcs = [(o, k, name) for o in objs.values() for k, (sec, val, name) in enumerate(o.funcs)]
    by_name = collections.defaultdict(list)
    for f in funcs: by_name[f[2]].append(f)
    refs_of = {}
    def refs(f):
        if id(f) not in refs_of:
            o, k, _ = f; sec = o.funcs[k][0]; _, s, e = o.func_bytes(k)
            refs_of[id(f)] = {o.syms.get(si, ("",))[0] for a, (si, t) in o.sections[sec]["rels"].items() if s <= a < e}
        return refs_of[id(f)]
    rows = verified({"function", "copy"}); done = 0
    for r in rows:
        va = int(r["va"], 16)
        if r["kind"] == "function":
            cand = [f for f in by_name.get(r["name"], []) if os.path.basename(f[0].path) == r["source"]] or by_name.get(r["name"], [])
        else:
            key = r["name"]
            ref = reference_objects(r["source"])
            pool = [f for f in funcs if any(os.path.basename(f[0].path).startswith((x + ".", x + "_")) for x in ref)] or funcs
            if key.startswith("@self:"):
                cand = [f for f in pool if f[2] == key[6:]]
            else:
                hit = [f for f in pool if any(key in x for x in refs(f))]   # part of a symbol, as the anti-cheat does
                cand = ([f for f in hit if f[2].startswith("_$E")] + [f for f in hit if not f[2].startswith("_$E")])[:60]
        for o, k, name in cand:
            CURRENT[0] = va
            before = {s: {t: set(v) for t, v in d.items()} for s, d in SEEN.items()}
            try:
                C.compare_function(o, k, va, orig, dis); done += 1; break
            except C.Mismatch:
                SEEN.clear(); SEEN.update({s: collections.defaultdict(set, d) for s, d in before.items()})  # drop a failed try
        CURRENT[0] = None
    return pe.base, done, len(rows), None


# ------------------------------------------------------------------------------------------- JPOG
def jpog(resdir):
    C, SC = tools()
    tmp = None
    allp = os.path.join(resdir, "ALL.txt")
    if os.path.exists(allp) and not glob.glob(os.path.join(resdir, "*.rel")):
        tmp = tempfile.mkdtemp(prefix="mapsuggest_")
        cur, buf = None, []
        def flush():
            if cur and cur.endswith(".rel"):
                open(os.path.join(tmp, cur), "w", encoding="latin1", newline="").write("".join(buf))
        for ln in open(allp, encoding="latin1", newline=""):
            if ln.startswith("##FILE "):
                flush(); cur, buf = ln[7:].strip(), []
            else:
                buf.append(ln)
        flush(); resdir = tmp
    originals = {}
    for p in glob.glob(os.path.join(ROOT, "Original", "**", "*.dll"), recursive=True) + glob.glob(os.path.join(ROOT, "Original", "*.exe")):
        b = os.path.basename(p).replace("_inst", "").replace(".dll", "").replace(".exe", "")
        if b not in originals or "_inst" in p: originals[b] = p
    rows = verified({"function"}); done = 0; bases = {}
    by_dll = collections.defaultdict(list)
    for r in rows: by_dll[r["source"].split("/")[0]].append(r)
    relcache = {}
    for dll, lst in sorted(by_dll.items()):
        if dll not in originals: continue
        spe = SC.PEInfo(originals[dll]); bases[dll] = spe.base
        pats = [(k, v) for k, v in read_map(os.path.join(ROOT, "Notes", dll + ".map"), spe.base)]
        res = SC.Resolver(spe, pats)
        for r in lst:
            stem = os.path.basename(r["source"])[:-4]                       # TApplication.TApplication
            rp = os.path.join(resdir, stem + ".rel")
            if not os.path.exists(rp): continue
            if rp not in relcache: relcache[rp] = SC.jpog_relocs(rp)
            relocs = relcache[rp].get(r["name"])
            if not relocs: continue
            CURRENT[0] = (dll, int(r["va"], 16))
            SC.jpog_check_function(res, int(r["va"], 16), relocs); done += 1
            CURRENT[0] = None
    # remember which DLL each symbol was seen in, for the map file
    return bases, done, len(rows), None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", help="build folder (default Results)")
    ap.add_argument("--write", action="store_true", help="add the confirmed entries to the maps")
    a = ap.parse_args()
    resdir = a.results or os.path.join(ROOT, "Results")
    if ZOO:
        base, done, total, _ = zoo(resdir)
    else:
        bases, done, total, _ = jpog(resdir)
    confirmed, single, several = [], [], []
    for sym, targets in sorted(SEEN.items()):
        if len(targets) > 1:
            several.append((sym, targets)); continue
        (target, users), = targets.items()
        (confirmed if len(users) >= 2 else single).append((sym, target, users))
    def where(users):
        if ZOO: return ", ".join(f"{u:#x}" for u in sorted(users)[:4]) + (" ..." if len(users) > 4 else "")
        return ", ".join(f"{d} {v:#x}" for d, v in sorted(users)[:3]) + (" ..." if len(users) > 3 else "")
    def entry(sym, target, users):
        if ZOO:
            return "Notes\\symbols.map", f"{sym} = {target:#x}"
        dll = sorted(users)[0][0]
        return f"Notes\\{dll}.map", f"{sym} = {target - bases[dll]:#x}"
    L = ["# Map suggestions", "",
         f"Generated by Tools/mapsuggest.py from {done} re-compared matched functions (of {total} with unverified references).",
         "An entry is CONFIRMED when two or more matched functions reference the symbol and all point to the same",
         "address; only those may go into the maps (`--write`). The anti-cheat then checks every other use against it.", "",
         f"## Confirmed ({len(confirmed)})", ""]
    if confirmed:
        L += ["| Map | Entry | Referenced by |", "|---|---|---|"]
        L += [f"| {entry(s, t, u)[0]} | `{entry(s, t, u)[1]}` | {len(u)}: {where(u)} |" for s, t, u in confirmed]
    L += ["", f"## One reference only ({len(single)}) - not evidence on its own", ""]
    if single:
        L += ["| Entry | Referenced by |", "|---|---|"] + [f"| `{entry(s, t, u)[1]}` | {where(u)} |" for s, t, u in single[:300]]
    L += ["", f"## Several addresses ({len(several)}) - copies (templates, inline statics): record as instances, not in a map", ""]
    for s, ts in several[:100]:
        L.append(f"- `{s}`: " + ", ".join(f"{t:#x} ({len(u)})" for t, u in sorted(ts.items())))
    out = os.path.join(ROOT, "Notes", "map_suggestions.md")
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"{done} matched functions re-compared; {len(confirmed)} confirmed entries, {len(single)} single references, "
          f"{len(several)} symbols at several addresses -> Notes\\map_suggestions.md")
    if a.write and confirmed:
        per = collections.defaultdict(list)
        for s, t, u in confirmed:
            f, line = entry(s, t, u); per[f].append(line)
        for f, lines in per.items():
            p = os.path.join(ROOT, f.replace("\\", os.sep))
            existing = open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""
            new = [l for l in lines if l.split(" = ")[0] + " =" not in existing]
            if not new: continue
            with open(p, "a", encoding="utf-8", newline="\n") as fh:
                if existing and not existing.endswith("\n"): fh.write("\n")
                fh.write("# ---- mapsuggest.py: confirmed by two or more matched functions each\n" + "\n".join(new) + "\n")
            print(f"  {len(new)} entries added to {f}")


if __name__ == "__main__":
    main()
