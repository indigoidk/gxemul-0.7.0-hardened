import io, sys
#  Apply ONE named mutant to <tree>/src/cpus/cpu_m88k.c (the FIXED source).  Every mutant asserts its find-text exactly once
#  (a find-text that matches nothing is a FAIL, never a silent no-op -- MUTANT-TEXT-NOT-FOUND is itself a presence pin).
#  Usage: python3 mut_m88kexc.py <tree> <mutant>
tree, mut = sys.argv[1], sys.argv[2]
p = tree + "/src/cpus/cpu_m88k.c"
s = io.open(p, encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, ("MUTANT-TEXT-NOT-FOUND", mut, old[:60], n)
    s = s.replace(old, new)
IMPL = "\t\timplemented = true;\t/*  m88kexcdeliver  */\n"
CLASSES = ["MISALIGNED_ACCESS", "UNIMPLEMENTED_OPCODE", "PRIVILEGE_VIOLATION", "BOUNDS_CHECK_VIOLATION",
           "ILLEGAL_INTEGER_DIVIDE", "INTEGER_OVERFLOW", "ERROR"]
TAIL = "".join("\t\tcase M88K_EXCEPTION_%s:\n" % c for c in CLASSES)
if mut == "M_REVERT":            # floor (b): every class back to the fallback (implemented stays false)
    rep(IMPL, "\t\t/* M_REVERT */\n", count=7)
elif mut == "M_REVERT1":         # one class (BOUNDS_CHECK) back to the fallback
    rep('"BOUNDS_CHECK_VIOLATION", VERBOSITY_INFO, "");\n' + IMPL,
        '"BOUNDS_CHECK_VIOLATION", VERBOSITY_INFO, "");\n\t\t/* M_REVERT1 */\n')
elif mut == "M_ERRORDROP":       # ERROR alone back to the fallback
    rep('"ERROR", VERBOSITY_INFO, "");\n' + IMPL, '"ERROR", VERBOSITY_INFO, "");\n\t\t/* M_ERRORDROP */\n')
elif mut == "M_NAIVE":           # the one-site form: keep implemented, drop the seven tail labels
    rep(TAIL, "\t\t/* M_NAIVE: tail labels removed */\n")
elif mut == "M_VEC4":
    rep("\tcpu->pc = cpu->cd.m88k.cr[M88K_CR_VBR] + 8 * vector;\n", "\tcpu->pc = cpu->cd.m88k.cr[M88K_CR_VBR] + 4 * vector;\n")
elif mut == "M_NOSHADOW":        # skip the shadow update whenever the vector is one of the seven
    rep("\tif (update_shadow_regs) {\n\t\tcpu->cd.m88k.cr[M88K_CR_SSBR] = 0;\n",
        "\tif (update_shadow_regs && !(vector >= 4 && vector <= 10)) {\n\t\tcpu->cd.m88k.cr[M88K_CR_SSBR] = 0;\n")
elif mut == "M_NOSFRZ":
    rep("\t    | M88K_PSR_SFRZ\t/*  Freeze shadow registers,          */\n", "\t    | 0\t/*  M_NOSFRZ  */\n")
elif mut == "M_NOMODE":
    rep("\t    | M88K_PSR_MODE,\t/*  and switch to supervisor mode.    */\n", "\t    | 0,\t/*  M_NOMODE  */\n")
elif mut == "M_SNIPX":           # the non-delay-slot return address becomes the faulting pc
    rep("\t\t} else {\n\t\t\tcpu->cd.m88k.cr[M88K_CR_SNIP] = (cpu->pc + 4) | M88K_NIP_V;\n",
        "\t\t} else {\n\t\t\tcpu->cd.m88k.cr[M88K_CR_SNIP] = (cpu->pc) | M88K_NIP_V;\n")
elif mut == "M_NOEPSR":          # skip the EPSR save
    rep("\t\t/*  Freeze shadow registers, and save the PSR:  */\n\t\tcpu->cd.m88k.cr[M88K_CR_EPSR] = cpu->cd.m88k.cr[M88K_CR_PSR];\n",
        "\t\t/*  M_NOEPSR  */\n")
elif mut == "M_TAILRETURN":      # the new arms return instead of break (skips m88k_pc_to_pointers)
    rep("\t\t\t    SSBR keeps its old value) and fcr2/fcr4/fcr5 for the divide.  */\n\t\t\tbreak;\n",
        "\t\t\t    SSBR keeps its old value) and fcr2/fcr4/fcr5 for the divide.  */\n\t\t\treturn;\t/* M_TAILRETURN */\n")
elif mut == "M_DSLOT":           # the else-arm's SFIP loses the delay target
    rep("\t\t\t\tcpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;\n\t\t\t}\n",
        "\t\t\t\tcpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.cr[M88K_CR_SNIP] + 4;\n\t\t\t}\n")
elif mut == "M_ERRORTAIL":      # drop ONLY the ERROR tail label (the double-fault route then hits the tail default)
    rep("\t\tcase M88K_EXCEPTION_INTEGER_OVERFLOW:\n\t\tcase M88K_EXCEPTION_ERROR:\n",
        "\t\tcase M88K_EXCEPTION_INTEGER_OVERFLOW:\n\t\t/* M_ERRORTAIL */\n")
elif mut == "M_ISTRAP":         # the four instruction-route classes deliver only when NOT named by a trap (grok/deepseek pass-2 shape)
    for c in ["MISALIGNED_ACCESS", "UNIMPLEMENTED_OPCODE", "PRIVILEGE_VIOLATION", "ILLEGAL_INTEGER_DIVIDE", "INTEGER_OVERFLOW"]:
        rep('"%s", VERBOSITY_INFO, "");\n' % c + IMPL,
            '"%s", VERBOSITY_INFO, "");\n' % c + "\t\tif (!is_trap) implemented = true;\t/* M_ISTRAP */\n")
elif mut == "M_TRAPONLY":       # BOUNDS delivers only when named by a trap -- EXPECTED EQUIVALENT (no instruction raises 7); disclosed
    rep('"BOUNDS_CHECK_VIOLATION", VERBOSITY_INFO, "");\n' + IMPL,
        '"BOUNDS_CHECK_VIOLATION", VERBOSITY_INFO, "");\n' + "\t\tif (is_trap) implemented = true;\t/* M_TRAPONLY */\n")
elif mut == "M_NOVBR":          # the vector base dropped: every row but vbrtb runs with VBR == 0 (Opus pass 2: 10/10 escape)
    rep("\tcpu->pc = cpu->cd.m88k.cr[M88K_CR_VBR] + 8 * vector;\n", "\tcpu->pc = 8 * vector;\t/* M_NOVBR */\n")
elif mut == "M_SFRZTRAP":       # a trap while frozen is re-routed to ERROR like a fault (Opus pass 2: 10/10 escape)
    rep("\t\tif (!is_trap) {\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n", "\t\tif (true) {\t/* M_SFRZTRAP */\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n")
elif mut == "M_SFIPNOTGT":      # the delay-slot else-arm's SFIP stops reading delay_target (Opus pass 2: 10/10 escape)
    rep("\t\t\t\tcpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;\n\t\t\t}\n",
        "\t\t\t\tcpu->cd.m88k.cr[M88K_CR_SFIP] = (cpu->pc + 4) | M88K_NIP_V;\t/* M_SFIPNOTGT */\n\t\t\t}\n")
elif mut == "M_DSLOTSWAP":      # the else-arm's two assignments swapped (Opus pass 2: 10/10 escape)
    rep("\t\t\t\tcpu->cd.m88k.cr[M88K_CR_SNIP] = (cpu->pc + 4) | M88K_NIP_V;\n\t\t\t\tcpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;\n",
        "\t\t\t\tcpu->cd.m88k.cr[M88K_CR_SFIP] = (cpu->pc + 4) | M88K_NIP_V;\t/* M_DSLOTSWAP */\n\t\t\t\tcpu->cd.m88k.cr[M88K_CR_SNIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;\n")
elif mut == "M_CARRYCLR":       # the exception-path PSR write clears the carry bit (UM 6.6: 'carry bit unchanged')
    rep("\tm88k_stcr(cpu, cpu->cd.m88k.cr[M88K_CR_PSR]\n\t    | M88K_PSR_SFRZ\t",
        "\tm88k_stcr(cpu, (cpu->cd.m88k.cr[M88K_CR_PSR] & ~M88K_PSR_C)\t/* M_CARRYCLR */\n\t    | M88K_PSR_SFRZ\t")
elif mut == "M_DELIVERALL":     # the fallback disabled: residual vectors and SFU1 fall into the tail (D4-like) -- the negative-control rows must red
    rep("\tif (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {\n", "\tif (false && !implemented) {\t/* M_DELIVERALL */\n")
elif mut == "M_TAILLE":         # the tail switch's guard `<' -> `<=': user vector 128 enters the tail default and stops (codex, pass 2)
    rep("\tif (vector < M88K_EXCEPTION_USER_TRAPS_START) {\n", "\tif (vector <= M88K_EXCEPTION_USER_TRAPS_START) {\t/* M_TAILLE */\n")
elif mut == "M_NOIND":          # the exception-path PSR write no longer sets IND (grok/codex pass 3: unobservable while every row started with IND set)
    rep("\t    | M88K_PSR_IND\t/*  disable interrupts,               */\n", "\t    | 0\t/*  M_NOIND  */\n")
elif mut == "M_NOSTOP":         # the fallback keeps its diagnostic and DROPS the stop (codex pass 3: HALT was classified from the text alone)
    rep("\t\t\t(int)cpu->pc);\n\t\tfor (int j = 0; j < cpu->machine->ncpus; ++j)\n\t\t\tcpu->machine->cpus[j]->running = false;\n",
        "\t\t\t(int)cpu->pc);\n\t\tfor (int j = 0; j < cpu->machine->ncpus; ++j)\n\t\t\t(void) j;\t/* M_NOSTOP */\n")
elif mut == "M_OVFSUPONLY":     # OVERFLOW delivered only from supervisor mode (Opus pass 4: 23/23 sweep on v4)
    rep('"INTEGER_OVERFLOW", VERBOSITY_INFO, "");\n' + IMPL,
        '"INTEGER_OVERFLOW", VERBOSITY_INFO, "");\n' + "\t\timplemented = (cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_MODE) != 0;\t/* M_OVFSUPONLY */\n")
elif mut == "M_MISSUPONLY":     # MISALIGNED delivered only from supervisor mode (the same hole on the other class)
    rep('"MISALIGNED_ACCESS", VERBOSITY_INFO, "");\n' + IMPL,
        '"MISALIGNED_ACCESS", VERBOSITY_INFO, "");\n' + "\t\timplemented = (cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_MODE) != 0;\t/* M_MISSUPONLY */\n")
elif mut == "M_SFRZMIS":        # the SFRZ re-route only for MISALIGNED (Opus pass 4: 23/23 sweep -- `error' was that cell's only row)
    rep("\t\tif (!is_trap) {\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n",
        "\t\tif (!is_trap && vector == M88K_EXCEPTION_MISALIGNED_ACCESS) {\t/* M_SFRZMIS */\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n")
elif mut == "M_SFRZNOOVF":      # the SFRZ re-route for every non-trap class EXCEPT overflow
    rep("\t\tif (!is_trap) {\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n",
        "\t\tif (!is_trap && vector != M88K_EXCEPTION_INTEGER_OVERFLOW) {\t/* M_SFRZNOOVF */\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n")
elif mut == "M_NOSFD1":         # the exception-path PSR write no longer sets SFD1 (Opus pass 4: 1/23 -- 21 bad=psr + sfu1h STOP)
    rep("\t    | M88K_PSR_SFD1\t/*  disable the floating point unit,  */\n", "\t    | 0\t/*  M_NOSFD1  */\n")
elif mut == "M_SFRZNODIV0":     # the SFRZ re-route for every non-trap class EXCEPT divide-by-zero (killed only by errdiv0)
    rep("\t\tif (!is_trap) {\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n",
        "\t\tif (!is_trap && vector != M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE) {\t/* M_SFRZNODIV0 */\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n")
elif mut == "M_SFRZNOPRIV":     # ... EXCEPT privilege violation (killed only by errpriv)
    rep("\t\tif (!is_trap) {\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n",
        "\t\tif (!is_trap && vector != M88K_EXCEPTION_PRIVILEGE_VIOLATION) {\t/* M_SFRZNOPRIV */\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n")
elif mut == "M_SFRZNOUNIMPL":   # ... EXCEPT unimplemented opcode (killed only by errunimpl)
    rep("\t\tif (!is_trap) {\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n",
        "\t\tif (!is_trap && vector != M88K_EXCEPTION_UNIMPLEMENTED_OPCODE) {\t/* M_SFRZNOUNIMPL */\n\t\t\tvector = M88K_EXCEPTION_ERROR;\n")
elif mut == "M_LEVEL":           # INFO -> ERROR for the seven: expected to SURVIVE (disclosed)
    for c in CLASSES:
        rep('"%s", VERBOSITY_INFO, "");\n' % c, '"%s", VERBOSITY_ERROR, "");\n' % c)
else:
    raise SystemExit("unknown mutant " + mut)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("applied", mut)
