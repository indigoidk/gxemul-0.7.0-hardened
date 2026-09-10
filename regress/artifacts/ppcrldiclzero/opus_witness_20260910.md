VERDICT: CONFIRMED AND WITNESSED AT RUNG 3 -- `X(rldicl)` writes ZERO on all 190 (SH,MB) cells driven, on three unmodified in-tree 64-bit PPC machines including `macppc -e g5`; the one-character repair `tmp |=` -> `tmp2 |=` turns the identical script from 19/27 to 24/27 with the census going 190-wrong -> 0-wrong. THE BRIEF UNDERSTATES IT IN THREE WAYS: (a) TWO tokens are wrong, not one, and the "obvious" repair of deleting `& tmp2` was BUILT and MEASURED still wrong; (b) there is a SECOND observable channel -- `rldicl.` reports CR0=EQ always, so it corrupts control flow, not only data; (c) the sibling audit found TWO more live defects in the same family, `X(rldimi)` and `X(rlwimi)`, both measured, which makes this a CLASS rather than a typo.

OPUS_RLDICL_WITNESS_20260910

Third line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`, verbatim as read at the start of this run:

    HEAD: `ce61689`

*Honesty note, and it is a real observation rather than a hedge: that file CHANGED UNDER ME during the run. Re-read at the end it says ``HEAD: `7b7f76b` ``, which matches `git log --oneline -1`. So the checkpoint was stale when I opened it and was refreshed by concurrent activity while I worked; it is in sync now and I am NOT reporting staleness as a finding. I quote what I actually read, per the token's purpose.*

---

## 0. Tree confirmation

Read `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\cpus\cpu_ppc_instr.c`. `X(rldicl)` is at **line 2431**, `tmp2 = 0;` at **2444**, the assignment at **2449**. The brief's anchor and my line numbers agree to the line, so I am in the tree under review and not in one of the 2021-vintage copies. (Cross-check: the fork's file is 146,943 bytes / 5,3xx lines; a 2021 copy would put this function hundreds of lines away.)

## 1. THE BRIEF'S READING IS CORRECT -- AND INCOMPLETE

Verbatim, `cpu_ppc_instr.c:2438-2449`:

```c
	uint64_t tmp = cpu->cd.ppc.gpr[rs], tmp2;
	/*  TODO: Fix this, its performance is awful:  */
	while (sh-- != 0) {
		int b = (tmp >> 63) & 1;
		tmp = (tmp << 1) | b;
	}
	tmp2 = 0;
	while (mb <= 63) {
		tmp |= ((uint64_t)1 << (63-mb));
		mb ++;
	}
	cpu->cd.ppc.gpr[ra] = tmp & tmp2;
