import io
p = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus/wit_main.c"
s = io.open(p, encoding="utf-8", newline="").read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (old[:80], s.count(old))
    s = s.replace(old, new)


rep("""static int irq_asserts, irq_deasserts;
static void noop_assert(struct interrupt *i) { (void) i; irq_asserts++; }
static void noop_deassert(struct interrupt *i) { (void) i; irq_deasserts++; }""",
"""/*  The CPU interrupt LINE LEVEL per instance is the guest-visible quantity; the call counts are what the
    harness rows count.  A redundant ASSERT on a high line (or DEASSERT on a low one) changes no level.  */
static int irq_asserts, irq_deasserts;
static void *irq_b, *irq_v;
static int lvl_b, lvl_v;
static void noop_assert(struct interrupt *i)
{ irq_asserts++; if ((void *) i == irq_b) lvl_b = 1; else if ((void *) i == irq_v) lvl_v = 1; }
static void noop_deassert(struct interrupt *i)
{ irq_deasserts++; if ((void *) i == irq_b) lvl_b = 0; else if ((void *) i == irq_v) lvl_v = 0; }""")
rep("""extern void base_line(void *, int, int), var_line(void *, int, int);""",
"""extern void base_line(void *, int, int), var_line(void *, int, int);
extern void *base_irqptr(void *), *var_irqptr(void *);""")
rep("""typedef struct { int rv; uint64_t val; int ann, as, ds; } obs_t;""",
"""typedef struct { int rv; uint64_t val; int ann, as, ds, lvl; } obs_t;""")
rep("""	r.ann = fatal_calls - f0; r.as = irq_asserts - a0; r.ds = irq_deasserts - d0;
	return r;""",
"""	r.ann = fatal_calls - f0; r.as = irq_asserts - a0; r.ds = irq_deasserts - d0;
	r.lvl = var ? lvl_v : lvl_b;
	return r;""")
rep("""/*  returns bit0 = some step differs guest-visibly, bit1 = some step differs in announces,
    bit2 = internal state differs at the end  */""",
"""/*  returns bit0 = some step differs GUEST-visibly (return, read buffer, CPU irq line LEVEL),
    bit1 = some step differs in announces, bit2 = internal state differs at the end,
    bit3 = some step differs only in irq CALL COUNTS (same level: a redundant call)  */""")
rep("""	base_set(b, ST[st].is, ST[st].ie, ST[st].fs, ST[st].fe);
	var_set(v, ST[st].is, ST[st].ie, ST[st].fs, ST[st].fe);
	for (i = 0; i < n; i++) {
		obs_t ob = apply(0, b, &AL[seq[i]]), ov = apply(1, v, &AL[seq[i]]);
		int g = ob.rv != ov.rv || ob.val != ov.val || ob.as != ov.as || ob.ds != ov.ds;
		int a = ob.ann != ov.ann;
		flags |= (g ? 1 : 0) | (a ? 2 : 0);
		if (verbose) {
			printf("      %-16s base: rv=%d val=%016" PRIx64 " ann=%d A=%d D=%d | var: rv=%d val=%016" PRIx64
			    " ann=%d A=%d D=%d%s\\n", opname(&AL[seq[i]], s), ob.rv, ob.val, ob.ann, ob.as, ob.ds,
			    ov.rv, ov.val, ov.ann, ov.as, ov.ds, g ? "   <-- GUEST-VISIBLE" : a ? "   <-- ANNOUNCE" : "");
		}
	}""",
"""	irq_b = base_irqptr(b); irq_v = var_irqptr(v);
	lvl_b = lvl_v = 0;
	base_set(b, ST[st].is, ST[st].ie, ST[st].fs, ST[st].fe);
	var_set(v, ST[st].is, ST[st].ie, ST[st].fs, ST[st].fe);
	for (i = 0; i < n; i++) {
		obs_t ob = apply(0, b, &AL[seq[i]]), ov = apply(1, v, &AL[seq[i]]);
		int g = ob.rv != ov.rv || ob.val != ov.val || ob.lvl != ov.lvl;
		int a = ob.ann != ov.ann;
		int c = !g && (ob.as != ov.as || ob.ds != ov.ds);
		flags |= (g ? 1 : 0) | (a ? 2 : 0) | (c ? 8 : 0);
		if (verbose) {
			printf("      %-16s base: rv=%d val=%016" PRIx64 " ann=%d A=%d D=%d line=%d | var: rv=%d val=%016" PRIx64
			    " ann=%d A=%d D=%d line=%d%s\\n", opname(&AL[seq[i]], s), ob.rv, ob.val, ob.ann, ob.as, ob.ds, ob.lvl,
			    ov.rv, ov.val, ov.ann, ov.as, ov.ds, ov.lvl, g ? "   <-- GUEST-VISIBLE" : a ? "   <-- ANNOUNCE"
			    : c ? "   <-- irq call count only" : "");
		}
	}""")
rep("""		int found[3] = { 0, 0, 0 }, fl[3] = { 0, 0, 0 }, fseq[3][8];
		long cnt[3] = { 0, 0, 0 }, total = 0;""",
"""		int found[4] = { 0, 0, 0, 0 }, fl[4] = { 0, 0, 0, 0 }, fseq[4][8];
		long cnt[4] = { 0, 0, 0, 0 }, total = 0;""")
rep("""				for (k = 0; k < 3; k++)
					if (f & (1 << k)) {""",
"""				for (k = 0; k < 4; k++)
					if (f & (1 << k)) {""")
rep("""		printf("START %-6s exhaustive len 1..%d: %ld sequences; diverging: guest-visible %ld, announce %ld, internal %ld\\n",
		    ST[st].nm, lmax, total, cnt[0], cnt[1], cnt[2]);
		if (found[0]) show("GUEST-VISIBLE divergence", fseq[0], fl[0], st);
		if (found[1]) show("ANNOUNCE divergence", fseq[1], fl[1], st);
		if (found[2] && !found[0] && !found[1]) show("INTERNAL-ONLY divergence", fseq[2], fl[2], st);""",
"""		printf("START %-6s exhaustive len 1..%d: %ld sequences; diverging: guest-visible %ld, announce %ld, internal %ld,"
		    " irq-call-count-only %ld\\n", ST[st].nm, lmax, total, cnt[0], cnt[1], cnt[2], cnt[3]);
		if (found[0]) show("GUEST-VISIBLE divergence", fseq[0], fl[0], st);
		if (found[1]) show("ANNOUNCE divergence", fseq[1], fl[1], st);
		if (found[3] && !found[0]) show("IRQ-CALL-COUNT-ONLY divergence", fseq[3], fl[3], st);
		if (found[2] && !found[0] && !found[1]) show("INTERNAL-ONLY divergence", fseq[2], fl[2], st);""")
rep("""		long r, cg = 0, ca = 0, ci = 0;""", """		long r, cg = 0, ca = 0, ci = 0, cc = 0;""")
rep("""			if (f & 4) ci++;""", """			if (f & 4) ci++;
			if (f & 8) cc++;""")
rep("""		printf("RANDOM reset len 4..6: %ld sequences; diverging: guest-visible %ld, announce %ld, internal %ld\\n",
		    nrand, cg, ca, ci);""",
"""		printf("RANDOM reset len 4..6: %ld sequences; diverging: guest-visible %ld, announce %ld, internal %ld,"
		    " irq-call-count-only %ld\\n", nrand, cg, ca, ci, cc);""")
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("patched")
