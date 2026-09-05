# #501 pcc2defaultkill -- PASS 2: the nine-seat pass on the REAL DIFF.  The `default:` arm of DEVICE_ACCESS(pcc2) ended the emulator process on any access to an offset with no `case`, reads included; it now keeps served reads and declines writes, one latched announce per offset per instance.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

The pass-1 panel (nine seats, 2026-09-05 02:17-03:27) converged on this design and found two premises of the pass-1
brief wrong (the guest driver never attaches on this model; the conf excerpt was empty because the grep was wrong)
and one witness disposition-blind (13/13 under BOTH candidate fixes).  This pass reviews what was BUILT: the product
diff, the 23-row detector, the gate section, the kill table, and the record.  **Check the premises, not just the
derivations; be harder on the accepted dispositions than the rejected ones; a seat whose position was adopted
(Opus's fix A) scrutinises it MORE.**  Anything you can check against the tree, check.  **VERDICT LINE FIRST.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/`, UNCOMMITTED on top of `7076134`.**  Three
pristine-2021 copies of `src/` under the project root are NOT this fork; if your line numbers disagree with mine by
hundreds you are reading one -- say so.  The guest source is `_guest-src-openbsd22/`; the MVME187 board manual is
`_scratchpad/vmesbcp2.txt` (fetched 2026-09-05 at the codex seat's citation).

## PREMISES ALREADY SETTLED, RE-INLINED (each is a QUESTION if you can check it)

1. **43 of the 0x40 byte offsets reach `default:`** -- 18 named unimplemented registers, 12 counter-word interior
   bytes, 13 unnamed (derived from mvme_pcctworeg.h against the 21 case labels; two seats re-derived it).
2. **Reads are served BEFORE the switch** by the memcpy (with the #119 end-span guard: a read crossing 0x40 is
   zero-filled, not served -- irrelevant to byte offsets, and premise 2 of the pass-1 brief was over-general there).
3. **The witness** (`witness_20260905/`): on the committed build a GUEST `st.b` or `ld.bu` to IEICR ends the host
   (exit 1) with the arm's own `pcc2: unimplemented` line first; IEBERR, the in-word byte 0x05 and the alias 0x6a
   likewise; the debugger's `put b` does NOT reach the arm (a control -- `put b` never reaches a DM_DEFAULT device).
   7/13 pre-fix, 13/13 post-fix (both inlined).  The IEBERR/IEERR row measures IEBERR only (the exiting build dies at
   the first); IEERR's kill follows from source (codex).  **The witness is DISPOSITION-BLIND** (Opus built both
   candidates: 13/13 under decline and under backed-accept) -- the DETECTOR's `ieicr rdawr`/`ieerr rdawr` rows (store
   0x5a then load in ONE session, want 0x0) are what pin the disposition; `sccerr rdawr` (a CASED write-to-clear
   sibling, 0x0 under either) is the control that makes the delta attributable.
