OPUS549P2_ALIVE
VERDICT: SHIP WITH CHANGES

I found no floor breach, and the fix and the gate block behave as claimed. The changes I ask for are two cheap rows in the probe's refusal session, plus corrections to the contract wording and the kill-table citation. The details are below.

**1. The committed detector against `build/gxemul` scores 41/41 — measured.**
- **Freshness:** the binary's md5 is 4cc158f6, matching the brief. Its mtime (11:10:44) is newer than `build/src/devices/dev_fbctrl.c` (11:10:14), and that source is `cmp`-equal to the working tree.
- **Result:** `FBCTRLP_CONTROL=OK`, `FBCTRLP_RESULT=41/41`, `FBCTRLP_DONE`, exit status 0.
- **My own build:** built from the working tree in my /tmp clone, it also scores 41/41.

**2. 14 new variants outside the table's 25 — measured.** Each was built in a WSL /tmp clone and scored with the committed probe.

Red (caught):
- The PORT read masked to 3 (`N_rdmask3`, 26/41).
- The PORT read OR'd with the latch (`N_rdlatch`, 31/41).
- The command dispatched on port 1, or also run on a DATA read (`N_cmdport` and `N_cmdread`, 40/41). Only the SIGNATURE control catches them, so CONTROL fails.
- The latch cleared by an accepted selector (`N_rearm`, 40/41). Session P's re-select before each refusal is what catches this one.

Equivalent (41/41, no behaviour difference on reachable states):
- The accepted selector stored as `(uint32_t)` (`N_acc32`).
- The PORT read masked to 7 (`N_rdmask7`).
- The latch field moved ahead of `port[]` (`N_order`). This changes only where an index of 8 would land, which matters only if the DATA check is deleted, and that is already disclosed.

**41/41 but with real behaviour changes:**
- **`N_datarearm`** — the latch is cleared by any DATA write. Alternating a DATA write with a refused PORT write then announces every time, which defeats the once-per-device claim. P never writes DATA between refusals, so nothing sees it.
- **`N_clobcell`** — the refused value is stored into `port[idata & 7]`: a refused `sw 9` silently changes port 1's cell. Session K checks only port 5's cell.
- **`N_clobcmd`** — the same, into COMMAND's cell (it reads back through DATA at PORT=0).
- **`N_runcmd`** — the refusal branch runs `fbctrl_command()`. A refused selector write then exits the process whenever COMMAND holds a command other than 0–2.

**Grade: FILE, not a breach.** Each of these adds a store, a clear or a call at a site the fix does not guard. They are outside the enumeration of the fix's own predicate, store and latch, which table 2 covers completely. The contract's "the store reached for an out-of-range value" reads as covering `N_clobcell`, so the wording should say "the selector store".

Two cheap rows would close all four, at no new oracle:
- **In P, write DATA between two refusals** and require the `(once)` count to stay 1. That catches `N_datarearm`.
- **After the refusals, read back every port's DATA cell.** First run GET_RESOLUTION once, then set X1=123 and require it still reads 123 after a refusal. That catches `N_clobcell`, `N_clobcmd` and `N_runcmd`.

Also outside #549's scope: narrowing the DATA path to 8 or 16 bits (`N_datawr8`, `N_datard16`) scores 41/41, because every round-trip value is below 0x100. The unit that takes the resolution/command arms should use values above 0xFFFF.

**3. The gate-16 block against malformed probe logs — measured.** I ran the extracted block (lines 53–74 of the working `gate_mips_folds.sh`) with the real `lib.sh` and a fake probe printing each fixture.

| fixture | result |
|---|---|
| good log | PASS (6 checks) |
| empty (missing) log | FAIL |
| whole log duplicated | FAIL |
| truncated before `FBCTRLP_DONE` | FAIL |
| truncated mid-rows | FAIL |
| `RESULT` line removed | FAIL |
| `CONTROL` line removed | FAIL |
| `DONE` duplicated | FAIL |
| `RESULT` duplicated | FAIL |
| `RESULT` with a trailing space | FAIL |
| one row flipped to FAIL, `RESULT` intact | FAIL (the rows-failed count) |

Every malformed log fails. The one synthetic fixture that passes is a row line deleted with `RESULT=41/41` left intact. The real probe cannot produce that log, because it computes `RESULT` from the rows it printed (probe lines 360–361), so the pinned 41 would catch a deleted row.

**4. The "probe exit status" row can fail only if Python crashes — measured.** Run against a nonexistent binary, the probe printed `CONTROL=FAILED`, `RESULT=5/41` and exited **0**. So that row never fires on a probe-level failure (the controls and count rows do). Either make the probe exit nonzero when it is not 41/41 with controls OK, or describe the row as the crash check it is.

In the same run, five rows passed with no emulator at all: the four "disassembly mismatches = 0" rows and "no `(once)` line". They are zero-count rows that pass by construction when nothing runs. They are guarded by the step-survival rows and CONTROL, so this is not a gap, but they are not evidence on their own.

**5. Stale records — read.** The gate block's comment and the probe's CONTRACT both cite "kill table 1: 20 of 20". The brief's evidence is table 2: 25 variants, 22 of 22 red, `M_revert` 25/41, two disclosed escapes. Table 1 was run on the instrument whose per-row credit was later corrected. Cite table 2 (`table2/TABLE.out`) in both places before commit.

**6. Everything else checked out — read.**
- The diff matches the brief's inlined hunks.
- The DATA tripwire comment is accurate.
- The contract's NOT CLAIMED list (the process-global latch, the deleted DATA check, the command and offset defaults) matches what was measured.

**State.** I used a fresh WSL /tmp clone only. The clone-local `.MUTANT` sentinel was cleared after a `cmp`-equal restore and a rebuild matching the base md5. All /tmp material is removed, no emulator processes remain, and the repo is untouched outside `opus549_measured/p2/`.

Logs are in `GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/p2/`:
- `TABLE_new.out` and `probe_N_*.out` (the variant table and per-variant logs)
- `variants.diff`
- `gate16_fixtures.out` and `gate16_fixtures/` (the malformed-log fixtures)
- `gate16_block_extracted.sh`
- `probe_build_gxemul.out`, `probe_missing_binary.out`
- `INPUTS.md5`

---
*Recorded by the main loop on 2026-09-25 -- RECOVERED from the agent transcript: agent a86286fc69054c85b (resumed from its pass-1 run), final text by claude-opus-5-5 at 2026-09-24T16:45:07.611Z.  This pass-2 answer was never written to the artifacts when it landed; found while building #549's ledger records.  Badge s.*
