#!/usr/bin/env bash
# dismiss.sh -- dismiss the GitHub code-scanning alerts that plan.tsv puts in class DISMISS (the triage's no-action set).
#
#   bash dismiss.sh            DRY RUN (the default): print each `gh api -X PATCH ...` command.  No network access at all.
#   bash dismiss.sh --check    READ-ONLY: re-fetch each alert (GET) and report MATCH or REFUSED.  Never PATCHes.
#   bash dismiss.sh --apply    re-fetch each alert; REFUSE it unless its state is `open` and its rule and path:line still
#                              equal plan.tsv's; only then PATCH it to dismissed, and read the new state back.
#   options: --plan FILE (default: plan.tsv beside this script)
#   env:     GH (the gh executable; default: /c/Program Files/GitHub CLI/gh.exe, else gh on PATH)
#            REPO_SLUG (default: indigoidk/gxemul-0.7.0-hardened)
#
# The owner authorized these dismissals only AFTER the code-scan fixes land and are pushed.  A line that moved in the push
# (#130 is predicted to, see SUMMARY.md) is REFUSED until plan.tsv is re-derived from a fresh fetch (tools/mkplan.py).
# Exit status: 0 if every DISMISS row was printed / matched / applied; 1 if any row was refused, invalid or failed; 2 on usage.
set -u
export MSYS_NO_PATHCONV=1                        # git-bash: never rewrite an argument that looks like a path

here=$(cd "$(dirname "$0")" && pwd)
mode=dry
plan="$here/plan.tsv"
while [ $# -gt 0 ]; do
	case "$1" in
	--apply|--check)
		[ "$mode" = dry ] || { echo "dismiss.sh: give at most one of --check / --apply" >&2; exit 2; }
		mode=${1#--} ;;
	--plan)
		[ $# -ge 2 ] || { echo "dismiss.sh: --plan needs a file" >&2; exit 2; }
		shift; plan=$1 ;;
	-h|--help)
		sed -n '2,15p' "$0"; exit 0 ;;
	*)
		echo "dismiss.sh: unknown argument: $1" >&2; exit 2 ;;
	esac
	shift
done

slug=${REPO_SLUG:-indigoidk/gxemul-0.7.0-hardened}
if [ -n "${GH:-}" ]; then gh=$GH
elif [ -x "/c/Program Files/GitHub CLI/gh.exe" ]; then gh="/c/Program Files/GitHub CLI/gh.exe"
else gh=gh; fi

[ -r "$plan" ] || { echo "dismiss.sh: cannot read plan: $plan" >&2; exit 2; }
want_hdr=$'number\trule\tpath:line\tclass\treason\tcomment'
got_hdr=$(head -n 1 "$plan" | tr -d '\r')
[ "$got_hdr" = "$want_hdr" ] || { echo "dismiss.sh: $plan: unexpected header: $got_hdr" >&2; exit 2; }
bad_nf=$(awk -F'\t' '{ sub(/\r$/, "") } NR > 1 && NF != 6 { printf "%d ", NR }' "$plan")
[ -z "$bad_nf" ] || { echo "dismiss.sh: $plan: rows without exactly 6 tab-separated fields at lines: $bad_nf" >&2; exit 2; }

US=$'\037'                                       # unit separator: not IFS whitespace, so empty fields survive `read`
echo "# dismiss.sh mode=$mode plan=$plan repo=$slug"
[ "$mode" = apply ] && echo "# APPLY MODE: this changes alert states on GitHub."

