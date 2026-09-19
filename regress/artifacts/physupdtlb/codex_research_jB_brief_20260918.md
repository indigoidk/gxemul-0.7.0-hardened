# Research job B -- `physupdtlb`: does a PHYSICAL memory_rw that reaches RAM install a VA==PA translation?

    VERDICT: REAL | NOT REAL | UNSETTLED -- <one line naming the deciding fact>

Put the verdict line first.  The tree is `GXEMUL-SEC/` at HEAD `cdbe7d7`; ignore any other `src/` under the project
root.  **Read ONLY these files:**

    GXEMUL-SEC/src/cpus/memory_rw.c         the PHYSICAL branch (~245) and the RAM path (~720-790)
    GXEMUL-SEC/src/cpus/cpu_dyntrans.c      every update_translation_table implementation it generates
    GXEMUL-SEC/src/cpus/cpu_mips.c          how MIPS keys and invalidates its translation tables (for KUSEG)
    GXEMUL-SEC/src/devices/dev_sgi_mec.c    the 7 bare-PHYSICAL memory_rw calls
    GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c   its bare-PHYSICAL call
    GXEMUL-SEC/src/devices/dev_ram.c        its bare-PHYSICAL call

**The hypothesis.**  Under PHYSICAL, memory_rw sets `paddr = vaddr`.  On the RAM path it then calls
`cpu->update_translation_table(cpu, vaddr & ~offset_mask, memblock, ..., paddr & ~offset_mask)`, guarded by
`!dyntrans_device_danger`, `!(ok & MEMORY_NOT_FULL_PAGE)` and `!no_exceptions`, but NOT by PHYSICAL.  So a device's
PHYSICAL (and not NO_EXCEPTIONS) access to RAM installs a translation for the VIRTUAL page numerically equal to that
physical page -- possibly over whatever the guest maps at that VA.

**Answer, citing file:line:**
1. Is the guard reading right?  Is there any check (in memory_rw.c or inside each update_translation_table) that
   refuses or scopes such an entry -- e.g. a segment check, an ASID/tag, a "physical" flag in the entry?
2. For MIPS, does an installed entry for a KUSEG VA survive until a guest TLB write, or is it invalidated by
   something the guest routinely does?  Could a user-mode access at that VA then hit the device's page?
3. For each of the three devices: which machine uses it, which CPU, and does its PHYSICAL call reach RAM (vs a
   device) on a normal run?  Which is the most plausible witness, and what would the witness observe?
4. Your verdict on whether the defect is real, and its severity if so.
If you found anything else, say so briefly.
