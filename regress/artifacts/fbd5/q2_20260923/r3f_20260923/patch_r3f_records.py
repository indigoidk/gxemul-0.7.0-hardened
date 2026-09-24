#!/usr/bin/env python3
"""#545 repair 3f, RECORDS ONLY (comments; no check changes) -- 3e's own pass (panel_20260923_210234: codex, grok,
glm, deepseek DO NOT SHIP; agy, minimax, kimi-k3:cloud SHIP; q2h/codex_ded FAIL).  Every seat that dissented found the
two closures correctly IMPLEMENTED and the contract OVERSTATING them:
  (A) per-access checks exist on the three rows that CLAIM kept fields, not on every multi-access row (the DEVINIT
      reads and Set/Clear rows make several accesses and claim values and the drive) -- grok: `d->irq_asserted = 1`
      on the IRQ_STATUS read passes, because the DEVINIT reads row claims no kept field;
  (B) pad_kept sees a write-back past len at X6's declined accesses and X9/X10's legal reads; a FETCH past len whose
      value no channel uses (every declined write; the Opus seat's FW03) and a STORE past len inside a legal write
      (codex dedicated: `data[len] = 0` in the Clear write) are unobserved.  (B) was an above-floor addition (3d's D4),
      so its remainder is FILED as coverage debt, `fbbufbounds`, not rowed.
plus the caller sentence (codex: conditions that hold for the one fixed caller), FS02's condition and FMT01's attribution;
and from the Opus seat (its first turn fell back to opus-4-8 after a refusal; RESUMED, the verdict and corrections are
opus-5-5's): the common tail's write-back past len at VENDOR_ID/TIMER_1_VALUE, which X3 and X7 read without pad_kept --
re-measured by the main loop and EXTENDED to +0x288/+0x28c (q2_20260923/qwb_20260923/: all four green on 864) -- and
the caller line's count (ten shapes over seven fields).
usage: patch_r3f_records.py IN OUT"""
import io, sys

src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()
T = "\t"


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:100])
    s = s.replace(old, new)


rep(T + " *  four fields, the interrupt calls and, for a read, the read data over the width -- and in X6, X9 and X10\n"
    + T + " *  the bytes above the width untouched (3e) -- except X7 (the return value and the announce count only) and\n",
    T + " *  four fields, the interrupt calls and, for a read, the read data over the width -- and, after X6's declined\n"
    + T + " *  accesses and X9/X10's legal reads, the bytes above the width untouched: no write-back past len (3e) --\n"
    + T + " *  except X7 (the return value and the announce count only) and\n")
rep(T + " *    irq_asserted kept -- checked after EACH of its access (3e) (X14).\n",
    T + " *    irq_asserted kept -- checked after EACH of its accesses (3e) (X14).\n")
rep(T + " *    machine of type MACHINE_NONE -- and mem NULL, so a condition on ANY caller state in any test passes\n"
    + T + " *    every row (the Opus seat, 3c's pass: `mem` and the machine type, MC01-MC05 and MC07; grok, 3d's pass:\n",
    T + " *    machine of type MACHINE_NONE -- and mem NULL, so any condition on caller state that holds for that one\n"
    + T + " *    fixed caller (and not for a real one) passes every row (the Opus seat, 3c's pass: `mem` and the\n"
    + T + " *    machine type, MC01-MC05 and MC07; grok, 3d's pass:\n")
rep(T + " *    pass: ten more -- cpu->running, byte_order, is_32bit, ninstrs, machine->ncpus, pc, cpsr, CX01-CX10,\n"
    + T + " *    q2_20260923/q2g_opus/SUMMARY.txt);\n",
    T + " *    pass: ten more shapes over seven fields, two of them grok's -- cpu->running, byte_order, is_32bit,\n"
    + T + " *    ninstrs, machine->ncpus, pc, cpsr, CX01-CX10, q2_20260923/q2g_opus/SUMMARY.txt);\n")
rep(T + " *    to an announce that passes no argument, undefined behaviour in the real fatal(), whose vsnprintf has no\n"
    + T + " *    format attribute to warn from (FMT01; the Opus seat, 3d's pass);\n",
    T + " *    to an announce that passes no argument, undefined behaviour in the real fatal(), whose declaration\n"
    + T + " *    carries no format attribute, so no compiler warns (FMT01; the Opus seat, 3d's pass);\n")
