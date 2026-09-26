# PASS 2 -- `#549` (fbctrlportkill): the diff, as it will be committed -- dev_fbctrl.c refuses an out-of-range PORT selector

Project root C:\DocumentNoSnc\cc\GXEMUL; the tree under review is `GXEMUL-SEC/` (ignore any other `src/`).
2026-09-24.  **FIRST LINE:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly -- and pass 1 of THIS round
found five false sentences in my own brief.  **Check the premises, not just the derivations**, and check every sentence
the diff ADDS (comments, the probe's contract, the gate block) against the source and against the measurements below.
**If you cannot read files that is expected** -- the whole diff and every measurement are inlined.  Name any premise you
cannot settle from this packet.  Seats that read files: stay within `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py` /
`*.sh`, plus the evidence directory named below; please do not read `tools/pipeline/ledger.json`.  **VERDICT LINE FIRST.**

## 0. WHAT PASS 1 SETTLED (fable5_p1b.md, claude-fable-5-1; re-inlined so nobody re-derives it)

* **The fix:** the PORT arm REFUSES a selector >= 8 on the full 64-bit `idata`, keeps the previous (always-valid)
  selector, and announces the refusal once per device with the house `(once)` marker.  Unanimous across nine seats.
* **The DATA arm's range check and `exit(1)` are KEPT, unedited except for a comment**, as a tripwire: once PORT refuses
  it is unreachable, and it is what stands between a future broken PORT arm and `port[8]` (which, after this diff's
  struct change, is the `warned_port` latch).  Precedent: `#521` left an unreachable `default:` exit "deliberately ... as
  a tripwire".  Dissent (codex panel, pass 1): make it a quiet refusal -- ruled against on the arguments.
* **Out of scope and FILED, not taken:** `fbctrl_command()`'s `default:` (any command other than 0-2, including the
  documented but unimplemented FILL (3) / COPY (4)) and the access function's `default:` (any offset other than 0x00 /
  0x10).  Both still end the process.  The Opus seat MEASURED that keep-previous-from-reset routes "refused selector,
  then a DATA write of an unknown command" into the command default; the contract says so.  Dissent (kimi-sub): the
  command default meets the reopening rule -- ruled against: a different fix design (implement vs decline FILL/COPY).
* **The rung-3 witness is valid** (unmodified `-E testmips`, stepped real `sw`/`lw`, liveness + device-signature +
  disassembly controls, death AND diagnostic required).  On HEAD: `sw 9` to PORT then `lw` from DATA ends the process,
  exit status 1.

## 1. THE MEASUREMENTS (the evidence directory is `GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/`)

* **The detector on HEAD f4f601c4: 25/41** -- every refusal, witness and announce row red.  **On the fix: 41/41.**
* **Build trees:** `build/` rebuilt to the fix (md5 4cc158f6, identical to the scratch fix build), `/tmp/gxsec-build`
  and `build-asan/` rebuilt, part 1 CLEAN and part 2 FRESH on all three, no compiler warnings; `est/` byte-identical.
* **Kill table 2** (`table2/TABLE.out`; the frozen instrument is `table2/fbctrl_port_probe.table2.py.txt`; predictions
  written first in `PRETABLE.out` and `PRETABLE_ADDENDUM_t2.out`).  Each variant built in a WSL `/tmp` clone of `build/`,
  scored by the probe below.  Rows red per variant, verbatim from TABLE.out:

