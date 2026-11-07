# GXemul hardened fork -- DRAFT A FIX for one filed issue, `bootblockzeroaddr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `bootblockzeroaddr`, state `open`, severity `MED`)

**title:** src/disk/bootblock.c:245-258 -- a DEC boot block whose load-address bytes are zero ends the process with exit(1) at boot setup, before the guest runs -- EXIT (disk image content)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- host process should not exit(1) on malformed guest disk images.

## The code at the cited lines

### `src/disk/bootblock.c` around the row's cited line 245 (HEAD 2d25df65, lines 200-290)

```c
  200| 				}
  201| 			}
  202| 
  203| 			/*
  204| 			 *  It seems that the real LUNA88K PROM is able to load
  205| 			 *  boot programs from (old-style) UFS partitions, thus
  206| 			 *  it does not really have the concept of "boot
  207| 			 *  blocks" or second stage boot loader as on some
  208| 			 *  other machines.
  209| 			 *
  210| 			 *  Try these in order (typically from partition 'a'):
  211| 			 *	vmunix	(OMRON UniOS?)
  212| 			 *	boot	(OpenBSD/luna88k)
  213| 			 */
  214| 
  215| 			// TODO.
  216| 			debugmsg(SUBSYS_STARTUP, "", VERBOSITY_INFO, "TODO: load boot program");
  217| 
  218| 			debug_indentation(-1);
  219| 		}
  220| 		return 1;
  221| 
  222| 	case MACHINE_PMAX:
  223| 		/*
  224| 		 *  The first few bytes of a disk contains information about
  225| 		 *  where the bootblock(s) are located. (These are all 32-bit
  226| 		 *  little-endian words.)
  227| 		 *
  228| 		 *  Offset 0x10 = load address
  229| 		 *         0x14 = initial PC value
  230| 		 *         0x18 = nr of 512-byte blocks to read
  231| 		 *         0x1c = offset on disk to where the bootblocks
  232| 		 *                are (in 512-byte units)
  233| 		 *         0x20 = nr of blocks to read...
  234| 		 *         0x24 = offset...
  235| 		 *
  236| 		 *  nr of blocks to read and offset are repeated until nr of
  237| 		 *  blocks to read is zero.
  238| 		 *
  239| 		 *  TODO: Make use of src/include/thirdparty/bootblock.h now
  240| 		 *  that it is in the tree, rather than using hardcoded numbers.
  241| 		 */
  242| 		res = diskimage_access(m, boot_disk_id, boot_disk_type, 0, 0,
  243| 		    minibuf, sizeof(minibuf));
  244| 
  245| 		bootblock_loadaddr = minibuf[0x10] + (minibuf[0x11] << 8)
  246| 		  + (minibuf[0x12] << 16) + ((uint64_t)minibuf[0x13] << 24);
  247| 
  248| 		/*  Convert loadaddr to uncached:  */
  249| 		if ((bootblock_loadaddr & 0xf0000000ULL) != 0x80000000 &&
  250| 		    (bootblock_loadaddr & 0xf0000000ULL) != 0xa0000000) {
  251| 			fatal("\nWARNING! Weird load address 0x%08" PRIx32
  252| 			    " for SCSI id %i.\n\n",
  253| 			    (uint32_t)bootblock_loadaddr, boot_disk_id);
  254| 			if (bootblock_loadaddr == 0) {
  255| 				fatal("I'm assuming that this is _not_ a "
  256| 				    "DEC bootblock.\nAre you sure you are"
  257| 				    " booting from the correct disk?\n");
  258| 				exit(1);
  259| 			}
  260| 		}
  261| 
  262| 		bootblock_loadaddr &= 0x0fffffffULL;
  263| 		bootblock_loadaddr |= 0xffffffffa0000000ULL;
  264| 
  265| 		bootblock_pc = minibuf[0x14] + (minibuf[0x15] << 8)
  266| 		  + (minibuf[0x16] << 16) + ((uint64_t)minibuf[0x17] << 24);
  267| 
  268| 		bootblock_pc &= 0x0fffffffULL;
  269| 		bootblock_pc |= 0xffffffffa0000000ULL;
  270| 		cpu->pc = bootblock_pc;
  271| 
  272| 		debugmsg(SUBSYS_MACHINE, "DEC boot", VERBOSITY_INFO,
  273| 		    "loadaddr=0x%08" PRIx32", pc=0x%08" PRIx32,
  274| 		    (uint32_t) bootblock_loadaddr, (uint32_t) bootblock_pc);
  275| 
  276| 		debug_indentation(1);
  277| 
  278| 		readofs = 0x18;
  279| 
  280| 		for (;;) {
  281| 			res = diskimage_access(m, boot_disk_id, boot_disk_type,
  282| 			    0, readofs, minibuf, sizeof(minibuf));
  283| 			if (!res) {
  284| 				fatal("Couldn't read the disk image. "
  285| 				    "Aborting.\n");
  286| 				return 0;
  287| 			}
  288| 
  289| 			n_blocks = minibuf[0] + (minibuf[1] << 8)
  290| 			  + (minibuf[2] << 16) + ((uint64_t)minibuf[3] << 24);
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

End with one line: `FIXDRAFT_BOOTBLOCKZEROADDR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
