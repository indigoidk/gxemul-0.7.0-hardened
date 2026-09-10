#  ctlq_20260909 mutator.  ONE anchor serves all four mutants; MUTANT-TEXT-NOT-FOUND is a hard
#  FAIL, which makes every find-text a presence pin.  Sources are ALWAYS restored from SEC first
#  (never from a script's own backup -- the carrier's rule).
import sys, shutil
SEC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c"
TGT = "/tmp/gxopusctlq/src/devices/dev_pcc2.c"

GUARD  = "\tif (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {\n"
ASSERT = "\t\t}\n\t\tassert = 0;\n\t}\n"

MUTANTS = {
  #  guard WIDENING: the accept-side growth mutant the de-escalation clause owes a row for.
  #  0x10 is an UNNAMED GENCTL bit (the header names only DR0 0x80 / C040 0x04 / MIEN 0x02 /
  #  FAST 0x01), which is exactly why BENIGN = 0x10 is a legal benign write.
  "M_widen":        (GUARD,  "\tif (d->pcctwo_reg[PCCTWO_GENCTL] & (PCC2_C040 | 0x10)) {\n"),
  #  clause (d): keep the guard, null the repair.
  "M_d1_noassert":  (ASSERT, "\t\t}\n\t}\n"),
  "M_return":       (ASSERT, "\t\t}\n\t\treturn;\n\t}\n"),
  "M_latchinside":  (ASSERT, "\t\t\tassert = 0;\n\t\t}\n\t}\n"),
  "BASE":           (None, None),
}

name = sys.argv[1]
if name not in MUTANTS:
    sys.exit("UNKNOWN MUTANT %r" % name)
shutil.copyfile(SEC, TGT)                      #  restore from SEC, never from a backup
find, repl = MUTANTS[name]
if find is None:
    print("MUTANT=BASE  (pristine SEC copy restored)")
    sys.exit(0)
src = open(TGT, "rb").read().decode("latin-1")
n = src.count(find)
if n != 1:
    sys.exit("ANCHOR NOT UNIQUE for %s: found %d occurrences -- REFUSING" % (name, n))
open(TGT, "wb").write(src.replace(find, repl, 1).encode("latin-1"))
print("MUTANT=%s applied (1 site)" % name)
