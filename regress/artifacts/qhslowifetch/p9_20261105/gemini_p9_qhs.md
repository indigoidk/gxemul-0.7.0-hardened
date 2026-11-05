# Gemini 4 Argon -- job `p9_qhs`, banked 2026-11-05 10:58Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p9_qhs/gemini_web.out (mtime 2026-11-05 04:49:33 local, 3711 bytes)
* sender verdict line: (none)

---

VERDICT: VALID. The test-suite expansion correctly targets the cancellation loophole without modifying emulator product state, though several premises rely on external files.

**Defensive Review of Claims and Code State:**

*   **Product State Preservation:** The claim "The product is UNCHANGED since repair 5" (Section 0) is tested against the provided diffs. Diffs `2a` and `2c` modify only test scripts (`regress/ppc_ifetch_probe.py` and `regress/gate_ppc.sh`). No emulator C code is altered in this patch. Therefore, every state the running code can save (registers, PC, MSR, memory) is mathematically left alone. This step is correct.

*   **Read-ahead Breakpoint Bypass:** The claim "the breakpoint keeps read-ahead off" (`2a:296`) is tested against the `cpu_dyntrans.c` logic. In `1b:1938-1939`, read-ahead strictly requires `cpu->machine->breakpoints.n == 0`. The session setup injects `"breakpoint add 0x3000"` (`2a:300`). Assuming this successfully increments `n`, read-ahead is aborted before evaluating `MAX_DYNTRANS_READAHEAD`. This claim is correct.

*   **Read-ahead Transfer to `bad:` Silenced:** The claim that a "read-ahead transfer returns silently" (`2a:254`) is tested against the `bad:` label. At `1b:1990-1991`, `if (cpu->translation_readahead) return;` executes immediately after resetting the slot to `TO_BE_TRANSLATED` (`1b:1988`), confirming that it bypasses the `UNIMPLEMENTED` print at `1b:2006` and the `cpu->running = 0` at `1b:2014`. This claim is correct.

*   **The Park at Arm (C) and Checkstop Absence:** The claim "arm (c) parked it; no checkstop" (`2a:306`) relies on the fetch being parked before reaching arm (d). In `1:4176`, `if (!cpu->running)` returns early and parks `next_ic`. Because the session uses `flags=["-T"]` (`2a:301`), if `-T` properly clears running, the CPU is parked and the checkstop logic (`1:4203`) is unreachable. The logical step within `cpu_ppc_instr.c` is correct. 

*   **Row Arithmetic:** The claim "Rows: 137 -> 153 in 20 sessions" (`0` and `2c:1`) is tested against the diff. `2a` introduces a loop over two unaligned patterns (`"o1"` and `"o2"`). The loop iterates 2 times, generating exactly 8 `row(...)` calls per iteration (`2a:302-309`). 2 * 8 = 16 new rows. 137 + 16 = 153. The script logic is correct.

**Unsettled Claims (Refutations limited by provided context):**

*   **Double-Entry Cancellation:** The claim "Every read-ahead session enters the failure block TWICE" (`2a:292-293`) cannot be fully verified. While read-ahead correctly fails and returns without advancing the PC, we must assume the main run loop correctly circles back to re-evaluate `TO_BE_TRANSLATED` on the same PC. UNSETTLED: requires the main execution loop in `cpu_dyntrans.c` or `cpu_ppc.c`.
*   **BLR Register Setup:** The claim that `T blr o1` and `T blr o2` properly place `r3 = 0x02040005 / 0x02040006` (`2a:298-299`) into the PC relies on `BLR_PUTS`. `2a:297` defines `BLR_PUTS = cmds[2:]`. The sequence inside `cmds` determining if `mtlr` and `blr` correctly transfer `r3` to `PC` is missing. UNSETTLED: requires the base `regress/ppc_ifetch_probe.py` defining `cmds`.
*   **`-T` Flag Mechanism:** The claim that `-T` clears `cpu->running` (`1:4136` comment and Section 3) cannot be verified from the fetch block alone. UNSETTLED: requires `memory.c` to confirm the `-T` flag behavior. 
*   **Guest PC Unmasking:** The claim "mtlr and bclr copy LR unmasked" (`1:4160`) cannot be mathematically proven without the architectural instruction models. UNSETTLED: requires `cpu_ppc_instr.c` instruction implementations for `mtlr`/`bclr` or the PowerPC manual.

P-GWEBP9QHS-891a
Review completed defensively based strictly on the provided inline block text.