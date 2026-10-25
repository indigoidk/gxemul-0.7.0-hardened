# i8259eoiirr (#574) -- the Fable 5.1 seat is HELD (owner hold of 2026-10-21, standing on 2026-10-25); its question

Fable 5.1 is DELIBERATELY NOT FIRED on this pass (the owner's hold stands; the cloud route was classifier-stopped on
2026-10-25 for #573's brief and is not retried).  The question it would be asked, kept so the hold carries it:

Of the five candidate designs in section 3 of packet.md -- (A) EOI clears ISR only; (B) A + the poll read acknowledges
(sets ISR); (C) A + edge emulation for one-way sources; (D) a line-level shadow; (E) device-side re-assert only -- which
should ship for this round, does `i8259isrnever` join it, and what does (A) alone do to a guest whose 8253 is in use
(a source that never deasserts and whose pending count nothing decrements)?  Which of section 2's premises is wrong?
