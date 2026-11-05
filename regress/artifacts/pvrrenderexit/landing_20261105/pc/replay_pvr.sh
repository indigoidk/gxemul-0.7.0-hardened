#!/bin/bash
set -u
. "$LIBSH"
PVRLOG=$LOGDIR/pvr_zwrite.log
cp "$SRCLOG" "$PVRLOG"   # REPLAY: the probe call replaced by a banked log
if ! grep -q "PVR_ZWRITE_PROBE_DONE" "$PVRLOG"; then
    check "pvr zwrite probe completed" "no" "yes"
else
    check "pvr zwrite probe completed" "yes" "yes"
    check "pvr zwrite sentinel once" "$(grep -c '^PVR_ZWRITE_PROBE_DONE$' "$PVRLOG")" "1"
    pzres=$(sed -n 's/^PVR_ZWRITE_RESULT=//p' "$PVRLOG")
    check "pvr_zwrite rows run"     "${pzres#*/}" 148
    check "pvr_zwrite rows correct" "${pzres%/*}" "148"
    check "pvr zwrite controls" "$(grep -c '^PVR_ZWRITE_CONTROL=OK$' "$PVRLOG")" "1"
    check "pvr zwrite symptom absent" "$(grep -c '^PVR_ZWRITE_SYMPTOM=ABSENT$' "$PVRLOG")" "1"
    for v in "neg apparatus" "id session" "id r8" "zon session" "zon rendered" "zon prompt" "zoff rendered" "zoff session" "zoff prompt" "ovoff session" "ovoff overlap" "ovoff t2 only" "ovoff t1 only" "ovoff bg" "ovon overlap" "ovon t2 only" "ovon t1 only" "ovon bg" "behind session" "behind overlap" "behind t2 only" "behind t1 only" "texoff session" "texoff overlap" "texoff t1 only" "texoff t2 only" "texbeh session" "texbeh overlap" "texbeh t2 only" "texbeh t1 only" "texon overlap" "texon t2 only" "two session" "two overlap" "two t1 only" "two t2 only" "sticky session" "sticky overlap" "sticky t2 only" "edges l in" "edges l out" "edges r in" "edges r out" "edges rspan" "texedges l in" "texedges l out" "texedges r in" "texedges r out" "texedges rspan" "equal overlap" "equal t2 only" "texequal overlap" "texequal t2 only" "yedges t in" "yedges b in" "yedges b out" "yedges swap" "yedges s end" "yedges s past" "texyedges t in" "texyedges b in" "texyedges b out" "texyedges swap" "texyedges s end" "texyedges s past" "mask overlap" "mask t2 only" "mask25 overlap" "swap s before" "swap s tip" "swap vert" "swap frac past" "swap s start" "texswap s before" "texswap s tip" "texswap vert" "ramp l end" "texramp l end" "edges2 l rev" "edges2 r rev" "edges2 l tip" "edges2 x2 tip" "texedges2 l rev" "texedges2 r rev" "texedges2 l tip" "texedges2 x2 tip" "zleft tip" "texzleft tip" "zeq overlap" "texzeq overlap" "maskoff overlap" "maskhi overlap" "zedges l in" "zedges l out" "zedges r in" "zedges r out" "zedges rspan" "zyedges t in" "zyedges b in" "zyedges b out" "zyedges swap" "zyedges s end" "zyedges s past" "zswap s before" "zswap s tip" "zswap vert" "zswap frac past" "zswap s start" "zedges2 l rev" "zedges2 r rev" "zedges2 l tip" "zramp l end" "ztedges l in" "ztedges l out" "ztedges r in" "ztedges r out" "ztedges rspan" "ztyedges t in" "ztyedges b in" "ztyedges b out" "ztyedges swap" "ztyedges s end" "ztyedges s past" "ztswap s before" "ztswap s tip" "ztswap vert" "ztedges2 l rev" "ztedges2 r rev" "ztedges2 l tip" "ztramp l end" "half swap" "half r x1" "half r x2" "zhalf swap" "zhalf r x1" "zhalf r x2" "ramp8 r end" "zramp8 r end" "texramp8 r end" "ztramp8 r end" "ramp8hi r end" "ramp8hi l end" "zramp8hi r end" "zramp8hi l end" "negx n start" "znegx n start" "texnegx n start" "ztnegx n start"; do
        check "pvr zwrite row: $v" "$(count "$PVRLOG" "^$v  .*ok$")" "1"
    done
    check "pvr zwrite rows emitted" "$(( $(count "$PVRLOG" " ok$") + $(count "$PVRLOG" " FAIL$") ))" "148"
    check "pvr zwrite rows green"   "$(count "$PVRLOG" " ok$")"   "148"
    check "pvr zwrite rows red"     "$(count "$PVRLOG" " FAIL$")" "0"
fi
echo "REPLAY_DONE checks=$_checks fails=$_fails"
