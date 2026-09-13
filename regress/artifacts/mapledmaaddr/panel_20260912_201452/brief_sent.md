# VERIFICATION PASS — `mapledmaaddr` (#528): is the regression test's output comparison now complete?

VERDICT LINE FIRST (`CLOSES` or `GAP: <exact edit>`), then the liveness token `FINAL528_20260912`.

This is ordinary mutation-testing work on an emulator's regression test.  Please check the premises, not only the
reasoning, and say which ones you could not check from this text.  Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`
(ignore any other `src/`, which is an unmodified 2021 upstream copy).

## Background (settled; re-stated because the questions depend on it)

* The code fix: in `src/devices/dev_dreamcast_maple.c`, the Maple bus device's register-read handler for `MAPLE_DMAADDR`
  (offset 0x04) used to print a "TODO" message and terminate the emulator; it now just returns the stored value, like
  its sibling register `MAPLE_ENABLE`.  The fix has been unchanged and uncontested for the whole review.
* The regression test `regress/maple_dmaaddr_probe.py` (37 checks) drives real guest instructions through GXemul's
  debugger over a pseudo-terminal.  One check, `read silent`, requires that reading the register produces NO extra
  emulator output — an earlier review ruled that a reinstated message alone must fail the test.
* How `read silent` works now: for each of twelve test sessions, it builds from the typed commands alone the exact
  list of lines the debugger prints (command echo, register value, memory-write confirmation, one disassembly line per
  stepped instruction), and compares the session's WHOLE output — from the first prompt until the pseudo-terminal
  closes after `quit` — against that list, line by line.  Any extra, missing or altered line, anything after the
  `quit` echo, or any carriage return not part of CRLF fails it.

## What the previous pass found, and what changed

The previous version compared only the output captured BEFORE `quit` was typed.  Four reviewers predicted, and the
compile-and-measure reviewer confirmed (37/37 — the test missed it), that a handler which registers an `atexit()`
callback printing a message would print after that point and go unnoticed.  The earlier grammar-based version of the
test had looked at the whole buffer, so this was a coverage loss introduced by the previous change.

The change under review (below): the session now reads until the pseudo-terminal reaches end-of-file after `quit`,
and the comparison covers the whole output, with `quit` expected to print exactly its echo and then nothing more.
A clean build passes 37/37 with it.

**Kill table 6** (targeted; results in `regress/artifacts/mapledmaaddr/killtable6_20260912/SCORES.txt` and
`POSTTABLE.out` once it finishes): 17 runs, 17 exactly on prediction.  New version: correct build 37/37 three times; the original defect 11/37; the `atexit` handler 36/37 (`read silent` fails in 12/12 sessions: one extra line after the `quit` echo); every earlier message shape (plain text, bare hex number, blank line, bare carriage return, prompt-like text with or without newline, the literal `GXemul> quit`) still fails `read silent`.  Previous version on the same binary: the `atexit` handler 37/37 (missed), reproducing the measurement.

## The change, verbatim (previous test version → current)

```diff
--- /c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/mapledmaaddr/killtable5_20260912/maple_dmaaddr_probe.FROZEN5.py	2026-09-12 18:13:40.186401100 -0500
+++ /c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/maple_dmaaddr_probe.py	2026-09-12 19:30:19.654684000 -0500
@@ -13,24 +13,24 @@
 handler.  Every load destination is seeded with a POISON value distinct from every want, so a fix that silently skips
 the load cannot pass a value row.
 
