#!/usr/bin/env python3
"""mk_pretable2.py -- writes PRETABLE2.out and PRETABLE2_predictions.json for #568 kill table 2, BEFORE table 2's first
build (the files' mtimes are the order proof).  Everything marked RECORDED below is computed by this script from the
inputs at run time (greps of fix568b, the diff HEAD -> fix568b, the row lists of the frozen probes and of the three
earlier PRETABLE files, the POP2 order and the shift arithmetic); the dispositions and per-leg predictions are the
measuring seat's derivations, written here before any table-2 leg is built.

usage (WSL python3):  python3 -I -B mk_pretable2.py <scratchpad vme dir> <project regress/artifacts/vmedefaultkill dir>
"""
import difflib
import hashlib
import io
import json
import os
import re
import sys

V, A = sys.argv[1], sys.argv[2]
R = os.path.join(V, "rev3")
T2 = os.path.join(R, "table2")


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def md5f(p):
    return hashlib.md5(io.open(p, "rb").read()).hexdigest()


FIXB = os.path.join(R, "dev_vme.fix568b.c")
HEADC = os.path.join(V, "fix", "dev_vme.head.c")
PROBE3 = os.path.join(R, "vme_default_probe.rev3.frozen.py")
PROBE2 = os.path.join(V, "killtable1", "vme_default_probe.frozen.py")
assert md5f(FIXB) == "beb120eae1be112b682bd528f103191c"
assert md5f(HEADC) == "2516a82bc777fe780f2dc6ccc00fd6c3"
assert md5f(PROBE3) == "ddcebfe3257d3370f3c16b0bee79a4be"
assert md5f(PROBE2) == "19de15b3ea69af28e437cdf92e22c97e"
fixb = rd(FIXB)
fixb_lines = fixb.split("\n")


def rows_of(raw):
    """row names of a probe run, in order (the probe prints `%-16s ...' rows between the header and SCORE)"""
    out, on = [], False
    for l in rd(raw).split("\n"):
        if l.startswith("row ") and " got " in l:
            on = True
            continue
        if on and l.startswith("SCORE "):
            break
        if on and l.rsplit(" ", 1)[-1] in ("ok", "FAIL") and not l.startswith("  "):
            out.append(l[:16].strip())
    return out


ROWS2 = rows_of(os.path.join(V, "killtable1", "legs", "BASE.raw"))
ROWS3 = rows_of(os.path.join(R, "dev", "dev1_BASE.raw"))
assert len(ROWS2) == 34 and len(ROWS3) == 38, (len(ROWS2), len(ROWS3))
CONTROL3 = ["session", "live", "neg apparatus", "unasm", "vbr reset", "free neg ctl"]
assert all(c in ROWS3 for c in CONTROL3)
POP_ROWS = ["p2 rd census", "p2 wr census", "p2 ld widths", "p2 st widths", "p2 ann rd", "p2 ann rd 2", "p2 ann wr",
            "p2 ann wr 2", "p2 nw rd", "p2 nw wr", "p1 fault lo", "p1 fault hi", "p1 fault mid", "p1 fault wr",
            "p1 p2 edge", "p3 interim", "p2 int byte", "p2 int half", "p1 census", "p1 widths"]
NEW_ROWS = ["p2 nw rd 2", "p2 nw wr 2", "p2 zero wr", "p1 quiet"]
P1_10 = ["p1 fault lo", "p1 fault hi", "p1 fault mid", "p1 fault wr", "p1 p2 edge", "p3 interim", "p2 int byte",
         "p2 int half", "p1 census", "p1 widths"]
ANN4 = ["p2 ann rd", "p2 ann rd 2", "p2 ann wr", "p2 ann wr 2"]

