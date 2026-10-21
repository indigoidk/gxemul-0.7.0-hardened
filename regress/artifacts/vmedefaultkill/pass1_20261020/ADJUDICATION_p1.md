# vmedefaultkill -- PASS 1 ADJUDICATION (main loop, 2026-10-20 ~19:5x)

Evidence basis: **4 of 4 roster seats answered** (owner roster 2026-10-20: GLM 5.3, grok-4.7 xhigh, GPT-6 Astra ultra,
Fable via the Agent tool -- Fable answered, no wall) **plus Argon (Gemini web) as a second packet-fed lens**.  Opus, agy,
kimi, deepseek, minimax: DELIBERATELY NOT FIRED (owner roster).  All five: PROCEED WITH CHANGES.

| seat | file | verdict |
|---|---|---|
| GPT-6 Astra (ultra) | codex_vmep1.txt (14,964 b) | PROCEED WITH CHANGES |
| grok-4.7 xhigh | grok_p1.txt (14,647 b) | PROCEED WITH CHANGES |
| GLM 5.3 (packet-fed) | glm_p1.txt (11,895 b) | PROCEED WITH CHANGES |
| Fable 5.1 (Agent) | fable5_p1.md (the agent's final report) | PROCEED WITH CHANGES |
| Argon (Gemini web, packet-fed) | _scratchpad/gweb/jobs_20261020_argonpack19/vmep1/gemini_web.out | PROCEED WITH CHANGES |

The HEAD re-witness (sub-agent, 2026-10-20): `../../witness_20261020/SUMMARY.md` -- 7 of 7 sites rc 1 on 5dbc000e;
free-running MASTERCTL read dies with NO `[ vme:` text; the free-running T1CMP control hits its breakpoint.

## Premises (Q1) -- all four held where arithmetic; two QUALIFIED

* Census 10 / 26 / 988 -- re-derived independently by Astra, Grok, Fable (from the header), GLM and Argon (from the packet).
* `d->reg[w] == 0` for every population-2 word for the device's life -- confirmed by all five (writers: indices 20, 21,
  24, 34 only; an 8-byte store writes one element; DM_DEFAULT has no host fast path).
