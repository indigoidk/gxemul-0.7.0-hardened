# fable5 adj B: the FULL argument-shape closure on top of pinned_sample -- (a) an in-domain low-precedence SWEEP
# sample `1 ? 33 : 0' (a value-asserting typedef through ADDR, both legs), (b) two TX raises in TVAL through TRIGGER
# (`1 ? 33 : 0' and `32 | 1', address and payload checked at e = 33).  Four cells: RANGE_OK's two `(e)' sites
# (the refusal sample) and ADDR's / BITMASK's `(e)' sites (the value sample and the TX raises).
import io, os, shutil, sys
BS = chr(92)
Q = chr(39)
W = sys.argv[1]
SRC = os.path.join(W, "variants", "pinned_sample")
OUT = os.path.join(W, "variants", "pinned_shape")
cases = io.open(os.path.join(SRC, "sysasic_range_cases.c"), encoding="utf-8", newline="").read()
drv = io.open(os.path.join(SRC, "sysasic_range_check.py"), encoding="utf-8", newline="").read()


def rep(t, old, new, n=1):
    assert t.count(old) == n, (old[:70], t.count(old))
    return t.replace(old, new)


# (a) the in-domain sample, beside the refusal sample
drv = rep(drv, '                 ("1 ? 200 : 5", 200)]\n',
          '                 ("1 ? 200 : 5", 200),\n'
          '                 #  and an IN-DOMAIN one: ADDR' + Q + 's `4*((e)>>5)' + Q + ' without its operand parentheses gives\n'
          '                 #  4*33 for this (SWEEP' + Q + 's typedef asserts the value on both legs; TVAL' + Q + 's TX raises\n'
          '                 #  carry it through TRIGGER, where BITMASK' + Q + 's `(e) & 31' + Q + ' is pinned).\n'
          '                 ("1 ? 33 : 0", 33)]\n')
# (b) the TX raises: driver side
drv = rep(drv, 'TT_LINE = re.compile(r"^TT (?P<tag>' + BS + 'w+) e=(?P<e>-?' + BS + 'd+) " + REC)\n',
          'TT_LINE = re.compile(r"^TT (?P<tag>' + BS + 'w+) e=(?P<e>-?' + BS + 'd+) " + REC)\n'
          'TX_LINE = re.compile(r"^TX (?P<tag>' + BS + 'w+) e=(?P<e>-?' + BS + 'd+) " + REC)\n'
          '#  ARGUMENT SHAPE through TRIGGER: in-domain values spelled as low-precedence expressions (the tag names the\n'
          '#  spelling; the value is 33 -- word 1, bit 1 -- so a lost parenthesis at ADDR' + Q + 's or BITMASK' + Q + 's operand moves\n'
          '#  the address (4*33) or the payload bit (1 << 33)).\n'
          'TX_WANT = [("cond33", 33), ("or33", 33)]\n')
drv = rep(drv, '    seen, typed, bad = {}, {}, []\n', '    seen, typed, shaped, bad = {}, {}, {}, []\n')
drv = rep(drv, '        m = TV_LINE.match(ln)\n        tag = None\n        if not m:\n            m = TT_LINE.match(ln)\n            if not m:\n                continue\n            tag = m.group("tag")\n',
          '        m = TV_LINE.match(ln)\n        tag, shape = None, False\n        if not m:\n            m = TT_LINE.match(ln)\n'
          '            if not m:\n                m = TX_LINE.match(ln)\n                shape = True\n            if not m:\n                continue\n            tag = m.group("tag")\n')
drv = rep(drv, '        if tag is None:\n            seen[e] = seen.get(e, 0) + 1\n        else:\n            typed[(tag, e)] = typed.get((tag, e), 0) + 1\n',
          '        if tag is None:\n            seen[e] = seen.get(e, 0) + 1\n        elif shape:\n            shaped[(tag, e)] = shaped.get((tag, e), 0) + 1\n'
          '        else:\n            typed[(tag, e)] = typed.get((tag, e), 0) + 1\n')
drv = rep(drv, '    if sorted(typed) != TT_WANT or any(v != 1 for v in typed.values()):\n        return False, "%d typed raises, want 0 and 95 once in each of the eight classes" % sum(typed.values())\n',
          '    if sorted(typed) != TT_WANT or any(v != 1 for v in typed.values()):\n        return False, "%d typed raises, want 0 and 95 once in each of the eight classes" % sum(typed.values())\n'
          '    if sorted(shaped) != TX_WANT or any(v != 1 for v in shaped.values()):\n        return False, "%d argument-shape raises, want each of %s once" % (sum(shaped.values()), TX_WANT)\n')
drv = rep(drv, '        return False, "%d of 112 raises WRONG: %s" % (len(bad), "; ".join(bad[:3]))\n    return True, ("96 of 96 int raises and 16 of 16 typed edge raises: address and device-visible "\n                  "payload exact; every argument pin held")\n',
          '        return False, "%d of 114 raises WRONG: %s" % (len(bad), "; ".join(bad[:3]))\n    return True, ("96 of 96 int raises, 16 of 16 typed edge raises and 2 of 2 argument-shape raises: address "\n                  "and device-visible payload exact; every argument pin held")\n')
# (b) the TX raises: cases side
cases = rep(cases, '#define\tTT2(tag, t)\tTT(tag, t, 0); TT(tag, t, 95)\n',
            '#define\tTT2(tag, t)\tTT(tag, t, 0); TT(tag, t, 95)\n'
            '/*  ARGUMENT SHAPE: an in-domain value spelled as a low-precedence expression, through TRIGGER.  The body\n'
            '    sites ADDR `4*((e)>>5)' + Q + ' and BITMASK `((e) & 31)' + Q + ' lose their operand parentheses silently (product-\n'
            '    identical: every product raise passes a define); the address (4*33) and the payload bit (1 << 33)\n'
            '    are what differ.  The out-of-domain twin `1 ? 200 : 5' + Q + ' is a SWEEP/TSWEEP sample (RANGE_OK' + Q + 's sites).  */\n'
            '#define\tTX(tag, expr, v)\tdo {\t\t\t\t\t\t' + BS + '\n'
            '\t\trec_reset();\t\t\t\t\t\t\t' + BS + '\n'
            '\t\tSYSASIC_TRIGGER_EVENT(expr);\t\t\t\t\t' + BS + '\n'
            '\t\tprintf("TX " #tag " e=%d " REC_FMT, (int)(v), REC_ARGS);\t' + BS + '\n'
            '\t} while (0)\n')
cases = rep(cases, '\tTT2(u64, unsigned long long);\n\tprintf("TVAL_DONE' + BS + 'n");\n',
            '\tTT2(u64, unsigned long long);\n\tTX(cond33, 1 ? 33 : 0, 33);\n\tTX(or33, 32 | 1, 33);\n\tprintf("TVAL_DONE' + BS + 'n");\n')
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
io.open(os.path.join(OUT, "sysasic_range_check.py"), "w", encoding="utf-8", newline="").write(drv)
io.open(os.path.join(OUT, "sysasic_range_cases.c"), "w", encoding="utf-8", newline="").write(cases)
print("variant pinned_shape written")
