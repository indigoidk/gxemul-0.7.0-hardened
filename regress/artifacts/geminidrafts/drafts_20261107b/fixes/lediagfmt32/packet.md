# GXemul hardened fork -- DRAFT A FIX for one filed issue, `lediagfmt32` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `lediagfmt32`, state `open`, severity `LOW`)

**title:** src/devices/dev_le.c:110,112,231,233 -- the init-block debug lines pass the uint32_t rdra and tdra to %06llx, which reads an unsigned long long (undefined under C99 7.19.6.1p9), the opposite width mismatch from lediagfmt's -- DIAGNOSTIC

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- diagnostic format string mismatch causes undefined behavior and requires a simple typecast.

## The code at the cited lines

### `src/devices/dev_le.c` around the row's cited line 110 (HEAD 8d9df658, lines 1-230)

```c
    1| /*
    2|  *  Copyright (C) 2003-2021  Anders Gavare.  All rights reserved.
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
   28|  *  COMMENT: LANCE ethernet, as used in DECstations
   29|  *
   30|  *  This is based on "PMAD-AA TURBOchannel Ethernet Module Functional
   31|  *  Specification". I've tried to keep symbol names in this file to what
   32|  *  the specs use.
   33|  *
   34|  *  This is what the memory layout looks like on a DECstation 5000/200:
   35|  *
   36|  *	0x000000 - 0x0fffff	Ethernet SRAM buffer  (should be 128KB)
   37|  *	0x100000 - 0x17ffff	LANCE registers
   38|  *	0x1c0000 - 0x1fffff	Ethernet Diagnostic ROM and Station
   39|  *				Address ROM
   40|  *
   41|  *  The length of the device is set to 0x1c0200, however, because Sprite
   42|  *  tries to read TURBOchannel rom data from 0x1c03f0, and that is provided
   43|  *  by the turbochannel device, not this device.
   44|  *
   45|  *
   46|  *  TODO:  RX ring exhaustion is emulated as of #262: a dropped frame sets
   47|  *	   CSR0.MISS (first buffer) or descriptor ERR|BUFF+RINT (mid-frame).
   48|  *
   49|  *	   (Old bug, but probably still valid:  "UDP packets that are too 
   50|  *	   large are not handled well by the Lance device.")
   51|  */
   52| 
   53| #include <stdio.h>
   54| #include <stdlib.h>
   55| #include <string.h>
   56| 
   57| #include "cpu.h"
   58| #include "devices.h"
   59| #include "emul.h"
   60| #include "machine.h"
   61| #include "memory.h"
   62| #include "misc.h"
   63| #include "net.h"
   64| 
   65| #include "thirdparty/if_lereg.h"
   66| 
   67| 
   68| #define	LE_TICK_SHIFT		14
   69| 
   70| 
   71| extern int quiet_mode;
   72| 
   73| #define	LE_MODE_PROM		0x8000
   74| #define	LE_MODE_LOOP		0x0004
   75| #define	LE_MODE_DTX		0x0002
   76| #define	LE_MODE_DRX		0x0001
   77| 
   78| 
   79| #define	N_REGISTERS		4
   80| #define	SRAM_SIZE		(128*1024)
   81| #define	ROM_SIZE		32
   82| 
   83| 
   84| struct le_data {
   85| 	struct nic_data	nic;
   86| 
   87| 	int		subsys;		/*  for debugmsg  */
   88| 
   89| 	struct interrupt irq;
   90| 	int		irq_asserted;
   91| 
   92| 	uint64_t	buf_start;
   93| 	uint64_t	buf_end;
   94| 	int		len;
   95| 
   96| 	uint8_t		rom[ROM_SIZE];
   97| 
   98| 	int		reg_select;
   99| 	uint16_t	reg[N_REGISTERS];
  100| 
  101| 	int		is_bigendian;
  102| 
  103| 	unsigned char	*sram;
  104| 
  105| 	/*  Initialization block:  */
  106| 	uint32_t	init_block_addr;
  107| 
  108| 	uint16_t	mode;
  109| 	uint16_t	ladrf[4];
  110| 	uint32_t	rdra;	/*  receive descriptor ring address  */
  111| 	int		rlen;	/*  nr of rx descriptors  */
  112| 	uint32_t	tdra;	/*  transmit descriptor ring address  */
  113| 	int		tlen;	/*  nr ot tx descriptors  */
  114| 
  115| 	int		allmulti;/* receive all multicast packets */
  116| 
  117| 	/*  Current rx and tx descriptor indices:  */
  118| 	int		rxp;
  119| 	int		txp;
  120| 
  121| 	unsigned char	*tx_packet;
  122| 	int		tx_packet_len;
  123| 
  124| 	unsigned char	*rx_packet;
  125| 	int		rx_packet_len;
  126| 	int		rx_packet_offset;
  127| 	int		rx_middle_bit;
  128| };
  129| 
  130| 
  131| /*
  132|  *  le_read_16bit():
  133|  *
  134|  *  Read a 16-bit word from the SRAM.
  135|  */
  136| static uint64_t le_read_16bit(struct le_data *d, int addr)
  137| {
  138| 	if (d->is_bigendian)
  139| 		return (d->sram[addr & (SRAM_SIZE-1)] << 8) +
  140| 			(d->sram[(addr+1) & (SRAM_SIZE-1)]);
  141| 
  142| 	return d->sram[addr & (SRAM_SIZE-1)] +
  143| 	       (d->sram[(addr+1) & (SRAM_SIZE-1)] << 8);
  144| }
  145| 
  146| 
  147| /*
  148|  *  le_write_16bit():
  149|  *
  150|  *  Write a 16-bit word to the SRAM.
  151|  */
  152| static void le_write_16bit(struct le_data *d, int addr, uint16_t x)
  153| {
  154| 	if (d->is_bigendian)
  155| 	{
  156| 		d->sram[addr & (SRAM_SIZE-1)] = (x >> 8) & 0xff;
  157| 		d->sram[(addr+1) & (SRAM_SIZE-1)] = x & 0xff;
  158| 	}
  159| 	else
  160| 	{
  161| 		d->sram[addr & (SRAM_SIZE-1)] = x & 0xff;
  162| 		d->sram[(addr+1) & (SRAM_SIZE-1)] = (x >> 8) & 0xff;
  163| 	}
  164| 
  165| }
  166| 
  167| 
  168| /*
  169|  *  le_chip_init():
  170|  *
  171|  *  Initialize data structures by reading an 'initialization block' from the
  172|  *  SRAM.
  173|  */
  174| static void le_chip_init(struct le_data *d)
  175| {
  176| 	uint16_t tmp;
  177| 	uint8_t macaddr[6];
  178| 
  179| 	d->init_block_addr = (d->reg[1] & 0xffff) + ((d->reg[2] & 0xff) << 16);
  180| 	if (d->init_block_addr & 1)
  181| 		debugmsg(d->subsys, "initialization block", VERBOSITY_WARNING,
  182| 		    "WARNING! address not word aligned?");
  183| 
  184| 	debugmsg(d->subsys, "initialization block", VERBOSITY_DEBUG,
  185| 	    "init_block_addr = 0x%06x", d->init_block_addr);
  186| 
  187| 	d->mode = le_read_16bit(d, d->init_block_addr + 0);
  188| 
  189| 	/*
  190| 	 * The MAC address is packed into the PADR field as 3 little-endian
  191| 	 * 16-bit words.
  192| 	 */
  193| 	tmp = le_read_16bit(d, d->init_block_addr + 2);
  194| 	macaddr[0] = (uint8_t)(tmp);
  195| 	macaddr[1] = (uint8_t)(tmp >> 8);
  196| 	tmp = le_read_16bit(d, d->init_block_addr + 4);
  197| 	macaddr[2] = (uint8_t)(tmp);
  198| 	macaddr[3] = (uint8_t)(tmp >> 8);
  199| 	tmp = le_read_16bit(d, d->init_block_addr + 6);
  200| 	macaddr[4] = (uint8_t)(tmp);
  201| 	macaddr[5] = (uint8_t)(tmp >> 8);
  202| 	memcpy(d->nic.mac_address, macaddr, sizeof(d->nic.mac_address));
  203| 
  204| 	/*
  205| 	 * The muticast address filter is packed into the LADRF field
  206| 	 * as 4 little-endian 16-bit words.
  207| 	 */
  208| 	d->ladrf[0] = le_read_16bit(d, d->init_block_addr + 8);
  209| 	d->ladrf[1] = le_read_16bit(d, d->init_block_addr + 10);
  210| 	d->ladrf[2] = le_read_16bit(d, d->init_block_addr + 12);
  211| 	d->ladrf[3] = le_read_16bit(d, d->init_block_addr + 14);
  212| 	if (d->ladrf[0] == 0xffff && d->ladrf[1] == 0xffff &&
  213| 	    d->ladrf[2] == 0xffff && d->ladrf[3] == 0xffff)
  214| 		d->allmulti = 1;
  215| 	else
  216| 		d->allmulti = 0;
  217| 
  218| 	d->rdra = le_read_16bit(d, d->init_block_addr + 16);
  219| 	d->rdra += ((le_read_16bit(d, d->init_block_addr + 18) & 0xff) << 16);
  220| 	d->rlen = 1 << ((le_read_16bit(d, d->init_block_addr + 18) >> 13) & 7);
  221| 	d->tdra = le_read_16bit(d, d->init_block_addr + 20);
  222| 	d->tdra += ((le_read_16bit(d, d->init_block_addr + 22) & 0xff) << 16);
  223| 	d->tlen = 1 << ((le_read_16bit(d, d->init_block_addr + 22) >> 13) & 7);
  224| 
  225| 	debug("[ le: DEBUG: mode                 %04x ]\n", d->mode);
  226| 	debug("[ le: DEBUG: padr    %02x:%02x:%02x:%02x:%02x:%02x ]\n",
  227| 	      macaddr[0], macaddr[1], macaddr[2],
  228| 	      macaddr[3], macaddr[4], macaddr[5]);
  229| 	debug("[ le: DEBUG: ladrf %04x:%04x:%04x:%04x ]\n",
  230| 	      d->ladrf[0], d->ladrf[1], d->ladrf[2], d->ladrf[3]);
```