-CONTRACT (vacuity-floor clause e).  Designed to catch, and each MEASURED in a kill table under
-artifacts/mapledmaaddr/ (killtable2_20260912/ .. killtable5_20260912/): the removed fatal()+exit(1) reinstated (HEAD);
-a diagnostic alone, in ANY wording or shape -- verbatim, reworded with or without the device name, latched, a bare hex
-value, a blank line, a bare carriage return, a prompt-shaped line with or without a newline, the text of a typed
-command -- because the silence row compares each of the twelve read sessions' transcript, as it stood BEFORE `quit'
-was typed, with the exact line sequence its commands owe (owed(): every echo, value, `put' confirmation and
-disassembly line, computed from the command alone), and rejects any CR that is not the pty's CRLF (never a device
-name, never a whitelist of line shapes); exit(1) alone; the FAULT idiom `return 0' (a silent load-skip on SH4, where
-memory_rw.c raises no exception); DECLINE, unconditional or keyed on the consumer's partitions -- `read aligned' (a
-32-byte-aligned value), `read enabled' (after MAPLE_ENABLE = 1) and their joint cell `read joint'; an exit keyed on
-either partition; the read hoisted out of its `relative_addr == 0x04' guard; the selector narrowed by any ONE bit --
-the eight-cell generating set `relative_addr & ~bit' folds 0x04|bit or 0x04&~bit onto DMAADDR: `alias 0x05' (mov.b),
-`alias 0x06' (mov.w), `alias 0x00' (bit 2 dropped, e.g. `case 0x00:' stacked on the label), `alias 0x0c/24/44/84',
-`other 0x14' -- and 0x04 widened onto any other case label (`other 0x..'); a read arm that also writes MAPLE_ENABLE
-or the timeout (`other pre read' then `other 0x14' / `other 0x80'); a read that clears the field, or sets or clears
-any one bit of it (`double read 2', `zero reread', `ones reread'); an effect that starts on the third read (`reread
-3'); masking of the low five bits; an exit keyed on the value 0, 4, bit 30, or a 16- or 8-bit access (`read width16',
-`read width8').
+CONTRACT (vacuity-floor clause e).  Designed to catch, and each MEASURED in a kill table under artifacts/mapledmaaddr/
+(killtable2_20260912/ .. killtable6_20260912/): the removed fatal()+exit(1) reinstated (HEAD); a diagnostic alone, in
+ANY wording or shape -- verbatim, reworded with or without the device name, latched, a bare hex value, a blank line, a
+bare carriage return, a prompt-shaped line with or without a newline, the text of a typed command, or a line printed
+late (an atexit handler, a buffered stream's flush at exit) -- because the silence row compares each of the twelve
+read sessions' WHOLE transcript, from its first prompt to the pty's EOF, with the exact line sequence its commands owe
+(owed(): every echo, value, `put' confirmation and disassembly line, computed from the command alone; the typed `quit'
+owes its echo and then nothing), and rejects any CR that is not the pty's CRLF (never a device name, never a whitelist
+of line shapes); exit(1) alone; the FAULT idiom `return 0' (a silent load-skip on SH4, where memory_rw.c raises no
+exception); DECLINE, unconditional or keyed on the consumer's partitions -- `read aligned' (a 32-byte-aligned value),
+`read enabled' (after MAPLE_ENABLE = 1) and their joint cell `read joint'; an exit keyed on either partition; the read
+hoisted out of its `relative_addr == 0x04' guard; the selector narrowed by any ONE bit -- the eight-cell generating
+set `relative_addr & ~bit' folds 0x04|bit or 0x04&~bit onto DMAADDR: `alias 0x05' (mov.b), `alias 0x06' (mov.w),
+`alias 0x00' (bit 2 dropped, e.g. `case 0x00:' stacked on the label), `alias 0x0c/24/44/84', `other 0x14' -- and 0x04
+widened onto any other case label (`other 0x..'); a read arm that also writes MAPLE_ENABLE or the timeout (`other pre
+read' then `other 0x14' / `other 0x80'); a read that clears the field, or sets or clears any one bit of it (`double
+read 2', `zero reread', `ones reread'); an effect that starts on the third read (`reread 3'); masking of the low five
+bits; an exit keyed on the value 0, 4, bit 30, or a 16- or 8-bit access (`read width16', `read width8').
 NOT COVERED, each DISCLOSED under clause (e), for one of two different reasons.  (1) A VALUE CELL OF THE BODY-READ
 FIELD that the body does not partition -- inside the DEPENDS-ON enumeration, not floor because the arm copies the
 field and tests nothing about it: an effect keyed on another exact value, or on a bit pattern all-ones does not set;
@@ -46,7 +46,8 @@
 the host); 64-bit reads (no reachable 8-byte callback on this SH4: fmov with SZ=1 issues two 4-byte accesses); a
 `writeflag' that is neither MEM_READ nor MEM_WRITE (no caller passes one -- EQUIVALENT); moving the assignment out of
 the `else' (the tail ignores odata on a write -- EQUIVALENT); a diagnostic that prints no byte (`fatal("")' --
-EQUIVALENT: va_debug prints nothing for an empty format).
+EQUIVALENT: va_debug prints nothing for an empty format); output on a channel the pty never carries (a file the arm
+opens, syslog) -- off the operator's console, and outside what a transcript can observe.
 NO ROW asserts what a read returns AFTER a DMA transfer.  Whether the transfer's cursor update (`d->dmaaddr = addr'
 at the end of maple_do_dma_xfer) is architectural is the separate row `mapledmaadvance', whose detector will observe
 it through this read arm using the refusal message's printed field as its oracle -- never a computed `P + 12'.
