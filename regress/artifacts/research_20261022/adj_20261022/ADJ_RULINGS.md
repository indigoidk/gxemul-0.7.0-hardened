# External-fixes research -- adjudication rulings, 2026-10-22 (main loop merging GPT-6 Astra + Grok 4.7; Fable 5.1 HELD)

Seats: GPT-6 Astra (ultra, pointer form; `codex_resadj.txt`) AMEND; Grok 4.7 (xhigh, plan mode; `grok_adj.txt`) AMEND.
Fable 5.1: DELIBERATELY NOT FIRED (owner 2026-10-22 "hold on Fable adjudication"; `fable5.NOT_FIRED.txt`).  Both seats
read source at HEAD de8c7547; neither built or ran anything.  Dispositions below; where the seats disagree both sides
are named and the argument counted, not the seats.  Applied to the records drafter's output before the filing commit.

## A. Confirmed as classed (both seats, from source)
T1 (m88k scaled-byte xmem NULL slot; user-mode HOST-STOP), T3 (`ppcllscrcexit`, user-mode), T5, T7, T8, T10, T11, T12
(guest-kernel HOST-STOP), T2 (PPC DS-form: `stdu` stores at EA+1 and skips the update; `ldu`/`lwa` wrong; GUEST-
CORRUPTION; no alignment exception exists to intercept it), T18 (`crandc`/`crorc` compute NAND/NOR; unfiled; real).
No further duplicate found among the UNFILED rows (T23, T89, T139/T140, T142 each exceed the row they resemble).

## B. Class / severity / reach amendments (apply to the filing)
* **T4 (IDE LBA):** FILE as GUEST-CORRUPTION but mark **LATENT in this tree** -- IDENTIFY word 49 is stored 0
  (`dev_wdc.c:374-377`), so a guest honouring it never addresses by LBA; the `#if 0` formula (`:470/:562`) means `d->lba`
  is never read for an address.  Live only for a guest that ignores word 49 (report B says FreeBSD 10+; UNVERIFIED here).
  DISAGREEMENT: Astra retains present-tense corruption and batches it 3rd; Grok (the measurement above) says latent,
  queue it, batch later, and decide word 49 FIRST.  Grok's argument is the measured one; adopted.  Both: do not port the
  FreeBSD patch as-is (it keys on bit 5; a CHS `0xa0` sets bit 5); the round owes the word-49 decision and a bit-6 decode.
* **T6:** reach **U on 32-bit** (a user branch to an unmapped address; `memory_ppc.c:314-326` has already raised ISI,
  `memory_rw.c:259-268` returns failure, then `cpu_ppc_instr.c:4115-4119` exits).  PPC970 (the testppc/bareppc default)
  never reaches it -- it dies first in the 64-bit translation exit (new row N3 below).  The fix is "return into the ISI
  already raised", which must not be presented as the fix for N3/N4/N5.
* **T9:** NOT re-filed.  `b120` (held) already is "an unknown command is reported to the guest as success"; WRITE AND
  VERIFY falls into that same default arm.  Per-controller outcomes differ (ASC synthesises GOOD; mb89352 stops; osiop
  leaves status unchanged; ATAPI completes without error) -- carried in `b120`'s record, not a second row.
* **T11:** cite BOTH exit sites: `cpu_mips_coproc.c:2040-2041` (invalidating the old entry) and `:2168-2169` (installing
  the new one).  Reach K (TLB writes are kernel; VR4102-VR4131 are MIPS_R4100).  No port exists; the round owes a design
  (removing the exits alone does not implement 1 KB-page translation).
* **T14:** construction-time (DEC 3000/300 interrupt wiring), reach C.  **T16, T17:** host-environment/debugger, C --
  not guest-triggered.  **T15 (ns16550 `115200 / divisor`):** UB, NOT a host kill in the shipped `-O3` build --
  `OUTSTANDING_BUGS.md:6146-6174` already measured SIGFPE at -O0/-O1 and survival at -O3; do not file it again as a host
  kill; word it "observed with the recorded compiler at -O0/-O1".
* **T136:** consolidate `m88kmxmkill` + `m88kpsrmxm` (keep both histories, add an alias); MED (guest-kernel CPU stop).
* **T141 (missing variadic argument):** guest-triggered host UB -> at least MED, not hygiene (a crash is not established).
* **Reach:** T149 -> K (TLBWR selects at runtime); T147, T151, T152 -> C.  None is build-only.
* **T127:** port confidence Y -> UNVERIFIED (legal MC88100 `.wt` semantics not established; the recipe is not authority).
* **T92-T95 (FILED-IN-PART):** their unfiled residuals need a carrier -- widen the existing row or add a residual row;
  the "121 unfiled" count did not cover them.

## C. New defects the adjudication found (ADD rows; none in TRIAGE.md)
* **N1** `cpu_m88k_instr.c:3045`: `xmem` to r0 decoded as NOP -- the memory write and its access semantics are dropped
  (manual `_scratchpad/mc88100.txt:6435`); user-reachable WRONG-RESULT.  Not resolved by T126.  (Astra)
* **N2** `cpu_m88k_instr.c:2359` vs `:3604`: the xmem handler reads the `.usr` bit as `0x80` while the decoder identifies
  `.usr` as `0x100` and rejects `0x80` as `.wt` -- wrong address-space/privilege semantics; WRONG-RESULT.  (Astra)
