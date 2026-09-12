#!/usr/bin/env python3
"""
arm_bdt_probe.py -- Rung-3 witness for ARM block data transfer (armbdt).

Tests all four callers of arm_pop / arm_push:
  1. X(bdt_load)          (ARM LDM)
  2. X(bdt_store)         (ARM STM)
  3. Thumb POP            (cpu_arm.c:1677)
  4. Thumb PUSH           (cpu_arm.c:1670)

Under cold debugger on unmodified in-tree machine testarm.
Core row shape: identical instruction against identical unaligned base executed
COLD and WARM, asserting both produce identical architecturally-correct bytes.
Discriminates writeback (W=1) unmasked arithmetic result to kill mask-at-entry mutant.
Includes liveness control and attribution control asserting specific byte splice.

PROMOTED 2026-09-11 from regress/artifacts/armbdt/agy_armbdt_witness_20260911.py,
which stays in place as the AS-RUN record of tables 1-5.  This copy is the one
that evolves and that gate_arm.sh executes; editing the artifact copy would
falsify what those tables actually measured.

*** read_mem32() DUMPS FROM THE 16-BYTE-ALIGNED BASE.  An unaligned dump start
still carries the aligned line label but BLANK-PADS the leading word groups,
and .split() then shifts every column index -- so the read silently returns a
NEIGHBOURING word.  That defect corrupted 8 of 10 legs of table 4 and made a
CORRECT fix report a red BASE row.  Row: probereadalign. ***
"""

import os, sys, pty, select, time, re

BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxarmbdt_clone/gxemul"
LEG = sys.argv[2] if len(sys.argv) > 2 else "BASE"
STUB = "/tmp/stub_armbdt.bin"
if not os.path.exists(STUB):
    with open(STUB, "wb") as f:
        f.write((0xE1A00000).to_bytes(4, "little"))

CODE = 0x00008000
PAGE_LDM = 0x00020000
PAGE_STM = 0x00021000
PAGE_TPOP = 0x00022000
PAGE_TPUSH = 0x00023000

class GXemulSession:
    def __init__(self, bin_path, timeout=30):
        self.bin_path = bin_path
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(bin_path, [bin_path, "-V", "-A", "-T", "-E", "testarm", "-M", "64", "0x%x:%s" % (CODE, STUB)])
            os._exit(127)
        self.buf = ""
        self.dead = False
        self.wait_prompt(timeout)

    def rd(self, t=0.2):
        r, _, _ = select.select([self.fd], [], [], t)
        if self.fd not in r:
            return False
        try:
            d = os.read(self.fd, 65536)
        except OSError:
            self.dead = True
            return False
        if not d:
            self.dead = True
            return False
        self.buf += d.decode("latin1", "replace")
        return True

    def wait_prompt(self, timeout=20):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if self.dead:
                return False
            self.rd(0.1)
            if self.buf.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(self, cmd_str, timeout=15):
        if self.dead:
            return ""
        mark = len(self.buf)
        b = (cmd_str + "\n").encode("latin1")
        try:
            os.write(self.fd, b)
        except OSError:
            self.dead = True
            return ""
        t0 = time.time()
        while time.time() - t0 < timeout:
            if self.dead:
                return ""
            self.rd(0.1)
            if len(self.buf) > mark and self.buf[mark:].rstrip().endswith("GXemul>"):
                return self.buf[mark:]
        return ""

    def run_prog(self, prog_words, timeout=3.0):
        for i, w in enumerate(prog_words):
            self.send("put w 0x%x, 0x%08x" % (CODE + 4*i, w))
        self.send("pc=0x%x" % CODE)
        mark = len(self.buf)
        try:
            os.write(self.fd, b"continue\n")
        except OSError:
            self.dead = True
            return False
        t0 = time.time()
        while time.time() - t0 < timeout:
            self.rd(0.1)
        try:
            os.write(self.fd, b"\x03")
        except OSError:
            pass
        return self.wait_prompt(timeout=5)

    def get_reg(self, rname):
        raw = self.send("print %s" % rname)
        m = re.search(r"0x([0-9a-fA-F]+)", raw)
        return int(m.group(1), 16) if m else None

    def read_mem32(self, addr):
        #  *** DUMP FROM THE 16-BYTE-ALIGNED BASE, ALWAYS. ***  Measured
        #  2026-09-11: `dump` at an UNALIGNED start still labels the line
        #  with the aligned address but BLANK-PADS the leading word groups:
        #    aligned    0x00021000  00000000 44332211
        #    unaligned  0x00021000           44332211 00000000
        #  `.split()` collapses that padding, so every group index shifts
        #  and parts[idx] silently returns a NEIGHBOURING word.  Dumping
        #  from the aligned base keeps all four groups present, which is
        #  what the idx arithmetic below already assumes.
        base = addr & ~0xF
        raw = self.send("dump 0x%x 0x%x" % (base, base + 16))
        hex_addr = "0x%08x" % (addr & ~0xF)
        offset_in_16 = addr & 0xF
        for line in raw.splitlines():
            if line.startswith(hex_addr):
                parts = line[12:48].split()
                idx = offset_in_16 // 4
                if idx < len(parts):
                    hex_str = parts[idx]
                    if len(hex_str) == 8:
                        b0 = int(hex_str[0:2], 16)
                        b1 = int(hex_str[2:4], 16)
                        b2 = int(hex_str[4:6], 16)
                        b3 = int(hex_str[6:8], 16)
                        return b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)
        return None

    def get_tlb_page(self, vaddr):
        raw = self.send("tlbdump 0,r")
        hex_addr = "0x%08x" % (vaddr & ~0xFFF)
        for line in raw.splitlines():
            if hex_addr in line:
                m_load = re.search(r"load=([yn])", line)
                m_store = re.search(r"store=([yn])", line)
                load_ok = (m_load.group(1) == "y") if m_load else False
                store_ok = (m_store.group(1) == "y") if m_store else False
                return True, load_ok, store_ok
        return False, False, False

    def close(self):
        try:
            self.send("quit", timeout=2)
            os.kill(self.pid, 9)
            os.waitpid(self.pid, 0)
        except Exception:
            pass

