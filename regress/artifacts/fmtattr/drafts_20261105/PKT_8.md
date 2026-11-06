# GXemul hardened fork -- fix printf-format mismatches (packet 8 of 8; a defensive code-quality task)

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

### `src/cpus/cpu_ppc.c` (3 warnings)

GCC:
- line 386: too many arguments for format (`-Wformat-extra-args`)
- line 392: too many arguments for format (`-Wformat-extra-args`)
- line 478: format '%i' expects a matching 'int' argument (`-Wformat=`)

```c
  384 | 		else
  385u| 			debug("\ncpu%i: ", x);
  386u| 		debug("ctr = 0x", x);
  387 | 		if (bits32)
  388u| 			debug("%08" PRIx32, (uint32_t)cpu->cd.ppc.spr[SPR_CTR]);
     ...
  390u| 			debug("%016" PRIx64, (uint64_t)cpu->cd.ppc.spr[SPR_CTR]);
  391 | 
  392u| 		debug("  xer = 0x", x);
  393 | 		if (bits32)
  394u| 			debug("%08" PRIx32, (uint32_t)cpu->cd.ppc.spr[SPR_XER]);
     ...
  476u| 		    (uint64_t) cpu->cd.ppc.spr[SPR_SDR1]);
  477u| 		if (cpu->cd.ppc.cpu_type.flags & PPC_601)
  478u| 			debug("cpu%i:  PPC601-style, TODO!\n");
  479 | 		else {
  480u| 			for (i=0; i<8; i++) {
```

### `src/cpus/cpu_sh.c` (4 warnings)

GCC:
- line 1176: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1205: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1275: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1465: too many arguments for format (`-Wformat-extra-args`)

```c
 1174 | 					debug("<%s>", symbol);
 1175 | 				else
 1176 | 					debug("0x%08" PRIx32, addr);
 1177 | 			}
 1178 | 			debug("\n");
     ...
 1203 | 					debug("<%s>", symbol);
 1204 | 				else
 1205 | 					debug("0x%08" PRIx32, addr);
 1206 | 			}
 1207 | 			debug("\n");
     ...
 1273 | 				debug("<%s>", symbol);
 1274 | 			else
 1275 | 				debug("0x%08" PRIx32, addr);
 1276 | 		}
 1277 | 		debug("\n");
     ...
 1463u| 			debug("stc.l\tr%i_bank,@-r%i\n", (lo8 >> 4) & 7, r8);
 1464u| 		else if ((lo8 & 0x8f) == 0x87)
 1465u| 			debug("ldc.l\t@r%i,r%i_bank\n", r8, (lo8 >> 4) & 7, r8);
 1466u| 		else if ((lo8 & 0x8f) == 0x8e)
 1467u| 			debug("ldc\tr%i,r%i_bank\n", r8, (lo8 >> 4) & 7);
```

## WHAT TO RETURN

EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:
  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]
Use JSON escapes: \t for a tab, \n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to
make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.
