#!/usr/bin/env python3
#  #519 TABLE 2 mutants (pass-2 findings).  Usage: mut519x.py <clone dev_sgi_re.c> <mutant>
#  M13_okorx  -- grok: `if (ok)' -> `if (ok || x)': every table-1 PUT sat at (0,0), so it kept 14/14.
#  M14_okory  -- the y form of the same cell.
#  M15_texrd  -- grok: SGIRE_W_BADCOLOR -> SGIRE_W_TEX_RD at both latch sites: independence is rowed only
#                against BADMODE, so this is EXPECTED TO ESCAPE and is DISCLOSED under clause (e) -- the
#                body never tests TEX_RD, and one row per other bit is the unbounded shape.  Built so the
#                disclosure carries a measured score rather than a prediction.
#  M16/M17    -- the RGB and RGBA case dropped (minimax: M_dropcase_rgb was missing from the plan; grok: two
#                accept rows had only M8 as their growth mutant).  Table 2b.
import io, sys
P, m = sys.argv[1], sys.argv[2]
T = '\t'
NL = chr(10)
GUARD = T*2 + "if (ok)" + T + "/*  #519: a declined type stores nothing  */" + NL
LATCH = T*3 + "if (!(d->warned & SGIRE_W_BADCOLOR)) {" + NL + T*4 + "d->warned |= SGIRE_W_BADCOLOR;" + NL
RGB_PUT = (T*2 + "case DE_MODE_TYPE_RGB:" + NL + T*3 + "buf[0] = *color >> 24;" + NL + T*3 + "buf[1] = *color >> 16;" + NL
           + T*3 + "buf[2] = *color >> 8;" + NL + T*3 + "buf[3] = 0;" + NL + T*3 + "break;" + NL)
RGBA_PUT = (T*2 + "case DE_MODE_TYPE_RGBA:" + NL + T*3 + "buf[0] = *color >> 24;" + NL + T*3 + "buf[1] = *color >> 16;" + NL
            + T*3 + "buf[2] = *color >> 8;" + NL + T*3 + "buf[3] = *color;" + NL + T*3 + "break;" + NL)
M = {
 'M13_okorx': (GUARD, T*2 + "if (ok || x)" + T + "/*  #519: a declined type stores nothing  */" + NL),
 'M14_okory': (GUARD, T*2 + "if (ok || y)" + T + "/*  #519: a declined type stores nothing  */" + NL),
 'M15_texrd': (LATCH, T*3 + "if (!(d->warned & SGIRE_W_TEX_RD)) {" + NL + T*4 + "d->warned |= SGIRE_W_TEX_RD;" + NL),
 'M16_dropcase_rgb':  (RGB_PUT, ""),     # accept-row failability for `rgb put' (minimax, grok): the case dropped
 'M17_dropcase_rgba': (RGBA_PUT, ""),    # the same for `live' -- RGBA falls to the default and is declined
 'M18_sharedbit_tlba': (LATCH, T*3 + "if (!(d->warned & SGIRE_W_TLBA_LEN)) {" + NL + T*4 + "d->warned |= SGIRE_W_TLBA_LEN;" + NL),
   # a WIDTH bit shared (bit 0): with the all-bits row this and M15 are expected KILLED by `allbits announce'
}
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
