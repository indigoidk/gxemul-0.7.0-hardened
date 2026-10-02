#!/usr/bin/env python3
"""build_f2.py -- assemble the #529 repair-15 pass-2 ADJUDICATION packet (BRIEF_TEMPLATE.md section F2): every seat's
findings numbered and attributed, the main loop's disposition on each and what changed, the disagreements with both
sides, what is still owed -- and the EVIDENCE inlined VERBATIM by anchor (the packet-fed seats cannot open files, and
three of their pass-2 challenges came from sessions the pass-2 brief never showed them).  A missing anchor is a hard
failure.  Writes f2_packet.md (and f2_packet_codex.md, scoped per section C5) beside this file."""
import io, os, re, sys

SEC = r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC"
A = os.path.join(SEC, r"regress\artifacts\crimewidthkill")
R15 = os.path.join(A, "repair15_pass2_20260926")
T14 = os.path.join(A, "table14_20260926")
T15 = os.path.join(A, "table15a_20260926")
T16 = os.path.join(A, "table16_20260926")
OPUS = os.path.join(A, r"opus_r15p2_20260926\opus5_r15p2.md")
HERE = os.path.dirname(os.path.abspath(__file__))
F = "```"


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace", newline="").read().replace("\r\n", "\n")


def between(text, start, end, incl_end=True):
    i = text.find(start)
    if i < 0:
        sys.exit("ANCHOR MISSING: %r" % start[:60])
    j = text.find(end, i + len(start))
    if j < 0:
        sys.exit("END ANCHOR MISSING: %r" % end[:60])
    return text[i:j + (len(end) if incl_end else 0)]


def blk(lang, text):
    return F + lang + "\n" + (text if text.endswith("\n") else text + "\n") + F + "\n"


ip32 = rd(os.path.join(SEC, r"src\devices\dev_sgi_ip32.c"))
p16 = rd(os.path.join(T16, "crime_width_probe.table16.py"))
p15 = rd(os.path.join(T14, "crime_width_probe.table14.py"))
ctl_arm = between(ip32, "\tcase CRIME_CONTROL:\t/*  0x008  */", "\tcase CRIME_INTSTAT:", False)
e_istat = between(p16, "for lbl, off in ((\"imask\", 0x18), (\"istat\", 0x10)):",
                  "row(\"%s lh\" % lbl, ip2(nth(t, \"cause\", 3)), \"clear\", \"refused lh +0x%x: no reassert\" % off)\n")
e_accepts = between(p16, "ACCEPTS = ((\"sd\", 0x00, 0),", "KINDS = ACCEPTS\n")
e_rearm = between(p16, "for op, off, val in KINDS:\n",
                  "row(\"rearm surv\", pr(t, \"v1\"), \"0x%x\" % LIVE_VAL, \"the whole interleave completes (a RAM trip)\")\n")
e_latch = between(p16, "# ---- the latch: five refused accesses, one session, exactly one announce ----\n",
                  "row(\"latch surv\", pr(t, \"v1\"), \"0x%x\" % LIVE_VAL, \"host survives all five\")\n")
e_said = between(p16, "def said(t, ln, off, clean):", "def dflt(t, clean, off, write):", False)
e_rst = between(p16, "def rst_session(op):", "        \"not run, so v1 keeps the SENTINEL (absent would mean the HOST died -- a different outcome) ***\"\n")
e_sw08 = between(p16, "x, _ = st(A, \"sw\", CRIME + 0x08, 0x0800)\n",
                 "row(\"sw08 halts\", pr(t, \"v1\"), \"0x%x\" % SENT, \"CONTROL: sw 0x800 +0x08 stops CPUs (crimectllane)\")\n")
base14 = rd(os.path.join(T14, r"logs\probe_base.raw"))
tl_base = "\n".join(l for l in base14.split("\n") if re.match(r"^(tl |time )", l))
d16 = rd(os.path.join(HERE, "probe_r16.diff"))
m16 = rd(os.path.join(T16, "mutants_16.py"))
m16_body = between(m16, "if name == \"base\":", "elif name == \"list\":", False)
t15 = rd(os.path.join(T15, "check15a.out"))
fable = rd(os.path.join(R15, "fable5_r15p2.md"))
grokd = rd(os.path.join(R15, "grok_dedicated_r15p2.txt"))
lanes16 = [os.path.join(T16, r"logs\lane%d.out" % i) for i in range(6)]
c16p = os.path.join(T16, "check16.out")
if os.path.exists(c16p):
    t16 = "".join(rd(p) for p in lanes16 if os.path.exists(p)) + "\n" + rd(c16p)