rep(T + " *    28 of its 29 greens, q2_20260923/q2g_opus/); X14's multi-access rows check the five fields after every\n"
    + T + " *    access since 3e;\n",
    T + " *    28 of its 29 greens, q2_20260923/q2g_opus/).  Since 3e the three X14 rows that CLAIM kept fields (the\n"
    + T + " *    DEVINIT declines rows, the re-arm row) check the five fields after each access; the DEVINIT reads and\n"
    + T + " *    Set/Clear rows claim values and the drive, and the same instance's declines row pins the four fields at\n"
    + T + " *    its end, so a store there to irq_asserted -- the one field of the five that those rows, X9 and X10 never\n"
    + T + " *    name -- passes (grok, 3e's pass: `d->irq_asserted = 1` on the IRQ_STATUS read);\n"
    + T + " *    the caller's BUFFER beyond len where no check looks (filed `fbbufbounds`): a FETCH past len whose value no\n"
    + T + " *    channel uses -- at every declined write, and the Opus seat's FW03, an 8-byte fetch at len 4, equivalent\n"
    + T + " *    for the guest and a read past a real word store's data[4] -- because the harness's memory helpers do not\n"
    + T + " *    record the length the device asks for; a STORE past len inside a legal write (codex, 3e's pass:\n"
    + T + " *    `data[len] = 0` in the Clear write, measured green -- X12/X13 poison the buffer and do not re-check it\n"
    + T + " *    after the write); and the common tail's write-back past len at the legal reads outside X9/X10's five\n"
    + T + " *    registers, among them VENDOR_ID (+0x00), the timer value (+0x304; +0x324/+0x344/+0x364 fold onto it),\n"
    + T + " *    FIQEnable (+0x288) and the FIQEnableClear read (+0x28c) -- which X7 reads, and X3 three of them, with no\n"
    + T + " *    check above the width -- and the timer LOAD and CLEAR reads at the top of this file, whose 4-byte buffer\n"
    + T + " *    such a write-back overflows silently: an 8-byte write-back keyed on any one of them passes (the Opus\n"
    + T + " *    seat, 3e's pass, for VENDOR_ID and the timer value; the flagship seat's final adjudication for the\n"
    + T + " *    timer reads; all measured, q2_20260923/qwb_20260923/);\n")
rep(T + " *    and enabled (the Opus seat's FS02): only the Clear 0x10 row reaches that state, and it leaves irq_asserted\n",
    T + " *    and enabled (the Opus seat's FS02): of the Clears entered with irq_asserted 1, only the Clear 0x10 row\n"
    + T + " *    reaches that state, and it leaves irq_asserted\n")
rep(T + " *  pass) checks every field and irq_asserted after EACH access of the multi-access rows (codex: a toggle on\n"
    + T + " *  each +0x180 decline cancelled across the re-arm row's two batches), again with no new row\n",
    T + " *  pass) checks every field and irq_asserted after EACH access of the three rows that claim them kept (codex:\n"
    + T + " *  a toggle on each +0x180 decline cancelled across the re-arm row's two batches), again with no new row\n")
rep("/*  3e: a KEPT field is checked after EACH access of a multi-access row, never only at its end -- a toggle on\n"
    "    every +0x180 decline cancelled across the re-arm row's two batches and passed (codex, 3d's pass).  */\n",
    "/*  3e: a field an X14 row claims KEPT is checked after EACH of that row's accesses, never only at its end -- a\n"
    "    toggle on every +0x180 decline cancelled across the re-arm row's two batches and passed (codex, 3d's\n"
    "    pass).  */\n")
rep("\t    pass (3e): 864 -- X14's kept fields after each access, and X6/X9/X10's bytes above the width.  */\n",
    "\t    pass (3e): 864 -- X14's three kept-field rows after each access, and the bytes above the width after X6's\n"
    "\t    declined accesses and X9/X10's legal reads; 3e's own pass (3f): records only.  */\n")
io.open(dst, "w", encoding="utf-8", newline="").write(s)
print("patched ->", dst)
