# `shortread` — the PRE-TABLE SIBLING-PARITY CHECK, run before the mutant table

*Derived 2026-08-27 by reading `src/disk/diskimage.c` and by `git log -L`, not
transcribed. Every claim below names how it was settled.*

---

## 1. THE FORK ALREADY ANSWERED THIS QUESTION, IN NEW CODE, IN THE SAME FILE

`diskimage__internal_access()` has **three** read-path producers of `lendone`.
Only one has the defect.

| producer | short-transfer policy | who wrote it |
|---|---|---|
| `fwrite_helper()` (write sibling) | **refuse**: rejects unaligned/non-block-multiple up front (`#164`), `return 0` on a short write | fork |
| `diskimage_access__cue()` | **two policies, split by CAUSE** — see below | fork (`5ee491e`) |
| `diskimage_access__cdrom()` | `return 0` on a short sector read | — |
| **`fread_helper()`** | **advance by REQUESTED, count ACTUAL** — the defect | **upstream** (`39748e3`) |

### The CUE path is the load-bearing precedent, and it splits by cause

```c
		if (t == NULL) {
			/*  Sector belongs to no track:  */
			memset(buf + total_copied, 0, chunk);      /*  <- FILL IN PLACE  */
		} else {
			...
			bytes_read = fread(buf + total_copied, 1, chunk, f);
			if (bytes_read != chunk) {
				fatal("[ diskimage_access__cue(): short read ... ]\n", ...);
				total_copied += bytes_read;                /*  <- STOP  */
				break;
			}
		}

		total_copied += chunk;
```

* **Unbacked BY DESIGN** (no track covers this sector) -> zero-fill **at its own
  position**, count it, continue.
* **UNEXPECTED short read** -> record the contiguous prefix and **stop**, so the
  caller's tail `memset` is correct by construction.

### *** AND THE WARRANT IS REAL, NOT ASSUMED -- I CHECKED WHETHER THE FORK ACTUALLY
### CHOSE IT, BECAUSE A PRECEDENT INHERITED FROM UPSTREAM IS NOT A DECISION. ***

```
git log --oneline -L 1113,1140:src/disk/diskimage.c
  5ee491e  Security review (#130-#154) + feature round (#120-#129): 23 fixes

grep -c "diskimage_access__cue" <pristine 2021 upstream copy>/disk/diskimage.c
  0
```

**The whole CUE path is fork-authored and absent from upstream.** So this is a
deliberate choice made by this project when it wrote new code for exactly this
question -- which is what makes it transferable at all.

By contrast:

```
git log --oneline -L 1405,1418:src/disk/diskimage.c
  00d546d  #472 b115: an unaligned overlay read took its bytes from the wrong layer
  39748e3  Import GXemul 0.7.0 (unmodified upstream baseline)
```

`fread_helper()`'s accounting is **upstream residue the fork has never revisited**.
`#472` came close and was aimed at the CLAMP, not at the short-read arithmetic.
*That is why it survived: the round that touched these exact lines was asking a
different question.*

---

## 2. THIS NARROWS MY OWN REACHABILITY CLAIM, AND THE NARROWING IS THE HONEST PART

The brief implies any short read corrupts. **It does not.**

**The defect needs a short read FOLLOWED BY A SUCCESSFUL ONE.**

Work the pure past-EOF case -- the one every image in this project relies on,
because advertised capacity is rounded up to whole cylinders:

* iteration 1 reads 200 of 512 and stops short;
* **every later iteration reads 0**, because the file ended;
* nothing is written past byte 200, so `totallenread == 200` and the caller's
  tail `memset(buf + 200, 0, len - 200)` covers the whole remainder.

**Today's code is ACCIDENTALLY CORRECT there** -- and that is why this has never
been seen. Corruption requires a *mid-image* short source with readable blocks
after it: a truncated overlay whose bitmap claims a block, with base blocks
behind it. That is what the reproduction constructs, and it is
**not guest-reachable** -- a guest cannot truncate a host file.

---

## 3. WHERE THAT LEAVES THE OPTION SET

The brief leaned **B** (fill the hole in place, count it as done). The fork's own
warrant points at **A** (stop and report the contiguous prefix).

*** BUT THE WARRANT'S ANALOGY IS IMPERFECT, AND THE DISANALOGY IS SPECIFIC. ***
In the CUE path a short read means one track FILE is bad, and the sectors after it
usually live in that same file -- so stopping discards data that is probably bad
anyway. In `fread_helper()` **each block may come from a DIFFERENT file**: a short
read of the OVERLAY says nothing whatever about the BASE image. Option A therefore
discards good data from a healthy file because a *different* file was short.

Measured on the reproduction (1536 bytes, block 0 from a 200-byte overlay,
blocks 1-2 from a healthy base):

| | stale caller bytes | valid base bytes delivered | caller told |
|---|---|---|---|
| shipped | **312** | 712 of 1024 | success |
| **A** stop | 0 | **0** of 1024 | success |
| **B** fill in place | 0 | **1024** of 1024 | success |

Both fixes kill the stale hole. **B additionally preserves 1024 bytes that A
throws away**, and neither can signal failure to the caller, because the read side
has no way to -- `writeflag && lendone < len` is the only failure path and it is
write-only.

**So this is a genuine split**: precedent says A, consequence says B. It is the
panel's to settle, and the pass-2 packet carries both halves.

*I am recording that my pass-1 brief argued B without knowing any of this. The
sibling-parity check is the reason I know it, and it is the third item on the
pre-table checklist -- the one that "only seemed unreachable because it was
approached from the mutant side".*
