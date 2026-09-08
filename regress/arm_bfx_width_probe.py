#!/usr/bin/env python3
#
#  armbfxwidth32 -- RUNG-3 WITNESS: UBFX/SBFX build their mask with a shift that is undefined
#  at the top of the encoded width range.
#
#      cpu_arm_instr.c:4486  ubfx:  int width = 1 + ((iword >> 16) & 31);   -> {1..32}
#      cpu_arm_instr.c:4493  sbfx:  int width = 1 + ((iword >> 16) & 31);   -> {1..32}
#      cpu_arm_instr.c:1316  ubfx:  uint32_t mask = (1 << width) - 1;
#      cpu_arm_instr.c:1340  sbfx:  uint32_t mask = (1 << width) - 1;
#      cpu_arm_instr.c:1344  sbfx:  uint32_t topBitMask = 1 << (width-1);
#      cpu_arm_instr.c:1370  bfi :  uint32_t mask = (1 << width) - 1;       (width = msb-lsb+1)
#
#  `1' is a plain int, so `1 << 32' shifts by the full width of the type (C99 6.5.7p3) and
#  `1 << 31' is a signed overflow (6.5.7p4).
#
#  *** WHICH OF THOSE IS OBSERVABLE IS A DIFFERENT QUESTION, AND ONLY ONE IS. ***  Derived by
#  walking the values, against the pass-1 panel's own framing of "two widths wide":
#
#      width  correct       predicted today   observable?
#      32     0x89abcdef    0x00000000        YES -- the whole register becomes zero
#      31     0x09abcdef    0x09abcdef        no -- `1<<31' gives INT_MIN and INT_MIN-1 wraps
#                                             back to INT_MAX = 0x7fffffff, the CORRECT mask
#       8     0x000000de    0x000000de        no
#       1     0x00000001    0x00000001        no
#
#  So the RED row is width 32 alone.  The width-31 row is carried anyway, because it pins that a
#  repair does not BREAK the case that currently works by accident.
#
#  ---------------------------------------------------------------------------------------------
#  *** THE HAND-ASSEMBLED-ENCODING TRAP IS LOAD-BEARING HERE, NOT MERELY PRUDENT. ***
#
#  This project has been bitten four times by hand-assembled encodings, once in a COMMITTED gate
#  row that measured the wrong register for months.  The signature is always the same: a wrong
#  field yields 0, and any row that accepts 0 passes by accident.
#
#  **The width-32 symptom IS exactly zero.**  So a mis-encoded word that never executed is
#  indistinguishable from the defect this probe exists to witness.  THREE independent controls,
#  because one is not enough:
#
#    * `pc adv'  -- pc must advance by exactly 4.  A word the decoder cannot translate does not
#                  quietly do nothing.  *** AN EARLIER DRAFT SAID IT ALWAYS REACHES THE SHARED
#                  `bad' LABEL AND SETS cpu->running = 0.  THAT IS STALE: `#312' added an
#                  UNDEFINED-INSTRUCTION route, and cpu_arm_instr.c says so in its own words --
#                  "Routing to und fixes that", "This is where the und routing lives now" -- while
#                  a `goto bad' remains for other cases.  So the claim is true of SOME encodings
#                  and false as stated.  Either way pc does not land on CODE+4 with r0 set, which
#                  is what this row actually tests. ***
#    * `mid'     -- UBFX r0,r1,#4,#8 must give 0xde.  A small nonzero answer that only a correctly
#                  encoded, correctly executed instruction produces.
#    * `live'    -- a plain MOV proves plant/step/print works before any bitfield word is tried.
#
#  ---------------------------------------------------------------------------------------------
#  MACHINERY, established from source by a codex capability pass rather than assumed:
#
#    * `put w' -> store_32bit_word() writes through cpu->byte_order and applies NO encoding
#      whitelist; the CPU memory function calls invalidate_code_translation(), and ARM's
#      invalidator resets the ENTIRE 4 KiB instruction page.  No guest cache maintenance needed.
#    * testarm is LITTLE-endian, SA1110, supervisor mode, MMU DISABLED, so virtual == physical.
#      Base RAM is [0, R) and `-M 64' gives 0x00000000-0x03ffffff.
#    * *** r10-r15 ARE NOT REGISTERED DEBUGGER NAMES. ***  arm_cpu_new() exposes r0-r9, then
#      sl, fp, ip, sp, lr, plus pc and cpsr.  `print r10' fails a lookup and returns nothing --
#      so this probe uses r0 and r1 ONLY.
#    * *** A DIRECT `cpsr' PRINT CAN SHOW STALE NZCV *** (the settings access does not sync the
#      execution-flags field).  This probe therefore reads a GPR and never the flags.
#    * The top of RAM is occupied -- a 12-byte halt stub at SP+32 with SP = R-4096, AND a PROM
#      hook at R-8 written by arm_cpu_new().  CODE is planted low, at 0x10000.
#    * Coprocessor encodings still exit(1) in arm_coproc_15 / i80321_6 / xscale_14.  Every word
#      below is a data-processing media encoding; none touches CP space.
#
#  ---------------------------------------------------------------------------------------------
#  *** WHAT THIS PROBE CANNOT SEE, from the pass-2 panel, stated before anyone relies on it. ***
#
#  Two one-line regressions re-open real undefined behaviour and score FULL MARKS, and no
#  guest-value row can kill either.  Disclosed, not covered:
#
#    * `1U' -> `1' in the mask ternary.  Re-opens C99 6.5.7p4 at width 31.  `w31' stays green --
#      it is the very wrap the fix comment describes -- and `w32' never evaluates the shift.
#      `1 << 31' and `1U << 31' yield the SAME mask after the `- 1'.
#    * restoring `uint32_t topBitMask = 1 << (width-1);' above the `if'.  Re-opens the second UB.
#      `s w32' stays green: with a correct 32-bit mask, `x |= ~mask' is `x |= 0'.
#      **`s w32' pins the MASK -- not topBitMask, and not the hoist.**
#
#  Both are DEFINEDNESS repairs, and definedness has no guest-visible value on a non-trapping
#  host.  The vehicle that could pin them is UBSAN or a source pin, not a row.
#
#  *** AND UBSAN IS PRESENT.  An earlier draft of this paragraph said "whether build-asan/
#  carries UBSAN is UNCHECKED" -- a wrong record written one grep away from the answer, in
#  the same file, while composing an otherwise honest disclosure.  Checked:
#      build-asan/Makefile      -fsanitize=address,undefined
#      build-asan/src/Makefile  -fsanitize=address,undefined
#      regress/gate_asan_sweep.sh   already exists
#  So both escapes ARE pinnable -- as a DIFFERENTIAL, not a row: the fixed source produces no
#  shift diagnostic and the `1U' -> `1' mutant produces one.  That is a second binary and a
#  STDERR oracle rather than a value oracle, i.e. a new measurement lane, so it is filed as
#  [[ubsanshiftlane]] for its own round rather than bolted onto one whose pass 2 has run. ***
#
#  The honest statement is therefore: these two are unkillable BY THIS PROBE, not unkillable
#  in principle.  Recorded so a future reader does not read a full score as covering the
#  whole diff.
#
#  Usage:  arm_bfx_width_probe.py <gxemul-binary> [label]
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-12s %-14s %-14s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