n_rows=0; n_ok=0; n_ref=0; n_bad=0; n_fail=0
while IFS=$US read -r num rule loc reason comment; do
	n_rows=$((n_rows + 1))
	why=""
	case "$num" in ''|*[!0-9]*) why="alert number is not a number: '$num'" ;; esac
	case "$reason" in "false positive"|"won't fix"|"used in tests") ;; *) why="${why:+$why; }reason is not a GitHub dismissed_reason: '$reason'" ;; esac
	[ -n "$comment" ] || why="${why:+$why; }empty comment"
	[ "${#comment}" -le 280 ] || why="${why:+$why; }comment is ${#comment} characters (GitHub allows 280)"
	[[ "$loc" =~ ^.+:[0-9]+$ ]] || why="${why:+$why; }path:line is malformed: '$loc'"
	if [ -n "$why" ]; then
		echo "INVALID  #$num: $why"; n_bad=$((n_bad + 1)); continue
	fi
	cmd=("$gh" api -X PATCH "repos/$slug/code-scanning/alerts/$num"
	     -f state=dismissed -f "dismissed_reason=$reason" -f "dismissed_comment=$comment")
	if [ "$mode" = dry ]; then
		printf '%q ' "${cmd[@]}"; echo
		n_ok=$((n_ok + 1)); continue
	fi
	# --check and --apply: re-fetch (GET) and compare with the plan row before anything else
	# (no pipe inside the substitution: $? must be gh's own status; stdin from /dev/null so gh cannot eat the plan stream)
	cur=$("$gh" api "repos/$slug/code-scanning/alerts/$num" --jq \
		'[.state, .rule.id, (.most_recent_instance.location.path + ":" + (.most_recent_instance.location.start_line | tostring)), .most_recent_instance.commit_sha[0:8]] | join("\u001f")' \
		2>&1 < /dev/null)
	rc=$?
	cur=${cur//$'\r'/}
	if [ "$rc" -ne 0 ]; then
		echo "REFUSED  #$num: re-fetch failed (gh rc=$rc): $(printf '%s' "$cur" | head -c 200)"; n_ref=$((n_ref + 1)); continue
	fi
	IFS=$US read -r c_state c_rule c_loc c_sha <<< "$cur"
	why=""
	[ "$c_state" = open ] || why="state is '$c_state', not 'open'"
	[ "$c_rule" = "$rule" ] || why="${why:+$why; }rule is '$c_rule', plan says '$rule'"
	[ "$c_loc" = "$loc" ] || why="${why:+$why; }path:line is '$c_loc', plan says '$loc'"
	if [ -n "$why" ]; then
		echo "REFUSED  #$num: $why (scan $c_sha)"; n_ref=$((n_ref + 1)); continue
	fi
	if [ "$mode" = check ]; then
		echo "MATCH    #$num: open, $c_rule, $c_loc (scan $c_sha) -- would run: $(printf '%q ' "${cmd[@]}")"
		n_ok=$((n_ok + 1)); continue
	fi
	res=$("${cmd[@]}" --jq '.state + "\u001f" + (.dismissed_reason // "")' 2>&1 < /dev/null)
	rc=$?
	res=${res//$'\r'/}
	IFS=$US read -r r_state r_reason <<< "$res"
	if [ "$rc" -eq 0 ] && [ "$r_state" = dismissed ] && [ "$r_reason" = "$reason" ]; then
		echo "APPLIED  #$num: dismissed as '$r_reason' ($c_loc)"; n_ok=$((n_ok + 1))
	else
		echo "FAILED   #$num: gh rc=$rc, response: $(printf '%s' "$res" | head -c 200)"; n_fail=$((n_fail + 1))
	fi
done < <(awk -F'\t' '{ sub(/\r$/, "") } NR > 1 && $4 == "DISMISS" { printf "%s\037%s\037%s\037%s\037%s\n", $1, $2, $3, $5, $6 }' "$plan")

case "$mode" in dry) okword=printed ;; check) okword=matched ;; apply) okword=applied ;; esac
echo "# DISMISS rows: $n_rows; $okword: $n_ok; refused: $n_ref; invalid: $n_bad; failed: $n_fail"
[ "$n_rows" -gt 0 ] || { echo "# no DISMISS rows in $plan" >&2; exit 1; }
[ $((n_ref + n_bad + n_fail)) -eq 0 ]
