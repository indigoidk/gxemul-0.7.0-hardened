#!/usr/bin/env python3
"""fix_misc_h.py -- stage src/include/misc.h with the four printf-format attributes made permanent (owner ruling 2026-11-05:
enforcement is a gate check; gate 1 already refuses any compiler warning).  GX_PRINTF expands to the GCC/clang attribute and to
nothing elsewhere, so the C99 build stays portable.  Exact anchors, each asserted once."""
import io
import os
import subprocess

REPO = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
ST = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix/stage/"
f = "src/include/misc.h"
assert subprocess.run(["git", "-C", REPO, "grep", "-q", "GX_PRINTF", "HEAD", "--", "src"]).returncode != 0, "GX_PRINTF exists"
t = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + f], capture_output=True).stdout.decode("latin-1")
E = [
    ("void debug_indentation(int diff);\n",
     "/*  #NNN: the diagnostic functions are printf-like; with GCC or clang a format\n"
     "    that does not match its arguments is a compiler warning, which gate 1\n"
     "    refuses.  Other compilers see nothing.  */\n"
     "#ifdef __GNUC__\n"
     "#define\tGX_PRINTF(f, a)\t__attribute__((format(printf, f, a)))\n"
     "#else\n"
     "#define\tGX_PRINTF(f, a)\n"
     "#endif\n"
     "void debug_indentation(int diff);\n"),
    ("void debug(const char *fmt, ...);\n", "void debug(const char *fmt, ...) GX_PRINTF(1, 2);\n"),
    ("void fatal(const char *fmt, ...);\n", "void fatal(const char *fmt, ...) GX_PRINTF(1, 2);\n"),
    ("void debugmsg(int subsystem, const char *name, int verbosity_required, const char *fmt, ...);\n",
     "void debugmsg(int subsystem, const char *name, int verbosity_required, const char *fmt, ...) GX_PRINTF(4, 5);\n"),
    ("void debugmsg_cpu(struct cpu* cpu, int subsystem, const char *name, int verbosity_required, const char *fmt, ...);\n",
     "void debugmsg_cpu(struct cpu* cpu, int subsystem, const char *name, int verbosity_required, const char *fmt, ...) "
     "GX_PRINTF(5, 6);\n"),
]
for old, new in E:
    assert t.count(old) == 1, (old, t.count(old))
    t = t.replace(old, new)
os.makedirs(os.path.dirname(ST + f), exist_ok=True)
io.open(ST + f, "w", encoding="latin-1", newline="").write(t)
print("staged misc.h: GX_PRINTF defined and applied to 4 declarations")
