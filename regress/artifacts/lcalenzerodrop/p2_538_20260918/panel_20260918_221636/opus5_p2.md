OPUS_SEAT_ALIVE_20260918_538P2
claude-opus-5[1m]
VERDICT: CLOSES -- all four floor cells ({write arm} x lane 0..3 at C=16) are rowed. Each one is shown red-capable by the single variant that exempts that lane alone: vc_ne0..3 red exactly l0w16 / low16 / l2w16 / wide. So the lane-1 escape is killed and 0 of 4 cells are open. Everything else I found is an L4 records nit or harness hardening, and none of it is a floor breach.

# #538 pass 2: Opus 5 seat

**How I worked:** read-only. No builds and no emulator runs.
- **Read:** the brief; the working-tree `lca_widewrite_probe.py`; `closure538_20260918/` in full (PRETABLE, frozen instrument, `mk538`, all 16 variant diffs, all 17 raw logs, and selected transcripts); my own `opus_p2_20260918/` (README, RESULTS, variant diffs).
- **Source read:** `dev_lca.c` at 8bd97e4/HEAD, plus `core/memory.c` `store_buf`, `cpu_alpha_palcode.c` `alpha_prom_call`, and the register models `dev_ns16550.c`, `dev_8259.c`, `dev_lpt.c`.
- **Beyond the brief's list:** the header region of `lca_isalane_probe.py` (:130-224), because Q4 is about it.

**What I verified before answering:**
- **The brief's inlined diff is the real diff.** `git diff -- regress/lca_isalane_probe.py regress/lca_widewrite_probe.py` has md5 `05787748…`, which is the same as the brief's fenced block. `diff` of the two is empty, and there are 6 hunks. So the diff was delivered.
- **The baseline is 8bd97e4's dev_lca.c.** `logs/INSTRUMENT.md5`'s dev_lca.c hash `8084ff07…` equals the 8bd97e4/HEAD blob, so the table ran on 8bd97e4's file. The working tree's `71be9474…` is the later #540 edit.
- **The shipped probe matches the frozen instrument except for one paragraph.** The frozen instrument `4c74db01…` differs from the working-tree probe only by the MEASURED paragraph (`diff`, rc 1, one added block).
- **The ordering holds:** PRETABLE 19:38:31, frozen instrument 21:03:39, first leg about 21:18.
- **All 17 legs completed cleanly:** every raw log ends in `WIDEWRITE_DONE`, and all 68 cell lines say `retried=none`.
- **Every variant is a single edit.** All 16 variant diffs are one-edit and match `mk538.frozen.py`, and every variant build recompiled `dev_lca.c`.
- **The real emulator delivered len > 8 at these cells.** KILLLEN8's `transcript_KILLLEN8.wide:98` reads `[ writing to device 'lca_isa' addr 00005fe0 failed ]`: the handler's `len > 8` refusal fired. This is the empirical width evidence for the measured binary.

---

## Q1 -- DOES IT CLOSE?

**The floor as ruled is {write arm} × {lane 0, 1, 2, 3} at C=16.**
- **Premise checked:** at len 16, `ofs = (relative_addr & 3) % 16` is exactly the lane (dev_lca.c:297), and the write arm forwards `data[ofs]` (:300-302).
- **Chunking checked:** I replayed `store_buf` (memory.c:837-857) by hand. `0x5fe0`, `0x5f80`, `0x420` and `0x5fc0` each fail the 1024, 256 and 64 alignment tests, or fail the n ≥ 64 test, and pass at 16. So each cell is ONE 16-byte chunk reaching the handler whole.
- **Length checked:** GETENV's `len = a3; if (strlen(s) < len) len = strlen(s)+1` (palcode.c:141-143) gives 16 for a 16-character `-o` string.

| lane | cell / register (port) | row that pins it | preset → want | measured red under |
|---|---|---|---|---|
| 0 | l0w16 / COM2 MCR (0x2fc) | `l0w16 getenv` | 0x03 → 0x41 `'A'` | **vc_ne0 (this row alone, 12/13)**, vc, M2_len8, KILLLEN8 |
| 1 | low16 / 8259 IMR (0x021) | `low16 getenv` | 0xff → 0x42 `'B'` | **vc_ne1 (this row alone, 12/13)**, vc, vf (0x41), M2_len8, KILLLEN8, and ve (incidental) |
| 2 | l2w16 / COM2 MSR (0x2fe) | `l2w16 getenv` | reads 0xb0 → 0xf3 (`'C'` \| 0xb0) | **vc_ne2 (this row alone, 12/13)**, vc, vf (0xf1), M2_len8, KILLLEN8 |
| 3 | wide / COM2 SCR (0x2ff) | `wide getenv` | 0x5a → 0x44 `'D'` | **vc_ne3 (this row alone, 12/13)**, vf (0x41), M2_len8, KILLLEN8 |

