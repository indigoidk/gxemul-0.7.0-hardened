"""Rebuild the three CALL-SITE mutants the opus seat measured escaping, plus the
clause-(b) control, against the #480 candidate detector.

The mutant definitions are taken VERBATIM from that seat's own generators
(o479/mk.py, o479/mk2.py) rather than re-derived, so the table measures the same
edits it measured -- a re-derivation would be a different mutant wearing the same
name, which is exactly the mis-built-mutant class the carrier records.
"""
import os, shutil

S = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC"
C = ("/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL"
     "/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r480")
O = "/tmp/gx480"

CALL   = "\twdc_new_command_reset(d);\n"
HANDLE = "\t/*  Handle the command:  */\n"
CUR    = "\td->cur_command = idata;\n"


def uniq(t, s, name):
    n = t.count(s)
    assert n == 1, "anchor for %s occurs %d times, want 1" % (name, n)


#  M11: "a repeated opcode is a retry, not a new command"
def m_sameop(t):
    uniq(t, CUR, "sameop"); uniq(t, CALL, "sameop/call")
    t = t.replace(CUR, "\tint same_cmd = (d->cur_command == idata);\n" + CUR)
    return t.replace(CALL, "\tif (!same_cmd)\n\t" + CALL)


#  M4: "a command rejected with ABRT must not clobber the previous state"
def m_afterguard(t):
    uniq(t, CALL, "afterguard"); uniq(t, HANDLE, "afterguard/handle")
    t = t.replace(CALL, "")
    return t.replace(HANDLE, CALL + "\n" + HANDLE)


#  M23: "IDENTIFY and READ load their answer INTO the ring, so do not flush"
def m_exempt_fill(t):
    uniq(t, CALL, "exemptfill")
    return t.replace(CALL,
        "\tif (idata != WDCC_IDENTIFY && idata != WDCC_READ &&\n"
        "\t    idata != WDCC_READMULTI && idata != ATAPI_IDENTIFY_DEVICE)\n"
        "\t" + CALL)


#  clause (b): verbatim reinstatement of the defect the round removed
def m_revert(t):
    uniq(t, CALL, "revert")
    return t.replace(CALL, "\td->atapi_cmd_in_progress = 0;\n")


MUT = dict(M11_sameop=m_sameop, M4_afterguard=m_afterguard,
           M23_exemptfill=m_exempt_fill, Mb_revert=m_revert)

src = open(C + "/src/devices/dev_wdc.c").read()
for name, fn in MUT.items():
    d = "%s/%s" % (O, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d + "/regress")
    os.makedirs(d + "/src/devices")
    shutil.copy(C + "/regress/diff_wdc_identify.c", d + "/regress/")
    t2 = fn(src)
    assert t2 != src, "MUTANT %s CHANGED NOTHING" % name
    open(d + "/src/devices/dev_wdc.c", "w").write(t2)
    print("built", name)
