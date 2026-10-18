# `#564` sgirekills (MTE half) -- PASS 2: the diff, the detector and its kill table

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a fact from something this brief did NOT give it is worth more than
a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/` AT HEAD `2951694f` PLUS THIS ROUND'S UNCOMMITTED WORKING-TREE CHANGES** to
`src/devices/dev_sgi_re.c`, `regress/gate_arm.sh` and the new `regress/sgi_mte_decline_probe.py` -- all three inlined
below.  The working tree also carries another session's uncommitted edits to OTHER files (`dev_lca.c`, `dev_pcc2.c`,
`dev_sh4.c`, `cpu_alpha_palcode.c`, some regress files); they are not this round's.  Ignore the pristine upstream
copies of GXemul under the project root (`./src/`, `_archive/...`).

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle.

**VERDICT LINE FIRST.**

---

## 1. What pass 1 decided (three seats answered; full record `pass1_564_20261017/CONVERGENCE.md`)

GPT-6 Astra, Grok 4.7 and GLM 5.3 each answered PROCEED WITH CHANGES; Fable 5.1 was a SEAT FAILURE (HTTP 429, usage
limit), its stage held by owner ruling.  Unanimous design: **member 3 (decline the transfer, latched announcement) at
all five sites**, `return` OUTSIDE the latch, S2 kept as `src > MTE_TLB_C` for fills and copies, one latch bit per site
(`1 << 13` .. `1 << 17`), messages carrying the refused value and `-- transfer declined (once)` with each old key phrase
kept.  Detector rows were added for every hole the three seats named: BYTEMASK never written (the reset default), the
whole refused source domain {3,4,5,6,7}, S1/S2 at every destination kind, S3-S5 at both linear labels, all refused
depths at both labels, the 32 single-zero masks, a same-session five-site latch row and an existing-bit row, linear
fixtures that map the page in only the selected array, the PROM's own mode `0x11`, tiled transfers with a partial mask,
and a decline followed by a working transfer.  Declined: moving S5 above the linear arm's `debug()` (host-only, minimal
diff).  Filed for later rounds: S2 narrowed to COPY (needs a hardware warrant); IMPLEMENT at S4/S5; START honoured on a
READ of a START-tagged address (Astra).

**Settled premises -- each with its warrant, so no seat need re-derive them:**
* `fatal()` RETURNS.  `src/core/debugmsg.c:384-391` is `va_start; va_debug(argp, fmt); va_end;` and nothing else -- no
  `exit`, no early-out.  A declined site is `fatal()` once, then `return`.
* A transfer runs only on a WRITE whose address carries the START bit (`0x800`): `DEVICE_ACCESS(sgi_mte)` takes
  `startFlag = relative_addr & CRIME_DE_START` and masks it off before decoding (section 3c).  So the largest register
  index is `0x7ff / 4 = 511` and the 64-bit arm's `regnr + 1` stays inside the 1024-word `mte_reg[]`.
* `CRIME_DE_STATUS` is the constant `0x1e000000` (`DEVICE_ACCESS(sgi_de_status)`), which is why it is the probe's
  device-signature control.
* `BYTEMASK` is zero at init: `dev_sgi_re_init()` allocates ONE `struct sgi_re_data` and `memset`s it to zero
  (`dev_sgi_re.c:864-865`), and `dev_sgi_mte_init()` registers the MTE window over that same struct (`:871`, `:1873-1877`)
  without writing any register.  So a guest that never writes BYTEMASK reaches S5 with mask 0 -- the `mask unwritten`
  row.

## 2. The measurements (every number names its log, all under `regress/artifacts/sgirekills/`)

| what | HEAD `2951694f` (scratch build) | the fix (same tree, only `dev_sgi_re.c` replaced) | log |
|---|---|---|---|
| rung-3 witness `witness_20261017/sgi_mte_exit_witness.py` (md5 dcbb328d) | 4/9 -- five deaths, each with ONLY its own text | 9/9 -- five survivals, own text present | `witness_20261017/witness_HEAD_2951694f.out`, `witness_FIX_564.out` |
| detector as TABLED (md5 8d625289, 14-column names) | 8/53 -- controls 3 and ACCEPT 5 green, every decline row `died` | 53/53 | `detector_564_20261017/probe_HEAD_2951694f.out`, `probe_FIX_564.out` |
| detector as SHIPPED (16-column names, otherwise identical) | see section 6 | see section 6 | `detector_564_20261017/probe_*_shipped.out` |
| null medium (`/bin/true` as the binary) | -- | 0/53 | `killtable_564_20261017/raw/null.out` |
| kill table, 34 one-edit mutants of the fix | -- | **34/34 caught** | `killtable_564_20261017/KILLTABLE.txt` (section 5) |
| kill table 2: the two ACCEPT-side growth mutants table 1 lacked (S1 and S3), SHIPPED instrument | -- | **2/2 caught** -- `s1grow` 52/53, `s3growa` 50/53; base 53/53, null 0/53 | `killtable_564_20261017/KILLTABLE2.txt` (section 5d) |

**A CONSTRUCTION DEFECT OF MINE, CAUGHT BEFORE ANY TABLE (L1):** the detector's first draft (md5 ceed62be) compared the
`lw` result -- which SIGN-EXTENDS, so the paint `0x99999999` reads back as `0xffffffff99999999` -- against the 32-bit
literal.  Every `paint kept` row read "written" on the fixed build, and every `landed` row was vacuous (a surviving paint
also differed from the literal).  Fixed by masking each read to 32 bits; both builds re-run on the corrected instrument;
the flawed runs are kept as `detector_564_20261017/*.v1_signext.out`.  **Then a second, format-only change:** two row
names are exactly 14 characters, and the gate greps `^<name>  .*ok$` (two spaces), so the name field went 14 -> 16
columns.  The tabled instrument was reconstructed from the shipped file by reverting only that edit, and its md5
reproduces `8d625289` exactly (`killtable_564_20261017/sgi_mte_decline_probe.tabled.py`).

## 3. The files this round changes (`git diff --numstat`, each marked)

