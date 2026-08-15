#!/usr/bin/env python3
"""Drive an emulated guest to a shell over a pty and check what it computes.

Why a pty rather than a pipe: on a pipe, both the emulator and the guest's libc switch to
block buffering, so a run cut short by a timeout loses its last partial block. An earlier
version of this harness compared byte counts across builds over pipes and "found" a
capability regression that was entirely a lost 4 KB buffer. A pty is line-buffered and is
also the only way to type at a login prompt.

Usage:  drive_guest.py <rig> <emulator-binary>
Exit:   0 all markers seen, 1 otherwise. Marker counts are printed as KEY=VALUE lines so
        the calling gate can parse them without guessing.
"""
import os
import pty
import re
import select
import sys
import time

IMAGES = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"

# Each rig: the emulator arguments, the conversation, and the markers that must appear.
# A rig proves something only if it CHECKS AN ANSWER -- "the guest survived" is not a
# result. The FP steps below compute values whose correct output is known, so a wrong
# float_emul.c arm shows up as a wrong number rather than as a still-running guest.
RIGS = {
    # m88k: cpu_m88k_instr.c stores IEEE_FMT_S, i.e. the exact arm #287 changed, and had
    # no execution coverage at all before this rig existed.
    "luna88k": {
        # "R:" opens the base image read-only and sends every guest write to a temporary
        # overlay that is thrown away at exit. Without it each run mutates the shared 2 GB
        # image and later runs inherit whatever filesystem state earlier ones left --
        # including an unclean unmount when a timeout kills a booted guest. That made
        # gate 7 fail non-deterministically; see the note in gate_ab.sh.
        # #420: -N makes gxemul print "[ <ninstrs> instrs; ...]" every 2^25 instructions.
        # That stream is the progress oracle; see boot_progress() below.
        "args": ["-N", "-e", "luna-88k", "-d",
                 "R:" + IMAGES + "/liveimage-luna88k-raw-20250518.img", "boot"],
        "boot_wait": 2400,
        # #420, each measured. The 600 s that used to sit in boot_wait was the defect:
        # under 8 busy loops on 8 cores a healthy, fully-correct boot needs far longer
        # than 600 s. Two runs, and they are DIFFERENT runs -- do not merge them: gate 7's
        # file-polling driver reached login at 742 s (markers only), and this gate's pty
        # driver reached it at 720.8 s with every marker AND both computed values correct.
        # Against the old budget that boot scored BOOT_REACHED=0 and three red rows -- a
        # capability regression that never was.
        # 12 G is the same budget gate 7 uses (observed max 7.786 G over eleven boots,
        # +54%); it bounds only the failure path, since a healthy boot stops at the
        # marker long before it. 120 s of silence is 17x the worst inter-record gap
        # measured on this path under saturation (7.06 s; n=219, median 3.86).
        "budget": 12000000000,
        "stall": 120,
        "boot_pat": r"login:",
        "tries": 4,
        # Markers split in the source so they can only come from guest OUTPUT, never from
        # the pty echoing what was typed.
        "steps": [
            ("root\n", 8),
            ("\n", 5),
            ("echo GX_SHELL''_OK; uname -m\n", 12, r"GX_SHELL_OK"),
            # 1.5/3.0 = 0.5 and sqrt(2) = 1.414214 -- the ANSWER is what is checked.
            ("awk 'BEGIN{printf \"GX_FP %.6f %.6f\\n\", 1.5/3.0, 2.0**0.5}'\n", 15,
             r"GX_FP [\d.]+ [\d.]+"),
            ("echo GX_DO''NE\n", 8, r"GX_DONE"),
        ],
        "markers": ["login:", "GX_SHELL_OK", "GX_DONE"],
        "expect_values": {r"GX_FP ([\d.]+) ([\d.]+)": ["0.500000", "1.414214"]},
    },
    # SuperH: cpu_sh_instr.c also stores IEEE_FMT_S. The 7.6 install kernel stops at an
    # installer menu offering (S)hell.
    #
    # NO IN-GUEST FP CHECK HERE, and that is a measured limitation rather than an
    # oversight: the OpenBSD install ramdisk was probed and has no awk, perl, bc, dc or
    # python, and its shell arithmetic is integer-only ($((3/2)) evaluates to 1). There is
    # nothing on the media that can compute a float. What this rig therefore proves is
    # that the SH4 core executes a complete kernel boot and an interactive shell -- real
    # instruction-level coverage of cpu_sh_instr.c, but not of its FP store path.
    #
    # That gap is narrower than it looks. #287 is in the SHARED float_emul.c, and the
    # luna88k rig above exercises that shared arm from a non-MIPS caller with a checked
    # answer. What remains unproven for SuperH is only its own caller glue.
    "landisk": {
        "args": ["-N", "-E", "landisk", "-M", "64",
                 IMAGES + "/openbsd76-landisk-bsd.rd"],
        "boot_wait": 900,
        # *** #420: NO INSTRUCTION BUDGET FOR LANDISK, AND THAT IS DELIBERATE. ***
        # Six idle landisk boots span 2,046,965,550 to 2,852,740,381 -- a 39.4% spread,
        # against luna88k's 3.57% over eight runs. A ceiling derived from that would be
        # either uselessly loose or a false-FAIL waiting to happen, and inventing one
        # from six samples would be exactly the "mean quoted as a worst case" error #419
        # pass 4 corrected. Landisk relies on the stall detector and the backstop until
        # somebody measures its rate properly; that is FILED, not fixed.
        #
        # Note also that landisk had no measured false-FAIL to begin with: it reaches its
        # prompt in 7.2-8.3 s against the old 420 s budget, 50x headroom. Converting it
        # buys DISTINGUISHABILITY -- a hung SH4 core now reports STALLED instead of a
        # timeout indistinguishable from load -- not headroom.
        "budget": 0,
        # Its -N records arrive far more often in WALL TIME than luna88k's (median gap
        # 0.04 s against 3.86 s; 62-87 records in an 8 s boot), so 60 s of silence is
        # overwhelming evidence of a hang.
        #
        # NOTE THE FRAMING, because an earlier version of this comment got it wrong twice:
        # it said "~20x denser" when the stated medians give 96x, and "denser" is the wrong
        # word anyway -- PER GUEST INSTRUCTION both streams fire at the same 2^25 cadence.
        # What differs is how fast landisk executes, not how often gxemul prints.
        "stall": 60,
        "boot_pat": r"\(I\)nstall, \(U\)pgrade, \(A\)utoinstall or \(S\)hell\?",
        # This rig is INTERACTIVE again as of #293. It originally sent no input at all,
        # because typed lines vanished non-deterministically -- measured at 10 of 12
        # commands lost whole, no echo, no execution. The cause was never the SCIF: the
        # machine's main console handle was unclaimed on landisk, so handle 0 (polled
        # every tick for CTRL-C) raced the SCIF for the same host stdin and stole whole
        # lines. #293 makes the SCIF claim the main console, after which the same probe
        # measures 12 of 12 commands delivered. The confirm-and-retry machinery is kept
        # as a belt against future regressions -- a retry that never fires is free.
        #
        # Markers are split in the source (GX_SH''ELL_OK) so a pty echo of the typed
        # command cannot satisfy them; only guest output can.
        "tries": 3,
        "settle": 2,
        "steps": [
            ("S\n", 15),
            ("stty sane\n", 5),
            ("echo GX_SH''ELL_OK\n", 8, r"GX_SHELL_OK"),
            # The checked ANSWER: integer arithmetic computed by the guest shell. The
            # typed text is "$((6*7))", which does not contain "42", so the value can
            # only come from execution.
            ("echo GX_ANS $((6*7))\n", 8, r"GX_ANS 42"),
            ("echo GX_DO''NE\n", 8, r"GX_DONE"),
        ],
        "markers": ["OpenBSD 7.6", "root on rd0a", "GX_SHELL_OK", "GX_DONE"],
        # Both the boot-time hardware probe AND the interactive answer are asserted.
        # Anchored on the shpcic0 line: a bare "HITACHI (SH\w+)" matches the earlier
        # cpu0 line and returns "SH4".
        "expect_values": {
            r"shpcic0 at mainbus0: HITACHI (\w+)": ["SH7751R"],
            r"GX_ANS (\d+)": ["42"],
        },
    },
}


