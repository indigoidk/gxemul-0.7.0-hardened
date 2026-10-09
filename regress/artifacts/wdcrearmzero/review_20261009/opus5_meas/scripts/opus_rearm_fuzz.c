/*
 *  opus_rearm_fuzz.c -- opus5 late REVIEW seat, wdcrearmzero (#473), 2026-10-09.
 *
 *  THE QUESTION: can any guest-reachable access leave the DATA ring NON-EMPTY when the
 *  ATAPI re-arm runs?
 *
 *  RUNG 1, AND SAID SO.  This drives the REAL dev_wdc_access() and
 *  dev_wdc_altstatus_access() of an INSTRUMENTED COPY of dev_wdc.c.  The copy differs
 *  from its revision by ONE inserted call, OPUS_REARM_PRE(d), placed at the head of the
 *  re-arm branch (`data_in_len) {`), which only READS inbuf_head/inbuf_tail.  It is a
 *  state-machine search plus directed sequences, never a witness.  Every access it makes
 *  is an ordinary register access a guest can issue on an in-tree wdc machine.
 *
 *  Three things are measured:
 *    rearm_dirty  re-arms entered with ring occupancy != 0      (THE QUESTION)
 *    inv_viol     states with flag && phase != CMDOUT && occupancy != atapi_len
 *    content_bad  bytes a DATA read pops that are not data_in[received + k]
 *  plus `short_mid`: a data read whose lanes were short-popped (over-read) while the
 *  transfer still had bytes left -- the chunk-boundary straddle.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>

int quiet_mode = 1;
static long n_fatal = 0;
void fatal(const char *fmt, ...) { (void) fmt; n_fatal ++; }

struct wdc_data;
static void opus_rearm_pre(struct wdc_data *d);
#define OPUS_REARM_PRE(dd) opus_rearm_pre(dd)

#include "../src/devices/dev_wdc.c"

void debug(const char *fmt, ...) { (void) fmt; }

uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len)
{
	uint64_t x = 0; int i;
	(void) cpu;
	for (i = 0; i < len; i++)
		x |= (uint64_t) buf[i] << (8*i);
	return x;
}

void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data)
{
	int i;
	(void) cpu;
	for (i = 0; i < len; i++)
		buf[i] = (unsigned char) (data >> (8*i));
}

/*  ---------------------------------------------------------------- stubs  */
static unsigned xfer_serial = 0;
static long n_dispatch = 0;

static unsigned char content(unsigned serial, size_t i)
{
	uint32_t x = (uint32_t) (i * 2654435761u) ^ (serial * 0x9E3779B9u);
	x ^= x >> 15; x *= 0x2c1b3c6du; x ^= x >> 12;
	return (unsigned char) x;
}

struct scsi_transfer *scsi_transfer_alloc(void)
{
	return (struct scsi_transfer *) calloc(1, sizeof(struct scsi_transfer));
}

void scsi_transfer_free(struct scsi_transfer *p)
{
	if (p == NULL)
		return;
	free(p->cmd);
	free(p->data_in);
	free(p);
}

int diskimage_scsicommand(struct cpu *cpu, int id, int type,
	struct scsi_transfer *x)
{
	size_t len = 0, i;
	unsigned char op;
	(void) cpu; (void) id; (void) type;
	n_dispatch ++;
	op = x->cmd[0];
	if (op == 0x28) {			/*  READ(10), 2048-byte blocks  */
		size_t blocks = ((size_t) x->cmd[7] << 8) | x->cmd[8];
		len = blocks * 2048;
		if (len > 600000)
			len = 600000;
	} else if (op == 0x12) {		/*  INQUIRY: allocation length  */
		len = x->cmd[4];
	} else if (op == 0x55 || op == 0x15) {
		return 2;			/*  a DATA-OUT command  */
	} else
		return 0;			/*  rejected  */
	xfer_serial ++;
	if (len == 0)
		return 1;
	x->data_in = (unsigned char *) malloc(len);
	for (i = 0; i < len; i++)
		x->data_in[i] = content(xfer_serial, i);
	x->data_in_len = len;
	return 1;
}

int diskimage_exist(struct machine *m, int id, int type)
{ (void) m; (void) id; (void) type; return 1; }

int diskimage_access(struct machine *m, int id, int type, int writeflag,
	off_t offset, unsigned char *buf, size_t len)
{
	(void) m; (void) id; (void) type; (void) offset;
	if (!writeflag && buf != NULL)
		memset(buf, 0xEE, len);
	return 1;
}

