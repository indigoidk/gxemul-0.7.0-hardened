FABLE_SEAT_ALIVE_20261102_P1
# PANEL PASS 1 -- `shfcnvsdfpul`: the SuperH FCNVSD handler overwrites FPUL, a register the instruction only reads

VERDICT: PROCEED WITH CHANGES (4)

Seat: Fable 5.1, file-reading, pass 1, read-only. Tree read: `GXEMUL-SEC` at HEAD `987cb596` (confirmed by `git rev-parse`), every
source line through `git show HEAD:<path>`; the two manuals by absolute path; the probe and gate at HEAD. Nothing built or run; the
3/6 witness output is taken from the brief (the artifacts directory was excluded from my reading). My line numbers for the handler
(`:3049-3063`), its sibling (`:3064-3076`) and the decoder (`:5061-5068`) agree with the brief's exactly.

The four changes, in one place:
1. L4 record correction: the bug file's prose row (`OUTSTANDING_BUGS.md:8240` at HEAD) says the cast is the one `#297` "removed from
   FTRC". It was not removed; it was guarded. Correct in place, quoting the old wording (Q1c).
2. Mark ONE of the FPUL rows `NODN` so the table has a DN=0 leg at zero added sessions; that catches weakening (f) and its mirror (Q3).
3. Spread the FPUL rows over at least two destination registers, one of them DR0 (`0xf0ad`); that catches weakening (g) and its mirror,
   also at zero cost (Q3).
4. The `nan` row's input `0x7fc00000` is a SIGNALING NaN under the SH-4 convention (fraction MSB = 1, `sh4_programming.txt:4980-4989`).
   Label it `snan`, or use a qNaN pattern such as `0x7fa00000`, and write the NaN classing into the clause (e) contract (Q2, Found).

Everything else in the brief that I could check, I confirmed by reading or by enumeration; the details follow.

## Q1, premise audit

Q1 (a): yes, deleting the line leaves DRn byte-identical for every FPUL value. In the handler as shown (and as at HEAD, `:3056-3062`),
`op1.f` is read by the cast and never written by it; the DRn store at `:3060` consumes `op1.f` and nothing else. `op1.nan` is never
consulted. The only theoretical route to a difference is the compiler exploiting the undefined cast to assume `op1.f` in range on HEAD,
and the fix removes that line, so the direction that matters is safe; the measured `dr hi 1.5` and `dr lo 0.1` rows on HEAD agree
with the table. Re-derived, not taken from the brief: I walked `ieee_store_float_value_rm` (`float_emul.c:422-699`). The FP_ZERO arm
(`:679-681`) adds nothing to the sign bit set at `:499-501`, so `-0` gives `80000000 00000000` as the brief predicted; FP_INFINITE gives
`7ff00000...`; FP_NAN gives `7fffffff ffffffff` with the sign lost as well as the payload, because `ieee_interpret_float_value`
sets `fvp->f = NAN` and jumps past the sign step (`:151-153`, `:271-276`); the host `NAN` is positive. The subnormal `0x00000001`
decodes to exactly 2^-149 (`:226-231`, fraction halved once and exponent raised to 1 - bias) and stores as `36a00000 00000000`
(biased exponent 874 = 0x36a); `sh_dn()` returns it untouched because `mag >> 52` is nonzero (`cpu_sh_instr.c:189`). The brief's claim
that `sh_dn()` never changes an FCNVSD result holds for the whole input space: a widened single has biased exponent 874..1151, or is
zero, Inf or NaN, and every one of those returns at `:181`, `:183` or `:189-190`.

