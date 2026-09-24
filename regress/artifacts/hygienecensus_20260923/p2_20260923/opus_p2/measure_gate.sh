#!/bin/bash
# opus measuring seat, hygienecensus pass 2 -- gate_hygiene.sh readiness rows on COPIES only.
# Never writes under GXEMUL-SEC: one read-only snapshot of regress/ top-level files, then one
# fresh copy per case from that snapshot, one edit per copy, the UNMODIFIED gate run in the copy
# with LOGDIR pointing at an empty directory.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/opus_census0923
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus/runs
LOC=$W/loc                       # private compiled en_US.UTF-8 (locprobe.sh); nothing system-wide
mkdir -p "$OUT"
rm -rf "$W/snap" "$W/c" "$W/sp ace"; mkdir -p "$W/snap/regress" "$W/c"

# ---- one snapshot, so every case starts from the SAME bytes ----
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/snap/regress/" \;)
{
  echo "snapshot taken $(date '+%F %T') from $SEC/regress (top-level files only)"
  echo "files: $(ls "$W/snap/regress" | wc -l)   .py: $(ls "$W/snap/regress"/*.py | wc -l)"
  md5sum "$W/snap/regress/gate_hygiene.sh" "$W/snap/regress/luna_absentcpu_probe.py" \
         "$W/snap/regress/arm_bdt_probe.py" "$W/snap/regress/arm_flags_probe.py" | sed "s|$W/snap/||"
  echo "HEAD gate md5: $(git -C "$SEC" show HEAD:regress/gate_hygiene.sh | md5sum)"
  echo "--- pins in the snapshot's gate:"
  grep -nE '^(EXPECT_[A-Z_]+|WHOLE_FULL_FILES)=' "$W/snap/regress/gate_hygiene.sh"
  echo "--- luna fresh-mark spelling in the snapshot:"
  grep -nE '_?mark = len\(self\.buf\)|wait\(mark=_?mark' "$W/snap/regress/luna_absentcpu_probe.py"
} > "$OUT/00_snapshot.txt" 2>&1

mk() {   # mk <case> [parent]  -> prints the regress dir of a fresh copy
  local p=${2:-$W/c/$1}
  rm -rf "$p"; mkdir -p "$p/regress" "$p/logs"
  cp -p "$W/snap/regress/"* "$p/regress/"
  printf '%s' "$p/regress"
}
app() {  # app <file> <line>...   append lines verbatim (python, so no shell quoting touches them)
  python3 - "$@" <<'PY'
import io, sys
f, lines = sys.argv[1], sys.argv[2:]
s = io.open(f, encoding="utf-8", newline="").read()
if not s.endswith("\n"): s += "\n"
io.open(f, "w", encoding="utf-8", newline="").write(s + "".join(l + "\n" for l in lines))
PY
}
sub1() { # sub1 <file> <old> <new>   replace exactly ONE occurrence (asserts the old text is present)
  python3 - "$@" <<'PY'
import io, sys
f, old, new = sys.argv[1:]
s = io.open(f, encoding="utf-8", newline="").read()
assert s.count(old) >= 1, ("absent", f, old)
io.open(f, "w", encoding="utf-8", newline="").write(s.replace(old, new, 1))
PY
}
rows() { grep -E 'readiness' "$1" | sed 's/\x1b\[[0-9;]*m//g'; }
raw() {  # the gate's OWN census code (its lines up to the last readiness check) + one echo of the intermediates
  local d=$1 n tag=$2; shift 2
  n=$(grep -n 'check "readiness: send takes a fresh mark (#392)"' "$d/gate_hygiene.sh" | cut -d: -f1)
  { head -n "$n" "$d/gate_hygiene.sh"
    printf '%s\n' 'echo "RAW allends=$allends bare=$bare full=$full unknown=$unknown whole_full=$whole_full whole_files=[$whole_files] ptyn=$_ptyn promptless=$_got/$_want new=[$(echo $_new)] conv=$conv_anchor/$conv_echo/$conv_mark"'
    echo 'exit 0'; } > "$d/zz_raw_gate.sh"
  ( cd "$d" && env LOGDIR="$d/../logs_raw" "$@" bash ./zz_raw_gate.sh 2>/dev/null | grep '^RAW' ) > "$OUT/$tag.raw"
  rm -f "$d/zz_raw_gate.sh"
}
run() {  # run <tag> <regress dir> [env assignments...]
  local tag=$1 d=$2; shift 2
  ( cd "$d" && env LOGDIR="$d/../logs" "$@" bash ./gate_hygiene.sh ) > "$OUT/$tag.out" 2>&1
  rows "$OUT/$tag.out" > "$OUT/$tag.rows"
  raw "$d" "$tag" "$@"
  {
    echo "===== $tag  ($(grep -cE '^\s*(ok|FAIL)\b' "$OUT/$tag.out") rows graded in the whole gate; readiness rows below)"
    sed 's/^/   /' "$OUT/$tag.rows"
    grep -A6 'NEW PROMPTLESS' "$OUT/$tag.out" | sed 's/^/   | /'
    sed 's/^/   /' "$OUT/$tag.raw"
    if [ "$tag" != base ]; then
      if diff -q "$OUT/base.rows" "$OUT/$tag.rows" >/dev/null; then
        echo "   -> readiness rows IDENTICAL to base (no row changed)"
      else
        echo "   -> readiness rows CHANGED vs base:"
        diff "$OUT/base.rows" "$OUT/$tag.rows" | grep -E '^[<>]' | sed 's/^/      /'
      fi
    fi
  } >> "$OUT/SUMMARY.txt"
}
: > "$OUT/SUMMARY.txt"

