# #530 PASS 2 -- the Opus 5 seat (Agent tool, measuring)

*** TRANSCRIBED BY THE MAIN LOOP (the Agent seats leave no file).  Verdict and tables VERBATIM in substance from the
returned answer; the seat's first turn ended mid-wait and it was RESUMED to finish (no re-launch).  The main loop
re-read the table logs before recording: table_p2.out ends KILLP2_DONE, table_p2b.out ends KILLP2B_DONE, and every
p_* leg reads `LCAISALANE_RESULT=37/37' on the 37-row instrument; disc_base.out / split_base.out quoted below. ***

Liveness `OPUS_SEAT_ALIVE_20260914_LCA530_P2`; CHECKPOINT line 1 quoted verbatim.

## VERDICT: HOLD -- the FIX is right; the 37-row DETECTOR is not

`byte = data[ofs];` -> `byte = data[ofs & 1];` scores 37/37 (logs/probe_p_wbit1.raw) while a guest `stl 0x7e000000` to
sparse SCR lands 0x00 instead of 0x7e (logs/disc_p_wbit1.out) -- a contract breach (the contract claimed "a lane decode
that drops bit 1"), clause (e), L2.  Nine of eleven mutants scored 37/37; eight change a guest-visible outcome, one is
a true equivalent.

## Q1 -- the fix: YES
Producers: the Alpha load/store path emits len 1, 2, 4, 8; memory_rw's 1 KB split emits heads/tails 1..7 (MEASURED);
the device's end-of-window clamp gives 1..7 at port 0xffff only (read, not measured); nothing emits len 0.  For every
len >= 1, `ofs = (P & 3) % len < len` -- no OOB, no divide, no exit left.  Split heads measured: a 3-byte head at port
0x3ff returns 0x5a at position 0, 5/6/7-byte heads at position 3 (logs/split_base.out).  The ignored nested-read
return is harmless (the one non-zeroing path halts the CPU first).  Out of round: memory_alpha.c's `exit(1)` at
vaddr 0xfffffffd80000000 with ptbr 0 -- ALREADY FILED as `alphavmkill`.

## Q2 -- the floor gap, MEASURED
| mutant | 37-row | guest outcome changes? | disposition |
|---|---|---|---|
| p_wbit1 `byte = data[ofs & 1];` | 37/37 | stl -> SCR 0x00 (want 0x7e); stq -> 0x00 (want 0x6d) | contract breach, L2 |
| p_rep4 `data[i] = (i == ofs \|\| len == 4)? byte : 0x00;` | 37/37 | ldl LSR 0x60606060 (want 0x6000) | contract breach, L2 |
| p_wnarrow `if (writeflag == MEM_WRITE && len <= 2) {` | 37/37 | len-4/8 stores become reads | clause-(d) conjunct on the edited line's guard |
| p_wdrop4 `if (len == 0 \|\| (len > 2 && writeflag == MEM_WRITE)) return 0;` | 37/37 | stores dropped | same class |
| p_waddr4 forward to `relative_addr ^ (len > 2)` | 37/37 | stl SCR lands on MSR; stl MCR lands on LSR | forwarded-address gap |
| p_lane0decl `if (len == 0 \|\| (len > 1 && (relative_addr & 3) == 0)) return 0;` | 37/37 | ldl MCR keeps the sentinel; stl MCR dropped | (2,0)(4,0)(8,0) both arms |
| p_andmask `& (len - 1)` | 37/37 | at split heads: q_h3 0x5a0000, q_h5 0x5a, w_h3 0xc3 | disclosed on a FALSE premise |
| p_q8lane `(relative_addr & (len > 4? 1 : 3)) % len` | 37/37 | stq/ldq lane 3 give 0x0 | arguably under lcaisaqword |
| p_port10 `relative_addr &= 0x3ff;` | 37/37 | port 0x7ff reads SCR | outside the fix |
| p_nozero `if (i == ofs) data[i] = byte;` | 37/37 | NO (memory_rw's #95 pre-zero) | truly equivalent |

Repair, measured on base (no new process needed): `stl 0x7e000000` -> SCR; `stl 3` -> MCR then full-register `ldl`;
full-register `ldl` of LSR; `ldq`/`stq` at SP(SCR) + 0x1d (the (3,3) split head, red on HEAD); a lane-3 `stq`/`ldq`.
Clone /tmp/gxopus530 restored: no sentinel, cmp-clean, fresh, restored == base.

## Q3 -- wrong statements (8)
1. The split-head disclosure's premise ("needs a TRANSLATED access"): FALSE -- MEMORY_RW splits whenever
   `translate_v2p != NULL` and the access is not PHYSICAL; Alpha always sets it; measured on K0SEG.
2. Fix comment "byte/word access to a port 2 or 3 mod 4": a word at 2 mod 4 never exited (`2 > 2' is false).
3. Fix comment "the rule the write arm already applied to every narrower one": the exit fired first at 3 of 8 cells.
4. PRETABLE item 1 lists w11/w22 as changed cells: HEAD already served both; the changed (3,3) read had no row.
5. PRETABLE item 3 "the fix's only guard reads len": the edited line is also guarded by `writeflag == MEM_WRITE'.
6. POSTTABLE FLOOR "(d) ... all red": incomplete (p_wnarrow).
7. POSTTABLE "RETRIED=none on all 14 legs": that line covered only the three witness sessions; dsession retried silently.
8. The contract's "drops bit 1" and "replicated into every position": measured false for the write arm and len 4.

## Could not check
A translated (page-table) guest access; a real OS boot; hardware's len-8 lane; the port-0xffff clamp producer.
