# T1 (`m88kscaledbyte`) pass-1 brief -- drafter's notes: inconsistencies found, with dispositions

Read at HEAD `cb2eba1e`.  "Astra" = `regress/artifacts/research_20261022/crit_20261022/codex_rescrit.txt`; "Grok" =
`.../grok_crit.txt` (same directory).  Source line numbers are HEAD's (identical at `de8c7547`, where the seats read).
Ranked by what each could change in the round.  Each item: the finding, then **Disposition**.

## 1. The generated table is a tracked file; neither seat, nor the ruling, mentions it (seats vs source)
`src/cpus/tmp_m88k_loadstore.c` is in `git ls-files`, last changed at the import `39748e3c`, byte-identical in
GXEMUL-SEC/est/build/build-asan.  `src/cpus/Makefile.skel:134-135` regenerates it from the generator binary at build
time; `tools/precommit_check.sh` has 0 hits for `tmp_` or `generate_`.  Astra Q1 (:7-20), Grok Q1 (:5-24) and
CRIT_RULINGS.md:13 all describe the repair as a generator edit only.  Consequences the panel must settle: whether the
diff also carries the regenerated table (24 lines `NULL` -> name) plus est/ and build-tree propagation; and that a
detector in GATE 2's `#375` idiom (reads the COMMITTED table, `regress/gate_offline.sh:26-72`) would stay green if only
the generator were reverted, because the build regenerates and the committed copy does not.
**Disposition:** brief S14 + P4; asked in Q1(d), Q2(a)(b), Q3(a).

## 2. "cpu_m88k.c:130 forces big-endian" is true of the constructor only (Grok vs source); the seats disagree on the endianness axis
Grok :13 ("forces big-endian, and xmem always adds `ENDIANNESS` (16) ... endianness is not a floor axis").  Source:
`src/core/emul.c:651-652` applies the file loader's byte order after construction (`src/file/file_elf.c:693-694`
reports `EMUL_LITTLE_ENDIAN` for an `ELFDATA2LSB` file), and `emul.c:737-738` applies a configuration-file
`byte_order` (`src/core/emul_parse.c:493-499`).  So the little-endian half (12 of 24 slots) is reachable in principle.
Astra :14 counts LE and BE in its 24; Grok excludes endianness as an axis.  (Both can stand: the repair maps LE and BE
byte slots to the same 12 names -- `generate_m88k_loadstore.c:74-75` -- so the difference is which rows are owed, not
what the repair does.)
**Disposition:** brief P1; reconciliation asked in Q2(c).  Not settled by the drafter.

