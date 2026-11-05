# PRETABLE_3.out -- erratum (2026-11-05, main loop, from table 3's own check)

CORRECTS line 138: `Vt_swap_nov  exactly: texramp_l_end`.
The measured red set is `texramp_l_end, ztramp_l_end` (table3/SCORES.txt, table3/CHECK.txt `PRED=MISS Vt_swap_nov`).  The prediction
contradicted PRETABLE_3's own rule at line 7 -- a Z-off twin reds exactly when its Z-on row does, except under the variants that treat
Z-off drawing differently -- and Vt (a texture-coordinate swap deleted) is not such a variant: the wrong v reaches the sampled texel in
the Z-off ramp exactly as in the Z-on one.  So the correct prediction was both rows.  The variant is detected either way; no row changes.

# PRETABLE_3.out -- second erratum (2026-11-05, repair 4; codex pass 4 F8, upheld with the reason corrected by ../adj_p4_20261105/ADJ_MYTHOS_local.md section 3)

CORRECTS line 69's reason, not its class: `M17_reset_at_end  exactly: none -- GREEN (EQUIVALENT (table 1/2): no early exit after the
reset's old position; DEVINIT zeroes the field)`.
There IS one early exit after the reset's old position (dev_pvr.c:1137): the frame-outside-VRAM `return` at :1166.  (The RGB565 check's
exit at :1090 precedes the reset; the list-command exit at :1432 ends the process.)  M17 stays EQUIVALENT because that return comes
before every header of its render, and the field is zero there -- from DEVINIT, or from the previous render's end, where M17 now resets
it.  Table 3 measured M17 green, 128/128, as predicted.  The same false reason stood in the probe's docstring, corrected in place by
repair 4; table 1's VERDICT.md (../det_20261104/table1/VERDICT.md, line 13) carries it too and is outside repair 4's write scope.
