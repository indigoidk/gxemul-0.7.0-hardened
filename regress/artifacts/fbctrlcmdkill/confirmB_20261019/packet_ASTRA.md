# Commit B confirm -- #567 (fbctrlcmdkill), the unit as it will be committed

Open your answer with the token ASTRA_FBCMD_CF_20261019, then ONE line: VERDICT: COMMIT | COMMIT WITH CHANGES | DO NOT COMMIT -- <one line>.

READ-ONLY.  A records and correctness CONFIRM before a local commit: does the unit say only what is true, change only what it should, and carry out the owner's 2026-10-19 ruling on pass 3 ('land with filed debt': add only the two R:edges rows the probe already collects, commit, and file pass 3's remaining observation cells as coverage debt)?  Name any wrong number, any claim no artifact supports, any line that does not belong, and anything missing.  The tree is C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC (its working tree); ignore every other src/.

## 1. The commit message (verbatim)
```
#567 (fbctrlcmdkill): dev_fbctrl.c refuses every command but 0-2 before the store -- COMMAND kept, one announce per device; a 125-row detector in gate 16; held for Fable

A DATA write at COMMAND of any value but NOP (0), SET_RESOLUTION (1) and GET_RESOLUTION (2) reached
fbctrl_command()'s default: and ended the emulator -- FILL and COPY included -- and a wide sd was
stored into the int cell as its low word and run.  Witness on an unmodified -E testmips with HEAD's
binary: 2/12; the fix 12/12.

* src/devices/dev_fbctrl.c: the DATA arm refuses, before the store, any COMMAND value above
  GET_RESOLUTION compared on all 64 bits; COMMAND keeps its value, nothing runs, and a new
  warned_cmd latch prints one "(once)" announce per device.  default: stays as a tripwire.
* regress/fbctrl_cmd_probe.py (new): 125 rows, 27 sessions; its header is the contract, with
  NOT CLAIMED (0)-(7).
* regress/gate_mips_folds.sh: the probe's block in gate 16 -- parse, CONTROL=OK, exit 0, the
  score pinned at 125 by equality, every row checked by name.  Run in situ: PASS on the fix
  (161 checks), FAIL on HEAD's build (77 of 161, all in this block).
* regress/gate_hygiene.sh: EXPECT_PTY_PROBES 75 -> 76, EXPECT_CONVERTED 25 -> 26 for this probe.
* tools/precommit_check.sh: SCORE_CLAIMS_MANIFEST 35 -> 36.
* check_probe_wiring.py: the probe's MANIFEST line and its frozen v1 copy's.
* ledger: fbctrlcmdkill HELD for fable5; FILED fbctrlobsgrid (MED), fbctrlvec128 (LOW),
  gate16fence (LOW); gatedevicesplit records gate 16's stop.  CHANGELOG, OUTSTANDING_BUGS,
  matrix and fable queue follow.

Measured (regress/artifacts/fbctrlcmdkill/), each table's predictions written before it ran: kill
table 4 found all 44 mutants red on the 123-row v4; the 125-row probe scores 125/125 on the fix,
51/125 on HEAD's build and 17/125 with CONTROL=FAILED on two null media.  Passes 1, 2, F2 and 3 by GPT-6 Astra, Grok
4.7 and GLM 5.3; pass 3's observation cells filed by the owner's ruling ("land with filed debt").
Fable 5.1 walled on every pass (held).  Confirm (GPT-6 Astra): requested on this unit.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## 2. The code and gate diffs against HEAD 3e7b1f4e
```diff
diff --git a/regress/gate_hygiene.sh b/regress/gate_hygiene.sh
index e3992ecf..f71ba52e 100644
--- a/regress/gate_hygiene.sh
+++ b/regress/gate_hygiene.sh
@@ -385,7 +385,7 @@ check "readiness: no unrecognised endswith spelling" "$unknown" "$EXPECT_UNKNOWN
 #  and reds THREE rows -- this one, the promptless count and the promptless-names row -- because all three are
 #  grandfathered names that exist only in the working tree (measured on a copy with them removed: 70/73, 40/43,
 #  names gone=the three).  Written by `tools/derive_hygiene_pins.sh --write`, never by hand. ***
-EXPECT_PTY_PROBES=75
+EXPECT_PTY_PROBES=76
 #  *** AND THE SAME PROBE BROKE A SECOND CENSUS IN THIS FILE, WHICH pass 11's OWN
 #  REPAIR DID NOT FIX.  Found by the codex seat reviewing that repair. ***
 #
@@ -604,7 +604,7 @@ fi
 #  send() spelled the fresh mark `mark=mark`, which the fresh-mark census does not read, so that one said
 #  23 and the three #392 counts DISAGREED at HEAD.  The probe's rename to `_mark` (same change) makes the
 #  three agree; the deriver refuses to write while they disagree, which is why the rename precedes the pin. ***
-EXPECT_CONVERTED=25
+EXPECT_CONVERTED=26
 #  One helper for all three, so they agree on WHAT they look at.  The first draft
 #  used py_code() for the anchored count and a raw grep for the other two, which
 #  meant a comment mentioning the echo guard would have inflated one count and not
diff --git a/src/devices/dev_fbctrl.c b/src/devices/dev_fbctrl.c
index eab10df8..2013d66e 100644
--- a/src/devices/dev_fbctrl.c
+++ b/src/devices/dev_fbctrl.c
@@ -50,6 +50,7 @@ struct fbctrl_data {
 	int		current_port;
 	int		port[DEV_FBCTRL_NPORTS];
 	int		warned_port;	/* #549: the refused-selector announce */
+	int		warned_cmd;	/* #567: the refused-command announce */
 };
 
 
@@ -98,6 +99,9 @@ static void fbctrl_command(struct cpu *cpu, struct fbctrl_data *d)
 
 	/*  TODO: Block copy and fill.  */
 
+	/*  #567: unreachable while the DATA arm refuses every command
+	    other than these three; kept as a tripwire for a later edit
+	    that lets one in, as #549 kept the selector's.  */
 	default:fatal("fbctrl_command: Unimplemented command %i.\n", cmd);
 		exit(1);
 	}
@@ -146,7 +150,24 @@ DEVICE_ACCESS(fbctrl)
 
 		if (writeflag == MEM_READ)
 			odata = d->port[d->current_port];