int diskimage_is_a_cdrom(struct machine *m, int id, int type)
{ (void) m; (void) id; (void) type; return 1; }

int diskimage_is_a_tape(struct machine *m, int id, int type)
{ (void) m; (void) id; (void) type; return 0; }

int diskimage_getname(struct machine *m, int id, int type, char *buf, size_t n)
{ (void) m; (void) id; (void) type; snprintf(buf, n, "opusfuzz"); return 1; }

int64_t diskimage_getsize(struct machine *m, int id, int type)
{ (void) m; (void) id; (void) type; return (int64_t) 2048 * 100000; }

/*  ---------------------------------------------------------------- rig  */
static struct machine stub_machine;
static struct cpu     stub_cpu;
static int irq_line = 0;
static void s_assert(struct interrupt *i)   { (void) i; irq_line = 1; }
static void s_deassert(struct interrupt *i) { (void) i; irq_line = 0; }

static uint64_t rng_state = 88172645463325252ULL;
static uint64_t rnd(void)
{
	rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7;
	rng_state ^= rng_state << 17; return rng_state;
}
static int rndn(int n) { return (int) (rnd() % (uint64_t) n); }

static int occ(struct wdc_data *d)
{
	int o = d->inbuf_head - d->inbuf_tail;
	while (o < 0)
		o += WDC_INBUF_SIZE;
	return o;
}

/*  the op trace, for printing the first instance of each dirty signature  */
#define TRACE_N 40
static char trace[TRACE_N][96];
static int trace_pos = 0;
static void tr(const char *fmt, ...)
{
	va_list ap;
	va_start(ap, fmt);
	vsnprintf(trace[trace_pos % TRACE_N], sizeof(trace[0]), fmt, ap);
	va_end(ap);
	trace_pos ++;
}
static void dump_trace(void)
{
	int i, start = trace_pos > TRACE_N ? trace_pos - TRACE_N : 0;
	for (i = start; i < trace_pos; i++)
		printf("      | %s\n", trace[i % TRACE_N]);
}

static void dev_init(struct wdc_data *d)
{
	memset(d, 0, sizeof(*d));
	d->addr_mult = 1;
	d->io_enabled = 1;
	d->error = 1;
	d->inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d->irq.interrupt_assert = s_assert;
	d->irq.interrupt_deassert = s_deassert;
	memset(&stub_cpu, 0, sizeof(stub_cpu));
	stub_cpu.machine = &stub_machine;
	stub_cpu.byte_order = EMUL_LITTLE_ENDIAN;
}

static void dev_fini(struct wdc_data *d)
{
	if (d->atapi_st != NULL)
		scsi_transfer_free(d->atapi_st);
	d->atapi_st = NULL;
	free(d->inbuf);
	d->inbuf = NULL;
}

static uint64_t acc(struct wdc_data *d, int reg, int len, int wr, uint64_t val)
{
	unsigned char b[8];
	memset(b, 0, sizeof(b));
	if (wr)
		memory_writemax64(&stub_cpu, b, len, val);
	dev_wdc_access(&stub_cpu, NULL, (uint64_t) reg, b, (size_t) len,
	    wr ? MEM_WRITE : MEM_READ, d);
	return memory_readmax64(&stub_cpu, b, len);
}

static uint64_t alt(struct wdc_data *d, int off, int wr, uint64_t val)
{
	unsigned char b[8];
	memset(b, 0, sizeof(b));
	if (wr)
		b[0] = (unsigned char) val;
	dev_wdc_altstatus_access(&stub_cpu, NULL, (uint64_t) off, b, 1,
	    wr ? MEM_WRITE : MEM_READ, d);
	return b[0];
}

/*  ---------------------------------------------------------------- measures  */
static long rearm_total = 0, rearm_dirty = 0;
static long inv_viol = 0, content_bad = 0, short_mid = 0, reads_total = 0;
static unsigned cur_sig = 0;		/*  interference kinds since the last dispatch  */
static long sig_hist[64];
static unsigned sig_seen[64];
static int nsig = 0;
static int quiet_dirty = 0;		/*  directed tests print their own result  */
static int last_rearm_occ = -1;

