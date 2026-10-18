**Your token: `GROK_RCDELTA_20261018`** -- open your answer with it.

# `sgirandomcolour`'s closure records -- the DELTA pass (pass 2 of the records review)

## 0. What this is

Pass 1 reviewed ten corrections that apply the 7n-5 ruling (Fable 5.1, 2026-10-09; GPT-6 Astra confirming) to the records of the ledger row `sgirandomcolour` (round `#519`, committed as `fd15065`).  Its seats raised five flags and named several uncorrected sibling sentences (E5).  Each was applied.  This pass reviews ONLY what changed.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD 620ddd09; ignore any other `src/` you find.  READ-ONLY: write nothing to any project tree.

## 1. E1 -- the ruling, verbatim (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md, lines 60-102)

E1:60  ## 7n-5.  FLOOR OR DEBT -- ARE A DERIVED-COORDINATE ESCAPE AND A VALUE SLICE THE SAME SPECIES?
E1:61  
E1:62  ### 1. Still live?  PARTLY OVERTAKEN, in both halves, with three wrong records left standing.
E1:63  
E1:64  * **The doctrinal half was decided on 2026-09-25**, after this question was filed: the flagship D1 ruling on `#549` v6 pinned *"'TESTS' MEANS MASKS OR COMPARES AS A CASE, NOT 'DEPENDS ON'"* -- a relational compare "tests NO bit: its generating set is its three regions, below / at / past the bound", a slice of a compared value crossed with a floor cell is clause (e), and *"grading by consequence would reopen #548"*.  7n-5 asks whether a data-flow test ("flows into the address operand") promotes an untested input to a floor axis; D1 answers no, two weeks after the question.
E1:65  * **The instance half was decided on 2026-09-12 by the committed probe itself.**  `regress/sgi_re_colourdefault_probe.py:26-28`: *"CONTRACT -- #519 closure design, 2026-09-12.  This is the controlling coverage contract; older CONTRACT/CLOSED/COMPLETE claims below are historical and are superseded wherever they claim a larger domain or describe missing coverage."*  `:50-51`: *"OUTSIDE: exhaustive coordinates, tile indices, descriptor payloads, raw mode bits, foreground values ..."* -- descriptor payloads ARE the TLB array contents.  The controlling contract already files the gap as clause (e).
E1:66  * **What is left standing against both:** (i) the `sgirandomcolour` note (row text at `scratchpad` line 962): *"the array VALUE is a genuine floor-shaped gap ... Filed as OWED"*; (ii) the probe's historical block `:614-617`: *"the one exception that is genuinely FLOOR-shaped ... filed as owed rather than fixed"* -- formally superseded by the `:26-28` banner (it "describes missing coverage"), but a reader landing there by grep reads it as live; (iii) `regress/pass2_ledger.tsv:159` (the fd15065 receipt): *"Disclosed under (e): bare-predicate mutants with an uninitialised buf; the exact historical M28/M28r edit"* -- the four derived sweeps and the SAMPLED axes the probe discloses at `:593-608` are absent from the receipt's list.  Three L4s.
E1:67  * **Never measured, and that is honest rather than a gap:** table 4 (09-11, M1..M41) and table 5 (09-12, 15 legs) contain no `tileptr & 0xfff00000`, `mode & 1`, `x & 1` or `y & 2` leg; the probe says so (`:607-608` "DERIVED, not measured -- no table has run them").  The round's state is `in work` ("closure records owed"), so the corrections below have their vehicle.
E1:68  
E1:69  ### 2. The two-minute check that turns "predicted 77/77" into "equivalent by construction".
E1:70  
E1:71  `src/devices/dev_sgi_re.c` at HEAD: `tileptr = d->re_tlb_[abc][tile_nr] << 16` (`:258-262`), `tileptr = 0x80000000 | (re_linear_a[tile_nr] << 12)` (`:267`), the valid-bit test `if (!(tileptr & 0x80000000))` (`:312`), then **`tileptr &= ~0x80000000;` at `:319`** before the stores at `:374`/`:377`.  Every descriptor the committed probe drives is `0x8001..0x8005` (`:447-449`, `:704`) and the linear tile is `0x10000` (`:95`), so at the guarded store `tileptr` is in `{0x10000, 0x20000, 0x30000, 0x40000, 0x50000}` and `tileptr & 0xfff00000 == 0` on EVERY row.  `if (ok || (tileptr & 0xfff00000))` is therefore textually `if (ok)` on every driven row: 89/89 at HEAD by construction, not by prediction.  The same inspection also classifies it under D1: bit 31 IS a body-tested mask (`:312`), so it belongs to the generating set -- and it is constant-cleared before the store, so the `0xfff00000` slice touches no tested bit at the point of the guard.  Bits 20-30 are untested.  Clause (e), by the letter.
E1:72  
E1:73  ### 3. Ruling, with its warrant and bound.
E1:74  
E1:75  **"Closable by a finite row set" is not a discriminator, and the carrier already rejected it.**  On 2026-09-04 the main loop's *"pairs of body-read lvalues over a finite reachable space"* was rejected as SELF-REFUTING: *"the counts' raw value space is 2^32 apiece, so 'finite' does no bounding work ... (a C int is finite)"*.  The measuring seat's floor warrant -- *"pure functions of (x, y, bufdepth, tlb_mode), so the free input set is finite"* -- is that bound back under a new name: `(x, y)` ranges over 2048 x 128 after `y &= 127`, and C1-C4 SAMPLE it (the probe's own vocabulary, `:595`).  And its debt warrant is the same error inverted: *"a slice within an already-driven class is not closable by any finite row set"* (`:610-611`) is true of the FAMILY of slices and false of every member -- `x & 1` dies to one odd-`x` row, `y & 2` to one row with `y` bit 1 set, `mode & 1` to one mode word with bit 0 set, `tileptr & 0xfff00000` to one descriptor `>= 0x8010`.  Finiteness is identical in both buckets: each single predicate is one-row closable; the family of predicates is unbounded.  So it separates nothing, which is why the round graded one species two ways by it.
E1:76  
E1:77  **The governing discriminator is the one the carrier already carries, read with its bounds.**  (i) Clause (d)'s operand-swap enumeration draws swaps from *fields the guarded BODY READS*, walked up only to the enclosing-function boundary: here `tileptr`, `ofs`, `buf`, `bufdepth`.  Those swaps were all killed at 59 rows (`ok || ofs` 58/59 by `ycrcb x4y1`; `ok || tileptr` by every decline row, since `tileptr` is nonzero everywhere).  (ii) The CELLS owed are the cross-product of the guard's dominating predicates with the body-TESTED partitions of the device-state lvalues the repair path reads (pass 11, 09-04), where "tests" means masks or compares as a case (D1, 09-25).  (iii) A value, bit or slice the body never tests as a case is clause (e), disclosed; consequence orders the debt queue and never promotes to floor (D1: `#549`'s latch x bit was graded (e) although its consequence was the round's own defect).
E1:78  
E1:79  Applied to `#519`'s survivors, this gives ONE answer for all of them:
E1:80  
E1:81  | escape | what the body tests on that operand | grade |
E1:82  |---|---|---|
E1:83  | `M30`/`M31` `tile_nr == 0` / `ok \|\| tile_nr` | `tile_nr < 256` only (the `#100` bound) -- relational, three regions; no zero test | (e) |
E1:84  | `M32` `tile_nr_x`, `M33` `y == 0` | `x`,`y` tested `< 0` / `>= 2048`; `y &= 127` runs first; no zero test | (e) |
E1:85  | `ok \|\| (tileptr & 0xfff00000)` -- the TLB array contents | bit 31 tested (`:312`), constant 0 at the store; bits 20-30 untested | (e) |
E1:86  | `x & 1`, `y & 2`, `mode & 1` | bits of compared values / bits read by nothing | (e) |
E1:87  | `M28` nibble carve, `M37` `*color` | `default:` is ONE label for 12 nibbles; `*color` untested | (e) -- already so ruled |
E1:88  
E1:89  **So the measuring seat's FLOOR grade of the tile-index family was wrong AS A GRADE, and the codex class-closure review of 2026-09-11 was right** (*"BECAUSE THE BODY NEVER TESTS `tile_nr` FOR ZERO, `M30` ... IS NOT A FLOOR AXIS UNDER THE BODY-TESTED-PARTITION RULE -- IT IS CLAUSE-(e) DEBT"*).  The data-flow sentence the seat used (*"flows into the address operand at least as directly as `tlb_mode` does"*) is the 2026-09-09 LABEL clause with its first half dropped: a dispatch LABEL becomes a floor axis when its value flows into a body-read lvalue -- `tlb_mode` is a label the body tests as a case AND flows into `tileptr`; `tile_nr` flows and is not tested as a case.  Flow alone is the transitive-chasing reading the 08-24 bound forbids.
E1:90  
E1:91  **Harder on the author's leaning, as the brief asks.**  The author leaned YES (floor, L2, a repair owing its own pass).  YES would have reopened a chain the receipt closed ("NO FURTHER PASS IS OWED") on a mutant that no instrument in the tree can see; it would grade by consequence, which D1 refused; and its warrant is the rejected finiteness bound.  And harder on NO, because NO carries a real cost: `ok || (tileptr & 0xfff00000)` keeps the instrument green while re-opening the uninitialised-`buf` store on every real framebuffer tile at a physical address `>= 1 MB` -- the `M30` shape (fix kept on the instrument, open on the world).  The carrier's answer to that is the one it gave at `#549`: severity ORDERS the debt and does not promote it.  So the row is filed at the TOP of this file's coverage debt, below its live defects (`sgirebufuninit`, med), and it costs ONE readback.
E1:92  
E1:93  **What was legitimately done anyway.**  The 59 -> 77 -> 89 repairs were L1 (pre-ship construction: fd15065 landed 09-12, after all of them), licensed by the round's own choice on a severity finding (98.75% of the screen re-opened by `M30`).  L1 permits strengthening for any reason; only the floor MANDATES.  Nothing the round did was wrong; what it recorded about WHY was.
E1:94  
E1:95  **EXHAUSTED / SAMPLED: ADOPTED as clause-(e) disclosure vocabulary, with one correction.**  It is exactly what clause (e) asks for -- *"write into the CONTRACT which cells are covered and which are deliberately not"* -- made explicit per axis.  Definitions: EXHAUSTED := every cell of the BODY-TESTED partition of that lvalue is rowed (floor discharged on that axis); SAMPLED := driven at two or more values, with the untested slices and their derived or measured sweeps named.  The probe's `:587` wording "every value in the reachable domain is driven" coincides with the partition definition for `tlb_mode`/`bufdepth`/`color_mode` (tiny domains) and must not be the definition: the next probe with a 2^32 operand could never write EXHAUSTED under it and would write it anyway for a 16-value field the body tests at one bound.  BOUND: a disclosure vocabulary can never DEMAND a row (the carrier's filter rule: *"a filter can reject or repair a row; it can never demand a new one"*), so it cannot grow.  STRUCTURAL LANDING SPOT, per the structure-first rule: the PRETABLE block's GUARD FIELD vs BODY FIELD check gains one column, "partition the BODY induces on this lvalue" (the codex 09-11 table is the exemplar), and EXHAUSTED/SAMPLED is read off that column rather than asserted.  A template line, not a checker.
E1:96  
E1:97  ### 4. Measurable consequences, in order.
E1:98  
E1:99  1. **Records, L4, three sites, in the closure-records commit the row already owes:** (i) `sgirandomcolour` note line "genuine floor-shaped gap ... Filed as OWED" -> "(e) under D1 2026-09-25: bit 31 is the only tested bit of `tileptr` and is constant-cleared at `:319`; equivalent to the fix on every driven row by inspection; one-row debt, filed"; and the "GRADED FLOOR" / "finite" sentences for `M30`-`M33` -> L1 strengthening on a severity warrant; (ii) probe `:610-617` -> one note that the `:26-28` contract supersedes it and the species is (e) (the `#556` hrecord vehicle); (iii) `pass2_ledger.tsv:159` disclosure list -> add the SAMPLED axes and the four derived sweeps.
E1:100  2. **File ONE debt row** (`sgirecontentslice` or similar), ranked at the top of this file's coverage debt and below `sgirebufuninit`: four readbacks in existing sessions -- a descriptor `>= 0x8010` (physical `>= 0x100000`) at an already-rowed cell (kills the array-contents slice and adds a second anchored address), an odd-`x` cell, a `y` with bit 1 set, a mode word with bit 0 set -- one re-table, scores MEASURED, pin 89 -> 93.  Not in-round, not L2, no pass reopened; it ships the next time a measuring seat opens this instrument.
E1:101  3. **Released:** the repair pass the queue entry said the TLB-contents gap "owes"; any class-closure demand over `(x, y)`.
E1:102  4. **Carrier, one sentence under the joint-cells clause, with the structural column above:** *"A derived input (a local computed from the function's inputs and feeding a body-read operand) is graded by the partition the body induces on IT, never by the flow that reaches it: `#519`'s `tile_nr`, tested only at `< 256`, is clause (e); the finite-row-set warrant is the 09-04 finiteness bound and buys nothing in either direction."*

