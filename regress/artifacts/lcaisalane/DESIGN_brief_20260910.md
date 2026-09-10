# lcaisalane -- FIX DESIGN: three defects in the eleven-line ISA lane handler, and the last executable exit(1) in dev_lca.c

Please do not simply ratify. Check the premises, not just the derivations. Prose only -- no patch to apply,
though you may SKETCH an edit against the full function inlined below, which is why it is inlined. VERDICT
LINE FIRST. Ordinary bounds-correctness engineering on a bus-bridge byte-lane handler.

## THE TREE
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`. Ignore any other `src/` under the project root. Read
`src/devices/dev_lca.c` (working tree; the `#518` diff is uncommitted and touches only `lca_ioc`), and your
own earlier assessment at `regress/artifacts/lcaisalane/codex_assess_20260908.txt` (it censused the idiom
across five files, bounded the severities, found the obvious one-character fix makes things WORSE, and noted
a double-count with lcabadval -- that exit is now ASSIGNED to this row).

## SETTLED
S1. THE ROW: `DEVICE_ACCESS(lca_isa)` -- an off-by-one guard (`ofs > len`, where `ofs == len` is accepted)
    that lets a bus-hitting read return all zeros; the downstream `memory_rw` result discarded; and an
    uninitialised byte consumed on that failure. The `ofs > len` branch is a `fatal()` + `exit(1)` -- the last
    executable process exit in this file after `#516` and `#518`.
S2. The 2026-09-09 adjudication assigned the `ofs > len` exit to THIS row (it had been double-counted with
    lcabadval). The option set for an exit is: 1 delete, 2 silent decline, 3 decline + latched announce,
    4 accept, 5 fault (NOT available on Alpha: memory_rw dispatches a failed-device exception only for MIPS
    and M88K), 6 backed accept, 7 implement.
S3. Accesses arrive through `memory_rw` with `len` in {1,2,4,8} and `relative_addr` any byte offset inside
    the ISA window; `ofs = relative_addr & 3`.

## THE FULL ENCLOSING FUNCTION (verbatim from the working tree)
```c
DEVICE_ACCESS(lca_isa)
{
	unsigned int ofs, i;
	uint8_t byte;

	relative_addr >>= 5;

	ofs = relative_addr & 3;
	if (ofs > len) {
		fatal("[ ofs=%i len=%i in lca_isa access function. "
		    "aborting ]\n", ofs, len);
		exit(1);
	}

	if (writeflag == MEM_WRITE) {
		byte = data[ofs % len];
		return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
		    relative_addr, &byte, 1, writeflag, CACHE_NONE);
	}

	cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
	    &byte, 1, MEM_READ, CACHE_NONE);

	for (i=0; i<len; i++)
		data[i] = i == ofs? byte : 0x00;

	return 1;
}
```

## THE QUESTIONS
Q1. PREMISES AS QUESTIONS: enumerate every (len, ofs) pair `memory_rw` can deliver here (is the CPU's
    alignment gate upstream, so a width-w access arrives w-aligned? -- the carrier records that such a gate
    changed an 8201-cell enumeration to 6144 once). For each pair: accepted or refused today, what byte is
    selected, and what the guest observes.
Q2. THE FIX, per defect: (a) the guard -- which predicate is the correct one, and what should the refused
    case DO (member, from S2)? (b) the discarded `memory_rw` result -- what should a failed downstream access
    return to the caller, and is `return 0` a decline or a fault on this CPU? (c) the uninitialised byte --
    initialise, or restructure so it is never read?  Sketch each against the function above and check the
    common tail.
Q3. THE SMALLEST EDIT THAT BREAKS EACH FIX AND STILL LOOKS RIGHT, and the row that would catch it.
Q4. WITNESS: which guest access (machine `alphabook1`, an ISA device at a known offset -- the 8042 at
    ISA 0x60/0x64 and the ns16550 at 0x3f8 are already used by `regress/lca_irqstub_probe.py`) shows the
    zero-return defect on the committed build, and what would a rung-3 row assert?
State what you read versus what you took from this packet. If you found something ELSE, say so.
