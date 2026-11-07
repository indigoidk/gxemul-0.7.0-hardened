#!/usr/bin/env python3
"""A ROUND CAN SHIP WITHOUT WRITING BACK, AND NO GATE COULD SEE IT.  (ledger row `ghostround`)

PROTOTYPE, in scratch (`_scratchpad/wghost/`).  Not wired into any gate: wiring it is an
OWNER decision (the row says so), because it changes what every commit must pass.

THE DEFECT CLASS, measured 2026-08-29: `#479` shipped on 2026-08-27 (`2343036`) and its
CHANGELOG block names three rows (`wdcwipclear`, `wdcringnoflush`, `wdcstalephase`).  Two
days later all three were still `in work`, the ledger recorded nothing about the ship, and a
nine-seat panel was fired to redo shipped work.  The CHANGELOG knew; the ledger did not.
Section H cannot see it by construction: it reads ledger ENTRIES and skips stages that never
started.

WHAT THIS CHECKS (existence-only).  For every ROUND block of CHANGELOG.md (see `block_kind`)
and every ledger row the block NAMES, the row must be terminal (`closed`/`dropped`) or carry
a WRITE-BACK.  It checks that a write-back EXISTS, never whether it says the right thing.

THE WRITE-BACK RULE, and the default is NOT the wording the row filed:

  * `--rule=date` -- the row's wording: "an entry dated on or after the round".
    *** MEASURED BLIND TO ITS OWN MOTIVATING CASE. ***  At `d9efd339`, the commit before the
    write-back, each `#479` row carried nine RESEARCH entries dated 2026-08-27 -- the ship day.
    Entries carry a DATE and no time, so pre-ship stages on ship day satisfy "on or after" and
    the rule passes the ghost (controls/out/c4b_d9efd339_date_BLIND.out).  Replayed on all 141
    landing commits since the ledger entered git it catches 2 of the 11 rows a later record
    documents as shipped-and-unrecorded, and fails 84 landings -- every November one --
    because a row a round FILES has no entry yet (replay.out, replay_class.out).
  * `--rule=mention` (default) -- the row's record NAMES THE ROUND: the block's own number
    (`#479`, or `Round 479`) in the row's state_note / hold / hold_question / closure /
    witness / commits / note, or in an entry dated on or after the round.  A pre-ship stage
    cannot know which round shipped it; a write-back says so.  At `d9efd339` the three rows
    name `#479` nowhere, so this rule fires (controls/out/c4a_d9efd339_mention.out).  A ROUND
    block with no number of its own (`Round pcc2widthkills, pass 13`, the two id-headed
    harness blocks) falls back to the date rule, and the hit line says so.  Usable at
    pre-commit time: the landing commit knows its round number, never its own sha.
  * `--accept-commits` also counts a `commits` field naming the commit that added the block
    (git blame).  OFF by default, on a measurement: `#526`, `#527` and `#528` (2026-09-12)
    carried ONLY that sha, still `in work`, for 36 days until a 2026-10-18 records round found
    them "never moved out of `in work`".  At `2951694f` (2026-10-17) the default names all four
    rows; with this flag they go silent (controls/out/c7*.out).  Under the default scope it
    rescues no pair at HEAD, and inside a landing commit it can never apply.

SCOPE, measured by replaying every landing commit (replay.out): which named rows are checked.
  * `--scope=subject` (default) -- rows the block names in its HEADER (the round's subject) and
    any named row still `in work` (claimed).  It catches all 11 documented ghosts, in 7 rounds
    (`#479` named its three rows only in the BODY; they were `in work`), and would have failed
    20 of 141 landing commits -- 13 with a real gap, 7 on references or filings only -- and 2
    of the 32 since October, both references (replay_class.tsv).
  * `--scope=all` -- every named row, the row's literal reading: 76 of 141 landings fail,
    because a round block names its residual filings and its neighbours as well as its rows.
  * NOT checked by either: a row a round shipped on that is `open` or `held` and named only in
    the body.  A filing and a reference look the same there, and that is the price of the
    default's quiet.

FORWARD-ONLY BY DATE, the check_bugfile_sync.py / HOLDQ_CUTOFF idiom: hits in blocks that
LANDED on or before CUTOFF are REPORTED and not failed ("ARCHIVED"); later ones FAIL.  A rule
that retro-fails the archive gets switched off.

TWO DATES PER BLOCK, because they answer different questions:
  * the ROUND date -- the header's own date, else the date git blame gives the header line --
    is what "an entry on or after the round" compares against;
  * the LANDED date -- git blame's date, else the header's -- is what the cutoff compares
    against, so an old date typed into a NEW header cannot archive it.
  A line git reports as not yet committed lands TODAY, which is what it is.  No date at all
  (no header date, no git) is UNDATED: NEW for the cutoff (check_bugfile_sync.py's rule), and
  TODAY for the entry comparison.

HOW A ROW IS "NAMED", the check_bugfile_sync.py idiom: in the BODY, a markdown code span that
is exactly a row id, or a comma/plus/slash list whose every member is one; in the HEADER, the
same, or a SUBJECT position -- an element of a parenthesised list (`(lecsrmask)`,
`(sgirekills, the MTE half)`) or the word right after the round marker (`Round #504
sgirandompixel`, `#502` m88kexcdeliver).  NOT a bare word elsewhere in a header: row `census`
is also an English word, and `#546`'s header says "gate 6's readiness census was 24 probes
stale".  Fenced code is skipped: it is quoted output, not a claim.

Overridable inputs, so controls run against COPIES (the check_stage_panels.py lesson: a
control that silently reads the real file is indistinguishable from a passing one), and every
run prints what it read:
  GXLEDGER  GXCHANGELOG  GXGHOST_CUTOFF  GXGHOST_TODAY

Options: `--list` also prints the ARCHIVED hits; `--at=REV` replays commit REV read-only from
git (`git show REV:CHANGELOG.md`, `REV:tools/pipeline/ledger.json`, `git blame REV`);
`--no-git` (without --at) dates blocks by their headers only; `--rule=`, `--scope=` and
`--accept-commits` as above.

Exit 0 clean; 1 on post-cutoff hits; 2 VOID -- no round block, no ledger row, or no (block,
row) pair was parsed.  A run that read nothing must not render as a clean one: an empty
CHANGELOG is a NULL MEDIUM, not a pass.
"""
import datetime
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(HERE, "ledger.json")):          # installed in tools/pipeline/
    _SEC = os.path.join(HERE, os.pardir, os.pardir)
