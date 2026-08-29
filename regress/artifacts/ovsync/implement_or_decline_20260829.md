# `ovsync` — the implement-or-decline question, ANSWERED BY READING.  2026-08-29

**Reading only.  No build, no probe, no edit.  This is a design finding, not a shipped fix.**

The row was narrowed by adjudication on 2026-08-27 to exactly one residual:

> *"b120's fix makes opcode 0x91 an honest CHECK CONDITION.  **It does not implement
> SYNCHRONIZE CACHE(16), so it does not make the flush happen.**  That residual — implement
> 0x91, or formally decline it — is NOT covered by b120 and is what this row should carry."*

## 1. THE DEFECT AT HEAD, CONFIRMED

`SCSICMD_SYNCHRONIZE_CACHE` is **0x35** — the TEN-byte form (`src/include/diskimage.h`).  The
top-level switch in `src/disk/diskimage_scsicmd.c` has **22 case labels** and **0x91 is not
among them**; no constant for it exists anywhere in the tree.

So SYNCHRONIZE CACHE(16) falls to the `default:` arm, which today sets no status and reaches
`return 1`.  **A guest that issues it is told the command succeeded and nothing is flushed** —
a silent durability lie, which is the harm class this row exists for.

## 2. *** THE ANSWER IS **IMPLEMENT**, AND THE READING MAKES IT ALMOST FREE. ***

The whole argument is in what the 0x35 arm actually does:

```c
	case SCSICMD_SYNCHRONIZE_CACHE:
		debug("SYNCHRONIZE_CACHE");

		if (xferp->cmd_len != 10)
			debug(" (weird len=%i)", xferp->cmd_len);

		/*  TODO: actualy care about cmd[]  */
		...
		if (!diskimage_sync(d)) {
			fatal("[ SYNCHRONIZE_CACHE: sync failed on disk id %i ]\n", d->id);
			diskimage__return_check_condition(xferp, d,
			    0x03, 0x0c, 0x00);	/*  MEDIUM ERROR, WRITE ERROR  */
		} else
			diskimage__return_default_status_and_message(xferp, d);
		break;
```

**It IGNORES the CDB.**  `/* TODO: actualy care about cmd[] */` is not decoration — the arm
never reads `cmd[]` at all.  It calls `diskimage_sync(d)`, which flushes the **whole disk**,
and reports the result honestly.

> **THE CDB-LAYOUT DIFFERENCE BETWEEN THE 10- AND 16-BYTE FORMS IS THEREFORE IRRELEVANT.**
> SYNCHRONIZE CACHE(16) carries an 8-byte LBA at offset 2 and a 4-byte count at offset 10,
> against the 10-byte form's 4-byte LBA and 2-byte count.  **Neither is read.**  Both forms
> mean "flush", and this implementation flushes everything for both.
>
> So `case 0x91:` shares the existing body **verbatim** — one added label, plus widening the
> `cmd_len != 10` debug so a legitimate 16 does not print "(weird len)".

## 3. WHY THIS IS A TRANSFERRED WARRANT AND NOT "IT CANNOT HURT"

The addition licence in this project is explicit: additions are licensed by a MEASURED DELTA or
a TRANSFERRED WARRANT, never by "it cannot hurt."

**This is the strongest available form of transferred warrant: the warrant is the 0x35 arm's
own shipped implementation, and the transfer is EXACT rather than analogical**, because the
property being transferred (behaviour does not depend on the CDB) is stated by the code itself.
`#437` already established that `diskimage_sync()` is the correct flush — it fixed an inline
`fsync(fileno(d->f))` that *"flushed no stdio buffer and, with an overlay, synced the one file
the guest's data was NOT in."*

**Implement beats decline on the merits, not on effort:**

| option | what the guest gets | does the flush happen? |
|---|---|---|
| decline (b120u's fix alone) | honest CHECK CONDITION, INVALID COMMAND | **NO** |
| implement | GOOD, or MEDIUM ERROR if the sync fails | **YES** |

Declining is *honest* and still leaves the data unflushed; implementing costs one label and
does what the guest asked.  **b120u's fix is still required** — it is what makes every OTHER
unimplemented opcode honest — but for 0x91 specifically it is the weaker of the two answers.

## 4. WHAT THIS DOES NOT ESTABLISH — the parts that need a round, not a reading

* **Reachability is UNMEASURED.**  I have not shown any in-tree guest issues 0x91.  The row's
  sibling evidence is that OpenBSD's ATA path issues neither 0xE7 nor 0xEA; the SCSI picture is
  a separate question and this reading does not answer it.  **An unreachable opcode is a
  documented-only fix, not a durability fix**, and that distinction decides how the round ranks.
* **`cmd_len` for a 16-byte CDB is unverified.**  The controllers set `cmd_len`; `dev_wdc.c`
  sets 12 or 10 for ATAPI.  Whether any path produces 16 needs checking before the widened
  length test is written.
* **No witness.**  Same ceiling the row already records.

*So the ANSWER to the row's question is settled — implement, with the body shared — while the
RANKING of the resulting round still depends on a reachability measurement nobody has taken.*
