#!/bin/bash
#  FIVE CONTROL STATES for the gdrom_w_masks_disjoint compile-time assert.
#  Extracts the enum + masks + assert into a standalone TU so the property is
#  tested exactly, without a 6 MB build.  Run as a SCRIPT FILE (the wsl -c
#  dollar-stripping trap).
set -u
T=/tmp/gdromassert
rm -rf "$T"; mkdir -p "$T"

gen () {   # $1 = outfile, $2 = FMT bit, $3 = CMD bit, $4 = "yes"|"no" include assert
cat > "$1" <<EOF
enum {
	GDROM_W_LEN_B,
	GDROM_W_NODATA_B,
	GDROM_W_NOTWAIT_B,
	GDROM_W_OVERREAD_B,
	GDROM_W_DMANODATA_B,
	GDROM_W_DMAARM_B,
	GDROM_W_TOCLEN_B,
	GDROM_W_FMT_B,
	GDROM_W_CMD_B,
	GDROM_W_NBITS
};
#define	GDROM_W_LEN		(1u << GDROM_W_LEN_B)
#define	GDROM_W_NODATA		(1u << GDROM_W_NODATA_B)
#define	GDROM_W_NOTWAIT		(1u << GDROM_W_NOTWAIT_B)
#define	GDROM_W_OVERREAD	(1u << GDROM_W_OVERREAD_B)
#define	GDROM_W_DMANODATA	(1u << GDROM_W_DMANODATA_B)
#define	GDROM_W_DMAARM		(1u << GDROM_W_DMAARM_B)
#define	GDROM_W_TOCLEN		(1u << GDROM_W_TOCLEN_B)
#define	GDROM_W_FMT		(1u << $2)
#define	GDROM_W_CMD		(1u << $3)
EOF
if [ "$4" = "yes" ]; then
cat >> "$1" <<'EOF'
typedef char gdrom_w_masks_disjoint[
    ((GDROM_W_LEN | GDROM_W_NODATA | GDROM_W_NOTWAIT | GDROM_W_OVERREAD |
      GDROM_W_DMANODATA | GDROM_W_DMAARM | GDROM_W_TOCLEN | GDROM_W_FMT |
      GDROM_W_CMD) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];
EOF
fi
echo 'int main(void) { return 0; }' >> "$1"
}

run () {  # $1 label, $2 want COMPILES|REFUSED, $3 fmtbit, $4 cmdbit, $5 assert
  gen "$T/t.c" "$3" "$4" "$5"
  if gcc -std=gnu99 -c "$T/t.c" -o "$T/t.o" 2>"$T/err"; then got=COMPILES; else got=REFUSED; fi
  if [ "$got" = "$2" ]; then mark=ok; else mark="*** WRONG ***"; fi
  printf '  %-46s want=%-9s got=%-9s %s\n' "$1" "$2" "$got" "$mark"
}

echo "=== FIVE CONTROL STATES ==="
run "1. correct source, assert present"        COMPILES GDROM_W_FMT_B      GDROM_W_CMD_B  yes
run "2. E1 alias: FMT -> OVERREAD_B"           REFUSED  GDROM_W_OVERREAD_B GDROM_W_CMD_B  yes
run "3. Ma_toclen shape: FMT -> TOCLEN_B"      REFUSED  GDROM_W_TOCLEN_B   GDROM_W_CMD_B  yes
run "4. M3shared shape: CMD -> FMT_B"          REFUSED  GDROM_W_FMT_B      GDROM_W_FMT_B  yes
run "5. NEGATIVE CONTROL: E1, assert ABSENT"   COMPILES GDROM_W_OVERREAD_B GDROM_W_CMD_B  no
echo
echo "=== the refusal message the assert actually produces (state 2) ==="
gen "$T/t.c" GDROM_W_OVERREAD_B GDROM_W_CMD_B yes
gcc -std=gnu99 -c "$T/t.c" -o "$T/t.o" 2>&1 | head -3 | sed 's/^/  /'
echo
echo "ASSERT_CONTROLS_DONE"
