## 5. The file's own idiom and the sibling dispositions (all quoted from HEAD in section 3 or below)

* **The house idiom in this file is a latched decline with a `(once)` marker**, one bit of `uint32_t warned` in
  `struct sgi_re_data` per site.  The enum's last enumerator at HEAD is `SGIRE_W_BADCOLOR = 1 << 12`, and its own
  comment says *"THE NEXT FREE BIT IS 1 << 13, AND THIS IS THE LAST ENUMERATOR"*.  Every entry above it records the
  rule *"a latch shared with any other site is silenced by that site's ordinary traffic"*, so each site gets its OWN
  bit.  A complete example, `horrible_getputpixel()`'s mode decline, is inlined in section 3d.
* **Census of suppression markers, run at brief-writing time against HEAD `2951694f`** (all `src/devices/*.c`, adjacent C
  string literals joined first): 92 markers in 13 spellings -- `(once)` 52, `(once per offset)` 12, `(once per offset
  per direction)` 5, `(further occurrences suppressed)` 5, `(once per bit)` 5, `(once per encoding)` 5, `(reported once)`
  2, and one each of `(once for each channel)`, `(once per direction)`, `(reported once per cpu)`, `(once per channel)`,
  `(reported once per register)`, `(once per timer)`.  (The raw scan printed a fourteenth spelling: one `(once per
  offset per direction)` torn across a COMMENT continuation, which the string-literal join does not repair.)
  `dev_sgi_re.c` carries 14 markers, all `(once)`.
* **The siblings inside `do_mte_transfer()` itself announce and CONTINUE, unlatched:** the `dst_y_step` check is
  `fatal(...); // exit(1);` (the call disabled by a comment), and the `switch (dst_tlb)` `default:` arm is a bare
  `fatal(...)`.  Both are guest-drivable and unlatched; both are FILED as their own rows (`mtetlbflood`,
  `sgimtetlbdefault`, LOW) and are NOT in this round.  The register arms `CRIME_MTE_STIPPLEMASK`, `CRIME_MTE_NULL` and
  `CRIME_MTE_FLUSH` in `DEVICE_ACCESS(sgi_mte)` are unlatched `fatal()`s too.
* **No completion status can hang the guest:** `CRIME_DE_STATUS` returns the constant `CRIME_DE_IDLE |
  CRIME_DE_SETUP_IDLE | CRIME_DE_PIXPIPE_IDLE | CRIME_DE_MTE_IDLE` whatever the transfer did (section 3c).

## 6. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

* **`fatal()` does not end the process** -- it prints and returns (`src/core/debugmsg.c`); only the `exit(1)` beside it
  terminates.  Settled repeatedly in this campaign; `debug()` has a verbosity early-out, `fatal()` has none.
* **`do_mte_transfer()` is called from exactly one place**: the end of `DEVICE_ACCESS(sgi_mte)`, `if (startFlag)
  do_mte_transfer(cpu, d);`, followed by that handler's common tail (`if (writeflag == MEM_READ)
  memory_writemax64(...); return 1;`) -- section 3b.  `do_mte_transfer()` returns `void` and has NO statements after its
  `switch`, so a `return` inside it skips nothing the caller depends on.
* **`mte_reg[]` is zeroed at device init** (`memset(d, 0, sizeof(struct sgi_re_data))` in `dev_sgi_re_init()`), so
  `BYTEMASK` reads 0 until a guest writes it: a LINEAR fill by a guest that never writes BYTEMASK reaches S5 today.
* **The sixth `exit(1)` is unreachable** (`if (len == 4) ... else if (len != 4) ... else`) -- GPT-6 Astra, 2026-09-09,
  re-derivable from section 3b; filed as `sgimtewidth`.
* **Grok 4.7's 2026-09-07 design answer already classed these five** as *"unimplemented transfer features (member 7 /
  decline-the-transfer, not member 4)"*, separate from the RE read arms by function, trigger, member and detector -- which
  is why `#513` excluded them.  It also noted that the `depth == 4` dead branch (`#509`, row `sgimtedepth4dead`) is on
  the TILED path and that declining linear `depth != 8` does not touch it.

## 7. The disposition -- my leaning, stated as QUESTIONS

The option set has SEVEN members: **1 DELETE** the terminating call only (announce and continue, the `dst_y_step`
shape) / **2 DECLINE silently** / **3 DECLINE + LATCHED ANNOUNCE** / **4 ACCEPT** (the model already computes the right
answer) / **5 FAULT** (model the space as unmapped -- `dev_unreadable.c`) / **6 BACKED ACCEPT** (fabricate storage) /
**7 IMPLEMENT** the feature.  Members 4 and 6 do not fit a TRANSFER (there is no value being read back), and member 5
does not fit an access to a mapped register whose only fault is the parameter it carries -- **say so if you disagree.**

**My leaning: member 3 at all five sites** -- `if (<guard>) { if (!(d->warned & SGIRE_W_MTE_<x>)) { d->warned |=
SGIRE_W_MTE_<x>; fatal("[ sgi_mte: ... -- transfer declined (once) ]\n", ...); } return; }`, five new bits `1 << 13`
.. `1 << 17`, the enum's "last enumerator" sentence moved with them.  The transfer is refused BEFORE any memory write:
S1 and S2 return before the destination switch, S3-S5 return before the fill loop (`memset(zerobuf, ...)` and the
`memory_rw` calls).  **Check each part of that:**

