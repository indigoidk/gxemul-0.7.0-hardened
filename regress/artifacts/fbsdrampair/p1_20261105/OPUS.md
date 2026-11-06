# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-05 04:18:39Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpfbopus/60a93c22-8cd9-4834-9004-50ed6165df38.jsonl`
* session: `https://claude.ai/code/session_015fEQzKdUS7Y8R8EMzQKRXC`   trigger: `trig_012eJ6hrxmwfecFRKn3Rtam6`   packet: `C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/cloud_r3/FBSDRAM_P1.md`
* the answer's message: timestamp 2026-11-05T04:06:41.044Z, model field `claude-opus-5-5` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-opus-5-5'])
* delivery token `CLOUDFBSDRAMP1`: present; 6941 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDFBSDRAMP1: 5 ANSWERS 2 FALSE-PREMISES 11 ROWS-PROPOSED VERDICT:3

---
CLOUDFBSDRAMP1
model: claude-opus-5-5
VERDICT: 3 (DECLINE + a latched announce, one latch per register) for the reads, but the declined read returns each register's documented reset value (mask 0x00FC0000, offset 0), not 0; keep the writes.

**1. Disposition of the reads**

- **FAULT (5) is ruled out.** Both registers exist on the chip, so modelling them as unmapped would be wrong.
- **DELETE (1) and silent DECLINE (2) are ruled out.** A guest reading a register the model doesn't hold should be visible, so the decline needs its announce.
- **ACCEPT (4) needs a value the model already computes.** It computes nothing for these registers.
- **BACKED ACCEPT (6) needs a measured difference or a transferred warrant.** This packet supplies neither.
  - From memory, and not checked here: Linux `dc21285_preinit` only writes these two registers. I can't settle whether NetBSD/cats, OpenBSD/cats or the CATS firmware read them. GXemul boots the kernel directly, with no firmware, so a firmware read never happens here. So the filing's "0/2 consumers" is plausible but unverified.
- **Is 0 the wrong value?** Yes, and this is where I part from the filing. The filing frames the harm as "a guest that reads them back after writing". But a guest that never writes also gets the wrong answer.
  - The mask resets to 0x00FC0000 (datasheet line 3225). A read before any write should return 0x00FC0000. Returning 0 means a 256KB window, which hardware never reports from reset.
  - After a write, hardware returns the written value with the read-only bits cleared: mask = value & 0x8FFC0000, offset = value & 0x0FFC0000.
- **Returning the reset value fits the model as it stands.** The model discards every write, so its true state is the reset state. Returning that state is consistent with what the model actually does, and needs no new storage.
- **Return the reset value, and the code-path tests can see the value.** If the decline returned 0, a variant that flips the `writeflag` test would read 0 for the mask, exactly like the fix, and only the announce text would expose it.
- **Offset:** reset value is 0, so 0 is right until a write.

**2. The writes**

- **Keep them.** Adding backing fields is BACKED ACCEPT, and it needs the warrant (a guest that writes then reads). File that as its own row.
- **The 0x8FFC0000 ("No window") whitelist case is a separate row.** It is the same device but a different semantic class and a different detector:
  - It is not an exit. It prints a spurious, unlatched announce for a legal value.
  - Its detector counts stderr messages; this round's detector is whether the process survives.
- **Other things for that separate row:**
  - The whitelist compares the whole `idata`, so a legal mask plus reserved bits 17:0 (for example 0x00FC0001) is announced, though hardware ignores those bits.
  - The write announces at lines 751 and 763 are unbounded, so a guest can flood the log.

**3. The witness (rung 3, `-E cats`)**

Run two separate arms. On HEAD the process ends at the first read, so one combined arm can never reach the second site.

