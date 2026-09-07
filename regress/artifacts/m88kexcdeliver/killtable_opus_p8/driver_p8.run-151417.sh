#!/bin/bash
#  #502 pass 8 kill table -- Opus 5 measuring seat.  Runs ONLY in the scratch clone.
CLONE=/tmp/gxopus502p8
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/killtable_opus_p8
PROBE=$OUT/m88k_exc_probe.frozenP8.py
CPROBE=$OUT/m88k_exc_probe.censusP8.py
MUT=$OUT/mutate_p8.py
SRC=$CLONE/src/cpus/cpu_m88k.c
BASELINE=$SEC/src/cpus/cpu_m88k.c

log(){ echo "$*" | tee -a "$OUT/driver.log"; }
die(){ log "ABORT: $*"; exit 9; }

: > "$OUT/driver.log"
log "KILLTABLE_P8_START $(date +%H:%M:%S)"

#  ---- 1. NAME THE BASELINE and clone ----
rm -rf "$CLONE"
cp -a /tmp/gxm88kexc_kill "$CLONE" || die "clone failed"
rm -f "$CLONE/.MUTANT"
cmp -s "$SRC" "$BASELINE" || die "clone baseline != SEC working copy (the #502 fix)"
cp "$BASELINE" "$OUT/cpu_m88k.baseline.c"
log "baseline = GXEMUL-SEC working copy (HEAD 83df95c + uncommitted #502 fix), md5 $(md5sum "$BASELINE" | cut -c1-8)"
log "frozen probe md5 $(md5sum "$PROBE" | cut -c1-8)  (shipped regress/m88k_exc_probe.py)"

build(){   #  $1 = tag
    rm -f "$CLONE"/src/cpus/*.o
    ( cd "$CLONE" && make -j2 ) > "$OUT/build_$1.log" 2>&1
    if [ ! "$CLONE/gxemul" -nt "$SRC" ]; then
        log "  BUILD FRESHNESS FAIL for $1 (binary not newer than source)"; tail -5 "$OUT/build_$1.log" | sed 's/^/    /' | tee -a "$OUT/driver.log"; return 1
    fi
    return 0
}
runp(){    #  $1 = tag, $2 = probe
    python3 -u "$2" "$CLONE/gxemul" > "$OUT/$1.out" 2>&1
    grep -m1 '^M88KEXC_RESULT=' "$OUT/$1.out" || echo "NO RESULT LINE"
}
reds(){    #  diff a mutant's row lines against BASE's
    diff <(grep '^M88KEXC_ROW=' "$OUT/BASE.out" | awk '{print $1, $2}') \
         <(grep '^M88KEXC_ROW=' "$OUT/$1.out"   | awk '{print $1, $2}') \
      | grep '^>' | sed 's/^/    RED /' | tee -a "$OUT/driver.log"
}

#  ---- 2. BASE ----
build BASE || die "base build"
log "BASE $(runp BASE "$PROBE")"

#  ---- 3. CENSUS (a premise check, not a scored mutant) ----
echo "cpu_m88k.c census printf" > "$CLONE/.MUTANT"
python3 "$MUT" "$SRC" census || die "census mutate"
build CENSUS || die "census build"
log "CENSUS $(runp CENSUS "$CPROBE")"
M88KEXC_VERBOSE=1 python3 -u "$CPROBE" "$CLONE/gxemul" > "$OUT/CENSUS_verbose.out" 2>&1
grep -o 'M88KCENSUS v=[0-9]* psr=0x[0-9a-f]* t=[0-9]*' "$OUT/CENSUS_verbose.out" | sort | uniq -c | sort -rn > "$OUT/CENSUS_cells.txt"
log "census cells harvested: $(wc -l < "$OUT/CENSUS_cells.txt") distinct (vector,psr,is_trap) triples -> CENSUS_cells.txt"
cp "$BASELINE" "$SRC"; cmp -s "$SRC" "$BASELINE" && rm -f "$CLONE/.MUTANT" || die "census restore"

#  ---- 4. THE MUTANTS ----
run_mutant(){   #  $1 = tag, $2 = class, $3 = expr
    log "=== $1 : case M88K_EXCEPTION_$2 -> implemented = $3  ($(date +%H:%M:%S)) ==="
    echo "cpu_m88k.c $1" > "$CLONE/.MUTANT"
    python3 "$MUT" "$SRC" "$2" "$3" >> "$OUT/driver.log" 2>&1 || { log "  MUTATE FAIL -- counted as FAIL"; cp "$BASELINE" "$SRC"; rm -f "$CLONE/.MUTANT"; return; }
    if build "$1"; then
        log "$1 $(runp "$1" "$PROBE")"
        reds "$1"
    fi
    cp "$BASELINE" "$SRC"
    if cmp -s "$SRC" "$BASELINE"; then rm -f "$CLONE/.MUTANT"; else log "  RESTORE FAIL -- sentinel kept"; fi
}

PSR='cpu->cd.m88k.cr[M88K_CR_PSR]'
run_mutant M_DIV0IND      ILLEGAL_INTEGER_DIVIDE  "($PSR & M88K_PSR_IND) != 0"
run_mutant M_ERRNOC       ERROR                   "!($PSR & M88K_PSR_C)"
run_mutant M_BNDIND       BOUNDS_CHECK_VIOLATION  "($PSR & M88K_PSR_IND) != 0"
run_mutant CTL_DIV0INDINV ILLEGAL_INTEGER_DIVIDE  "!($PSR & M88K_PSR_IND)"
run_mutant CTL_OVFNOC     INTEGER_OVERFLOW        "!($PSR & M88K_PSR_C)"
run_mutant CTL_DIV0SFD1   ILLEGAL_INTEGER_DIVIDE  "!($PSR & M88K_PSR_SFD1)"

#  ---- 5. BASE_final + clearance ----
build BASE_final || die "final build"
log "BASE_final $(runp BASE_final "$PROBE")"
cmp -s "$SRC" "$BASELINE" && log "clone cmp CLEAN vs baseline" || log "clone DIRTY"
[ -f "$CLONE/.MUTANT" ] && log "SENTINEL PRESENT -- clone is mutant" || log "clone clean: no sentinel"
log "KILLTABLE_P8_DONE $(date +%H:%M:%S)"
