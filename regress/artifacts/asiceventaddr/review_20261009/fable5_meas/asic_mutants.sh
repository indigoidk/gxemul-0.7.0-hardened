#!/bin/bash
# fable5 late-review seat, asiceventaddr: the GUARD's own kill table, compile-only.
# Every mutant is applied to a COPY of the header under $SD; the tree is never written.
set -u
SD=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fableq/asictest
REAL=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/include/thirdparty/dreamcast_sysasicvar.h
cd "$SD" || exit 9
OUT=$SD/asic_mutants.out
: > "$OUT"
say() { echo "$@" | tee -a "$OUT"; }
say "real header md5: $(md5sum "$REAL" | cut -c1-12)   gcc: $(gcc --version | head -1)"
say "rows: R1_legal (t_ok.c compiles AND all 21 events same=1)  R2_e96 (must FAIL)  R3_neg1 (must FAIL)  R4_runtime (must FAIL)"

rows() { # $1 = dir holding the header copy
  local inc=$1 res="" spec name file expect got
  for spec in "R1_legal:t_ok.c:ok" "R2_e96:t_96.c:err" "R3_neg1:t_neg1.c:err" "R4_runtime:t_runtime.c:err"; do
    IFS=: read -r name file expect <<< "$spec"
    if gcc -std=c99 -pedantic-errors -Wall -Wextra -O0 -I"$inc" "$file" -o "$inc/$name.bin" > "$inc/$name.log" 2>&1; then got=ok; else got=err; fi
    if [ "$name" = R1_legal ] && [ "$got" = ok ]; then
      if "$inc/$name.bin" | grep -q 'same=0'; then got=shifted; fi
    fi
    if [ "$got" = "$expect" ]; then res="$res $name=green"; else res="$res $name=RED($got)"; fi
  done
  echo "$res"
}

mkdir -p base && cp "$REAL" base/
say "BASE :$(rows "$SD/base")"

mutate() { # name find1 repl1 [find2 repl2]
  local name=$1; shift
  mkdir -p "$name" && cp "$REAL" "$name/"
  python3 -I - "$name/dreamcast_sysasicvar.h" "$@" <<'PY'
import sys, io
p = sys.argv[1]; pairs = sys.argv[2:]
s = io.open(p, encoding="utf-8", newline="").read()
for i in range(0, len(pairs), 2):
    f, r = pairs[i], pairs[i+1]
    n = s.count(f)
    if n != 1:
        print("MUTANT-TEXT-NOT-FOUND-OR-AMBIGUOUS count=%d for %r" % (n, f)); sys.exit(2)
    s = s.replace(f, r)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("applied %d edit(s)" % (len(pairs)//2))
PY
  local rc=$?
  if [ $rc -ne 0 ]; then say "$name: MUTANT NOT APPLIED (rc=$rc) -- scored as a driver FAIL, not as a kill"; return; fi
  local r; r=$(rows "$SD/$name")
  case "$r" in
    *RED*) say "$name: KILLED   ->$r" ;;
    *)     say "$name: *** ESCAPED ***  ->$r" ;;
  esac
  diff -u "$REAL" "$name/dreamcast_sysasicvar.h" | grep -E '^[-+][^-+]' | sed 's/^/      /' | tee -a "$OUT"
}

mutate M1_upper128  '(e) < 96) ? 1 : -1'                   '(e) < 128) ? 1 : -1'
mutate M2_nolower   '((e) >= 0 && (e) < 96) ? 1 : -1'      '((e) < 96) ? 1 : -1'
mutate M3_arrayform '((int)sizeof(struct { int sysasic_event_in_range :\' '((int)sizeof(char[\' \
                    '? 1 : -1; }) * 0)'                    '? 1 : -1]) * 0)'
mutate M4_valueleak '? 1 : -1; }) * 0)'                    '? 1 : -1; }) * 1)'
mutate M5_reinstate ' + SYSASIC_EVENT_RANGE_OK(e))'        ')'
say "ASIC_MUTANTS_DONE"
