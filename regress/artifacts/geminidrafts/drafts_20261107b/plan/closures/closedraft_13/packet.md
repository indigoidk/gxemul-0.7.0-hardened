# Reading task: closedraft_13 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE13-e381` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `leiadrbit0` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** src/devices/dev_le.c:179-182 -- init_block_addr takes CSR1 bit 0 (only a warning follows), where IADR is CSR1 bits 15:1 and bit 0 must be zero -- DOCUMENTED (an interpretation)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** the behavior is an interpretation of the datasheet that is already documented and appropriately issues a warning.

### ROW `pciabsentallones` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** src/devices/bus_pci.c:110-115 -- a config read of an absent device returns all-ones only for register 0 and zero for every other register -- DOCUMENTED (design question)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** explicitly documented as emulator-compatibility oracle

### ROW `rs5c313gmtime` -- state `open`, severity `LOW`; PROPOSED: **DROP**

**title:** src/devices/dev_rs5c313.c:69-72 -- the gmtime() result is used without a NULL test (the argument is time(NULL)) -- NULL (host only)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** unreachable by guest input

### ROW `sprstringsbound` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** src/include/make_ppc_spr_strings.c:36,54-56 -- the build tool stores names[n] with n taken from strtol() and no bound against the 1024-entry array -- OOB-WRITE (build tool, latent: the in-tree ppc_spr.h tops out at 0x3ff)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** bounded input from ppc_spr.h makes the OOB impossible

### ROW `srecbytecount` -- state `open`, severity `LOW`; PROPOSED: **DROP**

**title:** src/file/file_srec.c:56,177,202 -- the int byte counter can overflow after more than 2 GiB of S-record data; the value is only printed -- WRONG-RESULT (loaded file, impractical)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** benign overflow only affecting a debug print for impossibly large files

### ROW `ppcifetchdeclineprod` -- state `open`, severity `LOW`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** src/cpus/cpu_ppc_instr.c X(to_be_translated), arm (d) and the checkstop fallback (#582) -- no measured machine produces a device declining an instruction-width read while running, so the machine check (MSR[ME] set) and the checkstop (clear) ship unmeasured; the design rulings' ROW 5 (-E prep -e ibm6050 -X, the vga_gfx window's last word) needs an X11 build with a display

**state_note (head):** Filed 2026-11-05 by #582 as the reconciliation's ROW 5, 'FILED pending X11' in the contract (regress/artifacts/qhslowifetch/adj_20261104/RECON_FABLE.md, ROW 5; the pmppc window sweep det_20261104/window_sweep.out: WINDOW_SWEEP_ARM_D=NOT_REACHED).  The regress review names the cheaper measurement: a window sweep, as det_20261104 did for pmppc, on bebox, prep, macppc and mvmeppc (regress_20261105/REG_MYTHOS_local.md, P2).  Seven of table 12's fourteen green variants sit in these arms.  Fixing `vgagfxwindowend` removes ROW 5's producer.

**hold_question:** (none)

**the triage pass's reason:** fixing vgagfxwindowend removes the producer.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_13: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE13: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
