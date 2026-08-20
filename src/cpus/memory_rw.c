/*
 *  Copyright (C) 2003-2021  Anders Gavare.  All rights reserved.
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
 *  Generic memory_rw(), with special hacks for specific CPU families.
 *
 *  Example for inclusion from memory_mips.c:
 *
 *	MEMORY_RW should be mips_memory_rw
 *	MEM_MIPS should be defined
 *
 *
 *  TODO: Cleanup the "ok" variable usage!
 */


/*
 *  memory_rw():
 *
 *  Read or write data from/to memory.
 *
 *	cpu		the cpu doing the read/write
 *	mem		the memory object to use
 *	vaddr		the virtual address
 *	data		a pointer to the data to be written to memory, or
 *			a placeholder for data when reading from memory
 *	len		the length of the 'data' buffer
 *	writeflag	set to MEM_READ or MEM_WRITE
 *	misc_flags	CACHE_{NONE,DATA,INSTRUCTION} | other flags
 *
 *  If the address indicates access to a memory mapped device, that device'
 *  read/write access function is called.
 *
 *  This function should not be called with cpu == NULL.
 *
 *  Returns one of the following:
 *	MEMORY_ACCESS_FAILED
 *	MEMORY_ACCESS_OK
 *
 *  (MEMORY_ACCESS_FAILED is 0.)
 */

/*
 *  #430: THE PAGE SIZE, IN ONE PLACE.
 *
 *  It was a local inside the function.  The wrapper below needs the same number, and two
 *  copies of a page size that can silently diverge is the shape this tree has been bitten
 *  by before -- so it is hoisted to a macro and the local now reads it.  Note the Alpha
 *  value: it is 8 KB, not 4 KB, so anything that splits at "the page boundary" must use
 *  THIS and never a literal 4096.  A review seat caught exactly that hazard in the design
 *  brief, which had said "4 KB page" throughout.
 */
#ifdef MEM_ALPHA
#define	MRW_OFFSET_MASK		0x1fff
#else
#define	MRW_OFFSET_MASK		0xfff
#endif

/*
 *  #430: THE SPLIT GRANULE IS 1 KB, AND IT IS NOT THE SAME NUMBER AS THE MASK ABOVE.
 *
 *  MRW_OFFSET_MASK is the HOST-page granule: what memory_paddr_to_hostaddr() is asked for
 *  and what update_translation_table() caches.  The granule the SPLIT needs is a different
 *  thing -- the smallest unit at which a translator in this tree can send two adjacent
 *  virtual addresses to unrelated physical ones -- and it is SMALLER:
 *
 *      memory_arm.c:198-207   descriptor type 3 on a non-XScale core is a 1 KB page,
 *                             *return_paddr = (d2 & 0xfffffc00) | (vaddr & 0x3ff)
 *      memory_sh.c:116        SH4_PTEL_SZ_1K gives mask 0xfffffc00
 *      memory_mips_v2p.c      the VR41xx path likewise has 1 KB logic
 *
 *  A first draft of this split used the 4 KB mask and a review seat produced the
 *  counterexample: with a 1 KB mapping, a four-byte access at 0x13fe crosses a translation
 *  boundary but NOT a 4 KB one, so the loop never fired and the defect survived exactly
 *  where MEMORY_NOT_FULL_PAGE says it is most likely.  Splitting finer is always SAFE --
 *  each chunk is then inside one mapping for every translator here, and the worker's own
 *  host-page arithmetic is unchanged -- so the only cost is more worker calls on the slow
 *  path for a multi-page translated access, which is rare (large transfers are PHYSICAL
 *  and exempt).  Correctness at a known granule beats a faster one that is wrong on ARM.
 */
#define	MRW_SPLIT_MASK		0x3ff

/*  The one-page worker; its name is derived from MEMORY_RW because cpu_alpha.c includes
    this file TWICE in one translation unit (alpha_userland_memory_rw, then alpha_memory_rw
    via tmp_alpha_tail.c), so a plainly named static would be a redefinition.  */
#ifndef MRW_CAT2
#define	MRW_CAT2(a,b)		a##b
#define	MRW_CAT(a,b)		MRW_CAT2(a,b)
#endif
#define	MEMORY_RW_ONE_PAGE	MRW_CAT(MEMORY_RW, _one_page)

