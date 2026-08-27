"""#483 L1, defects 2 and 3: the orphan row's control guards the wrong threat, and it
pins a single occupancy value.

  (2) THE LIVENESS CONTROL EXCLUDES THE WRONG THING.  It proves the bytes were staged.  It
      does NOT prove that the PURGE IS SPECIFIC TO SRST -- because the live leg performs no
      altstatus access at all, a mutant that purges on ANY control write leaves it untouched
      and passes the reset leg too.

      The missing third leg: the same stores, then an altstatus write with BIT 2 CLEAR,
      asserting the bytes SURVIVE.  That is the difference between "SRST purges" and "any
      control write purges", which is the property the row actually claims.

  (3) THE ROW STAGES EXACTLY 16 BYTES, so a THRESHOLD guard (`occ > 8`) passes it while
      leaving any smaller orphan ring stale across a reset.  Closed by staging a SECOND,
      SMALLER count -- the same move the sweep makes against the mask family: pin a SPACE
      rather than a point.

      2 bytes is chosen because it is the smallest a single data-port store can produce, so
      any threshold at all is caught.

Both named by the kimi-k3:cloud seat.  Its framing is the durable part: *the surviving
escape space is multi-dimensional, not a single point.*
"""
import io

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"
s = io.open(P, encoding="utf-8", newline="").read()

a = s.index("static void row_srst_purges_orphan_ring(void)")
b = s.index("static void row_srst_aborts_pkt_empty_ring(void)")
body = s[a:b]

OLD = (T + "rows ++;" + NL +
       T + "if (live != 16 || occ != 0) {" + NL +
       T*2 + "printf(\"  FAIL %-38s live %i occ %i" + BS + "n\"," + NL +
       T*2 + "    \"an SRST purges an orphan ring\", live, occ);" + NL +
       T*2 + "failures ++;" + NL +
       T + "} else {" + NL +
       T*2 + "printf(\"  ok   %-38s live %i occ %i" + BS + "n\"," + NL +
       T*2 + "    \"an SRST purges an orphan ring\", live, occ);" + NL +
       T + "}" + NL)
assert body.count(OLD) == 1, "orphan assert occurs %d times" % body.count(OLD)

NEW = ('''	/*  THIRD LEG: A CONTROL WRITE WITH BIT 2 CLEAR MUST *NOT* PURGE.
	    The liveness leg above proves the bytes were staged.  It does NOT prove
	    the purge is specific to SRST -- it performs no altstatus access at all,
	    so a mutant purging on ANY control write leaves it untouched and passes
	    the reset leg as well.  This leg is the difference between "SRST purges"
	    and "any control write purges", which is what the row claims.
	    Named by the kimi-k3:cloud seat.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP orphan benign@N@");
		return;
	}
	for (i = 0; i < 8; i++) {
		buf[0] = 0x5a; buf[1] = 0x5a;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_4BIT;			/*  bit 2 CLEAR -- not a reset  */
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);
	benign = d.inbuf_head - d.inbuf_tail;
	while (benign < 0)
		benign += WDC_INBUF_SIZE;
	altctl_free(&d);

	/*  FOURTH LEG: A SMALLER RING, so a THRESHOLD guard cannot hide.  The row
	    staged exactly 16 bytes, so `occ > 8` in front of the abort passed it
	    while leaving every smaller orphan ring stale across a reset.  Two
	    bytes is the least a single data-port store can produce, so any
	    threshold at all is caught.  The escape space is multi-dimensional;
	    pin a SPACE, not a point -- the same move the bit-2 sweep makes.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP orphan small@N@");
		return;
	}
	buf[0] = 0x5a; buf[1] = 0x5a;
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	small_live = d.inbuf_head - d.inbuf_tail;
	while (small_live < 0)
		small_live += WDC_INBUF_SIZE;
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_4BIT;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);
	small = d.inbuf_head - d.inbuf_tail;
	while (small < 0)
		small += WDC_INBUF_SIZE;

	rows ++;
	if (live != 16 || occ != 0 || benign != 16 ||
	    small_live != 2 || small != 0) {
		printf("  FAIL %-38s live %i occ %i benign %i sm %i/%i@N@",
		    "an SRST purges an orphan ring",
		    live, occ, benign, small_live, small);
		failures ++;
	} else {
		printf("  ok   %-38s %i/%i/%i/%i/%i@N@",
		    "an SRST purges an orphan ring",
		    live, occ, benign, small_live, small);
	}
''').replace("@N@", N)

body = body.replace(OLD, NEW, 1)
body = body.replace(T + "int i, live, occ;" + NL,
                    T + "int i, live, occ, benign, small_live, small;" + NL, 1)
s = s[:a] + body + s[b:]
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  orphan row: benign-control leg and small-ring leg added")
