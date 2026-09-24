import json, io, re, os, sys, subprocess, collections
# FALSIFIER for "nothing was lost": every path the RECENT records cite -- does it exist on disk, in HEAD, in a snapshot?
# Sources: ledger entries dated >= CUTOFF (working-tree ledger), OUTSTANDING_BUGS.md, the newest CHANGELOG blocks.
ROOT = r'C:\DocumentNoSnc\cc\GXEMUL'
SEC = os.path.join(ROOT, 'GXEMUL-SEC')
CUTOFF = sys.argv[1] if len(sys.argv) > 1 else '2026-09-12'
SNAPS = ['60b28f6', 'ff7ab93']
PATH = re.compile(r'(?:GXEMUL-SEC/)?(?:regress/artifacts|_scratchpad|regress|tools|src)/[A-Za-z0-9_.@+\-/]+[A-Za-z0-9_]')
def git(*a):
    return subprocess.run(['git', '-C', SEC] + list(a), capture_output=True, text=True, encoding='utf-8', errors='replace')
head_files = set(git('ls-tree', '-r', '--name-only', 'HEAD').stdout.split('\n'))
snap_files = {s: set(git('ls-tree', '-r', '--name-only', s).stdout.split('\n')) for s in SNAPS}
def in_tree(names, rel):
    return rel in names or any(n.startswith(rel.rstrip('/') + '/') for n in names)
cites = collections.defaultdict(set)
L = json.load(io.open(os.path.join(SEC, 'tools', 'pipeline', 'ledger.json'), encoding='utf-8'))
for r in L['rows']:
    for e in r.get('entries') or []:
        if (e.get('date') or '') >= CUTOFF:
            for k in ('note', 'ev', 'outcome_note', 'evidence'):
                for m in PATH.findall(str(e.get(k) or '')):
                    cites[m].add('ledger:' + r['id'])
bugs = io.open(os.path.join(SEC, 'OUTSTANDING_BUGS.md'), encoding='utf-8').read()
for m in PATH.findall(bugs[-400000:]):
    cites[m].add('BUGS(tail)')
cl = io.open(os.path.join(SEC, 'CHANGELOG.md'), encoding='utf-8').read()
for m in PATH.findall(cl[:400000]):
    cites[m].add('CHANGELOG(head)')
missing, ok, weird = [], 0, 0
for p, src in sorted(cites.items()):
    if any(ch in p for ch in '<>*{}') or p.endswith(('.', '-')) or '...' in p:
        weird += 1; continue
    rel = p[len('GXEMUL-SEC/'):] if p.startswith('GXEMUL-SEC/') else p
    if rel.startswith('_scratchpad/'):
        disk = os.path.exists(os.path.join(ROOT, rel)) or os.path.exists(os.path.join(SEC, rel))
        where = 'scratch'
    else:
        disk = os.path.exists(os.path.join(SEC, rel))
        where = 'repo'
    if disk:
        ok += 1; continue
    h = in_tree(head_files, rel) if where == 'repo' else False
    s = [x for x in SNAPS if where == 'repo' and in_tree(snap_files[x], rel)]
    missing.append((where, rel, h, s, sorted(src)[:3]))
w = io.open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)
w.write('cited paths: %d  exist on disk: %d  skipped (templates/globs/truncated): %d  MISSING on disk: %d\n' % (len(cites), ok, weird, len(missing)))
for where, rel, h, s, src in missing:
    w.write('  MISSING %-7s %-95s HEAD=%s snaps=%s  cited by %s\n' % (where, rel[:95], 'yes' if h else 'no', ','.join(s) or '-', ', '.join(src)))
w.flush()
