"""Add the mutants the SEATS named, which my generator did not have.

Six of these came from #478's pass 2 and none was mine.  A kill table built only from
the author's own imagination measures the author's imagination.

  M_le_nobad   delete `badlen_this = 1;` from the LITTLE-ENDIAN arm only.  Was
               INVISIBLE -- byte-identical detector output, same md5 -- until the LE
               rows landed.  The reason every table this session was half-blind.
  M_wmfold     fold the two drain arms, since they differ only in a modulus.  READS
               AS PURE DE-DUPLICATION and writes 131,072 bytes.
  M_wmmod      the WRITEMULTI modulus narrowed to 512: drains at the wrong MOMENT
               with the right byte count, which a shape-only row cannot see.
  M_lat        move `badlen_this = 1;` inside `if (!d->warned_badlen)`.  One line,
               looks like tidying the latch -- and because the latch holds for the
               device's life, every bad-len store after the first drains again.
  M_ann0       add `inbuf_len == 0 &&` to the announce, removing the notice from
               the leftover door.
  M_nodisp     drop `!badlen_this` from the CDB dispatch -- the #479 repair itself.
"""
import io, os

NL, T = chr(10), chr(9)
P = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
     r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\mk479.py")
s = io.open(P, encoding="utf-8", newline="").read()

if "M_le_nobad" in s:
    print("  already present")
    raise SystemExit(0)

EXTRA = '''
#  ---- mutants named by SEATS on #478's pass 2, not by me --------------------
BADSET = T*4 + "        badlen_this = 1;" + NL
assert SRC.count(BADSET) == 2, "badlen assignments %d" % SRC.count(BADSET)
_i = SRC.index(BADSET)

DRAIN = (T*3 + "if (inbuf_len > 0 && !badlen_this &&" + NL +
         T*3 + "    (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
         T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL +
         T*3 + "    ||" + NL +
         T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
         T*3 + "    inbuf_len % 512 == 0)) ) {" + NL)
assert SRC.count(DRAIN) == 1, "drain anchor %d" % SRC.count(DRAIN)

DISP = T*3 + "if (d->atapi_cmd_in_progress && !badlen_this &&" + NL
assert SRC.count(DISP) == 1, "dispatch anchor %d" % SRC.count(DISP)

MUT += [
    ("M_le_nobad", "(d) delete badlen_this=1 from the LITTLE-ENDIAN arm only  [fable]",
     [(SRC[_i:_i + len(BADSET)], "")]),

    ("M_wmfold", "(d) fold the two drain arms -- reads as de-duplication  [opus]",
     [(DRAIN, T*3 + "if (inbuf_len > 0 && !badlen_this &&" + NL +
       T*3 + "    ((d->write_in_progress == WDCC_WRITEMULTI ||" + NL +
       T*3 + "    d->write_in_progress == WDCC_WRITE) &&" + NL +
       T*3 + "    inbuf_len % 512 == 0) ) {" + NL)]),

    ("M_wmmod", "(d) WRITEMULTI modulus narrowed to 512  [opus]",
     [(T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL,
       T*3 + "    inbuf_len % 512 == 0)" + NL)]),

    ("M_lat", "(d) badlen_this=1 moved inside the warned_badlen latch  [opus]",
     [(SRC[_i:_i + len(BADSET)] + T*4 + "        if (!d->warned_badlen) {" + NL,
       T*4 + "        if (!d->warned_badlen) {" + NL +
       T*4 + "                badlen_this = 1;" + NL)]),

    ("M_nodisp", "(d) drop !badlen_this from the CDB dispatch -- the #479 repair",
     [(DISP, T*3 + "if (d->atapi_cmd_in_progress &&" + NL)]),
]
'''

anchor = "if os.path.isdir(OUT):"
assert s.count(anchor) == 1, "OUT anchor %d" % s.count(anchor)
s = s.replace(anchor, EXTRA + NL + anchor, 1)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  mk479.py: five seat-named mutants added")
