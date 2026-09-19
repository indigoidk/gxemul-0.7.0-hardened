FABLE_SEAT_ALIVE_20260918_540P1
claude-fable-5-1 | "# CHECKPOINT -- 2026-09-18 21:3x   HEAD: cdbe7d7 #537 fbsmlane: #442's harness printed a verdict token its own self-mutant lane could never read -- the lane runs, pinned on R3"
VERDICT: GO-WITH-CHANGES -- the two `PHYSICAL` tokens ship as proposed (Q1 GO); the lane cells are FLOOR, six rows owed in the one armed session (Q2); HIGH as witnessed (Q3); two records corrections and one scorer refinement (Q4); no change to the fix.

# #540 (lcaisaphys) pass 1 -- Fable 5 seat, adjudicating

**How I worked.**  Read-only: no build, no emulator, no panel script; this file is the only write.  Read in full:
`fable5_p1_packet.md`, `brief_sent.md`, `opus5_p1.md`, `codex_adv540p1.txt`, `grok.txt`, the committed
`regress/lca_isaphys_probe.py`, `_scratchpad/w540/lca_isaphys_probe.EXT.py`, `PRETABLE_DRAFT.md`, and the #530 §F2
block (`GXEMUL-SEC/CHANGELOG.md:307-326`).  Grepped `kimi.txt`, `codex.txt` and `agy.txt` for the claims the packet
attributes to them (F2, F4, F5, F11).  Read every source line a disposition rests on; all paths below are under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`.  The four packet-fed answers I checked only through the packet.

## Q1 -- GO

`src/devices/dev_lca.c:301-302` and `:305-306` pass `CACHE_NONE` with no `PHYSICAL`; `src/cpus/memory_rw.c:245`
translates every such call; `src/cpus/memory_alpha.c:62` and `:73` are the only identity arms and both require
`!userMode`.  The two tokens are the smallest edit that makes the forward independent of ptbr AND of PS<CM>.  Opus's
census shows every other device-to-device nested forward in the tree carried `PHYSICAL` from the upstream import, so
this is residue, not policy.  Nothing any seat found changes the fix.

## Q2 -- OWED.  The lane cells are FLOOR.  The discriminator, stated to bind:

> **An axis is a FLOOR axis of an edited statement when BOTH hold inside the enclosing function: (i) the body's OWN
> CODE induces a partition on it -- a test, or an index/selector it computes from its inputs, whether those inputs
> are device state or the access parameters `len` / `writeflag` / `relative_addr`; and (ii) that partition's value
> FLOWS INTO an operand of the edited statement, or the body RE-TESTS it on the edited statement's output path.
> The floor is the cross-product of such axes with the dominating predicates.  An axis meeting one condition but not
> the other is clause (e).**

This is the 2026-09-09 JOIN clause (a selector is a floor axis when its value flows into an lvalue the guarded body
reads or writes, or the body re-tests it after the join) stated for a selector that is not a `case` label -- and it
is the pass-11 floor read the way pass-11 itself applies it.  That clause says in the same breath that it enumerates
`#499`'s width x component x direction x position cells "from `len`, `writeflag` and `relative_addr`": ACCESS
PARAMETERS, not device state.  Opus's reading takes "device-STATE lvalues" as exclusive, which puts `#499`'s own
three L2 breaches outside the floor.  The word came from TxICR, where the lvalues happened to be pending counts; it
names the instance the clause was minted on, not the class.

Applied to `DEVICE_ACCESS(lca_isa)` (`dev_lca.c:275-312`):

* **direction** -- dominating predicate `writeflag == MEM_WRITE` (`:299`).  Floor; both cells rowed.
* **lane `ofs`** -- (i) `ofs = (relative_addr & 3) % len` (`:297`) is the body's own partition; (ii) on the write
  arm `byte = data[ofs]` (`:300`) is the DATA operand of the edited call (`:301`), and on the read arm `i == ofs`
  (`:309`) re-tests it on the edited call's output.  Both conditions hold on both arms.  *"`ofs` is off the repair
  path"* is false by reading: it is the statement immediately before the write call and the consumer immediately
  after the read call.  **Floor: {R, W} x {0,1,2,3} = 8 cells.  The witness rows two** -- both `ofs` 0, because
  `% len` with len 1 is 0 at every port, whatever its low two bits.  **SIX ROWS OWED.**
