#!/usr/bin/env python3
"""Opus seat, #545 q2c: make a GATED scratch copy of the FROZEN 707-row harness.

FBSKIP=<comma list> disables whole row families AT CODE LEVEL (the family's accesses do not run and
its rows do not exist).  With FBSKIP unset the gated binary must print byte-for-byte what the frozen
binary prints -- the driver checks that for every variant.

Gates: P, X1, X2, X3, X4, X5, X6 (sub: X6R the +0x18c read site, X6W the four write sites, X6P the
repeat access), X7 (sub: X7W enable writes, X7R legal reads), X8, X9 (sub: X9R reads, X9W writes),
X10 (sub: X10R reads, X10W the Clear write), X11, X12; states SEEDED, ZERO, WIDE, ONES (X6, X7, X9,
X10, X12 -- X11 always uses the seeded state and is gated only by X11).
Every edit is an exact-string replacement that must match exactly once, or this script refuses.
Usage: mkgated.py <frozen harness> <output path>
"""
import io, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = io.open(src_path, encoding="utf-8", newline="").read()
T = "\t"
NL = "\n"
Q = '"'

GATEFN = (
    "/*  OPUS q2c SCRATCH GATE: FBSKIP=<comma list> disables row families; unset = the frozen instrument.  */" + NL
    + "static const char *fbskip_env;" + NL
    + "static int G(const char *fam)" + NL
    + "{" + NL
    + T + "const char *p = fbskip_env;" + NL
    + T + "size_t n = strlen(fam);" + NL
    + T + "if (p == NULL || *p == '\\0')" + NL
    + T + T + "return 1;" + NL
    + T + "for (;;) {" + NL
    + T + T + "const char *e = strchr(p, ',');" + NL
    + T + T + "size_t m = e ? (size_t) (e - p) : strlen(p);" + NL
    + T + T + "if (m == n && strncmp(p, fam, n) == 0)" + NL
    + T + T + T + "return 0;" + NL
    + T + T + "if (e == NULL)" + NL
    + T + T + T + "return 1;" + NL
    + T + T + "p = e + 1;" + NL
    + T + "}" + NL
    + "}" + NL
    + "static int GS(int st)" + NL
    + "{" + NL
    + T + "return G(st == 0 ? " + Q + "SEEDED" + Q + " : st == 1 ? " + Q + "ZERO" + Q + " : st == 2 ? "
    + Q + "WIDE" + Q + " : " + Q + "ONES" + Q + ");" + NL
    + "}" + NL + NL)

