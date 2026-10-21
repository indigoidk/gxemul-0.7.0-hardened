Seat key: **AX** GPT-6 Astra (file-reading), **GK** Grok 4.7 (file-reading), **GL** GLM 5.3 (packet-fed), **FB** Fable 5.1
(file-reading), **AR** Argon (packet-fed).  Each seat's own finding number is in brackets.

**F1 -- FLOOR BREACH (predicted, not yet built): the announce's DIRECTION predicate can be swapped to a body-read value
and every row stays green.**  AX [F8]: *"Replace only the population-2 announcement's direction condition: `- if
(writeflag == MEM_WRITE)` / `+ if (idata)`.  This should preserve all 34 greens ... Every tested population-2 store is
nonzero: a5a5a5a5, d4, c3d4, or 1122334455667788; reads leave idata zero.  A guest's first zero store to a fresh
population-2 register would instead produce a read/served announcement."*  **Checked by reading** the probe: every store
to a population-2 offset uses r2 = 0xa5a5a5a5, r12 (the 0xd4 / 0xc3d4 narrow value) or r10 (0x1122334455667788) --
section 5c; no row stores zero there.
**Disposition: ACCEPTED as a clause-(d) floor breach** -- the predicate `writeflag == MEM_WRITE` is one the fix ADDED,
and `idata` is a field the guarded body reads (it is printed), which is exactly the operand-swap form the DEPENDS-ON
enumeration names.  **Change:** measure leg M_IDATA on the frozen rev-2 instrument FIRST (predicted 34/34 -- if it reds,
the finding is refuted and recorded so); then probe REV 3 adds a first-access ZERO STORE to an untouched population-2
register, wanting the WRITE-form line `... (len 4): 0x0 -- declined.  (once) ]`; M_IDATA must red rev 3.

**F2 -- WRONG RECORD (product comment): the typedef claims more than it checks.**  GL [F5], FB [F1], AX [F1, as DEFECT],
GK (Q1b: "The 1ULL conjunct ... was not its own leg").  FB: *"Only the field is checked; `sizeof(1ULL)` in the typedef
is a different literal from the arm's.  A `1u` in the arm compiles with no diagnostic ... at runtime `1u << 35` is UB
and on x86-64's 5-bit shift mask lands on bit 3 = SLAVELMOD2's."*  AX wants a shared definition used by both shifts
and the check; FB and GL want the comment reworded (FB: "take the reword now and file the macro").
**Disposition: ACCEPTED; fix REFINED (see D5):** reword the comment to claim the FIELD only, DELETE the tautological
`&& (VME2_MISC >> 2) < 8 * sizeof(1ULL)` conjunct (a check that cannot fail, with no runtime footprint -- the binary is
unchanged), and MEASURE leg M_ONENARROW (both arm literals `1ULL` -> `1u`) on rev 3, so the comment may say what catches a
narrowed literal at run time instead of claiming a compile-time guard it does not have.

**F3 -- WRONG RECORD (product comment): "The in-tree OpenBSD 2.2 guest reaches six of them".**  GL [F4], FB [F7], AX [F5].
FB, verified in the guest source: six registers have guest SITES (MASTERCTL, MASTER3, MASTER4, MASTER4MOD, IRQSTAT,
IRQCLR), but IRQCLR is written only inside `if` on a non-zero IRQSTAT, so under this model the guest REACHES five; and
"in-tree" reads as GXemul's tree.  **Disposition: ACCEPTED.**  New wording: the OpenBSD 2.2 mvme88k driver
(`sys/arch/mvme88k/dev/vme.c`) has access sites at six of them and, with IRQSTAT served 0, reaches five.

**F4 -- NIT (product and gate comment): `default:`'s "memory_rw then raises the m88k data-access exception" is
unqualified.**  FB [F8], AX [F5].  An instruction fetch gets INSTRUCTION_ACCESS; NO_EXCEPTIONS callers never reach the
arm.  **Disposition: ACCEPTED:** "for a guest data load or store", in the device and in the gate block's comment.

**F5 -- the read announce prints `0x%x` of `(unsigned) odata` where pass 1's D2 named `0x%llx` / `(unsigned long long)`.**
GL [F6] ALIGN, AX [F4] ALIGN (NIT); FB [F10] KEEP and amend D2's record; GK [F4] KEEP and amend.  Two-two -- **see D1.**

**F6 -- DEFECT (landing) + WRONG RECORD (pass-2 packet section 3): the probe-wiring MANIFEST registration does not exist,
and SCORE_CLAIMS_MANIFEST is still 36.**  FB [F2], AX [F7], GK [F2].  The working tree's `check_probe_wiring.py` diff
(+15) is entirely OTHER units' lines (b115, wdcnullxfer, wdcrearmzero, fbclearread and a #563 comment); my packet's
section 3 described it as this round's.  **Disposition: ACCEPTED.**  The commit builds that file from HEAD's blob plus
this round's lines only: `regress/vme_default_probe.py` CLASS_DETECTOR (gate 14, pinned by EQUALITY at rev 3's row
count), the frozen probe copies CLASS_WITNESS, the leg generators / comparators CLASS_TOOL, the witness scripts
CLASS_WITNESS; `SCORE_CLAIMS_MANIFEST` 36 -> 37.  The packet-section-3 misdescription is recorded as a brief defect.

**F7 -- WRONG RECORD (probe docstring): "NO KILL TABLE EXISTS FOR THIS REVISION" and its neighbours.**  GL [F12], FB [F3],
AX [F10], GK [F3].  Additions: cite BOTH tables by full hash; keep the original predictions AS DATED PREDICTIONS (AX);
"a design claim until a kill table measures it" is now measured; the docstring's claim that EVERY device session opens
with `ld r30,r3,0x88` is false -- the control session reads VBR into r5 after an `or`, the cased census into r13 (AX);
the docstring cites scratchpad files with no durable copy (FB) -- now copied to `probe_20261020/`; mark which per-mutant
counts in the ROW PLAN were measured and which were never built (FB: "a latch set at one constant bit (51)", "a
per-direction latch (52)").  **Disposition: ACCEPTED, all of it, in rev 3's docstring.**

**F8 -- DEFECT (instrument reporting): product-reddable rows sit in CONTROL_ROWS.**  GL [F11], FB [F4], AX [F6], GK [F5].
`cased census`, `t1cmp rt` and `free ctl` red under product edits (M_DROPTCTL, M_DROPIRQEN, M_T1CMPWRDROP), so those kills
print CONTROL=FAIL -- a product failure under the apparatus reason.  AX: *"CONTROL failure cannot establish an apparatus
cause ... Move functional expectations into detector classification with separate apparatus controls."*  GK and FB: do
it at the next instrument revision, not by unfreezing the measured one.  **Disposition: ACCEPTED, in REV 3** (rev 3
exists anyway because of F1, so "next revision" and "now" coincide): CONTROL_ROWS = `session`, `live`, `neg apparatus`,
`unasm`, `vbr reset` (the device-presence signature), `free neg ctl` (the free-running proof); `cased census`, `t1cmp
rt`, `free ctl` and `free quiet` become scored detector rows.  See D2.

**F9 -- WRONG RECORD (instrument text): "(FAILED FOR SOME OTHER REASON)" on red rows whose stop IS the leg's edit.**  AX
[F11]: change before shipping, neutral wording (`dependent check not exercised: pass 1 did not complete`; `unexpected
stop pc=0x18 before announce verification`), keep them red.  GL [Q5b]: accurate, keep.  GK [Q5b]: leave it; the miss
note is the place.  FB [F9]: the second-pass text is honestly dependent; the non-word session's stop text misattributes
an own-channel kill -- change it at the next revision.  **Disposition: ACCEPTED in REV 3** with AX's neutral wording;
every such row stays red.  See D3.

**F10 -- COVERAGE DEBT from the one ask-again (clause e unless you show otherwise), with predicted 34/34 escapes:**
* (a) FB [F5]: the latch SET conditioned on width -- `if (len == 4)` in front of `d->warned_unimpl |= ...` -- leaves every
  non-word access announcing on EVERY access, an unbounded guest-drivable `fatal()` (the flood class).  The two-pass
  sessions use `ld`/`st` only; the non-word session touches each register once.
* (b) FB [F6], GK [Q3/F6], AX [F9 tail]: `default:`'s `debug(` -> `fatal(` (or deleting the two `debug()` lines) -- host
  output at population-1 faults is pinned by nothing; D5's text rests on review.
* (c) GL [F8]: `if (len == 2 && (relative_addr & 3) == 0) break;` in `default:` -- a halfword/byte at a WORD-ALIGNED
  population-1 offset declines instead of faulting; `p1 widths` probes only lanes 1-3 and len-8.
* (d) GK [Q3], FB: `case 0x91:` (any unsampled population-1 interior) added to the decline list -- already NOT CLAIMED.
* (e) GK [F6]: deleting the whole typedef -- all 34 green (a compile-time guard has no runtime row; M_CAPNARROW is a leg).
**Disposition: REFINED -- take (a), (b), (c) under L1 (pre-ship construction) in REV 3, because each is one or two
accesses in an EXISTING session: a second pass over the six non-word accesses wanting 0 lines; a count of `[ vme:` text
in the free-running population-1 census wanting 0; two lane-0 accesses (`ld.hu` and `st.b` at word-aligned population-1
offsets) added to `p1 widths`, 6 -> 8 faults.  FILE (d) and (e) as disclosed coverage debt.**  Both FB and GL
recommended FILING (a)-(c) -- **see D4**.

**F11 -- WRONG RECORD (pass-2 brief premises): the enumerations were incomplete.**  GL [F2], FB [Q1d], AX [F2], GK [F1]:
the `return 0` set also holds the 2964 sub-word starts inside population-1 words (AX: 7554 (offset, length) pairs per
direction reach `default:`).  AX [F3]: the brief's S4 says population 4 (a cased base at len != 4) reaches the fault --
**it does not**: byte and halfword accesses at all ten cased bases match their exact label and are SERVICED (and `ld.d`
succeeds at 0x00/0x50/0x60/0x80/0x88).  **Disposition: ACCEPTED** -- brief errata; the CHANGELOG block and the probe
contract state the correct sets; population 4 is described as serviced by the cased arm (with the `vmewidthlanes` lane
defect), never as faulting.

**F12 -- WRONG RECORD (contract): NOT CLAIMED lines are missing.**  GL [F10] (word-aligned narrow/double accesses at the
~22 population-2 registers no non-word row touches), AX [F9] (population-2 non-word offsets, cross-width latch reuse
and store-data patterns are SAMPLED; the fault rows do not assert the two `debug()` lines), FB [Q4e] (F10a's class; host
output at population-1 faults; D7's negative control lives only in the table), GK [Q4e] (the fault rows pin `return 0`,
DMA0 and DMT0, not the `debug()` text).  **Disposition: ACCEPTED** -- each becomes a NOT CLAIMED line in rev 3's contract
(those F10 (a)-(c) now rows are struck from it).

**F13 -- WRONG RECORD (kill-table observation (b)): the per-row kill census counts DEPENDENT reds as independent kills.**
FB [F9]: `p2 ann rd 2` / `p2 ann wr 2` each hold 3 own-channel + 4 dependent reds; `p2 nw rd` under M_WRFAULT and
`p2 nw wr` under M_LENFAULT are dependent.  **Disposition: ACCEPTED** -- a dated records note beside the table; the
table itself is not edited.

**F14 -- NIT (gate comment): "mvme88k/mvme187 constructs from the PROM, like the mk48/pcc2 blocks above".**  FB [F15]:
this probe constructs with `-M 64` and a 4-byte dummy at 0x10000, no PROM image.  **Disposition: ACCEPTED.**

**F15 -- RECORD FORM (clause c).**  GL [F9], FB [F13], AX [Q4c]: `(c): measured at
regress/artifacts/vmedefaultkill/killtable1_20261020/legs/NULL.raw` (the vme `device_add` removed from
`machine_mvme88k.c`; 5/34, CONTROL=FAIL).  **Disposition: ACCEPTED** -- the CHANGELOG block carries that line (and rev 3's
table re-measures it).

**F16 -- EVIDENCE GAP (gate run) -- RESOLVED.**  GL [F7]: "the gate-14 block has no measured run in the packet."  Now
measured both ways and inside the full gate (section 1).  **Disposition: ACCEPTED and discharged.**

**F17 -- PROVENANCE (legs).**  AX [Q1e]: freshness of the leg builds is *"corroborated historical evidence, not
independently remeasured"*; the build logs are not in the preserved directory.  **Disposition: ACCEPTED** -- copy the
per-leg build logs (`killtable1/build/*.build.log`, `table1b/build/`) beside the tables.

**F18 -- RECORD: FB withdrew its pass-1 D1 dissent.**  FB: *"My pass-1 D1 dissent (a bound test in `default:`) is
WITHDRAWN: M_ADD94 and M_ADD90 measured that the label form's growth edit is caught by the census."*  **Recorded.**

{ARGON}
