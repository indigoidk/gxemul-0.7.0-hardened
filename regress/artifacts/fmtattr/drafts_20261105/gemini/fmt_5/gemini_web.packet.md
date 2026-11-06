# Reading task: format fixes packet 5 (Gemini web; 2026-11-05)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBFMT5-dccb` on a line of its own.

# GXemul hardened fork -- fix printf-format mismatches (packet 5 of 8; a defensive code-quality task)

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

### `src/devices/dev_mb89352.c` (6 warnings)

GCC:
- line 253: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 307: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 307: format '%x' expects a matching 'unsigned int' argument (`-Wformat=`)
- line 433: format '%i' expects argument of type 'int', but argument 7 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 678: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 685: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  251 | 	debugmsg_cpu(cpu, d->subsys, "",
  252 | 	    VERBOSITY_DEBUG,
  253u|     	    "%i bytes written", d->transfer_bufpos);
  254 | 
  255u| 	int res;
     ...
  305 | 		debugmsg_cpu(cpu, d->subsys, "",
  306 | 		    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  307u| 	    	    "unimplemented LEN: %i-bit access, address 0x%x: 0x%x",
  308 | 	    	    len * 8,
  309 | 	    	    (int) relative_addr);
     ...
  431 | 					debugmsg_cpu(cpu, d->subsys, "",
  432 | 					    VERBOSITY_DEBUG,
  433u| 				    	    "Transfer command: phase %i, len %i",
  434u| 				    	    d->phase, d->transfer_count);
  435 | 
     ...
  676 | 			debugmsg_cpu(cpu, d->subsys, "",
  677 | 			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  678u| 		    	    "unimplemented %i-bit WRITE to address 0x%x: 0x%x",
  679 | 		    	    len * 8,
  680u| 			    (int) relative_addr,
     ...
  683 | 			debugmsg_cpu(cpu, d->subsys, "",
  684 | 			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  685u| 		    	    "unimplemented %i-bit READ from address 0x%x",
  686 | 		    	    len * 8,
  687 | 			    (int) relative_addr);
```

### `src/devices/dev_mp.c` (1 warnings)

GCC:
- line 247: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  245 | 
  246 | 	default:
  247u| 		fatal("[ dev_mp: unimplemented relative addr 0x%x ]\n",
  248u| 		    relative_addr);
  249 | 	}
```

### `src/devices/dev_ps2_gif.c` (1 warnings)

GCC:
- line 385: format '%i' expects argument of type 'int', but argument 3 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  383 | 				}
  384u| 		} else {		/*  Unknown command:  */
  385 | 			fatal("[ gif write to addr 0x%x (len=%i):",
  386u| 			    (int)relative_addr, len);
  387u| 			for (i=0; i<len; i++)
```

### `src/devices/dev_ps2_stuff.c` (1 warnings)

GCC:
- line 239: format '%i' expects a matching 'int' argument (`-Wformat=`)

```c
  237 | 			    timer_nr, (long long)odata);
  238 | 			if (timer_nr >= 2)
  239u| 				fatal("[ WARNING: ps2: read from non-"
  240u| 				    "existant timer %i hold register ]\n");
  241 | 		} else {
```

### `src/devices/dev_pvr.c` (1 warnings)

GCC:
- line 1131: format '%i' expects argument of type 'int', but argument 3 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
 1129u| 	double baseRed = 0.0, baseGreen = 0.0, baseBlue = 0.0;
 1130 | 
 1131u| 	debug("[ pvr_render: rendering to FB offset 0x%x, "
 1132u| 	    "%i Tile Accelerator commands ]\n", fb_base, d->n_ta_commands);
 1133 | 
```

### `src/devices/dev_px.c` (1 warnings)

GCC:
- line 488: too many arguments for format (`-Wformat-extra-args`)

```c
  486 | 
  487 | 		if (px_debug)
  488u| 			debug("[ px putchar: v1 = 0x%08x  v2 = 0x%08x x=%i y=%i ]\n",
  489u| 			    (int)v1, (int)v2, x,y, x2,y2);
  490 | 
```

### `src/devices/dev_sgi_ip32.c` (6 warnings)

GCC:
- line 398: format '%i' expects argument of type 'int', but argument 3 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 407: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 640: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 652: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 657: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 729: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  396 | 	default:
  397u| 		if (writeflag==MEM_READ) {
  398u| 			debug("[ crime: read from 0x%x, len=%i:",
  399u| 			    (int)relative_addr, len);
  400 | 			for (i=0; i<len; i++)
     ...
  405 | 			for (i=0; i<len; i++)
  406 | 				debug(" %02x", data[i]);
  407 | 			debug(" (len=%i) ]\n", len);
  408 | 		}
  409 | 	}
     ...
  638 | 			for (i=0; i<len; i++)
  639u| 				fatal(" %02x", data[i]);
  640u| 			fatal(" (len=%i) ]\n", len);
  641 | 		}
  642 | 		break;
     ...
  650 | 			for (i=0; i<len; i++)
  651 | 				debug(" %02x", data[i]);
  652 | 			debug(" (len=%i) ]\n", len);
  653 | 		} else {
  654u| 			debug("[ mace: write to 0x%x:", (int)relative_addr);
  655 | 			for (i=0; i<len; i++)
  656 | 				debug(" %02x", data[i]);
  657 | 			debug(" (len=%i) ]\n", len);
  658 | 		}
  659 | 	}
     ...
  727 | 
  728u| 	if (len != 4)
  729u| 		fatal("[ macepci: unimplemented len %i ]\n", len);
  730 | 
  731 | 	if (writeflag == MEM_WRITE) {
```

## WHAT TO RETURN

EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:
  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]
Use JSON escapes: \t for a tab, \n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to
make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBFMT5: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
