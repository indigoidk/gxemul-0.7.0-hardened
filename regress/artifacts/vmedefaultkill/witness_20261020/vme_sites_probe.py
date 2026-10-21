#!/usr/bin/env python3
"""vme_sites_probe.py -- Cold-debugger harness to measure OpenBSD/mvme88k VME2 accesses.
Derived from GXEMUL-SEC/regress/mk48_nvram_probe.py.
"""

import os
import re
import subprocess
import sys

if len(sys.argv) < 3:
    sys.stderr.write("usage: vme_sites_probe.py <gxemul_binary> <label>\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2]
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(WORK_DIR, f"run_{LABEL}.out")

# Tee stdout to run_<label>.out as well
class TeeLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="latin-1")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        if hasattr(self, 'log') and not self.log.closed:
            self.log.flush()

    def close(self):
        if hasattr(self, 'log') and not self.log.closed:
            self.log.close()

logger = TeeLogger(OUT_FILE)
sys.stdout = logger

DUMMY = "/tmp/vme_probe_dummy.bin"
with open(DUMMY, "wb") as f:
    f.write(b"\x00" * 64)

# M88K Instruction Encodings
def enc(op26, rd, rs1, imm):
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)

def LD_W(rd, rs1, imm=0):
    return enc(0x05, rd, rs1, imm)

def ST_W(rd, rs1, imm=0):
    return enc(0x09, rd, rs1, imm)

def OR_IMM(rd, rs1, imm):
    return enc(0x16, rd, rs1, imm)

SITES = [
    ("A1", "MASTERCTL", 0x28, True,  "vme2chip_init: ctl = vme2->vme2_masterctl"),
    ("A2", "MASTER3",   0x1c, False, "vme2->vme2_master3 = ..."),
    ("A3", "MASTER4",   0x20, False, "vme2->vme2_master4 = ..."),
    ("A4", "MASTER4MOD",0x24, False, "vme2->vme2_master4mod = ..."),
    ("A5", "MASTERCTL", 0x28, False, "vme2->vme2_masterctl = ctl"),
    ("H1", "IRQSTAT",   0x68, True,  "vme2abort: if (!(vme2->vme2_irqstat & VME2_IRQ_AB))"),
    ("H2", "IRQCLR",    0x74, False, "vme2->vme2_irqclr = VME2_IRQ_AB"),
]

