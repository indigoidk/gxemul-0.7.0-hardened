"""#480 Q4: name the three call-site rows in gate_offline.sh.

The round FIRST DECLINED to do this, on the ADDITION LICENCE -- the detector's own
identity row already reds the gate on a deletion, so naming would guard a shut door.

TWO SEATS REFUTED THAT BY DIFFERENT ROUTES AND BOTH WERE THEN MEASURED:

  D1_renumber      (kimi-k3:cloud)  delete the call AND renumber the pin in one edit
                   -> 82 rows, 0 failures, WDC_IDENTIFY_PASS
  D2_rowsplusplus  (codex)          replace the call with `rows ++;`
                   -> 83 rows, 0 failures, WDC_IDENTIFY_PASS   <- no renumber at all

So the pin binds the row COUNT, not row IDENTITY.  The addition now has a measured
delta, which is what licenses it.

BS = chr(92): a backslash that must survive into the file is built by concatenation,
never written as a literal in a heredoc -- this script exists because doing the latter
failed twice in one session.
"""
import io

NL, BS = chr(10), chr(92)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\gate_offline.sh"
s = io.open(P, encoding="utf-8", newline="").read()

IND, CONT = " " * 4, " " * 14
anchor = (IND + 'check     "wdc IDENTIFY: the packing anchor is present" ' + BS + NL +
          CONT + '"$(grep -c ' + chr(39) + 'packing anchor' + chr(39) +
          ' "$WDCLOG")" "1"' + NL)
assert s.count(anchor) == 1, "anchor occurs %d times" % s.count(anchor)
assert "the same-opcode reissue row is present" not in s, "already applied"


def row(label, token):
    return (IND + 'check     "wdc IDENTIFY: ' + label + '" ' + BS + NL +
            CONT + '"$(grep -c ' + chr(39) + token + chr(39) + ' "$WDCLOG")" "1"' + NL)


COMMENT = (
    IND + "#  #480: THE THREE CALL-SITE ROWS ARE NAMED, BECAUSE THE COUNT PIN IS NOT ENOUGH." + NL +
    IND + "#" + NL +
    IND + "#  This round first DECLINED to name them, reasoning that the detector's own identity" + NL +
    IND + "#  row (`if (rows != 85)`) already reds the gate on any deletion, so naming would guard" + NL +
    IND + "#  a shut door -- which the ADDITION LICENCE refuses.  TWO SEATS REFUTED THAT BY" + NL +
    IND + "#  DIFFERENT ROUTES, and both refutations were then MEASURED:" + NL +
    IND + "#" + NL +
    IND + "#    D1_renumber      delete the call AND renumber the pin in the same edit" + NL +
    IND + "#                     -> 82 rows, 0 failures, WDC_IDENTIFY_PASS" + NL +
    IND + "#    D2_rowsplusplus  replace `row_rejected_cmd_resets();` with `rows ++;`" + NL +
    IND + "#                     -> 83 rows, 0 failures, WDC_IDENTIFY_PASS  <- no renumber at all" + NL +
    IND + "#" + NL +
    IND + "#  So the count pin binds the row COUNT and not row IDENTITY, and the SOLE CARRIER for" + NL +
    IND + "#  M4_afterguard could have been removed with this gate staying green.  These three" + NL +
    IND + "#  checks close exactly that mode." + NL +
    IND + "#" + NL +
    IND + "#  WHAT THEY DO NOT CLOSE, stated because a guard whose scope is overclaimed is worse" + NL +
    IND + "#  than none: an oracle WEAKENED while keeping its label.  `rows` stays right, the" + NL +
    IND + "#  label still prints, and these greps still pass.  That remains kill-table territory." + NL)

NEW = (anchor + NL + COMMENT +
       row("the same-opcode reissue row is present",
           "a same-opcode reissue resets the ring") +
       row("the rejected-command row is present",
           "a rejected command still resets") +
       row("the refill-command row is present",
           "a refill command starts from empty"))

io.open(P, "w", encoding="utf-8", newline="").write(s.replace(anchor, NEW, 1))
print("  gate_offline.sh: three named row checks added")
