# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `bootblockzeroaddr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `bootblockzeroaddr`, state `open`)

**title:** src/disk/bootblock.c:245-258 -- a DEC boot block whose load-address bytes are zero ends the process with exit(1) at boot setup, before the guest runs -- EXIT (disk image content)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `<src/disk/bootblock.c:258>` shows `exit(1);` which still halts the host on a zero load address.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/disk/bootblock.c b/src/disk/bootblock.c
index 1fa97b13..b9a10bcd 100644
--- a/src/disk/bootblock.c
+++ b/src/disk/bootblock.c
@@ -255,7 +255,8 @@ int load_bootblock(struct machine *m, struct cpu *cpu,
 				fatal("I'm assuming that this is _not_ a "
 				    "DEC bootblock.\nAre you sure you are"
 				    " booting from the correct disk?\n");
-				exit(1);
+				/* #NNN: do not exit host */
+				return 0;
 			}
 		}
```

## Every edited function, after the fix

### `src/disk/bootblock.c` -- post-edit lines 72-560 (`+` marks a line the diff added or the point of a deletion)

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
  258|+ 				/* #NNN: do not exit host */
  259|+ 				return 0;
  260|  			}
  261|  		}
  262|  
  263|  		bootblock_loadaddr &= 0x0fffffffULL;
  264|  		bootblock_loadaddr |= 0xffffffffa0000000ULL;
  265|  
  266|  		bootblock_pc = minibuf[0x14] + (minibuf[0x15] << 8)
  267|  		  + (minibuf[0x16] << 16) + ((uint64_t)minibuf[0x17] << 24);
  268|  
  269|  		bootblock_pc &= 0x0fffffffULL;
  270|  		bootblock_pc |= 0xffffffffa0000000ULL;
  271|  		cpu->pc = bootblock_pc;
  272|  
  273|  		debugmsg(SUBSYS_MACHINE, "DEC boot", VERBOSITY_INFO,
  274|  		    "loadaddr=0x%08" PRIx32", pc=0x%08" PRIx32,
  275|  		    (uint32_t) bootblock_loadaddr, (uint32_t) bootblock_pc);
  276|  
  277|  		debug_indentation(1);
  278|  
  279|  		readofs = 0x18;
  280|  
  281|  		for (;;) {
  282|  			res = diskimage_access(m, boot_disk_id, boot_disk_type,
  283|  			    0, readofs, minibuf, sizeof(minibuf));
  284|  			if (!res) {
  285|  				fatal("Couldn't read the disk image. "
  286|  				    "Aborting.\n");
  287|  				return 0;
  288|  			}
  289|  
  290|  			n_blocks = minibuf[0] + (minibuf[1] << 8)
  291|  			  + (minibuf[2] << 16) + ((uint64_t)minibuf[3] << 24);
  292|  
  293|  			bootblock_offset = (minibuf[4] + (minibuf[5] << 8) +
  294|  			  (minibuf[6]<<16) + ((uint64_t)minibuf[7]<<24)) * 512;
  295|  
  296|  			if (n_blocks < 1 || n_blocks > 128)	/* #111: bound disk-controlled count (fatal() doesn't exit; 128*512=64K) */
  297|  				break;
  298|  
  299|  			debug(readofs == 0x18? "%i" : " + %i", n_blocks);
  300|  
  301|  			if (n_blocks * 512 > 65536)
  302|  				fatal("\nWARNING! Unusually large bootblock "
  303|  				    "(%i bytes)\n\n", n_blocks * 512);
  304|  
  305|  			CHECK_ALLOCATION(bootblock_buf = (unsigned char *) malloc(n_blocks*512));
  306|  
  307|  			res = diskimage_access(m, boot_disk_id, boot_disk_type,
  308|  			    0, bootblock_offset, bootblock_buf, n_blocks * 512);
  309|  			if (!res) {
  310|  				fatal("WARNING: could not load bootblocks from"
  311|  				    " disk offset 0x%llx\n",
  312|  				    (long long)bootblock_offset);
  313|  			}
  314|  
  315|  			store_buf(cpu, bootblock_loadaddr,
  316|  			    (char *)bootblock_buf, n_blocks * 512);
  317|  
  318|  			bootblock_loadaddr += 512*n_blocks;
  319|  			free(bootblock_buf);
     | [... lines 320-530 not shown ...]
  531|  			retval = iso_load_bootblock(m, cpu, boot_disk_id,
  532|  			    boot_disk_type, iso_type, bootblock_buf,
  533|  			    n_loadp, load_namesp);
  534|  	}
  535|  
  536|  	if (retval != 0)
  537|  		goto ret_ok;
  538|  
  539|  	/*  Apple parition table:  */
  540|  	res = diskimage_access(m, boot_disk_id, boot_disk_type,
  541|  	    0, 0x0, bootblock_buf, 0x800);
  542|  	if (!res) {
  543|  		fatal("Couldn't read the disk image. Aborting.\n");
  544|  		return 0;
  545|  	}
  546|  	if (bootblock_buf[0x000] == 'E' && bootblock_buf[0x001] == 'R' &&
  547|  	    bootblock_buf[0x200] == 'P' && bootblock_buf[0x201] == 'M') {
  548|  		if (cpu->machine->boot_kernel_filename == NULL ||
  549|  		    cpu->machine->boot_kernel_filename[0] == '\0')
  550|  			fatal("\nApple partition table, but no kernel "
  551|  			    "specified? (Use the -j option.)\n");
  552|  		else
  553|  			retval = apple_load_bootblock(m, cpu, boot_disk_id,
  554|  			    boot_disk_type, n_loadp, load_namesp);
  555|  	}
  556|  
  557|  ret_ok:
  558|  	free(bootblock_buf);
  559|  	return retval;
  560|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_BOOTBLOCKZEROADDR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_BOOTBLOCKZEROADDR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
