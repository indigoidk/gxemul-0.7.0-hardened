# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `heldrecedits` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `heldrecedits`, state `open`)

**title:** #560 and #561 HELD 30 ruled corrections on 2026-10-06 that no ledger row carries: 29 src/ comments (#560's 12, #561's 17; each owes est/ byte-identity and build-tree propagation) and #560's `hrec extra' comment in regress/diff_ieee_store.c (:296-301) -- the bug file's #560 and #561 sections end `Still owed'

**state_note (head):** [2026-10-20, widened by the late-review adjudication (regress/artifacts/argonlate_20261020/adj/, A3)] One more held src/ comment, from #565's records: src/cpus/cpu_ppc_instr.c:2470-2471, X(rldicl)'s note on its witness, reads `The wants come from the rldiclx RTL in the architecture manual, not from this tree' -- true of the witness's rldicl rows, too broad for its rldimi, rlwinm and rlwimi rows and its `bits32 rld bad' (the tree's own decoder text).  Ruled replacement (GPT-6 Astra's wording): `The rldicl general-register expected values come from the rldiclx RTL in the architecture manual, not from this tree'.  Held, not applied -- Fable 5.1, Grok 4.7, GLM 5.3 and Argon; GPT-6 Astra would have included it and accepted a source commit's pass 2 -- because a src/ hunk would have made the records unit a source commit owing its own pass 2; carried on this row rather than in a round block (Fable 5.1).  Reconciled against HEAD 1a59a47e; like the rest, it is re-checked against HEAD before it is applied.  ||  filed 2026-10-18 with ip30abortkill's closure records.  The lists are OUTSTANDING_BUGS.md's `### #560' section (HELD (20)) and `### #561' section (HELD (17): every src/ comment, each with its ruled replacement under regress/artifacts/recordfix_20261002/adjudication_20261006/EDITS_561.json key `held'); #560's rulings are its ADJ_FINAL.md and ADJ_HREC_FINAL.md.  This row carries the 30 of those 37 that no ledger row carried: the 29 src/ comments -- #560's 12, dev_pcc2.c's among them (held then because the peer session's uncommitted work sits in that file), and #561's 17 -- and #560's `hrec extra' (diff_ieee_store.c:296-301).  #560's other seven held sites (hrec 2, 9, 10, 19a-c, 20) are hrecordowed's members hbundle_regress15:F7, hbundle_tools1:F5/F6 and hdiffieeestore:F6/F7, and stay there (GPT-6 Astra, the confirm).  Four of the 29 are #561's places 7-10, dev_sgi_ip30.c's stale comment counts, which ip30abortkill's closure check first proposed to move onto ip30abortresidual -- a split of one held set (Grok 4.7).  The lists are as of 2026-10-06, and #565 has since corrected hrec 2's claim, so the round reconciles each item against HEAD before applying it.

**The drafter's own reading:** STILL PRESENT: YES -- `src/cpus/cpu_ppc_instr.c:2483`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 508e9181..c8c2ecc9 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -2480,9 +2480,10 @@ X(rldicl)
 		        pass2_20260910/opus_threemachine.log -- bareppc, testppc
 		        and macppc -e g5 (the Power Mac G5, a PPC970 and therefore
 		        64-bit), all three zero pre-fix and architectural post-fix
-		    The wants come from the rldiclx RTL in the architecture manual,
-		    not from this tree; the encodings were re-read by the tree's own
-		    disassembler, a different code path from this handler.
+		    The rldicl general-register expected values come from the
+		    rldiclx RTL in the architecture manual, not from this tree;
+		    the encodings were re-read by the tree's own disassembler,
+		    a different code path from this handler.
 
 		    *** TWO EDITS TO THIS LINE PAIR ARE MEASURED WRONG, AND THEY
 		    ARE WRONG IN DIFFERENT WAYS.  BOTH ARE TEMPTING. ***
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 2444-2514 (`+` marks a line the diff added or the point of a deletion)

