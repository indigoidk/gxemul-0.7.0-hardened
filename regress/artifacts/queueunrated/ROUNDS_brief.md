# PASS-2 REVIEW — three complete rounds, held uncommitted for the 2026-09-09 adjudication

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Today you corrected five separate counts of mine and
two premises; another seat refuted my reasoning about a mask twice. **Assume at least one of these
three diffs is wrong or under-witnessed and find it.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  Nothing here is committed; HEAD is `a264a34` and all
three rounds sit in the working tree.

**VERDICT LINE FIRST.**

## The three rounds

Each is test-first: a rung-3 witness RED on the committed build, the fix, then the SAME script GREEN.

    #505 sgirergbroundtrip  RGB GET read the pad byte and dropped red
                            detector regress/sgi_re_rgb_probe.py, 10 rows
                            prefix10row 4/10 -> base 10/10 ; nullmedium 1/10
                            kill table 6: M13_composite 9/10, M14_compmirror 7/10, both KILLED
    #506 lcaconfwidth       the LCA kill diagnostic named a value the guard ACCEPTS
                            witness regress/lca_confwidth_probe.py   HEAD 4/6 -> fix 6/6
    #507 alphaswpctxptbr    swpctx assigned apcb_ptbr twice and apcb_flags never
                            witness regress/alpha_harness_probe.py   HEAD 7/10 -> fix 10/10

## The diffs, inlined

```diff
diff --git a/src/cpus/cpu_alpha_palcode.c b/src/cpus/cpu_alpha_palcode.c
index e6d92dc..69846b7 100644
--- a/src/cpus/cpu_alpha_palcode.c
+++ b/src/cpus/cpu_alpha_palcode.c
@@ -279,7 +279,13 @@ Make sure they are correct, as documented in the Manual.
 			cpu->cd.alpha.pcb.apcb_cpc = new_cpc;
 			cpu->cd.alpha.pcb.apcb_asn = new_asn;
 			cpu->cd.alpha.pcb.apcb_unique = new_unique;
-			cpu->cd.alpha.pcb.apcb_ptbr = new_flags;
+			/*  #507: was `apcb_ptbr = new_flags' -- a field-name transposition that
+			    assigned apcb_ptbr TWICE (here and three lines up) and apcb_flags NEVER,
+			    while every other field in this block is assigned exactly once.  Two
+			    consequences: apcb_ptbr ended up holding the flags word, and the incoming
+			    context's flags were dropped -- so the NEXT save published a never-loaded
+			    word back into the outgoing PCB, wiping what the guest planted.  */
+			cpu->cd.alpha.pcb.apcb_flags = new_flags;	/*  #507  */
 			cpu->cd.alpha.pcb.apcb_decrsv0 = new_decrsv0;
 			cpu->cd.alpha.pcb.apcb_decrsv1 = new_decrsv1;
 
diff --git a/src/devices/dev_lca.c b/src/devices/dev_lca.c
index 4f09c65..1e40144 100644
--- a/src/devices/dev_lca.c
+++ b/src/devices/dev_lca.c
@@ -201,8 +201,14 @@ DEVICE_ACCESS(lca_ioc)
 			/*  Only bit 0 is implemented so far, the PCI bus 0 vs
 			    bus non-0 selection bit.  */
 			if (idata & ~1) {
+				/*  #506: was `0x%x', (int)idata -- a 64-bit guarded value
+				    narrowed to 32 in the KILL diagnostic, so a write of
+				    0x100000000 trips `idata & ~1' and then reports "0x0",
+				    which is a value this same guard ACCEPTS.  The five
+				    sibling arms below already print the full width this
+				    way; this arm was the file's own outlier.  */
 				fatal("TODO: Write to unimplemented bit of"
-				    " IOC_CONF: 0x%x\n", (int)idata);
+				    " IOC_CONF: 0x%" PRIx64 "\n", (uint64_t)idata);
 				exit(1);
 			}
 		}
@@ -310,7 +316,7 @@ DEVICE_ACCESS(lca_ioc)
 		    writeflag == MEM_WRITE? "write" : "read", (int)
 		    relative_addr);
 		if (writeflag == MEM_WRITE)
-			fatal(": 0x%x", (int)idata);
+			fatal(": 0x%" PRIx64, (uint64_t)idata);	/*  #506  */
 		fatal(" ]\n");
 		exit(1);
 	}
```

## The questions

**Q1 — IS ANY OF THE THREE FIXES WRONG?** Read each against its enclosing function's real control
flow, not against my description. `#507` in particular is a one-token field-name change inside a
nine-line assignment block.

**Q2 — WHICH IS THE MOST UNDER-WITNESSED?** For each, name the smallest edit that keeps the witness
green while re-opening the defect, and name the row you expect to stay green. Two of today's fix
reviews found exactly this: a correct fix whose witness could not distinguish it from a lesser one.

**Q3 — DO THE COMMENTS CLAIM MORE THAN THE CODE DOES?** Each fix carries a `/* #NNN: */` block. **A
comment asserting completeness above an incomplete list is the defect `#507` itself repaired** —
`:275` said "Update all variables in the pcb simultaneously" above a list that did not. Check mine for
the same shape.

**Q4 — ANY INTERACTION BETWEEN THE THREE?** They touch three different files, but `#505` and the
`sgirebufuninit`/`sgimtedepth4dead` family share `horrible_getputpixel`. Does `#505`'s change alter
what those open rows describe?

**Q5 — WHAT IS MISSING FROM THE RECORDS?** The CHANGELOG blocks are in the working tree. **Name any
claim in them a measurement does not support**, which is the L4 class this project fixes in-round.

## What I am not asking

Do not write patches and do not run anything. **Nothing ships until the flagship adjudication.**

**If, while verifying a claim, you found something ELSE — say so.**
