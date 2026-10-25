SCORES_README.txt -- what the columns of SCORES.txt, SCORES2.txt, SCORES_V12_V7.txt and SCORES_V17v.txt mean (written 2026-10-25
after the Fable 5.1 seat, answering through the Claude Code cloud route, asked for `control` to be defined; the measured files are
not edited).

  score=p/n   p of the n = 33 scored rows matched the FIX column (the probe's GATE mode judges one leg against the FIX wants).
  control     the probe's WDC_LBA_CONTROL line, computed as `leg_ctrl = ctrl_ok and enc_all and hit_all` (wdc_lba_probe.py:780):
              OK when every row of kind `control` passed (a row whose HEAD and FIX wants AGREE -- the ram liveness rows, the
              IDENTIFY rows, the CHS reads, the SDH read-backs, and the write session's companion / refused-write read-backs
              such as `lba wr h1s5` and `lba wr cylhi`), AND every session's hand-encoded words agreed with the emulator's
              disassembler, AND every halt breakpoint was hit; FAIL otherwise.  It is NOT part of the score: a mutant is KILLED
              when p < n OR control is FAIL (the gate requires both p == n and OK).  That is why it flips between twins: V8
              (the read-site head term dropped) reds a SYMPTOM row only -> OK, while V8w (the write-site twin) reds the
              control-kind row `lba wr h1s5` (raw_mut/V8w.out:64) -> FAIL; T_m1 reds symptom rows only -> OK, while T_p1 also
              reds the control-kind row `lba wr cylhi` (raw_mut/T_p1.out:69) -> FAIL.
  reds        the labels of the failed rows in probe order ("LEG" = the leg verdict line itself).
  KILLED / SURVIVED / EQUIVALENT: KILLED = p < 33 or control FAIL; SURVIVED = 33/33 OK; EQUIVALENT = a survivor whose edit cannot
              change any observable (V12: the one head writer masks already).
