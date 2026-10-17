FABLE_CXLANDV5_20261017
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: SHIP WITH CHANGES (5)

**Evidence basis.**  Fable 5.1 (claude-fable-5-1), the v5 pass, 2026-10-17 04:1x-05:0x.  READ: the whole packet (1,354
lines); `tools/cxlaunch.sh` on disk (md5 `af18158e` = the packet's; its v3 -> final diff is **0 non-comment lines**,
MEASURED by `diff` of the two files with `^ *#` lines removed, and v4 -> final likewise 0); `run_controls_v5.sh` (`12effca6`),
`mut_launcher_v5.py`, `run_mutants_v5.sh`, `CENSUS_v5.txt`, the fixtures, the tracked (`cb180d9d`) and before (`3c51a757`)
launchers, `_scratchpad/codexpack_20260928/run_pack_body.sh` whole, and my own v4 answer and measurements.  MEASURED, in a
mirror of the relative layout under my session scratchpad (`...\scratchpad\cxv5\root\`, nothing written to any project tree
but this file): the v5 base controls on the three columns (**224/224**, md5s identical, 0 `NO`, sentinel, exit 0);
TWENTY-ONE one-edit mutants of my own through the 224 controls' after column (every run carrying `CXLAND_CONTROLS_DONE`
and the 94 denominator); an extended copy of the controls (`run_controls_v5x.sh`: +7 rows, +4 checks, 249 checks) on the
three launchers and on the 11 mutants it is meant to kill; the landed launcher on a MISSING and on a RELATIVE brief; the
locale behaviour of `.` and `wc -m`; a census of my own over the `.err` files on record.  NOT re-run: the 105-mutant
table -- the main loop's re-run on `af18158e` (started 04:04:22, controls `12effca6`) was in flight for the whole pass; its
105 lines in the packet were checked BY READING each red set against the mechanism its line names.  Every scratch receipt
is at a VOLATILE path (`...\scratchpad\cxv5\out\base.out`, `out\basex.out`, `out\SUMMARY.txt`, `outx\SUMMARY.txt`,
`out\m_*.out`, `outx\m_*.out`, `mut\*.sh`, `mkmut5.py`, `snip_*.sh`, `root\...\run_controls_v5x.sh`); every number is
reproduced here and every mutant is given as its exact edit, so the main loop can re-derive each from this file alone.

## 0. The answer in one paragraph

The v5 CONTRACT is derived from the file, as it claims, and it is a far better record than v4's.  Of the **53 decision
constructs** I read off the executable lines, every one is EITHER listed with a row that straddles its edge OR disclosed
with a true reason -- except four groups, none of them a floor breach, each with a MEASURED one-edit escape of all 224:
(1) the override VALUES -- `CX_EFFORT`, `CX_AUP_EFFORT`, a non-empty `CX_AUP_MODEL` -- six mutants pass; (2) the
redirections' TRUNCATE semantics (`>` vs `>>`) -- two pass, and the pack runner RETRIES a 5 or a 6 into the same out dir,
so the shape is production's; (3) synthetic constant edges that the CONTRACT's own pin-the-constant reason demands and it
does not pin -- a bare `ESC[m`, `mkdir`'s `-p`, the `model:` label's case, the identity compare's case, `wc -m`, and four
display-or-equivalent edits -- ten pass; (4) U21's disclosure is a WRONG RECORD about the launcher: on a missing or
relative brief it calls codex with an EMPTY brief argument and, when codex answers, reports `seat answered` at exit 0
(MEASURED with the fake); the incident's exit 1 was codex's, not the launcher's.  Eleven of the eighteen valid escapes are
killed by five rows/checks I built and measured (OV, SO, NP, ESCM, LOG2); the other eight are equivalents to disclose.
On U7 I rule AGAINST my v4 position: PIN, DISCLOSE withdrawn -- with one condition, that the CONTRACT state the BOUNDARY of
what it pins synthetically, because the reason it gives demands the rows in (3).  **Zero floor breaches**, on a denominator
of 53 constructs, 21 mutants built (2 invalid, my own quoting error, recorded) and 105 table lines read.  The five changes
are rows and records, not launcher code; the chain CLOSES on this pass if the adjudication grades (1)-(4) as I do (L4 record
defects, repaired by rows and sentences), and the row additions owe the kill-table re-run with the new mutants in
`mut_launcher_v5.py` -- a scoped verification, not another panel.

## 1. Q1 -- my own v4 findings: is the disposition right, AND is the fix right?

I raised U1-U7, U11, U12 (with others) and U20.  For each, READ against the file and the kill table's red sets, MEASURED
where cheap:

| U | the fix | does the named row go red under the named mutant FOR THE REASON NAMED? |
|---|---|---|
| U1 | RC1A (rc 1 + answer + clean header -> 1), RC3A (rc 3 -> 3) | YES.  `m_rcpass` (`if false`): RC1A 0 want 1, RC3A 0 want 3 -- the pass-through deleted.  `m_rcgt1`: RC1A 0, RC3A still 3 -- the edge below 2.  `m_rcone` (`exit 1`): RC3A 1 want 3 -- the RAW rc.  RC3A is what makes "otherwise codex's own nonzero rc" a claim about the VALUE, not merely non-zero |
| U2 | D5 (P2 asked ON Daybreak, fallback on: 7, ONE call) | YES.  `m_samemodel` leaves the exit at 7 and makes TWO calls; the kill is the `D5  after` content check (call count), which the driver reads because it parses any `after` line.  The exit row alone would NOT kill it -- the content check is load-bearing, and it exists |
| U3 | FD (56 rows that set `CX_AUP_MODEL` empty: exactly one call each) | YES, both mutants: `m_aupcolon` (`:-`) makes the empty override mean Daybreak, `m_noempty` drops `-n`; under each every refusal row with the override empty fires the fallback (`-m ""` under the second): 2 calls -> `fbad`.  Population re-derived: 8 rows leave it unset (D1 D2 D3 D4 D5 FB1 FB2 EO, `grep -vc 'CX_AUP_MODEL='` over the 65 `three` lines), 57 set it empty, X15 excluded by the `!= X15` clause (it never reaches codex) -> 56 = NFD |
| U4 | CH (`head -12 fx/R2.stderr`, the real coloured block, asked gpt-6-other -> 5; log names gpt-6-astra) | YES.  Unstripped, `ESC[1mmodel:ESC[0m gpt-6-astra` is not `^model:` -> RAN empty -> UNVERIFIED -> 0 (want 5) AND the content grep "codex's header says gpt-6-astra" misses.  Both reds are the HEADER-path strip, which `m_nostrip`'s A1/Q3/R2X/D3 kills (all rc 1, all through `CXERR`) never tested -- the v4 point exactly.  The row is REAL (R2 is byte-identical to the 2026-09-19 refusal file, cmp'd on the v4 pass) |
| U5 | SI (every run fed a marker on stdin; the fake writes `head -c 60` of ITS stdin; none may be non-empty) | YES: `m_nostdin` lets the fake inherit the marker -> `sbad`.  It pins "codex does not inherit the launcher's stdin", which is the decision |
| U6 | N1F (out dir holds exactly `codex_N1.txt` + `.err`, byte-for-byte) | YES for `m_txtname`, `m_errname`, `m_swapio`; `m_nomkdir` (4/94) is killed by N1 and 71 others because without the dir no redirect succeeds and E0 reports the fake unreached.  But N1F does NOT straddle the redirections' TRUNCATE edge -- section 2, group (2) |
| U7 | PINNED against my DISCLOSE | ruled in section 5: PIN upheld, my v4 position withdrawn, a boundary demanded |
| U11 | RW, RI, WI, EM, IR + P1, P2, X1 for the ten adjacent pairs | YES, each pair READ against its mutant: `m_ord_wr` RW (8 not 7); `m_ord_re` P2 (6 not 7, plus every refusal row, all rc 1 and empty); `m_ord_ri` RI (5 not 7); `m_ord_rc` P2 (1 not 7); `m_ord_we` P1 (6 not 8); `m_ord_wi` WI (5 not 8); `m_ord_wc` P1 (1 not 8); `m_ord_ei` EM (5 not 6); `m_ord_ec` X1 (1 not 6) and IR; `m_ord_ic` IR (1 not 5).  All ten orderings pinned; the three borrowed rows (P1, P2, X1) carry the right joint shape |
| U12 | WS (`model:<TAB><SP><SP>gpt-6-astra<SP><CR>` verifies), BA, CWD; `\|\| exit 9` disclosed | YES.  `m_trailws` leaves `gpt-6-astra <CR>` -> 5 and WMT red; `m_leadws` (`: ` only) leaves `<TAB><SP>gpt-6-astra` -> 5.  BA: under `m_bannerun` the `> OpenAI Codex v0.1` line is a banner, its `--------` the first rule, `model: gpt-6-other` read -> 0 want 5; under `m_rule1h`/`m_close2h` the pre-banner rule is consumed -> 0 want 5.  CWD: `m_cd` -> the fake's `pwd` is `$T/home` -> `cbad` |
| U20 | the five record corrections | READ: all five applied as described (section 4 re-checks each) |

Harder on the fixes than on the findings: the one thing I would change in my own v4 rows is F7/U7 (section 5).  Nothing
else of mine was fixed wrongly.

## 2. Q2 -- the enumeration: every decision of `tools/cxlaunch.sh`, by construct, against the CONTRACT

Method: the executable lines (79-181 of the packet's listing) read construct by construct -- each `if`, `[ ]`, `&&`/`||`,
`grep` flag, `sed`/`awk` expression, redirection, `exit`, constant and default -- and for each asked "which of the 224 checks
reds if this changes"; where reading could not settle it, the cheapest one-edit mutant was BUILT and RUN through the 224
(after column, 94 checks each; every run to its sentinel).  **53 constructs.**  `MEAS` = a mutant was run.

| # | line | construct | CONTRACT | my check |
|---|---|---|---|---|
| 1 | 79 | `set -u` | NOT PINNED, reason given | agreed: `m_nounsetu` (`: set -u`) MEAS 94/94.  One sharpening: it is not only "reached by a missing positional" -- it is what makes `m_noinit` die (an unbound `$refus` in the rc-0 branch); without it that mutant's `[ "" -gt 0 ]` errors to false and behaves like the base.  Say "load-bearing for one kill" rather than "reached only by" |
| 2 | 80 | `BRIEF OUT TAG` roles | E1 (the brief's content), N1F (the names) | pinned |
| 3 | 81 | `PROJ` | CWD | pinned (a non-existent `PROJ` exits 9 everywhere) |
| 4 | 82 | `CODEX`: default path, `:-`, honoured | DP, EO, E0b | pinned, all three edges |
| 5 | 83 | `MODEL`: default, `:-`, honoured | E1, EO; honoured by the 8 rows that set `CX_MODEL` (M1 X5 X13 D5 CH EO BA R7B, grep) | pinned |
| 6 | 84 | `EFFORT`: default, `:-`, **honoured** | E1, EO; **honoured: nothing** | **`m_effortignore`** (`"${CX_EFFORT:-` -> `"${CX_EFFORTX:-`) **MEAS 94/94 ESCAPES** -- no row sets `CX_EFFORT` non-empty |
| 7 | 85 | `AUP_MODEL`: default, `-`, honoured (EMPTY), **honoured (a VALUE)** | E2, FD; **a non-empty override value: nothing** | **`m_aupmodelhard`** (`run_codex gpt-daybreak-blue-latest "$AUP_EFFORT"; classify`) and **`m_ansbyhard`** (`    ANSWERED_BY=gpt-daybreak-blue-latest`) **MEAS 94/94 each** -- no row sets `CX_AUP_MODEL` to another model |
| 8 | 86 | `AUP_EFFORT`: default, `:-`, **honoured** | E2, EO; **honoured: nothing** | **`m_aupeffignore`** (`CX_AUP_EFFORTX`), **`m_aupeffswap`** (`run_codex "$AUP_MODEL" "$EFFORT"; classify`), **`m_effortglobal`** (`-c model_reasoning_effort="$EFFORT"` for `"$2"`) **MEAS 94/94 each**.  Both efforts default to `ultra` and EO empties both, so they are indistinguishable on every row |
| 9 | 87 | `mkdir -p "$OUT"` | N1F (`m_nomkdir`) | `mkdir` pinned; **`-p` equivalent on the controls** (every out dir is fresh with an existing parent): `m_nop` (`mkdir "$OUT"`) MEAS 94/94.  Undisclosed |
| 10 | 88 | `TXT`, `ERR` names | N1F, D1R | pinned |
| 11 | 89 | `ESC` | every strip row | pinned |
| 12 | 91 | `sz=$(wc -c < "$BRIEF")` | X14/X15 (the cap) | the cap pinned at both edges.  `-c` -> `-m`: `m_wcm` MEAS 94/94 -- equivalent on ASCII briefs, and under the C locale this harness runs in (`LANG` unset: MEASURED `wc -m` of `ab`+U+2019 is 5, bytes; 3 under `LC_ALL=C.UTF-8`) equivalent on any brief.  **A MISSING brief is unhandled**: `sz` empty, line 93 prints `integer expression expected` and falls through, and codex is called -- group (4) |
| 13 | 92 | `echo brief bytes` | display | agreed |
| 14 | 93 | `-gt 30000`, `exit 9` | X14/X15 | pinned, status included |
| 15 | 95 | `cd "$PROJ" \|\| exit 9` | CWD; `\|\| exit 9` NOT PINNED | agreed |
| 16 | 97 | `strip_ansi`: `ESC\[`, `[0-9;]*`, `[A-Za-z]`, `g`, `2>/dev/null` | A1, Q3, R2X, CSI, CH; `m_sgr`, `m_strip_nog`, `m_strip_nosemi` | `[A-Za-z]` pinned by CSI's `ESC[2K`; `g` by A1; `;` by CSI.  **`*` -> `\{1,\}` (a bare `ESC[m`, a documented SGR reset)**: `m_stripplus` MEAS 94/94 -- equivalent on the controls, 0 on record (my census: 0 of 2,381 codex `.err` files carry `ESC[m`).  `2>/dev/null` dropped: `m_sedquiet` MEAS 94/94, display-level |
| 17 | 100-101 | the argument sequence | E1, E2, EO, DP, compared whole | pinned -- except that `"$2"` and `"$EFFORT"` coincide on every row (row 8) |
| 18 | 101 | `> "$TXT" 2> "$ERR" < /dev/null` | N1F (swap), SI (stdin) | streams and stdin pinned.  **TRUNCATION is not**: `m_appout` (`>> "$TXT"`) and `m_apperr` (`2>> "$ERR"`) **MEAS 94/94 each** -- every row's out dir is fresh.  The pack runner RETRIES a 5 or a 6 into the SAME `$ARTS/$art/$id` (run_pack_body.sh:65-66: `mkdir -p` then the launch, the launch log truncated by the runner, the `.txt`/`.err` left to the launcher), so a stale `.txt`/`.err` under the new run is production's shape; under `>>` the stale header is the one read and the stale answer the one a reader sees first |
| 19 | 102 | `rc=$?` | RC1A, RC3A, every rc row | pinned |
| 20 | 109 | the strip on the header | CH | pinned |
| 21 | 109 | `NR > 12 && h < 2 { exit }` | W12/W13, X13, `m_hlt1`/`m_hlt3` | pinned at both edges of the window and both forms of the guard |
| 22 | 110 | `h == 0 && /^OpenAI Codex/ { h = 1; next }` | HB, BA, every header row; `next` NOT PINNED (equivalent) | pinned; `/^OpenAI Codex v/` (a narrowing): `m_bannerv` MEAS 94/94, equivalent on the controls and on record (every banner on record is `OpenAI Codex v...`).  Same family as the disclosed `next` |
| 23 | 111 | `h == 1 && /^--------/ { h = 2; next }` | BA, R7A, M1 (`next`) | pinned.  The premise behind "nine dashes find no block anywhere" checked: the real rule lines of N1, R2 and X13's source are EXACTLY 8 dashes (`awk length` on the stripped files: 8 at lines 3/12, 3/12, 5/14) |
| 24 | 112 | `h == 2 && /^--------/ { exit }` | BA, R7B, NM | pinned; `exit` -> `h = 3; next`: `m_exith3` MEAS 94/94, equivalent by construction (nothing matches at h = 3) -- the edge that matters, `exit` vs `next`, is NM's |
| 25 | 113 | `h == 2 { if (++n > 30) exit; print }` | R7A, K30/K31, `m_capn`, `m_nocap`, `m_bodyh1` | pinned at both edges and both operator forms |
| 26 | 114 | `grep -m1 '^model:'` | TM, MA | pinned; **the label's CASE**: `m_modelcase` (`grep -m1 -i`) MEAS 94/94, equivalent on the controls, 0 on record (all 975 blocks match `^model:` by the census's own rule) |
| 27 | 114 | the two trims | WS | pinned (both) |
| 28 | 115 | the `codex rc=` line | LOG (N1) | the SHAPE pinned on a one-call run.  `asked: $1 / $2` -> `asked: $MODEL / $EFFORT`: `m_askedglobal` MEAS 94/94 -- LOG does not straddle the fallback's second line, which the launch-log censuses also parse |
| 29 | 116 | the `ran:` line | display | agreed |
| 30 | 138 | `CXERR`: strip, `grep -a '^ERROR:'` | X1, X8, A1/Q3/CSI | pinned |
| 31 | 139 | `verd` | display | agreed (no decision reads it; X2 pins that) |
| 32 | 140 | `body=$(wc -c < "$TXT")` | N3, X1, B1G, B1E | pinned (`-l` would red B1E: the 1-byte fixture has no newline) |
| 33 | 141 | `refus=0; wall=0` | `m_noinit` (via `set -u`) | pinned |
| 34 | 142 | the gate | N1, N2, X2, N4, RC2W, B1G, `m_gateand` | pinned at every edge |
| 35 | 143 | refusal alternatives x4, `-i` | P2, RF1-RF3, RFC | pinned.  **The `.` of `can.t` and `won.t` is a QUOTING device, not a pattern decision**: the pattern is single-quoted, an ASCII `'` cannot be written inside it, and `.` stands in for it.  I first read it as a curly-apostrophe wildcard and built `m_curly1`/`m_curly2` (`'` for `.`): MEASURED 3/94 each, every row `line 173: unexpected EOF` -- the edit breaks the quoting, the mutants are INVALID, and my premise was wrong (recorded as such).  The only narrowing that keeps the quoting is `'\''`, which nobody writes by accident, so there is no edge to pin.  Incidental, MEASURED: with `LANG` unset `.` is one BYTE, so `can.t` does not match `can’t` (U+2019, three bytes); under `LC_ALL=C.UTF-8` it does; 0 column-0 `ERROR:` lines on record carry U+2019 or any non-ASCII byte (my census, 1,076 lines).  Disclose the `.` as the quoting form; nothing owed |
| 36 | 144 | wall alternatives x4, `-i` | P1, WL1-WL3, WLC | pinned |
| 37 | 146-147 | the IGNORED note | display | agreed |
| 38 | 149 | `verdict-in-stdout` line | display | agreed |
| 39 | 153 | `ANSWERED_BY="$MODEL"` | N1V, M1 | pinned |
| 40 | 155 | the trigger's three conjuncts | D1-D5, FB1/FB2, FD | pinned, each conjunct |
| 41 | 156-157 | the excerpt | display | agreed |
| 42 | 158 | the two `mv -f` | D1R | pinned; `-f`: `m_mvnof` MEAS 94/94, equivalent (`mv` prompts only on a tty) |
| 43 | 159 | the AUP FALLBACK line | display | agreed |
| 44 | 160 | `run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify` | E2 (the model), D1/D4 (`classify` runs again) | pinned except the effort and the model VALUE (rows 7-8) |
| 45 | 161 | `ANSWERED_BY="$AUP_MODEL"` | D1, D2 (`m_ansby`) | pinned against `$MODEL`; not against the hardcoded constant (row 7) |
| 46 | 164-169 | refusal -> 7, `-gt 0`, the LOST phrase | P2, Q1, A1, D1, R2X, D4; PK | pinned |
| 47 | 170 | wall -> 8 | W1L, P1, N4 | pinned |
| 48 | 171 | empty -> 6, `-eq 0` | N3, X1, B1E | pinned |
| 49 | 172-175 | identity -> 5, `-n RAN` | M1 ... BA -> 5; M2 ... HB -> 0 | pinned; **the compare's CASE**: `m_identcase` (`[ "${RAN,,}" != "${ANSWERED_BY,,}" ]`) MEAS 94/94, equivalent on the controls, 0 on record |
| 50 | 176 | `rc -ne 0 -> exit rc` | RC1A, RC3A, IR | pinned |
| 51 | 177-181 | the final messages | PK, N1V, WMT, the UNVERIFIED rows | pinned |
| 52 | 164-176 | the ORDER, ten adjacent pairs | RW, P2, RI, P1, WI, EM, X1, IR | pinned (section 1, U11) |
| 53 | 155-162 | the fallback run's OTHER outcomes -- walled, empty, rc != 0 with an answer and another header | D1 (answer), D2 (wrong model), D4 (refused) | unrowed; the cascade is one code path on the LAST run's counts and D4 pins that `classify` re-runs.  No one-edit escape found by reasoning (a mutant must keep D1/D2/D4 green yet change a refused-then-walled run).  Rowed anyway in my extended controls as the composition's own receipt: DW (P2 then P1) 7/8/8, DE (P2 then N3) 7/6/6, DR (P2 then rc 1 + answer + another header) 7/1/5 -- all MEASURED as predicted, the before column firing the fallback and never comparing the model |

**Decisions MISSING from the CONTRACT or listed with a row that does not straddle their edge** -- the exact mutant, what
it passes, the property it breaks.  All MEASURED (94/94 = passes every after-column check):

| group | mutants (exact edit) | 224 | property broken |
|---|---|---|---|
| (1) override VALUES | `m_effortignore` `"${CX_EFFORT:-` -> `"${CX_EFFORTX:-`; `m_aupeffignore` likewise; `m_aupeffswap` `run_codex "$AUP_MODEL" "$EFFORT"; classify`; `m_effortglobal` `-c model_reasoning_effort="$EFFORT"`; `m_aupmodelhard` `run_codex gpt-daybreak-blue-latest "$AUP_EFFORT"; classify`; `m_ansbyhard` `    ANSWERED_BY=gpt-daybreak-blue-latest` | 94/94, all six | the header's "Overrides, each only so the branches are testable" is false of the mutant for `CX_EFFORT`, `CX_AUP_EFFORT` and `CX_AUP_MODEL`'s value; the CONTRACT's configuration lines cite EO, which straddles only the EMPTY edge.  Production unaffected (nothing on record sets any `CX_*`: grep of `tools/` and `_scratchpad/` finds only launcher copies and the controls); it is the CONTRACT's completeness and the harness's own ability to vary the effort.  **Killed by one row, OV** (section 8) |
| (2) truncation | `m_appout` `>> "$TXT"`; `m_apperr` `2>> "$ERR"` | 94/94, both | "the stdout/stderr redirections" are listed with N1F, which cannot see append on a fresh dir.  Production shape: the runner's retry into the same out dir.  **Killed by one row, SO** |
| (3) synthetic / equivalent constant edges the pin-the-constant reason demands | `m_stripplus` (bare `ESC[m`), `m_nop`, `m_modelcase`, `m_identcase`, `m_wcm`, `m_askedglobal`, `m_mvnof`, `m_sedquiet`, `m_bannerv`, `m_exith3`, `m_nounsetu` | 94/94, all eleven (`m_nounsetu` is already disclosed) | none breaks a CONTRACT line as WRITTEN; each breaks the REASON the CONTRACT gives for its synthetic rows, applied to a constant it did not pin.  **ESCM kills `m_stripplus`, NP kills `m_nop`, LOG2 kills `m_askedglobal`**; the rest are equivalents to DISCLOSE (section 5) |
| (4) a missing / relative brief | no mutant: the SHIPPED file | -- | section 5, U21: the launcher passes codex an EMPTY brief argument (`ARG []`, MEASURED with the fake) and reports its answer `seat answered`, exit 0 |

Everything else: 53 of 53 constructs either pinned at the edge the row names or disclosed with a true reason.

## 3. Q3 -- the kill table

**(a) Killed for a reason other than the one its line names?**  READ: all 105 lines' red sets against the mechanism the
edit implies.  NONE is killed for another reason.  The ones worth stating because their red sets are large or look odd:
`m_nomkdir` 4/94 -- no out dir, no redirect succeeds, the fake is never reached (E0) and every row reds, N1 among them;
`m_swapio` 41/94 -- the classifier reads the swapped files, so every row whose exit depends on which stream holds what
reds, N1F among them; `m_noinit` 50/94 -- `set -u` kills every rc-0 row in the else branch (unbound `$refus`), N1 among
them; `m_rule1next` 79/94 -- without `next` the first rule is immediately re-read as the closing rule, no block has a body,
every 5-row and every verified-credit check reds, M1 among them; `m_nomodelsed` 75/94 -- RAN keeps its `model: ` prefix,
every verified row exits 5 and CH's content grep misses; `m_binignore` 93/94 -- only E0b, exactly because the scratch
HOME's default fake absorbs every call (why U10 needed HOME for every column); `m_ord_re`/`m_ord_rc` 70/67 -- every refusal
fixture is rc 1 and empty, so an empty/rc check ahead of the refusal reds them all; `m_gateand` -- N4, Q2 (rc 0 empty with
a wall) and RC2W, the three joint shapes the `||` serves; `m_bodyverd` -- B1G and X2 both lack a verdict line (the fixture
comment records that X2's first draft contained the word).  Each named control is in its red set and the red set is what
the edit predicts.

**(b) A one-edit mutant OUTSIDE the table passing all 224 and breaking a line of the CONTRACT?**  Built 21; shapes swept:
every override's name and value (6), both redirections' truncation (2), `mkdir`'s flag, `wc`'s unit, the strip's `*`, the two
`.` alternatives, the `model:` label's case, the identity compare's case, the fallback line's `asked:`, `mv -f`, sed's
`2>/dev/null`, the banner `v`, the closing rule's form, `set -u`.  Results, every run with its sentinel and the 94 denominator:

| mutant | 94 | red | reads as |
|---|---|---|---|
| m_effortignore, m_aupeffignore, m_aupeffswap, m_effortglobal, m_aupmodelhard, m_ansbyhard | 94/94 each | none | ESCAPE, group (1) |
| m_appout, m_apperr | 94/94 each | none | ESCAPE, group (2) |
| m_stripplus, m_nop, m_askedglobal | 94/94 each | none | ESCAPE, group (3), pinnable (ESCM, NP, LOG2) |
| m_modelcase, m_identcase, m_wcm, m_mvnof, m_sedquiet, m_bannerv, m_exith3, m_nounsetu | 94/94 each | none | ESCAPE, group (3), EQUIVALENT on the controls -- disclose |
| m_curly1, m_curly2 | 3/94 each | 91 | INVALID (the edit breaks the single-quoted pattern: `unexpected EOF`) -- my error, not a finding |

So: 19 valid mutants, 19 escapes; 11 pinnable (and pinned in section 8), 8 disclosable.  Shapes swept and found PINNED by
reading (no mutant built): the window and cap constants and operators, the awk guards in every form the table has, the
first-`model:` rule, the gate's operands and `||`, the anchor and `-a`, every alternative, both case folds, the multiplicity
guards at all three sites, the trigger's three conjuncts, the renames, the credit, the cascade's five statuses and ten
orders, the final messages, the argument sequence, the names, the stdin, the cwd, the default path, the five `:-`/`-`
forms.

## 4. Q4 -- the records (section 5): which sentences are false of what ships?

TRUE, checked: "its executable lines are v3's; v4 and v5 changed comments only" (MEASURED, 0 non-comment lines v3 -> final);
every after-row expectation and content check of RECEIPT_v5 (MEASURED 224/224 on my mirror, same three md5s); "N4 (6)"
(MEASURED 6 wall lines on N1's stripped stderr); "nine dashes find no block anywhere" (MEASURED: the real rules are exactly
8 dashes); the `;`-joined SGR is on record (MEASURED 42 of 2,381 codex `.err` files by a stricter name filter; the census's
44 of 2,425 is the same fact at its population); the FB comment "set EMPTY by every other row" (MEASURED 57 of 65, the 8
exceptions as listed); U18's refutation (MEASURED: W12 and K30 set no `CX_MODEL`; the eight rows that do are M1 X5 X13 D5
CH EO BA R7B -- EO sets it EMPTY, which U18's list omits and need not include); 2b's "run_pack_body.sh is the only caller
that reads the log" (READ + grep over `tools/` and `_scratchpad/`: `panel.sh` names the launcher only in a comment and its
`seat answered` hits are its own seats'; the agy launchers PRINT the phrase for their own logs; the runner reads `seat
answered` and `The answer is LOST` in `done_job`, `answered by: [^)]*` with `tail -1` in `reap`, and the exits 7 and 8);
2b's "HOME changes nothing else" (READ: `$HOME` occurs once in the launcher; `sed`/`awk`/`grep`/`wc`/`mv`/`timeout` read no
HOME; non-interactive bash sources nothing); "Every caller on record passes absolute paths" (READ: the runner passes
`$ARTS/...` with `ARTS` absolute).

FALSE or over-claimed, each with its correction:

1. **The CONTRACT's NOT PINNED entry for RELATIVE paths, and the launcher's usage line** -- "codex got no brief and the run
   exited 1, NOT a clean run, nothing laundered".  True of the 2026-10-17 incident; FALSE as a property of the launcher.
   MEASURED with the fake codex (an answer fixture, a clean header): a MISSING brief -> `wc` errors, `brief bytes: `
   (empty), `[: : integer expression expected`, the `cd`, `cat` fails, codex is called with `ARG []` as its brief, and the
   run ends `seat answered. (answered by: gpt-6-astra)`, **exit 0**; a RELATIVE brief that exists in the caller's cwd ->
   `brief bytes: 14`, then after the `cd` the same empty argument and the same `seat answered`, exit 0.  The exit 1 on the
   day was CODEX's response to an empty prompt.  Correct both texts to: "the launcher does not check the brief; codex
   received an EMPTY prompt and itself exited 1; had it answered, the run would have been reported `seat answered`".
2. **The CONTRACT's configuration lines** imply the three overrides are pinned (E1, E2, EO): their VALUES are not (group 1).
   **"the output names and the stdout/stderr redirections -- N1F"**: truncation is not (group 2).  Repair by the rows in
   section 8, or move the edges to NOT PINNED with their reason.
3. **The SYNTHETIC SHAPES sentence** lists RF1-RF3, RFC, WL1-WL3, WLC, RW, BA, HB, R7A, R7B, NM, TM, MA, WS, K30, K31,
   W12/W13 and CSI's non-SGR half.  Also synthetic, by CENSUS_v5's own lines 4-5 (0 off the diagonal, 0 carrying both):
   RC1A, RC3A, RC2W, IR, B1G, B1E, EM, RI, WI, D5 (nothing sets `CX_MODEL`), and the fallback rows' Daybreak answers.
   Incomplete, not false; complete it -- the sentence is where a reader learns which rows are real.
4. **The ledger closure note and the CHANGELOG draft**: "each pinned at its edges or disclosed with its reason" -- the
   over-claim of item 2 in two more places.  True once the rows land; until then write "the v5 pass's four groups included".
5. **"KILLTABLE_v5.txt kills each of its mutants as named"** (closure note, witness) is a PRECONDITION, not a fact, at the
   time of this pass: the file on disk was the 04:04:22 header plus the two BASE lines (4 lines) for the whole pass -- the
   driver prints its mutant lines only after all 105 finish; and the 03:00 table the packet reproduces ran on launcher
   `236cda5f` and controls `362c8a93`, NEITHER of which is preserved on disk (the landed v4 is `ee4f5aec`, the final
   `af18158e`; no copy of `362c8a93` exists), so "comments only since" is checkable only through the re-run.  The record
   must be written from the completed re-run (105/105, `CXLAND_MUTANTS_DONE`), not before.  Its state when this file was
   finished is in section 9.
6. **The launcher header, lines 105-106** -- "line 5 of stderr in 599 of 600 codex .err files and line 7 in one (Astra)": a
   named, older population; CENSUS_v5 says 974 of 975 / 1.  Not false; re-cite the census.

## 5. Q5 -- U7 and U21

### U7: pin or disclose the six 0-on-record alternatives.  RULING: PIN.  My v4 DISCLOSE is withdrawn.

Harder on my own side first.  My v4 reason was *"0 instances on record is the pass-2 ruling's own criterion for DISCLOSE"*
-- a PRECEDENT argument, not a merits one, and the precedent was overturned in v5 (RC2W, CSI, RW pinned) with my agreement.
Worse, the same v4 answer asked for RC1A to be PINNED, whose shape is also 0 on record (0 of 474 launch lines off the
diagonal), on the ground that its fixture "carries no realism objection N4 does not" -- so I applied the criterion to F7 and
not to F1 in one answer.  The distinction I drew (a real rc and a real answer versus an invented diagnostic line) does not
survive the floor's own letter: clause (b) is "verbatim reinstatement"; K30/K31, W12/W13, every constant row is a statement
about the CODE, not about the record; *"a synthetic `ERROR: quota` would pin nothing real"* is true of every one of them,
and I had accepted every other one.

On the merits the packet's reason holds and is the stronger one: a deleted alternative changes what the CALLER does.
READ in `run_pack_body.sh`: an 8 writes STOP and ends the pack; a 6 leaves the job not done and the next pack run fires it
again, spending a codex call per run until a human reads the log.  If codex ever emits a sole `not authenticated` (the
carrier records `grok` printing exactly those words when logged out), a dropped alternative turns a stop into a retry
loop.  The rows cost one fixture each and the table 0.6 s each.  PIN.

What survives of my position, and it is the condition I attach: **the reason the CONTRACT gives -- "a constant's edges are
what an edge row is for" -- has no boundary, and the CONTRACT applies it selectively.**  By the same reason the file owes
rows for: a bare `ESC[m` (a documented SGR reset; `[0-9;]*` -> `\{1,\}` passes all 224, MEASURED; 0 on record, like
`quota`); `mkdir`'s `-p` (passes all 224); the `model:` label's case and the identity compare's case (pass all 224); `wc
-m` (passes all 224).  Each is a constant with a 0-on-record edge and a one-edit escape -- `quota`'s exact situation.
Without a stated boundary the next pass finds the next such constant, which is the `#392` shape wearing the CONTRACT's
clothes.  **Proposed boundary, to be written into the CONTRACT:** *a synthetic edge is PINNED when the constant selects an
EXIT STATUS or a CALL ARGUMENT on an input codex can produce through its documented interface -- a diagnostic line, a
header line, an escape sequence; it is DISCLOSED as equivalent when the edge is reachable only through the harness
environment (a locale), an input encoding the file does not claim, a flag whose other value is unreachable here, or a
display line.*  Applied: the six alternatives PIN (diagnostic lines); the bare `ESC[m` PINS (one row, ESCM -- MEASURED to kill
`m_stripplus`, section 8); `mkdir -p` PINS cheaply (NP, measured) or is disclosed; the `model:` label's case and the identity
compare's case DISCLOSE (codex's header is lower-case by its format; a folded compare is a policy change, not a drift);
`wc -m` DISCLOSE (bytes under the C locale this harness runs in; the briefs are ASCII); `-f`, `2>/dev/null`, the banner `v`,
the closing rule's form DISCLOSE as equivalent on the controls; the `.` of `can.t`/`won.t` DISCLOSE as the quoting form of
`'` (section 2, row 35 -- my curly-apostrophe reading was wrong and is withdrawn).

### U21: fix the relative-path behaviour in this landing, or disclose and file?  RULING: DISCLOSE AND FILE -- but the disclosure as written is a wrong record (section 4, item 1), corrected in-round, and the filing carries the measured shape.

The disposition is right: the executable lines have been v3's through three passes; every caller on record passes
absolute paths; the pack runner additionally checks the brief exists before launching (run_pack_body.sh:57, `MISSING
BRIEF ... skipped`); and a guard is new code -- a new floor-bound diff with its own rows (missing -> 9 before any call;
empty -> 9; relative -> the content reaches codex) and its own pass.  Not in this landing.

What the filing must say, because the current text understates it: the launcher does not check that the brief exists or
is non-empty; on a missing or relative brief it calls codex with an EMPTY argument and classifies whatever comes back --
the incident failed because codex exits 1 on an empty prompt, a property of CODEX, not of this file; a hand-launched job
(as on the dashboard pass) has no caller-side check; and a real codex call is spent each time.  The one-line shape that
closes missing, empty and relative briefs at once: read the brief BEFORE the `cd` into a variable and refuse an empty one
(`BODY=$(cat "$BRIEF") && [ -n "$BODY" ] || exit 9`, then pass `"$BODY"`), which needs no path parsing; the relative OUT dir
is the remaining half (a `case` on `/*|?:*` resolves it, the `?:*` arm being the Windows-absolute form the packet named).
Severity LOW: loud today by codex's behaviour; the cost is a wasted call.

## 6. Q6 -- which of the 22 dispositions is wrong?

Checked 22 of 22 against the file, the controls, the fixtures, the census, the callers and the kill table's red sets.
Wrong as stated: **U21** -- the disposition (disclose and file) is right; the disclosure's CONTENT is a wrong record about
the launcher (measured above).  Incomplete: **U7** -- PIN is right; the reason needs the boundary of section 5, since it
licenses rows the CONTRACT does not have.  **U10** -- right for `CX_CODEX_BIN` and for every `:-`/`-`; the configuration
section it produced lists `CX_EFFORT` and `CX_AUP_EFFORT` with rows that do not straddle "honoured" (group 1).  **U6** --
right for the names; the redirections' truncation is not straddled (group 2).  **U14** -- right; LOG pins the line's shape
on N1 only, not the fallback line's `asked:` (LOG2 closes it).  The other 17 are right as stated and as fixed.

## 7. The changes (the 5 of the verdict), ranked

1. **Row OV** (one row, one fixture; MEASURED): `CX_EFFORT=high CX_AUP_EFFORT=low CX_AUP_MODEL=gpt-6-other`, P2 then an
   answer whose header says gpt-6-other; tracked/before/after 7/0/0; check the whole two-call sequence (`-m gpt-6-astra` /
   `model_reasoning_effort=high`, then `-m gpt-6-other` / `low`) and `answered by: gpt-6-other`.  Kills all six group-(1)
   mutants.  Plus **LOG2**: D1's second `codex rc=` line says `asked: gpt-daybreak-blue-latest / ultra` (kills
   `m_askedglobal`).  CONTRACT line: "the overrides' VALUES reach the calls and the credit -- OV".
2. **Row SO** (a stale `codex_SO.txt`/`.err` pre-seeded in each column's out dir, replaced byte-for-byte; 0/0/0; MEASURED):
   kills `m_appout` and `m_apperr` (the latter also by exit: the stale other-model header is read first).  **NP** (an out
   dir whose parent is missing; 0/0/0): kills `m_nop`.  CONTRACT line: "the redirections TRUNCATE and `mkdir -p` creates
   the path (a retried job's out dir holds the previous run's files) -- SO, NP".
3. **U21's record corrected in place** (usage line, CONTRACT entry) to the measured behaviour, and the guard FILED with the
   shape in section 5 and its three rows named.
4. **The synthetic-pin BOUNDARY written into the CONTRACT** (section 5), the six alternatives kept PINNED, **ESCM** added
   (`ESC[mERROR: This content was flagged...`, rc 1: 6/6/7; kills `m_stripplus`), and the equivalents disclosed under NOT
   PINNED with their reasons (the quoting `.`, the two case edges, `wc -m` and the C locale, `-f`, `2>/dev/null`, the banner
   `v`, the closing rule's form).
5. **The SYNTHETIC SHAPES sentence completed** (section 4, item 3); the closure note's and CHANGELOG's "each pinned at its
   edges or disclosed" and "KILLTABLE_v5.txt kills each" written AFTER the kill-table re-run lands, citing it.

Add the eleven pinnable mutants (exact edits in section 2) to `mut_launcher_v5.py` with their killers (OV x6, SO x2, NP,
ESCM, LOG2), and DW/DE/DR as rows if the composition receipt is wanted (they kill nothing new).  No launcher code changes.
The chain closes on this pass if the adjudication grades these as records-and-rows, which is how I grade them: **zero
floor breaches** -- clause (d)'s DEPENDS-ON set (the gate, the strip, the header read, the trigger's conjuncts, the cascade)
is pinned at every edge I could find; the escapes are in test plumbing, a redirection flag and constants the file's own
reason owes rows for.  The re-run of the kill table on the extended controls is the scoped verification the row additions
owe; I would not fire another four-seat panel for comment-and-row changes.

## 8. The extended controls, MEASURED (`run_controls_v5x.sh`, 72 rows, 249 checks)

Calibration on the three launchers (my mirror, 04:2x-04:4x): **247/249**, the two reds being ONE apparatus flake (section 9)
and the E0 count it dragged; every new row and check as predicted:

| row | fixture / env | tracked | before | after | check |
|---|---|---|---|---|---|
| OV | P2, then OV2 (ans + hdr gpt-6-other) when `-m gpt-6-other`; `CX_AUP_MODEL=gpt-6-other CX_EFFORT=high CX_AUP_EFFORT=low` | 7 | 0 | 0 | the two-call sequence with `high` then `low`, `answered by: gpt-6-other` -- ok |
| SO | ANS, the out dir pre-seeded with a stale answer and a gpt-6-other header | 0 | 0 | 0 | both files byte-for-byte the fixture's -- ok |
| NP | ANS, out dir `$T/np/<row>_<col>/deep` (parent missing) | 0 | 0 | 0 | the files exist there, byte-for-byte -- ok |
| ESCM | `ESC[mERROR: This content was flagged for possible cybersecurity risk.`, rc 1 | 6 | 6 | 7 | -- |
| DW | P2, then P1 on Daybreak | 7 | 8 | 8 | (`SEAT WALLED (gpt-daybreak-blue-latest)`) |
| DE | P2, then N3 on Daybreak | 7 | 6 | 6 | (`EMPTY STDOUT`) |
| DR | P2, then rc 1 + answer + hdr gpt-6-other on Daybreak | 7 | 1 | 5 | (`A DIFFERENT MODEL RAN: asked gpt-daybreak-blue-latest, codex's header says gpt-6-other`) |
| LOG2 | -- | | | | D1's second `codex rc=` line, `asked: gpt-daybreak-blue-latest / ultra` -- ok |

Kills, each mutant through the extended after column (105 checks; every run with its sentinel):

| mutant | 105 | red |
|---|---|---|
| m_effortignore | 99/105 | OV (+ a flake: D3's first call left no files -- section 9) |
| m_aupeffignore, m_aupeffswap, m_effortglobal | 104/105 each | OV |
| m_aupmodelhard, m_ansbyhard | 103/105 each | OV (row exit 7 and the sequence check) |
| m_appout | 104/105 | SO |
| m_apperr | 103/105 | SO (the check and the row: exit 5, the stale header read) |
| m_nop | 99/105 | NP, and CWD E0 FD SI (NP's codex is never reached -- the mutant's own effect) |
| m_askedglobal | 104/105 | LOG2 |
| m_stripplus | 104/105 | ESCM |

11 of 11 killed by the row written for each, and by no other row except where the mechanism itself removes a run.

## 9. Apparatus observations, what I could not check, and the state of the in-flight artifacts

**A flake class, MEASURED twice in about 2,570 launcher runs today** (195 + 216 base runs, 21 x 65 and 11 x 72 mutant
runs), both under 8+ concurrent control runs (the main loop's 4-way table plus mine): a run whose `mkdir -p "$OUT"`
printed nothing then failed its first redirect -- the signature in the log is `codex rc=1   stdout= b   stderr= b` (EMPTY
counts where numbers belong) preceded by three bash `No such file or directory` lines -- in `B1E tracked` of my extended
base (hence E0's `NOT reached: B1E_tracked`) and in `D3 after`'s FIRST call of one mutant run (hence that run's spurious
E0/SI/CWD/D3 reds).  Neither is the launcher's doing; the cause (an MSYS/Windows transient between `mkdir` and the next
process's open, under load) is NOT established.  The direction is fail-safe for the table: a flake only ADDS reds, so it
cannot hide a kill, and a flaked BASE run already aborts the table; it can put a spurious name in a "killed by" list.
Two cheap defences, filed not demanded: the driver treats a run containing `stdout= b` as INCOMPLETE and re-runs that
mutant once; and the controls' per-run `cut -c1-170` hides the error text behind the path prefix -- print bash's error
lines without the prefix, or widen the cut.  (Note `m_nop`'s NP run shows the same signature legitimately: that is the
mutant's own effect, and the distinction is whether the base run shows it.)

**Not checked**: the 105-mutant table was not re-run (section 3a reads it); Astra's two census scopes (322/519, 319/493;
330 answered runs with a header) were not reproduced -- named derivers, consistent in direction with CENSUS_v5.  The
`cxlaunch_before.sh` column's own semantics were recorded, not reasoned (it fires the fallback and never compares the
model: OV 0, DR 1, ESCM 6).

**State of the main loop's re-run when this file was finished**: `KILLTABLE_v5.txt` = 4 lines (the 04:04:22 header on
launcher `af18158e`, controls `12effca6`; `BASE CONTROLS: 224/224`; `BASE 65 rows ... 94`), the mutant block not yet
printed, 34 bash processes alive at 05:01:50.  The record must cite the finished file with `KILL TABLE: 105/105` and
`CXLAND_MUTANTS_DONE`; if any line reads INCOMPLETE, check it for the flake signature above before reading it as a
launcher fact.
