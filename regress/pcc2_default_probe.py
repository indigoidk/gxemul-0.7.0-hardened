#!/usr/bin/env python3
"""pcc2defaultkill DETECTOR (#501) -- the `default:' arm of DEVICE_ACCESS(pcc2) in dev_pcc2.c.

Before #501 that arm ended the emulator process (`exit(1)') on ANY access to an offset with no `case'
-- READS included, although the memcpy above the switch had already served them.  Forty-three of the
0x40 byte offsets reach it (derived from mvme_pcctworeg.h against the case list): eighteen NAMED
registers the model does not implement (PSCALECNT, GPIO_ICR/PCR, SCCMOIACK, SCCTXIACK, IEERR, IEICR,
IEBERR, SCSIERR, the printer block, SPEED, PRTDATA), the bytes INSIDE the four 32-bit counter/compare
words, and the unnamed offsets.  A single guest `st.b' or `ld.bu' at any of them was a host kill
(rung-3 witness, 7/13 on the committed build: regress/artifacts/pcc2defaultkill/witness_20260905/).

THE FIX (pass-1 panel of 2026-09-05, nine seats, converged): READ side -- keep the byte the memcpy
already served (the register array's CURRENT byte -- the tick's, inside a running COUNT word: the announce says so);
WRITE side -- DECLINE + a per-offset latched `fatal()' ("(once)", the house idiom), NOT a backed
accept: the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear, the ICRs
mask and reassert, PSCALECNT/SPEED/the IACKs are read-only), the addition licence is unmet (no guest
reaches these offsets on this model's inspected driver paths -- if_ie never attaches), and a store into pcctwo_reg[] from the
one arm reached by 43 offsets adds a bounded-write surface the decline does not have.

CONTRACT -- what this detector is built to catch, by row (46 rows: 23 at pass 2, +13 by the pass-2 repair, +10 by the
pass-3 repair; every pass-3 row was APPENDED to an existing session):
  member 6 on the READ side of the latched path -- a read whose bit is already set gets its RESPONSE zeroed (codex
      M_LATCH_RD_ZERO: every rowed read after a preceding access expected 0 anyway)
                                                    -> `srvd rd latch' (0x34 after a read set the bit), `srvd wr latch'
                                                       (0x78 after a write set it)
  the announce's width label constant (`(int) len' -> `4', codex: no byte row required `(len 1)')
                                                    -> `srvd val text' (`0x5 (len 1) -- served 0x34'), `wr val text'
                                                       (`0x30 (len 1): 0x5a'), `srvd half text' (`(len 2)')
  (b) the verbatim `exit(1)' reinstated             -> every survival row (named/inword/unnamed wr AND rd, alias, wide)
  (d) the announce unlatched                        -> `latch sameoff' (3 lines, not 1: two writes and the appended
                                                       read-back; the row said 2 until pass 4 -- measured 3 under M_UNLATCH)
  (d) one whole-arm latch bit instead of per-offset -> `latch twooff' (1 line, not 2), `named wr msg' (1, not 18)
  (d) the latch SET conditioned on writes (grok A)  -> `latch rd rd' (2, not 1), `latch rd wr' (2, not 1): with
      `latch sameoff' (W,W) and `latch rw one' (W,R) these are ALL FOUR setter x tester direction cells
  (d) the latch SET conditioned on OFFSET CLASS (Opus M_LATCHOFF, MEASURED 36/36)
                                                    -> `inword msg' (12), `unnamed msg' (13): a second write to one
                                                       offset of each class is silent; the named class is `latch sameoff'
  (d) `|=' -> `=' at the latch update (codex)       -> `latch aba' (3, not 2): bits already set survive a new offset
  (d) a writeflag guard that re-kills READS         -> `named rd' (host exit)
  (d) a width re-kill -- the removed kill was width-agnostic, so `len != 1' (grok B) or `len == 2' (grok, Fable) is a
      partial reinstatement                         -> `wide wr' / `wide rd' (len 4, host exit); `srvd half text' /
                                                       `half wr rdawr' (len 2, host exit)
  (d) a re-kill at ONE unsampled offset (Fable)     -> `inword wr' / `unnamed wr' drive all 12 / all 13, and `inword rd'
                                                       / `unnamed rd' read them: every one of the 43 uncased offsets is
                                                       written once and read once
  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text' / `wr declined'
  member 6 (BACKED ACCEPT) substituted for member 3 -> `ieicr rdawr' / `ieerr rdawr' read back the stored byte (0x5a)
      instead of 0x0 -- the DISPOSITION-pinning rows; `sccerr rdawr' (a CASED, write-to-clear sibling) is the
      control that reads 0x0 under either and makes the delta attributable
  member 6 on the LATCHED path only (Opus M_O2, MEASURED 23/23)   -> `sameoff val' (0x5a, not 0x0)
  member 6 scoped to an OFFSET CLASS (Opus M_BACKEDLOW `relative_addr < 0x14', MEASURED 36/36; kimi M_STORE1)
                                                    -> `inword rdawr' (0x5a), `unnamed rdawr' (0x5a), `half wr rdawr'
                                                       (0xbb78): one read-back per class -- named (ieicr/ieerr rdawr),
                                                       in-word, unnamed, and the len-2 write
  the READ announce printing a wrong or constant byte (Opus M_O1, MEASURED 23/23)
                                                    -> `srvd val text' (`served 0x34' absent) -- the served byte itself
                                                       is one the GUEST wrote (`srvd val'), not a default
  the READ announce printing the wrong byte of a HALFWORD read (Opus M_LASTBYTE `data[len-1]', MEASURED 36/36: `wide rd
      srvd' reads four ZERO bytes, so its channel could not vary)   -> `srvd half text' (0x56 of 0x5678, not 0x78).  NOT the
      wrong byte of a WORD read: `data[len>>2]' (Opus MO1, pass 4) MEASURED 46/46 -- see DISCLOSED
  THE ANNOUNCE GRID (channel x arm x width), written so the next pass verifies rather than hunts -- R = rowed, D = disclosed:
      channel        READ len1  READ len2  READ len4   WRITE len1  WRITE len2  WRITE len4
      fate            R          R          R           R           R           R
      count           R          R(0x06)    R(0x30)     R           D(silent)   R
      direction text  R          R          R           R           D(silent)   R
      width label     R          R          R           R           D(silent)   R
      value           R          R          D(zeros)    R           D(silent)   R
      offset label    R(0x5,0x6) R(0x6)     D           R(0x2a,0x30) D(silent)  R(0x28)
      every offset label outside those five is D (Opus MO3 `relative_addr < 0x14 ? relative_addr : 0', MEASURED 46/46);
      the low bit of every value cell is D (codex: all exact anchors are even)
  the WRITE announce printing a wrong or constant value (Opus M_WRVAL0 `0' and M_WRDATA0 `data[0]', MEASURED 36/36 --
      the mirror of M_O1, unrowed by the pass-2 repair)  -> `wr val text' (0x5a at len 1), `wide wr val' (0x5a5a5a5a at
                                                       len 4, where data[0] says 0x5a)
  the announce omitting the access width            -> `wide wr msg' / `wide rd srvd' / `srvd half text' (`(len N)')
  the `relative_addr %= PCC2_SIZE' fold changed      -> `alias msg' (the announce names offset 0x2a, not 0x6a)
  the fix perturbing a cased arm                    -> `genctl rt', `t1cmp word rt'
DISCLOSED, not caught: the read announce printing a RELOAD of the array instead of data[0] (Opus M_RELOAD, MEASURED
36/36 on the pass-3 instrument and 46/46 on this one, table 4 -- expected: the two differ only on the end-span zero-fill path, where every reachable start offset's array
byte is 0, and inside a running COUNT word, where the SIGALRM-driven tick (timer.c calls the callback from the
handler) can land between the copy and the announce -- a race no deterministic row can pin; data[0] is what was
served and stays the operand); len-8 default accesses (ld.d/st.d exist in cpu_m88k_instr.c; a re-kill of ONLY len 8
passes -- outside the contract, not a breach of it); the len-2 WRITE announce TEXT -- the probe's one halfword store
(st.h at 0x06) arrives with its bit already set and is declined SILENTLY, so no len-2 write announce is ever observed:
a write-value or width-label mutant scoped to len 2 passes all 46 rows (Fable, glm, grok, codex, pass 4; the write value
is pinned at len 1 and len 4, len is printed and never tested, so this is clause-(e) debt of the len-8 species -- and
`half wr rdawr' pins the DISPOSITION of that latched st.h, not its text); the len-4 READ value -- an aligned uncased word
read can only serve zero bytes (every word-aligned uncased offset's four bytes are 0, and the in-word bytes a cased
word store fills are not word-aligned; ld.w at 0x05 is rejected before memory_rw), so `wide rd srvd' pins the label
and the byte 0x00 and its VALUE channel cannot vary (a read-value or byte-selection mutant scoped to len 4 passes:
unpinnable by construction, disclosed); the LOW BIT of every announced value -- every exact value anchor is EVEN (0x5a,
0x5a5a5a5a, 0x34, 0x56, 0x00), so `& ~1' on either announce operand passes 46 rows (codex, pass 4; an artificial mask,
not a plausible edit -- use ODD test values the next time the instrument changes); the literal `(once)' marker --
pinned by no row, so dropping it passes 46 rows (kimi, pass 4; cosmetic: the latch BEHAVIOUR is pinned by the count
rows, the marker is the house idiom's spelling); `debug()' in place of `fatal()' -- every session single-steps, and
under stepping both print, so the swap is invisible here (the width probe discloses the same limit); an END-SPANNING wide read (0x3d + 4 > 0x40) is announced `served
0x00' truthfully but no row drives it; the in-word bytes are the interior of IMPLEMENTED counters, declined here as a
width/alignment matter (pcc2widecompose's business), and inside the two COUNT words the served byte is the tick's
while a counter runs; the disposition is value-pinned at ONE offset per class (IEICR/IEERR, 0x06, 0x21, plus 0x28 at
len 4 and 0x06 at len 2), valid because the arm has no per-offset branch -- a member 6 scoped to a single OTHER
offset passes (the `#392' shape if rowed per offset); the announce COUNT is pinned for WRITES at every one of the 43
offsets (named wr msg 18, inword msg 12, unnamed msg 13) and for READS at the named class (named rd msg 18) and at
0x05 -- a silent skip of a READ announce at another in-word or unnamed offset passes (grok, codex, pass 4); the fold of 0x40..0xfff onto 0x00..0x3f IS the real part's: Motorola VMESBCP2
Table 6-1 lists $FFF42040-$FFF42FFF as 'PCCchip2 Registers  Repeated' (_scratchpad/vmesbcp2.txt:4629; two seats had
rightly called it unestablished before the manual was on disk); the fork's PCC2_SIZE (0x40) and the guest header's
(0x1000) name different things; the IACK offsets 0x23/0x25 are declined like the rest -- modelling them (on the
SCCRXIACK shape) would open two new entries into the C040 path, so pcc2c040kill goes first; `named wr'/`named rd'
touch all eighteen offsets in ONE session each (valid because the fix has no per-offset branch; the count rows are
AGGREGATES, so a per-offset failure is located by reading the log, not by a row) -- if a later round branches per
offset this compression is invalid; "unnamed" means the FORK HEADER has no label, not that the part is undocumented
(0x39 is SPEED's second byte, 0x3b PRTDATA's low byte); per-instance latch scope is not provable by fresh sessions
(each is a new process; `pcc2latchinst').
The debugger's `put b' never reaches a DM_DEFAULT arm (measured): `put b ctl' is a control, not a witness.

Usage: python3 pcc2_default_probe.py <gxemul> <label>      Sentinel: PCC2D_PROBE_DONE
The pty session helper is the width probe's own (extracted at run time), never hand-rolled: a first
draft of the witness hand-rolled it and read every host kill as "survived".
"""
import io, os, pty, re, select, sys, time
BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
DUMMY = "/tmp/pcc2_dummy.bin"
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 4096)
HERE = os.path.dirname(os.path.abspath(__file__))
_w = io.open(os.path.join(HERE, "pcc2_width_probe.py"), encoding="utf-8").read()
exec(_w[_w.index("def session("):_w.index("\ndef printed")])     # session(cmds) -> (transcript, alive, how)

