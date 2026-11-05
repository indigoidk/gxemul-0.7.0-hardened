#!/usr/bin/env python3
"""sim_gate_memc.py -- gate 14's memc block AS IT SHOULD READ AFTER REPAIR 6 (r7_20261105/gate_memc_block.new) replayed over table 6's
banked logs (r7_20261105/table6/probe_*.out), the probe call replaced (marked) by a copy of each log; lib.sh's check/count verbatim
in shape (lib.sh:80-88, :326-331).  Modelled on _scratchpad/wmemc/landing/dryrun_memc.py.  No emulator runs and nothing in the repo
is written except SIM_GATE_MEMC.out: each leg runs in a temp dir (outside the repo) whose ../src/devices/dev_mvme187.c is
GXEMUL-SEC's source, so the block's source check reads the fix; one leg puts det_20261104/dev_mvme187.c.HEAD there instead.
Legs: base (want green); HEAD, the three null media, B1, B2, B3 and the eight own-latch variants (want red); `HEAD source` (base
log, HEAD's source: only the source check may red); and four SYNTHETIC logs built from base's log, one per pin
regress_20261105/REG_MYTHOS_local.md P5 says H1 never showed red -- `dead probe` (empty log: probe completed), `sentinel twice`
(sentinel once), `row lost` (one row line removed and RESULT set to 212/212: rows run, rows emitted) and `row added` (one extra
row line and RESULT 214/214: rows run, rows emitted).
Exit 0 only if base is green, every other leg red, the HEAD-source leg red on exactly the source check, and each synthetic leg red
on its named pins.
Usage: python -I sim_gate_memc.py   (Windows python; Git Bash runs the block -- a bare `bash` from Windows python is WSL's)
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(HERE)
SEC = os.path.dirname(os.path.dirname(os.path.dirname(MD)))
T6 = os.path.join(HERE, "table6")
BASH = "C:/Program Files/Git/bin/bash.exe"
BLOCK = os.path.join(HERE, "gate_memc_block.new")
OUT = os.path.join(HERE, "SIM_GATE_MEMC.out")
NL = chr(10)
EIGHT = ["L_MB_M_xori_any", "L_ME_M_xori_any", "L_DB_D_xori_any", "L_DA_D_xori_any", "L_MT_M_xori_M", "L_MW_M_xori_M",
         "L_DT_D_xori_D", "L_DT_D_idat_W.D"]

g = io.open(BLOCK, encoding="utf-8", newline="").read().split(NL)
i0 = next(k for k, x in enumerate(g) if x.startswith("MEMCLOG=$LOGDIR/mvme187_memc.log"))
i1 = next(k for k in range(i0, len(g)) if g[k].startswith('check "mvme187 memc no indexed read"'))
call = 'python3 -u mvme187_memc_probe.py "$PMAX" gate > "$MEMCLOG" 2>&1 || true'
blk = g[i0:i1 + 1]
assert blk.count(call) == 1, "the probe call line moved"
blk[blk.index(call)] = 'cp "$SRCLOG" "$MEMCLOG"   # REPLAY: the probe call replaced by a banked log'
helpers = r'''
_checks=0; _fails=0
check() { _checks=$((_checks+1)); if [ "$2" = "$3" ]; then printf "  ok   %-52s %s\n" "$1" "$2"; else printf "  FAIL %-52s got=%s want=%s\n" "$1" "$2" "$3"; _fails=$((_fails+1)); fi; }
count() { [ -f "$1" ] || { echo 0; return; }; local c; c=$(grep -ac -- "$2" "$1" 2>/dev/null); echo "${c:-0}"; }
'''
TMP = tempfile.mkdtemp(prefix="simgatememc_")
rb = os.path.join(TMP, "replay_memc.sh")
io.open(rb, "w", encoding="utf-8", newline="\n").write("#!/bin/bash\nset -u\n" + helpers + NL.join(blk) +
                                                     '\necho "REPLAY_DONE checks=$_checks fails=$_fails"\n')
fix_src = open(os.path.join(SEC, "src", "devices", "dev_mvme187.c"), "rb").read()
head_src = open(os.path.join(MD, "det_20261104", "dev_mvme187.c.HEAD"), "rb").read()
base_log = io.open(os.path.join(T6, "probe_base.out"), encoding="latin-1", newline="").read()


def synth(kind):
    lines = base_log.split(NL)
    if kind == "dead":
        return ""
    if kind == "twice":
        return base_log + "MVME187_MEMC_PROBE_DONE" + NL
    if kind == "lost":
        k = next(i for i, x in enumerate(lines) if x.startswith("R18 pc "))
        del lines[k]
        return NL.join(lines).replace("MVME187_MEMC_RESULT=213/213", "MVME187_MEMC_RESULT=212/212")
    if kind == "added":
        k = next(i for i, x in enumerate(lines) if x.startswith("R18 cnf line "))
        lines.insert(k + 1, "%-18s %-20s %-20s %-46s %s" % ("R19 extra", "yes", "yes", "a row the gate does not pin", "ok"))
        return NL.join(lines).replace("MVME187_MEMC_RESULT=213/213", "MVME187_MEMC_RESULT=214/214")
    raise ValueError(kind)


LEGS = [("base (the fix)", "probe_base.out", "green", fix_src, None),
        ("HEAD", "probe_HEAD.out", "red", fix_src, None),
        ("/bin/true", "probe_null_true.out", "red", fix_src, None),
        ("absent binary", "probe_null_absent.out", "red", fix_src, None),
        ("/bin/false", "probe_null_false.out", "red", fix_src, None),
        ("B1 memconf exit reinstated", "probe_B1_cnf_exit.out", "red", fix_src, None),
        ("B2 default exit reinstated", "probe_B2_def_exit.out", "red", fix_src, None),
        ("B3 indexed read reinstated", "probe_B3_idx_read.out", "red", fix_src, None)]
LEGS += [(n, "probe_%s.out" % n, "red", fix_src, None) for n in EIGHT]
LEGS += [("HEAD source", "probe_base.out", "srconly", head_src, None),
         ("SYNTHETIC dead probe", None, ["mvme187 memc probe completed"], fix_src, "dead"),
         ("SYNTHETIC sentinel twice", None, ["mvme187 memc sentinel once"], fix_src, "twice"),
         ("SYNTHETIC row lost", None, ["mvme187_memc rows run", "mvme187 memc rows emitted"], fix_src, "lost"),
         ("SYNTHETIC row added", None, ["mvme187_memc rows run", "mvme187 memc rows emitted"], fix_src, "added")]
out = ["gate 14's memc block AFTER REPAIR 6 (r7_20261105/gate_memc_block.new) replayed by sim_gate_memc.py over table 6's banked logs",
       "(r7_20261105/table6/probe_*.out); the probe call replaced, marked, by a copy of each log; SYNTHETIC legs are built from base's log.", ""]
ok = True
for name, f, want, src, kind in LEGS:
    td = tempfile.mkdtemp(dir=TMP)
    for d in ("src/devices", "regress", "log"):
        os.makedirs(os.path.join(td, d))
    open(os.path.join(td, "src", "devices", "dev_mvme187.c"), "wb").write(src)
    srclog = os.path.join(td, "banked.out")
    if kind:
        io.open(srclog, "w", encoding="latin-1", newline="").write(synth(kind))
    else:
        shutil.copyfile(os.path.join(T6, f), srclog)
    env = dict(os.environ, LOGDIR=os.path.join(td, "log").replace("\\", "/"), PMAX="/nonexistent/gxemul",
               SRCLOG=srclog.replace("\\", "/"))
    r = subprocess.run([BASH, rb.replace("\\", "/")], capture_output=True, cwd=os.path.join(td, "regress"), env=env)
    text = r.stdout.decode("latin-1").replace("\r", "")
    m = re.search(r"REPLAY_DONE checks=(\d+) fails=(\d+)", text)
    fails = [x for x in text.split(NL) if x.startswith("  FAIL ")]
    failnames = [re.match(r"  FAIL (.*?)\s+got=", x).group(1).strip() for x in fails]
    if not m:
        verdict = "NO REPLAY_DONE"
        good = False
    elif want == "green":
        good = int(m.group(2)) == 0
        verdict = "green" if good else "RED"
    elif want == "red":
        good = int(m.group(2)) > 0
        verdict = "red" if good else "GREEN"
    elif want == "srconly":
        good = failnames == ["mvme187 memc no indexed read"]
        verdict = "red on the source check only" if good else "WRONG: %s" % failnames
    else:
        good = all(p in failnames for p in want)
        verdict = ("red on %s" % ", ".join(want)) if good else "WRONG: wanted %s red, got %s" % (want, failnames)
    ok = ok and good
    out.append("--- %s (%s): %s  [%s]" % (name, f or "synthetic:" + kind, m.group(0) if m else "no result", verdict))
    out.extend("    " + x.strip() for x in fails[:12])
    if len(fails) > 12:
        out.append("    ... %d more FAIL lines" % (len(fails) - 12))
out.append("")
out.append("SIM_GATE_MEMC: %s" % ("PASS (base green, every other leg red as wanted)" if ok else "FAIL"))
io.open(OUT, "w", encoding="utf-8", newline="\n").write(NL.join(out) + NL)
shutil.rmtree(TMP, ignore_errors=True)
print(NL.join(out[-3:]))
sys.exit(0 if ok else 1)
