These are copied from the VOLATILE path _scratchpad/panel_20260907_170713/, because
README.txt cites them and /tmp-style paths evaporate.  pass1_brief_sent_20260907.md is
the brief the #509 pass-1 panel ACTUALLY received; it is NOT the same file as
../PASS1_brief.md, which does not contain the 'Proposed additional rows' table.

grep -c 'fill b top':
  pass1_brief_sent_20260907.md               1
  ../PASS1_brief.md                          0

the proposed-rows table, verbatim:
  338:**Proposed additional rows:**
  339-
  340-| row | shape | what it pins |
  341-|---|---|---|
  342-| `copy top` | TLB_A, depth 32, copy ON, source pixel holds `aa bb cc dd` | that the two `|=` assignments move TOGETHER |
  343-| `fill b top` | TLB_B, depth 32, fill | the label axis |
