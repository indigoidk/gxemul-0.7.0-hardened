VERDICT: WITNESS BUILT AND RUN — the defect REPRODUCES at rung 3 on the committed build. 15/47, with all 15 controls green and all 32 kill rows red (`opus_witness_run_20260910.txt`). The brief's constants, registration length and attach address are all CORRECT as stated. **Two corrections to the brief's framing, both measured:** the killing population is not eight cells but **SIXTEEN** — every one of the eight offsets kills in BOTH directions, `st.b` as well as `ld.bu` — and the kill is **WIDTH-INDEPENDENT**, decided purely by the start offset, so `ld`/`ld.h`/`ld.bu` all die at the same address. I drove all sixteen. One further finding the brief did not describe: the eight killing offsets are exactly `mk48txxreg.h`'s "first bank of eight registers at offset (nvramsz - 16)", a coherent flags/alarm/interrupt/watchdog group, not an arbitrary set.

OPUS_MK48_WITNESS_20260910

Third line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`, verbatim:

HEAD: `032a588`

---

# `mk48nvramkill` — rung-3 witness, Opus 5 measuring seat, 2026-09-10

## 0. Tree identity and build clearance (checked, not assumed)

Working tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`. `git log --oneline -1` matched
CHECKPOINT.md's `032a588` at session start, and the dirty set matched CHECKPOINT.md's
declared uncommitted working set (`dev_lca.c`, `dev_sgi_re.c`, the three new probes). I am
in the fork, not one of the 2021 copies: `src/devices/dev_mk48txx.c` is **144 lines** with
the grep anchor `default:if (writeflag == MEM_READ)` at **:112**, and `memory_rw.c`'s
`paddr -= mem->devices[i].baseaddr;` sits at **:494** — the fork's ~794-line file, not the
530-line pristine copy. No line I cite is off by hundreds.

Two-part clearance on `build/gxemul`, run rather than asserted, for both files under test:

```
dev_mk48txx.c      : CMP CLEAN vs SEC      binary -nt source : YES
machine_mvme88k.c  : CMP CLEAN vs SEC      binary -nt source : YES
no .MUTANT sentinel
```

Both are shared files, not on the `est_divergence.txt` list, so `cmp` against SEC is the
correct comparison here.

**HEAD MOVED DURING MY RUN and I am labelling this honestly rather than quietly.** The main
loop committed `fb76c63` (records-only) while I was measuring, so my run log says
`MK48_LABEL=committed-HEAD-032a588` while HEAD is now `fb76c63`. I checked rather than
assumed: `git diff --stat 032a588..HEAD -- src/devices/dev_mk48txx.c src/machines/machine_mvme88k.c
src/include/thirdparty/mk48txxreg.h src/cpus/cpu_m88k_instr.c` is **empty**, and both files
still `cmp` clean against the build tree. **The measurement is valid at both commits**; only
the label's wording is narrower than the truth.

## 1. Premise audit — I checked every constant, and they are all right

The brief asked me not to ratify. I did not; I opened each one.

| brief's claim | source | verdict |
|---|---|---|
| `MK48TXX_LEN` = `MK48T08_CLKSZ` = 8192 | `dev_mk48txx.c:49`; `thirdparty/mk48txxreg.h:115` | **CORRECT** |
| registration is for that length | `dev_mk48txx.c:138-140`, `memory_device_register(..., MK48TXX_LEN, ...)` | **CORRECT** |
| `MK48T08_CLKOFF` = 0x1ff0 | `mk48txxreg.h:116` | **CORRECT** |
| `MK48TXX_ISEC` = 9 | `mk48txxreg.h:72` | **CORRECT** |
| `MK48TXX_ICSR` = 8, so the one case is 0x1ff8 | `mk48txxreg.h:71` | **CORRECT** |
| accept block passes everything outside `[0x1ff0, 0x1ff9)` via `goto ret` | `dev_mk48txx.c:87-94` | **CORRECT** |
| switch holds exactly one case | `dev_mk48txx.c:96-119` | **CORRECT** |
| eight offsets 0x1ff0..0x1ff7 hit `default:` → `exit(1)` | `dev_mk48txx.c:112-118` | **CORRECT** |
| attached unconditionally at `0xfffc0000` | `machine_mvme88k.c:114-117` | **CORRECT**, in the `MACHINE_MVME88K_187` arm |
| fatal addresses are `0xfffc1ff0..0xfffc1ff7` | — | **CORRECT, and confirmed empirically** — the disassembler prints `[0xfffc1ff0]` … `[0xfffc1ff7]` |

