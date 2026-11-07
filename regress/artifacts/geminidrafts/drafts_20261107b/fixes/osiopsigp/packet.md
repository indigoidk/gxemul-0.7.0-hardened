# GXemul hardened fork -- DRAFT A FIX for one filed issue, `osiopsigp` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `osiopsigp`, state `open`, severity `MED`)

**title:** devices/dev_osiop.c -- an ISTAT SIGP write stops the script instead of waking WAIT RESELECT; CTEST2's SIGP mirror, the selection-timeout STO bit and SFBR are not modelled -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T84 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A7-40).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:1063-1083, :1043-1051, :693-700.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 04

## The code at the cited lines

### `src/devices/dev_osiop.c` around the row's cited line 1063 (HEAD 8d9df658, lines 943-1183)

```c
  943| 		case OSIOP_DSP:
  944| 		case OSIOP_DSPS:
  945| 		case OSIOP_SCRATCH:
  946| 		case OSIOP_ADDER:
  947| 			relative_addr = origofs;
  948| 			non1lenOk = 1;
  949| 
  950| 			uint32_t *p = (uint32_t*) &d->reg[origofs];
  951| 
  952| 			if (writeflag == MEM_WRITE)
  953| 				*p = idata;
  954| 			else
  955| 				odata = *p;
  956| 			
  957| 			break;
  958| 		}
  959| 	} else {
  960| 		/*  Byte access:  */
  961| 		oldreg = d->reg[relative_addr];
  962| 
  963| 		if (writeflag == MEM_WRITE)
  964| 			d->reg[relative_addr] = idata;
  965| 		else
  966| 			odata = oldreg;
  967| 	}
  968| 
  969| 	switch (relative_addr) {
  970| 
  971| 	case OSIOP_SCNTL0:
  972| 	case OSIOP_SCNTL1:
  973| 		break;
  974| 
  975| 	case OSIOP_SIEN:
  976| 		/*  Used by OpenBSD/mvme88k during probing:  */
  977| 		if (len == 4)
  978| 			non1lenOk = 1;
  979| 		if (writeflag == MEM_WRITE)
  980| 			osiop_reassert_interrupts(d);
  981| 		break;
  982| 
  983| 	case OSIOP_SCID:
  984| 		if (writeflag == MEM_WRITE && idata != oldreg) {
  985| 			/*  Guest-reachable via an ordinary register write,
  986| 			    and recoverable: warn once, ignore the ID change
  987| 			    and stop the script engine (the #118 pattern)
  988| 			    instead of exit(1). (Write-gated: on MEM_READ,
  989| 			    idata is not meaningful here.)  */
  990| 			static int warned = 0;
  991| 			if (!warned) {
  992| 				fatal("[ osiop: TODO: attempt to change SCID "
  993| 				    "(0x%02x -> 0x%02x); ignoring, stopping "
  994| 				    "script ]\n", (int) oldreg, (int) idata);
  995| 				warned = 1;
  996| 			}
  997| 			/*  Undo the generic byte store above (which only
  998| 			    happens for the non-32-bit access path):  */
  999| 			if (len != sizeof(uint32_t))
 1000| 				d->reg[relative_addr] = oldreg;
 1001| 			d->scripts_running = 0;
 1002| 		}
 1003| 		break;
 1004| 
 1005| 	case OSIOP_SBDL:
 1006| 		if (writeflag == MEM_WRITE)
 1007| 			fatal("[ osiop: SBDL set to 0x%x, but should be "
 1008| 			    "read-only! ]\n", (int) idata);
 1009| 		break;
 1010| 
 1011| 	case OSIOP_SBCL:
 1012| 		if (writeflag == MEM_WRITE) {
 1013| 			if (osiop_debug)
 1014| 				debug("[ osiop: SBCL set to 0x%x ]\n", (int) idata);
 1015| 		}
 1016| 		break;
 1017| 
 1018| 	case OSIOP_DSTAT:
 1019| 		/*  Cleared when read. Most likely not writable.  */
 1020| 		odata = d->reg[OSIOP_DSTAT];
 1021| 		d->reg[OSIOP_DSTAT] = OSIOP_DSTAT_DFE;
 1022| 		osiop_reassert_interrupts(d);
 1023| 		break;
 1024| 
 1025| 	case OSIOP_SSTAT0:
 1026| 		/*  Cleared when read. Most likely not writable.  */
 1027| 		odata = d->reg[OSIOP_SSTAT0];
 1028| 		d->reg[OSIOP_SSTAT0] = 0;
 1029| 		osiop_reassert_interrupts(d);
 1030| 		break;
 1031| 
 1032| 	case OSIOP_SSTAT1:
 1033| 	case OSIOP_SSTAT2:
 1034| 		break;
 1035| 		
 1036| 	case OSIOP_DSA:
 1037| 		if (writeflag == MEM_WRITE) {
 1038| 			if (osiop_debug)
 1039| 				debug("[ osiop: DSA set to 0x%x ]\n", (int) idata);
 1040| 		}
 1041| 		break;
 1042| 
 1043| 	case OSIOP_CTEST0:
 1044| 	case OSIOP_CTEST1:
 1045| 	case OSIOP_CTEST2:
 1046| 	case OSIOP_CTEST3:
 1047| 	case OSIOP_CTEST4:
 1048| 	case OSIOP_CTEST5:
 1049| 	case OSIOP_CTEST6:
 1050| 	case OSIOP_CTEST7:
 1051| 		break;
 1052| 
 1053| 	case OSIOP_TEMP:
 1054| 		if (writeflag == MEM_WRITE) {
 1055| 			if (osiop_debug)
 1056| 				debug("[ osiop: TEMP set to 0x%x ]\n", (int) idata);
 1057| 		}
 1058| 		break;
 1059| 
 1060| 	case OSIOP_DFIFO:
 1061| 		break;
 1062| 
 1063| 	case OSIOP_ISTAT:
 1064| 		if (writeflag == MEM_WRITE) {
 1065| 			if ((idata & 0x3f) != 0x00) {
 1066| 				/*  Unimplemented low ISTAT bits, reachable
 1067| 				    via an ordinary register write and
 1068| 				    recoverable: warn once, drop the
 1069| 				    unimplemented bits and stop the script
 1070| 				    engine (the #118 pattern) instead of
 1071| 				    exit(1).  */
 1072| 				static int warned = 0;
 1073| 				if (!warned) {
 1074| 					fatal("[ osiop: TODO: istat 0x%x; "
 1075| 					    "ignoring unimplemented low bits, "
 1076| 					    "stopping script ]\n", (int) idata);
 1077| 					warned = 1;
 1078| 				}
 1079| 				d->scripts_running = 0;
 1080| 				idata &= ~0x3f;
 1081| 			}
 1082| 
 1083| 			d->reg[relative_addr] = idata &
 1084| 			    ~(OSIOP_ISTAT_ABRT | OSIOP_ISTAT_RST);
 1085| 			osiop_reassert_interrupts(d);
 1086| 		}
 1087| 		break;
 1088| 
 1089| 	case OSIOP_CTEST8:
 1090| 		odata = (odata & 0xf) | (OSIOP_CHIP_REVISION << 4);
 1091| 		break;
 1092| 
 1093| 	case OSIOP_DBC:
 1094| 		break;
 1095| 
 1096| 	case OSIOP_DSP:
 1097| 		if (writeflag == MEM_WRITE) {
 1098| 			if (osiop_debug)
 1099| 				debug("[ osiop: DSP set to 0x%x ]\n", (int) idata);
 1100| 
 1101| 			d->scripts_running = 1;
 1102| 			osiop_execute_scripts(cpu, d);
 1103| 			osiop_reassert_interrupts(d);
 1104| 		}
 1105| 		break;
 1106| 
 1107| 	case OSIOP_DSPS:
 1108| 	case OSIOP_SCRATCH:
 1109| 		break;
 1110| 
 1111| 	case OSIOP_DMODE:
 1112| 		break;
 1113| 
 1114| 	case OSIOP_DIEN:
 1115| 		if (writeflag == MEM_WRITE)
 1116| 			osiop_reassert_interrupts(d);
 1117| 		break;
 1118| 
 1119| 	case OSIOP_DWT:
 1120| 		break;
 1121| 
 1122| 	case OSIOP_DCNTL:
 1123| 		if (writeflag == MEM_WRITE &&
 1124| 		    (idata & (OSIOP_DCNTL_SSM | OSIOP_DCNTL_LLM |
 1125| 		    OSIOP_DCNTL_STD))) {
 1126| 			/*  Unimplemented DCNTL modes (single-step, low-level,
 1127| 			    manual start-DMA), reachable via an ordinary
 1128| 			    register write and recoverable: warn once and stop
 1129| 			    the script engine (the #118 pattern) instead of
 1130| 			    exit(1). The message includes the value, so the
 1131| 			    specific bit (SSM/LLM/STD) is identifiable.  */
 1132| 			static int warned = 0;
 1133| 			if (!warned) {
 1134| 				fatal("[ osiop: TODO: DCNTL 0x%02x (SSM/LLM/"
 1135| 				    "STD unimplemented); stopping script ]\n",
 1136| 				    (int) idata);
 1137| 				warned = 1;
 1138| 			}
 1139| 			d->scripts_running = 0;
 1140| 		}
 1141| 		break;
 1142| 
 1143| 	default:
 1144| 		if (writeflag == MEM_READ) {
 1145| 			fatal("[ osiop: read from 0x%02lx ]\n",
 1146| 			    (long)relative_addr);
 1147| 		} else {
 1148| 			fatal("[ osiop: write to  0x%02lx: 0x%02x ]\n",
 1149| 			    (long)relative_addr, (int)idata);
 1150| 		}
 1151| 
 1152| 		exit(1);
 1153| 	}
 1154| 
 1155| 	if (len != 1 && !non1lenOk) {
 1156| 		/*  Unusual access width from the guest, on a register where
 1157| 		    only byte access is implemented: recoverable, so warn once
 1158| 		    and stop the script engine (the #118 pattern), completing
 1159| 		    the access instead of exit(1).  */
 1160| 		static int warned = 0;
 1161| 		if (!warned) {
 1162| 			fatal("[ osiop: TODO: len != 1, addr 0x%0x; "
 1163| 			    "stopping script ]\n", (int)relative_addr);
 1164| 			warned = 1;
 1165| 		}
 1166| 		d->scripts_running = 0;
 1167| 	}
 1168| 
 1169| 	if (writeflag == MEM_READ)
 1170| 		memory_writemax64(cpu, data, len, odata);
 1171| 
 1172| 	return 1;
 1173| }
 1174| 
 1175| 
 1176| DEVINIT(osiop)
 1177| {
 1178| 	struct osiop_data *d;
 1179| 
 1180| 	CHECK_ALLOCATION(d = (struct osiop_data *) malloc(sizeof(struct osiop_data)));
 1181| 	memset(d, 0, sizeof(struct osiop_data));
 1182| 
 1183| 	/*  Set up initial device register values:  */
```

