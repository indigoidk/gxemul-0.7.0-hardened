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
        print("%-20s %-4s %s=0x%08x want 0x%08x (buggy 0x%08x)  %s"
              % (name, kind, reg, v, arch, buggy, "ok" if ok else "FAIL"))

print("ENDIAN_CONTROL=%s" % control)
print("ENDIAN_CONTROL378=%s"
      % ("OK" if control378.get("be stm cold b0")
         and control378.get("be ldm cold r1") else "FAIL"))
print("PUT_STATUS=%s" % ("OK" if puts_ok else "FAIL"))
print("ENDIAN_RESULT=%d/%d" % (ngot, ntot))
