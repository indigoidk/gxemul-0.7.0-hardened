#!/usr/bin/env python3
"""
agy_xscale_witness_20260911.py -- Rung-3 witness for xscaleinten on -E iq80321.
"""

import os, sys, pty, select, time, re

BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxxscale/gxemul"
LEG = sys.argv[2] if len(sys.argv) > 2 else "BASE"
STUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "regress", "arm_bfx_stub.bin")
if not os.path.exists(STUB):
    STUB = "/tmp/stub.bin"
    if not os.path.exists(STUB):
        with open(STUB, "wb") as f:
            f.write(bytes(16))

CODE = 0x00008000
S1 = 0xA500005A
S2 = 0x5AA5F00D
TRR0_SEED = 0x11112222
MARKER = 0x5A
NOP = 0xE1A00000

def hexs(v):
    return "-" if v is None else ("0x%08x" % v if isinstance(v, int) else str(v))

class Session:
    def __init__(self, bin_path, timeout=60):
        self.bin_path = bin_path
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(bin_path, [bin_path, "-V", "-T", "-E", "iq80321", "-M", "32", "0x%x:%s" % (CODE, STUB)])
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

    def wait_prompt(self, timeout=30):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if self.dead:
                return False
            self.rd(0.1)
            if self.buf.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(self, cmd_str, timeout=30):
        if self.dead:
            return False
        b = (cmd_str + "\n").encode("latin1")
        try:
            os.write(self.fd, b)
        except OSError:
            self.dead = True
            return False
        return self.wait_prompt(timeout)

    def get_regs(self):
        regs = {}
        if self.dead:
            return regs
        mark = len(self.buf)
        if self.send("reg", timeout=10):
            seg = self.buf[mark:]
            for m in re.finditer(r"\br([0-9]+)\s*=\s*0x([0-9a-fA-F]+)", seg):
                regs[int(m.group(1))] = int(m.group(2), 16)
            slm = re.search(r"\bsl\s*=\s*0x([0-9a-fA-F]+)", seg)
            if slm:
                regs[10] = int(slm.group(1), 16)
            fpm = re.search(r"\bfp\s*=\s*0x([0-9a-fA-F]+)", seg)
            if fpm:
                regs[11] = int(fpm.group(1), 16)
            ipm = re.search(r"\bip\s*=\s*0x([0-9a-fA-F]+)", seg)
            if ipm:
                regs[12] = int(ipm.group(1), 16)
            spm = re.search(r"\bsp\s*=\s*0x([0-9a-fA-F]+)", seg)
            if spm:
                regs[13] = int(spm.group(1), 16)
            lrm = re.search(r"\blr\s*=\s*0x([0-9a-fA-F]+)", seg)
            if lrm:
                regs[14] = int(lrm.group(1), 16)
                regs["lr"] = int(lrm.group(1), 16)
            pm = re.search(r"\bpc\s*=\s*0x([0-9a-fA-F]+)", seg)
            if pm:
                regs["pc"] = int(pm.group(1), 16)
            cpm = re.search(r"\bcpsr\s*=\s*([a-zA-Z]+)", seg)
            if cpm:
                regs["cpsr"] = cpm.group(1)
        return regs

    def close(self):
        try:
            os.write(self.fd, b"quit\n")
            time.sleep(0.1)
        except OSError:
            pass
        try:
            os.close(self.fd)
        except OSError:
            pass
        try:
            _, st = os.waitpid(self.pid, 0)
            code = os.WEXITSTATUS(st) if os.WIFEXITED(st) else None
            sig = os.WTERMSIG(st) if os.WIFSIGNALED(st) else None
        except Exception:
            code, sig = None, None
        return code, sig, self.buf

