# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ioasic3minscc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ioasic3minscc`, state `open`)

**title:** devices/dev_dec_ioasic.c -- 3MIN SCC transmit/receive DMA is under `#if 0` -- WRONG-RESULT (Ultrix 4.5 serial console waits forever)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T67 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-47).  Source URLs: https://github.com/rpajarola/gxemul/commit/7aeae85458685ce7628f0ca5b6bcf9ebe611f393.  Our site at de8c7547: src/devices/dev_dec_ioasic.c:180-258.  Portable fix: yes -- port rpajarola 7aeae85.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- lines exceeding 79 columns.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_dec_ioasic.c b/src/devices/dev_dec_ioasic.c
index 6b2ed1f3..51684a02 100644
--- a/src/devices/dev_dec_ioasic.c
+++ b/src/devices/dev_dec_ioasic.c
@@ -177,85 +177,57 @@ DEVICE_ACCESS(dec_ioasic)
 		debug("[ dec_ioasic: %s CSR, data=0x%08" PRIx64 " ]\n",
 			writeflag == MEM_WRITE ? "write to" : "read from",
 			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
-#if 0
+		/* #NNN: uncomment and port to explicit fields */
 		if (writeflag == MEM_WRITE) {
-			csr = d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) / 0x10];
+			uint32_t csr_val = d->csr;
 
-			d->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) / 0x10] &=
-			    ~IOASIC_INTR_T2_PAGE_END;
+			d->intr &= ~IOASIC_INTR_T2_PAGE_END;
 
-			if (csr & IOASIC_CSR_DMAEN_T2) {
-				/*  Transmit data:  */
-				curptr = (d->reg[(IOASIC_SCC_T2_DMAPTR -
-				    IOASIC_SLOT_1_START) / 0x10] >> 3)
-				    | ((d->reg[(IOASIC_SCC_T2_DMAPTR -
-				    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);
-				dma_len = 0x1000 - (curptr & 0xffc);
+			if (csr_val & IOASIC_CSR_DMAEN_T2) {
+				uint64_t curptr = (d->isdn_x_dmaptr >> 3)
+				    | ((d->isdn_x_dmaptr & 0x1f) << 29);
+				int dma_len = 0x1000 - (curptr & 0xffc);
 
-				if ((curptr & 0xfff) == 0)
-					break;
+				if ((curptr & 0xfff) != 0) {
+					if (d->dma_func[3] != NULL) {
+						d->dma_func[3](cpu,
+						    d->dma_func_extra[3], curptr,
+						    dma_len, 1);
+					}
 
-				if (d->dma_func[3] != NULL) {
-					d->dma_func[3](cpu,
-					    d->dma_func_extra[3], curptr,
-					    dma_len, 1);
-				} else
-					fatal("[ dec_ioasic: DMA tx: data @ "
-					    "%08x, len %i bytes, but no "
-					    "handler? ]\n", (int)curptr,
-					    dma_len);
-
-				/*  and signal the end of page:  */
-				d->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) /
-				    0x10] |= IOASIC_INTR_T2_PAGE_END;
-
-				d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) /
-				    0x10] &= ~IOASIC_CSR_DMAEN_T2;
-				curptr |= 0xfff;
-				curptr ++;
-
-				d->reg[(IOASIC_SCC_T2_DMAPTR -
-				    IOASIC_SLOT_1_START) / 0x10] = ((curptr <<
-				    3) & ~0x1f) | ((curptr >> 29) & 0x1f);
+					d->intr |= IOASIC_INTR_T2_PAGE_END;
+					d->csr &= ~IOASIC_CSR_DMAEN_T2;
+					curptr |= 0xfff;
+					curptr ++;
+
+					d->isdn_x_dmaptr = ((curptr << 3) & ~0x1f)
+					    | ((curptr >> 29) & 0x1f);
+				}
 			}
 
