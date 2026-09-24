#!/usr/bin/env python3
"""Opus seat, #545 q2r: one-line variants of the five declined arms of dev_footbridge.c,
each built into the FROZEN 491-row harness and scored row by row.

Mutates ONLY /tmp/opusq2r/src/devices/dev_footbridge.c (a scratch copy), behind a
/tmp/opusq2r/.MUTANT sentinel; restores from the FROZEN copy and cmp-verifies at the end,
then rebuilds and re-runs the baseline before clearing the sentinel.
A variant whose anchor text is not found exactly once is recorded as ANCHOR-ERROR, never
as green.
"""
import hashlib, os, re, subprocess, sys, time, difflib

X = "/tmp/opusq2r"
P = "/mnt/c/DocumentNoSnc/cc/GXEMUL"
FROZEN = P + "/_scratchpad/fbd5/q2r/frozen/dev_footbridge.c"
OUT = P + "/_scratchpad/fbd5/q2r/opus"
SRC = X + "/src/devices/dev_footbridge.c"
REG = X + "/regress"
LOGS = X + "/logs"
DIFFS = X + "/diffs"
SENT = X + "/.MUTANT"

GCC = ["gcc", "-O2", "-std=c99", "-D_POSIX_C_SOURCE=200809L", "-D_DEFAULT_SOURCE",
       "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
       "-I" + X + "/src", "-I" + X + "/src/include", "-I" + X + "/src/include/thirdparty",
       "-o", "dv", "diff_footbridge.c", "-lm"]

frozen = open(FROZEN, encoding="utf-8", newline="").read()

L = ["warned_irq_status_w", "warned_irq_raw_w", "warned_irq_clear_r", "warned_fiq_status_w", "warned_fiq_raw_w"]
F = ["irq_status", "irq_enable", "fiq_status", "fiq_enable"]

ARMS = {
    "A0": dict(nm="IRQ_STATUS",
               dir_old="\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->irq_status & d->irq_enable;",
               dir_head="\t\tif (writeflag == MEM_READ", dir_tail=")\n\t\t\todata = d->irq_status & d->irq_enable;",
               flag_old="\t\telse if (!d->warned_irq_status_w) {",
               flag_head="\t\telse if (!d->warned_irq_status_w", flag_tail=") {",
               flag_swap="\t\telse if (!d->%s) {",
               body_old="\t\t\td->warned_irq_status_w = 1;",
               read_old="\t\t\todata = d->irq_status & d->irq_enable;", rw="MEM_READ"),
    "A1": dict(nm="IRQ_RAW_STATUS",
               dir_old="\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->irq_status;",
               dir_head="\t\tif (writeflag == MEM_READ", dir_tail=")\n\t\t\todata = d->irq_status;",
               flag_old="\t\telse if (!d->warned_irq_raw_w) {",
               flag_head="\t\telse if (!d->warned_irq_raw_w", flag_tail=") {",
               flag_swap="\t\telse if (!d->%s) {",
               body_old="\t\t\td->warned_irq_raw_w = 1;",
               read_old="\t\t\todata = d->irq_status;\n\t\telse if (!d->warned_irq_raw_w) {", rw="MEM_READ"),
    "A2": dict(nm="IRQ_ENABLE_CLEAR",
               dir_old="\t\tif (writeflag == MEM_WRITE) {\n\t\t\td->irq_enable &= ~idata;",
               dir_head="\t\tif (writeflag == MEM_WRITE", dir_tail=") {\n\t\t\td->irq_enable &= ~idata;",
               flag_old="\t\t} else if (!d->warned_irq_clear_r) {",
               flag_head="\t\t} else if (!d->warned_irq_clear_r", flag_tail=") {",
               flag_swap="\t\t} else if (!d->%s) {",
               body_old="\t\t\td->warned_irq_clear_r = 1;",
               read_old=None, rw="MEM_WRITE"),
    "A3": dict(nm="FIQ_STATUS",
               dir_old="\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->fiq_status & d->fiq_enable;",
               dir_head="\t\tif (writeflag == MEM_READ", dir_tail=")\n\t\t\todata = d->fiq_status & d->fiq_enable;",
               flag_old="\t\telse if (!d->warned_fiq_status_w) {",
               flag_head="\t\telse if (!d->warned_fiq_status_w", flag_tail=") {",
               flag_swap="\t\telse if (!d->%s) {",
               body_old="\t\t\td->warned_fiq_status_w = 1;",
               read_old="\t\t\todata = d->fiq_status & d->fiq_enable;", rw="MEM_READ"),
    "A4": dict(nm="FIQ_RAW_STATUS",
               dir_old="\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->fiq_status;",
               dir_head="\t\tif (writeflag == MEM_READ", dir_tail=")\n\t\t\todata = d->fiq_status;",
               flag_old="\t\telse if (!d->warned_fiq_raw_w) {",
               flag_head="\t\telse if (!d->warned_fiq_raw_w", flag_tail=") {",
               flag_swap="\t\telse if (!d->%s) {",
               body_old="\t\t\td->warned_fiq_raw_w = 1;",
               read_old="\t\t\todata = d->fiq_status;\n\t\telse if (!d->warned_fiq_raw_w) {", rw="MEM_READ"),
}
ARM_IDX = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4}

