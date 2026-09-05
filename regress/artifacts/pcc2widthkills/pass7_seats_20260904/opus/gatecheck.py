import re
s = open("/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gate_arm.sh").read()
m = re.search(r'for v in ("live" "devsig" "byte rd".*?); do', s, re.S)
names = re.findall(r'"([^"]*)"', m.group(1))
print("gate names listed:", len(names))
print("names >= 15 chars:", [(n, len(n)) for n in names if len(n) >= 15])
seen = {}
for n in names: seen[n] = seen.get(n,0)+1
print("duplicated gate names:", {k:v for k,v in seen.items() if v>1})
# probe row names
p = open("/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/pcc2_width_probe.py").read()
