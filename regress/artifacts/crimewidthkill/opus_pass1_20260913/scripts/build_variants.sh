#!/bin/bash
# build_variants.sh -- scratch clone of build/, one binary per crimewidthkill candidate.
# Writes ONLY /tmp/gxopuscrime and /tmp/gxopuscrime_bins.  Restores the clone at the end.
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxopuscrime_bins
F=src/devices/dev_sgi_ip32.c
rm -rf "$C" "$B"; mkdir -p "$B"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$C" || { echo "CLONE FAILED"; exit 1; }
cd "$C" || exit 1
if cmp -s "$F" "$SEC/$F"; then echo "BASELINE_CMP CLEAN $F"; else echo "BASELINE_CMP DIFFERS $F -- abort"; exit 1; fi
for f in src/cpus/memory_rw.c src/cpus/cpu_mips_instr_loadstore.c src/cpus/cpu_mips.c \
         src/cpus/cpu_mips_coproc.c src/cpus/cpu_mips_instr.c src/cpus/cpu_mips_instr_unaligned.c \
         src/machines/machine_sgi.c src/include/thirdparty/crimereg.h src/devices/dev_unreadable.c; do
    if cmp -s "$f" "$SEC/$f"; then echo "cmp CLEAN $f"; else echo "cmp DIFF  $f"; fi
done
echo "$F crimewidthkill variants (opus pass1)" > .MUTANT

build() {
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > "$B/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1 rc=$rc fresh=yes"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -20 "$B/build_$1.log"; return 1
    fi
}

build base || exit 1
for v in fault decline delete; do
    python3 "$SP/apply_variant.py" "$v" "$SEC/$F" "$F" || { echo "APPLY FAILED $v"; exit 1; }
    diff -u "$SEC/$F" "$F" > "$B/$v.diff"
    build "$v" || exit 1
done

# restore the clone from SEC and rebuild; clear the sentinel only after cmp AND freshness
cp "$SEC/$F" "$F"
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
if cmp -s "$B/base" "$B/restored"; then echo "restored binary == base binary (byte-identical)"; else echo "restored binary differs from base (timestamps/paths may embed)"; fi
ls -la "$B"
echo BUILD_VARIANTS_DONE
