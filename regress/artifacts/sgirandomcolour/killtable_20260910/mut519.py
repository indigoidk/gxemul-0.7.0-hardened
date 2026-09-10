#!/usr/bin/env python3
#  #519 mutator.  Usage: mut519.py <path-to-clone-dev_sgi_re.c> <mutant>   (the driver restores from SEC first)
#  One named edit per mutant, exact find/replace; MUTANT-TEXT-NOT-FOUND is a hard failure (exit 9).
#  M1 (b) reinstates the pre-fix ARM verbatim (the four random() fills and the unlatched fatal) inside the
#  new structure, so the store is taken again; M11 is the null medium (the pre-fix file wholesale).
import io, shutil, sys
P, m = sys.argv[1], sys.argv[2]
PRE = ('/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/'
       '8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/dev_sgi_re.pre519.c')
T = '\t'
ARM_NEW = (T*3 + "ok = 0;\n"
           + T*3 + "if (!(d->warned & SGIRE_W_BADCOLOR)) {\n"
           + T*4 + "d->warned |= SGIRE_W_BADCOLOR;\n"
           + T*4 + "fatal(\"[ put: color mode = 0x%x ] sgi_re: unimplemented \"\n"
           + T*4 + "    \"colour type in horrible_getputpixel, x=%i y=%i; store \"\n"
           + T*4 + "    \"declined (once) ]\\n\", color_mode, x, y);\n"
           + T*3 + "}\n")
ARM_OLD = (T*3 + "buf[0] = random();\n"
           + T*3 + "buf[1] = random();\n"
           + T*3 + "buf[2] = random();\n"
           + T*3 + "buf[3] = random();\n"
           + T*3 + "// TODO.\n"
           + T*3 + "fatal(\"[ put: color mode = 0x%x ]\\n\", color_mode);\n")
GUARD = T*2 + "if (ok)" + T + "/*  #519: a declined type stores nothing  */\n"
LATCH = T*3 + "if (!(d->warned & SGIRE_W_BADCOLOR)) {\n"
SETBIT = T*4 + "d->warned |= SGIRE_W_BADCOLOR;\n"
FATAL3 = (T*4 + "fatal(\"[ put: color mode = 0x%x ] sgi_re: unimplemented \"\n"
          + T*4 + "    \"colour type in horrible_getputpixel, x=%i y=%i; store \"\n"
          + T*4 + "    \"declined (once) ]\\n\", color_mode, x, y);\n")
CI_PUT = (T*2 + "case DE_MODE_TYPE_CI:\n" + T*3 + "buf[0] = *color;\n" + T*3 + "break;\n"
          + T*2 + "case DE_MODE_TYPE_RGB:\n" + T*3 + "buf[0] = *color >> 24;\n")
CI_PUT_NEW = (T*2 + "case DE_MODE_TYPE_RGB:\n" + T*3 + "buf[0] = *color >> 24;\n")
ABGR_PUT = (T*2 + "case DE_MODE_TYPE_ABGR:\n" + T*3 + "buf[0] = *color;\n" + T*3 + "buf[1] = *color >> 8;\n"
            + T*3 + "buf[2] = *color >> 16;\n" + T*3 + "buf[3] = *color >> 24;\n" + T*3 + "break;\n")
M = {
 'M1_reinstate':   (ARM_NEW, ARM_OLD),
 'M2_noguard':     (GUARD, ""),
 'M3_zerofill':    (T*3 + "ok = 0;\n", T*3 + "buf[0] = buf[1] = buf[2] = buf[3] = 0;\n"),
 'M4_okinlatch':   (T*3 + "ok = 0;\n" + LATCH + SETBIT, LATCH + T*4 + "ok = 0;\n" + SETBIT),
 'M5_nolatch':     (LATCH, T*3 + "if (1) {\n"),
 'M6_sharedbit':   (LATCH + SETBIT, T*3 + "if (!(d->warned & SGIRE_W_BADMODE)) {\n" + T*4 + "d->warned |= SGIRE_W_BADMODE;\n"),
 'M7_silent':      (FATAL3, ""),
 'M8_declineall':  (T*2 + "int ok = 1;", T*2 + "int ok = 0;"),
 'M9_dropcase_ci': (CI_PUT, CI_PUT_NEW),
 'M10_dropcase_abgr': (ABGR_PUT, ""),
 'M12_prefix_reworded': ("fatal(\"[ put: color mode = 0x%x ] sgi_re: unimplemented \"", "fatal(\"[ put: colour mode = 0x%x ] sgi_re: unimplemented \""),
}
if m == 'M11_null':
    shutil.copy(PRE, P); print('M11_null: pre-fix file copied'); sys.exit(0)
if m not in M:
    print('unknown mutant', m); sys.exit(9)
s = io.open(P, encoding='utf-8', newline='').read()
old, new = M[m]
c = s.count(old)
if c != 1:
    print('MUTANT-TEXT-NOT-FOUND: %s matched %d times' % (m, c)); sys.exit(9)
s = s.replace(old, new)
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('applied', m)
