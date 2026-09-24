# hygienecensus pass 2 -- dispositions (main loop, 2026-09-23 ~14:4x)

Panel `_scratchpad/panel_20260923_140627` (brief 26,858 b) + Opus measuring seat (agent a39de4577195faad0, claude-opus-5-5
x37, clean).  Seats: codex DO NOT SHIP; grok DO NOT SHIP; agy DO NOT SHIP -> GO-WITH-CHANGES; deepseek DO NOT SHIP;
kimi-k3 (substitute; the kimi CLI walled on its WEEKLY limit) DO NOT SHIP; glm SHIP (five non-blocking defects);
minimax SHIP; opus5 "14 EVASIONS MEASURED".  Fable: not yet fired -- fires LAST, on the F2 pass.

Stopping rule: in-round only a MEASURED FALSE PASS or a WRONG RECORD in THIS round's material (L1: the deriver and the
name row are new material still being built); everything else FILED.

## IN-ROUND

C1  crime_width_probe.py is a PROMPTLESS pty probe (settle/spin timed drains, session() :469) hidden from the promptless
    census ONLY by the comment this round added at :956-957 (it contains `endswith(`; the promptless scan is a raw
    `grep -L` that keeps comments).  MEASURED (opus e15: got=43 want=42 once the comment is reworded); codex, grok, agy
    independently.  A false pass THIS DIFF created.  FIX: (a) the promptless classifier strips full-line comments, like
    every other census scan (closes the class -- opus dL5 -- and changes no other file's classification today: opus
    SUMMARY3 found crime_width the ONLY such file); (b) reword the comment anyway; (c) grandfather crime_width_probe.py BY
    NAME -- the owner's principle for untracked promptless probes (ruling 2), applied to the third one the census had
    hidden.  REPORTED TO THE OWNER as a third name, not silently folded in.
C2  single-quoted whole-buffer site evades BOTH whole-buffer rows (count and the new name row match only `"GXemul>"`,
    while the closed-world `full` recogniser accepts both quotes, so `unknown` stays 0).  MEASURED (opus c1: every row
    green).  The name row is this round's.  FIX: both patterns quote-agnostic.
C3  the name row pins a SET, so a site MOVED between the two allowlisted files is invisible (opus e6: count 3, set
    unchanged).  FIX: the row pins `name:count` per file -- `arm_bdt_probe.py:1 arm_flags_probe.py:2` -- a refinement
    INSIDE ruling 3 (allowlist by name), not a new member.
C4  the promptless row compares COUNTS, so swapping one grandfathered probe for a new promptless one reads 42 == 42
    (opus e14, kimi-k3, grok); the NEW PROMPTLESS notice prints but is not graded.  Ruling 2 says grandfather BY NAME.
    FIX: grade the set -- new and gone must both be empty.
C5  the deriver (NEW, ships with this round) --write RAISES EXPECT_UNKNOWN (opus dL1, codex, kimi-k3) and
    EXPECT_WHOLE_FULL (opus dL2, grok), both pins the gate says are never answered by raising; it neither derives,
    reports nor writes WHOLE_FULL_FILES (agy, deepseek, kimi-k3, glm), so ruling 5 ("never by hand") was unachievable for
    the pin this round added; it masks its own python failures (codex: `exit 0` after --grandfather's subprocess,
    DERIVE_DONE regardless); and it re-pins to ZERO if the enumerators see nothing (glm: no plausibility floor).
    FIX: refuse any rise of EXPECT_UNKNOWN; refuse a rise of EXPECT_WHOLE_FULL or any change of the per-file set unless
    WHOLE_FULL_RULING names an owner ruling (then write both, derived); derive + report + write WHOLE_FULL_FILES;
    propagate python exit status; refuse when the pty denominator is 0.