/*
 *  The one relationship between the two that MUST hold, asserted at COMPILE TIME because it
 *  cannot be asserted at run time by the offline differential.
 *
 *  MEM_ALPHA is never compiled by that differential -- its fixture is 4 KB-specific -- so a
 *  review seat MEASURED that widening MRW_OFFSET_MASK, or hardcoding the worker's local back
 *  to 0xfff (exactly the drift this macro exists to prevent), leaves every row green.  A
 *  static assertion costs nothing and covers the Alpha build the test cannot reach.  The
 *  name is derived because this file is included twice per translation unit.
 */
typedef char MRW_CAT(MEMORY_RW, _split_le_page)
    [(MRW_SPLIT_MASK) <= (MRW_OFFSET_MASK) ? 1 : -1];

static int MEMORY_RW_ONE_PAGE(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
	unsigned char *data, size_t len, int writeflag, int misc_flags);


/*
 *  #430: TRANSLATE ONCE PER PAGE, NOT ONCE PER ACCESS.
 *
 *  The worker below translates the START vaddr and then copies the whole length from the
 *  host pointer for THAT page.  memory_paddr_to_hostaddr() returns a pointer into a 1 MB
 *  memblock, so the copy walks host memory that is contiguous PHYSICALLY while the guest's
 *  span is contiguous VIRTUALLY.  Those coincide only by luck, and the moment the length
 *  carries past the page boundary the guest reads -- or OVERWRITES -- whatever physical
 *  page happens to follow.  Measured offline against a deliberately non-monotonic map: a
 *  straddling read returned the physically-following page's bytes, and a straddling WRITE
 *  left the guest's intended page untouched while corrupting an unrelated one.  Measured
 *  too: when the tail page had no valid translation the old code returned
 *  MEMORY_ACCESS_OK anyway, so this was a MISSING FAULT as well as a wrong page.
 *
 *  The existing split at the end of the worker is NOT this guard and must not be mistaken
 *  for it: it fires at BITS_PER_MEMBLOCK (1 MB) granularity and its job is to stop the memcpy
 *  running off the end of a host allocation.
 *
 *  It is ONE BOUNDARY IN 1024, not 256: MRW_SPLIT_MASK is 0x3ff, so the split granule is
 *  1024 bytes and 1 MB / 1024 = 1024.  The old "256" came from dividing 1 MB by a 4 KB page
 *  -- a granule this split does not use, as the note above says: "The granule the SPLIT
 *  needs is a different one."  (And per that note the real page here is 8 KB anyway.)
 *
 *  Two properties of the memblock split, both MEASURED:
 *    - post-#430 it fires only on PHYSICAL accesses.  A TRANSLATED 4096-byte write across a
 *      1 MB boundary is chunked at the 1024-byte SPLIT granule, so it costs 4 translations
 *      and 4 host lookups and never reaches here; PHYSICAL costs 0 and 2.  A chunk of at
 *      most one granule, granule-aligned, cannot cross 1 MB.
 *    - its head can NEVER be a device, in either version: device dispatch `goto
 *      do_return_ok`s first.  Measured with a device straddling the memblock boundary --
 *      one device call, offset 0xffe, len 4, zero host lookups.
 *
 *  A LOOP, not recursion.  A recursive split costs a real frame per chunk when the compiler
 *  does NOT eliminate the tail call -- measured at -O0, 1,834,896 bytes of stack for a 16 MB
 *  access -- and a large enough access then dies on the stack rather than returning an
 *  answer.
 *
 *  CORRECTION, and it is the reason this paragraph is worded carefully: the first draft said
 *  "gcc does not turn the tail call into a loop at -O2".  MEASURED, IT DOES -- gcc 15.2.1
 *  performs the sibling-call optimisation at -O2 and -O3, leaving a 96-byte span.  So the
 *  loop is still the right implementation (it does not depend on an optimisation being
 *  applied, and -O0 builds and other compilers are real), but the justification was wrong,
 *  and the row that certified it was VACUOUS until the differential was given
 *  -fno-optimize-sibling-calls.  No caller in the tree passes an access large enough for
 *  this to bite today; it is insurance, and it costs about fifteen lines.
 *
 *  ONLY WHEN A TRANSLATION ACTUALLY HAPPENS.  Under PHYSICAL (or with no translate_v2p)
 *  paddr == vaddr, there is no per-page mapping to redo, and splitting would buy nothing
 *  while turning one large DMA into thousands of calls -- so those go straight through and
 *  the memblock split keeps doing its job unchanged.
 */
