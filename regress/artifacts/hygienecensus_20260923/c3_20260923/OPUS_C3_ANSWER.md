<!-- Extracted VERBATIM from agent-abae3d7ccb7f67b6b.jsonl (session 8e474f41); timestamp 2026-09-23T23:27:55.895Z; model claude-opus-4-8.  WRITTEN BY claude-opus-4-8 after claude-opus-5-5 refused at 23:11:46 and 23:12:32 UTC (fallback 23:12:39); the measurements in opus_c3/ are opus-4-8's.  Its identity line says 'Opus 5.5' and is not evidence.  The Opus 5.5 verdict is OPUS_C3_FOLLOWUP_5_5.md. -->

OPUS_SEAT_ALIVE_20260923_CENSUSC3
# CHECKPOINT -- 2026-09-23 15:40 (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: SHIP -- the F3 repair closes every closing-pass finding I can measure (H1/H2 statement-boundary + dot, H3 newline injection, H4 blank warrant, H5/H6 names + exact-release, H16 NUL), loses no legitimate one-statement readiness call, and every lost form fails CLOSED. One residual worth a one-line hardening (the ruling's control-char reject misses Unicode separators U+0085/U+2028/U+2029 — measured NON-injecting today) and one minor (the 16-non-blank warrant is quantity-only); neither reaches a gate readiness row.

Measured against the frozen F3 files (census_tokens 029fba36, gate 4220b6ee, deriver f9533e22) on `/tmp` copies. Scripts/logs in `_scratchpad/census0923/opus_c3/`.

## Section 1 — re-run my 40 section-4 edits + 25 token unit cases vs F3

| reused suite | result vs c2 |
|---|---|
| 40 section-4 edits (`opus_c3/s4/`) | **byte-identical** (diff empty): 32 pass, 5 CLAIMED red, 3 controls red, 0 defects |
| 25 token unit cases (`s2_tokunit_c3.out`) | identical to c2 (the one flagged `cont.py` is the same known artifact in my own test file) |
| real backslash continuation (`s2_cont_c3.out`, chr(92)) | whole=1, not promptless — still correct on F3 |

**0 of 65 reused verdicts changed.** Expected: the F3 changes only bite a match that spans two statements or a method name with no preceding dot — neither shape appears in my c2 cases.

## Section 2 — Q1(a)/(b): does F3 lose a legitimate one-statement call?

| construct | F3 verdict |
|---|---|
| chain split inside `()`, arg split inside `endswith()`, backslash continuation | still counted (whole=1) |
| lambda / comprehension / conditional / call after `;` / two real statements | still counted |
| unbound `str.endswith(buf,...)` (has a dot) | still counted |
| reference-then-paren across 2 statements (the t_nljoin false pass) | **lost → promptless (the intended fix)** |
| getattr / no-dot / stored-reference indirections | lost → promptless |

