# Read-only audit: the SIX read-arm host kills in `dev_sgi_re.c`, and whether the scope split is right

**Tree under review: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\src\`.  IGNORE ANY OTHER `src/`
YOU FIND UNDER THE PROJECT ROOT — there are three pristine-2021-upstream copies there, and a
seat that reads one reports line numbers off by hundreds and arms whose existence differs.
If your line numbers disagree with mine by more than a few, you are in the wrong tree; say so.**

**THIS IS A READ-ONLY AUDIT.  Do not build, do not run the emulator, do not write to any
tree.** Another seat is running a kill table right now and its oracles are wall-clock
sensitive; a concurrent build would corrupt its measurement, not just slow it. Reading and
grepping are free. If you think a question needs a measurement, say which measurement and why
— naming it is the deliverable, not running it.

## Please do not simply ratify

A recent panel had seven of nine seats confirm a premise this project's brief stated wrongly,
and **today the main loop asserted a census that was wrong twice over** — `grep -c 'exit(1)'`
counted commented-out exits as live, and `DEVICE_ACCESS(...)` heads were used as function
boundaries when three plain functions sit between them. **Check the premises, not just the
derivations.** I have marked mine as questions where they are cheap to check.

## Context, inlined

`src/devices/dev_sgi_re.c` models the SGI IP32 "CRIME" rendering engine. `DEVICE_ACCESS(sgi_re)`
spans lines **221–384**. It dispatches on six address windows: `CRIME_RE_TLB_A`, `_TLB_B`,
`_TLB_C`, `_TEX`, `_LINEAR_A`, `_LINEAR_B`. Each window has this shape:

```c
} else if (relative_addr >= CRIME_RE_TLB_B && relative_addr < CRIME_RE_TLB_C) {
        if (len != 8) {
                fatal("TODO: unimplemented len=%i for CRIME_RE_TLB_B\n", len);
                exit(1);                       /* <- WIDTH KILL   (round #497, in flight) */
        }

        if (writeflag == MEM_WRITE) {
                int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;
                for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
                        d->re_tlb_b[tlbi] = data[hwi]*256 + data[hwi+1];
                        debug("d->re_tlb_b[%i] = 0x%04x\n", tlbi, d->re_tlb_b[tlbi]);
                        tlbi++;
                }
        } else {
                fatal("TODO: read from CRIME_RE_TLB_B\n");
                exit(1);                       /* <- READ KILL    (filed as sgirekills)   */
        }
```

**MY CENSUS — derived, and I want it checked because I already got it wrong once today.**
Live `exit(1)` = an `exit(1)` whose stripped source line does not begin `//`. Four are
commented out (143, 152, 473, 965). Attributing each to the nearest preceding line matching
`^[A-Za-z].*(` without a `;`:

| function | span | live exits |
|---|---|---|
| `DEVICE_ACCESS(sgi_re)` | 221–384 | **13** |
| `do_mte_transfer` | 940–1140 | 5 |
| `draw_primitive` | 408–660 | 1 |
| `DEVICE_ACCESS(sgi_de)` | 661–922 | 1 |
| `DEVICE_ACCESS(sgi_mte)` | 1141–1276 | 1 |
| **file total** | | **21** |

And `sgi_re`'s 13 decompose as **6 WIDTH kills** (233, 250, 267, 284, 301, 351), **6 READ
kills** (245, 262, 279, 296, 346, 362), **1 other** (372) — *exactly one width kill and one
read kill per window, six windows, plus one straggler.*

**Q0. Is that decomposition right?** It is load-bearing for everything below, and it is a
premise, not a derivation.

## The questions

**Q1 — REACHABILITY, and this is the one that matters most.** Is each of the six read kills
reachable by an ordinary guest load on an unmodified in-tree machine? The machine is
`-E sgi -e ip32`; `dev_sgi_re_init` is at line 385 and the base address is passed there.
**Give me the guest virtual address of each of the six windows**, derived from the base and
the `CRIME_RE_*` constants (grep the header for them), so a probe author can write the rows
without re-deriving. If any window is NOT reachable — masked by an earlier `else if`, outside
the registered range, shadowed by another device — say which and why, because that would
change the severity.

**Q2 — THE SCOPE SPLIT.** Round `#497` fixes the six WIDTH kills. The six READ kills are filed
separately as `sgirekills`. The width guard is evaluated FIRST, so after `#497` a 4-byte read
declines safely while an **8-byte read still ends the host process**. Is splitting these into
two rounds correct, or is it one defect cut in half? The argument for splitting: different
predicates, different fix shapes, and the read arms need a decision about what value to return
that the width arms do not. The argument against: the round record will say "the width kills
are fixed" while the same window stays lethal by another door, and a reader could reasonably
conclude reads were made safe. **I want your view, and the reason, not a vote.**

**Q3 — WHAT SHOULD A READ RETURN?** The project's de-fatalisation option set has four members:
delete / decline / decline + bounded-announce / **ACCEPT** (where the model already computes
the right answer and merely discards it). For each of the six read arms, which member applies?
Specifically: **is the data the guest would want actually present in the struct?** `re_tlb_a`,
`re_tlb_b`, `re_tlb_c`, `re_tex`, `re_linear_a`, `re_linear_b` are all written by the store
path — so a read could plausibly return what was written, which would be ACCEPT, not decline.
Check whether that is true for each, because if it is, this round is much smaller than it looks.

**Q4 — THE HOUSE IDIOM.** If any arm needs an announce, the fork's idiom is `N = 1` per device
instance plus an explicit marker in the message text, and the plurality spelling is `(once)`
(9 of 14 sites; `(further occurrences suppressed)` 3, `(reported once)` 2). Confirm the latch
field would go in `struct sgi_re_data` and that **one malloc serves all four handlers**
(`sgi_re`, `sgi_de`, `sgi_mte`, `sgi_de_status`) — which matters because a shared struct means
`#497`'s latch infrastructure is already reachable from here.

**Q5 — THE SEVENTH SITE.** `DEVICE_ACCESS(sgi_de)` has its own width kill at line 694, accept
set `{4, 8}`, so `len` in `{1,2,3,5,6,7}` ends the host — one guest `sb`. It is filed as
`sgidewidth` and deliberately excluded from `#497` (different handler, different accept set,
and its registers are READABLE so its rows read back through `odata` rather than through debug
lines). **Confirm or refute that exclusion**, and tell me whether `sgi_de`'s read path has the
same problem as `sgi_re`'s or whether it genuinely serves reads.

## Output

**VERDICT LINE FIRST** so the answer survives truncation. Then Q0–Q5 in order, each with
file:line evidence you have actually read. Where you cannot settle something from the source,
say so plainly — an honest UNKNOWN outranks a confident guess here, and this project has been
burned by both a stale tree and a confident census in the last twelve hours.