# *** THE TERMINATOR IS MANDATORY WHILE STREAMING. ***
# It used to be optional (`\]\r?\n?`), and that recreated the very wrong answer the strip
# exists to prevent: the instant `]` arrived the record matched WITHOUT its newline, the hold
# emptied, and the newline turned up on the next read as ordinary console text -- rejoining
# nothing and leaving `HITACHI SH77\n51R`. Measured at 1 of 138 split offsets for LF and 2 of
# 81 for CRLF. Not reachable on today's rigs (zero of 740 real pty reads landed inside a
# record) but a WRONG ANSWER rather than a miss.
REC = re.compile(r"\[ *(\d+) instrs[^\]]*\]\r?\n")
# At end of run there is no next read, so a final record that never got its newline is
# matched terminator-less rather than left in the log.
REC_EOF = re.compile(r"\[ *(\d+) instrs[^\]]*\]\r?\n?")
# The longest record actually observed is 106 chars (landisk,
# <sh4_emode_dcache_wbinv_range_index+0x62>); luna88k's run 45-66 and carry no symbol at all.
HOLD_MAX = 256


def split_stream(tail, text):
    """Split pty text into console output and instruction records.

    Returns (console_chunk, new_tail, last_ninstrs_or_None).

    AT MODULE SCOPE ON PURPOSE. The gate can only observe this driver's OUTPUT, so it cannot
    reach this function through any row -- 13 of 18 driver mutants were measured surviving
    every gate row. regress/selftest_absorb.py calls THIS function, not a copy: a
    re-implementation would test the copy and leave the shipped code unguarded, which is the
    same "a row guards a different instance than it appears to" trap this harness has now hit
    twice.

    HOLD ON A MISSING NEWLINE, not merely on a missing ']'. Both are unfinished records:
    "[ 123 inst" and "[ 123 instrs; ...]" alike. Testing only for ']' let a bracket-complete
    but unterminated record through, which is exactly the defect REC above closes. A newline
    always releases the hold, so a guest line containing a bare '[' cannot stall the buffer.
    """
    tail += text
    out, pos, n = [], 0, None
    for m in REC.finditer(tail):
        out.append(tail[pos:m.start()])
        n = int(m.group(1))
        pos = m.end()
    rest = tail[pos:]
    i = rest.rfind("[")
    if i != -1 and "\n" not in rest[i:] and len(rest) - i < HOLD_MAX:
        out.append(rest[:i])
        tail = rest[i:]
    else:
        out.append(rest)
        tail = ""
    return "".join(out), tail, n


