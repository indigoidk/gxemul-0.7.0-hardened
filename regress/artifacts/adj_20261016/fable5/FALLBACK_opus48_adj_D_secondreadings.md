FABLE_ADJ_D_20261016

Verbatim line from `regress/artifacts/adj_20261016/meas_main/libcq.out`:

    malloc(0) -> non-NULL

# Fable 5.1 adjudication — packet D (the agy pack's grok + Argon second readings)

Independent of the astra/ and grok/ answers (not read). Read: packet D in full; all five
pre-screens in full; the HEAD source for every site I rule on; the HEAD ledger rows for the
three HIGH candidates and their prior-art siblings; Astra's `DISPOSITIONS.md`; OUTSTANDING_BUGS,
CHANGELOG, REVIEW_FINDINGS at HEAD. MEASURED: I built HEAD `e483d931` in a private clone
(`/tmp/fableD`, git archive → configure → make -j8, WSL Gentoo gcc 15.2.1, binary md5
`579abef4...`) and ran a rung-3 host-exit witness; logs in `fable5/meas_D/`. No project tree was
mutated.

READ = I opened the line/ran the grep at HEAD. MEASURED = I ran the built binary. REASONED =
inference from code I read.

---

## VERDICT

**VERDICT: UPHOLD WITH CHANGES (2 rulings changed)** — H1/H2/H3 are all real, unfixed, un-declined
host exits (H1 and H2 now carry a rung-3 witness I measured; both end the host at exit 1 on an
unmodified in-tree machine). The §4 wholesale adoption is sound on a 27-row sample (0 grades
wrong), but "adopt … as written" over-reaches and is narrowed; and the pre-screens missed one
guest-reachable host exit of the H1/H2 class (SH `prom_emul` default, `cpu_sh_instr.c:3833-3834`).

