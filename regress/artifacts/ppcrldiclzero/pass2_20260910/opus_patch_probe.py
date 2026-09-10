#!/usr/bin/env python3
#  Opus pass-2 seat: build a +3-row COPY of the shipped probe IN THE SCRATCHPAD, to
#  MEASURE (not predict) that three cheap rows close both measured escapes.
#  Never writes into GXEMUL-SEC.
#
#  *** ADD IS A **RAW** TRIPLE-QUOTED STRING.  In the first version it was a plain
#  '''...''' and Python turned the regex's `\b' into a literal BACKSPACE, so the
#  emitted probe carried r"^Hcr\s+= ..." -- a pattern that matches nothing, which
#  would have failed the `rc cr0' row on EVERY leg including BASE.  That is the
#  carrier's "one backslash level is consumed" trap and its "a pattern that matched
#  nothing reports zero for everything" trap in one line.  The emitted file is
#  grepped before any leg runs.  ***
import io, sys
src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding='utf-8', newline='').read()

ADD = r'''
# ============================== OPUS PASS-2 CANDIDATE ROWS (measurement only) ===
# Its OWN session, so the control session's disasm cross-check lists are untouched.
xregs, _, xT, xhow = session(
    seed([(SRC, RS_VAL)] + [(r, SENT) for r in DESTS]),
    [RLDICL(8, SRC, 63, 0),            # rotldi r8,r3,63 -- SH=63 NEEDS the sh5 bit
     RLDICL(11, SRC, 32, 32),          # high-word extract -- SH=32 NEEDS the sh5 bit
     enc_md(0, SRC, 10, 0, 32, rc=1)]) # rldicl. r10,r3,0,32 -- THE RECORD FORM
_cr = re.findall(r"cr[ \t]+= (0x[0-9a-fA-F]+)", xT)
_crv = int(_cr[-1], 16) if _cr else -1
row("cand session", xhow, "exit0", "the candidate-row session ran to `quit'")
row("cr parsed", "yes" if _cr else "no", "yes",
    "NEGATIVE CONTROL on the apparatus: the cr regex must MATCH something")
row("sh63 rldicl", hex(xregs.get(8, -1)), hex(want_rldicl(RS_VAL, 63, 0)),
    "SH=63: pins the sh5 bit of the SH decode")
row("sh32 rldicl", hex(xregs.get(11, -1)), hex(want_rldicl(RS_VAL, 32, 32)),
    "SH=32,MB=32 high-word extract: pins the sh5 bit again, on a masked cell")
row("rc cr0", hex(_crv), hex(0x40000000),
    "rldicl. -> CR0=GT.  defect gives EQ(0x2...), update_cr0(cpu,tmp) gives LT(0x8...)")

'''
anchor = "# ================================ WHY THE SIBLING ROWS ARE NOT HERE ============="
assert s.count(anchor) == 1, "ANCHOR NOT UNIQUE"
s = s.replace(anchor, ADD + anchor)
io.open(dst, 'w', encoding='utf-8', newline='').write(s)
print("patched probe written to", dst)
