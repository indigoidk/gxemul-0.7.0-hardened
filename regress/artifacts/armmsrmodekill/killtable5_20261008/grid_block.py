# ---------------------------------------------------------------- #562 repair 5: the GENERATED GRID
#  Owner ruling 2026-10-08: the restore/MSR detector rows are GENERATED from the full space, not
#  written by hand.  Three sessions (one per path: msr_imm, DPI S-to-PC, arm_pop), each a list of
#  OBSERVATIONS produced by grid_obs() below.  One observation:
#      debugger:  cpsr=0xd3 (re-arm; a previous result may have T set), pc=<block>, r0=OLD, r1=NEW
#      guest:     msr cpsr_fsxc,r0           -- OLD CPSR, a modelled label, set by a real MSR
#                                               (bank switch and `flags' both correct)
#                 msr spsr_fsxc,r1           -- (restore paths only) SPSR := NEW
#                 the instruction under test -- msr cpsr_fsxc,r1 / movs pc,r2 / ldmia r6,{pc}^
#                                               (pop also: ldmia r6,{pc}, ldmia r6,{r0}^, ldmia r6,{r0})
#      debugger:  print cpsr                 -- the WHOLE result word, compared exactly with WANT
#  WANT is computed: accept -> NEW; decline -> (NEW & ~0x1f) | label; a non-restoring pop form
#  -> OLD.  The first decline in a session runs with the site's latch CLEAR, every later one with
#  it SET; the site must announce exactly once and no Save/Load backstop text may appear.
#
#  G1 per path x outcome x bit 0..31 x polarity: observations come in COMPLEMENTARY PAIRS --
#     p1: OLD = label (bits 31:5 all 0)          NEW = 0xffffffe0 | mode (bits 31:5 all 1, T SET)
#     p2: OLD = 0xffffffc0 | label (31:6 all 1)  NEW = mode (bits 31:5 all 0)
#     so for every non-mode bit both result polarities are observed with the OLD value different
#     (keep-old, force-0 and force-1 all change the word).  T cannot be 1 in OLD (the guest runs
#     ARM code), so T polarity 0 is observed only with OLD T = 0 -- keep-old T is caught at p1.
#  G2 MSR label x mode bit: each label also declines label ^ 0x1f, which differs in EVERY mode bit
#     (and is always unmodelled, since bit 4 is cleared); on the restore paths the same value is
#     the declined SPSR, so a keep-mode mask that lets any SPSR mode bit through changes the word.
#  G3 helper boundary: ALL 25 unmodelled values (0x00-0x0f, 0x14-0x16, 0x18-0x1a, 0x1c-0x1e) are
#     declined on EVERY path, labels cycling; ALL 7 modelled modes are accepted on every path.
#     A narrowed projection (e.g. `& 0x17' admits 0x18-0x1a) or widened one changes some word.
#  G4 pop enclosing cells: {S, non-S} x {PC, no PC} all four, both polarities.
#  The `grid cov' row re-derives the bit x polarity table from the generated observations and
#  reds if any cell outside the named equivalents is uncovered.
MODELLED = (0x10, 0x11, 0x12, 0x13, 0x17, 0x1B, 0x1F)
UNMODELLED = tuple(m for m in range(32) if m not in MODELLED)          # 25 values
RESTORE_LABELS = (0x11, 0x12, 0x13, 0x17, 0x1B)                        # SPSR-bearing
MSR_LABELS = (0x11, 0x12, 0x13, 0x17, 0x1B, 0x1F)                      # USR strips the c-byte
WORDS["msr_spsr_fsxc_r1"] = 0xE16FF001       # msr spsr_fsxc, r1
WORDS["movs_pc_r2"] = 0xE1B0F002             # movs pc, r2
WORDS["ldm_r6_pc"] = 0xE8968000              # ldmia r6, {pc}        (non-S, PC)
WORDS["ldm_r6_r0_s"] = 0xE8D60001            # ldmia r6, {r0}^       (S, no PC)
WORDS["ldm_r6_r0"] = 0xE8960001              # ldmia r6, {r0}        (non-S, no PC)
GRID_CHECK = {"msr_spsr_fsxc_r1": lambda w: w & 0x0FFFFFF0 == 0x016FF000 and w & 0xF == 1,
              "movs_pc_r2": lambda w: (w >> 21) & 0xF == 0xD and (w >> 20) & 1
              and (w >> 12) & 0xF == 15 and w & 0xFFF == 2 and (w >> 25) & 7 == 0,
              "ldm_r6_pc": lambda w: w & 0x0FFFFFFF == 0x08968000,
              "ldm_r6_r0_s": lambda w: w & 0x0FFFFFFF == 0x08D60001,
              "ldm_r6_r0": lambda w: w & 0x0FFFFFFF == 0x08960001}
