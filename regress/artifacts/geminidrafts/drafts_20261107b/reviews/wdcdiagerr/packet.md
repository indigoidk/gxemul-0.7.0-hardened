# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `wdcdiagerr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `wdcdiagerr`, state `open`)

**title:** wdcdiagerr  after EXECUTE DEVICE DIAGNOSTIC (and after a channel reset) dev_wdc.c sets `d->error = 1' -- the correct error-REGISTER diagnostic code (01h = no error detected) -- but `status_byte' ORs WDCS_ERR whenever d->error != 0, so the STATUS register shows ERR while the error register says 'no error'; upstream code

**state_note (head):** FILE, LOW, live-latent.  Reachability CHECKED against the in-tree OpenBSD 2.2 driver (isa/wdc.c): wdcprobe issues WDCC_DIAGNOSE then `wait_for_unbusy', whose wdcwait returns WDCS_ERR (positive) when the status has ERR -- the probe tests `< 0', so OpenBSD 2.2 TOLERATES the spurious ERR; wdcreset reads and discards wd_error.  Other guests' drivers (NetBSD, Linux) untested; a driver that treats ERR after DIAGNOSE as a failed drive would not attach.  Found by Fable one grep from a batch-3a row; upstream (import 39748e3).  Fix shape: clear d->error's effect on the ERR bit for the diagnostic code (keep the register value), with a row reading status + error after WDCC_DIAGNOSE.  Provenance: retrospective re-check (owner directive 2026-09-04) batch 3a -- GPT-6 Astra (codex, max effort) read-only review, adjudicated by Fable 5.1; artifacts regress/artifacts/retro_20260905/batch3a_wdc/ (astra_batch3a.txt, fable_adj_batch3a.md).  The other seven panel seats were DELIBERATELY NOT FIRED on the retrospective (owner scope); a fix round runs the full nine-seat panel.

*** THE ROW'S PREMISE IS INVERTED BY ATA-2, AND THE REAL DEFECT IS BETTER THAN THE ONE I FILED.  2026-09-11 (ata2batch/codex_ata2batch_20260911.txt), then traced locally before recording. ***

**I filed this as "the model writes 1 where the correct diagnostic code belongs".  `0x01` IS THE CORRECT CODE.**  ATA-2 `:2534-2535`: *"Device 1 sets bit 7 of the Error register to zero and posts its diagnostic results to bits 6 through 0 of Error register"*, and the reset algorithm at `:5083-5084`: *"If Device 1 completed all initialization and diagnostic without error, Set the Error register to 01h and assert PDIAG-."*  So the VALUE the model writes is right.

*** THE DEFECT IS THE COUPLING, NOT THE VALUE -- AND `d->error' IS ONE VARIABLE SERVING TWO REGISTERS WITH OPPOSITE MEANINGS. ***  Traced in `dev_wdc.c`:
  * `:1843`  `odata = d->error;`                     -- it IS the **Error register** content;
  * `:594`   `if (d->error) odata |= WDCS_ERR;`      -- it ALSO drives the **Status register's ERR**
                                                        flag, inside `status_byte()`.

**ATA-2 keeps those apart and the header does too**: the generic `ERR` flag belongs to the STATUS register, while the Error register holds either a diagnostic code or ordinary error bits depending on context -- `0x01` is *diagnostic success* after a reset or diagnostic, and `AMNF`, Address Mark Not Found, under the ordinary interpret [... 8700 more characters not shown]

**The drafter's own reading:** STILL PRESENT: YES -- `dev_wdc.c:593`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_wdc.c b/src/devices/dev_wdc.c
index e369ebc0..19f3e9df 100644
--- a/src/devices/dev_wdc.c
+++ b/src/devices/dev_wdc.c
@@ -590,7 +590,7 @@ static int status_byte(struct wdc_data *d, struct cpu *cpu)
 		odata |= WDCS_DRQ;
 	if (d->write_in_progress)
 		odata |= WDCS_DRQ;
-	if (d->error)
+	if (d->error && d->error != 0x01)
 		odata |= WDCS_ERR;
 	if (d->atapi_cmd_in_progress && (d->atapi_phase & WDCS_DRQ)) {
 		odata |= WDCS_DRQ;
```

## Every edited function, after the fix

### `src/devices/dev_wdc.c` -- post-edit lines 583-599 (`+` marks a line the diff added or the point of a deletion)

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
  593|+ 	if (d->error && d->error != 0x01)
  594|  		odata |= WDCS_ERR;
  595|  	if (d->atapi_cmd_in_progress && (d->atapi_phase & WDCS_DRQ)) {
  596|  		odata |= WDCS_DRQ;
  597|  	}
  598|  	return odata;
  599|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_WDCDIAGERR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_WDCDIAGERR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
