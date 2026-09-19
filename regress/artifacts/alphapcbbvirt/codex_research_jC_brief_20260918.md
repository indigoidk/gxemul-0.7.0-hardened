# Research job C -- `alphapcbbvirt`: is the PCB base swpctx receives a PHYSICAL address, and how to witness it?

    VERDICT: PHYSICAL | VIRTUAL | UNSETTLED -- <one line naming the deciding fact>

Put the verdict line first.  The tree is `GXEMUL-SEC/` at HEAD `cdbe7d7`; ignore any other `src/` under the project
root.  **Read ONLY these files:**

    GXEMUL-SEC/src/cpus/cpu_alpha_palcode.c      swpctx (~229-300) and wrfen (~215-224)
    GXEMUL-SEC/src/core/memory.c                 load_64bit_word / store_64bit_word (~760-900)
    GXEMUL-SEC/src/include/thirdparty/alpha_cpu.h     alpha_pal_swpctx and any PCB comments
    GXEMUL-SEC/src/include/thirdparty/alpha_rpb.h     the HWRPB/PCS fields that name PCBs
    GXEMUL-SEC/src/machines/machine_alpha.c      how the emulator sets up the initial PCB/context

**The claim under test.**  swpctx and wrfen access the PCB through load_/store_64bit_word, which call memory_rw with
CACHE_DATA and NO PHYSICAL, so the PCB base (`ctx`) is translated as a VIRTUAL address.  Architecturally (OSF/1 PAL)
the PCBB is a PHYSICAL address.

**Answer, citing file:line:**
1. What in these files (a comment, a field name, the way the emulator itself sets up the first PCB) establishes whether
   `ctx`/a0 is physical or virtual?  The only in-tree anchor I know is alpha_rpb.h's `pcs_halt_pcbb /* phys addr of
   halt PCB */`.  Is there a stronger one?  Does machine_alpha.c pass the initial PCB as a physical or K0SEG address?
2. If the PCBB is physical: with paging armed (ptbr != 0, supervisor mode), what exactly happens on swpctx with a
   physical a0 that the current table does not map?  Trace the nine loads and the saves.
3. A rung-3 WITNESS SPEC on an unmodified `-E alpha -e alphabook1` cold debugger: the setup, the rows, the controls
   (liveness + a signature proving the loads went through the walk), and what distinguishes pre-fix from post-fix.
If you found anything else, say so briefly.
