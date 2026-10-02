# DEDICATED ADVERSARIAL SEAT -- #529 repair 15, pass 2

Read the brief at `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair15_pass2_20260926\pass2_brief.md` in full first (it inlines the device function, the probe helpers, the repair
diff, every mutant and every table).  You are READ-ONLY: do not modify any file.

YOUR JOB IS TO BREAK IT, not to review it.  Find the SMALLEST edit to `DEVICE_ACCESS(crime)` in
`GXEMUL-SEC/src/devices/dev_sgi_ip32.c` that still compiles and that the 218-row probe would NOT detect,
where the edit either
  (i)   lets a narrow access reach the register switch at a guest-visible label in SOME latch state
        (the decline-suppression class -- the brief's section 2), or
  (ii)  changes what an ACCEPTED access at CONTROL does to the DOG / HARD_RESET / residue handling in a way
        no row reads (the entries-13/17 area -- section 6), or
  (iii) breaks any other claim in the contract block of section 5.
For each candidate: the exact edit, the rows you expect to change and the rows you expect to STAY GREEN,
and why each stays green (walk the session).  Be concrete: a candidate without a named green row is not
an answer.  If you find none, list the candidate shapes you tried and why each is caught -- that list is
the denominator, and "none found" without it does not count.

VERDICT LINE FIRST (BREAK FOUND / NO BREAK FOUND with the denominator).
