# DESIGN — `sgirandomcolour`: the COLOUR-mode PUT default arm writes four `random()` bytes into guest memory

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** On a panel two hours ago I stated a weakened premise
about `#95` as *settled*; **three of six seats confirmed it and one seat opened the file and refuted
it** — the refutation was right and it reversed the round's blocking question. **Where a claim below
rests on a search, ask what the search would miss.** At least one premise here is probably wrong.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork; a seat reading one reports line numbers off by hundreds
and different arms exist.

**SCOPE:** `GXEMUL-SEC/src/devices/dev_sgi_re.c`, `GXEMUL-SEC/src/devices/crmfbreg.h`,
`GXEMUL-SEC/regress/sgi_re_*.py`.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES, each with how it was derived

**S1 — THE SITE.** `horrible_getputpixel()`'s **colour-mode PUT** switch implements four cases —
`DE_MODE_TYPE_` CI, RGB, RGBA, ABGR — and its `default:` arm assigns `buf[0..3] = random()` and then
lets the common tail write those bytes to the destination. Anchor: `buf[0] = random();`.

**S2 — A DOCUMENTED MODE REACHES IT.** `crmfbreg.h` documents **five** colour types; the fifth is
`DE_MODE_TYPE_YCRCB 0x000000f0`, and `grep -c YCRCB src/devices/dev_sgi_re.c` = **0**. So YCRCB is
handled nowhere and falls to `default:`. *(A prior panel established that the type nibble has
**sixteen** values and only four are implemented, so the reachable set is larger than YCRCB alone —
enumerating by named constants misses the unnamed values.)*

**S3 — THE SIBLING PRECEDENT, and it is in the same function.** `sgirandompixel` (`#498`) fixed the
**GET** side of this same helper, which had `*color = random()`. It chose **DECLINE + LATCHED
ANNOUNCE**: leave `*color` alone so the caller's own `uint32_t color = fg` stands and what lands is at
least deterministic; latch the diagnostic because the helper is per-pixel. Its comment is at the
`default:` arm.

**S4 — WHY THIS IS NOT A COPY OF S3.** The GET arm's decline works because the caller **already owns
an initialised variable**. This arm fills a **local `uint8_t buf[8]`** whose contents are then written
out. *A decline that simply skips the fill writes whatever was on the stack.*

**S5 — THE ADJACENT ROW, and it is live right now.** `sgirebufuninit` is an open row about that exact
buffer: `buf[8]` is declared with no initialiser, and the arms assign fewer bytes than `bufdepth`
transfers. **So S4's question and that row's fix are the same question**, and a decline designed here
without reference to it could ship an uninitialised write in place of a random one.

**S6 — THE OPTION SET this project uses**, and members 4–7 were each found by grepping the tree rather
than by argument: **DELETE · DECLINE (silent) · DECLINE + LATCHED ANNOUNCE · ACCEPT · FAULT · BACKED
ACCEPT · IMPLEMENT.** FAULT is not universally available — it needs the CPU family's exception
delivery. The house latch idiom is **N=1 per device instance with `(once)` in the message text**, not
a counter.

---

## The questions

**Q1 — WHAT SHOULD A DECLINED PUT LEAVE IN `buf`, AND WHO OWNS THAT DECISION?** This is the question
S4 and S5 create and it is the one I most want attacked. Candidates: skip the write entirely (what
does the caller then transfer?); zero the span; leave the destination untouched by returning before
the transfer. **Say what each does to the guest, and whether the answer belongs to this round or to
`sgirebufuninit`.** If these two rounds must be ordered, say which comes first and why.

**Q2 — WHICH MEMBER OF S6, and argue AGAINST decline+latched-announce.** The sibling chose it, and
*"the sibling chose it"* is not a warrant — it is the thing to check. **Grep the fork for the existing
idiom before answering**, including how the file's other unimplemented arms dispose of themselves.

**Q3 — THE WITNESS.** This row has **none**. Before it can be recorded as documented-only, this
project requires that one seat be asked to try a **rung-3 cold-debugger probe**: a real guest
instruction through real address decode on an *unmodified* in-tree machine description, with a
liveness control and a device-signature control. `sgi_re_randompixel_probe.py` is the sibling's, and
it measured non-deterministic destination values on successive runs. **Can the PUT default arm be
driven the same way?** If you conclude it cannot, say so plainly and say what blocks it — that is a
real answer and it changes the round's disposition, not a failure.

**Q4 — THE SMALLEST EDIT that breaks the fix and still passes. Name the row you expect to stay
green.** I am after the clause-(d) family — a repair conditioned on a field the guarded body reads. A
neighbouring round in this same file was swept clean three times by that shape: at a transfer width no
row drove, an addressing mode no row used, and finally the joint cell of the two.

**Q5 — IS S2 ACTUALLY RIGHT?** It rests on `grep -c YCRCB` returning 0 and on reading `crmfbreg.h`.
**A count of a named constant cannot enumerate a class** — that error cost a sibling row a wrong
census this week. **Enumerate the type nibble's reachable values properly** and say whether a guest
can actually present one, or whether the callers constrain the mode field before it arrives.

## What I am not asking

Do not write a patch, and do not run builds, gates or probes. **Nothing ships until the flagship
adjudication on 2026-09-09** — this packet exists to be complete, not to authorise work.

**If, while verifying a claim, you found something ELSE — say so.** The row itself exists because a
seat volunteered a residual it was not asked about.
