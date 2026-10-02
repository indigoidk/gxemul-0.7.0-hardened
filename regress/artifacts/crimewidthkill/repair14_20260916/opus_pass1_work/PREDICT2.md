# PREDICT2.md -- Opus pass-1 seat, table 2.  WRITTEN BEFORE THE TABLE-2 BUILDS.
# Table 1 is still in flight; these two mutants are chosen from the HANDLER, not from its result.

THE CLASS TABLE 2 TESTS -- and it is not the class repair 14 addresses.

  The 56-cell enumeration in P2 is the ACCEPT half of the space.  Every axis it names
  ({latch} x {len 4,8} x {R,W} x {7 labels}) describes an access that is SERVICED.  The
  DECLINE arm has its own product -- {len 1,2} x {R,W} x {7 labels} x {latch} -- and the
  enumeration contains none of it.  Part A (a pre-latch mirror of accept cells) and Part B
  (HARD_RESET at CONTROL) are both on the accept side, so neither can reach it.

  The decline arm's own repair is `goto crime_declined'.  Narrowing it by LABEL alone is
  ROWED (contract item 3: "the goto lost, or narrowed by width, direction, or ADDRESS" --
  `time lb/sb/lh/sh' are the TIME rows).  But every one of those rows drives its refusal as
  the SESSION'S FIRST, so it is measured with the latch CLEAR at the moment of the test.
  Conjoin the label narrowing with the latch and the rows go blind -- the exact mirror of
  the accept-side K-class, one arm over.

M4_timeplain    KILLED.  `goto crime_declined;' -> `if (relative_addr != CRIME_TIME)
                goto crime_declined;'.  A narrow access at CRIME_TIME falls into the switch
                and reaches crime_update_crime_time(), in EVERY latch state.
                I expect `time lb', `time sb', `time lh' and `time sh' to red.
                THIS IS THE DISCRIMINATING CONTROL.  Without it an escape by M3 proves
                nothing, because it could mean the TIME channel is unobservable rather than
                unobserved in one state.

M3_timelatch    188/188 ESCAPE.  The same narrowing, plus the goto moved inside the latch
                block so the SESSION'S FIRST refusal still declines correctly:
                    if (!(d->warned & CRIME_W_LEN)) { latch; fatal; goto crime_declined; }
                    if (relative_addr != CRIME_TIME) goto crime_declined;
                Effect: a narrow access at CRIME_TIME that is NOT its session's first refusal
                falls into the switch and advances the clock, SILENTLY.
                WHY I EXPECT AN ESCAPE, derived from the session map (mirror14.py, sentinel
                MIRROR14_DONE) rather than guessed:
                  * sessions 21-24 (`time lb/sb/lh/sh') each refuse at +0x38 FIRST, so under
                    M3 they decline correctly and stay green;
                  * session 39 (`free time said') refuses once;
                  * the only sessions refusing at +0x38 with the latch ALREADY SET are
                    session 40 (`latch x5' -- tail `lb +0x00', `lb +0x38' after five
                    refusals) and session 30 (dog-first).  `latch x5' carries an announce
                    count, a RAM round trip and an announce text; none reads TIME.  Session
                    30's TIME rows (`time sd lb v0', `time sd lh v0') are ANSWER rows, and
                    the answer is still 0 because the decline arm never assigns `odata'.
                GUEST-VISIBLE: the fix's own comment names this as one of the four defects
                the goto exists to prevent -- "one at CRIME_TIME advance the clock".

IF M3 ESCAPES AND M4 IS KILLED, the pair is the answer to Q2: a two-line edit, on an axis
repair 14 as proposed does not touch, whose single-axis form is already rowed.
