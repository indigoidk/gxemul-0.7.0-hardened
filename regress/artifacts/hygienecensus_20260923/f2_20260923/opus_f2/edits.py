#!/usr/bin/env python3
"""opus measuring seat, hygienecensus F2 pass -- ONE named edit per case, applied to a COPY of regress/.

usage:  edits.py <case> <regress-dir>      apply the edit, print what was changed
        edits.py --desc <case>             print the one-line description
Every edit asserts its anchor text is present (and unique where it says so), so a case can never
silently apply nothing -- a MUTANT-TEXT-NOT-FOUND is a hard error, which also pins the anchor.
"""
import io, os, re, shutil, sys

L = "luna_absentcpu_probe.py"          # pty-driving, prompt-detecting, NOT whole-buffer-allowlisted
BDT = "arm_bdt_probe.py"               # allowlisted whole-buffer file (1 line)
FLG = "arm_flags_probe.py"             # allowlisted whole-buffer file (2 lines)
PL = "pcc2_width_probe.py"             # a grandfathered PROMPTLESS pty probe, used as a template

D = None
def P(f): return os.path.join(D, f)
def rd(f): return io.open(P(f), encoding="utf-8", newline="").read()
def wr(f, s): io.open(P(f), "w", encoding="utf-8", newline="").write(s)
def app(f, *lines):
    s = rd(f)
    if not s.endswith("\n"): s += "\n"
    wr(f, s + "".join(l + "\n" for l in lines))
    for l in lines: print("  append %s: %s" % (f, l))
def sub(f, old, new, unique=True):
    s = rd(f); n = s.count(old)
    assert n >= 1, ("ANCHOR NOT FOUND", f, old)
    if unique: assert n == 1, ("ANCHOR NOT UNIQUE", f, old, n)
    wr(f, s.replace(old, new, 1))
    print("  %s: -%s\n  %s  +%s" % (f, old.replace("\n", "\n   -"), " " * len(f), new.replace("\n", "\n   +")))
def cp(src, dst):
    os.makedirs(os.path.dirname(P(dst)) or D, exist_ok=True)
    shutil.copy2(P(src), P(dst)); print("  copy %s -> %s" % (src, dst))

SITE = '_control_site = lambda buf: buf.rstrip().endswith("GXemul>")'
C = {}
def case(name, desc):
    def deco(fn): C[name] = (desc, fn); return fn
    return deco

# ---------------- PART 1: the fourteen from pass 2, byte-for-byte the same edits -----------------
@case("e_c1", "c1  a 4th whole-buffer site, SINGLE-quoted, in a non-allowlisted pty probe")
def _(): app(L, "_control_site = lambda buf: buf.rstrip().endswith('GXemul>')")
@case("e_e1", "e1  a whole-buffer site on another buffer NAME (out)")
def _(): app(L, '_control_site = lambda out: out.rstrip().endswith("GXemul>")')
@case("e_e2", "e2  a whole-buffer site SPLIT across two lines")
def _(): app(L, '_control_site = lambda buf: (buf.rstrip()', '                             .endswith("GXemul>"))')
@case("e_e3", "e3  a whole-buffer site with a SPACE before endswith's paren")
def _(): app(L, '_control_site = lambda buf: buf.rstrip().endswith ("GXemul>")')
@case("e_e4", "e4  a whole-buffer SLICE compare, no endswith at all")
def _(): app(L, '_control_site = lambda buf: buf.rstrip()[-7:] == "GXemul>"')
@case("e_e5", "e5  a whole-buffer site with strip() for rstrip()")
def _(): app(L, '_control_site = lambda buf: buf.strip().endswith("GXemul>")')
@case("e_e6", "e6  a site MOVED arm_flags -> arm_bdt (arm_flags one site -> slice; arm_bdt gains one)")
def _():
    sub(FLG, 'if buf.rstrip().endswith("GXemul>"):', 'if buf.rstrip()[-7:] == "GXemul>":', unique=False)
    app(BDT, SITE)
