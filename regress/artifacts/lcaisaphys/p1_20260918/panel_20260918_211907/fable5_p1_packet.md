# `#540` (lcaisaphys) PASS 1 -- CONSOLIDATED FINDINGS for the fable5 seat (LAST seat; everyone else has answered)

**Tree:** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` at HEAD `cdbe7d7`.  `dev_lca.c`, `memory_rw.c` and
`memory_alpha.c` are byte-identical to `e0be9b2`, the commit the brief named.  **Use absolute paths.**
`C:\DocumentNoSnc\CC\GXEMUL\src\` is a pristine 2021 upstream copy, and its line numbers differ by hundreds.

**The brief:** `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\panel_20260918_211907\brief_sent.md`.
**Every seat answer is in that directory:**

    codex.txt           GPT-6 Astra max, panel seat. The answer is the LAST `VERDICT:` block (the file streams reasoning first).
    codex_adv540p1.txt  GPT-6 Astra max, the dedicated adversarial job (equivalence, premise audit, cell map).
                        Its brief: _scratchpad/cx540p1_adv_brief.md
    kimi.txt            the kimi CLI (file-reading). Its answer is the last `VERDICT:` block.
    grok.txt, agy.txt   file-reading.
    ollama_{glm,deepseek,minimax,kimi}.txt   packet-fed.
    opus5_p1.md         the Opus 5 Agent seat (compile-and-measure seat, read-only this pass).

## VERDICTS

All eight scriptable seats, the dedicated job and the Opus seat ruled GO or GO-WITH-CHANGES on the fix itself.  Opus's
identity was verified (claude-opus-5[1m], CHECKPOINT quoted).  Its answer is the richest of the ten, and F14-F20 below
come from it.

    GO               agy, glm, minimax, kimi-k3 (sub), grok, kimi CLI
    GO-WITH-CHANGES  deepseek (witness wording), codex (claim wording), codex_adv (detector coverage),
                     opus5 (detector + scorer + witness hygiene; severity MED as witnessed)

## THE FINDINGS, NUMBERED, EACH WITH MY DISPOSITION

**F1. The fix.**  Add `| PHYSICAL` to both nested forwards and keep `CACHE_NONE`.  Unanimous.  **ACCEPT.**

**F2. "The forward works ONLY while ptbr == 0" is FALSE.**  Raised by codex, kimi-k3, grok and the kimi CLI.  With a
nonzero ptbr the inner VA is walked through the GUEST's tables.  `0x1d00003fd` uses L1 index 0, which is the
low-memory slot, and a real OS has that slot valid.  So the walk either misses deeper (the kimi CLI names the extra
unlatched `TODO: pte2 not valid.` line) or, if the guest maps that VA, it silently MISROUTES the ISA access into
whatever was mapped there.  **ACCEPT.**  The fix comment and the records will say "translated through the guest's page
tables: a miss answers a false zero or drops the store; a hit misroutes it".  The witness measures only the miss case,
and says so.

**F3. K0SEG is a masked direct mapping, not numeric VA == PA, and the ptbr == 0 arm carries special remaps.**  Raised
by codex and codex_adv (P2 FALSE as written).  **ACCEPT, as wording.**  The witness's addresses are unaffected.

**F4. Severity.**
- HIGH: agy, grok, minimax and the kimi CLI.  kimi-k3 and glm call HIGH defensible; deepseek calls it plausibly HIGH.
- MED, provisionally: codex, because universal failure and the flood's host impact are unmeasured.

**MY DISPOSITION: HIGH.**  The measured case is enough: the whole sparse ISA window dies for any guest whose tables
miss that VA.  That window carries the console UART, 8042, PIC, PIT and CMOS, and each access prints two unlatched lines
(the translator miss, plus memory_rw's "writing to device ... failed" on writes, per the kimi CLI).  The misroute case
is worse.  HIGH does not need the failure to be universal.

**F5. The score of candidate (c), `NO_EXCEPTIONS | PHYSICAL`, is disputed.**
- grok says 11/13: the miss rows go green, the data rows stay red.
- agy, codex, codex_adv, the kimi CLI, kimi-k3 and deepseek say `CONTROL=DEAD, RESULT=0/0`.  The pre-arm `live` row is
  itself a sparse access through the same forwarder, so the 8042 handler is skipped and the reply reads zero.

**MY DISPOSITION: CONTROL=DEAD.**  grok's table never considers row 2.  It gets MEASURED in the kill table
regardless.  Either outcome kills (c).

**F6. DETECTOR GAPS.**  codex_adv found these independently; I had drafted the same two before its answer landed.
- **(f)** `PHYSICAL` only for ports >= 0x200 survives all 13 rows.  Every armed row uses a UART port, and the low
  ports (8042, PIC, PIT, CMOS) are exercised only before the arm.
- **LANES.**  Every witness access is `LDBU`/`STB`, and `ofs = (relative_addr & 3) % len` is 0 for every len-1 access.
  So the armed cells {read, write} x {len > 1 at ofs 0, ofs 1, ofs 2, ofs 3} are all NO ROW.  A variant applying
  `PHYSICAL` only at `ofs == 0` escapes the witness entirely.

**MY DISPOSITION: ADD ROWS before the first table (L1, since the witness is unshipped).**
- one post-arm 8042 self-test;
- wide stores and loads at lanes 0-3 on **COM2** registers with readback: MCR `0x2fc` (lane 0), IER `0x2f9` (lane 1),
  MSR `0x2fe` (lane 2; reads back `| 0xb0`) and SCR `0x2ff` (lane 3).  COM2 keeps every new miss string off
  `0x1d00003fd`/`0x1d00003ff`, which `r miss` and `w miss` own.  The width is `LDL`/`STL`, per F15;
- each write observed through FLAT, each read planted through FLAT.  Every new row must be RED on the committed build.

**F7. Candidate (g): the read arm returns the inner status instead of 1.**  NO ROW, and no seat could name a concrete
failing port.  With `PHYSICAL` the inner call cannot fail by translation.  **DOCUMENTED ONLY, NOT FILED.**  It is a
design dissent that names no measurable consequence.

**F8. An unnamed option: OR the inner address into K0SEG and still omit `PHYSICAL`.**  Named by grok, kimi-k3, glm and
the kimi CLI.  It passes the witness, because the witness runs in kernel mode.  A user-mode outer access would walk
again.  **REJECT as a fix.  As a MUTANT it escapes, and user mode is CPU state the body never tests, so I would
DISCLOSE it under clause (e) rather than row it.**

**F9. Bare `PHYSICAL` is EQUIVALENT here but not in general.**  agy, codex, codex_adv, grok and the kimi CLI each
enumerated every read of `cache`.  `CACHE_DATA` is 0, so on a RAM path a read would invalidate code translations.
**ACCEPT.**  Keep `CACHE_NONE`, and build `M_d` in the kill table as a predicted-equivalent MEASUREMENT.

**F10. Witness note narrowing (codex).**
- An absent `pte2 todo` does not by itself prove an L1 stop, since unbacked table levels also reach `not_found`
  silently.
- "vehicle never armed" should read "setup not validated".
- `flat lsr` checks only the `0x60` bits.
- `alive` is PTY-observed, not an exit status.

**ACCEPT all four as note corrections, pre-ship.**

**F11. The write-side flood has a second line**, memory_rw's device-failure message (kimi CLI).  **ACCEPT.**  It goes
into the records.

**F12. `dev_ether.c:188` is not a sibling.**  It forwards a guest-supplied pointer, where this defect forwards a
host-constructed physical address.  My complement census reproduces this: 59 real calls, of which 56 pass `PHYSICAL`,
two are this defect, and one is ether.  **NOT FILED.**

**F13. The §1 commit pin is stale** (HEAD is `cdbe7d7`), and the reviewed path is identical.  **ACCEPT.**


## THE OPUS SEAT'S FINDINGS (it landed last before you; read `opus5_p1.md` for the derivations)

**F14.  THE SCORER TRAP.**  `CONTROL=DEAD` prints `RESULT=0/0` and exits 2.  A kill-table scorer that tests `N == M`
reports that as an ESCAPE, both for (c) and for every host-death mutant, and host death is the class this fork cares
about most.  **MY DISPOSITION: ACCEPT.**  The #540 driver scores ESCAPED only on exit 0 AND `RESULT=N/N`.  Anything
else is KILLED, with the red rows or the dead control named.  I do not adopt Opus's structural alternative, which
would gate only on rows 4-7 plus `flat lsr` and score `live` as an ordinary row.  My reason: the driver rule already
closes the hole without restructuring the witness's gate.  **Challenge that if you think the structural form is owed.**

**F15.  (e') AND (f) BOTH ESCAPE, INDEPENDENTLY CONFIRMED.**  These are the same gaps as F6.  Opus adds a point that
changes the row design: **the 21066 is EV4 and has no BWX.**  A real 21066 driver reaches sparse space with
`ldl`/`stl`.  The witness proves reachability only through `LDBU`/`STB`, which the modelled CPU lacks, even though
the emulator decodes them.  **MY DISPOSITION: ACCEPT.**  The lane rows will use `LDL`/`STL` (len 4, so `ofs =
port & 3`) instead of the `LDQ`/`STQ` in my draft.

**F16.  THE RULE QUESTION HAS A DISSENT, and it comes from Opus.**  In its words: *"The fix adds a flag, not a
predicate.  Inside DEVICE_ACCESS(lca_isa), the predicates dominating the two edited calls are `len == 0` and
`writeflag == MEM_WRITE`.  lca_isa has no device state.  So the floor cells are {read, write} x {len > 0}, and both
are rowed ... (e'), (f) and (g) are clause-(e) coverage debt.  The body never tests port ranges; it tests `len` only
against 0; and `ofs` is off the repair path."*  My reading of your #530 ruling (LANE is a floor axis for this handler)
points the other way.  **Both of us agree the rows get added**: they are cheap and licensed by their kills.  So the
question is about the RECORD and about future rounds: are the lane cells floor or debt?

**F17.  SEVERITY: MED as witnessed, HIGH only with a HIT-CASE witness (Opus).**  The hit case has the inner VA mapped
by a real 3-level table, so a pre-fix sparse read returns the planted page's byte and a pre-fix write lands in guest
memory: a user-to-kernel influence channel.  Opus sketched it at three `put d` PTEs, and it would give the value
channel a positive pre-fix signature.  **MY DISPOSITION: undecided; this is Q3.**  If you rule HIGH, I build the hit
case as a second session of the same probe.

**F18.  WITNESS HYGIENE (Opus).**  Four items:
- Step D's SCR baseline is 0, the same value a failed read zero-fills, so `w lands` = 0 cannot tell "store abandoned"
  from "observer failed".  Use 0xa5.
- `pte2 todo` does not check `TODO: pte3`.
- `live` also proves the pre-arm WRITE arm; its note undersells it.
- The shipped probe differs from the frozen measured copy by a docstring edit made 16 s after the run.  Hash the probe
  that ships.

**ACCEPT all four.**

**F19.  E1, A SIBLING CLASS OUTSIDE DEVICES (Opus).**  Alpha PAL swpctx and wrfen access the PCB through
`store_64bit_word`/`load_64bit_word`, which call `memory_rw` with no `PHYSICAL`.  The architectural PCBB is physical.
At a later swpctx with paging on, the save walks and is abandoned on a miss, and the nine loads return zeros: **ptbr
silently becomes 0 and identity mode returns.**  I verified the call sites by reading (`cpu_alpha_palcode.c`:222 and
:231-248).  Not witnessed.  **MY DISPOSITION: FILE as its own row.**  It is not a device, and it is not this round.

**F20.  E2, A RESIDUAL THE FIX INTRODUCES, plus a general hypothesis (Opus).**  I verified by reading that
`memory_rw.c:738-750` calls `update_translation_table(cpu, vaddr & ~offset_mask, memblock, ...)` on the RAM path
without a PHYSICAL guard, and under `PHYSICAL` vaddr == paddr.
- **For #540**, this matters only with `-M` >= 7425 MB, where a device-less ISA port lands in RAM.
  **MY DISPOSITION: DISCLOSE it in the contract.**
- **The general form** is any PHYSICAL (and not NO_EXCEPTIONS) access that reaches RAM installing a VA==PA
  translation over the guest's own mapping.  That covers 18 device calls, and dev_sgi_mec, dev_dreamcast_gdrom and
  dev_ram look RAM-bound.  **MY DISPOSITION: FILE it as a HYPOTHESIS row**, unwitnessed.  Its reachability per device
  is unestablished.

(Opus's E4 is the known `alphavmkill` row, already queued next.  E3, `-M` >= 6145 overlapping the IOC, and E5, the
non-architectural K0SEG decode, are pre-existing and out of scope.  I record them and do not file them.)

## QUESTIONS FOR YOU, and they are the reason you are last

**Q1 -- GO / NO-GO on the fix as proposed (F1).**

**Q2 -- THE RULE QUESTION, which I will not decide alone.**  On #530 you ruled LANE a FLOOR axis for THIS handler:
`data[ofs]` distinguishes all four lanes, and `vc` serviced wide writes at the rowed lane alone.  #540's fix adds a
FLAG, not a predicate, and `lca_isa` holds no device state.  Read literally, the pass-11 FLOOR ("the guard's
dominating predicates x the device-STATE lvalues the repair path reads") gives only {read, write}, which the witness
already covers.  The JOINT-CELLS enumeration ("partitions the body's own code distinguishes") gives direction x lane.
**Are F6's lane cells OWED (floor) or DISCLOSED (clause-(e) debt)?**  I lean OWED, for consistency with your #530
ruling, and because the rows are cheap: one armed session.  Tell me if that is the wrong reason.

**Q3 -- Severity (F4): HIGH or MED?**

**Q4 -- WHICH OF MY TWENTY DISPOSITIONS IS WRONG?**  I accepted or rejected every finding above.  A round that
accepted almost everything has either had a very good panel or stopped arguing.  Be hardest on F5, F7, F8 and F14, where I
overruled or narrowed a seat, and on F16, where a seat dissents from the reading of YOUR OWN ruling.

**IDENTITY -- the first three lines of your answer:**

    FABLE_SEAT_ALIVE_20260918_540P1
    <your exact model id> | <the first line of C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md, verbatim>
    VERDICT: GO | GO-WITH-CHANGES | NO-GO -- <one line>

**READ-ONLY.**  Another session starts a long gate with wall-clock oracles right after you finish.  Run no builds and
no emulator, and write nothing except your answer file, `fable5_p1.md`, in the panel directory above.
