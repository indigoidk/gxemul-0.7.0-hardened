# `vmedefaultkill` (#568) -- THE ADJUDICATION PASS (§F2): every pass-2 finding, my disposition on each, and the disputes -- adjudicate them, and tell me which of my dispositions is wrong

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

This packet consolidates the FIVE pass-2 answers (GPT-6 Astra, Grok 4.7, GLM 5.3, Fable 5.1, and Argon -- Gemini web,
packet-fed) on one change.  **You are now reading the other seats' findings.  Correct them where they are wrong, and be
HARDEST on findings that are your own and on dispositions that adopt your position** -- a ruling in your favour is the
one you are least likely to test.  **I accepted most findings; that is a suspicious ratio, and agreement is not
evidence.**  Where a claim is checkable, check it rather than weigh it.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/` -- its working tree on committed HEAD `1a59a47e`.**
The round's edits are uncommitted there.  Another session's uncommitted edits to `dev_pcc2.c`, `dev_lca.c`, `dev_sh4.c`,
`cpu_alpha_palcode.c` and `mvme_pcctworeg.h` are NOT part of this round.  Three pristine-2021-upstream copies of GXemul
sit under the project root; if your line numbers disagree with mine by hundreds you are reading one of them.

**If you cannot read files that is expected** -- the change (section 5) and every finding are inlined.  Name any premise
you cannot settle from this packet rather than guessing.  **VERDICT LINE FIRST.**

## 1. The round, and what changed since pass 2

`src/devices/dev_vme.c` ended the emulator (`exit(1)`, announced only by a `debug()` that is silent at default verbosity
while free-running) on any VME2 offset its switch did not name.  Owner rulings: the 26 header-named registers the model
does not implement (population 2) DECLINE + ANNOUNCE ONCE; every other unmatched offset (population 1) FAULTS via
`return 0` (memory_rw raises the m88k data-access exception).  The fix is section 5; the 34-row rung-3 detector is
`regress/vme_default_probe.py` (frozen copy md5 `19de15b3`); kill tables 1 and 1b ran 27 legs in a scratch clone
(every leg killed except the two predicted equivalents M_ODATA0 and M_SERVED0; NULL medium 5/34; HEAD 14/34).

**Measured since the pass-2 packet was written (it said the gate block had no run):** the gate-14 block run ALONE reds
on the pre-fix binary (22 of 39 checks) and is green on the fixed one (39/39); the FULL gate 14 on the fixed `build/gxemul`
PASSED, 1264 checks, 0 failed (`regress/artifacts/vmedefaultkill/gate_20261020/`: `mini_PREFIX.out`, `mini_FIX.out`,
`GATE14_FULL.out`).  The two-part clearance holds on `build/`, `build-asan/`, `/tmp/gxsec-build` (source cmp CLEAN,
binary newer) and `est/` (source CLEAN; no binary).  The probe-development files the docstring cites were copied to
`regress/artifacts/vmedefaultkill/probe_20261020/`.  Nothing else has changed: the fix and the probe are as pass 2 read them.

## 2. The findings, numbered, with my disposition on each

{FINDINGS}

## 3. The disagreements -- each side in its own words; adjudicate your own

{DISPUTES}

## 3b. The first adjudication already in

{FABLEF2}

## 4. What is still OWED, and where I may be fooling myself

{OWED}

## 5. The change under review (inlined for the seats that cannot read files)

### 5a. The diff of `src/devices/dev_vme.c`, verbatim

```diff
{DIFF}
```

### 5b. The whole device after the fix, numbered from the working file

```c
{FUNC}
```

### 5c. Every store instruction the probe places, with the register seeds, verbatim from `regress/vme_default_probe.py` (the population-2 stores are lines 655, 675 and 735-746 -- POP2_OFFS is the 26 offsets; the others store to the ten cased offsets or to 0x90+; r2 holds WVAL, r12 NARROW, r10/r11 DHI/DLO)

```
{STORES}
```

## 6. Questions

1. **Adjudicate F1..F{NF} and D1..D{ND}: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE**, one line each with the reason.
   For a finding that is your own, say whether my DISPOSITION and my FIX are right -- not merely whether the finding was.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted {NACC} of {NF} findings outright and refined {NREF}.  Name
   the one you would overturn first.
3. **The planned instrument revision (section 4's REV 3)** adds rows.  For EACH proposed row, name the mutant it is
   meant to kill and the observable that differs under it (the CHANNEL line) -- and say if a row's channel CANNOT vary
   under its mutant (vacuous by construction).  For F1 in particular: is one zero-store first access enough, or does
   the closure need a zero store at more than one width?
4. **WHAT DID ALL OF US MISS?**  You now have every seat's output.

If, while verifying a claim, you found something ELSE -- say so.

## 7. Answer format

Your token on the first line, then ONE line `VERDICT: PROCEED AS DISPOSED | PROCEED WITH CHANGES | DO NOT PROCEED -- <one
line>`, then Q1 as a table (id | ruling | reason), then Q2-Q4.  Facts and flags; no restating the packet.
