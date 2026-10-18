**Your token: `GROK_IP30WIRE_20261018`** -- open your answer with it.

# Wiring `regress/artifacts/ip30abortkill/ip30_abort_probe.py` into gate 14 before its exemption refuses every commit -- design, pass 1

**Please do not simply ratify.**  A recent panel had seven of nine seats confirm a premise its brief stated wrongly.
Check the premises against the files, not just the reasoning; where a premise below is stated as a fact, it carries the
command or file that settled it, and you are asked to re-check any you can.  The tree is
`C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD 2036a3d5; ignore any other `src/` you find.  READ-ONLY: write nothing to
any project tree.  **The working tree carries THIS round's uncommitted edits** in `regress/gate_arm.sh` (the block in
section 3, and nothing else), `tools/precommit_check.sh` (one pin, 34 -> 35) and `tools/pipeline/check_probe_wiring.py`
(three hunks, section 1 S5) -- and `check_probe_wiring.py` ALSO carries another unit's uncommitted lines, so read its
committed text with `git show HEAD:`.  The probe file itself is unmodified (working tree == HEAD).

## 0. The problem

`tools/pipeline/check_probe_wiring.py` (precommit section R) keeps a dated EXEMPT table of committed DETECTORS that no
gate runs.  `regress/artifacts/ip30abortkill/ip30_abort_probe.py` -- round #531's detector (686d179c, 2026-09-18) for four
guest-reachable `abort()` calls in `src/devices/dev_sgi_ip30.c` on the advertised `-E sgi -e ip30` -- is exempt until
**2026-10-30**.  Measured 2026-10-18 with HEAD's checker: `--today 2026-10-31` prints
`FAIL  EXPIRED EXEMPTION  artifacts/ip30abortkill/ip30_abort_probe.py came due 2026-10-30 (today 2026-10-31) and is still
run by no gate` (beside four other entries that are another session's).  Its date history, from `git log` of the checker:
2026-09-20 (686d179c), then eec0f4a3 (2026-09-19) to 09-27, 04500deb (#550, 2026-09-26) to 10-15, 7b23b785 (2026-10-16) to
10-30 -- the last by a four-seat ruling where three seats ruled re-date and GPT-6 Astra ruled "wire now".  The entry's own
text: "no gate runs an SGI IP30 guest session (gate_asan_sweep.sh constructs only)"; its comment adds that gate_arm.sh
already runs seven sgi cold-debugger probes of this shape (each execs `-e ip32` itself), "so a home exists", and that
"#550 measured the probe at 568 s standalone for its 33 rows ... gate_arm.sh runs in the weekly battery and as an attended
targeted gate, never per commit."

## 1. Settled premises (each with its warrant -- re-check what you can)

* **S1 the probe's protocol** (`ip30_abort_probe.py`, its report section at the end of the file): it prints a header line,
  `IP30ABORT_CONTROL=OK|DEAD`, then one line per row as
  `print("  %-12s got=%-12s want=%-12s %s  %s" % (nm, got, want, "ok" if ok else "FAIL", note[:70]))`, then
  `IP30ABORT_RESULT=%d/%d` (n green / len(rows)) and `IP30ABORT_DONE`.  CONTROL is DEAD when row `live` or `devsig` misses
  its want; then it prints `IP30ABORT_RESULT=0/0`, a SETUP FAILED line, every row as `"  %-12s got=%-12s want=%-12s %s"`
  (NO status token), and `IP30ABORT_DONE`, and raises `SystemExit(0)`.  So the exit status is 0 on every path that
  finishes; non-zero only on a crash.  Each session is one `pty.fork` + `execv(BIN, [-V -x -E sgi -e ip30 -M 64 ...])`.
* **S2 run time**: 568 s for 33/33 on `build/gxemul` (#550's measurement, `regress/artifacts/exemptredate_20260925/
  opus550_measured_p2/keep_p1_logs.out`; and this round's run 10:42-10:52 on 2026-10-18, 33/33).  The cost is the probe's
  12 s death poll, which every SURVIVING session waits out (`deadline = time.time() + 12.0` after a 2.5 s spin).
* **S3 gate 14 today**: last weekly battery (2026-10-11, before #564 added rows) `gate 14: ... PASS (1110 checks)`.  Neither
  `regress/run.sh` nor `tools/nightly_battery.sh` contains `timeout` (grep).  That battery ran 18:02 -> 22:02.
* **S4 section U** (`tools/pipeline/check_score_claims.py`): its PIN regex is
  `check\s+"(\S+)\s+rows\s+run"\s+"[^"]*"\s+(\d+)`; for each pin it checks comment lines in that gate naming the stem, and
  the docstring of `regress/<stem>_probe.py` or `regress/<stem>.py` ONLY -- so this probe's docstring, under
  `regress/artifacts/`, is NOT checked.  Measured on the working tree: `SCORE_CLAIMS_PASS 35 gate comment set(s) checked; 13
  of 35 stems also have a probe docstring checked`.  `precommit_check.sh` pins the count by equality, 34 -> 35 here.