else:
    t16 = "*** TABLE 16 HAS NOT FINISHED -- this packet is a DRAFT and must not be fired. ***\n"
opus = rd(OPUS) if os.path.exists(OPUS) else ""
if len(opus) < 500:
    opus = "*** THE OPUS SEAT HAS NOT ANSWERED -- this packet is a DRAFT and must not be fired. ***\n"
else:
    #  its verdict paragraph and its sections 4-5 (the sweep with its census table, and its Q3 options) -- the parts the
    #  findings list cites; the whole answer is on disk for the seats that can read it
    opus = (opus[:opus.find("## 1. WHAT I RAN")].rstrip() + "\n\n[... sections 1-3 on disk ...]\n\n"
            + between(opus, "## 4. Q2 -- THE SWEEP AND ITS DENOMINATOR", "## 6. Q4", False).rstrip()
            + "\n\n[... sections 6-9 on disk: opus_r15p2_20260926/opus5_r15p2.md ...]\n")
findings = rd(os.path.join(HERE, "f2_findings.md"))

S = []
S.append("""# #529 crimewidthkill -- REPAIR 15, PASS 2: THE ADJUDICATION PASS (F2), with REPAIR 16 AS ITS DISPOSITION

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

This packet carries every seat's pass-2 findings, MY disposition on each, and the disagreements with both sides.  **The
load-bearing question is Q2: which of my dispositions is WRONG.**  Several of your pass-2 challenges could not be settled
from the pass-2 packet because it did not show the sessions they turned on; those sessions are inlined here (E1-E7) --
please re-check your own finding against them, and say plainly if it still stands.  A seat whose finding I ADOPTED
should scrutinise my ruling HARDER, not less: a ruling in your favour is the one you are least likely to test.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (the uncommitted #529 working set, `dev_sgi_ip32.c` md5 8c1d1545) and the
probes frozen under `GXEMUL-SEC/regress/artifacts/crimewidthkill/`.  Three pristine-2021-upstream copies of GXemul sit
under the project root; they are not this fork.  If you cannot read files that is expected -- the evidence is inlined.
Name any premise you cannot settle.  **Enumerate rather than reason** where a claim is arithmetic.  **VERDICT LINE FIRST.**
Language: ordinary bounds-and-error-handling review of an emulator device model.

**STATUS WHEN WRITTEN:** nothing of #529 is committed (HEAD f4f601c4); nothing will commit before #549 does and before
the GPT-6 Astra adjudicator confirms.  Repair 15's pass-2 roster: codex WALLED (usage limit, re-fire after 07:01);
kimi CLI 403 (its seat covered by kimi-k3:cloud, PACKET-FED); agy, grok, glm, deepseek, minimax, kimi-k3:cloud answered;
the dedicated adversarial grok job answered; the Fable seat answered after a fallback it recovered from (the fallback
text is kept, labelled NOT A SEAT ANSWER); the Opus measuring seat's answer is section 5.
""")
S.append(findings)
S.append("## 4. EVIDENCE, VERBATIM\n\n**E1 -- the CONTROL arm** (`dev_sgi_ip32.c` 8c1d1545, `case CRIME_CONTROL`):\n\n"
         + blk("c", ctl_arm)
         + "\n**E2 -- the INTSTAT/INTMASK session and its first four rows** (every 1-byte read at +0x10/+0x18 in the probe is "
           "the `lb' here -- the session's FIRST refusal -- or a free-running announce session's only refusal):\n\n"
         + blk("python", e_istat)
         + "\n**E3 -- ACCEPTS, the re-arm session (each accepted entry followed by a refusal -- so entries after the first "
           "run with the latch SET), and the latch session (every entry BEFORE the first refusal -- latch CLEAR)**:\n\n"
         + blk("python", e_accepts + "\n...\n" + e_rearm + "\n...\n" + e_latch)
         + "\n**E4 -- `said()`**:\n\n" + blk("python", e_said)
         + "\n**E5 -- the TIME rows on table 14's base leg (raw values; SMALL = 6,600,000)**:\n\n" + blk("", tl_base)
         + "\n**E6 -- every session holding an accepted 0x800 write before repair 16** (`sw08 halts', and `rst 4w'/`rst 8w' "
           "via `rst_session'):\n\n" + blk("python", e_sw08 + "\n...\n" + e_rst)
         + "\n**E7 -- REPAIR 16, the whole diff** (probe f5e915f6 -> 1534bc9e):\n\n" + blk("diff", d16)
         + "\n**E8 -- the new mutants, verbatim** (`table16_20260926/mutants_16.py`, applied to 8c1d1545):\n\n"
         + blk("python", m16_body)
         + "\n**E9 -- table 15a** (the 218-row repair-15 probe against the HARD_RESET and ENDIANESS clears):\n\n"
         + blk("", t15)
         + "\n**E10 -- table 16** (repair 16's 222-row probe; 25 legs; predictions pre-registered in PRETABLE16.out):\n\n"
         + blk("", t16))
