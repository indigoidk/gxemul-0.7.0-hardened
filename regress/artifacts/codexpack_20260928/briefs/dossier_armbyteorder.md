DESIGN DOSSIER -- ARM: a control-register write that changes the byte-order bit ends the process

Open your answer with the token `CODEXPACK_DOSSIER_ARMBYTEORDER_ALIVE`.  Second line: the VERDICT line specified at the end.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git): a hardened fork of the GXemul 0.7.0 full-system machine emulator, in C99.  Read
COMMITTED files only, at commit `db8b1a33`: `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:<path>` (number the lines with
`awk '{print NR": "$0}'` or use `grep -n`).  The WORKING TREE carries other people's uncommitted work -- do not read
source files from disk.  Ignore every other `src/` under the project root (`src/`, `est/`, `build/`, `build-asan/`,
`_archive/` are other copies; a copy reports line numbers off by hundreds).

**Reading scope.**  `src/`, `regress/*.py`, `regress/*.sh`, `regress/*.c`, `OUTSTANDING_BUGS.md` and `CHANGELOG.md`
(all at `db8b1a33`), the hardware manuals `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\*.txt` (on disk), and the files this
brief names by path.  Do not read anything else under `regress/artifacts/`, and not `tools/pipeline/ledger.json`.

**This is a reading task.**  Build nothing, run nothing, write nothing.  Do not write programs or patches: describe
behaviour and cite lines.  Cite `path:line` at `db8b1a33` for every claim and quote the line when the claim rests on its
exact text.  Say "not checked" rather than guessing.  Where a claim is ARITHMETIC (an offset, an index range, a count)
enumerate the values rather than reasoning about them.

## The finding under study

A write to CP15 c1 (opcode2 0) stores the guest's value into `cpu->cd.arm.control`
(`src/cpus/cpu_arm_coproc.c`, the `Write to control` block); when its `ARM_CONTROL_BIG` bit differs from the byte
order the machine was configured with, the handler calls `fatal()` + `exit(1)` ("Trying to switch endianness").  A
comment from round #378 says the exit is load-bearing for byte-order decisions made at translation time (the
LDM/STM fast-path install gate reads `cpu->byte_order` once).  Graded HIGH.  Include in item 2 whether a
user-mode guest can execute the `mcr` at all (find where CP15 access is dispatched and what it checks).

## What is wanted: a DESIGN DOSSIER for the correction round.  Nothing is changed by this job.

1. **TRUE OR FALSE.**  Is the finding true of the source at `db8b1a33`?  Walk the path line by line from the point where
   guest-supplied data enters (the instruction word, the register write, the DMA descriptor) to the terminating call or
   the CPU stop, naming every condition on the way.  Quote the lines.
2. **WHO CAN REACH IT.**  From which guest privilege level; which CPU models and which machine types in `src/machines/`
   instantiate the code (grep for the CPU type or the device name); whether any configuration makes it unreachable.
3. **WHAT THE HARDWARE DOES.**  Quote the manual (file and line in `_scratchpad\*.txt`) for the behaviour the
   architecture specifies in this case.  If no manual on disk covers it, say so -- do not cite from memory.
4. **SIBLINGS.**  Every other site in the same file(s) with the same shape -- a terminating call, or a CPU stop
   (`cpu->running = 0`), behind a condition guest input can control -- each with its line, its condition, and whether
   `OUTSTANDING_BUGS.md` already records it (the id, or the line range of the prose when it has no id).
5. **THE OPTION SET.**  This project's dispositions for an access the model cannot service: (1) delete the terminating
   call; (2) decline silently; (3) decline and announce once per device or CPU (the house latch idiom, a `(once)`
   marker); (4) accept -- the model already computes the right value; (5) fault -- deliver the architecture's
   exception; (6) accept into invented backing store; (7) implement the missing behaviour.  Name the member that fits
   and whether the machinery it needs exists on THIS CPU (option 5 needs the exception delivery to be modelled; say
   where it is).  Cite the nearest precedent in this fork where the same kind of access is already handled without
   ending the process.  Is there a member this list does not name?
6. **WHAT A REGRESSION CHECK WOULD OBSERVE.**  For the behaviour before and after a correction, name the observable
   channels that differ (a register read back, a diagnostic line, execution continuing, an exception vector taken)
   and the ones that do not.  Name the legal neighbouring cases a correction must keep working -- the accesses it
   must not start refusing.
7. **RECORDS.**  Is any comment, CHANGELOG sentence or OUTSTANDING_BUGS entry about this code false at `db8b1a33`?  Quote
   it and give the corrected sentence.

VERDICT line (the second line of your answer): `VERDICT: finding TRUE / FALSE / TRUE WITH CHANGES -- disposition
member <n> -- <one clause>`.  End with the DENOMINATOR: the files and line ranges you read, and what you did not.
