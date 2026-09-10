# sgirandomcolour -- Rung-3 Witness Report (agy measuring seat)

**Date**: 2026-09-10  
**Seat**: agy (fallback measuring seat)  
**Binary under test**: `build/gxemul` (READ-ONLY, HEAD commit `1ce8296`)  
**Instrument**: `regress/sgi_re_colourdefault_probe.py`  
**Frozen copy**: `regress/artifacts/sgirandomcolour/witness_20260910/sgi_re_colourdefault_probe.asrun.py`  
**Instrument MD5**: `bc0bbc6a58e137034094e08c07b87f8e`

---

## 1. Executive Summary

This report provides the rung-3 witness for the unhandled colour mode default arm defect in `src/devices/dev_sgi_re.c` (`horrible_getputpixel`).

When performing a drawing engine (DE) PUT operation, `horrible_getputpixel()` extracts `color_mode = mode & DE_MODE_TYPE_MASK` (mask `0x000000f0`, bits 4–7). Only four of the sixteen possible nibble values are implemented (`DE_MODE_TYPE_CI` `0x00`, `DE_MODE_TYPE_RGB` `0x10`, `DE_MODE_TYPE_RGBA` `0x20`, `DE_MODE_TYPE_ABGR` `0x30`). The remaining twelve values fall through to `default:`, which executes:
```c
default:buf[0] = random();
	buf[1] = random();
	buf[2] = random();
	buf[3] = random();
	// TODO.
	fatal("[ put: color mode = 0x%x ]\n", color_mode);
```
Because `fatal()` in `src/core/debugmsg.c` logs the message and returns without exiting, the common tail of `horrible_getputpixel()` proceeds to execute:
```c
cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
    buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
```
writing four host-PRNG bytes into the guest's framebuffer / tile memory.

The defect affects both documented colour modes (`DE_MODE_TYPE_YCRCB` `0x000000f0` from `src/include/thirdparty/crmfbreg.h`) and undocumented/reserved colour mode encodings (e.g., `0x50`).

---

## 2. Row Table (got / want)

The probe was run twice against the committed `build/gxemul` binary without modification.

### Run 1 (`HEAD_run1.out`)

| Row | Got | Want | Result | Note |
|---|---|---|---|---|
| `live` | `0xaabbccdd` | `0xaabbccdd` | **ok** (PASS) | LIVENESS: supported RGBA DE PUT lands known colour in destination |
| `ycrcb put` | `0x56e8857a` | `0x11223344` | **FAIL** (RED) | DEFECT: YCRCB (0xf0) PUT must leave sentinel unchanged; on HEAD clobbered |
| `ycrcb attrib` | `yes` | `yes` | **ok** (PASS) | ATTRIBUTION: transcript carries `[ put: color mode = 0xf0 ]` |
| `reserved put` | `0x5e1b3ef4` | `0x11223344` | **FAIL** (RED) | RESERVED: unsupported 0x50 PUT must leave sentinel unchanged; on HEAD clobbered |
| `determinism` | `differ` | `identical` | **FAIL** (RED) | DETERMINISM: repeat YCRCB put; post-fix identical (sentinel), pre-fix differs across runs |

**Score**: `SGICOLOUR_RESULT=2/5`  
**Sentinel**: `SGICOLOUR_DONE` (exit code 1)

### Run 2 (`HEAD_run2.out`)

| Row | Got | Want | Result | Note |
|---|---|---|---|---|
| `live` | `0xaabbccdd` | `0xaabbccdd` | **ok** (PASS) | LIVENESS: supported RGBA DE PUT lands known colour in destination |
| `ycrcb put` | `0x38abc4e1` | `0x11223344` | **FAIL** (RED) | DEFECT: YCRCB (0xf0) PUT must leave sentinel unchanged; on HEAD clobbered |
| `ycrcb attrib` | `yes` | `yes` | **ok** (PASS) | ATTRIBUTION: transcript carries `[ put: color mode = 0xf0 ]` |
| `reserved put` | `0x80618a59` | `0x11223344` | **FAIL** (RED) | RESERVED: unsupported 0x50 PUT must leave sentinel unchanged; on HEAD clobbered |
| `determinism` | `differ` | `identical` | **FAIL** (RED) | DETERMINISM: repeat YCRCB put; post-fix identical (sentinel), pre-fix differs across runs |

