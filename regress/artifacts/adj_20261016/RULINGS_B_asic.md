# RULINGS -- packet B (asiceventaddr), 2026-10-16

Consolidated by the main loop (Opus 5.5, 087a90) from three independent adjudications of `packet_B_asic.md`:

| seat | answer | verdict |
|---|---|---|
| GPT-6 Astra (ultra) | `astra/B_asic/codex_adjB.txt` | UPHOLD WITH CHANGES (3 changed) |
| Grok 4.7 (xhigh; its answer's FIRST `VERDICT:` line quotes STATUS.md's summary -- its own verdict is the second) | `grok/B_asic/grok_adjB.txt` | UPHOLD WITH CHANGES (2 changed) |
| Fable 5.1 (clean claude-fable-5-1; MEASURED in `/tmp/gxfable_adjB`, 249 logs in `fable5/meas_B/`, MANIFEST.md5 verified) | `fable5/fable5_adj_B_asic.md` | UPHOLD WITH CHANGES (3 changed) |

Roster 3 of 3.  The two measured breaches (F1, F2) and pins A/B/C stand unanimously; every change is a refinement of
scope or wording, and the load-bearing ones are MEASURED.

## Final rulings

- **F1 -- UPHELD (3/3).**  Pin A at `size_t` width: `unsigned long long rw_len`, `%llu`, compare `== 8`, sentinel
  `~0ULL` -- Fable measured it green on BASE, HEAD, `(size_t)8` and every equivalent, red on `0x100000008`.  (Grok: the
  stub's own `n = len < 8 ? len : 8` clamp is why the wide length also hid from AddressSanitizer.)  Fable's precision:
  TRIGGER's call arguments are not DEPENDS-ON predicates, so the clause is (e) + L3/L4 (a claimed pin implemented at the
  wrong width); the disposition -- repair in this build -- is unchanged.
- **F2 -- UPHELD (3/3).**  Pin B (AddressSanitizer).  The object is pinned FROM BELOW: at least 8 accessible bytes at the
  passed pointer during the instrumented accesses, on PROD ID and TVAL only (Astra's F14 wording; Fable).
- **F3 / D3 -- UPHELD (3/3).**  Pin C MEASURED (Fable `pinned_mw2`: a stub `MEM_WRITE` drifted to 2 -> FAIL ID+TVAL,
  `wflag=2 (MEM_WRITE is 1)`).  Record 3 is then rewritten to describe the PINNED behaviour, which makes the cases-file
  sentence true rather than reversed.
- **F4 / D2 -- REFINED (Fable, MEASURED; Astra and Grok upheld the row).**  The argument-shape class is the macro block's
  FOUR parenthesised operand sites, not two: `(e) >= 0`, `(e) < 96` (RANGE_OK), `4*((e)>>5)` (TO_ADDR) and `((e) & 31)`
  (TO_BITMASK).  One `1 ? 200 : 5` refusal kills the two RANGE_OK drops (measured, oracle-shaped: one `error:` line, the
  RANGE_OK note, both legs, both routes) but leaves `A_enoparen` and `B_enoparen` green; the IN-DOMAIN raise `1 ? 33 : 0`
  exposes them (address `0x5f6984` for 33 under A; payload `0x100000000`, the bit lost, under B).  **The repair (Fable's
  `pinned_shape`, measured: BASE and HEAD PASS at 9272/9153 on both legs, TVAL "96 + 16 + 2 of 2 argument-shape raises",
  all four drops red, no false red):** `SWEEP_SAMPLES += ("1 ? 200 : 5", 200), ("1 ? 33 : 0", 33)`; TVAL gains
  `TX(cond33, 1 ? 33 : 0, 33)` and `TX(or33, 32 | 1, 33)` (`fable5/meas_B/diffs/shape_cases.diff`, `shape_driver.diff`).
  The expression is passed WITHOUT an extra outer parenthesis (Astra -- one would mask the defect).
- **F5 -- UPHELD (3/3).**  The census disclosure stands; record 4 (six lines at e483d931).  Fable names the closure's cost
  for the filed coverage debt: `gcc -MM` over 122 `.c` files under `src/devices` per gate run.
- **F6 -- UPHELD (3/3), no row.**  The class table lists `cpu->byte_order` and the `MEM_PCI_LITTLE_ENDIAN` length bit as
  UNPINNED BY DESIGN (unobservable through a count-pinned serializer call; the flag bit reds `slen`), plus the stub's
  `struct cpu` surface (`mem` and `memory_rw` only) as RED BY DESIGN (Fable; also `prescreen_asic.md` item 10).  Grok: a
  third `byte_order` value would not round-trip but lies outside the field's domain.
- **F7 -- REFINED (Grok; Astra).**  Disclose `static uint8_t buf[8]` AND the measured larger objects `buf[9]`, `buf[16]`,
  `buf[64]` (green under the shipped stub, `sizeof` and AddressSanitizer), as storage-duration/size coverage, without
  claiming reentrant equivalence.
- **F8-F13 -- UPHELD (3/3).**
- **F14 -- REFINED (Astra).**  Records 1, 2, 5 stand; the extent sentence says "at least eight accessible bytes at the
  passed pointer", and ID/TVAL are recorded as running with the extra sanitizer flags.
- **F15 -- OVERTURNED (Astra).**  deepseek's own verdict was BREACH on the short buffer
  (`panel_20261013_234442/ollama_deepseek.txt:4`); "BUILT" was its quotation of the builder's summary -- my error.  And
  grok's panel CLEAN explicitly excluded the short-buffer case, so F2 does not refute it; F1 does.
- **F16 -- UPHELD (3/3)**, measured by Fable in exactly that form.
- **D1 -- REFINED (3/3): AddressSanitizer, upheld ON MEASUREMENT, with a VOID preflight inside the instrument.**  Fable:
  `ptr8`, both casts, `buf + 0`, `(size_t)8`, `u64obj`, `static8`, `buf16` green; `ptr4` (a pointer to a 4-byte
  allocation) RED under ASan and an ESCAPE under OM's `sizeof` form -- PIN's argument proved by measurement.  Without a
  preflight, a toolchain lacking libasan reports `FAIL [PROD.ID, PROD.TVAL]` (measured: `cannot find -lasan`) -- a
  header-defect verdict from a toolchain fact; with a compile + link + RUN preflight it is `SYSASIC_RANGE_VOID` with the
  reason named (measured).  Astra: state ASan's scope (instrumented access checking; a short array MEMBER inside a larger
  struct is a named, unrun limitation).  The stage-5 `cc -m32` leg owes a re-run under pin B (Fable).
