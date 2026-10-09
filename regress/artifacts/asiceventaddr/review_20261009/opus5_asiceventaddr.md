SEAT_ALIVE_20261009_ASIC466
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: RATIFY WITH CHANGES (9) -- not `9ca9cca`'s comment-only disposition, which was wrong and is already superseded, but the `#468`/`#469` guard that replaced it. I measured that guard SOUND: all 17 out-of-domain arguments I tried fail to compile, each with the guard's own diagnostic, a runtime `e` hard-errors, and all 21 events are byte-identical. The row's decode defect can no longer be compiled. **But the guard has NO detector:** I built 4 guard mutants and every one leaves every in-tree raise byte-identical. And **8 wrong records stand**:
- **3 in the header:** `352` should be `288`; "adding an event >= 96 makes it live"; "refuted by measurement ... by two seats".
- **4 in the ledger row:** "5.5x / 352"; "opus5 never fired", although it answered `#466`'s pass 2; entry [2] credits codex with both `RANGE_OK` and the guard, and offers a one-token BITMASK remedy that rejects none of 31/63/95; the `commits`/`witness` fields.
- **No CHANGELOG block** exists for `#466`, `#468` or `#469`.

Seat: opus5 (Opus 5.5, `claude-opus-5-5`), file-reading AND compile-and-measure.
**Conflict disclosure (badge `s`, and `A` where noted):** the guard I am ratifying is my OWN SEAT's 2026-08-26 V3 plus `#469`'s lower bound, and the `352 / 5.5x` error I correct below ORIGINATED in that same seat's answer. Everything load-bearing here was RE-RUN from scratch today; nothing is carried over from that answer.
Tree: `GXEMUL-SEC/` at HEAD `ef577140`. The header and `dev_dreamcast_asic.c` are clean against HEAD (`git --no-optional-locks status`). The header is byte-identical in `est/`, `build/`, `build-asan/` and WSL `/tmp/gxsec-build` (`cmp`).

---

## 0. The brief's premises: four are wrong, and one of them is the brief's own reason for asking me

| premise in the brief | status | how settled |
|---|---|---|
| *"the Agent seats were never fired"*, panel *"ran 6/9"* | **FALSE for opus5.** An Opus seat was fired on `#466`'s pass 2 and answered. The stage was **7/9**: deepseek burned, fable5 was not fired. | READ the subagent transcript `~/.claude/projects/C--DocumentNoSnc-cc-GXEMUL/8e474f41-.../subagents/agent-ae8cdaeb6e2c30095.jsonl` (meta: `"description":"Opus reviews the 466 comment diff","model":"opus"`). It ran 2026-08-26 22:26:14-22:36:39 CDT, every record is `claude-opus-5` (no fallback), and it opens `OPUS_466P2_ALIVE` against `brief_466_pass2.md`. **This is the carrier's documented trap: Agent seats leave NO FILE in the panel dir.** The ledger's held marker (entry [9]) fell into it, and this brief copied it. |
| *"`git log -S SYSASIC_EVENT_RANGE_OK` names ONE later commit, `29b450ce`"*, which *"added ... `(e) >= 0 && (e) < 96`"* | **Incomplete, and it misattributes the predicate.** `git log -- <header>` shows FOUR commits: import, `9ca9ccae`, `29b450ce` (22:46), `4d7b2f41` (23:31). `29b450ce` shipped `((e) < 96)` ONLY, so `-1` compiled clean. The two-sided form is **`#469`, in `4d7b2f41`**. | RAN `git log --format=... -- src/include/thirdparty/dreamcast_sysasicvar.h` and `git show --format=` on each commit. **Pickaxe trap:** `-S` counts OCCURRENCES of the name, and `#469` edited the predicate without changing that count. Use `git log -- <path>` or `-G`. (Unrestricted, `-S` names 12 commits, mostly records/ledger commits. Restricted to `src/`, it names 2: `29b450ce` and `84765ec7`, the latter a gdrom comment. Restricted to the header, it names 1.) |
| codex's *"a THIRD partial guard -- `RANGE_OK` protects ADDR and not BITMASK"* came from the six answers in `panel_20260826_222557` | **IMPOSSIBLE as attributed.** `codex.txt` contains `RANGE_OK` **0** times. Codex finished at **22:34**, before the opus5 seat even proposed V3 (22:36) and before `29b450ce` (22:46). | RAN `grep -c` and READ codex's final answer (lines 2036-2078). What codex actually said (`:2054`): *"At `e=159` ... the adjacent bitmask macro evaluates signed `1 << 31` ... The same caveat affects 127."* That is an OUT-of-domain observation. The "third partial guard" framing is the main loop's 2026-09-17 reframing (ledger entry [2]), credited to codex. |
| the comment is *"held since 2026-09-18"* with dissents only from `panel_20260826_222557` | **Two more pass-2 panels exist on the guard itself, and NEITHER is cited on this row.** `panel_20260826_230207` (pass 2 on `29b450c`) appears only on `seatthinkburn`; `panel_20260826_235440` (pass 2 on `4d7b2f4`) appears **nowhere** in the ledger. | RAN a scan of all 887 ledger rows for each panel dir. Contents: section 5, F3. |

