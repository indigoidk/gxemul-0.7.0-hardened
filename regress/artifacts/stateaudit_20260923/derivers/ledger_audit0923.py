import io, json, shutil
# Records of the 2026-09-23 state audit (session GXEMUL [087a90]).  Every entry is [NOT A SEAT ANSWER]: the seats'
# own answers live in regress/artifacts/stateaudit_20260923/seats/.  The PEER's rows (alphavmkill, alphaifetchkill,
# cxseatcheck, lcaisaphys, lcalenzerodrop, dev_lca.c rows) are deliberately NOT touched.  Format preserved exactly:
# CRLF, indent=1, ensure_ascii=False, no trailing newline.
P = 'C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/pipeline/ledger.json'
BK = 'C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/verify_20260923/ledger.before_audit_20260923.json'
raw = io.open(P, encoding='utf-8', newline='').read()
L = json.loads(raw)
assert json.dumps(L, indent=1, ensure_ascii=False).replace('\n', '\r\n') == raw, 'format round-trip failed -- refusing'
shutil.copyfile(P, BK)
A = 'regress/artifacts/stateaudit_20260923/'
BY = '[NOT A SEAT ANSWER] Filed by GXEMUL [087a90] (main loop) from the 2026-09-23 records audit (' + A + \
     '; seats codex GPT-6 Astra + grok 4.7 x2 rounds, fable 5.1 last, identity verified).  '
D = '2026-09-23'
rows = {r['id']: r for r in L['rows']}
def entry(phase, note, ev=''):
    return {'phase': phase, 'seat': 'fable5', 'date': D, 'grade': '', 'grader': '', 'ev': ev, 'note': BY + note}
def add(rid, phase, note, ev=''):
    assert rid in rows, rid
    rows[rid].setdefault('entries', []).append(entry(phase, note, ev))
    print('entry ->', rid)

add('stagetokens', 'review',
    "L4 -- entry [18]'s 'ALL REPAIRED' is FALSE for one half of its Q4 item 1.  The finding "
    "(_scratchpad/panel_20260918_124702/codex.txt) had two halves: the CLOSURE half ('a closed row passes H and I; the wall "
    "omits it'), which WAS repaired (CHANGELOG #534, 'A closed row cannot hide a hold behind zero answers or a malformed "
    "marker'), and the DASHBOARD half ('The dashboard's malformed-marker fallback also disappears when the filer has an "
    "answer'), which was NOT: tools/pipeline/gen_dashboard.py:143-146 keeps the fallback inside `if not ents:` and :173 "
    "excludes held records from an answered seat's cell -- both written by 09ded75 itself.  Settled by reading the code "
    "(codex round-2 claim 081: ABSENT; grok: 'half-fix'), upheld by Fable 5.1, which struck codex's supporting citation "
    "(fable5_lastseat.md:36 is about t_selflate, not this).  The dashboard half is FILED as `dashmalformedheld`.",
    A + 'DISPOSITIONS_r2.md')

rows_new = [{
    'id': 'dashmalformedheld',
    'title': "gen_dashboard.py: a malformed hold filed AFTER a seat's answer renders as the plain answer -- #534's fallback "
             "lives only in the no-answer branch (:143-146) and :173 drops held records from an answered seat's cell",
    'sev': 'LOW', 'state': 'open', 'opened': D, 'commits': '',
    'witness': "none -- found by READING (codex 2026-09-18 Q4 item 1, second half); not measured.  A display defect: the "
               "closure checks (H, I, the wall) already refuse the case.",
    'hold_question': '',
    'entries': [entry('assess',
        "The unrepaired half of `stagetokens` entry [18]'s 'ALL REPAIRED'.  Consequence: a hold marker in no parseable "
        "shape, filed on a stage after that seat's answer, is invisible on the dashboard -- the cell shows the answer.  "
        "Fix shape (not built): take the malformed-marker fallback out of the `if not ents:` branch, or annotate it into "
        "the answered cell's tip.  Owes a fixture both ways.", A + 'DISPOSITIONS_r2.md')],
}]

add('gdromdmadefault', 'review',
    "Entry [11]'s 'FOUR APPLIED' is true of two sites and false of a third.  The `dma alias` correction IS at "
    "regress/gdrom_default_probe.py:160-166 and :1608-1610 (working tree only; HEAD has neither) and was MISSED at "
    ":1186-1187, which still says 'BOTH are on the ARMING arm' -- and ':1186' calls that sentence 'true when written', "
    "which it never was (dma alias is a default:-arm store at +0x05).  A sibling miss, found by the audit's reverse "
    "reconciliation and corrected in its wording by Fable 5.1 (the audit's own brief had called it 'never applied', and "
    "both round-2 seats ratified that).  OWED with the uncommitted repairB/U5 work, by its owner; not edited by the audit.",
    A + 'DISPOSITIONS_r2.md')

