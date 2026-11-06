# uiscan.py <project root> [target va ...]  (python3 -I Tools/uiscan.py . > list.txt): unmatched functions that call one of the targets (default find 0x40157D)
import sys, os, re, csv
root=sys.argv[1]; sys.path.insert(0, os.path.join(root,"Tools"))
from compare import PE, Disasm, OrigCode
from dis import blocks
targets={int(t,0) for t in sys.argv[2:]} or {0x40157d}
pe=PE(os.path.join(root,"Original","zoo.exe")); orig=OrigCode(pe,Disasm())
have=set()
for l in open(os.path.join(root,"Notes","zoo.map")):
    m=re.search(r"=\s*(0x[0-9a-fA-F]+)",l)
    if m: have.add(int(m.group(1),16))
for f in os.listdir(os.path.join(root,"Notes")):
    if f.startswith(("instances_","libmatch","importthunks","attempts")) and f.endswith(".csv"):
        for r in csv.reader(open(os.path.join(root,"Notes",f))):
            if r and r[0].startswith("0x") and (f!="attempts.csv" or "MATCH" in ",".join(r)): have.add(int(r[0],16))
failed=set(int(x,16) for x in open(os.path.join(root,"Notes","generated","shapes_failed.txt")).read().split())
out=[]
for r in csv.DictReader(open(os.path.join(root,"Notes","inventory.csv"))):
    va=int(r["va"],16)
    if va in have or va in failed: continue
    try: seen,_=blocks(orig,va)
    except Exception: continue
    n=sum(1 for i in seen.values() if i.kind=="call" and getattr(i,"target",None) in targets)
    if n: out.append((int(r["size"]),va,n,r["callers"]))
for s,va,n,c in sorted(out): print(f"{va:#x} size={s} calls={n} callers={c}")
print(len(out),"candidates",file=sys.stderr)
