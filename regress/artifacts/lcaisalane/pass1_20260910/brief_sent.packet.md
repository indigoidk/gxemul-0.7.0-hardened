# `lcaisalane` -- PASS 1 ON THE DESIGN: the LCA sparse-I/O byte-lane handler ends the host on an ordinary byte access to two documented UART registers and hands the guest a silent zero for a third

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

Ordinary bounds-correctness engineering on a bus-bridge byte-lane handler.  Prose only; you may SKETCH an
edit against the full function inlined below (that is why it is inlined), but nothing here is applied.

## §C0 — HAS THIS ROUND SHIPPED?  NO.
`git log --oneline -3` at sending: `1ce8296` #509 follow-up, `1f2b27a` #512 follow-up, `e73623a` records.
The ledger row is `lcaisalane` (sev high, state open, witness field set to the rung-3 probe below).  The
working tree carries two UNCOMMITTED rounds in OTHER arms of the same file (#518 `lca_ioc`) and in
`dev_sgi_re.c` (#519); neither touches `lca_isa`.  Nothing about this row has shipped.

## §C — SETTLED PREMISES (re-inlined; say which you cannot settle from this packet)
S1. `fatal()` RETURNS (`src/core/debugmsg.c`, grep `void fatal(`: no early-out, no exit), so every `fatal()`
    here is a diagnostic and the process exit is the separate `exit(1)` line.
S2. THE ROW (filed 2026-09-08, assigned the `ofs > len` exit on the 2026-09-09 adjudication after a double
    count with `lcabadval`): `DEVICE_ACCESS(lca_isa)` is the LAST executable process exit in `dev_lca.c`
    once #516 (the two interrupt stubs) and #518 (`lca_ioc`'s six value guards and its default arm) land.
S3. THE OPTION SET for a de-fatalisation, all seven members: 1 delete; 2 silent decline; 3 decline + latched
    announce (the house idiom: N = 1 per device instance, `(once)` in the text); 4 accept; 5 FAULT -- NOT
    AVAILABLE ON ALPHA, `memory_rw.c` dispatches a failed-device exception only for MIPS and M88K; 6 backed
    accept; 7 implement.  Codex's design reading (`regress/artifacts/lcaisalane/codex_design_20260910.txt`)
    recommends member 3 with `ofs >= len`, a `return 0` for BOTH directions on a refused lane, and checking
    the downstream read's result BEFORE the packing loop.  That recommendation is a CANDIDATE here, not a
    ruling.
S4. The emulated Alpha DECODES THE BWX BYTE/WORD LOADS AND STORES WITHOUT ANY CPU-TYPE GATE:
    `src/cpus/cpu_alpha_instr.c`, grep `case 0x0a: loadstore_type = 0; load = 1;` (`ldbu`), `case 0x0c:`
    (`ldwu`), `case 0x0e:` (`stb`).  So a guest instruction reaches this handler with `len == 1` and
    `len == 2` even though a real 21066 has no BWX.  (`regress/lca_irqstub_probe.py` already drives `stb`
    on this machine.)
S5. The handler is registered by `dev_lca.c` (grep `memory_device_register(devinit->machine->memory, "lca_isa"`)
    on `alphabook1` only (`device_add(machine, "lca")` under `ST_ALPHABOOK1`); the access arrives through
    `memory_rw` with `len` in {1, 2, 4, 8} and `relative_addr` any byte offset inside the window.
S6. THE HARDWARE, from the local manual `_scratchpad/21066_66a_hrm.txt` (Alpha 21066/21066A HRM), which is
    where the fork's `>> 5` comes from: S6.2.6 (`:8840`) maps CPU physical address bits <31:7> to PCI
    address bits <26:2>; the byte-enable table is Table 6-3 at `:8857`, and `:8850` says "Physical address
    bits <4:3> also specify transfer size".  Verbatim rows of that table (extracted text; the header is
    staggered by the extractor, the DATA rows are not):

        a<6:5> a<4:3> Size      c_be_l<3:0>   PCI Memory ad<1:0>   PCI I/O ad<1:0>   Type
        00     00     Byte      1110          00                   00                Masked
        01     00     Byte      1011 / 0111   00                   01                Masked
        10     00     Byte                    00                   10                Masked
        11     00     Byte                    00                   11                Masked
        00     01     Word      1100 / 1001   00                   00                Masked
        01     01     Word      0011          00                   01                Masked
        10     01     Word                    00                   10                Masked
        00     10     Tribyte   1000 / 0001   00                   00                Masked
        01     10     Tribyte                 00                   01                Masked

    So on hardware the LANE is a<6:5> (it becomes PCI I/O ad<1:0>) and the SIZE is a<4:3>; the CPU issues
    a LONGWORD or QUADWORD access whatever the size encoded.  THE MODEL: `relative_addr >>= 5` keeps a<6:5>
    as the two low bits of the derived port (so `ofs = port & 3` IS the hardware lane -- the witness probe
    proves the lane is a function of the port, not an independent field), DISCARDS a<4:3> entirely, and uses
    the CPU access width `len` as the size.  That divergence is a premise question below, not a settled fact.

## THE FULL ENCLOSING FUNCTION (verbatim from the working tree; the whole handler, every exit path)
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
`LCA_ISA_BASE` is `(LCA_PCI_SIO + 0x10000000)`.  There is no common tail after the read loop other than
`return 1`; the write arm returns the downstream result directly.

## THE WITNESS (rung 3, Opus measuring seat, `regress/lca_isalane_probe.py`, unmodified `alphabook1`, no
## disk, no OS; `regress/artifacts/lcaisalane/witness_20260910/HEAD_run1.out` and `HEAD_run2.out`, both
## `LCAISALANE_RESULT=13/16`, sentinel `LCAISALANE_DONE`)
Guest LDBU/LDL/STB instructions through the sparse window, with the UART at ISA 0x3f8 (lane = port & 3):
```
port & 3 == 0   ->  ofs 0.  data[0] = byte.                                         CORRECT   (`live': 8042 data 0x55)
port & 3 == 1   ->  ofs 1.  `1 > 1' is FALSE, so ACCEPTED -- and the packing loop
                    `for (i = 0; i < 1; i++) data[i] = (i == 1)? byte : 0' is never
                    true, so THE DEVICE BYTE IS DISCARDED AND THE GUEST IS HANDED ZERO
                    with a success return.  A false success, not a decline.            `ofs1 zero': 0x0, want 0x60 (LSR)
port & 3 == 2   ->  ofs 2.  `2 > 1' -> fatal() + exit(1).                            `ofs2 exit': dead     (MSR 0x3fe)
port & 3 == 3   ->  ofs 3.  `3 > 1' -> fatal() + exit(1).                            `ofs3 exit': dead     (scratch 0x3ff)
```
Controls green on HEAD: `base alive`, `live` (lane 0 returns the keyboard controller's reply), `ofs1 devsig`
and `ofs1 wide` (the SAME LSR read through the flat mapping and through a 32-bit LDL at lane 1 both return
the LSR's fixed bits 0x60 -- so the device answers and RAM would not), `ctl`/`ctl zero` (a lane-0 read of a
port with no device), `ofs2 devsig`/`ofs2 wide`, `ofs3 devsig`/`ofs3 wide` (each register's value through the
other two paths), and the two `attrib` rows (the death is attributed by the handler's own `[ ofs=%i len=%i in
lca_isa access function. aborting ]` text).  Three RED rows, all the defect.

## WHAT CODEX'S DESIGN READING SAID (candidate, not ruling; its verdict line verbatim)
*"VERDICT: Use `ofs >= len` with member 3, and return downstream failure before packing the byte. S3's length
census is incomplete in this tree; the uninitialized-byte claim is conditional."*  Its sketch: keep the decode;
clear the caller's buffer for reads only; reject `ofs >= len` through a per-instance latch and `return 0`;
keep the write arm's immediate downstream return (indexing may become `data[ofs]`); check the downstream READ's
result immediately and `return 0` on failure BEFORE the packing loop; only successful reads reach the loop and
`return 1`.  It also found: both downstream `memory_rw` calls lack `PHYSICAL` though they target registered
physical ISA addresses; the old diagnostic prints `size_t len` with `%i`; changing only `>` to `>=` while
keeping the exit would EXPAND termination to the equality cases (the obvious one-character fix makes it worse).

## §E — THE QUESTIONS (verdict line first; cite by grep anchor, never by line number)
1. **PREMISES AS QUESTIONS.**
   (a) Is the model's lane decode the hardware's?  From Table 6-3, a<6:5> -> PCI I/O ad<1:0>; the model's
       `(relative_addr >> 5) & 3` is a<6:5>.  Confirm or refute by walking one address: a guest LDL at sparse
       offset `(0x3fd << 5)` -- which lane, which port, which PCI ad<1:0>?
   (b) The model DISCARDS a<4:3> (the hardware size) and uses `len`.  For a real 21066 driver -- which has no
       BWX and issues LDL with the size in a<4:3> -- does the model serve a byte read of the LSR correctly
       (LDL, a<6:5> = 01, a<4:3> = 00 -> len 4, ofs 1 -> `data[1] = byte`)?  Which hardware-legal encodings
       does the model serve WRONGLY today (a word at lane 3? a tribyte?), and is any of that THIS round's
       scope or a separate row (my premise: separate -- `lcaisasize`, filed if you agree it is real)?
   (c) Given S4, can a guest binary on the emulated machine issue `ldbu`/`ldwu`/`stb` at all, or is the
       len-1/len-2 path reachable only from the debugger?  My premise: yes, the decoder has no gate, and
       the witness DID issue LDBU from guest code.  If you disagree, say what would stop it.
   (d) What does a DEVICE_ACCESS `return 0` do to the guest on ALPHA?  Codex says the destination register is
       left UNCHANGED (no fault path).  Read `src/cpus/memory_rw.c` around the device dispatch (grep
       `mem->devices[i].f(`) and the Alpha load template (`cpu_alpha_instr_loadstore.c`): what value, if
       any, lands in the register, and does the CPU keep running?  This decides whether "decline" is even
       observable to a guest and therefore what the detector's channel is.
   (e) The `#i` cases: for `len == 2` and `ofs == 3`, the write arm today does `data[3 % 2] = data[1]` -- is
       that the tribyte/word lane semantics or nonsense?  After `>=` it is declined.  Enumerate every
       (len, ofs) cell -- len in {1,2,4,8}, ofs in {0,1,2,3} -- and label each: served correctly today /
       false success today / exit today / declined after the candidate / still served after the candidate.
       That table IS the (d) DEPENDS-ON enumeration for the detector; a cell you cannot label is a premise
       I have not settled.
2. **THE SMALLEST EDIT that breaks the candidate fix and still passes the rows you would expect** -- name the
   row you expect to stay green.  Candidates I already see: `>=` back to `>` (the equality cells); `return 0`
   moved inside the not-yet-warned branch (the second refused access forwards); the failed-read `return 0`
   changed to `return 1`; the failure check moved below the packing loop; the latch shared with one of the
   eight `LCA_W_IOC_*` bits #518 added; `PHYSICAL` dropped again.  Name the ones I have not.
3. **OPTION-SET COMPLETENESS.**  Is there a member S3 did not name for THIS site?  In particular: is member 4
   (ACCEPT) available for the `ofs == len` equality cells -- i.e. does the packing loop, once fixed to place
   the byte, make those accesses CORRECT rather than refusable?  Is member 7 (honour a<4:3>) the right
   disposition for (b) and what would it cost?  Grep the fork for the sibling idiom: `lca_ioc`'s #518
   default arm and `lca_pci_conf` in the same file.
4. **THE DETECTOR SHAPE the fix must ship with** -- rows, not prose.  From the (d) table in 1(e): an accept
   row per served cell (the de-escalation clause: the old exit was the tripwire for lane-guard growth), a
   decline row per refused cell reading the DECLINE CHANNEL (the zero downstream call, the unchanged
   register, the once-latched text), the (b) reinstatement, the two failure-propagation rows codex named, and
   `latch indep` against a #518 bit.  Which of these is VACUOUS BY CONSTRUCTION -- a row whose channel cannot
   vary under its mutant -- given your answer to 1(d)?
5. **If, while verifying a claim, you found something ELSE — say so.**

Do not run builds or probes (three kill tables are using the scratch clones and `build/`); do not propose a
patch to apply -- a sketch against the function above is welcome.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
