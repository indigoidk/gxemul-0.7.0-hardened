# GXemul est/ — Outstanding bug candidates (not yet fixed)

> ## 2026-07-19 — GXEMUL emulation-fidelity candidates from the cross-arch TRUENESS review (pmax/arc)
> Two gxemul emulation BUGs identified in the emulation-vs-physical trueness campaign, NOT yet fixed and IN the
> pmax/arc mandate (candidates for a future round):
> - **[BUG] arc headless VGA text-console character-drop under load** — `dev_vga` `vga_update_textmode` →
>   `console_putchar` → stdout mirror loses bytes on long/rapid (~70-char) lines (`BOUND`→`BOUN`, mangled hex;
>   surfaced 2026-07-18). Real arc VGA does not drop. DISTINCT device path from the UART serial-drop L12 (fixed
>   as **#251**) — the VGA text mirror, not the DZ/ns16550 TX. Likely the same flush/buffering class as #251;
>   surgical. Workaround: route results through the arc writable raw disk, not the console.
> - **[BUG] unaligned instruction-fetch exception CLASS — gxemul raises TLBL (ExcCode=2) where real R3000/R4000
>   raise AdEL (ExcCode=4)** for a controlled jump to an unaligned/OOB PC (e.g. `0x42424242`; observed firing #20
>   lprm, noted for #267). Fault-signature fidelity, pmax+arc; extends the #210–#233 exception line. Immaterial to
>   security verdicts (captured PC = attacker bytes either way) but a real class delta. Verify the current ifetch
>   path first (#234/#228 are adjacent).
> Already-resolved trueness items (NOT open): **L12** serial-drop → #251; **L5** pty/forkpty hang → #252; **L13**
> UDP-inetd handoff → dispositioned (userspace-NAT topology, reachable via tap **#253**). Inherent GAPs (not
> fixable without a rewrite): **L1** not-cycle-accurate; **L7** FP/uninitialized-memory lowest-confidence (FP
> largely #254/#255; uninit zero-fill #244). **[FAITHFUL]** L2 strict-alignment + LE endianness are correct
> reproductions — do NOT touch. All the trueness doc's #5–#23 security items are [FAITHFUL] gxemul reproductions
> (they *confirm* fidelity), not emulator defects.

> ## 2026-07-18 — Twenty-eighth round (#254, #255): MIPS FPU result-correctness (4-model panel)
> Item #1 of the 8-item TODO-triage batch. Applied **#254** (div/sqrt/compare result bugs in `fpu_op`) + **#255**
> (NaN → legacy-MIPS quiet-NaN canonicalization), 4-model-panel designed+reviewed (Codex xhigh + agy + Fable +
> Ollama), build 0/0 both, pmax 15/15 + arc 13/13 boot, host-side FP-logic microtest 11/11 (rig image lacks an
> in-guest compiler).
> **DEFERRED (own future corrections, documented):**
> - **FCSR V/Z/O/U/I cause/flag maintenance + enabled-exception trapping** — needs qNaN/sNaN discrimination (`struct
>   ieee_float_value` keeps only one `nan` flag), target-format rounding for O/U/I, R4000-gating (R3000 FCSR must
>   stay bit-identical per #246), and the CTC1-writes-enabled-cause TODO (`cpu_mips_coproc.c` ~2216). ~0 benefit for
>   OpenBSD 2.2 (no FP traps enabled); medium-high risk. Panel unanimous DEFER.
> - **S-format round-to-nearest** in `ieee_store_float_value` (`float_emul.c` ~277 truncates to 23 fraction bits →
>   single-precision inexact results 1 ulp low). Pre-existing, all ops; own correction.
> - **In-guest FP microtest blocked** — the OpenBSD 2.2 rig image has no comp set / working `cc`; a future round
>   could install a toolchain or inject a static MIPS test binary to exercise c.olt/c.ole live (gcc never emits them,
>   so only hand-asm reaches those paths).

> ## 2026-07-18 — Twenty-seventh round (#253): Linux tun/tap enablement — L13 inbound now DELIVERABLE (Codex + Fable)
> Round 26 dispositioned L13 (inetd UDP `dgram/wait`) as "not an emulator bug — the userspace NAT has no
> unsolicited-inbound path; resolve via tap or an outbound hole-punch." A Codex `gpt-5.6-sol` + Fable panel enabled
> the tap path on Linux. **Applied + verified live:** **#253** `net/net_tap.c` `net_tap_init()` gains a
> `#if defined(__linux__)` branch opening `/dev/net/tun` + `ioctl(TUNSETIFF, IFF_TAP|IFF_NO_PI, ifr_name=tapdev)`
> (Linux tapdev = tap interface **name**; BSD `open(tapdev)` device-path unchanged in `#else`; shared FIONBIO/tail →
> non-Linux compiles byte-identical). Build 0/0 both trees; both NAT boot regressions still pass (pmax 15/15 + arc
> 13/13 → `uid=0(root)`, zero NAT-path impact since `net_tap_init` is only reached when `tapdev != NULL`). **Live
> proof (pmax rig):** `gxemul -e 3max -L tap0 -d 1:disk bsd.pmax` attaches (host `tap0` → `UP,LOWER_UP`); guest
> `ifconfig le0 10.0.0.10`; then host→guest **unsolicited** `ping` = 4/4 replies and a UDP datagram reached the guest
> kernel (ICMP port-unreachable) — the delivery the NAT structurally can't do.
> **=> The L13 class (unsolicited-inbound UDP services: inetd dgram/wait, portmap, photurisd) is now reachable via
> `-L tap0`.** Host setup: `ip tuntap add dev tap0 mode tap user $USER; ip addr add 10.0.0.1/8 dev tap0; ip link set
> tap0 up`. **Use the pmax rig** (arc/pica SONIC `dev_sn.c` is an RX/TX-less register stub; 3max LANCE `dev_le.c` is
> complete). Under WSL2 the tap is host↔guest only (VM net not bridged to the LAN) — sufficient for the proof. Header
> choice (`<net/if.h>`+`<linux/if_tun.h>`, not `<linux/if.h>`) resolved by test-compiling all three variants.

> ## 2026-07-18 — Twenty-sixth round (#251, #252): console host-glue fidelity (3-view panel)
> An OpenBSD 2.2 pmax/arc audit reported three "emulation-layer" bugs. A source-verified panel (Codex `gpt-5.6-sol`
> high + Fable + reviewer holistic pass, each `diff`-checked vs pristine `src/`) **converged** that the audit
> mis-attributed the subsystem in all three; the two real defects are in the shared host-console glue
> (`console/console.c`, byte-identical to stock 0.7.0). **Applied (both trees, build 0/0, pmax 15/15 + arc 13/13
> boot PASS, reproduced+fixed on the pmax rig):**
> - **#251** `console_putchar` cleared the stdout flush-pending flag on `'\n'` assuming libc line-flush — false
>   when stdout is a pipe/file (fully buffered), so newline-terminated bursts sit unflushed and are lost on
>   kill/wedge (the audit's "L12 serial drops output"). Always mark pending → `console_flush()` drains it. Not the
>   UART (DZ/ns16550 TX is lossless).
> - **#252** `console_charavail` drain loop spins forever on stdin EOF (`select`→readable, `read`→0), *inside a
>   device tick*, wedging the whole emulator (the audit's "L5 pty/forkpty hang"). `if (len < 1) break;`. Repro:
>   `gxemul -e 3max -d 1:disk bsd.pmax < /dev/null` froze at 0 bytes; post-fix boots to `root device?` like an
>   open-stdin control.
>
> **Triaged / DEFERRED / DO-NOT (documented — not applied):**
> - **L13 inetd UDP `dgram/wait` — NOT an emulator/device bug.** The userspace NAT (`net/net_ip.c` `net_ip_udp` /
>   `net_udp_rx_avail`) creates mappings only from guest-*outbound* traffic and has **no unsolicited-inbound path**;
>   an `inetd dgram wait` service waits on purely unsolicited inbound → never delivered (once `inetd`'s `select()`
>   is readable, the datagram is already in the guest socket buffer — nothing is lost in the fork+exec window). The
>   real axis is *solicited vs unsolicited*, not inetd-vs-standalone. Resolutions: tap networking
>   (`net/net_tap.c`, already implemented) or a one-datagram outbound "hole-punch" in the test — NOT a
>   `dev_le`/`dev_sn`/`net.c` change. True inbound port-forwarding = a new feature with new state/options, out of
>   the minimal-surgical ethos.
> - **L12 UART model — not a bug** (lossless; the ready-always TX status is a fidelity simplification, not a
>   data-loss source).
> - **`dev_jazz.c` R4030 `EXT_IMASK` IP3/4/6 namespace gating** — real interrupt-model issue in the *est/* copy
>   (ANDs CPU-IP funnel enables directly against Jazz device-line bits, arc-only). **SEC's `dev_jazz.c` already
>   carries the corrected split** (the SEC-only jazz boot-enablement layer the arc rig runs), and pmax has no
>   jazzio — so it affects neither rig and is not the L5 hang. Companion **OB-22** (`dev_jazz.c` vector-read
>   blanket deassert) stays deferred (self-healing; would touch the verified arc boot).
> - Minor `console/console.c` residual (not applied, low value): `d_avail()` retries *all* `select()` errors as if
>   `EINTR` (incl. `EBADF`); could tighten to `errno==EINTR` only. #252's `break` already resolves the reachable
>   (EOF) freeze.

> ## 2026-07-17 — Twenty-fifth round (#248, #250): debugger QoL for the audit (4-model panel)
> Scoped the author's `doc/TODO.html` for **debuggability** wins for the OpenBSD 2.2 pmax/arc audit. A **4-model
> panel** (Codex `gpt-5.6-sol` + agy Gemini + Ollama `gpt-oss:120b-cloud` + Kimi `kimi-k2.5`; Fable seat down on
> credits) reviewed the verified-undone candidates. **Applied (both trees, build 0/0, pmax+arc boot + live feature
> verification):** **#248** breakpoint hit-counts + "run N then break" (`breakpoint add addr[, N]`, counts on
> `show`/CTRL-T); **#250** data write-watchpoints (`watchpoint add addr[, len]` → break on guest store, report
> writer pc/value; physical-address match via `host_store` suppression + early `memory_rw` check). Both opt-in and
> guest-invisible (single `n!=0` early-out when unset). See CHANGELOG / REVIEW_FINDINGS "Twenty-fifth round".
> **Already implemented — candidate withdrawn (recon before coding):**
> - **C3 disk fsync-on-write toggle → the shipped `-f` option** (`main.c` `case 'f'`, opts string, `usage()`).
>   Its tentative number **#249 is VOID / unconsumed.**
> - The rest of the panel's "already-done" set: `find`, `put s/z`, `step call`, `verbosity`, subsystem/`debugmsg`
>   breakpoints, prefix-abbrev subcmds, `tlbdump`, CTRL-T-while-single-stepping (all the #120–#128 author-TODO round).
> **Assessed, DEFERRED / DO-NOT (documented — not applied):**
> - **CTRL-T in the main emul (run) loop — DEFER (unanimous):** async stdin polling under `-x` is historically
>   fiddly and risks console regression, for mostly-observational value; subsystem breakpoints + halt cover the need.
> - **PC / execution statistics (profil-style coverage) — DO-NOT (unanimous):** hot-path per-instruction counters
>   are a fuzzer feature, out of the accuracy-or-debuggability charter and against the minimal-changes ethos.
> - **Watchpoint limitations (documented, by design):** matches on physical addresses (so it needs the typed vaddr
>   to be translatable at add-time — trivial for kseg0/kseg1, needs a mapped TLB entry for kseg2/kuseg); write-only
>   (no read watchpoints); the shared expression parser doesn't accept bare register names (`r29`) — use literals.

> ## 2026-07-17 — Twenty-fourth round (#245–#246): debuggability logging + FPU denormal fidelity (5-model panel)
> A **5-model panel** (Codex `gpt-5.6-sol` + Fable + agy Gemini + Ollama `gpt-oss:120b-cloud` + Kimi `kimi-k2.5`)
> reviewed the round-23 Part-B suggestions. **Applied:** #245 (C5) route the rounds-18–23 guest-reachable
> fault-conversion diagnostics (`dev_asc`/`dec_prom`/`arcbios`, 8 sites) through the verbosity-gated
> `debugmsg`/`ENOUGH_VERBOSITY` channel (`VERBOSITY_DEBUG`) so a guest/fuzzer can't flood the host log; #246 (C3)
> FPU denormals → real Unimplemented-Operation trap (FCSR cause E + `EXCEPTION_FPE`, no result written), **gated to
> EXC4K+ (arc)** — EXC3K/pmax bit-identical. Build 0/0, pmax+arc boot (trap active on arc, no misfire). See
> CHANGELOG "Twenty-fourth round". **Assessed, intentionally left (not bugs to force):**
> - **C1 (R3000 IsC cache) — already correct:** GXemul allocates real per-cache buffers (`cpu_mips.c`
>   `cache[i] = malloc(...)`) + `memory_cache_R3000()` routes isolated data accesses to them. Faithful already.
> - **C2 (R4000 TLB-Shutdown on overlap) — DO-NOT:** no machine-check delivery (`EXCEPTION_MCHECK` never raised, no
>   `STATUS_TS`/DS state); R4000 multiple-match is architecturally undefined (reset-latched wedge, not an
>   exception); MIPS32 ExcCode 24 would be anachronistic + panic-prone on OpenBSD 2.2; upstream's own duplicate
>   detector is `#if 0`'d as unreliable; first-match is a valid concretization of UNDEFINED. **#247 unconsumed.**
> - **C4 (R3000 delayed-IE / IRQ-in-delay-slot) — already correct where it matters:** the delay-slot
>   `Cause.BD`+`EPC=branch` signature is textbook; only the 1–2-instruction IE cycle-timing hazard is unmodeled and
>   nothing depends on it (functional emulator, no cycle timing).
> - Residual (deferred, low value): FCSR *flag* bits still never set; CTC1-written cause bits don't trap
>   (pre-existing TODO); the optional C2 write-time overlap **debug warning** (resurrect the `#if 0` block at
>   `cpu_mips_coproc.c` as a `debugmsg` — tooling, not fidelity) was left unimplemented.

> ## 2026-07-16 — Twenty-third round (#234–#244): guest-reachable host-halt tail → hardware-plausible faults
> A **Fable (source-verified) + agy** panel took the remaining guest-reachable **host-halt** tail of the Codex
> round-19 backlog (~13 candidates). **10 DO-NOW** (all MIPS/pmax/arc audit path) converted to the correct fault
> or graceful return: #234 failed ifetch `goto bad`→`return` (cf. #210); #235 `break 0x30378` reboot sentinel gated
> to the reset stub (phys `0x1fc00000`), else real BP; #236 reserved COP0 fn→RI; #237 COP0 STANDBY/SUSPEND/HIBERNATE
> → R4100 idle / else RI (was HIBERNATE `goto bad`, SUSPEND reboot-at-any-PC); #238 `memory_mips_v2p` supervisor/
> reserved KSU→TLB walk not `exit(1)`; #239 R3000 `tlbw*` under IsC→`return`; #240 `dev_asc` unimplemented cmd→
> deliver the ILL IRQ, no exit; #241 `dec_prom` unsupported services→`V0=-1`+return; #242 `arcbios` non-SGI private
> call / `0x888` / unimplemented vector→`V0=ARCBIOS_EINVAL`+return; #243 `diskimage_scsicmd` `malloc(0)`→`malloc(1)`;
> #244 `memory_rw` zero-fill the read buffer on a failed/`NO_EXCEPTIONS` translation (whole class; DEC-PROM uninit
> buf). Build 0/0, pmax+arc boot. See CHANGELOG "Twenty-third round". **Clears ~10 of the ~15 remaining Codex
> round-19 items; ~5 remain for #245+** (all off the MIPS audit path or verified unreachable there):
> **DEFERRED / NOT reachable on pmax/arc (documented — not bugs to force):**
> - **#10 PPC/ARM slow-path ifetch `exit`** (`cpu_ppc_instr.c` ifetch fail; `cpu_arm.c` `running=0`) — direct analog
>   of #234 but off the MIPS audit path; the PPC data side is already fixed (#216). Fix = `return`/RI when promoted.
> - **#11 PPC `MSR.IP` reboot hack** (`cpu_ppc.c`) and **#12 m88k CMMU / `dev_mb89352`** fatal errors — off-path.
> - **SPECIAL3 `RDHWR` selector halt + `HWREna` gate** (`cpu_mips_instr.c`): Fable verified SPECIAL3 is ISA-gated to
>   RI on R3000/R4000, so the halt is **unreachable** on pmax/arc (MIPS32r2-only). Cheap hardening for a future
>   round; no audit-path exposure.

> ## 2026-07-16 — Twenty-second round (#230–#233): MIPS fault-signature fidelity (FULL 4-model panel)
> A **full 4-model panel** — Codex `gpt-5.6-sol` + agy `Gemini` + Ollama (`gpt-oss:20b`; the `480b-cloud` model
> returned HTTP 410) + Fable — fixed 4 fidelity items and DEFERRED 2. **FIXED:** #230 R3000 RFE KUo/IEo preserve
> (`~0x0f`); #231 ERET-on-R3000 → RI (decode-gate); #232 J/JAL region from the delay-slot PC `(branch+4)[31:28]`;
> #233 `mtc0`/`dmtc0` `cop0_availability_check` (writes only). Build 0/0, pmax+arc boot. See CHANGELOG
> "Twenty-second round". Clears 4 of the ~19 remaining Codex round-19 items; ~15 remain for #234+.
> **DEFERRED by the panel (documented — NOT bugs to force):**
> - **Privilege-transition fast-map bleed (Codex #17):** the dyntrans fast host-page map is not privilege-tagged,
>   so a kseg mapping cached in kernel mode can be hit by a later user access, bypassing AdEL/AdES (the slow
>   `memory_mips_v2p` path raises it correctly). The proposed invalidate-all-on-RFE/Status-write fix is a
>   non-starter — R3000 RFE fires on every syscall/interrupt/TLB-miss return, so a full invalidate there causes
>   continuous re-translation and would **hang the boot**; a Status-write-only hook misses R3000 RFE entirely
>   (RFE rotates Status directly in `X(rfe)`); the only correct+cheap fix is privilege-tagging the fast map = a
>   structural refactor the ethos forbids. agy+Fable ruled DEFER; Codex+Ollama conceded HIGH risk. Documented as
>   a known fast-map-vs-slow-path privilege-boundary fidelity limitation for the audit.
> - **#233 remainder:** the mfc0/dmfc0 READ-side availability check (side-effect-free fast paths), the
>   `rt==$zero`→nop fold, and the EXC3K user-mode-from-PC heuristic (in-code comment: forcing KUc "crashes
>   Linux") — invasive/risky for marginal exploit value; deferred.

> ## 2026-07-16 — Twenty-first round (#227–#229): fault-signature fidelity trio (multi-model panel, unanimous 3-0)
> A **multi-model advisory panel** — Codex `gpt-5.6-sol` + agy `Gemini` + Fable (Ollama not installed on host) —
> unanimously (3-0) FIXED the three fault-signature-fidelity items promoted from the Codex round-19 backlog:
> **#227** `SWL/SWR` store pre-read mislabeled every fault as TLBS → map only load→store codes (TLBL→TLBS,
> AdEL→AdES; DBE/Mod correctly left alone); **#228** misaligned `jr`/`jalr` silently rounded down → raise AdEL
> (BadVAddr=EPC=rs, BD=0) in all 6 register-jump handlers; **#229** `mtc0 $8` `BadVAddr` → read-only. Build 0/0,
> pmax+arc boot. The panel resolved the earlier BadVAddr disagreement (Codex "fix" vs a prior Fable
> "Irix-compat/document-only") **3-0 to fix**, after Codex extracted the OpenBSD 2.2 kernel source and confirmed
> pmax/arc only `mfc0`-read CP0 $8 → no boot regression. See CHANGELOG "Twenty-first round".
> This clears **3 of the ~22 Codex round-19 backlog items**; ~19 remain for #230+ — the rest of the
> fault-signature fidelity set (`J/JAL` region from page-base not PC+4; R3000 `RFE` Status bits; `ERET`-on-R3000
> → RI; CP0 availability check; privilege-transition fast-map bleed) plus the guest-reachable host-halt tail
> (`goto bad`, `malloc(0)`, PPC/Thumb/m88k slow-path, dec_prom/arcbios unsupported-service, DEC-PROM uninit buf).

> ## 2026-07-16 — Twentieth round (#224–#226) + Codex round-19 backlog recorded
> Applied **3 HIGH MIPS-FPU memory-safety fixes** to both trees (build 0/0, pmax boots): #224 `ldc1`/`sdc1`
> `ft=31` → `reg[32]` OOB into `tlbs`; #225 `ldc1` uninitialised-`fpr` leak on a faulting load; #226 coproc
> paired-store `fd+1` sign-extension OOB. See CHANGELOG "Twentieth round".
> **Codex round-19 backlog — 22 items NOT yet applied (future rounds; full text saved in the session scratchpad
> `codex_round19.txt`, 2026-07-16):**
> - **HIGH (done this round):** Codex #23→#225, #24→#224, #25→#226.
> - **Fault-signature fidelity (recommended next — directly affects controlled-PC / BADVADDR trust):** misaligned
>   `JR/JALR` silently rounded down (should raise instruction-fetch AdEL with BadVAddr); `SWL/SWR` pre-read
>   rewrites every fault as TLBS (should preserve AdES/DBE); `mtc0`-writable `BadVAddr` (Codex: fix for
>   fault-signature auditing — Fable-B had called it Irix-compat/document-only, so reconcile); `J/JAL` region from
>   translated page base not `PC+4`; R3000 BEV=1 vector base `0xbfc00200` vs `0xbfc00100`; R3000 `RFE` Status bits;
>   `ERET` accepted on R3000 (should RI); CP0 availability check omitted; privilege-transition fast-map bleed
>   (stale kseg mapping bypasses AdEL/AdES after kernel→user).
> - **More guest-reachable host-halts:** `cpu_mips_instr` `goto bad`/BREAK-reboot-sentinel/RDHWR/SUSPEND;
>   `memory_mips_v2p` KSU=supervisor `exit(1)`; TLBWI/TLBWR under Status.IsC; `dev_asc` unsupported-command exit;
>   `dec_prom`/`arcbios` unsupported-firmware-service halts; `diskimage_scsicmd` `malloc(0)`→NULL→exit; PPC/Thumb
>   slow-path; PPC `MSR.IP` reboot hack; m88k CMMU / `dev_mb89352` protocol errors.
> - **Category 3:** `dec_prom` uninitialised `ch`/`buf` on a failed `NO_EXCEPTIONS` translation (silent
>   nondeterminism / unbounded string scan).

> ## 2026-07-16 — Nineteenth round (#210–#223): MIPS exception fidelity/debuggability + host-halt sweep
> Codex `gpt-5.6-sol`/ultra + a 2-agent Fable panel + per-site verification applied **14 corrections #210–#223**
> to both trees (build **0/0**, all tags matched, **pmax boot regression PASS**) — see CHANGELOG /
> REVIEW_FINDINGS "Nineteenth round". Highlights: #210 wire MIPS exceptions to the trappable `SUBSYS_EXCEPTION`
> breakpoint (catches controlled-PC-into-unmapped that `-p` can't reach); #211 AdEL/AdES no longer clobber
> Context/EntryHi (BadVAddr only, like silicon); #212 unaligned LL/SC → AdEL/AdES; #213/#214 CONFIG/ENTRYLO1;
> #215–#217 Alpha/PPC/SH host-crashes → guest faults; #218–#223 OF + footbridge/mp/kn02ba/8253 guest-reachable
> `exit(1)`s → graceful.
> **New deferred (broad device-exit tail):** the same untagged `fatal("…TODO/unimplemented…"); exit(1)` inside
> many other guest-writable `DEVICE_ACCESS` handlers persists (Fable-A's list: `dev_adb.c`, `dev_clmpcc.c`,
> `dev_igsfb.c`, `dev_lca.c`, `dev_m8820x.c`, the `dev_pcc2.c` remainder, `dev_mb8696x.c`, `dev_mvme187.c`,
> dreamcast gdrom/maple/g2, and `cpu_arm_coproc.c` CP15 writes 165/252/407/518). Each is guest-reachable when its
> machine is selected; extending the #118/#119 warn-once-and-continue pattern would close them — a future round.
> **Document-only (assessed, not bugs):** R3000 BEV=1 bootstrap-vector base (`0xbfc00200` vs `0xbfc00100`; off the
> exploit window — OpenBSD clears BEV early); `mtc0`-writable `BADVADDR` (Irix compat); the SH `sh_exception()`
> default and the dyntrans `bad:` halt (both already emit a trappable SUBSYS message — an intentional
> "unimplemented" signal the maintainers want surfaced).

> ## 2026-07-16 — Eighteenth round (#188–#208): accuracy/debuggability pass (Codex 5.6-Sol-Ultra + Fable panel)
> A fresh full-tree Codex `gpt-5.6-sol`/ultra review (17 findings) + a 4-reviewer Fable panel + per-site
> verification, narrowed to **hardware-accuracy + debuggability + ethos** (not new hardening for its own sake),
> applied **21 corrections #188–#208** to both `est/` and `GXEMUL-SEC/` (build **0/0**, all 21 tags matched) —
> see CHANGELOG / REVIEW_FINDINGS "Eighteenth round". This **clears one deferred item below: the `dev_ram.c`
> MAP_FAILED-vs-NULL #175 straggler → now fixed as #208.** Highlights: R4000 invalid-PageMask host-`exit()`
> (#188 write-canonicalize / #189 translate-refill), `TLBWR` divide-by-zero (#190), DEC/ARC PROM `malloc` DoS
> (#191/#192), ARM/Alpha/m88k page-walk & signed-div host-crashes → guest faults (#193–#195), and Codex HIGH
> guest→host OOBs (#202 SII, #203 MEC, #204 flat-CD, #205 MODE SELECT, #207 PX copyspans).
> **Still deferred (unchanged):** #185 ASC DATA_OUT `exit(1)`; the four PVR render/texture-loop `exit(1)`s
> (868/1084/1245/1419); CUE symlink-follow; cross-memblock invalidation gap (#165); overlay write
> silent-success; Jazz `LB_IE` / dual-pending IRQ; ARC partition signed-`*512`; TCP-debug over-read; NE2000 TX
> log-flood.
> **New "not changed" (documented):** the MIPS `add/addi/sub` Integer-Overflow *trap* (`cpu_mips_instr.c`) —
> defined 2's-complement wrap in practice; a real trap is the hottest instruction path + boot-regression risk,
> so left per OB-24.

> ## 2026-07-10 — Cross-model re-review (Codex 5.6-Sol-Ultra + Fable panel): #182–#187 applied; deferred candidates
> A full-tree adversarial re-review (Codex `gpt-5.6-sol`/ultra, 17 findings, + a 4-reviewer Fable panel, each
> source-verified) fixed a **CRITICAL fb-resize stale-length OOB (#182)**, a HIGH X11 alloc overflow (#183), and the
> clean part of the guest-`exit(1)` cluster (#184 dev_fb, #186 mb89352, #187 eight dev_pvr MMIO sites) — see
> CHANGELOG / REVIEW_FINDINGS "Seventeenth round". Build 0/0 (gcc 15.2.1); applied to both `est/` and `GXEMUL-SEC/`.
> **Deferred candidates (recorded for a follow-up fix pass; not yet applied):**
> - **#185 `devices/dev_asc.c` DATA_OUT `data_out_len==0` `exit(1)` (med DoS):** reachable via `NCRCMD_TRPAD|DMA`
>   before a SELECT (TRPAD allocates `xferp`, so the #167 null-guard passes, then the DATA_OUT phase has len 0).
>   The fix needs a structural transfer-skip (wrap the ~40-line copy in `if (len != 0)`), so it is held for its own pass.
> - **`devices/dev_pvr.c` render/texture-loop `exit(1)`s (med DoS): lines 868 (texture pixelformat), 1084 (non-RGB565
>   render cfg), 1245, 1419 (unimplemented TA list-cmd).** Reachable via STARTRENDER; converting these safely needs
>   flood-free per-iteration recovery, unlike the simple MMIO-write fall-through used for #187.
> - **CUE symlink/junction bypass of #158 (`disk/diskimage.c`, med, host-side threat):** the #158 guard rejects only
>   *lexical* `..`/absolute paths; `fopen()` still follows a symlink/junction inside an attacker-supplied CUE bundle.
>   Needs an attacker-supplied disk image (host-side), not a malicious guest — lower priority under the guest→host charter.
> - **Cross-memblock dyntrans invalidation gap in #165 (`cpus/memory_rw.c`, med):** a bulk RAM write spanning a
>   memblock boundary invalidates only the endpoint pages, so translated code in interior pages can go stale.
> - **Lower-severity Codex findings:** overlay write rejected-but-reported-GOOD (`diskimage.c`, silent data loss);
>   Jazz `LB_IE` not implemented + dual-pending-IRQ loss (`dev_jazz.c`); ARC partition LBA signed-`int *512` overflow
>   (`arcbios.c`, defeats the #168 bound); TCP-debug options over-read (`net_ip.c`, debug-verbosity only); NE2000
>   invalid-TX log-flood (`dev_ne2000.c`, SEC-only); one `dev_ram.c` `MAP_FAILED`-vs-NULL check (#175 straggler).

> ## ✅ 2026-06-28 — OB-35 RESOLVED (correction #117; build 0/0, Codex+agy APPROVE FOR COMMIT, regression-clean)
> Added a **7445/7455 CPU model** as a NEW, purely-additive macppc subtype **`-e g4plus`** (→ MPC7455, PVR
> 0x80010000) so the existing `-e g4` (MPC7400) and g3/g5 are unchanged and OpenBSD 3.4/macppc stays
> regression-safe. **Verified:** on `-e g4plus`, NetBSD 8.2/macppc sets HID0[HIGH_BAT_EN] → #116's extended
> BATs **engage** (gate-opened=1, confirmed via a temporary ppc_bat debug) → it advances past the BAT/MMU
> layer; on `-e g4` the gate stays closed. Files: `cpu_ppc.h` (cpu_type row), `machine.h`
> (MACHINE_MACPPC_G4PLUS=4), `machine_macppc.c` (CPU map + subtype). See CHANGELOG/REVIEW_FINDINGS
> "Eleventh round".
> - **Known residual (NOT a safety bug, pre-existing): macppc OpenFirmware is skeletal.** Past the MMU,
>   NetBSD 8.2/macppc stalls in GXemul's incomplete OpenFirmware (`machine_macppc.c` skeletal model + `of.c`
>   device-tree `getprop` gaps). Reaching a full NetBSD-8.2/macppc multiuser boot is open-ended OF/device
>   work beyond OB-35's CPU-model scope — left as a future enhancement, not tracked as an OOB/safety OB.


> ## ✅ 2026-06-28 — OB-27..34 RESOLVED (corrections #106–#113; build 0/0, pmax+arc regression-clean)
> All 8 deferred Phase-B/C candidates were Claude-verified (**all confirmed real**) and fixed — see
> CHANGELOG / REVIEW_FINDINGS "Eighth round". Map: OB-27→#106 (dev_fb from_x), OB-28→#108 (ps2_gif),
> OB-29→#107 (pvr span), OB-30→#109 + OB-31→#110 (iso9660), OB-32→#111 (bootblock n_blocks), OB-33→#112
> (diskimage %s), OB-34→#113 (SCSI CDB-length).
> ~~Still open: OB-25 / OB-26~~ → **now also RESOLVED: OB-25→#115 (mymkstemp unpredictable overlay temp
> names), OB-26→#114 (osiop skip data phase instead of exit(1)) — see "Ninth round". ALL OB-1..34 are now
> resolved.**

> ## 2026-06-28 — Phase-C deeper audit (3-agent fan-out): #101–#105 applied; 1 new candidate
> Agents swept network/NAT, SCSI/ATA storage, and the remaining devices + dyntrans. Claude verified +
> fixed 5 bugs (#101–#105, incl. 2 CRITICAL: dev_scc OOB heap write + net_arp heap overflow — see
> CHANGELOG / REVIEW_FINDINGS "Seventh round"). One candidate deferred:
> - **OB-34 `disk/diskimage_scsicmd.c` short-CDB over-read (med):** `diskimage_scsicommand()` only checks
>   `cmd_len >= 1`, then every opcode reads fixed CDB offsets (up to `cmd[8]`) — so a guest that submits a
>   short CDB (the SCSI/ATA controllers allocate `cmd[]` to the guest's byte count) causes an OOB read of
>   the host `cmd` buffer, influencing the computed LBA/transfer length. Fix with a per-opcode CDB-length
>   table (6/10/12/16) validated before the reads, under its own regression (touches every controller).

> ## 2026-06-28 — Phase-B new-surface audit (3-agent fan-out): #96–#100 applied; 7 new candidates
> Agents swept the PROMs (all CLEAN), the framebuffer renderers, and the disk parsers; Claude verified +
> fixed 5 bugs (#96–#100, incl. a CRITICAL ps2_gs OOB heap write and a HIGH Apple-partition stack
> over-read — see CHANGELOG / REVIEW_FINDINGS "Sixth round"). These further agent-found candidates are
> **not yet exact-fix-verified by Claude** (record for a follow-up fix pass):
> - **OB-27 `devices/dev_fb.c` `framebuffer_blockcopyfill` (high):** in copy mode the source column
>   `from_x` is not clipped (dst `x1/x2` and `from_y` are), so the `memmove` source over-reads the host
>   framebuffer; reachable from dev_ps2_gif blockcopy and dev_igsfb scroll → host-heap info leak.
> - **OB-28 `devices/dev_ps2_gif.c` TA-putchar (high):** pixel source offset `(24 + y*xsize)*4` uses
>   guest `xsize`/`ysize` (≤65535) with no check against the input `len` → large OOB read of the host DMA
>   buffer (also an `int addr` overflow).
> - **OB-29 `devices/dev_pvr.c:2438` (med):** the 24-bit `pvr_fb_tick` copy wraps only the start
>   `vram_ofs % VRAM_SIZE`, not the span → reads past the 8 MB VRAM; also signed `vram_ofs` can go
>   negative. Other pixelmodes wrap each access.
> - **OB-30 `disk/bootblock_iso9660.c:188` (med):** the root-directory walk reads the 8-byte record
>   header + up to 64 name bytes past `dirbuf` (guard only checks `dp < dirbuf+dirlen` at the top).
> - **OB-31 `disk/bootblock_iso9660.c:308` (med):** `if (i < len - strlen(filename))` underflows
>   `size_t` when `strlen(filename) > len`, defeating the bound → over-read.
> - **OB-32 `disk/bootblock.c` (low):** the bootblock/OSLoader size "WARNING" checks call `fatal()`,
>   which does NOT exit (debugmsg.c:334), so a disk-controlled `n_blocks*512` proceeds with int-overflow
>   UB → `malloc` abort (DoS). Make the checks `return`; use size_t math + an upper bound.
> - **OB-33 `disk/diskimage.c:321` (low):** `fatal("… type %i …", id, diskimage_types[type])` passes a
>   `char *` to `%i` (UB on the not-found path); use `%s`.

> ## 2026-06-28 — multi-model review (Codex + agy + Claude): #89–#94 applied; 2 new candidates
> A three-engine review (Codex `gpt-5.5`/xhigh, agy `Gemini 3.1 Pro`/High, Claude verification + a
> consensus rebuttal loop) of the full hardening diff fixed **6 confirmed bugs (#89–#94** — see
> `CHANGELOG.md` / `REVIEW_FINDINGS.md` "Fifth round") and **rejected 3 false positives** (both models
> conceded). **2 lower-severity items remain open:**
> - **OB-25 `disk/diskimage.c` temp-file TOCTOU (low, local-only).** #7/#20 create the overlay temp
>   files with `fopen "wx"` but then close and **reopen them by name** in `diskimage_add_overlay()`,
>   leaving a swap/symlink race window. Fix: `mkstemp()` + pass the fd; never reopen by name.
> - **OB-26 `devices/dev_osiop.c` guest-reachable `exit(1)` (low DoS).** The #10 NULL-`xferp` guard
>   calls `exit(1)` on a state a guest can drive (SCSI data phase, no active transfer) → a guest can
>   halt the emulator. Prefer aborting the phase (`break`) over killing the process. (Replaced a worse
>   null-deref, so not a regression — a hardening-quality improvement.)

> ## ✅ RESOLVED 2026-06-27 — see CHANGELOG.md "#70–#88"
> All 24 candidates below were triaged (Codex `gpt-5.5` *xhigh* proposals + independent source audit):
> - **19 fixed → corrections #70–#88** (builds 0/0; pmax + arc rigs re-verified):
>   OB-1 #70 · OB-2 #71 · OB-3 #72 · OB-6 #73 · OB-7 #74 · OB-8 #75 · OB-9 #76 · OB-11 #77 ·
>   OB-12 #78 · OB-13 #79 · OB-14 #80 · OB-15 #81 · OB-16 #82 · OB-17 #83 · OB-18 #84 · OB-19 #85 ·
>   OB-20 #86 · OB-21 #87 · OB-23 #88.
> - **3 false positives (not real)** — OB-4, OB-5, OB-10: `cpus/memory_rw.c:288` clamps `len` to the
>   device length before the handler runs, and these three are registered with length == backing size
>   and have no direct callers, so the "end-span" is unreachable.
> - **1 deferred** — OB-22 (jazz jazzio vector-ack): emulation correctness, not host-OOB;
>   medium-confidence; in the #69 arc interrupt path — deferred to avoid regressing the verified arc boot.
> - **1 skipped** — OB-24 (signed `byte<<24` in CPU instruction cores): UBSan-only, hottest path, no
>   exploit path; consistent with the pre-existing "intentionally left" decision (shared decoder fixed in #27).
>
> The per-finding analysis below is retained as the audit record.

---

Consolidated from two **read-only** Codex reviews (model `gpt-5.5`, effort `high` + `xhigh`)
on 2026-06-27, plus the manual audit. These are **static-analysis findings** — bounds/overflow
reasoning from reading the source; most are **not yet runtime-confirmed** (several need a specific
guest/board, e.g. Dreamcast, SGI, TURBOchannel framebuffers). They are candidates for the next
correction set (#70+). The 69 already-applied corrections are in `REVIEW_FINDINGS.md` / `CHANGELOG.md`
and are **not** repeated here. `src/` (pristine baseline) is untouched.

**Threat model:** the emulator runs untrusted guest OS images (device MMIO/DMA) and loads untrusted
executable files (loaders). HIGH = a malicious guest or input file can cause a guest→**host**
memory-safety violation (OOB read/write of host memory). MED/LOW = host DoS / UB / device-state
corruption without a clear host-OOB path.

**Two dominant root patterns** (almost every HIGH below is one of these):
1. **End-span not checked.** An MMIO handler validates the *start* (`addr < size`) but then
   `memcpy`/indexes `len` bytes, so a 2/4/8-byte access at the last valid offset crosses the host
   buffer. Fix shape: require `addr + len <= size` (or clamp `len`).
2. **MMIO window larger than its backing array.** The registered device length exceeds the
   allocation, so high offsets index past it. Fix shape: bound the offset to the real backing size.

---

## High — guest → host OOB read/write

| ID | Site | Pattern | Trigger / impact |
|----|------|---------|------------------|
| OB-1 | `devices/dev_fb.c:646` (+ callers `dev_dec21030.c:135`, `dev_sgi_mardigras.c:200`) | end-span | `dev_fb_access()` checks `relative_addr >= framebuffer_size` only, then `memcpy(framebuffer+addr,…,len)` — wide access at last pixel → host fb heap OOB R/W |
| OB-2 | `devices/dev_px.c:608` | window>backing | PX SRAM MMIO window is 512 KB (`0x200000..0x27ffff`) but `sram[]` is 128 KB; offsets >`0x21ffff` corrupt host heap — any PX/PXG TURBOchannel guest |
| OB-3 | `devices/dev_px.c:315` (+`:414`,`:531`) | unchecked rows | PX STAMP DMA copyspans/fill/putchar use guest `span_src/span_dst` rows in fb pointer math with only `span_len` capped → fb heap OOB R/W |
| OB-4 | `devices/dev_pvr.c:2551` / `:2567` | end-span | `dev_pvr_vram_access()` copies to/from `vram+relative_addr` without `addr+len <= VRAM_SIZE` (distinct from the fixed #65/#68 render/texture paths) |
| OB-5 | `devices/dev_asc.c:778` / `:794` | end-span | ASC 128 KB DMA window: raw `memcpy(dma+addr,…,len)` with no end check |
| OB-6 | `devices/dev_adb.c:300` / `:305` | unbounded append | `output_buf[MAX_BUF=100]` appended via `output_buf[cur_output_offset++]=c` with no cap; guest toggles ACK in output mode → heap OOB write past `struct adb_data` |
| OB-7 | `devices/dev_igsfb.c:183` | unbounded index | DAC `palette_write_index` unclamped; `rgb_palette[index*3+sub]` past the 256-entry palette (start at 255) |
| OB-8 | `devices/dev_kn01.c:171` | unbounded index | KN01 VDAC overlay palette has 16 entries but `cur_write_addr_overlay` is raw guest data → `rgb_palette_overlay+3*addr` OOB |
| OB-9 | `devices/dev_sgi_mardigras.c:220` / `:224` | end-span | microcode-RAM MMIO validates `< MICROCODE_END` only, copies `len` → OOB past `microcode_ram` |
| OB-10 | `devices/dev_ether.c:82` / `:89` | end-span | test-ethernet `buf` MMIO copies to/from `buf+addr` with no end check |
| OB-11 | `devices/dev_pcc2.c:327` (+`:372`) | end-span | `relative_addr %= PCC2_SIZE` folds the *start* only; wide access near end of the 0x40-byte `pcctwo_reg[]` spans past it |
| OB-12 | `devices/dev_pmagja.c:111` | window>backing | PMAG-JA treats all `>=0x200000` as 8-bit pixels up to `0x3c0000`, but `pixeldata` is only 1280×1024 → OOB (and drives `dev_fb_access` out of range) |
| OB-13 | `devices/dev_sgi_gbe.c:706` | unmasked index | GBE palette store `selected_palette[color_index]` instead of `[color_index & 0xff]`; cmap 1..31 writes far past the 256-entry cache |
| OB-14 | `devices/dev_sgi_gbe.c:274` | stack over-read | tile convert: `fb_buf` sized for 512 px but guest partial-tile fields make `fb_len` up to 992 px → `dev_fb_access` copies past `fb_buf` (stack-byte leak into emulated fb) |
| OB-15 | `devices/dev_vga.c:607` | window>backing | VGA gfx window is fixed `0x18000` but `gfx_mem_size` is realloc'd per mode (e.g. 64,000 for mode 0x13) → access in-window but past `gfx_mem` → heap OOB |
| OB-16 | `devices/dev_vga.c:412` | unchecked index | VGA CRTC guest-programmed `base` (start hi/lo) added to every visible charcell index without `base+end` check → charcell heap OOB read on redraw |

## Medium — host DoS / overflow / device-state corruption

| ID | Site | Issue |
|----|------|-------|
| OB-17 | `devices/dev_dec21143.c:763` | TX descriptor chain: many non-`LS` descriptors → repeated `realloc(cur_tx_buf_len+bufsize)` (unbounded host alloc); `int cur_tx_buf_len` can wrap → alloc/copy size bug |
| OB-18 | `file/file_android.c:103` / `:146` / `:186` | file-controlled `page_size`: `==0` → divide-by-zero; very large → 32-bit page/seek overflow → crash/misload |
| OB-19 | `file/file_elf.c:94` (loop `:450`–`:482`) | PT_LOAD copy cursor `ofs` is `int` vs file-controlled `p_filesz` → signed overflow/UB on huge segments (chunk buffer itself is bounded) |
| OB-20 | `devices/dev_dreamcast_gdrom.c:183` (`:90`) | `READ_SECTORS` with `cnt==0` derives `cnt = 2048*sector_count` from guest bytes, then allocates it → guest-triggered host OOM/hard-exit |
| OB-21 | `devices/dev_dreamcast_g2.c:94` | EXTDMA maps `0x100` but `extdma_reg[]` is 0x80; offsets `0x90..0xbc` index `extdma_reg[>=36]` → C subobject OOB into adjacent `misc_reg` (device-state corruption) |
| OB-22 | `devices/dev_jazz.c:613` (`jazz_jazzio`) | **pre-existing, correctness only** (NOT a #69 regression): after reporting a vector it deasserts `mips_irq_3` without clearing `int_asserted` → possible stuck/missed non-timer JAZZ IRQs until next edge/mask write |

## Low / reviewed

| ID | Site | Note |
|----|------|------|
| OB-23 | `devices/dev_sgi_re.c:1127` | MTE fill subtracts `sizeof(zerobuf)` from `dstlen` while writing only `fill_len` → mis-accounting → guest hang / wrong emulated writes (no host OOB observed) |
| OB-24 | `cpus/*` (e.g. `cpu_arm_instr_loadstore.c:297`; ARM/MIPS/PPC/m88k/PROM) | residual signed `byte<<24` UB; real C UB but does not feed host pointers/sizes/indices — sanitizer/portability cleanup, no exploit path found |

## Confirmed clean
- **#69 (arc Jazz interrupt-enable mask)** — both review passes independently found **no regression**:
  assert/deassert gate on `int_asserted & int_enable_mask`, `EXT_IMASK` recomputes IRQ3/6 on mask
  change, and masked pendings stay in `int_asserted` (delivered when later enabled).

## Suggested remediation order
1. **Window>backing (OB-2, OB-12, OB-15):** straight host-heap corruption from any access in-window;
   bound the offset to the real allocation size. Highest priority.
2. **End-span family (OB-1, OB-4, OB-5, OB-9, OB-10, OB-11):** add `addr+len <= size`; many share the
   `dev_fb_access` helper (fix once in OB-1 covers OB-1's direct callers).
3. **Unbounded index/append (OB-6, OB-7, OB-8, OB-13, OB-14, OB-16, OB-3):** clamp/mask the
   guest-controlled index; size the temp buffer to the max (OB-14).
4. **Loader/alloc (OB-17..OB-21):** reject `page_size==0`, cap aggregate/realloc sizes, widen `int`
   cursors to `off_t`/`size_t`, validate `cnt`.

> Generated read-only; no source was modified. Raw review transcripts:
> session scratchpad `codex_review.txt` (high) and `codex_review_xhigh.txt` (xhigh).
