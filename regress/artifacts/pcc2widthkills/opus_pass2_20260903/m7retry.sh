#!/bin/bash
#  M7 RETRY -- the first attempt died on the documented Bash->heredoc->Python
#  backslash trap (one level consumed; the C string literal was split by a REAL
#  newline).  Built with chr(92) this time, per the carrier's own remedy.
#  Then the Q1 IPL wide-read check on the restored BASE binary.
T=/tmp/gxopus_pcc2
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p2_opus
REF=$OUT/dev_pcc2.b78bb0f.c
SRC=$T/src/devices/dev_pcc2.c
build () {
	rm -f "$T/src/devices/dev_pcc2.o" "$T/gxemul"
	( cd "$T" && make ) > /tmp/pcc2_build.log 2>&1
	[ -x "$T/gxemul" ] || { echo "  BUILD FAILED"; grep -m6 -E 'error|Error' /tmp/pcc2_build.log; return 1; }
	[ "$T/gxemul" -nt "$SRC" ] || { echo "  *** STALE BINARY ***"; return 1; }
	echo "  build ok, binary -nt source"; return 0
}
echo "=== M7 RETRY: verbatim exit(1) kill reinstated at PCCTWO_IPL (0x3e, EVEN => GUEST-reachable) ==="
echo "M7 dev_pcc2.c" > "$T/.MUTANT"
cp /tmp/pcc2_baseline.c "$SRC"
python3 - <<'PYEOF'
BS = chr(92)
p = "/tmp/gxopus_pcc2/src/devices/dev_pcc2.c"
s = open(p).read()
old = ('if (len != 1 && writeflag == MEM_WRITE) {\n'
       '\t\t\tpcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);\n'
       '\t\t\tbreak;')
new = ('if (len != 1) {\n'
       '\t\t\tfatal("TODO: pcc2: non-byte access to PCCTWO_IPL' + BS + 'n");\n'
       '\t\t\texit(1);')
assert s.count(old) == 1, "COUNT %d" % s.count(old)
open(p, "w").write(s.replace(old, new))
print("  mutated: M7  (C string ends with backslash-n: %r)"
      % new.split('fatal(')[1][:52])
PYEOF
if build; then
	( cd "$SEC/regress" && timeout 1800 python3 -u pcc2_width_probe.py "$T/gxemul" M7 ) \
	    > "$OUT/probe_M7.out" 2>&1
	grep -E '^PCC2W_(RESULT|RED|PROBE_DONE)' "$OUT/probe_M7.out" | sed 's/^/  /'
fi

echo
echo "=== RESTORE to the b78bb0f blob and rebuild ==="
cp /tmp/pcc2_baseline.c "$SRC"
if cmp -s "$SRC" "$REF"; then echo "  PART 1 OK: == b78bb0f blob"; else echo "  PART 1 FAIL"; fi
build && rm -f "$T/.MUTANT" && echo "  SENTINEL CLEARED (both parts verified)"

echo
echo "=== Q1: wide READ of PCCTWO_IPL on the restored BASE binary ==="
python3 -u "$OUT/iplread_check.py" "$T/gxemul" 2>&1 | sed 's/^/  /'
echo "M7RETRY_DONE"
