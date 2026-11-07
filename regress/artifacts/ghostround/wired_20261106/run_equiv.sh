#!/usr/bin/env bash
# run_equiv.sh INSTALLED PROTOTYPE REPO -- the installed checker against the census prototype
# (regress/artifacts/ghostround/census_20261106/check_ghost_rounds.py), both replaying the same commits read-only
# (`--at=REV`, GXSEC=REPO): 4 revisions x 3 cutoffs x 6 option sets.  The outputs are compared whole, minus the one
# line that names what was read (`  read: ...`), which differs by design.  Ends `EQUIV: N comparisons, M DIFFERENT`.
I=$1; P=$2; REPO=$3
[ -f "$I" ] && [ -f "$P" ] && [ -d "$REPO" ] || { echo "usage: $0 INSTALLED PROTOTYPE REPO"; exit 9; }
n=0; d=0
T=$(mktemp -d)
for rev in 2632277f d9efd339 4cc3952a 2951694f; do
	for cut in 2026-11-05 2026-08-26 2026-09-11; do
		for opts in "" "--list" "--list --scope=all" "--list --rule=date" "--list --rule=date --scope=all" "--list --accept-commits"; do
			GXSEC=$REPO GXGHOST_CUTOFF=$cut python -W ignore "$I" --at=$rev $opts 2>&1 | grep -v '^  read: ' > "$T/i"
			GXSEC=$REPO GXGHOST_CUTOFF=$cut python -W ignore "$P" --at=$rev $opts 2>&1 | grep -v '^  read: ' > "$T/p"
			n=$((n+1))
			tok=$(grep -oE '^GHOST_ROUNDS_(PASS|FAIL|VOID)' "$T/i" | head -1)
			if cmp -s "$T/i" "$T/p"; then v=SAME; else v=DIFFERENT; d=$((d+1)); fi
			printf '%s  %s %-36s %s  (%d lines, %s)\n' "$rev" "$cut" "${opts:-(default)}" "$v" "$(wc -l < "$T/i")" "${tok:-no token}"
		done
	done
done
rm -rf "$T"
echo "EQUIV: $n comparisons, $d DIFFERENT"
