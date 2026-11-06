#!/usr/bin/env python3
"""fix_hand4.py -- GPT-6 Astra's pass-2b repair (p2b_astra/codex_fmtp2b.txt): file_ecoff.c:407 printed two off_t values with
%08lx, but off_t need not be long.  Print both full width with PRIx64 and (uint64_t) casts.  Idempotent."""
import io

ST = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix/stage/"
N = chr(92) + "n"
f = "src/file/file_ecoff.c"
old = ('\t\tdebug("%i symbols @ 0x%08lx (strings @ 0x%08lx)' + N + '",\n'
       '\t\t    iextMax, cbExtOffset, cbSsExtOffset);')
new = ('\t\tdebug("%i symbols @ 0x%08" PRIx64\n'
       '\t\t    " (strings @ 0x%08" PRIx64 ")' + N + '",\n'
       '\t\t    iextMax, (uint64_t)cbExtOffset, (uint64_t)cbSsExtOffset);')
t = io.open(ST + f, encoding="latin-1", newline="").read()
if t.count(old) == 0 and t.count(new) == 1:
    print("already applied")
else:
    assert t.count(old) == 1, t.count(old)
    assert all(len(l.expandtabs(8)) <= 79 for l in new.split("\n"))
    io.open(ST + f, "w", encoding="latin-1", newline="").write(t.replace(old, new))
    print("file_ecoff.c: off_t printed with PRIx64")
