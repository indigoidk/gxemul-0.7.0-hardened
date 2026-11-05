# m_memc RESUMED restatement (agent a3a5ac29b58a7c4f2; the first run fell back to opus-4-8 after a refusal; this restatement, from the saved logs only, is claude-opus-5-5 at 2026-11-04T08:18:48.342Z).

OPUS_SEAT_ALIVE_20261104_MMEMC

**VERDICT: ORDER-CONFIRMED.** If the two `exit(1)` calls are replaced by declined register accesses and the array read before the switch is left unbounded, AddressSanitizer reports that read at `dev_mvme187.c:68`. With the draft's bound added, both offsets run clean.
**DRAFT: RESULT 21/21.** All four declined reads return 0. The declined memconf write leaves memconf at 0x3. Each declined path prints one notice and the session continues.

I re-read every figure from the saved logs and ran nothing new. Two corrections to my earlier report came out of that, listed at the end.

### Variants (bodies from the saved `.diff` files)
- **A1:** the exits become declines and the default arm sets `odata = 0`. There is no bound. Its diff starts at line 75, so line 68 is still the original array read `odata = ((uint8_t*)&d->memcreg)[relative_addr];`.
- **A2:** the same as A1, except the default arm does not reset `odata`, so the value from the line-68 array read is passed to the guest. There is no bound.
- **A3:** the draft. The array read moves inside the chipid/chiprev/memconf arms (that is the bound), and both declines print a notice once. The diff bodies for the ASAN clone and the plain clone are identical, so the same draft was built both times.

### Results
Logs are under `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus_20261104\m_memc\`.

| variant | access | result (from the log) | artifact |
|---|---|---|---|
| A1, ASAN | `ld.bu` +0x7c | 0 ASAN reports; `reg` and `quit` reached; pc 0x10004, r2 0x0 | `out_asan\A1_off_7c.txt` |
| A1, ASAN | `ld.bu` +0xff | 0 ASAN reports; `reg` and `quit` reached; r2 0x0 | `out_asan\A1_off_ff.txt` |
| A2, ASAN | `ld.bu` +0x7c | heap-buffer-overflow, READ of size 1, frame #0 at `dev_mvme187.c:68`; "0 bytes after 124-byte region"; transcript stops at `step 1` (no `reg`, no `quit`) | `out_asan\A2_off_7c.txt` |
| A2, ASAN | `ld.bu` +0xff | heap-buffer-overflow, READ of size 1, frame #0 at `dev_mvme187.c:68`; "131 bytes after 124-byte region"; transcript stops at `step 1` | `out_asan\A2_off_ff.txt` |
| A3, ASAN | `ld.bu` +0x7c | 0 ASAN reports; "unimplemented read from offset 0x7c (once)"; `reg` and `quit` reached; r2 0x0 | `out_asan\A3_off_7c.txt` |
| A3, ASAN | `ld.bu` +0xff | 0 ASAN reports; "unimplemented read from offset 0xff (once)"; r2 0x0 | `out_asan\A3_off_ff.txt` |
| A3, plain | repo probe | 21 rows, 21 ok, 0 FAIL; RESULT 21/21, CONTROL OK, SYMPTOM ABSENT, RED none; `MVME187_MEMC_PROBE_DONE` present; the four formerly fatal sessions record exit0 | `out_plain\probe.out`, `out_plain\probe_work\` |
| A3, plain | `ld.bu` +0x0c | r2 0x0, pc 0x10004; notice "offset 0xc (once)" | `out_plain\rd_0x0c.txt` |
| A3, plain | `ld.bu` +0x7c | r2 0x0, pc 0x10004 | `out_plain\rd_0x7c.txt` |
| A3, plain | `ld.bu` +0xff | r2 0x0, pc 0x10004 | `out_plain\rd_0xff.txt` |
| A3, plain | `ld.bu` +0x10c | r2 0x0, pc 0x10004; folds to controller 1, offset 0xc | `out_plain\rd_0x10c.txt` |
| A3, plain | `st.b` 0x07 to +0x08, then `ld.bu` +0x08 | the store line shows `[0xfff43008] = 0x07`; afterwards r2 0x3, pc 0x10008 (two instructions); "memconf write 0x7 declined (once)" | `out_plain\memconf_wr_then_rd.txt` |

### ASAN text, verbatim (`out_asan\A2_off_7c.txt`)
```
==1288==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x774c505e0e3c at pc 0x57e51bfd8140 bp 0x7fff47c7bad0 sp 0x7fff47c7bac0
READ of size 1 at 0x774c505e0e3c thread T0
    #0 0x57e51bfd813f in dev_mvme187_memc_access /tmp/gxopus_memc_asan/src/devices/dev_mvme187.c:68
```
The allocation note reads `0x774c505e0e3c is located 0 bytes after 124-byte region`, with the allocation in `devinit_mvme187` at line 101. So the register struct is exactly 124 bytes, and +0x7c is the first byte past it.

### What is settled
- **The ordering claim (measured).** With the exits removed and no bound, the array read reaches the guest and AddressSanitizer reports it (A2). The draft's bound removes it (A3).
- **One caveat (measured).** A1 shows no report. When the default arm overwrites `odata` with 0, the `-O3` compiler can drop the now-unused array read on that path. This is the same reason the original build showed no report: the `exit(1)` made the read's result unused there. So whether an unbounded intermediate shows the defect depends on the exact form of the decline. The bound is what reliably prevents it, and the draft has it.
- **The draft's behaviour (measured).** The probe gives 21/21, every declined read returns 0, the declined memconf write does not change the register, and each path prints one notice.

### Not settled (not measured)
- Whether a memconf write should be declined or accepted. Firmware may expect its write to read back.
- Whether controller 1 should keep sharing one struct with controller 0.
- Whether in-range unimplemented offsets (0x0c to 0x7b) should return the stored struct byte instead of 0.
- Access widths other than a byte, and stores to registers other than memconf.

### Corrections to my earlier report
1. I said the +0xff ASAN text was "identical bar addresses". The error line and frame #0 do match, but the location note differs: 0 bytes after the region at +0x7c (offset 124) and 131 bytes after it at +0xff (offset 255).
2. The exit statuses I gave for the ASAN runs (rc=0 and rc=1) came from console output and are not in any saved file. The saved evidence is the transcript itself: the A2 runs stop at `step 1` with the ASAN report, while A1 and A3 reach `reg` and `quit`. For the plain-build probe, the saved transcripts do record the exit statuses (exit0 for each formerly fatal row, and exit1 for the bogus-machine control row, which expects it).

The ASAN-build transcripts also contain `[ pcc2: IPL = 0, MASK = 0 => no assert ]` lines. They come from the `dev_pcc2.c` already in `build-asan`, not from the memory-controller code.

Both scratch clones were removed earlier. No project tree was written.
