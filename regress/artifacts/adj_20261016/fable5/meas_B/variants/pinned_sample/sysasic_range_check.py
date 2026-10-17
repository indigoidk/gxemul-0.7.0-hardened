#!/usr/bin/env python3
"""asiceventaddr DETECTOR: the compile-time event-domain guard in
src/include/thirdparty/dreamcast_sysasicvar.h, measured by COMPILING against it -- and, on the
raise route, by RUNNING what compiles.

WHAT IT DEFENDS.  SYSASIC_EVENT_TO_ADDR(e) is correct only for e in [0,95] (#466).  #468 (e >= 96)
and #469 (e < 0) put SYSASIC_EVENT_RANGE_OK(e) inside it: a bit-field whose width is -1 for any e
outside [0,95], so an out-of-domain RAISE fails to COMPILE.  No in-tree raise is out of domain, so
a weakened GUARD leaves all four product objects byte-identical (the closure round's table: 41 of
the 43 header variants that compile, the other two moving an in-domain VALUE --
regress/artifacts/asiceventaddr/killtable_20261009/PRODEQ.tsv; this instrument's own table
re-measures it in regress/artifacts/asiceventaddr/table2_20261013/PRODEQ.tsv).  Byte-identical
objects mean no test of the BUILT product can tell such a header from the committed one; a
compiler run against the header can, and that is what this is.

THE ROWS (17).  Fifteen are case blocks in sysasic_range_cases.c, one translation unit each
(-DSYSASIC_CASE=<n>); SWEEP and CENSUS are built here.  PROD runs 16 of them (17 with --census;
C89 counts here, with its own flags), POL the 13 that only compile.
  A0 A95          accepted, and the VALUE anchored inside the TU (0x5f6900, 0x5f6908)
  X96 X97 X128    refused through ADDR.  X96 defines its own SYSASIC_EVENT_FOO 96 (the header's
  Xm1 X2p32       example); X97 is the only fixed row that sees a gap opened further out; Xm1
                  (with XTm1) carries #469; X2p32 is one named row for five measured weakenings
                  -- an operand mask, an unsigned compare, a narrowing cast, a far disjunct, an
                  operand modulo.  2**32 is the FIRST value only the compare and the cast admit;
                  `& 0xff' first admits 256 and `> 128' and `% 129' first admit 129, which SWEEP
                  and TSWEEP also see
  RT              a RUNTIME e is refused (the width must be an integer constant), compiled three
                  times: e an int, a long long and an unsigned long long
  XT96 XTm1 RTT   the same refusals through SYSASIC_TRIGGER_EVENT, the only road the product
                  uses (RTT typed as RT).  A TRIGGER that stops calling ADDR keeps every ADDR row
                  green; these rows, TSWEEP and CENSUS see it
  ID              the 21 real events through TRIGGER, compiled, linked and RUN: each address and
                  the FULL 64-bit payload checked against 0x5f6900 + 4*(e div 32) and
                  (1 << (e mod 32)) | 2**32, computed HERE from the event NUMBER the program
                  prints for each define, plus every argument pin below
  C89             the header's own sentence: ADDR over the 21 events plus 0 and 95 is clean under
                  -std=c89 -pedantic-errors -Wall -Wextra -Werror
  SWEEP           one TU, one top-level ADDR invocation per line for every e in [-1024, 8192)
                  plus 54 wide, odd-typed and typed-edge samples: 9270 lines.  In-domain lines are
                  VALUE-asserting typedefs, out-of-domain lines bare uses.  Green iff the set of
                  erroring lines is EXACTLY the out-of-domain lines, every error on them is a
                  constant bit-field-width class, and nothing else errors.  Compiled with
                  -ftrack-macro-expansion=0 so gcc reports each error at the line that invoked
                  the macro; one top-level macro invocation per line makes the attribution by
                  construction.  On the committed header 9152 of the 9270 lines error, both legs;
                  gate 2 pins both numbers by equality.
  TSWEEP          SWEEP's refusal-set equality through SYSASIC_TRIGGER_EVENT: one raise per line
                  over the same 9270 values, compiled -fsyntax-only (measured, nine media on both
                  legs: the same error set as -c at a fraction of the time -- t9_syntaxonly in the
                  table's directory).  A transform of e on the raise route alone
                  (`ADDR((e) % 128)', `(e) == 100 ? 0 : (e)') keeps every ADDR row green and is
                  visible here.  9152 of the 9270 lines error on the committed header, both legs.
  TVAL            every e in [0,95] raised through TRIGGER as an int, plus the in-domain edges 0
                  and 95 raised in each of the eight sizeof/sign classes (signed and unsigned
                  char, short, int and long long), compiled, linked and RUN: the address and the
                  device-visible payload (the low 32 bits and bit 32: the device tests bit 32 and
                  folds the word into uint32_t pending_irq[]) checked against the same references,
                  plus every argument pin below
  CENSUS          (--census TREE only) preprocess the four product TUs that include the header --
                  dev_dreamcast_asic, _gdrom, _maple, dev_pvr -- at the tree's own flags and
                  count, per TU, 0x5f6900 literals and guard SHAPES (a sizeof of a struct holding
                  one int bit-field), keyed on neither macro name.  Pinned by equality: asic 1 and
                  0, gdrom 4 and 4, maple 1 and 1, pvr 10 and 10.  AGGREGATE counts of two
                  correlates of a guarded raise -- not operand identity, not routing (DISCLOSES)

THE ARGUMENT PINS, ID and TVAL, every raise.  The stub is an ORACLE here, so it is built not to
hide a wrong argument.  MEM_WRITE and PHYSICAL are memory.h's values, not the stub's choice: the
run is VOID unless src/include/memory.h (--memory-h) carries `#define MEM_WRITE 1' and `#define
PHYSICAL 32' each as ONE WHOLE LINE, with no other definition of either name, and the flags
TRIGGER passes must be 32.  The cpu and the memory handle are DISTINCT objects, and the pointers
TRIGGER must pass are retained apart from the struct it reads.  Per raise: memory_rw called ONCE
in all, whatever the writeflag, and that call the write; its cpu, its handle and its buffer the
expected ones (the buffer the serializer filled); flags PHYSICAL; length 8; memory_writemax64
called once, with the expected cpu (the product's dereferences it on its first line) and length
8.  (The pass-2 prototype defined PHYSICAL as 2 -- memory.h's CACHE_NONE -- aliased the handle to
the cpu, counted writes rather than calls and never looked at the serializer's arguments; table 2
measures what that let through.)

THE ORACLE, and why not the exit status alone.  A REFUSAL row is green only when the compiler
exits nonzero AND prints exactly ONE `error:' line AND that line is a bit-field-width class (X
rows: negative width | zero width | width exceeds its type; RT rows: width not an integer constant)
AND a `note: in expansion of macro SYSASIC_EVENT_RANGE_OK' follows it.  The exit status alone is
green on a comment-only header (every refusal row refuses, for the wrong reason), and it already
false-passed on this very row once: #468's own harness redefined SYSASIC_BASE and every leg died of
`redefined'.  The class carries no field name, so the pre-#469 header (field sysasic_event_lt_96)
is red only where it is really wrong.  The note names the MACRO the error came from, and that is
all it does: it cannot tell the two routes apart -- a guard added to BITMASK while TRIGGER
bypasses ADDR gives the same note, and that header still refuses every out-of-domain raise (green,
correctly).  An ACCEPT row is green on exit status 0 and zero `error:' lines.

LEGS.  PROD (the floor; every row): the configured tree's CWARNINGS + COPTIM, from --prod-flags,
else the MIRROR below -- -O3 -DNDEBUG and no -std, so a guard wrapped in #ifndef NDEBUG, #ifndef
__OPTIMIZE__ or a dialect test is compiled the way the product compiles it.  POL (portability; the
13 compile-only rows, no run rows): -std=c99 -pedantic-errors -Wall -Wextra -O0.  It proves no
refusal RELIES on -O3 folding, and it is a leg of its own, not a subset of PROD: a width built on
`__builtin_constant_p' is folded at -O0 and deferred at -O3, so such a guard can admit a runtime e
on POL alone (an int, or only an 8-byte one); and TRIGGER evaluating e once into an int local is
caught on both legs, by TSWEEP on PROD (the 64-bit samples truncate) and by XT96/XTm1 on POL (-O0
does not fold the local).  C89: one row, the header's own flags.  --cc takes the WHOLE compiler
command (`cc', `gcc -m32'), shell-split, and every compiler operation uses all of it: the identity
line, the gcc check, every row and the census.

TOKENS.  One line per row, `  <status>  <leg>  <row>  <detail>', the status (ok or FAIL) and the
leg (PROD, POL, C89) each padded to four columns and the row to six -- so match the gaps with
` +', never a literal run of spaces (`ok' is followed by four, `FAIL' by two).  Then
`PROD rows run: N' (17 with --census, 16 without; C89 counts here), `POL rows run: 13',
`rows red: N', `<n> rows, <m> failures', and SYSASIC_RANGE_PASS / SYSASIC_RANGE_FAIL /
SYSASIC_RANGE_VOID.  VOID = the instrument cannot give a verdict: the compiler is not gcc (the
oracle strings are gcc's), the header, the cases file or memory.h is missing, memory.h does not
carry `#define MEM_WRITE 1' and `#define PHYSICAL 32' as one whole line each and no other
definition of either, the cases file does not match the row table, or a sweep's errors cannot be
attributed to its lines.  Exit 0 only on PASS.

THE CONTRACT -- what this detector is designed to catch, and what it discloses.  Measured in
regress/artifacts/asiceventaddr/table2_20261013/ (SCORES.txt, the per-medium logs, PRODEQ.tsv).
  CATCHES: an edit to either bound at its edges and every single-value exemption in
  [-1024, 8192), through ADDR (SWEEP) and through TRIGGER (TSWEEP); the same at the 54 samples,
  among them the eight sizeof/sign classes a guard can key on (1, 2, 4 and 8 bytes, signed and
  unsigned, on LP64) at the four edges -1, 0, 95 and 96 -- and, at the in-domain edges 0 and 95,
  the VALUE of a typed raise in each class (TVAL) and of a typed ADDR (SWEEP's typedefs); the
  width mechanism (a non-constant width, for a runtime int, long long and unsigned long long;
  zero width and exceeds-its-type are accepted as EQUIVALENT refusals); the `* 0' contribution at
  every e in [0,95]; the guard's presence in ADDR; a TRIGGER that bypasses ADDR or folds its
  operand; a one-event address or payload offset anywhere in [0,95] on the raise route; the
  handle, flags, writeflag, length, buffer and cpu arguments on the raise route (TVAL, ID), with
  the stub's constants taken from memory.h; a guard wrapped in #ifndef NDEBUG, #ifndef
  __OPTIMIZE__ or a dialect test (PROD leg); the C89 claim; the per-TU counts of 0x5f6900
  literals and guard shapes in the four product TUs.
  DISCLOSES:
  * The partition the guard induces on e -- {e < 0} {0} {1..94} {95} {96} {e > 96} and a
    non-constant e -- is EXHAUSTED: every cell is rowed.  The NUMERIC range [-1024, 8192) is SWEPT
    value by value; outside it the 54 samples stand for everything, so a fold or exemption whose
    first wrong value lies beyond the sweep and off the samples (`% 10000', `== 8192',
    `== 12345') passes.
  * TYPE is exhausted only as the eight sizeof/sign classes AT THE FOUR EDGES, on this LP64 host:
    refusal and acceptance through both routes, and the in-domain edges' values through both.
    That set closes the type class, which two consecutive passes breached (pass 2: an 8-byte -1;
    the F2 pass: the 1-byte rank).  `_Bool' is not sampled (it holds 0 and 1 only; no
    out-of-domain weakening keys on it).  Value x type AWAY from the edges is not checked on the
    raise route (`tmp1 + 4*(sizeof(e) == 8 && (e) == 42)' passes) and is sampled through ADDR
    (`(e) == 97 && sizeof(e) > 4' passes); types wider than 64 bits are not sampled (a (long
    long) cast in the guard admits (__int128)1 << 64, which the committed header refuses).
  * RUNTIME e: RT and RTT use int, long long and unsigned long long; other runtime types are not
    sampled.  A non-constancy exemption spelled `!__builtin_constant_p(e) ||' is still refused on
    both legs -- PROD by the hard error, POL only through -pedantic-errors -- and only a -O0 build
    without -pedantic-errors, which neither leg is, would accept it.
  * HOST: verdicts are for this host's gcc 15.2.1 on LP64.  A guard wrapped in
    `#if __GNUC__ >= 15' passes here (it reds under a simulated gcc 14); `(long)(e)' and
    `(unsigned long)(e) < 96ul' are EQUIVALENT on LP64 and weakenings under -m32; a non-gcc
    compiler makes the run VOID; C++ refuses the idiom.
  * EQUIVALENT BY DESIGN, green: + to -, `? 1 : 0', a field rename, De Morgan, `__builtin_expect'
    around the condition, a `__typeof__' cast, RANGE_OK delegating to a second macro, and a
    literal 32 or 1 in place of PHYSICAL or MEM_WRITE (memory.h's own values).  An exceeding width
    spelled `95 - (e)' is green on PROD and reds POL's sweeps: it overflows at the INT_MIN and
    LLONG_MIN samples, and -pedantic-errors makes that an error.
  * RED BY DESIGN, though not a weakening: a rename of SYSASIC_EVENT_RANGE_OK, or a guard
    refactored away from the bit-field idiom, reds the named refusal rows for TEXT and must be
    re-pinned; a second guard on BITMASK reds the TRIGGER rows (two errors per raise) and CENSUS
    (two shapes).
  * The 21 define VALUES are pinned by no row.  ID derives its reference from the event NUMBER
    printed from each define; TVAL never reads a define; neither pins the name-to-value mapping,
    so a define that moved is green as long as its raise is right for the new number.
  * PAYLOAD: TVAL checks the device-visible projection (the low 32 bits, bit 32) at every e; bits
    33..63 are checked only by ID, at its 21 events, and the device never sees them.  At 31, 63
    and 95 `1 << 31' sign-extends and sets bit 32 before the hack bit is OR-ed in, so dropping the
    hack bit there passes TVAL (with `1u <<' it does not); `1u <<' itself, the filed
    sysasicbitmask31 remedy, is EQUIVALENT on the device path.
  * BITMASK's value is pinned only through TRIGGER (TVAL, ID): no product TU calls BITMASK or ADDR
    directly, so corrupting BITMASK while TRIGGER inlines the original is product-equivalent.
  * CENSUS proves per-TU AGGREGATE counts of two correlates, not operand identity and not routing:
    a raise REPLACED by an open-coded write plus a dummy one-bit bit-field keeps both counts, and an
    open-coded write ADDED beside the guarded raises and spelled 6252800 or 0x5F6900 changes
    neither.  CENSUS is outside every in-gate control (they run without --census); the table
    measures it.  The population it reads is gate 2's LEXICAL count of files that spell the include
    (four): an in-tree wrapper header can take an includer out of that count while a fifth TU
    reaches the header, and a macro-generated or out-of-tree include is not counted.
  * Guest MMIO into the window, and the device switch's bands, belong to the callee and are
    outside the claim.
"""
import argparse
import hashlib
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(HERE, "sysasic_range_cases.c")
HEADER = os.path.normpath(os.path.join(HERE, "..", "src", "include", "thirdparty",
                                       "dreamcast_sysasicvar.h"))
