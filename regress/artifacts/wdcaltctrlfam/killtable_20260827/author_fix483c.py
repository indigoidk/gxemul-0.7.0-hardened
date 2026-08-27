"""#483 L1: the sweep pins the DECODE across 256 values and the PURGE at none.

BOTH flagship seats independently built the same one-line escape:

    if (idata & WDCTL_RST) {
            d->cur_command = COMMAND_RESET;
            if (idata & WDCTL_4BIT)          <- the whole mutant
                    wdc_new_command_reset(d);
    }

It escapes all 103 rows.  ROOT CAUSE, from the fable seat: *** ALL SIX purge/abort rows use
the reset value 0x0c. ***  So any guard keyed on a bit that 0x0c happens to carry escapes
every one of them -- and the sweep, which does vary the input, reads only `cur_command`.

*** AND IT IS REACHABLE BY REAL DRIVER BEHAVIOUR, not just by a maintainer's edit. ***
0x04 is the canonical soft-reset bit and 0x06 is what this tree's own row documents as
"what older OpenBSD writes".  Neither carries bit 3.  Under the mutant, 0x06 latches the
signature and leaves `write_in_progress 0x30, occ 16` -- a stale writer and a stale ring
across a reset, which is #479's corruption defect returning.

THE REMEDY IS THE OPUS SEAT'S, MEASURED BY IT BEFORE PROPOSAL: stage state before each of
the 256 writes and assert BOTH effects IFF bit 2.  A half-reset -- latch without purge, or
purge without latch -- is wrong whichever way bit 2 went.

  Measured by that seat across the whole matrix: pristine stays 103/0, the five
  abort-nulling escapes all die, and EVERY EXISTING KILL IS PRESERVED AT ITS EXACT COUNT
  (disj2 1, wipocc 1, hob6 1, hob7 2, narrow 8, revert 12).  Nothing is traded.

ALSO FIXED HERE, from the kimi-k3:cloud seat:
  * the LITERAL "256 of 256" denominator, with a silent `continue` on allocation failure --
    a sweep that tested nothing would have reported a full pass, and unlike its siblings it
    does not `return`, so the row-count tripwire could not catch it either;
  * `wide`/`narrow` are -1 sentinels printed with %02x, rendering as 0xffffffff in every
    one-sided FAIL line.
"""
import io

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"
s = io.open(P, encoding="utf-8", newline="").read()

a = s.index("static void row_reset_bit_iff(void)")
b = s.index("static void row_arm_overrun(void)")
body = s[a:b]

NEW = '''static void row_reset_bit_iff(void)
{
	int v, ran = 0, wide = -1, narrow = -1, half = -1;

	for (v = 0; v < 256; v++) {
		struct wdc_data d;
		unsigned char buf[8];
		int i, occ, want, got;

		altctl_fresh(&d);
		if (d.inbuf == NULL)
			continue;
		ran ++;
		d.cur_command = WDCC_IDENTIFY;

		/*  STATE TO PURGE.  Without it this row could only ever observe
		    the LATCH, and a guard qualifying the abort alone escaped all
		    103 rows -- built independently by both flagship seats.  */
		d.write_in_progress = WDCC_WRITE;
		d.write_count = 1;
		for (i = 0; i < 8; i++)
			wdc_addtoinbuf(&d, 0x5a);

		memset(buf, 0, sizeof(buf));
		buf[0] = v;
		dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1,
		    MEM_WRITE, &d);

		occ = d.inbuf_head - d.inbuf_tail;
		while (occ < 0)
			occ += WDC_INBUF_SIZE;

		/*  BOTH EFFECTS, IFF BIT 2.  got == 1 is a HALF RESET and is
		    wrong whichever way bit 2 went: a latch without a purge, or
		    a purge without a latch.  */
		want = (v & WDCTL_RST) ? 2 : 0;
		got  = ((d.cur_command == COMMAND_RESET) ? 1 : 0)
		     + ((d.write_in_progress == 0 && occ == 0) ? 1 : 0);

		if (got == 1 && half < 0)
			half = v;
		else if (got == 2 && want == 0 && wide < 0)
			wide = v;
		else if (got == 0 && want == 2 && narrow < 0)
			narrow = v;
		altctl_free(&d);
	}

	/*  *** THE DENOMINATOR IS COUNTED, NOT WRITTEN.  An earlier version printed
	    a LITERAL "256 of 256" after an unconditional rows++, with the NULL case
	    doing `continue` rather than `return` -- so a sweep in which every
	    allocation failed would have reported a full pass, and the row-count
	    tripwire could not have caught it either.  The comment above warns about
	    exactly that shape and the row reproduced it.  A hardcoded denominator is
	    a denominator that cannot fail.  Named by the kimi-k3:cloud seat. ***

	    The sentinels print as %i, not %02x: they are -1 when unset, and %02x
	    rendered that as 0xffffffff in every one-sided failure line.  */
	rows ++;
	if (ran != 256 || wide >= 0 || narrow >= 0 || half >= 0) {
		printf("  FAIL %-38s %i of 256 w %i n %i h %i@N@",
		    "reset ACTS IFF bit 2 is set", ran, wide, narrow, half);
		failures ++;
	} else {
		printf("  ok   %-38s %i of 256@N@",
		    "reset ACTS IFF bit 2 is set", ran);
	}
}


'''.replace("@N@", N)

#  keep the header comment, replace the function
h = body.index("static void row_reset_bit_iff(void)")
s = s[:a] + body[:h] + NEW + s[b:]
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  sweep now asserts BOTH effects, counts its denominator, and prints %i sentinels")
print("  NOTE: the label changed -- 'latches' -> 'ACTS'.  The gate grep must move with it.")