`grep -n "exit(\|fatal(" src/devices/dev_mk48txx.c` returns exactly three lines (113, 116,
118) — one `exit(1)`, reached by both message arms. There is no other kill in this device.
`grep -rn mk48txx src/machines/` returns exactly one attach site, so `mvme88k`/`mvme187` is
the only machine that can reach this device at all.

**One thing the brief states that is true but understated:** it says the switch "holds
exactly ONE case, `0x1ff8`". It does — and that case is safe in *both* directions, not just
on write. On a read it falls straight through `break` to the `ret:` label at `:121` and
returns `odata`, which `:84-85` already loaded. I measured it green in both directions
rather than reasoning about it (`ok rd 1ff8`, `ok wr 1ff8`).

## 2. What I built

`mk48_nvram_witness.py`, in the session scratchpad as instructed, with a durable copy at
`regress/artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py`. I did **not** place
it in `regress/` — the brief said you will place it if it lands.

**Rung 3, and nothing was modified to reach the site.** Real MC88100 instructions, executed
by the CPU, through real address decode and real `memory_rw`, on the unmodified in-tree
`-E mvme88k -e mvme187`. No machine description edited, no `device_add` added, no
`#include`/direct-call harness anywhere. `mvme187` already attaches this device, which is
what makes the witness legitimate rather than laundered.

I followed `regress/pcc2_width_witness.py`'s shape — it is the in-tree witness for the PCC2,
which `machine_mvme88k.c` attaches **twenty-two lines above** the mk48txx in the same block,
so the machine, the scratch addresses and the m88k encodings were already proven for exactly
this rig. I did not hand-roll new pty plumbing; in fact I did not need a pty at all (see §3).

Exact command line, one per row-group; this is the literal `argv`:

```
/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul -V -x -E mvme88k -e mvme187 -M 64 \
    0x10000:/tmp/mk48_dummy.bin
```

driven by:

```
MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/Users/.../scratchpad/run_witness.sh
  -> python3 -u .../mk48_nvram_witness.py \
         /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul committed-HEAD-032a588
```

Each session is the same three-instruction program with only the middle slot varying:

```
    st    r5,r3,0        ; 0x24a30000   seed scratch RAM with 0x5a5a5a5a
    <ACCESS UNDER TEST>  ;              ld.bu / st.b / ld / ld.h at r2+offset
    ld    r4,r3,0        ; 0x14830000   POST-ACCESS OBSERVABLE
    br    .              ; 0xc0000000
```

with `r2 = 0xfffc0000`, `r3 = 0x00020000`, `r5 = 0x5a5a5a5a`, and every result register
pre-set to `0xdeadbeef` so "absent", "sentinel" and "correct" are three distinguishable
states. Encodings are generated by `enc(op26, rd, rs1, imm)` rather than hand-assembled —
this project's hand-assembled-encoding trap — and the opcodes are read off
`cpu_m88k_instr.c:3051-3079`: `ld.bu` 0x03, `ld` 0x05, `ld.h` 0x06, `st` 0x09, `st.b` 0x0b.
The disassembly in every transcript confirms the encoding decoded to the instruction and
address I intended.

## 3. The oracle — which discriminator I used, and why not the other two

The brief is right that this oracle is unusual and easy to get wrong. **The discriminator I
scored on is the REAPED WAIT STATUS, paired with a POST-ACCESS OBSERVABLE.** Neither alone;
the row is a conjunction.

1. **Reaped wait status (primary).** `subprocess.run(...)` returns the child's status.
   `returncode == 1` is `exit(1)`; `returncode == 0` is the debugger's own `quit`. A hang is
   a **structurally distinct third state** — `subprocess.TimeoutExpired`, reported as
   `TIMEOUT` — so "timed out" can never be silently read as "killed". This answers the
   brief's first hazard directly: I never infer death from a timeout, because a timeout has
   its own token and would fail the row against `exit0` while looking nothing like `exit1`.