else:                                                          # the scratch prototype
    _SEC = os.path.join(HERE, os.pardir, os.pardir, "GXEMUL-SEC")
SEC = os.path.abspath(os.environ.get("GXSEC") or _SEC)
LEDGER = os.environ.get("GXLEDGER") or os.path.join(SEC, "tools", "pipeline", "ledger.json")
CHANGELOG = os.environ.get("GXCHANGELOG") or os.path.join(SEC, "CHANGELOG.md")

#  Proposed: the census date at HEAD 2632277f.  Every hit already in the file is reported and
#  none is failed; the first round block to land after it is held to the rule.
CUTOFF = os.environ.get("GXGHOST_CUTOFF") or "2026-11-05"
TODAY = os.environ.get("GXGHOST_TODAY") or datetime.date.today().isoformat()

#  Derived from the data, as check_bugfile_sync.py's comment demands: the states that occur
#  are closed, dropped, held, "in work" and open; the first two owe nothing.
TERMINAL = ("closed", "dropped")
UNDATED = "9999-99-99"

_D = r"(20\d\d-[01]\d-[0-3]\d)"
#  A header's OWN date, read only where headers state one: first in a parenthesised group --
#  `(2026-11-05)`, `(2026-11-02, landed 2026-11-03)`, `(follow-up, 2026-11-05)`,
#  `(e8a2bc, 2026-09-19)` -- or after a leading keyword (`Records, 2026-10-24:`,
#  `RECORDS 2026-09-17 --`, `## 2026-10-09 -- records:`).  NOT any date in the prose: `#550`'s
#  header says "the ten probe-wiring exemptions that all fell due on 2026-09-27", and the
#  round landed on 2026-09-26.
HEADER_DATE = (re.compile(r"\((?:follow-up, |[0-9a-f]{6,40}, )?" + _D + r"\b"),
               re.compile(r"^#+ (?:Records,|RECORDS|ADJUDICATION|MARKER CENSUS|SEAT AUDIT|"
                          r"GATE 2 SC_EXEMPT|Probe wiring,) " + _D),
               re.compile(r"^## " + _D + r" -- "))


