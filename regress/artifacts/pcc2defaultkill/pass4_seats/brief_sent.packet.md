# #501 pcc2defaultkill -- PASS 4: the pass on the PASS-3 REPAIR DIFF.  Pass 3 measured six clean sweeps of the 36-row detector (one the mirror of the cell pass 2 had closed) and derived four more; the repair appends ten rows to existing sessions and this pass reviews THAT diff.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A repair made in response to a pass owes its own pass, scoped to the repair diff -- **but the FLOOR QUESTION is asked of
the shipped COMPOSITE**: does a clause-(d) mutant exist that sweeps the 46-row detector clean?  Two passes running, seats
that READ said close and a seat that BUILT found sweeps.  Build (or derive with the row list in hand), do not vote.  The
pass-3 repair closed the announce's VALUE channel on the arm the pass-2 mutant had NOT used -- the `#499` shape -- so ask
first: **what is the mirror of each new row?**  Be harder on the accepted dispositions; a seat whose escape was adopted
scrutinises its own repair row MORE (does the row kill the mutant for the reason claimed, or by accident?).  **VERDICT
LINE FIRST.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/`, UNCOMMITTED on top of `7076134`.**  Three
pristine-2021 copies of `src/` under the project root are NOT this fork; if your line numbers disagree by hundreds you are
reading one -- say so.  The pass-3 product state is preserved verbatim as
`regress/artifacts/pcc2defaultkill/killtable3_20260905/dev_pcc2.pass3.c` and the pass-3 instrument as
`killtable3_20260905/frozen_probe.py` (md5 10737375): the diffs below are against THOSE.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot
settle from this packet rather than guessing at it.  Answer in under 600 words.
## PREMISES ALREADY SETTLED, RE-INLINED (each is a QUESTION if you can check it)

1. **The fix** (unchanged in substance since pass 1; unchanged in CODE since pass 2): the `default:` arm no longer calls
   `exit(1)`; a READ keeps the byte the memcpy served and is announced `served 0x%02x` from `data[0]` with its length;
   a WRITE is DECLINED (member 3) and announced with its length and value; one latched `fatal()` per offset per instance
   (`uint64_t warned_unimpl`, bit `relative_addr`, folded `%= PCC2_SIZE` (0x40) first so the shift is 0..63).  43 of the
   0x40 offsets reach the arm (18 named-unimplemented, 12 counter interiors, 13 the fork header leaves unnamed).
2. **The pass-3 repair to the product is TWO COMMENT SENTENCES** (the tick reason narrowed to the two COUNT words while a
   counter runs, with the end-span reason added; "a counter interior" -> "inside a running COUNT word").  No code line.
3. **The pass-3 escapes and the row that now kills each** (all ten rows APPENDED to existing sessions, zero new sessions):
     Opus M_WRVAL0 / M_WRDATA0  write announce value -> 0 / -> data[0] (MEASURED 36/36)  -> `wr val text', `wide wr val'
     Opus M_LASTBYTE            read announce data[len-1] (MEASURED 36/36)             -> `srvd half text' (0x56 of 0x5678)
     Opus M_RELOAD              read announce reloads the array (MEASURED 36/36)       -> DISCLOSED: no deterministic row
     Opus M_BACKEDLOW           member 6 for relative_addr < 0x14 (MEASURED 36/36)     -> `inword rdawr', `half wr rdawr'
     Opus M_LATCHOFF            latch SET only at IEICR/IEERR (MEASURED 36/36)          -> `inword msg', `unnamed msg'
     grok/Fable  `if (len == 2) exit(1);'                                               -> the srvd session (len-2 read+write)
     codex M_LATCH_RD_ZERO      latched-path READ response zeroed (derived)             -> `srvd rd latch', `srvd wr latch'
     codex len -> 4 on either arm (derived)                                             -> `srvd val text' (`(len 1)'), `wr val text'
   In table 4 each of the ten is scored by BOTH instruments: the pass-3 one (36/36 = the breach, measured -- M_RELOAD's
   46/46 on the new one is the DISCLOSED expectation) and the repaired one (red).  BASE is measured full on both.
