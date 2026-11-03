#!/usr/bin/env python3
"""shblreset -- RUNG-3 WITNESS: which EXPEVT code does a general exception taken with SR.BL set leave behind?

Manual (sh7750_hardware.txt): 5.5.3 (:12302-12304) "When the BL bit in SR is 1 and a general exception other than a user break is
generated, the CPU's internal registers and the registers of the other modules are set to their states following a MANUAL reset,
and the CPU branches to the same address as in a reset (H'A000 0000)"; the revision note (:678-681) "The value in EXPEVT at this
time is H'0000 0020".  Table 5.2 (:12006, :12010) lists the two TLB multiple-hit exceptions as reset-category in their own right,
code H'140 (:12461).  HEAD's sh_exception() (src/cpus/cpu_sh.c:910-918) rewrites EVERY expevt to EXPEVT_RESET_POWER (H'000) when
BL is set -- the wrong reset code for a general exception, and a clobber of the multiple-hit code.

Shape: the cold debugger pre-sets SR, places one real guest instruction (or the committed multiple-hit program) at CODE, steps,
and reads EXPEVT / PC back with `print <name>` (CPU_SETTINGS_ADD_REGISTER32; the dump does not show them), anchored to the
command echo.  Machine: UNMODIFIED in-tree `-E landisk' with the rig kernel loaded for construction only -- the shape of
regress/sh_tlbmulti_probe.py, whose session() this file copies.

Rows:
  bl trapa expevt   sr = MD|BL, TRAPA #1 -> EXPEVT     want 0x00000020 (manual reset)   HEAD predicted 0x00000000   DEFECT
  bl trapa pc       same session -> PC                 want 0xa0000000                                                LIVENESS (the reset path ran)
  nobl trapa expevt sr = MD, TRAPA #1 -> EXPEVT        want 0x00000160 (TRAPA)                                        CONTROL (BL clear: the general vector, EXPEVT readable)
  bl multihit       sr = MD|BL, the two-entry UTLB associative write -> EXPEVT   want 0x00000140                      CONTROL (the exemption: BL must not clobber H'140)
                                                                                 HEAD predicted 0x00000000
A row whose got equals the HEAD-predicted value prints FAILED-FOR-THE-REASON-UNDER-TEST; a dead session or an absent readback prints
FAILED-FOR-SOME-OTHER-REASON and must not be claimed as the defect.

usage: sh_blreset_witness.py <gxemul> <landisk kernel>
Sentinel: SH_BLRESET_WITNESS_DONE
"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
KERNEL = sys.argv[2]
CODE = 0x8c010000
UTLB_AA = 0xf6000000
ENTRY0 = UTLB_AA + 0x000
ENTRY1 = UTLB_AA + 0x100
ASSOC = UTLB_AA + 0x080
VPN_A = 0x12345100
SR_MD = 0x400000f0            # privileged, BL clear, IMASK 0xf
SR_MD_BL = 0x500000f0         # privileged, BL set,   IMASK 0xf
TRAPA_1 = 0xc301              # trapa #1 : 1100 0011 0000 0001
MOV_L_R0_AT_R1, MOV_L_R4_AT_R5, MOV_L_R6_AT_R7 = 0x2102, 0x2542, 0x2762


def session(pre, program, steps, reads=("expevt", "pc", "sr")):
    """pre: debugger assignments; program: list of 16-bit words at CODE; returns (transcript, died)"""
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-E", "landisk", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        got_any = False
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.2)
            if fd in r:
                try:
                    d = os.read(fd, 65536)
                except OSError:
                    return False
                if not d:
                    return False
                buf += d.decode("latin-1", "replace"); got_any = True
                if buf.rstrip().endswith("GXemul>"):
                    return True
        return got_any or True

    alive = rd(8.0)
    cmds = list(pre) + ["put h 0x%x, 0x%04x" % (CODE + 2 * i, w) for i, w in enumerate(program)] + \
           ["pc=0x%x" % CODE, "step %d" % steps] + ["print %s" % r for r in reads]
    for c in cmds:
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(1.5):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); time.sleep(0.2); os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    return buf, not alive


def reg(t, name):
    m = re.search(r"print\s+%s\s*\r?\n\s*0x([0-9a-f]+)" % re.escape(name), t)
    return ("0x%08x" % int(m.group(1), 16)) if m else "absent"


MULTIHIT = (["r0=0x%08x" % VPN_A, "r1=0x%x" % ENTRY0, "r4=0x%08x" % VPN_A, "r5=0x%x" % ENTRY1,
             "r6=0x%08x" % VPN_A, "r7=0x%x" % ASSOC], [MOV_L_R0_AT_R1, MOV_L_R4_AT_R5, MOV_L_R6_AT_R7], 3)

print("shblreset RUNG-3 WITNESS -- binary=%s" % BIN)
print("machine: -E landisk -M 64 (UNMODIFIED in-tree), kernel loaded for construction only")
print("%-18s %-10s %-10s %-9s %s" % ("row", "got", "want", "role", "verdict"))
ok = 0
results = []
t1, d1 = session(["sr=0x%08x" % SR_MD_BL], [TRAPA_1], 1)
results.append(("bl trapa expevt", "died" if d1 else reg(t1, "expevt"), "0x00000020", "0x00000000", "DEFECT"))
results.append(("bl trapa pc", "died" if d1 else reg(t1, "pc"), "0xa0000000", None, "LIVENESS"))
t2, d2 = session(["sr=0x%08x" % SR_MD], [TRAPA_1], 1)
results.append(("nobl trapa expevt", "died" if d2 else reg(t2, "expevt"), "0x00000160", None, "CONTROL"))
pre, prog, steps = MULTIHIT
t3, d3 = session(["sr=0x%08x" % SR_MD_BL] + pre, prog, steps)
results.append(("bl multihit", "died" if d3 else reg(t3, "expevt"), "0x00000140", "0x00000000", "CONTROL"))
for name, got, want, headpred, role in results:
    if got == want:
        ok += 1; v = "ok"
    elif got in ("died", "absent"):
        v = "FAILED-FOR-SOME-OTHER-REASON (%s)" % got
    elif headpred is not None and got == headpred:
        v = "FAILED-FOR-THE-REASON-UNDER-TEST (EXPEVT rewritten to the power-on code)"
    else:
        v = "FAILED-FOR-SOME-OTHER-REASON (unexpected value)"
    print("%-18s %-10s %-10s %-9s %s" % (name, got, want, role, v))
print("RESULT=%d/%d" % (ok, len(results)))
print("SH_BLRESET_WITNESS_DONE")
