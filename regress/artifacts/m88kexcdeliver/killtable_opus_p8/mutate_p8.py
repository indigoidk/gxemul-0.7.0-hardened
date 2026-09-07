#!/usr/bin/env python3
"""Anchored mutator for #502 pass 8.  MUTANT-TEXT-NOT-FOUND is a FAIL (presence pin)."""
import re, sys
BS = chr(92)                    # the Bash -> heredoc -> Python path eats one level; never write it literally

path, kind = sys.argv[1], sys.argv[2]
src = open(path, encoding="latin1").read()

if kind == "census":
    anchor = "\tbool implemented = false;\n"
    if src.count(anchor) != 1:
        print("MUTATE_FAIL anchor count %d" % src.count(anchor)); sys.exit(9)
    ins = (anchor
           + '\tfatal("[ M88KCENSUS v=%d psr=0x%08x t=%d ]' + BS + 'n", vector,\n'
           + '\t    (int)cpu->cd.m88k.cr[M88K_CR_PSR], is_trap);\n')
    src = src.replace(anchor, ins)
else:
    cls, expr = kind, sys.argv[3]
    pat = re.compile(r'(\tcase M88K_EXCEPTION_%s:\n'
                     r'\t\tdebugmsg_cpu\(cpu, SUBSYS_EXCEPTION, "%s", VERBOSITY_INFO, ""\);\n)'
                     r'\t\timplemented = true;\t/\*  m88kexcdeliver  \*/\n' % (cls, cls))
    n = len(pat.findall(src))
    if n != 1:
        print("MUTATE_FAIL match count %d for %s" % (n, cls)); sys.exit(9)
    src = pat.sub(lambda m: m.group(1) + "\t\timplemented = %s;\t/*  MUTANT  */\n" % expr, src)

open(path, "w", encoding="latin1", newline="").write(src)
print("MUTATE_OK %s" % kind)
