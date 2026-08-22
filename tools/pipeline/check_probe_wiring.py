#!/usr/bin/env python3
"""Every committed DETECTOR under regress/ is RUN by a gate, or carries a dated exemption.

*** SIXTY-SIX DETECTOR ROWS DEFENDED NOTHING BETWEEN BATTERIES, AND NO GATE, CHECK OR
    LEDGER FIELD COULD SAY SO. ***  Named by a batched flagship regress pass on 2026-08-21,
    which sorted every detector escape in this project into three shapes and found that two
    had mechanical guards and the third -- "nobody runs it" -- had none.  Its own census said
    24 rows across two rounds.  MEASURED at HEAD 3d752b4 it is FOUR rounds and 66:

        pit8253_latch_probe.py   #439/#440   18 rows   run by NO gate
        sh4_bsc_width_probe.py   #441        13 rows   run by NO gate
        fbpending_drain_probe.py #442        11 rows, REPORT-ONLY by default (EXPECT_CAP<0)
        hpcmips_ctor_probe.py    #444        24 rows   run by NO gate  (+4 emitted in loops;
                                            its round's own record audits 26 emitted rows)

    THE MEASURE IS NAMED BECAUSE THE FIRST ONE WAS WRONG.  These are `row()` CALL SITES WITH
    A LITERAL LABEL, counted through `ast`, not grepped.  A first pass used `grep -o 'row("R'`
    and reported 12/11/7/26 = 56 -- it silently dropped every control row that is not
    R-prefixed (pit8253's A1 A2 C1 C2 E T, fbpending's K P T).  Same shape as the padded-column
    grep trap: a number that looks right and counts the wrong set.  A count nobody can re-derive
    is not a fact, which is what run.sh's own GATE_MANIFEST comment says.  Re-derive with:
        python -c "import ast,io;t=ast.parse(io.open(F).read());print(sum(1 for n in ast.walk(t)
        if isinstance(n,ast.Call) and getattr(n.func,'id','')=='row'))"

WHY THE EXISTING GUARDS DO NOT COVER THIS.  gate_hygiene's EXPECT_CONVERTED pin is a CENSUS
PIN: it asserts that a new probe carries the three #392 pty constructs and that the count
moved.  It is a good guard and it has fired four times -- but its subject is the probe's
SOURCE TEXT, never its EXECUTION.  All four files above satisfy that pin today.  The pin says
"this probe is well formed"; nothing said "this probe runs".

THE TWO TRAPS THIS INHERITS FROM gate_offline.sh's SM_COVERED/SC_COVERED, both re-read before
a line of this was written:

  1. A PREFIX IS NOT A NAME.  SM_COVERED's loop compares whole stems ([ "$_c" = "$stem" ])
     precisely because a substring match would accept a stem that is merely a prefix of
     another.  Hours before this file was written, check_fable_queue.py matched round ids by
     SUBSTRING and reported a round as queued when the only occurrence was a parenthetical
     cross-reference.  So this file matches FULL BASENAMES, and it decides "is it run?" from
     COMMAND POSITION rather than from a name appearing somewhere on a line.
     THE LIVE INSTANCE, not a hypothetical: gate_sh_rounding.sh:185 and eight lines of
     gate_hygiene.sh MENTION the unwired probes -- one of them in order to COMPLAIN that they
     are unwired.  A grep-for-the-name check scores all four WIRED and prints green over the
     entire defect it exists to catch.

  2. THE MANIFEST MUST NOT VERIFY THE LEDGER INSTEAD OF THE WORK.  gate_offline's F3 note
     records a pass-2 seat measuring BOTH directions green: delete a selfmutant_one call and
     leave SM_COVERED intact -> GREEN.  The structural answer here is that THERE IS NO
     COVERED LIST.  The manifest below carries ONLY the one fact a machine cannot derive --
     what CLASS an artefact is -- and the wiring is DERIVED, every run, from the gate scripts
     named in run.sh's GATES array.  The manifest cannot lie about wiring because it never
     states it, and the derivation PRINTS ITS EVIDENCE (gate_arm.sh:97) so the derivation is
     auditable rather than trusted.

WITNESS vs DETECTOR -- THE LINE, AND WHY IT IS NOT SYNTACTIC.

    A DETECTOR asserts the REPAIRED property: it is GREEN once the defect is gone.
    A WITNESS   asserts the PRE-FIX SYMPTOM:  it is RED   once the defect is gone.

That is sharp, but no grep can evaluate it.  MEASURED, so this is not a preference:

  * pit8253_latch_probe.py opens "Rung-3 cold-debugger WITNESS for pitlatch / pitclobber"
    -- and its rows assert the FIXED behaviour ("R1/R2 fail on the PRE-FIX build"), so by the
    line above it is a DETECTOR.  A self-label grep classifies it wrongly and, worse, then
    stops asking for a gate.
  * hpcmips_ctor_probe.py and sh4_bsc_width_probe.py are DETECTORS whose docstrings both say
    "The pre-fix WITNESS ... asserts the SYMPTOM" in prose.  A self-label grep classifies
    BOTH as witnesses -- and would then demand they never be gated, which is backwards.

So the class is DECLARED here, by a human, one line each.  The file's own summary line is
cross-checked as an ADVISORY (SELFLABEL), never as a failure, for the measured reason above.

WHY GATING A WITNESS IS A FAILURE, not merely pointless -- the tooth in the other direction,
which the reading seat's recommendation did not name.  A witness goes RED the day its fix
lands.  Wiring one into the battery converts a successful repair into a red gate with a
bookkeeping cause: the phantom-regression class this project already names, manufactured on
purpose.  So witness entries are checked for the ABSENCE of a gate call.

RETROACTIVE IN DOMAIN, GREEN AT INTRODUCTION.  check_boilerplate.py and check_bugfile_sync.py
are forward-only BY DATE because retro-failing an archive of hundreds of ledger rows gets the
rule switched off, and a disabled rule is worse than no rule.  That argument does not carry
here: the domain is a few dozen files in ONE FLAT DIRECTORY, enumerable in full today, and an
unwired probe has no date to be forward-only about.  A date cutoff would also grandfather the
four files this check exists for, permanently.  So nothing is grandfathered -- and the check is
still green on the day it lands, because each existing gap is written down as a DATED
EXEMPTION naming the round that owes it.  Debt that expires, not debt that disappears.

DATES ARE VALIDATED, NEVER GUESSED.  gate_offline.sh records a malformed exemption date that
never expired AND still satisfied the coverage check ("ieee_store:2026-8-1", 19 days past,
sorted as FUTURE).  Here a missing or malformed date is RED and names itself; it is never
silently treated as unexpired.

WHAT THIS CANNOT DO, said plainly so a green line is not read as more than it is:
  * it cannot tell whether a gated probe's rows are any good.  gate_offline's selfmutant lane
    and the vacuity taxonomy are what answer that; this answers only "does anything run it".
  * it cannot stop a DETECTOR being misfiled as tool to silence the requirement.  The
    filename tooth below refuses *_probe.py/*_witness.py in that class, which closes the
    cheapest form; a rename defeats it.  What is left is a written lie in a tracked file, and
    that is the same footing every manifest in this harness stands on.  Said, not hidden.

*** --selftest IS PART OF THE CHECK, NOT A CONVENIENCE. ***  A gate that cannot be shown to
go RED is the vacuity class this project names first, and "I ran the mutants once" is a
remembered grep -- the mrwstore2 shape, where a round's witness left no artefact and a later
row had to re-cost the work.  `--selftest` applies 18 mutants to COPIES in a temp directory
(never the repo) and asserts the exit status of each.  It is re-runnable by someone who was
not there, which is the only kind of measurement that survives.

Usage:  python check_probe_wiring.py [-v] [--regress DIR] [--today YYYY-MM-DD]
        python check_probe_wiring.py --selftest [-v]
Exit 0 and print PROBEWIRING_PASS, or exit 1 and print PROBEWIRING_FAIL.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REGRESS = os.path.normpath(os.path.join(HERE, "..", "..", "regress"))

#  Scripts that are part of the battery but are not in the GATES array: run.sh drives it and
#  lib.sh is sourced by every gate, so an invocation placed in either really would run.
ALWAYS = ("run.sh", "lib.sh")

#  A script argument is only a REPO probe if its directory is the regress dir.  gate_offline
#  runs `python3 "$ACDIR/selftest_absorb.py"` on a MUTATED COPY in the log dir -- counting
#  that as "the repo file is gated" would be the absorb-control mutant vouching for the
#  artefact it was built to attack.  Anything else is reported under IGNORED rather than
#  dropped, so a legitimate new spelling shows up as a line to read instead of a silent red.
HERE_DIRS = ("", ".", "$HERE", "${HERE}")

CLASS_DETECTOR = "detector"
CLASS_WITNESS = "witness"
CLASS_TOOL = "tool"
CLASSES = (CLASS_DETECTOR, CLASS_WITNESS, CLASS_TOOL)

#  ---------------------------------------------------------------------------------------
#  THE MANIFEST.  One line per python artefact in regress/.  The CLASS is the only thing a
#  machine cannot derive; the wiring is derived below and printed with its file:line.
#
#  Adding a probe means adding a line here, deliberately -- the same idiom as run.sh's
#  GATE_MANIFEST and gate_offline's SM_COVERED.  An unlisted file is RED, so a new detector
#  cannot arrive unnoticed, which is exactly how all four debts below arrived.
MANIFEST = {
    # -- detectors a gate RUNS today (the evidence is derived, not asserted here) ---------
    "arm_endian_probe.py":         (CLASS_DETECTOR, "ARM LDR rotation / endianness"),
    "arm_flags_probe.py":          (CLASS_DETECTOR, "ARM flag semantics"),
    "arm_fold_marker_probe.py":    (CLASS_DETECTOR, "instruction-combination markers"),
    "arm_idle_probe.py":           (CLASS_DETECTOR, "ARM idle detection"),
    "arm_memcpy_probe.py":         (CLASS_DETECTOR, "memcpy fold"),
    "arm_strlen_probe.py":         (CLASS_DETECTOR, "strlen fold"),
    "arm_writeback_probe.py":      (CLASS_DETECTOR, "LDR/STR writeback"),
    "diag_div_sweep.py":           (CLASS_DETECTOR, "class ratchet: drivable divisions"),
    "footbridge_sites_probe.py":   (CLASS_DETECTOR, "footbridge reachability sites"),
    "luna_intmask_probe.py":       (CLASS_DETECTOR, "#438 luna88k interrupt mask"),
    "m8820x_sites_probe.py":       (CLASS_DETECTOR, "m8820x CMMU sites"),
    "m88k_idle_probe.py":          (CLASS_DETECTOR, "m88k idle detection"),
    "m88k_rounding_probe.py":      (CLASS_DETECTOR, "m88k FP rounding"),
    "mips_fixedmode_probe.py":     (CLASS_DETECTOR, "MIPS FS / fixed mode"),
    "mips_fold_probe.py":          (CLASS_DETECTOR, "MIPS instruction folds"),
    "mips_rounding_probe.py":      (CLASS_DETECTOR, "MIPS FP rounding"),
    "mips_subnorm_probe.py":       (CLASS_DETECTOR, "MIPS subnormal decode/encode"),
    "ppc_halt_probe.py":           (CLASS_DETECTOR, "PPC halt path"),
    "ppc_rounding_probe.py":       (CLASS_DETECTOR, "PPC FP rounding"),
    "readiness_predicate_test.py": (CLASS_DETECTOR, "#392 readiness truth table"),
    "selftest_absorb.py":          (CLASS_DETECTOR, "drive_guest.split_stream selftest"),
    "selftest_budget.py":          (CLASS_DETECTOR, "wall-clock budget selftest"),
    "selftest_logdir.py":          (CLASS_DETECTOR, "#422 $LOGDIR honouring selftest"),
    #  CLASSIFIED WHILE ITS OWN ROUND WAS STILL IN THE INDEX, and that is the check working
    #  rather than an exception to it: this file was `git add`ed by a concurrent #446 round
    #  MINUTES after this checker was written, went straight into the domain, and was named
    #  UNCLASSIFIED on the first run.  Reading it settled both questions in under a minute --
    #  its own first line says "#446 DETECTOR", and gate_offline.sh:1815 really does run it,
    #  so it needs no exemption.  #446 wired its probe in the same commit as its fix.
    "sgi_eaddr_probe.py":          (CLASS_DETECTOR, "#446 SGI eaddr value oracle at arcbios_init"),
    "sh4_pcic_probe.py":           (CLASS_DETECTOR, "#443 sh4 PCIC exit sites"),
    "sh4_chcr_probe.py":           (CLASS_DETECTOR, "#448 sh4 CHCR field decoders"),
    "sh4_chcr_witness.py":         (CLASS_WITNESS,  "#448 pre-fix symptom: TD=1 ends the host"),
    "sh4_val_probe.py":            (CLASS_DETECTOR, "#447 sh4 DEVICE_ACCESS value guards"),
    "sh4_val_witness.py":          (CLASS_WITNESS,  "#447 pre-fix symptom: the host dies"),
    "sh_halt_probe.py":            (CLASS_DETECTOR, "SH halt path"),
    "sh_rounding_probe.py":        (CLASS_DETECTOR, "SH FP rounding"),

    # -- detectors that NOTHING RUNS.  Each carries a dated exemption below. --------------
    #  pit8253's docstring line 1 calls it a "witness"; its rows assert the FIXED behaviour
    #  ("R1/R2 fail on the PRE-FIX build"), so by the green-once-fixed line it is a DETECTOR.
    #  This is the measured case that rules out classifying by self-label.
    "pit8253_latch_probe.py":      (CLASS_DETECTOR, "#439/#440 PIT latch + LSB/MSB selector"),
    "sh4_bsc_width_probe.py":      (CLASS_DETECTOR, "#441 BCR2/BCR3 non-16-bit access"),
    "fbpending_drain_probe.py":    (CLASS_DETECTOR, "#442 footbridge pending-tick backlog"),
    "hpcmips_ctor_probe.py":       (CLASS_DETECTOR, "#444 every hpcmips subtype constructs"),

    # -- witnesses.  RED once the fix lands, so gating one manufactures a regression. -----
    "fbpending_witness.py":        (CLASS_WITNESS, "#442 pre-fix: the clock stops 42.9s in 85.9s"),
    "hpcabort_witness.py":         (CLASS_WITNESS, "#444 pre-fix: 3 of 8 subtypes SIGABRT"),
    "sh4pcic_witness.py":          (CLASS_WITNESS, "#443 pre-fix: guest loads end the host"),

    # -- tools: apparatus and libraries, not assertions about the emulator ----------------
    "drive_guest.py":              (CLASS_TOOL, "the pty driver library every rig probe imports"),
    "selfmutant.py":               (CLASS_TOOL, "differential mutation harness; gate 2 drives it"),
    "absorb_census.py":            (CLASS_TOOL,
                                    "measures selftest_absorb.py's KILL RATE by hand over 22 "
                                    "rebuilt mutants. The gated artefact is selftest_absorb.py; "
                                    "this grades that detector and is not one itself."),
}

#  DATED, NAMED DEBT -- not a count and not a silent allowlist.  gate_offline.sh MEASURED that
#  a COUNT pin actively obstructs the shrink it claims to want ("6, shrinking not growing" went
#  RED at 5).  A date expires; shrinking is green by construction.
#
#  2026-09-20 matches the fbpending_bound:2026-09-20 deadline already standing in
#  gate_offline.sh's SM_EXEMPT, so #442's two debts fall due together.  IT IS A PROPOSAL: the
#  owner set the SM dates and set them TIGHTER than the ones proposed, and a deadline nobody
#  chose is a deadline nobody owns.
#
#  These are wiring jobs, not design ones -- each probe already prints a verdict token and
#  exits nonzero on failure.  What each needs is a gate that owns it, its rig preconditions,
#  and ONE clean gate run proving it green before it ships.  That last part is why they are
#  exempted here rather than wired here: gate_hygiene's own comments record FOUR probes that
#  shipped latently RED because the commit that added them never fired the gate.
EXEMPT = {
    "pit8253_latch_probe.py":   ("2026-09-20", "wants gate 14 (gate_arm; -E cats + STUB)"),
    "sh4_bsc_width_probe.py":   ("2026-09-20", "wants gate 10 (gate_sh_rounding; -E landisk)"),
    "fbpending_drain_probe.py": ("2026-09-20",
                                 "REPORT-ONLY by default: EXPECT_CAP must be set before a "
                                 "gate row can mean anything, so wiring is a design step first"),
    "hpcmips_ctor_probe.py":    ("2026-09-20",
                                 "rung 2, ~8 s, no rig image -- wants a construction gate"),
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


#  *** A PYTHON DICT LITERAL ACCEPTS A DUPLICATE KEY IN SILENCE, AND THE LAST ONE WINS.
#  MEASURED ON THIS FILE, HOURS AFTER IT WAS WRITTEN. ***
#
#  Two rounds added `sgi_eaddr_probe.py` to MANIFEST independently -- the author of this
#  checker, and the #446 round whose probe it was.  Both landed, four lines apart, and
#  `len(MANIFEST)` reported ONE entry.  Nothing complained, because nothing can: by the
#  time the module object exists the earlier entry is already gone.  Here the two agreed
#  on CLASS, so the behaviour was identical and the only damage was a stale line.  Had
#  they disagreed -- one DETECTOR, one TOOL -- the file would have carried a visible,
#  reviewed, *tracked* classification that the checker silently did not use, and the
#  filename tooth that refuses `*_probe.py` in class `tool` would have been reading the
#  wrong entry while looking correct in the diff.
#
#  It has to be caught by re-reading THIS FILE'S SOURCE TEXT, because the data structure
#  cannot represent the fault it suffers from.  A duplicate is a SETUP FAULT, not a
#  finding: it exits before any wiring is derived, so it can never be confused with a
#  probe that is genuinely unwired.
#  The open() is INLINE rather than a call to read() below: this guard runs at import time,
#  fifty lines before read() is defined, and the first draft died with a NameError proving it.
#  It failed loudly, which is luck -- a guard placed in a branch would have failed silently.
def _refuse_duplicate_keys():
    with open(os.path.abspath(__file__), "r", encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    for name, start in (("MANIFEST", "MANIFEST = {"), ("EXEMPT", "EXEMPT = {")):
        i = src.find(start)
        if i < 0:
            continue
        j = src.find("\n}", i)
        seen, dupes = set(), []
        for k in re.findall(r'^\s*"([^"]+)"\s*:', src[i:j], re.M):
            (dupes.append(k) if k in seen else None)
            seen.add(k)
        if dupes:
            print("PROBEWIRING_SETUP_FAULT  %s names the same key twice; a dict literal" % name)
            print("  keeps only the LAST and says nothing.  Delete the stale line(s):")
            for k in sorted(set(dupes)):
                print("    %s" % k)
            sys.exit(2)


_refuse_duplicate_keys()

#  A python interpreter token.  Bare python/python3, or the $PY-style indirections other
#  harnesses in this tree use.  Anchored so python3.12 and mypython do not match.
INTERP_RE = re.compile(
    r'"?\$\{?(?:PY|PY3|PYTHON|PYTHON3)\}?"?'
    r'|(?<![\w./-])python3?(?![\w.-])'
)

#  COMMAND POSITION -- the whole defence against "a mention counts as wiring".  Everything
#  before the interpreter must be shell scaffolding: leading space, an assignment opening a
#  command substitution (out=$( ), control keywords, and environment-variable prefixes.
#
#  THE LINE THIS WAS BUILT AGAINST IS REAL AND LIVE, not invented:
#      gate_hygiene.sh:331   note "diag_div_sweep.py or python3 missing -- class ratchet NOT run"
#  It carries a probe basename AND the token python3 on one non-comment line, and it is a
#  message saying the probe DID NOT RUN.  A two-sided "name near python" regex scores it as
#  execution.  Here the interpreter's prefix is `note "diag_div_sweep.py or `, which is not
#  scaffolding, so the line is rejected.
CMDPOS_RE = re.compile(
    r"""^\s*
        (?: [A-Za-z_]\w* = (?:\$\()? \s* )?
        (?: (?: if | then | else | elif | while | until | do | ! | \$\( | \( ) \s* )*
        (?: [A-Za-z_]\w* = (?: "[^"]*" | '[^']*' | \S* ) \s+ )*
        $""",
    re.X,
)

VAR_RE = re.compile(r"^\$\{?([A-Za-z_]\w*)\}?$")
ASSIGN_RE = re.compile(r"^\s*([A-Za-z_]\w*)=(\S+)")


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def unquote(tok):
    tok = tok.strip().rstrip(");,")
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        tok = tok[1:-1]
    return tok.strip("\"'")


def gate_list(regress):
    """The battery's OWN array is the authority on which scripts run.

    Deriving from run.sh rather than from a gate_*.sh glob is deliberate, and carries a
    second-order property worth having: a gate script that exists but was dropped out of
    GATES does not run, so every probe it owned becomes unwired here and this goes RED.
    A glob would have called those probes gated forever.
    """
    run = os.path.join(regress, "run.sh")
    if not os.path.isfile(run):
        return None, "regress/run.sh is missing -- cannot tell which gates run"
    m = re.search(r"^GATES=\(([^)]*)\)", read(run), re.M)
    if not m:
        return None, "regress/run.sh has no GATES=( ... ) array -- cannot derive the battery"
    return [n + ".sh" for n in m.group(1).split()], None


def exec_sites(regress, scripts):
    """Return (hits, ignored, missing).

    hits[basename] = ["gate_arm.sh:97", ...]  -- a real invocation of the regress copy
    ignored        = ["gate_offline.sh:153  $ACDIR/selftest_absorb.py", ...]
    """
    hits, ignored, missing = {}, [], []
    for script in scripts:
        path = os.path.join(regress, script)
        if not os.path.isfile(path):
            missing.append(script)
            continue
        lines = read(path).splitlines()
        #  One-level variable map, from this file only.  gate_hygiene really does write
        #  DIVSWEEP=$HERE/diag_div_sweep.py and then run "$DIVSWEEP", so refusing to resolve
        #  one level would report a genuinely gated probe as unwired -- and a false red is
        #  how a rule gets switched off.
        varmap = {}
        for ln in lines:
            if ln.lstrip().startswith("#"):
                continue
            a = ASSIGN_RE.match(ln)
            if a and ".py" in a.group(2):
                varmap[a.group(1)] = unquote(a.group(2))
        for no, ln in enumerate(lines, 1):
            if ln.lstrip().startswith("#"):
                continue
            for m in INTERP_RE.finditer(ln):
                if not CMDPOS_RE.match(ln[: m.start()]):
                    continue
                toks = ln[m.end():].split()
                if toks and toks[0].startswith("-c"):
                    continue          # an inline program, not a script invocation
                for tok in toks:
                    t = unquote(tok)
                    v = VAR_RE.match(t)
                    if v:
                        t = varmap.get(v.group(1), "")
                    if not t.endswith(".py"):
                        continue
                    d, b = os.path.split(t)
                    if d in HERE_DIRS:
                        hits.setdefault(b, []).append("%s:%d" % (script, no))
                    else:
                        ignored.append("%s:%d  %s" % (script, no, t))
                    break             # the first .py argument is the script
    return hits, ignored, missing


#  STANDALONE WORDS ONLY.  The first draft used a plain substring and reported
#  mips_fold_probe.py as self-labelled "witness" -- its summary line reads "the MIPS
#  fold-witness COUNTERS", where the word names a counter, not the artefact.  That is the
#  substring trap in the one place in this file that was allowed to be a heuristic, and an
#  advisory that cries wolf is an advisory nobody reads.  MEASURED: with the hyphen guard
#  the noise line disappears and pit8253's real disagreement still fires.
_LBL_W = re.compile(r"(?<![\w-])witness(?![\w-])", re.I)
_LBL_D = re.compile(r"(?<![\w-])detector(?![\w-])", re.I)


def domain(regress):
    """The .py artefacts this check governs, and (mode, why) describing how it decided.

    *** COMMITTED-OR-STAGED, NOT "ON DISK", AND THE FIRST VERSION HAD IT WRONG. ***  The
    first draft enumerated the directory, and MINUTES AFTER IT WAS WRITTEN a concurrent
    round dropped `sgi_eaddr_probe.py` into regress/ as untracked in-flight work.  This
    check went red -- correctly identifying a real unwired detector, but firing at a
    file its author had not yet offered for commit, in someone else's working tree.

    `git ls-files` reads the INDEX, so a probe enters the domain the moment it is `git
    add`ed -- which is precisely when "every COMMITTED detector" starts to apply, and
    precisely when the author is present to classify it.  A scratch probe that is never
    staged defends nothing in a fresh clone either, so it is honestly out of scope.

    FALLBACK IS ANNOUNCED, NEVER SILENT.  Outside a work tree (the --selftest copies)
    git cannot answer, and a fallback that quietly changes what a check governs is the
    kind of silent scope change this harness keeps being bitten by.  So the mode is
    printed on the summary line.
    """
    try:
        p = subprocess.run(["git", "ls-files", "--", "*.py"], cwd=regress,
                           capture_output=True, text=True)
        if p.returncode == 0:
            files = sorted(f for f in p.stdout.split()
                           if f.endswith(".py") and "/" not in f
                           and os.path.isfile(os.path.join(regress, f)))
            if files:
                return files, "tracked-or-staged"
    except OSError:
        pass
    return (sorted(f for f in os.listdir(regress)
                   if f.endswith(".py") and os.path.isfile(os.path.join(regress, f))),
            "on-disk (git could not answer)")


def self_label(path):
    """The file's OWN summary line, for the SELFLABEL advisory only.  Never a verdict."""
    try:
        head = read(path).splitlines()[:6]
    except OSError:
        return None
    for ln in head:
        has_w, has_d = bool(_LBL_W.search(ln)), bool(_LBL_D.search(ln))
        if has_w and not has_d:
            return CLASS_WITNESS
        if has_d and not has_w:
            return CLASS_DETECTOR
        if has_w and has_d:
            return None
    return None


#  =======================================================================================
#  SELFTEST.  Mutants are applied to COPIES in a temp dir; nothing in the repository is
#  touched, so no .MUTANT sentinel is needed.  EXIT STATUS IS TAKEN FROM THE PROCESS: this
#  project lost a whole battery result to `cmd | tail`, which reports tail's status, so a
#  KILLED run read as exit 0.  subprocess.run(...).returncode cannot make that mistake.
#
#  A CHECKER-SOURCE MUTANT THAT DOES NOT APPLY EXACTLY ONCE IS A FAULT, NEVER A PASS --
#  absorb_census.py's rule, and it is what keeps this selftest from silently going vacuous
#  after someone reformats the manifest below.
#
#  *** AND IT FIRED ON ITS OWN AUTHOR, FIRST RUN. ***  The mutants below started life as
#  plain string literals, which meant the text they searched for existed TWICE in this file:
#  once in the manifest and once in the selftest.  _st_apply refused ("x2 ... want 1") rather
#  than mutating both, which would have silently mutated the selftest instead of the subject.
#  So every mutant target is BUILT from its parts and never written out whole.
def _lit(*parts):
    """Join fragments, so the assembled search string appears nowhere in this source."""
    return "".join(parts)


def _exline(key):
    """Rebuild an EXEMPT source line from the table itself, for the same reason."""
    date, why = EXEMPT[key]
    return '    "%s":   ("%s", "%s"),\n' % (key, date, why)


PIT_RUN = '\npython3 pit8253_latch_probe.py "$PMAX" "$STUB" > "$PLOG" 2>&1 || true\n'
#  Four shapes of MENTION, none of which is an invocation.  The third is the live
#  gate_hygiene.sh:331 shape: one non-comment line carrying the basename AND `python3`,
#  whose message is that the probe did NOT run.
PIT_MENTIONS = (
    '\n#python3 pit8253_latch_probe.py "$PMAX" "$STUB" > "$PLOG" 2>&1 || true\n'
    '#  TODO: wire pit8253_latch_probe.py in\n'
    'note "pit8253_latch_probe.py or python3 missing -- PIT rows NOT run"\n'
    'echo "see pit8253_latch_probe.py"\n'
)


def _st_apply(path, old, new, want=1):
    src = read(path)
    n = src.count(old)
    if n != want:
        raise RuntimeError("MUTANT DID NOT APPLY: %r x%d in %s (want %d)"
                           % (old[:56], n, os.path.basename(path), want))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src.replace(old, new))


def _st_append(path, text):
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def selftest(verbose=False):
    import shutil
    import subprocess
    import tempfile

    src_regress = DEFAULT_REGRESS
    me = os.path.abspath(__file__)
    root = tempfile.mkdtemp(prefix="probewiring_selftest_")
    results = []

    #  *** THE BASELINE MUST BE GREEN BY CONSTRUCTION, AND THE FIRST VERSION WAS NOT. ***
    #  fresh() copied EVERY .py from the live tree, so when a concurrent round dropped an
    #  unclassified probe into regress/, M0/M2b/M5a all went red and the selftest announced
    #  "THE CHECKER CAN NO LONGER BE SHOWN TO FAIL".  Right colour, WRONG DIAGNOSIS: it
    #  blamed the checker for an APPARATUS state -- gate_offline's F5 shape, and the
    #  dangerous one, because it points the reader at the wrong file.
    #
    #  So the baseline copies exactly the MANIFEST set.  Live-tree content can no longer
    #  perturb a mutant, and M6 still tests the unclassified-arrival path by ADDING one.
    #  A MANIFEST entry with no source file is a SETUP FAULT here, never a mutant result --
    #  absorb_census.py's rule that a crash is a fault and never a detection.
    def fresh():
        work = tempfile.mkdtemp(dir=root)
        rg = os.path.join(work, "regress")
        os.makedirs(rg)
        for f in os.listdir(src_regress):
            if f.endswith(".sh") or (f.endswith(".py") and f in MANIFEST):
                shutil.copyfile(os.path.join(src_regress, f), os.path.join(rg, f))
        chk = os.path.join(work, "check_probe_wiring.py")
        shutil.copyfile(me, chk)
        return rg, chk

    absent = [f for f in sorted(MANIFEST) if not os.path.isfile(os.path.join(src_regress, f))]
    if absent:
        print("PROBEWIRING_SELFTEST_SETUP  the MANIFEST names files regress/ does not have:")
        for f in absent:
            print("    %s" % f)
        print("  fix the manifest first; a selftest on a broken baseline proves nothing.")
        return 2

    def case(name, want_rc, want_text, chk, rg, extra=(), forbid=None):
        p = subprocess.run([sys.executable, chk, "--regress", rg] + list(extra),
                           capture_output=True, text=True)
        out = p.stdout + p.stderr
        ok = (p.returncode == want_rc) and (want_text in out)
        if forbid is not None and forbid in out:
            ok = False
        results.append(ok)
        print("  %s  %-48s rc=%d want=%d" % ("ok  " if ok else "FAIL", name,
                                             p.returncode, want_rc))
        if verbose or not ok:
            for l in out.splitlines():
                if want_text in l or l.startswith("PROBEWIRING"):
                    print("          %s" % l.strip()[:160])
        if not ok:
            print("      --- full output ---\n%s" % out)

    print("=" * 96)
    print("  check_probe_wiring --selftest   (mutants on copies; the repo is not touched)")
    print("=" * 96)

    rg, chk = fresh()
    case("M0  unmutated copy is GREEN", 0, "PROBEWIRING_PASS", chk, rg)

    rg, chk = fresh(); _st_apply(chk, _exline("pit8253_latch_probe.py"), "")
    case("M1  an unwired detector is NAMED", 1,
         "UNWIRED DETECTOR  pit8253_latch_probe.py", chk, rg)

    rg, chk = fresh(); _st_apply(chk, _exline("pit8253_latch_probe.py"), "")
    _st_append(os.path.join(rg, "gate_arm.sh"), PIT_MENTIONS)
    case("M2  4 MENTIONS do not count as wiring", 1,
         "UNWIRED DETECTOR  pit8253_latch_probe.py", chk, rg)

    rg, chk = fresh(); _st_apply(chk, _exline("pit8253_latch_probe.py"), "")
    _st_append(os.path.join(rg, "gate_arm.sh"), PIT_RUN)
    case("M2b SATISFIABLE: a real invocation turns it green", 0, "PROBEWIRING_PASS",
         chk, rg, forbid="UNWIRED")

    rg, chk = fresh(); _st_append(os.path.join(rg, "gate_arm.sh"), PIT_RUN)
    case("M3  wired AND still exempt -> STALE EXEMPTION", 1,
         "STALE EXEMPTION  pit8253_latch_probe.py", chk, rg)

    rg, chk = fresh()
    _st_append(os.path.join(rg, "gate_sh_rounding.sh"),
               '\npython3 sh4pcic_witness.py "$PMAX" "$KERNEL" > "$WLOG" 2>&1 || true\n')
    case("M4  a WITNESS wired into a gate reddens", 1,
         "GATED WITNESS  sh4pcic_witness.py", chk, rg)

    rg, chk = fresh()
    case("M5a a live exemption is GREEN the day before", 0, "PROBEWIRING_PASS", chk, rg,
         extra=("--today", "2026-09-19"))
    case("M5b the same tree is RED the day after", 1, "EXPIRED EXEMPTION", chk, rg,
         extra=("--today", "2026-09-21"))

    for tag, bad in (("M5c unpadded (the ieee_store shape)", '"2026-9-20"'),
                     ("M5d empty", '""'),
                     ("M5e not a date at all", '"soon"')):
        rg, chk = fresh()
        k = "sh4_bsc_width_probe.py"
        _st_apply(chk, _exline(k), '    "%s":   (%s, "x"),\n' % (k, bad))
        case("%-44s is RED, not unexpired" % tag, 1,
             "MALFORMED EXEMPTION  sh4_bsc_width_probe.py", chk, rg,
             extra=("--today", "2026-08-21"))

    rg, chk = fresh()
    with open(os.path.join(rg, "zz_new_probe.py"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("#!/usr/bin/env python3\n")
    case("M6  a NEW probe arriving unclassified reddens", 1,
         "UNCLASSIFIED  zz_new_probe.py", chk, rg)

    rg, chk = fresh(); os.remove(os.path.join(rg, "pit8253_latch_probe.py"))
    case("M7  a MANIFEST entry whose file is gone reddens", 1,
         "GHOST  the MANIFEST names pit8253_latch_probe.py", chk, rg)

    rg, chk = fresh()
    _st_apply(chk, _lit('"pit8253_latch_probe.py"', ':      (CLASS_DETECTOR'),
              _lit('"pit8253_latch_probe.py"', ':      (CLASS_TOOL'))
    case("M8  hiding a detector in class 'tool' reddens", 1,
         "MISFILED  pit8253_latch_probe.py", chk, rg)

    rg, chk = fresh()
    _st_apply(os.path.join(rg, "run.sh"), " gate_arm gate_ppc_halt", " gate_ppc_halt")
    case("M9  dropping gate_arm from GATES unwires its 8", 1,
         "UNWIRED DETECTOR  arm_flags_probe.py", chk, rg)

    rg, chk = fresh(); os.remove(os.path.join(rg, "gate_ppc.sh"))
    case("M10 a gate named in GATES with no file reddens", 1,
         "run.sh names gate_ppc.sh", chk, rg)

    rg, chk = fresh(); _st_apply(os.path.join(rg, "run.sh"), "GATES=(", "GATESX=(")
    case("M11 an unparseable GATES array reddens", 1, "no GATES=( ... ) array", chk, rg)

    rg, chk = fresh()
    _st_apply(chk, _lit('"hpcmips_ctor_probe.py"', ':    ("2026-09-20"'),
              _lit('"hpcabort_witness.py"', ':    ("2026-09-20"'))
    case("M12 exempting a WITNESS reddens", 1,
         "ORPHAN EXEMPTION  hpcabort_witness.py", chk, rg)

    shutil.rmtree(root, ignore_errors=True)
    n_ok = sum(1 for r in results if r)
    print()
    if n_ok != len(results):
        print("PROBEWIRING_SELFTEST_FAIL  %d/%d mutants behaved as specified"
              % (n_ok, len(results)))
        return 1
    print("PROBEWIRING_SELFTEST_PASS  %d/%d mutants behaved as specified"
          % (n_ok, len(results)))
    return 0


def main(argv):
    verbose = "-v" in argv or "--verbose" in argv
    if "--selftest" in argv:
        return selftest(verbose)
    regress = DEFAULT_REGRESS
    today = None
    for i, a in enumerate(argv):
        if a == "--regress" and i + 1 < len(argv):
            regress = os.path.abspath(argv[i + 1])
        if a == "--today" and i + 1 < len(argv):
            today = argv[i + 1]
    if today is None:
        import datetime
        today = datetime.date.today().isoformat()

    fails, notes = [], []

    if not os.path.isdir(regress):
        print("PROBEWIRING_FAIL  no regress dir at %s" % regress)
        return 1

    scripts, err = gate_list(regress)
    if err:
        print("  FAIL  %s" % err)
        print("PROBEWIRING_FAIL  the battery could not be derived")
        return 1
    scripts = scripts + [s for s in ALWAYS if s not in scripts]

    hits, ignored, missing = exec_sites(regress, scripts)
    for s in missing:
        fails.append("run.sh names %s and the file does not exist -- the battery is broken" % s)

    on_disk, mode = domain(regress)

    for f in on_disk:
        if f not in MANIFEST:
            fails.append("UNCLASSIFIED  %s is not in check_probe_wiring.py's MANIFEST.\n"
                         "                classify it detector (green once fixed), witness "
                         "(red once fixed) or tool." % f)
    for f in sorted(MANIFEST):
        if f not in on_disk:
            fails.append("GHOST  the MANIFEST names %s and regress/ has no such file -- "
                         "delete the entry" % f)

    rows = []
    for f in on_disk:
        if f not in MANIFEST:
            continue
        cls, why = MANIFEST[f]
        where = hits.get(f, [])
        if cls not in CLASSES:
            fails.append("BAD CLASS  %s is classified '%s'; want one of %s"
                         % (f, cls, "/".join(CLASSES)))
            continue

        if cls == CLASS_TOOL and (f.endswith("_probe.py") or f.endswith("_witness.py")):
            fails.append("MISFILED  %s is classified 'tool'. A file named *_probe.py or "
                         "*_witness.py asserts something; classify it detector or witness."
                         % f)

        if cls == CLASS_DETECTOR:
            if where:
                state = "RUN by " + ", ".join(where)
                if f in EXEMPT:
                    fails.append("STALE EXEMPTION  %s is RUN by %s and still carries an "
                                 "exemption dated %s -- the debt is paid, delete the line"
                                 % (f, where[0], EXEMPT[f][0]))
            elif f in EXEMPT:
                d = EXEMPT[f][0]
                if not DATE_RE.match(d or ""):
                    fails.append("MALFORMED EXEMPTION  %s:'%s' is not YYYY-MM-DD. A date "
                                 "nothing validates never expires -- refusing to guess."
                                 % (f, d))
                    state = "EXEMPT(BAD-DATE)"
                elif d < today:
                    fails.append("EXPIRED EXEMPTION  %s came due %s (today %s) and is still "
                                 "run by no gate" % (f, d, today))
                    state = "EXEMPT(EXPIRED %s)" % d
                else:
                    state = "EXEMPT until %s" % d
            else:
                fails.append("UNWIRED DETECTOR  %s is run by NO gate and has no dated "
                             "exemption.\n                wire it into a gate, or add a dated "
                             "line to EXEMPT naming the gate that owes it." % f)
                state = "UNWIRED"
        elif cls == CLASS_WITNESS:
            if where:
                fails.append("GATED WITNESS  %s is invoked at %s. A witness asserts the "
                             "PRE-FIX symptom, so it goes RED the day the fix lands -- "
                             "gating it manufactures a regression." % (f, where[0]))
                state = "GATED (must not be): " + ", ".join(where)
            else:
                state = "not run (correct)"
        else:
            state = ("RUN by " + ", ".join(where)) if where else "-"

        if cls in (CLASS_DETECTOR, CLASS_WITNESS):
            lbl = self_label(os.path.join(regress, f))
            if lbl and lbl != cls:
                notes.append("SELFLABEL  %s: manifest says %s, its own summary line says %s. "
                             "Advisory only -- self-labels are measurably unreliable in both "
                             "directions." % (f, cls, lbl))
        rows.append((cls, f, state, why))

    for f in sorted(EXEMPT):
        if f not in MANIFEST:
            fails.append("ORPHAN EXEMPTION  %s is exempted and is not in the MANIFEST" % f)
        elif MANIFEST[f][0] != CLASS_DETECTOR:
            fails.append("ORPHAN EXEMPTION  %s is classified '%s'; only a detector can be "
                         "exempted from being run" % (f, MANIFEST[f][0]))

    print("  check_probe_wiring: %d python artefacts in %s/ [%s], %d battery scripts "
          "from run.sh" % (len(on_disk), os.path.basename(regress), mode, len(scripts)))
    if verbose:
        for cls in CLASSES:
            for c, f, state, why in rows:
                if c == cls:
                    print("    %-8s %-28s %-38s %s" % (c, f, state, why))
        for line in ignored:
            print("    IGNORED  %s   (not the regress copy)" % line)
    for n in notes:
        print("  note  %s" % n)
    for f in fails:
        print("  FAIL  %s" % f)

    det = [r for r in rows if r[0] == CLASS_DETECTOR]
    run = [r for r in det if r[2].startswith("RUN")]
    ex = [r for r in det if r[2].startswith("EXEMPT")]
    wit = [r for r in rows if r[0] == CLASS_WITNESS]
    if fails:
        print("PROBEWIRING_FAIL  %d problem(s); %d/%d detectors run by a gate, %d dated-exempt"
              % (len(fails), len(run), len(det), len(ex)))
        return 1
    print("PROBEWIRING_PASS  %d/%d detectors run by a gate, %d dated-exempt, %d witnesses "
          "correctly ungated" % (len(run), len(det), len(ex), len(wit)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
