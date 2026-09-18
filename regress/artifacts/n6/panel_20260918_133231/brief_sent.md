# `n6` ASSESS STAGE -- the seven missing seats, by OWNER DECISION 2026-09-18

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
The tree under review is `GXEMUL-SEC/src/`; ignore any other `src/` under the project root.  If you cannot read files,
that is expected -- the live code is inlined below.  **VERDICT LINE FIRST.**  A recent panel had seven of nine seats
confirm a premise the brief stated wrongly: **check the premises, not only the derivations.**

## THE ROW
`n6`: "The record says the footbridge host-halts were made graceful; the guest-reachable kills are not."  Round #220
removed two `exit(1)` calls from `src/devices/dev_footbridge.c` (the ARM DC21285 'Footbridge' model) and the project's
record (OUTSTANDING_BUGS / CHANGELOG summary of #218-#223) says the footbridge's guest-reachable `exit(1)` calls were made
graceful.  The assess stage ran 2/9 on 2026-08-15 (opus5, fable5: REAL); on 2026-08-30 fable5 (a READING seat, nothing
run) moved the round's shape.  The owner has re-opened the stage: you are the seven seats it never had.

## PREMISES -- STATED AS QUESTIONS; TEST THEM AGAINST THE INLINED CODE
P1. The record's claim of graceful footbridge host-halts is WRONG: live guest-reachable `exit(1)` calls remain.  True?
P2. The count: a comment-aware census finds 10 live `exit(` calls; TWO are in `DEVINIT(footbridge)` (construction-time,
    not guest-reachable), leaving EIGHT guest-access kills.  The row title says NINE; the ninth (a divide-by-zero on a
    guest-written timer encoding) was fixed by #432.  Count them yourself from the code below.
P3. Dispositions proposed (codex, 2026-08-30): ACCEPT at `+0x188` (IRQEnable is a documented READ -- DC21285 Table 7-10 --
    and the model already computes `d->irq_enable`, then dies: delete the kill, keep the value, no message).
    DECLINE + BOUNDED (LATCHED) ANNOUNCE for the invalid-DIRECTION accesses: WRITES to IRQStatus `+0x180`, FIQStatus
    `+0x280`, IRQRawStatus `+0x184`, FIQRawStatus `+0x284` (read-only), and the READ of IRQEnableClear `+0x18c`
    (write-only) -- which must additionally NOT return `d->irq_enable`.  DECLINE + ACCURATE ANNOUNCE ('unimplemented
    read', not 'invalid access') for SDRAM Base Address Mask `+0x100` / Offset `+0x104`, which are legal R/W registers
    the model does not implement.  Is that partition right?  Is `+0x18c` its own round-group?
P4. The 2026-08-30 reshaping (fable5): blast radius 1 arm -> 3; the gate's kill-arm probe row K1 (which today REQUIRES
    the `+0x188` read to kill the host, as its proof that guest code reached the device) must be REPOINTED -- to
    `+0x100` (one hop), not `+0x18c` as codex first said -- in the same commit as the ACCEPT fix, or that fix turns a
    green gate red by succeeding; and the accept row's oracle is the handler's OR-accumulation signature, not a readback.
    Is `+0x100` the right repoint target (it stops being a kill once group 3 lands)?

## QUESTIONS
Q1. Is the record defect (P1) real, and what exactly must the record correction say?
Q2. P2-P4: confirm or refute each, citing the code below.
Q3. What single round should be done FIRST, and what does its detector owe (accept rows, per-site latch bitmask vs one
    shared latch, a failability leg once the last kill is gone)?

## THE LIVE `exit(` SITES OF `src/devices/dev_footbridge.c` AT HEAD (each with 10 lines of context)
```c
---- line 565 ----
555: 
556: 	case UART_FLAGS:
557: 		odata = UART_TX_EMPTY;
558: 		break;
559: 
560: 	case IRQ_STATUS:
561: 		if (writeflag == MEM_READ)
562: 			odata = d->irq_status & d->irq_enable;
563: 		else {
564: 			fatal("[ WARNING: footbridge write to irq status? ]\n");
565: 			exit(1);
566: 		}
---- line 574 ----
564: 			fatal("[ WARNING: footbridge write to irq status? ]\n");
565: 			exit(1);
566: 		}
567: 		break;
568: 
569: 	case IRQ_RAW_STATUS:
570: 		if (writeflag == MEM_READ)
571: 			odata = d->irq_status;
572: 		else {
573: 			fatal("[ footbridge write to irq_raw_status ]\n");
574: 			exit(1);
575: 		}
---- line 589 ----
579: 		if (writeflag == MEM_WRITE) {
580: 			d->irq_enable |= idata;
581: 			if (d->irq_status & d->irq_enable)
582: 				INTERRUPT_ASSERT(d->irq);
583: 			else
584: 				INTERRUPT_DEASSERT(d->irq);
585: 		} else {
586: 			odata = d->irq_enable;
587: 			fatal("[ WARNING: footbridge read from "
588: 			    "ENABLE SET? ]\n");
589: 			exit(1);
590: 		}
---- line 604 ----
594: 		if (writeflag == MEM_WRITE) {
595: 			d->irq_enable &= ~idata;
596: 			if (d->irq_status & d->irq_enable)
597: 				INTERRUPT_ASSERT(d->irq);
598: 			else
599: 				INTERRUPT_DEASSERT(d->irq);
600: 		} else {
601: 			odata = d->irq_enable;
602: 			fatal("[ WARNING: footbridge read from "
603: 			    "ENABLE CLEAR? ]\n");
604: 			exit(1);
605: 		}
---- line 613 ----
603: 			    "ENABLE CLEAR? ]\n");
604: 			exit(1);
605: 		}
606: 		break;
607: 
608: 	case FIQ_STATUS:
609: 		if (writeflag == MEM_READ)
610: 			odata = d->fiq_status & d->fiq_enable;
611: 		else {
612: 			fatal("[ WARNING: footbridge write to fiq status? ]\n");
613: 			exit(1);
614: 		}
---- line 622 ----
612: 			fatal("[ WARNING: footbridge write to fiq status? ]\n");
613: 			exit(1);
614: 		}
615: 		break;
616: 
617: 	case FIQ_RAW_STATUS:
618: 		if (writeflag == MEM_READ)
619: 			odata = d->fiq_status;
620: 		else {
621: 			fatal("[ footbridge write to fiq_raw_status ]\n");
622: 			exit(1);
623: 		}
---- line 712 ----
702: 				d->pending_timer_interrupts[timer_nr] --;
703: 			}
704: 
705: 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
706: 		}
707: 		break;
708: 
709: 	case SDRAM_BA_MASK:
710: 		if (writeflag == MEM_READ) {
711: 			fatal("[ footbridge read from sdram_ba_mask ]\n");
712: 			exit(1);
713: 		} else {
---- line 737 ----
727: 			default:
728: 				fatal("[ footbridge write to sdram_ba_mask "
729: 				    "%#llx ]\n", (long long)idata);
730: 				break;
731: 			}
732: 		}
733: 		break;
734: 	case SDRAM_BA_OFFSET:
735: 		if (writeflag == MEM_READ) {
736: 			fatal("[ footbridge read from sdram_ba_offset ]\n");
737: 			exit(1);
738: 		} else {
---- line 841 ----
831: 	}
832: 
833: 	switch (devinit->machine->machine_type) {
834: 	case MACHINE_CATS:
835: 		snprintf(irq_path_isa, sizeof(irq_path_isa), "%s.10", irq_path);
836: 		break;
837: 	case MACHINE_NETWINDER:
838: 		snprintf(irq_path_isa, sizeof(irq_path_isa), "%s.11", irq_path);
839: 		break;
840: 	default:fatal("footbridge unimpl machine type\n");
841: 		exit(1);
842: 	}
---- line 877 ----
867: 	case MACHINE_NETWINDER:
868: 		bus_pci_add(devinit->machine, d->pcibus,
869: 		    devinit->machine->memory, 0xc0, 11, 0, "symphony_83c553");
870: 		bus_pci_add(devinit->machine, d->pcibus,
871: 		    devinit->machine->memory, 0xc0, 11, 1, "symphony_82c105");
872: 		memory_device_register(devinit->machine->memory,
873: 		    "footbridge_reset", 0x7c000338, 1,
874: 		    dev_footbridge_reset_access, d, DM_DEFAULT, NULL);
875: 		break;
876: 	default:fatal("footbridge: unimplemented machine type.\n");
877: 		exit(1);
878: 	}
```


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
