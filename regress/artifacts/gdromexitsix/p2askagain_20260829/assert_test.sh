#!/bin/bash
#  Controls for the PROPOSED mask-disjointness assert.  Uses the file's OWN idiom
#  (negative-size typedef, as gdrom_w_fits_its_carriers at dev_dreamcast_gdrom.c).
#  Four states, including the two NEGATIVE ones.
set -u
D=/tmp/gxassert490
rm -rf "$D"; mkdir -p "$D"

hdr () {
cat <<'EOF'
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
#define	GDROM_W_LEN	(1u << GDROM_W_LEN_B)
#define	GDROM_W_NODATA	(1u << GDROM_W_NODATA_B)
#define	GDROM_W_NOTWAIT	(1u << GDROM_W_NOTWAIT_B)
#define	GDROM_W_OVERREAD	(1u << GDROM_W_OVERREAD_B)
#define	GDROM_W_DMANODATA	(1u << GDROM_W_DMANODATA_B)
#define	GDROM_W_DMAARM	(1u << GDROM_W_DMAARM_B)
#define	GDROM_W_TOCLEN	(1u << GDROM_W_TOCLEN_B)
EOF
}

assert () {
cat <<'EOF'
typedef char gdrom_w_masks_disjoint[
    ((GDROM_W_LEN | GDROM_W_NODATA | GDROM_W_NOTWAIT | GDROM_W_OVERREAD
      | GDROM_W_DMANODATA | GDROM_W_DMAARM | GDROM_W_TOCLEN | GDROM_W_FMT
      | GDROM_W_CMD) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];
int main(void) { return 0; }
EOF
}

#  STATE 1 -- shipped masks.  MUST COMPILE.
{ hdr; echo '#define	GDROM_W_FMT	(1u << GDROM_W_FMT_B)';
        echo '#define	GDROM_W_CMD	(1u << GDROM_W_CMD_B)'; assert; } > "$D/s1_correct.c"

#  STATE 2 -- E1's measured escape.  MUST FAIL.
{ hdr; echo '#define	GDROM_W_FMT	(1u << GDROM_W_OVERREAD_B)';
        echo '#define	GDROM_W_CMD	(1u << GDROM_W_CMD_B)'; assert; } > "$D/s2_E1alias.c"

#  STATE 3 -- Ma_toclen's shape (alias onto TOCLEN).  MUST FAIL.
{ hdr; echo '#define	GDROM_W_FMT	(1u << GDROM_W_TOCLEN_B)';
        echo '#define	GDROM_W_CMD	(1u << GDROM_W_CMD_B)'; assert; } > "$D/s3_Matoclen.c"

#  STATE 4 -- M3shared's shape (both sites one bit).  MUST FAIL.
{ hdr; echo '#define	GDROM_W_FMT	(1u << GDROM_W_FMT_B)';
        echo '#define	GDROM_W_CMD	(1u << GDROM_W_FMT_B)'; assert; } > "$D/s4_M3shared.c"

#  STATE 5 -- the WITHOUT-assert control: E1's alias must compile CLEAN with no assert,
#  which is what makes the escape possible in the first place.
{ hdr; echo '#define	GDROM_W_FMT	(1u << GDROM_W_OVERREAD_B)';
        echo '#define	GDROM_W_CMD	(1u << GDROM_W_CMD_B)';
        echo 'int main(void) { return 0; }'; } > "$D/s5_E1_noassert.c"

for f in s1_correct s2_E1alias s3_Matoclen s4_M3shared s5_E1_noassert; do
    if gcc -std=c99 -pedantic-errors -Wall -Wextra -o "$D/$f.out" "$D/$f.c" 2>"$D/$f.err"; then
        printf "%-18s COMPILES\n" "$f"
    else
        printf "%-18s REFUSED  -- %s\n" "$f" "$(grep -m1 -o 'size of array .* is negative\|error: .*' "$D/$f.err" | head -1)"
    fi
done
echo "ASSERTTEST_DONE"
