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

POP_FUNC_HEAD = "void arm_pop(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint32_t iw)\n{"
POP_FUNC_NULL = "void arm_pop(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint32_t iw)\n{\n\treturn;"

PUSH_FUNC_HEAD = "void arm_push(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint16_t regs)\n{"
PUSH_FUNC_NULL = "void arm_push(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint16_t regs)\n{\n\treturn;"

if leg == "HEAD":
    # Verbatim pre-fix HEAD
    pass
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
