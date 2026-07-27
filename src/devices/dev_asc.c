/*
 *  Copyright (C) 2003-2019  Anders Gavare.  All rights reserved.
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
 *  COMMENT: NCR53C9X "ASC" SCSI controller
 *
 *  This is the SCSI controller used in some DECstation/DECsystem models and
 *  the PICA-61 machine.
 *
 *  Supposed to support SCSI-1 and SCSI-2. I've not yet found any docs
 *  on NCR53C9X, so I'll try to implement this device from LSI53CF92A docs
 *  instead.
 *
 *
 *  Memory layout on DECstation:
 *
 *	NCR53C94 registers	at base + 0
 *	DMA address register	at base + 0x40000
 *	128K SRAM buffer	at base + 0x80000
 *	ROM			at base + 0xc0000
 *
 *  Memory layout on PICA-61:
 *
 *	I haven't had time to look this up yet, but length = 0x1000.
 *
 *
 *  TODO:  This module needs a clean-up, and some testing to see that
 *         it works will all OSes that might use it (NetBSD, OpenBSD,
 *         Ultrix, Linux, Mach, OSF/1, Sprite, ...)
 *
 *	   Running Linux/DECstation 2.4.26 with no scsi disks attached causes
 *	   a warning message to be printed by Linux. (Whether this is a bug,
 *	   is is the way it works on real hardware, I don't know.)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cpu.h"
#include "devices.h"
#include "diskimage.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"

#include "thirdparty/ncr53c9xreg.h"


/*  #define ASC_DEBUG  */
/*  #define debug fatal  */
/*  #define ASC_FULL_REGISTER_ACCESS_DEBUG  */
/*  static int quiet_mode = 0;  */

#define	ASC_TICK_SHIFT		15

extern int quiet_mode;


#define	ASC_FIFO_LEN		16
#define	STATE_DISCONNECTED	0
#define	STATE_INITIATOR		1
#define	STATE_TARGET		2

#define	PHASE_DATA_OUT		0
#define	PHASE_DATA_IN		1
#define	PHASE_COMMAND		2
#define	PHASE_STATUS		3
#define	PHASE_MSG_OUT		6
#define	PHASE_MSG_IN		7


/*  The controller's SCSI id:  */
#define	ASC_SCSI_ID		7

#define	ASC_DMA_SIZE		(128*1024)

struct asc_data {
	int		mode;

	void		*turbochannel;
	struct interrupt irq;
	int		irq_asserted;

	/*  Current state and transfer:  */
	int		cur_state;
	int		cur_phase;
	struct scsi_transfer *xferp;

	/*  FIFO:  */
	unsigned char	fifo[ASC_FIFO_LEN];
	int		fifo_in;
	int		fifo_out;
	int		n_bytes_in_fifo;		/*  cached  */

	/*  #269: one-shot latches for the two guest-reachable FIFO
	    diagnostics below. (The read-side message says "overrun" for
	    historical reasons; the condition is a read of an EMPTY FIFO.)
	    Deliberately NOT cleared by dev_asc_reset() or dev_asc_fifo_flush():
	    a guest could otherwise re-arm the flood with RSTCHIP. Zeroed by
	    the memset in dev_asc_init().  */
	int		fifo_underrun_warned;
	int		fifo_overrun_warned;

	/*  #277: one-shot latches for the two guest-repeatable transfer
	    diagnostics. SEPARATE fields on purpose: a single shared flag would
	    let whichever message fires first mask the other one for good.
	    Not cleared by dev_asc_reset(), same rule as #269.  */
	int		unknown_phase_warned;
	int		newxfer_warned;

	/*  ATN signal:  */
	int		atn;

	/*  Incoming dma data:  */
	unsigned char	*incoming_data;
	int		incoming_len;
	int		incoming_data_addr;

	/*  Built-in DMA memory (for DECstation 5000/200):  */
	uint32_t	dma_address_reg;
	unsigned char	*dma_address_reg_memory;
	unsigned char	*dma;

	void		*dma_controller_data;
	size_t		(*dma_controller)(void *dma_controller_data,
			    unsigned char *data, size_t len, int writeflag);

	/*  Read registers and write registers:  */
	uint32_t	reg_ro[0x10];
	uint32_t	reg_wo[0x10];
};

/*  (READ/WRITE name, if split)  */
const char *asc_reg_names[0x10] = {
	"NCR_TCL", "NCR_TCM", "NCR_FIFO", "NCR_CMD",
	"NCR_STAT/NCR_SELID", "NCR_INTR/NCR_TIMEOUT",
	"NCR_STEP/NCR_SYNCTP", "NCR_FFLAG/NCR_SYNCOFF",
	"NCR_CFG1", "NCR_CCF", "NCR_TEST", "NCR_CFG2",
	"NCR_CFG3", "reg_0xd", "NCR_TCH", "reg_0xf"
};


/*  This is referenced below.  */
static int dev_asc_select(struct cpu *cpu, struct asc_data *d, int from_id,
	int to_id, int dmaflag, int n_messagebytes);


DEVICE_TICK(asc)
{
	struct asc_data *d = (struct asc_data *) extra;
	int new_assert = d->reg_ro[NCR_STAT] & NCRSTAT_INT;

	if (new_assert && !d->irq_asserted)
		INTERRUPT_ASSERT(d->irq);

	d->irq_asserted = new_assert;
}


/*
 *  dev_asc_fifo_flush():
 *
 *  Flush the fifo.
 */
static void dev_asc_fifo_flush(struct asc_data *d)
{
	d->fifo[0] = 0x00;
	d->fifo_in = 0;
	d->fifo_out = 0;
	d->n_bytes_in_fifo = 0;
}


/*
 *  dev_asc_reset():
 *
 *  Reset the state of the asc.
 */
static void dev_asc_reset(struct asc_data *d)
{
	d->cur_state = STATE_DISCONNECTED;
	d->atn = 0;

	if (d->xferp != NULL)
		scsi_transfer_free(d->xferp);
	d->xferp = NULL;

	dev_asc_fifo_flush(d);

	/*  According to table 4.1 in the LSI53CF92A manual:  */
	memset(d->reg_wo, 0, sizeof(d->reg_wo));
	d->reg_wo[NCR_TCH] = 0x94;
	d->reg_wo[NCR_CCF] = 2;
	memcpy(d->reg_ro, d->reg_wo, sizeof(d->reg_ro));
	d->reg_wo[NCR_SYNCTP] = 5;

	/*  #266: a chip reset (RSTCHIP, the only caller) also releases the
	    interrupt output.  reg_ro incl. NCRSTAT_INT was cleared above, but
	    DEVICE_TICK(asc) only asserts on a rising edge and the sole other
	    deassert is the NCR_INTR read -- so without this a pending IRQ stays
	    latched (line high, STAT==0) until the guest happens to read INTR.
	    dev_asc_reset runs only at RSTCHIP, after INTERRUPT_CONNECT.  */
	INTERRUPT_DEASSERT(d->irq);
	d->irq_asserted = 0;
}


/*
 *  dev_asc_fifo_read():
 *
 *  Read a byte from the asc FIFO.
 */