CODE = 0x8000                     # the address arm_flags_probe.py uses; low RAM, clear of the
                                  # halt stub at SP+32 and the PROM hook at R-8

#  *** A LOAD FILE IS REQUIRED, NOT COSMETIC -- AND I REPRODUCED THE EXACT DEFECT A PANEL HAD
#  CAUGHT IN A SIBLING PROBE HOURS EARLIER. ***  `main.c` with no loadfile and no `-d` prints
#  "No filename given. Aborting." and exits, so EVERY session reports `died`.  The first run of
#  this probe scored 1/11 with all ten measurement rows reading `died` -- and the `live` row is
#  what named it as an apparatus failure instead of letting it read as a defect signal.
#  Every ARM probe in this tree passes `"0x%x:%s" % (CODE, STUB)`; they take the stub path from
#  their gate caller, so a standalone probe must make its own.  Contents are irrelevant -- every
#  word is overwritten by `put w` before `pc` is set -- but the file must exist and be non-empty.
STUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arm_bfx_stub.bin")
if not os.path.exists(STUB):
    with open(STUB, "wb") as f:
        f.write(bytes(16))        # 16 zero bytes; no escape, so the heredoc trap cannot recur
SRC  = 0x89abcdef                 # four distinct nibble groups, top bit SET on purpose:
                                  # width 32 must return it WHOLE, and a mask of 0 returns 0.
