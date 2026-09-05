OPUS PASS-4 SEAT -- pcc2widthkills.  Premises RE-DERIVED FROM SOURCE (not from the packet).
Tree: GXEMUL-SEC @ b78bb0f + uncommitted.  Every citation below was opened, not quoted.

P1  fatal() RETURNS, no early-out.
    src/core/debugmsg.c, `void fatal(const char *fmt, ...)' -> va_start/va_debug/va_end. CONFIRMED.

P2  memory_rw dispatches a device only under !no_exceptions || DM_READS_HAVE_NO_SIDE_EFFECTS.
    src/cpus/memory_rw.c, grep anchor `if (!no_exceptions || (mem->devices[i].flags &'.  CONFIRMED.

P3  pcc2 registers DM_DEFAULT, length 4096.
    src/devices/dev_pcc2.c, grep anchor `memory_device_register(devinit->machine->memory, "pcc2"'
    -> addr, 4096, dev_pcc2_access, d, DM_DEFAULT, NULL.  CONFIRMED.
    PCC2_SIZE = 0x0040 (src/include/thirdparty/mvme_pcctworeg.h).  4096/0x40 aliasing preserves
    parity because 0x40 is even.  CONFIRMED.

P4  debugger `put b' uses memory_rw(...,1,MEM_WRITE,CACHE_NONE|NO_EXCEPTIONS) DIRECTLY;
    `put h/w/d' use store_16/32/64bit_word, which call memory_rw with CACHE_DATA (no
    NO_EXCEPTIONS).  src/debugger/debugger_cmds.c `case 'b':' / `case 'h':' / `case 'w':' /
    `case 'd':'; src/core/memory.c `int store_16bit_word' / `int store_64bit_word'.  CONFIRMED.
    => the pass-3 `put b' finding is right, AND `put d' reaches the arms at len 8.

P5  m88k alignment check precedes memory_rw and is skipped for bytes.
    src/cpus/cpu_m88k_instr_loadstore.c, `#ifndef LS_1' / `if (addr & (LS_SIZE - 1))' ->
    m88k_exception(M88K_EXCEPTION_MISALIGNED_ACCESS) then return, BEFORE the
    `#ifdef LS_LOAD ... cpu->memory_rw' block.  CONFIRMED.

P6  d->warned is written in EXACTLY ONE place.  grep -n warned dev_pcc2.c -> :398 (test),
    :399 (|=), plus the struct field and an UNRELATED function-static `warned' in the
    read-span arm.  CONFIRMED.  12 call sites of pcc2_width_decline (13 occurrences - 1 def).

P7  reassert_interrupts(): 8 calls inside the switch = 7 of the twelve blocks + SCCRXIACK.
    TxCTL does NOT reassert.  The product comment's "seven of the twelve ... (five of those
    eight)" is CORRECT.  RE-DERIVED, contradicts nothing.

P8  SCCERR's E warrant HOLDS but its named deriver cannot establish it.  The arm's store is
    `d->pcctwo_reg[relative_addr] = 0;' -- addressed by relative_addr, NOT by the name.  So
    the contract's "(grep SCCERR dev_pcc2.c)" keys on a CORRELATE, not on the class.  The
    claim is true; the deriver is wrong.

INSTRUMENT PROVENANCE (derived by md5, not from the packet):
    part2   23330  cd22f951   part3   32868  3dcf73de
    part3b  33119  280d9ab3   part3c  34288  72759b4f  == the ON-DISK probe (byte-identical)
    part3 -> part3b delta: `rb t1ctl'/`rb t1icr' want string ONLY.  Row-name set identical.
    part3b -> part3c delta: `acc all' session (put b -> guest st.b) + docstring.  Same set.
    => on the SHIPPED bytes only BASE and M_GROW_PSCALEADJ have ever run.  The other four
       part-3/3b mutants TRANSFER (each killing row untouched by both deltas) -- true, but
       the brief's table does not say three instruments were involved.

GATE/PROBE CONSISTENCY (mechanical):
    gate_arm.sh row list = 96 names, 0 duplicates, max length 14 (< the probe's 15-char
    assert and < the %-16s column) -> the padded-column trap cannot fire.
    comm against part3c/BASE.out's 96 emitted names: EMPTY both directions.  Denominator
    pins 96/96/0 consistent.

CELL CENSUS (12 blocks x 9 shapes = 108):
    ~27 M, ~28 S, 1 E (SCCERR FALL), 6 UNREACHABLE (odd blocks' RDDECL),
    and 41 cells whose SOLE carrier is one of three aggregate rows:
        latch all    -> ALIAS x12 + SWAP x11   = 23
        latch all w  -> LEN2 x11               = 11
        acc all      -> GROW x7 (C-only blocks)=  7
    The round has ALREADY measured one of those three vacuous (acc all's put-b form).

================================ MEASURED, PASS 4 (this seat) ================================
Scratch clone /tmp/gxopus_p4 (cp -a of build/); frozen instrument md5 72759b4f == the SHIPPED
probe byte-for-byte; sentinel dropped per mutant; restored + rebuilt + verified against SEC;
build/ never written (no .MUTANT, git status unchanged).  driver.log in this directory.

  BASE            96/96   -                       (reproduces part 3c in an independent clone)
  M_LATCHASSIGN   96/96   TOTAL CLEAN SWEEP       `d->warned |= (1u << bit);'
                                                  -> `d->warned = (1u << bit);'   ONE CHARACTER
                          proof: 0 x '|=', 1 x 'd->warned = ' in source; binary 18:21:46 newer
                          than source 18:21:45.  0 FAIL rows in M_LATCHASSIGN.out.
  M_BITSHIFT      96/96   escape, but EQUIVALENT  `1u << bit' -> `1u << (bit + 1)'
                          (12 distinct bits, all < 32, no collision, bit identity has no
                          consumer outside the helper).  Clause-(f) control: it shows the
                          cardinality rows are DISTINCTNESS-only, which is SAFE here for a
                          reason the contract does not state.

WHY M_LATCHASSIGN ESCAPES, derived before it was built: no session in the probe writes wide
to block A, then to a DIFFERENT block, then to A again.  Every session has either exactly one
wide write, or two ADJACENT writes to the SAME block (`latch same'), or 12 writes to 12
DISTINCT blocks (`latch all', `latch all w').  Under `=' each of those still announces exactly
as under `|='.
CHEAPEST REPAIR: one session, one row.
  t,_,how = session(setup(r6="0xaabb") + program([ST_H(6,GENCTL), ST_H(6,T2CTL), ST_H(6,GENCTL)]))
  row("latch aba", t.count("write to PCCTWO_GENCTL " + DECL), 1,
      "A,B,A -> GENCTL announces ONCE: the latch ACCUMULATES, it does not just remember the last")
