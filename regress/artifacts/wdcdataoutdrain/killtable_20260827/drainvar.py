"""Score the candidate drain fixes against the THREE measured entrances.

  empty      occupancy 0, 3-byte write            (first=0xdd)
  empty8     occupancy 0, 8-byte write            (first=0xdd)
  leftover   occupancy 512 UNREAD, 8-byte write   (first=0xbe)

The grok seat's claim is that `inbuf_len > 0` closes the first two and NOT the third.
That is measured here rather than argued: 512 > 0 passes the guard.

Variants:
  A       inbuf_len > 0 &&                         (the brief's candidate)
  A2      inbuf_len >= 512 * count-equivalent      (grok's stronger form)
  D       the width `default:` arm does not fall through into the drain
"""
import io, os, shutil

NL, T = chr(10), chr(9)
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
SCR = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad")
DET = os.path.join(SCR, "drain", "regress", "diff_wdc_identify.c")
OUT = os.path.join(SCR, "dvar")

SRC = io.open(os.path.join(ROOT, "src", "devices", "dev_wdc.c"),
              encoding="utf-8", newline="").read()

#  the drain condition, derived from the file rather than typed
DRAIN = (NL + T*3 + "if (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
         T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL +
         T*3 + "    ||" + NL +
         T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
         T*3 + "    inbuf_len % 512 == 0) ) {" + NL)
assert SRC.count(DRAIN) == 1, "drain anchor %d" % SRC.count(DRAIN)

#  the width default: arm, which pushes nothing and falls through
#  *** THERE ARE TWO OF THESE, one per endianness branch, both at 4 tabs.
#  The brief showed only the little-endian arm.  A `default:`-side fix therefore
#  costs TWO edits where a drain-side guard costs one -- which is itself an
#  argument, and it was found by an anchor assert rather than by reading. ***
DEFAULT = (T*4 + "default:if (!d->warned_badlen) {" + NL)
assert SRC.count(DEFAULT) == 2, "default anchor %d (expected 2)" % SRC.count(DEFAULT)

DECL = (T*3 + "int inbuf_len;" + NL)
assert SRC.count(DECL) == 1, "decl anchor %d" % SRC.count(DECL)

VAR = [
    ("A_gt0", "inbuf_len > 0 &&  (the brief's candidate)",
     [(DRAIN, NL + T*3 + "if (inbuf_len > 0 &&" + NL +
       T*3 + "    (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
       T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL +
       T*3 + "    ||" + NL +
       T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
       T*3 + "    inbuf_len % 512 == 0)) ) {" + NL)]),

    ("D_nofall", "the width default: arm sets a flag; the drain honours it",
     [(DEFAULT, T*5 + "default:d->badlen_seen = 1;" + NL +
       T*5 + "        if (!d->warned_badlen) {" + NL),
      (DRAIN, NL + T*3 + "if (!d->badlen_seen &&" + NL +
       T*3 + "    (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
       T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL +
       T*3 + "    ||" + NL +
       T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
       T*3 + "    inbuf_len % 512 == 0)) ) {" + NL)]),

    ("AD_local", "BOTH, but the bad-len flag is a PER-ACCESS LOCAL",
     [(DECL, T*3 + "int inbuf_len;" + NL + T*3 + "int badlen_this = 0;" + NL),
      (DEFAULT, T*4 + "default:badlen_this = 1;" + NL +
       T*4 + "        if (!d->warned_badlen) {" + NL),
      (DRAIN, NL + T*3 + "if (inbuf_len > 0 && !badlen_this &&" + NL +
       T*3 + "    (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
       T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL +
       T*3 + "    ||" + NL +
       T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
       T*3 + "    inbuf_len % 512 == 0)) ) {" + NL)]),
    ("AD_both", "BOTH: inbuf_len > 0 AND the default: arm declines",
     [(DEFAULT, T*5 + "default:d->badlen_seen = 1;" + NL +
       T*5 + "        if (!d->warned_badlen) {" + NL),
      (DRAIN, NL + T*3 + "if (inbuf_len > 0 && !d->badlen_seen &&" + NL +
       T*3 + "    (( d->write_in_progress == WDCC_WRITEMULTI &&" + NL +
       T*3 + "    inbuf_len % (512 * d->write_count) == 0)" + NL +
       T*3 + "    ||" + NL +
       T*3 + "    ( d->write_in_progress == WDCC_WRITE &&" + NL +
       T*3 + "    inbuf_len % 512 == 0)) ) {" + NL)]),
]

#  D and AD need the field.  Add it beside the existing latch flags.
FIELD = T + "int" + T*2 + "warned_badlen;" + NL
assert SRC.count(FIELD) == 1, "field anchor %d" % SRC.count(FIELD)

if os.path.isdir(OUT):
    shutil.rmtree(OUT)

for name, desc, edits in VAR:
    s = SRC
    if "badlen_seen" in NL.join(r for _, r in edits):
        s = s.replace(FIELD, FIELD + T + "int" + T + "badlen_seen;" + NL, 1)
    for find, repl in edits:
        n = s.count(find)
        want = 2 if find == DEFAULT else 1
        assert n == want, "%s: anchor matched %d, wanted %d" % (name, n, want)
        s = s.replace(find, repl, want)
    assert s != SRC, "%s: no-op" % name
    d = os.path.join(OUT, name)
    os.makedirs(os.path.join(d, "src", "devices"))
    os.makedirs(os.path.join(d, "regress"))
    io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
            "w", encoding="utf-8", newline="").write(s)
    shutil.copy(DET, os.path.join(d, "regress", "diff_wdc_identify.c"))
    print("  %-10s %s" % (name, desc))

#  the unfixed tree, as the control column
d = os.path.join(OUT, "_unfixed")
os.makedirs(os.path.join(d, "src", "devices"))
os.makedirs(os.path.join(d, "regress"))
io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
        "w", encoding="utf-8", newline="").write(SRC)
shutil.copy(DET, os.path.join(d, "regress", "diff_wdc_identify.c"))
print("  %-10s %s" % ("_unfixed", "control column -- must show all three RED"))