-		else {
+		else if (d->current_port == DEV_FBCTRL_PORT_COMMAND &&
+		    idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION) {
+			/*  #567: a command other than NOP, SET_RESOLUTION and
+			    GET_RESOLUTION is REFUSED before it is stored: COMMAND
+			    keeps its previous value and nothing executes.  It used
+			    to reach fbctrl_command()'s default: and end the
+			    emulator, FILL (3) and COPY (4) included -- the header
+			    names them under a TODO and gives them no ports.  The
+			    compare is on all 64 bits: the cell is an int, so a
+			    wide 0x100000001 used to be stored as 1 and run
+			    SET_RESOLUTION.  Announced once per device.  */
+			if (!d->warned_cmd) {
+				fatal("[ fbctrl: command 0x%llx is not supported; "
+				    "the command port is unchanged (once) ]\n",
+				    (unsigned long long) idata);
+				d->warned_cmd = 1;
+			}
+		} else {
 			d->port[d->current_port] = idata;
 			if (d->current_port == DEV_FBCTRL_PORT_COMMAND)
 				fbctrl_command(cpu, d);
diff --git a/tools/precommit_check.sh b/tools/precommit_check.sh
index c157ab43..f6aaaade 100644
--- a/tools/precommit_check.sh
+++ b/tools/precommit_check.sh
@@ -353,7 +353,10 @@ elif out=$(python "$SCORECHK" 2>&1); then
 	#  the stem, and only a docstring at regress/<stem>_probe.py or regress/<stem>.py; no comment line
 	#  names ip30_abort and the probe lives under artifacts/, so for this pin it checks no prose -- only
 	#  the pin is counted.
-	SCORE_CLAIMS_MANIFEST=35
+	#  RAISED 35 -> 36 ON 2026-10-18, DELIBERATELY.  One newly gated probe: fbctrl_cmd_probe.py
+	#  (#567, pinned UNQUOTED in gate_mips_folds.sh at its final 125 rows; 95 when this line was
+	#  first written, before the review passes grew it).
+	SCORE_CLAIMS_MANIFEST=36
 	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
 	if [ -z "$_spinned" ]; then
 		bad "check_score_claims printed no SCORE_CLAIMS_PINNED line -- the count cannot be pinned"
--- /dev/fd/63	2026-10-19 08:26:44.000000000 -0500
+++ /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd/commitB/cpw_commit.py	2026-10-19 08:24:24.831443100 -0500
@@ -2849,6 +2849,9 @@
     "sh4_bsc_width_probe.py":      (CLASS_DETECTOR, "#441 BCR2/BCR3 non-16-bit access"),
     "fbpending_drain_probe.py":    (CLASS_DETECTOR, "#442 footbridge pending-tick backlog"),
     "fbctrl_port_probe.py":        (CLASS_DETECTOR, "#549 fbctrl PORT selector refusal"),
+    "fbctrl_cmd_probe.py":         (CLASS_DETECTOR, "#567 fbctrl COMMAND refusal"),
+    "artifacts/fbctrlcmdkill/pass2_20261018/legs/probe.frozen.py":
+        (CLASS_RESEARCH, "#567 the shipped probe's v1 copy run for its in-tree legs, preserved as evidence"),
     "artifacts/fbctrlportkill_20260924/opus549_measured/c3/gen_c3.py":
         (CLASS_RESEARCH, "#549 the Opus measuring seat: the verifying pass's floor-edit generator (edits of the final dev_fbctrl.c not in table 5), preserved as evidence"),
     "artifacts/fbctrlportkill_20260924/opus549_measured/c3/gen_mask.py":
```

## 3. Gate 16's #567 block as committed (regress/gate_mips_folds.sh)
```sh
#  ---------------------------------------------------------------------------------------
#  #567 fbctrlcmdkill: the same device's COMMAND port.  Before #567 a DATA write at COMMAND of any
#  command but NOP (0), SET_RESOLUTION (1) and GET_RESOLUTION (2) -- FILL and COPY among them --
#  reached fbctrl_command()'s default: and ended the emulator, and a wide value was stored into the
#  int cell as its low word, so 0x100000001 ran SET_RESOLUTION.  #567 refuses every other 64-bit
#  value before the store (COMMAND keeps its value, nothing runs) and announces once per device.
#  regress/fbctrl_cmd_probe.py drives real guest sb/sh/sw/sd and lb/lh/lw/ld on an unmodified
#  testmips, like the #549 probe above, so it too runs before the pmax-kernel check.  THE CONTRACT is
#  its header: it holds the bound's edges and the latch at every access WIDTH (the class two review
#  passes found open), and its NOT CLAIMED (7) names the width x latch cells pass 3 found reached but
#  not observed (filed as `fbctrlobsgrid`).  Kill table 4 (regress/artifacts/fbctrlcmdkill/
#  killtable4_20261019/) re-ran all 44 mutants built for this round on v4's 123 rows -- every one
#  red, the twelve built last having escaped the 106-row v3.  Pass 3 added two rows (`edge x1',
#  `edge y1'); the 125 rows score 125 on the fix, 51 on HEAD's build, and 17 on a binary that runs
#  nothing -- absence rows read green there and the record still parses, so this block requires CONTROL=OK, pins the
#  score by EQUALITY, and checks EVERY row by name (pass 2: a row swapped for an unrelated unique
#  green one keeps every count).
#  `gatedevicesplit` (#498) grows by this second device probe in a CPU gate.  That is debt, not a
#  fit: pass 2 asked that it not be called fine (Grok 4.7), and the STOP is recorded on that row --
#  a third device probe lands here only with the split or with a pin on this gate's launch count
#  (GLM 5.3).  Like #549's, the launch below has no timeout: a wedged probe hangs the gate, which is
#  visible and not a false pass (filed for both blocks as `gate16fence`).
#  The probe prints a row's status AFTER got/want, unlike the #549 probe, so every row count below
#  uses one anchored pattern, FCROW.  The v4 block (123 names), replayed on kill table 4's 48 logs,
#  was green only on the fix (wiring_20261019/GATE16_REPLAY_v4.out); this one adds the two names and
#  moves the pins, and was run in situ on both builds (wiring_20261019/INSITU.md).
FCLOG=$LOGDIR/fbctrl_cmd_probe.log
FCROW='^  [^ ].* got=[^ ]* +want=[^ ]* +'
FCNAMES=("live" "devsig" "ref 3 alive" "ref 3 cmd" "ref 3 x1" "ref 3 y1" "ref 3 once" "ref 3 noset"
         "ref 4 alive" "ref 4 cmd" "ref 4 x1" "ref 4 y1" "ref 4 once" "ref 4 noset" "ref sb3 alive"
         "ref sb3 cmd" "ref sb3 x1" "ref sb3 y1" "ref sb3 once" "ref sb3 noset" "ref sh4 alive" "ref sh4 cmd"
         "ref sh4 x1" "ref sh4 y1" "ref sh4 once" "ref sh4 noset" "ref 5 alive" "ref 5 cmd" "ref 5 x1"
         "ref 5 y1" "ref 5 once" "ref 5 noset" "ref m1w alive" "ref m1w cmd" "ref m1w x1" "ref m1w y1"
         "ref m1w once" "ref m1w noset" "ref w3 alive" "ref w3 cmd" "ref w3 x1" "ref w3 y1" "ref w3 once"
         "ref w3 noset" "ref w0 alive" "ref w0 cmd" "ref w0 x1" "ref w0 y1" "ref w0 once" "ref w0 noset"
         "ref w1 alive" "ref w1 cmd" "ref w1 x1" "ref w1 y1" "ref w1 once" "ref w1 noset" "ref w2 alive"
         "ref w2 cmd" "ref w2 x1" "ref w2 y1" "ref w2 once" "ref w2 noset" "ref m1d alive" "ref m1d cmd"
         "ref m1d x1" "ref m1d y1" "ref m1d once" "ref m1d noset" "edge alive" "edge cmd" "edge once"
         "edge x1" "edge y1" "acc nop cmd" "acc nop x1" "acc nop quiet" "acc set cmd" "acc set ran"
         "acc set res" "acc set quiet" "acc get cmd" "acc get x1" "acc get y1" "acc get quiet" "acc sd get x1"
         "acc sh get x1" "acc edges cmd" "acc edges quiet" "latch get x1" "latch nop cmd" "latch set cmd"
         "latch set ran" "latch once" "rdcmd val" "rdcmd again" "rdcmd noexec" "rdx1 again" "x2 three"
         "x2 quiet" "x2 sb" "x2 sh" "x2 sd" "m3 quiet" "rdw lb" "rdw lh" "rdw ld" "rdw lw" "rdw x1" "two once"
         "two cmd" "wl alive" "wl once" "wl sb get x1" "wl sh get x1" "wl sd get x1" "wl cmd" "wb once"
         "wb cmd" "p1 port" "p1 cmd" "p2 cmd" "p2 port" "free alive" "free once" "sessions clean")
fcrc=0
python3 -u fbctrl_cmd_probe.py "$PMAX" > "$FCLOG" 2>&1 || fcrc=$?
if [ "$(grep -cx 'FBCMD_DONE' "$FCLOG")" != "1" ] ||
   [ "$(grep -c '^FBCMD_RESULT=' "$FCLOG")" != "1" ] ||
   ! grep -Eq '^FBCMD_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$FCLOG" ||
   [ "$(grep -c '^FBCMD_CONTROL=' "$FCLOG")" != "1" ] ||
   ! grep -Eq '^FBCMD_CONTROL=(OK|FAILED)$' "$FCLOG"; then
    note "fbctrl command probe produced no unique, complete record; last lines follow"
    tail -5 "$FCLOG" | sed 's/^/       /'
    check "fbctrl command probe output parses" "no" "yes"
else
    check "fbctrl command probe output parses" "yes" "yes"
    grep -E "${FCROW}FAIL  " "$FCLOG" | sed 's/^/       /'
    check "fbctrl command probe controls" "$(sed -n 's/^FBCMD_CONTROL=//p' "$FCLOG")" "OK"
    #  As for #549: the probe exits nonzero on a crash OR a red row, a second catcher of a red score.
    check "fbctrl command probe exit 0 (nonzero: a crash or a red row)" "$fcrc" "0"
    fcres=$(sed -n 's/^FBCMD_RESULT=//p' "$FCLOG")
    #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin (as #549's).
    check "fbctrl_cmd rows run" "${fcres#*/}" 125
    check "fbctrl_cmd rows correct" "${fcres%/*}" "125"
    check "fbctrl_cmd rows failed" "$(grep -cE "${FCROW}FAIL  " "$FCLOG")" "0"
    #  Reconcile the rows printed with the trailer, and require each row name once (#549 F2).
    check "fbctrl_cmd rows emitted match the trailer total" \
          "$(grep -cE "${FCROW}(ok|FAIL)  " "$FCLOG")" "${fcres#*/}"
    check "fbctrl_cmd ok rows match the trailer count" \
          "$(grep -cE "${FCROW}ok  " "$FCLOG")" "${fcres%/*}"
    check "fbctrl_cmd row names are unique" \
          "$(grep -E "${FCROW}(ok|FAIL)  " "$FCLOG" | sed -E 's/^  (.*[^ ]) +got=.*/\1/' |
             sort | uniq -d | wc -l)" "0"
    #  And EVERY expected row by NAME, green exactly once: counts and uniqueness cannot tell an expected
    #  row from an unrelated unique one put in its place (pass 2, GPT-6 Astra).
    check "fbctrl_cmd named rows" "${#FCNAMES[@]}" 125
    for v in "${FCNAMES[@]}"; do
        check "  fbctrl_cmd row: $v" "$(grep -cE "^  ${v} +got=[^ ]* +want=[^ ]* +ok  " "$FCLOG")" "1"
    done
fi

```

## 4. The new probe's header -- its CONTRACT (regress/fbctrl_cmd_probe.py, docstring only; the code is in the file)
```
#567 fbctrlcmdkill -- the DETECTOR for dev_fbctrl.c's command port, on an UNMODIFIED `-E testmips`.

machine_test.c installs `fbctrl addr=0x12f00000` in testmips's own setup.  t0 = 0xffffffffb2f00000, kseg1 of
DEV_FBCTRL_ADDRESS; PORT is +0x00, DATA +0x10.  Port 0 is COMMAND; a DATA write there executes the command.  Pre-#567
any command other than NOP (0), SET_RESOLUTION (1) and GET_RESOLUTION (2) reached fbctrl_command()'s default: and
ended the emulator, and a WIDE value was stored truncated into the int cell and dispatched as its low word.  #567
refuses every 64-bit value other than 0, 1 and 2 in the DATA arm BEFORE the store: COMMAND keeps its value, nothing
executes, and one announce per device names the full value -- `[ fbctrl: command 0x... is not supported; the command
port is unchanged (once) ]`.

SESSIONS (each on a fresh emulator, every word stepped and compared with the emulator's own step line, unless F):
  C    controls: PORT=5, DATA=0x2a, read back (LIVENESS); PORT=1, DATA=123, PORT=0, DATA=2 (GET_RESOLUTION, headless:
       zeroes X1/Y1), PORT=1, read (DEVICE-SIGNATURE: 0 where RAM would keep 123).
  R:v  one REFUSAL per class, on a device seeded with COMMAND = 2 (by a GET), X1 = 123, Y1 = 77: PORT=0, DATA=v, then
       read COMMAND, X1, Y1; no SET's resolution-change line may print.  Classes: 3, 4, 5 and 0xffffffff by sw; 3 by sb and 4 by sh (the gate never tests len,
       so `&& len >= 4' would let a byte or halfword command through --
       regress/artifacts/fbctrlcmdkill/draft_20261018/PRETABLE.out, section 1); 0x100000003, 0x100000000, 0x100000001,
       0x100000002 and 0xffffffffffffffff by sd.  The wide aliases of ACCEPTED commands are the width pin: a compare on
       the stored int would run NOP (COMMAND reads 0), SET_RESOLUTION (COMMAND reads 1) or GET_RESOLUTION (X1/Y1 read 0).
  A:edges  ACCEPT GET_RESOLUTION -- the at-bound 2 -- by sd and by sh: each dispatch zeroes X1 (123 -> 0), so dispatch
       at both widths is observable; COMMAND reads 2, no announce.
  R:edges  REFUSE 3 -- past the bound -- by sh, then by sd, on the seeded device: alive, COMMAND keeps 2, one announce,
       and X1 and Y1 keep 123 and 77 -- the second refusal is made with the latch SET while a GET sits in COMMAND.
  A:n  ACCEPT, latch clear, one width each: NOP by sd after COMMAND 2 (COMMAND reads 0, X1 keeps 123); SET_RESOLUTION by sh with X1 = Y1 = 0
       (dev_fb_resize() prints `size too small (0 x 0); ignored.` -- a fatal() that returns; COMMAND reads 1; and the resolution-change debug() line
       prints -- the noset rows' channel, shown live); GET_RESOLUTION by sb after X1 = 123, Y1 = 77 (both read 0; COMMAND reads 2).  No command announce in any of them.
  L    ACCEPT with the latch SET: refuse 3 first, then GET (X1 123 -> 0), NOP (COMMAND 0), SET at 0 x 0 (the resize line
       once, COMMAND 1) -- one command announce in the whole session.
  M1   a READ of COMMAND does not execute it: COMMAND = 2 by a GET, X1 = 123, PORT=0, read DATA twice (2, 2), PORT=1,
       read X1 twice (123, 123): a re-executed GET would zero X1, and a read that STORED would zero the second read.
  M2   a DATA write of 3 to a NON-COMMAND port (PORT=3, X2) is ordinary storage: reads back 3, no announce.
  M3   WIDTH at a non-COMMAND port and on the read path: 3, 4 and 5 stored at X2 by sb, sh and sd (each reads
       back; no announce); then COMMAND = 2 by a GET, X1 = 123, and COMMAND read by lb, lh, ld and lw -- 2 each,
       so no read stored anything -- and X1 still 123, so no read ran the GET.
  T2   refuse 3; ACCEPT a NOP; READ COMMAND; refuse 5; refuse sd 0x100000005 -- the latch persists across the accept
       and the read: ONE command announce, naming 0x3; COMMAND reads 0.
  W:latch  WIDTH x LATCH at the bound's edges: sd 3 with the latch CLEAR (refused and announced -- an sd refusal
       sets the latch), then sb, sh and sw 3 with it SET (refused, silent), then GET by sb, sh and sd with it SET
       (each zeroes X1 again; COMMAND reads 2).
  W:sb  the latch SET by a byte refusal: sb 3 (announced), then sh 4 (silent); COMMAND keeps 0.
  P1   selector refused first (PORT=9, #549's announce), then command 4 refused: one announce of each kind.
  P2   the reverse order: command 4, then selector 9: one of each.
  F    FREE-RUNNING: PORT=0, DATA=3, then continue to a breakpoint -- the announce must print: under free-running
       debug() returns at default verbosity while fatal() prints, so this is the one row that sees a demotion.
Every refusal row rests on `fatal()` printing and RETURNING (src/core/debugmsg.c's fatal(): no early-out, no exit).

CONTRACT (clause e) -- AN ENUMERATION.
THE FLOOR.  The fixed DATA arm's refusal branch tests the access direction, the port (`current_port == COMMAND`), the
written value (`idata > DEV_FBCTRL_COMMAND_GET_RESOLUTION`, on all 64 bits memory_readmax64() builds) and the latch
(`!warned_cmd`); the accept branch stores the value and, at COMMAND, dispatches it.  Every cell of those is held:
  the value  at the bound, 2 (A:get, A:edges, W:latch, every seed); below it, 1 (A:set) and 0 (A:nop); past it, 3
             (R:3, R:sb3, R:edges, W:latch, W:sb, L, T2, F -- rule D2's B+1 edge), 4 (R:4, R:sh4, W:sb, P1, P2), 5
             (R:5, T2), 0xffffffff (R:m1w) and all-ones (R:m1d)
  the port   COMMAND (every R, A and W session, L, T2, P1, P2, F) and not COMMAND (M2 and M3: 3, 4 and 5 at X2 are data)
  the latch  clear (the first refusal of every R and W session, L, T2, P1, P2, F) and set -- then crossed with a later
             refusal (R:edges, W:latch, W:sb, T2), a wide refusal (T2's sd 0x100000005), and an accept and a read that
             a later refusal follows (T2: an sw NOP and an lw read) -- so its PERSISTENCE is observed at sw and lw only
             (NOT CLAIMED (7)); the selector's latch apart from it, in both orders (P1, P2)
  direction  a write (all) and a read (M1: COMMAND and X1 each read twice; M3: COMMAND by lb, lh, ld and lw) -- a read
             returns the cell, runs nothing and stores nothing.  "Stores nothing" is pinned at COMMAND and X1; Y1 is
             read once per session
WIDTH -- the class two consecutive passes found open (pass 2's E13; F2's E15-E19).  The arm never tests len --
memory_readmax64() consumes it to build idata -- so a cell held at one width only leaves the others unchecked.  HELD AT
EVERY WIDTH, as enumerated before it was measured (regress/artifacts/fbctrlcmdkill/killtable4_20261019/
PRETABLE_ADDENDUM_t4.out) and listed below.  Pass 3 (GPT-6 Astra, GLM 5.3) showed that enumeration counts cells REACHED,
not every effect OBSERVED there; the cells it named are NOT CLAIMED (7):
  edge x latch   accept 2, latch clear: sb A:get, sh A:edges, sw C and the seeds, sd A:edges
                 accept 2, latch set:   sb, sh and sd W:latch, sw L
                 refuse 3, latch clear: sb R:sb3 and W:sb, sh R:edges, sw R:3, L, T2 and F, sd W:latch
                 refuse 3, latch set:   sb, sh and sw W:latch, sd R:edges (silent and run nothing; that the sb
                                        refusal STORES nothing is not observed -- NOT CLAIMED (7))
  the latch SET by a refusal at sb (W:sb), sh (R:edges), sw (T2) and sd (W:latch), each seen by a later refusal staying
                 silent; TESTED -- a refusal with it set stays silent -- at sb (W:latch), sh (W:latch, W:sb), sw (T2's
                 5, W:latch) and sd (R:edges, T2)
  an accept is dispatched -- GET zeroes X1 -- at every width (sb A:get, W:latch; sh A:edges, W:latch; sw C, L; sd
                 A:edges, W:latch) and stored at every width (sb A:get, sh A:set, sw L, sd A:nop)
  a non-COMMAND store at every width with the latch clear (sb, sh and sd M3; sw M2 and every seed); a read of
                 COMMAND at every width with the latch clear (lb, lh and ld M3; lw M1 and M3) -- non-COMMAND cells are
                 read by lw only
  wide values exist only at sd -- the width pin: the four whose low word is 0..3 (R:w0..R:w3) are refused, where a
                 compare on the low word would run NOP, SET or GET
EFFECTS, each held by the sessions named:
  a refused command keeps COMMAND's previous value -- 2 (every R class, R:edges), 0 (T2, W:sb)
  a refused command executes nothing -- no GET (X1 and Y1 kept, with a GET in COMMAND: every R class, and R:edges,
      whose second refusal is made with the latch set) and no SET (no
      resolution-change line: every R class's `noset' row; A:set's `acc set res' shows that channel live).  That line
      is a debug() which prints while STEPPING, so `noset' is a claim about stepped sessions; F free-runs and is not
      read for it.  A NOP has no observable effect and is not claimed to run.
  the first refusal announces once, naming the full value -- every R class; R:edges, W:latch and W:sb, whose later
      refusals stay silent; T2 (0x3, then 5 and a wide value silent across a NOP and a read); P1 and P2 (beside #549's
      selector announce); F (free-running: fatal() prints where debug() would not)
  an accepted command is stored -- read back at a value distinguishable from the one before it by A:get, A:set, A:nop
      and L (A:edges and W:latch read COMMAND once after several accepts) -- and GET_RESOLUTION is seen to RUN (X1 zeroed) at every
      width, with the latch clear (A:get, A:edges, C) and set (L, W:latch); SET_RESOLUTION is seen to run by sh (A:set)
      and sw (L: the resize line); a NOP is stored (A:nop by sd, L by sw) and not claimed to run
  every session survives and exits 0 -- `sessions clean', pinned to the literal 27
Measured (regress/artifacts/fbctrlcmdkill/): kill table 4 re-ran every mutant built -- 44 -- on v4, this probe less
pass 3's two `edge' rows, and every one is red (killtable4_20261019/): the gate removed (the pre-#567 arm, HEAD's own score), the compare
narrowed to 32 bits, to `int' or made signed, its bound moved down by one, two and three or up by one, its operand
swapped for the resident cell, the gate qualified by width (byte and halfword escaping, or every non-word access
refused), the latch shared, never set, set by an accept, or bypassed for wide values once set, the announce demoted to
debug() or its argument truncated, the refused value stored, the port test dropped, a NOP or a SET refused alone, the
dispatch hoisted out of the store branch, made unconditional on the port, or added to the read path, the read path
falling into the store branch; and, at one width, the dispatch skipped or the bound moved down or up (E15-E19), the
latch cleared by an accept or a read (E20, E21), the bound relaxed in one (width, latch) cell or GET refused at three
widths once the latch is set (E22-E26), the latch set or tested at only some widths (E27-E29), the port test bypassed
for non-word stores (E30), and a read running the command (ld), storing after it returns (lb) or returning nothing
(lb) (E31-E33).  The twelve E22-E33 were measured in the same table on the 106-row v3, and every one escaped it whole.
Earlier tables measured the rest on v1 (95 rows: tables 1, 1b, 2a), v2 (99: 2, 3a) and v3 (106: 3): v1 let three
escape, v2 seven and v3 twelve -- the reason v4 had 123 rows.  Pass 3 added `edge x1' and `edge y1', grading values
R:edges already read, and changed no other row: this probe scores 125/125 on the fix, 51/125 on HEAD's build and 17/125
with CONTROL=FAILED on both null media (killtable4_20261019/legs41/).  The measured check that those two rows catch
the case pass 3 described is owed, with the rest of its cells (NOT CLAIMED (7)).
On a dead binary 17 rows read green -- the eleven `noset' rows and six announce counts, which read 0 on a session that
never started; `acc set res' and `sessions clean' are among the red -- so gate 16 requires FBCMD_CONTROL=OK, pins the
score by equality and checks every row by name (kill table 4's null media).
NOT CLAIMED (disclosed).  (0) The latch SET crossed with a wide ALIAS of an accepted command (w0-w2): T2's third
refusal is a wide non-alias (0x100000005), which pins the latch-set x wide cell; an edit exempting only the aliases of
0-2 once the latch is set is a value carve-out, (2) -- E14's measured closure does not reach it.  (1) A refusal that
STORES a value aliasing the previous COMMAND: w2 truncates to 2 and its `cmd' row cannot vary; ten classes, T2 and W:sb
pin the store (D8).  (2) Values and bits not listed: the compare is relational, so its generating set is its regions,
held at their edges; single-bit coverage like #549's session B is not claimed, and an edit refusing every listed value
but exempting one unlisted (`&& idata != 6'), or a listed value at a width no row writes it at (4 by sb), passes --
only a compare reshaped into an enumeration of the accepted values would close that family.  (3) A second fbctrl instance (#549's fbctrltwoinst,
filed): warned_cmd is per device and the probe drives one.  (4) The device's other offsets (fbctrloffkill, filed).  (5)
fbctrl_command()'s default:, kept as a tripwire: unreachable while the arm refuses, so no row reaches it on the fixed
device; likewise the DATA arm's own selector-range check (#549's tripwire), unreachable while the PORT arm refuses.  (6) A 16-BYTE store: testppc (default_test() installs this device) issues stvx/stvxl, which reach this arm
with len 16; the callback receives all 16 bytes, but memory_readmax64() builds idata from the low 64, so the prefix is
dropped before the compare and a 128-bit value whose low half is 0, 1 or 2 is accepted and runs (a low half of 1 runs
SET_RESOLUTION) -- this round's width defect one width out.  This MIPS probe cannot issue one; filed with #549's PORT
arm, which shares it, as fbctrlvec128.  (7) The width x latch OBSERVATION cells pass 3 named (GPT-6 Astra, GLM 5.3,
Grok 4.7): the latch's persistence after a non-word accept, a non-word read or a non-COMMAND store, each followed by a
refusal; a read with the latch set at lb, lh and ld; a non-COMMAND read at lb, lh and ld; a non-COMMAND store with the
latch set at sb, sh and sd; COMMAND read after a byte refusal made with the latch already set; and other refusal and
accept effects that a later write overwrites before any row reads them.  Filed as coverage debt, fbctrlobsgrid.
FILL (3) and COPY (4) are refused because nothing implements them (the header lists them under a TODO); a round that
implements one moves its rows from the refusal list to the accept list.

Output: one row per check, then FBCMD_CONTROL=OK|FAILED, FBCMD_RESULT=n/t, FBCMD_DONE.  The exit status is 0 only when
the controls are OK and every row is green.
usage: fbctrl_cmd_probe.py <gxemul-binary>
```

## 5. The CHANGELOG block (verbatim)
```
# `#567` (fbctrlcmdkill): the test machines' framebuffer controller ended the emulator on any command but NOP, SET_RESOLUTION and GET_RESOLUTION, and ran a WIDE value as its low word -- every other 64-bit value at COMMAND is refused before the store now, COMMAND kept, one announce per device; with a 125-row rung-3 detector, gated in gate 16; held for Fable

**The defect** (filed by `#549`'s review, `fbctrlcmdkill`, HIGH).  `fbctrl_command()`'s `default:` called `fatal()`
then `exit(1)` for every command other than NOP (0), SET_RESOLUTION (1) and GET_RESOLUTION (2) -- FILL (3) and COPY (4)
included, which `dev_fb.h` names under a bare `TODO:` with no port semantics.  A guest reaches it with ONE DATA write
while COMMAND (port 0, the power-on selector) is selected, on every test machine (`machine_test.c` installs
`fbctrl addr=0x12f00000`).  And `d->port[]` is `int`, so a wide `sd` was stored as its low word and DISPATCHED:
`0x100000003` ended the emulator as FILL, and `0x100000001` silently ran SET_RESOLUTION.  Witness, rung 3 on an
unmodified `-E testmips` with HEAD's binary: 2/12 -- 3, 4, 5, -1 and `sd 0x100000003` each exit 1
(`regress/artifacts/fbctrlcmdkill/pass1_20261018/WITNESS_headbin.out`); 12/12 on the fix.

**What ships.**
* `src/devices/dev_fbctrl.c` -- the DATA arm refuses, BEFORE the store, any write at COMMAND whose full 64-bit value is
  above GET_RESOLUTION: COMMAND keeps its previous value, nothing executes, and a new `warned_cmd` latch prints one
  `[ fbctrl: command 0x... is not supported; the command port is unchanged (once) ]` per device.  `fbctrl_command()`'s
  `default:` stays, unreachable, as a tripwire (as `#549` kept the selector's).  `est/` byte-identical; `build/`,
  `build-asan/` and `/tmp/gxsec-build` rebuilt and cleared both parts.
* `regress/fbctrl_cmd_probe.py` (new, 125 rows, 27 sessions on an unmodified `-E testmips`) -- eleven refusal classes
  (3, 4, 5 and `0xffffffff` by `sw`; 3 by `sb`, 4 by `sh`; `0x100000003`, the three wide aliases of accepted commands
  and all-ones by `sd`) on a device seeded with COMMAND = 2, X1 = 123, Y1 = 77; the bound's two edges -- 2 accepted with
  an observable dispatch, 3 refused -- at every access width, with the latch clear and set; reads and non-COMMAND stores
  at every width; the latch across an accept and a read; the selector's latch apart from it in both orders; one
  free-running session for the announce level.  Its CONTRACT is its header -- the floor, the width cells held, the
  effects, and NOT CLAIMED (0)-(7), (7) being the observation cells pass 3 named and the owner filed as debt.
* `regress/gate_mips_folds.sh` (gate 16) -- the probe's block beside `#549`'s, before the pmax-kernel check: parse
  before score; CONTROL `OK`; exit 0; the score pinned by EQUALITY at 125; rows emitted, green rows and unique names
  reconciled with one anchored pattern (this probe prints a row's status after got/want); and EVERY expected row checked
  by name, green exactly once.
* `regress/gate_hygiene.sh` -- `EXPECT_PTY_PROBES` 75 -> 76 and `EXPECT_CONVERTED` 25 -> 26 for this probe (`#564`'s own
  stranded pin landed alone, in the commit before this one).
* `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 35 -> 36 (`fbctrl_cmd rows run ... 125`).
* `tools/pipeline/check_probe_wiring.py` -- the probe's MANIFEST line.
* `tools/pipeline/ledger.json` -- `fbctrlcmdkill` HELD for fable5 (Fable walled on every pass; a row may not close while
  a stage awaits a seat); FILES `fbctrlobsgrid` (MED: pass 3's observation cells), `fbctrlvec128` (LOW: a 16-byte vector
  store is taken as its low 64 bits, at DATA and at `#549`'s PORT) and `gate16fence` (LOW: gate 16 launches both device
  probes unfenced); `gatedevicesplit` gains the gate-16 stop -- a third device probe lands there only with the split or
  with a pin on the launch count.

**Measured** (`regress/artifacts/fbctrlcmdkill/`; every table's predictions written first, in a `PRETABLE*` file whose
mtime is the order proof).
* The draft (`draft_20261018/`): PRE-FIX 36/95 on HEAD's binary -- exactly the PRETABLE's prediction -- and 95/95 on
  the fix.
* Kill tables 1 and 1b (`killtable1_20261018/`, `killtable1b_20261018/`): sixteen mutants on the 95-row v1, all red;
  clause (b) `B_gateoff` (the arm as HEAD has it) row for row the pre-fix leg; clause (c) measured -- an absent and a
  non-emulator binary each CONTROL=FAILED.
* Pass 2's mutants, measured BEFORE any repair (table 2a): three passed v1 whole; probe v2 (99 rows) closed them and
  table 2 re-ran all 25: every one red.  F2's, measured before any repair (table 3a): seven passed v2 whole; probe v3
  (106 rows) closed them and table 3 re-ran all 32: every one red, every prediction held.
* Two consecutive passes had found one class open -- access WIDTH -- so v4 (123 rows) was built from an enumeration
  written before it ran (`killtable4_20261019/PRETABLE_ADDENDUM_t4.out`).  **Table 4** (06:30-07:03): the twelve
  newest mutants passed the 106-row v3 whole, and on v4 all 44 are red; legs 123/123 on the fix and 51/123 on HEAD's
  binary; both null media CONTROL=FAILED; every prediction held row for row (`KILLTABLE4_VS_PRETABLE.out`).
* Pass 3 found the v4 enumeration counted cells REACHED, not every effect OBSERVED; by the owner's ruling two rows were
  added from values R:edges already collected (`edge x1`, `edge y1`), and plain regression runs measured the 125-row
  probe: the fix 125/125, HEAD's build 51/125, both null media 17/125 with CONTROL=FAILED (`killtable4_20261019/legs41/`).
* Gate 16 run IN SITU (`wiring_20261019/INSITU.md`): on the default binary PASS, 161 checks; on HEAD's binary FAIL, 77 of
  161, every red check this block's.  The v4 block replayed on all 48 table-4 logs and five broken logs was green only
  on the fix (`GATE16_REPLAY_v4.out`).
* The weekly battery of 2026-10-18 (re-run at 23:19 after Modern Standby killed the 18:00 run) passed 16/16 with
  `#567`'s first, 95-row block in gate 16; the block that ships is the 125-row one, run in situ above.

**Panel.**  Pass 1 (`pass1_20261018/`): GPT-6 Astra, Grok 4.7 and GLM 5.3 chose member 3 (decline + latched announce),
the full 64-bit compare and a new gated probe; `fbctrloffkill` stays its own row (2-1).  Pass 2 (`pass2_20261018/`): all
three SHIP WITH CHANGES.  F2 (`pass2_20261018/f2/F2_DISPOSITIONS.md`): all three SHIP WITH CHANGES, converging on width x
bound edge and the latch's persistence.  Records corrected on the way, each a seat's catch: NOT CLAIMED (6) put the
16-byte loss in the wrong place (Astra, Grok); testppc's install is `machine_test.c`'s line 154, not 337 (Astra, Grok);
E8 sets the latch on an accept (GLM); GET_RESOLUTION makes four X1/Y1 assignments (Astra, Grok); v2's bound edges were
held at `sb` and `sw`.  Pass 3 (`pass3_20261019/F3_DISPOSITIONS.md`): GPT-6 Astra, GLM 5.3 and Grok 4.7 all SHIP WITH CHANGES -- the width enumeration counted cells reached, not every effect observed; by the owner's ruling two rows were added (`edge x1`, `edge y1`), the remaining cells filed as `fbctrlobsgrid`, and the records corrected (the gate comment, the probe's width list and NOT CLAIMED (2), (5) and (7)).  Confirm (GPT-6 Astra): requested on this unit.
Fable 5.1 walled (HTTP 429) on passes 1, 2, F2 and 3 -- each a seat failure, held with its question, never agreement;
the row is held for it.  Opus 5.5, agy, kimi, deepseek and minimax deliberately not fired (the owner's 2026-10-17
roster).  Twice while preparing a fuller pass-3 repair the main loop's own response was stopped by the safety
classifier; the owner then ruled the landing above.

```

## 6. The OUTSTANDING_BUGS.md section (verbatim)
```
### 2026-10-19 -- `#567`: dev_fbctrl.c refuses every command but 0-2 before the store (`fbctrlcmdkill` held for Fable); three rows filed; gate 16's stop recorded

* **`fbctrlcmdkill` (HIGH) HELD for fable5** -- `#567`: the DATA arm refuses, before the store, any write at COMMAND whose
  full 64-bit value is above GET_RESOLUTION -- COMMAND kept, nothing run, one `(once)` announce per device.  Witness
  2/12 on HEAD's binary, 12/12 on the fix (`regress/artifacts/fbctrlcmdkill/pass1_20261018/`).  Detector
  `regress/fbctrl_cmd_probe.py`, 125 rows, gated in gate 16 by name: the fix 125/125, HEAD's build 51/125, null media
  17/125 with CONTROL=FAILED; gate 16 in situ PASS on the fix, FAIL on HEAD.  Fable 5.1 walled on every pass of the
  round (HTTP 429), and a row may not close while a stage awaits a seat, so it is held with Fable's questions.
* **`fbctrlobsgrid` (MED, open)** -- pass 3's coverage debt, filed by the owner's 2026-10-19 ruling: in the 125-row probe
  several width x latch cells are REACHED but an effect there is not OBSERVED -- the latch's persistence after a
  non-word accept, a non-word read or a non-COMMAND store, each followed by a refusal; a read with the latch set at
  lb/lh/ld; a non-COMMAND read at lb/lh/ld; a non-COMMAND store with the latch set at sb/sh/sd; and refusal and accept
  effects a later write overwrites before any row reads them.  Also owed here: the measured check that the two rows
  added for pass 3 (`edge x1`, `edge y1`) catch the case it described.  Disclosed as the probe's NOT CLAIMED (7).
  From GPT-6 Astra and GLM 5.3, pass 3.
* **`fbctrlvec128` (LOW, open)** -- a 16-byte vector store (testppc's `stvx`/`stvxl`; `default_test()` installs the
  device) reaches the DATA and PORT arms with `len` 16; the callback receives all 16 bytes and `memory_readmax64()` keeps
  the low 64, so a 128-bit COMMAND value whose low half is 0-2 is accepted and runs (a low half of 1 runs
  SET_RESOLUTION) and a 128-bit selector whose low half is 0-7 is accepted -- `#567`'s and `#549`'s width defect one
  width out.  Owed: a rung-3 witness on testppc at both ports, then one disposition for both arms.  From GPT-6 Astra's
  pass-2 F1; filed, not repaired, by all three seats at F2.
* **`gate16fence` (LOW, open)** -- gate 16 launches `#549`'s and `#567`'s device probes with no timeout: a probe that
  hangs holds gate 16 and the weekly battery with it (visible, not a false pass).  A harness round: `timeout` sized from
  a measured run, red on exit 124, controlled both ways.  From GLM 5.3's pass-2 Q6, upheld as FILE at F2.
* **`gatedevicesplit`** -- gate 16 is now the second CPU gate holding device probes (`#549`'s and `#567`'s, both on
  `-E testmips`).  THE STOP (GLM 5.3, upheld at F2): a third device probe lands in gate 16 only with the split or with a
  pin on the gate's launch count.  Procedural, not mechanical -- this entry, the row and the gate's own comment carry it.
```

## 7. The ledger rows the unit changes (fbctrlcmdkill: its fields and the entries this round added)
```json
{
 "id": "gatedevicesplit",
 "note_tail": "s the only gate with probe infrastructure and a machine they share.  *The split was not done in this round on purpose: it is a harness round owing its own negative controls, and holding a HIGH device fix hostage to a gate refactor would be the tail wagging the dog.  What was not acceptable was compounding it silently.*  *** 2026-10-19, #567: GATE 16 (regress/gate_mips_folds.sh) IS THE SECOND CPU GATE HOLDING DEVICE PROBES -- #549's fbctrl_port_probe.py and now #567's fbctrl_cmd_probe.py, both on -E testmips.  THE STOP, in GLM 5.3's form (#567 pass 2; upheld at F2 by GPT-6 Astra, Grok 4.7 and GLM 5.3): A THIRD DEVICE PROBE LANDS IN GATE 16 ONLY WITH THE SPLIT, OR WITH A PIN ON THE GATE'S LAUNCH COUNT.  The stop is procedural, not mechanical -- this row and the gate's own comment are all that carry it.  Grok 4.7: 'The arm can land.  The sentence that this placement is fine should not.' ***",
 "last_entry": {
  "phase": "assess",
  "seat": "fable5",
  "date": "2026-10-19",
  "grade": "",
  "grader": "",
  "ev": "regress/artifacts/fbctrlcmdkill/pass2_20261018/f2/F2_DISPOSITIONS.md",
  "note": "[NOT A SEAT ANSWER] #567 (2026-10-19) adds the second device probe to gate 16, regress/gate_mips_folds.sh -- fbctrl_cmd_probe.py beside #549's fbctrl_port_probe.py, on -E testmips -- and records the stop: a third device probe lands there only with the split or with a pin on the launch count (GLM 5.3, upheld at F2)."
 }
}
Traceback (most recent call last):
  File "<stdin>", line 8, in <module>
  File "C:\Users\User00\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2713' in position 2336: character maps to <undefined>
```

## 8. Evidence summaries
```
LEGS41 start 2026-10-19 08:05:24; probe md5 9137235b5ae21129af65fc40580e12d7
/tmp/gx567: the fix, binary fresh, sentinel none
/tmp/gx566: HEAD source, binary fresh
FIX        rc=0 FBCMD_RESULT=125/125 FBCMD_CONTROL=OK last=FBCMD_DONE
        edge x1                got=0x7b                 want=0x7b                 ok  X1 keeps 123: neither refusal ran the resident GET (pass 3)
        edge y1                got=0x4d                 want=0x4d                 ok  Y1 keeps 77
HEAD       rc=1 FBCMD_RESULT=51/125 FBCMD_CONTROL=OK last=FBCMD_DONE
        edge x1                got=-                    want=0x7b                 FAIL  X1 keeps 123: neither refusal ran the resident GET (pass 3)
        edge y1                got=-                    want=0x4d                 FAIL  Y1 keeps 77
C_absent   rc=1 FBCMD_RESULT=17/125 FBCMD_CONTROL=FAILED last=FBCMD_DONE
        edge x1                got=-                    want=0x7b                 FAIL  X1 keeps 123: neither refusal ran the resident GET (pass 3)
        edge y1                got=-                    want=0x4d                 FAIL  Y1 keeps 77
C_bintrue  rc=1 FBCMD_RESULT=17/125 FBCMD_CONTROL=FAILED last=FBCMD_DONE
        edge x1                got=-                    want=0x7b                 FAIL  X1 keeps 123: neither refusal ran the resident GET (pass 3)
        edge y1                got=-                    want=0x4d                 FAIL  Y1 keeps 77
LEGS41 end 2026-10-19 08:05:46
LEGS41_DONE

INSITU start 2026-10-19 08:07:21
build/: part 1 ok, part 2 ok; /tmp/gx566: HEAD source,  binary fresh
probe in the tree: 7c34e8809f11f5d889542be73fb712f6; gate: 6cef649b9b0452e56ed8b647c370ecd4
=== fix 08:07:21
fix: gate rc=0; gate 16: MIPS fold witness (#388): PASS (161 checks)
fix: fbctrl_cmd checks 135, of them FAIL 0
=== head 08:07:52
head: gate rc=1; gate 16: MIPS fold witness (#388): FAIL (77 of 161 checks)
head: fbctrl_cmd checks 135, of them FAIL 77
INSITU end 2026-10-19 08:08:18
INSITU_DONE
```

## 9. Pretests on the unit
```
STAGE_PANELS_PASS / BOILERPLATE_PASS (0 new) / FABLE_QUEUE_PASS / ATTRIBUTION_PASS 0 hard 4 soft / WITNESS_PASS / PROBEWIRING_PASS 78/86 / section C: every cited src|regress path is touched
```
