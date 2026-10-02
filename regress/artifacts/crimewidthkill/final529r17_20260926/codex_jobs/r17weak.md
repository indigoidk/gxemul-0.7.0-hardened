You are an independent reviewer for a C hardware emulator project (the GXemul hardened fork).  The tree is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  Read-only: change no file and build nothing.

`src\devices\dev_sgi_ip32.c`, `DEVICE_ACCESS(crime)`, lines ~296-320: an access whose length is neither 8 nor 4 is
DECLINED -- a once-latched announce through `d->warned & CRIME_W_LEN`, then `goto crime_declined` (the common tail,
~line 411) past the register switch.  The test probe that defends it is
`regress\artifacts\crimewidthkill\final529r17_20260926\crime_width_probe.r17.py` (226 rows; its module docstring is its
contract; its sessions are the `session(...)` calls and its rows the `row(...)` calls).

CHECK THESE SUPPLIED VARIANTS OF THE FIXED CODE (each is a small text change; do not construct others):
  V1  `if (!(d->warned & CRIME_W_LEN))` -> `if (!(d->warned & CRIME_W_LEN) && writeflag == MEM_WRITE)`
  V2  `goto crime_declined;` -> `if (writeflag == MEM_WRITE) goto crime_declined;`
  V3  `goto crime_declined;` -> `if (relative_addr != CRIME_TIME) goto crime_declined;`
  V4  the `} else if (len == 4) {` arm widened to `} else if (len == 4 || len == 2) {`
  V5  `fatal("[ crime: unimplemented len=...` -> `debug("[ crime: unimplemented len=...` (same text)
  V6  the announce text without its `  (once)` marker
  V7  `d->warned |= CRIME_W_LEN;` removed (the announce prints on every declined access)
  V8  `crime_declined:` moved to just below the `memory_writemax64(cpu, data, len, odata);` read-back
For EACH: the FIRST row (its name, and the observable that differs) that would read differently from the fixed code
when the probe runs on `-E sgi -e ip32` -- or "every row passes".  For each that every row passes: does the contract
DISCLOSE it (quote the sentence) or claim to catch it (quote the sentence)?

FIRST LINE: `VERDICT: <k> of 8 pass every row; <m> of those the contract claims to catch`.  Say what you read (file and
line) and what you inferred.  Note the probe single-steps most sessions, and `debug()` output is visible while
stepping in this emulator (`src\core\debugmsg.c`).
