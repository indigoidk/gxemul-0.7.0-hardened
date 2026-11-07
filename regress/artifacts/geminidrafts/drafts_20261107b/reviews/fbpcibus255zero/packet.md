# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `fbpcibus255zero` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `fbpcibus255zero`, state `open`)

**title:** A PCI-config read decoding to bus 255 returns 0, not the no-device answer

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): CONFIRMED-NEW MED `fbpcibus255zero` "A PCI-config read decoding to bus 255 returns 0, not the no-device answer".** `dev_footbridge.c:486-491`: after `bus_pci_setaddr`, bus 255 prints and `return 1` BEFORE `bus_pci_data_access()` (`:498-499`) and before the read writeback (`:501-502`); `memory_rw.c:491-492` has pre-zeroed the buffer, so the guest reads 0. Everywhere else an absent device...

**The drafter's own reading:** STILL PRESENT: YES -- dev_footbridge.c:496

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_footbridge.c b/src/devices/dev_footbridge.c
index 77f7d960..8315a418 100644
--- a/src/devices/dev_footbridge.c
+++ b/src/devices/dev_footbridge.c
@@ -493,6 +493,10 @@ DEVICE_ACCESS(footbridge_pci)
 		    " pc (might not be updated) = 0x%08x ]\n", (int)cpu->pc);
 		/*  #220: (Codex/Fable) don't exit() the host on a guest PCI
 		    access to the (unlikely) bus 255; treat it as handled.  */
+		if (writeflag == MEM_READ) {
+			/* #NNN: Empty PCI bus reads return all 1s */
+			memory_writemax64(cpu, data, len|MEM_PCI_LITTLE_ENDIAN, ~0ULL);
+		}
 		return 1;
 	}
```

## Every edited function, after the fix

### `src/devices/dev_footbridge.c` -- post-edit lines 478-514 (`+` marks a line the diff added or the point of a deletion)

```c
  478|  DEVICE_ACCESS(footbridge_pci)
  479|  {
  480|  	struct footbridge_data *d = (struct footbridge_data *) extra;
  481|  	uint64_t idata = 0, odata = 0;
  482|  	int bus, dev, func, reg;
  483|  
  484|  	if (writeflag == MEM_WRITE)
  485|  		idata = memory_readmax64(cpu, data, len|MEM_PCI_LITTLE_ENDIAN);
  486|  
  487|  	/*  Decompose the (direct) address into its components:  */
  488|  	bus_pci_decompose_1(relative_addr, &bus, &dev, &func, &reg);
  489|  	bus_pci_setaddr(cpu, d->pcibus, bus, dev, func, reg);
  490|  
  491|  	if (bus == 255) {
  492|  		fatal("[ footbridge DEBUG ERROR: bus 255 unlikely,"
  493|  		    " pc (might not be updated) = 0x%08x ]\n", (int)cpu->pc);
  494|  		/*  #220: (Codex/Fable) don't exit() the host on a guest PCI
  495|  		    access to the (unlikely) bus 255; treat it as handled.  */
  496|+ 		if (writeflag == MEM_READ) {
  497|+ 			/* #NNN: Empty PCI bus reads return all 1s */
  498|+ 			memory_writemax64(cpu, data, len|MEM_PCI_LITTLE_ENDIAN, ~0ULL);
  499|+ 		}
  500|  		return 1;
  501|  	}
  502|  
  503|  	debug("[ footbridge pci: %s bus %i, device %i, function %i, register "
  504|  	    "%i ]\n", writeflag == MEM_READ? "read from" : "write to", bus,
  505|  	    dev, func, reg);
  506|  
  507|  	bus_pci_data_access(cpu, d->pcibus, writeflag == MEM_READ?
  508|  	    &odata : &idata, len, writeflag);
  509|  
  510|  	if (writeflag == MEM_READ)
  511|  		memory_writemax64(cpu, data, len|MEM_PCI_LITTLE_ENDIAN, odata);
  512|  
  513|  	return 1;
  514|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_FBPCIBUS255ZERO: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_FBPCIBUS255ZERO: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
