# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `bootblockzeroaddr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `bootblockzeroaddr`, state `open`)

**title:** src/disk/bootblock.c:245-258 -- a DEC boot block whose load-address bytes are zero ends the process with exit(1) at boot setup, before the guest runs -- EXIT (disk image content)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/disk/bootblock.c` -- AT HEAD, lines 72-559 (`*` marks a line your previous draft changed)

```c
   72|  {
   73|  	struct sgi_boot_block sgi_boot_block;
   74|  	int boot_disk_type = 0, n_blocks, res, readofs, iso_type, retval = 0;
   75|  	unsigned char minibuf[0x20];
   76|  	unsigned char *bootblock_buf;
     | [... lines 77-147 not shown ...]
  148|  			    local buffer; a strdup() directly from bootblock_buf
  149|  			    could scan past the field (and the allocation) when
  150|  			    it contains no NUL/space.  */
  151|  			char name[17];
  152|  			int i = 0;
  153|  			memcpy(name, bootblock_buf + 0x60, 16);
  154|  			name[16] = '\0';
  155|  			while (i < 16) {
  156|  				if (name[i] == ' ')
  157|  					name[i] = '\0';
  158|  				i ++;
  159|  			}
  160|  			CHECK_ALLOCATION(cpu->machine->boot_kernel_filename =
  161|  			    strdup(name));
  162|  		}
  163|  
  164|  		debug("Dreamcast boot filename: %s (to be loaded to 0x8c010000)\n",
  165|  		    cpu->machine->boot_kernel_filename);
  166|  
  167|  		free(bootblock_buf);
  168|  
  169|  		break;
  170|  
  171|  	case MACHINE_LUNA88K:
  172|  		{
  173|  			const int disklabel_size = 512;
  174|  			uint8_t disklabel[disklabel_size];
  175|  
  176|  			res = diskimage_access(m, boot_disk_id, boot_disk_type,
  177|  			    0, 0x0, disklabel, disklabel_size);
  178|  			if (!res) {
  179|  				debugmsg(SUBSYS_STARTUP, "bootblock", VERBOSITY_ERROR,
  180|  				    "ERROR: could not load disklabel");
  181|  				return 0;
  182|  			}
  183|  
  184|  			debugmsg(SUBSYS_STARTUP, "bootblock", VERBOSITY_INFO, "LUNA88K disklabel");
  185|  			debug_indentation(1);
  186|  
  187|  			for (int i = 0; i < 8; ++i) {
  188|  				int ofs = 0x1bc + 8 * i;
  189|  				uint32_t offset = (disklabel[ofs] << 24) +
  190|  				    (disklabel[ofs+1] << 16) +
  191|  				    (disklabel[ofs+2] << 8) +
  192|  				    (disklabel[ofs+3]);
  193|  				uint32_t nsectors = (disklabel[ofs+4] << 24) +
  194|  				    (disklabel[ofs+5] << 16) +
  195|  				    (disklabel[ofs+6] << 8) +
  196|  				    (disklabel[ofs+7]);
  197|  				if (nsectors > 0) {
  198|  					debug("%c: %i sectors at offset %i\n",
  199|  					    'a' + i, nsectors, offset);
  200|  				}
  201|  			}
  202|  
  203|  			/*
  204|  			 *  It seems that the real LUNA88K PROM is able to load
  205|  			 *  boot programs from (old-style) UFS partitions, thus
  206|  			 *  it does not really have the concept of "boot
  207|  			 *  blocks" or second stage boot loader as on some
  208|  			 *  other machines.
  209|  			 *
  210|  			 *  Try these in order (typically from partition 'a'):
  211|  			 *	vmunix	(OMRON UniOS?)
  212|  			 *	boot	(OpenBSD/luna88k)
  213|  			 */
  214|  
  215|  			// TODO.
  216|  			debugmsg(SUBSYS_STARTUP, "", VERBOSITY_INFO, "TODO: load boot program");
  217|  
  218|  			debug_indentation(-1);
  219|  		}
  220|  		return 1;
  221|  
  222|  	case MACHINE_PMAX:
  223|  		/*
  224|  		 *  The first few bytes of a disk contains information about
  225|  		 *  where the bootblock(s) are located. (These are all 32-bit
  226|  		 *  little-endian words.)
  227|  		 *
  228|  		 *  Offset 0x10 = load address
  229|  		 *         0x14 = initial PC value
  230|  		 *         0x18 = nr of 512-byte blocks to read
  231|  		 *         0x1c = offset on disk to where the bootblocks
  232|  		 *                are (in 512-byte units)
  233|  		 *         0x20 = nr of blocks to read...
  234|  		 *         0x24 = offset...
  235|  		 *
  236|  		 *  nr of blocks to read and offset are repeated until nr of
  237|  		 *  blocks to read is zero.
  238|  		 *
  239|  		 *  TODO: Make use of src/include/thirdparty/bootblock.h now
  240|  		 *  that it is in the tree, rather than using hardcoded numbers.
  241|  		 */
  242|  		res = diskimage_access(m, boot_disk_id, boot_disk_type, 0, 0,
  243|  		    minibuf, sizeof(minibuf));
  244|  
  245|  		bootblock_loadaddr = minibuf[0x10] + (minibuf[0x11] << 8)
  246|  		  + (minibuf[0x12] << 16) + ((uint64_t)minibuf[0x13] << 24);
  247|  
  248|  		/*  Convert loadaddr to uncached:  */
  249|  		if ((bootblock_loadaddr & 0xf0000000ULL) != 0x80000000 &&
  250|  		    (bootblock_loadaddr & 0xf0000000ULL) != 0xa0000000) {
  251|  			fatal("\nWARNING! Weird load address 0x%08" PRIx32
  252|  			    " for SCSI id %i.\n\n",
  253|  			    (uint32_t)bootblock_loadaddr, boot_disk_id);
  254|  			if (bootblock_loadaddr == 0) {
  255|  				fatal("I'm assuming that this is _not_ a "
  256|  				    "DEC bootblock.\nAre you sure you are"
  257|  				    " booting from the correct disk?\n");
  258|* 				exit(1);
  259|* 			}
  260|  		}
  261|  
  262|  		bootblock_loadaddr &= 0x0fffffffULL;
  263|  		bootblock_loadaddr |= 0xffffffffa0000000ULL;
  264|  
  265|  		bootblock_pc = minibuf[0x14] + (minibuf[0x15] << 8)
  266|  		  + (minibuf[0x16] << 16) + ((uint64_t)minibuf[0x17] << 24);
  267|  
  268|  		bootblock_pc &= 0x0fffffffULL;
  269|  		bootblock_pc |= 0xffffffffa0000000ULL;
  270|  		cpu->pc = bootblock_pc;
  271|  
  272|  		debugmsg(SUBSYS_MACHINE, "DEC boot", VERBOSITY_INFO,
  273|  		    "loadaddr=0x%08" PRIx32", pc=0x%08" PRIx32,
  274|  		    (uint32_t) bootblock_loadaddr, (uint32_t) bootblock_pc);
  275|  
  276|  		debug_indentation(1);
  277|  
  278|  		readofs = 0x18;
  279|  
  280|  		for (;;) {
  281|  			res = diskimage_access(m, boot_disk_id, boot_disk_type,
  282|  			    0, readofs, minibuf, sizeof(minibuf));
  283|  			if (!res) {
  284|  				fatal("Couldn't read the disk image. "
  285|  				    "Aborting.\n");
  286|  				return 0;
  287|  			}
  288|  
  289|  			n_blocks = minibuf[0] + (minibuf[1] << 8)
  290|  			  + (minibuf[2] << 16) + ((uint64_t)minibuf[3] << 24);
  291|  
  292|  			bootblock_offset = (minibuf[4] + (minibuf[5] << 8) +
  293|  			  (minibuf[6]<<16) + ((uint64_t)minibuf[7]<<24)) * 512;
  294|  
  295|  			if (n_blocks < 1 || n_blocks > 128)	/* #111: bound disk-controlled count (fatal() doesn't exit; 128*512=64K) */
  296|  				break;
  297|  
  298|  			debug(readofs == 0x18? "%i" : " + %i", n_blocks);
  299|  
  300|  			if (n_blocks * 512 > 65536)
  301|  				fatal("\nWARNING! Unusually large bootblock "
  302|  				    "(%i bytes)\n\n", n_blocks * 512);
  303|  
  304|  			CHECK_ALLOCATION(bootblock_buf = (unsigned char *) malloc(n_blocks*512));
  305|  
  306|  			res = diskimage_access(m, boot_disk_id, boot_disk_type,
  307|  			    0, bootblock_offset, bootblock_buf, n_blocks * 512);
  308|  			if (!res) {
  309|  				fatal("WARNING: could not load bootblocks from"
  310|  				    " disk offset 0x%llx\n",
  311|  				    (long long)bootblock_offset);
  312|  			}
  313|  
  314|  			store_buf(cpu, bootblock_loadaddr,
  315|  			    (char *)bootblock_buf, n_blocks * 512);
  316|  
  317|  			bootblock_loadaddr += 512*n_blocks;
  318|  			free(bootblock_buf);
  319|  			readofs += 8;
     | [... lines 320-529 not shown ...]
  530|  			retval = iso_load_bootblock(m, cpu, boot_disk_id,
  531|  			    boot_disk_type, iso_type, bootblock_buf,
  532|  			    n_loadp, load_namesp);
  533|  	}
  534|  
  535|  	if (retval != 0)
  536|  		goto ret_ok;
  537|  
  538|  	/*  Apple parition table:  */
  539|  	res = diskimage_access(m, boot_disk_id, boot_disk_type,
  540|  	    0, 0x0, bootblock_buf, 0x800);
  541|  	if (!res) {
  542|  		fatal("Couldn't read the disk image. Aborting.\n");
  543|  		return 0;
  544|  	}
  545|  	if (bootblock_buf[0x000] == 'E' && bootblock_buf[0x001] == 'R' &&
  546|  	    bootblock_buf[0x200] == 'P' && bootblock_buf[0x201] == 'M') {
  547|  		if (cpu->machine->boot_kernel_filename == NULL ||
  548|  		    cpu->machine->boot_kernel_filename[0] == '\0')
  549|  			fatal("\nApple partition table, but no kernel "
  550|  			    "specified? (Use the -j option.)\n");
  551|  		else
  552|  			retval = apple_load_bootblock(m, cpu, boot_disk_id,
  553|  			    boot_disk_type, n_loadp, load_namesp);
  554|  	}
  555|  
  556|  ret_ok:
  557|  	free(bootblock_buf);
  558|  	return retval;
  559|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/disk/bootblock.c",
    "old": "\t\t\tif (bootblock_loadaddr == 0) {\n\t\t\t\tfatal(\"I'm assuming that this is _not_ a \"\n\t\t\t\t    \"DEC bootblock.\\nAre you sure you are\"\n\t\t\t\t    \" booting from the correct disk?\\n\");\n\t\t\t\texit(1);\n\t\t\t}",
    "new": "\t\t\tif (bootblock_loadaddr == 0) {\n\t\t\t\tfatal(\"I'm assuming that this is _not_ a \"\n\t\t\t\t    \"DEC bootblock.\\nAre you sure you are\"\n\t\t\t\t    \" booting from the correct disk?\\n\");\n\t\t\t\t/* #bootblockzeroaddr: do not exit host */\n\t\t\t\treturn 0;\n\t\t\t}",
    "why": "Gracefully abort boot instead of terminating the host process on zero load address."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_BOOTBLOCKZEROADDR: DEFECT, 3 FINDINGS
