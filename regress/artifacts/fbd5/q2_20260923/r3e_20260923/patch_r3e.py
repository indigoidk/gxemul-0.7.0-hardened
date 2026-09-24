#!/usr/bin/env python3
"""#545 repair 3e -- 3d's own pass (panel_20260923_202025, q2g/codex_ded, the Opus seat).  No row is added.
Two classes the last two passes each hit are closed in one diff, as the carrier's class-closure rule requires:
  * a claimed-KEPT channel read only at the END of a multi-access row (3c's pass: read nowhere; 3d's pass: a
    toggle on each +0x180 decline cancels across the re-arm row's two batches -- codex) -> X14 now checks every
    field and irq_asserted after EACH decline, read and Clear of its multi-access rows;
  * the handler's use of the caller's buffer beyond `len` (3c's pass: the fetch -- deepseek; 3d's pass: the read
    write-back -- kimi-k3:cloud, and a real ARM narrow load passes data[1]/data[2]/data[4]) -> X6, X9 and X10 now
    check that the bytes above a read's or write's width are untouched.
and two disclosures are widened to their whole classes: the caller context (grok: the calloc'd cpu's byte order
and pc), and which interrupt a Clear drives (codex's dedicated job: a destination keyed on a field bit).
Records: E3's reason, the 0xa5 fill's reason, FS02's condition, the "five checks" count.
usage: patch_r3e.py IN OUT"""
import io, sys

src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()
T = "\t"


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:100])
    s = s.replace(old, new)


# ------------------------------------------------------------------ code
#  C1: the helper
rep("static void x14_line(struct footbridge_data *x, int n)\n",
    "/*  #545 3e: the caller's buffer beyond `len` is not the handler's -- a real ARM narrow load passes data[1],\n"
    "    data[2] or data[4] (cpu_arm_instr_loadstore.c) -- so every row that fills b with 0xa5 can check that a read or\n"
    "    write left the bytes above its width alone (kimi-k3:cloud, 3d's pass: a write-back of 8 bytes passed).  */\n"
    "static int pad_kept(const unsigned char *p, int w)\n"
    "{\n"
    "\tint i;\n"
    "\tfor (i = w; i < 8; i++)\n"
    "\t\tif (p[i] != 0xa5)\n"
    "\t\t\treturn 0;\n"
    "\treturn 1;\n"
    "}\n"
    "static void x14_line(struct footbridge_data *x, int n)\n")
#  C2: X6 -- both directions
rep(T * 7 + "    && (S5[si].wf != MEM_READ || memory_readmax64(cpu, b, W[wi]) == 0);\n",
    T * 7 + "    && (S5[si].wf != MEM_READ || memory_readmax64(cpu, b, W[wi]) == 0) && pad_kept(b, W[wi]);\n")
#  C3: X9 reads
rep(T * 5 + "ok = rv == 1 && fatal_calls == 0 && memory_readmax64(cpu, b, w) == want\n",
    T * 5 + "ok = rv == 1 && fatal_calls == 0 && memory_readmax64(cpu, b, w) == want && pad_kept(b, w)\n")
#  C4: X10 reads
rep(T * 5 + "ok = rv == 1 && fatal_calls == f0 && memory_readmax64(cpu, b, WY[w]) == want && YSAME(st)\n",
    T * 5 + "ok = rv == 1 && fatal_calls == f0 && memory_readmax64(cpu, b, WY[w]) == want && pad_kept(b, WY[w])\n"
    + T * 5 + "    && YSAME(st)\n")
#  C5: X14 -- a snapshot of the five fields, checked after EACH decline
rep(T * 2 + "int i, k, tk, a0, d0, f0, rv, ok;\n" + T * 2 + "struct footbridge_data *x;\n"
    + "#define ZZERO() ",
    T * 2 + "int i, k, tk, a0, d0, f0, rv, ok;\n" + T * 2 + "uint32_t zs[5];\n" + T * 2 + "struct footbridge_data *x;\n"
    + "/*  3e: a KEPT field is checked after EACH access of a multi-access row, never only at its end -- a toggle on\n"
    + "    every +0x180 decline cancelled across the re-arm row's two batches and passed (codex, 3d's pass).  */\n"
    + "#define ZSNAP() do { zs[0] = x->irq_status; zs[1] = x->irq_enable; zs[2] = x->fiq_status; \\\n"
    + T * 2 + "zs[3] = x->fiq_enable; zs[4] = (uint32_t) x->irq_asserted; } while (0)\n"
    + "#define ZKEPT() (x->irq_status == zs[0] && x->irq_enable == zs[1] && x->fiq_status == zs[2] \\\n"
    + T * 2 + "&& x->fiq_enable == zs[3] && (uint32_t) x->irq_asserted == zs[4])\n"
    + "#define ZZERO() ")
