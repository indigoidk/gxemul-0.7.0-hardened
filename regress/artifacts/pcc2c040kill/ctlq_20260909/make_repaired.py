#  Build pcc2_c040_probe.REPAIRED.py from the FROZEN shipped copy.
#  Exact-string edits; NOT-FOUND is a hard failure (every find-text is a presence pin).
SRC = "/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/ctlq/probe_SHIPPED.frozen.py"
DST = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/pcc2c040kill/ctlq_20260909/pcc2_c040_probe.REPAIRED.py"

s = open(SRC, "rb").read().decode("utf-8")

#  ---- edit 1: DELETE the SAYS definition from its old place -------------------------------------
OLD_SAYS = '''
#  The announce's own distinctive substring.  Deliberately NOT the whole sentence: a row that
#  matches the full text also fails on a harmless rewording, which makes it a spelling test.
SAYS = "C040 (MC68040 EIPL)"
'''
NEW_SAYS_SITE = '''
#  (SAYS is defined ABOVE the CONTROL block -- hoisted 2026-09-09 so `genctl ctlq' can key on it.)
'''

#  ---- edit 2: HOIST it above the CONTROL block --------------------------------------------------
OLD_CTL_HDR = '''#  ---- CONTROL: the identical instruction, register and width, with a benign value ---------------
'''
NEW_CTL_HDR = '''#  The announce's own distinctive substring.  Deliberately NOT the whole sentence: a row that
#  matches the full text also fails on a harmless rewording, which makes it a spelling test.
#  *** HOISTED HERE 2026-09-09 (artifacts/pcc2c040kill/ctlq_20260909/) so the `genctl ctlq' CONTROL
#  row below can key on it.  It is the ONE binding for the shipped announce text; a second literal
#  copy of the sentence would drift away from this one. ***
SAYS = "C040 (MC68040 EIPL)"

#  ---- CONTROL: the identical instruction, register and width, with a benign value ---------------
'''

#  ---- edit 3: THE ONE-STRING REPAIR, with its provenance -----------------------------------------
OLD_ROW = '''ctl_saw_c040 = ("C040 interrupt assertions" in t)
'''
NEW_ROW = '''#  *** 2026-09-09: THIS ROW WAS KEYED ON RETIRED TEXT AND COULD NOT FAIL.  ONE STRING CHANGED. ***
#
#  IT WAS KEYED ON  ("C040 interrupt assertions" in t)  -- the PRE-FIX fatal() text, which #512
#  replaced with the announce bound as SAYS above.  `grep -c "C040 interrupt assertions"
#  src/devices/dev_pcc2.c' is 0 on every post-fix build, so `ctl_saw_c040' was ALWAYS False:
#  the row was green under the shipped fix AND under all ten measured mutants alike.  It appears
#  in no FAIL list in either kill table.  That is an accept row discharged BY EXISTING, which the
#  accept-row failability rule says is no discharge at all.
#
#  WHY IT IS OWED.  #512 removed a host-fatal guard, so the de-escalation clause makes the detector
#  pin the ACCEPT SIDE of that predicate: a benign GENCTL bit must still NOT reach the C040 arm when
#  the guard GROWS onto it.  This row drives BENIGN = 0x10 through the identical instruction,
#  register and width, so it is precisely the row that should redden on a widening -- and did not.
#
#  MEASURED (artifacts/pcc2c040kill/ctlq_20260909/, 16-row instrument, scratch clone):
#
#      M_widen  `& PCC2_C040' -> `& (PCC2_C040 | 0x10)'   SHIPPED probe  16/16  *** CLEAN SWEEP ***
#               0x10 is BENIGN, an UNNAMED GENCTL bit --  REPAIRED probe 15/16  THIS ROW RED
#               the header names only DR0/C040/MIEN/FAST
#
#  IT IS NOW KEYED ON SAYS, what the arm actually emits today, so the benign write reaching the arm
#  is visible.  BOUND, stated rather than glossed: this pins the accept side for GENCTL bits the
#  guard could grow ONTO and whose value this session drives -- 0x10.  A widening onto MIEN (0x02)
#  is caught elsewhere and by accident (`irq live' suppresses); a widening onto DR0 (0x80) is caught
#  by NO row here.
#
#  *** DO NOT "FIX" `c040 attrib' BELOW ALONG WITH THIS ONE. ***  It keys on the SAME retired string
#  and is CORRECT that way: the death it attributes is the REINSTATED pre-fix kill (M_b_reinstate),
#  which carries the old text.  The two rows key on one string for opposite and both-valid reasons.
ctl_saw_c040 = (SAYS in t)
'''

for find, repl, label in ((OLD_SAYS, NEW_SAYS_SITE, "delete-old-SAYS"),
                          (OLD_CTL_HDR, NEW_CTL_HDR, "hoist-SAYS"),
                          (OLD_ROW, NEW_ROW, "the-one-string")):
    n = s.count(find)
    if n != 1:
        raise SystemExit("EDIT %s: anchor found %d times -- REFUSING" % (label, n))
    s = s.replace(find, repl, 1)
    print("edit applied: %s" % label)

open(DST, "wb").write(s.encode("utf-8"))
print("WROTE %s" % DST)
