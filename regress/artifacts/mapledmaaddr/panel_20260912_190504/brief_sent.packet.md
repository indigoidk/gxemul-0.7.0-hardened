# CLOSING PASS — `mapledmaaddr` (#528): the silence oracle's CLASS CLOSURE.  One question: does it close?

VERDICT LINE FIRST (`CLOSES` or `SURVIVOR: <exact edit>`), then the liveness token `CLOSE528_20260912`.

Please **do not ratify.**  Three consecutive passes on this detector each found a survivor of the same class, and the
repair for each one reproduced the class inside itself.  This is the fourth oracle.  Check the premises below, not only
the derivations; state which you could not check from this packet.  Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` —
ignore any other `src/` (the project root holds pristine 2021 upstream copies).

## SETTLED PREMISES (recorded resolutions; re-inlined because questions below depend on them)

* THE FIX (unchanged since pass 1, upheld by every seat on three passes): `src/devices/dev_dreamcast_maple.c`, case
  `0x04` (MAPLE_DMAADDR), read arm: `fatal(TODO); odata = d->dmaaddr; exit(1);` → `odata = d->dmaaddr;`.  The common
  tail is `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata); return 1;`.  The default arm prints
  `[ dreamcast_maple: UNIMPLEMENTED read from addr 0x.. ]` and answers 0.
* INTERVAL SILENCE IS FLOOR (flagship ruling, pass 1; upheld pass 2): a diagnostic-alone reinstatement is half of the
  removed defect.  So a diagnostic of ANY wording or shape printed during a DMAADDR read must red `read silent`.
* `fatal()` returns (it does not exit) and prints unconditionally; `va_debug` prints nothing for an empty format, so
  `fatal("")` is EQUIVALENT (flagship seat verified `debugmsg.c`).
* Under `step`, the disassembly line is printed BEFORE the instruction executes (`cpu_dyntrans.c`), so a device
  diagnostic lands after the disassembly line's newline and before the debugger's next prompt.
* The debugger echoes each typed command after its `GXemul> ` prompt; `rN=0x..` and `pc=0x..` print the value on its
  own line; `put h A, V` prints `0xA: VVVV`; `step N` prints N disassembly lines `aaaaaaaa:  oooo  mnemonic...`;
  `print rN` prints the value.  A clean read session, measured (tail of the `read val_a` session):

```
GXemul> r1=0xa05f6c04\r\n0xa05f6c04\r\nGXemul> r2=0xa5a55a5a\r\n0xa5a55a5a\r\nGXemul> put h 0x8c001020, 0x6212\r\n
0x8c001020: 6212\r\nGXemul> put h 0x8c001022, 0xaffe\r\n0x8c001022: affe\r\nGXemul> put h 0x8c001024, 0x0009\r\n
0x8c001024: 0009\r\nGXemul> pc=0x8c001020\r\n0x8c001020\r\nGXemul> step 1\r\n8c001020:  6212        mov.l\t@r1,r2\t;
r1 = 0xa05f6c04\r\nGXemul> print r2\r\n0x8c012345\r\nGXemul> quit\r\n
```

## THE HISTORY (the class, stated once)

| oracle | swept by |
|---|---|
| a literal (`dreamcast_maple` in the transcript) | `fatal("[ maple: DMAADDR read ]")` |
| a quiet grammar (prompt echo / bare hex / put confirmation / disassembly) | `fatal("0x%08x\n", ...)` — a `print` answer's shape |
| grammar + per-class counts | `fatal("\n")` — the grammar's shape-free blank line |
| + blank / bare-CR / prompt counts, typed `quit` echo EXEMPT | `fatal("GXemul> quit\n")` — MEASURED 35/35 (the exemption); `fatal("GXemul> ")` predicted 35/35, measured 34/35 only because ONE session steps two instructions |

## THE FOURTH ORACLE (the diff below): an EXACT OWED TRANSCRIPT

`session()` snapshots the pty buffer BEFORE it types `quit`; `owed(cmds)` computes from the commands alone the exact
line sequence a quiet session prints — echo, assigned value, `put` address+value, each stepped instruction's address
and opcode — and `noise()` rejects any missing / extra / altered line, any trailing text other than "" or a waiting
`GXemul> `, and any CR that is not the pty's CRLF.  Two value rows were added in the same diff (`zero reread`, `ones
reread`), 35 → 37 rows.

**MEASURED — kill table 5** (targeted, `regress/artifacts/mapledmaaddr/killtable5_20260912/`, PRETABLE before,
POSTTABLE after): 21 runs, 20 exactly on prediction.  New instrument: BASE 37/37 three times; HEAD 11/37; every
diagnostic leg — verbatim, bare hex, blank line, bare CR, prompt line, glued `GXemul> `, `GXemul> quit` — 36/37 on
`read silent` alone (12/12 sessions for the last two); `& ~0x10` 35/37; `& ~0x04` 21/37; `|= 0x80000000` 36/37 (`zero
reread`); `&= ~0x40000000` 36/37 (`ones reread`); read-to-clear 33/37; third-read exit 35/37.  Earlier tables 1–4 killed
every other enumerated mutant (a hoist, eight single-bit selector narrowings, consumer-keyed declines and exits, width
exits, a sibling write, a joint decline, value-keyed exits).  The fourth oracle is a strict tightening of the third.

## THE DIFF (table 4's instrument → the shipped one), verbatim

```diff
--- artifacts/mapledmaaddr/killtable4_20260912/maple_dmaaddr_probe.FROZEN4.py	2026-09-12 16:22:05.443072400 -0500
+++ maple_dmaaddr_probe.py	2026-09-12 18:09:56.666036200 -0500
@@ -14,33 +14,39 @@
 the load cannot pass a value row.
 
 CONTRACT (vacuity-floor clause e).  Designed to catch, and each MEASURED in a kill table under
