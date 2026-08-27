"""#477 pass-2 kill table.

The seventh mutant four seats proposed independently (codex, grok, deepseek, agy)
is the DEPENDS-ON operand swap: the guard's phase test replaced by or widened with
`atapi_len == 0`, which every REAL PHASE_COMPLETED state satisfies.

Plus the revert of the read-arm repair the Fable seat measured, which is the
(a)-clause test for the two new accept rows.

NO REPO MUTATION: scratch trees only.
"""
import io, os, shutil

NL, T = chr(10), chr(9)
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
SCR = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\m477b")

SRC = io.open(os.path.join(ROOT, "src", "devices", "dev_wdc.c"),
              encoding="utf-8", newline="").read()
DIF = os.path.join(ROOT, "regress", "diff_wdc_identify.c")

#  ---- the two guards #477 ships, derived rather than typed ----
DISP = (NL + T*3 + "if (d->atapi_cmd_in_progress &&" + NL +
        T*3 + "    d->atapi_phase == PHASE_CMDOUT && inbuf_len == 12) {" + NL)
assert SRC.count(DISP) == 1, "dispatch anchor %d" % SRC.count(DISP)

#  NL-PREFIXED so the anchor cannot match INSIDE a deeper indent: a run of
#  tabs is a suffix of any longer run, which is exactly how the #477 edit
#  silently dropped one tab while its count==1 assert passed.
READ = (NL + T*4 + "} else if (d->atapi_len == 0 &&" + NL +
        T*4 + "    d->atapi_phase != PHASE_CMDOUT) {" + NL)
assert SRC.count(READ) == 1, "read-arm anchor %d" % SRC.count(READ)

#  verbatim from `git show 1cec2da:src/devices/dev_wdc.c` -- derived, not typed
READ_PRE = NL + T*4 + "} else if (d->atapi_len == 0) {" + NL

MUT = [
    ("Mr_readarm",
     "(a) revert ONLY the read-arm repair, keep the phase guard  [Fable]",
     [(READ, READ_PRE)]),

    ("M7_zerolen",
     "(d) phase test WIDENED by `|| atapi_len == 0`  [codex/grok/deepseek]",
     [(DISP, NL + T*3 + "if (d->atapi_cmd_in_progress &&" + NL +
       T*3 + "    (d->atapi_phase == PHASE_CMDOUT ||" + NL +
       T*3 + "    d->atapi_len == 0) && inbuf_len == 12) {" + NL)]),

    ("M7_notcompleted",
     "(d) phase test relaxed to `!= PHASE_COMPLETED`  [deepseek]",
     [(DISP, NL + T*3 + "if (d->atapi_cmd_in_progress &&" + NL +
       T*3 + "    d->atapi_phase != PHASE_COMPLETED && inbuf_len == 12) {" + NL)]),

    ("M7_ge12",
     "(d) occupancy equality relaxed to `>= 12`  [agy/kimi]",
     [(DISP, NL + T*3 + "if (d->atapi_cmd_in_progress &&" + NL +
       T*3 + "    d->atapi_phase == PHASE_CMDOUT && inbuf_len >= 12) {" + NL)]),

    ("M2_curcmd",
     "(d) redundant `cur_command` conjunct -- RE-MEASURED with fixed fixtures",
     [(DISP, NL + T*3 + "if (d->atapi_cmd_in_progress &&" + NL +
       T*3 + "    d->cur_command == ATAPI_PKT_CMD &&" + NL +
       T*3 + "    d->atapi_phase == PHASE_CMDOUT && inbuf_len == 12) {" + NL)]),

    ("Mb_revert",
     "(b) VERBATIM reinstatement -- both #477 guards removed",
     [(DISP, NL + T*3 + "if (d->atapi_cmd_in_progress && inbuf_len == 12) {" + NL),
      (READ, READ_PRE)]),
]

if os.path.isdir(SCR):
    shutil.rmtree(SCR)

names = []
for name, desc, edits in MUT:
    s = SRC
    for find, repl in edits:
        n = s.count(find)
        assert n == 1, "%s: anchor matched %d" % (name, n)
        s = s.replace(find, repl, 1)
    assert s != SRC, "%s: no-op" % name
    d = os.path.join(SCR, name)
    os.makedirs(os.path.join(d, "src", "devices"))
    os.makedirs(os.path.join(d, "regress"))
    io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
            "w", encoding="utf-8", newline="").write(s)
    shutil.copy(DIF, os.path.join(d, "regress", "diff_wdc_identify.c"))
    names.append((name, desc))

#  clause (c): a null medium.  The detector must not pass against a file
#  holding no device at all.
d = os.path.join(SCR, "Mc_null")
os.makedirs(os.path.join(d, "src", "devices"))
os.makedirs(os.path.join(d, "regress"))
io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
        "w", encoding="utf-8", newline="").write("/*  clause (c) null medium.  */" + NL)
shutil.copy(DIF, os.path.join(d, "regress", "diff_wdc_identify.c"))
names.append(("Mc_null", "(c) NULL MEDIUM"))

print("  %d mutants written" % len(names))
for n, dsc in names:
    print("    %-18s %s" % (n, dsc))