---

## 1. The original brief's question, answered about `9ca9cca` as shipped

*(I am not "the seat that never answered": my seat answered at 22:26. This is an independent re-answer, and where it differs from that answer I say so.)*

**Premises.**
- (P1) *No product code changed:* **TRUE** (READ the diff: 18 comment lines and nothing else). The 2026-08-26 opus5 answer also preprocessed before/after with `cc -E -P` and found them byte-identical (READ from its transcript; NOT re-run by me).
- (P2) *Fork never edited the file:* **TRUE** (RAN `git log -- <path>`: `39748e3c` import, then `9ca9ccae`).
- (P3) *21 defines, max 67, so LATENT:* **TRUE** (RAN: `t_pos.c` compiles all 21 by NAME; values 2..67).
  - **Census caution, and it is live today:** the header now quotes `` `#define SYSASIC_EVENT_FOO 96` `` inside a comment, at the line reading `MEASURED: `#define SYSASIC_EVENT_FOO 96` plus a raise`. A naive regex census reports 22 defines with max 96. The main loop hit this twice (2026-08-26 and 2026-09-17). Census by compiled name, or strip comments first.

**Claim 1, "correct only for e in [0,95]":** **TRUE for ADDR.** MEASURED in E: `0..95` lands on `+0x00/04/08` = `pending_irq[0..2]`; `96` is the first value that does not. **It is not true of the macro PAIR:** inside [0,95], `e = 31, 63, 95` make `SYSASIC_EVENT_TO_BITMASK` evaluate signed `1 << 31` (section 4).

**Claim 2, "e 128..159 -> +0x10 ... CLOBBERS mask_13[0]":**
- **TRUE.** READ `dev_dreamcast_asic.c`, the `case 0x10:` arm: `d->mask_13[r] = idata; dev_dreamcast_asic_tick(cpu, d);`. There is no hack-bit test, the 64-bit idata is truncated into a `uint32_t`, and the tick runs immediately. "Clobber" is the right word.
- **INCOMPLETE:** the true clobber set is **9 mask words / 288 values** (MEASURED, E). `9ca9cca` named 64 of them and omitted the `mask_9` group entirely.
- *"Same for 256..287 -> +0x20"* is ambiguous: `+0x20` is `mask_11[0]`, not `mask_13[0]`.

**Claim 3, "e >= 2048 -> outside the device window":** **TRUE.** MEASURED in E: 2048..8191 are OUTSIDE.
- 6144..8191 land in Maple's window: `0x5f6c00`, `dev_dreamcast_maple.c:654`.
- 2016..2047 land on `+0xfc` and STRADDLE the device end. READ `memory_rw.c`: the `if (paddr + len > mem->devices[i].length)` block clamps `len` and still dispatches, so they hit `default:` and are DROPPED.