EDITS = [
    # the gate functions, before main()'s preamble comment
    ("gatefn",
     "/*  The helper is static inside the shipped file, which is exactly why this driver includes",
     GATEFN + "/*  The helper is static inside the shipped file, which is exactly why this driver includes"),
    ("getenv",
     T + "setvbuf(stdout, NULL, _IOLBF, 0);" + NL,
     T + "setvbuf(stdout, NULL, _IOLBF, 0);" + NL + T + "fbskip_env = getenv(" + Q + "FBSKIP" + Q + ");" + NL),
    # P0-P9
    ("P",
     T + "{" + NL + T + T + "struct footbridge_data *h = calloc(1, sizeof(struct footbridge_data));" + NL
     + T + T + "unsigned char buf[8];",
     T + "if (G(" + Q + "P" + Q + ")) {" + NL + T + T
     + "struct footbridge_data *h = calloc(1, sizeof(struct footbridge_data));" + NL + T + T + "unsigned char buf[8];"),
    # X1
    ("X1",
     T * 2 + "for (w = 1; w <= 2; w++)" + NL + T * 3 + "for (i = 0; i < 5; i++) {" + NL
     + T * 4 + "x = calloc(1, sizeof(*x)); XSEED(x);",
     T * 2 + "if (G(" + Q + "X1" + Q + "))" + NL
     + T * 2 + "for (w = 1; w <= 2; w++)" + NL + T * 3 + "for (i = 0; i < 5; i++) {" + NL
     + T * 4 + "x = calloc(1, sizeof(*x)); XSEED(x);"),
    # X2 (the reads loop, then its summary row)
    ("X2a",
     T * 2 + "for (w = 1; w <= 2; w++)" + NL + T * 3 + "for (i = 0; i < 5; i++) {" + NL
     + T * 4 + "memset(b, 0, sizeof(b));",
     T * 2 + "if (G(" + Q + "X2" + Q + "))" + NL
     + T * 2 + "for (w = 1; w <= 2; w++)" + NL + T * 3 + "for (i = 0; i < 5; i++) {" + NL
     + T * 4 + "memset(b, 0, sizeof(b));"),
    ("X2b",
     T * 2 + "check_u(" + Q + "X2 the legal narrow reads announce nothing" + Q + ", fatal_calls, 0);",
     T * 2 + "if (G(" + Q + "X2" + Q + "))" + NL
     + T * 2 + "check_u(" + Q + "X2 the legal narrow reads announce nothing" + Q + ", fatal_calls, 0);"),
    # X3: open before its first decline loop, close after its last row
    ("X3a",
     T * 2 + "for (i = 0; i < 5; i++) {" + NL + T * 3 + "memory_writemax64(cpu, b, 4, 0x70);" + NL
     + T * 3 + "dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);" + NL + T * 2 + "}" + NL
     + T * 2 + "check_u(" + Q + "X3 the five declines latch (5 announces)" + Q,
     T * 2 + "if (G(" + Q + "X3" + Q + ")) {" + NL
     + T * 2 + "for (i = 0; i < 5; i++) {" + NL + T * 3 + "memory_writemax64(cpu, b, 4, 0x70);" + NL
     + T * 3 + "dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);" + NL + T * 2 + "}" + NL
     + T * 2 + "check_u(" + Q + "X3 the five declines latch (5 announces)" + Q),
    ("X3b",
     T * 2 + "check_u(" + Q + "X3 legal ZERO-data enable writes and other-register reads re-arm NO latch" + Q
     + ", fatal_calls - f0, 0);" + NL,
     T * 2 + "check_u(" + Q + "X3 legal ZERO-data enable writes and other-register reads re-arm NO latch" + Q
     + ", fatal_calls - f0, 0);" + NL + T * 2 + "}" + NL),
    # X4
    ("X4",
     T * 2 + "for (i = 0; i < 5; i++) {" + NL + T * 3 + "x = calloc(1, sizeof(*x)); XSEED(x);" + NL
     + T * 3 + "if (s5[i].wf == MEM_READ)",
     T * 2 + "if (G(" + Q + "X4" + Q + "))" + NL
     + T * 2 + "for (i = 0; i < 5; i++) {" + NL + T * 3 + "x = calloc(1, sizeof(*x)); XSEED(x);" + NL
     + T * 3 + "if (s5[i].wf == MEM_READ)"),
    # X5
    ("X5",
     T * 2 + "dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);" + NL
     + T * 2 + "check_u(" + Q + "X5 a legal ZERO EnableClear write announces nothing" + Q + ", fatal_calls, 0);" + NL
     + T * 2 + "check_u(" + Q + "X5 ... and leaves IRQEnable at 0x30" + Q + ", x->irq_enable, 0x30);" + NL,
     T * 2 + "if (G(" + Q + "X5" + Q + ")) {" + NL
     + T * 2 + "dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);" + NL
     + T * 2 + "check_u(" + Q + "X5 a legal ZERO EnableClear write announces nothing" + Q + ", fatal_calls, 0);" + NL
     + T * 2 + "check_u(" + Q + "X5 ... and leaves IRQEnable at 0x30" + Q + ", x->irq_enable, 0x30);" + NL
     + T * 2 + "}" + NL),
    # X6: per cell, and the repeat access
    ("X6",
     T * 5 + "for (dv = 0; dv < (S5[si].wf == MEM_WRITE ? 2 : 1); dv++) {" + NL
     + T * 6 + "x = calloc(1, sizeof(*x)); XSET(x, st);",
     T * 5 + "for (dv = 0; dv < (S5[si].wf == MEM_WRITE ? 2 : 1); dv++) {" + NL
     + T * 6 + "if (!G(" + Q + "X6" + Q + ") || !G(S5[si].wf == MEM_READ ? " + Q + "X6R" + Q + " : " + Q + "X6W" + Q
     + ") || !GS(st))" + NL + T * 7 + "continue;" + NL
     + T * 6 + "x = calloc(1, sizeof(*x)); XSET(x, st);"),
    ("X6P",
     T * 6 + "for (ord = 0; ord < 2; ord++) {",
     T * 6 + "for (ord = 0; ord < (G(" + Q + "X6P" + Q + ") ? 2 : 1); ord++) {"),
    # X7
    ("X7",
     T * 3 + "for (k = 0; k < 8 + 9 * 3; k++) {" + NL + T * 4 + "x = calloc(1, sizeof(*x)); XSET(x, st);",
     T * 3 + "for (k = 0; k < 8 + 9 * 3; k++) {" + NL
     + T * 4 + "if (!G(" + Q + "X7" + Q + ") || !G(k < 8 ? " + Q + "X7W" + Q + " : " + Q + "X7R" + Q
     + ") || !GS(st))" + NL + T * 5 + "continue;" + NL
     + T * 4 + "x = calloc(1, sizeof(*x)); XSET(x, st);"),
    # X8
    ("X8",
     T + "{" + NL + T * 2 + "struct footbridge_data *x = calloc(1, sizeof(*x));" + NL + T * 2 + "unsigned char b[8];"
     + NL + T * 2 + "arm_irqs(x);",
     T + "if (G(" + Q + "X8" + Q + ")) {" + NL + T * 2 + "struct footbridge_data *x = calloc(1, sizeof(*x));" + NL
     + T * 2 + "unsigned char b[8];" + NL + T * 2 + "arm_irqs(x);"),
    # X9
    ("X9",
     T * 3 + "for (k = 0; k < 5 * 3 + 8; k++) {" + NL,
     T * 3 + "for (k = 0; k < 5 * 3 + 8; k++) {" + NL
     + T * 4 + "if (!G(" + Q + "X9" + Q + ") || !G(k < 15 ? " + Q + "X9R" + Q + " : " + Q + "X9W" + Q
     + ") || !GS(st))" + NL + T * 5 + "continue;" + NL),
    # X10 reads, X10 Clear write
    ("X10R",
     T * 3 + "for (r = 0; r < 5; r++)" + NL + T * 4 + "for (w = 0; w < 3; w++) {" + NL,
     T * 3 + "for (r = 0; r < 5; r++)" + NL + T * 4 + "for (w = 0; w < 3; w++) {" + NL
     + T * 5 + "if (!G(" + Q + "X10" + Q + ") || !G(" + Q + "X10R" + Q + ") || !GS(st))" + NL
     + T * 6 + "continue;" + NL),
    ("X10W",
     T * 3 + "{" + NL + T * 4 + "uint32_t is = SY[st].is, ne = SY[st].ie & ~0x70u;",
     T * 3 + "if (G(" + Q + "X10" + Q + ") && G(" + Q + "X10W" + Q + ") && GS(st)) {" + NL
     + T * 4 + "uint32_t is = SY[st].is, ne = SY[st].ie & ~0x70u;"),
    # X11
    ("X11",
     T * 4 + "if (i == j)" + NL + T * 5 + "continue;" + NL,
     T * 4 + "if (i == j || !G(" + Q + "X11" + Q + "))" + NL + T * 5 + "continue;" + NL),
    # X12
    ("X12",
     T * 3 + "for (c = 0; c < 5; c++) {" + NL,
     T * 3 + "for (c = 0; c < 5; c++) {" + NL
     + T * 4 + "if (!G(" + Q + "X12" + Q + ") || !GS(st))" + NL + T * 5 + "continue;" + NL),
]

for tag, old, new in EDITS:
    n = s.count(old)
    if n != 1:
        print("REFUSE: anchor %s matches %d times" % (tag, n))
        sys.exit(2)
    s = s.replace(old, new)
    print("applied", tag)
io.open(out_path, "w", encoding="utf-8", newline="").write(s)
print("MKGATED_DONE", len(EDITS), "edits")
