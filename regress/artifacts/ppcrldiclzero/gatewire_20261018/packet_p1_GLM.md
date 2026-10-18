**Your token: `GLM_RLDICLWIRE_20261018`** -- open your answer with it.

# Wiring `regress/ppc_rldicl_probe.py` into gate 13 before its exemption refuses every commit -- design, pass 1

**Please do not simply ratify.**  A recent panel had seven of nine seats confirm a premise its brief stated wrongly.
Check the premises against the files, not just the reasoning.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at
HEAD; ignore any other `src/` you find.  READ-ONLY: write nothing to any project tree.  The working tree carries another
session's uncommitted edits in some files -- NOT in `regress/gate_ppc.sh`, `regress/ppc_rldicl_probe.py` or
`regress/lib.sh`; `tools/pipeline/check_probe_wiring.py` IS dirty, so read its committed text with `git show HEAD:`.

## 0. The problem

`tools/pipeline/check_probe_wiring.py` (precommit section R) keeps an EXEMPT table of committed detectors no gate runs,
each with a date.  `ppc_rldicl_probe.py` -- round #522's detector for `rldicl` writing zero on every execution, fixed in
`e777ff06` -- is exempt until **2026-10-22**; on that day section R refuses EVERY commit until it is wired or re-dated (a
re-date takes an owner ruling, `04f3e7c0` was the last one).  Its exemption text says what is owed:

    #  gates drive a 32-bit part.  Closing that is a harness round, filed to wiringcliff.
    #  *** ITS REASON EXPIRES WITH THE rlwimi/rldimi WIRING: gate_ppc.sh now EXECUTES -M 64. ***
    #  What remains is a gate block: this probe prints ok/FAIL rows, `SCORE n/m' and a DONE line, which a
    #  gate can score by rows, as gate_arm.sh scores mk48's; it prints no RESULT/CONTROL lines, and adding
    #  them is one way to write that block, not a prerequisite for it.  (This said "What remains is the
    #  instrument: this probe prints no RESULT/CONTROL lines", and before #550 went on "so a gate could only
    #  score its exit status" -- both false: GPT-6 Astra, late on the F2b pass.)
    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the cheapest of
    #  the ten -- 24/24 in under a second on a machine gate_ppc.sh already runs (the run:
    #  regress/artifacts/exemptredate_20260925/opus550_measured_p2/p1_runs/); owed: a gate_ppc.sh block
    #  beside rldimi/rlwimi, scoring its rows -- or RESULT/CONTROL lines, then that block.  None of
    #  want_rldimi, want_rlwimi, want_rlwinm or mask32 is called outside the helpers' own definitions
    #  (grep -nE '(want_rldimi|want_rlwimi|want_rlwinm|mask32)[(]' on the probe), so an edit of them
    #  is no prerequisite.
    #  Re-dated 2026-10-08 -> 2026-10-22 on 2026-10-09 by owner ruling, in its own commit: it came due with its
    #  gate_ppc.sh block still owed and refused every commit.  A re-date is not a discharge.
    "ppc_rldicl_probe.py":         ("2026-10-22",
                                    "gate_ppc.sh now executes -M 64 (rlwimi/rldimi); owed: a "
                                    "gate_ppc.sh block scoring its ok/FAIL rows as gate_arm.sh "
                                    "scores mk48's -- RESULT/CONTROL lines first is a chosen "
                                    "approach, not a prerequisite; filed to wiringcliff"),

