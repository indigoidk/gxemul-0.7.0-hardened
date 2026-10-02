You are the second ADJUDICATOR (with the flagship seat) for a test-coverage change in a C hardware emulator (GXemul,
change #529 crimewidthkill: the SGI IP32 CRIME device's narrow-width accesses are declined and announced once, and a
226-row detector, `regress/crime_width_probe.py`, defends that).  Read-only; no file may be changed.  The flagship seat
has adjudicated the last review pass (repair 16's F2 pass) and ruled that the review chain CLOSES with no row owed and
thirteen text-only corrections; nothing is committed until you confirm.

Read, in this order:
1. The flagship ruling: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\repair16_f2_20260926\fable5_f2_adjudication.md`.
2. The packet it ruled on, `..\repair16_f2_20260926\f2_packet_codex_v2.md` (the label-corrected copy; the sent copy is
   `f2_packet.md` -- its E7/E10 labels are stale, which the ruling notes), and the seats' answers beside it:
   `codex_f2.txt`, `codex_f2ded.txt`, `grok_dedicated_f2.txt`, `opus5_f2.md` with `opus_f2\` (the measuring seat's runs),
   and the panel seats' files in `..\repair16_f2_20260926\panels\panel_20260926_053828\` (a durable copy of the
   panel directory `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260926_053828\`).
3. The measurements: `..\table15a_20260926\` and `..\table16_20260926\` (`PRETABLE*.out` written before each table,
   `POSTTABLE*.out`, `check16.out`, `logs\`).
4. The final text: `..\final529r17_20260926\crime_width_probe.r17.py` -- repair 16's probe with the ruling's text
   edits; `mk_r17.py.txt` beside it applies them and REFUSES unless the code is unchanged (the AST without the module
   docstring and with the three edited row notes blanked is identical to repair 16's).  Its diff against repair 16 is
   what `mk_r17.py.txt` writes; `DIFF_vs_table16_base.txt` and `probe_base_r17.raw` are ONE base leg of the final bytes
   on table 16's own base binary, diffed against table 16's base log.  One edit goes beyond the ruling: the contract's
   "ENTRIES 13/17" and "13/17 CHANNEL" became "13 and 17", because `tools/pipeline/check_score_claims.py` reads an N/M
   pair in a probe docstring as a score claim against the gate pin (226) and would fail the commit.

The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  The device is
`src/devices/dev_sgi_ip32.c` (`DEVICE_ACCESS(crime)`); the probe's module docstring is its CONTRACT, and the REPAIR 16
block in it is what the ruling rewrote.  Check each "measured" claim in that block against the named artifact.

FIRST LINE: `VERDICT: <CONFIRM | CONFIRM WITH CHANGES | DO NOT CONFIRM>`.  Then: (1) whether the chain should close
here -- if not, the specific change to the device that the contract, as worded, says is detected, yet a named
measurement shows every row passing; (2) which of the ruling's grades (X1-X9) you would overturn, and why; (3) every
sentence in r17's contract block, its added disclosure bullet, and its three rewritten comments or row notes that is
false, with the file evidence; (4) anything the ruling calls DERIVED that a saved measurement contradicts.  Say what is a
reading and what is a measurement.