* **S5 section R**: with the block in the working tree, HEAD's checker reports `FAIL STALE EXEMPTION artifacts/ip30abortkill/
  ip30_abort_probe.py is RUN by gate_arm.sh:1528 and still carries an exemption dated 2026-10-30 -- the debt is paid, delete
  the line`; with the entry and its comment (28 lines) deleted it reports `PROBEWIRING_PASS 77/85 detectors run by a gate, 8
  dated-exempt`.  The same edit adds a DISCHARGED note beside #565's and corrects the MANIFEST entry's own text, which said
  `*** RUNS IN NO GATE: see EXEMPT. ***`.
* **S6 #531 changed one source file**: `git show --stat 686d179c -- src/` lists only `src/devices/dev_sgi_ip30.c`, and its
  parent's copy is byte-identical to the upstream import's (39748e3c) with 4 `abort()` calls (HEAD's has 1 match, in a
  comment).

## 2. The probe's output today (`build/gxemul`, 2026-10-18 10:52; notes truncated by the probe at 70 characters)

```
ip30_abort_probe -- binary=/mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul label=gate machine=sgi/ip30
IP30ABORT_CONTROL=OK
  live         got=0x11223344   want=0x11223344   ok  LIVENESS: a known value planted in RAM returns through a guest load. I
  devsig       got=0xffffffff80010000 want=0xffffffff80010000 ok  DEVICE-SIGNATURE: case 0x20 answers 0x80010000 and `lw' SIGN-EXTENDS i
  acc 18       got=0xffffffffdeadbeef want=0xffffffffdeadbeef ok  case 0x10018 is IMPLEMENTED r/w (the PROM complains without it). An ac
  acc 30 rd    got=alive        want=alive        ok  case 0x10030 IS writeflag-tested, so its READ returns d->isr and must 
  acc 20000    got=stored+N*1000 want=stored+N*1000 ok  case 0x20000 is writeflag-tested r/w AND is incremented 1000 per DEVIC
  acc 30000    got=0x5678       want=0x5678       ok  case 0x30000, writeflag-tested r/w. Second neighbour.
  acc imask    got=0x40000      want=0x40000      ok  case 0x10000 (imask0) accepts and reads back. THE accept row for the t
  kill 20 rd   got=alive        want=alive        ok  *** A GUEST **LOAD** AT 0x0ff10020. case 0x10020 has NO writeflag test
  kill 20 rd txt got=no           want=no           ok  DIAGNOSIS ONLY, never half the trigger: a reworded-message mutant stil
  kill 28 rd   got=alive        want=alive        ok  case 0x10028, same missing writeflag test; `d->isr &= ~idata' is a no-
  kill 28 rd txt got=no           want=no           ok  DIAGNOSIS ONLY, never half the trigger: a reworded-message mutant stil
  kill 30 wr   got=alive        want=alive        ok  case 0x10030's WRITE arm aborts while its read is serviced -- the asym
  kill 30 txt  got=yes          want=yes          ok  DIAGNOSIS sibling for the 0x10030 WRITE arm, bound to THIS session's 0
  tick 50      got=alive        want=alive        ok  *** ARM imask0 BIT 50 WITH `sd', THEN ONE STEP. ***  Pre-fix the DEVIC
  tick 50 txt  got=yes          want=yes          ok  *** THE POST-FIX HALF OF THE DISCRIMINATOR. ***  `tick 50' pins that t
  tick 49      got=no           want=no           ok  DISCRIMINATOR for `tick 50': bit 49 is NOT the guarded bit, so the arm
  kill 20 wr   got=alive        want=alive        ok  A guest WRITE at this offset.  Pre-fix it reaches the same abort(); po
  kill 20 wr txt got=yes          want=yes          ok  DIAGNOSIS for the 20 WRITE arm specifically.  Single-access session, s
  kill 28 wr   got=alive        want=alive        ok  A guest WRITE at this offset.  Pre-fix it reaches the same abort(); po
  kill 28 wr txt got=yes          want=yes          ok  DIAGNOSIS for the 28 WRITE arm specifically.  Single-access session, s
  isr keep     got=0x5a5a       want=0x5a5a       ok  *** ISR UNCHANGED ACROSS A LOAD AT 0x10020. ***  Seed via the Set arm,
  isr clr      got=0x5050       want=0x5050       ok  *** 0x5a5a & ~0x0a0a = 0x5050. ***  Pins that the Clear-ISR store STIL
  isr drop 30  got=0x5a5a       want=0x5a5a       ok  *** THE WRITE MUST BE DISCARDED. ***  Re-inserting `d->isr &= ~idata' 
  xbit isr     got=1            want=1            ok  *** TICK FIRST, THEN AN ISR ACCESS, IN ONE DEVICE LIFETIME. ***  Both 
  xbit tick    got=1            want=1            ok  The other half of the same session: the TICK announce is still exactly
  latch 1x     got=1            want=1            ok  TWO declined ISR accesses, ONE announce -- that is what the unqualifie
  isr 20 rd val got=0x0          want=0x0          ok  A declined READ at 0x10020 returns ZERO, not a mirror of d->isr.  `oda
  isr 28 rd val got=0x0          want=0x0          ok  A declined READ at 0x10028 returns ZERO, not a mirror of d->isr -- the
  latch 28wr   got=1            want=1            ok  TWO accesses at THIS ARM ALONE, so the count attributes to it.  `latch
  latch 30wr   got=1            want=1            ok  TWO accesses at THIS ARM ALONE, so the count attributes to it.  `latch
  latch tick   got=1            want=1            ok  *** TWO TICKS IN ONE LIFETIME (step 65536 -- MEASURED to fire exactly 
  xbit rev     got=1            want=1            ok  *** TICK -> ISR -> TICK: the order the product comment's own hazard ne
  xbit rev2    got=1            want=1            ok  *** ISR -> TICK -> ISR: the mirror of `xbit rev', and the only order i
