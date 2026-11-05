# REG_FIXES.md -- the #575 regress review's three record findings, applied at the landing (text only)

Source: `regress/artifacts/ppccrandcorc/regress_20261105/REG_MYTHOS_local.md` (Claude Mythos 5.1, run locally: `MYTHOSREG575: 41 CHECKS 0 FLOOR-BREACHES 3 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS`), section 5.  The packet it answered, as sent: `landing_20261105/REGRESS_575.md` (md5 f42f15fd393e5aaa5203d3c833746744).  Applied by the landing kit's reg_fixes_575.py and build_staged_575.py; nothing measured changes: no row, seed, want, instruction, gate check or product line.

## R2 -- regress/ppc_crlogic_probe.py, docstring clause (5): applied (verified again on a re-run)

The finding: "Block A :141-143 says 'the round-3 whole-CR rows carry ones only where the set-literal cells need zeros'.  The two read rows (`baread` over 0xfffffffe, `bbread` over 0xfffffffc) carry ones at 30 of 32 bits ... The sentence is true of the two setbits rows only."  (The seeds carry 31 and 30 ones; the corrected text says so.)

REPLACES (working tree, md5 55523a4198d42cc1b412584897eb9d35 before):

```
      destination -- the table seeds hold no ones there, the hi and round-2 pin sessions check only the destination, and the
      round-3 whole-CR rows carry ones only where the set-literal cells need zeros (CLOSURE3.md's appendix lists what they
      see incidentally: most crorc clear literals 1+2^k, k = 1..30, and no crandc one above k = 10); and a crandc body that
```

WITH (md5 141591f8a2de70bfbd9ad4038bcd40d8 after):

```
      destination -- the table seeds hold no ones there, the hi and round-2 pin sessions check only the destination, the two
      `setbits' rows carry zeros where the set-literal cells need them, and the two read rows (`baread' over 0xfffffffe and
      `bbread' over 0xfffffffc: ones at 31 and 30 of the 32 bits) see extra clears only incidentally (CLOSURE3.md's appendix
      lists what the whole-CR rows see: most crorc clear literals 1+2^k, k = 1..30, and no crandc one above k = 10; the
      regress review, R2, corrected "the round-3 whole-CR rows carry ones only where the set-literal cells need zeros");
      and a crandc body that
```

Proof, Python 3.12.10: `ast.dump` with the module docstring dropped, every string kept -- after == before: **True**; with every string constant masked -- after == before: **True**, after == `r3_20261105/table3/probe70_frozen.py` (md5 772576e7f1795ff8006c5884148e0fa8): **True**.  Longest line 143.  The staged copy is rebuilt from this file by build_staged_575.py, which re-applies the seven section-U rewordings and re-proves the same identities (PROBE_IDENTITY.md).

## R3 -- r3_20261105/CLOSURE3.errata.md, F4's red-set parenthetical: applied (verified again on a re-run)

The finding: "For crorc C=2 in the 64 session, crorc 12 (result 1) sets bit 20, which is CR[11], the destination of `64 crandc 11` (want 0): that row is red too, as are `edge crorc bt31`, `edge others`, `64 crorc bbread` and the 32-bit copies."

Checked before writing (a correction is not safer than what it corrects): `v575c.predict({"crorc": {"set_lit": 2}}, 70)` = `64 crandc 11`, `64 crorc 00`, `64 crorc 01`, `64 crorc 11`, `edge crorc bt31`, `edge others`, `64 crorc bbread`, `64 crorc setbits`, `32 crandc 11`, `32 crorc 00`, `32 crorc 01`, `32 crorc 11` -- the review's list plus the four the parenthetical already named.  The sentence is marked in place and a dated section appended that quotes it.  md5 68f9ffe72e66eb95670ee4cc01a9d8d2 before, 132af8532952a2b05c415c9e872b5f86 after.

## R1 -- regress/gate_ppc.sh, the #575 block's comment: applied to the STAGED gate; the working-tree edit is a patch

The finding: "gate_ppc.sh:343 (staged :296) says '453 cells: 56 escaped the 66 rows, 0 escape the 70'.  Read plainly, '0 escape the 70' is false: 36 EQUIVALENT cells and the 1 DISCLOSED crandc toggle are not red on the 70 ... The comment should say '0 undetected beyond 36 EQUIVALENT and 1 DISCLOSED'."

build_staged_575.py replaces, in the block it takes from the working tree, `0 escape the 70).  BEFORE the NetBSD` with the corrected text quoting it (STAGED_DIFFS.md prints the hunk).  The working-tree gate_ppc.sh is being edited in another block by another implementer, so it is NOT edited here: `wt_gate_r1.patch` (a unified diff) and `apply_wt_gate_r1.py` (an exact-string applier that refuses unless the old text occurs once, then checks the working-tree #575 block equals the staged one) carry it.  After the commit the working tree differs from HEAD in that comment until the patch is applied; post_575_wt.py reports it.
