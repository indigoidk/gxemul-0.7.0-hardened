/*  opus5 measurement, DOMAIN leg: one argument per compile, -DCASE=n.
    Expect a hard error exactly when the value is outside [0,95].  */
#include "thirdparty/dreamcast_sysasicvar.h"

#if   CASE == 1
#define	EV	0
#elif CASE == 2
#define	EV	95
#elif CASE == 3
#define	EV	96
#elif CASE == 4
#define	EV	127
#elif CASE == 5
#define	EV	128
#elif CASE == 6
#define	EV	159
#elif CASE == 7
#define	EV	479
#elif CASE == 8
#define	EV	2048
#elif CASE == 9
#define	EV	6144
#elif CASE == 10
#define	EV	(-1)
#elif CASE == 11
#define	EV	(-32)
#elif CASE == 12
#define	EV	(-2147483647 - 1)
#elif CASE == 13
#define	EV	2147483647
#elif CASE == 14
#define	EV	96u
#elif CASE == 15
#define	EV	4294967295u
#elif CASE == 16
#define	EV	0x100000000LL
#elif CASE == 17
#define	EV	((unsigned char)200)
#elif CASE == 18
#define	EV	'A'
#elif CASE == 19
#define	EV	(0, 50)
#elif CASE == 20
#define	EV	(0, 100)
#elif CASE == 21
#define	EV	31
#elif CASE == 22
#define	EV	63
#elif CASE == 23
#define	EV	-1
#elif CASE == 24
#define	EV	0x5f
#endif

long f(void) { return (long)SYSASIC_EVENT_TO_ADDR(EV); }
