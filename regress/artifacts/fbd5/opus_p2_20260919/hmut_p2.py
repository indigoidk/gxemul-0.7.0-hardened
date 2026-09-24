# Opus pass-2 HARNESS mutants of the sites probe (M13 family); written to a NEW file.
import io, sys
src, dst, mut = sys.argv[1:4]
s = io.open(src, encoding='utf-8', newline='').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, (mut, old[:60], s.count(old))
    s = s.replace(old, new)
# inert hardening so a closed fd does not crash select() in the later teardown (measured GREEN alone as R0)
RD_OLD = '''        r, _, _ = select.select([fd], [], [], t)
'''
RD_NEW = '''        try:
            r, _, _ = select.select([fd], [], [], t)
        except (OSError, ValueError):
            dead[0] = True
            return False
'''
CLOSE_FIRST = '''            try:
                os.close(fd)          # M13: teardown BEFORE the observation
            except OSError:
                pass
            h2["next_rc"] = send("reg", timeout=10)
'''
if mut in ('R0', 'M13', 'M13q'):
    rep(RD_OLD, RD_NEW)
if mut in ('M13', 'M13q'):
    rep('''            h2["next_rc"] = send("reg", timeout=10)
''', CLOSE_FIRST)
if mut == 'M13q':
    rep('''            h2["quit_rc"] = send("quit", timeout=10)
''', '''            h2["quit_rc"] = None          # M13q: NO quit either
''')
io.open(dst, 'w', encoding='utf-8', newline='').write(s)
print("HMUT", mut, "->", dst)
