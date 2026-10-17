#!/usr/bin/env python3
"""write_baseline.py <ledger.json> <out baseline.json> [--force] -- ONE-TIME: freeze the off-domain ANSWER entries present when
check_entry_domain.py landed (2026-10-16, ledger `dashokclass`), as [row, phase, seat, date, d, note_sha, count] rows, one per
line, sorted for a stable diff, and print the md5 to pin as the checker's BASELINE_MD5.  It REFUSES an existing destination
without --force: re-freezing would launder every entry added since, so it is a reviewed decision made in the checker (its
BASELINE_MD5 changes in the same commit, with the reason), never a side effect of running this file."""
import collections, hashlib, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if a != "--force"]
src, dst = args[0], args[1]
if os.path.exists(dst) and "--force" not in sys.argv:
    print("REFUSING: %s exists -- re-freezing is a reviewed decision (see check_entry_domain.py's BASELINE_MD5)" % dst)
    sys.exit(2)
sys.path.insert(0, os.environ.get("GXPIPELINE") or os.path.join(HERE, os.pardir, os.pardir, os.pardir, "tools", "pipeline"))
import check_entry_domain as ced  # noqa: E402  (the checker's own off_domain_answers: one definition)

L = json.load(io.open(src, encoding="utf-8"))
c = collections.Counter(ced.off_domain_answers(L))
rows = sorted([list(k) + [n] for k, n in c.items()], key=lambda r: [str(x) for x in r])
text = "[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n"
io.open(dst, "w", encoding="utf-8", newline="\n").write(text)
print("baseline: %d off-domain answer entries in %d identities -> %s" % (sum(c.values()), len(c), dst))
print("BASELINE_MD5 = %s" % hashlib.md5(text.encode("utf-8")).hexdigest())