```
base_fix FBCTRLP_RESULT=41/41 FBCTRLP_CONTROL=OK FBCTRLP_DONE
M_acc4      26/41                  accept selector 0 written by sw; accept selector 1 written by sb; accept selector 2 written by sh; accept selector 3 written by sw; accept selector 4 written by sd; accept selector 5 written by sb; accept selector 6 written by sh; accept selector 7 written by sd; port 1 round-trips its DATA value; port 2 round-trips its DATA value; port 3 round-trips its DATA value; port 4 round-trips its DATA value; port 5 round-trips its DATA value; port 6 round-trips its DATA value; port 7 round-trips its DATA value
M_acclatch  40/41                  refuse 9 after PORT=7, PORT keeps 7
M_and5      40/41                  refuse 9 after PORT=7, PORT keeps 7
M_ann_any   40/41                  C nothing refused, no (once) line
M_bit       38/41                  refuse 16 (sw), PORT keeps 5; refuse 0x200000000 (sd), PORT keeps 5; refuse 0x100 (sh), PORT keeps 5
M_clamp     29/41                  refuse 9 (sw), PORT keeps 5; refuse 8 (sw), PORT keeps 5; refuse 16 (sw), PORT keeps 5; refuse 0x200000000 (sd), PORT keeps 5; refuse 0x100000003 (sd), PORT keeps 5; refuse all-ones (sd), PORT keeps 5; refuse all-ones (sw), PORT keeps 5; refuse 0xff (sb), PORT keeps 5; refuse 0x100 (sh), PORT keeps 5; refuse 9 after PORT=7, PORT keeps 7; K DATA read after the refusal is port 5's; K DATA write after the refusal lands in port 5
M_debug     40/41                  F refusal announced while free-running (fatal)
M_decl      40/41                  refuse all-ones (sd), PORT keeps 5
M_gt        40/41                  refuse 8 (sw), PORT keeps 5
M_i32       37/41                  refuse 0x200000000 (sd), PORT keeps 5; refuse 0x100000003 (sd), PORT keeps 5; refuse all-ones (sd), PORT keeps 5; refuse all-ones (sw), PORT keeps 5
M_i64       40/41                  refuse all-ones (sd), PORT keeps 5
M_latch0    40/41                  announce: still exactly 1 after ten refusals
M_latchcnt  38/41                  announce: exactly 1 right after the FIRST refusal; announce: still exactly 1 after ten refusals; F refusal announced while free-running (fatal)
M_latchinv  38/41                  announce: exactly 1 right after the FIRST refusal; announce: still exactly 1 after ten refusals; F refusal announced while free-running (fatal)
M_mod33     40/41                  refuse 0x200000000 (sd), PORT keeps 5
M_noguard   41/41                  (none red)
M_perval    40/41                  announce: still exactly 1 after ten refusals
M_reflatch  32/41                  refuse 8 (sw), PORT keeps 5; refuse 16 (sw), PORT keeps 5; refuse 0x200000000 (sd), PORT keeps 5; refuse 0x100000003 (sd), PORT keeps 5; refuse all-ones (sd), PORT keeps 5; refuse all-ones (sw), PORT keeps 5; refuse 0xff (sb), PORT keeps 5; refuse 0x100 (sh), PORT keeps 5; refuse 9 after PORT=7, PORT keeps 7
M_rej2      39/41                  accept selector 2 written by sh; port 1 round-trips its DATA value
M_reset0    28/41                  refuse 9 (sw), PORT keeps 5; refuse 8 (sw), PORT keeps 5; refuse 16 (sw), PORT keeps 5; refuse 0x200000000 (sd), PORT keeps 5; refuse 0x100000003 (sd), PORT keeps 5; refuse all-ones (sd), PORT keeps 5; refuse all-ones (sw), PORT keeps 5; refuse 0xff (sb), PORT keeps 5; refuse 0x100 (sh), PORT keeps 5; refuse 9 after PORT=7, PORT keeps 7; K survives DATA after a refused PORT write; K DATA read after the refusal is port 5's; K DATA write after the refusal lands in port 5
M_revert    25/41                  refuse 9 (sw), PORT keeps 5; refuse 8 (sw), PORT keeps 5; refuse 16 (sw), PORT keeps 5; refuse 0x200000000 (sd), PORT keeps 5; refuse 0x100000003 (sd), PORT keeps 5; refuse all-ones (sd), PORT keeps 5; refuse all-ones (sw), PORT keeps 5; refuse 0xff (sb), PORT keeps 5; refuse 0x100 (sh), PORT keeps 5; refuse 9 after PORT=7, PORT keeps 7; announce: exactly 1 right after the FIRST refusal; announce: still exactly 1 after ten refusals; K survives DATA after a refused PORT write; K DATA read after the refusal is port 5's; K DATA write after the refusal lands in port 5; F refusal announced while free-running (fatal)
M_static    41/41                  (none red)
M_store     28/41                  refuse 9 (sw), PORT keeps 5; refuse 8 (sw), PORT keeps 5; refuse 16 (sw), PORT keeps 5; refuse 0x200000000 (sd), PORT keeps 5; refuse 0x100000003 (sd), PORT keeps 5; refuse all-ones (sd), PORT keeps 5; refuse all-ones (sw), PORT keeps 5; refuse 0xff (sb), PORT keeps 5; refuse 0x100 (sh), PORT keeps 5; refuse 9 after PORT=7, PORT keeps 7; K survives DATA after a refused PORT write; K DATA read after the refusal is port 5's; K DATA write after the refusal lands in port 5
M_u32       39/41                  refuse 0x200000000 (sd), PORT keeps 5; refuse 0x100000003 (sd), PORT keeps 5
M_wide      39/41                  refuse 0xff (sb), PORT keeps 5; refuse 0x100 (sh), PORT keeps 5
```

  22 of 22 variants of the fix's own predicate, store and latch are red; `M_revert` (HEAD's PORT arm verbatim at the one
  fixed site -- floor clause b) is 25/41; `M_static` (a process-global latch) and `M_noguard` (the DATA check deleted)
  are 41/41, as the contract discloses.  Table 1 ran the same 23 variants without session P's re-select and matched on
  every verdict; its per-row credit was overstated by a cascade (the flagship seat caught it), which is why the probe
  now re-selects PORT=5 before every refusal.

* **Gates on the working tree** (both files are the committed text):

```
## GATE: gate 16: MIPS fold witness (#388)
  ok   fbctrl probe output parses                           yes
  ok   fbctrl probe controls                                OK
  ok   fbctrl probe exit status                             0
  ok   fbctrl_port rows run                                 41
  ok   fbctrl_port rows correct                             41
  ok   fbctrl_port rows failed                              0
gate 16: MIPS fold witness (#388): PASS (23 checks)
GATE16_RC=0 WALL=7s
(gate 6: derive_hygiene_pins.sh report got == pinned on every census: PTY 74/74, promptless 43/43,
 converted 25/25 x3, whole-buffer 3/3; then gate 4 -> gate 6 run alone: mips-rigs PASS (6 checks, 246 s), log-hygiene PASS (36 checks, 184 s) --
 gates/gate4.out, gates/gate6.out)
```

## 2. THE DIFF -- `git diff --numstat` and disclosure per file

```
16   5   src/devices/dev_fbctrl.c                 INLINED (est/ carries the byte-identical file)
366  0   regress/fbctrl_port_probe.py (new)       INLINED
41   0   regress/gate_mips_folds.sh               INLINED
2    2   regress/gate_hygiene.sh                  INLINED (written by tools/derive_hygiene_pins.sh --write)
1    0   tools/pipeline/check_probe_wiring.py     INLINED (the committed hunk; the working copy also carries another
                                                  unit's uncommitted lines, which this commit does not include)
3    1   tools/precommit_check.sh                 INLINED (committed hunk, same caveat)
-    -   regress/artifacts/fbctrlportkill_20260924/   NOT SHOWN -- the evidence directory; its tables are inlined above
-    -   CHANGELOG.md, OUTSTANDING_BUGS.md, ledger     NOT YET WRITTEN -- records follow this pass
```

