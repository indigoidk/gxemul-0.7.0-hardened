# `lcaisalane` — RUNG-3 WITNESS, measured 2026-09-10 (Opus 5 measuring seat)

**VERDICT: RUNG-3 WITNESS BUILT AND REPRODUCED. `LCAISALANE_RESULT=13/16`, three RED rows, all
three the defect. Four runs, byte-identical. The round may proceed to a fix.**

| | |
|---|---|
| probe | `GXEMUL-SEC/regress/lca_isalane_probe.py` (new) |
| frozen as-run copy | `regress/artifacts/lcaisalane/witness_20260910/lca_isalane_probe.asrun.py` — `cmp`-identical to the shipped file |
| driver | `.../witness_20260910/run_witness.sh` |
| logs | `.../witness_20260910/HEAD_run1.out`, `HEAD_run2.out` (sentinel `LCAISALANE_DONE` last line), plus `HEAD_run*_prelim.out` and `RUNMETA_*.txt` |
| raw pty transcripts | `.../witness_20260910/raw1/`, `raw2/` (+ `raw*_prelim/`) — every guest instruction disassembled by the emulator itself |
| binary | `C:\DocumentNoSnc\CC\GXEMUL\build\gxemul`, **read-only, not rebuilt** |
| tree under test | `GXEMUL-SEC/` at HEAD `1ce8296` + the uncommitted `#518` diff in `lca_ioc` (a different handler) |
| machine | `-E alpha -e alphabook1 -M 64`, unmodified: no `device_add`, no disk image, no machine edit |

## Two-part clearance — RUN, not asserted (recorded in `RUNMETA_1.txt` / `RUNMETA_2.txt`)

```
PART1 cmp build/src/devices/dev_lca.c vs GXEMUL-SEC : CLEAN
PART2 [ build/gxemul -nt build/src/devices/dev_lca.c ] : YES
     build/gxemul                     2026-09-10 00:19:30.591925800 -0500
     build/src/devices/dev_lca.c      2026-09-10 00:19:24.074102600 -0500
build/.MUTANT : absent
```

`dev_lca.c` is a SHARED file (it is not in `tools/est_divergence.txt`), so the `cmp` half of the
clearance is applicable and was run. The measured binary is therefore built from exactly the source
this report quotes, `#518` included. **Nothing was built, nothing in `build/` was written, no
sentinel was owed or dropped.**

## The decoded lane mapping — VERIFIED, and the codex design reading is right

The brief offered *bits 0–1 or bits 5–6*. **It is bits 5–6 of `relative_addr`, i.e. bits 1–0 of the
derived ISA port**, because the shift precedes the mask:

```c
	relative_addr >>= 5;          /*  relative_addr is now the ISA PORT NUMBER  */

	ofs = relative_addr & 3;      /*  so ofs = port & 3  */
	if (ofs > len) { fatal("[ ofs=%i len=%i in lca_isa access function. aborting ]\n", ofs, len); exit(1); }
	...
	cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr, &byte, 1, MEM_READ, CACHE_NONE);
	for (i=0; i<len; i++)
		data[i] = i == ofs? byte : 0x00;
```

The literal source line *is* `ofs = relative_addr & 3`, which is why the brief's phrasing is
defensible — but by then `relative_addr` has already been shifted, and the forwarded access goes to
`LCA_ISA_BASE + relative_addr`, i.e. **to that same port, including the two bits the lane came
from.**

