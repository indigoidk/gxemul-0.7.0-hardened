# GXemul hardened fork -- DRAFT A FIX for one filed issue, `tcemptyslot` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `tcemptyslot`, state `open`, severity `MED`)

**title:** devices/dev_turbochannel.c:DEVICE_ACCESS -- empty-slot reads at 0x3e0-0x4ff return zero with no bus error on every model -- WRONG-RESULT (KN02-BA PROM reports a bad option ROM per empty slot)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T73 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-45).  Source URLs: https://github.com/rpajarola/gxemul/commit/042b61b040deedf4c1aafb361a563fdc4f9eedb9.  Our site at de8c7547: src/devices/dev_turbochannel.c:143-149.  Portable fix: yes -- port rpajarola 042b61b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 042b61b

## The code at the cited lines

### `src/devices/dev_turbochannel.c` around the row's cited line 143 (HEAD 2d25df65, lines 98-188)

```c
   98| 		case 0x3f4:
   99| 			odata = 0x00000000; debug("ROM signature byte 1");
  100| 			break;
  101| 		case 0x3f8:
  102| 			odata = 0xaaaaaaaa; debug("ROM signature byte 2");
  103| 			break;
  104| 		case 0x3fc:
  105| 			odata = 0xffffffff; debug("ROM signature byte 3");
  106| 			break;
  107| 		case 0x470:
  108| 			/*  0=nothing, 1=parity  */
  109| 			odata = 0x00000000; debug("flags"); break;
  110| 		default:
  111| 			if (relative_addr >= 0x400 && relative_addr < 0x420)
  112| 				odata = d->card_firmware_version[
  113| 				    (relative_addr-0x400)/4];
  114| 			else if (relative_addr >= 0x420 &&
  115| 			    relative_addr < 0x440)
  116| 				odata = d->card_vendor_name[
  117| 				    (relative_addr-0x420)/4];
  118| 			else if (relative_addr >= 0x440 &&
  119| 			    relative_addr < 0x460)
  120| 				odata = d->card_module_name[
  121| 				    (relative_addr-0x440)/4];
  122| 			else if (relative_addr >= 0x460 &&
  123| 			    relative_addr < 0x470)
  124| 				odata = d->card_firmware_type[
  125| 				    (relative_addr-0x460)/4];
  126| 			else {
  127| 				debug("?");
  128| 			}
  129| 		}
  130| 
  131| 		/*
  132| 		 *  If this slot is empty, return an error so that a DBE
  133| 		 *  exception is caused. (This is the way DECstation operating
  134| 		 *  systems have to detect the absence of cards in a
  135| 		 *  TURBOchannel slot.)
  136| 		 *
  137| 		 *  NOTE:  The Sprite kernel reads from offsets 0x3e0..0x400
  138| 		 *  without handling the DBE exception, and both Ultrix and
  139| 		 *  NetBSD seem to detect the DBE exception using addresses
  140| 		 *  around offset 0x0 or 0x3c0000.  This code seems to work
  141| 		 *  with all of the those OS kernels:
  142| 		 */
  143| 		if (d->card_module_name[0] ==  ' ') {
  144| 			/*  Return no data for empty slot:  */
  145| 			odata = 0;
  146| 
  147| 			/*  Return DBE exception in some cases:  */
  148| 			if (relative_addr < 0x3e0 || relative_addr >= 0x500)
  149| 				return 0;
  150| 		}
  151| 
  152| 		debug(") ]\n");
  153| 	} else {
  154| 		debug("[ turbochannel: write to  0x%08lx: 0x%08x ]\n",
  155| 		    (long)relative_addr, (int)idata);
  156| 	}
  157| 
  158| 	if (writeflag == MEM_READ)
  159| 		memory_writemax64(cpu, data, len, odata);
  160| 
  161| 	return 1;
  162| }
  163| 
  164| 
  165| /*
  166|  *  dev_turbochannel_init():
  167|  *
  168|  *  This is a generic turbochannel card device.  device_name should point
  169|  *  to a string such as "PMAG-BA".
  170|  *
  171|  *  TODO: When running for example dual-head, maybe the name of each
  172|  *        framebuffer should include the card slot number?
  173|  */
  174| void dev_turbochannel_init(struct machine *machine, struct memory *mem,
  175| 	int slot_nr, uint64_t baseaddr, uint64_t endaddr,
  176| 	const char *device_name, const char *irq_path)
  177| {
  178| 	struct vfb_data *fb;
  179| 	struct turbochannel_data *d;
  180| 	int rom_offset=0x3c0000, rom_length=DEV_TURBOCHANNEL_LEN, rom_skip=0;
  181| 	char *name2;
  182| 	size_t nlen;
  183| 
  184| 	if (device_name == NULL)
  185| 		return;
  186| 
  187| 	if (strlen(device_name) > 8) {
  188| 		fprintf(stderr, "dev_turbochannel_init(): bad device_name\n");
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

End with one line: `FIXDRAFT_TCEMPTYSLOT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