add('n6', 'review',
    "Durable copy MADE: regress/artifacts/n6/p1_20260919/fable5_p1_20260919.md, from _scratchpad/n6/fable5_p1_20260919.md "
    "(cmp-verified).  Entry [21] cited that durable path and it had never been populated -- a volatile-path defect in "
    "this session's own #539 records, found by the audit's citation check.",
    'regress/artifacts/n6/p1_20260919/fable5_p1_20260919.md')

add('ip30abortkill', 'review',
    "Durable copy MADE: regress/artifacts/ip30abortkill/PROBEATTACK_grok_20260917.txt, from "
    "_scratchpad/grokpush_20260917/grok_ip30probeattack.txt (13,519 b, cmp-verified).  Entry [15] cited that path and it "
    "had never been populated.  Identified by its mutant names (M_tick_abort, M_tick_bit49: 4 hits) -- entry [15] "
    "PARAPHRASES the file rather than quoting it (Fable 5.1).",
    'regress/artifacts/ip30abortkill/PROBEATTACK_grok_20260917.txt')

add('pcc2genctlc040alias', 'review',
    "CHANGELOG.md's #517 heading ('the second definition was a different register's bits') CORRECTED IN PLACE (L4) in the "
    "working tree, uncommitted: 0x03 is FAST | MIEN, two other bits of the SAME General Control Register, as the block's "
    "own body says.  Flagged by entry [10] on 2026-09-18 and corrected nowhere until today.", 'CHANGELOG.md')

rows_new.append({
    'id': 'stateaudit0923',
    'title': "2026-09-23 state audit after the 09-22 Windows-Update reboot: nothing on disk lost; the records and the tree "
             "disagree in ten places, all pre-reboot; gate 6 is red at HEAD; thirteen exemptions lapse 2026-09-28",
    'sev': 'HIGH', 'state': 'open', 'opened': D, 'commits': '',
    'witness': 'harness:' + A + ' -- name-status vs refs/snapshots (0 deleted), 883 + 1650 cited paths resolved, 81 '
               'applied-change claims reconciled by two seats, gate-6 census measured on a pure HEAD export',
    'hold_question': 'Owner: (1) the census population and one bulk pin re-derivation before the 2026-09-27 battery; '
                     '(2) the thirteen exemptions lapsing 2026-09-28; (3) the #545 commit and its Fable hold; (4) commits '
                     'of the other sessions\' verified work since 2026-09-17; (5) the never-commit list vs section J.',
    'entries': [entry('assess',
        "Full record: " + A + "FINAL.md.  Discrepancies D1-D10 (all present in the 2026-09-21 snapshot): gdromdmadefault "
        "[11] sibling miss; stagetokens [18] half-repaired (-> dashmalformedheld); #539's CHANGELOG green-line claim never "
        "shipped (corrected in place); #517 heading (corrected in place); this session's #545 draft (corrected; M9 "
        "re-measured on the final 37-row probe 33/37, regress/artifacts/fbd5/r3_m9_20260923/); two durable copies never "
        "made (made today); 18 artifact dirs cited by COMMITTED records with no tracked file; stale numbers in #529's "
        "uncommitted comments; older evidence gaps (08-27 ollama_ name mismatches, a mis-pathed alphatbinegsel citation, "
        "armbdt/passD/fable_floor_20260911.md never made, regress/fable5_2026-08-15.md nowhere); gate 6 RED AT HEAD "
        "(pty 70/46, promptless 40/20, anchor 24/23, echo 24/23, whole-buffer 3/2).  The peer's #540-#544 work that no "
        "snapshot held is copied, never edited, to " + A + "peer_carriers/ (1170 files, cmp+md5 verified).  Findings "
        "still carried ONLY by uncommitted drafts: armdesc3kill, armdacr2kill, fbirqsoftunimpl, hygienecensus, "
        "upstreamdeleteprose (_scratchpad/fbd5/records/bugs_draft545.md) and the peer's six #542 filings.",
        A + 'FINAL.md')],
})
for r in rows_new:
    assert r['id'] not in rows, r['id']
    L['rows'].append(r)
    print('row   ->', r['id'])
out = json.dumps(L, indent=1, ensure_ascii=False).replace('\n', '\r\n')
io.open(P, 'w', encoding='utf-8', newline='').write(out)
chk = io.open(P, encoding='utf-8', newline='').read()
assert chk == out and not chk.endswith('\n')
print('ledger written: %d -> %d bytes; backup at %s' % (len(raw.encode('utf-8')), len(out.encode('utf-8')), BK))
