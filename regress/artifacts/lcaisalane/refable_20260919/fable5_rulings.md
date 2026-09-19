FABLE_SEAT_ALIVE_20260919_REFABLE
claude-fable-5-1 | # CHECKPOINT -- 2026-09-19 01:4x
VERDICT: A AGREE ; B CLOSES: none undetected (lane floor 0/4 open)

# The handler, read (the object of both rulings)

`DEVICE_ACCESS(lca_isa)`, `src/devices/dev_lca.c:275-320` (READ). The body-induced partitions,
and which flow into the #530-edited write statement `byte = data[ofs]` (`:308`) / its forward
`LCA_ISA_BASE + relative_addr` (`:309-310`):

- `relative_addr >>= 5` (`:280`) makes `relative_addr` the PORT.
- `len` is tested ONLY against 0 (`:295`) and used as the `%` divisor in `ofs = (relative_addr & 3) % len`
  (`:297`). The `%` partitions `len` into {1,2,3,>=4} only; it does NOT distinguish 16 / 64 / 256, and
  the body never compares `len` to any threshold above 0 (READ `:295-297`).
- `ofs = (relative_addr & 3) % len` computes a selector from the LANE = `relative_addr & 3`; at len 16 it
  is exactly the lane. `data[ofs]` (`:308`) is the operand of the edited write statement (READ).
- the whole port flows into the forward ADDRESS (`:309-310`), but the body never tests it against a
  constant and computes no port-magnitude selector (READ).

By my #540-pass-1 rule, the sole FLOOR axis of the len>8 write case is LANE: the body computes it
(`ofs`), and it flows into an operand of the edited statement (`data[ofs]`). Floor = {write arm} x
{lane 0,1,2,3}. Every other axis is clause (e). (INFERRED from the READ above.)

# (A) The seven variants #530's single lane-3 row leaves undetected -- AGREE with all seven

