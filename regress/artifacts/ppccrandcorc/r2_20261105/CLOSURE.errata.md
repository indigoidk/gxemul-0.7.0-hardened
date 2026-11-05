# CLOSURE.md -- errata (2026-11-05, round 3; pass 3 = p3_20261105/codex_codex_r575_p3.txt)

CLOSURE.md is a record of round 2 and is not rewritten.  Each item quotes what it corrects.

## R2 -- "WHY THESE FOUR AND NO FEWER" is false: three rows would have closed the 239 cells

CLOSURE.md, "WHY THESE FOUR AND NO FEWER", says:

> crandc clear-before-read needs BT == BB with b = 1 (want 0), a different seed: its own row (BT == BA is invisible for crandc:
> a is forced to 1-want, and the early clear changes a only when b = 1, where the result is 0 either way).  [...]  The two crandc
> needs (want 1 uniform ones; BT == BB with b = 1) and the two crorc needs (uniform ones; uniform zeros) are pairwise incompatible
> seeds, so four rows is the minimum for single-instruction sessions.

"a is forced to 1-want" carries the INVERSE pre-set into a design that, two sentences earlier, already pre-sets EQUAL.  With an
EQUAL pre-set, the single row

    crandc 16,16,31 over 0xfffffffe, want 1 (a = CR[16] = 1 pre-set EQUAL, b = CR[31] = 0)

sees the clear moved before the reads (a -> 0, result 0), every BB field mask 0..30 (CR[m] = 1 -> b = 1 -> 0), BB <- BT (CR[16] =
1 -> 0) and the BB read masks & 3 / & 7 (CR[30] = 1 -> bb != 0 -> 0): everything `64 crandc bbmask' and `64 crandc order' close
together.  Verified by simulation in round 3 (r3_20261105/v575c.py, the same 239 cells): the 62 rows plus {crandc 16,16,31, `64 crorc
bamask', `64 crorc bbmask'} leave the same 4 EQUIVALENT cells and the same 1 disclosed cell undetected as the four round-2 rows do --
three rows, not four, was the minimum.  The four rows STAY as they are: table 2 measured them (table2/SCORES.txt, 27 variants exactly
as predicted), and round 3 adds its rows beside them (r3_20261105/CLOSURE3.md).

## The vocabulary was narrower than the classes it put in scope (pass 3, B1-B4)

CLOSURE.md, ENUMERATION:

> the read mask `& 1' widened to `& 3' and `& 7' at BA and at BB; the clear moved before the reads, deleted, or replaced by a
> toggle; the set deleted or `|=' -> `^='

and "DENOMINATOR: 239 cells".  Those statements are true of the 239 cells, and every prediction in CLOSURE.md stands for them.
But the read-mask sites (cpu_ppc_instr.c:2732-2733, :2759-2760) and the set statements (:2736, :2763) admit other single-constant
edits the enumeration did not list: `& (1|1<<k)' for k = 2..31 and & 0, 2, 4, 6 at each read, and the set literal 1 -> 1+2^k.
Of those, 54 (codex B1-B4: crorc BB read masks k = 2..30, crorc BA `& 0x8001', crandc set literals k = 7, 9, 11..30, crorc set
literals k = 26, 27) plus k = 31 at crorc BB and at the crandc set literal survive the 66 rows.  Round 3's enumeration (453 cells)
and its four whole-CR rows close them: r3_20261105/CLOSURE3.md.  The sentence in the probe's clause (e) that "with the four rows
every cell is red by simulation except four EQUIVALENT cells" was true of the 239 cells only; the probe's clause (e) now says so.
