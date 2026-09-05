import re
from collections import Counter
base='/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/'
src = open(base+'gate_arm.sh', encoding='utf-8', errors='replace').read()
m = re.search(r'for v in ("live" "devsig" "byte rd".*?); do\n\s+check "pcc2 width row', src, re.S)
names = re.findall(r'"([^"]*)"', m.group(1))
print("GATE names:", len(names), "unique:", len(set(names)))
print("GATE dupes:", [k for k,v in Counter(names).items() if v>1])
p = open(base+'pcc2_width_probe.py', encoding='utf-8', errors='replace').read()
rn = re.findall(r'^\s*row\("([^"]+)"', p, re.M)
print("PROBE row() literals:", len(rn), "unique:", len(set(rn)))
print("in probe not gate:", sorted(set(rn)-set(names)))
print("in gate not probe:", sorted(set(names)-set(rn)))
print("longest names:", sorted(((len(n),n) for n in rn), reverse=True)[:4])
