#!/usr/bin/env python3
"""#444 DETECTOR: every `hpcmips` subtype the binary advertises in `-H` can
actually be CONSTRUCTED, instead of three of eight core-dumping inside
`interrupt_handler_lookup()`.

Rung 2 (machine construction), and that is the CEILING here rather than a
shortcut -- the defect kills the process during `MACHINE_SETUP(hpcmips)`, so
a rung-3 cold-debugger probe is not merely unnecessary but impossible: a probe
needs a constructed machine and construction is what aborted.

WITNESS vs DETECTOR.  The pre-fix witness (`_scratchpad/hpcabort_witness.py`)
asserts the SYMPTOM -- 3 of 8 advertised subtypes SIGABRT -- so it correctly
goes red once the defect is gone.  This file asserts the REPAIRED property, is
red on the pre-fix build, and is built to fail on the mutants listed at the
foot of this docstring.  Grading one by the other's clauses is a category error
in either direction.

THE DEFECT, and every line number below was read out of the file today.
`device_add()` copies an `irq=` value VERBATIM into `devinit.interrupt_path`
(`src/devices/device.c:336-339`); `DEVINIT(ns16550)` hands that string to
`INTERRUPT_CONNECT` (`src/devices/dev_ns16550.c:342`); a name that is neither
empty nor a registered path falls out of the scan loop in
`src/core/interrupt.c` and reaches :190-198, which prints the failing name,
prints every registered path, prints "Aborting." and calls `abort()`.  Three
arms of `MACHINE_SETUP(hpcmips)` passed a bare integer where a dotted path
belongs -- "0" for the two Casio arms and "17" for the Agenda VR3 -- so those
three subtypes could not be started at all.

TWO WRONGNESSES, and the detector has to see both.  `dev_vr41xx_init()` is what
REGISTERS the `...vrip.N` names (`src/devices/dev_vr41xx.c:691-702`, lines
0..25).  The BE-300 and E-105 arms called `device_add` BEFORE it, so correcting
only the string would still abort -- at the moment of failure not one `vrip.`
name existed.  Rows A3/A4 see that because the run still dies; row S2 sees it
in the source ORDER, so the two halves are checked independently.

*** THE KNOWN RESIDUAL IS PINNED, NOT HIDDEN -- see row R1. ***  Fixing the
abort exposes a SECOND, MILDER defect that the abort used to mask: on the three
arms that add a UART of their own, `dev_vr41xx_init()` has ALREADY added an
ns16550 of its own (`dev_vr41xx.c:777-787`) with `device_add`'s default
`in_use = 1` (`device.c:266`).  Two console inputs then exist, and
`console_warn_if_slaves_are_needed()` (`src/console/console.c:994-1007`)
exit(1)s unless slave xterms are enabled.  MEASURED: `-x` makes all eight reach
the debugger prompt, and `in_use=0` on the machine's own UART does too.  That
is a separate fix with a separate judgement behind it (which of the two UARTs
is the console on real hardware is not knowable from this tree), so #444 does
not make it, and R1 pins the residual as a FAIL-CLOSED ALLOWLIST: the set is
derived from the source rather than hardcoded, and EXPECT_X_ONLY must be edited
to 0 in the same commit that closes it.

WHAT THIS FILE DOES NOT CLAIM.  Nothing about whether a real hpcmips guest
boots, and nothing about whether `VRIP_INTR_SIU` is the CORRECT hardware line
for these UARTs.  There is no VR41xx datasheet in this tree; the line is a
JUDGEMENT and the round records it as one.  Only the path FORM is measured --
row C3 shows a registered `vrip.N` being accepted and row C4 shows `vrip.N+1`
still aborting, which is what makes acceptance a real lookup rather than a
no-op.

*** A LINE THAT IS WRONG BUT REGISTERED IS NOT CAUGHT BEHAVIOURALLY BY
ANYTHING IN THIS FILE, AND THAT WAS MEASURED. ***  `VRIP_INTR_SIU + 1` is
vrip.10, which `dev_vr41xx_init` HAS registered, so it connects in silence and
scored 26/26 against every run-based row here.  Row S1 is what closes it, and
S1 is a SOURCE-TEXT row -- see its comment for exactly what it does and does
not buy.

MUTANTS THIS FILE IS BUILT TO KILL (every one built, compiled and MEASURED --
see the round record for the scores):
  * the pre-fix source                                    -> A3 A4 A5 B1 C5 S1 S2 S3 R1
  * only one of the three arms corrected                  -> A3 A4 A5 B1 S1 S2 S3 R1
  * the string corrected but `device_add` NOT moved below
    `dev_vr41xx_init` on the two Casio arms               -> A3 A4 A5 B1 S2 R1
  * `VRIP_INTR_SIU` replaced by an out-of-range line 26   -> A3 A4 A5 B1 C5 S1 R1
  * `machine->path` replaced by a hardcoded "machine[0]"  -> C5 ONLY
  * `VRIP_INTR_SIU + 1` -- registered, so wired in silence -> S1 ONLY

usage:  python3 -u regress/hpcmips_ctor_probe.py [options]
        run under WSL (`wsl -d Gentoo`); the binary is a Linux ELF.
        --binary PATH   the gxemul to test  (default $GXROOT/build/gxemul)
        --source PATH   machine_hpcmips.c for the STATIC rows.  Default: the
                        copy in the BINARY's own tree if there is one, else the
                        committed source -- the static rows must read the text
                        that produced the binary, not some other tree's.
        --timeout N     per-run wall budget, seconds (default 40)
"""

