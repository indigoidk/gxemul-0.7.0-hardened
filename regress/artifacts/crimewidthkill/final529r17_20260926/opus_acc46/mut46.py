#!/usr/bin/env python3
"""mut46.py SRC DST -- the Opus seat's MEASUREMENT-ONLY mutant for the ACCEPTS enumeration (never product code).

Inserts, immediately before the width dispatch `if (len == 8) {' of DEVICE_ACCESS(crime) -- after the prelude, the
placement of table 16's G_glm_tim4clear -- a SILENT decline of every access the environment variable ACC46 names:
    ACC46 = SPEC[;SPEC...]      SPEC = LEN:DIR:OFF:WIN:VAL:LATCH      (`*' = any)
    LEN 4|8   DIR R|W   OFF hex relative_addr   WIN 0|1 (pc in the REV arm's PROM window)   VAL hex idata (writes)
    LATCH C|S (d->warned & CRIME_W_LEN clear / set AT THE ACCESS)
A matching access jumps to `crime_declined' with NO announce and the latch UNTOUCHED, after marking the hit on
stderr as `[ACC46HIT ...]'.  With ACC46 unset the block matches nothing.  Sentinel: MUT46_APPLIED."""
import sys

LEN8 = "\tif (len == 8) {\n"
BLOCK = r'''	/*  OPUS_ACC46: MEASUREMENT-ONLY MUTANT, never product code.  A SILENT decline of
	    the accesses $ACC46 names -- LEN:DIR:OFF:WIN:VAL:LATCH;... with `*' = any --
	    with no announce and the latch untouched; each hit is marked on stderr.  */
	{
		static int acc46_n = -1;
		static struct acc46_spec {
			int len, dir, win, latch, anyval;
			uint64_t off, val;
		} acc46[64];
		int acc46_k;
		int acc46_set = (d->warned & CRIME_W_LEN) != 0;
		int acc46_win = ((uint32_t)cpu->pc & 0xffffff00) ==
		    (uint32_t)0xbfc05100;

		if (acc46_n < 0) {
			const char *s = getenv("ACC46");
			acc46_n = 0;
			while (s != NULL && *s != '\0' && acc46_n < 64) {
				char f[6][32];
				int nf = 0, c = 0;
				memset(f, 0, sizeof(f));
				while (*s != '\0' && *s != ';') {
					if (*s == ':') {
						nf++;
						c = 0;
					} else if (nf < 6 && c < 31)
						f[nf][c++] = *s;
					s++;
				}
				if (*s == ';')
					s++;
				if (nf != 5)
					continue;
				acc46[acc46_n].len = atoi(f[0]);
				acc46[acc46_n].dir = f[1][0] == 'W' ? MEM_WRITE : MEM_READ;
				acc46[acc46_n].off = strtoull(f[2], NULL, 16);
				acc46[acc46_n].win = f[3][0] == '*' ? -1 : atoi(f[3]);
				acc46[acc46_n].anyval = f[4][0] == '*';
				acc46[acc46_n].val = strtoull(f[4], NULL, 16);
				acc46[acc46_n].latch = f[5][0] == '*' ? -1 :
				    (f[5][0] == 'S');
				acc46_n++;
			}
			fprintf(stderr, "[ACC46INIT n=%d]\n", acc46_n);
		}
		for (acc46_k = 0; acc46_k < acc46_n; acc46_k++) {
			struct acc46_spec *p = &acc46[acc46_k];
			if ((size_t)p->len != len || p->dir != writeflag ||
			    p->off != relative_addr)
				continue;
			if (p->win >= 0 && p->win != acc46_win)
				continue;
			if (!p->anyval && (writeflag != MEM_WRITE ||
			    p->val != idata))
				continue;
			if (p->latch >= 0 && p->latch != acc46_set)
				continue;
			fprintf(stderr, "[ACC46HIT len=%d %c off=0x%x latch=%c "
			    "win=%d]\n", (int)len, writeflag == MEM_WRITE ?
			    'W' : 'R', (int)relative_addr,
			    acc46_set ? 'S' : 'C', acc46_win);
			goto crime_declined;
		}
	}

'''

src, dst = sys.argv[1], sys.argv[2]
text = open(src, "r", newline="").read()
n = text.count(LEN8)
if n != 1:
    print("MUT46: anchor occurs %d times, wanted 1 -- NOT APPLIED" % n)
    sys.exit(1)
text = text.replace(LEN8, BLOCK + LEN8)
open(dst, "w", newline="").write(text)
print("MUT46_APPLIED (1 insertion before the width dispatch)")
