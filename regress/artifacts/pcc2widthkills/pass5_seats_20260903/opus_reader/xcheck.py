import re
g = open("regress/gate_arm.sh").read()
blocks = re.findall(r'for v in ((?:"[^"]*"\s*)+); do\n\s*check "pcc2 width row: \$v" "\$\(count "\$PCC2LOG"', g)
print("gate blocks anchored on PCC2LOG:", len(blocks))
gate = re.findall(r'"([^"]*)"', blocks[0])
print("gate names:", len(gate), " unique:", len(set(gate)))
log = open("/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p5_opus/artifacts/probe_BASE.out").read()
emitted = [l[:16].rstrip() for l in log.splitlines() if l.endswith(" ok") or l.endswith(" FAIL")]
emitted = [e for e in emitted if e and e != "row"]
print("probe rows emitted:", len(emitted), " unique:", len(set(emitted)))
print("gate names NOT emitted:", sorted(set(gate) - set(emitted)))
print("emitted but NOT in gate :", sorted(set(emitted) - set(gate)))
for m in re.finditer(r'check "pcc2 width rows (\w+)"\s+"[^"]*"\s+"(\d+)"', g):
    print("gate pin: rows %-8s = %s" % (m.group(1), m.group(2)))
print("max row-name length:", max(len(e) for e in emitted), "(probe asserts <= 15)")
