# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `fbctrlvec128` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `fbctrlvec128`, state `open`)

**title:** dev_fbctrl.c's DATA and PORT arms take a 16-byte store as its LOW 64 bits: testppc's stvx/stvxl reach the device with len 16 (default_test() installs fbctrl), the callback receives all 16 bytes, and memory_readmax64() builds idata from the low half -- so a 128-bit COMMAND value whose low half is 0-2 is accepted and runs (a low half of 1 runs SET_RESOLUTION), and a 128-bit selector whose low half is 0-7 is accepted: #567's and #549's width defect one width out

**state_note (head):** filed 2026-10-19 by #567 from its pass 2 (GPT-6 Astra's F1, source-derived: X(stvx) and PPC_31_STVXL hand memory_rw a 16-byte buffer, DATA at +0x10 in the 0x20 window is not truncated, memory_readmax64() keeps the low half on a big-endian guest; testppc installs the device through default_test(), machine_test.c's line 154 -- line 337 is testmips's own install) and its F2 pass (GPT-6 Astra, Grok 4.7 and GLM 5.3: FILE, not this round -- a PowerPC stvx oracle lies outside #567's MIPS detector and a len > 8 refusal would ship unwitnessed; Grok 4.7 and Astra corrected the mechanism the probe's contract had stated: the device is NOT spared the prefix, it receives it and the conversion drops it).  Disclosed as NOT CLAIMED (6) in regress/fbctrl_cmd_probe.py.  LOW: no host kill follows (only 0-2 run), but a wide value is accepted as its low part, the class #567 closed at 64 bits.  Owed: a rung-3 witness on testppc (a 16-byte store at DATA and at PORT), then one disposition for BOTH arms in one round -- a refusal of len > 8 before the conversion, or an acceptance documented as the architecture's.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_fbctrl.c:116

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_fbctrl.c b/src/devices/dev_fbctrl.c
index 2013d66e..8ed54d90 100644
--- a/src/devices/dev_fbctrl.c
+++ b/src/devices/dev_fbctrl.c
@@ -113,6 +113,12 @@ DEVICE_ACCESS(fbctrl)
 	struct fbctrl_data *d = (struct fbctrl_data *) extra;
 	uint64_t idata = 0, odata = 0;
 
+	if (len > 8) {
+		/*  #567: a memory access wider than 8 bytes is REFUSED before conversion.  */
+		fatal("[ fbctrl: access length > 8 is not supported ]\n");
+		exit(1);
+	}
+
 	if (writeflag == MEM_WRITE)
 	        idata = memory_readmax64(cpu, data, len);
```

## Every edited function, after the fix

### `src/devices/dev_fbctrl.c` -- post-edit lines 111-194 (`+` marks a line the diff added or the point of a deletion)

```c
  111|  DEVICE_ACCESS(fbctrl)
  112|  {
  113|  	struct fbctrl_data *d = (struct fbctrl_data *) extra;
  114|  	uint64_t idata = 0, odata = 0;
  115|  
  116|+ 	if (len > 8) {
  117|+ 		/*  #567: a memory access wider than 8 bytes is REFUSED before conversion.  */
  118|+ 		fatal("[ fbctrl: access length > 8 is not supported ]\n");
  119|+ 		exit(1);
  120|+ 	}
  121|+ 
  122|  	if (writeflag == MEM_WRITE)
  123|  	        idata = memory_readmax64(cpu, data, len);
  124|  
  125|  	switch (relative_addr) {
  126|  
  127|  	case DEV_FBCTRL_PORT:
  128|  		if (writeflag == MEM_READ)
  129|  			odata = d->current_port;
  130|  		else if (idata >= DEV_FBCTRL_NPORTS) {
  131|  			/*  #549: an out-of-range selector is REFUSED, and
  132|  			    current_port keeps its previous, always-valid value.
  133|  			    It used to be stored as an int with only a warning:
  134|  			    9 made the next DATA access end the emulator in the
  135|  			    range check below, and a wide value was truncated
  136|  			    onto a legal port (0x100000003 selected port 3).
  137|  			    Announced once per device.  */
  138|  			if (!d->warned_port) {
  139|  				fatal("[ fbctrl: port number 0x%llx is out of range; "
  140|  				    "the selector is unchanged (once) ]\n",
  141|  				    (unsigned long long) idata);
  142|  				d->warned_port = 1;
  143|  			}
  144|  		} else
  145|  			d->current_port = idata;
  146|  		break;
  147|  
  148|  	case DEV_FBCTRL_DATA:
  149|  		/*  #549: unreachable while the PORT arm refuses; kept as a
  150|  		    tripwire for a later edit that lets a bad selector in.  */
  151|  		if (d->current_port < 0 || d->current_port
  152|  		    >= DEV_FBCTRL_NPORTS) {
  153|  			fatal("[ fbctrl port number is out of range! ]\n");
  154|  			exit(1);
  155|  		}
  156|  
  157|  		if (writeflag == MEM_READ)
  158|  			odata = d->port[d->current_port];
  159|  		else if (d->current_port == DEV_FBCTRL_PORT_COMMAND &&
  160|  		    idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION) {
  161|  			/*  #567: a command other than NOP, SET_RESOLUTION and
  162|  			    GET_RESOLUTION is REFUSED before it is stored: COMMAND
  163|  			    keeps its previous value and nothing executes.  It used
  164|  			    to reach fbctrl_command()'s default: and end the
  165|  			    emulator, FILL (3) and COPY (4) included -- the header
  166|  			    names them under a TODO and gives them no ports.  The
  167|  			    compare is on all 64 bits: the cell is an int, so a
  168|  			    wide 0x100000001 used to be stored as 1 and run
  169|  			    SET_RESOLUTION.  Announced once per device.  */
  170|  			if (!d->warned_cmd) {
  171|  				fatal("[ fbctrl: command 0x%llx is not supported; "
  172|  				    "the command port is unchanged (once) ]\n",
  173|  				    (unsigned long long) idata);
  174|  				d->warned_cmd = 1;
  175|  			}
  176|  		} else {
  177|  			d->port[d->current_port] = idata;
  178|  			if (d->current_port == DEV_FBCTRL_PORT_COMMAND)
  179|  				fbctrl_command(cpu, d);
  180|  		}
  181|  
  182|  		break;
  183|  
  184|  	default:
  185|  		fatal("[ dev_fbctrl: unimplemented relative addr 0x%x ]\n",
  186|  		    (int)relative_addr);
  187|  		exit(1);
  188|  	}
  189|  
  190|  	if (writeflag == MEM_READ)
  191|  		memory_writemax64(cpu, data, len, odata);
  192|  
  193|  	return 1;
  194|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_FBCTRLVEC128: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_FBCTRLVEC128: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