static int dev_asc_fifo_read(struct asc_data *d)
{
	int res = d->fifo[d->fifo_out];

	if (d->n_bytes_in_fifo == 0) {	/*  #265: fifo_in==fifo_out is also true
	    when the FIFO is exactly full (16); test the cached count so a full
	    FIFO drains instead of being read as empty forever.  */
		/*  #197: (Codex/Fable) reading an empty FIFO must not drive
		    n_bytes_in_fifo negative -- a later non-DMA selection turns
		    the negative count into a huge size_t alloc -> exit(). Warn
		    and return without underflowing.  */
		/*  #269: warn once per device. A guest looping reads of
		    NCR_FIFO while empty otherwise emits one host line per read
		    (measured: 24 reads -> 24 lines). fatal() is deliberately
		    kept rather than debugmsg(): under -q the post-startup
		    verbosity settles at VERBOSITY_ERROR (main.c lowers it by
		    one, but debugmsg_add_verbosity_level() floors at 0), so a
		    WARNING-level debugmsg would be invisible to the boot-log
		    hygiene grep, and an ERROR-level one would change the
		    printed form and would trip #261's global break-on-ERROR
		    whenever that is armed.  */
		if (!d->fifo_underrun_warned) {
			d->fifo_underrun_warned = 1;
			fatal("dev_asc: WARNING! FIFO overrun!"
			    " (further occurrences suppressed)\n");
		}
		return res;
	}

	d->fifo_out = (d->fifo_out + 1) % ASC_FIFO_LEN;
	d->n_bytes_in_fifo --;

	return res;
}


/*
 *  dev_asc_fifo_write():
 *
 *  Write a byte to the asc FIFO.
 */
static void dev_asc_fifo_write(struct asc_data *d, unsigned char data)
{
	/*  #197: (Codex/Fable) don't push the FIFO occupancy past its
	    physical size; a bloated count later becomes a huge size_t alloc
	    -> exit() (mirror of the read underflow guard).  */
	if (d->n_bytes_in_fifo >= ASC_FIFO_LEN) {
		/*  #265: this is the real overflow -- the byte is dropped here.
		    The old post-write fifo_in==fifo_out check fired on the legal
		    16th byte instead and could never catch an actual 17th-byte
		    overrun.  */
		/*  #269: ...but it fires on EVERY dropped byte, i.e. one host
		    line per guest store (measured: 24 dropped -> 24 lines), and
		    fatal() is not verbosity-gated and writes stdout one
		    character at a time -- the same stream the boot harness
		    pattern-matches -- so an undrained pipe can block the
		    single-threaded emulator. Warn once per device.  */
		if (!d->fifo_overrun_warned) {
			d->fifo_overrun_warned = 1;
			fatal("dev_asc: WARNING! FIFO overrun on write!"
			    " (further occurrences suppressed)\n");
		}
		return;
	}
	d->fifo[d->fifo_in] = data;
	d->fifo_in = (d->fifo_in + 1) % ASC_FIFO_LEN;
	d->n_bytes_in_fifo ++;
}


/*
 *  dev_asc_newxfer():
 *
 *  Allocate memory for a new transfer.
 */
static void dev_asc_newxfer(struct asc_data *d)
{
	if (d->xferp != NULL) {
		/*  #277: this fires on two SELECTs without an intervening
		    MSGOK, which a guest can repeat forever (measured: one host
		    line per store). Warn once per device. fatal() rather than
		    the bare printf() that used to be here, so the message is
		    decorated like the rest of this file. The transfer itself
		    is still freed every time.  */
		if (!d->newxfer_warned) {
			d->newxfer_warned = 1;
			fatal("WARNING! dev_asc_newxfer(): freeing previous"
			    " transfer (further occurrences suppressed)\n");
		}
		scsi_transfer_free(d->xferp);
		d->xferp = NULL;
	}

	d->xferp = scsi_transfer_alloc();
#if 0
	d->xferp->get_data_out = dev_asc_get_data_out;
	d->xferp->gdo_extra = (void *) d;
#endif
}


/*
 *  dev_asc_transfer():
 *
 *  Transfer data from a SCSI device to the controller (or vice versa),
 *  depending on the current phase.
 *
 *  Returns 1 if ok, 0 on error.
 */
