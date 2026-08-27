"""Three row changes, all from measured seat findings, all in two rows.

  A. grok: read the signature after the 0x0c assert too.  REPAIRS A FALSE CLAIM BY MAKING
     IT TRUE -- the comment promised 0x0c coverage that no row provided.
  B. opus: cut the nIEN row as a DELTA, like its sibling.  Its oracle is ABSOLUTE
     (`== COMMAND_RESET`) where row_routine_ctl's is a delta, and `Mo_nienzero` walks
     straight through the gap: it clobbers cur_command to 0 on every nIEN write -- THE
     ROUND'S OWN DEFECT #2 -- and the row still reports ok.
  C. opus: an unreset CD-ROM must read back the cylinder bytes the GUEST WROTE.  The
     existing "non-CD-ROM does not sign" control tests the OTHER half of the read-site
     guard, so `Mo_sigalways` (drop the cur_command conjunct entirely) escapes all three
     signature checks.

Opus measured the repair: base green at 95 rows, the revert control still killed at 5, and
Mo_nienzero / Mo_nien4bit / Mo_sigalways all die.

Edits are made INSIDE each function, located by name, so an anchor cannot stray into a
neighbour -- the mistake that de-indented two lines earlier in this session.
"""
import io

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"
s = io.open(P, encoding="utf-8", newline="").read()


def within(fn, nxt, old, new, label):
    global s
    a = s.index("static void %s(void)" % fn)
    b = s.index("static void %s(void)" % nxt)
    body = s[a:b]
    c = body.count(old)
    assert c == 1, "%s: anchor occurs %d times inside %s" % (label, c, fn)
    s = s[:a] + body.replace(old, new, 1) + s[b:]
    print("  %s" % label)


TEAR = (T + "stub_cdrom_poison = 0;" + NL +
        T + "stub_disk_exists = 0;" + NL +
        T + "altctl_free(&d);" + NL)

#  ---- A + C: both land in row_srst_signature, before its teardown ---------------
ADD = ('''	/*  (C) THE RESET CONJUNCT, pinned.  The "non-CD-ROM does not sign" control
	    above tests the OTHER half of the read-site guard -- `is_a_cdrom` -- so
	    dropping the `cur_command == COMMAND_RESET` conjunct entirely escaped
	    every signature check this row had.  An UNRESET CD-ROM must read back
	    the bytes the GUEST WROTE, not a signature.  Named and measured by the
	    opus seat (`Mo_sigalways`).  */
	altctl_free(&d);
	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		stub_cdrom_poison = 0;
		stub_disk_exists = 0;
		return;
	}
	stub_cdrom_poison = 1;

	memset(buf, 0, sizeof(buf));
	buf[0] = 0x55;
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_lo, buf, 1, MEM_WRITE, &d);
	memset(buf, 0, sizeof(buf));
	buf[0] = 0x66;
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_hi, buf, 1, MEM_WRITE, &d);
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_lo, buf, 1, MEM_READ, &d);
	lo = buf[0];
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_hi, buf, 1, MEM_READ, &d);
	hi = buf[0];

	rows ++;
	if (lo != 0x55 || hi != 0x66) {
		printf("  FAIL %-38s 0x%02x%02x want 0x6655@N@",
		    "an unreset CD-ROM does not sign", hi, lo);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x%02x@N@",
		    "an unreset CD-ROM does not sign", hi, lo);
	}

	/*  (A) THE OTHER ASSERT FORM.  0x0c is what libata writes to assert SRST and
	    differs from OpenBSD's 0x06 in BIT 3 -- the exact bit this round moved away
	    from.  A predicate accepting 0x06 but not 0x0c would pass every other row
	    in this file.  Proposed by the grok seat, which found this row's comment
	    already CLAIMING 0x0c coverage that no row provided.  Fresh device, so it
	    cannot inherit the latch set above.  */
	altctl_free(&d);
	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		stub_cdrom_poison = 0;
		stub_disk_exists = 0;
		return;
	}
	stub_cdrom_poison = 1;

	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_4BIT;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_lo, buf, 1, MEM_READ, &d);
	lo = buf[0];
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_hi, buf, 1, MEM_READ, &d);
	hi = buf[0];

	rows ++;
	if (lo != 0x14 || hi != 0xeb) {
		printf("  FAIL %-38s 0x%02x%02x want 0xeb14@N@",
		    "the libata SRST form signs too", hi, lo);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x%02x@N@",
		    "the libata SRST form signs too", hi, lo);
	}

''').replace("@N@", N) + TEAR

within("row_srst_signature", "row_arm_overrun", TEAR, ADD, "A+C: 0x0c read + unreset control")

#  ---- B: the nIEN row's oracle becomes a DELTA ---------------------------------
within("row_nien_is_not_a_reset", "row_srst_aborts",
 T + "if (a == COMMAND_RESET || b == COMMAND_RESET) {" + NL,
 T + "/*  (B) A DELTA, NOT AN ABSOLUTE.  This asked only whether the value BECAME" + NL +
 T + "    COMMAND_RESET, where its sibling row asks whether the value CHANGED." + NL +
 T + "    A mutant that clobbers cur_command to 0 on an nIEN write -- which is" + NL +
 T + "    this round's own defect #2, reached through a different bit -- walked" + NL +
 T + "    straight through that gap and the row still reported ok.  Measured by" + NL +
 T + "    the opus seat (`Mo_nienzero`, `Mo_nien4bit`).  The re-pin's own" + NL +
 T + "    rationale applied to both rows; only one of them got it.  */" + NL +
 T + "if (a != WDCC_IDENTIFY || b != WDCC_IDENTIFY) {" + NL,
 "B: nIEN oracle absolute -> delta")

for lbl in ("an unreset CD-ROM does not sign", "the libata SRST form signs too"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

for a, b in [("if (rows != 94) {", "if (rows != 96) {"),
             ("rows = %i, want 94", "rows = %i, want 96")]:
    assert s.count(a) == 1, "%r occurs %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  identity pin 94 -> 96")