OP_MOV_R0_2A = 0xe3a0002a         # mov r0, #0x2a   -- the liveness word

#  UBFX/SBFX encodings, DERIVED from the decoder rather than recalled, and self-checked below
#  against its own mask.  Field positions read out of X(to_be_translated):
#      rd  = (iword >> 12) & 15
#      *** THE SOURCE IS `rm' = iword & 15, NOT `rn' *** -- rn's bits 19:16 are occupied by
#      widthm1, which is exactly why the ubfx block takes rm.  Getting that backwards IS the
#      hand-assembled-encoding trap.
def bfx(base, rd, rm, lsb, width):
    return (0xe << 28) | base | (((width - 1) & 31) << 16) | ((rd & 15) << 12) \
           | ((lsb & 31) << 7) | (rm & 15)

UBFX_BASE, SBFX_BASE = 0x07e00050, 0x07a00050
UBFX_MASK, SBFX_MASK = 0x0fe00070, 0x0fe00070

def ubfx(lsb, width): return bfx(UBFX_BASE, 0, 1, lsb, width)
def sbfx(lsb, width): return bfx(SBFX_BASE, 0, 1, lsb, width)

def session(cmds, settle=1.5, spin=1.5):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-A", "-E", "testarm", "-M", "64",
                       "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.22):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % int(m.group(1), 16)

def run_word(iw, src=SRC):
    """Plant ONE instruction word, step it, and read r0 and pc back."""
    cmds = ["r1=0x%x" % src, "r0=0x0",
            "put w 0x%x, 0x%08x" % (CODE, iw),
            "pc=0x%x" % CODE, "step 1", "print r0", "print pc"]
    t, alive = session(cmds)
    return t, alive, printed(t, "r0"), printed(t, "pc")

print("arm_bfx_width_probe -- binary=%s label=%s machine=testarm" % (BIN, LABEL))
print("%-12s %-14s %-14s %-56s %s" % ("row", "got", "want", "note", ""))

#  ---- the encodings must satisfy the decoder's OWN mask, checked before anything is run -------
enc_ok = all((w & UBFX_MASK) == UBFX_BASE for w in (ubfx(0, 32), ubfx(0, 31), ubfx(4, 8), ubfx(0, 1))) \
     and all((w & SBFX_MASK) == SBFX_BASE for w in (sbfx(0, 32), sbfx(4, 8)))
row("enc ok", "yes" if enc_ok else "no", "yes",
    "every planted word matches the decoder's own mask -- checked before any run")

#  ---- CONTROL 1: the plant/step/print path works at all ---------------------------------------
t, alive, r0, pc = run_word(OP_MOV_R0_2A)
row("live", r0 if alive else "died", "0x2a",
    "LIVENESS: a plain `mov r0,#0x2a' plants, steps and prints")
row("pc adv", pc if alive else "died", "0x%x" % (CODE + 4),
    "CONTROL: pc advanced exactly 4.  A bad encoding sets running=0 and pc does NOT move")

#  ---- CONTROL 2: a small NONZERO answer, because the defect's symptom is exactly zero ---------
t, alive, r0, pc = run_word(ubfx(4, 8))
row("mid", r0 if alive else "died", "0xde",
    "UBFX #4,#8 of 0x89abcdef -- only a correct encoding AND execution gives 0xde")
row("mid pc", pc if alive else "died", "0x%x" % (CODE + 4),
    "CONTROL: the bitfield word really executed; it did not stop the machine")

t, alive, r0, pc = run_word(ubfx(0, 1))
row("w1", r0 if alive else "died", "0x1",
    "UBFX #0,#1 -- the narrowest field, nonzero")