def header_date(header):
    best = None
    for p in HEADER_DATE:
        m = p.search(header)
        if m and (best is None or m.start(1) < best.start(1)):
            best = m
    return best.group(1) if best else ""
FENCE = re.compile(r"^\s*(?:>\s?)*```")
SPAN = re.compile(r"`([^`\n]+)`")

#  The block's OWN round number, read only where a header states it -- `#584` (...),
#  Round #504 x, Round 495 (#495), Round 477 pass 2, R11 (#438), Twentieth round (#224...).
#  A number later in the header is a REFERENCE ("the accept side of #495's guard",
#  "closing #530's chain") and is not the block's own.
OWN_RNUM = (re.compile(r"^#+ `#(\d+[a-z]?)`"),
            re.compile(r"^#+ Round #?(\d+[a-z]?)\b"),
            re.compile(r"^## R\d+ \(#(\d+[a-z]?)\b"),
            re.compile(r"^## #(\d+[a-z]?)\b"),
            re.compile(r"^## [A-Z][a-z]+(?:-[a-z]+)* round \(#(\d+[a-z]?)"))

#  H2 lines that START a block.  Every H1 outside a fence starts one; H2 is a block level only
#  in the older stretch of the file and for a few standalone records entries, in these shapes.
#  Every other H2 is a subsection of the enclosing block -- "## Gate", "## Records", and also
#  "## Records corrections made in-round" and "## Not changed (assessed, disclosed in the
#  probe header)", which a looser pattern split blocks on.
H2_BLOCK = re.compile(
    r"^## (?:Round\b|R\d+ \(#|#\d|[A-Z][a-z]+(?:-[a-z]+)* round \(#|Records correction -- |"
    r"Retrospective|The `fable5` adjudication|20\d\d-[01]\d-[0-3]\d -- |"
    r"Changes by file \(|Not changed \(assessed, intentionally left\))")

#  Blocks that record records or harness housekeeping rather than a round.  They NAME rows --
#  filings above all ("126 queue rows from GitHub forks") -- and a filing is legitimately
#  open, so checking them would make every filing a ghost.  Counted, never checked.  ANCHORED
#  to the header's opening words: "## Round #500 pass 11 -- the ADJUDICATION pass" is a round,
#  and an unanchored pattern filed it as records.
RECORDS = re.compile(
    r"^#+ (?:`#\d+[a-z]?` )?Records\b|^#+ RECORDS\b|"
    r"^## (?:#\d+[a-z]?|20\d\d-[01]\d-[0-3]\d) -- records:|"
    r"^# (?:ADJUDICATION|MARKER CENSUS|SEAT AUDIT|Probe wiring|GATE 2 SC_EXEMPT)\b|"
    r"^#+ Retrospective\b|^## The `fable5` adjudication")
SECTION = re.compile(r"^# GXemul 0\.7\.0|^## Changes by file \(|"
                     r"^## Not changed \(assessed, intentionally left\)")
SUBJECT_AFTER_MARKER = re.compile(r"^#+ (?:`#\d+[a-z]?`|Round #?\d+[a-z]?|Round)\s+([A-Za-z0-9_]+)")


