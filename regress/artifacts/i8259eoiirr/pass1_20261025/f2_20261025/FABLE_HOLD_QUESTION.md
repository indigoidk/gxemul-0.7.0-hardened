# i8259eoiirr (#574) F2 (the adjudication of pass 1) -- the Fable 5.1 seat is HELD (owner hold of 2026-10-21); its question

Fable 5.1 is DELIBERATELY NOT FIRED on this pass.  The question it would be asked, kept so the hold carries it:

The main loop takes design (G) to this pass -- EOI touches ISR only; the guest's ACKNOWLEDGE (the OCW3 poll read, and
the GT64120 IACK read on malta) moves the request to service, clearing the IRR bit and setting the ISR bit; the 8253's
pending event is retired at that acknowledge -- and REJECTS (A) alone because Linux/malta (which selects I8253, requests
IRQ 0 and returns IRQ_HANDLED unconditionally) would never see IRQ 0 fall again.  Is (G) the right member of the option
set, is the GT IACK site inside the round-scope rule or a second round, and is edge-only (ICW1 LTIM ignored, as both
guests program 0x11) acceptable with level mode filed?  Which of the main loop's accepted dispositions F1..F26 is wrong?
