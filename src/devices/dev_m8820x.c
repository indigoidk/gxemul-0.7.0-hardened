/*
 *  Copyright (C) 2007-2021  Anders Gavare.  All rights reserved.
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
 *  COMMENT: M88200/M88204 CMMU (Cache/Memory Management Unit)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cpu.h"
#include "device.h"
#include "emul.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"

#include "thirdparty/m8820x.h"
#include "thirdparty/m8820x_pte.h"


struct m8820x_data {
	int		cpu_nr;
	int		cmmu_nr;

	/*
	 *  #433: COMPLAIN ONCE, NOT ONCE PER ACCESS.
	 *
	 *  Per DEVICE INSTANCE -- there are two CMMUs per CPU and up to eight in a machine --
	 *  so the first unmodelled access of each kind is reported in full, naming the
	 *  instance, and the rest go to debug().  Measured basis: a real OpenBSD/luna88k boot
	 *  writes CMMU_SCR 640,016 times in 132 s, about 4,850 per second, so an unlatched
	 *  fatal() on that path is a guest-drivable unbounded stderr write -- the `cflood`
	 *  class -- at roughly a quarter of a megabyte per second.
	 */
	int		reported_offset;
	int		reported_command;
};


/*
 *  #433: the shared complain-once helper for an access the model does not implement.
 *
 *  Every site that used to call exit(1) calls this instead.  Terminating the HOST process is
 *  not a behaviour the emulated machine can have, and MEASURED, 1007 of 1024 word offsets in
 *  this device's window did exactly that on a plain READ -- reachable by one supervisor-mode
 *  instruction on luna88k, which boots in this tree.
 *
 *  Why complain-and-continue rather than cpu->running = 0: the tree already assigns those two
 *  shapes to two MEANINGS, and #220 is the precedent for both -- dev_footbridge.c:348 halts
 *  because THE GUEST ASKED THE MACHINE TO HALT, while :379 complains and continues for an
 *  out-of-range PCI bus, which is a model gap.  Every site here is the second kind.  A guest
 *  probing an unimplemented register should not forfeit its session.
 */
static void m8820x_unimplemented(struct m8820x_data *d, const char *what)
{
	if (!d->reported_offset) {
		d->reported_offset = 1;
		fatal("[ m8820x: cpu%i cmmu%i: unimplemented %s; ignored "
		    "(reported once) ]\n", d->cpu_nr, d->cmmu_nr, what);
	} else {
		debug("[ m8820x: cpu%i cmmu%i: unimplemented %s; ignored ]\n",
		    d->cpu_nr, d->cmmu_nr, what);
	}
}


/*
 *  m8820x_command():
 *
 *  Handle M8820x commands written to the System Command Register.
 */
