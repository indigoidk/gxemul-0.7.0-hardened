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


def session(prog, verbose, seed_regs=None, extra=None, bseed=None,
            machine="testarm", loadsrc_be=False, dump_raw=False):
    """Free-running two-pass session. Returns (marker_count, verb_took, regs).

    #383: `machine` selects the rig. `barearm` sets EMUL_BIG_ENDIAN outright
    (machine_test.c) -- the same BE rig arm_endian_probe.py uses -- and is how
    the copyin/copyout folds' byte-order handling is put on the test surface;
    the folds install and fire on BE exactly as on testarm (their matchers gate
    on HOST endianness, not guest). The stub is packed in guest order so its
    fetch decodes. loadsrc_be seeds LOADSRC with `put b` in architectural
    big-endian byte order (11 22 33 44 ...), so every BE expectation traces to
    DDI 0100I Table A2-2 alone rather than to trusting `put w`'s own swap.
    """
    stub = "/tmp/r104f_stub_%s.bin" % machine
    order = "big" if machine == "barearm" else "little"
    with open(stub, "wb") as f:
        f.write((0xE1A00000).to_bytes(4, order))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-A"] + (extra or []) +
                  ["-E", machine, "-M", "64", "0x%x:%s" % (CODE, stub)])
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

    put_failed = False
    if loadsrc_be:
        #  #383: architectural big-endian bytes, laid one at a time with `put b`
        #  (order-free: CACHE_NONE|NO_EXCEPTIONS, so no emulator byte_order code
        #  touches the seed). Word k = 0x11223344+k -> bytes 11 22 33 (44+k).
        for i in range(8):
            w = 0x11223344 + i
            for b in range(4):
                if "FAILED" in send("put b 0x%x, 0x%x"
                                    % (LOADSRC + 4 * i + b,
                                       (w >> (8 * (3 - b))) & 0xff)):
                    put_failed = True
    else:
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

    regs = {"__put_failed": put_failed}   # #383: BE rows assert this (#379 PUT_STATUS)
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
    if prog is COPYOUT or dump_raw:
        mark = len(buf)
        send("dump 0x%x 0x%x" % (STOREDST, STOREDST + 24))
        w = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})", buf[mark:])
        hexwords = "".join(w).split()[:6]
        if dump_raw:
            #  #383: return the RAW 24 memory bytes in address order. `dump`
            #  renders bytes in memory order; the committed path below then
            #  reassembles them LITTLE-endian, which would INVERT a BE row
            #  (green on the broken build, red on the fixed one). A BE copyout
            #  row compares the byte sequence itself against the architectural
            #  layout, with no assembly-order assumption.
            regs["__dstbytes"] = b"".join(bytes.fromhex(x) for x in hexwords)
        else:
            mem = [int.from_bytes(bytes.fromhex(x), "little")
                   for x in hexwords]
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
WARM_STRT = 0xE4A15004      # strt r5,[r1],#4   -- copyout warms with a STORE
                            # because that sets host_store under ANY config.
                            # (#382: the older reason "a load leaves host_store
                            # NULL" holds only MMU-on + read-only page; MMU-off
                            # here, a load sets host_store too -- ok-1==1. The
                            # store warm-up is the robust choice, not the only
                            # one -- the corrected fact lives at cpu_arm_instr.c
                            # X(netbsd_copyout) and arm_endian_probe.py:60.)


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

