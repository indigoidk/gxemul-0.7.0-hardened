/*
 *  Copyright (C) 2005-2021  Anders Gavare.  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 *  SUCH DAMAGE.
 *
 *
 *  TODO:  Many things...
 *
 *	o)  Big-endian Double-Word loads/stores are likely INCORRECT.
 *
 *	o)  "Base Updated Abort Model", which updates the base register
 *	    even if the memory access failed.
 *
 *	o)  Some ARM implementations use pc+8, some use pc+12 for stores?
 *
 *	o)  All load/store variants with the PC register are not really
 *	    valid. (E.g. a byte load into the PC register. What should that
 *	    accomplish?)
 *
 *	o)  Perhaps an optimization for the case when offset = 0, because
 *	    that's quite common, and also when the Reg expression is just
 *	    a simple, non-rotated register (0..14).
 */


#if defined(A__SIGNED) && !defined(A__H) && !defined(A__L)
#define A__LDRD
#endif
#if defined(A__SIGNED) && defined(A__H) && !defined(A__L)
#define A__STRD
#endif


#ifndef NOTHING_CALL
#define NOTHING_CALL
static struct arm_instr_call nothing_call = { arm_instr_nothing, {0,0,0} };
#endif


/*
 *  General load/store, by using memory_rw(). If at all possible, memory_rw()
 *  then inserts the page into the translation array, so that the fast
 *  load/store routine below can be used for further accesses.
 */
