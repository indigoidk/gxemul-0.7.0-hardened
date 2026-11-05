Replication readings of the two cloud seats on the same pass-2 packet (`RemoteTrigger run`, same prompt; badge s -- same-model replication,
never a second family).  Banked verbatim at p2_20261105/FABLE_r2.md and OPUS_r2.md.  Both: REPAIR-NEEDED on the detector only, the fix right.

REPEATS (no new disposition): Fable r2's F1 (y bounds) is P1 and F2 (span end) is P2; its one false record is P7 (the banner).  Opus r2's
G1-G4 are P1, G5-G6 are P2, G7-G8 (the render-mode exit at 1088 and the fb_base guard at 1158-1159: "the bound as written includes them ...
it may already be covered by #119's own gate rows") are P5's disclosure; its F1 is P7, F2 is P12 and F4 is P9.

ROW-GEOMETRY ALTERNATIVES offered for the class closure (the base run settles the exact pixels either way): Fable r2 -- BOTTOM
(260,450) (380,450) (320,510) with `b in` (320,479) and `b out` (320,480) at linear VRAM 2*(480*640+320) = 0x96280, outside the memset
frame; Opus r2 -- a triangle with a VERTICAL right edge at x = 300.0, reading (300, y) drawn and (301, y) background, "first confirm the
rasterizer's integer x2 on the base build".

P22 (Opus r2 F3) NEW, a wrong count in PRETABLE addendum 7(d): it says "eight of its thirteen 'controls' sit in Z-off sessions".  NINE do --
`zoff rendered` sits in the zoff session too; eight are moved by B1, and `zoff rendered` survives because the debug line prints before the
exit (which is why 7(d) could keep it a control).  MINE: ACCEPT, an errata line beside the frozen PRETABLE (the conclusion -- which rows are
controls -- is unchanged and measured: CONTROL=OK on every variant).
