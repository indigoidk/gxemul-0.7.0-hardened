"""#479 kill table.

Three of these were named by seats that BUILT them and found the suite blind; the rows
that catch them were added before this table ran, so an escape here is a real escape and
not a missing row.
"""
import io, os, shutil

NL, T = chr(10), chr(9)
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
SCR = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad")
OUT = os.path.join(SCR, "m479")
DET = os.path.join(ROOT, "regress", "diff_wdc_identify.c")

SRC = io.open(os.path.join(ROOT, "src", "devices", "dev_wdc.c"),
              encoding="utf-8", newline="").read()

BODY = (T + "d->atapi_cmd_in_progress = 0;" + NL +
        T + "d->atapi_phase = 0;" + NL +
        T + "d->write_in_progress = 0;" + NL)
assert SRC.count(BODY) == 1, "helper body anchor %d" % SRC.count(BODY)

RING = T + "d->inbuf_head = d->inbuf_tail = 0;" + NL
assert SRC.count(RING) == 1, "ring anchor %d" % SRC.count(RING)

CALL = T + "wdc_new_command_reset(d);" + NL
assert SRC.count(CALL) == 1, "call anchor %d" % SRC.count(CALL)

MUT = [
    ("MdEndRing", "(d) move ONLY the ring flush out of the helper  [opus]",
     [(RING, ""),
      ("	d->int_assert = 1;" + NL + "}" + NL,
       "	d->int_assert = 1;" + NL +
               "	d->inbuf_head = d->inbuf_tail = 0;" + NL + "}" + NL)]),

    ("MdLatchReset", "(d) the helper also clears the warned_* latches  [opus]",
     [(BODY, BODY + T + "d->warned_badlen = 0;" + NL +
       T + "d->warned_empty_drain = 0;" + NL)]),

    ("MdNotSame", "(d) skip the reset for a REPEATED command  [opus]",
     [(CALL, T + "if (idata != d->cur_command)" + NL + T*2 +
       "wdc_new_command_reset(d);" + NL)]),

    ("MdNoPhase", "(d) drop the phase reset -- keep flag and ring",
     [(T + "d->atapi_phase = 0;" + NL, "")]),

    ("MdNoRing", "(d) drop the ring flush -- keep flag and phase",
     [(RING, "")]),

    ("MdNoWip", "(d) drop the write-flag clear -- keep ring and phase",
     [(T + "d->atapi_phase = 0;" + NL + T + "d->write_in_progress = 0;" + NL,
       T + "d->atapi_phase = 0;" + NL)]),

    ("Mb_revert", "(b) VERBATIM reinstatement: the bare flag clear",
     [(CALL, T + "d->atapi_cmd_in_progress = 0;" + NL)]),
]


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
     [(BADSET, ("", 1))]),

    ("M_wmfold", "(d) fold the two drain arms -- reads as de-duplication  [opus]",
     [(DRAIN, T*3 + "if (inbuf_len > 0 && !badlen_this &&" + NL +
       T*3 + "    ((d->write_in_progress == WDCC_WRITEMULTI ||" + NL +
       T*3 + "    d->write_in_progress == WDCC_WRITE) &&" + NL +
       T*3 + "    inbuf_len % 512 == 0) ) {" + NL)]),

    #  *** OCCURRENCE 1 ON PURPOSE.  #478 wrote this modulus into BOTH the drain
    #  guard and the announce arm, which a seat flagged as a duplication hazard --
    #  and it is now biting the mutant generator itself.  Narrowing only the DRAIN
    #  copy is also the more realistic edit: a partial fix is what actually happens
    #  to a duplicated expression. ***
    ("M_wmmod", "(d) WRITEMULTI modulus narrowed to 512, drain arm  [opus]",
     [(T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL,
       (T*3 + "    inbuf_len % 512 == 0)" + NL, 1))]),

    ("M_lat", "(d) badlen_this=1 moved inside the warned_badlen latch  [opus]",
     [(BADSET + T*4 + "        if (!d->warned_badlen) {" + NL,
       (T*4 + "        if (!d->warned_badlen) {" + NL +
        T*4 + "                badlen_this = 1;" + NL, "all"))]),

    ("M_nodisp", "(d) drop !badlen_this from the CDB dispatch -- the #479 repair",
     [(DISP, T*3 + "if (d->atapi_cmd_in_progress &&" + NL)]),
]

if os.path.isdir(OUT):
    shutil.rmtree(OUT)

for name, desc, edits in MUT:
    s = SRC
    for find, repl in edits:
        #  *** THE TWO ENDIANNESS ARMS ARE BYTE-IDENTICAL, so an anchor inside one
        #  matches BOTH by construction.  A uniqueness assert is the wrong test for a
        #  deliberately-duplicated switch -- it rejects the very mutant that proves the
        #  arms are separately covered.  An edit may name WHICH occurrence. ***
        which = None
        if isinstance(repl, tuple):
            repl, which = repl
        n = s.count(find)
        if which is not None:
            if which == "all":
                #  a tidy-up edit applied to a duplicated switch touches BOTH copies;
                #  targeting one would build a mutant no author would actually write.
                assert n >= 2, "%s: matched %d, wanted >= 2" % (name, n)
                s = s.replace(find, repl)
                continue
            assert n >= which, "%s: matched %d, wanted >= %d" % (name, n, which)
            pos = -1
            for _ in range(which):
                pos = s.index(find, pos + 1)
            s = s[:pos] + repl + s[pos + len(find):]
        else:
            assert n == 1, "%s: anchor matched %d" % (name, n)
            s = s.replace(find, repl, 1)
    assert s != SRC, "%s: no-op" % name
    d = os.path.join(OUT, name)
    os.makedirs(os.path.join(d, "src", "devices"))
    os.makedirs(os.path.join(d, "regress"))
    io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
            "w", encoding="utf-8", newline="").write(s)
    shutil.copy(DET, os.path.join(d, "regress", "diff_wdc_identify.c"))
    print("  %-14s %s" % (name, desc))

d = os.path.join(OUT, "Mc_null")
os.makedirs(os.path.join(d, "src", "devices"))
os.makedirs(os.path.join(d, "regress"))
io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
        "w", encoding="utf-8", newline="").write("/*  clause (c) null medium.  */" + NL)
shutil.copy(DET, os.path.join(d, "regress", "diff_wdc_identify.c"))
print("  %-14s %s" % ("Mc_null", "(c) NULL MEDIUM"))