V = []   # (vid, family, arm, old, new, text)


def add(vid, fam, arm, old, new, text):
    V.append((vid, fam, arm, old, new, text))


def dirc(arm, op, c):
    a = ARMS[arm]
    return a["dir_old"], a["dir_head"] + " " + op + " (" + c + ")" + a["dir_tail"], \
        "if (writeflag == %s %s (%s))" % (a["rw"], op, c)


def flagc(arm, op, c):
    a = ARMS[arm]
    own = L[ARM_IDX[arm]]
    return a["flag_old"], a["flag_head"] + " " + op + " (" + c + ")" + a["flag_tail"], \
        "else if (!d->%s %s (%s))" % (own, op, c)


for arm in ["A0", "A1", "A2", "A3", "A4"]:
    ai = ARM_IDX[arm]
    own = L[ai]
    for f in F:
        add("a_pos_%s_%s" % (arm, f), "a_pos", arm, *dirc(arm, "&&", "d->" + f))
        add("a_neg_%s_%s" % (arm, f), "a_neg", arm, *dirc(arm, "&&", "!d->" + f))
    for li, l in enumerate(L):
        tag = "own" if li == ai else ("later" if li > ai else "earlier")
        add("b_pos_%s_L%d%s" % (arm, li, tag[0]), "b_pos", arm, *dirc(arm, "&&", "d->" + l))
        add("b_neg_%s_L%d%s" % (arm, li, tag[0]), "b_neg", arm, *dirc(arm, "&&", "!d->" + l))
    for nm, c in [("len4", "len == 4"), ("lenne1", "len != 1"), ("lenne2", "len != 2")]:
        add("c_dir_%s_%s" % (arm, nm), "c_dir", arm, *dirc(arm, "&&", c))
    for nm, c in [("len4", "len == 4"), ("lenne1", "len != 1")]:
        add("c_flag_%s_%s" % (arm, nm), "c_flag", arm, *flagc(arm, "&&", c))
    for f in F:
        add("d_pos_%s_%s" % (arm, f), "d_pos", arm, *flagc(arm, "&&", "d->" + f))
        add("d_neg_%s_%s" % (arm, f), "d_neg", arm, *flagc(arm, "&&", "!d->" + f))
    for li, l in enumerate(L):
        if li == ai:
            continue
        tag = "later" if li > ai else "earlier"
        add("fl_pos_%s_L%d%s" % (arm, li, tag[0]), "fl_pos", arm, *flagc(arm, "&&", "d->" + l))
        add("fl_neg_%s_L%d%s" % (arm, li, tag[0]), "fl_neg", arm, *flagc(arm, "&&", "!d->" + l))
    for f in F:
        add("e_dir_%s_%s" % (arm, f), "e_dir", arm, *dirc(arm, "&&", "d->%s != 0x10" % f))
        add("e_flag_%s_%s" % (arm, f), "e_flag", arm, *flagc(arm, "&&", "d->%s != 0x10" % f))
    for f in F:
        add("bit_dir_b1_%s_%s" % (arm, f), "bit_dir_b1", arm, *dirc(arm, "&&", "!(d->%s & 0xff00u)" % f))
        add("bit_dir_b3_%s_%s" % (arm, f), "bit_dir_b3", arm, *dirc(arm, "&&", "!(d->%s & 0xff000000u)" % f))
        add("bit_flag_b1_%s_%s" % (arm, f), "bit_flag_b1", arm, *flagc(arm, "&&", "!(d->%s & 0xff00u)" % f))
    for li, l in enumerate(L):
        tag = "own" if li == ai else ("later" if li > ai else "earlier")
        add("or_L_%s_L%d%s" % (arm, li, tag[0]), "or_L", arm, *dirc(arm, "||", "d->" + l))
    for f in F:
        add("or_Fpos_%s_%s" % (arm, f), "or_F", arm, *dirc(arm, "||", "d->" + f))
        add("or_Fneg_%s_%s" % (arm, f), "or_F", arm, *dirc(arm, "||", "!d->" + f))
    a = ARMS[arm]
    for li, l in enumerate(L):
        if li == ai:
            continue
        tag = "later" if li > ai else "earlier"
        add("swap_flag_%s_L%d%s" % (arm, li, tag[0]), "swap_flag", arm, a["flag_old"], a["flag_swap"] % l,
            "flag operand -> else if (!d->%s)" % l)
        add("swap_body_%s_L%d%s" % (arm, li, tag[0]), "swap_body", arm, a["body_old"], "\t\t\td->%s = 1;" % l,
            "decline body sets d->%s = 1 instead of its own latch" % l)
    # direction-test operand forms
    if arm == "A2":
        add("dir_eq_A2", "dir_eq", arm, a["dir_old"], a["dir_old"].replace("writeflag == MEM_WRITE", "writeflag != MEM_READ"),
            "if (writeflag != MEM_READ)")
        add("dir_idata_A2", "dir_eq", arm, a["dir_old"], a["dir_old"].replace("writeflag == MEM_WRITE", "idata"),
            "if (idata)")
    else:
        add("dir_eq_%s" % arm, "dir_eq", arm, a["dir_old"], a["dir_old"].replace("writeflag == MEM_READ", "writeflag != MEM_WRITE"),
            "if (writeflag != MEM_WRITE)")
        add("dir_idata_%s" % arm, "dir_eq", arm, a["dir_old"], a["dir_old"].replace("writeflag == MEM_READ", "!idata"),
            "if (!idata)")