2. **Post-access observable (co-primary).** The killing access is sandwiched between a
   scratch store and a scratch load, and the session ends `print r4`. If the guest ran on,
   `r4 == 0x5a5a5a5a`. If the host died, the third `step` and the `print` never happen and
   the row reads `died`. **This is what separates DEATH from a `fatal()` that merely
   complains and returns** — the brief's second hazard, and a real one in this fork, where
   `fatal()` has no early-out and does not exit. A complaining-but-surviving build would
   show `exit0` *and* `0x5a5a5a5a`; only a real death shows `exit1` *and* `died`. Every one
   of the sixteen shows the latter.

3. **Attribution by message (corroboration only, never scored alone).** The `msg census` row
   requires all sixteen sessions to have printed a message naming **its own** offset —
   `[ mk48txx: unimplemented READ from offset 0x1ff3 ]` for `rd 1ff3`, and the `WRITE to`
   form with the stored byte for the write direction. 16/16. I state plainly that this row is
   *not* proof of death, exactly as the brief warns; it is proof that the death is *this*
   device's, at *this* offset.

4. **Attribution by sibling (the control the brief suggested).** Six otherwise-identical
   sessions at `0x1fef` (below the window), `0x1ff8` (the implemented case) and `0x1ff9`
   (first accepted clock register), in both directions, all run to completion with the
   observable present. So the death is not a property of the session shape, the machine, the
   program, or the device — it is a property of the offset. The `shape` row makes the same
   point from the other side: the identical program with a plain RAM load in the access slot
   exits 0.

I did not need a pty. The debugger drives correctly off a pipe on this machine (verified in
the transcripts — prompt, echo and replies all present), and a pipe gives me the wait status
directly with no timing games. Every emulator invocation is reaped; nothing is left running.

### Controls, clause (ii) of the ladder

- **`live`** — a byte written to NVRAM offset `0x100` and read back through the same decode
  returns `0x5a`. Device mapped, responding, reached at the address I think.
- **`nvram0`** — a never-written neighbour at `0x101` reads `0x00`. So the backing array is
  zero-filled, which means a *non-zero* clock byte cannot be zero-fill, a stuck bus, or a
  fallback.
- **`devsig yr / mon / mday / wday`** — the device-signature control, and I made it four-way
  on purpose because of the footbridge probe that returned `0x0` everywhere with its RAM
  control green. Four clock registers are compared against the *host's own* `gmtime`, **in
  two different encodings**: `0x1fff/0x1ffe/0x1ffd` are BCD (`0x26`, `0x9`, `0x10` =
  2026-09-10) while `0x1ffc` is `tm_wday + 1` **raw, not BCD** (`0x5` = Thursday). A
  four-way match across two encodings could only have come from
  `mk48txx_update_regs()` at `dev_mk48txx.c:58-73`. RAM answers 0; a fallback answers 0;
  a stuck bus answers a constant.
- **`neg apparatus`** — the control on the controls, and I added it because this project has
  been bitten by checks that cannot fail. It runs the `live` program under the bogus subtype
  `-e 187` (the exact mistake `pcc2_width_witness.py` records making) and **asserts
  `exit1/absent`**: no machine is built, so the liveness oracle *must* go red. It does. The
  green `live` above is therefore evidence rather than decoration.

## 4. Results — `MK48_RESULT=15/47`, committed build, no fix present

Full log preserved at `regress/artifacts/mk48nvramkill/opus_witness_run_20260910.txt`,
completion sentinel `MK48_WITNESS_DONE` verified by `tail -1` (not by size).

Every `want` is the **FIXED** behaviour, so this is test-first in the per-probe sense: the
committed build is red and the same script goes green after a fix.

