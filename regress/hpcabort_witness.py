#!/usr/bin/env python3
"""`hpcabort` WITNESS -- three of the eight `hpcmips` subtypes the shipped
binary advertises in `-H` CORE-DUMP during machine construction.

*** RUNG 2 (WITNESS LADDER), AND THE CLAIM IS MADE EXPLICITLY BECAUSE RUNG 2 IS
    NOT GENERALLY A REPRODUCTION. ***

CLAUDE.md's ladder rates MACHINE CONSTRUCTION as "a reproduction ONLY for
defects in code construction itself executes (init-time, e.g. the macppc heap
OOB #23).  Never for access-path defects: registration proves presence, not
reachability."

This defect IS the init-time case, and nothing weaker would do:

  * The failing call is `INTERRUPT_CONNECT(devinit->interrupt_path, d->irq)` at
    `src/devices/dev_ns16550.c:342`, reached from `DEVINIT(ns16550)` <-
    `device_add()` <- `MACHINE_SETUP(hpcmips)`.  `device_add` is called from the
    machine-setup switch itself, so the *only* way to execute the site is to
    construct the machine.  There is no guest instruction to issue, no address
    to decode and no driver to wait for -- the process is dead before the file
    loader runs, before the debugger prompt, before instruction zero.
  * A rung-3 probe is therefore not merely unnecessary, it is IMPOSSIBLE: a cold
    debugger probe needs a constructed machine, and construction is what aborts.
    A rung-4 boot is impossible for the same reason and additionally for want of
    an image.  Rung 2 is the CEILING here, not a shortcut.
  * The rung-1 exclusion is respected.  Nothing is `#include`d, no function is
    called directly, no stub is substituted.  The ladder's mechanical
    discriminator -- "if it still compiles and still fails after the machine
    description and CPU/device dispatch are removed, it was never a
    reproduction" -- is answered the right way: remove the machine description
    and this measures nothing at all, because the machine description IS the
    defect's carrier.

Ladder clause (iii) is satisfied verbatim: the machine descriptions are the
committed ones, unmodified; no `device_add` of ours is introduced; the binary is
`build/gxemul` as committed.  Clause (ii)'s two controls are C2 (liveness -- the
majority of subtypes construct through the same invocation) and C4/C6 (signature
-- the aborting name is the exact string the committed source passes, and the
set of registered handlers at the moment of failure is the one the source's own
call ORDER predicts).  Clause (i) is the two modes: the default asserts the
SYMPTOM, so it passes today and goes red when the defect is gone;
`--expect-fixed` asserts the repaired property, so it fails today and passes
after the fix.

    HEAD at authoring time: 6bec468 ("#443 sh4pcicexit")
    binary: build/gxemul, ELF x86-64 (built 2026-08-21 01:26), whose build/src
            copies of all five files in the causal chain are `cmp`-identical to
            GXEMUL-SEC's committed source (checked at run time by row P2).

THE DEFECT, read out of the committed source (every line number below was
verified by opening the file; the script re-derives them at run time and prints
what it finds rather than trusting this comment).

`device_add()` parses `irq=` at `src/devices/device.c:336-339` and copies the
value VERBATIM into `devinit.interrupt_path`:

        } else if (strncmp(s2, "irq=", 4) == 0) {
                snprintf(devinit.interrupt_path, interrupt_path_len, "%s", s3);

`DEVINIT(ns16550)` hands that string to `INTERRUPT_CONNECT`
(`dev_ns16550.c:342`), which is `interrupt_handler_lookup()` +
`interrupt_connect()` (`src/include/interrupt.h:77-80`).  A name that is neither
empty nor a registered path falls out of the scan loop and reaches
`src/core/interrupt.c:190-198`, which prints the failing name, prints every
registered path, prints "Aborting." and calls `abort()`.

Three arms of `MACHINE_SETUP(hpcmips)` pass a bare integer where a path belongs.
The other five arms add no `ns16550` at all -- they call only
`dev_vr41xx_init()` -- so there is no latent copy of the bad argument on an
untaken path inside this machine (row S3 checks that mechanically).

TWO DISTINCT WRONGNESSES, and the fix design turns on telling them apart.
`dev_vr41xx_init()` is what REGISTERS the `...vrip.N` handler names
(`dev_vr41xx.c:691-702`, lines 0..25).  The BE-300 and E-105 arms call
`device_add` BEFORE `dev_vr41xx_init`, so at the moment of failure not one
`vrip.` name exists yet; the Agenda VR3 arm calls `dev_vr41xx_init` FIRST, so all
26 do.  Row C6 derives that prediction from the source line ORDER alone and
checks it against the handler list the aborting process actually prints -- which
is the device-signature control the ladder demands, and simultaneously the
measurement that says whether a fix must REORDER an arm or only correct a string.

WHAT THIS FILE DOES NOT CLAIM.  It says nothing about whether a real hpcmips
guest would boot afterwards, and nothing about the CORRECT interrupt line for
the VR41xx SIU -- the source's own comment is unsure ("TODO: Hm... irq 17
according to linux, but VRIP_INTR_SIU (=9) here?") and this script does not
guess.  It measures reachability of the abort, the identity of the failing
string, and the registration state at the moment it fails.  Nothing else.

usage:  python3 -u _scratchpad/hpcabort_witness.py [options]
        run under WSL (`wsl -d Gentoo`); the binary is a Linux ELF.
        --expect-fixed   assert the REPAIRED property instead of the symptom
        --timeout N      per-run wall budget, seconds (default 30)
        --keep           keep the temp dir and print its path
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

# ---------------------------------------------------------------------------
# Paths.  Everything is absolute and explicit.  Rule from CLAUDE.md: never hand
# a bare name to exec -- subprocess/execvp would search $PATH and could pick up
# some other gxemul entirely.
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("GXROOT") or os.path.dirname(HERE)
BIN = os.path.join(ROOT, "build", "gxemul")
SEC = os.path.join(ROOT, "GXEMUL-SEC")
SRC = os.path.join(SEC, "src", "machines", "machine_hpcmips.c")
MACHINE = "hpcmips"

# Files whose committed text this witness cites.  If the build tree's copy of
# any of them differs, the binary under test is not the source under discussion.
CHAIN = [
    "src/machines/machine_hpcmips.c",
    "src/devices/dev_ns16550.c",
    "src/devices/dev_vr41xx.c",
    "src/devices/device.c",
    "src/core/interrupt.c",
]

# ---------------------------------------------------------------------------
# Result classes.  NOT_RUN is a first-class value and is never "ok": a subtype
# whose run never happened must produce a RED row, not a blank.
# ---------------------------------------------------------------------------
OK = "CONSTRUCTED_OK"
LOOKUP = "ABORT_LOOKUP"        # SIGABRT *at interrupt_handler_lookup*
ABORT_OTHER = "ABORT_OTHER"    # SIGABRT somewhere else entirely
SIG_OTHER = "SIGNAL_%d"        # killed by some other signal
EXIT_OTHER = "EXIT_%s"         # ordinary non-zero exit
TIMEOUT = "TIMEOUT"
NOT_RUN = "NOT_RUN"

_rows = []


def row(name, ok, got, want):
    _rows.append((name, bool(ok)))
    print("  [%s] %-56s got=%s want=%s" % ("ok" if ok else "FAIL", name, got, want))


def note(s):
    print("  --- %s" % s)


# ---------------------------------------------------------------------------
# Classifier.  A pure function of (returncode, output) so it can be unit-checked
# without spawning anything -- see the F rows.  rc None means the run never
# completed; that is NOT_RUN and must never fall through to OK.
# ---------------------------------------------------------------------------
def classify(rc, out):
    if rc is None:
        return NOT_RUN
    if rc == "timeout":
        return TIMEOUT
    if rc < 0:
        sig = -rc
        if sig == SIGABRT:
            # "the process died" and "it died HERE" are different claims.  Only
            # the diagnostic makes it the second one.
            if "interrupt_handler_lookup(" in out and "Aborting." in out:
                return LOOKUP
            return ABORT_OTHER
        return SIG_OTHER % sig
    if rc == 0 and "cpu:" in out and "memory:" in out:
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
# Enumeration.  From the BINARY's own -H, never a hardcoded list: a hardcoded
# roster that drifts is exactly the stale-record class this project keeps paying
# for.  The parse follows gate 9's awk (regress/gate_asan_sweep.sh:50-55): a type
# line is indented 8 and carries ("name"); its subtypes are indented 12 and
# start with "- ".
# ---------------------------------------------------------------------------
def enumerate_subtypes(bin_path, machine):
    p = subprocess.run([bin_path, "-H"], stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                       timeout=60)
    text = p.stdout.decode("utf-8", "replace")
    subs, in_block = [], False
    for line in text.splitlines():
        mtype = re.match(r'^ {8}\S.*\("([a-z0-9_.-]+)"', line)
        if mtype:
            in_block = (mtype.group(1) == machine)
            continue
        if in_block:
            msub = re.match(r'^ {12}- (.*?)\s*\((.*)\)\s*$', line)
            if msub:
                aliases = re.findall(r'"([^"]+)"', msub.group(2))
                if aliases:
                    subs.append((msub.group(1), aliases))
    return text, subs


# ---------------------------------------------------------------------------
# Source scan.  Derives, mechanically, which arms pass a non-path irq argument
# and in what order they call device_add vs dev_vr41xx_init.  Reports the ACTUAL
# line numbers found today rather than any remembered ones.
# ---------------------------------------------------------------------------
def scan_source(path):
    text = open(path, "r", encoding="utf-8", errors="replace").read()
    lines = text.splitlines()

    # subtype constant -> aliases, from MACHINE_REGISTER
    const_aliases = {}
    for m in re.finditer(
            r'machine_entry_add_subtype\s*\(\s*me\s*,\s*"([^"]*)"\s*,\s*'
            r'(MACHINE_\w+)\s*,\s*((?:"[^"]*"\s*,\s*)+)NULL\s*\)', text, re.S):
        const_aliases[m.group(2)] = re.findall(r'"([^"]*)"', m.group(3))

    # *** ONLY the MACHINE_SETUP function. ***  This file switches on
    # machine->machine_subtype THREE times -- MACHINE_SETUP, MACHINE_DEFAULT_CPU
    # and MACHINE_DEFAULT_RAM -- and a scan that takes every `case` label in the
    # file silently keeps the LAST arm for each constant, i.e. the RAM table,
    # which contains no device_add and no irq at all.  The first draft of this
    # script did exactly that and reported "0 arms pass a bad irq argument"
    # while the runs beside it were core-dumping.  Bound the scan.
    setup_lo = setup_hi = None
    for i, ln in enumerate(lines, 1):
        if setup_lo is None and re.match(r'^MACHINE_SETUP\(', ln):
            setup_lo = i
        elif setup_lo is not None and re.match(r'^\}', ln):
            setup_hi = i
            break
    if setup_lo is None or setup_hi is None:
        return const_aliases, {}

    # case arms of the machine-setup switch
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
        info = {"case_line": lno, "end_line": end - 1, "irqs": [],
                "device_add_lines": [], "vr41xx_lines": []}
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


def is_path_like(arg):
    """A registered interrupt name is a dotted path ("machine[0].cpu[0].2"), and
    every in-tree producer builds it from machine->path with a '.' in it (see
    dev_vr41xx.c:684, :693, :709).  An argument with no '.' cannot be one.  That
    is the whole rule, stated rather than assumed: "0" and "%i" have no dot."""
    return "." in arg


# ---------------------------------------------------------------------------
def run_subtype(bin_path, machine, alias, rawspec, tmo, stdbuf):
    """Returns (rc, out).  rc is an int (negative => killed by that signal), the
    string "timeout", or None if the run could not be started at all."""
    argv = list(stdbuf) + [bin_path, "-V", "-E", machine, "-e", alias, rawspec]
    return _run(argv, tmo)


def run_raw(bin_path, args, rawspec, tmo, stdbuf):
    argv = list(stdbuf) + [bin_path, "-V"] + args + [rawspec]
    return _run(argv, tmo)


def _run(argv, tmo):
    try:
        p = subprocess.run(argv, input=b"quit\n", stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=tmo, cwd=ROOT)
        return p.returncode, p.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired as e:
        return "timeout", (e.stdout or b"").decode("utf-8", "replace")
    except OSError as e:
        print("  !! could not start %r: %s" % (argv, e))
        return None, ""


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect-fixed", action="store_true",
                    help="assert the repaired property (every advertised "
                         "subtype constructs) instead of the symptom")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()

    print("hpcabort witness -- RUNG 2 (machine construction), %s"
          % ("EXPECT-FIXED mode" if a.expect_fixed else "SYMPTOM mode"))
    print("  ROOT = %s" % ROOT)
    print("  BIN  = %s" % BIN)

    # ---- provenance -------------------------------------------------------
    have_bin = os.path.isfile(BIN) and os.access(BIN, os.X_OK)
    row("P1 binary present and executable", have_bin, have_bin, True)
    if not have_bin:
        print("HPCABORT_WITNESS_RESULT=0/%d" % len(_rows))
        print("HPCABORT_WITNESS_FAIL")
        return 1

    same = []
    for rel in CHAIN:
        s, b = os.path.join(SEC, rel), os.path.join(ROOT, "build", rel)
        try:
            same.append(open(s, "rb").read() == open(b, "rb").read())
        except OSError:
            same.append(False)
    row("P2 build tree byte-identical to committed source (%d files)" % len(CHAIN),
        all(same), sum(same), len(CHAIN))

    try:
        st = subprocess.run(["git", "-C", SEC, "status", "--porcelain", "--", "src"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.DEVNULL,
                            timeout=120).stdout.decode("utf-8", "replace")
        head = subprocess.run(["git", "-C", SEC, "log", "-1", "--format=%h %s"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL,
                              timeout=120).stdout.decode("utf-8", "replace").strip()
    except Exception as e:
        st, head = "?%s: %s" % (type(e).__name__, e), "?"
    note("HEAD: %s" % head)
    row("P3 no uncommitted change under src/", st.strip() == "",
        repr(st.strip()[:60]), "''")

    # stdbuf: abort() does NOT flush stdio, and stdout to a PIPE is block
    # buffered -- without this the diagnostic is LOST and an aborting run looks
    # like a bare 43-byte core dump.  Measured on this very defect before the
    # guard existed.  With stdbuf absent, say so loudly rather than measure
    # nothing and call it a pass.
    sb = shutil.which("stdbuf")
    row("P4 stdbuf present (abort() does not flush a block-buffered stdout)",
        sb is not None, sb, "a path")
    if sb is None:
        print("HPCABORT_WITNESS_RESULT=%d/%d"
              % (sum(1 for _, ok in _rows if ok), len(_rows)))
        print("HPCABORT_WITNESS_FAIL")
        return 1
    stdbuf = [sb, "-o0", "-e0"]

    # ---- F rows: the classifier itself, unit-checked, nothing spawned ------
    row("F1 absent data is not ok (classify(None,'') is NOT_RUN)",
        classify(None, "") == NOT_RUN, classify(None, ""), NOT_RUN)
    row("F2 rc=0 with no construction evidence is not ok",
        classify(0, "") != OK, classify(0, ""), "not " + OK)
    row("F3 a SIGABRT WITHOUT the diagnostic is not scored as this defect",
        classify(-SIGABRT, "boom") == ABORT_OTHER, classify(-SIGABRT, "boom"),
        ABORT_OTHER)
    row("F4 a SIGABRT WITH the diagnostic is scored as this defect",
        classify(-SIGABRT, 'interrupt_handler_lookup("0") failed.\nAborting.')
        == LOOKUP, LOOKUP, LOOKUP)
    row("F5 a timeout is not ok", classify("timeout", "cpu: memory:") == TIMEOUT,
        classify("timeout", "cpu: memory:"), TIMEOUT)

    # ---- enumeration from the binary --------------------------------------
    try:
        _htext, subs = enumerate_subtypes(BIN, MACHINE)
    except Exception as e:
        row("C1 subtypes enumerated from the binary's own -H", False,
            "exception %s" % e, ">= 2")
        print("HPCABORT_WITNESS_RESULT=%d/%d"
              % (sum(1 for _, ok in _rows if ok), len(_rows)))
        print("HPCABORT_WITNESS_FAIL")
        return 1
    row("C1 subtypes enumerated from the binary's own -H (not hardcoded)",
        len(subs) >= 2, len(subs), ">= 2")
    for disp, al in subs:
        note("-H says: %-28s %s" % (disp, ", ".join(al)))
    if len(subs) < 2:
        print("HPCABORT_WITNESS_RESULT=%d/%d"
              % (sum(1 for _, ok in _rows if ok), len(_rows)))
        print("HPCABORT_WITNESS_FAIL")
        return 1

    # ---- source scan -------------------------------------------------------
    const_aliases, arms = scan_source(SRC)
    row("S1 machine-setup switch arms found in %s" % os.path.basename(SRC),
        len(arms) >= 2, len(arms), ">= 2")

    print()
    print("  SOURCE SITES -- line numbers read out of the committed file today:")
    print("  %-34s %-6s %-9s %-10s %-8s %s"
          % ("case constant", "case", "irq line", "irq value", "dev_add",
             "vr41xx_init"))
    predicted_bad, predicted_vrip, = {}, {}
    for const, info in sorted(arms.items(), key=lambda kv: kv[1]["case_line"]):
        bad = [(n, v) for (n, v) in info["irqs"] if not is_path_like(v)]
        da, vr = info["device_add_lines"], info["vr41xx_lines"]
        print("  %-34s %-6d %-9s %-10s %-8s %s"
              % (const, info["case_line"],
                 ",".join(str(n) for n, _ in info["irqs"]) or "-",
                 ",".join(v for _, v in info["irqs"]) or "-",
                 ",".join(map(str, da)) or "-",
                 ",".join(map(str, vr)) or "-"))
        prim = (const_aliases.get(const) or [None])[0]
        if prim is None:
            continue
        if bad:
            predicted_bad[prim] = bad
            # Would the vrip.* names exist yet when device_add runs?  Purely a
            # question of source ORDER inside this one arm.
            predicted_vrip[prim] = bool(vr and da and min(vr) < min(da))
    print()

    row("S2 at least one arm passes a non-path irq argument",
        len(predicted_bad) >= 1, sorted(predicted_bad), ">= 1")
    arms_with_dev_add = set()
    for c, i in arms.items():
        if i["device_add_lines"]:
            p = (const_aliases.get(c) or [None])[0]
            if p:
                arms_with_dev_add.add(p)
    row("S3 every arm that calls device_add has a BAD irq arg (none latent-good)",
        arms_with_dev_add == set(predicted_bad),
        sorted(arms_with_dev_add), sorted(predicted_bad))

    # ---- the runs ----------------------------------------------------------
    tmp = tempfile.mkdtemp(prefix="hpcabort.")
    raw = os.path.join(tmp, "raw.bin")
    with open(raw, "wb") as f:
        f.write(b"\0" * 64)
    # A RAW load rather than an ELF: the machine constructs, the loader accepts
    # it, the debugger prompt is reached, and `quit` gives a clean rc=0.  With a
    # bogus ELF every healthy subtype exits 1 at the loader instead, and then
    # "constructed" and "exit status" stop agreeing -- measured.
    rawspec = "0x80000000:" + raw

    # Every enumerated subtype starts as NOT_RUN.  Nothing downstream may turn a
    # missing measurement into a pass.
    results = {al[0]: [NOT_RUN, "", None] for _, al in subs}

    print("  RUNS -- %s -V -E %s -e <subtype> 0x80000000:<64 zero bytes>, "
          "stdin='quit':" % (os.path.basename(BIN), MACHINE))
    for _disp, al in subs:
        prim = al[0]
        rc, out = run_subtype(BIN, MACHINE, prim, rawspec, a.timeout, stdbuf)
        cls = classify(rc, out)
        results[prim] = [cls, out, rc]
        nm = failing_name(out)
        print("    %-14s rc=%-9s %-16s %s"
              % (prim, rc, cls, ("name=%r" % nm) if nm is not None else ""))
    print()

    row("C3 every enumerated subtype produced a result (no NOT_RUN)",
        all(v[0] != NOT_RUN for v in results.values()),
        sum(1 for v in results.values() if v[0] == NOT_RUN), 0)
    row("C3b no run hit the wall clock",
        all(v[0] != TIMEOUT for v in results.values()),
        sum(1 for v in results.values() if v[0] == TIMEOUT), 0)

    measured_ok = sorted(k for k, v in results.items() if v[0] == OK)
    measured_lookup = sorted(k for k, v in results.items() if v[0] == LOOKUP)
    measured_other = sorted(k for k, v in results.items()
                            if v[0] not in (OK, LOOKUP))

    # ---- C2 LIVENESS -------------------------------------------------------
    row("C2 LIVENESS: at least one subtype constructs via this invocation",
        len(measured_ok) >= 1, measured_ok, ">= 1 subtype")

    # ---- discrimination controls ------------------------------------------
    rc, out = run_subtype(BIN, MACHINE, "nosuchsubtype", rawspec, a.timeout, stdbuf)
    cls = classify(rc, out)
    row("D1 a bogus subtype is neither ok nor this defect",
        cls not in (OK, LOOKUP) and "Unknown subtype" in out, cls,
        "not %s / not %s" % (OK, LOOKUP))
    # A machine that DOES abort, for an unrelated reason (measured today:
    # "bus_pci_add(): pci_data == NULL!").  This is the row that stops a future
    # unrelated crash being scored as this defect.
    rc, out = run_raw(BIN, ["-E", "mvmeppc", "-e", "mvme1600"], rawspec,
                      a.timeout, stdbuf)
    cls = classify(rc, out)
    last = ([ln for ln in out.strip().splitlines() if ln.strip()] or [""])[-1]
    row("D2 an UNRELATED SIGABRT classifies %s, not %s" % (ABORT_OTHER, LOOKUP),
        cls == ABORT_OTHER, "%s (%s)" % (cls, last.strip()[:44]), ABORT_OTHER)

    # ---- C4/C5/C6: signature ----------------------------------------------
    ok_names, ok_bytes, ok_vrip = True, True, True
    for prim in measured_lookup:
        out = results[prim][1]
        nm = failing_name(out)
        bad = predicted_bad.get(prim)
        want_txt = bad[0][1] if bad else None
        # "%i" in the source is a FORMAT, so an exact string compare is only
        # meaningful where the source argument is a literal; where it is a
        # format, require the measured name to be a bare integer -- which is all
        # that format can produce.
        if want_txt is None:
            ok_names = False
        elif "%" in want_txt:
            if nm is None or not re.fullmatch(r"-?\d+", nm):
                ok_names = False
        elif nm != want_txt:
            ok_names = False
        if len(out) < 200 or "Available handler paths are:" not in out:
            ok_bytes = False
        hs = available_handlers(out) or []
        has_vrip = any(".vrip." in h for h in hs)
        if has_vrip != predicted_vrip.get(prim):
            ok_vrip = False
        note("%-12s failing name=%-6r source arg=%-6r handlers registered=%-3d "
             "vrip present=%s (source order predicts %s)"
             % (prim, nm, want_txt, len(hs), has_vrip, predicted_vrip.get(prim)))

    row("C4 SIGNATURE: failing name is the string the committed source passes",
        ok_names, "%s over %d aborting" % (ok_names, len(measured_lookup)), True)
    row("C5 the diagnostic reached the pipe (stdio was not buffered away)",
        ok_bytes, ok_bytes, True)
    row("C6 SIGNATURE: handler set at failure matches the source's call ORDER",
        ok_vrip, ok_vrip, True)

    # ---- C7: the 1:1 claim -------------------------------------------------
    row("C7 aborting set == set predicted from the source's bad irq args",
        measured_lookup == sorted(predicted_bad),
        measured_lookup, sorted(predicted_bad))
    row("C8 no subtype failed in some third way",
        measured_other == [], measured_other, [])
    note("MEASURED: %d abort at interrupt_handler_lookup, %d construct, "
         "%d other, of %d advertised"
         % (len(measured_lookup), len(measured_ok), len(measured_other), len(subs)))

    # ---- the assertion under test -----------------------------------------
    if a.expect_fixed:
        row("W  FIXED: every advertised subtype constructs",
            len(measured_ok) == len(subs) and not measured_lookup,
            "%d/%d ok, %d aborting" % (len(measured_ok), len(subs),
                                       len(measured_lookup)),
            "%d/%d ok, 0 aborting" % (len(subs), len(subs)))
    else:
        row("W  SYMPTOM: advertised subtypes SIGABRT at construction",
            len(measured_lookup) >= 1,
            "%d of %d advertised subtypes abort"
            % (len(measured_lookup), len(subs)), ">= 1 (0 once fixed)")

    if a.keep:
        note("temp dir kept: %s" % tmp)
    else:
        shutil.rmtree(tmp, ignore_errors=True)

    fails = sum(1 for _, ok in _rows if not ok)
    print()
    print("HPCABORT_WITNESS_RESULT=%d/%d" % (len(_rows) - fails, len(_rows)))
    print("HPCABORT_WITNESS_PASS" if fails == 0 else "HPCABORT_WITNESS_FAIL")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