# value-specific controls that DO coincide with a seed (the machinery must be able to kill this shape)
add("e_ctl_A0_ie30", "e_ctl", "A0", *dirc("A0", "&&", "d->irq_enable != 0x30"))
add("e_ctl_A0flag_is18", "e_ctl", "A0", *flagc("A0", "&&", "d->irq_status != 0x18"))
add("e_ctl_A2_ie30", "e_ctl", "A2", *dirc("A2", "&&", "d->irq_enable != 0x30"))

# byte-lane edits (OUTSIDE the predicate bound: read expressions and decline bodies) -- the wide
# state's lanes: is 0x80010018, ie 0x00010030, fs 0x40020060, fe 0x000200c0 -- byte 1 is 0 everywhere
LANE = [
    ("lane_A0_read_b1", "A0", "\t\t\todata = d->irq_status & d->irq_enable;",
     "\t\t\todata = d->irq_status & d->irq_enable & 0xffff00ffu;", "odata = d->irq_status & d->irq_enable & 0xffff00ffu"),
    ("lane_A0_read_b3", "A0", "\t\t\todata = d->irq_status & d->irq_enable;",
     "\t\t\todata = d->irq_status & d->irq_enable & 0x00ffffffu;", "odata = d->irq_status & d->irq_enable & 0x00ffffffu"),
    ("lane_A1_read_b1", "A1", "\t\t\todata = d->irq_status;\n\t\telse if (!d->warned_irq_raw_w) {",
     "\t\t\todata = d->irq_status & 0xffff00ffu;\n\t\telse if (!d->warned_irq_raw_w) {", "odata = d->irq_status & 0xffff00ffu"),
    ("lane_A3_read_b1", "A3", "\t\t\todata = d->fiq_status & d->fiq_enable;",
     "\t\t\todata = d->fiq_status & d->fiq_enable & 0xffff00ffu;", "odata = d->fiq_status & d->fiq_enable & 0xffff00ffu"),
    ("lane_A3_read_b3", "A3", "\t\t\todata = d->fiq_status & d->fiq_enable;",
     "\t\t\todata = d->fiq_status & d->fiq_enable & 0x00ffffffu;", "odata = d->fiq_status & d->fiq_enable & 0x00ffffffu"),
    ("lane_A4_read_b1", "A4", "\t\t\todata = d->fiq_status;\n\t\telse if (!d->warned_fiq_raw_w) {",
     "\t\t\todata = d->fiq_status & 0xffff00ffu;\n\t\telse if (!d->warned_fiq_raw_w) {", "odata = d->fiq_status & 0xffff00ffu"),
    ("lane_A0_body_is_b1", "A0", "\t\t\td->warned_irq_status_w = 1;",
     "\t\t\td->warned_irq_status_w = 1; d->irq_status &= 0xffff00ffu;", "decline body also: d->irq_status &= 0xffff00ffu"),
    ("lane_A0_body_ie_b3", "A0", "\t\t\td->warned_irq_status_w = 1;",
     "\t\t\td->warned_irq_status_w = 1; d->irq_enable &= 0x00ffffffu;", "decline body also: d->irq_enable &= 0x00ffffffu"),
    ("lane_A3_body_fe_b3", "A3", "\t\t\td->warned_fiq_status_w = 1;",
     "\t\t\td->warned_fiq_status_w = 1; d->fiq_enable &= 0x00ffffffu;", "decline body also: d->fiq_enable &= 0x00ffffffu"),
    ("lane_A2_body_ie_b1", "A2", "\t\t\td->warned_irq_clear_r = 1;",
     "\t\t\td->warned_irq_clear_r = 1; d->irq_enable &= 0xffff00ffu;", "decline body also: d->irq_enable &= 0xffff00ffu"),
]
for vid, arm, old, new, text in LANE:
    add(vid, "lane", arm, old, new, text)

