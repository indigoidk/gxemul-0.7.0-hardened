# fable5 adj B: a run program that raises an IN-DOMAIN value spelled as low-precedence expressions through the
# frozen recording stub (the cases file's own preamble and stub blocks, extracted by their text).
import io, os, sys
W = sys.argv[1]
cases = io.open(os.path.join(W, "frozen", "sysasic_range_cases.c"), encoding="utf-8", newline="").read().split("\n")
pre_a = cases.index('#include <stdint.h>')
pre_b = cases.index('void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data);')
stub_a = cases.index('#include <stdio.h>')
stub_b = [i for i, l in enumerate(cases) if l.startswith('\t\tser_cpu_ok ? "ok" : "BAD", ser_len')][0]
tu = cases[pre_a:pre_b + 1] + ['#include "thirdparty/dreamcast_sysasicvar.h"'] + cases[stub_a:stub_b + 1] + [
    'int main(void)', '{', '\tstruct cpu c;', '\tstruct cpu *cpu = &c;', '\trec_install(&c);',
    '\trec_reset();', '\tSYSASIC_TRIGGER_EVENT(1 ? 33 : 0);', '\tprintf("TV[1 ? 33 : 0] e=%d " REC_FMT, 33, REC_ARGS);',
    '\trec_reset();', '\tSYSASIC_TRIGGER_EVENT(0 ? 0 : 33);', '\tprintf("TV[0 ? 0 : 33] e=%d " REC_FMT, 33, REC_ARGS);',
    '\trec_reset();', '\tSYSASIC_TRIGGER_EVENT(32 | 1);', '\tprintf("TV[32 | 1] e=%d " REC_FMT, 33, REC_ARGS);',
    '\treturn 0;', '}', '']
io.open(os.path.join(W, "latent", "indomain.c"), "w", encoding="utf-8", newline="").write("\n".join(tu))
print("  indomain.c written: %d lines" % len(tu))
