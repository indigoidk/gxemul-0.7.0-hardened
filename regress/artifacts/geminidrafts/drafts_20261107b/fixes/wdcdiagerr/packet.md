# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `wdcdiagerr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `wdcdiagerr`, state `open`)

**title:** wdcdiagerr  after EXECUTE DEVICE DIAGNOSTIC (and after a channel reset) dev_wdc.c sets `d->error = 1' -- the correct error-REGISTER diagnostic code (01h = no error detected) -- but `status_byte' ORs WDCS_ERR whenever d->error != 0, so the STATUS register shows ERR while the error register says 'no error'; upstream code

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_wdc.c` -- AT HEAD, lines 583-599 (`*` marks a line your previous draft changed)

```c
  583|  static int status_byte(struct wdc_data *d, struct cpu *cpu)
  584|  {
  585|  	int odata = 0;
  586|  	if (diskimage_exist(cpu->machine, d->drive + d->base_drive,
  587|  	    DISKIMAGE_IDE))
  588|  		odata |= WDCS_DRDY | WDCS_DSC;
  589|  	if (d->inbuf_head != d->inbuf_tail)
  590|  		odata |= WDCS_DRQ;
  591|  	if (d->write_in_progress)
  592|  		odata |= WDCS_DRQ;
  593|* 	if (d->error)
  594|* 		odata |= WDCS_ERR;
  595|  	if (d->atapi_cmd_in_progress && (d->atapi_phase & WDCS_DRQ)) {
  596|  		odata |= WDCS_DRQ;
  597|  	}
  598|  	return odata;
  599|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_wdc.c",
    "old": "\tif (d->error)\n\t\todata |= WDCS_ERR;",
    "new": "\tif (d->error && d->error != 0x01)\n\t\todata |= WDCS_ERR;",
    "why": "Hack to prevent diagnostic success (0x01) from asserting ERR, though it breaks WDCE_AMNF."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_WDCDIAGERR: DEFECT, 1 FINDINGS
1. The diff removes the diagnostic symptom at `dev_wdc.c:593` by ensuring `WDCS_ERR` is not set when `d->error == 0x01`. However, as the issue text states, `0x01` also represents the `AMNF` (Address Mark Not Found) ordinary error bit. The diff fails to distinguish between the diagnostic context and ordinary context, missing a necessary state check.
2. HOLDS. No `return`, `goto`, `break`, or early exit is added in the edited function `dev_wdc.c:583-599`. Control flow reaches the common tail at `dev_wdc.c:598` identically.
3. BROKEN. The return value at `dev_wdc.c:598` (`odata`) now drops the `WDCS_ERR` bit if `d->error` is exactly `0x01`. While correct for a diagnostic run, it erroneously means a guest will read a successful status even when an `AMNF` error has occurred. 
4. BROKEN. Beyond removing the diagnostic defect, the diff changes the guest-visible `status_byte` during an `AMNF` failure state. A guest experiencing a real `AMNF` error will now see `WDCS_ERR` cleared at `dev_wdc.c:593`, hiding the error state.
5. HOLDS. There are no new style violations, prints, or comments added in `dev_wdc.c:583-599`.
dev_wdc.c:593 DEFECT The condition incorrectly masks legitimate `AMNF` (0x01) errors because it lacks contextual awareness; fix requires checking the preceding command or diagnostic state.
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_WDCDIAGERR: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_WDCDIAGERR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
