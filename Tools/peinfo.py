import struct, sys, datetime
d=open(sys.argv[1],'rb').read()
pe=struct.unpack_from('<I',d,0x3c)[0]
mach,nsec,ts=struct.unpack_from('<HHI',d,pe+4)
optsz=struct.unpack_from('<H',d,pe+20)[0]
opt=pe+24
magic,lmaj,lmin=struct.unpack_from('<HBB',d,opt)
ep=struct.unpack_from('<I',d,opt+16)[0]; base=struct.unpack_from('<I',d,opt+28)[0]
osmaj,osmin=struct.unpack_from('<HH',d,opt+40)
print(f"timestamp {datetime.datetime.utcfromtimestamp(ts)}  linker {lmaj}.{lmin}  os {osmaj}.{osmin}  base {base:#x} ep {ep:#x}")
secs=[]
so=opt+optsz
for i in range(nsec):
    n,vs,va,rs,ra=struct.unpack_from('<8sIIII',d,so+40*i)
    secs.append((n.rstrip(b'\0').decode(),va,vs,ra,rs)); print(f"  {n.rstrip(b'\0').decode():8} va {va:#08x} vsz {vs:#08x} raw {rs:#08x}")
def rva2off(r):
    for n,va,vs,ra,rs in secs:
        if va<=r<va+max(vs,rs): return r-va+ra
# rich header
dans=d.find(b'Rich')
if dans>0:
    key=struct.unpack_from('<I',d,dans+4)[0]
    i=dans-4; ents=[]
    while True:
        v=struct.unpack_from('<I',d,i)[0]^key
        if v==0x536e6144: break
        ents.append(v); i-=4
    ents=ents[::-1]
    print("Rich header (prodid, build, count):")
    for j in range(3,len(ents),2) if False else range(0,len(ents),2):
        a,c=ents[j],ents[j+1] if j+1<len(ents) else 0
        if a==0 and c==0: continue
        print(f"  prod {a>>16:3d} build {a&0xffff:5d} count {c}")
# imports
dd=opt+96
imp_rva=struct.unpack_from('<I',d,dd+8)[0]
o=rva2off(imp_rva)
print("Imports:")
while True:
    oft,_,_,name,ft=struct.unpack_from('<IIIII',d,o)
    if name==0: break
    no=rva2off(name); dll=d[no:d.index(b'\0',no)].decode()
    t=rva2off(oft or ft); cnt=0; names=[]
    while True:
        e=struct.unpack_from('<I',d,t)[0]
        if e==0: break
        if e&0x80000000: names.append(f"#{e&0xffff}")
        else:
            no=rva2off(e)+2; names.append(d[no:d.index(b'\0',no)].decode())
        t+=4; cnt+=1
    print(f"  {dll} ({cnt})" + ("  "+", ".join(names[:60]) if len(sys.argv)>2 else ""))
    o+=20
