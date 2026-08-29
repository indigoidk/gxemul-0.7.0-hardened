#!/bin/bash
#  codex's escape: alias the ENUMERATOR, not the mask.
#      GDROM_W_CMD_B = GDROM_W_FMT_B
#  Both masks then use bit 7, and NBITS collapses from 9 to 8, so the RHS
#  shrinks with it.  Does that escape `|`?  Does it escape `+`?
set -u
T=/tmp/enumalias
rm -rf "$T"; mkdir -p "$T"

gen () {  # $1 out, $2 CMD_B decl, $3 operator
cat > "$1" <<EOF
enum {
	GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B, GDROM_W_OVERREAD_B,
	GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, GDROM_W_TOCLEN_B,
	GDROM_W_FMT_B, $2 GDROM_W_NBITS
};
#define	GDROM_W_LEN		(1u << GDROM_W_LEN_B)
#define	GDROM_W_NODATA		(1u << GDROM_W_NODATA_B)
#define	GDROM_W_NOTWAIT		(1u << GDROM_W_NOTWAIT_B)
#define	GDROM_W_OVERREAD	(1u << GDROM_W_OVERREAD_B)
#define	GDROM_W_DMANODATA	(1u << GDROM_W_DMANODATA_B)
#define	GDROM_W_DMAARM		(1u << GDROM_W_DMAARM_B)
#define	GDROM_W_TOCLEN		(1u << GDROM_W_TOCLEN_B)
#define	GDROM_W_FMT		(1u << GDROM_W_FMT_B)
#define	GDROM_W_CMD		(1u << GDROM_W_CMD_B)
typedef char gdrom_w_masks_disjoint[
    ((GDROM_W_LEN $3 GDROM_W_NODATA $3 GDROM_W_NOTWAIT $3 GDROM_W_OVERREAD $3
      GDROM_W_DMANODATA $3 GDROM_W_DMAARM $3 GDROM_W_TOCLEN $3 GDROM_W_FMT $3
      GDROM_W_CMD) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];
int main(void) { return 0; }
EOF
}

cell () { gen "$T/t.c" "$1" "$2"
  if gcc -std=gnu99 -c "$T/t.c" -o "$T/t.o" 2>/dev/null; then echo -n "COMPILES"; else echo -n "REFUSED "; fi; }

NORMAL='GDROM_W_CMD_B,'
ALIASED='GDROM_W_CMD_B = GDROM_W_FMT_B,'

printf '  %-46s %-10s %-10s\n' "case" "with |" "with +"
printf '  %-46s %-10s %-10s\n' "1. normal enum"           "$(cell "$NORMAL" '|')"  "$(cell "$NORMAL" '+')"
printf '  %-46s %-10s %-10s\n' "2. codex: ENUMERATOR aliased" "$(cell "$ALIASED" '|')" "$(cell "$ALIASED" '+')"
echo
echo "  the arithmetic, so the result is explicable rather than just observed:"
echo "    aliased  -> both FMT and CMD are bit 7, and NBITS collapses 9 -> 8"
echo "    with |   -> OR  = 0xff        RHS = (1<<8)-1 = 0xff   EQUAL   -> escapes"
echo "    with +   -> SUM = 1+2+4+8+16+32+64+128+128 = 383   RHS = 255  -> caught"
echo
echo "=== the OTHER thing codex found: 1u << NBITS at NBITS == 32 ==="
cat > "$T/w.c" <<'EOF'
int main(void) { unsigned x = (1u << 32) - 1u; return (int)x; }
EOF
gcc -std=gnu99 -c "$T/w.c" -o "$T/w.o" 2>&1 | head -3 | sed 's/^/    /'
echo "    (a diagnostic above = it fails LOUDLY rather than silently miscomputing)"
echo
echo "ENUMALIAS_DONE"