@case("e_e7", "e7  a NEW promptless pty probe whose FILE NAME holds a space")
def _(): cp(PL, "zz opus_newprobe.py")
@case("e_e9", "e9  the #37 BARE defect itself with one space: buf.endswith (\">\")")
def _(): app(L, '_control_site = lambda buf: buf.endswith (">")')
@case("e_e14", "e14 a grandfathered promptless probe RENAMED (a swap: one leaves, one arrives)")
def _(): os.rename(P("gdrom_cond_probe.py"), P("zz_renamed_cond_probe.py")); print("  rename gdrom_cond_probe.py -> zz_renamed_cond_probe.py")
@case("e_dL1", "dL1 an UNRECOGNISED spelling endswith(PROMPT), then --write")
def _(): app(L, '_control_site = lambda buf: buf.rstrip().endswith(PROMPT)')
@case("e_dL2", "dL2 a 4th whole-buffer site inside an ALLOWLISTED file (arm_bdt), then --write")
def _(): app(BDT, SITE)
@case("e_dL3", "dL3 a NEW promptless pty probe in a new SUBDIRECTORY, then --write")
def _(): cp(PL, "newsub/zz_opus_subprobe.py")
@case("e_dL5", "dL5 a NEW promptless pty probe whose only endswith( is a full-line COMMENT, then --write")
def _():
    cp(PL, "zz_opus_newprobe.py"); app("zz_opus_newprobe.py", "# readiness: fixed waits, no endswith( predicate here")

# ---------------- PART 2: new edits -----------------
AE_OLD = '            if len(buf) > mark and buf[mark:].rstrip().endswith("GXemul>"):\n'
@case("n1a", "PROMPTLESS HIDDEN BY A TRAILING COMMENT: arm_endian's only predicate -> `len(buf) > mark`, old text kept as a trailing comment")
def _(): sub("arm_endian_probe.py", AE_OLD, '            if len(buf) > mark:  # was: buf[mark:].rstrip().endswith("GXemul>")\n')
@case("n1b", "PROMPTLESS HIDDEN BY A STRING: arm_endian's predicate conjunct wrapped in quotes (a truthy constant)")
def _(): sub("arm_endian_probe.py", AE_OLD, "            if len(buf) > mark and \"buf[mark:].rstrip().endswith('GXemul>')\":\n")
@case("n1c", "PROMPTLESS HIDDEN BY A DOCSTRING: arm_endian's wait_from gains a docstring naming the predicate; the predicate goes")
def _():
    sub("arm_endian_probe.py",
        '    def wait_from(mark, timeout=30):\n        t = time.time()\n',
        '    def wait_from(mark, timeout=30):\n        """Ready once the slice after `mark` endswith("GXemul>") -- or once anything arrives."""\n        t = time.time()\n')
    sub("arm_endian_probe.py", AE_OLD, '            if len(buf) > mark:\n')
@case("n1d", "#392 ANCHOR HIDDEN BY A TRAILING COMMENT: mips_rounding's anchored predicate -> `len(buf) > mark`, old text as a comment")
def _(): sub("mips_rounding_probe.py", '            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):\n',
             '            if len(buf) > mark:  # resp.rstrip().endswith("GXemul>")\n')
@case("n2a", "NEW promptless probe, endswith(\"GXemul>\") only in its module DOCSTRING (then --write)")
def _():
    cp(PL, "zz_opus_docprobe.py")
    sub("zz_opus_docprobe.py", '"""pcc2widthkills DETECTOR --', '"""pcc2widthkills DETECTOR (timed drains; no endswith("GXemul>") wait) --')
@case("n2b", "NEW promptless probe, endswith(\"GXemul>\") only in a TRAILING comment (then --write)")
def _():
    cp(PL, "zz_opus_trailprobe.py")
    sub("zz_opus_trailprobe.py", 'import os, pty, re, select, sys, time\n',
        'import os, pty, re, select, sys, time  # timed drains, no endswith("GXemul>") wait\n')