**Gate 6's two pins** count what lies in the working tree, by the owner's 2026-09-23 ruling ("re-pin, count all"):
`EXPECT_PTY_PROBES` 73 -> 74 (this probe) and `EXPECT_CONVERTED` 24 -> 25 (it uses the canonical readiness form).  A clean
export of HEAD plus these files counts 71, because three other units' probes lie untracked in the working tree -- the
same state HEAD's own pins already carry (their comment says so).  **The gate-16 pin raises `SCORE_CLAIMS_MANIFEST`
30 -> 31**, because `check_score_claims.py` now sees one more pinned probe.

## 3. THE DIFF, INLINED

### dev_fbctrl.c, gate_mips_folds.sh, gate_hygiene.sh

```diff
diff --git a/regress/gate_hygiene.sh b/regress/gate_hygiene.sh
index 193b5054..221ecd71 100644
--- a/regress/gate_hygiene.sh
+++ b/regress/gate_hygiene.sh
@@ -382,7 +382,7 @@ check "readiness: no unrecognised endswith spelling" "$unknown" "$EXPECT_UNKNOWN
 #  and reds THREE rows -- this one, the promptless count and the promptless-names row -- because all three are
 #  grandfathered names that exist only in the working tree (measured on a copy with them removed: 70/73, 40/43,
 #  names gone=the three).  Written by `tools/derive_hygiene_pins.sh --write`, never by hand. ***
-EXPECT_PTY_PROBES=73
+EXPECT_PTY_PROBES=74
 #  *** AND THE SAME PROBE BROKE A SECOND CENSUS IN THIS FILE, WHICH pass 11's OWN
 #  REPAIR DID NOT FIX.  Found by the codex seat reviewing that repair. ***
 #
@@ -593,7 +593,7 @@ fi
 #  send() spelled the fresh mark `mark=mark`, which the fresh-mark census does not read, so that one said
 #  23 and the three #392 counts DISAGREED at HEAD.  The probe's rename to `_mark` (same change) makes the
 #  three agree; the deriver refuses to write while they disagree, which is why the rename precedes the pin. ***
-EXPECT_CONVERTED=24
+EXPECT_CONVERTED=25
 #  One helper for all three, so they agree on WHAT they look at.  The first draft
 #  used py_code() for the anchored count and a raw grep for the other two, which
 #  meant a comment mentioning the echo guard would have inflated one count and not
diff --git a/regress/gate_mips_folds.sh b/regress/gate_mips_folds.sh
index 409a5209..4b57ab00 100644
--- a/regress/gate_mips_folds.sh
+++ b/regress/gate_mips_folds.sh
@@ -32,6 +32,47 @@ PMAX=${PMAX:-$ROOT/build/gxemul}
 PMAX_KERNEL=$ROOT/gxemul_pmax_rig/bsd
 
 if [ ! -x "$PMAX" ]; then gate_skip "no gxemul binary at $PMAX"; fi
+
+#  ---------------------------------------------------------------------------------------
+#  #549 fbctrlportkill: dev_fbctrl.c's PORT selector, on -E testmips.  Before #549 a guest
+#  store of 8 or more to PORT was STORED with only a warning, and the next DATA access ended
+#  the emulator in the DATA arm's range check.  #549 refuses the selector (the previous one
+#  is kept) and announces the refusal once.  regress/fbctrl_port_probe.py drives real guest
+#  sb/sh/sw/sd/lw on an unmodified testmips -- no kernel, no rig image -- so it runs BEFORE
+#  this gate's pmax-kernel check: a missing kernel still skips the fold rows below, and
+#  gate_skip reports FAIL, not SKIP, if an fbctrl row failed first.
+#
+#  THE CONTRACT is the probe's header (CATCHES / NOT CLAIMED).  Kill table 1 was red on 20 of
+#  20 edits of the fix's own predicate, store and latch; a process-global latch and the
+#  deletion of the DATA arm's kept check are DISCLOSED escapes; and the device still ends the
+#  process through its command and offset defaults, which are filed, not claimed.  HEAD before
+#  #549 scored 25/41 here, every refusal row red.
+#
+#  `gatedevicesplit` is OWED (#498): one more device probe in a CPU gate, as #548 added to
+#  gate 14.  Recorded, not compounded silently.
+FBCLOG=$LOGDIR/fbctrl_port_probe.log
+fbrc=0
+python3 -u fbctrl_port_probe.py "$PMAX" > "$FBCLOG" 2>&1 || fbrc=$?
+if [ "$(grep -cx 'FBCTRLP_DONE' "$FBCLOG")" != "1" ] ||
+   [ "$(grep -c '^FBCTRLP_RESULT=' "$FBCLOG")" != "1" ] ||
+   ! grep -Eq '^FBCTRLP_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$FBCLOG" ||
+   [ "$(grep -c '^FBCTRLP_CONTROL=' "$FBCLOG")" != "1" ] ||
+   ! grep -Eq '^FBCTRLP_CONTROL=(OK|FAILED)$' "$FBCLOG"; then
+    note "fbctrl probe produced no unique, complete record; last lines follow"
+    tail -5 "$FBCLOG" | sed 's/^/       /'
+    check "fbctrl probe output parses" "no" "yes"
+else
+    check "fbctrl probe output parses" "yes" "yes"
+    grep -E '^  FAIL ' "$FBCLOG" | sed 's/^/       /'
+    check "fbctrl probe controls" "$(sed -n 's/^FBCTRLP_CONTROL=//p' "$FBCLOG")" "OK"
+    check "fbctrl probe exit status" "$fbrc" "0"
+    fbres=$(sed -n 's/^FBCTRLP_RESULT=//p' "$FBCLOG")
+    #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin.
+    check "fbctrl_port rows run" "${fbres#*/}" 41
+    check "fbctrl_port rows correct" "${fbres%/*}" "41"
+    check "fbctrl_port rows failed" "$(grep -c '^  FAIL ' "$FBCLOG")" "0"
+fi
+
 if [ ! -f "$PMAX_KERNEL" ]; then gate_skip "no pmax kernel at $PMAX_KERNEL"; fi
 
 FLOG=$LOGDIR/gate_mips_folds.log
diff --git a/src/devices/dev_fbctrl.c b/src/devices/dev_fbctrl.c
index cc69ab3e..7a03224f 100644
--- a/src/devices/dev_fbctrl.c
+++ b/src/devices/dev_fbctrl.c
@@ -49,6 +49,7 @@ struct fbctrl_data {
 	struct vfb_data *vfb_data;
 	int		current_port;
 	int		port[DEV_FBCTRL_NPORTS];
+	int		warned_port;	/* #549: the refused-selector announce */
 };
 
 
@@ -116,15 +117,25 @@ DEVICE_ACCESS(fbctrl)
 	case DEV_FBCTRL_PORT:
 		if (writeflag == MEM_READ)
 			odata = d->current_port;
-		else {
+		else if (idata >= DEV_FBCTRL_NPORTS) {
+			/*  #549: an out-of-range selector is REFUSED, and
+			    current_port keeps its previous, always-valid value.
+			    It used to be stored with only a warning, and the
+			    next DATA access then ended the emulator in the
+			    range check below.  Announced once per device.  */
+			if (!d->warned_port) {
+				fatal("[ fbctrl: port number 0x%llx is out of range; "
+				    "the selector is unchanged (once) ]\n",
+				    (unsigned long long) idata);
+				d->warned_port = 1;
+			}
+		} else
 			d->current_port = idata;
-			if (idata >= DEV_FBCTRL_NPORTS)
-				fatal("[ WARNING: fbctrl port number is out"
-				    " of range! ]\n");
-		}
 		break;
 
 	case DEV_FBCTRL_DATA:
+		/*  #549: unreachable while the PORT arm refuses; kept as a
+		    tripwire for a later edit that lets a bad selector in.  */
 		if (d->current_port < 0 || d->current_port
 		    >= DEV_FBCTRL_NPORTS) {
 			fatal("[ fbctrl port number is out of range! ]\n");
```

