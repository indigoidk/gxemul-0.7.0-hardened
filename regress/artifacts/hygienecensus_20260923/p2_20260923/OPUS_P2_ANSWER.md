<!-- Extracted VERBATIM from the subagent transcript agent-a39de4577195faad0.jsonl (session 8e474f41), the LAST assistant text block; timestamp 2026-09-23T19:20:53.163Z; model claude-opus-5-5; models seen in the run: ['claude-opus-5-5']. -->

OPUS_SEAT_ALIVE_20260923_CENSUS

VERDICT: 14 EVASIONS MEASURED

Ten single edits leave all 11 readiness rows green with the gate alone. Four more go green once the operator runs `derive_hygiene_pins.sh --write`, which the gate's own comments tell them to do. Separately, one live instance is in the tree now: `crime_width_probe.py` is a promptless pty probe that the census misses only because of the comment this round added to it.

**Your single-quote suspicion is confirmed.** And the original #37 bare-prompt row can be walked around with one space.

## Method and identity
- **Snapshot:** one copy of `regress/`'s 149 top-level files, taken 14:14:17. At 14:19 all 149 were compared against the tree and none differed. Gate md5 is `7551ecef…` (HEAD is `12e179ad…`, so this is the working-tree version with the diff).
- **Per case:** a fresh copy from the snapshot, one edit, then the unmodified gate run with an empty `LOGDIR`. Nothing under `GXEMUL-SEC` was modified; I checked md5s, my file names and `_control_site` afterwards.
- **Extra instrument:** a truncated copy of the gate that echoes its intermediate values (allends, full, whole_full, and so on). Those values are in each case's `.raw` file.
- **Non-readiness rows:** the two class-ratchet rows fail in every copy because `src/` is absent there, the same as in your controls. I report readiness rows only.
- **Outputs:** each case is in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\opus\runs\<tag>.out`, with `.rows` and `.raw` beside it. The results are collected in `SUMMARY.txt`, `SUMMARY2.txt`, `SUMMARY3.txt`, `DERIVER_SUMMARY.txt` and `DERIVER2_SUMMARY.txt` in the same directory.

The base run (`base`) was all green: 0, 0, 73, 42, 3, `arm_bdt_probe.py arm_flags_probe.py`, 24, 24, 24, 2, 5.

## The seven requested cases

**1. `c1_single_quote`: no row changes.** Intermediates: allends 49→50 and full 49→50, so the closed-world recogniser accepts the single-quoted form as a known spelling and `unknown` stays 0. whole_full stays 3. The whole-buffer pattern only matches double quotes, so neither the count row nor the name row sees it.

**2. `c2_inner_spaces`:** exactly one row reds.
```
FAIL readiness: no unrecognised endswith spelling         got=1 want=0
```
It is caught by the spelling row, not by the whole-buffer rows (whole_full stays 3).

**3. `c3a_comment_indented` and `c3b_comment_col0`: no row changes.** The name row still prints `arm_bdt_probe.py arm_flags_probe.py`. This is correct behaviour and consistent with the count row.

**4. `c4_space_in_path`:** the name row and count row stay green and correct. The two older rows built on `_ptylist` (a bare `xargs`) red:
```
FAIL readiness: pty-probe denominator (enumerate FIRST)   got=0 want=73
FAIL readiness: promptless probes, grandfathered set only got=1 want=42
```
The offender notice then names a phantom file, printed as `(standard` / `input)` across two lines: `grep -L` read `/dev/null`.

**5. `c5_no_population`:** 76 population files were removed. The name row fails closed with an empty got:
```
FAIL readiness: whole-buffer sites, allowlisted files     got= want=arm_bdt_probe.py arm_flags_probe.py
```
Also red: denominator `got=0 want=73`, promptless `got=1 want=42` (the same phantom), whole-buffer count `got=0 want=3`, and anchored/echo/fresh-mark `got=0 want=24` each. The bare, unknown and truth-table rows are unchanged.

**6. Locale: no row changes under any of four settings.**
- The battery's own environment: `LANG=en_US.UTF-8`, but that locale is **not installed** on the WSL image (`locale -a` lists only C, C.utf8 and POSIX), so it silently falls back to C.
- `LC_ALL=C`.
- `LC_ALL=C.utf8`.
- A real `en_US.UTF-8` that I compiled privately with `localedef` into `/tmp/opus_census0923/loc` and used via `LOCPATH`.

The mechanism does exist: under the real en_US, `armb_x.py` sorts before `arm_c.py`, and C sorts them the other way (`locprobe.out`). The two current names are unaffected. A future pair like that would give a false red, never a false green, because got is compared against a literal.

**7a. `d7a_write`:** `--write` refuses with rc=5 and the gate file is unchanged (`cmp` clean).
```
REFUSED: the three #392 counts disagree (24/24/23) -- a guard present but uncounted; fix the probe, not the pin
```

**7b. `d7b_write`:** `--write` refuses with rc=5 and the gate file is unchanged. The name appears in the report block just above the refusal (`NEW PROMPTLESS … zz_opus_newprobe.py`); the refusal line itself does not name it.

## Evasions, gate alone (all 11 rows identical to base; every planted line parses as Python, see `syntax_check.txt`)

| tag | edit | why no row sees it |
|---|---|---|
| c1 | `buf.rstrip().endswith('GXemul>')` | full recognises it; whole-buffer pattern is double-quote only |
| e1 | `out.rstrip().endswith("GXemul>")` | the buffer variable must end in `buf` |
| e2 | same predicate split across two lines | the pattern is line-based |
| e5 | `buf.strip().endswith("GXemul>")` | the pattern requires `rstrip()` |
| e3 | `buf.rstrip().endswith ("GXemul>")` | allends stays 49: the enumerator keys on the literal `endswith(` |
| **e9** | **`buf.endswith (">")`, the #37 bare defect itself** | bare=0; control `e9ctl` without the space gives `FAIL … bare-prompt sites frozen (#37) got=1 want=0` |
| e4 | `buf.rstrip()[-7:] == "GXemul>"` | not an `endswith` at all. This is also the replacement your `move` control used, so that control relabels the arm_bdt site rather than converting it |
| e6 | move one site from arm_flags_probe.py into arm_bdt_probe.py | the count stays 3 and the file set is unchanged; per-file counts are not pinned |
| e7 | new promptless pty probe named `zz opus_newprobe.py` | the bare `xargs` in `_ptylist` splits the name. Control `e7ctl` (no space) reds both rows and names the file; the deriver's `--write` is also a no-op here (`dE7`) |
| e14 | rename `gdrom_cond_probe.py` to a new name | the promptless row compares counts (42 = 42). The NEW PROMPTLESS notice prints but is not a graded row. The deriver does refuse this one and names both files (`dE14`) |

## Evasions through `--write` (the gate reds first; the sanctioned command then makes it green)

| tag | edit | red before `--write` | what `--write` did | after |
|---|---|---|---|---|
| dL1 | add `endswith(PROMPT)` | unknown `got=1 want=0` | rc=0, EXPECT_UNKNOWN 0→1 | 0 FAIL of 11 |
| dL2 | 4th whole-buffer site in arm_bdt_probe.py | `got=4 want=3` | rc=0, EXPECT_WHOLE_FULL 3→4 | 0 FAIL |
| dL3 | promptless probe in a new subdirectory | denominator 74/73 (the promptless row stays 42/42 because it looks up basenames in `$HERE`) | rc=0, EXPECT_PTY_PROBES 73→74 | 0 FAIL |
| dL5 | promptless probe whose only `endswith(` is in a comment | denominator 74/73 | rc=0, EXPECT_PTY_PROBES 73→74 | 0 FAIL |

Control `dL4` (a 4th site in a file that is not allowlisted): after `--write` the new name row stays red. So the new row does its job in that case.

The pattern: the deriver refuses a raise only for EXPECT_BARE. It raises EXPECT_UNKNOWN and EXPECT_WHOLE_FULL, which the gate describes as pins that must never be raised.

## Live in the tree now
- Of the 31 pty probes the census classes as prompt-detecting, exactly one, `crime_width_probe.py`, has no prompt predicate in code (`SUMMARY3.txt`). Its `session()` reads by elapsed time.
- Its only two `endswith(` occurrences are the comment lines this round added at 956-957.
- Rewording only those two comment lines (`e15`) gives:
```
FAIL readiness: promptless probes, grandfathered set only got=43 want=42
```
  with `NEW PROMPTLESS … crime_width_probe.py`.
- So there are three untracked promptless probes by the census's own rule, not the two that premise 2 grandfathers. The third is hidden by a comment.

## Premises (a), (d), (e), as measured
- **(a) holds,** with conditions I checked: every `.py` outside `artifacts/` is at the top level, so a top-level copy has the full population. The scheduled task uses the same `wsl.exe -d Gentoo -- bash` form, so the battery gets the same locale fallback. The battery's path has no spaces.
- **(d):** the name row is fine with a space in the path, fails closed on an empty population, and does not change with locale. Its gaps are e6 (per-file counts) and the spelling blindness it shares with the count row.
- **(e):** 70 pty probes are tracked at HEAD (`git grep`), plus 3 untracked, which makes 73. The grandfathered list equals the census's promptless set (the deriver printed no NEW and no GONE block). "Promptless" in the property sense is false for `crime_width_probe.py`, as above.

Not measured: premise (b) (`op[-1:]` versus `endswith`) and Q3–Q5. The runs are in `_scratchpad` and the copies in WSL `/tmp`; if a commit cites any of these numbers, copy them into `regress/artifacts/hygienecensus_20260923/` first, which I was not permitted to do.

**Seat record.** Model: Opus 5.5 (claude-opus-5-5[1m]).
- **Read:** the brief; `census_controls.sh`; all 869 lines of `gate_hygiene.sh`; `lib.sh` lines 20-160; the deriver (inlined in the brief, and executed); `crime_width_probe.py` `session()`; the header of `nightly_battery.sh`; the scheduled task's action.
- **Ran, all on copies in WSL `/tmp/opus_census0923`:** `envprobe.sh`, `locprobe.sh`, `measure_gate.sh`, `measure_gate2.sh`, `measure_gate3.sh`, `measure_deriver.sh`, `measure_deriver2.sh`, `check_syntax.sh`, `cmp_snap.sh`. All are in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\opus\`.