#  ---- #368: the copyin fold's ROTATION, with an UNALIGNED base ---------------
#  Every arm above bases on `mov r0,#0x10000`, so `r0 & 3 == 0` and #362's
#  six-word rotation block in X(netbsd_copyin) NEVER EXECUTES. Measured: with
#  that block neutralised, the writeback probe stayed 17/17 and this probe stayed
#  14/14. So the rotation shipped unreachable, not merely unmeasured.
#
#  The row is a fold-versus-TEMPLATE differential on ONE binary, not a check
#  against constants computed here. Pass 1 declines (the is_userpage bit is
#  clear), so its six loads run through the very handler the fold's bail-out
#  delegates to; pass 2 folds. r1 accumulates `sl` across both passes, so
#  r1 == 0 iff the two paths AGREE -- and when they do not, pass 1's own value is
#  recoverable as r1 ^ sl. That XOR is the whole design: a row that read
#  registers only at the end would measure pass 2 against hand-arithmetic,
#  because pass 2 OVERWRITES r6-r11 and pass 1's values are gone.
#
#  r1 is the accumulator deliberately: session() already reads it back and only
#  the copyout arms assert it, so the shared helper needs no change.
#
#  #369: the accumulator covers ONE register of six (`sl`), and the reason that
#  is sufficient is load-bearing enough to write down. All six ldrt dispatch the
#  SAME instantiation, load_w1_word_u1_p0_imm, so a template defect cannot hit
#  five destination registers and spare sl -- the six are not independent
#  samples, they are one code path exercised six times. The six `vals` are still
#  compared individually, so a FOLD defect that mangles one register is caught
#  by those; the XOR's job is only the cross-path comparison. If a future change
#  ever specialises one of those six slots to a different handler, this argument
#  lapses and the accumulator must widen -- it would narrow silently otherwise.
#
#  #369: these arms also arm COMBINE(xchg) in passing (any eor_regshort decode
#  arms it) and it declines -- but NOT for the reason #368's record gave. It is
#  not a same-register short-circuit on r1: COMBINE(xchg) reads
#  a = ic[-2].arg[0] and b = ic[-1].arg[0], which at the eor's slot are the
#  `ldrt r8` and `ldrt r9` slots, whose arg[0] are BOTH &r[0] -- the two loads'
#  shared BASE register. So `a != b` fails on that, and independently ic[-2].f
#  is a load handler rather than instr(eor_regshort). Same conclusion, different
#  mechanism. xchg prints only on install, so nothing is emitted either way; and
#  because count()/declined()/installed() are name-scoped, a future xchg decline
#  marker would not disturb these rows.
#
#  THREE offsets, not one. `8 * (r0 & 1)` agrees with `8 * (r0 & 3)` at +1 and
#  differs at +2 and +3, and a guard of `if (r0 & 1)` would skip the rotation
#  entirely at +2 -- one arm cannot tell those apart.
#
#  Every iword was checked through `unassemble`; the branch target especially,
#  since a wrong target silently changes the pass count and the pass count is
#  what makes fire=1/dec=1 a DERIVED number rather than a threshold. 0x5AFFFFF4
#  disassembles as `bpl 0x8008`, which is word index 2 -- the re-seed point.
#
#  HONEST SCOPE -- #370: the bcopyinout claim below is UNVERIFIED. It exists in
#  this tree only in our own writing; no NetBSD source is present, so it is
#  panel recollection, the DDI 0100I provenance pattern. Until someone reads the
#  real bcopyinout.S or disassembles copyin in the battery's ARM kernel image,
#  the honest statement is "these rows pin internal consistency; guest
#  reachability of the unaligned fold path is unverified."
#  REPORTEDLY: NetBSD's bcopyinout.S does `ands r3,r0,#0x03 / bne` before its
#  six-ldrt block, so a real guest never reaches this fold with an unaligned
#  base. These rows pin an INTERNAL-CONSISTENCY property -- the fold agreeing
#  with the handler its own bail-out delegates to, the #342/#355 class -- and not
#  a guest-reachable behaviour. Also note #362's own comment describes the BROKEN
#  build ("pass 1 yields the rotated word while pass 2 folds and yields the
#  unrotated one"); on the shipped build BOTH rotate, so the healthy expectation
#  here is AGREEMENT, not contradiction.
MOV_R1_0 = 0xE3A01000       # mov  r1,#0
EOR_R1_SL = 0xE021100A      # eor  r1,r1,sl
ADD_R0_N = (0xE2800001, 0xE2800002, 0xE2800003)     # add r0,r0,#1 / #2 / #3


