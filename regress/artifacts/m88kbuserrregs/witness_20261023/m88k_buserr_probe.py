#!/usr/bin/env python3
"""m88k_buserr_probe.py -- rung-3 WITNESS (pre-fix) and detector base for m88kbuserrregs (TRIAGE.md T36).

REVISION 1 (2026-10-23), 24 rows.  Written by the measuring seat of T36's REPRODUCE step (test-first, before any
edit).  It is to move to regress/ as the round's detector base; the round re-derives the rows and this contract
against its own diff (PRETABLE, floor (a)-(d), the ask-again) -- nothing here is a kill-table measurement.

DEFECT (HEAD 66920157; both sites are the 0.7.0 import).  When a guest data load or store reaches a device whose
access function REFUSES it (returns 0 with the cpu still running), src/cpus/memory_rw.c's refused-access arm
(`if (res <= 0 && !no_exceptions)', :603-625) raises the m88k data-access exception (the MEM_M88K block,
:614-623) and writes NOTHING into the data CMMU's P-bus fault status register (PFSR, offset 0x108) or P-bus fault
address register (PFAR, 0x10c) -- its own TODO at :615-619 says "the faulting address should probably be
included somewhere too".  A guest fault handler that reads them sees whatever they held before.  The LUNA probe
address -- src/devices/dev_luna88k.c:624-627, `case 0x3ffffff0' -- writes PFSR = CMMU_PFSR_BERROR << 16 on
cmmu[1] only, writes NO PFAR, and `break's into `return 1' (:930): the access SUCCEEDS, serving 0, and no
exception is raised at all.

WHICH ACCESSES REACH THAT ARM -- a premise correction, measured: only an access a device CLAIMS and REFUSES.  An
access to a physical address NO device claims never enters the device scan's success branch; it falls through to
memory_rw.c:662-713 (`Outside of physical RAM?'), where memory_warn_about_unimplemented_addr() (core/memory.c:
598-655) prints at most a warning -- or, under `-T' (core/main.c:465-466), stops every cpu -- and a read is served
zeros: no exception and no CMMU write, before or after T36's fix (INFO `unclaimed' below, default options).  So the refusing devices used here are ones the in-tree machine description installs
to model absent hardware: mvme187's `unreadable' window and VME population 1.

THE FIX (ruled, not yet written -- regress/artifacts/research_20261022/crit_20261022/CRIT_RULINGS.md row T36, Astra
Q2 in codex_rescrit.txt and Grok Q2 in grok_crit.txt beside it): in the refused-access arm select cmmu[0] for an
instruction access and cmmu[1] for a data access; if that pointer exists, write PFSR = CMMU_PFSR_BERROR << 16
(0x00030000) and PFAR = orig_paddr (the PHYSICAL address saved at memory_rw.c:437 -- not the device-relative
paddr :494 makes); the NULL check wraps the two writes only, the exception stays outside it, and the sibling
CMMU is not cleared (Grok Q2).  The LUNA case returns 0 through that repaired arm, its own PFSR write deleted.

RUNG 3: real MC88100 instructions (ld/st/or/br) through real address decode and real memory_rw, on two
UNMODIFIED in-tree machines: `-E mvme88k -e mvme187 -M 64' (machine_mvme88k.c; vme_default_probe.py's shape) and
`-E luna88k -e luna-88k' (machine_luna88k.c), each started with a 4-byte dummy raw image at 0x10000 (no PROM, no
disk).  An optional third argument names the rig images directory; the LUNA session then runs in
luna_absentcpu_probe.py's rig shape instead (`-e luna-88k -d R:<images>/liveimage-luna88k-raw-20250518.img boot',
cwd = the images directory) -- the two shapes were measured to give identical registers (witness_20261023/
explore1.out cases 5 and 6).  No device_add, no machine edit.  STEPPED sessions feed the debugger on stdin
(vme_default_probe.py's run_piped); no pty plumbing is used, which is why _scratchpad/gxprobe.py (MIPS presets,
installs MIPS stubs on construction) is not.  A synchronous device refusal is visible while stepping; a
FREE-RUNNING run of the exploration program (explore2.py.txt: the same access, the same four seeds, a shorter
preamble without the instruction-CMMU IDR and readbacks) gave the same stale registers (explore2.out case 1), so
the symptom is not a single-step artifact.

THE PROGRAM (every session; only the ACCESS word and its registers differ):
    0x10   or r7,r0,2 ; br H         vector 2 (INSTRUCTION_ACCESS) marker -- VBR is 0 at reset (measured)
    0x18   or r7,r0,3 ; br H         vector 3 (DATA_ACCESS) marker
    CODE   ld r10,r3,0x0             data CMMU IDR           -- DEVICE SIGNATURE (0x00a90000; RAM cannot answer it)
           ld r9,r2,0x0              instruction CMMU IDR    -- the same, for the sibling
           st r20,r3,0x108 / st r21,r3,0x10c / st r22,r2,0x108 / st r23,r2,0x10c
                                     SEED both CMMUs' PFSR and PFAR with four distinct values
           ld r11,r3,0x108 / ld r12,r3,0x10c / ld r17,r2,0x108 / ld r18,r2,0x10c
                                     LIVENESS through the same decode: each seed reads back
           ACCESS                    the access under test (CODE + 0x28)
           or r6,r0,0x1234 ; br H    FALL-THROUGH marker: runs only if the access raised nothing
    H      ld r13,r3,0x108 / ld r14,r3,0x10c / ld r15,r2,0x108 / ld r16,r2,0x10c
                                     the four registers AFTER the access, read by GUEST LOADS in the handler
           or r31,r0,0x5678 ; br .   the handler ran to its end
  So the reads happen on BOTH paths: a refused access enters vector 3 (or 2) and branches to H; an access that
  raises nothing falls through to the same H.  r7 says which vector was entered, r6 whether it fell through, and
  `reg 0,0' gives SXIP (the faulting instruction | V) and DMA0 (the faulting word address) -- the attribution
  control: the exception came from THIS access.  19 steps reach H's `br .' on either path.  One fault per session:
  the exception sets PSR.SFRZ, and a second fault while it is set becomes ERROR (cpu_m88k.c:811-819).

ADDRESSES AND OFFSETS (each cited; the probe uses literals on purpose, so a header edit cannot silently move them):
  CMMU register offsets -- src/include/thirdparty/m8820x.h:60 CMMU_IDR (0x000 / 4), :65 CMMU_PFSR (0x108 / 4),
      :66 CMMU_PFAR (0x10c / 4); dev_m8820x.c:257-258 serves a read as regs[relative_addr / 4]; :437-461 STORES a
      guest write to PFSR/PFAR (which is what makes the seed-and-readback liveness possible); IDR is never stored
      (:262-272).  BERROR: m8820x.h:125 (CMMU_PFSR_BERROR 3), the field extract :123 ((pfsr >> 16) & 7).
  IDR seed 0x00a90000 = (M88200_ID << 21) | (9 << 16), M88200_ID 5 at m8820x.h:152 -- dev_mvme187.c:139 and :151,
      dev_luna88k.c:949 and :960.
  mvme187 CMMUs: data 0xfff7f000, instruction 0xfff77000 (mvme187.h:57, :56); attached at dev_mvme187.c:140-142
      (addr2=0 -> cmmu_nr 0) and :154-156 (addr2=1); cmmu[0] = instruction, cmmu[1] = data (dev_mvme187.c:136-137,
      :148-149; dev_m8820x.c:540-543; memory_m88k.c:112 uses the same index).
  luna-88k CPU-0 CMMUs: data 0xfff06000, instruction 0xfff07000 (luna88k_board.h:163 CMMU_D0, :162 CMMU_I0;
      attached by add_cmmu_for_cpu(devinit, 0, CMMU_I0, CMMU_D0) at dev_luna88k.c:1074, :934-965).
  refused device #1 -- `unreadable addr=0xfff46000 len=0x1000' (machine_mvme88k.c:106, the ie0 placeholder):
      dev_unreadable.c's access function is `return 0;'.  The probe uses 0xfff46010, so the device-relative
      offset (0x10) differs from the physical address.
  refused device #2 -- the VME2 window at VME2_BASE 0xfff40000 (mvme88k_vme.h:44; machine_mvme88k.c:95-96):
      offset 0x90 is population 1 of #568 (vmedefaultkill), dev_vme.c:207-220 `default:' returns 0.  The probe
      uses 0xfff40090 (device-relative 0x90).
  accepted device access (the accept control) -- VME VBR at 0xfff40088 (mvme88k_vme.h:80 VME2_VBR 0x0088), served
      by its cased arm (dev_vme.c:144) from DEVINIT's seed VME2_SET_VBR0(6) + VME2_SET_VBR1(7) = 0x67000000
      (dev_vme.c:238-239).
  the LUNA probe address 0x3ffffff0 -- LUNA88K_REGISTERS_BASE (dev_luna88k.c:78; the device registered there at
      :990-992), `case 0x3ffffff0' at :624-627.
  vectors -- cpu_m88k.h:202-203 (INSTRUCTION_ACCESS 2, DATA_ACCESS 3); pc = VBR + 8 * vector (cpu_m88k.c:863);
      SXIP = pc | M88K_XIP_V (cpu_m88k.c:837; m88k_psl.h:90 V = 0x2), | M88K_XIP_E for an instruction access
      (:859-860); DMT0/DMD0/DMA0 copied from the data unit on DATA_ACCESS (:908-912).

ROWS, each with the mutant it is DESIGNED to catch and the channel that differs under it.  These are DATED
PREDICTIONS (2026-10-23) read off the ruled design; no mutant has been built.  The pre-fix HEAD is the one
measured "mutant": the symptom rows below are its channels.
  CONTROL rows -- DEFINITION (vme_default_probe.py's): a row whose role is a PREREQUISITE of the scored rows -- an
  apparatus, medium or device-signature proof.  CONTROL=FAIL means a prerequisite failed and claims NO cause.
    neg apparatus  a bogus subtype `187': no machine, no register dump -- the session oracle MUST be able to go red
    mv devsig      mvme187 data + instruction CMMU IDR = 0x00a90000 each (RAM, or no device, reads 0)
    mv cmmu rt     mvme187: the four seeds read back through the same decode (the accept session's)
    luna devsig    luna-88k: the same two IDRs
    luna cmmu rt   luna-88k: the four seeds read back (the LUNA session's)
    unasm          every placed word re-read by the disassembler; LITERAL count
  Every scored row additionally reports `nodev ...', `readback ...' or `handler ...' instead of a value when ITS
  OWN session failed a prerequisite, so a red row never claims a cause it did not observe.
  accept side (mvme187, `ld r4,r5,0' at VME VBR 0xfff40088 -- an ACCEPTED device access)
    ok route       fall-through, r4 = 0x67000000.  Mutant: the refused-access arm's condition widened so an
                   accepted access faults (`res <= 0' -> `res <= 1') -- the route reads v3
    ok regs        all four seeds survive an accepted access.  Mutant: the two writes placed OUTSIDE `res <= 0'
                   (every device access writes metadata) -- the data seeds change
  generic arm, data LOAD (mvme187, `ld r4,r5,0' at 0xfff46010, the unreadable window)
    uld route      vector 3, SXIP = CODE + 0x28 | V, DMA0 = 0xfff46010, r4 keeps its sentinel.  Mutant: the
                   exception DROPPED -- the row reads fall-through or the handler is never reached.  NOT the
                   exception moved inside the NULL check: both CMMUs exist here, so that one needs an absent CMMU
                   (NOT CLAIMED).  GREEN on HEAD (the exception is raised today; the fix must keep it)
    uld pfsr       data PFSR = 0x00030000.  HEAD: the seed 0x5a5a5a5a.  Mutants: no write (HEAD); raw 3 instead of
                   3 << 16; the write on cmmu[0] instead of cmmu[1]
    uld pfar       data PFAR = 0xfff46010.  HEAD: the seed 0x13572468.  Mutants: no write (HEAD); the
                   device-RELATIVE paddr (0x10); a PFSR-only repair; cmmu[0] instead of cmmu[1]
    uld icmmu      instruction CMMU PFSR/PFAR keep their seeds.  Mutants: the write on BOTH CMMUs, or cmmu[0]
                   only; the sibling cleared as the translation-fault path does (memory_m88k.c:383-384)
  generic arm, data STORE (mvme187, `st r8,r5,0' at 0xfff46010, r8 = 0xa5a5a5a5)
    ust route / ust pfsr / ust pfar / ust icmmu    the same four channels for the store direction.  Mutant: a
                   repair conditioned on the direction (`writeflag == MEM_READ') -- the store pfsr/pfar read seeds
  generic arm, a SECOND refusing device (mvme187, `ld r4,r5,0' at 0xfff40090, VME population 1, #568's FAULT)
    vme route / vme pfsr / vme pfar / vme icmmu    the same four channels; PFAR = 0xfff40090 (device-relative 0x90).
                   Mutant: a repair keyed to one device (by name, base or length) -- one device's rows read seeds
  the LUNA probe address (luna-88k, `ld r4,r5,0' at 0x3ffffff0)
    luna route     vector 3, SXIP = CODE + 0x28 | V, DMA0 = 0x3ffffff0, r4 keeps its sentinel.  HEAD: fall-through,
                   SXIP 0, DMA0 0, r4 = 0 (the access is SERVED).  Mutant: the case left returning 1
    luna pfsr      data PFSR = 0x00030000.  GREEN on HEAD (the case's own write) -- pins that deleting that write
                   while routing through the generic arm keeps the status.  Mutant: the case's write deleted and
                   the route left at `return 1'
    luna pfar      data PFAR = 0x3ffffff0.  HEAD: the seed 0x13572468.  Mutants: the case's PFSR-only body kept
                   (no PFAR); the device-relative paddr (0x0 here: the access is AT the device's base)
    luna icmmu     the instruction CMMU keeps its seeds
  INFO (unscored): an INSTRUCTION fetch refused by the same unreadable window (mvme187, `jmp r5' to 0xfff46010),
                   and a load from an UNCLAIMED physical address (mvme187, `ld r4,r5,0' at 0x10000000: past the
                   64 MB of RAM, below every device).  Printed, never scored -- see NOT CLAIMED and the premise
                   correction above.

SYMPTOM CLASSIFICATION (the "did it fail for the reason under test?" line): the eight rows that the fix changes
(uld/ust/vme pfsr and pfar, luna route, luna pfar) are each classified STALE (got is exactly the probe's own seed,
or, for luna route, the fall-through with r4 served 0), FIXED (got == want) or OTHER.  M88K_BUSERR_SYMPTOM prints
PRESENT n/8 when all eight are STALE, ABSENT when all eight are FIXED, else MIXED with the list.  Neither data seed
carries BERROR in the field the guest tests: (0x5a5a5a5a >> 16) & 7 == 2 and (0x2468ace0 >> 16) & 7 == 0, so a
stale seed cannot pass for a recorded bus error even under the guest's own looser extract.

CONTRACT (clause e).  DESIGNED to catch: the pre-fix defect (measured: witness_20261023/WITNESS_headbin.out) and
the predicted mutants named per row above.  NOT CLAIMED, so a later escape is outside the contract rather than an
argument:
  * translation ON.  Every session runs with the CMMUs' APR invalid (physical = virtual, memory_m88k.c:130-144),
    so a repair that writes the VIRTUAL address into PFAR is indistinguishable here (Astra Q2 names "translated VA
    differing from PA" as owed -- the round's);
  * an ABSENT CMMU (the NULL check): mvme187 and luna-88k always attach both CMMUs, so a repair without the check,
    or with the exception moved inside it, passes every row (route rows catch only a DROPPED exception);
  * no_exceptions callers (the debugger's put/dump/unassemble never reach a DM_DEFAULT handler, memory_rw.c:584);
  * INSTRUCTION-access refusals.  Measured, not scored: STEPPED, the debugger's own disassembly pre-read
    (cpu_dyntrans.c:287-290, CACHE_INSTRUCTION) raises vector 2 and the vector runs -- an artifact of single-step;
    FREE-RUNNING, the fetch takes vector 2 (SXIP 0xfff46013) and then to_be_translated()'s read failure
    (cpu_m88k_instr.c:2989-2993) reaches `bad:' and STOPS the cpu with "UNIMPLEMENTED instruction at 0x10"
    (cpu_dyntrans.c:2002-2014; explore2.out case 2), so no guest handler can read cmmu[0] after an instruction
    refusal on HEAD.  The cmmu[0] cell is the round's to build;
  * an UNCLAIMED physical address (no device at all): it raises nothing and is served zeros before and after the
    ruled fix (memory_rw.c:662-713; INFO `unclaimed') -- a different path, not T36's arm;
  * sub-word accesses and byte addresses (PFAR = the byte address vs the word address DMA0 holds): every access
    here is a word at a word-aligned address;
  * more than one cpu (luna-88k `-n 2..4': the per-cpu CMMU selection), xmem, the 88110 (mvme197);
  * the OpenBSD reader itself (trap.c's `(dpfsr >> 16) & 7 == 3' and badaddr()'s eh.S recovery, which bypasses the
    PFSR read -- CRIT_RULINGS.md T36): no guest kernel runs here; a boot is the stronger witness;
  * the sibling-CMMU premise of the icmmu rows (not cleared) is the ruling's (Grok Q2); a round that decides the
    data-side bus error should clear cmmu[0]'s PFSR, as the translation-fault path does, changes those wants;
  * PFSR / PFAR bits beyond the exact values written (no partial-value or field-only row);
  * anything about real MC88200 timing or the P-bus.

TEST-FIRST SHAPE: on the committed HEAD the eight symptom rows are red -- the six generic pfsr/pfar rows each read
back the probe's own seed, `luna route' falls through with the access served 0 and `luna pfar' reads its seed
(M88K_BUSERR_SYMPTOM=PRESENT 8/8) -- while the six controls and the other ten scored rows are green.  After the
round's fix the same script is expected all green (M88K_BUSERR_SYMPTOM=ABSENT); that half is OWED to the round
(witness clause (i)), not measured here.

usage: m88k_buserr_probe.py <gxemul> [label] [images-dir]
       M88K_BUSERR_DUMP=<dir> also writes every session's raw debugger transcript to <dir>/<session>.txt
       (unset: nothing is written; the rows and lines below are identical either way).
Sentinel: M88K_BUSERR_PROBE_DONE (plus M88K_BUSERR_RESULT=n/N, M88K_BUSERR_CONTROL=OK|FAIL,
M88K_BUSERR_SYMPTOM=PRESENT n/8|ABSENT|MIXED ...)
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: m88k_buserr_probe.py <gxemul> [label] [images-dir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
IMAGES = sys.argv[3] if len(sys.argv) > 3 else None
DUMP = os.environ.get("M88K_BUSERR_DUMP") or None
#  A private dummy file: a shared /tmp path once let two concurrent runs race on it (vme_default_probe.py).
_TMPDIR = tempfile.mkdtemp(prefix="m88k_buserr_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
with open(DUMMY, "wb") as _f:
    _f.write(b"\x00\x00\x00\x00")

CODE = 0x00010000
H = 0x00010100              # the reading handler both paths reach
VEC_IACC = 0x10             # VBR 0 + 8 * M88K_EXCEPTION_INSTRUCTION_ACCESS (2)
VEC_DACC = 0x18             # VBR 0 + 8 * M88K_EXCEPTION_DATA_ACCESS (3)
SENT = 0xdeadbeef
FALL = 0x1234               # r6: the access raised nothing
LIVE = 0x5678               # r31: the handler ran to its end
D_PFSR_SEED = 0x5a5a5a5a    # (>> 16) & 7 == 2: not BERROR under the guest's extract
D_PFAR_SEED = 0x13572468
I_PFSR_SEED = 0x2468ace0    # (>> 16) & 7 == 0
I_PFAR_SEED = 0x0badf00d
SEEDS = (D_PFSR_SEED, D_PFAR_SEED, I_PFSR_SEED, I_PFAR_SEED)
IDR = (5 << 21) | (9 << 16)                 # 0x00a90000: (M88200_ID << 21) | (9 << 16)
BERROR = 3 << 16                            # CMMU_PFSR_BERROR << 16 = 0x00030000
OFF_IDR, OFF_PFSR, OFF_PFAR = 0x000, 0x108, 0x10c
MV_DCMMU, MV_ICMMU = 0xfff7f000, 0xfff77000   # MVME187_SBC_CMMU_D / _I
LU_DCMMU, LU_ICMMU = 0xfff06000, 0xfff07000   # CMMU_D0 / CMMU_I0
UNREAD = 0xfff46010         # inside `unreadable addr=0xfff46000 len=0x1000': device-relative 0x10
VME = 0xfff40000            # VME2_BASE
VME_P1 = VME + 0x90         # population 1 (#568's FAULT): device-relative 0x90
VME_VBR = VME + 0x88        # VME2_VBR, a CASED register: an accepted access
VBR_SEED = 0x67000000       # dev_vme.c DEVINIT: VME2_SET_VBR0(6) + VME2_SET_VBR1(7)
LUNA_PROBE = 0x3ffffff0     # LUNA88K_REGISTERS_BASE == the `case 0x3ffffff0' label
UNCLAIMED = 0x10000000      # INFO only: past mvme187's 64 MB, below its lowest device (0xff780000)
STVAL = 0xa5a5a5a5
ACCESS_PC = CODE + 4 * 10
SXIP_DATA = ACCESS_PC | 0x2               # M88K_XIP_V
H_END = H + 4 * 5
NSTEPS = 19                               # 10 + access + 2 (vector or fall-through) + 6 handler
PROMPT = "GXemul> "
RIG_IMG = "liveimage-luna88k-raw-20250518.img"


# ------------------------------------------------------------------- encodings
class Ins(object):
    __slots__ = ("word", "mnem", "ops")

    def __init__(self, word, mnem, ops):
        self.word, self.mnem, self.ops = word, mnem, ops


def enc(op26, rd, rs1, imm):
    assert 0 <= op26 < 64 and 0 <= rd < 32 and 0 <= rs1 < 32 and 0 <= imm <= 0xffff
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | imm


def LD(rd, rs1, off):       # op26 0x05 (vme_default_probe.py's table)
    return Ins(enc(0x05, rd, rs1, off), "ld", "r%d,r%d,0x%x" % (rd, rs1, off))


def ST(rs, rs1, off):       # op26 0x09
    return Ins(enc(0x09, rs, rs1, off), "st", "r%d,r%d,0x%x" % (rs, rs1, off))


def OR_I(rd, rs1, imm):     # op26 0x16; the disassembler prints this immediate in hex
    assert rd != 0
    return Ins(enc(0x16, rd, rs1, imm), "or", "r%d,r%d,0x%x" % (rd, rs1, imm))


def BR_TO(frm, to):         # op26 0x30, d26 = (to - frm) / 4
    return Ins(0xc0000000 | (((to - frm) >> 2) & 0x3ffffff), "br", "0x%08x" % to)


def BR_SELF():              # d26 = 0; the operand is filled in on placement
    return Ins(0xc0000000, "br", None)


def JMP(rs2):               # jmp (rS2) = 0xf400c000 | rs2 (luna88kprom.c's `jmp (r1)' = 0xf400c001)
    return Ins(0xf400c000 | rs2, "jmp", "(r%d)" % rs2)


def blocks_for(access):
    vec = [(VEC_IACC, [OR_I(7, 0, 2), BR_TO(VEC_IACC + 4, H)]),
           (VEC_DACC, [OR_I(7, 0, 3), BR_TO(VEC_DACC + 4, H)])]
    code = [LD(10, 3, OFF_IDR), LD(9, 2, OFF_IDR),
            ST(20, 3, OFF_PFSR), ST(21, 3, OFF_PFAR), ST(22, 2, OFF_PFSR), ST(23, 2, OFF_PFAR),
            LD(11, 3, OFF_PFSR), LD(12, 3, OFF_PFAR), LD(17, 2, OFF_PFSR), LD(18, 2, OFF_PFAR),
            access,
            OR_I(6, 0, FALL), BR_TO(CODE + 4 * 12, H)]
    assert CODE + 4 * code.index(access) == ACCESS_PC
    hnd = [LD(13, 3, OFF_PFSR), LD(14, 3, OFF_PFAR), LD(15, 2, OFF_PFSR), LD(16, 2, OFF_PFAR),
           OR_I(31, 0, LIVE), BR_SELF()]
    assert H + 4 * (len(hnd) - 1) == H_END
    return vec + [(CODE, code), (H, hnd)]


# ------------------------------------------------------------------- sessions
def hx(v):
    return "absent" if v is None else "0x%x" % v


def argv_for(machine):
    if machine == "mvme187":
        return [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64", "0x%x:%s" % (CODE, DUMMY)], None
    if machine == "187":            # the apparatus negative control: no such subtype
        return [BIN, "-V", "-x", "-E", "mvme88k", "-e", "187", "-M", "64", "0x%x:%s" % (CODE, DUMMY)], None
    if machine == "luna-88k":
        if IMAGES:
            return ([BIN, "-V", "-x", "-e", "luna-88k", "-d", "R:" + os.path.join(IMAGES, RIG_IMG), "boot"],
                    IMAGES)
        return [BIN, "-V", "-x", "-E", "luna88k", "-e", "luna-88k", "0x%x:%s" % (CODE, DUMMY)], None
    raise ValueError(machine)


def seeds(pairs):
    return ["r%d=0x%x" % (r, v) for r, v in pairs]


def place(blocks):
    """blocks: [(addr, [Ins])] -> (debugger commands, [(addr, Ins)]).  Every block is re-read with
       `unassemble' (end-exclusive) right after it is written."""
    cmds, placed = [], []
    for at, insns in blocks:
        for i, ins in enumerate(insns):
            a = at + 4 * i
            if ins.ops is None:
                ins = Ins(ins.word, ins.mnem, "0x%08x" % a)
            cmds.append("put w 0x%x, 0x%08x" % (a, ins.word))
            placed.append((a, ins))
        cmds.append("unassemble 0x%x 0x%x" % (at, at + 4 * len(insns)))
    return cmds, placed


def run_piped(machine, cmds, tag, timeout=90):
    argv, cwd = argv_for(machine)
    inp = ("\n".join(list(cmds) + ["quit"]) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout,
                           cwd=cwd)
        text = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        text, how = (e.output or b"").decode("latin-1", "replace").replace("\r", ""), "TIMEOUT"
    if DUMP:
        with open(os.path.join(DUMP, "%s.txt" % tag), "w") as f:
            f.write("# argv: %s\n# cwd: %s\n# how: %s\n" % (" ".join(argv), cwd, how))
            f.write(text)
    return text, how


DIS_RE = re.compile(r"^[su]([0-9a-f]{8}): ([0-9a-f]{8})\s+(?:<-\s+)?(\S+)(?:\t(\S+))?[ \t]*$", re.M)
GPR_RE = re.compile(r"\br(\d+)\s*=\s*(0x[0-9a-fA-F]+)")
PC_RE = re.compile(r"cpu\d+:\s+pc\s+=\s+(0x[0-9a-fA-F]+)")
CR_RE = re.compile(r"\b([A-Z][A-Z0-9]*)=(0x[0-9a-fA-F]+)")


class Res(object):
    pass


def analyse(text, how, placed):
    """Split the transcript at the prompts; parse every unassemble, the last `reg' and the last `reg 0,0'."""
    r = Res()
    r.how, r.text, r.placed = how, text, placed
    r.dis, r.regs, r.pc, r.cr = {}, None, None, None
    for part in text.split(PROMPT)[1:]:
        cmd, _, out = part.partition("\n")
        cmd = cmd.strip()
        if cmd.startswith("unassemble"):
            for m in DIS_RE.finditer(out):
                r.dis[int(m.group(1), 16)] = (int(m.group(2), 16), m.group(3), m.group(4) or "")
        elif cmd == "reg":
            m = PC_RE.search(out)
            if m:
                r.regs = {int(g.group(1)): int(g.group(2), 16) for g in GPR_RE.finditer(out)}
                r.pc = int(m.group(1), 16)
        elif cmd == "reg 0,0":
            cr = {g.group(1): int(g.group(2), 16) for g in CR_RE.finditer(out)}
            if cr:
                r.cr = cr
    return r


UNASM = {"ok": 0, "n": 0, "bad": []}


def check_unasm(r, scored=True):
    ok = n = 0
    for a, ins in r.placed:
        n += 1
        d = r.dis.get(a)
        if d is not None and d == (ins.word, ins.mnem, ins.ops):
            ok += 1
        elif scored:
            UNASM["bad"].append("0x%x:%08x %s %s -> %r" % (a, ins.word, ins.mnem, ins.ops, d))
    if scored:
        UNASM["ok"] += ok
        UNASM["n"] += n
    return ok, n


def session(tag, machine, dcmmu, icmmu, access, extra, scored=True):
    cmds, placed = place(blocks_for(access))
    regs = [(2, icmmu), (3, dcmmu), (20, D_PFSR_SEED), (21, D_PFAR_SEED), (22, I_PFSR_SEED), (23, I_PFAR_SEED)]
    regs += [(rr, SENT) for rr in (4, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 31)] + extra
    cmds = seeds(regs) + cmds + ["pc=0x%x" % CODE, "step %d" % NSTEPS, "reg", "reg 0,0"]
    t, how = run_piped(machine, cmds, tag)
    r = analyse(t, how, placed)
    check_unasm(r, scored)
    return r


TIMEOUTS = ("TIMEOUT",)


def died(r):
    return ("timeout:%s" if r.how in TIMEOUTS else "died:%s") % r.how


def g(r, n):
    return r.regs.get(n) if r.regs is not None else None


def prereq_bad(r):
    """None when the session's own prerequisites held; else a cause-free reason (the row stays red)."""
    if r.regs is None:
        return died(r)
    if g(r, 10) != IDR or g(r, 9) != IDR:
        return "nodev d=%s i=%s: device signature absent, check not made" % (hx(g(r, 10)), hx(g(r, 9)))
    back = (g(r, 11), g(r, 12), g(r, 17), g(r, 18))
    if back != SEEDS:
        return "readback %s: seeds did not round-trip, check not made" % "/".join(hx(v) for v in back)
    if r.pc != H_END or g(r, 31) != LIVE:
        return "handler pc=%s r31=%s: the reads did not complete" % (hx(r.pc), hx(g(r, 31)))
    return None


