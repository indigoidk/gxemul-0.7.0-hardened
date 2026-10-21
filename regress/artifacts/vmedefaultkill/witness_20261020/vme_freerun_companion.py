#!/usr/bin/env python3
"""vme_freerun_companion.py -- companion to the UNMODIFIED vme_sites_probe.py (2026-10-09).

It does NOT replace the probe and does not change its result.  It adds what the probe
cannot show:

  PART 1 (attribution, "did it die for the reason under test?"):  re-runs the probe's
         seven SINGLE-STEPPED site sessions with byte-identical argv and commands, and
         keeps each raw transcript, so the default arm's own debug() text can be seen
         beside rc=1.  The probe itself scores a site "died" on rc != 0 alone.
  PART 2 (the brief's free-running session):  MASTERCTL read (0xfff40028) and the T1CMP
         control (0xfff40050), free-running via `continue` to a breakpoint, default
         verbosity, same argv as the probe.  Each run twice (determinism).
  PART 3 (extra controls, beyond the brief, clearly labelled):
         FR_KILL_V  -- the PART-2 kill session with -v added: free-running debug() then
                       has v = 1 - 1 = 0, so the default arm's text should appear.  This is
                       the attribution control for the FREE-RUNNING death.
         FR_TCR     -- free-running read of TCR (0xfff4004c), a CASED arm that calls debug()
                       and does NOT exit: does debug() text show free-running at default
                       verbosity when no kill is involved?
         STEP_TCR   -- the same TCR read single-stepped (the probe's shape): the contrast.

usage: vme_freerun_companion.py <gxemul_binary> <label>
"""

import hashlib
import os
import re
import subprocess
import sys