def run():
    print(f"=== XSCALEINTEN WITNESS [{LEG}] ===")
    print(f"BINARY: {BIN}")
    rows = []
    
    def report_row(tag, desc, got, want, ok):
        st = "ok" if ok else "FAIL"
        print(f"{tag:<16} {desc:<48} got={hexs(got):<14} want={hexs(want):<14} {st}")
        rows.append((tag, ok, desc, got, want))
        return ok

    # -------------------------------------------------------------
    # ARM D: Value Tracking & Subject Reads
    # -------------------------------------------------------------
    s = Session(BIN)
    for i in range(11):
        s.send(f"r{i}=0xdeadbe{i:02x}")
    s.send(f"r1=0x{S1:08x}")
    s.send("r2=0x00000000")
    s.send(f"r3=0x{S2:08x}")
    s.send(f"r7=0x{TRR0_SEED:08x}")

    prog_d = [
        (0x00, 0xEE047611, "mcr 6,0,r7,cr4,cr1,0"),      # seed trr0
        (0x04, 0xEE148611, "mrc 6,0,r8,cr4,cr1,0"),      # read trr0 (CP6 liveness)
        (0x08, 0xEE109610, "mrc 6,0,r9,cr0,cr0,0"),      # read inten at reset (expect 0)
        (0x0C, 0xEE001610, "mcr 6,0,r1,cr0,cr0,0"),      # inten <- S1
        (0x10, 0xEE104610, "mrc 6,0,r4,cr0,cr0,0"),      # read inten (expect S1)
        (0x14, 0xEE002610, "mcr 6,0,r2,cr0,cr0,0"),      # inten <- 0
        (0x18, 0xEE105610, "mrc 6,0,r5,cr0,cr0,0"),      # read inten (expect 0)
        (0x1C, 0xEE003610, "mcr 6,0,r3,cr0,cr0,0"),      # inten <- S2
        (0x20, 0xEE106610, "mrc 6,0,r6,cr0,cr0,0"),      # read inten (expect S2)
        (0x24, 0xEE10A630, "mrc 6,0,r10,cr0,cr0,1"),     # 4th read: opcode2=1 (expect S2)
        (0x28, 0xE3A0005A, "mov r0,#0x5a"),              # continuation marker
        (0x2C, NOP,        "mov r0,r0")                   # landing pad
    ]
    for off, w, _ in prog_d:
        s.send(f"put w 0x{CODE+off:08x}, 0x{w:08x}")
    s.send(f"pc=0x{CODE:08x}")

    dest_map = {0x08: 9, 0x10: 4, 0x18: 5, 0x20: 6, 0x24: 10}
    expect_map = {0x08: 0, 0x10: S1, 0x18: 0, 0x20: S2, 0x24: S2}
    pre_snapshots = {}
    post_snapshots = {}
    d_died_at = None

    for off, w, dis in prog_d[:-1]:
        if off in dest_map:
            regs_pre = s.get_regs()
            pre_snapshots[off] = regs_pre.get(dest_map[off])
        
        ok = s.send("step 1", timeout=10)
        if not ok or s.dead:
            d_died_at = off
            break
        
        # Snapshot immediately after step while alive
        if off in (0x04, 0x08, 0x10, 0x18, 0x20, 0x24, 0x28):
            post_snapshots[off] = s.get_regs()

    code_d, sig_d, buf_d = s.close()

    # P2 Vacuity Guard Check
    vacuity_violated = False
    for off, rd in dest_map.items():
        val = pre_snapshots.get(off)
        if val is not None and val == expect_map[off]:
            vacuity_violated = True

    report_row("P2_VACUITY", "D: subject dest held poison pre-step",
               "VOID" if vacuity_violated else "POISON_CLEAN",
               "POISON_CLEAN",
               not vacuity_violated)

    # A2 Check: no generic uninstalled coproc message
    a2_bad = "[ TODO: arm_mcr_mrc:" in buf_d and "cp_num=6" in buf_d
    report_row("A2_INSTALLED", "CP6 is installed in IQ80321",
               "ABSENT" if not a2_bad else "FOUND",
               "ABSENT",
               not a2_bad)

    # Check TRR0 liveness (stepped at 0x04)
    r8_trr0 = post_snapshots.get(0x04, {}).get(8)
    report_row("D_TRR0", "D: trr0 CP6 liveness", r8_trr0, TRR0_SEED, r8_trr0 == TRR0_SEED)

    # Check TODO text absence in D
    d_todo = "TODO: XScale read from inten?" in buf_d
    report_row("D_TODO_ABS", "D: TODO read diagnostic absent",
               "ABSENT" if not d_todo else "PRESENT",
               "ABSENT",
               not d_todo)

    if d_died_at is not None:
        report_row("D_SURVIVE", "D: ran to marker without exit(1)", f"died@0x{d_died_at:02x}", "SURVIVED", False)
        report_row("D_RESET", "D: inten reset val (rd=9)", "VOID" if vacuity_violated else "-", 0, False)
        report_row("D_S1", "D: inten read S1 (rd=4)", "VOID" if vacuity_violated else "-", S1, False)
        report_row("D_ZERO", "D: inten read 0 (rd=5)", "VOID" if vacuity_violated else "-", 0, False)
        report_row("D_S2", "D: inten read S2 (rd=6)", "VOID" if vacuity_violated else "-", S2, False)
        report_row("D_OP2", "D: inten read opcode2=1 (rd=10)", "VOID" if vacuity_violated else "-", S2, False)
        report_row("D_MARKER", "D: marker reached (r0=0x5a)", "-", MARKER, False)
    else:
        regs_final = post_snapshots.get(0x28, {})
        report_row("D_SURVIVE", "D: ran to marker without exit(1)", "SURVIVED", "SURVIVED", True)
        report_row("D_RESET", "D: inten reset val (rd=9)", "VOID" if vacuity_violated else regs_final.get(9), 0, (not vacuity_violated) and regs_final.get(9) == 0)
        report_row("D_S1", "D: inten read S1 (rd=4)", "VOID" if vacuity_violated else regs_final.get(4), S1, (not vacuity_violated) and regs_final.get(4) == S1)
        report_row("D_ZERO", "D: inten read 0 (rd=5)", "VOID" if vacuity_violated else regs_final.get(5), 0, (not vacuity_violated) and regs_final.get(5) == 0)
        report_row("D_S2", "D: inten read S2 (rd=6)", "VOID" if vacuity_violated else regs_final.get(6), S2, (not vacuity_violated) and regs_final.get(6) == S2)
        report_row("D_OP2", "D: inten read opcode2=1 (rd=10)", "VOID" if vacuity_violated else regs_final.get(10), S2, (not vacuity_violated) and regs_final.get(10) == S2)
        report_row("D_MARKER", "D: marker reached (r0=0x5a)", regs_final.get(0), MARKER, regs_final.get(0) == MARKER)

    # -------------------------------------------------------------
    # ARM LNC: Condition, NOP, Subject read
    # -------------------------------------------------------------
    s_lnc = Session(BIN)
    s_lnc.send("r0=0xdeadbe00")
    s_lnc.send(f"r1=0x{S1:08x}")
    s_lnc.send("r3=0xdeadbe03")

    prog_lnc = [
        (0x00, 0xEE001610, "mcr 6,0,r1,cr0,cr0,0"),  # inten <- S1
        (0x04, 0x0E103610, "mrceq 6,0,r3,cr0,cr0,0"),# cond EQ is false -> must NOT touch r3
        (0x08, NOP,        "mov r0,r0"),              # NOP -> dest r0 must not hold S1
        (0x0C, 0xEE103610, "mrc 6,0,r3,cr0,cr0,0"),  # subject read -> MUST write S1 to r3
        (0x10, 0xE3A0005A, "mov r0,#0x5a"),          # marker
        (0x14, NOP,        "mov r0,r0")               # landing pad
    ]
    for off, w, _ in prog_lnc:
        s_lnc.send(f"put w 0x{CODE+off:08x}, 0x{w:08x}")
    s_lnc.send(f"pc=0x{CODE:08x}")

    s_lnc.send("step 1") # mcr
    s_lnc.send("step 1") # mrceq
    r_after_mrceq = s_lnc.get_regs().get(3)
    report_row("LNC_COND", "LNC: mrceq preserves poison in r3",
               r_after_mrceq, 0xDEADBE03, r_after_mrceq == 0xDEADBE03)

    s_lnc.send("step 1") # NOP
    r0_after_nop = s_lnc.get_regs().get(0)
    r3_before_sub = s_lnc.get_regs().get(3)
    report_row("X4_NOP", "LNC: NOP dest r0 does NOT hold S1",
               r0_after_nop, 0xDEADBE00, r0_after_nop != S1 and r0_after_nop == 0xDEADBE00)
    report_row("LNC_P2", "LNC: r3 poison preserved before subject",
               r3_before_sub, 0xDEADBE03, r3_before_sub == 0xDEADBE03)

    ok_sub = s_lnc.send("step 1") # subject mrc
    lnc_died = (not ok_sub) or s_lnc.dead

    if lnc_died:
        code_lnc, _, buf_lnc = s_lnc.close()
        lnc_todo = "TODO: XScale read from inten?" in buf_lnc
        report_row("LNC_TODO_ABS", "LNC: TODO read diagnostic absent",
                   "ABSENT" if not lnc_todo else "PRESENT",
                   "ABSENT",
                   not lnc_todo)
        report_row("LNC_SUB", "LNC: subject mrc r3 <- S1", "HOST-DIED", hexs(S1), False)
        report_row("LNC_MARKER", "LNC: marker reached (r0=0x5a)", "HOST-DIED", hexs(MARKER), False)
    else:
        r3_after_sub = s_lnc.get_regs().get(3)
        s_lnc.send("step 1") # marker
        r0_marker = s_lnc.get_regs().get(0)
        code_lnc, _, buf_lnc = s_lnc.close()
        lnc_todo = "TODO: XScale read from inten?" in buf_lnc
        report_row("LNC_TODO_ABS", "LNC: TODO read diagnostic absent",
                   "ABSENT" if not lnc_todo else "PRESENT",
                   "ABSENT",
                   not lnc_todo)
        report_row("LNC_SUB", "LNC: subject mrc r3 <- S1",
                   r3_after_sub, S1, r3_after_sub == S1)
        report_row("LNC_MARKER", "LNC: marker reached (r0=0x5a)",
                   r0_marker, MARKER, r0_marker == MARKER)

    # -------------------------------------------------------------
    # ARM E: Unknown register / opcode -> MUST DIE both builds
    # -------------------------------------------------------------
    s_e = Session(BIN)
    s_e.send(f"put w 0x{CODE:08x}, 0xee79b6b2")
    s_e.send(f"pc=0x{CODE:08x}")
    s_e.send("step 1", timeout=5)
    code_e, _, buf_e = s_e.close()
    e_died = (code_e == 1) or s_e.dead
    e_msg = ("arm_coproc_i80321_6: unimplemented opcode1=3 opcode2=5 crn=9 crm=2 rd=11 l=1" in buf_e)
    report_row("E_UNKNOWN", "E: unknown opcode dies with 6 fields",
               "DIED_WITH_MSG" if (e_died and e_msg) else ("DIED" if e_died else "SURVIVED"),
               "DIED_WITH_MSG",
               e_died and e_msg)

    # -------------------------------------------------------------
    # ARM S: ISRC write kill -> MUST DIE both builds
    # -------------------------------------------------------------
    s_s = Session(BIN)
    s_s.send(f"put w 0x{CODE:08x}, 0xee080610")
    s_s.send(f"pc=0x{CODE:08x}")
    s_s.send("step 1", timeout=5)
    code_s, _, buf_s = s_s.close()
    s_died = (code_s == 1) or s_s.dead
    s_msg = ("TODO: XScale int ack?" in buf_s)
    report_row("S_ISRC_WR", "S: isrc write dies (exit 1)",
               "DIED_WITH_MSG" if (s_died and s_msg) else ("DIED" if s_died else "SURVIVED"),
               "DIED_WITH_MSG",
               s_died and s_msg)

    # -------------------------------------------------------------
    # ARM SIB: crn=4 sibling pair
    # -------------------------------------------------------------
    # SIB_R: crn=4 silent-accept READ (survives both)
    s_sibr = Session(BIN)
    s_sibr.send("r0=0xdeadbe00")
    s_sibr.send(f"put w 0x{CODE:08x}, 0xee147610")
    s_sibr.send(f"put w 0x{CODE+4:08x}, 0xe3a0005a")
    s_sibr.send(f"pc=0x{CODE:08x}")
    s_sibr.send("step 1")
    s_sibr.send("step 1")
    r0_sibr = s_sibr.get_regs().get(0)
    report_row("SIB_READ", "SIB: crn-4 read silent-accept",
               r0_sibr, MARKER, r0_sibr == MARKER)
    s_sibr.close()

    # SIB_W: crn=4 non-zero store (dies both)
    s_sibw = Session(BIN)
    s_sibw.send(f"r1=0x{S1:08x}")
    s_sibw.send(f"put w 0x{CODE:08x}, 0xee041610")
    s_sibw.send(f"pc=0x{CODE:08x}")
    s_sibw.send("step 1", timeout=5)
    code_sibw, _, buf_sibw = s_sibw.close()
    sibw_died = (code_sibw == 1) or s_sibw.dead
    sibw_msg = ("ARM xscale interrupt steering is not yet implemented" in buf_sibw)
    report_row("SIB_WRITE", "SIB: crn-4 non-zero store dies",
               "DIED_WITH_MSG" if (sibw_died and sibw_msg) else ("DIED" if sibw_died else "SURVIVED"),
               "DIED_WITH_MSG",
               sibw_died and sibw_msg)

    # -------------------------------------------------------------
    # ARM RD15: Destination PC (r15)
    # -------------------------------------------------------------
    s_r15 = Session(BIN)
    s_r15.send("r0=0xdeadbe00")
    s_r15.send(f"r1=0x{S1:08x}")
    s_r15.send(f"put w 0x{CODE:08x}, 0xee001610")      # mcr inten <- S1
    s_r15.send(f"put w 0x{CODE+0x04:08x}, 0xee10f610") # mrc 6,0,r15,cr0,cr0,0 (rd=15)
    s_r15.send(f"put w 0x{CODE+0x08:08x}, 0xe3a0005a") # mov r0,#0x5a (marker)
    s_r15.send(f"put w 0x{CODE+0x0C:08x}, 0xe1a00000") # landing pad
    s_r15.send(f"pc=0x{CODE:08x}")
    s_r15.send("step 1") # mcr
    ok_r15 = s_r15.send("step 1") # mrc to r15
    if (not ok_r15) or s_r15.dead:
        report_row("RD15_SURVIVE", "RD15: read into r15 survives to marker", "HOST-DIED", hexs(MARKER), False)
    else:
        s_r15.send("step 1") # marker mov r0, #0x5a
        r0_r15 = s_r15.get_regs().get(0)
        report_row("RD15_SURVIVE", "RD15: read into r15 survives to marker",
                   r0_r15, MARKER, r0_r15 == MARKER)
    s_r15.close()

    # -------------------------------------------------------------
    # ARM ANCHOR: Free-running Interrupt Trigger & Contrast
    # -------------------------------------------------------------
    s_anc = Session(BIN)
    s_anc.send("r1=0x10000000")
    s_anc.send("r2=0xfe800000")
    s_anc.send("r3=0x02")
    s_anc.send("r4=0x08")
    s_anc.send("r7=0xdeadbe07")
    s_anc.send("r9=0xdeadbe09")

    prog_anc = [
        (0x00, NOP,        "mov r0,r0"),          # 0x00: step 1 tick burn
        (0x04, 0xEE001610, "mcr 6,0,r1,cr0,cr0,0"), # 0x04: inten <- 0x10000000
        (0x08, 0xE5C23001, "strb r3,[r2,#1]"),     # 0x08: com_ier <- 2
        (0x0C, 0xE5C24004, "strb r4,[r2,#4]"),     # 0x0C: com_mcr <- 8 (asserts irq 28)
        (0x10, 0xEE187610, "mrc 6,0,r7,cr8,cr0,0"), # 0x10: read isrc back -> r7
        (0x14, 0xEE109610, "mrc 6,0,r9,cr0,cr0,0"), # 0x14: read inten back while isrc!=0 -> r9 (M1 trap!)
        (0x18, 0xE10F5000, "mrs r5,cpsr"),
        (0x1C, 0xE3C55080, "bic r5,r5,#0x80"),
        (0x20, 0xE121F005, "msr cpsr_c,r5"),
        (0x24, 0xEAFFFFFE, "b .")
    ]
    for off, w, _ in prog_anc:
        s_anc.send(f"put w 0x{CODE+off:08x}, 0x{w:08x}")
    s_anc.send(f"pc=0x{CODE:08x}")

    post_anc = {}
    anc_died_at = None
    for off, _, _ in prog_anc[:6]:
        ok = s_anc.send("step 1")
        if not ok or s_anc.dead:
            anc_died_at = off
            break
        post_anc[off] = s_anc.get_regs()

    r7_isrc = post_anc.get(0x10, {}).get(7)
    r9_inten = post_anc.get(0x14, {}).get(9)

    report_row("ANCHOR_ISRC", "ANCHOR: isrc has bit 28 asserted",
               r7_isrc, 0x10000000, r7_isrc == 0x10000000)
    report_row("ANCHOR_M1", "ANCHOR: inten read while isrc!=0 (M1 floor)",
               r9_inten, 0x10000000, r9_inten == 0x10000000)

    if s_anc.dead:
        report_row("ANCHOR_EXC", "ANCHOR: IRQ exception reached vector 0x18", "HOST-DIED", "0x00000018", False)
    else:
        for off, _, _ in prog_anc[6:]:
            s_anc.send("step 1")
        s_anc.send("breakpoint add 0x18")
        s_anc.send("continue", timeout=3)
        regs_anc_cont = s_anc.get_regs()
        pc_hit = regs_anc_cont.get("pc")
        report_row("ANCHOR_EXC", "ANCHOR: IRQ exception reached vector 0x18",
                   pc_hit, 0x00000018, pc_hit == 0x00000018)
    s_anc.close()

    # ANCHOR_CONTRAST: inten = 0 -> spins in b ., vector 0x18 never reached
    s_ctl = Session(BIN)
    s_ctl.send("r1=0x00000000")
    s_ctl.send("r2=0xfe800000")
    s_ctl.send("r3=0x02")
    s_ctl.send("r4=0x08")
    for off, w, _ in prog_anc:
        s_ctl.send(f"put w 0x{CODE+off:08x}, 0x{w:08x}")
    s_ctl.send(f"pc=0x{CODE:08x}")
    
    ctl_died = False
    for off, _, _ in prog_anc:
        ok = s_ctl.send("step 1")
        if not ok or s_ctl.dead:
            ctl_died = True
            break
            
    if ctl_died:
        pc_ctl = "HOST-DIED"
    else:
        s_ctl.send("breakpoint add 0x18")
        os.write(s_ctl.fd, b"continue\n")
        time.sleep(0.4)
        try:
            os.write(s_ctl.fd, b"\x03")
            s_ctl.wait_prompt(2)
            regs_ctl = s_ctl.get_regs()
            pc_ctl = regs_ctl.get("pc")
        except:
            pc_ctl = None
    s_ctl.close()
    report_row("ANCHOR_CONTRAST", "ANCHOR: inten=0 spins, 0x18 never reached",
               pc_ctl, CODE+0x24, pc_ctl == (CODE+0x24))

    passed = sum(1 for _, ok, _, _, _ in rows if ok)
    total = len(rows)
    failing = [tag for tag, ok, _, _, _ in rows if not ok]
    print()
    print(f"SCORE {passed}/{total}")
    if failing:
        print(f"FAILING: {', '.join(failing)}")
    else:
        print("FAILING: NONE")
    print("XSCALE_WITNESS_DONE")
    return passed, total

if __name__ == "__main__":
    run()
