# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `fbctrlvec128` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `fbctrlvec128`, state `open`)

**title:** dev_fbctrl.c's DATA and PORT arms take a 16-byte store as its LOW 64 bits: testppc's stvx/stvxl reach the device with len 16 (default_test() installs fbctrl), the callback receives all 16 bytes, and memory_readmax64() builds idata from the low half -- so a 128-bit COMMAND value whose low half is 0-2 is accepted and runs (a low half of 1 runs SET_RESOLUTION), and a 128-bit selector whose low half is 0-7 is accepted: #567's and #549's width defect one width out

**state_note (head):** filed 2026-10-19 by #567 from its pass 2 (GPT-6 Astra's F1, source-derived: X(stvx) and PPC_31_STVXL hand memory_rw a 16-byte buffer, DATA at +0x10 in the 0x20 window is not truncated, memory_readmax64() keeps the low half on a big-endian guest; testppc installs the device through default_test(), machine_test.c's line 154 -- line 337 is testmips's own install) and its F2 pass (GPT-6 Astra, Grok 4.7 and GLM 5.3: FILE, not this round -- a PowerPC stvx oracle lies outside #567's MIPS detector and a len > 8 refusal would ship unwitnessed; Grok 4.7 and Astra corrected the mechanism the probe's contract had stated: the device is NOT spared the prefix, it receives it and the conversion drops it).  Disclosed as NOT CLAIMED (6) in regress/fbctrl_cmd_probe.py.  LOW: no host kill follows (only 0-2 run), but a wide value is accepted as its low part, the class #567 closed at 64 bits.  Owed: a rung-3 witness on testppc (a 16-byte store at DATA and at PORT), then one disposition for BOTH arms in one round -- a refusal of len > 8 before the conversion, or an acceptance documented as the architecture's.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_fbctrl.c` -- AT HEAD, lines 111-188 (`*` marks a line your previous draft changed)

```c
  111|  DEVICE_ACCESS(fbctrl)
  112|  {
  113|  	struct fbctrl_data *d = (struct fbctrl_data *) extra;
  114|  	uint64_t idata = 0, odata = 0;
  115|  
  116|* 	if (writeflag == MEM_WRITE)
  117|  	        idata = memory_readmax64(cpu, data, len);
  118|  
  119|  	switch (relative_addr) {
  120|  
  121|  	case DEV_FBCTRL_PORT:
  122|  		if (writeflag == MEM_READ)
  123|  			odata = d->current_port;
  124|  		else if (idata >= DEV_FBCTRL_NPORTS) {
  125|  			/*  #549: an out-of-range selector is REFUSED, and
  126|  			    current_port keeps its previous, always-valid value.
  127|  			    It used to be stored as an int with only a warning:
  128|  			    9 made the next DATA access end the emulator in the
  129|  			    range check below, and a wide value was truncated
  130|  			    onto a legal port (0x100000003 selected port 3).
  131|  			    Announced once per device.  */
  132|  			if (!d->warned_port) {
  133|  				fatal("[ fbctrl: port number 0x%llx is out of range; "
  134|  				    "the selector is unchanged (once) ]\n",
  135|  				    (unsigned long long) idata);
  136|  				d->warned_port = 1;
  137|  			}
  138|  		} else
  139|  			d->current_port = idata;
  140|  		break;
  141|  
  142|  	case DEV_FBCTRL_DATA:
  143|  		/*  #549: unreachable while the PORT arm refuses; kept as a
  144|  		    tripwire for a later edit that lets a bad selector in.  */
  145|  		if (d->current_port < 0 || d->current_port
  146|  		    >= DEV_FBCTRL_NPORTS) {
  147|  			fatal("[ fbctrl port number is out of range! ]\n");
  148|  			exit(1);
  149|  		}
  150|  
  151|  		if (writeflag == MEM_READ)
  152|  			odata = d->port[d->current_port];
  153|  		else if (d->current_port == DEV_FBCTRL_PORT_COMMAND &&
  154|  		    idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION) {
  155|  			/*  #567: a command other than NOP, SET_RESOLUTION and
  156|  			    GET_RESOLUTION is REFUSED before it is stored: COMMAND
  157|  			    keeps its previous value and nothing executes.  It used
  158|  			    to reach fbctrl_command()'s default: and end the
  159|  			    emulator, FILL (3) and COPY (4) included -- the header
  160|  			    names them under a TODO and gives them no ports.  The
  161|  			    compare is on all 64 bits: the cell is an int, so a
  162|  			    wide 0x100000001 used to be stored as 1 and run
  163|  			    SET_RESOLUTION.  Announced once per device.  */
  164|  			if (!d->warned_cmd) {
  165|  				fatal("[ fbctrl: command 0x%llx is not supported; "
  166|  				    "the command port is unchanged (once) ]\n",
  167|  				    (unsigned long long) idata);
  168|  				d->warned_cmd = 1;
  169|  			}
  170|  		} else {
  171|  			d->port[d->current_port] = idata;
  172|  			if (d->current_port == DEV_FBCTRL_PORT_COMMAND)
  173|  				fbctrl_command(cpu, d);
  174|  		}
  175|  
  176|  		break;
  177|  
  178|  	default:
  179|  		fatal("[ dev_fbctrl: unimplemented relative addr 0x%x ]\n",
  180|  		    (int)relative_addr);
  181|  		exit(1);
  182|  	}
  183|  
  184|  	if (writeflag == MEM_READ)
  185|  		memory_writemax64(cpu, data, len, odata);
  186|  
  187|  	return 1;
  188|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_fbctrl.c",
    "old": "\tuint64_t idata = 0, odata = 0;\n\n\tif (writeflag == MEM_WRITE)\n\t        idata = memory_readmax64(cpu, data, len);",
    "new": "\tuint64_t idata = 0, odata = 0;\n\n\tif (len > 8) {\n\t\tfatal(\"[ fbctrl: access length > 8 is not supported ]\\n\");\n\t\treturn 1;\n\t}\n\n\tif (writeflag == MEM_WRITE)\n\t        idata = memory_readmax64(cpu, data, len);",
    "why": "Refuse length > 8 on both arms before conversion to avoid dropping upper bytes."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_FBCTRLVEC128: DEFECT, 2 FINDINGS
1. Yes, the diff removes the defect. By checking `len > 8` at lines 116-119, it catches out-of-bounds lengths before `memory_readmax64()` processes them and before the `switch` branches to the DATA or PORT arms.
2. Yes, the added `return 1;` at line 118 skips the function's common tail. It skips: `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata);` (lines 189-190). On a read access with length > 8, this hands the guest an unwritten `data` buffer.
3. No, the path returns `1`, which matches the existing return value at the end of the function (line 192). This implies the access was successfully handled and no bus error or exception should be raised to the guest.
4. Beyond removing the defect, the diff introduces a new console diagnostic on a path that previously printed nothing (a path that used to silently accept and truncate the access now prints a `fatal` message).
5. The new code violates house idioms: the diagnostic lacks a latch (e.g., `d->warned_len`) to prevent spamming the host console, misses the `(once)` marker in the format string, and is missing the `/* #567: ... */` comment tag.
- `src/devices/dev_fbctrl.c:118` DEFECT. Early return skips the common tail on read accesses. Fix: replace `return 1;` with `exit(1);` (similar to line 186) or handle the read properly.
- `src/devices/dev_fbctrl.c:117` STYLE. Diagnostic lacks a once-latch and issue tag. Fix: wrap in `if (!d->warned_len) { ... }` and add `(once)` to the string.
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

End with two lines: `REVISION_FBCTRLVEC128: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_FBCTRLVEC128: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
