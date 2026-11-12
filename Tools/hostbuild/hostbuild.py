#!/usr/bin/env python3
"""
hostbuild.py - compile on the PC itself, without the VM round trip. Free tool (Tools\\TOOLS.md), both projects.

The 1998-2001 compilers run on current Windows, so the fast, repeated builds of the working loop (the background
permuter above all) need not go through the VM. The VM build stays the TRUSTED one: host results go to
Results_host\\, which the anti-cheat never reads, and nothing counts until a normal VM build verifies it.

    py Tools\\hostbuild\\hostbuild.py --setup            write hostbuild.json (in the project folder) and say what to copy
    py Tools\\hostbuild\\hostbuild.py --check gx         build Src\\gx here and compare with the VM's Results\\gx.* -
                                                       run this once per folder before trusting host builds
    py Tools\\hostbuild\\hostbuild.py --check all        the same for every folder of Src, with a summary
    py Tools\\hostbuild\\hostbuild.py gx                 build one folder into Results_host\\  (same file names as the VM)
    py Tools\\hostbuild\\hostbuild.py --watch            serve Tools\\queue\\hostreq_<id>.txt ("<id> <time> <folder>") so a
                                                       Claude session can ask for a host build; DONE in Results_host\\DONE.txt
    py Tools\\permuter\\permute.py <file> <function> --host      the permuter then builds here, in parallel

hostbuild.json (machine-specific, never published - it sits outside Src, Tools and Notes):
    compiler   folder with cl.exe (Zoo: the SP3 compiler, C:\\VC6SP3\\Bin) / icl.exe (JPOG: C:\\ICC501\\bin)
    vc98       ...\\Microsoft Visual Studio\\VC98           (Include, Lib, Bin with dumpbin/link)
    msdev      ...\\Microsoft Visual Studio\\Common\\MSDev98\\Bin   (mspdb60.dll)
    icc        JPOG only: the Intel compiler's root (include, lib)
    jobs       compiles to run at once (default 4)
    path_map   optional: {"C:\\\\stlport": "D:\\\\somewhere\\\\stlport"} when a flags.txt path lives elsewhere on this PC
    env        optional extra environment variables (e.g. the Intel licence variable from the VM's iccvars.bat)
Copy those folders out of the VM (through the shared folder) to the same paths on the PC if you can; the compilers
are Microsoft's / Intel's, so keep them outside the project folder and never publish them.

Flags and layout follow Tools\\build_core.bat: the project's base flags, then Src\\<folder>\\flags.txt and
<file>.cpp.flags; headers from Src\\include. If build_core.bat changes, change BASE_FLAGS here too.
JPOG is experimental here: the Intel compiler may refuse to run outside the VM (licence). --check tells you.
Idea from decompdecomp, which runs these compilers natively.
"""
import argparse, concurrent.futures, glob, json, os, re, shutil, struct, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ZOO = os.path.exists(os.path.join(ROOT, "Original", "zoo.exe"))
CONFIG = os.path.join(ROOT, "hostbuild.json")
OUT = os.path.join(ROOT, "Results_host")
BASE_FLAGS = (["/nologo", "/c", "/W3", "/ML", "/O2", "/D", "WIN32", "/D", "NDEBUG", "/D", "_WINDOWS"] if ZOO else
              ["-Qvc6", "-nologo", "-Gz", "-MD", "-W3", "-vmg", "-vmm", "-Zi", "-O2", "-D", "TOSHI_SKU_WINDOWS", "-D", "WIN32",
               "-D", "_WINDOWS", "-D", "_UNICODE", "-D", "TOSHI_FINAL", "-D", "NDEBUG", "-D", "USER_JPBUILD", "-c"])
EXE = "cl.exe" if ZOO else "icl.exe"
ZOO_COMPID = {0x000B20FF, 0x000A20FF}          # VC6 SP3 (build 8447), C++ and C