* **N3** `memory_ppc.c:280-288`: translated access with `bits != 32` prints `TODO: ppc 64-bit translation` and `exit(1)`
  -- on PPC970, the testppc/bareppc DEFAULT CPU, the first access with MSR IR or DR set kills the host.  HOST-STOP, reach
  K, HIGH; large design (a page-table walker), not a small round.  (Grok)
* **N4** same function: the `TODO: 601` exit.  HOST-STOP.  (Grok)
* **N5** `memory_ppc.c:69-73` returns 0 for PP=none or a write to a read-only BAT and the caller exits (`TODO: BAT
  exception`) -- a 32-bit guest protection failure that never raises DSI.  HOST-STOP / WRONG-RESULT.  (Grok)

## D. The first batch (merged; each seat's own order is in its answer)
1. T1  (both first; fix shape DISPUTED: Astra -- dropping ajfa's `op != 3` exemption leaves the NULL call because
   `xmem_slow` rebuilds `scaled` from the word (`:2395`); repair the TABLE by mapping scaled-byte slots to the unscaled
   byte handlers, keep the generation suppression (duplicate names otherwise); Grok -- drop the exemption.  Pass 1 of the
   round settles it by reading `:2357-2395` and `generate_m88k_loadstore.c:254`.)
2. T3  (both)       3. T6 (Grok 3rd / Astra 6th)       4. T2 (both; design owed, nothing safe to copy)
5. T36 88K bus-error PFSR/PFAR before ANY 88K fault round (both; upstream r6542/r6547 shape; preserve the ORIGINAL
   physical address -- `memory_rw.c:437` has already made `paddr` device-relative; select the right CMMU; keep the NULL
   check; do not import the plain-RAM CMMU windows).  Also the carrier of the reopened PFAR defect (R2) -- no new row.
6. T18 (Grok adds; Astra "consider next")   7. T120 MIPS no-case primary opcodes (same)
8. T7 bounds repair FIRST, exits' disposition after (both)   9. T11 (both; design owed)   10. T5 (both; one exit only)
Tail, in order: T12 (settled DECLINE, narrow), T4 (word-49 decision first), T8 (after T7, same disposition), T10 (name
ONE site; exclude the 2^24-byte MEMORY MOVE), T13, N3 (large design; file, do not fold into T6).

## E. The records corrections
* **R2 CONFIRMED by both:** correct `OUTSTANDING_BUGS.md:1896-1898` in place quoting the three sites (`m8820x.h:66`,
  `memory_m88k.c:399/:405`, `dev_m8820x.c:438`); reopen under T36.  `m88kexit` (`memory_m88k.c:390-394`) is a different
  row -- do not merge.
* **R1 CONFIRMED in conclusion; details CORRECTED by Astra's frozen comparison:** THREE `1U <<` sites in
  `generate_arm_r.c` (139, 200, 279), not two; the 59 extras vs `root_src` are 50 `tmp_*.c` + `autodev.c` +
  `automachine.c` + six generated font files + `ppc_spr_strings.h`; vs frozen upstream 61 incl. two `grep.exe.stackdump`
  (also present in `root_src`); the `configure` difference is the GNU89-inline probe absent upstream.  Grok notes the
  "inside commit 39748e3c" pin was the coordinator's measurement (git archive), which stands.
  DISPOSITION (both: never rewrite the commit; never retroactively re-attribute old A/B results): correct the false
  "unmodified upstream" label in `gate_ab.sh:4` and beside `CHANGELOG.md:24451-24462` NOW (a comment-only script edit --
  its own small commit, not the records commit); keep `PRISTINE_REF` (Grok: old logs name it; `1U` does not move guest-
  visible results); a byte-true SECOND ref for future "pristine" claims is FILED as an owner option (Astra).

## F. Do not port (both seats; beyond the two recorded cautions)
The FreeBSD/DragonFly WDC patch as a patch; rs6000 `9a05a7b` (DS-form host abort), its CA rewrite (T128), no-execute
ISI bit (T25), `month_days[-1]` (T106), softfloat (T34), TGPR-dropping MSR mask, dyntrans branch-target abort; ajfa
patch 01's scaled-byte xmem exemption (that IS T1) and patch 04's 2^24-byte MEMORY MOVE and `.wt`-as-hint (T127);
upstream `4e3e72b1`'s plain-RAM CMMU windows (T36/T134); any upstream `exit(1)` deletion that relies on error-level
messages stopping the CPU (T135, T138); Glaw's MAC patch (`fprintf` of a pointer before its NULL test, T118); Debian's
TAP variant (unterminated truncated name); ryoon `e1ce5e9`/`714ef40` (they ADDED the footbridge exits; `fbsdrampair` is
DECLINE); CHERI's ties-away `round()`, COP2-as-NOP, the misplaced signed-overflow guard in unsigned division, dead
RECIP/RSQRT code, trunk's unconditional FP divide-zero exception; jroark's VR4131 register map (T109) and HIBERNATE
vector (T110) as if they were a manual (`in_use=0` on the extra SIU, T114, is a portable one-line fact).  Take hunks
after reading them; neither rs6000 nor the ajfa series is a correct GXemul.