def block_kind(header):
    if SECTION.search(header):
        return "SECTION"
    if RECORDS.search(header):
        return "RECORDS"
    return "ROUND"


def own_round(header):
    for p in OWN_RNUM:
        m = p.search(header)
        if m:
            return m.group(1)
    return ""


def span_ids(text, row_ids, out, where, counts=None):
    for sp in SPAN.findall(text):
        c = sp.strip()
        members = [x for x in re.split(r"[\s,+/]+", c) if x]
        if counts is not None:
            counts[0] += 1
            counts[1] += len(members)
        if c in row_ids:
            out.setdefault(c, where)
        elif len(members) > 1 and all(x in row_ids for x in members):
            for x in members:
                out.setdefault(x, where)


def header_ids(header, row_ids):
    out = {}
    span_ids(header, row_ids, out, "header")
    for grp in re.findall(r"\(([^()]*)\)", header):
        for el in re.split(r"\s*[,+]\s*", grp):
            el = el.strip().strip("`")
            if el in row_ids:
                out.setdefault(el, "header")
    m = SUBJECT_AFTER_MARKER.match(header)
    if m and m.group(1) in row_ids:
        out.setdefault(m.group(1), "header")
    return out


def read_text(path):
    with io.open(path, encoding="utf-8", errors="replace", newline="") as f:
        return f.read()


def git_show(rev, relpath):
    p = subprocess.run(["git", "-C", SEC, "show", "%s:%s" % (rev, relpath)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit("check_ghost_rounds: git show %s:%s failed: %s"
                         % (rev, relpath, p.stderr.decode("utf-8", "replace").strip()))
    return p.stdout.decode("utf-8", "replace")


def git_blame(path, rev=None):
    """{1-based line: (YYYY-MM-DD, sha)}, or {} when git cannot blame the file.

    With `rev`, blames `path` (relative to the repo) AS OF that commit -- the --at replay."""
    try:
        if rev:
            cmd = ["git", "-C", SEC, "blame", "--porcelain", rev, "--", path]
        else:
            d = os.path.dirname(os.path.abspath(path))
            top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                                 capture_output=True, text=True, timeout=30)
            if top.returncode != 0:
                return {}
            cmd = ["git", "-C", d, "blame", "--porcelain", "--", os.path.abspath(path)]
        p = subprocess.run(cmd, capture_output=True, timeout=300)
        if p.returncode != 0:
            return {}
    except (OSError, subprocess.SubprocessError):
        return {}
    times, out, cur = {}, {}, None
    for raw in p.stdout.decode("utf-8", "replace").split("\n"):
        if raw.startswith("\t"):
            continue
        m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", raw)
        if m:
            cur = m.group(1)
            out[int(m.group(2))] = cur
            continue
        if cur and raw.startswith("committer-time "):
            times.setdefault(cur, [None, "+0000"])[0] = int(raw.split()[1])
        elif cur and raw.startswith("committer-tz "):
            times.setdefault(cur, [None, "+0000"])[1] = raw.split()[1]
    res = {}
    for ln, sha in out.items():
        if set(sha) == {"0"}:
            res[ln] = (TODAY, "")            # not committed yet: it lands today
            continue
        t, tz = times.get(sha, [None, "+0000"])
        if t is None:
            continue
        off = (1 if tz[0] == "+" else -1) * (int(tz[1:3]) * 3600 + int(tz[3:5]) * 60)
        res[ln] = (datetime.datetime.fromtimestamp(t + off, datetime.timezone.utc)
                   .strftime("%Y-%m-%d"), sha)
    return res


def parse_blocks(text, row_ids, blame=None):
    """[{line, header, kind, date, date_src, landed, sha, rnum, ids, spans, tokens}]"""
    blame = blame or {}
    lines = text.split("\n")
    starts, infence = [], False
    for i, raw in enumerate(lines, 1):
        s = raw.rstrip("\r")
        if FENCE.match(s):
            infence = not infence
            continue
        if not infence and (s.startswith("# ") or H2_BLOCK.match(s)):
            starts.append(i)
    blocks = []
    for k, ln in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines) + 1
        header = lines[ln - 1].rstrip("\r")
        bdate, bsha = blame.get(ln, ("", ""))
        hd = header_date(header)
        if hd:
            date, src = hd, "header"
        elif bdate:
            date, src = bdate, "blame"
        else:
            #  No date anywhere: NEW for the cutoff (landed = UNDATED), and TODAY for "an entry on
            #  or after the round" -- comparing entries against 9999-99-99 would fail every row,
            #  which a control measured (c1c's date leg read FAIL for that reason alone).
            date, src = TODAY, "undated"
        landed = bdate or (date if src == "header" else UNDATED)
        ids = header_ids(header, row_ids)
        counts = [0, 0]
        infence = False
        for raw in lines[ln:end - 1]:
            s = raw.rstrip("\r")
            if FENCE.match(s):
                infence = not infence
                continue
            if not infence:
                span_ids(s, row_ids, ids, "body", counts)
        blocks.append({"line": ln, "header": header, "kind": block_kind(header),
                       "date": date, "date_src": src, "landed": landed, "sha": bsha,
                       "rnum": own_round(header), "ids": ids,
                       "spans": counts[0], "tokens": counts[1]})
    return blocks