def load_config():
    if not os.path.exists(CONFIG):
        sys.exit(f"no {CONFIG} - run: py Tools\\hostbuild\\hostbuild.py --setup")
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    for k in ["compiler", "vc98", "msdev"] + ([] if ZOO else ["icc"]):
        if not cfg.get(k) or not os.path.isdir(cfg[k]):
            sys.exit(f"hostbuild.json: '{k}' is missing or not a folder ({cfg.get(k)!r})")
    if not os.path.isfile(os.path.join(cfg["compiler"], EXE)):
        sys.exit(f"hostbuild.json: no {EXE} in {cfg['compiler']}")
    return cfg


def environment(cfg):
    env = dict(os.environ)
    vc, icc = cfg["vc98"], cfg.get("icc")
    path = [cfg["compiler"]] + ([os.path.join(icc, "bin")] if icc else []) + [os.path.join(vc, "Bin"), cfg["msdev"]]
    inc = ([os.path.join(icc, "include")] if icc else []) + [os.path.join(vc, "ATL", "Include"), os.path.join(vc, "Include"),
                                                               os.path.join(vc, "MFC", "Include")]
    lib = ([os.path.join(icc, "lib")] if icc else []) + [os.path.join(vc, "Lib"), os.path.join(vc, "MFC", "Lib")]
    env["PATH"] = os.pathsep.join(path + [env.get("PATH", "")])
    env["INCLUDE"] = os.pathsep.join(inc)
    env["LIB"] = os.pathsep.join(lib)
    env.update({k: str(v) for k, v in cfg.get("env", {}).items()})
    return env


def read_flags(path, cfg):
    if not os.path.isfile(path):
        return []
    line = open(path, encoding="latin1").read().splitlines()
    text = line[0] if line else ""
    for a, b in cfg.get("path_map", {}).items():
        text = re.sub(re.escape(a), lambda m: b, text, flags=re.I)
    return text.split()


def compile_one(cfg, env, folder_dir, cpp, name, include_dir, outdir):
    """compile one file in its own work folder -> (name, ok, compiler output)"""
    work = tempfile.mkdtemp(prefix="hostbuild_")
    try:
        for h in glob.glob(os.path.join(folder_dir, "*.h")) + glob.glob(os.path.join(folder_dir, "*.inl")):
            shutil.copy2(h, work)
        local = os.path.join(work, os.path.basename(cpp))
        shutil.copy2(cpp, local)
        flags = BASE_FLAGS + read_flags(os.path.join(folder_dir, "flags.txt"), cfg) + read_flags(cpp + ".flags", cfg)
        obj = os.path.join(work, os.path.splitext(os.path.basename(cpp))[0] + ".obj")
        cmd = [os.path.join(cfg["compiler"], EXE)] + flags + ["/I" if ZOO else "-I", include_dir, os.path.basename(cpp)]
        r = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, errors="replace")
        log = f"extra flags: [{' '.join(flags[len(BASE_FLAGS):])}]\n" + (r.stdout or "") + (r.stderr or "")
        open(os.path.join(outdir, name + ".compile.txt"), "w", encoding="utf-8", errors="replace").write(log)
        if not os.path.isfile(obj):
            return name, False, log
        dst = os.path.join(outdir, name + ".obj")
        shutil.copy2(obj, dst)
        dumpbin = os.path.join(cfg["vc98"], "Bin", "dumpbin.exe")
        if not ZOO or cfg.get("dumps"):
            for args, ext in ((["/disasm"], ".txt"), (["/relocations", "/symbols"], ".rel")):
                d = subprocess.run([dumpbin] + args + [os.path.basename(obj)], cwd=work, env=env, capture_output=True,
                                   text=True, errors="replace")
                open(os.path.join(outdir, name + ext), "w", encoding="latin1", errors="replace").write(d.stdout or "")
        return name, True, log
    finally:
        shutil.rmtree(work, ignore_errors=True)