import argparse
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

SIGABRT = int(signal.SIGABRT)          # 6 on Linux

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.environ.get("GXROOT") or os.path.dirname(os.path.dirname(HERE))
SEC_SRC = os.path.join(os.path.dirname(HERE), "src", "machines",
                       "machine_hpcmips.c")
MACHINE = "hpcmips"

#  The IDENTITY constant.  A probe copied into a tree where it no longer runs
#  all of its rows must not report a green verdict over a shorter file.
EXPECT_ROWS = 26

#  FAIL-CLOSED ALLOWLIST for the residual described in the docstring: how many
#  advertised subtypes still need `-x` because they end up with two console
#  inputs.  The MEMBERS are derived from the source (the arms that add a UART of
#  their own); this number pins the SIZE so the derivation cannot quietly drift.
#  It goes to 0 in the same commit that gives those UARTs `in_use=0` -- or that
#  otherwise settles which of the two is the console.
EXPECT_X_ONLY = 3

#  debugger.c:107.  A debugger command line longer than this is TRUNCATED IN
#  SILENCE -- see the comment on rows C3/C4, which is where it bit.
MAX_CMD_BUFLEN = 72

# ---------------------------------------------------------------------------
# Result classes.  NOT_RUN is a first-class value and is never "ok": a subtype
# whose run never happened must produce a RED row, not a blank.
# ---------------------------------------------------------------------------
OK = "CONSTRUCTED_OK"          # constructed AND reached the debugger prompt
LOOKUP = "ABORT_LOOKUP"        # SIGABRT *at interrupt_handler_lookup*
XONLY = "NEEDS_XTERM_SLAVES"   # constructed, then exit(1) for two console inputs
ABORT_OTHER = "ABORT_OTHER"    # SIGABRT somewhere else entirely
SIG_OTHER = "SIGNAL_%d"
EXIT_OTHER = "EXIT_%s"
TIMEOUT = "TIMEOUT"
NOT_RUN = "NOT_RUN"

#  Classes in which MACHINE_SETUP itself ran to completion.  XONLY belongs here
#  and LOOKUP does not: that is the whole distinction #444 turns on.
CONSTRUCTED = (OK, XONLY)

_rows = []


def row(name, ok, got, want):
    _rows.append((name, bool(ok)))
    print("  [%s] %-58s got=%s want=%s" % ("ok" if ok else "FAIL", name,
                                           got, want))


def note(s):
    print("  --- %s" % s)


