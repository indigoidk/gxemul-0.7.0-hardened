# PANEL PASS 2 — `#505` sgirergbroundtrip, on the real diff

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. **Pass 1 of this very round refuted my central premise** — I claimed the GET arm was wrong on
two grounds and four seats showed one was circular and the other neutralised. They were right. So
this brief's premises have already been wrong once today; assume they can be again.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES, re-inlined so nobody spends an answer re-deriving them

**S1 — THE DEFECT.** `horrible_getputpixel()`'s RGB PUT wrote the three channels at `buf[0..2]` and
an explicit pad at `buf[3]`; its RGB GET read `buf[1..3]`. RGB was the only 32-bit colour mode in the
file failing its own round trip.

**S2 — WHY THE *GET* IS THE WRONG ARM, settled on pass 1 and NOT by the argument I first gave.**
My original grounds were refuted as circular. The surviving warrant comes from a **different device**:
`dev_sgi_gbe.c`'s scanout reads the same tile memory back for display as
`(buf[i]<<24)+(buf[i+1]<<16)+(buf[i+2]<<8)+buf[i+3]`, and `CRMFB_MODE_TYP_RGB8` — commented in-tree
as *"Used by NetBSD's X11 server"* — takes R, G and B from bits 31..24, 23..16 and 15..8. **Byte 0
is R and byte 3 is unused.** The pad sits at `buf[3]` because the *consumer* ignores `buf[3]`, which
is what makes the warrant independent of either arm under test.

A pass-1 seat added the other half: **RGBA and ABGR write identical memory bytes `[R,G,B,A]`** and
differ only in register word order, so all three 4-byte PUT arms agree on the container and the RGB
GET is the lone outlier.

**S3 — THE POST-FIX VALUE IS NOT THE SOURCE VALUE.** RGB carries three channels, so a corrected read
of `0xaabbccdd` yields **`0xaabbcc00`**. My pre-panel oracle pinned `0xaabbccdd` and would have
failed a correct fix; four seats named `0xaabbcc00` independently. The oracle was re-pinned **before**
the code changed and the committed build re-measured RED under the new expectation.

**S4 — MEASURED.** Pre-fix `4/6`, post-fix `8/8`, same script, on an unmodified `-E sgi -e ip32`,
with a liveness control, a device-signature control and a sibling accept control (`copy lin_a`, an
RGBA source through the same helper) green throughout.

**S5 — TWO KILL TABLES. Table 1 found a floor breach in my own detector.**

| mutant | table 1 (6 rows) | table 2 (8 rows) |
|---|---|---|
| base | 6/6 | 8/8 |
| `M1_verbatim` (clause b) | 4/6 | 4/8 |
| `M2_off1` | 5/6 | 5/8 |
| `M3_pad` (returns the source word) | 5/6 | 6/8 |
| `M4_or` (`+`→`|`) | 6/6 | 8/8 |
| `M5_rev` | 5/6 | 5/8 |
| `M6_cond` (clause d, exempts bufdepth 4) | **6/6 SWEEP** | **7/8** |
| `M7_cond8` (the mirror, exempts bufdepth 8) | — | **7/8** |
| `M8_put` (corrupts the RGB PUT arm) | — | **7/8** |
| null medium | 1/6 | 1/8 |

`M6_cond` kept the guard and conditioned the repair on `bufdepth == 4` — and **every session then
used `BUFDEPTH_32`, so bufdepth was 4 in all of them and the mutant's fix branch was the only one the
detector executed.** Repaired in-round (L2) by `rgb depth64`, a session at `BUFDEPTH_64`. `M7_cond8`
was then built specifically to test whether I had repaired only the cell the mutant named; it dies.

**S6 — `M4_or` IS AN EQUIVALENT MUTANT.** The three byte fields are disjoint (bits 24-31, 16-23,
8-15), so `+`, `|` and `^` compute the same value — enumerated over 80 byte triples with zero
disagreements, and its row values are byte-identical to base. It is unkillable by construction, not a
coverage hole.