S.append("## 5. THE SEATS' OWN WORDS, where a finding turns on them\n\n**The dedicated adversarial grok seat** "
         "(`grok_dedicated_r15p2.txt`, verbatim):\n\n" + blk("", grokd)
         + "\n**The Fable seat** (`fable5_r15p2.md`, verified claude-fable-5-1, verbatim):\n\n" + blk("", fable)
         + "\n**The Opus measuring seat** (`opus_r15p2_20260926/opus5_r15p2.md`, verbatim):\n\n" + blk("", opus))
S.append("""## 6. QUESTIONS (verdict line first; then one line per item; then reasons)

**Q1.** Adjudicate F1..Fn and D1..Dn: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with the reason.
**Q2. WHICH OF MY DISPOSITIONS IS WRONG?**  I accepted or rejected every finding in section 2 and ruled every disagreement in
section 3 -- that is a suspicious number of rulings by one party, and agreement is not evidence.  Name the one you would
overturn first.
**Q3. WHAT DID ALL OF US MISS?**  You now have every seat's findings and the new tables.
**Q4. REPAIR 16 (E7, E8, E10):** do the four new rows' channels vary under exactly their named mutants?  Is the class
closure in the contract text true as written -- each TESTED bit of the CONTROL arm carrying a side-effect detector AND a
residue-print detector?
**Q5. THE RULE QUESTIONS (D2, D3, D4):** floor or clause (e)?  The measured deltas are in E10.

If, while verifying a claim, you found something ELSE -- say so.
""")
body = "\n".join(S)
nf = sum(1 for l in body.split("\n") if l.startswith(F))
if nf % 2:
    sys.exit("UNBALANCED CODE FENCES: %d" % nf)
out = os.path.join(HERE, "f2_packet.md")
io.open(out, "w", encoding="utf-8", newline="").write(body)
print("wrote %s: %d bytes%s%s" % (out, len(body.encode("utf-8")),
                                  "" if os.path.exists(c16p) else "  [TABLE 16 PENDING]",
                                  "" if len(rd(OPUS) if os.path.exists(OPUS) else "") >= 500 else "  [OPUS PENDING]"))
cscope = ("\n**READING SCOPE FOR THIS SEAT.**  Everything you need is inlined.  If you verify anything, read ONLY "
          "`GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`; do NOT read `GXEMUL-SEC/regress/artifacts/`, `_scratchpad/`, "
          "`GXEMUL-SEC/CHANGELOG.md` or `GXEMUL-SEC/tools/pipeline/`.  Please CHECK the constructions shown; you are not "
          "asked to construct new ones.\n")
cbody = body.replace("**VERDICT LINE FIRST.**", cscope + "\n**VERDICT LINE FIRST.**", 1)
cbody = cbody.replace("# #529 crimewidthkill -- REPAIR 15", "# #529 (the CRIME narrow-width decline) -- REPAIR 15", 1)
outc = os.path.join(HERE, "f2_packet_codex.md")
io.open(outc, "w", encoding="utf-8", newline="").write(cbody)
print("wrote %s: %d bytes" % (outc, len(cbody.encode("utf-8"))))