## 3. Clause (c): both seats name an identity body because the packet told them to; the owner's ruling makes the detector offline (seats vs rules)
Astra :13 ("an identity `xmem` body that retires without exchanging anything"); Grok :19 ("Identity body: decode,
retire, write neither rD nor memory").  The crit packet stated the floor that way (`crit_20261022/packet.md:13`).
`WITNESS_ATTEMPT.md:18-19` (owner ruling) names an OFFLINE regression detector.  The clause-(c) rule
(`tools/CLAUDE.md` working tree :1340-1348) picks the medium by instrument kind: an `#include` differential's medium is
a comment-only product source that fails to compile; an identity body is the medium for an instruction-handler round.
A table-census detector does not execute a handler body at all.
**Disposition:** brief P6; asked in Q2(a) and Q3(c).

## 4. Records still say DISPUTED / witness none, and the witness record is untracked (records vs rulings)
Ledger row state_note (HEAD) "Fix shape DISPUTED (D1) ... Pass 1 of the round settles it" and "witness: none --
research finding, not yet reproduced here"; `OUTSTANDING_BUGS.md:28-29` and `:25263` "fix shape disputed; pass 1
settles it".  `CRIT_RULINGS.md:13`, committed in the same HEAD, records T1 SETTLED / READY.
`regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md` (BLOCKED, owner ruling) is UNTRACKED
(`git ls-files` empty for that directory).
**Disposition:** stated in brief sections 1-2; the records correction and committing the witness file are the
coordinator's (this drafter is read-only).

## 5. The rules the brief applies are uncommitted (rules provenance)
Clause (c) by instrument kind, the two record forms, and rule D2 exist only in the WORKING-TREE `tools/CLAUDE.md`
(:1340-1367, :1557-1566) and `tools/BRIEF_TEMPLATE.md` (854 lines; HEAD has 702, no section C6/C7; last committed
`0aaaf5bc` 2026-09-10; working-tree mtime 2026-10-09).  `git log -S` finds no commit ever containing those texts.
HEAD's carrier (:1281-1285) still has the superseded clause-(c) wording.
**Disposition:** brief section 10 quotes the working-tree texts and states this provenance.

## 6. Grok's literal edit would not compile (Grok vs source)
Grok :9 "Delete that `continue` and let `:259-262` call `print_function_name`."  At
`generate_m88k_loadstore.c:254-257` the `printf("\tNULL");` (:255) precedes the `continue` (:256); removing only the
`continue` prints `NULL` and a handler name for the same entry -- a syntax error in the generated file (loud, not
silent).  CRIT_RULINGS.md:13 says ":254-257" (the whole arm).
**Disposition:** brief P5; Q1(c).

## 7. Accept rows sit at WORD; the growth variant names HALF or WORD; rule D2's edge is HALF (seat-internal + rules)
Grok :22 accept "a scaled word `xmem` still uses scale 4", growth "a scaled half or word slot is aliased to the byte
function"; Astra :15 "scaled wider operations".  The alias depends on `scaledness && size > 0`
(`generate_m88k_loadstore.c:80`), whose B+1 edge is size 1 (halfword); `xmem` has no halfword form
(`cpu_m88k_instr.c:3585-3590`), so a halfword row is `ld`/`st`-only.  No seat names a scaled-halfword accept row.
Linked question: that predicate is in a CALLEE of the edited function, and the DEPENDS-ON bound stops at the enclosing
function (`tools/CLAUDE.md` working tree :1448-1451).
**Disposition:** Q2(c)(d).

## 8. The two (d) specifications differ, and Grok's notation is ambiguous (seat vs seat)
Grok :20 names cells (`&& no_pc_sync`, `&& !no_pc_sync`, one signed scaled `ld.b`, one `.usr` scaled `ld.b`/`st.b`);
read literally as conjuncts on the NULL arm, "`&& no_pc_sync` leaves scaled `ld.b` dead" is backwards -- it is
consistent only if the conjunct attaches to the REPAIR.  Astra :13 "repair-null variants that retain selection but
omit the required mapping or effect" names no concrete form.  The repair is a pure deletion, for which the rule says
re-introduce the behaviour under a DIFFERENT predicate (`tools/CLAUDE.md` working tree :1432-1433).
**Disposition:** Q2(b) lists v1-v6 verbatim, asks equivalence and first-differing index, and asks for the notation to
be confirmed.

## 9. Astra's census oracle is relative (seat vs anchor rule)
Astra :14 "Check each against its corresponding unscaled entry" -- slot i against slot i-32.  A relative check is
satisfied by any edit that moves both together (anchor rule, `tools/CLAUDE.md` working tree :1814-1817).
**Disposition:** Q2(e).

## 10. Reachability of the 24 is narrower than either seat states (both vs source)
From the four producers (`cpu_m88k_instr.c:2377`, `:2411`, `:3087`, `:3622`): on a big-endian CPU today 8 slots have
a producer (176, 180, 184, 240, 244, 248 via `ld`/`st`; 432, 436 via `xmem`); 440/504 (and LE 424/488) have none
(`xmem` never adds SIGNEDNESS, the decoders never add NO_PC_SYNC); 496/500 (and LE 480/484) have none today because
`xmem_slow` takes `.usr` from `0x80` (:2359), which the register-form decoder rejects as `.wt` (:3606-3614) -- they
gain a producer if N2 (`m88kxmemusr`) is fixed.  Astra calls all 24 "valid repaired entries"; Grok's cells are a
subset.  Consistent with both, stated by neither.
**Disposition:** brief section 7 table (marked as the drafter's enumeration) + P2/P3.

## 11. Minor
* The "24" is Astra's count (:14).  CRIT_RULINGS.md:13 puts "(24 repaired table entries; ...)" beside "Grok Q1"; Grok's
  Q1 gives no count.  The committed-table census measures 24.  **Disposition:** census in section 7; no action.
* Working-tree drift: `regress/gate_offline.sh` differs from HEAD (uncommitted edits from line 1741 on; the cited
  ranges 26-72, 477-546, 982-986 are identical); `tools/pipeline/ledger.json` differs (another session's in-flight
  records).  **Disposition:** stated in brief section 0; the ledger row is quoted from HEAD.
* The verbatim quotes carry vocabulary the template's codex section flags ("Host dies", "death", "dead", "kills",
  "host SIGSEGV").  Kept verbatim as instructed; the drafter's own prose is neutral, codex's reading is scoped, and
  no question asks for a construction (v1-v6 are seat-supplied candidates in the template's substitute form).
  **Disposition:** risk named here; if the codex seat refuses twice, the template's two-refusal rule applies.
* Size: FULL 109,037 bytes, COMPACT 92,439 bytes -- above `panel.sh`'s 30,000-byte argv cap (pointer form for the
  argv-fed seats) and above the Gemini-web packet limit (60,000).  The carrier recommends one question per packet-fed
  firing.  **Disposition:** COMPACT asks the seat to answer Q1 and Q2 first; splitting is the coordinator's call.

## Template section F, self-check
* Settled premises present (section 5, S1-S14), each with the line re-read at HEAD.
* Cross-file citations: anchors verified unique (or counts given) by `grep -cF` against HEAD copies.
* Quotes marked VERBATIM are verbatim; the assembler re-reads every excerpt from its source after assembly (FULL 54,
  COMPACT 57, 0 mismatches).  Condensed: Grok line 1 (narration before `VERDICT:` cut, marked `[...]`); COMPACT's
  section 4 (a table, labelled CONDENSED) and its trimmed excerpts (gaps marked).
* State claims true as of sending: nothing is described as shipped; C0 says NOT SHIPPED.
* Pass-2-only numstat item: not applicable (pass 1).
* Every named path checked by `ls` (`LS_PERMITTED.txt`): none missing.
