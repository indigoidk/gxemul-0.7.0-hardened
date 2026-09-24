import io, sys
p = sys.argv[1]; s = io.open(p, encoding="utf-8", newline="").read()
old = '''            if [ -e "$HERE/$f" ]; then
                astcall "$HERE/$f"; _a=$?
                [ $_a -eq 0 ] || { echo "REFUSED: $f -- the parser finds no readiness call in it (rc $_a): it is still promptless"; exit 4; }
            fi
'''
new = '''            if printf '%s\n' "$_ptylist" | grep -qxF -- "$f"; then
                astcall "$HERE/$f"; _a=$?
                [ $_a -eq 0 ] || { [ $_a -eq 1 ] && echo "REFUSED: $f -- the parser finds no readiness call in it: it is still promptless" \
                                   || echo "REFUSED: $f -- Python's parser cannot read it (rc $_a); fix the file first"; exit 4; }
            elif [ -e "$HERE/$f" ] && grep -qE 'forkpty|pty\.spawn' "$HERE/$f"; then
                echo "REFUSED: $f no longer says pty.fork but still creates a pty (forkpty or pty.spawn), which the census does not enumerate -- keep pty.fork, or give it prompt detection"; exit 4
            fi
'''
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
o2 = '    t = ast.parse(open(sys.argv[1], encoding="utf-8").read())'
assert s.count(o2) == 1
s = s.replace(o2, '    t = ast.parse(open(sys.argv[1], encoding="utf-8-sig").read())')
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("FIXAP applied")
