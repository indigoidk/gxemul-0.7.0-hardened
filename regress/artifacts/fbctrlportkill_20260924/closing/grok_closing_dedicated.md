You are the DEDICATED adversarial reviewer (a separate job from the panel's grok seat) for a C hardware-emulator
correction, GXemul #549, before it is committed.  Read-only review.

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\closing\closing_brief.md` first -- it
inlines the repair diff (the probe grew from 41 to 73 rows after the F2 adjudication), the 62-variant table (54 red, the
8 disclosed at 73/73), and the gate test.  The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.

FIRST LINE: `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.  Push hard; an edit already in
the table is worth nothing.  Your job, and only this:
1. Edits to `src/devices/dev_fbctrl.c` NOT in the table that break the intended behaviour (refuse >= 8 on the full 64-bit
   value, keep the previous selector, announce once per device, keep the DATA check) and still score 73/73.  Give exact
   tokens and the row you expect to stay green.  Consider the PORT read path, odata, widths, the latch's interaction with
   fbctrl_command() and the DATA arm, and state that persists across the refusal.
2. Rows in the new probe that are vacuous by construction (the observable cannot differ under the edit they name).
3. Any sentence the repair adds that is false, or true only for the case measured.
Settle by reading the files and by arithmetic; say plainly which findings are readings.  No files may be changed.