# ---------------------------------------------------------------------------
# Classifier.  A pure function of (returncode, output) so it can be
# unit-checked without spawning anything -- see the F rows.
# ---------------------------------------------------------------------------
def classify(rc, out):
    if rc is None:
        return NOT_RUN
    if rc == "timeout":
        return TIMEOUT
    if rc < 0:
        sig = -rc
        if sig == SIGABRT:
            #  "the process died" and "it died HERE" are different claims.
            #  Only the diagnostic makes it the second one.
            if "interrupt_handler_lookup(" in out and "Aborting." in out:
                return LOOKUP
            return ABORT_OTHER
        return SIG_OTHER % sig
    built = "cpu:" in out and "memory:" in out and "cpu0: starting at" in out
    if rc == 1 and built and "More than one console input" in out:
        return XONLY
    if rc == 0 and built and "GXemul>" in out:
        return OK
    return EXIT_OTHER % rc


def failing_name(out):
    m = re.search(r'interrupt_handler_lookup\("([^"]*)"\) failed', out)
    return m.group(1) if m else None


def available_handlers(out):
    """The list the aborting process prints between its header and 'Aborting.'"""
    m = re.search(r"Available handler paths are:\n(.*?)\nAborting\.", out, re.S)
    if not m:
        return None
    return [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]


# ---------------------------------------------------------------------------
def _run(argv, tmo, feed=b"quit\n"):
    """Returns (rc, out).  rc is an int (negative => killed by that signal),
    the string "timeout", or None if the run could not be started at all."""
    try:
        p = subprocess.run(argv, input=feed, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=tmo)
        return p.returncode, p.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired as e:
        return "timeout", (e.stdout or b"").decode("utf-8", "replace")
    except OSError as e:
        print("  !! could not start %r: %s" % (argv, e))
        return None, ""


# ---------------------------------------------------------------------------
# Enumeration.  From the BINARY's own -H, never a hardcoded list: a hardcoded
# roster that drifts is exactly the stale-record class this project keeps paying
# for.  The parse follows gate 9's awk, gate_asan_sweep.sh:233-249 (OPENED, not
# remembered -- an earlier draft cited :50-55, which is prose about the sweep's
# cost and not the parser at all): a type line is indented 8 and carries
# ("name"); its subtypes are indented 12 and start with "- ".  The alias
# character class is that awk's WIDENED one, `[A-Za-z0-9_.+/-]`, for the reason
# its own comment at :56-58 records -- the narrow lowercase class silently
# re-attributed one machine's subtypes to another.
# ---------------------------------------------------------------------------
def enumerate_subtypes(bin_path, machine, tmo):
    rc, text = _run([bin_path, "-H"], tmo, feed=b"")
    subs, in_block = [], False
    for line in text.splitlines():
        mtype = re.match(r'^ {8}\S.*\("([A-Za-z0-9_.+/-]+)"', line)
        if mtype:
            in_block = (mtype.group(1) == machine)
            continue
        if in_block:
            msub = re.match(r'^ {12}- (.*?)\s*\((.*)\)\s*$', line)
            if msub:
                aliases = re.findall(r'"([^"]+)"', msub.group(2))
                if aliases:
                    subs.append((msub.group(1), aliases))
    return subs


# ---------------------------------------------------------------------------
# Source scan, bounded to MACHINE_SETUP.  This file switches on
# machine->machine_subtype THREE times -- MACHINE_SETUP, MACHINE_DEFAULT_CPU and
# MACHINE_DEFAULT_RAM -- and an unbounded scan silently keeps the LAST arm for
# each constant, i.e. the RAM table, which holds no device_add and no irq at
# all.  Bound it, or the S rows measure nothing.
# ---------------------------------------------------------------------------
def strip_comments(text):
    """Blank out /* ... */ bodies, PRESERVING the line count so every number
    printed below is still the number in the file.  Doing it per line with a
    'starts with *' test was the first draft and it is not closed: a comment
    whose continuation line happens to begin with prose reads as code, and the
    S rows would then see `VRIP_INTR_SIU` in a sentence ABOUT the constant."""
    out, i = [], 0
    while True:
        j = text.find("/*", i)
        if j < 0:
            out.append(text[i:])
            return "".join(out)
        out.append(text[i:j])
        k = text.find("*/", j + 2)
        if k < 0:
            out.append("\n" * text[j:].count("\n"))
            return "".join(out)
        out.append("\n" * text[j:k].count("\n"))
        i = k + 2