4. **The guest driver never attaches on this model**: `machine_mvme88k.c:106` installs `unreadable` at 0xfff46000
   (the ie0 address), `if_ie.c:407-409` fails its match on `badpaddr()` there, and `ie_setupram()` returns early
   at `:561-564` before the PCC2 store at `:609`.  `ie0` IS configured in `conf/M187` and `conf/NFS` (the pass-1
   brief's conf grep looked in the wrong files).  So the HIGH ranking rests on the witness and severity.
5. **The alias is DOCUMENTED**: Motorola VMESBCP2 Table 6-1 lists `$FFF42040-$FFF42FFF  PCCchip2 Registers  Repeated`
   (`_scratchpad/vmesbcp2.txt` line 4629), so `relative_addr %= PCC2_SIZE` models the part.  The fork's
   `PCC2_SIZE` (0x40) and the guest header's (0x1000) name different things.
6. **The design, converged**: READ side keeps the byte the memcpy served and says so (`served 0x%02x` -- it is the
   array's default, NOT a computed value: not member 4 of the option set); WRITE side member 3 -- DECLINE + latched
   `fatal()` `(once)`, per OFFSET (one `uint64_t` bit per byte offset; `relative_addr` is folded to 0..0x3f above
   the switch so the shift is defined).  NOT member 6 (backed accept): the cased siblings contradict a blanket store
   (SCCERR is write-to-clear -- the manual's SCLR bits read as zero; the ICRs mask + reassert; PSCALECNT/SPEED/the
   IACKs are read-only), the addition licence is unmet, and a store from the one arm 43 offsets reach adds a
   bounded-write surface.  The codex seat's alternative -- ONE latch for the whole site, writes only, reads keep
   the old `debug()` -- is RECORDED, not adopted (per-offset announces are what a driver scanning registers needs;
   both are bounded).
7. **The IACK offsets 0x23/0x25 are declined like the rest**; modelling them (on the SCCRXIACK shape) would open
   two new entries into the C040 path, so `pcc2c040kill` goes first (filed as a cross-round obligation).  The
   in-word bytes are the interior of IMPLEMENTED counters -- declined here as a width matter, disclosed, not
   claimed as unimplemented registers.
8. **`return 0` denotes a FAILED TRANSACTION**, not inherently unmapped hardware (an IACK cycle with no interrupt
   pending times out on the real part) -- a correction to the option set's member-5 wording (codex).
9. **The roster**: all nine seats; agy DELIBERATELY NOT FIRED (measurement reserve).

## THE MEASUREMENTS (every number names its log)

The witness, pre-fix (`witness_20260905/witness_committed.out`) and post-fix (`witness_fixed_501.out`):
```
pcc2defaultkill WITNESS -- binary=/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul label=committed-b78bb0f-plus-width-chain (session() = the probe's own)
live             0x5a5a5a5a     0x5a5a5a5a     ok   LIVENESS: the probe's own scratch st/ld round-trip
devsig chipid    0x20           0x20           ok   DEVICE-SIGNATURE: CHIPID reads PCC2_ID through a guest ld.bu (RAM would read 0)
ieicr st.b       host exit1     survived       FAIL GUEST byte store to IEICR (0x2a) -- the write if_ie.c makes at attach; no case -> default:
ieicr st.b msg   1              1              ok   the default: arm's own 'pcc2: unimplemented' line was printed (the arm was REACHED)
ieicr ld.bu      host exit1     survived       FAIL GUEST byte load of IEICR: the memcpy serves it, then default: -- the READ side
ieicr ld.bu msg  1              1              ok   the default: arm reached on the READ too
ieicr rd val     n/a (host exit1) 0x0            FAIL the served value (post-fix): the register array's byte
ieicr put b      survived       survived       ok   the operator path (cold-debugger put b); the carrier says put b never reaches a DM_DEFAULT arm -- a CONTROL
ieicr put b msg  0              0              ok   ...so no 'unimplemented' line: the arm was NOT reached by put b
ieberr/ieerr     host exit1     survived       FAIL the other two if_ie.c targets (0x2b, 0x28)
t1cmp+1 st.b     host exit1     survived       FAIL a BYTE inside the T1CMP word (0x05): no case -> default:
alias 0x6a       host exit1     survived       FAIL the %= PCC2_SIZE fold: 0x6a aliases IEICR
genctl rt        0x82           0x82           ok   an IMPLEMENTED register still round-trips (the fix must not perturb the cased arms)
DEFAULTKILL_RESULT=7/13 label=committed-b78bb0f-plus-width-chain binary=/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul
DEFAULTKILL_WITNESS_DONE
```
```
pcc2defaultkill WITNESS -- binary=/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul label=fixed-501 (session() = the probe's own)
live             0x5a5a5a5a     0x5a5a5a5a     ok   LIVENESS: the probe's own scratch st/ld round-trip
devsig chipid    0x20           0x20           ok   DEVICE-SIGNATURE: CHIPID reads PCC2_ID through a guest ld.bu (RAM would read 0)
ieicr st.b       survived       survived       ok   GUEST byte store to IEICR (0x2a) -- the write if_ie.c makes at attach; no case -> default:
ieicr st.b msg   1              1              ok   the default: arm's own 'pcc2: unimplemented' line was printed (the arm was REACHED)
ieicr ld.bu      survived       survived       ok   GUEST byte load of IEICR: the memcpy serves it, then default: -- the READ side
ieicr ld.bu msg  1              1              ok   the default: arm reached on the READ too
ieicr rd val     0x0            0x0            ok   the served value (post-fix): the register array's byte
ieicr put b      survived       survived       ok   the operator path (cold-debugger put b); the carrier says put b never reaches a DM_DEFAULT arm -- a CONTROL
ieicr put b msg  0              0              ok   ...so no 'unimplemented' line: the arm was NOT reached by put b
ieberr/ieerr     survived       survived       ok   the other two if_ie.c targets (0x2b, 0x28)
t1cmp+1 st.b     survived       survived       ok   a BYTE inside the T1CMP word (0x05): no case -> default:
alias 0x6a       survived       survived       ok   the %= PCC2_SIZE fold: 0x6a aliases IEICR
genctl rt        0x82           0x82           ok   an IMPLEMENTED register still round-trips (the fix must not perturb the cased arms)
DEFAULTKILL_RESULT=13/13 label=fixed-501 binary=/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul
DEFAULTKILL_WITNESS_DONE
```

The kill table (`killtable_20260905/driver.log`; frozen instrument md5 a96b8bcf, live a96b8bcf; scratch clone
of build/, BASE rebuilt in the clone, each mutant compile-checked before the table and proven by a diff count):
    BASE         23/23    -
    M_EXIT       7/23     named wr,named wr msg,named rd,named rd msg,named rd srvd,inword wr,unnamed wr,ieicr rdawr,ieerr rdawr,latch sameoff,latch twooff,latch rw one,alias 0x6a,alias msg,dir wr text,dir rd text
    M_UNLATCH    21/23    latch sameoff,latch rw one
    M_ONELATCH   19/23    named wr msg,named rd msg,named rd srvd,latch twooff
    M_BACKED     21/23    ieicr rdawr,ieerr rdawr
    M_RDKILL     16/23    named rd,named rd msg,named rd srvd,ieicr rdawr,ieerr rdawr,latch rw one,dir rd text
    M_DIRSWAP    20/23    named rd srvd,dir wr text,dir rd text

PREDICTIONS written BEFORE the table (`PRETABLE_501.out`, VERBATIM):
```
PRE-TABLE BLOCK, #501 pcc2defaultkill -- written BEFORE the table (mtime against killtable_20260905/driver.log).

  - SIBLING PARITY -- the twelve cased byte arms DECLINE wide writes with a latched announce and ACCEPT byte writes;
    the default: arm now DECLINES byte-and-wide writes with a latched announce and keeps served reads.  Asymmetry
    disclosed: the cased arms' declines are per BLOCK, this arm's are per OFFSET (43 offsets in one arm); the
    announce says 'declined' / 'served 0x%02x' -- never 'ignored'.
  - CLAIM -> ROW -- the product comment claims: reads keep the served byte (named rd srvd, ieicr rdawr 0x0), writes
    declined (ieicr/ieerr rdawr 0x0 with sccerr rdawr as the cased control), one announce per offset per instance
    (named wr msg 18, latch sameoff 1, latch twooff 2, latch rw one 1), the fold is documented (alias 0x6a + alias msg),
    the cased arms untouched (genctl rt, t1cmp word rt), put b never reaches the arm (put b ctl).
  - GUARD FIELD vs BODY FIELD -- the guard reads warned_unimpl (bit relative_addr); the body reads writeflag, idata,
    pcctwo_reg[relative_addr].  They disagree only in the latch's own state, which the sameoff/twooff/rw-one rows
    build.  No offset-range predicate is added (stated, not left blank).
  - CHANNEL -- per row: the fate (survival) for (b); the announce COUNT for the latch mutants; the read-back VALUE for
    member 6; the announce TEXT for the direction swap; the served-value text for reads.  Each named channel varies
    under its named mutant by construction of the mutant string.

PREDICTIONS (six mutants plus BASE, 23-row instrument; MINIMUM red set per mutant, derived extras noted):
    BASE        23/23
    M_EXIT       8/23   red: named wr, named wr msg (n/a), named rd, named rd msg, named rd srvd, inword wr, unnamed wr,
                        ieicr rdawr, ieerr rdawr, latch sameoff, latch twooff, latch rw one, alias 0x6a, alias msg,
                        dir wr text, dir rd text (host exits on the first uncased access in each session: fifteen rows)
                        green: live, devsig chipid, sccerr rdawr, genctl rt, t1cmp word rt, put b ctl, put b ctl msg
    M_UNLATCH   21/23   latch sameoff 2, latch rw one 2
    M_ONELATCH  19/23   named wr msg 1, named rd msg 1, named rd srvd 1, latch twooff 1
    M_BACKED    21/23   ieicr rdawr 0x5a, ieerr rdawr 0x5a (sccerr rdawr 0x0: the control holds)
    M_RDKILL    18/23   named rd (host exit1), named rd msg n/a, named rd srvd n/a, dir rd text n/a, latch rw one (the
                        read in that session exits: n/a) -- five
    M_DIRSWAP   20/23   dir wr text 0, dir rd text 0, named rd srvd 0
  A miss in the SAFE direction is recorded; one in the UNSAFE direction (a predicted red that stays green) stops the
  round.  Written 2026-09-05 04:12:20.
```

Gate 14 (`killtable_20260905/gate14_501.log`): pcc2 default rows emitted 23, green 23; pcc2 width rows
emitted 251, green 251; GATE_RC=0.

## SECTION F2 -- THE PASS-1 DISPOSITIONS, numbered

ACCEPTED
 1. (opus5, fable5, codex, grok, kimi, glm, deepseek, minimax, kimi-k3) De-fatalise the arm; keep served reads.
 2. (opus5, fable5, codex, grok, kimi) Member 3 for writes, not member 6.  Warrants: sibling semantics, the addition
    licence, the bounded-write surface, the manual's SCLR/ICLR clearing bits (codex).
 3. (opus5, measured) The witness is disposition-blind -> the detector carries read-after-write rows in ONE session,
    with the cased SCCERR control.
 4. (fable5, codex, grok, opus5) if_ie never attaches; the filing and the ranking RE-BASED on the witness.  APPLIED.
 5. (codex) The alias is documented (Table 6-1) -> premise 1 upgraded; the manual fetched.  APPLIED.
 6. (opus5) The filing's "cheapest witness: put b" is measured FALSE -> corrected in place.  APPLIED.
 7. (codex) The IEBERR/IEERR witness row measures IEBERR only -> recorded; the detector has one session per direction
    across all 18 named offsets, valid because the fix has no per-offset branch (disclosed).
 8. (fable5, opus5) IACKs declined; c040kill before any IACK modelling.  Cross-round obligation recorded.
 9. (deepseek) Premise 2 over-general (end-spanning wide reads are zero-filled); "every exit path is return 1" should
    read "every RETURN path".  Wording L4s in the brief.
10. (codex) `return 0` = failed transaction.  Option-set wording, to the carrier.
11. (opus5, codex) Per-offset announce (Opus) over per-site (codex) -- ADOPTED per-offset; codex's alternative
    recorded.  Both bounded (64 bits; 43 reachable).
12. (codex) Two fresh sessions cannot establish per-instance latch scope (each is a new process) -- the detector
    makes no such claim; a two-instance fixture is filed as debt.

REJECTED / NOT CREDITED
13. Member 6 (backed accept) -- rejected on the warrants above; measured to read back the stored byte (0x5a).
14. Member 5 (fault every default access) -- no warrant: these are documented, present registers.
15. Splitting the disposition by offset class -- rejected: an offset-range predicate with no measured warrant;
    the contract discloses the three populations instead.

## QUESTIONS

1. **IS THE FIX RIGHT?**  Read the whole arm (inlined) and its two callers of state: does `break` reach the single
   `return 1`; is `1ULL << relative_addr` always defined; does the read announce ever print a wrong value; does the
   per-offset latch collide with the width latch word (`warned` vs `warned_unimpl`); is anything the memcpy served
   now different?  What does the ONE in-tree guest (OpenBSD 2.2, byte accesses only at cased offsets) see?
2. **DOES THE DETECTOR PIN THE DISPOSITION, NOT MERE SURVIVAL?**  For each of the 23 rows name the mutant it kills
   and the channel (the pre-table CHANNEL line); then check the kill table: six mutants, every prediction (inlined)
   against the measured result.  A prediction that missed is the interesting case.
3. **THE CLAUSE-(d) ENUMERATION for the new code**: predicates the fix adds or depends on -- the switch's no-case
   outcome, the latch bit, `writeflag` in the announce -- and NO value or range predicate (stated).  Is any
   partition held on one side only?  Is the (writeflag x latch) product held (four cells)?
4. **THE SMALLEST EDIT THAT BREAKS THE PROPERTY AND PASSES 23 ROWS.**  Name the row you expect to stay green and why.
5. **IS THE RECORD HONEST?**  The CHANGELOG block, the contract (the probe's docstring), the pre-table file and the
   filing are inlined.  Name any sentence a measurement refutes, any count without a deriver.
6. **CLOSE?**  A closing zero must be VALID: the diff delivered (inlined), the roster complete or misses named, the
   zero carried WITH its denominator (which mutant shapes, which cells).

If, while verifying a claim, you found something ELSE -- say so.

## THE PRODUCT DIFF (`git diff -- src/devices/dev_pcc2.c`, VERBATIM)

```diff
diff --git a/src/devices/dev_pcc2.c b/src/devices/dev_pcc2.c
index 412e6a5..20e0c04 100644
--- a/src/devices/dev_pcc2.c
+++ b/src/devices/dev_pcc2.c
@@ -138,6 +138,10 @@ struct pcc2_data {
 	/*  pcc2widthkills: one bit per width-guard block, see the enum.  Zeroed by
 	    the init memset, so every instance starts with every announce armed.  */
 	uint32_t		warned;
+	/*  #501: one bit per BYTE OFFSET (0..0x3f) for the default: arm's announce;
+	    relative_addr is folded to PCC2_SIZE above the switch, so the shift is
+	    always defined.  Zeroed by the same memset.  */
+	uint64_t		warned_unimpl;
 
 	uint8_t			cur_int_vec[8];
 
@@ -658,13 +662,40 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	default:
-		debug("[ pcc2: unimplemented %s offset 0x%x",
-		    writeflag == MEM_WRITE? "write to" : "read from",
-		    (int) relative_addr);
-		if (writeflag == MEM_WRITE)
-			debug(": 0x%x", (int)idata);
-		debug(" ]\n");
-		exit(1);
+		/*  #501 (pcc2defaultkill): this arm ended the host with exit(1) on ANY
+		    access to an offset with no case -- 43 of the 0x40 byte offsets:
+		    eighteen documented registers the model does not implement (IEICR,
+		    IEERR, IEBERR, GPIO, SCSIERR, the printer block, SPEED, the *IACKs),
+		    the bytes inside the four counter/compare words, and the unnamed
+		    ones -- READS included, though the memcpy above the switch had
+		    already served them.  A guest ld.bu or st.b at any of them was a host
+		    kill (rung-3 witness).  Now: a READ keeps the served byte (the array's
+		    default, said so -- not a computed value); a WRITE is DECLINED.  Not a
+		    backed store: the cased siblings contradict one (SCCERR clears on
+		    write, the ICRs mask and reassert, PSCALECNT/SPEED/the IACKs are
+		    read-only), no guest reaches these offsets on this model (if_ie never
+		    attaches: unreadable sits at its 82596 address), and a store from the
+		    one arm 43 offsets reach would add a bounded-write surface.  One
+		    latched fatal() per offset per instance, the house `(once)' shape --
+		    unlike PSCALEADJ's UNLATCHED print four arms up (pcc2pscaleflood).  The
+		    IACK offsets 0x23/0x25 are declined like the rest: modelling them (on
+		    the SCCRXIACK shape) would open two new entries into the C040 path,
+		    so pcc2c040kill goes first.  The %= fold above IS the real part's:
+		    Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as repeated
+		    PCCchip2 registers.  */
+		if (!(d->warned_unimpl & (1ULL << relative_addr))) {
+			d->warned_unimpl |= 1ULL << relative_addr;
+			if (writeflag == MEM_WRITE)
+				fatal("[ pcc2: unimplemented write to offset "
+				    "0x%x: 0x%x -- declined.  (once) ]\n",
+				    (int) relative_addr, (int) idata);
+			else
+				fatal("[ pcc2: unimplemented read from offset "
+				    "0x%x -- served 0x%02x.  (once) ]\n",
+				    (int) relative_addr,
+				    d->pcctwo_reg[relative_addr]);
+		}
+		break;
 	}
 
 	return 1;

```

## THE HANDLER AS IT NOW STANDS (`DEVICE_ACCESS(pcc2)`, VERBATIM -- every exit path)

```c
DEVICE_ACCESS(pcc2)
{
	uint64_t idata = 0;
	struct pcc2_data *d = (struct pcc2_data *) extra;

	/*  0xfff42000..0xfff42fff, but only 0x40 unique registers:  */
	relative_addr %= PCC2_SIZE;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	if (writeflag == MEM_READ) {
		if (relative_addr + len <= PCC2_SIZE)	/* OB-11: end-span */
			memcpy(data, d->pcctwo_reg + relative_addr, len);
		else {
			static int warned = 0;	/* #119: loud-once (course-correction) */
			if (!warned) {
				fatal("[ pcc2: read 0x%x+%i beyond reg space 0x%x; "
				    "zero-filled ]\n", (int)relative_addr, (int)len,
				    (int)PCC2_SIZE);
				warned = 1;
			}
			memset(data, 0, len);	/* OB-11b: don't leak uninit host memory */
		}
	}

	switch (relative_addr) {

	case PCCTWO_CHIPID:
	case PCCTWO_CHIPREV:
		if (writeflag == MEM_WRITE) {
			fatal("[ IGNORING write to read-only PCCTWO_CHIPID/"
			    "CHIPREV register ]\n");
		}
		break;

	case PCCTWO_GENCTL:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata;
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_VECBASE:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xf0;
			if (idata & ~0xf0)
				fatal("[ pcc2: HUH? write to PCCTWO_VECBASE"
				    " with value 0x%02x. ]\n", (int) idata);
		}
		break;

	case PCCTWO_T1CMP:
	case PCCTWO_T2CMP:
	case PCCTWO_T1COUNT:
	case PCCTWO_T2COUNT:
		if (writeflag == MEM_WRITE &&
		    relative_addr + len <= PCC2_SIZE)	/* OB-11: end-span */
			memcpy(d->pcctwo_reg + relative_addr, data, len);
		break;

	case PCCTWO_PSCALEADJ:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_PSCALEADJ_LEN, "PCCTWO_PSCALEADJ", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			fatal("[ pcc2: write to PSCALEADJ ignored (value "
			    "0x%02x) ]\n", (int)idata);
		}
		break;

	case PCCTWO_T2CTL:
	case PCCTWO_T1CTL:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_TXCTL_LEN, "PCCTWO_TxCTL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			/*  PCC2_TCTL_CEN and PCC2_TCTL_COC:  */
			d->pcctwo_reg[relative_addr] &= 0xfc;
			d->pcctwo_reg[relative_addr] |= (idata & 3);

			if (idata & PCC2_TCTL_COVF)
				d->pcctwo_reg[relative_addr] &=
				    ~(PCC2_TCTL_OVF | PCC2_TCTL_COVF);

			if (idata & ~7)
				fatal("[ pcc2: HUH? write to PCCTWO_TxCTL"
				    " with value 0x%02x. ]\n", (int) idata);
		}
		break;

	case PCCTWO_T2ICR:
	case PCCTWO_T1ICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] &= ~0x17;
			d->pcctwo_reg[relative_addr] |= (idata & 0x17);

			if (relative_addr == PCCTWO_T1ICR &&
			    !(idata & PCC2_TTIRQ_IEN))
				d->pending_timer1_interrupts = 0;
			if (relative_addr == PCCTWO_T2ICR &&
			    !(idata & PCC2_TTIRQ_IEN))
				d->pending_timer2_interrupts = 0;

			if (relative_addr == PCCTWO_T1ICR && (idata & PCC2_TTIRQ_ICLR)
			    && d->pcctwo_reg[relative_addr] & PCC2_TTIRQ_INT
			    && d->pending_timer1_interrupts > 0)
				d->pending_timer1_interrupts --;

			if (relative_addr == PCCTWO_T2ICR && (idata & PCC2_TTIRQ_ICLR)
			    && d->pcctwo_reg[relative_addr] & PCC2_TTIRQ_INT
			    && d->pending_timer2_interrupts > 0)
				d->pending_timer2_interrupts --;

			if (idata & PCC2_TTIRQ_ICLR)
				d->pcctwo_reg[relative_addr] &= ~PCC2_TTIRQ_INT;

			if (idata & 0xe0)
				fatal("[ pcc2: HUH? write to PCCTWO_TxICR"
				    " with value 0x%02x. ]\n", (int) idata);

			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCERR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCERR_LEN, "PCCTWO_SCCERR", len);
			break;
		}
		if (writeflag == MEM_WRITE)
			d->pcctwo_reg[relative_addr] = 0;	/*  clear  */
		break;

	case PCCTWO_SCCICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCICR_LEN, "PCCTWO_SCCICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0x1f;
			if (idata & ~0x1f)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCICR"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCTX:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0x1f;
			if (idata & ~0x1f)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCTX"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCRX:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCRX", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xdf;
			if (idata & ~0xdf)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCRX"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCRXIACK:
		/*  TODO. Hm. Is this enough?  */
		d->pcctwo_reg[PCCTWO_SCCRX] &= ~PCC2_IRQ_INT;
		reassert_interrupts(d);
		break;

	case PCCTWO_SCSIICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCSIICR_LEN, "PCCTWO_SCSIICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xdf;
			if (idata & ~0xdf)
				fatal("[ pcc2: HUH? write to PCCTWO_SCSIICR"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_IPL:
		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
		    said "ignored" about a READ the memcpy above had already served.
		    Now per-instance, write-only, like the ten blocks above -- that is
		    the WIDTH latch; the body's own #119 `static int w' below stays
		    process-global (pcc2pscaleflood's family; not this round's).  */
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			static int w = 0;	/* #119: was exit(1) (IPL is read-only) */
			if (!w) { fatal("[ pcc2: write to read-only PCCTWO_IPL; "
			    "ignored ]\n"); w = 1; }
		} else {
			if (d->pcctwo_reg[PCCTWO_IPL] == 0) {
				static int w = 0;	/* #119: was exit(1) */
				if (!w) { fatal("[ pcc2: IPL == 0 on read ]\n");
				    w = 1; }
			}
		}
		break;

	case PCCTWO_MASK:
		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
		    said "ignored" about a READ the memcpy above had already served.
		    Now per-instance, write-only, like the ten blocks above -- that is
		    the WIDTH latch.  (pcc2widthkills pass 7: this comment once claimed a
		    #119 static of MASK's own "below" -- there is none; the body stores
		    the byte and reasserts.  The static belongs to IPL's arm above.)  */
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata;
			reassert_interrupts(d);
		}
		break;

	default:
		/*  #501 (pcc2defaultkill): this arm ended the host with exit(1) on ANY
		    access to an offset with no case -- 43 of the 0x40 byte offsets:
		    eighteen documented registers the model does not implement (IEICR,
		    IEERR, IEBERR, GPIO, SCSIERR, the printer block, SPEED, the *IACKs),
		    the bytes inside the four counter/compare words, and the unnamed
		    ones -- READS included, though the memcpy above the switch had
		    already served them.  A guest ld.bu or st.b at any of them was a host
		    kill (rung-3 witness).  Now: a READ keeps the served byte (the array's
		    default, said so -- not a computed value); a WRITE is DECLINED.  Not a
		    backed store: the cased siblings contradict one (SCCERR clears on
		    write, the ICRs mask and reassert, PSCALECNT/SPEED/the IACKs are
		    read-only), no guest reaches these offsets on this model (if_ie never
		    attaches: unreadable sits at its 82596 address), and a store from the
		    one arm 43 offsets reach would add a bounded-write surface.  One
		    latched fatal() per offset per instance, the house `(once)' shape --
		    unlike PSCALEADJ's UNLATCHED print four arms up (pcc2pscaleflood).  The
		    IACK offsets 0x23/0x25 are declined like the rest: modelling them (on
		    the SCCRXIACK shape) would open two new entries into the C040 path,
		    so pcc2c040kill goes first.  The %= fold above IS the real part's:
		    Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as repeated
		    PCCchip2 registers.  */
		if (!(d->warned_unimpl & (1ULL << relative_addr))) {
			d->warned_unimpl |= 1ULL << relative_addr;
			if (writeflag == MEM_WRITE)
				fatal("[ pcc2: unimplemented write to offset "
				    "0x%x: 0x%x -- declined.  (once) ]\n",
				    (int) relative_addr, (int) idata);
			else
				fatal("[ pcc2: unimplemented read from offset "
				    "0x%x -- served 0x%02x.  (once) ]\n",
				    (int) relative_addr,
				    d->pcctwo_reg[relative_addr]);
		}
		break;
	}

	return 1;
}
```

## THE DETECTOR (`regress/pcc2_default_probe.py`, VERBATIM, contract included)

```python
#!/usr/bin/env python3
"""pcc2defaultkill DETECTOR (#501) -- the `default:' arm of DEVICE_ACCESS(pcc2) in dev_pcc2.c.

Before #501 that arm ended the emulator process (`exit(1)') on ANY access to an offset with no `case'
-- READS included, although the memcpy above the switch had already served them.  Forty-three of the
0x40 byte offsets reach it (derived from mvme_pcctworeg.h against the case list): eighteen NAMED
registers the model does not implement (PSCALECNT, GPIO_ICR/PCR, SCCMOIACK, SCCTXIACK, IEERR, IEICR,
IEBERR, SCSIERR, the printer block, SPEED, PRTDATA), the bytes INSIDE the four 32-bit counter/compare
words, and the unnamed offsets.  A single guest `st.b' or `ld.bu' at any of them was a host kill
(rung-3 witness, 7/13 on the committed build: regress/artifacts/pcc2defaultkill/witness_20260905/).

THE FIX (pass-1 panel of 2026-09-05, nine seats, converged): READ side -- keep the byte the memcpy
already served (it is the register array's default, NOT a computed value: the announce says so);
WRITE side -- DECLINE + a per-offset latched `fatal()' ("(once)", the house idiom), NOT a backed
accept: the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear, the ICRs
mask and reassert, PSCALECNT/SPEED/the IACKs are read-only), the addition licence is unmet (no guest
reaches these offsets on this model -- if_ie never attaches), and a store into pcctwo_reg[] from the
one arm reached by 43 offsets adds a bounded-write surface the decline does not have.

CONTRACT -- what this detector is built to catch, by row:
  (b) the verbatim `exit(1)' reinstated             -> every survival row (named wr/rd, inword, unnamed, alias)
  (d) the announce unlatched                        -> `latch sameoff' (2 lines, not 1)
  (d) one whole-arm latch bit instead of per-offset -> `latch twooff' (1 line, not 2), `named wr msg' (1, not 18)
  (d) a writeflag guard that re-kills READS         -> `named rd' (host exit)
  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text'
  member 6 (BACKED ACCEPT) substituted for member 3 -> `ieicr rdawr' / `ieerr rdawr' read back the stored
      byte (0x5a) instead of 0x0 -- the DISPOSITION-pinning rows; `sccerr rdawr' (a CASED, write-to-clear
      sibling) is the control that reads 0x0 under either and makes the delta attributable
  the `relative_addr %= PCC2_SIZE' fold changed      -> `alias msg' (the announce names offset 0x2a, not 0x6a)
  the fix perturbing a cased arm                    -> `genctl rt', `t1cmp word rt'
DISCLOSED, not caught: the in-word bytes are the interior of IMPLEMENTED counters, declined here as a
width/alignment matter (pcc2widecompose's business), not as unimplemented registers; the fold of
0x40..0xfff onto 0x00..0x3f IS the real part's: Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as
'PCCchip2 Registers  Repeated' (_scratchpad/vmesbcp2.txt:4629, fetched at the codex seat's citation -- two
seats had rightly called it unestablished before the manual was on disk), so `alias 0x6a' pins a documented
behaviour; the fork's PCC2_SIZE (0x40) and the guest header's (0x1000) name different things;
the IACK offsets 0x23/0x25 are declined like the rest -- modelling them (on the SCCRXIACK shape) would
open two new entries into the C040 path, so pcc2c040kill goes first; `named wr'/`named rd' touch all
eighteen offsets in ONE session each (valid because the fix has no per-offset branch; `named wr msg'
localises a failure) -- if a later round branches per offset this compression is invalid.
The debugger's `put b' never reaches a DM_DEFAULT arm (measured): `put b ctl' is a control, not a witness.

Usage: python3 pcc2_default_probe.py <gxemul> <label>      Sentinel: PCC2D_PROBE_DONE
The pty session helper is the width probe's own (extracted at run time), never hand-rolled: a first
draft of the witness hand-rolled it and read every host kill as "survived".
"""
import io, os, pty, re, select, sys, time
BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
DUMMY = "/tmp/pcc2_dummy.bin"
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 4096)
HERE = os.path.dirname(os.path.abspath(__file__))
_w = io.open(os.path.join(HERE, "pcc2_width_probe.py"), encoding="utf-8").read()
exec(_w[_w.index("def session("):_w.index("\ndef printed")])     # session(cmds) -> (transcript, alive, how)