rep("#define ZDECLINE() do { for (i = 0; i < 5; i++) { memset(b, 0xa5, sizeof(b)); \\\n",
    "#define ZDECLINE() do { ZSNAP(); for (i = 0; i < 5; i++) { memset(b, 0xa5, sizeof(b)); \\\n")
rep(T * 2 + "ok = ok && rv == 1 && (DD[i].wf == MEM_WRITE || memory_readmax64(cpu, b, 4) == 0); } } while (0)\n",
    T * 2 + "ok = ok && rv == 1 && (DD[i].wf == MEM_WRITE || memory_readmax64(cpu, b, 4) == 0) && ZKEPT(); } } \\\n"
    + T * 2 + "while (0)\n")
#  C6: the re-arm row -- each legal read and the Clear keep the five fields too
rep(T * 3 + "rv = dev_footbridge_access(cpu, NULL, RA[i].addr, b, 4, MEM_READ, x);\n"
    + T * 3 + "ok = ok && rv == 1 && memory_readmax64(cpu, b, 4) == RA[i].want;\n"
    + T * 2 + "}\n" + T * 2 + "ZCLR(0x400);\n" + T * 2 + "ok = ok && rv == 1;\n",
    T * 3 + "rv = dev_footbridge_access(cpu, NULL, RA[i].addr, b, 4, MEM_READ, x);\n"
    + T * 3 + "ok = ok && rv == 1 && memory_readmax64(cpu, b, 4) == RA[i].want && ZKEPT();\n"
    + T * 2 + "}\n" + T * 2 + "ZCLR(0x400);\n" + T * 2 + "ok = ok && rv == 1 && ZKEPT();     /*  0x10 & ~0x400: nothing changes  */\n")
rep("#undef ZDECLINE\n", "#undef ZDECLINE\n#undef ZKEPT\n#undef ZSNAP\n")

# ------------------------------------------------------------------ records
rep(T + " *  four fields, the interrupt calls and, for a read, the read data over the width, except X7 (the return\n"
    + T + " *  value and the announce count only) and X14's rows (the channels in each row's name and header):\n",
    T + " *  four fields, the interrupt calls and, for a read, the read data over the width -- and in X6, X9 and X10\n"
    + T + " *  the bytes above the width untouched (3e) -- except X7 (the return value and the announce count only) and\n"
    + T + " *  X14's rows (the channels in each row's name and header):\n")
rep(T + " *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff) and the buffer's bytes above the width not zero,\n",
    T + " *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff) and the buffer's bytes above the width poisoned,\n")
rep(T + " *    kept where a Clear leaves a line pending), and the five declines, each with the interrupt output (X14);\n",
    T + " *    kept where a Clear leaves a line pending), and the five declines, each with the interrupt output and\n"
    + T + " *    every field and irq_asserted checked after EACH decline (X14);\n")
rep(T + " *    their values and a Clear, five declines again: 5 announces, one CPU assert, the fields and irq_asserted\n"
    + T + " *    kept (X14).\n",
    T + " *    their values and a Clear, five declines again: 5 announces, one CPU assert, and the fields and\n"
    + T + " *    irq_asserted kept -- checked after EACH of its access (3e) (X14).\n")
rep(T + " *    WHICH interrupt a Clear write drives, below len 4: X14 counts the CPU line apart at len 4 only, and X9-X13\n"
    + T + " *    count calls on the shared pair, so a destination conditioned on the width passes (codex, repair 3's pass);\n",
    T + " *    WHICH interrupt a Clear write drives, outside X14's own instances: X14 counts the CPU line apart only\n"
    + T + " *    there (len 4; fiq_enable 0 or 0xc0), and X9-X13 count calls on one shared pair, so a destination keyed on\n"
    + T + " *    the width (codex, repair 3's pass) or on a field X14's instances do not vary (codex, 3d's pass:\n"
    + T + " *    `fiq_enable & 1`) passes;\n")