Prelude for every arm:
```
mrc p15,0,r0,c1,c0,0
bic r0,r0,#1
mcr p15,0,r0,c1,c0,0
mrc p15,0,r1,c1,c0,0      ; prove bit 0 is clear
ldr r2,=0x42000000
ldr r3,[r2,#0]            ; signature: 0x1011
ldr r4,=0xDEADBEEF        ; sentinel
```
- **Arm M:** `ldr r4,[r2,#0x100]`, then write a RAM liveness word and read it back.
- **Arm O:** the same, reading `[r2,#0x104]` into r5 (also preloaded with the sentinel).
- **Expected results:**
  - HEAD: exit status 1, stderr shows "read from sdram_ba_mask" (or "…offset"), and no liveness word.
  - Fix: the process survives, liveness is present, r4 = 0x00FC0000, r5 = 0.
- **MMU-on discriminator:** the same reads with the MMU left on. They hit PA 0x02000000 (RAM), so the guest must not see 0x1011 and HEAD must not exit.

**4. The detector**

| Row | What it checks | What catches what |
|---|---|---|
| R1 | HEAD, arm M | process ends |
| R2 | HEAD, arm O | process ends |
| R3 | Fix, arm M | r4 = 0x00FC0000 and exactly one "(once)" announce |
| R4 | Fix, arm O | r5 = 0 and exactly one announce. The value alone can't catch a flipped test here (reset value is 0), so the announce count must be checked |
| R5 | Fix, reads interleaved M, O, M, O | announce count = 2, one per register |
| R6 | Fix: write 0x03FC0000 to the mask, then read | 0x00FC0000 comes back (pins the decline, so accidental backing shows), and no write announce |
| R7 | Fix: write 0x12345678 to the mask | the whitelist announce appears and the read announce does not |
| R8 | Fix: write 1 to the offset | the write announce appears |
| R9 | Null medium on HEAD and fix: liveness and signature only, no access to 0x100/0x104 | identical output |
| R10 | MMU-on discriminator | as in section 3 |
| R11 | Liveness and signature controls | present in every arm |

How each variant is caught:
- **Removed exit put back verbatim at both sites:** R3 and R4 fail, because the process ends. Separate arms let you tell which site.
- **`writeflag == MEM_READ` test dropped** (the arm always declines): R7/R8 lose the write announce and gain the read announce.
- **Test inverted:** the mask read goes to the whitelist path. R3 then sees r4 = 0, not 0x00FC0000, and gets no announce. R4 gets no announce.
- **Early `return` in a read arm:** R3/R4 see the 0xDEADBEEF sentinel, because `odata` is never written back.
- **Latch never set or never tested:** R5 count is greater than 2.
- **One shared latch:** R5 count is 1.
- **Latch test inverted:** R5 count is 0.

Use one latch per register, matching the per-site latches #545 added. The observable for every row is the guest registers, the stderr announce count and the exit status.

**5. Premises**

False:
- **(a) The #545 value warrant doesn't carry over.** That warrant (datasheet: a nonexistent CSR reads as zeros) covers registers that don't exist. These two exist, so it gives no license for returning 0.
- **(b) "The whitelist rejects 0x8FFC0000" overstates it.** Every write is discarded the same way. The only difference is an extra announce.

Confirmed by enumeration:
- **Table 7-7 pairing holds.** There are 12 names and 12 values, so pairing them in order works. Each set bit in mask bits 27:18 doubles the window, so window = 2^(18 + set bits): 0x00FC0000 has 6 bits set, which gives 16MB; 0x0FFC0000 has 10, which gives 256MB.
- **These are the last two exits.** The function has only two `exit` calls, at lines 735 and 760.
- **#545 removed five exits.** There are five #545-tagged arms.

Unsettled from this packet:
- Whether the fork's `dc21285reg.h` has `SDRAM_WINDOW_DISABLE (1<<31)`. I recall upstream NetBSD has it.
- Whether `footbridge_data` is zeroed when allocated. The new latches depend on it.
- The probe's MMU-alias claim, and that the code turning the MMU off runs at an address where VA equals PA.

CLOUDFBSDRAMP1: 5 ANSWERS 2 FALSE-PREMISES 11 ROWS-PROPOSED VERDICT:3
