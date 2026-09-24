#!/bin/bash
#  extras6.sh TAG GROUP... -- the addendum cases.  Sources lib6.sh for mk/run/gate/pins/rep.
set -u
TAG=$1; shift
case "$TAG" in
  W) B=/mnt/c/DocumentNoSnc/cc/GXEMUL; WORK=/tmp/opusc6_w ;;
  G) B=/c/DocumentNoSnc/cc/GXEMUL; WORK=$B/_scratchpad/census0923/opus_c6/work_g ;;
  *) echo "bad tag"; exit 2 ;;
esac
SRC=$B/GXEMUL-SEC/regress; FROZ=$B/_scratchpad/census0923/c6_frozen; OUT=$B/_scratchpad/census0923/opus_c6/out
TAB=$OUT/TABLE_X$TAG.txt; GLIST=$OUT/GLIST_X.txt
mkdir -p "$OUT" "$WORK"
. "$B/_scratchpad/census0923/opus_c6/lib6.sh"
[ -d "$WORK/_master" ] || master
echo "extras6 $TAG [$*] start $(date '+%F %T')" >> "$TAB"

fixA() {   # the candidate fix, in the COPY's deriver only
    local t="$D/GXEMUL-SEC/tools/derive_hygiene_pins.sh"
    sed -i 's|^            if \[ -e "\$HERE/\$f" \]; then$|            if printf '"'"'%s\\n'"'"' "$_ptylist" \| grep -qxF -- "$f"; then|' "$t"
    echo "FIXA [$TAG] patch landed: $(grep -c 'if printf .%s\\n. "$_ptylist" | grep -qxF -- "$f"; then' "$t") (old form left: $(grep -c 'if \[ -e "$HERE/$f" \]; then' "$t"))" >> "$TAB"; }
k14() { printf '\n\ndef _k14(x):\n    match x:\n        case K.%s("GXemul>"):\n            pass\n' "$EW" >> "$R/gdrom_cond_probe.py"; }
crash_after() {  # $1 = mode to crash in (promptless|whole|any), $2 = after N input lines -- edits the COPY's classifier
    python3 - "$R/census_tokens.py" "$1" "$2" <<'PY'
import io, sys
p, mode, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
s = io.open(p, encoding="utf-8", newline="").read()
old = '    for line in sys.stdin.read().split("\\n"):'
assert s.count(old) == 1, s.count(old)
cond = "True" if mode == "any" else "mode == %r" % mode
new = old + '\n        _zzn = globals().setdefault("_zzn", [0]); _zzn[0] += 1\n        if %s and _zzn[0] > %d: raise RuntimeError("simulated classifier crash")' % (cond, n)
io.open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
PY
}

x_S15() {
    mk S15; cp -p "$R/lca_badval_probe.py" "$R/zz_unk_probe.py"; printf '\n\ndef _zz_ready(buf, PROMPT):\n    if buf.%s(PROMPT):\n        return True\n' "$EW" >> "$R/zz_unk_probe.py"
    run S15.1; run S15.2 --write; gate S15.3; }
x_S16() {
    mk S16; cp -p "$R/lca_badval_probe.py" "$R/zz_newpl_probe.py"; trio "$R/gdrom_cond_probe.py" ":"; rm "$R/sgi_re_rgb_probe.py"
    run S16.1; run S16.2 --write; run S16.3 --grandfather zz_newpl_probe.py; run S16.4 --release gdrom_cond_probe.py sgi_re_rgb_probe.py
    run S16.5 --write; gate S16.6; }
x_FIXA() {
    mk FA8a; fixA; sed -i '190s/pty\.fork()/os.forkpty()/' "$R/lca_badval_probe.py"
    run FA8a.1 --release lca_badval_probe.py; run FA8a.2 --write; gate FA8a.3
    mk FA8b; fixA; sed -i '190s/pty\.fork()/drive_guest.fork_guest()/; 124s/$/\nimport drive_guest/' "$R/lca_badval_probe.py"
    run FA8b.1 --release lca_badval_probe.py; run FA8b.2 --write; gate FA8b.3
    mk FA8c; fixA; cp -p "$R/luna_absentcpu_probe.py" "$R/zz_session_helper.py"
    sed -i '190s/pty\.fork()/zz_session_helper.fork_guest()/; 124s/$/\nimport zz_session_helper/' "$R/lca_badval_probe.py"
    run FA8c.1 --release lca_badval_probe.py; run FA8c.2 --write; gate FA8c.3
    mk FAk14; fixA; k14; run FAk14.1 --release gdrom_cond_probe.py
    mk FA3; fixA; trio "$R/gdrom_cond_probe.py" ":"; run FA3.1 --release gdrom_cond_probe.py; run FA3.2 --write; gate FA3.3
    mk FA4a; fixA; rm "$R/lca_badval_probe.py"; run FA4a.1 --release lca_badval_probe.py; run FA4a.2 --write; gate FA4a.3
    mk FA6c; fixA; trio "$R/gdrom_cond_probe.py" ""; run FA6c.1 --release gdrom_cond_probe.py
    mk FAbase; fixA; run FAbase.1; run FAbase.2 --write; gate FAbase.3; }