# ---------------------------------------------------------------------------------------------- the predictions
#  (leg, edit summary, predicted red rows, CONTROL, note).  CONTROL is OK for every leg but NULL: after the CONTROL
#  split no product leg touches session / live / neg apparatus / unasm / vbr reset / free neg ctl.
PRED = [
    ("BASE", "fix568b, rev 3", [], "OK", "38 green (development run rev3/dev/dev1_BASE.raw MEASURED it: 38 of 38)"),
    ("HEAD", "1a59a47e unmodified", POP_ROWS + NEW_ROWS, "OK",
     "the 20 population rows die (exit 1) and the four new rows die or are not exercised (dev1_HEAD.raw MEASURED it)"),
    ("NULL", "machine_mvme88k.c without the vme device_add (dev_vme.c = fix568b)",
     [r for r in ROWS3 if r not in ("neg apparatus", "session", "live", "unasm", "free quiet")], "FAIL",
     "see NULL PER CLASS (dev1_NULL.raw MEASURED it)"),
    ("M_EXIT", "default: return 0 -> exit(1)", P1_10 + ["p1 quiet"], "OK",
     "p1 quiet is DEPENDENT: its census session dies"),
    ("M_DROPMCTL", "drop case MASTERCTL", ["p2 rd census", "p2 wr census", "p2 ld widths", "p2 st widths"] + ANN4, "OK",
     "table 1 measured these eight; no rev-3 row touches 0x28 otherwise"),
    ("M_DROPMISC", "drop case MISC", ["p2 rd census", "p2 wr census", "p1 p2 edge"] + ANN4, "OK", "as table 1"),
    ("M_ADD94", "case 0x94 added", ["p1 fault mid", "p1 census", "p1 quiet"], "OK",
     "NEW channel: the census now DECLINES 0x94 and its first-access fatal() prints one `[ vme:' line in the free run, "
     "so p1 quiet (want 0/0) reads 1/0"),
    ("M_LATCHONE", "one shared latch", ["p2 ann rd", "p2 ann wr", "p2 nw rd", "p2 nw wr", "p2 nw wr 2"], "OK",
     "the non-word session's first access (ld.bu 0x04) takes the shared latch: pass 1 has 1 read line and 0 write "
     "lines, so p2 nw wr 2 reads `pass 1 silent' (dependent) while p2 nw rd 2 sees 0 (green); p2 zero wr is its "
     "session's only population-2 access, so it announces (green)"),
    ("M_LATCHNOSET", "no latch set", ANN4 + ["p2 nw rd 2", "p2 nw wr 2"], "OK",
     "pass 2 of the non-word session re-announces all six (3 + 3)"),
    ("M_LATCHRDSET", "latch set only on reads", ["p2 ann wr", "p2 nw wr 2"], "OK",
     "non-word writes never latch: pass 2 re-announces the three stores"),
    ("M_LATCHCLRW", "a write clears the bit BEFORE the check", ["p2 ann rd", "p2 ann rd 2", "p2 ann wr 2", "p2 nw wr 2"],
     "OK", "every write re-announces: pass 2's three stores"),
    ("M_LATCHCLRW_POST", "a write clears the bit AFTER the check", ["p2 ann rd 2", "p2 ann wr", "p2 ann wr 2",
                                                                    "p2 nw wr 2"], "OK",
     "pass 1's stores clear their bits, so pass 2's three stores re-announce"),
    ("M_WDEBUG", "write announce fatal -> debug", ["p2 ann wr", "p2 ann wr 2", "p2 nw wr", "p2 nw wr 2", "p2 zero wr"],
     "OK", "p2 nw wr 2 `pass 1 silent' (dependent); p2 zero wr prints nothing (0/0)"),
    ("M_RDEBUG", "read announce fatal -> debug", ["p2 ann rd", "p2 ann rd 2", "p2 nw rd", "p2 nw rd 2"], "OK",
     "p2 nw rd 2 `pass 1 silent' (dependent); the zero store is a write (green)"),
    ("M_ANNLEN4", "announce and latch only for len 4", ["p2 nw rd", "p2 nw wr", "p2 nw rd 2", "p2 nw wr 2"], "OK",
     "pass 1 silent in both directions, so both pass-2 rows read `pass 1 silent' (dependent)"),
    ("M_TRUNC", "write announce prints 32 bits", ["p2 nw wr"], "OK",
     "the zero store prints 0x0 either way (green); pass 2 is latched (green)"),
    ("M_WRFAULT", "decline arm faults writes", ["p2 wr census", "p2 st widths", "p2 nw rd", "p2 nw wr", "p2 nw rd 2",
                                                "p2 nw wr 2", "p2 zero wr"] + ANN4, "OK",
     "the non-word session stops at its first store; both pass-2 rows `not exercised' (dependent); the zero store "
     "announces then faults (unexpected stop)"),
    ("M_LENFAULT", "decline arm faults len != 4", ["p2 ld widths", "p2 st widths", "p2 nw rd", "p2 nw wr", "p2 nw rd 2",
                                                   "p2 nw wr 2"], "OK",
     "the non-word session stops at its first ld.bu; both pass-2 rows `not exercised' (dependent)"),
    ("M_STORE", "decline arm stores writes", ["p2 wr census", "p2 st widths"], "OK", "as table 1"),
    ("M_ODATA0", "odata = 0 in the arm", [], "OK", "predicted SURVIVOR (equivalent today: no population-2 word is ever "
                                                    "non-zero)"),
    ("M_SERVED0", "read announce prints a literal 0", [], "OK", "predicted SURVIVOR (equivalent today)"),
    ("M_FLTBREAK", "default: return 0 -> break", P1_10, "OK",
     "p1 quiet stays green: both free runs complete and default:'s debug() is silent"),
    ("M_FLTLEN", "default: refusal narrowed to len 4", ["p3 interim", "p2 int byte", "p2 int half", "p1 widths"], "OK",
     "p1 widths 0/8: all eight width accesses are non-word"),
    ("M_FLTWR", "default: writes no longer refused", ["p1 fault wr", "p1 widths"], "OK",
     "p1 widths 4/8: the four stores decline"),
    ("M_NOONCE", "(once) dropped from the read announce", ["p2 ann rd", "p2 nw rd"], "OK",
     "p2 nw rd 2 green: pass 1 printed three read lines (no exact match, but RD_HEAD-prefixed), pass 2 none"),
    ("M_DROPTCTL", "drop case TCTL", ["cased census", "tctl rt", "vbr rt", "t1count inc"], "OK",
     "CONTROL is now OK: cased census is scored after the split; vbr rt and t1count inc are DEPENDENT (one session)"),
    ("M_CAPNARROW", "uint64_t warned_unimpl -> uint32_t", "BUILD_FAILS", "-",
     "the typedef must refuse the build: size of array 'vme_warned_fits' is negative"),
    ("M_DROPIRQEN", "drop case IRQEN", ["cased census", "cased wr"], "OK", "CONTROL OK after the split"),
    ("M_T1CMPWRDROP", "T1CMP store dropped", ["t1cmp rt", "free ctl"], "OK",
     "CONTROL OK after the split: both are scored rows now"),
    ("M_ADD90", "case 0x90 added", ["p1 fault lo", "p1 fault wr", "p1 p2 edge", "p1 census", "p1 quiet"], "OK",
     "NEW channel as for M_ADD94: the census's first load (0x90) now announces, p1 quiet 1/0"),
    ("M_IDATA", "if (writeflag == MEM_WRITE) -> if (idata)", ["p2 zero wr"], "OK",
     "the zero store prints the READ form: p2 zero wr 0/1; every other store in the probe is non-zero"),
    ("M_LATCHLEN4", "if (len == 4) before the latch set", ["p2 nw rd 2", "p2 nw wr 2"], "OK",
     "pass 2 re-announces the three reads and the three stores (3 each)"),
    ("M_DFATAL", "default: READ debug -> fatal", ["p1 quiet"], "OK", "p1 quiet 988/4 (census reads, widths reads)"),
    ("M_DFATALW", "default: WRITE debug -> fatal", ["p1 quiet"], "OK", "p1 quiet 0/4 (the four width stores)"),
    ("M_LANE0H", "default: aligned len-2 accesses served", ["p1 widths"], "OK",
     "p1 widths 7/8 with r8 losing its sentinel; ld.hu 0x96 and 0x2a are lane 2 (still fault)"),
    ("M_LANE0B", "default: aligned len-1 accesses served", ["p1 widths"], "OK",
     "p1 widths 7/8; every other byte access in the probe is at lane 1 or 3"),
    ("M_ONENARROW", "both arm literals 1ULL -> 1u", ["p2 ann rd", "p2 ann wr"], "OK",
     "UB-MEDIATED (see M_ONENARROW): IF this x86-64 build masks the 32-bit shift count to 5 bits, MISC (35) lands on "
     "bit 3 = SLAVELMOD2's, which POP2 order sets first, so MISC is silenced: 25 lines each.  A shift-to-zero build "
     "would red the four ann rows instead; a build using a 64-bit bit-test/set with the unmasked count would SURVIVE.  "
     "The leg's object code is disassembled AFTER the run and recorded."),
    ("BASE_FINAL", "fix568b restored", [], "OK", "38 green"),
]
LEG_NAMES = [p[0] for p in PRED]
man = rd(os.path.join(T2, "legs", "MANIFEST.txt"))
for name in LEG_NAMES:
    if name not in ("BASE", "HEAD", "BASE_FINAL"):
        assert re.search(r"^%s\s" % re.escape(name), man, re.M), name
