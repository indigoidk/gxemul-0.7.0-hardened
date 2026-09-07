# DESIGN — `gdromcondavail`: `COND_DATA_AVAIL` stays set after the buffer is exhausted

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Today five separate counts of mine were wrong, each
because a key or a domain went unstated, and **you found two of them**. A sibling row's title claimed
"TEN live width kills" when the fix had removed all ten. **Assume something below is stale or
overstated and find it.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies sit under the
project root and are NOT this fork.

**SCOPE:** `GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c`, `GXEMUL-SEC/regress/gdrom_*.py`.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES, each read from the source today

**S1 — THE GUEST CONTROLS `d->cnt` DIRECTLY**, one byte at a time:

```c
	:1194	d->cnt = (d->cnt & 0xff00) | (idata & 0xff);
	:1202	d->cnt = (d->cnt & 0x00ff) | ((idata & 0xff) << 8);
```

**S2 — AVAILABILITY IS CLEARED ONLY WHEN THE COUNT EXHAUSTS**, in the normal read path:

```c
	:1073	if (d->cur_data_offset < d->data_len) {
	:1074		odata  =  d->data[d->cur_data_offset ++];
	:1075		odata |= (d->data[d->cur_data_offset ++] << 8);
	:1076		d->cur_cnt += sizeof(uint16_t);
	:1077		if (d->cur_cnt >= d->cnt) {
	:1078			if (d->cur_data_offset >= d->data_len) {
	:1079				d->cond &= ~COND_DATA_AVAIL;
	:1080			} else {
	:1081				d->cnt = d->data_len - d->cur_data_offset;
	:1082				d->cur_cnt = 0;
	:1083			}
	:1085			SYSASIC_TRIGGER_EVENT(SYSASIC_EVENT_GDROM);
			}
		} else {
	:1094		if (!(d->warned & GDROM_W_OVERREAD)) { ... "(once)" ... }
	:1101		odata = 0xffff;
	:1102		break;
		}
```

**S3 — THE INCONSISTENT STATE, and it is reachable by S1 alone.** Raise `cnt` after data is armed and
`cur_cnt >= d->cnt` never becomes true, so `:1079` never runs. The buffer still exhausts, and reads
fall to the `:1087` else-arm, which returns `0xffff` **and does not touch `d->cond`**. So the guest
reads status, sees `COND_DATA_AVAIL`, reads data, gets `0xffff`, and repeats — with the diagnostic
**latched after the first occurrence**.

**S4 — THE QUALIFICATION, which corrects this row's own title.** The row says availability
*"permanently lies"*. It does not: **ordinary exhaustion does clear it**, and another command can
recover the state. The persistent lie is confined to *repeated reads after entering the inconsistent
state*.

**S5 — THE STIMULUS ALREADY EXISTS AND THE ORACLE DOES NOT.** `regress/gdrom_data_probe.py:374`
(anchors `overread`, `overread x1`) already drives exactly this disagreement — **but it checks
SURVIVAL and DIAGNOSTIC COUNT, never the subsequent `COND` state.** A row whose stimulus reaches the
defect and whose oracle cannot see it is this project's named "channel" failure.

**S6 — THE `:1087` ARM IS DELIBERATE, NOT AN OVERSIGHT.** Its comment records `#460` joining it to the
`:1052` guard on the merits: *"this and the COND_DATA_AVAIL site above are ONE predicate family, 'read
when there is nothing to give'."* **So any change here touches a decision a previous round argued
explicitly**, and the `0xffff` value is also documented as non-self-identifying (the TOC is
`memset(0xff)`), which is why the diagnostic rather than the value is the truthfulness channel.

---

## The questions

**Q1 — SHOULD THE `:1087` ARM CLEAR `COND_DATA_AVAIL`?** That is the obvious repair and I want it
attacked. **What legitimate flow, if any, relies on availability surviving an over-read?** Note `:1081`
re-arms `cnt` mid-transfer, so the device does have a state where more data is coming; check whether
clearing at `:1087` can strand it.

**Q2 — OR IS THE REAL DEFECT AT `:1077`?** The condition couples two independent quantities — a
guest-writable count and a device-owned buffer extent. An alternative repair clears availability
whenever `cur_data_offset >= d->data_len`, **regardless of the count**. **Which is right, and which
does the hardware do?** If the source cannot settle it, say so plainly.

**Q3 — THE ORACLE.** Given S5, what row observes the COND state after the inconsistent read? It must
distinguish *availability correctly cleared* from *availability never set* and from *the device
recovering via another command*. **Name the register read and the expected values.**

**Q4 — THE SMALLEST EDIT that breaks the fix and still passes. Name the row you expect to stay
green.** I am after the clause-(d) family — a repair conditioned on a field the guarded body reads.
`d->cnt`, `d->cur_cnt`, `d->cur_data_offset` and `d->data_len` are all in scope, and a neighbouring
round in this same file was swept clean three times by that shape.

**Q5 — IS THERE A MIRROR STATE?** S3 raises `cnt`. **What does LOWERING it do** — can a guest make
`cur_cnt >= d->cnt` true immediately and clear availability while data remains, i.e. the opposite
inconsistency? If so, is that a second defect or the same one?

## What I am not asking

Do not write a patch or a probe, and do not run builds, gates or probes. **Nothing ships until the
flagship adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