def path_of(r):
    v7, v6 = g(r, 7), g(r, 6)
    if v7 == 3 and v6 == SENT:
        return "v3"
    if v7 == 2 and v6 == SENT:
        return "v2"
    if v7 == SENT and v6 == FALL:
        return "fall"
    return "odd(r6=%s,r7=%s)" % (hx(v6), hx(v7))


def route(r, load):
    cr = r.cr or {}
    s = "%s/%s/%s" % (path_of(r), hx(cr.get("SXIP")), hx(cr.get("DMA0")))
    if load and g(r, 4) != SENT:
        s += " r4=%s" % hx(g(r, 4))
    return s


def kept_i(r):
    """'kept' when the instruction CMMU's PFSR/PFAR still hold their seeds after the access."""
    if (g(r, 15), g(r, 16)) == (I_PFSR_SEED, I_PFAR_SEED):
        return "kept"
    return "ipfsr=%s ipfar=%s" % (hx(g(r, 15)), hx(g(r, 16)))


rows = []
SYMPTOM = []                # (row name, classification)


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15, name     # `%-16s ' keeps a gate's `^$v  .*ok$' satisfiable
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-34s %-34s %-62s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    sys.stdout.flush()
    return ok


def symptom(name, got, want, stale):
    SYMPTOM.append((name, "FIXED" if got == want else ("STALE" if got == stale else "OTHER")))