static int dev_asc_transfer(struct cpu *cpu, struct asc_data *d, int dmaflag)
{
	int res = 1, all_done = 1;
	int len, i, ch;

	/*  #167: (Codex/Fable) a transfer command issued
	    before any SELECT leaves d->xferp NULL (fresh state has cur_phase ==
	    PHASE_DATA_OUT); returning failure here lets the callers report a
	    disconnect (NCRINTR_DIS|NCRSTAT_INT) instead of dereferencing NULL
	    in the phase branches below.  */
	if (d->xferp == NULL) {
		fatal("[ asc: transfer command with no transfer in"
		    " progress (no SELECT)? ]\n");
		return 0;
	}

	if (!quiet_mode)
		debug(" { TRANSFER to/from id %i: ", d->reg_wo[NCR_SELID] & 7);

	if (d->cur_phase == PHASE_DATA_IN) {
		/*  Data coming into the controller from external device:  */
		if (!dmaflag) {
			if (d->xferp->data_in == NULL) {
				fatal("no incoming data?\n");
				res = 0;
			} else {
/*  TODO  */
fatal("TODO..............\n");
				len = d->reg_wo[NCR_TCL] +
				    d->reg_wo[NCR_TCM] * 256;

				len--;
				ch = (d->incoming_data == NULL) ? 0 :	/* #105: incoming_data is never allocated -> avoid NULL deref */
				    d->incoming_data[d->incoming_data_addr];
				debug(" %02x", ch);

				d->incoming_data_addr ++;
				dev_asc_fifo_write(d, ch);

				if (len == 0) {
					free(d->incoming_data);
					d->incoming_data = NULL;
				}

				d->reg_ro[NCR_TCL] = len & 255;
				d->reg_ro[NCR_TCM] = (len >> 8) & 255;
			}
		} else {
			/*  Copy from the incoming data into dma memory:  */
			if (d->xferp->data_in == NULL) {
				fatal("no incoming DMA data?\n");
				res = 0;
			} else {
				size_t lenIn = d->xferp->data_in_len;
				size_t lenIn2 = d->reg_wo[NCR_TCL] +
				    d->reg_wo[NCR_TCM] * 256;
				size_t programmed;
				size_t moved = 0;	/*  #286  */
				if (lenIn2 == 0)
					lenIn2 = 65536;

				/*  #281: the count the guest actually asked
				    for, snapshotted before the clamps below
				    rewrite lenIn2 into the count that moved.  */
				programmed = lenIn2;

                                if (lenIn < lenIn2) {
					/*  #282: lenIn/lenIn2 are size_t, so
					    passing them to %i was undefined on
					    LP64. Cast, as the neighbouring
					    warning below already does.  */
                                        fatal("{ asc: data in, lenIn=%i lenIn2=%i "
					    "}\n", (int)lenIn, (int)lenIn2);
                                }

				/*  TODO: check lenIn2 in a similar way?  */
				if (lenIn + (d->dma_address_reg &
				    (ASC_DMA_SIZE-1)) > ASC_DMA_SIZE)
					lenIn = ASC_DMA_SIZE -
					    (d->dma_address_reg &
					    (ASC_DMA_SIZE-1));

				if (lenIn2 > lenIn) {
					/*  #281: the memset that used to stand
					    here is gone. It zeroed exactly the
					    region the memcpy below overwrites,
					    and on arc it zeroed d->dma, which
					    is not the destination at all. With
					    an honest residual the driver stops
					    reading the tail, so zeroing it is
					    unnecessary rather than merely
					    redundant.  */
					lenIn2 = lenIn;
				}

#ifdef ASC_DEBUG
				if (!quiet_mode) {
					int i;
					for (i=0; i<lenIn; i++)
						debug(" %02x", d->xferp->
						    data_in[i]);
				}
#endif

				/*
				 *  Are we using an external DMA controller?
				 *  Then use it. Otherwise place the data in
				 *  the DECstation 5000/200 built-in DMA
				 *  region.
				 */
				/*  #286: capture what the controller actually
				    moved; the built-in DMA region always moves it
				    all.  */
				if (d->dma_controller != NULL)
					moved = d->dma_controller(
					    d->dma_controller_data,
					    d->xferp->data_in,
					    lenIn2, 1);
				else {
					memcpy(d->dma + (d->dma_address_reg &
					    (ASC_DMA_SIZE-1)),
					    d->xferp->data_in, lenIn2);
					moved = lenIn2;
				}

				/*
				 *  #286: the controller's return used to be
				 *  discarded, so the residual below came from the
				 *  count REQUESTED rather than the count that
				 *  MOVED: when programmed == lenIn2 it read as 0
				 *  with NCRSTAT_TC set, making a short DATA_IN
				 *  indistinguishable from a complete one while the
				 *  guest's buffer kept its stale tail. The arc
				 *  driver does read this counter (ASC_TC_GET, six
				 *  sites) even though it ignores the TC status bit.
				 *
				 *  moved is compared post-clamp, so a target that
				 *  merely offered less than was programmed is not
				 *  read as a controller failure; all three counts
				 *  are size_t with moved <= lenIn2 <= programmed,
				 *  so the subtraction cannot underflow. Placed
				 *  BEFORE the multitransfer block, which advances
				 *  data_in by lenIn2 and would discard the bytes
				 *  that never arrived. The TRANS/TRPAD caller
				 *  writes only INTR/STAT/STEP, so the counter set
				 *  here survives (#264/#283 contract).
				 *
				 *  Reports the fault; does not repair it. A real
				 *  53C94 would stall awaiting a DREQ, so the
				 *  disconnect is the same robustness approximation
				 *  as #283, not fidelity -- and the transfer is
				 *  abandoned rather than retried, because
				 *  NCRCMD_ENSEL below is an unimplemented no-op.
				 *  Ending the transfer normally instead was
				 *  measured at two injection points and panics the
				 *  guest. See the CHANGELOG round block.
				 */
				if (lenIn2 > 0 && moved < lenIn2) {
					size_t residual = programmed - moved;

					fatal("[ asc: short DATA_IN DMA, %i of %i"
					    " bytes moved ]\n", (int)moved,
					    (int)lenIn2);

					d->reg_ro[NCR_TCL] = residual & 255;
					d->reg_ro[NCR_TCM] = (residual >> 8) & 255;

					return 0;
				}

				if (d->xferp->data_in_len > lenIn2) {
					unsigned char *n;

if (d->dma_controller != NULL)
	printf("WARNING!!!!!!!!! BUG!!!! Unexpected stuff..."
	    "lenIn2=%i d->xferp->data_in_len=%i\n", (int)lenIn2,
	    (int)d->xferp->data_in_len);

					all_done = 0;
					/*  fatal("{ asc: multi-transfer"
					    " data_in, lenIn=%i lenIn2=%i }\n",
					    (int)lenIn, (int)lenIn2);  */

					d->xferp->data_in_len -= lenIn2;
					CHECK_ALLOCATION(n = (unsigned char *)
					    malloc(d->xferp->data_in_len));
					memcpy(n, d->xferp->data_in + lenIn2,
					    d->xferp->data_in_len);
					free(d->xferp->data_in);
					d->xferp->data_in = n;

					lenIn = lenIn2;
				}

				/*
				 *  #281: report the transfer honestly. What
				 *  moved is lenIn2; what the guest programmed
				 *  is `programmed`. The residual left in the
				 *  counter is the difference, and Terminal
				 *  Count is set ONLY when that difference is
				 *  zero -- this used to store 0 and set TC
				 *  unconditionally, so a short DATA_IN was
				 *  bit-for-bit indistinguishable from a
				 *  complete one and the guest was told the
				 *  full count had moved. Both bytes are
				 *  written: on a 1024-byte residual the low
				 *  byte is 0x00, so writing TCL alone would
				 *  still read as "complete". TCH is left
				 *  alone; the counter is 16-bit here. (A
				 *  count programmed as 0 means 65536, which
				 *  the 16-bit counter cannot represent -- it
				 *  reads back as 0 with TC clear, exactly as
				 *  the status bit exists to disambiguate.)
				 */
				lenIn = programmed - lenIn2;

				d->reg_ro[NCR_TCL] = lenIn & 255;
				d->reg_ro[NCR_TCM] = (lenIn >> 8) & 255;

				if (lenIn == 0) {
					/*  Successful DMA transfer:  */
					d->reg_ro[NCR_STAT] |= NCRSTAT_TC;
				}
			}
		}
	} else if (d->cur_phase == PHASE_DATA_OUT) {
		/*  Data going from the controller to an external device:  */
		if (!dmaflag) {
fatal("TODO.......asdgasin\n");
		} else {
			/*  Copy data from DMA to data_out:  */
			int len2 = d->reg_wo[NCR_TCL] +
			    d->reg_wo[NCR_TCM] * 256;
			int programmed;		/*  #283  */
			size_t moved = 0;	/*  #283  */
			len = d->xferp->data_out_len;

			if (len2 == 0)
				len2 = 65536;

			/*  #283: the count the guest actually asked for,
			    snapshotted before the clamps below rewrite len2
			    into the count this transfer may move.  */
			programmed = len2;

			if (len == 0) {
				/*  #264: a DATA_OUT transfer with a zero-length
				    data_out buffer (notably TRPAD, which allocates
				    a fresh empty transfer via dev_asc_newxfer) must
				    not exit() the host; fail the transfer so the
				    TRANS/TRPAD caller reports a disconnect
				    (NCRINTR_DIS|NCRSTAT_INT), matching the #167 guard
				    and the nonexistent-target selection path.  */
				fatal("[ asc: DATA_OUT transfer with "
				    "data_out_len == 0 ]\n");
				return 0;
			}

			/*  TODO: Make sure that len2 doesn't go outside
			    of the dma memory?  */

			/*  fatal("    data out offset=%5i len=%5i\n",
			    d->xferp->data_out_offset, len2);  */

			if (d->xferp->data_out_offset + len2 >
			    d->xferp->data_out_len) {
				len2 = d->xferp->data_out_len -
				    d->xferp->data_out_offset;
			}

				/*  Bound len2 to the source d->dma buffer (the DMA offset
				    is guest-controlled) to avoid an OOB read past ASC_DMA_SIZE.  */
				{
					size_t dma_off = d->dma_address_reg & (ASC_DMA_SIZE - 1);
					if (dma_off + (size_t)len2 > ASC_DMA_SIZE)
						len2 = ASC_DMA_SIZE - dma_off;
				}

			/*
			 *  Are we using an external DMA controller? Then use
			 *  it. Otherwise place the data in the DECstation
			 *  5000/200 built-in DMA region.
			 */
			if (d->xferp->data_out == NULL) {
				/*  #263: zero the buffer so a short or wrong-direction
				    DMA cannot disclose uninitialized host heap into the
				    guest disk image (scsi_transfer_allocbuf only clears
				    when clearflag != 0).  */
				scsi_transfer_allocbuf(&d->xferp->data_out_len,
				    &d->xferp->data_out, len, 1);

				/*  #283: capture what the controller moved.  */
				if (d->dma_controller != NULL)
					moved = d->dma_controller(
					    d->dma_controller_data,
					    d->xferp->data_out,
					    len2, 0);
				else {
					memcpy(d->xferp->data_out,
					    d->dma + (d->dma_address_reg &
					    (ASC_DMA_SIZE-1)), len2);
					moved = len2;
				}
				d->xferp->data_out_offset = moved;
			} else {
				/*  Continuing a multi-transfer:  */
				/*  #283: ditto -- fixing only the fresh path
				    above would leave this one able to commit
				    an underfilled final chunk.  */
				if (d->dma_controller != NULL)
					moved = d->dma_controller(
					    d->dma_controller_data,
					    d->xferp->data_out +
						d->xferp->data_out_offset,
					    len2, 0);
				else {
					memcpy(d->xferp->data_out +
					    d->xferp->data_out_offset,
					    d->dma + (d->dma_address_reg &
					    (ASC_DMA_SIZE-1)), len2);
					moved = len2;
				}
				d->xferp->data_out_offset += moved;
			}

			/*
			 *  #283: the controller's return used to be discarded
			 *  while data_out_offset was advanced by the REQUESTED
			 *  len2, so a short transfer still passed the disk
			 *  layer's "is the buffer full yet" gate and committed
			 *  bytes the guest never supplied to the disk image --
			 *  silently, since a short and a complete transfer
			 *  reported identical STAT/TCL/TCM/STEP/INTR. The
			 *  fatal() below is the only witness this has.
			 *
			 *  ANY short fails the transfer, not just a zero one:
			 *  fault injection on OpenBSD 2.2/arc panics the guest
			 *  on a positive partial that is allowed to continue,
			 *  and survives when it is aborted here. #267's
			 *  translation-limit break and #268's count mask are
			 *  themselves sources of a short callback, and this
			 *  covers them; dev_jazz.c zeroes dma0_count on such a
			 *  break, so the R4030 cannot resume mid-transfer, but
			 *  the disconnect makes the guest re-arm anyway.
			 *
			 *  len2 is the count AFTER the clamps above: comparing
			 *  against the programmed one would fire on a benign
			 *  re-entry where the disk wants less than was offered.
			 *  len2 > 0 keeps a clamped-to-nothing (or negative)
			 *  count from being read as a failure.
			 *
			 *  A real 53C94 does NOT synthesize a disconnect here;
			 *  it stalls waiting for a DREQ that never comes, and
			 *  the measurement shows stalling panics the guest.
			 *  This is therefore a deliberate ROBUSTNESS
			 *  APPROXIMATION and not hardware fidelity: an
			 *  instantaneous emulator cannot express an indefinite
			 *  bus stall, and DIS is the nearest guest-handleable
			 *  terminal state. The faithful path is the R4030
			 *  DMA_INT_SRC fault interrupt, a known gap since #267.
			 */
			if (len2 > 0 && moved < (size_t)len2) {
				int residual = programmed - (int)moved;

				fatal("[ asc: short DATA_OUT DMA, %i of %i "
				    "bytes moved, offset %i ]\n", (int)moved,
				    (int)len2, (int)d->xferp->data_out_offset);

				/*  The honest residual, both bytes (#281):
				    reg_ro[] is uint32_t and the DEC read path
				    returns the whole word. NCRSTAT_TC is left
				    CLEAR -- nothing here reached terminal
				    count.  */
				d->reg_ro[NCR_TCL] = residual & 255;
				d->reg_ro[NCR_TCM] = (residual >> 8) & 255;

				/*  Fail BEFORE diskimage_scsicommand() below.
				    The NCRCMD_TRANS caller turns this into
				    STATE_DISCONNECTED + NCRINTR_DIS |
				    NCRSTAT_INT and frees the transfer; it
				    writes only INTR/STAT/STEP, so the counter
				    written above survives. #264 already
				    returns 0 under the same contract.  */
				return 0;
			}

			/*  If the disk wants more than we're DMAing,
			    then this is a multitransfer:  */
			if (d->xferp->data_out_offset !=
			    d->xferp->data_out_len) {
				if (!quiet_mode)
					debug("[ asc: data_out, multitransfer "
					    "len = %i, len2 = %i ]\n",
					    (int)len, (int)len2);
				if (d->xferp->data_out_offset >
				    d->xferp->data_out_len)
					fatal("[ asc data_out dma: too much?"
					    " ]\n");
				else
					all_done = 0;
			}

#ifdef ASC_DEBUG
			if (!quiet_mode) {
				int i;
				for (i=0; i<len; i++)
					debug(" %02x", d->xferp->data_out[i]);
			}
#endif
			len = 0;

			d->reg_ro[NCR_TCL] = len & 255;
			d->reg_ro[NCR_TCM] = (len >> 8) & 255;

			/*  Successful DMA transfer:  */
			d->reg_ro[NCR_STAT] |= NCRSTAT_TC;
		}
	} else if (d->cur_phase == PHASE_MSG_OUT) {
		if (!quiet_mode)
			debug("MSG OUT: ");
		/*  Data going from the controller to an external device:  */
		if (!dmaflag) {
			/*  There should already be one byte in msg_out, so we
			    just extend the message:  */
			int oldlen = d->xferp->msg_out_len;
			int newlen;

			if (oldlen != 1) {
				fatal(" (PHASE OUT MSG len == %i, "
				    "should be 1)\n", oldlen);
			}

			newlen = oldlen + d->n_bytes_in_fifo;
			CHECK_ALLOCATION(d->xferp->msg_out = (unsigned char *)
			    realloc(d->xferp->msg_out, newlen));
			d->xferp->msg_out_len = newlen;

			i = oldlen;
			while (d->n_bytes_in_fifo > 0) {	/*  #265: see fifo_read;
			    a full(16) FIFO has fifo_in==fifo_out and would copy 0 of
			    the bytes just realloc'd into msg_out.  */
				ch = dev_asc_fifo_read(d);
				d->xferp->msg_out[i++] = ch;
#ifdef ASC_DEBUG
				debug("0x%02x ", ch);
#endif
			}

#ifdef MACH
			/*  Super-ugly hack for Mach/PMAX:  TODO: make nicer  */
			if (d->xferp->msg_out_len == 6 &&
			    (d->xferp->msg_out[0] == 0x80 ||
			     d->xferp->msg_out[0] == 0xc0) &&
			    d->xferp->msg_out[1] == 0x01 &&
			    d->xferp->msg_out[2] == 0x03 &&
			    d->xferp->msg_out[3] == 0x01 &&
			    d->xferp->msg_out[4] == 0x32 &&
			    d->xferp->msg_out[5] == 0x0f) {
				fatal(" !! Mach/PMAX hack !! ");
				all_done = 0;
				d->cur_phase = PHASE_MSG_IN;
			}
#endif
		} else {
			/*  Copy data from DMA to msg_out:  */
			fatal("[ DMA MSG OUT: xxx TODO! ]");
			/*  TODO  */
			res = 0;
		}
	} else if (d->cur_phase == PHASE_MSG_IN) {
		if (!quiet_mode)
			debug(" MSG IN");
		fatal("[ MACH HACK! ]");
		/*  Super-ugly hack for Mach/PMAX:  TODO: make nicer  */
		dev_asc_fifo_write(d, 0x07);
		d->cur_phase = PHASE_COMMAND;
		all_done = 0;
	} else if (d->cur_phase == PHASE_COMMAND) {
		if (!quiet_mode)
			debug(" COMMAND ==> select ");
		res = dev_asc_select(cpu, d, d->reg_ro[NCR_CFG1] & 7,
		    d->reg_wo[NCR_SELID] & 7, dmaflag, 0);
		return res;
	} else {
		/*  #277: the transfer tail leaves cur_phase == PHASE_STATUS,
		    which no branch above handles, so a guest that keeps issuing
		    transfer commands lands here once per store (measured
		    together with the newxfer warning above at 2.00 host lines
		    per store). Warn once per device.
		    LATCHED RATHER THAN VERBOSITY-GATED, unlike the stray-access
		    messages of #276 in this same file: this arm sets no
		    interrupt, so the transfer simply hangs and the guest is
		    never told through any other channel. A DEBUG gate would
		    leave a wedged guest completely silent under -q -- the mode
		    the boot harness runs in -- whereas a latch keeps exactly
		    one line in the log it greps.  */
		if (!d->unknown_phase_warned) {
			d->unknown_phase_warned = 1;
			fatal("!!! TODO: unknown/unimplemented phase "
			    "in transfer: %i (further occurrences "
			    "suppressed)\n", d->cur_phase);
		}
	}

	/*  Redo the command if data was just sent using DATA_OUT:  */
	if (d->cur_phase == PHASE_DATA_OUT) {
		res = diskimage_scsicommand(cpu, d->reg_wo[NCR_SELID] & 7,
		    DISKIMAGE_SCSI, d->xferp);
	}

	if (all_done) {
		if (d->cur_phase == PHASE_MSG_OUT)
			d->cur_phase = PHASE_COMMAND;
		else
			d->cur_phase = PHASE_STATUS;
	}

	/*
	 *  Cause an interrupt after the transfer:
	 *
	 *  NOTE:  Earlier I had this in here as well:
	 *	d->reg_ro[NCR_INTR] |= NCRINTR_FC;
	 *  but Linux/DECstation and OpenBSD/pmax seems to choke on that.
	 */
	d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
	d->reg_ro[NCR_INTR] |= NCRINTR_BS;
	d->reg_ro[NCR_STAT] = (d->reg_ro[NCR_STAT] & ~7) | d->cur_phase;
	d->reg_ro[NCR_STEP] = (d->reg_ro[NCR_STEP] & ~7) | 4;	/*  4?  */

	if (!quiet_mode)
		debug("}");
	return res;
}