### regress/fbctrl_port_probe.py (new file)

```diff
diff --git a/regress/fbctrl_port_probe.py b/regress/fbctrl_port_probe.py
new file mode 100644
index 00000000..352c6d24
--- /dev/null
+++ b/regress/fbctrl_port_probe.py
@@ -0,0 +1,366 @@
+#!/usr/bin/env python3
+r"""#549 fbctrlportkill -- the DETECTOR for dev_fbctrl.c's port selector, on an UNMODIFIED `-E testmips`.
+
+machine_test.c installs `fbctrl addr=0x12f00000` in testmips's own setup (and in default_test() for the other test
+machines).  Every access below is a real guest sb/sh/sw/sd/lw placed with `put w` and executed through real address decode
+and memory_rw -- stepped one instruction at a time, except session F, which free-runs to a breakpoint.  No machine or
+device is added to reach the site.  t0 = 0xffffffffb2f00000, kseg1 of DEV_FBCTRL_ADDRESS; PORT is +0x00, DATA +0x10.
+
+THE DEFECT (HEAD before #549): the PORT arm STORED any selector with only a warning, and the DATA arm then called exit(1)
+on the stored int -- `sw 9` to PORT followed by any DATA access ended the emulator process.  #549 REFUSES a selector >= 8
+at the PORT arm (the previous, valid selector is kept) and announces the refusal once per device, `(once)`.
+
+SESSIONS (each on a fresh emulator)
+  C  controls: PORT=5, DATA=0x2a, read both back (LIVENESS); X1=123, COMMAND=GET_RESOLUTION, read X1 (DEVICE SIGNATURE:
+     the model zeroes X1/Y1 without X11 -- RAM at +0x10 would read back 2, the last value written there, and a banked
+     register WITHOUT command execution would read 123); no `(once)` line may appear (nothing is refused).
+  A  accept: all EIGHT selectors, written at widths 1, 2, 4 and 8, each read back through PORT; ports 1-7 round-trip
+     a distinct DATA value (port 0 is COMMAND and is written only with NOP).
+  P  refusal, anchored to a previous selector: PORT=5 (DATA 0x2a), then nine out-of-range writes -- 9, 8, 16 (sw),
+     0x200000000, 0x100000003, all-ones (sd), all-ones (sw), 0xff (sb), 0x100 (sh) -- each PRECEDED by a fresh
+     PORT=5 and followed by a PORT read that must still say 5, so every row fails only on its own value; then
+     PORT=7 and a refused 9 must leave 7.  The `(once)` count must be exactly 1 right
+     after the FIRST refusal and still 1 after the last.
+  K  the witness pair, repaired: PORT=5, DATA=0x2a, PORT=9 refused, then a DATA READ (must survive and read port 5's
+     0x2a) and a DATA WRITE of 0x77 (must land in port 5: read back through PORT=5).
+  F  free-running: one refused PORT write, then `continue` to a breakpoint.  Stepping raises debug()'s verbosity, so a
+     refusal announced with debug() instead of fatal() would pass every stepped row; free-running it does not print.
+
+CONTRACT (clause e).  CATCHES: the store reached for an out-of-range value (or a clamped/masked/reset one), the compare
+narrowed or signed (bit 63, bits 32-33, 32-bit truncation), a boundary slip at 8, a refusal applied to some widths only,
+a legal selector refused, a refusal that rewrites the previous selector, a latch never set / set late / keyed per value,
+an announce demoted to debug(), and the pre-#549 process exit on DATA (kill table 1: 20 of 20 such edits red,
+regress/artifacts/fbctrlportkill_20260924/table1/TABLE.out).  NOT CLAIMED: a process-global latch instead of the
+per-instance field (every machine installs ONE fbctrl; adding a device to reach a second would be laundering); the
+deletion of the DATA arm's range check, which a correct PORT arm makes unreachable -- it is KEPT as a tripwire, and it
+matters beyond style: `warned_port` sits right after `port[8]`, so an index of 8 that got past a broken PORT arm would
+land on the latch itself; and the device's OTHER two process-ending calls -- fbctrl_command()'s default (any command
+other than 0-2, including the documented but unimplemented FILL/COPY; a refused selector at power-on leaves COMMAND
+selected, so a following DATA write of such a value reaches it) and the access function's default (any offset other
+than 0x00/0x10).  Those are filed.  Session P re-selects PORT=5 before each refusal: kill table 1 ran without the
+re-select, and one corrupted selector then turned every later "keeps 5" row red, overstating which row catches
+what (the flagship seat, pass 1).
+
+Every stepped word is compared with the emulator's own step line (the hand-assembled-encoding trap).
+Output: one row per check, then FBCTRLP_CONTROL=OK|FAILED, FBCTRLP_RESULT=n/t, FBCTRLP_DONE.
+usage: fbctrl_port_probe.py <gxemul-binary>
+"""
+import os
+import pty
+import re
+import select
+import signal
+import sys
+import time
+
+BIN = sys.argv[1]
+
+STUBADDR = 0xffffffff80100000
+CODE = 0xffffffff80100020
+FBCTRL = 0xffffffffb2f00000
+
+ONCE_RE = re.compile(r"\[ fbctrl: port number 0x[0-9a-f]+ is out of range; the selector is unchanged \(once\) \]")
+
+REG = dict(zr=0, v0=2, v1=3, a0=4, a1=5, a2=6, a3=7, t0=8, t1=9, t2=10, t3=11, t4=12, t5=13, t6=14, t7=15,
+           s0=16, s1=17, s2=18, s3=19, s4=20, s5=21, s6=22, s7=23, t8=24, t9=25)
+OPS = dict(sb=0x28, sh=0x29, sw=0x2b, sd=0x3f, lw=0x23)
+
+
+def ins(op, rt, off, base="t0"):
+    return (OPS[op] << 26) | (REG[base] << 21) | (REG[rt] << 16) | (off & 0xffff)
+
+
+def text(op, rt, off, base="t0"):
+    return "%s %s,%d(%s)" % (op, rt, off, base)
+
+
+ANCHOR = (0x0f << 26) | (REG["t7"] << 16)                   # lui t7,0 -- the breakpoint anchor, never executed
+#  Pinned independently of the helper: a wrong register field would otherwise pass silently.
+assert ins("sw", "t1", 0) == 0xad090000
+assert ins("lw", "t2", 0x10) == 0x8d0a0010
+assert ins("sd", "t5", 0) == 0xfd0d0000
+assert ins("sb", "t8", 0) == 0xa1180000
+assert ins("sh", "t9", 0) == 0xa5190000
+assert ANCHOR == 0x3c0f0000
+
+
+def stub_path():
+    p = "/tmp/gx_fbctrl549p_%d.bin" % os.getpid()
+    with open(p, "wb") as f:
+        f.write(b"\x00\x00\x00\x00")
+    return p
+
+
+def session(label, prog, regs, reads, stub, free_run=False):
+    """prog: list of (op, rt, off, tag).  Steps each (or free-runs to an anchor after the last), then prints reads.
+    Returns dict: status, exit, badis, vals, once_after (tag -> cumulative (once) count right after that step), buf."""
+    pid, fd = pty.fork()
+    if pid == 0:
+        os.execvp(BIN, [BIN, "-V", "-E", "testmips", "-M", "64", "0x%x:%s" % (STUBADDR, stub)])
+        os._exit(127)
+    buf = ""
+    dead = [False]
+
+    def rd(t=0.4):
+        nonlocal buf
+        r, _, _ = select.select([fd], [], [], t)
+        if fd not in r:
+            return True
+        try:
+            d = os.read(fd, 65536)
+        except OSError:
+            dead[0] = True
+            return False
+        if not d:
+            dead[0] = True
+            return False
+        buf += d.decode("latin1", "replace")
+        return True
+
+    def wait(mark=0, echo=None, timeout=60):
+        t = time.time()
+        while time.time() - t < timeout:
+            if not rd():
+                return False
+            resp = buf[mark:]
+            if echo is not None and echo not in resp:
+                continue
+            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
+                return True
+        return False
+
+    def send(x, timeout=60):
+        b = (x + "\n").encode("latin1")
+        _mark = len(buf)
+        n = 0
+        try:
+            while n < len(b):
+                n += os.write(fd, b[n:])
+        except OSError:
+            dead[0] = True
+            return False
+        return wait(mark=_mark, echo=x if x else None, timeout=timeout)
+
+    words = [ins(op, rt, off) for op, rt, off, _t in prog] + [ANCHOR]
+    status, badis, vals, once_after, steps = "?", [], {}, {}, 0
+    if not wait(timeout=120):
+        status = "NO-PROMPT"
+    else:
+        for i, w in enumerate(words):
+            send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
+        for name, val in regs:
+            send("%s=0x%x" % (name, val & 0xffffffffffffffff))
+        send("pc=0x%x" % CODE)
+        status = "SURVIVED"
+        if free_run:
+            send("breakpoint add 0x%x" % (CODE + 4 * len(prog)))
+            mark = len(buf)
+            b = b"continue\n"
+            try:
+                os.write(fd, b)
+            except OSError:
+                dead[0] = True
+            if not wait(mark=mark, timeout=60) or dead[0]:
+                status = "HOST-DIED" if dead[0] else "NO-BREAK"
+            elif ("%016x" % (CODE + 4 * len(prog))) not in buf[mark:] and \
+                    ("%08x" % ((CODE + 4 * len(prog)) & 0xffffffff)) not in buf[mark:]:
+                status = "NO-BREAK"
+            else:
+                steps = len(prog)
+                once_after["free"] = len(ONCE_RE.findall(buf))
+        else:
+            for i, (op, rt, off, tag) in enumerate(prog):
+                mark = len(buf)
+                if not send("step 1", timeout=30) or dead[0]:
+                    status = "HOST-DIED"
+                    break
+                steps += 1
+                seg = buf[mark:]
+                w = words[i]
+                m = re.search(r"%016x:?\s+%08x\s+([^\r\n<]+)" % (CODE + 4 * i, w), seg)
+                got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(no step line)"
+                if not got.startswith(text(op, rt, off)):
+                    badis.append("+0x%02x planted 0x%08x -> %r, expected %r" % (4 * i, w, got, text(op, rt, off)))
+                if tag:
+                    once_after[tag] = len(ONCE_RE.findall(buf))
+        if status == "SURVIVED":
+            for name in reads:
+                got = None
+                for _ in range(2):
+                    mark = len(buf)
+                    if not send("print %s" % name, timeout=30) or dead[0]:
+                        break
+                    m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
+                    if m:
+                        got = int(m.group(1), 16)
+                        break
+                vals[name] = got
+    try:
+        os.write(fd, b"quit\n")
+    except OSError:
+        pass
+    t1 = time.time()
+    while time.time() - t1 < 20.0:
+        if not rd(0.1):
+            break
+    try:
+        os.close(fd)
+    except OSError:
+        pass
+    rpid, st = 0, None
+    t1 = time.time()
+    while rpid == 0 and time.time() - t1 < 10.0:
+        try:
+            rpid, st = os.waitpid(pid, os.WNOHANG)
+        except OSError:
+            break
+        if rpid == 0:
+            time.sleep(0.05)
+    if rpid == 0:
+        try:
+            os.kill(pid, signal.SIGKILL)
+            _, st = os.waitpid(pid, 0)
+        except OSError:
+            st = None
+    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
+    print("  session %-2s %-9s steps=%d/%d exit=%s once=%d" % (label, status, steps, len(prog), code,
+                                                              len(ONCE_RE.findall(buf))))
+    for b in badis:
+        print("      DISASSEMBLY MISMATCH: %s" % b)
+    return {"status": status, "exit": code, "badis": badis, "vals": vals, "once_after": once_after,
+            "steps": steps, "buf": buf, "n": len(prog)}
+
+
+RESULTS = []
+
+
+def row(name, got, want, note=""):
+    ok = got == want
+    RESULTS.append(ok)
+    print("  %-4s %-48s got=%-20s want=%-20s %s" % ("ok" if ok else "FAIL", name, got, want, note))
+    return ok
+
+
+def hx(v):
+    return "-" if v is None else "0x%x" % v
+
+
+M64 = 0xffffffffffffffff
+
+
+def lw32(v):
+    """what `lw` of a 32-bit device answer yields in a 64-bit register (sign-extended)"""
+    v &= 0xffffffff
+    return v | 0xffffffff00000000 if v & 0x80000000 else v
+
+
+# ---------------------------------------------------------------- sessions
+PROG_C = [("sw", "t1", 0, None), ("sw", "t3", 16, None), ("lw", "t4", 16, None), ("lw", "t5", 0, None),
+          ("sw", "t6", 0, None), ("sw", "t7", 16, None), ("sw", "s0", 0, None), ("sw", "s1", 16, None),
+          ("sw", "t6", 0, None), ("lw", "s2", 16, None)]
+REGS_C = [("t0", FBCTRL), ("t1", 5), ("t3", 0x2a), ("t6", 1), ("t7", 123), ("s0", 0), ("s1", 2),
+          ("t4", 0xdead), ("t5", 0xdead), ("s2", 0xdead)]
+
+#  A: selector p written at a rotating width and read back through PORT into s<k> (poisoned 0xdead first, so a
+#  read that never ran cannot pass -- selector 0 would otherwise match a register's reset value); DATA value 0x11*p
+#  for p >= 1, read back through DATA INTO THE SELECTOR REGISTER, which holds p before the read, never 0x11*p.
+#  Port 0 is COMMAND: written with NOP (0, from zr) only.
+ACC = [(0, "sw"), (1, "sb"), (2, "sh"), (3, "sw"), (4, "sd"), (5, "sb"), (6, "sh"), (7, "sd")]
+SEL_REG = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"]           # the selector values
+VAL_REG = ["zr", "a0", "a1", "a2", "a3", "v0", "v1", "t9"]           # the DATA values (port 0 gets zr = NOP)
+PORT_RB = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7"]           # PORT read-backs
+PROG_A, REGS_A = [], [("t0", FBCTRL)]
+for k, (p, w) in enumerate(ACC):
+    REGS_A.append((SEL_REG[k], p))
+    REGS_A.append((PORT_RB[k], 0xdead))
+    if k:
+        REGS_A.append((VAL_REG[k], 0x11 * p))
+    PROG_A.append((w, SEL_REG[k], 0, None))                            # PORT = p at width w
+    PROG_A.append(("lw", PORT_RB[k], 0, None))                         # read PORT
+    PROG_A.append(("sw", VAL_REG[k], 16, None))                        # DATA = 0x11*p (NOP for port 0)
+#  the DATA read-backs, one per port 1..7: re-select p, read DATA into the selector register
+for k, (p, w) in enumerate(ACC):
+    if k:
+        PROG_A.append(("sw", SEL_REG[k], 0, None))
+        PROG_A.append(("lw", SEL_REG[k], 16, None))
+READS_A = PORT_RB + SEL_REG[1:]
+
+#  P: previous selector 5, then nine refusals, then previous 7 and one more.
+REFUSE = [("sw", "t1", 9, "9 (sw)"), ("sw", "t2", 8, "8 (sw)"), ("sw", "t3", 16, "16 (sw)"),
+          ("sd", "t4", 0x200000000, "0x200000000 (sd)"), ("sd", "t5", 0x100000003, "0x100000003 (sd)"),
+          ("sd", "t6", M64, "all-ones (sd)"), ("sw", "t7", 0xffffffff, "all-ones (sw)"),
+          ("sb", "t8", 0xff, "0xff (sb)"), ("sh", "t9", 0x100, "0x100 (sh)")]
+READ_P = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "v0"]
+PROG_P = [("sw", "a0", 0, None), ("sw", "a1", 16, None)]
+REGS_P = [("t0", FBCTRL), ("a0", 5), ("a1", 0x2a), ("a2", 7)]
+for k, (w, r, v, _n) in enumerate(REFUSE):
+    REGS_P.append((r, v))
+    if k:
+        PROG_P.append(("sw", "a0", 0, None))                   # a fresh PORT=5 before every later refusal
+    PROG_P.append((w, r, 0, "r%d" % k))
+    PROG_P.append(("lw", READ_P[k], 0, None))
+PROG_P += [("sw", "a2", 0, None), ("sw", "t1", 0, "r9"), ("lw", "v1", 0, None)]
+READS_P = READ_P + ["v1"]
+
+PROG_K = [("sw", "t1", 0, None), ("sw", "t3", 16, None), ("sw", "t2", 0, None), ("lw", "s0", 16, None),
+          ("sw", "t4", 16, None), ("sw", "t1", 0, None), ("lw", "s1", 16, None)]
+REGS_K = [("t0", FBCTRL), ("t1", 5), ("t3", 0x2a), ("t2", 9), ("t4", 0x77), ("s0", 0xdead), ("s1", 0xdead)]
+
+PROG_F = [("sw", "t1", 0, None)]
+REGS_F = [("t0", FBCTRL), ("t1", 9)]
+
+
+def main():
+    stub = stub_path()
+    try:
+        C = session("C", PROG_C, REGS_C, ["t4", "t5", "s2"], stub)
+        A = session("A", PROG_A, REGS_A, READS_A, stub)
+        P = session("P", PROG_P, REGS_P, READS_P, stub)
+        K = session("K", PROG_K, REGS_K, ["s0", "s1"], stub)
+        F = session("F", PROG_F, REGS_F, [], stub, free_run=True)
+    finally:
+        try:
+            os.unlink(stub)
+        except OSError:
+            pass
+    ctl = []
+    print("CONTROLS")
+    ctl.append(row("C every step survived", "%s %d/%d" % (C["status"], C["steps"], C["n"]),
+                   "SURVIVED %d/%d" % (len(PROG_C), len(PROG_C))))
+    ctl.append(row("C disassembly of every stepped word", len(C["badis"]), 0))
+    ctl.append(row("C LIVENESS: DATA round-trips 0x2a", hx(C["vals"].get("t4")), "0x2a"))
+    ctl.append(row("C LIVENESS: PORT reads back 5", hx(C["vals"].get("t5")), "0x5"))
+    ctl.append(row("C SIGNATURE: X1 zeroed by GET_RESOLUTION", hx(C["vals"].get("s2")), "0x0",
+                   "(RAM: 2; banked w/o command: 123)"))
+    row("C nothing refused, no (once) line", len(ONCE_RE.findall(C["buf"])), 0)
+    for S in (A, P, K):
+        ctl.append(row("%s disassembly of every stepped word" % "APK"[(A, P, K).index(S)], len(S["badis"]), 0))
+    print("ACCEPT (session A: %s %d/%d)" % (A["status"], A["steps"], A["n"]))
+    for k, (p, w) in enumerate(ACC):
+        row("accept selector %d written by %s" % (p, w), hx(A["vals"].get(PORT_RB[k])), hx(p))
+    for k, (p, w) in enumerate(ACC):
+        if k:
+            row("port %d round-trips its DATA value" % p, hx(A["vals"].get(SEL_REG[k])), hx(0x11 * p))
+    print("REFUSE (session P: %s %d/%d)" % (P["status"], P["steps"], P["n"]))
+    for k, (w, r, v, name) in enumerate(REFUSE):
+        row("refuse %s, PORT keeps 5" % name, hx(P["vals"].get(READ_P[k])), "0x5")
+    row("refuse 9 after PORT=7, PORT keeps 7", hx(P["vals"].get("v1")), "0x7")
+    row("announce: exactly 1 right after the FIRST refusal", P["once_after"].get("r0"), 1)
+    row("announce: still exactly 1 after ten refusals", P["once_after"].get("r9"), 1)
+    print("THE WITNESS PAIR (session K)")
+    row("K survives DATA after a refused PORT write", "%s %d/%d" % (K["status"], K["steps"], K["n"]),
+        "SURVIVED %d/%d" % (len(PROG_K), len(PROG_K)))
+    row("K DATA read after the refusal is port 5's", hx(K["vals"].get("s0")), "0x2a")
+    row("K DATA write after the refusal lands in port 5", hx(K["vals"].get("s1")), "0x77")
+    print("FREE-RUNNING (session F)")
+    row("F free-run reached its breakpoint", F["status"], "SURVIVED")
+    row("F refusal announced while free-running (fatal)", F["once_after"].get("free"), 1)
+    control = all(ctl)
+    n_ok, n = sum(RESULTS), len(RESULTS)
+    print("FBCTRLP_CONTROL=%s" % ("OK" if control else "FAILED"))
+    print("FBCTRLP_RESULT=%d/%d" % (n_ok, n))
+    print("FBCTRLP_DONE")
+
+
+if __name__ == "__main__":
+    main()
```