## 2. E2 -- GPT-6 Astra's confirmation, its 7n-5 items, verbatim (regress/artifacts/fablequeue7n_20261009/codex_astra_confirm.txt)

E2:25  7. **7n-5: `tile_nr` is “tested only at `< 256`”; “stores at `:374`/`:377`.”**  
E2:26     The tiled branch checks `>= 256`, but LIN_A recomputes `tile_nr` and checks **`>= 32`** at [dev_sgi_re.c:264](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c:264). Scope the proposed carrier sentence to the tiled branch or name both bounds. Also, line 374 starts the write; [line 377](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c:377) starts a **read**. Neither correction defeats the low-address guard-equivalence finding.
E2:47  - **7n-5:** The controlling contract and source inspection support its disposition. Correct the proposed carrier sentence’s bounds. Treat “four readbacks, 89→93” as a proposed budget, not established sufficiency: the [contract itself](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/sgi_re_colourdefault_probe.py:46) says identical-byte writes are invisible and uninitialized-buffer kills require measurement.
E2:57  - **7n-5 omits an important correction destination:** [OUTSTANDING_BUGS.md:19342](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/OUTSTANDING_BUGS.md:19342) still declares “#519 DOES NOT CLOSE … FLOOR BREACH,” calls the 59-row instrument shipped, and repeats the rejected rationale.
E2:60  Scope limit: I did not independently verify ledger-only states, carrier quotations, scratchpad claims or `pass2_ledger.tsv` contents outside the permitted reading set. Those remain unverified here, not disproved. Likewise, absence of a recorded review link establishes **unrecorded**, not necessarily **unread**.

## 3. E3 -- `src/devices/dev_sgi_re.c` at HEAD 620ddd09, the lines the corrections describe