MEMORY_H = os.path.normpath(os.path.join(HERE, "..", "src", "include", "memory.h"))

#  THE PRODUCT'S FLAGS, MIRRORED from a configured tree's src/devices/Makefile (CWARNINGS then
#  COPTIM; configure adds -DNDEBUG at `CFLAGS="-DNDEBUG $CFLAGS"' and picks -O3 in its non-DEBUG
#  -O probe).  Gate 2 compares this string with the configured tree's whenever one exists, so a
#  drift is a red row, not a silent mismatch.
PROD_MIRROR = ("-Wshadow -Wcast-align -Wstrict-aliasing -Wall -Wextra -Wno-unused-parameter "
               "-Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline "
               "-O3 -DNDEBUG")
POL_FLAGS = "-std=c99 -pedantic-errors -Wall -Wextra -O0"
C89_FLAGS = "-std=c89 -pedantic-errors -Wall -Wextra -Werror"
#  presentation only: no source excerpts, no colour.  The locale is pinned to C as well, and
#  the oracle still matches gcc's quote characters as ANY character -- in a UTF-8 locale gcc
#  prints U+2018/U+2019, and an ASCII-quote pattern once selected nothing.
DIAG = ["-fno-diagnostics-show-caret", "-fdiagnostics-color=never"]
SWEEP_EXTRA = ["-ftrack-macro-expansion=0", "-fmax-errors=0"]

