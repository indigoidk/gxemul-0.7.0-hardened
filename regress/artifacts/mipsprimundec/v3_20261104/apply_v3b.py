#!/usr/bin/env python3
"""apply_v3b.py <v3 cpu_mips_instr.c> <dst> -- a measured ALTERNATIVE to the v3 for the adjudicator (main loop, 2026-11-04 05:1x; not a
ruling).  v3b = v3 plus the disputed D1 cell resolved the way two local manuals read: on ISA III, LWC3 (0x33) and SWC3 (0x3b) are
Reserved Instruction -- MIPS IV Instruction Set rev 3.2, A 8.6 Table A-39 leaves both cells empty and its note says the never-implemented
Coprocessor 3 instructions "were removed or changed to another use starting in MIPS III" (_scratchpad/mips-iv.txt:1366, :1388); the
R4000 User's Manual, Figure A-2, marks both `*`, "reserved instruction exceptions in all current implementations"
(_scratchpad/mips_r4000.txt:5823, :5834).  Through MIPS II both stay Coprocessor Unusable with CE = 3, as in v3.  The comments are
rewritten to be true as written: the v3 text "no COP3 is modelled" is false (machine_pmax.c:81 and :170 allocate coproc[3]).
Applied to apply_v3.py's output by exact-string edits; each anchor must occur exactly once."""
import io
import sys

src, dst = sys.argv[1], sys.argv[2]
t = io.open(src, encoding="utf-8", newline="").read()


def once(old, new):
    global t
    n = t.count(old)
    if n != 1:
        sys.exit("ANCHOR count %d (want 1): %r" % (n, old[:70]))
    t = t.replace(old, new)


once("\tcase HI6_SWC3:\n"
     "\t\t/*  #NNN: SWC3 is a coprocessor-3 store on ISA I-III (CpU, CE = 3)\n"
     "\t\t    and a reserved encoding from ISA IV on (Reserved Instruction);\n"
     "\t\t    neither stops the CPU.  */\n"
     "\t\tif (cpu->cd.mips.cpu_type.isa_level >= 4) {\n",
     "\tcase HI6_SWC3:\n"
     "\t\t/*  #NNN: through MIPS II, SWC3 is a coprocessor-3 store; no\n"
     "\t\t    coprocessor-3 load or store is implemented, so it raises\n"
     "\t\t    Coprocessor Unusable with CE = 3 whatever Status.CU3 holds.\n"
     "\t\t    MIPS III removed the coprocessor-3 loads and stores and later\n"
     "\t\t    levels keep the encoding reserved, so from ISA III on it is a\n"
     "\t\t    Reserved Instruction (MIPS IV Instruction Set rev 3.2, Table\n"
     "\t\t    A-39; R4000 User's Manual, Figure A-2).  Neither stops the\n"
     "\t\t    CPU.  */\n"
     "\t\tif (cpu->cd.mips.cpu_type.isa_level >= 3) {\n")

once("\t\t} else {\n"
     "\t\t\t/*  #NNN: LWC3 on ISA I-III is a coprocessor-3 load and no\n"
     "\t\t\t    COP3 is modelled: the architectural result is Coprocessor\n"
     "\t\t\t    Unusable with Cause.CE = 3 (the #236 idiom), not a stopped\n"
     "\t\t\t    CPU.  */\n"
     "\t\t\tic->f = instr(cpu);\n"
     "\t\t\tic->arg[0] = 3;\n"
     "\t\t}\n",
     "\t\t} else if (cpu->cd.mips.cpu_type.isa_level == 3) {\n"
     "\t\t\t/*  #NNN: MIPS III removed the coprocessor-3 loads; the\n"
     "\t\t\t    encoding is a Reserved Instruction there (MIPS IV\n"
     "\t\t\t    Instruction Set rev 3.2, Table A-39; R4000 User's\n"
     "\t\t\t    Manual, Figure A-2).  */\n"
     "\t\t\tic->f = instr(reserved);\n"
     "\t\t} else {\n"
     "\t\t\t/*  #NNN: through MIPS II, LWC3 is a coprocessor-3 load.  No\n"
     "\t\t\t    coprocessor-3 load or store is implemented, so it raises\n"
     "\t\t\t    Coprocessor Unusable with Cause.CE = 3 (the #236 idiom)\n"
     "\t\t\t    whatever Status.CU3 holds, instead of stopping the CPU.  */\n"
     "\t\t\tic->f = instr(cpu);\n"
     "\t\t\tic->arg[0] = 3;\n"
     "\t\t}\n")

io.open(dst, "w", encoding="utf-8", newline="").write(t)
print("APPLY_V3B_OK")