4. **The offset axis is NOT floor** (the arm has no `if' on `relative_addr'; the switch tests cased vs uncased only) --
   pass 3 closed it per CLASS (named / in-word / unnamed: one count and one read-back each) and DISCLOSES single-offset
   scoping.  `len' is not tested by the arm either: width rows are CLAIM rows; len 1, 2 and 4 are now rowed both ways,
   len 8 (the m88k core issues ld.d/st.d) stays disclosed.
5. **The witness** (rung 3, unchanged): 7/13 on the committed build, 13/13 on the fix (`witness_20260905/`).
6. **The roster**: nine seats; agy DELIBERATELY NOT FIRED (measurement reserve).  Pass 3's glm burned twice (recorded as a
   seat failure); kimi paged the pointer form but exited without a verdict line while it waited on a scratch build.
   **This packet is therefore SHORT on purpose, and its questions are CLOSED where they can be.**

## THE MEASUREMENTS (every number names its log)

Table 4 (`killtable4_20260905/driver.log`; frozen repaired instrument md5 b9b2fadc == live; the pass-3 instrument
`old36/` 10737375).  `.old36` rows are the pass-3 instrument on the same binary.  PREDICTIONS (`PRETABLE_501c.out`, written
before the table): every mutant's predicted score and red set were EXACT except five SAFE misses of one class -- `srvd val
text` counted 2 under M_LATCHOFF, M_UNLATCH, M_WRLATCH and M_ABA (the repair appended a re-read of 0x05, which announces
again whenever 0x05 is left unlatched), and M_RDKILL additionally reddened `inword wr` and `unnamed wr` (their sessions now
end in a read).  No predicted red stayed green.  M_RELOAD 46/46 was PREDICTED (disclosed as unrowable).
    BASE               46/46    -
    BASE.old36         36/36    -
    M_WRVAL0           44/46    wr val text,wide wr val
    M_WRVAL0.old36     36/36    -
    M_WRDATA0          45/46    wide wr val
    M_WRDATA0.old36    36/36    -
    M_LASTBYTE         45/46    srvd half text
    M_LASTBYTE.old36   36/36    -
    M_RELOAD           46/46    -
    M_RELOAD.old36     36/36    -
    M_BACKEDLOW        43/46    inword rdawr,half wr rdawr,srvd wr latch
    M_BACKEDLOW.old36  36/36    -
    M_LATCHOFF         42/46    inword msg,unnamed msg,srvd val text,srvd half text
    M_LATCHOFF.old36   36/36    -
    M_HALFKILL         40/46    srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch
    M_HALFKILL.old36   36/36    -
    M_LATCHRD0         43/46    half wr rdawr,srvd rd latch,srvd wr latch
    M_LATCHRD0.old36   36/36    -
    M_LEN4R            44/46    srvd val text,srvd half text
    M_LEN4R.old36      36/36    -
    M_LEN4W            45/46    wr val text
    M_LEN4W.old36      36/36    -
    M_EXIT             7/46     named wr,named wr msg,named rd,named rd msg,named rd srvd,inword wr,inword msg,inword rdawr,inword rd,unnamed wr,unnamed msg,unnamed rdawr,unnamed rd,ieicr rdawr,ieerr rdawr,latch sameoff,sameoff val,latch twooff,latch rw one,latch rd rd,latch rd wr,latch aba,alias 0x6a,alias msg,dir wr text,wr declined,wr val text,dir rd text,srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch,wide wr,wide wr msg,wide wr val,wide rd,wide rd srvd
    M_UNLATCH          36/46    inword msg,unnamed msg,latch sameoff,latch rw one,latch rd rd,latch rd wr,latch aba,srvd val text,srvd half text,wide wr msg
    M_ONELATCH         38/46    named wr msg,named rd msg,named rd srvd,inword msg,unnamed msg,latch twooff,latch aba,srvd half text
    M_BACKED           38/46    inword rdawr,unnamed rdawr,ieicr rdawr,ieerr rdawr,sameoff val,half wr rdawr,srvd wr latch,wide wr
    M_RDKILL           16/46    named rd,named rd msg,named rd srvd,inword wr,inword msg,inword rdawr,inword rd,unnamed wr,unnamed msg,unnamed rdawr,unnamed rd,ieicr rdawr,ieerr rdawr,latch sameoff,sameoff val,latch rw one,latch rd rd,latch rd wr,dir rd text,srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch,wide wr,wide wr msg,wide wr val,wide rd,wide rd srvd
    M_DIRSWAP          37/46    named rd srvd,dir wr text,wr declined,wr val text,dir rd text,srvd val text,srvd half text,wide wr val,wide rd srvd
    M_WRLATCH          43/46    latch rd rd,latch rd wr,srvd val text
    M_WIDEKILL         35/46    srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch,wide wr,wide wr msg,wide wr val,wide rd,wide rd srvd
    M_OFFKILL          36/46    inword wr,inword msg,inword rdawr,inword rd,srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch
    M_SRVD0            44/46    srvd val text,srvd half text
    M_BACKED2          42/46    inword rdawr,unnamed rdawr,sameoff val,half wr rdawr
    M_ABA              42/46    inword msg,unnamed msg,latch aba,srvd val text

Gate 14 (`killtable4_20260905/gate14_501c.log`, run alone): pcc2 default rows emitted 46, green 46; pcc2 width
rows emitted 251, green 251; the gate's own line `PASS (867 checks)`; GATE_RC=0.

## SECTION F2 -- THE PASS-3 DISPOSITIONS, numbered (the adjudication the panel shares)

ACCEPTED, REPAIRED IN-ROUND (L1: the detector is uncommitted; the class closure per the repair-chain amendment)
 1. (opus5, MEASURED) M_WRVAL0 / M_WRDATA0 -- the write announce's value: `wr val text', `wide wr val'.
 2. (opus5, MEASURED) M_LASTBYTE -- `srvd half text' serves two bytes that differ (0x56 0x78).  L4 on the contract's
    "wrong or constant byte" claim: reworded to the rows.
 3. (opus5, MEASURED) M_BACKEDLOW, M_LATCHOFF -- one read-back and one count per offset class (`inword msg/rdawr',
    `unnamed msg/rdawr').  NOT 43 value rows (the #392 shape); single-offset scoping DISCLOSED.
 4. (codex, derived) M_LATCH_RD_ZERO -- `srvd rd latch' (bit set by a read), `srvd wr latch' (bit set by a write).
 5. (codex, derived) `len' -> `4' -- `srvd val text' reworded to `0x5 (len 1) -- served 0x34'; `wr val text' carries `(len 1)'.
 6. (grok, fable5) `len == 2' re-kill -- the srvd session's ld.hu/st.h/ld.hu (`srvd half text', `half wr rdawr'): the
    pass-2 len-2 disclosure is CLOSED; len 8 stays disclosed.
 7. (opus5, MEASURED) M_RELOAD -- DISCLOSED as unrowable (a race in the COUNT words under the signal-driven tick, or the
    end-span path where every reachable start byte is 0); `data[0]' stays the operand, with the end-span reason in the
    comment (fable5) -- Fable's "ticks run between instructions" premise REFUTED by reading timer.c (the SIGALRM handler
    calls the callbacks directly); grok's narrowing (COUNT words only, CEN off at init) adopted; codex's "twelve
    interiors" -> six.
 8. L4s corrected IN PLACE: "875 checks" -> the gate's own 857 (grok, Opus, codex); the headline and the detector heading
    "23 rows" (grok, Fable, Opus); the four pass-1 sentences the pass-2 section had corrected only in a later paragraph
    (codex); the unrecorded `latch sameoff 3' safe miss (Opus, codex); the CHANGELOG denominator list vs the probe's
    DISCLOSED list (Opus); SEATS.txt's "kimi MISSING" reconciled in the record (codex).
 9. (kimi, grok) the write-value and offset-class residuals filed as `pcc2dispall' at pass 3 -> WITHDRAWN as a filing:
    both are rows now.

REJECTED / NOT CREDITED
10. (grok, deepseek, minimax; fable5 GO-WITH-CHANGES) close on the 36-row instrument -- overtaken by six measured sweeps.
    Readings, recorded by name; not seat failures.
11. (fable5) R2 as stated -- the premise was wrong (timer.c), the second reason right and adopted.
12. (opus5) "eight of the twelve interiors are tick-written" -- six (the two COUNT words' interiors).
13. (glm) SEAT FAILURE, thinking burn x2 -- not agreement.

## THE TEN NEW ROWS (from the detector diff; the full diff is in the file-reading seats' brief)

```
+row("inword msg", t.count(MSG) if alive else "n/a", 12, "...twelve announces for twelve offsets; the SECOND write to 0x06 and the read-back are silent: the latch is per offset in THIS class too (Opus M_LATCHOFF)")
+row("inword rdawr", val(t, alive, how), "0x0", "...and 0x06 reads back 0x0 after two writes: DECLINED in this class too -- a member 6 scoped to the low offsets reads 0x5a (Opus M_BACKEDLOW)")
+row("unnamed msg", t.count(MSG) if alive else "n/a", 13, "...thirteen announces; the second write to 0x21 and its read-back are silent (per-offset latch, unnamed class)")
+row("unnamed rdawr", val(t, alive, how), "0x0", "...and 0x21 reads back 0x0: declined in the unnamed class too (a member 6 scoped by offset class reads 0x5a)")
+row("wr val text", t.count("0x30 (len 1): 0x5a -- declined") if alive else "n/a", 1, "...and the announced VALUE is the byte written: the mirror of `srvd val text' on the write arm -- `idata -> 0' printed 0x0 and passed 36 rows (Opus M_WRVAL0, MEASURED)")
+row("srvd val text", t.count("0x5 (len 1) -- served 0x34") if alive else "n/a", 1, "...and the announce prints THAT byte (data[0], what was served) WITH its width: `served 0x%02x' of 0 passed 23 rows (Opus M_O1, MEASURED); `(len 1)' -> `(len 4)' passed 36 (codex)")
+row("srvd half text", t.count("0x6 (len 2) -- served 0x56") if alive else "n/a", 1, "a len-2 default read at 0x06 is announced from its FIRST byte (0x56 of 0x5678): data[len-1] says 0x78 (Opus M_LASTBYTE, MEASURED 36/36); a len-2 re-kill dies here")
+row("half wr rdawr", (printed(t, "r6") if alive else fate(alive, how)), "0x5678", "...then st.h 0xaabb at 0x06 is DECLINED (silent: the bit is set) and ld.hu reads 0x5678 back: len-2 disposition; a byte-truncated backed store reads 0xbb78")
+row("srvd rd latch", (printed(t, "r8") if alive else fate(alive, how)), "0x34", "a SECOND read at 0x05 -- its bit set by the FIRST READ -- still receives 0x34: a latched-path read whose response is zeroed passes count rows (codex M_LATCH_RD_ZERO)")
+row("srvd wr latch", (printed(t, "r9") if alive else fate(alive, how)), "0x78", "st.b 0xbb at 0x07 (declined, announced) then ld.bu at 0x07 -- its bit set by a WRITE -- receives 0x78: the response is preserved on the latched path whichever direction set the bit")
+row("wide wr val", t.count("(len 4): 0x5a5a5a5a -- declined") if alive else "n/a", 1, "...and the announced value is the WHOLE word: printing data[0] instead of idata says 0x5a (Opus M_WRDATA0, MEASURED 36/36)")
```

## THE THREE QUESTIONS (closed where they can be)

**1. From table 4 and its predictions: does any mutant's measured score or red set differ from its prediction (yes/no,
which)?  Is any of the ten pass-3 mutants NOT 36/36 on the pass-3 instrument (yes/no, which)?**

**2. For each of the ten new rows, is its mirror cell (other arm / other setter direction / other width / other offset
class) rowed, disclosed, or neither?  List only the NEITHER cases.**

**3. Should #501 close and commit?  One line, with the denominator's exclusions.**
Anything you cannot settle from this packet: one line.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
