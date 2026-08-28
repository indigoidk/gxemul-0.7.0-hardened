"""wdcoddstep: is it still live at HEAD, or did #475's clamp already close it?

The queue says MEASURED: with `atapi_len = 3` and a four-byte read, `atapi_len` lands on -1
and `atapi_received` on 4 where `data_in_len` is 3.

BUT #475 ADDED `if (consumed > d->atapi_len) consumed = d->atapi_len;` IMMEDIATELY BEFORE the
subtraction.  If that clamp is on the path the queue's route takes, the subtraction cannot go
negative and the row is OVERTAKEN -- the single most valuable thing a triage can find.

So this measures rather than reads, through the REAL REGISTER PATH (`dev_wdc_access`), not by
calling internals -- the lesson #485 paid for.

  LEG 1  the queue's exact route: atapi_len 3, a FOUR-byte data-port read.
         Report atapi_len, atapi_received, and data_in_len.
  LEG 2  a control that must still work: an EVEN transfer of the same size class,
         so a red leg 1 cannot be blamed on the fixture.
  LEG 3  the truthfulness half the owner ruled on: does atapi_received exceed
         data_in_len?  That is the half `<= 0` would leave open.
"""
import io
import os
import shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\odd")

src = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
              encoding="utf-8", newline="").read()

ROW = '''

/*  wdcoddstep: MEASURE whether #475's clamp already closed it.  */
static void probe_oddstep(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int len3 = -1, recv3 = -1, dil3 = -1;
	int len4 = -1, recv4 = -1, dil4 = -1;

	/*  LEG 1 -- THE QUEUE'S EXACT ROUTE: atapi_len 3, a FOUR-byte read.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP odd1@N@"); return; }
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_st = scsi_transfer_alloc();
	d.atapi_st->data_in_len = 3;
	d.atapi_st->data_in = (unsigned char *) malloc(3);
	memset(d.atapi_st->data_in, 0x5a, 3);
	d.atapi_len = 3;
	d.atapi_received = 0;
	wdc_addtoinbuf(&d, 0x5a); wdc_addtoinbuf(&d, 0x5a); wdc_addtoinbuf(&d, 0x5a);
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 4, MEM_READ, &d);
	len3 = d.atapi_len;
	recv3 = d.atapi_received;
	dil3 = (d.atapi_st != NULL) ? (int) d.atapi_st->data_in_len : -1;
	altctl_free(&d);

	/*  LEG 2 -- THE CONTROL: an EVEN transfer of the same size class must be
	    unaffected, so a red leg 1 cannot be blamed on the fixture.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP odd2@N@"); return; }
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_st = scsi_transfer_alloc();
	d.atapi_st->data_in_len = 4;
	d.atapi_st->data_in = (unsigned char *) malloc(4);
	memset(d.atapi_st->data_in, 0x5a, 4);
	d.atapi_len = 4;
	d.atapi_received = 0;
	wdc_addtoinbuf(&d, 0x5a); wdc_addtoinbuf(&d, 0x5a);
	wdc_addtoinbuf(&d, 0x5a); wdc_addtoinbuf(&d, 0x5a);
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 4, MEM_READ, &d);
	len4 = d.atapi_len;
	recv4 = d.atapi_received;
	dil4 = (d.atapi_st != NULL) ? (int) d.atapi_st->data_in_len : -1;
	altctl_free(&d);

	rows ++;
	printf("  ODDSTEP odd(len3,4byte): atapi_len=%i received=%i data_in_len=%i"
	    " | even control: atapi_len=%i received=%i data_in_len=%i@N@",
	    len3, recv3, dil3, len4, recv4, dil4);
	printf("  ODDSTEP want odd: atapi_len >= 0 AND received <= 3"
	    "   (negative = the defect is LIVE; over-count = the truthfulness half)@N@");
	if (len3 < 0 || (dil3 >= 0 && recv3 > dil3)) {
		printf("  FAIL %-38s see the ODDSTEP line@N@", "wdcoddstep is closed");
		failures ++;
	} else {
		printf("  ok   %-38s len=%i recv=%i@N@",
		    "wdcoddstep is closed", len3, recv3);
	}
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert src.count(anchor) == 1, "anchor %d" % src.count(anchor)
reg = T + "row_completion_irq();" + NL
assert src.count(reg) == 1, "reg %d" % src.count(reg)
s = src.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "probe_oddstep();" + NL, 1)
for a, b in [("if (rows != 128) {", "if (rows != 129) {"),
             ("rows = %i, want 128", "rows = %i, want 129")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "regress"))
os.makedirs(os.path.join(OUT, "src", "devices"))
io.open(os.path.join(OUT, "regress", "diff_wdc_identify.c"),
        "w", encoding="utf-8", newline="").write(s)
shutil.copy(os.path.join(ROOT, "src", "devices", "dev_wdc.c"),
            os.path.join(OUT, "src", "devices", "dev_wdc.c"))
print("  oddstep probe written; REPO NOT TOUCHED")