print("m88kbuserrregs RUNG-3 WITNESS (revision 1) -- binary=%s label=%s" % (BIN, LABEL))
print("machines: -E mvme88k -e mvme187 -M 64 and -E luna88k -e luna-88k (UNMODIFIED); luna shape: %s"
      % ("rig (%s)" % IMAGES if IMAGES else "dummy raw image at 0x%x" % CODE))
print("seeds: dPFSR=%s dPFAR=%s iPFSR=%s iPFAR=%s; want BERROR<<16=%s" % (tuple(hx(v) for v in SEEDS) + (hx(BERROR),)))
t0 = time.time()
print("%-16s %-34s %-34s %-62s %s" % ("row", "got", "want", "note", ""))

# ================================================================ apparatus
#  APPARATUS NEGATIVE CONTROL: the session oracle must be able to go red.
cmds, _ = place([(CODE, [OR_I(4, 0, LIVE), BR_SELF()])])
t, how = run_piped("187", seeds([(4, SENT)]) + cmds + ["pc=0x%x" % CODE, "step 1", "reg"], "neg_apparatus")
rn = analyse(t, how, [])
row("neg apparatus", "%s/%s" % (how, hx(g(rn, 4))), "exit1/absent",
    "bogus subtype `187' -> no machine -> no register dump")