# idata-keyed legal-write conjuncts at +0x18c (OUTSIDE the stated bound: idata is read by the legal branch only)
add("idata_A2_ne20", "idata", "A2", *dirc("A2", "&&", "idata != 0x20"))
add("idata_A2_hi", "idata", "A2", *dirc("A2", "&&", "!(idata >> 8)"))

# The two predicates that DOMINATE every arm's decline but are not in the brief's list (case label,
# direction test, latch): the idata load at the function head, and the timer-fold range test.
# Selected only when named ("dom"), so the 425-row table above is unchanged by adding them.
if "dom" in sys.argv[1:]:
    IDL = "\tif (writeflag == MEM_WRITE)\n\t\tidata = memory_readmax64(cpu, data, len);\n\n\tif (relative_addr >= TIMER_1_LOAD"
    FOLD = "\tif (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {"
    add("dom_idata_len4", "dom", "head", IDL, IDL.replace("writeflag == MEM_WRITE)", "writeflag == MEM_WRITE && len == 4)"),
        "if (writeflag == MEM_WRITE && len == 4) idata = memory_readmax64(...)")
    add("dom_idata_lenne1", "dom", "head", IDL, IDL.replace("writeflag == MEM_WRITE)", "writeflag == MEM_WRITE && len != 1)"),
        "if (writeflag == MEM_WRITE && len != 1) idata = memory_readmax64(...)")
    add("dom_fold_from180", "dom", "head", FOLD, FOLD.replace(">= TIMER_1_LOAD", ">= IRQ_STATUS"),
        "if (relative_addr >= IRQ_STATUS && relative_addr <= TIMER_4_CLEAR) {  (timer fold widened)")
    add("dom_fold_from100", "dom", "head", FOLD, FOLD.replace(">= TIMER_1_LOAD", ">= 0x100"),
        "if (relative_addr >= 0x100 && relative_addr <= TIMER_4_CLEAR) {  (timer fold widened)")

