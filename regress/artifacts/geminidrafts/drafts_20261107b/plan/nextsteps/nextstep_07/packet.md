# Reading task: nextstep_07 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBNEXT07-2f89` on a line of its own.

# GXemul hardened fork -- THE NEXT STEP for 1 filed issues that must NOT be closed yet (a defensive project's queue work)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier pass found that each row below still names work owed, so it stays open.  You cannot
read files; work from the text.  Ledger at HEAD 8d9df658.  Proposals only.

## The rows

### ROW `ppcifetchdeclineprod` -- state `open`, severity `LOW`

**title:** src/cpus/cpu_ppc_instr.c X(to_be_translated), arm (d) and the checkstop fallback (#582) -- no measured machine produces a device declining an instruction-width read while running, so the machine check (MSR[ME] set) and the checkstop (clear) ship unmeasured; the design rulings' ROW 5 (-E prep -e ibm6050 -X, the vga_gfx window's last word) needs an X11 build with a display

**state_note:** Filed 2026-11-05 by #582 as the reconciliation's ROW 5, 'FILED pending X11' in the contract (regress/artifacts/qhslowifetch/adj_20261104/RECON_FABLE.md, ROW 5; the pmppc window sweep det_20261104/window_sweep.out: WINDOW_SWEEP_ARM_D=NOT_REACHED).  The regress review names the cheaper measurement: a window sweep, as det_20261104 did for pmppc, on bebox, prep, macppc and mvmeppc (regress_20261105/REG_MYTHOS_local.md, P2).  Seven of table 12's fourteen green variants sit in these arms.  Fixing `vgagfxwindowend` removes ROW 5's producer.

**hold_question:** (none)

## For EACH row (a numbered block, its id first)

1. The ONE concrete next step that would resolve it, as exactly one of: FIX-ROUND (a code change, with its site),
   MEASUREMENT (what to run and what result settles it), READING (a question a careful reading of named code or a manual
   answers), RECORD (a correction or closure note), OWNER-DECISION (the question, phrased so it can be answered).
2. If it is a READING or a RECORD that the text above already settles, DRAFT it now (two to six lines).  Otherwise say
   what the step needs that is not in the text.
3. Whether it can be COMBINED with another row in this packet (same device, same next step).
Do not invent measurements, commits or file contents.

End with one line: `NEXTSTEP_07: <f> FIX-ROUND, <m> MEASUREMENT, <r> READING, <c> RECORD, <o> OWNER-DECISION`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBNEXT07: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