for name, _e, red, ctl, _n in PRED:
    if red != "BUILD_FAILS":
        assert all(r in ROWS3 for r in red), (name, [r for r in red if r not in ROWS3])

# ---------------------------------------------------------------------------------------------- the channel map
#  row -> (designed-to-kill legs, observable).  `designed' = the row's own channel; a red under any other leg is
#  DEPENDENT (its session stopped) or a SECOND CHANNEL (named in the leg's note).
CHANNEL = {
    "neg apparatus": ([], "APPARATUS: a bogus subtype must make `live' fail"),
    "session": ([], "APPARATUS: the control session runs to quit"),
    "live": ([], "APPARATUS: an or-immediate reads back"),
    "vbr reset": ([], "MEDIUM: DEVINIT's VBR seed (a DEVINIT-seed edit or a device-less build reds it; no leg edits DEVINIT)"),
    "free neg ctl": ([], "APPARATUS: GCSRCTL's debug() line, 1 stepped and 0 free-running"),
    "unasm": ([], "APPARATUS: every placed word re-read (literal 1441)"),
    "t1cmp rt": (["M_T1CMPWRDROP"], "read-back value of a cased store"),
    "cased census": (["M_DROPTCTL", "M_DROPIRQEN"], "a dropped cased label FAULTs: PC 0x18 + sentinels"),
    "free ctl": (["M_T1CMPWRDROP"], "free-running T1CMP round trip value"),
    "free quiet": ([], "no `[ vme:' text in the free ctl run (a cased access that announced would show; no such leg)"),
    "tctl rt": (["M_DROPTCTL"], "TCTL store/read-back value or PC"),
    "vbr rt": ([], "VBR store/read-back (no leg breaks the VBR write path: DEPENDENT under M_DROPTCTL)"),
    "t1count inc": ([], "T1COUNT store + `+= 100' (no leg breaks it: DEPENDENT under M_DROPTCTL)"),
    "cased wr": (["M_DROPIRQEN"], "PC after six stores to non-storing cased arms"),
    "p2 rd census": (["M_DROPMCTL", "M_DROPMISC"], "a dropped population-2 label FAULTs: PC + sentinels"),
    "p2 wr census": (["M_DROPMCTL", "M_DROPMISC", "M_STORE", "M_WRFAULT"], "read-back value / PC after stores"),
    "p2 ld widths": (["M_LENFAULT", "M_DROPMCTL"], "PC + destinations of ld.bu/ld.hu 0x28, ld.d 0x08"),
    "p2 st widths": (["M_LENFAULT", "M_WRFAULT", "M_STORE", "M_DROPMCTL"], "PC / read-back after st.b/st.h/st.d"),
    "p2 ann rd": (["M_LATCHONE", "M_LATCHNOSET", "M_LATCHCLRW", "M_RDEBUG", "M_NOONCE", "M_ONENARROW", "M_DROPMCTL",
                   "M_DROPMISC"], "pass-1 line count / form / tail literal"),
    "p2 ann rd 2": (["M_LATCHNOSET", "M_LATCHCLRW", "M_LATCHCLRW_POST"], "pass-2 line count"),
    "p2 ann wr": (["M_LATCHONE", "M_LATCHNOSET", "M_LATCHRDSET", "M_LATCHCLRW_POST", "M_WDEBUG", "M_WRFAULT",
                   "M_ONENARROW", "M_DROPMCTL", "M_DROPMISC"], "pass-1 line count / form"),
    "p2 ann wr 2": (["M_LATCHNOSET", "M_LATCHCLRW", "M_LATCHCLRW_POST"], "pass-2 line count"),
    "p2 nw rd": (["M_ANNLEN4", "M_RDEBUG", "M_NOONCE", "M_LENFAULT", "M_LATCHONE"], "the `(len N)' read lines"),
    "p2 nw wr": (["M_ANNLEN4", "M_TRUNC", "M_WDEBUG", "M_LENFAULT", "M_WRFAULT", "M_LATCHONE"],
                 "the `(len N)' write lines and the 64-bit value"),
    "p2 nw rd 2": (["M_LATCHLEN4", "M_LATCHNOSET"], "pass-2 read-form line count, same process"),
    "p2 nw wr 2": (["M_LATCHLEN4", "M_LATCHNOSET", "M_LATCHRDSET", "M_LATCHCLRW", "M_LATCHCLRW_POST"],
                   "pass-2 write-form line count, same process"),
    "p2 zero wr": (["M_IDATA", "M_WDEBUG", "M_WRFAULT"], "the exact write-form literal of a zero first store"),
    "p1 fault lo": (["M_FLTBREAK", "M_EXIT", "M_ADD90"], "PC 0x18, DMA0, DMT0, process alive"),
    "p1 fault hi": (["M_FLTBREAK", "M_EXIT"], "PC 0x18, DMA0, DMT0, process alive"),
    "p1 fault mid": (["M_FLTBREAK", "M_EXIT", "M_ADD94"], "PC 0x18, DMA0, DMT0, process alive"),
    "p1 fault wr": (["M_FLTBREAK", "M_EXIT", "M_FLTWR", "M_ADD90"], "PC 0x18, DMA0, DMT0 of a store"),
    "p1 p2 edge": (["M_DROPMISC", "M_ADD90", "M_FLTBREAK", "M_EXIT"], "0x8c declines, 0x90 faults"),
    "p3 interim": (["M_FLTLEN", "M_FLTBREAK", "M_EXIT"], "a sub-word start faults"),
    "p2 int byte": (["M_FLTLEN", "M_FLTBREAK", "M_EXIT"], "a sub-word start faults"),
    "p2 int half": (["M_FLTLEN", "M_FLTBREAK", "M_EXIT"], "a sub-word start faults"),
    "p1 census": (["M_ADD94", "M_ADD90", "M_FLTBREAK", "M_EXIT"], "988 counted faults"),
    "p1 widths": (["M_FLTLEN", "M_FLTWR", "M_LANE0H", "M_LANE0B", "M_FLTBREAK", "M_EXIT"],
                  "eight counted width faults + r8's sentinel"),
    "p1 quiet": (["M_DFATAL", "M_DFATALW"], "`[ vme:' lines in the census and widths free runs"),
}
assert sorted(CHANNEL) == sorted(ROWS3), sorted(set(ROWS3) ^ set(CHANNEL))

