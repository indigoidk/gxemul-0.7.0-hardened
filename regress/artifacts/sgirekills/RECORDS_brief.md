# #513 -- a records-only review of the composite, before commit

## 0. READING SCOPE AND WHAT THIS IS NOT

Read `GXEMUL-SEC/src/devices/dev_sgi_re.c`, `GXEMUL-SEC/regress/sgi_re_width_probe.py` and
`GXEMUL-SEC/regress/gate_arm.sh`. Please avoid `regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root -- it disagrees by
hundreds of lines and has none of these symbols.

*** THIS BRIEF ASKS FOR NO MUTANT, NO EVASION, AND NO GUEST SEQUENCE. *** You refused the pass-3
brief, correctly by your own lights, because it asked you to construct an edit that defeats a
detector. **Nothing here does.** I am asking only: **does the prose in these three files now say
what the code does?**

## 1. WHY THIS PASS EXISTS

Round `#513` has been through two adversarial passes and a class-closure repair. Across them, SIX
wrong records were found in my own edits -- by kimi, codex and grok independently:

* the enum's *"next free bit is 1 << 11; the enum ends HERE"* went false when the round took
  `1 << 11`;
* my LINEAR comment claimed the `len == 8` guard *"keeps tlbi even"* -- width does not imply
  alignment;
* the probe's contract header still described six live read kills the round had removed;
* the `VAL_HI` comment overclaimed what a second value buys;
* the `PRETABLE` clause-(d) enumeration omitted `odata`;
* the `tex xbit` row's own comment claimed it caught *"any `*_LEN`"* collision when it fired only
  six of eleven latch bits.

**Every one was in text I wrote during this round, and each was caught by a reader rather than by a
check.** The corrections have themselves been edited since. **A correction carries more authority
than the error, so it earns a second reading, not less of one** -- and this project has three
recorded instances of a correction repeating the error it corrects.

## 2. THE ONE QUESTION

**Does any comment, contract line or gate annotation in those three files now assert something the
code does not do?**

Please be concrete: quote the sentence, quote the code, and say which is wrong. I would rather
receive five findings I have to dismiss than miss one.

Specific things I know I touched and would like checked hardest:

**Q1. The enum block.** I demoted the stale next-free claim on `SGIRE_W_BADMODE` and moved a live
one onto `SGIRE_W_TEX_RD`, in the style the same file used for `SGIRE_W_PRIM_OP`. **Is the live
claim now correct, and is it on the last enumerator?** Does the demoted text read as demoted, or
could a future reader still take it as live?

**Q2. The two LINEAR read arms.** I corrected the alignment attribution at both. **Are they now
consistent with the OLDER write-arm comment above them**, which explains the CPU-side mechanisms
correctly? A correction that disagrees with a correct neighbour is worse than the original error.

**Q3. The probe's contract header.** It now carries `#497`'s and `#499`'s original text plus a
correction block. **Is the LIVE contract -- what this detector claims to catch -- stated anywhere
unambiguously**, or does a reader have to reconcile three layers to find it?

**Q4. The `tex xbit` comment.** It now describes firing latch bits 0-8 and discloses that bits 9
and 10 are not fired. **Does the disclosure state its reason and a settling fact**, or does it read
as an excuse? And is the bit table in that comment correct against the enum?

**Q5. `gate_arm.sh`.** The row list and both denominators moved 35 -> 44 -> 46 across this round.
**Do the comments beside them describe the CURRENT arithmetic**, or a superseded step?

**Q6. Anything else.** Including in text I have not listed -- especially any sentence that was true
before this round and is false now. That is the class that produced five of the six above.
