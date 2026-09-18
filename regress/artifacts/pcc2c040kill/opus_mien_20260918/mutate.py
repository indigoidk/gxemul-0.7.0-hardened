import sys, shutil
SEC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c"
TGT = "/tmp/gxopus_pcc2k/src/devices/dev_pcc2.c"
LATCH = "\t\tif (!(d->warned & (1u << PCC2_W_C040))) {\n"
MUT = {
  "M_announce_notmien": (LATCH, "\t\tif (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN) &&\n\t\t    !(d->warned & (1u << PCC2_W_C040))) {\n"),
  "M_announce_onlyifsuppressing": (LATCH, "\t\tif (assert && !(d->warned & (1u << PCC2_W_C040))) {\n"),
  "BASE": (None, None),
}
name = sys.argv[1]
shutil.copyfile(SEC, TGT)
f, r = MUT[name]
if f is None: print("BASE restored"); sys.exit(0)
s = open(TGT, "rb").read().decode("latin-1")
if s.count(f) != 1: sys.exit("ANCHOR count %d -- REFUSING" % s.count(f))
open(TGT, "wb").write(s.replace(f, r, 1).encode("latin-1")); print("applied", name)