out = []
w = out.append
w("PRETABLE2 -- #568 (vmedefaultkill) REPAIR 1, kill table 2, written BEFORE table 2's first build (this file's mtime")
w("and PRETABLE2_predictions.json's are the order proof).  Measuring seat (Opus 5.5), 2026-10-21.  Spec: rev3/REV3_SPEC.md")
w("sections 1-6 (section 6's amendments govern).  Lines marked RECORDED are computed by mk_pretable2.py from the inputs; the")
w("dispositions and the per-leg predictions are the seat's derivations, written before any table-2 leg was built.")
w("")
w("== 0. INPUTS (RECORDED md5s) ==")
w("  fix568b  rev3/dev_vme.fix568b.c          %s  (mk_fix568b.py over fix568 4e3e7fc2; objdump record:" % md5f(FIXB))
w("           rev3/OBJDUMP_fix568_vs_fix568b.txt)")
w("  HEAD     fix/dev_vme.head.c              %s  (1a59a47e's dev_vme.c)" % md5f(HEADC))
w("  rev 3    rev3/vme_default_probe.rev3.frozen.py  %s  (38 rows; the ONE instrument of table 2)" % md5f(PROBE3))
w("  rev 2    killtable1/vme_default_probe.frozen.py %s  (34 rows; tables 1, 1b and the M_IDATA run)" % md5f(PROBE2))
w("  legs     rev3/table2/legs/MANIFEST.txt (mk_legs568t2.py; 34 legs + NULL, each ONE exact find/replace)")
w("  DEVELOPMENT runs of rev 3, before this file and before any leg was built (rev3/dev/, a clone since deleted):")
for lab in ("dev1_BASE", "dev1_HEAD", "dev1_NULL"):
    t = rd(os.path.join(R, "dev", lab + ".raw"))
    res = re.search(r"^VME_DEFAULT_RESULT=(\S+)", t, re.M).group(1)
    ctl = re.search(r"^VME_DEFAULT_CONTROL=(\S+)", t, re.M).group(1)
    w("    %-10s VME_DEFAULT_RESULT=%s CONTROL=%s  (RECORDED from rev3/dev/%s.raw)" % (lab, res, ctl, lab))
