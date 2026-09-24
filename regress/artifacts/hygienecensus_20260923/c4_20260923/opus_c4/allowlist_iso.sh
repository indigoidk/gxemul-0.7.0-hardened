#!/bin/bash
chk() { local f=$1; if [ -n "$f" ] && [ -z "$(printf '%s' "$f" | LC_ALL=C tr -d 'A-Za-z0-9._/-')" ]; then echo "PASSES allow-list"; else echo "refused"; fi; }
printf 'name zz<NL>x.py   : '; chk "$(printf 'zz\nx.py')"
printf 'name zz<TAB>x.py  : '; chk "$(printf 'zz\tx.py')"
printf 'name zz<CR>x.py   : '; chk "$(printf 'zz\rx.py')"
printf 'name <NL> only    : '; chk "$(printf '\nX' | head -c1)"
printf 'name ok.py<NL>    : '; chk "ok.py"$'\n'
printf 'bytes left by tr for zz<NL>x.py: '; printf 'zz\nx.py' | LC_ALL=C tr -d 'A-Za-z0-9._/-' | od -An -c
echo ALLOWLIST_ISO_DONE
