#!/usr/bin/env python3
"""PRECOMMIT SECTION P2 (#587, ledger row `ghostround`): A ROUND BLOCK'S ROWS MUST RECORD THE ROUND.

HARD by owner ruling 2026-11-06.  The census, the replay and the controls that set its shape are
regress/artifacts/ghostround/census_20261106/ (DECISION.md first); the wired section's own controls
are regress/artifacts/ghostround/wired_20261106/ (RECEIPT.md first).

THE DEFECT, measured 2026-08-29: `#479` shipped on 2026-08-27 (2343036) and its CHANGELOG block named
three rows -- `wdcwipclear`, `wdcringnoflush`, `wdcstalephase`.  Two days later all three were still
`in work` with nothing on them about the ship, and a nine-seat panel was fired to redo shipped work.
The CHANGELOG knew; the ledger did not.  Section H cannot see it: it reads ledger entries and skips
stages that never started.

THE RULE (existence-only).  For every ROUND block of CHANGELOG.md, each row the block names IN ITS
HEADER and each named row still `in work` must be `closed`/`dropped`, or its record must name the
round -- the block's own number (`#479`, or `Round 479`) in the row's state_note, hold,
hold_question, closure, witness, commits or note, or in an entry dated on or after the round.  It
checks that a write-back EXISTS, never what it says.  Each choice was measured, not assumed, by a
replay of 141 landing commits since 2026-08-17 (census_20261106/replay.out, replay_class.tsv):
  * the row's own wording, "an entry dated on or after the round", catches 2 of the 11 documented
    ghosts -- entries carry a date and no time, and the pre-ship stages run on ship day;
  * checking EVERY named row fails 76 of the 141 landings, because a round block also names the
    rows it files and its neighbours;
  * this rule catches 11 of 11, and would have failed 20 landings (13 with a real gap) -- 2 of
    the 32 since October, both references.
A sha in `commits` alone is not a write-back (`--accept-commits` makes it one): `#526`, `#527` and
`#528` carried only their landing sha, still `in work`, for 36 days.  A ROUND block with no number
of its own falls back to the date rule.  NOT checked: an `open`/`held` row named only in a block's
body -- there a filing and a reference look the same.

FORWARD-ONLY.  A block that LANDED on or before CUTOFF (git blame's date for its header line) is
reported with --list and never fails; a later one fails.  A block not yet committed lands today --
and so does an OLD block whose header line is being edited: blame gives the edited line the all-zero
sha, so from that commit on the block is enforced and owes the write-back its rows lack.  Measured:
`#557`'s header blames e1871fa5 unmodified and the all-zero sha after a one-space edit
(wired_20261106/HEADER_REDATE.out).  An edit can make an old block newly ENFORCED, never newly exempt.

WHAT IT READS IS THE INDEX, AND A READ THAT FAILS IS VOID.  CHANGELOG.md and tools/pipeline/ledger.json
come from the INDEX (`git show :<path>`; dates from `git blame --contents`), so a peer's uncommitted
edits in a shared working tree cannot fail an unrelated commit -- the narrowing sections A and B made
for the same reason.  If either `git show` or the blame fails, or the blame dates fewer lines than the
file holds, the result is GHOST_ROUNDS_VOID (exit 2): never the working copies, never the header dates.
(This said "what it reads is what is being committed" while a failed read fell back to the working
copies behind a `note:` the hook did not show, and a failed blame to the header dates; three review
seats found it.  Then it said "if either `git show` or the blame fails" while a blame that exited 0 and
dated fewer lines left the undated headers to their own text; the repair's pass 2 found it.)
`--at=REV` replays a commit read-only from git and is VOID on the same failures.  `--worktree` reads
the working copies; GXLEDGER / GXCHANGELOG read given files (the controls' mode: dated by blame when the
file is committed in a repo, else by its headers); `--no-git` dates by headers only.  GXGHOST_CUTOFF and
GXGHOST_TODAY set the two dates.  Section P2 runs this with all five GX* names cleared (`env -u`).

THE CONTRACT -- every cell of what it reads and what the hook does with its verdict, and the leg that
pins each (wired_20261106/run_checker_controls.sh; the mutants, run_mutants.sh; Fable 5.1's ruling of
2026-11-07, s.4, wired_20261106/REPAIR_RULING.md):
  --at    git show fails, either read or both: VOID (no leg -- the hook never runs --at, and before the
          repair it was a SystemExit, rc 1, never a pass).
          blame fails: VOID (c4d; mutant M9).  blame dates fewer lines than the file: VOID (c8k; M10).
          ledger not JSON: a traceback, rc 1, which P2 hard-fails (no leg; disclosed).
  index   git show fails -- either read, or both: VOID (c8h both; c8l the ledger alone, c8m CHANGELOG
          alone -- the guard tests the two reads separately, so a one-sided fallback is its own cell;
          M15, M16, the pre-repair checker).  blame fails: VOID (c8i; M14, the pre-repair checker).
          blame dates fewer lines: VOID (c8j; M10).  ledger not JSON: as --at.
          A temporary index (GIT_INDEX_FILE: `git commit -a`, a partial commit) is the one read (c8g; M5).
  file mode (--worktree, GXLEDGER/GXCHANGELOG): header dates where git cannot date -- BY DESIGN (c1-c3;
          c6 is file mode where git CAN date, by blame); --no-git: header dates by design, no leg.
  hook    the PASS token: ok (the GREEN run).  rc 0 with no token: a hard FAIL (c9c; M8).  FAIL: a hard
          FAIL naming each row (c9a, c9b; M1, M7), counted in `fail` (HOOK-fail=1; M13).  VOID: a hard
          FAIL (c9e; M12).  A crash: a hard FAIL through the same branch as c9c (disclosed).  The five
          GX* names are cleared (c9b exports GXLEDGER; the other four are pinned by M7's find-text -- a
          presence pin, not a behavioural leg); GIT_INDEX_FILE is NOT (c9d; M11).
A repository whose object format is not SHA-1 is VOID: the porcelain parser reads 40-hex shas.

"NAMED" is check_bugfile_sync.py's idiom: in the BODY, a code span that is exactly a row id, or a
comma/plus/slash list whose every member is one; in the HEADER the same, or a subject position --
an element of a parenthesised list (`(lecsrmask)`, `(sgirekills, the MTE half)`) or the word right
after the round marker (`Round #504 sgirandompixel`).  Never a bare word elsewhere in a header: row
`census` is also an English word.  Fenced code is skipped: it is quoted output, not a claim.

Options: --list (ARCHIVED hits too), --rule=date, --scope=all (the measured alternatives).
Exit 0 clean; 1 on a hit in a block that landed after CUTOFF; 2 VOID -- a read this mode depends on
failed or came back short, or no round block, no ledger row or no named row was read.  A check that
read nothing is not a pass.
"""
import datetime
import io
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.abspath(os.environ.get("GXSEC") or os.path.join(HERE, os.pardir, os.pardir))
LEDGER_REL = "tools/pipeline/ledger.json"
CHANGELOG_REL = "CHANGELOG.md"
LEDGER = os.environ.get("GXLEDGER") or os.path.join(SEC, "tools", "pipeline", "ledger.json")
CHANGELOG = os.environ.get("GXCHANGELOG") or os.path.join(SEC, "CHANGELOG.md")

