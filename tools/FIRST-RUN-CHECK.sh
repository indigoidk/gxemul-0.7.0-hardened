#!/bin/bash
# GXemul resume -- first-run environment check for a NEW machine.
# Run from inside WSL Gentoo, from the project root:
#     wsl -d Gentoo -- bash FIRST-RUN-CHECK.sh /path/to/project/root
# Reports PASS/FAIL per item. Nothing is modified.
ROOT="${1:-$(pwd)}"
pass=0; fail=0
ok()   { echo "  PASS  $1"; pass=$((pass+1)); }
bad()  { echo "  FAIL  $1"; fail=$((fail+1)); }
note() { echo "  ....  $1"; }

echo "=== project root: $ROOT ==="
echo
echo "--- 1. trees present ---"
for d in GXEMUL-SEC est build gxemul_arc_rig gxemul_pmax_rig; do
    [ -d "$ROOT/$d" ] && ok "$d present" || bad "$d MISSING"
done

echo
echo "--- 2. toolchain (this distro) ---"
for c in gcc make python3; do
    v=$(command -v $c 2>/dev/null)
    [ -n "$v" ] && ok "$c -> $v" || bad "$c NOT FOUND"
done
[ -f /usr/include/X11/Xlib.h ] && ok "X11 headers present" || bad "X11 headers MISSING (build will configure differently)"
note "distro name must be 'Gentoo' -- every build command is: wsl -d Gentoo"

echo
echo "--- 3. the two trees must be byte-identical except the known 5 ---"
diffs=0
for f in $(cd "$ROOT/GXEMUL-SEC/src" && find . -name '*.c' -o -name '*.h' | sort); do
    a="$ROOT/est/src/$f"; b="$ROOT/GXEMUL-SEC/src/$f"
    [ -f "$a" ] && [ -f "$b" ] || continue
    cmp -s "$a" "$b" || { diffs=$((diffs+1)); echo "        differs: $f"; }
done
if [ "$diffs" -le 6 ]; then ok "divergence = $diffs files (expect ~5-6: dev_jazz.c diskimage.c machine_arc.c arcbios.c dev_ne2000.c + Makefile.skel)"
else bad "divergence = $diffs files -- TOO MANY, the trees are out of sync"; fi

echo
echo "--- 4. git ---"
if git -C "$ROOT/GXEMUL-SEC" rev-parse HEAD >/dev/null 2>&1; then
    ok "repo readable, HEAD $(git -C "$ROOT/GXEMUL-SEC" rev-parse --short HEAD)"
    d=$(git -C "$ROOT/GXEMUL-SEC" status --porcelain | wc -l)
    [ "$d" = "0" ] && ok "working tree clean" || bad "working tree has $d modified files -- investigate before building"
else
    bad "git cannot read the repo (on a network share, add safe.directory -- see RESUME.md)"
fi

echo
echo "--- 5. the arc build tree is NOT in the snapshot and must be recreated ---"
if [ -d /tmp/gxsec-build ]; then
    ok "/tmp/gxsec-build exists"
    [ -f /tmp/gxsec-build/Makefile ] && ok "/tmp/gxsec-build is configured" \
        || bad "/tmp/gxsec-build has NO Makefile -- run: cd /tmp/gxsec-build && ./configure"
else
    note "/tmp/gxsec-build absent -- expected. Recreate: cp -a \"$ROOT/GXEMUL-SEC\" /tmp/gxsec-build"
    note "  THEN CONFIGURE IT: cd /tmp/gxsec-build && ./configure  -- the Makefile is GENERATED,"
    note "  not tracked, so a fresh cp -a has none and make dies with 'no makefile found' (rc=2,"
    note "  0 objects/0 errors). regress_clean_build.sh calls make directly and does not do this."
fi
note "NO VPATH: edits must be propagated into build/ and /tmp/gxsec-build, or you test stale binaries"

echo
echo "--- 6. rigs bootable? (images present) ---"
ls "$ROOT/gxemul_pmax_rig"/*.img >/dev/null 2>&1 && ok "pmax rig images present" || bad "pmax rig images MISSING"
ls "$ROOT/gxemul_arc_rig"/*.img >/dev/null 2>&1 && ok "arc rig images present" || bad "arc rig images MISSING"
[ -f "$ROOT/gxemul_pmax_rig/boot_login.sh" ] && ok "pmax boot harness present" || bad "pmax boot harness MISSING"
[ -f "$ROOT/gxemul_arc_rig/boot_login_arc_r23.sh" ] && ok "arc boot harness present" || bad "arc boot harness MISSING"

echo
echo "--- 7. hardcoded paths that will need rewriting ---"
if [ -d "$ROOT/_scratchpad" ]; then
    n=$(grep -rl "DocumentNoSnc\|/mnt/c/Users/user00a" "$ROOT/_scratchpad" 2>/dev/null | wc -l)
    note "$n scratchpad files reference the ORIGINAL absolute paths -- rewrite before running probes"
else
    bad "$ROOT/_scratchpad NOT FOUND -- cannot audit hardcoded paths (and the probe rigs are missing)"
fi

echo
echo "=================================================="
echo "  PASS: $pass    FAIL: $fail"
[ "$fail" -eq 0 ] && echo "  Environment looks sound. Next: rebuild both trees (regress_clean_build.sh)," \
                  && echo "  then boot both rigs (expect pmax 15/15, arc 13/13 -> uid=0) BEFORE any code change."
[ "$fail" -gt 0 ] && echo "  Resolve the FAIL items first -- see RESUME.md."
echo "=================================================="
