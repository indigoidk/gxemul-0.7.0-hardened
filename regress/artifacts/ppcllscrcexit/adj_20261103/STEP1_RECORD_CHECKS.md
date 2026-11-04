# #579 -- MYTHOS_F2R step 1, the record checks (run 2026-11-04 16:57Z by the main loop, Opus 5.5)

MYTHOS_F2R part 23 (D1, the L3 item) and part 30 (F2's weakest point) require these lines inlined before the comments ship, and a HOLD if any disagrees.  None disagrees.

## Book I v2.01 (_scratchpad/ppc_uisa_book1_v201.txt, 783679 bytes)
```
430:     handler, the system data storage error handler,       1.5.2 Reserved Fields
431:     etc.
432:                                                           Reserved fields in instructions are ignored by the
433:  Each bit and field in instructions, and in status        processor.
434:     and control registers (e.g., XER, FPSCR) and
435:     Special Purpose Registers, is either defined or       The handling of reserved bits in System Registers
436:     reserved.                                             (e.g., XER, FPSCR) is implementation-dependent.
...
1107: 1.9.2 Invalid Instruction Forms                           1.11 Exceptions
1108: 
1109: Some of the defined instructions can be coded in a        There are two kinds of exception, those caused
1110: form that is invalid. An instruction form is invalid if   directly by the execution of an instruction and those
1111: one or more fields of the instruction, excluding the      caused by an asynchronous event. In either case, the
1112: opcode fields and reserved fields, are coded incor-       exception may cause one of several components of
1113: rectly in a manner that can be deduced by examining       the system software to be invoked.
1114: only the instruction encoding.
1115:                                                           The exceptions that can be caused directly by the
1116: Any attempt to execute an invalid form of an instruc-     execution of an instruction include the following:
1117: tion will either cause the system illegal instruction
1118: error handler to be invoked or yield boundedly unde-        an attempt to execute an illegal instruction, or an
1119: fined results. Exceptions to this rule are stated in the        attempt by an application program to execute a
1120: instruction descriptions.                                       "privileged" instruction (see Book III, PowerPC
```
Right column :430-433, §1.5.2 Reserved Fields: "Reserved fields in instructions are ignored by the processor."  Left column :1107-1120, §1.9.2 Invalid Instruction Forms: a form is invalid only if fields "excluding the opcode fields and reserved fields" are coded incorrectly; an invalid form "will either cause the system illegal instruction error handler to be invoked or yield boundedly undefined results. Exceptions to this rule are stated in the instruction descriptions."

## Book II v2.01 (_scratchpad/ppc_vea_book2_v201.txt, 183402 bytes)
```
1259: Load Word And Reserve Indexed                         Load Doubleword And Reserve Indexed
1260: X-form                                                X-form
1261: 
1262: lwarx       RT,RA,RB                                  ldarx       RT,RA,RB
1263: 
1264:    31       RT      RA          RB      20  /            31       RT      RA          RB      84  /
1265: 
1266: 0      6        11          16      21      31        0      6        11          16      21      31
...
1301: stwcx.         RS,RA,RB
1302: 
1303:                                                           stdcx.         RS,RA,RB
1304: 
1305:    31          RS RA RB                  150  1
1306: 
1307: 0           6         11     16     21        31             31          RS RA RB                  214  1
1308: 
1309:                                                           0           6         11     16     21        31
```
lwarx/ldarx bit 31 is "/" (reserved); stwcx./stdcx. bit 31 is "1".  The stwcx./stdcx. description (:1341-1371) states NO exception to §1.9.2 for the bit-clear form; its one "boundedly undefined" (:1366-1368) is about EA alignment.

## memory_rw.c:600-645 (GXEMUL-SEC working tree)
```
603: 				if (res <= 0 && !no_exceptions) {
604: 					debug("[ %s device '%s' addr %08lx "
605: 					    "failed ]\n", writeflag?
606: 					    "writing to" : "reading from",
607: 					    mem->devices[i].name, (long)paddr);
608: #ifdef MEM_MIPS
609: 					mips_cpu_exception(cpu,
610: 					    cache == CACHE_INSTRUCTION?
611: 					    EXCEPTION_IBE : EXCEPTION_DBE,
612: 					    0, vaddr, 0, 0, 0, 0);
613: #endif
614: #ifdef MEM_M88K
... (lines 615-641: the #570 M88K arm) ...
642: #endif
643: 					return MEMORY_ACCESS_FAILED;
644: 				}
645: 				goto do_return_ok;
```
Only MEM_MIPS and MEM_M88K raise on a failed device access; there is NO PowerPC branch, so the F2 replacement's "(a failed device access raises no PPC exception)" is true as written.
