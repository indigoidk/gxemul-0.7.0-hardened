# fable5 adj B: driver/stub variants.  orig = frozen deliverables.  pinned = PIN's pins A (size_t width, %llu), B
# (-fsanitize=address inside run_row) and C (writeflag recorded, compared to memory.h's MEM_WRITE).  pinned_sample =
# pinned + the SWEEP/TSWEEP sample `1 ? 200 : 5' (F4's row in sample form).  pinned_preflight = pinned_sample + an
# AddressSanitizer preflight that VOIDs the run when ASAN cannot link or run.  sizeof_both = opus5's measured `both'
# stub (sizeof extent capture + long long length) on the frozen driver, for the D1 comparison.  pinned_mw2 = pinned
# with the STUB's own MEM_WRITE drifted to 2 (pin C's negative control).
import io, os, shutil, sys
BS = chr(92)
Q = chr(39)
W = sys.argv[1]
SRC = os.path.join(W, "frozen")
OUT = os.path.join(W, "variants")
cases = io.open(os.path.join(SRC, "sysasic_range_cases.c"), encoding="utf-8", newline="").read()
drv = io.open(os.path.join(SRC, "sysasic_range_check.py"), encoding="utf-8", newline="").read()


def rep(t, old, new, n=1):
    assert t.count(old) == n, (old[:60], t.count(old))
    return t.replace(old, new)


# ---- pin A + pin C in the cases file
OLD_DECL = "static int\t\trw_calls, rw_writes, rw_cpu_ok, rw_mem_ok, rw_buf_ok, rw_flags, rw_len;\n"
NEW_DECL = ("static int\t\trw_calls, rw_writes, rw_cpu_ok, rw_mem_ok, rw_buf_ok, rw_flags, rw_wflag;\n"
            "static unsigned long long\trw_len;\t/*  PIN A: memory_rw's size_t length, recorded at full width  */\n")
OLD_RESET = "\trw_flags = rw_len = -1;\n"
NEW_RESET = "\trw_flags = rw_wflag = -1;\n\trw_len = ~0ULL;\n"
OLD_SET = "\trw_len = (int)len;\n"
NEW_SET = "\trw_len = (unsigned long long)len;\n"
OLD_FLAGS = "\trw_flags = cache_flags;\n"
NEW_FLAGS = "\trw_flags = cache_flags;\n\trw_wflag = writeflag;\t/*  PIN C: the int the function received  */\n"
OLD_FMT = '"flags=%d len=%d ser=%d scpu=%s slen=%d' + BS + 'n"'
NEW_FMT = '"flags=%d wflag=%d len=%llu ser=%d scpu=%s slen=%d' + BS + 'n"'
OLD_ARGS = 'rw_buf_ok ? "ok" : "BAD", rw_flags, rw_len, ser_calls,'
NEW_ARGS = 'rw_buf_ok ? "ok" : "BAD", rw_flags, rw_wflag, rw_len, ser_calls,'
pc = cases
for o, n in ((OLD_DECL, NEW_DECL), (OLD_RESET, NEW_RESET), (OLD_SET, NEW_SET), (OLD_FLAGS, NEW_FLAGS),
             (OLD_FMT, NEW_FMT), (OLD_ARGS, NEW_ARGS)):
    pc = rep(pc, o, n)

# ---- pin B + pin C in the driver
pd = drv
pd = rep(pd, 'r" flags=(?P<flags>-?' + BS + 'd+) len=(?P<len>-?' + BS + 'd+) ser=',
         'r" flags=(?P<flags>-?' + BS + 'd+) wflag=(?P<wflag>-?' + BS + 'd+) len=(?P<len>-?' + BS + 'd+) ser=')
pd = rep(pd, 'PHYSICAL_VAL = dict(PRODUCT_DEFINES)["PHYSICAL"]\n',
         'PHYSICAL_VAL = dict(PRODUCT_DEFINES)["PHYSICAL"]\nMEM_WRITE_VAL = dict(PRODUCT_DEFINES)["MEM_WRITE"]\n')
pd = rep(pd, '    if int(m.group("len")) != 8:\n        bad.append("len=%s" % m.group("len"))\n',
         '    if int(m.group("wflag")) != MEM_WRITE_VAL:\n'
         '        bad.append("wflag=%s (MEM_WRITE is %d)" % (m.group("wflag"), MEM_WRITE_VAL))\n'
         '    if int(m.group("len")) != 8:\n        bad.append("len=%s" % m.group("len"))\n')
ASAN = '"-fsanitize=address"'
pd = rep(pd, '            rc, out, err = run(cc + flags + DIAG + ["-I" + hdrdir,\n'
             '                               "-DSYSASIC_CASE=%d" % n, "-o", exe, cases], work)\n',
         '            #  PIN B: the run rows under AddressSanitizer -- the 8-byte object extent\n'
         '            rc, out, err = run(cc + flags + [' + ASAN + '] + DIAG + ["-I" + hdrdir,\n'
         '                               "-DSYSASIC_CASE=%d" % n, "-o", exe, cases], work)\n')

