# DATED NOTE beside `bound_assert_controls.sh` -- written 2026-09-06 by the retrospective
# re-check (batch 8b, GPT-6 Astra reviewing, adjudicated).  THE RECEIPT IS NOT EDITED.
# `bound_assert_controls_20260828.out` remains valid for the tree as it stood that day.

## What changed under the script, and why re-running it TODAY would mis-report

`bound_assert_controls.sh` negative-controls `gdrom_w_fits_its_carriers`, the static assert that
`GDROM_W_NBITS` fits the `warned` field.  When it was written the enum had SIX bit enumerators;
`#489`, `#490` and `#496` have since added five, so today

    sed -n '/^enum {/,/GDROM_W_NBITS/p' src/devices/dev_dreamcast_gdrom.c | grep -c '_B,'   ->  11

(derive it, do not trust this number -- the rounds that read it are the rounds that change it).
The script's own C1 label still says "shipped source, 6 bits over uint32_t".

**C3 would now report FAIL, and for a reason that has nothing to do with what C3 tests.**  C3
adds three enumerators and expects a CLEAN compile ("9 bits over the shipped uint32_t").  With
eleven already present that makes `GDROM_W_NBITS` fourteen -- still comfortably inside a
`uint32_t`, so the assert C3 aims at is still satisfied -- but a SECOND assert has landed since
(`gdrom_w_masks_disjoint`, added by `#490`), and it is written as

    (GDROM_W_LEN + ... + GDROM_W_CONDVAL) == ((1u << GDROM_W_NBITS) - 1u)

i.e. the sum of the ELEVEN NAMED masks against `2^NBITS - 1`.  C3's three extra enumerators
raise the requirement to 16383 while the named sum stays 2047, so the translation unit fails to
compile.  C3 gets `error`, wants `clean`, and prints `*** FAIL ***`.

**And nothing downstream would notice**, which is the part worth recording: `try()` prints its
verdict and does not propagate a status -- there is no `rc` accumulator and the script exits on
whatever its last command returned.  A driver that ran this and checked the exit code would read
a clean run.

## Disposition

No edit to the script and none to the receipt.  A future round that wants these controls live
again owes: C3 re-cut to add its enumerators AND their masks together (or to target the carriers
assert in a unit that does not carry the disjointness one), the C1 label re-derived rather than
transcribed, and `try()` given a status accumulator so a FAIL reaches the caller.  Filed as a
harness item rather than done here, because it is a change to a control script and controls owe
their own negative controls -- the shape this project has paid for before.
