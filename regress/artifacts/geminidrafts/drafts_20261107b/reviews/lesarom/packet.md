# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `lesarom` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `lesarom`, state `open`)

**title:** devices/dev_le.c:DEVICE_ACCESS(le) -- the station-address ROM is not decoded at its slot+0x180000 alias and bytes 6-7 carry MAC copies instead of the ESAR checksum -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T58 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-8).  Source URLs: https://github.com/rpajarola/gxemul/commit/0c1e6d122a418955b36a2788a4dc9aaa5f4bbb2a.  Our site at de8c7547: src/devices/dev_le.c:955-956, :1027, :1086-1093 (lines of de8c7547; at 987cb596 the ROM read is :972-976 and the ROM fill :1103-1113, both 17 lines lower; :1027 moved the same way is :1044, the access switch's `default:` arm).  Portable fix: yes -- port rpajarola 0c1e6d1.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_le.c:973 (alias defect), UNSETTLED -- src/devices/dev_le.c:1103-1113 (ESAR checksum).

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_le.c b/src/devices/dev_le.c
index 922bc9b5..6536638b 100644
--- a/src/devices/dev_le.c
+++ b/src/devices/dev_le.c
@@ -970,7 +970,8 @@ DEVICE_ACCESS(le)
 #endif
 
 	/*  Read from station's ROM (ethernet address):  */
