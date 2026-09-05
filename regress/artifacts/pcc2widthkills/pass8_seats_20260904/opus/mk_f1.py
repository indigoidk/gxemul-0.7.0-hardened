import io
BS = chr(92)
NL = BS + "n"          # the two characters backslash-n, to land inside a C-like literal

src = io.open("/tmp/gxopus_p8/p8/frozen_probe.py", encoding="utf-8").read()

a = "            until = c[2] if len(c) > 2 else None\n"
assert src.count(a) == 1, ("anchor a", src.count(a))
ins_a = ('            sys.stderr.write("F1 tuple: c=%r until=%r w=%r' + NL + '"'
         ' % (c, until, w))\n')
src = src.replace(a, a + ins_a)

b = "        if not rd(w, until):\n"
assert src.count(b) == 1, "anchor b"
ins_b = ("        _t0 = time.time()\n"
         "        _ok = rd(w, until)\n"
         "        if until is not None:\n"
         '            sys.stderr.write("F1 wait: %.3f s  until=%r  BREAKPOINT_in_buf=%s'
         + NL + '" % (time.time() - _t0, until, "BREAKPOINT" in buf))\n'
         "        if not _ok:\n")
src = src.replace(b, ins_b)

c = ('    "T2ICR unchanged -- a `&& !pending_timer2' + chr(39)
     + ' guard would land 0x20 and drop the pending count")\n')
assert src.count(c) == 1, "anchor c"
src = src.replace(c, c + '\nsys.stderr.write("F1 EARLY EXIT after pend2' + NL + '")\nraise SystemExit(0)\n')

io.open("/tmp/gxopus_p8/p8/f1_probe.py", "w", encoding="utf-8").write(src)
print("f1_probe written, bytes =", len(src))
