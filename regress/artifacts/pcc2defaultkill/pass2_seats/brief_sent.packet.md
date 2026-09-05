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

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot
settle from this packet rather than guessing at it.
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

## THE PRODUCT DIFF (VERBATIM)

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

## THE THREE QUESTIONS

**1. Is the fix right (the arm is in the diff above: `break` to the single `return 1`; the shift defined by the fold;
the read announce's value), and which accepted disposition is wrong, by number?**

**2. From the kill table and predictions above: does any mutant's result contradict its prediction, and does the
detector pin DECLINE against BACKED ACCEPT by a channel other than survival?**

**3. Should #501 close and commit?  Carry the denominator.**
Anything you cannot settle from this packet: one line.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
