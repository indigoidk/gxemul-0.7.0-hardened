FABLE_ADJ_C_20261016

Verbatim line from `GXEMUL-SEC/regress/artifacts/adj_20261016/cxctl_optionC/RECEIPT.txt` (its line 17):
`     note: 6 ERROR:-shaped line(s) in stderr IGNORED -- rc 0 with an answer, so they are quoted source`

VERDICT: UPHOLD WITH CHANGES (7 rulings changed: F1, F2, F4, F5, F6, F8, D2 refined; none overturned) -- the production
launcher rule stands and its empirical premise is now MEASURED (387 launch lines, zero off-diagonal), but F8 as written
would land a comment the peer's next commit silently reverts, F5 adopts one Astra correction that is false on both copies
on disk, F2(b) keys the legacy class on the one spelling my v1 objected to singling out, F6 drops Astra's N3 correction,
and the packet does not see the expired `ip30_abort_probe.py` exemption that reds precommit section R on every commit it
schedules.

Fable 5.1, 2026-10-16 ~12:0x CDT.  Self-review of RA (my 2026-10-13 adjudication); F1, F2 and F5 correct my own work and
are held to a harder standard below.  I did not read `adj_20261016/astra/` or `adj_20261016/grok/`.

---

## 0. Evidence basis

READ: the packet; RA v1 and v2 in full (`fable5_records_adjudication.md`, 277 lines); `astra_v2/codex_recadjv2.txt` in
full; `astra/codex_recadj.txt:140-219` (the #560/#561 per-entry assessments); `cxctl_optionC/{RECEIPT.txt,
cxlaunch_frozen.sh, fakecodex.sh, launcher.md5}`; every file in `agyprobe_rc/` and the 10-13 `agyprobe/`;
`prescreen/prescreen_records.md` -- **the version at 11:55:05, 918 lines / 105,780 bytes** (it was 151 lines when I
first opened it at ~11:29 and was still being appended by forks; any adjudicator who read it before ~11:55 ruled on a
fragment -- state the version you read); HEAD text via `git show e483d931:` for `tools/cxlaunch.sh`,
`tools/pipeline/gen_dashboard.py` (:40-80, :120-185, :250-270, :400-425), `tools/pipeline/seat_verdicts.py`
(:380-390, :462-482, :498-508, :524-536), `tools/pipeline/ledger.json` (:27110-27125, :29540-29575, :62410-62425,
:62483-62515), `OUTSTANDING_BUGS.md` (:22490-22526, :24708-24720), `tools/pipeline/check_probe_wiring.py:3097-3100`,
`tools/panel.sh:334-344`, `src/devices/dev_pcc2.c:375-379`, `src/disk/diskimage.c`, `src/cpus/cpu_sh.c`,
`src/devices/dev_sh4.c`; the working tree's `git status`, `git diff --stat` on the peer-dirty files,
`check_probe_wiring.py:3112-3115` and `:3956`; `exemptredate_20260925/final550/*`; `_scratchpad/codexpack_20260928/`
launcher copies (md5); `_scratchpad/agypack_20261013/agylaunch.sh` and `r2/r3/r4/`; `launcher_controls_20261013{,_v2}.txt`;
the agy install directory; `_scratchpad/panel_20260925_151610/codex.txt:1-18`; `_scratchpad/panel_20260918_180558/codex.txt`
(tail, `cat -v`); `_scratchpad/panel_20260911_103402/codex.txt` and `regress/artifacts/armbdt/panel_20260911/codex.txt`
at six line numbers; `est/` (top level).

MEASURED, receipts under `adj_20261016/fable5/meas_C/` (durable, nothing written elsewhere in the project):
- `launchlog_census.txt` -- every `codex rc=` line in the cxlaunch-family launch logs on disk: **362 rc=0 with
  non-empty stdout, 25 rc=1 with empty stdout, ZERO off-diagonal** (387 lines in 376 files).
- `ansi_census.txt` -- ANSI-coloured `ERROR:` diagnostics: **0 of 593** cxlaunch-family `codex_*.err`; **7 of 453**
  panel.sh `codex.txt` (all 2026-09-18..21).  The apparatus was tested on a file known to carry colour first, because my
  first pattern (`grep -P`) returned 0 on that very file -- `grep: -P supports only unibyte and UTF-8 locales` went to
  the stderr I had discarded.  A check that could not fail, caught by the carrier's own rule before it was cited.
- `okdomain_census.txt` -- on the HEAD ledger copy (`adj_20261013/ledger_HEAD.json`, md5 `db0b22a2` = `git show
  e483d931:tools/pipeline/ledger.json`): 5,150 entries; 3,170 explicit `d`; 1,773 glyphs; **1,397 explicit off-domain**
  = OK 439 + other 399 + N/A 253 + dates 128 + y 89 + HELD 31 + blank 29 + NOT-FIRED 22 + WALL 7 (reproduces Astra v2 and
  RA v2.3 exactly); kimi `OK` entries whose note or `ev` names the substitute: 18 under that loose criterion.
- `cxctl_fable/RECEIPT_fable.txt` (+ the three fixture stderr files) -- three boundary fixtures of my own against the
  frozen launcher (md5 `3c51a757...`, identical to `cxlaunch_pack.sh` and all 46 `cxlaunch_pack.run-*.sh` copies, so
  "the production rule" is one text): Q1 rc 1 / empty stdout / quoted refusal lines -> exit 7 REFUSED; Q2 rc 0 / empty
  stdout / the real wall text -> exit 8 WALLED; Q3 rc 1 / empty stdout / the wall text with ANSI colour on the `ERROR:`
  token -> **exit 6, "seat down, cause NOT established"** (the `^ERROR:` anchor does not see a coloured diagnostic).

REASONED items are labelled where they occur.

---

## 1. F1..F10 and D1..D2

**F1 -- REFINE (the rule stands; the record and controls change).**  ACCEPT the refutation of Option B (final550 verified:
rc 0, 4,265 b answer, six column-0 usage-limit lines at `.err:5625-5626, 5653-5654, 5891-5892` inside an `exec` block,
`astra550.launch.log` = `SEAT WALLED`); ACCEPT landing the production rule into `tools/cxlaunch.sh` with `ultra` and the
Daybreak fallback (HEAD's `:26-27` runs `max` and has no fallback; `cxlaunchdaybreak` :62410 files exactly that gap, so it
closes).  Four refinements:
(i) **the premise "every real wall and refusal is rc 1 with empty stdout" is now MEASURED, not quoted from the
launcher's comment** -- 387 launch lines, 25 rc=1 all empty, 362 rc=0 all non-empty, zero off-diagonal
(`meas_C/launchlog_census.txt`); cite it in the row.
(ii) **merge the prior filing.**  `OUTSTANDING_BUGS.md:22494-22503` at HEAD, `cxlaunchwallfp` (LOW, harness, filed
2026-09-26), already names BOTH halves of this class -- final550's six quoted lines and #549's "quotation" -- with the fix
shape "key the stderr test on codex's own error block at the END of the stream".  It has no ledger row, and neither RA
v1/v2, Astra v1/v2, nor the packet cites it (the prescreen found it).  `cxlaunchquotation` (:62483) covers only the stdout
half.  The landing commit closes BOTH, and its record must say why the filed tail shape was not the one built: the rc /
empty-stdout rule was measured (six fixtures, 387 launches) and closes the same instance; the tail rule has a filed
warrant but no measurement.  That is also the honest form of D1's "no warrant" sentence -- see D1.
(iii) **strip ANSI before the `^ERROR:` anchor** -- a one-line `sed`, control Q3 (RED today: exit 6; must read WALLED,
exit 8).  Warrant: seven real panel.sh `codex.txt` files (2026-09-18..21) carry `ESC[1mESC[31mERROR:ESC[0m` diagnostics
under the SAME `> file 2>&1` redirect shape panel.sh uses (`panel.sh:337-339` at HEAD), and v3 `seat_verdicts.py`
already strips ANSI for the same reason (measured on five of them, RA v2.1).  Zero of 593 launcher `.err` files carry it,
so if the coordinator declines the edit as an addition without a launcher instance, record Q3 beside N4 as a disclosed
residual -- it mislabels a wall as "seat down" and never credits an answer, so the cost is a wrong re-fire schedule, not a
laundered run.
(iv) **the N4 residual's cost is a lost answer on re-fire** (REASONED): exit 8 leaves `codex_<tag>.txt` in place and a
re-fire with the same tag overwrites it.  Recommend renaming on exit 8 to `codex_<tag>.walled.{txt,err}`, as the refusal
branch already does at `:82`.  Not a ruling; one line.
Rewrite HEAD `:41` ("stdout ... may be grepped freely") with the fix: it is the premise being corrected.
OUTSTANDING_BUGS.md:24714-24716 and ledger :62489 prescribe Option A -- correct both to the landed rule (L4), and
correct my RA v2.2 `:232` ("correct both to B") by reference.

**F2 -- REFINE (accept the withdrawal; change the key of (b)).**  ACCEPT: every mechanical sweep is withdrawn.  Astra's
three counterexamples verified at HEAD (`wdcatapistswap/review/deepseek` `d: OK`, outcome `REJECT-AS-WRITTEN`, grade
CONFIRMED, :29546-29553; `glm` `BURNED-THEN-ANSWERED-ON-REFIRE` :29556-29563; `wdcdataoutdrain/research/kimi` `d: OK`,
outcome UNVERIFIED, :27114-27121), and my v2.3 "262 / 177" does not reproduce.  (a) and (d) stand.  (c) stands with
Astra's four conditions.  (b) is right in what it asserts and wrong in what it keys on -- ruled under D2.

**F3 -- UPHOLD.**  `agyprobe_rc/bogus.rc`, `bogus_v2.rc`, `bogus2.rc` each read `rc=1`; `.out` files 0 b; the two
diagnostics on stderr; agy 1.4.0 (`version.txt`); MANIFEST.md5 present.  The claim now stands on a receipt.

**F4 -- REFINE (file it; add a serial pre-flight).**  The evidence holds by reading the install directory:
`agy.exe` 2026-10-16 11:21:27, `agy.exe.1792167684245670300.old` 2026-10-13 22:33:37 -- and the `.old` suffix is a
Unix nanosecond stamp that decodes to 2026-10-16 16:21:24 UTC = 11:21:24 CDT, one second after the first probe
(`probe_time.txt` 11:21:23), so the swap is timed, not inferred.  `bogus2.APPARATUS_FAIL.rc` = `rc=127`,
`..._during_selfupdate.err` = `timeout: failed to run command 'agy': No such file or directory`.  One race, observed
once, but its mechanism is read off the filesystem.  FILE `agyselfupdate`, severity low, UPHELD.  Refinement: the current
`agylaunch.sh` (22:53:02) already runs `agy models` per job as a pre-flight (`:28`), and a per-job pre-flight fired
three-at-a-time can itself race the swap.  Run ONE `agy models` (or `agy --version`) SERIALLY in the pack runner before
the concurrent launches, then treat rc 127 + "No such file" as LAUNCH FAILURE re-fired once -- with the negative control
the carrier owes every re-fire rule: a job that answered is NOT re-fired.

**F5 -- REFINE (five of six accepted; one Astra correction REJECTED; one sharpened).**
- C3 is 19 bytes: TRUE (`launcherctl/c3.txt`, 19 b).  Accept.
- Seven controls, six after C3's withdrawal: TRUE by reading v2.4's table.  Accept.
- **armbdt lines "5805/6215/6355, not 5796/6206/6346": FALSE on both copies on disk.**  `_scratchpad/panel_20260911_103402/
  codex.txt` AND `regress/artifacts/armbdt/panel_20260911/codex.txt`: `:5796` is `VERDICT: NOT RATIFIED ...`, `:6206`
  and `:6346` are the bare `codex` headers; `:5805`, `:6215`, `:6355` are body lines (a mask sentence, a PPC `if`, a
  `#524` table row).  RA v2.1's numbers stand.  Astra could not run bash and its reader counted differently (cause not
  established); the packet adopted the correction unchecked, and so would I have -- **a correction is not safer than the
  thing it corrects**, and this one cost one `sed -n` to test.  Reject.
- "none was found when it was written": SHARPEN.  By mtime: my control run `launcherctl/ctl_receipt.txt` 21:44:38; the
  durable receipt `agypack_20261013/launcher_controls_20261013.txt` 22:06:57; Astra v1 answered on the v1 text at
  22:22:08.  So the durable receipt existed BEFORE v1 was finalised, and v1's "NO receipt anywhere" was false when
  written -- it was true at 21:44, when the check was made, and the text did not re-check.  Record: "none existed at
  21:44 when the control was run; a durable receipt was written at 22:06:57, before this text was finalised, and was not
  re-checked."  That is harder on my record than either wording in the packet, and it is what the mtimes say.
- 48/49 by reading only: accept; the `stagetokenscontrols` commit's control run supplies the receipt.
- 11 kimi-substitute entries: accept Astra's 11 WITH ITS CRITERION (the substitute answered; the eleven are named in
  Astra v2 :121).  My loose criterion (note or `ev` names kimi-k3/substitute) gives 18 (`meas_C/okdomain_census.txt`);
  the seven extra are entries where the substitute stalled or the CLI walled.  A count names its criterion or it is a
  correlate -- the carrier's counts rule, landing on my own v2.3 "7".

**F6 -- REFINE (accept; carry Astra's N3 correction into the filing).**  v3 is supported (53 class changes, every one
read; Astra v2 confirms).  The row is ABSENT at HEAD and in the working tree (grep 0 / 0) -- FILE it.  Two things the
packet's F6 drops from Astra v2 item 3: (i) N3's explanation in RA v2.1 is wrong -- the wall phrase is inside the
4,000-char window; what suppresses the wall class is `:469`'s `and not v` (verified at HEAD), i.e. a recognised verdict,
not position; (ii) the synthetic verdict-less kimi answer that quotes the 284-byte notice scores WALLED under v3.  That
is the STRONG-phrase class's standing behaviour since 2026-08-23 for every verdict-less file, which the kimi phrase
joins; disclose it in the row with the fixture as a documented non-control (no such file exists on disk: 37 files carry
the phrase, all the identical 284-byte wall).  Also carry Astra's census corrections (51 anchored / 47 terminal / 4
non-terminal with ANSI stripping; 14 anchored quotations in `panel_20260919_015846/kimi.txt`, not 6) and the eight
invocations / fifteen files / nine byte-distinct versions.

**F7 -- UPHOLD.**  `HARVEST.md:109` names `wdczerolendatain` a NEW FILING; absent at HEAD and in the working tree
(0 / 0).  FILE.

**F8 -- REFINE (the edit list stands; the mechanics as written would be reverted by the peer).**  RA §3's 37 and Astra
v1's per-entry assessments (:189-203: every replacement TRUE, four halves UNCHECKABLE there -- place 2's hardware
warrant, place 29's 10/10, place 39's documentary attribution, place 40's historical implementation -- which the
replacement text must not assert beyond its receipt) are the edit list.  HEAD has not moved (e483d931).  Verified:
`dev_pcc2.c` +20 and `cpu_alpha_palcode.c` +23 lines dirty vs HEAD (peer), `tools/panel.sh` +41/-9;
`dev_pcc2.c:377-378` still carries the old sentence.  **But "land the comment on HEAD's copy, never the working file" gets
the trap backwards** (REASONED from ordinary git semantics): a commit staged from HEAD blob + comment leaves the working
file (peer's edits, no comment) differing from the new HEAD by the peer's hunks AND the comment's absence; the peer's
next `git add src/devices/dev_pcc2.c` then commits the comment's REMOVAL inside a product commit, silently.  The right
mechanics: apply the comment hunk to BOTH the index (`git apply --cached <hunk>`) and the working file (`git apply
<hunk>`; comment-only, it cannot conflict with the peer's hunks), then check `git diff HEAD -- <file>` shows only the
peer's hunks after the commit -- or hold those two files behind the peer.  Same for `cpu_alpha_palcode.c`.  Two more
items fold in from the prescreen, both verified: E53 -- place14's NEW text cites `OUTSTANDING_BUGS.md:14809-14812`, and
that paragraph is at `:14821` at HEAD (re-key to the sentence before applying); E54 -- `est/` has NO `regress/`
directory, so `regress/diff_ieee_store.c` and `ppc_rldicl_probe.py` owe est/ nothing -- an erratum to my own RA v2.6
(`:271`) and to HV:226 (see §5).  The diff_ieee_store.c identity guard (precommit E) in the same commit: UPHELD; "or
exempt" stays withdrawn.  The two `panel.sh` items stay HELD.  And see §3 item 1: no commit in this plan passes
precommit until the expired exemption is handled.

**F9 -- UPHOLD, with one owner-less remedy named.**  Astra's table reproduces against the files I opened (mechanism
lines :365/:475-477/:530; "twice" correctly withdrawn; Thumb exits `memory_arm.c:79`/`:254`; regress/ edits outside the
`src/*` propagation population; "or exempt" withdrawn).  The one thing F9 accepts without an owner: the deepseek
712-byte overruling's REMEDY (a verdict-token branch for short files in `panel.sh:459/:708` and
`check_seats_read.py` MIN_ANSWER, with the 712-byte file as positive control and a short echoed-brief-plus-error file as
negative) is filed NOWHERE -- `grep MIN_ANSWER\|712-byte` is 0 in the working-tree ledger and 0 in OUTSTANDING_BUGS.md
at HEAD and in the tree.  Astra v2 says it "still needs execution before shipping"; nothing schedules it.  FILE it.

**F10 -- UPHOLD (not adjudicable here).**  Add, for the owner's packet, the prescreen's new evidence on the D2 draft
(CD5-CD8: the 32769/32767 rows come from the 137-row extension, "`< 97` detected at 96" is derived not scored, §C7's
`> B-1` is the EQUIVALENT mutant at a clamp, "every one-token move" overclaims four measured moves) and on ROUTE PARITY
(CD10, CD13: the two recorded route bounds differ -- enclosing function vs block/file).  Read by me in the prescreen;
not re-derived.

**D1 -- UPHOLD the ruling; correct its reason.**  Land the rule as measured; record N4 as the residual; do not add the
tail-only read.  But the "addition licence" sentence is misapplied: the tail rule is not an addition without warrant --
it is the FILED fix shape of `cxlaunchwallfp` (2026-09-26), minted from a real instance (final550).  The honest reason
to prefer the rc / empty-stdout rule is that it is MEASURED (six fixtures; 387 launches with zero off-diagonal; three
weeks of Astra jobs) and closes the same instance, while the tail rule is unmeasured.  Is the residual acceptable?  Yes:
N4 is a shape with zero instances in 387 launches, and under it the launcher mislabels, it does not credit.  Record it
with its re-fire cost (F1 iv).  The fake-codex caveat is right and stays: the real codex's exit status in a mid-answer
wall is measured nowhere, and nothing here changes that.

**D2 -- REFINE: adopt (b) keyed on the DOMAIN, not on the spelling "OK".**  The packet asks whether (b) repeats my v1
mistake.  In what it ASSERTS, no -- "legacy" asserts nothing, where `"ok"` asserted approval.  In what it KEYS ON, yes --
it singles out one spelling, which was the v1 objection's first half, and it leaves the other **958** explicit off-domain
values (69% of the 1,397; measured on the HEAD ledger) in the `pend` class whose legend reads "no answer / seat failure
(not agreement)" -- the row's own complaint, still true for two thirds of the population after the fix.  The same edit
fixes all 1,397: at `gen_dashboard.py:161`, `cls = D_CLASS.get(d) or ("legacy" if "d" in ent else "pend")` (the cell
already prints the raw `d` text at `:178`, so nothing is hidden); the legend gains one line -- "a pre-domain value: not a
verdict glyph; neither approval nor failure; hover for its text"; and the strip (`:407`) prints a FIFTH number, the
off-domain count, so the five numbers sum to the entry total (today 3,753 + 1,397 = 5,150; `summary()` at `:258-262`
already counts every `d`).  Do not write "unread" into the class name: for OK it is true of 177 and false of the four I
read, and for `N/A`/`y`/dates it asserts something about the reader that nobody measured.  (c)'s domain check then
refuses NEW off-domain values after the cutoff, which is what stops the spelling from being canonised; (b)-general is a
rendering of the past, (c) is the rule for the future, and neither needs a per-entry read.  Controls: the existing
`t_okclass` DASH fixture (`d="OK"`, explicit, so a sweep cannot touch it -- RA v2.3) now asserts class `legacy`; add
one fixture with `d="N/A"` asserting the same class (the control that rejects the spelling-keyed form); the four glyph
fixtures stay green; mutant: the `"d" in ent` test removed must red the N/A row.

---

## 2. WHICH OF THE TEN ACCEPTED DISPOSITIONS IS WRONG?

**F8**, in its execution clause.  "Land the comment on HEAD's copy, never the working file" produces a records commit
that the peer's next commit of `dev_pcc2.c` or `cpu_alpha_palcode.c` reverts without anyone noticing -- the propagation
rule's failure mode inside the working tree.  The edit list is right; the procedure is reversed (apply to both, or hold).
And no commit in F8's plan -- nor F1's, F6's or F7's -- passes `precommit_check.sh` today, because section R reds on the
expired `ip30_abort_probe.py` exemption (§3 item 1), which the packet does not mention.

Second: **F5** accepts a correction that is false on both copies on disk (the armbdt lines).  Third, weaker: **F2(b)**
keys on the spelling; **F6** drops a correction the packet's own source made.

"I accepted all ten" was the right thing to be suspicious of: three of the ten carry a defect, and all three are of the
kind that a correction inherits from the thing it corrects.

---

## 3. WHAT DID ALL OF US MISS?

1. **The expired exemption blocks every commit this packet schedules.**  `tools/pipeline/check_probe_wiring.py` carries
   `"artifacts/ip30abortkill/ip30_abort_probe.py": ("2026-10-15", ...)` at HEAD `:3097-3098` and in the working tree
   `:3112-3113`; the test is `elif d < today:` (`:3956`), `today` defaults to `date.today()`, and precommit section R runs
   the checker with no `--today` (`precommit_check.sh:546`).  Today is 2026-10-16.  REASONED from those three lines (I
   did not run the checker); found by the prescreen (PW6), absent from the packet.  Re-date it with a reason, or wire the
   probe, BEFORE the F1 landing, the F6/F7 filings and the F8 records commit.  Next cliffs: 10-22 (ppc_rldicl,
   alpha_tbi), 10-23 (lca_badval), 10-26, 10-27.
2. **`cxlaunchwallfp` (OB 2026-09-26) is the prior filing of F1's whole class**, names the tail-rule fix shape D1 debates,
   has no ledger row, and is cited by none of RA v1/v2, Astra v1/v2 or the packet.  The row the packet closes
   (`cxlaunchquotation`) covers the stdout half only.  Close both; say why the filed shape was not the one built.
3. **F8's mechanics revert under the peer's next commit** (§2).
4. **The 712-byte remedy has no owner** (F9).
5. **Astra's armbdt line correction is false on both copies** and was adopted unchecked (F5).
6. **`est/` has no `regress/`.**  RA v2.6 `:271` ("the `regress/` edits owe est/ byte-identity under the shared-file
   rule only") and HV:226 are wrong; the prescreen's E54 is right.  Erratum to my own record, §5.
7. **The `^ERROR:` anchor is blind to coloured diagnostics, and the shape is real**: 7 of 453 panel.sh `codex.txt`
   files (2026-09-18..21) carry `ESC[1mESC[31mERROR:` under a plain file redirect; 0 of 593 launcher `.err` files do.
   Under the production rule a coloured wall reads "seat down, cause NOT established" (Q3, measured: exit 6).  Why the
   seven got colour under the same redirect shape is NOT established (a CLI-version window is a guess).
8. **Both production launchers are untracked scratchpad files.**  F1 lands `cxlaunch_pack.sh` into `tools/`; the agy
   launcher (`_scratchpad/agypack_20261013/agylaunch.sh`, with the v2.4 stderr-only gate and the `agy models` pre-flight
   applied at 22:53:02 and receipted at 22:53:05) owes the same landing, and nothing files it.
9. **The prescreen was a growing file during the adjudication window** -- 151 lines at ~11:29, 918 at 11:55.  A ruling
   on "its LIVE list" without the version read is a ruling on an unknown denominator.
10. **A seat-coverage count without its criterion is a correlate**: 7 (v2.3), 11 (Astra), 18 (my loose grep) are all
    "the kimi-substitute OK entries".

---

## 4. The prescreen's LIVE list (version of 11:55:05, 918 lines; 93 LIVE)

Rulings by group.  Where one grep settled it, I ran the grep; the rest are READ from the prescreen's evidence column and
marked so.

**Time-bound.**  PW6 -- UPHOLD, URGENT; verified (§3 item 1).  Handle before any commit.

**Held specs with new evidence.**  CX3 -- UPHOLD: this IS F1's rule; HEAD `:56` decides the wall before `:58` tests rc
(verified).  SV11 -- UPHOLD as a FILING: `panel.sh:568` token-greps the whole file and `:708-709` count `ok` at >= 800 b
(prescreen READ; HEAD `panel.sh` has 0 hits for `flagged`); v3 fixes `seat_verdicts.py` only.  File a `panel.sh` sibling
of `seatverdictrefusal` carrying the terminal-refusal test; the edit waits on the panel.sh hold, the filing does not.
Until then, record in the row that `SEATS.txt` is not a refusal authority.

**Fix specs never adjudicated (AR1-AR6, AR10, AR13-AR17, HF1-HF4, HF7-HF9, PW1-PW3, PW5 -- 22 items).**  CANNOT SETTLE
HERE, by design: each needs its drafts inlined and, for most, a run (HF5's seven exit-status runs; PW1/PW2's unexecuted
diffs; AR10's control).  Two facts the adjudicating pass should start from, both verified or one-step: HF2 -- the battery
runs as uid 0, so a chmod RED control cannot redden and the RED control must be a grep-status-2 stand-in (prescreen READ
of `id -u`); AR17 -- a SessionStart hook that `exit 2`s before emitting its JSON loses the panel-directive reinjection
exactly when the alert fires (REASONED; alert on stderr, keep the JSON).  Carry PW5 to the recorded HIGH-severity rule
question; do not file it twice.

**Owner rule questions (CD5-CD8, CD10, CD13).**  Not adjudicable here; appended to F10 above.

**Rulings asked for.**  PS3 (+PS2, PS4) -- UPHOLD the annotation form: the `pass2_ledger.tsv` seat columns are free
text (81 six-field rows, 49 three-field, no seat cells after 2026-08-31); annotate the header, no retro-fill, and add
"an answer count" beside `:93`'s `7of9`.  BN3 -- UPHOLD: ticked lines under "### OPEN" violate OB:14's own charter;
remove them (the charter is the older rule and nobody proposed amending it).  BN7 -- UPHOLD the qualifier ("none in
`src/`"); the commit message stands as history.  NC7 -- CANNOT SETTLE without reading `mutate_altdigin.py`; the 10-09
clause-(c) block admits "a build WITHOUT the device" for a device round, and a read stub is not that -- the burden is on
the artifact to say which admitted medium it is, else an L4.  NC8 -- UPHOLD the L4 (channel controls are not a null
product medium under the 10-09 block); peer-owned.

**Records corrections (L4 class, 55 items).**  UPHOLD as a class, with these checks: CC1 (`diskimage.c:1879` is the
prefix guard -- verified), CC14 (`cpu_sh.c`'s only `exit(1)` calls are `:101` and `:1085` -- verified; "sits in the
assert path" is stale), CC16 (`cpu_sh.c:458` cites `dev_sh4.c:2386-2388`; HEAD `:2386` is `case SH4_RTCOR:`, the IRLM
refusal is around `:2501-2509` -- verified; a src comment fix owes four-tree propagation and the two-part clearance),
E53 (verified, folded into F8), E54 (verified, §5), DA13 (`run_controls.py:16-17` says "48/48 ... scratchpad
fable534/drive_fable.out" on a 49-row instrument -- verified; annotate as measured on a 48-row instrument with a
non-durable log).  The remaining carrier citations (CC2, CC4-CC13, CC15), the decayed counts (CN2-CN4, CN6, CN7, CN12,
CN17: FILE per the counts rule, no sweep), the PDF inventory (CN13-CN16, CD22: 20 top-level, 26 with `lance/`; `ata2`
cited by `dev_wdc.c:640` and listed nowhere), CD17/CD19/CD21, BN2/BN4/BN5/BN8/BN9/BN11, PC1/PC2/PC3/PC6/PC9/PC10,
AR7/AR14, PS5/PS6, NL6/NL7, CX15 -- READ from the prescreen, not re-derived; UPHOLD each as an L4 to land where its file
is next touched, and PC2 (a live `[HELD AWAITING SEAT ...]` literal at :42749) now, since three tools read that literal.
NC1/NC12 -- UPHOLD adopting the 87-directory census with a written deriver at a durable path; NC4 -- UPHOLD the one L4,
peer-owned.

**CANNOT SETTLE (prescreen's own two).**  HF5 and PC4 -- agree; each names its one settling action.

**The prescreen's two owed filings** -- `seatverdictrefusal` and `wdczerolendatain` ABSENT at HEAD and WT (verified
0/0): F6 and F7.

---

## 5. Errata to my own record (RA), in place by reference

- v2.1 N3's explanation: the verdict (`:469 and not v`) suppresses the wall class, not the window (Astra v2; verified).
- v2.1 "0 verdict values": 0 verdict-ONLY changes; v3 clears 15 verdict fields with the refusal reclassifications.
- v2.1 `sv_v2` is not "Parts A+B" (Astra v2 :84): rename the intermediate candidate.
- v2.1 census: 51 anchored / 47 terminal / 4 non-terminal with ANSI stripping; the saved manifest omits the five ANSI
  files; 14 anchored quotations in kimi `015846`; "34 files" is stale (37 / 18 + 19).
- v2.3 "262 / 177": does not reproduce (272 / 167, and the subset is not semantically safe); withdrawn.
- v2.3 "7 covered-by-substitute": 11 under Astra's criterion, stated.
- v2.4 / v1 §6 item 3 "no receipt anywhere was true when written": false when written; see F5.
- v2.6 `:271` "regress/ edits owe est/ byte-identity under the shared-file rule only": FALSE -- `est/` has no
  `regress/` (verified by `ls`).  regress/ edits owe precommit E only.  HV:226 carries the same error.
- v2.6 "C3 20 bytes": 19.  "the launcher table has six fixtures": seven controls, six after C3's withdrawal.
- v2.1's armbdt lines 5796 / 6206 / 6346: STAND (both copies verified); the packet's F5 correction of them is rejected.
- v1 §3 / F8: "never the working file" was the packet's wording, not mine, but my §3 said nothing about the peer-dirty
  mechanics at all; the apply-to-both procedure above is the missing half.

---

Receipts (all under `GXEMUL-SEC/regress/artifacts/adj_20261016/fable5/meas_C/`, durable): `launchlog_census.txt`,
`ansi_census.txt`, `okdomain_census.txt`, `cxctl_fable/RECEIPT_fable.txt`, `cxctl_fable/Q1.stderr`, `Q2.stderr`,
`Q3.stderr`.  The fixture scripts and the frozen launcher copy I drove live in my session scratchpad
(`.../scratchpad/fable_adjC/`), volatile; the launcher's md5 (`3c51a7579065c5e6bebd5fd59d32b3ed`) is in the receipt.
Nothing else was written to any project tree.
