import sys, shutil
SP = "/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus535"
BASE = SP + "/pcc2_HEAD.c"
TGT = "/tmp/gxopus535/src/devices/dev_pcc2.c"
LT = "\t\tif (!(d->warned & (1u << PCC2_W_C040))) {\n"
LS = "\t\t\td->warned |= (1u << PCC2_W_C040);\n"
FA = "\t\t\tfatal(\"[ pcc2: C040 (MC68040 EIPL)"
MUT = {
 # A: latch bypassed in the MIEN-set cell -> announces on EVERY C040 reassert once MIEN is set
 "A_latch_bypass_mien": [(LT, "\t\tif ((d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN) ||\n\t\t    !(d->warned & (1u << PCC2_W_C040))) {\n")],
 # C: announce downgraded fatal() -> debug() (silenceable by -q / free-running)
 "C_fatal_to_debug": [(FA, "\t\t\tdebug(\"[ pcc2: C040 (MC68040 EIPL)")],
 # D: latch keyed on a bit another arm sets (MASK width decline) -- collision, not GENCTL_LEN
 "D_latch_bit_masklen": [(LT, "\t\tif (!(d->warned & (1u << PCC2_W_MASK_LEN))) {\n"),
                         (LS, "\t\t\td->warned |= (1u << PCC2_W_MASK_LEN);\n")],
 # E: announce gated on a pending count the body never tests
 "E_announce_pending_gate": [(LT, "\t\tif (d->pending_timer2_interrupts == 0 &&\n\t\t    !(d->warned & (1u << PCC2_W_C040))) {\n")],
 # F: latch SET only when MIEN clear (A's sibling via the store, not the test)
 "F_latchset_mienclear": [(LS, "\t\t\tif (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))\n\t\t\t\td->warned |= (1u << PCC2_W_C040);\n")],
 "BASE": [],
}
name = sys.argv[1]
shutil.copyfile(BASE, TGT)
s = open(TGT, "rb").read().decode("latin-1")
for f, r in MUT[name]:
    if s.count(f) != 1: sys.exit("ANCHOR count %d for %r -- REFUSING" % (s.count(f), f))
    s = s.replace(f, r, 1)
open(TGT, "wb").write(s.encode("latin-1")); print("applied", name)