CODE, SCRATCH, PCC2, SENTINEL = 0x00010000, 0x00020000, 0xfff42000, 0xdeadbeef
CHIPID, GENCTL, T1CMP, SCCERR = 0x00, 0x02, 0x04, 0x1c
IEERR, IEICR, IEBERR, SCCTXIACK, PRTICR = 0x28, 0x2a, 0x2b, 0x25, 0x30
NAMED18 = [0x14, 0x18, 0x19, 0x23, 0x25, 0x28, 0x2a, 0x2b, 0x2c, 0x30, 0x31, 0x32, 0x33, 0x34, 0x36, 0x37, 0x38, 0x3a]
INWORD = [0x05, 0x06, 0x07, 0x09, 0x0a, 0x0b, 0x0d, 0x0e, 0x0f, 0x11, 0x12, 0x13]   # all 12 counter interiors
UNNAMED = [0x20, 0x21, 0x22, 0x24, 0x26, 0x29, 0x2d, 0x2e, 0x35, 0x39, 0x3b, 0x3c, 0x3d]   # all 13 the fork header leaves unnamed
assert len(NAMED18) + len(INWORD) + len(UNNAMED) == 43 and len(set(NAMED18 + INWORD + UNNAMED)) == 43
MSG = "pcc2: unimplemented"
def enc(op26, rd, rs1, imm): return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)
def LD_BU(rd, off): return enc(0x03, rd, 2, off)
def LD_W(rd, off): return enc(0x05, rd, 2, off)
def ST_B(rs, off): return enc(0x0b, rs, 2, off)
def ST_W(rs, off): return enc(0x09, rs, 2, off)
def LD_HU(rd, off): return enc(0x02, rd, 2, off)   # pass 3: a len-2 default read
def ST_H(rs, off): return enc(0x0a, rs, 2, off)    # pass 3: a len-2 default write
I_ST_SCR = enc(0x09, 5, 3, 0); I_LD_SCR = enc(0x05, 4, 3, 0); I_BR_SELF = 0xc0000000
def program(insns, at=CODE):
    words = list(insns) + [I_BR_SELF, 0]
    return ["put w 0x%x, 0x%08x" % (at + 4 * k, w) for k, w in enumerate(words)] + ["pc=0x%x" % at, "step %d" % len(insns)]
