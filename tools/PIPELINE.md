# Multi-LLM Fix Pipeline — portable methodology

> Supplied by the project owner 2026-08-15 (pasted into the loop four times — adopted as a
> standing directive). Saved verbatim below; the GXemul-specific adoption mapping lives at the
> end and in CLAUDE.md. Its own rule applies to itself: nothing lives only in a chat context.

A project-agnostic method for running bug fixes through a panel of LLMs, with one flagship model
holding final say. Distilled 2026-08-15 from a working emulation-accuracy project; every rule here
was either measured to matter or added by the project owner after seeing the alternative fail.

---

## 1. The panel

Use as many distinct model families as you can run. Two classes of seat, by what they can see:

| class | what it does well | what it must never be asked |
|---|---|---|
| File-reading (CLI/agent seats with repo access) | "What is true of the repository/artifact?" — independent derivation, per-diff review, source verification | to review through a summary someone wrote for them |
| Packet-fed (API seats given a self-contained text packet, NO file access) | attack reasoning: "refute this claim", "is this criterion sufficient?", "what would break this fix?" | anything requiring facts not in the packet — their blindness is a feature, keep it |

One model is the flagship (judge). Record every seat as `name + version + effort level`.
The flagship can rotate; when it does, its conflict-of-interest set rotates with it.

Measured lesson (the reason for the two classes): on a spend-or-drop vote, 4/4 file-reading
seats voted one way and 2/2 packet-fed seats the other — both packet seats citing a false sentence
the packet's author had written. Packet-fed review inherits the packet author's errors silently.
A packet can carry an argument to test; it cannot carry the repository. Never count the two classes
as equivalent votes on a question of fact, and record which class each seat was in.

## 2. The four phases — every phase full-panel, flagship closes each

| phase | file-reading seats | packet-fed seats | flagship closes with |
|---|---|---|---|
| 1 Assessment | independently characterize the bug — no shared packet (a shared brief = the author's errors, inherited) | attack the bug claim: prove it's not a bug / not yours / already fixed | a problem statement of record + an evidence grade |
| 2 Research | each proposes a fix WITH its grounding (spec section, datasheet, measured behavior — or an honest UNKNOWN) | attack the proposals: name what regresses under each | one chosen approach + named rejected alternatives (a do-not-relitigate list) |
| 3 Final review | per-diff review of the actual change + message truth check (does the commit message claim only what the diff does?) | attack the final diff's reasoning and its stated claims | the adjudication — last say |
| 4 Regression | verify test logs against pre-registered expectations; name the cross-consumer control up front | attack the test design: "what would this suite miss?" | pass/fail on the pre-registered predicate |

Rules that bind the phases:

- **Halt at every phase boundary.** The flagship's closure is presented to the owner as an explicit
  question, never a line in a status report, and the next phase dispatches only on their go.
- **Floor, not ceiling.** A phase closes when every seat has been heard at least once — but one
  round per seat is a floor. Follow-up rounds, targeted re-dispatches, and seat-vs-seat challenge
  through the coordinator are all allowed inside a phase.
- **Full-panel-or-pause.** If a seat is down mid-phase, that bug's phase pauses (it does not proceed
  short-handed); other bugs keep flowing. The pause is per-fix, never global.
- **Rejected bugs are still recorded.** "Not a bug" is a finding with a row, per-seat inputs, and a
  ruling — it feeds the do-not-relitigate list.
- **Round sizing:** substantive fix = 4 separate rounds; trivial fix = 2 dispatch rounds
  (assessment+research combined, review+regression combined) — same four columns recorded.
- Multiple bugs run concurrently, each waiting at its own boundary.

## 3. Conflict of interest (the rule that actually catches things)

A model may not clear an artifact it helped author. Eligibility is per-artifact, checked
against the artifact's recorded authoring participants — never assumed from memory. When the
flagship judges work its own model authored (common when the flagship also drafts), the ruling
carries a visible "author self-review (disclosed)" badge rather than silence. Same-model
replication (two instances of one model) is disclosed as weaker than two-family certification,
never passed off as it.

Measured lesson: a flagship seat, told plainly it was reviewing its own lineage's ruling and
handed contrary evidence, wrote: "I adopt the correction against my own lineage's ruling, as the
record requires." Ask for exactly that behavior; badge it when you get it.

## 4. Evidence discipline

- Evidence ladder, on every claim: `CONFIRMED w/ source` > `MANUAL` (documented) > `BELIEVED`
  (inferred) > `UNKNOWN`. An honest UNKNOWN outranks a confident guess.
- Every ledger entry names a real file. An entry with no artifact behind it is not evidence.
- Verbatim seat outputs are banked under `evidence/<row>/<phase>/<seat>_<date>.md` — raw, not
  summarized. A new model joins by reading the row directory; nothing lives only in a chat context.
- A zero result is evidence only if the probe is proven capable of a non-zero result. Before
  trusting "no failures found", show the detector detecting a failure elsewhere.
- Co-occurrence is not attribution. A document that lists all your items does not count as a
  review of any one of them; only artifacts that name the item specifically do.
- Pre-register regression predicates before the run, so a pass cannot be redefined after.

## 5. The ledger-first dashboard

One machine-readable ledger (JSON) is the single source of truth: seats, phases, rows, entries
(seat, date, disposition, evidence path, flags). A small generator renders the dashboard from it.
Write the ledger first, regenerate, republish — never hand-edit the dashboard. A dashboard cell
without a ledger entry behind it is a defect.

Rendering conventions that proved worth it:

- Minimal cells: a colored glyph (✓ approved · ⏸ held · ✕ concern · … pending) plus a small
  badge (A = author self-review; s = same-model subagent; ? = attribution unverified). Date,
  disposition, note, and evidence path live in the hover tooltip.
