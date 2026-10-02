## 2026-10-02 -- GXEMUL [087a90]: `#555` gives ids to this file's ID-LESS entries -- 130 rows, 43 sentences added in place, 104 passages pointed at the id that carries them

**NONE OF THE 130 ROWS BELOW IS FIXED BY THIS SECTION.**  This file names most rows by a short backticked id, and
some entries record open work in prose only.  A row with no id cannot be claimed, ranked or closed, and the ledger
cannot see it.  GPT-6 Astra scanned the file for such entries at commit `db8b1a33` (279 claimed); the grok seat
ruled each one first-hand, and 13 more that it found the scan had missed; Astra confirmed, overturned or amended
each ruling (`regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`, 292 dispositions).  The table derived
from that record was checked by Astra, every finding of that check was ruled first-hand by grok, and what grok held
went back to Astra.  Astra's closing check of the assembled result found eleven further things; they are repaired,
grok ruled the ones that were not the assembler's own mistakes, and one of them is the class row below.  The result
is `IDLESS_TABLE2.tsv`, assembled by `mk_itable2.py.txt` from the seats' own lines and
written out below by `records555.py.txt` (both kept under `regress/artifacts/idless_20261002/`).

**What is here.**
* 130 rows -- 7 HIGH, 29 MED, 94 LOW.  129 of them are AN ID FOR AN ENTRY THIS FILE ALREADY CARRIES IN
  PROSE: no second entry is opened, and each row names the lines of its prose as of `db8b1a33`.  The 36 HIGH and MED
  rows have their own headings and ledger rows; the LOW rows are written out by id under the class row `idlesslow`.
* One row is of another kind: `closeassessrows` (MED), a class row for a records defect of the LEDGER that the review found
  while checking which rows carry this file's prose.  A sweep on 2026-08-27 closed rows on the adjudicator's note
  `CLOSE (assess)`, which signs off the assess stage; 8 of the rows it closed still name work that is not done.
  Nothing is re-opened here: that is the class row's work, one decision per member.
* 43 sentences ADDED IN PLACE, each beginning `[#555, 2026-10-02 -- the id-less review: ...]`.  41 follow a
  passage whose text is stale: the source shows the thing it names done, closed or changed.  That is a count of
  sentences, not of passages wholly closed -- 5 of them say what is done and name the id that carries what stays
  open.  2 follow passages the review had called unsettled, one settled by the source and one by the manuals.
  Nothing was deleted or rewritten: the old text stands, and the sentence follows its paragraph (inside the last cell
  of the row where the passage is a table row).
* The heading of `m88kidleslotsem`, a row `#554` filed, is corrected in place.  Its title stated one half of the entry it names
  (lines 4675-4682 at `db8b1a33`): the slot that writes the polled word.  GPT-6 Astra held that the row therefore did
  not cover the entry's accumulating, MMIO and order-sensitive slots and asked for a second row; the grok seat held
  that the id is the whole entry's.  Both are right about what they read -- the id was proposed for the whole entry and
  the title stated half of it -- so the title now states the entry's own sentence and no second row is opened.  Astra
  then withdrew its demand (`ifile_04`, part C), on one condition that binds whoever closes the row: the closure must
  cover BOTH halves, and correcting only the premature-idle case would not close it.

**What is NOT here, so that a blank is not read as "nothing owed":**
* 104 passages get no row because an id carries them; they are listed at the end of this section with that id or
  those ids -- a row that existed before this section, or one of the rows above (marked).  A carrying id's ledger state
  is given where it is not `open`.  8 of the passages are carried only by rows that are closed or dropped; GPT-6
  Astra read each of those and found nothing still open in them (`ifile_04`, part D).  Four more were in that state
  and DO record open work: three are now also pointed at `closeassessrows` and one at `gdromtailcov`.
* 35 entries were ruled KEEP-AS-IS (history, or a rule).  The check of the table found that 17 of them still
  record work an id carries -- those are in the list at the end -- and 18 owe nothing (`IDLESS_NOTOWED.tsv`).
* 4 entries stay UNSETTLED; each is listed at the end with what is unsettled.  Three entries called a manual
  unopened or absent.  The manuals are on this machine, in the project root's `_scratchpad/`, outside the git tree the
  seats read; grok read them (`regress/artifacts/idlessread_20261002/`).  They settle one entry (the `lwarx` /
  `stwcx.` reservation: a sentence is added in place) and do NOT define `FSCA` or `lvx` / `stvx`, so those two stay
  unsettled for want of documents that are not here: an SH-4A software manual and the AltiVec programming
  environments manual.
* The agy seat's audits of the table: 4 of 9 answered before its quota wall of 2026-10-02 13:58, and the
  eight claims in them that no other seat had made were ruled by grok (`grok/grok_irule_c.txt`).  The other 5
  (`icite_04to09`, `ifiled_a`, `ifiled_b`, `ifiled_c`, `ikeep`) did not run; what they find is owed to a later records round.
* The flagship seat was deliberately not fired on 2026-10-02 (owner instruction); its sign-off on this unit is
  batched with `#554`'s, not waived.

### HIGH -- 7 rows

