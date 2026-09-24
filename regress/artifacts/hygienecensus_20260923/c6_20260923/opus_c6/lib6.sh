#!/bin/bash
#  lib6.sh -- the Opus seat's c6 case library, SOURCED by drv6.sh in each shell.  Needs:
#    SRC  SEC's regress/ (read only)     FROZ  c6_frozen/      WORK  this run's work root (created)
#    OUT  output dir (per-step .out)     TAG   W (WSL /tmp) | D (WSL on DrvFs) | G (git-bash)
#    TAB  the result table               GLIST (G only) file collecting trees for the WSL gate pass
EW="ends""with"     # never spell the method with its paren in a file that might be scanned
R1="2026-09-23: owner ruled in chat -- allowlist arm_bdt_probe.py BY NAME (ledger row armbdtreadiness)"
R2="2026-09-23: owner ruled; evidence in regress/artifacts/hygienecensus_20260923/controls_c6d"
R3="2026-09-23: owner ruled; evidence at /c/DocumentNoSnc/cc/GXEMUL/_scratchpad/x.txt"
R4="2026-09-23: owner ruled, table=/regress/artifacts/x kept as evidence"
R5="2026-09-23: owner ruled: sites 3->5 after the arm_bdt:1 and arm_flags:2 review"
R6="2026-09-23: owner's ruling -- 'count all' (50% of sites) #392 & #524 | ok"

master() {   # one pristine copy per run; cases cp -a from it
    M="$WORK/_master"; rm -rf "$M"; mkdir -p "$M/GXEMUL-SEC/regress" "$M/GXEMUL-SEC/tools"
    find "$SRC" -maxdepth 1 -type f -print0 | xargs -0 cp -p -t "$M/GXEMUL-SEC/regress/"
    cp -p "$FROZ/gate_hygiene.sh" "$FROZ/census_tokens.py" "$M/GXEMUL-SEC/regress/"
    cp -p "$FROZ/derive_hygiene_pins.sh" "$M/GXEMUL-SEC/tools/"
    echo "[$TAG] master: $(ls "$M/GXEMUL-SEC/regress" | wc -l) files; deriver $(md5sum "$M/GXEMUL-SEC/tools/derive_hygiene_pins.sh" | cut -c1-8) gate $(md5sum "$M/GXEMUL-SEC/regress/gate_hygiene.sh" | cut -c1-8) tokens $(md5sum "$M/GXEMUL-SEC/regress/census_tokens.py" | cut -c1-8)" >> "$TAB"
}
mk() { local d="$WORK/$1"; rm -rf "$d"; cp -a "$WORK/_master" "$d"; R="$d/GXEMUL-SEC/regress"; D="$d"; }
gfn() { awk 'index($0,"GRANDFATHERED_PROMPTLESS=")==1 {p=1} p {print} p && /"[[:space:]]*$/ && NR>1 && !/^GRANDFATHERED_PROMPTLESS="[^"]*$/ {exit}' "$1" \
        | sed 's/^GRANDFATHERED_PROMPTLESS="//; s/"[[:space:]]*$//' | tr ' ' '\n' | grep -c '\.py$'; }
pins() { local g="$1/GXEMUL-SEC/regress/gate_hygiene.sh"
    PINS="PTY=$(sed -n 's/^EXPECT_PTY_PROBES=//p' "$g" | head -1) CONV=$(sed -n 's/^EXPECT_CONVERTED=//p' "$g" | head -1) WF=$(sed -n 's/^EXPECT_WHOLE_FULL=//p' "$g" | head -1) WFF=[$(sed -n 's/^WHOLE_FULL_FILES="\(.*\)"$/\1/p' "$g" | head -1)] GF=$(gfn "$g") RULINGS=$(grep -c '^#  RULING' "$g") CR=$(tr -cd '\r' < "$g" | wc -c) bash-n=$(bash -n "$g" 2>/dev/null && echo ok || echo BAD)"; }
