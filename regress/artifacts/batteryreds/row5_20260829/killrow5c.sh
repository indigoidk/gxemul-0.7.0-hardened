#!/bin/bash
#  ROW 5 KILL TABLE, TAKE 3.
#
#  *** TAKE 2's M1 AND M2 BUILT DIFFERENT MUTANTS THAN THEY WERE LABELLED, and
#  the SCORE was the tell. ***  Found by the fable5 seat on pass 2.
#
#  M1 claimed "delete a guard PAIR" and its sed looked for a one-line
#  `if (!d->warned_data_unexpected) {`.  The real guard is SPLIT:
#      1335:     !d->warned_data_unexpected) {
#  so only the SET line was deleted -- a true pair deletion reads 5/5, and the
#  table showed 5/6.  M2 claimed a gut-plus-prose mutant on a live guard; the
#  real guard is `if (len != 1 && !d->warned_nonbyte_read) {` at :1823, so its
#  substitution matched nothing and the "prose" half was never exercised.
#
#  The old `vac()` guard only caught TOTAL no-ops: when ONE of two seds fires,
#  cmp differs and the row passes while measuring something else.  This version
#  checks EVERY pattern it intends to change, and refuses the row otherwise.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SRC="$SEC/src/devices/dev_wdc.c"
CEN="$SEC/regress/wdc_latch_census.py"
W=/tmp/row5c
rm -rf "$W"; mkdir -p "$W"
WANT="6/6/6/11"

score () {
	local o
	o=$(python3 "$CEN" "$1" 2>/dev/null)
	printf '%s/%s/%s/%s' \
	  "$(printf '%s\n' "$o" | grep -oE 'WDC_LATCH_SET=[0-9]+'      | cut -d= -f2)" \
	  "$(printf '%s\n' "$o" | grep -oE 'WDC_LATCH_READ=[0-9]+'     | cut -d= -f2)" \
	  "$(printf '%s\n' "$o" | grep -oE 'WDC_LATCH_BALANCED=[0-9]+' | cut -d= -f2)" \
	  "$(printf '%s\n' "$o" | grep -oE 'WDC_LATCH_DECL=[0-9]+'     | cut -d= -f2)"
}

#  want_delta <file> <pattern> <expected-count-in-mutant>
#  Refuse to score a mutant whose intended edit did not land.
want_delta () {
	local n; n=$(grep -cE "$2" "$1")
	if [ "$n" != "$3" ]; then
		printf '  %-46s *** PATTERN CHECK FAILED: %s is %s, want %s -- ROW REFUSED ***\n' "$4" "$2" "$n" "$3"
		return 1
	fi
	return 0
}

row () {
	local got v
	if [ ! -f "$2" ]; then got="(no file)"; else got=$(score "$2"); fi
	if [ "$3" = yes ]; then [ "$got" = "$WANT" ] && v="*** ESCAPED ***" || v="killed"
	else [ "$got" = "$WANT" ] && v="ok" || v="*** FALSE POSITIVE ***"; fi
	printf '  %-46s %-14s %s\n' "$1" "$got" "$v"
}

echo "=== ROW 5 KILL TABLE 3  (want $WANT for BASE only) ==="
cp "$SRC" "$W/base.c"; row "BASE  unmodified HEAD" "$W/base.c" no

# ---- M1 REBUILT: delete a real guard PAIR, on a SINGLE-LINE-guard latch -----
#  inbuf_overread's guard IS one line, so a pair deletion is expressible.
sed '/if (!d->warned_inbuf_overread) {/d; /d->warned_inbuf_overread = 1;/d' "$SRC" > "$W/m1.c"
if want_delta "$W/m1.c" 'd->warned_inbuf_overread' 0 "M1 delete a real guard PAIR" ; then
	row "M1 delete a real guard PAIR (set+read gone)" "$W/m1.c" yes
fi

# ---- M2 REBUILT: gut the REAL :1823 guard, keep its SET, add prose ----------
sed 's|!d->warned_nonbyte_read) {|0) { /* !d->warned_nonbyte_read !d->warned_nonbyte_read */|' "$SRC" > "$W/m2.c"
if want_delta "$W/m2.c" '!d->warned_nonbyte_read' 2 "M2 gut the REAL guard + name it twice in prose" ; then
	row "M2 gut REAL guard, SET kept, 2 prose mentions" "$W/m2.c" yes
fi

# ---- the pass-2 escapes ----------------------------------------------------
awk 'NR==246 {sub(/if \(!d->warned_inbuf_overrun\) \{/, "if (1) {")} {print}' "$SRC" > "$W/e1.c"
want_delta "$W/e1.c" 'if \(1\) \{' 1 "E1" && row "E1 neutralise 1 of 2 sites (one token)" "$W/e1.c" yes
awk 'NR==515 {sub(/if \(!d->warned_inbuf_overrun\) \{/, "if (1) {")} {print}' "$SRC" > "$W/e2.c"
want_delta "$W/e2.c" 'if \(1\) \{' 1 "E2" && row "E2 neutralise the OTHER site" "$W/e2.c" yes
awk 'NR==246 {sub(/warned_inbuf_overrun/, "warned_inbuf_overread")} {print}' "$SRC" > "$W/e3.c"
want_delta "$W/e3.c" '!d->warned_inbuf_overread' 2 "E3" && row "E3 redirect guard to another latch" "$W/e3.c" yes
D=$(grep -nE 'warned_null_xfer;' "$SRC" | head -1 | cut -d: -f1)
awk -v L="$D" 'NR==L {print; print "\tint\t\twarned_brand_new;"; next} {print}' "$SRC" > "$W/e7.c"
want_delta "$W/e7.c" 'warned_brand_new' 1 "E7" && row "E7 declare a 12th latch" "$W/e7.c" yes
sed 's|!d->warned_nonbyte_read)|!d->warned_nonbyte_read_hi)|' "$SRC" > "$W/e8.c"
want_delta "$W/e8.c" 'warned_nonbyte_read_hi' 1 "E8" && row "E8 READ redirected to a LONGER name" "$W/e8.c" yes
awk 'NR==247 {print "\t\t\t// see note \\"; print; next} {print}' "$SRC" > "$W/e6.c"
want_delta "$W/e6.c" '// see note' 1 "E6" && row "E6 C99 // continuation swallows a SET" "$W/e6.c" yes

# ---- M4 / M3 / M5 ----------------------------------------------------------
sed 's|d->warned_nonbyte_write = 1;||' "$SRC" > "$W/m4.c"
want_delta "$W/m4.c" 'd->warned_nonbyte_write = 1;' 0 "M4" && row "M4 delete the SET only" "$W/m4.c" yes
printf '/*\n * comment-only, naming d->warned_inbuf_overrun in prose\n */\n' > "$W/m3.c"
row "M3 NULL MEDIUM (comment-only file)" "$W/m3.c" yes
row "M5 absent file" "$W/nosuch.c" yes

rm -rf "$W"
echo
echo "KILLROW5C_DONE"
