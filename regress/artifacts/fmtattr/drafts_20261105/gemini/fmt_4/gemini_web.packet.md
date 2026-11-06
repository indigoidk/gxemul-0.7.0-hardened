# Reading task: format fixes packet 4 (Gemini web; 2026-11-05)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBFMT4-c277` on a line of its own.

# GXemul hardened fork -- fix printf-format mismatches (packet 4 of 8; a defensive code-quality task)

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

### `src/net/net_ip.c` (1 warnings)

GCC:
- line 1620: format '%i' expects argument of type 'int', but argument 5 has type 'ssize_t' {aka 'long int'} (`-Wformat=`)

```c
 1618u| 			    net->tcp_connections[con_id].outside_seqnr;
 1619 | 			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
 1620u| 			    "  putting %i bytes (seqnr %u) in the incoming "
 1621u| 			    "buf", res, net->tcp_connections[con_id].
 1622u| 			    incoming_buf_seqnr);
```

### `src/devices/dev_ether.c` (1 warnings)

GCC:
- line 177: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  175 | 			break;
  176 | 
  177u| 		default:fatal("[ ether: UNIMPLEMENTED command 0x"
  178u| 			    "%02x ]\n", idata);
  179u| 			cpu->running = 0;
```

### `src/promemul/arcbios.c` (1 warnings)

GCC:
- line 1594: too many arguments for format (`-Wformat-extra-args`)

```c
 1592u| 		debug("[ ARCBIOS Open(\"");
 1593 | 		dump_mem_string(cpu, cpu->cd.mips.gpr[MIPS_GPR_A0]);
 1594u| 		debug("\",0x%x,0x%x)", (int)cpu->cd.mips.gpr[MIPS_GPR_A0],
 1595 | 		    (int)cpu->cd.mips.gpr[MIPS_GPR_A1],
 1596u| 		    (int)cpu->cd.mips.gpr[MIPS_GPR_A2]);
```

### `src/core/memory.c` (2 warnings)

GCC:
- line 623: format '%i' expects argument of type 'int', but argument 8 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 635: format '%i' expects argument of type 'int', but argument 8 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  621 | 		debugmsg_cpu(cpu, SUBSYS_MEMORY,
  622 | 		    writeflag ? "WRITE" : "READ",
  623 | 		    verbosity, "%s non-existant "
  624u| 			"paddr=0x%08" PRIx32 " len=%i pc=0x%08" PRIx32 "%s%s%s",
  625 | 		    writeflag ? "to" : "from",
     ...
  633 | 		debugmsg_cpu(cpu, SUBSYS_MEMORY,
  634 | 		    writeflag ? "WRITE" : "READ",
  635 | 		    verbosity, "%s non-existant "
  636u| 			"paddr=0x%016" PRIx64 " len=%i pc=0x%016" PRIx64 "%s%s%s",
  637 | 		    writeflag ? "to" : "from",
```

### `src/promemul/ps2_bios.c` (1 warnings)

GCC:
- line 166: too many arguments for format (`-Wformat-extra-args`)

```c
  164 | 		break;
  165u| 	case 65:
  166u| 		fatal("[ SIFBIOS alloc iop heap(0x" PRIx32") ]\n",
  167u| 		    (uint32_t)cpu->cd.mips.gpr[MIPS_GPR_A1]);
  168 | 
```

### `src/devices/dev_le.c` (7 warnings)