static void m8820x_command(struct cpu *cpu, struct m8820x_data *d)
{
	uint32_t *regs = cpu->cd.m88k.cmmu[d->cmmu_nr]->reg;
	int cmd = regs[CMMU_SCR];
	uint32_t sar = regs[CMMU_SAR];
	size_t i;
	uint32_t super, all;

	switch (cmd) {

	case CMMU_FLUSH_CACHE_CB_LINE:
	case CMMU_FLUSH_CACHE_CB_PAGE:
	case CMMU_FLUSH_CACHE_CB_SEGMENT:	/*  #433  */
	case CMMU_FLUSH_CACHE_CB_ALL:		/*  #433  */
	case CMMU_FLUSH_CACHE_INV_LINE:
	case CMMU_FLUSH_CACHE_INV_PAGE:
	case CMMU_FLUSH_CACHE_INV_SEGMENT:	/*  #433  */
	case CMMU_FLUSH_CACHE_INV_ALL:
	case CMMU_FLUSH_CACHE_CBI_LINE:
	case CMMU_FLUSH_CACHE_CBI_PAGE:
	case CMMU_FLUSH_CACHE_CBI_SEGMENT:
	case CMMU_FLUSH_CACHE_CBI_ALL:
		/*  TODO: this model has no cache, so every cache command is a no-op.  #433
		    added the three SEGMENT/ALL variants that were falling through to the
		    default arm and killing the host; they are no-ops for exactly the same
		    reason as the nine that were already here.  */
		break;

	case CMMU_FLUSH_USER_LINE:		/*  #433  */
	case CMMU_FLUSH_USER_PAGE:
	case CMMU_FLUSH_USER_SEGMENT:		/*  #433  */
	case CMMU_FLUSH_USER_ALL:
	case CMMU_FLUSH_SUPER_LINE:		/*  #433  */
	case CMMU_FLUSH_SUPER_PAGE:
	case CMMU_FLUSH_SUPER_SEGMENT:		/*  #433  */
	case CMMU_FLUSH_SUPER_ALL:
		/*
		 *  #433: THE FOUR LINE/SEGMENT VARIANTS ARE FOLDED IN HERE, AND THAT FOLD IS
		 *  WHY THE REST OF THIS ROUND IS SAFE TO MAKE AT ALL.
		 *
		 *  These are PATC (TLB) flushes.  Before this round an unimplemented
		 *  0x30/0x32/0x34/0x36 died LOUDLY, so no silent path existed.  Converting the
		 *  default arm to complain-and-drop -- which is the rest of this round -- would
		 *  have turned FLUSH_SUPER_LINE into a SILENTLY IGNORED TLB FLUSH.  That is not
		 *  a cosmetic gap: memory_m88k.c:190-234 is the translation fast path, and a
		 *  valid matching PATC entry SHORT-CIRCUITS the table walk and returns the
		 *  cached physical address, so a guest that edited a PTE and issued
		 *  FLUSH_SUPER_LINE would keep translating through the torn-down mapping.
		 *  The fix and the fold are ONE change: without the fold, the fix would
		 *  introduce a defect worse than the crash it removes.  0x34 is also ONE BIT
		 *  from 0x35, which a measured boot issues 158,664 times.
		 *
		 *  LINE takes PAGE's settings and SEGMENT takes ALL's.  A line lies within a
		 *  page and the PATC is page-granular, so LINE is exactly PAGE here; SEGMENT
		 *  over-invalidates, which is architecturally safe in a model that re-walks the
		 *  tables on a miss -- the cost is performance, never correctness.  What real
		 *  silicon does at segment granularity is UNKNOWN (there is no 88200/88204
		 *  manual in this project) and the safe direction does not depend on it.
		 */
		all = super = 0;
		if (cmd == CMMU_FLUSH_USER_ALL ||
		    cmd == CMMU_FLUSH_SUPER_ALL ||
		    cmd == CMMU_FLUSH_USER_SEGMENT ||
		    cmd == CMMU_FLUSH_SUPER_SEGMENT)
			all = 1;
		if (cmd == CMMU_FLUSH_SUPER_ALL ||
		    cmd == CMMU_FLUSH_SUPER_PAGE ||
		    cmd == CMMU_FLUSH_SUPER_LINE ||
		    cmd == CMMU_FLUSH_SUPER_SEGMENT)
			super = M8820X_PATC_SUPERVISOR_BIT;

		/*  TODO: Don't invalidate EVERYTHING like this!  */
		cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);

		for (i=0; i<N_M88200_PATC_ENTRIES; i++) {
			uint32_t v = cpu->cd.m88k.cmmu[d->cmmu_nr]
			    ->patc_v_and_control[i];
			uint32_t p = cpu->cd.m88k.cmmu[d->cmmu_nr]
			    ->patc_p_and_supervisorbit[i];

			/*  Already invalid? Then skip this entry.  */
			if (!(v & PG_V))
				continue;

			/*  Super/user mismatch? Then skip the entry.  */
			if ((p & M8820X_PATC_SUPERVISOR_BIT) != super)
				continue;

			/*  If not all pages are to be invalidated, there
			    must be a virtual address match:  */
			if (!all && (sar & 0xfffff000) != (v & 0xfffff000))
				continue;

			/*  Finally, invalidate the entry:  */
			cpu->cd.m88k.cmmu[d->cmmu_nr]->patc_v_and_control[i]
			    = v & ~PG_V;
		}

		break;

	default:
		/*
		 *  #433: this used to exit(1) -- a guest COMMAND killed the HOST process.
		 *  Measured: reachable by ONE supervisor-mode instruction, and CMMU_SCR is
		 *  written 640,016 times in a single boot, so this arm sat one flipped bit
		 *  away from an ordinary hot path.
		 *
		 *  After the fold above, what actually reaches here is the two PROBEs
		 *  (0x20 PROBE_USER, 0x24 PROBE_SUPER) and undefined values.  A dropped probe
		 *  leaves regs[CMMU_SSR] at zero, which has the V bit clear -- a deterministic
		 *  "no valid translation", a defined error path rather than a plausible-looking
		 *  valid answer that could steer the guest's paging.  Real probe semantics need
		 *  the translation walk and are FILED, not invented here.
		 */
		if (!d->reported_command) {
			d->reported_command = 1;
			fatal("[ m8820x: cpu%i cmmu%i: unimplemented command "
			    "0x%02x; ignored (reported once) ]\n",
			    d->cpu_nr, d->cmmu_nr, cmd);
		} else {
			debug("[ m8820x: cpu%i cmmu%i: unimplemented command "
			    "0x%02x; ignored ]\n", d->cpu_nr, d->cmmu_nr, cmd);
		}
		break;
	}
}


