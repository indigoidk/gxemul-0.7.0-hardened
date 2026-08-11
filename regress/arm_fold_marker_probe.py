#!/usr/bin/env python3
"""#358: fold-fired markers for netbsd_copyin / netbsd_copyout.

WHY THESE TWO FOLDS AND WHY NOW. Both replace six user-mode transfers with one C
function whose registers, read/written addresses and instruction billing are
IDENTICAL to the instructions they replace, so a row asserting their result
passes whether or not the fold ever fires. Until #357 there was exactly one
witness: the load/store template masked its base writeback while these folds did
not, so an unaligned base gave r0 = 0x10019 folded against 0x10018 genuine.
#357 corrected the template -- the folds were right all along -- and that
one-bit detector disappeared with it. These two folds also had NO harness rows of
any kind, so #358 adds the marker and this probe adds the first rows.

THE ROWS ARE FREE-RUNNING, AND THAT IS NOT A STYLE CHOICE. Three measured facts,
each of which independently breaks a plausible-looking row:

  - STEPPING UN-FOLDS THE SLOT. A `step` onto a fold slot re-translates it
    UNCOMBINED, so the step executes a plain instruction and no marker appears.
    A row driven with `step` therefore measures the genuine sequence while
    believing it measured the fold. (This is also why an earlier pc-stride
    experiment here read pc + 4: not "a breakpoint suppresses the fold", which
    was the first guess, but stepping destroying the thing it would measure.)
  - A BREAKPOINT INSIDE THE LOOP GIVES ZERO FOLDS ON A HEALTHY BINARY. Measured
    over 8 passes: breakpoint after the sequence gives 1 matcher install and 7
    folds; breakpoint inside gives 8 installs and 0 folds, because the block is
    re-translated every pass. That row would read exactly like a dead fold, and
    the signature is invisible without instrumenting the matcher.
  - A BREAKPOINT ANYWHERE DISABLES READ-AHEAD, so the combiner installs only
    AFTER the entry slot has already dispatched once, making the fold count
    `passes - 1` rather than `passes`. Any row's expected count must be a number
    derived from that rule, never "greater than zero".

A breakpoint ON the entry slot is worse still: that path re-marks its own slot
for retranslation and the matchers test ic[i].f, so a fold can never install
there at all.

TWO PASSES ARE REQUIRED. The folds gate on is_userpage, which only an access
carrying the user-access flag sets -- and that access is the general handler the
fold's own bail-out delegates to. So pass 1 always runs genuinely and sets the
bit; only pass 2 and later can fold.

PAGE LAYOUT IS LOAD-BEARING. The user page must differ from the code page,
because instruction translation updates the code page's entry WITHOUT the user
flag and the translation layer clears the bit before re-setting it. Code 0x8000,
user data 0x10000 (loads) / 0x11000 (stores), and nothing is published to memory.
Measured deterministic: 5 consecutive runs gave identical results.

EACH FOLD GETS A PAIR, so neither row can be vacuous in either direction:
  fires (DISC) -- combining on, marker present, AND the verbosity echo present.
                  The echo matters: a session whose verbosity raise silently
                  failed would report zero markers and look exactly like a dead
                  fold, so a row that only counted markers could pass for the
                  wrong reason. It also asserts the six transferred values, so
                  the row proves the work happened, not merely that a line was
                  printed.
  quiet (PIN)  -- default verbosity, zero markers. Must use continue/free-run,
                  NEVER `step`: single-step BYPASSES the verbosity gate, so a
                  stepped session prints markers at default verbosity and this
                  row would fail for a reason that has nothing to do with the
                  fold.

Proven non-vacuous before shipping, on a scratch tree built from this exact
source with ONLY this fold's arming line removed and combining otherwise
enabled: markers 0 with the arming gone, 1 with it present, verbosity confirmed
raised in both. That isolates the fold's own arming rather than all combining,
which `-J` alone would not.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
CODE = 0x8000
LOADSRC = 0x10000          # user page read by copyin
STOREDST = 0x11000         # user page written by copyout

#  Every encoding below was confirmed through the emulator's own `unassemble`
#  before use. The six-transfer register ORDER is fixed by the matchers, which
#  pin each transfer's register, and by the arming iword of the sixth.
#    copyin : ldrt sl,fp,r6,r7,r8,r9 from [r0],#4   arming 0xe4b09004
#    copyout: strt r8,r9,sl,fp,r6,r7 to  [r1],#4    arming 0xe4a17004
COPYIN = [
    0xE3A03001,   # mov  r3,#1            two passes
    0xE3A00801,   # L: mov r0,#0x10000    user page, distinct from code
    0xE4B0A004,   # ldrt sl,[r0],#4       <- fold entry slot
    0xE4B0B004,   # ldrt fp,[r0],#4
    0xE4B06004,   # ldrt r6,[r0],#4
    0xE4B07004,   # ldrt r7,[r0],#4
    0xE4B08004,   # ldrt r8,[r0],#4
    0xE4B09004,   # ldrt r9,[r0],#4       arms COMBINE(netbsd_copyin)
    0xE2533001,   # subs r3,r3,#1
    0x5AFFFFF6,   # bpl -> word 1
    0xEAFFFFFE,   # b .
]

COPYOUT = [
    0xE3A03001,   # mov  r3,#1
    0xE3A01A11,   # L: mov r1,#0x11000    user page for the stores
    0xE4A18004,   # strt r8,[r1],#4       <- fold entry slot
    0xE4A19004,   # strt r9,[r1],#4
    0xE4A1A004,   # strt sl,[r1],#4
    0xE4A1B004,   # strt fp,[r1],#4
    0xE4A16004,   # strt r6,[r1],#4
    0xE4A17004,   # strt r7,[r1],#4       arms COMBINE(netbsd_copyout)
    0xE2533001,   # subs r3,r3,#1
    0x5AFFFFF6,   # bpl -> word 1
    0xEAFFFFFE,   # b .
]


def session(prog, verbose, seed_regs=None, extra=None, bseed=None):
    """Free-running two-pass session. Returns (marker_count, verb_took, regs)."""
    stub = "/tmp/r104f_stub.bin"
    with open(stub, "wb") as f:
        f.write((0xE1A00000).to_bytes(4, "little"))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-A"] + (extra or []) +
                  ["-E", "testarm", "-M", "64", "0x%x:%s" % (CODE, stub)])
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait_from(mark, timeout=30):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if len(buf) > mark and buf[mark:].rstrip().endswith("GXemul>"):
                return True
        return False

    def send(sx, timeout=30):
        mark = len(buf)
        b = (sx + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait_from(mark, timeout)
        return buf[mark:]

    if not wait_from(0, 60):
        os.kill(pid, 9); os.waitpid(pid, 0)
        return None

    for i in range(8):
        send("put w 0x%x, 0x%08x" % (LOADSRC + 4 * i, 0x11223344 + i))
    #  #361: BYTE seeding, deliberately. `put b` goes through memory_rw with
    #  CACHE_NONE | NO_EXCEPTIONS, so unlike `put w` it does NOT warm the
    #  translation mapping -- measured. The scanc rows warm explicitly with a
    #  guest load through an unpinned base instead, so they do not depend on a
    #  side effect of the seeding width either way.
    for a, v in (bseed or []):
        send("put b 0x%x, 0x%x" % (a, v))
    for r, v in (seed_regs or {}).items():
        send("%s=0x%x" % (r, v))
    for i, iw in enumerate(prog):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    send("pc=0x%x" % CODE)
    if verbose:
        send("verbosity cpu 3")

    #  The program parks in `b .`, so `continue` never returns a prompt on its
    #  own and every later command would sit out its own timeout -- the first
    #  revision of this probe took minutes per session and had to be killed.
    #  Let it free-run briefly (both passes finish in microseconds; the fold
    #  needs pass 2, so this must NOT be a breakpoint stop), then interrupt.
    cmark = len(buf)
    os.write(fd, b"continue\n")
    t = time.time()
    while time.time() - t < 2.0:
        rd(0.3)
    if not (len(buf) > cmark and buf[cmark:].rstrip().endswith("GXemul>")):
        os.write(fd, b"\x03")
        wait_from(cmark, 15)

    regs = {}
    #  r3 and r5 are read for the #361 scanc rows: r3 is that fold's three-way
    #  value witness and r5 its run-to-the-end sentinel. Omitting them was a
    #  probe defect that reported r3 = 0 and the sentinel absent while the marker
    #  counts were already correct -- i.e. it looked like the guest had not run
    #  when in fact only the readback was missing.
    for rn in ("sl", "fp", "r6", "r7", "r8", "r9", "r0", "r1", "r3", "r5"):
        mark = len(buf)
        send("print %s" % rn)
        m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
        if m:
            regs[rn] = int(m.group(1), 16)
    mem = []
    if prog is COPYOUT:
        mark = len(buf)
        send("dump 0x%x 0x%x" % (STOREDST, STOREDST + 24))
        w = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})", buf[mark:])
        mem = [int.from_bytes(bytes.fromhex(x), "little")
               for x in "".join(w).split()][:6]
    try:
        os.write(fd, b"quit\n"); time.sleep(0.2)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    return buf, regs, mem


def count(buf, name):
    return len([l for l in buf.splitlines() if "%s: combined" % name in l])


def declined(buf, name):
    return len([l for l in buf.splitlines() if "%s: declined" % name in l])


def installed(buf, name):
    return len([l for l in buf.splitlines() if "%s: installed" % name in l])


#  #360: the A/B pair. The `quiet` rows above assert the marker is ABSENT at
#  default verbosity, which tests the verbosity gate rather than the fold. These
#  test the fold: two programs differing by ONE instruction, where the cold arm
#  must produce a DECLINE rather than merely a silence.
#
#  Why "reads zero" is not a control, measured: with verbosity off the guest ran
#  perfectly -- full six-transfer advance -- and reported zero fires AND zero
#  installs, so an install marker does not rescue it either; and a program whose
#  pc never reaches the block also reads zero. Both are indistinguishable from a
#  dead fold if the row only counts absences. So every arm below asserts the
#  verbosity echo, a positive execution witness (the six transferred values,
#  which are identical folded or not and therefore prove the program ran without
#  presuming the fold), and the exact decline count.
#
#  The cold arm replaces the warm-up with a NOP rather than deleting it, so the
#  two programs have identical layout and no address-derived expectation shifts.
NOP = 0xE1A00000            # mov r0,r0
WARM_LDRT = 0xE4B05004      # ldrt r5,[r0],#4   -- sets the user bit for the page
WARM_STRT = 0xE4A15004      # strt r5,[r1],#4   -- copyout needs a STORE: a load
                            # leaves host_store NULL and the fold declines
                            # "no-page" instead of firing, so an ldrt warm-up
                            # would make the healthy build fail its own row.


def ab_prog(fold, warm):
    """Straight-line single-pass program. No loop, no branch, no breakpoint."""
    if fold == "copyin":
        return ([0xE3A00801,            # mov r0,#0x10000
                 warm and WARM_LDRT or NOP,
                 0xE3A00801,            # mov r0,#0x10000  (re-seed)
                 0xE4B0A004, 0xE4B0B004, 0xE4B06004,
                 0xE4B07004, 0xE4B08004, 0xE4B09004,
                 0xEAFFFFFE])           # b .
    return ([0xE3A01A11,                # mov r1,#0x11000
             warm and WARM_STRT or NOP,
             0xE3A01A11,                # mov r1,#0x11000  (re-seed)
             0xE4A18004, 0xE4A19004, 0xE4A1A004,
             0xE4A1B004, 0xE4A16004, 0xE4A17004,
             0xEAFFFFFE])


print("=== #358: fold-fired markers, netbsd_copyin / netbsd_copyout ===")
rows = []

#  ---- copyin ----------------------------------------------------------------
r = session(COPYIN, True)
if r is None:
    rows.append(("A fold copyin fires", "DISC", "DEAD", False))
else:
    buf, regs, _ = r
    n = count(buf, "netbsd_copyin")
    verb = "3: DEBUG" in buf
    #  The six loaded words prove the work happened; they hold folded or not,
    #  which is why they are part of the row rather than a row of their own.
    vals_ok = (regs.get("sl") == 0x11223344 and regs.get("fp") == 0x11223345
               and regs.get("r6") == 0x11223346 and regs.get("r9") == 0x11223349)
    rows.append(("A fold copyin fires", "DISC",
                 "markers=%d verb=%s vals=%s" % (n, verb, vals_ok),
                 n >= 1 and verb and vals_ok))

r = session(COPYIN, False)
if r is None:
    rows.append(("A fold copyin quiet", "PIN", "DEAD", False))
else:
    buf, _, _ = r
    n = count(buf, "netbsd_copyin")
    rows.append(("A fold copyin quiet", "PIN", "markers=%d" % n, n == 0))

#  ---- copyout ---------------------------------------------------------------
SEED = {"r6": 0x66660001, "r7": 0x77770002, "r8": 0x88880003,
        "r9": 0x99990004, "sl": 0xAAAA0005, "fp": 0xBBBB0006}
r = session(COPYOUT, True, seed_regs=SEED)
if r is None:
    rows.append(("A fold copyout fires", "DISC", "DEAD", False))
else:
    buf, regs, mem = r
    n = count(buf, "netbsd_copyout")
    verb = "3: DEBUG" in buf
    #  Store order is r8,r9,sl,fp,r6,r7 -- pinned by the matcher. Asserting the
    #  MEMORY makes a future permutation regression visible, which a
    #  register-only row could not see.
    want = [SEED["r8"], SEED["r9"], SEED["sl"],
            SEED["fp"], SEED["r6"], SEED["r7"]]
    mem_ok = (mem == want)
    rows.append(("A fold copyout fires", "DISC",
                 "markers=%d verb=%s mem=%s" % (n, verb, mem_ok),
                 n >= 1 and verb and mem_ok))

r = session(COPYOUT, False, seed_regs=SEED)
if r is None:
    rows.append(("A fold copyout quiet", "PIN", "DEAD", False))
else:
    buf, _, _ = r
    n = count(buf, "netbsd_copyout")
    rows.append(("A fold copyout quiet", "PIN", "markers=%d" % n, n == 0))

#  ---- #360: A/B pairs ------------------------------------------------------
#  Expected counts are NUMBERS derived from the mechanism, never thresholds: a
#  straight-line single-pass block dispatches the entry slot exactly once, so a
#  warm arm is 1 fire / 0 declines and a cold arm is 0 fires / 1 decline, with
#  1 install either way because the matcher runs at translation regardless.
SEED2 = {"r5": 0x5A5A0001, "r6": 0x66660001, "r7": 0x77770002,
         "r8": 0x88880003, "r9": 0x99990004, "sl": 0xAAAA0005,
         "fp": 0xBBBB0006}
for fold, warm, want_fire, want_dec in (("copyin", True, 1, 0),
                                        ("copyin", False, 0, 1),
                                        ("copyout", True, 1, 0),
                                        ("copyout", False, 0, 1)):
    nm = "A fold %s %s" % (fold, "warm" if warm else "cold")
    r = session(ab_prog(fold, warm), True, seed_regs=SEED2)
    if r is None:
        rows.append((nm, "DISC" if warm else "PIN", "DEAD", False))
        continue
    buf, regs, _ = r
    full = "netbsd_" + fold
    f, d, i = (count(buf, full), declined(buf, full), installed(buf, full))
    verb = "3: DEBUG" in buf
    #  The execution witness: r0/r1 advanced by the full six transfers. This
    #  holds folded OR not, so it proves the program ran without presuming the
    #  fold -- which is exactly what makes the cold arm's zero meaningful.
    adv = (regs.get("r0") == 0x10000 + 24 if fold == "copyin"
           else regs.get("r1") == 0x11000 + 24)
    ok = (f == want_fire and d == want_dec and i == 1 and verb and adv)
    rows.append((nm, "DISC" if warm else "PIN",
                 "fire=%d dec=%d inst=%d verb=%s adv=%s"
                 % (f, d, i, verb, adv), ok))

#  ---- #361: xchg and netbsd_scanc, which had #358 fire markers but no rows ---
#  Every iword below was verified through the emulator's own `unassemble`.
XCHG_POS = [0xE0212002, 0xE0221001, 0xE0212002,   # eor r2,r1,r2 / r1,r2,r1 / r2,r1,r2
            0xE3A0505A, 0xEAFFFFFE]               # sentinel, park
XCHG_NEG = [0xE0211001, 0xE0211001, 0xE0211001,   # eor r1,r1,r1 x3 -- #342 rejects
            0xE3A0505A, 0xEAFFFFFE]

#  scanc: warm through r4 (a base the matcher does NOT pin) so the warm-up load
#  is not itself a fold candidate, then the pinned r1/r2 sequence. The two
#  negative arms move ONE immediate each into unmapped space; the layout is
#  otherwise identical so no address-derived expectation shifts.
def scanc_prog(str_base, tbl_base):
    return [str_base, tbl_base, 0xE3A0C0FF,       # mov r1,# / mov r2,# / mov ip,#0xff
            0xE3A04801, 0xE5D43000,               # warm the string page via r4
            0xE3A04802, 0xE5D43000,               # warm the table page via r4
            0xE5D13000,                           # ldrb r3,[r1]  <- fold entry
            0xE7D23003,                           # ldrb r3,[r2,r3]
            0xE113000C,                           # tsts r3,ip    arms the matcher
            0xE3A0505A, 0xEAFFFFFE]               # sentinel, park

SC_R1_OK, SC_R2_OK = 0xE3A01801, 0xE3A02802       # r1=0x10000, r2=0x20000
SC_UNMAPPED = 0xE3A01201                          # #0x10000000 -- out of RAM
SC_R2_BAD = 0xE3A02201

#  #361: the xchg negative arm is VACUOUS ON ITS OWN, which a measuring seat
#  caught -- install 0 / fire 0 reads identically on a healthy build and on one
#  with xchg's arming removed, so alone it cannot tell "the matcher rejected the
#  shape" from "the matcher does not exist". That is the very defect #360 was
#  about. Rather than relocate #342's `a != b` term into the matched shape to
#  make the arm self-diagnosing (measured to work, and recorded as the rejected
#  alternative -- it edits a shipped correction's guard for instrumentation's
#  sake), the coupling is made EXPLICIT: selectivity is ONE row over BOTH arms,
#  which cannot pass unless the matcher both installs for distinct registers and
#  declines for equal ones. The pair was always the meaningful unit; this stops a
#  reader mistaking half of it for a test.
for nm, prog, want_fire, want_inst, wit in (
        ("A fold xchg fires", XCHG_POS, 1, 1, ("r1", 0xB2B2B202)),
        ("A fold xchg samereg", XCHG_NEG, 0, 0, ("r1", 0x00000000))):
    r = session(prog, True, seed_regs={"r1": 0xA1A1A101, "r2": 0xB2B2B202})
    if r is None:
        rows.append((nm, "DISC", "DEAD", False)); continue
    buf, regs, _ = r
    f, i = count(buf, "xchg"), installed(buf, "xchg")
    verb, wr = "3: DEBUG" in buf, regs.get(wit[0]) == wit[1]
    rows.append((nm, "DISC" if want_fire else "PIN",
                 "fire=%d inst=%d verb=%s wit=%s" % (f, i, verb, wr),
                 f == want_fire and i == want_inst and verb and wr))
    if want_fire:
        _xchg_pos = (f, i)
    else:
        #  The row that cannot pass on a build where xchg does not exist.
        rows.append(("A fold xchg selective", "DISC",
                     "pos(inst=%d fire=%d) neg(inst=%d fire=%d)"
                     % (_xchg_pos[1], _xchg_pos[0], i, f),
                     _xchg_pos == (1, 1) and (f, i) == (0, 0)))

#  scanc: r3 is a genuine three-way value witness -- 0x77 is table[4] on the
#  positive arm, 0x66 is table[0] because an unmapped string load yields 0, and
#  0x00 when the table page itself is missing. Plus the r5 sentinel, measured
#  not to perturb the fold.
for nm, prog, wf, wd, wr3 in (
        ("A fold scanc fires", scanc_prog(SC_R1_OK, SC_R2_OK), 1, 0, 0x77),
        ("A fold scanc nostr", scanc_prog(SC_UNMAPPED, SC_R2_OK), 0, 1, 0x66),
        ("A fold scanc notbl", scanc_prog(SC_R1_OK, SC_R2_BAD), 0, 1, 0x00)):
    r = session(prog, True, seed_regs={"r3": 0xDEAD, "r5": 0},
                bseed=[(0x10000, 0x04), (0x20004, 0x77), (0x20000, 0x66)])
    if r is None:
        rows.append((nm, "DISC" if wf else "PIN", "DEAD", False)); continue
    buf, regs, _ = r
    f, d, i = (count(buf, "netbsd_scanc"), declined(buf, "netbsd_scanc"),
               installed(buf, "netbsd_scanc"))
    verb = "3: DEBUG" in buf
    #  `is not None` matters: the notbl arm legitimately expects r3 == 0, so a
    #  missing readback must not be silently accepted as a correct zero.
    got3 = regs.get("r3")
    ok = (f == wf and d == wd and i == 1 and verb
          and got3 is not None and got3 == wr3 and regs.get("r5") == 0x5A)
    rows.append((nm, "DISC" if wf else "PIN",
                 "fire=%d dec=%d inst=%d r3=%s sent=%s"
                 % (f, d, i, "none" if got3 is None else "0x%x" % got3,
                    regs.get("r5") == 0x5A), ok))

ngot = 0
for name, kind, detail, ok in rows:
    ngot += ok
    print("%-28s  %-4s %-40s %s" % (name, kind, detail, "ok" if ok else "FAIL"))
print("FOLDMARK_RESULT=%d/%d" % (ngot, len(rows)))