1. **Defect removal:** Yes, the diff replaces the `exit(1)` at `src/disk/bootblock.c:258` described by the issue.
2. **CONTROL FLOW:** Yes, the added `return 0;` at line 259 skips the function's common tail, specifically `free(bootblock_buf);` at line 558. 
3. **RETURN VALUE:** The path now returns `0` instead of halting the host. Based on other failure paths (lines 181, 287, 544), returning `0` implies a failure to load the bootblock.
4. **ELSE changed:** Because the host no longer exits, the guest can now survive the failure and potentially trigger the `fatal()` messages at lines 251 and 255 repeatedly.
5. **House idioms:** The `fatal()` messages now require a latch and `(once)` because they can be triggered repeatedly by the guest. Also, the new comment at line 258 uses the issue name instead of a numeric `#NNN:` tag.
**Findings:**
`src/disk/bootblock.c:259`: QUESTION: The early return skips the common tail `free(bootblock_buf);` (line 558). Fix: Check if `bootblock_buf` is initialized before line 148; if safe, use `goto ret_ok;`, otherwise UNSETTLED (requires checking lines 77-147).
`src/disk/bootblock.c:255`: STYLE: Diagnostic can now be triggered repeatedly without exiting. Fix: Gate behind a device instance latch and add `(once)` to the message string.
`src/disk/bootblock.c:258`: STYLE: The comment uses `/* #bootblockzeroaddr: ... */` instead of the house idiom. Fix: Change to `/* #NNN: do not exit host */`.
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_BOOTBLOCKZEROADDR: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_BOOTBLOCKZEROADDR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
