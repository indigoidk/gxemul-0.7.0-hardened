"""The FULL escape set the pass-2 seats named, built against the 87-row detector.

Nothing here is my own invention.  M23's conjuncts were split by the opus seat; the
same-single-member escapes were reached independently by fable (`!= WDCC_READ` its
smallest, `!= ATAPI_IDENTIFY_DEVICE` opus's).  p1 is opus's move-below-the-FIRST-guard.
Mq_pktretry is fable's.

The point of re-running the WHOLE set rather than only the new rows is that a row added
for one escape routinely changes another mutant's score, and this round has already been
bitten by exactly that (M11 went 3 -> 1 -> 2 across two row edits).
"""
import os, shutil

S = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC"
C = ("/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL"
     "/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r480b")
O = "/tmp/gx480b"

CALL   = "\twdc_new_command_reset(d);\n"
HANDLE = "\t/*  Handle the command:  */\n"
CUR    = "\td->cur_command = idata;\n"
G1     = ("\tif (!diskimage_exist(cpu->machine, d->drive + d->base_drive,\n"
          "\t    DISKIMAGE_IDE)) {\n")


def uniq(t, s, name):
    n = t.count(s)
    assert n == 1, "anchor for %s occurs %d times, want 1" % (name, n)


def exempt(opcode):
    def f(t):
        uniq(t, CALL, "exempt/" + opcode)
        return t.replace(CALL, "\tif (idata != %s)\n\t" % opcode + CALL, 1)
    return f


def m_sameop(t):
    uniq(t, CUR, "sameop"); uniq(t, CALL, "sameop/call")
    t = t.replace(CUR, "\tint same_cmd = (d->cur_command == idata);\n" + CUR)
    return t.replace(CALL, "\tif (!same_cmd)\n\t" + CALL)


def m_afterguard(t):
    uniq(t, CALL, "afterguard"); uniq(t, HANDLE, "afterguard/handle")
    t = t.replace(CALL, "")
    return t.replace(HANDLE, CALL + "\n" + HANDLE)


def m_exempt_fill(t):
    uniq(t, CALL, "exemptfill")
    return t.replace(CALL,
        "\tif (idata != WDCC_IDENTIFY && idata != WDCC_READ &&\n"
        "\t    idata != WDCC_READMULTI && idata != ATAPI_IDENTIFY_DEVICE)\n"
        "\t" + CALL)


#  opus: move the call below the FIRST early return ONLY -- strictly smaller than M4
def m_p1(t):
    uniq(t, CALL, "p1"); uniq(t, G1, "p1/guard1")
    t = t.replace(CALL, "")
    i = t.index(G1)
    j = t.index("\t}\n", i) + len("\t}\n")
    return t[:j] + "\n" + CALL + t[j:]


#  fable: a PKT retry is not a new command
def m_pktretry(t):
    uniq(t, CUR, "pktretry"); uniq(t, CALL, "pktretry/call")
    t = t.replace(CUR, "\tint was_pkt = (d->cur_command == ATAPI_PKT_CMD);\n" + CUR)
    return t.replace(CALL,
        "\tif (!(was_pkt && idata == ATAPI_PKT_CMD))\n\t" + CALL)


def m_revert(t):
    uniq(t, CALL, "revert")
    return t.replace(CALL, "\td->atapi_cmd_in_progress = 0;\n")


MUT = {
    "M11_sameop": m_sameop,
    "M4_afterguard": m_afterguard,
    "M23_exemptfill": m_exempt_fill,
    "Mb_revert": m_revert,
    #  ---- the escapes the pass-2 seats measured against the 85-row detector ----
    "Mq_read": exempt("WDCC_READ"),
    "Mq_readmulti": exempt("WDCC_READMULTI"),
    "Mq_atapiid": exempt("ATAPI_IDENTIFY_DEVICE"),
    "Mq_writemulti": exempt("WDCC_WRITEMULTI"),
    "Mq_idp": exempt("WDCC_IDP"),
    "Mq_setfeat": exempt("SET_FEATURES"),
    "Mq_softreset": exempt("ATAPI_SOFT_RESET"),
    "Mq_identify": exempt("WDCC_IDENTIFY"),
    "p1_belowguard1": m_p1,
    "Mq_pktretry": m_pktretry,
}

src = open(C + "/src/devices/dev_wdc.c").read()
shutil.rmtree(O, ignore_errors=True)
for name, fn in MUT.items():
    d = "%s/%s" % (O, name)
    os.makedirs(d + "/regress")
    os.makedirs(d + "/src/devices")
    shutil.copy(C + "/regress/diff_wdc_identify.c", d + "/regress/")
    t2 = fn(src)
    assert t2 != src, "MUTANT %s CHANGED NOTHING" % name
    open(d + "/src/devices/dev_wdc.c", "w").write(t2)
print("built %d mutants" % len(MUT))