```
row              got                    want                   result
live             0x5a                   0x5a                   ok
nvram0           0x0                    0x0                    ok
neg apparatus    exit1/absent           exit1/absent           ok
devsig yr        0x26                   0x26                   ok
devsig mon       0x9                    0x9                    ok
devsig mday      0x10                   0x10                   ok
devsig wday      0x5                    0x5                    ok
shape            exit0/0x5a5a5a5a       exit0/0x5a5a5a5a       ok
ok rd 1fef       exit0/0x5a5a5a5a       exit0/0x5a5a5a5a       ok
ok wr 1fef       exit0/0x5a5a5a5a       exit0/0x5a5a5a5a       ok
ok rd 1ff8       exit0/0x5a5a5a5a       exit0/0x5a5a5a5a       ok
ok wr 1ff8       exit0/0x5a5a5a5a       exit0/0x5a5a5a5a       ok
ok rd 1ff9       exit0/0x5a5a5a5a       exit0/0x5a5a5a5a       ok
ok wr 1ff9       exit0/0x5a5a5a5a       exit0/0x5a5a5a5a       ok
rd 1ff0          exit1                  exit0                  FAIL
rd 1ff0 obs      died                   0x5a5a5a5a             FAIL
rd 1ff1          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
rd 1ff2          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
rd 1ff3          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
rd 1ff4          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
rd 1ff5          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
rd 1ff6          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
rd 1ff7          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
wr 1ff0          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
wr 1ff1          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
wr 1ff2          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
wr 1ff3          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
wr 1ff4          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
wr 1ff5          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
wr 1ff6          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
wr 1ff7          exit1 / died           exit0 / 0x5a5a5a5a     FAIL FAIL
msg census       16                     16                     ok
MK48_RESULT=15/47
```

(The kill block is rendered two-rows-per-line above for width; the preserved log has each
`<tag>` and `<tag> obs` on its own line, and the `rd 1ff0` pair is shown unfolded so the
shape is visible.)

A representative raw transcript, unfiltered, from the `rd 1ff0` session:

```
GXemul> step 3
s00010000: 24a30000        st	r5,r3,0x0	; [0x00020000] = 0x5a5a5a5a
s00010004: 0c821ff0        ld.bu	r4,r2,0x1ff0	; [0xfffc1ff0]
[ mk48txx: unimplemented READ from offset 0x1ff0 ]
                                       <- transcript ENDS. no third step, no `print r4'.
RC=1
```

and the write direction, `wr 1ff3`:

```
s00010004: 2ca21ff3        st.b	r5,r2,0x1ff3	; [0xfffc1ff3] = 0x5a
[ mk48txx: unimplemented WRITE to offset 0x1ff3: 0x5a ]
RC=1
```

against the sibling control `ok rd 1ff9`, which is the same program one byte higher:

```
s00010004: 0c821ff9        ld.bu	r4,r2,0x1ff9	; [0xfffc1ff9]
s00010008: 14830000        ld	r4,r3,0x0	; [0x00020000]
GXemul> print r4
0x5a5a5a5a
GXemul> quit
RC=0        mk48txx messages: 0
```

### A number I did not trust until I had measured it three ways

`MK48_ELAPSED=0.4s` for twenty-six emulator sessions looked impossible, and this project's
own rule is that a contradiction is the cheapest signal there is. I checked instead of
explaining it away: an independent external clock around the whole run gave
`1789063733.642648624 - 1789063733.137441189` = **0.505 s** including Python startup, and a
separate `time` of the emulator alone gave **0.025 s for one session** and **0.358 s for
twenty-six in a loop**. It is real — there is no PROM boot here, just machine construction
and a few single-steps. The number stands, now derived rather than transcribed.

## 5. A defect I found in MY OWN probe, reported because the first run blamed the emulator

The first run scored **13/46** with `devsig mon` red: got `0x9`, want `0x10`. **The want was
wrong and the device was right.** `dev_mk48txx.c:71` is `BCD(tmp->tm_mon + 1)` using C's
`struct tm`, where `tm_mon` is **0-based**; Python's `time.struct_time.tm_mon` is
**1-based**, so `bcd(g.tm_mon + 1)` computed October. Fixed to `bcd(g.tm_mon)`, and the
probe now carries a comment block naming all four C-vs-Python disagreements, because
`tm_wday` differs too (C 0=Sunday, Python 0=Monday — I had happened to handle that one) and
`tm_year` agrees mod 100 only for 2000–2099.

I am recording this rather than quietly fixing it because a control that fails for the
probe's reason is exactly the "did it fail for the reason under test?" hazard, and had it
been a *kill* row instead of a control I would have shipped a false positive. It cost one
re-run; the re-run is the log cited above.

## 6. Q3 — how many of the eight did I drive, and why

**All eight, in both directions — sixteen killing accesses — and the honest census is
sixteen, not eight.** Three reasons, and the first is the one that matters:

1. **The census was free, unlike the PCC2's.** `pcc2_width_witness.py` could only reach five
   of its twelve arms because a non-byte m88k access is alignment-checked before
   `memory_rw`, and `relative_addr %= PCC2_SIZE` keeps an odd offset odd. **None of that
   applies here.** The killing accesses are *byte* accesses: `cpu_m88k_instr.c:3070` decodes
   `ld.bu` at `opsize 0` and `:3078` `st.b` at `opsize 0`, and
   `cpu_m88k_instr_loadstore.c:167` guards the alignment check with `#ifndef LS_1`, so a
   size-1 access is **never alignment-checked**. Every offset is reachable, so driving one
   and extrapolating would have been a choice to know less for no saving. Sixteen sessions
   cost 0.4 seconds.