/*
 *  dev_asc_select():
 *
 *  Select a SCSI device, send msg bytes (if any), and send command bytes.
 *  (Call diskimage_scsicommand() to handle the command.)
 *
 *  Return value: 1 if ok, 0 on error.
 */
static int dev_asc_select(struct cpu *cpu, struct asc_data *d, int from_id,
	int to_id, int dmaflag, int n_messagebytes)
{
	int ok, len, i, ch;

	if (!quiet_mode)
		debug(" { SELECT id %i: ", to_id);

	/*
	 *  Message bytes, if any:
	 */
	if (!quiet_mode)
		debug("msg:");

	if (n_messagebytes > 0) {
		scsi_transfer_allocbuf(&d->xferp->msg_out_len,
		    &d->xferp->msg_out, n_messagebytes, 0);

		i = 0;
		while (n_messagebytes-- > 0) {
			int ch2 = dev_asc_fifo_read(d);
			if (!quiet_mode)
				debug(" %02x", ch2);
			d->xferp->msg_out[i++] = ch2;
		}

		if ((d->xferp->msg_out[0] & 0x7) != 0x00) {
			debug(" (LUNs not implemented yet: 0x%02x) }",
			    d->xferp->msg_out[0]);
			return 0;
		}

		if (((d->xferp->msg_out[0] & ~0x7) != 0xc0) &&
		    ((d->xferp->msg_out[0] & ~0x7) != 0x80)) {
			fatal(" (Unimplemented msg out: 0x%02x) }",
			    d->xferp->msg_out[0]);
			return 0;
		}

		if (d->xferp->msg_out_len > 1) {
			fatal(" (Long msg out, not implemented yet;"
			    " len=%i) }", d->xferp->msg_out_len);
			return 0;
		}
	} else {
		if (!quiet_mode)
			debug(" none");
	}

	/*  Special case: SELATNS (with STOP sequence):  */
	if (d->cur_phase == PHASE_MSG_OUT) {
		if (!quiet_mode)
			debug(" MSG OUT DEBUG");
		if (d->xferp->msg_out_len != 1) {
			fatal(" (SELATNS: msg out len == %i, should be 1)",
			    d->xferp->msg_out_len);
			return 0;
		}

/* d->cur_phase = PHASE_COMMAND; */

		/*  According to the LSI manual:  */
		d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
		d->reg_ro[NCR_INTR] |= NCRINTR_FC;
		d->reg_ro[NCR_INTR] |= NCRINTR_BS;
		d->reg_ro[NCR_STAT] = (d->reg_ro[NCR_STAT] & ~7) | d->cur_phase;
		d->reg_ro[NCR_STEP] = (d->reg_ro[NCR_STEP] & ~7) | 1;

		if (!quiet_mode)
			debug("}");
		return 1;
	}

	/*
	 *  Command bytes:
	 */
	if (!quiet_mode)
		debug(", cmd: ");

	if (!dmaflag) {
		if (!quiet_mode)
			debug("[non-DMA] ");

		scsi_transfer_allocbuf(&d->xferp->cmd_len,
		    &d->xferp->cmd, d->n_bytes_in_fifo, 0);

		i = 0;
		while (d->n_bytes_in_fifo > 0) {	/*  #265: a full(16) FIFO has
		    fifo_in==fifo_out and would copy 0 of the 16 bytes just
		    allocated (clearflag=0) as the CDB.  */
			ch = dev_asc_fifo_read(d);
			d->xferp->cmd[i++] = ch;
			if (!quiet_mode)
				debug("%02x ", ch);
		}
	} else {
		if (!quiet_mode)
			debug("[DMA] ");
		len = d->reg_wo[NCR_TCL] + d->reg_wo[NCR_TCM] * 256;
		if (len == 0)
			len = 65536;

		scsi_transfer_allocbuf(&d->xferp->cmd_len,
		    &d->xferp->cmd, len, 0);

		for (i=0; i<len; i++) {
			int ofs = d->dma_address_reg + i;
			ch = d->dma[ofs & (ASC_DMA_SIZE-1)];
			d->xferp->cmd[i] = ch;
			if (!quiet_mode)
				debug("%02x ", ch);
		}

		/*
		 *  #284: the loop above is infallible and exits at i == len,
		 *  so every one of the `len` bytes has been copied and the
		 *  honest residual is ZERO. The counter used to be loaded
		 *  with the FULL count while Terminal Count was asserted --
		 *  "nothing moved" and "the transfer completed" reported at
		 *  the same time, which no real 53C94 can do. TC stays set.
		 *
		 *  This is a conformance fix, not a guest-visible one: the
		 *  next DMA command reloads the counter from the write-only
		 *  registers, so the stale value was overwritten before any
		 *  data phase could read it. It is not a latent path either,
		 *  though -- OpenBSD/pmax issues SEL_ATN|DMA for every SCSI
		 *  command and reaches this 1659 times per boot. (arc preloads
		 *  the CDB into the FIFO and never gets here.)
		 */
		d->reg_ro[NCR_TCL] = 0;
		d->reg_ro[NCR_TCM] = 0;

		d->reg_ro[NCR_STAT] |= NCRSTAT_TC;
	}

	/*
	 *  Call the SCSI device to perform the command:
	 */
	ok = diskimage_scsicommand(cpu, to_id, DISKIMAGE_SCSI, d->xferp);


	/*  Cause an interrupt:  */
	d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
	d->reg_ro[NCR_INTR] |= NCRINTR_FC;
	d->reg_ro[NCR_INTR] |= NCRINTR_BS;

	if (ok == 2)
		d->cur_phase = PHASE_DATA_OUT;
	else if (d->xferp->data_in != NULL)
		d->cur_phase = PHASE_DATA_IN;
	else
		d->cur_phase = PHASE_STATUS;

	d->reg_ro[NCR_STAT] = (d->reg_ro[NCR_STAT] & ~7) | d->cur_phase;
	d->reg_ro[NCR_STEP] = (d->reg_ro[NCR_STEP] & ~7) | 4;	/*  DONE (?)  */

	if (!quiet_mode)
		debug("}");

	return ok;
}


