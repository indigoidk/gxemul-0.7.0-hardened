# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ioasic3minscc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ioasic3minscc`, state `open`)

**title:** devices/dev_dec_ioasic.c -- 3MIN SCC transmit/receive DMA is under `#if 0` -- WRONG-RESULT (Ultrix 4.5 serial console waits forever)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T67 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-47).  Source URLs: https://github.com/rpajarola/gxemul/commit/7aeae85458685ce7628f0ca5b6bcf9ebe611f393.  Our site at de8c7547: src/devices/dev_dec_ioasic.c:180-258.  Portable fix: yes -- port rpajarola 7aeae85.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_dec_ioasic.c` -- AT HEAD, lines 66-449 (`*` marks a line your previous draft changed)

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
  180|* #if 0
  181|* 		if (writeflag == MEM_WRITE) {
  182|* 			csr = d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) / 0x10];
  183|* 
  184|* 			d->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) / 0x10] &=
  185|* 			    ~IOASIC_INTR_T2_PAGE_END;
  186|* 
  187|* 			if (csr & IOASIC_CSR_DMAEN_T2) {
  188|* 				/*  Transmit data:  */
  189|* 				curptr = (d->reg[(IOASIC_SCC_T2_DMAPTR -
  190|* 				    IOASIC_SLOT_1_START) / 0x10] >> 3)
  191|* 				    | ((d->reg[(IOASIC_SCC_T2_DMAPTR -
  192|* 				    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);
  193|* 				dma_len = 0x1000 - (curptr & 0xffc);
  194|* 
  195|* 				if ((curptr & 0xfff) == 0)
  196|* 					break;
  197|* 
  198|* 				if (d->dma_func[3] != NULL) {
  199|* 					d->dma_func[3](cpu,
  200|* 					    d->dma_func_extra[3], curptr,
  201|* 					    dma_len, 1);
  202|* 				} else
  203|* 					fatal("[ dec_ioasic: DMA tx: data @ "
  204|* 					    "%08x, len %i bytes, but no "
  205|* 					    "handler? ]\n", (int)curptr,
  206|* 					    dma_len);
  207|* 
  208|* 				/*  and signal the end of page:  */
  209|* 				d->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) /
  210|* 				    0x10] |= IOASIC_INTR_T2_PAGE_END;
  211|* 
  212|* 				d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) /
  213|* 				    0x10] &= ~IOASIC_CSR_DMAEN_T2;
  214|* 				curptr |= 0xfff;
  215|* 				curptr ++;
  216|* 
  217|* 				d->reg[(IOASIC_SCC_T2_DMAPTR -
  218|* 				    IOASIC_SLOT_1_START) / 0x10] = ((curptr <<
  219|* 				    3) & ~0x1f) | ((curptr >> 29) & 0x1f);
  220|* 			}
  221|  
  222|* 			if (csr & IOASIC_CSR_DMAEN_R2) {
  223|* 				/*  Receive data:  */
  224|* 				curptr = (d->reg[(IOASIC_SCC_R2_DMAPTR -
  225|* 				    IOASIC_SLOT_1_START) / 0x10] >> 3)
  226|* 				    | ((d->reg[(IOASIC_SCC_R2_DMAPTR -
  227|* 				    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);
  228|* 				dma_len = 0x1000 - (curptr & 0xffc);
  229|* 
  230|* 				dma_res = 0;
  231|  				if (d->dma_func[3] != NULL) {
  232|  					dma_res = d->dma_func[3](cpu,
  233|  					    d->dma_func_extra[3], curptr,
  234|  					    dma_len, 0);
  235|* 				} else
  236|* 					fatal("[ dec_ioasic: DMA tx: data @ "
  237|* 					    "%08x, len %i bytes, but no "
  238|* 					    "handler? ]\n", (int)curptr,
  239|* 					    dma_len);
  240|* 
  241|* 				/*  and signal the end of page:  */
  242|  				if (dma_res > 0) {
  243|* 					if ((curptr & 0x800) != ((curptr +
  244|* 					    dma_res) & 0x800))
  245|* 						d->reg[(IOASIC_INTR -
  246|* 						    IOASIC_SLOT_1_START) / 0x10]
  247|* 						    |= IOASIC_INTR_R2_HALF_PAGE;
  248|* 					curptr += dma_res;
  249|* /*					d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START
  250|* 					   ) / 0x10] &= ~IOASIC_CSR_DMAEN_R2; */
  251|* 					d->reg[(IOASIC_SCC_R2_DMAPTR -
  252|* 					    IOASIC_SLOT_1_START) / 0x10] =
  253|* 					    ((curptr << 3) & ~0x1f) | ((curptr
  254|* 					    >> 29) & 0x1f);
  255|* 				}
  256|  			}
  257|* 		}
  258|* #endif
  259|  		break;
  260|  
  261|  	case IOASIC_INTR:
  262|  		if (writeflag == MEM_WRITE) {
  263|  			/*  Clear bits on write?  */
  264|  			d->intr &= ~idata;
  265|  			dec_ioasic_reassert(d);
  266|  		} else {
  267|  			odata = d->intr;
  268|  
  269|  			/*  Note/TODO: How about other models than KN03?  */
  270|  			//if (!d->rackmount_flag)
  271|  			//	odata |= KN03_INTR_PROD_JUMPER;
  272|  		}
  273|  
  274|  		debug("[ dec_ioasic: %s INTR, data=0x%08" PRIx64 " ]\n",
  275|  			writeflag == MEM_WRITE ? "write to" : "read from",
  276|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  277|  
  278|  		break;
  279|  
  280|  	case IOASIC_IMSK:
  281|  		if (writeflag == MEM_WRITE) {
  282|  			d->imsk = idata;
  283|  			dec_ioasic_reassert(d);
  284|  		} else {
  285|  			odata = d->imsk;
  286|  		}
  287|  
  288|  		debug("[ dec_ioasic: %s IMSK, data=0x%08" PRIx64 " ]\n",
  289|  			writeflag == MEM_WRITE ? "write to" : "read from",
  290|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  291|  		break;
  292|  
  293|  	case IOASIC_ISDN_X_DATA:
  294|  		if (writeflag == MEM_WRITE)
  295|  			d->isdn_x_data = idata;
  296|  		else
  297|  			odata = d->isdn_x_data;
  298|  
  299|  		debug("[ dec_ioasic: %s ISDN_X_DATA, data=0x%08" PRIx64 " ]\n",
  300|  			writeflag == MEM_WRITE ? "write to" : "read from",
  301|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  302|  		break;
  303|  
  304|  	case IOASIC_ISDN_R_DATA:
  305|  		if (writeflag == MEM_WRITE)
  306|  			d->isdn_r_data = idata;
  307|  		else
  308|  			odata = d->isdn_r_data;
  309|  
  310|  		debug("[ dec_ioasic: %s ISDN_R_DATA, data=0x%08" PRIx64 " ]\n",
  311|  			writeflag == MEM_WRITE ? "write to" : "read from",
  312|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  313|  		break;
  314|  
  315|  	case IOASIC_LANCE_DECODE:
  316|  		if (writeflag == MEM_WRITE)
  317|  			d->lance_decode = idata;
  318|  		else
     | [... lines 319-419 not shown ...]
  420|  	case 0x0f004:
  421|  	case 0x1f008:
  422|  	case 0x2f00c:
  423|  	case 0x3f010:
  424|  	case 0x4f014:
  425|  	case 0x5f018:
  426|  	case 0x6f01c:
  427|  	case 0x7f020:
  428|  	case 0x8f024:
  429|  	case 0x9f028:
  430|  	case 0xaf02c:
  431|  	case 0xbf030:
  432|  		break;
  433|  
  434|  	default:
  435|  		if (writeflag == MEM_WRITE)
  436|  			fatal("[ dec_ioasic: unimplemented write to address "
  437|  			    "0x%llx, data=0x%08llx ]\n",
  438|  			    (long long)relative_addr, (long long)idata);
  439|  		else
  440|  			fatal("[ dec_ioasic: unimplemented read from address "
  441|  			    "0x%llx ]\n", (long long)relative_addr);
  442|  		// exit(1);
  443|  	}
  444|  
  445|  	if (writeflag == MEM_READ)
  446|  		memory_writemax64(cpu, data, len, odata);
  447|  
  448|  	return 1;
  449|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_dec_ioasic.c",
    "old": "#if 0\n\t\tif (writeflag == MEM_WRITE) {\n\t\t\tcsr = d->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) / 0x10];\n\n\t\t\td->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) / 0x10] &=\n\t\t\t    ~IOASIC_INTR_T2_PAGE_END;\n\n\t\t\tif (csr & IOASIC_CSR_DMAEN_T2) {\n\t\t\t\t/*  Transmit data:  */\n\t\t\t\tcurptr = (d->reg[(IOASIC_SCC_T2_DMAPTR -\n\t\t\t\t    IOASIC_SLOT_1_START) / 0x10] >> 3)\n\t\t\t\t    | ((d->reg[(IOASIC_SCC_T2_DMAPTR -\n\t\t\t\t    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);\n\t\t\t\tdma_len = 0x1000 - (curptr & 0xffc);\n\n\t\t\t\tif ((curptr & 0xfff) == 0)\n\t\t\t\t\tbreak;\n\n\t\t\t\tif (d->dma_func[3] != NULL) {\n\t\t\t\t\td->dma_func[3](cpu,\n\t\t\t\t\t    d->dma_func_extra[3], curptr,\n\t\t\t\t\t    dma_len, 1);\n\t\t\t\t} else\n\t\t\t\t\tfatal(\"[ dec_ioasic: DMA tx: data @ \"\n\t\t\t\t\t    \"%08x, len %i bytes, but no \"\n\t\t\t\t\t    \"handler? ]\\n\", (int)curptr,\n\t\t\t\t\t    dma_len);\n\n\t\t\t\t/*  and signal the end of page:  */\n\t\t\t\td->reg[(IOASIC_INTR - IOASIC_SLOT_1_START) /\n\t\t\t\t    0x10] |= IOASIC_INTR_T2_PAGE_END;\n\n\t\t\t\td->reg[(IOASIC_CSR - IOASIC_SLOT_1_START) /\n\t\t\t\t    0x10] &= ~IOASIC_CSR_DMAEN_T2;\n\t\t\t\tcurptr |= 0xfff;\n\t\t\t\tcurptr ++;\n\n\t\t\t\td->reg[(IOASIC_SCC_T2_DMAPTR -\n\t\t\t\t    IOASIC_SLOT_1_START) / 0x10] = ((curptr <<\n\t\t\t\t    3) & ~0x1f) | ((curptr >> 29) & 0x1f);\n\t\t\t}\n\n\t\t\tif (csr & IOASIC_CSR_DMAEN_R2) {\n\t\t\t\t/*  Receive data:  */\n\t\t\t\tcurptr = (d->reg[(IOASIC_SCC_R2_DMAPTR -\n\t\t\t\t    IOASIC_SLOT_1_START) / 0x10] >> 3)\n\t\t\t\t    | ((d->reg[(IOASIC_SCC_R2_DMAPTR -\n\t\t\t\t    IOASIC_SLOT_1_START) / 0x10] & 0x1f) << 29);\n\t\t\t\tdma_len = 0x1000 - (curptr & 0xffc);\n\n\t\t\t\tdma_res = 0;\n\t\t\t\tif (d->dma_func[3] != NULL) {\n\t\t\t\t\tdma_res = d->dma_func[3](cpu,\n\t\t\t\t\t    d->dma_func_extra[3], curptr,\n\t\t\t\t\t    dma_len, 0);\n\t\t\t\t} else\n\t\t\t\t\tfatal(\"[ dec_ioasic: DMA tx: data @ \"\n\t\t\t\t\t    \"%08x, len %i bytes, but no \"\n\t\t\t\t\t    \"handler? ]\\n\", (int)curptr,\n\t\t\t\t\t    dma_len);\n\n\t\t\t\t/*  and signal the end of page:  */\n\t\t\t\tif (dma_res > 0) {\n\t\t\t\t\tif ((curptr & 0x800) != ((curptr +\n\t\t\t\t\t    dma_res) & 0x800))\n\t\t\t\t\t\td->reg[(IOASIC_INTR -\n\t\t\t\t\t\t    IOASIC_SLOT_1_START) / 0x10]\n\t\t\t\t\t\t    |= IOASIC_INTR_R2_HALF_PAGE;\n\t\t\t\t\tcurptr += dma_res;\n/*\t\t\t\t\td->reg[(IOASIC_CSR - IOASIC_SLOT_1_START\n\t\t\t\t\t   ) / 0x10] &= ~IOASIC_CSR_DMAEN_R2; */\n\t\t\t\t\td->reg[(IOASIC_SCC_R2_DMAPTR -\n\t\t\t\t\t    IOASIC_SLOT_1_START) / 0x10] =\n\t\t\t\t\t    ((curptr << 3) & ~0x1f) | ((curptr\n\t\t\t\t\t    >> 29) & 0x1f);\n\t\t\t\t}\n\t\t\t}\n\t\t}\n#endif",
    "new": "\t\t/* #NNN: uncomment and port to explicit fields */\n\t\tif (writeflag == MEM_WRITE) {\n\t\t\tuint32_t csr_val = d->csr;\n\n\t\t\td->intr &= ~IOASIC_INTR_T2_PAGE_END;\n\n\t\t\tif (csr_val & IOASIC_CSR_DMAEN_T2) {\n\t\t\t\tuint64_t curptr = (d->isdn_x_dmaptr >> 3)\n\t\t\t\t    | ((d->isdn_x_dmaptr & 0x1f) << 29);\n\t\t\t\tint dma_len = 0x1000 - (curptr & 0xffc);\n\n\t\t\t\tif ((curptr & 0xfff) != 0) {\n\t\t\t\t\tif (d->dma_func[3] != NULL) {\n\t\t\t\t\t\td->dma_func[3](cpu,\n\t\t\t\t\t\t    d->dma_func_extra[3], curptr,\n\t\t\t\t\t\t    dma_len, 1);\n\t\t\t\t\t}\n\n\t\t\t\t\td->intr |= IOASIC_INTR_T2_PAGE_END;\n\t\t\t\t\td->csr &= ~IOASIC_CSR_DMAEN_T2;\n\t\t\t\t\tcurptr |= 0xfff;\n\t\t\t\t\tcurptr ++;\n\n\t\t\t\t\td->isdn_x_dmaptr = ((curptr << 3) & ~0x1f) | ((curptr >> 29) & 0x1f);\n\t\t\t\t}\n\t\t\t}\n\n\t\t\tif (csr_val & IOASIC_CSR_DMAEN_R2) {\n\t\t\t\tuint64_t curptr = (d->isdn_r_dmaptr >> 3)\n\t\t\t\t    | ((d->isdn_r_dmaptr & 0x1f) << 29);\n\t\t\t\tint dma_len = 0x1000 - (curptr & 0xffc);\n\t\t\t\tint dma_res = 0;\n\n\t\t\t\tif (d->dma_func[3] != NULL) {\n\t\t\t\t\tdma_res = d->dma_func[3](cpu,\n\t\t\t\t\t    d->dma_func_extra[3], curptr,\n\t\t\t\t\t    dma_len, 0);\n\t\t\t\t}\n\n\t\t\t\tif (dma_res > 0) {\n\t\t\t\t\tif ((curptr & 0x800) != ((curptr + dma_res) & 0x800))\n\t\t\t\t\t\td->intr |= IOASIC_INTR_R2_HALF_PAGE;\n\t\t\t\t\tcurptr += dma_res;\n\t\t\t\t\td->isdn_r_dmaptr = ((curptr << 3) & ~0x1f) | ((curptr >> 29) & 0x1f);\n\t\t\t\t}\n\t\t\t}\n\t\t\tdec_ioasic_reassert(d);\n\t\t}",
    "why": "Uncommenting and mapping obsolete array references to updated struct fields."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_IOASIC3MINSCC: DEFECT, 3 FINDINGS
1. The diff successfully removes the `#if 0` defect described in the issue at `IOASIC_CSR` (lines 180-227), porting the array register accesses to explicit struct fields (`csr`, `intr`, `isdn_x_dmaptr`, `isdn_r_dmaptr`).
2. CONTROL FLOW: No code is skipped. The `break;` at line 228 correctly exits the `switch (relative_addr)` statement and falls through to the common tail (line 414: `if (writeflag == MEM_READ) memory_writemax64...`), ensuring the guest always receives the result.
3. RETURN VALUE: No path returns anything different. The function continues to return `1` in all cases, indicating a successfully handled memory access.
4. ELSE: The diff removes calls to `fatal(...)` when `d->dma_func[3] == NULL`, which successfully fulfills the project goal of removing crash-on-malformed-input defects (it now silently ignores the DMA instead of aborting the emulator). It also adds a call to `dec_ioasic_reassert(d)` (line 226) after modifying the CSR, which is correct for updating interrupt lines.
5. HOUSE IDIOMS: The new comment correctly uses the `/* #NNN: ... */` tag format. However, several added lines exceed the 79-column limit.
src/devices/dev_dec_ioasic.c:203: STYLE - Line exceeds 79 columns. Fix: wrap the bitwise operations to a new line.
src/devices/dev_dec_ioasic.c:220: STYLE - Line exceeds 79 columns. Fix: wrap the condition inside the `if` statement.
src/devices/dev_dec_ioasic.c:223: STYLE - Line exceeds 79 columns. Fix: wrap the bitwise operations to a new line.
FIXREVIEW_IOASIC3MINSCC: DEFECT, 3 FINDINGS
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_IOASIC3MINSCC: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_IOASIC3MINSCC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
