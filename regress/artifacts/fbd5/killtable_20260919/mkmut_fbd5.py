# fbdeclinefive (#545) kill table -- the PRODUCT mutants, each ONE edit on the FIXED dev_footbridge.c (PRETABLE M1-M11).
#   python mkmut_fbd5.py <tree-root> <mutant>     (mutant = base | M1 ... M11)
# `base` re-applies nothing (the caller restores from the fixed copy).  Every edit must match EXACTLY ONCE.
import io, sys, os
root, mut = sys.argv[1], sys.argv[2]
p = os.path.join(root, 'src', 'devices', 'dev_footbridge.c')
s = io.open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
def rep(old, new):
    global s
    o, n = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(o) == 1, (mut, o[:70], s.count(o))
    s = s.replace(o, n)

if mut == 'base':
    pass
elif mut == 'M1':      # keep the exit at the FIQ_RAW_STATUS write (clause b: verbatim reinstatement at one site)
    rep('''		else if (!d->warned_fiq_raw_w) {
			/*  #545: read-only (7.3.30); declined, announced once.  */
			d->warned_fiq_raw_w = 1;
			fatal("[ footbridge write to fiq_raw_status (once) ]\\n");
		}
''', '''		else {
			fatal("[ footbridge write to fiq_raw_status ]\\n");
			exit(1);
		}
''')
elif mut == 'M2':      # unlatched announce at IRQ_STATUS
    rep('''		else if (!d->warned_irq_status_w) {
			/*  #545: read-only register (7.3.29); the write is
			    declined -- no state changes -- and announced once.  */
			d->warned_irq_status_w = 1;
''', '''		else if (1) {
			/*  #545: read-only register (7.3.29); the write is
			    declined -- no state changes -- and announced once.  */
			d->warned_irq_status_w = 1;
''')
elif mut == 'M3':      # IRQ_STATUS and IRQ_RAW_STATUS share one latch
    rep('''		else if (!d->warned_irq_raw_w) {
			/*  #545: read-only (7.3.30); declined, announced once.  */
			d->warned_irq_raw_w = 1;
''', '''		else if (!d->warned_irq_status_w) {
			/*  #545: read-only (7.3.30); declined, announced once.  */
			d->warned_irq_status_w = 1;
''')
elif mut == 'M4':      # copy-paste: FIQ_RAW_STATUS tests/sets the FIQ_STATUS latch
    rep('''		else if (!d->warned_fiq_raw_w) {
			/*  #545: read-only (7.3.30); declined, announced once.  */
			d->warned_fiq_raw_w = 1;
''', '''		else if (!d->warned_fiq_status_w) {
			/*  #545: read-only (7.3.30); declined, announced once.  */
			d->warned_fiq_status_w = 1;
''')
elif mut == 'M5':      # the 18c read keeps leaking irq_enable
    rep('''		} else if (!d->warned_irq_clear_r) {
			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
''', '''		} else if ((odata = d->irq_enable), !d->warned_irq_clear_r) {
			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
''')
elif mut == 'M6':      # the IRQ_STATUS decline stores into irq_status
    rep('''			d->warned_irq_status_w = 1;
			fatal("[ WARNING: footbridge write to irq status? "
			    "(once) ]\\n");
		}
''', '''			d->warned_irq_status_w = 1;
			fatal("[ WARNING: footbridge write to irq status? "
			    "(once) ]\\n");
		}
		if (writeflag == MEM_WRITE)
			d->irq_status = idata;
''')
elif mut == 'M7':      # the LEGAL IRQ_STATUS read narrowed to a constant 0 (Q2 f)
    rep('''	case IRQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status & d->irq_enable;
''', '''	case IRQ_STATUS:
		if (writeflag == MEM_READ)
			odata = 0;
''')
elif mut == 'M8':      # FIQ_STATUS read drops the &
    rep('''	case FIQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status & d->fiq_enable;
''', '''	case FIQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status;
''')
elif mut == 'M9':      # misnamed register in the IRQ_RAW_STATUS announce
    rep('''			fatal("[ footbridge write to irq_raw_status (once) ]\\n");
''', '''			fatal("[ WARNING: footbridge write to irq status? (once) ]\\n");
''')
elif mut == 'M10':     # the 18c read clears its own latch after announcing (announces every time)
    rep('''			d->warned_irq_clear_r = 1;
			fatal("[ WARNING: footbridge read from "
			    "ENABLE CLEAR? (once) ]\\n");
		}
''', '''			d->warned_irq_clear_r = 1;
			fatal("[ WARNING: footbridge read from "
			    "ENABLE CLEAR? (once) ]\\n");
			d->warned_irq_clear_r = 0;
		}
''')
elif mut == 'M11':     # decline only word accesses at IRQ_STATUS (a len guard on the decline)
    rep('''		else if (!d->warned_irq_status_w) {
			/*  #545: read-only register (7.3.29); the write is
''', '''		else if (len == 4 && !d->warned_irq_status_w) {
			/*  #545: read-only register (7.3.29); the write is
''')
else:
    raise SystemExit("unknown mutant " + mut)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print("MUTANT", mut, "applied to", p)