def scan_source(path):
    text = strip_comments(
        open(path, "r", encoding="utf-8", errors="replace").read())
    lines = text.splitlines()

    const_aliases = {}
    for m in re.finditer(
            r'machine_entry_add_subtype\s*\(\s*me\s*,\s*"([^"]*)"\s*,\s*'
            r'(MACHINE_\w+)\s*,\s*((?:"[^"]*"\s*,\s*)+)NULL\s*\)', text, re.S):
        const_aliases[m.group(2)] = re.findall(r'"([^"]*)"', m.group(3))

    setup_lo = setup_hi = None
    for i, ln in enumerate(lines, 1):
        if setup_lo is None and re.match(r'^MACHINE_SETUP\(', ln):
            setup_lo = i
        elif setup_lo is not None and re.match(r'^\}', ln):
            setup_hi = i
            break
    if setup_lo is None or setup_hi is None:
        return const_aliases, {}

    starts = []
    for i, ln in enumerate(lines, 1):
        if not (setup_lo <= i <= setup_hi):
            continue
        m = re.match(r'^\tcase\s+(MACHINE_\w+):', ln)
        if m:
            starts.append((i, m.group(1)))
        elif re.match(r'^\tdefault:', ln):
            starts.append((i, None))

    arms = {}
    for idx, (lno, const) in enumerate(starts):
        if const is None:
            continue
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines) + 1
        body = lines[lno - 1:end - 1]
        info = {"case_line": lno, "irqs": [], "device_add_lines": [],
                "vr41xx_lines": [], "code": "\n".join(body)}
        for off, bl in enumerate(body):
            n = lno + off
            for m in re.finditer(r'irq=([^\s"]*)', bl):
                info["irqs"].append((n, m.group(1)))
            if "device_add(" in bl:
                info["device_add_lines"].append(n)
            if "dev_vr41xx_init(" in bl:
                info["vr41xx_lines"].append(n)
        arms[const] = info
    return const_aliases, arms


def siu_form(code):
    """How an arm spells the VRIP line it hands to device_add.  "plain" is the
    constant passed WHOLE as one argument; anything else is named so the S1 row
    can say WHICH escape it saw rather than only that one happened."""
    if re.search(r'VRIP_INTR_SIU\s*[-+*/]', code) or \
       re.search(r'[-+*/]\s*VRIP_INTR_SIU', code):
        return "arithmetic"
    if re.search(r'VRIP_INTR_SIU\s*[,)]', code):
        return "plain"
    if "VRIP_INTR_SIU" in code:
        return "other-use"
    return "absent"


