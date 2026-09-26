exempt_expired () {          # exempt_expired <today> <entries...>
    local today="$1"; shift
    local out="" e d
    for e in "$@"; do
        case "$e" in
            *:*) ;;
            *) out="$out $e(NO-DATE)"; continue ;;
        esac
        d=${e##*:}
        case "$d" in
            [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;;
            *) out="$out ${e%%:*}(BAD-DATE:${d:-empty})"; continue ;;
        esac
        [ "$d" \< "$today" ] && out="$out ${e%%:*}"
    done
    printf '%s' "${out:-none}"
}
SM_EXEMPT="ieee_store:2099-01-01"   # #537: fbpending_bound moved to SM_COVERED
SC_EXEMPT="ieee_store:2026-12-10 wdc_identify:2026-09-27"
AB_EXEMPT="
    alpha/3000/300:2026-11-30
    decstation/3maxplus:2026-11-30
    decstation/maxine:2026-11-30
    decstation/5400:2026-11-30
    decstation/5500:2026-11-30
    mvmeppc/mvme1600:2026-11-30
    mvmeppc/mvme2100:2026-11-30
    sgi/ip19:2026-11-30
    sgi/ip20:2026-11-30
    sgi/ip22:2026-11-30
    sgi/ip24:2026-11-30
    sgi/ip27:2026-11-30
"
echo "SC_EXEMPT=$SC_EXEMPT"; echo "SM_EXEMPT=$SM_EXEMPT"
d=2026-09-25; prevsc=none; prevab=none
while [ "$d" \< "2027-01-01" ]; do
  sc=$(exempt_expired $d $SC_EXEMPT); ab=$(exempt_expired $d $AB_EXEMPT); sm=$(exempt_expired $d $SM_EXEMPT)
  if [ "$sc" != "$prevsc" ] || [ "$ab" != "$prevab" ]; then
    echo "$d $(date -d $d +%a)  SC:${sc}  AB:$( [ "$ab" = none ] && echo n=0 || echo "n=$(echo $ab | wc -w)" )  SM:${sm}"
  fi
  prevsc=$sc; prevab=$ab; d=$(date -d "$d + 1 day" +%F)
done
