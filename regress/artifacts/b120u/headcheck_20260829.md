# `b120u` — the structural claim RE-DERIVED AT HEAD, 2026-08-29

**Reading only.  No build, no probe, no edit.**  The row is `held` ("R8 — the unknown-command
half only") with `witness: none yet ... building the probe needs a build, which the machine
embargo forbids".  This does not lift that.  It re-checks the claim the row rests on, because
an audit is a claim with a shelf life and this row has already lost one mechanism to an L4
correction.

## 1. THE STRUCTURAL CLAIM — CONFIRMED

The row says the `default:` arm is the only one that never calls
`diskimage__return_default_status_and_message()` or `diskimage__return_check_condition()`.
**True at HEAD.**  `src/disk/diskimage_scsicmd.c`, the top-level `default:` arm, in full:

```c
	default:
		debug("[ UNIMPLEMENTED SCSI command 0x%02x, disk id=%i",
		    xferp->cmd[0], id);
		// exit(1);
	}

	debug(" ]\n");

	return 1;
}
```

Counts, with their deriver so they are checkable rather than transcribed:

    grep -cE '^[[:space:]]*case[[:space:]]+[A-Za-z_0-9]+:'   -> 30 case arms
    grep -cE '^[[:space:]]*default:'                         ->  4 default arms
    grep -c '..._default_status_and_message(xferp'           -> 23  CALLS
    grep -c '..._check_condition(xferp'                      ->  3  CALLS

*** THE FIRST DRAFT PRINTED 25 AND 5 -- THE RAW GREPS, WHICH COUNT THE COMMENT HEADER AND
THE DEFINITION AS CALLS.  Corrected 2026-08-29. ***  The row's own "only one of 25" has
the same contamination and is wrong under any unit; the correct denominator is **20
TOP-LEVEL ARMS** (22 labels forming 19 bodies -- MODE_SENSE/10, READ/READ_10 and
WRITE/WRITE_10 share bodies -- plus the default).  My own "~30" counted NESTED labels.

**Three of the four `default:` arms are nested switches** (two tabs: mode_sense length at 578,
and the arms at 683 and 1111).  The row's subject is the ONE at a single tab — the top-level
command switch.  *The row says "the default arm" as though there were one; there are four, and
a future reader grepping for `default:` lands on the wrong one three times out of four.*

## 2. AN `exit(1)` IS ALREADY COMMENTED OUT THERE

`// exit(1);` sits in the arm.  So this site was de-fatalised by someone before the current
campaign, and the row's disposition is NOT the usual four-member de-fatalisation choice —
the kill is already gone.  What remains is purely the missing status.

## 3. *** THE RETURN VALUE IS **NOT** THE DEFECT, AND I NEARLY WROTE THAT IT WAS. ***

The function documents its own contract above the definition, verbatim:

```
 *  Returns:
 *	2 if the command expects data from the DATA_OUT phase,
 *	1 if otherwise ok,
 *	0 on error.
```

The `default:` arm reaches `return 1` — "otherwise ok" — which reads exactly like the row's
title.  **But every return in the function was enumerated before that was stated, and it does
not survive:**

    282, 295, 302, 315, 327   return 0   ALL pre-switch (first case is at 345): setup/arg failures
    892, 1291                 return 2   inside specific DATA_OUT arms
    1388                      return 1   THE SINGLE COMMON TAIL

The `default:` arm contains **no return of its own** — it falls out of the switch to 1388, and
so does every other arm that is not one of the two DATA_OUT cases.  **So `return 1` is shared
and distinguishes nothing.**  *(This said "roughly twenty-eight arms", which was underived; the
honest figure is **20 arms reach 1388** — 19 bodies plus the default.)*

> **CONSEQUENCE FOR ANY FIX: `return 0` in the default arm is a SKETCH, not a fix.**  It would
> add a sixth error-return in a structurally different position from the other five — those are
> all pre-switch setup failures, before any status or data has been staged.

### *** AND THE ADJUDICATION MADE THAT REFUTATION MUCH STRONGER: `return 0` IS NOT MERELY
### STRUCTURALLY WRONG, IT IS A MEASURED BEHAVIOURAL REGRESSION.  2026-08-29, each consumer
### read and re-verified. ***

* **`dev_osiop.c:500-505`** — `res == 0` sets **`d->scripts_running = 0`**.  A guest probing one
  unsupported opcode **kills its own SCRIPTS engine**, and no status phase ever happens.
* **`dev_asc.c:1395-1400`** — `ok == 0` gives `STATE_DISCONNECTED` + `NCRINTR_DIS`: the guest
  sees a target DISCONNECT instead of CHECK CONDITION, so it retries or resets rather than
  issuing REQUEST SENSE.  **This also refutes the row's own state_note, which says asc does not
  test for 0 at all.**
* **`dev_wdc.c:1528-1541`** — the `res == 0` arm sets **no error bit**, and `status_byte()`
  raises `WDCS_ERR` only from `d->error`.  So on wdc, `return 0` is guest-INDISTINGUISHABLE
  from success-with-no-data.

> **`return 0` helps no consumer and harms two.**  That is the form to cite, not my structural
> argument — it is checkable at three named lines.

**THE RIGHT SHAPE** is `diskimage__return_check_condition(xferp, d, 0x05, 0x20, 0x00)` —
ILLEGAL REQUEST / INVALID COMMAND OPERATION CODE — **keeping the fall-through `return 1`**,
because CHECK-CONDITION-then-`return 1` is already this file's refusal idiom at four shipped
sites that all four controllers handle today.  It must NOT allocate `data_in` (the controllers
pick the DATA_IN phase off `data_in != NULL`), and it **also cures `mb89352halt`'s mechanism**,
since `status_len` becomes 1 and the PH_STAT read stops tripping `cpu->running = 0`.

## 4. THE FIVE CONSUMERS ANY FIX MUST BE CHECKED AGAINST

    dev_asc.c:852      res = diskimage_scsicommand(...)
    dev_asc.c:1027     ok  = diskimage_scsicommand(...)
    dev_mb89352.c:268  res = ...
    dev_mb89352.c:276  res = ...
    dev_osiop.c:498    res = ...
    dev_osiop.c:538    res = ...
    dev_wdc.c:1515     res = ...

Four device files, seven call sites.  The row's own note records that an adversarial pass found
**four different wrong outcomes** rather than one — consistent with per-controller handling of
`status == NULL, status_len == 0` alongside a success return.

## 5. WHAT IS AND IS NOT ADVANCED BY THIS

**Advanced:** the structural claim holds at HEAD; the arm is already non-fatal; the return value
is excluded as the defect and as a fix; the consumer set is enumerated.

**NOT advanced:** no witness.  The rung-3 ASK the 2026-08-27 lifecycle ruling requires has
still not been made — one invocation, deferred only because a probe needs a build and a
measurement holds the machine.

### *** AND THE WITNESS CHANNEL I ASSUMED IS THE WRONG ONE — this inverts what I wrote when I
### raised the ATAPI route as making a witness CHEAPER. ***

`dev_wdc.c:1515` does feed ATAPI packet commands into `diskimage_scsicommand()`, and `res == 1`
with no data yields PHASE_COMPLETED and no error bit — so the defect is genuinely reachable
that way.  **But `atapi_st->status` is read NOWHERE in `dev_wdc.c`.**  An ATAPI witness would
therefore stay RED after a dispatcher-only fix, because it witnesses the COMBINED dispatcher +
wdc defect rather than this one.

> **The discriminating channels for THIS fix are `asc` (ICCS fifo byte 0x00 → 0x02, on the
> pmax rig) or `mb89352` (the loudest pre-fix symptom on record: the emulated CPU stops).**
> The wdc consumer repair — consult `atapi_st->status`, drive `d->error` so `WDCS_ERR` appears
> — is its own hunk in a different file and should be filed separately.  The
> one-omission-in-one-shared-function warrant does not stretch to it.

**A SIBLING THIS ROUND DOES NOT TOUCH, filed rather than fixed:** `SPACE`'s NESTED `default:`
`fatal()`s and then falls through to the status helper, **telling the guest GOOD for an
unimplemented SPACE type**.  Same false-success class, but inside a KNOWN arm rather than the
default one, so b120u's fix cannot reach it.

*The counts here were contaminated on first writing and the fix shape was understated; both are
corrected above rather than swapped silently.  The full adjudication is on the ledger row.*
