#!/usr/bin/env python3
"""
mutate_armbdt.py -- Mutator for armbdt kill table.
Usage: mutate_armbdt.py <leg> <tgt_file> <baseline_file> <head_file>
"""

import sys, os, shutil

if len(sys.argv) < 5:
    print(f"Usage: {sys.argv[0]} <leg> <tgt_file> <baseline_file> <head_file>")
    sys.exit(1)

leg = sys.argv[1]
tgt = sys.argv[2]
baseline = sys.argv[3]
headfile = sys.argv[4]

with open(headfile, "r") as f:
    content = f.read()

# Target patterns in cpu_arm_instr.c:
POP_RW_OLD = """\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr, data,
\t\t\t    sizeof(data), MEM_READ, CACHE_DATA)) {"""

POP_RW_NEW = """\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr & ~3, data,
\t\t\t    sizeof(data), MEM_READ, CACHE_DATA)) {"""

PUSH_RW_OLD = """\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr, data,
\t\t\t    sizeof(data), MEM_WRITE, CACHE_DATA)) {"""

PUSH_RW_NEW = """\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr & ~3, data,
\t\t\t    sizeof(data), MEM_WRITE, CACHE_DATA)) {"""

POP_ENTRY_OLD = "\tuint32_t addr = *np;"
POP_ENTRY_MUT = "\tuint32_t addr = *np & ~3;"

PUSH_ENTRY_OLD = "\tuint32_t value, addr = *np;"
PUSH_ENTRY_MUT = "\tuint32_t value, addr = *np & ~3;"

#  M_MASK1 -- the clause-(d) mutant: the fix PRESENT, its repair WEAKENED.
#  0xfffffffc -> 0xfffffffe, i.e. the carrier's own #461 `m_align1' shape
#  (a mask narrowed & 3 -> & 1).  Fable ruled that #524 owes this, and that
#  grok mis-graded the round as L3 when the fix IS the mask.
#
#  PREDICTED 25/25 -- every unaligned base the probe drives is +1, and
#  x+1 & ~1 == x+1 & ~3 -- but a prediction is not a measurement, and this
#  project's rule is that "it would sweep the table" must be MEASURED.
#  Built from the FIXED text, not the baseline: it weakens a repair that is
#  present, which is what makes it clause (d) rather than clause (b).
POP_MASK1_MUT  = POP_RW_NEW.replace('addr & ~3', 'addr & ~1')
PUSH_MASK1_MUT = PUSH_RW_NEW.replace('addr & ~3', 'addr & ~1')

POP_FUNC_HEAD = "void arm_pop(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint32_t iw)\n{"
POP_FUNC_NULL = "void arm_pop(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint32_t iw)\n{\n\treturn;"

PUSH_FUNC_HEAD = "void arm_push(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint16_t regs)\n{"
PUSH_FUNC_NULL = "void arm_push(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint16_t regs)\n{\n\treturn;"

if leg == "HEAD":
    #  *** THE PRESENCE PIN THE FIRST DRIVER LACKED.  Every MUTANT leg was
    #  protected by its find-text -- a not-found exits 1, so each find-text
    #  doubles as a pin on the feature it edits.  The BASELINE leg asserted
    #  NOTHING, so it would silently measure a post-fix file and label the
    #  score HEAD.  The one leg without a pin is the one that would lie.
    #  Counting rather than merely finding also catches a file where ONE
    #  site was repaired and the other was not. ***
    n = content.count(POP_RW_OLD) + content.count(PUSH_RW_OLD)
    if n != 2:
        print("ERROR: HEAD leg expected 2 unmasked call sites, found %d -- "
              "the baseline is not the pre-fix text" % n)
        sys.exit(1)
elif leg == "BASE":
    if POP_RW_OLD not in content or PUSH_RW_OLD not in content:
        print("ERROR: call sites not found for BASE")
        sys.exit(1)
    content = content.replace(POP_RW_OLD, POP_RW_NEW, 1)
    content = content.replace(PUSH_RW_OLD, PUSH_RW_NEW, 1)
elif leg == "M_ENTRY":
    if POP_ENTRY_OLD not in content or PUSH_ENTRY_OLD not in content:
        print("ERROR: entry sites not found for M_ENTRY")
        sys.exit(1)
    content = content.replace(POP_ENTRY_OLD, POP_ENTRY_MUT, 1)
    content = content.replace(PUSH_ENTRY_OLD, PUSH_ENTRY_MUT, 1)
elif leg == "M_POP_ONLY":
    if POP_RW_OLD not in content:
        print("ERROR: pop call site not found for M_POP_ONLY")
        sys.exit(1)
    content = content.replace(POP_RW_OLD, POP_RW_NEW, 1)
elif leg == "M_PUSH_ONLY":
    if PUSH_RW_OLD not in content:
        print("ERROR: push call site not found for M_PUSH_ONLY")
        sys.exit(1)
    content = content.replace(PUSH_RW_OLD, PUSH_RW_NEW, 1)
elif leg == "M_MASK1":
    content = content.replace(POP_RW_OLD, POP_RW_NEW, 1)
    content = content.replace(PUSH_RW_OLD, PUSH_RW_NEW, 1)
    if POP_RW_NEW not in content or PUSH_RW_NEW not in content:
        print("ERROR: fixed call sites not found for M_MASK1")
        sys.exit(1)
    content = content.replace(POP_RW_NEW, POP_MASK1_MUT, 1)
    content = content.replace(PUSH_RW_NEW, PUSH_MASK1_MUT, 1)
elif leg == "M_NULL_MEDIUM":
    if POP_FUNC_HEAD not in content or PUSH_FUNC_HEAD not in content:
        print("ERROR: func heads not found for M_NULL_MEDIUM")
        sys.exit(1)
    content = content.replace(POP_FUNC_HEAD, POP_FUNC_NULL, 1)
    content = content.replace(PUSH_FUNC_HEAD, PUSH_FUNC_NULL, 1)
else:
    print(f"ERROR: unknown leg {leg}")
    sys.exit(1)

with open(tgt, "w") as f:
    f.write(content)

print(f"Mutator applied leg {leg} successfully")
