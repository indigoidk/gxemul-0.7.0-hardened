#!/usr/bin/env python3
"""Round 104 gate candidate: the ARM load/store base writeback (#19).

The template `cpu_arm_instr_loadstore.c` computes one address, MASKS it for
alignment, and then writes the base register back from the masked value. ARM ARM
DDI 0100I computes the writeback from the UNMASKED Rn:

  A5.2.8 post-indexed:  address = Rn ;  Rn = Rn + offset_12
  A5.2.5 pre-indexed:   address = Rn + offset_12 ;  Rn = address
  A2-43: the truncation lives inside Memory[<address>,<size>], i.e. on the
         address sent to memory -- never on the register.

There are EXACTLY FOUR writeback sites in the single-register path, established
by enumeration: two `reg(ic->arg[0]) =` statements in `A__NAME__general` (the
pre-index and post-index forms) and the matching pair in `A__NAME`'s fast path.
#364 removed the numeric cites that used to stand here -- they had gone stale a
THIRD time, in the very file whose #357 note below says a numeric cite here has
gone stale twice. Grep for the statement, not a line.
`A__NAME_PC` and every conditional variant (`__eq`, `__ne`,
...) merely CALL `A__NAME`; two review seats suspected the PC special case was a
third copy and it is not. A review seat enumerated the instantiations from
generate_arm_loadstore.c -- 8 p/u/w files x (8 mode-2 + 12 mode-3) = 160 handler
families -- all funnelling through those four statements.

WHICH SITE EACH ROW REACHES  --  #364: THE TABLE BELOW USED TO BE INVERTED
---------------------------------------------------------------------------
It claimed "the fast path only runs once the page is in the translation array,
so a SINGLE-execution row measures the GENERAL path and nothing else", and
attributed rows to general sites on that basis. MEASURED FALSE, and in the worst
direction: NO row in this probe reached the general path AT ALL. A temporary
marker at the top of `A__NAME__general` counted ZERO hits across all 17 rows --
not only the `once()` rows but the `loop10` iterations and both `warmed` passes.

The cause is this probe's own seeding. `put w` routes through
`store_32bit_word` -> `memory_rw` with CACHE_DATA, and insertion into the
translation array is gated on `!no_exceptions`, so seeding a page with `put w`
ALREADY warms it: `host_load` is non-NULL before the guest executes a single
instruction. `put b` is the opposite -- CACHE_NONE | NO_EXCEPTIONS -- and does
not insert. The old note had these two backwards.

Consequence, stated plainly because two shipped rounds leaned on the old table:
`#357`'s general-path writeback sites and `#362`'s general-path rotation were
BOTH unmeasured, and each was independently confirmed deletable with the whole
of gate 14 still green at 261 checks. The historical pre-fix sweep of 5/14 is
entirely attributable to the fast path.

TWO AXES, kept apart, because conflating them is how the first draft of this very
correction went wrong. A round of review found that draft claimed the new cold
rows covered "general post-index writeback". They do not, and the reason is worth
stating because it is easy to miss twice: `LDR_OFF0` is P=1/W=0, and the writeback
is emitted only under (P and W) or (not P) -- so an offset form has NO WRITEBACK
STATEMENT AT ALL, and `wb_addr` is not even declared for it. So:

WHICH ROWS REACH THE FOUR WRITEBACK SITES (the `reg(ic->arg[0]) =` statements)
  fast    post-index  -- A, A2, B, F, S, R, G, `post4 algn`, `algn load data`,
                         `byte post1 unal`, `wrap from zero`      (11 rows)
  fast    pre-index   -- C (`pre4 unal gen`) and C2 (`pre4 unal fast`, BOTH
                         passes, not just the second)              (2 rows)
  general post-index  -- `ldrt post4 unal` (this probe), and the fold-marker
                         probe's `copyin cold` / `copyout cold` arms
  general pre-index   -- `cold pre4 unal` (this probe), and the strlen probe's
                         `ldrb r3,[r4,#1]!` walk on each new page

#365 CORRECTED A CLAIM #364 MADE HERE. This table used to say both general
writeback sites were UNCOVERED and that `#357`'s fix "STILL has no row reaching
it". Measured false, and the correction is sharper than the claim: both sites
were already REACHED, just not by rows in this file -- deleting the two general
writeback statements turns 8 gate checks red in the strlen and fold-marker
sections while this probe stays 20/20. What was missing was DISCRIMINATION.
Rebuild with the faithful pre-`#357` bug (general writeback re-masked, fast pair
intact) and the whole gate passed at 264: `ldrb` has datalen 1, so
`addr &= ~(datalen - 1)` is the identity, and the fold arms use aligned bases.
Reaching a statement without discriminating its correction measures nothing about
it. The two `#365` rows are the first anywhere in the battery that do discriminate
it, verified against that exact mutant.

ROWS WITH NO WRITEBACK SITE AT ALL (P=1/W=0 offset forms)
  `pre4 no wb` and the three `rot word unal` rows -- in the FAST function
  the three `rot word cold` rows                 -- in the GENERAL function

WHICH ROWS REACH THE GENERAL FUNCTION AT ALL, which is a different question and
the one this round actually answers: the three `rot word cold` rows, and nothing
else. They exercise `A__NAME__general`'s load-and-rotate arm and the `memory_rw`
slow path -- the first rows in this file's history to enter that function. That
is a DATA site, not a writeback site, and the round's value is real either way:
`#362`'s general-path rotation was deletable with the whole gate green before
these rows existed.

Deliberately no line numbers here: the `#357` note below says a numeric cite in
this file has gone stale twice, and the ones this table used to carry had gone
stale a third time by the round that corrected it.

A general-path row therefore needs a page this probe never touches with `put w`.
That is what COLD/COLD1/COLD2/COLD3 are for, and the three `cold` rotation rows
are the first rows in this file's history to enter `A__NAME__general`.
A guest STORE does NOT work for this and was tried: `update_translation_table`
sets `host_load` unconditionally and gates only `host_store` on the write flag,
so storing to a page warms it for loading too.

`put b` is not the ONLY cold seeding -- a review seat corrected an earlier draft
that said so. The debugger's string modes `put s` and `put z` also write through
`memory_rw` with `CACHE_NONE | NO_EXCEPTIONS` and leave a page equally cold. It
is the flag that matters, not the command; `put b` is simply the convenient one
for laying down four chosen bytes. (`put h`/`put w`/`put d` all reach CACHE_DATA
via store_16/32/64bit_word, so all three warm.)

TWO INSERTION ROUTES THAT DO NOT OBEY THE `!no_exceptions` GATE, both found in
review and both counter-intuitive enough to be worth naming here rather than
leaving for the next person to trip over:
  * THE DEVICE ARM INSERTS DESPITE NO_EXCEPTIONS. `memory_rw`'s device path gates
    on `update_translation_table != NULL && !(ok & MEMORY_NOT_FULL_PAGE) &&
    (devices[i].flags & DM_DYNTRANS_OK)` -- with NO `!no_exceptions` term. So a
    `put b` to a fully-backed DM_DYNTRANS_OK device page WARMS it, and with
    NO_EXCEPTIONS set the device handler is not even called, so the write is
    dropped while the mapping is installed. Harmless at 0x20000 on testarm, whose
    devices all sit at >= 0x10000000 -- but fatal to this mechanism if COLD ever
    moves, and the assert below does NOT check for it.
  * INSTRUCTION FETCH INSERTS WITH writeflag 0. quick_pc_to_pointers' generic
    path calls update_translation_table when host_load is NULL, so EXECUTING on a
    page warms it for LOADS (leaving host_store NULL). Irrelevant to COLD, which
    is never executed, but it means "put b leaves a page cold" is a statement
    about SEEDING and not about the page's whole life.
Also contingent, and worth knowing before this is reused: with the MMU ON,
arm_translate_v2p_mmu failure returns BEFORE the insertion gate, so `put w` would
not warm an unmapped page at all. testarm never enables the MMU. And the
translation array is a 384-entry round-robin TLB, so a row set touching more
pages than that would silently re-cool a warmed page -- this probe's working set
is about four pages, so the attribution here is a property of that, not a theorem.

Loads and stores are SEPARATE instantiations of this template, so a row set made
only of loads cannot see a store-side regression at all: row S is a store
livelock. Register-offset forms (`A__REG`) are a third family: row R.

THE HEADLINE IS A LOOP THAT CANNOT MAKE PROGRESS
------------------------------------------------
When the post-index offset is not a multiple of the access size the masked
writeback is a FIXED POINT. Word base 0x10001 with offset 1 masks to 0x10000,
adds 1, and writes back 0x10001 -- the value it started from. No amount of guest
patience recovers from that, which is why it is the headline rather than the
one-off wrong values. Progress is asserted as an exact architectural value after
an architecturally bounded iteration count, never as "how far did it get in T
seconds": the loop is counted in r3, which is independent of r0.

WHAT IS MANDATED VERSUS MERELY PERMITTED
----------------------------------------
A review seat supplied a precision worth keeping: the writeback is ARCHITECTURALLY
MANDATED for word accesses, whose unaligned behaviour is defined. Unaligned
halfword loads (A4.1.28) and doubleword accesses (A2.8) are UNPREDICTABLE prior
to ARMv6, so there an unmasked writeback is permitted-and-consistent rather than
required. Every row below except G is a word form, i.e. in mandated space. Row G
is labelled DISC-M ("model") for exactly that reason: it pins the pseudocode
model of A5.3.6, not a silicon mandate, and it asserts only the BASE -- an
unaligned halfword load's DATA is UNPREDICTABLE and must never be asserted.

NO LDRD/STRD ROW, overruling three review seats: A2.8 makes a doubleword access
UNPREDICTABLE prior to ARMv6 whenever the address is not doubleword-aligned, so
every base that would exercise the `~7` mask makes the instruction unspecified.
The general-path fix covers LDRD/STRD (the fast path chickens out to it at
:226-228, masking with `datalen - 1` == 7) but that coverage cannot honestly be
gated. #355 already taught this project not to assert on encodings the
architecture declines to define.

UNALIGNED-LOAD-DATA ROWS -- #364: THIS SECTION USED TO SAY THERE WERE NONE, and
it was written when that was true. It argued that a PIN on the unrotated value
would be "inverted by the round that fixes the rotation", i.e. rewritten by the
change it exists to guard, so only an ALIGNED-base data row was safe.

That reasoning was sound and its conclusion is now obsolete: `#362` FIXED the
rotation and added three DISC rows on the unrotated-vs-rotated pair (a DISC row
states both values, so it is not inverted by the fix -- it is satisfied by it),
and `#364` added three more from a cold page. Six rows now pin unaligned loaded
data. The aligned-base row stays, and stays correct for its own reason: no
rotation applies at offset 0 in any architecture version.

Kept rather than deleted because the ARCHITECTURE note is still the reference:
ARMv5 and below with CP15 A == 0 rotate the aligned word right by 8 * addr[1:0]
(A2.8 p. A2-38, A4.1.23), so a base of 0x10001 over the word 0x11223344 owes
0x44112233 and NOT the masked 0x11223344.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
CODE = 0x8000
SRC = 0x10000

#  Encodings. Bits after the 010 class are P U B W L, verified against the
#  ldrt form 0xe4b0a004 (`ldrt sl,[r0],#4`) that netbsd_copyin matches; the
#  register-offset forms use class 011. The halfword layout is
#  cond 000 P U I W L Rn Rd immH 1SH1 immL, checked against `ldrh r1,[r0]` ==
#  0xe1d010b0. EVERY word below was confirmed through the emulator's own
#  `unassemble` before this probe was run -- this project has shipped a
#  mis-encoded row before, one of them a committed gate row that measured the
#  wrong register for months.
MOV_R0_10000 = 0xE3A00801   # mov  r0,#0x10000
MOV_R0_0     = 0xE3A00000   # mov  r0,#0
ADD_R0_1     = 0xE2800001   # add  r0,r0,#1
MOV_R2_1     = 0xE3A02001   # mov  r2,#1
MOV_R3_0     = 0xE3A03000   # mov  r3,#0
MOV_R3_1     = 0xE3A03001   # mov  r3,#1
LDR_P1       = 0xE4901001   # ldr  r1,[r0],#1     post-index, +1
LDR_P4       = 0xE4901004   # ldr  r1,[r0],#4     post-index, +4
LDR_PRE4W    = 0xE5B01004   # ldr  r1,[r0,#4]!    pre-index + writeback
LDR_PRE4     = 0xE5901004   # ldr  r1,[r0,#4]     pre-index, NO writeback
LDR_M4       = 0xE4101004   # ldr  r1,[r0],#-4    post-index, -4  (U == 0)
LDRB_P1      = 0xE4D01001   # ldrb r1,[r0],#1     byte: masks nothing
LDRH_P1      = 0xE0D010B1   # ldrh r1,[r0],#1     halfword: masks ~1
#  0xE480, not 0xE400: with L == 0 the U bit sits in the same nibble, so the
#  obvious guess 0xe4002001 disassembles as `str r2,[r0],#-1` -- a NEGATIVE
#  offset. Caught by `unassemble` before the sweep; it would have produced an
#  UNEXPECTED value and sent the round debugging the emulator.
STR_P1       = 0xE4802001   # str  r2,[r0],#1     STORE post-index, +1
LDR_POST_R2  = 0xE6901002   # ldr  r1,[r0],r2     post-index, REGISTER offset
ADD_R3_1     = 0xE2833001   # add  r3,r3,#1
SUBS_R3_1    = 0xE2533001   # subs r3,r3,#1
CMP_R3_10    = 0xE353000A   # cmp  r3,#10
SPIN         = 0xEAFFFFFE   # b .

#  #365: the T form -- P=0/U=1/B=0/W=1/L=1, class 010. CHECKED through
#  `unassemble` as `ldrt r1,[r0],#4`, and it lands in
#  tmp_arm_loadstore_p0_u1_w1.c, handler arm_instr_load_w1_word_u1_p0_imm
#  (generator index reg*512+p*256+u*128+b*64+w*32+l*16+c, so
#  ((iword >> 16) & 0x3f0) + cond = 176 + 14 = 190).
#
#  WHY A T FORM RATHER THAN A COLD PAGE: this reaches A__NAME__general BY
#  CONSTRUCTION and is immune to warming. The template tests
#  is_userpage[addr >> 17] BEFORE the `page == NULL` test, and a clear bit calls
#  A__NAME__general regardless of how warm the page is. The bit is set only when
#  update_translation_table receives MEMORY_USER_ACCESS, which only this T-form
#  family passes -- so a `put w` page is warm and the first `ldrt` still goes
#  general. That cannot be silently voided by a future seeding change, which a
#  cold page can be (see the device-arm and instruction-fetch notes above).
#
#  Rd is r1 DELIBERATELY, not r9: `0xE4B09004` is the word that arms
#  COMBINE(netbsd_copyin), so an r9 destination would put this row in the
#  instruction-combiner's path and measure something else entirely.
LDRT_P4      = 0xE4B01004           # ldrt r1,[r0],#4   post-index +4, T bit

UNAL = [MOV_R0_10000, ADD_R0_1]     # base 0x10001
ADD_R0_2     = 0xE2800002           # add  r0,r0,#2
ADD_R0_3     = 0xE2800003           # add  r0,r0,#3
LDR_OFF0     = 0xE5901000           # ldr  r1,[r0]   pre-index, offset 0, no wb
UNAL2 = [MOV_R0_10000, ADD_R0_2]    # base 0x10002
UNAL3 = [MOV_R0_10000, ADD_R0_3]    # base 0x10003
ALIGN = [MOV_R0_10000]              # base 0x10000
ZERO = [MOV_R0_0]                   # base 0

#  #364: a page this probe seeds with `put b` and NEVER with `put w`, so its
#  translation entry stays absent and a load from it takes the GENERAL path.
#  That is the whole point -- see the seeding note in run() and the corrected
#  site table above. 0xE3A00802 is `mov r0,#0x20000`, CHECKED THROUGH
#  `unassemble` rather than derived: same rot-8 immediate field as the verified
#  MOV_R0_10000 (0xE3A00801) with imm8 stepped 1 -> 2.
#
#  THE SEEDING MECHANISM, cited from source rather than asserted. A review seat
#  made the fair point that the previous note here stated this mechanism in
#  several places without a citation -- and since the note it replaced was
#  itself inverted, leaning on an uncited claim a second time would repeat the
#  original mistake one level up. So, the four links:
#    put b  -> debugger_cmds.c  memory_rw(..., MEM_WRITE, CACHE_NONE|NO_EXCEPTIONS)
#    put w  -> debugger_cmds.c  store_32bit_word()
#           -> memory.c         cpu->memory_rw(..., MEM_WRITE, CACHE_DATA)
#    insertion gate, memory_rw.c:
#           if (cpu->update_translation_table != NULL && !dyntrans_device_danger
#               && !(ok & MEMORY_NOT_FULL_PAGE) && !no_exceptions)
#                   cpu->update_translation_table(...)
#  So NO_EXCEPTIONS blocks insertion outright, which is why `put b` leaves the
#  page cold and `put w` does not. Note the gate ALSO requires a full page, so
#  a device-backed or partial-page target would stay cold under `put w` too --
#  irrelevant here (plain RAM), but it is the other way this can surprise.
COLD = 0x20000
MOV_R0_20000 = 0xE3A00802           # mov  r0,#0x20000
COLD1 = [MOV_R0_20000, ADD_R0_1]    # base 0x20001, page never warmed
COLD2 = [MOV_R0_20000, ADD_R0_2]    # base 0x20002
COLD3 = [MOV_R0_20000, ADD_R0_3]    # base 0x20003

#  #364: assert nothing this probe warms shares COLD's page. A review seat found
#  the hole: nothing enforced the inequality, so if a future edit moved CODE, SRC
#  or the row-K address onto COLD's page, the program-write loop would warm it
#  BEFORE `pc=` was sent -- and the three cold rows would still PASS, because the
#  fast path yields the same rotated answer. Silent vacuity, in the exact shape
#  this round exists to correct, merely pushed one step away.
#
#  Evaluated ONCE at import, not inside run(): a second review pass pointed out
#  that inside run() it fires 20 times, each time AFTER forking an emulator and
#  sending seeds, so a failure would leak a child and a pty master and would not
#  fire until the first fork. Here it fires before any process exists.
#
#  Failure mode, stated so nobody misdiagnoses it: an AssertionError means no
#  WRITEBACK_RESULT= line, which makes gate_arm.sh call gate_skip, and gate_skip
#  exits EXIT_SKIP -- so every check AFTER the writeback section stops running and
#  gate 14 reports SKIP, which reads like a missing rig image rather than a
#  broken invariant. (That gate_skip swallows already-recorded failures is itself
#  a separate defect, recorded in OUTSTANDING_BUGS.)
#
#  The 4 KB mask is not an assumption: ARM_ADDR_TO_PAGENR shifts by 12,
#  tmp_arm_head.c sets DYNTRANS_PAGESIZE 4096, N_VPH32_ENTRIES is 2^32/2^12, and
#  memory_rw inserts at `vaddr & ~offset_mask` with offset_mask 0xfff for ARM.
#  What this guard does NOT cover, per the notes above: COLD landing on a
#  DM_DYNTRANS_OK device page, which inserts even under NO_EXCEPTIONS.
_PG = ~0xFFF
for _n, _a in (("CODE", CODE), ("CODE end", CODE + 4 * 15),
               ("SRC", SRC), ("SRC end", SRC + 4 * 7),
               ("row K", 0x0), ("testarm stub", 64 * 1048576 - 4096 + 32)):
    assert (_a & _PG) != (COLD & _PG), \
        "%s 0x%x shares COLD's page 0x%x -- it would be warmed" % (_n, _a, COLD)


def _br(cond, frm, to):
    return cond | ((to - (frm + 2)) & 0xFFFFFF)


def once(setup, body):
    """One execution of `body`, then spin.

    #364: this used to claim "Reaches the GENERAL path only." MEASURED FALSE --
    it reaches the general path NEVER. A marker at the top of A__NAME__general
    counted zero hits on all 17 rows. The reason is this probe's own seeding:
    `put w` goes through store_32bit_word -> memory_rw with CACHE_DATA, which
    inserts the page into the translation array, so by the time the guest runs,
    `host_load` is already non-NULL and even a single execution takes the FAST
    path. Use COLD1/2/3 for a general-path row -- those pages are seeded with
    `put b`, which uses CACHE_NONE | NO_EXCEPTIONS and does not insert.
    """
    return list(setup) + list(body) + [SPIN]


def loop10(setup, body):
    """`body` ten times, counted in r3 so the count cannot depend on r0.

    #364: this used to claim iteration 1 takes the general path and iterations
    2+ the fast one, i.e. "one row, both writeback sites". MEASURED FALSE -- the
    page is ALREADY in the translation array before the guest runs, because the
    probe seeds it with `put w`. Every iteration takes the fast path, and the
    marker count for these rows is zero like all the others. One row, ONE site.
    """
    prog = list(setup) + [MOV_R3_0]
    top = len(prog)
    prog += list(body) + [ADD_R3_1, CMP_R3_10]
    br = len(prog)
    prog += [_br(0x1A000000, br, top), SPIN]      # bne -> top
    return prog


def warmed(body):
    """Two passes, base RE-SEEDED each pass, so pass 2 is still unaligned.

    Without the re-seed the pre-index row self-heals: pass 1 leaves an ALIGNED
    base, and pass 2 then has nothing to discriminate.

    #364: this used to claim pass 2 is "the only execution in this whole set
    that reaches the fast pre-index site". MEASURED FALSE in the other direction
    from once()/loop10 -- BOTH passes reach it, because the probe's `put w`
    seeding warms the page before pass 1. The re-seed is still load-bearing for
    the reason above; only the site claim was wrong.
    """
    prog = [MOV_R3_1]
    top = len(prog)
    prog += UNAL + list(body) + [SUBS_R3_1]
    br = len(prog)
    prog += [_br(0x5A000000, br, top), SPIN]      # bpl -> top
    return prog


#  #364: the column is `%-32s` followed by TWO LITERAL SPACES in the format
#  string, not `%-34s` as this note used to say -- a review seat caught the
#  discrepancy. It matters that the two spaces are literal: they are emitted
#  unconditionally, so even a name that filled the whole 32-column field would
#  still satisfy a two-space gate pattern. The longest name here is 26 chars
#  ("A wb regofs post1 unal x10"); a draft of this very note said 24, which is
#  the length of the six `rot word` names -- corrected in review, and worth
#  correcting rather than shrugging at in a note whose whole subject is being
#  exact about this trap.
#  Names stay well inside that column, so a gate check of
#  the form "<name>  *DISC" always sees at least two spaces. A name as long as
#  its column makes such a check UNSATISFIABLE -- shipped once before.
ROWS = [
    # name, kind, program, register, buggy, arch
    ("A wb word post1 unal x10", "DISC",
     loop10(UNAL, [LDR_P1]), "r0", 0x10001, 0x1000B),
    ("A wb word post1 algn x10", "DISC",
     loop10(ALIGN, [LDR_P1]), "r0", 0x10001, 0x1000A),
    ("A wb word post4 unal", "DISC",
     once(UNAL, [LDR_P4]), "r0", 0x10004, 0x10005),
    ("A wb word pre4 unal gen", "DISC",
     once(UNAL, [LDR_PRE4W]), "r0", 0x10004, 0x10005),
    ("A wb word pre4 unal fast", "DISC",
     warmed([LDR_PRE4W]), "r0", 0x10004, 0x10005),
    ("A wb word postneg4 unal", "DISC",
     once(UNAL, [LDR_M4]), "r0", 0x0000FFFC, 0x0000FFFD),
    ("A wb store post1 unal x10", "DISC",
     loop10(UNAL, [STR_P1]), "r0", 0x10001, 0x1000B),
    ("A wb regofs post1 unal x10", "DISC",
     loop10(UNAL + [MOV_R2_1], [LDR_POST_R2]), "r0", 0x10001, 0x1000B),
    ("A wb halfword post1 unal", "DISC-M",
     once(UNAL, [LDRH_P1]), "r0", 0x10001, 0x10002),
    ("A wb word post4 algn", "PIN",
     once(ALIGN, [LDR_P4]), "r0", 0x10004, 0x10004),
    ("A wb algn load data", "PIN",
     once(ALIGN, [LDR_P4]), "r1", 0x11223344, 0x11223344),
    ("A wb byte post1 unal", "PIN",
     once(UNAL, [LDRB_P1]), "r0", 0x10002, 0x10002),
    ("A wb word pre4 no wb", "PIN",
     once(ALIGN, [LDR_PRE4]), "r0", 0x10000, 0x10000),
    ("A wb wrap from zero", "PIN",
     once(ZERO, [LDR_M4]), "r0", 0xFFFFFFFC, 0xFFFFFFFC),

    #  #362: an unaligned word LOAD returns the aligned word ROTATED RIGHT by
    #  8 * addr[1:0] (DDI 0100I A2.8, A4.1.23). This template masked and never
    #  rotated. The word at 0x10000 is 0x11223344, so the three offsets owe
    #  0x44112233, 0x33441122 and 0x22334411, and the "buggy" column is the
    #  unrotated word -- which is what the pre-fix build returned in all three.
    #
    #  These rows IDENTIFY the model rather than merely failing an expectation:
    #  mask-only, rotate, and the ARMv6 U == 1 true-unaligned access are pairwise
    #  distinct at every nonzero offset, so a wrong answer says WHICH model is
    #  implemented. Measured MASK-only on all three pre-fix, ROTATE post-fix.
    #
    #  Offset 0 is deliberately absent: rotation by zero is the identity, so such
    #  a row could never fail, and the aligned case is already pinned elsewhere.
    ("A wb rot word unal plus1", "DISC",
     once(UNAL, [LDR_OFF0]), "r1", 0x11223344, 0x44112233),
    ("A wb rot word unal plus2", "DISC",
     once(UNAL2, [LDR_OFF0]), "r1", 0x11223344, 0x33441122),
    ("A wb rot word unal plus3", "DISC",
     once(UNAL3, [LDR_OFF0]), "r1", 0x11223344, 0x22334411),

    #  #364: the same three offsets, from a page seeded ONLY with `put b`, so the
    #  translation entry is absent and the load takes the GENERAL path. These are
    #  the first rows in this file to enter `A__NAME__general` -- see the
    #  corrected site table at the top.
    #
    #  Why they are not redundant with the three rows above, which is the whole
    #  finding: with `#362`'s general-path rotation neutralised and its fast-path
    #  rotation left intact, the rows above stayed GREEN and the whole of gate 14
    #  passed at 261 checks. These three go red, reading the unrotated
    #  0x11223344. The two triples differ in exactly one thing -- the seeding
    #  width of the page they read -- which is what pins the mechanism: on ONE
    #  binary, `put b` gave ls_general=1 and the mask-only answer while `put w`
    #  gave ls_general=0 and the rotated answer.
    ("A wb rot word cold plus1", "DISC",
     once(COLD1, [LDR_OFF0]), "r1", 0x11223344, 0x44112233),
    ("A wb rot word cold plus2", "DISC",
     once(COLD2, [LDR_OFF0]), "r1", 0x11223344, 0x33441122),
    ("A wb rot word cold plus3", "DISC",
     once(COLD3, [LDR_OFF0]), "r1", 0x11223344, 0x22334411),

    #  #365: the first two rows anywhere in the battery that DISCRIMINATE #357's
    #  general-path correction. The distinction matters and cost a refuted
    #  prediction to find: the two general writeback SITES were already being
    #  REACHED before this round -- the strlen probe's `ldrb r3,[r4,#1]!` is
    #  P=1/W=1 and takes the general pre-index arm on each new page, and the
    #  fold-marker probe's `copyin cold` / `copyout cold` arms are six ldrt/strt
    #  with the is_userpage bit left clear, and their r0/r1-advanced-by-24
    #  witness IS a writeback assertion. Deleting both statements turns 8 gate
    #  checks red in THOSE sections.
    #
    #  #366 corrected a detail this comment got wrong when it shipped: it said
    #  ALL SIX of those ldrt/strt run in A__NAME__general. Only the FIRST does.
    #  The general path's own memory_rw insert SETS the user bit --
    #  cpu_dyntrans.c does `if (useraccess) is_userpage[index >> 5] |= 1 <<
    #  (index & 31)`, and the found-entry arm clears-then-sets it -- so the
    #  second ldrt on that page finds the bit set and takes the FAST path. The
    #  fold-marker probe's own docstring already said as much ("only pass 2 and
    #  later can fold"). The count is ONE general entry per cold arm, not six.
    #  Nothing else here changes: the arms still reach the site, and the 8-red
    #  measurement stands.
    #
    #  But nothing DISCRIMINATED the mask. Rebuild with the faithful pre-#357
    #  bug -- the general writeback re-masked, `addr` instead of `wb_addr`, fast
    #  pair intact -- and the whole of gate 14 passed at 264 checks, 0 failures.
    #  Every row that reached those sites was blind to it: `ldrb` has
    #  datalen 1, so `addr &= ~(datalen - 1)` is the IDENTITY, and the fold arms
    #  use aligned bases 0x10000/0x11000 where masked and unmasked agree. So the
    #  honest statement is "undiscriminated", not "unreached" -- and a row that
    #  reaches a statement without discriminating its correction measures nothing
    #  about it.
    #
    #  Measured on four builds. Pristine: both ok. General writeback DELETED:
    #  both red at the un-incremented base. General writeback RE-MASKED (the real
    #  #357 bug): both red at exactly the predicted masked values. POST-index
    #  only: the ldrt row red and the cold pre4 row green, which separates the
    #  two sites -- as it must, since P=0/W=1 and P=1/W=1 are distinct
    #  translation units each compiling only its own #ifdef arm.
    ("A wb word ldrt post4 unal", "DISC",
     once(UNAL, [LDRT_P4]), "r0", 0x10004, 0x10005),
    ("A wb word cold pre4 unal", "DISC",
     once(COLD1, [LDR_PRE4W]), "r0", 0x20004, 0x20005),
]


def run(prog, regs):
    stub = "/tmp/r104c_stub.bin"
    with open(stub, "wb") as f:
        f.write((0xE1A00000).to_bytes(4, "little"))
    pid, fd = pty.fork()
    if pid == 0:
        #  -T halts on a non-existent memory access rather than logging one
        #  host line per access: a run that goes wrong stops instead of
        #  flooding the pty and making the row host-speed dependent.
        os.execvp(BIN, [BIN, "-V", "-A", "-T", "-E", "testarm", "-M", "64",
                        "0x%x:%s" % (CODE, stub)])
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait_from(mark, timeout=30):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if len(buf) > mark and buf[mark:].rstrip().endswith("GXemul>"):
                return True
        return False

    def send(sx):
        mark = len(buf)
        b = (sx + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        return wait_from(mark)

    if not wait_from(0, 60):
        os.kill(pid, 9)
        os.waitpid(pid, 0)
        return None

    #  Four distinct bytes per word, so a byte-order or rotation change would
    #  be unmistakable rather than a plausible-looking value.
    for i in range(8):
        send("put w 0x%x, 0x%08x" % (SRC + 4 * i, 0x11223344 + i))
    send("put w 0x0, 0x99887766")        # row K reads from address 0

    #  #364: the COLD page, laid down a BYTE AT A TIME on purpose. `put b` uses
    #  CACHE_NONE | NO_EXCEPTIONS, and translation-array insertion is gated on
    #  `!no_exceptions`, so this page is NOT warmed and a load from it takes the
    #  general path -- which no other row in this file does. `put w` here would
    #  silently convert these rows into three more fast-path rows.
    #
    #  Bytes ascending so the little-endian word reads 0x11223344, matching the
    #  `put w` pages above: 0x44 at COLD+0 through 0x11 at COLD+3. Do NOT switch
    #  the whole probe to `put b` -- that would move all 17 existing rows to the
    #  general path and DELETE the fast-path coverage, which is currently the
    #  only coverage those four sites have.
    for i, b in enumerate((0x44, 0x33, 0x22, 0x11)):
        send("put b 0x%x, 0x%02x" % (COLD + i, b))

    for i, iw in enumerate(prog):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    send("pc=0x%x" % CODE)

    #  The programs finish in microseconds and then spin at `b .`, so the two
    #  second wait is ~six orders of magnitude of margin: the registers are
    #  settled long before the interrupt, and no row's value depends on how far
    #  execution got. The iteration count lives in r3, not in elapsed time.
    cmark = len(buf)
    os.write(fd, b"continue\n")
    t = time.time()
    while time.time() - t < 2.0:
        rd(0.3)
    if not (len(buf) > cmark and buf[cmark:].rstrip().endswith("GXemul>")):
        os.write(fd, b"\x03")
        wait_from(cmark, 15)

    out = {}
    for rn in regs:
        mark = len(buf)
        send("print %s" % rn)
        #  `print <reg>` answers with the bare value on its own line
        #  ("0x11223344"), NOT "r0 = 0x...". An earlier revision grepped for
        #  the "r0 = " form and scored every row DEAD -- a broken probe that
        #  looks exactly like a broken emulator.
        m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
        if m:
            out[rn] = int(m.group(1), 16)

    #  #367: how many times this row entered A__NAME__general, read from the
    #  emulator's own counter via `tlbdump`. This is the round that stopped path
    #  attribution being a claim in a comment: which path a row takes was wrong
    #  three times running (#364's inverted seeding note, #364's draft
    #  mis-attributing a writeback site to an offset form that compiles none, and
    #  #365 finding the sites reached but undiscriminated), and each was
    #  rediscovered with a throwaway marker and a scratch build.
    #
    #  PULL, not push: `tlbdump` prints only when asked, so it cannot disturb the
    #  rows elsewhere in this battery that assert an ABSENCE of output, and it
    #  cannot flood a free-running guest. It is read AFTER the registers so a
    #  parse failure here cannot cost a register value.
    #
    #  A missing line is DEAD, never 0 -- 0 is the expected value for every warm
    #  row, so defaulting to it would make a lost read indistinguishable from a
    #  correct answer, which is the defect class this battery keeps finding.
    mark = len(buf)
    send("tlbdump")
    m = re.search(r"arm\.ls_general\s*=\s*(\d+)", buf[mark:])
    out["_lsgen"] = int(m.group(1)) if m else None

    try:
        os.write(fd, b"quit\n")
        time.sleep(0.2)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    return out


#  Gate-convention output: one "<name>  ... ok" / "... FAIL" line per row, a
#  RESULT= line, and a CONTROL= line proving the instrument is LIVE rather than
#  merely quiet. The control is the loaded-data row: r1 starts at 0, so a
#  distinctive NONZERO value proves the guest really executed and really loaded,
#  which is the check this project adds after a committed row was found to be
#  measuring the wrong register field -- a wrong field reads 0, and a row that
#  accepts 0 accepts that mistake by accident.
print("=== #19: ARM load/store base writeback (pre/post-index) ===")
print("    buggy = masked base + offset ; arch = unmasked (A5.2.5 / A5.2.8)")
print("    DISC-M pins the A5.3.6 pseudocode model, not a silicon mandate")

#  #367: the expected number of A__NAME__general entries per row. Derived from
#  the template's control flow, NOT guessed, because a wrong expectation here
#  becomes a new false red:
#
#      count = (page x needed-permission) upgrade events + T-form first touches
#
#  The general path's own memory_rw SELF-WARMS -- it inserts, setting host_load
#  unconditionally, host_store iff the access was a write, and the is_userpage
#  bit iff it was a user access. So:
#    * every `put w`-seeded row is 0, including all ten iterations of the x10
#      rows and both passes of the re-seeded row: the page is warm before the
#      guest runs a single instruction;
#    * the four `put b`-seeded cold rows are 1 -- one entry, which then warms;
#    * the `ldrt` T-form row is 1 even though its page IS warm, because the
#      is_userpage test precedes the page test and a kernel `put w` insert never
#      sets that bit. Its own general call then SETS it, which is why a SECOND
#      ldrt on that page would be fast.
#  Non-obvious cases for whoever adds rows: a COLD x10 row is 1, not 0 and not
#  10 -- iteration 1 warms via the general path's own insert. It is 10 only where
#  insertion is BLOCKED (a device page, a partial page, MMU-on unmapped). A cold
#  row doing a load then a store on one page is 2, because the load's insert
#  leaves host_store NULL.
LSGEN = {
    "A wb rot word cold plus1": 1,
    "A wb rot word cold plus2": 1,
    "A wb rot word cold plus3": 1,
    "A wb word cold pre4 unal": 1,
    "A wb word ldrt post4 unal": 1,
}

ngot = 0
control = "FAIL"
lsgot = 0
lswant = 0
for name, kind, prog, reg, buggy, arch in ROWS:
    got = run(prog, [reg])
    if got is None or reg not in got:
        print("%-32s  %-6s DEAD  FAIL" % (name, kind))
        continue
    v = got[reg]
    ok = (v == arch)
    ngot += ok
    if name == "A wb algn load data" and v == 0x11223344:
        control = "OK"
    print("%-32s  %-6s %s=0x%08x want 0x%08x (buggy 0x%08x)  %s"
          % (name, kind, reg, v, arch, buggy, "ok" if ok else "FAIL"))

    #  #367: the path assertion, printed as its own row so the gate can name it.
    #
    #  The name gets a " path" SUFFIX, and that is load-bearing rather than
    #  cosmetic. The gate greps named rows as "^<name>  .*ok$" -- TWO spaces --
    #  so a path row printed under the bare name would give every one of the 22
    #  existing named checks a count of 2 where it expects 1, turning the whole
    #  section red. The suffix puts a single space after the base name, which
    #  that pattern cannot match, so the value checks stay exact and the path
    #  rows get their own names. The longest becomes 31 chars
    #  ("A wb regofs post1 unal x10 path"), still inside the %-32s column, and
    #  the format's two literal spaces keep the gate pattern satisfiable
    #  regardless of padding.
    lswant += 1
    exp = LSGEN.get(name, 0)
    seen = got.get("_lsgen")
    lsok = (seen is not None and seen == exp)
    lsgot += lsok
    print("%-32s  %-6s general=%s want %d  %s"
          % (name + " path", "PATH", "unread" if seen is None else seen, exp,
             "ok" if lsok else "FAIL"))

print("WRITEBACK_CONTROL=%s" % control)
print("WRITEBACK_RESULT=%d/%d" % (ngot, len(ROWS)))
print("LSGEN_RESULT=%d/%d" % (lsgot, lswant))
