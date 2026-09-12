#!/usr/bin/env python3
"""opus524 mutator -- clause-(d) candidates for the armbdt detector.
Usage: mutate_opus.py <leg> <tgt_file> <baseline_file>
Every leg is built from the IMMUTABLE baseline 8d372aa text.
Every leg carries a find-text presence pin: a not-found exits 1."""
import sys

leg, tgt, baseline = sys.argv[1], sys.argv[2], sys.argv[3]
content = open(baseline).read()

POP_OLD = ("\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr, data,\n"
           "\t\t\t    sizeof(data), MEM_READ, CACHE_DATA)) {")
POP_NEW = ("\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr & 0xfffffffc, data,\n"
           "\t\t\t    sizeof(data), MEM_READ, CACHE_DATA)) {")
PUSH_OLD = ("\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr, data,\n"
            "\t\t\t    sizeof(data), MEM_WRITE, CACHE_DATA)) {")
PUSH_NEW = ("\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr & 0xfffffffc, data,\n"
            "\t\t\t    sizeof(data), MEM_WRITE, CACHE_DATA)) {")

def pin(n_want):
    n = content.count(POP_OLD) + content.count(PUSH_OLD)
    if n != n_want:
        sys.exit("PIN FAILED: expected %d unmasked sites, found %d" % (n_want, n))

pin(2)
# Apply the shipped fix at both sites first; every mutant below WEAKENS a fix
# that is PRESENT, which is what makes it clause (d) rather than clause (b).
content = content.replace(POP_OLD, POP_NEW, 1)
content = content.replace(PUSH_OLD, PUSH_NEW, 1)
if POP_NEW not in content or PUSH_NEW not in content:
    sys.exit("PIN FAILED: fixed sites absent after applying the fix")

def repl(site_new, expr, which):
    global content
    mut = site_new.replace('addr & 0xfffffffc', expr)
    if site_new not in content:
        sys.exit("PIN FAILED: %s site not found" % which)
    content = content.replace(site_new, mut, 1)

if leg == "BASE":
    pass
elif leg == "M_MASK1":                       # reproduction control, want 29/32
    repl(POP_NEW,  'addr & 0xfffffffe', 'pop')
    repl(PUSH_NEW, 'addr & 0xfffffffe', 'push')
elif leg == "M_MASK15":                      # discrimination control, want <32
    repl(POP_NEW,  'addr & 0xfffffff0', 'pop')
    repl(PUSH_NEW, 'addr & 0xfffffff0', 'push')
elif leg == "M_POPP_NONE":                   # fix ABSENT when p_bit (LDMIB/LDMDB)
    repl(POP_NEW, 'p_bit ? addr : (addr & 0xfffffffc)', 'pop')
elif leg == "M_POPP_WEAK":                   # mask weakened when p_bit
    repl(POP_NEW, 'addr & (p_bit ? 0xfffffffe : 0xfffffffc)', 'pop')
elif leg == "M_POPW_WEAK":                   # mask weakened when w_bit
    repl(POP_NEW, 'addr & (w_bit ? 0xfffffffe : 0xfffffffc)', 'pop')
elif leg == "M_SBIT_NONE":                   # fix ABSENT when s_bit, BOTH sites
    repl(POP_NEW,  's_bit ? addr : (addr & 0xfffffffc)', 'pop')
    repl(PUSH_NEW, 's_bit ? addr : (addr & 0xfffffffc)', 'push')
elif leg == "M_NPMASK":                      # mask the WRONG operand: the base, not the running addr
    repl(POP_NEW, '(*np) & 0xfffffffc', 'pop')
else:
    sys.exit("unknown leg %s" % leg)

open(tgt, "w").write(content)
print("mutator applied leg %s" % leg)