IP30ABORT_RESULT=33/33
IP30ABORT_DONE
```

## 3. The proposed block -- `regress/gate_arm.sh`, at depth 0, right after the #564 `sgi_mte_decline` block

```sh
#  ---- #566 ip30abortkill (#531, 686d179c): dev_sgi_ip30.c's four guest-reachable abort() calls -- a guest load or
#  ---- store at 0x0ff10020 or 0x0ff10028, a store to 0x0ff10030, and DEVICE_TICK once a legal imask0 write sets bit
#  ---- 50 -- have declined with a latched announce since #531.  Its detector shipped with that fix and ran in no gate:
#  ---- check_probe_wiring.py held it EXEMPT, dated 2026-09-20 and re-dated three times (eec0f4a3 to 09-27, #550's
#  ---- 04500deb to 10-15, 7b23b785 on 2026-10-16 to 10-30), and HEAD's checker run with --today 2026-10-31 FAILS on it
#  ---- (measured 2026-10-18).  This block discharges that exemption.  The probe's CONTRACT, its MEASURED ESCAPES and
#  ---- its DOES NOT CATCH list are in its header; its kill tables are in regress/artifacts/ip30abortkill/.  At depth 0,
#  ---- so another probe's missing sentinel cannot swallow it.
#  ----
#  ---- RUN TIME, about 9.5 minutes: 568 s for the 33 rows on build/gxemul (#550 and #566 each measured it), because every
#  ---- session that survives waits out the probe's 12 s death poll.  That poll is what stops a slow abort reading as
#  ---- `alive', so it is not shortened here.  The waits are wall-clock: on a host loaded past them a session can be
#  ---- killed before its stepped access runs, and its row then reads that, not the device.  gate_arm.sh runs in the
#  ---- weekly battery, alone, and as an attended targeted gate -- never per commit.
#  ----
#  ---- Run from its artifacts path, as gate_sh_rounding.sh runs gdrom_pio_null_probe.py; a missing file fails the parse
#  ---- check below -- a FAIL, never a SKIP.
IP30LOG=$LOGDIR/ip30_abort.log
ip30rc=0
python3 -u artifacts/ip30abortkill/ip30_abort_probe.py "$PMAX" gate > "$IP30LOG" 2>&1 || ip30rc=$?

