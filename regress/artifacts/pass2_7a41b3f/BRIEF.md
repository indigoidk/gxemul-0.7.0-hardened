# RETROSPECTIVE PASS 2 on `7a41b3f` — rounds `#505` `#506` `#507` `#508`

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**This commit shipped WITHOUT a pass 2, and the pre-commit gate refused the NEXT commit until
this pass exists.** So the honest framing is: four rounds are already in the tree, and I am asking
whether they should have been. **Closure changes the LICENCE, never the truth-value.**

A recent panel had seven of nine seats confirm a premise stated wrongly, and the pass 1 and pass 2
on the round AFTER this one found three errors in my brief each. **Check the premises, not just
the derivations.** A seat that re-derives a premise from something this brief did NOT give it is
worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul
exist under the project root and are NOT this fork. Line numbers off by hundreds mean you are
reading one of them — say so rather than reconciling.

**If you cannot read files that is expected** — the ENTIRE product diff is inlined below, verbatim
and complete (5 hunks, 63 changed lines, checked before this brief was sent). Name any premise
you cannot settle from the packet.

**Where this brief states an ARITHMETIC claim, ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST.**

### If you can read files
Scope your reading to `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`.
**Do not read `regress/artifacts/` or `tools/pipeline/ledger.json`.**

---

## 1. WHAT THE FOUR ROUNDS CLAIM, one line each

* **`#505` sgirergbroundtrip** — `dev_sgi_re.c`: the RGB colour arms are off by one byte position.
  The PUT arm writes three channels at `buf[0..2]` with an explicit pad at `buf[3]`; the GET arm
  read `buf[1..3]`, so an RGB pixel did not survive a round trip.
* **`#506` lcaconfwidth** — `dev_lca.c`: a 64-bit guarded value was printed through `(int)` in a
  terminating diagnostic, so the message could name a value the guard ACCEPTS. Two sites.
* **`#507` alphaswpctxptbr** — `cpu_alpha_palcode.c`: `swpctx` assigned `apcb_ptbr` twice; the
  second write put `new_flags` into it, so `apcb_flags` was never loaded and the next save
  published a never-loaded word.
* **`#508` alphapfnoffset** — `memory_alpha.c`: the page-table walk returned `PFN << pageSizeShift`
  and dropped the within-page offset, so every walked access resolved to the page's first bytes.

**Each shipped with a rung-3 witness measured RED pre-fix and GREEN post-fix with the same
script.** Three of the four gained an extra row because a fix review refused the round — the
witness could not distinguish the fix from a lesser edit.

## 2. THE ENTIRE PRODUCT DIFF, verbatim

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
 
diff --git a/src/cpus/memory_alpha.c b/src/cpus/memory_alpha.c
index 3ab5f39..7337fcf 100644
--- a/src/cpus/memory_alpha.c
+++ b/src/cpus/memory_alpha.c
@@ -165,7 +165,21 @@ if (vaddr == 0xfffffffd80000000ULL) fatal("AYONA3\n");
 		goto not_found;
 	}
 
-	(*return_paddr) = ALPHA_PTE_TO_PFN(pte3) << pageSizeShift;
+	/*  #508: was just `PFN << pageSizeShift' -- a PAGE BASE.  memory_rw then takes
+	    `offset = paddr & offset_mask', which was therefore always zero, so every
+	    walked access resolved to the page's first bytes.  Measured: a cold guest ldq
+	    of vaddr+8 returned the vaddr+0 value.  A debugger watchpoint on a walked page
+	    landed at the base for the same reason.
+	
+	    The mask is derived from pageSizeShift rather than written as 0x1fff: this
+	    function already has TWO names for 13 (ALPHA_PAGESHIFT and this local), and a
+	    literal beside the shift is how the two drift.  `|' rather than `+' because
+	    that is what every other CPU's walk in this tree writes; here they are equal,
+	    the shifted PFN having bits 12:0 clear.  The TODO below STAYS: `flags' is
+	    still ignored, the protection bits untested, and `return 2' still reports
+	    every walked page writable.  */
+	(*return_paddr) = (ALPHA_PTE_TO_PFN(pte3) << pageSizeShift)
+	    | (vaddr & ((1ULL << pageSizeShift) - 1));
 
 	// TODO.
 	return 2;
