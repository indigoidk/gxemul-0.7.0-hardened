FABLE_SEAT_ALIVE_20260918_541P1
claude-fable-5-1 | "# CHECKPOINT -- 2026-09-18 22:4x   HEAD: cdbe7d7 #537 fbsmlane: #442's harness printed a verdict token its own self-mutant lane could never read -- the lane runs, pinned on R3"
VERDICT: 4 + latch -- ACCEPT (keep the arm's identity result, drop exit(1), latch the fatal once per CPU); the neighbour measurement shows this is what the rest of the identity window ALREADY does, and it is the only member that removes all three host-death cells in-round rather than relocating the fetch death to cpu_dyntrans.c:729-733.

# alphavmkill (#541) pass 1 -- Fable 5 seat, adjudicating the disposition

**How I worked.**  Read-only; this file is the only write.  Read the packet, `brief_sent.md`, `opus5_p1.md`,
`codex_adv541p1.txt`, `kimi.txt` (through its landed conclusions), the site (`memory_alpha.c:60-96`, `:192-199`),
the two death paths (`cpu_dyntrans.c:700-749`, and the load/store abandon via `memory_rw.c:245-259`), the
verbosity model (`debugmsg.c` + the carrier's `-q`->ERROR rule), and both measurement receipts
(`alphavmkill/neighbours_20260918/RESULT.out`, which carries Session A neighbours AND Session B alphaifetchkill).
I settled H9's three facts by reading the code and both seats' landed text, not by weighing.

## Q1 -- MEMBER 4 + LATCH.  The measurement decides it, not the seat count.

**The discriminator, stated to bind the next "tripwire in an identity window":**

> **When a guest-fatal tripwire sits inside a decode/translate arm, the fix is the disposition the arm ALREADY
> applies to the rest of its window, with any TRUE announcement latched.**  This arm identity-maps its ENTIRE
> `!userMode && base == 0` window (`memory_alpha.c:73-90`); every address but this one returns 2 with an identity
> paddr.  So the arm's established disposition is ACCEPT, and member 4 extends it to the one hole.  DECLINE is correct
> only where the arm's own window is decline/unmapped -- a lone DECLINE inside an ACCEPT window makes that address the
> sole anomaly, and here it additionally RELOCATES the death to the fetch path.

This is the footbridge `+0x188` ruling generalised: there the arm already computed the right value, so ACCEPT-keep-
value; here the arm already identity-accepts, so ACCEPT-identity.  Both say *match the arm's own policy for the
window*.

**The measurement is what tips this from the 7-seat position, and it must be read as doing exactly that.**  Seven
seats chose member 3, and codex_adv named its reason honestly: it could not confirm member 4's FETCH survives from
its four-file scope (*"whole-FETCH survival is unsettled ... the physical-memory helper is outside the permitted
files"*).  The neighbour run settles precisely that gap, on the committed binary, with no build:

- **LOAD** `0xfffffffd80000008` -> `0x0`, next instruction ran (`mark 0x1234`);
- **STORE** -> dropped, next instruction ran (`mark 0x5678`);
- **FETCH** `0xfffffffd80002000` -> `[ Alpha PALcode 0x0 unimplemented! ]`, `All machines stopped`, process ALIVE,
  clean exit (wait 0).

That is member 4's derived behaviour, already happening at VMKILL's neighbours in the same identity window.  Member 4
makes `0xfffffffd80000000` behave like `+8` and `+0x2000`; it adds no code path.  **codex_adv's caution was right on
its evidence and is removed by the measurement** -- which is the carrier's "disagreements are settled empirically,"
so I rule on the measurement, not by overruling seven considered votes on their own packet.

**Session B confirms the cost of member 3:** an armed JMP to a raw VA dies at `cpu_dyntrans.c:729-733`
(`could not find physical` 1, FATAL, wait 256).  A DECLINE at VMKILL returns 0, so a FETCH there takes exactly that
path and the host dies.  **Member 3 does not fix the defect -- it converts a load/store host-kill into a fetch
host-kill** and hands that cell to `alphaifetchkill`, whose fix is NOT a one-liner (H8).  For a fork whose whole
purpose is "no guest-drivable host death," leaving a host death outstanding and dependent on a hard, unscheduled fix
is the worse outcome.  Member 4 closes all three cells now, independent of `alphaifetchkill`.

**Being at least as hard on my own leaning: member 4's real costs, disclosed, none decisive.**
- **A per-access `non-existant paddr` WARNING** that member 3 avoids.  Member 4 lets translation SUCCEED (return 2),
  so `memory_rw` reaches the past-`physical_max` path (`:663`) and `memory_warn_about_unimplemented_addr` fires; a
  DECLINE fails earlier (`:259`) and never warns.  It is `VERBOSITY_WARNING`, so **`-q` silences it** (the carrier's
  `-q`->`VERBOSITY_ERROR` rule) but it **shows at default and `-V`** and is **unlatched (per-access)**.  This is the
  7 seats' strongest point and it is real; it does not flip the decision because it is verbosity-gated, the whole
  window already emits it, and a tripwire is not a hot path -- only a pathological looping guest floods it, and even
  then member 3's alternative is an actual host death.  **Disclose it in the contract.**
- **The STx_C success-lie** (Opus, derived): a dropped store under member 4 reports success and STx_C sets status 1.
  But member 3's abandon leaves STx_C's status non-deterministic; neither is correct (the store is lost either way),
  and there is no correct behaviour here, so this favours neither.  Disclose.
- **Neither harms guest state:** `0x3fd80000000` is ~4 TB, past RAM on every realistic `-M`, so the dropped store
  corrupts nothing.  (Opus finding #2 -- a 40-bit alias into real RAM at `-M` >= ~1038849 MB -- is a PRE-EXISTING
  property of the whole identity arm, not introduced here; disclose, do not fix.)

**Latch:** per-CPU field in `cpu->cd.alpha`, not function-static (the carrier's per-instance rule; a static latch
joins `staticlatchscope` and would need its machine-wide-limitation excuse written down).  Keep the existing message
text, bounded `(once)`; it survives `-q` where the generic WARNING does not, and it is the marker a future member-5
implementer would look for -- which blunts kimi's "the return-value contract is the fault-delivery hook" argument:
the latched announcement is a louder hook than a silent `return 0`, and member 5 is not available today anyway
(names no measurable consequence -> files as documented-only, does not decide).

## Q2 -- IF the owner overrides to member 3

Under member 4 the ordering is moot: a fetch at VMKILL has no translation failure, so this round is independent of
`alphaifetchkill`, which may then go in either order.  **If 3 is chosen instead:** `alphaifetchkill` (HIGH,
witnessed at rung 3) must go FIRST, because this round would otherwise ship with a guest-drivable host death at its
own fetch cell, merely relabelled from the kill message to `could not find physical address`.  Shipping "with the
fetch cell disclosed" is a documented outstanding host-death in a hardening fork -- acceptable only as an explicit
owner decision, and worse because H8 shows `alphaifetchkill` is not a quick fix, so "first" is not soon.  The
measurable consequence: under 3-then-disclose, a fetch row is RED (host dies) on this round's own commit; under 4, it
is GREEN.  That asymmetry is the whole case for 4.

## Q3 -- the nine dispositions: no DECISION is wrong; H9's framing of two "disputes" is

I traced each to source or to the seat's landed text.  **None of H1-H8's decisions reverses.**  H1 (4+latch)
affirmed above.  H2 affirmed (the announcement is true and worth latching under either reading -- see H9.3).  H4
(AYONA3 its own row, FILE LOW) affirmed: different class (flood not kill), different vehicle (walk path, ptbr != 0),
no witness.  H5 (three-way scorer) affirmed -- it is my own #540/#538 rule; a DIED_ELSEWHERE under a mutant is a
KILL, never a 0/0 escape.  H6 affirmed (the single-step trace read self-logs at `cpu_dyntrans.c:287`/`:325`; the
cold generic fetch is the dying path).  H7's detector plan affirmed, and the **ANCHOR row is load-bearing** -- a
load at VMKILL+8 behaving like VMKILL pins the special case's width against a mutant keyed on the exact address or
page.  H8 affirmed (not a one-liner; under 4 this round does not depend on it).

**What is wrong is H9's characterization, and it matters because it reads as three live disputes when two are
agreements:**

- **H9.1 (the per-access WARNING) -- both half-right, settled.**  It is a `VERBOSITY_WARNING`, unlatched/per-access
  (kimi's "flood" is true at default/`-V`), AND silenced by `-q` (Opus is right).  Neither statement alone is the
  whole fact.  My measurement's "4 under `-V`" is consistent.  Record it as *"unlatched per-access WARNING, shown at
  default, silenced by -q."*
- **H9.2 (#194) -- NOT a dispute; kimi AGREES with Opus.**  I read `memory_alpha.c:194-198`: the ACTION clause
  ("must not exit; report 0") is TRUE and is what #194 achieved (the `not_found` `fatal()` prints and does NOT exit
  in this fork -- `debugmsg.c:384-390`).  The RATIONALE clause ("so the caller raises the fault") is FALSE for Alpha:
  loads/stores abandon (`memory_rw.c:259` + #215), fetches exit (`:729-733`).  **kimi's landed text says exactly
  this** (`kimi.txt:712`: *"the comment's rationale is aspirational for Alpha ... accurate for the return-value
  contract"*), and codex_adv found it independently.  So H3 is CORRECT, but the packet's "kimi reads #194 as
  TRUTHFUL, against Opus's WRONG RECORD" misreads kimi's mid-stream musing for its conclusion.  **Sharpen H3:**
  correct the RATIONALE clause only (keep the true action clause), and note it is adjacent to -- not required by --
  member 4's edit at `:75-78`, so it may equally ride with H4's walk-path cleanup.  This is the carrier's own
  "read the body, not the verdict line," landing on a summary of the body.
- **H9.3 (the VPT slot) -- NOT a dispute either; both agree it is inside the VPT, and the difference is
  immaterial.**  kimi read the guest header (`kimi.txt:562`: OpenBSD-2.2 alpha `vmparam.h:154`,
  `VPTBASE 0xfffffffc00000000`) and computes VMKILL at +6 GB, **inside** the 8 GB VPT self-map (`:592`).  Opus
  agrees it is inside, and additionally sign-extends the slot's target to `ALPHA_K1SEG_BASE` -- the very segment
  this arm remaps at `:83-84`.  kimi's "non-canonical" refers to the slot's intermediate 43-bit target VA (6 TB, in
  the VA hole) read without sign-extension.  **The disposition does not turn on it:** both members 3 and 4 latch, and
  the announcement is a TRUE record under either reading, so H2 holds.  Opus's sign-extension is the better-supported
  reading (the self-map indexes canonical VPNs, and it lands on the arm's own special-cased segment), but I do not
  stake the ruling on it because it is immaterial.

**How I checked for a wrong decision:** I re-read the site and both death paths, confirmed member 4's fetch survival
against Session A and member 3's fetch death against Session B, confirmed the WARNING is `VERBOSITY_WARNING` and
`-q`-gated, and read kimi's and codex_adv's LANDED conclusions on #194 and the VPT (not their mid-stream reasoning).
The decisions hold; the only corrections are to H9's framing and H3's scope.

## Found something else
- **The packet's H9 over-reports disagreement.**  On two of its three "disputes" the dissenting seat's landed
  conclusion agrees with the disposition; only H9.1 is genuinely two-sided (and there both sides are half-right).
  This is the seat-failure-vs-agreement distinction one level up: a mid-stream musing quoted as a verdict manufactures
  a dispute that the body resolves.  Worth a line in the record so a future reader does not re-litigate #194.
- **Member 4's contract owes three disclosures**, none blocking: the per-access verbosity-gated WARNING (H9.1); the
  STx_C dropped-store-reports-success lie (Opus, derived -- I relay it as derived, not independently re-read); and
  the pre-existing exotic-`-M` 40-bit identity alias (Opus #2).  All three are properties member 4 shares with the
  arm's existing behaviour, not defects it introduces.