#  PARSE BEFORE SCORE: exactly one well-formed RESULT, CONTROL and DONE line.  A crash, a killed run or a missing file
#  leaves none and reds here.
if [ "$(grep -c '^IP30ABORT_RESULT=' "$IP30LOG")" != "1" ] ||
   ! grep -Eq '^IP30ABORT_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$IP30LOG" ||
   [ "$(grep -c '^IP30ABORT_CONTROL=' "$IP30LOG")" != "1" ] ||
   ! grep -Eq '^IP30ABORT_CONTROL=(OK|DEAD)$' "$IP30LOG" ||
   [ "$(grep -cx 'IP30ABORT_DONE' "$IP30LOG")" != "1" ]; then
    note "ip30_abort probe produced no unique, valid completion record; last lines follow"
    tail -5 "$IP30LOG" | sed 's/^/       /'
    check "ip30_abort probe output parses" "no" "yes"
else
    check "ip30_abort probe output parses" "yes" "yes"
    grep -E '^  .* got=.* want=.* FAIL  ' "$IP30LOG" | sed 's/^/       /'
    #  CONTROLS: `live' (a RAM plant returns through a guest load) and `devsig' (0x20 answers 0x80010000, which RAM
    #  cannot).  A DEAD vehicle prints a zero-row RESULT and rows with no status token, so every row check below reds too.
    check "ip30_abort controls" "$(sed -n 's/^IP30ABORT_CONTROL=//p' "$IP30LOG")" "OK"
    check "ip30_abort probe exit status" "$ip30rc" "0"

    #  EVERY ROW BY NAME, EXACTLY ONCE -- identity and uniqueness, which the counts below cannot give.  The probe prints
    #  `  %-12s got=%-12s want=%-12s <ok|FAIL>  <note>': the status token is NOT at the end of the line, so ` ok$'
    #  matches nothing here, and six names (`kill 20 rd txt', `isr 20 rd val', ...) are longer than their 12-column
    #  field.  So a row is matched by position -- its name, the got= and want= tokens (no value carries a space), then
    #  the status and its two trailing spaces -- and `^  <name>  *got=' cannot match a longer name beginning with this
    #  one (`kill 20 rd' / `kill 20 rd txt', `xbit rev' / `xbit rev2').  count() is plain grep: every `*' is BRE.
    for v in "live" "devsig" "acc 18" "acc 30 rd" "acc 20000" "acc 30000" "acc imask" "kill 20 rd" "kill 20 rd txt" "kill 28 rd" "kill 28 rd txt" "kill 30 wr" "kill 30 txt" "tick 50" "tick 50 txt" "tick 49" "kill 20 wr" "kill 20 wr txt" "kill 28 wr" "kill 28 wr txt" "isr keep" "isr clr" "isr drop 30" "xbit isr" "xbit tick" "latch 1x" "isr 20 rd val" "isr 28 rd val" "latch 28wr" "latch 30wr" "latch tick" "xbit rev" "xbit rev2"; do
        check "ip30_abort row: $v" "$(count "$IP30LOG" "^  $v  *got=[^ ]*  *want=[^ ]*  *ok  ")" "1"
    done

    #  DENOMINATORS, pinned to LITERALS: `rows run' is the probe's own count (RESULT's), `rows emitted' the row lines it
    #  printed -- two, because one cannot tell a LOST row from a failing one.  `[^=]*' stops at the first `=', which in a
    #  row line is got='s.  All 33 green on build/gxemul, measured before these pins were written
    #  (regress/artifacts/ip30abortkill/gatewire_20261018/).
    ip30res=$(sed -n 's/^IP30ABORT_RESULT=//p' "$IP30LOG")
    ip30ok=$(count "$IP30LOG" '^  [^=]* got=[^ ]*  *want=[^ ]*  *ok  ')
    ip30bad=$(count "$IP30LOG" '^  [^=]* got=[^ ]*  *want=[^ ]*  *FAIL  ')
    check "ip30_abort rows run"     "${ip30res#*/}" 33
    check "ip30_abort rows correct" "${ip30res%/*}" "33"
    check "ip30_abort rows emitted" "$((ip30ok + ip30bad))" "33"
    check "ip30_abort rows green"   "$ip30ok" "33"
    check "ip30_abort rows red"     "$ip30bad" "0"
fi
```

`count` is `regress/lib.sh`'s (`grep -ac -- "$2" "$1"`, echoing 0 for an absent file -- plain BRE, so `*` repeats the space
before it); `check` compares two strings exactly and counts a failure; `note` prints.  `gate_arm.sh` does
`cd "$(dirname "$0")"` first, so the path is relative to `regress/`; `PMAX` defaults to `$ROOT/build/gxemul` and
`need_exec "$PMAX"` runs at the top of the gate.  The gate's title is unchanged (it lists no SGI probe).

## 4. Measured so far, and what is running

The scoring text (everything after the probe invocation through `fi`) was extracted and run, under WSL bash, against the
real 33/33 log and ten doctored copies of it:

```
scoring text: 42 lines, md5 bc71bb535db4692030c6328dd97986e6
good          checks=41  fails=0   GREEN as-expected
n1_onefail    checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: kill 30 wr got=0] [ip30_abort rows green got=32] [ip30_abort rows red got=1]
n2_rowlost    checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: tick 49 got=0] [ip30_abort rows emitted got=32] [ip30_abort rows green got=32]
n3_rowdup     checks=41  fails=2   RED   as-expected
      red: [ip30_abort row: tick 50 got=2] [ip30_abort row: tick 49 got=0]