### tools/pipeline/check_probe_wiring.py (the committed hunk)

```diff
diff --git a/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbctrl549/dry/cpw_HEAD.py b/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbctrl549/dry/cpw_549.py
index 6363cd86..ede6d3ff 100644
--- a/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbctrl549/dry/cpw_HEAD.py
+++ b/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbctrl549/dry/cpw_549.py
@@ -2379,6 +2379,7 @@ MANIFEST = {
     "pit8253_latch_probe.py":      (CLASS_DETECTOR, "#439/#440 PIT latch + LSB/MSB selector"),
     "sh4_bsc_width_probe.py":      (CLASS_DETECTOR, "#441 BCR2/BCR3 non-16-bit access"),
     "fbpending_drain_probe.py":    (CLASS_DETECTOR, "#442 footbridge pending-tick backlog"),
+    "fbctrl_port_probe.py":        (CLASS_DETECTOR, "#549 fbctrl PORT selector refusal"),
     "hpcmips_ctor_probe.py":       (CLASS_DETECTOR, "#444 every hpcmips subtype constructs"),
 
     # -- witnesses.  RED once the fix lands, so gating one manufactures a regression. -----
```

### tools/precommit_check.sh (the committed hunk)

```diff
diff --git a/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbctrl549/dry/pcc_HEAD.sh b/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbctrl549/dry/pcc_549.sh
index 5c1e4b08..e47498f0 100644
--- a/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbctrl549/dry/pcc_HEAD.sh
+++ b/C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbctrl549/dry/pcc_549.sh
@@ -338,7 +338,9 @@ elif out=$(python "$SCORECHK" 2>&1); then
 	#  (#528, pinned UNQUOTED in gate_sh_rounding.sh at 37 rows).
 	#  RAISED 29 -> 30 ON 2026-09-18, DELIBERATELY.  One newly gated probe: landisk_aux_probe.py
 	#  (#533, pinned UNQUOTED in gate_sh_rounding.sh at 6 rows).
-	SCORE_CLAIMS_MANIFEST=30
+	#  RAISED 30 -> 31 ON 2026-09-24, DELIBERATELY.  One newly gated probe: fbctrl_port_probe.py
+	#  (#549, pinned UNQUOTED in gate_mips_folds.sh at 41 rows).
+	SCORE_CLAIMS_MANIFEST=31
 	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
 	if [ -z "$_spinned" ]; then
 		bad "check_score_claims printed no SCORE_CLAIMS_PINNED line -- the count cannot be pinned"
```