## The data structures those files define (every field that exists)

### `src/devices/dev_le.c` -- `struct le_data {` (HEAD lines 84-128)

```c
   84| struct le_data {
   85| 	struct nic_data	nic;
   86| 
   87| 	int		subsys;		/*  for debugmsg  */
   88| 
   89| 	struct interrupt irq;
   90| 	int		irq_asserted;
   91| 
   92| 	uint64_t	buf_start;
   93| 	uint64_t	buf_end;
   94| 	int		len;
   95| 
   96| 	uint8_t		rom[ROM_SIZE];
   97| 
   98| 	int		reg_select;
   99| 	uint16_t	reg[N_REGISTERS];
  100| 
  101| 	int		is_bigendian;
  102| 
  103| 	unsigned char	*sram;
  104| 
  105| 	/*  Initialization block:  */
  106| 	uint32_t	init_block_addr;
  107| 
  108| 	uint16_t	mode;
  109| 	uint16_t	ladrf[4];
  110| 	uint32_t	rdra;	/*  receive descriptor ring address  */
  111| 	int		rlen;	/*  nr of rx descriptors  */
  112| 	uint32_t	tdra;	/*  transmit descriptor ring address  */
  113| 	int		tlen;	/*  nr ot tx descriptors  */
  114| 
  115| 	int		allmulti;/* receive all multicast packets */
  116| 
  117| 	/*  Current rx and tx descriptor indices:  */
  118| 	int		rxp;
  119| 	int		txp;
  120| 
  121| 	unsigned char	*tx_packet;
  122| 	int		tx_packet_len;
  123| 
  124| 	unsigned char	*rx_packet;
  125| 	int		rx_packet_len;
  126| 	int		rx_packet_offset;
  127| 	int		rx_middle_bit;
  128| };
```

### `src/include/net.h` -- `struct nic_data` (HEAD lines 118-122)

```c
  118| struct nic_data {
  119| 	struct net	*net;		/* net we belong to */
  120| 	uint8_t		mac_address[6];	/* our MAC address */
  121| 	int		promiscuous_mode;/* receive all packets */
  122| };
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

End with one line: `FIXDRAFT_LEDIAGFMT32: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
