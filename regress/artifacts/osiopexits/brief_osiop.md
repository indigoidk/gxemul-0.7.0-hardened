# `dev_osiop.c` -- the largest single concentration of unowned host kills, on a machine this project boots

Nonce: `CODEX_OSIOP_20260910`. Open with `VERDICT:` naming which of the sites you would file, in priority
order, then echo the nonce.

Ordinary robustness triage on a SCSI controller model in an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under the
project root. **Verdict line first.**

**Please do not simply ratify.** Six briefs of mine this week had premises or proposed repairs corrected
by a seat that opened the file, and every correction improved the round. **Check the premises.** In
particular the site list below came from an earlier census of yours and I have re-derived none of it.

## WHY THIS FILE

A census this morning enumerated **76 guest-reachable error-exit sites across 24 files that own no
tracker row**. `dev_osiop.c` is the largest single concentration at **fourteen**, ranked I2/E3 --
"MVME187 SCRIPTS execution and controller accesses", effort E3 because "preserve command termination,
status, and interrupt behavior".

The enumerated lines were **406, 411, 419, 426, 656, 668, 715, 727, 791, 821, 825, 830, 870, 1152**.

**The machine matters here.** `machine_mvme88k.c` attaches this controller on MVME187, the same machine
whose clock chip I fixed today (`#521`) and whose PCC2 timer this project has been running rounds against
all week. It is a live, exercised machine on an architecture where the memory layer CAN deliver a bus
fault, which most of this queue cannot use.

## WHAT I WANT

**Not fourteen rows.** Eight real rows beat twenty padded ones, and an E3 group needs splitting by what a
fix would actually have to preserve, not by line number.

## THE QUESTIONS

1. **RE-DERIVE THE SITES at HEAD.** Are those fourteen lines still the exits, and are they all
   `exit(1)`? Give the grep anchors rather than line numbers -- line numbers decay here and anchors do
   not.
2. **SPLIT THEM BY REACHABILITY, and this is the part that decides the filing.** Three populations,
   counted: **(i)** reachable by an ordinary guest register access or by SCRIPTS execution the guest
   started; **(ii)** reachable only through a state the model itself can never construct; **(iii)**
   internal consistency failures where continuing would be worse than stopping. **Population (ii) and
   (iii) are RESULTS when recorded with their warrant** -- a dead path named with its reason stops the
   next round re-finding it -- so list them separately rather than dropping them.
3. **GROUP POPULATION (i) BY WHAT A FIX MUST PRESERVE.** The audit's own E3 reason is that command
   termination, status and interrupt behaviour have to survive a decline. So: which sites can decline
   with no state obligation at all, which owe a status write, which owe an interrupt, and which owe a
   completed command handshake? **That grouping IS the round split.**
4. **FOR THE TOP TWO, give the smallest honest fix**, the option-set member from {delete, silent decline,
   decline + latched announce, accept, fault, backed accept, implement}, and whether that member is
   AVAILABLE here. Note this is M88K, so the memory layer's failed-device path exists -- but a present
   controller refusing one register is not an absent device, and a recent review ruled FAULT out on
   exactly that ground for two other sites. Say whether the same reasoning applies.
5. **WHAT WOULD YOU NOT FILE, and why?** A row for a path nothing reaches competes with real work in a
   queue of this size.
6. **IS THERE A GUEST THAT DRIVES THIS AT ALL?** The tree's OpenBSD/mvme88k story is that the kernel is
   downloaded externally rather than shipped, so I do not know whether any in-tree workload touches the
   controller. **If the honest answer is that nothing in-tree reaches it, say so** -- that changes the
   severity of every row here and is worth more than a ranking.
7. If you found something else, say so.

Read-only: no builds, no probe runs, no edits, no patches. Prose and tables only.