## 4. QUESTIONS

1. **Premise audit of the DIFF.**  Check every sentence the diff adds -- the two comments in `dev_fbctrl.c`, the probe's
   header (SESSIONS / CONTRACT / NOT CLAIMED), the gate-16 block's comment -- against the source and against section 1's
   measurements.  A sentence true only for the case measured, or overstating what a row observes, is a finding.  Pass 1
   found five such sentences in my own brief.
2. **What is the SMALLEST EDIT to `dev_fbctrl.c` -- outside the 25 variants in table 2 -- that breaks the refusal and still
   scores 41/41?**  Name the row you expect to stay green.  And the smallest edit to the PROBE or to the gate-16 block that
   keeps every pin green while the device is wrong.
3. **The gate-16 block.**  Is the parse guard complete (a missing, duplicated or malformed RESULT/CONTROL/DONE line; a
   probe that dies early)?  Does moving the pmax-kernel check below the block change gate 16's result for any state it
   could be in before (binary missing, kernel missing, fold rows red)?
4. **The contract.**  Is the NOT CLAIMED list complete and true -- the process-global latch, the deleted DATA check, the
   struct-layout sentence about `port[8]`, the command and offset defaults?  Is anything CLAIMED that no row observes?
5. **Records owed by this commit** (CHANGELOG block, OUTSTANDING_BUGS filings for the command default and the offset
   default, the ledger row) -- is anything owed that I have not listed?

If, while verifying a claim, you found something ELSE -- say so.