#  (row, case number, kind).  The cases file must carry exactly these.
NAMED = [("A0", 1, "accept"), ("A95", 2, "accept"),
         ("X96", 3, "refuse"), ("X97", 4, "refuse"), ("X128", 5, "refuse"),
         ("Xm1", 6, "refuse"), ("X2p32", 7, "refuse"), ("RT", 8, "runtime"),
         ("XT96", 9, "refuse"), ("XTm1", 10, "refuse"), ("RTT", 11, "runtime"),
         ("ID", 12, "id"), ("C89", 13, "c89"), ("TSWEEP", 14, "tsweep"), ("TVAL", 15, "tval")]
COMPILE_ONLY = [r for r in NAMED if r[2] in ("accept", "refuse", "runtime")]
ID_EVENTS = 21
#  RT and RTT compile once per type: a constancy test keyed on the 8-byte rank -- the width
#  `__builtin_constant_p(e) ? <the guard> : (sizeof(e) == 8 ? 1 : (e))' -- refuses a runtime int and
#  ACCEPTS a runtime 8-byte e at -O0 (measured on the F2 pass), which an int-only row cannot see.
RT_TYPES = ["int", "long long", "unsigned long long"]
#  The values TRIGGER's MEM_WRITE and PHYSICAL must carry -- memory.h's, checked in memory.h.
PRODUCT_DEFINES = (("MEM_WRITE", 1), ("PHYSICAL", 32))
PHYSICAL_VAL = dict(PRODUCT_DEFINES)["PHYSICAL"]
MEM_WRITE_VAL = dict(PRODUCT_DEFINES)["MEM_WRITE"]