DEVICE_ACCESS(asc_address_reg)
{
	struct asc_data *d = (struct asc_data *) extra;

	if (relative_addr + len > 4)
		return 0;

	if (writeflag==MEM_READ) {
		memcpy(data, d->dma_address_reg_memory + relative_addr, len);
	} else {
		memcpy(d->dma_address_reg_memory + relative_addr, data, len);
	}

	return 1;
}


DEVICE_ACCESS(asc_dma)
{
	struct asc_data *d = (struct asc_data *) extra;

	if (writeflag==MEM_READ) {
		memcpy(data, d->dma + relative_addr, len);
#ifdef ASC_DEBUG
		{
			int i;
			debug("[ asc: read from DMA addr 0x%05x:",
			    (int) relative_addr);
			for (i=0; i<len; i++)
				debug(" %02x", data[i]);
			debug(" ]\n");
		}
#endif

		/*  Don't return the common way, as that
		    would overwrite data.  */
		return 1;
	} else {
		memcpy(d->dma + relative_addr, data, len);
#ifdef ASC_DEBUG
		{
			int i;
			debug("[ asc: write to  DMA addr 0x%05x:",
			    (int) relative_addr);
			for (i=0; i<len; i++)
				debug(" %02x", data[i]);
			debug(" ]\n");
		}
#endif
		/*  Quick return.  */
		return 1;
	}
}