E3:250  	uint32_t tlb_mode = (mode >> 10) & 0x7;
E3:251  	int linear = tlb_mode > 3;
E3:252  
E3:253  	if (!linear && (x < 0 || y < 0 || x >= 2048 || y >= 2048))
E3:254  		return;
E3:255  
E3:256  	int tilewidth_in_pixels = 512 / bufdepth;
E3:257  	
E3:258  	int tile_nr_x = x / tilewidth_in_pixels;
E3:259  	int tile_nr_y = y >> 7;
E3:260  
E3:261  	unsigned int tile_nr = tile_nr_y * 16 + tile_nr_x;
E3:262  
E3:263  	y &= 127;
E3:264  	int xofs = (x % tilewidth_in_pixels) * bufdepth;
E3:265  	int ofs = 512 * y + xofs;
E3:266  
E3:267  	uint32_t tileptr = 0;
E3:268  
E3:269  	/*  #100: cases 0-2 index re_tlb_[abc][256] with a guest-derived
E3:270  	    tile_nr = (y>>7)*16 + x/tilewidth; bound it (case 4 self-checks).  */
E3:271  	if (tlb_mode <= 2 && tile_nr >= 256)
E3:272  		return;
E3:273  
E3:274  	switch (tlb_mode) {
E3:275  	case 0:	tileptr = d->re_tlb_a[tile_nr] << 16;
E3:276  		break;
E3:277  	case 1:	tileptr = d->re_tlb_b[tile_nr] << 16;
E3:278  		break;
E3:279  	case 2:	tileptr = d->re_tlb_c[tile_nr] << 16;
E3:280  		break;
E3:281  	case 4:	tile_nr = x >> 12;
E3:282  		if (tile_nr >= 32)
E3:283  			return;
E3:284  		tileptr = 0x80000000 | (d->re_linear_a[tile_nr] << 12);
E3:285  		ofs = x & 4095;
E3:286  		// TODO... probably not correct!
E3:287  		// printf("tileptr = %08x x = %i y = %i tile_nr = %i ofs = %i\n", tileptr, x, y, tile_nr, ofs);
E3:288  		break;
E3:289  	default:/*  sgirandompixel: this arm used to assign `*color = random()' -- with
E3:290  		    its exit(1) commented out -- so a failed GET handed the CALLER a
...
E3:326  	}
E3:327  
E3:328  	// The highest bit seems to be set for a "valid" tile pointer.
E3:329  	if (!(tileptr & 0x80000000)) {
E3:330  		//printf("dst_mode %i, tile_nr = %i,  tileptr = 0x%llx\n", dst_mode, tile_nr, (long long)tileptr);
E3:331  		//fatal("sgi gbe horrible_getputpixel: unexpected non-set high bit of tileptr?\n");
E3:332  		//exit(1);
E3:333  		return;
E3:334  	}
E3:335  	
E3:336  	tileptr &= ~0x80000000;
E3:337  
...
E3:380  			    separate row, and the GET default below is untouched.  */
E3:381  			ok = 0;
E3:382  			if (!(d->warned & SGIRE_W_BADCOLOR)) {
E3:383  				d->warned |= SGIRE_W_BADCOLOR;
E3:384  				fatal("[ put: color mode = 0x%x ] [ sgi_re: unimplemented "
E3:385  				    "colour type in horrible_getputpixel, x=%i y=%i; store "
E3:386  				    "declined (once) ]\n", color_mode, x, y);
E3:387  			}
E3:388  		}
E3:389  
E3:390  		if (ok)	/*  #519: a declined type stores nothing  */
E3:391  			cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,

## 4. E4 -- the other evidence, verbatim