Q1 (b): nothing in the tree relies on FCNVSD having changed FPUL. `git grep fpul HEAD -- src/` outside `cpu_sh_instr.c` and `cpu_sh.c`
hits only the struct field (`cpu_sh.h:111`); in `cpu_sh.c` the uses are the debugger registration (`:141`) and the register dump
(`:763-768`) and disassembly text. In the handler file the FPUL readers are `float_fpul_frn` (`:2921`), this handler (`:3056`),
`fsca_fpul_drn` (`:3092`) and the copy/store handlers reached through `arg` pointers (STS, STS.L, FSTS at `:4222`, `:4593`, `:5020`).
None depends on the truncated integer. Guest-side dependence cannot be settled from the tree; I have the same non-evidence the brief
has, and I note it under unsettled premises.

Q1 (c): "guarded", not "removed". Both FTRC arms at HEAD still end in `cpu->cd.sh.fpul = (int32_t) op1.f;` (`:3016`, `:3038`); what
`#297` added is the range ladder ahead of them (`:2996-3014`, `:3020-3036`), and the handler's own comment says so: "In the NORM arm the
truncated value fits int32 by construction, so the cast there is defined C and byte-identical to the old path" (`:2989-2990`). The
CHANGELOG block agrees: "only then hands in-range values to the old interpret-and-cast path" and "the one cast that remains is defined C
on every host" (`CHANGELOG.md:25567-25569`, `:25585-25588`). So the bug file's row at `:8240` ("the same UB `(int32_t)` cast `#297`
removed from FTRC") is a wrong record: `#297` removed the undefined REACH of the cast, not the cast. L4, correct in place.

