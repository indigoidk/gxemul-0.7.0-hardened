You are a reviewer for a multi-model code-review harness around a C hardware emulator project (the GXemul
hardened fork; tree `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`).  Read-only: change no file.

Ledger row `agentrefusal` (HIGH, open; `tools\pipeline\ledger.json` id `agentrefusal`, and `OUTSTANDING_BUGS.md`): when
an Agent-tool reviewer seat (the Fable or Opus model) ends a turn in a REFUSAL, the tool silently re-runs the rest on a
different model and the answer keeps the requested seat's identity line, so a fallback answer can be recorded as the
seat.  Today this is caught by hand with `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\agent_models.py` (read it).

FIRST LINE: `VERDICT: <the mechanical check you recommend, in one phrase>`.  Then: (1) where in the harness a check
could key on the subagent transcripts (read `tools\precommit_check.sh`'s section list and `tools\pipeline\*.py`);
(2) what the check reads, what it compares, and what it reports -- concretely, with the ledger fields it would use; (3)
how it would have caught each fallback already on record (search the ledger for `[NOT A SEAT ANSWER]` and `opus-4-8`);
(4) its negative controls; (5) what it cannot see.  Say what you read and what you inferred.