static void opus_rearm_pre(struct wdc_data *d)
{
	int o = occ(d), i;
	rearm_total ++;
	last_rearm_occ = o;
	if (o == 0)
		return;
	rearm_dirty ++;
	if (quiet_dirty)
		return;
	for (i = 0; i < nsig; i++)
		if (sig_seen[i] == cur_sig)
			break;
	if (i == nsig && nsig < 64) {
		sig_seen[nsig] = cur_sig;
		sig_hist[nsig] = 0;
		nsig ++;
		printf("  DIRTY RE-ARM #%ld: occupancy %d at re-arm entry, sig=0x%x, "
		    "received=%zu, data_in_len=%zu\n", rearm_dirty, o, cur_sig,
		    d->atapi_received, d->atapi_st ? d->atapi_st->data_in_len : 0);
		dump_trace();
	}
	if (i < 64)
		sig_hist[i] ++;
}

static int is_active(struct wdc_data *d)
{
	return d->atapi_cmd_in_progress && d->atapi_phase != PHASE_CMDOUT &&
	    d->atapi_st != NULL && d->atapi_st->data_in != NULL;
}

static long last_bad_print = 0;
static unsigned char last_lanes[8];
static void data_read(struct wdc_data *d, int len)
{
	int calls = (len == 4) ? 4 : (len >= 2 ? 2 : 1);
	int o0 = occ(d), pops = calls < o0 ? calls : o0, k;
	int act = is_active(d);
	size_t rec0 = d->atapi_received;
	unsigned char b[8];
	reads_total ++;
	if (act) {
		for (k = 0; k < pops; k++) {
			size_t p = rec0 + (size_t) k;
			unsigned char got = d->inbuf[(d->inbuf_tail + k) % WDC_INBUF_SIZE];
			if (p >= d->atapi_st->data_in_len ||
			    got != d->atapi_st->data_in[p]) {
				content_bad ++;
				if (content_bad - last_bad_print >= 1 && last_bad_print < 3 && !quiet_dirty) {
					last_bad_print ++;
					printf("  CONTENT MISMATCH: pos %zu got 0x%02x want 0x%02x (sig 0x%x)\n",
					    p, got, p < d->atapi_st->data_in_len ?
					    d->atapi_st->data_in[p] : 0, cur_sig);
				}
			}
		}
	}
	if (d->atapi_len <= 8 || o0 <= 16 || !act)
		tr("read%d occ %d alen %d rec %zu ph 0x%x fl %d", len, o0,
		    d->atapi_len, rec0, d->atapi_phase, d->atapi_cmd_in_progress);
	memset(b, 0, sizeof(b));
	dev_wdc_access(&stub_cpu, NULL, (uint64_t) wd_data, b, (size_t) len,
	    MEM_READ, d);
	memcpy(last_lanes, b, sizeof(b));
	if (act && pops < calls && d->atapi_st != NULL &&
	    d->atapi_received < d->atapi_st->data_in_len)
		short_mid ++;
}

static void inv_check(struct wdc_data *d)
{
	if (d->atapi_cmd_in_progress && d->atapi_phase != PHASE_CMDOUT &&
	    occ(d) != d->atapi_len) {
		inv_viol ++;
	}
}

/*  ---------------------------------------------------------------- guest ops  */
static void send_cdb(struct wdc_data *d, const unsigned char cdb[12])
{
	int i;
	acc(d, wd_command, 1, 1, 0xa0);
	tr("CMD 0xa0 (PKT)");
	for (i = 0; i < 12; i += 2)
		acc(d, wd_data, 2, 1, (uint64_t) cdb[i] | ((uint64_t) cdb[i+1] << 8));
	tr("CDB op 0x%02x written (6 words)", cdb[0]);
}

static void start_read10(struct wdc_data *d, int blocks)
{
	unsigned char cdb[12];
	memset(cdb, 0, sizeof(cdb));
	cdb[0] = 0x28;
	cdb[7] = (unsigned char) (blocks >> 8);
	cdb[8] = (unsigned char) blocks;
	send_cdb(d, cdb);
	cur_sig = 0;
}

static void start_inquiry(struct wdc_data *d, int alloc)
{
	unsigned char cdb[12];
	memset(cdb, 0, sizeof(cdb));
	cdb[0] = 0x12;
	cdb[4] = (unsigned char) alloc;
	send_cdb(d, cdb);
	cur_sig = 0;
}