def entries(row):
    return [e for e in (row.get("entries") or []) if isinstance(e, dict)]


def round_pattern(rnum):
    return re.compile(r"(?:#|\b[Rr]ound\s+)%s(?![0-9A-Za-z])" % re.escape(rnum))


def as_text(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def mentions_round(row, rnum, date):
    """Does the row's record name round `rnum`?  Entries count only when dated on/after."""
    pat = round_pattern(rnum)
    for k in ("state_note", "hold", "hold_question", "closure", "witness", "commits", "note"):
        v = row.get(k)
        if v and pat.search(as_text(v)):
            return True
    return any((e.get("date") or "") >= date and pat.search(as_text(e)) for e in entries(row))


def commits_of(row):
    c = row.get("commits") or ""
    if isinstance(c, list):
        c = " ".join(str(x) for x in c)
    return [x for x in re.split(r"[\s,;]+", str(c)) if re.fullmatch(r"[0-9a-f]{7,40}", x)]


def names_commit(row, sha):
    return bool(sha) and any(sha.startswith(c) for c in commits_of(row))


def written_back(row, block, rule, accept_commits=False):
    """(bool, how) for a NON-TERMINAL row named in a round block."""
    d = block["date"]
    if rule == "mention":
        if accept_commits and names_commit(row, block["sha"]):
            return True, "commits"
        if block["rnum"]:
            return mentions_round(row, block["rnum"], d), "mention of #%s" % block["rnum"]
        return (any((e.get("date") or "") >= d for e in entries(row)),
                "entry on/after %s (fallback: the block has no number)" % d)
    return any((e.get("date") or "") >= d for e in entries(row)), "entry on/after %s" % d


def in_scope(row, where, scope):
    """`subject` (default): a row the block names in its HEADER -- the round's own subject --
    or any named row still `in work`, i.e. claimed.  `all`: every row the block names."""
    return scope == "all" or where == "header" or row.get("state") == "in work"


def hits(blocks, rows, rule, scope="subject", accept_commits=False):
    out = []
    for b in blocks:
        if b["kind"] != "ROUND":
            continue
        for rid, where in sorted(b["ids"].items()):
            row = rows[rid]
            if row.get("state") in TERMINAL or not in_scope(row, where, scope):
                continue
            ok, how = written_back(row, b, rule, accept_commits)
            if not ok:
                out.append((b, rid, row.get("state", "?"), where, how))
    return out


def main(argv):
    rule, scope = "mention", "subject"
    for a in argv:
        if a.startswith("--rule="):
            rule = a.split("=", 1)[1]
        elif a.startswith("--scope="):
            scope = a.split("=", 1)[1]
    if rule not in ("mention", "date") or scope not in ("subject", "all"):
        print("check_ghost_rounds: --rule=mention|date, --scope=subject|all (got %s, %s)"
              % (rule, scope))
        return 9
    listing = "--list" in argv
    accept_commits = "--accept-commits" in argv
    at = ([a.split("=", 1)[1] for a in argv if a.startswith("--at=")] or [""])[0]

    if at:
        #  REPLAY: what this check says about commit `at`, read entirely from git (read-only).
        ledger = json.loads(git_show(at, "tools/pipeline/ledger.json"))
        text = git_show(at, "CHANGELOG.md")
        blame = git_blame("CHANGELOG.md", rev=at)
        src = "%s:CHANGELOG.md / %s:tools/pipeline/ledger.json" % (at, at)
    else:
        ledger = json.load(io.open(LEDGER, encoding="utf-8", newline=""))
        text = read_text(CHANGELOG)
        blame = {} if "--no-git" in argv else git_blame(CHANGELOG)
        src = "%s / %s" % (CHANGELOG, LEDGER)
    rows = {r["id"]: r for r in ledger.get("rows", [])}
    blocks = parse_blocks(text, set(rows), blame)

    rounds = [b for b in blocks if b["kind"] == "ROUND"]
    pairs = [(b, rid, w) for b in rounds for rid, w in b["ids"].items()]
    nonterm = [(b, rid, w) for b, rid, w in pairs if rows[rid].get("state") not in TERMINAL]
    scoped = [p for p in nonterm if in_scope(rows[p[1]], p[2], scope)]
    found = hits(blocks, rows, rule, scope, accept_commits)
    live = [h for h in found if h[0]["landed"] > CUTOFF]
    srcs = {}
    for b in rounds:
        srcs[b["date_src"]] = srcs.get(b["date_src"], 0) + 1

    print("check_ghost_rounds: rule=%s scope=%s cutoff=%s  %d blocks parsed, %d ROUND (dated by "
          "%s); %d ledger rows; %d (round block, row) pairs, %d non-terminal, %d in scope, "
          "%d without a write-back"
          % (rule, scope, CUTOFF, len(blocks), len(rounds),
             ", ".join("%s %d" % kv for kv in sorted(srcs.items())) or "nothing",
             len(rows), len(pairs), len(nonterm), len(scoped), len(found)))
    print("  read: %s" % src)
    void = [w for w, bad in (("no ROUND block", not rounds), ("no ledger row", not rows),
                              ("no (block, row) pair", not pairs)) if bad]
    if void:
        print("GHOST_ROUNDS_VOID  %s parsed -- NOT a pass." % " and ".join(void))
        print("  A check that read nothing is a null medium; a clean result from it would be")
        print("  the check-that-cannot-fail.")
        return 2

    for b, rid, state, where, how in found:
        tag = "GHOST" if b["landed"] > CUTOFF else "ARCHIVED"
        if tag == "ARCHIVED" and not listing:
            continue
        print("  %-8s %-22s %-8s named in the %s of %s (round %s, landed %s, line %d) -- no %s"
              % (tag, rid, state, where, ("#" + b["rnum"]) if b["rnum"] else "an unnumbered block",
                 b["date"], b["landed"], b["line"], how))
    if live:
        print("GHOST_ROUNDS_FAIL  %d row(s) named by a round block that landed after %s carry "
              "no write-back" % (len(live), CUTOFF))
        print("  Close the row, or record the round on it -- name `#NNN` in its state_note or an")
        print("  entry.  Inside the landing commit the number is knowable; the sha is not.")
        return 1
    print("GHOST_ROUNDS_PASS  %d archived (landed on/before %s), 0 new" % (len(found), CUTOFF))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