ERRLINE = re.compile(r": (?:fatal )?error: ")
DIAGLINE = re.compile(r": (?:fatal )?(?:error|warning): ")
CONST_W = re.compile(r"negative width in bit-field|zero width for bit-field"
                     r"|width of .* exceeds its type")
NONCONST_W = re.compile(r"width not an integer constant")
NOTE_GUARD = re.compile(r"note: in expansion of macro .SYSASIC_EVENT_RANGE_OK.")
CASE_LINE = re.compile(r"^#if SYSASIC_CASE == (\d+)\s+/\*\s*(\w+)\s*\*/\s*$")
REC = (r"addr=0x(?P<addr>[0-9a-f]+) pay=0x(?P<pay>[0-9a-f]+) calls=(?P<calls>\d+)"
       r" writes=(?P<writes>\d+) cpu=(?P<cpu>\w+) mem=(?P<mem>\w+) buf=(?P<buf>\w+)"
       r" flags=(?P<flags>-?\d+) wflag=(?P<wflag>-?\d+) len=(?P<len>-?\d+) ser=(?P<ser>\d+) scpu=(?P<scpu>\w+)"
       r" slen=(?P<slen>-?\d+)$")
ID_LINE = re.compile(r"^ID (?P<name>\w+) e=(?P<e>-?\d+) " + REC)
TV_LINE = re.compile(r"^TV e=(?P<e>-?\d+) " + REC)
TT_LINE = re.compile(r"^TT (?P<tag>\w+) e=(?P<e>-?\d+) " + REC)
#  TVAL's typed raises: the two in-domain edges in each of the eight sizeof/sign classes.
TT_WANT = sorted((t, v) for t in ("s8", "u8", "s16", "u16", "s32", "u32", "s64", "u64") for v in (0, 95))
SWEEP_ERR = re.compile(r"^(.*?):(\d+):(\d+): (?:fatal )?error: (.*)$")

SWEEP_LO, SWEEP_HI = -1024, 8192
SWEEP_SAMPLES = [("2147483647", 2147483647), ("(-2147483647-1)", -2147483648),
                 ("0x100000000LL", 2 ** 32), ("0x100000060LL", 2 ** 32 + 96),
                 ("(-0x100000000LL)", -(2 ** 32)), ("96u", 96), ("4294967295u", 4294967295),
                 ("0xffffffffffffffffULL", 2 ** 64 - 1), ("9223372036854775807LL", 2 ** 63 - 1),
                 ("(-9223372036854775807LL-1)", -(2 ** 63)), ("((unsigned char)200)", 200),
                 ("((signed char)-1)", -1), ("'A'", 65), ("'a'", 97), ("0x5f", 95),
                 ("(char)95", 95),
                 #  TYPED EDGES (pass 2): -1, 0, 95, 96 in each integer type -- a size- or sign-keyed
                 #  exemption at an edge (`sizeof(e) == 8 && (e) < 0 && (e) >= -1') escapes every int row.
                 ("((long long)-1)", -1),
                 ("((long long)0)", 0),
                 ("((long long)95)", 95),
                 ("((long long)96)", 96),
                 ("((unsigned long long)-1)", 18446744073709551615),
                 ("((unsigned long long)0)", 0),
                 ("((unsigned long long)95)", 95),
                 ("((unsigned long long)96)", 96),
                 ("((long)-1)", -1),
                 ("((long)0)", 0),
                 ("((long)95)", 95),
                 ("((long)96)", 96),
                 ("((unsigned long)-1)", 18446744073709551615),
                 ("((unsigned long)0)", 0),
                 ("((unsigned long)95)", 95),
                 ("((unsigned long)96)", 96),
                 ("((unsigned int)-1)", 4294967295),
                 ("((unsigned int)0)", 0),
                 ("((unsigned int)95)", 95),
                 ("((unsigned int)96)", 96),
                 ("((short)-1)", -1),
                 ("((short)0)", 0),
                 ("((short)95)", 95),
                 ("((short)96)", 96),
                 ("((unsigned short)-1)", 65535),
                 ("((unsigned short)0)", 0),
                 ("((unsigned short)95)", 95),
                 ("((unsigned short)96)", 96),
                 #  THE 1-BYTE RANK (the F2 pass): -1, 0, 95, 96 in char, signed char and unsigned char,
                 #  less the two above ((signed char)-1 and (char)95).  `|| (sizeof(e) == 1 && (e) == 96)'
                 #  passed every row before these.  (char)-1 is -1 on this host, where char is signed, and
                 #  255 where it is not -- out of domain either way.
                 ("((char)-1)", -1),
                 ("((char)0)", 0),
                 ("((char)96)", 96),
                 ("((signed char)0)", 0),
                 ("((signed char)95)", 95),
                 ("((signed char)96)", 96),
                 ("((unsigned char)-1)", 255),
                 ("((unsigned char)0)", 0),
                 ("((unsigned char)95)", 95),
                 ("((unsigned char)96)", 96),
                 #  ARGUMENT SHAPE: an out-of-domain value spelled as a low-precedence expression.  `(e)'
                 #  -> `e' at either RANGE_OK site accepts it (measured: s11_latent) while the committed
                 #  header refuses it; ?: binds looser than && and <.
                 ("1 ? 200 : 5", 200)]

TUS = ["dev_dreamcast_asic", "dev_dreamcast_gdrom", "dev_dreamcast_maple", "dev_pvr"]
#  (0x5f6900 literals, guard shapes) per TU.  asic's one literal is the device REGISTRATION and
#  it raises nothing; gdrom's comment claims "FOUR of them, compiled on every build".
CENSUS_PIN = {"dev_dreamcast_asic": (1, 0), "dev_dreamcast_gdrom": (4, 4),
              "dev_dreamcast_maple": (1, 1), "dev_pvr": (10, 10)}
