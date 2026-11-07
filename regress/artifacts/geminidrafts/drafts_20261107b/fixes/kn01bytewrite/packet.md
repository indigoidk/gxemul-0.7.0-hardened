# GXemul hardened fork -- DRAFT A FIX for one filed issue, `kn01bytewrite` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `kn01bytewrite`, state `open`, severity `MED`)

**title:** src/devices/dev_kn01.c:89-101 -- a CSR read that is not two bytes wide only prints a message and then writes data[0] and data[1], so a byte load writes one byte past the caller's one-byte stack buffer -- OOB-WRITE (DECstation 3100)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- clear out-of-bounds memory write on the host buffer requires an immediate patch to return early on invalid length.

## The code at the cited lines

### `src/devices/dev_kn01.c` around the row's cited line 89 (HEAD 8d9df658, lines 1-209)

```c
    1| /*
    2|  *  Copyright (C) 2003-2009  Anders Gavare.  All rights reserved.
    3|  *
    4|  *  Redistribution and use in source and binary forms, with or without
    5|  *  modification, are permitted provided that the following conditions are met:
    6|  *
    7|  *  1. Redistributions of source code must retain the above copyright
    8|  *     notice, this list of conditions and the following disclaimer.
    9|  *  2. Redistributions in binary form must reproduce the above copyright  
   10|  *     notice, this list of conditions and the following disclaimer in the 
   11|  *     documentation and/or other materials provided with the distribution.
   12|  *  3. The name of the author may not be used to endorse or promote products
   13|  *     derived from this software without specific prior written permission.
   14|  *
   15|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *   
   27|  *
   28|  *  COMMENT: DEC KN01 ("PMAX", DECstation type 1) control register and VDAC
   29|  *
   30|  *  TODO: The CSR isn't really complete.
   31|  *
   32|  *  One of the few usable bits in the csr would be KN01_CSR_MONO.
   33|  *  If that bit is set, the framebuffer is treated as a monochrome
   34|  *  one.
   35|  */
   36| 
   37| #include <stdio.h>
   38| #include <stdlib.h>
   39| #include <string.h>
   40| 
   41| #include "cpu.h"
   42| #include "devices.h"
   43| #include "memory.h"
   44| #include "misc.h"
   45| 
   46| #include "thirdparty/dec_kn01.h"
   47| 
   48| 
   49| struct kn01_data {
   50| 	int			color_fb;
   51| 	uint32_t		csr;
   52| };
   53| 
   54| 
   55| struct vdac_data {
   56| 	unsigned char	vdac_reg[DEV_VDAC_LENGTH];
   57| 
   58| 	int		color_fb_flag;
   59| 
   60| 	unsigned char	cur_read_addr;
   61| 	unsigned char	cur_write_addr;
   62| 
   63| 	int		sub_color;	/*  subcolor. 0, 1, or 2  */
   64| 	unsigned char	cur_rgb[3];
   65| 
   66| 	unsigned char	*rgb_palette;		/*  ptr to 256 * 3 (r,g,b)  */
   67| 
   68| 	unsigned char	cur_read_addr_overlay;
   69| 	unsigned char	cur_write_addr_overlay;
   70| 
   71| 	int		sub_color_overlay;	/*  subcolor: 0, 1, or 2  */
   72| 	unsigned char	cur_rgb_overlay[3];
   73| 
   74| 	unsigned char	rgb_palette_overlay[16 * 3];	/*  16 * 3 (r,g,b)  */
   75| };
   76| 
   77| 
   78| DEVICE_ACCESS(kn01)
   79| {
   80| 	struct kn01_data *d = (struct kn01_data *) extra;
   81| 	int csr;
   82| 
   83| 	if (writeflag == MEM_WRITE) {
   84| 		/*  TODO  */
   85| 		return 1;
   86| 	}
   87| 
   88| 	/*  Read:  */
   89| 	if (len != 2 || relative_addr != 0) {
   90| 		fatal("[ kn01: trying to read something which is not "
   91| 		    "the first half-word of the csr ]");
   92| 	}
   93| 
   94| 	csr = d->csr;
   95| 
   96| 	if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
   97| 		data[0] = csr & 0xff;
   98| 		data[1] = (csr >> 8) & 0xff;
   99| 	} else {
  100| 		data[1] = csr & 0xff;
  101| 		data[0] = (csr >> 8) & 0xff;
  102| 	}
  103| 
  104| 	return 1;
  105| }
  106| 
  107| 
  108| /*
  109|  *  dev_vdac_access():
  110|  */
  111| DEVICE_ACCESS(vdac)
  112| {
  113| 	struct vdac_data *d = (struct vdac_data *) extra;
  114| 
  115| 	/*  Read from/write to the vdac:  */
  116| 	switch (relative_addr) {
  117| 	case DEV_VDAC_MAPWA:
  118| 		if (writeflag == MEM_WRITE) {
  119| 			d->cur_write_addr = data[0];
  120| 			d->sub_color = 0;
  121| 		} else {
  122| 			debug("[ vdac: read from MAPWA ]\n");
  123| 			data[0] = d->vdac_reg[relative_addr];
  124| 		}
  125| 		break;
  126| 	case DEV_VDAC_MAP:
  127| 		if (writeflag == MEM_WRITE) {
  128| 			d->cur_rgb[d->sub_color] = data[0];
  129| 			d->sub_color++;
  130| 
  131| 			if (d->sub_color > 2) {
  132| 				/*  (Only update for color, not mono mode)  */
  133| 				if (d->color_fb_flag)
  134| 					memcpy(d->rgb_palette +
  135| 					    3*d->cur_write_addr, d->cur_rgb, 3);
  136| 
  137| 				d->sub_color = 0;
  138| 				d->cur_write_addr ++;
  139| 			}
  140| 		} else {
  141| 			if (d->sub_color == 0) {
  142| 				memcpy(d->cur_rgb, d->rgb_palette +
  143| 				    3 * d->cur_read_addr, 3);
  144| 			}
  145| 			data[0] = d->cur_rgb[d->sub_color];
  146| 			d->sub_color++;
  147| 			if (d->sub_color > 2) {
  148| 				d->sub_color = 0;
  149| 				d->cur_read_addr ++;
  150| 			}
  151| 		}
  152| 		break;
  153| 	case DEV_VDAC_MAPRA:
  154| 		if (writeflag == MEM_WRITE) {
  155| 			d->cur_read_addr = data[0];
  156| 			d->sub_color = 0;
  157| 		} else {
  158| 			debug("[ vdac: read from MAPRA ]\n");
  159| 			data[0] = d->vdac_reg[relative_addr];
  160| 		}
  161| 		break;
  162| 	case DEV_VDAC_OVERWA:
  163| 		if (writeflag == MEM_WRITE) {
  164| 			d->cur_write_addr_overlay = data[0] & 15;	/* OB-8: 16-entry overlay palette */
  165| 			d->sub_color_overlay = 0;
  166| 		} else {
  167| 			debug("[ vdac: read from OVERWA ]\n");
  168| 			data[0] = d->vdac_reg[relative_addr];
  169| 		}
  170| 		break;
  171| 	case DEV_VDAC_OVER:
  172| 		if (writeflag == MEM_WRITE) {
  173| 			d->cur_rgb_overlay[d->sub_color_overlay] = data[0];
  174| 			d->sub_color_overlay++;
  175| 
  176| 			if (d->sub_color_overlay > 2) {
  177| 				/*  (Only update for color, not mono mode)  */
  178| 				if (d->color_fb_flag)
  179| 					memcpy(d->rgb_palette_overlay +
  180| 					    3 * d->cur_write_addr_overlay,
  181| 					    d->cur_rgb_overlay, 3);
  182| 
  183| 				d->sub_color_overlay = 0;
  184| 				d->cur_write_addr_overlay ++;
  185| 				if (d->cur_write_addr_overlay > 15)
  186| 					d->cur_write_addr_overlay = 0;
  187| 			}
  188| 		} else {
  189| 			if (d->sub_color_overlay == 0) {
  190| 				memcpy(d->cur_rgb_overlay,
  191| 				    d->rgb_palette_overlay +
  192| 				    3 * d->cur_read_addr_overlay, 3);
  193| 			}
  194| 			data[0] = d->cur_rgb_overlay[d->sub_color_overlay];
  195| 			d->sub_color_overlay++;
  196| 			if (d->sub_color_overlay > 2) {
  197| 				d->sub_color_overlay = 0;
  198| 				d->cur_read_addr_overlay ++;
  199| 				if (d->cur_read_addr_overlay > 15)
  200| 					d->cur_read_addr_overlay = 0;
  201| 			}
  202| 		}
  203| 		break;
  204| 	case DEV_VDAC_OVERRA:
  205| 		if (writeflag == MEM_WRITE) {
  206| 			d->cur_read_addr_overlay = data[0] & 15;	/* OB-8b: 16-entry overlay palette (read addr; cf #75) */
  207| 			d->sub_color_overlay = 0;
  208| 		} else {
  209| 			debug("[ vdac: read from OVERRA ]\n");
```