n4_dead       checks=41  fails=38  RED   as-expected
      red: [ip30_abort controls got=DEAD] [ip30_abort row: live got=0] [ip30_abort row: devsig got=0] [ip30_abort row: acc 18 got=0] [ip30_abort row: acc 30 rd got=0] [ip30_abort row: acc 20000 got=0] [ip30_abort row: acc 30000 go
n5_empty      checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n6_nodone     checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n7_tworesult  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n8_contra     checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: latch tick got=0] [ip30_abort rows green got=32] [ip30_abort rows red got=1]
n9_shrunk     checks=41  fails=5   RED   as-expected
      red: [ip30_abort row: xbit rev2 got=0] [ip30_abort rows run got=32] [ip30_abort rows correct got=32] [ip30_abort rows emitted got=32] [ip30_abort rows green got=32]
n10_renamed   checks=41  fails=1   RED   as-expected
      red: [ip30_abort row: acc imask got=0]
SCORE_SELFTEST_DONE
```

Running now in a scratch clone of `build/` (results to pass 2): **base** = HEAD rebuilt (must be green); **prefix** = HEAD
with `dev_sgi_ip30.c` set to 686d179c^'s, i.e. all four `abort()` calls back -- clause (a), and since #531 touched no other
source it is also clause (b)'s verbatim reinstatement at every fixed site; **absent** = `/nonexistent/gxemul` and
**nonemu** = `/bin/true` -- clause (c)'s null media for a runtime probe ("an ABSENT or NON-EMULATOR binary").  Each log is
scored by the block's own text, extracted from `gate_arm.sh`.  After this pass: ONE full gate 14 run with the final block,
before commit.

## 5. Questions

**Q1.**  Row matching.  Can `^  NAME  *got=[^ ]*  *want=[^ ]*  *ok  ` match the wrong line or miss the right one -- the six
names longer than the 12-column field (`kill 20 rd txt` etc.), got/want values longer than 12 (`0xffffffffdeadbeef`,
`stored+N*1000`), a value that could contain a space, a prefix pair (`kill 20 rd` / `kill 20 rd txt`, `xbit rev` /
`xbit rev2`, `tick 50` / `tick 50 txt`)?  Are the two denominator patterns (`^  [^=]* got=...  *ok  ` and `... *FAIL  `)
sound, and is any row line able to escape both?
**Q2.**  Parse-before-score.  Is the RESULT / CONTROL / DONE gate complete?  Is a case missing (a probe that dies after
DONE; a DEAD vehicle; an interleaved stray line)?  Does `probe exit status` add anything given S1?
**Q3.**  Run it from its artifacts path (as proposed; `gate_sh_rounding.sh` does the same for
`artifacts/gdrompionull/gdrom_pio_null_probe.py`), or MOVE / COPY it to `regress/ip30_abort_probe.py`?  The ledger's witness
field and #531's records cite the artifacts path; a move would bring its docstring under section U; a copy makes two
files that can drift.  Which, and why?
**Q4.**  Run time and load.  ~9.5 minutes added to gate 14, wall-clock waits throughout (S1, S2).  Is the block comment's
disclosure accurate and enough?  Does anything bound gate 14's duration or the battery's (nightly_check's max age, a
scheduled-task limit) that 9.5 minutes could break?
**Q5.**  The floor for a WIRING round.  Are the four legs in section 4 the right ones?  Is a build WITHOUT the ip30 device
owed (the 2026-10-09 ruling lists it as a null medium "for a device round")?  Anything else the block must be shown to red on?
**Q6.**  Records.  What else must change in the same commit (the ledger rows `ip30abortkill` and `wiringcliff`, the probe's
MANIFEST text, `OUTSTANDING_BUGS.md`, a CHANGELOG block)?  Should `ip30abortkill` -- `in work` since #531 with this wiring as
its last named debt -- CLOSE in this commit, or in a separate closure-records commit as #527's rows did?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q6.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
