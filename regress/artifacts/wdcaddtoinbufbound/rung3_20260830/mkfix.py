"""Apply ONE candidate fix (or one mutant OF a candidate fix) to a tree copy's
dev_wdc.c.

Every replacement is COUNT-CHECKED: an anchor that matches 0 or >1 times is a
hard failure, never a silent no-op.  (A pattern that matches nothing reports a
clean, confident, wrong answer -- this project has paid for that repeatedly.)

TAB is chr(9) and is built by name rather than written as an escape, because
this file has been round-tripped through a shell heredoc and one backslash
level is consumed on that path in both directions.
"""
import sys

TAB = chr(9)
NL = chr(10)


def T(n):
    return TAB * n


variant, path = sys.argv[1], sys.argv[2]
src = open(path).read()

# ---- anchors ------------------------------------------------------------
# The WRITE arm's little-endian switch.  `cpu->byte_order == EMUL_LITTLE_ENDIAN`
# also appears in the READ arm, so the anchor carries the switch AND the first
# case lines to be unique.
W_ANCHOR = (
    T(3) + "if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {" + NL +
    T(4) + "switch (len) {" + NL +
    T(4) + "case 4:" + TAB + "wdc_addtoinbuf(d, idata & 0xff);" + NL +
    T(5) + "wdc_addtoinbuf(d, (idata >> 8) & 0xff);" + NL +
    T(5) + "wdc_addtoinbuf(d, (idata >> 16) & 0xff);" + NL
)
W_TAIL = W_ANCHOR.split(NL, 1)[1]

# The DATA-IN refill loop inside the re-arm (option b's site).
R_ANCHOR = (
    T(6) + "for (int j=0; j<d->atapi_len; j++)" + NL +
    T(7) + "wdc_addtoinbuf(d, d->atapi_st->" + NL +
    T(8) + "data_in[d->atapi_received + j]);" + NL
)

# fixA's own predicate, used as the anchor when mutating fixA.
FIXA_PRED = (
    T(3) + "if (d->atapi_cmd_in_progress &&" + NL +
    T(3) + "    d->atapi_phase != PHASE_CMDOUT) {" + NL
)


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.stderr.write("FATAL: anchor %s matched %d times (want 1)%s" % (label, n, NL))
        sys.exit(2)
    return text.replace(old, new)


def apply_fixA(text, note):
    new = (
        T(3) + "if (d->atapi_cmd_in_progress &&" + NL +
        T(3) + "    d->atapi_phase != PHASE_CMDOUT) {" + NL +
        T(4) + "/*  " + note + "  */" + NL +
        T(3) + "} else if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {" + NL
    ) + W_TAIL
    return sub(text, W_ANCHOR, new, "fixA/write-arm")


if variant == "fixA":
    #  OPTION (a): a phase guard on the data-port WRITE arm.
    #  Scoped to `atapi_cmd_in_progress && phase != PHASE_CMDOUT`, so ordinary
    #  ATA sector writes (write_in_progress, flag clear) are untouched, and the
    #  CDB-collection window (phase == PHASE_CMDOUT) is untouched.
    #  NO EARLY RETURN: control still reaches inbuf_len, the dispatch and the
    #  common tail, so the access stays handled (`return 1`).
    src = apply_fixA(src, "CANDIDATE FIX A: a packet command is active but we"
                          " are not collecting a CDB, so these bytes belong to"
                          " no transfer.  Refuse the PUSH ONLY -- the access is"
                          " still handled and falls through to the common tail.")

elif variant == "fixB":
    #  OPTION (b): the RE-ARM refuses to refill onto a dirty ring.  Implemented
    #  as a FLUSH of foreign bytes immediately before the refill push.
    new = (
        T(6) + "/*  CANDIDATE FIX B: drop anything the ring still holds" + NL +
        T(6) + "    before refilling, so chunk N+1 is what the guest" + NL +
        T(6) + "    reads next.  */" + NL +
        T(6) + "d->inbuf_head = d->inbuf_tail;" + NL
    ) + R_ANCHOR
    src = sub(src, R_ANCHOR, new, "fixB/refill")

elif variant in ("mutA1", "mutA2", "mutA3"):
    #  Mutants OF fixA.  Each is built by first applying fixA and then editing
    #  ITS OWN predicate, so every mutant differs from fixA by one expression.
    src = apply_fixA(src, "CANDIDATE FIX A (mutated: " + variant + ")")
    if variant == "mutA1":
        #  DROP THE FLAG CONJUNCT.  #477 records that BOTH conjuncts of the
        #  dispatch guard are load-bearing because the phase goes STALE; this
        #  asks the same question of the mirror guard.
        src = sub(src, FIXA_PRED,
                  T(3) + "if (d->atapi_phase != PHASE_CMDOUT) {" + NL,
                  "mutA1/drop-flag-conjunct")
    elif variant == "mutA2":
        #  CLAUSE (d): keep the guard, NULL ITS REPAIR.  Still reads as a phase
        #  check; no longer covers DATAIN.
        #  The predicate's SECOND LINE alone is NOT a unique anchor -- the
        #  re-arm at the read arm carries the same text at a different indent
        #  and the count check caught it -- so both lines are matched.
        src = sub(src, FIXA_PRED,
                  T(3) + "if (d->atapi_cmd_in_progress &&" + NL +
                  T(3) + "    d->atapi_phase == PHASE_COMPLETED) {" + NL,
                  "mutA2/null-repair")
    elif variant == "mutA3":
        #  CLAUSE (d) variant: qualify the guard with an access width, so it
        #  reads like the same check and covers strictly less.
        src = sub(src, FIXA_PRED,
                  T(3) + "if (d->atapi_cmd_in_progress &&" + NL +
                  T(3) + "    d->atapi_phase != PHASE_CMDOUT && len == 1) {" + NL,
                  "mutA3/width-qualified")

else:
    sys.stderr.write("unknown variant %s%s" % (variant, NL))
    sys.exit(2)

open(path, "w").write(src)
print("applied %s to %s" % (variant, path))
