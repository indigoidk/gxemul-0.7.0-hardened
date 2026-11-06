#!/bin/bash
#  replay_fbs.sh -- gate 14's footbridge block as staged (dryrun_fbs.py), its probe call replaced by a banked log
set -u
. "$LIBSH"
FBLOG=$LOGDIR/footbridge_sites.log
cp "$SRCLOG" "$FBLOG"   # REPLAY: the probe call replaced by a banked log
grep -E "^(  arm |C[0-9]|A[0-9]|I1|H[12]|D1|E(C1|A1|[0-6])|S(C1|A1|[1-5]|F[12])|N[0-5O]|[MOXWBU](C|[1-3])) " "$FBLOG" | sed 's/^/       /'

if ! grep -q "FOOTBRIDGE_SITES_" "$FBLOG"; then
    note "footbridge probe produced no verdict; last lines follow"
    tail -5 "$FBLOG" | sed 's/^/       /'
    check "footbridge probe completed" "no" "yes"
else
    #  THE CONTROL FIRST, and separately from the verdict.  A probe whose controls failed has
    #  measured NOTHING, and this one has a control that a liveness row cannot substitute for.
    check "footbridge: controls prove the probe measures" \
          "$(grep -c 'FOOTBRIDGE_SITES_CONTROL=OK' "$FBLOG")" "1"
    check "footbridge: every row green" \
          "$(grep -c 'FOOTBRIDGE_SITES_PASS' "$FBLOG")" "1"
    #  VALUES, NOT SURVIVAL.  0x1011 is DC21285_VENDOR_ID (dev_footbridge.c `case VENDOR_ID`)
    #  and is a MODEL value: real hardware packs DeviceID:VendorID into a word read at +0x0,
    #  so the round that fixes packed config reads changes this pin in the same commit.  It can only
    #  have come back through this device; an unmapped read survives too, it just returns 0.
    check "footbridge: VENDOR_ID 0x1011 through a real guest ldr" \
          "$(grep -cE '^A1 .*got=0x00001011 .*ok$' "$FBLOG")" "1"
    #  The vanishing top byte IS the handler's signature: `case TIMER_1_LOAD`'s write branch stores
    #  idata & TIMER_MAX_VAL.
    #  RAM, or any decode that merely absorbed the store, returns 0x12345678 unchanged.
    check "footbridge: TIMER_1_LOAD masked to 24 bits by the handler" \
          "$(grep -cE '^A2 .*got=0x00345678 .*ok$' "$FBLOG")" "1"
    #  THE PROBE'S OWN FAILABILITY CONTROLS -- #545 replaced the kill bridge (arm K, a +0x18c read
    #  the device used to answer with exit(1); #545 declines it) with two HARNESS legs, pinned by
    #  their DISCRIMINATING tokens, not by the rows existing:
    #    H1 an unknown -E name: NO prompt, the diagnostic NAMING the input, WIFEXITED && == 1.
    #       Five different startup refusals all exit 1 with no prompt, so the text is the pin.
    #    H2 quit after a VERIFIED prologue (fresh-reg values), the next send dead BEFORE
    #       teardown, reaped exit 0 -- a child dead before the prologue shows `dead` identically,
    #       so the prologue clause and exit 0 are both required, and both are in the row.
    check "footbridge: H1 startup leg green (unknown -E named, exit 1)" \
          "$(grep -cE '^H1 .*named=True .*ok$' "$FBLOG")" "1"
    check "footbridge: H1's diagnostic names the rejected input" \
          "$(grep -c 'Sorry, emulation "no-such-machine-fbd5" is unknown' "$FBLOG")" "1"
    check "footbridge: H2 quit leg green (prologue verified, dead, exit 0)" \
          "$(grep -cE '^H2 .*prologue=True next=False dead=True exit=0 .*ok$' "$FBLOG")" "1"
    #  #545: the five declined sites, ONE process (arm S).  N0 counts five DISTINCT once-announces
    #  (a shared or aggregate latch reads 4 or 1); N1-N5 count each site's text over the whole arm and NO
    #  requires the announces in site order (ORDER, not emitter); S1-S5 and SF1/SF2 pin every
    #  interrupt register unchanged through the declines, with the FINAL raw reads after the last write
    #  of every pair.  Every family is pinned by its DISTINCT green ids (a duplicated green line cannot
    #  stand in for a missing id -- pass 2), and the probe's own total by ROWS= (37 at #545; 56 since
    #  #585 added the nineteen SDRAM rows below).
    check "footbridge: the sites probe ran all 56 rows green (ROWS=56 of 56)" \
          "$(grep -cE '^ROWS=56 of 56$' "$FBLOG")" "1"
    check "footbridge: arm S controls SC1, SA1 -- two DISTINCT green ids" \
          "$(grep -E '^S(C1|A1) .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "2"
    check "footbridge: N0 five sites, one process, five distinct once" \
          "$(grep -cE '^N0 .*distinct-once=5 fatals=5 exit=0 .*ok$' "$FBLOG")" "1"
    check "footbridge: NO the five announces arrive in access order" \
          "$(grep -cE '^NO .*order=N1,N2,N3,N4,N5 .*ok$' "$FBLOG")" "1"
    check "footbridge: N1-N5 each announced exactly once (count=1)" \
          "$(grep -cE '^N[1-5] .*count=1 .*ok$' "$FBLOG")" "5"
    check "footbridge: N1-N5 are five DISTINCT green row ids" \
          "$(grep -E '^N[1-5] .*count=1 .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "5"
    check "footbridge: S1-S5 the legal reads between the declines -- five DISTINCT green ids" \
          "$(grep -E '^S[1-5] .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "5"
    check "footbridge: S3 IRQEnable intact at 0x30 through the declines" \
          "$(grep -cE '^S3 .*got=0x00000030 .*ok$' "$FBLOG")" "1"
    check "footbridge: SF1/SF2 final raw status reads -- two DISTINCT green ids, both 0" \
          "$(grep -E '^SF[12] .*got=0x00000000 .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "2"
    #  #545: the corrected controls -- C4 now requires the key present; C5 requires arm T's exit 0.
    check "footbridge: C4 the MMU-on arm cannot see the device (key present)" \
          "$(grep -cE '^C4 .*ok$' "$FBLOG")" "1"
    check "footbridge: C5 the MMU-on control arm survives, exit 0" \
          "$(grep -cE '^C5 .*ok$' "$FBLOG")" "1"
    #  #539: IRQEnable (+0x188) is readable -- reset 0, Set ORs, Clear clears, byte and
    #  halfword reads return the low lanes -- and arm E raises no footbridge diagnostic.
    #  Seven value/text rows, pinned by count AND by the two that carry the datasheet claims.
    check "footbridge: IRQEnable ACCEPT rows E0-E6 all green" \
          "$(grep -cE '^E[0-6] .*ok$' "$FBLOG")" "7"
    #  Seven green lines are not seven rows: a duplicated id could stand in for a missing one, so
    #  the DISTINCT ids are counted OVER THE GREEN LINES -- seven distinct green ids proves
    #  "each of E0-E6 is green" by itself (fable5, #539 F2: counting ids over all lines would
    #  pass a duplicated green E2 beside a red E3).
    check "footbridge: E0-E6 are seven DISTINCT green row ids" \
          "$(grep -E '^E[0-6] .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "7"
    check "footbridge: IRQEnable reads 0 at reset (E0)" \
          "$(grep -cE '^E0 .*got=0x00000000 .*ok$' "$FBLOG")" "1"
    check "footbridge: Set ORs (E2 = P|Q; Clear is pinned by E5)" \
          "$(grep -cE '^E2 .*got=0x60002002 .*ok$' "$FBLOG")" "1"
    #  #585 fbsdrampair: a guest READ of SDRAM_BA_MASK (+0x100) or SDRAM_BA_OFFSET (+0x104) used to end
    #  the emulator (fatal() then exit(1)); both are R/W (DC21285 7.3.9, 7.3.10) and both write arms keep
    #  nothing, so the read is DECLINED with 0 and announced once per register.  Six arms, one process
    #  each: M and O read one register three times (one site per process, so the pre-fix build shows
    #  each site's own death), X reads both (per-register latches), W only writes (a write never takes the
    #  read path; HEAD's write announces intact), B writes, reads, writes again (writes are not kept; a
    #  write with the read latch set still takes the write path), U is M's reads with the MMU left ON
    #  (never the device).  Each control (MC OC XC WC BC UC) is a `reg` taken BEFORE the arm's first
    #  SDRAM access, so the pre-fix build reds M1-M3 O1-O3 X1 B1-B3 under green controls (measured,
    #  regress/artifacts/fbsdrampair/impl_20261105/probe_HEAD.out: ROWS=46 of 56, CONTROL=OK).
    check "footbridge: SDRAM controls MC OC XC WC BC UC -- six DISTINCT green ids" \
          "$(grep -E '^[MOXWBU]C .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "6"
    check "footbridge: SDRAM rows M1-M3 O1-O3 X1 W1 W2 B1-B3 U1 -- thirteen DISTINCT green ids" \
          "$(grep -E '^([MOB][1-3]|X1|W[12]|U1) .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "13"
    check "footbridge: M2 three SDRAM_BA_MASK reads each return 0 (the declined value)" \
          "$(grep -cE '^M2 .*r7=0x00000000 r8=0x00000000 r9=0x00000000 .*ok$' "$FBLOG")" "1"
    check "footbridge: O2 three SDRAM_BA_OFFSET reads each return 0" \
          "$(grep -cE '^O2 .*r7=0x00000000 r8=0x00000000 r9=0x00000000 .*ok$' "$FBLOG")" "1"
    check "footbridge: X1 one read announce per register, mask first" \
          "$(grep -cE '^X1 .*order=mask,offset .*ok$' "$FBLOG")" "1"
    check "footbridge: B1/B2 a written mask/offset is not kept (reads 0 after a write)" \
          "$(grep -cE '^B[12] .*r[78]=0x00000000 .*ok$' "$FBLOG")" "2"
    #  The defence against the hand-assembled-encoding trap: every planted word is compared
    #  against the disassembly the emulator printed AS IT STEPPED IT.
    check "footbridge: no planted word failed its disassembly check" \
          "$(grep -c 'DISASSEMBLY MISMATCH' "$FBLOG")" "0"
fi
echo "REPLAY_DONE checks=$_checks fails=$_fails"
