"""#499 pass-4 follow-up mutators, anchored on text unique to DEVICE_ACCESS(sgi_re).

v1's anchor used the common tail `memory_writemax64(cpu, data, len, odata);', which
occurs FIVE times in dev_sgi_re.c across four handlers -- so it matched twice and the
run aborted.  Both anchors here are tied to SGIRE_W_UNMAP_* text, which appears only
in the sgi_re catch-all.
"""
import io
import sys

P = 'src/devices/dev_sgi_re.c'
WHICH = sys.argv[1]

s = io.open(P, encoding='utf-8').read()

if WHICH == 'both':
    #  after the WHOLE catch-all closes, before the common tail
    anchor = (
        '\t\t\t\t    (long long)relative_addr);\n'
        '\t\t\t}\n'
        '\t\t}\n'
        '\t}\n')
    repl = (
        '\t\t\t\t    (long long)relative_addr);\n'
        '\t\t\t}\n'
        '\t\t}\n'
        '\t\texit(0);\n'
        '\t}\n')
elif WHICH == 'write':
    #  inside the WRITE arm only, immediately after its latch block closes
    anchor = (
        '\t\t\t\t    (long long)relative_addr, (long long)idata);\n'
        '\t\t\t}\n'
        '\t\t} else {\n')
    repl = (
        '\t\t\t\t    (long long)relative_addr, (long long)idata);\n'
        '\t\t\t}\n'
        '\t\t\texit(0);\n'
        '\t\t} else {\n')
else:
    raise SystemExit('usage: e0_mut.py both|write')

n = s.count(anchor)
if n != 1:
    raise SystemExit('  ANCHOR MATCHED %d TIMES for %r -- refusing to mutate' % (n, WHICH))

io.open(P, 'w', encoding='utf-8', newline='').write(s.replace(anchor, repl))
print('  %s applied (anchor unique)' % WHICH)
