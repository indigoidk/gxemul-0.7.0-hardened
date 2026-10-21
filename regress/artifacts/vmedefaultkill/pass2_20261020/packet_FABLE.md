Open your answer with the token FABLE_VME_P2_20261020, then ONE line:
VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>

# `vmedefaultkill` (#568, HIGH) -- PASS 2 (diff review): the fix as it now sits in the working tree, its 34-row rung-3 detector, the gate-14 block, and KILL TABLE 1 (measured)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not
just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/` -- its WORKING TREE, on committed HEAD `1a59a47e`.**  The
round's edits are UNCOMMITTED there (section 3 lists every file).  There are THREE pristine-2021-upstream copies of GXemul
under the project root (`./src/` and two under `_archive/audit-results-*/builds/`); they are NOT this fork.  If your line
numbers disagree with mine by hundreds you are reading one of them -- say so rather than reconciling.  **Another session's
uncommitted edits also sit in this working tree** (`dev_pcc2.c`, `dev_lca.c`, `dev_sh4.c`, `cpu_alpha_palcode.c`,
`mvme_pcctworeg.h` among them): they are NOT part of this round -- ignore them, and do not cite their line numbers.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from
this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- an offset set, a bit index, a count -- ENUMERATE it rather than reasoning
about it.**  **And ENUMERATE THE RIGHT DOMAIN**: ask what the PRODUCER of the values can emit (here: which `relative_addr` /
`len` pairs the m88k load/store path delivers to a device) before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.

## 1. The round in one paragraph

`src/devices/dev_vme.c`'s `DEVICE_ACCESS(vme)` named ten offsets of its 4 KiB window and sent every other offset to
`default:`, which printed with `debug()` (silent at default verbosity while free-running) and called `exit(1)` -- the
emulator ended with no visible reason on any unnamed offset.  The device exists only on `-E mvme88k -e mvme187`
(window 0xfff40000-0xfff40fff).  **Two owner rulings fixed the disposition (S2, S3 below); pass 1 (4 of 4 roster seats
plus a second packet-fed lens, all PROCEED WITH CHANGES) reviewed the sketch and the detector plan; this pass reviews
what was BUILT and MEASURED.**  The disposition itself is not open here unless you can show the code does not implement
it.

## 2. SETTLED PREMISES (re-inlined so nobody spends an answer re-deriving them)

* **S1** `dev_vme.c` was untouched since the 0.7.0 import before this round (`git log` lists one commit, `39748e3c`).
* **S2 OWNER RULING 2026-09-11 -- population 1 (word starts the header does not name, 0x90..0xffc, and every sub-word
  start): FAULT** (`return 0`; `memory_rw.c` turns a handler's `return 0` into an m88k data-access exception for a guest
  load/store).  Justified as "an access the emulator cannot service", NOT as a claim about the real VMEchip2, whose
  register chapter is not on disk.
* **S3 OWNER RULING 2026-10-09 -- population 2 (the 26 header-named register word starts with no case): DECLINE +
  ANNOUNCE ONCE** -- "reads 0, writes dropped, one `fatal()` per register, `(once)` marker", the shape of `#501`'s arm in
  `dev_pcc2.c`.  BACKED ACCEPT (inventing storage) was ruled NOT licensed.
* **S4** populations 3 (sub-word starts inside the ten CASED words) and 4 (a CASED base at len != 4) are FILED as
  `vmewidthlanes` (LOW).  This round DISCLOSES that they reach the fault, and pins ONE interim row as a named channel.
* **S5 (pass 1, re-derived by five readers)** the census is 10 cased / 26 population-2 / 988 population-1 word starts.
* **S6 (pass 1, all five)** `d->reg[w] == 0` for every population-2 word for the device's life: the only writers of
  `d->reg[]` are the T1CMP, T1COUNT, TCTL and VBR arms (indices 20, 21, 24, 34) and DEVINIT's VBR seed; an 8-byte store
  writes one element; `DM_DEFAULT` gives no host fast path.
