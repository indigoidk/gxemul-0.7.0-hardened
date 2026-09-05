pcc2widthkills PASS 6 -- Opus seat, source-verified notes (tree: GXEMUL-SEC, b78bb0f + uncommitted repair)

RE-DERIVED FROM SOURCE (not from the packet):
  dev_pcc2.c:399-406 helper; :408-668 DEVICE_ACCESS; 12 decline call sites (grep -c = 12)
  :414 relative_addr %= PCC2_SIZE(0x40) -- even modulus, parity preserved      VERIFIED
  :419-432 read memcpy; :420 end-span guard                                     VERIFIED
  :472-474 counter memcpy, relative_addr in {0x04,0x08,0x0c,0x10}, max span 0x18 -> cannot
        reach SCCERR 0x1c; CAN reach PSCALEADJ 0x15 / T2CTL 0x16 / T1CTL 0x17   VERIFIED
  :735 DM_DEFAULT registration                                                  VERIFIED
  memory_rw.c:584-585 dispatch iff (!no_exceptions || DM_READS_HAVE_NO_SIDE_EFFECTS)  VERIFIED
  memory_rw.c:604 "failed ]" is a debug(), not a fatal()                        VERIFIED
  cpu_m88k_instr_loadstore.c:167-185 #ifndef LS_1 alignment check               VERIFIED
  memory.c store_16bit_word -> ONE memory_rw(len 2, CACHE_DATA)                 VERIFIED
  memory.h:117-118 MEM_READ 0 / MEM_WRITE 1                                     VERIFIED
  debugger.c:800 timer_stop; :836 step returns; :840 timer_start                VERIFIED
  timer.c:284 callbacks run ONLY from the SIGALRM handler                       VERIFIED
  dev_pcc2.c:62 DEV_PCC2_TICK_SHIFT 14 -> DEVICE_TICK never fires under step 4  VERIFIED
  counts: 8 masking/RMW/clearing arms; 7 of 12 blocks call reassert_interrupts;
          5 of those 8; 3 other files emit the DECL suffix (gdrom, sgi_re, sh4) ALL CORRECT
  gate list: 118 names, no duplicates, all <= 15 chars; probe emits 118; sets identical

F1  d->pending_timer1_interrupts / pending_timer2_interrupts are DIRECT reads of the TxICR
    guarded body (:528, :533) and are ZERO at every decision point in all 118 rows.
    Writers: pcc_timer_tick (:249,:251) only, a timer_add/SIGALRM callback -- stopped for the
    whole of every `step'.  Second independent reason: no row writes T1CMP/T2CMP, so
    compare==0 and `old_count < compare' is unsatisfiable.
    PRETABLE.out Section 1 line 31 NAMES the field as a body read; the "Disagreeing states"
    lines 34-39 convert only `idata'.  The owed disagreeing state was never written.
    MUTANT M2: `&& d->pending_timer1_interrupts == 0' at the TxICR guard -> predict 118/118.

F2  No row observes the LANDING channel at len 4 or len 8.  Census of device-directed wide
    writes in the instrument: 42 at len 2, 12 at len 4 (latch all w), 12 at len 8 (latch all d),
    plus one guest ST_W at SCCERR (value-identical).  latch all w / latch all d read only
    t.count(DECL); neither has a readback or liveness row.  Every rb*/rb2* readback is st.h /
    put h, len 2.  So the contract sentence "latch all, latch all w and latch all d pin the
    REFUSAL at every block for each non-byte width" is false: they pin the ANNOUNCE.
    MUTANT M1: `break;' -> `if (len < 4) break;' at all twelve -> predict 118/118.

F3  d->pcctwo_reg[relative_addr] is driven non-initial at 9 blocks by a byte pre-set, but only
    at BYTE granularity.  The one BIT the TxICR body reads (PCC2_TTIRQ_INT 0x20) can never be
    set by a guest write (`&= ~0x17' / `|= idata & 0x17' both exclude it) and is set only by
    reassert_interrupts under pending_timer* > 0.  So `&& !(d->pcctwo_reg[relative_addr] &
    PCC2_TTIRQ_INT)' at TxICR is F1's twin and escapes for the same reason.

F4  d->pcctwo_reg[PCCTWO_IPL] is 0 in every session (memset; reassert_interrupts:274 zeroes it;
    the IPL write body stores nothing).  It is read by the IPL arm's READ branch (:633).
    `&& d->pcctwo_reg[PCCTWO_IPL] == 0' at the IPL guard escapes; consequence is message-only.

F5  d->cur_int_vec[] -- read by NO guarded body in DEVICE_ACCESS(pcc2) (only
    dev_mvme187_iack_access:679).  Outside the clause-(d) rule-(2) closure.  Honest N/A.
    Bounds are correct: PCC2_TTIRQ_IL/PCC2_IRQ_IPL = 0x07, INTERRUPT_LEVEL_MASK = 0x07,
    array is [8].

F6  The announce-ONCE property is pinned at len 2 only (latch same / same2 / aba are all st.h /
    put h).  latch all w / d write each block once, so a per-width flood is invisible.
    Coverage debt, records severity.

F7  `latch all fail' is the SOLE carrier of the FAULT member at the six operator-only blocks
    (L3), and its channel is memory_rw.c:604 debug(), not fatal().  debug() is verbosity- and
    single-step-gated; fatal() is not.  Disclose the dependency.

F8  RECORD: PRETABLE_pass4.out mtime 20:23:26 > part4/driver.log 19:10:26.  Its own first line
    ("its own file so its mtime is its own order witness for part 4") and PRETABLE.out:22-23
    ("Only PRETABLE_pass4.out and PRETABLE_pass5.out carry their own order witness") are both
    false at HEAD.  PRETABLE.out:19-20 records an 18:35 re-stamp; the actual mtime is 20:23:26,
    so there was a LATER one the file does not record.  PRETABLE_pass5.out 20:23:26 <
    part5/driver.log 20:54:17 -- that one HOLDS.

F9  PRETABLE Section 1's shared-bitfield deriver greps the NAME `warned', which conflates
    d->warned with the unrelated function-static `warned' at dev_pcc2.c:423.  The conclusion
    (one writer) is right; the deriver keys on a correlate.  Its "lines mentioning 'warned': 7"
    is 8 at HEAD (the typedef added two).

ONE-CHARACTER / ONE-TOKEN SWEEP -- no escape found (denominator):
  len != 1 -> {!= 0 (acc all), != 2 (rb *), > 1 (equiv), > 2 (rb *), == 2 (latch all w)}
  writeflag == MEM_WRITE -> {<= (hrd * nod), != (rb *), >= (equiv)}
  && -> || (acc all)
  helper TEST: & -> == (latch aba), & -> | (rb genctl dcl), !(x) -> (x) (rb genctl dcl)
  helper SET: |= -> = (latch aba), (1u<<bit) -> 1 (latch same2), << -> >> (latch same2),
              |= -> ^=/+= (equivalent under the TEST), bit -> bit+1 (equivalent, disclosed)
  enum member aliased (latch all), break -> return 1 (equivalent), break -> return 0
              (latch all fail / hwr * lv)
  relative_addr conjunct at the shared blocks (rb t1ctl / rb t1icr / rb t2ctl / rb t2icr)