---- E4a  regress/sgi_re_colourdefault_probe.py at HEAD (the controlling contract) ----
E4a:24  #  writing to memory, leaving the destination pre-paint intact.
E4a:25  #
E4a:26  #  CONTRACT -- #519 closure design, 2026-09-12.  This is the controlling coverage
E4a:27  #  contract; older CONTRACT/CLOSED/COMPLETE claims below are historical and are
E4a:28  #  superseded wherever they claim a larger domain or describe missing coverage.
---- E4b  regress/artifacts/sgirandomcolour/killtable5_20260912/SCORES.txt (legs BASE, HEAD and the first two controls) ----
E4b:1  #519 KILL TABLE 5   2026-09-12T07:27:41Z
E4b:2  baseline = SEC src/devices/dev_sgi_re.c (post-fix working set)   probe = FROZEN (sgi_re_colourdefault_probe.py.frozen)
E4b:3  baseline cmp: CLEAN
E4b:4  SENTINEL DROPPED (clone-local)
E4b:5  
E4b:6  === LEG BASE ===
E4b:7    build rc=0 binary=FRESH
E4b:8    SGICOLOUR_RESULT=89/89  sentinel=[SGICOLOUR_DONE]
E4b:9    FAILING: 
E4b:10  
E4b:11  === LEG HEAD ===
E4b:12    build rc=0 binary=FRESH
E4b:13    SGICOLOUR_RESULT=28/89  sentinel=[SGICOLOUR_DONE]
E4b:14    FAILING: ycrcb put,reserved put,determinism,announce text,two declined,once,ycrcb x4y1,x4y1 announce,allbits announce,allbits paint,latch indep,indep paint,tA ycrcb d1,tA ycrcb d2,tA ycrcb d4,tA ycrcb d8,tA ycrcb rpt,tA ann1,tB ycrcb d1,tB ycrcb d2,tB ycrcb d4,tB ycrcb d8,tB ycrcb rpt,tB ann1,tC ycrcb d1,tC ycrcb d2,tC ycrcb d4,tC ycrcb d8,tC ycrcb rpt,tC ann1,lin ycrcb d1,lin ycrcb d2,lin ycrcb d8,nib 40,nib 60,nib 70,nib 80,nib 90,nib a0,nib b0,nib c0,nib d0,nib e0,nib ann,xy dec c1,xy dec c2,xy dec c3,xy dec c4,xy ann,tA d2 first,tA d8 first,tB d2 first,tB d4 first,tB d8 first,tC d2 first,tC d4 first,tC d8 first,lin d2 first,lin d8 first,lin d1 repeat,M28 nib60
E4b:15  
E4b:16  === LEG FIRST_A2_ZERO ===
E4b:17    build rc=0 binary=FRESH
E4b:18    SGICOLOUR_RESULT=88/89  sentinel=[SGICOLOUR_DONE]
E4b:19    FAILING: tA d2 first
E4b:20  
E4b:21  === LEG FIRST_A8_ZERO ===
E4b:22    build rc=0 binary=FRESH
E4b:23    SGICOLOUR_RESULT=88/89  sentinel=[SGICOLOUR_DONE]
E4b:24    FAILING: tA d8 first
E4b:25  
E4b:26  === LEG FIRST_B2_ZERO ===
---- E4c  regress/gate_arm.sh (the colourdefault block's pins) ----
E4c:1605  #  measured 15 legs, every one on its pre-registered prediction: BASE 89/89, HEAD 28/89, eleven
E4c:1606  #  single-cell zero-store controls 88/89 each on its OWN row, NIB_OTHER 78/89, TAIL8 81/89.
E4c:1607  #  PARSE BEFORE SCORE: the RESULT and DONE lines must each appear exactly once and be well formed.
E4c:1608  #  The denominator is a LITERAL -- a pin that follows the probe cannot tell gained rows from lost ones.
E4c:1609  COLLOG=$LOGDIR/sgi_re_colourdefault.log
E4c:1610  python3 sgi_re_colourdefault_probe.py "$PMAX" gate > "$COLLOG" 2>&1 || true
E4c:1611  colres=$(grep -c '^SGICOLOUR_RESULT=' "$COLLOG")
E4c:1612  colresok=$(grep -cE '^SGICOLOUR_RESULT=[0-9]+/[0-9]+$' "$COLLOG")
E4c:1613  coldone=$(grep -cx 'SGICOLOUR_DONE' "$COLLOG")
E4c:1614  if [ "$colres" = 1 ] && [ "$colresok" = 1 ] && [ "$coldone" = 1 ]; then
E4c:1615      check "sgi_re colourdefault protocol parsed" "yes" "yes"
E4c:1616      #  `live' is the liveness control: a supported RGBA PUT lands its colour.  Two spaces after the
E4c:1617      #  name, the padded-column idiom above -- `live silent' must not match `live'.
E4c:1618      check "sgi_re colourdefault liveness row" "$(count "$COLLOG" "^live  .*ok$")" "1"
E4c:1619      col=$(grep '^SGICOLOUR_RESULT=' "$COLLOG" | cut -d= -f2)
E4c:1620      check "sgi_re colourdefault rows run"     "${col#*/}" 89
E4c:1621      check "sgi_re colourdefault rows correct" "${col%/*}" 89
E4c:1622  else
E4c:1623      note "sgi_re colourdefault: protocol lines missing or duplicated (result=$colres/$colresok done=$coldone)"
E4c:1624      tail -5 "$COLLOG" | sed 's/^/       /'
E4c:1625      check "sgi_re colourdefault protocol parsed" "no" "yes"
E4c:1626  fi
---- E4d  CHANGELOG.md, the 2026-10-09 records block's 7n-5 paragraph ----
E4d:596  **7n-5 (Fable 5.1, Astra-confirmed).**  `sgirandomcolour`'s tile-index escapes, TLB-contents slice and value slices are
E4d:597  one species, clause (e); the contents gap is DEBT, filed as `sgirecontentslice` (four readbacks, 89 -> 93 a PROPOSED
E4d:598  budget per Astra).  Its three L4s stay owed in that row's closure-records commit, as ruled; the row now says so.
---- E4e  ledger row sgirecontentslice at HEAD ----
E4e  title: regress/sgi_re_colourdefault_probe.py: the TLB-array-contents slice of tileptr and three value slices (odd x, y bit 1, mode bit 0) are clause-(e) coverage debt of #519's detector -- four readbacks in existing sessions
E4e  state: open LOW
E4e  state_note: filed 2026-10-09 from Fable 5.1's 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md, consequence 2), ranked at the top of that file's coverage debt and BELOW sgirebufuninit.  The tile-index escapes, the TLB-contents slice and the value slices are ONE species, clause (e): the body tests tile_nr only at >= 256 (tiled) and >= 32 (LIN_A, dev_sgi_re.c -- GPT-6 Astra's correction to the ruling's '< 256'), never for zero, so they are not floor.  Proposed: four readbacks in existing sessions -- a descriptor >= 0x8010 (physical >= 0x100000) at an already-rowed cell (kills the array-contents slice and adds a second anchored address), an odd-x cell, a y with bit 1 set, a mode word with bit 0 set -- one re-table, pin 89 -> 93.  GPT-6 Astra (regress/artifacts/fablequeue7n_20261009/codex_astra_confirm.txt): 89 -> 93 is a PROPOSED budget, not established sufficiency -- the probe's own contract says identical-byte writes are invisible and uninitialised-buffer kills need measurement.  Not in-round, not L2, no pass reopened; it ships the next time a measuring seat opens this instrument.
---- E4f  the row note's six escapes, as recorded ----
E4f  13 builds, 11 instrument runs, 13 controls; `regress/artifacts/sgirandomcolour/pass2_20260911/`.

    M30_tilenrdecline   ok=0 -> if (tile_nr == 0) ok = 0;        59/59   tile 1, 0x70630000
    M31_tilenrguard     if (ok) -> if (ok || tile_nr)            59/59   tile 1, 0x6368696e
    M32_tilenrxdecline  ok=0 -> if (tile_nr_x == 0) ok = 0;      59/59   tile 1, 0x706300fe
    M33_tiledorigin     ok=0 -> if (linear || y == 0) ok = 0;    59/59   tiled (0,1)
    M28r_permit_othernib   my disclosed escape, replicated       59/59   nibble 0x60
    M37_fgvalue         ok=0 -> if (*color == 0xaabbccdd) ok=0;  59/59   fg 0x12345678

*** `0x6368696e` IS ASCII **"chin"** -- host stack TEXT reaching gue
---- E4g  the row note's closing measurements ----
E4g  -09-12: THE CLASS CLOSURE IS MEASURED AND THE ROUND LANDS.  Kill table 5 (regress/artifacts/sgirandomcolour/killtable5_20260912/SCORES.txt): 15 legs, EVERY ONE ON PREDICTION -- BASE 89/89, HEAD 28/89, eleven single-cell zero-store controls 88/89 each on its own row, NIB_OTHER 78/89, TAIL8 81/89.  Codex closing pass (codex_passE_20260912.txt): 0/32 cells unoccupied, 11 measured + 21 predicted isolated kills -- a zero WITH its denominator.  Probe wired into gate_arm.sh (pin 89): gate 14 PASS 914 checks (gate_arm_89rows.log).  Three wrong records corrected in PRETABLE.out's appended section (GUARD/BODY, CLAIM->ROW, and the mtime claim the append itself de

## 5. E5 -- pass 1's flags and named siblings, verbatim

---- E5a  Astra (codex_rcclose.txt), its Q2 ----
Q2.

FLAG: C3/C5 -- [tools/pipeline/ledger.json:38326](/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/pipeline/ledger.json:38326), the separate 59→77 measuring-record paragraph, retains: “The enumeration is BOUNDED and that is why this is not `#392`” and “So *close every derived coordinate* IS *close the pair (x, y)*: **two free variables, read off the function, unable to grow by argument.**” This retains the rejected bounding rationale rather than a literal FLOOR label. E1:75 rejects that warrant; E1:99 specifically requires correcting it. None of C1–C5 addresses this paragraph’s rationale locally.

FLAG: C6 -- [regress/sgi_re_colourdefault_probe.py:277](/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/sgi_re_colourdefault_probe.py:277) retains “DISCLOSURES (i), (ii) AND (iii) BELOW WERE MEASURED TO BE FLOOR BREACHES, NOT DEBT” and “ARE NOW CLOSED BY THE PASS-4 BLOCK AT THE END OF THIS FILE.” Lines 287–289 identify the six escapes, including M30–M33. E1:89,93 reject that grade. C6 corrects the separate later PASS-4 block without naming this earlier assertion; E1:66 establishes why general supersession alone leaves a wrong-record correction outstanding.

No additional uncovered target-family claim found in the specified receipt, bug entry or CHANGELOG block. C6’s block-level correction covers the repeated assertions within PASS-4; C1 explicitly includes M28r in its nearby grade correction.

---- E5b  Grok (grok_rcclose.txt), its FLAG lines and Q2 ----
FLAG: C5 OVERREACH -- "`x & 1` dies to one odd-x row" states a kill. E1:67 says table 4 and table 5 never ran `x & 1`, `y & 2`, or `mode & 1` (`:607-608`, "DERIVED, not measured"). E2:47 says uninitialised-buffer kills require measurement and 89→93 is a proposed budget. The probe's driven `x` is `{0, 4, 132}`, all even (`regress/sgi_re_colourdefault_probe.py:595`; `killtable4_20260911/RESIDUALS.md:102`).
FLAG: C9 FACT-WRONG -- "the four L4 corrections it named" and "the 7n-5 ruling's four L4s". E1:99 lists three sites. E4d:598 says "Its three L4s stay owed". E2:57 says the ruling omitted `OUTSTANDING_BUGS.md`.
**Q2**

These still grade the family as floor, as a mandated closure, or as not closable by a finite row set, and none of C1–C10 sits beside them. `pass2_ledger.tsv:159` does not. The `sgirandomcolour` entry in `OUTSTANDING_BUGS.md` (`:19356-19400`) gets a C8 note on each of its three sentences. The `#519` block of `CHANGELOG.md` (`:5447-5630`) does not; `:596-598` grades the family clause (e) and owes the three L4 records, which is this commit.

`regress/sgi_re_colourdefault_probe.py:277-279`: "*** DISCLOSURES (i), (ii) AND (iii) BELOW WERE MEASURED TO BE FLOOR BREACHES, NOT DEBT, AND ARE NOW CLOSED BY THE PASS-4 BLOCK ***". `:287-297` names `M30/M31/M32`, `M33`, `M28`, `M37`, then "NOW CLOSED, over the COMPLETE free input set" because the derived coordinates "are pure functions" of `(x, y, ...)`.

`regress/sgi_re_colourdefault_probe.py:563-569`: the pass-4 block exists because the six 59/59 mutants were measured, and "The rule forbids buying another cell, so this closes the CLASS", naming `M30/M31/M32`, `M33`, `M37`.

`regress/sgi_re_colourdefault_probe.py:599-601`: "by the 2026-09-09 flow test the array VALUE is as much a floor axis as the array CHOICE (tlb_mode) already is."

`tools/pipeline/ledger.json:38326`, before the C1 banner: "*** MY DISPOSITION CHANGES: `M28` IS NOT CLAUSE-(e) DEBT. It is the second pass of a recurring class, and the round owes the closure before it ships. ***"

`tools/pipeline/ledger.json:38326`, the sentence after C3's insertion point: "The 16-cell closure was principled and **incomplete on its own principle** -- the same reasoning that justified closing `tlb_mode x bufdepth` justifies closing the tile index."

Same line, between that sentence and the C4 sentence, outside the three predicates and still the warrant E1:75 rejects: "close every derived coordinate IS close the pair (x, y): two free variables ... unable to grow by argument." The probe's twin is `:579-581`.

Outside the named set: `regress/artifacts/sgirandomcolour/killtable4_20260911/RESIDUALS.md:110-118` still calls the TLB-array contents "FLOOR-SHAPED" and "OWED", and calls `x & 1` / `y & 2` "not closable by any finite row set".

---- E5c  GLM (glm_rcclose.txt), its Q2 and FLAG ----
**Q2:** NOT CHECKABLE (packet-fed). Risks a file seat should grep, named from the packet alone: (a) E1:66(i) locates the OWED sentence at "`scratchpad` line 962" while C1-C5 edit the ledger row's note -- if the scratchpad is persisted, it may carry an uncorrected copy; (b) E1:99(i) promises corrections for "the 'GRADED FLOOR' / 'finite' sentences for M30-M33" (plural) -- the packet shows one FLOOR heading (C1) and one finite sentence about the *value slices* (C5); further GRADED-FLOOR/"finite" sentences about M30-M33 itself may survive; (c) the row-note heading (C1's beside-text) still reads "ON THE SHIPPED INSTRUMENT" and "#519 DOES NOT CLOSE ON THIS DETECTOR" after C1 -- the twin claims Astra flagged (E2:57) and C8 corrects in the bug file; (d) the bug-file entry spans ~19354-19410+ and C8 touches three spots only.
FLAG: C9 -- "the 7n-5 ruling's four L4s" (state_note) and "the four L4 corrections it named" (closure note; antecedent = the ruling): the ruling named three sites (E1:66 "Three L4s"; E1:99 "three sites"; E4d "Its three L4s stay owed"); the fourth site, the bug file, is Astra's (E2:57: "7n-5 omits an important correction destination"). C10 in the same commit states the attribution correctly, and C9's four-item list is itself right -- minor, attribution only.