GBAD = [k for k, f in GRID_CHECK.items() if not f(WORDS[k]) or WORDS[k] >> 28 != 0xE]
for k in ("ldm_r6_pc_s",):
    if WORDS[k] & 0x0FFFFFFF != 0x08D68000:
        GBAD.append(k)

HI1, HI0 = 0xFFFFFFE0, 0xFFFFFFC0             # bits 31:5 set (T set) / bits 31:6 set (T clear)


def grid_obs(path):
    """[(kind, label, OLD, NEW, WANT)] for one path -- the whole generated table."""
    labels = MSR_LABELS if path == "msr" else RESTORE_LABELS
    obs = []

    def add(kind, lab, new, pol):
        old = lab if pol == 1 else (HI0 | lab)
        newv = (HI1 | new) if pol == 1 else new
        if kind == "acc":
            want = newv
        elif kind == "dec":
            want = (newv & ~0x1F) | lab
        else:                                    # non-restoring pop forms
            want = old
        obs.append((kind, lab, old, newv, want))

    i = 0
    for lab in labels:                           # G2 complement declines, both polarities
        for pol in (1, 2):
            add("dec", lab, lab ^ 0x1F, pol)
    for m in UNMODELLED:                         # G3 every unmodelled value
        add("dec", labels[i % len(labels)], m, 1 + (i % 2))
        i += 1
    j = 0
    for lab in labels:                           # accepts: every modelled mode, both polarities,
        for pol in (1, 2):                       # mode != label
            cands = [m for m in MODELLED if m != lab]
            add("acc", lab, cands[(j * 3) % len(cands)], pol)
            j += 1
    for m in MODELLED:                           # and every modelled mode as an accept target
        lab = [l for l in labels if l != m][j % (len(labels) - 1)]
        add("acc", lab, m, 1 + (j % 2))
        j += 1
    if path == "pop":                            # G4 the three non-restoring enclosing cells
        for kind in ("ldm_pc", "ldm_r0_s", "ldm_r0"):
            for pol in (1, 2):
                add(kind, 0x13 if pol == 1 else 0x12, 0x1F, pol)
    return obs


def grid_cov(path):
    """Uncovered (outcome, bit, polarity) cells of path's observations, outside the named
    equivalents.  Covered: some observation whose WANT bit == pol while the alternative differs --
    OLD's bit for every non-mode bit and for accept mode bits, NEW's (the SPSR / operand's) bit
    for decline mode bits.  Named equivalents: bit 4 polarity 0 (no modelled mode or label has it
    clear), bit 4 on ACCEPT at either polarity (OLD's bit 4 is always 1, as is the accepted
    mode's, so keep-old and force-1 equal the right answer), and bit 5 polarity 0 vs OLD (OLD T
    is always 0: the guest runs ARM code)."""
    miss = []
    obs = grid_obs(path)
    for outc in ("acc", "dec"):
        for bit in range(32):
            for pol in (0, 1):
                if (bit == 4 and pol == 0) or (bit == 5 and pol == 0) or                         (bit == 4 and outc == "acc"):
                    continue
                ok = False
                for kind, lab, old, new, want in obs:
                    if kind != outc or ((want >> bit) & 1) != pol:
                        continue
                    alt = new if (outc == "dec" and bit < 5) else old
                    if ((alt >> bit) & 1) != pol:
                        ok = True
                        break
                if not ok:
                    miss.append("%s/b%d/%d" % (outc, bit, pol))
    return miss