@case("n3a", "whole-buffer site, space INSIDE rstrip's parens: buf.rstrip( ).endswith(\"GXemul>\")")
def _(): app(L, '_control_site = lambda buf: buf.rstrip( ).endswith("GXemul>")')
@case("n3b", "whole-buffer site, extra parens round the receiver: (buf).rstrip().endswith(\"GXemul>\")")
def _(): app(L, '_control_site = lambda buf: (buf).rstrip().endswith("GXemul>")')
@case("n3c", "whole-buffer site, extra parens round the chain: (buf.rstrip()).endswith(\"GXemul>\")")
def _(): app(L, '_control_site = lambda buf: (buf.rstrip()).endswith("GXemul>")')
@case("n3d", "CONTROL: spaces INSIDE endswith's parens: buf.rstrip().endswith( \"GXemul>\" )")
def _(): app(L, '_control_site = lambda buf: buf.rstrip().endswith( "GXemul>" )')
@case("n3e", "CONTROL: extra parens round endswith's ARGUMENT: buf.rstrip().endswith((\"GXemul>\"))")
def _(): app(L, '_control_site = lambda buf: buf.rstrip().endswith(("GXemul>"))')
@case("n3f", "whole-buffer site, rstrip with an argument: buf.rstrip(\"\\r\\n\").endswith(\"GXemul>\")")
def _(): app(L, r'_control_site = lambda buf: buf.rstrip("\r\n").endswith("GXemul>")')
@case("n3g", "whole-buffer site, space before .rstrip: buf .rstrip().endswith(\"GXemul>\")")
def _(): app(L, '_control_site = lambda buf: buf .rstrip().endswith("GXemul>")')
@case("n3h", "whole-buffer site, receiver self.buffer (single quotes): self.buffer.rstrip().endswith('GXemul>')")
def _(): app(L, "_control_site = lambda self: self.buffer.rstrip().endswith('GXemul>')")
@case("n3i", "whole-buffer REGEX readiness: re.search(r\"GXemul>\\s*$\", buf)")
def _(): app(L, r'_control_site = lambda buf: re.search(r"GXemul>\s*$", buf) is not None')
@case("n3j", "a 2nd whole-buffer site ON AN ALLOWLISTED LINE (arm_bdt:76 gains `or self.rxbuf.rstrip().endswith(...)`)")
def _(): sub(BDT, '            if self.buf.rstrip().endswith("GXemul>"):\n',
             '            if self.buf.rstrip().endswith("GXemul>") or self.rxbuf.rstrip().endswith("GXemul>"):\n')
@case("n3m", "a site MOVED arm_bdt -> arm_flags: arm_bdt's line anchored + old text as a trailing comment; arm_flags:144 gains a 2nd site")
def _():
    sub(BDT, '            if self.buf.rstrip().endswith("GXemul>"):\n',
        '            if len(self.buf) > self.mark and self.buf[self.mark:].rstrip().endswith("GXemul>"):  # was: self.buf.rstrip().endswith("GXemul>")\n')
    sub(FLG, '            if buf.rstrip().endswith("GXemul>"):\n                return True\n',
        '            if buf.rstrip().endswith("GXemul>") or rxbuf.rstrip().endswith("GXemul>"):\n                return True\n', unique=False)
@case("n3k", "a whole-buffer readiness HELPER module (no pty.fork, no drive_guest import): new regress/zz_ready_util.py")
def _():
    io.open(P("zz_ready_util.py"), "w", encoding="utf-8", newline="").write(
        '"""Readiness helper shared by probes."""\n\n\ndef at_prompt(buf):\n    return buf.rstrip().endswith("GXemul>")\n')
    print("  new zz_ready_util.py: def at_prompt(buf): return buf.rstrip().endswith(\"GXemul>\")")
@case("n3k2", "n3k + m88k_exc_probe.py's fallback test switched to the helper (2 files)")
def _():
    C["n3k"][1]()
    sub("m88k_exc_probe.py", 'import os, pty, re, select, struct, sys, time\n', 'import os, pty, re, select, struct, sys, time\nimport zz_ready_util\n')
    sub("m88k_exc_probe.py", '    if not s.buf[mark:].rstrip().endswith("GXemul>"):\n', '    if not zz_ready_util.at_prompt(s.buf):\n')
@case("n4a", "NEW promptless probe that forks its pty with os.forkpty() (in pty_driving's population, not in _ptylist's)")
def _():
    cp(PL, "zz_opus_forkpty_probe.py")
    sub("zz_opus_forkpty_probe.py", "pty.fork/execv", "forkpty/execv")
    sub("zz_opus_forkpty_probe.py", "pid, fd = pty.fork()", "pid, fd = os.forkpty()")
    assert not re.search(r"pty.fork", rd("zz_opus_forkpty_probe.py")), "pty.fork still matches"