def copyin_unal(n):
    """Two passes, base re-seeded to 0x1000n each pass. No breakpoint anywhere:
    read-ahead must stay alive so the fold is installed before its slot
    dispatches, and a breakpoint would also make the fold count passes - 1."""
    return [
        0xE3A03001,        # 0  mov  r3,#1        two passes
        MOV_R1_0,          # 1  mov  r1,#0        agreement accumulator
        0xE3A00801,        # 2  L: mov r0,#0x10000
        ADD_R0_N[n - 1],   # 3  add  r0,r0,#n     UNALIGNED, re-seeded each pass
        0xE4B0A004,        # 4  ldrt sl,[r0],#4   <- fold entry slot
        0xE4B0B004,        # 5  ldrt fp,[r0],#4
        0xE4B06004,        # 6  ldrt r6,[r0],#4
        0xE4B07004,        # 7  ldrt r7,[r0],#4
        0xE4B08004,        # 8  ldrt r8,[r0],#4
        0xE4B09004,        # 9  ldrt r9,[r0],#4   arms COMBINE(netbsd_copyin)
        EOR_R1_SL,         # 10 eor  r1,r1,sl     0 iff both passes agree
        0xE2533001,        # 11 subs r3,r3,#1
        0x5AFFFFF4,        # 12 bpl -> word 2
        0xEAFFFFFE,        # 13 b .
    ]


#  ROR 8*n of the six seeded words 0x11223344..0x49. "Rotation absent" would give
#  the UNROTATED words -- which is exactly what the aligned `fires` row asserts,
#  so a fold that stops rotating cannot pass these rows by satisfying that one.
for n in (1, 2, 3):
    rot = 8 * n
    want = tuple(((0x11223344 + k) >> rot) | (((0x11223344 + k) << (32 - rot))
                 & 0xFFFFFFFF) for k in range(6))
    nm = "A fold copyin rot plus%d" % n
    r = session(copyin_unal(n), True, seed_regs=SEED2)
    if r is None:
        rows.append((nm, "DISC", "DEAD", False))
        continue
    buf, regs, _ = r
    f, d, i = (count(buf, "netbsd_copyin"), declined(buf, "netbsd_copyin"),
               installed(buf, "netbsd_copyin"))
    verb = "3: DEBUG" in buf
    #  r0 advanced by the full six transfers from the UNALIGNED base. #357 makes
    #  the fold and the template agree here, so this proves the program ran
    #  without presuming the fold -- a run-witness, not a fold-witness.
    adv = regs.get("r0") == 0x10000 + n + 24
    vals = tuple(regs.get(k) for k in ("sl", "fp", "r6", "r7", "r8", "r9"))
    agree = regs.get("r1") == 0
    ok = (f == 1 and d == 1 and i == 1 and verb and adv
          and vals == want and agree)
    rows.append((nm, "DISC",
                 "fire=%d dec=%d inst=%d adv=%s vals=%s xor=%s"
                 % (f, d, i, adv, vals == want,
                    "unread" if regs.get("r1") is None else "0x%x" % regs["r1"]),
                 ok))


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

#  ---- #383: the copyin/copyout folds vs GUEST byte order (barearm) ----------
#  Both fold bodies moved raw HOST words between the guest registers and the
#  host page with no byte-order term, while the load/store_w1_word template
#  they delegate to on a decline is order-aware since #372 -- the #342/#355
#  self-contradiction class, and (unlike memset/memcpy) NOT closed by #378's
#  install gate because these matchers key on the GENERIC handler, which
#  installs for a BE guest too. These rows put the folds' BE behaviour on the
#  test surface: on the committed build they read reversed values (the defect);
#  after the swap they agree with the order-aware general path.
#
#  The two-pass XOR is the copyin machinery reused verbatim: pass 1 declines
#  (is_userpage clear on the first ldrt) and runs the order-aware general
#  handler, pass 2 folds. r1 == 0 iff the two AGREE, and the final `vals` are
#  the fold's own output. THE UNALIGNED ROWS ARE LOAD-BEARING: the aligned row
#  cannot tell swap-before-rotation from swap-after (ROR by 0 and 16 commute
#  with a 4-byte reversal), so a fix that swapped AFTER #362's rotation would
#  pass every aligned row and ship green. +1 and +3 are the offsets where the
#  two orders diverge (a sweep that only hit palindromic seeds would miss this
#  -- the tail a sweep cannot reach). LOADSRC is seeded with `put b` in
#  big-endian byte order so every expectation below traces to DDI 0100I Table
#  A2-2 (p. A2-32) and LDR's Alignment note (p. A4-44), not to `put w`'s swap.
def copyin_xor(off):
    """copyin_unal generalised to offset 0 (a NOP in the add slot keeps the
    14-word layout and the proven 0x5AFFFFF4 bpl target)."""
    return [
        0xE3A03001, MOV_R1_0, 0xE3A00801,
        NOP if off == 0 else ADD_R0_N[off - 1],
        0xE4B0A004, 0xE4B0B004, 0xE4B06004, 0xE4B07004, 0xE4B08004, 0xE4B09004,
        EOR_R1_SL, 0xE2533001, 0x5AFFFFF4, 0xEAFFFFFE,
    ]