C6  WRONG RECORDS (L4-in-construction), each fixed where it stands:
    - deriver usage line says --write rewrites EXPECT_BARE (it never does) -- codex, grok, glm, kimi-k3;
    - the grandfather note says each of the 20 "uses a fixed-wait or drain-to-EOF session rather than a prompt
      predicate" -- FALSE for alpha_tbi_probe.py, whose wait_prompt (:182-196) is a real readiness wait spelled
      `"gxemul>" in buf[last_pos:].lower()`, invisible to the census (grok);
    - "20 promptless pty probes ... that moved no census" -- they moved the promptless census and the denominator; they
      moved no PIN (glm);
    - "the LAST TWO LINES of the list" -- positional; the next --grandfather makes it false (agy, glm, kimi-k3): anchor by
      the first NAME of each appended block;
    - fresh-clone sentence: a clone reds the promptless row as well as the denominator, and the count is 70 only while
      NONE of the three is committed (codex, grok);
    - "FILED (armbdtreadiness)" -- the row did not exist (codex): FILE it in this round's records;
    - the surviving "PRESENT VALUE OF 2" comment near the whole-buffer rows (codex).
C7  LC_ALL=C on the name row's sort (agy, glm): the pin is a literal; today's pair cannot reorder (opus measured four
    locales, and the battery's en_US.UTF-8 is not installed on the WSL image -- it falls back to C), so this is a flake
    guard, not a false pass.  Cheap; TAKEN.

## FILED (new row `hygienecensusholes`, MED, harness) -- pre-existing census holes, MEASURED by opus, none introduced here
  e1 another buffer name (`out.rstrip()...`); e2 the predicate split across lines; e5 `strip()` for `rstrip()`; e3
  `endswith (` with a space; **e9 `buf.endswith (">")` -- the #37 bare defect itself -- walks past the #37 row with one
  space**; e4 a slice compare (`buf.rstrip()[-7:] == "GXemul>"`, which the round's own `move` control used); e7 a
  filename with a space (bare `xargs` in `_ptylist`); dL3 a probe in a subdirectory (the promptless scan looks basenames
  up in `$HERE`); codex's `_mark = -len(self.buf)` (the fresh-mark row checks the call spelling, not the value);
  kimi-k3's second session with no predicate inside an already-counted file; glm's enumerator-narrowing then --write.
  **The census is a SPELLING census** (glm): it guarantees spellings, not readiness.  Ranked below live defects.
  Also filed to #529's own round: crime_width_probe.py:937's "six KINDS" comment does not describe the literal domain
  (eight distinct op strings, 46 entries -- codex).

## DISAGREEMENTS -- settled by measurement, not vote
  D1 "a single-quoted site reds the unknown row" (minimax, deepseek, glm, kimi-k3 -- all packet-fed) vs "it evades every
     row" (codex, grok, agy, opus).  SETTLED BY OPUS'S RUN c1: allends 49 -> 50 and full 49 -> 50, so unknown stays 0 and
     all eleven rows stay green.  The packet did not inline the `full` pattern, which accepts both quotes; the four
     packet-fed seats reasoned correctly from what they had and named the premise they could not settle (glm and kimi-k3
     explicitly) -- a CONDITIONED answer, scored as such.
  D2 SHIP (glm, minimax) vs DO NOT SHIP (five seats + opus's measurements).  Not a vote: C1, C2, C5 are measured false
     passes in this round's material; glm itself listed C5's halves and C7 as defects, calling them non-blocking.
  D3 "the new name row alone could reorder under another locale" -- all agree it fails CLOSED; opus measured no change
     under four locales.  C7 taken as a flake guard only.
  D4 (e) "every grandfathered name really is promptless" -- TRUE under the census's lexical proxy (codex enumerated all
     42; grok, agy); FALSE as a property for crime_width (hidden, C1) and misleading for alpha_tbi / drive_guest (real
     readiness waits the proxy cannot see -- C6, and the gate's own drive_guest note).

## OWNER QUESTIONS raised by this pass
  O1 a THIRD untracked promptless probe (crime_width_probe.py, #529) -- grandfathered by name under ruling 2's principle;
     reversible if the owner prefers converting it (its session is timed-drain).
  O2 an EXPIRY on the whole-buffer allowlist entry for arm_bdt_probe.py (codex, grok, agy, glm, kimi-k3): the house idiom
     exists (gate_offline.sh exempt_expired, gate_asan_sweep.sh ab_expired).  Needs an owner-chosen date; not added.