- Diagonal column headers, one per seat: `Name Version (Effort)`; model id in the tooltip.
- Hold tags: when a row is held or blocked by another fix, show ⏸ + a short reason + "waiting
  on X" right on the row, detail on hover — so a stall is never invisible.

## 6. Seat operations (the operational traps, all hit in practice)

- Echo-test availability: put a nonce in the prompt and a second nonce in a file; require both
  back. Distinguishes launcher faults from real outages. An outage is a timestamped observation,
  never a standing property — re-test before routing around a seat; stale "down" records cost this
  project three times.
- Transport: drive API-class seats via plain HTTP (one POST, non-streaming), banking a receipt
  (endpoint, packet SHA-256, body SHA-256, status, bytes, timestamps). Avoid interactive CLI
  wrappers for packet delivery — one measured CLI greedily opened "filenames" it found inside packet
  prose. Avoid agent-gateway frameworks for packet seats: giving an attacker seat file access
  destroys the one property that makes it useful.
- Long dispatches truncate. Put the verdict line FIRST in the requested output format, so a cut
  output still carries the answer. Read truncated fragments anyway — they carry real findings.
- A seat that finishes the work but can't write its file still has the answer in its log —
  treat the log as the deliverable of record.
- Fold results incrementally with an idempotent script (safe to re-run as batches land).

## 7. The synthesis round that made dissent useful

When attackers dissent from the file-readers' consensus, do not just outvote them. The flagship
records the dissent and why it is discounted (usually: it objects to evidence the seat could not
see), preserves its valid residue into the next phase's agenda — then, if the owner wants, run a
round 2 targeted at the dissenters only: hand them the specific evidence their objections named
as missing, inlined, plus an honest section on what genuinely remains open, and ask them to re-judge
objection by objection. Measured result: both dissenters reversed, retracting each objection
individually — turning a 7-2 split into 9/9 unanimity that actually means something.

## 8. Minimum viable adoption

Pick seats; classify file-reading vs packet-fed; name the flagship. Record model+version+effort.
Create the ledger JSON + a generator; publish the dashboard somewhere stable.
For each bug: full-panel Assessment (independent derivation + claim-attack) → flagship closure →
ask the owner → Research → ask → Final review (per-artifact conflict check first) → ask →
pre-registered Regression → ask. Bank everything, badge self-review, record rejections.
Keep one list of standing owner decisions, and surface every gate as a direct question.

---
---

# GXemul adoption mapping (2026-08-15)

**Seats and classes** (the 9-seat roster, now classified per §1):

| seat | class | notes |
|---|---|---|
| **Fable 5 (max)** — main loop | file-reading | **FLAGSHIP** (adjudicator by standing directive; session model as of 2026-08-15) |
| Opus 5 — Agent measure seat | file-reading | compiles AND runs; overturned the main loop 10+ times |
| Codex 5.6-SOL (xhigh) | file-reading | discloses read-only sessions honestly — then it is a READING |
| agy 3.7 (`gemini-3.7-flash-high`, high) | file-reading | via `--add-dir` |
| Grok 4.6 (xhigh) | file-reading | `--prompt-file`, immune to the argv cap |
| Kimi 3 (`kimi-code/k3`) | file-reading **+ measuring** | runs its own probes; held the adjudication alone 2026-08-15 |
| Ollama glm-5.2:cloud | **packet-fed** | the honest exemplar: *"no files read... the prompt's, re-stated"* |
| Ollama deepseek-v4-pro:cloud | **packet-fed** | stalls if asked to read files — a brief defect, not an outage |
| Ollama minimax-m3:cloud | **packet-fed** | same; answered 12 KB the first time a brief inlined everything |

**Already our practice under other names** (§1's measured lesson = our "the cloud seats cannot
read files and the brief decides whether they answer"; §4's zero-result rule = our "a check that
cannot fail is not evidence — negative-test it"; §4's pre-registration = the battery's four
pre-declared signals; §4's banked outputs = `_scratchpad/panel_<timestamp>/` raw seat files;
§7 = "disagreements are settled empirically, never by vote").

**Newly adopted from this document:**
1. **Conflict-of-interest badging (§3).** The main loop both authors and closes; the Opus seat is
   same-family with an Opus main loop. Neither was ever disclosed. The ledger now badges `A`
   (author self-review) and `s` (same-model replication) wherever they occurred — including
   retroactively on tonight's rounds.
2. **Evidence ladder vocabulary (§4)** — CONFIRMED/MANUAL/BELIEVED/UNKNOWN on ledger entries.
3. **Verdict line FIRST (§6)** in every panel brief's requested output format.
4. **Echo-test with a file nonce (§6)** for seat health — distinguishes launcher faults from
   outages (the minimax misdiagnosis would have been caught by this).
5. **The ledger + generated dashboard (§5, §8)** — `pipeline/ledger.json` +
   `pipeline/gen_dashboard.py`, never hand-edited.

**Two recorded divergences, held deliberately (owner directives on file):**
- *Halt at every phase boundary and ask* (§2) vs the standing self-sustaining loop, which runs
  unattended and stops only for destructive actions or genuine scope changes. THE LOOP DIRECTIVE
  IS THE OWNER'S AND MORE RECENT for this project; gates are surfaced in reports and the
  checkpoint rather than as blocking questions. For any NEW project adopting this pipeline,
  §2's halt rule applies as written.
- *Full-panel-or-pause* (§2) vs our degrade-and-record: with Fable quota-dead for days, pausing
  every fix would have stopped the project. The owner's newer directive (Kimi may hold the
  adjudication alone; a dead seat is a SEAT FAILURE, recorded by name, never counted as
  agreement) governs here.
