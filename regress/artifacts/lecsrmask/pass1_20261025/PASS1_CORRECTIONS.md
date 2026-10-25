# lecsrmask pass 1 -- corrections to the brief (`packet.md`), each found by a seat and VERIFIED by the main loop

Written 2026-10-25 04:5x, after six of the seven fired answers were read (codex, grok, GLM x2, DeepSeek x2; Argon via agy
WALLED -- see `argon_transport_20261025.txt`; its web-route firing is pending).  The brief itself is left as the seats
answered it; this file is the correction record and feeds the adjudication packet.  Each item: the brief's claim, the
correction, the evidence as READ here, who found it, and the disposition.

## C1 -- "TM1986's extracted prose carries no 'read as zeroes' sentence" (brief 3.4 D2, 9.2, P2) is FALSE

Found by grok and codex.  Verified by reading `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\lance\TM1986.txt` (Am7990 LANCE
Technical Manual, AMD 1986):

```
1539:                Reserved and read as zeroes.                             RINT            <- RAP bits 15:02
1545:     01 :00 CSR(1 :0) CSR address select. READ/WRITE.
1695: 01  STRT START enables the LANCE to send and                                   15:08 RES Reserved.      <- CSR2
1697:             receive packets, perform direct memory ac- 07:00 IADR The high order 8 bits of the address of the first
1732: CONTROL AND STATUS REGISTER 1 (CSR1)                                           Bit Name Description
1733: READ/WRITE: Accessible only when the STOP bit of CSRo is
1734:                                                                                15:03 RES Reserved and read as "O".   <- CSR3
1745: 15:01 IADR  The low order 15 bits of the address of the first
1746: 00          word (lowest address) in the Initialization
1749:             Must be zero.                                                                                           <- CSR1 bit 0
2853: 4.1 SOFTWARE TASKS                                                        CSR1 and CSR2 are normally not affected when the Stop bit is
2854:                                                                           set in CSRo. (When the Stop bit is set, CSR3 is cleared and
2855: First the LANCE interface with the system is checked out both             CSRo is set to 0004 Hex, Stop bit set.) However, it is recom-
2856: in Bus Master and Bus Slave Mode, and the internal logic of               mended to reload CSR1 and CSR2 whenever the Stop bit is
2857: the LANCE is tested in diagnostic mode for both internal and              set.
```

So the Am7990 manual says: RAP 15:2 and CSR3 15:3 read as zero; **CSR2 15:8 only "Reserved."**; CSR1 bit 0 "Must be zero."
**How the brief got it wrong:** the drafting grep for `CSR2|CSR3|IADR|BSWP|ACON|BCON` was cut with `head -40`, which ended
around line 879, before the register-description pages (1530-1750) -- the pattern-that-selected-nothing class, in the
brief's own primary-sources section.  Disposition: L4 record correction (this file + the CHANGELOG block); the design
question it opens is C2.

## C2 -- the CSR1 / CSR2 masks are C-LANCE behaviour; on the Am7990 the reserved bits are WRITABLE (hardware-diagnostic evidence)

Found by grok (citing MAME); verified by fetching MAME's source directly, 2026-10-25 04:4x:
`https://raw.githubusercontent.com/mamedev/mame/master/src/devices/machine/am79c90.cpp`, register-write handler, VERBATIM:

```
		case 1: // Least significant 15 bits of the Initialization Block
			// Datasheet says "must be zero", but doesn't indicate what
			// happens if it's written non-zero. Must be writable to pass
			// system diagnostic on MIPS RS2030.
			if (m_csr[0] & CSR0_STOP)
				m_csr[1] = data;
			break;

		case 2: // Most significant 8 bits of the Initialization Block
			// The C-LANCE datasheet explicitly states these bits read and
			// write as zero, while LANCE datasheet just says "reserved".
			// MIPS RS2030 diagnostic requires these bits to be writable,
			// so assuming this is older device behaviour.
			if (m_csr[0] & CSR0_STOP)
				m_csr[2] = (type() == AM7990) ? data : (data & 0x00ff);
			break;

		case 3: // Bus master interface
			if (m_csr[0] & CSR0_STOP)
				m_csr[3] = data & CSR3_MASK;
			break;
```

