#!/usr/bin/env python3
"""#446 DETECTOR: the SGI ethernet-address buffer is filled where it is ALLOCATED,
not only in the one subtype arm that happened to write it.

THE DEFECT.  `machine_setup_sgi()` malloc'ed ETHERNET_STRING_MAXLEN bytes and left
them UNINITIALISED.  Exactly one subtype arm (ip32) ever wrote to the buffer, yet
`arcbios_init()` was handed it UNCONDITIONALLY, where `set_env()` -> `strdup()`
scans for a NUL that is not there.  MEASURED under ASan: a 41-byte READ past a
40-byte allocation on ip12, ip28, ip30 and ip35, with NO terminator anywhere in
the region.

*** WHERE THE DEFECT IS NOT.  ***  ASan names `arcbios.c` in the report, and the
first filing followed it there.  `set_env()` is CORRECT CODE: its append branch
grows both arrays before writing to either, and its `envstrings` is malloc+memset
at the call site.  It cannot detect a missing terminator from the inside, so
"harden the callee instead" is not a trade-off here -- it is an impossibility.
The owner is the caller.

WHY THIS FILE IS A SOURCE-TEXT DETECTOR, and what owns the other half.

The behavioural oracle for a heap overflow is ASan, and gate 9
(`gate_asan_sweep.sh`) already sweeps every machine/subtype under an instrumented
build and greps for `AddressSanitizer` -- so a REGRESSION of the overflow itself
is gate 9's job, and it will catch it there.  Two reasons that is not sufficient
on its own, and both are recorded rather than assumed:

  1. *** AN ASan-ONLY ORACLE CANNOT SEE THE MOST LIKELY BAD FIX. ***  Writing
     `eaddr_string[0] = '\\0';` silences ASan COMPLETELY -- the read stops at
     byte 0 and no overflow occurs -- while handing the guest an EMPTY MAC
     address.  A pass-1 seat named that hole before this file existed.  Only a
     LENGTH/FORMAT oracle sees it, and this file is that oracle.
  2. Gate 9's instrumented binaries were 23 days stale when this defect was
     found, so its green meant "the July binary is clean" -- a true statement
     about the wrong artefact.  Tracked as `asanstale`.

WHAT THIS FILE DOES NOT CLAIM.  Nothing about the bytes the GUEST sees.  The
string is copied into guest RAM by `add_environment_string()` and exposed through
`GetEnvironmentVariable`, but reading it back needs a rung-3 cold-debugger probe
on a machine that gets that far, and gxemul exits on a dummy ELF before any
prompt.  There is no SGI rig in this tree.  That is READ, not measured, and this
file asserts none of it.

FIVE OTHER SUBTYPES WERE MASKING THIS.  ip19/20/22/24/27 abort() before the
handing-off line, so they never reached the overflow.  *** THE COUPLING RUNS ONE
WAY: fixing those aborts first would have grown the overflow from four subtypes
to nine. ***  Recorded on `ctorabortclass`.

usage:  python3 regress/sgi_eaddr_probe.py [--source PATH]
"""

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC_SRC = os.path.join(os.path.dirname(HERE), "src", "machines", "machine_sgi.c")

#  The IDENTITY constant.  A probe copied into a tree where it no longer runs all
#  of its rows must not report green over a shorter file.
EXPECT_ROWS = 7

_rows = []


def row(name, ok, got, want):
    _rows.append((name, bool(ok)))
    print("  [%s] %-56s got=%s want=%s" % ("ok" if ok else "FAIL", name, got, want))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=SEC_SRC)
    a = ap.parse_args(argv)

    if not os.path.exists(a.source):
        print("  OPERATIONAL FAILURE: no such source %s" % a.source)
        print("SGI_EADDR_RESULT=0/%d" % EXPECT_ROWS)
        print("SGI_EADDR_FAIL")
        return 1

    src = open(a.source, encoding="utf-8", errors="replace").read()

    #  ---- the allocation and the fill, and their ORDER -----------------------
    m_alloc = re.search(r"eaddr_string\s*=\s*\(char\s*\*\)\s*malloc\s*\(", src)
    row("E1 the buffer is still allocated where this file expects",
        bool(m_alloc), bool(m_alloc), True)

    fills = [m.start() for m in
             re.finditer(r"snprintf\s*\(\s*eaddr_string\s*,", src)]
    row("E2 at least one snprintf targets the buffer", len(fills) >= 1,
        len(fills), ">= 1")

    #  *** THE ROW THE DEFECT WAS: a fill that exists only inside one subtype arm
    #  is not a fill.  It must come BEFORE the subtype switch, so every arm
    #  inherits it.  This is the property, and it is an ORDER property -- which
    #  is why counting fills is not enough.
    m_switch = re.search(r"switch\s*\(\s*machine->machine_subtype\s*\)", src)
    row("E3 the subtype switch is still where this file expects",
        bool(m_switch), bool(m_switch), True)
    ok_order = bool(m_alloc) and bool(m_switch) and any(
        m_alloc.start() < f < m_switch.start() for f in fills)
    row("E4 the buffer is filled BEFORE the subtype switch, so every arm inherits it",
        ok_order,
        "fills at %s, switch at %s" % (fills, m_switch.start() if m_switch else None),
        "at least one fill between the malloc and the switch")

    #  ---- the FORMAT, which is what an ASan-only oracle cannot see -----------
    #
    #  `eaddr_string[0] = '\0'` silences ASan completely and hands the guest an
    #  EMPTY MAC.  So assert the SHAPE of what is written, not merely that
    #  something is.  Six colon-separated 2-digit hex fields, i.e. 17 characters.
    pre = src[m_alloc.start():m_switch.start()] if (m_alloc and m_switch) else ""
    mac_fmt = "%02x:%02x:%02x:%02x:%02x:%02x"
    row("E5 the pre-switch fill writes a full six-octet MAC format",
        mac_fmt in pre, mac_fmt in pre, True)
    row("E6 it is fed six macaddr octets, not a truncated list",
        len(re.findall(r"macaddr\[\d\]", pre)) >= 6,
        len(re.findall(r"macaddr\[\d\]", pre)), ">= 6")

    #  ---- IDENTITY ----------------------------------------------------------
    row("E0 IDENTITY row count -- guards against a stale copy",
        len(_rows) + 1 == EXPECT_ROWS, len(_rows) + 1, EXPECT_ROWS)

    bad = sum(1 for _, ok in _rows if not ok)
    print()
    print("SGI_EADDR_RESULT=%d/%d" % (len(_rows) - bad, len(_rows)))
    print("SGI_EADDR_PASS" if bad == 0 else "SGI_EADDR_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
