"""Control suite for .claude/hooks/wsl_dollar_guard.py.

Rebuilt 2026-08-29 after the shipped hook was measured to have a FALSE
NEGATIVE on the shape that actually bites: a multi-line `bash -c '...'` block
whose bare dollar sits on a LATER LINE than the `-c`.

The original 12 controls were run inline and never preserved -- the
volatile-path defect, committed by the author of the rule against it.  This
file is the durable form.

Each row is (name, must_fire, command).  A control suite that only proves the
guard FIRES is half a suite: the two false positives that drove line-scoping
are rows here too, and they must stay SILENT.
"""
import io
import json
import subprocess
import sys

#  *** THE HOOK PATH IS DERIVED, NOT HARDCODED.  It read
#  `C:\DocumentNoSnc\CC\GXEMUL\.claude\hooks\wsl_dollar_guard.py` until 2026-08-30 --
#  ONE MACHINE'S ABSOLUTE PATH, in a tracked file. ***  That is the defect the whole
#  harness migration fixed in 2026-08-17 ("scripts now DERIVE the project root from
#  their own location; they used to hardcode one machine's absolute path, which is only
#  half-tracked"), and this suite was written twelve days later carrying it anyway.
#
#  This file lives at  <root>/GXEMUL-SEC/regress/artifacts/makercfalse/
#  hook_controls_20260829/, so the project root is five levels up.  $GXHOOK overrides.
#
#  IT DELIBERATELY TESTS THE `.claude/` PATH RATHER THAN THE TRACKED ONE: that is what
#  Claude Code actually invokes, so testing it exercises the shim AND the real hook
#  behind it.  Pointing this at the tracked file directly would stop testing the
#  delegation, which is the part that can silently break.
import os as _os
_here = _os.path.dirname(_os.path.abspath(__file__))
_root = _os.path.abspath(_os.path.join(_here, *([_os.pardir] * 5)))
HOOK = _os.environ.get(
    "GXHOOK", _os.path.join(_root, ".claude", "hooks", "wsl_dollar_guard.py"))
if not _os.path.isfile(HOOK):
    raise SystemExit("HOOKCTL_SETUP: no hook at %s -- refusing to report 18 of 18 "
                     "against a file that is not there" % HOOK)
NL = chr(10)
Q = chr(39)
D = chr(36)

CASES = []


def case(name, must_fire, cmd):
    CASES.append((name, must_fire, cmd))


# ---------------------------------------------------------------- MUST FIRE
case("single-line bare var", True,
     "wsl -d Gentoo -- bash -c " + Q + "echo " + D + "S" + Q)
case("single-line " + D + "?", True,
     "wsl -d Gentoo -- bash -c " + Q + "false; echo " + D + "?" + Q)
case("braced " + D + "{V}", True,
     "wsl -d Gentoo -- bash -c " + Q + "echo " + D + "{V}" + Q)
case("with env prefix", True,
     "MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash -c " + Q + "echo " + D + "X" + Q)
case("wsl.exe spelling", True,
     "wsl.exe -- bash -c " + Q + "echo " + D + "X" + Q)
case("--command long form", True,
     "wsl -d Gentoo --command " + Q + "echo " + D + "X" + Q)
case("after a pipe", True,
     "cat f | wsl -- bash -c " + Q + "grep " + D + "P" + Q)

# *** THE MEASURED FALSE NEGATIVE -- this is why the suite was rebuilt. ***
# The dollar is on a LATER LINE than the -c.  This exact shape ran today and
# lost both its variables: a cmp compared against /src/... and reported
# DIVERGED, and gcc looked for /src/devices/... and reported not-found.  Two
# confident wrong answers from one stripped variable.
case("MULTI-LINE, dollar on later line", True,
     "wsl -d Gentoo -- bash -c " + Q + NL +
     "S=/mnt/c/x" + NL +
     "cmp -s /tmp/a " + D + "S/b" + NL + Q)
case("MULTI-LINE, dollar 6 lines down", True,
     "MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash -c " + Q + NL +
     "set -u" + NL + "A=1" + NL + "B=2" + NL + "echo hi" + NL +
     "echo " + D + "A" + NL + Q)

# --------------------------------------------------------------- MUST NOT FIRE
case("escaped " + D + "? (safe form 1)", False,
     "wsl -d Gentoo -- bash -c " + Q + "false; echo " + chr(92) + D + "?" + Q)
case("script file (safe form 2)", False,
     "wsl -d Gentoo -- bash /mnt/c/tmp/s.sh")
case("$(...) outer substitution", False,
     "wsl -d Gentoo -- bash -c " + Q + "echo " + D + "(date)" + Q)
case("no wsl at all", False,
     "python x.py && echo " + D + "HOME")
case("wsl without -c", False,
     "wsl -d Gentoo -- ls " + D + "PWD")
case("literal paths only", False,
     "wsl -d Gentoo -- bash -c " + Q + "cmp -s /tmp/a /mnt/c/b" + Q)

# *** THE TWO FALSE POSITIVES THAT DROVE LINE-SCOPING. ***  Both are prose or
# data MENTIONING the pattern; neither runs wsl.  A guard that blocks people
# writing ABOUT the defect is one that gets switched off.
case("FP1: pattern as DATA in a heredoc", False,
     "python - <<" + Q + "PYEOF" + Q + NL +
     "CASES = [" + NL +
     "  " + Q + "wsl -d Gentoo -- bash -c " + chr(34) + "echo " + D + "S" + chr(34) + Q + "," + NL +
     "]" + NL +
     "PYEOF")
case("FP2: pattern in heredoc COMMENTS", False,
     "cat > check.py <<" + Q + "EOF" + Q + NL +
     "#  Flags `wsl ... -c` calls that carry a bare " + D + "VAR." + NL +
     "#  The safe form is wsl -- bash -c " + Q + "echo " + D + "X" + Q + " escaped." + NL +
     "import re" + NL +
     "EOF")
case("FP3: a shell COMMENT line", False,
     "# wsl -d Gentoo -- bash -c " + Q + "echo " + D + "X" + Q + NL +
     "echo hello")


def run(cmd):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})
    p = subprocess.run([sys.executable, HOOK], input=payload,
                       capture_output=True, text=True)
    return p.returncode != 0 or bool(p.stderr.strip())


def main():
    L = []
    ok = bad = 0
    L.append("  %-40s %-10s %-10s %s" % ("control", "want", "got", "verdict"))
    L.append("  " + "-" * 74)
    for name, must_fire, cmd in CASES:
        got = run(cmd)
        good = (got == must_fire)
        if good:
            ok += 1
        else:
            bad += 1
        L.append("  %-40s %-10s %-10s %s" % (
            name[:40],
            "FIRE" if must_fire else "silent",
            "FIRE" if got else "silent",
            "ok" if good else "*** WRONG ***"))
    L.append("")
    L.append("  %d of %d controls pass, %d wrong" % (ok, ok + bad, bad))
    L.append("")
    L.append("  denominator: %d rows -- %d must FIRE, %d must stay SILENT"
             % (len(CASES),
                sum(1 for c in CASES if c[1]),
                sum(1 for c in CASES if not c[1])))
    L.append("")
    L.append("HOOKCTL_DONE")
    out = NL.join(L)
    io.open(sys.argv[1] if len(sys.argv) > 1 else "hookctl.out",
            "w", encoding="utf-8", newline=NL).write(out + NL)
    print(out)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
