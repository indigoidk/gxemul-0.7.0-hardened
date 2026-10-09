#  loop_row.py -- the Opus pass-2R5 PROTOTYPE of the `msr loop' row (Q2).  NOT a shipped file.
#  It is written to be pasted into arm_msrmode_probe.py just before the `row count' identity row
#  (probe48.py does exactly that) and it uses only that probe's own helpers (prog_session,
#  arming, dumped, dumpcmd, announces, row, diag_unimpl, WORDS, POISON).
#
#  ONE translated MSR re-executed inside a SINGLE `step N': no debugger interaction between the
#  passes, so debugger() never reaches "Clear all dyntrans translations" and every pass after the
#  first runs the SAME struct arm_instr_call -- the cached ic->arg[] the msr_imm comment says the
#  decline must not write.  Two MSRs are re-executed eight times each:
#    REGISTER form  msr cpsr_fsxc,r1  -- r1 loaded from a table each pass (accepts AND declines);
#                                        pins a decline that writes ic->arg[1] (M_msr_argmask: the
#                                        mask loses M[4:0], so every LATER accept through it is lost)
#    IMMEDIATE form msr cpsr_c,#0x14  -- always declined, from a DIFFERENT label each pass; pins a
#                                        decline that rewrites ic->arg[0] (M_msr_arg0cur: the next
#                                        pass from another label switches to the stale mode)
#  r1 r3 r5 r6 r7 are unbanked in every mode (FIQ banks r8-r14), and the table/output words live
#  on the DATA page (0x9000), never the code page, so no store invalidates a translation.
WORDS["ldr_r1_r5_p4"] = 0xE4951004           # ldr  r1, [r5], #4
WORDS["str_r3_r7_p4"] = 0xE4873004           # str  r3, [r7], #4
WORDS["subs_r6_1"] = 0xE2566001              # subs r6, r6, #1
WORDS["bne_m10"] = 0x1AFFFFF6                # bne  (.+8) - 40  = back to the ldr
LOOP_V = (0x11, 0x0E, 0x12, 0x17, 0x15, 0x1B, 0x1F, 0x13)    # accept, DECLINE, accept x2, DECLINE, x3
LOOP_TBL, LOOP_OUT = 0x9200, 0x9400
LOOP_OPS = ["ldr_r1_r5_p4", "msr_fsxc_r1", "mrs_r3", "str_r3_r7_p4",
            "c_14", "mrs_r3", "str_r3_r7_p4", "subs_r6_1", "bne_m10"]
_lbad = []
for _k, _w in (("ldr_r1_r5_p4", WORDS["ldr_r1_r5_p4"]), ("str_r3_r7_p4", WORDS["str_r3_r7_p4"])):
    #  single data transfer, immediate offset 4, POST-indexed (P=0, W=0), U=1, B=0
    _rn = {"ldr_r1_r5_p4": 5, "str_r3_r7_p4": 7}[_k]
    _rd = {"ldr_r1_r5_p4": 1, "str_r3_r7_p4": 3}[_k]
    _l = {"ldr_r1_r5_p4": 1, "str_r3_r7_p4": 0}[_k]
    if not (_w >> 28 == 0xE and (_w >> 25) & 7 == 2 and not (_w >> 24) & 1 and (_w >> 23) & 1
            and not (_w >> 22) & 1 and not (_w >> 21) & 1 and (_w >> 20) & 1 == _l
            and (_w >> 16) & 0xF == _rn and (_w >> 12) & 0xF == _rd and _w & 0xFFF == 4):
        _lbad.append(_k)
_w = WORDS["subs_r6_1"]
if not (_w >> 28 == 0xE and (_w >> 25) & 7 == 1 and (_w >> 21) & 0xF == 2 and (_w >> 20) & 1
        and (_w >> 16) & 0xF == 6 and (_w >> 12) & 0xF == 6 and _w & 0xFFF == 1):
    _lbad.append("subs_r6_1")
_w = WORDS["bne_m10"]
_off = _w & 0xFFFFFF
_off = _off - (1 << 24) if _off & 0x800000 else _off
#  the bne is LOOP_OPS[8]: target = its address + 8 + 4*off must be LOOP_OPS[0]
if not (_w >> 28 == 0x1 and (_w >> 24) & 0xF == 0xA and 8 + 4 * _off == -4 * 8):
    _lbad.append("bne_m10")
_want_loop = []
_m = 0x13                                    # boot SVC32, after the prefix
for _v in LOOP_V:
    if _v in MODELLED:
        _m = _v
    _want_loop += [_m, _m]                   # reg-form result, then the #0x14 decline (label kept)
early, late, alive, marked, full = prog_session(
    LOOP_OPS,
    data=dict([(LOOP_TBL + 4 * i, v) for i, v in enumerate(LOOP_V)]
              + [(LOOP_OUT + 4 * i, POISON) for i in range(2 * len(LOOP_V))]),
    regs=["r5=0x%x" % LOOP_TBL, "r6=%d" % len(LOOP_V), "r7=0x%x" % LOOP_OUT],
    segments=(((), 9 * len(LOOP_V)), ([dumpcmd(LOOP_OUT, LOOP_OUT + 8 * len(LOOP_V) - 4)], 0)))
if _lbad:
    got = "enc " + ",".join(_lbad)
elif not marked or not arming(early, full):
    got = "unarmed"
elif not alive:
    got = "dead"
else:
    vals = [dumped(late, LOOP_OUT + 4 * i) for i in range(2 * len(LOOP_V))]
    t = early + late
    got = " ".join("nofire" if v in (None, POISON) else "%x" % v for v in vals) \
        + " n=%d" % announces(t, "msr_imm")
    if announces(t, "register_bank"):
        got += " bank=%d" % announces(t, "register_bank")
row("msr loop", got, " ".join("%x" % v for v in _want_loop) + " n=1",
    "ONE translated reg MSR and #0x14 MSR re-run 8x in ONE step: ic->arg[] never written.")
diag_unimpl("msr loop", early + late)