# ================================================================ accept side (mvme187): an ACCEPTED device access
r_ok = session("ok", "mvme187", MV_DCMMU, MV_ICMMU, LD(4, 5, 0), [(5, VME_VBR)])
bad = prereq_bad(r_ok)
row("mv devsig", died(r_ok) if r_ok.regs is None else "%s/%s" % (hx(g(r_ok, 10)), hx(g(r_ok, 9))),
    "%s/%s" % (hx(IDR), hx(IDR)), "DEVICE SIGNATURE: mvme187 data/instr CMMU IDR (RAM reads 0)")
row("mv cmmu rt", died(r_ok) if r_ok.regs is None else "/".join(hx(g(r_ok, n)) for n in (11, 12, 17, 18)),
    "/".join(hx(v) for v in SEEDS), "LIVENESS: four seeds stored and read back via the CMMU decode")
row("ok route", bad if bad else "%s/r4=%s" % (path_of(r_ok), hx(g(r_ok, 4))), "fall/r4=%s" % hx(VBR_SEED),
    "ld VME VBR 0xfff40088 (cased): served 0x67000000, no exception")
row("ok regs", bad if bad else "/".join(hx(g(r_ok, n)) for n in (13, 14, 15, 16)), "/".join(hx(v) for v in SEEDS),
    "an ACCEPTED device access writes no fault metadata")

