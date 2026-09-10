# lcaiocstat0 -- DESIGN PRE-READ: four documented LCA IOC registers the model has never had (STAT0, STAT1, SFT_RST, PAR_DIS)

Please do not simply ratify. Check the premises, not just the derivations. ANALYSIS only -- prose, no
patch, no guest sequence. VERDICT LINE FIRST. Ordinary register-modelling engineering.

## THE TREE
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`. Ignore any other `src/` under the project root. Read
`src/devices/dev_lca.c` (`DEVICE_ACCESS(lca_ioc)`, the working tree carries the uncommitted `#518` diff),
`src/include/thirdparty/alpha_lcareg.h`, and the LOCAL manual `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\21066_66a_hrm.txt`
(Alpha 21066/21066A HRM; extracted tables STAGGER names against values -- prefer the prose, and calibrate
any table on a row below the value you cite).

## SETTLED (say which you cannot verify)
S1. The IOC handler's `switch` lists BASE, CONF (+0x020), TBIA, TB_ENA (+0x0a0), W_BASE0/1 (+0x100/+0x120),
    W_MASK0/1 (+0x140/+0x160), W_T_BASE0/1 (+0x180/+0x1a0); every other offset takes `default:`, which since
    `#518` declines a write (state untouched, one announce per direction) and answers a read with zero.
S2. The grok seat reported on `#518`'s pass 2 that STAT0 (+0x040), STAT1 (+0x060), SFT_RST (+0x0c0) and
    PAR_DIS (+0x0e0) are documented registers (HRM around `:10461`, `:10496`), that S6.4.14 items 1-2
    REQUIRE the SROM initialisation sequence to write SFT_RST and STAT0, and that `alpha_lcareg.h` defines
    STAT0/STAT1 with field masks and has no SFT_RST.
S3. Option-set members for an unimplemented register: 1 delete, 2 silent decline, 3 decline + latched
    announce (what `#518` shipped at `default:`), 4 accept (the model already computes it), 5 fault (not
    available on Alpha), 6 backed accept (invent storage), 7 implement.

## THE QUESTIONS -- answer extensionally with manual line citations
Q1. For each of the four registers: its fields and their types (R/W, W1C, RO, X), its reset value, and what
    the SROM sequence writes to it and why (quote S6.4.14). Which of them does any OTHER code in the fork
    read or consume (grep `src/` for STAT0/STAT1/SFT_RST/PAR_DIS and for `pcictl`/`rst`-style consumers)?
Q2. Disposition per register, from the option set: which member, and what it costs. In particular: is
    SFT_RST a write-only pulse (member 6 or 7 would need to DO something -- a PCI reset callback exists?
    grep `bus_pci` for a reset entry point) or a stored bit? Are STAT0/STAT1 W1C error logs that nothing in
    this model ever sets, so member 6 (backed accept: store, echo, W1C on write) is the honest floor?
Q3. Which guests reach these offsets: does NetBSD/alpha or Linux/alpha's LCA support write SFT_RST or read
    STAT0 (grep the fork's own comments; do not guess), and does the PROM sequence matter for an emulator
    that boots a kernel directly?
Q4. The detector shape for a member-6 round: rows per register (write, read back, W1C where applicable),
    and the (d) mutants a reviewer would build. Two lines each.
State what you read versus what you took from this packet. If, while verifying a claim, you found something
ELSE -- say so.
