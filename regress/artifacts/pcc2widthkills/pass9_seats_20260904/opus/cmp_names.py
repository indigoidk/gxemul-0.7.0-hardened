import sys, re
base, gate = sys.argv[1], sys.argv[2]
rows = []
for l in open(base, encoding='latin-1'):
    if l.rstrip('\n').endswith(' ok') or l.rstrip('\n').endswith(' FAIL'):
        rows.append(l[:16].rstrip())
g = [l.strip() for l in open(gate, encoding='utf-8') if l.strip()]
print("probe rows:", len(rows), " unique:", len(set(rows)))
print("gate names:", len(g), " unique:", len(set(g)))
print("in probe not gate:", sorted(set(rows) - set(g)))
print("in gate not probe:", sorted(set(g) - set(rows)))
