# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `strtoullbase` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `strtoullbase`, state `open`)

**title:** src/core/misc.c:175-191 -- mystrtoull() accepts a digit at or above the base (for example 9 in an octal number) and wraps silently on long input -- WRONG-RESULT (host command line and configuration file)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/core/misc.c:186

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/core/misc.c b/src/core/misc.c
index b1c90d29..e02a50cd 100644
--- a/src/core/misc.c
+++ b/src/core/misc.c
@@ -182,6 +182,9 @@ unsigned long long mystrtoull(const char *s, char **endp, int base)
 			c = c - 'A' + 10;
 		else
 			break;
+		/* #001: check base and overflow */
+		if (c >= base || res > (~0ULL - c) / base)
+			break;
 		switch (base) {
 		case 8:	res = (res << 3) | c;
 			break;
```

## Every edited function, after the fix

### `src/core/misc.c` -- post-edit lines 139-201 (`+` marks a line the diff added or the point of a deletion)

```c
  139|  unsigned long long mystrtoull(const char *s, char **endp, int base)
  140|  {
  141|  	unsigned long long res = 0;
  142|  	int minus_sign = 0;
  143|  
  144|  	if (s == NULL)
  145|  		return 0;
  146|  
  147|  	/*  TODO: Implement endp?  */
  148|  	if (endp != NULL) {
  149|  		fprintf(stderr, "mystrtoull(): endp isn't implemented\n");
  150|  		exit(1);
  151|  	}
  152|  
  153|  	if (s[0] == '-') {
  154|  		minus_sign = 1;
  155|  		s++;
  156|  	}
  157|  
  158|  	/*  Guess base:  */
  159|  	if (base == 0) {
  160|  		if (s[0] == '0') {
  161|  			/*  Just "0"? :-)  */
  162|  			if (!s[1])
  163|  				return 0;
  164|  			if (s[1] == 'x' || s[1] == 'X') {
  165|  				base = 16;
  166|  				s += 2;
  167|  			} else {
  168|  				base = 8;
  169|  				s ++;
  170|  			}
  171|  		} else if (s[0] >= '1' && s[0] <= '9')
  172|  			base = 10;
  173|  	}
  174|  
  175|  	while (s[0]) {
  176|  		int c = s[0];
  177|  		if (c >= '0' && c <= '9')
  178|  			c -= '0';
  179|  		else if (c >= 'a' && c <= 'f')
  180|  			c = c - 'a' + 10;
  181|  		else if (c >= 'A' && c <= 'F')
  182|  			c = c - 'A' + 10;
  183|  		else
  184|  			break;
  185|+ 		/* #001: check base and overflow */
  186|+ 		if (c >= base || res > (~0ULL - c) / base)
  187|+ 			break;
  188|  		switch (base) {
  189|  		case 8:	res = (res << 3) | c;
  190|  			break;
  191|  		case 16:res = (res << 4) | c;
  192|  			break;
  193|  		default:res = (res * base) + c;
  194|  		}
  195|  		s++;
  196|  	}
  197|  
  198|  	if (minus_sign)
  199|  		res = (uint64_t) -(int64_t)res;
  200|  	return res;
  201|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_STRTOULLBASE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_STRTOULLBASE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