def build(folder, cfg=None, outdir=OUT, only=None, quiet=False):
    """build Src\\<folder> (or the given .cpp paths in it) -> {name: ok}; results as <folder>.<file>.obj/.txt/.rel"""
    cfg = cfg or load_config()
    env = environment(cfg)
    folder_dir = os.path.join(ROOT, "Src", folder)
    files = only or sorted(glob.glob(os.path.join(folder_dir, "*.cpp")) + (glob.glob(os.path.join(folder_dir, "*.c")) if ZOO else []))
    os.makedirs(outdir, exist_ok=True)
    for old in glob.glob(os.path.join(outdir, folder + ".*")):
        try: os.remove(old)
        except OSError: pass
    include_dir = os.path.join(ROOT, "Src", "include")
    res = {}
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, int(cfg.get("jobs", 4)))) as ex:
        jobs = [ex.submit(compile_one, cfg, env, folder_dir, f, f"{folder}.{os.path.splitext(os.path.basename(f))[0]}",
                          include_dir, outdir) for f in files]
        for j in concurrent.futures.as_completed(jobs):
            name, ok, log = j.result()
            res[name] = ok
            if not ok and not quiet:
                print(f"  FAILED {name}: " + " | ".join(l for l in log.splitlines()[1:4]))
    if not quiet:
        print(f"{folder}: {sum(res.values())} of {len(res)} files compiled in {time.time() - t0:.1f} s -> {os.path.relpath(outdir, ROOT)}")
    return res


# ------------------------------------------------------------------------------------------- --check
def coff_code(path):
    """-> (comp.id, {section index: bytes of every code section}) of a COFF object"""
    d = open(path, "rb").read()
    mach, ns, ts, sp, nsym, opt, ch = struct.unpack_from("<HHIIIHH", d, 0)
    code = []
    for i in range(ns):
        h = 20 + opt + 40 * i
        rs, rp = struct.unpack_from("<II", d, h + 16)
        fl = struct.unpack_from("<I", d, h + 36)[0]
        if fl & 0x20 and rp:                           # IMAGE_SCN_CNT_CODE
            code.append(d[rp:rp + rs])
    cid = None
    for i in range(nsym):
        o = sp + 18 * i
        if d[o:o + 8].startswith(b"@comp.id"):
            cid = struct.unpack_from("<I", d, o + 8)[0]
    return cid, code


def strip_dump(text):
    """the disassembly only: dumpbin's banner and its closing Summary (section sizes, e.g. .drectve, which holds
    linker directives that depend on this PC's library settings, not on the code) are left out"""
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.strip() == "Summary":
            lines = lines[:i]; break
    return [l for l in lines if l.strip() and not re.match(r"^(Dump of file|Microsoft|Copyright|File Type)", l.strip())]


def vm_dumps():
    """JPOG: the VM's dumpbin text per file - Results\\<name>.txt, or straight out of Results\\ALL.txt (no unbundling)"""
    out = {}
    allp = os.path.join(ROOT, "Results", "ALL.txt")
    if os.path.isfile(allp):
        cur, buf = None, []
        for ln in open(allp, encoding="latin1", newline=""):
            if ln.startswith("##FILE "):
                if cur: out[cur] = "".join(buf)
                cur, buf = ln[7:].strip(), []
            else:
                buf.append(ln)
        if cur: out[cur] = "".join(buf)
    for p in glob.glob(os.path.join(ROOT, "Results", "*.txt")):
        out.setdefault(os.path.basename(p), None)               # read on demand
    return out


def check(folder):
    cfg = load_config()
    dumps = None if ZOO else vm_dumps()
    res = build(folder, cfg)
    same = diff = missing = 0
    for name, ok in sorted(res.items()):
        if not ok:
            continue
        if ZOO:
            vm = os.path.join(ROOT, "Results", name + ".obj")
            if not os.path.isfile(vm):
                missing += 1; continue
            a, b = coff_code(os.path.join(OUT, name + ".obj")), coff_code(vm)
            if a[0] not in ZOO_COMPID:
                print(f"  {name}: built by compiler id {a[0]:#x}, not VC6 SP3 (0xb20ff) - wrong cl.exe in hostbuild.json")
            equal = a == b
        else:
            if name + ".txt" not in dumps:
                missing += 1; continue
            vm = dumps[name + ".txt"]
            if vm is None:
                vm = open(os.path.join(ROOT, "Results", name + ".txt"), encoding="latin1").read()
            equal = strip_dump(open(os.path.join(OUT, name + ".txt"), encoding="latin1").read()) == strip_dump(vm)
        if equal: same += 1
        else:
            diff += 1; print(f"  DIFFERENT from the VM build: {name}")
    print(f"{folder}: {same} files identical to the VM's build, {diff} different, {missing} not in Results\\ "
          f"(build the folder in the VM first), {sum(1 for v in res.values() if not v)} failed to compile here")
    if diff or not same:
        print("NOT trusted: host builds of this folder do not reproduce the VM. Use the VM for it.")
        return False
    print("OK: this PC reproduces the VM's code for this folder.")
    return True


