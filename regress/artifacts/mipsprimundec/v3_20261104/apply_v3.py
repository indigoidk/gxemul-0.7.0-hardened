#!/usr/bin/env python3
"""apply_v3.py <src cpu_mips_instr.c> <dst> -- the mipsprimundec v3 (main loop, 2026-11-04 04:4x): the measured draft
(draft_20261104/draft.diff) plus ONLY the two changes grok 4.7's consolidation of the four share-findings reviews lists as consensus
(_scratchpad/v3_consol/grok_mipsprimundec_v3consol.txt, section 2): V3-1 split LDC2/SDC2 off the coprocessor-2 case with the LDC1/SDC1
ISA-II gate; V3-2 the non-R5900 half of 0x1e decodes as Reserved Instruction.  The draft's unrelated hunk (a deleted blank line after
`switch (s6) {`) is NOT carried.  Applied to HEAD's text by exact-string edits; each anchor must occur exactly once."""
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


NEW_CASES = (
    "\tcase HI6_LWC2:\n"
    "\tcase HI6_SWC2:\n"
    "\t\t/*  #NNN: coprocessor-2 word loads and stores.  No COP2 is\n"
    "\t\t    modelled on any emulated MIPS, so the architectural result is\n"
    "\t\t    Coprocessor Unusable (Cause.CE = 2), as X(cpu) already raises\n"
    "\t\t    for COP1 (#236).  Before this they fell to default: goto bad,\n"
    "\t\t    which stopped the emulated CPU from any privilege level.  */\n"
    "\t\tic->f = instr(cpu);\n"
    "\t\tic->arg[0] = 2;\n"
    "\t\tbreak;\n"
    "\n"
    "\tcase HI6_LDC2:\n"
    "\tcase HI6_SDC2:\n"
    "\t\t/*  #NNN: the doubleword forms are MIPS II; below that the\n"
    "\t\t    encoding is reserved, as LDC1/SDC1 already are (above).  */\n"
    "\t\tif (cpu->cd.mips.cpu_type.isa_level < 2) {\n"
    "\t\t\tic->f = instr(reserved);\n"
    "\t\t} else {\n"
    "\t\t\tic->f = instr(cpu);\n"
    "\t\t\tic->arg[0] = 2;\n"
    "\t\t}\n"
    "\t\tbreak;\n"
    "\n"
    "\tcase HI6_SWC3:\n"
    "\t\t/*  #NNN: SWC3 is a coprocessor-3 store on ISA I-III (CpU, CE = 3)\n"
    "\t\t    and a reserved encoding from ISA IV on (Reserved Instruction);\n"
    "\t\t    neither stops the CPU.  */\n"
    "\t\tif (cpu->cd.mips.cpu_type.isa_level >= 4) {\n"
    "\t\t\tic->f = instr(reserved);\n"
    "\t\t} else {\n"
    "\t\t\tic->f = instr(cpu);\n"
    "\t\t\tic->arg[0] = 3;\n"
    "\t\t}\n"
    "\t\tbreak;\n"
    "\n"
    "\tcase 0x1d:\n"
    "\t\t/*  #NNN: JALX exists only with MIPS16e, which this tree does not\n"
    "\t\t    model; the encoding is a Reserved Instruction here (#309's\n"
    "\t\t    REGIMM precedent), not a stopped CPU.  */\n"
    "\t\tic->f = instr(reserved);\n"
    "\t\tbreak;\n"
    "\n")

# 1. the new arms go immediately before LWC3, after the LWC1/SDC1 block's break (the draft's placement)
once("\t\t\tic->arg[0] = 1;\n\t\t}\n\t\tbreak;\n\n\tcase HI6_LWC3:\n",
     "\t\t\tic->arg[0] = 1;\n\t\t}\n\t\tbreak;\n\n" + NEW_CASES + "\tcase HI6_LWC3:\n")

# 2. LWC3 below ISA IV: Coprocessor Unusable CE = 3 (the draft's text, unchanged)
once("\t\t} else {\n"
     "\t\t\tif (!cpu->translation_readahead)\n"
     "\t\t\t\tfatal(\"TODO: lwc3 not implemented yet\\n\");\n"
     "\t\t\tgoto bad;\n"
     "\t\t}\n",
     "\t\t} else {\n"
     "\t\t\t/*  #NNN: LWC3 on ISA I-III is a coprocessor-3 load and no\n"
     "\t\t\t    COP3 is modelled: the architectural result is Coprocessor\n"
     "\t\t\t    Unusable with Cause.CE = 3 (the #236 idiom), not a stopped\n"
     "\t\t\t    CPU.  */\n"
     "\t\t\tic->f = instr(cpu);\n"
     "\t\t\tic->arg[0] = 3;\n"
     "\t\t}\n")

# 3. V3-2: the non-R5900 half of 0x1e (the R5900 half, with its goto bad, is unchanged)
once("\t\tif (!cpu->translation_readahead)\n"
     "\t\t\tfatal(\"TODO: MDMX\\n\");\n"
     "\n"
     "\t\tgoto bad;\n"
     "\t\t/*  break  */\n",
     "\t\t/*  #NNN: MDMX is not implemented, so the encoding decodes as a\n"
     "\t\t    Reserved Instruction (as on a CPU without the MDMX ASE)\n"
     "\t\t    instead of stopping the CPU.  */\n"
     "\t\tic->f = instr(reserved);\n"
     "\t\tbreak;\n")

io.open(dst, "w", encoding="utf-8", newline="").write(t)
print("APPLY_V3_OK")