## 6. E6 -- the HEAD text of the newly corrected sites

---- E6a  regress/sgi_re_colourdefault_probe.py at HEAD, the disclosure headline and what follows it ----
E6a:277  #  *** DISCLOSURES (i), (ii) AND (iii) BELOW WERE MEASURED TO BE FLOOR BREACHES, NOT DEBT, AND
E6a:278  #  ARE NOW CLOSED BY THE PASS-4 BLOCK AT THE END OF THIS FILE.  The text is kept because it is
E6a:279  #  the record being corrected, and because its REASON was wrong in a way worth not repeating. ***
E6a:280  #
E6a:281  #  (i) said `color_mode' "does not flow into any lvalue the guarded body reads".  THAT IS FALSE:
E6a:282  #  color_mode selects among four arms every one of which writes `buf', and `buf' is the store's
E6a:283  #  DATA operand.  The correct reason M28 was survivable is different and narrower -- the body's
E6a:284  #  own tests partition color_mode into five LABELS and all five were driven, so M28 sliced WITHIN
E6a:285  #  a label.  The wrong reason mattered: applied consistently it also excluded `tile_nr', which
E6a:286  #  flows into `tileptr' -- the ADDRESS operand -- at least as directly as tlb_mode does.
E6a:287  #  (ii) and (iii) were disclosed honestly but classified as debt.  Pass 2 measured SIX mutants at
E6a:288  #  59/59 on this instrument, each writing uninitialised host stack into guest memory:
E6a:289  #  M30/M31/M32 (tile index), M33 (tiled y), M28 (nibble), M37 (foreground value).  The smallest
E6a:290  #  was ELEVEN CHARACTERS -- `if (ok)' -> `if (ok || tile_nr)'.  See
E6a:291  #  regress/artifacts/sgirandomcolour/pass2_20260911/.
E6a:292  #
E6a:293  #  NOW CLOSED, over the COMPLETE free input set of the guarded store rather than a mutant list:
E6a:294  #  { bufdepth, tlb_mode } by the sixteen cells above; { color_mode, *color } by the ten-nibble
E6a:295  #  session at a second foreground colour; { x, y } -- and with them every derived coordinate,
E6a:296  #  since tile_nr, tile_nr_x, tile_nr_y, xofs and ofs are pure functions of them -- by the four
E6a:297  #  coordinate cells.  The bound that makes this finite is stated at the pass-4 block.
---- E6b  the same file, the pass-4 block's header and its bound ----
E6b:563  # ================================================================ #519 PASS-4 -- THE CLASS CLOSURE
E6b:564  #  WHY THIS BLOCK EXISTS.  Pass 2 measured SIX mutants scoring 59/59 on the instrument as it
E6b:565  #  stood -- zero red rows, six times -- each one writing uninitialised host stack into guest
E6b:566  #  memory (regress/artifacts/sgirandomcolour/pass2_20260911/).  They were three passes of ONE
E6b:567  #  shape: a decline conditioned on an input the rows hold at a SINGLE VALUE.  M13/M14 were that
E6b:568  #  shape on bufdepth and tlb_mode; M28 on color_mode; M30/M31/M32 on the tile index, M33 on y,
E6b:569  #  M37 on the foreground colour.  The rule forbids buying another cell, so this closes the CLASS.
E6b:570  #
E6b:571  #  THE ENUMERATION, from the function's own inputs rather than from a list of mutant forms.
E6b:572  #  The guarded store reads exactly four lvalues -- tileptr, ofs, buf, bufdepth -- and their
E6b:573  #  inputs, walked up only to the enclosing function boundary, are:
E6b:574  #      bufdepth    <- (mode>>8)&3                  domain {1,2,4,8}   CLOSED by the 16 cells
E6b:575  #      tileptr     <- tlb_mode, tile_nr, array     tlb_mode {0,1,2,4} CLOSED by the 16 cells
E6b:576  #      ofs         <- x, y, bufdepth, tlb_mode
E6b:577  #      buf         <- color_mode (arm), *color (value)
E6b:578  #
E6b:579  #  THE BOUND: tile_nr, tile_nr_x, tile_nr_y, xofs and ofs are NOT independent axes.  Each is a
E6b:580  #  pure function of (x, y, bufdepth, tlb_mode).  So "close every derived coordinate" IS "close
E6b:581  #  the pair (x, y)" -- two free variables, not an open-ended demand.
---- E6c  the same file, the pass-4 block's SAMPLED list and its historical paragraph ----
E6c:593  #  SAMPLED -- driven at more than one value, which kills the measured single-value family, but
E6c:594  #  NOT exhausted, so a slice WITHIN a driven class can still escape:
E6c:595  #      x           {0, 4, 132} of 2048          y  {0,1} masked, of 128
E6c:596  #      *color      2 values of 2^32
E6c:597  #      tileptr     {0x10000,0x20000,0x30000,0x40000,0x50000} -- the TLB ARRAY CONTENTS, which
E6c:598  #                  the line above lists as an input to tileptr and which the superseded
E6c:599  #                  sentence then silently dropped.  This one matters most: tileptr IS the
E6c:600  #                  store's address operand, so by the 2026-09-09 flow test the array VALUE is
E6c:601  #                  as much a floor axis as the array CHOICE (tlb_mode) already is.
E6c:602  #      mode        the raw parameter.  Bits 0-3 and 13-31 are read by NOTHING in this function,
E6c:603  #                  and every mode word any row drives has low nibble 0.
E6c:604  #
E6c:605  #  WHAT THAT COSTS, stated rather than glossed: `if (ok || (tileptr & 0xfff00000))',
E6c:606  #  `if (ok || (mode & 1))', `if (ok || (x & 1))' and `if (ok || (y & 2))' are each predicted to
E6c:607  #  score 77/77 and each is reachable by one ordinary guest store.  They are DERIVED, not
E6c:608  #  measured -- no table has run them.  They are filed in killtable4_20260911/RESIDUALS.md.
E6c:609  #
E6c:610  #  WHY THEY ARE NOT REPAIRED HERE, and this is the honest boundary rather than a dodge: a slice
E6c:611  #  within an already-driven class is not closable by any finite row set -- for any cells you
E6c:612  #  drive, a predicate false on exactly those cells exists.  That is the same species the
E6c:613  #  2026-09-04 ruling files as clause-(e) debt, and it is the species this round already accepted
E6c:614  #  for M28 (a value slice inside a driven label).  The tileptr/array-contents axis is the one
E6c:615  #  exception that is genuinely FLOOR-shaped, because the value flows into the address operand;
E6c:616  #  it is filed as owed rather than fixed in this diff, because a repair made in response to a
E6c:617  #  review owes its own pass and this block has not had one.
---- E6d  regress/artifacts/sgirandomcolour/killtable4_20260911/RESIDUALS.md at HEAD, R5 ----
E6d:92  ## R5. FOUR ONE-TERM MUTANTS PREDICTED TO SWEEP THE 77-ROW INSTRUMENT (from the closure audit)
E6d:93  
E6d:94  A read-only seat audited the pass-4 block against the source and found that its completeness
E6d:95  claim overreached. **DERIVED, NOT MEASURED — no table has run these.** Each is reachable by one
E6d:96  ordinary guest store. The probe's contract now discloses them; this is the filing it cites.
E6d:97  
E6d:98  | mutant | why it escapes every driven cell | reachable by |
E6d:99  |---|---|---|
E6d:100  | `if (ok \|\| (tileptr & 0xfff00000))` | driven tileptr is only {0x1,0x2,0x3,0x4,0x5}0000 | `re_tlb_a[0] = 0x8010` |
E6d:101  | `if (ok \|\| (mode & 1))` | every mode word any row drives has low nibble 0; bits 0-3 and 13-31 are read by nothing in the function | `DE_MODE_DST = 0x12f1` |
E6d:102  | `if (ok \|\| (x & 1))` | driven x is {0, 4, 132} -- all even | vertex x = 1 |
E6d:103  | `if (ok \|\| (y & 2))` | driven masked y is {0, 1} | vertex y = 2 |
E6d:104  
E6d:105  plus a mixed conjunction, `if (ok || (tile_nr_x && ofs == 0))`, true only at (x=128, y=0) --
E6d:106  a cell the pass-4 block explicitly considered and then did not drive.
E6d:107  
E6d:108  **THE DISPOSITIONS ARE NOT ALL THE SAME, and the difference is the whole point:**
E6d:109  
E6d:110  * **`tileptr` (the TLB array CONTENTS) is FLOOR-SHAPED and is the real gap.** The value flows
E6d:111    into the store's ADDRESS operand, so by the 2026-09-09 flow test it is a floor axis exactly as
E6d:112    `tlb_mode` is. The pass-4 enumeration NAMED it (`tileptr <- tlb_mode, tile_nr, array`) and then
E6d:113    dropped it from its conclusion. Closing it is cheap -- one cell whose tile entry is programmed
E6d:114    outside the 0x8001..0x8005 range -- and it is OWED.
E6d:115  * **`mode & 1` is clause-(e) debt by the same test that saved M28**: the unread bits flow into
E6d:116    NOTHING the guarded body reads. That is the `mode & COPY` shape the ruling names explicitly.
E6d:117  * **`x & 1` and `y & 2` are within-class value slices.** They are not closable by any finite row
E6d:118    set -- for any cells you drive, a predicate false on exactly those cells exists -- which is
E6d:119    why the contract now separates EXHAUSTED axes (tlb_mode, bufdepth, color_mode) from SAMPLED
E6d:120    ones (x, y, *color, tileptr, mode) instead of calling all of them "closed".
E6d:121  
E6d:122  **AND THE UNRESOLVED TENSION, which is an adjudication question and not mine to settle:** this
E6d:123  round graded the tile-index and tiled-origin escapes as FLOOR breaches, and those are also value
E6d:124  slices of a store input. If value slices are floor, these are live floor breaches; if they are
E6d:125  debt, the earlier grading was wrong. **The round currently asserts the first and ships the
E6d:126  second.** It needs ONE ruling, not two. Recorded here rather than decided.
E6d:127  