w("")
w("== 1. SIBLING PARITY ==")
w("  * `default:' (FAULT) vs the five cased debug-only arms (GCSRCTL, TCR, IRQEN, IRQL3, IRQL4: DECLINE + unlatched")
w("    debug()): both print only through debug(), silent free-running.  Rev 2 pinned the cased side (`free quiet',")
w("    `free neg ctl'); rev 3 adds the FAULT side -- `p1 quiet' counts `[ vme:' in the two free-running population-1")
w("    runs, so a debug -> fatal promotion in `default:' (either direction) is visible.  DELETION of those debug()")
w("    calls is the same on both sides (silent either way): NOT CLAIMED, said so in the contract.")
w("  * the population-2 arm vs #501's PCC2 `default:' (latched fatal, direction decides wording, `(once)'): rev 3")
w("    adds the zero-valued first store (`p2 zero wr': direction decides the wording even when the value is 0) and")
w("    the cross-width latch hold (`p2 nw rd 2' / `p2 nw wr 2': a non-word first access latches).")
w("  * `default:' vs dev_unreadable.c (pure FAULT): both `return 0'; no asymmetry owed (unchanged from PRETABLE.out).")
w("  * the population-2 arm vs itself across lanes (FB F10c): word starts are labels, sub-word starts fault; `p1")
w("    widths' now holds BOTH lane-0 widths in population 1 (ld.hu 0xb0, st.b 0xb4) beside the lane-1/2/3 accesses.")
w("")
w("== 2. CLAIM -> ROW (every comment sentence fix568b ADDS or REWRITES over HEAD; RECORDED: the added comment text) ==")
hd = rd(HEADC).split("\n")
#  which fix568b lines carry comment text: a /* ... */ state scan (no comment in this file nests or sits in a string)
in_c, is_com = False, []
for l in fixb_lines:
    started = in_c or "/*" in l
    is_com.append(started)
    if "/*" in l:
        in_c = "*/" not in l[l.rindex("/*"):]
    elif in_c and "*/" in l:
        in_c = False
added = []
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, hd, fixb_lines, autojunk=False).get_opcodes():
    if tag in ("replace", "insert"):
        added += range(j1, j2)
com = [j for j in added if is_com[j]]
w("  RECORDED (%d lines added or rewritten over HEAD, %d of them comment text; fix568b line numbers):"
  % (len(added), len(com)))
for j in com:
    w("    %4d | %s" % (j + 1, fixb_lines[j].rstrip().replace("\t", "    ")))
