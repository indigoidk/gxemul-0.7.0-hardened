# PASS 1 DESIGN BRIEF — `gdromexitsix` **Round 2**: the two remaining `exit(1)`s, and the oracle they re-key

> ### *** THIS BRIEF WAS SENT WITH THREE DEFECTS.  THEY ARE CORRECTED HERE RATHER THAN
> ### SILENTLY EDITED, BECAUSE THE SEATS ANSWERED THE SENT VERSION.  Found independently by
> ### the fable and grok seats; the third by fable alone. ***
>
> **(1) "Round 1 shipped (`#489`)" IS FALSE.**  `#489` was UNCOMMITTED when this went out —
> HEAD was `84765ec` (`gdromwarnbits`), `dev_dreamcast_gdrom.c` was dirty, the 13-row
> detector was untracked, and its kill table was still running.  The SUBSTANCE held (the
> detector was 13/13 green and the table's base row reproduced it), but "shipped" is a state
> claim and it was wrong.  *Load-bearing, as grok noted: had the table redded, §1 would have
> been false and everything downstream would have inherited it.*
>
> **(2) `:409` AND `:486` ARE TWO-GENERATIONS-STALE CITATIONS.**  They are the `exit(1)` line
> numbers at rev `5b5089d`.  The live sites are at **`:574`** (the `case 0x30` data-format
> check) and **`:654`** (the `default:` arm) — Round 1's own comment insertions moved them by
> ~170.  **This is the FIFTH generation of numbered-citation drift on this one file**, whose
> own committed probe header says in capitals: *"DO NOT RE-NUMBER THEM — GREP FOR THEM."*
> Cite these as grep anchors: `unimplemented data format` and `unimplemented command`.
>
> *Worse than untidy: the brief's own wrong-tree heuristic says "if your line numbers disagree
> with mine by hundreds you are reading a pristine copy" — and a seat reading the CORRECT tree
> sees +170.  The heuristic would have misdirected a correct seat.*
>
> **(3) §4's "it goes green for a new reason, which is worse" OVERSTATES THE DAMAGE, and both
> flagship seats refused it.**  NONE of `gdrompionull`'s 13 rows sends a mis-built packet, so
> the `exit1` mapping is a validation **FRAME**, not a row.  After de-fatalising both sites all
> 13 rows pass identically and nothing about them changes.  What weakens is the HEADER'S CLAIM
> — and that claim was **already false**, since birth, for two single-bit flips off the probe's
> own correct bytes (`cmd[0]` 0x30→0x70 hits the IMPLEMENTED mount arm; `cmd[1]` 0x20→0x24
> warns and continues).  **Corrected in `gdrom_pio_null_probe.py` on 2026-08-28.**
>
> *That third one is the useful correction: I claimed the wrong failure mode in one direction
> and missed a real one in the other.*
>
> ### *** (4) A FOURTH DEFECT, AND IT IS THE MOST REPEATABLE ONE: THE PACKET NEVER CARRIED
> ### THE `fatal()` PREMISE, AND TWO PACKET-FED SEATS BLOCKED ON EXACTLY THAT. ***
>
> `grep -c 'RETURNS' brief_sent.packet.md` returns **0**.  This packet went out without the
> settled-premises block.
>
> *** MY FIRST ACCOUNT OF THIS SAID THE BLOCK WAS IN "#489's PASS-2 BRIEF".  THAT IS WRONG,
> AND THE ADJUDICATOR CORRECTED IT — THE CORRECTION MAKES THE FAILURE WORSE, WHICH IS WHY IT
> IS RECORDED RATHER THAN QUIETLY FIXED. ***  There is no `#489` pass-2 packet; its kill table
> was still running.  The block is **section 4c, "PREMISES ALREADY SETTLED, RE-INLINED SO
> NOBODY SPENDS AN ANSWER RE-DERIVING THEM"**, in `_scratchpad/panel_20260827_222110/
> brief_sent.md` — **`#489`'s PASS-1 design brief**.  Its own preamble reads:
>
> > *"The previous round lost three seat-answers to facts it had settled and then failed to
> > carry into the packet.  So, stated here:"*
>
> **So the remedy was INVENTED on 08-27 from `#488`'s loss, APPLIED CORRECTLY that evening at
> 22:21 — and DROPPED at 11:55 the next morning, by the same author, in the very next brief of
> the same campaign.**  Fourteen hours from minting to breaking.
>
> *That is the frozen-copy signature exactly, and it is a far stronger argument for structure
> than "I filed it in the wrong place" was.  The carrier's own diagnosis applies verbatim:
> knowing a rule and having it fire on the right object are different problems, and only the
> second is solved by writing more.*
>
> **minimax:** *"the biggest is `fatal()`'s exit-behaviour — without it, the entire
> de-fatalisation mechanic is unanchored."*
> **deepseek:** *"UNCHECKABLE ... assumes `fatal()` does not exit.  If `fatal()` exits, then
> `0x24` is also fatal and the asymmetry disappears.  Single fact needed: definition of
> `fatal()`."*
>
> Both are correct and both are my fault.  The fact is settled and old: `debug()` has an
> early-out (`if ((quiet_mode && !ss) || v < 0) return;`) and **`fatal()` has none** — it
> goes straight to `va_debug` and RETURNS.  That is why a guest-drivable `fatal()` needs a
> latch and not a verbosity flag, and it is the premise the entire round rests on.
>
> **THIS IS THE SECOND MEASURED INSTANCE OF THE SAME CLASS IN ONE WEEK.**  `#488` queued
> exactly this as a rule question for the flagship seat — *should a packet be REQUIRED to
> re-inline every premise an earlier pass settled?* — after three packet-fed seats there
> refused to ratify for the same reason.  It has now happened again, on a sibling round in
> the same file, with the author who filed the question.
>
> *Knowing a rule and having it fire on the right object are different problems.  Two
> instances is the argument for a BRIEF-TEMPLATE LINE rather than prose — the brief is the
> artifact present at the moment of decision, which this project's own finding says is the
> one place prose demonstrably works.*

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A panel this morning found **four wrong premises** in my brief; one seat led with a defect in
the packet itself. **Check the premises, not just the derivations.** A seat that re-derives a
fact from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are THREE pristine-2021-upstream copies
of GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).
They are NOT this fork. If your line numbers disagree with mine by hundreds you are reading
one of them — say so rather than reconciling.