## 6b. R -- the corrections, marked against pass 1

D1  [CHANGED or NEW since pass 1]  (ledger row `sgirandomcolour`, `note`)
  THE TEXT IT SITS BESIDE (unchanged, the ~400 characters before it):
    ...- *the exact defect class `#519` exists to close.*  M13 and M14 were treated as floor kills and justified a forty-row expansion.  **The only thing separating M28 from them is which rows happen to exist to see it** -- and in the seat's words, *"an instrument-relative escape is not a contract-relative exemption."*

*** AND THIS PROJECT'S OWN CLASS-CLOSURE AMENDMENT FIRES ON EXACTLY THIS PATTERN. ***
  INSERTED:
     [CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra confirming): it does not.  The amendment's trigger is two consecutive passes finding BREACHES of one class, and M28 is not a breach: it slices WITHIN the one `default:` label that twelve nibbles share, which the ruling's table grades clause (e) ('already so ruled') and this note's own partition table, further down, says too.  The colour-mode closure that followed was L1 strengthening.]

D2  [CHANGED or NEW since pass 1]  (ledger row `sgirandomcolour`, `note`)
  THE TEXT IT SITS BESIDE (unchanged, the ~400 characters before it):
    ... "one row" is a cell repair rather than a closure in the other; *neither number was the closure, and the closure is the thing the rule asks for.*

**REVISED RE-TABLE: +11 (`color_mode` closure), +1 (`(1,0)` address), -4 (`ann cum`) = 67 rows.**

*** MY DISPOSITION CHANGES: `M28` IS NOT CLAUSE-(e) DEBT.  It is the second pass of a recurring class, and the round owes the closure before it ships. ***
  INSERTED:
     [CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra confirming): M28 IS clause-(e) debt: `default:` is one label for twelve nibbles (the ruling's table: '(e) -- already so ruled'), so no closure was owed, and the ten-nibble session the round added is L1 strengthening.]

D3  [CHANGED or NEW since pass 1]  (ledger row `sgirandomcolour`, `note`)
  THE TEXT IT SITS BESIDE (unchanged, the ~400 characters before it):
    ...), floor breach on the operand-swap route, and floor breach on the symmetry route -- and the third is the one that cites this project's own governing amendment.  Count the arguments, not the seats.*

*** PASS 2, MEASURED: **FLOOR BREACH.**  SIX MUTANTS SCORE 59/59 ON THE SHIPPED INSTRUMENT AND EVERY ONE WRITES UNINITIALISED HOST STACK INTO GUEST MEMORY.  `#519` DOES NOT CLOSE ON THIS DETECTOR. ***
  INSERTED:
     [CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra confirming): the six escapes are measured and real, and FLOOR BREACH was wrong AS A GRADE.  The body tests none of them as a case: tile_nr only at >= 256 on the tiled branch and >= 32 on LIN_A (M30, M31; M32's tile_nr_x is an untested component of it), x and y only against their bounds, < 0 and >= 2048, before `y &= 127` (M33), *color not at all (M37), and the twelve nibbles that reach `default:` only as that one cell (M28r).  Under D1 (2026-09-25: 'tests' means masks or compares as a case) each is clause (e).  The 59 -> 77 -> 89 repairs were L1 strengthening on a severity warrant (M30 re-opened the fix over 98.75% of the screen), legitimately done before fd15065 landed; only the recorded grade was wrong.  And the 59-row instrument this heading calls SHIPPED never shipped: fd15065 landed on 2026-09-12 with 89 rows.]

D4  [UNCHANGED since pass 1]  (ledger row `sgirandomcolour`, `note`)  -- the insertion beginning: [CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra con...

D5  [CHANGED or NEW since pass 1]  (ledger row `sgirandomcolour`, `note`)
  THE TEXT IT SITS BESIDE (unchanged, the ~400 characters before it):
    ... body-read lvalues, `bufdepth` is closed over its domain and `buf` over its label partition -- **`tileptr`'s INDEX and `ofs` are each held at a SINGLE VALUE by all 59 rows.**

*** THIS IS THE THIRD CONSECUTIVE PASS FINDING THE SAME SHAPE (bufdepth/linear, then color_mode, now tile index/y/fg), SO THE CLASS-CLOSURE RULE BITES HARD: the next repair owes the closure in ONE DIFF, not another cell. ***
  INSERTED:
     [CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra confirming): no closure was owed: the cells were clause (e), so the closure that followed was L1 strengthening chosen on a severity warrant, not one the class-closure rule mandated; and the 'same reasoning' the next sentence extends to the tile index is the flow warrant corrected above.]

D6  [CHANGED or NEW since pass 1]  (ledger row `sgirandomcolour`, `note`)
  THE TEXT IT SITS BESIDE (unchanged, the ~400 characters before it):
    ... `#392`:** the guarded store reads `tileptr`, `ofs`, `buf`, `bufdepth`, and **`tile_nr`, `tile_nr_x`, `tile_nr_y`, `xofs` and `ofs` are not independent axes** -- each is a pure function of `(x, y, bufdepth, tlb_mode)`, the latter two already closed by table 3.  So *close every derived coordinate* IS *close the pair (x, y)*: **two free variables, read off the function, unable to grow by argument.**
  INSERTED:
     [CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra confirming): this is the 2026-09-04 finiteness bound under a new name, and it bounds nothing: `(x, y)` ranges over 2048 x 128 after `y &= 127`, and the four coordinate cells SAMPLE it.  The derived coordinates are clause (e) because the body does not test them as a case, not because two free variables close them; this closure was L1 strengthening on a severity warrant.]