# ================================================================ generic arm: three refused accesses (mvme187)
def refused(tag, access, extra, addr, load, what):
    r = session(tag, "mvme187", MV_DCMMU, MV_ICMMU, access, extra)
    bad = prereq_bad(r)
    w_route = "v3/%s/%s" % (hx(SXIP_DATA), hx(addr & ~3))
    g_route = bad if bad else route(r, load)
    g_pfsr = bad if bad else hx(g(r, 13))
    g_pfar = bad if bad else hx(g(r, 14))
    row(tag + " route", g_route, w_route, "%s: vector 3, SXIP, DMA0 -- the exception is THIS access" % what)
    row(tag + " pfsr", g_pfsr, hx(BERROR), "data CMMU PFSR after the fault (seeded %s)" % hx(D_PFSR_SEED))
    row(tag + " pfar", g_pfar, hx(addr), "data CMMU PFAR after the fault (seeded %s)" % hx(D_PFAR_SEED))
    row(tag + " icmmu", bad if bad else kept_i(r), "kept", "instruction CMMU PFSR/PFAR keep their seeds")
    symptom(tag + " pfsr", g_pfsr, hx(BERROR), hx(D_PFSR_SEED))
    symptom(tag + " pfar", g_pfar, hx(addr), hx(D_PFAR_SEED))
    return r