- **D4 -- UPHELD (3/3).**

## What the packet missed (all MEASURED or READ; all go into the build)

1. **Re-run table 2 and the 395 one-token media on the REPAIRED instrument** -- one comparison owes one instrument; the
   pinned stub changes the record format; the nine paren/cast removals are reclassified (four DETECT, five
   EQUIVALENT-disclosed).  The `earlier74` comparison is a transition record and is not re-run (Fable).
2. **Counts that move with the samples:** the docstring's "9152 of the 9270" (twice; `check_score_claims` reads the
   docstring) and the gate comment's "54 samples ... 9152 of their 9270" become 56 samples, 9272/9153; TVAL 114 (Fable).
3. **Three record defects in the frozen build** (Astra): PRETABLE:25's denominator (114 header media = BASE + HEAD + 112
   variants, + 9 TU media = 123), PRETABLE:66's arithmetic citation (cite `finalpass_20261013/opus5/logs/enum_bands.out`),
   SUMMARY:232's "no FAIL line anywhere" (gate2.out carries intentional selfcheck FAIL diagnostics).
4. **The class table goes INTO the contract** (Fable §3: sixteen parameter/extent cells, each PINNED with its measured
   kill and greens, or named BY DESIGN: the return value, `byte_order`/`MEM_PCI`, the extent's upper side, payload bits
   33-63).  Grok: `tmp1`'s type narrowed to 32 bits is equivalent (the address fits); `tmp2` narrowed is red.
5. **The ten `prescreen_asic.md` LIVE items** (records: the two correction lists that diverged on 10-13, the `29b450c`
   credit, two unrecorded August panels in the volatile scratchpad, "never fired" text in three places,
   `pass2_ledger.tsv:95-96`, the third inert-remedy site at OB:21609-21611, the erratum placement, the final-pass seat
   record, the C89 docstring clause; coverage: the stub struct layout) -- routed to packet D.

## Build list for the next asiceventaddr build (Opus 5.5; PRETABLE first)

Fable §7 as the delta: pins A (size_t), B (inside `run_row`, with the VOID preflight), C; the two SWEEP samples and two TX
raises; gate pins 9272/9153, 56 samples, TVAL 114; the class table and the four by-design cells in the contract; CATCHES
gains the argument-shape class and the extent "at least 8, on PROD ID and TVAL under -fsanitize=address"; records 1-5 as
refined; F7's disclosure; the three PRETABLE/SUMMARY corrections; re-run table 2 and the one-token media.  Then the
closing pass verifies the two enumerations (the fixture class's sixteen cells; the argument-shape class's four sites x
{out-of-domain, in-domain}) rather than hunting.

## Self-review recorded (Fable §6, badge A)

The 10-13 ruling named fixture pins and never typed them, placed TRIGGER outside DEPENDS-ON so the fixture class closed one
cell per pass across three passes, took product-identity as the equivalence rule for a macro whose domain is argument
expressions, never anticipated a toolchain-feature VOID, and omitted the stub's `struct cpu` surface.  None of the ten
SHIP-WITH-CHANGES items is overturned.
