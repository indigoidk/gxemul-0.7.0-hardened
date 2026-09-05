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
already served (the register array's CURRENT byte -- the tick's, for a counter interior: the announce says so);
WRITE side -- DECLINE + a per-offset latched `fatal()' ("(once)", the house idiom), NOT a backed
accept: the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear, the ICRs
mask and reassert, PSCALECNT/SPEED/the IACKs are read-only), the addition licence is unmet (no guest
reaches these offsets on this model's inspected driver paths -- if_ie never attaches), and a store into pcctwo_reg[] from the
one arm reached by 43 offsets adds a bounded-write surface the decline does not have.

CONTRACT -- what this detector is built to catch, by row (36 rows; the 13 added by the pass-2 repair are marked +):
  (b) the verbatim `exit(1)' reinstated             -> every survival row (named/inword/unnamed wr AND rd, alias, wide)
  (d) the announce unlatched                        -> `latch sameoff' (2 lines, not 1)
  (d) one whole-arm latch bit instead of per-offset -> `latch twooff' (1 line, not 2), `named wr msg' (1, not 18)
  (d) the latch SET conditioned on writes (grok A)  -> + `latch rd rd' (2, not 1), + `latch rd wr' (2, not 1): with
      `latch sameoff' (W,W) and `latch rw one' (W,R) these are ALL FOUR setter x tester direction cells
  (d) `|=' -> `=' at the latch update (codex)       -> + `latch aba' (3, not 2): bits already set survive a new offset
  (d) a writeflag guard that re-kills READS         -> `named rd' (host exit)
  (d) a `len != 1' re-kill -- the removed kill was width-agnostic, so this is a partial reinstatement (grok B)
                                                    -> + `wide wr' / + `wide rd' (host exit)
  (d) a re-kill at ONE unsampled offset (Fable)     -> `inword wr' / `unnamed wr' now drive all 12 / all 13, and
                                                       + `inword rd' / + `unnamed rd' read them: every one of the 43
                                                       uncased offsets is written once and read once
  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text' / + `wr declined'
  member 6 (BACKED ACCEPT) substituted for member 3 -> `ieicr rdawr' / `ieerr rdawr' read back the stored byte (0x5a)
      instead of 0x0 -- the DISPOSITION-pinning rows; `sccerr rdawr' (a CASED, write-to-clear sibling) is the
      control that reads 0x0 under either and makes the delta attributable
  member 6 on the LATCHED path only (Opus M_O2: a store exempting the first write per offset -- MEASURED 23/23 on
      the 23-row instrument)                        -> + `sameoff val' (0x5a, not 0x0)
  the read announce printing a wrong or constant byte (Opus M_O1, MEASURED 23/23: `named rd srvd' counts the
      phrase, not the value)                        -> + `srvd val text' (`served 0x34' absent); + `srvd val' pins
      the served byte itself as one the GUEST wrote (through the cased T1CMP word arm), not a default
  the announce omitting the access width            -> + `wide wr msg' / + `wide rd srvd' (`(len 4)')
  the `relative_addr %= PCC2_SIZE' fold changed      -> `alias msg' (the announce names offset 0x2a, not 0x6a)
  the fix perturbing a cased arm                    -> `genctl rt', `t1cmp word rt'
DISCLOSED, not caught: half-word (len 2) default accesses (the mutant that kills len 4 also kills len 2; one that
kills ONLY len 2 is not rowed); an END-SPANNING wide read (0x3d + 4 > 0x40) takes the zero-fill path and is announced
`served 0x00' truthfully (data[0] is what was served) but no row drives it; the announce names the FIRST served byte
of a wide read, labelled with the width; the in-word bytes are the interior of IMPLEMENTED counters, declined here
as a width/alignment matter (pcc2widecompose's business) -- and their served byte is the tick's, not a default,
which is why the announce prints data[0] rather than reloading the array; the fold of 0x40..0xfff onto 0x00..0x3f
IS the real part's: Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as 'PCCchip2 Registers  Repeated'
(_scratchpad/vmesbcp2.txt:4629; two seats had rightly called it unestablished before the manual was on disk); the
fork's PCC2_SIZE (0x40) and the guest header's (0x1000) name different things; the IACK offsets 0x23/0x25 are
declined like the rest -- modelling them (on the SCCRXIACK shape) would open two new entries into the C040 path, so
pcc2c040kill goes first; `named wr'/`named rd' touch all eighteen offsets in ONE session each (valid because the
fix has no per-offset branch; the count rows are AGGREGATES, so a per-offset failure is located by reading the
log, not by a row) -- if a later round branches per offset this compression is invalid; "unnamed" means the FORK
HEADER has no label, not that the part is undocumented (0x39 is SPEED's second byte, 0x3b PRTDATA's low byte);
per-instance latch scope is not provable by fresh sessions (each is a new process; `pcc2latchinst').
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
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in INWORD]))
row("inword wr", fate(alive, how), "survived", "ALL twelve bytes inside the four 32-bit counter/compare words: no case -> default: (a re-kill at any one dies)")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in INWORD]))
row("inword rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the twelve (reads drove 18/43 offsets before this row -- codex, Fable)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in UNNAMED]))
row("unnamed wr", fate(alive, how), "survived", "ALL thirteen offsets the fork header does not name (the manual names some: 0x39 is SPEED's 2nd byte, 0x3b PRTDATA's)")
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
row("latch sameoff", t.count(MSG) if alive else "n/a", 1, "two writes to one offset announce ONCE: an unlatched arm prints 2 (the read-back is silent: bit set)")
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
t, alive, how = session(setup() + program([LD_BU(4, PRTICR)]))
row("dir rd text", t.count("unimplemented read from") if alive else "n/a", 1, "...and READ for a load")
# -- the served VALUE: a guest word store to the CASED T1CMP puts 0x34 in its interior byte 0x05, then an uncased ld.bu there
t, alive, how = session(setup(r5="0x12345678") + program([ST_W(5, T1CMP), LD_BU(4, 0x05)]) + ["print r4"])
row("srvd val", val(t, alive, how), "0x34", "the served byte is the array's CURRENT byte, here one the guest wrote through the cased word arm -- not a default")
row("srvd val text", t.count("served 0x34") if alive else "n/a", 1, "...and the announce prints THAT byte (data[0], what was served): `served 0x%02x' of 0 passes `named rd srvd' (Opus M_O1, MEASURED)")
# -- wide accesses at default offsets: the old kill was width-agnostic, so a `len != 1' re-kill is a partial reinstatement (grok B)
t, alive, how = session(setup(r5="0x5a5a5a5a") + program([ST_W(5, IEERR), LD_W(4, IEERR)]) + ["print r4"])
row("wide wr", val(t, alive, how), "0x0", "a guest st.w at IEERR (0x28..0x2b, all uncased) survives and is declined: reads back 0x0 (a memcpy-backed store reads 0x5a5a5a5a)")
row("wide wr msg", t.count("offset 0x28 (len 4)") if alive else "n/a", 1, "...announced once, with the width; the ld.w at the same offset is silenced by the per-offset bit")
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