refused("uld", LD(4, 5, 0), [(5, UNREAD)], UNREAD, True, "ld 0xfff46010 (unreadable)")
refused("ust", ST(8, 5, 0), [(5, UNREAD), (8, STVAL)], UNREAD, False, "st 0xfff46010 (unreadable)")
refused("vme", LD(4, 5, 0), [(5, VME_P1)], VME_P1, True, "ld 0xfff40090 (VME pop. 1)")

# ================================================================ the LUNA probe address (luna-88k)
r_lu = session("luna", "luna-88k", LU_DCMMU, LU_ICMMU, LD(4, 5, 0), [(5, LUNA_PROBE)])
bad = prereq_bad(r_lu)
row("luna devsig", died(r_lu) if r_lu.regs is None else "%s/%s" % (hx(g(r_lu, 10)), hx(g(r_lu, 9))),
    "%s/%s" % (hx(IDR), hx(IDR)), "DEVICE SIGNATURE: luna-88k data/instr CMMU IDR")
row("luna cmmu rt", died(r_lu) if r_lu.regs is None else "/".join(hx(g(r_lu, n)) for n in (11, 12, 17, 18)),
    "/".join(hx(v) for v in SEEDS), "LIVENESS: the four seeds read back")
if bad:
    g_lr = bad