**If you cannot read files that is expected** — every fact you need is inlined, including the
whole enclosing function. Name any premise you cannot settle from this packet rather than
guessing at it.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 0. THE QUESTION THIS ROUND EXISTS TO ANSWER

Two guest-reachable `exit(1)` sites remain in `handle_command()` after Round 1. Both are
"unimplemented" declines rather than bounds guards. **But de-fatalising them DESTROYS the
oracle of a committed, gated detector** — and that detector is how another round proves its
own packets are well-formed. *That* dependency, not the fix itself, is the hard part.

## 1. STATE OF PLAY — what Round 1 already settled

* **Round 1 shipped** (`#489`): `case 0x14`'s TOC length guard now declines with a latched
  `(once)` diagnostic instead of `exit(1)`. Guest-controlled, rung-3 witnessed, 13-row
  detector.
* **`:662` IS NOT GUEST-REACHABLE and KEEPS its `exit(1)`.** Its `cmd_count >= 12` predicate
  is unsatisfiable. Not in scope.
* **`:701`/`:761` belong to the open `gdromcondlies` row**, whose design already exists.
  Not in scope.
* So the remaining two are **`:409`** (the `case 0x30` data-format check) and **`:486`**
  (the `default:` arm).

## 2. THE TWO SITES, VERBATIM

### SITE A — the `case 0x30` data-format check

```c
	case 0x30:
		/*  Read sectors.  See NetBSD gdrom_read_sectors().  */
		if (d->cmd[1] == 0x24) {
			fatal("GDROM unimplemented data format 0x%02x. Continuing anway.\n", d->cmd[1]);
		} else if (d->cmd[1] != 0x20) {
			fatal("GDROM unimplemented data format 0x%02x\n",
			    d->cmd[1]);
			exit(1);
		}
		sector_nr    = d->cmd[2] * 65536 + d->cmd[3] * 256 + d->cmd[4];
		sector_count = d->cmd[8] * 65536 + d->cmd[9] * 256 + d->cmd[10];
		...
```

**PREMISE TO CHECK, and it is the interesting one: the file has ALREADY DECIDED that an
unimplemented format is survivable — for `0x24` only.** `0x24` warns and **falls through to
read sectors as though the format were `0x20`**. Every other non-`0x20` value ends the host.

I do NOT think that asymmetry is a reasoned design. It looks like *whichever value the author
happened to hit while developing against one driver*. **But that is a guess about intent and
I want it challenged.** If `0x24` continuing is correct, why is `0x25` fatal? If `0x24`
continuing is a BUG, this round may be widening a defect rather than fixing one.

### SITE B — the `default:` arm

```c
	default:fatal("GDROM handle_command: unimplemented command 0x%02x"
		    "\n", d->cmd[0]);
		exit(1);
	}
```

## 3. THE WHOLE ENCLOSING FUNCTION'S TAIL — inlined, because a proposed edit is a sketch

*A recent round had FOUR independent readers propose the same `return` into a function whose
common tail none of them had read; it would have handed a guest an untouched buffer.*

```c
	}   /*  end switch  */

	/*  Any resulting data? Then set COND_DATA_AVAIL. Otherwise clear it
	    and set count to zero.  */
	if (d->data != NULL) {
		d->cond |= COND_DATA_AVAIL;
	} else {
		d->cnt = 0;
		d->cond &= ~COND_DATA_AVAIL;
	}

	if (d->cnt == 65536)
		d->cnt = 32768;

	SYSASIC_TRIGGER_EVENT(SYSASIC_EVENT_GDROM);
}
```

`free_data()` runs at the TOP of `handle_command()`, so on entry to any arm `d->data == NULL`
and `d->data_len == 0`. A `break` from either site therefore reaches the tail's else branch:
`cnt = 0`, `COND_DATA_AVAIL` cleared, **and `SYSASIC_TRIGGER_EVENT` still fires** — "the
command produced no data", reported properly. An early `return` would skip that event and
hang the guest.

