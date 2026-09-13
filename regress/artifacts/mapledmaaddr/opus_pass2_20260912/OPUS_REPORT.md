OPUS_MAPLE_P2_20260912 — the Opus 5 measuring seat's pass-2 report on `mapledmaaddr` (#528), verbatim, saved because an
Agent seat leaves no file in a panel dir.  Brief: _scratchpad/brief_maple_pass2_20260912.md.  Every artifact it cites is in
this directory.
`# CHECKPOINT -- 2026-09-12 ~12:4x   HEAD 7457c04 (records)`

**VERDICT: SURVIVOR: `} else {` -> `} else if (d->dmaaddr & 0x1f) {` on the read arm of case 0x04. It scores 16/16 (`opus_pass2_20260912/probe_M_ALIGNDECLINE.raw`), and on a nonzero 32-byte-aligned value it reads back 0x0 where the fix reads 0x0c0f0000 (`discrim_M_ALIGNDECLINE.raw`).** Six more mutants also scored 16/16. All seven are proven non-equivalent to the fix by a separate discriminator probe.

**Setup.** I cloned `build/` to `/tmp/gxopus_maple2`, copied in the SEC fix (cmp CLEAN), and ran the detector from a frozen copy (`maple_dmaaddr_probe.FROZEN.py`, cmp IDENTICAL to `regress/`). Driver: `opus2_table.sh`, mutator: `mut_opus2.py`, one diff per leg in `diff_<leg>.txt`. **BASE scored 16/16** (`probe_BASE.raw`). Every mutant build returned rc=0 with a FRESH binary, and every log ends in `MAPLE_DMAADDR_PROBE_DONE`.

| mutant (edit to the fixed read arm) | 16-row score | failing | discriminator (`discrim_<leg>.raw`) |
|---|---|---|---|
| **M_ALIGNDECLINE** `} else if (d->dmaaddr & 0x1f) {` | **16/16** | none | 9/10: `read aligned` got 0x0 |
| **M_ENDECLINE** `} else if (!d->enable) {` | **16/16** | none | 9/10: `read enabled` got 0x0 |
| **M_ALIGNEXIT** after the load: `if (d->dmaaddr != 0 && !(d->dmaaddr & 0x1f)) { fatal(TODO); exit(1); }` | **16/16** | none | 8/10: `read aligned`, `aligned exit` |
| **M_ENEXIT** after the load: `if (d->enable) { fatal(TODO); exit(1); }` | **16/16** | none | 8/10: `read enabled`, `enabled exit` |
| **M_NOPREFIX** `fatal("[ maple: TODO: read from dmaaddr ]\n");` before the load | **16/16** | none | 9/10: `any output` = yes |
| M_LENEXIT `if (len != sizeof(uint32_t)) { fatal; exit(1); }` (width is disclosed) | 16/16 | none | 8/10: `read16`, `read16 exit` |
| M_THIRDREAD `static int n; if (++n > 2) { fatal; exit(1); }` | 16/16 | none | 8/10: `third read`, `third exit` |

Scores are in `SCORES.txt`. The discriminator is `discrim_opus2.py` and its results are in `DISCRIM.txt`; BASE scores 10/10 there (`discrim_BASE.raw`).

**Q1: why these survive.** The fix's own comment names the field's consumer, `maple_do_dma_xfer()`. That function tests two partitions of the device state:
- `!d->enable`, at `dev_dreamcast_maple.c:384`;
- `addr & 0x1f` ("DMA transfers must be 32-byte aligned"), at `:396`.

The detector never builds the reachable side of either one:
- **Alignment:** every nonzero value any row writes has nonzero low five bits (0x8c012345, 0x0c00001f, 0x4, 0xffffffff, 0x13579bdf). A 32-byte-aligned nonzero value is the only class a working driver can write, because the consumer rejects anything else. No row writes one.
- **Enable:** no session writes MAPLE_ENABLE, so `d->enable` is 0 in every row.

M_ALIGNDECLINE is the canonical (d) shape, `if (X)` -> `if (X && Y)`, applied to the dominating `writeflag != MEM_WRITE` arm. Its Y reads `d->dmaaddr`, which is the body-read field, so it falls inside the DEPENDS-ON bound as the brief states it. Under Fable's pass-1 rule, "value-keyed = clause (e)", you could argue it down to (e). But the contract does not disclose it as (e): the NOT COVERED list covers only value-keyed exits, not value-keyed declines. Either way the record is wrong, and the repair is cheap: one read-back row with an aligned value such as 0x0c0f0000, plus one session that writes ENABLE=1 first. Those two rows kill four of the survivors (both DECLINEs and both EXITs).

**Q2: a row whose channel cannot vary.** `read silent` tests `"dreamcast_maple" in t`, which is a literal substring. It cannot vary under a diagnostic that does not contain that token, and M_NOPREFIX measured exactly that. This is plausible rewording, not a contrived edit: the same file already prints `[ maple_do_dma_xfer: not enabled? ]` at `:385`, which lacks the token. A stronger channel would compare each read session's non-debugger output against a no-read baseline session.

**Q3: contract statements that are false or overclaim.**
1. *"the silence row counts ANY `dreamcast_maple' output … never one literal string"* is false. It is one literal string, just a shorter one; M_NOPREFIX is 16/16.
2. *"DECLINE (the value dropped)"* is listed as caught, with no qualifier. Only the unconditional decline is caught. Declines conditioned on alignment or on enable are 16/16 and appear nowhere in NOT COVERED.
3. The NOT COVERED warrant *"the body copies the field and tests no partition of it"* is true only of the arm itself. The consumer the fix cites does test partitions (`:384`, `:396`), and the rows sample neither reachable cell.
4. *"each MEASURED in the kill table"* overclaims:
   - "masking of high … bits": `killtable_20260912` has only M_MASKLOW, which masks the low five bits. No leg masks high bits. `read val_a` would plausibly catch one, but nothing measured it.
   - "any single SET bit": only bit 30 was measured (M_BIT30). The rest rests on reasoning about the all-ones row.
5. Not disclosed at all: every session reads DMAADDR at most twice, so an effect that starts on the third read is invisible (M_THIRDREAD).

The width disclosure is true, and M_LENEXIT confirms it by measurement (16/16 on the detector, killed by the 16-bit read).

**Restore.** The clone was restored from SEC and rebuilt: `cmp` CLEAN, binary FRESH, and `/tmp/gxopus_maple2/.MUTANT` removed (logged in both `SCORES.txt` and `DISCRIM.txt`, and re-checked by hand). Nothing was written to `GXEMUL-SEC\src`, `build\`, `build-asan\` or `est\`. My only repo write is the new `opus_pass2_20260912\` directory.
