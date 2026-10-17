# ADJUDICATION PACKET D -- the agy pack's second readings (grok + Argon), pre-screened

Prepared 2026-10-16 ~12:3x CDT by the main loop (Opus 5.5, session 087a90).  Owner directive of 2026-10-16:
**"Adjudicate any pending findings with both the Fable, Astra, and Grok."**  Three adjudicators answer independently:
Fable 5.1 (Agent seat), GPT-6 Astra (codex, ultra), Grok 4.7 (xhigh, plan mode).  Ordinary emulator correctness, test
coverage and records review.  **READ-ONLY: write nothing to any project tree.**

## 0. What this packet is

The 2026-10-13 "agy pack" (59 read-only briefs under `GXEMUL-SEC/regress/artifacts/agypack_20261013/briefs/`) was
answered by agy (harvested in `agypack_20261013/HARVEST.md`), then by grok (`agypack_20261013/<id>/grok_<id>.txt`, 46 +
30 reconcile runs + 11 premise audits) and by Gemini 4 Argon (`_scratchpad/gweb/jobs_20261014_argonpack6/<id>/
gemini_web.out`, 38 of 46 banked; the rest queued).  Nobody had ruled on the grok and Argon readings.  Five Opus 5.5
pre-screen agents (agent_models.py: all clean claude-opus-5-5) classified every grok/Argon finding DISPOSED / LIVE (or
CONFIRMED) / REFUTED / CANNOT SETTLE against HEAD e483d931, each citing what it opened.  Their files ARE the evidence for
this packet:

