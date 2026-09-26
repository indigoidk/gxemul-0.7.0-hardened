set -u
cd /tmp/opus550p2 || exit 1
tr -d '\r' < exp/regress/gate_offline.sh > goff.lf
tr -d '\r' < exp/regress/gate_asan_sweep.sh > asan.lf
{ sed -n '/^exempt_expired () {/,/^}/p' goff.lf
  grep -E '^SC_EXEMPT=|^SM_EXEMPT=' goff.lf
  sed -n '/^AB_EXEMPT="/,/^"/p' asan.lf
} > lists.sh
cat >> lists.sh <<'EOS'
echo "SC_EXEMPT=$SC_EXEMPT"; echo "SM_EXEMPT=$SM_EXEMPT"
d=2026-09-25; prevsc=none; prevab=none
while [ "$d" \< "2027-01-01" ]; do
  sc=$(exempt_expired $d $SC_EXEMPT); ab=$(exempt_expired $d $AB_EXEMPT); sm=$(exempt_expired $d $SM_EXEMPT)
  if [ "$sc" != "$prevsc" ] || [ "$ab" != "$prevab" ]; then
    echo "$d $(date -d $d +%a)  SC:${sc}  AB:$(echo $ab | wc -w | sed 's/^/n=/')  SM:${sm}"
  fi
  prevsc=$sc; prevab=$ab; d=$(date -d "$d + 1 day" +%F)
done
EOS
bash lists.sh