GRID_SITE = {"msr": "msr_imm", "dpi": "dpi S-to-pc", "pop": "arm_pop"}
GB0, GB1, GB2, GB3, GTGT = 0x8200, 0x8240, 0x8280, 0x82C0, 0x8300
for path in ("msr", "dpi", "pop"):
    obs = grid_obs(path)
    if path == "msr":
        blocks = [(GB0, ["msr_fsxc_r0", "msr_fsxc_r1"])]
        where = {"acc": (GB0, 2), "dec": (GB0, 2)}
    elif path == "dpi":
        blocks = [(GB0, ["msr_fsxc_r0", "msr_spsr_fsxc_r1", "movs_pc_r2"]), (GTGT, [])]
        where = {"acc": (GB0, 3), "dec": (GB0, 3)}
    else:
        blocks = [(GB0, ["msr_fsxc_r0", "msr_spsr_fsxc_r1", "ldm_r6_pc_s"]),
                  (GB1, ["msr_fsxc_r0", "msr_spsr_fsxc_r1", "ldm_r6_pc"]),
                  (GB2, ["msr_fsxc_r0", "msr_spsr_fsxc_r1", "ldm_r6_r0_s"]),
                  (GB3, ["msr_fsxc_r0", "msr_spsr_fsxc_r1", "ldm_r6_r0"]), (GTGT, [])]
        where = {"acc": (GB0, 3), "dec": (GB0, 3), "ldm_pc": (GB1, 3), "ldm_r0_s": (GB2, 3),
                 "ldm_r0": (GB3, 3)}
    segs = [((), 0)]
    first = True
    for kind, lab, old, new, want in obs:
        pc, nst = where[kind]
        pk = ([] if first else ["print cpsr"]) + ["cpsr=0xd3", "pc=0x%x" % pc,
                                                  "r0=0x%x" % old, "r1=0x%x" % new]
        segs.append((pk, nst))
        first = False
    segs.append((["print cpsr"], 0))
    early, late, alive, marked, full = prog_session(
        [], blocks=blocks, data={LDMW: GTGT},
        regs=["r2=0x%x" % GTGT, "r6=0x%x" % LDMW], segments=tuple(segs))
    if GBAD:
        got = "enc " + ",".join(GBAD)
    elif not marked or not arming(early, full):
        got = "unarmed"
    elif not alive:
        got = "dead"
    else:
        vals = [int(v, 16) for v in re.findall(r"print\s+cpsr\s*\n\s*(0x[0-9a-f]+)", late)]
        bad = ["%d:%08x!=%08x" % (k, v, o[4]) for k, (v, o) in enumerate(zip(vals, obs))
               if v != o[4]]
        t = early + late
        nbank = announces(t, "register_bank")
        got = "%d/%d n=%d" % (len(vals) - len(bad), len(obs), announces(t, GRID_SITE[path]))
        if len(vals) != len(obs):
            got += " read=%d" % len(vals)
        if nbank:
            got += " bank=%d" % nbank
        if bad:
            got += " " + " ".join(bad[:2])
            diagnosis.append("grid %s mismatches: %s" % (path, " ".join(bad[:12])))
    row("grid %s" % path, got, "%d/%d n=1" % (len(obs), len(obs)),
        "GENERATED: %d observations (G1-G4) on the %s path; whole-CPSR readback each." %
        (len(obs), path))
    diag_unimpl("grid %s" % path, early + late)

GMISS = sum((["%s:%s" % (p, c) for c in grid_cov(p)] for p in ("msr", "dpi", "pop")), [])
row("grid cov", "%d uncovered" % len(GMISS), "0 uncovered",
    "Static: every (path, outcome, bit, polarity) cell outside the named equivalents is observed.")
if GMISS:
    diagnosis.append("grid cov uncovered: " + " ".join(GMISS[:20]))

