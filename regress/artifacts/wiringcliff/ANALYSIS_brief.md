# Six regression probes are not run by any gate, and a checker starts rejecting them on 2026-09-20

**Answer in prose. Do not propose a code change, do not write a test, and do not construct any
input or instruction sequence.** I want an assessment of what each probe needs; I will do the wiring
myself.

## Read only these files

    regress/fbpending_drain_probe.py
    regress/hpcmips_ctor_probe.py
    regress/wdc_addtoinbuf_probe.py
    regress/wdc_altoffset_probe.py
    regress/wdc_altoffset_4bit_probe.py
    regress/wdc_altoffset_sig_probe.py
    regress/run.sh
    regress/gate_wdc.sh        (if it exists; otherwise the gate scripts run.sh names)
    tools/pipeline/check_probe_wiring.py

Do not read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md`, or anything under
`_scratchpad/`.

## Please do not simply ratify

Check the premises rather than reasoning from them. **Where I claim a count or a set, enumerate it
and report the number you get.**

**VERDICT LINE FIRST.**

## The situation, stated so you can refute it

`tools/pipeline/check_probe_wiring.py` requires every detector-class probe in `regress/` to be
executed by some gate script that `run.sh` runs. Six probes currently carry a dated exemption that
expires 2026-09-20; from the 21st the checker hard-fails, which blocks commits. I verified this by
running it with `--today 2026-09-21` — it reports exactly those six.

I want to wire them rather than extend the exemption, but I do not yet know what each one costs.

## The questions

**Q1. For each of the six, what does it need in order to run under a gate?** Specifically: what
arguments does it take, does it require a disk image or a rig, roughly how long does it run, and
does it depend on anything a gate would have to set up first. Please answer per-probe, not in
aggregate — I expect them to differ a lot and the aggregate is what has made this look like one big
job instead of four small ones and two real ones.

**Q2. Which gate script is the natural home for each?** Name the existing gate, and say what makes
it the right one — the device it covers, the machine it boots, or the log it greps. If a probe has
no natural home, say so; that is a real answer and it changes what I do.

**Q3. Do any of the three `wdc_altoffset*` probes overlap?** They have adjacent names and I suspect
they are variations on one measurement. If they are, say whether one gate invocation could carry all
three or whether they genuinely test different things. Enumerate what each one actually asserts.

**Q4. What does each probe print as its completion sentinel and its result line?** A gate greps for
those, so I need the exact strings. If any probe lacks a stable result line, that is a defect in the
probe and I want to know before I wire it.

**Q5. Is any of the six actually a WITNESS rather than a detector?** The checker's manifest classes
them, and it separately warns that `wdc_addtoinbuf_probe.py`'s own summary line disagrees with its
manifest entry. A witness that reproduces a defect on a pre-fix build is not the same kind of
artefact as a detector that must run forever, and it may not belong in a gate at all. Say which of
the six you think are which, and on what evidence in the file itself.