CODE, SCRATCH, PCC2, SENTINEL = 0x00010000, 0x00020000, 0xfff42000, 0xdeadbeef
CHIPID, GENCTL, T1CMP, SCCERR = 0x00, 0x02, 0x04, 0x1c
IEERR, IEICR, IEBERR, SCCTXIACK, PRTICR = 0x28, 0x2a, 0x2b, 0x25, 0x30
NAMED18 = [0x14, 0x18, 0x19, 0x23, 0x25, 0x28, 0x2a, 0x2b, 0x2c, 0x30, 0x31, 0x32, 0x33, 0x34, 0x36, 0x37, 0x38, 0x3a]
INWORD = [0x05, 0x09, 0x0d, 0x11]
UNNAMED = [0x20, 0x24, 0x29, 0x35, 0x3d]
MSG = "pcc2: unimplemented"
def enc(op26, rd, rs1, imm): return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)
def LD_BU(rd, off): return enc(0x03, rd, 2, off)
def LD_W(rd, off): return enc(0x05, rd, 2, off)
def ST_B(rs, off): return enc(0x0b, rs, 2, off)
def ST_W(rs, off): return enc(0x09, rs, 2, off)
I_ST_SCR = enc(0x09, 5, 3, 0); I_LD_SCR = enc(0x05, 4, 3, 0); I_BR_SELF = 0xc0000000
def program(insns, at=CODE):
    words = list(insns) + [I_BR_SELF, 0]
    return ["put w 0x%x, 0x%08x" % (at + 4 * k, w) for k, w in enumerate(words)] + ["pc=0x%x" % at, "step %d" % len(insns)]
