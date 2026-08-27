"""Add the AD_local variant: the same two edits as AD_both, but the bad-len flag is a
PER-ACCESS LOCAL rather than a struct field.

AD_both latches for the life of the device.  Both forms score identically on the four
corruption doors; only the accept row separates them.  That is exactly the shape the
de-escalation clause warns about -- a fix whose accept side nobody tested.
"""
import io, os

NL, T = chr(10), chr(9)
p = os.path.join(
    r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL",
    r"8e474f41-4d47-4c99-bf11-3406a84c4fcd", "scratchpad", "drainvar.py")
s = io.open(p, encoding="utf-8", newline="").read()

if "AD_local" in s:
    print("  AD_local already present")
    raise SystemExit(0)

#  the local-declaration anchor, derived: `int inbuf_len;` at three tabs
DECL_SRC = 'DECL = (T*3 + "int inbuf_len;" + NL)' + NL + \
           'assert SRC.count(DECL) == 1, "decl anchor %d" % SRC.count(DECL)' + NL + NL
anchor = "VAR = ["
assert s.count(anchor) == 1, "VAR anchor %d" % s.count(anchor)
s = s.replace(anchor, DECL_SRC + anchor, 1)

VARIANT = '''    ("AD_local", "BOTH, but the bad-len flag is a PER-ACCESS LOCAL",
     [(DECL, T*3 + "int inbuf_len;" + NL + T*3 + "int badlen_this = 0;" + NL),
      (DEFAULT, T*4 + "default:badlen_this = 1;" + NL +
       T*4 + "        if (!d->warned_badlen) {" + NL),
      (DRAIN, NL + T*3 + "if (inbuf_len > 0 && !badlen_this &&" + NL +
       T*3 + "    (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
       T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL +
       T*3 + "    ||" + NL +
       T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
       T*3 + "    inbuf_len % 512 == 0)) ) {" + NL)]),
'''
mark = '    ("AD_both",'
assert s.count(mark) == 1, "AD_both anchor %d" % s.count(mark)
s = s.replace(mark, VARIANT + mark, 1)

io.open(p, "w", encoding="utf-8", newline="").write(s)
print("  AD_local variant added (per-access local, no struct field)")
