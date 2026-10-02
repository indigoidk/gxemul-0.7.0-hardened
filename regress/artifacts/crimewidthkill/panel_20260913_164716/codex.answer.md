GAP: in `dev_sgi_ip32.c`, replace `#define CRIME_W_LEN (1 << 0)` with `#define CRIME_W_LEN (1 << (relative_addr == CRIME_INTMASK))`.

`CRIME_CLOSE2_20260913`

1. **The label-keyed latch class remains open.** That one-expression edit gives INTMASK its own latch bit. The only session refusing INTMASK performs four refusals exclusively at INTMASK, so `imask once` still counts one. Every other session uses the other bit. I traced all 32 generated sessions: the mutant’s announcement positions match the baseline throughout. Substituting `CRIME_INTSTAT` produces the same escape. This is one named-label axis, outside the disclosed joint-predicate debt. CONTRACT 4’s “class closed on its single axes” is therefore false. Add a refusal at another label to each [interrupt session](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py:453), retaining the expected count of one.

2. **The new DOG answer row misses a nonzero halfword answer.** Immediately before the decline arm’s [goto](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c:319), insert:

   ```c
   if (relative_addr == CRIME_DOG) odata = 0x100;
   ```

   `dog v0` cannot detect this: its only refused DOG read is `lb`, which receives the zero low byte. There is no refused halfword read at that label; refused writes ignore `odata`. A halfword read would return `0x100`, violating the named-label answer contract. This edit adds no width predicate and does not concern an unnamed offset. Add a seeded `lh` at DOG and assert zero. The missing cell is visible in the [new DOG session](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py:622).

3. **The rearm repair does not cover every existing accepted path.** Insert `d->warned = 0;` inside the existing [DOG_ENABLE branch](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c:361), immediately after its `idata` mask. All generated accepted CONTROL writes carry only `0`, `1`, or `0x800`; none enters that branch. The refused writes carrying DOG_ENABLE skip the switch. Consequently `rearm once` cannot change. This is an insertion into an existing branch, without an invented joint predicate. CONTRACT 8’s “closed over every place an accepted access can go” overstates the repair. Add refusal → accepted CONTROL write `0x0200` → refusal, expecting one announcement.

There are also documentation errors:

- CONTRACT 6 credits `devsig hi` with pinning acceptance at the near high half, although refusal also returns its expected zero. DISCLOSED correctly credits `rev pc ctl`; make CONTRACT consistent.
- DISCLOSED’s accept-offset exception list omits the newly covered near end.
- The TIME assumption should explicitly permit the initial tick it has just acknowledged, then exclude subsequent ticks through the sampling read.

**Verification limits:** I independently checked the source hash, identical shipped/frozen executable ASTs, all 57 completion sentinels, and agreement between raw logs and recorded predictions. Those checks support the recorded measurements. Each new edit above is independently predicted to retain **111/111, CONTROL=OK**; these are static predictions, not new emulator measurements. The missing measurement is a separate detector run for each edit, followed by its proposed discriminator. Compilation and emulator execution were not performed in this read-only workspace.

NO-GO
