#!/usr/bin/env python3
"""
#372: the general-path word STORE ignored cpu->byte_order.
#378: the LDM/STM fast path ignored it too -- polarity INVERTED.

The general path's word-store arm was UNCONDITIONALLY EMPTY -- its guard was
`!A__B && !A__H && HOST_LITTLE_ENDIAN` and its only body was `#ifdef A__STRD`,
but A__STRD implies A__H, which the guard excludes. So a plain word STR on an LE
host emitted no bytes and memory_rw copied the register's HOST bytes to guest
memory, never consulting byte order. The FAST path's word arm has always been
order-aware, so one STR wrote guest order to a WARM page and host order to a
COLD one -- the #342/#355 self-contradiction class -- and every `strt`, which is
general-path on its first access per page (#366), was reversed.

Measured before the fix on -E barearm: a cold store of 0x11223344 read back
0x44332211. After #372's fix: 0x11223344.

#378 is the SIBLING WITH THE POLARITY INVERTED: the LDM/STM fast path emitted by
generate_arm_multi.c moved raw host words (no byte-order term anywhere in the
generator), while the bdt_load/bdt_store fallback (arm_pop/arm_push) swaps on
BOTH its warm and cold arms. So for multi-transfers the WARM rows discriminate
and the COLD rows are the already-correct controls -- exactly opposite to
#372's rows above. The fix gates the fast path's INSTALLATION on
cpu->byte_order == EMUL_LITTLE_ENDIAN (sound because byte_order cannot change
after translation: the CP15 endian-switch route exits the emulator, SETEND is
undecoded, and every other write is machine-setup-time), so post-fix a BE guest
takes bdt_* everywhere and warm == cold == architectural.

Measured before the fix on -E barearm: stmia of r1=0x11223344,r2=0x55667788 to
a WARM page laid down 44 33 22 11 88 77 66 55; DDI 0100I Table A2-2 (p. A2-32,
with A2.7.2 p. A2-33 making LDM/STM a series of ordinary word accesses)
requires 11 22 33 44 55 66 77 88. After the fix: the architectural bytes.

THIS PROBE RUNS BOTH BYTE ORDERS.
  * The BE rig is `-E barearm`, whose MACHINE_SETUP sets EMUL_BIG_ENDIAN
    outright (machine_test.c) -- no config file, no ELF, no stub-order wrinkle.
  * The LE rig is plain `-E testarm`. On LE the broken code was ACCIDENTALLY
    RIGHT (host order == guest order), so LE rows discriminate NOTHING: they
    are INVARIANCE CONTROLS, present to catch a fix that repairs BE by
    breaking LE.

Every row carries an EXPLICIT kind (DISC/CTRL) -- #372's rows derived kind from
"cold in name", which #378's inverted polarity would have turned into a lie.

The ldrb witnesses are the purest form, because a byte load has no byte order
(data[0] in both branches), so they expose the raw memory layout with no
dependence on any word path; each `buggy` column is the exact reverse of its
`arch` column, so the mirror-image BE and LE groups cannot both be satisfied
by a swapped expectation table. r10/r11 are printed as `sl`/`fp` -- the
debugger's ARM_REG_NAMES have no r10/r11 spellings.

In the STORE-test programs r1 = 0x11223344 and r2 = 0x55667788 are built with
immediates, never loaded (a load would add its own path under test); the LDM
programs of course DO load them -- that is what they test -- so those rows
zero both registers first as sentinels.
WARM pages are seeded with an explicit-width `put w` (which maps AND warms:
MMU off => ok-1 == 1 => host_store too; the polarity is proven from source --
memory_rw gates update_translation_table on !no_exceptions, and `put b` passes
NO_EXCEPTIONS). Exact bytes on a warm page are laid with `put b` AFTER the
`put w` (a byte write has no order and does not un-warm). The cold LDM page
sees ONLY `put b`; the cold STM page is fully UNSEEDED (no access of any kind
-- unseeded RAM is zero); #372's cold rows stay fully unseeded as before. The
`put` width is spelled on EVERY command -- put_type is static in
debugger_cmds.c and silently persists. #379: every put's echo is checked for
the debugger's FAILED marker (PUT_STATUS) -- a silently failing `put w` would
leave the warm pages cold and flip every warm DISC row to a FALSE GREEN on a
buggy build, the one direction the controls must never allow.

Every encoding below was verified through the emulator's own `unassemble`,
CHECKING THE REGISTER FIELDS, not just the mnemonic (the round-117 lesson).
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
CODE = 0x8000
WARM = 0x10000
COLD = 0x20000

#  Build r1 = 0x11223344 with immediates (mov + 3 orr), verified via unassemble.
BUILD_R1 = [0xE3A01411, 0xE3811822, 0xE3811C33, 0xE3811044]
#  Build r2 = 0x55667788 (mov + 3 orr, Rd=Rn=2), #378.
BUILD_R2 = [0xE3A02455, 0xE3822866, 0xE3822C77, 0xE3822088]
MOV_R0_WARM = 0xE3A00801        # mov r0,#0x10000
MOV_R0_COLD = 0xE3A00802        # mov r0,#0x20000
MOV_R3_WARM = 0xE3A03801        # mov r3,#0x10000
MOV_R3_COLD = 0xE3A03802        # mov r3,#0x20000
STR_R1_R0 = 0xE5801000          # str  r1,[r0]
LDR_R2_R0 = 0xE5902000          # ldr  r2,[r0]
LDRB = (0xE5D03000, 0xE5D04001, 0xE5D05002, 0xE5D06003)  # ldrb r3..r6,[r0,#0..3]
#  #378: stmia/ldmia r3,{r1,r2} (W=0 so r3 survives as the readback base) and
#  an 8-byte ldrb ladder BASED ON R3 into r4..r11 (never clobbering r1/r2/r3).
STMIA_R3 = 0xE8830006           # stmia r3,{r1,r2}
LDMIA_R3 = 0xE8930006           # ldmia r3,{r1,r2}
LDRB8_R3 = (0xE5D34000, 0xE5D35001, 0xE5D36002, 0xE5D37003,
            0xE5D38004, 0xE5D39005, 0xE5D3A006, 0xE5D3B007)
MOV_R1_0 = 0xE3A01000           # mov r1,#0  (LDM sentinel: a dead LDM reads 0)
MOV_R2_0 = 0xE3A02000           # mov r2,#0
SPIN = 0xEAFFFFFE               # b .

#  #386: swp/swpb. X(swp) goes through memory_rw directly (no warm/cold fast
#  path), so a put b-seeded page suffices and there is no #372-style split.
SWP_R2_R1_R0 = 0xE1002091      # swp  r2,r1,[r0]
SWPB_R2_R1_R0 = 0xE1402091     # swpb r2,r1,[r0]  (bit 22 = B)
ADD_R0_1 = 0xE2800001          # add r0,r0,#1   (unaligned rows)
SUB_R0_1 = 0xE2400001          # sub r0,r0,#1   (ladder re-bases at aligned P)
ADD_R0_2 = 0xE2800002          # add r0,r0,#2   (#387: the +2 offset groups)
SUB_R0_2 = 0xE2400002          # sub r0,r0,#2
LDRB_R7_R0_4 = 0xE5D07004      # ldrb r7,[r0,#4] -- the P+4 survivor sentinel
BUILD_R1_5567 = [0xE3A01455,   # mov r1,#0x55000000
                 0xE3811866,   # orr r1,r1,#0x00660000
                 0xE3811C77,   # orr r1,r1,#0x00007700
                 0xE3811088]   # orr r1,r1,#0x88      -> r1 = 0x55667788


def store_prog(base_mov):
    return BUILD_R1 + [base_mov, STR_R1_R0, LDR_R2_R0] + list(LDRB) + [SPIN]


def stm_prog(base_mov):
    return (BUILD_R1 + BUILD_R2 + [base_mov, STMIA_R3] + list(LDRB8_R3)
            + [SPIN])


def ldm_prog(base_mov):
    return [MOV_R1_0, MOV_R2_0, base_mov, LDMIA_R3, SPIN]


def seed_bytes(base):
    """Explicit-width put b commands laying 11 22 33 44 55 66 77 88."""
    return ["put b 0x%x, 0x%02x" % (base + i, v)
            for i, v in enumerate((0x11, 0x22, 0x33, 0x44,
                                   0x55, 0x66, 0x77, 0x88))]


#  #390: `str rX,[pc,#imm]` used a base of instruction+12 where A5.2.2 (and
#  A5.2.3/A5.2.4, and A5.3.2/A5.3.3 for mode 3) define R15-as-Rn to be the
#  address of the instruction PLUS EIGHT.  One scratch word was serving two
#  roles -- the BASE when Rn == PC, and the DATA when Rd == PC -- and the store
#  arm set it to +12 for both.  LDRD was caught in it too: mode 3 encodes LDRD
#  with L == 0, so the generator never defines A__L for it and it takes the
#  store arm despite being a load.
#
#  Readback is ALWAYS through a register base, never a pc-relative load: the
#  decoder folds pc-relative LOADS into a constant MOV at TRANSLATE time, so
#  such a load reports the bytes as they were BEFORE the store under test.
STR_R4_PC_40  = 0xE58F4040      # str r4,[pc,#0x40]
STR_PC_R7     = 0xE587F000      # str pc,[r7]
STR_PC_PC_40  = 0xE58FF040      # str pc,[pc,#0x40]
LDRD_R0_PC_40 = 0xE1CF04D0      # ldrd r0,[pc,#0x40]
MOV_R7_20000  = 0xE3A07802      # mov r7,#0x20000
MOV_R3_8000   = 0xE3A03C80      # mov r3,#0x8000   (0x80 ror 24)
ORR_R3_58     = 0xE3833058      # orr r3,r3,#0x58  -> r3 = 0x8058
ORR_R3_48     = 0xE3833048      # orr r3,r3,#0x48  -> r3 = 0x8048
LDR_R5_R3     = 0xE5935000      # ldr r5,[r3]
LDR_R6_R3_4   = 0xE5936004      # ldr r6,[r3,#4]
LDR_R5_R7     = 0xE5975000      # ldr r5,[r7]


def str_base_prog():
    """R1: str r4,[pc,#0x40] at CODE+0x10; read BOTH candidate words.

    The +8 candidate is 0x8058 and the +12 candidate 0x805c, so one ldr pair
    covers both and the WRONG candidate is asserted to hold its sentinel --
    a row that only checked the right address would pass a store-to-both.
    """
    return (list(BUILD_R4) + [STR_R4_PC_40, MOV_R3_8000, ORR_R3_58,
                              LDR_R5_R3, LDR_R6_R3_4, SPIN])


def str_data_prog():
    """R2: str pc,[r7] -- the DATA role, with an ordinary base register.

    Must read instruction+12 BEFORE and AFTER the fix.  This is the row that
    catches a role-aware guard written without an else: that leaves the scratch
    word holding whatever the previous PC-relative instruction left in it.
    """
    return [MOV_R7_20000, STR_PC_R7, LDR_R5_R7, SPIN]


def str_bothpc_prog():
    """R3: str pc,[pc,#0x40] -- both roles at once, the load-bearing row.

    Needs base = instruction+8 AND stored value = instruction+12 SIMULTANEOUSLY.
    Checking the VALUE at the +8 address is what separates the two-word fix from
    a blanket +8, which puts the right address there carrying the wrong word.
    """
    return [STR_PC_PC_40, MOV_R3_8000, ORR_R3_48, LDR_R5_R3, SPIN]


def ldrd_pc_prog():
    """R4: ldrd r0,[pc,#0x40] with three distinct words planted.

    r0/r1 identify WHICH pair was read, so a base that is four bytes high is
    distinguishable from a correct one rather than merely 'not the sentinel'.
    """
    return [LDRD_R0_PC_40, SPIN]


def swp_prog():
    return BUILD_R1_5567 + [MOV_R0_COLD, SWP_R2_R1_R0] + list(LDRB) + [SPIN]


def swpb_prog():
    return BUILD_R1_5567 + [MOV_R0_COLD, SWPB_R2_R1_R0, LDRB[0]] + [SPIN]


def swp_unal_prog():
    #  r0 = P+1 for the swp only; the ladder re-bases at the aligned P and adds
    #  the P+4 sentinel read. Pre-fix the swp reads/writes 4 RAW bytes at P+1;
    #  post-fix both accesses use P and the load rotates (DDI 0100I A4.1.108).
    return (BUILD_R1_5567 + [MOV_R0_COLD, ADD_R0_1, SWP_R2_R1_R0, SUB_R0_1]
            + list(LDRB) + [LDRB_R7_R0_4, SPIN])


#  #386 unaligned seeds: the P+4 sentinel byte must NOT be 0x55 -- the buggy
#  raw store's last byte (LE emit of 0x55667788) lands 0x55 at P+4, so a 0x55
#  seed would make survival and corruption indistinguishable. 0x99 is disjoint
#  from every seed and store byte.
def swp_unal_seeds():
    return seed_bytes(COLD)[:4] + ["put b 0x%x, 0x99" % (COLD + 4)]


#  #389: LDRD/STRD. Encodings verified by the round's RED reproduction (the
#  committed build produced the exact predicted buggy values, impossible for
#  a wrong or UNDEFINED word). The pair register is IMPLICIT R(d+1) -- mode-3
#  has no Rt2 field; bit 22 = 1 is the IMMEDIATE form; LDRD sits in the L=0
#  half of the extra-loads space (S/H distinguish it).
LDRD_R4_R3 = 0xE1C340D0        # ldrd r4,[r3]  (loads r4 AND r5)
STRD_R4_R3 = 0xE1C340F0        # strd r4,[r3]  (stores r4 AND r5)
MOV_R4_0 = 0xE3A04000          # mov r4,#0  (dead-LDRD sentinel)
MOV_R5_0 = 0xE3A05000          # mov r5,#0
BUILD_R4 = [0xE3A04411,        # mov r4,#0x11000000
            0xE3844822,        # orr r4,r4,#0x00220000
            0xE3844C33,        # orr r4,r4,#0x00003300
            0xE3844044]        # orr r4,r4,#0x44      -> r4 = 0x11223344
BUILD_R5 = [0xE3A05455,        # mov r5,#0x55000000
            0xE3855866,        # orr r5,r5,#0x00660000
            0xE3855C77,        # orr r5,r5,#0x00007700
            0xE3855088]        # orr r5,r5,#0x88      -> r5 = 0x55667788


def ldrd_prog():
    return [MOV_R4_0, MOV_R5_0, MOV_R3_COLD, LDRD_R4_R3, SPIN]


def strd_prog():
    #  The STRD page is fully UNSEEDED (no access of any kind -- unseeded RAM
    #  is zero), so a dead STRD reads sentinel 0 through the ladder.
    return (BUILD_R4 + BUILD_R5 + [MOV_R3_COLD, STRD_R4_R3]
            + list(LDRB8_R3) + [SPIN])


#  #387: the +2 groups seed P+5 explicitly (0xAA, disjoint from everything)
#  so the buggy raw P+2..P+5 read has a defined fourth byte that does not
#  lean on the unseeded-RAM-is-zero assumption.
def swp_un2_prog():
    return (BUILD_R1_5567 + [MOV_R0_COLD, ADD_R0_2, SWP_R2_R1_R0, SUB_R0_2]
            + list(LDRB) + [LDRB_R7_R0_4, SPIN])


def swp_un2_seeds():
    return swp_unal_seeds() + ["put b 0x%x, 0xaa" % (COLD + 5)]


def run(machine, prog, seeds, regs):
    #  A raw stub just makes the machine construct. barearm lays no LE halt stub
    #  of its own (unlike testarm), so nothing decodes as garbage post-flip.
    stub = "/tmp/gx_endian_%s.bin" % machine
    order = ">I" if machine == "barearm" else "<I"
    import struct
    with open(stub, "wb") as f:
        f.write(struct.pack(order, 0xE1A00000))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-A", "-E", machine, "-M", "64",
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
        wait_from(mark)
        return buf[mark:]

    if not wait_from(0, 60):
        try:
            os.kill(pid, 9); os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    #  #379: every seed/program `put` is CHECKED for the debugger's "FAILED"
    #  echo. The ten warm DISC rows depend on `put w` having warmed the page;
    #  a silently failing put would leave it cold, route the transfer through
    #  bdt_*, and turn every DISC row architecturally green ON A BUGGY BUILD --
    #  a false pass, the one direction a control must never allow.
    put_ok = True
    for s in seeds:
        if "FAILED" in send(s):
            put_ok = False
    for i, iw in enumerate(prog):
        if "FAILED" in send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw)):
            put_ok = False
    send("pc=0x%x" % CODE)
    send("step %d" % (len(prog) - 1))    # straight-line, ends at the spin

    out = {"__put_ok": put_ok}
    for rn in regs:
        mark = len(buf)
        send("print %s" % rn)
        m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
        if m:
            out[rn] = int(m.group(1), 16)
    try:
        os.write(fd, b"quit\n"); time.sleep(0.2)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    return out


SEED_WARM_W = ["put w 0x%x, 0x00000000" % WARM]

#  Row groups: one emulator spawn each; every row carries an EXPLICIT kind.
#  (group_label, machine, prog, seeds, [(row_name, reg, arch, buggy, kind)])
#  `buggy` = the value the PRE-FIX build produces (#372 rows: pre-#372;
#  #378 rows: pre-#378). arch == buggy marks a control by construction.
GROUPS = [
    #  ---- #372 rows, byte-identical behaviour to the committed probe --------
    ("372 be warm", "barearm", store_prog(MOV_R0_WARM), SEED_WARM_W, [
        ("be warm word", "r2", 0x11223344, 0x11223344, "CTRL"),
    ]),
    ("372 be cold", "barearm", store_prog(MOV_R0_COLD), SEED_WARM_W, [
        ("be cold word", "r2", 0x11223344, 0x44332211, "DISC"),
        ("be cold byte0", "r3", 0x11, 0x44, "DISC"),
        ("be cold byte1", "r4", 0x22, 0x33, "DISC"),
        ("be cold byte2", "r5", 0x33, 0x22, "DISC"),
        ("be cold byte3", "r6", 0x44, 0x11, "DISC"),
    ]),
    ("372 le warm", "testarm", store_prog(MOV_R0_WARM), SEED_WARM_W, [
        ("le warm word", "r2", 0x11223344, 0x11223344, "CTRL"),
    ]),
    ("372 le cold", "testarm", store_prog(MOV_R0_COLD), SEED_WARM_W, [
        ("le cold word", "r2", 0x11223344, 0x11223344, "CTRL"),
        ("le cold byte0", "r3", 0x44, 0x44, "CTRL"),
        ("le cold byte1", "r4", 0x33, 0x33, "CTRL"),
        ("le cold byte2", "r5", 0x22, 0x22, "CTRL"),
        ("le cold byte3", "r6", 0x11, 0x11, "CTRL"),
    ]),
    #  ---- #378 rows: WARM discriminates, COLD is the already-correct control.
    ("378 be stm warm", "barearm", stm_prog(MOV_R3_WARM), SEED_WARM_W, [
        ("be stm warm b0", "r4", 0x11, 0x44, "DISC"),
        ("be stm warm b1", "r5", 0x22, 0x33, "DISC"),
        ("be stm warm b2", "r6", 0x33, 0x22, "DISC"),
        ("be stm warm b3", "r7", 0x44, 0x11, "DISC"),
        ("be stm warm b4", "r8", 0x55, 0x88, "DISC"),
        ("be stm warm b5", "r9", 0x66, 0x77, "DISC"),
        ("be stm warm b6", "sl", 0x77, 0x66, "DISC"),
        ("be stm warm b7", "fp", 0x88, 0x55, "DISC"),
    ]),
    ("378 be stm cold", "barearm", stm_prog(MOV_R3_COLD), [], [
        ("be stm cold b0", "r4", 0x11, 0x11, "CTRL"),
        ("be stm cold b1", "r5", 0x22, 0x22, "CTRL"),
        ("be stm cold b2", "r6", 0x33, 0x33, "CTRL"),
        ("be stm cold b3", "r7", 0x44, 0x44, "CTRL"),
    ]),
    ("378 be ldm warm", "barearm", ldm_prog(MOV_R3_WARM),
     SEED_WARM_W + seed_bytes(WARM), [
        ("be ldm warm r1", "r1", 0x11223344, 0x44332211, "DISC"),
        ("be ldm warm r2", "r2", 0x55667788, 0x88776655, "DISC"),
    ]),
    ("378 be ldm cold", "barearm", ldm_prog(MOV_R3_COLD), seed_bytes(COLD), [
        ("be ldm cold r1", "r1", 0x11223344, 0x11223344, "CTRL"),
        ("be ldm cold r2", "r2", 0x55667788, 0x55667788, "CTRL"),
    ]),
    ("378 le stm warm", "testarm", stm_prog(MOV_R3_WARM), SEED_WARM_W, [
        ("le stm warm b0", "r4", 0x44, 0x44, "CTRL"),
        ("le stm warm b1", "r5", 0x33, 0x33, "CTRL"),
        ("le stm warm b2", "r6", 0x22, 0x22, "CTRL"),
        ("le stm warm b3", "r7", 0x11, 0x11, "CTRL"),
    ]),
    ("378 le ldm warm", "testarm", ldm_prog(MOV_R3_WARM),
     SEED_WARM_W + seed_bytes(WARM), [
        ("le ldm warm r1", "r1", 0x44332211, 0x44332211, "CTRL"),
        ("le ldm warm r2", "r2", 0x88776655, 0x88776655, "CTRL"),
    ]),
    #  ---- #386 rows: X(swp) was LE-only on BOTH its load-assemble and its
    #  store-emit, and used the RAW address with no rotate (DDI 0100I A4.1.108
    #  U==0: load rotates by 8*addr[1:0], store does not, both accesses use the
    #  aligned word). `buggy` = the pre-#386 build. The LE ALIGNED rows are
    #  byte-identical pre/post (CTRL); the LE UNALIGNED rows MOVE under the fix
    #  (the manual's rotation is endian-independent), so they are ARCH rows,
    #  deliberately NOT must-not-move controls. "swp be unal b2" is arch==buggy
    #  BY CONSTRUCTION for the +1 shift: buggy puts LE-d[1]=bits[15:8] at P+2,
    #  fixed puts BE-d[2]=bits[15:8] there too -- same byte for ANY store value.
    #  The P+4 sentinel (0x99 seed) proves the buggy raw P+1..P+4 write did NOT
    #  occur -- 0x99 survives fixed, 0x55 (the buggy write's last byte) pre-fix.
    ("386 be swp", "barearm", swp_prog(), seed_bytes(COLD)[:4], [
        ("swp be word", "r2", 0x11223344, 0x44332211, "DISC"),
        ("swp be b0", "r3", 0x55, 0x88, "DISC"),
        ("swp be b1", "r4", 0x66, 0x77, "DISC"),
        ("swp be b2", "r5", 0x77, 0x66, "DISC"),
        ("swp be b3", "r6", 0x88, 0x55, "DISC"),
    ]),
    ("386 le swp", "testarm", swp_prog(), seed_bytes(COLD)[:4], [
        ("swp le word", "r2", 0x44332211, 0x44332211, "CTRL"),
        ("swp le b0", "r3", 0x88, 0x88, "CTRL"),
        ("swp le b1", "r4", 0x77, 0x77, "CTRL"),
        ("swp le b2", "r5", 0x66, 0x66, "CTRL"),
        ("swp le b3", "r6", 0x55, 0x55, "CTRL"),
    ]),
    ("386 be swpb", "barearm", swpb_prog(), seed_bytes(COLD)[:1], [
        ("swpb be r2", "r2", 0x11, 0x11, "CTRL"),
        ("swpb be mem", "r3", 0x88, 0x88, "CTRL"),
    ]),
    ("386 be swp unal", "barearm", swp_unal_prog(), swp_unal_seeds(), [
        ("swp be unal r2", "r2", 0x44112233, 0x99443322, "DISC"),
        ("swp be unal b0", "r3", 0x55, 0x11, "DISC"),
        ("swp be unal b1", "r4", 0x66, 0x88, "DISC"),
        ("swp be unal b2", "r5", 0x77, 0x77, "CTRL"),
        ("swp be unal b3", "r6", 0x88, 0x66, "DISC"),
        ("swp be unal sent", "r7", 0x99, 0x55, "DISC"),
    ]),
    ("386 le swp unal", "testarm", swp_unal_prog(), swp_unal_seeds(), [
        ("swp le unal r2", "r2", 0x11443322, 0x99443322, "DISC"),
        ("swp le unal b0", "r3", 0x88, 0x11, "DISC"),
        ("swp le unal b1", "r4", 0x77, 0x88, "DISC"),
        ("swp le unal b2", "r5", 0x66, 0x77, "DISC"),
        ("swp le unal b3", "r6", 0x55, 0x66, "DISC"),
        ("swp le unal sent", "r7", 0x99, 0x55, "DISC"),
    ]),
    #  ---- #387 rows: the +2 offset. The +1 groups above cannot distinguish
    #  the shipped `8*(addr&3)` / `if(rot_sh)` / `addr&=~3` from three wrong
    #  forms that AGREE at +1 -- `8*(addr&1)`, a guard of `if(addr&1)`, and a
    #  mask of `~1` (the fold-marker probe's three-offsets rule, its :437).
    #  At +2 all three diverge: the &1 amount gives 0, the &1 guard skips the
    #  rotate entirely, and the ~1 mask leaves the access at P+2. Every +2 row
    #  is DISC -- the +1 b2 by-construction collision does not recur (buggy at
    #  +2 puts LE-d[0]=bits[7:0]=0x88 at P+2; fixed puts bits[15:8]=0x77).
    #  `buggy` = the pre-#386 build: raw LE load of P+2..P+5 = 33 44 99 AA ->
    #  0xAA994433; raw LE store at P+2..P+5 -> ladder 11 22 88 77, sent 66.
    ("387 be swp un2", "barearm", swp_un2_prog(), swp_un2_seeds(), [
        ("swp be un2 r2", "r2", 0x33441122, 0xAA994433, "DISC"),
        ("swp be un2 b0", "r3", 0x55, 0x11, "DISC"),
        ("swp be un2 b1", "r4", 0x66, 0x22, "DISC"),
        ("swp be un2 b2", "r5", 0x77, 0x88, "DISC"),
        ("swp be un2 b3", "r6", 0x88, 0x77, "DISC"),
        ("swp be un2 sent", "r7", 0x99, 0x66, "DISC"),
    ]),
    ("387 le swp un2", "testarm", swp_un2_prog(), swp_un2_seeds(), [
        ("swp le un2 r2", "r2", 0x22114433, 0xAA994433, "DISC"),
        ("swp le un2 b0", "r3", 0x88, 0x11, "DISC"),
        ("swp le un2 b1", "r4", 0x77, 0x22, "DISC"),
        ("swp le un2 b2", "r5", 0x66, 0x88, "DISC"),
        ("swp le un2 b3", "r6", 0x55, 0x77, "DISC"),
        ("swp le un2 sent", "r7", 0x99, 0x66, "DISC"),
    ]),
    #  ---- #389 rows: LDRD/STRD were three defects deep on BE -- a word-pair
    #  inversion on BOTH sides (Rd took the upper word; the architecture pairs
    #  Rd with the LOWER address, A4.1.26/A4.1.102), a carry-corrupting
    #  data[1]<<6 term (buggy Rd = 0x55660908, NOT a byte permutation), and a
    #  verbatim-LE R(d+1) branch. Both always take the general path (the
    #  chicken-out is unconditional for A__LDRD||A__STRD), so no warm/cold
    #  split. The LE rows are true invariance controls (LE was correct).
    #  Oracle: the ldrd arch values equal the committed LDM rows' on the same
    #  bytes. buggy = the pre-#389 build, measured in the RED reproduction.
    ("389 be ldrd", "barearm", ldrd_prog(), seed_bytes(COLD), [
        ("ldrd be r4", "r4", 0x11223344, 0x55660908, "DISC"),
        ("ldrd be r5", "r5", 0x55667788, 0x44332211, "DISC"),
    ]),
    ("389 le ldrd", "testarm", ldrd_prog(), seed_bytes(COLD), [
        ("ldrd le r4", "r4", 0x44332211, 0x44332211, "CTRL"),
        ("ldrd le r5", "r5", 0x88776655, 0x88776655, "CTRL"),
    ]),
    ("389 be strd", "barearm", strd_prog(), [], [
        ("strd be b0", "r4", 0x11, 0x55, "DISC"),
        ("strd be b1", "r5", 0x22, 0x66, "DISC"),
        ("strd be b2", "r6", 0x33, 0x77, "DISC"),
        ("strd be b3", "r7", 0x44, 0x88, "DISC"),
        ("strd be b4", "r8", 0x55, 0x11, "DISC"),
        ("strd be b5", "r9", 0x66, 0x22, "DISC"),
        ("strd be b6", "sl", 0x77, 0x33, "DISC"),
        ("strd be b7", "fp", 0x88, 0x44, "DISC"),
    ]),
    ("389 le strd", "testarm", strd_prog(), [], [
        ("strd le b0", "r4", 0x44, 0x44, "CTRL"),
        ("strd le b1", "r5", 0x33, 0x33, "CTRL"),
        ("strd le b2", "r6", 0x22, 0x22, "CTRL"),
        ("strd le b3", "r7", 0x11, 0x11, "CTRL"),
        ("strd le b4", "r8", 0x88, 0x88, "CTRL"),
        ("strd le b5", "r9", 0x77, 0x77, "CTRL"),
        ("strd le b6", "sl", 0x66, 0x66, "CTRL"),
        ("strd le b7", "fp", 0x55, 0x55, "CTRL"),
    ]),

    #  ---- #390 rows: the PC-as-base role conflation.  Addresses, not bytes,
    #  so every value below is byte-order INDEPENDENT and both rigs must agree
    #  -- which is itself the check that no byte-order-specific regression hides
    #  here.  All four groups run on barearm and testarm alike.
    #
    #  buggy = MEASURED on the pre-#390 build (parent 495a07a), not predicted.
    #  A THIRD implementation, a blanket +8 that also moves the data role, is
    #  what "390 bothpc" exists to catch: it would put the right ADDRESS there
    #  carrying 0x8008 instead of 0x800c, which no other row can see.
    #
    #  STR is at CODE+0x10 in the base group (four BUILD_R4 words precede it),
    #  so its +8 target is 0x8058 and its +12 target 0x805c.  In the bothpc and
    #  ldrd groups the instruction is first, at CODE, so the targets are 0x8048
    #  and 0x804c.
    ("390 be base", "barearm", str_base_prog(), [], [
        ("390 be base +8",  "r5", 0x11223344, 0x00000000, "DISC"),
        ("390 be base +12", "r6", 0x00000000, 0x11223344, "DISC"),
    ]),
    ("390 le base", "testarm", str_base_prog(), [], [
        ("390 le base +8",  "r5", 0x11223344, 0x00000000, "DISC"),
        ("390 le base +12", "r6", 0x00000000, 0x11223344, "DISC"),
    ]),

    #  DATA-role guard.  arch == buggy ON PURPOSE: this row must pass on BOTH
    #  builds.  It is not a discriminator for the defect -- it is the detector
    #  for a WRONG FIX that moves the stored R15 value off +12.  A2-9 forbids
    #  an implementation using +8 for some R15 stores and +12 for others.
    ("390 be data", "barearm", str_data_prog(), [], [
        ("390 be data +12", "r5", 0x8010, 0x8010, "CTRL"),
    ]),
    ("390 le data", "testarm", str_data_prog(), [], [
        ("390 le data +12", "r5", 0x8010, 0x8010, "CTRL"),
    ]),

    #  BOTH-PC: base +8 and data +12 at the same time.  buggy = 0 because
    #  pre-#390 nothing was written to the +8 target at all.
    ("390 be bothpc", "barearm", str_bothpc_prog(), [], [
        ("390 be bothpc", "r5", 0x800c, 0x00000000, "DISC"),
    ]),
    ("390 le bothpc", "testarm", str_bothpc_prog(), [], [
        ("390 le bothpc", "r5", 0x800c, 0x00000000, "DISC"),
    ]),

    #  LDRD base -- CTRL, and the story behind that is the point.
    #
    #  These began life as DISC rows, on the reasoning that LDRD encodes L == 0
    #  and so takes A__NAME_PC's store arm and inherited its +12 base.  That
    #  reasoning was WRONG, and the mutant battery is what exposed it: reverting
    #  the base assignment to +12 left these rows GREEN, which they could not be
    #  if they depended on it.  Building the actual pre-#390 parent settled it --
    #  r0 reads 0xaaaa0001 there too, identical to the fixed build.  LDRD's base
    #  was NEVER four bytes high, and the `buggy` column these rows used to
    #  carry was fiction: they could not have failed for the stated reason.
    #
    #  They are kept, re-typed CTRL with arch == buggy, because the measurement
    #  is worth having: it is the standing evidence that LDRD with Rn == PC is
    #  UNAFFECTED by the base-role split, and it will redden if some future
    #  round drags LDRD into that path.  Three distinct planted words, so the
    #  row still says WHICH pair was read rather than merely "not a sentinel".
    ("390 be ldrd", "barearm", ldrd_pc_prog(),
     ["put w 0x8048, 0xaaaa0001", "put w 0x804c, 0xbbbb0002",
      "put w 0x8050, 0xcccc0003"], [
        ("390 be ldrd r0", "r0", 0xaaaa0001, 0xaaaa0001, "CTRL"),
        ("390 be ldrd r1", "r1", 0xbbbb0002, 0xbbbb0002, "CTRL"),
    ]),
    ("390 le ldrd", "testarm", ldrd_pc_prog(),
     ["put w 0x8048, 0xaaaa0001", "put w 0x804c, 0xbbbb0002",
      "put w 0x8050, 0xcccc0003"], [
        ("390 le ldrd r0", "r0", 0xaaaa0001, 0xaaaa0001, "CTRL"),
        ("390 le ldrd r1", "r1", 0xbbbb0002, 0xbbbb0002, "CTRL"),
    ]),
]

print("=== #372 store + #378 LDM/STM: byte order must reach guest memory ===")
print("    #372 DISC rows are COLD (general path was wrong);")
print("    #378 DISC rows are WARM (fast path was wrong) -- inverted polarity")

#  Controls: `be warm word` proves the #372 machinery live (fast STR was always
#  order-aware). `be stm cold b0` + `be ldm cold r1` prove the #378 machinery
#  live INDEPENDENT of the fix state -- bdt_* swaps on every build, so these
#  read arch values on buggy and fixed builds alike; a dead rig, wrong register
#  field or non-firing LDM reads 0 / a sentinel instead.
control = "FAIL"
control378 = {}
controlD = {}
puts_ok = True
ngot = ntot = 0
for glabel, machine, prog, seeds, rows in GROUPS:
    regs = [r[1] for r in rows]
    got = run(machine, prog, seeds, regs)
    if got is not None and not got.get("__put_ok", False):
        puts_ok = False
    for name, reg, arch, buggy, kind in rows:
        ntot += 1
        if got is None or reg not in got:
            print("%-20s DEAD  FAIL" % name)
            continue
        v = got[reg]
        ok = (v == arch)
        ngot += ok
        if name == "be warm word" and v == 0x11223344:
            control = "OK"
        if name in ("be stm cold b0", "be ldm cold r1"):
            control378[name] = ok
        #  #389 liveness pins: fix-state-independent LE rows whose DEAD value
        #  is the sentinel 0 (MOV_R4_0 / the unseeded STRD page) -- nonzero
        #  proves the instructions executed on the rig at all.
        if name in ("ldrd le r4", "strd le b0"):
            controlD[name] = (v != 0)
        print("%-20s %-4s %s=0x%08x want 0x%08x (buggy 0x%08x)  %s"
              % (name, kind, reg, v, arch, buggy, "ok" if ok else "FAIL"))

print("ENDIAN_CONTROL=%s" % control)
print("ENDIAN_CONTROL378=%s"
      % ("OK" if control378.get("be stm cold b0")
         and control378.get("be ldm cold r1") else "FAIL"))
print("ENDIAN_CONTROL_D=%s"
      % ("OK" if controlD.get("ldrd le r4")
         and controlD.get("strd le b0") else "FAIL"))
print("PUT_STATUS=%s" % ("OK" if puts_ok else "FAIL"))
print("ENDIAN_RESULT=%d/%d" % (ngot, ntot))
