# RULING -- FABLE_QUEUE item 4: the code-scanning items (final) and `#584` fmtattr as shipped

> **DURABLE COPY, banked 2026-11-06 by a records commit.**  The original is `_scratchpad/fable_20261106/item4/RULING.md` (scratch, not durable; md5 6363ecbc), written 2026-11-06 by the Fable 5.1 seat for FABLE_QUEUE item 4 (the code-scanning items, final, and `#584` fmtattr as shipped); the coordinator verified its author with `agent_models.py` as claude-fable-5-1 (this kit did not re-check it).  This banner and the marked citation rewrites `PROVENANCE.md` lists are the only edits; the ruling's text is otherwise verbatim.

Fable 5.1 (flagship review seat), 2026-11-06.  Token `FABLE_LIVE_20261106_I4`.
First line of `_scratchpad/CHECKPOINT.md` [scratch, not durable], verbatim: `# CHECKPOINT -- 2026-11-04 17:0x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)`

**Evidence basis.**  A READING, not a measurement: I opened the repo (`GXEMUL-SEC/`, HEAD `2632277f`), the two commits
`ccd1c502` (#584) and `2632277f`, the round's artifacts under `regress/artifacts/fmtattr/`, the triage, the brief, both
adjudication drafts, Astra's passes 2 and 2b, the probe, gate 1's block, the ledger rows, and the dismissal plan
(`_scratchpad/codescan/dismiss/SUMMARY.md`, `plan.tsv`, `dismiss.sh`, `checks/run_checks.out` [scratch originals; banked at `regress/artifacts/codeqlscope/plan_20261106/`, whose `plan.tsv` carries this ruling's two wording notes]).  I built nothing, ran no gate, fired
no panel, called no seat, and changed nothing on GitHub or in any tree.  Every number below is quoted from a named artifact or
re-derived from the source lines I cite; where reading could not settle a point I say so (section 7).

**Verdict line.**  `FABLEI4: 4 ITEMS GRADED (3 REAL+LOW, 1 FALSE POSITIVE); #584 RATIFIED AS SHIPPED, CHAIN CLOSED (0 breaches over
the stated denominator); 16 DISMISSALS CONFIRMED, 0 CORRECTED, 2 WORDING NOTES; 1 ITEM FILED, 0 L2/L3/L4`.

---

## 1. The four items, graded

Both drafts (GPT-6 Astra, `regress/artifacts/fmtattr/adj_20261105/astra/codex_csadj.txt`; Gemini 4 Argon, `regress/artifacts/fmtattr/adj_20261105/gemini_adj_items/reply.txt`)
agree on the four load-bearing points.  I did not take that agreement as evidence; I re-derived each grade from the source.

| item | grade | severity | what I checked |
|---|---|---|---|
| `fmtmissarg` | **REAL** | **LOW** | `fmt_warnings.tsv:99` shows the `dev_ps2_stuff.c:239` `-Wformat=` "expects a matching 'int' argument"; the three calls at HEAD (`dev_ps2_stuff.c:239-240`, `dev_mb89352.c:305-309`, `cpu_ppc.c:478`) are now format-clean and carry the right values (section 3.1).  The effect of the defect was an unspecified vararg printed to the user's own console; it is undefined behaviour in the C sense but reaches no host memory under guest control.  Gemini's "potential host memory leak" (severity 1) overstates it: what leaks is a register or stack word into the local console of the person running the emulator.  LOW stands. |
| `fmtattr` | **REAL** | **LOW** | a diagnostic-correctness class (truncated or garbled numbers in diagnostics, one stray comma making `%i` read a string pointer at `x11.c:551`).  No guest-visible consequence; the one measured observable is the SGI loader line printing the low 32 bits of a disk offset (`DRYRUN_fmt.out` legs `head_wsl`/`head_pmax`: `FMTBB_RESULT=2/3`, offset `0x0`). |
| `arcmemdescnr` | **REAL** | **LOW** | `arcbios.c:1565-1579` at HEAD is unchanged from the triage's reading.  I re-did the arithmetic the triage got wrong: with `s` the descriptor size, `a0 = base-1` gives `nr = -1`, `-1 / s == 0` (C truncates toward zero), `nr++ == 1`, so V0 = `base + s` -- the SECOND descriptor, which the proposed `nr < 1` guard would still accept.  `a0 = base-s` gives `nr = 0`, V0 = `base`; `a0 = base-2s` gives `nr = -1`, V0 = `base - s`, below the table.  Also: `int nr = a0 - base` narrows a 64-bit difference; `s * nr` is signed `int` arithmetic (overflow is UB, not a wrap); and `(uint32_t)a0 == 0` at `:1565` aliases ARC64 `0x100000000` to NULL.  The result reaches the guest only through V0 (`:1576`, then `break`) -- no host access.  Astra's boundary-membership fix (handle NULL and the low-32-bit NULL test; reject `a0 < base`; unsigned wide difference; reject a nonzero remainder and an out-of-range index BEFORE any multiplication) is the right design and is complete over the option set; Gemini's alignment check is the same member.  The round is HELD on a classifier stop (`ARC_HELD_NOTE.md` [scratch original `_scratchpad/codescan/ARC_HELD_NOTE.md`, not durable]); I rule on the design only and do not touch the round. |
| `disasmnullmnem` | **FALSE POSITIVE** | -- | I read the three switches myself, not the drafts' tables.  `cpu_alpha.c:626-651`: the outer cases are exactly `{0x31, 0x35, 0x38..0x3f}` and the inner switch assigns `mnem` for exactly those ten values.  `cpu_m88k.c:1422-1439`: outer `{0x20,0x22,0x24,0x26,0x28,0x2a}`, inner the same six.  `cpu_alpha.c:307-356`: the inner switch's `0x27..0x2f` arms are at `:344-352` and the outer list starts `0x0a..0x0f, 0x20..` at `:307-318`; I did not count every line of the outer list between `:318` and `:328`, so for THAT switch I rely on Astra's and Gemini's independent full readings plus the fact that GCC's warning was a `-Wformat-overflow` deduction (it cannot see switch coverage), not a reachability proof.  No opcode reaches a flagged `debug()` with `mnem` NULL.  **Zero bug-fix rounds**, as both drafts said.  The shipped accommodation -- an unreachable `default: mnem = "?"; break;` with a comment naming it unreachable and naming the warning it silences (`cpu_alpha.c:353-355`, `:648-650`; `cpu_m88k.c:1436-1438`) -- is the "documented false-positive accommodation" Astra licensed, and it is behaviour-neutral on every defined path.  Right that no ledger row exists for it. |

**Severity order:** `fmtmissarg` ~ `arcmemdescnr` > `fmtattr`; `disasmnullmnem` carries no defect.  None is a host-memory
corruption on any reviewed path.  I checked the one place that could have changed this: `arcmemdescnr`'s `s * nr` UB is in HOST
arithmetic on a guest-supplied value, but its only sink is a guest register, so the UB can produce a wrong V0, never a host access.

## 2. Round shapes

* **ONE combined format round with `fmtmissarg` folded in but separately identified: RIGHT, and that is what shipped.**  The
  attribute catches all three missing arguments as the same compiler class; a separate implementation round would have duplicated
  the staging, the build and the gate work for three lines.  The two guest-reachable sites did deserve a stronger witness than the
  compiler's diagnostic; see section 5 for the one obligation that leaves open.
* **Not split per file or subsystem: RIGHT.**  The attribute is one declaration change that lights up every call at once; a split
  would either land the attribute with a red build or land fixes with no detector.
* **A separate ARC round: RIGHT**, and it is held for the reason the note records.
* **`disasmnullmnem`: no round; the two-CPU accommodation inside #584: RIGHT.**

## 3. `#584` fmtattr as shipped (`ccd1c502` + records follow-up `2632277f`) -- the six hold questions

The regress stage of `fmtattr` and `fmtmissarg` is held with a six-part question (ledger `hold_question`, quoted in full in both
rows).  Answers in order.  Where a question asks "is X right", the answer is what I verified, not what the record asserts.

### 3.1  (1) Grades and shape -- YES.  Section 1 and 2 above.  Additionally, the shipped fixes at the named sites are correct:

* `cpu_ppc.c:478` `debug("cpu%i:  PPC601-style, TODO!\n", x);` -- the CPU identity restored, Astra's pass-2 correction applied.
* `cpu_arm.c:1041-1046`, `:1051` -- `%zu` for the `size_t` products; correct type, decimal radix kept.
* `dev_bt455.c:71-72`, `dev_dc7085.c:181-182`, `:202-203` -- `PRIx64` with `(uint64_t)idata`, minimum widths `02`/`04` kept; the
  value is logged before masking, so the wide form is the right one.
* `dev_le.c:1037-1041` -- `PRIu64` with `(uint64_t)idata`; the `idata >= N_REGISTERS` branch is exactly the one where `idata` is not
  small, so the earlier `(int)` would have printed `1` for `0x100000001`.
* `dev_mb89352.c:307-309` -- the unsupported trailing value field removed (`idata` is still its initial zero at that point: Astra pass 2 item 3).
* `dev_ps2_stuff.c:239-240` -- `timer_nr` supplied; it is 2 or 3 in that branch.
* `x11.c:549-553` -- only the stray comma removed; the concatenated string is whole again.
* `file_ecoff.c:407-409` -- pass 2b's one repair: both `off_t` values cast `(uint64_t)` and printed with `PRIx64` (`:273` declares them `off_t`).

### 3.2  (2) Is the enforcement sound -- YES; no other policy is owed.

* **The attribute.**  `misc.h:260-278`: `GX_PRINTF(f, a)` is `__attribute__((format(printf, f, a)))` under `__GNUC__` and empty
  otherwise; indices `(1,2)` on `debug`/`fatal`, `(4,5)` on `debugmsg(int, const char *, int, const char *fmt, ...)`, `(5,6)` on
  `debugmsg_cpu(struct cpu *, int, const char *, int, const char *fmt, ...)`.  I counted the parameters; the indices are right.
* **The gate.**  `gate_build.sh:119-124` counts `warning:` lines in each tree's build log and `check`s the count against `0`; so with the
  attribute permanent, any mismatched call reds gate 1 in either tree.  That IS an enforced failure policy.  `-Werror` would add
  nothing the gate does not already refuse and would break user builds on compilers whose spurious warnings this project does not
  control; the owner's ruling (gate check, warning-only build) is the right one.
* **The controls.**  `gate_build.sh:264-281`: one deliberate `%i` with an `int64_t` per function, each on its own line, compiled with
  the tree's own `CC` and `CWARNINGS` (`-Wall` carries `-Wformat`) and `-fsyntax-only` against the headers just built; 4 warnings
  wanted of every kind, and each line keyed by number to a `-Wformat` warning.  This pins two things the zero-count cannot: that
  the attribute is live on every one of the four declarations, and that the flag set still enables format checking.  The dry run
  (`DRYRUN_fmt.out`) measured it: `A1_nofatal` reds exactly the `fatal` control (3 of 4), `A3_noargs` -- a `(4,0)` index -- reds
  exactly the `debugmsg` control, `A2_empty` reds all four, `S3_noheader` reds the compile check.  Each nulled attribute reds on
  exactly its controls, as the CHANGELOG claims.
* **The two residuals, disclosed and acceptable.**  (i) Protection is conditional on `__GNUC__`; gate 1 runs under GCC, so the GATE is
  universal even though the build-time check is not.  (ii) The count check keys on the literal `warning:`; a future `-w` or
  `-Wno-format` in `CWARNINGS` would silence it -- but the seeded controls compile with the same `CWARNINGS` and would then fail to
  warn, so that edit reds the gate too.  Sound.

### 3.3  (3) Is ONE output row the right bound for the type-compatible class -- YES; nothing more is owed in this round.

The class the compiler cannot see is a type-compatible wrong value or radix: `PRIx64 -> PRIu64`, or `(uint64_t)(uint32_t)x`.  The
shipped row (`regress/fmt_bootblock_probe.py`, 3 rows) pins one representative wide-hex repair by its OUTPUT on an unmodified
`-E sgi -e ip32` machine, and it is built the way Astra's pass 2b required: it matches the LOADING line only
(`re.search(r'Loading voldir entry "sash"[^\n]*')` compared whole against the wanted text), so the later read-failure warning that
also prints the right offset cannot mask a mutant.  Kill table (`row_20261105/bb_kill.out`): base 3/3; `M1_radix` 2/3 printing
`0x4294967296`; `M2_narrow` 2/3 printing `0x0`; both built with 0 format warnings, both binaries newer than their mutant source.

Why one row is the bound and not one per call: the fix introduces no predicate, so clause (d)'s DEPENDS-ON enumeration is the empty
set, and the carrier's remedy for a class breach is a class closure written into the CONTRACT, not a cell-by-cell chase.  The
probe's docstring and gate 1's block comment (`gate_build.sh:259-263`) name the one row claimed and disclose the rest; the CHANGELOG
floor paragraph carries Astra's count of the disclosed population (48 calls exposed to the radix edit, 39 to the narrowing edit).
That is clause (e) done properly.  More would be owed only if a disclosed call had a measured guest-visible consequence or fed a
gate's grep; none was shown, and diagnostics are host-console output.

### 3.4  (4) Were the inherited narrowings right to FILE -- YES.

They predate the round (Astra pass 2, "Other truncations"; pass 2b item 4), they are not made worse by it, and widening the diff to
fix them would have taken the round past its adjudicated scope with no detector of their own.  The two that the round newly CONSUMES
-- `arcbios.c:1594-1595`'s A1/A2 and `ps2_bios.c:167`'s A1 -- went from printing the wrong field to printing the right field
truncated, which is an improvement that leaves a disclosed defect; filing them is the honest disposition.  They are filed as
`fmttruncinherited` (ledger: open, LOW, naming the eight files) and are in flight as `#585` (FABLE_QUEUE item 5), so nothing is lost.

### 3.5  (5) Is the GitHub dismissal list right -- YES, as the plan now states it.  Section 4.

### 3.6  (6) The closing pass on pass 2b's repair and the new detector -- ZERO BREACHES; the chain closes.

The repair-chain rule requires a VALID closing pass with its denominator.  This pass is a reading over measured artifacts; the
denominator is:

* **Pass 2b's repair** (`fix_hand4.py`, `file_ecoff.c:407-409`, two conversions): read at HEAD; type-correct; radix preserved; no
  predicate touched.  Its own detector on the MEASURED host is nil -- on LP64, `%08lx` with `off_t` (= `long`) never warned, so the
  repair is a portability correction with no observable on x86-64.  That is a disclosed limit, not a breach: nothing claims a row
  for it, and the compiler on a host with 32-bit `long` and 64-bit `off_t` is the detector it would have.
* **The probe** (3 rows): each row's CHANNEL varies under a named mutant -- `loading offset` under `M1_radix`, `M2_narrow`, `M0_revert`
  (and on HEAD); `voldir parsed` and `session ended` under the null media `N1_true`, `N2_absent`, `N3_false` (`CONTROL=FAIL`, 1/3, 0/3, 1/3).
  No survive-only row, no self-comparing row.
* **The gate block** (14 checks): `rows run` pinned to the literal 3 (`S1_extrarow` reds it), `rows correct` pinned by equality,
  the result line and control line by exact match, the sentinel last (`S2_nodone` reds it), every row by name.  Each of the 14 was
  red on at least one of the 15 legs (`DRYRUN_fmt.out`, 16 of 16 as predicted in `PRETABLE_fmt.out`, written first).
* **The vacuity floor over the composite:** (a) pre-fix red on both HEAD build trees (controls 0 of 4, probe 2/3); (b) verbatim
  reinstatement -- at the probed site measured (`M0_revert`: build warns twice at `bootblock.c:435` and `:442`, probe 2/3), and at
  every other fixed site by construction, since the verbatim pre-fix text IS a compiler warning (that is what the 181-warning scan
  measured); (c) null media red; (d) the attribute nulled three ways, each red on exactly its controls; (e) the contract in the probe
  docstring and the gate comment; (f) not applicable (no address decode).

**One mutant shape I looked for and did not find a hole in:** a type-compatible edit at `bootblock.c:442` that keeps `0x100000000` for
THIS input and breaks another -- e.g. `PRIx64` with a mask `& 0x1ffffffff`.  It would pass the row; it is the disclosed class and
no row can close it by enumeration.  Disclosed, not owed.

### 3.7  Records I checked against the artifacts

The CHANGELOG `#584` block's numbers resolve: 181 warnings at the scan (`fmtscan.out`), 0 with the stage (`fmtverify2.out`: warnings 0,
errors 0, controls 4 of 4), three trees rebuilt with both clearance parts and `FMTBB_RESULT=3/3` on each (`UPDATE_FMT.out`, binaries
`f646c36009dc`, `b660fb5d1322`, `e690f2cce4ef`), gate 1 in situ `clean-build: PASS (32 checks)` with the block's 14 ok
(`GATE1_INSITU_fmt.out`), "warns twice" measured at `DRYRUN_fmt.out:371-373`.  `pass2_ledger.tsv:196` carries the receipt and names
the two seat failures (Grok 4.7 402, GLM 5.3 monthly limit) and the non-firings by name.  `ledger.json`: `fmtattr`/`fmtmissarg` closed,
`commits` = `ccd1c502`, witness `detector:regress/fmt_bootblock_probe.py` with its reasoning; `arcmemdescnr` open, `witness: none`;
`codeqlscope` open with `ccd1c502` (the workflow and config landed; the repository setting is the owner's).  The witness term
`detector:` is right for `fmtattr`: the probe is a real boot-path execution on an unmodified machine and shows the symptom pre-fix, so
it would also qualify as the round's rung-3 attempt (the ledger says so); for `fmtmissarg` see section 5.

## 4. The dismissal plan -- 16 rows, each checked at the source

Method: for each row I opened the flagged line at HEAD and every assignment to its operands, and compared the plan's reason and
comment with what the code supports.  "CONFIRMED" means both the GitHub reason and the comment's claim hold.

| alert | path:line | plan | ruling | what the source shows |
|---|---|---|---|---|
| #121 | `cpu_mips_instr_unaligned.c:115` | false positive | **CONFIRMED** | `wlen` is `sizeof(uint32_t)` or `sizeof(uint64_t)` at all eight callers (`cpu_mips_instr.c:3222-3229`); `i < wlen`; `dir` is `1` or `-dir` (`:61-71`).  `i*dir` is in [-7, 7]. |
| #122 | `cpu_mips_instr_unaligned.c:145` | false positive | **CONFIRMED** | same operands, same bound. |
| #123 | `cpu_sh.c:1567` | false positive | **CONFIRMED** | `lo8 = iword & 255` at `:1146`, in scope; factor `2` or `4`; product at most 1020. |
| #124 | `dev_fb.c:905` | won't fix | **CONFIRMED** | `size = d->ysize * d->bytes_per_line`, both set at `dev_fb_init` from the caller (24 callers, all device-init functions; the guest runs later).  VGA passes `fb_max_x = pixel_repx * max_x` (`dev_vga.c:1307`, `:1324-1325`) with `pixel_repx` from the host's `scaleup`; at scale 53 and 24-bit depth the product exceeds `INT_MAX`, as Astra computed and the comment says.  Host-only and real: "won't fix" with that honest comment is the right GitHub state. |
| #125 | `dev_fb.c:332` | false positive | **CONFIRMED** | `x1`, `x2` clamped to `[0, d->xsize-1]` (`:298-301`), `y2 < y1` and `x2 < x1` returned early (`:328`); `(x2-x1+1) * (bit_depth/8)` is at most `xsize * 4`, with `xsize` at most 16384 after any resize. |
| #126 | `dev_fb.c:175` | false positive | **CONFIRMED, wording note** | `d->bytes_per_line * y`, `y < new_ysize <= 16384` (`:147`).  The NEW stride is bounded by the resize guards; the OLD stride `d->bytes_per_line` is bounded by a prior resize or by init.  On every guest-reachable path the product is below 2^31 (65536 x 16383); a host configuration large enough to break it has already overflowed #124 at init.  The comment's "so rows * line stays below 2^30" is true for the new stride and for the fork's actual initial strides; I would add "on guest-reachable paths; the host-set initial stride is #124's" so a reader does not take the resize guards as the whole proof (Astra's premise b made the same point).  Not a wrong reason. |
| #127 | `dev_fb.c:176` | false positive | **CONFIRMED, same note** | `new_bytes_per_line * y`: both factors bounded by the resize guards (`:147-168`); below 2^30 outright. |
| #128 | `dev_ps2_gif.c:176` | won't fix | **CONFIRMED** | inside `test_triangle()`; its only calls are under `#if 0` (`:424-430`); no other reference in `src/`.  The comment's reason (disabled demonstration code) is exact.  Even if enabled: `d->xsize` is only ever 640 (`:413`), the coordinates are the constants at `:425-429`. |
| #129 | `dev_ps2_gif.c:178` | won't fix | **CONFIRMED** | same function, same `#if 0`. |
| #130 | `dev_pvr.c:2317` (HEAD `:2330`) | false positive | **CONFIRMED** | `xsize = ((DIWSIZE_DPL & 0x3ff) + 1) * 4 / bytes_per_pixel [/ 2]` (`:576-593`), `ysize = (DIWSIZE_LPF & 0x3ff) + 1 [/ 2]`, `bytes_per_pixel` in {2, 3, 4} (`:585-587`), `DIWSIZE_MASK = 0x3ff` (`dreamcast_pvr.h:168`).  `bytes_per_line * ysize` is at most 4096 x 1024 = 4,194,304 -- Astra's figure exactly.  The comment's phrasing ("xsize and ysize come from the masked DIWSIZE fields") is loose about the `(dpl+1)*4/bpp` derivation but the bound it asserts holds.  The plan already records that the line moved and that `dismiss.sh --apply` will REFUSE this row until `plan.tsv` is re-derived from a fresh fetch; that is the right behaviour and must not be bypassed by hand-editing the line. |
| #131 | `dev_px.c:326` | false positive | **CONFIRMED** | `span_len` clamped to `PX_XSIZE` = 1280 (`:317-318`, `:93`); `span_src`, `span_dst` `< PX_YSIZE` = 1024 (`:323`, `:94`); `bytesperpixel = bitdepth >> 3` with `bitdepth` 24 or 8 (`:778-787`).  Largest product 1023 x 1280 x 3 < 4M. |
| #132 | `dev_vga.c:492` | won't fix | **CONFIRMED** | `3 * scaleup * font_width`, `font_width = 8` (`:833`, `:844`, `:1304`), `scaleup` from the host command line.  Host-only; "won't fix" is honest (a host value could in principle exceed the bound). |
| #133 | `file_elf.c:362` | false positive | **CONFIRMED** | `ephnum` is a 16-bit header field (`Elf64_Quarter`/`Elf32_Half`, `:152`, `:177`); `ephentsize` must equal `sizeof(Elf64_Phdr)`/`sizeof(Elf32_Phdr)` or the loader `exit(1)`s (`:158-164`, `:183-189`).  65535 x 56 < 2^22. |
| #134 | `file_elf.c:511` | false positive | **CONFIRMED** | same for `eshnum`, `eshentsize` (`:165-171`, `:190-`); 65535 x 64 = 4,194,240 < 2^22 = 4,194,304. |
| #136 | `arcbios.c:487` | false positive | **CONFIRMED** | `n_memdescriptors` increments once per `arcbios_add_memory_descriptor` (`:509`): two fixed calls (`:2936`, `:2938`), one per 256 MB of `physical_ram_in_mb` (`:2946-2962`), one per loaded program (`emul.c:337`).  `s` is 24 (`struct arcbios_mem64`: `uint32_t, uint32_t, uint64_t, uint64_t`, `sgi_arcbios.h:356-361`) or the 32-bit struct's size.  Bounded by the host's memory configuration; cannot approach 2^31. |
| #137 | `diskimage.c:2100` | won't fix | **CONFIRMED** | `access(fname, R_OK)`/`access(fname, W_OK)` at `:2074-2075`, `fopen` at `:2100`: a real check-then-use race on the user's own image path, which the guest cannot influence.  Outside the threat model; "won't fix" is the right reason, and the comment says exactly that. |

**Rows that are NOT dismissals, checked too.**
* **#135 `arcbios.c:1577` PENDING-FIX: RIGHT.**  It is the real defect of `arcmemdescnr`; do not dismiss it.  It closes when that
  round lands and is pushed.
* **EXPECTED-TO-CLOSE (108): accepted.**  The three-way evidence (`verify_expected.py`: the same GCC warning at the scan commit for
  108 of 108; `git blame` naming `ccd1c502` for every call; `tree_identity.py`: 502 of HEAD's 505 `src/` files byte-identical to the
  tree `fmtverify2` built, the other 3 differing in 4 comment-only lines) makes the claim "nothing of the class is left at HEAD"
  checkable without a new build.  Each closes on the rescan after the push.
* **ARTIFACT-COPY (71): right not to dismiss.**  They are copies of product sources under `regress/artifacts/` and `experiments/`;
  `.github/codeql/codeql-config.yml` ignores both paths and the workflow uses the Default setup's category `/language:c-cpp`.  For
  #1/#2 (`experiments/dump-hp700rx-rom.c`) the fallback reason the plan holds ready -- `won't fix`, real mismatches in a tool the
  build does not compile -- is the right one if the advanced setup does not close them; it is NOT a false positive (Astra's
  correction, which I confirm: the TSV describes real mismatches).
* **The plan's safety:** `dismiss.sh --apply` refuses any alert whose state is not `open` or whose rule or `path:line` differs from
  `plan.tsv` (`dismiss.sh:83-87`), reads the state back (`:93-97`), and its negative control (`plan_neg.tsv`: a moved line, a
  changed rule, a closed alert, two invalid rows, a nonexistent alert, one MATCH) behaved as predicted (`run_checks.out`).  Apply mode
  has never run.  The order the plan states -- fixes land, push, re-fetch, `mkplan.py`, `run_checks.sh`, then `--apply` on the
  owner's word -- is the right order, and the ARC round's hold means #135 is the one alert that waits past it.

**Dismissal-list verdict: 16 of 16 confirmed with their reasons; 0 corrected; 2 wording notes (#126/#127, #130 comment precision),
neither a wrong reason.**  Nothing is to be dismissed by this ruling, and I dismissed nothing.

## 5. Dissents and filings under the late-dissent rule

The round has landed, so closure changes the licence, never the truth-value.  Three dispositions were available; here is where each
finding lands.

1. **No L4 (wrong record).**  Every record I checked resolves to its artifact (section 3.7).
2. **No L2/L3 (measured false pass).**  Section 3.6.
3. **ONE filing, disposition 3 -- `fmtmissargwitness` (LOW):** the `detector:` term's own bound (carrier: "a round using it still owes the
   rung-3 ATTEMPT ... and must record that the attempt was made and what it found") was met for `fmtattr` (the probe IS a boot-path
   reproduction on an unmodified machine) but not for `fmtmissarg`: its witness field says, honestly, "their rung-3 candidates (a
   timer 2/3 hold read, a non-byte MB89352 access, a PPC601 register dump) were not built -- the compiler's diagnostic is exact for a
   missing argument".  That is a recorded NON-attempt, which the carrier says must not render the same as "tried and could not".  The
   dissent, verbatim for the row: *the two guest-reachable sites (a PS2 timer-hold read; a non-byte MB89352 access) were not offered to
   one seat for a single rung-3 attempt before the round was recorded on a detector witness.*  Disposition: a filed LOW item, not a
   round -- the fix is in, the compiler's diagnostic is exact for the class, and a probe built now would be a detector row, with the
   pre-fix behaviour measurable only on `ccd1c502^`.  The owner may drop it as documented-only; the record then says "not attempted,
   dropped by ruling", which is the honest state.  Not a wrong record, so not L4.
4. **Two wording notes on the dismissal comments (section 4, #126/#127 and #130):** GitHub comments are not records the gates read;
   they are recommendations, and the plan's generator (`mkplan.py`) is where the text lives, so a one-line edit there before the
   re-derivation carries them.  Not owed.

## 6. What I did NOT rule on

* The ARC round itself (`arcmemdescnr`): design confirmed in section 1; its witness, fix and detector are HELD by the owner's
  classifier-stop rule and are not mine to advance here.
* `fmttruncinherited` / `#585` (queue item 5) and the census row `fmttrunctree`: separate items, separate ruling.
* The owner's GitHub repository setting (Default -> Advanced): the owner's.

## 7. What reading could not settle

* **GitHub's behaviour on the first push.**  The plan warns that 909 new C files under the ignored paths (907 of them pvrrenderexit
  copies) would, under the DEFAULT setup, open artifact-copy alerts by the hundreds, and that the Advanced setup -- whose workflow
  file is committed but takes effect only once it is on GitHub and the Default setup is switched off -- avoids that churn.  Whether a
  Default-setup analysis and a later Advanced-setup analysis under the same category `/language:c-cpp` supersede each other's
  results cleanly is a GitHub behaviour I cannot verify by reading this repository.  The plan already defers the order to the owner;
  I add only that the dismissal step must follow a FRESH fetch after whichever order is chosen, which `dismiss.sh`'s refusals enforce.
* **The Alpha disassembler's first switch** (`cpu_alpha.c:307-356`): I verified the inner arms `0x27..0x2f` and the outer list's first
  twelve entries, and rely on two independent full readings (Astra, Gemini) for the remaining outer entries.  The second Alpha
  switch and the M88K switch I verified completely.
* **Pass 2b's `file_ecoff.c` repair has no measured detector on the host that measured it** (LP64: the pre-repair `%08lx` with `off_t`
  did not warn).  Correct by reading; a 32-bit-`long` host's compiler would be its detector.  Disclosed above; not a breach.
* **The disclosed type-compatible population** (48 radix, 39 narrowing): Astra's counts from pass 2, quoted in the CHANGELOG.  I did not
  re-count them; the contract claims one row and discloses the rest, so the counts are descriptive, not load-bearing.

## 8. Disposition of the held stages

This ruling discharges the `FABLE FINAL` hold on the regress stage of `fmtattr` and `fmtmissarg` with the answers in section 3 (all six
"yes" except as refined there), confirms the dismissal plan for the 16 rows, and grades the four items.  The ledger entry (seat
`fable5`, phase `regress`, dated after 2026-11-05, pointing at this file) and the `fmtmissargwitness` filing are for the main loop to
write; I was told to write this file and nothing else, and I have.

`FABLEI4: 4 ITEMS GRADED (3 REAL+LOW, 1 FALSE POSITIVE); #584 RATIFIED AS SHIPPED, CHAIN CLOSED (0 breaches over the stated denominator); 16 DISMISSALS CONFIRMED, 0 CORRECTED, 2 WORDING NOTES; 1 ITEM FILED, 0 L2/L3/L4`
