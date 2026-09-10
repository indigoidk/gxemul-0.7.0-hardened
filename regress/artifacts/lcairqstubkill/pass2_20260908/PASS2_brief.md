# `lcairqstubkill` / `#516` — PASS 2 ON THE REAL DIFF

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**On pass 1 the grok seat found FOUR defects in my brief and one of them nearly shipped a broken
round.** Check the premises, not just the derivations. A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies exist under the
project root; they are not this fork. Line numbers off by hundreds mean you are in one of them.

**Where I state an ARITHMETIC or COUNT claim, ENUMERATE it** rather than reasoning about it.

**VERDICT LINE FIRST.**

## §C0 — has this round shipped?  Re-run IMMEDIATELY before firing, not while drafting.

```
git log -1 --oneline -- src/devices/dev_lca.c
  b4d4177  #515 lcaconfbus1kill: ...        (a DIFFERENT handler in the same file)

grep -c lcairqstubkill CHANGELOG.md
  1   -- and it is a SCOPE NOTE inside #515's "what this round does NOT close" block,
       introduced by b4d4177 itself.  No round has shipped for this row.
```

*On pass 1 I wrote "0" here. It was true when I formed it and false when I quoted it, because my own
commit landed in between — grok caught it. **A §C0 result has a shelf life measured in commits.***

## §C — WHAT PASS 1 SETTLED (do not re-derive; challenge only if you disagree)

**P4 — ALPHA HAS NO INTERRUPT DELIVERY. CONFIRMED by a seat that tried to refute it.**
`cd.alpha.irq_asserted` is written at `cpu_alpha.c:218`/`:223` and read nowhere; `cpu_dyntrans.c`
dispatches for ARM (`:208`), M88K (`:212`, `:382`) and PPC (`:243`) only. grok: *"Yes. I tried to
refute it and failed. Delivery does not exist."*

**Forwarding is not available at these call sites at all.** `interrupt->extra` is a
`struct lca_data *`, not a `struct cpu *`. Forwarding would be `INTERRUPT_CONNECT` +
`INTERRUPT_ASSERT` — chipset wiring, not a field store.

**Neither witness reaches `_deassert`.** `isa_interrupt_common` takes ONE EDGE per call; the 8042
probe never reads the `0x55` reply, and the UART probe leaves IER on and free-runs, so the aggregate
never falls back to zero. **The deassert latch is therefore UNWITNESSED and that is disclosed in the
probe.**

**The witness term stays `probe:`.** `detector:` is for a fix with no guest-path witness; this row
has two rung-3 probes. Unobservable *delivery* is a contract fact, not a missing witness.

## §D — THE MEASUREMENT, one instrument both directions

```
                              PRE-FIX   POST-FIX
lca_irqstub_probe.py           3/6        6/6
lca_irqstub_uart_probe.py      2/5        5/5
```

Scratch clone `/tmp/gxlca`, baseline = `git show HEAD:src/devices/dev_lca.c` rebuilt in the clone.
No project tree was mutated.

**THREE ROWS WERE ADDED because both probes' own contracts demanded them** — `lca_irqstub_probe.py`
says in its header: *"it is NOT a detector of a repair: 'host survives' would green for a silent
return, for a latched announce, and for an actual interrupt implementation alike. A fix round owes a
row that discriminates those."*

* `irq announce` — the announce text is present. A silent return prints nothing; a real
  implementation would print nothing either. Only this repair prints this.
* `irq honest` — the announce contains *"Alpha has no"*. The round's whole claim is that it stops the
  host dying **without** making interrupts work, and this diagnostic is the only place a reader
  learns that.
* `irq latched` — **counts** the announce in the free-running UART session, want exactly `1`. That
  session's tick re-asserts repeatedly, so an unlatched announce prints many times. Counting is the
  oracle because a presence row would be satisfied by a latch that never engages.

*** A DEFECT I INTRODUCED AND CAUGHT, disclosed because it changes how you should read the numbers
above. *** Adding those rows BELOW each probe's score computation split both scorers — numerator
over the old row set, denominator evaluated at print time. The 8042 probe printed **six rows all
`ok` under a summary of 4/6**. Repaired by moving the computation adjacent to the print. **A census
over HEAD shows 0 of 73 candidate probes were ever split — I created both instances.** The figures
above are from the repaired scorers.

## §E — THE DIFF UNDER REVIEW