else:
    cr = r_lu.cr or {}
    g_lr = "%s/%s/%s/r4=%s" % (path_of(r_lu), hx(cr.get("SXIP")), hx(cr.get("DMA0")), hx(g(r_lu, 4)))
w_lr = "v3/%s/%s/r4=%s" % (hx(SXIP_DATA), hx(LUNA_PROBE), hx(SENT))
row("luna route", g_lr, w_lr, "ld 0x3ffffff0: a refused access raises vector 3, serves nothing")
g_lpfsr = bad if bad else hx(g(r_lu, 13))
g_lpfar = bad if bad else hx(g(r_lu, 14))
row("luna pfsr", g_lpfsr, hx(BERROR), "data CMMU PFSR (seeded %s)" % hx(D_PFSR_SEED))
row("luna pfar", g_lpfar, hx(LUNA_PROBE), "data CMMU PFAR (seeded %s)" % hx(D_PFAR_SEED))
row("luna icmmu", bad if bad else kept_i(r_lu), "kept", "instruction CMMU PFSR/PFAR keep their seeds")
SYMPTOM.append(("luna route", "FIXED" if g_lr == w_lr else
                ("STALE" if g_lr == "fall/0x0/0x0/r4=0x0" else "OTHER")))
symptom("luna pfar", g_lpfar, hx(LUNA_PROBE), hx(D_PFAR_SEED))