def main():
    print(f"=== ARM BLOCK DATA TRANSFER WITNESS (armbdt)  LEG={LEG} ===")
    print(f"Binary: {BIN}")
    print("Core symptom: Unaligned base splices bytes across word boundary on cold host pages")
    print("Mandatory writeback: Unmasked Rn arithmetic preserved under W=1 Mode 4 transfers")
    print("")

    results = []
    failing = []

    def record(name, kind, ok, detail=""):
        res_str = "ok" if ok else "FAIL"
        print(f"{name:<34}  {kind:<8}  {detail:<38}  {res_str}", flush=True)
        results.append((name, kind, ok, detail))
        if not ok:
            failing.append(name)

    # -------------------------------------------------------------
    # 1. LIVENESS CONTROL: Aligned LDM/STM round-trip at 0x10000
    # -------------------------------------------------------------
    s = GXemulSession(BIN)
    s.send("put w 0x10000, 0xCAFEBABE")
    prog_ctrl = [0xe3a00801, 0xe8900002, 0xeafffffe]
    s.run_prog(prog_ctrl)
    val = s.get_reg("r1")
    s.close()
    ctrl_live = (val == 0xCAFEBABE)
    record("CONTROL_LIVENESS", "CTRL", ctrl_live, f"r1={val:#010x} want 0xcafebabe")

    # -------------------------------------------------------------
    # 2. CALLER 1: ARM LDM (X(bdt_load)) - COLD vs WARM
    # -------------------------------------------------------------
    # Cold run: seed 0x20000 with put b (CACHE_NONE | NO_EXCEPTIONS)
    s = GXemulSession(BIN)
    bytes_ldm = [0x44, 0x33, 0x22, 0x11, 0x88, 0x77, 0x66, 0x55]
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))
    in_tlb_cold, _, _ = s.get_tlb_page(PAGE_LDM)

    prog_ldm = [0xe3a00802, 0xe2800001, 0xe8900002, 0xeafffffe]
    s.run_prog(prog_ldm)
    r1_cold = s.get_reg("r1")
    s.close()

    # Warm run: seed 0x20000 with put w (CACHE_DATA warms page)
    s = GXemulSession(BIN)
    s.send("put w 0x%x, 0x11223344" % PAGE_LDM)
    s.send("put w 0x%x, 0x55667788" % (PAGE_LDM + 4))
    in_tlb_warm, _, _ = s.get_tlb_page(PAGE_LDM)
    s.run_prog(prog_ldm)
    r1_warm = s.get_reg("r1")
    s.close()

    # Attribution control (pre-fix bug produces exact spliced bytes)
    record("CONTROL_ATTRIB_PLUS1", "CTRL-A", (r1_cold == 0x88112233 or r1_cold == 0x11223344),
           f"cold r1={r1_cold:#010x} (bug=0x88112233)")

    record("ARM_LDM_PATH_COLD", "PATH", (not in_tlb_cold),
           f"page resident before cold={in_tlb_cold} want False")
    record("ARM_LDM_PATH_WARM", "PATH", in_tlb_warm,
           f"page resident before warm={in_tlb_warm} want True")
    record("ARM_LDM_COLD_DATA", "DATA", (r1_cold == 0x11223344),
           f"r1={r1_cold:#010x} want 0x11223344 (bug 0x88112233)")
    record("ARM_LDM_WARM_DATA", "DATA", (r1_warm == 0x11223344),
           f"r1={r1_warm:#010x} want 0x11223344")
    record("ARM_LDM_DIV_CHECK", "DISC", (r1_cold == r1_warm and r1_cold == 0x11223344),
           f"cold={r1_cold:#010x} warm={r1_warm:#010x}")

    #  ---- #524 clause-(d) closure: the +2 base ----
    #  M_MASK1 (the fix present, its mask weakened 0xfffffffc -> 0xfffffffe)
    #  scored 25/25 -- a MEASURED TOTAL ESCAPE -- because EVERY unaligned base
    #  above is +1, and x+1 & ~1 == x+1 & ~3.  A +2 base separates them:
    #  0x20002 & ~3 == 0x20000 (correct), 0x20002 & ~1 == 0x20002 (mutant).
    #  Predicted by arithmetic, then measured -- which is the order this
    #  project requires, because "it would sweep the table" is a measurement.
    #  +3 is deliberately NOT rowed: ~1 dies here at +2 and ~2 already dies at
    #  +1, so a +3 row buys no ENUMERATED mutant.  Residue 3 is disclosed in
    #  the contract instead.  Rows are owed per enumerated mutant, never per
    #  reachable value.
    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))
    in_tlb_p2, _, _ = s.get_tlb_page(PAGE_LDM)
    prog_ldm_p2 = [0xe3a00802, 0xe2800002, 0xe8900002, 0xeafffffe]
    s.run_prog(prog_ldm_p2)
    r1_p2 = s.get_reg("r1")
    s.close()
    record("ARM_LDM_PATH_COLD_P2", "PATH", (not in_tlb_p2),
           f"page resident before +2 cold={in_tlb_p2} want False")
    record("ARM_LDM_COLD_DATA_P2", "DATA", (r1_p2 == 0x11223344),
           f"r1={r1_p2:#010x} want 0x11223344 (mask1 mutant 0x77881122)")

    #  ==== CLASS CLOSURE, cell 1 of 3: WORD POSITION WITHIN THE 8-BYTE BLOCK ====
    #  The repair-chain pass found that `& ~7' (OVER-alignment) sweeps all 29
    #  assertions: every base the instrument drove -- 0x10000, 0x2000{1,2},
    #  0x2100{1,2} -- lies in the FIRST word of its 8-byte block, where ~3 and
    #  ~7 agree.  A base with ADDRESS BIT 2 SET separates them.
    #    0x20005 & ~3 == 0x20004  (correct -> bytes[4..7] = 88 77 66 55)
    #    0x20005 & ~7 == 0x20000  (mutant  -> bytes[0..3] = 44 33 22 11)
    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))
    prog_ldm_b2 = [0xe3a00802, 0xe2800005, 0xe8900002, 0xeafffffe]
    s.run_prog(prog_ldm_b2)
    r1_b2 = s.get_reg("r1")
    s.close()
    record("ARM_LDM_COLD_DATA_BIT2", "DATA", (r1_b2 == 0x55667788),
           f"r1={r1_b2:#010x} want 0x55667788 (mask~7 mutant 0x11223344)")

    #  ==== CLASS CLOSURE, THE p/u/s/w x SITE PRODUCT ON THE **LOAD** SIDE ====
    #
    #  *** PASS C MEASURED **FIVE** clause-(d) mutants at 32/32 -- a TOTAL ESCAPE
    #  EACH -- and they are all one class:  every p/u/s/w partition was
    #  discharged on the STORE side and undischarged on the LOAD side, because
    #  the only leg that varied any of those bits was Thumb PUSH, which calls
    #  arm_push().  arm_pop() was driven at exactly ONE (p,u,s) point: (0,1,0).
    #  Artifacts: regress/artifacts/armbdt/killtable_20260911f_opus/SCORES.txt
    #
    #     M_POPP_NONE   p_bit ? addr : (addr & ~3)            32/32
    #     M_POPP_WEAK   addr & (p_bit ? ~1 : ~3)              32/32
    #     M_POPW_WEAK   addr & (w_bit ? ~1 : ~3)              32/32
    #     M_SBIT_NONE   s_bit ? addr : (addr & ~3), BOTH      32/32
    #     M_NPMASK      (*np) & ~3 -- mask on the WRONG operand  32/32
    #
    #  M_POPP_NONE is clause (b) -- the removed defect reinstated VERBATIM --
    #  restricted to p_bit == 1.  A non-equivalence control ran LDMDB for real
    #  (ldmdb_*.out): BASE r1=0x55667788, mutant r1=0x00005566 (the FIX-ABSENT
    #  value), r0 writeback correct on both -- so these CORRUPT A GUEST REGISTER
    #  and are live defects, not equivalent mutants.
    #
    #  *** THE LOAD CELL COULD NOT BE CLOSED BY COPYING THE PUSH ROW: the only
    #  p_bit=1 caller in the instrument is Thumb PUSH, so closing it needs a NEW
    #  INSTRUCTION WORD, not a new base.  That is why it was missable. ***
    #
    #  All five rows below use a COLD page and a base at residue 2 (or a net
    #  access there), which is where ~1 and ~3 disagree.  bytes_ldm seeds
    #  0x11223344 at +0 and 0x55667788 at +4.

    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))   # put b = COLD seed
    prog_arm_ldm_ib_p2 = [0xe3a00802, 0xe2800002, 0xe9900002, 0xeafffffe]
    s.run_prog(prog_arm_ldm_ib_p2)
    arm_ldm_ib_p2_v = s.get_reg("r1")
    s.close()
    record("ARM_LDM_IB_P2", "DATA", (arm_ldm_ib_p2_v == 0x55667788),
           f"r1={arm_ldm_ib_p2_v:#010x} want 0x55667788  -- LDMIB r0,{{r1}} from 0x20002: PRE-increment gives access 0x20006 -> word at 0x20004. Closes pop x p_bit=1; kills M_POPP_NONE / M_POPP_WEAK")

    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))   # put b = COLD seed
    prog_arm_ldm_da_p2 = [0xe3a00802, 0xe2800006, 0xe8100002, 0xeafffffe]
    s.run_prog(prog_arm_ldm_da_p2)
    arm_ldm_da_p2_v = s.get_reg("r1")
    s.close()
    record("ARM_LDM_DA_P2", "DATA", (arm_ldm_da_p2_v == 0x55667788),
           f"r1={arm_ldm_da_p2_v:#010x} want 0x55667788  -- LDMDA r0,{{r1}} from 0x20006: post-DECREMENT, access 0x20006. Closes pop x u_bit=0")

    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))   # put b = COLD seed
    prog_arm_ldm_db_p2 = [0xe3a00802, 0xe280000a, 0xe9300002, 0xeafffffe]
    s.run_prog(prog_arm_ldm_db_p2)
    arm_ldm_db_p2_v = s.get_reg("r1")
    s.close()
    record("ARM_LDM_DB_P2", "DATA", (arm_ldm_db_p2_v == 0x55667788),
           f"r1={arm_ldm_db_p2_v:#010x} want 0x55667788  -- LDMDB r0!,{{r1}} from 0x2000a: PRE-decrement gives access 0x20006. Closes pop x (p=1,u=0); this exact word was the pass-C non-equivalence control")

    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))   # put b = COLD seed
    prog_arm_ldm_s_p2 = [0xe3a00802, 0xe2800002, 0xe8d00002, 0xeafffffe]
    s.run_prog(prog_arm_ldm_s_p2)
    arm_ldm_s_p2_v = s.get_reg("r1")
    s.close()
    record("ARM_LDM_S_P2", "DATA", (arm_ldm_s_p2_v == 0x11223344),
           f"r1={arm_ldm_s_p2_v:#010x} want 0x11223344  -- LDM r0,{{r1}}^ from 0x20002: S-bit form, access 0x20002 -> word at 0x20000. Closes s_bit; kills M_SBIT_NONE")

    #  THE BARGAIN ROW: one leg, THREE assertions.  A 2-register writeback load
    #  from residue 2 closes w_bit x residue-2 AND the register-list-length axis
    #  together, killing M_POPW_WEAK and M_NPMASK at once.  It has to be at +2:
    #  at the existing WB_UNAL2 base (0x20001/0x20005) the low bits are 01, where
    #  ~1 and ~3 AGREE, so that row cannot see a w_bit-conditioned weakening.
    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))   # put b = COLD seed
    prog_ldm_multi_p2 = [0xe3a00802, 0xe2800002, 0xe8b00006, 0xeafffffe]
    s.run_prog(prog_ldm_multi_p2)
    r1_mp2 = s.get_reg("r1")
    r2_mp2 = s.get_reg("r2")
    r0_mp2 = s.get_reg("r0")
    s.close()
    record("ARM_LDM_MULTI_P2_R1", "DATA", (r1_mp2 == 0x11223344),
           f"r1={r1_mp2:#010x} want 0x11223344  -- LDMIA r0!,{{r1,r2}} from 0x20002, first word")
    record("ARM_LDM_MULTI_P2_R2", "DATA", (r2_mp2 == 0x55667788),
           f"r2={r2_mp2:#010x} want 0x55667788  -- second word; kills M_NPMASK, which masks *np once")
    record("ARM_LDM_MULTI_P2_WB", "WB", (r0_mp2 == 0x2000a),
           f"r0={r0_mp2:#010x} want 0x0002000a  -- writeback keeps the RAW base; kills M_POPW_WEAK")


    # Writeback 1-reg: ldmia r0!, {r1} with unaligned base 0x20001
    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))
    prog_ldm_wb1 = [0xe3a00802, 0xe2800001, 0xe8b00002, 0xeafffffe]
    s.run_prog(prog_ldm_wb1)
    r0_wb1 = s.get_reg("r0")
    s.close()
    record("ARM_LDM_WB_UNAL1", "WB", (r0_wb1 == 0x20005),
           f"r0={r0_wb1:#010x} want 0x00020005 (mutant 0x00020004)")

    # Writeback 2-regs: ldmia r0!, {r1, r2} with unaligned base 0x20001
    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_LDM + i, b))
    prog_ldm_wb2 = [0xe3a00802, 0xe2800001, 0xe8b00006, 0xeafffffe]
    s.run_prog(prog_ldm_wb2)
    r0_wb2 = s.get_reg("r0")
    s.close()
    record("ARM_LDM_WB_UNAL2", "WB", (r0_wb2 == 0x20009),
           f"r0={r0_wb2:#010x} want 0x00020009 (mutant 0x00020008)")

    # -------------------------------------------------------------
    # 3. CALLER 2: ARM STM (X(bdt_store)) - COLD vs WARM
    # -------------------------------------------------------------
    # Cold STM: seed 0x21000..0x21007 with zeroes via put b
    s = GXemulSession(BIN)
    for i in range(8):
        s.send("put b 0x%x, 0x00" % (PAGE_STM + i))
    in_tlb_stm_cold, _, _ = s.get_tlb_page(PAGE_STM)

    prog_stm = [
        0xe59f0008, 0xe59f1008, 0xe8800002, 0xeafffffe,
        0x00021001, 0x11223344
    ]
    s.run_prog(prog_stm)
    r4_stm_cold = s.read_mem32(PAGE_STM)
    r5_stm_cold = s.read_mem32(PAGE_STM + 4)
    s.close()

    # Warm STM: seed 0x21000..0x21007 with zeroes via put w
    s = GXemulSession(BIN)
    s.send("put w 0x%x, 0x00000000" % PAGE_STM)
    s.send("put w 0x%x, 0x00000000" % (PAGE_STM + 4))
    in_tlb_stm_warm, _, _ = s.get_tlb_page(PAGE_STM)
    s.run_prog(prog_stm)
    r4_stm_warm = s.read_mem32(PAGE_STM)
    r5_stm_warm = s.read_mem32(PAGE_STM + 4)
    s.close()

    record("ARM_STM_PATH_COLD", "PATH", (not in_tlb_stm_cold),
           f"page resident before cold={in_tlb_stm_cold} want False")
    record("ARM_STM_PATH_WARM", "PATH", in_tlb_stm_warm,
           f"page resident before warm={in_tlb_stm_warm} want True")
    record("ARM_STM_COLD_DATA", "DATA", (r4_stm_cold == 0x11223344),
           f"w0={r4_stm_cold:#010x} want 0x11223344 (bug 0x22334400)")
    record("ARM_STM_COLD_CLOBBER", "DATA", (r5_stm_cold == 0x00000000),
           f"w1={r5_stm_cold:#010x} want 0x00000000 (bug 0x00000011)")
    record("ARM_STM_WARM_DATA", "DATA", (r4_stm_warm == 0x11223344 and r5_stm_warm == 0),
           f"w0={r4_stm_warm:#010x} w1={r5_stm_warm:#010x}")
    record("ARM_STM_DIV_CHECK", "DISC", (r4_stm_cold == r4_stm_warm and r4_stm_cold == 0x11223344),
           f"cold={r4_stm_cold:#010x} warm={r4_stm_warm:#010x}")

    #  ---- #524 clause-(d) closure: the +2 base, STM side ----
    #  Same discrimination on the store path.  Correct: the word lands at
    #  PAGE_STM.  Under ~1 the base stays 0x21002, so the bytes straddle and
    #  PAGE_STM reads 0x33440000 instead.
    s = GXemulSession(BIN)
    for i in range(8):
        s.send("put b 0x%x, 0x00" % (PAGE_STM + i))
    in_tlb_stm_p2, _, _ = s.get_tlb_page(PAGE_STM)
    prog_stm_p2 = [
        0xe59f0008, 0xe59f1008, 0xe8800002, 0xeafffffe,
        0x00021002, 0x11223344
    ]
    s.run_prog(prog_stm_p2)
    w0_p2 = s.read_mem32(PAGE_STM)
    s.close()
    record("ARM_STM_PATH_COLD_P2", "PATH", (not in_tlb_stm_p2),
           f"page resident before +2 cold={in_tlb_stm_p2} want False")
    record("ARM_STM_COLD_DATA_P2", "DATA", (w0_p2 == 0x11223344),
           f"w0={w0_p2:#010x} want 0x11223344 (mask1 mutant 0x33440000)")

    #  ==== CLASS CLOSURE, cell 2 of 3: the same word position, STORE side ====
    #    0x21005 & ~3 == 0x21004 (correct: word lands at PAGE_STM+4)
    #    0x21005 & ~7 == 0x21000 (mutant:  word lands at PAGE_STM)
    #  Both halves are asserted, so the row cannot pass by the value merely
    #  being absent from one place.
    s = GXemulSession(BIN)
    for i in range(8):
        s.send("put b 0x%x, 0x00" % (PAGE_STM + i))
    prog_stm_b2 = [
        0xe59f0008, 0xe59f1008, 0xe8800002, 0xeafffffe,
        0x00021005, 0x11223344
    ]
    s.run_prog(prog_stm_b2)
    w0_b2 = s.read_mem32(PAGE_STM)
    w1_b2 = s.read_mem32(PAGE_STM + 4)
    s.close()
    record("ARM_STM_COLD_DATA_BIT2", "DATA", (w1_b2 == 0x11223344 and w0_b2 == 0x00000000),
           f"w0={w0_b2:#010x} w1={w1_b2:#010x} want w1=0x11223344 w0=0 (mask~7 swaps them)")

    # Writeback STM: stmia r0!, {r1} with unaligned base 0x21001
    s = GXemulSession(BIN)
    for i in range(8):
        s.send("put b 0x%x, 0x00" % (PAGE_STM + i))
    prog_stm_wb = [
        0xe59f0008, 0xe59f1008, 0xe8a00002, 0xeafffffe,
        0x00021001, 0x11223344
    ]
    s.run_prog(prog_stm_wb)
    r0_stm_wb = s.get_reg("r0")
    s.close()
    record("ARM_STM_WB_UNAL", "WB", (r0_stm_wb == 0x21005),
           f"r0={r0_stm_wb:#010x} want 0x00021005 (mutant 0x00021004)")

    # -------------------------------------------------------------
    # 4. CALLER 3: Thumb POP (cpu_arm.c:1677) - COLD vs WARM
    # -------------------------------------------------------------
    # Cold Thumb POP:
    s = GXemulSession(BIN)
    for i, b in enumerate(bytes_ldm):
        s.send("put b 0x%x, 0x%02x" % (PAGE_TPOP + i, b))
    prog_tpop = [0xe59f0008, 0xe1a0d000, 0xe28f0005, 0xe12fff10, 0x00022001, 0xe7febc02]
    s.run_prog(prog_tpop)
    r1_tpop_cold = s.get_reg("r1")
    sp_tpop_cold = s.get_reg("sp")
    s.close()

    # Warm Thumb POP:
    s = GXemulSession(BIN)
    s.send("put w 0x%x, 0x11223344" % PAGE_TPOP)
    s.send("put w 0x%x, 0x55667788" % (PAGE_TPOP + 4))
    s.run_prog(prog_tpop)
    r1_tpop_warm = s.get_reg("r1")
    s.close()

    record("THUMB_POP_COLD_DATA", "DATA", (r1_tpop_cold == 0x11223344),
           f"r1={r1_tpop_cold:#010x} want 0x11223344 (bug 0x88112233)")
    record("THUMB_POP_WARM_DATA", "DATA", (r1_tpop_warm == 0x11223344),
           f"r1={r1_tpop_warm:#010x} want 0x11223344")
    record("THUMB_POP_DIV_CHECK", "DISC", (r1_tpop_cold == r1_tpop_warm and r1_tpop_cold == 0x11223344),
           f"cold={r1_tpop_cold:#010x} warm={r1_tpop_warm:#010x}")
    record("THUMB_POP_WB_UNAL", "WB", (sp_tpop_cold == 0x22005),
           f"sp={sp_tpop_cold:#010x} want 0x00022005 (mutant 0x00022004)")

    # -------------------------------------------------------------
    # 5. CALLER 4: Thumb PUSH (cpu_arm.c:1670) - COLD vs WARM
    # -------------------------------------------------------------
    # Thumb push {r1} decrements sp by 4 before store (stmdb sp!, {r1}).
    # Initial sp = 0x23005 -> decrements to 0x23001, stores r1 = 0x11223344.
    # Cold Thumb PUSH:
    s = GXemulSession(BIN)
    for i in range(8):
        s.send("put b 0x%x, 0x00" % (PAGE_TPUSH + i))
    prog_tpush = [
        0xe59f0014,  # 0x8000: ldr r0, [pc, #20] -> loads 0x23005 at 0x801c
        0xe1a0d000,  # 0x8004: mov sp, r0
        0xe59f1010,  # 0x8008: ldr r1, [pc, #16] -> loads 0x11223344 at 0x8020
        0xe28f0005,  # 0x800c: add r0, pc, #5    -> 0x8019 (target 0x8018 | 1)
        0xe12fff10,  # 0x8010: bx r0
        0xe1a00000,  # 0x8014: nop
        0xe7feb402,  # 0x8018: push {r1} (0xb402), b . (0xe7fe)
        0x00023005,  # 0x801c
        0x11223344   # 0x8020
    ]
    s.run_prog(prog_tpush)
    sp_tpush_cold = s.get_reg("sp")
    r4_tpush_cold = s.read_mem32(PAGE_TPUSH)
    r5_tpush_cold = s.read_mem32(PAGE_TPUSH + 4)
    s.close()

    # Warm Thumb PUSH:
    s = GXemulSession(BIN)
    s.send("put w 0x%x, 0x00000000" % PAGE_TPUSH)
    s.send("put w 0x%x, 0x00000000" % (PAGE_TPUSH + 4))
    s.run_prog(prog_tpush)
    r4_tpush_warm = s.read_mem32(PAGE_TPUSH)
    r5_tpush_warm = s.read_mem32(PAGE_TPUSH + 4)
    s.close()

    record("THUMB_PUSH_COLD_DATA", "DATA", (r4_tpush_cold == 0x11223344),
           f"w0={r4_tpush_cold:#010x} want 0x11223344 (bug 0x22334400)")
    record("THUMB_PUSH_COLD_CLOBBER", "DATA", (r5_tpush_cold == 0x00000000),
           f"w1={r5_tpush_cold:#010x} want 0x00000000 (bug 0x00000011)")
    record("THUMB_PUSH_WARM_DATA", "DATA", (r4_tpush_warm == 0x11223344 and r5_tpush_warm == 0),
           f"w0={r4_tpush_warm:#010x} w1={r5_tpush_warm:#010x}")
    record("THUMB_PUSH_DIV_CHECK", "DISC", (r4_tpush_cold == r4_tpush_warm and r4_tpush_cold == 0x11223344),
           f"cold={r4_tpush_cold:#010x} warm={r4_tpush_warm:#010x}")

    #  ==== CLASS CLOSURE, cell 3 of 3: THE PREDICATE AXIS (p_bit) ====
    #  The repair-chain pass found a CONDITIONAL weakening that sweeps all 29:
    #  mask 0xfffffffe when p_bit is true, 0xfffffffc when false.  Every ARM STM
    #  run uses IA (p_bit=0) and gets the correct mask; Thumb PUSH uses DB
    #  (p_bit=1) and gets the weakened one -- but its only effective address was
    #  PAGE_TPUSH+1, where ~1 and ~3 AGREE.  So the predicate axis was exercised
    #  at exactly one residue and the conditional was invisible.
    #
    #  sp starts 0x23006; push {r1} is stmdb sp!, so it decrements to 0x23002.
    #    0x23002 & ~3 == 0x23000  (correct -> word at PAGE_TPUSH = 0x11223344)
    #    0x23002 & ~1 == 0x23002  (mutant  -> straddles; PAGE_TPUSH = 0x33440000)
    s = GXemulSession(BIN)
    for i in range(8):
        s.send("put b 0x%x, 0x00" % (PAGE_TPUSH + i))
    prog_tpush_p2 = [
        0xe59f0014, 0xe1a0d000, 0xe59f1010, 0xe28f0005,
        0xe12fff10, 0xe1a00000, 0xe7feb402,
        0x00023006, 0x11223344
    ]
    s.run_prog(prog_tpush_p2)
    w0_tp2 = s.read_mem32(PAGE_TPUSH)
    s.close()
    record("THUMB_PUSH_COLD_DATA_P2", "DATA", (w0_tp2 == 0x11223344),
           f"w0={w0_tp2:#010x} want 0x11223344 (p_bit-conditional mutant 0x33440000)")
    record("THUMB_PUSH_WB_UNAL", "WB", (sp_tpush_cold == 0x23001),
           f"sp={sp_tpush_cold:#010x} want 0x00023001 (mutant 0x00023000)")

    # -------------------------------------------------------------
    # SUMMARY & SENTINEL
    # -------------------------------------------------------------
    n_ok = sum(1 for _, _, ok, _ in results if ok)
    n_total = len(results)
    print("")
    print(f"SCORE {n_ok}/{n_total}")
    #  Gate-idiom lines, matching the other ARM probes in gate_arm.sh.
    #  PRINT-ONLY: no row verdict depends on them, so adding them does not
    #  change the instrument the kill tables measured.
    ctrl = "OK" if all(ok for name, _, ok, _ in results
                       if name.startswith("CONTROL_")) else "BROKEN"
    print(f"ARMBDT_CONTROL={ctrl}")
    print(f"ARMBDT_RESULT={n_ok}/{n_total}")
    if failing:
        print(f"FAILING: {','.join(failing)}")
    else:
        print("FAILING: none")
    print("ARMBDT_WITNESS_DONE")

if __name__ == "__main__":
    main()
