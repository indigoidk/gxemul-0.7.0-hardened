import re, glob
#  LIMIT 3 of the length scanner: a site passing sizeof(buf) is excluded by construction, yet a
#  sizeof(buf) transfer of a PARTIALLY FILLED buffer is the same defect.  This closes that
#  direction: every memory_rw that WRITES a stack byte-buffer into guest-visible memory, with
#  whether the enclosing function ever initialises that buffer wholesale.
call = re.compile(r'memory_rw\s*\((.*?)\)\s*;', re.S)
fn   = re.compile(r'^[A-Za-z_][\w \t\*]*\b(\w+)\s*\([^;]*\)\s*\{', re.M)
rows = []
for f in sorted(glob.glob('*.c')):
    src = open(f, encoding='utf-8', errors='replace').read()
    decls = dict(re.findall(r'\b(?:unsigned char|uint8_t)\s+(\w+)\s*\[\s*(\d+)\s*\]\s*;', src))
    if not decls: continue
    fns = [(m.start(), m.group(1)) for m in fn.finditer(src)]
    for m in call.finditer(src):
        args = [a.strip() for a in m.group(1).split(',')]
        if len(args) < 6: continue
        nm = re.sub(r'^&', '', args[3]).split('[')[0]
        if nm not in decls: continue
        if 'MEM_WRITE' not in args[5]: continue      # writes INTO guest-visible memory
        owner = 'file-scope'
        for pos, name in fns:
            if pos < m.start(): owner = name
        # does anything initialise the whole buffer?
        init = bool(re.search(r'memset\s*\(\s*&?' + nm + r'\b', src)) or \
               bool(re.search(r'\b(?:unsigned char|uint8_t)\s+' + nm + r'\s*\[\s*\d+\s*\]\s*=', src))
        line = src[:m.start()].count('\n') + 1
        rows.append((f, line, owner, nm, decls[nm], args[4], "yes" if init else "NO"))
print("%-24s %5s %-26s %-10s %5s %-14s %s" % ("file","line","function","buffer","size","len","wholesale init?"))
for r in rows: print("%-24s %5d %-26s %-10s %5s %-14s %s" % r)
print("\n%d MEM_WRITE sites from a stack byte-buffer; %d with NO wholesale initialisation"
      % (len(rows), sum(1 for r in rows if r[6] == "NO")))