D7  [UNCHANGED since pass 1]  (ledger row `sgirandomcolour`, `note`)  -- the insertion beginning: [CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra con...

D8  [CHANGED or NEW since pass 1]  (ledger row `sgirandomcolour`, `note`)
  THE TEXT IT SITS BESIDE (unchanged, the ~400 characters before it):
    ...(e), not owed.  Bit 31 is the only tested bit of `tileptr` and it is constant-cleared before the store, so `if (ok || (tileptr & 0xfff00000))` is the fix on every driven row by inspection; the array-contents slice is coverage debt, one of the four readbacks filed as `sgirecontentslice`.]
* `mode & 1`, `x & 1`, `y & 2` also sweep -- **within-class value slices, not closable by any finite row set.**
  INSERTED:
     [CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra confirming): each slice is predicted one-row closable -- `x & 1` should die to one odd-x row, derived and never run -- and only the FAMILY is not, so 'closable by a finite row set' discriminates nothing (the 2026-09-04 finiteness bound under a new name); they are clause (e) because the body does not test them as a case.]

D9  [the probe's FOUR comment notes, whole diff; the module's syntax tree is unchanged.  Pass 1 saw ONE of them, the end-of-historical-part note, in an earlier wording]
--- a/regress/sgi_re_colourdefault_probe.py
+++ b/regress/sgi_re_colourdefault_probe.py
@@ -277,6 +277,15 @@
 #  *** DISCLOSURES (i), (ii) AND (iii) BELOW WERE MEASURED TO BE FLOOR BREACHES, NOT DEBT, AND
 #  ARE NOW CLOSED BY THE PASS-4 BLOCK AT THE END OF THIS FILE.  The text is kept because it is
 #  the record being corrected, and because its REASON was wrong in a way worth not repeating. ***
+#  *** CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/
+#  fable5_rule7n_35.md, GPT-6 Astra confirming).  "FLOOR BREACHES, NOT DEBT" is wrong AS A
+#  GRADE.  The six pass-2 escapes are measured and real, but the body tests none of them as a
+#  case -- tile_nr only at >= 256 (tiled) and >= 32 (LIN_A), x and y only against their bounds,
+#  *color not at all, the twelve default: nibbles only as one label -- so each is clause (e)
+#  (D1, 2026-09-25), and the closure the pass-4 block records was L1 strengthening on a
+#  severity warrant.  The paragraphs below give two reasons that ruling rejects: flow alone
+#  (tile_nr "flows into `tileptr'") is not the test, and "the COMPLETE free input set" is the
+#  2026-09-04 finiteness bound under a new name.  ***
 #
 #  (i) said `color_mode' "does not flow into any lvalue the guarded body reads".  THAT IS FALSE:
 #  color_mode selects among four arms every one of which writes `buf', and `buf' is the store's
@@ -567,6 +576,10 @@
 #  shape: a decline conditioned on an input the rows hold at a SINGLE VALUE.  M13/M14 were that
 #  shape on bufdepth and tlb_mode; M28 on color_mode; M30/M31/M32 on the tile index, M33 on y,
 #  M37 on the foreground colour.  The rule forbids buying another cell, so this closes the CLASS.
+#  *** CORRECTED 2026-10-18 by the 7n-5 ruling: no class closure was owed.  Each of the six pass-2
+#  mutants is clause (e) -- the body tests none of them as a case -- so the closure this block
+#  records is L1 strengthening on a severity warrant.  The CORRECTED notes earlier in this file and
+#  at the end of this block's historical part give the reasons.  ***
 #
 #  THE ENUMERATION, from the function's own inputs rather than from a list of mutant forms.
 #  The guarded store reads exactly four lvalues -- tileptr, ofs, buf, bufdepth -- and their
@@ -579,6 +592,10 @@
 #  THE BOUND: tile_nr, tile_nr_x, tile_nr_y, xofs and ofs are NOT independent axes.  Each is a
 #  pure function of (x, y, bufdepth, tlb_mode).  So "close every derived coordinate" IS "close
 #  the pair (x, y)" -- two free variables, not an open-ended demand.
+#  *** CORRECTED 2026-10-18 by the 7n-5 ruling: this is the 2026-09-04 finiteness bound under a
+#  new name, and it bounds nothing -- (x, y) ranges over 2048 x 128 after `y &= 127', and the four
+#  coordinate cells SAMPLE it.  The derived coordinates are clause (e) because the body does not
+#  test them as a case.  ***
 #
 #  *** AND THE WORD "COMPLETE" DOES NOT BELONG HERE.  An earlier draft of this block said "the
 #  complete free input set is therefore { x, y, *color, color_mode-within-default }" and that
@@ -615,6 +632,19 @@
 #  exception that is genuinely FLOOR-shaped, because the value flows into the address operand;
 #  it is filed as owed rather than fixed in this diff, because a repair made in response to a
 #  review owes its own pass and this block has not had one.
+#
+#  *** CORRECTED 2026-10-18 by the 7n-5 ruling (regress/artifacts/fablequeue7n_20261009/
+#  fable5_rule7n_35.md, GPT-6 Astra confirming).  This block is HISTORICAL: the 2026-09-12
+#  CONTRACT banner at the top of this file supersedes it.  Its "as much a floor axis" and
+#  "genuinely FLOOR-shaped" are wrong AS A GRADE -- a value the body does not TEST AS A CASE is
+#  clause (e), whatever it flows into (D1, 2026-09-25).  tileptr's only tested bit is 31,
+#  constant-cleared before the store, so `if (ok || (tileptr & 0xfff00000))' is the fix on every
+#  driven row by inspection; tile_nr is tested only at >= 256 (tiled) and >= 32 (LIN_A).  The
+#  array-contents slice is coverage debt, one of the four readbacks filed as sgirecontentslice,
+#  not owed.  "Not closable by any finite row set" is the 2026-09-04 finiteness bound under a new
+#  name: each slice is predicted one-row closable (derived, never run) and only the family is not.
+#  And EXHAUSTED above means every cell of the BODY-TESTED partition of that lvalue is rowed --
+#  not every value of its domain; the two coincide here only because the three domains are tiny.  ***
 #
 #  STILL DISCLOSED rather than rowed, and named so a later escape is inside or outside the
 #  contract by inspection: (a) a predicate that ENUMERATES this cell set by value


D10  [NEW since pass 1]  (RESIDUALS.md R5)
--- a/regress/artifacts/sgirandomcolour/killtable4_20260911/RESIDUALS.md
+++ b/regress/artifacts/sgirandomcolour/killtable4_20260911/RESIDUALS.md
@@ -126,4 +126,13 @@
 second.** It needs ONE ruling, not two. Recorded here rather than decided.
 
