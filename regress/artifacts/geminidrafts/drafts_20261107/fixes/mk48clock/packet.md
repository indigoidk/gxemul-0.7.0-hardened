# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mk48clock` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mk48clock`, state `open`, severity `MED`)

**title:** devices/dev_mk48txx.c -- the time-of-day registers refresh only at init and on a READ 0-to-1 transition -- WRONG-RESULT (clock does not run)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T88 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-48).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_mk48txx.c:165, :129-135.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 06 (NVRAM file backing is a feature).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 06.

## The code at the cited lines

### `src/devices/dev_mk48txx.c` around the row's cited line 165 (HEAD d2a6f233, lines 120-174)

```c
  120| 		if (writeflag == MEM_WRITE)
  121| 			d->reg[relative_addr] = idata;
  122| 		goto ret;
  123| 	}
  124| 
  125| 	switch (relative_addr) {
  126| 
  127| 	case MK48T08_CLKOFF + MK48TXX_ICSR:
  128| 		if (writeflag == MEM_WRITE) {
  129| 			if ((idata & MK48TXX_CSR_READ) &&
  130| 			    !(d->reg[relative_addr] & MK48TXX_CSR_READ)) {
  131| 				/*  Switching the read bit from 0 to 1 causes
  132| 				    registers to be "froozen". In the emulator,
  133| 				    simply updating them with data from the
  134| 				    host should be good enough.  */
  135| 				mk48txx_update_regs(d);
  136| 			}
  137| 			d->reg[relative_addr] = idata;
  138| 		}
  139| 		break;
  140| 
  141| 	default:if (writeflag == MEM_READ)
  142| 			fatal("[ mk48txx: unimplemented READ from offset 0x%x ]"
  143| 			    "\n", (int)relative_addr);
  144| 		else
  145| 			fatal("[ mk48txx: unimplemented WRITE to offset 0x%x: "
  146| 			    "0x%x ]\n", (int)relative_addr, (int)idata);
  147| 		exit(1);
  148| 	}
  149| 
  150| ret:
  151| 	if (writeflag == MEM_READ)
  152| 		memory_writemax64(cpu, data, len, odata);
  153| 
  154| 	return 1;
  155| }
  156| 
  157| 
  158| DEVINIT(mk48txx)
  159| {
  160| 	struct mk48txx_data *d;
  161| 
  162| 	CHECK_ALLOCATION(d = (struct mk48txx_data *) malloc(sizeof(struct mk48txx_data)));
  163| 	memset(d, 0, sizeof(struct mk48txx_data));
  164| 
  165| 	mk48txx_update_regs(d);
  166| 
  167| 	memory_device_register(devinit->machine->memory, devinit->name,
  168| 	    devinit->addr, MK48TXX_LEN, dev_mk48txx_access, (void *)d,
  169| 	    DM_DEFAULT, NULL);
  170| 
  171| 	return 1;
  172| }
  173| 
  174| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_mk48txx.c` -- `struct mk48txx_data {` (HEAD lines 53-55)

```c
   53| struct mk48txx_data {
   54| 	uint8_t		reg[MK48TXX_LEN];
   55| };
```

RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_MK48CLOCK: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