| file (`GXEMUL-SEC/regress/artifacts/adj_20261016/prescreen/`) | jobs | findings | LIVE / CONFIRMED | refuted | cannot settle |
|---|---|---|---|---|---|
| `prescreen_563.md` | 9 (#563 chain) | 166 | 15 (14 distinct; none a floor row) | 28 | 0 |
| `prescreen_asic.md` | 7 (asiceventaddr) | 147 | 14 (10 distinct) | 25 | 2 |
| `prescreen_records.md` | 16 (records + harness) | 227 | 93 | 39 | 2 |
| `prescreen_prep.md` | 14 (future-round prep) | 239 | 194 (12 FILE / 8 add-to-row / 46 record / 111 premise ...) | 35 | 2 (+3 sub) |
| `prescreen_audits5.md` | 11 (grok premise audits) | 219 | 125 (3 FILE / 61 record / 61 premise) | 46 | 5 |

Caveats you must weigh: the pre-screens are OPUS answers; three of them fanned out to read-only sub-forks and
spot-checked them; every row carries READ or REASONED.  They read the WORKING tree in places -- cite HEAD.  Two later grok
reconcile runs swap agy and grok labels (`prescreen_563.md` and `prescreen_asic.md` say which).  Packets A, B and C
(already adjudicated by all three of you) covered the formal #563 / asiceventaddr / records findings; this packet is
everything else.

Ground rules as before: repo `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD **e483d931**
(`git show e483d931:<path>`); the working tree carries two sessions' uncommitted edits; never read the project root's
pristine 2021 `src/`.  Separate READ / REASONED / MEASURED.  Count arguments, not seats.

## 1. URGENT -- `wiringcliff` (already ruled in packet C; repeated because it blocks every action below)

`tools/pipeline/check_probe_wiring.py` exempts `ip30_abort_probe.py` until `2026-10-15` (HEAD :3097, working tree
:3112); the test is `elif d < today:` and precommit section R runs it without `--today`, so from 2026-10-16 every commit
in either session is refused.  Next expiries 10-22 (two), 10-23, 10-26, 10-27.  Found independently by Fable (packet C),
`prescreen_records.md` PW6 and `prescreen_audits5.md` records_three/F5.  **MINE: resolve before any commit -- re-date
each expiring exemption individually with its reason (the owner's 2026-09-24 precedent for the 09-28 cliff) or wire the
probe.**

## 2. NEW ROWS -- MY DISPOSITIONS (the three HIGH ones I verified myself by reading HEAD)

**H1 `ofemulnodata` -- FILE, HIGH (verified).**  `src/promemul/of.c:1096-1101`: `of_emul()` calls `exit(1)` when
`machine->md.of_data == NULL`, and only `machine_macppc.c:99` (via `of_emul_init`, of.c:1078) sets it.  The magic
instructions are decoded unconditionally: ARM SWI `0xef8c64be` (`cpu_arm_instr.c:5034-5036` -> `X(openfirmware)`
:988-991 calls `of_emul`) and PowerPC `sc` `0x44ee0002` (`cpu_ppc_instr.c:4400-4402` -> `X(openfirmware)` :3956-3958).
So one guest instruction, user mode included, ends the host on every ARM machine and every PowerPC machine without
OpenFirmware emulation.  No row covers it (`ofopenexit` and `ofpeerexit` are other sites).  Source: `prescreen_audits5.md`
of_two/F9.

**H2 `mipssyscallprom` -- FILE, HIGH (verified).**  `cpu_mips_instr.c:4650-4657` routes `syscall` with code `0x30378`
at ANY address to `X(promemul)`, whose `default:` arm (`:2649-2650`) is `fatal(...); exit(1);` for every machine type
other than PMAX/PS2/ARC/SGI/EVBMIPS (testmips, cobalt, hpcmips, algor ...).  `#235` closed exactly this for `break
0x30378` with an address gate (`:4659-4669`); `syscall` was never gated.  No row covers it (`mipsresetalias`, ledger
:57833, is the BREAK gate's own alias defect).  Source: `prescreen_prep.md` mips_two/F10.

**H3 `asccmdwidecount` -- FILE, HIGH (verified), cross-linked to `ascwidecount`.**  `dev_asc.c:154` declares `uint32_t
reg_wo[0x10]` and `:1155` stores the guest's whole `idata`; the COMMAND-phase DMA path computes `len = reg_wo[NCR_TCL] +
reg_wo[NCR_TCM] * 256` as an `int` (`:987`) and passes it to `scsi_transfer_allocbuf` (`:991-992`), whose `size_t`
request fails and takes the out-of-memory `exit(1)` (`diskimage_scsicmd.c:151-155`).  The open HIGH row `ascwidecount`
(ledger :57458) is the DATA_OUT sibling (`len2`, :577, a memcpy) -- same register, different consequence; one fix design
(mask or bound the count) may cover both, so they are candidates for ONE round under the reopening rule.  Source:
`prescreen_prep.md` ascwidecount/F6.

**Other new rows** (`prescreen_prep.md` §A, `prescreen_audits5.md` FILE, `prescreen_563.md`, `prescreen_asic.md`) --
**MINE: FILE each as the pre-screen proposes, severity as stated, unless you refute it:** MIPS `X(ei_or_di)` skips
`cop0_availability_check` (MED); `armcp15c1fallthrough` (MED); ARM TTB/L2 address mask `0x0fffffff` (armdesc3kill F17);
coarse domain fault raised before the L2 fetch (LOW); Thumb LDR(3) raises Prefetch Abort, not Data Abort; coarse-L2 type-3
entry treated as a 1 KB tiny page (N2); MB89352 diagnostic with three conversions for two arguments (N1, LOW);
DEC21143 unbudgeted RX drain under TAP input (audits5 net_three/F8 -- FILE or fold into `ne2krxbudget`); the BE case-4
byte-lane shift "Filed" with no row (#563 pre-screen item 9 -- FILE); `pvr` F15 FOLD into `gdromcondhow`.  The two
harness-builder faults are ONE row each: `mk_briefs4.py:17` reads `severity` where the ledger says `sev` (every brief shows
"(?, open)"), and #554's GOVERNING TEXT windows (`mk_filing.py.txt:83,187`) start 60 characters before the row's own id
and cut at 400 (117 of 221 rows misaligned per `prescreen_prep.md` ppc_six/F7).

## 3. FIX SPECS THAT NEVER GOT A RULING (`prescreen_records.md` §3)

`agentrefusal` (AR1-AR6), `asanexit1subtype` (AR10), `batterymissedruns` (AR13, AR15-AR17), `harness_five` (HF1-HF4,
HF7-HF9), `probewiring` (PW1-PW3, PW5).  The pre-screen confirmed concrete defects in the drafts (a RED control that cannot
redden under root; a word token that aborts `$(( ))` under `set -u`; nothing invokes `nightly_check.sh`, and every
verdict since 08-30 is dirty, so a FAIL-keyed caller would be permanently red; grok's hook drops the SessionStart JSON;
Argon's heredoc diff does not compile ...).  **MINE: NONE IS READY TO BUILD AS DRAFTED.  Each row stays open with the
confirmed defects attached as the next draft's premises; no draft is adopted here.**  Rule: is any of the five READY
with named fixes?

## 4. RECORD CORRECTIONS (~290 across the five files)

**MINE: ADOPT every pre-screen-CONFIRMED record correction as written, to land in records commits grouped by file**
(carrier citations CC1-CC16 -- CC16 is a `src/cpus/cpu_sh.c` comment and owes four-tree propagation plus the two-part
clearance; decayed counts CN*; the PDF inventory CN13-CN16/CD22 -- 20 PDFs on disk, the carrier lists 19 and says
fifteen, `ata2` cited by `dev_wdc.c:640` is missing; batch-8n records BN*; the pcc2 ruling record PC* -- PC2 is a LIVE
held marker never defanged; harness text; the clause-(c) census NC*; every `prescreen_audits5.md` RC row; every
`prescreen_prep.md` §C row; `prescreen_563.md` items 1-6 and 10-14; `prescreen_asic.md` items 2-9).  `prescreen_asic.md`
item 10 (the stub's `struct cpu` puts `mem` first; the product's starts with `machine`) goes into packet B's fixture
table as a disclosure.  **Spot-check: open at least FIVE corrections in each file and say whether each holds.**

## 5. BRIEF PREMISES (~180)

**MINE: ADOPT as premises of the round that takes each row; record them by pointer in each row's note (the next records
commit adds `premises: adj_20261016/prescreen/prescreen_<x>.md <job>/F<n>`).**  No action now beyond the pointer.

## 6. CANNOT SETTLE -- three settled by MY measurement today

`adj_20261016/meas_main/libcq.c` + `libcq.out` (WSL Gentoo, gcc 15.2.1, glibc 2.42, x86-64): `malloc(0)` -> non-NULL;
`realloc(p, 0)` -> NULL with errno 0 (the block is freed); `fseek(f, -8, SEEK_SET)` and `fseeko(f, -1, SEEK_SET)` -> -1,
EINVAL, position unchanged.  Consequences for the rows: arcbios F9 / `arczeroalloc` / `dectxzero` -- on the build host
`malloc(0)` does not return NULL, so a NULL-means-OOM exit after `malloc(0)` is not reached HERE (portability exposure
only; C99 permits NULL); net_three F16 -- a `realloc(p, 0)` whose NULL result is treated as out-of-memory IS reached on
this host (check the cited site's handling); loaders_four F7 -- a negative `fseek` fails cleanly with EINVAL (the
consequence depends on whether the loader checks the return).  The rest stay CANNOT SETTLE (a macppc NetBSD boot; a
sweep from a clean checkout; a 32-bit libc; a backtrace rerun; the vector-unmapped rerun).

## 7. The owner's questions

The records pre-screen's CD5-CD8 (D2 wording: "`< 97`" is derived not measured; §C7's `> B-1` is the equivalent
mutant at a clamp; "every one-token move" overclaims; the 32769/32767 rows came from the 137-row extension) and CD10/CD13
(ROUTE PARITY's row-kind wording contradicts itself; the two recorded route bounds differ) are inputs to the OWNER's
open questions.  **MINE: forwarded to the owner; not ruled here.**

## 8. QUESTIONS (VERDICT LINE FIRST)

Open with your seat token and ONE verbatim line from `GXEMUL-SEC/regress/artifacts/adj_20261016/meas_main/libcq.out`.

`VERDICT: UPHOLD ALL / UPHOLD WITH CHANGES (<n> rulings changed) / OVERTURN (<the load-bearing ruling>) -- <one line>`

1. Rule H1, H2, H3 individually (FILE? severity? fold?), opening the cited lines yourself.  Then the "other new rows"
   list: UPHOLD / REJECT per item, one line each.
2. §3: is any fix spec READY?
3. **WHICH OF MY CLASS ADOPTIONS IS WRONG?**  §4 and §5 adopt ~470 pre-screen rows wholesale -- the most suspicious
   disposition in all four packets.  Spot-check at least five rows per pre-screen file (twenty-five in all), name each
   row you checked and whether it holds, and name any row whose REFUTED/DISPOSED grade you think is wrong.
4. **WHAT DID THE PRE-SCREENS MISS?**  In particular: any other guest-reachable host exit their readers walked past.
5. Is §6's reading of my measurement right for each of the three rows?

Seat-specific:
- **Grok**: most findings here are YOUR earlier runs' -- self-review; be harder on the ones the pre-screens CONFIRMED.
- **Astra**: you cannot run code; say where a claim needs a run.
- **Fable**: H1-H3 are new HIGH host-exit rows; check that each is really unfixed at HEAD and not already declined by an
  earlier round under another id.