DEVICE_ACCESS(asc)
{
	int regnr;
	struct asc_data *d = (struct asc_data *) extra;
	int target_exists;
	int n_messagebytes = 0;
	uint64_t idata = 0, odata = 0;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

#if 0
	/*  Debug stuff useful when trying to make dev_asc compatible
	    with the 'arc' emulation mode, which is different from
	    the DECstation mode.  */
	fatal("[ asc: writeflag=%i addr=%08x idata=%016llx ]\n",
	    writeflag, (int)relative_addr, (long long)idata);
#endif

	switch (d->mode) {
	case DEV_ASC_DEC:
		regnr = relative_addr / 4;
		break;
	case DEV_ASC_PICA:
	default:
		regnr = relative_addr;
	}

	/*  Controller's ID is fixed:  */
	d->reg_ro[NCR_CFG1] = (d->reg_ro[NCR_CFG1] & ~7) | ASC_SCSI_ID;

	d->reg_ro[NCR_FFLAG] = ((d->reg_ro[NCR_STEP] & 0x7) << 5)
	    + d->n_bytes_in_fifo;

	d->dma_address_reg =
	    d->dma_address_reg_memory[0] +
	    (d->dma_address_reg_memory[1] << 8) +
	    (d->dma_address_reg_memory[2] << 16) +
	    (d->dma_address_reg_memory[3] << 24);

	if (regnr < 0x10) {
		if (regnr == NCR_FIFO) {
			if (writeflag == MEM_WRITE)
				dev_asc_fifo_write(d, idata);
			else
				odata = dev_asc_fifo_read(d);
		} else {
			if (writeflag==MEM_WRITE)
				d->reg_wo[regnr] = idata;
			else
				odata = d->reg_ro[regnr];
		}

#ifdef ASC_FULL_REGISTER_ACCESS_DEBUG
		if (!quiet_mode) {
			if (writeflag==MEM_READ) {
				debug("[ asc: read from %s: 0x%02x",
				    asc_reg_names[regnr], (int)odata);
			} else {
				debug("[ asc: write to  %s: 0x%02x",
				    asc_reg_names[regnr], (int)idata);
			}
		}
#endif
	} else if (relative_addr >= 0x300 && relative_addr < 0x600
	    && d->turbochannel != NULL) {
		debug("[ asc: offset 0x%x, redirecting to turbochannel"
		    " access ]\n", relative_addr);
		return dev_turbochannel_access(cpu, mem,
		    relative_addr, data, len, writeflag,
		    d->turbochannel);
	} else {
		/*  #276: every access to an offset this device does not model
		    lands here (on arc/PICA that is all of 0x10..0xfff), and an
		    ungated fatal() emitted one host line per guest access
		    (measured: 1.00 lines/access). This is ordinary probing
		    traffic for registers we do not implement, not a deficiency
		    tripwire -- and unlike the latched sites in #277 the guest
		    does get an answer (a read returns odata, a write is
		    dropped), so nothing hangs waiting for a message that isn't
		    printed. Gate it at DEBUG level: silent in a normal run,
		    shown at -v -v or with `break device`.  (relative_addr is a
		    uint64_t, so cast it for %x as the disabled debug block at
		    the top of this function already does.)  */
		if (writeflag==MEM_READ) {
			debugmsg(SUBSYS_DEVICE, "asc", VERBOSITY_DEBUG,
			    "read from 0x%04x: 0x%02x",
			    (int)relative_addr, (int)odata);
		} else {
			debugmsg(SUBSYS_DEVICE, "asc", VERBOSITY_DEBUG,
			    "write to  0x%04x: 0x%02x",
			    (int)relative_addr, (int)idata);
		}
	}

	/*
	 *  Some registers are read/write. Copy contents of
	 *  reg_wo to reg_ro:
	 */
#if 0
	d->reg_ro[ 0] = d->reg_wo[0];	/*  Transfer count lo and  */
	d->reg_ro[ 1] = d->reg_wo[1];	/*  middle  */
#endif
	d->reg_ro[ 2] = d->reg_wo[2];
	d->reg_ro[ 3] = d->reg_wo[3];
	d->reg_ro[ 8] = d->reg_wo[8];
	d->reg_ro[ 9] = d->reg_wo[9];
	d->reg_ro[10] = d->reg_wo[10];
	d->reg_ro[11] = d->reg_wo[11];
	d->reg_ro[12] = d->reg_wo[12];

	if (regnr == NCR_CMD && writeflag == MEM_WRITE) {
		if (!quiet_mode)
			debug(" ");

		/*  TODO:  Perhaps turn off others here too?  */
		d->reg_ro[NCR_INTR] &= ~NCRINTR_SBR;

		if (idata & NCRCMD_DMA) {
			if (!quiet_mode)
				debug("[DMA] ");

			/*
			 *  DMA commands load the transfer count from the
			 *  write-only registers to the read-only ones, and
			 *  the Terminal Count bit is cleared.
			 */
			d->reg_ro[NCR_TCL] = d->reg_wo[NCR_TCL];
			d->reg_ro[NCR_TCM] = d->reg_wo[NCR_TCM];
			d->reg_ro[NCR_TCH] = d->reg_wo[NCR_TCH];
			d->reg_ro[NCR_STAT] &= ~NCRSTAT_TC;
		}

		switch (idata & ~NCRCMD_DMA) {

		case NCRCMD_NOP:
			if (!quiet_mode)
				debug("NOP");
			break;

		case NCRCMD_FLUSH:
			if (!quiet_mode)
				debug("FLUSH");
			/*  Flush the FIFO:  */
			dev_asc_fifo_flush(d);
			break;

		case NCRCMD_RSTCHIP:
			if (!quiet_mode)
				debug("RSTCHIP");
			/*  Hardware reset.  */
			dev_asc_reset(d);
			break;

		case NCRCMD_RSTSCSI:
			if (!quiet_mode)
				debug("RSTSCSI");
			/*  No interrupt if interrupts are disabled.  */
			if (!(d->reg_wo[NCR_CFG1] & NCRCFG1_SRR))
				d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
			d->reg_ro[NCR_INTR] |= NCRINTR_SBR;
			d->reg_ro[NCR_INTR] |= NCRINTR_FC;
			d->cur_state = STATE_DISCONNECTED;
			break;

		case NCRCMD_ENSEL:
			if (!quiet_mode)
				debug("ENSEL");
			/*  TODO  */
			break;

		case NCRCMD_ICCS:
			if (!quiet_mode)
				debug("ICCS");
			/*  Reveice a status byte + a message byte.  */

			/*  TODO: how about other status and message bytes?  */
			if (d->xferp != NULL && d->xferp->status != NULL)
				dev_asc_fifo_write(d, d->xferp->status[0]);
			else
				dev_asc_fifo_write(d, 0x00);

			if (d->xferp != NULL && d->xferp->msg_in != NULL)
				dev_asc_fifo_write(d, d->xferp->msg_in[0]);
			else
				dev_asc_fifo_write(d, 0x00);

			d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
			d->reg_ro[NCR_INTR] |= NCRINTR_FC;
/*			d->reg_ro[NCR_INTR] |= NCRINTR_BS; */
			d->reg_ro[NCR_STAT] = (d->reg_ro[NCR_STAT] & ~7) | 7;
				/*  ? probably 7  */
			d->reg_ro[NCR_STEP] = (d->reg_ro[NCR_STEP] & ~7) | 4;
				/*  ?  */
			break;

		case NCRCMD_MSGOK:
			/*  Message is being Rejected if ATN is set,
			    otherwise Accepted.  */
			if (!quiet_mode) {
				debug("MSGOK");
				if (d->atn)
					debug("; Rejecting message");
				else
					debug("; Accepting message");
			}
			d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
			d->reg_ro[NCR_INTR] |= NCRINTR_DIS;

			d->reg_ro[NCR_STAT] = (d->reg_ro[NCR_STAT] & ~7) |
			    d->cur_phase;	/*  6?  */
			d->reg_ro[NCR_STEP] = (d->reg_ro[NCR_STEP] & ~7) |
			    4;	/*  ?  */

			d->cur_state = STATE_DISCONNECTED;

			if (d->xferp != NULL)
				scsi_transfer_free(d->xferp);
			d->xferp = NULL;
			break;

		case NCRCMD_SETATN:
			if (!quiet_mode)
				debug("SETATN");
			d->atn = 1;
			break;

		case NCRCMD_RSTATN:
			if (!quiet_mode)
				debug("RSTATN");
			d->atn = 0;
			break;

		case NCRCMD_SELNATN:
		case NCRCMD_SELATN:
		case NCRCMD_SELATNS:
		case NCRCMD_SELATN3:
			d->cur_phase = PHASE_COMMAND;
			switch (idata & ~NCRCMD_DMA) {
			case NCRCMD_SELATN:
			case NCRCMD_SELATNS:
				if ((idata & ~NCRCMD_DMA) == NCRCMD_SELATNS) {
					if (!quiet_mode)
						debug("SELATNS: select with "
						    "atn and stop, id %i",
						    d->reg_wo[NCR_SELID] & 7);
					d->cur_phase = PHASE_MSG_OUT;
				} else {
					if (!quiet_mode)
						debug("SELATN: select with atn"
						    ", id %i",
						    d->reg_wo[NCR_SELID] & 7);
				}
				n_messagebytes = 1;
				break;
			case NCRCMD_SELATN3:
				if (!quiet_mode)
					debug("SELNATN: select with atn3, "
					    "id %i", d->reg_wo[NCR_SELID] & 7);
				n_messagebytes = 3;
				break;
			case NCRCMD_SELNATN:
				if (!quiet_mode)
					debug("SELNATN: select without atn, "
					    "id %i", d->reg_wo[NCR_SELID] & 7);
				n_messagebytes = 0;
			}

			/*  TODO: not just disk, but some generic
			    SCSI device  */
			target_exists = diskimage_exist(cpu->machine,
			    d->reg_wo[NCR_SELID] & 7, DISKIMAGE_SCSI);

			if (target_exists) {
				/*
				 *  Select a SCSI device, send message bytes
				 *  (if any) and command bytes to the target.
				 */
				int ok;

				dev_asc_newxfer(d);

				ok = dev_asc_select(cpu, d,
				    d->reg_ro[NCR_CFG1] & 7,
				    d->reg_wo[NCR_SELID] & 7,
				    idata & NCRCMD_DMA? 1 : 0,
				    n_messagebytes);

				if (ok)
					d->cur_state = STATE_INITIATOR;
				else {
					d->cur_state = STATE_DISCONNECTED;
					d->reg_ro[NCR_INTR] |= NCRINTR_DIS;
					d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
					d->reg_ro[NCR_STEP] =
					    (d->reg_ro[NCR_STEP] & ~7) | 0;
					if (d->xferp != NULL)
						scsi_transfer_free(d->xferp);
					d->xferp = NULL;
				}
			} else {
				/*
				 *  Selection failed, non-existant scsi ID:
				 *
				 *  This is good enough to fool Ultrix, NetBSD,
				 *  OpenBSD and Linux to continue detection of
				 *  other IDs, without giving any warnings.
				 */
				d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
				d->reg_ro[NCR_INTR] |= NCRINTR_DIS;
				d->reg_ro[NCR_STEP] &= ~7;
				d->reg_ro[NCR_STEP] |= 0;
				dev_asc_fifo_flush(d);
				d->cur_state = STATE_DISCONNECTED;
			}
			break;

		case NCRCMD_TRPAD:
			if (!quiet_mode)
				debug("TRPAD");

			dev_asc_newxfer(d);
			{
				int ok;

				ok = dev_asc_transfer(cpu, d,
				    idata & NCRCMD_DMA? 1 : 0);
				if (!ok) {
					d->cur_state = STATE_DISCONNECTED;
					d->reg_ro[NCR_INTR] |= NCRINTR_DIS;
					d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
					d->reg_ro[NCR_STEP] = (d->reg_ro[
					    NCR_STEP] & ~7) | 0;
					if (d->xferp != NULL)
						scsi_transfer_free(d->xferp);
					d->xferp = NULL;
				}
			}
break;

/*  Old code which didn't work with Mach:  */
#if 0
			d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
			d->reg_ro[NCR_INTR] |= NCRINTR_BS;
			d->reg_ro[NCR_INTR] |= NCRINTR_FC;
			d->reg_ro[NCR_STAT] |= NCRSTAT_TC;

			d->reg_ro[NCR_TCL] = 0;
			d->reg_ro[NCR_TCM] = 0;

			d->reg_ro[NCR_STEP] &= ~7;
#if 0
			d->reg_ro[NCR_STEP] |= 0;
			dev_asc_fifo_flush(d);
#else
			d->reg_ro[NCR_STEP] |= 4;
#endif
			break;
#endif

		case NCRCMD_TRANS:
			if (!quiet_mode)
				debug("TRANS");

			{
				int ok;

				ok = dev_asc_transfer(cpu, d,
				    idata & NCRCMD_DMA? 1 : 0);
				if (!ok) {
					d->cur_state = STATE_DISCONNECTED;
					d->reg_ro[NCR_INTR] |= NCRINTR_DIS;
					d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
					d->reg_ro[NCR_STEP] = (d->reg_ro[
					    NCR_STEP] & ~7) | 0;
					if (d->xferp != NULL)
						scsi_transfer_free(d->xferp);
					d->xferp = NULL;
				}
			}
			break;

		default:
			/*  #240: An unimplemented/illegal ASC command must not
			    halt the host. The illegal-command interrupt has
			    been asserted (NCRSTAT_INT | NCRINTR_ILL) and
			    dev_asc_tick() delivers it to the guest, exactly as
			    real hardware reports an illegal command.  */
			/*  #245: route the guest-spammable diagnostic through the
			    verbosity-gated SUBSYS_DEVICE channel (suppressed by
			    default, shown at -v or `break device`) so a guest
			    hammering NCR_CMD can't flood the host log.  */
			debugmsg_cpu(cpu, SUBSYS_DEVICE, "asc", VERBOSITY_DEBUG,
			    "unimplemented command 0x%02x", (int)idata);
			d->reg_ro[NCR_STAT] |= NCRSTAT_INT;
			d->reg_ro[NCR_INTR] |= NCRINTR_ILL;
		}
	}

	if (regnr == NCR_INTR && writeflag == MEM_READ) {
		/*
		 *  Reading the interrupt register de-asserts the
		 *  interrupt pin.  Also, INTR, STEP, and STAT are all
		 *  cleared, according to page 64 of the LSI53CF92A manual,
		 *  if "interrupt output is true".
		 */
		if (d->reg_ro[NCR_STAT] & NCRSTAT_INT) {
			d->reg_ro[NCR_INTR] = 0;
			d->reg_ro[NCR_STEP] = 0;
			d->reg_ro[NCR_STAT] = 0;

			/*  For Mach/PMAX? TODO  */
			d->reg_ro[NCR_STAT] = PHASE_COMMAND;
		}

		INTERRUPT_DEASSERT(d->irq);
		d->irq_asserted = 0;
	}

	if (regnr == NCR_CFG1) {
		/*  TODO: other bits  */
		if (!quiet_mode) {
			debug(" parity %s,", d->reg_ro[regnr] &
			    NCRCFG1_PARENB? "enabled" : "disabled");
			debug(" scsi_id %i", d->reg_ro[regnr] & 0x7);
		}
	}

#ifdef ASC_FULL_REGISTER_ACCESS_DEBUG
	debug(" ]\n");
#endif
	dev_asc_tick(cpu, extra);

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


/*
 *  dev_asc_init():
 *
 *  Register an 'asc' device.
 */
void dev_asc_init(struct machine *machine, struct memory *mem,
	uint64_t baseaddr, const char *irq_path, void *turbochannel, int mode,
	size_t (*dma_controller)(void *dma_controller_data,
		unsigned char *data, size_t len, int writeflag),
	void *dma_controller_data)
{
	struct asc_data *d;

	CHECK_ALLOCATION(d = (struct asc_data *) malloc(sizeof(struct asc_data)));
	memset(d, 0, sizeof(struct asc_data));

	INTERRUPT_CONNECT(irq_path, d->irq);
	d->turbochannel = turbochannel;
	d->mode         = mode;

	d->reg_ro[NCR_CFG3] = NCRF9XCFG3_CDB;

	CHECK_ALLOCATION(d->dma_address_reg_memory = (unsigned char *)
	    malloc(machine->arch_pagesize));
	memset(d->dma_address_reg_memory, 0, machine->arch_pagesize);

	CHECK_ALLOCATION(d->dma = (unsigned char *) malloc(ASC_DMA_SIZE));
	memset(d->dma, 0, ASC_DMA_SIZE);

	d->dma_controller      = dma_controller;
	d->dma_controller_data = dma_controller_data;

	memory_device_register(mem, "asc", baseaddr,
	    mode == DEV_ASC_PICA? DEV_ASC_PICA_LENGTH : DEV_ASC_DEC_LENGTH,
	    dev_asc_access, d, DM_DEFAULT, NULL);

	if (mode == DEV_ASC_DEC) {
		memory_device_register(mem, "asc_dma_address_reg",
		    baseaddr + 0x40000, 4096, dev_asc_address_reg_access, d,
		    DM_DYNTRANS_OK | DM_DYNTRANS_WRITE_OK,
		    (unsigned char *)&d->dma_address_reg_memory[0]);
		memory_device_register(mem, "asc_dma", baseaddr + 0x80000,
		    ASC_DMA_SIZE, dev_asc_dma_access, d,
		    DM_DYNTRANS_OK | DM_DYNTRANS_WRITE_OK, d->dma);
	}

	machine_add_tickfunction(machine, dev_asc_tick, d, ASC_TICK_SHIFT);
}

