#!/usr/bin/env python3
"""build_fable_f2.py -- the FLAGSHIP ADJUDICATION brief for #529's F2 pass (the Fable seat, LAST; GPT-6 Astra confirms).
Fable is a file-reading seat, so the evidence is POINTED TO by absolute path (every path verified to exist here) and the
disagreements are stated in the seats' own words, verbatim excerpts taken by anchor.  Writes fable_f2_brief.md."""
import io, os, sys

A = r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill"
F2 = os.path.join(A, "repair16_f2_20260926")
PANEL = r"C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260926_053828"
HERE = os.path.dirname(os.path.abspath(__file__))

paths = {
    "the F2 packet (as sent)": os.path.join(F2, "f2_packet.md"),
    "table 16's scoring": os.path.join(A, r"table16_20260926\check16.out"),
    "POSTTABLE16": os.path.join(A, r"table16_20260926\POSTTABLE16.out"),
    "PRETABLE16": os.path.join(A, r"table16_20260926\PRETABLE16.out"),
    "the repair-16 probe (frozen)": os.path.join(A, r"table16_20260926\crime_width_probe.table16.py"),
    "the repair-16 diff": os.path.join(F2, "probe_r16.diff"),
    "agy (F2)": os.path.join(PANEL, "agy.txt"),
    "grok panel seat (F2)": os.path.join(PANEL, "grok.txt"),
    "glm (F2)": os.path.join(PANEL, "ollama_glm.txt"),
    "kimi-k3:cloud (F2)": os.path.join(PANEL, "ollama_kimi.txt"),
    "minimax (F2)": os.path.join(PANEL, "ollama_minimax.txt"),
    "deepseek (F2)": os.path.join(PANEL, "ollama_deepseek.txt"),
    "the dedicated grok job (F2)": os.path.join(F2, "grok_dedicated_f2.txt"),
    "the Opus measuring seat (F2)": os.path.join(F2, "opus5_f2.md"),
    "codex / GPT-6 Astra (F2, after 07:01)": os.path.join(F2, "codex_f2.txt"),
    "your own pass-2 answer": os.path.join(A, r"repair15_pass2_20260926\fable5_r15p2.md"),
}
missing = [k for k, p in paths.items() if not os.path.exists(p)]
if missing:
    print("NOT YET PRESENT (the brief must not be fired until each is): " + "; ".join(missing))

lines = ["# #529 -- THE FLAGSHIP ADJUDICATION OF THE F2 PASS (repair 15's pass-2 findings; repair 16)",
         "",
         "Liveness first: begin with the token FABLE5_F2ADJ_ALIVE_0926 and quote verbatim the first line of",
         "`C:\\DocumentNoSnc\\cc\\GXEMUL\\_scratchpad\\CHECKPOINT.md`.",
         "",
         "You adjudicate LAST: every other seat has answered the F2 packet.  GPT-6 Astra confirms your ruling afterwards,",
         "and nothing commits before #549 does.  This is ordinary test-coverage review of an emulator device model: which",
         "of the main loop's dispositions stand, which rows (if any) are still owed before the chain can close, and what",
         "the contract text must say.  Please be hardest on the rulings that follow your own earlier answers.",
         "",
         "## THE EVIDENCE (read-only; every path verified to exist when this brief was written)", ""]
for k, p in paths.items():
    lines.append("* %s: `%s`%s" % (k, p, "" if os.path.exists(p) else "  (NOT YET PRESENT)"))
lines += ["", io.open(os.path.join(HERE, "fable_f2_questions.md"), encoding="utf-8").read()]
out = os.path.join(HERE, "fable_f2_brief.md")
io.open(out, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("wrote %s (%d bytes)%s" % (out, os.path.getsize(out), "" if not missing else "  [INCOMPLETE]"))