@@ -141,12 +142,10 @@
             break
         if not rd(spin if i == len(cmds) - 1 else 0.20):
             break
-    global SNAP
-    SNAP = buf                  # the transcript BEFORE `quit' is typed: what noise() reads (no exemption needed)
     try:
         os.write(fd, b"quit\n")
-        rd(0.4)
-    except OSError:
+        rd(10.0)                # read to EOF (rd returns at once when the pty closes): whatever the emulator prints
+    except OSError:             # on its way out -- an atexit handler, a buffered stream's flush -- is in the transcript
         pass
     try:
         os.close(fd)
@@ -172,10 +171,15 @@
 #    table 4  plus blank / bare-CR / prompt counts, with the typed `quit' echo EXEMPTED -- and Fable (pass 2) predicted
 #             `fatal("GXemul> ")' glued onto the next prompt line and `fatal("GXemul> quit\n")' in the exemption.
 #  Three passes, one class: a silence oracle built as a whitelist has, by construction, a shape to hide in.  So the
-#  oracle is now the TRANSCRIPT ITSELF: every command owes an exact, in-order sequence of lines computed from the
-#  command alone (owed() below), the snapshot is taken before `quit' is typed (so nothing is exempt), and every CR must
-#  be the pty's CRLF.  A quiet emulator prints exactly that; anything else -- extra, missing, glued or reordered -- is
-#  the emulator speaking.  The only disguise left is a diagnostic that emits no byte (`fatal("")': EQUIVALENT).
+#  oracle became the TRANSCRIPT ITSELF (table 5): every command owes an exact, in-order sequence of lines computed from
+#  the command alone (owed() below), and every CR must be the pty's CRLF.
+#    table 5  ...read from a snapshot taken BEFORE `quit' was typed -- and the closing pass (deepseek, kimi, glm) found
+#             the TIME axis: `atexit(announce)' registered by the read prints after the snapshot, which table 4's
+#             whole-buffer grammar would have caught.  The repair had narrowed the window it was meant to close.
+#  So the transcript is now the WHOLE session, from the first prompt to the pty's EOF: `quit' owes exactly its echo and
+#  then nothing, whatever the emulator would print on its way out.  A quiet emulator prints exactly the owed lines;
+#  anything else -- extra, missing, glued, reordered, altered, or late -- is the emulator speaking.  What is left: a
+#  diagnostic that emits no byte (`fatal("")': EQUIVALENT) and output on a channel the pty never carries (a file).
 _HEX = re.compile(r"^0x([0-9a-f]+)$")
 _PUT = re.compile(r"^0x([0-9a-f]+): ([0-9a-f]+)$")
 _DIS = re.compile(r"^([0-9a-f]{8}):\s+([0-9a-f]{4})\s")