void A__NAME__general(struct cpu *cpu, struct arm_instr_call *ic)
{
	/*
	 *  #367: count ENTRIES, before any work, so an exception-driven early
	 *  exit still counts -- an exception is still a general-path event.
	 *  Read via `tlbdump`; see the declaration in cpu_arm.h for why this is
	 *  a counter and not a debugmsg.
	 */
	cpu->cd.arm.ls_general ++;				/*  #367  */

#if !defined(A__P) && defined(A__W)
	const int memory_rw_flags = CACHE_DATA | MEMORY_USER_ACCESS;
#else
	const int memory_rw_flags = CACHE_DATA;
#endif

#ifdef A__REG
	uint32_t (*reg_func)(struct cpu *, struct arm_instr_call *)
	    = (uint32_t (*)(struct cpu *, struct arm_instr_call *))
	      (void *)(size_t)ic->arg[1];
#endif

#if defined(A__STRD) || defined(A__LDRD)
	unsigned char data[8];
	const int datalen = 8;
#else
#ifdef A__B
	unsigned char data[1];
	const int datalen = 1;
#else
#ifdef A__H
	unsigned char data[2];
	const int datalen = 2;
#else
	const int datalen = 4;
#ifdef HOST_LITTLE_ENDIAN
	unsigned char *data = (unsigned char *) ic->arg[2];
#else
	unsigned char data[4];
#endif
#endif
#endif
#endif

	uint32_t addr, low_pc, offset =
#ifndef A__U
	    -
#endif
#ifdef A__REG
	    reg_func(cpu, ic);
#else
	    ic->arg[1];
#endif

	low_pc = ((size_t)ic - (size_t)cpu->cd.arm.
	    cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	addr = reg(ic->arg[0])
#ifdef A__P
	    + offset
#endif
	    ;

	/*
	 *  #357: the base writeback is computed from the UNMASKED address.
	 *  DDI 0100I A5.2.8 (post-indexed) is `address = Rn` then
	 *  `Rn = Rn + offset_12`, and A5.2.5 (pre-indexed) is
	 *  `address = Rn + offset_12` then `Rn = address` -- both reading the raw
	 *  Rn. The alignment truncation belongs to the memory access, not to the
	 *  register: A2-43 says the mask lives inside Memory[<address>,<size>],
	 *  and where the manual really does force an address it says so (LDC
	 *  "ignores the least significant two bits"), which it never says about a
	 *  base register. Every other ARM base writeback in this emulator already
	 *  follows the unmasked model, checked over the whole set and not just a
	 *  sample: arm_pop/arm_push, the generated LDM/STM (which masks its DATA
	 *  pointer but steps the base raw), bdt_load/bdt_store (which delegate to
	 *  pop/push), and all of netbsd_cacheclean, cacheclean2, copyin, copyout,
	 *  memcpy, memset and strlen. ldrex/strex/swp/scanc have no base writeback
	 *  and LDC/STC are unimplemented, so no other path exists. This template
	 *  was the sole outlier, and the folds that were queued as defects for
	 *  writing an unmasked base were right all along. Note those folds fall
	 *  back into these handlers on a page or user-page miss, so before this
	 *  correction the emulator disagreed with ITSELF between the folded and
	 *  unfolded executions of one guest loop.
	 *
	 *  What masking actually did, stated exactly, because the first draft of
	 *  this comment got it too broad: the map b -> (b & ~(datalen-1)) + offset
	 *  drives the base's low bits to offset & (datalen-1) after a single
	 *  iteration and then holds them there, so from the second iteration a loop
	 *  advances by offset & ~(datalen-1) -- the offset truncated down to a
	 *  multiple of the access size. When the offset is SMALLER than the access
	 *  size that advance is zero and the base is a FIXED POINT: base 0x10001
	 *  with offset 1 masks to 0x10000, adds 1, and writes back the value it
	 *  started from, so the loop never advanced at all. A larger non-multiple
	 *  offset is not a fixed point but still wrong -- offset 5 on a word access
	 *  advances by 4. Only the copy handed to memory is masked, below.
	 *
	 *  Declared only where a writeback exists: the p1_w0 (offset-addressing)
	 *  instantiations have no writeback block, and this file is #included once
	 *  per variant, so an unconditional local would warn per instantiation.
	 */
#if !defined(A__P) || defined(A__W)
	const uint32_t wb_addr = addr;
#endif

	/*
	 *  #362: an unaligned word LOAD returns the aligned word ROTATED RIGHT by
	 *  8 * addr[1:0]. DDI 0100I A2.8 (p. A2-38) states it, and A4.1.23 LDR's
	 *  pseudocode is `data = Memory[address,4] Rotate_Right (8 * address[1:0])`
	 *  when the CP15 U bit is 0. This template masked and never rotated, so it
	 *  returned the aligned word unchanged -- measured wrong in 3 of the 4
	 *  low-bit cases.
	 *
	 *  LOADS ONLY: A4.1.99 says STR ignores the low two address bits, so stores
	 *  are already right, and A4.1.28 makes an unaligned halfword load's data
	 *  UNPREDICTABLE, so masking without rotating is permitted there. LDRD is
	 *  excluded automatically because A__LDRD does not define A__L.
	 *
	 *  Applied UNCONDITIONALLY rather than gated on architecture version, and
	 *  the reason is dominance rather than convenience: rotation is correct for
	 *  ARMv3/v4/v5 and for v6+ with U == 0, and where v6+ with U == 1 wants a
	 *  true unaligned access, masking and rotating are wrong equally -- so this
	 *  is never worse than what it replaces, in any combination. Gating would
	 *  also be unsound here: there is no architecture level in the CPU type
	 *  table (its own header says "TODO: Include ARM level" and "Most of these
	 *  are bogus"), deriving one from cpu_id[19:16] misclassifies ARM7500FE as
	 *  ARMv6 -- wrong in the direction that changes behaviour -- and no
	 *  ARM_CONTROL_U is defined anywhere. Recorded divergence: v6+ with U == 1.
	 *
	 *  #357's `wb_addr` cannot be reused for this: it exists only under
	 *  `!defined(A__P) || defined(A__W)`, and the plain offset-addressing word
	 *  load has neither. Captured here, after the address is computed and
	 *  before the mask.
	 */
#if defined(A__L) && !defined(A__B) && !defined(A__H) && !defined(A__LDRD)
	const uint32_t rot_sh = 8 * (addr & 3);
#endif

	addr &= ~(datalen - 1);

#if defined(A__L) || defined(A__LDRD)
	/*  Load:  */
	if (!cpu->memory_rw(cpu, cpu->mem, addr, data, datalen,
	    MEM_READ, memory_rw_flags)) {
		/*  load failed, an exception was generated  */
		if (!cpu->running)
			cpu->cd.arm.next_ic = &nothing_call;
		return;
	}
#if defined(A__B) && !defined(A__LDRD)
	reg(ic->arg[2]) =
#ifdef A__SIGNED
	    (int32_t)(int8_t)
#endif
	    data[0];
#else
#if defined(A__H) && !defined(A__LDRD)
	reg(ic->arg[2]) =
#ifdef A__SIGNED
	    (int32_t)(int16_t)
#endif
	    (cpu->byte_order == EMUL_LITTLE_ENDIAN
	    ? (data[0] + (data[1] << 8))
	    : (data[1] + (data[0] << 8)));
#else
#ifndef A__LDRD
	reg(ic->arg[2]) =
		cpu->byte_order == EMUL_LITTLE_ENDIAN
		? data[0] + (data[1] << 8) + (data[2] << 16) + (data[3] << 24)
		: data[3] + (data[2] << 8) + (data[1] << 16) + (data[0] << 24);
	/*  #362: rotate right by 8 * addr[1:0]; see the capture above. Guarded on
	    rot_sh so the aligned case emits no shift at all, and because a 32-bit
	    value shifted left by 32 is undefined in C.  */
	if (rot_sh)
		reg(ic->arg[2]) = (reg(ic->arg[2]) >> rot_sh) |
		    (reg(ic->arg[2]) << (32 - rot_sh));
#else
	// TODO: Double-check if this is correct
	reg(ic->arg[2]) =
		cpu->byte_order == EMUL_LITTLE_ENDIAN
		? data[0] + (data[1] << 8) + (data[2] << 16) + (data[3] << 24)
		: data[7] + (data[1] << 6) + (data[5] << 16) + (data[4] << 24);
	reg(((uint32_t *)ic->arg[2]) + 1) =
		cpu->byte_order == EMUL_LITTLE_ENDIAN
		? data[4] + (data[5] << 8) + (data[6] << 16) + (data[7] << 24)
		: data[0] + (data[1] << 8) + (data[2] << 16) + (data[3] << 24);
#endif
#endif
#endif
#else
	/*  Store:  */
#if !defined(A__B) && !defined(A__H) && defined(HOST_LITTLE_ENDIAN)
#ifdef A__STRD
	*(uint32_t *)data = reg(ic->arg[2]);
	*(uint32_t *)(data + 4) = reg(ic->arg[2] + 4);
#endif
#else
	int i = cpu->byte_order == EMUL_LITTLE_ENDIAN ? 0 : datalen - 1;
	data[i] = reg(ic->arg[2]);
	i += cpu->byte_order == EMUL_LITTLE_ENDIAN ? 1 : -1;
#ifndef A__B
	data[i] = reg(ic->arg[2]) >> 8;
	i += cpu->byte_order == EMUL_LITTLE_ENDIAN ? 1 : -1;
#if !defined(A__H) || defined(A__STRD)
	data[i] = reg(ic->arg[2]) >> 16;
	i += cpu->byte_order == EMUL_LITTLE_ENDIAN ? 1 : -1;
	data[i] = reg(ic->arg[2]) >> 24;
	i += cpu->byte_order == EMUL_LITTLE_ENDIAN ? 1 : -1;
#ifdef A__STRD
	// TODO: Double-check if this is correct
	data[i] = reg(ic->arg[2] + 4);
	i += cpu->byte_order == EMUL_LITTLE_ENDIAN ? 1 : -1;
	data[i] = reg(ic->arg[2] + 4) >> 8;
	i += cpu->byte_order == EMUL_LITTLE_ENDIAN ? 1 : -1;
	data[i] = reg(ic->arg[2] + 4) >> 16;
	i += cpu->byte_order == EMUL_LITTLE_ENDIAN ? 1 : -1;
	data[i] = reg(ic->arg[2] + 4) >> 24;
	i += cpu->byte_order == EMUL_LITTLE_ENDIAN ? 1 : -1;
#endif
#endif
#endif
#endif
	if (!cpu->memory_rw(cpu, cpu->mem, addr, data, datalen,
	    MEM_WRITE, memory_rw_flags)) {
		/*  store failed, an exception was generated  */
		if (!cpu->running)
			cpu->cd.arm.next_ic = &nothing_call;
		return;
	}
#endif

#ifdef A__P
#ifdef A__W
	reg(ic->arg[0]) = wb_addr;		/*  #357  */
#endif
#else	/*  post-index writeback  */
	reg(ic->arg[0]) = wb_addr + offset;	/*  #357  */
#endif
}


/*
 *  Fast load/store, if the page is in the translation array.
 */
void A__NAME(struct cpu *cpu, struct arm_instr_call *ic)
{
#if defined(A__LDRD) || defined(A__STRD)
	/*  Chicken out, let's do this unoptimized for now:  */
	A__NAME__general(cpu, ic);
#else
#ifdef A__REG
	uint32_t (*reg_func)(struct cpu *, struct arm_instr_call *)
	    = (uint32_t (*)(struct cpu *, struct arm_instr_call *))
	      (void *)(size_t)ic->arg[1];
#endif
	uint32_t offset =
#ifndef A__U
	    -
#endif
#ifdef A__REG
	    reg_func(cpu, ic);
#else
	    ic->arg[1];
#endif
	uint32_t addr = reg(ic->arg[0])
#ifdef A__P
	    + offset
#endif
	    ;
	/*
	 *  #357: unmasked, for the writeback -- see A__NAME__general above. It
	 *  must be captured HERE, because unlike the general function this path
	 *  masks `addr` in place further down and separately for each access size
	 *  (the halfword and word arms of both the load and the store), while the
	 *  byte arms mask nothing at all. Deliberately no line numbers: a numeric
	 *  cite in this file has gone stale twice before, and this comment's own
	 *  first draft cited the four pre-patch mask lines, one of which then
	 *  resolved to the middle of this comment.
	 *
	 *  `page` and `is_userpage` below are deliberately still indexed from the
	 *  UNMASKED addr, and that is correct: an AND can only clear bits, and it
	 *  clears at most the low three, so it can never carry into bit 12 --
	 *  (addr & ~mask) >> 12 == addr >> 12 for every size. The mask on the value
	 *  used to index the page is therefore load-bearing for BOUNDS as well as
	 *  for architecture: masked offset + datalen - 1 <= 0xfff for all sizes, so
	 *  the access stays inside the page that was selected, which is what keeps
	 *  the last touched byte in range when the unmasked in-page offset is
	 *  0xfff. Do not "simplify" it away -- that would be a memory defect, not a
	 *  cosmetic one. This became easier to hit with #357, because a base can now
	 *  STAY unaligned across iterations where masking previously healed it after
	 *  one step, so unaligned fast-path accesses are more frequent than before.
	 */
#if !defined(A__P) || defined(A__W)
	const uint32_t wb_addr = addr;
#endif
	unsigned char *page = cpu->cd.arm.
#ifdef A__L
	    host_load
#else
	    host_store
#endif
	    [addr >> 12];


#if !defined(A__P) && defined(A__W)
	/*
	 *  T-bit: userland access: check the corresponding bit in the
	 *  is_userpage array. If it is set, then we're ok. Otherwise: use the
	 *  generic function.
	 */
	uint32_t x = cpu->cd.arm.is_userpage[addr >> 17];
	if (!(x & (1 << ((addr >> 12) & 31))))
		A__NAME__general(cpu, ic);
	else
#endif


	if (page == NULL) {
		A__NAME__general(cpu, ic);
	} else {
#ifdef A__L
#ifdef A__B
		reg(ic->arg[2]) =
#ifdef A__SIGNED
		    (int32_t)(int8_t)
#endif
		    page[addr & 0xfff];
#else
#ifdef A__H
		addr &= ~1;
		reg(ic->arg[2]) =
#ifdef A__SIGNED
		    (int32_t)(int16_t)
#endif
		    (cpu->byte_order == EMUL_LITTLE_ENDIAN
		    ? (page[addr & 0xfff] + (page[(addr & 0xfff) + 1] << 8))
		    : ((page[addr & 0xfff] << 8) + page[(addr & 0xfff) + 1]));
#else
		/*  #362: captured before the mask, and AFTER `page` and
		    `is_userpage` were indexed from the unmasked addr, so #357's
		    bounds argument is untouched. This path already assembles the
		    bytes of the ALIGNED word, so rotating the assembled value is
		    exactly equivalent to re-indexing them -- which is why the fix
		    here is the same three lines as the general path, and not the
		    larger job an earlier round's notes predicted.  */
		const uint32_t rot_sh = 8 * (addr & 3);

		addr &= ~3;
		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
			reg(ic->arg[2]) = page[addr & 0xfff] +
			    (page[(addr & 0xfff) + 1] << 8) +
			    (page[(addr & 0xfff) + 2] << 16) +
			    (page[(addr & 0xfff) + 3] << 24);
		else
			reg(ic->arg[2]) = page[(addr & 0xfff) + 3] +
			    (page[(addr & 0xfff) + 2] << 8) +
			    (page[(addr & 0xfff) + 1] << 16) +
			    (page[(addr & 0xfff) + 0] << 24);
		if (rot_sh)					/*  #362  */
			reg(ic->arg[2]) = (reg(ic->arg[2]) >> rot_sh) |
			    (reg(ic->arg[2]) << (32 - rot_sh));
#endif
#endif
#else
#ifdef A__B
		page[addr & 0xfff] = reg(ic->arg[2]);
#else
#ifdef A__H
		addr &= ~1;
		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)  {
			page[addr & 0xfff] = reg(ic->arg[2]);
			page[(addr & 0xfff)+1] = reg(ic->arg[2]) >> 8;
		} else {
			page[addr & 0xfff] = reg(ic->arg[2]) >> 8;
			page[(addr & 0xfff)+1] = reg(ic->arg[2]);
		}
#else
		addr &= ~3;
		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)  {
			page[addr & 0xfff] = reg(ic->arg[2]);
			page[(addr & 0xfff)+1] = reg(ic->arg[2]) >> 8;
			page[(addr & 0xfff)+2] = reg(ic->arg[2]) >> 16;
			page[(addr & 0xfff)+3] = reg(ic->arg[2]) >> 24;
		} else {
			page[addr & 0xfff] = reg(ic->arg[2]) >> 24;
			page[(addr & 0xfff)+1] = reg(ic->arg[2]) >> 16;
			page[(addr & 0xfff)+2] = reg(ic->arg[2]) >> 8;
			page[(addr & 0xfff)+3] = reg(ic->arg[2]);
		}
#endif
#endif
#endif

		/*  Index Write-back:  */
#ifdef A__P
#ifdef A__W
		reg(ic->arg[0]) = wb_addr;		/*  #357  */
#endif
#else
		/*  post-index writeback  */
		reg(ic->arg[0]) = wb_addr + offset;	/*  #357  */
#endif
	}