-artifacts/mapledmaaddr/ (killtable2_20260912/, killtable3_20260912/, killtable4_20260912/): the removed
-fatal()+exit(1) reinstated (HEAD); a diagnostic alone -- verbatim, reworded WITH or WITHOUT the device name, latched,
-or printing only a bare hex value, a blank line, a bare carriage return or a prompt-shaped line -- because the silence
-row counts, in the twelve read sessions, any transcript line outside the debugger's quiet grammar AND any line class
-(hex / put / disassembly / prompt) whose count differs from what the session's commands owe, any interior blank line
-and any CR that is not the pty's CRLF (never a device name); exit(1) alone;
-the FAULT idiom `return 0' (a silent load-skip on SH4, where memory_rw.c raises no exception); DECLINE, unconditional
-or keyed on the consumer's partitions -- `read aligned' (a 32-byte-aligned value), `read enabled' (after
-MAPLE_ENABLE = 1) and their joint cell `read joint'; an exit keyed on either partition; the read hoisted out of its
-`relative_addr == 0x04' guard; 0x04 widened onto another case label (a read at EVERY other label, `other 0x..'), onto
-a single-bit alias in the default arm (`alias 0x0c/24/44/84', and through the low bits by the SUB-WORD accesses that
-reach them, `alias 0x05' mov.b and `alias 0x06' mov.w), or onto 0x00 (`alias 0x00'); a read arm that also writes
-MAPLE_ENABLE or the timeout (`other pre read' then `other 0x14' / `other 0x80'); a read that clears the field (`double
-read 2'); an effect that starts on the third read (`reread 3'); masking of the low five bits; an exit keyed on the
-value 0, 4, bit 30, or a 16- or 8-bit access (`read width16', `read width8').
-NOT COVERED, each clause (e) -- the arm copies the field and tests no partition of it, and DEPENDS-ON's bound stops
-at the enclosing function: an effect keyed on another exact value, or on a bit pattern all-ones does not set; any
-single SET bit is pinned by all-ones by construction but only bit 30 was measured; masking of HIGH bits is covered by
-the values but was not separately measured; an effect starting after the third read in one process (counter > 3);
-side effects on sibling state the rows never read back (MAPLE_STATE reads a constant 0; the port devices; anything
-read only by maple_do_dma_xfer()); effects keyed on the environment (time, verbosity, the host); 64-bit reads (no
-reachable 8-byte callback on this SH4); a `writeflag' that is neither MEM_READ nor MEM_WRITE (no caller passes one --
-EQUIVALENT); moving the assignment out of the `else' (the tail ignores odata on a write -- EQUIVALENT); a diagnostic
-that prints no byte (`fatal("")' -- EQUIVALENT: nothing reaches the guest or the operator).  The
-consumer-keyed forms (`enable', the alignment bits, the read count) are outside the BOUND, not merely value cells:
-`d->enable' is read by maple_do_dma_xfer(), never by the guarded body.  Their rows are L1 -- licensed because cheap,
-never graded floor because cheap.
+artifacts/mapledmaaddr/ (killtable2_20260912/ .. killtable5_20260912/): the removed fatal()+exit(1) reinstated (HEAD);
+a diagnostic alone, in ANY wording or shape -- verbatim, reworded with or without the device name, latched, a bare hex
+value, a blank line, a bare carriage return, a prompt-shaped line with or without a newline, the text of a typed
+command -- because the silence row compares each of the twelve read sessions' transcript, as it stood BEFORE `quit'
+was typed, with the exact line sequence its commands owe (owed(): every echo, value, `put' confirmation and
+disassembly line, computed from the command alone), and rejects any CR that is not the pty's CRLF (never a device
+name, never a whitelist of line shapes); exit(1) alone; the FAULT idiom `return 0' (a silent load-skip on SH4, where
+memory_rw.c raises no exception); DECLINE, unconditional or keyed on the consumer's partitions -- `read aligned' (a
+32-byte-aligned value), `read enabled' (after MAPLE_ENABLE = 1) and their joint cell `read joint'; an exit keyed on
+either partition; the read hoisted out of its `relative_addr == 0x04' guard; the selector narrowed by any ONE bit --
+the eight-cell generating set `relative_addr & ~bit' folds 0x04|bit or 0x04&~bit onto DMAADDR: `alias 0x05' (mov.b),
+`alias 0x06' (mov.w), `alias 0x00' (bit 2 dropped, e.g. `case 0x00:' stacked on the label), `alias 0x0c/24/44/84',
+`other 0x14' -- and 0x04 widened onto any other case label (`other 0x..'); a read arm that also writes MAPLE_ENABLE
+or the timeout (`other pre read' then `other 0x14' / `other 0x80'); a read that clears the field, or sets or clears
+any one bit of it (`double read 2', `zero reread', `ones reread'); an effect that starts on the third read (`reread
+3'); masking of the low five bits; an exit keyed on the value 0, 4, bit 30, or a 16- or 8-bit access (`read width16',
+`read width8').
+NOT COVERED, each DISCLOSED under clause (e), for one of two different reasons.  (1) A VALUE CELL OF THE BODY-READ
+FIELD that the body does not partition -- inside the DEPENDS-ON enumeration, not floor because the arm copies the
+field and tests nothing about it: an effect keyed on another exact value, or on a bit pattern all-ones does not set;
+any single SET bit is pinned by all-ones by construction but only bit 30 was measured; masking of HIGH bits is covered
+by the values but was not separately measured.  The alignment rows (`read aligned', `read joint') are of this kind and
+are L1 -- licensed because cheap, never graded floor because cheap.  (2) OUTSIDE THE DEPENDS-ON ENUMERATION -- not a
+lvalue the guarded body reads: `d->enable' (read by maple_do_dma_xfer(), never by the body), a read counter, `len'
+(the common tail's argument); the rows `read enabled', `reread 3', `read width16/8' are L1 on the same terms.  Also
+disclosed: an effect starting after the third read in one process (counter > 3); an effect KEYED on sibling state the
+rows leave at its reset value (`} else if (d->timeout) {' -- the timeout is 0 in every read session); side effects on
+sibling state the rows never read back (MAPLE_STATE reads a constant 0; the port devices; anything read only by
+maple_do_dma_xfer()); two-bit selector merges (multi-axis joints); effects keyed on the environment (time, verbosity,
+the host); 64-bit reads (no reachable 8-byte callback on this SH4: fmov with SZ=1 issues two 4-byte accesses); a
+`writeflag' that is neither MEM_READ nor MEM_WRITE (no caller passes one -- EQUIVALENT); moving the assignment out of
+the `else' (the tail ignores odata on a write -- EQUIVALENT); a diagnostic that prints no byte (`fatal("")' --
+EQUIVALENT: va_debug prints nothing for an empty format).
 NO ROW asserts what a read returns AFTER a DMA transfer.  Whether the transfer's cursor update (`d->dmaaddr = addr'
 at the end of maple_do_dma_xfer) is architectural is the separate row `mapledmaadvance', whose detector will observe
 it through this read arm using the refusal message's printed field as its oracle -- never a computed `P + 12'.
