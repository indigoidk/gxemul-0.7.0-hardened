**The Opus seat measured the disclosure's other half** (`pass7_seats_20260904/opus/`, own clone
of build/, frozen part-6b instrument md5 ef3f43b4, predictions written 03:44 before the first
build at 03:49, restore cmp-clean and rebuilt): `&& d->pending_timer2_interrupts == 0` at ALL
TWELVE guards scores **157/159** with exactly the TxICR-only red pair -- eleven more arms
carrying the identical conjunct changed not one row -- and `&& d->pcctwo_reg[PCCTWO_IPL] == 0`
at all twelve scores **155/159**, KILLED by the four pend rows because `reassert_interrupts()`
has raised IPL to the pending level at TxICR.  So the contract now says, per arm: pending and
INT are in closure at TxICR only and closed there; at the other eleven arms they are reached
only through the callee and the same conjunct escapes -- disclosed with its measurement; and
`reg[IPL] == 0` escapes at the IPL guard (one message) and at any arm no row wide-writes with
an interrupt pending, but not at TxICR.  The seat also noted, correctly, that "a declined
write's readback is the preset whatever the value" is an incomplete transfer warrant -- the
value change at GENCTL altered SURVIVAL, not the readback, and the transfer is safe only
because the one mutant where that mattered was re-run in part 6b; and that its own driver's
proof line printed zero for a bracketed pattern (a BRE character class), the same class as the
inert line it had just reported.  Its "another kill table is running in build/" observation
at 04:13 was this round's propagation of the comment fix (sentinel dropped, three trees rebuilt,
two-part clearance recorded), not a table.