def setup(r5="0x5a5a5a5a"):
    return ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=%s" % r5, "r4=0x%x" % SENTINEL]
def printed(t, reg="r4"):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return "0x%x" % int(m.group(1), 16) if m else "absent"
def fate(alive, how): return "survived" if alive else "host " + how
def val(t, alive, how): return printed(t) if alive else fate(alive, how)
rows, bad = [], []
def row(name, got, want, why):
    ok = str(got) == str(want)
    rows.append(name); (None if ok else bad.append(name))
    #  STATUS LAST: gate 14 counts a row with `^<name>  .*ok$' / ` ok$' / ` FAIL$' -- a first draft printed the
    #  status before the note and the gate counted ZERO of 23 rows while the probe said DONE (caught by the gate, L1).
    print("%-16s %-14s %-14s %-60s %s" % (name, got, want, why[:60], "ok" if ok else "FAIL"), flush=True)
print("pcc2defaultkill DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-14s %-14s %-60s %s" % ("row", "got", "want", "note", ""))

t, alive, how = session(setup() + program([I_ST_SCR, I_LD_SCR]) + ["print r4"])
row("live", val(t, alive, how), "0x5a5a5a5a", "LIVENESS: scratch RAM st/ld round-trip")
t, alive, how = session(setup() + program([LD_BU(4, CHIPID)]) + ["print r4"])
row("devsig chipid", val(t, alive, how), "0x20", "DEVICE-SIGNATURE: CHIPID reads PCC2_ID through a guest ld.bu (RAM would read 0)")
# -- the eighteen named unimplemented registers, one session each direction
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in NAMED18]))
row("named wr", fate(alive, how), "survived", "guest st.b at all 18 named unimplemented registers in ONE session: (b) reinstated exit(1) kills on the first")
row("named wr msg", t.count(MSG) if alive else "n/a", 18, "one announce PER OFFSET: a whole-arm latch prints 1, an unlatched arm prints 18 too -- see `latch sameoff' (an aggregate count, not a locator)")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in NAMED18]))
row("named rd", fate(alive, how), "survived", "guest ld.bu at all 18 in one session: the READ side of the defect; a writeflag guard that re-kills reads dies here")
row("named rd msg", t.count(MSG) if alive else "n/a", 18, "the read announce fires once per offset too")
row("named rd srvd", t.count("served 0x") if alive else "n/a", 18, "the read announce says what happened -- SERVED, never 'ignored' (the VALUE is pinned by `srvd val text')")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in INWORD] + [ST_B(5, 0x06), LD_BU(4, 0x06)]) + ["print r4"])
row("inword wr", fate(alive, how), "survived", "ALL twelve bytes inside the four 32-bit counter/compare words: no case -> default: (a re-kill at any one dies)")
row("inword msg", t.count(MSG) if alive else "n/a", 12, "...twelve announces for twelve offsets; the SECOND write to 0x06 and the read-back are silent: the latch is per offset in THIS class too (Opus M_LATCHOFF)")
row("inword rdawr", val(t, alive, how), "0x0", "...and 0x06 reads back 0x0 after two writes: DECLINED in this class too -- a member 6 scoped to the low offsets reads 0x5a (Opus M_BACKEDLOW)")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in INWORD]))
row("inword rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the twelve (reads drove 18/43 offsets before this row -- codex, Fable)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in UNNAMED] + [ST_B(5, 0x21), LD_BU(4, 0x21)]) + ["print r4"])
row("unnamed wr", fate(alive, how), "survived", "ALL thirteen offsets the fork header does not name (the manual names some: 0x39 is SPEED's 2nd byte, 0x3b PRTDATA's)")
row("unnamed msg", t.count(MSG) if alive else "n/a", 13, "...thirteen announces; the second write to 0x21 and its read-back are silent (per-offset latch, unnamed class)")
row("unnamed rdawr", val(t, alive, how), "0x0", "...and 0x21 reads back 0x0: declined in the unnamed class too (a member 6 scoped by offset class reads 0x5a)")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in UNNAMED]))
row("unnamed rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the thirteen: with named rd + inword rd every one of the 43 is read once")
# -- the disposition-pinning rows: read-after-write in ONE session
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), LD_BU(4, IEICR)]) + ["print r4"])
row("ieicr rdawr", val(t, alive, how), "0x0", "st.b 0x5a then ld.bu at IEICR in ONE session reads 0x0: the write was DECLINED (a backed accept reads 0x5a)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEERR), LD_BU(4, IEERR)]) + ["print r4"])
row("ieerr rdawr", val(t, alive, how), "0x0", "the same at IEERR (0x28), the write-to-clear class whose cased sibling SCCERR clears on write")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, SCCERR), LD_BU(4, SCCERR)]) + ["print r4"])
row("sccerr rdawr", val(t, alive, how), "0x0", "CONTROL: the CASED write-to-clear sibling reads 0x0 under either disposition -- makes the two rows above attributable")
# -- the latch: per offset, per instance
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEICR), LD_BU(4, IEICR)]) + ["print r4"])
row("latch sameoff", t.count(MSG) if alive else "n/a", 1, "two writes to one offset announce ONCE: an unlatched arm prints 3 -- both writes and the appended read-back (silent under the fix: bit set); measured 3 in table 4")
row("sameoff val", val(t, alive, how), "0x0", "...and the SECOND write (latch already set) is declined too: a store exempting the first write reads 0x5a (Opus M_O2, MEASURED 23/23 escape)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEBERR)]))
row("latch twooff", t.count(MSG) if alive else "n/a", 2, "two offsets announce TWICE: a single whole-arm latch bit prints 1")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), LD_BU(4, IEICR)]))
row("latch rw one", t.count(MSG) if alive else "n/a", 1, "a write then a read at ONE offset announce once: the WRITE sets the bit the READ tests")
t, alive, how = session(setup() + program([LD_BU(4, IEICR), LD_BU(4, IEICR)]))
row("latch rd rd", t.count(MSG) if alive else "n/a", 1, "two READS at one offset announce once: a latch SET only on writes prints 2 (grok A) -- the setter x tester cell rw one cannot see")
t, alive, how = session(setup(r5="0x5a") + program([LD_BU(4, IEICR), ST_B(5, IEICR)]))
row("latch rd wr", t.count(MSG) if alive else "n/a", 1, "a READ then a write at one offset announce once: the read's bit silences the write (the fourth setter x tester cell)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEBERR), ST_B(5, IEICR)]))
row("latch aba", t.count(MSG) if alive else "n/a", 2, "A,B,A announces TWICE: `|=' -> `=' forgets A when B announces and prints 3 (codex) -- earlier bits survive a new offset")
# -- the fold and the text
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, 0x6a)]))
row("alias 0x6a", fate(alive, how), "survived", "0x6a folds onto 0x2a (`relative_addr %= PCC2_SIZE'): the real part's fold too (VMESBCP2 Table 6-1, `Repeated')")
row("alias msg", t.count("offset 0x2a") if alive else "n/a", 1, "...and the announce names the FOLDED offset 0x2a: a changed fold names another")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, PRTICR)]))
row("dir wr text", t.count("unimplemented write to") if alive else "n/a", 1, "the announce says WRITE for a store (an inverted writeflag test in the text says read)")
row("wr declined", t.count("declined") if alive else "n/a", 1, "...and the word is DECLINED (no other row counts it: `ignored' would pass every count row)")
row("wr val text", t.count("0x30 (len 1): 0x5a -- declined") if alive else "n/a", 1, "...and the announced VALUE is the byte written: the mirror of `srvd val text' on the write arm -- `idata -> 0' printed 0x0 and passed 36 rows (Opus M_WRVAL0, MEASURED)")
t, alive, how = session(setup() + program([LD_BU(4, PRTICR)]))
row("dir rd text", t.count("unimplemented read from") if alive else "n/a", 1, "...and READ for a load")
# -- the served VALUE: a guest word store to the CASED T1CMP puts 0x34 in its interior byte 0x05, then an uncased ld.bu there
t, alive, how = session(setup(r5="0x12345678") + ["r7=0xaabb"] + program([ST_W(5, T1CMP), LD_BU(4, 0x05), LD_HU(6, 0x06), ST_H(7, 0x06), LD_HU(6, 0x06), LD_BU(8, 0x05), ST_B(7, 0x07), LD_BU(9, 0x07)]) + ["print r4", "print r6", "print r8", "print r9"])
row("srvd val", val(t, alive, how), "0x34", "the served byte is the array's CURRENT byte, here one the guest wrote through the cased word arm -- not a default")
row("srvd val text", t.count("0x5 (len 1) -- served 0x34") if alive else "n/a", 1, "...and the announce prints THAT byte (data[0], what was served) WITH its width: `served 0x%02x' of 0 passed 23 rows (Opus M_O1, MEASURED); `(len 1)' -> `(len 4)' passed 36 (codex)")
row("srvd half text", t.count("0x6 (len 2) -- served 0x56") if alive else "n/a", 1, "a len-2 default read at 0x06 is announced from its FIRST byte (0x56 of 0x5678): data[len-1] says 0x78 (Opus M_LASTBYTE, MEASURED 36/36); a len-2 re-kill dies here")
row("half wr rdawr", (printed(t, "r6") if alive else fate(alive, how)), "0x5678", "...then st.h 0xaabb at 0x06 is DECLINED (silent: the bit is set) and ld.hu reads 0x5678 back: len-2 disposition; a byte-truncated backed store reads 0xbb78")
row("srvd rd latch", (printed(t, "r8") if alive else fate(alive, how)), "0x34", "a SECOND read at 0x05 -- its bit set by the FIRST READ -- still receives 0x34: a latched-path read whose response is zeroed passes count rows (codex M_LATCH_RD_ZERO)")
row("srvd wr latch", (printed(t, "r9") if alive else fate(alive, how)), "0x78", "st.b 0xbb at 0x07 (declined, announced) then ld.bu at 0x07 -- its bit set by a WRITE -- receives 0x78: the response is preserved on the latched path whichever direction set the bit")
# -- wide accesses at default offsets: the old kill was width-agnostic, so a `len != 1' re-kill is a partial reinstatement (grok B)
t, alive, how = session(setup(r5="0x5a5a5a5a") + program([ST_W(5, IEERR), LD_W(4, IEERR)]) + ["print r4"])
row("wide wr", val(t, alive, how), "0x0", "a guest st.w at IEERR (0x28..0x2b, all uncased) survives and is declined: reads back 0x0 (a memcpy-backed store reads 0x5a5a5a5a)")
row("wide wr msg", t.count("offset 0x28 (len 4)") if alive else "n/a", 1, "...announced once, with the width; the ld.w at the same offset is silenced by the per-offset bit")
row("wide wr val", t.count("(len 4): 0x5a5a5a5a -- declined") if alive else "n/a", 1, "...and the announced value is the WHOLE word: printing data[0] instead of idata says 0x5a (Opus M_WRDATA0, MEASURED 36/36)")
t, alive, how = session(setup() + program([LD_W(4, PRTICR)]) + ["print r4"])
row("wide rd", val(t, alive, how), "0x0", "a guest ld.w at PRTICR (0x30..0x33, all uncased) survives and is served the four zero bytes")
row("wide rd srvd", t.count("(len 4) -- served 0x00") if alive else "n/a", 1, "...and the announce names the width and the first served byte")
# -- the cased arms are untouched
t, alive, how = session(setup(r5="0x82") + program([ST_B(5, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
row("genctl rt", val(t, alive, how), "0x82", "an IMPLEMENTED byte register still round-trips (no C040 bit in 0x82)")
t, alive, how = session(setup(r5="0x12345678") + program([ST_W(5, T1CMP), LD_W(4, T1CMP)]) + ["print r4"])
row("t1cmp word rt", val(t, alive, how), "0x12345678", "the cased 32-bit counter arm still round-trips a word: the fix swallowed no cased arm")
t, alive, how = session(["put b 0xfff4202a, 0x00"])
row("put b ctl", fate(alive, how), "survived", "CONTROL: the debugger's put b never reaches a DM_DEFAULT arm (measured before the fix too)")
row("put b ctl msg", t.count(MSG) if alive else "n/a", 0, "...so it prints nothing -- not a witness, a control")
print("PCC2D_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
if bad:
    print("PCC2D_RED=%s" % ",".join(bad))
print("PCC2D_PROBE_DONE")
