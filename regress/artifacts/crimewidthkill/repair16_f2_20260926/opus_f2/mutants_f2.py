#!/usr/bin/env python3
"""mutants_f2.py NAME SRC DST -- the Opus measuring seat's legs for the repair-16 F2 pass.

Exact-string edits on the BASELINE dev_sgi_ip32.c 8c1d1545.  MUTANT-TEXT-NOT-FOUND is a hard FAIL.

  S_rst4clr    the 4-byte, latch-CLEAR mirror of table 16's S_rst8clr: an ACCEPTED 4-byte 0x800 write with the latch
               CLEAR no longer stops the CPUs.  The CHANNEL check for `ctlrst sw halt', the one repair-16 row table 16
               gave no mutant (its natural mutant also reds `sw08 halts', which is a CRIMEP_CONTROL row).
  M_ctldebug   the CONTROL arm's residue text demoted from fatal() to debug(): every CONTROL-text count row runs STEPPED,
               where debug() prints too.  The residue-text CHANNEL axis (the analogue of contract item 5 for the
               decline announce).
  H_rstclr4clr the HARD_RESET clear skipped only for a 4-byte write with the latch CLEAR -- one cell of the four the
               class closure claims (`ctlrst sw msg' should be its only red).
  E_endlatch   the ENDIANESS clear skipped only with the latch SET -- one latch-state half of the ENDIANESS closure
               (`rearm ctl msg' should be its only red).
"""
import io, sys

name = sys.argv[1]
if name == "list":
    print("base S_rst4clr M_ctldebug H_rstclr4clr E_endlatch")
    sys.exit(0)
src, dst = sys.argv[2], sys.argv[3]
s = io.open(src, encoding="latin-1", newline="").read()

HALT = ("\t\t\t\tfor (j=0; j<cpu->machine->ncpus; j++)\n"
        "\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n")
RST_CLEAR = "\t\t\t\tidata &= ~CRIME_CONTROL_HARD_RESET;\n"
END_CLEAR = "\t\t\tidata &= ~CRIME_CONTROL_ENDIANESS;\n"
CTL_PRINT = "\t\t\t\tfatal(\"[ CRIME_CONTROL: unimplemented \"\n"


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("MUTANT TEXT NOT FOUND (or not unique) for %s: %d occurrences" % (name, n))
    s = s.replace(old, new)


if name == "base":
    pass
elif name == "S_rst4clr":
    sub(HALT, "\t\t\t\tif (!(len == 4 && !(d->warned & CRIME_W_LEN)))\n" + HALT)
elif name == "M_ctldebug":
    sub(CTL_PRINT, "\t\t\t\tdebug(\"[ CRIME_CONTROL: unimplemented \"\n")
elif name == "H_rstclr4clr":
    sub(RST_CLEAR, "\t\t\t\tif (!(len == 4 && !(d->warned & CRIME_W_LEN)))\n\t" + RST_CLEAR)
elif name == "E_endlatch":
    sub(END_CLEAR, "\t\t\tif (!(d->warned & CRIME_W_LEN))\n\t" + END_CLEAR)
elif name == "T_halttwin":
    #  Q3 item 3 only (not a probe leg): a nonzero residue ALSO stops the CPU, so in `ctlrst' the 0x0001 twin halts and
    #  the 0x0800 store never runs -- the session's two rows cannot tell, AFTER's unrowed `print pc' can
    sub("\t\t\t\t    \"control 0x%016llx ]\\n\", (long long)idata);\n",
        "\t\t\t\t    \"control 0x%016llx ]\\n\", (long long)idata), cpu->running = 0;\n")
else:
    sys.exit("unknown mutant %s" % name)

io.open(dst, "w", encoding="latin-1", newline="").write(s)
print("APPLIED %s" % name)