sect() { sed -n "/^$2/,/^[A-Z]/p" "$1" | grep -E '^  ' | sed 's/^  //' | tr -d '\r' | tr '\n' ' '; }
rep() { local f=$1
    REP="PTY $(awk '$1=="EXPECT_PTY_PROBES"{print $2"/"$3}' "$f" | tr -d '\r') PL $(awk '/^promptless vs GRANDFATHERED/{print $(NF-1)"/"$NF}' "$f" | tr -d '\r') CONV $(awk '/^EXPECT_CONVERTED \(/{printf "%s,", $(NF-1)}' "$f" | tr -d '\r')/$(awk '/^EXPECT_CONVERTED \(anchor/{print $NF}' "$f" | tr -d '\r') WF $(awk '$1=="EXPECT_WHOLE_FULL"{print $2"/"$3}' "$f" | tr -d '\r') WFFgot[$(sed -n 's/^WHOLE_FULL_FILES *got *\[\(.*\)\]$/\1/p' "$f" | tr -d '\r')] NEW[$(sect "$f" 'NEW PROMPTLESS')] GONE[$(sect "$f" 'GRANDFATHERED BUT')] UNTR $(sect "$f" 'UNTRACKED' | wc -w) CRout $(tr -cd '\r' < "$f" | wc -c)"; }