if len(sys.argv) < 3:
    sys.stderr.write("usage: vme_freerun_companion.py <gxemul_binary> <label>\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2]
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
TDIR = os.path.join(WORK_DIR, "transcripts_" + LABEL)
os.makedirs(TDIR, exist_ok=True)
OUT_FILE = os.path.join(WORK_DIR, "run_FREERUN_" + LABEL + ".out")
_log = open(OUT_FILE, "w", encoding="latin-1")


def say(s=""):
    print(s)
    _log.write(s + "\n")
    _log.flush()


# Same dummy as the probe: 64 zero bytes (the probe rewrites it identically).
DUMMY = "/tmp/vme_probe_dummy.bin"
with open(DUMMY, "wb") as f:
    f.write(b"\x00" * 64)


def enc(op26, rd, rs1, imm):
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def LD_W(rd, rs1, imm=0):
    return enc(0x05, rd, rs1, imm)


def ST_W(rd, rs1, imm=0):
    return enc(0x09, rd, rs1, imm)


def OR_IMM(rd, rs1, imm):
    return enc(0x16, rd, rs1, imm)


# m88k `br` (no delay slot) is op26 0x30 with a 26-bit signed WORD displacement
# (cpu_m88k.c: d26 = ((int32_t)((iw & 0x03ffffff) << 6)) >> 4).  d26 = 0 -> self.
BR_SELF = 0x30 << 26   # 0xc0000000


def session(cmds, extra_opts=(), timeout=30, subtype="mvme187"):
    # Identical to the probe's session() except that extra_opts (e.g. "-v") may be
    # inserted among the options.  extra_opts is EMPTY for every brief-specified session.
    argv = [BIN, "-V", "-x"] + list(extra_opts) + ["-E", "mvme88k", "-e", subtype,
                                                   "-M", "64", "0x10000:" + DUMMY]
    inp = ("\n".join(cmds + ["quit"]) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
        rc = p.returncode
        out = p.stdout.decode("latin-1", "replace").replace("\r", "")
    except subprocess.TimeoutExpired as e:
        out = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        rc = -999
    return out, rc, argv


def parse_reg(transcript):
    parts = transcript.split("GXemul> reg\n")
    if len(parts) < 2:
        return None
    dump = parts[1]
    res = {}
    m = re.search(r"cpu\d+:\s+pc\s+=\s+(0x[0-9a-fA-F]+)", dump)
    res["pc"] = m.group(1).lower() if m else None
    for r in ["r2", "r3", "r4", "r5"]:
        m = re.search(r"\b" + r + r"\s+=\s+(0x[0-9a-fA-F]+)", dump)
        res[r] = m.group(1).lower() if m else None
    return res


def save(name, argv, cmds, out, rc):
    path = os.path.join(TDIR, name + ".txt")
    with open(path, "w", encoding="latin-1") as f:
        f.write("# argv: " + " ".join(argv) + "\n")
        f.write("# stdin: " + " | ".join(cmds + ["quit"]) + "\n")
        f.write("# rc: %d\n" % rc)
        f.write("# ---- combined stdout+stderr follows ----\n")
        f.write(out)
    return path


def tail(out, n=4):
    lines = [l for l in out.split("\n") if l.strip() != ""]
    return lines[-n:]


md5 = hashlib.md5(open(BIN, "rb").read()).hexdigest()
say("=== VME FREE-RUNNING COMPANION: BINARY=%s md5=%s LABEL=%s ===" % (BIN, md5, LABEL))
say("BR_SELF encoding = 0x%08x" % BR_SELF)

# ---------------------------------------------------------------------------
# PART 1: the probe's seven single-stepped sessions, transcripts kept.
# ---------------------------------------------------------------------------
SITES = [
    ("A1", "MASTERCTL", 0x28, True),
    ("A2", "MASTER3", 0x1c, False),
    ("A3", "MASTER4", 0x20, False),
    ("A4", "MASTER4MOD", 0x24, False),
    ("A5", "MASTERCTL", 0x28, False),
    ("H1", "IRQSTAT", 0x68, True),
    ("H2", "IRQCLR", 0x74, False),
]

say("")
say("--- PART 1: single-stepped site sessions (probe-identical argv + stdin) ---")
p1_ok = True
for site_id, reg_name, offset, is_read in SITES:
    addr = 0xfff40000 + offset
    insn = LD_W(2, 3, 0) if is_read else ST_W(2, 3, 0)
    r2_val = 0xdeadbeef if is_read else 0x5a5a1234
    cmds = [
        "r3=0x%08x" % addr,
        "r2=0x%08x" % r2_val,
        "r4=0x0",
        "put w 0x10000, 0x%08x" % insn,
        "put w 0x10004, 0x%08x" % OR_IMM(4, 0, 0x1234),
        "unassemble 0x10000 0x10008",
        "pc=0x10000",
        "step 2",
        "reg",
        "reg 0,0",
    ]
    out, rc, argv = session(cmds)
    path = save("step_%s_%s" % (site_id, reg_name), argv, cmds, out, rc)
    if is_read:
        want = "[ vme: unimplemented READ from offset 0x%x ]" % offset
    else:
        want = "[ vme: unimplemented WRITE to offset 0x%x: 0x%x ]" % (offset, r2_val)
    has_msg = want in out
    reached_reg = "GXemul> reg" in out
    attributed = (rc == 1 and has_msg and not reached_reg)
    if not attributed:
        p1_ok = False
    say("%s %-10s +0x%02x %-5s rc=%-4d default-arm text present=%-5s reached 'reg'=%-5s -> %s"
        % (site_id, reg_name, offset, "read" if is_read else "write", rc, has_msg,
           reached_reg, "DIED IN DEFAULT ARM" if attributed else "NOT ATTRIBUTED"))
    say("     wanted text: %s" % want)
    say("     last lines : %s" % " || ".join(tail(out, 3)))
    say("     transcript : %s" % os.path.basename(path))

# ---------------------------------------------------------------------------
# PART 2 + 3: free-running sessions.
# ---------------------------------------------------------------------------
def freerun_cmds(addr):
    return [
        "r3=0x%08x" % addr,
        "r2=0xdeadbeef",
        "r4=0x0",
        "put w 0x10000, 0x%08x" % LD_W(2, 3, 0),
        "put w 0x10004, 0x%08x" % OR_IMM(4, 0, 0x1234),
        "put w 0x10008, 0x%08x" % BR_SELF,
        "unassemble 0x10000 0x1000c",
        "breakpoint add 0x10008",
        "pc=0x10000",
        "continue",
        "reg",
    ]


def unasm_ok(out):
    ld = bool(re.search(r"ld\s+r2,r3,(0x)?0\b", out))
    orr = bool(re.search(r"or\s+r4,r0,0x1234", out))
    br = bool(re.search(r"00010008:\s*c0000000\b[^\n]*\bbr\s+0x0*10008\b", out))
    return ld, orr, br


def run_freerun(name, addr, extra_opts=()):
    cmds = freerun_cmds(addr)
    out, rc, argv = session(cmds, extra_opts=extra_opts)
    path = save(name, argv, cmds, out, rc)
    regs = parse_reg(out)
    ld, orr, br = unasm_ok(out)
    res = {
        "name": name,
        "rc": rc,
        "vme_text": "[ vme: unimplemented" in out,
        "vme_lines": [l.strip() for l in out.split("\n") if "[ vme:" in l],
        "breakpoint_hit": "BREAKPOINT: pc = 0x10008" in out,
        "reached_reg": regs is not None,
        "pc": regs.get("pc") if regs else None,
        "r2": regs.get("r2") if regs else None,
        "r4": regs.get("r4") if regs else None,
        "unasm": (ld, orr, br),
        "argv": " ".join(argv),
        "path": os.path.basename(path),
        "tail": tail(out, 3),
    }
    say("%s: rc=%d  '[ vme: unimplemented' anywhere=%s  BREAKPOINT@0x10008=%s  reached reg=%s"
        % (name, rc, res["vme_text"], res["breakpoint_hit"], res["reached_reg"]))
    say("     pc=%s r2=%s r4=%s   unassemble ld/or/br-self = %s/%s/%s"
        % (res["pc"], res["r2"], res["r4"], ld, orr, br))
    if res["vme_lines"]:
        say("     [ vme: ] lines: %s" % " || ".join(res["vme_lines"]))
    say("     argv: %s" % res["argv"])
    say("     last lines: %s" % " || ".join(res["tail"]))
    say("     transcript: %s" % res["path"])
    return res


say("")
say("--- PART 2: free-running sessions (brief-specified; default verbosity; probe argv) ---")
fr = {}
for rep in (1, 2):
    fr["kill%d" % rep] = run_freerun("freerun_KILL_MASTERCTL_rep%d" % rep, 0xfff40028)
    fr["ctrl%d" % rep] = run_freerun("freerun_CTRL_T1CMP_rep%d" % rep, 0xfff40050)

say("")
say("--- PART 3: extra controls (beyond the brief) ---")
fr["kill_v"] = run_freerun("freerun_KILL_MASTERCTL_with_-v", 0xfff40028, extra_opts=("-v",))
fr["tcr"] = run_freerun("freerun_TCR_cased_debug_arm", 0xfff4004c)

# STEP_TCR: TCR read in the probe's single-stepped shape.
cmds = [
    "r3=0xfff4004c",
    "r2=0xdeadbeef",
    "r4=0x0",
    "put w 0x10000, 0x%08x" % LD_W(2, 3, 0),
    "put w 0x10004, 0x%08x" % OR_IMM(4, 0, 0x1234),
    "unassemble 0x10000 0x10008",
    "pc=0x10000",
    "step 2",
    "reg",
    "reg 0,0",
]
out, rc, argv = session(cmds)
path = save("step_TCR_cased_debug_arm", argv, cmds, out, rc)
regs = parse_reg(out)
st_tcr = {
    "rc": rc,
    "msg": "[ vme: unimplemented READ from TCR ]" in out,
    "r4": regs.get("r4") if regs else None,
    "r2": regs.get("r2") if regs else None,
    "pc": regs.get("pc") if regs else None,
}
say("step_TCR: rc=%d  '[ vme: unimplemented READ from TCR ]' present=%s  pc=%s r2=%s r4=%s  transcript: %s"
    % (rc, st_tcr["msg"], st_tcr["pc"], st_tcr["r2"], st_tcr["r4"], os.path.basename(path)))

# ---------------------------------------------------------------------------
# Verdict rows (each row states its own expectation; nothing is a constant).
# ---------------------------------------------------------------------------
say("")
say("=== ROWS ===")
rows = []


def row(name, got, want):
    ok = (got == want)
    rows.append(ok)
    say("%-58s got=%-14s want=%-14s %s" % (name, got, want, "ok" if ok else "FAIL"))


row("P1 all seven stepped sites died in the default arm", p1_ok, True)
for rep in (1, 2):
    k = fr["kill%d" % rep]
    c = fr["ctrl%d" % rep]
    row("FR kill rep%d: exit code" % rep, k["rc"], 1)
    row("FR kill rep%d: '[ vme: unimplemented' anywhere" % rep, k["vme_text"], False)
    row("FR kill rep%d: breakpoint never reached" % rep, k["breakpoint_hit"], False)
    row("FR kill rep%d: unassemble ld/or/br-self all correct" % rep, all(k["unasm"]), True)
    row("FR ctrl rep%d: exit code" % rep, c["rc"], 0)
    row("FR ctrl rep%d: breakpoint at 0x10008 hit" % rep, c["breakpoint_hit"], True)
    row("FR ctrl rep%d: pc" % rep, c["pc"], "0x00010008")
    row("FR ctrl rep%d: r4 (liveness or)" % rep, c["r4"], "0x00001234")
    row("FR ctrl rep%d: r2 (T1CMP reset value, not sentinel)" % rep, c["r2"], "0x00000000")
    row("FR ctrl rep%d: unassemble ld/or/br-self all correct" % rep, all(c["unasm"]), True)
kv = fr["kill_v"]
row("EXTRA FR kill with -v: exit code", kv["rc"], 1)
row("EXTRA FR kill with -v: default-arm READ 0x28 text present",
    "[ vme: unimplemented READ from offset 0x28 ]" in " ".join(kv["vme_lines"]), True)
t = fr["tcr"]
row("EXTRA FR TCR (cased debug arm): exit code", t["rc"], 0)
row("EXTRA FR TCR: breakpoint hit", t["breakpoint_hit"], True)
row("EXTRA FR TCR: r4", t["r4"], "0x00001234")
row("EXTRA FR TCR: '[ vme: unimplemented' anywhere", t["vme_text"], False)
row("EXTRA STEP TCR: exit code", st_tcr["rc"], 0)
row("EXTRA STEP TCR: TCR debug text present when stepping", st_tcr["msg"], True)
row("EXTRA STEP TCR: r4", st_tcr["r4"], "0x00001234")

say("")
say("ROWS: %d/%d as expected" % (sum(rows), len(rows)))
say("VME_FREERUN_DONE")
_log.close()