def setup():
    guess = dict(compiler=r"C:\VC6SP3\Bin" if ZOO else r"C:\ICC501\bin",
                 vc98=r"C:\Program Files\Microsoft Visual Studio\VC98",
                 msdev=r"C:\Program Files\Microsoft Visual Studio\Common\MSDev98\Bin", jobs=4, path_map={}, env={})
    if not ZOO:
        guess["icc"] = r"C:\ICC501"
    if os.path.exists(CONFIG):
        print(f"{CONFIG} exists - edit it by hand")
    else:
        json.dump(guess, open(CONFIG, "w", encoding="utf-8"), indent=2)
        print(f"wrote {CONFIG}")
    print("\nCopy these folders out of the VM to this PC (same paths if possible), then correct hostbuild.json:")
    for k in ["compiler", "vc98", "msdev"] + ([] if ZOO else ["icc"]):
        print(f"  {k:9} {guess[k]}   {'(found)' if os.path.isdir(guess[k]) else '(not on this PC yet)'}")
    if ZOO:
        print("  and C:\\stlport (the flags.txt files point at it), or map it with \"path_map\"")
    print("\nThen:  py Tools\\hostbuild\\hostbuild.py --check <a folder the VM has just built>")


def watch():
    q = os.path.join(ROOT, "Tools", "queue")
    os.makedirs(q, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    print(f"host build watcher: {q}\\hostreq_*.txt  (Ctrl+C stops)")
    cfg = load_config()
    while True:
        for p in sorted(glob.glob(os.path.join(q, "hostreq_*.txt"))):
            time.sleep(1.0)
            req = open(p, errors="replace").read().strip()
            try: os.remove(p)
            except OSError: pass
            w = req.split()
            print(f"request: {req}")
            state = "ERROR no folder named"
            if len(w) >= 3 and re.match(r"^[\w.-]+$", w[2]) and os.path.isdir(os.path.join(ROOT, "Src", w[2])):
                res = build(w[2], cfg)
                state = "OK" if res and all(res.values()) else "FAILED " + ",".join(n for n, ok in res.items() if not ok)[:200]
            open(os.path.join(OUT, "DONE.txt"), "w").write(f"{req} {state}\n")
        time.sleep(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?"); ap.add_argument("--setup", action="store_true")
    ap.add_argument("--check", metavar="FOLDER"); ap.add_argument("--watch", action="store_true")
    a = ap.parse_args()
    if a.setup: setup()
    elif a.check and a.check.lower() == "all":
        folders = sorted(os.path.basename(d) for d in glob.glob(os.path.join(ROOT, "Src", "*"))
                         if os.path.isdir(d) and os.path.basename(d).lower() not in ("include", "zzperm"))
        folders = [f for f in folders if glob.glob(os.path.join(ROOT, "Src", f, "*.cpp")) or glob.glob(os.path.join(ROOT, "Src", f, "*.c"))]
        ok = {}                                      # (folders with no .cpp, e.g. headers only, have nothing to check)
        for f in folders:
            print(f"\n=== {f}"); ok[f] = check(f)
        print("\nSummary: trusted for host builds: " + (", ".join(f for f in folders if ok[f]) or "none"))
        bad = [f for f in folders if not ok[f]]
        if bad: print("NOT trusted (use the VM for these): " + ", ".join(bad))
        sys.exit(0 if not bad else 1)
    elif a.check: sys.exit(0 if check(a.check) else 1)
    elif a.watch: watch()
    elif a.folder:
        res = build(a.folder)
        sys.exit(0 if res and all(res.values()) else 1)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
