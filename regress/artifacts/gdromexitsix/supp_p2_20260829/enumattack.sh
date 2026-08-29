#!/bin/bash
#  ATTACK THE gdrom_w_masks_disjoint DECLARATION FROM THE ENUM SIDE.
#
#  The shipped controls (assert_controls_20260829/controls.sh) vary ONLY the
#  #define block: gen() hardcodes nine implicit enumerators, so GDROM_W_NBITS is
#  pinned at 9 in every one of the five states.  With NBITS fixed the equality is
#  a genuine pigeonhole -- nine one-bit masks whose OR has nine bits set MUST be
#  distinct.
#
#  This varies the ENUM instead.  An alias written as an explicit enumerator
#  initialiser moves NBITS DOWN in lockstep with the bit it loses, so the
#  equality re-balances.
set -u
T=/tmp/gdromenum
rm -rf "$T"; mkdir -p "$T"

emit_masks_and_assert () {
cat >> "$1" <<'EOF'
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
    ((GDROM_W_LEN | GDROM_W_NODATA | GDROM_W_NOTWAIT | GDROM_W_OVERREAD |
      GDROM_W_DMANODATA | GDROM_W_DMAARM | GDROM_W_TOCLEN | GDROM_W_FMT |
      GDROM_W_CMD) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];
EOF
#  the OTHER shipped assert, so states are tested against BOTH declarations
cat >> "$1" <<'EOF'
struct dreamcast_gdrom_data { unsigned int warned; };
typedef char gdrom_w_fits_its_carriers[
    (GDROM_W_NBITS <= 8 * sizeof(((struct dreamcast_gdrom_data *)0)->warned) &&
     GDROM_W_NBITS <= 8 * sizeof(1u)) ? 1 : -1];
EOF
#  print the two quantities so an ESCAPE is visibly an escape and not a typo
cat >> "$1" <<'EOF'
#include <stdio.h>
int main(void) {
	unsigned int orv = (GDROM_W_LEN | GDROM_W_NODATA | GDROM_W_NOTWAIT |
	    GDROM_W_OVERREAD | GDROM_W_DMANODATA | GDROM_W_DMAARM |
	    GDROM_W_TOCLEN | GDROM_W_FMT | GDROM_W_CMD);
	printf("    NBITS=%d  OR=0x%03x  want=0x%03x  FMT_B=%d TOCLEN_B=%d "
	    "OVERREAD_B=%d CMD_B=%d  FMT==TOCLEN:%d FMT==OVERREAD:%d CMD==FMT:%d\n",
	    GDROM_W_NBITS, orv, (1u << GDROM_W_NBITS) - 1u,
	    GDROM_W_FMT_B, GDROM_W_TOCLEN_B, GDROM_W_OVERREAD_B, GDROM_W_CMD_B,
	    GDROM_W_FMT == GDROM_W_TOCLEN, GDROM_W_FMT == GDROM_W_OVERREAD,
	    GDROM_W_CMD == GDROM_W_FMT);
	return 0;
}
EOF
}

run () {   # $1 label, $2 want, $3 = heredoc-generated enum file
  f="$T/t.c"
  cp "$3" "$f"
  emit_masks_and_assert "$f"
  if gcc -std=gnu99 -pedantic-errors -Wall -Wextra -c "$f" -o "$T/t.o" 2>"$T/err"; then
    got=COMPILES
  else
    got=REFUSED
  fi
  if [ "$got" = "$2" ]; then mark=ok; else mark="*** ESCAPE ***"; fi
  printf '  %-52s want=%-9s got=%-9s %s\n' "$1" "$2" "$got" "$mark"
  if [ "$got" = COMPILES ]; then
    gcc -std=gnu99 "$f" -o "$T/t.exe" 2>/dev/null && "$T/t.exe"
  else
    grep -m1 "error:" "$T/err" | sed 's|^.*error:|      refusal: |'
  fi
}

# ---- S0: the shipped enum, verbatim ----
cat > "$T/e0" <<'EOF'
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
EOF