## The data structures those files define (every field that exists)

### `src/devices/dev_osiop.c` -- `struct osiop_data {` (HEAD lines 75-99)

```c
   75| struct osiop_data {
   76| 	struct interrupt	irq;
   77| 	int			asserted;
   78| 	
   79| 	int			scripts_running;
   80| 
   81| 	/*  Current transfer:  */
   82| 	int			selected_id;
   83| 	struct scsi_transfer	*xferp;
   84| 	size_t			data_offset;
   85| 
   86| 	/*  Cached emulated physical RAM page lookup:  */
   87| 	uint32_t		last_phys_page;
   88| 	uint8_t			*last_host_page;
   89| 	int			hostpage_fault_warned;	/* #118: warn once */
   90| 
   91| 	/*  ALU:  */
   92| 	int			carry;
   93| 	
   94| 	/*
   95| 	 *  Most of these are byte-addressed, but some are not. (Note: For
   96| 	 *  convenience, 32-bit words are stored in host byte order!)
   97| 	 */
   98| 	uint8_t			reg[OSIOP_NREGS];
   99| };
```

RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_OSIOPSIGP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
STILL PRESENT: UNSETTLED -- src/devices/dev_osiop.c:1065
I cannot write a fix because the provided code does not contain the macro definitions for the SIGP bit in ISTAT and CTEST2, the STO bit, or the SFBR register. I would need to see the header file that defines the OSIOP constants (e.g., `OSIOP_ISTAT_SIGP`, `OSIOP_SFBR`) to properly adjust the bitmasks at line 1065 and correctly model the registers, as well as the function/logic to wake the script engine from a WAIT RESELECT state.
FIXDRAFT_OSIOPSIGP: UNSETTLED PRESENT, 0 EDITS
```

## What you said was missing, from HEAD

### `src/include/thirdparty/osiopreg.h` lines 318-334 (where HEAD defines `OSIOP_ISTAT_SIGP`)

```c
  318| 
  319| #define OSIOP_DFIFO_FLF		0x80	/* Flush (spill) DMA FIFO */
  320| #define OSIOP_DFIFO_BO		0x7f	/* FIFO byte offset counter */
  321| 
  322| /* Interrupt status register (istat) */
  323| 
  324| #define OSIOP_ISTAT_ABRT	0x80	/* Abort operation */
  325| #define OSIOP_ISTAT_RST		0x40	/* Software reset */
  326| #define OSIOP_ISTAT_SIGP	0x20	/* Signal process */
  327| #define OSIOP_ISTAT_RES		0x10
  328| #define OSIOP_ISTAT_CON		0x08	/* Connected */
  329| #define OSIOP_ISTAT_RES1	0x04
  330| #define OSIOP_ISTAT_SIP		0x02	/* SCSI Interrupt pending */
  331| #define OSIOP_ISTAT_DIP		0x01	/* DMA Interrupt pending */
  332| 
  333| /* Chip test register 8 (ctest8) */
  334| 
