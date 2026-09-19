# J3 -- three small rows on `tools/pipeline/check_probe_wiring.py` and one gated probe: choose a disposition for each

## READING SCOPE AND FORM

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (git HEAD cdbe7d7).  Pristine 2021 copies of GXemul
under the project root (`./src/`, `_archive/`) are NOT this fork.  Do not read `regress/artifacts/`, the ledger, the
CHANGELOG or OUTSTANDING_BUGS; the facts you need are here.  Read-only: no edits, builds or runs.
VERDICT LINE FIRST.  Mark claims READ (file:line), REASONED or NOT CHECKED; counts carry denominators; check the
premises rather than ratifying them.

`check_probe_wiring.py` is a pre-commit checker: it classifies every `regress/**/*.py` (MANIFEST), requires each
DETECTOR to be run by some gate script, and carries dated exemptions (EXEMPT) that expire (`d < today`).  Its
`--selftest` applies 22 mutants to copies of itself and the gates (M0..M15) and precommit pins that count.

## ROW A -- `exemptcal` (LOW): calendar validity of exemption dates

`DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")` accepts `2026-09-99`.  Production compares the strings (`d < today`),
so an impossible date passes today and "expires" at a lexicographic boundary; the selftest's M5 derivation calls
`date.fromisoformat()` on the earliest dated detector exemption and would die with an uncaught ValueError instead
of a named FAIL.  All eleven real dates are valid today.
  Q: cite DATE_RE, every place `d < today` / `fromisoformat` is used, and the MALFORMED EXEMPTION branch.  What is
  the smallest change that makes an impossible date a MALFORMED EXEMPTION in production AND a named FAIL in the
  selftest, and which selftest case (new or existing) would pin it?  Is a `--today` value also unvalidated?

## ROW B -- `m5dayb` (LOW, optional): a 23rd selftest case

The selftest's M5a runs on the earliest stamped date itself (green) and M5b the day after (red); both days are
DERIVED from the table.  A measured matrix (six one-token forms of the expiry comparison x three layouts) showed
that the day-BEFORE case (M5a0) is the only case that catches `!=` deterministically; without it `!=` is caught
only by M0/M2b reading the real clock, i.e. on every day except the stamped date.  `<=` is caught by M5a-on-date.
  Q: read the M5 block and `_pick_exempt_detector()`.  Would adding M5a0 change any other case's meaning?  What is
  the exact precommit pin to raise (cite the line in `tools/precommit_check.sh`)?  Disposition: add it now, keep it
  filed, or drop it -- and the fact that decides it.

## ROW C -- `hpcmipsc2` (LOW): a gated probe's control borrowed from a live defect

`regress/hpcmips_ctor_probe.py` (wired into `regress/gate_arm.sh` by #536) has row C2, which requires the
construction of machine `mvme1600` (`-E mvmeppc -e mvme1600`) to ABORT, classified `ABORT_OTHER`, as its
"unrelated-abort" control.  That abort is a LIVE defect in `bus_pci_add()` ("pci_data == NULL!").  A round that
fixes mvme1600 turns C2 red.  Row F3 in the same probe covers the classifier with a SYNTHETIC abort.
  Q: cite C2, F3 and the classifier.  Does F3 already prove everything C2 proves?  If C2 is re-based on a
  synthetic abort, what does the probe LOSE (a real-emulator abort path vs a synthetic one)?  Is there an abort in
  the tree that is DELIBERATE and permanent (a documented refusal) that C2 could use instead?  Disposition.

## ROW D -- the EXEMPT block's own prose

The block's comment said every exempt probe "already prints a verdict token and exits nonzero on failure"; that was
false of `mk48_nvram_probe.py` (it prints `MK48_RESULT=n/m` and a DONE sentinel, exits 0 with rows red) and was
corrected for that probe.  Q: for the ELEVEN probes still in EXEMPT (`fbpending_drain_probe.py`,
`wdc_altoffset_probe.py`, `wdc_altoffset_sig_probe.py`, `wdc_altoffset_4bit_probe.py`, `wdc_addtoinbuf_probe.py`,
`ppc_rldicl_probe.py`, `alpha_tbi_probe.py`, `lca_badval_probe.py`, `lca_widewrite_probe.py`,
`lca_isalane_probe.py`, `artifacts/ip30abortkill/ip30_abort_probe.py`), open each and report: verdict token
printed (which), exit status on a red row (0 / nonzero), completion sentinel.  A table, 11 rows.

**Standing licence:** anything else found while verifying.
