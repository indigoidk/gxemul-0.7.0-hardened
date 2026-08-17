#!/usr/bin/env bash
# adjudicate.sh -- cross-check ONE seat's research output with the Ollama cloud
# seats, in one command.
#
#   Usage:  bash adjudicate.sh <finding_file> [tail_bytes] [out_dir]
#           bash adjudicate.sh _scratchpad/codex_par_.../codex_76.txt
#
# WHY THIS EXISTS.  panel.sh convenes a panel on a BRIEF.  This is the other
# direction: one seat has produced a finding, and the question is whether it
# survives independent scrutiny.  The project rule is that disagreements are
# settled by MECHANISM, never by vote -- so these seats are asked to REFUTE,
# and a refutation only counts if it names the mechanism.  Their agreement is
# not proof; their specific, checkable objection is the useful output.
#
# The three Ollama seats CANNOT read files, so the finding is INLINED.  Codex
# streams its reasoning into its output file, so by default only the TAIL is
# taken -- that is where the answer lives, and the whole file can be megabytes.
# Check the tail actually contains the conclusion before trusting a run.
#
# Kimi is deliberately NOT wired in here: it has been returning
# 403 usage-limit-for-billing-cycle since 2026-08-12 and was re-health-tested
# on 2026-08-13 with the same result.  Add it back only after `kimi -p "say OK"`
# answers.  A dead seat is a SEAT FAILURE and is never counted as agreement.
set -u

#  PROJ is the PROJECT ROOT.  It used to equal this script's directory,
#  which stopped being true when the harness moved into GXEMUL-SEC/tools/.
TOOLS="$(cd "$(dirname "$0")" && pwd)"
PROJ="${GXROOT:-$(cd "$TOOLS/.." && cd .. && pwd)}"
SRC="${1:?usage: adjudicate.sh <finding_file> [tail_bytes] [out_dir]}"
[ -f "$SRC" ] || { echo "no such finding file: $SRC" >&2; exit 1; }
TAILB="${2:-24000}"
BASE="$(basename "$SRC" .txt)"
OUT="${3:-$PROJ/_scratchpad/adjudicate_${BASE}_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"

BRIEF="$OUT/brief.md"
{
    cat <<'HDR'
# Adjudication — refute this finding, or say precisely why it stands

Another model produced the engineering finding below, about a hardened fork of
GXemul 0.7.0 (an open-source machine emulator). You are an independent
adjudicator. This is ordinary correctness engineering.

Your job is NOT to summarise or agree. It is to find what is WRONG with it.
Agreement is cheap and carries no information here; a specific, checkable
objection is the entire value of this pass.

Answer these, in order:

1. **Which claims are load-bearing?** List the specific factual claims the
   conclusion actually depends on. Ignore the ones that are decoration.
2. **Which of those could be false?** For each, say what would have to be true
   for the claim to fail, and how someone could check it against the source or
   the architecture manual in one step.
3. **Is any reasoning circular or assumed?** In particular: does it verify a
   mechanism, or does it restate the premise it was handed? A finding that
   assumes its own premise is the most common failure mode here.
4. **Reachability.** If it claims a defect, can real guest code reach it, or
   does it need an encoding the architecture leaves undefined? A defect on a
   dead path is a record, not a fix — and this project has stopped a change
   from shipping for exactly that reason.
5. **Is the proposed test able to FAIL?** If a regression row is proposed, name
   a wrong implementation the row would still pass. A row that cannot fail is
   worse than none, because it reads as coverage.
6. **Your verdict**: STANDS / STANDS-WITH-CORRECTIONS / REFUTED, and for
   anything other than STANDS, the mechanism that breaks it.

Do not defer to the finding's confidence. It may be entirely correct — say so
plainly if it is, but only after trying to break it.

---

## THE FINDING

HDR
    tail -c "$TAILB" "$SRC"
} > "$BRIEF"

echo "adjudicate: src=$SRC (tail ${TAILB}b)  out=$OUT"
BSZ=$(wc -c < "$BRIEF")
echo "brief: ${BSZ} bytes"

for m in glm-5.2:cloud deepseek-v4-pro:cloud minimax-m3:cloud; do
    short="${m%%:*}"
    python "$TOOLS/panel_ollama.py" "$m" "$OUT/$short.txt" "$BRIEF" \
        > "$OUT/$short.err" 2>&1 &
done
wait

echo "---- seat check ----"
ok=0; miss=""
for m in glm-5.2 deepseek-v4-pro minimax-m3; do
    f="$OUT/$m.txt"
    if [ -s "$f" ] && [ "$(wc -c < "$f")" -ge 800 ]; then
        echo "  $m: $(wc -c < "$f")b answered"
        ok=$((ok+1))
    else
        echo "  $m: NO ANSWER ($( [ -f "$f" ] && wc -c < "$f" || echo 0 )b)"
        miss="$miss $m"
    fi
done
echo "ADJUDICATORS: $ok/3${miss:+ -- no answer from:$miss}"
echo "       (a non-answering seat is a SEAT FAILURE, never counted as agreement)"