BASE_LIT = re.compile(r"(?<![0-9A-Za-z_])0x5f6900(?![0-9A-Za-z_])")
SHAPE = re.compile(r"sizeof\s*\(\s*struct\s*\{\s*int\s+[A-Za-z_]\w*\s*:")


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def md5(path):
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def run(args, cwd, timeout=300):
    env = dict(os.environ, LC_ALL="C", LANG="C")
    try:
        p = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMED OUT after %d s" % timeout
    except OSError as exc:
        return 127, "", "could not run %s: %s" % (args[0], exc)
    return (p.returncode, p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


def first_errors(text, n=2):
    errs = [ln.strip() for ln in text.splitlines() if ERRLINE.search(ln)]
    return " | ".join(errs[:n]) if errs else "(no error line)"


def refusal(rc, diag, cls):
    lines = diag.splitlines()
    errs = [i for i, ln in enumerate(lines) if ERRLINE.search(ln)]
    if rc == 0:
        return False, "COMPILED (rc 0): the value was ACCEPTED"
    if len(errs) != 1:
        return False, "%d error lines, want exactly one: %s" % (len(errs), first_errors(diag))
    i = errs[0]
    msg = lines[i].split("error: ", 1)[-1].strip()
    if not cls.search(lines[i]):
        return False, "refused for the WRONG reason: " + msg
    j, noted = i + 1, False
    while j < len(lines) and not DIAGLINE.search(lines[j]):
        noted = noted or bool(NOTE_GUARD.search(lines[j]))
        j += 1
    if not noted:
        return False, "refused, but NOT inside SYSASIC_EVENT_RANGE_OK's expansion: " + msg
    return True, "refused: " + msg + " [in SYSASIC_EVENT_RANGE_OK]"


def accept(rc, diag, what):
    nerr = sum(1 for ln in diag.splitlines() if ERRLINE.search(ln))
    if rc != 0 or nerr:
        return False, "REFUSED: rc %d, %d error lines: %s" % (rc, nerr, first_errors(diag))
    return True, what


def product_defines(path):
    """memory.h must carry each pinned define as ONE WHOLE LINE, `#define <NAME> <value>' and
    nothing else on it, and no other definition of that name anywhere -- so neither a
    commented-out copy, nor a second definition below the first, nor a suffixed or annotated
    value can satisfy it."""
    if not os.path.isfile(path):
        return False, "memory.h missing: %s" % path
    text = read(path)
    bad, seen = [], []
    for name, want in PRODUCT_DEFINES:
        whole = re.findall(r"^#define[ \t]+%s[ \t]+%d$" % (name, want), text, re.M)
        anydef = re.findall(r"^[ \t]*#[ \t]*define[ \t]+%s\b(.*)$" % name, text, re.M)
        seen.append("%s %d" % (name, want))
        if len(whole) != 1 or len(anydef) != 1:
            bad.append("%s: %d whole-line `#define %s %d', %d definitions in all; want one of each"
                       % (name, len(whole), name, want, len(anydef)))
    return not bad, ("; ".join(bad) if bad else ", ".join(seen) + " (one whole line each)")


def arg_faults(m):
    """the argument pins every recorded raise must meet (THE ARGUMENT PINS in the docstring)"""
    bad = []
    if int(m.group("calls")) != 1:
        bad.append("memory_rw calls=%s" % m.group("calls"))
    if int(m.group("writes")) != 1:
        bad.append("writes=%s" % m.group("writes"))
    for k in ("cpu", "mem", "buf", "scpu"):
        if m.group(k) != "ok":
            bad.append("%s=%s" % (k, m.group(k)))
    if int(m.group("flags")) != PHYSICAL_VAL:
        bad.append("flags=%s (PHYSICAL is %d)" % (m.group("flags"), PHYSICAL_VAL))
    if int(m.group("wflag")) != MEM_WRITE_VAL:
        bad.append("wflag=%s (MEM_WRITE is %d)" % (m.group("wflag"), MEM_WRITE_VAL))
    if int(m.group("len")) != 8:
        bad.append("len=%s" % m.group("len"))
    if int(m.group("ser")) != 1:
        bad.append("serializer calls=%s" % m.group("ser"))
    if int(m.group("slen")) != 8:
        bad.append("serializer len=%s" % m.group("slen"))
    return bad


def id_verdict(rc, diag, run_rc, out):
    if rc != 0:
        return False, "did not compile and link: rc %d: %s" % (rc, first_errors(diag))
    got, bad = [], []
    for ln in out.splitlines():
        m = ID_LINE.match(ln)
        if not m:
            continue
        name, e = m.group("name"), int(m.group("e"))
        a, p = int(m.group("addr"), 16), int(m.group("pay"), 16)
        got.append(name)
        ra = 0x5f6900 + 4 * (e // 32) if 0 <= e <= 95 else None
        rp = (1 << (e % 32)) | (1 << 32) if 0 <= e <= 95 else None
        faults = arg_faults(m)
        if ra is None or a != ra or p != rp or faults:
            bad.append("%s e=%d addr=0x%x want %s pay=0x%x want %s%s" % (
                name, e, a, "0x%x" % ra if ra is not None else "none", p,
                "0x%x" % rp if rp is not None else "none",
                (" " + " ".join(faults)) if faults else ""))
    done = "ID_DONE" in out.splitlines()
    if run_rc != 0 or not done:
        return False, "the program did not finish: exit %d, ID_DONE %s" % (
            run_rc, "present" if done else "ABSENT")
    if len(got) != ID_EVENTS or len(set(got)) != ID_EVENTS:
        return False, "%d event lines (%d distinct), want %d" % (len(got), len(set(got)), ID_EVENTS)
    if bad:
        return False, "%d of %d events WRONG: %s" % (len(bad), ID_EVENTS, "; ".join(bad[:3]))
    return True, ("%d of %d events: address and full payload exact; every argument pin held"
                  % (ID_EVENTS, ID_EVENTS))


def tval_verdict(rc, diag, run_rc, out):
    if rc != 0:
        return False, "did not compile and link: rc %d: %s" % (rc, first_errors(diag))
    seen, typed, bad = {}, {}, []
    for ln in out.splitlines():
        m = TV_LINE.match(ln)
        tag = None
        if not m:
            m = TT_LINE.match(ln)
            if not m:
                continue
            tag = m.group("tag")
        e, a, p = int(m.group("e")), int(m.group("addr"), 16), int(m.group("pay"), 16)
        if tag is None:
            seen[e] = seen.get(e, 0) + 1
        else:
            typed[(tag, e)] = typed.get((tag, e), 0) + 1
        ra = 0x5f6900 + 4 * (e // 32) if 0 <= e <= 95 else None
        rlo = (1 << (e % 32)) & 0xffffffff if 0 <= e <= 95 else None
        faults = arg_faults(m)
        if ra is None or a != ra or (p & 0xffffffff) != rlo or not (p >> 32) & 1 or faults:
            bad.append("%se=%d addr=0x%x pay=0x%x%s" % ("" if tag is None else "(%s) " % tag, e, a, p,
                                                     (" " + " ".join(faults)) if faults else ""))
    if run_rc != 0 or "TVAL_DONE" not in out.splitlines():
        return False, "the program did not finish: exit %d" % run_rc
    if sorted(seen) != list(range(96)) or any(v != 1 for v in seen.values()):
        return False, "%d distinct values raised, want each of 0..95 exactly once" % len(seen)
    if sorted(typed) != TT_WANT or any(v != 1 for v in typed.values()):
        return False, "%d typed raises, want 0 and 95 once in each of the eight classes" % sum(typed.values())
    if bad:
        return False, "%d of 112 raises WRONG: %s" % (len(bad), "; ".join(bad[:3]))
    return True, ("96 of 96 int raises and 16 of 16 typed edge raises: address and device-visible "
                  "payload exact; every argument pin held")


def sweep_source():
    lines = ['#include "thirdparty/dreamcast_sysasicvar.h"',
             "/*  generated by sysasic_range_check.py: one ADDR use per line  */"]
    mp = {}
    vals = [("%d" % e if e >= 0 else "(%d)" % e, e) for e in range(SWEEP_LO, SWEEP_HI)]
    vals += SWEEP_SAMPLES
    k = 0
    for txt, v in vals:
        if 0 <= v <= 95:
            lines.append("typedef char sysasic_sweep_v%d[(SYSASIC_EVENT_TO_ADDR(%s)) == 0x%x ? 1 : -1];"
                         % (k, txt, 0x5f6900 + 4 * (v // 32)))
            mp[len(lines)] = (txt, v, "accept")
            k += 1
    lines += ["unsigned long sysasic_sweep_sink;", "void sysasic_sweep(void);",
              "void sysasic_sweep(void)", "{"]
    for txt, v in vals:
        if not 0 <= v <= 95:
            lines.append("\tsysasic_sweep_sink += SYSASIC_EVENT_TO_ADDR(%s);" % txt)
            mp[len(lines)] = (txt, v, "refuse")
    lines += ["}", ""]
    return "\n".join(lines), mp


def tsweep_source():
    lines = ["#define\tSYSASIC_CASE\t14", '#include "sysasic_range_cases.c"',
             "void sysasic_tsweep(struct cpu *cpu);", "void sysasic_tsweep(struct cpu *cpu)", "{"]
    mp = {}
    vals = [("%d" % e if e >= 0 else "(%d)" % e, e) for e in range(SWEEP_LO, SWEEP_HI)] + SWEEP_SAMPLES
    for txt, v in vals:
        lines.append("\tSYSASIC_TRIGGER_EVENT(%s);" % txt)
        mp[len(lines)] = (txt, v, "accept" if 0 <= v <= 95 else "refuse")
    lines += ["}", ""]
    return "\n".join(lines), mp


def sweep_verdict(rc, diag, mp, fname="sysasic_sweep.c"):
    by, stray = {}, 0
    for ln in diag.splitlines():
        if not ERRLINE.search(ln):
            continue
        m = SWEEP_ERR.match(ln)
        if m and os.path.basename(m.group(1)) == fname and int(m.group(2)) in mp:
            by.setdefault(int(m.group(2)), []).append(m.group(4))
        else:
            stray += 1
    attributed = sum(len(v) for v in by.values())
    wrong_acc = [mp[n][0] for n in sorted(mp) if mp[n][2] == "refuse" and n not in by]
    wrong_ref = [mp[n][0] for n in sorted(mp) if mp[n][2] == "accept" and n in by]
    off = [mp[n][0] for n in sorted(by)
           if mp[n][2] == "refuse" and not all(CONST_W.search(x) for x in by[n])]
    void = rc != 0 and attributed == 0
    detail = ("lines=%d erroring=%d wrong-accept=%d wrong-refuse=%d off-class=%d stray=%d "
              "attributed=%s" % (len(mp), len(by), len(wrong_acc), len(wrong_ref), len(off),
                                 stray, "no" if void else "yes"))
    for lab, lst in (("first wrongly ACCEPTED", wrong_acc), ("first wrongly REFUSED", wrong_ref),
                     ("first off-class", off)):
        if lst:
            detail += "; %s: %s" % (lab, ",".join(lst[:6]))
    ok = not void and not wrong_acc and not wrong_ref and not off and stray == 0
    return ok, void, detail


def makefile_vars(tree):
    text = read(os.path.join(tree, "src", "devices", "Makefile"))
    out = {}
    for name in ("CWARNINGS", "COPTIM", "XINCLUDE", "DINCLUDE"):
        m = re.search(r"^%s=(.*)$" % name, text, re.M)
        out[name] = m.group(1).split() if m else []
    return out


def census(cc, tree, hdrdir, logdir):
    mv = makefile_vars(tree)
    #  the header under test FIRST, so it shadows the tree's own copy for every TU that
    #  includes it by "thirdparty/..." from src/devices/ -- which all four do
    flags = mv["CWARNINGS"] + mv["COPTIM"] + ["-I" + hdrdir] + mv["XINCLUDE"] + \
        (mv["DINCLUDE"] or ["-I../include/"])
    cwd = os.path.join(tree, "src", "devices")
    per, bad = [], []
    for tu in TUS:
        rc, out, err = run(cc + flags + ["-E", tu + ".c"], cwd)
        if logdir:
            write(os.path.join(logdir, "CENSUS_%s.err" % tu), err)
        lits, shapes = len(BASE_LIT.findall(out)), len(SHAPE.findall(out))
        per.append("census %s base=%d guards=%d rc=%d" % (tu, lits, shapes, rc))
        if rc != 0 or (lits, shapes) != CENSUS_PIN[tu]:
            bad.append("%s %d and %d (want %d and %d)%s" % (
                tu, lits, shapes, CENSUS_PIN[tu][0], CENSUS_PIN[tu][1],
                "" if rc == 0 else " PREPROCESS FAILED rc %d" % rc))
    detail = " ".join("%s=%d,%d" % (p.split()[1], int(p.split()[2][5:]), int(p.split()[3][7:]))
                      for p in per)
    return not bad, (detail if not bad else "WRONG: " + "; ".join(bad)), per


def is_gcc(cc, work):
    rc, out, err = run(cc + ["-dM", "-E", "-x", "c", os.devnull], work)
    macros = set(re.findall(r"^#define (\w+)", out, re.M))
    return rc == 0 and "__GNUC__" in macros and "__clang__" not in macros \
        and "__INTEL_COMPILER" not in macros


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--header", default=HEADER)
    ap.add_argument("--memory-h", default=MEMORY_H,
                    help="the product's memory.h: MEM_WRITE and PHYSICAL must be 1 and 32 there")
    ap.add_argument("--cc", default="cc",
                    help="the WHOLE compiler command, shell-split; every compiler operation uses all of it")
    ap.add_argument("--prod-flags", default=None)
    ap.add_argument("--census", metavar="TREE", default=None)
    ap.add_argument("--keep", metavar="DIR", default=None,
                    help="write every row's compiler output here (kept)")
    a = ap.parse_args(argv)

    res = []            # (leg, row, ok, detail)
    voids = []

    def row(leg, name, ok, detail):
        res.append((leg, name, ok, detail))
        print("  %-4s  %-4s  %-6s  %s" % ("ok" if ok else "FAIL", leg, name, detail))
        sys.stdout.flush()

    def finish():
        n_prod = sum(1 for r in res if r[0] in ("PROD", "C89"))
        n_pol = sum(1 for r in res if r[0] == "POL")
        red = sum(1 for r in res if not r[2])
        print("PROD rows run: %d" % n_prod)
        print("POL rows run: %d" % n_pol)
        print("rows red: %d" % red)
        print("%d rows, %d failures" % (len(res), red))
        for v in voids:
            print("VOID: " + v)
        tok = "VOID" if voids else ("FAIL" if red else "PASS")
        print("SYSASIC_RANGE_" + tok)
        return {"PASS": 0, "FAIL": 1, "VOID": 2}[tok]

    hdr = os.path.abspath(a.header)
    memh = os.path.abspath(a.memory_h)
    print("sysasic_range_check: header  %s  md5 %s" % (
        hdr, md5(hdr) if os.path.isfile(hdr) else "MISSING"))
    print("sysasic_range_check: cases   %s  md5 %s" % (
        CASES, md5(CASES) if os.path.isfile(CASES) else "MISSING"))
    if not os.path.isfile(hdr) or not os.path.isfile(CASES):
        voids.append("the header or the cases file is missing")
        return finish()
    pd_ok, pd_detail = product_defines(memh)
    print("sysasic_range_check: memory.h %s  md5 %s  %s" % (
        memh, md5(memh) if os.path.isfile(memh) else "MISSING", pd_detail))
    if not pd_ok:
        voids.append("memory.h no longer carries the values the stub passes on (%s)" % pd_detail)
        return finish()
    cc = shlex.split(a.cc)
    if not cc:
        voids.append("--cc is empty")
        return finish()

    found = {}
    for ln in read(CASES).splitlines():
        m = CASE_LINE.match(ln)
        if m:
            found.setdefault((int(m.group(1)), m.group(2)), 0)
            found[(int(m.group(1)), m.group(2))] += 1
    want = dict(((n, r), 1) for r, n, _k in NAMED)
    if found != want:
        voids.append("the cases file does not match the row table: missing %s, extra or "
                      "duplicated %s" % (sorted(set(want) - set(found)),
                                         sorted(k for k in found if want.get(k) != found[k])))
        return finish()

    work = tempfile.mkdtemp(prefix="sysasic_range_")
    try:
        hdrdir = os.path.join(work, "hdr")
        os.makedirs(os.path.join(hdrdir, "thirdparty"))
        shutil.copyfile(hdr, os.path.join(hdrdir, "thirdparty", "dreamcast_sysasicvar.h"))
        shutil.copyfile(CASES, os.path.join(work, "sysasic_range_cases.c"))
        cases = os.path.join(work, "sysasic_range_cases.c")
        logdir = os.path.abspath(a.keep) if a.keep else None
        if logdir:
            os.makedirs(logdir, exist_ok=True)

        rc, out, err = run(cc + ["--version"], work)
        ident = (out.splitlines() or [err.strip() or "(no output)"])[0]
        gcc = is_gcc(cc, work)
        print("sysasic_range_check: cc      %s  %s  [%s]" % (
            " ".join(cc), ident, "gcc" if gcc else "NOT gcc"))
        prod = a.prod_flags.split() if a.prod_flags is not None else PROD_MIRROR.split()
        print("sysasic_range_check: PROD mirror: %s" % " ".join(PROD_MIRROR.split()))
        print("sysasic_range_check: PROD flags (%s): %s" % (
            "--prod-flags" if a.prod_flags is not None else "the mirror", " ".join(prod)))
        print("sysasic_range_check: POL flags: %s" % POL_FLAGS)
        print("sysasic_range_check: C89 flags: %s" % C89_FLAGS)
        if not gcc:
            voids.append("the compiler is not gcc -- the oracle strings are gcc's, and "
                         "nothing else has been measured")
            return finish()

        def keep(name, text):
            if logdir:
                write(os.path.join(logdir, name), text)

        def case_row(leg, flags, name, n, kind):
            if kind == "runtime":
                first = None
                for t in RT_TYPES:
                    tag = t.replace(" ", "_")
                    obj = os.path.join(work, "%s_%s_%s.o" % (leg, name, tag))
                    rc, out, err = run(cc + flags + DIAG + ["-I" + hdrdir, "-DSYSASIC_CASE=%d" % n,
                                       "-DSYSASIC_RT_TYPE=" + t, "-c", "-o", obj, cases], work)
                    keep("%s_%s_%s.err" % (leg, name, tag), "rc=%d\n%s" % (rc, err))
                    ok, detail = refusal(rc, err, NONCONST_W)
                    if not ok:
                        return False, "e %s: %s" % (t, detail)
                    first = first or detail
                return True, first + " -- e an int, a long long and an unsigned long long"
            obj = os.path.join(work, "%s_%s.o" % (leg, name))
            rc, out, err = run(cc + flags + DIAG + ["-I" + hdrdir,
                               "-DSYSASIC_CASE=%d" % n, "-c", "-o", obj, cases], work)
            keep("%s_%s.err" % (leg, name), "rc=%d\n%s" % (rc, err))
            if kind == "accept":
                return accept(rc, err, "accepted; the value assertion in the TU holds")
            return refusal(rc, err, CONST_W)

        def sweep_row(leg, flags):
            src, mp = sweep_source()
            path = os.path.join(work, "sysasic_sweep.c")
            write(path, src)
            rc, out, err = run(cc + flags + DIAG + SWEEP_EXTRA +
                               ["-I" + hdrdir, "-c", "-o",
                                os.path.join(work, "sweep_%s.o" % leg), path], work)
            keep("%s_SWEEP.err" % leg, "rc=%d\n%s" % (rc, err))
            ok, void, detail = sweep_verdict(rc, err, mp)
            if void:
                voids.append("%s SWEEP: rc %d but no error could be attributed to a sweep line "
                             "(%s)" % (leg, rc, first_errors(err)))
            return ok, detail

        def tsweep_row(leg, flags):
            #  -fsyntax-only: the front end alone, which is where a bit-field width is decided.
            #  Measured to give the same error set as -c (t9_syntaxonly), where -c spent over a
            #  minute generating code for an unguarded TRIGGER.
            src, mp = tsweep_source()
            path = os.path.join(work, "sysasic_tsweep.c")
            write(path, src)
            rc, out, err = run(cc + flags + DIAG + SWEEP_EXTRA +
                               ["-I" + hdrdir, "-fsyntax-only", path], work)
            keep("%s_TSWEEP.err" % leg, "rc=%d\n%s" % (rc, err))
            ok, void, detail = sweep_verdict(rc, err, mp, "sysasic_tsweep.c")
            if void:
                voids.append("%s TSWEEP: rc %d but no error could be attributed to a swept raise "
                             "(%s)" % (leg, rc, first_errors(err)))
            return ok, detail

        def run_row(flags, n, name, verdict):
            exe = os.path.join(work, "sysasic_case%d" % n)
            #  PIN B: the run rows under AddressSanitizer -- the 8-byte object extent
            rc, out, err = run(cc + flags + ["-fsanitize=address"] + DIAG + ["-I" + hdrdir,
                               "-DSYSASIC_CASE=%d" % n, "-o", exe, cases], work)
            keep("PROD_%s.err" % name, "rc=%d\n%s" % (rc, err))
            run_rc, run_out = 1, ""
            if rc == 0:
                run_rc, run_out, run_err = run([exe], work, timeout=60)
                keep("PROD_%s.run" % name, "exit=%d\n%s%s" % (run_rc, run_out, run_err))
            return verdict(rc, err, run_rc, run_out)

        #  ---- PROD: the floor leg ----
        for name, n, kind in COMPILE_ONLY:
            ok, detail = case_row("PROD", prod, name, n, kind)
            row("PROD", name, ok, detail)
        ok, detail = run_row(prod, 12, "ID", id_verdict)
        row("PROD", "ID", ok, detail)
        ok, detail = sweep_row("PROD", prod)
        row("PROD", "SWEEP", ok, detail)
        ok, detail = tsweep_row("PROD", prod)
        row("PROD", "TSWEEP", ok, detail)
        ok, detail = run_row(prod, 15, "TVAL", tval_verdict)
        row("PROD", "TVAL", ok, detail)

        #  ---- C89: the header's own sentence ----
        rc, out, err = run(cc + C89_FLAGS.split() + DIAG +
                           ["-I" + hdrdir, "-DSYSASIC_CASE=13", "-c", "-o",
                            os.path.join(work, "c89.o"), cases], work)
        keep("C89_C89.err", "rc=%d\n%s" % (rc, err))
        ok, detail = accept(rc, err, "clean under " + C89_FLAGS)
        row("C89", "C89", ok, detail)

        #  ---- CENSUS: the product TUs (only with a configured tree) ----
        if a.census and not os.path.isfile(os.path.join(a.census, "src", "devices", "Makefile")):
            voids.append("--census %s: no src/devices/Makefile (not a configured tree)" % a.census)
        elif a.census:
            ok, detail, per = census(cc, os.path.abspath(a.census), hdrdir, logdir)
            for p in per:
                print(p)
            row("PROD", "CENSUS", ok, detail)

        #  ---- POL: the portability leg, compile-only rows ----
        polf = POL_FLAGS.split()
        for name, n, kind in COMPILE_ONLY:
            ok, detail = case_row("POL", polf, name, n, kind)
            row("POL", name, ok, detail)
        ok, detail = sweep_row("POL", polf)
        row("POL", "SWEEP", ok, detail)
        ok, detail = tsweep_row("POL", polf)
        row("POL", "TSWEEP", ok, detail)
        return finish()
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
