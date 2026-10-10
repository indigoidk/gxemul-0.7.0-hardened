# Records check of one methodology ruling (queue item 7n-4) -- GPT-6 Astra confirmation

Open with `VERDICT: CONFIRM / CONFIRM WITH CHANGES (<n>) / DO NOT CONFIRM`.  READ-ONLY: write nothing, build nothing.

**Scope your reading** to: the ruling `GXEMUL-SEC\regress\artifacts\fablequeue7n_20261009\fable5_rule7n_4.md`; the queue
entry `### 7n-4.` in `GXEMUL-SEC\tools\pipeline\fable_queue.md`; `GXEMUL-SEC\src\devices\dev_vme.c` and the VME2 header it
includes; `GXEMUL-SEC\src\core\memory.c` (the word-access helpers it cites); and the OpenBSD 2.2 guest sources the ruling
cites under `C:\DocumentNoSnc\cc\GXEMUL\_guest-src-openbsd22\` (`sys/arch/mvme88k/dev/vme.c`, `trap.c`, `eh.S`).  Do not
read `regress/artifacts/` beyond the ruling, or `tools/pipeline/ledger.json`.

The flagship seat ruled on whether the owner's earlier disposition for `dev_vme.c`'s `default:` arm (return a bus error,
"FAULT", for any offset no case handles) reaches three populations of offsets: (1) offsets no register occupies,
(2) registers the header names that the emulator does not implement, (3) sub-word lanes of implemented registers.  Its
reading: FAULT fits (1) only; for (2) the in-tree OpenBSD 2.2 guest reads and writes several such registers
unconditionally (MASTERCTL, MASTER3/4/4MOD at attach; IRQSTAT/IRQCLR in its abort handler) with no fault recovery, so a
bus error there would stop the guest; (3) is an access-width question the ruling never addressed.

**This is a RECORDS CHECK of the ruling's FACTS, not a re-argument of the policy.**  Check: the population counts it
derives (26 named-but-unhandled registers; 40 sub-word starts); that the cited OpenBSD lines access those registers
outside any probe or recovery path; that `memory.c`'s helpers make "serve the containing word" read the wrong lane and
clobber a whole word on a sub-word write, and that T1COUNT's read has a side effect; that `dev_vme.c` is unchanged since
the upstream import; and that `_scratchpad/vmesbcp2.pdf`/`.txt` lacks the VMEchip2 chapter (count pages and chapters).

## Questions -- `<n> | <answer>`
1. Which factual claims are FALSE or unsupported?  Quote each and give the correct fact.
2. Does the conclusion that population 2 needs the owner's re-ruling follow from the facts as corrected?
3. Anything omitted that the owner would need to decide population 2?
**If you found something ELSE -- say so.**
