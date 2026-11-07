# Reading task: oldrec567 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC567-284e` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #567 fbctrlcmdkill (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 2905-2978 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 2905| # `#567` (fbctrlcmdkill): the test machines' framebuffer controller ended the emulator on any command but NOP, SET_RESOLUTION and GET_RESOLUTION, and ran a WIDE value as its low word -- every other 64-bit value at COMMAND is refused before the store now, COMMAND kept, one announce per device; with a 125-row rung-3 detector, gated in gate 16; held for Fable
 2906| 
 2907| **The defect** (filed by `#549`'s review, `fbctrlcmdkill`, HIGH).  `fbctrl_command()`'s `default:` called `fatal()`
 2908| then `exit(1)` for every command other than NOP (0), SET_RESOLUTION (1) and GET_RESOLUTION (2) -- FILL (3) and COPY (4)
 2909| included, which `dev_fb.h` names under a bare `TODO:` with no port semantics.  A guest reaches it with ONE DATA write
 2910| while COMMAND (port 0, the power-on selector) is selected, on every test machine (`machine_test.c` installs
 2911| `fbctrl addr=0x12f00000`).  And `d->port[]` is `int`, so a wide `sd` was stored as its low word and DISPATCHED:
 2912| `0x100000003` ended the emulator as FILL, and `0x100000001` silently ran SET_RESOLUTION.  Witness, rung 3 on an
 2913| unmodified `-E testmips` with HEAD's binary: 2/12 -- 3, 4, 5, -1 and `sd 0x100000003` each exit 1
 2914| (`regress/artifacts/fbctrlcmdkill/pass1_20261018/WITNESS_headbin.out`); 12/12 on the fix
 2915| (`draft_20261018/WITNESS_postfix.out`).
 2916| 
 2917| **What ships.**
 2918| * `src/devices/dev_fbctrl.c` -- the DATA arm refuses, BEFORE the store, any write at COMMAND whose full 64-bit value is
 2919|   above GET_RESOLUTION: COMMAND keeps its previous value, nothing executes, and a new `warned_cmd` latch prints one
 2920|   `[ fbctrl: command 0x... is not supported; the command port is unchanged (once) ]` per device.  `fbctrl_command()`'s
 2921|   `default:` stays, unreachable, as a tripwire (as `#549` kept the selector's).  `est/` byte-identical; `build/`,
 2922|   `build-asan/` and `/tmp/gxsec-build` rebuilt and cleared both parts.
 2923| * `regress/fbctrl_cmd_probe.py` (new, 125 rows, 27 sessions on an unmodified `-E testmips`) -- eleven refusal classes
 2924|   (3, 4, 5 and `0xffffffff` by `sw`; 3 by `sb`, 4 by `sh`; `0x100000003`, the three wide aliases of accepted commands
 2925|   and all-ones by `sd`) on a device seeded with COMMAND = 2, X1 = 123, Y1 = 77; the bound's two edges -- 2 accepted with
 2926|   an observable dispatch, 3 refused -- at every access width, with the latch clear and set; reads and non-COMMAND stores
 2927|   at every width; the latch across an accept and a read; the selector's latch apart from it in both orders; one
 2928|   free-running session for the announce level.  Its CONTRACT is its header -- the floor, the width cells held, the
 2929|   effects, and NOT CLAIMED (0)-(7), (7) being the observation cells pass 3 named and the owner filed as debt.
 2930| * `regress/gate_mips_folds.sh` (gate 16) -- the probe's block beside `#549`'s, before the pmax-kernel check: parse
 2931|   before score; CONTROL `OK`; exit 0; the score pinned by EQUALITY at 125; rows emitted, green rows and unique names
 2932|   reconciled with one anchored pattern (this probe prints a row's status after got/want); and EVERY expected row checked
 2933|   by name, green exactly once.
 2934| * `regress/gate_hygiene.sh` -- `EXPECT_PTY_PROBES` 75 -> 76 and `EXPECT_CONVERTED` 25 -> 26 for this probe (`#564`'s own
 2935|   stranded pin landed alone, in the commit before this one).
 2936| * `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 35 -> 36 (`fbctrl_cmd rows run ... 125`).
 2937| * `tools/pipeline/check_probe_wiring.py` -- the probe's MANIFEST line.
 2938| * `tools/pipeline/ledger.json` -- `fbctrlcmdkill` HELD for fable5 (Fable walled on every pass; a row may not close while
 2939|   a stage awaits a seat); FILES `fbctrlobsgrid` (MED: pass 3's observation cells), `fbctrlvec128` (LOW: a 16-byte vector
 2940|   store is taken as its low 64 bits, at DATA and at `#549`'s PORT) and `gate16fence` (LOW: gate 16 launches both device
 2941|   probes unfenced); `gatedevicesplit` gains the gate-16 stop -- a third device probe lands there only with the split or
 2942|   with a pin on the launch count.
 2943| 
 2944| **Measured** (`regress/artifacts/fbctrlcmdkill/`; every table's predictions written first, in a `PRETABLE*` file whose
 2945| mtime is the order proof).
 2946| * The draft (`draft_20261018/`): PRE-FIX 36/95 on HEAD's binary -- exactly the PRETABLE's prediction -- and 95/95 on
 2947|   the fix.
 2948| * Kill tables 1 and 1b (`killtable1_20261018/`, `killtable1b_20261018/`): sixteen mutants on the 95-row v1, all red;
 2949|   clause (b) `B_gateoff` (the arm as HEAD has it) row for row the pre-fix leg; clause (c) measured -- an absent and a
 2950|   non-emulator binary each CONTROL=FAILED.
 2951| * Pass 2's mutants, measured BEFORE any repair (table 2a): three passed v1 whole; probe v2 (99 rows) closed them and
 2952|   table 2 re-ran all 25: every one red.  F2's, measured before any repair (table 3a): seven passed v2 whole; probe v3
 2953|   (106 rows) closed them and table 3 re-ran all 32: every one red, every prediction held.
 2954| * Two consecutive passes had found one class open -- access WIDTH -- so v4 (123 rows) was built from an enumeration
 2955|   written before it ran (`killtable4_20261019/PRETABLE_ADDENDUM_t4.out`).  **Table 4** (06:30-07:03): the twelve
 2956|   newest mutants passed the 106-row v3 whole, and on v4 all 44 are red; legs 123/123 on the fix and 51/123 on HEAD's
 2957|   binary; both null media CONTROL=FAILED; every prediction held row for row (`KILLTABLE4_VS_PRETABLE.out`).
 2958| * Pass 3 found the v4 enumeration counted cells REACHED, not every effect OBSERVED; by the owner's ruling two rows were
 2959|   added from values R:edges already collected (`edge x1`, `edge y1`), and plain regression runs measured the 125-row
 2960|   probe: the fix 125/125, HEAD's build 51/125, both null media 17/125 with CONTROL=FAILED (`killtable4_20261019/legs41/`).
 2961| * Gate 16 run IN SITU (`wiring_20261019/INSITU.md`): on the default binary PASS, 161 checks; on HEAD's binary FAIL, 77 of
 2962|   161, every red check this block's.  The v4 block replayed on all 48 table-4 logs and five broken logs was green only
 2963|   on the fix (`GATE16_REPLAY_v4.out`).
 2964| * The weekly battery of 2026-10-18 (re-run at 23:19 after Modern Standby killed the 18:00 run) passed 16/16 with
 2965|   `#567`'s first, 95-row block in gate 16; the block that ships is the 125-row one, run in situ above.
 2966| 
 2967| **Panel.**  Pass 1 (`pass1_20261018/`): GPT-6 Astra, Grok 4.7 and GLM 5.3 chose member 3 (decline + latched announce),
 2968| the full 64-bit compare and a new gated probe; `fbctrloffkill` stays its own row (2-1).  Pass 2 (`pass2_20261018/`): all
 2969| three SHIP WITH CHANGES.  F2 (`pass2_20261018/f2/F2_DISPOSITIONS.md`): all three SHIP WITH CHANGES, converging on width x
 2970| bound edge and the latch's persistence.  Records corrected on the way, each a seat's catch: NOT CLAIMED (6) put the
 2971| 16-byte loss in the wrong place (Astra, Grok); testppc's install is `machine_test.c`'s line 154, not 337 (Astra, Grok);
 2972| E8 sets the latch on an accept (GLM); GET_RESOLUTION makes four X1/Y1 assignments (Astra, Grok); v2's bound edges were
 2973| held at `sb` and `sw`.  Pass 3 (`pass3_20261019/F3_DISPOSITIONS.md`): GPT-6 Astra, GLM 5.3 and Grok 4.7 all SHIP WITH CHANGES -- the width enumeration counted cells reached, not every effect observed; by the owner's ruling two rows were added (`edge x1`, `edge y1`), the remaining cells filed as `fbctrlobsgrid`, and the records corrected (the gate comment, the probe's width list and NOT CLAIMED (2), (5) and (7)).  Confirm (GPT-6 Astra, `confirmB_20261019/`): COMMIT WITH CHANGES -- the fix, the two-row update, 125 rows and 27 sessions, the 125/51/17 scores and the 44-mutant table checked against the artifacts; taken: the F2 ledger entry's "closed by v3/v4" narrowed to the measured escapes, and the fixed witness's own path cited.  Its other items read the working tree, where this unit's CHANGELOG, bug file, matrix and queue are not yet written (the unit carries them), and its packet's ledger export had failed on an encoding error (the seat read the ledger itself).
 2974| Fable 5.1 walled (HTTP 429) on passes 1, 2, F2 and 3 -- each a seat failure, held with its question, never agreement;
 2975| the row is held for it.  Opus 5.5, agy, kimi, deepseek and minimax deliberately not fired (the owner's 2026-10-17
 2976| roster).  Twice while preparing a fuller pass-3 repair the main loop's own response was stopped by the safety
 2977| classifier; the owner then ruled the landing above.
 2978| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_567: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC567: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