-			if (csr & IOASIC_CSR_DMAEN_R2) {
-				/*  Receive data:  */
-				curptr = (d->reg[(IOASIC_SCC_R2_DMAPTR -
-				    IOASIC_SLOT_1_START) / 0x10] >> 3)
-				    | ((d->reg[(IOASIC_SCC_R2_DMAPTR -
-				    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);
-				dma_len = 0x1000 - (curptr & 0xffc);
+			if (csr_val & IOASIC_CSR_DMAEN_R2) {
+				uint64_t curptr = (d->isdn_r_dmaptr >> 3)
+				    | ((d->isdn_r_dmaptr & 0x1f) << 29);
+				int dma_len = 0x1000 - (curptr & 0xffc);
+				int dma_res = 0;
 
-				dma_res = 0;
 				if (d->dma_func[3] != NULL) {
 					dma_res = d->dma_func[3](cpu,
 					    d->dma_func_extra[3], curptr,
 					    dma_len, 0);
-				} else
-					fatal("[ dec_ioasic: DMA tx: data @ "
-					    "%08x, len %i bytes, but no "
-					    "handler? ]\n", (int)curptr,
-					    dma_len);
+				}
 
-				/*  and signal the end of page:  */
 				if (dma_res > 0) {
 					if ((curptr & 0x800) != ((curptr +
 					    dma_res) & 0x800))
-						d->reg[(IOASIC_INTR -
-						    IOASIC_SLOT_1_START) / 0x10]
-						    |= IOASIC_INTR_R2_HALF_PAGE;
+						d->intr |= IOASIC_INTR_R2_HALF_PAGE;
 					curptr += dma_res;
-/*					d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START
-					   ) / 0x10] &= ~IOASIC_CSR_DMAEN_R2; */
-					d->reg[(IOASIC_SCC_R2_DMAPTR -
-					    IOASIC_SLOT_1_START) / 0x10] =
-					    ((curptr << 3) & ~0x1f) | ((curptr
-					    >> 29) & 0x1f);
+					d->isdn_r_dmaptr = ((curptr << 3) & ~0x1f)
+					    | ((curptr >> 29) & 0x1f);
 				}
 			}
+			dec_ioasic_reassert(d);
 		}
-#endif
 		break;
 
 	case IOASIC_INTR:
```

## Every edited function, after the fix

### `src/devices/dev_dec_ioasic.c` -- post-edit lines 66-421 (`+` marks a line the diff added or the point of a deletion)

```c
   66|  DEVICE_ACCESS(dec_ioasic)
   67|  {
   68|  	struct dec_ioasic_data *d = (struct dec_ioasic_data *) extra;
   69|  	uint64_t idata = 0, odata = 0;
   70|  	// uint64_t curptr;
   71|  	// uint32_t csr;
   72|  	// int dma_len, dma_res, regnr;
   73|  
   74|  	if (writeflag == MEM_WRITE)
   75|  		idata = memory_readmax64(cpu, data, len);
   76|  
   77|  	switch (relative_addr) {
   78|  	
   79|  	case 0:
   80|  		/*  NetBSD/pmax and OpenBSD/pmax read from this address.  */
   81|  		break;
   82|  
   83|  	case IOASIC_SCSI_DMAPTR:
   84|  		if (writeflag == MEM_WRITE)
   85|  			d->scsi_dmaptr = idata;
   86|  		else
   87|  			odata = d->scsi_dmaptr;
   88|  
   89|  		debug("[ dec_ioasic: %s SCSI_DMAPTR, data=0x%08" PRIx64 " ]\n",
   90|  			writeflag == MEM_WRITE ? "write to" : "read from",
   91|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
   92|  		break;
   93|  
   94|  	case IOASIC_SCSI_NEXTPTR:
   95|  		if (writeflag == MEM_WRITE)
   96|  			d->scsi_nextptr = idata;
   97|  		else
   98|  			odata = d->scsi_nextptr;
   99|  
  100|  		debug("[ dec_ioasic: %s SCSI_NEXTPTR, data=0x%08" PRIx64 " ]\n",
  101|  			writeflag == MEM_WRITE ? "write to" : "read from",
  102|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  103|  		break;
  104|  
  105|  	case IOASIC_LANCE_DMAPTR:
  106|  		if (writeflag == MEM_WRITE)
  107|  			d->lance_dmaptr = idata;
  108|  		else
  109|  			odata = d->lance_dmaptr;
  110|  
  111|  		debug("[ dec_ioasic: %s LANCE_DMAPTR, data=0x%08" PRIx64 " ]\n",
  112|  			writeflag == MEM_WRITE ? "write to" : "read from",
  113|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  114|  		break;
  115|  
  116|  	case IOASIC_FLOPPY_DMAPTR:
  117|  		if (writeflag == MEM_WRITE)
  118|  			d->floppy_dmaptr = idata;
  119|  		else
  120|  			odata = d->floppy_dmaptr;
  121|  
  122|  		debug("[ dec_ioasic: %s FLOPPY_DMAPTR, data=0x%08" PRIx64 " ]\n",
  123|  			writeflag == MEM_WRITE ? "write to" : "read from",
  124|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  125|  		break;
  126|  
  127|  	case IOASIC_ISDN_X_DMAPTR:
  128|  		if (writeflag == MEM_WRITE)
  129|  			d->isdn_x_dmaptr = idata;
  130|  		else
  131|  			odata = d->isdn_x_dmaptr;
  132|  
  133|  		debug("[ dec_ioasic: %s ISDN_X_DMAPTR, data=0x%08" PRIx64 " ]\n",
  134|  			writeflag == MEM_WRITE ? "write to" : "read from",
  135|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  136|  		break;
  137|  
  138|  	case IOASIC_ISDN_X_NEXTPTR:
  139|  		if (writeflag == MEM_WRITE)
  140|  			d->isdn_x_nextptr = idata;
  141|  		else
  142|  			odata = d->isdn_x_nextptr;
  143|  
  144|  		debug("[ dec_ioasic: %s ISDN_X_NEXTPTR, data=0x%08" PRIx64 " ]\n",
  145|  			writeflag == MEM_WRITE ? "write to" : "read from",
  146|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  147|  		break;
  148|  
  149|  	case IOASIC_ISDN_R_DMAPTR:
  150|  		if (writeflag == MEM_WRITE)
  151|  			d->isdn_r_dmaptr = idata;
  152|  		else
  153|  			odata = d->isdn_r_dmaptr;
  154|  
  155|  		debug("[ dec_ioasic: %s ISDN_R_DMAPTR, data=0x%08" PRIx64 " ]\n",
  156|  			writeflag == MEM_WRITE ? "write to" : "read from",
  157|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  158|  		break;
  159|  
  160|  	case IOASIC_ISDN_R_NEXTPTR:
  161|  		if (writeflag == MEM_WRITE)
  162|  			d->isdn_r_nextptr = idata;
  163|  		else
  164|  			odata = d->isdn_r_nextptr;
  165|  
  166|  		debug("[ dec_ioasic: %s ISDN_R_NEXTPTR, data=0x%08" PRIx64 " ]\n",
  167|  			writeflag == MEM_WRITE ? "write to" : "read from",
  168|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  169|  		break;
  170|  
  171|  	case IOASIC_CSR:
  172|  		if (writeflag == MEM_WRITE)
  173|  			d->csr = idata;
  174|  		else
  175|  			odata = d->csr;
  176|  
  177|  		debug("[ dec_ioasic: %s CSR, data=0x%08" PRIx64 " ]\n",
  178|  			writeflag == MEM_WRITE ? "write to" : "read from",
  179|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  180|+ 		/* #NNN: uncomment and port to explicit fields */
  181|  		if (writeflag == MEM_WRITE) {
  182|+ 			uint32_t csr_val = d->csr;
  183|  
  184|+ 			d->intr &= ~IOASIC_INTR_T2_PAGE_END;
  185|  
  186|+ 			if (csr_val & IOASIC_CSR_DMAEN_T2) {
  187|+ 				uint64_t curptr = (d->isdn_x_dmaptr >> 3)
  188|+ 				    | ((d->isdn_x_dmaptr & 0x1f) << 29);
  189|+ 				int dma_len = 0x1000 - (curptr & 0xffc);
  190|  
  191|+ 				if ((curptr & 0xfff) != 0) {
  192|+ 					if (d->dma_func[3] != NULL) {
  193|+ 						d->dma_func[3](cpu,
  194|+ 						    d->dma_func_extra[3], curptr,
  195|+ 						    dma_len, 1);
  196|+ 					}
  197|  
  198|+ 					d->intr |= IOASIC_INTR_T2_PAGE_END;
  199|+ 					d->csr &= ~IOASIC_CSR_DMAEN_T2;
  200|+ 					curptr |= 0xfff;
  201|+ 					curptr ++;
  202|+ 
  203|+ 					d->isdn_x_dmaptr = ((curptr << 3) & ~0x1f)
  204|+ 					    | ((curptr >> 29) & 0x1f);
  205|+ 				}
  206|  			}
  207|  
  208|+ 			if (csr_val & IOASIC_CSR_DMAEN_R2) {
  209|+ 				uint64_t curptr = (d->isdn_r_dmaptr >> 3)
  210|+ 				    | ((d->isdn_r_dmaptr & 0x1f) << 29);
  211|+ 				int dma_len = 0x1000 - (curptr & 0xffc);
  212|+ 				int dma_res = 0;
  213|  
  214|+ 				if (d->dma_func[3] != NULL) {
  215|  					dma_res = d->dma_func[3](cpu,
  216|  					    d->dma_func_extra[3], curptr,
  217|  					    dma_len, 0);
  218|+ 				}
  219|  
  220|+ 				if (dma_res > 0) {
  221|  					if ((curptr & 0x800) != ((curptr +
  222|  					    dma_res) & 0x800))
  223|+ 						d->intr |= IOASIC_INTR_R2_HALF_PAGE;
  224|  					curptr += dma_res;
  225|+ 					d->isdn_r_dmaptr = ((curptr << 3) & ~0x1f)
  226|+ 					    | ((curptr >> 29) & 0x1f);
  227|  				}
  228|  			}
  229|+ 			dec_ioasic_reassert(d);
  230|  		}
  231|+ 		break;
  232|  
  233|  	case IOASIC_INTR:
  234|  		if (writeflag == MEM_WRITE) {
  235|  			/*  Clear bits on write?  */
  236|  			d->intr &= ~idata;
  237|  			dec_ioasic_reassert(d);
  238|  		} else {
  239|  			odata = d->intr;
  240|  
  241|  			/*  Note/TODO: How about other models than KN03?  */
  242|  			//if (!d->rackmount_flag)
  243|  			//	odata |= KN03_INTR_PROD_JUMPER;
  244|  		}
  245|  
  246|  		debug("[ dec_ioasic: %s INTR, data=0x%08" PRIx64 " ]\n",
  247|  			writeflag == MEM_WRITE ? "write to" : "read from",
  248|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  249|  
  250|  		break;
  251|  
  252|  	case IOASIC_IMSK:
  253|  		if (writeflag == MEM_WRITE) {
  254|  			d->imsk = idata;
  255|  			dec_ioasic_reassert(d);
  256|  		} else {
  257|  			odata = d->imsk;
  258|  		}
  259|  
  260|  		debug("[ dec_ioasic: %s IMSK, data=0x%08" PRIx64 " ]\n",
  261|  			writeflag == MEM_WRITE ? "write to" : "read from",
  262|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  263|  		break;
  264|  
  265|  	case IOASIC_ISDN_X_DATA:
  266|  		if (writeflag == MEM_WRITE)
  267|  			d->isdn_x_data = idata;
  268|  		else
  269|  			odata = d->isdn_x_data;
  270|  
  271|  		debug("[ dec_ioasic: %s ISDN_X_DATA, data=0x%08" PRIx64 " ]\n",
  272|  			writeflag == MEM_WRITE ? "write to" : "read from",
  273|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  274|  		break;
  275|  
  276|  	case IOASIC_ISDN_R_DATA:
  277|  		if (writeflag == MEM_WRITE)
  278|  			d->isdn_r_data = idata;
  279|  		else
  280|  			odata = d->isdn_r_data;
  281|  
  282|  		debug("[ dec_ioasic: %s ISDN_R_DATA, data=0x%08" PRIx64 " ]\n",
  283|  			writeflag == MEM_WRITE ? "write to" : "read from",
  284|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  285|  		break;
  286|  
  287|  	case IOASIC_LANCE_DECODE:
  288|  		if (writeflag == MEM_WRITE)
  289|  			d->lance_decode = idata;
  290|  		else
  291|  			odata = d->lance_decode;
     | [... lines 292-391 not shown ...]
  392|  	case 0x0f004:
  393|  	case 0x1f008:
  394|  	case 0x2f00c:
  395|  	case 0x3f010:
  396|  	case 0x4f014:
  397|  	case 0x5f018:
  398|  	case 0x6f01c:
  399|  	case 0x7f020:
  400|  	case 0x8f024:
  401|  	case 0x9f028:
  402|  	case 0xaf02c:
  403|  	case 0xbf030:
  404|  		break;
  405|  
  406|  	default:
  407|  		if (writeflag == MEM_WRITE)
  408|  			fatal("[ dec_ioasic: unimplemented write to address "
  409|  			    "0x%llx, data=0x%08llx ]\n",
  410|  			    (long long)relative_addr, (long long)idata);
  411|  		else
  412|  			fatal("[ dec_ioasic: unimplemented read from address "
  413|  			    "0x%llx ]\n", (long long)relative_addr);
  414|  		// exit(1);
  415|  	}
  416|  
  417|  	if (writeflag == MEM_READ)
  418|  		memory_writemax64(cpu, data, len, odata);
  419|  
  420|  	return 1;
  421|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_IOASIC3MINSCC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_IOASIC3MINSCC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