Q1 (d): +0 is the only fixed point, and I enumerated it by exponent band rather than by trusting the brief's hand derivation. Write the
single as b = (e << 23) + m with value v = (2^23 + m) * 2^(e-150), and ask when `(int32_t) v`, read back as a uint32 pattern, equals b.
Positive side: for e < 127 the truncation is 0, equal to b only at b = 0 (that is +0); for 127 <= e < 150 the truncation is below 2^24
while b >= 127 * 2^23, no solution; for e = 150..157 the equation (2^23 + m) * 2^(e-150) = e * 2^23 + m is linear in m, and the unique
rational solution is out of range for e = 150..156 (m > 2^23) and non-integral at e = 157 (127 m = 29 * 2^23, m = 1915509.70);
e = 158 (2^31) and above is out of int32 range. Negative side: the pattern of a negative result is 2^32 - trunc(|v|); the equation
trunc(|v|) = 2^31 - e * 2^23 - m has no solution for any e (for e = 157 the right side is negative, for e = 156 the solution
65 m = 36 * 2^23 is non-integral, for e <= 155 the right side exceeds the truncation), and exactly -2^31 (`0xcf000000`) gives the
defined result INT32_MIN = `0x80000000`, not `0xcf000000`. For the inputs where the cast is undefined in C (finite |v| >= 2^31 other
than -2^31, +-Inf, NaN) the x86-64 host returns the integer-indefinite `0x80000000` (recorded by the ftrc comment at `:2951-2952` and by
`#297`'s record), which equals none of those inputs. So on this host HEAD changes FPUL for every input except +0, and the brief's
statement is exact.

Q1 (e): yes to both. The cold debugger's `fpul=` write goes straight to the field: `CPU_SETTINGS_ADD_REGISTER32("fpul",
cpu->cd.sh.fpul)` at `cpu_sh.c:141`, with `fr%i`, `xf%i` and `fpscr` registered the same way (`:140`, `:184-190`). Note `fpscr=`
bypasses `sh_update_fpscr()` and so performs no bank swap, which is fine while FR stays 0, and every existing row already relies on
it. The readback shape is the ftrc rows' shape byte for byte: `(0x025a << 16) | 0xf2ad` then `(0x0009 << 16) | 0x2122`, three
instructions, and the probe steps 3 when a second word is present (`sh_rounding_probe.py:269-270`). `sts fpul,r2` is
`copy_fp_register` with `arg[0] = &fpul` (`:4220-4223`, handler `:2869-2873`) and reads the field at execution time, after the FCNVSD
has written it. FD is clear at reset (`cpu_sh.c:123`, `SH_SR_MD | SH_SR_IMASK`), so the macro at `:57-66` does not fire. The six
committed `ftrcS-*`/`ftrcD-*` rows prove this exact channel green at HEAD, and the witness measured it for FCNVSD.

Other section 2/4/6/7 premises checked and holding: the handler is upstream residue (`git log -L3049,3063` returns only `39748e3c`);
no `fatal()`/`exit` in the handler; `fpul` and `fr[]` are `uint32_t` (`cpu_sh.h:104`, `:111`); FPSCR resets to `0x00040001`
(`cpu_sh.c:118`, DN=1 and RM=RZ); the decoder requires bit 8 clear so `r8` is even (`:5061`); the decoder and both handlers test no PR.
The `0x3dcccccd` arithmetic: mantissa `0x4ccccd`, high 20 bits `0x4ccccd >> 3 = 0x99999`, low 3 bits `5 << 29 = 0xa0000000`, biased
exponent 123 - 127 + 1023 = 1019 = `0x3fb`, giving `3fb99999 a0000000`; the interpret/store loops are exact for a widened single, so
no rounding question arises and the mode does not enter (`ieee_store_float_value`, not `_rm`, is used at `:3060`). One section 7
statement is conservative rather than load-bearing: `%-28s` pads and does not truncate, and the gate greps `^$v.*ok$` with no mandatory
double space, so a 28-character name would still match; keeping names short is good practice, not a hard constraint.

## Q2, the partition

By what HEAD's cast does to FPUL (the fix leaves every class unchanged, so the fix changes the answer for every class except P0):

* P0: `0x00000000` (+0): HEAD writes 0, the pattern it read. Unchanged; a fixed point. No row can show the defect here, and the table
  rightly has none.
* P1: |v| < 1 with a nonzero pattern: `0x00000001..0x3f7fffff` and `0x80000000..0xbf7fffff` (subnormals of both signs, -0, normals of
  size below 1). HEAD writes 0. Rows: `0.1`, `-0`. The subnormal member is not rowed (fine for FPUL: DN does not enter this channel).
* P2: 1 <= |v| < 2^31, plus exactly -2^31: `0x3f800000..0x4effffff`, `0xbf800000..0xcf000000`. HEAD writes trunc(v), a defined cast,
  never equal to the input (Q1d). Rows: `1.5`, `-1.5`. The boundary of this class is exactly the ftrc ladder's constants (strict
  `> 0x4effffff` positive, `> 0x4f000000` on the negative magnitude, `:3025`, `:3031`), which is a nice cross-check on both.
* P3: finite |v| >= 2^31 other than -2^31: `0x4f000000..0x7f7fffff`, `0xcf000001..0xff7fffff`. Undefined cast; `0x80000000` on this
  host. No row (section 6 lists `0x4f000000` but section 7 does not row it). Disclose.
* P4: +-Inf. Undefined cast; `0x80000000` on this host. Row: `+Inf`. `-Inf` not rowed.
* P5: NaN. Undefined cast; `0x80000000` on this host. Row: `0x7fc00000`, which is an sNaN under the SH-4 convention; the manual's
  `fpul_type` splits NaN at `0x7fc00000` (`:10948-10950`) and routes qNaN to `qnan(n)` and sNaN to `invalid(n)` (`:10907-10909`), both
  of which write `DR[n]` only (`:8861-8867`, `:8914-8926`), so FPUL is read-only in every NaN arm too. qNaN not rowed.

So the table has a member in P1, P2, P4 and P5, none in P3, and correctly none in P0. The brief's "Is FPUL really never written?"
question: I agree. The pseudocode assigns only `DR[n>>1]` (`:10903`), `*FPUL` is read by `fpul_type` and by that assignment, and the
`qnan`/`invalid`/`set_E` helpers write `FR[n]`/`FR[n+1]` or FPSCR, never FPUL. The sibling FCNVDS's prose says explicitly that FPUL is
"not updated" on an exception (`:10763-10764`); FCNVSD has no FPUL output at all. The missing `NORM` label in the `fcnvsd` case list
(`:10897-10909`) is a manual omission, as the brief reads it: the sibling's list carries `NORM` (`:10782`) and the special-case table
gives `+NORM`/`-NORM` (`:10958`).

## Q3, candidate weakenings

F is the fixed handler (no FPUL write). "First differs" names the lowest bit pattern at which the candidate's FPUL differs from F's.

* (a) verbatim: differs at every input except +0, first at `0x00000001`. Red: all six FPUL rows (`inf` and `nan` red on the x86-64
  host; the C standard gives them no value, the same caveat the ftrc comment records). This is floor clause (b).
* (b) `|v| >= 1`: differs on P2, P3, P4 (`INFINITY >= 1.0` is true; both NaN comparisons are false). First at `0x3f800000`. Red: `1.5`,
  `-1.5`, `inf`. Green: `0.1`, `-0`, `nan`.
* (c) `|v| < 1 -> 0`: differs on P1 only (writing 0 to +0 is a no-op; NaN comparisons false). First at `0x00000001`. Red: `0.1`, `-0`.
* (d) specials `-> 0x80000000`: differs on P4 and P5. First at `0x7f800000`. Red: `inf`, `nan`. On this host (d) is byte-identical to
  HEAD on P4/P5 and agrees with F on P3, i.e. it is "HEAD's special cases made defined", a plausible edit shape.
* (e) `RM == RZ`: differs at every non-+0 input under toward-zero only. The table runs each row in both modes and the gate wants two `ok`
  lines per row, so red: all six FPUL rows (toward-zero leg). Its mirror (`== RN`) reds the nearest leg. Caught at no cost by the
  vehicle itself.
* (f) `DN clear`: differs only with DN = 0. The probe ORs DN into every row that is not `NODN` (`:297-299`), so under the table as
  proposed it writes nothing and ESCAPES. With one FPUL row marked `NODN` (the marker strips DN and the row still runs both modes, since
  `NODN` does not restrict the mode keys), that row reds and its mirror (`DN set`) reds the other five. Change 2.
* (g) `destination != DR0`: differs for every destination other than DR0; with all rows at `dr2` it is caught, but its mirror
  (`== DR0`) escapes. Encode one FPUL row with `0xf0ad` (DR0) and the rest elsewhere, and both forms red. The FPUL rows do not read
  DRn, so the destination choice is free. Change 3.
* (h) low half after the store: differs at every input except +0, first at `0x00000001`. The low word of a widened single is
  `(m & 7) << 29`, one of eight values, equal to the input pattern only for +0 (the patterns `0x20000000`, `0x40000000`, ... all
  have zero low mantissa bits). Red: all six FPUL rows.
* (i) halves exchanged: FPUL untouched, so the FPUL rows are green; both DRn rows red (`hi` reads `0xa0000000`, `lo` reads
  `0x3fb99999`). It differs at every input except +0. This is a mutant of unchanged code and shows the DRn rows are not vacuous;
  it is detector hygiene, not the fix's floor.

Floor or disclosure. The rule enumerates the predicates dominating the edited line within the function and the partitions the body
tests. The only dominating predicate is the FD check in the macro (`:57-66`), whose reachable cell at the body is FD = 0, the one
every row runs in; re-introducing the write under FD is either (a) again or dead code. The body tests nothing: `sh_dn()`'s DN test
(`:182`) and `fpclassify` live in callees, outside the DEPENDS-ON bound. So none of (b) to (g) is inside the floor; all are clause (e)
material. (b), (c), (d), (e) and (h) are caught by the proposed table anyway; (f) and (g) are caught after changes 2 and 3 at zero
added sessions, so I would take them rather than disclose them. What remains to disclose in the (e) contract: the value classes with no
row (P3 finite out-of-range, `-Inf`, qNaN, a subnormal input), since a weakening keyed to exactly one of those classes, for example
`if (op1.f >= 2147483648.0) <that line>`, would escape; and the +0 fixed point, which no row can observe. I did not invent further
forms beyond that one, which has its first-differing input (`0x4f000000`) named.

## Q4, option-set completeness

Delete is the only member consistent with the manual, and the sibling grep supports it. FPUL readers in the file that do not write it:
`float_fpul_frn` (`:2919-2935`) and `fsca_fpul_drn` (`:3090-3099`). FPUL writers: `ftrc` and `fcnvds`, whose destination it is, and the
LDS/FLDS copies. FCNVSD is the file's only reader that also writes FPUL, so the arm under review is the outlier among its siblings,
which is the stronger warrant. The other members do not apply: there is no value to ACCEPT or storage to BACK (the architecture
defines no FPUL write), nothing to DECLINE or FAULT (the instruction is legal), and a "make the write defined" form (saturating cast)
would keep the defect. IMPLEMENT would mean modelling the DENORM/qNaN/sNaN arms (`set_E`, `invalid`, `qnan`) for DRn, which is the
exception-model round the tree has already named. No missing member found.

PR = 0: the tree never models `undefined_operation()` for a PR-reserved combination, so FCNVSD is not an outlier here either: FCNVSD and
FCNVDS at PR = 0 (manual `:10883`, `:10770`; handlers test no PR), FIPR at PR = 1 (`:11251`; handler `:3111-3132` tests no PR), FTRV at
PR = 1 (`:12852`; handler `:3140-3174` tests no PR). FILE once as a class, not per instruction. Agree with the brief.

FCNVDS row as a same-file control: not owed, and I would not ride it. The six ftrc rows already prove the `sts fpul,r2 ; mov.l r2,@r1`
channel in the same table, so the detector has its channel control; the witness's `fcnvds ctl` row was the right control for the
witness and it was run. FCNVDS's own coverage is scope growth, and there is a candidate defect in it (see Found while checking), which
is the better reason to give it its own row rather than a rider here.

DN = 1 subnormal input: leave it to `#303`'s named gap. A FPUL row with a subnormal input would be clean (FPUL is unchanged either way)
but adds nothing the P1 rows do not already carry; a DRn row there would pin the known-divergent value, which is the wrong thing to pin.