#endif	/*  not STRD  */
}


/*
 *  Special case when loading or storing the ARM's PC register, or when the PC
 *  register is used as the base address register.
 *
 *  o)	Loads into the PC register cause a branch. If an exception occured
 *	during the load, then the PC register should already point to the
 *	exception handler, in which case we simply recalculate the pointers a
 *	second time (no harm is done by doing that).
 *
 *	TODO: A tiny performance optimization would be to separate the two
 *	cases: a load where arg[0] = PC, and the case where arg[2] = PC.
 *
 *  o)	Stores store "PC of the current instruction + 12". The solution I have
 *	choosen is to calculate this value and place it into a temporary
 *	variable (tmp_pc), which is then used for the store.
 */
void A__NAME_PC(struct cpu *cpu, struct arm_instr_call *ic)
{
#ifdef A__L
	/*  Load:  */
	if (ic->arg[0] == (size_t)(&cpu->cd.arm.tmp_pc)) {
		/*  tmp_pc = current PC + 8:  */
		uint32_t low_pc, tmp;
		low_pc = ((size_t)ic - (size_t) cpu->cd.arm.cur_ic_page) /
		    sizeof(struct arm_instr_call);
		tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
		    ARM_INSTR_ALIGNMENT_SHIFT);
		tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
		cpu->cd.arm.tmp_pc = tmp + 8;
	}
	A__NAME(cpu, ic);
	if (ic->arg[2] == (size_t)(&cpu->cd.arm.r[ARM_PC])) {
		cpu->pc = cpu->cd.arm.r[ARM_PC];
		quick_pc_to_pointers(cpu);
		if (cpu->machine->show_trace_tree)
			cpu_functioncall_trace(cpu, cpu->pc);
	}
