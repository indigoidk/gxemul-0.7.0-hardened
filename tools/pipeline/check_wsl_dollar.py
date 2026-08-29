#!/usr/bin/env python3
#
#  RATCHET: no tracked script may invoke `wsl ... -c` with a BARE dollar in the
#  command string.
#
#  THE DEFECT.  Measured 2026-08-29, artifact
#  regress/artifacts/makercfalse/wsl_dollar_20260829.out (sections A-F):
#
#      bash -c 'false; echo $?'             -> 1     ordinary, local
#      wsl -- bash -c 'false; echo $?'      -> 0     THE DEFECT
#      wsl -- bash -c 'X=hello; echo [$X]'  -> []    set and used in ONE command
#      wsl -- bash -c 'echo "a  b"'         -> a  b  quoting DOES survive
#
#  SINGLE QUOTES DO NOT PROTECT.  A mutant that is never applied then scores the
#  BASE binary and reports a clean kill table.
#
#  *** STATE ITS RECALL HONESTLY, BECAUSE THAT IS WHAT DECIDED ITS SHAPE. ***
#
#  RECALL ON THE RECORDED HISTORY IS **ZERO**.  The class has bitten five times
#  (nightly_battery.sh's header 2026-08-17; af4884c 2026-08-20; CHANGELOG
#  #477-era; asanbaselinedrift 2026-08-28; and once more the same hour the fifth
#  was written up) and EVERY occurrence was an interactive, ad-hoc command.  A
#  census of the committed tree finds the form four times and ALL FOUR ARE
#  QUOTATIONS OF THE DEFECT in prose.  So this check would have caught none of
#  them.
#
#  It is therefore NOT the primary defence and must not be read as one.  The
#  primary defence is the PreToolUse hook at .claude/hooks/wsl_dollar_guard.py,
#  which fires at the surface where all five actually happened.  THIS check
#  exists for the one thing the hook cannot do: stop the form from being
#  COMMITTED into a script, where it would then run unattended forever.
#
#  ZERO-POPULATION RATCHET.  Measured 2026-08-29: 229 tracked .sh/.py files, 4
#  mention wsl, and NONE carries this form on a non-comment line.  So it
#  grandfathers nothing and needs no dated cutoff -- it fails on the first
#  violation.  If that population is ever non-zero at introduction, convert it to
#  the dated-cutoff shape check_bugfile_sync.py uses rather than retro-failing
#  work nobody scheduled: a rule that blocks the next commit on reconstruction
#  gets switched off, which is worse than a rule that warns.
#
#  WHAT IT PRINTS WHEN THE THING IS FALSE: a file list and exit 1.  When true:
#  one line naming the DENOMINATOR.  A run that scanned zero files reports that
#  as a failure, because a pattern selecting nothing reports 0 for everything.
#
import os
import re
import subprocess
import sys

#  `$(` is a DELIBERATE outer-shell substitution and is exempt; `\$` is the
#  measured-safe escaped form.  A bare `$` before a name, brace or `?` is the
#  hazard.
BARE_DOLLAR = re.compile(r'(?<!\\)\$(?!\()[A-Za-z_?{]')
WSL_CALL = re.compile(r'(?:^|[|;&]|\s)wsl(?:\.exe)?\b')
DASH_C = re.compile(r'\s-c\b|\s--command\b')


def tracked(sec):
    out = subprocess.run(["git", "-C", sec, "ls-files", "--", "*.sh", "*.py"],
                         capture_output=True, text=True)
    return [p for p in out.stdout.splitlines() if p.strip()]


def offending(line):
    s = line.strip()
    if s.startswith("#"):
        return False
    if not WSL_CALL.search(line):
        return False
    m = DASH_C.search(line)
    if not m:
        return False
    return bool(BARE_DOLLAR.search(line[m.end():]))


def main():
    sec = sys.argv[1] if len(sys.argv) > 1 else "."
    files = tracked(sec)
    hits = []
    scanned = 0
    for rel in files:
        p = os.path.join(sec, rel)
        if not os.path.isfile(p):
            continue
        scanned += 1
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    if offending(line):
                        hits.append((rel, n, line.strip()[:100]))
        except OSError:
            continue

    if scanned == 0:
        print("  WSL_DOLLAR_SCANNED_ZERO -- ls-files selected nothing, so this "
              "proved nothing")
        return 1
    if hits:
        for rel, n, txt in hits:
            print("  %s:%d carries `wsl ... -c` with a bare dollar" % (rel, n))
            print("      %s" % txt)
        print("  Use the escaped form (\\$) or run a SCRIPT FILE.  See "
              "regress/artifacts/makercfalse/wsl_dollar_20260829.out")
        return 1
    print("  WSL_DOLLAR_PASS  no tracked script carries `wsl ... -c` with a bare "
          "dollar (%d scanned)" % scanned)
    return 0


if __name__ == "__main__":
    sys.exit(main())
