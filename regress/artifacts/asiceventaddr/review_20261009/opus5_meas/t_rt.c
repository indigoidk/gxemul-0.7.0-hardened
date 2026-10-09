/*  opus5 measurement, CONSTANCY leg: does a non-constant e hard-error, and do
    the constant forms a future event-adder might use (const object, enum,
    C23 constexpr) get checked correctly?  -DCASE=n.  */
#include "thirdparty/dreamcast_sysasicvar.h"

#if   CASE == 1
/*  a runtime event number  */
long f(int e) { return (long)SYSASIC_EVENT_TO_ADDR(e); }
#elif CASE == 2
static const int ce = 5;
long f(void) { return (long)SYSASIC_EVENT_TO_ADDR(ce); }
#elif CASE == 3
static const int ce = 100;
long f(void) { return (long)SYSASIC_EVENT_TO_ADDR(ce); }
#elif CASE == 4
enum { EV_OK = 50 };
long f(void) { return (long)SYSASIC_EVENT_TO_ADDR(EV_OK); }
#elif CASE == 5
enum { EV_BAD = 100 };
long f(void) { return (long)SYSASIC_EVENT_TO_ADDR(EV_BAD); }
#elif CASE == 6
/*  V2, the negative-size ARRAY form the header comment rejects, with a
    runtime e: the comment says it silently degrades to a VLA.  Built here
    locally; it is NOT in the tree.  */
#define	V2_OK(e)	((int)sizeof(char[((e) >= 0 && (e) < 96) ? 1 : -1]) * 0)
long f(int e) { return (long)(0x5f6900 + 4*((e)>>5) + V2_OK(e)); }
#elif CASE == 7
/*  C23 constexpr object -- the build's default dialect is gnu23  */
constexpr int ce = 5;
long f(void) { return (long)SYSASIC_EVENT_TO_ADDR(ce); }
#elif CASE == 8
constexpr int ce = 100;
long f(void) { return (long)SYSASIC_EVENT_TO_ADDR(ce); }
#elif CASE == 9
/*  a side-effecting argument  */
int g;
long f(void) { return (long)SYSASIC_EVENT_TO_ADDR(g++); }
#endif