**Zero open cells: 0 of 4 open, 4 of 4 rowed and red-capable.** Each cell is pinned independently, because the one-lane exemption vc_neL reds exactly its own lane's row and nothing else. That is the strongest form the evidence could take.

**The lane-1 escape the ruling named** (`&& (len <= 8 || (P & 3) != 1)`) is vc_ne1. It scored 12/13, and `probe_vc_ne1.raw` shows `low16 getenv 0xff` (preset kept) against 0x42.

Variant denominators:

| group | variants | result |
|---|---|---|
| floor-shaped | M2_len8, KILLLEN8, vc, vc_ne0..3, vf | **8 of 8 killed** |
| disclosed class | va, vb, ve, vg, vt1, vt2 | 5 of 6 escape as predicted; ve is killed incidentally at port 0x21 |
| equivalent | vd, vh | 2 of 2 score 13/13 |

All 17 matched PRETABLE, register values included.

**Why the channel holds for each register.** I read the device code rather than taking the xforms on trust:
- SCR, MCR and IMR each store and return the full byte (`dev_ns16550.c` default arm and `com_mcr`; `dev_8259.c` case 0x01).
- The MSR ORs `0xb0` on every access (ns16550.c:128; `comreg.h` DCD 0x80, DSR 0x20, CTS 0x10). Even so, the 16 string bytes stay distinct under `| 0xb0` (0x41..0x4f → 0xf1..0xff, and 0x50 → 0xf0). So lane-2 ROUTING is fully pinned. See Q2 for the three bits it cannot see.

---

## Q2 -- THE CONTRACT

**None of (i)-(viii) lies inside the ruled floor.** Each warrant checks out, with the corrections below.

- **(i) Width thresholds above 16.** Outside the floor: they are serviced at C=16. The warrant is correct.
  - "each is MEASURED killed at a wider cell in opus_p2_20260918" is **true**. From my RESULTS.txt:
    - va: red at l0w64, l2w64, kbc256 and kbc1024
    - vb: red at l0w64 and kbc1024
    - vw64: red at kbc256 and kbc1024
    - vw256: red at kbc1024

    Those kills came from my scratch cells, not from the shipped detector, and the text says "not rowed here". That is honest.
  - Nit: "the body tests `len` only against 0" should also say that `% len` separates len 1/2/3 from ≥ 4. It is irrelevant above 16.
- **(ii) Port-conditioned refusals.** Outside the floor, but the wording is too broad. **The lane IS two port bits**, so a refusal keyed on `P & 1` or `P & 3` is "port-conditioned", sits inside the floor, and is caught. For example, `len > 8 && (P & 1)` reds low16 and wide. Say "port bits ABOVE the lane (P >> 2), or port values and ranges", as the parent's p_port10 does ("keyed on an EXACT PORT VALUE"). Otherwise the line mis-discloses floor cells as debt.
- **(iii) The discarded a<4:0>.** Outside the floor, as the warrant says: they are shifted away before any use. vg and vt1 escaped as predicted.
- **(iv) Chunk position ≥ 2.** Outside the floor; "the handler holds no state" is correct. **But the blindness is wider than the wording.** One session per cell gives every cell exactly ONE wide write. So *any* stateful decline also scores 13/13, for example "service only the first len > 8 write in this process". Name the stateful class, not just chunk position.
- **(v) The READ direction.** Warranted; I checked the producers. PROM PUTS reads 1 byte with `NO_EXCEPTIONS` (palcode.c:114-115), so it never even reaches a `DM_DEFAULT` handler. An Alpha instruction fetch is `sizeof(ib)` = 4 (cpu_alpha_instr.c:812), the single-step disassembly read is 4, LDQ is 8, and `load_64bit_word` is 8. `store_buf` only writes.
- **(vi) Non-lane bytes (`lcawidefold`).** Outside the floor: the write body reads only `data[ofs]`.
- **(vii) A zero byte is never forwarded.** This is **stronger than disclosed: it is unreachable, i.e. EQUIVALENT for every guest input.**
  - The last wide chunk ends at or before `len = strlen+1`.
  - So the NUL sits at chunk offset ≥ C-1 ≥ 15, while the forwarded byte sits at chunk offset ≤ 3.
  - `argv` strings contain no NUL.
