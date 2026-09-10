#!/usr/bin/env python3
#  #518 table-4 extras.  Usage: mut518x.py <path-to-clone-dev_lca.c> <mutant>  (restore from SEC first).
#  M48_wen_perreg: PRETABLE §4's own prescribed mutant -- TWO WEN latch bits (BASE1 announces on another
#                  bit), so `wen once' (BASE0 then BASE1 in one session) sees two announces.
#  M49_def_narrow: the default-arm diagnostic narrowed to 32 bits ((int) cast on the printed value), the
#                  mutant `def width' exists for -- the audit found no preserved narrowing measurement.
import io, sys
P, m = sys.argv[1], sys.argv[2]
T = '\t'
s = io.open(P, encoding='utf-8', newline='').read()
M = {
 'M48_wen_perreg': (
    T*3 + "d->window_base_1 = idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN);\n"
    + T*3 + "if (idata & IOC_W_BASE_WEN)\n"
    + T*4 + "lca_ioc_announce(d, LCA_W_IOC_WEN, \"a DMA window was\"\n",
    T*3 + "d->window_base_1 = idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN);\n"
    + T*3 + "if (idata & IOC_W_BASE_WEN)\n"
    + T*4 + "lca_ioc_announce(d, LCA_W_IOC_WMASK1, \"a DMA window was\"\n"),
 'M49_def_narrow': (
    T*5 + "fatal(\": 0x%\" PRIx64 \" -- declined\",\n"
    + T*5 + "    (uint64_t)idata);" + T + "/*  #506  */\n",
    T*5 + "fatal(\": 0x%x -- declined\",\n"
    + T*5 + "    (int)idata);" + T + "/*  #506  */\n"),
}
if m not in M:
    print('unknown mutant', m); sys.exit(9)
old, new = M[m]
c = s.count(old)
if c != 1:
    print('MUTANT-TEXT-NOT-FOUND: %s matched %d times' % (m, c)); sys.exit(9)
io.open(P, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
print('applied', m)