@case("n5a", "NEW promptless probe in a SUBDIRECTORY under a PROMPT-DETECTING top-level basename (newsub/luna_absentcpu_probe.py), then --write")
def _(): cp(PL, "newsub/" + L)
@case("n5b", "NEW promptless probe in a SUBDIRECTORY under a GRANDFATHERED basename (newsub/gdrom_cond_probe.py), then --grandfather + --write")
def _(): cp(PL, "newsub/gdrom_cond_probe.py")
MS_OLD = ('            resp = buf[mark:]\n'
          '            #  #392: the ECHO first -- a prompt in the slice proves\n'
          '            #  nothing until the debugger has taken the command.\n'
          '            if echo is not None and echo not in resp:\n'
          '                continue\n'
          '            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):\n'
          '                return True\n'
          '        return False\n'
          '\n'
          '    def send(s):\n'
          '        b = (s + "\\n").encode("latin1")\n'
          '        _mark = len(buf)\n'
          '        n = 0\n'
          '        while n < len(b):\n'
          '            n += os.write(fd, b[n:])\n'
          '        return wait(mark=_mark, echo=s if s else None)\n')
MS_NEW = ('            if len(buf) > mark and buf[mark:].rstrip().endswith("GXemul>"):\n'
          '                return True\n'
          '        return False\n'
          '\n'
          '    def send(s):\n'
          '        b = (s + "\\n").encode("latin1")\n'
          '        _mark = len(buf)\n'
          '        n = 0\n'
          '        while n < len(b):\n'
          '            n += os.write(fd, b[n:])\n'
          '        return wait(mark=_mark)\n')
@case("n6", "#392 FALL: mips_subnorm session 1 loses its echo guard (anchor respelled, echo arg dropped) -- 3 counts fall together, then --write")
def _(): sub("mips_subnorm_probe.py", MS_OLD, MS_NEW)
@case("n7", "dL2's edit (4th site in arm_bdt), --write with WHOLE_FULL_RULING=no")
def _(): app(BDT, SITE)
@case("n8", "ONE-CHARACTER GATE EDIT: probe_code's find -name '*.py' -> '*.pyx' (the #392 enumerator sees nothing), then --write")
def _():
    sub("gate_hygiene.sh", "probe_code() { find \"$HERE\" -name '*.py'", "probe_code() { find \"$HERE\" -name '*.pyx'")
@case("n9", "a GRANDFATHERED promptless probe gains a trailing-comment endswith(\"GXemul>\"), then --release + --write")
def _(): app("gdrom_cond_probe.py", '_READINESS = "timed drains"  # no endswith("GXemul>") wait in this probe')
@case("n10", "the #37 BARE form as a slice: buf.rstrip()[-1:] == \">\"")
def _(): app(L, '_control_site = lambda buf: buf.rstrip()[-1:] == ">"')
@case("n11", "an allowlisted site RESPELLED, not converted: arm_flags:144 -> (buf).rstrip().endswith(\"GXemul>\"), then --write (the SHRINK branch)")
def _(): sub(FLG, '            if buf.rstrip().endswith("GXemul>"):\n                return True\n',
             '            if (buf).rstrip().endswith("GXemul>"):\n                return True\n', unique=False)
@case("n8b", "ONE-CHARACTER GATE EDIT: pty_driving's find -name '*.py' -> '*.pyx' (the whole-buffer enumerator sees nothing), then --write")
def _(): sub("gate_hygiene.sh", "pty_driving() { find \"$HERE\" -name '*.py'", "pty_driving() { find \"$HERE\" -name '*.pyx'")
@case("n12", "Q1(a) CONTROL: a PROMPT-DETECTING probe in a subdirectory (copy of arm_endian_probe.py -> newsub/zz_endian_copy_probe.py)")
def _(): cp("arm_endian_probe.py", "newsub/zz_endian_copy_probe.py")
@case("clone","FRESH-CLONE SIMULATION: the working tree minus its three untracked probes (crime_width, arm_msrmode, lca_isaphys)")
def _():
    for f in ("crime_width_probe.py", "arm_msrmode_probe.py", "lca_isaphys_probe.py"):
        os.remove(P(f)); print("  remove " + f)

if __name__ == "__main__":
    if sys.argv[1] == "--desc":
        print(C[sys.argv[2]][0]); sys.exit(0)
    D = sys.argv[2]
    C[sys.argv[1]][1]()
