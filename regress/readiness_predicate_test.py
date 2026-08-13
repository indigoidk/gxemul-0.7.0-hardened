#!/usr/bin/env python3
"""#392: the readiness predicate, proved offline.

WHY THIS EXISTS. The defect it guards was an intermittent flake for months: the
probes' readiness predicate could return before a command's reply had been read.
Reproducing it live needed a guest, a pty and a 1-byte reader, and even then the
failure was a scheduler race. This test removes the race entirely -- the wait()
loop is replayed over a SCRIPTED byte stream, so the answer is deterministic and
depends on no emulator, no pty and no host timing.

That last point is deliberate. This project has already had a 45-minute battery
false-FAIL because a wall-clock budget was used as an oracle under host load. A
readiness test whose verdict moves with host speed would be the same mistake.

WHAT IT PROVES. Four predicate forms are replayed against the same stream:

    bare '>'  + whole buffer     the committed form before #392
    full      + whole buffer     the "obvious" fix -- AND IT DOES NOT WORK
    bare '>'  + fresh mark       the other half alone -- also does not work
    full      + fresh mark       the shipped form

Only the fourth reads the new command's reply. The other three return early.

THE MECHANISM, which is easy to get backwards. The debugger prompt is "GXemul> "
WITH A TRAILING SPACE. A wait that stops as soon as it has seen "...GXemul>"
leaves that space unread. The NEXT wait's first read consumes exactly that one
byte -- and rstrip() then DELETES IT AGAIN, so a whole-buffer predicate matches
the SAME prompt a second time and returns having read nothing of the new reply.
rstrip() erases the only evidence that the prompt was already consumed. That is
why a stricter prompt STRING cannot help: the string it matches is a real prompt,
just the wrong one. Measured against the live probe, the bare and full
whole-buffer arms scored identically (0/80, same rows dead, same two rows wrong),
which is exactly what this predicts.

SCOPE, stated so nobody reads more into a green than it carries: this file tests
the four FORMS, not the probes. On its own it would stay green if a probe were
reverted. The static census in gate_hygiene.sh is what ties the shipped code to
this result -- it counts the converted sites and fails if one goes back. The two
checks are only meaningful together.
"""

PROMPT = "GXemul> "

#  A scripted session, byte-for-byte as a pty delivers it: the previous command's
#  reply and prompt, then the new command's echo, its reply, and its prompt. The
#  register-dump line is the real one (cpu_m88k.c:277 and its siblings print
#  "  <%s>\n" with " no symbol " as the fallback), because its trailing '>' is
#  what the bare form matches.
PREV_REPLY = "cpu0:  pc  = 0x00010000  < no symbol >\r\n"
NEW_ECHO = "reg\r\n"
NEW_REPLY = "cpu0:  pc  = 0x00000400  < no symbol >\r\n"


def replay(predicate):
    """Run two consecutive wait() loops over the scripted stream.

    Returns (bytes the SECOND wait consumed, whether it saw the new reply).
    One byte per read, so the predicate is evaluated at every boundary the race
    could land on -- this is what turns the race into a certainty.
    """
    stream = PREV_REPLY + PROMPT + NEW_ECHO + NEW_REPLY + PROMPT
    buf = ""
    pos = 0

    def rd():
        nonlocal buf, pos
        if pos >= len(stream):
            return False
        buf += stream[pos]
        pos += 1
        return True

    while rd():                       # the PREVIOUS command's wait
        if predicate(buf, 0):
            break

    mark = len(buf)                   # taken BEFORE the next write, as send() does
    start = pos
    while rd():                       # the wait under test
        if predicate(buf, mark):
            break

    return pos - start, NEW_REPLY.strip() in buf[mark:]


ARMS = [
    ("bare-whole", lambda b, m: b.rstrip().endswith(">"), False),
    ("full-whole", lambda b, m: b.rstrip().endswith("GXemul>"), False),
    ("bare-mark", lambda b, m: len(b) > m and b[m:].rstrip().endswith(">"), False),
    ("full-mark", lambda b, m: len(b) > m and b[m:].rstrip().endswith("GXemul>"), True),
]

bad = 0
for name, pred, want_saw in ARMS:
    consumed, saw = replay(pred)
    ok = (saw == want_saw)
    if not ok:
        bad += 1
    print("READINESS_ROW %-12s bytes=%-4d saw_reply=%-3s want=%-3s %s"
          % (name, consumed, "yes" if saw else "no",
             "yes" if want_saw else "no", "ok" if ok else "FAIL"))


#  ---- SCENARIO B: the LATE PROMPT, which is what the echo guard is for -------
#
#  The four arms above prove the MARK and the PROMPT STRING. They do NOT touch
#  the echo conjunct -- a review seat measured that the echo half could be
#  deleted from all fourteen sites with every gate still green, because nothing
#  executed it. This scenario is that missing coverage.
#
#  The situation: a PREVIOUS command's prompt is still in flight when the next
#  command's mark is taken, so it lands INSIDE the new slice. Byte anchoring
#  cannot help -- the stale prompt is genuinely after the mark. Only requiring
#  the new command's own echo first can tell the two prompts apart, because the
#  debugger emits the echo only when it starts consuming that command
#  (debugger.c:589).
LATE = PROMPT + NEW_ECHO + NEW_REPLY + PROMPT


def replay_late(predicate):
    """Everything arrives AFTER the mark, beginning with the stale prompt."""
    buf = ""
    pos = 0

    def rd():
        nonlocal buf, pos
        if pos >= len(LATE):
            return False
        buf += LATE[pos]
        pos += 1
        return True

    mark = 0
    while rd():
        if predicate(buf, mark, NEW_ECHO.strip()):
            break
    return pos, NEW_REPLY.strip() in buf[mark:]


LATE_ARMS = [
    #  no echo requirement: the stale prompt ends the wait immediately
    ("late-noecho", lambda b, m, e: len(b) > m and b[m:].rstrip().endswith("GXemul>"), False),
    #  the shipped form: the echo must appear before any prompt is accepted
    ("late-echo",
     lambda b, m, e: (e in b[m:]) and len(b) > m and b[m:].rstrip().endswith("GXemul>"), True),
]
for name, pred, want_saw in LATE_ARMS:
    consumed, saw = replay_late(pred)
    ok = (saw == want_saw)
    if not ok:
        bad += 1
    print("READINESS_ROW %-12s bytes=%-4d saw_reply=%-3s want=%-3s %s"
          % (name, consumed, "yes" if saw else "no",
             "yes" if want_saw else "no", "ok" if ok else "FAIL"))

#  The leftover byte, printed rather than asserted in prose, so a reader can see
#  the mechanism instead of taking it on trust.
seen = PREV_REPLY + PROMPT
print("READINESS_LEFTOVER stripped=%r keeps_prompt=%s"
      % (PROMPT[-1], "yes" if seen.rstrip().endswith("GXemul>") else "no"))
print("READINESS_RESULT=%d/%d" % (len(ARMS) + len(LATE_ARMS) - bad,
                                 len(ARMS) + len(LATE_ARMS)))
