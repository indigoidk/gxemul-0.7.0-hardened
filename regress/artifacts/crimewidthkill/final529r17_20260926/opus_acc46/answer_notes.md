NOTES FOR THE ANSWER (scratch, not the answer)

instrument: final529r17_20260926/crime_width_probe.r17.py 2fe7123b (226 rows, 68 sessions)
  == table16's 5f770991 except three row NOTES (comment-stripped diff); my earlier freeze 064aca65 (scratchpad p529/r17,
  08:25) differs only at docstring 472-480, below the bucket block.  NOT regress/crime_width_probe.py (a0af7c92).
source: GXEMUL-SEC/src/devices/dev_sgi_ip32.c 8c1d1545.
clone: /tmp/gxopus_acc46 = cp -a /tmp/gxopus_r14 (read only); base b5b99e6d == /tmp/gxopus_r14_bins16/base (table 16's
  base, 226/226 there); envmut 858bfb4c (mut46.py 8c87dc3b, 66-line insertion); restored == base; no .MUTANT.
timeline: PREDICT46.out 08:48:04 < build46 08:48:10-08:48:41 < capture 08:50-09:11 (1243 s, 226/226 OK) < smoke k32C
  225/226 {c t4w gap} < replays (replay46.frozen.py 861ec105; capture ran replay46.py 2d138730 -- same capture path).
capture transcripts: 68 sessions, 68 clean, one [ACC46INIT n=0] each, zero hits.
FROMCACHE: S38 (rearm) + S52 (latch x5) served from capture for the 31 guest-visible entries (derivation); re-run for
  the 15 FULL entries {1,3,4,8,10,11,12,13,14,15,16,17,40,43,44}.
rulings: flagship 09-25 re-rule: "FILE: the +2 translations and the eight unlistable bucket members";
  Astra 09-25: "The eight unlisted bucket members require an L4 enumeration correction and justified dispositions,
  not blanket filing as coverage debt."  (rerule_20260925/fable5_rerule_529_20260925.md, codex_astra529rerule.txt)
close-7 OPUS_REPORT.md s2(a): named all 10 EQ + 5 HOST by class; s1: named the 8 pinned (INTSTAT 4R, INTMASK 4R and 8R,
  TIME 8R, DOG 8R, default 8W and 8R at +0x40, default 8R at +0x278).