def ror32(v, r):
    r &= 31
    return v if r == 0 else ((v >> r) | (v << (32 - r))) & 0xFFFFFFFF


control_be = "FAIL"
for off in (0, 1, 3):
    want = tuple(ror32(0x11223344 + k, 8 * off) for k in range(6))
    nm = "A fold copyin BE +%d" % off
    r = session(copyin_xor(off), True, seed_regs=SEED2,
                machine="barearm", loadsrc_be=True)
    if r is None:
        rows.append((nm, "DISC", "DEAD", False)); continue
    buf, regs, _ = r
    f, d, i = (count(buf, "netbsd_copyin"), declined(buf, "netbsd_copyin"),
               installed(buf, "netbsd_copyin"))
    verb = "3: DEBUG" in buf
    adv = regs.get("r0") == 0x10000 + off + 24
    vals = tuple(regs.get(k) for k in ("sl", "fp", "r6", "r7", "r8", "r9"))
    agree = regs.get("r1") == 0
    puts = not regs.get("__put_failed")
    #  FOLDMARK_CONTROL_BE: pass 1's general value is r1 ^ sl, which is the
    #  architectural word on BOTH builds -- a fix-state-independent liveness
    #  pin (the barearm rig constructed, both passes ran, the fold fired),
    #  mirroring ENDIAN_CONTROL378. A dead or mis-threaded session cannot
    #  false-green the BE group.
    if off == 0 and regs.get("r1") is not None and regs.get("sl") is not None:
        if (regs["r1"] ^ regs["sl"]) == 0x11223344:
            control_be = "OK"
    ok = (f == 1 and d == 1 and i == 1 and verb and adv
          and vals == want and agree and puts)
    rows.append((nm, "DISC",
                 "fire=%d dec=%d inst=%d adv=%s vals=%s xor=%s puts=%s"
                 % (f, d, i, adv, vals == want,
                    "unread" if regs.get("r1") is None else "0x%x" % regs["r1"],
                    puts), ok))

#  copyout BE: single warm pass, then compare the RAW 24 stored bytes against
#  the architectural big-endian layout (store order r8,r9,sl,fp,r6,r7, pinned
#  by the matcher). Raw bytes, never a little-assembled value -- see dump_raw.
BE_STORE_SEED = {"r5": 0x5A5A0000, "r6": 0x66660001, "r7": 0x77770002,
                 "r8": 0x88880003, "r9": 0x99990004, "sl": 0xAAAA0005,
                 "fp": 0xBBBB0006}
BE_WANT_BYTES = bytes([0x88, 0x88, 0x00, 0x03, 0x99, 0x99, 0x00, 0x04,
                       0xAA, 0xAA, 0x00, 0x05, 0xBB, 0xBB, 0x00, 0x06,
                       0x66, 0x66, 0x00, 0x01, 0x77, 0x77, 0x00, 0x02])
r = session(ab_prog("copyout", True), True, seed_regs=BE_STORE_SEED,
            machine="barearm", dump_raw=True)
if r is None:
    rows.append(("A fold copyout BE", "DISC", "DEAD", False))
else:
    buf, regs, _ = r
    f = count(buf, "netbsd_copyout")
    verb = "3: DEBUG" in buf
    gotb = regs.get("__dstbytes")
    bytes_ok = (gotb == BE_WANT_BYTES)
    adv = regs.get("r1") == 0x11000 + 24
    rows.append(("A fold copyout BE", "DISC",
                 "markers=%d verb=%s adv=%s bytes=%s"
                 % (f, verb, adv, gotb.hex() if gotb else "none"),
                 f >= 1 and verb and adv and bytes_ok))

ngot = 0
for name, kind, detail, ok in rows:
    ngot += ok
    print("%-28s  %-4s %-40s %s" % (name, kind, detail, "ok" if ok else "FAIL"))
print("FOLDMARK_CONTROL_BE=%s" % control_be)
print("FOLDMARK_RESULT=%d/%d" % (ngot, len(rows)))
