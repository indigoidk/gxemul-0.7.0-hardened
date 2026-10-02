# PREDICT.md -- Opus pass-1 seat, #529 repair 14 brief.  WRITTEN BEFORE ANY BUILD.
# Instrument: the SHIPPED 188-row probe, GXEMUL-SEC/regress/crime_width_probe.py, frozen once.
# Clone: /tmp/gxopus_r14 (cp -a of /tmp/gxopusc8, cmp-clean vs SEC, binary -nt source at 22:46).

base            188/188   CRIMEP_CONTROL=OK.  Harness validation.

PC_imk4r        187/188   POSITIVE CONTROL, close-8's already-built G_clr_imk4r binary re-run under MY
                          driver.  Expect the SAME score and the SAME failing row (`gate line') as
                          close-8's table A.  If it disagrees, my harness is wrong, not the mutant.

M1_gotolatch    KILLED, and I expect `sh08b run' to be the reddening row.
                THE EDIT: `goto crime_declined;' MOVED INSIDE the latch block (one line, moved up one
                line).  Effect: the FIRST refusal in a session declines correctly; EVERY LATER ONE
                falls through into the register switch, SILENTLY (the latch suppresses the announce).
                WHY I EXPECT A KILL: session `sh08b' (probe :620-635) issues FOUR refused halfword
                writes at CRIME_CONTROL before any other refusal -- 0x0201, 0x0900, 0x0a00, 0xffff.
                The FIRST (0x0201) still declines; the SECOND (0x0900) reaches the CONTROL arm with
                idata & CRIME_CONTROL_HARD_RESET (0x0800) SET, so every CPU stops and the session's
                RAM round-trip never runs -> `sh08b run' reds.  `sh08b msg' may move too.
                WHAT A KILL WOULD MEAN: the decline-side latch cell is OCCUPIED, but by the INCIDENTAL
                structure of a multi-refusal session rather than by any named row -- the
                "pinned where a row happens to touch it" class.
                WHAT AN ESCAPE WOULD MEAN: a floor cell the 56-cell enumeration does not contain at
                all, because the enumeration is the ACCEPT half of a 112-cell space.

M2_ld278clr     188/188 ESCAPE.  A silent latch-CLEAR bypass at ACCEPTS entry 46:
                `relative_addr == 0x278 && len == 8 && writeflag == MEM_READ && !(d->warned & CRIME_W_LEN)'
                -> goto crime_declined, inserted BEFORE the width test (the G-form, no announce).
                WARRANT FOR THE PREDICTION, derived not guessed: buckets8.py (close-8's own script,
                re-run by me today, sentinel BUCKETS8_DONE) reports N_PRE_BLIND=8 and entry 46
                `ld +0x278 DFL' is one of the eight -- its ONLY pre-latch driver is session 40
                (`latch x5'), whose three rows (`latch x5' an announce count, `latch surv' a RAM trip,
                `latch said' the announce text) are all blind to a silent decline.
                GUEST-VISIBLE: reg[0x278/8] = reg[79] is NOT rewritten by the prelude (:229-273 touches
                reg[0], reg[1], reg[2] and reg[65..72] only), so a seeded value persists and a declined
                8R answers 0 instead of it.
                WHY IT MATTERS: the brief's P5 names FOUR escapes and entry 46 is not among them.