```diff
diff --git a/src/devices/dev_lca.c b/src/devices/dev_lca.c
index 97c2e6b..98355d5 100644
--- a/src/devices/dev_lca.c
+++ b/src/devices/dev_lca.c
@@ -48,9 +48,16 @@
 #define	LCA_ISA_MEMBASE	(LCA_PCI_SIO + 0x18000000)
 
 
+/*  #516: warn-once latch bits, one per stub.  PER-INSTANCE, reached through
+    `interrupt->extra' -- see the comment on lca_interrupt_assert().  */
+#define	LCA_W_IRQ_ASSERT	0	/*  #516  */
+#define	LCA_W_IRQ_DEASSERT	1	/*  #516  */
+
 struct lca_data {
 	struct pci_data		*pci_data;
 
+	unsigned int		warned;		/*  #516  */
+
 	uint64_t		ioc_conf;
 	uint64_t		tlb_enable;
 	uint64_t		window_base_0;
@@ -69,8 +76,38 @@ struct lca_data {
  */
 void lca_interrupt_assert(struct interrupt *interrupt)
 {
-	fatal("lca_interrupt_assert: TODO\n");
-	exit(1);
+	struct lca_data *d = (struct lca_data *) interrupt->extra;	/*  #516  */
+
+	/*  #516: this was `fatal(); exit(1)' with NO GUARD -- not a refused value,
+	    an unimplemented path -- and DEVINIT below installs it as the ISA
+	    interrupt callback that `bus_isa_init' wires to BUS_ISA_IDE0|IDE1.  So an
+	    ordinary ISA interrupt ended the host, needing no unusual value anywhere.
+	    MEASURED on two independent guest paths: one store to the 8042 command
+	    port (regress/lca_irqstub_probe.py, 3/4) and three byte stores to the
+	    ns16550 on IRQ 4 (regress/lca_irqstub_uart_probe.py, 2/4).
+
+	    *** THE STUB IS NOT REPLACED BY A FORWARD, BECAUSE A FORWARD WOULD BE A
+	    NO-OP.  ALPHA HAS NO INTERRUPT DELIVERY AT ALL. ***  `cd.alpha.irq_asserted'
+	    is written by `cpu_alpha.c' and read NOWHERE: `cpu_dyntrans.c' turns a
+	    pending interrupt into a delivered one for ARM, M88K and PPC only, and
+	    Alpha is absent from that list.  Calling `cpu_interrupt()' here would set
+	    a field nothing consumes.  Implementing delivery is a SUBSYSTEM -- the
+	    dyntrans dispatch, the PALcode entry and the IPL check -- and is its own
+	    round, not this one.
+
+	    So the disposition is DECLINE plus a bounded announce, and what it buys is
+	    stated narrowly on purpose: THE HOST STOPS DYING.  Interrupts do not start
+	    working; they were never delivered on this architecture and still are not.
+
+	    The latch is PER-INSTANCE (`interrupt->extra'), not function-static: a
+	    function-static bit would let one guest access to one device instance
+	    silence the diagnostic for every other instance, which is a class already
+	    filed against this tree.  */
+	if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {	/*  #516  */
+		d->warned |= 1u << LCA_W_IRQ_ASSERT;
+		fatal("[ lca: ISA interrupt assert not implemented (Alpha has no "
+		    "interrupt delivery); ignored  (once) ]\n");
+	}
 }
 
 
@@ -81,8 +118,17 @@ void lca_interrupt_assert(struct interrupt *interrupt)
  */
 void lca_interrupt_deassert(struct interrupt *interrupt)
 {
-	fatal("lca_interrupt_deassert: TODO\n");
-	exit(1);
+	struct lca_data *d = (struct lca_data *) interrupt->extra;	/*  #516  */
+
+	/*  #516: the sibling of lca_interrupt_assert() above, same reasoning.  A
+	    SEPARATE latch bit, so the two are distinguishable: a driver normally
+	    reaches both within one interrupt cycle, and one shared bit would report
+	    whichever arrived first and hide the other entirely.  */
+	if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {	/*  #516  */
+		d->warned |= 1u << LCA_W_IRQ_DEASSERT;
+		fatal("[ lca: ISA interrupt deassert not implemented (Alpha has no "
+		    "interrupt delivery); ignored  (once) ]\n");
+	}
 }
 
 
```

## §E2 — THE TWO FUNCTIONS IN FULL, POST-FIX

```c
void lca_interrupt_assert(struct interrupt *interrupt)
{
	struct lca_data *d = (struct lca_data *) interrupt->extra;	/*  #516  */

	/*  #516: this was `fatal(); exit(1)' with NO GUARD -- not a refused value,
	    an unimplemented path -- and DEVINIT below installs it as the ISA
	    interrupt callback that `bus_isa_init' wires to BUS_ISA_IDE0|IDE1.  So an
	    ordinary ISA interrupt ended the host, needing no unusual value anywhere.
	    MEASURED on two independent guest paths: one store to the 8042 command
	    port (regress/lca_irqstub_probe.py, 3/4) and three byte stores to the
	    ns16550 on IRQ 4 (regress/lca_irqstub_uart_probe.py, 2/4).

	    *** THE STUB IS NOT REPLACED BY A FORWARD, BECAUSE A FORWARD WOULD BE A
	    NO-OP.  ALPHA HAS NO INTERRUPT DELIVERY AT ALL. ***  `cd.alpha.irq_asserted'
	    is written by `cpu_alpha.c' and read NOWHERE: `cpu_dyntrans.c' turns a
	    pending interrupt into a delivered one for ARM, M88K and PPC only, and
	    Alpha is absent from that list.  Calling `cpu_interrupt()' here would set
	    a field nothing consumes.  Implementing delivery is a SUBSYSTEM -- the
	    dyntrans dispatch, the PALcode entry and the IPL check -- and is its own
	    round, not this one.

	    So the disposition is DECLINE plus a bounded announce, and what it buys is
	    stated narrowly on purpose: THE HOST STOPS DYING.  Interrupts do not start
	    working; they were never delivered on this architecture and still are not.

	    The latch is PER-INSTANCE (`interrupt->extra'), not function-static: a
	    function-static bit would let one guest access to one device instance
	    silence the diagnostic for every other instance, which is a class already
	    filed against this tree.  */
	if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {	/*  #516  */
		d->warned |= 1u << LCA_W_IRQ_ASSERT;
		fatal("[ lca: ISA interrupt assert not implemented (Alpha has no "
		    "interrupt delivery); ignored  (once) ]\n");
	}
}
void lca_interrupt_deassert(struct interrupt *interrupt)
{
	struct lca_data *d = (struct lca_data *) interrupt->extra;	/*  #516  */

	/*  #516: the sibling of lca_interrupt_assert() above, same reasoning.  A
	    SEPARATE latch bit, so the two are distinguishable: a driver normally
	    reaches both within one interrupt cycle, and one shared bit would report
	    whichever arrived first and hide the other entirely.  */
	if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {	/*  #516  */
		d->warned |= 1u << LCA_W_IRQ_DEASSERT;
		fatal("[ lca: ISA interrupt deassert not implemented (Alpha has no "
		    "interrupt delivery); ignored  (once) ]\n");
	}
}
```

## §G — THE QUESTIONS

**Q1 — THE DE-ESCALATION CLAUSE. What accept rows does this diff owe?** It deletes `exit(` from a
device, so every predicate that used to gate death owes a row pinning its accept side. **But there
was NO guard** — the stubs were unconditional — so the "predicates that gated death" enumeration is
the EMPTY SET. The fix *adds* two predicates: `d != NULL` and `!(d->warned & (1u << BIT))`.
**Is the accept side of each rowed?** I believe `irq announce` pins the second (first call
announces) and `irq latched` pins its complement (second call does not). **`d != NULL` is rowed by
nothing.** Is that a floor breach or clause-(e) debt? I lean debt — `extra` is set unconditionally
in `DEVINIT` and no path can reach these callbacks with it NULL — but I want that challenged.

**Q2 — WHAT IS THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES ALL 11 ROWS?** Name it as a
property or an edit, whichever you prefer. Candidates I have deliberately not explored, offered so
you can dismiss or exploit them: the latch bit numbers (`0` and `1`) are not pinned by any row; the
two callbacks could be made to share one bit; `d->warned` is `unsigned int` and the shift could
exceed its width if bits were added carelessly later.

**Q3 — IS THE ANNOUNCE TEXT ITSELF A LIABILITY?** `lca_irqstub_uart_probe.py` has a shipped row
`stub named` wanting the literal `lca_interrupt_assert` ABSENT from the output. My message says
*"ISA interrupt assert"*, so it passes — **measured, not read**. But I satisfied that constraint by
accident, not by design. **Should the constraint be written into the probe or the source so the next
edit cannot violate it?**

**Q4 — THE DEASSERT PATH IS UNWITNESSED AND I AM SHIPPING ANYWAY.** No row exercises
`lca_interrupt_deassert`, so its latch bit and its whole body are uncovered; a mutant of them could
not be killed. It is disclosed in the probe under clause (e). **Is shipping with a wholly unwitnessed
second function acceptable here, or does the round owe a session that lowers the interrupt first?**
Note what closing it costs: a guest sequence that drives IRR back to zero, which neither existing
witness does and which is a new session, not a new row.

**Q5 — DOES THE RECORD OVERCLAIM?** The fix buys *the host stops dying*. It does NOT buy *interrupts
work* — they were never delivered on this architecture and still are not. **Read the diff's comments
and the row notes and tell me whether any of it could be read as the latter.** I would rather be told
the wording is loose than discover it in a CHANGELOG six weeks from now.