```

### `src/include/thirdparty/osiopreg.h` lines 60-76 (where HEAD defines `OSIOP_SFBR`)

```c
   60| #define OSIOP_SDID	(0x00+BL2)	/* rw: SCSI destination ID */
   61| #define OSIOP_SIEN	(0x00+BL3)	/* rw: SCSI interrupt enable */
   62| 
   63| #define OSIOP_SCID	(0x04+BL0)	/* rw: SCSI Chip ID reg */
   64| #define OSIOP_SXFER	(0x04+BL1)	/* rw: SCSI Transfer reg */
   65| #define OSIOP_SODL	(0x04+BL2)	/* rw: SCSI Output Data Latch */
   66| #define OSIOP_SOCL	(0x04+BL3)	/* rw: SCSI Output Control Latch */
   67| 
   68| #define OSIOP_SFBR	(0x08+BL0)	/* ro: SCSI First Byte Received */
   69| #define OSIOP_SIDL	(0x08+BL1)	/* ro: SCSI Input Data Latch */
   70| #define OSIOP_SBDL	(0x08+BL2)	/* ro: SCSI Bus Data Lines */
   71| #define OSIOP_SBCL	(0x08+BL3)	/* rw: SCSI Bus Control Lines */
   72| 
   73| #define OSIOP_DSTAT	(0x0c+BL0)	/* ro: DMA status */
   74| #define OSIOP_SSTAT0	(0x0c+BL1)	/* ro: SCSI status reg 0 */
   75| #define OSIOP_SSTAT1	(0x0c+BL2)	/* ro: SCSI status reg 1 */
   76| #define OSIOP_SSTAT2	(0x0c+BL3)	/* ro: SCSI status reg 2 */
```


Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.
