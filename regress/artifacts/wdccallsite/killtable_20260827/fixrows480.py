"""#480 L1: three construction defects in my own rows, all named by pass-2 seats.

  (a) All three rows PRE-SET `d.cur_command` before calling wdc_command() -- which
      assigns it itself.  Redundant, and it WARPS entry-condition mutants: M11 tests
      `d->cur_command == idata`, so pre-setting it to the opcode about to be issued
      makes `same_cmd` true BY CONSTRUCTION.  In row_rejected that is not the
      scenario being tested at all (a real guest issuing PKT then IDENTIFY has
      cur_command == ATAPI_PKT_CMD when IDENTIFY arrives), so one of M11's three
      reds was an artifact of the fixture.  Named by the kimi-k3:cloud seat.

  (b) The rows assert their OUTCOME without asserting their SETUP reached the state
      it needed.  Named by codex: same-opcode should require occupancy 100 before
      the reissue; refill should require occupancy 510 after the abandoned word.
      (The WDCE_ABRT half of this was already fixed and measured.)

Both are L1 -- pre-ship construction, fixed before commit.
"""
import io, os

NL, T = chr(10), chr(9)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"
s = io.open(P, encoding="utf-8", newline="").read()


def span(name, nxt):
    a = s.index("static void %s(void)" % name)
    b = s.index("static void %s(void)" % nxt)
    return a, b


def edit(name, nxt, pairs):
    global s
    a, b = span(name, nxt)
    body = s[a:b]
    for old, new in pairs:
        n = body.count(old)
        assert n == 1, "%s: %r occurs %d" % (name, old[:46], n)
        body = body.replace(old, new, 1)
    s = s[:a] + body + s[b:]
    print("  %-28s %d edit(s)" % (name, len(pairs)))


#  ---- row_same_opcode_resets -------------------------------------------------
edit("row_same_opcode_resets", "row_rejected_cmd_resets", [
    #  (b) prove the 100 abandoned bytes are actually staged before the reissue
    (T + "stub_disk_writes = 0;" + NL,
     T + "/*  SETUP LIVENESS.  Without this the row asserts an outcome without" + NL +
     T + "    proving its premise: if the staging loop stopped working, the ring" + NL +
     T + "    would be empty and a clean 0xbb sector would land for a reason that" + NL +
     T + "    has nothing to do with the reset.  Named by the codex seat.  */" + NL +
     T + "{" + NL +
     T + T + "int staged = d.inbuf_head - d.inbuf_tail;" + NL +
     T + T + "while (staged < 0)" + NL +
     T + T + T + "staged += WDC_INBUF_SIZE;" + NL +
     T + T + "rows ++;" + NL +
     T + T + "if (staged != 100) {" + NL +
     T + T + T + "printf(\"  FAIL %-38s staged %i\\n\"," + NL +
     T + T + T + "    \"setup: 100 bytes are abandoned\", staged);" + NL +
     T + T + T + "failures ++;" + NL +
     T + T + "} else {" + NL +
     T + T + T + "printf(\"  ok   %-38s %i\\n\"," + NL +
     T + T + T + "    \"setup: 100 bytes are abandoned\", staged);" + NL +
     T + T + "}" + NL +
     T + "}" + NL + NL +
     T + "stub_disk_writes = 0;" + NL),
    #  (a) wdc_command() assigns cur_command itself; pre-setting it warps M11
    (T + "d.cur_command = WDCC_WRITE;" + NL + T + "wdc_command(fake_cpu(), &d, WDCC_WRITE);" + NL,
     T + "/*  NOT pre-set: wdc_command() assigns cur_command itself, and pre-setting" + NL +
     T + "    it makes M11's `cur_command == idata` true BY CONSTRUCTION.  Here the" + NL +
     T + "    same-opcode condition must come from the SCENARIO -- the previous" + NL +
     T + "    WDCC_WRITE left it set -- not from the fixture.  */" + NL +
     T + "wdc_command(fake_cpu(), &d, WDCC_WRITE);" + NL),
])

#  ---- row_rejected_cmd_resets ------------------------------------------------
edit("row_rejected_cmd_resets", "row_refill_cmd_resets", [
    (T + "d.cur_command = ATAPI_PKT_CMD;" + NL + T + "wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);" + NL,
     T + "wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);" + NL),
    (T + "d.cur_command = WDCC_IDENTIFY;" + NL + T + "wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);" + NL,
     T + "/*  NOT pre-set.  A real guest reaching here has cur_command ==" + NL +
     T + "    ATAPI_PKT_CMD, so IDENTIFY is a DIFFERENT opcode -- which is the" + NL +
     T + "    scenario.  Pre-setting it made M11 skip the reset here too and" + NL +
     T + "    contributed a red that was an artifact of the fixture rather than" + NL +
     T + "    of the defect.  Named by the kimi-k3:cloud seat.  */" + NL +
     T + "wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);" + NL),
])

#  ---- row_refill_cmd_resets --------------------------------------------------
edit("row_refill_cmd_resets", "row_arm_overrun", [
    (T + "d.cur_command = WDCC_IDENTIFY;" + NL +
     T + "wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);" + NL + NL +
     T + "/*  ...the guest reads one word and abandons it...  */" + NL,
     T + "wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);" + NL + NL +
     T + "/*  ...the guest reads one word and abandons it...  */" + NL),
    (T + "d.cur_command = WDCC_IDENTIFY;" + NL +
     T + "wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);" + NL + NL +
     T + "occ = d.inbuf_head - d.inbuf_tail;" + NL,
     T + "/*  SETUP LIVENESS.  510 bytes must actually be sitting there, or the" + NL +
     T + "    final occupancy-512 assertion is satisfied by a ring that was empty" + NL +
     T + "    all along and proves nothing about the flush.  Named by codex.  */" + NL +
     T + "{" + NL +
     T + T + "int left = d.inbuf_head - d.inbuf_tail;" + NL +
     T + T + "while (left < 0)" + NL +
     T + T + T + "left += WDC_INBUF_SIZE;" + NL +
     T + T + "rows ++;" + NL +
     T + T + "if (left != 510) {" + NL +
     T + T + T + "printf(\"  FAIL %-38s left %i\\n\"," + NL +
     T + T + T + "    \"setup: 510 bytes remain unread\", left);" + NL +
     T + T + T + "failures ++;" + NL +
     T + T + "} else {" + NL +
     T + T + T + "printf(\"  ok   %-38s %i\\n\"," + NL +
     T + T + T + "    \"setup: 510 bytes remain unread\", left);" + NL +
     T + T + "}" + NL +
     T + "}" + NL + NL +
     T + "wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);" + NL + NL +
     T + "occ = d.inbuf_head - d.inbuf_tail;" + NL),
])

#  two setup rows added -> 85
for a, b in [("if (rows != 83) {", "if (rows != 85) {"),
             ("rows = %i, want 83", "rows = %i, want 85")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

for lbl in ("setup: 100 bytes are abandoned", "setup: 510 bytes remain unread"):
    assert len(lbl) < 38, "label %d: %s" % (len(lbl), lbl)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  identity pin 83 -> 85")
