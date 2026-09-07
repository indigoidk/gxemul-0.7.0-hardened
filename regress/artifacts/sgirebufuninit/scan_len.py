import re, glob, os
#  The sgirebufuninit signature: a stack buffer passed to memory_rw with a length that is
#  NOT sizeof(buf) and not a literal -- i.e. a length the GUEST may influence, where the
#  fill and the transfer can disagree.
call = re.compile(r'memory_rw\s*\((.*?)\)\s*;', re.S)
hits = []
for f in sorted(glob.glob('*.c')):
    src = open(f, encoding='utf-8', errors='replace').read()
    # stack byte buffers declared in this file
    bufs = set(re.findall(r'\b(?:unsigned char|uint8_t)\s+(\w+)\s*\[\s*\d+\s*\]\s*;', src))
    if not bufs:
        continue
    for m in call.finditer(src):
        args = [a.strip() for a in m.group(1).split(',')]
        if len(args) < 6:
            continue
        databuf, ln = args[3], args[4]
        nm = re.sub(r'^&', '', databuf).split('[')[0]
        if nm not in bufs:
            continue
        if ln.startswith('sizeof') or re.fullmatch(r'(0x)?[0-9]+', ln):
            continue          # transfer length pinned to the buffer -> not this class
        line = src[:m.start()].count('\n') + 1
        hits.append((f, line, nm, ln, args[5]))
print("%-26s %6s %-12s %-16s %s" % ("file", "line", "buffer", "length", "dir"))
for h in hits:
    print("%-26s %6d %-12s %-16s %s" % h)
print("\n%d call sites where the transfer length is NOT pinned to the buffer" % len(hits))