## Q5, the vehicle and proportionality

The vehicle is right. Checked against HEAD: the pin at `gate_sh_rounding.sh:64` moves 36 -> 52 (or 50 if one row is dropped); the
per-row loop at `:78-83` wants two `ok` lines per name; `disc` stays 9 because `discriminating` counts table dictionaries with more than
one distinct value (`sh_rounding_probe.py:320`) and the new rows' RN and RZ keys are equal (the S -> D widening is exact and the D
store ignores the mode). Names: no proposed name is a prefix of another or of any of the 17 existing list entries, and the longest
(`fcnvsd fpul -1.5`) is 16 characters. One small hazard worth a comment: the names are used as regexes in `grep -c "^$v.*ok$"`, so the
`.` in `1.5` and `0.1` is a metacharacter; harmless today. The #548 staging recipe for the gate file (HEAD-based copy, commit, restore
the working file, md5 check) is the right way to keep the three uncommitted hunks out of this round.

Witness controls: adequate without a further control, for a reason the brief did not state. A FPUL row cannot false-green on a dead or
partial session: if `sts` never ran, r2 holds its reset value 0, not the seed; if `mov.l` never ran, DEST holds `0xdeadbeef`; neither
equals any proposed want. The one false-green shape is "the handler ran and did nothing", which is exactly the identity medium, and
the DRn rows are what red on it. So the (c) record must name the DRn rows as its carriers, as the brief already does.