diff --git a/src/devices/dev_lca.c b/src/devices/dev_lca.c
index 4f09c65..7837239 100644
--- a/src/devices/dev_lca.c
+++ b/src/devices/dev_lca.c
@@ -201,8 +201,17 @@ DEVICE_ACCESS(lca_ioc)
 			/*  Only bit 0 is implemented so far, the PCI bus 0 vs
 			    bus non-0 selection bit.  */
 			if (idata & ~1) {
+				/*  #506: was `0x%x', (int)idata -- a 64-bit guarded value
+				    narrowed to 32 in the KILL diagnostic, so a write of
+				    0x100000000 trips `idata & ~1' and then reports "0x0",
+				    which is a value this same guard ACCEPTS.  The five
+				    sibling arms below already print the full width this
+				    way; this arm was the outlier among the VALUE-guard
+				    diagnostics.  (Not the file's only narrowing site --
+				    the default arm below has the same cast, and this
+				    round fixes it too.)  */
 				fatal("TODO: Write to unimplemented bit of"
-				    " IOC_CONF: 0x%x\n", (int)idata);
+				    " IOC_CONF: 0x%" PRIx64 "\n", (uint64_t)idata);
 				exit(1);
 			}
 		}
@@ -310,7 +319,7 @@ DEVICE_ACCESS(lca_ioc)
 		    writeflag == MEM_WRITE? "write" : "read", (int)
 		    relative_addr);
 		if (writeflag == MEM_WRITE)
-			fatal(": 0x%x", (int)idata);
+			fatal(": 0x%" PRIx64, (uint64_t)idata);	/*  #506  */
 		fatal(" ]\n");
 		exit(1);
 	}
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 2a81d79..b3239b4 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -324,7 +324,30 @@ void horrible_getputpixel(int put, struct cpu* cpu, struct sgi_re_data* d,
 			*color = buf[0];
 			break;
 		case DE_MODE_TYPE_RGB:
-			*color = (buf[1] << 24) + (buf[2] << 16) + (buf[3] << 8);
+			/*  #505: this read buf[1..3] while the PUT arm above
+			    writes the three channels at buf[0..2] and an
+			    explicit pad at buf[3] -- so an RGB pixel did not
+			    survive its own round trip, shifting one byte left
+			    with a zero fill on every RGB source read.
+
+			    The PUT arm is the authoritative one, and the
+			    warrant is OUTSIDE this function: dev_sgi_gbe.c's
+			    scanout reads the same tile memory back for display
+			    as (buf[0]<<24)+(buf[1]<<16)+(buf[2]<<8)+buf[3],
+			    then CRMFB_MODE_TYP_RGB8 takes R,G,B from bits
+			    31..24, 23..16 and 15..8 -- byte 0 is R and byte 3
+			    is UNUSED.  So the pad sits at buf[3] because the
+			    consumer ignores buf[3], not because PUT writes a
+			    zero there; that is what makes this non-circular.
+			    The RGBA and ABGR PUT arms independently agree --
+			    both lay [R,G,B,x] in memory despite opposite
+			    register word orders -- which leaves this GET the
+			    lone container outlier among the 32-bit arms.
+
+			    The low byte stays ZERO on purpose: RGB carries
+			    three channels, so a corrected read of 0xaabbccdd
+			    yields 0xaabbcc00, NOT the source word.  */
+			*color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8);
 			break;
 		case DE_MODE_TYPE_RGBA:
 			*color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8) + buf[3];
```

## 3. WHAT HAS CHANGED SINCE, and it bears on two of these files

**A later round (`#509`) and a probe-helper audit both found things in this territory. I am
telling you because they may bear on whether these four are right, not to steer you:**

* `dev_sgi_re.c`'s GET arms compute `buf[i] << 24` on a promoted `uint8_t` — undefined for a byte
  `>= 0x80`. That is filed separately (`sgirebufshiftub`). **`#505` edits the RGB GET arm.
  Does its correction sit on that UB, and does that change the disposition?**
* An audit found that **five `negate=True` rows across three of this commit's own witnesses went
  GREEN on a NON-OBSERVATION** — `"absent"`, `"died"`, or `0x0`. They were repaired afterwards and
  measured in both directions. **The question for you: does that change what this commit's
  measured HEAD scores MEAN?** The equality siblings reded on those states, so I believe the
  detectors never escaped and only the rows' own notes overclaimed — **check that belief.**

## 4. QUESTIONS

1. **The premise audit.** Is each fix correct as a repair of the defect it names? Is any of the
   four a repair of something that was not broken, or a partial repair presented as complete?
2. **Which of these four would you NOT have shipped, and why?** All four are already in the tree,
   so this is the question that matters. **A pass that ratifies all four has either had four good
   rounds or has stopped arguing, and only a seat can tell me which.**
3. **Do the added COMMENTS claim anything the code does not do?** This project has repeatedly
   shipped a records correction that was itself wrong.
4. **`#508` deliberately KEPT a `// TODO.` line.** `flags` is never read and the protection bits
   are untested, so `return 2` means writable unconditionally. **Was keeping that TODO right, or
   does the round owe a disclosure it did not make?**

If, while verifying a claim, you found something ELSE — say so.