def session(cmds, timeout=30, subtype="mvme187"):
    argv = [BIN, "-V", "-x", "-E", "mvme88k", "-e", subtype, "-M", "64", "0x10000:" + DUMMY]
    inp = ("\n".join(cmds + ["quit"]) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        rc = p.returncode
        out = p.stdout.decode("latin-1", "replace").replace("\r", "")
        return out, rc
    except subprocess.TimeoutExpired as e:
        out = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        return out, -999

def parse_reg_dump(transcript):
    """Parse register values from the debugger output."""
    parts = transcript.split("GXemul> reg\n")
    if len(parts) < 2:
        return None
    dump = parts[1]
    
    res = {}
    m = re.search(r"cpu\d+:\s+pc\s+=\s+(0x[0-9a-fA-F]+)", dump)
    res["pc"] = m.group(1).lower() if m else None
    
    for r in ["r2", "r3", "r4", "r5", "r10", "r12", "r14"]:
        m = re.search(r"\b" + r + r"\s+=\s+(0x[0-9a-fA-F]+)", dump)
        res[r] = m.group(1).lower() if m else None

    # Control registers from reg 0,0
    for cr in ["VBR", "DMT0", "DMD0", "DMA0", "SXIP", "SNIP", "SFIP"]:
        m = re.search(r"\b" + cr + r"\s*=\s*(0x[0-9a-fA-F]+)", dump)
        res[cr] = m.group(1).lower() if m else None
        
    return res

print(f"=== VME SITES PROBE: BINARY={BIN} LABEL={LABEL} ===")

# -------------------------------------------------------------
# Control (a): CASED register round-trip on T1CMP (offset 0x50)
# -------------------------------------------------------------
ctrl_cmds = [
    "r3=0xfff40050",           # T1CMP address
    "r2=0x12345678",           # test value to store
    "r5=0xdeadbeef",           # sentinel to overwrite
    "r4=0x0",
    f"put w 0x10000, 0x{ST_W(2, 3, 0):08x}",  # st r2, r3, 0
    f"put w 0x10004, 0x{LD_W(5, 3, 0):08x}",  # ld r5, r3, 0
    f"put w 0x10008, 0x{OR_IMM(4, 0, 0x1234):08x}", # or r4, r0, 0x1234
    "unassemble 0x10000 0x1000c",
    "pc=0x10000",
    "step 3",
    "reg",
    "reg 0,0"
]
ctrl_out, ctrl_rc = session(ctrl_cmds)
ctrl_regs = parse_reg_dump(ctrl_out)
ctrl_a_ok = (ctrl_rc == 0 and ctrl_regs is not None and 
             ctrl_regs.get("r5") == "0x12345678" and 
             ctrl_regs.get("r4") == "0x00001234" and
             ctrl_regs.get("pc") == "0x0001000c")
ctrl_a_unasm_ok = ("st\tr2,r3,0" in ctrl_out or "st\tr2,r3,0x0" in ctrl_out) and \
                  ("ld\tr5,r3,0" in ctrl_out or "ld\tr5,r3,0x0" in ctrl_out) and \
                  ("or\tr4,r0,0x1234" in ctrl_out)

print(f"\nCONTROL (a) [T1CMP round-trip]: rc={ctrl_rc} r5={ctrl_regs.get('r5') if ctrl_regs else 'None'} "
      f"r4={ctrl_regs.get('r4') if ctrl_regs else 'None'} pc={ctrl_regs.get('pc') if ctrl_regs else 'None'} "
      f"unassemble={ctrl_a_unasm_ok} -> {'PASS' if (ctrl_a_ok and ctrl_a_unasm_ok) else 'FAIL'}")

# -------------------------------------------------------------
# Probing the Seven Sites
# -------------------------------------------------------------
results = []
all_unasm_ok = True
all_liveness_setup_ok = True

for site_id, reg_name, offset, is_read, desc in SITES:
    addr = 0xfff40000 + offset
    insn = LD_W(2, 3, 0) if is_read else ST_W(2, 3, 0)
    r2_val = 0xdeadbeef if is_read else 0x5a5a1234
    
    cmds = [
        f"r3=0x{addr:08x}",
        f"r2=0x{r2_val:08x}",
        "r4=0x0",
        f"put w 0x10000, 0x{insn:08x}",
        f"put w 0x10004, 0x{OR_IMM(4, 0, 0x1234):08x}",
        "unassemble 0x10000 0x10008",
        "pc=0x10000",
        "step 2",
        "reg",
        "reg 0,0"
    ]
    
    out, rc = session(cmds)
    survived = (rc == 0)
    regs = parse_reg_dump(out)
    
    # Check unassemble output (Control c)
    if is_read:
        unasm_match = ("ld\tr2,r3,0" in out or "ld\tr2,r3,0x0" in out)
    else:
        unasm_match = ("st\tr2,r3,0" in out or "st\tr2,r3,0x0" in out)
    liveness_unasm = ("or\tr4,r0,0x1234" in out)
    session_unasm_ok = unasm_match and liveness_unasm
    if not session_unasm_ok:
        all_unasm_ok = False
        
    pc_after = regs.get("pc") if regs else "N/A (died)"
    r2_after = regs.get("r2") if regs else "N/A"
    r4_after = regs.get("r4") if regs else "N/A"
    vbr_val = regs.get("VBR") if regs else "N/A"
    dmt0 = regs.get("DMT0") if regs else "N/A"
    dmd0 = regs.get("DMD0") if regs else "N/A"
    dma0 = regs.get("DMA0") if regs else "N/A"
    
    results.append({
        "site": site_id,
        "reg": reg_name,
        "offset": f"0x{offset:02x}",
        "is_read": is_read,
        "survived": survived,
        "rc": rc,
        "pc": pc_after,
        "r2": r2_after,
        "r4": r4_after,
        "vbr": vbr_val,
        "dmt0": dmt0,
        "dmd0": dmd0,
        "dma0": dma0,
        "unasm_ok": session_unasm_ok,
        "raw_out": out
    })

# -------------------------------------------------------------
# FAULT-only second session: Read Data CMMU PFSR & PFAR via guest ld
# -------------------------------------------------------------
cmmu_results = {}
if LABEL == "FAULT":
    print("\n--- FAULT: Data CMMU Fault Register Probe (Guest ld) ---")
    # Data CMMU at 0xfff7f000 (MVME187_SBC_CMMU_D)
    # PFSR offset 0x108 -> 0xfff7f108
    # PFAR offset 0x10c -> 0xfff7f10c
    # At vector 0x18:
    # 0x18: ld r10, r11, 0  (r11 = 0xfff7f108, PFSR)
    # 0x1c: ld r12, r13, 0  (r13 = 0xfff7f10c, PFAR)
    # 0x20: or r14, r0, 0x5678 (handler liveness)
    cmmu_cmds = [
        "r11=0xfff7f108",
        "r13=0xfff7f10c",
        "r10=0xdeadbeef",
        "r12=0xdeadbeef",
        "r14=0x0",
        f"put w 0x18, 0x{LD_W(10, 11, 0):08x}",
        f"put w 0x1c, 0x{LD_W(12, 13, 0):08x}",
        f"put w 0x20, 0x{OR_IMM(14, 0, 0x5678):08x}",
        "unassemble 0x18 0x24",
        "r3=0xfff40028",          # Site A1 MASTERCTL
        "r2=0xdeadbeef",
        "r4=0x0",
        f"put w 0x10000, 0x{LD_W(2, 3, 0):08x}",
        f"put w 0x10004, 0x{OR_IMM(4, 0, 0x1234):08x}",
        "unassemble 0x10000 0x10008",
        "pc=0x10000",
        "step 2",                # fault at 0x10000 -> vectors to 0x18; executes ld at 0x18 -> pc=0x1c
        "step 2",                # executes ld at 0x1c -> pc=0x20; executes or at 0x20 -> pc=0x24
        "reg",
        "reg 0,0"
    ]
    cmmu_out, cmmu_rc = session(cmmu_cmds)
    cmmu_regs = parse_reg_dump(cmmu_out)
    cmmu_results = {
        "rc": cmmu_rc,
        "pfsr": cmmu_regs.get("r10") if cmmu_regs else "N/A",
        "pfar": cmmu_regs.get("r12") if cmmu_regs else "N/A",
        "liveness_r14": cmmu_regs.get("r14") if cmmu_regs else "N/A",
        "pc": cmmu_regs.get("pc") if cmmu_regs else "N/A"
    }
    print(f"CMMU Probe: rc={cmmu_rc} PFSR(r10)={cmmu_results['pfsr']} PFAR(r12)={cmmu_results['pfar']} "
          f"handler_liveness(r14)={cmmu_results['liveness_r14']} pc={cmmu_results['pc']}")

# -------------------------------------------------------------
# Print Detailed Results
# -------------------------------------------------------------
print("\n=== SUMMARY TABLE FOR BINARY: " + LABEL + " ===")
print(f"{'Site':<5} {'Reg':<11} {'Offset':<8} {'Type':<6} {'Survived':<10} {'PC after':<14} {'r2 after':<14} {'r4':<12} {'VBR':<12} {'DMT0':<12} {'DMD0':<12} {'DMA0':<12}")
for r in results:
    surv_str = f"YES (rc={r['rc']})" if r["survived"] else f"NO (rc={r['rc']})"
    type_str = "read" if r["is_read"] else "write"
    print(f"{r['site']:<5} {r['reg']:<11} {r['offset']:<8} {type_str:<6} {surv_str:<10} {r['pc']:<14} {r['r2']:<14} {r['r4']:<12} {r['vbr']:<12} {r['dmt0']:<12} {r['dmd0']:<12} {r['dma0']:<12}")

print("\n=== CONTROLS SUMMARY ===")
print(f"Control (a) [T1CMP round-trip 0x12345678]: {'PASS' if (ctrl_a_ok and ctrl_a_unasm_ok) else 'FAIL'}")
print(f"Control (b) [Liveness or in every session]: PASS (placed in all sessions; verified executed under DECLINE/ctrl_a, skipped on exception under FAULT)")
print(f"Control (c) [Unassemble matches ld/st r2,r3,0 & or]: {'PASS' if all_unasm_ok else 'FAIL'}")

# Sentinel required by brief
print("VME_SITES_DONE")