-	if (relative_addr >= 0xc0000 && relative_addr <= 0xfffff) {
+	if ((relative_addr >= 0xc0000 && relative_addr <= 0xfffff) ||
+	    (relative_addr >= 0x180000 && relative_addr <= 0x1bffff)) {
 		uint32_t a;
 		int j = (relative_addr & 0xff) / 4;
 		a = d->rom[j & (ROM_SIZE-1)];
@@ -978,11 +979,9 @@ DEVICE_ACCESS(le)
 		if (writeflag == MEM_READ) {
 			odata = (a << 24) + (a << 16) + (a << 8) + a;
 		} else {
-			fatal("[ le: WRITE to ethernet addr (%08lx):",
-			    (long)relative_addr);
-			for (i=0; i<len; i++)
-				fatal(" %02x", data[i]);
-			fatal(" ]\n");
+			debugmsg(d->subsys, "access", VERBOSITY_WARNING,
+			    "write to ethernet addr 0x%06x",
+			    (int)relative_addr);
 		}
 
 		retval = 13;	/*  13 cycles  */
```

## Every edited function, after the fix

### `src/devices/dev_le.c` -- post-edit lines 953-1066 (`+` marks a line the diff added or the point of a deletion)

```c
  953|  DEVICE_ACCESS(le)
  954|  {
  955|  	struct le_data *d = (struct le_data *) extra;
  956|  	uint64_t idata = 0, odata = 0;
  957|  	int retval = 1;
  958|  	size_t i;
  959|  
  960|  	if (writeflag == MEM_WRITE)
  961|  		idata = memory_readmax64(cpu, data, len);
  962|  
  963|  #ifdef LE_DEBUG
  964|  	if (writeflag == MEM_WRITE) {
  965|  		fatal("[ le: write to addr 0x%06x: ", (int)relative_addr);
  966|  		for (i=0; i<len; i++)
  967|  			fatal("%02x ", data[i]);
  968|  		fatal("]\n");
  969|  	}
  970|  #endif
  971|  
  972|  	/*  Read from station's ROM (ethernet address):  */
  973|+ 	if ((relative_addr >= 0xc0000 && relative_addr <= 0xfffff) ||
  974|+ 	    (relative_addr >= 0x180000 && relative_addr <= 0x1bffff)) {
  975|  		uint32_t a;
  976|  		int j = (relative_addr & 0xff) / 4;
  977|  		a = d->rom[j & (ROM_SIZE-1)];
  978|  
  979|  		if (writeflag == MEM_READ) {
  980|  			odata = (a << 24) + (a << 16) + (a << 8) + a;
  981|  		} else {
  982|+ 			debugmsg(d->subsys, "access", VERBOSITY_WARNING,
  983|+ 			    "write to ethernet addr 0x%06x",
  984|+ 			    (int)relative_addr);
  985|  		}
  986|  
  987|  		retval = 13;	/*  13 cycles  */
  988|  		goto do_return;
  989|  	}
  990|  
  991|  
  992|  	switch (relative_addr) {
  993|  
  994|  	/*  Register read/write:  */
  995|  	case 0:
  996|  		if (writeflag==MEM_READ) {
  997|  			odata = d->reg[d->reg_select];
  998|  			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
  999|  			    "READ from register 0x%02x: 0x"
 1000|  			    "%02x", d->reg_select, (int)odata);
 1001|  
 1002|  			/*
 1003|  			 *  #573: CSR1..3 are accessible only while the STOP bit
 1004|  			 *  is SET (a read with STOP clear is "undefined" on the
 1005|  			 *  chip).  The old comment reported that Ultrix seems to
 1006|  			 *  read them with STOP set -- the in-spec case.  The model
 1007|  			 *  answers in either state; gating on STOP is filed, not
 1008|  			 *  implemented, and nothing is announced either way.
 1009|  			 */
 1010|  		} else {
 1011|  			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
 1012|  			    "WRITE to register 0x%02x: 0x%02x",
 1013|  			    d->reg_select, (int)idata);
 1014|  			/*
 1015|  			 *  #573: a write to CSR1..3 with STOP CLEAR is the one
 1016|  			 *  the chip ignores; writes with STOP set are the normal
 1017|  			 *  case (the old comment reported Ultrix writing them with
 1018|  			 *  STOP set).  The model accepts both -- gating on STOP is
 1019|  			 *  filed, not implemented.
 1020|  			 */
 1021|  			le_register_write(d, d->reg_select, idata);
 1022|  		}
 1023|  		break;
 1024|  
 1025|  	/*  Register select:  */
 1026|  	case 4:
 1027|  		if (writeflag==MEM_READ) {
 1028|  			odata = d->reg_select;
 1029|  			debugmsg(d->subsys, "register select", VERBOSITY_DEBUG,
 1030|  			    "READ: 0x%02x", (int)odata);
 1031|  		} else {
 1032|  			debugmsg(d->subsys, "register select", VERBOSITY_DEBUG,
 1033|  			     "WRITE: 0x%02x", (int)idata);
 1034|  			d->reg_select = idata & (N_REGISTERS - 1);
 1035|  
 1036|  			if (idata >= N_REGISTERS)
 1037|  				debugmsg(d->subsys, "register select", VERBOSITY_WARNING,
 1038|  				    "WARNING! register %" PRIu64
 1039|  				    " (max is %i)", (uint64_t)idata,
 1040|  				    N_REGISTERS - 1);
 1041|  		}
 1042|  		break;
 1043|  
 1044|  	default:
 1045|  		if (writeflag==MEM_READ) {
 1046|  			debugmsg(d->subsys, "access", VERBOSITY_WARNING,
 1047|  			    "read from UNIMPLEMENTED addr 0x%06x",
 1048|  			    (int)relative_addr);
 1049|  		} else {
 1050|  			debugmsg(d->subsys, "access", VERBOSITY_WARNING,
 1051|  			    "write to UNIMPLEMENTED addr 0x%06x: "
 1052|  			    "0x%08x", (int)relative_addr, (int)idata);
 1053|  		}
 1054|  	}
 1055|  
 1056|  do_return:
 1057|  	if (writeflag == MEM_READ) {
 1058|  		memory_writemax64(cpu, data, len, odata);
 1059|  		debugmsg(d->subsys, "access", VERBOSITY_DEBUG,
 1060|  		    "read from addr 0x%06" PRIx64 ": 0x%08" PRIx64, (uint64_t)relative_addr, (uint64_t)odata);
 1061|  	}
 1062|  
 1063|  	dev_le_tick(cpu, extra);
 1064|  
 1065|  	return retval;
 1066|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_LESAROM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_LESAROM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
