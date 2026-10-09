# NEW ROW -- **PRIVILEGED GUEST `MSR` IS PROCESS DEATH.**  You found it; now scope it.

## VERDICT LINE FIRST.  TREE: `GXEMUL-SEC/src/` (ignore the three pristine-2021 `src/` at the project
## root).  **DO NOT RATIFY** -- every premise below is YOUR OWN claim and §S4 asks you to break it.

## S1 -- PROVENANCE: THIS ROW DOES NOT EXIST YET, AND YOU ARE THE REASON IT SHOULD

While refuting a brief that had mis-attached five sites to `armthumbabortkill`, you found a
SEPARATE defect and said so under the standing license (*"if while verifying a claim you found
something ELSE -- say so"*).  Verbatim:

> *"**Load `:606` is HIGH**, and it is **worse** than the Thumb row: privileged guest `MSR` is
> **process death**, not `running = 0`.  A previous reading of this file already said so
> (`grok_armhalts_20260917.txt`).  It is not `armthumbabortkill`, and member 1 DELETE is the wrong
> member."*

and:

> *"Of the five `exit(1)` sites it then asks about, only the two register-bank `default:` arms are
> guest-reachable, and they are process death via privileged `MSR` / exception-return -- not member
> 1 DELETE, and not UND.  The other three are not guest-reachable.  `arm_cdp` does not transfer.
> `:621` is not a de-fatalisation."*

and on reachability:

> *"That is a guest instruction through real decode.  `USR32` cannot do it; boot is not USR32.
> Thumb on SA1110 has no `MSR`.  Gate 14 never feeds this encoding."*

**Note the last clause: GATE 14 NEVER FEEDS THIS ENCODING.**  358 real-decode checks across three
ARM machines, and none of them reaches it.  That is a gate blind-spot, which this project ranks
queue items by.

The two sites (fork line numbers, verbatim):

```c
/* :559-562  arm_save_register_bank() */
	default:fatal("arm_save_register_bank: unimplemented mode %i\n",
		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
		exit(1);
	}

/* :606-609  arm_load_register_bank() */
	default:fatal("arm_load_register_bank: unimplemented mode %i\n",
		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
		exit(1);
	}
```

## S2 -- SETTLED PREMISES (re-inlined; do not re-derive)

* **`fatal()` DOES NOT EXIT.**  `debug()` has an early-out (`if ((quiet_mode && !ss) || v < 0) return;`);
  **`fatal()` has none** and goes straight to `va_debug`.  The `exit(1)` on the next line is the kill,
  and `fatal()` cannot be silenced by `-q` -- which is why a guest-drivable one needs a LATCH, not a
  verbosity flag.
* **THE OPTION SET HAS SEVEN MEMBERS:** 1 DELETE - 2 DECLINE (silent) - 3 DECLINE + LATCHED ANNOUNCE -
  4 ACCEPT - 5 FAULT - 6 BACKED ACCEPT - 7 IMPLEMENT.  **Before choosing, CHECK THE MEMBER IS
  AVAILABLE ON THIS CPU** -- member 5 works on MIPS/M88K because `memory_rw` dispatches an exception
  on a failed DEVICE access, and there is no Alpha equivalent.  **You already ruled that `arm_cdp`'s
  UND precedent does NOT transfer here**, so do not re-argue it -- say what DOES.
* **THE HOUSE LATCH IDIOM** is `N = 1`, per instance, plus a suppression marker in the message text.
  A 2026-09-17 census measured **80 markers / 12 files / 13 spellings**, `(once)` being 41 of 80.
  **Do not quote those numbers back; run the deriver if you need them.**

## S3 -- THE QUESTIONS

**Q1. WHICH MEMBER, PER SITE, AND WHAT DOES THE GUEST SEE AFTERWARDS?**  These are CPU-core sites
with a `default:` on a mode the emulator does not model.  Save and Load are not symmetric -- Save
discards state, Load FABRICATES it.  **Does one member fit both, or do they differ?**  If the answer
for Load is "there is no correct value to load", say what the least-wrong behaviour is and why.

**Q2. IS IT ONE ROUND OR TWO?**  The reopening rule: a round takes ONE site; a second joins only if
it is witnessed, in the SAME file and SAME semantic class (so one fix design covers both), and
covered by the SAME detector with no new oracle.  **Do these two qualify as one round?**

**Q3. THE WITNESS, and you have already said it is CHEAPER than the Thumb one.**  Name it concretely:
which machine, which privileged `MSR` encoding, which reserved mode value, what the probe observes.
**A host that calls `exit(1)` produces a DEAD EMULATOR -- what does the probe read to tell that apart
from a normal exit and from a crash?**  Name the channel; a row whose channel cannot vary under its
mutant is vacuous by construction.

**Q4. THE DE-ESCALATION COST.**  If the fix removes a host-fatal guard, it DELETES THE ACCIDENTAL
TRIPWIRE that made guard growth self-announcing: before, an unmodelled mode meant `exit(1)` on the
first write -- unmissable; after, it means a silently refused one.  **So the detector owes ACCEPT
ROWS pinning that LEGAL mode writes still land.**  Enumerate them from the diff: which modes are
modelled, which adjacent value carries the accept row, and **can a guest store actually leave that
value in the predicate's OPERAND?**  (Read the store arm and cite it -- write-1-to-clear, read-only
and never-set bits cannot carry an accept row, and one round here shipped a guest that *did* write
the bit while the store arm filtered it before the predicate ever saw it.)

**Q5. SEVERITY AND RANK.**  Is this HIGH?  **Rung measures reachability-proof strength, NOT harm** --
a witness makes an item ELIGIBLE, and SEVERITY plus GATE BLIND-SPOTS order the queue.  You say gate
14 never feeds the encoding.  **Rank it against the Thumb row and say which should run first.**

## S4 -- *** BREAK YOUR OWN FINDING. ***

> **"Privileged guest `MSR` reaches `:606`" is a REACHABILITY claim, and this project's own record is
> that reachability claims are where it goes wrong.**

Name what would refute it.  In particular: is there a MASK, a mode-validity filter, or a decode
guard between the guest's `MSR` and the `default:` arm that would stop a reserved mode value ever
landing in `cpsr & ARM_FLAG_MODE`?  **One round here had a guest that genuinely wrote the offending
bit at the interface and the store arm filtered it before the predicate saw it** -- the finding
looked identical to this one and was wrong for exactly that reason.

**Trace it instruction -> CPSR write -> mode field -> the `switch`, and cite each step.**  If the
path is clean, say CONFIRMED and show the chain.  If a filter exists, this row does not survive and
I would rather learn that now than after building a probe for it.
