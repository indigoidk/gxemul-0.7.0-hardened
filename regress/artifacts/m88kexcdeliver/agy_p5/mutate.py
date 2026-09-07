import sys

F = "/tmp/gxagy502/src/cpus/cpu_m88k.c"

MUTANTS = {
    # 1. MANDATORY FIRST: fallback upper bound < 127
    "M_FALLBACK127": (
        "\tif (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {\n",
        "\tif (vector < 127 && !implemented) {\n"
    ),

    # 2. Fallback predicate: drop upper bound entirely (only !implemented)
    "M_FALLBACK_NO_BOUND": (
        "\tif (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {\n",
        "\tif (!implemented) {\n"
    ),

    # 3. Operand swap: PSR vs EPSR in SFRZ re-route predicate
    "M_SFRZ_EPSR_SWAP": (
        "\tif (cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_SFRZ) {\n",
        "\tif (cpu->cd.m88k.cr[M88K_CR_EPSR] & M88K_PSR_SFRZ) {\n"
    ),

    # 4. Tail switch: remove ERROR case label
    "M_TAIL_ERROR_DROP": (
        "\t\tcase M88K_EXCEPTION_INTEGER_OVERFLOW:\n\t\tcase M88K_EXCEPTION_ERROR:\n\t\t\t/*  m88kexcdeliver:",
        "\t\tcase M88K_EXCEPTION_INTEGER_OVERFLOW:\n\t\t\t/*  m88kexcdeliver:"
    ),

    # 5. Tail switch: remove BOUNDS case label
    "M_TAIL_BOUNDS_DROP": (
        "\t\tcase M88K_EXCEPTION_PRIVILEGE_VIOLATION:\n\t\tcase M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:\n\t\tcase M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:\n",
        "\t\tcase M88K_EXCEPTION_PRIVILEGE_VIOLATION:\n\t\tcase M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:\n"
    ),

    # 6. Joint cell: {SFRZ set, is_trap} on update_shadow_regs
    "M_SFRZ_TRAP_UPDATE": (
        "\t\tupdate_shadow_regs = false;\n\t} else {\n",
        "\t\tupdate_shadow_regs = is_trap;\n\t} else {\n"
    ),
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mutate.py <MUTANT_NAME>")
        sys.exit(1)
    
    name = sys.argv[1]
    if name not in MUTANTS:
        print("MUTATE_FAIL: unknown mutant %s" % name)
        sys.exit(2)
    
    find, repl = MUTANTS[name]
    with open(F, "r") as f:
        src = f.read()
    
    n = src.count(find)
    if n != 1:
        print("MUTATE_FAIL %s find-count=%d (want exactly 1)" % (name, n))
        sys.exit(3)
    
    new_src = src.replace(find, repl, 1)
    with open(F, "w") as f:
        f.write(new_src)
    
    print("MUTATE_OK %s" % name)
