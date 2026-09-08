# sgirandomcolour -- design pass 1: what should a DECLINED buffer fill leave behind?

**Everything you need is in this packet. Do not plan to read files.** Several seats here cannot
open the repository at all; the facts below are inlined for that reason and are quoted from
`GXEMUL-SEC/src/devices/dev_sgi_re.c` at HEAD plus this round's uncommitted working set.

**VERDICT LINE FIRST**, please -- one line at the top saying what you would do, so it survives
truncation.

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise the brief
stated wrongly, and a later one refuted four of my premises when asked to. **Check the premises, not
just the derivations.** If a premise below cannot be settled from this packet alone, say so plainly
rather than assuming it -- an honest "not checkable from here" is the answer I want.

## 1. THE CODE

`horrible_getputpixel()` writes one pixel into a tile. On a PUT it packs bytes into a local buffer
and hands them to memory:

    uint8_t buf[8];             /* #100: bufdepth can be 8 = 1<<((mode>>8)&3) */
    if (put) {
            switch (color_mode) {
            case DE_MODE_TYPE_CI:                        /* 0x00 */
                    buf[0] = *color;
                    break;
            case DE_MODE_TYPE_RGB:                       /* 0x10 */
                    buf[0] = *color >> 24;  buf[1] = *color >> 16;
                    buf[2] = *color >> 8;   buf[3] = 0;
                    break;
            case DE_MODE_TYPE_RGBA:                      /* 0x20 */
                    buf[0] = *color >> 24;  buf[1] = *color >> 16;
                    buf[2] = *color >> 8;   buf[3] = *color;
                    break;
            case DE_MODE_TYPE_ABGR:                      /* 0x30 */
                    buf[0] = *color;        buf[1] = *color >> 8;
                    buf[2] = *color >> 16;  buf[3] = *color >> 24;
                    break;
            default:buf[0] = random();
                    buf[1] = random();
                    buf[2] = random();
                    buf[3] = random();
                    // TODO.
                    fatal("[ put: color mode = 0x%x ]\n", color_mode);
            }

            cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
                buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
    } else {
            ... GET side, not the subject of this round ...
    }

`buf` is a plain automatic array and **is never initialised**. `bufdepth = 1 << ((mode >> 8) & 3)`,
so it is 1, 2, 4 or 8 and the GUEST chooses it. `color_mode = mode & DE_MODE_TYPE_MASK`.

## 2. SETTLED PREMISES -- stated so you need not re-derive them; challenge any that look wrong

* `crmfbreg.h` defines **`DE_MODE_TYPE_MASK 0x000000f0`** and five types:
  `CI 0x00`, `RGB 0x10`, `RGBA 0x20`, `ABGR 0x30`, **`YCRCB 0xf0`**.
* `grep -c YCRCB` over the device file is **0** -- YCRCB is handled nowhere, so a documented mode
  lands on the `default:` arm.
* the mask admits **16** values (0x00, 0x10 ... 0xf0). Four are implemented. **So 12 of the 16 reach
  the random arm, one of which (`0xf0`) is documented.** *I derived this from the mask; please check
  the arithmetic and the claim.*
* the sibling defect `sgirebufuninit` is **already filed separately**: no colour arm writes
  `buf[4..7]`, and `CI` writes only `buf[0]`, so when `bufdepth` exceeds the bytes an arm sets, the
  write sends uninitialised host stack into guest memory. **That row exists; this brief is not asking
  you to re-find it** -- but see question Q3, where it collides with this fix.
* `random()` here is the C library PRNG, not a hardware entropy source.

## 3. THE PRECEDENT IN THIS SAME FUNCTION -- round `#504`, already shipped

A different `default:` arm in the *same helper* had the identical shape and was fixed. Its comment
now reads, in part:

> *"this arm used to assign `*color = random()` ... so a failed GET handed the CALLER a random value,
> and `draw_primitive()` then wrote it to the destination in the same loop iteration ... MEASURED,
> rung 3: the destination received 0x4b1763a1, 0x2ee4b4df and 0x7433cdc1 on successive runs.*
> *NOW DECLINED: `*color` is left alone, so the caller's own `uint32_t color = fg` stands and what
> lands is at least DETERMINISTIC. The announce is latched because this helper is per-pixel."*

The shipped disposition there was **decline + latched announce**, leaving the caller's variable
untouched, using a `d->warned` latch bit.

## 4. THE DESIGN SPACE -- the project's standing option set

Seven members, and a round is expected to say why it picked one:
**1 DELETE · 2 DECLINE (silent) · 3 DECLINE + BOUNDED/LATCHED ANNOUNCE · 4 ACCEPT (the model already
computes the right value) · 5 FAULT (model the space as unmapped) · 6 BACKED ACCEPT (invent storage)
· 7 IMPLEMENT (write the code).**

## 5. QUESTIONS

**Q1. Which member, and what does the buffer contain afterwards?** This is the question the row was
filed on and it is NOT the same as `#504`'s. There the fix left a CALLER's variable alone and the
caller's own initialised value stood. **Here the thing left alone is `buf`, which is uninitialised**
-- so "leave it alone" writes host stack rather than noise, which is arguably worse. Candidates I can
see, and I want them ranked with reasons:

  * **(a) zero-fill `buf` and let the write proceed** -- deterministic, but publishes a colour the
    guest never asked for;
  * **(b) skip the `memory_rw` entirely for a declined mode** -- nothing is written, but this needs
    control flow, not just a different fill;
  * **(c) leave `buf` untouched** -- *rejected by me as strictly worse; tell me if I am wrong*;
  * **(d) something else.**

**Q2. If you pick (b), what is the exact control flow?** *** CAUTION, and this is a real failure this
project has recorded: on an earlier round FOUR independent readers proposed an early `return` into a
function whose common tail did necessary work, and none of them looked nine lines down. *** Here the
`memory_rw` is followed by the end of the `if (put)` branch and then the function's `else` for GET.
**If you propose skipping the write, say exactly which statement is skipped and what the function
does afterwards** -- and if you cannot see enough of the function from this packet to be sure, say
that instead of guessing.

**Q3. ROUND SCOPE: is this one round with `sgirebufuninit`, or two?** They are in the same switch. A
zero-fill of `buf` at its declaration would arguably fix both at once. The project's rule is: a round
takes ONE site; a second joins only if it is the same semantic class, covered by ONE fix design and
ONE detector with no new oracle. **More findings create more candidate rounds, never bigger rounds.**
Argue it either way, but name the ONE oracle if you say one round.

**Q4. What is the detector, and what is the smallest edit that defeats it?** The oracle cannot be
"the value is not random" -- a single run cannot distinguish a fixed value from a lucky draw. It also
must not be satisfiable by a mutant that keeps the guard and nulls its effect. Name a channel, and
name the mutant you would build to try to escape it.

**Q5. Is there a WITNESS?** The ladder wants a real guest instruction through real device dispatch on
an unmodified in-tree machine, red before the fix and green after with the SAME script, plus a
liveness control. `#504`'s witness drove an XFER copy through this helper on `-E sgi -e ip32` and
observed the destination bytes. Does the PUT path admit the same shape, or does the guest need to
select a colour mode that the surrounding code rejects earlier? **If you think no witness is
constructible, say why** -- that is a real answer and the round would then be documented-only.
