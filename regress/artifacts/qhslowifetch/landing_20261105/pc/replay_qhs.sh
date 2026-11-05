#!/bin/bash
set -u
. "$LIBSH"
IFLOG=$LOGDIR/ppc_ifetch.log
cp "$SRCLOG" "$IFLOG"   # REPLAY: the probe call replaced by a banked log
if [ "$(grep -cx 'PPC_IFETCH_PROBE_DONE' "$IFLOG")" != 1 ]; then
    note "ppc_ifetch: completion sentinel missing or duplicated; last lines follow"
    tail -5 "$IFLOG" | sed 's/^/       /'
    check "ppc_ifetch probe completed" "no" "yes"
else
    check "ppc_ifetch probe completed" "yes" "yes"
    check "ppc_ifetch sentinel is the last line" "$(tail -n 1 "$IFLOG")" "PPC_IFETCH_PROBE_DONE"
    for k in RESULT CONTROL SYMPTOM RED; do
        check "ppc_ifetch $k= lines" "$(grep -c "^PPC_IFETCH_$k=" "$IFLOG")" "1"
    done
    check "ppc_ifetch RESULT=249/249"  "$(grep -cx 'PPC_IFETCH_RESULT=249/249' "$IFLOG")" "1"
    check "ppc_ifetch CONTROL=OK"      "$(grep -cx 'PPC_IFETCH_CONTROL=OK' "$IFLOG")" "1"
    check "ppc_ifetch SYMPTOM=ABSENT"  "$(grep -cx 'PPC_IFETCH_SYMPTOM=ABSENT' "$IFLOG")" "1"
    check "ppc_ifetch RED=none"        "$(grep -cx 'PPC_IFETCH_RED=none' "$IFLOG")" "1"
    for v in "ctl session" "ctl live" "ctl srr0 kept" "neg apparatus" "isi session" "isi srr0" "isi pc" "isi text" "isi nonex" "isi1 session" "isi1 srr0" "isi1 pc" "isi1 nonex" "noT session" "noT pc" "noT srr0 kept" "noT unimpl" "noT chkstop" "T cont session" "T cont text" "T cont prompt" "T cont pc" "T cont srr0" "T cont nonex" "T cont unimpl" "T cont exc" "T cont chkstop" "T cont msr" "T step session" "T step text" "T step prompt" "T step pc" "T step srr0" "T step nonex" "T step unimpl" "T step exc" "T step chkstop" "T step msr" "T me session" "T me pc" "T me srr0" "T me nonex" "T me text" "T me exc" "T me unimpl" "T me chkstop" "T me msr" "again session" "again pc" "again srr0" "again nonex" "again text" "again unimpl" "again exc" "again chkstop" "again prompt" "again msr" "T ra session" "T ra pc" "T ra nonex" "T ra addr" "T ra stopped" "T ra msr" "T ra chkstop" "T ra srr0" "T ra unimpl" "T ra me session" "T ra me pc" "T ra me nonex" "T ra me addr" "T ra me stopped" "T ra me chkstop" "T ra me msr" "T ra me srr0" "T ra me unimpl" "T ra odd session" "T ra odd pc" "T ra odd nonex" "T ra odd addr" "T ra odd stopped" "T ra odd msr" "T ra odd chkstop" "T ra odd srr0" "T ra odd unimpl" "T ra o1m session" "T ra o1m pc" "T ra o1m nonex" "T ra o1m addr" "T ra o1m stopped" "T ra o1m msr" "T ra o1m chkstop" "T ra o1m srr0" "T ra o1m unimpl" "T ra o2 session" "T ra o2 pc" "T ra o2 nonex" "T ra o2 addr" "T ra o2 stopped" "T ra o2 msr" "T ra o2 chkstop" "T ra o2 srr0" "T ra o2 unimpl" "T ra o2m session" "T ra o2m pc" "T ra o2m nonex" "T ra o2m addr" "T ra o2m stopped" "T ra o2m msr" "T ra o2m chkstop" "T ra o2m srr0" "T ra o2m unimpl" "T ra o3 session" "T ra o3 pc" "T ra o3 nonex" "T ra o3 addr" "T ra o3 stopped" "T ra o3 msr" "T ra o3 chkstop" "T ra o3 srr0" "T ra o3 unimpl" "T ra o3m session" "T ra o3m pc" "T ra o3m nonex" "T ra o3m addr" "T ra o3m stopped" "T ra o3m msr" "T ra o3m chkstop" "T ra o3m srr0" "T ra o3m unimpl" "T rp session" "T rp pc" "T rp nonex" "T rp addr" "T rp stopped" "T rp msr" "T rp chkstop" "T rp srr0" "T rp unimpl" "T rp me session" "T rp me pc" "T rp me nonex" "T rp me addr" "T rp me stopped" "T rp me msr" "T rp me chkstop" "T rp me srr0" "T rp me unimpl" "T rp odd session" "T rp odd pc" "T rp odd nonex" "T rp odd addr" "T rp odd stopped" "T rp odd msr" "T rp odd chkstop" "T rp odd srr0" "T rp odd unimpl" "T rp o1m session" "T rp o1m pc" "T rp o1m nonex" "T rp o1m addr" "T rp o1m stopped" "T rp o1m msr" "T rp o1m chkstop" "T rp o1m srr0" "T rp o1m unimpl" "T rp o2 session" "T rp o2 pc" "T rp o2 nonex" "T rp o2 addr" "T rp o2 stopped" "T rp o2 msr" "T rp o2 chkstop" "T rp o2 srr0" "T rp o2 unimpl" "T rp o2m session" "T rp o2m pc" "T rp o2m nonex" "T rp o2m addr" "T rp o2m stopped" "T rp o2m msr" "T rp o2m chkstop" "T rp o2m srr0" "T rp o2m unimpl" "T rp o3 session" "T rp o3 pc" "T rp o3 nonex" "T rp o3 addr" "T rp o3 stopped" "T rp o3 msr" "T rp o3 chkstop" "T rp o3 srr0" "T rp o3 unimpl" "T rp o3m session" "T rp o3m pc" "T rp o3m nonex" "T rp o3m addr" "T rp o3m stopped" "T rp o3m msr" "T rp o3m chkstop" "T rp o3m srr0" "T rp o3m unimpl" "T blr session" "T blr pc" "T blr nonex" "T blr srr0" "T blr msr" "T blr chkstop" "T blr unimpl" "T blr lr" "T blr o1 session" "T blr o1 pc" "T blr o1 nonex" "T blr o1 srr0" "T blr o1 msr" "T blr o1 chkstop" "T blr o1 unimpl" "T blr o1 lr" "T blr o2 session" "T blr o2 pc" "T blr o2 nonex" "T blr o2 srr0" "T blr o2 msr" "T blr o2 chkstop" "T blr o2 unimpl" "T blr o2 lr" "T blr m1 session" "T blr m1 pc" "T blr m1 nonex" "T blr m1 srr0" "T blr m1 msr" "T blr m1 chkstop" "T blr m1 unimpl" "T blr m1 lr" "T blr m2 session" "T blr m2 pc" "T blr m2 nonex" "T blr m2 srr0" "T blr m2 msr" "T blr m2 chkstop" "T blr m2 unimpl" "T blr m2 lr" "T blr m3 session" "T blr m3 pc" "T blr m3 nonex" "T blr m3 srr0" "T blr m3 msr" "T blr m3 chkstop" "T blr m3 unimpl" "T blr m3 lr"; do
        check "ppc_ifetch row: $v" "$(count "$IFLOG" "^$v  .*ok$")" "1"
    done
    ifok=$(count "$IFLOG" " ok$"); ifbad=$(count "$IFLOG" " FAIL$"); ifrun=$((ifok + ifbad))
    check "ppc_ifetch rows run"   "$ifrun" 249
    check "ppc_ifetch rows green" "$ifok" 249
    check "ppc_ifetch rows red"   "$ifbad" 0
fi
echo "REPLAY_DONE checks=$_checks fails=$_fails"
