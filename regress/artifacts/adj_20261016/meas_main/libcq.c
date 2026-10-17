#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
int main(void) {
	void *p0 = malloc(0);
	printf("malloc(0) -> %s\n", p0 ? "non-NULL" : "NULL");
	void *p = malloc(16);
	errno = 0;
	void *r = realloc(p, 0);
	printf("realloc(p,0) -> %s (errno=%d)\n", r ? "non-NULL" : "NULL", errno);
	FILE *f = tmpfile();
	fputs("hello", f);
	errno = 0;
	int rc = fseek(f, (long)-8, SEEK_SET);
	printf("fseek(f,-8,SEEK_SET) -> %d errno=%d (%s), ftell=%ld\n", rc, errno, strerror(errno), ftell(f));
	errno = 0;
	rc = fseeko(f, (off_t)-1, SEEK_SET);
	printf("fseeko(f,(off_t)-1,SEEK_SET) -> %d errno=%d (%s)\n", rc, errno, strerror(errno));
	printf("sizeof(long)=%zu sizeof(off_t)=%zu\n", sizeof(long), sizeof(off_t));
	printf("LIBCQ_DONE\n");
	return 0;
}
