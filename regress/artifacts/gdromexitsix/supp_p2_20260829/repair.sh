#!/bin/bash
#  A CANDIDATE REPAIR, MEASURED ACROSS THE WHOLE STATE SET -- both the shipped
#  #define-side states and the new enum-side ones.
#
#  SHIPPED  (S):  OR(9 terms) == (1u << GDROM_W_NBITS) - 1u
#  CANDIDATE(A):  SUM(9 terms) == OR(9 terms)
#
#  For one-bit masks SUM >= OR always, with equality iff pairwise disjoint --
#  and SUM/OR are computed from the SAME nine terms, so neither side moves when
#  the enum re-numbers.  That is the anchor the shipped form lacks.
set -u
T=/tmp/gdromrepair
rm -rf "$T"; mkdir -p "$T"

MASKS='#define	GDROM_W_LEN		(1u << FMTLEN_X)
#define	GDROM_W_NODATA		(1u << GDROM_W_NODATA_B)
#define	GDROM_W_NOTWAIT		(1u << GDROM_W_NOTWAIT_B)
#define	GDROM_W_OVERREAD	(1u << GDROM_W_OVERREAD_B)
#define	GDROM_W_DMANODATA	(1u << GDROM_W_DMANODATA_B)
#define	GDROM_W_DMAARM		(1u << GDROM_W_DMAARM_B)
#define	GDROM_W_TOCLEN		(1u << GDROM_W_TOCLEN_B)'

build () {   # $1 outfile, $2 enumfile, $3 fmtbit, $4 cmdbit, $5 which assert(S|A|BOTH)
  cp "$2" "$1"
  cat >> "$1" <<EOF
#define	GDROM_W_LEN		(1u << GDROM_W_LEN_B)
#define	GDROM_W_NODATA		(1u << GDROM_W_NODATA_B)
#define	GDROM_W_NOTWAIT		(1u << GDROM_W_NOTWAIT_B)
#define	GDROM_W_OVERREAD	(1u << GDROM_W_OVERREAD_B)
#define	GDROM_W_DMANODATA	(1u << GDROM_W_DMANODATA_B)
#define	GDROM_W_DMAARM		(1u << GDROM_W_DMAARM_B)
#define	GDROM_W_TOCLEN		(1u << GDROM_W_TOCLEN_B)
#define	GDROM_W_FMT		(1u << $3)
#define	GDROM_W_CMD		(1u << $4)
EOF
  case "$5" in
   S|BOTH) cat >> "$1" <<'EOF'
typedef char gdrom_w_masks_disjoint[
    ((GDROM_W_LEN | GDROM_W_NODATA | GDROM_W_NOTWAIT | GDROM_W_OVERREAD |
      GDROM_W_DMANODATA | GDROM_W_DMAARM | GDROM_W_TOCLEN | GDROM_W_FMT |
      GDROM_W_CMD) == ((1u << GDROM_W_NBITS) - 1u)) ? 1 : -1];
EOF
  ;; esac
  case "$5" in
   A|BOTH) cat >> "$1" <<'EOF'
typedef char gdrom_w_masks_pairwise[
    ((GDROM_W_LEN + GDROM_W_NODATA + GDROM_W_NOTWAIT + GDROM_W_OVERREAD +
      GDROM_W_DMANODATA + GDROM_W_DMAARM + GDROM_W_TOCLEN + GDROM_W_FMT +
      GDROM_W_CMD) ==
     (GDROM_W_LEN | GDROM_W_NODATA | GDROM_W_NOTWAIT | GDROM_W_OVERREAD |
      GDROM_W_DMANODATA | GDROM_W_DMAARM | GDROM_W_TOCLEN | GDROM_W_FMT |
      GDROM_W_CMD)) ? 1 : -1];
EOF
  ;; esac
  echo 'int main(void) { return 0; }' >> "$1"
}