DEVICE_ACCESS(m8820x)
{
	// NOTE:
	//	cpu is the struct cpu* of the processor doing the device access.
	//	c   is the struct cpu* where the M88200 CMMU is located.
	uint64_t idata = 0, odata = 0;
	struct m8820x_data *d = (struct m8820x_data *) extra;
	struct cpu* c = cpu->machine->cpus[d->cpu_nr];
	uint32_t *regs = c->cd.m88k.cmmu[d->cmmu_nr]->reg;
	uint32_t *batc = c->cd.m88k.cmmu[d->cmmu_nr]->batc;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	if (writeflag == MEM_READ)
		odata = regs[relative_addr / sizeof(uint32_t)];

	switch (relative_addr / sizeof(uint32_t)) {

	case CMMU_IDR:
		if (writeflag == MEM_WRITE) {
			/*  #433: an ACCESS-SHAPE refusal, not a model gap -- IDR is a
			    read-only identification register.  What real silicon does with
			    the write is UNKNOWN (no 88200/88204 manual here), but exit(1)
			    is certainly wrong: terminating the HOST is not a behaviour the
			    emulated machine can have.  Ignoring it corrupts no model state,
			    and the seeded ID survives for the next read.  */
			m8820x_unimplemented(d, "write to CMMU_IDR");
		}
		break;

	case CMMU_SCR:
		if (writeflag == MEM_READ) {
			/*  #433: odata already holds regs[CMMU_SCR] from the read above,
			    i.e. the last command written -- so "reads back the last
			    command" is a defensible answer available for free.  Whether
			    real hardware makes SCR readable is UNKNOWN; returning the
			    stored word is inert to the emulator either way.  */
			m8820x_unimplemented(d, "read from CMMU_SCR");
		} else {
			regs[relative_addr / sizeof(uint32_t)] = idata;
			m8820x_command(c, d);
		}
		break;

	case CMMU_SSR:
		if (writeflag == MEM_WRITE) {
			/*  #433: SSR is the probe-status register, written by the MODEL
			    rather than by the guest, so ignoring a guest write corrupts
			    nothing the model maintains.  */
			m8820x_unimplemented(d, "write to CMMU_SSR");
		}
		break;

	case CMMU_PFSR:
	case CMMU_PFAR:
	case CMMU_SAR:
	case CMMU_SCTR:
	case CMMU_SAPR:		/*  TODO: Invalidate something for  */
	case CMMU_UAPR:		/*  SAPR and UAPR writes?  */
		/*  TODO: Don't invalidate everything.  */
		c->invalidate_translation_caches(c, 0, INVALIDATE_ALL);
		if (writeflag == MEM_WRITE)
			regs[relative_addr / sizeof(uint32_t)] = idata;
		break;

	case CMMU_BWP0:
	case CMMU_BWP1:
	case CMMU_BWP2:
	case CMMU_BWP3:
	case CMMU_BWP4:
	case CMMU_BWP5:
	case CMMU_BWP6:
	case CMMU_BWP7:
		if (writeflag == MEM_WRITE) {
			uint32_t old;
			int i = (relative_addr / sizeof(uint32_t)) - CMMU_BWP0;

			regs[relative_addr / sizeof(uint32_t)] = idata;

			/*  Also write to the specific batc registers:  */
			old = batc[i];
			batc[i] = idata;
			if (old != idata) {
				/*  TODO: Don't invalidate everything?  */
				c->invalidate_translation_caches(
				    c, 0, INVALIDATE_ALL);
			}
		}
		break;

	case CMMU_CSSP0:
		/*  TODO: Actually care about cache details.  */
		break;

	default:
		/*
		 *  #433: THE ARM THAT COVERS 1006 OF THE 1024 WORD OFFSETS.  It used to
		 *  exit(1), so an ordinary guest LOAD of an unmodelled register terminated the
		 *  host process -- measured at 1007 of 1024 offsets on a read.
		 *
		 *  The MMU objection to continuing does not apply here, and that is a measured
		 *  fact rather than a hope: every register the emulator's own translation
		 *  consults -- SAPR and UAPR read at memory_m88k.c:135,137, PFSR and PFAR
		 *  written at :382-405 -- is a HANDLED case label above.  Nothing reaching this
		 *  arm can alter what the emulator translates.  The defined-but-unhandled
		 *  registers are all cache diagnostics (CDP0-3, CTP0-3, and the 88204-only
		 *  CSSP1-3) against a model that has no cache -- and the neighbouring CSSP0 arm
		 *  ALREADY answers exactly this way, silently, on a path a real boot exercises
		 *  1024 times.  Continuing here is the same policy, said out loud once.
		 *
		 *  On a read the caller gets the regs[] value fetched above, which is zero for
		 *  anything never stored; a write is dropped rather than stored, because
		 *  RAM-like read-back could satisfy a guest's write-then-verify probe for a
		 *  register the model does not implement.
		 */
		if (writeflag == MEM_WRITE) {
			char w[64];
			snprintf(w, sizeof(w), "write to offset 0x%x: 0x%x",
			    (int) relative_addr, (int) idata);
			m8820x_unimplemented(d, w);
		} else {
			char r[64];
			snprintf(r, sizeof(r), "read from offset 0x%x",
			    (int) relative_addr);
			m8820x_unimplemented(d, r);
		}
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVINIT(m8820x)
{
	struct m8820x_data *d;

	CHECK_ALLOCATION(d = (struct m8820x_data *) malloc(sizeof(struct m8820x_data)));
	memset(d, 0, sizeof(struct m8820x_data));

	// Hack: Use the addr2 field to select cpu and cmmu numbers.
	// cmmu nr 0 = instruction, 1 = data.
	d->cmmu_nr = devinit->addr2 & 1;
	d->cpu_nr = devinit->addr2 >> 1;

	memory_device_register(devinit->machine->memory, devinit->name,
	    devinit->addr, M8820X_LENGTH, dev_m8820x_access, (void *)d,
	    DM_DEFAULT, NULL);

	return 1;
}

