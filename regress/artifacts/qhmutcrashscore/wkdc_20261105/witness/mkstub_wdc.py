#!/usr/bin/env python3
"""mkstub_wdc.py MODE -- print a STUB stand-in for regress/diff_wdc_identify.c (killdrivercrash witness).

It is NOT the detector and runs NO emulator code.  It prints the detector's OUTPUT SHAPE as HEAD's
diff_wdc_identify.c does -- `  ok   <row>` / `  FAIL <row>` lines, then "\\n<N> rows, <F> failures" and
the completion sentinel WDC_IDENTIFY_PASS or WDC_IDENTIFY_FAIL as the LAST line -- so a kill driver's
SCORER can be fed a run whose ending is chosen on purpose:

  base         5 rows ok, trailer, WDC_IDENTIFY_PASS              (a green baseline)
  Mk_kill      rows b,c FAIL, trailer, WDC_IDENTIFY_FAIL, exit 1  (a GENUINE kill: 2 red)
  Ms_survive   identical to base                                   (a GENUINE survivor)
  Mc_early     SIGFPE before any FAIL row; stdout is a file, so the buffered rows are LOST
  Mc_late      row b FAIL (flushed), then SIGFPE: no trailer, no sentinel
  Mx_exit1     row b FAIL, then fatal + exit(1) -- the "host kill" shape: stdio IS flushed by exit()
  Mcf_nocompile  a syntax error: the build fails, nothing runs
"""
import sys

MODES = ("base", "Mk_kill", "Ms_survive", "Mc_early", "Mc_late", "Mx_exit1", "Mcf_nocompile")

BODY = r'''
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
static int rows, failures;
static void row(const char *name, int ok, int flush)
{
	rows++;
	if (ok)
		printf("  ok   %-38s\n", name);
	else {
		failures++;
		printf("  FAIL %-38s stub row for the killdrivercrash witness\n", name);
	}
	if (flush)
		fflush(stdout);
}
static void crash(void)
{
	/*  raise(), not `1 / zero': gcc rewrites 1/x as a compare and never traps (measured on
	    the first run of this witness: the "crash" stubs ran to their sentinel).  */
	raise(SIGFPE);
}
int main(void)
{
	int fl = (MODE == 4 || MODE == 5);   /* Mc_late / Mx_exit1 flush their rows */
	printf("diff_wdc_identify STUB mode=%s (no emulator code)\n", MODENAME);
	row("stub row a", 1, fl);
	if (MODE == 3) crash();                               /* Mc_early */
	row("stub row b", !(MODE == 1 || MODE == 4 || MODE == 5), fl);
	if (MODE == 4) crash();                               /* Mc_late */
	if (MODE == 5) { fprintf(stderr, "fatal: stub host kill\n"); exit(1); }   /* Mx_exit1 */
	row("stub row c", !(MODE == 1), fl);
	row("stub row d", 1, fl);
	row("stub row e", 1, fl);
	printf("\n%d rows, %d failures\n", rows, failures);
	printf(failures ? "WDC_IDENTIFY_FAIL\n" : "WDC_IDENTIFY_PASS\n");
	return failures != 0;
}
'''


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in MODES:
        sys.exit("usage: mkstub_wdc.py {%s}" % "|".join(MODES))
    m = sys.argv[1]
    num = {"base": 0, "Mk_kill": 1, "Ms_survive": 0, "Mc_early": 3, "Mc_late": 4, "Mx_exit1": 5,
           "Mcf_nocompile": 0}[m]
    src = "#define MODE %d\n#define MODENAME \"%s\"\n" % (num, m) + BODY
    if m == "Mcf_nocompile":
        src += "\nthis line is not C;\n"
    sys.stdout.write(src)


if __name__ == "__main__":
    main()
