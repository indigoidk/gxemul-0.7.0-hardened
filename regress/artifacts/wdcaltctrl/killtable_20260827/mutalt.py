"""ALT-CTRL kill table.

CLAUSE (b) is the verbatim reinstatement of what shipped before.
CLAUSE (d) is DEPENDS-ON: the predicates DOMINATING the diff's edited lines, walked up
only to the enclosing function -- here that is the one guard the fix introduced, plus the
two effects it guards. Each is weakened to the least-restrictive form that still READS
like the same check.
CLAUSE (c) is the null medium, a comment-only device file: a COMPILE failure by
construction, so it has no .out and that is not a lost log.

Two mutants a seat named are DELIBERATELY ABSENT and their absence is a result:
  * `m2` (edge dropped) IS THE SHIPPED DESIGN. It was a mutant only against the B1
    variant the round declined on a measured zero delta.
  * `m7` (prev_ctl update mis-scoped) is IMPOSSIBLE BY CONSTRUCTION under B4 -- there is
    no prev_ctl to mis-scope. That is the point of choosing B4, and recording it here is
    what stops a future round from re-adding the field without re-deriving the argument.
"""
import os, shutil

S = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC"
O = "/tmp/gxaltk"

GUARD = ("\t\tif (idata & WDCTL_RST) {\n"
         "\t\t\td->cur_command = COMMAND_RESET;\n"
         "\t\t\twdc_new_command_reset(d);\n"
         "\t\t}\n")


def uniq(t, s, name):
    n = t.count(s)
    assert n == 1, "anchor for %s occurs %d times, want 1" % (name, n)


#  (b) verbatim reinstatement of the shipped defect
def m_revert(t):
    uniq(t, GUARD, "revert")
    return t.replace(GUARD, "\t\tif (idata & WDCTL_4BIT)\n"
                            "\t\t\td->cur_command = COMMAND_RESET;\n")


#  (d) the guard kept, the ABORT half of its repair removed
def m_nohelper(t):
    uniq(t, GUARD, "nohelper")
    return t.replace(GUARD, "\t\tif (idata & WDCTL_RST)\n"
                            "\t\t\td->cur_command = COMMAND_RESET;\n")


#  (d) the guard kept, the LATCH half of its repair removed
def m_nolatch(t):
    uniq(t, GUARD, "nolatch")
    return t.replace(GUARD, "\t\tif (idata & WDCTL_RST) {\n"
                            "\t\t\twdc_new_command_reset(d);\n"
                            "\t\t}\n")


#  (d) the predicate WIDENED -- the `m1` escape a seat measured against the old rows
def m_widemask(t):
    uniq(t, GUARD, "widemask")
    return t.replace(GUARD, GUARD.replace("idata & WDCTL_RST",
                                          "idata & (WDCTL_RST | WDCTL_IDS)"))


#  (d) the predicate swapped back to the wrong bit, repair intact -- the subtler half
#      of the original defect, and the one a "tidy-up" could plausibly reintroduce
def m_bitswap(t):
    uniq(t, GUARD, "bitswap")
    return t.replace(GUARD, GUARD.replace("idata & WDCTL_RST", "idata & WDCTL_4BIT"))


#  (d) the guard qualified by a field the guarded BODY reads -- the operand-swap form
def m_qualcmd(t):
    uniq(t, GUARD, "qualcmd")
    return t.replace(GUARD, GUARD.replace(
        "if (idata & WDCTL_RST) {",
        "if ((idata & WDCTL_RST) && d->cur_command != 0) {"))


MUT = dict(Mb_revert=m_revert, Md_nohelper=m_nohelper, Md_nolatch=m_nolatch,
           Md_widemask=m_widemask, Md_bitswap=m_bitswap, Md_qualcmd=m_qualcmd)

#  ---- the three escapes the opus seat measured, now expected to DIE ------------
#  Mo_nienzero / Mo_nien4bit re-open THIS ROUND'S OWN DEFECT #2 through a different
#  bit: they clobber cur_command on an nIEN write.  The old ABSOLUTE oracle ("did it
#  become COMMAND_RESET?") could not see that; the DELTA form can.
NL, T = chr(10), chr(9)

def m_nienzero(t):
    uniq(t, GUARD, "nienzero")
    return t.replace(GUARD, GUARD + T + T + "else if (idata & WDCTL_IDS)" + NL + T + T + T + "d->cur_command = 0;" + NL)


def m_nien4bit(t):
    uniq(t, GUARD, "nien4bit")
    return t.replace(GUARD, GUARD + T + T + "else if (idata & WDCTL_4BIT)" + NL + T + T + T + "d->cur_command = 0;" + NL)


#  Mo_sigalways drops the reset conjunct at the READ site, so an unreset CD-ROM signs.
#  The pre-existing "non-CD-ROM" control tests the OTHER conjunct, which is why it
#  escaped all three signature checks before the new control landed.
SIGLO = T + T + T + "if (d->cur_command == COMMAND_RESET &&" + NL


def m_sigalways(t):
    n = t.count(SIGLO)
    assert n == 2, "signature guards: %d" % n
    return t.replace(SIGLO, T + T + T + "if (" + NL)


MUT["Mo_nienzero"] = m_nienzero
MUT["Mo_nien4bit"] = m_nien4bit
MUT["Mo_sigalways"] = m_sigalways

src = open(S + "/src/devices/dev_wdc.c").read()
shutil.rmtree(O, ignore_errors=True)
for name, fn in MUT.items():
    d = "%s/%s" % (O, name)
    os.makedirs(d + "/regress")
    os.makedirs(d + "/src/devices")
    shutil.copy(S + "/regress/diff_wdc_identify.c", d + "/regress/")
    t2 = fn(src)
    assert t2 != src, "MUTANT %s CHANGED NOTHING" % name
    open(d + "/src/devices/dev_wdc.c", "w").write(t2)
    print("built", name)

#  (c) the null medium: a comment-only device file
d = O + "/Mc_null"
os.makedirs(d + "/regress")
os.makedirs(d + "/src/devices")
shutil.copy(S + "/regress/diff_wdc_identify.c", d + "/regress/")
open(d + "/src/devices/dev_wdc.c", "w").write(
    "/*  clause (c): the null medium.  A detector that passes against this is\n"
    "    measuring nothing at all.  Expected: COMPILE FAILURE, no .out.  */\n")
print("built Mc_null")