w("  CLAIMS and their rows:")
CLAIMS = [
    ("struct: one bit per register WORD ... Zeroed by DEVINIT's memset, so every instance starts with every announce armed",
     "p2 ann rd / p2 ann wr (26 first-access lines each), p2 nw rd / p2 nw wr, p2 zero wr"),
    ("typedef: a warned_unimpl narrower than VME2_MISC >> 2 + 1 bits ... make that a compile error",
     "NO RUNTIME ROW, by construction: leg M_CAPNARROW must FAIL TO BUILD"),
    ("typedef: The 1ULL in the shifts below is not checked here",
     "a DISCLOSURE; leg M_ONENARROW measures what that literal's narrowing does on this host (UB-mediated)"),
    ("arm: registers the header names but this model does not implement. Each ended the emulator in default: below",
     "HEAD (test-first): the 20 population rows die on HEAD"),
    ("arm: OpenBSD 2.2's mvme88k driver has access sites at six of them. Its attach reaches four ... IRQSTAT and IRQCLR "
     "... ABORT-switch interrupt handler, and this model raises no VME2 interrupt",
     "NO ROW: a SOURCE-READING claim about the guest (no mvme187 OpenBSD boot image on this host; GLM's boot census "
     "offered, not adopted); NOT CLAIMED in the probe contract"),
    ("arm: A bus error here would panic that guest's attach", "NO ROW: counterfactual about a guest boot; NOT CLAIMED"),
    ("arm: a read is served the word preloaded above, which is 0 ... (odata is deliberately not forced to 0, so a "
     "store added by a later edit would show in a read-back)",
     "p2 rd census, p2 ld widths (0 served); p2 wr census, p2 st widths (a store shows: M_STORE)"),
    ("arm: a write is dropped", "p2 wr census, p2 st widths"),
    ("arm: one fatal() per register per device, the first access's direction deciding its wording",
     "p2 ann rd/rd 2/wr/wr 2, p2 nw rd/wr, p2 nw rd 2/wr 2, p2 zero wr (wording on a ZERO store: M_IDATA)"),
    ("arm: Sub-word starts inside these words are not matched here and reach default: (vmewidthlanes)",
     "p2 int byte, p2 int half"),
    ("default: an offset this model does not service ... Refuse the access -- for a guest data load or store, memory_rw "
     "then raises the m88k data-access exception",
     "p1 fault lo/hi/mid/wr (PC 0x18, DMA0, DMT0), p1 census, p1 widths, p3 interim, p2 int byte/half; instruction "
     "fetch NOT CLAIMED (the qualifier)"),
    ("default: the bus error a badaddr() probe expects", "NO ROW: the guest's recovery path; NOT CLAIMED"),
    ("default: instead of exit(1), which ended the emulator with no visible reason", "HEAD's `died:exit1' rows"),
    ("default: (debug() is silent at default verbosity)",
     "p1 quiet (0 `[ vme:' lines in two free runs) -- and free quiet / free neg ctl on the cased side"),
]
for c, rr in CLAIMS:
    w("    - %s" % c)
    w("        -> %s" % rr)
w("")
w("== 3. GUARD FIELD vs BODY FIELD, with the partition the body induces (RECORDED: the greps) ==")
w("  RECORDED `grep -n warned_unimpl' fix568b (every reader and writer of the latch field):")
for i, l in enumerate(fixb_lines, 1):
    if "warned_unimpl" in l:
        w("    %4d: %s" % (i, l.replace("\t", "    ").rstrip()))
w("  RECORDED `grep -n memset' fix568b:")
for i, l in enumerate(fixb_lines, 1):
    if "memset" in l:
        w("    %4d: %s" % (i, l.replace("\t", "    ").rstrip()))
w("  WRITERS of warned_unimpl: the arm's `|=' and DEVINIT's memset ONLY -- no state where guard field and body field")
w("  disagree is buildable within one instance (one vme device per process: NOT CLAIMED).")
w("  Partitions the arm's body induces, per lvalue:")
w("    writeflag      tested `== MEM_WRITE' -> {READ, WRITE} -- EXHAUSTED (both rowed at every label: the ann pair)")
w("    latch bit      tested by the guard -> {clear, set} -- EXHAUSTED (pass 1 clear, pass 2 set)")
w("    label (26)     each a dispatch label whose value flows into the latch index -> a FLOOR AXIS (26 x 2 x 2 = 104")
w("                   cells, the ann pair)")
w("    len            NOT tested by the fixed body (printed only) -- SAMPLED: 1, 2, 4, 8 by the non-word rows (one")
w("                   register per width) and the width rows at 0x28 / 0x08; the latch-hold across widths now rowed")
w("                   (`p2 nw rd 2', `p2 nw wr 2')")
w("    idata          NOT tested by the fixed body (printed in the write form); the operand swap M_IDATA makes the")
w("                   direction test read idata's zero-ness -> {0, non-0}: the 0 cell at a first access is rowed by")
w("                   `p2 zero wr' (one width, len 4), the non-0 cell by every other store -- DEPENDS-ON clause (2)")
w("    odata          NOT tested (printed in the read form; always 0 today: M_ODATA0 / M_SERVED0 equivalent)")
w("  `default:': no predicate of its own (the switch's fallthrough); the body tests writeflag (which debug())")
w("  -> {READ, WRITE} and nothing else.  The refusal-narrowing mutants each condition `return 0' on a lvalue the")
w("  body reads: len (M_FLTLEN), writeflag (M_FLTWR), len x lane (M_LANE0H, M_LANE0B) -- rowed by `p1 widths' (8")
w("  accesses: len 1, 2 and 8, lanes 0-3, both directions) and the stepped fault rows (len 4).")
w("")
w("== 4. CHANNEL: per row, the legs it is DESIGNED to kill and the observable that differs ==")
for r in ROWS3:
    legs, obs = CHANNEL[r]
    w("  %-14s %-12s %s" % (r, "CONTROL" if r in CONTROL3 else "scored", obs))
    if legs:
        w("  %-14s %-12s designed against: %s" % ("", "", ", ".join(legs)))