#else
	/*  Store:  */
	uint32_t low_pc, tmp;
	/*  Calculate tmp from this instruction's PC + 12  */
	low_pc = ((size_t)ic - (size_t) cpu->cd.arm.cur_ic_page) /
	    sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->cd.arm.tmp_pc = tmp + 12;
	A__NAME(cpu, ic);
#endif
}


#ifndef A__NOCONDITIONS
/*  Load/stores with all registers except the PC register:  */
void A__NAME__eq(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_Z) A__NAME(cpu, ic); }
void A__NAME__ne(struct cpu *cpu, struct arm_instr_call *ic)
{ if (!(cpu->cd.arm.flags & ARM_F_Z)) A__NAME(cpu, ic); }
void A__NAME__cs(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_C) A__NAME(cpu, ic); }
void A__NAME__cc(struct cpu *cpu, struct arm_instr_call *ic)
{ if (!(cpu->cd.arm.flags & ARM_F_C)) A__NAME(cpu, ic); }
void A__NAME__mi(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_N) A__NAME(cpu, ic); }
void A__NAME__pl(struct cpu *cpu, struct arm_instr_call *ic)
{ if (!(cpu->cd.arm.flags & ARM_F_N)) A__NAME(cpu, ic); }
void A__NAME__vs(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_V) A__NAME(cpu, ic); }
void A__NAME__vc(struct cpu *cpu, struct arm_instr_call *ic)
{ if (!(cpu->cd.arm.flags & ARM_F_V)) A__NAME(cpu, ic); }

