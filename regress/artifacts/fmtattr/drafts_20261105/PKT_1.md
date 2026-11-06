# GXemul hardened fork -- fix printf-format mismatches (packet 1 of 8; a defensive code-quality task)

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

### `src/console/x11.c` (2 warnings)

GCC:
- line 550: format '%i' expects argument of type 'int', but argument 5 has type 'char *' (`-Wformat=`)
- line 550: too many arguments for format (`-Wformat-extra-args`)

```c
  548u| 	    fbwin->x11_screen_depth != 24) {
  549 | 		debugmsg(SUBSYS_X11, "fb_init", VERBOSITY_WARNING,
  550u| 		    "***\n***  WARNING! Your X server is running %i-bit "
  551u| 		    "color mode. This is not really\n",
  552u| 		    "***  supported yet.  8, 15, 16, and 24 bits should "
```

### `src/devices/dev_8253.c` (3 warnings)

GCC:
- line 187: format '%i' expects argument of type 'int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 204: format '%i' expects argument of type 'int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 270: format '%i' expects argument of type 'int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  185 | 				else
  186u| 					d->hz[relative_addr] = 0;
  187u| 				debug("[ 8253: counter %i set to %i (%i Hz) "
  188u| 				    "]\n", relative_addr, d->counter[
  189u| 				    relative_addr], d->hz[relative_addr]);
     ...
  202 | 				}
  203 | 				break;
  204u| 			default:fatal("[ 8253: huh? writing to counter"
  205 | 				    " %i but neither from msb nor lsb? ]\n",
  206 | 				    relative_addr);
     ...
  268u| 				odata = (d->counter[relative_addr] >> 8) & 0xff;
  269 | 				break;
  270u| 			default:fatal("[ 8253: huh? reading from counter"
  271 | 				    " %i but neither from msb nor lsb? ]\n",
  272 | 				    relative_addr);
```

### `src/disk/bootblock.c` (2 warnings)

GCC:
- line 435: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 442: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  433 | 
  434u| 			if (partitions_blocks != 0)
  435u| 				debug("partition %i: %i blocks at %i (type %i)\n",
  436u| 					pi, partitions_blocks, partitions_first, partitions_type);
  437 | 		}
     ...
  440u| 		// Read OSLoader binary into emulated RAM. (Typically "sash.")
  441u| 		uint64_t diskoffset = (uint64_t)found_osloader_block * 512;	/* #136: 64-bit multiply; block index can be up to 2^31-1 */
  442u| 		debug("Loading voldir entry \"%s\", 0x%x bytes from disk offset 0x%x\n",
  443u| 			found_osloader, found_osloader_bytes, diskoffset);
  444 | 
```

### `src/devices/dev_ahc.c` (1 warnings)

GCC:
- line 80: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
   78 | 
   79u| 	if (len != 1)
   80u| 		fatal("[ ahc: ERROR! Unimplemented len %i ]\n", len);
   81 | 
   82 | 	if (writeflag == MEM_READ)
```

### `src/disk/diskimage.c` (2 warnings)

GCC:
- line 2460: format '%i' expects argument of type 'int', but argument 2 has type 'int64_t' {aka 'long int'} (`-Wformat=`)
- line 2460: format '%i' expects argument of type 'int', but argument 4 has type 'int64_t' {aka 'long int'} (`-Wformat=`)

```c
 2458 | 
 2459u| 		if (d->type == DISKIMAGE_FLOPPY || d->chs_override)
 2460u| 			debug(" (CHS=%i,%i,%i)", d->cylinders, d->heads,
 2461u| 			    d->sectors_per_track);
 2462 | 		else
```

### `src/devices/dev_asc.c` (3 warnings)

GCC:
- line 929: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 943: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1173: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  927 | 
  928u| 		if (d->xferp->msg_out_len > 1) {
  929u| 			fatal(" (Long msg out, not implemented yet;"
  930u| 			    " len=%i) }", d->xferp->msg_out_len);
  931 | 			return 0;
     ...
  941u| 			debug(" MSG OUT DEBUG");
  942u| 		if (d->xferp->msg_out_len != 1) {
  943u| 			fatal(" (SELATNS: msg out len == %i, should be 1)",
  944u| 			    d->xferp->msg_out_len);
  945 | 			return 0;
     ...
 1171u| 	} else if (relative_addr >= 0x300 && relative_addr < 0x600
 1172u| 	    && d->turbochannel != NULL) {
 1173u| 		debug("[ asc: offset 0x%x, redirecting to turbochannel"
 1174u| 		    " access ]\n", relative_addr);
 1175u| 		return dev_turbochannel_access(cpu, mem,
```

## WHAT TO RETURN

EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:
  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]
Use JSON escapes: \t for a tab, \n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to
make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.
