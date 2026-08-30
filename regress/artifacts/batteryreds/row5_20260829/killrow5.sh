#!/bin/bash
#  ROW 5 KILL TABLE.  The bare floor was MEASURED VACUOUS; this form must be
#  measured too, against the same mutants, or it is an assertion.
#
#  Mutants, all applied to a SCRATCH copy -- no project tree is written:
#    M1  delete one latch's two-line guard pair   (the floor PASSED this at 13)
#    M2  gut a guard, name the latch twice in a COMMENT (floor PASSED at 15)
#    M3  null medium: comment-only file           (floor clause (c))
#    M4  the OTHER half: delete a SET, keep TWO READS -- the shape that refutes
#        a per-latch `>= 2`, which was the competing design
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
W=/tmp/row5kill
rm -rf "$W"; mkdir -p "$W"
SRC="$SEC/src/devices/dev_wdc.c"
CEN="$SEC/regress/wdc_latch_census.py"

score () {   # $1 = file ; prints "SET/READ"
	local o s r
	o=$(python3 "$CEN" "$1" 2>/dev/null)
	s=$(printf '%s\n' "$o" | grep -oE 'WDC_LATCH_SET=[0-9]+' | cut -d= -f2)
	r=$(printf '%s\n' "$o" | grep -oE 'WDC_LATCH_READ=[0-9]+' | cut -d= -f2)
	printf '%s/%s' "${s:-?}" "${r:-?}"
}

row () {   # $1 = label, $2 = file, $3 = want-kill(yes/no)
	local got verdict
	got=$(score "$2")
	if [ "$3" = yes ]; then
		[ "$got" = "6/6" ] && verdict="*** ESCAPED ***" || verdict="killed"
	else
		[ "$got" = "6/6" ] && verdict="ok" || verdict="*** FALSE POSITIVE ***"
	fi
	printf '  %-46s %-8s %s\n' "$1" "$got" "$verdict"
}

echo "=== ROW 5 KILL TABLE (want 6/6 only for BASE) ==="
cp "$SRC" "$W/base.c"
row "BASE  unmodified HEAD" "$W/base.c" no

#  M1 -- delete one latch's guard pair.  The floor scored 13 and PASSED.
sed '/if (!d->warned_data_unexpected) {/d; /d->warned_data_unexpected = 1;/d' \
    "$SRC" > "$W/m1.c"
if cmp -s "$W/m1.c" "$SRC"; then echo "  *** M1 SED MATCHED NOTHING -- row vacuous ***"; fi
row "M1  delete data_unexpected guard pair" "$W/m1.c" yes

#  M2 -- gut the guard, then name the latch twice in a COMMENT.  The floor
#  scored 15 and PASSED; a raw grep cannot tell prose from code.
sed 's|if (!d->warned_nonbyte_read) {|if (1) { /* d->warned_nonbyte_read d->warned_nonbyte_read = 1; */|; s|d->warned_nonbyte_read = 1;||' \
    "$SRC" > "$W/m2.c"
if cmp -s "$W/m2.c" "$SRC"; then echo "  *** M2 SED MATCHED NOTHING -- row vacuous ***"; fi
row "M2  gut guard + name it twice in a comment" "$W/m2.c" yes

#  M4 -- delete only the SET, keep the reads.  This is what refutes a per-latch
#  `>= 2`, the competing design: two reads and no set satisfies >= 2.
sed 's|d->warned_nonbyte_write = 1;||' "$SRC" > "$W/m4.c"
if cmp -s "$W/m4.c" "$SRC"; then echo "  *** M4 SED MATCHED NOTHING -- row vacuous ***"; fi
row "M4  delete the SET only, keep the READ" "$W/m4.c" yes

#  M3 -- null medium.  Floor clause (c).
printf '/*\n * a comment-only file naming d->warned_inbuf_overrun and\n * d->warned_unimpl_cmd = 1; in prose only\n */\n' > "$W/m3.c"
row "M3  NULL MEDIUM (comment-only file)" "$W/m3.c" yes

#  M5 -- a file that does not exist.  MISSING and EMPTY must not render alike.
row "M5  absent file (must not look like 0 latches)" "$W/nosuch.c" yes
echo -n "     and it says which: "
python3 "$CEN" "$W/nosuch.c" 2>/dev/null | grep -oE 'WDC_LATCH_FILE=[A-Z]+'

rm -rf "$W"
echo
echo "KILLROW5_DONE"
