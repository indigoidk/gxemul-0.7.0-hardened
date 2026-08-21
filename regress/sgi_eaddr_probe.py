#!/usr/bin/env python3
"""#446 DETECTOR: the ethernet-address string handed to arcbios_init() is the correctly
formatted form of the MAC bytes handed alongside it -- read AT THE CALL SITE, from the
running emulator.

*** THIS FILE WAS A SOURCE-TEXT DETECTOR AND IT WAS VACUOUS.  THE REPLACEMENT IS HERE
BECAUSE OF WHAT A MEASURING SEAT DID TO THE FIRST VERSION, NOT BECAUSE OF A REVIEW
OPINION. ***

The first version matched six regexes over machine_sgi.c: that the malloc existed, that an
`snprintf(eaddr_string,` existed, that the subtype switch existed, that the snprintf's byte
offset fell between the other two, that a six-field "%02x:..." literal appeared in that
span, and that six `macaddr[N]` references appeared in it.  A pass-2 panel built SIXTEEN
mutants against it and SIXTEEN SCORED 7/7, among them:

  * `0*ETHERNET_STRING_MAXLEN` as the size argument -- TWO CHARACTERS, compiles with ZERO
    warnings, and `snprintf` with size 0 writes NOTHING, not even the NUL.  Measured under
    ASan: the heap-buffer-overflow returns on ip12/ip28/ip30/ip35, exactly as before the
    fix, while the gate row printed green.
  * size `1` (writes only the NUL -> EMPTY MAC, ASan silent) and `sizeof(eaddr_string)`
    (= 8 on this host -> the truncated "08:20:3").
  * `#if 0`, `/* */`, `if (0)`, `if (subtype == 32)`, a second malloc, an arm re-pointing
    the pointer, and `#define snprintf(b,l,...) ((void)(b))`.

*** AND THE REDUCTIO THAT SETTLES IT: A 217-BYTE FILE CONTAINING NOTHING BUT A C COMMENT
SCORED 7/7. ***  No function, no MACHINE_SETUP, nothing that could ever be compiled into
the emulator.  That is not a weak detector, it is a VACUOUS one under this project's own
taxonomy, and no additional regex repairs it -- the failure is the medium, not the rows.

The old file's stated purpose made the gap sharper still.  Its docstring claimed to be "the
LENGTH/FORMAT oracle" that sees what ASan cannot.  *** IT NEVER EXAMINED THE LENGTH
ARGUMENT. ***  The size-1 mutant is precisely the `eaddr_string[0] = '\\0'` hole it named as
its reason for existing, spelled with an snprintf, and it passed.

WHAT THIS VERSION DOES INSTEAD.  It breaks on arcbios_init() in a real run of a real
subtype and reads the two arguments the fix is about:

    void arcbios_init(struct machine *machine, int is64bit, uint64_t sgi_ram_offset,
                      const char *primary_ether_addr, uint8_t *primary_ether_macaddr)

and requires the STRING to be the six-octet formatting of the BYTES.  That is a provenance
check, not a shape check: RAM garbage, an empty string, a truncated string and a
right-shaped-but-wrong-octet string all fail it, and none of them can be produced by
editing a comment.  Every mutant listed above dies here.

RUNG.  Machine CONSTRUCTION (rung 2), which is the ceiling for this defect and not a
shortfall: no guest instruction executes, the input is a dummy ELF that fails to load, and
the overflow happens while the machine is being built.  The macppc heap OOB (#23) is the
precedent.  A rung-3 probe is unnecessary here, not missing.

CLASS: DETECTOR (green once the defect is gone), so it must be run by a gate.

HOW THE ARGUMENTS ARE READ, and its one real portability limit.  build/gxemul carries an
ELF symtab but NO DWARF, so `primary_ether_addr` cannot be named.  They are read from the
SysV AMD64 argument registers -- arg4 = RCX, arg5 = R8 -- and breaking without DWARF lands
at the raw function entry, before any prologue moves them, which is exactly when they are
still live.  *** THIS TIES THE FILE TO x86-64 SysV. ***  Stated rather than hidden; on
another ABI it must be re-derived, and the liveness row below is what would catch it -- a
wrong register yields an unreadable pointer or a mismatch, never a silent pass.  (This is
the hand-assembled-encoding trap in another costume: a wrong field usually reads as zero,
and a row that accepts zero accepts the mistake.  V6 and V7 exist so nothing here does.)

usage:  python3 regress/sgi_eaddr_probe.py [--binary PATH]
"""

import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))

#  Subtypes that REACH the hand-off.  Measured, not assumed: of the ten advertised
#  subtypes these five return 1 and the other five return 134 (SIGABRT).
REACHING = ["ip12", "ip28", "ip30", "ip32", "ip35"]

#  The negative control, and the two are chosen for DIFFERENT MECHANISMS rather than for
#  coverage: ip19 has a literal abort() in its own arm, while ip27 has none and dies inside
#  its own device_add() at interrupt_handler_lookup() <- devinit_z8530(), on its `irq=0`.
#  A control using two of the same kind would not show that the probe distinguishes
#  "did not reach" from "reached and was fine".
ABORTERS = ["ip19", "ip27"]

#  The IDENTITY constant.  A probe copied into a tree where it no longer runs all of its
#  rows must not report green over a shorter file.
EXPECT_ROWS = 10

_rows = []


def row(name, ok, got, want):
    _rows.append((name, bool(ok)))
    print("  [%s] %-58s got=%s want=%s" % ("ok" if ok else "FAIL", name, got, want))


