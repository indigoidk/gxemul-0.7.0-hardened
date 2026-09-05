import io, os, pty, re, select, sys, time
#  RUNG-3 WITNESS for pcc2defaultkill, run under WSL against a named binary: real guest loads and stores (and
#  cold-debugger puts) at offsets with no `case' in DEVICE_ACCESS(pcc2), on the UNMODIFIED mvme187 machine, through
#  real decode and memory_rw.  Pre-fix: the host process exits (`default: exit(1)').  Post-fix: it survives and the
#  controls still hold.
#  The pty SESSION HELPER IS THE PROBE'S OWN, extracted from regress/pcc2_width_probe.py at run time -- the first
#  draft hand-rolled one and its prompt detection accepted a STALE prompt, so a host that died mid-command read as
#  "survived" (every row green on a build that kills).  The carrier says not to hand-roll pty plumbing; this is why.
#  Encoders and register convention are the probe's too (r2 = PCC2 base, r3 = scratch, r4 = load target, r5 = store
#  source; ld.bu is op 0x03).  Controls: LIVENESS (the probe's scratch st/ld round-trip) and DEVICE-SIGNATURE (CHIPID
#  reads PCC2_ID 0x20, which RAM would not).  Usage: python3 defaultkill_witness.py <gxemul> <label>
#  Emits DEFAULTKILL_WITNESS_DONE last; a session that dies says how in its own row.
BIN, LABEL = sys.argv[1], sys.argv[2]
DUMMY = "/tmp/pcc2_dummy.bin"
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 4096)
PROBE = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/pcc2_width_probe.py"
psrc = io.open(PROBE, encoding="utf-8").read()
i = psrc.index("def session("); j = psrc.index("\ndef printed")
exec(psrc[i:j])           # session(cmds, settle, spin) -> (transcript, alive, how); how in exit0/exit1/killed/no-breakpoint/...
CODE, SCRATCH, PCC2, SENTINEL, CHIPID = 0x00010000, 0x00020000, 0xfff42000, 0xdeadbeef, 0x00
IEICR, IEBERR, IEERR, T1CMP_B1, ALIAS_IEICR, GENCTL = 0x2a, 0x2b, 0x28, 0x05, 0x6a, 0x02
def enc(op26, rd, rs1, imm): return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)
def LD_BU(rd, off): return enc(0x03, rd, 2, off)
def ST_B(rs, off): return enc(0x0b, rs, 2, off)
I_ST_SCR = enc(0x09, 5, 3, 0); I_LD_SCR = enc(0x05, 4, 3, 0); I_BR_SELF = 0xc0000000
def program(insns, at=CODE):
    words = list(insns) + [I_BR_SELF, 0]
    return ["put w 0x%x, 0x%08x" % (at + 4 * k, w) for k, w in enumerate(words)] + ["pc=0x%x" % at, "step %d" % len(insns)]
def setup(r5="0x5a5a5a5a"):
    return ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=%s" % r5, "r4=0x%x" % SENTINEL]
def val(t, reg="r4"):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t); return m.group(1) if m else "absent"
def fate(alive, how): return "survived" if alive else "host " + how
rows = []
def row(name, got, want, why):
    rows.append((name, str(got), str(want)))
    print("%-16s %-14s %-14s %-4s %s" % (name, got, want, "ok" if str(got) == str(want) else "FAIL", why), flush=True)
def unimpl(t): return t.count("pcc2: unimplemented")
print("pcc2defaultkill WITNESS -- binary=%s label=%s (session() = the probe's own)" % (BIN, LABEL))
t, alive, how = session(setup() + program([I_ST_SCR, I_LD_SCR]) + ["print r4"])
row("live", val(t) if alive else fate(alive, how), "0x5a5a5a5a", "LIVENESS: the probe's own scratch st/ld round-trip")
t, alive, how = session(setup() + program([LD_BU(4, CHIPID)]) + ["print r4"])
row("devsig chipid", val(t) if alive else fate(alive, how), "0x20", "DEVICE-SIGNATURE: CHIPID reads PCC2_ID through a guest ld.bu (RAM would read 0)")
t, alive, how = session(setup(r5="0x0") + program([ST_B(5, IEICR)]))
row("ieicr st.b", fate(alive, how), "survived", "GUEST byte store to IEICR (0x2a) -- the write if_ie.c makes at attach; no case -> default:")
row("ieicr st.b msg", unimpl(t), 1, "the default: arm's own 'pcc2: unimplemented' line was printed (the arm was REACHED)")
t, alive, how = session(setup() + program([LD_BU(4, IEICR)]) + ["print r4"])
row("ieicr ld.bu", fate(alive, how), "survived", "GUEST byte load of IEICR: the memcpy serves it, then default: -- the READ side")
row("ieicr ld.bu msg", unimpl(t), 1, "the default: arm reached on the READ too")
row("ieicr rd val", val(t) if alive else "n/a (" + fate(alive, how) + ")", "0x0", "the served value (post-fix): the register array's byte")
t, alive, how = session(["put b 0xfff4202a, 0x00"])
row("ieicr put b", fate(alive, how), "survived", "the operator path (cold-debugger put b); the carrier says put b never reaches a DM_DEFAULT arm -- a CONTROL")
row("ieicr put b msg", unimpl(t), 0, "...so no 'unimplemented' line: the arm was NOT reached by put b")
t, alive, how = session(setup(r5="0x0") + program([ST_B(5, IEBERR), ST_B(5, IEERR)]))
row("ieberr/ieerr", fate(alive, how), "survived", "the other two if_ie.c targets (0x2b, 0x28)")
t, alive, how = session(setup(r5="0x0") + program([ST_B(5, T1CMP_B1)]))
row("t1cmp+1 st.b", fate(alive, how), "survived", "a BYTE inside the T1CMP word (0x05): no case -> default:")
t, alive, how = session(setup(r5="0x0") + program([ST_B(5, ALIAS_IEICR)]))
row("alias 0x6a", fate(alive, how), "survived", "the %= PCC2_SIZE fold: 0x6a aliases IEICR")
t, alive, how = session(setup(r5="0x82") + program([ST_B(5, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
row("genctl rt", val(t) if alive else fate(alive, how), "0x82", "an IMPLEMENTED register still round-trips (the fix must not perturb the cased arms)")
ok = sum(1 for r in rows if r[1] == r[2])
print("DEFAULTKILL_RESULT=%d/%d label=%s binary=%s" % (ok, len(rows), LABEL, BIN))
print("DEFAULTKILL_WITNESS_DONE")