void A__NAME__hi(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_C &&
!(cpu->cd.arm.flags & ARM_F_Z)) A__NAME(cpu, ic); }
void A__NAME__ls(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_Z ||
!(cpu->cd.arm.flags & ARM_F_C)) A__NAME(cpu, ic); }
void A__NAME__ge(struct cpu *cpu, struct arm_instr_call *ic)
{ if (((cpu->cd.arm.flags & ARM_F_N)?1:0) ==
((cpu->cd.arm.flags & ARM_F_V)?1:0)) A__NAME(cpu, ic); }
void A__NAME__lt(struct cpu *cpu, struct arm_instr_call *ic)
{ if (((cpu->cd.arm.flags & ARM_F_N)?1:0) !=
((cpu->cd.arm.flags & ARM_F_V)?1:0)) A__NAME(cpu, ic); }
void A__NAME__gt(struct cpu *cpu, struct arm_instr_call *ic)
{ if (((cpu->cd.arm.flags & ARM_F_N)?1:0) ==
((cpu->cd.arm.flags & ARM_F_V)?1:0) &&
!(cpu->cd.arm.flags & ARM_F_Z)) A__NAME(cpu, ic); }
void A__NAME__le(struct cpu *cpu, struct arm_instr_call *ic)
{ if (((cpu->cd.arm.flags & ARM_F_N)?1:0) !=
((cpu->cd.arm.flags & ARM_F_V)?1:0) ||
(cpu->cd.arm.flags & ARM_F_Z)) A__NAME(cpu, ic); }


