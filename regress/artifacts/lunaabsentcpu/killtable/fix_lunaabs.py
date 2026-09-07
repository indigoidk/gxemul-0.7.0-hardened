import io, os, sys
#  lunaabsentcpu (#503) -- option (a): bound reassert_interrupts()' walk to the slots DEVINIT actually connected.
#  The exact form the Opus measuring seat built and measured on pass 1 (opus_p1_logs/diff_FIXA.diff: witness 6/6,
#  accept 8/8, es438 rows green; the clamp variant measured identical on all 28 rows and is NOT added -- the DEVINIT
#  `ncpus > 4' exit ~70 lines below fires before any walk, and "cannot hurt" is not a warrant).  Applied to ONE tree
#  given on argv[1]; every edit asserts its exact old text once, so a drifted tree fails loudly.
root = sys.argv[1] if len(sys.argv) > 1 else r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
p = os.path.join(root, "src", "devices", "dev_luna88k.c")
s = io.open(p, encoding="utf-8").read()
def edit(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)

edit("struct luna88k_data {\n\tstruct interrupt cpu_irq[MAX_CPUS];\n",
     "struct luna88k_data {\n"
     "\t/*  #503 (lunaabsentcpu): the number of CPUs actually INTERRUPT_CONNECTed at\n"
     "\t    DEVINIT.  Slots at or above this index were never connected, so their\n"
     "\t    cpu_irq[].interrupt_assert/deassert pointers are the memset's NULL.  The\n"
     "\t    walk bound and the connect predicate are the same number on purpose.  */\n"
     "\tint\t\tncpus;\n"
     "\tstruct interrupt cpu_irq[MAX_CPUS];\n")
edit("\tfor (cpu = 0; cpu < MAX_CPUS; cpu++) {\n\t\t// printf(\"cpu%i: status = 0x%08x, enable = 0x%08x\\n\",\n",
     "\tfor (cpu = 0; cpu < d->ncpus; cpu++) {\t\t/*  #503  */\n\t\t// printf(\"cpu%i: status = 0x%08x, enable = 0x%08x\\n\",\n")
edit("\tmemset(d, 0, sizeof(struct luna88k_data));\n\n\t// TODO: Values should correspond to the bootable disk id!\n",
     "\tmemset(d, 0, sizeof(struct luna88k_data));\n\n"
     "\t/*  #503 (lunaabsentcpu): bound reassert_interrupts() to the slots connected\n"
     "\t    below.  It walked all MAX_CPUS and called the NULL interrupt_assert of an\n"
     "\t    unpopulated slot: on the default one-cpu machine a guest store of\n"
     "\t    0xfc000000 to INT_ST_MASK1 followed by a store to SOFT_INT1 (or any device\n"
     "\t    line whose bit that mask enables) killed the emulator with SIGSEGV --\n"
     "\t    measured, regress/luna_absentcpu_probe.py.  The absent slots' MASK/SOFT\n"
     "\t    registers stay guest-writable storage with readback (a board-model\n"
     "\t    question, row lunaabsentmaskdecl); the `ncpus > 4' exit below still\n"
     "\t    bounds this value to the array size.  Pre-existing upstream (the HACK\n"
     "\t    comment's per-count connects and this walk are the 0.7.0 import).  */\n"
     "\td->ncpus = devinit->machine->ncpus;\n\n"
     "\t// TODO: Values should correspond to the bootable disk id!\n")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("lunaabsentcpu (#503) fix applied to", p)