int MEMORY_RW(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
	unsigned char *data, size_t len, int writeflag, int misc_flags)
{
	if (!(misc_flags & PHYSICAL) && cpu->translate_v2p != NULL) {
		size_t granule = (size_t) MRW_SPLIT_MASK + 1;
		size_t offset = (size_t) (vaddr & MRW_SPLIT_MASK);

		/*  `len > granule - offset`, NOT `offset + len > granule`: the sum can
		    wrap for an absurd length (offset 1, len SIZE_MAX), which would skip
		    the loop and hand the whole thing to the worker.  The subtraction
		    cannot wrap, because offset < granule always.

		    STATED EXACTLY, because the first version of this comment implied more
		    than it delivers: this form does not SERVICE such a length, it declines
		    to mis-copy it.  A length near SIZE_MAX now iterates about 2^54 times
		    instead of silently under-splitting -- measured, a fuzz watchdog fired
		    at two million chunks.  No caller passes anything remotely like it (the
		    largest in the tree are PHYSICAL and exempt), so the case is recorded
		    and filed rather than handled.  */
		while (len > granule - offset) {
			size_t head = granule - offset;

			if (!MEMORY_RW_ONE_PAGE(cpu, mem, vaddr, data, head,
			    writeflag, misc_flags)) {
				/*  #244 PROMISES THE WHOLE READ BUFFER, AND SPLITTING BROKE
				    THAT: the worker zeroes only the chunk IT was given, so a
				    failure before the last chunk used to leave the caller's
				    remaining bytes untouched -- uninitialised host stack, for
				    a caller that ignores the return value.  Unsplit, one call
				    covered the whole length.  Zero the rest here so the
				    guarantee is the same as it was.  */
				if (writeflag == MEM_READ)
					memset(data, 0, len);
				return MEMORY_ACCESS_FAILED;
			}

			vaddr += head;
			data += head;
			len -= head;
			offset = 0;
		}
	}

	return MEMORY_RW_ONE_PAGE(cpu, mem, vaddr, data, len, writeflag, misc_flags);
}


