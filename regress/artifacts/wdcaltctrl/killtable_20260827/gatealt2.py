"""Name the four rows the gate block MISSED, found by the opus seat.

The #481 gate block names FIVE rows. There are SEVEN alt-ctrl rows, now NINE. The two
original controls -- `control: a non-CD-ROM does not sign` and `control: the reset signature
works` -- are named NOWHERE, so deleting either keeps the gate fully green.

*** THAT IS THE EXACT FAILURE THE BLOCK'S OWN COMMENT SAYS NAMING EXISTS TO CLOSE. ***  I
wrote that comment, citing #480's measurement that the identity row binds row COUNT and never
row IDENTITY -- and then named five of seven rows. A guard that closes a hole for most of its
population is the check-that-cannot-fail shape wearing a partial disguise.

Also names the two rows added after the panel (`an unreset CD-ROM does not sign`, `the libata
SRST form signs too`), both of which are SOLE or near-sole carriers.

BS = chr(92) throughout -- a trailing backslash in a heredoc'd literal has now failed four
times in this session, most recently ten minutes ago.
"""
import io

NL, BS = chr(10), chr(92)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\gate_offline.sh"
s = io.open(P, encoding="utf-8", newline="").read()

IND, CONT = " " * 4, " " * 14
anchor = (IND + 'check     "wdc IDENTIFY: the SRST-signature accept row is present" ' + BS + NL +
          CONT + '"$(grep -c ' + chr(39) + 'a real SRST still signs the CD-ROM' + chr(39) +
          ' "$WDCLOG")" "1"' + NL)
assert s.count(anchor) == 1, "anchor occurs %d times" % s.count(anchor)
assert "the non-CD-ROM control is present" not in s, "already applied"


def row(label, token):
    return (IND + 'check     "wdc IDENTIFY: ' + label + '" ' + BS + NL +
            CONT + '"$(grep -c ' + chr(39) + token + chr(39) + ' "$WDCLOG")" "1"' + NL)


COMMENT = (
 IND + "#  *** THE BLOCK ABOVE NAMED FIVE OF SEVEN ROWS, AND THE TWO IT MISSED WERE BOTH" + NL +
 IND + "#      CONTROLS.  Found by the opus seat: deleting either kept this gate fully" + NL +
 IND + "#      green -- which is the precise failure the comment above says naming exists" + NL +
 IND + "#      to close.  A guard that covers most of its population is not a partial" + NL +
 IND + "#      guard; it is a guard with an unadvertised hole. ***" + NL +
 IND + "#" + NL +
 IND + "#  The two controls are load-bearing, not decoration:" + NL +
 IND + "#    non-CD-ROM        stops the signature assertion being satisfied by a device" + NL +
 IND + "#                      that signs unconditionally -- a different defect wearing" + NL +
 IND + "#                      this one's clothes" + NL +
 IND + "#    reset-signature   separates \"the power-on half is missing\" from \"the" + NL +
 IND + "#                      signature is broken\" -- two different repairs" + NL +
 IND + "#" + NL +
 IND + "#  The last two rows were added after the panel and are sole carriers:" + NL +
 IND + "#    unreset CD-ROM    SOLE carrier for Mo_sigalways (the reset conjunct dropped" + NL +
 IND + "#                      at the read site).  The non-CD-ROM control tests the OTHER" + NL +
 IND + "#                      conjunct, which is why that mutant escaped three checks" + NL +
 IND + "#    libata SRST form  0x0c differs from OpenBSD's 0x06 in BIT 3, the exact bit" + NL +
 IND + "#                      this round moved away from" + NL)

NEW = (anchor + NL + COMMENT +
       row("the non-CD-ROM control is present",
           "control: a non-CD-ROM does not sign") +
       row("the reset-signature control is present",
           "control: the reset signature works") +
       row("the unreset-CD-ROM row is present",
           "an unreset CD-ROM does not sign") +
       row("the libata-SRST-form row is present",
           "the libata SRST form signs too"))

io.open(P, "w", encoding="utf-8", newline="").write(s.replace(anchor, NEW, 1))
print("  gate_offline.sh: four missing rows named (2 controls + 2 new)")