# ================================================================ INFO (unscored): an INSTRUCTION-access refusal
#  Measured so the round has the number; NOT a row.  Stepped, the debugger's own disassembly pre-read raises vector 2
#  (an artifact: free-running halts at `bad:' instead -- see NOT CLAIMED).  The extra transcript markers say which.
ri = session("info_ifetch", "mvme187", MV_DCMMU, MV_ICMMU, JMP(5), [(5, UNREAD)], scored=False)
cri = ri.cr or {}
print("INFO ifetch      jmp (r5) to 0xfff46010: how=%s path=%s SXIP=%s iPFSR=%s iPFAR=%s dPFSR=%s dPFAR=%s "
      "pre-read-msg=%d halt-msg=%d unasm=%d/%d"
      % (ri.how, path_of(ri) if ri.regs else "absent", hx(cri.get("SXIP")), hx(g(ri, 15)), hx(g(ri, 16)),
         hx(g(ri, 13)), hx(g(ri, 14)), ri.text.count("could not read the instruction"),
         ri.text.count("UNIMPLEMENTED instruction"), *check_unasm(ri, scored=False)))
#  An UNCLAIMED physical address never reaches the refused-access arm (the premise correction in the header).
ru = session("info_unclaimed", "mvme187", MV_DCMMU, MV_ICMMU, LD(4, 5, 0), [(5, UNCLAIMED)], scored=False)
cru = ru.cr or {}
print("INFO unclaimed   ld 0x%08x (no device, past RAM): how=%s path=%s r4=%s SXIP=%s dPFSR=%s dPFAR=%s "
      "iPFSR=%s iPFAR=%s non-existant-msg=%d unasm=%d/%d"
      % (UNCLAIMED, ru.how, path_of(ru) if ru.regs else "absent", hx(g(ru, 4)), hx(cru.get("SXIP")),
         hx(g(ru, 13)), hx(g(ru, 14)), hx(g(ru, 15)), hx(g(ru, 16)), ru.text.count("non-existant"),
         *check_unasm(ru, scored=False)))

# ================================================================ disassembly cross-check
#  LITERAL want, derived by hand BEFORE the first run: each scored session places 23 words (vectors 2 + 2, CODE 13,
#  handler 6); the scored sessions are ok, uld, ust, vme, luna = 5 x 23 = 115.  The apparatus session and the two
#  INFO sessions are not counted.  Computing it from the session list would let a shrunk list pass its own count.
row("unasm", "%d/%d" % (UNASM["ok"], UNASM["n"]), "115/115", "every placed word re-read by the disassembler")
for b in UNASM["bad"][:8]:
    print("  unasm mismatch: %s" % b)

# ================================================================ score + done
npass = sum(1 for _, ok in rows if ok)
print("SCORE %d/%d" % (npass, len(rows)))
CONTROL_ROWS = ("neg apparatus", "mv devsig", "mv cmmu rt", "luna devsig", "luna cmmu rt", "unasm")
_status = dict(rows)
control_ok = all(_status.get(n, False) for n in CONTROL_ROWS)    # a renamed control fails loudly
assert len(SYMPTOM) == 8, SYMPTOM
_cls = [c for _, c in SYMPTOM]
if all(c == "STALE" for c in _cls):
    sym = "PRESENT %d/8" % len(_cls)
elif all(c == "FIXED" for c in _cls):
    sym = "ABSENT"
else:
    sym = "MIXED " + ",".join("%s=%s" % (n, c) for n, c in SYMPTOM)
print("M88K_BUSERR_RESULT=%d/%d" % (npass, len(rows)))
print("M88K_BUSERR_CONTROL=%s" % ("OK" if control_ok else "FAIL"))
print("M88K_BUSERR_SYMPTOM=%s" % sym)
print("M88K_BUSERR_LABEL=%s" % LABEL)
print("M88K_BUSERR_ELAPSED=%.3fs" % (time.time() - t0))
red = [n for n, ok in rows if not ok]
if red:
    print("M88K_BUSERR_RED=%s" % ",".join(red))
shutil.rmtree(_TMPDIR, ignore_errors=True)
print("M88K_BUSERR_PROBE_DONE")
sys.stdout.flush()
sys.exit(0 if control_ok and npass == len(rows) else 1)
