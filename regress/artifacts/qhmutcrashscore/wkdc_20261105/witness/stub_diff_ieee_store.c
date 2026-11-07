/*
 *  STUB stand-in for regress/diff_ieee_store.c -- killdrivercrash harness witness, gate 3.
 *  It is NOT the differential and tests NOTHING in float_emul.c (which is linked in, unused).
 *  It prints the differential's verdict tokens -- "DIFF_PASS ..." or "DIFF_FAIL" as the last
 *  line, exactly as HEAD's diff_ieee_store.c does -- and chooses each run's ENDING by the binary's
 *  own name, which selftest_mutation.sh sets to "real" or "mut_<name>".
 *
 *  STUBSET=mixed (default):
 *      real              DIFF_PASS                       the control arm
 *      mut_revert287     a FAIL row, DIFF_FAIL           a GENUINE kill
 *      mut_flushband     a FAIL row, DIFF_FAIL           a GENUINE kill
 *      mut_tiesaway      DIFF_PASS                       a GENUINE survivor (gate 3 must go red)
 *      mut_modeignored   raise(SIGFPE) before any output (buffered output lost)
 *      mut_wlegacyrounds a FAIL row (flushed), then raise(SIGFPE): no verdict token
 *      mut_revert303     a FAIL row, fatal + exit(1): no verdict token (the "host kill" shape)
 *      mut_maskcarry     prints NOTHING and returns 0
 *  STUBSET=allkill: every mut_* is a genuine kill (a FAIL row, DIFF_FAIL); real passes.
 *  STUBSET=allcrash: every mut_* raises SIGFPE before printing anything; real passes.
 */
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*  float_emul.c references fatal(); the real differential supplies it the same way.  */
void fatal(const char *fmt, ...)
{
	(void) fmt;
}

int main(int argc, char **argv)
{
	const char *b = strrchr(argv[0], '/');
	const char *set = getenv("STUBSET");
	b = b ? b + 1 : argv[0];
	(void) argc;
	if (set != NULL && strcmp(set, "allkill") == 0 && strncmp(b, "mut_", 4) == 0) {
		printf("  FAIL stub row\nDIFF_FAIL\n");
		return 0;
	}
	if (set != NULL && strcmp(set, "allcrash") == 0 && strncmp(b, "mut_", 4) == 0)
		raise(SIGFPE);
	if (strcmp(b, "real") == 0) {
		printf("  ok   stub row\nDIFF_PASS -- stub\n");
		return 0;
	}
	if (strcmp(b, "mut_revert287") == 0 || strcmp(b, "mut_flushband") == 0) {
		printf("  FAIL stub row\nDIFF_FAIL\n");
		return 0;
	}
	if (strcmp(b, "mut_tiesaway") == 0) {
		printf("  ok   stub row\nDIFF_PASS -- stub survivor\n");
		return 0;
	}
	if (strcmp(b, "mut_modeignored") == 0) {
		printf("  ok   stub row (buffered, lost)\n");
		raise(SIGFPE);
	}
	if (strcmp(b, "mut_wlegacyrounds") == 0) {
		printf("  FAIL stub row\n");
		fflush(stdout);
		raise(SIGFPE);
	}
	if (strcmp(b, "mut_revert303") == 0) {
		printf("  FAIL stub row\n");
		fprintf(stderr, "fatal: stub host kill\n");
		exit(1);
	}
	if (strcmp(b, "mut_maskcarry") == 0)
		return 0;
	printf("stub: unknown binary name %s\n", b);
	return 2;
}