**Score**: `SGICOLOUR_RESULT=2/5`  
**Sentinel**: `SGICOLOUR_DONE` (exit code 1)

---

## 3. Four Bytes Seen at `ycrcb put`

- **Pre-painted Destination Sentinel**: `0x11223344` (`11 22 33 44`)
- **Source Foreground Colour**: `0xaabbccdd` (`aa bb cc dd`)
- **Observed Destination (Run 1)**: `0x56e8857a` (`56 e8 85 7a`)
- **Observed Destination (Run 2)**: `0x38abc4e1` (`38 ab c4 e1`)
- **Observed Destination (Repeated in-probe session)**: `0x38abc4e1` in run 2, `0x74f0664d` / `0x31b37ed1` in exploratory runs.

### Classification
**Neither.** The destination received neither the pre-painted sentinel (`0x11223344`) nor any packing/recombination of the foreground colour (`0xaabbccdd`). Instead, the destination was overwritten with four pseudorandom bytes produced by `buf[0..3] = random()`.

---

## 4. Attribution Text

The execution transcript for `ycrcb put` captures the exact diagnostic emitted by the `default:` branch:
```
[ put: color mode = 0xf0 ]
```
Similarly, for `reserved put` (mode `0x1250` with colour type `0x50`), the transcript captures:
```
[ put: color mode = 0x50 ]
```
This confirms direct reachability of the `default:` arm in `horrible_getputpixel()` and attributes the destination corruption specifically to this path.

---

## 5. What Was Read vs What Was Assumed

### Read from Codebase:
1. `src/devices/dev_sgi_re.c` (lines 308–340): Verified `color_mode = mode & DE_MODE_TYPE_MASK` and the four handled cases (`CI`, `RGB`, `RGBA`, `ABGR`). Verified the `default:` arm populates `buf[0..3]` with `random()`, calls `fatal()`, and proceeds to `cpu->memory_rw(..., MEM_WRITE, ...)`.
2. `src/include/thirdparty/crmfbreg.h` (lines 328–333): Verified `DE_MODE_TYPE_YCRCB` is `0x000000f0` and `DE_MODE_TYPE_MASK` is `0x000000f0`.
3. `src/core/debugmsg.c` (lines 384–398): Verified `fatal()` prints the diagnostic at default verbosity and returns without terminating the emulator process.
4. `src/core/main.c` (lines 688–692): Verified `if (!skip_srandom_call) { gettimeofday(&tv, NULL); srandom(tv.tv_sec ^ getpid() ^ tv.tv_usec); }`. The emulator process seeds the host PRNG with PID and timestamp upon startup.

### Assumed vs Observed:
- **Assumption in Brief**: The brief noted *"unseeded `random()` is deterministic per process; say what you observe, do not assert what it should be."*
- **Observed**: `gxemul` seeds `random()` with `tv.tv_sec ^ getpid() ^ tv.tv_usec` on startup in `main.c`. Therefore, distinct `gxemul` processes produce different pseudo-random bytes across runs (`0x56e8857a` vs `0x38abc4e1`).
- **Post-Fix Expectation**: Post-fix, an unhandled colour mode PUT will be declined (skipping `memory_rw`), so the destination will deterministically retain the sentinel `0x11223344` on both runs.

---

## 6. Verification and Unexpected Events

- **Host Survival**: The host process survived all sessions (`alive=True`); no unexpected crashes or timeouts occurred.
- **Defect Attribution**: The failure of `ycrcb put` and `reserved put` is wholly attributed to the `horrible_getputpixel()` `default:` arm clobbering memory with PRNG data.
- **Sentinel Consistency**: Both runs printed `SGICOLOUR_RESULT=2/5` followed by `SGICOLOUR_DONE` as their final lines.