`case 0x30` already ships that `break` idiom twice for its own guards (grep this file for
`OB-20: was exit(1)`), and Round 1 added a third at `case 0x14`.

## 4. *** THE DEPENDENCY, AND IT IS THE REASON THIS ROUND IS NOT A SWEEP ***

`regress/artifacts/gdrompionull/gdrom_pio_null_probe.py` is a COMMITTED, GATED detector
(gate `gdrompio`, 13 rows, wired in `gate_sh_rounding.sh`). Its oracle, quoted verbatim from
its own header:

> ```
>   sig11  = the deref                    (the defect)
>   exit1  = some guarded refusal          (a mis-built packet, NOT the defect)
>   exit0  = survived and quit cleanly
> That distinction is what makes "died" evidence here.  It also validates the
> hand-assembled packet for free: a wrong cmd[0] lands in handle_command's
> `default:` arm and a wrong cmd[1] in the 0x30 arm's format check -- both
> exit(1) -- so a coding error CANNOT be mistaken for the defect.
> ```

**Those two arms are EXACTLY the two sites this round de-fatalises.** After the fix, a
mis-assembled packet DECLINES instead of dying — so that probe silently loses its ability to
tell "my packet was wrong" from "the packet was right and the device behaved". It does not go
red. **It goes green for a new reason**, which is worse.

*Note the shape: this is not a detector that breaks. It is a detector whose EVIDENCE VALUE
quietly drops while every row still passes.*

## 5. THE ORDERING RULE THIS TRIGGERS, and the alternative one seat proposed

This project's **ORACLE-CORRECTION RULE** says: when a shipped oracle pins something the code
change invalidates, **re-pin the oracle FIRST, measure the COMMITTED build RED under the new
expectations, and only THEN change the code** — because re-pinning after the fact is
observationally identical to fitting the test to the binary.

**But a seat argued on Round 1's pass 1 that the oracle-correction rule does NOT apply here,
and I think it may be right.** Its position: this is not an expectation CORRECTION (the old
pin was never wrong), it is oracle STRENGTHENING. Its proposed order:

> assert the failure; show the correct probe GREEN; flip `cmd[0]` and `cmd[1]` independently
> in probe MUTANTS and show those RED; then de-fatalise and show the SAME mutants STILL RED.

If that works, the packet-validation property survives on a channel that does not depend on
the host dying — and requiring the unmodified product to go RED would be inappropriate,
because nothing about the old pin was false.

**QUESTION 1 (the round's main design question): which order governs — CORRECTION or
STRENGTHENING? And what is the replacement channel?** If a mis-built packet no longer kills,
what observable distinguishes it from a well-built one? Candidates I can see, none verified:
the new decline diagnostic's text; `COND_DATA_AVAIL` state; the absence of TOC bytes. Say
which and why.

## 6. THE OPTION SET — four members, and I want the fourth argued

Per this project's de-fatalisation rule the set is **delete / decline / decline +
bounded-announce / accept**, and a fourth-member ACCEPT is real (the footbridge `+0x188`
case: the model already computed the right value and then killed the host over it).

| site | delete | decline+latched announce | accept |
|---|---|---|---|
| `:409` | ? | the house idiom | ? — is `0x24`'s existing fall-through the accept precedent? |
| `:486` | pass 1 called bare removal SAFE here | ? | no |

**QUESTION 2:** For `:486`, pass 1 established that falling through to the common tail is
already CORRECT behaviour for an unhandled command. Does it then need a diagnostic at all, or
is a silent decline right? A guest scanning the command space would otherwise produce a
LATCHED message per instance — is that worth having?

**QUESTION 3:** For `:409`, is a decline correct, or does continuing (the `0x24` treatment)
better model the hardware? One pass-1 seat objected that deleting `:409`'s exit *"yields
invented success rather than corruption"* — the guest asked for a format we do not implement
and would be handed `0x20` data as though it were what it asked for. **That is a correctness
argument AGAINST the `0x24` precedent, and it applies to `0x24` today.** Is `0x24`'s
fall-through itself a defect this round should file?

**QUESTION 4:** Is this ONE round or TWO? The round-scope rule allows a second site only if
it is in the SAME semantic class under one fix design and covered by the SAME detector with
no new oracle. `:409` and `:486` are both "unimplemented, decline" — but they differ in
whether a decline INVENTS SUCCESS (`:409` continues into a real read; `:486` does not).

**QUESTION 5 — THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES.** Assume a detector
along Round 1's lines. Be adversarial and concrete.

## 7. WHAT I BELIEVE, SO YOU CAN ATTACK IT

* The two sites are one round, because one decline design and one detector cover both.
* `:409` should decline, not continue, and `0x24`'s fall-through should be FILED as a
  separate correctness question rather than fixed here.
* The gdrompionull oracle needs STRENGTHENING, not correction, and the replacement channel
  is the decline diagnostic's text.
* Each site gets a latched `(once)` announce, since a guest scanning the command space is
  precisely the flood case latches exist for.

**Every one of those is a guess. Please break the ones that are wrong.**
