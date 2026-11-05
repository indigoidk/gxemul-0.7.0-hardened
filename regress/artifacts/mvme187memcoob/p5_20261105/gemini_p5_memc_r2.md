# Gemini 4 Argon -- job `p5_memc_r2`, banked 2026-11-05 10:47Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p5_memc_r2/gemini_web.out (mtime 2026-11-05 04:35:56 local, 2016 bytes)
* sender verdict line: GWEBP5MEMCR: 4 ATTACKS 1 BROKEN 3 HOLDS 0 UNSETTLED DRAFTABLE:NO

---

VERDICT LINE FIRST.
REPAIR

1. THE FLOOR QUESTION:
Under the project's DEPENDS-ON bound, a null-repair variant must be drawn from the predicates DOMINATING the diff's edited lines. The fix removed an unconditional indexed read and replaced it with field reads inside the `switch (relative_addr)` arms. Inserting entirely new state-changing statements (`if (G) T op V;`) at positions not touched by the fix, gated on predicates (like the latches M and D) that the fix's own path does not read or test, falls OUTSIDE the DEPENDS-ON bound. The 517 survivor groups are combinations of these inserted statements and gates. They are not floor cells owed rows in-round; they are clause-(e) coverage debt because they cross-multiply predicates and states beyond what the fix's data flow jointly reaches.

2. NB4:
`&=` under `!controller` for `chiprev` and `memconf` really is NOCHANGE. As noted in the packet, `memconf` is fixed to 3, and `chiprev` is 1. The controller-0 first memconf stores in the probe are 0x07, 0xff, and 0xffffffff. Applying `&= 0x07`, `&= 0xff`, or `&= 0xffffffff` to 1 or 3 results in 1 or 3. No state is changed at all, which is why PRETABLE_5 correctly classes it as NOCHANGE.

3. THE DIFF:
Each new row's logic matches its claims. R16 correctly triggers the memconf write 0x7 on controller 0 and the default write to 0x1c on controller 1. R17 correctly triggers the default read from 0xf3. However, there is a false sentence in the records: the notes for `rd 0x7c`, `R3 7c r4`, and R8 say "+0x7c (first byte past the struct)". Line 85 confirms that +0x7c is past `memcreg`, but it is still *inside* `struct mvme187_data` (it hits the latches). The memory "outside the allocation" is beyond the struct's end, not at +0x7c. 

4. VERDICT:
REPAIR. (Fix the "past the struct" wording in the notes to "past the register image" or "past memcreg", and record the survivors as clause-(e) debt rather than floor breaches).

P-GWEBP5MEMCR-8e5f
GWEBP5MEMCR: 4 ATTACKS 1 BROKEN 3 HOLDS 0 UNSETTLED DRAFTABLE:NO