Proportionality: eight rows at two modes is sixteen cold-debugger sessions against a section that already runs 36 plus the halt probe;
I did not time a session. Sole-carrier analysis over (a) to (i): `fcnvsd fpul inf` carries nothing another row does not (`nan` carries
(d), `1.5` and `-1.5` carry (b)); `fcnvsd fpul -0` likewise (`0.1` carries (c)). Dropping both leaves every named candidate red at 12
sessions. I would drop `inf` first and keep `-0`, because `-0` is the only row where HEAD corrupts the pattern without changing the
value, which is the corruption a guest is least likely to notice; and keep both DRn rows, since `dr lo` carries clause (c) and (i) but
`dr hi` is what shows the conversion lands in FR(n) at all. Seven rows, fourteen sessions, or eight if the owner wants the manual's
special-case columns (+-0, +-INF) each represented.

## Found while checking

1. SH-4's NaN convention is the reverse of the x86 one, and three things follow. The manual (`sh4_programming.txt:4980-4989`) makes a
   fraction MSB of 1 a signaling NaN. (i) The proposed `nan` row's `0x7fc00000` is therefore an sNaN; the manual routes it to
   `invalid(n)`, not `qnan(n)`. FPUL is unchanged in both arms, so the FPUL claim is untouched; the label and the contract should say
   sNaN (change 4). (ii) The existing probe row `ftrcS-nan qNaN+` (`sh_rounding_probe.py:173`) uses the same pattern and is mislabelled
   by the same convention; records only, since the ftrc ladder treats every NaN alike. (iii) More than a label: every single-precision
   NaN RESULT this file stores is the shared encoder's all-ones pattern `0x7fffffff` (`float_emul.c:511-516`; double `0x7fffffffffffffff`),
   which SH-4 classes as SIGNALING, while the hardware's generated qNaN is `0x7fbfffff` / `0x7ff7ffffffffffff` (`:5005-5008`), and
   FCNVDS's pseudocode writes `0x7fbfffff` to FPUL for both NaN kinds (`:10790`, `:10794`). The MIPS coprocessor already canonicalises
   for exactly this reason (`#255`, `cpu_mips_coproc.c:1199-1209`: "ieee_store_float_value() emits all-ones ... a SIGNALING NaN; an
   arithmetic result must be quiet"); the SH tree has no equivalent (`git grep 7fbfffff -- src/` hits only the MIPS file). Severity LOW
   (bit pattern only; this model raises no FP exceptions, so a guest sees it only by inspecting bits), a class across the FP store sites
   in `cpu_sh_instr.c`, with an in-tree precedent for the fix shape (a canonicalisation at `sh_dn()`'s position would cover all sites at
   once, the way `#334` did). Not this round's; FILE. It also gives the brief's section 6 item 2 a second reason: the DRn NaN value is not
   just "a policy with the payload lost", it is a pattern the architecture classes as signaling where hardware emits quiet, so rowing it
   now would pin the wrong bits.
2. The `#297` wording in the bug file, Q1(c) above: L4, one sentence.
3. Section 6's table lists `0x4f000000` as undefined (correct) but the boundary is worth writing into the contract: exactly `-2^31`
   (`0xcf000000`) is a DEFINED cast yielding INT32_MIN, and the defined/undefined boundary of the deleted cast coincides with the ftrc
   ladder's constants (`:3025`, `:3031`), which is independent confirmation that both are right.

## Premises I could not settle from this packet or the tree

* Whether any guest depends on FPUL holding the truncated integer after FCNVSD. No guest source read; the tree cannot answer it.
* The pre-fix redness of the `inf` and `nan` rows (floor clause (a)) rests on the x86-64 host returning `0x80000000` for the undefined
  casts. I read that from the ftrc comment and `#297`'s record, not from a run; the witness had no Inf/NaN row. The owed pre-fix run of
  the detector settles it.
* The wall-clock cost of sixteen more sessions: not measured.
* `op1.f` being a `double`: consistent with every call signature I read (`ieee_store_float_value_rm(double nf, ...)`), but I did not open
  `float_emul.h`.

VERDICT: PROCEED WITH CHANGES (4)