#define N_EV 23
static const char *ev_name[N_EV] = {
	"DATA_WRITE_2", "DATA_WRITE_4", "DATA_WRITE_1", "DATA_WRITE_3",
	"CMD_PKT_BARE", "CMD_ATAPI_IDENTIFY", "CMD_ATA_READ", "CMD_ATAPI_SOFTRESET",
	"CMD_RECAL", "CMD_RANDOM", "ALTCTRL_SRST", "ALTCTRL_0x08",
	"ALTCTRL_0x0e", "ALT_OFF1_WRITE", "ALT_STATUS_READ", "STATUS_READ",
	"REG_READ_RANDOM", "REG_WRITE_RANDOM", "SDH_WRITE", "CDB_PARTIAL",
	"NEW_TRANSFER", "DATA_READ_1", "DATA_READ_8"
};

static void apply_event(struct wdc_data *d, int ev)
{
	int r, i, k;
	if (ev < 20)
		cur_sig |= 1u << (ev < 31 ? ev : 31);
	switch (ev) {
	case 0:  acc(d, wd_data, 2, 1, rnd()); break;
	case 1:  acc(d, wd_data, 4, 1, rnd()); break;
	case 2:  acc(d, wd_data, 1, 1, rnd()); break;
	case 3:  acc(d, wd_data, 3, 1, rnd()); break;
	case 4:  acc(d, wd_command, 1, 1, 0xa0); break;
	case 5:  acc(d, wd_command, 1, 1, 0xa1); break;
	case 6:  acc(d, wd_seccnt, 1, 1, 1 + rndn(4));
		 acc(d, wd_command, 1, 1, 0x20); break;
	case 7:  acc(d, wd_command, 1, 1, 0x08); break;
	case 8:  acc(d, wd_command, 1, 1, 0x10); break;
	case 9:  acc(d, wd_command, 1, 1, rndn(256)); break;
	case 10: alt(d, 0, 1, 0x04); alt(d, 0, 1, 0x00); break;
	case 11: alt(d, 0, 1, 0x08); break;
	case 12: alt(d, 0, 1, 0x0e); alt(d, 0, 1, 0x0a); break;
	case 13: alt(d, 1, 1, rndn(256)); break;
	case 14: alt(d, 0, 0, 0); break;
	case 15: acc(d, wd_command, 1, 0, 0); break;
	case 16: r = 1 + rndn(6); acc(d, r, 1, 0, 0); break;
	case 17: r = 1 + rndn(6); acc(d, r, 1, 1, rndn(256)); break;
	case 18: acc(d, wd_sdh, 1, 1, rndn(2) ? 0xa0 : 0xb0); break;
	case 19: k = 1 + rndn(5);
		 for (i = 0; i < k; i++)
			acc(d, wd_data, 2, 1, rnd());
		 break;
	case 20: start_read10(d, 17 + rndn(120)); break;
	case 21: data_read(d, 1); break;
	case 22: data_read(d, 8); break;
	}
	tr("EVENT %s", ev_name[ev]);
	inv_check(d);
}

/*  after an event that ended the packet command, a follow-up that re-enters
    ATAPI accounting without a fresh transfer -- the stale-state route  */
static void follow_up(struct wdc_data *d)
{
	int f = rndn(4);
	if (f == 0) {
		acc(d, wd_command, 1, 1, 0xa0);
		tr("FOLLOWUP bare PKT 0xa0");
		cur_sig |= 1u << 24;
	} else if (f == 1) {
		start_read10(d, 17 + rndn(120));
		tr("FOLLOWUP new READ10");
	}
	inv_check(d);
}

static int width_for(int policy)
{
	switch (policy) {
	case 0: return 2;
	case 1: return 4;
	case 2: return 1;
	case 3: { int w[3] = {1, 2, 4}; return w[rndn(3)]; }
	default: { int w[5] = {1, 2, 3, 4, 8}; return w[rndn(5)]; }
	}
}