### `src/cpus/cpu_mips_instr_loadstore.c` around the row's cited line 46 (HEAD 8d9df658, lines 1-166)

```c
    1| /*
    2|  *  Copyright (C) 2006-2021  Anders Gavare.  All rights reserved.
    3|  *
    4|  *  Redistribution and use in source and binary forms, with or without
    5|  *  modification, are permitted provided that the following conditions are met:
    6|  *
    7|  *  1. Redistributions of source code must retain the above copyright
    8|  *     notice, this list of conditions and the following disclaimer.
    9|  *  2. Redistributions in binary form must reproduce the above copyright
   10|  *     notice, this list of conditions and the following disclaimer in the
   11|  *     documentation and/or other materials provided with the distribution.
   12|  *  3. The name of the author may not be used to endorse or promote products
   13|  *     derived from this software without specific prior written permission.
   14|  *
   15|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *
   27|  *
   28|  *  MIPS load/store instructions; the following args are used:
   29|  *  
   30|  *  arg[0] = pointer to the register to load to or store from
   31|  *  arg[1] = pointer to the base register
   32|  *  arg[2] = offset (as an int32_t)
   33|  *
   34|  *  The GENERIC function always checks for alignment, and supports both big
   35|  *  and little endian byte order.
   36|  *
   37|  *  The quick function is included twice (big/little endian) for each
   38|  *  GENERIC function.
   39|  */
   40| 
   41| 
   42| #ifdef LS_INCLUDE_GENERIC
   43| void LS_GENERIC_N(struct cpu *cpu, struct mips_instr_call *ic)
   44| {
   45| 	MODE_int_t addr = reg(ic->arg[1]) + (int32_t)ic->arg[2];
   46| 	uint8_t data[LS_SIZE];
   47| #ifdef LS_LOAD
   48| 	uint64_t x;
   49| #endif
   50| 
   51| 	/*  Synchronize the PC:  */
   52| 	int low_pc = ((size_t)ic - (size_t)cpu->cd.mips.cur_ic_page)
   53| 	    / sizeof(struct mips_instr_call);
   54| 	cpu->pc &= ~((MIPS_IC_ENTRIES_PER_PAGE-1)<<MIPS_INSTR_ALIGNMENT_SHIFT);
   55| 	cpu->pc += (low_pc << MIPS_INSTR_ALIGNMENT_SHIFT);
   56| 
   57| #ifndef LS_1
   58| 	/*  Check alignment:  */
   59| 	if (addr & (LS_SIZE - 1)) {
   60| #if 1
   61| 		uint64_t vaddr_vpn2=0, vaddr_asid=0;
   62| 
   63| 		int exc_model = cpu->cd.mips.cpu_type.exc_model;
   64| 		struct mips_coproc *cp0 = cpu->cd.mips.coproc[0];
   65| 
   66| 		if (exc_model == EXC3K) {
   67| 			vaddr_asid = (cp0->reg[COP0_ENTRYHI] &
   68| 			    R2K3K_ENTRYHI_ASID_MASK) >>
   69| 			    R2K3K_ENTRYHI_ASID_SHIFT;
   70| 			vaddr_vpn2 = (addr & R2K3K_ENTRYHI_VPN_MASK) >>
   71| 			    R2K3K_ENTRYHI_VPN_SHIFT;
   72| 		} else {
   73| 			vaddr_asid = cp0->reg[COP0_ENTRYHI] & ENTRYHI_ASID;
   74| 
   75| 			if (cpu->cd.mips.cpu_type.mmu_model == MMU10K) {
   76| 				vaddr_vpn2 = (addr &
   77| 				    ENTRYHI_VPN2_MASK_R10K) >>
   78| 				    ENTRYHI_VPN2_SHIFT;
   79| 			} else {
   80| 				vaddr_vpn2 = (addr & ENTRYHI_VPN2_MASK) >>
   81| 				    ENTRYHI_VPN2_SHIFT;
   82| 			}
   83| 		}
   84| 
   85| 		/*  Cause an address alignment exception:  */
   86| 		mips_cpu_exception(cpu,
   87| #ifdef LS_LOAD
   88| 		    EXCEPTION_ADEL,
   89| #else
   90| 		    EXCEPTION_ADES,
   91| #endif
   92| 		    0, addr, 0, vaddr_vpn2, vaddr_asid, 0);
   93| #else
   94| 		fatal("{ mips dyntrans alignment exception, size = %i,"
   95| 		    " addr = %016"PRIx64", pc = %016"PRIx64" }\n", LS_SIZE,
   96| 		    (uint64_t) addr, cpu->pc);
   97| 
   98| 		cpu->running = false;
   99| 		cpu->cd.mips.next_ic = &nothing_call;
  100| #endif
  101| 		return;
  102| 	}
  103| #endif
  104| 
  105| #ifdef LS_LOAD
  106| 	if (!cpu->memory_rw(cpu, cpu->mem, addr, data, sizeof(data),
  107| 	    MEM_READ, CACHE_DATA)) {
  108| 		/*  Exception.  */
  109| 		if (!cpu->running)
  110| 			cpu->cd.mips.next_ic = &nothing_call;
  111| 		return;
  112| 	}
  113| 	x = memory_readmax64(cpu, data, LS_SIZE);
  114| #ifdef LS_SIGNED
  115| #ifdef LS_1
  116| 	x = (int8_t)x;
  117| #endif
  118| #ifdef LS_2
  119| 	x = (int16_t)x;
  120| #endif
  121| #ifdef LS_4
  122| 	x = (int32_t)x;
  123| #endif
  124| #endif
  125| 	reg(ic->arg[0]) = x;
  126| #else	/*  LS_STORE:  */
  127| 	memory_writemax64(cpu, data, LS_SIZE, reg(ic->arg[0]));
  128| 	if (!cpu->memory_rw(cpu, cpu->mem, addr, data, sizeof(data),
  129| 	    MEM_WRITE, CACHE_DATA)) {
  130| 		/*  Exception.  */
  131| 		if (!cpu->running)
  132| 			cpu->cd.mips.next_ic = &nothing_call;
  133| 		return;
  134| 	}
  135| #endif
  136| }
  137| #endif	/*  LS_INCLUDE_GENERIC  */
  138| 
  139| 
  140| void LS_N(struct cpu *cpu, struct mips_instr_call *ic)
  141| {
  142| 	MODE_uint_t addr = reg(ic->arg[1]) + (int32_t)ic->arg[2];
  143| 	unsigned char *p;
  144| #ifdef MODE32
  145| #ifdef LS_LOAD
  146| 	p = cpu->cd.mips.host_load[addr >> 12];
  147| #else
  148| 	p = cpu->cd.mips.host_store[addr >> 12];
  149| #endif
  150| #else	/*  !MODE32  */
  151| 	const uint32_t mask1 = (1 << DYNTRANS_L1N) - 1;
  152| 	const uint32_t mask2 = (1 << DYNTRANS_L2N) - 1;
  153| 	const uint32_t mask3 = (1 << DYNTRANS_L3N) - 1;
  154| 	uint32_t x1, x2, x3;
  155| 	struct DYNTRANS_L2_64_TABLE *l2;
  156| 	struct DYNTRANS_L3_64_TABLE *l3;
  157| 
  158| 	x1 = (addr >> (64-DYNTRANS_L1N)) & mask1;
  159| 	x2 = (addr >> (64-DYNTRANS_L1N-DYNTRANS_L2N)) & mask2;
  160| 	x3 = (addr >> (64-DYNTRANS_L1N-DYNTRANS_L2N-DYNTRANS_L3N)) & mask3;
  161| 	/*  fatal("X3: addr=%016"PRIx64" x1=%x x2=%x x3=%x\n",
  162| 	    (uint64_t) addr, (int) x1, (int) x2, (int) x3);  */
  163| 	l2 = cpu->cd.DYNTRANS_ARCH.l1_64[x1];
  164| 	/*  fatal("  l2 = %p\n", l2);  */
  165| 	l3 = l2->l3[x2];
  166| 	/*  fatal("  l3 = %p\n", l3);  */
```