- **(viii) Forward COUNT.** This **over-discloses.** A duplicate of the lane byte, a forward that precedes it, or a forward to an unobserved port is invisible. But an added forward to the SAME port AFTER the lane byte is visible, because the latch keeps the last write. A full-fold variant, forwarding all 16 bytes, would leave `s[15]` = `'P'` in every register and red all four rows. Say so, so that nobody later assumes a full fold escapes.

**Missing disclosures:**
- **(ix) MSR bit blindness at lane 2.** `l2w16` observes only bits 0-3 and 6. A lane-2 value edit confined to mask `0xb0` is invisible: `'C' | 0x10` = `'S'` reads 0xf3 = want. This is value-debt by the parent's own ruled class ("the write body tests no bit of the value"), not a floor cell, but this file claims per-lane coverage and should say which bits lane 2 sees.
  - MSR is the right choice: I checked the alternatives. LPT control (0x37a) is write-only in the model (the read returns 0), and a STROBE prints to the console. FCR/IIR at 0x2fa exposes 2 bits. There is no 8259, PIT, pckbc or pccmos latch at lane 2.
- **The contract's "any variant that DECLINES, REFUSES or MISROUTES"** should be qualified to "any variant keyed only on the body's inputs (len, writeflag, the lane)". Keys the body never reads (CPU mode, pc, time) are an unlisted clause-(e) class. Mode-keyed declines are in fact unreachable: 0x3fffffe is privileged and halts from user mode (palcode.c:183-191).

**Claims not backed by a measured red** (derived, not measured; not a coverage gap, but label them):
- "`== L` for any lane L" is measured only at L = 3 (vc). The L = 0, 1, 2 forms are derived from each lane row's measured red-capability (vc_neL).
- **Address** misroutes, such as a len > 8-gated `relative_addr ^ 1`, are not measured. Only the byte misroute (vf) is. They red by construction on the same preset-kept channel as M2_len8 and KILLLEN8. At lane 1, `^ 1` hits 8259 port 0x20, where `0x42` is an "unimplemented command" that sets `cpu->running = 0` (dev_8259.c:137-140). That still reds.

---

## Q3 -- THE HARNESS FIXES

**Both are right as written.**
- **Retry only if alive:** `if alive and any(printed(...) is None ...)`. A death during any `rd()` window returns EIO on the pty master, `rd` returns False, and `alive` = False with no retry. `alive` can only go True → False, never back.
- **Exit status:** `sys.exit(0 if ok == len(rows) else 1)`. An uncaught assertion also exits 1, without a DONE line.

**I found no path on which a host death scores as a pass:**
- A death before or during GETENV leaves the post-GETENV `print` missing. `printed()` returns None, which never equals an int want, so the row is red. The `alive` row is also red.
- A CPU halt without process exit leaves T4 at its reset value 0. Every want (0x44, 0x41, 0x42, 0xf3) is nonzero, so the row is red.
- The theoretical hole is a death that does NOT close the pty, via a slave fd held by a forked child. It does not arise in these cells:
  - `-x` forks xterms only when OUTPUT is sent (console.c:51), and no cell writes a THR.
  - gxemul installs no SIGHUP handler (grep: only SIGINT, SIGCONT, SIGALRM and SIGPIPE), so the new `os.waitpid(pid, 0)` cannot hang. Closing the master SIGHUPs the session leader.

**Two hardening notes, neither blocking:**
- **(a) The new `os.waitpid` status is collected and DISCARDED.** Recording it would make death detection independent of pty timing. A non-zero exit, or a signal other than the SIGHUP that follows the probe's own close, means died. That would also close the one residual: an intermittent death that went undetected and then passed on retry.
- **(b) The retry still turns an intermittent HANG into a pass.** That is the accepted price of the load-flake retry, and the same as the parent's `dsession()`.

---

## Q4 -- THE PARENT'S L4

