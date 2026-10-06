RULING ASKED OF GROK: does `qhm88kstops` carry the MB89352 stops that queue passage 2616 names, or is a row owed?

FIRST line of your answer: `VERDICT: CONCEDE -- a row is owed` / `VERDICT: CONCEDE IN PART -- <what>` / `VERDICT: HOLD -- the passage is carried`.
SECOND line: the token `GROK_MBSTOPS_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

READ-ONLY.  Write nothing, build nothing, run no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, the
committed revision under discussion is `c29a5fd3` (`#555`).  Your plan mode reads the WORKING tree: `src/devices/dev_mb89352.c`
is clean there (the other session's uncommitted edits are in `dev_lca.c`, `cpu_alpha_palcode.c`, `dev_pcc2.c`,
`dev_sh4.c`, `mvme_pcctworeg.h`), so its line numbers below are good; every fact you need is also inlined.

**The standing arrangement (owner, 2026-10-02):** GPT-6 Astra finds, YOU rule on Astra's findings, Astra confirms.  This
is one Astra finding.  Please do not ratify it because it is Astra's or reject it because it is narrow; rule on what the
passage says and what the rows carry.

**The passage** (`OUTSTANDING_BUGS.md` at `db8b1a33`, line 2616, inside a 2026-07 audit list):
> `> - **#11 PPC MSR.IP reboot hack** (cpu_ppc.c) and **#12 m88k CMMU / dev_mb89352 fatal errors** - off-path.`

**What `#555` did with it** (`regress/artifacts/idless_20261002/IDLESS_TABLE2.tsv` at `c29a5fd3`): it POINTED the
passage at `m88kexit` (the m88k CMMU half) and FILED two rows on line 2616:
* `qhppciphack` HIGH -- "MSR.IP stops the CPU instead of selecting the exception vector base" (the #11 half; the stop
  is `cpu_ppc.c:288-291` at `c29a5fd3`, `if (cpu->cd.ppc.msr & PPC_MSR_IP) { ... cpu->running = 0; }`);
* `qhm88kstops` HIGH -- "An MB89352 data-register read with no transfer object stops the emulated CPU" (provenance:
  `grok_icompound.txt`, a compound disposition; "the table's derivation had dropped this row").

**Astra's finding** (`aconf_agyflags/codex_aconf_agyflags.txt`, verbatim): "`qhppciphack` covers the PPC half, but
`qhm88kstops` covers only **a data-register read with no transfer object** (IDLESS_TABLE2.tsv:119).  The passage names
MB89352 fatal/protocol errors more broadly (db8b1a33:OUTSTANDING_BUGS.md:2616,2671).  Separate unimplemented-phase
read/write stops remain at c29a5fd3:src/devices/dev_mb89352.c:166-170,232-236; that title does not carry them.  Earlier
rulings repeat the narrowing without disposing of this remainder (IDLESS_DISPOSITIONS.md:119,176)."

**The stops in `dev_mb89352.c` at `c29a5fd3`, all TEN `cpu->running = 0` sites** (read by the main loop; the flag at
`:61` is `const bool mb89352_abort_on_unimplemented_stuff = true;`, so the three gated ones are live):

| line | message | guarded by |
|---|---|---|
| :146 | `DREG: no ongoing transfer to read from?` | `d->xferp == NULL` -- **this is `qhm88kstops`** |
| :169 | `DREG: read in unimplemented phase %i` | `default:` of the read-phase switch |
| :176 | `DREG: read longer than buffer?` | `transfer_bufpos >= len` |
| :235 | `DREG: write in unimplemented phase %i` | `default:` of the write-phase switch |
| :242 | `DREG: write longer than buffer?` | `transfer_bufpos >= len` |
| :290 | `DREG write: UNIMPLEMENTED PHASE %i` | `default:` of the end-of-write dispatch |
| :312 | `unimplemented LEN: %i-bit access, address 0x%x` | the flag |
| :533 | `unimplemented SCMD: 0x%x` | the flag |
| :690 | `unimplemented %i-bit READ from address 0x%x` | the flag |

(`:146` and the eight others are each a `debugmsg_cpu(..., VERBOSITY_ERROR, ...)` followed by `cpu->running = 0`.)

**What else in the committed ledger touches them** (grep of every row's title, closure, notes and entries at `c29a5fd3`):
* `b120` (held, "SCSI: an unknown command is reported to the guest as success") -- its text cites `read longer than
  buffer?` as REFUTING the "told success" reading (queue line 11457 at `c29a5fd3`: "transfer position at 0, so the
  `read longer than buffer?` guard sees `0 >= 0`, fires, and sets ..."); it is a row about the unknown-command path,
  with the `:176` stop as one of its four outcomes.
* `mb89352halt` (DROPPED 2026-08-27 "as a duplicate I filed myself: it is b120's mb89352 face") -- "An unimplemented
  SCSI command stops the emulated CPU rather than refusing the command"; it reasons about the `:533` SCMD stop and the
  `PH_STAT` path.
* `mboutcapacity` (open) -- "MB89352: the WRITE path re-sizes data_out_len without reallocating, and DREG writes bound
  ..." -- the write path, not a stop.
* Nothing names `:169`, `:235`, `:290`, `:312` or `:690`.

**The question.**  The passage says "dev_mb89352 fatal errors", plural and generic.  `#555` gave it ONE row, for `:146`.
Rule:
1. **CONCEDE** -- a row is owed for the MB89352 stops no row names.  Then say WHICH sites (all nine? the two
   unimplemented-phase ones Astra named? the three flag-gated ones?), with what title (one sentence a reader can
   test against the source) and severity (`qhm88kstops` is HIGH; this project grades a guest-drivable stop of the
   emulated CPU as a host-stop class -- say whether these are guest-drivable, per site, from the guards above).
2. **CONCEDE IN PART** -- e.g. `:176`/`:242` are b120's, `:533` is the dropped duplicate's and so b120's, and only
   `:169`/`:235`/`:290`/`:312`/`:690` are uncarried.  Say which and why.
3. **HOLD** -- the passage is adequately carried (say by which rows, site by site).

Also: is widening `qhm88kstops`' TITLE to the family the better repair than a second row?  (The project's rule: a row
is one defect with one fix shape; a `default:`-arm stop and a NULL-transfer stop may or may not share a fix.)

End with `DENOMINATOR: <s> of 10 stop sites read in dev_mb89352.c; <r> of 4 rows read in the ledger`.
