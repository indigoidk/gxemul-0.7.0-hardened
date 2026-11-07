# GXemul hardened fork -- DRAFT A FIX for one filed issue, `sgirebufuninit` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `sgirebufuninit`, state `open`, severity `med`)

**title:** dev_sgi_re.c horrible_getputpixel(): uint8_t buf[8] is never initialised and the guest picks how many of its bytes are used -- uninitialised host stack reaches guest-visible memory on PUT and *color on GET

**state_note (head):**

FILED 2026-09-07, found while writing the design brief for `sgirandomcolour' -- i.e. by reading the arm NEXT
to the one grok pointed at.  **This is a bigger defect than the row that led me to it, and it needs no
undocumented mode at all.**

`horrible_getputpixel()' declares `uint8_t buf[8];' and NEVER INITIALISES IT.  Verified: no memset in the
function, no initialiser, and the only memsets in the file are the device struct, `rop_used' and `zerobuf'.
The two fields that decide how much of `buf' is USED are decoded from the SAME guest-written mode register
and are INDEPENDENT of each other:

    uint32_t color_mode = mode & DE_MODE_TYPE_MASK;      /* bits 4-7  */
    int bufdepth = 1 << ((mode >> 8) & 3);               /* bits 8-9  -> 1, 2, 4 or 8 */

The colour arms fill a number of bytes fixed by the COLOUR type; the transfer length is `bufdepth'.  Nothing
anywhere makes them agree -- `grep -rn '>> *8) *& *3' src/devices/' finds the decode, its own #100 comment,
and the XFER siblings; NO GUARD.

**TWO REACHABLE UNINITIALISED PATHS, IN OPPOSITE DIRECTIONS:**

* **PUT -- host stack INTO guest-visible memory.**  With the depth field = 3 (`bufdepth' 8) NO colour arm
  writes `buf[4..7]' -- not one of the five, including the correct ones -- and all eight bytes go straight to
  `memory_rw(..., tileptr + ofs, buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL)'.  `DE_MODE_TYPE_CI'
  writes only `buf[0]', so CI at any depth above 1 leaks the rest.
* **GET -- host stack INTO `*color', which the caller then STORES.**  The read fills only `bufdepth' bytes,
  then RGB/RGBA/ABGR combine `buf[0..3]'.  Depth field 0 (`bufdepth' 1) with `DE_MODE_TYPE_RGBA' reads ONE
  byte from memory and builds a 32-bit colour from four.  `draw_primitive()' writes that to the destination
  in the same loop iteration -- **the identical caller-consumes-a-failed-read shape `sgirandompixel' just
  fixed one arm of**, reached here with every colour mode documented and implemented.

*** THE #100 COMMENT IS THE TELL, AND IT IS ON THE DECLARATION ITSELF. ***  It reads
`/*  #100: bufdepth can be 8 = 1<<((mode>>8)&3)  */' -- so a previous round worked out that the guest can
demand 8 bytes and GREW THE ARRAY to match, which fixed a stack OVERFLOW.  **It did not ask what fills the
bytes it had just added.**  The array is the right size and the contents are undefined.

SEVERITY: guest-reachable read of uninitialised host stack whose value becomes guest-visible.  In a loop the
stale bytes are usually the PREVIOUS pixel's, so the everyday symptom is wrong colours; on the first call in
a frame they are whatever the host stack held.  Both mode words are ordinary device registers reached by
ordinary stores, and all seven call sites pass one of them.

NOT YET WITNESSED -- filed at once so the finding is durable.  The witness is expected to be cheap because
`regress/sgi_re_randompixel_probe.py' already programs this exact path on unmodified `-E sgi -e ip32' and
needs only a different mode word: its `MODE_LIN_A = 0x1220' is LIN_A | depth-field 2 (`bufdepth' 4) | RGBA,
which is the MATCHED case and leaks nothing.  `0x1020' is the same line with depth field 0.

*** PASS-1 CORRECTION FROM THE GROK SEAT, VERIFIED AGAINST THE HEADER BEFORE BEING ACCEPTED.  MY PATH-A
EXEMPLAR WAS THE WEAKER ONE, AND A FULLY DOCUMENTED VEHICLE EXISTS. ***

The brief drove PATH A with mode `0x1320' -- depth field 3, `bufdepth' 8 -- and called it reachable.  grok:
*"BUFDEPTH in the header is 8/16/32 only -- field [... 44895 more characters not shown]

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Initialize buf to prevent guest-visible host stack leak.