**The correction is accurate and does not overclaim in either direction.** I checked each clause:
- "true of the two variants named above": M2 and KILLLEN8 were caught by the first version.
- "that file's first version rowed ONE of the four byte lanes": lane 3, port 0x2ff.
- "a variant servicing wide writes at lane 3 only swept it 3/3": RESULTS.txt `frozen × vc = 3/3 0x44`.
- "#538 rows all four lanes at C=16, k=0": true.
- The contract "cites p_port10 and lcaisasize by name": it does, in (ii) and (iii).
- "RULED AT #530's PASS 2": 3c41f01's message settles "three sentences ... are wrong records" at pass 2, so the provenance holds.

It deliberately stops short of calling the class COVERED. It hands the "what is not caught" list to the child's contract, which is the right direction.

**Its siblings were not updated:**
- **`lca_isalane_probe.py:164-169`, unchanged, is now stale present tense.** It says "It drives ... a PROM GETENV ... whose a2 is the ns16550 SCR -- so store_buf issues ONE 16-byte memory_rw", with "base 3/3 ... 2/3". Those are the FIRST version's shape and scores; the file now drives four cells for 13/13, with M2 and KILLLEN8 at 9/13. Mark them "first version" or restate them.
- **:179** "`lcawidefold` (only s[3] of a 16-byte store reaches the port)" is lane-3-specific. The class statement is "only s[P & 3]".
- A small precision gap: the correction names only vc. RESULTS shows the first version was swept by SEVEN variants (va, vb, vc, ve, vg, vt1, vt2). vc was the only floor breach, and the child's HISTORY says "seven", so this is fine, if terse.

---

## FOUND SOMETHING ELSE

1. **The `l2w16 live` row is not a round-trip control. This is an L4 in the note and in PRETABLE's CHANNEL line.**
   - The MSR's reset value is 0, and every access ORs 0xb0. So the preset 0x00 reads 0xb0 whether or not the preset write landed. The row proves only the read path and the device signature.
   - The other three presets do differ from their register's reset value: SCR 0, MCR 0, and IMR 0 (the 8259 is `memset`).
   - Fix: preset 0x01 (reads 0xb1; still ≠ 0xf3).
2. **Fresh-clone false red.** The probe never creates `alpha_dummy.bin` (line 68). The file is **untracked** (`git ls-files` is empty) and is created only as a side effect of other probes, for example the parent at `lca_isalane_probe.py:369-372`. Run first or alone on a fresh clone, the emulator fails to load it and every row reds. This is the safe direction, but a phantom red. Copy the parent's three lines.
3. **The width pin replays the probe's own model of `store_buf`, not the emulator's.** If `memory.c`'s chunk ladder ever changed, the replay would still say `[16]`, the base would stay 13/13, and the detector would silently stop testing len > 8. The measured pin is KILLLEN8's `failed` line at `00005fe0`, true of this binary. Cheap guard: a source presence pin on `size_t psize = 1024;` and `psize >>= 2;`, using `mk538`'s exact-once idiom.
4. **Durable receipts.** The brief asserts that "every [variant binary] differs from base" and that the clone was restored. `closure538_20260918/` carries no binary hashes and no restore `cmp` record, only make logs. The 13/13 escape and equivalent legs (va, vb, vg, vt1, vt2, vd, vh) rest on "binary differs". Each build log does show a `dev_lca.c` recompile, but copy the `bins.md5` equivalent into `logs/`, as `opus_p2_20260918/logs/bins.md5` does.
5. **#540 does not disturb this table.** Every session runs at ptbr == 0 in kernel mode, where the identity translation equals `PHYSICAL` (my #540 pass 1). So the uncommitted `| PHYSICAL` tokens cannot move any of these 17 scores, whichever round commits first.

---

## RECOMMENDED EDITS (none blocks closure)

1. Change the `l2w16` preset to 0x01, or change the `live` note and PRETABLE's CHANNEL line.
2. Contract wording:
   - (ii): port bits above the lane.
   - (iv): any stateful decline.
   - (vii): equivalent/unreachable.
   - (viii): an added forward after the lane byte is visible.
   - Add (ix): MSR's blind bits `0xb0`.
   - Qualify "any variant" to the body's inputs.
   - Label `== L` for L ≠ 3, and address misroutes, as derived.
3. Parent header: update :164-169 (first-version present tense) and :179 (`s[3]`).
4. Create `alpha_dummy.bin` in the probe.
5. Record the `waitpid` status.
6. Add a source presence pin for the `store_buf` ladder.
7. Add binary hashes and the restore `cmp` to the durable artifacts.
