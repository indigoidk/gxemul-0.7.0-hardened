# `fbctrlcmdkill` (HIGH) -- pass 2 on the real diff: `#567` refuses every framebuffer-controller command but 0-2 before the store

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise its brief's author stated wrongly.  **Check the premises, not
just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`, its WORKING TREE (the diff below is uncommitted).**
Ignore every other `src/` under the project root (pristine 2021 upstream copies).  The working tree also carries
UNRELATED uncommitted edits to other files (`dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`, `cpu_alpha_palcode.c`,
`regress/diff_wdc_identify.c`, `regress/gate_offline.sh` and others) -- they are not this round; ignore them.  Frozen
copies of this round's files are in `regress/artifacts/fbctrlcmdkill/pass2_20261018/frozen/` -- cite those.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from
this packet rather than guessing at it.  **Where this brief states an arithmetic claim -- a value range, a count of rows
-- ENUMERATE it rather than reasoning about it**, and enumerate the right domain: ask what the producer of a value can
actually emit before walking it.

**VERDICT LINE FIRST**, so your answer survives truncation.  READ-ONLY: write nothing to any project tree.

## What this pass reviews -- `git diff --numstat`, each file with its disclosure

```
22   1  src/devices/dev_fbctrl.c               INLINED -- the whole diff, and the post-fix functions in full (section 1)
378  0  regress/fbctrl_cmd_probe.py (NEW)      INLINED IN FULL (section 2)
47   0  regress/gate_mips_folds.sh             INLINED -- the whole added block (section 3)
14   6  regress/gate_hygiene.sh                INLINED -- the whole diff (section 5)
3    1  tools/precommit_check.sh               INLINED (section 5)
1    0  tools/pipeline/check_probe_wiring.py   INLINED (section 5); the working file carries 15 MORE uncommitted lines
                                               from other work -- not this round, not shown, not to be staged
```

`est/src/devices/dev_fbctrl.c` (the non-git twin tree) is byte-identical to SEC's (md5 490b57d8...).  The records
(CHANGELOG block, bug-file entry, ledger) are not written yet; they follow this pass.

## SETTLED PREMISES -- recorded resolutions, re-inlined so nobody spends an answer re-deriving them

* **`fatal()` prints and RETURNS** -- `src/core/debugmsg.c`'s `fatal()` has no early-out and no exit.  Every refusal row
  rests on it (as `#549`'s 117-row detector does).
* **Pass 1 (2026-10-18, `pass1_20261018/ADJUDICATION_p1.md`)**: GPT-6 Astra, Grok 4.7 and GLM 5.3 each chose option
  member 3 -- REFUSE every 64-bit DATA value other than 0, 1 and 2 at COMMAND **before the store**, leave COMMAND
  unchanged, one new `warned_cmd` latch and one `(once)` announce naming the full value, a new gated probe.  FILL (3) and
  COPY (4) have no port semantics anywhere (a `TODO:` over two bare constants), so implementing them is a feature, not a
  fix.  `fbctrloffkill` (the same file's offset `default:`) stays its own row, 2-1.  The Fable seat walled (held).
* **The test-first witness (rung 3, unmodified `-E testmips`, HEAD's binary): 2/12** -- DATA writes of 3, 4, 5, -1 at
  COMMAND, and `sd 0x100000003`, each end the host with exit 1 (`pass1_20261018/WITNESS_headbin.out`); 12/12 on the fix.
* **The house latch idiom** is one latch per device instance and per message, with a `(once)` marker; `#549`'s
  `warned_port` is this device's existing one.
* **Floor clause (c)** is recorded in one of two forms -- `(c): measured at <artifact>` or `(c): by construction via
  <row/pin>, leg not run` -- and the null medium for a runtime probe is an absent or non-emulator binary.
* **Rule D2**: a compare against a constant bound B that a fix depends on is pinned by rows at B+1 (past the bound) and
  B-1 (below it); a far row proves the branch exists and never pins the bound.

## 1. The fix -- the diff, then the post-fix code in full (every exit path and the common tail)

```diff
<<DIFF_DEV>>
```

The post-fix struct, `fbctrl_command()` and `DEVICE_ACCESS(fbctrl)`, verbatim from the frozen copy:

```c
<<FUNCS>>
```

## 2. The detector -- `regress/fbctrl_cmd_probe.py`, in full (its header carries the CONTRACT)

```python
<<PROBE>>
```

Its code is the instrument kill table 1 measured (`killtable1_20261018/probe.frozen.py.txt`) with ONE change:
`send()`'s local `mark` renamed `_mark`, the spelling gate 6's fresh-mark census keys on (`#549` made the same rename).
An AST comparison with only that local renamed is equal; the docstring gained the CONTRACT.

## 3. The gate wiring -- the block added to `regress/gate_mips_folds.sh` (gate 16), before its pmax-kernel check

```bash
<<GATEBLOCK>>
```

**REPLAYED OFFLINE** (`wiring_20261018/GATE16_REPLAY.out`): the block's own lines (minus the probe launch and its `fcrc=0`
initializer) were sourced with a stub `check()` against every kill-table-1 log, each with its recorded exit status:

```
<<REPLAY>>
```

## 4. The measurements

<<LEGS>>

**Kill table 1** (`killtable1_20261018/`, PRETABLE written beforehand at `draft_20261018/PRETABLE.out`, 17:30:58; table
21:34-21:42; the clone restored to the fix, both clearance parts, its sentinel cleared):

```
<<SCORES1>>
```

**Its predictions against those scores** (`killtable1_20261018/KILLTABLE1_VS_PRETABLE.out`, verbatim):

```
<<VS1>>
```

<<TABLE1B>>

<<BATTERY>>

## 5. The census pins, the score manifest and the wiring manifest

Gate 6 (`gate_hygiene.sh`) pins how many pty probes lie in the tree and how many are PROMPTLESS (send without waiting
for the debugger prompt).  Re-deriving them for `#567`'s probe with `tools/derive_hygiene_pins.sh` showed two moves,
not one: the census read 76 against a pin of 74, and the promptless census 44 against 43.  The second probe is
`regress/sgi_mte_decline_probe.py`, committed by `#564` (`e7fc97e6`) THIS MORNING without moving either pin -- so this
week's battery would have reddened gate 6 whatever `#567` did -- and it is PROMPTLESS (fixed waits: a 1.5 s settle,
0.22 s between commands).  `--write` REFUSES while a promptless probe is neither grandfathered nor prompt-detecting, so
`#567` grandfathered it with the tool (`--grandfather sgi_mte_decline_probe.py`, the 2026-09-19 precedent: twenty
promptless probes grandfathered, "converting a probe's readiness is its own round"), then ran `--write`: 76 and 26.
After it, all eight censuses equal their pins.  Two rows are filed beside it: `ptyprobepins` (a precommit check, so a
commit cannot strand the pins again) and `sgimtereadiness` (the conversion).

```diff
<<DIFF_HYG>>
```

```diff
<<DIFF_PRE>>
```

`tools/pipeline/check_probe_wiring.py`, this round's one line (beside `#549`'s entry):

```
    "fbctrl_cmd_probe.py":         (CLASS_DETECTOR, "#567 fbctrl COMMAND refusal"),
```

`check_score_claims.py` now reports `SCORE_CLAIMS_PINNED=36` and passes (the manifest moves 35 -> 36 with it).