* **Q-a.** Is member 1 (delete only the `exit(1)`, keep going -- the file's own `dst_y_step` precedent) wrong here?
  My reason: at S3-S5 continuing runs the LINEAR fill with the unsupported parameter ignored -- at S4 the fill is
  `memset(zerobuf, bg, ...)`, which repeats only the LOW BYTE of `bg` at 16/32 bpp; at S5 it writes every byte the mask
  says to leave.  That is a silently wrong guest-visible result plus an unlatched message per transfer.  At S1 a
  stippled fill would become a solid fill.  Is "the destination is left untouched" actually better for a guest than
  "the destination is written approximately"?  Neither matches hardware.
* **Q-b. S2 refuses FILLS over a field a fill never reads.**  `src` is read only by S2's guard; `src_tlb` feeds only
  `src_mode`, which is used only under `if (mode & MTE_MODE_COPY)` in the tiled arm, and the linear arm reads no source
  at all (section 3a).  So today `src = 3..7` with COPY CLEAR ends the process for a transfer that would never touch
  the source.  Should S2 be scoped to COPY -- decline only `(mode & MTE_MODE_COPY) && src > MTE_TLB_C`, and let a fill
  with an unused source field proceed?  That would be a NARROWING of a guard, so it needs a warrant, not "cannot hurt":
  is there one (an SGI/NetBSD source, a manual) for what the hardware does with SRC_BUF on a fill?  If there is none,
  is the conservative answer to decline exactly what is refused today?
* **Q-c. Member 7 (implement) at S4 and S5.**  A depth-16/32 linear fill is a pattern-width change to an existing
  loop, and a byte mask is a read-merge-write per page.  The addition licence here requires a measured delta or a
  transferred warrant.  Is there one, or is IMPLEMENT a separate row?
* **Q-d. Latch granularity.**  One bit per SITE (five bits), or one per site AND destination label (S3-S5 sit in a block
  shared by `MTE_TLB_LIN_A` and `MTE_TLB_LIN_B`)?  A per-site bit means a LIN_B transfer is silent after a LIN_A one at
  the same site.
* **Q-e. Decline scope.**  The decline skips every remaining side effect and still answers through the caller's
  common exit (section 6).  Is anything between the top of `do_mte_transfer()` and S1-S5 a side effect that should not
  happen on a declined transfer?  (I see `debug()` calls and the `dst_y_step` `fatal()`; S5 sits after the linear arm's
  `debug(... LINEAR TRANSFER ...)`.)

## 8. The detector I propose (it ships WITH the fix; written before any table runs)

A new probe, `regress/sgi_mte_decline_probe.py`, grown from the witness (same session mechanics), wired into
`regress/gate_arm.sh` beside `sgi_re_width_probe.py` with its row counts pinned by equality.  Rows, each with the
mutant it is meant to catch and the observable that differs (the CHANNEL line):

| row(s) | what it drives | catches | channel |
|---|---|---|---|
| `<site> surv`, five | the witness's transfer | `exit(1)` reinstated (floor clause b) | the process ends |
| `<site> nowrite`, five | the same transfer at a destination the transfer WOULD write, pre-painted (tiled: the `TLBA_TILE` page `sgi_mte_fill_probe.py` uses; linear: a `re_linear_a/b` entry mapping the page) | member 1 -- `exit(1)` deleted, no `return` | the paint is overwritten |
| `<site> once`, five | two transfers in one session | a missing latch, a missing announce, a shared bit | the site's text appears exactly once |
| `lin b <site>`, three (S3-S5 at `MTE_TLB_LIN_B`) | the label the linear block also serves | a repair conditioned on `dst_tlb == MTE_TLB_LIN_A` | survival / paint at LIN_B |
| `src c fill` | a tiled fill with `src` field 2 (`MTE_TLB_C`, the bound) | `src > C` moved down one (`>= C`): the at-the-bound value would be refused | the fill lands |
| `src tex` / `src clip` | `src` 3 (B+1) and 6 | `src > C` moved up one (`> 3`): the first refused value would pass | decline |
| `lin fill`, `lin b fill` | every guarded value legal, at both labels | guard growth at S3-S5 (the de-escalation clause's accept side) | the fill lands |
| `bytemask lo`, `bytemask hi` | `0xfffffffe` and `0x7fffffff` | a narrowed mask compare (`(bytemask & 0xffff) != 0xffff`, `& 0xff...`) | decline vs fill |
| `depth 16/32/64` | fields 1, 2, 3 at LIN_A | `depth != 8` qualified to one value | decline |
| `live`, `devsig`, `mode rt` | as in the witness | -- | controls |

Clause (c), the null medium: an absent or non-emulator binary -- every session dies, so every `surv` and `nowrite` row
reds and the gate's equality pin on rows-green fails; I intend to MEASURE that leg rather than claim it by construction.
Clause (e), the contract, goes in the probe header.  A `PRETABLE.out` is written before table 1.

