# #499 re-pin -- measurement bundle (opus5 seat, 2026-08-31)

Baseline: HEAD 096a18a, src/devices/dev_sgi_re.c md5 c6cc309cbcd2d96d45333c2376c40325,
regress/sgi_re_width_probe.py md5 f7f77b1c6de332e21158402bb8a9c773.
Scratch clone /tmp/gx500r, full clean rebuild from 0 objects.  Nothing under
GXEMUL-SEC/, build/, est/ or build-asan/ was written.

table500.out   pass 1  base/fix/mexit0 x {P, N(devsig), N3} + the SHIPPED 35-row probe
table500b.out  pass 2  base/fix/mexit0/mret0/mrdexit0 x {P, N3, N1, N2} + the #499 detector
table500c.out  pass 3  the RE-PINNED probe in situ, all five binaries

fix_v2.patch                    #499's fix, enum placement corrected (both new
                                enumerators AFTER SGIRE_W_DE_LEN, numeric order)
repin.patch                     the re-pin for regress/sgi_re_width_probe.py
gate_arm.patch                  one token: "other kill" -> "other decl"
sgi_re_width_probe.repinned.py  the post-patch probe, as measured in pass 3

mk500.py       variant generator; every anchor asserted UNIQUE, duplicate-enumerator
               guard, and a last-enumerator-is-highest-bit guard
score500.py    pass-1 scorer   } lines 66-197 of the shipped probe copied in BY
score500b.py   pass-2 scorer   } EXTRACTION, so session()/printed()/Addr/store/load
               are the shipped ones by construction; fidelity is diff-checkable
clone.sh rebuild.sh table500.sh table500b.sh table500c.sh   drivers
