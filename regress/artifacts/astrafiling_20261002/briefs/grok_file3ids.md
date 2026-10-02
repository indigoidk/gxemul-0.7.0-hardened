THREE ROWS THE FILING TABLE MISSED -- your own rulings named them; check the rows as they will be filed

FIRST line of your answer: `VERDICT: <t> of 3 rows true as titled and rightly graded, <c> need a change`.
SECOND line: the token `GROK_FILE3IDS_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

**Context.**  In the retro review of this project's emulator source you ruled three findings `CONFIRMED-FILED <id>`,
each time noting that the queue (`OUTSTANDING_BUGS.md`) carries the defect in PROSE with no short id and proposing the
id (`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\adjudication\grok_20261002\grok_rule3f.txt`
lines 37-38 and 70-71; `...\grok_rule3g.txt` lines 13-14).  The filing table read "CONFIRMED-FILED" as "nothing to
file", so the three ids exist nowhere: not in `tools/pipeline/ledger.json`, not in the queue file, not in the table.
A mechanical check found them (every id a disposition calls already filed must exist somewhere).  They are now added
as rows of kind "an id for an entry the queue already carries in prose".  A row graded HIGH gets a correction round, so
a false or over-wide title misdirects real work.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`.  Read committed files
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`); if that is refused to you, read from disk and
say so (none of the files named here carries an uncommitted edit).  The queue passages are lines 2727-2732 of
`OUTSTANDING_BUGS.md` at commit `db8b1a33` (unchanged at `7440e129`).  Never read any other `src/` under the project
root; never `git status` or `git diff`.  Write nothing.

**Severity, as the campaign applied it to emulator defects:** HIGH -- guest-controlled input ends the emulator
process, makes one of its memory accesses leave a buffer's bounds, or stops it making progress; MED -- wrong
guest-visible behaviour; LOW -- diagnostics, latent code, records.

**The three rows, as drafted** (id | grade | title):
1. `ramspaninval` | MED | a bulk RAM write invalidates translated code once per memblock fragment, at the fragment's
   first page (`src/cpus/memory_rw.c:760`; the split and recursion at `:762-775`), so translated code in the fragment's
   later pages can go stale; the queue's prose says "only the endpoint pages".
2. `tcpdebugopts` | HIGH | the TCP options dump in `src/net/net_ip.c` (`:420-447`) runs while `i < data_offset` with no
   test against the frame length, so on a short frame it reads past a transmit buffer allocated at exactly the
   transmitted length (`src/devices/dev_dec21143.c:788-809`, `src/devices/dev_le.c:410-439`; `dev_ne2000.c:278` is a
   2048-byte buffer and is not affected) -- CONDITIONAL: the dump runs only while NET debug verbosity is on.
3. `jazzlbmask` | MED | the Jazz local-bus interrupt enable (`LB_IE`, `src/include/thirdparty/pica.h:117`) is not
   implemented: `src/devices/dev_jazz.c` makes no use of it, so the missing mask affects which local interrupts are
   forwarded (the "dual-pending-IRQ loss" half of the queue's sentence is the existing entry OB-22).

I believe -- check each, do not take it from here -- that: (1) your ruling gave `ramspaninval` an independent MED;
(2) your ruling said the exact-sized callers of `tcpdebugopts` are HIGH "by the severity rule's letter" while NET debug
verbosity is on; (3) your ruling gave `jazzlbmask` NO grade, and the MED above is GPT-6 Astra's (its confirmation of
the id-less scan), so it needs yours.

**For each row, ONE line:**
`<id> | TITLE: TRUE / CONDITIONAL: <a condition the title omits> / NOT TRUE: <what the source shows> | GRADE: <HIGH / MED / LOW> -- <one reason> | <the lines you read, path:line>`
Say also who reaches each: a guest action on an in-tree machine (name one), a host option, or neither.

End with `DENOMINATOR: <s> of 3 rows read in the source`.