* **S7 (pass 1, qualified by four seats)** `return 0` -> a data-access exception (vector 3; VBR 0 at reset -> PC 0x18)
  for a GUEST load/store.  NO_EXCEPTIONS callers (the debugger's `dump`/`put`, the disassembler, `memory.c` helpers)
  never reach the handler -- silent success with a zero fill, identical before and after.  An INSTRUCTION fetch takes
  vector 2 and then halts the emulation (pre-existing for every faulting fetch).  A second fault while PSR.SFRZ is set
  becomes ERROR (PC 0x50), so every stepped fault row has a session of its own.
* **S8 (pass 1, three seats by reading `cpu_m88k_instr_loadstore.c`)** the producer domain is naturally-aligned
  accesses only: a misaligned halfword/word/double traps on alignment BEFORE the device; `ld.d`/`st.d` is ONE len-8 call;
  nothing crosses the 1 KiB splitter or the device end.
* **S9 (MEASURED, probe revision 2)** DMT0 = 0x423d (word load into r4), 0x433d (into r6), 0x403f (word store), 0x4211
  (byte at addr & 3 == 1), 0x420d (halfword at addr & 2 == 2); DMA0 is the WORD address.  Eight values PREDICTED from the
  CPU code before the first run, all eight measured as predicted.
* **S10 (MEASURED, 2026-10-20 re-witness on HEAD 5dbc000e)** 7 of 7 guest sites end the emulator (rc 1); a free-running
  MASTERCTL read dies with NO `[ vme:` text.

**Pass-1 dispositions the build implements (condensed; the full record is `pass1_20261020/ADJUDICATION_p1.md`):**
D1 exact case labels (one dissent, Fable, for a bound test in `default:` -- recorded, main loop kept labels);
D2 no `odata = 0`, a comment states the zero-storage invariant, **and the read announce prints the served value**;
D3 the write announce prints all 64 bits (`0x%llx` of `(unsigned long long) idata`); D4 sub-word starts inside
population-2 words FAULT as the interim, disclosed, pinned by two rows; D5 population 1 keeps both `debug()` lines,
`exit(1)` -> `return 0`, comment "an offset this model does not service"; D6 the guest comment corrected (MASTERCTL is
READ then written back; IRQSTAT read, IRQCLR never written when it reads 0); D7 a compile-time capacity check on the latch.

**ONE KNOWN DEVIATION, DISCLOSED BY THE AUTHOR -- please rule on it (Q2c):** D2's record names the read-announce form
`-- served 0x%llx` with `(unsigned long long) odata`.  **The built code prints `-- served 0x%x` with `(unsigned) odata`.**
`odata` is `uint64_t`, assigned `d->reg[relative_addr / sizeof(uint32_t)]` -- a `uint32_t` element -- so its high 32 bits
are zero for every read this arm serves and the printed TEXT is identical today.  Nothing in the build record says why the
form changed; I found it while writing this brief.

## 3. The round's files (`git diff --numstat` plus the new files), each marked

```
    regress/gate_arm.sh                        +24    -0     INLINED (section 7)
    src/devices/dev_vme.c                      +75    -1     INLINED (section 4 diff + section 5 whole device)
    tools/pipeline/check_probe_wiring.py       +15    -0     SUMMARIZED -- MANIFEST lines registering the new probe (CLASS_DETECTOR) and the round's research scripts; carries another unit's hunks too
    regress/vme_default_probe.py               (new, 871 lines)  SUMMARIZED -- row plan + contract inlined (section 6); file-reading seats read the frozen copy
    regress/artifacts/vmedefaultkill/*_20261020/ (new)  NOT SHOWN -- records: the pass-1 packets/answers, the HEAD re-witness, the PRETABLE files, kill table 1's logs
    tools/pipeline/ledger.json, matrix.html    (modified)  NOT SHOWN -- the ledger row and the matrix render
```
Every other modified path in `git status` belongs to another unit or another session and is NOT part of this round.

## 4. The diff of `src/devices/dev_vme.c`, verbatim (`git diff -- src/devices/dev_vme.c`)

```diff
diff --git a/src/devices/dev_vme.c b/src/devices/dev_vme.c
index b4a6050d..34023b8d 100644
--- a/src/devices/dev_vme.c
+++ b/src/devices/dev_vme.c
@@ -51,8 +51,21 @@
 
 struct vme_data {
 	uint32_t	reg[VME_LEN / sizeof(uint32_t)];
+
+	/*  #568: one bit per register WORD (relative_addr >> 2) for the
+	    unimplemented-register announce below; the highest such word is
+	    VME2_MISC (0x8c >> 2 == 35).  Zeroed by DEVINIT's memset, so every
+	    instance starts with every announce armed.  */
+	uint64_t	warned_unimpl;
 };
 
+/*  #568: narrowing warned_unimpl, or the 1ULL below, would shift past bit
+    VME2_MISC >> 2; make that a compile error (dev_pcc2.c's
+    pcc2_w_fits_in_warned shape).  */
+typedef char vme_warned_fits[((VME2_MISC >> 2) <
+    8 * sizeof(((struct vme_data *)0)->warned_unimpl)
+    && (VME2_MISC >> 2) < 8 * sizeof(1ULL)) ? 1 : -1];
+
 
 DEVICE_ACCESS(vme)
 {
@@ -134,13 +147,74 @@ DEVICE_ACCESS(vme)
 			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 		break;
 
+	/*  #568 (vmedefaultkill): registers the header names but this model
+	    does not implement.  Each ended the emulator in default: below.
+	    The in-tree OpenBSD 2.2 guest reaches six of them: vme2chip_init()
+	    reads MASTERCTL and writes it back and writes MASTER3, MASTER4 and
+	    MASTER4MOD; vme2abort() reads IRQSTAT (served 0, it reports "irq
+	    not set" and returns before writing IRQCLR).  A bus error here
+	    would panic that guest's attach, so these DECLINE: a read is served
+	    the word preloaded above, which is 0 because nothing writes these
+	    words of d->reg[] (odata is deliberately not forced to 0, so a store
+	    added by a later edit would show in a read-back); a write is
+	    dropped; one fatal() per register per device, the first access's
+	    direction deciding its wording (#501's shape in dev_pcc2.c).
+	    Sub-word starts inside these words are not matched here and reach
+	    default: (vmewidthlanes).  */
+	case VME2_SADDR2:
+	case VME2_SLAVELMOD1:
+	case VME2_SLAVELMOD2:
+	case VME2_SLAVECTL:
+	case VME2_MASTER1:
+	case VME2_MASTER2:
+	case VME2_MASTER3:
+	case VME2_MASTER4:
+	case VME2_MASTER4MOD:
+	case VME2_MASTERCTL:
+	case VME2_DMACTL:
+	case VME2_DMAMODE:
+	case VME2_DMALADDR:
+	case VME2_DMAVMEADDR:
+	case VME2_DMACOUNT:
+	case VME2_DMATABLE:
+	case VME2_DMASTAT:
+	case VME2_T2CMP:
+	case VME2_T2COUNT:
+	case VME2_PRESCALE:
+	case VME2_IRQSTAT:
+	case VME2_SETSOFTIRQ:
+	case VME2_IRQCLR:
+	case VME2_IRQL1:
+	case VME2_IRQL2:
+	case VME2_MISC:
+		if (!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {
+			d->warned_unimpl |= 1ULL << (relative_addr >> 2);
+			if (writeflag == MEM_WRITE)
+				fatal("[ vme: unimplemented write to register "
+				    "0x%x (len %d): 0x%llx -- declined.  (once) ]\n",
+				    (unsigned) relative_addr, (int) len,
+				    (unsigned long long) idata);
+			else
+				fatal("[ vme: unimplemented read from register "
+				    "0x%x (len %d) -- served 0x%x.  (once) ]\n",
+				    (unsigned) relative_addr, (int) len,
+				    (unsigned) odata);
+		}
+		break;
+
 	default:if (writeflag == MEM_READ)
 			debug("[ vme: unimplemented READ from offset 0x%x ]"
 			    "\n", (int)relative_addr);
 		else
 			debug("[ vme: unimplemented WRITE to offset 0x%x: "
 			    "0x%x ]\n", (int)relative_addr, (int)idata);
-		exit(1);
+		/*  #568 (vmedefaultkill): an offset this model does not service:
+		    no header-named register, or the inside of one (a sub-word
+		    start).  Refuse the access -- memory_rw then raises the m88k
+		    data-access exception, the bus error a badaddr() probe
+		    expects -- instead of exit(1), which ended the emulator with
+		    no visible reason (debug() is silent at default verbosity).  */
+		return 0;
 	}
 
 	if (writeflag == MEM_READ)
```

## 5. The whole device AFTER the fix, numbered from the working file (struct, the access function with its common tail, DEVINIT)

```c
  52  struct vme_data {
  53  	uint32_t	reg[VME_LEN / sizeof(uint32_t)];
  54  
  55  	/*  #568: one bit per register WORD (relative_addr >> 2) for the
  56  	    unimplemented-register announce below; the highest such word is
  57  	    VME2_MISC (0x8c >> 2 == 35).  Zeroed by DEVINIT's memset, so every
  58  	    instance starts with every announce armed.  */
  59  	uint64_t	warned_unimpl;
  60  };
  61  
  62  /*  #568: narrowing warned_unimpl, or the 1ULL below, would shift past bit
  63      VME2_MISC >> 2; make that a compile error (dev_pcc2.c's
  64      pcc2_w_fits_in_warned shape).  */
  65  typedef char vme_warned_fits[((VME2_MISC >> 2) <
  66      8 * sizeof(((struct vme_data *)0)->warned_unimpl)
  67      && (VME2_MISC >> 2) < 8 * sizeof(1ULL)) ? 1 : -1];
  68  
  69  
  70  DEVICE_ACCESS(vme)
  71  {
  72  	struct vme_data *d = (struct vme_data *) extra;
  73  	uint64_t idata = 0, odata = 0;
  74  
  75  	if (writeflag == MEM_WRITE)
  76  		idata = memory_readmax64(cpu, data, len);
  77  
  78  	if (writeflag == MEM_READ)
  79  		odata = d->reg[relative_addr / sizeof(uint32_t)];
  80  
  81  	switch (relative_addr) {
  82  
  83  	case 0:	/*  Used by OpenBSD/mvme88k when probing...  */
  84  		break;
  85  
  86  	case VME2_GCSRCTL:
  87  		debug("[ vme: unimplemented GCSRCTL ]\n");
  88  		break;
  89  
  90  	case VME2_TCR:
  91  		if (writeflag == MEM_READ)
  92  			debug("[ vme: unimplemented READ from TCR ]\n");
  93  		else
  94  			debug("[ vme: unimplemented WRITE to TCR: "
  95  			    "0x%x ]\n", (int)idata);
  96  		break;
  97  
  98  	case VME2_T1CMP:
  99  		if (writeflag == MEM_WRITE)
 100  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 101  		break;
 102  
 103  	case VME2_T1COUNT:
 104  		if (writeflag == MEM_WRITE)
 105  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 106  		else {
 107  			/*  NOTE! This is a quick hack. TODO: Fix!  */
 108  			d->reg[relative_addr / sizeof(uint32_t)] += 100;
 109  		}
 110  		break;
 111  
 112  	case VME2_TCTL:
 113  		if (writeflag == MEM_WRITE)
 114  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 115  
 116  		/*  TODO  */
 117  		/*  debug("[ vme: unimplemented TCTL ]\n");  */
 118  		break;
 119  
 120  	case VME2_IRQEN:
 121  		if (writeflag == MEM_READ)
 122  			debug("[ vme: unimplemented READ from IRQEN ]\n");
 123  		else
 124  			debug("[ vme: unimplemented WRITE to IRQEN: "
 125  			    "0x%x ]\n", (int)idata);
 126  		break;
 127  
 128  	case VME2_IRQL3:
 129  		if (writeflag == MEM_READ)
 130  			debug("[ vme: unimplemented READ from IRQL3 ]\n");
 131  		else
 132  			debug("[ vme: unimplemented WRITE to IRQL3: "
 133  			    "0x%x ]\n", (int)idata);
 134  		break;
 135  
 136  	case VME2_IRQL4:
 137  		if (writeflag == MEM_READ)
 138  			debug("[ vme: unimplemented READ from IRQL4 ]\n");
 139  		else
 140  			debug("[ vme: unimplemented WRITE to IRQL4: "
 141  			    "0x%x ]\n", (int)idata);
 142  		break;
 143  
 144  	case VME2_VBR:
 145  		/*  Vector Base Register.  */
 146  		if (writeflag == MEM_WRITE)
 147  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 148  		break;
 149  
 150  	/*  #568 (vmedefaultkill): registers the header names but this model
 151  	    does not implement.  Each ended the emulator in default: below.
 152  	    The in-tree OpenBSD 2.2 guest reaches six of them: vme2chip_init()
 153  	    reads MASTERCTL and writes it back and writes MASTER3, MASTER4 and
 154  	    MASTER4MOD; vme2abort() reads IRQSTAT (served 0, it reports "irq
 155  	    not set" and returns before writing IRQCLR).  A bus error here
 156  	    would panic that guest's attach, so these DECLINE: a read is served
 157  	    the word preloaded above, which is 0 because nothing writes these
 158  	    words of d->reg[] (odata is deliberately not forced to 0, so a store
 159  	    added by a later edit would show in a read-back); a write is
 160  	    dropped; one fatal() per register per device, the first access's
 161  	    direction deciding its wording (#501's shape in dev_pcc2.c).
 162  	    Sub-word starts inside these words are not matched here and reach
 163  	    default: (vmewidthlanes).  */
 164  	case VME2_SADDR2:
 165  	case VME2_SLAVELMOD1:
 166  	case VME2_SLAVELMOD2:
 167  	case VME2_SLAVECTL:
 168  	case VME2_MASTER1:
 169  	case VME2_MASTER2:
 170  	case VME2_MASTER3:
 171  	case VME2_MASTER4:
 172  	case VME2_MASTER4MOD:
 173  	case VME2_MASTERCTL:
 174  	case VME2_DMACTL:
 175  	case VME2_DMAMODE:
 176  	case VME2_DMALADDR:
 177  	case VME2_DMAVMEADDR:
 178  	case VME2_DMACOUNT:
 179  	case VME2_DMATABLE:
 180  	case VME2_DMASTAT:
 181  	case VME2_T2CMP:
 182  	case VME2_T2COUNT:
 183  	case VME2_PRESCALE:
 184  	case VME2_IRQSTAT:
 185  	case VME2_SETSOFTIRQ:
 186  	case VME2_IRQCLR:
 187  	case VME2_IRQL1:
 188  	case VME2_IRQL2:
 189  	case VME2_MISC:
 190  		if (!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {
 191  			d->warned_unimpl |= 1ULL << (relative_addr >> 2);
 192  			if (writeflag == MEM_WRITE)
 193  				fatal("[ vme: unimplemented write to register "
 194  				    "0x%x (len %d): 0x%llx -- declined.  (once) ]\n",
 195  				    (unsigned) relative_addr, (int) len,
 196  				    (unsigned long long) idata);
 197  			else
 198  				fatal("[ vme: unimplemented read from register "
 199  				    "0x%x (len %d) -- served 0x%x.  (once) ]\n",
 200  				    (unsigned) relative_addr, (int) len,
 201  				    (unsigned) odata);
 202  		}
 203  		break;
 204  
 205  	default:if (writeflag == MEM_READ)
 206  			debug("[ vme: unimplemented READ from offset 0x%x ]"
 207  			    "\n", (int)relative_addr);
 208  		else
 209  			debug("[ vme: unimplemented WRITE to offset 0x%x: "
 210  			    "0x%x ]\n", (int)relative_addr, (int)idata);
 211  		/*  #568 (vmedefaultkill): an offset this model does not service:
 212  		    no header-named register, or the inside of one (a sub-word
 213  		    start).  Refuse the access -- memory_rw then raises the m88k
 214  		    data-access exception, the bus error a badaddr() probe
 215  		    expects -- instead of exit(1), which ended the emulator with
 216  		    no visible reason (debug() is silent at default verbosity).  */
 217  		return 0;
 218  	}
 219  
 220  	if (writeflag == MEM_READ)
 221  		memory_writemax64(cpu, data, len, odata);
 222  
 223  	return 1;
 224  }
 225  
 226  
 227  DEVINIT(vme)
 228  {
 229  	struct vme_data *d;
 230  
 231  	CHECK_ALLOCATION(d = (struct vme_data *) malloc(sizeof(struct vme_data)));
 232  	memset(d, 0, sizeof(struct vme_data));
 233  
 234  	/*  According to OpenBSD/mvme88k:  */
 235  	d->reg[VME2_VBR / sizeof(uint32_t)] =
 236  	    VME2_SET_VBR0(6) + VME2_SET_VBR1(7);
 237  
 238  	memory_device_register(devinit->machine->memory, devinit->name,
 239  	    devinit->addr, VME_LEN, dev_vme_access, (void *)d,
 240  	    DM_DEFAULT, NULL);
 241  
 242  	return 1;
 243  }
```

## 6. The detector: `regress/vme_default_probe.py` (new, 34 rows)

**File-reading seats: read the FROZEN COPY of the measured instrument, not the working file** -- `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/vmedefaultkill/killtable1_20261020/vme_default_probe.frozen.py` (md5 `19de15b3ea69af28e437cdf92e22c97e`, byte-identical to the working `regress/vme_default_probe.py` at brief-writing time, 871 lines).  Packet-fed seats: its row plan and contract are inlined below.

Its own docstring's ROW PLAN, verbatim (each row with the mutant it is designed to catch and the channel that differs):

```
ROWS, each with the mutant it is DESIGNED to catch and the channel that differs under it.
*** NO KILL TABLE EXISTS FOR THIS REVISION.  Every mutant outcome below is PREDICTED by reading fix568; only
HEAD, fix568 and the null medium were measured (run2_HEAD.out / run2_FIX568.out / run2_NULL.out). ***
  apparatus (CONTROL)
    neg apparatus  a bogus subtype: the liveness oracle MUST go red (it is failable)
    session / live the control session runs to `quit'; an or-immediate reads back
    vbr reset      DEVICE SIGNATURE: DEVINIT's VBR seed (RAM or a device-less build answers 0)
    t1cmp rt       cased T1CMP stores and reads back (and is the null medium's second discriminator)
    cased census   one ld at each of the ten cased offsets, ONE session, sentinel-seeded, PC + liveness after:
                   a cased label dropped FAULTs that offset and every later load keeps its sentinel
    free ctl       FREE-RUNNING T1CMP round trip to a breakpoint
    free quiet     ...that run prints NO vme text at all (a cased access never announces)
    free neg ctl   GCSRCTL's debug() line: PRESENT in the stepped cased census, ABSENT in the free run -- the
                   run was free at verbose 0, so the fatal-vs-debug channel of the announce rows can vary
    unasm          every placed word re-read by the disassembler
  cased accept side -- the write paths the de-escalation clause owes (not CONTROL: they detect mutants)
    tctl rt        TCTL stores a word and reads it back
    vbr rt         VBR stores a word and reads it back, then is restored to the seed and read back again
    t1count inc    T1COUNT stores a word; two reads give it and it + 100 (the read arm's `+= 100')
    cased wr       a word store to each of the six NON-storing cased arms (0x00, GCSRCTL, TCR, IRQEN, IRQL3,
                   IRQL4): no fault, PC + liveness after
  population 2 (decline)
    p2 rd census   26 ld: all 0, no fault, PC + liveness after; a label dropped FAULTs (HEAD: the host dies)
    p2 wr census   26 st of 0xa5a5a5a5, a liveness or (checked: a FAULTING store stops it), then the 26 ld:
                   all 0.  A decline that STORES reads back non-zero -- visible because fix568 does NOT force
                   odata = 0; a decline conditioned on direction FAULTs
    p2 ld widths   ld.bu + ld.hu at 0x28, ld.d at 0x08 (BOTH r6 and r7): 0, no fault -- a decline conditioned
                   on len FAULTs one of them
    p2 st widths   st.b + st.h at 0x28, st.d at 0x08, a liveness or, then read 0x28, 0x08, 0x0c back: all 0
  announce (FREE-RUNNING; full tail literals; every offset exactly once)
    p2 ann rd      each of the 26 READ then immediately WRITTEN: exactly 26 read-form lines, 0 write-form
    p2 ann rd 2    the same pairs again in the same session: 0 lines, PC at the breakpoint, liveness proof
    p2 ann wr      each WRITTEN then immediately READ: exactly 26 write-form lines `(len 4): 0xa5a5a5a5'
    p2 ann wr 2    the same pairs again: 0 lines, PC at the breakpoint, liveness proof
                   -- together 26 labels x {read, write} x {latch clear, set}: read- or write-branch
                   fatal -> debug (0 lines), a shared latch (1), a never-set latch (52), a per-direction latch
                   (52), a latch cleared by a write (pass 2 re-announces), a latch set at one constant bit
                   (51), a dropped `(once)' or changed tail (no exact match)
    p2 nw rd       FIRST access to three untouched registers by ld.bu / ld.hu / ld.d: `(len 1)', `(len 2)',
                   `(len 8) -- served 0x0.' -- an announce that fires only for 4-byte accesses gives 0
    p2 nw wr       FIRST access by st.b / st.h / st.d: `(len 1): 0xd4', `(len 2): 0xc3d4',
                   `(len 8): 0x1122334455667788' -- a 32-bit truncation of the 64-bit value fails the match
  population 1 (fault)
    p1 fault lo / hi / mid   ld at 0x90 / 0xffc / 0x94: PC 0x18, DMA0, DMT0 (word load into r4), host alive;
                   `return 0' -> `break' serves the read (PC advances); exit(1) reinstated kills the host
    p1 fault wr    st at 0x90: PC 0x18, DMA0, DMT0 (the word-store form)
    p1 p2 edge     ld 0x8c declines (0), then ld 0x90 faults: the label set's last member dropped faults at
                   0x8c instead; a label added AT 0x90 declines it
    p1 census      FREE-RUNNING: all 988 population-1 word starts, faults counted: a label added at ANY of them
                   gives 987; `return 0' -> `break' gives 0
    p1 widths      FREE-RUNNING: ld.bu 0x93, ld.hu 0x96, ld.d 0x98, st.b 0x9d, st.h 0xa2, st.d 0xa8 -- six
                   faults: a FAULT narrowed to word accesses (or to one direction) declines some of them
  interims -- NAMED channels of `vmewidthlanes': that round reds these and re-derives them
    p3 interim     ld.bu 0x51 (inside cased T1CMP): fault, DMA0 0xfff40050 -- also `if (len != 4) break;' in
                   `default:' (Fable) declines it
    p2 int byte    ld.bu 0x29 (inside population-2 MASTERCTL): fault, DMA0 0xfff40028
    p2 int half    ld.hu 0x2a (inside MASTERCTL): fault, DMA0 0xfff40028

CONTRACT (clause e).  DESIGNED to catch: the mutants named above, by the channels named above -- a design claim
until a kill table measures it.  NOT CLAIMED, so a later escape is outside the contract rather than an argument:
  * populations 3 and 4 and population-2 sub-word starts beyond the three interim pins (one byte at 0x51, one
    byte at 0x29, one halfword at 0x2a);
  * ld.d / st.d at the cased bases 0x00, 0x60 and 0x88, whose second word is a population-2 register (0x04,
    0x64, 0x8c): the device sees ONE access to the cased label;
  * cased-word ld.d / st.d lane placement (population 4: a 32-bit register served into, or stored from, the
    wrong half of an 8-byte access);
  * NO_EXCEPTIONS callers -- the debugger's put/dump/unassemble never reach the handler (silent zero fill);
  * instruction fetch from the window (a population-1 fetch takes vector 2 and halts; a population-2 fetch
    declines);
  * xmem (declines twice at population 2 -- the store silently; its load faults at population 1);
  * per-instance latch isolation: mvme187 attaches ONE vme device per process;
  * the guest's abort-handler consequence (IRQSTAT served 0: OpenBSD's vme2abort() returns "irq not set");
  * population-1 accesses other than the 988 word loads, the four stepped faults and the six width faults;
  * a served value other than 0 in the read announce (no population-2 word is ever non-zero);
  * anything about the real VMEchip2 (its register chapter is not on disk).
```

## 7. The gate-14 block (`regress/gate_arm.sh`), verbatim from the diff

```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index 887c3302..e33f2ceb 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1884,6 +1884,30 @@ else
 fi
 
 
+#  ------------------------------------------------------------ vmedefaultkill (#568)
+#  dev_vme.c's default: ended the emulator (exit(1), announced only by debug() -- silent while
+#  free-running) on any VME2 offset the switch did not name.  Now: the 26 header-named registers
+#  the model does not implement DECLINE (reads served the preloaded word, writes dropped, one
+#  latched fatal() per register); every other unmatched offset returns 0, and memory_rw raises the
+#  m88k data-access exception.  The rung-3 witness (regress/artifacts/vmedefaultkill/
+#  witness_20261020/, 7 of 7 guest sites rc 1 on 5dbc000e) is NOT run here; this is its detector.
+#  Needs only the binary: mvme88k/mvme187 constructs from the PROM, like the mk48/pcc2 blocks above.
+VMEDLOG=$LOGDIR/vme_default.log
+python3 -u vme_default_probe.py "$PMAX" gate > "$VMEDLOG" 2>&1 || true
+if ! grep -q "VME_DEFAULT_PROBE_DONE" "$VMEDLOG"; then
+    check "vme default probe completed" "no" "yes"
+else
+    check "vme default probe completed" "yes" "yes"
+    check "vme default controls" "$(grep -c '^VME_DEFAULT_CONTROL=OK$' "$VMEDLOG")" "1"
+    for v in "neg apparatus" "session" "live" "vbr reset" "t1cmp rt" "cased census" "free ctl" "free quiet" "free neg ctl" "tctl rt" "vbr rt" "t1count inc" "cased wr" "p2 rd census" "p2 wr census" "p2 ld widths" "p2 st widths" "p2 ann rd" "p2 ann rd 2" "p2 ann wr" "p2 ann wr 2" "p2 nw rd" "p2 nw wr" "p1 fault lo" "p1 fault hi" "p1 fault mid" "p1 fault wr" "p1 p2 edge" "p3 interim" "p2 int byte" "p2 int half" "p1 census" "p1 widths" "unasm"; do
+        check "vme default row: $v" "$(count "$VMEDLOG" "^$v  .*ok$")" "1"
+    done
+    check "vme default rows emitted" "$(( $(count "$VMEDLOG" " ok$") + $(count "$VMEDLOG" " FAIL$") ))" "34"
+    check "vme default rows green"   "$(count "$VMEDLOG" " ok$")"   "34"
+    check "vme default rows red"     "$(count "$VMEDLOG" " FAIL$")" "0"
+fi
+
+
 #  ------------------------------------------------------------ hpcmipsctor (#444) + #536
 #  Three of eight advertised hpcmips subtypes SIGABRTed during construction (#444).  Its rung-2
 #  detector (~8 s, no rig image) shipped EXEMPT for want of a construction gate; #536 wires it here.
```

## 8. KILL TABLE 1 -- MEASURED in a scratch clone of HEAD, one build per leg, the probe frozen for the whole table

Condensed from `regress/artifacts/vmedefaultkill/killtable1_20261020/KILLTABLE1_VS_PRETABLE.out` and `table1b/KILLTABLE1B.out` (the measuring seat's comparisons of every leg against predictions written before each table ran): the per-leg prediction text and the seat-reading field are dropped from each table line, table 1's own per-row census is replaced by table 1b's COMBINED census, and the apparatus observations (timing, restore, run hygiene) and table 1b's provenance header are omitted.  Everything else is verbatim.

```
KILLTABLE1_VS_PRETABLE -- #568 (vmedefaultkill) kill table 1, measured 2026-10-20 by the measuring seat (Opus 5.5).
Fix: scratchpad vme/fix/dev_vme.fix568.c md5 4e3e7fc220062b429f7d9d6e140fec9e.  Detector: vme_default_probe.py revision 2,
FROZEN as killtable1/vme_default_probe.frozen.py (md5 19de15b3ea69af28e437cdf92e22c97e) and that copy alone ran every leg.
Clone: WSL /tmp/gxkt568 from `git archive 1a59a47e' (1a59a47e3ebbb648f06268ab790f901cbc71c88a), configure + make -j4;
each leg = ONE exact find/replace on fix568 (mk_legs568.py; legs/<LEG>.diff), dev_vme.o + machine_mvme88k.o + gxemul
removed before every build, `[ gxemul -nt <source> ]' checked after it (RUNLOG.txt, build/<LEG>.build.log).  This script
refuses any raw lacking VME_DEFAULT_PROBE_DONE; first-attempt and frozen-md5 counts are in OBSERVATIONS (f).
Predictions = PRETABLE_ADDENDUM_v2.out section 4, quoted verbatim, parsed by one rule: `a/b' expands to the named rows; a
second-pass row (p2 ann rd 2 / p2 ann wr 2) counts as predicted ONLY where the text names it.  MATCH = measured red set ==
predicted set; MISS = a predicted row stayed green or an unpredicted row went red.  The pre-run seat reading
(SEAT_PREDICTIONS_prerun.txt, mtime before the first build) is compared in the last field.

######## TABLE 1
== REFERENCE RUNS ==
HEAD | 14/34 | CONTROL=OK | red(20): p2 rd census, p2 wr census, p2 ld widths, p2 st widths, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p2 nw rd, p2 nw wr, p1 fault lo, p1 fault hi, p1 fault mid, p1 fault wr, p1 p2 edge, p3 interim, p2 int byte, p2 int half, p1 census, p1 widths | MATCH
BASE | 34/34 | CONTROL=OK | red(0): - | MATCH
NULL | 5/34 | CONTROL=FAIL | red(29): vbr reset, t1cmp rt, cased census, free ctl, free neg ctl, tctl rt, vbr rt, t1count inc, cased wr, p2 rd census, p2 wr census, p2 ld widths, p2 st widths, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p2 nw rd, p2 nw wr, p1 fault lo, p1 fault hi, p1 fault mid, p1 fault wr, p1 p2 edge, p3 interim, p2 int byte, p2 int half, p1 census, p1 widths | MATCH
BASE_FINAL | 34/34 | CONTROL=OK | red(0): - | MATCH

== THE TABLE (LEG | score | CONTROL | measured red rows | vs the pre-table prediction) ==
M_EXIT | 24/34 | CONTROL=OK | red(10): p1 fault lo, p1 fault hi, p1 fault mid, p1 fault wr, p1 p2 edge, p3 interim, p2 int byte, p2 int half, p1 census, p1 widths | MATCH
M_DROPMCTL | 26/34 | CONTROL=OK | red(8): p2 rd census, p2 wr census, p2 ld widths, p2 st widths, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2 | MISS (unpredicted red: p2 ld widths, p2 st widths)
M_DROPMISC | 27/34 | CONTROL=OK | red(7): p2 rd census, p2 wr census, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p1 p2 edge | MISS (unpredicted red: p2 ann rd 2, p2 ann wr 2)
M_ADD94 | 32/34 | CONTROL=OK | red(2): p1 fault mid, p1 census | MATCH
M_LATCHONE | 30/34 | CONTROL=OK | red(4): p2 ann rd, p2 ann wr, p2 nw rd, p2 nw wr | MISS (unpredicted red: p2 nw rd, p2 nw wr)
M_LATCHNOSET | 30/34 | CONTROL=OK | red(4): p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2 | MATCH
M_LATCHRDSET | 33/34 | CONTROL=OK | red(1): p2 ann wr | MATCH
M_LATCHCLRW | 31/34 | CONTROL=OK | red(3): p2 ann rd, p2 ann rd 2, p2 ann wr 2 | MISS (unpredicted red: p2 ann rd 2, p2 ann wr 2)
M_LATCHCLRW_POST | 31/34 | CONTROL=OK | red(3): p2 ann rd 2, p2 ann wr, p2 ann wr 2 | MISS (predicted but GREEN: p2 ann rd; unpredicted red: p2 ann rd 2, p2 ann wr, p2 ann wr 2)
M_WDEBUG | 31/34 | CONTROL=OK | red(3): p2 ann wr, p2 ann wr 2, p2 nw wr | MISS (unpredicted red: p2 ann wr 2)
M_RDEBUG | 31/34 | CONTROL=OK | red(3): p2 ann rd, p2 ann rd 2, p2 nw rd | MISS (unpredicted red: p2 ann rd 2)
M_ANNLEN4 | 32/34 | CONTROL=OK | red(2): p2 nw rd, p2 nw wr | MATCH
M_TRUNC | 33/34 | CONTROL=OK | red(1): p2 nw wr | MATCH
M_WRFAULT | 26/34 | CONTROL=OK | red(8): p2 wr census, p2 st widths, p2 ann rd, p2 ann rd 2, p2 ann wr, p2 ann wr 2, p2 nw rd, p2 nw wr | MISS (unpredicted red: p2 ann rd, p2 ann rd 2, p2 ann wr 2, p2 nw rd)
M_LENFAULT | 30/34 | CONTROL=OK | red(4): p2 ld widths, p2 st widths, p2 nw rd, p2 nw wr | MATCH
M_STORE | 32/34 | CONTROL=OK | red(2): p2 wr census, p2 st widths | MISS (unpredicted red: p2 st widths)
M_ODATA0 | 34/34 | CONTROL=OK | red(0): - | MATCH
M_SERVED0 | 34/34 | CONTROL=OK | red(0): - | MATCH
M_FLTBREAK | 24/34 | CONTROL=OK | red(10): p1 fault lo, p1 fault hi, p1 fault mid, p1 fault wr, p1 p2 edge, p3 interim, p2 int byte, p2 int half, p1 census, p1 widths | MATCH
M_FLTLEN | 30/34 | CONTROL=OK | red(4): p3 interim, p2 int byte, p2 int half, p1 widths | MATCH
M_FLTWR | 32/34 | CONTROL=OK | red(2): p1 fault wr, p1 widths | MATCH
M_NOONCE | 32/34 | CONTROL=OK | red(2): p2 ann rd, p2 nw rd | MISS (unpredicted red: p2 nw rd)
M_DROPTCTL | 30/34 | CONTROL=FAIL | red(4): cased census, tctl rt, vbr rt, t1count inc | MISS (unpredicted red: vbr rt, t1count inc)
M_CAPNARROW | BUILD FAILED | - | 66:dev_vme.c:65:14: error: size of array 'vme_warned_fits' is negative | MATCH

== SURVIVORS ==
M_ODATA0          34/34 CONTROL=OK -- PRETABLE: predicted SURVIVOR (equivalent today).  PREDICTED SURVIVOR: an equivalent-today edit (no population-2 word is ever non-zero, so a read is 0 and its announce prints 0x0 with or without the edit); a result about the TARGET, not a detector gap -- the probe's contract discloses it ("a served value other than 0 in the read announce").
M_SERVED0         34/34 CONTROL=OK -- PRETABLE: predicted SURVIVOR (equivalent today -- section 2 (i)).  PREDICTED SURVIVOR: an equivalent-today edit (no population-2 word is ever non-zero, so a read is 0 and its announce prints 0x0 with or without the edit); a result about the TARGET, not a detector gap -- the probe's contract discloses it ("a served value other than 0 in the read announce").

== MISS NOTES ==
M_DROPMCTL        cause: PREDICTION.  p2 ld widths / p2 st widths access 0x28 itself with ld.bu+ld.hu / st.b+st.h; the switch keys on relative_addr, not len, so `case VME2_MASTERCTL' declines those today and, dropped, they reach default: and FAULT (0/4 pc=0x18, 0/3 pc=0x18).  [measured: p2 ld widths = 0/4 pc=0x18 r31=0xdeadbeef; p2 st widths = 0/3 pc=0x18 r31=0xdeadbeef after-st r1=0xdeadbeef]
M_DROPMISC        cause: PREDICTION.  p2 ann rd 2 / p2 ann wr 2 read "pass 1 not completed" whenever pass 1 stops on a fault (here at 0x8c, after 25 lines) -- the mechanical consequence the addendum names for M_DROPMCTL ("+ their 2nd passes not completed") and omits for this leg.  [measured: p2 ann rd 2 = pass 1 not completed (FAILED FOR SOME OTHER REASON); p2 ann wr 2 = pass 1 not completed (FAILED FOR SOME OTHER REASON)]
M_LATCHONE        cause: PREDICTION.  the nonword session's six FIRST accesses also share the one latch: only its first access (ld.bu 0x04) announces, so p2 nw rd = 1/1 and p2 nw wr = 0/0.  [measured: p2 nw rd = 1/1; p2 nw wr = 0/0]
M_LATCHCLRW       cause: PREDICTION.  built as the addendum describes it (a write clears its bit BEFORE the check, so a read-first register re-announces on its write: p2 ann rd 52/26/26 as predicted); every later write re-announces too, so both second passes print 26 lines (p2 ann rd 2 = 26, p2 ann wr 2 = 26).  [measured: p2 ann rd 2 = 26; p2 ann wr 2 = 26]
M_LATCHCLRW_POST  cause: EDIT (translation, not a defect).  the VARIANT: PRETABLE.out section 5 says "the write clears; later reads", i.e. the clear AFTER the check.  Then the predicted row p2 ann rd stays GREEN (26/26/26: the read announces before the write clears it) and the rows that see it are p2 ann wr (52/26/26: each write-first register re-announces on its read) and both second passes (26 each).  The prediction text belongs to the pre-check form (M_LATCHCLRW); the detector kills both forms.  [measured: p2 ann rd = 26/26/26; p2 ann rd 2 = 26; p2 ann wr = 52/26/26; p2 ann wr 2 = 26]
M_WDEBUG          cause: PREDICTION.  p2 ann wr 2 reads "pass 1 silent (FAILED FOR SOME OTHER REASON)" whenever pass 1 printed no vme text -- a mechanical consequence of the predicted p2 ann wr 0/0/0.  [measured: p2 ann wr 2 = pass 1 silent (FAILED FOR SOME OTHER REASON)]
M_RDEBUG          cause: PREDICTION.  p2 ann rd 2 reads "pass 1 silent (FAILED FOR SOME OTHER REASON)" -- the same mechanical consequence of the predicted p2 ann rd 0/0/0.  [measured: p2 ann rd 2 = pass 1 silent (FAILED FOR SOME OTHER REASON)]
M_WRFAULT         cause: PREDICTION.  p2 ann rd's pass 1 WRITES each register right after reading it, so its first write faults (1/1/1 stopped pc=0x18) and both second passes read "pass 1 not completed"; the nonword session's first store (st.b 0x14) faults and stops the session, so p2 nw rd fails with p2 nw wr ("stopped pc=0x18").  [measured: p2 ann rd = 1/1/1 stopped pc=0x18; p2 ann rd 2 = pass 1 not completed (FAILED FOR SOME OTHER REASON); p2 ann wr 2 = pass 1 not completed (FAILED FOR SOME OTHER REASON); p2 nw rd = stopped pc=0x18 (FAILED FOR SOME OTHER REASON)]
M_STORE           cause: PREDICTION.  p2 st widths reads 0x28, 0x08 and 0x0c back after st.h 0x28 / st.d 0x08: a storing decline returns 0xc3d4 and 0x55667788 (1/3) -- that row sees a store exactly as p2 wr census does.  [measured: p2 st widths = 1/3]
M_NOONCE          cause: PREDICTION.  p2 nw rd's three first reads are matched against the same full read-form literal, so a dropped `(once)' fails it too (0/3).  [measured: p2 nw rd = 0/3]
M_DROPTCTL        cause: PREDICTION.  tctl rt, vbr rt and t1count inc share ONE stepped session whose first store is to TCTL (0x60); the fault stops it at 0x18, so all three accept rows go red, not tctl rt alone.  CONTROL=FAIL because cased census is a control row: detected, under the control reason (as the addendum's section 2 (iii) records for a dropped VBR label).  [measured: vbr rt = 0xdeadbeef/0xdeadbeef pc=0x18 r31=0xdeadbeef; t1count inc = 0xdeadbeef/0xdeadbeef pc=0x18 r31=0xdeadbeef]

== OBSERVATIONS (b), (c), (e) ==
(b) Red rows whose own got-text says "(FAILED FOR SOME OTHER REASON)" although the stop IS the leg's edit: 12 -- M_DROPMCTL/p2 ann rd 2, M_DROPMCTL/p2 ann wr 2, M_DROPMISC/p2 ann rd 2, M_DROPMISC/p2 ann wr 2, M_WDEBUG/p2 ann wr 2, M_RDEBUG/p2 ann rd 2, M_WRFAULT/p2 ann rd 2, M_WRFAULT/p2 ann wr 2, M_WRFAULT/p2 nw rd, M_WRFAULT/p2 nw wr, M_LENFAULT/p2 nw rd, M_LENFAULT/p2 nw wr.
    They are kills (the row reds, the score drops), but a reader of the row text alone would discount them.  Two
    shapes: a second-pass row ("pass 1 not completed" / "pass 1 silent") that only restates pass 1, and the
    nonword rows' "stopped pc=0x18" under M_WRFAULT and M_LENFAULT -- for M_LENFAULT those two rows ARE the
    channel PRETABLE named, so the CHANNEL claim holds while the row's text disowns it.
(c) CHANNEL check (PRETABLE section 4's last line asks the table to say whether each named channel varied): every row
    PRETABLE section 4 names against a leg built here went red under that leg.  Rows NO leg reds (10): neg apparatus, session, live, vbr reset, t1cmp rt, free ctl, free quiet, free neg ctl, cased wr, unasm.
    Nine are CONTROL rows; `cased wr' is not.  PRETABLE section 4 aims t1cmp rt, tctl rt, vbr rt, t1count inc and
    cased wr at "a cased WRITE path broken" and NO leg of this table builds that edit: tctl rt, vbr rt and
    t1count inc red only because M_DROPTCTL's label drop stops their shared session at its first store, and t1cmp
    rt / cased wr see no leg at all.  Likewise "a label added AT 0x90" (p1 p2 edge) was not built (M_ADD94 adds
    0x94).  Not measured here -- a gap in the TABLE, not a demonstrated detector gap.
(e) M_LATCHCLRW: PRETABLE.out section 5 ("the write clears; later reads") and the addendum ("each read-first
    register re-announces on its write") describe two different edits.  Both were built (M_LATCHCLRW = clear before
    the check, the addendum's; M_LATCHCLRW_POST = clear after it, section 5's) and both are killed (31/34 and 31/34).

== COUNTS ==
legs: 24 (the 23 PRETABLE legs + M_LATCHCLRW_POST, a second translation of M_LATCHCLRW); MATCH 13 (11 killed as predicted, incl. M_CAPNARROW's build failure; 2 predicted survivors); MISS 11; survivors 2; seat pre-run reading identical to the measured red set for 24 of 24 legs.
VERDICT: TABLE DONE -- 24 legs, 11 red as predicted, 11 misses, 2 survivors

######## TABLE 1b -- three legs added after table 1 to close the gaps its observation (c) names (no leg built
######## "a cased WRITE path broken"; no leg added a label AT 0x90).  Same frozen probe, a fresh clone, predictions
######## written to PRETABLE1B.txt BEFORE the first build.  Source: killtable1_20261020/table1b/KILLTABLE1B.out
== REFERENCE RUNS ==
BASE | 34/34 | CONTROL=OK | red(0): - | MATCH
BASE_FINAL | 34/34 | CONTROL=OK | red(0): - | MATCH

== THE TABLE (LEG | score | CONTROL | measured red rows | vs PRETABLE1B) ==
M_DROPIRQEN | 32/34 | CONTROL=FAIL | red(2): cased census, cased wr | MATCH
M_T1CMPWRDROP | 32/34 | CONTROL=FAIL | red(2): t1cmp rt, free ctl | MATCH
M_ADD90 | 30/34 | CONTROL=OK | red(4): p1 fault lo, p1 fault wr, p1 p2 edge, p1 census | MATCH

== MEASURED GOT-VALUES OF THE RED ROWS ==
M_DROPIRQEN       cased census = 6/11 pc=0x18; cased wr = 0x18/0xdeadbeef
M_T1CMPWRDROP     t1cmp rt = 0x0; free ctl = 0x0/0x67000000/0x1234
M_ADD90           p1 fault lo = exit0/0x1000c/0x0/0x0 r4=0x0 r5=0x1234; p1 fault wr = exit0/0x1000c/0x0/0x0 r5=0x1234; p1 p2 edge = 0x0/0x10010/0x0/0x0 r5=0x1234 r6=0x0; p1 census = 987/988 r4=0x0

== COUNTS ==
legs: 3; MATCH 3 (3 killed as predicted, 0 predicted survivors); MISS 0; survivors 0; seat reading identical (red rows and CONTROL) for 3 of 3.
VERDICT: TABLE 1B DONE -- 3 legs, 3 red as predicted, 0 misses, 0 survivors

== PER-ROW KILL CENSUS, TABLES 1 + 1b COMBINED (legs that red each row; HEAD and NULL excluded) ==
neg apparatus     0  -- no leg in either table reds it
session           0  -- no leg in either table reds it
live              0  -- no leg in either table reds it
vbr reset         0  -- no leg in either table reds it
t1cmp rt          1   | 1b: M_T1CMPWRDROP
cased census      2  M_DROPTCTL | 1b: M_DROPIRQEN
free ctl          1   | 1b: M_T1CMPWRDROP
free quiet        0  -- no leg in either table reds it
free neg ctl      0  -- no leg in either table reds it
tctl rt           1  M_DROPTCTL
vbr rt            1  M_DROPTCTL
t1count inc       1  M_DROPTCTL
cased wr          1   | 1b: M_DROPIRQEN
p2 rd census      2  M_DROPMCTL, M_DROPMISC
p2 wr census      4  M_DROPMCTL, M_DROPMISC, M_WRFAULT, M_STORE
p2 ld widths      2  M_DROPMCTL, M_LENFAULT
p2 st widths      4  M_DROPMCTL, M_WRFAULT, M_LENFAULT, M_STORE
p2 ann rd         8  M_DROPMCTL, M_DROPMISC, M_LATCHONE, M_LATCHNOSET, M_LATCHCLRW, M_RDEBUG, M_WRFAULT, M_NOONCE
p2 ann rd 2       7  M_DROPMCTL, M_DROPMISC, M_LATCHNOSET, M_LATCHCLRW, M_LATCHCLRW_POST, M_RDEBUG, M_WRFAULT
p2 ann wr         8  M_DROPMCTL, M_DROPMISC, M_LATCHONE, M_LATCHNOSET, M_LATCHRDSET, M_LATCHCLRW_POST, M_WDEBUG, M_WRFAULT
p2 ann wr 2       7  M_DROPMCTL, M_DROPMISC, M_LATCHNOSET, M_LATCHCLRW, M_LATCHCLRW_POST, M_WDEBUG, M_WRFAULT
p2 nw rd          6  M_LATCHONE, M_RDEBUG, M_ANNLEN4, M_WRFAULT, M_LENFAULT, M_NOONCE
p2 nw wr          6  M_LATCHONE, M_WDEBUG, M_ANNLEN4, M_TRUNC, M_WRFAULT, M_LENFAULT
p1 fault lo       3  M_EXIT, M_FLTBREAK | 1b: M_ADD90
p1 fault hi       2  M_EXIT, M_FLTBREAK
p1 fault mid      3  M_EXIT, M_ADD94, M_FLTBREAK
p1 fault wr       4  M_EXIT, M_FLTBREAK, M_FLTWR | 1b: M_ADD90
p1 p2 edge        4  M_EXIT, M_DROPMISC, M_FLTBREAK | 1b: M_ADD90
p3 interim        3  M_EXIT, M_FLTBREAK, M_FLTLEN
p2 int byte       3  M_EXIT, M_FLTBREAK, M_FLTLEN
p2 int half       3  M_EXIT, M_FLTBREAK, M_FLTLEN
p1 census         4  M_EXIT, M_ADD94, M_FLTBREAK | 1b: M_ADD90
p1 widths         4  M_EXIT, M_FLTBREAK, M_FLTLEN, M_FLTWR
unasm             0  -- no leg in either table reds it
```

## 9. Questions

**Q1 -- premise audit.**  Check each, by reading or enumerating rather than by agreeing:
* (a) The 26 labels are exactly the header-named register WORD STARTS in 0x04..0x8c minus the ten cased offsets -- no
  more, no fewer, no duplicate.  (Enumerate against section 5's labels and S5's census.)
* (b) `relative_addr >> 2` over the 26 labels takes 26 DISTINCT values, the largest 35 (MISC 0x8c), so a `uint64_t`
  latch has room and the typedef evaluates to an array of size 1 -- and narrowing either the field or the `1ULL` to 32
  bits makes it size -1.  (Leg M_CAPNARROW measured the field form as a failed build.)
* (c) At the population-2 arm, for a READ, `odata` already holds `d->reg[relative_addr / 4]`, which is 0 (S6), and the
  common tail then writes it to the guest and returns 1.  For a WRITE the arm stores nothing.
* (d) `return 0` in `default:` is reached by exactly: the 988 population-1 word starts, every sub-word start inside a
  population-2 word, and every sub-word start inside a cased word (population 3) -- and by nothing a guest could reach
  before this round without dying.  Use S8's producer domain.
* (e) Each kill-table leg is ONE edit of the fix and was built fresh (section 8's md5s and build log lines).

**Q2 -- the diff, hunk by hunk.**  (a) Does each hunk implement S2/S3 and D1-D7 against the function's REAL control flow
(section 5, common tail included)?  (b) Is any ADDED comment sentence false or stronger than the code?  (c) **Rule on the
disclosed D2 deviation**: keep `0x%x`/`(unsigned)` (lossless today) or align with D2's `0x%llx`/`(unsigned long long)`
(symmetric with the write announce; robust if a later `vmewidthlanes` fix ever composes a 64-bit `odata` for an `ld.d`)?
Give the reason either way.  (d) Anything in the gate block that cannot fail, or that fails for a reason other than the
one it names?

**Q3 -- the ask-again (capped at ONE per detector per round; this is it).**  Kill table 1 is clean except for the legs
predicted equivalent.  **What is the SMALLEST EDIT to `dev_vme.c` that breaks the ruled behaviour (S2/S3/D2-D7) and still
passes all 34 rows?**  Name the row you expect to stay green, and the observable that would differ for a guest.  Edits
already measured are in section 8 -- do not re-propose them.  Describe edits in words or as a one-line diff; do not build
anything.

**Q4 -- the vacuity floor, clause by clause.**  (a) fails pre-fix; (b) fails on a verbatim reinstatement of `exit(1)`;
(c) fails on a NULL medium -- this round's is a build WITHOUT the vme device, recorded as `(c): measured at <artifact>`;
(d) fails when the fix is present but its repair is NULLED -- enumerate the predicates DOMINATING the edited lines (to the
enclosing function boundary) and the body-read lvalues, and the dispatch-LABEL axis (each label's value flows into the
latch index) -- and say which (d) cell, if any, no leg or row covers; (e) the CONTRACT (the docstring's NOT CLAIMED list)
-- is anything missing that a reader would assume is covered?; (f) ANCHORING -- "if every address in this device shifted
one word, which row reds?"  If the answer for some class of rows is NONE, name the class.

Two measured facts for (d)-(f), from section 8: **`cased census` and `t1cmp rt` are CONTROL rows**, so a dropped cased
label (M_DROPTCTL) is detected as CONTROL=FAIL -- a product mutant reported under the apparatus reason, though `tctl rt`
also reds.  Is a CONTROL row the right home for a row that a product edit can red, or should `cased census` be a scored
detector row with a separate apparatus control?  And the PER-ROW KILL CENSUS lists the rows no leg reds: name any
non-CONTROL row in it that should have a measured kill and does not (table 1b was built for `cased wr` and `p1 p2 edge`).

**Q5 -- records.**  (a) The probe docstring says "NO KILL TABLE EXISTS FOR THIS REVISION" and calls every mutant outcome
PREDICTED.  After table 1 that sentence is a wrong record; the plan is to replace it with a citation of the preserved table
(a docstring-only edit -- the measured instrument is the frozen copy, md5 named in section 8).  Is that the right repair,
and is anything else in the docstring now false?  (b) Observation (b) in section 8: **12 red rows print "(FAILED FOR SOME
OTHER REASON)" although the stop IS the leg's edit** -- the second-pass rows ("pass 1 not completed" / "pass 1 silent") and
the non-word rows under M_WRFAULT/M_LENFAULT, where for M_LENFAULT they ARE the named channel.  The gate counts them red
either way.  Is the row text a wrong record that must change before shipping, or an accurate statement that the row's own
precondition failed?  If it must change, say to what -- and note any wording change is an instrument change that owes a
re-run of the table.

If, while verifying a claim, you found something ELSE -- say so.

## 10. Answer format

Open with your token (first line), then ONE line `VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>`, then
Q1..Q5 in order.  Number every finding `F<n>`, give it a severity (FLOOR BREACH / WRONG RECORD / DEFECT / NIT) and say
what would settle it if you could not.  Facts and flags; no restating the brief.
