# CORRECTION to §C0 of `PASS1_brief.md` — the count was stale, the answer was not

**Found by the grok seat, mid-panel, before it had finished reading:** *"The CHANGELOG already
mentions this row despite the brief's count of 0."*

**It is right.** Measured:

```
grep -c lcairqstubkill CHANGELOG.md
  1                     <- the brief says 0

grep -n lcairqstubkill CHANGELOG.md
  194:(`lcairqstubkill`, separately witnessed), the `lca_isa` `ofs > len` guard, ...
```

## The substance is unaffected, and that is checked rather than asserted

The single mention sits inside `#515`'s own round block, in its section headed **"Scope, and what
this round does NOT close"** — it is a note saying `lcairqstubkill` remains open, not a round that
shipped for it. §C0 asks *has this round already shipped?* and the answer is still **no**.

## But the number was invalidated by my own commit, between running the check and quoting it

```
git log --oneline -1 -S lcairqstubkill -- CHANGELOG.md
  b4d4177  #515 lcaconfbus1kill: ...
```

`b4d4177` is **this session's own commit, made roughly twenty minutes before the brief was
written.** The count was true when I formed it and false when I quoted it.

> *** A §C0 RESULT HAS A SHELF LIFE MEASURED IN COMMITS, NOT IN HOURS. ***  Re-run it immediately
> before the brief is fired, not while drafting — and especially when the drafting session has
> committed anything in between, which is exactly when a round-scoping brief gets written.

## Why this is worth a file rather than a shrug

I added §C0 to *this* brief **because I had skipped it on the previous one**, where a seat then
spent 84 KB establishing that shipped work had shipped. So the check fired, did its job, and its
output still went stale — by a mechanism the earlier failure did not have. **The lesson is not
"remember to run §C0"; it is that running it is not enough if anything commits afterwards.**

*Recorded here, beside the brief, so a later reader of `PASS1_brief.md` meets the correction at the
same moment as the claim. The seats that answered before this was written saw the wrong number; none
of their conclusions depend on it, and grok's catch is the reason it is known at all.*
