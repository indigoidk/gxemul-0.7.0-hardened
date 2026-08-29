# `idesync` — ASSESSED, NOT CHANGED.  Verified at HEAD 2026-08-29.

**This is the record the row owes** (*"one honest 'assessed, not changed' record naming the
IDENTIFY-word reason"*).  Reading only — no build, no probe, no edit.

> ### *** THE FIRST DRAFT OF THIS FILE SHIPPED A REFUTED CLAIM AND AN IMPOSSIBLE APPARATUS
> ### RESULT.  Both are corrected below and the correction is kept in place, not silently
> ### swapped.  Caught by an adjudicating seat before anything was staged. ***
>
> It said: *"No FLUSH constant exists in this tree's ATA headers — every `FLUSH` hit under
> `src/include/` is unrelated."*  **FALSE.**  `src/include/thirdparty/wdcreg.h:130` is
> `#define WDCC_FLUSHCACHE 0xe7 /* Flush cache */`.
>
> **And the recorded evidence could not have produced the recorded conclusion.**  I ran
> `grep -rn 'FLUSH' src/include/ | head -6` — there are **46** hits — and read a TRUNCATION as
> an ABSENCE, under a label that said "blank = the constant does not exist" while the output
> was not blank.  *That is the apparatus-failure class this very file warns about, committed in
> the file that warns about it.*
>
> **Three siblings already held the right answer** and none was consulted: this row's own
> CONFIRMED research entry of 2026-08-19 (*"0xE7 WDCC_FLUSHCACHE is DEFINED at wdcreg.h:130 and
> NEVER REFERENCED in dev_wdc.c"*), `OUTSTANDING_BUGS.md` at the same fact, and the header.

## 1. THE MEASURED NEGATIVE CONTROL — this is the primary warrant, and the first draft buried it

The row's research entry (2026-08-19) put **OpenBSD 7.6 through a full filesystem lifecycle**
and censused the ATA commands actually issued:

    0xEC 0xF5 0x10 0x91 0xC6 0x20 0xC4 0x30 0xC5 0xE0        -- no 0xE7, no 0xEA

**And it ran the discriminating experiment:** with IDENTIFY word 83 forced to `0x5000` /
`0x7000`, the guest **demonstrably read the new block** (it began issuing `0xEF`) **and STILL
never flushed.**

> **SO THE ADVERTISE-FACT IS NOT THE DEMONSTRATED CAUSE.**  opus5's review explicitly demoted
> it: why OpenBSD declines to flush *"remains an honest UNKNOWN."*  The first draft of this file
> re-derived a compressed one-clause version of that review and presented the IDENTIFY reason as
> *"the whole content of the disposition"*, which inverts the warrant hierarchy.  The
> measurement is the warrant; the IDENTIFY fact is what a **conforming** guest is *entitled* to
> conclude.

## 2. THE IDENTIFY-WORD REASON — correct, with its qualifier restored

`wdc_initialize_identify_struct()` memsets the 512-byte struct to zero, then writes at
**18 SITES — not 18 words.**  Three are `memcpy`s spanning ranges:

    :349   memcpy(&identify_struct[2 * 10], "#0                  ", 20)   -> words 10-19
    :352   memcpy(&identify_struct[2 * 23], "1.0     ",             8)   -> words 23-26
    :364   memcpy(&identify_struct[2 * 27], namebuf,               40)   -> words 27-46

So roughly 49 words are written, not 18.  **The load-bearing fact is unaffected and is better
stated as a ceiling: the highest word touched is 68** (derived, not transcribed:
`grep -oE 'identify_struct\[2 \* [0-9]+' | sort -n | tail -1`).  Words 82-87 therefore keep the
memset's zero.

FLUSH CACHE support is **word 83 bit 12**, enabled is **word 86 bit 12**.  *Warrant named
rather than asserted: there is no ATA document in `_scratchpad/` — the `#485` comment in
`dev_wdc.c` says so plainly — so this comes from the NetBSD convention (`ATA_CMD2_FC` = 0x1000)
and is corroborated in-row by the 0x5000/0x7000 variants, whose bit 14 is the validity bit.*

**A stronger form of the same conclusion:** word 83 = `0x0000` also fails the bits 15:14 = 01b
validity signature, so a conforming host discards the whole word — the drive advertises **no
valid command-set information at all**, rather than merely a cleared flush bit.

## 3. THE COMMAND IS DEFINED AND UNREFERENCED — which is stronger than "absent"

    grep -n WDCC_FLUSHCACHE src/include/thirdparty/wdcreg.h   -> :130, 0xe7
    grep -c WDCC_FLUSHCACHE src/devices/dev_wdc.c             -> 0

**0xE7 falls to `default:` BY CONSTRUCTION**, which is a sharper claim than the false one it
replaces.  `0xEA` (FLUSH CACHE EXT) has no constant anywhere under `src/` and is in scope here
too — the 2026-08-19 research covered both, and the first draft's scope line covered only 0xE7.

Command dispatch is **20 case labels**: 16 `case WDCC_*`, 3 `case ATAPI_*`, **plus
`case SET_FEATURES:`** (0xEF, at `:847`) — defined in `wdcreg.h` *without* the `WDCC_` prefix,
so a prefix-keyed grep cannot see it.  *The first draft's "16 + 3" claimed completeness from an
instrument blind to unprefixed members.*  None of the 20 is a flush.

## 4. WHAT A NON-CONFORMING GUEST GETS: an honest abort, AND it is delivered

An unadvertised flush reaches `wdc_command()`'s `default:` arm, which carries **two** repairs,
both deliberately OUTSIDE the latch guard:

```c
	d->error |= WDCE_ABRT;        /*  #464  */
	d->int_assert = 1;            /*  #485  */
	if (!d->warned_unimpl_cmd) {
		d->warned_unimpl_cmd = 1;
		fatal("[ wdc: WARNING! Unimplemented command 0x%02x ... ]\n", ...);
	}
```

`#464` put the ABORT BIT outside the guard (inside it, the *second* unimplemented command
silently SUCCEEDS, because `wdc_command()` re-clears `d->error` per command).  **`#485` did the
same for the interrupt — and without it the abort was POLLING-ONLY**: an interrupt-driven guest
saw nothing at all.  The first draft cited only `#464` and so claimed an abort that, three days
earlier, would not have been delivered.

## 5. THE POLARITY CONTRAST — true at arm level, and it MUST NOT travel unqualified

IDE's `default:` aborts honestly.  SCSI's top-level `default:`
(`src/disk/diskimage_scsicmd.c`) calls neither status helper and falls to `return 1`, so an
unknown SCSI command is reported to the guest as SUCCESS (`b120u`).

> *** BUT `dev_wdc.c:1515` ROUTES ATAPI PACKET COMMANDS INTO `diskimage_scsicommand()`, AND
> dev_wdc TREATS `res == 1` AS SUCCESS. ***  So an unknown **packet** command on an IDE ATAPI
> drive lands in the b120u arm and takes the SUCCESS polarity — **through the wdc device.**
> One device, both polarities, selected by path.

**Deliberately NOT minted as a carrier line.**  It is an instance-pair, not a rule, and the
qualifier it requires makes it a paragraph; an unqualified line would itself be the
dropped-qualifier class the carrier already documents.  It lands here and as a cross-reference
on `b120u`, whose fixer gains a second reachability route.

*The "only one of ~30 arms" figure in my earlier `b120u` note is UNDERIVED — a direct count
gives 22 top-level `case` labels plus `default:`.  What I verified is narrower: the default arm
calls neither helper, and the helper call sites are distributed across the others.  The strict
"only" must rest on `b120u`'s own arm-by-arm census, cited, not on my count.*

## 6. DISPOSITION

**ASSESSED, NOT CHANGED.**  Measured non-issuance across a full lifecycle; the constant defined
but unreferenced so 0xE7 cannot be handled; nothing advertised; and an honest, delivered abort
if issued regardless.

**Witness:** `none` — *a non-event admits no rung-3/4 witness, a ceiling four seat entries
already record; the non-issuance claim itself is carried by the measured lifecycle census of
2026-08-19.*  That is the honest form: the 2026-08-27 ask-one-seat ruling is satisfied in
substance, because the attempt question was answered in-row by measurement rather than skipped.

**Scope:** this claims only that 0xE7/0xEA cannot produce a false durability promise on this
drive.  It does NOT claim IDE durability is correct in general; `ovsync` separately carries
SYNCHRONIZE CACHE(16), a different opcode on a different path.

*Not closed — closure owes the stage coverage the full-panel directive mandates.*