GCC:
- line 231: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint32_t' {aka 'unsigned int'} (`-Wformat=`)
- line 233: format '%llx' expects argument of type 'long long unsigned int', but argument 2 has type 'uint32_t' {aka 'unsigned int'} (`-Wformat=`)
- line 928: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 938: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1039: format '%i' expects argument of type 'int', but argument 5 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1060: format '%x' expects argument of type 'unsigned int', but argument 5 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 1060: format '%x' expects argument of type 'unsigned int', but argument 6 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  229u| 	debug("[ le: DEBUG: ladrf %04x:%04x:%04x:%04x ]\n",
  230u| 	      d->ladrf[0], d->ladrf[1], d->ladrf[2], d->ladrf[3]);
  231u| 	debug("[ le: DEBUG: rdra               %06llx ]\n", d->rdra);
  232u| 	debug("[ le: DEBUG: rlen                  %3i ]\n", d->rlen);
  233u| 	debug("[ le: DEBUG: tdra               %06llx ]\n", d->tdra);
  234u| 	debug("[ le: DEBUG: tlen                  %3i ]\n", d->tlen);
  235 | 
     ...
  926u| 			memcpy(data, d->sram + relative_addr, len);
  927 | 			if (!quiet_mode) {
  928u| 				debug("[ le: read from SRAM offset 0x%05x:",
  929 | 				    relative_addr);
  930 | 				for (i=0; i<len; i++)
     ...
  936u| 			memcpy(d->sram + relative_addr, data, len);
  937 | 			if (!quiet_mode) {
  938u| 				debug("[ le: write to SRAM offset 0x%05x:",
  939 | 				    relative_addr);
  940 | 				for (i=0; i<len; i++)
     ...
 1037u| 			if (idata >= N_REGISTERS)
 1038u| 				debugmsg(d->subsys, "register select", VERBOSITY_WARNING,
 1039u| 				    "WARNING! register %i (max is %i)",
 1040u| 				    idata, N_REGISTERS - 1);
 1041 | 		}
     ...
 1058u| 		memory_writemax64(cpu, data, len, odata);
 1059u| 		debugmsg(d->subsys, "access", VERBOSITY_DEBUG,
 1060u| 		    "read from addr 0x%06x: 0x%08x", relative_addr, odata);
 1061 | 	}
 1062 | 
```

### `src/cpus/cpu_arm.c` (2 warnings)

GCC:
- line 1041: format '%i' expects argument of type 'int', but argument 6 has type 'long unsigned int' (`-Wformat=`)
- line 1051: format '%i' expects argument of type 'int', but argument 5 has type 'long unsigned int' (`-Wformat=`)

```c
 1039 | 	case 0x7:
 1040 | 		// Load/Store with immediate offset.
 1041u| 		debug("%s%s\tr%i,[r%i,#%i]\n",
 1042 | 			l_bit ? "ldr" : "str",
 1043u| 			b_bit ? "b" : "",
     ...
 1049 | 	case 0x8:
 1050u| 		// Load/Store halfword.
 1051u| 		debug("%sh\tr%i,[r%i,#%i]\n",
 1052 | 			l_bit ? "ldr" : "str",
 1053 | 			rd,
```

### `src/devices/dev_luna88k.c` (2 warnings)

GCC:
- line 916: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 922: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  914 | 		if (writeflag == MEM_WRITE)
  915 | 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "luna88k", VERBOSITY_ERROR,
  916u| 		    	    "unimplemented %i-bit WRITE to address 0x%x: 0x%x",
  917 | 		    	    len * 8,
  918u| 			    (int) addr,
     ...
  920 | 		else
  921 | 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "luna88k", VERBOSITY_ERROR,
  922u| 		    	    "unimplemented %i-bit READ from address 0x%x",
  923 | 		    	    len * 8,
  924u| 			    (int) addr);
```

### `src/devices/dev_lunafb.c` (4 warnings)

GCC:
- line 82: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 88: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 174: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 180: format '%i' expects argument of type 'int', but argument 6 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
   80 | 		if (writeflag == MEM_WRITE)
   81 | 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "lunafb_a", VERBOSITY_ERROR,
   82 | 		    	    "unimplemented %i-bit WRITE to address 0x%x: 0x%x",
   83 | 		    	    len * 8,
   84 | 			    (int) addr,
     ...
   86 | 		else
   87 | 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "lunafb_a", VERBOSITY_ERROR,
   88 | 		    	    "unimplemented %i-bit READ from address 0x%x",
   89 | 		    	    len * 8,
   90 | 			    (int) addr);
     ...
  172 | 		if (writeflag == MEM_WRITE)
  173 | 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "lunafb_b", VERBOSITY_ERROR,
  174 | 		    	    "unimplemented %i-bit WRITE to address 0x%x: 0x%x",
  175 | 		    	    len * 8,
  176 | 			    (int) addr,
     ...
  178 | 		else
  179 | 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "lunafb_b", VERBOSITY_ERROR,
  180 | 		    	    "unimplemented %i-bit READ from address 0x%x",
  181 | 		    	    len * 8,
  182 | 			    (int) addr);
```

## WHAT TO RETURN

EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:
  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]
Use JSON escapes: \t for a tab, \n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to
make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBFMT4: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