def drive(rig, binary):
    cfg = RIGS[rig]
    #  d1: honour $LOGDIR (lib.sh exports it) so a mutation census can be given a private
    #  directory instead of poisoning the shared logs gate 6 grades.  `or`, not
    #  os.environ.get(LOGDIR, default): with LOGDIR set but EMPTY the two-argument form
    #  returns "" and these paths become "/drive_<rig>.log" -- the filesystem root.  The
    #  `or` form matches lib.sh's own ${LOGDIR:-...}, which also treats empty as unset.
    #  ABSOLUTE, and resolved BEFORE the os.chdir(IMAGES) below: makedirs runs in the
    #  caller's cwd while the two open() calls run in IMAGES, so a RELATIVE $LOGDIR would
    #  create the directory in one place and try to write the logs in another -- and gate 6
    #  would then grade a path neither of them used.  The old hardcode was absolute, so
    #  this hazard arrived with the fix; three review seats caught it.
    logdir = os.path.abspath(os.environ.get("LOGDIR") or "/tmp/gxregress")
    log_path = "%s/drive_%s.log" % (logdir, rig)
    raw_path = "%s/drive_%s.raw.log" % (logdir, rig)
    os.makedirs(logdir, exist_ok=True)
    os.chdir(IMAGES)
    # #420: TWO logs. The raw stream keeps everything for forensics; drive_<rig>.log is
    # console-only, because gate_hygiene.sh greps THAT file for distress SUBSTRINGS and an
    # instruction record embeds a guest symbol (e.g. "<sched_idle+0x8c>"). Measured over 527
    # records across three runs there is no collision today -- but the mechanism is there,
    # and splitting the streams removes it for nothing.
    raw = open(raw_path, "wb")
    log = open(log_path, "wb")

    #  Read the three progress constants BEFORE anything is spawned.  With the .get
    #  defaults gone (see boot_progress), a rig that omits one must fail -- and a review
    #  seat pointed out that it used to fail AFTER pty.fork(), which leaves an emulator
    #  child running behind the traceback.  Touch them here so a config error kills the
    #  run before it costs a process.
    _ = cfg["budget"], cfg["stall"], cfg["boot_wait"]

    #  a4: start the wall clock BEFORE the fork.  boot_progress()'s own t0 begins after
    #  exec, so it cannot see process startup, and it is scoped to that nested function.
    t_start = time.time()

    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(binary, [binary] + cfg["args"])
        os._exit(127)

    buf = ""
    tail = ""          # bytes that may be the START of a record; see absorb()
    ninstrs = 0

    # *** THE STRIP MUST BE UNANCHORED AND MUST EAT THE TRAILING NEWLINE. ***
    # cpu_show_cycles() printf's the record into the same stdout as the guest console with
    # NO LEADING NEWLINE, so it lands at the cursor and TERMINATES THE GUEST'S PARTIAL LINE.
    # Measured by injecting one record into the real logs at the place gxemul puts it:
    #
    #   assertion                 control     no strip   ANCHORED    unanchored
    #   landisk HITACHI (\w+)     SH7751R     SH77       SH77        SH7751R
    #   landisk boot_pat          MATCH       (none)     (none)      MATCH
    #   luna88k GX_FP ...         values      (none)     (none)      values
    #
    # An anchored `(?m)^...` strip heals NOTHING, because the pty emits bare CRs as well as
    # CRLF and Python's ^ only matches after \n. Worse, the landisk row then yields SH77 --
    # not a miss but a WRONG ANSWER, which reads as an emulation defect. Eating the trailing
    # newline is what rejoins the split line. Validated: free-stripping the -N logs
    # reproduces the previous no--N log content. NOTE: an earlier version of this line said
    # the log SIZES reproduce "exactly (6234 B, 3838 B)". That holds for luna88k and NOT for
    # landisk, which gives 3837 because the guest prints a variable CPU speed. The records
    # were corrected and this comment was not -- grep for siblings when correcting a claim.
    #
    # The guest printing something of this shape was checked and does NOT happen: zero
    # occurrences of "[ N instrs" in either complete no--N log.
    # *** THE TERMINATOR IS MANDATORY WHILE STREAMING. ***
    # It used to be optional (`\]\r?\n?`), and that recreated the very wrong answer the
    # comment above says it prevents: the instant `]` arrived the record matched WITHOUT its
    # newline, `tail` emptied, and the newline turned up on the next read as ordinary console
    # text -- rejoining nothing and leaving `HITACHI SH77\n51R`. The hold below could not
    # help, because it only engages when the fragment contains NO `]`.
    # Measured at 1 of 138 split offsets for LF and 2 of 81 for CRLF. Not reachable on
    # today's rigs -- zero of 740 real pty reads landed inside a record -- but it is a WRONG
    # ANSWER rather than a miss, and it costs one character to close.
    def absorb(text):
        """Split raw pty text into console text and instruction records.

        A pty read can END IN THE MIDDLE OF A RECORD, so any trailing fragment that could
        still become one is HELD BACK rather than classified -- otherwise half a record
        leaks into the match buffer and the other half is stripped, which corrupts exactly
        the assertions this rig makes. The hold is bounded: a newline or a ']' releases it,
        so a guest line containing a bare '[' cannot stall the buffer.

        The splitting itself lives in split_stream() at module scope, so a selftest can
        exercise it directly. That is not tidiness: the GATE CAN ONLY SEE THIS DRIVER'S
        OUTPUT, so it physically cannot reach this logic, and a measured 13 of 18 driver
        mutants survive every gate row. A canned-stream test of the real function kills 10
        of them -- but only if it calls the REAL function, not a copy of it.
        """
        nonlocal buf, tail, ninstrs
        chunk, tail, n = split_stream(tail, text)
        if n is not None:
            ninstrs = n
        buf += chunk
        if chunk:
            log.write(chunk.encode("latin1", "replace")); log.flush()

    def read_once(timeout):
        r, _, _ = select.select([fd], [], [], timeout)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        raw.write(d)
        raw.flush()
        absorb(d.decode("latin1", "replace"))
        return True

    def expect(pat, timeout):
        t = time.time()
        while time.time() - t < timeout:
            if not read_once(0.3):
                return False
            if re.search(pat, buf):
                return True
        return False

    def pump(secs):
        t = time.time()
        while time.time() - t < secs:
            if not read_once(0.3):
                return

    def send(s):
        b = s.encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])

    # SEND, THEN CONFIRM, THEN RETRY.
    #
    # The SuperH console drops guest input non-deterministically: a command vanishes
    # whole, with no echo and no output. Measured on one boot with ten commands of
    # increasing length, 15, 23 and 33 byte lines ran while 9, 17, 27 and 41 byte lines
    # were lost -- so it is neither a length limit nor a strict alternation, and adding
    # settle time before the write did not help. Roughly a third of writes get through.
    #
    # A rig cannot be built on "the send worked", so a step may carry a CONFIRM pattern
    # and is re-sent until that pattern appears. Steps without one are fire-and-forget.
    #
    # The confirm patterns match only what the command PRINTS, never what was typed --
    # a pty echoes the master's writes back, so a naive marker is satisfied by the echo
    # alone and proves nothing about execution.
    #  #425: THE GATE MUST GRADE THE VALUES THAT GOVERNED THE RUN.  Until this round the
    #  driver read the constants TWICE -- once in the call below, once in the record block --
    #  and nothing tied the two reads together.  MEASURED: mutating only the call site
    #  (`budget * 1000` in argument position) left every printed key identical and every gate
    #  row green, while the run went from REASON=BUDGET at 13 G to REASON=STALLED at 20 G.
    #  The oracle was disarmed and the record said otherwise.
    #
    #  Sharing a LOCAL between the two sites is not enough, and four review seats proposed it:
    #  the mutation rewrites the ARGUMENT EXPRESSION, so the local -- and the print taken from
    #  it -- stays honest.  A local proves what the caller INTENDED TO PASS.  Only the callee's
    #  own parameters prove what it RECEIVED, so boot_progress records them here.
    #
    #  Residual, stated rather than hidden -- and stated PRECISELY, because the first
    #  version of this comment claimed more than the detector delivers and a review seat
    #  MEASURED it false twice.  A mutation strictly INSIDE boot_progress, below this line,
    #  escapes the print.  What selftest_budget.py then covers:
    #    * an in-body change to the BUDGET, to within one instruction -- `budget = budget - 1`
    #      inserted here passes the straddle 7/0, because the straddle admits any threshold
    #      in {N-1, N}.  At 12 G that is one instruction in twelve billion;
    #    * an in-body change to STALL or BACKSTOP: NOT AT ALL.  `stall = stall * 10` passes
    #      7/0, because the under-budget leg accepts BACKSTOP as a stated reason and nothing
    #      straddles either constant.  That gap is FILED, not closed here.
    used = {}

    def boot_progress(pat, backstop, budget, stall):
        """Wait for the boot milestone against a budget of GUEST WORK, and say why it stopped.

        #420. The old form was `expect(boot_pat, 600)` -- a wall-clock budget, which is a
        LOAD-SENSITIVE ORACLE: under load the guest does less inside the same seconds, the
        milestone never arrives, and the rig reports a capability regression. Reproduced:
        the unmodified driver under 8 busy loops on 8 cores gave BOOT_REACHED=0 and three
        red rows at 601 s, with panic/FATAL/trap all zero and the log ending on ordinary
        late rc output -- 63.4% of the way to login. The same load with room to finish
        reached login at 720.8 s with every marker and both computed values correct.

        *** BACKSTOP IS A HARD FAIL HERE, unlike gate 7. *** Gate 7 can call a wall-clock
        expiry inconclusive because it boots pristine, prebatch and HEAD in one run, so
        prebatch reaching its marker is free evidence the host was healthy. THIS RIG BOOTS
        ONE GUEST. There is nothing to compare against, so "the host might have been slow"
        is not falsifiable BY A COMPARABLE WITNESS -- and an excuse nothing can contradict
        must not be allowed to soften a verdict. The differential-witness trick does not
        generalise. ("Unfalsifiable" was an overclaim: NINSTRS at the backstop partially
        falsifies host starvation, and the two rigs cross-witness. The decision stands; the
        wording should not claim more than it has.)
        """
        nonlocal tail
        used["backstop"], used["budget"], used["stall"] = backstop, budget, stall
        t0 = time.time()
        last_n, last_change = ninstrs, t0

        def stop(why):
            """*** THE MILESTONE MUST WIN A TIE. ***

            The marker is tested at the TOP of the loop, but every failure condition is
            tested AFTER read_once() -- so a milestone absorbed by the very read that also
            crossed a threshold would lose to the failure reason and false-FAIL a healthy
            run.  This is the same defect #419 pass 3 fixed in lib.sh (BACKSTOP reported
            with the marker already in the log, measured 3/3 deterministic); porting the
            loop's SHAPE across carried the bug rather than the fix.  Re-check before
            returning anything else, and flush whatever absorb() is holding first: a
            milestone whose text begins with '[' would otherwise still be in the hold.
            """
            if tail and re.search(pat, buf + tail):
                return "MARKER"
            if re.search(pat, buf):
                return "MARKER"
            return why

        while True:
            if re.search(pat, buf):
                return "MARKER"
            if not read_once(0.3):
                return stop("EXITED")   # the emulator died; a crash is not a timeout
            now = time.time()
            if ninstrs != last_n:
                last_n, last_change = ninstrs, now
            if budget and ninstrs > budget:
                return stop("BUDGET")   # a full allowance of WORK, still no milestone
            if now - last_change >= stall:
                # A slow host still emits records; a guest that has stopped executing does
                # not. NOT a universal: a BUSY-LOOP hang executes indefinitely and keeps
                # emitting, so this detects a WEDGED guest, not every hang.
                return stop("STALLED")
            if now - t0 >= backstop:
                return stop("BACKSTOP")

    settle = cfg.get("settle", 0)
    tries = cfg.get("tries", 1)
    #  NO .get DEFAULTS.  Both rigs declare all three keys, and the naive unification is a
    #  trap a review seat named: `.get("stall", 120)` on BOTH paths would make an omitted key
    #  print a PASSING 120 where today it prints a FAILING 0.  A rig that omits a key must die
    #  loudly here rather than run under an invented constant.
    reason = boot_progress(cfg["boot_pat"], cfg["boot_wait"],
                           cfg["budget"], cfg["stall"])
    # An absent oracle stream is a HARNESS fault and must be red: removing -N leaves the
    # guest booting perfectly, every marker matching and every value correct, while the
    # budget and stall detectors are silently unarmed. Measured on landisk, which has no
    # race to hide behind (8 s boot against a 60 s stall): every row stayed green.
    # THE KILL ROW ASSERTS THE COUNT, NEVER THE REASON.
    # EXITED outranks ABSENT, as it does in lib.sh: an emulator that died before its first
    # record is a dead build, not a harness fault, and relabelling it ABSENT would blame the
    # wrong thing. Only a run that neither died nor reached the milestone is a harness fault.
    if ninstrs == 0 and reason not in ("MARKER", "EXITED"):
        reason = "ABSENT"
    print("REASON=%s" % reason)
    print("NINSTRS=%d" % ninstrs)
    #  a4: TELEMETRY, NEVER AN ORACLE.  No gate row may fail on this value: a wall-clock
    #  threshold is a LOAD-SENSITIVE oracle, and this battery has already lost a 45-minute
    #  run to one (gate_ab, when subagents loaded the host).  Rows may assert that the key
    #  is PRESENT and that it is contained by the gate's own measured interval -- never a
    #  magnitude.  Paired with NINSTRS above, which is the count at this same instant, it
    #  gives instructions-per-second, which is the datum the landisk load note needs and
    #  today cannot accrue.  On a run that never reaches its marker this is time-to-REASON,
    #  not time-to-milestone.
    print("BOOT_WALL=%.1f" % (time.time() - t_start))
    # #420 pass 2: report the constants so the GATE can range-check them.
    #
    # Gate 7 had exactly this hole and #419 pass 3 closed it: its selftest exercised the
    # helper with LITERAL arguments, so multiplying the real budget by 1000 or disabling
    # the real stall threshold left every check green -- the rows guarded a different
    # INSTANCE than they appeared to. These live in a Python dict that no shell row can
    # see, which is the same shape one layer further away, so the driver has to hand them
    # over or they are unguardable.
    #  #425: from `used`, NOT from cfg -- see the note at boot_progress.  A second lookup
    #  here is exactly the hole this round measured.
    print("BUDGET=%d" % used["budget"])
    print("STALL=%d" % used["stall"])
    print("BACKSTOP=%d" % used["backstop"])
    reached = (reason == "MARKER")
    if reached:
        for step in cfg["steps"]:
            text, wait = step[0], step[1]
            confirm = step[2] if len(step) > 2 else None
            for attempt in range(tries if confirm else 1):
                if settle:
                    pump(settle)
                send(text)
                pump(wait)
                if confirm is None or re.search(confirm, buf):
                    break
                print("RETRY=%s attempt=%d" % (confirm, attempt + 1))

    try:
        os.write(fd, b"\x03")
        time.sleep(1.5)
        os.write(fd, b"quit\n")
        pump(5)
    except Exception:
        pass
    try:
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    # #420: flush whatever absorb() was holding. A fragment held back as a possible record
    # prefix is real console text if the run ended before it resolved, and dropping it would
    # silently truncate the log the verdict is computed from -- the same class of defect as
    # the lost 4 KB block that once faked a capability regression.
    if tail:
        # A final record that never received its newline is still a record; strip it with the
        # terminator-less pattern rather than writing it into the console log.
        m = REC_EOF.fullmatch(tail)
        if m:
            ninstrs = int(m.group(1))
        else:
            log.write(tail.encode("latin1", "replace"))
            buf += tail
        tail = ""
    log.close()
    raw.close()

    txt = open(log_path, "rb").read().decode("latin1", "replace")
    ok = True

    print("RIG=%s" % rig)
    print("BINARY=%s" % binary)
    print("LOG=%s" % log_path)
    print("BYTES=%d" % len(txt))
    print("BOOT_REACHED=%d" % (1 if reached else 0))
    if not reached:
        ok = False

    for m in cfg["markers"]:
        c = txt.count(m)
        print("MARKER_%s=%d" % (re.sub(r"\W", "_", m), c))
        if c == 0:
            ok = False

    # A rig with no expected values proves nothing about what the guest COMPUTED, only
    # that it survived. Treat that as a failure rather than silently printing no VALUES
    # line: with the gate comparing VALUES against VALUES_WANT, both absent compared
    # equal and the answer check went green while checking nothing.
    expectations = cfg.get("expect_values", {})
    if not expectations:
        print("VALUES=(no expectation declared)")
        print("VALUES_WANT=(none)")
        print("ERROR=rig declares no expect_values; it cannot check an answer")
        ok = False

    for pat, want in expectations.items():
        found = re.search(pat, txt)
        got = list(found.groups()) if found else []
        print("VALUES=%s" % (",".join(got) if got else "(none)"))
        print("VALUES_WANT=%s" % ",".join(want))
        if got != want:
            ok = False

    print("VERDICT=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in RIGS:
        sys.stderr.write("usage: drive_guest.py <%s> <emulator>\n"
                         % "|".join(sorted(RIGS)))
        sys.exit(2)
    sys.exit(drive(sys.argv[1], sys.argv[2]))
