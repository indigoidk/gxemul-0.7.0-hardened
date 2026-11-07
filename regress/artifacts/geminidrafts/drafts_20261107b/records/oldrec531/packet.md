# Reading task: oldrec531 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC531-00f8` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #531 ip30abortkill (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 7160-7898 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 7160| # `#531` (ip30abortkill): four guest-reachable `abort()` calls in `dev_sgi_ip30.c` — a guest LOAD zeroed the interrupt-status register and then killed the host
 7161| 
 7162| **`-E sgi -e ip30` is an advertised machine, and three `exit(` sweeps of this queue walked past
 7163| every one of these sites** — because `abort()` contains no `exit(`. That is the finding worth
 7164| carrying: a census keyed on `exit(` cannot see a host death spelled `abort()`.
 7165| 
 7166| ## WITNESS — rung 3, on unmodified `-E sgi -e ip30`
 7167| 
 7168| `regress/artifacts/ip30abortkill/ip30_abort_probe.py`, one fresh process per SESSION -- most
 7169| sessions score one row, but `tick 50`/`tick 50 txt` and `xbit isr`/`xbit tick` each score two
 7170| rows from one process, by design (the cross-bit mutant needs both announce classes in one device
 7171| lifetime) [#561], real
 7172| guest instructions through real decode and real `memory_rw` (never `dump` — all four ip30
 7173| registrations are `DM_DEFAULT`, so `dump` bypasses the handler and would prove nothing).
 7174| 
 7175|     PRE-FIX   PREFIX_21row_20260917.out            IP30ABORT_RESULT=8/21   13 defect rows red
 7176|     POST-FIX  probe_FIX531_21row_20260917.out      IP30ABORT_RESULT=21/21    0 red
 7177| 
 7178| **ONE INSTRUMENT, BOTH BUILDS.** The instrument grew from 18 rows to 21 during pass 2 (three
 7179| repairs and two new floor rows -- see the pass-2 section), so BOTH figures above were re-measured
 7180| on the 21-row form rather than carried forward. *The 18-row pair (11/18 and 18/18) is SUPERSEDED,
 7181| not merely stale: a comparison run owes ONE instrument, and citing a pre-fix number from one
 7182| instrument beside a post-fix number from another is the shape this project's own records rule
 7183| exists to refuse.* The 18-row form is frozen at `ip30_abort_probe.18row_20260917.frozen.py`.
 7184| 
 7185| **Both controls green throughout**: `live` returns `0x11223344` through the same decode
 7186| (liveness), and the accept rows are serviced (device signature). **The discriminating pair is
 7187| `tick 49` ALIVE against `tick 50` DEAD** — it is bit 50 specifically, not the tick path.
 7188| 
 7189| > ### *** THAT SENTENCE IS TRUE PRE-FIX AND FALSE OF THE SHIPPED BUILD, AND THE FIX ITSELF IS
 7190| > ### WHAT MADE IT FALSE.  Caught by the pass-2 codex seat and, independently and from the
 7191| > ### opposite direction, by minimax. ***
 7192| >
 7193| > After de-fatalisation **both rows read `alive`**, so the pair that discriminated pre-fix is two
 7194| > survival observations post-fix and can no longer tell the guarded bit from an unguarded one.
 7195| > That is the CHANNEL vacuity in its purest form -- *a row whose named channel cannot vary under
 7196| > its named mutant* -- and it arrived by an unusual route: **the fix removed the very channel the
 7197| > rows were built on.** A detector inherited from the reproduction is not automatically a
 7198| > detector for the repair.
 7199| >
 7200| > **REPAIRED IN-ROUND (L1):** both rows re-aimed onto the channel that DOES vary post-fix -- the
 7201| > latched announce. `tick 50 txt` wants it PRESENT; `tick 49` wants it ABSENT and still reads
 7202| > `died` on a dead host, so survival stays pinned rather than traded away.
 7203| 
 7204| ## THE DISPOSITION WAS SETTLED BY THE HEADER THIS FILE ITSELF CITES
 7205| 
 7206| `dev_sgi_ip30.c` says "according to Linux/IP30" three times, so Linux's
 7207| `arch/mips/include/asm/sgi/heart.h` is the document the code was written FROM, and it is the
 7208| document that settles what the code MEANT:
 7209| 
 7210|     set_isr    +0x10020   "set interrupt status register"          write-side
 7211|     clear_isr  +0x10028   "clear interrupt status register"        write-side
 7212|     isr        +0x10030   "interrupt status register (read-only)"   READ-only
 7213| 
 7214| | site | member | what shipped |
 7215| |---|---|---|
 7216| | `0x10020` | **4 ACCEPT** on WRITE *(label contested -- see below)*, **2 DECLINE (silent)** on READ | the store is kept; the read declines SILENTLY rather than mirroring `d->isr` |
 7217| | `0x10028` | same | same |
 7218| | `0x10030` | **3** on WRITE; READ unchanged | the clear-on-write is DROPPED |
 7219| | `DEVICE_TICK` | **3** | the counter update still runs; delivery is not implemented |
 7220| 
 7221| > ### *** THIS TABLE SAID **3 DECLINE + LATCHED ANNOUNCE** ON THE READ ARMS, AND THIS ROUND'S OWN
 7222| > ### F13 RULING HAD ALREADY OVERTURNED THAT TO **MEMBER 2, SILENT DECLINE**.  Corrected 2026-09-18
 7223| > ### by the fable5 flagship seat. ***
 7224| >
 7225| > Both statements shipped in the same block -- the table here, the F13 resolution further down --
 7226| > and **a reader meets the table first.**  That is the disposition a copier carries forward, so the
 7227| > stale half was the load-bearing one.
 7228| >
 7229| > F13 silenced both READ arms for two reasons that still hold: the announce *said the wrong thing*
 7230| > (all five ISR sites print "interrupt-status rewrite not implemented", and a read is not a
 7231| > rewrite), **and** it *stole the bit* -- one benign guest read consumed the single shared
 7232| > `IP30_W_ISR` latch and permanently silenced the genuine write-side diagnostic.  ISR announce
 7233| > sites went 5 -> 3, and the enumeration shrank from fourteen cells to ten.
 7234| >
 7235| > *The defect is not that the round changed its mind -- changing it was correct, and resolving the
 7236| > design question REMOVED four cells of detector work.  It is that a SUMMARY TABLE written early
 7237| > was never re-read against the ruling that superseded it.*
 7238| 
 7239| > ### *** THE FILE'S OWN `/* Clear-on-write (TODO: is this correct?) */` IS ANSWERED **NO** BY
 7240| > ### ITS OWN SOURCE. *** `heart.h` marks `isr` read-only and clearing goes through `clear_isr`
 7241| > ### at `0x10028`, so applying `d->isr &= ~idata` there would invent a second clear path. The
 7242| > ### TODO is deleted rather than kept — which is a member-3 decline, not a member-1 deletion.
 7243| 
 7244| > ### *** THAT WARRANT IS STATED IN THE PRESENT TENSE AND THIS ROUND'S OWN DIFF FALSIFIED IT.
 7245| > ### Measured by the pass-2 opus5 seat, re-derived here before the edit. ***
 7246| >
 7247| > `"according to Linux/IP30"` appears **THREE times at HEAD and ONCE in what ships** — because the
 7248| > diff rewrote two of the three comments that carried it. So the sentence above is true of the file
 7249| > the round *read* and false of the file the round *delivers*.
 7250| >
 7251| > **The uncomfortable shape is worth naming rather than smoothing: I leaned on the file citing its
 7252| > source three times as the warrant for trusting that source, and then deleted two of the three
 7253| > citations in the same diff.** The warrant is not destroyed — `heart.h` was still the document the
 7254| > code was written from, and that is a fact about history rather than about the current comment
 7255| > count — but a reader who checks the claim against the shipped file finds it false, and a warrant
 7256| > that cannot survive its own patch was stated too strongly.
 7257| >
 7258| > #### AND THERE IS A STRONGER WARRANT THAT DOES NOT DEPEND ON `heart.h` AT ALL
 7259| >
 7260| > The seat supplied it, and the brief never gave the panel the facts to find it. *Could a guest have
 7261| > depended on `0x10030`'s clear-on-write?* **No — and not as a matter of interpretation.** Pre-fix
 7262| > the clear was followed **UNCONDITIONALLY** by `abort()`; there is no `SIGABRT` handler anywhere in
 7263| > `src/`; and this round's own `sigabrt_disposition_20260917.out` measures *"KILLED BY SIGNAL 6"*.
 7264| > **So no guest ever executed another instruction after that clear, and its effect was
 7265| > unobservable BY CONSTRUCTION for the entire time it "shipped for years."**
 7266| >
 7267| > That argument survives even if `heart.h` turns out to be a driver author's model rather than a
 7268| > hardware contract — which this round's own honest-limit section already concedes is possible. It
 7269| > should lead; the `heart.h` reading should support it.
 7270| 
 7271| **`0x10020` had NO `writeflag` test and ran its store FIRST**, so a guest LOAD wrote `idata`
 7272| (which is 0 on a read) into the ISR and *then* killed the host. Rows `kill 20 rd` and `isr keep`
 7273| pin both halves of that.
 7274| 
 7275| **TWO latch bits, not one, and the reason is a TRANSFERRED WARRANT rather than a measurement of mine:** a single shared bit would let an
 7276| ordinary guest write to Set-ISR silence the *timer* diagnostic forever, because the first
 7277| ISR-side announce would consume it. The two sites are reached by unrelated guest actions.
 7278| 
 7279| > ### *** "THE REASON IS MEASURABLE" WAS FALSE AS WRITTEN -- I MEASURED NOTHING ABOUT THE LATCH
 7280| > ### IN THIS ROUND.  Caught by the pass-2 grok seat, in its words: *"CHANGELOG's 'the reason is
 7281| > ### measurable' is also false of this instance."*  ***
 7282| >
 7283| > **The claim is right and its warrant lives in ANOTHER ROUND, which is a different and weaker
 7284| > thing than having measured it here.**  `#490` built exactly this mutant -- a one-bit form,
 7285| > `M3shared` -- and it **ESCAPED**: *"a session declining at BOTH sites sees the second fall
 7286| > silent."*  That is a MEASURED, in-tree precedent for the two-bit design, and citing it is what
 7287| > the addition licence means by a TRANSFERRED WARRANT.
 7288| >
 7289| > Stating it as *measurable* claimed the stronger evidence without doing the work, which is the
 7290| > frozen-number class wearing a warrant's clothes: **a reader cannot tell a measurement from a
 7291| > reasoned claim once the word "measured" is attached to both.**  The repair is not to weaken
 7292| > the claim -- it is to name whose measurement it is.
 7293| 
 7294| **Shape checks, comments stripped:** live `abort()` **4 → 0**; live `exit(` 0 → 0; `return`
 7295| statements **6 → 6**. Every arm uses `break`, so the common tail still writes `odata` — the
 7296| sketch rule, which four readers once failed on a function none of them knew had a tail.
 7297| 
 7298| > ### *** THE MEMBER LABEL AT `0x10020`-WRITE IS WRONG, AND SO IS THE MESSAGE IT SHIPS.
 7299| > ### Found by the pass-2 opus5 seat, reading the option set's own definition against the code. ***
 7300| >
 7301| > This round records `0x10020`-WRITE as **member 4 ACCEPT** — whose *defining* property in the
 7302| > option set is **NO LATCH**: *"there is no event to announce, and a bounded announce would ship a
 7303| > wrong record in product code."* The shipped code keeps the store **and** announces
 7304| > `"interrupt-status rewrite not implemented"` — **at a site where the rewrite IS implemented**, as
 7305| > `isr keep` proves by round-tripping `0x5a5a` through it.
 7306| >
 7307| > **The announce is warranted and the words are not.** What is missing at that arm is the
 7308| > `cpu_interrupt()` recalculation, not the rewrite — the model stores the value and then fails to
 7309| > act on it. So the honest disposition is a HYBRID the label does not name: *accept the value,
 7310| > announce the missing consequence.* `dev_pcc2.c` is the in-tree wording model.
 7311| >
 7312| > **FILED, not changed here.** Rewording product text touches five shared message sites bound by
 7313| > the latch-granularity invariant above — change the strings and the latch must change with them —
 7314| > so it is a coupled change wanting a measured delta, not a "while we are here" edit. Recorded so
 7315| > the label is not copied forward as though it fitted.
 7316| >
 7317| > #### *** AND THAT CORRECTION IS HALF A CORRECTION: IT ATTACKS THE **LATCH** AXIS AND LEAVES THE
 7318| > #### **VALUE** AXIS STANDING. Found 2026-09-18 by the fable5 flagship seat. ***
 7319| >
 7320| > Member 4 has **two** defining properties and the paragraph above refutes only one. The other is
 7321| > that *"the model ALREADY COMPUTES THE RIGHT VALUE and then discards it"* -- and at this arm that
 7322| > is exactly what is **not established**.
 7323| >
 7324| > `heart.h`, quoted in this round's own fetched warrant (`HEART_reference_20260917.txt`), reads
 7325| > **"WRITE set_isr to set bits, WRITE clear_isr to clear bits, READ isr for status."**  The shipped
 7326| > code is `case 0x10020: d->isr = idata;` -- **REPLACE** -- sitting beside
 7327| > `case 0x10028: d->isr &= ~idata;`, which *is* bitwise.  **One register pair, one document, two
 7328| > semantics; the asymmetry is the tell.**
 7329| >
 7330| > **No shipped row can see it, BY CONSTRUCTION.**  `isr keep` seeds a **zero** ISR through the Set
 7331| > arm, and at zero `=` and `|=` coincide.  One session settles it: `sd 0x1`, then `sd 0x2` to
 7332| > `0x0ff10020`, then `ld 0x0ff10030` -- set-bits gives `0x3`, replace gives `0x2`, guest-visible
 7333| > through the one read `heart.h` defines.
 7334| >
 7335| > **THE VALUE SEMANTICS ARE NOT CHANGED HERE, AND THE REASON IS SCOPE RATHER THAN CAUTION:**
 7336| > `d->isr = idata;` is **PRE-EXISTING AT HEAD** -- `git show HEAD:src/devices/dev_sgi_ip30.c` has it
 7337| > at `case 0x10020`, inherited from upstream.  This round removed an `abort()` and re-indented the
 7338| > assignment under a guard; it did not author the semantics.  Changing `=` to `|=` is a second fix
 7339| > at a second site, which the round-scope rule forbids -- *more witnesses create more candidate
 7340| > ROUNDS, never bigger rounds* -- and it is already filed as **`ip30setisrassign`** (open, MED).
 7341| >
 7342| > *The flagship seat reported this question as UNDISPOSED.  It is not -- the row exists and was
 7343| > filed during the round, and I record that the seat was wrong about it.  What it found, and what
 7344| > stands, is that the LABEL still claims a property the filed row says is unverified.  So the
 7345| > correction above was incomplete, and this completes it:* **keep `=`, and stop calling the arm
 7346| > member 4 without qualification.**
 7347| 
 7348| ## TWO ROW DEFECTS THE FIX EXPOSED, BOTH L1, BOTH REPAIRED IN-ROUND
 7349| 
 7350| **`acc 20000` expected a counter not to count.** It stored `0x1234` and wanted it back; it read
 7351| `0x161c`, and **`0x161c − 0x1234 = 0x3E8 = 1000` exactly** — `DEVICE_TICK`'s
 7352| `d->reg_0x20000 += 1000`. *The device was right and the row was wrong*: as written it was **red
 7353| on a correct build** and could never signal the defect it shipped with. The replacement oracle
 7354| is stronger ON ONE AXIS AND WEAKER ON ANOTHER — the counter is always a multiple of 1000 and `0x1234` is not, so the
 7355| residue is an exact multiple **iff the store landed**, which pins reachability the old literal
 7356| compare only achieved by accident on a tickless run.
 7357| 
 7358| **`isr keep` read the wrong load.** It issues three commands and used `printed()`, which is
 7359| `re.search` — the FIRST match — so it read the `0x10020` load the fix correctly declines (`0x0`)
 7360| instead of the `0x10030` read-back it wants. **Pre-fix this was invisible**, because the seeding
 7361| write aborted and the row read `died`. Repaired with `printed_last()` beside the existing
 7362| reader, same pattern, differing only in selection.
 7363| 
 7364| ## THE RE-PIN OWED A RED, AND IT WAS MEASURED
 7365| 
 7366| Three `txt` rows pinned the literal `"IP30 legacy interrupt rewrite"` — the PRE-FIX message,
 7367| which this round renames. Re-pinning is necessary **and observationally identical to fitting the
 7368| test to the binary**, so the order discriminator was run explicitly:
 7369| 
 7370|     pre-fix HEAD   + OLD oracle        11/18    the three txt rows PASS
 7371|     pre-fix clone  + RE-PINNED oracle   8/18    the three txt rows FAIL   <- the red
 7372|     post-fix       + RE-PINNED oracle  18/18
 7373| 
 7374| **THESE THREE ARE THE 18-ROW INSTRUMENT AND THEY STAY AS THEY ARE.** They are not the round's
 7375| headline figures -- those are 8/21 and 21/21 above -- they are the ORDER PROOF for the oracle
 7376| correction, and an order proof is a statement about three runs of ONE instrument at one moment.
 7377| Re-measuring them on the 21-row form would not strengthen it and would quietly destroy the only
 7378| evidence that the re-pin preceded the code change.
 7379| 
 7380| `REPIN_prefix_20260917.out`, measured in a scratch clone restored by `git show HEAD:` (never
 7381| from a backup), verified to carry 4 `abort()` lines before being trusted, built fresh, with a
 7382| clone-local sentinel and no project tree mutated. **Without that middle row the score moves
 7383| 11 → 18 with no way to tell which part is the fix and which is the re-pin.**
 7384| 
 7385| *Assessed and not changed: `reg_0x20000` is a 52-bit counter and `reg_0x30000` a 24-bit compare
 7386| per `heart.h`, and the tick's "only interrupt if the counter has passed the compare" TODO is
 7387| still a TODO — this round removes the host death, not the missing delivery subsystem.*
 7388| 
 7389| > ### *** "STRICTLY STRONGER" WAS FALSE, AND THE opus5 F2 SEAT MEASURED IT. ***
 7390| >
 7391| > The replacement oracle accepts `(readback - 0x1234) % 1000 == 0`, and **N = 0 IS ADMISSIBLE**.
 7392| > So with `d->reg_0x20000 += 1000;` DELETED the readback is exactly `0x1234`, the residue is 0,
 7393| > and the row is GREEN: `MH_nocounter` **27/27**, a total clean sweep.
 7394| >
 7395| > It is stronger for **store reachability** (the old literal compare passed only on a tickless
 7396| > run) and **weaker for counter liveness** (the old compare at least required a specific value).
 7397| > *That is the dropped-qualifier class: a trade restated as a strict improvement.*
 7398| >
 7399| > ### *** AND THAT PARAGRAPH WAS ITSELF WRONG -- THE THIRD ERROR IN THIS COMMENT'S LINEAGE,
 7400| > ### REFUTED BY THE fable5 ADJUDICATOR AND VERIFIED HERE IN ONE LOOK. ***
 7401| >
 7402| > It read: *"The consequence is an L3, not a tidy-up. The counter update is the DE-ESCALATION
 7403| > ACCEPT SIDE of the de-fatalised TICK arm, and nothing pins it — so the round's claim to have
 7404| > pinned the accept side of each de-fatalised predicate is false at that arm."*
 7405| >
 7406| > **`DEVICE_TICK` reads:**
 7407| >
 7408| >     d->reg_0x20000 += 1000;              <- UNCONDITIONAL
 7409| >     if (d->imask0 & ((int64_t)1<<50)) {  <- the predicate the fix de-fatalised
 7410| >
 7411| > The counter runs on **every** tick regardless of bit 50. The fix neither introduces it nor
 7412| > gates it, so `MH_nocounter` mutates **pre-existing, fix-independent** behaviour — **COVERAGE
 7413| > DEBT, filed as optional**, not a clause-(d)/L3 obligation. And the accept side of the
 7414| > predicate that *was* de-fatalised is pinned, by `tick 50` (alive) and `tick 50 txt` (announce).
 7415| > **So the round's accept-side claim is TRUE, and my correction impugned it wrongly.**
 7416| >
 7417| > **The lineage is the lesson: `tick 49` → `acc 20000` → "L3 obligation". Three claims, two of
 7418| > them corrections, and only the L4 deletion was right.** In the adjudicator's words, *"the
 7419| > correction inherited more authority than the fact, and the over-grade then propagated into the
 7420| > CHANGELOG."* This project's rule is that a correction earns a SECOND reading rather than less
 7421| > of one; seven lines of comment defeated it three times.
 7422| >
 7423| > *And this is the SECOND time this comment has been corrected. It first credited `tick 49`;
 7424| > grok caught that; the correction moved the credit to `acc 20000` and was also wrong.
 7425| > **A correction carries more authority than the error it replaces, so it earns a second
 7426| > reading, not less of one** — and this one moved a false credit onto a row that cannot carry
 7427| > it either.*
 7428| 
 7429| ## THE CHAIN CLOSES -- KILL TABLES 4 AND 5, AND EVERY PREDICTION WRITTEN DOWN FIRST
 7430| 
 7431| `PRETABLE4.out` (03:06:49) and `PRETABLE5.out` (04:30:15) each precede their table's launch, so
 7432| every prediction below was recorded before the run that tested it.
 7433| 
 7434|     TABLE 4, base 32/32                      TABLE 5, base 33/33
 7435|     V1 31/32  xbit rev            KILL       V2 32/33  xbit rev2          KILL
 7436|     V3 31/32  latch 1x            KILL       V8 33/33  -- none --         ESCAPE (disclosed)
 7437|     V4 31/32  latch 28wr          KILL       V1 32/33  xbit rev           KILL (regression)
 7438|     V5 31/32  latch 30wr          KILL
 7439|     V6 30/32  latch tick+xbit rev KILL
 7440|     V7 32/32  -- none --          ESCAPE (disclosed)
 7441|     V2 32/32  -- none --          *** ESCAPED: a row I built wrong ***
 7442|     V8 28/32  four rows           *** KILLED: a mutant I built wrong ***
 7443| 
 7444| **THE DENOMINATOR, because a bare zero does not close a chain.** Ten cells: `{4 announce sites}
 7445| x {announce fires, latch sets}` + `{2 collision directions}`. Six were closed before table 4;
 7446| tables 4 and 5 killed the remaining four (`V2`/`V1` the two collision directions, `V4`/`V5` the
 7447| two remaining latch-sets, `V6` the tick latch-set). **Two cells are DISCLOSED WITH A RULING and
 7448| both were MEASURED to escape** — the counter (fix-independent, per the fable5 ruling) and the
 7449| width axis at 0x10020 (outside the floor by the `pcc2widthkills` bound). **Zero cells outside
 7450| the enumeration.** That is the fable5 fork's first branch, so **the chain CLOSES** and the
 7451| escape hatch — drop the latch axis wholesale to disclosed debt — remains unspent.
 7452| 
 7453| ### THE TWO MISPREDICTIONS WERE BOTH MINE, AND THEY ARE DIFFERENT KINDS OF WRONG
 7454| 
 7455| **`V2` — a bad ROW.** A clobber can only bite if the clobbered class's bit was *already set*.
 7456| `xbit isr` runs tick -> ISR, so when the tick assigns, the ISR bit has never been set and the
 7457| row is green on the mutant. I gave the mirror the opposite ORDER but not the opposite
 7458| OPERAND-AND-COUNT. *The `#499` shape a third time this round — and the same defect the opus5
 7459| seat diagnosed in the original `xbit`, reproduced inside the repair for it.* Fixed by ADDING
 7460| `xbit rev2` rather than re-aiming, since `xbit isr` still carries a real claim.
 7461| 
 7462| > **`V8` — a bad MUTANT, and this is the more dangerous failure because it looks like a
 7463| > success.** 28/32, four rows red. It was anchored on the FIRST `if (writeflag == MEM_WRITE)`
 7464| > in the file — `case 0x10000`, the **interrupt mask register**. Every tick row arms bit 50 with
 7465| > a 64-bit `sd`, so `&& len == 4` refused that store and four rows died **for a reason unrelated
 7466| > to the cell under test.**
 7467| >
 7468| > **Had I not checked WHICH rows died, I would have recorded the width axis as covered when it
 7469| > was never tested** — a false "covered" in the contract, strictly worse than the honest
 7470| > "disclosed" it would have replaced. Re-aimed to guard #3 and verified by dry-run diff; the
 7471| > correct mutant then escaped, as originally predicted.
 7472| 
 7473| **A PREDICTION THAT WAS PRE-REGISTERED AND HELD.** `PRETABLE5` predicted `V1` kills via
 7474| `xbit rev`; it did not say whether `xbit rev2` would *also* red. I derived beforehand that it
 7475| would not — under `V1` the ISR assignment clobbers nothing (TICK was never set), the tick then
 7476| sets its own bit, and the second ISR access is correctly silent. **Measured: `xbit rev` alone.**
 7477| So the two collision rows separate BY DIRECTION, which is stronger than either row firing on
 7478| both: the signature identifies *which* clobber, not merely that one happened.
 7479| 
 7480| **AND `V7`/`V8` ESCAPING AS PREDICTED IS A RESULT, NOT A GAP.** A written prediction of an
 7481| ESCAPE landing says the disclosure is honest rather than a hedge — the cell is named, ruled on,
 7482| and now measured.
 7483| 
 7484| ## THE fable5 ADJUDICATION -- ROSTER 9/9, AND THE RULING WENT AGAINST ME TWICE
 7485| 
 7486| The ninth and last seat. **Identity verified rather than assumed**, per standing directive: it
 7487| returned the liveness token, the verbatim first line of `CHECKPOINT.md`, and **named its own
 7488| model** (`claude-fable-5-1`) — an Agent invocation can silently land elsewhere, and this round
 7489| had no way to tell without asking.
 7490| 
 7491| **VERDICT: RATIFY THE FIX; DO NOT RATIFY THE DETECTOR AS SHIPPED. The latch-axis closure is
 7492| IN-ROUND, not filed.** Six of opus5's eight escapes weaken `d->warned |= IP30_W_*` statements
 7493| **the fix's own diff introduced** — the canonical clause-(d) shape — so L2 by the floor. And the
 7494| contract already claimed to catch two of them, measured false, which is an L4 to edit in-round
 7495| regardless. Filing was refused *because this closure had been mis-declared complete once
 7496| already.*
 7497| 
 7498| ### THE TWO RULINGS AGAINST ME
 7499| 
 7500| **(1) My counter-pin correction was itself wrong — the third error in one comment's lineage.**
 7501| `DEVICE_TICK` increments `reg_0x20000` **unconditionally, two lines above** the `imask0 &
 7502| (1<<50)` guard the fix de-fatalised. So `MH_nocounter` mutates **pre-existing, fix-independent**
 7503| behaviour: coverage debt, not an L3 obligation — and the accept side of the de-fatalised
 7504| predicate *is* pinned, by `tick 50` + `tick 50 txt`. **My correction impugned a claim that was
 7505| true.** Lineage: `tick 49` → `acc 20000` → "L3 obligation" — *three claims, two of them
 7506| corrections, and only the L4 deletion was right.*
 7507| 
 7508| **(2) My `§OWED` misfiled my own doubt.** I named F10 as the disposition I least trusted; it is
 7509| F13, and fable named the incoherent cell exactly. Axes: `{read announces}` × `{message
 7510| per-offset distinct}`. Rejecting F10 while keeping F13 sits at **(announce YES, distinct NO)** —
 7511| an undistinguished FALSE message that steals the write-side bit. Defensible on neither axis.
 7512| 
 7513| ### F13 RESOLVED: MEMBER 2, SILENT DECLINE -- AND IT MADE THE CLOSURE *SMALLER*
 7514| 
 7515| Both read arms are now silent. That kills two defects at once: the announce **said the wrong
 7516| thing** (all five ISR sites print "interrupt-status rewrite not implemented", and a read is not
 7517| a rewrite) and it **stole the bit** — one benign guest read consumed the single shared
 7518| `IP30_W_ISR` latch and permanently silenced the genuine write-side diagnostic, including the
 7519| architecturally-wrong `0x10030` write this round cares most about.
 7520| 
 7521| **ISR announce sites 5 → 3, so the enumeration went from FOURTEEN cells to TEN.** *Resolving the
 7522| design question removed four cells of detector work rather than adding them.*
 7523| 
 7524| > ### *** AND IT IMMEDIATELY INVALIDATED ONE OF MY OWN ROWS -- THE THIRD TIME THIS ROUND A FIX
 7525| > ### DESTROYED THE CHANNEL A ROW RESTED ON. ***
 7526| >
 7527| > `latch 1x` counted announces from the two READ arms. The moment they went silent it read
 7528| > `got=0 want=1` — vacuous by construction, measuring a channel the repair had removed. Caught
 7529| > only because the base was re-measured **before** the closure was built on top of it.
 7530| >
 7531| > The three instances: de-fatalisation removed the **death** channel (the tick pair, codex);
 7532| > the silent decline removed the **announce** channel (`kill 20/28 rd txt`, anticipated); and
 7533| > the same repair removed the announce `latch 1x` was counting (**not** anticipated).
 7534| >
 7535| > **The general form: a repair must be checked against every row whose oracle reads the channel
 7536| > it changes.** A row invalidated that way goes green or red for reasons unrelated to the mutant
 7537| > it names — the exact vacuity the CHANNEL rule exists to catch, arriving through a door that
 7538| > rule does not watch. `latch 1x` is re-aimed onto the two WRITE arms, which keep their store
 7539| > *and* announce.
 7540| 
 7541| ### THE CLASS CLOSURE -- TEN CELLS, AND THE MEASUREMENT I NEARLY UNDER-RAN
 7542| 
 7543| Enumerated from the function's own inputs: `{4 announce sites} × {announce fires, latch sets}` +
 7544| `{2 collision directions}`. Six were already closed; four rows close the rest — `latch 28wr`,
 7545| `latch 30wr`, `latch tick` (the `ME` flood cell, ranked worst of the eight) and `xbit rev` (the
 7546| `MA` direction `xbit` runs backwards).
 7547| 
 7548| Two of those need a **second forced `DEVICE_TICK`**. Fable allowed an unbuildable cell to be
 7549| disclosed with its apparatus reason — **but only after being measured unbuildable.** Measured,
 7550| counting ticks by the unconditional `reg_0x20000 += 1000`:
 7551| 
 7552|     step 1 / 2 / 3 / 8 / 1000  ->  ONE tick
 7553|     step 65536 / 70000         ->  TWO
 7554|     step 140000                ->  THREE
 7555| 
 7556| > **STOPPING AT `step 8` WOULD HAVE DISCLOSED TWO BUILDABLE CELLS AS UNBUILDABLE** — a false
 7557| > exemption written into the contract on an under-tested measurement. The threshold is ~65536
 7558| > because `machine.c` decrements `ticks_till_next` by **one** per single-step, so these rows are
 7559| > slow *by construction*: that is the price of the cell, not an accident.
 7560| 
 7561| *Two apparatus errors on the way, both caught by loud failures rather than luck: a bare `step N`
 7562| spliced between op-sequences, and — worse — an **invented address constant** (`0x0ff20000`)
 7563| where the probe defines `A_C20000`. The load returned the SENTINEL, which is the
 7564| hand-assembled-constant trap; a plausible value would have been believed.*
 7565| 
 7566| ### THE CHAIN'S STOP CONDITION, PRE-COMMITTED
 7567| 
 7568| Converging, not `#392` — the fix has been stable and approved since pass 1, and every pass has
 7569| been about the detector. **But closure was declared one pass early**, because kill table 2
 7570| counted the latch mechanism as two cells when it is roughly eight. *A bare zero against a wrong
 7571| enumeration does not close a chain* — this round's own citation of that rule, with itself as the
 7572| counter-example.
 7573| 
 7574| **The fork that makes it terminate:** one closure diff, one verifying pass confirming **zero
 7575| cells outside the stated enumeration**, denominator named. Only already-enumerated cells now
 7576| killed → the chain **closes**. A fifth escape **outside** the enumeration → the
 7577| fresh-process-probe-versus-shared-lifetime-latch architecture is the root cause, and the latch
 7578| axis drops **wholesale to disclosed debt** rather than becoming pass six.
 7579| 
 7580| ## THE ADJUDICATION PASS FOUND A FLOOR BREACH IN THE CLASS CLOSURE ITSELF
 7581| 
 7582| The §F2 pass — the panel sharing its findings rather than answering blind — ran on **8 of 9**
 7583| (seven scriptable seats; the kimi CLI on its weekly wall and COVERED by `kimi-k3:cloud`; the
 7584| opus5 seat outstanding). **Fable is held by standing directive and speaks last, so every ruling
 7585| here is PROVISIONAL ON ITS FACE.**
 7586| 
 7587| It found **one floor breach, two wrong warrants of mine, and one records gap in the harness.**
 7588| 
 7589| ### THE BREACH: `isr 28 rd val` -- the symmetric cell, left open by the closure that claimed to close it
 7590| 
 7591| Required by **agy** (GO-WITH-CHANGES), named independently by **grok**. The two READ arms are
 7592| structurally identical — both decline, both announce, both leave `odata` at 0 — so shipping
 7593| `isr 20 rd val` without its sibling is the `#499` shape exactly: *repaired at the address the
 7594| mutant used, symmetric cell left open for the next pass.* A mirror mutant at `0x10028` survives,
 7595| still announces (`kill 28 rd txt` stays green), and changes only a value no row reads.
 7596| 
 7597| **REPAIRED AND MEASURED — kill table 3** (`killtable3_20260918/`, `PRETABLE3.out` at `00:49:41`
 7598| against the table's `00:50:16`):
 7599| 
 7600|     base            28/28
 7601|     M11_mirror28    27/28    isr 28 rd val    0x5a5a -> 0x0
 7602| 
 7603| > ### *** THE CAUSE IS WORTH MORE THAN THE ROW, AND IT WAS IN THIS ROUND'S OWN PRE-TABLE BLOCK. ***
 7604| >
 7605| > grok's diagnosis: **`PRETABLE.out` listed BOTH read arms as *"decline, no value to pin"*.**
 7606| >
 7607| > **A DECLINE HAS A VALUE, AND IT IS 0.**
 7608| >
 7609| > That framing made the miss MECHANICAL. The enumeration asked which arms ANNOUNCE and treated a
 7610| > refusal as having no observable — when the refusal's own RETURNED VALUE is precisely the
 7611| > channel `M10` travels on. Having then added `isr 20 rd val` from the measuring seat's
 7612| > prescription, nothing sent me back to the sentence saying neither arm had a value.
 7613| >
 7614| > **The general form, for the next enumeration:** when a block classifies an arm as *"declines,
 7615| > nothing to observe"*, ask what the decline RETURNS. A refusal is not the absence of an
 7616| > observable; it is an observable with a specific value, and a mutant can change it while leaving
 7617| > every announce and every survival row untouched.
 7618| >
 7619| > *`PRETABLE.out` and `PRETABLE2.out` were NOT edited to carry this correction. Their mtimes ARE
 7620| > the order proofs for tables 1 and 2; editing either would reset the mtime and destroy the
 7621| > property the block exists to provide. **A correction to an order-proof artifact goes in the
 7622| > next block.***
 7623| 
 7624| ### THE FOURTH UNREAD REVIEW -- and the `#490` rule was OBEYED and could not catch it
 7625| 
 7626| grok pointed at its own earlier answer, and it was verified by opening the file rather than
 7627| taken on its word. `regress/artifacts/ip30abortkill/FIXDIFF_grok_20260917.txt:239`:
 7628| 
 7629| > ``5. `isr 20 rd` / `isr 28 rd` — load does not clobber ISR; load's **value** is not the seeded
 7630| > ISR (don't-mirror)``
 7631| 
 7632| **Both rows, prescribed by name, in a durable artifact, before the fix shipped.** The opus5 seat
 7633| independently reported the same pattern — four of grok's six prescribed rows never shipped.
 7634| 
 7635| **THE STRUCTURAL GAP:** after `#490` the rule is *"a row list rewritten from a panel's findings
 7636| is DIFFED against the pre-table block's own prescribed rows."* That binds the **PRETABLE**. Here
 7637| the prescription **never entered a PRETABLE** — it lived in a seat's FIX-DESIGN answer, and
 7638| nothing diffs a row list against that. **The rule was obeyed and the row was still lost: the
 7639| diff ran against the wrong source document.** Worse, the PRETABLE positively asserted that
 7640| neither row was owed — *a pre-table block that mis-classifies a cell does not merely fail to
 7641| catch the omission; it CERTIFIES it.* Filed as `seatprescriptiondiff`.
 7642| 
 7643| ### TWO WRONG WARRANTS OF MINE, BOTH CORRECTED -- right conclusions, reusable-wrong reasons
 7644| 
 7645| * **The `asdvasdvnb` out-of-scope filing** (caught by **kimi**, as its answer to *"which of your
 7646|   accepted dispositions is wrong?"*). My warrant read *"a host kill and a log flood are different
 7647|   classes"* — which **keys on IMPACT, a correlate of the defect**, committed in the sentence
 7648|   excluding a row during a round spent cataloguing that error. The reopening rule's real test is
 7649|   its own parenthetical, **"so one fix design covers both."** The filing stands and is stronger:
 7650|   it fails on THREE independent counts — not the same device (`sgi_ip30_2` is a separate
 7651|   registration), not one fix design (`#531` de-fatalises; that arm needs member 1 DELETE), and
 7652|   not the same detector (no row reaches that offset, so it needs a new oracle).
 7653| * **The `set_isr` assessed-not-changed warrant** (caught by **glm** and **kimi** independently).
 7654|   It said the addition licence wants a measured delta "**neither of which exists**" — while the
 7655|   measured delta sat in the SAME packet (`0x00ff` then `0x5a00` gives `0x5a00`, not `0x5aff`).
 7656|   The disposition stands on **SCOPE**, not on absence of evidence.
 7657| 
 7658| *A wrong reason gets reused. The next round filing a sibling would have copied "different
 7659| impact" and eventually applied it to two sites that DO share a fix design.*
 7660| 
 7661| ### RECORDED, NOT RESOLVED
 7662| 
 7663| **F13 — does the read-arm announce consuming the shared ISR latch make it a functional defect?**
 7664| **glm** and **deepseek** say yes independently (a single guest READ of `0x10020` consumes the one
 7665| bit the write-side announces need, so the architecturally-wrong `0x10030` write goes silent
 7666| forever); **kimi** upholds it as kept-and-disclosed. **SPLIT 2-1, FILED under the stopping rule**
 7667| — neither a measured false pass nor a wrong record. *A disagreement must not be settled by
 7668| whoever writes it up.*
 7669| 
 7670| Also filed: **the string's TRUTH was never audited** (glm and kimi, independently — the panel
 7671| examined the message's granularity and its latch, and never whether *"interrupt-status rewrite
 7672| not implemented"* is true at arms that keep their stores); **the per-INSTANCE latch axis** (kimi
 7673| — `N = 1` per device instance, and the tree ships `sgi_ip30_2`); and **fall-through after a
 7674| non-exiting `fatal()`** (deepseek).
 7675| 
 7676| ### WHAT THE PANEL SETTLED THAT I COULD NOT
 7677| 
 7678| **grok answered the closure's boundary question.** The width/`len` axis is **NOT floor here** —
 7679| no edited arm tests `len`, and the floor is dominating predicates x device-state lvalues the
 7680| repair path reads. Position/translation is **NOT floor either** — this detector claims no decode
 7681| window. Both are honest clause-(e) debt, which is what the contract says. It classified the
 7682| missing row as **sibling parity, not a new floor axis**, on the join-axis letter: `relative_addr`
 7683| does not flow into an lvalue the `0x10028` else body reads.
 7684| 
 7685| **And agy verified kill table 2 against the artifacts row by row** — re-reading each score and
 7686| each failing row from disk, and `cmp`-ing the restored tree against the preserved baseline —
 7687| rather than taking the packet's figures. It agreed.
 7688| 
 7689| ## KILL TABLE 1 -- THE FLOOR, DISCHARGED BY MEASUREMENT RATHER THAN BY A CLEAN SCORE
 7690| 
 7691| `21/21` discharged nothing. The two rows added for the L2 breach read `died` pre-fix **because
 7692| their seeding write aborts** — the reproduction working, not a measured kill — and the
 7693| failability rule is explicit that an accept-side row is discharged by a KILL, never by existing.
 7694| 
 7695| Six mutants, scratch clone, baseline NAMED (the round's post-fix working set, not HEAD) and
 7696| `cmp`'d SAME before mutant 1, baseline rebuilt in the clone with `[ binary -nt source ]` as its
 7697| own freshness proof, clone-local sentinel, restore from the named baseline and never from a
 7698| script backup. Every log carries `IP30ABORT_DONE`; all seven preserved at
 7699| `regress/artifacts/ip30abortkill/killtable_20260917/`.
 7700| 
 7701|     MUTANT             SCORE    ROW(S) RED           got -> want
 7702|     base                21/21   --
 7703|     M1_del28store       20/21   isr clr              0x5a5a -> 0x5050
 7704|     M2_reins30clear     20/21   isr drop 30          0x484a -> 0x5a5a
 7705|     M3_tickquiet        20/21   tick 50 txt          no -> yes
 7706|     M4_quiet30          20/21   kill 30 txt          no -> yes
 7707|     M5_bit49            19/21   tick 50 txt          no -> yes
 7708|                                 tick 49              yes -> no
 7709|     M6_sharedlatch      21/21   *** NONE -- CLEAN SWEEP, ESCAPED ***
 7710| 
 7711| **EVERY REPAIR THIS ROUND MADE IN RESPONSE TO A SEAT IS NOW MEASURED FAILABLE.** `M1` is the
 7712| measuring seat's own severest escape (it scored **19/19** against the pre-repair instrument) and
 7713| the row four packet-fed seats converged on kills it. `M4` is agy's cell — **19/19 on the old
 7714| binding, dead on the re-bound row.** And `M2`'s `0x484a` is exactly the value derived
 7715| arithmetically before the run, so the prediction and the measurement agree rather than merely
 7716| not conflicting.
 7717| 
 7718| **`M5` is the strongest signature in the table and it is not a simple red.** Moving the tick
 7719| guard from bit 50 to bit 49 reds BOTH halves of the re-aimed discriminator **in opposite
 7720| directions** — `tick 50 txt` loses the announce, `tick 49` gains it. The observable is not
 7721| "a row failed" but *"the announce MOVED"*, which only that mutant produces. That is the codex
 7722| finding closed end to end: the pre-fix pair discriminated by ALIVE/DEAD, the fix destroyed that
 7723| channel, and the re-aim restored discrimination **and made it directional.**
 7724| 
 7725| > ### *** `M6` ESCAPED, AND IT WAS PREDICTED IN WRITING BEFORE THE TABLE RAN. ***
 7726| >
 7727| > `PRETABLE.out` — whose mtime (`22:58:19`) precedes the table's launch (`22:59:36`), which is
 7728| > the order discriminator the block exists to provide — states the prediction and its
 7729| > derivation: **every session is a fresh process, so no row exercises both announce classes in
 7730| > one device lifetime**, which is exactly the state a shared bit corrupts. Measured: **21/21,
 7731| > clean sweep.**
 7732| >
 7733| > **THE PRE-TABLE BLOCK ASKED ITS FIRST MANDATED APPLICATION TO *CHECK* THE CHANNEL RULE, NOT
 7734| > MERELY OBEY IT.** The rule's claim is that a row's channel under its mutant is knowable at
 7735| > WRITING time, before any table runs. This is the first test of it in this project and **it
 7736| > held**: a cell was named, derived and disclosed in advance, and the measurement agreed.
 7737| >
 7738| > A predicted, disclosed escape is **coverage debt with a date on it**, not a surprise — and it
 7739| > is closed by the class closure below rather than left in the contract.
 7740| 
 7741| ## KILL TABLE 2 -- THE CLASS CLOSURE, AND THE CHAIN'S STOP CONDITION MET
 7742| 
 7743| `M6` escaped table 1 **as predicted in writing beforehand**. Two consecutive passes had then
 7744| found breaches of ONE class — announce ATTRIBUTION — so the `#499` amendment applies and the
 7745| repair does **not** patch the cell the mutant used. The space is enumerated from the function's
 7746| own inputs: `{0x10020, 0x10028, 0x10030} x {READ, WRITE}` minus the serviced `0x10030`-READ,
 7747| plus TICK — **six announce sites** — plus the latch mechanism's two failure modes, COLLISION
 7748| and DEFEAT. Every open cell closed in ONE diff: **21 -> 27 rows.**
 7749| 
 7750|     MUTANT             SCORE    ROW(S) RED                    got -> want
 7751|     base                27/27   --
 7752|     M6_sharedlatch      26/27   xbit isr                      0 -> 1
 7753|     M7_silent20wr       25/27   kill 20 wr txt + xbit isr     no -> yes
 7754|     M8_silent28wr       26/27   kill 28 wr txt                no -> yes
 7755|     M9_nolatch          26/27   latch 1x                      2 -> 1
 7756|     M10_mirror20        26/27   isr 20 rd val                 0x5a5a -> 0x0
 7757|     M1_del28store       26/27   isr clr                       0x5a5a -> 0x5050
 7758| 
 7759| > ### *** THE PARAGRAPH BELOW DECLARED THE CHAIN CLOSED AND IT WAS FALSE.  The opus5 F2 seat
 7760| > ### then built EIGHT mutants and ALL EIGHT scored 27/27, six of them inside cells this very
 7761| > ### enumeration called closed.  Corrected 2026-09-18 on the fable5 adjudication. ***
 7762| >
 7763| > **The defect was in the ENUMERATION, not in the arithmetic.** This pass counted the LATCH
 7764| > MECHANISM as **two cells** (collision, defeat). It is **roughly eight** — six duplicated
 7765| > `d->warned |= IP30_W_*` statements, one beside every announce, times two collision directions.
 7766| > **A bare zero against a wrong enumeration does not close a chain**, which is the repair
 7767| > chain's own Correction 1, and this round supplied the counter-example to its own citation of
 7768| > it.
 7769| >
 7770| > *The chain is CONVERGING rather than `#392` — the fix has been stable and approved since pass
 7771| > 1, and every pass has been about the detector — but closure was declared ONE PASS EARLY.*
 7772| 
 7773| **ZERO NEW BREACHES against the enumeration AS IT THEN STOOD.** The closing pass verified that
 7774| enumeration rather than hunting cells, which is the stop condition — and the denominator is stated rather than implied: six announce
 7775| sites, two latch failure modes, one declined-read value; the two axes deliberately NOT swept are
 7776| named in the contract below. *"Zero found" and "zero looked for" must not render the same.*
 7777| 
 7778| `M6` is the point of the exercise: **21/21 clean sweep before, 26/27 after**, killed by
 7779| `xbit isr got=0 want=1` — the tick consuming the shared bit and silencing the ISR arm, exactly
 7780| the derivation `PRETABLE2.out` recorded before the run.
 7781| 
 7782| > ### *** TWO ORACLE SHAPES THIS PROBE DID NOT HAVE, AND `M9` PROVES THE FIRST WAS NECESSARY
 7783| > ### RATHER THAN DECORATIVE. ***
 7784| >
 7785| > **`latch 1x` COUNTS announces instead of detecting one.** Under `M9` the arm announces on
 7786| > EVERY access: measured `got=2 want=1`. **A presence oracle reads `yes` on the fix AND on the
 7787| > mutant** — it cannot see the defect at all. Had that row been written `yes`/`no` it would have
 7788| > been VACUOUS BY CONSTRUCTION, which is the CHANNEL rule's own failure mode arriving one level
 7789| > along, inside the repair for it.
 7790| >
 7791| > **`xbit isr` / `xbit tick` put BOTH announce classes in ONE device lifetime.** Every other row
 7792| > in this probe runs in a fresh process, and a shared bit is only corrupt when two classes meet
 7793| > — so no fresh-process row can see a collision, however many there are. On the fix both read
 7794| > **1**, which is *the first direct measurement that the two latch bits are independent* — the
 7795| > round's central product-code claim, which the grok seat correctly called "a prediction sitting
 7796| > beside real measurements with no row behind it."
 7797| >
 7798| > *The recipe came from the measuring seat, including its warning that its own first attempt was
 7799| > a defective apparatus: `ticks_till_next[n] = 0`, so the tick's single free firing lands on the
 7800| > session's FIRST `machine_run` and a seeding store placed before the arm silently consumes it.
 7801| > ARM BIT 50 FIRST.*
 7802| 
 7803| **THE SIGNATURES DISAMBIGUATE, AND THAT IS A PROPERTY WITH A COST WORTH WRITING DOWN.**
 7804| `M6` reds `xbit isr` ALONE; `M7` reds `kill 20 wr txt` AND `xbit isr`, because the `xbit`
 7805| session's ISR access is itself a write at `0x10020`. So the pair separates "the bits collided"
 7806| from "that arm's announce is gone." **But `xbit isr` is therefore NOT a pure collision detector**
 7807| — it reds for two causes, and only `kill 20 wr txt` separates them. *The two rows are COUPLED:
 7808| delete `kill 20 wr txt` as redundant and `xbit isr` silently stops meaning what its comment
 7809| says.* Recorded because a future reader pruning rows would have no other way to know.
 7810| 
 7811| **`M1_del28store` WAS RE-RUN ON PURPOSE.** `#462` measured that adding rows perturbs other
 7812| mutants' scores, so table 1's five kills were claims about an instrument that no longer existed.
 7813| `PRETABLE2.out` stated plainly that "six new independent sessions cannot perturb it" was
 7814| REASONED, NOT MEASURED, and named `M1` as its single test. Measured: **26/27, `isr clr` alone,
 7815| `0x5a5a -> 0x5050` — identical to table 1.** The claim is now measured rather than asserted.
 7816| 
 7817| ### THE CONTRACT (vacuity-floor clause (e)) -- what this detector is designed to catch
 7818| 
 7819| **CATCHES**, each with a measured kill: reinstating any of the four `abort()` calls; deleting the
 7820| announce at ANY of the six sites; deleting either surviving store; re-inserting the dropped
 7821| `0x10030` clear-on-write; moving the tick guard between bits 49 and 50; mirroring `d->isr` into a
 7822| declined read; collapsing the two latch bits onto one; defeating the latch mask outright.
 7823| 
 7824| **DOES NOT CATCH, disclosed rather than discovered later:**
 7825| * **the WIDTH / `len` axis** — the probe uses only `lw`/`sw`/`ld`/`sd`. This is `#499`'s own axis
 7826|   and it is unexplored here.
 7827| * **POSITION / translation (clause (f))** — no row asserts WHICH cell an access lands on, so a
 7828|   re-map that keeps the probed offsets distinct is invisible.
 7829| * **latch-macro RENUMBERING** — measured EQUIVALENT (all uses go through the macros, no
 7830|   observable differs), so it is a RESULT rather than a gap.
 7831| * **`dev_sgi_ip30_2`** — a different device, filed separately as `ip30asdvasdvnb`.
 7832| 
 7833| ## PASS 2 DID NOT RATIFY, AND FOUR OF ITS FINDINGS WERE DEFECTS IN THIS ROUND'S OWN WORK
 7834| 
 7835| Seven scriptable seats answered (`_scratchpad/panel_20260917_215210`). **The kimi CLI was on its
 7836| weekly 403 wall and its seat is COVERED by the `kimi-k3:cloud` substitute, not lost** — recorded
 7837| by transport, as the ledger requires. opus5 was still running and **fable5 is held by standing
 7838| directive until every other seat has spoken**, so the stage stands at **7 of 9 and every ruling
 7839| below is PROVISIONAL ON ITS FACE.**
 7840| 
 7841| Not one seat ratified. Four findings were verified against the code — not taken on a seat's word
 7842| — and repaired in-round; two more were corrected in the records above.
 7843| 
 7844| | # | finding | seats | grade | repair |
 7845| |---|---|---|---|---|
 7846| | 1 | the latch comment's `ONE BIT PER SITE` is false — five ISR paths share one bit | codex, grok, glm | **L4** | comment restated as the invariant that makes the design correct |
 7847| | 2 | the tick pair stops discriminating post-fix — both rows read `alive` | codex, minimax | **L1** | both re-aimed onto the announce channel; `tick 50 txt` added |
 7848| | 3 | `kill 30 txt` read the `isr keep` transcript, which writes 0x10020 | agy | **L1** | re-bound to the 0x10030 session |
 7849| | 4 | nothing observed that `d->isr &= ~idata` still runs at 0x10028 | deepseek, glm, kimi, minimax | **L2 FLOOR BREACH** | row `isr clr` added |
 7850| | 5 | nothing pinned that the 0x10030 write is *discarded* | agy, glm, kimi | — | row `isr drop 30` added |
 7851| | 6 | the counter pin credited `tick 49`; `acc 20000` is the row | grok | **L4** | comment corrected |
 7852| 
 7853| **THE ONE WORTH CARRYING IS #3, AND NOT FOR ITS SIZE.** `kill 30 txt` was bound to a session that
 7854| writes **0x10020** and never touches 0x10030 — and because **all five ISR announces are byte-
 7855| identical**, it read `yes` off the wrong arm and sat GREEN while structurally blind to its own
 7856| named mutant. *The shared message is correct design — it is what makes the unqualified `(once)`
 7857| marker true — and it is exactly what made this undetectable by reading the output.* Pre-fix the
 7858| row reddened because its seeding session DIED, not because the announce it claims to observe was
 7859| absent: **right colour, wrong reason, on both builds.**
 7860| 
 7861| It is the **third** rolling-`t` defect in this one probe, after `acc 20000` and `isr keep`. All
 7862| three have the same shape — a row reading a transcript variable that a later `session()` call has
 7863| since overwritten — and the class is now closed by construction: every `t`-reading row binds to
 7864| the session immediately above it, verified by listing them in file order.
 7865| 
 7866| **FINDINGS REJECTED, WITH WARRANTS, because a round that accepted everything has stopped arguing:**
 7867| `deepseek`'s latch-macro renumbering is a true clean sweep but an **EQUIVALENT** mutant — all uses
 7868| go through the macros and no observable differs — so it is a RESULT, not a gap. `glm`'s request to
 7869| put the register offset in the warn text is **refused and filed**, and finding #1's own invariant
 7870| is the warrant: qualifying the message obliges qualifying the latch, so it is a coupled change
 7871| rather than a text edit. `codex`'s two extra option-set members are refused — halting the guest on
 7872| a legal-looking register write is worse than what shipped, and alias/forwarding is precisely what
 7873| `heart.h` rules out. `deepseek`'s claim that a guard-growth mutant at 0x10020/0x10028 would redden
 7874| no row is **measured false**: `kill 20 wr` and `kill 28 wr` exist and die.
 7875| 
 7876| **FILED, NOT FIXED:** `ip30asdvasdvnb` — an UNLATCHED guest-drivable `fatal()` with a keyboard-mash
 7877| message (`asdvasdvnb`) in `DEVICE_ACCESS(sgi_ip30_2)`, found by grok. Verified upstream residue
 7878| against HEAD. It is out of scope because it carries no `abort()`: a host kill and a log flood are
 7879| different semantic classes, and the round-scope rule admits a second site only in the same class.
 7880| 
 7881| **A BRIEF DEFECT OF MINE, recorded as such:** glm correctly objected that `heart.h` was never
 7882| INLINED, so every specific drawn from it — the offsets, `(read-only)`, the 52/24-bit widths — was
 7883| an *assertion* to a seat with no filesystem. That is the packet-fed rule this project has broken
 7884| before, and it is repaired in the adjudication packet rather than argued with.
 7885| 
 7886| > ### *** 21/21 DOES NOT DISCHARGE THE FLOOR, AND THIS ROUND WILL NOT IMPLY OTHERWISE. ***
 7887| >
 7888| > The two rows added for the L2 breach read `died` pre-fix **because their seeding write aborts** —
 7889| > not because they observed a wrong value. That is the reproduction working. The failability rule
 7890| > is explicit: an accept-side row is discharged by a **MEASURED KILL**, never by existing. The
 7891| > discharge is kill table 1, and `PRETABLE.out` was written before it ran so its own mtime proves
 7892| > the order.
 7893| >
 7894| > **These repairs also owe their own pass 2** — the obligation follows the material, not the
 7895| > narrative.
 7896| 
 7897| ---
 7898| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_531: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC531: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