rep(T + " *    the CALLER context: every row calls the handler with mem NULL on a machine of type MACHINE_NONE, so a\n"
    + T + " *    condition on `mem` or on the machine type in any test passes every row (the Opus seat, 3c's pass: MC01-\n"
    + T + " *    MC05 and MC07 green on 864; a cats or netwinder caller with a real mem reddens them in its scratch,\n"
    + T + " *    q2f/opus/SUMMARY.txt);\n",
    T + " *    the CALLER context, as a class: every row passes the same calloc'd cpu -- byte order undefined, pc 0, its\n"
    + T + " *    machine of type MACHINE_NONE -- and mem NULL, so a condition on ANY caller state in any test passes\n"
    + T + " *    every row (the Opus seat, 3c's pass: `mem` and the machine type, MC01-MC05 and MC07; grok, 3d's pass:\n"
    + T + " *    `cpu->byte_order != EMUL_LITTLE_ENDIAN`, `!cpu->pc`; a cats or netwinder caller with a real mem\n"
    + T + " *    reddens the first six in the Opus seat's scratch, q2f/opus/SUMMARY.txt);\n")
rep(T + " *    (`fbirqstuck`) is invisible here, and so is a Clear that clears irq_asserted (the Opus seat's FS02);\n",
    T + " *    (`fbirqstuck`) is invisible here, and so is a Clear that clears irq_asserted when it leaves nothing pending\n"
    + T + " *    and enabled (the Opus seat's FS02): only the Clear 0x10 row reaches that state, and it leaves irq_asserted\n"
    + T + " *    unread on purpose;\n")
rep("\t         (x 4 states): it returns 1, clears (ne = ie & ~idata, idata the low bytes the width carries -- 3d: the\n"
    "\t         buffer's bytes above the width hold 0xa5, as a real store's are not zero, so a fetch past len clears\n"
    "\t         more; deepseek's `memory_readmax64(cpu, data, 4)` passed every row while they were 0), drives the\n",
    "\t         (x 4 states): it returns 1, clears (ne = ie & ~idata, idata the low bytes the width carries -- 3d: the\n"
    "\t         buffer's bytes above the width hold 0xa5 POISON: a real narrow store's buffer is data[1] or data[2]\n"
    "\t         (cpu_arm_instr_loadstore.c), so bytes past len are not store data at all, and a fetch past len reads\n"
    "\t         them; deepseek's `memory_readmax64(cpu, data, 4)` passed every row while they were 0), drives the\n")
rep(T + " *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).  Repair 3d (3c's own pass): five of those checks\n"
    + T + " *  now read what their names and COVERED claim -- the raw status at the DEVINIT Clear 0x20 (codex, grok, glm:\n",
    T + " *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).  Repair 3d (3c's own pass): six named rows, at four\n"
    + T + " *  check sites, now read what their names and COVERED claim -- the raw status at the DEVINIT Clear 0x20\n"
    + T + " *  (codex, grok, glm:\n")
rep(T + " *  re-arm row (a decline clearing it passed) -- with no new row (q2_20260923/r3d_20260923).\n",
    T + " *  re-arm row (a decline clearing it passed) -- with no new row (q2_20260923/r3d_20260923).  Repair 3e (3d's own\n"
    + T + " *  pass) checks every field and irq_asserted after EACH access of the multi-access rows (codex: a toggle on\n"
    + T + " *  each +0x180 decline cancelled across the re-arm row's two batches), again with no new row\n"
    + T + " *  (q2_20260923/r3e_20260923).\n")
rep(T * 3 + "    dropping the masked line from it, passed).  irq_asserted is NOT pinned here: the enable arms never\n"
    + T * 3 + "    write it, which is `fbirqstuck`'s defect, and a row pinning it would pin that defect.  */\n",
    T * 3 + "    dropping the masked line from it, passed).  irq_asserted is NOT pinned here: the enable arms never\n"
    + T * 3 + "    write it, which is `fbirqstuck`'s defect -- so 1 after the DEASSERTING Clear 0x10 would pin that defect.\n"
    + T * 3 + "    After the asserting Clear 0x400, 1 is right, and the re-arm row pins exactly that.  */\n")
rep("\t    pass (3d): 864, no row added -- five X14 checks read more, and X12/X13's buffer bytes above the width.  */\n",
    "\t    pass (3d): 864, no row added -- six X14 rows read more, and X12/X13's buffer bytes above the width; 3d's own\n"
    "\t    pass (3e): 864 -- X14's kept fields after each access, and X6/X9/X10's bytes above the width.  */\n")

io.open(dst, "w", encoding="utf-8", newline="").write(s)
print("patched ->", dst)
