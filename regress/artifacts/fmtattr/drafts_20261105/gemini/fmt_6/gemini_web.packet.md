# Reading task: format fixes packet 6 (Gemini web; 2026-11-05)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBFMT6-c40f` on a line of its own.

# GXemul hardened fork -- fix printf-format mismatches (packet 6 of 8; a defensive code-quality task)

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

### `src/devices/dev_sgi_mec.c` (30 warnings)

GCC:
- line 461: format '%i' expects argument of type 'int', but argument 3 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 461: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'long long int' (`-Wformat=`)
- line 470: format '%i' expects argument of type 'int', but argument 3 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 470: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'long long int' (`-Wformat=`)
- line 474: format '%i' expects argument of type 'int', but argument 3 has type 'size_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 474: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'long long int' (`-Wformat=`)
- line 605: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 605: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 605: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 605: format '%x' expects argument of type 'unsigned int', but argument 5 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 605: format '%x' expects argument of type 'unsigned int', but argument 6 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 605: format '%x' expects argument of type 'unsigned int', but argument 7 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 611: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 611: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 611: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 611: format '%x' expects argument of type 'unsigned int', but argument 5 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 611: format '%x' expects argument of type 'unsigned int', but argument 6 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 611: format '%x' expects argument of type 'unsigned int', but argument 7 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 619: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 619: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 619: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 619: format '%x' expects argument of type 'unsigned int', but argument 5 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 619: format '%x' expects argument of type 'unsigned int', but argument 6 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 619: format '%x' expects argument of type 'unsigned int', but argument 7 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 625: format '%x' expects argument of type 'unsigned int', but argument 2 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 625: format '%x' expects argument of type 'unsigned int', but argument 3 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 625: format '%x' expects argument of type 'unsigned int', but argument 4 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 625: format '%x' expects argument of type 'unsigned int', but argument 5 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 625: format '%x' expects argument of type 'unsigned int', but argument 6 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)
- line 625: format '%x' expects argument of type 'unsigned int', but argument 7 has type 'uint64_t' {aka 'long unsigned int'} (`-Wformat=`)

```c
  459u| 	} else if (len == sizeof(uint16_t)) {
  460 | 		if (writeflag == MEM_WRITE) {
  461 | 			fatal("[ sgi_mec: unimplemented %s len %i (addr 0x%x) ]\n",
  462 | 				writeflag ? "write" : "read", len, (long long)relative_addr);
  463u| 		} else if ((relative_addr & 7) == 4) {
     ...
  468u| 			odata = (uint16_t)odata;
  469 | 		} else {
  470 | 			fatal("[ sgi_mec: unimplemented %s len %i (addr 0x%x) ]\n",
  471 | 				writeflag ? "write" : "read", len, (long long)relative_addr);
  472 | 		}
  473 | 	} else {
  474 | 		fatal("[ sgi_mec: unimplemented %s len %i (addr 0x%x) ]\n",
  475 | 			writeflag ? "write" : "read", len, (long long)relative_addr);
  476 | 	}
     ...
  603u| 	case MEC_STATION:	/*  0xa0  */
  604 | 		if (writeflag)
  605u| 			debug("[ sgi_mec: setting the MAC address to "
  606 | 			    "%02x:%02x:%02x:%02x:%02x:%02x ]\n",
  607 | 			    (idata >> 40) & 255, (idata >> 32) & 255,
     ...
  609 | 			    (idata >>  8) & 255, (idata >>  0) & 255);
  610 | 		else
  611u| 			fatal("[ sgi_mec: reading the MAC address as "
  612 | 			    "%02x:%02x:%02x:%02x:%02x:%02x ]\n",
  613 | 			    (odata >> 40) & 255, (odata >> 32) & 255,
     ...
  617u| 	case MEC_STATION_ALT:	/*  0xa8  */
  618 | 		if (writeflag)
  619u| 			debug("[ sgi_mec: setting the ALTERNATIVE MAC address"
  620u| 			    " to %02x:%02x:%02x:%02x:%02x:%02x ]\n",
  621 | 			    (idata >> 40) & 255, (idata >> 32) & 255,
     ...
  623 | 			    (idata >>  8) & 255, (idata >>  0) & 255);
  624 | 		else
  625u| 			debug("[ sgi_mec: reading the ALTERNATIVE MAC address"
  626u| 			    " as %02x:%02x:%02x:%02x:%02x:%02x ]\n",
  627 | 			    (odata >> 40) & 255, (odata >> 32) & 255,
```

## WHAT TO RETURN

EXACTLY ONE fenced ```json block: a list of edits, one per changed call, applied to the file named in each:
  [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; must occur EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line: which rule, and for a narrowing cast why the value is small>"}]
Use JSON escapes: \t for a tab, \n for a newline.  Prefer one whole `u` line as `old`; include a neighbouring line only to
make it unique.  Cover EVERY warning listed; if one should not change, say so after the json block with its line.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBFMT6: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
