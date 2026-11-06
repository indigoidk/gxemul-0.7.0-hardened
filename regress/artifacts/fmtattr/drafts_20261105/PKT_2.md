# GXemul hardened fork -- fix printf-format mismatches (packet 2 of 8; a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project.  GXemul is a computer-architecture emulator.  Its diagnostic
functions `debug`, `fatal`, `debugmsg` and `debugmsg_cpu` are printf-like, and GCC (given printf-format attributes) reports
the calls below whose format does not match its arguments.  You cannot read files; each flagged line is inlined with two
lines of context and its line number (`u` = that line's text occurs once in its file).  This is a DRAFTING task: write the
edits.  `uint64_t` is `unsigned long` on this platform and `<inttypes.h>` is already included.

## The fix rules (from the round's adjudication -- follow them exactly)

1. PRESERVE MEANING AND RADIX.  A `%i` stays decimal and a `%x` stays hex; do not convert everything to hex.
2. A 64-bit value printed in hex: the tree's idiom is `"0x%" PRIx64` (or `"%" PRIx64`) with the argument cast `(uint64_t)`.  A
   64-bit value printed in decimal: `"%" PRIi64` with `(int64_t)` or `"%" PRIu64` with `(uint64_t)`.
3. An `(int)` or `(unsigned)` cast is allowed ONLY where the value is small by construction (an offset inside a device's own
   register window, a register number, a byte, a loop index).  Say so in the `why` field.  Never narrow a value that can be
   large (an address, a 64-bit register, a size from the guest).
4. `size_t` -> `%zu` (or `%zx`); `long long` -> `%lli`/`%llx`; a pointer printed with `%x` -> `%p` with a `(void *)` cast.
5. A format with MORE conversions than arguments: add the missing argument ONLY if its value is computed at that point; if the
   value is not available yet (for example a variable still zero there), REMOVE the unsupported conversion instead.
6. A format with FEWER conversions than arguments (`-Wformat-extra-args`): first check for a missing conversion or a stray comma
   splitting a string literal; otherwise drop the extra argument.
7. Change nothing else: no reflowing, no renaming, no new comments.  Tabs stay tabs.  Keep lines within 79 columns where the
   original was; split a string literal with C's adjacent-literal concatenation if needed.

## The warnings and their code

### `src/disk/diskimage_scsicmd.c` (13 warnings)

GCC:
- line 300: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 313: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 348: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 362: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 475: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 578: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 733: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 751: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 843: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 860: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 919: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 944: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1351: format '%i' expects argument of type 'int', but argument 3 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  298u| 	if (xferp->cmd_len < 1) {
  299 | 		debugmsg_cpu(cpu, SUBSYS_DISK, "scsi",
  300u| 		    VERBOSITY_ERROR, "cmd_len = %i",
  301 | 		    xferp->cmd_len);
  302 | 		return 0;
     ...
  311u| 		if (xferp->cmd_len < (size_t)need) {
  312u| 			debugmsg_cpu(cpu, SUBSYS_DISK, "scsi", VERBOSITY_ERROR,
  313u| 			    "short CDB: cmd_len %i < %i (op 0x%02x)",
  314u| 			    xferp->cmd_len, need, xferp->cmd[0]);
  315 | 			return 0;
     ...
  346u| 		debug("TEST_UNIT_READY");
  347 | 		if (xferp->cmd_len != 6)
  348 | 			debug(" (weird len=%i)", xferp->cmd_len);
  349 | 
  350 | 		/*  TODO: bits 765 of buf[1] contains the LUN  */
     ...
  360u| 		debug("INQUIRY");
  361 | 		if (xferp->cmd_len != 6)
  362 | 			debug(" (weird len=%i)", xferp->cmd_len);
  363u| 		if (xferp->cmd[1] != 0x00) {
  364 | 			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
     ...
  473 | 
  474 | 		if (xferp->cmd_len != 10)
  475u| 			fatal(" [ weird READ_CAPACITY len=%i, should be 10 ] ",
  476 | 			    xferp->cmd_len);
  477u| 		else {
     ...
  576 | 			retlen = xferp->cmd[7] * 256 + xferp->cmd[8];
  577 | 			break;
  578u| 		default:fatal(" (unimplemented mode_sense len=%i)",
  579 | 			    xferp->cmd_len);
  580 | 		}
     ...
  731u| 			if (xferp->cmd[0] == SCSICMD_READ) {
  732 | 				if (xferp->cmd_len != 6)
  733 | 					debug(" (weird len=%i)",
  734 | 					    xferp->cmd_len);
  735 | 
     ...
  749 | 			} else {
  750 | 				if (xferp->cmd_len != 10)
  751 | 					debug(" (weird len=%i)",
  752 | 					    xferp->cmd_len);
  753 | 
     ...
  841u| 		if (xferp->cmd[0] == SCSICMD_WRITE) {
  842 | 			if (xferp->cmd_len != 6)
  843 | 				debug(" (weird len=%i)", xferp->cmd_len);
  844 | 
  845 | 			/*
     ...
  858 | 		} else {
  859 | 			if (xferp->cmd_len != 10)
  860 | 				debug(" (weird len=%i)", xferp->cmd_len);
  861 | 
  862 | 			/*
     ...
  917 | 
  918 | 		if (xferp->cmd_len != 10)
  919 | 			debug(" (weird len=%i)", xferp->cmd_len);
  920 | 
  921 | 		/*  TODO: actualy care about cmd[]  */
     ...
  942 | 
  943 | 		if (xferp->cmd_len != 6)
  944 | 			debug(" (weird len=%i)", xferp->cmd_len);
  945 | 
  946 | 		for (i=0; i<(ssize_t)xferp->cmd_len; i++)
     ...
 1349 | 
 1350u| 	case 0xbd:
 1351u| 		fatal("[ SCSI 0x%02x (len %i), TODO: ", xferp->cmd[0],
 1352 | 		    xferp->cmd_len);
 1353 | 		for (i=0; i<(ssize_t)xferp->cmd_len; i++)
```

### `src/devices/dev_bt455.c` (2 warnings)

GCC:
- line 71: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 76: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
   69u| 	case 0x00:		/*  addr_cmap  */
   70 | 		if (writeflag == MEM_WRITE) {
   71u| 			debug("[ bt455: write to addr_cmap, 0x%02x ]\n", idata);
   72u| 			d->addr_cmap = idata;
   73u| 			d->cur_rgb_offset = (d->addr_cmap & 0xf) * 3;
   74 | 		} else {
   75u| 			odata = d->addr_cmap;
   76u| 			debug("[ bt455: read from addr_cmap: 0x%0x ]\n", odata);
   77 | 		}
   78 | 		break;
```

### `src/file/file_aout.c` (1 warnings)

GCC:
- line 113: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'long int' (`-Wformat=`)

```c
  111u| 		entry = buf[20] + (buf[21] << 8) +
  112u| 		    (buf[22] << 16) + ((uint64_t)buf[23] << 24);
  113u| 		debug("OSF1 a.out, load address 0x%08lx, "
  114u| 		    "entry point 0x%08x\n", (long)vaddr, (long)entry);
  115u| 		symbsize = 0;
```

### `src/file/file_ecoff.c` (3 warnings)

GCC:
- line 256: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 407: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'off_t' {aka 'long int'} (`-Wformat=`)
- line 407: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'off_t' {aka 'long int'} (`-Wformat=`)

```c
  254 | 			
  255u| 			if (!relocated) {
  256u| 				debug("relocating from base 0x%08x to 0x%08x\n",
  257u| 					a_tstart, relocationTarget);
  258u| 				a_tstart += relocationOffset;
     ...
  405u| 		debug("symbol header: magic = 0x%x\n", sym_magic);
  406 | 
  407u| 		debug("%i symbols @ 0x%08x (strings @ 0x%08x)\n",
  408u| 		    iextMax, cbExtOffset, cbSsExtOffset);
  409 | 
```

### `src/file/file_macho.c` (1 warnings)

GCC:
- line 119: too many arguments for format (`-Wformat-extra-args`)

```c
  117 | 	}
  118u| 	if (!(flags & 1)) {
  119u| 		fatal("Error: File has 'undefined references'. Cannot"
  120u| 		    " be executed.\n", flags);
  121 | 		exit(1);
```

### `src/devices/dev_dc7085.c` (2 warnings)

GCC:
- line 181: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 201: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  179u| 	case 0x00:	/*  CSR:  Control and Status  */
  180 | 		if (writeflag == MEM_WRITE) {
  181u| 			debug("[ dc7085 write to CSR: 0x%04x ]\n", idata);
  182u| 			idata &= (CSR_TIE | CSR_RIE | CSR_MSE | CSR_CLR
  183u| 			    | CSR_MAINT);
     ...
  199u| 	case 0x08:	/*  LPR:  */
  200 | 		if (writeflag == MEM_WRITE) {
  201u| 			debug("[ dc7085 write to LPR: 0x%04x ]\n", idata);
  202u| 			d->regs.dc_rbuf_lpr = idata;
  203 | 			goto do_return;
```

### `src/devices/dev_dec21030.c` (2 warnings)

GCC:
- line 200: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 205: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  198u| 	case TGA_REG_GCSR:
  199u| 		d->copy_source = idata;
  200u| 		debug("[ dec21030: block copy source = 0x%08x ]\n", idata);
  201 | 		break;
  202 | 
  203u| 	/*  Block copy destination:  */
  204u| 	case TGA_REG_GCDR:
  205u| 		debug("[ dec21030: block copy destination = 0x%08x ]\n", idata);
  206u| 		newlen = 64;
  207u| 		/*  Both source and destination are raw framebuffer addresses,
```

## WHAT TO RETURN

EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:
  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]
Use JSON escapes: \t for a tab, \n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to
make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.