w("  CHECK OF THE CHANNEL LINE ITSELF: every channel above is named BEFORE table 2; the table's per-row reds say")
w("  whether each varied under its named legs.  A red under a leg NOT named for that row is reported as DEPENDENT")
w("  (its session stopped before the row's check, or pass 1 was silent) or as a SECOND CHANNEL (named in the leg's")
w("  note, e.g. p1 quiet under M_ADD94 / M_ADD90).")
w("")
w("== 5. ROW-LIST DIFF (the #490 rule): rev 3's rows against every row prescribed earlier ==")
pre1 = rd(os.path.join(A, "killtable1_20261020", "PRETABLE.out"))
add2 = rd(os.path.join(A, "killtable1_20261020", "PRETABLE_ADDENDUM_v2.out"))
p1b = rd(os.path.join(A, "killtable1_20261020", "table1b", "PRETABLE1B.txt"))
#  the prescribed names, transcribed from the three files and CHECKED to occur in them (RECORDED: each found)
PRESCRIBED = [
    ("PRETABLE.out", pre1, ["unasm", "live", "neg apparatus", "vbr reset", "free ctl", "free quiet", "cased census",
                            "t1cmp rt", "tctl rt", "vbr rt", "t1count inc", "cased wr", "p2 rd census", "p2 wr census",
                            "p2 ld widths", "p2 st widths", "p2 ann rd", "p2 ann wr", "p2 nonword ann", "p1 fault lo",
                            "p1 census", "p1 widths", "p1 p2 edge", "p2 int byte", "p2 int half", "p3 interim"]),
    ("PRETABLE_ADDENDUM_v2.out", add2, ["p2 nw rd", "p2 nw wr", "session", "free neg ctl", "p1 fault mid",
                                        "p2 ann rd 2", "p2 ann wr 2"]),
    ("PRETABLE1B.txt", p1b, ["cased wr", "cased census", "t1cmp rt", "free ctl", "p1 fault lo", "p1 fault wr",
                             "p1 p2 edge", "p1 census"]),
]
allp = []
for fn, txt, names in PRESCRIBED:
    found = [n for n in names if n in txt]
    w("  RECORDED %-26s %d names transcribed, %d found verbatim in the file" % (fn, len(names), len(found)))
    assert found == names, (fn, sorted(set(names) - set(found)))
    allp += names
#  `p1 fault lo/hi/wr' in PRETABLE.out names hi by the slash form; the addendum renamed `p2 nonword ann'
RENAMED = {"p2 nonword ann": ["p2 nw rd", "p2 nw wr"]}
allp = sorted(set(allp) | {"p1 fault hi"})
missing = []
for n in allp:
    if n in RENAMED:
        if not all(x in ROWS3 for x in RENAMED[n]):
            missing.append(n)
    elif n not in ROWS3:
        missing.append(n)
w("  prescribed rows (union, `p1 fault hi' from PRETABLE.out's `p1 fault lo/hi/wr'): %d; DROPPED in rev 3: %s"
  % (len(allp), ", ".join(missing) or "none"))
w("  renamed earlier and still present: `p2 nonword ann' -> `p2 nw rd' + `p2 nw wr' (addendum section 1)")
w("  rev 2 rows (RECORDED from killtable1/legs/BASE.raw): %d; rev 3 rows (RECORDED from rev3/dev/dev1_BASE.raw): %d"
  % (len(ROWS2), len(ROWS3)))
w("  ADDED in rev 3: %s" % ", ".join(r for r in ROWS3 if r not in ROWS2))
w("  REMOVED in rev 3: %s" % (", ".join(r for r in ROWS2 if r not in ROWS3) or "none"))
w("  CHANGED in rev 3 (same name): `p1 widths' 6 -> 8 faults (+ r8's sentinel); `p2 nw rd' / `p2 nw wr' now pass 1")
w("  of a two-pass session (their checks unchanged); `cased census', `t1cmp rt', `free ctl', `free quiet' leave")
w("  CONTROL_ROWS (scored); the stop wording of every row that stops before its check.")
w("")
w("== 6. NULL PER CLASS (the medium carries none of the behaviour under test; after the CONTROL split both classes ==")
w("==    red BY DESIGN, so a double FAIL is the expected shape, not an apparatus fault) ==")
nul = [p for p in PRED if p[0] == "NULL"][0]
nred = nul[2]
w("  CONTROL rows red  : %s" % ", ".join(r for r in CONTROL3 if r in nred))
w("  CONTROL rows green: %s  (apparatus that needs no device)" % ", ".join(r for r in CONTROL3 if r not in nred))
w("  scored rows red   : %d -- every row that reads the device: %s" % (sum(1 for r in nred if r not in CONTROL3),
                                                                     ", ".join(r for r in nred if r not in CONTROL3)))
