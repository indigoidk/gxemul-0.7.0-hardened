# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mk48gmtime` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mk48gmtime`, state `open`)

**title:** src/devices/dev_mk48txx.c:63-66 -- the gmtime() result is used without a NULL test (the argument is time(NULL)) -- NULL (host only)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 66| 	d->reg[MK48T08_CLKOFF + MK48TXX_ISEC] = BCD(tmp->tm_sec);

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mk48txx.c b/src/devices/dev_mk48txx.c
index 16174d78..659db5bc 100644
--- a/src/devices/dev_mk48txx.c
+++ b/src/devices/dev_mk48txx.c
@@ -63,6 +63,10 @@ void mk48txx_update_regs(struct mk48txx_data *d)
 	timet = time(NULL);
 	tmp = gmtime(&timet);
 
+	/* #mk48gmtime: gmtime() can return NULL */
+	if (tmp == NULL)
+		return;
+
 	d->reg[MK48T08_CLKOFF + MK48TXX_ISEC] = BCD(tmp->tm_sec);
 	d->reg[MK48T08_CLKOFF + MK48TXX_IMIN] = BCD(tmp->tm_min);
 	d->reg[MK48T08_CLKOFF + MK48TXX_IHOUR] = BCD(tmp->tm_hour);
```

## Every edited function, after the fix

### `src/devices/dev_mk48txx.c` -- post-edit lines 58-77 (`+` marks a line the diff added or the point of a deletion)

```c
   58|  void mk48txx_update_regs(struct mk48txx_data *d)
   59|  {
   60|  	struct tm *tmp;
   61|  	time_t timet;
   62|  
   63|  	timet = time(NULL);
   64|  	tmp = gmtime(&timet);
   65|  
   66|+ 	/* #mk48gmtime: gmtime() can return NULL */
   67|+ 	if (tmp == NULL)
   68|+ 		return;
   69|+ 
   70|  	d->reg[MK48T08_CLKOFF + MK48TXX_ISEC] = BCD(tmp->tm_sec);
   71|  	d->reg[MK48T08_CLKOFF + MK48TXX_IMIN] = BCD(tmp->tm_min);
   72|  	d->reg[MK48T08_CLKOFF + MK48TXX_IHOUR] = BCD(tmp->tm_hour);
   73|  	d->reg[MK48T08_CLKOFF + MK48TXX_IWDAY] = tmp->tm_wday + 1;
   74|  	d->reg[MK48T08_CLKOFF + MK48TXX_IDAY] = BCD(tmp->tm_mday);
   75|  	d->reg[MK48T08_CLKOFF + MK48TXX_IMON] = BCD(tmp->tm_mon + 1);
   76|  	d->reg[MK48T08_CLKOFF + MK48TXX_IYEAR] = BCD(tmp->tm_year % 100);
   77|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MK48GMTIME: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MK48GMTIME: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