#### `qhslowifetch` (HIGH, an id for an entry this file already carries in prose) -- PPC slow ifetch still calls exit on a failed instruction read, separate from the Thumb stops already filed as armthumbabortkill
the prose: 2614-2615 scoped to PPC (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt C11 (conceding in part Astra's ifile_01 finding)]

#### `qhppciphack` (HIGH, an id for an entry this file already carries in prose) -- MSR.IP stops the CPU instead of selecting the exception vector base
the prose: 2616 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qhrdhwrpolicy` (HIGH, an id for an entry this file already carries in prose) -- unimplemented RDHWR selector stops the CPU and there is no HWREna gate
the prose: 2617-2619 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qharmexalign` (HIGH, an id for an entry this file already carries in prose) -- Both queue passages record one defect: unaligned LDREX and STREX halt the emulator, though an alignment Data Abort is mandatory when (A,U) is not (0,0) and the halt is wrong under either setting.
the prose: 3625-3626; 4181-4202 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_ititles.txt]

#### `shreservedexit` (HIGH, an id for an entry this file already carries in prose) -- Privileged data access in the SH reserved hole still exits the emulator.
the prose: 8148 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_ititles.txt]

#### `qhppcdecode` (HIGH, an id for an entry this file already carries in prose) -- Ten PowerPC floating-point encodings still stop emulation: fctid, fctidz, fcfid, fcmpo, fmadds, fmsubs, fsqrt, fsqrts, fres and frsqrte
the prose: 1705-1716 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_icompound.txt (a compound disposition: the table's derivation had dropped this row)]

#### `qhm88kstops` (HIGH, an id for an entry this file already carries in prose) -- An MB89352 data-register read with no transfer object stops the emulated CPU
the prose: 2616 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_icompound.txt (a compound disposition: the table's derivation had dropped this row)]


### MED -- 29 rows

#### `qhppcni` (MED, an id for an entry this file already carries in prose) -- PPC FPSCR NI is defined and never consumed, and that Non-IEEE flush policy must not be pushed into the generic encoder
the prose: 1656-1657 and 3086 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt C5 (conceding Astra's ifile_01 finding)]

#### `qharmsxtadd` (MED, an id for an entry this file already carries in prose) -- sxtab and sxtah take the undefined-instruction path
the prose: 1843-1848 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qharmmediaver` (MED, an id for an entry this file already carries in prose) -- ARMv6 media encodings decode on the modelled ARMv4 CPUs
the prose: 1870-1872 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qhshdecode` (MED, an id for an entry this file already carries in prose) -- Modeled SH-4 machines still lack SGR transfers and DBR memory-transfer forms; other historical encodings are qualified by CPU model, and the historical list's SH-4A-only instructions are excluded
the prose: 1899-1903 and the SGR/DBR clause of 2945-2948 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt C6 (conceding Astra's ifile_01 finding)]

#### `qhscifssr` (MED, an id for an entry this file already carries in prose) -- SCIF SSR stores guest writes verbatim, the receive path maintains DR and does not generate RDF, FDR clamps the receive count at 255
the prose: 1980-1982 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt A2 (conceding Astra's ifile_01 finding); less its console-overrun clause, which grok/grok_irule_c.txt 1 (conceding in part the agy seat's flag) rules is `qhx11fifo`'s]

#### `qhx11fifo` (MED, an id for an entry this file already carries in prose) -- console FIFO overrun collides the queue when head meets tail
the prose: 2111-2132 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qhmipsps` (MED, an id for an entry this file already carries in prose) -- MIPS V and MIPS64 paired-single arithmetic is admitted and unimplemented
the prose: 2257-2275 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qhlancestp` (MED, an id for an entry this file already carries in prose) -- LANCE sets STP from a middle bit it just cleared
the prose: 2298-2306 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qhfcsrflags` (MED, an id for an entry this file already carries in prose) -- MIPS FCSR Cause and Flag V/Z/O/U/I maintenance and enabled-exception delivery remain missing, including CTC1 cause writes, and the work stays R4000-gated so R3000 FCSR behavior is unchanged
the prose: 2495-2498 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt A8 (conceding Astra's ifile_01 finding)]

#### `qhmipsfastpriv` (MED, an id for an entry this file already carries in prose) -- RFE leaves privilege-untagged dyntrans fast maps in place
the prose: 2628-2635 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qhshfpexcept` (MED, an id for an entry this file already carries in prose) -- SH FPU cause flags and traps are missing, including denormal-input errors and enabled division-by-zero, while DN clear delivers denormalized results and ftrc must not be patched alone
the prose: 1961-1964 and 2946-2948 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt C7 (conceding Astra's ifile_01 finding)]

#### `qharmarchlevel` (MED, an id for an entry this file already carries in prose) -- ARM CPU table has no architecture level, so version gates cannot be applied
the prose: 3022-3040 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `qhshsqat` (MED, an id for an entry this file already carries in prose) -- SQMD check is nested under AT and missing on store-queue fill
the prose: 3042-3063 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `shblreset` (MED, an id for an entry this file already carries in prose) -- BL already set stores EXPEVT_RESET_POWER instead of EXPEVT_RESET_MANUAL
the prose: 8145 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `shuseraddr` (MED, an id for an entry this file already carries in prose) -- user access to P1/P2, the reserved hole, and P4 raises a TLB miss
the prose: 8146 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `shfcnvsdfpul` (MED, an id for an entry this file already carries in prose) -- FCNVSD writes FPUL, which the instruction only reads
the prose: 8147 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `shwcrreset` (MED, an id for an entry this file already carries in prose) -- WCR3 resets to 0x77777777 instead of H'07777777
the prose: 8149 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `shtcrunf` (MED, an id for an entry this file already carries in prose) -- a TCR write can set UNF, which the manual says a write of 1 must leave unchanged
the prose: 8150 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `shbcr3mask` (MED, an id for an entry this file already carries in prose) -- BCR3 stores reserved bits 12:1 and the width probe expects them back
the prose: 8185 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `shrcr1af` (MED, an id for an entry this file already carries in prose) -- RCR1 stores a written 1 in AF, and V17/V18 expect that readback
the prose: 8186-8187 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [the governing line's quoted title (grok)]

#### `shrtcsrkey` (MED, an id for an entry this file already carries in prose) -- RTCSR and RTCOR accept unkeyed writes, the probes still require that unkeyed result, and the stale claim that no SH-4 document exists remains.
the prose: 8187-8190 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_ititles.txt]

#### `pcc2rxiackwrite` (MED, an id for an entry this file already carries in prose) -- Both queue passages record one defect: a guest write of SCCRXIACK acknowledges the RX interrupt without a direction check, and TX or modem acknowledge work leaves that write unchanged
the prose: 15038-15040; 15525-15530 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt A6 (conceding Astra's ifile_01 finding)]

#### `armcpabsent` (MED, an id for an entry this file already carries in prose) -- MRC or MCR to an uninstalled ARM coprocessor fatals and falls through, with Undefined Instruction delivery still commented out; CDP already delivers Undefined Instruction
the prose: 18709-18713 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt A10 (conceding Astra's ifile_01 finding)]

#### `heartirqdelivery` (MED, an id for an entry this file already carries in prose) -- IP30 HEART timer and ISR interrupts are not delivered and the Octane machine wiring is still the unimplemented interrupt TODO, separate from the repaired host-abort fix
the prose: 20873-20878 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_a.txt B3 (conceding Astra's ifile_01 finding)]

#### `ppcenabldeliv` (MED, an id for an entry this file already carries in prose) -- FPSCR enable bits set FEX and never deliver a program exception
the prose: 1685-1697 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_b.txt F2 (a remainder Astra's ifile_02 found unfiled)]

#### `armv6cachefmt` (MED, an id for an entry this file already carries in prose) -- ARMv6 cache-type register format is not the v4/v5 layout hardcoded for every CPU
the prose: 2097-2109; 1977-1979 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_b.txt F7 (a remainder Astra's ifile_02 found unfiled)]

#### `qharmvsixunal` (MED, an id for an entry this file already carries in prose) -- ARMv6 U=1 word loads still mask and rotate; ARM_CONTROL_U is undefined
the prose: 3617-3618 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_b.txt F10 (a remainder Astra's ifile_02 found unfiled)]

#### `armsa1110areset` (MED, an id for an entry this file already carries in prose) -- ARM reset ORs ARM_CONTROL_ALIGN, contradicting the SA-1110 reset state
the prose: 4139-4145 (line numbers of this file as of commit `db8b1a33`) -- `regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`  [grok/grok_irule_b.txt F11 (a remainder Astra's ifile_02 found unfiled)]

#### `closeassessrows` (MED, a CLASS row: a records defect of the LEDGER, found while checking which rows carry this file's prose) -- the 2026-08-27 sweep closed CLOSE (assess) rows that still name undone work, and each member needs a re-open decision
**What it is.**  On 2026-08-27 one sweep closed ledger rows that carried the adjudicator's note `CLOSE (assess)` -- "on the adjudicator's recorded authority", with "no independent re-verification of the underlying defect" (each row's own `state_note`).  That note signs off a row's ASSESS STAGE: seven rows carry it while held or in work.  For the 8 members below the grok seat found the work the row names NOT done and carried by no other row.  **Nothing is re-opened by this row or by `#555`**: whether each member is re-opened, re-filed or closed with a commit is this row's work, one decision per member.  Each member's ledger row carries a note saying so.

**Members (8):** `m8latch`, `gcsections`, `ns16550`, `pcchalt`, `wdcstandby`, `rtcnarrow`, `scunbacked`, `m437multi`.

**Read by no seat (2):** `ledgerwitness`, `cmtattr` -- closed by the same sweep with no commit; they belong to this row's audit.

**The ruling seat's evidence, in its words** (`regress/artifacts/idless_20261002/grok/grok_grok_irule_d.txt`; the `ledger.json` line numbers are those of commit `1202d342`): `CLOSE (assess)` signs off the assess stage. The seven rows whose notes continue past it are still live: `i8253zero` held (`ledger.json:9278`), `idesync` in work (`:12953`), `wdcflood` in work (`:13498`), `landiskdisk` in work (`:13993`), `rtcflood` held (`:15096`), `floodclass` held (`:15480`), `isaorder` held (`:16315`). The sweep's own text, `ledger.json:10393`, closed the bare note and performed no re-check. Eleven is too many. Checked and still undone, with no later carrier: `m8latch` (`dev_m8820x.c:90-97`), `gcsections` (`gate_offline.sh:729`, `:820`), `ns16550` (`dev_ns16550.c:181`), `pcchalt` (no `regress/ppc*.py` page-crossing probe; halt comment only at `cpu_ppc_instr_loadstore.c:63-84`), `wdcstandby` (`WDCC_STANDBY_IMMED` is `0xe0` at `wdcreg.h:138` and still hits `default:` with `WDCE_ABRT` at `dev_wdc.c:1155-1156`), `rtcnarrow` (`dev_vr41xx.c:606` integer-divides `RTCL1_L_HZ / idata` and `:614` ignores the high half; `ledger.json:15084` says the core floor is the wrong fix site), `scunbacked` (`gate_offline.sh:2346-2349` still greps bare `@@SELFCHECK@@` while `diff_rtc_range.c:140` names that token in a comment), `m437multi` (`diskimage.c:1291-1292` still writes only the last overlay, and `:2395-2412` fails the sync if any overlay fsync fails). Checked and left out: `m8sarseq` is carried by open `m8sarrows` (`ledger.json:25702-25704`); `xfamscope`'s two edits are in `gate_crossfamily.sh:173-193` and `:207-218`; `m437rtmp` owes no code, and its scope statement is `OUTSTANDING_BUGS.md:5806-5810` with the `R:` unlink at `diskimage.c:177-182`. One carrier, and this ruling does not re-open the closed rows. Passages 1-3 point here. Passage 4 does not.

**The passages of this file that point here:** 6082-6086; 6097-6099; 6101-6140; 5607-5615 (line numbers as of commit `db8b1a33`).  [grok/grok_grok_irule_d.txt 5 (conceding in part; Astra's ifile_04 raised it)]


### LOW -- 94 rows, under one class row

#### `idlesslow` (LOW, a CLASS row) -- the 94 LOW rows of the id-less review, one line each; a row is promoted to its own ledger row when a round takes it up
`regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`; the table with each row's source: `regress/artifacts/idless_20261002/IDLESS_TABLE2.tsv`.

* `qharmwbdebt` -- Owed record correction of the stale general-load coverage claims, cross-referencing qharmgenstore for the cold general-store row and qharmpathaudit for the measured inventory re-audit (lines 1518-1521 at `db8b1a33`)
* `qharmmultiorder` -- One order-blind ARM multi emitter, latent behind the little-endian install gate; a future big-endian path must emit endian variants and swap the memcpy fold's raw publishes in that same change (lines 1522-1525 and 4580-4591 at `db8b1a33`)
* `qhmutcrashscore` -- selftest_mutation.sh treats a mutant that crashes, times out, or prints nothing as detected, because it ignores the exit status and counts DIFF_PASS (lines 1529-1531 (task #55 only) and 4621-4628 at `db8b1a33`)
* `qharmpcmeasure` -- ARM PC 0xfffff000 case is still unmeasured (lines 1794-1805 at `db8b1a33`)
* `qhshapprox` -- fsca and fsrra rounding choice is still marked unsourced (lines 1974-1976 at `db8b1a33`)
* `qhdiagrest` -- Unlatched ASC diagnostics remain owed, and the repaired DEBUG-gated FDC diagnostics leave this debt. (lines 2319-2342 at `db8b1a33`)
* `qhvgasizestate` -- VGA updates its cached framebuffer size even when resize is rejected (lines 2392-2421 at `db8b1a33`)
* `qhnetxlog` -- Both queue passages record one defect: an invalid NE2000 transmit span emits an unlatched WARNING, which default INFO verbosity includes. (lines 2459-2460; 2731-2732 at `db8b1a33`)
* `qhfpguesttest` -- Owed committed-record coverage of live c.olt and c.ole remains, with the compiler prerequisite removed. (lines 2502-2504 at `db8b1a33`)
* `qhselectretry` -- d_avail retries every select error, including errors other than EINTR (lines 2554-2556 at `db8b1a33`)
* `qhrunctrlt` -- CTRL-T in the run loop is still commented out (lines 2572-2573 at `db8b1a33`)
* `qhcuepathlink` -- CUE/image open follows a symlink after the lexical .. check (lines 2724-2726 at `db8b1a33`)
* `qhatapiwitness` -- Landisk ATAPI witness remains owed; offline accounting checks exist (lines 3075-3077 at `db8b1a33`)
* `qharmmemsetdead` -- netbsd_memset arming is overwritten by the beq_etc catch-all (lines 3184-3193 at `db8b1a33`)
* `qhmemsetalias` -- latent netbsd_memset overwrites IP with the pre-subs address plus 128 (lines 3195-3200 at `db8b1a33`)
* `qhccmcrskip` -- cache-clean folds skip MCRs that cr7 currently implements as a no-op (lines 3332-3334 at `db8b1a33`)
* `qhmemreadflood` -- missing-physical-memory reads log one warning per access (lines 3338-3347 at `db8b1a33`)
* `qharmreadaudit` -- Owed coverage of ARM read-ahead on the guest path, because these probes install breakpoints and breakpoints disable read-ahead. (lines 3372-3378 at `db8b1a33`)
* `qhstrlenbilling` -- strlen probe cannot check 3n-1 billing closer than about 8K (lines 3544-3547 at `db8b1a33`)
* `qhcpycoldremeas` -- cold-source memcpy fold count is unreconciled and still queued for re-measurement (lines 3702-3707 at `db8b1a33`)
* `qhcpybailrate` -- Owed real-guest measurement of the memcpy bail rate, including silent zero-iteration bails. (lines 3741-3743 at `db8b1a33`)
* `qhcpybillmeas` -- Owed measurement of whether the -J arm and the marker arms agree on instruction billing. (lines 3743-3744 at `db8b1a33`)
* `qhcpytailcov` -- memcpy probe has no two-iteration tail row at word 16 (lines 3746-3751 at `db8b1a33`)
* `qhcpydumpdiag` -- memcpy probe treats a short dump as a bad destination word (lines 3751-3756 at `db8b1a33`)
* `qhcpysamplecov` -- memcpy probe samples five destination words and misses a 7-of-8 copy (lines 3757-3764 at `db8b1a33`)
* `qhbatchcounter` -- the guest mp counter includes the dyntrans batch quantum of 120 (lines 3801-3803 at `db8b1a33`)
* `qhstepbranch` -- Owed observation of a step onto a fold slot reached as a branch target, under the source-derived expectation of uncombined execution. (lines 3812 at `db8b1a33`)
* `qhusertlbmeas` -- Owed measurement of is_userpage across TLB eviction, recording that invalidation clears the bit. (lines 3847-3848 at `db8b1a33`)
* `qhcpycountcov` -- memcpy marker-count times 32 is unchecked against the r0 advance (lines 3885-3889; 3896-3898 at `db8b1a33`)
* `qhfireexact` -- copyin and copyout fires rows accept any positive marker count (lines 3899-3901 at `db8b1a33`)
* `qharmtucov` -- three ARM load/store translation units still have no writeback-probe row (lines 4107-4109 at `db8b1a33`)
* `qharmstorepre` -- store pre-index writeback has no probe row (lines 4114-4116 at `db8b1a33`)
* `qhwalloracles` -- Owed assessment of wall-clock measurement oracles and fixed execution windows, including halt-within-window gates, grace constants, and run_emu margins; transport timeouts stay with loadfragile (lines 4289-4294 at `db8b1a33`)
* `qharmstaleprompt` -- arm_flags_probe whole-buffer waits return on the previous prompt (lines 4308-4321 at `db8b1a33`)
* `qharmsendstatus` -- arm_flags_probe send drops the prompt-wait result (lines 4323-4326 at `db8b1a33`)
* `qharmreadretry` -- six register, print, and copyout reads still have no consumer-keyed retry (lines 4328-4339 at `db8b1a33`)
* `qharmdumptail` -- dump retry parsers take the first dump word in the slice (lines 4339-4341 at `db8b1a33`)
* `qharmretrycount` -- Report retries and unparseable reads as diagnostic telemetry; do not require zero retries (lines 4343-4347 at `db8b1a33`)
* `qharmcolorenv` -- gate_arm.sh still does not unset CLICOLOR (lines 4349-4352 at `db8b1a33`)
* `qhfpdefaultnote` -- float_emul.c still documents the withdrawn R3010/R4010 integer default (lines 4433-4443 at `db8b1a33`)
* `qharmgenstore` -- arm_writeback_probe.py lacks a cold general-store row (lines 4503-4509 at `db8b1a33`)
* `qharmgenwidth` -- arm_writeback_probe.py still lacks cold general-path rows for the byte arm, the halfword alignment mask, and register-offset forms. (lines 4510-4519 at `db8b1a33`)
* `qharmfasthstore` -- the fast store-halfword site has no probe row (lines 4560-4561 at `db8b1a33`)
* `qharmpathaudit` -- Owed measured re-audit of the ARM translation-unit inventory, correcting four missing units to three and cross-referencing qharmtucov (lines 4564-4568 at `db8b1a33`)
* `qhmipsdump` -- mips_rounding_probe accepts any dump-shaped line in the read slice (lines 4629-4638 at `db8b1a33`)
* `qhmipslong` -- arc round.l, ceil.l, and floor.l still have no row (lines 4639-4645 at `db8b1a33`)
* `qhfpucomment` -- Owed record correction of the comment that W/L stores ignore the rounding mode and that cvt.w and trunc.w are indistinguishable. (lines 4648-4651 at `db8b1a33`)
* `qhidlefoldloss` -- The m88k idle fold is lost only for loop-head tb1 at page index zero when a .n branch ends the previous page (lines 4661-4667; 4683-4686 at `db8b1a33`)
* `qhswpabort` -- swp abort prints via fatal and returns without the next_ic reset (lines 4801-4802 at `db8b1a33`)
* `qhptyfault` -- the #391 timeout detector still has no PTY-level fault injection (lines 4865-4871; 4954-4960; 4965-4966 at `db8b1a33`)
* `qhcmdresults` -- sibling probe sends still drop the wait verdict (lines 4873-4882 at `db8b1a33`)
* `qhcmdecho` -- register reads accept a bare hex line with no command echo (lines 4883-4889; 4968-4970 at `db8b1a33`)
* `qhcmdabort` -- A stalled pc=, step, or print is still unacted, so its late output shifts the next bare-hex read into the following register (lines 4839-4848 and 4953-4954 at `db8b1a33`)
* `qhcmdreaderr` -- EOF and read errors are reported as timeouts (lines 4955-4956 at `db8b1a33`)
* `qhcmdclock` -- probe deadlines use time.time (lines 4956-4957 at `db8b1a33`)
* `qhctrlcwait` -- post-control-C wait_from results are discarded (lines 4967-4968 at `db8b1a33`)
* `qhdhighseed` -- High-bit LDRD rows already exist, and the owed work is their mutation and sanitizer verification. (lines 5113-5121; 5140 at `db8b1a33`)
* `qhdwarmrows` -- a warm STRD page has no row, so the fast-path chicken-out has no detector (lines 5122-5126; 5140 at `db8b1a33`)
* `qhdaddrrows` -- LDRD and STRD register-offset and writeback rows remain owed, together with the STRD write-extent sentinel. (lines 5140-5141 at `db8b1a33`)
* `qhmipscensus` -- Complete and record the deferred Phase-C MIPS fold census (lines 5193-5197 at `db8b1a33`)
* `bareflopq` -- bare floppy-sized image is typed FLOPPY and no device selects that type (lines 5201-5209 at `db8b1a33`)
* `parsecovq` -- Parser tests do not establish controller acceptance (lines 5234-5238 at `db8b1a33`)
* `gateorderq` -- Binary withdrawal and republication, and baseline-directory producer-consumer order, still serialize the regression battery. (lines 5268-5280 at `db8b1a33`)
* `idlepatq` -- The pinned luna88k instruction budget depends on recognizing specific guest idle patterns. (lines 5289-5294 at `db8b1a33`)
* `finalcountq` -- SIGINT with absent or exhausted stdin blocks in the debugger before any final instruction count, while quit exits cleanly only when a command can be read. (lines 5302-5306 at `db8b1a33`)
* `landrateq` -- landisk still has no calibrated instruction budget (lines 5321-5326 at `db8b1a33`)
* `logspliceq` -- bracketed fatal() text can splice a guest console line (lines 5337-5343 at `db8b1a33`)
* `anchorevq` -- Owed record correction: the anchored-regex result was measured on whole logs and does not describe streaming, which matches each assembled tail at a new position-zero boundary. (lines 5376-5381 at `db8b1a33`)
* `tailstepq` -- Interactive confirmations ignore held stream tails (lines 5416-5419 at `db8b1a33`)
* `landwallq` -- landisk's runaway bound is still 900 s of wall clock (lines 5421-5425 at `db8b1a33`)
* `canaryq` -- Gate 5 ordinary rig runs still lack a standing mutant control, and gate 7 synthetic progress controls stay a separate case. (lines 5496-5499 at `db8b1a33`)
* `runnamesq` -- Gate 5 writes and grades fixed filenames in a reusable log namespace and never checks a run identifier. (lines 5507-5510 at `db8b1a33`)
* `armapcovq` -- The memory differential ignores real ARM subpage permission selection, grants its 1 KiB fixture access, tests mapping splits, and names both ARM and SH as producers. (lines 5662-5665 at `db8b1a33`)
* `qhwdcempty` -- no-disk WDC commands print an unlatched debug line per command (lines 7669-7671 at `db8b1a33`)
* `shdmacmask` -- DMATCR's transfer path masks 29 bits while the register write path keeps 24 (lines 8151 at `db8b1a33`)
* `shdnrecords` -- DN=0 comments still describe an FPU error where the manual specifies a denormal result (lines 8153-8163 at `db8b1a33`)
* `shfsrracite` -- the FSRRA comment at cpu_sh_instr.c:3281 still says single-precision only (lines 8163-8165 at `db8b1a33`)
* `shszpin` -- SZ1 is not assigned to bit 7 or bit 4 by either manual and has no empirical pin (lines 8178-8181 at `db8b1a33`)
* `shregattribution` -- SH7760, CHCR_TD/CHCR_CHSET, and SH_RCR2_ENABLE comments name the wrong chip or the wrong bit (lines 8192-8197 at `db8b1a33`)
* `pclockdeadcode` -- Owed probe hygiene: sh_pclock_probe.py keeps an unused dumped helper and duplicate landisk and dreamcast code entries. (lines 8839-8841 at `db8b1a33`)
* `gdromwideval` -- a declined 32-bit GDROM_DATA read returns 0x0000ffff and no row pins it (lines 9156-9157 at `db8b1a33`)
* `gdromlatchspent` -- Owed documentation, with no code change: the GDROM width warning latch is consumed before the declined store, so a later landing narrow store stays silent. (lines 9158-9160 at `db8b1a33`)
* `gdrom88rd` -- A read of GDROM 0x88 and a write of GDROM_STAT still call fatal with no latch, and the read is the flood that was ordered filed rather than latched (lines 10370-10373 and 10678-10680 at `db8b1a33`)
* `wdcoddstubclaim` -- row_odd_bytecount still says the harness does not stub diskimage_is_a_cdrom (lines 12198-12201 at `db8b1a33`)
* `gdrommaskclaim` -- Owed correction of the GDROM comment that still promises a new warn site cannot reuse another site's bit, a promise the following sentences retract. (lines 13274-13279 at `db8b1a33`)
* `seatcopywait` -- copy preserved seat logs after the panel wait (lines 18376-18405 at `db8b1a33`)
* `panelechocheck` -- ECHO-ONLY requires both the distinctive brief line in the answer and answer-minus-brief under 800; the owed work is a harness change plus two negative controls (lines 19498-19502 at `db8b1a33`)
* `shfaultclause` -- Owed record correction, deferred to carrier review and still owed: the member-5 clause omits that a failed SH load leaves its destination unchanged. (lines 19540-19542 at `db8b1a33`)
* `qhmipstlbwarn` -- The optional write-time MIPS TLB-overlap debug warning remains compiled out and was left unimplemented; it is tooling, not a fidelity defect (lines 2597-2599 at `db8b1a33`)
* `armcpsrprint` -- A direct debugger print of cpsr can show stale NZCV because the settings read does not fold the separate execution-flags field back into CPSR (lines 16972-16975 at `db8b1a33`)
* `pcc2lineexit` -- pcctwo_interrupt_common's default still calls exit on an unsupported interrupt line, and guest reachability is unestablished (lines 13932-13934 at `db8b1a33`)
* `qhshelltimeout` -- gate scripts still bound emulator runs with the timeout command (lines 5262-5266 at `db8b1a33`)
* `qhguestasan` -- the asan sweep constructs machines under -V and never executes a guest instruction (lines 7326-7338 at `db8b1a33`)
* `gdromtailcov` -- ship cnt-post tail-reach rows for both GD-ROM rejection arms (lines 10412-10418 at `db8b1a33`)

### The passages an id carries -- 104 (lines as of `db8b1a33` -> the id or ids; a note says where the id is not an open ledger row)

* 1526-1528 -> `m88kidleslotsem`, `qhidlefoldloss` (a `#555` row above)
* 1616-1622 -> `ppcfmarn`
* 1646-1649 -> `alphatinyzero`
* 1650-1655 -> `mipstinyprerm`
* 1672-1675 -> `ppcsinglealias`
* 1685-1697 -> `ppcfprfclass`, `ppcveinhibit`, `ppcenabldeliv` (a `#555` row above)
* 1705-1716 -> `qhppcdecode` (a `#555` row above)
* 1774-1777 -> `qhmipsps` (a `#555` row above)
* 1778-1779 -> `shoddprfield`
* 1931-1936 -> `sh4sqexpevt` (named in this file only: no ledger row of its own), `sh4sqwrite`, `qhshsqat` (a `#555` row above)
* 1940-1958 -> `sh4utlbmultihit`, `sh4sqexpevt` (named in this file only: no ledger row of its own), `sh4sqwrite`, `qhshsqat` (a `#555` row above)
* 1965-1970 -> `qhfcsrflags` (a `#555` row above)
* 1971-1973 -> `optinyband`
* 1977-1979 -> `armcachegeom`, `armv6cachefmt` (a `#555` row above)
* 1980-1982 -> `qhx11fifo` (a `#555` row above; in part: the console-overrun clause)
* 1983-1986 -> `qhlancestp` (a `#555` row above), `qhdiagrest` (a `#555` row above), `qhvgasizestate` (a `#555` row above)
* 1987-1988 -> `OB-22` (named in this file only: no ledger row of its own)
* 2038-2049 -> `qhfcsrflags` (a `#555` row above)
* 2086-2088 -> `qhscifssr` (a `#555` row above)
* 2097-2109 -> `armcachegeom`, `armv6cachefmt` (a `#555` row above)
* 2291-2297 -> `qhfcsrflags` (a `#555` row above)
* 2307-2318 -> `qhx11fifo` (a `#555` row above)
* 2453-2455 -> `arcpartlba` (named in this file only: no ledger row of its own)
* 2456-2459 -> `OB-22` (named in this file only: no ledger row of its own)
* 2597-2599 -> `qhfcsrflags` (a `#555` row above), `qhmipstlbwarn` (a `#555` row above)
* 2614-2615 -> `armthumbabortkill` (in part: the Thumb half only)
* 2616 -> `m88kexit` (ledger: held)
* 2636-2638 -> `mipsreadpriv`
* 2685-2689 -> `exitunowned76`
* 2721-2723 -> `pvrrenderexit`
* 2727-2728 -> `ramspaninval`
* 2730 -> `jazzlbmask`, `OB-22` (named in this file only: no ledger row of its own)
* 2730-2731 -> `arcpartlba` (named in this file only: no ledger row of its own)
* 2731 -> `tcpdebugopts`
* 3004-3005 -> `armcachecleanload`
* 3042-3063 -> `sh4sqexpevt` (named in this file only: no ledger row of its own; in part: the PREF exception kind)
* 3200-3202 -> `armbdtcombined`
* 3227-3233 -> `armcachecleanload`
* 3326-3331 -> `armcachecleanload`
* 3401-3408 -> `armbdtcombined`
* 3409-3413 -> `armmemcpyoverlap`
* 3500-3508 -> `qharmmemsetdead` (a `#555` row above), `qhmemsetalias` (a `#555` row above)
* 3617-3618 -> `qharmvsixunal` (a `#555` row above)
* 3740 -> `qhusertlbmeas` (a `#555` row above)
* 3903-3905 -> `qharmmemsetdead` (a `#555` row above)
* 4139-4145 -> `armalignexc`, `armsa1110areset` (a `#555` row above)
* 4251-4287 -> `lunabackhard` (named in this file only: no ledger row of its own)
* 4676-4682 -> `m88kidleslotsem`
* 4745-4746 -> `qhcpycoldremeas` (a `#555` row above)
* 4802-4803 -> `OB-24` (named in this file only: no ledger row of its own)
* 4966-4967 -> `qharmstaleprompt` (a `#555` row above), `qhctrlcwait` (a `#555` row above)
* 5046-5047 -> `armoddpair`
* 5085-5097 -> `armoddpair`
* 5142 -> `armdwordalign` (in whole)
* 5142-5143 -> `armoddpair`
* 5215-5223 -> `b126` (ledger: held)
* 5225-5232 -> `b126` (ledger: held)
* 5262-5266 -> `loadfragile` (ledger: in work; in part: the 5262-5266 transport sweep only), `qhshelltimeout` (a `#555` row above)
* 5310-5319 -> `loadfragile` (ledger: in work)
* 5405-5409 -> `strad` (ledger: held)
* 5492-5495 -> `batterymissedruns`
* 5500-5503 -> `census` (ledger: closed)
* 5504-5506 -> `auditmap` (ledger: held)
* 5563-5573 -> `capgap` (ledger: dropped)
* 5575-5580 -> `capN` (ledger: dropped)
* 5582-5585 -> `cflood` (ledger: dropped)
* 5587-5605 -> `sigunsafe` (ledger: dropped)
* 5678-5682 -> `mrwstore2` (ledger: held)
* 5686-5691 -> `mrwgrind` (ledger: dropped)
* 5692-5697 -> `mrwstore2` (ledger: held)
* 5701-5709 -> `optrow` (ledger: held)
* 5868-5881 -> `fbsdrampair`
* 5894-5898 -> `fbmode` (ledger: held)
* 5899-5902 -> `fbmode` (ledger: held)
* 5903-5907 -> `fbmode` (ledger: held)
* 5908-5911 -> `fbmode` (ledger: held)
* 5913-5920 -> `i8253zero` (ledger: held)
* 6082-6086 -> `m8latch` (ledger: closed; the row the passage names; it does not carry the open work), `closeassessrows` (a `#555` row above; the open work)
* 6095-6096 -> `m8snprintf` (ledger: dropped), `m8latch` (ledger: closed)
* 6097-6099 -> `gcsections` (ledger: closed; the row the passage names; it does not carry the open work), `closeassessrows` (a `#555` row above; the open work)
* 6101-6140 -> `ns16550` (ledger: closed; the row the passage names; it does not carry the open work), `closeassessrows` (a `#555` row above; the open work)
* 6804-6805 -> `pit8253bcdbinary`
* 6806-6809 -> `pitcount` (ledger: held)
* 6823-6826 -> `changelogroundgap`
* 7326-7338 -> `qhguestasan` (a `#555` row above)
* 8144 -> `sh4prio0` (ledger: closed)
* 8678-8690 -> `sh4iprunpinned`
* 8691-8694 -> `shdmteupper` (named in this file only: no ledger row of its own)
* 9063-9067 -> `gdrompiooddlen`
* 9148-9152 -> `hlen` (ledger: held)
* 10258-10261 -> `asicpermute`
* 10412-10418 -> `gdrompionull` (ledger: closed; the row the passage names; it does not carry the open work), `gdromtailcov` (a `#555` row above; the open work)
* 13612-13617 -> `outcomegap`
* 14302-14306 -> `gxprobepccache`
* 16630-16633 -> `printedvariants`
* 16756-16763 -> `armuserpageshift` (named in this file only: no ledger row of its own)
* 16972-16975 -> `armcpsrprint` (a `#555` row above)
* 16997-17000 -> `xscalecp6exits`, `armendianexit`
* 17093-17096 -> `m88ktrapmask` (named in this file only: no ledger row of its own)
* 17097-17102 -> `mipsextshift`
* 17979-17980 -> `guardfailsopen`
* 19984-19987 -> `pit8253bcdbinary`
* 20735-20738 -> `adjudglmtag`
* 20873-20878 -> `heartirqdelivery` (a `#555` row above)

### The entries that stay UNSETTLED -- 4 (lines as of `db8b1a33`; what is unsettled, in the ruling seat's words)

* 2947-2948 -- whether the SH-4 FSCA store owes the mode-aware rounding store. The handler stores through ieee_store_float_value. The manual was not opened.  READ SINCE (grok, 2026-10-02, the manuals in the project root's `_scratchpad/`): The SH-4 Programming Manual Rev. 5.0 and the SH7750 Group Hardware Manual Rev. 7.00 do not define FSCA, so they do not say how its two results are rounded or whether FPSCR.RM applies. The FIPR/FTRV approximation text does not transfer. Settling the store needs an SH-4A Software Manual, which is not among these extracts.  [the governing line (grok); idlessread_20261002/grok/grok_grok_iunsettled.txt 1 (an entry the table had as UNSETTLED; grok read the local manuals)]
* 5296-5300 -- a sample of upstream's hot locations or call stacks during the luna88k spin. Another liveness or instruction-rate measurement repeats 5296-5300.  [grok/grok_irule_b.txt U2]
* 5650-5654 -- `cpu_ppc_instr.c` `lvx`/`stvx` and a PowerPC manual were not opened; the queue itself says the mask rule is uncitable. Not raised to MED.  READ SINCE (grok, 2026-10-02, the manuals in the project root's `_scratchpad/`): Books I-III and both PEMs do not define lvx or stvx. The 16-byte EA mask stays uncitable until the AltiVec Technology Programming Environments Manual, named at ppc_pem_32and64_2005.txt:358 and :6252, is read. That manual is not here.  [the governing line (grok); idlessread_20261002/grok/grok_grok_iunsettled.txt 2 (an entry the table had as UNSETTLED; grok read the local manuals)]
* 6798-6803 -- a count write (`dev_8253.c:176-186`) does not clear `latched[]`; clears are on read (`:261`) and on a control word (`:311`). `_scratchpad/i8254.txt:334` says the latch holds "until it is read … or until the Counter is reprogrammed" and does not say a bare count write is a reprogram.  [the governing line (grok)]
