"""CONTROLS for the 2026-08-30 wsl-dollar-guard fix: combined short-flag clusters.

WHY IT EXISTS.  The guard's DASH_C was `\\s-c\\b|\\s--command\\b`, which requires a
BARE -c.  A real invocation used `wsl -d Gentoo -- bash -lc '...'` -- a combined
short-flag cluster, idiomatic bash -- and the guard did not fire.  Every $VAR was
stripped, a probe was handed nonexistent binaries, and it printed a full table of
`??` under a VERDICT line reading "declined" on both legs.  A FALSE PASS.

CONTROLLED IN BOTH DIRECTIONS, because a guard that blocks legitimate commands gets
switched off, which is worse than a guard with a gap.  The negative cases are the
point of this file, not padding:

  * `-exec` must NOT fire -- a bare `-[a-z]*c` pattern would have matched it, which
    is why the new alternative is anchored to a shell name.
  * the two measured-safe forms (escaped dollar, script file) must still pass.
  * `$(...)` stays exempt: it is a deliberate outer-shell substitution.

    python3 clusterctl.py            # exit 0 iff every case behaves
"""
import json
import os
import subprocess
import sys

NL = chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "..", "tools", "hooks", "wsl_dollar_guard.py"))

#  (name, must_fire, command)
CASES = [
    #  ---- THE REGRESSION THAT PROMPTED THE FIX ------------------------------
    ("cluster -lc, bare dollar          THE MEASURED MISS", True,
     "MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash -lc 'O=/tmp/gx; echo $O/sig'"),
    ("cluster -ic, bare dollar", True,
     "wsl -d Gentoo -- bash -ic 'echo $HOME'"),
    ("cluster -lc spanning newlines", True,
     "wsl -d Gentoo -- bash -lc '" + NL + "X=1" + NL + "echo $X" + NL + "'"),

    #  ---- THE ORIGINAL SHAPES MUST STILL FIRE -------------------------------
    ("bare -c, bare dollar", True,
     "wsl -d Gentoo -- bash -c 'echo $X'"),
    ("--command, bare dollar", True,
     "wsl --command 'echo $X'"),

    #  ---- NEGATIVE CONTROLS.  THESE ARE THE POINT. --------------------------
    ("find -exec inside a wsl segment   MUST NOT FIRE", False,
     "wsl -d Gentoo -- bash /mnt/c/run.sh && find . -exec grep '$X' {} ;"),
    ("script FILE, the safe form", False,
     "MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/x.sh"),
    ("cluster -lc with the dollar ESCAPED", False,
     "wsl -d Gentoo -- bash -lc 'false; echo " + chr(92) + "$?'"),
    ("cluster -lc with no dollar at all", False,
     "wsl -d Gentoo -- bash -lc 'echo hello'"),
    ("$(...) is a deliberate outer substitution", False,
     "wsl -d Gentoo -- bash -lc 'echo $(date)'"),
    ("no wsl anywhere", False,
     "bash -lc 'O=/tmp; echo $O'"),
]


def fires(cmd):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})
    p = subprocess.run([sys.executable, HOOK], input=payload,
                       capture_output=True, text=True)
    return p.returncode != 0


def main():
    print("=" * 86)
    print("wsl dollar guard -- CLUSTER controls (2026-08-30)")
    print("=" * 86)
    print("hook  %s" % HOOK)
    print("")
    bad = 0
    for name, must, cmd in CASES:
        got = fires(cmd)
        ok = (got == must)
        bad += 0 if ok else 1
        print("  %-4s %-42s want %-5s got %-5s" %
              ("ok" if ok else "FAIL", name,
               "FIRE" if must else "pass", "FIRE" if got else "pass"))
    print("")
    print("  %d cases: %d must fire, %d must pass" %
          (len(CASES), sum(1 for c in CASES if c[1]),
           sum(1 for c in CASES if not c[1])))
    print("")
    if bad:
        print("CLUSTERCTL_FAIL  %d case(s) wrong" % bad)
        return 1
    print("CLUSTERCTL_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
