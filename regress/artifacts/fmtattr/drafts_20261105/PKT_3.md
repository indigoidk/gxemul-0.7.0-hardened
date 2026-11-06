# GXemul hardened fork -- fix printf-format mismatches (packet 3 of 8; a defensive code-quality task)

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

### `src/cpus/cpu_alpha_palcode.c` (1 warnings)

GCC:
- line 136: format '%i' expects argument of type 'int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  134 | 			s = "";		/*  TODO  */
  135 | 			break;
  136u| 		default:fatal("[ Alpha PALcode: GXemul PROM getenv %i: TODO "
  137u| 			    "]\n", cpu->cd.alpha.r[ALPHA_A1]);
  138 | 			cpu->running = 0;
```

### `src/devices/dev_dec5800.c` (2 warnings)

GCC:
- line 296: too many arguments for format (`-Wformat-extra-args`)
- line 481: too many arguments for format (`-Wformat-extra-args`)

```c
  294 | 	default:
  295 | 		if (writeflag==MEM_READ) {
  296u| 			debug("[ decbi: (node %i) read from unimplemented "
  297 | 			    "0x%08lx ]\n", node_nr, (long)relative_addr,
  298 | 			    (int)odata);
     ...
  479 | 	default:
  480 | 		if (writeflag==MEM_READ) {
  481u| 			debug("[ decxmi: (node %i) read from unimplemented "
  482 | 			    "0x%08lx ]\n", node_nr, (long)relative_addr,
  483 | 			    (int)odata);
```

### `src/devices/dev_dec_ioasic.c` (21 warnings)

GCC:
- line 89: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 100: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 111: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 122: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 133: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 144: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 155: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 166: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 177: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 274: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 288: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 299: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 310: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 321: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 332: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 343: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 354: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 365: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 376: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 387: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 398: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
   87u| 			odata = d->scsi_dmaptr;
   88 | 
   89u| 		debug("[ dec_ioasic: %s SCSI_DMAPTR, data=0x%08x ]\n",
   90 | 			writeflag == MEM_WRITE ? "write to" : "read from",
   91 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
   98u| 			odata = d->scsi_nextptr;
   99 | 
  100u| 		debug("[ dec_ioasic: %s SCSI_NEXTPTR, data=0x%08x ]\n",
  101 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  102 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  109u| 			odata = d->lance_dmaptr;
  110 | 
  111u| 		debug("[ dec_ioasic: %s LANCE_DMAPTR, data=0x%08x ]\n",
  112 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  113 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  120u| 			odata = d->floppy_dmaptr;
  121 | 
  122u| 		debug("[ dec_ioasic: %s FLOPPY_DMAPTR, data=0x%08x ]\n",
  123 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  124 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  131u| 			odata = d->isdn_x_dmaptr;
  132 | 
  133u| 		debug("[ dec_ioasic: %s ISDN_X_DMAPTR, data=0x%08x ]\n",
  134 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  135 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  142u| 			odata = d->isdn_x_nextptr;
  143 | 
  144u| 		debug("[ dec_ioasic: %s ISDN_X_NEXTPTR, data=0x%08x ]\n",
  145 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  146 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  153u| 			odata = d->isdn_r_dmaptr;
  154 | 
  155u| 		debug("[ dec_ioasic: %s ISDN_R_DMAPTR, data=0x%08x ]\n",
  156 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  157 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  164u| 			odata = d->isdn_r_nextptr;
  165 | 
  166u| 		debug("[ dec_ioasic: %s ISDN_R_NEXTPTR, data=0x%08x ]\n",
  167 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  168 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  175u| 			odata = d->csr;
  176 | 
  177u| 		debug("[ dec_ioasic: %s CSR, data=0x%08x ]\n",
  178 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  179 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  272 | 		}
  273 | 
  274u| 		debug("[ dec_ioasic: %s INTR, data=0x%08x ]\n",
  275 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  276 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  286 | 		}
  287 | 
  288u| 		debug("[ dec_ioasic: %s IMSK, data=0x%08x ]\n",
  289 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  290 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  297u| 			odata = d->isdn_x_data;
  298 | 
  299u| 		debug("[ dec_ioasic: %s ISDN_X_DATA, data=0x%08x ]\n",
  300 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  301 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  308u| 			odata = d->isdn_r_data;
  309 | 
  310u| 		debug("[ dec_ioasic: %s ISDN_R_DATA, data=0x%08x ]\n",
  311 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  312 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  319u| 			odata = d->lance_decode;
  320 | 
  321u| 		debug("[ dec_ioasic: %s LANCE_DECODE, data=0x%08x ]\n",
  322 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  323 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  330u| 			odata = d->scsi_decode;
  331 | 
  332u| 		debug("[ dec_ioasic: %s SCSI_DECODE, data=0x%08x ]\n",
  333 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  334 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  341u| 			odata = d->scc0_decode;
  342 | 
  343u| 		debug("[ dec_ioasic: %s SCC0_DECODE, data=0x%08x ]\n",
  344 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  345 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  352u| 			odata = d->scc1_decode;
  353 | 
  354u| 		debug("[ dec_ioasic: %s SCC1_DECODE, data=0x%08x ]\n",
  355 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  356 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  363u| 			odata = d->floppy_decode;
  364 | 
  365u| 		debug("[ dec_ioasic: %s FLOPPY_DECODE, data=0x%08x ]\n",
  366 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  367 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  374u| 			odata = d->scsi_scr;
  375 | 
  376u| 		debug("[ dec_ioasic: %s SCSI_SCR, data=0x%08x ]\n",
  377 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  378 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  385u| 			odata = d->scsi_sdr0;
  386 | 
  387u| 		debug("[ dec_ioasic: %s SCSI_SDR0, data=0x%08x ]\n",
  388 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  389 | 			writeflag == MEM_WRITE ? idata : odata);
     ...
  396u| 			odata = d->scsi_sdr1;
  397 | 
  398u| 		debug("[ dec_ioasic: %s SCSI_SDR1, data=0x%08x ]\n",
  399 | 			writeflag == MEM_WRITE ? "write to" : "read from",
  400 | 			writeflag == MEM_WRITE ? idata : odata);
```

## WHAT TO RETURN

EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:
  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]
Use JSON escapes: \t for a tab, \n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to
make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.
