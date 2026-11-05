# ERRATA for r5_20261105/PRETABLE_5.out -- records 6, 2026-11-05 (adj_p5_20261105/ADJ_MYTHOS_local.md R4, R8, R9, R10)

PRETABLE_5.out is the pre-table prediction and is not rewritten (its mtime precedes table5/SCORES.txt and must stay so); each item
quotes the sentence it corrects.  Line numbers are PRETABLE_5.out's.

1. **:20 (R9).**  Quoted: "VACUOUS (semantically no-op at the position; not mutants, not built): 6676".
   Correction: "no-op under the Boolean-latch abstraction for a single access" -- semantic_vacuous (memc_variants_5.py:703-728)
   tests `bool(new) != bool(cur)` over Boolean reach states for one access (:716-721).  A cross-call escape of the form
   `if (idata & 2) D ^= idata` after the default test (D: 1 -> 2 -> 0 over stores of 0x03 then 0x02, then a re-announce) is inside
   this 6,676 and is NOT a semantic no-op.  The ungated `M ^= idata` at the memconf arm's end is the same kind of escape but is NOT
   inside the 6,676: the walker's idata = 1 sample clears a set latch (:698, :716-721), so it was built -- :7792-7794
   L_ME_M_xori_any, NOCHANGE, measured 206/206 at SCORES.txt:2917.  On this probe both are undetected (every session leaves both
   latches truthy).  Disclosed in the probe's CONTRACT (the cross-call caveat); filed in r6_20261105/FILING_memccoverdebt.md item 6.
   (Second reading, rec6 R9: this item first put both among the discarded cells.)

2. **:26-27 (R8).**  Quoted: "UNOBSERVED = the statement fired and changed the state but no later access read it back".
   Correction: "UNOBSERVED = the statement fired and changed the state (a field byte or a latch truth value, the sticky `changed`
   of memc_variants_5.py:358, :388-389, :407-408) and the probe's trace is nevertheless the fix's -- a change with no observed
   difference, cancellation included".  The survivor summary's DA ob2s (:9579), DT ob2s (:9609), H ob3c (:9615), TL ob3c (:9696)
   and TL ob4c (:9697) groups are toggles that WERE read back: R17's two word default stores at +0x1c and +0x11c toggle twice and
   cancel, R12's and R16's paired served stores likewise.

3. **:28 (R4).**  Quoted: "UNFIRED and UNOBSERVED are predicted SURVIVORS of the 206 rows inside the denominator."
   Correction: inside the WALK's denominator (the superset of :18-19), not all inside CONS section 3's alphabet: the CI/CR groups
   under idata bits 8..31 (48 summary lines, :9461-9508) and the ME groups (12 summary lines, :9632-9643) are the walk's additions
   (T5_PREP.md:31-32, :36-37, :68-69).  In representatives (:7788-9459, the unit :25 counts): UNFIRED 106 = 44 supplementary + 62
   inside; UNOBSERVED 411 = 21 supplementary (ME) + 390 inside; so 452 of the 517 are inside the ruling's alphabet and 65 are the
   implemented superset.  (Second reading, rec6 R4: this item first said "457 (58 + 399) / 60", counting summary lines as groups.)

4. **:8167-8178 and :8199, :8211 (R10, NB3 and NB4).**  Quoted (:8199): "K_MB_chiprev_and_D  exact: none -- NOCHANGE ... equiv
   (50): ... nC ... W.nC ..." and (:8211): "K_MB_memconf_and_D  exact: none -- NOCHANGE ... equiv (51): ... nC ... W.nC ...".
   Clarification, not a mis-prediction: these two representatives carry NB4 (`&=` into chiprev or memconf at the first memconf
   store under `!controller`) as equivalents, are among table 5's 665 green variants, and are classed NOCHANGE -- so they are
   ABSENT from the UNFIRED/UNOBSERVED survivor summary at :9460-9697 although they pass every row.  NOCHANGE here is
   probe-relative (:27's "probe-equivalent"): every controller-0 first memconf store the rows make is 0x07, 0xff or 0xffffffff, and
   0x01 & 0x07 = 0x01, 0x03 & 0x07 = 0x03; a controller-0 first store of 0x00 would zero both fields.  NB3 (:8167-8178, the four
   `|=`/`^=` keeps into chipid/chiprev at MB under `controller`, UNOBSERVED) is a gate x first-store x operator three-way joint
   that R9's 0x00 first controller-1 store cannot expose (0x00 is the OR/XOR identity).  Both are disclosed in the probe's
   CONTRACT, (3) and (4), and filed with their remedies (FILING items 3 and 4).

5. **:16 (superseded reference).**  Quoted: "THE DENOMINATOR (CONS_MYTHOS_local.md section 3, walked cell by cell ...)".
   The denominator is unchanged and stands; CONS section 3's CLOSURE claim is superseded by the pass-5 ruling (the walk measured
   coverage, the floor is narrower and has no surviving cell).  See ERRATA_T5_PREP_20261105.md item 1.
