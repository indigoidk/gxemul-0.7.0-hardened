## 7. Questions -- verdict line first, then answer each by number; say plainly what you could not check

1. **The rule.**  Does the landed file implement the ruled condition exactly -- `ERROR:` lines classified only when
   `rc != 0` OR stdout is empty?  Is there any path where a REAL wall or refusal (rc 1, empty stdout, codex's own
   `ERROR:` at column 0) now ends as exit 0, or where an rc-0 answer with a non-empty stdout ends as 7 or 8?
2. **The ANSI strip.**  `sed "s/${ESC}\[[0-9;]*[A-Za-z]//g"` over the whole stderr, then `grep '^ERROR:'`.  Is the
   expression right for the measured shape (`ESC[1m ESC[31m ERROR: ESC[0m ESC[0m`)?  Name any ANSI form it misses
   (OSC `ESC]...`, a lone `ESC[K`, a carriage return) that could leave a real codex diagnostic unmatched, and say
   whether that form has any instance on record or is hypothetical.  Can the strip CREATE a column-0 `ERROR:` that was
   not one before (e.g. a quoted line whose only prefix was a colour code)?  If so, is that a regression against the
   production copy, and does the classify-only-on-failure condition bound it?
3. **The identity check.**  Exit 5 when the header names a model other than the one asked, compared AFTER the Daybreak
   fallback against the fallback model.  Is `head -n 40` a safe window for the header?  Can a quoted `model:` line from
   streamed source ever be read as the header (the header precedes the brief in every log on record)?  And section 3's
   first bullet: is UNVERIFIED-not-failed right?
4. **The controls (section 6).**  Each behaviour the landing changes should red on the BEFORE launcher and green on the
   AFTER launcher: Q3 and A1 (the ANSI strip), M1 and D2 (the identity check).  Is any control vacuous -- green on both
   for a reason other than the one it names?  **What is the smallest edit to the landed file that passes all 30 controls
   and breaks a ruled property?**  (A sketch is fine; do not build anything.)
5. **Records.**  The landing will close `cxlaunchquotation` (witness `harness:regress/artifacts/cxlaunchland_20261016/
   RECEIPT.txt`) and `cxlaunchdaybreak`, and mark the bug-file entry `cxlaunchwallfp` MERGED into it (its "key the stderr
   test on codex's error block at the END of the stream" fix shape is the refinement the ruling withdrew).  Anything wrong
   with closing them on this evidence?
6. **Which of my dispositions is wrong?**  Name the count you checked.
