<!-- the Opus 5 measuring seat's answer, extracted from its subagent transcript; model claude-opus-5-5; 2026-09-24T07:19:34.488Z -->
OPUS547RP_ALIVE
# CHECKPOINT -- 2026-09-24 00:55 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: R'=SHIP WITH NOTES; RECORDS=SHIP WITH NOTES

R' is correct on all current data. One kind of edit still gets past every control you listed: a change to a default. It moves what section L actually runs (no `GXATTR_DEPTH`, no `GXLEDGER`, no arguments) while every control that sets those variables explicitly stays green. The records have three errors, one of them new in the docstring correction.

I wrote nothing under GXEMUL-SEC, est or the build trees; HEAD is still 3e33201d. The scratch clones clone2 through clone5 were `--shared` copies under `_scratchpad\opus547\`, and all of them are removed. The inlined diff matches the working diff exactly (139 of 139 lines). Commands 60–80 are in `_scratchpad\opus547\COMMANDS.log`.

## 1. Is `lists()` exactly the pre-R grammar where it should be?

**Yes, apart from width and two non-width consequences.**

MEASURED in memory: pre-R (3e33201d^) against R', with `fbsmlane.commits` set to various shapes at abbreviations 6, 7 and 8.
- Upper-case, parenthesised, 6-character and tab-separated values grade identically.
- The only differences come when the token's length differs from git's abbreviation. That is the intended width-independence.

The two differences that are not about width:
- **Ambiguity (REASONED).** Pre-R compared against git's short hash, which git guarantees is unique. A token shared by two commits therefore never matched either of them, and the check failed loudly. `lists()` credits every commit the token prefixes, silently. MEASURED: all 184 ledger tokens resolve to exactly one object today.
- **The 7-character floor.** With `core.abbrev` below 7, pre-R could credit a 4–6 character token and `lists()` cannot. MEASURED: `bad_commits()` rejects such a token as HARD in both versions, so the verdict is the same.

Q19a, b and c reproduce: pre-R gives HARD/HARD/HARD, HEAD gives PASS/HARD/PASS, and R' gives HARD/HARD/PASS.

One correction to the brief: Q19c's "which the pre-R whole-token test also credited" is true only at a 7-character abbreviation. MEASURED: at today's 8 characters, pre-R grades it HARD.

## 2. Does `git()` fail closed without failing anything legitimate?

Q20 reproduces (MEASURED): HEAD exits 0 with "scanned 0 … PASS"; R' exits 2 with a line starting "HARD … git log exited 128". The default invocation exits 0, and I found no normal invocation of this repo that exits nonzero. Two gaps remain.

- **A legitimate commit subject crashes the checker.** This is not introduced by R'.
  - MEASURED: Python here decodes git's output as cp1252 (`locale.getpreferredencoding` gives cp1252; UTF-8 mode is off).
  - A subject containing ” (U+201D, whose UTF-8 bytes include 0x9D) makes the reader thread raise UnicodeDecodeError. git itself still exits 0, so `r.stdout` comes back as None.
  - MEASURED in a scratch clone with one such commit: HEAD and R' both crash with an AttributeError, and neither prints a line starting "HARD". Section L would show only its header, for as long as that subject stays in the 60-commit window.
  - No subject in the 796-commit history contains such a byte today.
  - The fix is `encoding="utf-8", errors="replace"`.
- **The empty window still passes.** MEASURED on R': `GXATTR_DEPTH=0` gives "scanned 0 commits deep … ATTRIBUTION_PASS". A negative depth does fail closed (exit 2). So "a gate passing on nothing" is closed for git errors, not for an empty window.

## 3. Does any single edit keep every control green yet change a verdict on current data?

**Yes. MEASURED** with `battery_rp.py`: 57 mutants against every input the packet lists. I treated the 19 success-path inputs plus Q19a/b/c and Q6 as golden-identity controls against unmodified R', and added Q20 and Q21b (tag `7a361f47` in a scratch clone). Golden identity is a stronger assertion than yours, so anything that survives it would also survive your verifier. The success path itself holds: HEAD and R' are byte-identical on 19 of 19 inputs.

**Four mutants survive every control and change the verdict of the gate as section L runs it:**

| Mutant | Section-L-style run | Controls |
|---|---|---|
| D1 — `DEPTH` default "60" → "0" | exit 0, scanned 0, "ATTRIBUTION_PASS 0 hard, 0 soft" | all green |
| D2 — default "30" | 3 soft | all green |
| D3 — default "130" | 29 soft | all green |
| D4 — default ledger path → the untracked `ledger.json.before_nul546` | 11 soft | all green |

- D1 is the failure R' was written to close, reached through the default instead of through git.
- **One control closes all four** (MEASURED, `default_demo.py`): run the checker exactly as section L does, with no environment variables and no arguments, and compare it with the golden Q0 plus "scanned 60".
- If your golden Q0 was already run with no environment variables, these four are already killed. The packet doesn't say which.

Every other mutant is killed or changes nothing on current data. Each named construction dies on its intended control: C1 on Q16, the `{6,40}` extractor on Q7, `t in full` on Q11, reverting to `names()` on Q19a, `records_only(h)` on Q21b, and Lg5 on the golden Q0.

The latent survivors, none of which changes current data:
- the free-text `reopened` grammar: its boundaries, case, a substring match, or first-token-only;
- the `lists()` token grammar: `{6,40}`, `{7,}`, A–F, dropping the TOKEN test (masked by `bad_commits()`), `split(" ")`, `lower()`;
- `git()`: failing only when the exit code is above 1, failing only for `git log`, or keying on stderr instead of the exit code;
- a subject containing a tab; the closure branch excusing `dropped` rows or ignoring the word "closing"; dropping `ops` from NONREPO.

One more MEASURED point: E1 (the FAIL branch returns 0) on Q19a gives exit 0 with a HARD line. Section L keys only on the exit status, so it would show green. E1 dies only if your HARD-bearing controls assert the exit status.

## 4. Is every corrected sentence now true?

**True:**
- The SHA-block comment, with one caveat: "a `git gc`" is an inference from packed-refs being rewritten 13 seconds before a new pack appeared.
- The `names()` docstring, the `lists()` comment, the `git()` comment, and the main() lookup comment.
- codex's wording for what `reopened` may hold.
- The three corrected CHANGELOG sentences.
- The ledger fix. MEASURED: +4 bytes, and only the fbsmlane and citestale fields changed since the last pass. No control characters remain in the ledger, and `matrix.html` now has none.

**Not true:**
1. **New error: the docstring's corrected open-row SOFT paragraph is incomplete.** It names only records-only commits. MEASURED: 3 of today's 10 SOFT lines at depth 60 are a case it omits. That case is a non-records commit against a non-closed row whose `commits` field is non-empty but doesn't list it ("open row, commits=…"). The three are 3c365261, 9c91999a and 816e153e.
2. **The `records_only` comment's "8 HARD at full depth -- attribution drift it has been hiding" overclaims.** MEASURED:
   - 7 of the 8 change checker logic; 748c9daf only adds an entry to a MANIFEST table.
   - bbfc942e and 86ea7c0e are harness edits bundled into commits whose subjects name unrelated rows (shiftubcensus, asicbadaddr). HARD there would be a mis-attribution, not hidden drift.
   - Honest wording: "8 HARD; whether each is drift is a reading."
3. **An uncorrected sibling sentence.** CHANGELOG line 100 still reads: "Fixed the way section F's receipt check already was: a 7-40 character hex token names a commit when it is a PREFIX of %H".
   - Section F's check, `index(p, $1) == 1` on any non-empty first field, has no 7-40 rule.
   - The corrected code comment now says exactly that ("which section F does not have"), so the two records disagree again.
4. **In the brief only:** "neither field is read by it" is off. The checker does read `reopened`, but only for rows that are not closed, and lcaisalane is closed.

## Found something else

- **`regress/pass2_ledger.tsv` is a records file, but `records_only()` does not exempt it.** MEASURED across all history:
  - 43 commits are graded as code only because they touch it.
  - 13 of those are listed in some row's `commits` field — for example sh4prio0 lists 02883288, "Close sh4prio0…". Rows are naming records commits as though they shipped code.
  - This belongs in attrcheckgaps, together with the cp1252 crash, the empty-window pass, and the no-environment control.
- **Stage the #547 commit by path.** The working copy of `precommit_check.sh` also carries an unrelated change to `SCORE_CLAIMS_MANIFEST` (30 → 31), and the ledger holds rows from other work.