### `src/cpus/memory_rw.c` around the row's cited line 587 (HEAD 8d9df658, lines 467-707)

```c
  467| 		for (i=0; i<mem->n_mmapped_devices; i++)
  468| 			if (paddr >= (mem->devices[i].baseaddr & ~offset_mask)&&
  469| 			    paddr <= ((mem->devices[i].endaddr-1)|offset_mask)){
  470| 				dyntrans_device_danger = 1;
  471| 				break;
  472| 			}
  473| #endif
  474| 
  475| 		start = 0; end = mem->n_mmapped_devices - 1;
  476| 		i = mem->last_accessed_device;
  477| 
  478| 		/*  Scan through all devices:  */
  479| 		do {
  480| 			if (paddr >= mem->devices[i].baseaddr &&
  481| 			    paddr < mem->devices[i].endaddr) {
  482| 				/*  Found a device, let's access it:  */
  483| 				mem->last_accessed_device = i;
  484| 
  485| 				/*  #95: zero the caller's buffer up front on a read
  486| 				    so a device handler that fills only part of it --
  487| 				    or whose access is len-clamped just below -- can
  488| 				    never hand back uninitialised host memory to the
  489| 				    guest.  Root-cause fix for the uninit-read class
  490| 				    (cf. per-device #91/#93/#94).  */
  491| 				if (writeflag == MEM_READ)
  492| 					memset(data, 0, len);
  493| 
  494| 				paddr -= mem->devices[i].baseaddr;
  495| 				if (paddr + len > mem->devices[i].length) {
  496| 					/*  Note the truncation per the
  497| 					    warn-loudly ethos, but only at
  498| 					    debug verbosity (-v) and at most
  499| 					    8 times (single-threaded), since
  500| 					    probing at the end of a device's
  501| 					    mapped range is common and benign
  502| 					    (cf. the unwarned zero-fill in
  503| 					    #95/#119 above).  */
  504| 					static int n_trunc_msgs = 0;
  505| 					if (ENOUGH_VERBOSITY(SUBSYS_MEMORY,
  506| 					    VERBOSITY_DEBUG) &&
  507| 					    n_trunc_msgs < 8) {
  508| 						n_trunc_msgs ++;
  509| 						debugmsg_cpu(cpu,
  510| 						    SUBSYS_MEMORY,
  511| 						    mem->devices[i].name,
  512| 						    VERBOSITY_DEBUG,
  513| 						    "%s truncated at end of"
  514| 						    " device: offset 0x%llx,"
  515| 						    " len %i -> %i",
  516| 						    writeflag == MEM_WRITE ?
  517| 						    "write" : "read",
  518| 						    (long long) paddr,
  519| 						    (int) len,
  520| 						    (int) (mem->devices[i].
  521| 						    length - paddr));
  522| 					}
  523| 					len = mem->devices[i].length - paddr;
  524| 				}
  525| 
  526| 				if (cpu->update_translation_table != NULL &&
  527| 				    !(ok & MEMORY_NOT_FULL_PAGE) &&
  528| 				    mem->devices[i].flags & DM_DYNTRANS_OK) {
  529| 					int wf = writeflag == MEM_WRITE? 1 : 0;
  530| 					unsigned char *host_addr;
  531| 
  532| 					if (!(mem->devices[i].flags &
  533| 					    DM_DYNTRANS_WRITE_OK))
  534| 						wf = 0;
  535| 
  536| 					if (writeflag && wf) {
  537| 						if (paddr < mem->devices[i].
  538| 						    dyntrans_write_low)
  539| 							mem->devices[i].
  540| 							dyntrans_write_low =
  541| 							    paddr &~offset_mask;
  542| 						if (paddr >= mem->devices[i].
  543| 						    dyntrans_write_high)
  544| 							mem->devices[i].
  545| 						 	dyntrans_write_high =
  546| 							    paddr | offset_mask;
  547| 					}
  548| 
  549| 					if (mem->devices[i].flags &
  550| 					    DM_EMULATED_RAM) {
  551| 						/*  MEM_WRITE to force the page
  552| 						    to be allocated, if it
  553| 						    wasn't already  */
  554| 						uint64_t *pp = (uint64_t *)mem->
  555| 						    devices[i].dyntrans_data;
  556| 						uint64_t p = orig_paddr - *pp;
  557| 						host_addr =
  558| 						    memory_paddr_to_hostaddr(
  559| 						    mem, p & ~offset_mask,
  560| 						    MEM_WRITE);
  561| 					} else if ((paddr | offset_mask) <
  562| 					    mem->devices[i].length) {
  563| 						host_addr = mem->devices[i].
  564| 						    dyntrans_data +
  565| 						    (paddr & ~offset_mask);
  566| 					} else {
  567| 						/*  #155: (Codex/Fable)
  568| 						    don't install dyntrans
  569| 						    fast-path access to a
  570| 						    device page that is not
  571| 						    fully backed; keep it on
  572| 						    the bounded slow path.  */
  573| 						host_addr = NULL;
  574| 					}
  575| 
  576| 					if (host_addr != NULL)
  577| 						cpu->update_translation_table(
  578| 						    cpu, vaddr & ~offset_mask,
  579| 						    host_addr, wf,
  580| 						    orig_paddr & ~offset_mask);
  581| 				}
  582| 
  583| 				res = 0;
  584| 				if (!no_exceptions || (mem->devices[i].flags &
  585| 				    DM_READS_HAVE_NO_SIDE_EFFECTS)) {
  586| 					bool running_before_device_access = cpu->running;
  587| 					res = mem->devices[i].f(cpu, mem, paddr,
  588| 					    data, len, writeflag,
  589| 					    mem->devices[i].extra);
  590| 
  591| 					if (running_before_device_access && !cpu->running)
  592| 						return MEMORY_ACCESS_FAILED;
  593| 				}
  594| 
  595| 				if (res == 0)
  596| 					res = -1;
  597| 
  598| 				/*
  599| 				 *  If accessing the memory mapped device
  600| 				 *  failed, then return with an exception.
  601| 				 *  (Architecture specific.)
  602| 				 */
  603| 				if (res <= 0 && !no_exceptions) {
  604| 					debug("[ %s device '%s' addr %08lx "
  605| 					    "failed ]\n", writeflag?
  606| 					    "writing to" : "reading from",
  607| 					    mem->devices[i].name, (long)paddr);
  608| #ifdef MEM_MIPS
  609| 					mips_cpu_exception(cpu,
  610| 					    cache == CACHE_INSTRUCTION?
  611| 					    EXCEPTION_IBE : EXCEPTION_DBE,
  612| 					    0, vaddr, 0, 0, 0, 0);
  613| #endif
  614| #ifdef MEM_M88K
  615| 					/*  #570: record the bus error in the faulting side's
  616| 					    CMMU first: PFSR = BERROR << 16 (the field
  617| 					    OpenBSD/mvme88k's trap.c extracts) and PFAR =
  618| 					    orig_paddr, the PHYSICAL address saved before paddr
  619| 					    was made device-relative.  cmmu[0] is the instruction
  620| 					    CMMU, cmmu[1] the data CMMU (memory_m88k.c's index);
  621| 					    the other CMMU is not written.  For a CPU without a
  622| 					    CMMU, this arm makes no register write; the exception
  623| 					    call is unchanged.  `null route` scores data-access
  624| 					    delivery; instruction-access delivery is unscored
  625| 					    (`null surv` scores survival only).  NO_EXCEPTIONS
  626| 					    callers (e.g. the debugger's dump) never get here:
  627| 					    the test above keeps them out.  */
  628| 					{
  629| 						struct m8820x_cmmu *cmmu =
  630| 						    cpu->cd.m88k.cmmu[cache ==
  631| 						    CACHE_INSTRUCTION ? 0 : 1];
  632| 						if (cmmu != NULL) {
  633| 							cmmu->reg[CMMU_PFSR] =
  634| 							    CMMU_PFSR_BERROR << 16;
  635| 							cmmu->reg[CMMU_PFAR] =
  636| 							    (uint32_t) orig_paddr;
  637| 						}
  638| 					}
  639| 					m88k_exception(cpu, cache == CACHE_INSTRUCTION
  640| 					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  641| 					    : M88K_EXCEPTION_DATA_ACCESS, 0);
  642| #endif
  643| 					return MEMORY_ACCESS_FAILED;
  644| 				}
  645| 				goto do_return_ok;
  646| 			}
  647| 
  648| 			if (paddr < mem->devices[i].baseaddr)
  649| 				end = i - 1;
  650| 			if (paddr >= mem->devices[i].endaddr)
  651| 				start = i + 1;
  652| 			i = (start + end) >> 1;
  653| 		} while (start <= end);
  654| 	}
  655| 
  656| 
  657| #ifdef MEM_MIPS
  658| 	/*
  659| 	 *  Data and instruction cache emulation:
  660| 	 */
  661| 
  662| 	switch (cpu->cd.mips.cpu_type.mmu_model) {
  663| 	case MMU3K:
  664| 		/*  if not uncached addess  (TODO: generalize this)  */
  665| 		if (!(misc_flags & PHYSICAL) && cache != CACHE_NONE &&
  666| 		    !((vaddr & 0xffffffffULL) >= 0xa0000000ULL &&
  667| 		      (vaddr & 0xffffffffULL) <= 0xbfffffffULL)) {
  668| 			if (memory_cache_R3000(cpu, cache, paddr,
  669| 			    writeflag, len, data))
  670| 				goto do_return_ok;
  671| 		}
  672| 		break;
  673| 	default:
  674| 		/*  R4000 etc  */
  675| 		/*  TODO  */
  676| 		;
  677| 	}
  678| #endif	/*  MEM_MIPS  */
  679| 
  680| 
  681| 	/*  Outside of physical RAM?  */
  682| 	if (paddr >= mem->physical_max) {
  683| #ifdef MEM_MIPS
  684| 		if ((paddr & 0xffffc00000ULL) == 0x1fc00000) {
  685| 			/*  Ok, this is PROM stuff  */
  686| 		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
  687| 			/*  Sprite reads from this area of memory...  */
  688| 			/*  TODO: is this still correct?  */
  689| 			if (writeflag == MEM_READ)
  690| 				memset(data, 0, len);
  691| 			goto do_return_ok;
  692| 		} else
  693| #endif /* MIPS */
  694| 		{
  695| 			if (paddr >= mem->physical_max && !no_exceptions)
  696| 				if (memory_warn_about_unimplemented_addr
  697| 				    (cpu, mem, writeflag, paddr, len))
  698| 					return MEMORY_ACCESS_FAILED;
  699| 
  700| 			if (writeflag == MEM_READ) {
  701| 				/*  Return all zeroes? (Or 0xff? TODO)  */
  702| 				memset(data, 0, len);
  703| 
  704| #if 0
  705| /*
  706|  *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  707|  *  I think I introduced it because it was how some guest OS (NetBSD?) detected
```

