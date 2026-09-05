import re
R="/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/"
g=open(R+"gate_arm.sh").read()
blk=re.search(r'for v in "live" "devsig chipid".*?done', g, re.S).group(0)
names=re.findall(r'"([a-z0-9 ]+)"', blk)
names=[n for n in names if n not in ("1",)]
p=open(R+"pcc2_default_probe.py").read()
rows=re.findall(r'^row\("([^"]+)"', p, re.M)
print("gate names:",len(names),"probe rows:",len(rows))
print("gate == probe (as sets):", set(names)==set(rows))
print("gate order == probe order:", names==rows)
print("only in gate:",sorted(set(names)-set(rows)))
print("only in probe:",sorted(set(rows)-set(names)))
print("longest row name:",max((len(r),r) for r in rows))
bad=[r for r in rows if len(r)>14]
print("names over the 14-char gate anchor limit:",bad)
# prefix collisions: does "^<a>  " match <b>'s padded line for a != b?
def line(n): return ("%-16s"%n)
coll=[(a,b) for a in rows for b in rows if a!=b and line(b).startswith(a+"  ")]
print("gate-anchor prefix collisions:",coll)