#  ---- THE DEFECT ROW.  Asserts the CORRECT value and is expected to FAIL pre-fix. -------------
#  `1 << 32' shifts by the type's own width, the mask becomes 0 on the common lowering, and the
#  instruction returns 0 instead of the whole register.
t, alive, r0, pc = run_word(ubfx(0, 32))
row("w32", r0 if alive else "died", "0x89abcdef",
    "UBFX #0,#32 must return the WHOLE register -- `1 << 32' is undefined")
row("w32 pc", pc if alive else "died", "0x%x" % (CODE + 4),
    "CONTROL: it EXECUTED and returned a wrong value; it did not fail to decode")

#  ---- the neighbour that currently works BY ACCIDENT, pinned so a repair does not break it ----
t, alive, r0, pc = run_word(ubfx(0, 31))
row("w31", r0 if alive else "died", "0x9abcdef",
    "UBFX #0,#31 -- UB (1<<31 overflows int) but wraps to the right mask; must STAY right")

#  ---- SBFX: the same mask site, plus its own second shift at :1344 ----------------------------
t, alive, r0, pc = run_word(sbfx(4, 8))
row("s mid", r0 if alive else "died", "0xffffffde",
    "SBFX #4,#8 of 0x89abcdef: field 0xde, top bit set, so sign-extended")

t, alive, r0, pc = run_word(sbfx(0, 32))
row("s w32", r0 if alive else "died", "0x89abcdef",
    "SBFX #0,#32: the whole register.  Does NOT pin topBitMask -- see the header")

#  *** ADDED BY PASS 2.  grok derived this escape and it holds: deleting the BIT TEST from
#  `if (width < 32 && ...)' -- always sign-extend below width 32 -- scores full marks, because
#  EVERY byte field of 0x89abcdef has bit 7 set (0x89, 0xab, 0xcd, 0xef) and `s mid' is a byte
#  field.  No row had an SBFX field whose top bit is CLEAR, so nothing could see it. ***
#      SBFX #1,#4 of 0x89abcdef: (V >> 1) & 0xf = 0x7, bit 3 CLEAR -> NOT sign-extended -> 0x7
#      under always-extend:      0x7 | ~0xf = 0xfffffff7
row("s w32 pc", pc if alive else "died", "0x%x" % (CODE + 4),
    "CONTROL: the SBFX word EXECUTED -- see the note below")
#  *** ADDED BY PASS 2.  An earlier draft of this probe, its CHANGELOG block AND its commit
#  message all said `pc adv = 0x8004' holds "on EVERY row".  IT DID NOT: only `pc adv', `mid pc'
#  and `w32 pc' asserted pc, and all three are MOV/UBFX.  NO SBFX ROW CHECKED PC AT ALL -- and the
#  SBFX rows are the ones whose expected failure value is also EXACTLY ZERO, which is precisely
#  the case the pc control exists to disambiguate.  Named by the codex seat. ***

t, alive, r0, pc = run_word(sbfx(1, 4))
row("s clear", r0 if alive else "died", "0x7",
    "SBFX #1,#4 -> field 0x7, top bit CLEAR: must NOT sign-extend")

#  *** ADDED BY PASS 2: SBFX AT WIDTH 31 WAS ENTIRELY UNTESTED. ***  The round's headline claim --
#  "only the width-32 case is observable" -- rested on a UBFX width-31 row and generalised to SBFX
#  with no evidence.  SBFX #0,#31 of 0x89abcdef masks to 0x09abcdef, whose bit 30 is CLEAR, so it
#  must NOT sign-extend.  (codex.)
t, alive, r0, pc = run_word(sbfx(0, 31))
row("s w31", r0 if alive else "died", "0x9abcdef",
    "SBFX #0,#31: bit 30 CLEAR, so no sign extension -- and it pins SBFX at width 31 at all")

ok = sum(1 for _, o in rows if o)
print()
print("ARMBFX_RESULT=%d/%d" % (ok, len(rows)))
print("ARMBFX_DONE")
sys.exit(0 if ok == len(rows) else 1)
