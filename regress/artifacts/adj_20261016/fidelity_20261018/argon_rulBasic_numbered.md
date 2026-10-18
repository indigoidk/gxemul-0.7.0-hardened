ARGON_RULBASIC_20261018
VERDICT: ANSWERED (12 flags) -- F reverses Fable's F3/record-3 instruction, misstates F15's 1/3 overturn, fabricates 10 missing PSB items, and drops Grok's D1 runtime-vs-link distinction.

## 1. Line-by-line checks of F against S1, S2, S3

- `F:7-10`: HOLDS. Seat names, files, and top-level verdicts (`UPHOLD WITH CHANGES` with 3, 2, and 3 rulings changed) match `S1:3`, `S2:4`, `S3:5`.
- `F:16-20` (F1): HOLDS. 3/3 upheld (`S1:5`, `S2:8`, `S3:42`); Fable's measurement and clause `(e)+L3/L4` match `S3:32,42,58`; Grok's clamp observation matches `S2:8`.
- `F:21-22` (F2): HOLDS. 3/3 upheld (`S1:6`, `S2:10`, `S3:43`); Astra's F14 wording (`S1:38`) and Fable's `FROM BELOW` (`S3:43`) match.
- `F:23-25` (F3 / D3): BROKEN.
**B1** FLAG: `F:24-25` claims "Record 3 is then rewritten to describe the PINNED behaviour, which makes the cases-file sentence true rather than reversed", contradicting `S3:35` where Fable states the cases-file sentence "becomes TRUE under pin C instead of being rewritten to say the opposite" (while `S3:44,116` refers to rewriting Packet B's record 3, not the cases-file sentence).
- `F:26-34` (F4 / D2): HOLDS. Fable's refinement (`S3:37-38,45`), Astra and Grok upholding the single row (`S1:8,22`, `S2:14,42`), and Astra's outer-parenthesis warning (`S1:61`) match.
- `F:35-36` (F5): HOLDS. 3/3 upheld (`S1:9`, `S2:16`, `S3:46`); Fable's 122 `.c` files under `src/devices` matches `S3:46`.
- `F:37-40` (F6): BROKEN.
**B2** FLAG: `F:39` cites "(Fable; also `prescreen_asic.md` item 10)" for the stub's `struct cpu` surface, but all three seats report `prescreen_asic.md` does not exist on disk (`S1:117`, `S2:63`, `S3:15`).
- `F:41-43` (F7): BROKEN.
**B3** FLAG: `F:41` attributes the F7 refinement (`buf[9]`, `buf[16]`, `buf[64]`) to `(Grok; Astra)`, but only Grok refined F7 to add those three sizes (`S2:4,20,48`); Astra upheld F7 without naming those buffer sizes (`S1:11`, `S1:89`), and Fable upheld F7 as `static8` reentrancy only (`S3:48`).
- `F:44` (F8-F13): HOLDS. 3/3 upheld across `S1:12-17`, `S2:22-32`, `S3:49-53`.
- `F:45-46` (F14): BROKEN.
**B4** FLAG: `F:45` quotes Astra's F14 extent phrasing as `"at least eight accessible bytes at the passed pointer"`, which is not in `S1`; `S1:38` actually says `"eight accessible bytes at the passed pointer during the instrumented accesses"` while `"at least 8 bytes"` is Fable's F2 phrasing (`S3:43`).
- `F:47-49` (F15): BROKEN.
**B5** FLAG: `F:47` rules `F15 -- OVERTURNED (Astra)` without disclosing the 1/3 split: both Grok (`S2:36`) and Fable (`S3:55`) explicitly voted `F15 -- UPHOLD`, with Fable explicitly ruling that `"BUILT"` and the three `CLEAN`s are refuted by measurement.
**B6** FLAG: `F:48-49` attributes to Astra (or states without main-loop attribution) that "grok's panel CLEAN explicitly excluded the short-buffer case, so F2 does not refute it; F1 does", omitting that Grok itself (`S2:36`) and Fable (`S3:55`) both ruled that both F1 and F2 refute Grok's CLEAN.
- `F:50` (F16): HOLDS. 3/3 upheld (`S1:20`, `S2:38`, `S3:56`).
- `F:51-57` (D1): BROKEN.
**B7** FLAG: `F:52` claims Fable measured `buf16` green, whereas Fable's measurement table and prose (`S3:17,29`) name the medium `cand_buf16` (listing `buf16` only under `sizeof_both` and in `S3:43,98` shorthand).
- `F:58` (D4): HOLDS. 3/3 upheld (`S1:24`, `S2:46`, `S3:58`).
- `F:62-64` (Missed item 1): HOLDS. Matches `S3:94`.
- `F:65-66` (Missed item 2): HOLDS. Matches `S3:94`.
- `F:67-69` (Missed item 3): HOLDS. Matches `S1:94-96`.
- `F:70-72` (Missed item 4): BROKEN.
**B8** FLAG: `F:70` cites `Fable §3: sixteen parameter/extent cells`, whereas Fable's actual table in §3 (`S3:72-90`) contains 17 rows (Fable's summary prose at `S3:98` says `16 parameter/extent cells` by not counting the 17th row `the stub's struct cpu surface`).
- `F:73-76` (Missed item 5): BROKEN.
**B9** FLAG: `F:73-76` lists ten `prescreen_asic.md` LIVE items and routes them to packet D without stating this is the main loop's own addition, whereas all three seats (`S1:117`, `S2:63`, `S3:15,102`) testified that `prescreen_asic.md` was absent and there were zero LIVE items.
- `F:78-92` (Build list & Self-review): HOLDS on self-review summary (`S3:104-112`).