**Also wrong in `9ca9cca`:** *"e 96..127 -> +0x0c, +0x1c, ..."* is literally false. 96..127 maps ONLY to `+0x0c`; `+0x1c` is 224..255 (MEASURED, E). `29b450ce` fixed this.

**THE QUESTION, "is a comment the correct disposition?": NO, not as the sole artifact.** Both legs of its rationale fail:
- **The C11 leg ruled out a spelling, not a check.** The negative-width bitfield is clean under `-std=c89 -pedantic-errors -Wall -Wextra`, and under every dialect I tried (MEASURED, A2: c89, gnu89, c99, c11, c17, c23, gnu23, all rc 0 with zero diagnostics).
- **The shape leg analysed only a STANDALONE assert.** A check INSIDE `SYSASIC_EVENT_TO_ADDR` fires at the raise, so a new name cannot bypass it (MEASURED, B: `96` refused with the guard's own diagnostic).

The comment's PLACE (beside the macro) was right; its ARTIFACT was too weak. `#468` drew exactly this conclusion.

**Does anything in `9ca9cca` still matter after `29b450ce`? Yes: one sentence survived verbatim and is now FALSE.** At HEAD, header lines 117-118 read *"Max over the 21 defines above is 67 (67>>5 == 2), so this is LATENT. **Adding an event >= 96 makes it live.**"*
- Since `#468`, adding AND raising such an event is a **compile error** (MEASURED, B).
- Adding WITHOUT raising is **benign**, by the same comment's own HONEST CONTRACT (the paragraph opening `HONEST CONTRACT: the guard fires at a CALL SITE`).
- So the sentence contradicts its own comment's headline (`... AND IT IS NOW ENFORCED AT COMPILE TIME`) and its contract. Codex's 2026-08-26 correction #2 (*"Merely adding an unused #define does not make the runtime defect live"*) was never applied. L4, product comment.

---

## 2. The three dissents

### codex, "a third partial guard: `RANGE_OK` protects ADDR and not BITMASK"

**As a live hole in today's tree: NOT LIVE.** There is no use of `SYSASIC_EVENT_TO_BITMASK`, or of an event number, that escapes the compile-time bound.
- RAN `grep` over `src/`. `SYSASIC_EVENT_TO_BITMASK` occurs exactly twice: its definition, and once inside `SYSASIC_TRIGGER_EVENT`, on the line directly below `uint64_t tmp1 = SYSASIC_EVENT_TO_ADDR(e);`, with the SAME token sequence `e`.
- `SYSASIC_EVENT_TO_ADDR` also has exactly one use, the same trigger macro.
- There are **15** product raise sites (maple 1, gdrom 4, pvr 10), all `SYSASIC_TRIGGER_EVENT(<named #define>)`, covering 13 distinct events in {2..32}.
- No file in `src/` writes the ASIC window directly. The only `5f69` hits in `src/` are the header's `SYSASIC_BASE` define and a map comment in `machine_dreamcast.c`. The device registers through `SYSASIC_BASE`.

**So every BITMASK expansion sits in a statement whose ADDR expansion carries the guard, and an out-of-domain `e` fails the whole translation unit.** (The python probes hard-code decoded constants, e.g. `gdrom_toclen_probe.py`'s `SYSASIC_PEND1 = 0xa05f6904`. Those are test constants, not emulator address generation.)

**As a defect: REAL, but it is NOT a partial-guard defect, and the ledger's remedy is wrong.** BITMASK can never address anything (it is `& 31`). Its only hazard is signed `1 << 31`, and that trigger set **{31, 63, 95} is INSIDE the guarded domain**. MEASURED in D:
- the ledger's "one-token remedy" (`+ SYSASIC_EVENT_RANGE_OK(e)` on BITMASK) **compiles 31, 63 and 95**;
- it yields the same `0xffffffff80000000`;
- UBSan reports `left shift of 1 by 31 places cannot be represented in type 'int'` on the remedy exactly as on the shipped macro.

**The remedy rejects none of the values it is offered for.** The kimi substitute had the right framing on the same 2026-08-26 panel: *"`1<<31` (signed-shift UB in C99) whenever any event ≡ 31 (mod 32) is raised"*. That sentence is recorded nowhere. File it as its own item (section 5, F1); it does not belong to this row.

### kimi substitute ("the rationale fails on both legs") and minimax ("a build-time check would close it")

**DISCHARGED by `29b450ce` + `4d7b2f41`. Confirmed, not merely asserted.**
- **kimi:** its construction #2, *"choke-point compile-time assert ... wrapping the raise"*, is what shipped, in bitfield rather than typedef-array spelling. Its construction #1 (parse the header for define values) and #3 (runtime check at the raise) were not adopted. #1 is the definition-site contract that the HONEST CONTRACT deliberately declines. #3 is unnecessary, because a runtime `e` cannot compile (MEASURED, C).
- **minimax:** its Makefile-enumeration rule was not adopted. Its substance (the feared edit fails at BUILD time) is delivered at the raise site.
- The packet-fed status of both seats matters for scoring: neither MEASURED. The measurement that discharged them came from the opus5 seat (READ, transcript). The header's *"REFUTED BY MEASUREMENT on #466's pass 2, independently by two seats"* overstates this: one seat measured and the kimi substitute reasoned. `29b450ce`'s own message says so (*"by reasoning rather than building"*). Minor L4.

**Is the bitfield bound sound? YES. MEASURED, 24 domain cases + 9 constancy cases + 4 mutants, under the build compiler (`cc` = Gentoo GCC 15.2.1, default `__STDC_VERSION__ 202311L`) with the build's own flags from `build/src/devices/Makefile`:**
- **REFUSED (18 of 18), every one with the guard's OWN diagnostic at `dreamcast_sysasicvar.h:136:35`:**
  - `96, 127, 128, 159, 479, 2048, 6144, (-1), -1, (-32), INT_MIN, INT_MAX, 96u, 4294967295u, 0x100000000LL, (unsigned char)200` give `negative width in bit-field 'sysasic_event_in_range'`;
  - `(0, 50)` and `(0, 100)` give `width not an integer constant`.
  - This is rule 4: each failed for the reason under test.
- **COMPILED (6 of 6):** `0, 95, 'A', 31, 63, 0x5f`.
- **Runtime `int e`: hard error** (`width not an integer constant`) at `-O3` AND `-O0`. **`g++` (side effect): hard error.** enum 50 compiles, enum 100 is refused; C23 `constexpr` 5 compiles, 100 is refused.
- **V2 (negative-size ARRAY) with a runtime `e` COMPILES CLEAN** under the build flags; only `-Wvla` warns. So the header's V2-to-VLA rationale is TRUE (MEASURED).
- **The one non-uniformity (no escape):** a `static const int` argument. In range (5), it is ACCEPTED at `-O1/-O2/-O3` (a `-Wpedantic` warning only) but REFUSED at `-O0`. Out of range (100), it is refused at every level. So *"a bitfield width must be an integer constant and hard-errors"* is exact for runtime variables and optimisation-dependent for const-qualified OBJECTS. Benign: no in-tree caller uses one, and all three build trees use `-O3`.
- **Callers with a runtime event number: NONE** (above).
- **The `#469` pass-2 glm dissent is REFUTED by measurement.** Its claim was *"side-effecting expressions can still bypass the guard"*. A side-effecting or runtime argument cannot compile at all (C, CASE 1 and 9).

---

## 3. The row `asiceventaddr`: can its defect still occur?

**NO. It is no longer latent; it is PREVENTED at compile time.** The only code path that turns an event number into an ASIC address is `SYSASIC_TRIGGER_EVENT -> SYSASIC_EVENT_TO_ADDR`. That path now refuses every value outside [0,95], including the first DROP value (96), the first CLOBBER value (128), the window escape (2048) and the lower end (-1), as MEASURED in section 2. The event number is a compile-time constant at every raise site, so **no guest can choose it**. The defect was never guest-reachable, and now it is not compilable.

**What closes it.**

(a) **DISPOSITION: CLOSE as FIXED by `#468` + `#469`.** The row's `commits` field must name `29b450ce` and `4d7b2f41`; today it names only `9ca9cca`. Its `witness` text (*"LATENT ... 67 < 96"*) is the pre-fix warrant and is stale. Its `hold_question` conflates `9ca9cca` with `RANGE_OK`, which `9ca9cca` does not contain.

(b) **WITNESS: `detector:<path>` -- and that detector DOES NOT EXIST yet; it is owed before closure.** No file in `regress/` (artifacts excluded) or `tools/` mentions `RANGE_OK`, `sysasic_event_in_range` or `negative width` (RAN `grep`). **MEASURED, F: all four guard mutants I built leave the 21 in-tree events byte-identical (21/21 SAME, 21 raises), so no build and no gate can see the guard regress:**

| mutant (a COPY of the header, one line changed) | in-tree build | out-of-domain values that now COMPILE |
|---|---|---|
| `null`: `? 1 : -1` -> `? 1 : 1` (clause d, null repair) | 21/21 identical | 96, 127, 128, -1 |
| `upper`: the pre-`#469` predicate `((e) < 96)` | 21/21 identical | -1 |
| `wide`: `< 96` -> `< 128` (relaxed bound) | 21/21 identical | 96, 127 |
| `noguard`: drop `+ SYSASIC_EVENT_RANGE_OK(e)` (verbatim pre-`#468`, clause b) | 21/21 identical | 96, 127, 128, -1 |
| shipped header | 21/21 identical | none |

**The closing detector, sized from that table:** five negative-compile rows plus one identity row, in a gate such as `gate_offline.sh`. *A compile failure being the PASS condition for three of them is the point.*
- **ACCEPT:** `e = 0` and `e = 95` compile. These pin both bounds from inside: `95` is the window's LAST legal slot, per the accept-row rule.
- **REFUSE:** `e = 96` (first DROP), `e = 128` (first CLOBBER) and `e = -1` (below) each FAIL **with the `sysasic_event_in_range` diagnostic**, so they fail for our reason.
- **IDENTITY:** the 21 named events produce `0x5f6900 + 4*(e/32)` with payload `(1<<(e%32))|0x100000000`. This is `t_pos.c`'s check, and it passes today (MEASURED, A1).
- **MEASURED kills:** `null`, `noguard` and `wide` red on row 96; `upper` reds on row -1.
- **REASONED, not built:** a shrink to `< 95` reds the 95 accept row; `>= 1` reds the 0 accept row; an r==3-only guard such as `((e)>>5) != 3` reds rows 128 and -1.

**The rung-3 attempt (owed by the `detector:` term):** record it as **impossible by construction**. Every raise site passes a constant in {2..32}, so reaching the path would need a NEW raise site, which is laundering under clause (iii).

(c) **Does the BITMASK gap keep it open? NO.** It is a different defect:
- it is not an address decode;
- its trigger set {31, 63, 95} lies INSIDE the domain this row is about;
- the guard is therefore structurally unable to cover it, and so is the ledger's proposed extension (MEASURED, D).

File it separately (section 5, F1).

---

## 4. The BITMASK finding, measured (it belongs to a new row, not this one)

- **Shipped values:** `SYSASIC_EVENT_TO_BITMASK(31) = (63) = (95) = 0xffffffff80000000` (INT_MIN, sign-extended into the 64-bit `tmp2`).
- **Warnings and UBSan:** `-Wshift-overflow=2` flags `dreamcast_sysasicvar.h:141:44` (*"result of '1 << 31' requires 33 bits"*), but that level is NOT in the build flags, so the real build is silent. **UBSan reports it** under `-std=c99`, under `-std=gnu23`, and under `build-asan`'s own flags (`-O3 -fsanitize=address,undefined`): constant arguments are not folded away first. `gate_asan_sweep.sh`'s `sanhit()` greps `runtime error:`, so a LIVE raise of 31/63/95 would surface there *if* a swept workload executed it. Whether the sweep drives Dreamcast that far is NOT established here.
- **Latent:** no defined event satisfies `(e & 31) == 31`. The 21 values are 2,3,4,5,7,8,9,10,12,13,14,15,17,19,21,32,33,34,35,66,67.
- **Remedy: `(1u << ((e) & 31))`.** It is device-equivalent: the pending word after the raise is identical for **96/96** in-domain events (MEASURED). `case 0/4/8` ORs idata into a `uint32_t` and tests only bit 32, so the difference in bits 33-63 is invisible to the device. Its detector is a UBSan or `-Wshift-overflow=2` compile of a TU raising 31.

---

## 5. Changes (the `9`) and filings, by late-dissent disposition

**Category 1, WRONG RECORD -> L4, correct in place:**
1. **Header, `THE CLOBBER DOMAIN IS e IN [128,479] -- 352 values across NINE mask words.`:** must be **288** (9 words x 32). The table directly above it lists two 32-value DROPPED holes, 224..255 and 352..383, inside [128,479]. MEASURED: `CLOBBER total=288 across 9 distinct mask words (13:96 11:96 9:96)`. **Codex found this on `#468`'s pass 2 (`panel_20260826_230207/codex.txt`, final answer finding 4) and it was never recorded or applied.** It originated in my own seat's `#466` answer (`A`).
2. **Header, `Adding an event >= 96 makes it live.`:** FALSE since `#468` (section 1). For example: *"An event outside [0,95] cannot be raised: SYSASIC_EVENT_RANGE_OK makes the raise a compile error."*
3. **Header, `*** BOTH LEGS WERE REFUTED BY MEASUREMENT on #466's pass 2, independently by two seats`:** one seat measured (opus5) and one reasoned (the kimi substitute, packet-fed).
4. **Ledger `state_note`:** *"understated the clobber domain **5.5x** ... 352 values"* must be **4.5x**, **288**. (`29b450ce`'s message carries the same error immutably; the correction lands in the ledger and a CHANGELOG block.)
5. **Ledger entry [9], the HELD marker:** remove `opus5`. It answered `#466`'s pass 2 at 22:26 (`agent-ae8cdaeb6e2c30095.jsonl`). Record that answer as an entry citing the transcript; the stage was **7/9**. Defang the marker per the carrier; do not delete its text silently. *Today's opus5 answer is strictly later in the same stage anyway.*
6. **Ledger entry [2], three false statements:**
   - (a) *"Found by the codex seat in panel_20260826_222557"*: codex could not see `RANGE_OK`. Its finding was `1 << 31` at 127/159.
   - (b) *"That measurement is what #468's compile-time guard was built from, and this answer is where it came from"*: FALSE. `#468` shipped opus5's V3 **verbatim** (the transcript shows `sysasic_event_lt_96`, exactly `29b450ce`'s form). Codex proposed a Makefile-wired source enumeration and wrote that C assertions *"cannot discover an unused new definition"*.
   - (c) *"THE REMEDY ... COSTS ONE TOKEN"*: MEASURED to reject none of 31/63/95.
7. **Ledger row fields:** `commits` add `29b450ce`, `4d7b2f41`; `witness` is stale; `hold_question` conflates commits.
8. **CHANGELOG:** there is **no round block for `#466`, `#468` or `#469`**. RAN `grep -c`: `#468` 0, `#469` 0, `#466` 1, and that one is the census line *listing it as unwritten*. `29b450ce`'s 80 CHANGELOG lines are all the `#467` block. `#468`/`#469` put a new macro into product code. The 2026-08-26 opus5 answer already called `#466`'s missing record *"Undischarged obligation"*.

**Category 2, the row's own remaining work (a follow-up commit, measured necessary):**
9. **The negative-compile detector for the guard** (section 3b). The row is still OPEN, so this is not a late dissent against closed material; it is what licenses the closure. Under the vacuity floor it must red on the verbatim reinstatement (`noguard`: yes, row 96) and on a null repair (`null`: yes, row 96). Both are MEASURED.

**Category 3, FILE as new queue items, provenance verbatim:**
- **F1 `sysasicbitmask31`:** `SYSASIC_EVENT_TO_BITMASK` is signed `1 << 31` at in-domain e = 31/63/95. Latent, UB per ISO C (C99 through C23), UBSan-visible, GCC-benign. Fix `1u`. Provenance: kimi substitute, `panel_20260826_222557` (*"whenever any event ≡ 31 (mod 32) is raised"*), and codex, same panel (e = 127/159).
- **F2 (documented-only):** the `static const int` optimisation-level non-uniformity (section 2). No escape; worth one clause in the guard's contract.
- **F3 UNREAD REVIEWS:** record `panel_20260826_230207` (`#468` pass 2) and `panel_20260826_235440` (`#469` pass 2) on this row.
  - `#468`'s codex raised: (3) the lower bound, which `#469` fixed; (4) 288, never applied (change 1 above); plus `#467` items outside this row.
  - `#469`'s panel answered COMPLETE (codex, grok, agy, kimi substitute, minimax, deepseek in plain text); glm dissented and is refuted (section 2).
  - **No Agent seat was fired on either stage** (RAN: no subagent meta in the 23:00-00:30 window). Section H should see two short stages here.
- **Minor L4, sibling file:** `dev_dreamcast_gdrom.c`, in the comment containing `thirdparty/dreamcast_sysasicvar.h names for #466`, attributes the "guard written from the DEFECT" sentence to `#466`. It is `#469`'s (the `#468/#469` block), and it is quoted without the header's parentheticals and with no ellipsis.

---

## 6. READ vs RAN

**RAN** (all compiles in my own scratch dir; the SEC header passed read-only via `-I`; mutants are COPIES; header md5 `daccce33a5df9e7c3093c310153ce92e` before and after; `git --no-optional-locks status` clean for the header and device file):
- `opus5_meas/run.sh` -> `RUN.out`, sentinel `OPUS5_MEAS_DONE`. Legs: A1 positive (`t_pos.c`), A2 dialects (`t_c89.c`), B domain (`t_neg.c`, 24 cases x build flags and c99-pedantic), C constancy (`t_rt.c`, 9 cases x `-O3`/`-O0`), D BITMASK (`t_shift.c` + UBSan c99/gnu23), E enumeration (`t_enum.c`, [0,8192)), F mutants (4 copies, each verified to change exactly one line).
- `run2.sh` -> `RUN2.out`: the const-object behaviour by `-O` level.
- `run3.sh` -> `RUN3.out`: UBSan under `build-asan`'s flags.
- All of these are under `scratchpad/fableq/opus5_meas/`, which is a VOLATILE path. **Copy them into `regress/artifacts/` before any durable record cites a number from them.** I am read-only and did not do it.
- Also RAN: `git log`, `git show --format=`, `cmp` across four trees, and the greps and ledger scans cited above.

**READ** (not executed):
- the device switch and arms (`dev_dreamcast_asic.c`);
- `memory_rw.c`'s straddle clamp;
- the 15 raise sites;
- the build flags (`build/`, `build-asan/` Makefiles);
- all seat answers in the three panels;
- the 2026-08-26 opus5 transcript;
- the four commit messages;
- the ledger row (working tree; its state, commits, witness and 10 entries match HEAD `ef577140`).

**NOT re-measured:** V1, the standalone-assert leg of `29b450ce` (taken from the transcript; true by construction), and the `cc -E -P` byte-identity of `9ca9cca`.
