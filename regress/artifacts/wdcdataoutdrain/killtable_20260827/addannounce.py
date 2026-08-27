"""Rows for #478's decline-and-announce.

The oracle counts fatal() EMISSIONS, not the latch field.  The latch is a proxy: a fix
that sets the flag and never prints, or prints without setting it, passes a latch check
and fails the property.  The tree's own idiom is "N=1 PER DEVICE INSTANCE", and only an
emission count can measure both halves of that -- the 1 and the per-instance.

Three rows:
  * the announce FIRES on the input where a spurious sector used to reach the disk
  * it does NOT fire a second time on the same device
  * it DOES fire again on a DIFFERENT device -- which is what "per instance" means, and
    what a `static` counter (the shape #269 warns about) would get wrong
"""
import io

NL = chr(10)
DET = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"

s = io.open(DET, encoding="utf-8", newline="").read()

# ---- count fatal() emissions ----
OLD = ('void fatal(const char *fmt, ...)' + NL + '{' + NL +
       chr(9) + 'va_list ap;' + NL)
assert s.count(OLD) == 1, "fatal anchor %d" % s.count(OLD)
NEW = ('static int stub_fatals = 0;' + chr(9) + '/*  #478: EMISSIONS, not the latch  */' + NL + NL +
       'void fatal(const char *fmt, ...)' + NL + '{' + NL +
       chr(9) + 'va_list ap;' + NL +
       chr(9) + 'stub_fatals ++;' + NL)
s = s.replace(OLD, NEW, 1)

ROW = r'''

/*  #478's DECLINE-AND-ANNOUNCE, measured by EMISSION COUNT rather than by the latch.
 *
 *  The latch field is a proxy and a weak one: a fix that sets the flag without
 *  printing, or prints without setting it, satisfies a latch check and fails the
 *  property.  `fatal()` is counted instead, so both halves of "N=1 PER DEVICE
 *  INSTANCE" are observable -- the ONE, and the PER INSTANCE.
 *
 *  The third row is the one that matters for the idiom.  `#269` records that a
 *  shared counter across instances is the wrong shape; a `static` latch would pass
 *  rows one and two and fail row three.
 */
static void row_drain_announce(void)
{
	struct wdc_data d, e;
	unsigned char buf[8];
	int first, second, other;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP announce inbuf failed\n");
		return;
	}
	d.write_in_progress = WDCC_WRITE;
	d.write_count  = 1;
	d.write_offset = 0xd000;

	/*  the input where a spurious sector USED to reach the disk image  */
	stub_fatals = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);
	first = stub_fatals;

	/*  the SAME device again: the latch must hold  */
	stub_fatals = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);
	second = stub_fatals;

	/*  a DIFFERENT device: "per instance" means this one still gets told  */
	memset(&e, 0, sizeof(e));
	e.addr_mult  = 1;
	e.io_enabled = 1;
	e.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	e.irq.interrupt_assert = arm_sink;
	if (e.inbuf == NULL) { free(d.inbuf); return; }
	e.write_in_progress = WDCC_WRITE;
	e.write_count  = 1;
	e.write_offset = 0xd000;
	stub_fatals = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &e);
	other = stub_fatals;

	/*  the bad-len arm ALSO latches once, so the first access emits two
	    messages: #337's width notice and #478's dropped-write notice.  What
	    this row pins is that the count does not GROW on repetition.  */
	rows ++;
	if (first < 1) {
		printf("  FAIL %-38s emitted %i, want >= 1\n",
		    "a dropped write is announced", first);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a dropped write is announced", first);
	}

	rows ++;
	if (second != 0) {
		printf("  FAIL %-38s emitted %i on repeat, want 0\n",
		    "the announce is latched per device", second);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "the announce is latched per device", second);
	}

	rows ++;
	if (other < 1) {
		printf("  FAIL %-38s emitted %i, want >= 1\n",
		    "a second device is still told", other);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a second device is still told", other);
	}

	free(e.inbuf);
	free(d.inbuf);
}

'''

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)

reg = chr(9) + "row_altctl_cdb_accept();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + chr(9) + "row_drain_announce();" + NL, 1)

for a, b in [("if (rows != 57) {", "if (rows != 60) {"),
             ("rows = %i, want 57", "rows = %i, want 60")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

for lbl in ("a dropped write is announced",
            "the announce is latched per device",
            "a second device is still told"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  stub_fatals + 3 announce rows appended, pin -> 60")