# The CASE LABEL is the third dominating predicate the brief lists; its one-line widening is an extra label.
if "case" in sys.argv[1:]:
    for vid, old, new, text in [
        ("case_A0_1a0", "\tcase IRQ_STATUS:\n", "\tcase 0x1a0: case IRQ_STATUS:\n", "case 0x1a0: case IRQ_STATUS:"),
        ("case_A1_1a4", "\tcase IRQ_RAW_STATUS:\n", "\tcase 0x1a4: case IRQ_RAW_STATUS:\n", "case 0x1a4: case IRQ_RAW_STATUS:"),
        ("case_A2_1ac", "\tcase IRQ_ENABLE_CLEAR:\n", "\tcase 0x1ac: case IRQ_ENABLE_CLEAR:\n", "case 0x1ac: case IRQ_ENABLE_CLEAR:"),
        ("case_A3_2a0", "\tcase FIQ_STATUS:\n", "\tcase 0x2a0: case FIQ_STATUS:\n", "case 0x2a0: case FIQ_STATUS:"),
        ("case_A4_2a4", "\tcase FIQ_RAW_STATUS:\n", "\tcase 0x2a4: case FIQ_RAW_STATUS:\n", "case 0x2a4: case FIQ_RAW_STATUS:")]:
        add(vid, "case", vid.split("_")[1], old, new, text)

assert len(set(v[0] for v in V)) == len(V), "duplicate variant ids"
only = set(sys.argv[1:])
if only:
    V = [v for v in V if v[0] in only or v[1] in only]
    assert V, "subset selected nothing"


