"""#478 kill table.  The two mutants that matter came from the Opus seat and both
read as IMPROVEMENTS, which is what makes them dangerous:

  M3_ptr        `inbuf_len > 0`  ->  `d->inbuf_head != d->inbuf_tail`
                live pointers instead of a stale local -- looks better, and is
                invisible to every empty-ring row.
  M6_recompute  recompute occupancy from live pointers before the guard -- the
                intuitively CORRECT fix, and measurably worse: it fires on a
                2048-byte DATA-IN because 2048 % 512 == 0.

Plus the floor clauses: (b) verbatim revert, (c) null medium, (d) the one-character
`>= 0` tautology the Fable seat named, and the per-access/persistent distinction.
"""
import io, os, shutil

NL, T = chr(10), chr(9)
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
SCR = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad")
DET = os.path.join(SCR, "drain", "regress", "diff_wdc_identify.c")
OUT = os.path.join(SCR, "m478")

SRC = io.open(os.path.join(ROOT, "src", "devices", "dev_wdc.c"),
              encoding="utf-8", newline="").read()

GUARD = T*3 + "if (inbuf_len > 0 && !badlen_this &&" + NL
assert SRC.count(GUARD) == 1, "guard anchor %d" % SRC.count(GUARD)

#  the WHOLE condition, for mutants that rewrite more than the first line.  A
#  one-line anchor plus a multi-line replacement leaves the original tail behind
#  and the mutant DOES NOT BUILD -- which the carrier says is a FAULT, not a kill.
FULL = (GUARD +
        T*3 + "    (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
        T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL +
        T*3 + "    ||" + NL +
        T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
        T*3 + "    inbuf_len % 512 == 0)) ) {" + NL)
assert SRC.count(FULL) == 1, "full-guard anchor %d" % SRC.count(FULL)

DECL = T*3 + "int badlen_this = 0;" + NL
assert SRC.count(DECL) == 1, "decl anchor %d" % SRC.count(DECL)

SET = T*4 + "        badlen_this = 1;" + NL
assert SRC.count(SET) == 2, "set anchor %d (expected 2)" % SRC.count(SET)

MUT = [
    ("M1_ge0", "(d) `> 0` -> `>= 0`, a tautology  [fable]",
     [(GUARD, T*3 + "if (inbuf_len >= 0 && !badlen_this &&" + NL)]),

    ("M3_ptr", "(d) `inbuf_len > 0` -> live pointers  [opus -- reads BETTER]",
     [(GUARD, T*3 + "if (d->inbuf_head != d->inbuf_tail && !badlen_this &&" + NL)]),

    ("M6_recompute", "(d) recompute occupancy from live pointers  [opus]",
     [(GUARD, T*3 + "inbuf_len = d->inbuf_head - d->inbuf_tail;" + NL +
       T*3 + "while (inbuf_len < 0)" + NL +
       T*4 + "inbuf_len += WDC_INBUF_SIZE;" + NL +
       T*3 + "if (inbuf_len > 0 && !badlen_this &&" + NL)]),

    ("M7_nolen", "(d) drop the occupancy half, keep the bad-len half",
     [(GUARD, T*3 + "if (!badlen_this &&" + NL)]),

    ("M8_nobad", "(d) drop the bad-len half, keep the occupancy half",
     [(GUARD, T*3 + "if (inbuf_len > 0 &&" + NL)]),

    ("M9_persist", "(d) the per-access local made PERSISTENT across accesses",
     [(DECL, T*3 + "static int badlen_this = 0;" + NL)]),

    ("M10_modinv", "(d) modulus `== 0` -> `!= 0`  [codex -- inverts sufficiency]",
     [(FULL, T*3 + "if (inbuf_len > 0 && !badlen_this &&" + NL +
       T*3 + "    (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
       T*3 + "    inbuf_len % (512 * d->write_count) != 0)" + NL +
       T*3 + "    ||" + NL +
       T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
       T*3 + "    inbuf_len % 512 != 0)) ) {" + NL)]),

    ("Mb_revert", "(b) VERBATIM reinstatement of the unguarded drain",
     [(GUARD, T*3 + "if (" + NL),
      (SET, T*4 + "        (void) 0;" + NL)]),
]

if os.path.isdir(OUT):
    shutil.rmtree(OUT)

for name, desc, edits in MUT:
    s = SRC
    for find, repl in edits:
        n = s.count(find)
        want = 2 if find == SET else 1
        assert n == want, "%s: anchor matched %d, wanted %d" % (name, n, want)
        s = s.replace(find, repl, want)
    assert s != SRC, "%s: no-op" % name
    d = os.path.join(OUT, name)
    os.makedirs(os.path.join(d, "src", "devices"))
    os.makedirs(os.path.join(d, "regress"))
    io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
            "w", encoding="utf-8", newline="").write(s)
    shutil.copy(DET, os.path.join(d, "regress", "diff_wdc_identify.c"))
    print("  %-14s %s" % (name, desc))

d = os.path.join(OUT, "Mc_null")
os.makedirs(os.path.join(d, "src", "devices"))
os.makedirs(os.path.join(d, "regress"))
io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
        "w", encoding="utf-8", newline="").write("/*  clause (c) null medium.  */" + NL)
shutil.copy(DET, os.path.join(d, "regress", "diff_wdc_identify.c"))
print("  %-14s %s" % ("Mc_null", "(c) NULL MEDIUM"))