@@ -135,6 +141,8 @@
             break
         if not rd(spin if i == len(cmds) - 1 else 0.20):
             break
+    global SNAP
+    SNAP = buf                  # the transcript BEFORE `quit' is typed: what noise() reads (no exemption needed)
     try:
         os.write(fd, b"quit\n")
         rd(0.4)
@@ -156,44 +164,95 @@
     return buf, how
 
 
-#  THE SILENCE CHANNEL (pass 2, 2026-09-12).  The first version counted sessions whose transcript contained the text
-#  `dreamcast_maple' -- which IS one literal, and a token-free `fatal("[ maple: DMAADDR read ]")' passed it (codex, glm,
-#  kimi).  A clean session prints only this grammar after the first prompt -- measured on the fixed build: the
-#  `GXemul> ' command echo, a bare hex value (`r1=' / `print'), a `put' confirmation `0x...: hhhh', and the stepped
-#  instruction's disassembly `8c001000:  2122  mov.l ...'.  ANY other line is the emulator speaking, whatever it says.
-_QUIET = (re.compile(r"^$"), re.compile(r"^GXemul> "), re.compile(r"^0x[0-9a-f]+$"),
-          re.compile(r"^0x[0-9a-f]+: [0-9a-f]+$"), re.compile(r"^[0-9a-f]{8}:\s+[0-9a-f]{4}\s"))
-
-
-def noise(t, cmds=None):
-    """Lines after the first debugger prompt that are not in the quiet grammar -- AND, when the session's commands are
-    given, any surplus in a line CLASS.  The §F2 pass (codex) showed a grammar alone is a whitelist of SHAPES: a
-    diagnostic that prints a bare hex line (`fatal("0x%08x\\n", ...)') fits the shape of a `print' answer.  So each
-    command is owed exactly its expected output: one hex line per `rN=' / `pc=' / `print', one `put' confirmation per
-    `put', one disassembly line per stepped instruction, one prompt line per command.  A count that differs is the
-    emulator speaking.  And the grammar's two shape-free members are closed the same way (§F2, grok: `fatal("\\n")'
-    prints only a BLANK line): a clean session's only empty line is the one after its final newline, and every CR is
-    the pty's CRLF -- measured on the fixed build, 3 x 3 sessions (blank_measure: blanks=1, bare CR 0)."""
+#  THE SILENCE CHANNEL -- AN EXACT TRANSCRIPT, NOT A WHITELIST.  Its history is the lesson, so it is kept:
+#    pass 1   sessions containing the text `dreamcast_maple' -- one literal; `fatal("[ maple: ... ]")' passed it.
+#    pass 2   any line outside a quiet GRAMMAR (prompt echo, bare hex, put confirmation, disassembly) -- a whitelist of
+#             SHAPES; `fatal("0x%08x\n", ...)' took the shape of a `print' answer (§F2, codex).
+#    table 3  plus a COUNT per line class -- `fatal("\n")' used the grammar's shape-free blank line (grok).
+#    table 4  plus blank / bare-CR / prompt counts, with the typed `quit' echo EXEMPTED -- and Fable (pass 2) predicted
+#             `fatal("GXemul> ")' glued onto the next prompt line and `fatal("GXemul> quit\n")' in the exemption.
+#  Three passes, one class: a silence oracle built as a whitelist has, by construction, a shape to hide in.  So the
+#  oracle is now the TRANSCRIPT ITSELF: every command owes an exact, in-order sequence of lines computed from the
+#  command alone (owed() below), the snapshot is taken before `quit' is typed (so nothing is exempt), and every CR must
+#  be the pty's CRLF.  A quiet emulator prints exactly that; anything else -- extra, missing, glued or reordered -- is
+#  the emulator speaking.  The only disguise left is a diagnostic that emits no byte (`fatal("")': EQUIVALENT).
+_HEX = re.compile(r"^0x([0-9a-f]+)$")
+_PUT = re.compile(r"^0x([0-9a-f]+): ([0-9a-f]+)$")
+_DIS = re.compile(r"^([0-9a-f]{8}):\s+([0-9a-f]{4})\s")
+
+
+def owed(cmds):
+    """The lines a quiet session prints after its first prompt, in order, as (kind, text-or-values)."""
+    code, pc, out = {}, None, []
+    for c in cmds:
+        out.append(("echo", "GXemul> " + c))
+        m = re.match(r"^r\d+=0x([0-9a-f]+)$", c)
+        if m:
+            out.append(("hex", int(m.group(1), 16)))
+            continue
+        m = re.match(r"^pc=0x([0-9a-f]+)$", c)
+        if m:
+            pc = int(m.group(1), 16)
+            out.append(("hex", pc))
+            continue
+        m = re.match(r"^put ([hw]) 0x([0-9a-f]+), 0x([0-9a-f]+)$", c)
+        if m:
+            a, v = int(m.group(2), 16), int(m.group(3), 16)
+            if m.group(1) == "h":
+                code[a] = v
+            out.append(("put", (a, v)))
+            continue
+        m = re.match(r"^step (\d+)$", c)
+        if m:
+            for _ in range(int(m.group(1))):
+                out.append(("disasm", (pc, code.get(pc))))
+                pc += 2
+            continue
+        if re.match(r"^print r\d+$", c):
+            out.append(("value", None))        # WHICH value is the rows' business; that it is one hex line is this
+            continue
+        raise ValueError("owed(): no transcript model for command %r" % c)
+    return out
+
+
+def _is(kind, want, ln):
+    if kind == "echo":
+        return ln == want
+    if kind in ("hex", "value"):
+        m = _HEX.match(ln)
+        return bool(m) and (want is None or int(m.group(1), 16) == want)
+    if kind == "put":
+        m = _PUT.match(ln)
+        return bool(m) and (int(m.group(1), 16), int(m.group(2), 16)) == want
+    if kind == "disasm":
+        m = _DIS.match(ln)
+        return bool(m) and (int(m.group(1), 16), int(m.group(2), 16)) == want
+    return False
+
+
+def noise(t, cmds):
+    """Differences between the pre-`quit' transcript `t' and the exact transcript `cmds' owe.  Empty = silent."""
     i = t.find("GXemul> ")
     raw = t[i:] if i >= 0 else t