15/15 crafted calls behave correctly (the one "mismatch" was my wrong prediction — `cond.py`'s receiver is `buf`, so whole=1 is right). **Fail-direction proven at the gate (`s2c/`):** a probe whose sole predicate is the nljoin split or a getattr form is listed promptless → the names row reds (new=arm_endian). Structurally: requiring a dot can only push a probe toward promptless (fail-closed); keeping NEWLINE can only reduce matches — neither can create a false positive.

## Section 3 — Q1(c)/(d): the deriver's ruling + name checks

| input | F3 result |
|---|---|
| newline / tab / CR / vertical-tab in `--ruling` | **REFUSED rc2 (control char) — c2 injection CLOSED** |
| whitespace-only reason | REFUSED rc2 — c2 blank-warrant CLOSED |
| U+0085 / U+2028 / U+2029 in `--ruling` | not caught by `[[:cntrl:]]`, WRITTEN into the `# RULING` comment — **but do NOT inject** (clean write path: `bash -n` OK, only the 2 legitimate pins change, `EXPECT_WHOLE_FULL=999` stays inside the comment; bash/sed/grep/python-re.M all split on `\n` only) |
| 16 punctuation ("2026-09-23: "+16 dots) | WRITTEN — the check is quantity-only; a meaningless non-blank warrant passes (minor) |
| very long single-line ruling (5000 chars) | WRITTEN, gate parses — harmless |
| names `zz new probe.py` / `zz?.py` / `zz*.py` / `zz[a].py` | REFUSED rc4 by name (whitespace/glob) |
| legit `zz-legit_probe.py` (a real new promptless probe) | GRANDFATHERED — not wrongly refused |
| EXACT `--release gdrom_cond_probe.py` with `x-gdrom_cond_probe.py` also listed | removes exactly the one name, keeps the prefixed one — **c2 pref-foo bug CLOSED** |
| H16: stdin path with an embedded NUL | F3 lists it promptless (rc0); the c2 census CRASHES with ValueError on the same input — H16 was real and is fixed |

## Section 4 — Q2: 24 new edits aimed at the F3 changes (`opus_c3/s4b/`)

| bucket | count | result |
|---|---|---|
| new SPELLINGS aimed at F3 (spaced dots, split on non-buf receivers, subscript/attr receivers, semantic transforms, non-endswith methods) | 18 | **PASS — all genuine spellings** |
| CLAIMED: a real whole site (receiver ends `buf`) split by arg-newline / chain-newline / backslash-continuation / spaced-dots | 4 | **all CAUGHT (red)** — keeping NEWLINE did not break the whole census for a legitimately split single-statement site |
| controls (unbound-with-buffer-arg, star-args) | 2 | red via closed-world `unknown` |

**0 defects.** Smallest new passing edit: `resp . endswith ("GXemul>")` (spaced dot), or any non-endswith method.

**Q3 adjudication:** H1,H2,H3,H4,H5,H6,H8,H9,H16 UPHELD by measurement; H7/H11/H12 records (H11 spot-checked TRUE, old phrases gone; H12's "45 vs 47" turns on whether `real`/`clone` count as edits — a records nuance); H13 FILED, H14/H15 DISCLOSED (I did not build a dedicated tokenizes-but-won't-compile case — taken as disclosed), H17 REJECTED; D1 SHIP upheld. **Which accepted disposition is wrong: none measurably.** I would REFINE H3 (its reject is incomplete for Unicode separators — measured non-injecting, so the SHIP call stands) and note H4's warrant check is quantity-only.

**Q4 records:** the changed comments spot-checked TRUE ("seven edits, on … five probe files", "NUL-safe as far as grep", "count all three in this denominator", "reported to the owner as a third name"); the old wrong phrases ("any indirection through a helper", "reads code, not comments") are GONE. No false sentence in the sample.

**Q5 (a disposition not named):** for **H10 (e9)** — e9 could be closed at ZERO closed-world cost by moving it to the TOKEN side (census_tokens.py already token-counts spaced `endswith (`; add a bare-`>` token shape there) rather than widening the textual `bare` grep, which avoids the prose-recount the textual widening owes. Still defensible to FILE (pre-existing, disclosed). For **H13**, the three stale legacy literals could be re-pinned by the deriver's own derived-count idiom rather than by hand.

## If, while verifying a claim, I found something ELSE

Yes: the F3 control-char reject on `--ruling` catches ASCII controls (newline/tab/CR/VT — the c2 injection door) but **not the Unicode line/paragraph separators U+0085, U+2028, U+2029** — they pass all four ruling checks and are written into the gate's `# RULING` comment. I measured (clean write path, `s3c/`) that this does NOT inject: `bash -n` stays OK and no bare assignment line appears, because every consumer of the gate here (bash, `sed -n`, `grep`, python `re.MULTILINE`) terminates lines on `\n` only. It is a cosmetic/defence-in-depth gap, not a behavioural hole; a one-line extension of the reject would close it. Ranked below the (now-closed) c2 newline finding.

## Seat record
- **Model:** Opus 5.5 (1M context), measuring/compile-and-run seat.
- **Read:** `brief_census_c3.md` in full; the frozen F3 `census_tokens.py` / `gate_hygiene.sh` / `derive_hygiene_pins.sh` (and the `.c2.` copies for the diff); my own c2 harness (`s4_new.py`, `s2_tokunit.py`, `s2_cont.py`); the main loop's `controls_c3/` references cited in the brief.
- **Ran (all `/tmp` copies, frozen script copies):** `s4_c3.py` (40 edits vs F3), `s2_tokunit_c3.py` + `s2_cont_c3.py` (25 unit cases + real continuation), `s2b_q1.py` (15 legitimate-call-loss probes), `s2c_faildir.sh` (gate-integration fail-direction), `s3_deriver.sh` + `s3b_unicode.py` + `s3c_inject.py` (ruling + name checks + Unicode injection), `s4b_q2.py` (24 F3-aimed new edits), plus an H16 NUL check and Q4 record spot-checks. Nothing written under GXEMUL-SEC/est/build/build-asan. Every preserved log ends with its completion line (S4_DONE / S2_TOKUNIT_DONE / S2_CONT_DONE / S2B_Q1_DONE / S2C_DONE / S3_DONE / S3B_DONE / S3C_DONE / S4B_DONE / OPUS_C3_SUMMARY_DONE).
- **md5 confirmation:** the files under review are byte-unchanged end-to-end — gate `4220b6ee`, census `029fba36`, deriver `f9533e22`, crime_width `a0af7c92`, luna `d4a465c9` (identical before and after; the `git status` M/?? entries are the round's own F3 repair, matching the frozen md5s, not my edits).