score () {  # $1 label, $2 wantS, $3 wantA, $4 enumfile, $5 fmtbit, $6 cmdbit
  for w in S A; do
    build "$T/t_$w.c" "$4" "$5" "$6" "$w"
    if gcc -std=gnu99 -pedantic-errors -Wall -Wextra -c "$T/t_$w.c" -o "$T/t.o" 2>"$T/e_$w"; then
      eval "got_$w=COMPILES"
    else
      eval "got_$w=REFUSED"
    fi
  done
  mS=ok; mA=ok
  [ "$got_S" = "$2" ] || mS="ESCAPE"
  [ "$got_A" = "$3" ] || mA="ESCAPE"
  printf '  %-46s  shipped:%-9s %-7s   candidate:%-9s %s\n' "$1" "$got_S" "$mS" "$got_A" "$mA"
}

cat > "$T/e0" <<'EOF'
enum { GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B, GDROM_W_OVERREAD_B,
       GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, GDROM_W_TOCLEN_B,
       GDROM_W_FMT_B, GDROM_W_CMD_B, GDROM_W_NBITS };
EOF
cat > "$T/e1" <<'EOF'
enum { GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B, GDROM_W_OVERREAD_B,
       GDROM_W_FMT_B = GDROM_W_OVERREAD_B,
       GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, GDROM_W_TOCLEN_B,
       GDROM_W_CMD_B, GDROM_W_NBITS };
EOF
cat > "$T/e2" <<'EOF'
enum { GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B, GDROM_W_OVERREAD_B,
       GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, GDROM_W_TOCLEN_B,
       GDROM_W_FMT_B = GDROM_W_TOCLEN_B, GDROM_W_CMD_B, GDROM_W_NBITS };
EOF
cat > "$T/e3" <<'EOF'
enum { GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B, GDROM_W_OVERREAD_B,
       GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, GDROM_W_TOCLEN_B,
       GDROM_W_FMT_B, GDROM_W_CMD_B = GDROM_W_FMT_B, GDROM_W_NBITS };
EOF
cat > "$T/e5" <<'EOF'
enum { GDROM_W_NEWBIT_B, GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B,
       GDROM_W_OVERREAD_B, GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B,
       GDROM_W_TOCLEN_B, GDROM_W_FMT_B, GDROM_W_CMD_B, GDROM_W_NBITS };
EOF

echo "=== SHIPPED  vs  CANDIDATE(sum==or), ELEVEN STATES ==="
echo "     want: COMPILES only for the two correct states; REFUSED for every alias"
echo
echo "  -- #define-side states (the five shipped controls) --"
score "C0. correct source"                       COMPILES COMPILES "$T/e0" GDROM_W_FMT_B      GDROM_W_CMD_B
score "C1. E1  #define FMT -> OVERREAD_B"        REFUSED  REFUSED  "$T/e0" GDROM_W_OVERREAD_B GDROM_W_CMD_B
score "C2. Ma  #define FMT -> TOCLEN_B"          REFUSED  REFUSED  "$T/e0" GDROM_W_TOCLEN_B   GDROM_W_CMD_B
score "C3. M3s #define CMD -> FMT_B"             REFUSED  REFUSED  "$T/e0" GDROM_W_FMT_B      GDROM_W_FMT_B
echo
echo "  -- ENUM-side states (NEW: NBITS moves in lockstep) --"
score "S1. enum FMT_B = OVERREAD_B"              REFUSED  REFUSED  "$T/e1" GDROM_W_FMT_B      GDROM_W_CMD_B
score "S2. enum FMT_B = TOCLEN_B"                REFUSED  REFUSED  "$T/e2" GDROM_W_FMT_B      GDROM_W_CMD_B
score "S3. enum CMD_B = FMT_B"                   REFUSED  REFUSED  "$T/e3" GDROM_W_FMT_B      GDROM_W_CMD_B
echo
echo "  -- RANGE/COMPLETENESS states: does the candidate REPLACE or COMPLEMENT? --"
score "S5. new bit at FRONT, omitted from OR"    REFUSED  COMPILES "$T/e5" GDROM_W_FMT_B      GDROM_W_CMD_B
score "S6. FMT shifted OUT of range (1u<<20)"    REFUSED  COMPILES "$T/e0" 20                 GDROM_W_CMD_B
echo
echo "REPAIR_DONE"
