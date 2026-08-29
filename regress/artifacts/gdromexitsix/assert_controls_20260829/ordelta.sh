#!/bin/bash
#  MEASURED DELTA for `|` vs `+` in the disjointness assert.
#
#  The seat's claim: `|` catches single-bit aliasing but NOT a mask redefined as a
#  MULTI-BIT LITERAL, because OR-ing a superset still yields all-ones.  `+` catches
#  it, because a carry pushes the sum past all-ones.  Test both forms against both
#  mutants; the delta is the cell where they differ.
set -u
T=/tmp/ordelta
rm -rf "$T"; mkdir -p "$T"

gen () {  # $1 out, $2 FMT-define-body, $3 operator
cat > "$1" <<EOF
enum {
	GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B, GDROM_W_OVERREAD_B,
	GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, GDROM_W_TOCLEN_B,
	GDROM_W_FMT_B, GDROM_W_CMD_B, GDROM_W_NBITS
};
#define	GDROM_W_LEN		(1u << GDROM_W_LEN_B)
#define	GDROM_W_NODATA		(1u << GDROM_W_NODATA_B)
#define	GDROM_W_NOTWAIT		(1u << GDROM_W_NOTWAIT_B)
#define	GDROM_W_OVERREAD	(1u << GDROM_W_OVERREAD_B)
#define	GDROM_W_DMANODATA	(1u << GDROM_W_DMANODATA_B)
#define	GDROM_W_DMAARM		(1u << GDROM_W_DMAARM_B)
#define	GDROM_W_TOCLEN		(1u << GDROM_W_TOCLEN_B)
#define	GDROM_W_FMT		$2
#define	GDROM_W_CMD		(1u << GDROM_W_CMD_B)
typedef char gdrom_w_masks_disjoint[
    ((GDROM_W_LEN $3 GDROM_W_NODATA $3 GDROM_W_NOTWAIT $3 GDROM_W_OVERREAD $3
      GDROM_W_DMANODATA $3 GDROM_W_DMAARM $3 GDROM_W_TOCLEN $3 GDROM_W_FMT $3
      GDROM_W_CMD) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];
int main(void) { return 0; }
EOF
}

cell () {  # $1 label, $2 body, $3 op
  gen "$T/t.c" "$2" "$3"
  if gcc -std=gnu99 -c "$T/t.c" -o "$T/t.o" 2>/dev/null; then echo -n "COMPILES"; else echo -n "REFUSED "; fi
}

SINGLE='(1u << GDROM_W_FMT_B)'
ALIAS='(1u << GDROM_W_OVERREAD_B)'
MULTI='((1u << GDROM_W_FMT_B) | (1u << GDROM_W_OVERREAD_B))'

printf '  %-42s %-10s %-10s\n' "case" "with |" "with +"
printf '  %-42s ' "1. correct single-bit masks"
printf '%-10s ' "$(cell x "$SINGLE" '|')"; printf '%-10s\n' "$(cell x "$SINGLE" '+')"
printf '  %-42s ' "2. E1: FMT aliased onto OVERREAD_B"
printf '%-10s ' "$(cell x "$ALIAS" '|')"; printf '%-10s\n' "$(cell x "$ALIAS" '+')"
printf '  %-42s ' "3. FMT as a MULTI-BIT literal (the gap)"
printf '%-10s ' "$(cell x "$MULTI" '|')"; printf '%-10s\n' "$(cell x "$MULTI" '+')"
echo
echo "  ==> the DELTA is row 3: the cell where the two operators disagree."
echo
echo "ORDELTA_DONE"