PRINTF = (
    'printf "EADDR=[%s] MAC=%02x:%02x:%02x:%02x:%02x:%02x\\n", (char *)$rcx, '
    '*(unsigned char *)($r8+0), *(unsigned char *)($r8+1), *(unsigned char *)($r8+2), '
    '*(unsigned char *)($r8+3), *(unsigned char *)($r8+4), *(unsigned char *)($r8+5)'
)


def peek(binary, subtype, timeout=60):
    """Return (reached, eaddr, mac) for one subtype. eaddr/mac are None if not reached."""
    cmd = ["gdb", "-batch", "-nx",
           "-ex", "set confirm off",
           "-ex", "break arcbios_init",
           "-ex", "run",
           "-ex", PRINTF,
           "--args", binary, "-E", "sgi", "-e", subtype, "/dev/null"]
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return (None, None, None)
    out = p.stdout.decode("utf-8", "replace")
    reached = "Breakpoint 1, " in out
    m = re.search(r"^EADDR=\[([^\]]*)\] MAC=([0-9a-f:]+)\s*$", out, re.M)
    if not m:
        return (reached, None, None)
    return (reached, m.group(1), m.group(2))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary", default=os.path.join(PROJ, "build", "gxemul"))
    a = ap.parse_args(argv)

    #  An absent tool or binary is an OPERATIONAL FAILURE, never a pass.  A detector that
    #  reports green because it could not run is the failure mode this harness names most
    #  often, so it is refused explicitly here rather than left to a missing row.
    if not os.path.isfile(a.binary):
        print("  OPERATIONAL FAILURE: no emulator binary at %s" % a.binary)
        print("SGI_EADDR_RESULT=0/%d" % EXPECT_ROWS)
        print("SGI_EADDR_FAIL")
        return 1
    try:
        subprocess.run(["gdb", "--version"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=30)
    except Exception:
        print("  OPERATIONAL FAILURE: gdb is not available; this detector needs it")
        print("SGI_EADDR_RESULT=0/%d" % EXPECT_ROWS)
        print("SGI_EADDR_FAIL")
        return 1

    seen = {}
    for st in REACHING:
        seen[st] = peek(a.binary, st)

    #  ---- V1..V5: THE PROPERTY.  The string IS the formatting of the bytes. -----------
    for st in REACHING:
        reached, eaddr, mac = seen[st]
        ok = bool(reached) and eaddr is not None and mac is not None and eaddr == mac
        row("V%d %s: the eaddr string equals its own MAC bytes"
            % (REACHING.index(st) + 1, st),
            ok, "eaddr=%r mac=%r" % (eaddr, mac), "equal, and both read")

    #  ---- V6: LIVENESS.  A known value returned through the real path. ---------------
    #  Without this a wrong register, a renamed function or a build that never reaches
    #  construction would make V1-V5 fail for a reason that has nothing to do with the
    #  defect -- and the run would look like a detection.
    live = sum(1 for st in REACHING if seen[st][0])
    row("V6 LIVENESS the breakpoint was reached on every subtype",
        live == len(REACHING), live, len(REACHING))

    #  ---- V7: LENGTH, named separately because it is the class the old file MISSED. --
    #  size 0 -> unwritten garbage; size 1 -> ""; sizeof(ptr) -> "08:20:3".  All three
    #  scored 7/7 against the source-text version.  Seventeen is the only right answer.
    lens = {st: (len(seen[st][1]) if seen[st][1] is not None else -1) for st in REACHING}
    row("V7 every eaddr string is exactly 17 characters",
        all(v == 17 for v in lens.values()), lens, "all 17")

    #  ---- V8: NEGATIVE CONTROL.  The aborters must NOT reach the hand-off. -----------
    #  If one did, this file's five-subtype scope would be wrong and V1-V5 would be
    #  measuring an incomplete set while reporting green over it.
    reached_abort = []
    for st in ABORTERS:
        r_, _e, _m = peek(a.binary, st)
        if r_:
            reached_abort.append(st)
    row("V8 NEG-CTRL the aborting subtypes do not reach arcbios_init",
        not reached_abort, reached_abort or "none reached", "none reached")

    #  ---- V9: FAILABILITY.  Prove the comparison is live. ----------------------------
    #  V1-V5 are equality tests, and an equality test that is never exercised against an
    #  unequal pair is indistinguishable from `assert True`.  Compare the same real string
    #  against a deliberately corrupted form of its own MAC and require INEQUALITY.
    probe_str = seen[REACHING[0]][1]
    probe_mac = seen[REACHING[0]][2]
    if probe_str is None or probe_mac is None:
        row("V9 FAILABILITY the comparison can report unequal", False,
            "no value read -- cannot exercise", "an unequal pair is rejected")
    else:
        bad = probe_mac[:-1] + ("0" if probe_mac[-1] != "0" else "1")
        row("V9 FAILABILITY the comparison can report unequal",
            probe_str != bad, "%r vs corrupted %r" % (probe_str, bad),
            "an unequal pair is rejected")

    #  ---- IDENTITY -------------------------------------------------------------------
    row("V0 IDENTITY row count -- guards against a stale copy",
        len(_rows) + 1 == EXPECT_ROWS, len(_rows) + 1, EXPECT_ROWS)

    bad_n = sum(1 for _, ok in _rows if not ok)
    print()
    print("SGI_EADDR_RESULT=%d/%d" % (len(_rows) - bad_n, len(_rows)))
    print("SGI_EADDR_PASS" if bad_n == 0 else "SGI_EADDR_FAIL")
    return 1 if bad_n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