2. **The direction axis is not optional.** The `default:` arm at `:112-118` handles read
   *and* write and falls into the same `exit(1)`. A round that drove reads only would leave
   the write half of its own defect unwitnessed, and the eventual detector would owe rows it
   had never measured.
3. **The census is what a fix's floor will be built on.** Under clause (d) the repair's
   predicate will be `relative_addr` against this window, and the cells are {8 offsets} ×
   {read, write}. Handing the fix designer a measured sixteen rather than an argued eight is
   the difference between a contract and a guess.

One is indeed enough to *license* the fix; sixteen is what makes the fix's coverage claim
checkable. I would not have spent an hour on it, but it cost seconds.

## 7. Q4 — three things I noticed that the brief did not describe

### (a) The kill is WIDTH-INDEPENDENT — measured, not reasoned

The brief describes the defect in terms of offsets, which is right, but it is worth pinning
that the width axis is *inert* here, unlike `dev_pcc2.c` where width was the whole defect.
`relative_addr` is the start address, and `len` never enters the guard. Measured:

```
ld    r4,r2,0x1ff0   (WORD, 4-aligned, legal)   -> RC=1, "unimplemented READ from offset 0x1ff0"
ld.h  r4,r2,0x1ff2   (HALF, 2-aligned, legal)   -> RC=1, "unimplemented READ from offset 0x1ff2"
ld.bu r4,r2,0x1ff0   (BYTE)                     -> RC=1
```

So each of the sixteen cells is reachable by several instruction encodings, all collapsing
onto the same cell. **This is good news for a fix and bad news for a detector that pins
width**: there is no width axis to close, and a row varying width at a fixed offset would be
non-varying by construction — the CHANNEL-line vacuity this project already names.

### (b) The eight offsets are exactly one documented register bank — which changes the severity story

`mk48txxreg.h:59-62` says, in the tree's own words:

> *"The first bank of eight registers at offset (nvramsz - 16) is available only on more
> recent (which??) MK48Txx models."*

`nvramsz - 16` = `8192 - 16` = **0x1ff0**. So the eight killing offsets are not an arbitrary
tail — they are precisely that first bank: `IFLAGS`(0x1ff0), unused(0x1ff1),
`IASEC`/`IAMIN`/`IAHOUR`/`IADAY`(0x1ff2-5), `IINTR`(0x1ff6), `IWDOG`(0x1ff7). Flags, the
alarm quartet, interrupts, watchdog. The file's own header says the model is MK48T08 only
(`dev_mk48txx.c:30-31`, *"Only the MK48T08 is implemented so far"*), and `mk48txxreg.h:50-52`
attributes the battery-low/wakeup-alarm features to the MK48T59.

Two consequences for whoever designs the fix:

- **It explains why they are unimplemented** — they are the variant-specific bank — which is
  a much better warrant than "nobody got round to it", and it is the kind of warrant that
  survives review.