So another emulator, modelling BOTH chips, stores CSR1 whole on both and CSR2 whole on the Am7990, because a hardware
diagnostic for an Am7990 board (the MIPS RS2030) requires the reserved bits to read back as written -- a program written
against real silicon, which is the strongest evidence in this round about what the Am7990 does.  The Am79C90 datasheet's
own Appendix B (`am79c90_bitsavers.txt` 3411) lists a CSR1/CSR2 difference between the two chips (preservation across
STOP), so the chips are not bit-for-bit identical in these registers.  rpajarola `e108b54` applies the C-LANCE masks
without distinguishing the chip.  `dev_le.c` models "LANCE ethernet, as used in DECstations" -- the Am7990 (`TM1986`,
the KN01's chip; the Am79C90 is the later CMOS part).

**Disposition proposed for the adjudication pass (not yet ruled):** narrow the repair to CSR3 (`x & 0x0007`, settled by
BOTH manuals and by MAME); leave CSR1 and CSR2 stored whole as the Am7990 does, record WHY (this item's evidence), and
file the CSR1/CSR2 read-back question as its own documented row carrying both readings (rpajarola's C-LANCE masks and
the 3MIN PROM test he cites; MAME's RS2030 diagnostic).  The detector's CSR1/CSR2 rows then pin the stored-whole
behaviour as a deliberate contract (FIX wants 0xffff / 0xffff / 0x1235 for `csr1 all` / `csr2 all` / `csr1 odd`), so a
later C-LANCE-style change must re-pin them with the oracle-correction order.  Pre-fix GATE then reads 17/18 (only
`csr3 all` red), measured again before landing.

## C3 -- S6 / P5 ("the read-back is the fix's only guest-visible consequence") is FALSE for CSR1 bit 0

Found by codex.  Verified: `le_chip_init()` line 179 builds `init_block_addr` from `reg[1] & 0xffff`; `le_read_16bit()`
(line 136 onward) masks SRAM addresses with `SRAM_SIZE-1` = 0x1ffff and so PRESERVES bit 0; the initialisation block
(mode, MAC, LADRF, RDRA/RLEN, TDRA/TLEN) is read from `init_block_addr + 0 .. +22`.  Under a CSR1 mask a guest that wrote
an odd address would have its block read one byte lower than today -- a change in device behaviour on every machine
sharing the model, not only in a read-back.  Under C2's proposed narrowing CSR1 is not masked, so this consequence does
not arise; the record must still say so (the brief's "read-back only" sentence is withdrawn either way).

## C4 -- S14 ("got 78 vs pinned 77 ... gate 6 red at HEAD") needs its population named

Found by codex (committed-HEAD count) and grok (the working-tree file changed after the brief was fired).  Verified from
the derive tool's own output and `gate_hygiene.sh`: the census counts the TREE the battery runs in, and this tree holds
the peer's UNTRACKED `regress/lca_isaphys_probe.py` (named in `GRANDFATHERED_PROMPTLESS` and in the gate's comment at
451: "76 -> 77 (75 committed + this probe + lca_isaphys_probe.py, still untracked)").  So: tracked pty probes at HEAD =
77 = the old pin; working tree = 78 (the untracked file); the committed-HEAD defect is the NAME SET --
`wdc_lba_probe.py` (committed in 0901b388, promptless) absent from `GRANDFATHERED_PROMPTLESS`.  The follow-up commit's
pin 78 is right for the tree the weekly battery runs in; its CHANGELOG paragraph is to carry this sentence.  S14 was
read by grok AFTER `derive_hygiene_pins.sh --write` had changed the working-tree file (04:2x) -- expected, not a defect.

## C5 -- the variant predictions V18 and V19 under-counted their red rows

Found by GLM (both), DeepSeek (V19), grok (V19 N12), codex (V19).  Verified by arithmetic on the rows' wants:
V18 (one mask 0xfffe for all three) reds N7 (0xfffe), N8 (0x0005 & 0xfffe = 0x0004), N9 (0xfffe), N10 (0x00a5 & 0xfffe =
0x00a4) -- the brief listed N7 N9.  V19 (masks shifted one label) reds N7 N8 N9 N10 N11 N12 N13 N14 (N8 0x0004; N12
0x1235 & 0x00ff = 0x0035) -- the brief listed six.  Both under-predictions are in the safe direction; the tables in 7.4
(channel columns of N8, N10, N12) and 7.5 are corrected by this item.

## C6 -- the anchor explanation (7.6) was wrong about the mechanism, right about the rows

Found by grok, codex, GLM.  The RDP and RAP ports are FOUR bytes apart (`case 0:` / `case 4:`); a one-halfword window
shift lands the RDP access on an unimplemented offset (odata 0), not on RAP; a one-WORD shift exchanges them.  Either
way `csr0 reset` (N5) and `rap mask` (N6) go red on channels outside the decode (the reset value; the RAP masking), which
is what R7 asks.  Corrected wording for the contract.

## C7 -- "big-endian host" (3.3, 7.2) should read "big-endian emulated machine"

Found by codex: `d->is_bigendian = machine->cpus[0]->byte_order == EMUL_BIG_ENDIAN` (line 1064) is the EMULATED CPU's
byte order, not the host's.  Wording correction.

## C8 -- the detector revision's docstring and header need four corrections before it ships (L1)

Found by codex, grok, GLM.  (i) "every want is a literal" excludes the four `stable:<s>` rows, whose want is the first
observation; (ii) "the last RDP value read a second time" is wrong -- the probe reads the ALL value twice, immediately
(`v1` then `a2`), before the accept writes; (iii) N12 (`csr1 odd`, 0x1235) is not a dropped-bit-ALONE input -- it sets
bits 0, 2, 4, 5, 9 and 12; (iv) the CATCHES / OUTSIDE contract of 7.6 is NOT in the probe's header at all -- it must be,
with C6's wording and C2's disposition once ruled.  Also the "n/m mnemonics agree" line is informational and reads like
a failure: label it so (the word check is the control).

## C9 -- a better in-tree precedent for "reserved bits read as zero" than the one the brief cited

Found by codex: `dev_footbridge.c` 659-663, `case TIMER_1_LOAD:` stores `d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;`
-- the implemented bits masked AT THE STORE, which is M1's shape.  The brief's `#572` precedent preserves reserved select
bits for exact read-back, the opposite disposition; it is a precedent for storing what the chip would hold, not for
masking.  Verified by reading the lines.

## C10 -- a new filing: the RAP warning's format mismatch

Found by codex.  `dev_le.c` 1017-1020 passes `idata` (a `uint64_t`, line 939) to a `%i` conversion -- a variadic-format
mismatch (undefined behaviour under C99 7.19.6.1p9; on this ABI it prints the low 32 bits).  Not this round's edit; filed.

## C11 -- both STOP comments in `DEVICE_ACCESS(le)` invert the datasheet's condition

Found by every seat that read 8.3 (GLM, DeepSeek, grok, codex); the brief named only the first.  986-991 says a read
"should return 'undefined' result if the stop bit is set"; 996-1001 says a write "when the stop bit is set should be
ignored".  Both manuals say the opposite: CSR1-3 are "Accessible only when the STOP bit of CSR0 is a ONE" (TM1986 1733;
C-LANCE 1123-1124, 1146-1147, 1197-1198).  The Ultrix observations the comments record are of IN-SPEC accesses.
Disposition: correct both comments in the same change as records work (L4), keeping the Ultrix note with its corrected
meaning (codex, GLM) -- or file (grok).  For the adjudication.

## C12 -- grok's PMAD-AA and DEPCA citations are not from files on disk

`grep -rli PMAD-AA _scratchpad` finds only earlier seats' answer files, no specification; `am7990_ds.txt` is an unreadable
scan.  grok's section numbers (PMAD-AA 6.1.2.4-6.1.2.6) and the DEPCA extract are web-sourced and UNVERIFIED here; grok
itself labelled the DEPCA line "a dissent, not a settlement".  They are recorded as readings, not evidence.

## C13 -- clause (b) owes per-register verbatim restorations in the table

Found by codex.  V1 restores all three stores at once; the floor's clause (b) is "at EVERY fixed site", so the table owes
a CSR3-only revert (and, if C2 is not adopted, CSR1-only and CSR2-only reverts), each predicted 17/18 with CONTROL=OK.
Under C2 the fixed site is one, so one verbatim revert discharges (b).

## C14 -- seats: Argon via agy WALLED at launch (quota, resets in ~136 h); the web route is being fired with a trimmed
## packet (the job maker's 60,000-byte cap); Fable HELD (its question in `FABLE_HOLD_QUESTION.md`)

## C15 -- floor legs measured before any edit (the three-mask detector revision, md5 9f4bb210)

`regress/artifacts/lecsrmask/floor_20261025/RUN_IDENTITY.txt`: L0 (pre-fix build, GATE mode) `LE_CSRMASK_RESULT=14/18`
`CONTROL=OK` rc=1 -- clause (a); L3 (null medium `/bin/false`) `LE_CSRMASK_RESULT=0/18` `CONTROL=FAIL` rc=1 --
`(c): measured at regress/artifacts/lecsrmask/floor_20261025/RESULTS_L3_nullmedium.txt`.  P12's prediction held; the
dead-child path waits through four breakpoint deadlines (~8 min), as codex predicted.  Under C2 the shipping detector's
L0 becomes 17/18 and both legs are re-run on the re-pinned revision.
