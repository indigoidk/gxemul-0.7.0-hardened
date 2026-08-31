#!/usr/bin/env python3
"""Add the three mutants that discharge the ported probe's OWN new rows.

Without these, `wr lat1', `rd lat1', `wr rd 2msg' and `xwin rd' would ship
having never failed -- and an accept/latch row is discharged by a MEASURED
KILL, not by existing.  Each kill was previously measured only on the ARTIFACT
detector (or not at all), which is exactly the inheritance this pass exists to
stop.
"""
import io

P = ("/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/"
     "8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499/mkvariant499.py")
s = io.open(P, encoding="utf-8").read()

TAB = chr(9)
LF = chr(10)

add = '''elif variant == "mnolatch":
    # clause (d): keep the guard, NULL its repair -- announce but never set the
    # bit, so both declines FLOOD instead of latching.  Kills `wr lat1` and
    # `rd lat1`, which COUNT over two offsets rather than testing presence.
    s = apply_fix(s)
    T4 = chr(9) * 4
    for b in ("SGIRE_W_UNMAP_WR", "SGIRE_W_UNMAP_RD"):
        drop = T4 + "d->warned |= " + b + ";" + chr(10)
        if s.count(drop) != 1:
            die("mnolatch: latch-set line count %d for %s" % (s.count(drop), b))
        s = s.replace(drop, "")
elif variant == "mbothsame":
    # ONE bit for BOTH directions.  Whichever decline comes second is silently
    # suppressed.  Kills `wr rd 2msg`.
    s = apply_fix(s, 7, 7)
elif variant == "mrdcollide":
    # the READ bit reuses SGIRE_W_TLBA_LEN (1 << 0).  Kills `xwin rd`, which is
    # otherwise undischarged: fix6 collides only on the WRITE side.
    s = apply_fix(s, 7, 0)
'''
anchor = 'else:\n    die("unknown variant " + variant)\n'
assert s.count(anchor) == 1, s.count(anchor)
s = s.replace(anchor, add + anchor)

# the duplicate-enumerator check must not reject the DELIBERATE collisions
old = 'if variant != "fix6":'
new = 'if variant not in ("fix6", "mbothsame", "mrdcollide"):'
assert s.count(old) == 1
s = s.replace(old, new)

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("patched mkvariant499.py -- mnolatch, mbothsame, mrdcollide")
