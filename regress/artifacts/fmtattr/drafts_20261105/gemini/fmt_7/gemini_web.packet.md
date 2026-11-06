# Reading task: format fixes packet 7 (Gemini web; 2026-11-05)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBFMT7-b64c` on a line of its own.

# GXemul hardened fork -- fix printf-format mismatches (packet 7 of 8; a defensive code-quality task)

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

### `src/devices/dev_sgi_re.c` (12 warnings)

GCC:
- line 1258: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1272: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1280: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1288: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1296: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1304: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1312: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1321: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1335: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1343: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1726: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'long long int' (`-Wformat=`)
- line 1774: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
 1256 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1257 | 		if (writeflag == MEM_WRITE && idata != 0)
 1258u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_CLIPMODE: 0x%016llx ]\n", idata);
 1259 | 		break;
 1260 | 
     ...
 1270 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1271 | 		if (writeflag == MEM_WRITE && idata != 0)
 1272u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_SCRMASK0: 0x%016llx ]\n", idata);
 1273 | 		break;
 1274 | 
     ...
 1278 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1279 | 		if (writeflag == MEM_WRITE && idata != 0)
 1280u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_SCRMASK1: 0x%016llx ]\n", idata);
 1281 | 		break;
 1282 | 
     ...
 1286 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1287 | 		if (writeflag == MEM_WRITE && idata != 0)
 1288u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_SCRMASK2: 0x%016llx ]\n", idata);
 1289 | 		break;
 1290 | 
     ...
 1294 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1295 | 		if (writeflag == MEM_WRITE && idata != 0)
 1296u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_SCRMASK3: 0x%016llx ]\n", idata);
 1297 | 		break;
 1298 | 
     ...
 1302 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1303 | 		if (writeflag == MEM_WRITE && idata != 0)
 1304u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_SCRMASK4: 0x%016llx ]\n", idata);
 1305 | 		break;
 1306 | 
     ...
 1310 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1311 | 		if (writeflag == MEM_WRITE && idata != 0)
 1312u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_SCISSOR: 0x%016llx ]\n", idata);
 1313 | 		break;
 1314 | 
     ...
 1319 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1320u| 		if (writeflag == MEM_WRITE && idata != 0x3fff3fff)
 1321u| 			fatal("[ sgi_de: TODO: CRIME_DE_SCISSOR+4: 0x%016llx ]\n", idata);
 1322 | 		break;
 1323 | 
     ...
 1333 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1334 | 		if (writeflag == MEM_WRITE && idata != 0)
 1335u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_WINOFFSET_SRC: 0x%016llx ]\n", idata);
 1336 | 		break;
 1337 | 
     ...
 1341 | 		    writeflag == MEM_WRITE ? (long long)idata : (long long)odata);
 1342 | 		if (writeflag == MEM_WRITE && idata != 0)
 1343u| 			fatal("[ sgi_de: TODO: non-zero CRIME_DE_WINOFFSET_DST: 0x%016llx ]\n", idata);
 1344 | 		break;
 1345 | 
     ...
 1724u| 					MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
 1725 | 			} else {
 1726u| 				debug("[ sgi_mte: WARNING: address 0x%x not found in TLB? Ignoring fill. ]\n",
 1727u| 					(long long)fill_addr);
 1728 | 			}
     ...
 1772 | 		}
 1773 | 	} else {
 1774u| 		fatal("[ sgi_mte: UNIMPLEMENTED read/write len %i ]\n", len);
 1775u| 		exit(1);
 1776 | 	}
```

### `src/devices/dev_vga.c` (1 warnings)

GCC:
- line 783: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  781 | 			    (long)relative_addr);
  782 | 		} else {
  783u| 			debug("[ vga: write to  0x%08lx: 0x%08x ]\n",
  784u| 			    (long)relative_addr, idata);
  785 | 		}
```

### `src/devices/dev_vr41xx.c` (4 warnings)

GCC:
- line 243: unknown conversion type character ' ' in format (`-Wformat=`)
- line 243: too many arguments for format (`-Wformat-extra-args`)
- line 252: unknown conversion type character ' ' in format (`-Wformat=`)
- line 252: too many arguments for format (`-Wformat-extra-args`)

```c
  241u| 					case 'C': d->d0 = 0x1000; break;
  242 | 					case 'D': d->d0 = 0x10; break;
  243 | 					default:  fatal("[ vr41xx kiu: unimpl"
  244 | 					    "emented escape 0x%02 ]\n", ch);
  245 | 					}
     ...
  250u| 					case 'C': d->d0 = 0x20; break;
  251 | 					case 'D': d->d0 = 0x10; break;
  252 | 					default:  fatal("[ vr41xx kiu: unimpl"
  253 | 					    "emented escape 0x%02 ]\n", ch);
  254 | 					}
```

### `src/devices/dev_wdc.c` (2 warnings)

GCC:
- line 1606: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1640: format '%i' expects argument of type 'int', but argument 2 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
 1604 | 				        if (!d->warned_badlen) {
 1605 | 						d->warned_badlen = 1;
 1606 | 						fatal("wdc: unimplemented "
 1607 | 						    "write len %i (ignored)\n",
 1608 | 						    len);
     ...
 1638 | 				        if (!d->warned_badlen) {
 1639 | 						d->warned_badlen = 1;
 1640 | 						fatal("wdc: unimplemented "
 1641 | 						    "write len %i (ignored)\n",
 1642 | 						    len);
```

### `src/cpus/cpu_i960.c` (2 warnings)

GCC:
- line 458: unknown conversion type character ' ' in format (`-Wformat=`)
- line 458: too many arguments for format (`-Wformat-extra-args`)

```c
  456 | 	}
  457 | 
  458u| 	debug("%08 " PRIx32, (uint32_t) iw);
  459 | 
  460u| 	if (is_64bit_long_instruction) {
```

### `src/cpus/cpu_mips.c` (1 warnings)

GCC:
- line 2117: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
 2115 | 
 2116u| 				if ((reg[COP0_ENTRYHI] & ENTRYHI_ASID) != (uint32_t)vaddr_asid)
 2117u| 					fatal("[ huh? vaddr_asid 0x%02x not same as in ENTRYHI 0x%02x ]\n",
 2118u| 						vaddr_asid, reg[COP0_ENTRYHI] & ENTRYHI_ASID);
 2119 | 
```

## WHAT TO RETURN

EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:
  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]
Use JSON escapes: \t for a tab, \n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to
make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBFMT7: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
