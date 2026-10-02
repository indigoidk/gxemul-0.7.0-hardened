# DEDICATED SEAT -- #529 repair 15 pass 2, the ADJUDICATION pass (F2), and repair 16

Read the packet at `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\f2_packet.md`
in full first.  You are READ-ONLY: do not modify any file.

Your job is to find where the main loop's rulings are WRONG, not to confirm them.  Specifically:

1. Take each disposition in section 2 marked ACCEPTED, ROWED, REJECTED or DISCLOSED and say which ONE you would
   overturn first, and why -- with a concrete consequence (a variant of `DEVICE_ACCESS(crime)` in
   `GXEMUL-SEC/src/devices/dev_sgi_ip32.c` that the 226 rows would not detect, or a row whose channel cannot vary).
2. Check repair 16's new rows (E7) against their named variants (E8, E10): for each new row, is there a variant of the
   same clear or the same latch state that it would NOT detect?  Name the row you expect to stay green and walk the
   session.
3. The rule questions D2 and D5: which cells, if any, would you rule floor, and what is the cheapest row set that carries
   them?

If you find nothing, list the candidate shapes you checked and why each is detected -- that list is the denominator.
VERDICT LINE FIRST.
