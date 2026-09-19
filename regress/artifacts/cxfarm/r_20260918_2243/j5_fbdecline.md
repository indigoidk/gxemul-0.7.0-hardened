# J5 -- the SEVEN remaining process-ending sites in `DEVICE_ACCESS(footbridge)`, plus the FIQ read sibling: a census and a disposition for each

## READING SCOPE AND FORM

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (git HEAD cdbe7d7).  Pristine 2021 copies of GXemul
under the project root (`./src/`, `_archive/`) are NOT this fork.  Do not read `regress/artifacts/`, the ledger, the
CHANGELOG or OUTSTANDING_BUGS.  Read-only: no edits, builds or runs.  VERDICT LINE FIRST.  Mark claims READ
(file:line), REASONED or NOT CHECKED; counts carry denominators.  This asks WHAT IS TRUE and WHICH DISPOSITION --
it does not ask you to construct anything.

## THE SITUATION

`src/devices/dev_footbridge.c`, `DEVICE_ACCESS(footbridge)` (starts ~line 498; the DC21285 core-logic device of the
`-E cats` ARM machine at physical 0x42000000).  Eight guest-reachable accesses end the emulator process with
`exit(1)`.  One -- the READ of `+0x188` IRQ_ENABLE_SET, line ~589 -- is being handled in a separate round as ACCEPT
(the datasheet says the register is readable and the model already computes the value).  The other SEVEN, at
approximately lines 565, 574, 604, 613, 622, 712, 737, are the subject here.  The datasheet is
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\dc21285.txt` (Intel 278115-001; the register table is near line 6826,
the IRQ/FIQ prose near 6900-6960; grep for the register names).  Register offsets are in
`src/include/thirdparty/dc21285reg.h`.

The project's option set for such a site, with its own vocabulary: 1 DELETE the kill (keep the arm's other
behaviour); 2 DECLINE silently (refuse the access, no message); 3 DECLINE + a LATCHED announce (one `fatal()`
message per device instance, the house idiom -- `dev_wdc.c`'s `warned_badlen` is the reference; the marker text
`(once)`); 4 ACCEPT (the model already computes the right value); 5 FAULT (model the space as unmapped so the
architecture's bus error fires -- NOT available on every CPU; check whether ARM here delivers one: grep
`src/cpus/memory_rw.c` and the ARM memory code for what a device access returning 0 does); 6 BACKED ACCEPT
(invent storage); 7 IMPLEMENT.  The fork's `fatal()` (`src/core/debugmsg.c`) does NOT exit; only the explicit
`exit(1)` ends the process.  A handler's `return 1` means "handled"; the common tail at the end of the function
copies `odata` for reads.

## QUESTIONS

1. **The census, 7 rows + the FIQ sibling.**  For each site: line; register name and offset (from dc21285reg.h);
   direction (read/write) that triggers it; what the DATASHEET says that register is (readable? writable? quote
   the table line and any prose, with dc21285.txt line numbers); what the arm does BEFORE the exit (does it compute
   a value, store one, nothing?); what the sibling arm of the opposite direction does.
2. **Classify each** into the option set above with the fact that decides it, and say which sites share a class
   (so one design covers them).  For each site name the OBSERVABLE a probe row would read to tell the chosen
   disposition from the others (a value returned, a diagnostic line, the device's later state, exit status).
3. **FAULT availability on ARM.**  What happens today on this machine when a device access function returns 0
   (grep `memory_rw.c` and `src/cpus/cpu_arm*.c` / `memory_arm.c`): is an abort delivered to the guest, or is the
   access silently treated as done?  Cite lines.  This decides whether member 5 exists here.
4. **The FIQ sibling (`fiqenableread`).**  The read of `+0x288` FIQ_ENABLE_SET returns 0 rather than
   `d->fiq_enable` (line ~626-629).  Quote the datasheet's FIQEnable entry: is it readable, and does it read back
   the enable mask?  Is this the same defect class as the +0x188 site (which computes the value and exits) or a
   different one (computes nothing)?  Should it join the +0x188 round (same device, same class, same probe) or
   the seven-site round?
5. **Ordering.**  The seven-site round removes the LAST process-ending sites in this device.  Three probes
   (`regress/footbridge_sites_probe.py` arm K, `regress/fbpending_drain_probe.py`'s kill arm,
   `regress/fbpending_witness.py` arm K) use one of them (+0x100 SDRAM_BA_MASK read, line ~712) as their "the
   device can still end the process" failability control.  Once no site ends the process, what CAN those arms use
   as a failability control -- list the candidates you can find in the tree (a different device's kill, a
   deliberate `abort()`, a harness-side synthetic failure) with a line for each, and say which is soundest.
6. **Standing licence:** anything else found while reading this function -- e.g. an arm whose behaviour
   disagrees with the datasheet in a way no site exits on.
