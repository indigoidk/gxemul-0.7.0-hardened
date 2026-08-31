#  Build mutant W: re-add the pre-#499 `len != 8' kill at the top of the catch-all.
#  *** THE BACKSLASH IS chr(92) ON PURPOSE.  Writing "\n" here cooks into a REAL
#  NEWLINE through the Bash -> heredoc -> Python path and splits the C string
#  literal -- `error: missing terminating " character'.  The measuring seat warned
#  about exactly this and I hit it anyway on the first attempt. ***
import io
BS = chr(92)
TAB = chr(9)
NL = chr(10)
p = "/tmp/gxl2/src/devices/dev_sgi_re.c"
s = io.open(p, encoding="utf-8").read()
A = (TAB + "} else {" + NL +
     TAB + TAB + "if (writeflag == MEM_WRITE) {" + NL +
     TAB + TAB + TAB + "if (!(d->warned & SGIRE_W_UNMAP_WR)) {")
if s.count(A) != 1:
    raise SystemExit("ANCHOR COUNT %d -- ABORT" % s.count(A))
K = (TAB + "} else {" + NL +
     TAB + TAB + "if (len != 8) {" + NL +
     TAB + TAB + TAB + 'fatal("[ sgi_re: len = %i not implemented ]' + BS + 'n", (int) len);' + NL +
     TAB + TAB + TAB + "exit(1);" + NL +
     TAB + TAB + "}" + NL +
     TAB + TAB + "if (writeflag == MEM_WRITE) {" + NL +
     TAB + TAB + TAB + "if (!(d->warned & SGIRE_W_UNMAP_WR)) {")
io.open(p, "w", encoding="utf-8", newline=NL).write(s.replace(A, K, 1))
#  prove the literal survived intact rather than trusting it
t = io.open(p, encoding="utf-8").read()
line = [l for l in t.split(NL) if "len = %i not implemented" in l]
print("      inserted, literal on ONE line: %s" % (len(line) == 1 and line[0].rstrip().endswith(');')))
print("      %s" % line[0].strip()[:72])