## The code at the cited lines

### `src/core/main.c` around the row's cited line 688 (HEAD 2d25df65, lines 643-733)

```c
  643| 	progname = argv[0];
  644| 
  645| 
  646| 	enable_colorized_output = getenv("CLICOLOR") != NULL;
  647| 
  648| 	debugmsg_init();
  649| 
  650| 
  651| 	/*
  652| 	 *  Create the settings object, and add global settings to it:
  653| 	 *
  654| 	 *  Read-only "constants":     yes, no, true, false.
  655| 	 *  Global emulator settings:  verbose, single_step, ...
  656| 	 */
  657| 	global_settings = settings_new();
  658| 
  659| 	settings_add(global_settings, "yes", 0, SETTINGS_TYPE_INT,
  660| 	    SETTINGS_FORMAT_YESNO, (void *)&constant_yes);
  661| 	settings_add(global_settings, "no", 0, SETTINGS_TYPE_INT,
  662| 	    SETTINGS_FORMAT_YESNO, (void *)&constant_no);
  663| 	settings_add(global_settings, "true", 0, SETTINGS_TYPE_INT,
  664| 	    SETTINGS_FORMAT_BOOL, (void *)&constant_true);
  665| 	settings_add(global_settings, "false", 0, SETTINGS_TYPE_INT,
  666| 	    SETTINGS_FORMAT_BOOL, (void *)&constant_false);
  667| 
  668| 	/*  Read/write settings:  */
  669| 	settings_add(global_settings, "verbose", 1,
  670| 	    SETTINGS_TYPE_INT, SETTINGS_FORMAT_YESNO, (void *)&verbose);
  671| 	settings_add(global_settings, "quiet_mode", 1,
  672| 	    SETTINGS_TYPE_INT, SETTINGS_FORMAT_YESNO, (void *)&quiet_mode);
  673| 
  674| 	/*  Initialize various subsystems:  */
  675| 	console_init();
  676| 	cpu_init();
  677| 	device_init();
  678| 	machine_init();
  679| 	timer_init();
  680| 
  681| 	/*  Create a simple emulation setup:  */
  682| 	emul = emul_new(NULL);
  683| 	settings_add(global_settings, "emul", 1,
  684| 	    SETTINGS_TYPE_SUBSETTINGS, 0, emul->settings);
  685| 
  686| 	get_cmd_args(argc, argv, emul, &diskimages, &n_diskimages, &tap_devname);
  687| 
  688| 	if (!skip_srandom_call) {
  689| 		struct timeval tv;
  690| 		gettimeofday(&tv, NULL);
  691| 		srandom(tv.tv_sec ^ getpid() ^ tv.tv_usec);
  692| 	}
  693| 
  694| 	// -q means that only errors should be shown.
  695| 	if (quiet_mode)
  696| 		debugmsg_set_verbosity_level(SUBSYS_ALL, VERBOSITY_ERROR);
  697| 
  698| 	for (int k = 0; k < verbose; ++k)
  699| 		debugmsg_add_verbosity_level(SUBSYS_ALL, 1);
  700| 
  701| 	if (!quiet_mode)
  702| 		print_banner();
  703| 
  704| 	/*  Simple initialization, from command line arguments:  */
  705| 	if (emul->machines[0]->machine_type != MACHINE_NONE) {
  706| 		for (i=0; i<n_diskimages; i++) {
  707| 			if (diskimage_add(emul->machines[0], diskimages[i]) < 0) {
  708| 				fprintf(stderr, "Aborting.\n");
  709| 				return 1;
  710| 			}
  711| 		}
  712| 
  713| 		/*  Make sure that there are no configuration files as well:  */
  714| 		for (i=1; i<argc; i++)
  715| 			if (argv[i][0] == '@') {
  716| 				fprintf(stderr, "You can either start one "
  717| 				    "emulation with one machine directly from "
  718| 				    "the command\nline, or start an "
  719| 				    "emulation using a configuration file."
  720| 				    " Not both.\n");
  721| 				return 1;
  722| 			}
  723| 
  724| 		/*  Initialize one emul:  */
  725| 		if (!emul_simple_init(emul, tap_devname)) {
  726| 			fprintf(stderr, "Could not initialize the emulation.\n");
  727| 			return 1;
  728| 		}
  729| 	}
  730| 
  731| 	/*  Initialize an emulation from a config file:  */
  732| 	for (i=1; i<argc; i++) {
  733| 		if (argv[i][0] == '@') {
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_SGIREBUFUNINIT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