x_FIXApartial() {   # W only (python3 edits the classifier copy)
    mk FAkp; fixA; crash_after promptless 10; run FAkp.1; run FAkp.2 --release gdrom_cond_probe.py; }
x_N() {             # W only
    mk Nwf2; cp -p "$R/arm_flags_probe.py" "$R/zz:9 x.py"; run Nwf2.1 --write --ruling "$R1"; gate Nwf2.2
    mk Nk14; k14; run Nk14.1; run Nk14.2 --release gdrom_cond_probe.py
    mk Nkp; crash_after promptless 10; run Nkp.1; run Nkp.2 --release gdrom_cond_probe.py
    mk Npy0; cp -p "$R/pcc2_width_probe.py" "$R/zz-legit_probe.py"
    python3 - "$R/gate_hygiene.sh" <<'PY'
import io, re, sys
p = sys.argv[1]; s = io.open(p, encoding="utf-8", newline="").read()
m = re.search(r'(?ms)^GRANDFATHERED_PROMPTLESS="[^"]*"[ \t]*\n', s); assert m
s = s[:m.end()] + 'GRANDFATHERED_PROMPTLESS="gdrom_cond_probe.py"\n' + s[m.end():]
io.open(p, "w", encoding="utf-8", newline="").write(s)
PY
    run Npy0.1 --grandfather zz-legit_probe.py; echo "Npy0 [$TAG] zz-legit in the gate: $(grep -c 'zz-legit_probe.py' "$R/gate_hygiene.sh")" >> "$TAB"; }
x_S14() {           # W only: the classifier dies in WHOLE mode after 2 inputs (the canary feeds 1)
    mk S14; crash_after whole 2
    run S14.1; run S14.2 --write; run S14.3 --write --ruling "$R1"; gate S14.4
    cp -p "$WORK/_master/GXEMUL-SEC/regress/census_tokens.py" "$R/census_tokens.py"; gate S14.5real; }
x_S12() {           # G only: invocation variants on the baseline tree
    mk S12; local base="$OUT/G_S12.std.out"
    ( cd "$D/GXEMUL-SEC" && bash tools/derive_hygiene_pins.sh ) > "$base" 2>&1; echo "S12.std [G] rc=$?" >> "$TAB"
    ( cd "$D/GXEMUL-SEC/regress" && bash ../tools/derive_hygiene_pins.sh ) > "$OUT/G_S12.fromregress.out" 2>&1; echo "S12.fromregress [G] rc=$? same-as-std: $(cmp -s "$base" "$OUT/G_S12.fromregress.out" && echo yes || echo NO)" >> "$TAB"
    ( cd / && bash "$D/GXEMUL-SEC/tools/derive_hygiene_pins.sh" ) > "$OUT/G_S12.abs.out" 2>&1; echo "S12.abs [G] rc=$? same-as-std: $(cmp -s "$base" "$OUT/G_S12.abs.out" && echo yes || echo NO)" >> "$TAB"
    local win; win=$(cd "$D" && pwd -W)
    ( cd "$D/GXEMUL-SEC" && GXROOT="$win" bash tools/derive_hygiene_pins.sh ) > "$OUT/G_S12.gxrootwin.out" 2>&1; echo "S12.gxrootwin [G] GXROOT=$win rc=$? same-as-std: $(cmp -s "$base" "$OUT/G_S12.gxrootwin.out" && echo yes || echo NO)" >> "$TAB"
    ( cd "$D/GXEMUL-SEC" && MSYS_NO_PATHCONV=1 bash tools/derive_hygiene_pins.sh ) > "$OUT/G_S13.out" 2>&1; echo "S13.nopathconv [G] rc=$? $(grep -E '^(DERIVE_FAIL|DERIVE_DONE)' "$OUT/G_S13.out" | head -1 | cut -c1-140)" >> "$TAB"; }
for g in "$@"; do "x_$g"; done
echo "extras6 $TAG [$*] end $(date '+%F %T')" >> "$TAB"
echo EXTRAS6_DONE
