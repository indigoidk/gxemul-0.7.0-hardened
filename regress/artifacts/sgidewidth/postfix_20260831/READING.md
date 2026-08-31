# Reading the post-fix witness run: 11/22 is the RIGHT answer, and the reds split two ways

This is the SAME frozen witness that scored its kill rows 4/4 on the committed build, re-run
against the #498 binary.  **A witness pins the DEFECT, so post-fix it MUST go red on those
rows.**  Same script, opposite colour — which is test-first itself, restated per-probe.

## Group 1 — EIGHT rows inverted because the fix works

    w1_sb_msg    got=0                want=1                 the width-kill message is gone
    w1_sb_die    got=('running',None) want=('exit',1)        the host now survives
    w2_sh_*, w1_lbu_*, w2_lhu_*   ditto

Four access forms, message and survival each, all four kills removed.  These reds are the
deliverable.

## Group 2 — THREE rows that expect survival and still exit, and they are NOT this fix

    ldl_ffd_alive   got=('exit',1)  want=('running',None)
    ldr_ffd_alive   got=('exit',1)  want=('running',None)
    w8_end_ok       got=('exit',1)  want=('running',None)    "aligned sd at +0xff8 is len=8,
                                                              ACCEPTED, no truncation"

All three touch offsets with bit 0x800 set, so the handler's tail runs `draw_primitive()`, whose
`default:` arm ends the host on 254 of 256 ops — including the reset value.  **That is
`sgideprimop`, a separate filed HIGH row, and the measuring seat predicted this exact outcome:
"a correct fix cannot make the upper half survive, because the second kill is not this row's."**

Note `w8_end_ok` uses an ACCEPTED width (len=8).  It never reached the width guard at all, before
or after.  Its red is pure `sgideprimop`.

## Rows that stayed green and carry the attribution

    ld_ffd_adel     COP0 Cause.ExcCode == 4 — the alignment exception fires BEFORE memory_rw,
                    which is the measurement that retracted this round's own severity claim
    draw_op0_msg    the SECOND kill, on an ACCEPTED width, with no width defect involved
    draw_op0_die    ditto

## What this run does NOT establish

It is a WITNESS, not a detector.  It cannot tell a correct fix from a fix that also broke
something the witness never probed.  **The round still owes a DETECTOR** — rows that fail on a
mutant of the shipped repair — per the vacuity floor.  Until that exists this fix is not
shippable, however green the witness looks.