> ### THE STRUCTURAL CONSEQUENCE, and it is the one thing the brief's row list could not be built as written
>
> **The lane is not an independent field. It is a FUNCTION of the port.** So there is no way to
> address ONE device register through two different lanes: brief row 2 — *"the SAME device port
> addressed so that `ofs == 1`"* — **cannot exist**, and the codex seat had already said so from the
> other end (*"The named 8042 ports and UART base all have `ofs == 0`, so those offsets themselves
> cannot demonstrate the equality defect"*).
>
> The defect is therefore not "one register has a broken lane". It **partitions the entire 64 K ISA
> port space by `port & 3`**, and which class a register falls into is decided by its own address:

| `port & 3` | `ofs` | `len == 1` (LDBU/STB) | `len == 2` | `len == 4` / `8` |
|---|---|---|---|---|
| 0 | 0 | correct | correct | accepted, lane 0 |
| 1 | 1 | **ACCEPTED, answers ZERO** (`1 > 1` is false; the packing loop's `i == ofs` never fires) | correct | accepted, lane 1 |
| 2 | 2 | **`exit(1)`** | **ACCEPTED, answers ZERO** | accepted, lane 2 |
| 3 | 3 | **`exit(1)`** | **`exit(1)`** | accepted, lane 3 |

`ofs > len` (rather than `>=`) is exactly what admits the zero-answering cells: `ofs == len` passes
the guard and then indexes a lane that does not exist in the caller's buffer.

**What that costs at a real device.** The console UART occupies ISA `0x3f8..0x3ff`, so its eight
registers land in all four classes at once:

```
    0x3f8 data     ofs 0   ok        0x3fc mcr       ofs 0   ok
    0x3f9 ier      ofs 1   ZERO      0x3fd lsr       ofs 1   ZERO
    0x3fa iir      ofs 2   DEATH     0x3fe msr       ofs 2   DEATH
    0x3fb lctl     ofs 3   DEATH     0x3ff scratch   ofs 3   DEATH
```

A byte read of the **Line Status Register** — the register a polling console driver reads before
every character — returns zero, and a byte read of the **Modem Status** or **Line Control** register
ends the emulator. No unusual value, no driver setup, four guest instructions.

## The rows, as measured (`HEAD_run1.out`; run 2 differs only in its label line)

```
row            got                      want                     note
  RAW[base]: live=0x55 flatLSR=0x60 sparseLSR=0x0 wideLSR=0x6000 nodev=0x0 alive=True retried=False
base alive     alive                    alive                    CONTROL: nothing in this session may end the host        ok
live           0x55                     0x55                     LIVENESS+DEVSIG: 8042 self-test reply, THROUGH lca_isa at ofs 0 ok
ofs1 devsig    0x60                     0x60                     DEVSIG: TXRDY|TSRE are set by the ns16550 handler on every access ok
ofs1 zero      0x0                      0x60                     *** DEFECT: byte read of ISA 0x3fd (LSR) -- port 1 mod 4 -> ofs 1 *** FAIL
ofs1 answer    completed                completed                the handler returned 1: the guest was ANSWERED zero, not refused ok
ofs1 wide      0x60                     0x60                     SAME ADDRESS at len 4: the device byte lands in lane 1 -- so it arrived ok
ctl            alive                    alive                    CONTROL: byte access to an ISA port with NO device, ofs 0, survives ok
ctl zero       0x0                      0x0                      CONTROL: and it answers zero -- so zero alone proves nothing ok
  EVIDENCE[base]: [ pckbc: write to CTL: aa ]
  EVIDENCE[base]: [ lca: ISA interrupt assert not implemented (Alpha has no interrupt delivery); ignored  (once) ]
  EVIDENCE[base]: [ lca: ISA interrupt deassert not implemented (Alpha has no interrupt delivery); ignored  (once) ]
  EVIDENCE[base]: memory READ: from non-existant paddr=0x00000001d0000300 len=1 pc=0xfffffc000104005c

  RAW[ofs2]: flatMSR=0xb0 wideMSR=0xb00000 alive=False retried=False
ofs2 devsig    0xb0                     0xb0                     DEVSIG: DCD|DSR|CTS set by the ns16550 handler on every access ok
ofs2 wide      0xb0                     0xb0                     CONTROL: the SAME sparse address at len 4 survives and packs lane 2 ok
ofs2 exit      dead                     alive                    *** DEFECT: byte read of ISA 0x3fe (MSR) -- port 2 mod 4 -> ofs 2 *** FAIL
ofs2 attrib    yes                      yes                      ATTRIBUTION: a death here must carry the arm's own diagnostic ok
  EVIDENCE[ofs2]: [ ofs=2 len=1 in lca_isa access function. aborting ]

  RAW[ofs3]: flatSCR=0x5a wideSCR=0x5a000000 alive=False retried=False
ofs3 devsig    0x5a                     0x5a                     DEVSIG: the ns16550 scratchpad returns the byte just written to it ok
ofs3 wide      0x5a                     0x5a                     CONTROL: the SAME sparse address at len 4 survives and packs lane 3 ok
ofs3 exit      dead                     alive                    *** DEFECT: byte read of ISA 0x3ff (scratch) -- port 3 mod 4 -> ofs 3 *** FAIL
ofs3 attrib    yes                      yes                      ATTRIBUTION: a death here must carry the arm's own diagnostic ok
  EVIDENCE[ofs3]: [ ofs=3 len=1 in lca_isa access function. aborting ]

LCAISALANE_RETRIED=none
LCAISALANE_RESULT=13/16
LCAISALANE_WITNESS=FAIL
LCAISALANE_DONE
```

### THE THREE RED ROWS, with the exact text

| row | got | want | the text on the wire |
|---|---|---|---|
| **`ofs1 zero`** | `0x0` | `0x60` | *(no diagnostic — that is the finding)* the handler **returned 1** and the guest's destination register was overwritten with zero |
| **`ofs2 exit`** | `dead` | `alive` | `[ ofs=2 len=1 in lca_isa access function. aborting ]` |
| **`ofs3 exit`** | `dead` | `alive` | `[ ofs=3 len=1 in lca_isa access function. aborting ]` |

Both deaths carried the arm's own diagnostic, so both `attrib` rows are green: this is a
reproduction of the defect under test, **not a death for some other reason**. The literal
`in lca_isa access function` occurs exactly once in `src/` (`dev_lca.c`; the second `grep -l` hit is
the compiled `.o`).

### The disassembly, straight out of the emulator (`raw1/raw_ofs2.txt`)

The killing access and the surviving control are the **same address in the same process**, four
instructions apart, differing only in width:

```
GXemul> step 4
fffffc0001040014:  a4410008    ldq	t1,8(t0)
fffffc0001040018:  249f0bad    ldah	t3,0xbad
fffffc000104001c:  20841dea    lda	t3,0x1dea(t3)
fffffc0001040020:  a0820000    ldl	t3,0(t1)          <-- len 4 at sparse(0x3fe): SURVIVES
[ ns16550 (tty0): read from msr: 0xb0 ]
GXemul> print t3
0xb00000                                                 <-- the MSR byte, packed into lane 2
GXemul> step 4
fffffc0001040024:  a4410008    ldq	t1,8(t0)
fffffc0001040028:  24bf0bad    ldah	t4,0xbad
fffffc000104002c:  20a51dea    lda	t4,0x1dea(t4)
fffffc0001040030:  28a20000    ldbu	t4,0(t1)          <-- len 1 at THE SAME ADDRESS: HOST DEATH
[ ofs=2 len=1 in lca_isa access function. aborting ]
```

and `raw1/raw_base.txt` for the zero-answer cell:

```
fffffc000104003c:  28c20000    ldbu	t5,0(t1)          <-- len 1 at sparse(0x3fd)
GXemul> print t5
0x0                                                      <-- the LSR is 0x60.  The guest got 0.
fffffc000104004c:  a0e20000    ldl	t6,0(t1)          <-- len 4 at THE SAME ADDRESS
GXemul> print t6
0x6000                                                   <-- TXRDY|TSRE, in lane 1
```

## Why the zero row is evidence and not an artefact

The design seat's sharpest objection was: ***"Zero readback alone cannot distinguish the defect from
a zero-filled fallback."*** It is correct — unmapped space, a missed device and a failed access all
read zero (`memory_rw.c`'s `#95` pre-zero). Three separate rows answer it, and none of them is the
zero row:

* **`ofs1 devsig` = `0x60`** — the SAME register read through the flat ISA mapping returns
  `LSR_TXRDY|LSR_TSRE`, which `DEVICE_ACCESS(ns16550)` sets at the top of every access. Only the
  device produces that.
* **`ofs1 wide` = `0x60` (raw `0x6000`)** — the SAME sparse address at `len 4` returns the byte in
  lane 1. So the byte reaches the packing loop, and **the loop is what drops it.**
* **`ofs1 answer` = `completed`** — every load in this probe pre-seeds its destination register with
  `0x0bad1dea` first. A load whose `memory_rw` fails returns *before* writeback
  (`cpu_alpha_instr_loadstore.c`), leaving the sentinel. The sentinel is **gone**, so the handler
  returned 1 and the guest was **answered** zero. **A false success, not a decline** — which is the
  discriminator the design seat asked the fix round for, taken pre-fix.
* **`ctl zero` = `0x0`** — an ISA port with no device behind it answers zero through the same
  handler, stated explicitly so the zero row can never be read as self-supporting.

## Witness-ladder clauses

* **(i) symptom on the pre-fix committed build, green post-fix with the same script** — `13/16`
  measured, the three defect rows RED. Every row asserts the CORRECT behaviour, so a fix must take
  the same script to `16/16` with no oracle edit. *(`ofs1 zero`'s want is the flat readback taken in
  the same process, so a fix that hands back the device byte greens it; a fix that DECLINES the
  access also reds it, correctly — a decline must not be reported as a successful read of zero.)*
* **(ii) LIVENESS + DEVICE-SIGNATURE controls, and more than one of each** — `live` (0x55 from the
  8042, *through the handler under test*), `ofs1 devsig` (0x60 = TXRDY|TSRE), `ofs2 devsig`
  (0xb0 = DCD|DSR|CTS), `ofs3 devsig` (0x5a scratch echo), plus the two `wide` rows and `ctl`.
* **(iii) machine description and dispatch committed and unmodified** — `-e alphabook1` with a
  1-byte dummy load file. No `device_add`, no disk image, no source edit. `lca_isa` and every ISA
  device it forwards to are installed by `DEVINIT(lca)` and `bus_isa_init` as shipped.

**Ledger witness field: `probe:regress/lca_isalane_probe.py`.**

## Contract — what this witnesses and what it does NOT

It is a **WITNESS, not a detector.** `alive` greens equally for a decline, a fault, a latched
announce and a full implementation; `ofs1 zero` greens for anything that hands the byte back. A fix
round owes rows that discriminate those. Disclosed gaps, each derived from the source and **not
measured here**:

1. **THE WRITE DIRECTION IS UNROWED.** The guard dominates both directions — it runs before
   `if (writeflag == MEM_WRITE)` — so a byte **store** to ISA `0x3fe`/`0x3ff` ends the host by the
   same line. Source-derived; no row. It is one extra session for the fix round and worth taking,
   because `lctl`/`ier` are write-mostly registers.
2. **THE UNINITIALISED-`byte` PATH IS REACHABLE WITH ONE COMMAND-LINE FLAG, and this run did not
   take it.** The read arm ignores the forwarded `memory_rw`'s return value.
   `memory_warn_about_unimplemented_addr` returns `true` (→ `MEMORY_ACCESS_FAILED`) only when
   `machine->halt_on_nonexistant_memaccess` is set, which `main.c` does for **`-T`** and nothing
   else. This probe does not pass `-T`, so `ctl` exercised the benign branch and its
   `memory READ: from non-existant paddr=0x00000001d0000300 len=1` line is the warning, not a
   failure. **Under `-T` the same access packs an uninitialised local into the guest's buffer.**
   Flagged, unmeasured, and named as a fix-round row.
3. **`len 4`/`len 8` are clean WITH RESPECT TO THIS DEFECT ONLY.** They are not correct: the handler
   forwards exactly one byte whatever `len` is, so a longword read of ISA `0x3f8` returns one byte
   and three zeroes. That is a larger sparse-space modelling question (the 21066 encodes the
   transfer size in address bits `<4:3>`, which this model discards) and is **not** this row.
4. **Interrupt delivery is not observed and cannot be** — the `live` row's evidence lines are
   `#516`'s two announces firing once each. Note that this witness **could not have used the 8042
   route before `#516`**: the assert and deassert stubs were `fatal()`+`exit(1)`, so the control row
   would have killed the host before the subject did.

## Two things that were unexpected

* **The `%i`-against-`size_t` mismatch the design seat flagged printed correctly here.** The arm is
  `fatal("[ ofs=%i len=%i ...", ofs, len)` with `unsigned int ofs` and `size_t len`, and the
  transcripts read `ofs=2 len=1` / `ofs=3 len=1`. It is still undefined behaviour and still worth
  fixing; it simply is not observable on this x86-64 build, so the attribution row is keyed on the
  literal `in lca_isa access function` and not on the numbers.
* **The driver, not the instrument, had a log-shape defect on its first pair of runs.** Driver v1
  appended `EXIT=` and a timestamp *after* the probe output, so `LCAISALANE_DONE` was not the last
  line — a truncated run and a finished one would have rendered identically, which is exactly the
  completion-sentinel failure the carrier warns about. The clearance and exit status now go to
  `RUNMETA_$1.txt`. Both v1 runs are **preserved** as `HEAD_run*_prelim.out` (nothing was
  overwritten) and their row sections `diff` clean against the v2 pair.

## Reproducibility

Four runs on a machine concurrently loaded by a kill table: **all four identical**, `13/16`,
`LCAISALANE_RETRIED=none` — the built-in one-shot retry (settle ×3) never had to fire. Each run
takes ~57 s.

```
diff HEAD_run1.out HEAD_run2.out          -> only the `label=` line
diff <prelim row section> <v2 row section> -> identical
cmp  witness_20260910/lca_isalane_probe.asrun.py  regress/lca_isalane_probe.py  -> identical
```

## What I could not do

* **Nothing was blocked.** No build was attempted, no existing file was edited, and no path outside
  `regress/lca_isalane_probe.py` and `regress/artifacts/lcaisalane/` was written.
* Brief row 2 could not be built **as specified** — see the structural consequence above. It was
  reformulated onto the port-class partition, which is what the code actually does, and the report
  says so rather than quietly narrowing the claim.
* `src/devices/dev_sgi_re.c` appeared as modified in `git status` during this session. **It is not
  mine** — I touched no file under `src/`. Recorded so nobody attributes it here.