- **It sharpens reachability.** A generic `mk48txx` driver that probes for the alarm bank, or
  a driver written against the T59, walks straight into all eight. That is a plausible guest,
  not an exotic one. I have *not* established that OpenBSD/mvme88k's clock driver touches
  them — that is a boot-witness question I could not settle here, and I am not going to claim
  it. What I have established is that the bank is architecturally ordinary.

I would rank this as raising the severity above "a guest would have to go looking".

### (c) A second, non-fatal modelling defect in the same handler: one byte regardless of `len`

`:84-85` is `odata = d->reg[relative_addr];` and the accept path's write is
`d->reg[relative_addr] = idata;`. **Both touch exactly one byte whatever `len` says.** So a
wide access to the *accepted* clock block returns a single byte zero-extended rather than the
packed bytes. Measured rather than asserted, on the big-endian 88100:

```
ld.bu of 0x1ffc,0x1ffd,0x1ffe,0x1fff  ->  0x5, 0x10, 0x9, 0x26   (wday, mday, mon, year)
ld    (4 bytes) of 0x1ffc             ->  0x00000005
                    a true 4-byte big-endian device read would be 0x05100926
```

This is a wrong-value defect, not a kill, and it is **out of scope for this round** — I raise
it only because it lives three lines above the defect under test and a fix touching this
handler will be looking straight at it. It is also a reason not to "fix" the kill by widening
the accept block without thinking: routing 0x1ff0..0x1ff7 to the RAM path would give them
this same one-byte-per-access behaviour, which is probably fine for NVRAM-ish registers but
should be a decision rather than an accident.

There is no out-of-bounds hazard in `d->reg[relative_addr]`: the array is `MK48TXX_LEN`
= 8192 and the device is registered for exactly that length, and because only one byte is
ever touched, a wide access at 0x1fff cannot walk off the end.

## 8. Safety — the repo is untouched by me

I built nothing (`build/gxemul` was current and cleared the two-part check), so no tree was
copied or mutated and no `.MUTANT` sentinel was ever needed. I wrote **no** file into
`GXEMUL-SEC/src/`, `regress/*.py`, or any existing repo file.

`git status --porcelain` at the end shows `OUTSTANDING_BUGS.md`, `tools/pipeline/ledger.json`,
`tools/pipeline/matrix.html`, `regress/artifacts/mk48nvramkill/brief_*.md` and
`codex_design_20260910.*` as changed/added — **none of these are mine.** They are the main
loop's own concurrent work (it also advanced HEAD to `fb76c63` mid-run). The pre-existing
dirty set (`dev_lca.c`, `dev_sgi_re.c`, `sgi_de_primop_probe.py`, the three held probes) is
byte-unchanged from session start.

My writes, in full:

- session scratchpad — `mk48_nvram_witness.py`, `run_witness.sh`, `smoke{,2,3,4}.sh`,
  `extra{,2,3}.sh`, `timecheck.sh`, `witness_run{1,2}.txt`
- the new artifacts directory only, as the brief permitted — this file,
  `opus_witness_run_20260910.txt` (the cited log, at a durable path so the score claim stays
  checkable), and `opus_mk48_nvram_witness_20260910.py`

## 9. What this licenses, stated narrowly

A rung-3 witness exists, so `mk48nvramkill` is **eligible** — rung is a floor on
admissibility, not a priority, and severity ranking is not mine to settle here. The ladder's
clause (i) is satisfied (symptom shown on the committed pre-fix build, same script goes
green after a fix), clause (ii) is satisfied by the liveness, zero-fill, four-way
device-signature and negative-apparatus controls, and clause (iii) is satisfied because
nothing in the machine description or dispatch was touched.

The witness field for the ledger would be:

```
probe:regress/artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py
      (rung 3; -E mvme88k -e mvme187 unmodified; 15/47 on build/gxemul,
       32 kill rows red, 16/16 offset-named deaths; log opus_witness_run_20260910.txt)
```

`detector:` is **not** the right term here and `none` would be false — this is a genuine
rung-3 access witness, which is exactly the case the 2026-08-27 lifecycle ruling asked
someone to try for before recording a round as documented-only. It took one invocation.