# ---- the sample form of F4's row
ps = rep(pd, '                 ("((unsigned char)96)", 96)]\n',
         '                 ("((unsigned char)96)", 96),\n'
         '                 #  ARGUMENT SHAPE: an out-of-domain value spelled as a low-precedence expression.  `(e)' + Q + '\n'
         '                 #  -> `e' + Q + ' at either RANGE_OK site accepts it (measured: s11_latent) while the committed\n'
         '                 #  header refuses it; ?: binds looser than && and <.\n'
         '                 ("1 ? 200 : 5", 200)]\n')

# ---- the ASAN preflight (VOID, not a row FAIL, when the toolchain cannot link or run ASAN)
PRE = ('        if not gcc:\n'
       '            voids.append("the compiler is not gcc -- the oracle strings are gcc' + Q + 's, and "\n'
       '                         "nothing else has been measured")\n'
       '            return finish()\n')
PRE_NEW = PRE + (
       '        #  PIN B PREFLIGHT: the run rows need an AddressSanitizer that LINKS and RUNS here.  A toolchain\n'
       '        #  without libasan, or a host where an instrumented binary cannot start, cannot measure the extent\n'
       '        #  pin: VOID, with the reason -- never a red ID/TVAL that reads as a header defect.\n'
       '        pf_src = os.path.join(work, "sysasic_asan_preflight.c")\n'
       '        write(pf_src, "int main(void) { return 0; }' + BS + 'n")\n'
       '        pf_exe = os.path.join(work, "sysasic_asan_preflight")\n'
       '        rc, out, err = run(cc + prod + [' + ASAN + ', "-o", pf_exe, pf_src], work)\n'
       '        if rc == 0:\n'
       '            rc, out, err = run([pf_exe], work, timeout=60)\n'
       '            why = "an -fsanitize=address binary does not run here: exit %d: %s" % (\n'
       '                rc, (err.strip().splitlines() or ["(no output)"])[0])\n'
       '        else:\n'
       '            why = "cannot compile and link with -fsanitize=address: " + first_errors(err)\n'
       '        print("sysasic_range_check: asan    %s" % ("preflight ok (links and runs)" if rc == 0 else why))\n'
       '        if rc != 0:\n'
       '            voids.append("the extent pin needs AddressSanitizer on the run rows and this toolchain "\n'
       '                         "cannot provide it (%s)" % why)\n'
       '            return finish()\n')
pp = rep(ps, PRE, PRE_NEW)

# ---- opus5's `both' stub form (sizeof extent capture + long long length) for the D1 comparison
ANCHOR_INSTALL = ("static void rec_install(struct cpu *c)\n{\n\twant_cpu = c;\n\twant_mem = (struct memory *)&sysasic_memobj;"
                  "\t/*  a DISTINCT object, never c  */\n\tc->mem = want_mem;\n\tc->memory_rw = id_rw;\n}\n")
EXTENT = ANCHOR_INSTALL + (
    "\n/*  PIN VARIANT extent: the buffer's DECLARED extent, captured at TRIGGER's own serializer call  */\n"
    "#define\tmemory_writemax64(c, b, l, d)\t((memory_writemax64)((c), (b), (l), (d)),\t" + BS + "\n"
    "\t(sizeof(b) < (size_t)(int)(l) ? (void)(ser_len = -(int)sizeof(b)) : (void)0))\n")
sb = rep(cases, ANCHOR_INSTALL, EXTENT)
sb = rep(sb, OLD_DECL, "static int\t\trw_calls, rw_writes, rw_cpu_ok, rw_mem_ok, rw_buf_ok, rw_flags;\nstatic long long\trw_len;\n")
sb = rep(sb, OLD_SET, "\trw_len = (long long)len;\n")
sb = rep(sb, OLD_FMT, '"flags=%d len=%lld ser=%d scpu=%s slen=%d' + BS + 'n"')

# ---- pin C's negative control: the STUB's own MEM_WRITE drifted to 2
pm = rep(pc, "#define\tMEM_WRITE\t1\n", "#define\tMEM_WRITE\t2\n")


def variant(name, d, c):
    out = os.path.join(OUT, name)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    io.open(os.path.join(out, "sysasic_range_check.py"), "w", encoding="utf-8", newline="").write(d)
    io.open(os.path.join(out, "sysasic_range_cases.c"), "w", encoding="utf-8", newline="").write(c)
    print("variant %s written" % name)


variant("orig", drv, cases)
variant("pinned", pd, pc)
variant("pinned_sample", ps, pc)
variant("pinned_preflight", pp, pc)
variant("sizeof_both", drv, sb)
variant("pinned_mw2", pd, pm)
