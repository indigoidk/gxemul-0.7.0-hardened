# BUILD THE WITNESS for `alphatbinegsel` — a measurement job, not a reading

**You are the measurement seat. This asks you to BUILD AND RUN a probe, not to review one.**
If you cannot build it, say so plainly and say what stopped you — that is a real answer and the
round proceeds as documented-only with the attempt recorded.

## 0. HARD CONSTRAINTS — read these first

* **The tree under review is `C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/`.** There is a pristine 2021
  upstream copy at the project root that will make you confidently wrong; ignore it.
* *** DO NOT WRITE TO `GXEMUL-SEC/`, `build/`, `build-asan/`, `est/`, or `/tmp/gxsec-build`. ***
  Copy what you need to your own scratch directory and work there. Verify afterwards that the
  project trees are untouched.
* Build inside `wsl -d Gentoo` — the default distro has no `make`. `rm src/cpus/*.o` first.
  **`MAKE_RC` has been observed reporting 0 on a failed build, so the freshness test
  `[ binary -nt source ]` is the oracle, never the return code.**
* The emulator binary is a Linux ELF; run it under WSL, not git-bash.

## 1. THE DEFECT

`src/cpus/cpu_alpha_palcode.c`, `case 0x33 /* PAL_OSF1_tbi */`:

```c
	if (a0 >= 1)
		cpu->invalidate_translation_caches(cpu, a1, INVALIDATE_VADDR);
	else
		cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
```

`a0` is a **`uint64_t`** (captured at `:165`), with no signed cast. `alpha_cpu.h` defines
`ALPHA_TBIA()` as `alpha_pal_tbi(-2, 0)` and `ALPHA_TBIAP()` as `alpha_pal_tbi(-1, 0)`. So `-2`
compares as `0xff..fe >= 1` → **TRUE** → the VADDR branch, with `a1 = 0`.

The VADDR branch **invalidates only the entry matching `(vaddr_page & vaddr_mask)`**; the ALL
branch has no address test and walks every valid entry.

> **THEREFORE `ALPHA_TBIA()` — meaning *invalidate every TLB entry* — invalidates cached virtual
> page ZERO and nothing else. `ALPHA_TBIAP()` misdispatches identically.**

**The proposed fix is `if (a0 >= 1 && a0 <= 3)`.** Do not apply it to any project tree; apply it in
your scratch copy only, to measure the post-fix side.

## 2. FIVE TRAPS, EACH MEASURED OR DERIVED BY A SEAT — a witness that hits any of them is vacuous

1. **THE DEBUGGER ALL-FLUSHES BETWEEN INTERACTIONS.** When
   `debugger_n_steps_left_before_interaction` is not positive it calls `cpu_create_or_reset_tc` and
   `invalidate_translation_caches`. **So the fill, the remap, the `tbi` and the observing load must
   all be inside ONE `step N`** — otherwise both builds re-walk and the row is GREEN on the
   defective build.
2. **K0SEG IS CHECKED BEFORE `ptbr`.** A K0SEG address never consults the page table, so the
   obvious substrate cannot witness this at all.
3. *** DO NOT USE VPN 0 AS THE TEST PAGE. *** HEAD's defective arm flushes page zero, so a witness
   on page 0 goes **GREEN ON THE DEFECTIVE BUILD** — the defect is that only page 0 is flushed, so
   page 0 is the one page that cannot witness it.
4. **ZERO `a1` EXPLICITLY** before `call_pal 0x33`. If `a1` carries the test VPN, HEAD flushes
   exactly the entry under observation and the broken build looks correct.
5. **THE REMAP MUST CHANGE THE OBSERVED BYTES.** If the old and new pages hold the same data, the
   load cannot distinguish a cached hit from a re-walk.

## 3. A WORKING HARNESS EXISTS — start from it, do not hand-roll pty plumbing

`regress/alpha_swpctx_v0_probe.py` was written and measured today on this exact machine. It gives
you, already working:

* `pty.fork()` + `os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", "alphabook1", "-M", "64",
  "0x20000000:" + DUMMY])`, with `alpha_dummy.bin` an 8-byte stub;
* an Alpha memory-format encoder (`LDA`, `LDAH`, `LDQ`, `STQ`, `load_const`) and
  `CALL_PAL(func) = (0x00 << 26) | func`;
* the debugger command shapes that work: `put d <addr>, <val>` / `put w <addr>, <val>` /
  `pc=<addr>` / `step N` / `print <reg>`, and a `printed()` regex to read a register back;
* **the measured fact that an all-zero dummy decodes as `call_pal PAL_halt` and STOPS THE MACHINE**
  before any tick — plant a self-branch (`br r31,-1` = `0xc3ffffff`) if you need it to free-run.

`regress/lca_confbus_probe.py` and `regress/alpha_pfnoffset_probe.py` are two more working Alpha
probes on the same machine; `alpha_pfnoffset_probe.py` in particular already walks a page table,
so **read it before building one from scratch.**

## 4. WHAT THE PROBE MUST PRODUCE

* **ORACLE POLARITY: assert the CORRECT behaviour**, so the row is RED on the committed build and
  GREEN with the fix applied, **using the same script**. That is what makes it a witness rather
  than a restatement of the source.
* **A LIVENESS CONTROL** — a known value returns through the same path.
* **AN ATTRIBUTION CONTROL** — something that distinguishes "the flush was wrong" from "the
  sequence never executed". On `#514` this was the single most useful row: reading the register the
  handler wrongly wrote proved it had RUN, which a value check alone cannot.
* Print a row table and a `RESULT=n/m` line, and copy the raw output somewhere durable.

## 5. REPORT

1. **The two scores** — committed build and fixed build — with the raw output.
2. **Which of the five traps bit**, if any, and how you detected it.
3. **Whether the witness distinguishes `TBIA` from `TBIAP`** (`-2` versus `-1`), or only shows the
   misdispatch generically.
4. **If you could not build it: exactly where it stopped.** An honest failure with a named cause is
   worth more than a probe that passes for the wrong reason.