-    body = raw.replace("\r", "").split("\n")
-    bad = [ln for ln in body if not any(p.match(ln) for p in _QUIET)]
-    if cmds is not None:
-        want_hex = sum(1 for c in cmds if re.match(r"^(r\d+=|pc=|print )", c))
-        want_put = sum(1 for c in cmds if c.startswith("put "))
-        want_dis = sum(int(c.split()[1]) for c in cmds if c.startswith("step "))
-        got_hex = sum(1 for ln in body if _QUIET[2].match(ln))
-        got_put = sum(1 for ln in body if _QUIET[3].match(ln))
-        got_dis = sum(1 for ln in body if _QUIET[4].match(ln))
-        #  the `quit' echo is not counted: it is typed after the last command and may miss the read window on a
-        #  loaded host, which must not red a clean session
-        got_prm = sum(1 for ln in body if ln.startswith("GXemul> ") and ln != "GXemul> quit")
-        blanks = sum(1 for ln in body[:-1] if ln == "")
-        bare_cr = raw.count("\r") - raw.count("\r\n")
-        for name, g, w in (("hex", got_hex, want_hex), ("put", got_put, want_put), ("disasm", got_dis, want_dis),
-                           ("prompt", got_prm, len(cmds)), ("interior blank", blanks, 0), ("bare CR", bare_cr, 0)):
-            if g != w:
-                bad.append("%s lines %d, commands owe %d" % (name, g, w))
+    lines = raw.replace("\r", "").split("\n")
+    body, tail = lines[:-1], lines[-1]
+    exp = owed(cmds)
+    bad = []
+    for k, (kind, want) in enumerate(exp):
+        if k >= len(body):
+            bad.append("line %d missing: owed %s" % (k, kind))
+            break
+        if not _is(kind, want, body[k]):
+            bad.append("line %d is %r, owed %s" % (k, body[k], kind))
+            break
+    if not bad and len(body) > len(exp):
+        bad.append("%d surplus line(s), first %r" % (len(body) - len(exp), body[len(exp)]))
+    #  after the last command the debugger may already have printed the next prompt, or not yet (a read window)
+    if tail not in ("", "GXemul> "):
+        bad.append("trailing %r" % tail)
+    bare_cr = raw.count("\r") - raw.count("\r\n")
+    if bare_cr:
+        bad.append("bare CR x%d" % bare_cr)
     return bad
 
 
