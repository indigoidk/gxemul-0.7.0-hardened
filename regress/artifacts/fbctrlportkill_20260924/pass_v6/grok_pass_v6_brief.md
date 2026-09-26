# DEDICATED ADVERSARIAL JOB -- #549 v6's own pass (read-only)

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\pass_v6\pass_v6_brief.md` in full --
the fbctrl port-selector probe after its repair (v6, 117 rows: session B refuses every single-bit value at each width),
with the fixed PORT arm, the probe diff, the gate-16 diff and a 297-edit variant table inlined.  The tree is
`GXEMUL-SEC/` only; the working tree now holds v6 (`regress/fbctrl_port_probe.py`, md5 a9a2be3d) and the fix
(`src/devices/dev_fbctrl.c`, md5 129694b8).

You are the ADVERSARY for the floor question, asked of the SHIPPED COMPOSITE: **the smallest edit of the fixed PORT arm
(`case DEV_FBCTRL_PORT:` in `src/devices/dev_fbctrl.c`) that scores the full 117 rows of v6 while it changes the
refusal's behaviour on some reachable guest write -- OUTSIDE the probe header's NOT CLAIMED (0)-(8).**  The last pass
found the compare narrowed to a bit range; v6's session B is meant to close every narrowing of the bits the compare
tests.  Attack what B does not see: joint cells of width and bit, the previous selector, the latch, values with more
than one bit set, the accept path, the read path.

For each candidate, name the rows that stay green and why, and whether it restores the DATA arm's range-check exit.
If none exists, list every shape you tried -- a zero needs its denominator.  Open with
`VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`.  Do not write any file.