## The data structures those files define (every field that exists)

### `src/devices/dev_kn01.c` -- `struct kn01_data {` (HEAD lines 49-52)

```c
   49| struct kn01_data {
   50| 	int			color_fb;
   51| 	uint32_t		csr;
   52| };
```

### `src/devices/dev_kn01.c` -- `struct vdac_data {` (HEAD lines 55-75)

```c
   55| struct vdac_data {
   56| 	unsigned char	vdac_reg[DEV_VDAC_LENGTH];
   57| 
   58| 	int		color_fb_flag;
   59| 
   60| 	unsigned char	cur_read_addr;
   61| 	unsigned char	cur_write_addr;
   62| 
   63| 	int		sub_color;	/*  subcolor. 0, 1, or 2  */
   64| 	unsigned char	cur_rgb[3];
   65| 
   66| 	unsigned char	*rgb_palette;		/*  ptr to 256 * 3 (r,g,b)  */
   67| 
   68| 	unsigned char	cur_read_addr_overlay;
   69| 	unsigned char	cur_write_addr_overlay;
   70| 
   71| 	int		sub_color_overlay;	/*  subcolor: 0, 1, or 2  */
   72| 	unsigned char	cur_rgb_overlay[3];
   73| 
   74| 	unsigned char	rgb_palette_overlay[16 * 3];	/*  16 * 3 (r,g,b)  */
   75| };
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

End with one line: `FIXDRAFT_KN01BYTEWRITE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