The two changes:
1. **§4 adoption METHOD** (not reversed, narrowed): adopt each CONFIRMED finding, but land the
   line-citation corrections as **grep anchors** (the carrier's own CITATION-FORM rule), and
   **re-run the deriver at commit time** for the self-inconsistent counts rather than transcribing
   either figure — the corrections as written disagree with each other (PDF inventory 20 vs 26;
   the marker census).
2. **One missed new row**: SH `prom_emul` default `exit(1)` — FILE, same class as H1/H2.

Everything else (H1/H2/H3 FILE/HIGH, the other-new-rows list, §3 "none ready", §5 premises, §6's
three libc readings) is UPHELD.

---

## Q1 — H1, H2, H3 (cited lines opened; two measured)

### H1 `ofemulnodata` — UPHOLD: FILE, HIGH. Now MEASURED (rung-3).
READ at HEAD: `src/promemul/of.c:1096-1101` — `of_emul()` reads `cpu->machine->md.of_data` and does
`fatal("of_emul(): no of_data struct?\n"); exit(1);` when NULL. `md` is a **union**
(`machine.h:206-210`) zeroed by `machine_new` (`machines/machine.c:67 memset`); the only writer of
`md.of_data` is `of_emul_init` (`of.c:1078`), called only from `machine_macppc.c:99`, and only after
`if (!machine->prom_emulation) return;` (`:93-94`). The magic instructions decode unconditionally:
ARM `swi 0xef8c64be` (`cpu_arm_instr.c:5034-5036` → `X(openfirmware)` `:988-991`) and PPC `sc
0x44ee0002` (`cpu_ppc_instr.c:4400-4402` → `X(openfirmware)` `:3956-3958`). No privilege/mode test.
No row covers `:1100` (`ofopenexit` is `:448`, `ofpeerexit` is `:394` — different sites; grep for
`of_emul`/`of_data`/`44ee0002`/`ef8c64be` in ledger+OB = 0). **Not declined under another id.**

MEASURED (`meas_D/witness_hostexit.out`): on unmodified `-E testarm`, a liveness control
(`mov r0,r0`) steps and survives (pc 0x8000→0x8004, exit 0); then `00008000: ef8c64be swi 0x8c64be`
stepped → `of_emul(): no of_data struct?`, host **exit=1**. One guest instruction ends the host.
(PPC leg READ-confirmed, not built; same handler.)

Fold: H1, `ofopenexit`, `ofpeerexit` are three sites/predicates in `of.c`, same de-fatalisation
class — a shared ROUND is reasonable under the reopening rule (one fix design), but they stay
**three rows** (different predicates; the option-set member differs — H1 is a dispatcher-reached
NULL, not a refusal of a guest value).

### H2 `mipssyscallprom` — UPHOLD: FILE, HIGH. Now MEASURED (rung-3).
READ: `cpu_mips_instr.c:4650-4657` routes `syscall` with code `0x30378` at ANY address to
`X(promemul)`; its `default:` arm (`:2649-2650`) is `fatal("TODO: Unimplemented machine type for
PROM magic trap\n"); exit(1);` for every machine type outside PMAX/PS2/ARC/SGI/EVBMIPS. `#235`
(`:4659-4669`) gated the **BREAK** form to the reset stub but **SYSCALL was never gated**. Not
`mipsresetalias` (that is the BREAK alias, `:4666`). No row (grep 0).

MEASURED: on unmodified `-E testmips`, liveness `nop` survives (pc →+4, exit 0); then
`ffffffff80100000: 00c0de0c syscall 0x30378` stepped → `TODO: Unimplemented machine type for PROM
magic trap`, host **exit=1**. User-mode, any PC.

### H3 `asccmdwidecount` — UPHOLD: FILE, HIGH (witness REASONED, not built).
READ: `dev_asc.c:987` `len = d->reg_wo[NCR_TCL] + d->reg_wo[NCR_TCM] * 256;` as `int`, passed to
`scsi_transfer_allocbuf(... len, 0)` at `:991-992`. `reg_wo` is `uint32_t[0x10]` (`:154`) and `:1155`
stores the guest's whole `idata`, so a 32-bit store to NCR_TCL makes `len` negative; the COMMAND
path has **no span clamp** (unlike DATA_OUT). `scsi_transfer_allocbuf` (`diskimage_scsicmd.c:151-155`)
does `malloc(want_len ? want_len : 1)` with `want_len` a `size_t` ≈ 2^64 → NULL → `exit(1)`. Reached
via SELATN|DMA, which the #283 comment (`:1014-1016`) records pmax OpenBSD issuing on every command.
I did **not** build this witness (it needs pmax + a disk image + a SELATN|DMA sequence; I spent the
budget on the two single-instruction witnesses). It is rung-3 buildable on pmax per
`ascwidecount_prep/F6`. HIGH stands — arguably a cleaner HIGH than the `ascwidecount` sibling because
there is no clamp to condition on. Fold: H3 + `ascwidecount` are candidates for **one round** (same
register, same store `:1154-1155`; one mask/bound fix covers both). UPHOLD the fold.

### Other new rows — UPHOLD each as the pre-screen proposes:
- MIPS `X(ei_or_di)` skips `cop0_availability_check` (MED, mips_two F11) — **UPHOLD** (READ by pre-screen; a wrong exception, user-mode writes Status.IE where the ISA owes CpU).
- `armcp15c1fallthrough` (MED, armexits F20) — **UPHOLD**; I verified `cpu_arm_coproc.c:124-129` (opcode2≠0 → fatal, `// exit(1);` commented) falls through to the control write `:134-135`; the ARMv6 CPACR contingency (rpi) is met on the CPU half.
- ARM TTB/L2 mask `0x0fffffff` (armdesc3kill F17) — **UPHOLD** FILE; a real correctness bug (tables above 256 MB read from the wrong PA; rpi defaults to 512 MB).
- coarse domain fault before the L2 fetch (LOW, armmmuvehicle F19) — **UPHOLD** FILE LOW.
- Thumb LDR(3) raises Prefetch not Data Abort (armthumbabortkill F8) — **UPHOLD** FILE (sibling), and mark `ledger:48071`'s "UNVERIFIED" verified.
- coarse-L2 type-3 as a 1 KB tiny page (N2) — **UPHOLD** FILE candidate.
- MB89352 `len != 1` diagnostic, 3 conversions / 2 args (N1, LOW) — **UPHOLD** FILE LOW (or fold into `qhmbunimplstops`). Note: this is a genuine guest-reachable **format-string UB**, not cosmetic.
- DEC21143 unbudgeted RX drain under TAP (net_three F8) — **UPHOLD** FILE-or-fold-into-`ne2krxbudget`; I verified `dev_dec21143.c:356-366` (the `while (cur_rx_buf==NULL)` drain) and `:301-306` (drop-all when `drop_packet==NULL`). Panel picks file-vs-fold.
- BE case-4 byte-lane shift "Filed" with no slug (#563 item 9) — **UPHOLD** FILE as coverage debt.
- `pvr`/gdrom F15 → fold into `gdromcondhow` — **UPHOLD** (R3/R4 omit `how` too).
- the two harness-builder faults, one row each (`mk_briefs4.py:17` `severity` vs `sev`; the #554 GOVERNING-TEXT windows, ppc_six F7 = 221 rows / 117 misaligned) — **UPHOLD** FILE.

---

## Q2 — §3: is any fix spec READY? NO. UPHOLD.

None of `agentrefusal` (AR1-6), `asanexit1subtype` (AR10), `batterymissedruns` (AR13/15-17),
`harness_five` (HF1-4,7-9), `probewiring` (PW1-3,5) is ready to build as drafted. The pre-screens
confirmed a concrete defect in each: a RED control that cannot redden under root (`HF2`, uid 0
makes `[ -r ]` always true); a word token aborting `$(( ))` under `set -u` (`HF3`); nothing invokes
`nightly_check.sh` and every verdict since 08-30 is `TREE_DIRTY=YES`, so a FAIL-keyed caller is
permanently red (`AR13`/`AR15`); grok's SessionStart hook `exit 2`s before emitting the JSON
(`AR17`); Argon's heredoc diff does not compile (`PW1`). **Each row stays open with the confirmed
defects attached as the next draft's premises; no draft adopted.** I agree with the coordinator.
(`HF5` genuinely needs one run per `gate_upstream.sh` case before it can be ruled — CANNOT SETTLE,
correctly.)

---

## Q3 — WHICH OF THE CLASS ADOPTIONS IS WRONG? (25+ rows spot-checked, 5+ per file)

**Sample result: every REFUTED/DISPOSED/LIVE grade I re-derived HOLDS (0 wrong).** So the §4/§5
wholesale adoption is defensible in substance. The problem is the **verb "as written"**, for two
reasons named below. Rows I opened at HEAD:

**prescreen_563** — c563_contract F18 REFUTED (SCSI_MAX_XFER_BYTES=64 MiB, `diskimage_scsicmd.c:59`
✓); adj_563_ruling F3 DISPOSED (`PINNED AT ITS EDGE` = 0 hits in e483d931 `tools/CLAUDE.md` ✓);
c563_widths F2 LIVE (`dev_wdc.c:1229-1245` says `consumed` counts ATTEMPTS, names `wdcconsumedattempts`,
which exists in the ledger ✓); c563_candidates F9 REFUTED (`dev_wdc.c:1312` needs `atapi_len==0 &&
atapi_st==NULL` ✓); c563_edges F15 LIVE (OUTSTANDING_BUGS:24607 carries `68930` ✓). **All hold.**

**prescreen_asic** — AR4 DISPOSED (memory.h `CACHE_NONE 2`, so "invented" is wrong ✓); BF16 DISPOSED
(`sysasicbitmask31` filed at OB:24630 ✓); FX5 LIVE-low (cpu.h `machine` first `:348`, `mem` `:385`;
stub puts `mem` first — the layout-mask hazard is real ✓); GT2 REFUTED-grok's-anchor (configure:313
starts with a TAB ✓); BF21 LIVE-minor (pass2_ledger.tsv:95 literally reads "verified at four
boundaries: -1 refused, 0 and 95 compile, 96 and 128 refused" — 5 inputs ✓, and it is a vivid
instance of the ppc_six F7 run-on window defect). **All hold.**

**prescreen_records** — CC1 LIVE (`diskimage.c:1763` = `"NULL ptr");`, guard at `:1879` ✓); CC16 LIVE
(`cpu_sh.c:458` cites `dev_sh4.c:2386-2388` but `:2386` is `case SH4_RTCOR:`; IRLM fatal at
`:2507-2509` ✓); CN13 LIVE (20 top-level `_scratchpad/*.pdf` ✓); CN14 LIVE (`dev_wdc.c:640` cites
`_scratchpad/ata2_x3t10_948d.txt` ✓); DA13 LIVE-low (`run_controls.py:16` "measured passing 48/48",
`:125` "F_selfseat_skip 48/48" on a 49-row instrument ✓). **All hold.**

**prescreen_prep** — armexits F20 CONFIRMED (`cpu_arm_coproc.c:124-129/134-135` fall-through ✓);
ppc_six F12 CONFIRMED (`cpu_ppc_instr.c:4119 exit(1)`, `goto bad` commented, vs `cpu_sh_instr.c:4056
goto bad` ✓); crimectllane F2 CONFIRMED (`dev_sgi_ip32.c:319 goto crime_declined` before the switch
✓); m88k_four F11 CONFIRMED (`cpu_m88k_instr.c:2229` xcr → `m88k_stcr` ✓); mips_two F10 = H2
(MEASURED ✓). **All hold.**

**prescreen_audits5** — of_two F9 = H1 (MEASURED ✓); sgi_harness_five F21 CONFIRMED
(`arcbios.c:1140-1147` store_64bit_word to guest A1 with no alignment test ✓); net_three F8 CONFIRMED
(`dev_dec21143.c:356-366` / `:301-306` ✓); sgire_pcc2_vme F6 CONFIRMED (only `exit(1)` in dev_pcc2.c
is `:435`; width guards call `pcc2_width_decline`, fatal-only latched `:462-469` ✓); osiop_three F7
CONFIRMED (`dev_osiop.c:952-953` stores `idata` even for ADDER, `osiopreg.h:116` ADDER = `ro` ✓);
arcbios_three F13 CONFIRMED (`arcbios.c:1226 cpu->running=0` SGI default; `:1279 V0=ARCBIOS_EINVAL`
non-SGI ✓). **All hold.**

**No grade I checked is wrong.** But "adopt as written" is wrong for two subsets the coordinator
should carve out before the records commits land:

1. **Line-citation corrections must land as GREP ANCHORS, not re-keyed line numbers.** Many §C/RC
   dispositions offer a HEAD line number (e.g. "re-key to :2507-2509"). The carrier's own
   CITATION-FORM rule says a cross-file citation decays at the next edit and should be an anchor. CC16
   is the live proof: the IRLM fatal is `:2507` at HEAD but `:2635` in the working tree (peer added
   126 lines). Adopting the number "as written" re-arms exactly the rot the row is fixing.
2. **The self-inconsistent COUNTS must be re-derived at commit time, not transcribed.** The PDF
   inventory corrections disagree with each other — CN13/CN14 say 19→20, CN15 says 26 via `find`
   (the `lance/` subdir). The marker census (CN2) says 92/14/56.5%. Adopting "every CONFIRMED
   correction as written" would write mutually contradictory numbers. The carrier's counts rule
   already says: a corrected count lands as deriver-plus-demoted-prose, never a fresh literal. That
   rule governs here and §4's verb does not acknowledge it.

A third, smaller caveat: a few items filed under §4 are actually **ruling requests** the coordinator
does separate elsewhere (NC7/NC8 null-medium labels, BN3/BN7 charter/wording, PS3 schema). Those are
correctly NOT in the L4-correction adoption set — I confirmed §4's text scopes to CONFIRMED record
corrections and forwards the rulings to §7 / packet §3. No change needed there, but a reader of §4
alone could over-read "every CONFIRMED record correction."

§5 (premises recorded by pointer, no action now) is sound — it commits nothing but a provenance
pointer.

---

## Q4 — WHAT THE PRE-SCREENS MISSED

**A guest-reachable host exit of the H1/H2 class, in no row, in a file the SH prescreen job did not
open.** `cpu_sh_instr.c:4150-4152`: `else if (iword == SH_INVALID_INSTR) { ic->f = instr(prom_emul); }`
— a machine-independent decode. `X(prom_emul)` (`:3819-3835`) switches on `machine_type` and serves
only `MACHINE_DREAMCAST` and `MACHINE_LANDISK`; the **default is `fatal("SH prom_emul: unimplemented
machine type.\n"); exit(1);`** at `:3833-3834`. So on `MACHINE_BARESH` / `MACHINE_TESTSH` /
`MACHINE_HPCSH` a guest executing the SH PROM-trap instruction ends the host — the exact pattern of
H1 (ARM OF), H2 (MIPS promemul) and `arcsgiprivate` (SGI default). Grep of HEAD ledger + OB for any
SH-prom row = **0**. The `sh_two` prescreen (prescreen_prep) scoped itself to `memory_sh.c`
(`shifetchkill`/`shreservedexit`) and the ppc_six F12 row cites `cpu_sh_instr.c:4055-4056` (the
ifetch `goto bad`, the *good* sibling) — neither touched the `prom_emul` default at `:3833`.
**Recommend: FILE a new candidate** (severity MED-to-HIGH — reachable but on SH types not commonly
booted; the main loop/owner should rank it against the HIGH promemul siblings). I read it, did not
build it (one SH witness would mirror the H1/H2 recipe).

Two smaller points:
- The pre-screens graded H1/H2/H3 **READ-only**. A rung-3 witness was cheaply available (one guest
  instruction) and I built it for H1 and H2. The lifecycle's "ask one seat to try a rung-3 probe
  before recording a row as witness-less" step was not applied to these three; it is the cheapest
  thing in the file and it upgrades the evidence from a reading to a measured host death.
- The `dreamcast_scramble.c` 15 `exit(1)`s (the largest single-file exit count in the census) are
  correctly NOT guest-reachable: they run only at image-load time (`file.c:339
  dreamcast_descramble`), under the host-side image charter. No miss there.

---

## Q5 — §6's reading of the libc measurement (all three correct)

`meas_main/libcq.out` was produced on x86-64 glibc 2.42, gcc 15.2.1 — the build host. The three
readings are right:

- **arcbios F9 / `arczeroalloc` / `dectxzero` (the `malloc(0)` leg):** `malloc(0) -> non-NULL`, so a
  NULL-means-OOM `exit` after `malloc(0)` is **not reached on this host** → portability exposure only
  (C99 permits NULL elsewhere). **Correct.** The HIGH grade rests on other libcs, which stays CANNOT
  SETTLE.
- **net_three F16 (`dectxzero`, the `realloc(p,0)` leg):** `realloc(p,0) -> NULL (errno=0)`, block
  freed — so a site that treats `realloc(p,0)==NULL` as OOM **IS reached on this host**. **Correct.**
  The cited site `dev_dec21143.c:788-789` feeds `CHECK_ALLOCATION` (`misc.h:190-192` exits only on
  NULL), so the exit is live here. Check the handling at the site, as §6 says.
- **loaders_four F7 (negative `fseek`):** `fseek(f,-8,SEEK_SET) -> -1 EINVAL, position unchanged`
  (ftell=5). **Correct.** A negative seek fails cleanly; the `file_ecoff.c` loaders ignore the fseek
  return and exit only on a short `fread`, so position-unchanged means the next read takes bytes from
  the current offset — "reads the wrong bytes", which is exactly the row's conditional. Consequence
  depends on the caller's return check, as §6 says.

The remaining CANNOT SETTLE items (macppc NetBSD boot; clean-checkout sweep; 32-bit libc; backtrace
rerun; vector-unmapped rerun) stay unsettled — my single-host measurement does not touch them, and
the 32-bit/other-libc portability exposure for the `malloc(0)` rows genuinely needs a different
libc.

---

## Rulings CHANGED from the coordinator's (the two)

1. **§4 adoption method** — not reversed; narrowed from "adopt every CONFIRMED record correction *as
   written*" to "adopt the finding; land line citations as grep anchors (carrier citation-form rule);
   re-derive the inconsistent counts (PDF 20-vs-26; marker census) at commit time per the carrier
   counts rule." 27/27 sampled grades were correct, so the findings stand; only the verb changes.
2. **Completeness** — added one new-row candidate the pre-screens missed: SH `prom_emul` default
   `exit(1)` (`cpu_sh_instr.c:3833-3834`), a guest-reachable host exit of the H1/H2 class, in no row.

H1/H2/H3 (FILE/HIGH), the other-new-rows list, §3 (none ready), §5, and §6's three readings are all
UPHELD. H1 and H2 carry a rung-3 witness I measured (`meas_D/`); H3's witness is owed (REASONED).
