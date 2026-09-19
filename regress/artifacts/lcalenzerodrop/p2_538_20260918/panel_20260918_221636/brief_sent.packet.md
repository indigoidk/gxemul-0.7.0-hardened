# `#538` PASS 2 -- the lane-class closure of `#530`'s width row.  DOES IT CLOSE THE CHAIN?

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  **VERDICT LINE FIRST.**  **THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** at HEAD `cdbe7d7`
plus the working-tree diff inlined below (detector-only: no product line changes).  Pristine-2021 copies elsewhere under
the project root are NOT this fork.  **If you cannot read files, that is expected** -- the diff, the predictions and the
measured table are all inlined; name any premise you cannot settle.

**Seats that read files: read ONLY** `GXEMUL-SEC/regress/lca_widewrite_probe.py`, `GXEMUL-SEC/src/devices/dev_lca.c`,
`GXEMUL-SEC/src/core/memory.c` (store_buf) and `GXEMUL-SEC/regress/artifacts/lcalenzerodrop/closure538_20260918/PRETABLE.out`.
Do not browse the rest of `regress/`, `regress/artifacts/` or `tools/`.

    VERDICT: CLOSES | DOES NOT CLOSE -- <one line naming the deciding item>

**ONE MORE THING IN THE WORKING TREE, AND IT IS NOT THIS ROUND:** `src/devices/dev_lca.c` also carries an UNRELATED, UNCOMMITTED fix from round `#540` -- `CACHE_NONE` -> `CACHE_NONE | PHYSICAL` on the two nested `cpu->memory_rw` forwards in `DEVICE_ACCESS(lca_isa)`, plus its comment.  It changes the forward's ADDRESS CLASS (physical, not virtual) and nothing about `ofs`, `len` or the write arm's `data[ofs]`.  Every measurement in §3 was taken on 8bd97e4's dev_lca.c, before that edit.  Review THIS diff; ignore the `PHYSICAL` tokens.


## 1. WHAT THIS ROUND IS, AND THE RULE IT MUST MEET

`#530` (8bd97e4) shipped a one-cell width row: one PROM GETENV write of 16 bytes at (C=16, k=0, lane 3).  Its pass 2
measured seven one-edit variants that row cannot see, and the flagship ruled at the §F2 pass:

* **ONE floor breach, `vc`** -- `&& (len <= 8 || (P & 3) == 3)` services wide writes at the rowed lane only.  LANE is a
  floor axis because the body's `data[ofs]` distinguishes all four lanes, so the floor is {write arm} x {lane 0..3}.
* The other six are clause-(e) debt, disclosed against classes the parent header already ruled (`p_port10` for ports,
  `lcaisasize` for the discarded sparse bits), plus width thresholds above 16 and chunk position.
* The popular two-cell fix {mc2, kbc1024} is a COVERING, not a closure: a lane-1-only exemption escapes both.
* **The chain closes on the first VALID pass on THIS diff that verifies the enumeration -- diff delivered, roster
  complete, zero WITH its denominator -- and specifically shows the lane-1 escape killed and no lane cell open.**

## 2. THE DIFF (`git diff`, working tree against `cdbe7d7`; 6 hunks)

```diff
diff --git a/regress/lca_isalane_probe.py b/regress/lca_isalane_probe.py
index bd98f0d..1112fa1 100644
--- a/regress/lca_isalane_probe.py
+++ b/regress/lca_isalane_probe.py
@@ -168,8 +168,14 @@
 #      base 3/3 (SCR <- s[3] = 'D');  `&& len <= 8' 2/3;  `len == 0 || len > 8' 2/3
 #  Both mutants that swept THIS file's 352 rows clean are killed there.  Kept in a SEPARATE file on
 #  purpose: folding it in here would move 352 measured rows and owe a full re-measure to show nothing
-#  shifted, for no gain in coverage.  The width cell is therefore COVERED, not merely disclosed -- but
-#  by that file, so an edit that deletes it re-opens this cell and this header says where to look.
+#  shifted, for no gain in coverage.
+#  *** CORRECTED BY #538 -- AN L4, RULED AT #530's PASS 2.  This said "The width cell is therefore COVERED,
+#  not merely disclosed", which was true of the two variants named above and false of the class: that file's
+#  first version rowed ONE of the four byte lanes, and a variant servicing wide writes at lane 3 only swept
+#  it 3/3 (artifacts/lcalenzerodrop/opus_p2_20260918/RESULTS.txt).  #538 rows all four lanes at C=16, k=0,
+#  and that file's own CONTRACT enumerates what it still does not catch, citing THIS header's p_port10 and
+#  lcaisasize classes by name.  The width floor lives in that file, so an edit that deletes it re-opens the
+#  floor, and this header says where to look. ***
 #  `lcawidefold' (only s[3] of a 16-byte store reaches the port) REOPENS: that row IS the guest its
 #  reopen condition names.
 #  `len == 0' is refused and DISCLOSED (no producer); a DIRECTION swap (a store forwarded as a read, or the reverse)