w("  scored rows green : %s  (a run that prints nothing passes it with or without a device)"
  % ", ".join(r for r in ROWS3 if r not in nred and r not in CONTROL3))
w("  => 5 of 38 rows green, CONTROL=FAIL (`vbr reset': no DEVINIT seed; `free neg ctl': no GCSRCTL line).  The")
w("     development run dev1_NULL.raw already MEASURED this shape (see section 0); table 2 re-measures it as clause")
w("     (c)'s receipt for rev 3 (table 1's NULL.raw stays rev 2's).")
w("")
w("== 7. M_ONENARROW'S MECHANISM, PINNED (GLM: a future reorder would otherwise orphan the x86-64 kill silently) ==")
p3 = rd(PROBE3)
m = re.search(r"POP2 = \((.*?)\)\nPOP2_OFFS", p3, re.S)
offs = [int(x, 16) for x in re.findall(r"\((0x[0-9a-f]+), \"", m.group(1))]
names = re.findall(r", \"([A-Z0-9]+)\"\)", m.group(1))
w("  RECORDED POP2 order (frozen rev 3): %s" % " ".join("%s=0x%02x" % (n, o) for n, o in zip(names, offs)))
for o in offs:
    if (o >> 2) >= 32:
        w("  RECORDED %s at 0x%02x: latch index 0x%02x >> 2 = %d >= 32; a 32-bit shift whose count is masked to 5 bits"
          % (names[offs.index(o)], o, o, o >> 2))
        b = (o >> 2) & 31
        owner = [n for n, x in zip(names, offs) if (x >> 2) == b]
        w("           uses bit %d -- the bit of %s (0x%02x >> 2 = %d)" % (b, ",".join(owner) or "no population-2 register",
                                                                       offs[names.index(owner[0])] if owner else 0, b))
        if owner:
            i_o, i_m = names.index(owner[0]), offs.index(o)
            w("  RECORDED POP2 index of %s = %d, of %s = %d: %s is reached FIRST in `p2 ann rd' and `p2 ann wr' (both walk"
              % (owner[0], i_o, names[i_m], i_m, owner[0]))
            w("           POP2 in order), so its first access sets bit %d and MISC's first access then finds it set -- MISC's"
              % b)
            w("           announce is silenced: 25 lines in each pass 1.  No other population-2 index reaches 32.")
w("  This is the reading-derived prediction for THIS x86-64 build (Fable, grok, GLM).  The shift is UNDEFINED in C,")
w("  so no portable claim is made (Astra, D5): a build whose shift yields 0 would red all four ann rows (MISC never")
w("  latches: 27 lines in pass 1, 2 in pass 2); a build that emits a 64-bit bit-test/set with the unmasked count")
w("  would behave like the fix and SURVIVE.  Table 2 records the compiler, flags, host, the leg's object code for the")
w("  two arm lines (disassembled AFTER the run) and which row reds.")
w("")
w("== 8. THE TABLE: legs, edits and PREDICTED red rows (rev 3 frozen, fix568b; one leg at a time) ==")
for name, edit, red, ctl, note in PRED:
    if red == "BUILD_FAILS":
        w("  %-17s %-46s BUILD FAILS" % (name, edit))
    else:
        w("  %-17s %-46s %2d/38 CONTROL=%-4s red(%d): %s" % (name, edit[:46], 38 - len(red), ctl, len(red),
                                                            ", ".join(red) or "-"))
    w("  %-17s   %s" % ("", note))
w("  Predicted survivors: M_ODATA0, M_SERVED0 (equivalent today).  Every other leg must red at least one row; a")
w("  survivor is a RESULT, reported with the three-way diagnosis (mis-built / dead target / mis-cut row).")
w("  TIMING EXPECTED, so it is not mistaken for load: a two-pass session whose pass 1 stops on a fault runs pass 2")
w("  with PSR.SFRZ set and its `continue' never reaches a breakpoint (30-s budget, child killed).  Expected for")
w("  M_DROPMCTL and M_DROPMISC (both ann sessions), M_WRFAULT (both ann sessions + the non-word session) and")
w("  M_LENFAULT (the non-word session).  No row's value depends on it: those pass-2 rows report `dependent check not")
w("  exercised' from pass 1.  A leg that reds ONLY through a `timeout:' row is re-run alone before it is scored.")
w("")
w("PRETABLE2_DONE")
txt = "\n".join(out) + "\n"
io.open(os.path.join(T2, "PRETABLE2.out"), "w", encoding="latin-1", newline="").write(txt)
pj = {"rows": ROWS3, "control": CONTROL3,
      "legs": [{"leg": n, "edit": e, "red": r, "control": c, "note": t} for n, e, r, c, t in PRED],
      "channel": {r: CHANNEL[r][0] for r in ROWS3}}
io.open(os.path.join(T2, "PRETABLE2_predictions.json"), "w", encoding="latin-1", newline="").write(
    json.dumps(pj, indent=1) + "\n")
print(txt)
