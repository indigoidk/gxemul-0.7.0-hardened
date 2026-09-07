import io, sys
#  Apply ONE named mutant to <tree>/src/devices/dev_luna88k.c (the FIXED #503 source).  Every mutant asserts its find-text
#  exactly once (MUTANT-TEXT-NOT-FOUND is a FAIL, never a silent no-op -- a presence pin on the fix's own lines).
#  Usage: python3 mut_lunaabs.py <tree> <mutant>
tree, mut = sys.argv[1], sys.argv[2]
p = tree + "/src/devices/dev_luna88k.c"
s = io.open(p, encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, ("MUTANT-TEXT-NOT-FOUND", mut, old[:60], n)
    s = s.replace(old, new)
LOOP = "\tfor (cpu = 0; cpu < d->ncpus; cpu++) {\t\t/*  #503  */\n"
LOOP_MAX = "\tfor (cpu = 0; cpu < MAX_CPUS; cpu++) {\t\t/* %s: the pre-#503 walk */\n"
ASSIGN = "\td->ncpus = devinit->machine->ncpus;\n"
ASSERT = "\t\t                INTERRUPT_ASSERT(d->cpu_irq[cpu]);\n"
DEASSERT = "\t\t                INTERRUPT_DEASSERT(d->cpu_irq[cpu]);\n"
MASK_CALL = "\t\t\td->interrupt_enable[cpunr] = idata;\n\t\t\treassert_interrupts(d);\n"
SOFT_CALL = "\t\t\td->software_interrupt_status[cpunr] = 0;\n\t\t}\n\n\t\treassert_interrupts(d);\n\t\tbreak;\n"
if mut == "M_REVERT":            # floor (b): the walk back to MAX_CPUS (the assignment stays, unused)
    rep(LOOP, LOOP_MAX % mut)
elif mut == "M_OFFBY1":          # `<=': one slot past the connected ones
    rep(LOOP, "\tfor (cpu = 0; cpu <= d->ncpus; cpu++) {\t\t/* M_OFFBY1 */\n")
elif mut == "M_NOASSIGN":        # the bound never assigned: 0 after the memset -> the loop never runs (slot 0 never asserts)
    rep(ASSIGN, "\t/* M_NOASSIGN */\n")
elif mut == "M_HARD1":           # clause (d): the bound hardcoded -- every 1-cpu row green; only the -n 2 delivery row sees it
    rep(ASSIGN, "\td->ncpus = 1;\t/* M_HARD1 */\n")
elif mut == "M_SKIP1":           # the walk unbounded but slot 1 skipped: 1-cpu rows green; -n 2 delivery to cpu 1 lost
    rep(LOOP, LOOP_MAX % mut + "\t\tif (cpu == 1) continue;\t/* M_SKIP1 */\n")
elif mut == "M_NULLA":           # an ASSERT-only NULL guard instead of the bound: irqActive[1] is set, the DEASSERT walk dies
    rep(LOOP, LOOP_MAX % mut)
    rep(ASSERT, "\t\t                if (d->cpu_irq[cpu].interrupt_assert)\t/* M_NULLA */\n\t\t                    INTERRUPT_ASSERT(d->cpu_irq[cpu]);\n")
elif mut == "M_NULLAB":          # a BOTH-sided NULL guard instead of the bound: EXPECTED EQUIVALENT on every reachable configuration
    rep(LOOP, LOOP_MAX % mut)
    rep(ASSERT, "\t\t                if (d->cpu_irq[cpu].interrupt_assert)\t/* M_NULLAB */\n\t\t                    INTERRUPT_ASSERT(d->cpu_irq[cpu]);\n")
    rep(DEASSERT, "\t\t                if (d->cpu_irq[cpu].interrupt_deassert)\t/* M_NULLAB */\n\t\t                    INTERRUPT_DEASSERT(d->cpu_irq[cpu]);\n")
elif mut == "M_LATCH":           # decline the absent slot ONCE, then walk it (a latch-then-deliver shape)
    rep(LOOP, LOOP_MAX % mut + "\t\tif (cpu >= d->ncpus) { static int latched; if (!latched) { latched = 1; continue; } }\t/* M_LATCH */\n")
elif mut == "M_GUARDASSERT":     # the bound applied to the ASSERT call only (inside the branch); the DEASSERT walk still reaches NULL
    rep(LOOP, LOOP_MAX % mut)
    rep(ASSERT, "\t\t                if (cpu < d->ncpus)\t/* M_GUARDASSERT */\n\t\t                    INTERRUPT_ASSERT(d->cpu_irq[cpu]);\n")
elif mut == "M_CALLGUARD":       # the Fable-F4 alternative: bound the reassert CALL in the two store arms, walk untouched
    rep(LOOP, LOOP_MAX % mut)
    rep(MASK_CALL, "\t\t\td->interrupt_enable[cpunr] = idata;\n\t\t\tif (cpunr < d->ncpus)\t/* M_CALLGUARD */\n\t\t\t\treassert_interrupts(d);\n")
    rep(SOFT_CALL, "\t\t\td->software_interrupt_status[cpunr] = 0;\n\t\t}\n\n\t\tif (cpunr < d->ncpus)\t/* M_CALLGUARD */\n\t\t\treassert_interrupts(d);\n\t\tbreak;\n")
elif mut == "M_MASK30":          # pass 2 (deepseek): the walk ignores SIO line 5 -- a body-read field narrowed; no v2 row proved a DEVICE line delivers to a CONNECTED slot
    rep("\t\tuint32_t status = d->interrupt_status;\n", "\t\tuint32_t status = d->interrupt_status & ~(1 << 30);\t/* M_MASK30 */\n")
elif mut == "M_SWONLY":          # pass 2 (grok, ask-again): walk only the slots with a software interrupt pending -- device lines never deliver
    rep(LOOP, LOOP + "\t\tif (!d->software_interrupt_status[cpu]) continue;\t/* M_SWONLY */\n")
elif mut == "M_AND1":            # pass 2 (glm): slots 2 and 3 alias onto 0 and 1 -- invisible while every session runs ncpus in {1, 2}
    rep(ASSERT, ASSERT.replace("cpu_irq[cpu]", "cpu_irq[cpu & 1]"))
    rep(DEASSERT, DEASSERT.replace("cpu_irq[cpu]", "cpu_irq[cpu & 1]"))
elif mut == "M_MIN2":            # pass 2 (grok): the bound clamped to two -- same class as M_HARD1 one slot further out; only a -n 3/4 row sees it
    rep(ASSIGN, "\td->ncpus = devinit->machine->ncpus > 2 ? 2 : devinit->machine->ncpus;\t/* M_MIN2 */\n")
elif mut == "M_IRQACTIVE0":      # pass 2 (kimi): the per-slot latch collapsed onto slot 0 -- with two slots pending cpu 1's IPI is dropped
    rep("\t\t\tif (!d->irqActive[cpu])\n", "\t\t\tif (!d->irqActive[0])\t/* M_IRQACTIVE0 */\n")
    rep("\t\t\td->irqActive[cpu] = 1;\n", "\t\t\td->irqActive[0] = 1;\n")
    rep("\t\t\tif (d->irqActive[cpu])\n", "\t\t\tif (d->irqActive[0])\n")
    rep("\t\t\td->irqActive[cpu] = 0;\n", "\t\t\td->irqActive[0] = 0;\n")
elif mut == "M_SWLATCH":         # pass 3 (minimax): the software bit only while the latch is clear -- the second walk deasserts a still-pending IPI
    rep("\t\tif (d->software_interrupt_status[cpu])\n\t\t\tstatus |= (1 << 26);\n",
        "\t\tif (d->software_interrupt_status[cpu] && !d->irqActive[cpu])\t/* M_SWLATCH */\n\t\t\tstatus |= (1 << 26);\n")
elif mut == "M_NODEASSERT":      # pass 3: the connected slot's DEASSERT call dropped (the latch still clears)
    rep(DEASSERT, "\t\t                ;\t/* M_NODEASSERT */\n")
elif mut == "M_NOCLEAR":         # pass 3: the `irqActive[cpu] = 0' clear dropped -- a second IPI never re-asserts
    rep("\t\t\td->irqActive[cpu] = 0;\n", "\t\t\t;\t/* M_NOCLEAR */\n")
elif mut == "M_DEASSERT0":       # pass 3 (deepseek): the deassert side tests slot 0's latch for every slot
    rep("\t\t\tif (d->irqActive[cpu])\n", "\t\t\tif (d->irqActive[0])\t/* M_DEASSERT0 */\n")
elif mut == "M_SKIP2":           # pass 3 (kimi): the walk skips slot 2 -- v3 never pended slot 2, so nothing saw it
    rep(LOOP, LOOP + "\t\tif (cpu == 2) continue;\t/* M_SKIP2 */\n")
elif mut == "M_IRQACTIVEP1":     # pass 3 (kimi): the per-slot latch aliased by parity -- a same-parity pending pair drops one IPI
    rep("\t\t\tif (!d->irqActive[cpu])\n", "\t\t\tif (!d->irqActive[cpu & 1])\t/* M_IRQACTIVEP1 */\n")
    rep("\t\t\td->irqActive[cpu] = 1;\n", "\t\t\td->irqActive[cpu & 1] = 1;\n")
    rep("\t\t\tif (d->irqActive[cpu])\n", "\t\t\tif (d->irqActive[cpu & 1])\n")
    rep("\t\t\td->irqActive[cpu] = 0;\n", "\t\t\td->irqActive[cpu & 1] = 0;\n")
elif mut == "M_NOREASSERT":      # the SOFT arm no longer reasserts (disclosed debt: the clock's own reassert carries delivery)
    rep(SOFT_CALL, "\t\t\td->software_interrupt_status[cpunr] = 0;\n\t\t}\n\n\t\t/* M_NOREASSERT */\n\t\tbreak;\n")
else:
    raise SystemExit("unknown mutant " + mut)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("applied", mut)
