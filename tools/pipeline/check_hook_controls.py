#!/usr/bin/env python3
#
#  CHECK: the wsl-dollar PreToolUse guard still behaves as specified.
#
#  WHY THIS EXISTS, and it is a measurement rather than a worry.
#  ---------------------------------------------------------------------------
#  The guard fires on EVERY Bash call, and it shipped on 2026-08-29 with FOUR
#  defects that nobody noticed for hours:
#
#    * 2 FALSE NEGATIVES -- a multi-line `bash -c '...'` block whose bare dollar
#      sits on a LATER LINE than the -c.  That is the shape that actually bites.
#      It ran that day, through the guard, and lost both its variables: a `cmp`
#      reported DIVERGED on a byte-identical file, and gcc reported
#      file-not-found.  TWO confident wrong answers from one stripped variable,
#      and the guard built for exactly this was silent.
#
#    * 2 FALSE POSITIVES that the then-current LINE-SCOPING had been adopted to
#      fix AND NEVER FIXED.  A control of the very shape its own comment cited
#      as motivating -- a heredoc whose COMMENTS mention `wsl ... -c` -- still
#      fired.  Line-scoping killed two INSTANCES, not the CLASS, because those
#      two happened to split across lines.
#
#  It scored 14/18.  The rescoped form scores 18/18.
#
#  WHY tools/ AND NOT A regress/ GATE.  Owner decision 2026-08-29.  This tests a
#  Claude-Code hook, not the emulator, so an emulator gate running it would be a
#  category mixture -- and the battery's gates are the wrong cadence for a file
#  that is edited interactively.
#
#  *** THIS FILE IS THE AUTHORITATIVE SUITE, NOT A COPY OF ONE. ***  The
#  artifact at regress/artifacts/makercfalse/hook_controls_20260829/ is this
#  suite's PRESERVED OUTPUT plus the before/after pair, which is evidence.
#  Keeping a second executable copy would recreate exactly the divergence
#  problem the hook's own tracked-path fix was landed to remove.
#
#  A SUITE THAT ONLY PROVES THE GUARD FIRES IS HALF A SUITE.  Nine rows must
#  FIRE and nine must stay SILENT; the silent half is where the false positives
#  live, and a false positive is what gets a guard switched off.
#
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
#  tools/pipeline/ -> tools/ -> hooks/
HOOK = os.path.join(HERE, os.pardir, "hooks", "wsl_dollar_guard.py")

Q = chr(39)
D = chr(36)
NL = chr(10)

CASES = []


def case(name, must_fire, cmd):
    CASES.append((name, must_fire, cmd))


# ------------------------------------------------------------ MUST FIRE (9)
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
#  The measured false negative: the dollar is BELOW the -c.
case("MULTI-LINE, dollar on later line", True,
     "wsl -d Gentoo -- bash -c " + Q + NL +
     "S=/mnt/c/x" + NL +
     "cmp -s /tmp/a " + D + "S/b" + NL + Q)
case("MULTI-LINE, dollar 6 lines down", True,
     "MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash -c " + Q + NL +
     "set -u" + NL + "A=1" + NL + "B=2" + NL + "echo hi" + NL +
     "echo " + D + "A" + NL + Q)

# ---------------------------------------------------------- MUST STAY SILENT (9)
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
#  Prose and data MENTIONING the pattern.  Neither runs wsl.
case("FP1: pattern as DATA in a heredoc", False,
     "python - <<" + Q + "PYEOF" + Q + NL +
     "CASES = [" + NL +
     "  " + Q + "wsl -d Gentoo -- bash -c " + chr(34) + "echo " + D + "S" +
     chr(34) + Q + "," + NL +
     "]" + NL +
     "PYEOF")
case("FP2: pattern in heredoc COMMENTS", False,
     "cat > check.py <<" + Q + "EOF" + Q + NL +
     "#  Flags `wsl ... -c` calls that carry a bare " + D + "VAR." + NL +
     "#  The safe form is wsl -- bash -c " + Q + "echo " + D + "X" + Q +
     " escaped." + NL +
     "import re" + NL +
     "EOF")
case("FP3: a shell COMMENT line", False,
     "# wsl -d Gentoo -- bash -c " + Q + "echo " + D + "X" + Q + NL +
     "echo hello")


def fired(cmd):
    """True when the guard BLOCKS this command."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})
    p = subprocess.run([sys.executable, HOOK], input=payload,
                       capture_output=True, text=True)
    return p.returncode != 0 or bool(p.stderr.strip())


def main():
    if not os.path.isfile(HOOK):
        #  Not a failure of the guard's BEHAVIOUR -- say which it is.
        print("  note  HOOK ABSENT at %s -- nothing to check" % HOOK)
        print("HOOKCTL_SKIP")
        return 0

    #  A syntax error here would make every row "fire" and read as 9 failures
    #  in the silent half.  Name the real cause instead: this exact state
    #  happened on 2026-08-29 and a fail-safe try/except CANNOT catch it,
    #  because the file never parses.
    src = io.open(HOOK, encoding="utf-8").read()
    try:
        compile(src, HOOK, "exec")
    except SyntaxError as e:
        print("  FAIL  THE GUARD DOES NOT PARSE: %s line %s" % (e.msg, e.lineno))
        print("        Every Bash call in a live session gets a traceback, and")
        print("        the guard's own try/except cannot catch this.")
        print("HOOKCTL_FAIL  1 problem")
        return 1

    bad = []
    for name, must_fire, cmd in CASES:
        got = fired(cmd)
        if got != must_fire:
            bad.append((name, must_fire, got))

    nfire = sum(1 for c in CASES if c[1])
    if bad:
        for name, want, got in bad:
            print("  FAIL  %-38s want=%s got=%s"
                  % (name, "FIRE" if want else "silent",
                     "FIRE" if got else "silent"))
        print("HOOKCTL_FAIL  %d of %d controls wrong (%d must FIRE, %d must stay "
              "SILENT)" % (len(bad), len(CASES), nfire, len(CASES) - nfire))
        return 1

    print("  ok    wsl-dollar guard: %d/%d controls (%d FIRE, %d SILENT)"
          % (len(CASES), len(CASES), nfire, len(CASES) - nfire))
    print("HOOKCTL_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
