import re, sys
from collections import Counter
src = open('gate_arm.sh', encoding='utf-8', errors='replace').read()
lines = src.split('\n')
cand = None
for i,l in enumerate(lines):
    if l.strip().startswith('for v in ') and i+1 < len(lines) and 'PCC2LOG' in lines[i+1]:
        cand = (i+1, l)
print("gate for-line at line", cand[0])
names = re.findall(r'"([^"]*)"', cand[1])
print("names in list:", len(names))
c = Counter(names)
dups = {k:v for k,v in c.items() if v>1}
print("DUPLICATES:", dups)
print("unique:", len(c))
m = max(len(n) for n in names)
print("max name len:", m, [n for n in names if len(n)==m])
open(sys.argv[1],'w').write('\n'.join(sorted(set(names))))
