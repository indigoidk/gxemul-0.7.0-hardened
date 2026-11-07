# Reading task: hrec_mrwstore2 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBHRECMRWSTORE2-72ce` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one held harness row, `mrwstore2` (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator; this fork keeps a
ledger of every filed issue, and a HARNESS row is about the project's own test tooling.  The row below is HELD with its
fix committed; its record is the commit message(s) and any CHANGELOG block shown.  A flagship review is still owed.  You
cannot read files, so judge the record AS WRITTEN.  Do not simply ratify it.  A bracketed dated note is this project's
in-place correction form (it quotes what it corrects); it is not by itself a contradiction.

## The ledger row `mrwstore2` (state `held`)

**title:** mrwstore2  A straddling store whose tail faults makes an MMIO head see the write twice

**state_note (head):** *** L4 CORRECTION 2026-08-27: MY OBSERVABLE IS WRONG AND MY RANKING WAS TOO HIGH. The mature ledger entry already measured three of this row's claims FALSE, and I did not read it before writing a fresh note on top. ***

**THE OBSERVABLE IS NOT 'TWO WHEN BROKEN, ONE WHEN FIXED'.** It is **1 -> 4+ writes**. My two-versus-one framing was a guess at the shape of a count, not the measured count.

**THREE CLAIMS ALREADY MEASURED FALSE in this row's own history**, which I wrote over rather than read:
  * *introduced by `#430`* -- FALSE;
  * *the memblock split always had it* -- FALSE;
  * *256x* -- the real figure is **1024x**.

*** AND THE REACHABILITY IS NEAR-NIL, MEASURED: three instrumented guest boots -- pmax, luna88k, macppc -- produced **ZERO** straddling stores. Only **11 of 1024** offsets can even start one, and it is PowerPC-only. *** It may also be architecturally CORRECT partial-completion-with-restart, which no one has refuted.

**DISPOSITION: DOCUMENTED-ONLY, ranked LAST of the guest-reachable set (8th of 8).** Not a live-corruption peer of [[b115]] or [[wdcringambig]], which is where I had implicitly put it.

*The lesson is mine and specific: I recorded a fresh seat answer as a NEW note on a row that already had a mature, more-measured entry underneath. **A row with existing evidence must be READ before it is written to** -- otherwise a fresh reading silently outranks an older measurement, which is the opposite of how evidence should compose.*

*** EVIDENCE 2026-08-27: TRUE, guest-reachable on PowerPC, and the observable is unusually clean -- a COUNT, not a value. ***

**The mechanism, and it needs the guest's own fault handler to complete it:** a store that STRADDLES a page boundary performs its head chunk BEFORE translating the tail. When the head lands in MMI

**hold_question:** A straddling store whose tail faults makes an MMIO head see the write twice. The row was REPRODUCED at rung 3 and then RE-RANKED DOWN -- three of its factual claims were measured false, it is PPC-only, no in-tree guest reaches it, and the fix may itself DIVERGE from real hardware. QUESTION: given all that, is this documented-only? Be specific about the last point, because it is the one that decides: what does real PPC hardware do on a straddling store whose second half faults, and is our current behaviour actually wrong? If we cannot establish the hardware behaviour, then 'fix' is unwarranted and the honest disposition is to document the divergence and close.

## The record -- commit message(s)

### commit `0447c2ec 2026-08-20`

```text
mrwstore2 REPRODUCED at rung 3 -- and three of its own claims are measured false, including one that was also in the source

The defect is real.  The severity argument that put it top of a cluster is not.

THE WITNESS: unmodified in-tree `testppc`, cold debugger, real decode, real
memory_rw.  A PPC guest sets DBAT0 over a 128 KB window, enables MSR[DR], and
executes `stw r6,0(r5)` with r5 = 0x1201fffe -- unaligned, crossing the 1 KB split
granule.  Head reaches the in-tree `fb` device; tail has no BAT and no PTE, so a
real DSI fires; a planted `rfi` is the GUEST'S OWN restart.  ONE architectural
store, FOUR device writes -- and the trace is from a FULLY STOCK HEAD BINARY with
zero instrumentation.  Liveness, device-signature and negative controls all green.

CLAIM 1 -- "not introduced by #430" -- MEASURED FALSE.  Built from
`2458cfb^:src/cpus/memory_rw.c`: no exception, no restart, ONE device write.
Pre-#430 the tail was silently mis-applied to the physically-following location --
the defect #430 fixed -- so there was nothing to restart.  #430 CREATED the fault.

CLAIM 2 -- "the memblock split has had this property all along" -- MEASURED FALSE
twice.  Post-#430 it can only fire on PHYSICAL accesses, and its head can NEVER be
a device in either version because device dispatch `goto do_return_ok`s first.

CLAIM 3 -- "256x" -- MEASURED WRONG: it is 1024x.  MRW_SPLIT_MASK is 0x3ff, so
1 MB / 1024 = 1024.  The 256 came from comparing 1 MB to a 4 KB page -- the granule
this split does not use, as the comment fifty lines above says explicitly.

*** THE SAME WRONG NUMBER WAS ALSO IN THE SOURCE. ***  memory_rw.c's own comment
read "one boundary in 256".  ONE mis-derived constant became TWO records defects,
and the ledger row repeated it as a severity argument.  Both corrected here, with
the derivation written down so the next reader can check it rather than trust it.
The two measured properties of the memblock split are recorded in the same comment,
because a row asserted the opposite of both.

REACHABILITY IS FAR NARROWER THAN THE ROW IMPLIES, which is why it re-ranks DOWN:
ONLY PowerPC can emit a straddling store -- MIPS, ARM, SH, M88K and Alpha all
force alignment, each checked in source -- and PPC is the only family whose
device-failure arm can restart.  THREE REAL GUEST BOOTS (OpenBSD/pmax to root
login, OpenBSD/luna88k to login:, NetBSD/macppc to the root prompt) emit ZERO
straddling stores from guest code.  The seat first read macppc's 95 split writes as
guest activity and REFUTED ITSELF by logging the addresses: all len=65536 at
pc=0x0, the ELF loader running before any guest instruction.  Of 1024 offsets only
ELEVEN can start a straddling access, and the head always lands within 7 bytes
below a 1 KB boundary -- so a register at offset 0x00/0x10/0x20 can never be one.

*** AND THE FIX MAY ITSELF BE WRONG. ***  Partial completion with restart
re-applying the first part is what real PowerPC hardware does, so gxemul may be
CORRECT and a fix may introduce a divergence.  There is no PowerPC manual in
_scratchpad/ -- ARM, MIPS and m88k only -- so that is recorded as REASONING, NOT A
CITATION, the same trap CLAUDE.md records for SH.  Obtain a manual before editing.

memory_rw.c is shared: the correction landed byte-identical in est/ and in build/.
Comment-only, so no rebuild is needed for correctness.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
```


## Questions -- verdict line first

1. Does the record contradict itself -- two numbers for one quantity, a total its parts do not sum to, a claim one
   paragraph makes and another undoes, or the ledger row saying something the commit message does not?  Quote both.
2. Which claims are stated as MEASURED but cite no artifact (a log, a file under regress/artifacts/)?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the record's own evidence covers less?
4. What would a reviewer checking this record against its artifacts most likely find wrong?
When you count items the record enumerates, list them by name before giving the count.

End with one line: `HARNESSREC_MRWSTORE2: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBHRECMRWSTORE2: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
