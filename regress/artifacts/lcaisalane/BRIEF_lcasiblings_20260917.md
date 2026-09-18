# THREE UNREVIEWED `dev_lca.c` DEFECTS ON THE HANDLER YOU JUST SETTLED -- **ZERO SEAT ENTRIES EACH**

## VERDICT LINE FIRST.

**You have already done the hard reading for this.**  In settling `#530`'s len-16 question you
established, from `_scratchpad/21066_66a_hrm.txt`, that CPU `a<4:3>` IS the transfer size, that
`a<6:3>` generate `c_be_l<3:0>`, that I/O space takes `ad<1:0>` from `a<6:5>`, and that the widest
CPU-initiated sparse transfer is QUADWORD = 8 bytes.  **You then named `lcaisasize` yourself as the
real residual.**  This brief hands you that row and its two siblings.

**TREE: `GXEMUL-SEC/src/devices/dev_lca.c`.**  You can read files.  Three pristine-2021 upstream
copies sit under the PROJECT root -- ignore them.  **PLEASE DO NOT RATIFY.**

## S1 -- WHY THIS IS WORTH YOUR TIME AND NOT MINE

All three rows are `open`, `med`, and carry **ZERO seat entries of any kind** -- no codex, no grok,
no fable, nobody.  They were filed and never reviewed.  This project's standing directive is a
nine-seat panel on every fix; these never got one seat.

They are also **all on the SAME handler**, which is why they go out together rather than as three
briefs: the interesting question is not "is each real" but **whether they are three defects or one,
and whether a fix for one silently changes another.**

## S2 -- THE THREE ROWS, VERBATIM FROM THE LEDGER

### `lcaisaphys`
> dev_lca.c DEVICE_ACCESS(lca_isa): both nested memory_rw calls omit PHYSICAL, handing a physical
> address to the translator as a virtual one -- **the moment a guest enables page tables the ENTIRE
> sparse I/O window dies on an unlatched guest-drivable `fatal()`**

### `lcaisasize`
> dev_lca.c DEVICE_ACCESS(lca_isa): `relative_addr >>= 5` discards the a<4:3> TRANSFER-SIZE field,
> so **7 of the HRM's 11 legal encodings are under-copied** -- and on the canonical LDL path the
> guard never fires, making it **silent and total**

### `lcaisaqword`
> dev_lca.c DEVICE_ACCESS(lca_isa): for the QUADWORD encoding a<6:5> is NOT ad<1:0>, so **a
> quadword I/O access to port P is forwarded to port P+3** -- an ADDRESSING defect, and a fix for
> the width defect does not imply a fix for this

## S3 -- SETTLED, BY YOU, THIS HOUR (do not re-derive)

* `a<4:3>` is the transfer size; `a<6:3>` generate `c_be_l<3:0>`; `a<2:0>` must be zero.
* I/O space (S6.2.8) uses the same encodings, with `ad<1:0>` from `a<6:5>`.
* The widest CPU-initiated sparse/I/O transfer is QUADWORD = a PCI burst of two longwords = 8 bytes.
* The sparse slot is 32 CPU-address bytes per port -- the handler's `relative_addr >>= 5`.
* Forwarding ONE byte for a BYTE-encoded address is correct and is `#530`'s settled contract.

## S4 -- THE QUESTIONS

1. **IS EACH ONE REAL?**  Take them separately.  For each: does the defect exist in the shipped
   code, and is it GUEST-REACHABLE?  `lcaisaphys` claims a total window death once page tables are
   on -- **that is the most severe claim here and the one I most want checked**, because if true it
   is not a MED.

2. **ARE THEY THREE DEFECTS OR ONE?**  They all live in the same few lines.  Does fixing the size
   field fix the quadword addressing, or are the two genuinely independent as `lcaisaqword` asserts?
   **The row says a width fix "does not imply" an addressing fix -- test that claim.**

3. **DOES ANY FIX HERE COLLIDE WITH `#530`'s SHIPPED REPAIR?**  `#530` added `if (len == 0) return 0;`
   and `ofs = (relative_addr & 3) % len`, and its detector has 352 rows.  **A fix that changes what
   `relative_addr` means before the `% len` would move those rows.**  Which of the three, if any,
   cannot be done without re-tabling `#530`?

4. **SEVERITY AND ORDER.**  If you were spending one round on this handler, which row would you
   take first, and why?  This project ranks by SEVERITY and gate blind-spots, never by how strong
   the reachability proof is.

5. **IS THE `fatal()` IN `lcaisaphys` REALLY UNLATCHED AND GUEST-DRIVABLE?**  Settled premise:
   `fatal()` is a PRINT, not a kill (`src/core/debugmsg.c`, no `exit(`/`abort(`, no `-q` early-out),
   so the defect would be a `floodclass` log flood plus a dead window -- not a host death.

**STANDING LICENSE: if while checking these you find a FOURTH thing, say so.**
