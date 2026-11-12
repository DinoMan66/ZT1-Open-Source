"""qprio.py <weights.txt> [ids...] - per-block priority contributions logged by autoprio.cdb (Q lines).
Uses the first R section that has Q lines (round 1 of the function). Prints, per id, the final sum and each
block's contribution (k=1/2 referenced: +P*b, k=3 live unreferenced: -P)."""
import sys,re,collections
f=sys.argv[1]; want=[int(x) for x in sys.argv[2:]]
secs=[]; cur=None; G={}
for l in open(f,errors='replace'):
    if l.startswith('R'): cur=[]; secs.append(cur); continue
    m=re.match(r'Q k=(\d) id=(\d+) P=(-?\d+) b=(-?\d+) pri=(-?\d+) blk=(\w+) line=(\d+)',l)
    if m and cur is not None: cur.append(tuple(int(m.group(i)) if i!=6 else m.group(6) for i in range(1,8)))
    m=re.match(r'G id=(\d+) pri=(-?\d+) reg=(\d+).*?("[^"]*"|\(temp\))',l)
    if m and int(m.group(1)) not in G: G[int(m.group(1))]=(int(m.group(2)),int(m.group(3)),m.group(4))
secs=[s for s in secs if s]
print('sections with Q lines:',len(secs),[len(s) for s in secs])
s=secs[0]
tot=collections.Counter(); per=collections.defaultdict(list)
for k,i,P,b,pri,blk,line in s:
    d=P*b if k<3 else -P
    tot[i]+=d; per[i].append((line,blk,k,P,b,d))
ids=want or sorted(tot,key=lambda i:-tot[i])
for i in ids:
    g=G.get(i,('?','?','?'))
    print('id %d sum=%d G=%s'%(i,tot[i],g))
    if want:
        for line,blk,k,P,b,d in per[i]: print('   line %4d blk %s k=%d P=%3d b=%d -> %+d'%(line,blk,k,P,b,d))