#  The census date at HEAD 2632277f: every hit already in the file is reported and none fails -- until
#  its block's header line is edited (FORWARD-ONLY above).
CUTOFF = os.environ.get("GXGHOST_CUTOFF") or "2026-11-05"
TODAY = os.environ.get("GXGHOST_TODAY") or datetime.date.today().isoformat()

#  The states that occur are closed, dropped, held, "in work" and open; the first two owe nothing.
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


def header_date(header):
    best = None
    for p in HEADER_DATE:
        m = p.search(header)
        if m and (best is None or m.start(1) < best.start(1)):
            best = m
    return best.group(1) if best else ""


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


def git(args, cwd=SEC, timeout=300):
    """(rc, stdout bytes); rc 127 when git cannot be run at all."""
    try:
        p = subprocess.run(["git", "-C", cwd] + list(args), capture_output=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return 127, b""
    return p.returncode, p.stdout


def git_show(rev, relpath):
    """`rev:path` from git; rev "" is the INDEX (`git show :path`)."""
    rc, out = git(["show", "%s:%s" % (rev, relpath)])
    if rc != 0:
        return None
    return out


def porcelain_dates(out):
    """{1-based line: (YYYY-MM-DD, sha)} from `git blame --porcelain` output.  A line git reports
    as not yet committed (the all-zero sha) lands TODAY, which is what it is."""
    times, lines, cur = {}, {}, None
    for raw in out.decode("utf-8", "replace").split("\n"):
        if raw.startswith("\t"):
            continue
        m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", raw)
        if m:
            cur = m.group(1)
            lines[int(m.group(2))] = cur
            continue
        if cur and raw.startswith("committer-time "):
            times.setdefault(cur, [None, "+0000"])[0] = int(raw.split()[1])
        elif cur and raw.startswith("committer-tz "):
            times.setdefault(cur, [None, "+0000"])[1] = raw.split()[1]
    res = {}
    for ln, sha in lines.items():
        if set(sha) == {"0"}:
            res[ln] = (TODAY, "")
            continue
        t, tz = times.get(sha, [None, "+0000"])
        if t is None:
            continue
        off = (1 if tz[0] == "+" else -1) * (int(tz[1:3]) * 3600 + int(tz[3:5]) * 60)
        res[ln] = (datetime.datetime.fromtimestamp(t + off, datetime.timezone.utc)
                   .strftime("%Y-%m-%d"), sha)
    return res


def blame_rev(rev):
    """{line: (date, sha)}, or None when git cannot blame -- which the caller turns into VOID."""
    rc, out = git(["blame", "--porcelain", rev, "--", CHANGELOG_REL])
    return porcelain_dates(out) if rc == 0 else None


def blame_contents(data):
    """Blame CHANGELOG.md as if it held `data` (the index's bytes) -- lines HEAD lacks are new.
    None when git cannot blame: the caller turns that into VOID, never into header dating."""
    fd, tmp = tempfile.mkstemp(suffix=".changelog")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        rc, out = git(["blame", "--porcelain", "--contents", tmp, "--", CHANGELOG_REL])
    finally:
        os.remove(tmp)
    return porcelain_dates(out) if rc == 0 else None


def blame_file(path):
    d = os.path.dirname(os.path.abspath(path))
    rc, _ = git(["rev-parse", "--show-toplevel"], cwd=d, timeout=30)
    if rc != 0:
        return {}
    rc, out = git(["blame", "--porcelain", "--", os.path.abspath(path)], cwd=d)
    return porcelain_dates(out) if rc == 0 else {}


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


class Void(Exception):
    """A read the mode depends on failed.  The verdict is VOID (exit 2) -- never a fallback."""


def nlines(b):
    """The lines of `b` as git blame counts them: a last line without a newline is a line."""
    return b.count(b"\n") + (0 if b.endswith(b"\n") or not b else 1)


def complete(bl, cb, what):
    """`bl` once it dates EVERY line of `cb`; VOID when git could not blame (None) or dated fewer lines than the
    file holds -- a header line the porcelain parser cannot read (it reads 40-hex SHA-1 shas: every line of a
    repository whose object format is not SHA-1), or a sha with no committer-time.  An undated header would
    otherwise be dated by its own text: the fallback file mode and --no-git use BY DESIGN, never index or --at."""
    if bl is None:
        raise Void("%s failed in %s -- the blocks cannot be dated, and the header dates are not a substitute "
                   "(--no-git is the mode for them)" % (what, SEC))
    if len(bl) != nlines(cb):
        raise Void("%s dated %d of %d lines in %s -- an undated line is not dated by its header, and a repository "
                   "whose object format is not SHA-1 is VOID (the porcelain parser reads 40-hex shas)"
                   % (what, len(bl), nlines(cb), SEC))
    return bl


def load(argv):
    """(ledger dict, CHANGELOG text, blame, what was read); raises Void when git cannot read or blame, or
    the blame dates fewer lines than the file holds.

    INDEX MODE FAILS CLOSED.  A failed `git show :<path>` used to print a `note:` and read the working
    copies, and a failed blame returned {} so the header dates were trusted -- a fail-open path in the
    read the hook depends on, which section P2's PASS line hid.  Both are VOID now, and so is a blame
    that exits 0 short of the file (complete()); `--no-git` is the one explicit mode that dates by
    headers."""
    at = ([a.split("=", 1)[1] for a in argv if a.startswith("--at=")] or [""])[0]
    nogit = "--no-git" in argv
    if at:
        lb, cb = git_show(at, LEDGER_REL), git_show(at, CHANGELOG_REL)
        if lb is None or cb is None:
            raise Void("git show %s:%s or %s:%s failed in %s" % (at, CHANGELOG_REL, at, LEDGER_REL, SEC))
        bl = {} if nogit else complete(blame_rev(at), cb, "git blame %s -- %s" % (at, CHANGELOG_REL))
        return (json.loads(lb.decode("utf-8")), cb.decode("utf-8", "replace"), bl,
                "%s:%s and %s:%s" % (at, CHANGELOG_REL, at, LEDGER_REL))
    if not ("--worktree" in argv or os.environ.get("GXLEDGER") or os.environ.get("GXCHANGELOG")):
        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)
        if lb is None or cb is None:
            raise Void("git show :%s or :%s failed in %s -- the index being committed cannot be read, and "
                       "the working copies are not a substitute for it" % (CHANGELOG_REL, LEDGER_REL, SEC))
        bl = {} if nogit else complete(blame_contents(cb), cb, "git blame --contents <the index's %s>" % CHANGELOG_REL)
        return (json.loads(lb.decode("utf-8")), cb.decode("utf-8", "replace"), bl,
                "the index of %s (%s, %s)" % (SEC, CHANGELOG_REL, LEDGER_REL))
    ledger = json.load(io.open(LEDGER, encoding="utf-8", newline=""))
    return (ledger, read_text(CHANGELOG), {} if nogit else blame_file(CHANGELOG),
            "%s and %s" % (CHANGELOG, LEDGER))


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

    try:
        ledger, text, blame, src = load(argv)
    except Void as ex:
        print("GHOST_ROUNDS_VOID  %s -- NOT a pass." % ex)
        return 2
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