/*  ---------------------------------------------------------------- fuzz  */
static int heavy = 0;		/*  1: up to 8 events across 4 chunks  */
static void fuzz(long sessions)
{
	long s;
	static const int blocks_menu[] = { 17, 20, 32, 33, 48, 64, 96, 128, 129, 192, 255 };
	for (s = 0; s < sessions; s++) {
		struct wdc_data d;
		long trig[8]; int evs[8], ne, i, policy, steps;
		long bytes_req = 0;
		dev_init(&d);
		stub_cpu.byte_order = rndn(2) ? EMUL_LITTLE_ENDIAN : EMUL_BIG_ENDIAN;
		policy = rndn(10) < 7 ? (rndn(2) ? 0 : 1) : 2 + rndn(3);
		if (rndn(12) == 0)
			start_inquiry(&d, 1 + rndn(255));
		else
			start_read10(&d, blocks_menu[rndn(11)]);
		inv_check(&d);
		ne = heavy ? 1 + rndn(8) : 1 + rndn(3);
		for (i = 0; i < ne; i++) {
			static const int offs[] = { 0, 12, 32668, 32756, 32760, 32764, 32766, 32767 };
			int c = heavy ? rndn(4) : rndn(2);
			long o = rndn(3) == 0 ? (long) rndn(32768) : offs[rndn(8)];
			trig[i] = (long) c * 32768 + o;
			evs[i] = rndn(N_EV);
		}
		/*  sort triggers  */
		for (i = 0; i < ne; i++) {
			int j;
			for (j = i + 1; j < ne; j++)
				if (trig[j] < trig[i]) {
					long t = trig[i]; int e = evs[i];
					trig[i] = trig[j]; evs[i] = evs[j];
					trig[j] = t; evs[j] = e;
				}
		}
		i = 0;
		for (steps = 0; steps < 400000; steps++) {
			int w;
			while (i < ne && bytes_req >= trig[i]) {
				apply_event(&d, evs[i]);
				if (evs[i] >= 4 && evs[i] <= 12 && rndn(2))
					follow_up(&d);
				i ++;
			}
			if (i >= ne && d.atapi_cmd_in_progress &&
			    d.atapi_phase == PHASE_COMPLETED && occ(&d) == 0)
				break;
			if (i >= ne && !d.atapi_cmd_in_progress && occ(&d) == 0)
				break;
			w = width_for(policy);
			data_read(&d, w);
			bytes_req += (w == 4) ? 4 : (w >= 2 ? 2 : 1);
			inv_check(&d);
		}
		dev_fini(&d);
	}
}

/*  ---------------------------------------------------------------- directed  */
/*  THE GUEST-EYE CHECK.  The guest counts the lanes it asked for; lane n of the
    transfer should be data_in[n] of the transfer it started.  Independent of the
    ring, so it also sees what a full ring hides from an occupancy reading.
    Little-endian cpu: lanes arrive in buffer order (see memory_writemax64).  */
static unsigned char *g_data = NULL;
static size_t g_len = 0, g_pos = 0;
static long g_bad = 0, g_first_bad = -1;
static void drain(struct wdc_data *d, long nbytes, int w)
{
	long got = 0;
	int lanes = (w == 4) ? 4 : (w >= 2 ? 2 : 1), k;
	while (got < nbytes) {
		data_read(d, w);
		for (k = 0; k < lanes; k++, g_pos++)
			if (g_data != NULL && g_pos < g_len &&
			    last_lanes[k] != g_data[g_pos]) {
				if (g_first_bad < 0)
					g_first_bad = (long) g_pos;
				g_bad ++;
			}
		got += lanes;
	}
}