+**[RULED -- the 7n-5 ruling of 2026-10-09 (`regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md`; GPT-6
+Astra confirming), applied here 2026-10-18 at the row's closure.]**  The tension resolves to DEBT, not floor.  A value
+the body does not test as a case is clause (e), whatever it flows into (D1, 2026-09-25), so the tile-index and
+tiled-origin escapes AND the `tileptr` contents slice are all clause (e), and the earlier FLOOR grading was wrong as a
+grade.  `tileptr`'s only tested bit is 31, constant-cleared before the store, so `if (ok || (tileptr & 0xfff00000))` is
+the fix on every driven row by inspection: coverage debt, not OWED.  `x & 1` and `y & 2` are each predicted one-row
+closable (derived, never run) and only the family is not, so finiteness separates nothing.  The readbacks are filed
+as `sgirecontentslice`.
+
 ## R6. SMALLER ITEMS FROM THE SAME AUDIT, each verified before filing
 


D11  [CHANGED since pass 1]  (the ledger row's closure fields; the receipt line and the bug-file notes are UNCHANGED since pass 1)
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by its closure-records commit (2026-10-18): #519 (fd15065) shipped the COLOUR-mode PUT default arm's latched decline -- an unimplemented colour type stores nothing, announced once per device (SGIRE_W_BADCOLOR) -- with the 89-row detector regress/sgi_re_colourdefault_probe.py (kill table 5: the fix 89/89, the pre-fix HEAD leg 28/89; gate_arm.sh pins 89 rows run and 89 correct; the closing pass found 0 of 32 cells unoccupied).  The 7n-5 ruling (Fable 5.1, 2026-10-09, GPT-6 Astra confirming) graded the M30-M33 / contents / value-slice survivors clause (e) and released the repair pass the queue said they owed; this commit makes the three L4 corrections it named (the row note, the probe's historical block, the pass2_ledger.tsv receipt), the fourth GPT-6 Astra added (the bug file's entry), and the siblings the closure-records review found (regress/artifacts/sgirandomcolour/closure_20261018/).  Coverage debt: sgirecontentslice (filed)."}
  hold_question: REGRESS (held 2026-10-18 at the sgirandomcolour closure): does regress/sgi_re_colourdefault_probe.py still score 89/89 on a build of HEAD and 28/89 on a build of fd15065's parent e5867e45 -- kill table 5's HEAD leg (killtable5_20260912/SCORES.txt, which names no SHA; e5867e45 was HEAD when it ran)?
  state_note (head): [2026-10-18, CLOSED] The closure-records commit made the 7n-5 ruling's three L4s, GPT-6 Astra's fourth and the siblings its review found; REGRESS is held for the flagship (hold_question).  ||  [2026-10-09] QUEUE 7n-5 ANSWERED (Fable 5.1, regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md; GPT-6 Astra confirmed with corr
  NEW ENTRIES: {"date": "2026-10-18", "phase": "review", "seat": "codex", "note": "sgirandomcolour CLOSURE-RECORDS review, pass 1: 2 flags -- GPT-6 Astra: C1-C10 faithful to the 7n-5 ruling; two uncorrected siblings named (the row note's 'two free variables' bound; the probe's 'FLOOR BREACHES, NOT DEBT' headline) -- both corrected in place.", "ev": "regress/artifacts/sgirandomcolour/closure_20261018/codex_rcclose.txt", "d": "✓"}
    {"date": "2026-10-18", "phase": "review", "seat": "grok", "note": "sgirandomcolour CLOSURE-RECORDS review, pass 1: 2 flags -- Grok 4.7: C5's 'dies to one odd-x row' states a kill no table ran (reworded as predicted, there and in RESIDUALS.md); C9 booked GPT-6 Astra's fourth L4 site to the ruling (fixed).  Its siblings -- the pass-4 block's 'closes the CLASS' and 'two free variables', 'as much a floor axis', RESIDUALS.md R5 -- corrected in place.", "ev": "regress/artifacts/sgirandomcolour/closure_20261018/grok_rcclose.txt", "d": "✓"}
    {"date": "2026-10-18", "phase": "review", "seat": "glm", "note": "sgirandomcolour CLOSURE-RECORDS review, pass 1: 1 flag -- GLM 5.3: C9's attribution of the fourth L4 site (fixed); its Q2 risk that the row-note heading still called the 59-row instrument SHIPPED -- corrected in C1.", "ev": "regress/artifacts/sgirandomcolour/closure_20261018/glm_rcclose.txt", "d": "✓"}
    {"date": "2026-10-18", "phase": "review", "seat": "fable5", "note": "sgirandomcolour CLOSURE-RECORDS review, pass 1: SEAT FAILURE -- Fable 5.1, HTTP 429 (req_011Cg9W6JNR2wZurX4nyBy3Y); held by the owner's 2026-10-17 directive.", "ev": "regress/artifacts/sgirandomcolour/closure_20261018/fable5_SEAT_FAILURE.txt"}
    {"phase": "regress", "seat": "fable5", "date": "2026-10-18", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] sgirandomcolour closed by its closure-records commit and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the flagship sign-off.  The question is in the row's hold_question."}

D12  [CHANGED since pass 1]  (CHANGELOG.md, the block prepended at the top)
# Records, 2026-10-18: `sgirandomcolour` closes -- the 7n-5 ruling's L4s placed beside the sentences they correct

`#519` landed as `fd15065` on 2026-09-12 with the 89-row instrument, and the row stayed `in work` for its closure
records.  The 2026-10-09 block below records the 7n-5 ruling (Fable 5.1, `regress/artifacts/fablequeue7n_20261009/
fable5_rule7n_35.md`; GPT-6 Astra confirming with corrections) and says its three L4s "stay owed in that row's
closure-records commit".  This is that commit.  Each correction sits beside the sentence it corrects, which stays in
place unedited.

* **The ruling's three sites.**  The row note's "genuine floor-shaped gap ... Filed as OWED", its pass-2 "FLOOR BREACH"
  heading and its "not closable by any finite row set"; the probe's historical pass-4 paragraphs; and `fd15065`'s
  receipt in `regress/pass2_ledger.tsv`, whose disclosure list gains the SAMPLED axes and the four derived sweeps
  (predicted 77/77, never run).
* **Astra's fourth.**  `OUTSTANDING_BUGS.md`'s `sgirandomcolour` entry: a note under its heading, and two beside the flow
  warrant and the closure-owed sentence it "repeats".
* **The siblings the closure-records review found** (`regress/artifacts/sgirandomcolour/closure_20261018/`: Astra, Grok
  and GLM, plus an Argon reading).  In the row note: the flow warrant, "owes the closure in ONE DIFF", the "two free
  variables" bound, and both sentences that made M28 floor.  In the probe: the "FLOOR BREACHES, NOT DEBT" headline, and
  the pass-4 block's "closes the CLASS" and its "two free variables" bound.  And `killtable4_20260911/RESIDUALS.md` R5,
  which asked for exactly this ruling.  Every probe edit is a comment; the module's syntax tree is unchanged.

**Closed** with REGRESS held for the flagship; the question is in `hold_question`.  The Fable seat walled again (HTTP
429) and is recorded as a seat failure.  The owner's 2026-10-17 directive holds Fable adjudication, so this commit makes
no new ruling: it applies the 2026-10-09 one.  The coverage debt stays filed as `sgirecontentslice`.  No `src/` change.


## 7. Questions -- a DELTA pass: only what changed since pass 1

**Please do not simply ratify.**  Check the changes against E1-E6, not against each other.

**Q1.**  For EACH D marked CHANGED or NEW, one line: `D<n>: FAITHFUL | OVERREACH | CONTRADICTS | FACT-WRONG |
WRONG-SITE -- <why>`, citing the `E<x>:<line>` that settles it.

**Q2.**  For EACH pass-1 flag and named sibling in E5, one line: `FIXED | NOT FIXED | FIXED WRONGLY -- <which D>`.

**Q3.**  Is any sentence still standing that grades the M28 / M30-M33 / M37 / TLB-contents / value-slice family as floor,
as owed, as a mandated closure, or as "not closable by a finite row set" -- with no correction beside it after this
commit?  A FILE-READING seat: the working tree's files are still at HEAD (none of D1.. is in them yet); search the
`sgirandomcolour` row of `tools/pipeline/ledger.json`, `regress/sgi_re_colourdefault_probe.py`, `regress/pass2_ledger.tsv`
(the fd15065 line), `OUTSTANDING_BUGS.md`'s `sgirandomcolour` entry, `CHANGELOG.md`'s `#519` block and
`regress/artifacts/sgirandomcolour/killtable4_20260911/RESIDUALS.md`, and quote each hit with file and line.  A seat
that cannot read files: `Q3: NOT CHECKABLE`, then name any risk the packet shows.

**Q4.**  Name the ONE change most likely to be wrong, and why -- or say none, with the check that rules each out.

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q4.  Every defect is a line
starting `FLAG:` citing `D<n>` and its evidence.  Facts and flags only.
