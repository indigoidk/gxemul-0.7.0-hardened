# m_memc (agent a3a5ac29b58a7c4f2).  Final text 2026-11-04T08:16:21.594Z by claude-opus-4-8.

Both clones removed; `build/` and `build-asan/` `dev_mvme187.c` still byte-identical to SEC, and no `.MUTANT` sentinel remains in any project tree. Here is the full report.

---

OPUS_SEAT_ALIVE_20261104_MMEMC

**VERDICT: ORDER-CONFIRMED** — removing the exits while the unbounded pre-switch read stands makes the latent out-of-bounds read live under ASAN (`dev_mvme187.c:68`); adding the draft's bound makes it clean. One measured nuance qualifies it (below).

**DRAFT: 21/21** — the draft passes the witness probe (RESULT 21/21, CONTROL OK, SYMPTOM ABSENT, RED none); every declined access returns 0; the declined memconf write leaves memconf unchanged; both former exit sites now announce once and the session continues.

### Results table

| variant | access | result | artifact |
|---|---|---|---|
| A1 — exits→declines, default `odata=0`, **no bound** | `ld.bu` +0x7c / +0xff (ASAN) | **ASAN: none**, prompt returns, rc=0 | `out_asan/A1_off_7c.txt`, `out_asan/A1_off_ff.txt` |
| A2 — exits→declines, pre-read value flows out, **no bound** | `ld.bu` +0x7c (ASAN) | **heap-buffer-overflow READ size 1 @ `dev_mvme187.c:68`**, rc=1 | `out_asan/A2_off_7c.txt` |
| A2 | `ld.bu` +0xff (ASAN) | **heap-buffer-overflow READ size 1 @ `dev_mvme187.c:68`**, rc=1 | `out_asan/A2_off_ff.txt` |
| A3 — the draft (bound added) | `ld.bu` +0x7c / +0xff (ASAN) | **ASAN: none**, prompt returns, once-message prints, rc=0 | `out_asan/A3_off_7c.txt`, `out_asan/A3_off_ff.txt` |
| A3 — the draft | repo probe | **21/21**, CONTROL OK, SYMPTOM ABSENT, RED none | `out_plain/probe.out` |
| A3 | `ld.bu` +0x0c / +0x7c / +0xff / +0x10c, read r2 | **r2 = 0x0** each | `out_plain/rd_0x0c.txt` … `rd_0x10c.txt` |
| A3 | `st.b` 0x7→+0x08, then `ld.bu` +0x08 | **r2 = 0x3** (memconf unchanged); "memconf write 0x7 declined (once)" | `out_plain/memconf_wr_then_rd.txt` |

All artifacts under `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus_20261104\m_memc\` (diffs: `A1_*.diff`, `A2_*.diff`, `A3_*.diff`).

### Verbatim ASAN text (A2, +0x7c; `out_asan/A2_off_7c.txt`)
```
==1288==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x774c505e0e3c at pc 0x57e51bfd8140 bp 0x7fff47c7bad0 sp 0x7fff47c7bac0
READ of size 1 at 0x774c505e0e3c thread T0
    #0 0x57e51bfd813f in dev_mvme187_memc_access /tmp/gxopus_memc_asan/src/devices/dev_mvme187.c:68
```
+0xff is identical bar addresses/pid (`#0 … dev_mvme187.c:68`). The allocation note reads `0x…e3c is located 0 bytes after 124-byte region […] allocated by […] devinit_mvme187 /tmp/gxopus_memc_asan/src/devices/dev_mvme187.c:101` — confirming (MEASURED) the register file is exactly 124 bytes, so +0x7c (=124) is the first byte past it and +0xff (=255) is deep past it.

### What is settled
- **(a) Ordering claim — CONFIRMED, with a nuance.** The draft's own `odata = ((uint8_t*)&d->memcreg)[relative_addr]` at line 68 is the out-of-bounds read. When the exits are removed and that read is left unbounded **and its value is allowed to flow out** (A2, the minimal "just delete the exits" edit), ASAN reports a heap-buffer-overflow READ of size 1 at `dev_mvme187.c:68` at both +0x7c and +0xff. Moving the read inside the serving arms (A3, the draft's bound) makes both offsets clean. So the bound must land with or before any change to the exits. (MEASURED.)
- **Nuance (MEASURED, matters for the detector):** A1 — where the default arm instead assigns `odata = 0` — did **not** trip ASAN at `-O3`. The optimizer proves the pre-switch load dead on the default path and drops it, so no out-of-bounds access occurs. This is the same mechanism the witness recorded for the pre-fix build (the `exit(1)` made the load dead). Consequence: whether an "exits-removed-but-unbounded" state exposes the read depends on the exact decline form; a kill-table row that only checks "exits removed" could miss the exposure. The robust guarantee is structural — the draft's bound (read only inside the arms) — not any particular decline body.
- **(b) The draft.** Probe 21/21 (the four former-fatal rows — `rd 0x0c`, `rd 0x7c`, `rd 0xff`, `wr cnf` — now exit0 with the prompt back). Declined reads return r2 = 0x0 at +0x0c, +0x7c, +0xff, and +0x10c (+0x10c folds to controller-1 offset 0x0c; announce text "offset 0xc"). The declined memconf `st.b` of 0x7 does not stick: a re-read of +0x08 in the same session gives 0x3, the DEVINIT value. Both sites announce once ("unimplemented read from offset … (once)", "memconf write 0x7 declined (once)"). (MEASURED.)

### What is not settled (out of scope here)
- Whether a memconf **write** should be DECLINEd vs ACCEPTed (the draft's open design point: 187Bug may write the DRAM size code and compare its read-back). That is a firmware/datasheet question, not measured here — READ/REASONED only.
- The draft's other open points: controller-1 folding onto one struct, and whether in-range unimplemented offsets (0x0c..0x7b) should return the struct byte vs 0. Not measured.
- Widths other than a byte, stores other than to memconf, and controller-1 offsets beyond chipid — not measured.
- No detector/kill-table was built (not asked); the A1 nuance above is the one finding a detector author should weigh.

All work was in the two scratch clones (`/tmp/gxopus_memc`, `/tmp/gxopus_memc_asan`), both now removed; project trees untouched.
