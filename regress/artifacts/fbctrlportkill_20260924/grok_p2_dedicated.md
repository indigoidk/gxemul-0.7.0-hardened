You are the DEDICATED adversarial reviewer (a separate job from the panel's grok seat) for a C hardware-emulator
correction, GXemul #549, before it is committed.  Read-only review.

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\p2_brief.md` first -- it inlines the
whole diff (dev_fbctrl.c, the new regress/fbctrl_port_probe.py, the gate-16 block, two pins and two manifest hunks) and
every measurement, including kill table 2 (25 variants of the fix, each scored by the 41-row detector).  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  You may also read table2/*.raw beside the brief.

FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.  Push hard; the table already
has 25 variants, so a finding that repeats one of them is worth nothing.  Your job, and only this:

1. Name edits to `src/devices/dev_fbctrl.c` NOT in table 2 that break the intended behaviour (refuse >= 8 on the full
   64-bit value, keep the previous selector, announce once per device, keep the DATA check) and still score 41/41.
   Give exact tokens and the row you expect to stay green.  Consider the PORT READ path, odata, the struct field order,
   the memset, widths, and interactions with fbctrl_command().
2. Name edits to the PROBE or the gate-16 block that keep every pin green while the device is wrong -- or that make a
   correct device fail.
3. Find any sentence the diff adds that is false, or true only for the case measured.

Settle by reading the files and by arithmetic; say plainly which findings are readings.  No files may be changed.
