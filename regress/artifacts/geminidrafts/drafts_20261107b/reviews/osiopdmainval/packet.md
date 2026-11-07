# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `osiopdmainval` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `osiopdmainval`, state `open`)

**title:** devices/dev_osiop.c:write_byte -- SCRIPTS DMA writes guest RAM through the host page without invalidating translated code -- WRONG-RESULT (stale code runs after a DMA load)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T40 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-37).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:261-277.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04 (invalidate on DMA write).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- line 275

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_osiop.c b/src/devices/dev_osiop.c
index 87e9e955..7f79434d 100644
--- a/src/devices/dev_osiop.c
+++ b/src/devices/dev_osiop.c
@@ -273,6 +273,7 @@ static void write_byte(struct osiop_data *d, struct cpu *cpu, uint32_t addr, uin
 	}
 
 	d->last_host_page[addr & 0xfff] = byte;
+	cpu->invalidate_code_translation(cpu, addr, INVALIDATE_PADDR);
 }
```

## Every edited function, after the fix

### `src/devices/dev_osiop.c` -- post-edit lines 261-277 (`+` marks a line the diff added or the point of a deletion)

```c
  261|  static void write_byte(struct osiop_data *d, struct cpu *cpu, uint32_t addr, uint8_t byte)
  262|  {
  263|  	if (d->last_host_page == NULL ||
  264|  	    d->last_phys_page != (addr & 0xfffff000)) {
  265|  		d->last_phys_page = addr & 0xfffff000;
  266|  		d->last_host_page =
  267|  		    memory_paddr_to_hostaddr(cpu->mem, d->last_phys_page, 1);
  268|  	}
  269|  
  270|  	if (d->last_host_page == NULL) {	/* #118 */
  271|  		osiop_hostpage_fault(d);
  272|  		return;
  273|  	}
  274|  
  275|  	d->last_host_page[addr & 0xfff] = byte;
  276|+ 	cpu->invalidate_code_translation(cpu, addr, INVALIDATE_PADDR);
  277|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_OSIOPDMAINVAL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_OSIOPDMAINVAL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