def is_path_like(arg):
    """A registered interrupt name is a dotted path ("machine[0].cpu[0].2"),
    and every in-tree producer builds it from machine->path with a '.' in it
    (dev_vr41xx.c:684, :693, :709).  An argument with no '.' cannot be one --
    "0" and a bare "%i" have no dot.  Stated, rather than assumed."""
    return "." in arg


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--binary",
                    default=os.path.join(DEFAULT_ROOT, "build", "gxemul"))
    ap.add_argument("--source", default=None)
    ap.add_argument("--timeout", type=int, default=40)
    a = ap.parse_args()

    binary = os.path.abspath(a.binary)
    #  The static rows must read the text that produced THIS binary.  Reading
    #  the committed source while testing some other tree's binary is how a
    #  green S row gets attributed to a build it never described.
    src = a.source
    if src is None:
        cand = os.path.join(os.path.dirname(binary), "src", "machines",
                            "machine_hpcmips.c")
        src = cand if os.path.isfile(cand) else SEC_SRC
    src = os.path.abspath(src)

    print("#444  hpcmips machine construction -- DETECTOR (rung 2)")
    print("  binary = %s" % binary)
    print("  source = %s" % src)

    # ---- instrument -------------------------------------------------------
    have = os.path.isfile(binary) and os.access(binary, os.X_OK)
    row("P1 binary present and executable", have, have, True)

    #  stdbuf: abort() does NOT flush stdio, and stdout to a PIPE is block
    #  buffered -- without this the diagnostic is LOST and an aborting run
    #  looks like a bare core dump with no evidence of WHERE it died.  Measured
    #  on this very defect before the guard existed.  Absent stdbuf must FAIL,
    #  never quietly measure nothing.
    sb = shutil.which("stdbuf")
    row("P2 stdbuf present (abort() does not flush a buffered stdout)",
        sb is not None, sb, "a path")

    tmp = tempfile.mkdtemp(prefix="hpcctor.")
    raw = os.path.join(tmp, "raw.bin")
    try:
        with open(raw, "wb") as f:
            f.write(b"\0" * 64)
        made = os.path.getsize(raw) == 64
    except OSError:
        made = False
    #  A RAW load, not an ELF: the machine constructs, the loader accepts it,
    #  the debugger prompt is reached and `quit` gives a clean rc=0.  With a
    #  bogus ELF every healthy subtype exits 1 at the loader instead, and then
    #  "constructed" and "exit status" stop agreeing.
    row("P3 a 64-byte RAW image exists for the loader", made, made, True)

    # ---- F rows: the classifier itself, nothing spawned --------------------
    row("F1 absent data is not ok (classify(None,'') is NOT_RUN)",
        classify(None, "") == NOT_RUN, classify(None, ""), NOT_RUN)
    row("F2 rc=0 with no construction evidence is not ok",
        classify(0, "") != OK, classify(0, ""), "not " + OK)
    row("F3 a SIGABRT WITHOUT the diagnostic is not scored as this defect",
        classify(-SIGABRT, "boom") == ABORT_OTHER,
        classify(-SIGABRT, "boom"), ABORT_OTHER)
    row("F4 a SIGABRT WITH the diagnostic is scored as this defect",
        classify(-SIGABRT, 'interrupt_handler_lookup("0") failed.\nAborting.')
        == LOOKUP, LOOKUP, LOOKUP)
    row("F5 a timeout is not ok",
        classify("timeout", "cpu: memory: cpu0: starting at GXemul>")
        == TIMEOUT,
        classify("timeout", "cpu: memory: cpu0: starting at GXemul>"), TIMEOUT)

    if not (have and sb and made):
        return finish()
    stdbuf = [sb, "-o0", "-e0"]
    rawspec = "0x80000000:" + raw

    def run_sub(alias, extra=(), feed=b"quit\n"):
        argv = list(stdbuf) + [binary, "-V"] + list(extra) + \
            ["-E", MACHINE, "-e", alias, rawspec]
        return _run(argv, a.timeout, feed)

    # ---- enumeration -------------------------------------------------------
    subs = enumerate_subtypes(binary, MACHINE, a.timeout)
    row("E1 subtypes enumerated from the binary's own -H (not hardcoded)",
        len(subs) >= 2, len(subs), ">= 2")
    for disp, al in subs:
        note("-H says: %-28s %s" % (disp, ", ".join(al)))
    if len(subs) < 2:
        return finish()

    # ---- mode A: default flags ---------------------------------------------
    #  Every enumerated subtype starts as NOT_RUN.  Nothing downstream may turn
    #  a missing measurement into a pass.
    res = {al[0]: [NOT_RUN, ""] for _, al in subs}
    print("  RUNS A -- default flags:")
    for _disp, al in subs:
        rc, out = run_sub(al[0])
        res[al[0]] = [classify(rc, out), out]
        nm = failing_name(out)
        print("    %-14s rc=%-9s %-20s %s"
              % (al[0], rc, res[al[0]][0],
                 ("name=%r" % nm) if nm is not None else ""))

    a_lookup = sorted(k for k, v in res.items() if v[0] == LOOKUP)
    a_xonly = sorted(k for k, v in res.items() if v[0] == XONLY)
    a_built = sorted(k for k, v in res.items() if v[0] in CONSTRUCTED)
    a_other = sorted(k for k, v in res.items() if v[0] not in CONSTRUCTED)

    row("A1 every enumerated subtype produced a result (no NOT_RUN)",
        all(v[0] != NOT_RUN for v in res.values()),
        sum(1 for v in res.values() if v[0] == NOT_RUN), 0)
    row("A2 no run hit the wall clock",
        all(v[0] != TIMEOUT for v in res.values()),
        sum(1 for v in res.values() if v[0] == TIMEOUT), 0)
    row("A3 NO subtype dies inside interrupt_handler_lookup",
        not a_lookup, "%d aborting %s" % (len(a_lookup), a_lookup),
        "0 aborting")
    row("A4 every advertised subtype completes MACHINE_SETUP",
        len(a_built) == len(subs), "%d/%d" % (len(a_built), len(subs)),
        "%d/%d" % (len(subs), len(subs)))
    row("A5 no subtype failed in some third, unclassified way",
        not a_other, [(k, res[k][0]) for k in a_other], [])

    # ---- mode B: with slave xterms enabled ---------------------------------
    #  `-x` is an ordinary in-tree flag, not a source edit: it does not change
    #  the machine description, the device set or the dispatch.  It is what
    #  turns "MACHINE_SETUP finished" into "the emulator is actually usable",
    #  which is the property a user cares about.
    print("  RUNS B -- with -x (slave xterms allowed):")
    bres = {al[0]: NOT_RUN for _, al in subs}
    for _disp, al in subs:
        rc, out = run_sub(al[0], extra=("-x",))
        bres[al[0]] = classify(rc, out)
        print("    %-14s rc=%-9s %s" % (al[0], rc, bres[al[0]]))
    b_ok = sorted(k for k, v in bres.items() if v == OK)
    row("B1 with -x, EVERY advertised subtype reaches the debugger prompt",
        len(b_ok) == len(subs), "%d/%d ok, others=%s"
        % (len(b_ok), len(subs),
           [(k, v) for k, v in sorted(bres.items()) if v != OK]),
        "%d/%d" % (len(subs), len(subs)))

    # ---- controls ----------------------------------------------------------
    rc, out = run_sub("nosuchsubtype")
    cls = classify(rc, out)
    row("C1 LIVENESS: a bogus subtype is rejected, not scored as constructed",
        cls not in CONSTRUCTED and "Unknown subtype" in out, cls,
        "rejected, not " + OK)

    #  A machine that DOES abort for an unrelated reason (measured:
    #  "bus_pci_add(): pci_data == NULL!").  This is the row that stops some
    #  future unrelated crash being scored as this defect -- or, worse, this
    #  defect's return being scored as something else.
    rc, out = _run(list(stdbuf) + [binary, "-V", "-E", "mvmeppc", "-e",
                                   "mvme1600", rawspec], a.timeout)
    cls = classify(rc, out)
    last = ([ln for ln in out.strip().splitlines() if ln.strip()] or [""])[-1]
    row("C2 an UNRELATED SIGABRT classifies %s, not %s" % (ABORT_OTHER, LOOKUP),
        cls == ABORT_OTHER, "%s (%s)" % (cls, last.strip()[:40]), ABORT_OTHER)

    #  C3/C4 -- the DEVICE-SIGNATURE control, and the reason "the path is
    #  accepted" is a measurement rather than a tautology.  `device add` in the
    #  debugger (debugger_cmds.c:552-553) reaches the SAME device_add ->
    #  DEVINIT -> INTERRUPT_CONNECT path the machine setup uses, on a machine
    #  that is already constructed.  Feed it a name that cannot exist; the
    #  abort prints every registered path, from which the highest vrip line is
    #  DERIVED rather than remembered.  Then N must connect and N+1 must not.
    #  Both rows are green on the pre-fix binary too: they check the
    #  instrument, not the fix.
    #
    #  *** KEEP EVERY DEBUGGER COMMAND UNDER MAX_CMD_BUFLEN, debugger.c:107.
    #  IT IS 72, AND A LONGER LINE IS TRUNCATED IN SILENCE. ***  The first
    #  draft of these rows sent 73 and 78 characters; the trailing digits of
    #  the path were eaten, so BOTH the accept and the reject arms aborted on
    #  "...vrip." and C3 read as a failure of the fix rather than of the probe.
    #  The rows caught it only because C4 compares the failing name against the
    #  exact string it sent -- which is why it does.
    host = (b_ok or a_built or [None])[0]
    dev = "device add ns16550 addr=0x0d00%04x irq=%s.cpu[%i].vrip.%s"
    maxline, hs = None, []
    if host is not None:
        cmd = dev % (0x1000, "machine[0]", 0, "x")
        note("instrument cmd (%d chars, limit %d): %s"
             % (len(cmd), MAX_CMD_BUFLEN - 1, cmd))
        rc, out = run_sub(host, extra=("-x",),
                          feed=(cmd + "\nquit\n").encode())
        hs = available_handlers(out) or []
        ns = [int(m.group(1)) for m in
              (re.search(r"\.vrip\.(\d+)$", h) for h in hs) if m]
        maxline = max(ns) if ns else None
    note("instrument host=%s registered handlers=%d highest vrip line=%s"
         % (host, len(hs), maxline))

    good = bad = None
    if maxline is not None:
        cmd = dev % (0x2000, "machine[0]", 0, maxline)
        rc, out = run_sub(host, extra=("-x",),
                          feed=(cmd + "\nquit\n").encode())
        good = classify(rc, out)
        if len(cmd) >= MAX_CMD_BUFLEN:
            good = "COMMAND_TOO_LONG_FOR_THE_DEBUGGER"
        cmd = dev % (0x3000, "machine[0]", 0, maxline + 1)
        rc, out = run_sub(host, extra=("-x",),
                          feed=(cmd + "\nquit\n").encode())
        bad = (classify(rc, out), failing_name(out))
    row("C3 INSTRUMENT: a REGISTERED vrip.%s is accepted by the same path"
        % maxline, good == OK, good, OK)
    row("C4 INSTRUMENT: an UNREGISTERED vrip.%s still aborts (so C3 is a real "
        "lookup)" % (maxline + 1 if maxline is not None else "?"),
        bad is not None and bad[0] == LOOKUP
        and bad[1] == "machine[0].cpu[0].vrip.%s" % (maxline + 1),
        bad, (LOOKUP, "machine[0].cpu[0].vrip.%s"
              % (maxline + 1 if maxline is not None else "?")))

    #  C5 -- the path is PER MACHINE.  A hardcoded "machine[0]" passes every
    #  row above, because a single-machine run has no other path to confuse it
    #  with.  Put a NON-VR machine in slot 0 so that "machine[0].cpu[0].vrip.N"
    #  does not exist at all, and the hardcode aborts while machine->path does
    #  not.  This is the only row that separates the two.
    conf = os.path.join(tmp, "two.conf")
    with open(conf, "w") as f:
        f.write('machine(\n\ttype("dec")\n\tsubtype("5000/200")\n'
                '\tload("%s")\n)\n' % rawspec)
        f.write('machine(\n\ttype("%s")\n\tsubtype("%s")\n\tload("%s")\n)\n'
                % (MACHINE, (a_xonly or [subs[0][1][0]])[0], rawspec))
    rc, out = _run(list(stdbuf) + [binary, "-V", "-x", "@" + conf], a.timeout)
    cls = classify(rc, out)
    row("C5 hpcmips as machine[1] behind a non-VR machine[0] still constructs",
        cls == OK and out.count("cpu0: starting at") == 2,
        "%s, cpu0 lines=%d, %s"
        % (cls, out.count("cpu0: starting at"), failing_name(out)),
        "%s, cpu0 lines=2, None" % OK)

    # ---- static rows -------------------------------------------------------
    const_aliases, arms = scan_source(src)
    row("S0 machine-setup switch arms found in %s" % os.path.basename(src),
        len(arms) >= 2, len(arms), ">= 2")

    print("  SOURCE SITES -- line numbers read out of the file today:")
    print("  %-34s %-6s %-9s %-9s %-9s %s"
          % ("case constant", "case", "irq line", "dev_add", "vr41xx", "SIU"))
    bad_irq, unordered, adders, no_siu = [], [], [], []
    for const, info in sorted(arms.items(), key=lambda kv: kv[1]["case_line"]):
        da, vr = info["device_add_lines"], info["vr41xx_lines"]
        print("  %-34s %-6d %-9s %-9s %-9s %s"
              % (const, info["case_line"],
                 ",".join(str(n) for n, _ in info["irqs"]) or "-",
                 ",".join(map(str, da)) or "-",
                 ",".join(map(str, vr)) or "-", siu_form(info["code"])))
        prim = (const_aliases.get(const) or [None])[0]
        if prim is None:
            continue
        if any(not is_path_like(v) for _, v in info["irqs"]):
            bad_irq.append(prim)
        if da:
            adders.append(prim)
            if siu_form(info["code"]) != "plain":
                no_siu.append((prim, siu_form(info["code"])))
            if vr and min(da) < min(vr):
                unordered.append(prim)

    #  *** S1 IS THE ONLY ROW THAT SEES A WRONG-BUT-REGISTERED LINE, AND THAT
    #  IS A MEASURED CLAIM, NOT A GUESS. ***  `VRIP_INTR_SIU + 1` is vrip.10,
    #  which dev_vr41xx_init HAS registered, so it connects in silence: that
    #  mutant scored 26/26 against every behavioural row in this file before
    #  this row was tightened.  The shape is banned rather than the value,
    #  because the defect being fixed WAS an arithmetic adjustment of this very
    #  constant -- the Agenda arm used to pass `8+VRIP_INTR_SIU` -- so "the
    #  constant itself, whole, as one argument" is the property with history
    #  behind it.  Anchored through the argument separator for the reason
    #  gate_hygiene.sh:229-236 records: a check that stops at a PREFIX admits
    #  the broken form as a substring of the fixed one.
    #
    #  HONEST LIMIT, stated rather than papered over: this is a SOURCE-TEXT
    #  row.  It cannot say the line is right for the HARDWARE -- no VR41xx
    #  datasheet exists in this tree, the line is a JUDGEMENT, and the round
    #  records it as one -- and it would not notice VRIP_INTR_SIU being
    #  redefined in vripreg.h.  Catching a wrong-but-registered line
    #  BEHAVIOURALLY needs the UART to raise an interrupt and a guest load to
    #  read back which VRIP line latched, which is a rung-3 probe and a
    #  separate piece of work.
    row("S1 every UART-adding arm passes VRIP_INTR_SIU itself, no arithmetic",
        not no_siu, sorted(no_siu), [])
    row("S2 no arm calls device_add BEFORE dev_vr41xx_init",
        not unordered, sorted(unordered), [])
    row("S3 no arm passes a non-path irq argument", not bad_irq,
        sorted(bad_irq), [])

    # ---- R1: the pinned residual ------------------------------------------
    #  MEMBERS derived from the source, SIZE pinned.  Both halves are needed:
    #  the derivation alone would follow the code anywhere, and the count alone
    #  would not say WHICH.  See the docstring for what closes this.
    row("R1 residual (allowlist): exactly the UART-adding arms need -x",
        sorted(a_xonly) == sorted(adders)
        and len(a_xonly) == EXPECT_X_ONLY,
        "%s (%d)" % (sorted(a_xonly), len(a_xonly)),
        "%s (%d)" % (sorted(adders), EXPECT_X_ONLY))

    shutil.rmtree(tmp, ignore_errors=True)
    return finish()


def finish():
    row("I1 IDENTITY row count -- guards against a stale copy",
        len(_rows) + 1 == EXPECT_ROWS, "rows=%d" % (len(_rows) + 1),
        "rows=%d" % EXPECT_ROWS)
    fails = sum(1 for _, ok in _rows if not ok)
    print()
    print("HPCMIPS_CTOR_RESULT=%d/%d" % (len(_rows) - fails, len(_rows)))
    print("HPCMIPS_CTOR_PASS" if fails == 0 else "HPCMIPS_CTOR_FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