#  run the deriver the DOCUMENTED way: cwd = <copy>/GXEMUL-SEC, `bash tools/derive_hygiene_pins.sh ...`, no GXROOT
run() { local lab=$1; shift; local o="$OUT/${TAG}_$lab.out"
    ( cd "$D/GXEMUL-SEC" && bash tools/derive_hygiene_pins.sh "$@" ) > "$o" 2>&1; RC=$?
    FIRST=$(grep -E '^(REFUSED|WRITTEN|DERIVE_FAIL|GRANDFATHERED:|RELEASED:)' "$o" | head -1 | tr -d '\r' | cut -c1-170)
    DONE=$(grep -c '^DERIVE_DONE' "$o"); pins "$D"
    if [ $# -eq 0 ]; then rep "$o"; echo "$lab [$TAG] REPORT rc=$RC done=$DONE | $REP | $PINS" >> "$TAB"
    else echo "$lab [$TAG] rc=$RC done=$DONE | $FIRST | $PINS" >> "$TAB"; fi; }
gate() { local lab=$1
    if [ "$TAG" = G ]; then echo "$lab $D" >> "$GLIST"; return; fi
    local L; L=$(mktemp -d); local o="$OUT/${TAG}_$lab.gate.out"
    ( cd "$D/GXEMUL-SEC/regress" && LOGDIR="$L" bash ./gate_hygiene.sh ) > "$o" 2>&1; rm -rf "$L"
    sed 's/\x1b\[[0-9;]*m//g' "$o" | grep -E '^\s*(FAIL|ok)' | grep -E 'readiness|whole-buffer' > "$o.rows"
    echo "$lab [$TAG] GATE $(grep -cE '^\s*FAIL' "$o.rows") FAIL of $(wc -l < "$o.rows"): $(grep -E '^\s*FAIL' "$o.rows" | sed 's/^ *FAIL *//; s/  */ /g' | cut -c1-60 | tr '\n' ';')" >> "$TAB"; }
trio() {  # the three #392 constructs, as a converted probe carries them
    cat >> "$1" <<EOF


def _zz_ready(resp, echo, _mark, s, wait)$2
    if echo is not None and echo not in resp:
        return False
    if resp.rstrip().$EW("GXemul>"):
        return True
    return wait(mark=_mark, echo=s if s else None)
EOF
}
crlf() { sed -i 's/$/\r/' "$1"; }

c_B() {
    # ---- B baseline, git-initialised with SEC's tracked top-level set
    mk B; ( cd "$D/GXEMUL-SEC" && git init -q . && git -C "$SRC/.." ls-files regress | sed -n 's|^regress/\([^/]*\)$|\1|p' \
        | while IFS= read -r f; do [ -f "regress/$f" ] && echo "regress/$f"; done | tr '\n' '\0' | xargs -0 git add \
        && git -c user.name=o -c user.email=o@o commit -qm base ) >/dev/null 2>&1
    run B1; cp -p "$R/gate_hygiene.sh" "$WORK/B.gate0"
    run B2 --write;               echo "B2 [$TAG] gate byte-identical: $(cmp -s "$WORK/B.gate0" "$R/gate_hygiene.sh" && echo yes || echo NO)" >> "$TAB"
    run B3 --write --ruling "$R1"; echo "B3 [$TAG] gate byte-identical: $(cmp -s "$WORK/B.gate0" "$R/gate_hygiene.sh" && echo yes || echo NO)" >> "$TAB"
    run B4 --grandfather lca_badval_probe.py
    run B5 --release lca_badval_probe.py
    run B6 --grandfather
    gate B7
}
c_S1() {
    # ---- S1 new #392 probe
    mk S1; cp -p "$R/luna_absentcpu_probe.py" "$R/zz_new392_probe.py"
    run S1.1; run S1.2 --write; gate S1.3
}
c_S2() {
    # ---- S2 new promptless probe; S2n with non-ASCII content
    mk S2; cp -p "$R/lca_badval_probe.py" "$R/zz_newpl_probe.py"
    run S2.1; run S2.2 --write; run S2.3 --grandfather zz_newpl_probe.py; run S2.4 --write; gate S2.5
    mk S2n; cp -p "$R/lca_widewrite_probe.py" "$R/zz_newna_probe.py"
    run S2n.1 --grandfather zz_newna_probe.py; run S2n.2 --write; gate S2n.3
}
c_S3() {
    # ---- S3 grandfathered probe converted to the #392 form
    mk S3; trio "$R/gdrom_cond_probe.py" ":"
    run S3.1; run S3.2 --write; run S3.3 --release gdrom_cond_probe.py; run S3.4 --write; gate S3.5
}
c_S4() {
    # ---- S4 deletions
    mk S4a; rm "$R/lca_badval_probe.py"
    run S4a.1; run S4a.2 --release lca_badval_probe.py; run S4a.3 --write; gate S4a.4
    mk S4b; rm "$R/luna_absentcpu_probe.py"
    run S4b.1 --write; run S4b.2 --write --ruling "$R1"; gate S4b.3
    mk S4c; rm "$R/arm_bdt_probe.py"
    run S4c.1 --write; run S4c.2 --write --ruling "$R2"; gate S4c.3
}
c_S5() {
    # ---- S5 whole-buffer site added / removed
    mk S5a; printf '\n\ndef _zz_at_prompt(buf):\n    return buf.rstrip().%s("GXemul>")\n' "$EW" >> "$R/luna_absentcpu_probe.py"
    run S5a.1; run S5a.2 --write; run S5a.3 --write --ruling "$R5"; gate S5a.4
    mk S5b; sed -i '76s/self\.buf\.rstrip()/self.buf[-64:].rstrip()/' "$R/arm_bdt_probe.py"
    echo "S5b [$TAG] edit landed: $(sed -n '76p' "$R/arm_bdt_probe.py" | tr -s ' ')" >> "$TAB"
    run S5b.1; run S5b.2 --write; run S5b.3 --write --ruling "$R2"; gate S5b.4
}
c_S6() {
    # ---- S6 probes that do not parse
    mk S6a; cp -p "$R/lca_badval_probe.py" "$R/zz_synerr_probe.py"; sed -i '131s/:$//' "$R/zz_synerr_probe.py"
    echo "S6a [$TAG] edit landed: $(sed -n '131p' "$R/zz_synerr_probe.py")" >> "$TAB"
    run S6a.1; run S6a.2 --grandfather zz_synerr_probe.py; run S6a.3 --write; gate S6a.4
    mk S6b; cp -p "$R/luna_absentcpu_probe.py" "$R/zz_tokerr_probe.py"; printf '\nx = (\n' >> "$R/zz_tokerr_probe.py"
    run S6b.1; run S6b.2 --grandfather zz_tokerr_probe.py; run S6b.3 --write; gate S6b.4
    mk S6c; trio "$R/gdrom_cond_probe.py" ""
    run S6c.1; run S6c.2 --release gdrom_cond_probe.py; run S6c.3 --write; gate S6c.4
    mk S6d; printf '\nx = (\n' >> "$R/arm_bdt_probe.py"
    run S6d.1; run S6d.2 --write; run S6d.3 --grandfather arm_bdt_probe.py; gate S6d.4
}
c_S7() {
    # ---- S7 CRLF
    mk S7a; cp -p "$R/lca_badval_probe.py" "$R/zz_crlf_probe.py"; crlf "$R/zz_crlf_probe.py"
    run S7a.1; run S7a.2 --grandfather zz_crlf_probe.py; run S7a.3 --write; gate S7a.4
    mk S7b; trio "$R/gdrom_cond_probe.py" ":"; crlf "$R/gdrom_cond_probe.py"
    run S7b.1; run S7b.2 --release gdrom_cond_probe.py; run S7b.3 --write; gate S7b.4
    mk S7c; crlf "$R/arm_flags_probe.py"; cp -p "$R/gate_hygiene.sh" "$WORK/S7c.gate0"
    run S7c.1; run S7c.2 --write; echo "S7c [$TAG] gate byte-identical: $(cmp -s "$WORK/S7c.gate0" "$R/gate_hygiene.sh" && echo yes || echo NO)" >> "$TAB"; gate S7c.3
    mk S7d; crlf "$R/luna_absentcpu_probe.py"; cp -p "$R/gate_hygiene.sh" "$WORK/S7d.gate0"
    run S7d.1; run S7d.2 --write; echo "S7d [$TAG] gate byte-identical: $(cmp -s "$WORK/S7d.gate0" "$R/gate_hygiene.sh" && echo yes || echo NO)" >> "$TAB"; gate S7d.3
}
c_S8() {
    # ---- S8 a grandfathered probe leaves the pty population
    mk S8a; sed -i '190s/pty\.fork()/os.forkpty()/' "$R/lca_badval_probe.py"
    echo "S8a [$TAG] edit landed: $(sed -n '190p' "$R/lca_badval_probe.py" | tr -s ' '); pty.fork left: $(grep -c 'pty.fork' "$R/lca_badval_probe.py")" >> "$TAB"
    run S8a.1; run S8a.2 --release lca_badval_probe.py; run S8a.3 --write; run S8a.4 --write --ruling "$R1"; gate S8a.5
    mk S8b; sed -i '190s/pty\.fork()/drive_guest.fork_guest()/; 124s/$/\nimport drive_guest/' "$R/lca_badval_probe.py"
    echo "S8b [$TAG] edit landed: $(sed -n '124,125p;191p' "$R/lca_badval_probe.py" | tr -s ' ' | tr '\n' '|'); pty.fork left: $(grep -c 'pty.fork' "$R/lca_badval_probe.py")" >> "$TAB"
    run S8b.1; run S8b.2 --release lca_badval_probe.py; run S8b.3 --write; gate S8b.4
    mk S8c; cp -p "$R/luna_absentcpu_probe.py" "$R/zz_session_helper.py"
    sed -i '190s/pty\.fork()/zz_session_helper.fork_guest()/; 124s/$/\nimport zz_session_helper/' "$R/lca_badval_probe.py"
    run S8c.1; run S8c.2 --release lca_badval_probe.py; run S8c.3 --write; gate S8c.4
}
c_S9() {
    # ---- S9 UTF-8 BOM on a new prompt-detecting probe
    mk S9; { printf '\xef\xbb\xbf'; cat "$R/luna_absentcpu_probe.py"; } > "$R/zz_bom_probe.py"
    run S9.1; run S9.2 --grandfather zz_bom_probe.py; run S9.3 --write; gate S9.4
}
c_S10() {
    # ---- S10 subdirectory probe holding whole-buffer sites
    mk S10; mkdir -p "$R/newsub"; cp -p "$R/arm_flags_probe.py" "$R/newsub/zz_sub_probe.py"
    run S10.1; run S10.2 --write; run S10.3 --write --ruling "$R2"; gate S10.4
}
c_S11() {
    # ---- S11 rulings through the writer, each on a fresh S4b-shaped tree
    for i in 1 2 3 4 5 6; do eval "RR=\$R$i"
        mk S11r$i; rm "$R/luna_absentcpu_probe.py"
        run S11.R$i --write --ruling "$RR"
        echo "S11.R$i [$TAG] note: $(grep '^#  RULING' "$R/gate_hygiene.sh" | head -1 | cut -c1-200)" >> "$TAB"
        echo "S11.R$i [$TAG] verbatim: $(grep -qF "#  RULING $RR -- " "$R/gate_hygiene.sh" && echo yes || echo NO)" >> "$TAB"
    done
    gate S11.gate

}