This round wires it.  Witness kind `harness:` (the round's subject is the test apparatus): no `regress/gate_*.sh` names
the probe today (`grep -n rldicl regress/gate_*.sh` returns nothing).

## 1. The probe's output today (`build/gxemul`, built 2026-10-17 22:14, run once 2026-10-18; rows end ` ok` or ` FAIL`)

```
session            exit0                exit0                the control session ran to `quit'                ok
live               0x1234               0x1234               li r9,0x1234 -- the guest executes and readback works ok
seed holds         0x5a5a5a5a5a5a5a5a   0x5a5a5a5a5a5a5a5a   r30 seeded, never a destination: a 0 readback means SOMETHING wrote it ok
src intact         0xdeadbeefcafef00d   0xdeadbeefcafef00d   rS is unchanged by any of these instructions     ok
disasm xcheck      6/6                  6/6                  tree's OWN disassembler agrees with the encoder, operand for operand ok
zx32 rldicl        0xcafef00d           0xcafef00d           clrldi r4,r3,32 -- the 32-bit zero-extend compilers emit constantly ok
zx32 rldicr        0xdeadbeef00000000   0xdeadbeef00000000   DISCRIMINATING: the sibling, same session, same rotate, same encoder ok
rot8 rldicl        0xadbeefcafef00dde   0xadbeefcafef00dde   rotldi r6,r3,8 -- mask is all-ones, so this is a PURE rotate ok
rot8 rldicr        0xadbeefcafef00dde   0xadbeefcafef00dde   DISCRIMINATING: the same pure rotate through the good sibling ok
naive fix wrong    differs              differs              DERIVED, arithmetic only: `&'->`|' ships OR-not-AND (0xdeadbeefffffffff).  Deleting the AND on the FIXED code ships ROTL alone -- see M_NOM
neg apparatus      exit1/-0x1           exit1/-0x1           bogus machine -> no guest -> `live' MUST fail; the oracle is failable ok
bits32 live        0x1234               0x1234               PPC603 (32-bit): the guest still runs -- li executes ok
bits32 rld bad     TODO                 TODO                 decoder prints `TODO: rld* in 32-bit mode?' and goes to bad -- unreachable ok
vacuous cell       0x0                  0x0                  rS=0xffffffff00000000, SH=0, MB=32: correct answer IS 0 -- GREEN on a ok
vac neighbour      0xffffffff00000000   0xffffffff00000000     broken build.  Its MB=0 neighbour on the same rS is not vacuous. ok
census run         190                  190                  (SH,MB) cells driven: MB sweep + SH sweep + diagonal, rS=all-ones ok
census wrong       0                    0                    cells whose result differs from MASK(MB,63) -- want 0 after a fix ok
census zero        0                    0                    cells that returned EXACTLY ZERO -- want 0 after a fix ok
disasm total       196/196              196/196              every placed word re-read by the tree's own disassembler ok
cand session       exit0                exit0                the candidate-row session ran to `quit'          ok
cr parsed          yes                  yes                  NEGATIVE CONTROL on the apparatus: the cr regex must MATCH something ok
sh63 rldicl        0xef56df77e57f7806   0xef56df77e57f7806   SH=63: pins the sh5 bit of the SH decode         ok
sh32 rldicl        0xdeadbeef           0xdeadbeef           SH=32,MB=32 high-word extract: pins the sh5 bit again, on a masked cell ok
rc cr0             0x40000000           0x40000000           rldicl. -> CR0=GT.  defect gives EQ(0x2...), update_cr0(cpu,tmp) gives LT(0x8...) ok
SCORE 24/24  elapsed=0.3s  binary=/mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul  label=gate
FAILING: 
PPC_RLDICL_PROBE_DONE
```

## 2. The proposed block -- `regress/gate_ppc.sh`, after the rldimi block and BEFORE `need_file "$IMAGES/netbsd401-macppc-GENERIC"`

```sh

# ---- ppcrldiclzero (#522): X(rldicl) wrote ZERO on every execution -- its 24-row detector -----
# Shipped EXEMPT with e777ff06 (2026-09-10) and re-dated once (04f3e7c0, owner ruling) because no
# block here scored it; this block discharges that exemption.  BEFORE the NetBSD prerequisite for the
# reason the rlwimi block gives: `-E bareppc -M 64` needs no image, so a red row is recorded first.
# The probe prints no RESULT/CONTROL protocol, so it is scored as gate_arm.sh scores mk48's: its
# completion sentinel, then EVERY row by name, then the emitted/green/red counts and its own SCORE
# line, each pinned to a literal so a shrunk or renamed table cannot pass.  Names sit in a %-18s
# column and none is longer than 15, so `^name  ' cannot match a neighbour (the padded-column trap).
RLCLOG=$LOGDIR/ppc_rldicl.log
python3 -u ppc_rldicl_probe.py "$PMAX" gate > "$RLCLOG" 2>&1 || true
if [ "$(grep -cx 'PPC_RLDICL_PROBE_DONE' "$RLCLOG")" != 1 ]; then
    note "rldicl: completion sentinel missing or duplicated; last lines follow"
    tail -5 "$RLCLOG" | sed 's/^/       /'
    check "rldicl probe completed" "no" "yes"
else
    check "rldicl probe completed" "yes" "yes"
    for v in "session" "live" "seed holds" "src intact" "disasm xcheck" "zx32 rldicl" "zx32 rldicr" "rot8 rldicl" "rot8 rldicr" "naive fix wrong" "neg apparatus" "bits32 live" "bits32 rld bad" "vacuous cell" "vac neighbour" "census run" "census wrong" "census zero" "disasm total" "cand session" "cr parsed" "sh63 rldicl" "sh32 rldicl" "rc cr0"; do
        check "rldicl row: $v" "$(count "$RLCLOG" "^$v  .*ok$")" "1"
    done
    check "rldicl rows emitted" "$(( $(count "$RLCLOG" " ok$") + $(count "$RLCLOG" " FAIL$") ))" "24"
    check "rldicl rows green"   "$(count "$RLCLOG" " ok$")"   "24"
    check "rldicl rows red"     "$(count "$RLCLOG" " FAIL$")" "0"
    check "rldicl score line"   "$(grep -c '^SCORE 24/24 ' "$RLCLOG")" "1"
fi
```

`count` is `regress/lib.sh`'s (`grep -ac -- "$2" "$1"`, 0 for an absent file); `check` compares two strings exactly.
The model is the mk48 block in `regress/gate_arm.sh` (search `mk48nvramkill (#521) + #536`), which discharged the same
kind of exemption in `#536`.  The gate's `gate_begin` title gains "+ rldicl".  The commit also deletes the probe's EXEMPT
entry (and its comment lines) from `tools/pipeline/check_probe_wiring.py`.

## 3. The negative controls planned (the harness witness must FAIL on what it should catch)

1. the current build -> the block is green, 29 checks (completion + 24 rows + emitted + green + red + score);
2. a pre-fix binary (`e777ff06`'s parent, built in a scratch clone) -> the rows the defect reaches go red;
3. the same block run on DOCTORED logs: the DONE sentinel removed; a duplicated DONE; one row renamed; one row's `ok` turned
   to `FAIL`; a 23-row log; an extra stray ` ok` line -> each goes red on the check that should catch it;
4. section R's own result: the EXEMPT entry removed and the probe found wired.

## 4. Questions

**Q1.**  Is this block enough to DISCHARGE the exemption as its text words it ("a gate_ppc.sh block scoring its ok/FAIL rows
as gate_arm.sh scores mk48's")?  Does `check_probe_wiring.py` recognise a probe as wired by this exec line -- check how it
detects wiring (`git show HEAD:tools/pipeline/check_probe_wiring.py`)?
**Q2.**  Is any row check unsatisfiable or able to match the wrong line (substring overlap such as `live` / `bits32 live`,
`session` / `cand session`; a name at its column width; the `vac neighbour` row whose note is long)?
**Q3.**  Are the negative controls in section 3 the right ones, and is any one MISSING -- e.g. a run killed mid-way, a probe
that exits non-zero, a binary absent (`need_exec` already covers that at the top)?
**Q4.**  Placement and timing: before `need_file` as argued?  Any load-sensitive wall-clock in the probe that a gate run
could trip?  Is there anything else in the tree (the gate's own check count pin, a battery manifest, `run.sh`) that must
change in the same commit?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q4.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
