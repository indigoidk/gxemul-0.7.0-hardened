set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/exemptredate_20260925/opus550_measured_p2
mkdir -p "$O/p1_runs"
for f in /tmp/opus550/out_HEAD.txt /tmp/opus550/out_WT.txt /tmp/opus550/ip30/out_ip30.txt /tmp/opus550/alpha/out_alpha_tbi_probe.txt /tmp/opus550/alpha/out_lca_badval_probe.txt /tmp/opus550/alpha/out_lca_widewrite_probe.txt /tmp/opus550/alpha2/out_lca_isalane_probe.txt; do
  if [ -f "$f" ]; then
    b=$(echo "$f" | sed 's#^/tmp/opus550/##; s#/#_#g')
    cp "$f" "$O/p1_runs/$b"
    echo "kept $b ($(wc -c < "$f") bytes) last: $(tail -1 "$f" | cut -c1-60)"
  else
    echo "GONE $f"
  fi
done
s=$(stat -c %Y /tmp/opus550/ip30/ip30_abort_probe.py 2>/dev/null); e=$(stat -c %Y /tmp/opus550/ip30/out_ip30.txt 2>/dev/null)
[ -n "$s" ] && [ -n "$e" ] && echo "ip30 wall from file mtimes: $((e-s)) s (probe copied at start, log closed at end)"
