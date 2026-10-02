Read the review packet at C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\f2_packet_codex_v2.md, sections 1-4. It describes an emulator device model (the CRIME register window, GXEMUL-SEC/src/devices/dev_sgi_ip32.c, function DEVICE_ACCESS(crime)) and a 226-row test probe that checks it.

Your task is a COVERAGE CHECK by reading, not a construction. For the CONTROL register's write arm (case CRIME_CONTROL, inlined as E1): list every effect the arm has on anything a guest or the host log can observe (each clear, the CPU stop, the residue print), and for each effect and each latch state (the width latch d->warned set or clear), name the probe row that observes it, or say that no row does. Then say whether the packet's contract sentence -- that every clear the arm makes before its residue test has a residue-count check in both latch states -- is true as written, and what it does not cover.

If you verify anything, read ONLY GXEMUL-SEC/src/ and GXEMUL-SEC/regress/*.py; do not read GXEMUL-SEC/regress/artifacts/ (other than the packet), _scratchpad/, GXEMUL-SEC/CHANGELOG.md or GXEMUL-SEC/tools/pipeline/.

VERDICT LINE FIRST.