* **port threshold** ((e')/F6(f)) -- (ii) holds (`relative_addr` is the address operand), (i) fails: the body
  induces no partition on `relative_addr` beyond `& 3`.  Clause (e).  Consistent with #530's `p_port10`.  The
  post-arm 8042 row is LICENSED BY ITS KILL, not owed -- the draft already says so; keep saying so.
* **width beyond {0, >0}** -- the body tests `len` only at `:295`.  Marginal; clause (e).  A `len == 1`
  conditioning is red on the wide rows anyway, at no cost.
* **user mode, ptbr** -- not read by the function.  Clause (e); disclose in the contract (F8, (g)).
* **the forwarded byte's value** -- single-operand marginal; clause (e).

Bound check: finite (8 cells), derived from the diff and its enclosing function, no callee or caller walked.  It
cannot become `#392`.

**Why the packet's two reasons are the WRONG reasons, and it matters for future rounds.**  *"Consistency with
#530"*: floor is a property of the DIFF, not the handler.  On #530 the edited lines WERE the lane guard, so lane was
floor there by the dominating-predicate clause; that does not transfer by handler identity, and the next round on
this file must not cite "#530 said lane" as its warrant.  *"Cheap"*: cost is never a floor criterion; the addition
licence's "cannot hurt" is the same move in the other direction.  A row is owed because the body's partition reaches
the repaired statement, and it stays owed when it is expensive.

On *"adds a flag, not a predicate"*: the carrier moved clause (d) from INTRODUCED to DEPENDS ON on 2026-08-24
precisely because fixes that add no predicate enumerated the empty set.  A flag-add is that shape exactly.

Grading: L1, nothing shipped.  Had the 13-row witness shipped as the detector, `PHYSICAL only when ofs == 0` would
have been an L2 sweep -- the `#499` shape, and the exact shape #530's `vc` was.

## Q3 -- HIGH, as witnessed.

Reach does not lower harm -- the carrier's rule, and Opus concedes it.  What is left of MED is "host impact is prints
only" and "the hit case is unwitnessed".  Neither carries.  This fork ranks a SILENT WRONG ANSWER to the guest above
a loud failure, and the witnessed case is exactly that: every sparse read after the arm returns a false zero with
success, every store is dropped with no fault (#215), for the console UART, 8042, PIC, PIT, CMOS, LPT and IDE at
once.  It is universal under paging in practice: no real table maps USEG VA `0x1d00003fd` to the ISA flat address
(kernels reach physical space through K0SEG), so the inner access is a miss or a misroute, never correct -- only
the SHAPE varies.  Plus one `fatal()` per access (`memory_alpha.c:197`), `-q`-proof and guest-drivable, with
Opus's polled-console amplification.  HIGH does not need the misroute.  The hit-case witness is NOT a severity
condition (F17 below).

Correction that feeds this: the free-running flood is ONE unlatched line per access, not two -- see F11.

## Q4 -- the twenty dispositions

### Reversed or corrected (4)

**F2 -- the HEADING is a wrong record.**  *"The forward works ONLY while ptbr == 0"* is TRUE as far as it goes and
INCOMPLETE the other way: both identity arms also require kernel mode (`memory_alpha.c:62`, `:73`; Opus 1c(i),
codex_adv P2, grok).  What the brief got WRONG was the outcome list (miss-only).  Keep the body's correction, fix the
heading, and put the kernel-mode conjunct in the fix comment: *correct only while ptbr == 0 AND PS<CM> = kernel;
otherwise translated through the guest's tables -- a miss answers a false zero or drops the store, a hit misroutes
it.*

**F11, and the same sentence in F4 -- REVERSE AS WRITTEN.**  The second line is `debug()`
(`memory_rw.c:604-607`), not `fatal()`, and `debug()` returns early when free-running at default verbosity:
`src/core/debugmsg.c:365-376` -- `v = verbose; if (emul_executing) v--; ... if ((quiet_mode && !ss) || v < 0)
return;`.  It prints under `step` (which is why the witness transcript shows it) and under `-v`.  The kimi CLI said
"two lines per WRITE" and named it `debug()`; the packet generalised it to "each access", dropped "write", and called
it unlatched -- three dropped qualifiers.  Record: *one `fatal()` per access; on writes a second, verbosity-gated
`debug()` line.*  HIGH survives the correction.

**F16 / Q2 -- the CONCLUSION stands; the REASONS are replaced** by the discriminator above.  Opus's dissent is
rejected on the argument, not the seat.

**F14 -- UPHELD and REFINED.**  The structural alternative is not owed, and here is the check: on host death `t3` is
None, so `flat lsr` is red and Opus's rows-4-7-plus-`flat lsr` gate goes DEAD / 0/0 as well.  Only the scorer rule
closes BOTH (c) and host death.  But the rule as stated has one hole: under load the single retry can still return
all-None, giving CONTROL=DEAD with `alive` = alive -- a FALSE KILL that reads as detector strength, in the artefact
the record will cite.  Score three ways: **exit 0 and N/N -> ESCAPED; exit 2 with `alive` = died, or any control
red WITH A VALUE (e.g. (c)'s `live` = 0x0) -> KILLED, channel named; exit 2 with `alive` = alive and the controls
ABSENT -> INVALID RUN, re-run, never counted.**  A missing `LCAISAPHYS_DONE` is INVALID too.

### Upheld, with the check I made (16)

* **F1** GO.
* **F3** wording only; the witness's addresses match none of the four remap/exit predicates at
  `memory_alpha.c:75-88` (checked by arithmetic).
* **F4** HIGH (Q3), minus the "two unlatched lines" sentence.
* **F5** CONTROL=DEAD.  The pre-arm `live` write and read both go through the forwarder; under `NO_EXCEPTIONS` the
  8042 handler is skipped at `memory_rw.c:584-585` (pckbc is `DM_DEFAULT`, `dev_pckbc.c:1241-1242`), and the reply
  byte is 0x0 DETERMINISTICALLY by the #95 pre-zero at `:485-492`.  grok's table omits row 2; agy (`agy.txt:110-111`)
  and codex_adv are right, and the packet is faithful to them.  Record it as *KILLED at `live`; rows 9-12 NOT
  EVALUATED* -- never "11/13", never "green".
* **F6** ADD -- and they are floor (Q2), not merely L1.  I verified the COM2 readbacks the rows rest on: IER stores
  raw at `dev_ns16550.c:199` (the probe never writes LCR, so DLAB stays clear); MSR stores raw at `:236` and ORs
  `DCD|DSR|CTS` = 0xb0 at `:128` on EVERY access, so the pre-fix readback is 0xb0, not 0 -- the draft's assert
  `(X|O) != O` already covers it; MCR raw at `:284`, and 0x03 carries no `MCR_IENABLE`; SCR through the default arm
  `:302`/`:309`.  One pin to add when moving to LDL: `ldl` sign-extends bit 31, so the lane-3 READ plant must keep
  `(Y|O) < 0x80` (0x3c does) or the row compares the low 32 bits.  Lane-0 wide rows are the same cell as the byte
  rows under the body's partition; keep them as free width pins, licensed not owed.
* **F7** upheld -- and now CHECKED rather than taken from a seat's inability.  The one concrete candidate, an
  unregistered port, does NOT fail by default: `memory_warn_about_unimplemented_addr` returns true only under
  `halt_on_nonexistant_memaccess` (`src/core/memory.c:645-654`); otherwise `memory_rw.c:681-683` zero-fills and
  returns OK.  On the halting path the OUTER access fails anyway at `:591-592`.  So (g) has no measurable consequence
  on a default configuration.  (Hygiene, not filed: on that halting path `byte` at `dev_lca.c:278` is packed
  uninitialised; dead in effect because the outer returns FAILED.)
* **F8** upheld; add Opus's point that the K0SEG wrap still CALLS the translator -- wrong by construction, not only
  user-mode-fragile.
* **F9** upheld; the `:758` derivation needs `ok == 2`, which `memory_rw.c:235` sets unconditionally, so it holds.
* **F10, F12, F13, F18** upheld.
* **F15** upheld; `src/include/cpu_alpha.h:59-67` sets `ALPHA_FEATURE_BWX` for NO type and nothing in
  `src/cpus/cpu_alpha*.c` reads it, so BWX is ungated for every modelled CPU (the #530 comment's "ungated BWX").
  LDL/STL is the architectural width for the lane rows.
* **F17** ruled: HIGH without it.  The hit case is a WITNESS-STRENGTH improvement (a positive pre-fix signature for
  the value channel), not a floor cell and not a severity condition.  FILE it as its own witness row
  (`lcaisaphyshit`) rather than adding a second session in-round; if built, a SEPARATE session, so the miss rows
  keep their zero L1[0].  The record marks the misroute "derived by reading, not witnessed".
* **F19** upheld: `src/cpus/cpu_alpha_palcode.c:222`, `:231-248`, `:275-291`; the helpers at
  `src/core/memory.c:783` and `:891` pass `CACHE_DATA`, no `PHYSICAL`.  Same class, own row.
* **F20** upheld: `memory_rw.c:738-750` has no `PHYSICAL` guard, and `ok = 2` makes `:744` pass and `:758` fire.
  `-M >= 7425` only; disclose; file the general form as a hypothesis.

How I checked for reversals: each disposition was traced to the source line it rests on and to the seat text it
summarises.  The corrections above are exactly the places where the source, or the seat, said something narrower
than the packet.

## For the PRETABLE and the contract

1. **The (d) enumeration, by the bound, so the contract can cite it:** conditioning the added flag on `writeflag`
   (= (a)/(b): floor, rowed); on `ofs` (floor, six rows owed); on `len` (marginal, red on the wide rows for free);
   on a port threshold (clause (e), killed by the licensed 8042 row); on user mode or ptbr (clause (e), disclosed);
   on the byte value (marginal).  Closed over the function's hunks.
2. **The CHANNEL line names, per lane row, the mutant and the observable:** `w<k> wide` kills `PHYSICAL only when
   ofs == 0` and `except ofs == k` through the FLAT readback; `r<k> wide` through the packed longword.  The draft's
   `M_b` prediction at `arm kbc` is honestly UNCERTAIN; keep it so until measured.
3. Every new row RED on the committed build first, with the file that ships hashed (F18).
