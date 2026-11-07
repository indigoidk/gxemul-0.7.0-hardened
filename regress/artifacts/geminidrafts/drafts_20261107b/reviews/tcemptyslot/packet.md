# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `tcemptyslot` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `tcemptyslot`, state `open`)

**title:** devices/dev_turbochannel.c:DEVICE_ACCESS -- empty-slot reads at 0x3e0-0x4ff return zero with no bus error on every model -- WRONG-RESULT (KN02-BA PROM reports a bad option ROM per empty slot)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T73 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-45).  Source URLs: https://github.com/rpajarola/gxemul/commit/042b61b040deedf4c1aafb361a563fdc4f9eedb9.  Our site at de8c7547: src/devices/dev_turbochannel.c:143-149.  Portable fix: yes -- port rpajarola 042b61b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_turbochannel.c:148

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_turbochannel.c b/src/devices/dev_turbochannel.c
index 9f9a1a39..77431622 100644
--- a/src/devices/dev_turbochannel.c
+++ b/src/devices/dev_turbochannel.c
@@ -145,8 +145,10 @@ DEVICE_ACCESS(turbochannel)
 			odata = 0;
 
 			/*  Return DBE exception in some cases:  */
-			if (relative_addr < 0x3e0 || relative_addr >= 0x500)
+			if (relative_addr < 0x3e0 || relative_addr >= 0x400) {
+				debug(") ]\n");
 				return 0;
+			}
 		}
 
 		debug(") ]\n");
```

## Every edited function, after the fix

### `src/devices/dev_turbochannel.c` -- post-edit lines 64-164 (`+` marks a line the diff added or the point of a deletion)

```c
   64|  DEVICE_ACCESS(turbochannel)
   65|  {
   66|  	struct turbochannel_data *d = (struct turbochannel_data *) extra;
   67|  	uint64_t idata = 0, odata = 0;
   68|  
   69|  	if (writeflag == MEM_WRITE)
   70|  		idata = memory_readmax64(cpu, data, len);
   71|  
   72|  	relative_addr += d->rom_skip;
   73|  
   74|  	if (writeflag == MEM_READ) {
   75|  		debug("[ turbochannel: read from slot %i addr 0x%08lx (",
   76|  		    d->slot_nr, (long)relative_addr);
   77|  
   78|  		relative_addr &= 0x7fff;
   79|  
   80|  		switch (relative_addr) {
   81|  		case 0x3e0:
   82|  			odata = 0x00000001; debug("ROM width");
   83|  			break;
   84|  		case 0x3e4:
   85|  			odata = 0x00000004; debug("ROM stride");
   86|  			break;
   87|  		case 0x3e8:
   88|  			/*  8KB * romsize  */
   89|  			odata = 0x00000001; debug("ROM size");
   90|  			break;
   91|  		case 0x3ec:
   92|  			/*  4MB * slotsize  */
   93|  			odata = 0x00000001; debug("slot size");
   94|  			break;
   95|  		case 0x3f0:
   96|  			odata = 0x55555555; debug("ROM signature byte 0");
   97|  			break;
   98|  		case 0x3f4:
   99|  			odata = 0x00000000; debug("ROM signature byte 1");
  100|  			break;
  101|  		case 0x3f8:
  102|  			odata = 0xaaaaaaaa; debug("ROM signature byte 2");
  103|  			break;
  104|  		case 0x3fc:
  105|  			odata = 0xffffffff; debug("ROM signature byte 3");
  106|  			break;
  107|  		case 0x470:
  108|  			/*  0=nothing, 1=parity  */
  109|  			odata = 0x00000000; debug("flags"); break;
  110|  		default:
  111|  			if (relative_addr >= 0x400 && relative_addr < 0x420)
  112|  				odata = d->card_firmware_version[
  113|  				    (relative_addr-0x400)/4];
  114|  			else if (relative_addr >= 0x420 &&
  115|  			    relative_addr < 0x440)
  116|  				odata = d->card_vendor_name[
  117|  				    (relative_addr-0x420)/4];
  118|  			else if (relative_addr >= 0x440 &&
  119|  			    relative_addr < 0x460)
  120|  				odata = d->card_module_name[
  121|  				    (relative_addr-0x440)/4];
  122|  			else if (relative_addr >= 0x460 &&
  123|  			    relative_addr < 0x470)
  124|  				odata = d->card_firmware_type[
  125|  				    (relative_addr-0x460)/4];
  126|  			else {
  127|  				debug("?");
  128|  			}
  129|  		}
  130|  
  131|  		/*
  132|  		 *  If this slot is empty, return an error so that a DBE
  133|  		 *  exception is caused. (This is the way DECstation operating
  134|  		 *  systems have to detect the absence of cards in a
  135|  		 *  TURBOchannel slot.)
  136|  		 *
  137|  		 *  NOTE:  The Sprite kernel reads from offsets 0x3e0..0x400
  138|  		 *  without handling the DBE exception, and both Ultrix and
  139|  		 *  NetBSD seem to detect the DBE exception using addresses
  140|  		 *  around offset 0x0 or 0x3c0000.  This code seems to work
  141|  		 *  with all of the those OS kernels:
  142|  		 */
  143|  		if (d->card_module_name[0] ==  ' ') {
  144|  			/*  Return no data for empty slot:  */
  145|  			odata = 0;
  146|  
  147|  			/*  Return DBE exception in some cases:  */
  148|+ 			if (relative_addr < 0x3e0 || relative_addr >= 0x400) {
  149|+ 				debug(") ]\n");
  150|  				return 0;
  151|+ 			}
  152|  		}
  153|  
  154|  		debug(") ]\n");
  155|  	} else {
  156|  		debug("[ turbochannel: write to  0x%08lx: 0x%08x ]\n",
  157|  		    (long)relative_addr, (int)idata);
  158|  	}
  159|  
  160|  	if (writeflag == MEM_READ)
  161|  		memory_writemax64(cpu, data, len, odata);
  162|  
  163|  	return 1;
  164|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_TCEMPTYSLOT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_TCEMPTYSLOT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