static void directed(const char *name, int which, int blocks)
{
	struct wdc_data d;
	long dirty0 = rearm_dirty, bad0 = content_bad, tot0 = rearm_total, sm0 = short_mid;
	quiet_dirty = 1;
	dev_init(&d);
	last_rearm_occ = -1;
	start_read10(&d, blocks);		/*  blocks x 2048 B; chunk 1 = 32768  */
	free(g_data);
	g_data = NULL; g_len = 0; g_pos = 0; g_bad = 0; g_first_bad = -1;
	if (d.atapi_st != NULL && d.atapi_st->data_in != NULL) {
		g_len = d.atapi_st->data_in_len;
		g_data = (unsigned char *) malloc(g_len);
		memcpy(g_data, d.atapi_st->data_in, g_len);
	}
	switch (which) {
	case 1:	/*  D1: a data-port WRITE mid-chunk  */
		drain(&d, 32766, 2);
		acc(&d, wd_data, 2, 1, 0x5aa5);
		drain(&d, 2 + 32768, 2);	/*  finish chunk 1, then ALL of chunk 2  */
		break;
	case 2:	/*  D2: ATAPI IDENTIFY then a bare PACKET mid-chunk, then drain  */
		drain(&d, 32668, 2);
		acc(&d, wd_command, 1, 1, 0xa1);
		acc(&d, wd_command, 1, 1, 0xa0);
		drain(&d, 100 + 8, 2);
		break;
	case 3:	/*  D3: Device Control SRST (0x04, released), IDENTIFY, PACKET  */
		drain(&d, 32668, 2);
		alt(&d, 0, 1, 0x04); alt(&d, 0, 1, 0x00);
		acc(&d, wd_command, 1, 1, 0xa1);
		acc(&d, wd_command, 1, 1, 0xa0);
		drain(&d, 100 + 8, 2);
		break;
	case 4:	/*  D4: the FULL-RING route -- 229888 one-byte writes, then drain  */
		{
			long i;
			for (i = 0; i < 229888; i++)
				acc(&d, wd_data, 1, 1, 0x77);
			drain(&d, 32768 + 8, 1);
		}
		break;
	case 5:	/*  D5: mixed widths straddle the chunk boundary  */
		drain(&d, 1, 1);
		drain(&d, 32764, 4);		/*  atapi_len now 3  */
		drain(&d, 4 + 32764, 4);	/*  the straddling read, then chunk 2  */
		break;
	case 6:	/*  D6: control -- a conforming 2-byte reader, no interference  */
		drain(&d, 32768 + 32768, 2);
		break;
	case 7:	/*  D7: a conforming 2-byte reader drains the WHOLE transfer  */
		drain(&d, (long) blocks * 2048, 2);
		break;
	}
	printf("  %-50s re-arms %ld dirty %ld (entry occ %d) | ring-content bad %ld | "
	    "straddle %ld | GUEST-EYE wrong %ld of %zu lanes, first at %ld | "
	    "after: alen %d occ %d phase 0x%x\n", name,
	    rearm_total - tot0, rearm_dirty - dirty0, last_rearm_occ,
	    content_bad - bad0, short_mid - sm0, g_bad, g_pos, g_first_bad,
	    d.atapi_len, occ(&d), d.atapi_phase);
	dev_fini(&d);
	quiet_dirty = 0;
}

int main(int argc, char *argv[])
{
	long sessions = argc > 1 ? atol(argv[1]) : 3000;
	int i;
	if (argc > 2)
		rng_state = 88172645463325252ULL ^ (uint64_t) atoll(argv[2]) * 0x9E3779B97F4A7C15ULL;
	if (argc > 3)
		heavy = atoi(argv[3]);
	printf("seed-arg %s heavy %d\n", argc > 2 ? argv[2] : "default", heavy);
	printf("opus_rearm_fuzz: directed sequences (READ(10) of 2048-byte blocks, chunk 32768)\n");
	directed("D1 192blk data-port WRITE mid-chunk", 1, 192);
	directed("D1 32blk  data-port WRITE mid-chunk", 1, 32);
	directed("D2 192blk ATAPI IDENTIFY + bare PACKET", 2, 192);
	directed("D3 192blk SRST + IDENTIFY + PACKET", 3, 192);
	directed("D4 192blk full ring: 229888 1-byte writes", 4, 192);
	directed("D4 32blk  full ring: 229888 1-byte writes", 4, 32);
	directed("D5 192blk mixed-width straddle", 5, 192);
	directed("D5 32blk  mixed-width straddle", 5, 32);
	directed("D6 192blk CONTROL conforming 2-byte reader", 6, 192);
	directed("D6 32blk  CONTROL conforming 2-byte reader", 6, 32);
	directed("D7 96blk  whole transfer, conforming reader", 7, 96);
	directed("D7 128blk whole transfer, conforming reader", 7, 128);
	directed("D7 129blk whole transfer, conforming reader", 7, 129);

	rearm_total = rearm_dirty = inv_viol = content_bad = short_mid = reads_total = 0;
	last_bad_print = 0;
	printf("random search: %ld sessions\n", sessions);
	fuzz(sessions);
	printf("RESULT sessions=%ld reads=%ld dispatches=%ld rearm_total=%ld "
	    "rearm_dirty=%ld inv_viol=%ld content_bad=%ld short_mid=%ld\n",
	    sessions, reads_total, n_dispatch, rearm_total, rearm_dirty,
	    inv_viol, content_bad, short_mid);
	for (i = 0; i < nsig; i++) {
		int b;
		printf("  dirty sig 0x%06x x%ld :", sig_seen[i], sig_hist[i]);
		for (b = 0; b < 25; b++)
			if (sig_seen[i] & (1u << b))
				printf(" %s", b == 24 ? "FOLLOWUP_BARE_PKT" : ev_name[b]);
		printf("\n");
	}
	printf("FUZZ_DONE\n");
	return 0;
}