@@ -208,6 +212,8 @@
                 out.append(("disasm", (pc, code.get(pc))))
                 pc += 2
             continue
+        if c == "quit":
+            continue                            # owes its echo; then the process ends, and nothing may follow
         if re.match(r"^print r\d+$", c):
             out.append(("value", None))        # WHICH value is the rows' business; that it is one hex line is this
             continue
@@ -231,12 +237,13 @@
 
 
 def noise(t, cmds):
-    """Differences between the pre-`quit' transcript `t' and the exact transcript `cmds' owe.  Empty = silent."""
+    """Differences between the whole session transcript `t' (first prompt to EOF) and the exact transcript `cmds'
+    owe, the typed `quit' included.  Empty = silent."""
     i = t.find("GXemul> ")
     raw = t[i:] if i >= 0 else t
     lines = raw.replace("\r", "").split("\n")
     body, tail = lines[:-1], lines[-1]
-    exp = owed(cmds)
+    exp = owed(cmds + ["quit"])
     bad = []
     for k, (kind, want) in enumerate(exp):
         if k >= len(body):
@@ -247,8 +254,8 @@
             break
     if not bad and len(body) > len(exp):
         bad.append("%d surplus line(s), first %r" % (len(body) - len(exp), body[len(exp)]))
-    #  after the last command the debugger may already have printed the next prompt, or not yet (a read window)
-    if tail not in ("", "GXemul> "):
+    #  after `quit' the emulator exits: the transcript ends on the echo's newline
+    if tail != "":
         bad.append("trailing %r" % tail)
     bare_cr = raw.count("\r") - raw.count("\r\n")
     if bare_cr:
@@ -283,20 +290,17 @@
     sys.stdout.flush()
 
 
-#  The READ sessions: every one of them must be silent -- noise() finds its pre-`quit' transcript to be exactly the
-#  owed one.  A write to MAPLE_DMAADDR or MAPLE_ENABLE prints nothing (the former's debug() is
+#  The READ sessions: every one of them must be silent -- noise() finds its whole transcript, through `quit' to EOF,
+#  to be exactly the owed one.  A write to MAPLE_DMAADDR or MAPLE_ENABLE prints nothing (the former's debug() is
 #  commented out) and every other register read in these sessions is a quiet arm, so ANY extra output is the read
 #  speaking.  Keyed on the channel, never on one literal string (Fable pass 1: the literal form is vacuous by
 #  construction against a reworded or latched announce; §F2, codex: nor on a line SHAPE alone).
 READS = []
 
 
-SNAP = ""
-
-
 def rsession(cmds):
     t, how = session(cmds)
-    READS.append((SNAP, how, cmds))
+    READS.append((t, how, cmds))
     return t, how
 
 
@@ -404,7 +408,8 @@
 
 # -- silence over every read session, FLOOR ---------------------------------------------------------------------------
 noisy = [n for n in (noise(t, c) for t, _, c in READS) if n]
-row("read silent", "%d/%d" % (len(noisy), len(READS)), "0/%d" % 12, "read sessions whose transcript is not the owed one")
+row("read silent", "%d/%d" % (len(noisy), len(READS)), "0/%d" % 12,
+    "read sessions whose transcript is not the owed one")
 for n in noisy[:3]:
     print("    noise: %r" % n[:2])
 
```

## QUESTIONS

1. **Is any emulator output produced because of the register read still not compared?**  If so, give the exact C
   change to the read handler and what the test would see.  Output written somewhere other than the terminal (a file,
   syslog) is already listed as outside the test's reach; say if you disagree.
2. **Can a correct build fail this comparison?**  (Timing: the fixed read windows, the read-until-EOF after `quit`,
   a slow exit, the first prompt.)  Can a crashed session pass it?
3. **Does the review chain close here?**  Name what you checked.  If it closes, would a future miss be "outside the
   stated contract" or "a breach of it"?
4. **Which statement above is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