## 2. Seat findings, objections, or dissents omitted or contradicted by F

**B10** FLAG: `F:51-57` and `F:34` omit Grok's primary D1 change (`S2:4,34,40`): that `run_rc != 0` in `id_verdict` must not stay as-is because it conflates compile/link failure (VOID) with a runtime sanitizer abort after a successful link (row FAIL), which also changes Record 1's wording (`S2:34`).
**B11** FLAG: `F:26-34` and `F:80-85` omit Fable's explicit requirement (`S3:45,98,116`) to add the five other parenthesis/cast removals (`nooutparen` x3, `nocondparen`, `nocast`) to `DISCLOSES` as `EQUIVALENT` for in-tree use (naming `SYSASIC_EVENT_TO_ADDR(e) * 2` as the use that would see them), mentioning them only in passing as table-2 reclassifications at `F:63-64`.
**B12** FLAG: `F:51-57` and `F:80-85` omit Fable's explicit requirement (`S3:57,116`) to disclose `LeakSanitizer` in `DISCLOSES` (on by default under `-fsanitize=address`) and to add the `VOID` sentence to the gate 2 comment (`S3:57,116`).

## 3. Single line of F most likely to mislead a builder

`F:24-25`: "Record 3 is then rewritten to describe the PINNED behaviour, which makes the cases-file sentence true rather than reversed."
Why: In `sysasic_range_cases.c`, the existing comment ALREADY claims that a stub drifting on `MEM_WRITE` reds the committed header (`S2:12`, `S3:35`). Before Pin C, that comment in `cases.c` was false; Packet B's Record 3 had proposed rewriting the `cases.c` comment to say the opposite (`S3:35`). Under Pin C, the `cases.c` comment becomes true as-is and must NOT be rewritten (`S3:35`) — only Packet B's Record 3 summary is updated (`S3:44,116`). A builder acting on `F:24-25` can easily misread "Record 3" as referring to the comment in `sysasic_range_cases.c` (or believe `cases.c` currently says the reverse) and edit `sysasic_range_cases.c` when `cases.c`'s comment should be left untouched.

P-RULBASIC-ce73
RULBASIC: 19 ATTACKS 12 BROKEN 7 HOLDS 0 UNSETTLED DRAFTABLE:NO