L=luna_absentcpu_probe.py

# ---- baseline ----
d=$(mk base); run base "$d"

# ---- 1: single-quoted whole-buffer site in a pty-driving probe ----
d=$(mk c1_single_quote); app "$d/$L" "_control_site = lambda buf: buf.rstrip().endswith('GXemul>')"
run c1_single_quote "$d"

# ---- 2: double-quoted with inner spaces ----
d=$(mk c2_inner_spaces); app "$d/$L" '_control_site = lambda buf: buf.rstrip().endswith( "GXemul>" )'
run c2_inner_spaces "$d"

# ---- 3: the double-quoted site only inside a # comment line (indented, and column 0) ----
d=$(mk c3a_comment_indented); app "$d/$L" '            # if self.buf.rstrip().endswith("GXemul>"):'
run c3a_comment_indented "$d"
d=$(mk c3b_comment_col0); app "$d/$L" '# buf.rstrip().endswith("GXemul>")'
run c3b_comment_col0 "$d"

# ---- 4: the copy's directory path contains a space (unmodified files) ----
d=$(mk c4_space_in_path "$W/sp ace/c4"); run c4_space_in_path "$d"

# ---- 5: no file matches the pty-driving population at all ----
d=$(mk c5_no_population)
( cd "$d" && grep -lE 'pty\.fork|forkpty|pty\.spawn|^[[:space:]]*(import|from) drive_guest' ./*.py > "$OUT/c5_removed_files.txt"; \
  xargs rm -f < "$OUT/c5_removed_files.txt" )
echo "c5: removed $(wc -l < "$OUT/c5_removed_files.txt") population files; population now: $(cd "$d" && grep -lE 'pty\.fork|forkpty|pty\.spawn|^[[:space:]]*(import|from) drive_guest' ./*.py | wc -l)" >> "$OUT/SUMMARY.txt"
run c5_no_population "$d"

# ---- 6: locale -- the unmodified copy under four settings ----
d=$(mk c6_locale)
run c6_locale_default "$d"                                     # battery's own env: LANG=en_US.UTF-8, not installed -> C
run c6_locale_C "$d" LC_ALL=C
run c6_locale_Cutf8 "$d" LC_ALL=C.utf8                         # installed; codepoint order
run c6_locale_enUS_real "$d" LOCPATH="$LOC" LC_ALL=en_US.UTF-8  # REAL en_US collation, privately compiled
{ echo "c6: locale actually in effect for the real-en_US run:"; ( cd "$d" && env LOCPATH="$LOC" LC_ALL=en_US.UTF-8 locale 2>&1 | grep -E 'COLLATE|warning|Cannot' ); \
  echo "c6: sort check under that env: $(printf 'arm_c.py\narmb_x.py\n' | env LOCPATH="$LOC" LC_ALL=en_US.UTF-8 sort | tr '\n' ' ')(C gives: $(printf 'arm_c.py\narmb_x.py\n' | LC_ALL=C sort | tr '\n' ' '))"; } >> "$OUT/SUMMARY.txt"

# ---- other single edits (evasion hunt) ----
d=$(mk e1_receiver_named_out); app "$d/$L" '_control_site = lambda out: out.rstrip().endswith("GXemul>")'
run e1_receiver_named_out "$d"
d=$(mk e2_split_across_lines); app "$d/$L" '_control_site = lambda buf: (buf.rstrip()' '                             .endswith("GXemul>"))'
run e2_split_across_lines "$d"
d=$(mk e3_space_before_paren); app "$d/$L" '_control_site = lambda buf: buf.rstrip().endswith ("GXemul>")'
run e3_space_before_paren "$d"
d=$(mk e4_slice_compare); app "$d/$L" '_control_site = lambda buf: buf.rstrip()[-7:] == "GXemul>"'
run e4_slice_compare "$d"
d=$(mk e5_strip_not_rstrip); app "$d/$L" '_control_site = lambda buf: buf.strip().endswith("GXemul>")'
run e5_strip_not_rstrip "$d"
# MOVE inside the allowlisted set: arm_flags_probe.py loses one site, arm_bdt_probe.py gains one (count stays 3)
d=$(mk e6_move_within_allowlist)
sub1 "$d/arm_flags_probe.py" 'if buf.rstrip().endswith("GXemul>"):' 'if buf.rstrip()[-7:] == "GXemul>":'
app "$d/arm_bdt_probe.py" '_control_site = lambda buf: buf.rstrip().endswith("GXemul>")'
run e6_move_within_allowlist "$d"
# a NEW promptless pty probe whose FILE NAME holds a space (copy of a grandfathered promptless probe)
d=$(mk e7_new_promptless_space_name); cp -p "$d/pcc2_width_probe.py" "$d/zz opus_newprobe.py"
run e7_new_promptless_space_name "$d"
# control for e7: the same copy under a name WITHOUT a space must red
d=$(mk e7ctl_new_promptless_plain_name); cp -p "$d/pcc2_width_probe.py" "$d/zz_opus_newprobe.py"
run e7ctl_new_promptless_plain_name "$d"
# a NEW promptless pty probe in a new (non-artifacts) SUBDIRECTORY
d=$(mk e8_new_promptless_subdir); mkdir -p "$d/newsub"; cp -p "$d/pcc2_width_probe.py" "$d/newsub/zz_opus_subprobe.py"
run e8_new_promptless_subdir "$d"

echo "MEASURE_GATE_DONE" >> "$OUT/SUMMARY.txt"
echo MEASURE_GATE_DONE
