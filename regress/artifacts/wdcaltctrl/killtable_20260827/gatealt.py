"""Name the ALT-CTRL rows in gate_offline.sh, following #480's measured precedent.

#480 established the warrant by measurement rather than by preference: the detector's own
identity row binds the row COUNT, never row IDENTITY, so replacing a row's call with
`rows ++` keeps the count right, the verdict green and the gate passing while a SOLE
CARRIER disappears. Two seats found that independently and it was negative-controlled.

This round has TWO sole carriers -- Md_nohelper is caught only by the abort row, and
Md_widemask only by the nIEN row -- so the same argument applies with the same force.

BS = chr(92) throughout: a trailing backslash written literally into a heredoc'd python
string has failed three times in this session, and the carrier prescribes exactly this.
"""
import io

NL, BS = chr(10), chr(92)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\gate_offline.sh"
s = io.open(P, encoding="utf-8", newline="").read()

IND, CONT = " " * 4, " " * 14
anchor = (IND + 'check     "wdc IDENTIFY: the refill-command row is present" ' + BS + NL +
          CONT + '"$(grep -c ' + chr(39) + 'a refill command starts from empty' + chr(39) +
          ' "$WDCLOG")" "1"' + NL)
assert s.count(anchor) == 1, "anchor occurs %d times" % s.count(anchor)
assert "the SRST-is-a-reset row is present" not in s, "already applied"


def row(label, token):
    return (IND + 'check     "wdc IDENTIFY: ' + label + '" ' + BS + NL +
            CONT + '"$(grep -c ' + chr(39) + token + chr(39) + ' "$WDCLOG")" "1"' + NL)


COMMENT = (
 IND + "#  #481: the ALT-CTRL rows, named for the reason #480 MEASURED rather than assumed." + NL +
 IND + "#" + NL +
 IND + "#  The detector's identity row binds the row COUNT, never row IDENTITY: replacing a" + NL +
 IND + "#  row's call with `rows ++` keeps the count right, the verdict green and this gate" + NL +
 IND + "#  passing while a sole carrier vanishes.  Two seats found that independently on #480" + NL +
 IND + "#  and it was negative-controlled." + NL +
 IND + "#" + NL +
 IND + "#  THIS ROUND HAS TWO SOLE CARRIERS and they are the ones that matter most:" + NL +
 IND + "#    Md_nohelper (guard kept, abort removed)  -> only `an SRST aborts what was in" + NL +
 IND + "#                                                flight` reds" + NL +
 IND + "#    Md_widemask (mask widened to include IDS) -> only `an nIEN write is not a" + NL +
 IND + "#                                                reset` reds" + NL +
 IND + "#" + NL +
 IND + "#  Same honest scope as #480's block: naming closes DELETION and REPLACEMENT.  It" + NL +
 IND + "#  does NOT close an oracle weakened while keeping its label -- that stays kill-table" + NL +
 IND + "#  territory, and saying so is what keeps this guard from being overclaimed." + NL)

NEW = (anchor + NL + COMMENT +
       row("the SRST-is-a-reset row is present", "a real SRST (0x06) is a reset") +
       row("the routine-ctl row is present", "a routine 0x08 preserves the command") +
       row("the nIEN row is present", "an nIEN write is not a reset") +
       row("the SRST-abort row is present", "an SRST aborts what was in flight") +
       row("the SRST-signature accept row is present", "a real SRST still signs the CD-ROM"))

io.open(P, "w", encoding="utf-8", newline="").write(s.replace(anchor, NEW, 1))
print("  gate_offline.sh: five ALT-CTRL rows named")