def sh(cmd, cwd=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def parse(out):
    rows = fails = None
    verdict = "NONE"
    failing = []
    for ln in out.splitlines():
        m = re.match(r"^(\d+) rows, (\d+) failures$", ln)
        if m:
            rows, fails = int(m.group(1)), int(m.group(2))
        if ln.startswith("DIFF_FOOTBRIDGE_"):
            verdict = ln.strip()
        if ln.startswith("  FAIL  ") and "@@SELFCHECK@@" not in ln:
            failing.append(ln[8:].rstrip())
    return rows, fails, verdict, failing


def build_and_run(tag):
    if os.path.exists(REG + "/dv"):
        os.remove(REG + "/dv")
    b = sh(GCC, cwd=REG)
    if b.returncode != 0 or not os.path.exists(REG + "/dv"):
        return dict(build="BUILD-FAIL", err=b.stderr[-600:])
    if os.path.getmtime(REG + "/dv") < os.path.getmtime(SRC):
        return dict(build="STALE-BINARY", err="")
    bmd5 = md5(REG + "/dv")
    try:
        r = sh(["./dv"], cwd=REG, timeout=120)
        out, rc = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        so = e.stdout or ""
        out, rc = (so.decode("utf-8", "replace") if isinstance(so, bytes) else so), "TIMEOUT"
    open(LOGS + "/" + tag + ".log", "w", encoding="utf-8").write(out)
    rows, fails, verdict, failing = parse(out)
    return dict(build="ok", bmd5=bmd5, rc=rc, rows=rows, fails=fails, verdict=verdict, failing=failing)


os.makedirs(LOGS, exist_ok=True)
os.makedirs(DIFFS, exist_ok=True)
assert md5(FROZEN) == "783c0c7fb86823c6e9a5ae84be98b965", "frozen md5 changed"
assert open(SRC, encoding="utf-8", newline="").read() == frozen, "scratch src is not the frozen copy at start"

base = build_and_run("BASELINE")
print("BASELINE", base["rows"], base["fails"], base["verdict"], base["bmd5"], flush=True)
assert base["rows"] == 491 and base["fails"] == 0 and base["verdict"] == "DIFF_FOOTBRIDGE_PASS"
base_md5 = base["bmd5"]

open(SENT, "w").write("src/devices/dev_footbridge.c: one-line variant table in progress (driver.py)\n")
res_path = OUT + ("/results.tsv" if not only else os.environ.get("RESULTS_NAME", "/results_subset.tsv"))
rf = open(res_path, "w", encoding="utf-8")
rf.write("vid\tfamily\tarm\tvariant\tbuild\trows\tfailures\tverdict\tn_red\tfirst_failing_row\tbinary_same_as_base\n")
t0 = time.time()
try:
    for n, (vid, fam, arm, old, new, text) in enumerate(V):
        cnt = frozen.count(old)
        if cnt != 1 or old == new:
            rf.write("%s\t%s\t%s\t%s\tANCHOR-ERROR(count=%d)\t\t\t\t\t\t\n" % (vid, fam, arm, text, cnt))
            rf.flush()
            print("ANCHOR-ERROR", vid, cnt, flush=True)
            continue
        mut = frozen.replace(old, new)
        open(SRC, "w", encoding="utf-8", newline="").write(mut)
        diff = "".join(difflib.unified_diff(frozen.splitlines(True), mut.splitlines(True),
                                            "frozen/dev_footbridge.c", vid + "/dev_footbridge.c", n=1))
        open(DIFFS + "/" + vid + ".diff", "w", encoding="utf-8").write(diff)
        r = build_and_run(vid)
        if r["build"] != "ok":
            rf.write("%s\t%s\t%s\t%s\t%s\t\t\t\t\t%s\t\n" % (vid, fam, arm, text, r["build"], r["err"].replace("\n", " | ")[:300]))
        else:
            first = r["failing"][0] if r["failing"] else "-"
            rf.write("%s\t%s\t%s\t%s\tok\t%s\t%s\t%s\t%d\t%s\t%s\n" % (
                vid, fam, arm, text, r["rows"], r["fails"], r["verdict"], len(r["failing"]), first,
                "SAME" if r["bmd5"] == base_md5 else "differs"))
        rf.flush()
        if n % 20 == 0:
            print("%4d/%d %6.0fs %s" % (n, len(V), time.time() - t0, vid), flush=True)
finally:
    rf.close()
    # restore from the FROZEN project copy, verify by content, rebuild, re-run
    open(SRC, "w", encoding="utf-8", newline="").write(frozen)
    c = sh(["cmp", SRC, FROZEN])
    fin = build_and_run("BASELINE_AFTER")
    ok = (c.returncode == 0 and fin.get("rows") == 491 and fin.get("fails") == 0
          and fin.get("verdict") == "DIFF_FOOTBRIDGE_PASS" and fin.get("bmd5") == base_md5)
    print("RESTORE cmp rc=%d  after: %s %s %s  binary==base: %s" % (
        c.returncode, fin.get("rows"), fin.get("fails"), fin.get("verdict"), fin.get("bmd5") == base_md5), flush=True)
    if ok:
        os.remove(SENT)
        print("SENTINEL CLEARED", flush=True)
    else:
        print("SENTINEL LEFT IN PLACE -- restore NOT verified", flush=True)
print("DRIVER_DONE %d variants in %.0fs" % (len(V), time.time() - t0), flush=True)