def setup(r5="0x5a5a5a5a"):
    return ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=%s" % r5, "r4=0x%x" % SENTINEL]
def printed(t, reg="r4"):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return "0x%x" % int(m.group(1), 16) if m else "absent"
def fate(alive, how): return "survived" if alive else "host " + how
def val(t, alive, how): return printed(t) if alive else fate(alive, how)
rows, bad = [], []
def row(name, got, want, why):
    ok = str(got) == str(want)
    rows.append(name); (None if ok else bad.append(name))
    #  STATUS LAST: gate 14 counts a row with `^<name>  .*ok$' / ` ok$' / ` FAIL$' -- a first draft printed the
    #  status before the note and the gate counted ZERO of 23 rows while the probe said DONE (caught by the gate, L1).
    print("%-16s %-14s %-14s %-60s %s" % (name, got, want, why[:60], "ok" if ok else "FAIL"), flush=True)
print("pcc2defaultkill DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-14s %-14s %-60s %s" % ("row", "got", "want", "note", ""))

t, alive, how = session(setup() + program([I_ST_SCR, I_LD_SCR]) + ["print r4"])
row("live", val(t, alive, how), "0x5a5a5a5a", "LIVENESS: scratch RAM st/ld round-trip")
t, alive, how = session(setup() + program([LD_BU(4, CHIPID)]) + ["print r4"])
row("devsig chipid", val(t, alive, how), "0x20", "DEVICE-SIGNATURE: CHIPID reads PCC2_ID through a guest ld.bu (RAM would read 0)")
# -- the eighteen named unimplemented registers, one session each direction
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in NAMED18]))
row("named wr", fate(alive, how), "survived", "guest st.b at all 18 named unimplemented registers in ONE session: (b) reinstated exit(1) kills on the first")
row("named wr msg", t.count(MSG) if alive else "n/a", 18, "one announce PER OFFSET: a whole-arm latch prints 1, an unlatched arm prints 18 too -- see `latch sameoff'")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in NAMED18]))
row("named rd", fate(alive, how), "survived", "guest ld.bu at all 18 in one session: the READ side of the defect; a writeflag guard that re-kills reads dies here")
row("named rd msg", t.count(MSG) if alive else "n/a", 18, "the read announce fires once per offset too")
row("named rd srvd", t.count("served 0x") if alive else "n/a", 18, "the read announce says what happened -- SERVED (the array's byte), never 'ignored'")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in INWORD]))
row("inword wr", fate(alive, how), "survived", "a byte inside each 32-bit counter/compare word (0x05, 0x09, 0x0d, 0x11): no case -> default:")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in UNNAMED]))
row("unnamed wr", fate(alive, how), "survived", "unnamed offsets 0x20, 0x24, 0x29, 0x35, 0x3d -- 0x3d is the one a backed store at len 4 would overrun")
# -- the disposition-pinning rows: read-after-write in ONE session
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), LD_BU(4, IEICR)]) + ["print r4"])
row("ieicr rdawr", val(t, alive, how), "0x0", "st.b 0x5a then ld.bu at IEICR in ONE session reads 0x0: the write was DECLINED (a backed accept reads 0x5a)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEERR), LD_BU(4, IEERR)]) + ["print r4"])
row("ieerr rdawr", val(t, alive, how), "0x0", "the same at IEERR (0x28), the write-to-clear class whose cased sibling SCCERR clears on write")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, SCCERR), LD_BU(4, SCCERR)]) + ["print r4"])
row("sccerr rdawr", val(t, alive, how), "0x0", "CONTROL: the CASED write-to-clear sibling reads 0x0 under either disposition -- makes the two rows above attributable")
# -- the latch: per offset, per instance
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEICR)]))
row("latch sameoff", t.count(MSG) if alive else "n/a", 1, "two writes to one offset announce ONCE: an unlatched arm prints 2")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEBERR)]))
row("latch twooff", t.count(MSG) if alive else "n/a", 2, "two offsets announce TWICE: a single whole-arm latch bit prints 1")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), LD_BU(4, IEICR)]))
row("latch rw one", t.count(MSG) if alive else "n/a", 1, "a write then a read at ONE offset announce once: the latch is per offset, not per direction")
# -- the fold and the text
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, 0x6a)]))
row("alias 0x6a", fate(alive, how), "survived", "0x6a folds onto 0x2a (`relative_addr %= PCC2_SIZE'): the MODEL's fold, not proven of the real part")
row("alias msg", t.count("offset 0x2a") if alive else "n/a", 1, "...and the announce names the FOLDED offset 0x2a: a changed fold names another")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, PRTICR)]))
row("dir wr text", t.count("unimplemented write to") if alive else "n/a", 1, "the announce says WRITE for a store (an inverted writeflag test in the text says read)")
t, alive, how = session(setup() + program([LD_BU(4, PRTICR)]))
row("dir rd text", t.count("unimplemented read from") if alive else "n/a", 1, "...and READ for a load")
# -- the cased arms are untouched
t, alive, how = session(setup(r5="0x82") + program([ST_B(5, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
row("genctl rt", val(t, alive, how), "0x82", "an IMPLEMENTED byte register still round-trips (no C040 bit in 0x82)")
t, alive, how = session(setup(r5="0x12345678") + program([ST_W(5, T1CMP), LD_W(4, T1CMP)]) + ["print r4"])
row("t1cmp word rt", val(t, alive, how), "0x12345678", "the cased 32-bit counter arm still round-trips a word: the fix swallowed no cased arm")
t, alive, how = session(["put b 0xfff4202a, 0x00"])
row("put b ctl", fate(alive, how), "survived", "CONTROL: the debugger's put b never reaches a DM_DEFAULT arm (measured before the fix too)")
row("put b ctl msg", t.count(MSG) if alive else "n/a", 0, "...so it prints nothing -- not a witness, a control")
print("PCC2D_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
if bad:
    print("PCC2D_RED=%s" % ",".join(bad))
print("PCC2D_PROBE_DONE")

```

## THE GATE SECTION (`git diff -- regress/gate_arm.sh`, VERBATIM)

```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index 65930c2..fa51fd9 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1303,6 +1303,26 @@ else
 fi
 
 
+#  ------------------------------------------------------------ pcc2defaultkill (#501)
+#  The default: arm of DEVICE_ACCESS(pcc2) ended the host on any access to an uncased
+#  offset, reads included.  Now: reads keep the served byte, writes are declined, one
+#  latched announce per offset per instance.  The witness (regress/artifacts/pcc2defaultkill/
+#  witness_20260905/, 7/13 on the committed build) is NOT run here; this is its detector.
+PCC2DLOG=$LOGDIR/pcc2_default.log
+python3 -u pcc2_default_probe.py "$PMAX" gate > "$PCC2DLOG" 2>&1 || true
+if ! grep -q "PCC2D_PROBE_DONE" "$PCC2DLOG"; then
+    check "pcc2 default probe completed" "no" "yes"
+else
+    check "pcc2 default probe completed" "yes" "yes"
+    for v in "live" "devsig chipid" "named wr" "named wr msg" "named rd" "named rd msg" "named rd srvd" "inword wr" "unnamed wr" "ieicr rdawr" "ieerr rdawr" "sccerr rdawr" "latch sameoff" "latch twooff" "latch rw one" "alias 0x6a" "alias msg" "dir wr text" "dir rd text" "genctl rt" "t1cmp word rt" "put b ctl" "put b ctl msg"; do
+        check "pcc2 default row: $v" "$(count "$PCC2DLOG" "^$v  .*ok$")" "1"
+    done
+    check "pcc2 default rows emitted" "$(( $(count "$PCC2DLOG" " ok$") + $(count "$PCC2DLOG" " FAIL$") ))" "23"
+    check "pcc2 default rows green"   "$(count "$PCC2DLOG" " ok$")"   "23"
+    check "pcc2 default rows red"     "$(count "$PCC2DLOG" " FAIL$")" "0"
+fi
+
+
 PITLOG=$LOGDIR/pit8253_latch.log
 python3 pit8253_latch_probe.py "$PMAX" "$STUB" > "$PITLOG" 2>&1 || true
 

```

## THE CHANGELOG BLOCK (as it stands)

```
# Round #501 pcc2defaultkill -- the `default:` arm of DEVICE_ACCESS(pcc2) ended the host on any access to an uncased offset, reads included; now reads keep the served byte and writes are declined, one latched announce per offset

**2026-09-05.  HIGH, ranked first by the 2026-09-04 fix-review adjudication.  Product change: `src/devices/dev_pcc2.c`
-- the `exit(1)` replaced by a per-offset latched `fatal()` (`uint64_t warned_unimpl`, one bit per byte offset) that
says DECLINED for a write and SERVED 0x%02x for a read, then `break` to the handler's single `return 1`.  Detector:
`regress/pcc2_default_probe.py`, 23 rows, run by gate 14.  Witness: rung 3, measured before the edit.**

## The defect and its witness

Forty-three of the 0x40 byte offsets have no `case` (derived from `mvme_pcctworeg.h` against the 21 labels; two seats
re-derived it): eighteen NAMED registers the model does not implement (PSCALECNT, GPIO_ICR/PCR, SCCMOIACK, SCCTXIACK,
IEERR, IEICR, IEBERR, SCSIERR, the printer block, SPEED, PRTDATA), the twelve bytes INSIDE the four 32-bit
counter/compare words, and thirteen unnamed offsets.  Any access to one of them -- a READ included, although the
memcpy above the switch had already served it -- reached `default:` and `exit(1)`.

**The witness (`regress/artifacts/pcc2defaultkill/witness_20260905/`), measured on the committed build BEFORE the
edit: 7/13.**  A guest `st.b` to IEICR (0x2a) ends the host with exit status 1, the arm's own `pcc2: unimplemented`
line printed first (the arm was reached); a guest `ld.bu` there likewise -- the READ side kills too; IEBERR and the
in-word byte 0x05 and the alias 0x6a kill the same way.  Liveness (the probe's scratch round-trip) and
device-signature (CHIPID reads PCC2_ID 0x20) controls pass.  **The debugger's `put b` does NOT reach the arm** -- it
survives and prints nothing -- which the filing had called the cheapest witness (measured false; corrected).  The
witness script is the width probe's own `session()` helper: a first draft hand-rolled the pty wait, accepted a
STALE prompt, and read every kill as "survived" -- the carrier's rule about hand-rolled pty plumbing, re-learned.
The combined IEBERR/IEERR row measures IEBERR only (the exiting build dies at the first); IEERR's kill follows from
source (codex).  **13/13 on the fixed build.**

## The design (pass 1: nine seats, `_scratchpad/panel_20260905_021751`, converged)

READ: keep the byte the memcpy served and SAY it is served -- it is the register array's default, not a computed
value, so this is not the option set's member 4 and a bounded announce about it is not a wrong record.  WRITE:
member 3, DECLINE + latched announce -- NOT member 6 (backed accept), on three warrants the seats measured or read:
the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear -- the board manual's SCLR bits
read as zero; the ICRs mask and reassert; PSCALECNT/SPEED/the IACKs are read-only); the addition licence is unmet
(no guest reaches these offsets on this model); a store from the one arm 43 offsets reach adds a bounded-write
surface into `pcctwo_reg[]` at 0x3d.  The Opus seat BUILT both candidates in a scratch clone and measured the
13-row witness at 13/13 under BOTH -- disposition-blind -- so the detector carries read-after-write rows in ONE
session (`ieicr rdawr`, `ieerr rdawr`: store 0x5a then load, want 0x0 -- a backed accept reads 0x5a) with the CASED
write-to-clear sibling `sccerr rdawr` as the control that reads 0x0 under either.

**Two premises of the pass-1 brief were wrong and are corrected here.**  The in-tree guest driver (`if_ie.c`) writes
three of these offsets, but NEVER RUNS on this model: `machine_mvme88k.c:106` installs `unreadable` at the 82596
address, `if_ie.c:407-409` fails its match on `badpaddr()` there, and `ie_setupram()` returns early at `:561-564`
before the PCC2 store at `:609` (Fable, Opus, grok, codex independently; verified).  `ie0` IS configured in
`conf/M187` and `conf/NFS` -- the brief's conf grep looked in the wrong files.  So the HIGH ranking rests on the
witness and severity, not on the driver.  And the alias the model implements (`relative_addr %= PCC2_SIZE`) is the
REAL part's: Motorola VMESBCP2 Table 6-1 lists `$FFF42040-$FFF42FFF  PCCchip2 Registers  Repeated` -- the codex seat
cited it, the manual was fetched into `_scratchpad/` and the line read (`vmesbcp2.txt:4629`).  Two seats had rightly
called the fold unestablished before the manual was on disk.

Recorded alternatives: the codex seat's ONE latch for the whole site, writes only (not adopted: a driver scanning
registers should see each distinct one announced; both forms are bounded).  Corrections to the option set from this
round: `return 0` denotes a FAILED TRANSACTION, not inherently unmapped hardware (an IACK cycle with no interrupt
pending times out on the real part).  Disclosed: the in-word bytes are the interior of IMPLEMENTED counters, declined
here as a width/alignment matter (`pcc2widecompose`), not claimed as unimplemented registers; the IACK offsets
0x23/0x25 are declined like the rest -- modelling them on the SCCRXIACK shape would open two new entries into the
C040 path, so `pcc2c040kill` goes first (filed as a cross-round obligation); per-instance latch scope is not
provable by two fresh sessions (each is a new process) -- a two-instance fixture is filed.

## The detector (`regress/pcc2_default_probe.py`, 23 rows; gate 14 pins them)

Controls: `live`, `devsig chipid`, `sccerr rdawr` (cased sibling), `genctl rt`, `t1cmp word rt` (the cased arms are
untouched), `put b ctl` + `put b ctl msg` (the debugger path never reaches the arm).  Survival: `named wr`, `named rd`
(all eighteen named offsets in ONE session per direction -- valid because the fix has no per-offset branch;
`named wr msg` localises), `inword wr`, `unnamed wr`, `alias 0x6a`.  Disposition: `ieicr rdawr`, `ieerr rdawr` (0x0,
not the stored byte), `named rd srvd` (the read announce says SERVED, never ignored).  Latch: `named wr msg` 18,
`named rd msg` 18, `latch sameoff` 1, `latch twooff` 2, `latch rw one` 1.  Text: `alias msg` (the announce names the
FOLDED offset), `dir wr text`, `dir rd text`.  The pty helper is the width probe's, extracted at run time -- the
frozen instrument is therefore a PAIR (both files copied beside the table).

## The kill table (`regress/artifacts/pcc2defaultkill/killtable_20260905/driver.log`; predictions in `PRETABLE_501.out`, mtime 04:12:20; table launched 04:12:43; frozen instrument pair md5 c76e053a / a080e2bc == live)

| run | predicted | measured | red rows |
|---|---|---|---|
| BASE (fresh clone of build/, rebuilt) | 23/23 | **23/23** | -- |
| `M_EXIT` -- the verbatim `exit(1)` body reinstated | 8/23 | **7/23** | named wr, named wr msg, named rd, named rd msg, named rd srvd, inword wr, unnamed wr, ieicr rdawr, ieerr rdawr, latch sameoff, latch twooff, latch rw one, alias 0x6a, alias msg, dir wr text, dir rd text -- sixteen (the prediction listed fifteen and miscounted its own green set) |
| `M_UNLATCH` -- `if (1)` for the latch test | 21/23 | **21/23** | latch sameoff 2, latch rw one 2 -- exact |
| `M_ONELATCH` -- one whole-arm bit (`1ULL`) | 19/23 | **19/23** | named wr msg 1, named rd msg 1, named rd srvd 1, latch twooff 1 -- exact |
| `M_BACKED` -- a store into `pcctwo_reg[]` added (member 6) | 21/23 | **21/23** | ieicr rdawr 0x5a, ieerr rdawr 0x5a -- exact; `sccerr rdawr` (the cased write-to-clear control) stayed 0x0 |
| `M_RDKILL` -- `if (writeflag == MEM_READ) exit(1);` | 18/23 | **16/23** | named rd, named rd msg, named rd srvd, dir rd text, latch rw one (the read in that session exits) -- as predicted -- plus ieicr rdawr and ieerr rdawr, whose store-then-LOAD sessions exit at the load |
| `M_DIRSWAP` -- the announce's direction test inverted | 20/23 | **20/23** | dir wr text 0, dir rd text 0, named rd srvd 0 -- exact |

Six of six killed; three predictions exact, two missed in the SAFE direction (more reds), each derived: M_EXIT's
prediction listed fifteen red rows against a green set of seven and so summed to 22 of 23 -- an arithmetic slip in the
pre-table, not a channel surprise; M_RDKILL's read-after-write rows contain a LOAD, so they die with the reads.  Every
mutant string was gcc-syntax-checked before the table (`mut_syntax2.py`, anchors from the driver's own `mut` lines) and
proven by a diff count against SEC; the clone restored from SEC, rebuilt, cmp-clean, sentinel cleared.  The
disposition-pinning rows did their one job: `M_BACKED` reads back the stored byte at both uncased offsets while the
cased sibling reads 0x0 -- the difference between member 6 and member 3, measured, with its control.

**Two runs, one prediction file.**  Run 1 (04:12-04:25, frozen default probe `c76e053a`) is the table above; its row
PRINT format put the status before the note, and gate 14 -- which counts rows by `^<name>  .*ok$` -- then counted
ZERO of 23 rows while the probe said DONE (`killtable_20260905/gate14_501_FAIL_rowformat.log`, 25 of 844 checks
red, the 251 width rows all green).  L1, fixed in-round: status last, as the width probe prints; the gate's own
patterns then count 23.  Run 2 (05:05-05:18, frozen `a96b8bcf`) re-measured the same six mutants on the fixed-format
instrument -- BASE 23, M_EXIT 7, M_UNLATCH 21, M_ONELATCH 19, M_BACKED 21, M_RDKILL 16, M_DIRSWAP 20 -- identical
to run 1 row for row; run 1 is kept as `run1_oldrowformat/`.  *A probe whose summary line is right and whose rows
the gate cannot count is a detector that would have shipped green and counted nothing; the gate is the check
that saw it, which is what a gate is for.*

## Gate 14 (`killtable_20260905/gate14_501.log`; the live probes -- default md5 a96b8bcf, width a080e2bc, both equal to the frozen run-2 pair; run alone 05:19-05:55)

`gate 14: ARM/Thumb flags: PASS (844 checks)`, `pcc2 default rows emitted 23`, `pcc2 default rows green 23`, `pcc2 width rows emitted 251`,
`pcc2 width rows green 251`, GATE_RC=0.  The previous run of this gate (04:26-05:00, `gate14_501_FAIL_rowformat.log`) had
counted ZERO default rows against a probe that said DONE -- the row-format defect described above -- and is kept.

<<PANEL501_OWED>>

## Records

OUTSTANDING_BUGS: `pcc2defaultkill` FIXED; filed from this round: `pcc2iackmodel` (SCCTXIACK/SCCMOIACK acknowledge
semantics on the SCCRXIACK shape, AFTER `pcc2c040kill`), `pcc2latchinst` (a two-instance fixture for per-instance
latch scope, a harness debt shared with the width latch).  `pcc2c040kill` gains the fact the design panel found: the
SCCRXIACK arm runs on READS (no writeflag test) and the console driver reads that offset, so the ENTRY into the C040
path is routine guest traffic -- only the arming (C040 set in GENCTL) is rare.  Ledger: witness
`probe:regress/artifacts/pcc2defaultkill/witness_20260905/defaultkill_witness.py`, detector
`regress/pcc2_default_probe.py`, every seat of both passes by name.  Carrier: the MVME187 manual added to the primary
sources; the member-5 wording.

```

## DISCLOSURE -- `git diff --numstat` (the `sgi_de_primop_probe.py` line is a pre-existing unrelated edit, not this round's)

```
118	0	CHANGELOG.md
20	0	regress/gate_arm.sh
20	6	regress/sgi_de_primop_probe.py
38	7	src/devices/dev_pcc2.c

```


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