# ---- S1: E1's SEMANTIC (FMT aliased onto OVERREAD) spelled in the ENUM ----
cat > "$T/e1" <<'EOF'
enum {
	GDROM_W_LEN_B,
	GDROM_W_NODATA_B,
	GDROM_W_NOTWAIT_B,
	GDROM_W_OVERREAD_B,
	GDROM_W_FMT_B = GDROM_W_OVERREAD_B,
	GDROM_W_DMANODATA_B,
	GDROM_W_DMAARM_B,
	GDROM_W_TOCLEN_B,
	GDROM_W_CMD_B,
	GDROM_W_NBITS
};
EOF

# ---- S2: Ma_toclen's SEMANTIC (FMT aliased onto TOCLEN) in the ENUM ----
cat > "$T/e2" <<'EOF'
enum {
	GDROM_W_LEN_B,
	GDROM_W_NODATA_B,
	GDROM_W_NOTWAIT_B,
	GDROM_W_OVERREAD_B,
	GDROM_W_DMANODATA_B,
	GDROM_W_DMAARM_B,
	GDROM_W_TOCLEN_B,
	GDROM_W_FMT_B = GDROM_W_TOCLEN_B,
	GDROM_W_CMD_B,
	GDROM_W_NBITS
};
EOF

# ---- S3: M3shared's SEMANTIC (CMD shares FMT's bit) in the ENUM ----
cat > "$T/e3" <<'EOF'
enum {
	GDROM_W_LEN_B,
	GDROM_W_NODATA_B,
	GDROM_W_NOTWAIT_B,
	GDROM_W_OVERREAD_B,
	GDROM_W_DMANODATA_B,
	GDROM_W_DMAARM_B,
	GDROM_W_TOCLEN_B,
	GDROM_W_FMT_B,
	GDROM_W_CMD_B = GDROM_W_FMT_B,
	GDROM_W_NBITS
};
EOF

# ---- S4: NEGATIVE CONTROL -- explicit values, NBITS pinned, CMD typo'd onto FMT ----
cat > "$T/e4" <<'EOF'
enum {
	GDROM_W_LEN_B = 0,
	GDROM_W_NODATA_B = 1,
	GDROM_W_NOTWAIT_B = 2,
	GDROM_W_OVERREAD_B = 3,
	GDROM_W_DMANODATA_B = 4,
	GDROM_W_DMAARM_B = 5,
	GDROM_W_TOCLEN_B = 6,
	GDROM_W_FMT_B = 7,
	GDROM_W_CMD_B = 7,
	GDROM_W_NBITS = 9
};
EOF

# ---- S5: a bit added at the FRONT and NOT added to the OR list ----
cat > "$T/e5" <<'EOF'
enum {
	GDROM_W_NEWBIT_B,
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
EOF

echo "=== ENUM-SIDE ATTACK ON gdrom_w_masks_disjoint ==="
echo "    (the shipped controls vary only the #define block; NBITS is pinned at 9 there)"
echo
run "S0. shipped enum, verbatim"                        COMPILES "$T/e0"
run "S1. E1 semantic in the ENUM: FMT_B = OVERREAD_B"   REFUSED  "$T/e1"
run "S2. Ma_toclen semantic:      FMT_B = TOCLEN_B"     REFUSED  "$T/e2"
run "S3. M3shared semantic:       CMD_B = FMT_B"        REFUSED  "$T/e3"
run "S4. explicit values, NBITS pinned 9, CMD typo 7"   REFUSED  "$T/e4"
run "S5. new bit at FRONT, omitted from the OR list"    REFUSED  "$T/e5"
echo


# ---- S6: a tenth bit at the BACK, omitted from the OR list ----
#  This is the shipped comment's own fails-closed claim, worded literally:
#  "add a tenth bit without extending the OR below and the file stops compiling".
cat > "$T/e6" <<'EOF'
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
	GDROM_W_TENTH_B,
	GDROM_W_NBITS
};
EOF
run "S6. tenth bit at BACK, omitted from the OR list"   REFUSED  "$T/e6"
echo
echo "ENUMATTACK2_DONE"
