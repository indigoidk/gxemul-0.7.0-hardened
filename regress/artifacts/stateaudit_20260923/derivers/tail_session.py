import json, sys, io
# Print the last N human-readable turns of a Claude Code transcript (user text, assistant text,
# tool-use summaries), skipping bulky tool results.  Usage: tail_session.py <jsonl> [N] [maxchars]
path = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 40
MAXC = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
out = []
with io.open(path, encoding='utf-8', errors='replace') as f:
    for line in f:
        try:
            o = json.loads(line)
        except Exception:
            continue
        t = o.get('type')
        ts = o.get('timestamp', '')
        msg = o.get('message') or {}
        content = msg.get('content')
        if t == 'user':
            if isinstance(content, str):
                out.append((ts, 'USER', content))
            elif isinstance(content, list):
                for c in content:
                    if c.get('type') == 'text':
                        out.append((ts, 'USER', c.get('text', '')))
                    elif c.get('type') == 'tool_result':
                        r = c.get('content')
                        if isinstance(r, list):
                            r = ' '.join(x.get('text', '') for x in r if isinstance(x, dict))
                        out.append((ts, 'RESULT', str(r)[:300]))
        elif t == 'assistant':
            model = msg.get('model', '')
            if isinstance(content, list):
                for c in content:
                    if c.get('type') == 'text':
                        out.append((ts, 'ASSIST[' + model + ']', c.get('text', '')))
                    elif c.get('type') == 'tool_use':
                        inp = c.get('input', {})
                        s = inp.get('command') or inp.get('description') or inp.get('file_path') or inp.get('prompt') or json.dumps(inp)[:300]
                        out.append((ts, 'TOOL ' + c.get('name', ''), str(s)[:400]))
        elif t == 'system':
            out.append((ts, 'SYSTEM', str(o.get('content', ''))[:300]))
w = io.open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)
for ts, who, txt in out[-N:]:
    txt = txt if len(txt) <= MAXC else txt[:MAXC] + ' ...[+%d]' % (len(txt) - MAXC)
    w.write('--- %s %s\n%s\n' % (ts, who, txt))
w.flush()
