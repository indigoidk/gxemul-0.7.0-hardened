#!/usr/bin/env python3
"""Opus seat, #545 q2c: one line per differential report in wit2/ -- the class and the shortest witness.
GUEST = a guest-visible divergence (return value, read data, CPU irq line level) from DEVINIT's reset;
HOST = an announce divergence and no guest-visible one; INTERNAL = only the end state differs;
CALLOC-ONLY = a divergence only from the offline harness's all-zero instance; NONE = nothing, anywhere searched.
A report counts only if it ends with WIT2_DONE and rc=0."""
import glob, io, json, os, re

O = os.path.dirname(os.path.abspath(__file__))
pred = {}
for fn in ("results_all.jsonl",):
    p = os.path.join(O, fn)
    if os.path.exists(p):
        for l in io.open(p, encoding="utf-8"):
            r = json.loads(l)
            pred[r["vid"]] = (r.get("pred", ""), r.get("family", ""), r.get("arm", ""), r.get("text", ""))


def counts(line):
    m = re.search(r"guest-visible (\d+), announce (\d+), internal(?:-only)? (\d+), irq-call-count-only (\d+)", line)
    return tuple(int(x) for x in m.groups()) if m else None


rows = []
for f in sorted(glob.glob(os.path.join(O, "wit2_netwinder", "*.txt"))):
    vid = os.path.basename(f)[:-4]
    t = io.open(f, encoding="utf-8").read()
    complete = t.rstrip().endswith("rc=0") and "WIT2_DONE" in t
    dev = cal = rnd = None
    wit_g = wit_a = wit_i = ""
    sect = None
    for ln in t.splitlines():
        if ln.startswith("START devinit"):
            dev = counts(ln); sect = "dev"
        elif ln.startswith("START calloc"):
            cal = counts(ln); sect = "cal"
        elif ln.startswith("RANDOM"):
            rnd = counts(ln); sect = "rnd"
        m = re.match(r"^    shortest (.*?) divergence \(start (\w+), (\d+) steps?\): (.*)$", ln)
        if m:
            kind, start, n, ops = m.groups()
            w = "%s [%s, %s]" % (ops, start, n)
            if "GUEST" in kind and not wit_g:
                wit_g = w
            elif "ANNOUNCE" in kind and not wit_a:
                wit_a = w
            elif ("INTERNAL" in kind or "CALL-COUNT" in kind) and not wit_i:
                wit_i = w
    if not complete or dev is None:
        cls = "INCOMPLETE"
    elif dev[0] or (rnd and rnd[0]):
        cls = "GUEST"
    elif dev[1] or (rnd and rnd[1]):
        cls = "HOST"
    elif dev[2] or dev[3] or (rnd and (rnd[2] or rnd[3])):
        cls = "INTERNAL"
    elif cal and any(cal):
        cls = "CALLOC-ONLY"
    else:
        cls = "NONE"
    p = pred.get(vid, ("", "", "", ""))
    rows.append((vid, cls, p[0], p[2], p[3], dev, cal, rnd, wit_g, wit_a, wit_i))

out = io.open(os.path.join(O, "wit2_classes_netwinder.tsv"), "w", encoding="utf-8")
out.write("vid\tclass\tprediction\tarm\tline\tdevinit<=3 (g,a,i,c)\tcalloc<=2\trandom\tshortest guest-visible\t"
          "shortest announce\tshortest internal/call-count\n")
for r in rows:
    out.write("\t".join(str(x) for x in r) + "\n")
out.close()
for r in rows:
    vid, cls, pr, arm, text, dev, cal, rnd, wg, wa, wi = r
    print("%-22s %-11s pred=%-10s %-4s %s" % (vid, cls, pr, arm, text))
    if wg:
        print("      guest: " + wg)
    elif wa:
        print("      announce: " + wa)
    elif wi:
        print("      internal: " + wi)
print("CLASSIFY_DONE", len(rows))