The seven that are behavioral one-edits AND score full marks on the shipped `frozen` (lane-3) row
are `va, vb, vc, ve, vg, vt1, vt2` (MEASURED, opus_p2_20260918/RESULTS.txt: `frozen` row = 3/3 for
each; `vf` is 2/3 there, i.e. DETECTED, and `vd/vh` are equivalent, `vw64/vw256` a width ladder --
so those five are not the escaping seven). Variant diffs READ from
opus_p2_20260918/variants/*.diff.

| variant | edit (READ) | my disposition | vs record |
|---|---|---|---|
| `vc` | write arm `&& (len <= 8 \|\| (relative_addr & 3) == 3)` | **FLOOR** | AGREE |
| `va` | write arm `&& len <= 16` | disclosed (i) | AGREE |
| `vb` | `len == 0` -> `\|\| len > 16` return 0 | disclosed (i) | AGREE |
| `ve` | `\|\| (len > 8 && relative_addr < 0x200)` return 0 | disclosed (ii) | AGREE |
| `vg` | pre-shift `if (len > 8 && (relative_addr & 0x10)) return 0` | disclosed (iii) | AGREE |
| `vt1` | pre-shift `if (len > 8 && (relative_addr & 0x1f)) return 0` | disclosed (iii) | AGREE |
| `vt2` | pre-shift static continuation refusal | disclosed (iv) | AGREE |

Reasons (INFERRED from the READ handler unless noted):

- **`vc` is the one FLOOR breach.** It conditions the write service on LANE, servicing wide writes
  only at lane 3 and declining lanes 0,1,2 -- three of the four floor cells. LANE is floor (above),
  so `vc` reopens the defect at three unrowed floor cells while passing #530's lane-3 row. That is a
  floor breach, and it is exactly the gap #538 must row. AGREE.
- **`va`, `vb` -- DISCLOSED (i).** Both key on `len` above 16. The body induces no partition on `len`
  at 16 (tested only against 0; the `%` separates 1/2/3 from >=4 only). At all four wide cells
  `len == 16`, so both are no-ops there. Not body-induced -> not floor.
- **`ve` -- DISCLOSED (ii).** Keys on the shifted `relative_addr < 0x200` = PORT MAGNITUDE, which the
  body never tests or selects on (only `& 3`, the lane, is extracted). It incidentally reddens
  `low16` (port 0x021 < 0x200), but that is a sensitivity of a lane cell to a disclosed axis, not a
  new floor cell; the contract does not claim it. Not floor.
- **`vg`, `vt1` -- DISCLOSED (iii).** Both key on the pre-shift bits a<4:0> (the `k` bits `>>= 5`
  discards). The body uses those bits as neither selector nor index into the edited statement -- it
  drops them. Every cell is k=0, so both are no-ops. Not body-induced -> not floor.
- **`vt2` -- DISCLOSED (iv).** A STATEFUL continuation refusal; the shipped handler holds no state
  across calls (READ `:275-320`: no static/persistent variable), so "chunk position" is not a
  body-induced axis, and one wide write per session makes it a no-op. Not floor.

I also confirm the record's covering-vs-closure point: rowing fewer than four lanes leaves some
lane's single-lane exemption (`&& (len <= 8 || (P&3) != L)`) undetected, so the floor is a genuine
four-cell closure, not a two-cell covering.

# (B) #538 closes the lane floor -- CLOSES, no floor cell undetected

#538 rows all four floor lanes, one isolated session each: `wide`=lane3 (port 0x2ff), `l0w16`=lane0
(0x2fc), `low16`=lane1 (0x021), `l2w16`=lane2 (0x2fe) (READ lca_widewrite_probe.py:243-251; the
`assert sorted(... & 3) == [0,1,2,3]` pins all four lanes). 13 rows; base = construction control.

Measured, one-instrument re-run (MEASURED, rerun_20260919_0030/logs/TABLE.out; every leg
`clean=4/4`, so the wait-status harness moved no score):

- `base` 13/13 red=[] -- instrument sound.
- Each single-lane exemption is detected by EXACTLY its own lane's row: `vc_ne0` 12/13 red=[l0w16],
  `vc_ne1` 12/13 red=[low16], `vc_ne2` 12/13 red=[l2w16], `vc_ne3` 12/13 red=[wide].
- `vc` (services lane 3 only) 10/13 red=[l0w16, low16, l2w16] -- the three lanes #530 missed, lane 3
  correctly green.
- Total declines detected at all four: `M2_len8` 9/13 and `KILLLEN8` 9/13, red=[all four getenv].
- Wrong-lane-byte `vf` 10/13 red=[wide, low16, l2w16] (lane 0 green because `data[0]` is the lane-0
  byte) -- caught at the three lanes where it differs.

So every one of the four floor cells has a row that reddens when the defect is reopened at that
lane; the lane floor is 0/4 open. The specific escape a two-cell covering misses (`vc_ne1`, lane 1)
is red at `low16` (MEASURED, same table). INFERRED: no floor cell is left undetected.

Integrity of the re-run (the record's stated contingency), all MEASURED / READ:
- The re-run instrument is CODE-IDENTICAL to the shipped `regress/lca_widewrite_probe.py`; `diff`
  differs only inside the module docstring's MEASURED paragraph (READ, `diff` output lines 75-88, all
  within the `"""..."""`). So the shipped detector is the instrument that produced the table.
- Same 17 mutant binaries, verified before the legs (MEASURED, logs/bins.md5 + BUILD_PHASE.out:
  `BASELINE_CMP CLEAN`, `restored == base byte-identical`, every mutant `BINARY_DIFFERS`).
- The first table (logs/TABLE.out) gave the same scores and red-row sets (MEASURED), and the re-run
  matched its written-first predictions (MEASURED, rerun PRETABLE_RERUN.out vs TABLE.out: 17/17).
- `l2w16` (lane 2) is non-vacuous: preset 0x01 (not 0x00) so `live` reads 0xb1 and a decline keeps
  0xb1 != WANT 0xf3 (READ lca_widewrite_probe.py:247,249-250); it reddens under M2_len8/KILLLEN8/vc/
  vc_ne2 (MEASURED, TABLE.out).
