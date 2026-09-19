# #539: adds the seven artifact .py files of this round to check_probe_wiring.py's MANIFEST -- classified by the round.
# Applied to BOTH the HEAD copy (-> the staged blob _scratchpad/t539/cpw_stage.py) and the working tree (which also
# carries #529's uncommitted MANIFEST hunks), at the same unique anchor.  Refuses unless the anchor occurs once.
import io, sys
ANCHOR = ('    "artifacts/wiringcliff/r536_20260918/apply536_precommit.py":\n'
          '        (CLASS_TOOL, "#536: corrects precommit_check.sh section R\'s comment, which named the old 2026-09-20 date"),\n')
NEW = (ANCHOR +
'    #  #539 n6 (footbridge IRQEnable read ACCEPTED): the frozen instruments the kill tables ran, and the Opus seat\'s\n'
'    #  pass-1 harness.  FROZEN copies are the exact probe text a table scored (the tables cite their md5); the gated\n'
'    #  detector is regress/footbridge_sites_probe.py itself.  Tables 2-5 froze their probes as *.py.frozen (not .py).\n'
'    "artifacts/n6/killtable_20260919/footbridge_sites_probe.frozen.py":\n'
'        (CLASS_WITNESS, "#539 table 1 instrument (md5 e7df250e): the 19-row sites probe as scored on 12 mutants and the pre-fix HEAD"),\n'
'    "artifacts/n6/killtable_20260919/pending_probes_postfix/fbpending_drain_probe.frozen.py":\n'
'        (CLASS_WITNESS, "#539: the drain probe with its K arm at +0x18c and the status binding, as run post-fix (11/11 controls)"),\n'
'    "artifacts/n6/killtable_20260919/pending_probes_postfix/fbpending_witness.frozen.py":\n'
'        (CLASS_WITNESS, "#539: the witness probe likewise, as run post-fix (12/12, PASS)"),\n'
'    "artifacts/n6/opus_p1_20260919/opus_e.py":\n'
'        (CLASS_WITNESS, "#539 pass 1, Opus seat: rows E0-E6 measured on a post-fix build in its own clone before the round\'s probe existed (e_prefix/e_postfix.raw)"),\n'
'    "artifacts/n6/opus_p1_20260919/opus_m.py":\n'
'        (CLASS_RESEARCH, "#539 pass 1, Opus seat: the +0x100 / +0x18c kill-site verification and the d->irq_status == 0 measurement"),\n'
'    "artifacts/n6/opus_p1_20260919/opus_m3b.py":\n'
'        (CLASS_RESEARCH, "#539 pass 1, Opus seat: sub-word read lanes and the register-dump spellings (sl/fp/ip) it reported"),\n'
'    "artifacts/n6/opus_p1_20260919/opus_q4.py":\n'
'        (CLASS_RESEARCH, "#539 pass 1, Opus seat: the default-arm diagnostic-presence control candidate (not adopted: fable5 D1)"),\n')
for p in (r'C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\t539\check_probe_wiring.py.head',
          r'C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\tools\pipeline\check_probe_wiring.py'):
    s = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    t = s.replace('\r\n', '\n')
    if t.count(NEW) == 1:
        print("already applied:", p); continue
    assert t.count(ANCHOR) == 1, (p, t.count(ANCHOR))
    t = t.replace(ANCHOR, NEW)
    out = p if 'GXEMUL-SEC' in p else r'C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\t539\cpw_stage.py'
    if '--apply' in sys.argv:
        io.open(out, 'w', encoding='utf-8', newline='').write(t.replace('\n', nl)); print("wrote", out)
    else:
        print("would write", out)