/*  Load/stores with the PC register:  */
void A__NAME_PC__eq(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_Z) A__NAME_PC(cpu, ic); }
void A__NAME_PC__ne(struct cpu *cpu, struct arm_instr_call *ic)
{ if (!(cpu->cd.arm.flags & ARM_F_Z)) A__NAME_PC(cpu, ic); }
void A__NAME_PC__cs(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_C) A__NAME_PC(cpu, ic); }
void A__NAME_PC__cc(struct cpu *cpu, struct arm_instr_call *ic)
{ if (!(cpu->cd.arm.flags & ARM_F_C)) A__NAME_PC(cpu, ic); }
void A__NAME_PC__mi(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_N) A__NAME_PC(cpu, ic); }
void A__NAME_PC__pl(struct cpu *cpu, struct arm_instr_call *ic)
{ if (!(cpu->cd.arm.flags & ARM_F_N)) A__NAME_PC(cpu, ic); }
void A__NAME_PC__vs(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_V) A__NAME_PC(cpu, ic); }
void A__NAME_PC__vc(struct cpu *cpu, struct arm_instr_call *ic)
{ if (!(cpu->cd.arm.flags & ARM_F_V)) A__NAME_PC(cpu, ic); }

void A__NAME_PC__hi(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_C &&
!(cpu->cd.arm.flags & ARM_F_Z)) A__NAME_PC(cpu, ic); }
void A__NAME_PC__ls(struct cpu *cpu, struct arm_instr_call *ic)
{ if (cpu->cd.arm.flags & ARM_F_Z ||
!(cpu->cd.arm.flags & ARM_F_C)) A__NAME_PC(cpu, ic); }
void A__NAME_PC__ge(struct cpu *cpu, struct arm_instr_call *ic)
{ if (((cpu->cd.arm.flags & ARM_F_N)?1:0) ==
((cpu->cd.arm.flags & ARM_F_V)?1:0)) A__NAME_PC(cpu, ic); }
void A__NAME_PC__lt(struct cpu *cpu, struct arm_instr_call *ic)
{ if (((cpu->cd.arm.flags & ARM_F_N)?1:0) !=
((cpu->cd.arm.flags & ARM_F_V)?1:0)) A__NAME_PC(cpu, ic); }
void A__NAME_PC__gt(struct cpu *cpu, struct arm_instr_call *ic)
{ if (((cpu->cd.arm.flags & ARM_F_N)?1:0) ==
((cpu->cd.arm.flags & ARM_F_V)?1:0) &&
!(cpu->cd.arm.flags & ARM_F_Z)) A__NAME_PC(cpu, ic); }
void A__NAME_PC__le(struct cpu *cpu, struct arm_instr_call *ic)
{ if (((cpu->cd.arm.flags & ARM_F_N)?1:0) !=
((cpu->cd.arm.flags & ARM_F_V)?1:0) ||
(cpu->cd.arm.flags & ARM_F_Z)) A__NAME_PC(cpu, ic); }
#endif


#ifdef A__LDRD
#undef A__LDRD
#endif

#ifdef A__STRD
#undef A__STRD
#endif

