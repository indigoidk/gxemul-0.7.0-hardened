#!/usr/bin/env python3
# SECTION 4 -- >=30 NEW probe-file edits, each a differently-spelled prompt-readiness test, outside the thirteen
# filed shapes.  Each edit is applied to a FRESH /tmp snapshot (SEC regress top-level + the 4 FROZEN files under
# review), the UNMODIFIED frozen gate is run, and the readiness FAIL count is recorded.  For each PASS I classify:
#   SPELLING  -- a construct outside what a spelling census claims to count (expected pass; not a defect)
#   CLAIMED   -- a token-level variant of a shape the F2 repair CLAIMS to close (a PASS here would be a DEFECT)
#   CONTROL   -- expected to RED (proves the census still bites; the denominator of the search)
# Every predicate is appended as a never-run `def`, so the census sees the tokens/text without executing anything.
# /tmp only; never writes under GXEMUL-SEC.
import io, os, re, shutil, subprocess, sys, tempfile

SEC = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
FROZ = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c2_frozen"
OUT = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c2/s4"
TARGET = "luna_absentcpu_probe.py"   # a prompt-detecting, #392-converted pty probe; appending keeps its own predicate
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
W = tempfile.mkdtemp(prefix="gxc2_s4_")
SNAP = os.path.join(W, "snap")
os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/regress")); os.makedirs(os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in os.listdir(os.path.join(SEC, "regress")):
    p = os.path.join(SEC, "regress", f)
    if os.path.isfile(p): shutil.copy2(p, os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(SEC, "tools/derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))
for f in ("gate_hygiene.sh", "census_tokens.py", "crime_width_probe.py"):
    shutil.copy2(os.path.join(FROZ, f), os.path.join(SNAP, "GXEMUL-SEC/regress", f))
shutil.copy2(os.path.join(FROZ, "derive_hygiene_pins.sh"), os.path.join(SNAP, "GXEMUL-SEC/tools"))

EW = "ends" + "with"; SP = "%s (" % EW; NS = "%s(" % EW   # spaced vs no-space method+paren
# (tag, classification-hint, predicate-text).  Predicate text is appended as `def _r_<tag>(buf, resp=None, self=None): return <text>`.
# NS forms (literal endswith( with no space, arg != the two recognised) are CONTROLs (they raise `unknown`).
CASES = [
 ("removesuffix",  "SPELLING", 'buf.removesuffix("GXemul>") != buf'),
 ("sliceeq_rev",   "SPELLING", '"GXemul>" == buf.rstrip()[-7:]'),
 ("in_tail",       "SPELLING", '"GXemul>" in buf[-8:]'),
 ("find_ge0",      "SPELLING", 'buf.rstrip().find("GXemul>") >= 0'),
 ("rfind",         "SPELLING", 'buf.rfind("GXemul>") != -1'),
 ("strip_spaced",  "SPELLING", 'buf.strip().%s"GXemul>")' % SP),
 ("count_gt0",     "SPELLING", 'buf.count("GXemul>") > 0'),
 ("regex_star",    "SPELLING", 're.search("GXemul> *$", buf) is not None'),
 ("resp_spaced",   "SPELLING", 'resp.%s"GXemul>")' % SP),
 ("rpartition",    "SPELLING", 'buf.rpartition("GXemul>")[1] != ""'),
 ("tuple_spaced",  "SPELLING", 'buf.rstrip().%s("GXemul>",))' % SP),
 ("bytes_enc",     "SPELLING", 'buf.rstrip()[-7:].encode() == b"GXemul>"'),
 ("buf_endsw_sp",  "SPELLING", 'buf.%s"GXemul>")' % SP),
 ("splitlines",    "SPELLING", 'buf.splitlines()[-1:] == ["GXemul>"]'),
 ("computed_slice","SPELLING", 'buf[-len("GXemul>"):] == "GXemul>"'),
 ("re_match_dotall","SPELLING", 'bool(re.match(r".*GXemul>\\s*$", buf, re.S))'),
 ("implicit_in",   "SPELLING", '"GXemul" ">" in buf'),
 ("lastchar_and",  "SPELLING", 'buf.rstrip()[-1:] == ">" and "GXemul" in buf'),
 ("gen_spaced",    "SPELLING", 'any(x.rstrip().%s"GXemul>") for x in [buf])' % SP),
 ("getattr_ind",   "SPELLING", 'getattr(buf.rstrip(), "%s")("GXemul>")' % EW),
 ("dunder",        "SPELLING", 'buf.rstrip().__contains__("GXemul>")'),
 ("methodcaller",  "SPELLING", 'operator.methodcaller("%s", "GXemul>")(buf.rstrip())' % EW),
 ("comp_spaced",   "SPELLING", '[x for x in [buf] if x.rstrip().%s"GXemul>")]' % SP),
 ("removesuffix_eq","SPELLING",'buf.rstrip().removesuffix("GXemul>") == buf.rstrip()[:-7]'),
 ("startswith_rev","SPELLING", 'buf.rstrip()[::-1].startswith(">lumeXG")'),
 ("eq_after_strip","SPELLING", 'buf.rstrip().rsplit(chr(10),1)[-1] == "GXemul>"'),
 ("index_try",     "SPELLING", 'buf.rstrip().index("GXemul>") == len(buf.rstrip())-7'),
 ("regex_fullmatch","SPELLING",'re.fullmatch(r"(?s).*GXemul>\\s*", buf) is not None'),
 ("hexcmp",        "SPELLING", 'buf.rstrip()[-7:] == bytes.fromhex("47586d656d75").decode()+">"'),
 ("walrus_in",     "SPELLING", '(t := buf.rstrip()) and t.endswith (chr(62)) and "GXemul" in t'),
 ("prompt_const",  "SPELLING", 'buf.rstrip().%s_PROMPT)' % SP),        # spaced -> textual blind; token needs STRING after ( -> NAME, no match
 # --- CLAIMED-CLOSED boundary probes: token-level variants of the WHOLE shape the repair says it counts ---
 ("whole_tab",     "CLAIMED",  'buf.rstrip().' + EW + '\t("GXemul>")'),
 ("whole_trailcomma","CLAIMED",'buf.rstrip().%s"GXemul>",)' % NS),     # exact shape + trailing comma (extra OP token)
 ("whole_concatstr","CLAIMED", 'buf.rstrip().%s"GX" "emul>")' % NS),   # two adjacent STRING tokens
 ("whole_rxbuf",   "CLAIMED",  'self.rxbuf.rstrip().%s"GXemul>")' % NS),# receiver ends 'buf' -> SHOULD count (like n3j) -> expect RED
 ("whole_paren_arg","CLAIMED", 'buf.rstrip().%s("GXemul>"))' % NS),    # parens around the arg (n3c-ish but no receiver parens)
 # --- CONTROLS expected to RED (denominator of the search) ---
 ("ctl_full_nospace","CONTROL",'other.%s"GXemul>")' % NS),             # endswith("GXemul>") in code, non-buf receiver: full++ allends++, unknown unchanged -> PASS actually
 ("ctl_bare",      "CONTROL",  'buf.%s">")' % NS),                     # endswith(">") no space -> bare++ -> RED
 ("ctl_unknown",   "CONTROL",  'buf.rstrip().%sPROMPT)' % NS),         # endswith(PROMPT) -> unknown++ -> RED
 ("ctl_whole4",    "CONTROL",  'mybuf.rstrip().%s"GXemul>")' % NS),    # a real 4th whole site (receiver ends buf) -> whole_full 4 -> RED
]

def run_gate(rdir):
    logs = os.path.join(os.path.dirname(rdir), "logs"); os.makedirs(logs, exist_ok=True)
    env = dict(os.environ, LOGDIR=logs)
    r = subprocess.run(["bash", "./gate_hygiene.sh"], cwd=rdir, env=env, capture_output=True, text=True)
    rows = [re.sub(r"\x1b\[[0-9;]*m", "", l) for l in r.stdout.split("\n") if ("readiness" in l or "whole-buffer" in l)]
    fails = [l for l in rows if l.strip().startswith("FAIL")]
    return len(fails), fails

results = []
for tag, cls, pred in CASES:
    cdir = os.path.join(W, "c", tag); shutil.rmtree(cdir, ignore_errors=True); shutil.copytree(SNAP, cdir)
    rdir = os.path.join(cdir, "GXEMUL-SEC/regress")
    p = os.path.join(rdir, TARGET)
    s = io.open(p, encoding="utf-8").read()
    add = "\n\nimport operator as operator  # for methodcaller cases\n_PROMPT = \"GXemul>\"\ndef _r_%s(buf, resp=None, self=None):\n    return %s\n" % (tag, pred)
    io.open(p, "w", encoding="utf-8").write(s + add)
    nf, fails = run_gate(rdir)
    io.open(os.path.join(OUT, tag + ".fails"), "w", encoding="utf-8").write("\n".join(fails))
    results.append((tag, cls, nf, pred, fails))
    shutil.rmtree(cdir, ignore_errors=True)

# report
lines = []
npass = ncontrol_red = defect = 0
lines.append("%-18s %-9s %-7s %s" % ("tag", "class", "result", "predicate"))
for tag, cls, nf, pred, fails in results:
    res = "PASS" if nf == 0 else "red%d" % nf
    flag = ""
    if nf == 0:
        npass += 1
        if cls == "CLAIMED": flag = "  <-- DEFECT? passes a claimed-closed shape"; defect += 1
        if cls == "CONTROL": flag = "  <-- control did NOT red (reclassify)"
    else:
        if cls == "CONTROL": ncontrol_red += 1
        if cls in ("SPELLING", "CLAIMED"): flag = "  (red: caught)"
    lines.append("%-18s %-9s %-7s %s%s" % (tag, cls, res, pred[:70], flag))
lines.append("")
lines.append("PASSES: %d   CONTROLS that RED (denominator proof): %d   claimed-closed PASSES (defects): %d" % (npass, ncontrol_red, defect))
lines.append("Total cases: %d" % len(results))
out = "\n".join(lines)
io.open(os.path.join(OUT, "TABLE.txt"), "w", encoding="utf-8").write(out + "\nS4_DONE\n")
print(out); print("S4_DONE")
shutil.rmtree(W, ignore_errors=True)