diff --git a/regress/lca_widewrite_probe.py b/regress/lca_widewrite_probe.py
index a6983c3..3a6cdf9 100644
--- a/regress/lca_widewrite_probe.py
+++ b/regress/lca_widewrite_probe.py
@@ -1,57 +1,76 @@
 #!/usr/bin/env python3
-"""lca_widewrite_probe.py -- the width row #530 owed (lcalenzerodrop).  MEASURED 2026-09-18.
-
-WHAT IT PINS.  `#530`'s instruction-driven detector, lca_isalane_probe.py, cannot express a store wider
-than 8 bytes -- the widest Alpha store, STQ, is 8 bytes (its own header, :148-151).  So a guard that
-declines only len > 8 swept all 352 of its rows: `#530`'s KILLLEN8 leg (`len == 0 || len > 8') and the
-`&& len <= 8' write-arm conjunct both scored 352/352.  CLOSE6_VERDICT.md pre-committed the disposition:
-*escapes AND len > 8 is guest-reachable -> L2, add a len > 8 row in-round.*  This is that row.
-
-THE PATH -- the NON-INSTRUCTION one, because no instruction can reach it:
-    CALL_PAL 0x3fffffe      the word machine_alpha.c:189 stores at PROM_ENTRY_PADDR;
-                            cpu_alpha_palcode.c:519-520 dispatches it to alpha_prom_call
-      a0 = 0x22             PROM_R_GETENV          (thirdparty/alpha_prom.h:69)
-      a1 = 0x8              PROM_E_BOOTED_OSFLAGS  (:85) -> s = boot_string_argument, set by -o
-      a2 = k0(SP(0x2ff))    the ns16550 SCR, 64-bit K0SEG, loaded via put d + LDQ
-      a3 = 16               len = min(a3, strlen(s)+1) = min(16, 17) = 16   (palcode.c:141-143)
-      ra = the next insn    alpha_prom_call RETURNS THROUGH ra (palcode.c:153) -- see RUN 1 below
-    -> store_buf(cpu, a2, s, 16) -> ONE memory_rw(a2, 16): 0x5fe0 fails 1024/256/64 alignment and
-       passes 16 (memory.c:839-852) -> lca_isa: port 0x2ff, ofs = (0x2ff & 3) % 16 = 3 -> s[3] = 'D'
-
-MEASURED (regress/artifacts/lcalenzerodrop/widewrite_20260918/logs/TABLE.out; every value predicted
-in PRETABLE.out at 14:59:49, BEFORE any run, and every value matched):
-    base        3/3   wide getenv = 0x44 ('D')
-    M2_len8     2/3   wide getenv = 0x5a (the PRESET: the store fell into the READ arm)
-    KILLLEN8    2/3   wide getenv = 0x5a (the PRESET: `return 0' -> MEMORY_ACCESS_FAILED, and there
-                                          is no Alpha exception branch in memory_rw.c:603-624)
-
-RUN 1 WAS AN L1 CONSTRUCTION FAILURE and is preserved, not hidden (logs/run1_L1_no_return_address/):
-the CALL_PAL was executed inline WITHOUT loading ra, so the PROM call "returned" to address 0, phase 4
-never ran, and every binary read 0 alike.  The PRETABLE had pre-committed that a base leg short of 3/3
-means the ROW is broken, not the fix -- which is how it was read.
-
-CONTRACT (clause e).  DESIGNED TO CATCH: any guard that declines a len > 8 WRITE to lca_isa, in either
-the guard form or the write-arm-conjunct form.  DISCLOSED, NOT CAUGHT: (i) which of the 16 bytes
-reaches the port -- only s[3] does, and the other 15 are dropped; that is `lcawidefold', whose reopen
-condition ("a guest found issuing GETENV into the ISA window") THIS ROW MEETS; (ii) the READ side --
-store_buf only writes, and no wide-read producer was found, so a read twin would drive a path no guest
-reaches; (iii) widths 64/256/1024 -- 16 was measured; the others share the same `len > 8' predicate.
-
-WITNESS vs DETECTOR.  This is a DETECTOR (green once the defect is gone).  #530's rung-3 WITNESS is
-lca_isalane_probe.py's 13/16 on the committed build.
+"""lca_widewrite_probe.py -- #530's width row, CLASS-CLOSED by #538: the four C=16 WRITE lanes.
+
+WHAT IT PINS.  `#530`'s instruction-driven detector, lca_isalane_probe.py, cannot express an access wider than 8 bytes:
+the widest Alpha store, STQ, is 8.  The only guest producer of a wider access to DEVICE_ACCESS(lca_isa) is the PROM
+GETENV callback (CALL_PAL 0x3fffffe), which copies a host string into guest memory with store_buf() -- chunks of
+1024/256/64/16/4/1 bytes, each only at an address aligned to its size, each reaching the handler whole.  This file drives
+that producer at FOUR cells, one per byte lane, ONE ISOLATED EMULATOR SESSION PER CELL: a variant that drops a wide store
+into the read arm writes zeros into store_buf's SOURCE (the emulator's own boot string), so cells sharing a session would
+see a shorter string -- one session each removes the ordering question entirely.
+
+HISTORY, because the first version's claim was wrong.  #530 (8bd97e4) shipped ONE cell, (C=16, k=0, lane 3), and said
+"any guard that declines a len > 8 WRITE" was caught.  Its pass 2 measured seven one-edit variants that pass that cell
+(regress/artifacts/lcalenzerodrop/opus_p2_20260918/, 102 legs), and the flagship ruled (#530 §F2, fable5 R1/R2) that ONE of
+them is a floor breach: `&& (len <= 8 || (P & 3) == 3)` services wide writes at the rowed lane only.  LANE is a floor axis
+because the body's `data[ofs]' distinguishes all four lanes; so the floor is {write arm} x {lane 0, 1, 2, 3}, and #538
+rows the other three.  Row demand is per LANE, not per variant: the lane-1 exemption `&& (len <= 8 || (P & 3) != 1)`,
+which the popular two-cell covering {mc2, kbc1024} misses, is red here at `low16'.
+
+CONTRACT (clause e).  DESIGNED TO CATCH, at each of the four byte lanes (C=16, k=0): any variant that DECLINES, REFUSES
+or MISROUTES a len > 8 WRITE -- the guard form (`len == 0 || len > 8'), the write-arm-conjunct form (`&& len <= 8'), a
+LANE-conditioned form (`&& (len <= 8 || (P & 3) == L)', or `!= L', for any lane L), and a wrong lane byte (`data[0]'
+for `data[ofs]', red at lanes 1-3).
+DISCLOSED, NOT CAUGHT -- each with its warrant, and the named classes are ALREADY RULED in the parent's header:
+  (i)    width thresholds above 16 (`len <= 16', `<= 64', `<= 256'): the body tests `len' only against 0 (joint cells);
+         each is MEASURED killed at a wider cell in opus_p2_20260918 (va, vb, vw64, vw256), not rowed here.
+  (ii)   port-conditioned refusals: the parent's p_port10 class -- the body never compares the port to a constant.  A
+         refusal below port 0x200 happens to red `low16' (port 0x21); that is incidental, not a contract claim.
+  (iii)  the discarded sparse bits a<4:0> (k): the parent's lcaisasize class -- a k-keyed or alignment-keyed refusal.
+  (iv)   chunk position >= 2 of a multi-chunk write: the handler holds no state across calls.
+  (v)    the READ direction: no wide-read producer exists (store_buf only writes; PROM PUTS reads single bytes).
+  (vi)   delivery of a wide chunk's NON-LANE bytes: `lcawidefold' (reopened; the drop count is alignment-dependent).
+  (vii)  data values: a wide chunk never forwards 0 -- argv strings and basenames carry no NUL, and the lane byte sits at
+         offset <= 3 while the terminator is at >= 15.
+  (viii) forward COUNT: every row here reads a LATCH, so a len > 8-gated duplicate or added forward is invisible.
+
+WANT IS DERIVED, NEVER TYPED: sim_store_buf() replays src/core/memory.c's store_buf chunking on (a2, len) and applies the
+SHIPPED handler rule (byte = s[chunk offset + (P & 3) % C], forwarded to port P) to every chunk; the last byte landing on
+a register's port is that register's WANT.  THE WIDTH IS PINNED BY CONSTRUCTION, NOT BY VALUE: no forwarded byte can
+distinguish a 16-byte chunk from a 4-byte one at the same address (both forward s[lane]), so each cell declares its chunk
+list and the probe asserts it -- and asserts that the chunk landing on each observed register is wider than 8.
+
+HARNESS RULES, each from a defect of the first version:
+  * a session is RETRIED once, with tripled patience, only if its prints are missing AND the emulator was still ALIVE --
+    as the parent's dsession() does; the first version retried a DEAD session and so could record a host death as a pass.
+  * exit status is 0 only at full marks; the first version exited 0 on FAIL.
+  * the last row is an IDENTITY row pinning the row count this file emits.
+
+WITNESS vs DETECTOR.  This is a DETECTOR (green once the defect is gone).  #530's rung-3 WITNESS is lca_isalane_probe.py's
+13/16 on the pre-fix build.
+
+MEASURED 2026-09-18 -- #538's kill table, 17 legs, one isolated session per cell; every prediction was written first,
+in PRETABLE.out, whose mtime predates the frozen instrument.  Logs: regress/artifacts/lcalenzerodrop/closure538_20260918/
+logs/TABLE.out.  The instrument that ran is that directory's lca_widewrite.frozen.py; this file differs from it ONLY by
+this paragraph (`diff' the two).
+    base 13/13     M2_len8 9/13   KILLLEN8 9/13   vc 10/13      vf 10/13
+    vc_ne0 12/13 (l0w16)   vc_ne1 12/13 (low16)   vc_ne2 12/13 (l2w16)   vc_ne3 12/13 (wide)
+    ve 12/13 (low16 -- INCIDENTAL, disclosed class (ii))
+    va vb vg vt1 vt2 13/13 (disclosed (i), (iii), (iv))     vd vh 13/13 (EQUIVALENT)
+  17 of 17 as predicted, red-row sets included.  The lane-1 exemption that the covering {mc2, kbc1024} misses is red
+  at `low16' (vc_ne1).
 """
 import os, pty, re, select, sys, time
 
-BIN     = sys.argv[1]
-LABEL   = sys.argv[2] if len(sys.argv) > 2 else "?"
-MACH    = "alphabook1"
-BOOTSTR = "ABCDEFGHIJKLMNOP"          # strlen 16, so len = min(a3=16, 17) = 16
-DUMMY   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")   # as the parent
+BIN   = sys.argv[1]
+LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
+MACH  = "alphabook1"
+DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
 
-# ---- encoder, copied from lca_isalane_probe.py so the encodings are identical
-ZERO, T0, T1, T2, T3, T4 = 31, 1, 2, 3, 4, 5
-A0, A1, A2, A3 = 16, 17, 18, 19       # Alpha ABI a0..a3 = r16..r19.  NOT defined in the parent probe,
-                                      # which deliberately names only T0..T6 -- defined here, on purpose.
+# ---- encoder, copied from the parent via the first version, unchanged
+ZERO, T0, T1, T2, T3, T4, T5, T6, T7 = 31, 1, 2, 3, 4, 5, 6, 7, 8
+A0, A1, A2, A3 = 16, 17, 18, 19
+RA = 26
 def mem(op, ra, rb, disp):
     assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
     return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
@@ -60,9 +79,9 @@ def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
 def LDBU(ra, disp, rb):      return mem(0x0a, ra, rb, disp)
 def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)
 def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
-CALL_PAL_PROM = (0x00 << 26) | 0x3fffffe      # == 0x03fffffe, the word machine_alpha.c:189 stores
+CALL_PAL_PROM = (0x00 << 26) | 0x3fffffe
 
-def load_const(reg, val):                     # 32-bit only, exactly as the parent
+def load_const(reg, val):
     lo = val & 0xffff
     hi = (val >> 16) & 0xffff
     if lo >= 0x8000:
@@ -72,22 +91,23 @@ def load_const(reg, val):                     # 32-bit only, exactly as the pare
         ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
     return ops
 
-SENT = 0x0bad1d8a                             # the parent's pre-seed: a faulting load leaves it
+SENT = 0x0bad1d8a
 def sent(reg): return load_const(reg, SENT)
 
-K0SEG       = 0xfffffc0000000000
-def k0(p):  return K0SEG | p
-LCA_PCI_SIO = 0x1c0000000
-def SP(port): return LCA_PCI_SIO + (port << 5)
+K0SEG        = 0xfffffc0000000000
+def k0(p):   return K0SEG | p
+LCA_PCI_SIO  = 0x1c0000000
+LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000
+def SP(port):   return LCA_PCI_SIO + (port << 5)
+def FLAT(port): return LCA_ISA_BASE + port
 SCRATCH, CODE = 0x01020000, 0x01040000
+KBC_CMD, KBC_DAT = 0x64, 0x60
 
-# ---- harness: the parent's session(), with ONE change -- `-o BOOTSTR' -- in a separate function so
-#      the parent's 352 rows cannot be affected by it
-def session(cmds, settle, spin):
+def session(bootstr, cmds, settle, spin):
     pid, fd = pty.fork()
     if pid == 0:
         os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
-                       "-o", BOOTSTR, "0x20000000:" + DUMMY])
+                       "-o", bootstr, "0x20000000:" + DUMMY])
         os._exit(127)
     buf = ""
     def rd(t):
@@ -121,9 +141,13 @@ def session(cmds, settle, spin):
         os.close(fd)
     except OSError:
         pass
+    try:
+        os.waitpid(pid, 0)
+    except OSError:
+        pass
     return buf.replace("\r", ""), alive
 
-def build(consts, phases):                    # copied verbatim in behaviour
+def build(consts, phases):
     prog = load_const(T0, SCRATCH)
     lens = [len(prog)]
     for ops, _ in phases:
@@ -144,51 +168,119 @@ def printed(t, reg):
 
 rows = []
 def row(name, got, want, note=""):
+    assert len(name) <= 13, "row name %r exceeds 13 characters (the %%-14s column + gate pattern)" % name
     ok = (got == want)
     rows.append((name, ok))
-    print("%-14s %-24s %-24s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
+    g = got if not isinstance(got, int) else "0x%x" % got
+    w = want if not isinstance(want, int) else "0x%x" % want
+    print("%-14s %-24s %-24s %-56s %s" % (name, g, w, note, "ok" if ok else "FAIL"))
     return ok
 
-# ---- the session
-SCR, PRESET = 0x2ff, 0x5a
-WANT = ord(BOOTSTR[(SCR & 3) % 16])          # s[3] == 'D' == 0x44 -- derived, not typed in
-#  *** RUN 1 WAS AN L1 CONSTRUCTION FAILURE AND THIS IS ITS FIX. ***  alpha_prom_call ENDS WITH
-#  `cpu->pc = cpu->cd.alpha.r[ALPHA_RA]' (cpu_alpha_palcode.c:153) -- the real PROM entry is reached
-#  by `jsr', which loads ra.  Run 1 executed the CALL_PAL inline WITHOUT setting ra, so the call
-#  "returned" to address 0, phase 4 never ran, and t4 kept its initial 0 on every binary alike
-#  (logs/run1_L1_no_return_address/).  ra is now loaded with the address of the instruction AFTER the
-#  CALL_PAL -- COMPUTED FROM THE LAYOUT, not typed in, so an edit to any phase cannot silently strand it.
-RA = 26                                       # Alpha ra = r26
-p1 = [LDQ(T2, 0, T0)] + load_const(T1, PRESET) + [STB(T1, 0, T2)]           # preset the SCR
-p2 = [LDQ(T2, 0, T0)] + sent(T3) + [LDBU(T3, 0, T2)]                         # CONTROL: reads back
-p3 = (load_const(A0, 0x22) + load_const(A1, 0x8) + [LDQ(A2, 0, T0)]
-      + load_const(A3, 16) + [LDQ(RA, 8, T0), CALL_PAL_PROM])               # GETENV, 16-byte store
-p4 = [LDQ(T2, 0, T0)] + sent(T4) + [LDBU(T4, 0, T2)]                         # the SCR afterwards
-RET = k0(CODE) + 4 * (len(load_const(T0, SCRATCH)) + len(p1) + len(p2) + len(p3))
-consts = [k0(SP(SCR)), RET]                   # slot 0: the SCR; slot 8: where the PROM call returns
-phases = [(p1, None), (p2, "t3"), (p3, None), (p4, "t4")]
-
-print("lca_widewrite -- binary=%s label=%s machine=%s -o %s" % (BIN, LABEL, MACH, BOOTSTR))
-cmds = build(consts, phases)
-txt, alive = session(cmds, 3.0, 4.0)
-#  MIRRORS THE PARENT'S run(): a session whose prints did not all arrive TIMED OUT rather than
-#  measured, and is retried ONCE with tripled patience -- "the machine may be loaded".  Without this,
-#  a slow run under contention reads as a FAILED ROW: a phantom red that the row did not earn.
-retried = False
-if printed(txt, "t3") is None or printed(txt, "t4") is None:
-    retried = True
-    txt, alive = session(cmds, 3.0 * 3, 4.0 * 3)
-print("WIDEWRITE_RETRIED=%s" % ("yes" if retried else "none"))
-if os.environ.get("WIDEWRITE_RAW"):
-    open(os.environ["WIDEWRITE_RAW"], "w", encoding="utf-8").write(txt)
-
-t3, t4 = printed(txt, "t3"), printed(txt, "t4")
-row("wide alive", "alive" if alive else "died", "alive",
-    "the guest survives an inline CALL_PAL 0x3fffffe")
-row("wide live", t3, PRESET,
-    "LIVENESS + DEVICE SIGNATURE: a 1-byte store round-trips through the SCR")
-row("wide getenv", t4, WANT,
-    "a 16-byte store_buf write lands s[3] on the SCR; M2 (`&& len <= 8') leaves the PRESET")
+# ---- the producer, replayed (src/core/memory.c store_buf) + the SHIPPED lca_isa write rule
+def sim_store_buf(a, n):
+    out, off, psize = [], 0, 1024
+    while n != 0:
+        if (a & (psize - 1)) == 0:
+            while n >= psize:
+                out.append((a, psize, off)); a += psize; off += psize; n -= psize
+        psize >>= 2
+    return out                                # the trailing store_byte loop is dead: psize 1 drains it
+
+def shipped_lands(a_sparse, n, sbytes):
+    return [((a >> 5), sbytes[off + ((a >> 5) & 3) % c]) for a, c, off in sim_store_buf(a_sparse, n)]
+
+ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
+def pat(n): return (ALPH * (n // len(ALPH) + 1))[:n]
+IDENT = lambda v: v
+MSRX  = lambda v: v | 0xb0                    # the ns16550 MSR reads back OR DCD|DSR|CTS
+
+#  ---- THE CELLS
+#  name: (a3, target port, k, -o string, chunks expected, [(reg port, kind, preset, xform, row tag)])
+#  THE FLOOR, as ruled (fable5, #530 §F2, R1/R2): the four C=16 WRITE lanes at k = 0.  `wide' is the shipped
+#  cell and keeps its row names; the other three close the LANE partition that `data[ofs]' distinguishes.
+#  Each a3 = 16 against a 16-character string, so len = min(16, 17) = 16: ONE 16-byte chunk (asserted below).
+#  name     a3  port   k  -o string            chunks  [(reg port, kind, preset, xform, row tag)]
+CELLS = {
+    "wide":  (16, 0x2ff, 0, "ABCDEFGHIJKLMNOP", [16], [(0x2ff, "sp", 0x5a, IDENT, "")]),  # lane 3: ns16550 SCR
+    "l0w16": (16, 0x2fc, 0, "ABCDEFGHIJKLMNOP", [16], [(0x2fc, "sp", 0x03, IDENT, "")]),  # lane 0: ns16550 MCR
+    "low16": (16, 0x021, 0, "ABCDEFGHIJKLMNOP", [16], [(0x021, "sp", 0xff, IDENT, "")]),  # lane 1: 8259 IMR
+    "l2w16": (16, 0x2fe, 0, "ABCDEFGHIJKLMNOP", [16], [(0x2fe, "sp", 0x00, MSRX,  "")]),  # lane 2: ns16550 MSR
+}
+assert sorted(spec[1] & 3 for spec in CELLS.values()) == [0, 1, 2, 3], "the floor is ALL FOUR lanes"
+
+def run_cell(name, spec):
+    a3v, tgt, k, bootstr, chunks, regs = spec
+    sbytes = bootstr.encode("latin-1") + b"\0"
+    lenv = a3v if len(bootstr) >= a3v else len(bootstr) + 1   # alpha_prom_call: min(a3, strlen + 1)
+    a_sparse = (tgt << 5) + k
+    got_chunks = [c for _, c, _ in sim_store_buf(a_sparse, lenv)]
+    assert got_chunks == chunks, "cell %s: replayed chunks %r != declared %r -- the WIDTH is not what this cell claims" \
+        % (name, got_chunks, chunks)
+    lands = shipped_lands(a_sparse, lenv, sbytes)
+    #  THE WIDTH PIN (fable5 R2; the #530 pass-2 F10 gap).  No forwarded-byte VALUE can pin the width: a 4-byte chunk
+    #  at the same address forwards the same s[lane].  So the construction itself is asserted: the chunk that lands on
+    #  each observed register must be WIDER THAN 8, or this cell is not testing what its rows claim.
+    for a, c, off in sim_store_buf(a_sparse, lenv):
+        if any((a >> 5) == port for port, _, _, _, _ in regs):
+            assert c > 8, "cell %s: the chunk landing on port 0x%x is %d bytes -- not a wide write" % (name, a >> 5, c)
+    consts = [0, k0(SP(tgt) + k)]
+    def slot(v):
+        consts.append(v); return 8 * (len(consts) - 1)
+    res = [T3, T4, T5, T6, T7]
+    rname = {T3: "t3", T4: "t4", T5: "t5", T6: "t6", T7: "t7"}
+    plan = []
+    for port, kind, preset, xf, tag in regs:
+        if kind == "sp":
+            s_reg = slot(k0(SP(port)))
+            pre = [LDQ(T2, s_reg, T0)] + load_const(T1, preset) + [STB(T1, 0, T2)]
+            rd_ = lambda r, s_reg=s_reg: [LDQ(T2, s_reg, T0)] + sent(r) + [LDBU(r, 0, T2)]
+            arm = []
+        else:                                 # the 8042 command byte, sequenced through FLAT
+            s_cmd, s_dat = slot(k0(FLAT(KBC_CMD))), slot(k0(FLAT(KBC_DAT)))
+            pre = ([LDQ(T2, s_cmd, T0)] + load_const(T1, 0x60) + [STB(T1, 0, T2)]
+                   + [LDQ(T2, s_dat, T0)] + load_const(T1, preset) + [STB(T1, 0, T2)])
+            rd_ = lambda r, s_cmd=s_cmd, s_dat=s_dat: ([LDQ(T2, s_cmd, T0)] + load_const(T1, 0x20)
+                   + [STB(T1, 0, T2), LDQ(T2, s_dat, T0)] + sent(r) + [LDBU(r, 0, T2)])
+            arm = [LDQ(T2, s_cmd, T0)] + load_const(T1, 0x60) + [STB(T1, 0, T2)]
+        want = preset
+        for p, b in lands:
+            if p == port:
+                want = b
+        plan.append((port, xf, preset, tag, pre, rd_, arm, want))
+    phases = [(pre, None) for _, _, _, _, pre, _, _, _ in plan]
+    phases += [(rd_(res[j]), rname[res[j]]) for j, (_, _, _, _, _, rd_, _, _) in enumerate(plan)]
+    arm_all = sum((arm for _, _, _, _, _, _, arm, _ in plan), [])
+    phases.append((arm_all + load_const(A0, 0x22) + load_const(A1, 0x8) + [LDQ(A2, 8, T0)]
+                   + load_const(A3, a3v) + [LDQ(RA, 0, T0), CALL_PAL_PROM], None))
+    n = len(plan)
+    phases += [(rd_(res[n + j]), rname[res[n + j]]) for j, (_, _, _, _, _, rd_, _, _) in enumerate(plan)]
+    consts[0] = k0(CODE) + 4 * (len(load_const(T0, SCRATCH)) + sum(len(o) for o, _ in phases[:2 * n + 1]))
+    cmds = build(consts, phases)
+    names = [rname[r] for r in res[:2 * n]]
+    txt, alive = session(bootstr, cmds, 3.0, 4.0)
+    retried = False
+    if alive and any(printed(txt, x) is None for x in names):   # F6: never retry a session that DIED
+        retried = True
+        txt, alive = session(bootstr, cmds, 9.0, 12.0)
+    print("  cell %-8s a3=%d len=%d a2=SP(0x%x)+%d chunks=%s retried=%s"
+          % (name, a3v, lenv, tgt, k, got_chunks, "yes" if retried else "none"))
+    if os.environ.get("WIDEWRITE_RAW"):
+        open(os.environ["WIDEWRITE_RAW"] + "." + name, "w", encoding="utf-8").write(txt)
+    row("%s alive" % name, "alive" if alive else "died", "alive",
+        "the guest survives the inline CALL_PAL 0x3fffffe")
+    for j, (port, xf, preset, tag, _, _, _, want) in enumerate(plan):
+        row(("%s live%s" % (name, tag)).strip(), printed(txt, rname[res[j]]), xf(preset),
+            "ROUND-TRIP CONTROL: preset 0x%02x round-trips through port 0x%x" % (preset, port))
+    for j, (port, xf, preset, tag, _, _, _, want) in enumerate(plan):
+        row(("%s getenv%s" % (name, tag)).strip(), printed(txt, rname[res[n + j]]), xf(want),
+            "len %d: the shipped rule puts 0x%02x on port 0x%x" % (lenv, want, port))
+
+print("lca_widewrite -- binary=%s label=%s machine=%s cells=%s" % (BIN, LABEL, MACH, " ".join(CELLS)))
+for name, spec in CELLS.items():
+    run_cell(name, spec)
+EXPECT_ROWS = 3 * len(CELLS) + 1               # alive, live, getenv per cell, plus this row
+row("row count", len(rows) + 1, EXPECT_ROWS, "IDENTITY: the row count this file emits")
 ok = sum(1 for _, o in rows if o)
 print("WIDEWRITE_RESULT=%d/%d" % (ok, len(rows)))
 print("WIDEWRITE_DONE")
+sys.exit(0 if ok == len(rows) else 1)
```

## 3. MEASURED -- the kill table (`logs/TABLE.out`), every prediction written first in PRETABLE.out

```
base WIDEWRITE_RESULT=13/13 done=1 red=[]
M2_len8 WIDEWRITE_RESULT=9/13 done=1 red=[wide getenv,l0w16 getenv,low16 getenv,l2w16 getenv,]
KILLLEN8 WIDEWRITE_RESULT=9/13 done=1 red=[wide getenv,l0w16 getenv,low16 getenv,l2w16 getenv,]
vc WIDEWRITE_RESULT=10/13 done=1 red=[l0w16 getenv,low16 getenv,l2w16 getenv,]
vc_ne0 WIDEWRITE_RESULT=12/13 done=1 red=[l0w16 getenv,]
vc_ne1 WIDEWRITE_RESULT=12/13 done=1 red=[low16 getenv,]
vc_ne2 WIDEWRITE_RESULT=12/13 done=1 red=[l2w16 getenv,]
vc_ne3 WIDEWRITE_RESULT=12/13 done=1 red=[wide getenv,]
vf WIDEWRITE_RESULT=10/13 done=1 red=[wide getenv,low16 getenv,l2w16 getenv,]
va WIDEWRITE_RESULT=13/13 done=1 red=[]
vb WIDEWRITE_RESULT=13/13 done=1 red=[]
ve WIDEWRITE_RESULT=12/13 done=1 red=[low16 getenv,]
vg WIDEWRITE_RESULT=13/13 done=1 red=[]
vt1 WIDEWRITE_RESULT=13/13 done=1 red=[]
vt2 WIDEWRITE_RESULT=13/13 done=1 red=[]
vd WIDEWRITE_RESULT=13/13 done=1 red=[]
vh WIDEWRITE_RESULT=13/13 done=1 red=[]
```

17 of 17 legs as predicted, red-row sets AND register values included (e.g. `vf` put 0x41/0x41/0xf1 at wide/low16/l2w16,
exactly the misrouted s[0] PRETABLE named; `vc`/`M2_len8` left the presets 0x5a/0x03/0xff/0xb0 in place).  The baseline
was named and `cmp`'d (SEC `dev_lca.c` == 8bd97e4's), 16 variant binaries were built in a scratch clone (every one
differs from base), and the clone was restored before any leg ran.

## 4. SETTLED PREMISES (with their warrants -- challenge them if you can)

* `ofs = (relative_addr & 3) % len`, and the write arm forwards `data[ofs]` -- dev_lca.c DEVICE_ACCESS(lca_isa).
* store_buf chunks {1024, 256, 64, 16, 4, 1}, each only at an address aligned to its size, each reaching the handler
  whole; GETENV writes `min(a3, strlen(s)+1)` bytes -- measured on #530 (352 legs) and #538 (this table).
* The lane cells are one session each because a read-arm fall-through writes zeros into store_buf's SOURCE.

## 5. QUESTIONS

**Q1 -- DOES IT CLOSE?**  Enumerate the floor as ruled ({write arm} x {lane 0, 1, 2, 3} at C=16) and, for EACH cell,
name the row that pins it and the variant in §3 that proves the row can go red.  A cell with no red-capable row is an
open cell: name it.  Give your zero WITH its denominator (cells checked / cells in the floor).

**Q2 -- THE CONTRACT.**  Is each of the eight disclosed classes (i)-(viii) in the header honestly warranted, and is any
of them actually INSIDE the ruled floor (i.e. mis-disclosed)?  Is anything the contract claims to catch NOT backed by
a measured red in §3?

**Q3 -- THE HARNESS FIXES.**  The retry now fires only on a session that is still ALIVE, and the exit status is non-zero
on FAIL.  Are both right as written?  Is there a path on which a host death is still scored as a pass?

**Q4 -- THE PARENT'S L4.**  The diff corrects `lca_isalane_probe.py`'s "The width cell is therefore COVERED, not merely
disclosed" in place.  Is the correction itself accurate, or does it overclaim in the other direction?

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
