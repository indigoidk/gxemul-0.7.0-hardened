 on the once row. For the INTSTAT-label pre-set to be caught, a session needs: accepted access at +0x10, THEN a refusal, with a once-count row. In the istat session the lw at +0x10 is post-refusal. In the rearm session, post-first-refusal. So indeed invisible IF no other session.

Also — what about the ORDER within the istat session: the loop body — could the accepted lw at `off` come BEFORE the refusals? The rows: cause 0 = pre ("IP2 low after SOFTINT's default-arm store"), causes 1-4 = the refused cells, cause 5 = ctl ("CONTROL: accepted lw +0x%x reasserts"). Since cause 5 is the accepted lw's print and it's LAST, the lw is after all refusals ✓ (as I said).

Now — hold on, I realize I should double check one thing: the istat session's refusals are "lb, sb, lh, sh"? Rows: "%s lb" (cause 1), "%s sb" (cause 2), "%s sh" (cause 3), "%s ctl" (cause 5) — and cause 4? The v0 rows: a0 (lb), a1 (lh). So there are FOUR refusals: lb, sb, sh, lh — with lh's cause print at index 4. And "%s once" = "4 refusals at +0x%x, then +0x07: one notice" — 5 refusals total (4 at the label + lb +0x07). OK consistent.

Alright — so candidate GAP #1: pre-set keyed to the INTSTAT case label. Edit: in `DEVICE_ACCESS(crime)`, in the register switch, change

```c
	case CRIME_INTSTAT:	/*  0x010, Current interrupt status  */
	case CRIME_INTMASK:	/*  0x018, Current interrupt mask  */
```
to
```c
	case CRIME_INTSTAT:	/*  0x010, Current interrupt status  */
		d->warned |= CRIME_W_LEN;
	case CRIME_INTMASK:	/*  0x018, Current interrupt mask  */
```

This sets the latch on every ACCEPTED access at INTSTAT. For it to show, a session must make an accepted access at +0x10 before its first refusal; from the inlined rows, every accepted access at +0x10 (istat ctl lw; rearm KINDS lw 0x10) happens after that session's first refusal, so every once-count still reads 1 → 121/121.

BUT — caveat: I haven't seen all 121 rows (the warm session, the free-run, devsig, acc4, sh08, sb08, keeps sessions' full code, the six-width sessions). One of them might do an accepted +0x10 access first. Hmm. The six-width sessions ("<op> surv"): each width's own session — a refused access then...? "sb08 run" — the sb 0x01 at CONTROL then run. Hmm, the sb08 session: `sb 0x01 +0x08` (refused), then a run (v1 = LIVE_VAL roundtrip?). No +0x10.

What about "acc4 rhi/rlo/wlo/whi" at +0x30 — no. "devsig" at +0x00 — no.

"warm v0": accepted reads of a nonzero register. If the warm session reads INTSTAT accepted-ly... Let me think about which register the warm session uses. The warm session dates to the 40-row era (codex, F2). At 40 rows, what registers were seeded nonzero? The 40-row test: REV 0x11 (prelude always writes it). "accepted reads of a nonzero register" — REV is always nonzero (0x11) — a natural choice: read REV accepted (lw/lh at +0x00), then a refused read (lb at +0x07?) answers 0. Hmm — if warm's accepted reads are at REV, then the REV-arm pre-set... wait, the REV arm pre-set (c2_pre_rev) was caught via the ADDED lw at +0x00 in latch x5's prologue. If warm already read REV pre-refusal, the glm finding ("no counted session reached the REV arm before its first refusal") would be false — glm MEASURED c2_pre_rev passing the 111-row test. So warm's accepted reads are NOT at REV (else the REV arm would have been reached pre-refusal in a counted session and c2_pre_rev would have been caught at 111). Good — so warm's accepted reads are at some other nonzero register: DOG? At 111 rows DOG held 0 (the dog seed was added in repair 6 — "with DOG at 0 a decline answering the register read 0"). So not DOG at 111. INTSTAT/INTMASK at 111: seeded 0x10000000 (BIT) in the IRQ sessions — but warm is a separate session; INTSTAT in warm's session = SOFTINT|HARDINT = 0 (no SOFTINT store in warm) → 0. +0x278 (far slot): the warm session is 40-row era; the top/far slot rows came later (85-row era, "hi"). TIME: nonzero! TIME advances (66-990) — an accepted ld at TIME reads nonzero ("time lb/sb/lh/sh ctl (an accepted ld moves TIME)"). Hmm, "warm once (sd first) and time once (ld first)" — the TIME session's first access is an accepted ld at +0x38! So TIME holds a nonzero value after any access (crime_update_crime_time on every TIME access... well, on accepted accesses at TIME the arm calls update). Hmm — actually TIME is updated only when the arm runs (accepted accesses at 0x38). Initially d->reg[CRIME_TIME] = 0? The first accepted ld at TIME: the arm runs crime_update_crime_time(d) → sets TIME to the host-clock-derived value → odata = the updated value → nonzero ✓. So warm's "accepted reads of a nonzero register": plausibly TIME (accepted ld(s) at +0x38 → nonzero), then a refused read answers 0. If warm's accepted reads are at TIME, then no +0x10. 

Alternatively the warm session could read the far slot (+0x278 seeded)... the warm session predates the far-slot rows? "warm v0, warm once (the codex seat, F2)" — F2 = 71-row era? "the codex seat, F2" — so warm existed by 71 rows. Far slot rows: "hi"