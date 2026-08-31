import sys, re
F = "/tmp/gxo498/src/devices/dev_sgi_re.c"
ORIG = "/tmp/gxo498_orig_dev_sgi_re.c"
which = sys.argv[1]
src = open(ORIG, encoding="utf-8").read()
T = chr(9); NL = chr(10); BS = chr(92)
if which == "base":
    open(F,"w",encoding="utf-8",newline="").write(src); print("BASELINE RESTORED"); sys.exit(0)

#  PREFIX: floor clause (b) -- VERBATIM reinstatement of the removed defect,
#  taken from `git show cb28a6f^`.  Replaces the whole shipped else-arm body.
start = T+"} else {"+NL+T+T+"/*"+NL+T+T+" *  #498: THIS USED TO END THE HOST PROCESS."
end   = T+T+"goto de_declined;"+NL+T+"}"+NL
i = src.find(start)
j = src.find(end)
if i < 0 or j < 0:
    print("ANCHOR NOT FOUND i=%d j=%d -- FAIL" % (i, j)); sys.exit(9)
body = src[i:j+len(end)]
if src.count(start) != 1 or src.count(end) != 1:
    print("ANCHOR NOT UNIQUE -- FAIL"); sys.exit(9)
repl = (T+"} else {"+NL
      + T+T+'fatal("sgi_de: len = %i not implemented'+BS+'n", len);'+NL
      + T+T+"exit(1);"+NL
      + T+"}"+NL)
out = src[:i] + repl + src[j+len(end):]
#  the label is now unreferenced -- gcc warns but does not error; keep it so the
#  ONLY difference from HEAD is the arm body.
open(F,"w",encoding="utf-8",newline="").write(out)
print("MUTANT APPLIED: prefix (verbatim pre-fix arm, %d bytes -> %d)" % (len(body), len(repl)))
