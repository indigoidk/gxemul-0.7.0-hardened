OPUS PASS-5 SEAT -- pcc2widthkills.  MEASURED KILL TABLE, own scratch clone /tmp/gxopus_p5.
Baseline named: GXEMUL-SEC working tree (b78bb0f + the uncommitted repair), dev_pcc2.c md5
29921d744defada7cfb9393f3023816d.  Instrument: the SHIPPED probe, frozen copy
/tmp/gxopus_p5_probe.py md5 06594f0e189befcad0077d7de9339d59 (101 rows).
Every run: source cmp-clean against SEC before mutating, `rm src/devices/dev_pcc2.o', make -j4,
[ gxemul -nt dev_pcc2.c ] verified, mutation grepped in the source, PCC2W_PROBE_DONE checked.

  mutant                                                     score     reds
  BASE                                                       101/101   -
  M1  guard qualified by its OWN latch bit, all twelve       101/101   -   *** TOTAL SWEEP ***
  M2  the same at GENCTL alone (one arm)                     101/101   -   *** TOTAL SWEEP ***
  M3  guard DELETED at GENCTL (negative control)              92/101   rb genctl(0xbb), rb genctl dcl,
                                                                       rb genctl lo, latch all(11),
                                                                       latch same(0), latch two(1),
                                                                       latch aba(1), latch all w(11),
                                                                       latch all d(11)

M1/M2 =   if (len != 1 && writeflag == MEM_WRITE
              && !(d->warned & (1u << PCC2_W_<BLOCK>_LEN))) {

NON-EQUIVALENCE PROVED (discriminator.py, md5 93db5ce2457b85894ee7e94b3e27b7bb, run on the
saved BASE and M1 binaries):
  D1  guest: st.b 0x82 GENCTL; st.h 0xaabb GENCTL; st.h 0xaabb GENCTL; ld.bu GENCTL
      BASE GENCTL=0x82 declines=1     M1 GENCTL=0xbb declines=1
  D2  operator: st.b 0x12 MASK; put h 0xaabb MASK; put h 0xaabb MASK; ld.bu MASK
      BASE MASK=0x12  declines=1      M1 MASK=0xbb  declines=1
  D3  ONE wide write only (the shape EVERY shipped readback row uses)
      BASE GENCTL=0x82 declines=1     M1 GENCTL=0x82 declines=1   <- why the detector is blind

Artifacts: artifacts/probe_{BASE,M1,M2,M3}.out (each ends PCC2W_PROBE_DONE), artifacts/discriminator.py.
Clone left cmp-clean against SEC, rebuilt, .MUTANT cleared.  GXEMUL-SEC never written.
