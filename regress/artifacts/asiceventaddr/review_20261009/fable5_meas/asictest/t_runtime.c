#include "dreamcast_sysasicvar.h"
int main(int argc, char **argv) { int e = argc; (void)argv; int a = SYSASIC_EVENT_TO_ADDR(e); return a; }