* `return 0` -> data-access exception for a GUEST load/store: TRUE, qualified (Astra, GLM, Grok, Fable): NO_EXCEPTIONS
  callers (the debugger's dump/put, memory.c helpers, the disassembler) never reach the handler at all -- silent success
  with the #95 zero fill, identical today; an INSTRUCTION fetch gets INSTRUCTION_ACCESS (vector 2) and then
  `to_be_translated(): read failed` -> `goto bad` -> the emulation halts (pre-existing for every faulting fetch); a second
  fault in one session with PSR.SFRZ set becomes ERROR (PC 0x50).  -> CONTRACT text, no row (debugger blind; fetch out of
  scope); and EVERY FAULT ROW GETS ITS OWN SESSION (Grok).
* Producer domain (Astra, Grok, Fable, by reading cpu_m88k_instr_loadstore.c): naturally-aligned only -- 7,680 pairs;
  misaligned half/word/double never reach the device; `ld.d`/`st.d` is ONE len-8 call; nothing crosses the 1 KiB splitter
  or the device end.

## Dispositions

* **D1 -- exact case labels (KEPT).**  Grok, GLM, Argon prefer them (switch style, greppable, a dropped label is a
  FAULT the census sees); Astra: "explicit labels remain reasonable"; **Fable dissents, leaning to a bound test in
  `default:`** (`relative_addr < VME2_MISC + 4 && !(relative_addr & 3)`) because it removes the "append `case 0x94:` to
  the decline list" escape.  Counter-argument recorded: the bound form does not remove the CLASS -- a standalone
  `case 0x94: break;` is the same one-line growth edit in either form -- so it changes which edit looks natural, not
  what a detector can pin.  Interior population-1 growth is DISCLOSED (NOT CLAIMED) in either form; population 1 is
  pinned at its edges and at one interior sample.  Main loop's call, as Fable said it is.
* **D2 -- no `odata = 0` (unanimous).**  A comment beside the arm states the zero-storage invariant.  **And the read
  announce PRINTS the served value** (Fable): `-- served 0x%llx` with `(unsigned long long) odata`, so "served 0" is a
  measurement, as `#501` prints `data[0]`.
* **D3 -- the write announce prints all 64 bits** (Astra, Fable; Grok and GLM accepted a disclosure instead):
  `0x%llx` with `(unsigned long long) idata`; the offset `(unsigned)`.  13 population-2 bases take a reachable `st.d`.
* **D4 -- sub-word starts inside population-2 words FAULT as the interim (unanimous)**, disclosed, `vmewidthlanes`
  widened to name them (78 bytes + 26 aligned halfwords); pinned by TWO rows: `ld.bu` 0x29 and `ld.hu` 0x2a (a halfword
  at 0x29 traps on alignment before the device -- Astra).
* **D5 -- population 1: keep the two `debug()` lines, `exit(1)` -> `return 0` (unanimous).**  No host announce owed
  (Fable: `m88k_exception` already prints an INFO-level line while free-running).  Comment wording: "an offset this model
  does not service: no header-named register, or the interior of one" -- never "no register is defined here" (Astra) nor
  "no register occupies" (Fable: the absent VMEchip2 chapter's TOC names a GCSR map the header does not).
* **D6 -- the sketch's guest comment is CORRECTED** (Argon, Fable): `vme2chip_init()` READS MASTERCTL then writes it
  back (the read takes the latch, so the write announces nothing), writes MASTER3/MASTER4/MASTER4MOD; `vme2abort()` reads
  IRQSTAT, and with 0 served returns "irq not set" BEFORE writing IRQCLR.
* **D7 -- a compile-time capacity check on the latch** (Astra, transferred warrant: `dev_pcc2.c`'s own check on its
  `warned` bits): `typedef char vme_warned_fits[(VME2_MISC >> 2) < 8 * sizeof(((struct vme_data *)0)->warned_unimpl) ? 1 : -1];`
  -- narrowing the field to 32 bits makes `1ULL << 35` (MISC) land outside it; the check makes that a compile error.

## The detector, consolidated (rows the probe MUST carry; names <= 15 chars -- gate 14's `%-16s` column)

Apparatus / controls: `session`, `live`, `unasm` (every placed word), `neg apparatus`, `vbr reset` (0x67000000: the
DEVICE-SIGNATURE row), **`free neg ctl`** (a FREE-RUNNING GCSRCTL read whose `debug()` text must be ABSENT -- proves the
session ran free at verbose 0, so the fatal-vs-debug channel can vary; Fable).

Cased accept side (the de-escalation clause; Argon found the write paths unpinned): `cased census` (10 reads, one
session, sentinel-seeded, PC + liveness after), `t1cmp rt`, `tctl rt`, `vbr rt` (store then load back the stored
word), `t1count inc` (two reads, +100), `cased wr` (a store to each of GCSRCTL/TCR/IRQEN/IRQL3/IRQL4: no fault, PC +
liveness after).

Population 2 (decline): `p2 rd census` (26 `ld`, destinations seeded, PC + liveness after), `p2 wr census` (26 `st`
then 26 `ld`; destinations seeded; PC + liveness checked AFTER THE STORES -- Argon: an unseeded census cannot see writes
that FAULT), `p2 ld widths` (`ld.bu`/`ld.hu` 0x28, `ld.d` 0x08 checking BOTH destination registers), `p2 st widths`
(`st.b`/`st.h` 0x28, `st.d` 0x08: no fault, nothing stored).

Announce (FREE-RUNNING, one session, breakpoint after the last access): `p2 announce` -- each of the 26 registers is
accessed TWICE IN A ROW in opposite directions, 13 read-first and 13 write-first, so exactly 26 lines, 13 of each form,
each matched on its FULL tail literal (`-- served 0x0.  (once) ]` / `(len 4): 0xa5a5a5a5 -- declined.  (once) ]`) and
naming its offset; then `p2 once` -- a second pass over all 26 in the same session adds ZERO lines, with PC at the
breakpoint and a liveness register proving the pass ran.  Kills: write- or read-branch `fatal`->`debug`, a shared latch
(1 line), a never-set latch (52), a per-direction latch (52), a latch set only at 0x8c or cleared on a write (> 26),
a dropped `(once)` (tail mismatch).

Population 1 (FAULT, ONE SESSION EACH -- SFRZ): `p1 fault lo` (`ld` 0x90), `p1 fault hi` (`ld` 0xffc), `p1 fault wr`
(`st` 0x90), `p1 fault mid` (`ld` 0x94, the interior sample), each: PC 0x18, DMA0 the word address, DMT0
`0x4000|(dreg<<7)|0x3d` (read) / 0x403f-form (write), host alive.  `p1 p2 edge` (`ld` 0x8c declines, then `ld` 0x90
faults, one session: the first and only fault).

Interims (named `vmewidthlanes` channels): `p3 interim` (`ld.bu` 0x51 -> fault, DMA0 0xfff40050; its mutant is
`if (len != 4) break;` in `default:` -- Fable), `p2 int byte` (`ld.bu` 0x29 -> fault, DMA0 0xfff40028), `p2 int half`
(`ld.hu` 0x2a -> fault).

Floor plan: (a) HEAD red; (b) `exit(1)` reinstated at `default:`; (c) a device-less build (MEASURED: the record names
which rows it reds -- the decline rows cannot tell "declined" from "nothing there", `vbr reset` is their discriminator);
(d) one label dropped, write/read announce demoted, latch shared / never set / per-direction, decline conditioned on
`writeflag` or `len`, `return 0` -> `break`, FAULT conditioned on `len`; (e) CONTRACT with NOT CLAIMED: interior
population-1 labels (pinned at the edges and one sample), population 3/4 and population-2 sub-words (interim pins),
`ld.d`/`st.d` at cased bases 0x00/0x60/0x88 spanning a population-2 word (Grok), cased-word `ld.d`/`st.d` lane
placement (Fable; population 4), the guest's abort-handler consequence, NO_EXCEPTIONS callers, instruction fetch,
`xmem` (declines twice / load faults), per-instance latch isolation (one instance per process).

Gate: 14 (`regress/gate_arm.sh`, beside `pcc2_default_probe.py` and `mk48_nvram_probe.py`); row list + emitted/green/red
pins; `check_probe_wiring.py` MANIFEST; `SCORE_CLAIMS_MANIFEST` 36 -> 37; `PMAX` is `build/gxemul`, so the no-VPATH pmax
tree carries the edit and is rebuilt before any gate run (two-part clearance).

## Filed / recorded, not this round
* `vmewidthlanes` widened (population-2 sub-word starts; cased-word `ld.d`/`st.d` lane placement).
* PSR.MXM (misaligned-access round-down) is unmodelled in the m88k load/store path -- a CPU divergence, unfiled (Fable,
  verified absent from OUTSTANDING_BUGS/CHANGELOG by grep) -> FILE as a LOW row.
* The brief's guest-access list omitted six CASED sites (TCTL vme.c:349/:450, IRQEN :402/:527/:540, IRQL4 :519): the
  record lists them; they make `cased census` a guest-path accept row.
* Brief defect (Astra): section 4c inlined `dev_pcc2.c` from the WORKING TREE, which carries another session's 20-line
  comment; at HEAD the `#501` arm starts at :721.  Executable behaviour identical.
* The 2026-10-09 probe's "Control (b)" printed PASS as a constant (a check that cannot fail) -- recorded with the witness.
