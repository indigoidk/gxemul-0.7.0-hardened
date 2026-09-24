# fbdeclinefive (#545) -- HARNESS mutants of the (frozen, patched) sites probe, written to a NEW file; exact matches.
#   python hmut_fbd5.py <frozen-probe> <out-file> <M12|M14|M14ctl>
import io, sys
src, dst, mut = sys.argv[1:4]
s = io.open(src, encoding='utf-8', newline='').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, (mut, old[:60], s.count(old))
    s = s.replace(old, new)
LAUNCH_OLD = '''        os.execvp(BIN, [BIN, "-V", "-T", "-E", emul, "-M", "32",
'''
LAUNCH_NONAMING = '''        os.execvp(BIN, [BIN, "-V", "-T", "-E", "cats", "-M", ("notanumber" if emul != "cats" else "32"),
'''
if mut == 'M12':        # the quit leg without the quit: the next `reg` SUCCEEDS -> H2 must red
    rep('''            h2["quit_rc"] = send("quit", timeout=10)
''', '''            h2["quit_rc"] = None          # M12: NO quit
''')
elif mut == 'M14':      # H1 keyed on ANY nonzero exit, launched with a refusal that names no emulation
    rep('''h1_ok = (H["status"] == "NO-PROMPT" and not H["prompt"] and H["reject"]
         and H["exit"] == 1 and H["signal"] is None)
''', '''h1_ok = (H["exit"] not in (None, 0))    # M14: any nonzero exit
''')
    rep(LAUNCH_OLD, LAUNCH_NONAMING)
elif mut == 'M14ctl':   # the SHIPPED predicate against the same non-naming refusal: must red
    rep(LAUNCH_OLD, LAUNCH_NONAMING)
else:
    raise SystemExit("unknown " + mut)
io.open(dst, 'w', encoding='utf-8', newline='').write(s)
print("HMUT", mut, "->", dst)
