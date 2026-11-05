# ERRATA to PRETABLE_2.out -- dated 2026-11-05 (repair 3; codex GPT-6 Astra pass 3, records c and e)

PRETABLE_2.out is a measurement-time record and is NOT rewritten.  Two of its sentences are wrong; each is quoted, then corrected.

## c. The mtime claim (line 1-2)

> "Written BEFORE table 2 runs (its mtime precedes every file in table2/)."

**False as worded.**  `table2/probe68_frozen.py` is OLDER: 2026-11-05 00:37:14.426 against PRETABLE_2.out's 00:37:14.520 (`ls
--time-style=full-iso`), because the frozen probe was copied first, as `table2/VERDICT.md` itself says ("the only older file here is the
frozen probe, copied first").  **What holds:** PRETABLE_2.out precedes every file the table-2 DRIVER wrote -- `table2/MD5.txt` 00:37:24,
`build_base.log` 00:37:26, the first score at 00:38:57 (`TABLE.log`) -- so the order discriminator holds for the driver and its
results, with the frozen-probe exception.  The predictions are unaffected.

## e. Y2's reason (the Y2s_simple_ltm1 and Y2t_tex_ltm1 lines)

> "y = -1 admitted: the colour store lands before the frame (a negative VRAM offset when FB_RENDER_ADDR1 < 1280) ..."

**Overbroad.**  At y = -1 the TOP triangle draws columns 274..325 (row -1 spans 274.17..325.83).  Their depth indices are x - 640 =
-366..-315 (before vram_z, whatever the frame base); their colour bytes are fb_base + 2 * (x - 640) = fb_base - 732 .. fb_base - 629.
Those are negative only for fb_base below 630..732, not below 1280: at fb_base = 1000 they are 268..371, inside VRAM (one row's worth
before the frame).  **For the probe -- which never writes FB_RENDER_ADDR1, so fb_base is 0 -- the colour bytes ARE negative (before VRAM
itself) and the depth read is before vram_z**, so the conclusion stands: undefined behaviour, NOT PREDICTED.  Only the stated condition
was too wide.

## Not in this file

Codex's records a ("59 red, every one on its predicted rows"), b ("fifteen render sessions") and d ("the three sibling exits in the same
function") live in the probe docstring and in gate_arm.sh's pvr comment, and are corrected there (repair 3; the gate text in
`../r3_20261105/gate_pvr_block.new`).  The STDIN CAP that every table-2 leg met is recorded in `table2/VERDICT.errata.md`.