```

I checked for the escape routes the brief asked me to look for. **There are none.** `tmp2` is declared uninitialised at 2438, assigned `0` at 2444, and never appears again except in the AND at 2449. `gpr[ra]` is assigned exactly once in the function. `mb` is `((iw >> 6) & 31) | (iw & 0x20)`, so `0 <= mb <= 63` always and the loop body always executes at least once. The row does not collapse.

> **BUT THE DEFECT IS TWO TOKENS, NOT ONE, AND THE SECOND HIDES THE FIRST.**
> The mask is ORed into **`tmp`** -- the *rotated value* -- rather than into `tmp2`. So even setting the AND aside, the rotated data is destroyed by having every mask bit forced to 1. `tmp2` never being written is a *consequence* of the same slip, not an independent bug.

This matters because it changes what a correct repair looks like, and I did not want to assert that, so I **built both candidates**:

| candidate | edit | measured result |
|---|---|---|
| **`tmp \|=` -> `tmp2 \|=`** | one character | **CORRECT** -- 24/27, census 0 wrong / 0 zero |
| delete `& tmp2` | the "obvious" repair | **STILL WRONG** -- ships `ROTL64(rS,SH) \| MASK(MB,63)`, an OR where the architecture says AND |

The naive repair returns `0xdeadbeefffffffff` for `clrldi r4,r3,32` where the answer is `0xcafef00d`, and gets 126 of the 190 census cells wrong. It is *worse than the present bug in one specific way*: it removes the always-zero signature that makes the defect easy to spot, while leaving the value wrong. Recorded because a future round reading `tmp & tmp2` will be tempted by exactly that edit.

## 2. THE ORACLE, derived from the manual and not from this tree

`_scratchpad/ppc_pem_32and64_2005.txt:29736` (rldiclx RTL):

```
n <- sh[5] || sh[0-4]    r <- ROTL[64](rS, n)    b <- mb[5] || mb[0-4]
m <- MASK(b, 63)         rA <- r & m
```

and the prose at `:29737` -- *"A mask is generated having 1 bits from bit MB through bit 63 and 0 bits elsewhere. The rotated data is ANDed with the generated mask and the result is placed into rA."*

IBM bit numbering is big-endian, so `MASK(b,63)` is the **low `64-b` bits**. For `b=32` that is `0x00000000ffffffff`, which is why `rldicl rA,rS,0,32` is the canonical 32-bit zero-extend (`clrldi`, manual `:29758`). Every `want` in the probe is computed from those five lines. Deriving them from `X(rldicr)` would have been weaker and deriving them from `X(rldicl)` would have been circular, as the brief says.

**Field placement** was taken from the manual's own format diagram at `:29706-29734` (`0-5 opcode | 6-10 S | 11-15 A | 16-20 sh[0-4] | 21-26 mb[5]||mb[0-4] | 27-29 XO | 30 sh[5] | 31 Rc`) and independently confirmed: the handler's own extraction expressions invert to exactly that layout, and the opcode `30 << 26` = `0x78000000` matches the manual's `x'7800 0000'`.

## 3. THE WITNESS -- rung 3, unmodified machine

**Command line**, exactly as run:

```
build/gxemul -V -x -E bareppc -M 64 0x10000:/tmp/ppc_rldicl_dummy.bin
```

with debugger commands on stdin (`r3=...`, `put w`, `unassemble`, `pc=`, `step N`, `reg`, `quit`). The dummy is a 4-byte file that exists only to give the loader a load address; the instructions under test are written into guest RAM with `put w` and then fetched, decoded and executed by the real CPU core.

**Q1 -- which machine and CPU model.** `bareppc`. No CPU override is needed: `machine_test.c:448-451`, `MACHINE_DEFAULT_CPU(bareppc)`, is `strdup("PPC970")`, and `PPC970` is a **64-bit** entry in the in-tree table (`src/include/cpu_ppc.h:87`). The banner confirms it: `cpu: PPC970 (64-bit, PPC, I+D = 64+32 KB, L2 = 512 KB)`. Nothing was edited to get there.

> **AND IT IS NOT ONLY A TEST MACHINE, WHICH CHANGES THE SEVERITY THE WAY THE BRIEF ANTICIPATED -- IN THE BAD DIRECTION.** I drove the same two instructions on all three PPC machines that select a 64-bit CPU, and all three return zero:
>
> | machine | CPU | `rldicl r4,r3,0,32` |
> |---|---|---|
> | `-E bareppc` | PPC970 (64-bit) | `0x0` |
> | `-E testppc` | PPC970 (64-bit) | `0x0` |
> | **`-E macppc -e g5`** | **PPC970 (64-bit)** | **`0x0`** |
>
> `machine_macppc.c:182-184` gives `MACHINE_MACPPC_G5` the `PPC970`. So this is not confined to a synthetic bring-up target: the fork's Power Mac G5 model has a broken `rldicl`.

**Verbatim transcript** (`session_control_transcript.txt`, and the reason the encoding is trustworthy):

```
GXemul> unassemble 0x10000 0x10018
0000000000010000: 39201234 <- li	r9,4660
0000000000010004: 60000000    nop
0000000000010008: 78640020    rldicl	r4,r3,0,32
000000000001000c: 786507c4    rldicr	r5,r3,0,31
0000000000010010: 78664000    rldicl	r6,r3,8,0
0000000000010014: 786747e4    rldicr	r7,r3,8,63
```

The words are **generated** by an encoder built from the manual's field diagram, then re-read by **the tree's own disassembler** (`cpu_ppc.c:902`), which is a different code path from the execute handler. 196 of 196 placed words round-tripped operand-for-operand. That is the defence against this project's hand-assembled-encoding trap: a wrong register field yields zero, and zero is precisely the symptom under test, so an unchecked encoder could have manufactured this entire finding.

### Row results on the COMMITTED build (`witness_committed.out`, **SCORE 19/27**)

```
row                got                  want                 
session            exit0                exit0                ok
live               0x1234               0x1234               ok
seed holds         0x5a5a5a5a5a5a5a5a   0x5a5a5a5a5a5a5a5a   ok
src intact         0xdeadbeefcafef00d   0xdeadbeefcafef00d   ok
disasm xcheck      6/6                  6/6                  ok
zx32 rldicl        0x0                  0xcafef00d           FAIL
zx32 rldicr        0xdeadbeef00000000   0xdeadbeef00000000   ok
rot8 rldicl        0x0                  0xadbeefcafef00dde   FAIL
rot8 rldicr        0xadbeefcafef00dde   0xadbeefcafef00dde   ok
neg apparatus      exit1/-0x1           exit1/-0x1           ok
bits32 live        0x1234               0x1234               ok
bits32 rld bad     TODO                 TODO                 ok
vacuous cell       0x0                  0x0                  ok
vac neighbour      0x0                  0xffffffff00000000   FAIL
census run         190                  190                  ok
census wrong       190                  0                    FAIL
census zero        190                  0                    FAIL
disasm total       196/196              196/196              ok
rldimi sh8         0xffffffffffffffff   0xffffffffffffff00   FAIL
rldimi sh0         0xffffffffffffffff   0xffffffffffffffff   ok
rldimi sh32        0xffffffffffffffff   0xffffffff00000000   FAIL
rlwinm             0xf0                 0xf0                 ok
rlwimi wide        0x5a5a5a5aaaaaaaf0   0x5a5a5a5a000000f0   FAIL
rlwimi sh0         0x5a5a5a5a0000000f   0x5a5a5a5a0000000f   ok
wide live          0xaaaaaaa0000000fa   0xaaaaaaa0000000fa   ok
```

### The controls, and why each one is load-bearing

* **`live`** -- `li r9,0x1234` in the same session reads back `0x1234`. The guest really executes; the readback really works.
* **`seed holds`** -- **this is the control that makes a zero readback mean anything.** Every destination is pre-seeded with `0x5a5a5a5a5a5a5a5a` before `step`. A register that is seeded and stepped over but never written still holds the sentinel. So `0x0` in `r4` means *`rldicl` wrote zero*, not *nothing ever wrote `r4`*. Without this row the whole witness would be consistent with the instruction never having executed.
* **`neg apparatus`** -- a bogus machine name makes `live` go RED (`exit1`, register absent). Without it, `live` is a check that cannot fail.
* **`zx32 rldicr` / `rot8 rldicr`** -- **the discriminating control the brief asked for.** The sibling, in the *same session*, from the *same encoder*, over the *same rotate*, returns `0xdeadbeef00000000` and `0xadbeefcafef00dde` -- both exactly the architectural values. The failure is attributable to `X(rldicl)` and to nothing else in the apparatus.
* **`bits32 rld bad`** -- re-checks the brief's reachability claim from the other side: on `-C PPC603` (32-bit) the same encoded word does not execute as `rldicl`; the decoder prints `TODO: rld* in 32-bit mode?` and goes to `bad`, while `li` still runs. The 32-bit gate at `cpu_ppc_instr.c:4531-4535` is real.

### THE SECOND CHANNEL -- it is not only a wrong value, it is wrong CONTROL FLOW

`cr0_channel.out`, the record form `rldicl.` (`0x78640021`):

```
COMMITTED   r4 = 0x0           cr = 0x20000000   (EQ)
FIXED       r4 = 0xcafef00d    cr = 0x40000000   (GT)
```

`update_cr0` is fed `gpr[ra]`, which is always zero, so **`rldicl.` reports "equal to zero" on every execution regardless of operands.** Any `beq`/`bne` on the result of a masked compare takes the wrong branch. The brief framed the symptom as a wrong register value; this is a second, independent observable, and a future detector should carry a row on it.

## 4. TEST-FIRST: the same script, opposite colour

Both variants were built **in my own `/tmp`**, from `cp -a` copies, with `./configure`, `rm src/cpus/*.o`, `make -j4`, and `[ binary -nt source ]` checked rather than `MAKE_RC` (which reported 0 in both cases and is not trusted here). The three binaries are distinct objects (`md5sum` in `witness_*.out` provenance).

| build | edit | SCORE | census wrong | census zero |
|---|---|---|---|---|
| **committed** | -- | **19/27** | **190/190** | **190/190** |
| **fix** | `tmp \|=` -> `tmp2 \|=` | **24/27** | **0/190** | **0/190** |
| **naive** | delete `& tmp2` | **19/27** | **126/190** | 0/190 |

`candidate_fix.diff` is a single hunk of one line. **Every `rldicl` row flips green under it and no control changes.** The three rows still red under the fix are `rldimi sh8`, `rldimi sh32` and `rlwimi wide` -- the two *other* defects in section 6, which this one-character change does not touch and should not.

That is the discriminator the oracle-correction rule asks for: the expectations were written from the manual before any variant was built, the committed build measures RED against them, and the fix measures GREEN with the identical script.

## 5. ANSWERS TO THE NUMBERED QUESTIONS

**Q2 -- how many (SH,MB) combinations?** **190 distinct cells**, not one. The set is the MB sweep `(0, mb)` for `mb = 0..63`, the SH sweep `(sh, 0)` for `sh = 1..63`, and the diagonal `(k, k)` for `k = 1..63`. All 190 returned exactly zero on the committed build and all 190 returned the architectural value under the fix. I ran a census rather than one case because the brief is right that one licenses the fix while a census makes a detector's coverage claim checkable -- and because "always zero" is a universal claim that deserved more than a single sample. It costs nothing: 26 instructions fit in one session and a session takes 28 ms.

The census source is `rS = 0xFFFFFFFFFFFFFFFF` **deliberately**: with an all-ones source, `ROTL64` is the identity, so the architectural answer is exactly `MASK(MB,63)`, which is non-empty for every `MB` in `0..63`. **Every cell of the census is therefore provably non-vacuous by construction**, which is what makes "190 of 190" a real number. The rotate is exercised separately by the value rows with `rS = 0xDEADBEEFCAFEF00D`.

**Q3 -- is it unconditional, and where would a row be vacuous?** The defect is unconditional in `(SH, MB)`: there is no `(SH, MB)` pair at which the handler does the right thing, because the result does not depend on them at all. **Vacuity is a property of `(rS, SH, MB)` jointly, and I measured a cell that has it.** Row `vacuous cell` uses `rS = 0xFFFFFFFF00000000, SH = 0, MB = 32`: `ROTL64` is the identity, `MASK(32,63)` selects the low 32 bits, and those are all zero, **so the architecturally correct answer is itself `0x0` and the row is GREEN on the broken build.** Its neighbour `MB = 0` on the same source is not vacuous and reds normally.

Generally: a row is vacuous exactly when `ROTL64(rS,SH) & MASK(MB,63) == 0`, i.e. when the selected window of the rotated source happens to be all zeros. The cheap rule for a detector author is **choose `rS` so that every mask window is non-empty** -- all-ones is the safest, and any source with no 64-bit-aligned zero run longer than `64-MB` will do. Note the sharp corner: `MB = 63` selects a *single bit*, so at that end all but one source bit is irrelevant and vacuity is easy to hit by accident.

*One row of my own first draft was vacuous by construction and I corrected it rather than shipping it: `rlwimi wide` originally used the all-ones source, under which a 64-bit-wide rotate and a true `ROTL32` agree bit for bit, so the row went green while proving nothing. It is now driven with `0xAAAAAAAA0000000F`, whose halves differ.*

**Q4 -- the siblings. There are TWO more live defects, so this is a class, not a typo.**

* **`X(rldicr)` (2460-2478) is CORRECT.** Verified by reading and measured green on every row.
* **`X(rlwinm)` (2540) and `X(rlwnm)` (2519) are CORRECT.** Both do `tmp = (uint32_t)cpu->cd.ppc.gpr[rs];` *before* rotating, so the 32-bit rotate is genuinely 32-bit. Measured green.
* **`X(rldimi)` (2486-2509) IS BROKEN -- an uninitialised-ish variable reuse, and the same shape of slip.**

  ```c
  while (sh-- != 0) { ... }            /*  post-decrement leaves sh == -1  */
  m = mb; tmp = 0;
  do { tmp |= ((uint64_t)1 << (63-m)); m ++; } while (m != 63 - sh);
  ```

  `while (sh-- != 0)` exits with **`sh == -1` always**, so `63 - sh` is **always 64** and the mask always runs to bit 63. The architecture (`:29908`, and the prose at `:29909` -- *"1 bits from bit MB through bit 63 - SH"*) says the mask must **end at `63 - SH`**. Measured, `rA` seeded 0 and `rS` all-ones:

  | | got | want |
  |---|---|---|
  | `rldimi rA,rS,8,0` | `0xffffffffffffffff` | `0xffffffffffffff00` |
  | `rldimi rA,rS,32,0` | `0xffffffffffffffff` | `0xffffffff00000000` |
  | `rldimi rA,rS,0,0` | `0xffffffffffffffff` | `0xffffffffffffffff` (agrees -- `SH=0` is the one safe case) |

  So `rldimi` **overwrites `64 - SH` bits of the destination that the architecture requires it to preserve.** `rldimi` is the standard bitfield-insert; a compiler using it to splice a field will destroy everything to the right of that field. Live for every `SH != 0`.

* **`X(rlwimi)` (2560-2585) IS BROKEN in 64-bit mode -- a rotate performed at the wrong width.**

  ```c
  MODE_uint_t tmp = reg(ic->arg[0]), ra = reg(ic->arg[1]);
  tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;
  ```

  `cpu_ppc.c:53` defines `DYNTRANS_DUALMODE_32`, so this file is compiled twice and `MODE_uint_t` is **`uint64_t`** in the 64-bit build. The manual (`:29989`) specifies `r <- ROTL[32](rS[32-63], n)`, and `:6878` defines `ROTL32` as operating on *two copies of bits 32-63* -- **the high half of `rS` plays no part whatsoever.** Here `tmp >> (32-sh)` pulls bits out of the high half straight into the low 32 bits, which is where the mask lives. Unlike its two siblings, this handler never truncates `rS` to `uint32_t`. Measured with `rS = 0xAAAAAAAA0000000F`, `rA` seeded `0x5A5A...`, `rlwimi rA,rS,4,0,31`:

  ```
  got  0x5a5a5a5aaaaaaaf0      want  0x5a5a5a5a000000f0
  ```

  The `0xAAAAAA` in the result is high-half data that the architecture says cannot reach there. The companion rows confirm the attribution: `rlwinm` on the *same source and shift* is correct (it truncates), and `rlwimi` at `SH = 0` is correct (the ternary short-circuits the rotate entirely).

* **Adjacent, not a defect but worth recording:** `rldic` (XO=2), `rldcl` and `rldcr` are **not implemented at all** -- the decoder's `default: goto bad` at `:4538` swallows them. `rldic` in particular is a documented, compiler-emitted instruction.

**Q5 -- do any gates execute this? NO, AND THE REASON IS STRUCTURAL RATHER THAN AN OVERSIGHT.** Your grep result is confirmed and I can say *why*. The tree has two PPC gates, `gate_ppc.sh` and `gate_ppc_halt.sh`, and their probes select:

```
ppc_rounding_probe.py:114   -E macppc -e g4
ppc_halt_probe.py:131       -E macppc -e g4
```

`macppc/g4` is `MPC7400`, which the CPU table marks **32-bit**. So `cpu->cd.ppc.bits == 32` in every PPC gate this project runs, and the decoder sends *every* `rld*` to `bad` before any handler is reached.

> **The finding about the gates is therefore stronger than "no gate covers `rldicl`": no gate has ever instantiated a 64-bit PowerPC CPU at all, so the entire 64-bit-only instruction group -- `rldicl`, `rldicr`, `rldimi`, and the unimplemented `rldic`/`rldcl`/`rldcr` -- is invisible to the gates BY CONSTRUCTION rather than by omission.** It is not a green gate passing over a broken instruction, which would be the worse finding you were checking for; it is a coverage hole with a single cause, and one 64-bit probe closes all of it. `gate_ppc.sh:100` states its own scope honestly (*"machine: macppc/G4, NetBSD kernel loaded so the machine constructs; never executed"*), so nothing here is a false record.

**Q6 -- anything else.**

1. **No boot rig reaches this.** The witness is rung 3 and I could not get it higher: the only PPC kernel in `regress/images` is `netbsd401-macppc-GENERIC`, which the gates load onto a **G4** and never execute. So `macppc -e g5` is *constructible and reachable by a guest instruction*, but nothing in the tree boots a 64-bit PowerPC guest. That is the honest severity ceiling -- the defect is catastrophic for any 64-bit PPC guest and no in-tree guest is currently one.
2. **The `while (sh-- != 0)` idiom is the shared root of two of the three defects.** It leaves `sh == -1` in `rldicl`, `rldicr` and `rldimi` alike. `rldicr` survives only because it never reads `sh` again; `rldimi` reads it and is broken. Any future edit that reaches for `sh` after the rotate loop in *any* of these three will be wrong the same way. If a round fixes `rldimi`, the durable repair is to save `sh` before the loop rather than to patch the `63 - sh` expression.
3. **A detector for this must not use a survival oracle.** Nothing dies here -- the guest runs on with wrong data. The channels available are the destination register, and CR0 for the record forms. Both are in this probe.
4. **The probe is reusable as the detector skeleton.** `opus_ppc_rldicl_witness_20260910.py` takes the binary as `argv[1]`, is machine-unmodified, runs in 0.3 s for 27 rows and 190 census cells, carries its own negative-apparatus control, and ends in `PPC_RLDICL_WITNESS_DONE`. It already reds on the two sibling defects, so it would need its contract stating carefully: it is a *family* instrument, not an `rldicl` instrument.

## 6. HOUSE RULES -- verification

* **Nothing in `GXEMUL-SEC` was written.** `git status --porcelain` shows the **same four `M` entries** as the baseline I captured before starting (`sgi_de_primop_probe.py`, `dev_lca.c`, `dev_mk48txx.c`, `dev_sgi_re.c`). `src/cpus/cpu_ppc_instr.c` still carries its original mtime `2026-08-05 10:43:15` and hashes `bb5757ab395b26f48b0cb14f0e8f0482`, identical to `build/src/`.
* **The only new path I created is `regress/artifacts/ppcrldiclzero/`.** *Other* new untracked entries appeared in `git status` during my run (`artifacts/faultpair/`, `artifacts/fbctrlportkill/`, `mk48nvramkill/PASS2_brief_20260910.md`, `mk48nvramkill/killtable_20260910/`, `regress/mk48_nvram_probe.py`) -- **these are not mine**; they are concurrent activity in the same working tree, consistent with `CHECKPOINT.md` being rewritten under me. Recorded so nobody attributes them to this seat.
* **Builds were in `/tmp` only** (`/tmp/gxrldicl_fix`, `/tmp/gxrldicl_naive`), each a `cp -a` with exactly one hunk, each verified by `[ binary -nt source ]` rather than by `MAKE_RC`. Probes were written to the session scratchpad.
* **Two-part clearance run, not asserted**, before any measurement: `cpu_ppc_instr.c` is **not** in `tools/est_divergence.txt` (derived, 6 entries, none matching), so the shared-file recipe applies; `cmp build/src/cpus/cpu_ppc_instr.c GXEMUL-SEC/...` is CLEAN and `build/gxemul` (2026-09-10 13:17) is newer than the source (2026-08-30 18:00). No `.MUTANT` sentinel exists. The committed binary is a valid instrument for this file.
* Artifacts preserved at `regress/artifacts/ppcrldiclzero/`: `opus_ppc_rldicl_witness_20260910.py`, `witness_committed.out`, `witness_fix.out`, `witness_naive.out`, `cr0_channel.out`, `candidate_fix.diff`, `session_control_transcript.txt`. All three witness logs were verified by `tail -1` to end in `PPC_RLDICL_WITNESS_DONE` after the runs finished.

*Score claims name their logs: 19/27 is `witness_committed.out`, 24/27 is `witness_fix.out`, 19/27-with-126-wrong is `witness_naive.out`. All three were re-run into those exact files rather than transcribed from the console.*
