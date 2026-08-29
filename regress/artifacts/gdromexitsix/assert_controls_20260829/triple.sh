#!/bin/bash
#  kimi's UNMEASURED (6,3) shape: a TRIPLE enum alias.
#      GDROM_W_TOCLEN_B = GDROM_W_OVERREAD_B
#  which drags TOCLEN=OVERREAD, FMT=DMANODATA, CMD=DMAARM in one token.
#
#  kimi measured the COMPILE half under `|` (it compiles) and named the RUNTIME
#  half as owed, declining to claim it -- correctly, since the decline probe
#  never exercises the OVERREAD/DMANODATA/DMAARM paths before its decline tests.
#  If `+` REFUSES it at compile time, the runtime question never arises.
set -u
T=/tmp/triple
rm -rf "$T"; mkdir -p "$T"

gen () {   # $1 = TOCLEN_B declaration, $2 = operator
cat > "$T/t.c" <<EOF
enum {
	GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B, GDROM_W_OVERREAD_B,
	GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, $1
	GDROM_W_FMT_B, GDROM_W_CMD_B, GDROM_W_NBITS
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
    ((GDROM_W_LEN $2 GDROM_W_NODATA $2 GDROM_W_NOTWAIT $2 GDROM_W_OVERREAD $2
      GDROM_W_DMANODATA $2 GDROM_W_DMAARM $2 GDROM_W_TOCLEN $2 GDROM_W_FMT $2
      GDROM_W_CMD) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];
int main(void) { return 0; }
EOF
}

cell () { gen "$1" "$2"
  if gcc -std=gnu99 -c "$T/t.c" -o "$T/t.o" 2>/dev/null; then echo -n "COMPILES"; else echo -n "REFUSED "; fi; }

N='GDROM_W_TOCLEN_B,'
A='GDROM_W_TOCLEN_B = GDROM_W_OVERREAD_B,'

printf '  %-46s %-10s %-10s\n' "case" "with |" "with +"
printf '  %-46s %-10s %-10s\n' "normal enum"                   "$(cell "$N" '|')" "$(cell "$N" '+')"
printf '  %-46s %-10s %-10s\n' "kimi (6,3): TRIPLE enum alias" "$(cell "$A" '|')" "$(cell "$A" '+')"
echo
echo "  arithmetic: the alias drags THREE pairs together and NBITS collapses 9 -> 6."
echo "    with |  -> OR  = 0x3f            RHS = (1<<6)-1 = 0x3f   EQUAL  -> escapes"
echo "    with +  -> SUM = 1+2+4+8+16+32+8+16+32 = 119   RHS = 63          -> caught"
echo
echo "TRIPLE_DONE"
