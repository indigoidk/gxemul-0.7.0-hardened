# `wdclbaaddr` -- RUNG-3 WITNESS, measured 2026-10-24 17:03:32 on the committed build, BEFORE any product edit

Instrument: `regress/wdc_lba_probe.py`, md5 `8f3632ffc1c982fd523c7fd28d86f15d` (frozen copy beside this file:
`wdc_lba_probe.frozen.py`), base leg only (`<fix_bin>` = `-`).  Binary: `/tmp/gxt2/base/gxemul` (2026-10-24 05:35:58,
6,159,736 b), whose `src/devices/dev_wdc.c` is md5 `714071619d8f98e85fe48ae566139345` == `GXEMUL-SEC/src/devices/dev_wdc.c`
== HEAD cc1f69cc (the file last changed in e16a8b7c); two-part clearance printed by the runner (`cmp CLEAN`, binary newer than
source).  Machine: `evbmips -e malta`, UNMODIFIED, the wdc reached through the machine's own committed piix4_ide path; the disk
image (4096 sectors, sector n tagged `(n, ~n)` in words 0-1) is attached with `-d iR:<image>`, ordinary operation.
Run dir `/tmp/gxt2/work/t4/witness_20261024_170332` (volatile); durable copies here: `RESULTS_base.txt`, `RUN_IDENTITY.txt`,
`raw/<session>.txt` (six pty transcripts) and `raw/<session>.bin` (the six guest programs).

## The measured rows (verbatim from `RESULTS_base.txt`; H = IDENTIFY word 3 = 16, S = word 6 = 63)

    chs s1          0xffff0000   want 0xffff0000   ok        <- tag 0   (CHS cyl 0 sector 1)
    chs s2          0xfffe0001   want 0xfffe0001   ok        <- tag 1   (CHS cyl 0 sector 2)
    chs h1          0xffc0003f   want 0xffc0003f   ok        <- tag 63  (CHS head 1 sector 1 = index S)
    sdh rb          0x000000e5   want 0x000000e5   ok        <- SDH readback byte-exact
    sdh rb2         0x000000b3   want 0x000000b3   ok
    lba 70          0xffba0045   head 0xffba0045 fix 0xffb90046 [HEAD] ok   <- LBA 70 was SERVED AS tag 69 (CHS sector 70)
    lba 256         0xfc1003ef   head 0xfc1003ef fix 0xfeff0100 [HEAD] ok   <- LBA 256 was SERVED AS tag 1007 (= H*S - 1)
    lba 0           0x00000000   head !=0xffff0000 fix 0xffff0000 [HEAD] ok <- LBA 0 served zeros (CHS "sector 0")
    lba wr          0xffb90046   head 0xffb90046 fix 0x88887777 [HEAD] ok   <- the LBA-70 WRITE did not reach index 70 (tag 70 intact)
    lba wr2         0x88887777   head 0x88887777 fix 0xffba0045 [HEAD] ok   <- ... it landed at index 69 (CHS sector 70)
    id w49          0x00000000   want 0x00000000   ok        <- IDENTIFY word 49: LBA not advertised (unchanged by this round)
    19/19 passed   CONTROL=PASS   LEG base VERDICT: PASS      <- judged against the HEAD column; against the FIX column the
                                                              five `lba *` rows are RED -- that is the pre-fix symptom

Controls, per the witness ladder: LIVENESS -- a `sh`/`lhu` round-trip of 0x5a5a through plain RAM in every session (six
`ram:*` rows) and every session parked at its halt breakpoint; DEVICE SIGNATURE -- the tags `(n, ~n)` exist only in the image,
so a RAM cell could not have returned them (the IDENTIFY geometry words and the SDH readback are liveness of the register
file, not signatures: a RAM cell returns a written byte just as faithfully -- corrected 17:5x after the brief drafter's
NOTES.md item 19); ENCODINGS -- 490/490 hand-encoded
words agree with the emulator's own disassembler (per session 62, 50, 14, 36, 22, 306).  One MNEMONIC rendering differed and
is not a defect: `addiu t3,zr,0x8888` is printed by the disassembler as `addiu t3,zr,-30584` (the immediate is sign-extended;
the stored 16-bit value is 0x8888 either way, and the word `240b8888` matched).

## What this licenses

The reproduce step of the lifecycle is satisfied at rung 3 on the committed build, in the ORDER the witness ladder's clause (i)
demands (the symptom shown on the pre-fix committed build first; the same instrument must go green on the fixed build
afterwards).  Ledger witness term on closure: `probe:regress/wdc_lba_probe.py -- rung 3, unmodified evbmips -e malta, this
dir`.  The round's product edit has NOT been made at the time of this record.

Provenance of the binary beyond the one file: `/tmp/gxt2/base` was cloned from the working tree at 05:35 on 2026-10-24,
before #571 landed; its `src/` differs from HEAD in files off the malta/wdc path (the pre-#571 `cpu_ppc_instr.c` and the
peer session's uncommitted Alpha/LCA/PCC2/SH4 files).  `dev_wdc.c`, the file under test, is byte-identical to HEAD (md5 above).
Two witness rows (`lba wr`, `lba wr2`) read back through CHS sector numbers 71 and 70 with S = 63 -- sector numbers outside the
1..S range ATA-2 defines, served only because the model does not validate CHS triples; the shipped detector will use the valid
triples (head 1, sector 8) and (head 1, sector 7) for the same indices (drafter's NOTES.md item 16).  The measurement stands:
the model served the offsets its formula computes.