@@ -224,17 +283,20 @@
     sys.stdout.flush()
 
 
-#  The READ sessions: every one of them must be silent -- noise() finds no line outside the quiet grammar and no
-#  surplus in any line class.  A write to MAPLE_DMAADDR or MAPLE_ENABLE prints nothing (the former's debug() is
+#  The READ sessions: every one of them must be silent -- noise() finds its pre-`quit' transcript to be exactly the
+#  owed one.  A write to MAPLE_DMAADDR or MAPLE_ENABLE prints nothing (the former's debug() is
 #  commented out) and every other register read in these sessions is a quiet arm, so ANY extra output is the read
 #  speaking.  Keyed on the channel, never on one literal string (Fable pass 1: the literal form is vacuous by
 #  construction against a reworded or latched announce; §F2, codex: nor on a line SHAPE alone).
 READS = []
 
 
+SNAP = ""
+
+
 def rsession(cmds):
     t, how = session(cmds)
-    READS.append((t, how, cmds))
+    READS.append((SNAP, how, cmds))
     return t, how
 
 
@@ -302,15 +364,21 @@
         "r3=0x55aa55aa", "r4=0x%x" % MARKER] + run([0x6212, 0x2432], CODE) + load32(MARKER, CODE + 0x20, dest=5)
 t, how = rsession(cmds)
 row("marker survive", printed(t, "r5"), 0x55aa55aa, "the store after the read executes")
