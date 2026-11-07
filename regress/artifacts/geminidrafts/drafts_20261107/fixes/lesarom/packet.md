# GXemul hardened fork -- DRAFT A FIX for one filed issue, `lesarom` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `lesarom`, state `open`, severity `MED`)

**title:** devices/dev_le.c:DEVICE_ACCESS(le) -- the station-address ROM is not decoded at its slot+0x180000 alias and bytes 6-7 carry MAC copies instead of the ESAR checksum -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T58 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-8).  Source URLs: https://github.com/rpajarola/gxemul/commit/0c1e6d122a418955b36a2788a4dc9aaa5f4bbb2a.  Our site at de8c7547: src/devices/dev_le.c:955-956, :1027, :1086-1093 (lines of de8c7547; at 987cb596 the ROM read is :972-976 and the ROM fill :1103-1113, both 17 lines lower; :1027 moved the same way is :1044, the access switch's `default:` arm).  Portable fix: yes -- port rpajarola 0c1e6d1.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 0c1e6d1

## The code at the cited lines

### `src/devices/dev_le.c` around the row's cited line 955 (HEAD 2d25df65, lines 910-1000)

```c
  910| 	struct le_data *d = (struct le_data *) extra;
  911| 	size_t i;
  912| 	int retval;
  913| 
  914| #ifdef LE_DEBUG
  915| 	if (writeflag == MEM_WRITE) {
  916| 		fatal("[ le_sram: write to addr 0x%06x: ", (int)relative_addr);
  917| 		for (i=0; i<len; i++)
  918| 			fatal("%02x ", data[i]);
  919| 		fatal("]\n");
  920| 	}
  921| #endif
  922| 
  923| 	/*  Read/write of the SRAM:  */
  924| 	if (relative_addr < SRAM_SIZE && relative_addr + len <= SRAM_SIZE) {
  925| 		if (writeflag == MEM_READ) {
  926| 			memcpy(data, d->sram + relative_addr, len);
  927| 			if (!quiet_mode) {
  928| 				debug("[ le: read from SRAM offset 0x%05" PRIx64 ":",
  929| 				    (uint64_t)relative_addr);
  930| 				for (i=0; i<len; i++)
  931| 					debug(" %02x", data[i]);
  932| 				debug(" ]\n");
  933| 			}
  934| 			retval = 9;	/*  9 cycles  */
  935| 		} else {
  936| 			memcpy(d->sram + relative_addr, data, len);
  937| 			if (!quiet_mode) {
  938| 				debug("[ le: write to SRAM offset 0x%05" PRIx64 ":",
  939| 				    (uint64_t)relative_addr);
  940| 				for (i=0; i<len; i++)
  941| 					debug(" %02x", data[i]);
  942| 				debug(" ]\n");
  943| 			}
  944| 			retval = 6;	/*  6 cycles  */
  945| 		}
  946| 		return retval;
  947| 	}
  948| 
  949| 	return 0;
  950| }
  951| 
  952| 
  953| DEVICE_ACCESS(le)
  954| {
  955| 	struct le_data *d = (struct le_data *) extra;
  956| 	uint64_t idata = 0, odata = 0;
  957| 	int retval = 1;
  958| 	size_t i;
  959| 
  960| 	if (writeflag == MEM_WRITE)
  961| 		idata = memory_readmax64(cpu, data, len);
  962| 
  963| #ifdef LE_DEBUG
  964| 	if (writeflag == MEM_WRITE) {
  965| 		fatal("[ le: write to addr 0x%06x: ", (int)relative_addr);
  966| 		for (i=0; i<len; i++)
  967| 			fatal("%02x ", data[i]);
  968| 		fatal("]\n");
  969| 	}
  970| #endif
  971| 
  972| 	/*  Read from station's ROM (ethernet address):  */
  973| 	if (relative_addr >= 0xc0000 && relative_addr <= 0xfffff) {
  974| 		uint32_t a;
  975| 		int j = (relative_addr & 0xff) / 4;
  976| 		a = d->rom[j & (ROM_SIZE-1)];
  977| 
  978| 		if (writeflag == MEM_READ) {
  979| 			odata = (a << 24) + (a << 16) + (a << 8) + a;
  980| 		} else {
  981| 			fatal("[ le: WRITE to ethernet addr (%08lx):",
  982| 			    (long)relative_addr);
  983| 			for (i=0; i<len; i++)
  984| 				fatal(" %02x", data[i]);
  985| 			fatal(" ]\n");
  986| 		}
  987| 
  988| 		retval = 13;	/*  13 cycles  */
  989| 		goto do_return;
  990| 	}
  991| 
  992| 
  993| 	switch (relative_addr) {
  994| 
  995| 	/*  Register read/write:  */
  996| 	case 0:
  997| 		if (writeflag==MEM_READ) {
  998| 			odata = d->reg[d->reg_select];
  999| 			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
 1000| 			    "READ from register 0x%02x: 0x"
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_LESAROM: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
