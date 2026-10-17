#!/usr/bin/env python3
"""write_baseline.py <ledger.json> <out baseline.json> -- ONE-TIME: freeze the off-domain ANSWER entries present when
check_entry_domain.py landed (2026-10-16, ledger `dashokclass`), as [row, phase, seat, date, d, count] rows sorted for a
stable diff.  check_entry_domain.py only READS the baseline; re-running this to make a new entry pass would launder it,
which is why it lives in the round's artifacts directory and not beside the checker."""
import collections, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
src, dst = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.environ.get("GXPIPELINE") or os.path.join(HERE, os.pardir, os.pardir, os.pardir, "tools", "pipeline"))
import check_entry_domain as ced  # noqa: E402  (the checker's own off_domain_answers: one definition)

L = json.load(io.open(src, encoding="utf-8"))
c = collections.Counter(ced.off_domain_answers(L))
rows = sorted([list(k) + [n] for k, n in c.items()], key=lambda r: [str(x) for x in r])
#  one tuple per line, so a rewritten entry is a one-line diff
io.open(dst, "w", encoding="utf-8", newline="\n").write("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n")
print("baseline: %d off-domain answer entries in %d tuples -> %s" % (sum(c.values()), len(c), dst))