-row("exit status", how, "exit0", "the session ends by `quit'")
+row("exit status", how, "exit0", "ends by `quit' (an exit(0) at the read: marker survive)")
 
 # -- clause (e) cells, L1 (cheap, disclosed by class) ----------------------------------------------------------------
-t, how = rsession(load32(MAPLE_DMAADDR, CODE))
+#  A SECOND read in the zero and all-ones sessions (Fable pass 2): a post-copy side effect that SETS a bit (`d->dmaaddr
+#  |= bit') shows on the zero field, one that CLEARS a bit on the all-ones field -- the single-bit generating set of
+#  the read-side-effect class, which the VAL_A triple session sees only for bits VAL_A does not already hold.
+t, how = rsession(load32(MAPLE_DMAADDR, CODE, dest=2) + load32(MAPLE_DMAADDR, CODE + 0x20, dest=3))
 row("initial zero", printed(t, "r2"), 0x0, "fresh device: field is zero")
+row("zero reread", printed(t, "r3"), 0x0, "the read set no bit")
 t, how = rsession(store32(MAPLE_DMAADDR, VAL_4, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
 row("read four", printed(t, "r2"), VAL_4, "the value 4")
-t, how = rsession(store32(MAPLE_DMAADDR, VAL_ONES, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20))
+t, how = rsession(store32(MAPLE_DMAADDR, VAL_ONES, CODE) + load32(MAPLE_DMAADDR, CODE + 0x20, dest=2)
+                  + load32(MAPLE_DMAADDR, CODE + 0x40, dest=3))
 row("read all ones", printed(t, "r2"), VAL_ONES, "every bit set")
+row("ones reread", printed(t, "r3"), VAL_ONES, "the read cleared no bit")
 #  The CONSUMER's partitions (Opus pass 2, measured): maple_do_dma_xfer() tests `!d->enable' and `addr & 0x1f', and
 #  every other row writes a value with nonzero low five bits on a device never enabled -- so a read DECLINED or KILLED
 #  only for a 32-byte-aligned value, or only once enabled, scored 16/16.  An aligned nonzero value is exactly what a
@@ -336,7 +404,7 @@
 
 # -- silence over every read session, FLOOR ---------------------------------------------------------------------------
 noisy = [n for n in (noise(t, c) for t, _, c in READS) if n]
-row("read silent", "%d/%d" % (len(noisy), len(READS)), "0/%d" % 12, "read sessions with ANY off-grammar line")
+row("read silent", "%d/%d" % (len(noisy), len(READS)), "0/%d" % 12, "read sessions whose transcript is not the owed one")
 for n in noisy[:3]:
     print("    noise: %r" % n[:2])
 
```

## QUESTIONS

1. **Is there a diagnostic — or any edit to the fixed read arm — that the exact-transcript oracle cannot see?**  Name
   the exact C text and the session transcript it would produce.  Consider: output with no newline that lands INSIDE
   a line the oracle does not fully compare (a disassembly line is compared only on address and opcode — its mnemonic
   and comment are not; a `print` line only on being one hex line); output that arrives after the snapshot (a latched
   diagnostic deferred to exit, `atexit`, stderr buffering); output on a channel the pty never carries; output that
   REPLACES rather than adds.  For each, say whether it is reachable from a C edit to this arm, and whether a row
   could observe it.
2. **Is the oracle itself sound?**  Any way a CLEAN session could fail it (a false red under load: the 1.2 s tail
   window, a split read, the first prompt), or a DEAD session pass it?
3. **Does the repair chain close?**  State the denominator you swept.  If CLOSES, say what a future escape would be:
   "outside the contract, as stated" or "a breach of it".
4. **WHICH OF MY CLAIMS ABOVE IS WRONG?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