static int MEMORY_RW_ONE_PAGE(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
	unsigned char *data, size_t len, int writeflag, int misc_flags)
{
	const int offset_mask = MRW_OFFSET_MASK;

	int ok = 2;
	uint64_t paddr;
	int cache, no_exceptions, offset;
	unsigned char *memblock;
	int dyntrans_device_danger = 0;

	no_exceptions = misc_flags & NO_EXCEPTIONS;
	cache = misc_flags & CACHE_FLAGS_MASK;


	if (misc_flags & PHYSICAL || cpu->translate_v2p == NULL) {
		paddr = vaddr;
	} else {
		ok = cpu->translate_v2p(cpu, vaddr, &paddr,
		    (writeflag? FLAG_WRITEFLAG : 0) +
		    (no_exceptions? FLAG_NOEXCEPTIONS : 0)
		    + (misc_flags & MEMORY_USER_ACCESS)
		    + (cache==CACHE_INSTRUCTION? FLAG_INSTR : 0));

		/*
		 *  If the translation caused an exception, or was invalid in
		 *  some way, then simply return without doing the memory
		 *  access:
		 */
		if (!ok) {
			/*  #244: A failed (or NO_EXCEPTIONS) translation leaves
			    the caller's read buffer untouched; zero it so
			    callers that ignore the return value (e.g. the DEC
			    PROM string helpers) consume deterministic 0 bytes
			    instead of uninitialised host stack. Same zero-fill
			    ethos as the failed-device-read path (#95).  */
			if (writeflag == MEM_READ)
				memset(data, 0, len);
			return MEMORY_ACCESS_FAILED;
		}
	}

	/*
	 *  #250: data write-watchpoint. Checked here, before the device /
	 *  cache / RAM dispatch (several of which return early — notably the
	 *  R3000 cached path via memory_cache_R3000()), so every store that
	 *  reaches this slow path is covered. Watched pages are kept off the
	 *  fast store table by update_translation_table(), and R3000 cached
	 *  data already comes through here. Show the store (writer pc, target,
	 *  width, value) and request entry into the debugger after the current
	 *  instruction, via the same about_to_enter_single_step mechanism as
	 *  subsystem breakpoints. NOP unless a watchpoint is set.
	 */
	if (writeflag == MEM_WRITE && cpu->machine->watchpoints.n != 0 &&
	    !single_step && !about_to_enter_single_step &&
	    machine_watchpoint_match(cpu->machine, paddr, len)) {
		char valbuf[3 * 16 + 1];
		size_t vi, vn = len < 16 ? len : 16;
		valbuf[0] = '\0';
		for (vi = 0; vi < vn; vi++)
			snprintf(valbuf + strlen(valbuf),
			    sizeof(valbuf) - strlen(valbuf), "%s%02x",
			    vi ? " " : "", data[vi]);
		fatal("[ WATCHPOINT: write of %i byte(s) to vaddr 0x%" PRIx64
		    " (paddr 0x%" PRIx64") = %s%s, pc = 0x%" PRIx64" ]\n",
		    (int) len, (uint64_t) vaddr, (uint64_t) paddr, valbuf,
		    len > 16 ? " ..." : "", (uint64_t) cpu->pc);
		about_to_enter_single_step = true;
	}

#if 0
	/*
	 *  For quick-and-dirty debugging of 32-bit code, typically
	 *  unknown ROM code:  Write out a summary of accessed memory ranges.
	 */
	if (cpu->running && paddr < 0x00300000)
	{
		static int swriteflag = -1, lastswriteflag;
		static int32_t start = -1, stop = -1;
		static int32_t laststart = -1, laststop = -1;

		if (start == -1)
		{
			start = stop = paddr;
			swriteflag = writeflag;
		}
		else
		{
			if (paddr == stop + len && writeflag == swriteflag)
			{
				stop = paddr;
			}
			else
			{
				if (start != laststart || stop != laststop || swriteflag != lastswriteflag)
				{
					printf("%s  %08x -- %08x  %i-bit\n",
						swriteflag ? "WRITE" : "READ ",
						(int)start, (int)(stop + len - 1), (int)len*8);
				}

				laststart = start; laststop = stop; lastswriteflag = swriteflag;

				start = stop = paddr;
				swriteflag = writeflag;
			}
		}

		// Make sure the access is not put into quick lookup tables:
		ok |= MEMORY_NOT_FULL_PAGE;
	}
#endif

#if 0
	/*
	 *  For quick-and-dirty test to see which memory addresses are in use,
	 *  making a "waterfall spectrum"...
	 */
	if (cpu->running && (paddr < 0x200000 ||
		(paddr >= 0x0c000000 && paddr < 0x0d000000)))
	{
		int64_t xsize = 1920, ysize = 1080;
		static int y = 0;
		static int count = 0;
		static uint8_t* buf = NULL;

		if (buf == NULL)
		{
			buf = (uint8_t*)malloc(xsize * ysize*3);
			memset(buf, 0xff, xsize * ysize*3);
		}

		uint64_t paddr2 = paddr - 0x0c000000;
		
		if (paddr < 0x200000)
			paddr2 = paddr + 16*1048576;

		int64_t max = 16*1048576 + (2*1048576);

		int64_t x = xsize * paddr2 / max;

		if (x >= 0 && x < xsize)
		{
			if (writeflag)
			{
				int c = buf[(x+y*xsize)*3+0];
				if (c == 255)
					c = 128;
				else if (c > 0)
				{
					c = c - 8;
				}

				buf[(x+y*xsize)*3+1] = c;
				buf[(x+y*xsize)*3+2] = c;
			}
			else
			{
				int c = buf[(x+y*xsize)*3+1];
				if (c == 255)
					c = 128;
				else if (c > 0)
				{
					c = c - 8;
				}

				buf[(x+y*xsize)*3+0] = c;
				buf[(x+y*xsize)*3+2] = c;
			}
		}
		
		for (int meg = 0; meg < 18; ++meg)
			buf[((xsize * (meg * 0x100000LL) / max) +y*xsize)*3+1] = 64;

		count ++;
		if (count >= 8192)
		{
			count = 0;
			y ++;
			
			if (y >= ysize)
			{
				static int n = 0;
				char name[40];
				snprintf(name, sizeof(name), "memory_%05i.ppm", n++);
				FILE* f = fopen(name, "w");
				printf("writing out %s\n", name);
				fprintf(f, "P6\n%i %i\n255\n", (int)xsize, (int)ysize);
				fwrite((char*)buf, 1, (int)(xsize*ysize*3), f);
				fclose(f);
				memset(buf, 0xff, xsize*ysize);
				y = 0;
			}
		}
		
		// Make sure the access is not put into quick lookup tables:
		ok |= MEMORY_NOT_FULL_PAGE;
	}
#endif

	/*
	 *  Memory mapped device?
	 *
	 *  TODO: if paddr < base, but len enough, then the device should
	 *  still be written to!
	 */
	if (paddr >= mem->mmap_dev_minaddr && paddr < mem->mmap_dev_maxaddr) {
		uint64_t orig_paddr = paddr;
		int i, start, end, res;

#if 0

TODO: The correct solution for this is to add RAM devices _around_ the
dangerous device. The solution below incurs a slowdown for _everything_,
not just the device in question.

		/*
		 *  Really really slow, but unfortunately necessary. This is
		 *  to avoid the folowing scenario:
		 *
		 *	a) offsets 0x000..0x123 are normal memory
		 *	b) offsets 0x124..0x777 are a device
		 *
		 *	1) a read is done from offset 0x100. the page is
		 *	   added to the dyntrans system as a "RAM" page
		 *	2) a dyntranslated read is done from offset 0x200,
		 *	   which should access the device, but since the
		 *	   entire page is added, it will access non-existant
		 *	   RAM instead, without warning.
		 *
		 *  Setting dyntrans_device_danger = 1 on accesses which are
		 *  on _any_ offset on pages that are device mapped avoids
		 *  this problem, but it is probably not very fast.
		 *
		 *  TODO: Convert this into a quick (multi-level, 64-bit)
		 *  address space lookup, to find dangerous pages.
		 */
		for (i=0; i<mem->n_mmapped_devices; i++)
			if (paddr >= (mem->devices[i].baseaddr & ~offset_mask)&&
			    paddr <= ((mem->devices[i].endaddr-1)|offset_mask)){
				dyntrans_device_danger = 1;
				break;
			}
#endif

		start = 0; end = mem->n_mmapped_devices - 1;
		i = mem->last_accessed_device;

		/*  Scan through all devices:  */
		do {
			if (paddr >= mem->devices[i].baseaddr &&
			    paddr < mem->devices[i].endaddr) {
				/*  Found a device, let's access it:  */
				mem->last_accessed_device = i;

				/*  #95: zero the caller's buffer up front on a read
				    so a device handler that fills only part of it --
				    or whose access is len-clamped just below -- can
				    never hand back uninitialised host memory to the
				    guest.  Root-cause fix for the uninit-read class
				    (cf. per-device #91/#93/#94).  */
				if (writeflag == MEM_READ)
					memset(data, 0, len);

				paddr -= mem->devices[i].baseaddr;
				if (paddr + len > mem->devices[i].length) {
					/*  Note the truncation per the
					    warn-loudly ethos, but only at
					    debug verbosity (-v) and at most
					    8 times (single-threaded), since
					    probing at the end of a device's
					    mapped range is common and benign
					    (cf. the unwarned zero-fill in
					    #95/#119 above).  */
					static int n_trunc_msgs = 0;
					if (ENOUGH_VERBOSITY(SUBSYS_MEMORY,
					    VERBOSITY_DEBUG) &&
					    n_trunc_msgs < 8) {
						n_trunc_msgs ++;
						debugmsg_cpu(cpu,
						    SUBSYS_MEMORY,
						    mem->devices[i].name,
						    VERBOSITY_DEBUG,
						    "%s truncated at end of"
						    " device: offset 0x%llx,"
						    " len %i -> %i",
						    writeflag == MEM_WRITE ?
						    "write" : "read",
						    (long long) paddr,
						    (int) len,
						    (int) (mem->devices[i].
						    length - paddr));
					}
					len = mem->devices[i].length - paddr;
				}

				if (cpu->update_translation_table != NULL &&
				    !(ok & MEMORY_NOT_FULL_PAGE) &&
				    mem->devices[i].flags & DM_DYNTRANS_OK) {
					int wf = writeflag == MEM_WRITE? 1 : 0;
					unsigned char *host_addr;

					if (!(mem->devices[i].flags &
					    DM_DYNTRANS_WRITE_OK))
						wf = 0;

					if (writeflag && wf) {
						if (paddr < mem->devices[i].
						    dyntrans_write_low)
							mem->devices[i].
							dyntrans_write_low =
							    paddr &~offset_mask;
						if (paddr >= mem->devices[i].
						    dyntrans_write_high)
							mem->devices[i].
						 	dyntrans_write_high =
							    paddr | offset_mask;
					}

					if (mem->devices[i].flags &
					    DM_EMULATED_RAM) {
						/*  MEM_WRITE to force the page
						    to be allocated, if it
						    wasn't already  */
						uint64_t *pp = (uint64_t *)mem->
						    devices[i].dyntrans_data;
						uint64_t p = orig_paddr - *pp;
						host_addr =
						    memory_paddr_to_hostaddr(
						    mem, p & ~offset_mask,
						    MEM_WRITE);
					} else if ((paddr | offset_mask) <
					    mem->devices[i].length) {
						host_addr = mem->devices[i].
						    dyntrans_data +
						    (paddr & ~offset_mask);
					} else {
						/*  #155: (Codex/Fable)
						    don't install dyntrans
						    fast-path access to a
						    device page that is not
						    fully backed; keep it on
						    the bounded slow path.  */
						host_addr = NULL;
					}

					if (host_addr != NULL)
						cpu->update_translation_table(
						    cpu, vaddr & ~offset_mask,
						    host_addr, wf,
						    orig_paddr & ~offset_mask);
				}

				res = 0;
				if (!no_exceptions || (mem->devices[i].flags &
				    DM_READS_HAVE_NO_SIDE_EFFECTS)) {
					bool running_before_device_access = cpu->running;
					res = mem->devices[i].f(cpu, mem, paddr,
					    data, len, writeflag,
					    mem->devices[i].extra);

					if (running_before_device_access && !cpu->running)
						return MEMORY_ACCESS_FAILED;
				}

				if (res == 0)
					res = -1;

				/*
				 *  If accessing the memory mapped device
				 *  failed, then return with an exception.
				 *  (Architecture specific.)
				 */
				if (res <= 0 && !no_exceptions) {
					debug("[ %s device '%s' addr %08lx "
					    "failed ]\n", writeflag?
					    "writing to" : "reading from",
					    mem->devices[i].name, (long)paddr);
#ifdef MEM_MIPS
					mips_cpu_exception(cpu,
					    cache == CACHE_INSTRUCTION?
					    EXCEPTION_IBE : EXCEPTION_DBE,
					    0, vaddr, 0, 0, 0, 0);
#endif
#ifdef MEM_M88K
					/*  TODO: This is enough for
					    OpenBSD/mvme88k's badaddr()
					    implementation... but the
					    faulting address should probably
					    be included somewhere too!  */
					m88k_exception(cpu, cache == CACHE_INSTRUCTION
					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
					    : M88K_EXCEPTION_DATA_ACCESS, 0);
#endif
					return MEMORY_ACCESS_FAILED;
				}
				goto do_return_ok;
			}

			if (paddr < mem->devices[i].baseaddr)
				end = i - 1;
			if (paddr >= mem->devices[i].endaddr)
				start = i + 1;
			i = (start + end) >> 1;
		} while (start <= end);
	}


#ifdef MEM_MIPS
	/*
	 *  Data and instruction cache emulation:
	 */

	switch (cpu->cd.mips.cpu_type.mmu_model) {
	case MMU3K:
		/*  if not uncached addess  (TODO: generalize this)  */
		if (!(misc_flags & PHYSICAL) && cache != CACHE_NONE &&
		    !((vaddr & 0xffffffffULL) >= 0xa0000000ULL &&
		      (vaddr & 0xffffffffULL) <= 0xbfffffffULL)) {
			if (memory_cache_R3000(cpu, cache, paddr,
			    writeflag, len, data))
				goto do_return_ok;
		}
		break;
	default:
		/*  R4000 etc  */
		/*  TODO  */
		;
	}
#endif	/*  MEM_MIPS  */


	/*  Outside of physical RAM?  */
	if (paddr >= mem->physical_max) {
#ifdef MEM_MIPS
		if ((paddr & 0xffffc00000ULL) == 0x1fc00000) {
			/*  Ok, this is PROM stuff  */
		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
			/*  Sprite reads from this area of memory...  */
			/*  TODO: is this still correct?  */
			if (writeflag == MEM_READ)
				memset(data, 0, len);
			goto do_return_ok;
		} else
#endif /* MIPS */
		{
			if (paddr >= mem->physical_max && !no_exceptions)
				if (memory_warn_about_unimplemented_addr
				    (cpu, mem, writeflag, paddr, len))
					return MEMORY_ACCESS_FAILED;

			if (writeflag == MEM_READ) {
				/*  Return all zeroes? (Or 0xff? TODO)  */
				memset(data, 0, len);

#if 0
/*
 *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
 *  I think I introduced it because it was how some guest OS (NetBSD?) detected
 *  the amount of RAM on some machine.
 *
 *  TODO: Figure out if it is not needed anymore, and remove it completely.
 */
#ifdef MEM_MIPS
				/*
				 *  For real data/instruction accesses, cause
				 *  an exceptions on an illegal read:
				 */
				if (cache != CACHE_NONE && !no_exceptions &&
				    paddr >= mem->physical_max &&
				    paddr < mem->physical_max+1048576) {
					mips_cpu_exception(cpu,
					    EXCEPTION_DBE, 0, vaddr, 0,
					    0, 0, 0);
				}
#endif  /*  MEM_MIPS  */
#endif
			}

			/*  Hm? Shouldn't there be a DBE exception for
			    invalid writes as well?  TODO  */

			goto do_return_ok;
		}
	}


	/*
	 *  Uncached access:
	 *
	 *  1)  Translate the physical address to a host address.
	 *
	 *  2)  Insert this virtual->physical->host translation into the
	 *      fast translation arrays (using update_translation_table()).
	 *
	 *  3)  If this was a Write, then invalidate any code translations
	 *      in that page.
	 */
	memblock = memory_paddr_to_hostaddr(mem, paddr & ~offset_mask,
	    writeflag);
	if (memblock == NULL) {
		if (writeflag == MEM_READ)
			memset(data, 0, len);
		goto do_return_ok;
	}

	offset = paddr & offset_mask;

	if (cpu->update_translation_table != NULL && !dyntrans_device_danger
#ifdef MEM_MIPS
	    /*  Ugly hack for R2000/R3000 caches:  */
	    && (cpu->cd.mips.cpu_type.mmu_model != MMU3K ||
            !(cpu->cd.mips.coproc[0]->reg[COP0_STATUS] & MIPS1_ISOL_CACHES))
#endif
	    && !(ok & MEMORY_NOT_FULL_PAGE)
	    && !no_exceptions)
		cpu->update_translation_table(cpu, vaddr & ~offset_mask,
		    memblock, (misc_flags & MEMORY_USER_ACCESS) |
		    (cache == CACHE_INSTRUCTION?
			(writeflag == MEM_WRITE? 1 : 0) : ok - 1),
		    paddr & ~offset_mask);

	/*
	 *  If writing, or if mapping a page where writing is ok later on,
	 *  then invalidate code translations for the (physical) page address:
	 */

	if ((writeflag == MEM_WRITE
	    || (ok == 2 && cache == CACHE_DATA)
	    ) && cpu->invalidate_code_translation != NULL)
		cpu->invalidate_code_translation(cpu, paddr, INVALIDATE_PADDR);

	if ((paddr&((1<<BITS_PER_MEMBLOCK)-1)) + len > (1<<BITS_PER_MEMBLOCK)) {
		/*  #165: (Codex/Fable) split accesses that cross a memblock
		    boundary (e.g. large DMA transfers) at the boundary,
		    instead of exiting the whole emulator.  */
		size_t len_head = (size_t) ((1<<BITS_PER_MEMBLOCK) -
		    (paddr & ((1<<BITS_PER_MEMBLOCK)-1)));

		if (writeflag == MEM_WRITE)
			memcpy(memblock + offset, data, len_head);
		else
			memcpy(data, memblock + offset, len_head);

		return MEMORY_RW(cpu, mem, vaddr + len_head, data + len_head,
		    len - len_head, writeflag, misc_flags);
	}

	/*  And finally, read or write the data:  */
	if (writeflag == MEM_WRITE)
		memcpy(memblock + offset, data, len);
	else
		memcpy(data, memblock + offset, len);

do_return_ok:
	return MEMORY_ACCESS_OK;
}

/*  #430: this file is included more than once per translation unit (see cpu_alpha.c), so
    the per-inclusion macros must not leak into the next inclusion.  MRW_CAT/MRW_CAT2 are
    inclusion-independent and are left defined behind their own guard.  */
#undef MEMORY_RW_ONE_PAGE
#undef MRW_OFFSET_MASK
#undef MRW_SPLIT_MASK