```c
 2444|  X(rldicl)
 2445|  {
 2446|  	int rs = (ic->arg[0] >> 21) & 31;
 2447|  	int ra = (ic->arg[0] >> 16) & 31;
 2448|  	int sh = ((ic->arg[0] >> 11) & 31) | ((ic->arg[0] & 2) << 4);
 2449|  	int mb = ((ic->arg[0] >> 6) & 31) | (ic->arg[0] & 0x20);
 2450|  	int rc = ic->arg[0] & 1;
 2451|  	uint64_t tmp = cpu->cd.ppc.gpr[rs], tmp2;
 2452|  	/*  TODO: Fix this, its performance is awful:  */
 2453|  	while (sh-- != 0) {
 2454|  		int b = (tmp >> 63) & 1;
 2455|  		tmp = (tmp << 1) | b;
 2456|  	}
 2457|  	tmp2 = 0;
 2458|  	while (mb <= 63) {
 2459|  		/*  #522 (ppcrldiclzero): this was `tmp |=', so the MASK was
 2460|  		    accumulated into the ROTATED VALUE and `tmp2' -- assigned 0
 2461|  		    just above and never assigned again -- was still 0 at the AND
 2462|  		    below.  THE DESTINATION WAS THEREFORE SET TO ZERO ON EVERY
 2463|  		    EXECUTION, for every source, rotate amount and mask begin.
 2464|  		    The `|=' also destroyed the rotated data by forcing every mask
 2465|  		    bit to 1, which is moot only because the result was ANDed with
 2466|  		    zero.  `rldicl' is the canonical 64-bit masking and zero-extend
 2467|  		    instruction (`rldicl rA,rS,0,32' is the standard 32-bit
 2468|  		    zero-extend), so this was wrong on the ordinary path for
 2469|  		    ordinary compiler output.
 2470|  
 2471|  		    MEASURED at rung 3 BEFORE this edit, on unmodified -E bareppc:
 2472|  		        artifacts/ppcrldiclzero/opus_ppc_rldicl_witness_20260910.py
 2473|  		        witness_committed.out  -- 19/27, 190 of 190 census cells
 2474|  		                                  wrong and all 190 returning zero
 2475|  		        witness_fix.out        -- 24/27, 0 of 190 wrong
 2476|  		    AND ON TWO MORE MACHINES, in a SEPARATE log -- an earlier draft
 2477|  		    of this comment named all three here while citing only the
 2478|  		    one-machine files above, which a pass-2 seat caught and then
 2479|  		    re-measured rather than merely reporting:
 2480|  		        pass2_20260910/opus_threemachine.log -- bareppc, testppc
 2481|  		        and macppc -e g5 (the Power Mac G5, a PPC970 and therefore
 2482|  		        64-bit), all three zero pre-fix and architectural post-fix
 2483|+ 		    The rldicl general-register expected values come from the
 2484|+ 		    rldiclx RTL in the architecture manual, not from this tree;
 2485|+ 		    the encodings were re-read by the tree's own disassembler,
 2486|+ 		    a different code path from this handler.
 2487|  
 2488|  		    *** TWO EDITS TO THIS LINE PAIR ARE MEASURED WRONG, AND THEY
 2489|  		    ARE WRONG IN DIFFERENT WAYS.  BOTH ARE TEMPTING. ***
 2490|  		      * REPLACING the `&' with `|' ships ROTL64(rS,SH) |
 2491|  		        MASK(MB,63) -- an OR where the architecture says AND -- and
 2492|  		        gets 126 of 190 cells wrong.  Built and measured as the
 2493|  		        M_NAIVE leg of killtable_20260910.
 2494|  		      * DELETING the `& tmp2' outright now ships ROTL64 ALONE, with
 2495|  		        the mask IGNORED.  (Before this fix it would have shipped
 2496|  		        the OR, because the mask was in `tmp'; witness_naive.out
 2497|  		        measured THAT function, not this one.  A warning written
 2498|  		        against the old code would be a wrong record here, which is
 2499|  		        what a pass-2 seat caught.)
 2500|  		    Either is worse than the original defect in one specific way:
 2501|  		    it removes the always-zero signature that makes this easy to
 2502|  		    spot while leaving the value wrong.
 2503|  
 2504|  		    The sibling `rldicr' below is correct and shows the other
 2505|  		    shape: it CLEARS bits in `tmp' and assigns `tmp' directly.
 2506|  		    `rldimi' and `rlwimi' have their own separate defects, both
 2507|  		    measured -- see the ppcrldimimask and ppcrlwimiwidth rows.  */
 2508|  		tmp2 |= ((uint64_t)1 << (63-mb));
 2509|  		mb ++;
 2510|  	}
 2511|  	cpu->cd.ppc.gpr[ra] = tmp & tmp2;
 2512|  	if (rc)
 2513|  		update_cr0(cpu, cpu->cd.ppc.gpr[ra]);
 2514|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_HELDRECEDITS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_HELDRECEDITS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
