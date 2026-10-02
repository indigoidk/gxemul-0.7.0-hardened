GROK SEAT -- #529 (crimewidthkill) final text and records: an ADVERSARIAL READING beside the Fable seat's final ruling

Open your answer with the token `GROK_529_FINAL_ALIVE_0930`.  Then, FIRST LINE: `VERDICT: <n> of the packet's
dispositions are wrong -- <one clause>`.

You are the grok seat of this project's review panel (a hardened fork of the GXemul machine emulator; ordinary
bounds-and-correctness engineering).  The Fable seat is ruling on the same packet in parallel and does not see your
answer; GPT-6 Astra confirms afterwards.  Your job is to be the seat that finds what the packet's author got wrong.

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\final529r18_20260926\fable_final_packet.md`
and answer its items A0 and A-G exactly as they are put (its own instructions on reading committed files with
`git -C ... show HEAD:<path>` apply to you too; HEAD is db8b1a33; never read C:\DocumentNoSnc\CC\GXEMUL\src\, a
pristine 2021 upstream copy).  Item C is a grading question under this project's detector rules and you may answer
it from the packet's own statement of them.  Item E asks which carrier text to adopt; answer it.

Be hardest on: (1) the six corrected docstring sentences of r18/r19 -- read each against `src/devices/dev_sgi_ip32.c`
at HEAD and the probe, and say TRUE or FALSE per sentence with the line; (2) the ACCEPTS-46 block's claim that every
bucket member is named and the counts add up (31 + 4 + 1 + 10 = 46) -- count them yourself in
`final529r18_20260926/accepts_block.txt`; (3) the records drafts inlined in `final529r18_20260926/records_drafts.md`
-- any sentence still false of the code or the artifacts (two audits have already corrected nineteen; find the
twentieth); (4) the base-leg description in item F against `probe_base_r18.raw` and `DIFF_vs_table16_base.txt`.

Write nothing anywhere; return your answer as text.  End with a DENOMINATOR line: what you read, what you did not.
