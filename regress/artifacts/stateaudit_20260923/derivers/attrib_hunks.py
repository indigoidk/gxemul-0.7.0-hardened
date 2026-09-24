import subprocess, re, io, sys, collections
# For every tracked file modified in the working tree: hunks, +/- counts, and the #NNN round tags that
# appear in ADDED lines.  Then, for each tag, what the COMMITTED records say about it (HEAD's CHANGELOG,
# HEAD's ledger), so an uncommitted hunk whose round is recorded as SHIPPED stands out.
REPO = r'C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC'
def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
files = [l[3:] for l in git('status', '--porcelain=v1').splitlines() if l[:2] == ' M']
TAG = re.compile(r'#(5\d\d|4\d\d)\b')
cl_head = git('show', 'HEAD:CHANGELOG.md')
led_head = git('show', 'HEAD:tools/pipeline/ledger.json')
w = io.open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)
alltags = collections.Counter()
for f in files:
    d = git('diff', '-U0', 'HEAD', '--', f)
    hunks = d.count('\n@@')
    plus = [l[1:] for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')]
    minus = [l for l in d.splitlines() if l.startswith('-') and not l.startswith('---')]
    tags = collections.Counter(m for l in plus for m in TAG.findall(l))
    alltags.update({t: 1 for t in tags})
    w.write('%-44s hunks=%-3d +%-5d -%-5d tags(+lines)=%s\n' % (f, hunks, len(plus), len(minus),
            ', '.join('#%s x%d' % (t, n) for t, n in tags.most_common(8)) or '-'))
w.write('\n=== per tag: does HEAD\'s CHANGELOG carry a round block for it?  (heading "# `#NNN`" or "#NNN (")\n')
for t in sorted(alltags):
    hd = re.search(r'^#+ .*`?#%s\b' % t, cl_head, re.M)
    anyref = len(re.findall(r'#%s\b' % t, cl_head))
    w.write('  #%s  heading_in_HEAD_CHANGELOG=%s  mentions_in_HEAD_CHANGELOG=%d  mentions_in_HEAD_ledger=%d\n' % (
        t, 'YES' if hd else 'no', anyref, len(re.findall(r'#%s\b' % t, led_head))))
w.flush()
