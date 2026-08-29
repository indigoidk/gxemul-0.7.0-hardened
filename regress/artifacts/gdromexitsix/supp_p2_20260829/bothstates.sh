#!/bin/bash
#  *** THE TREE MOVED UNDER THIS REVIEW.  THIS FILE MEASURES BOTH STATES AND SAYS
#  WHICH IS WHICH, because an artifact whose caption describes one code state and
#  whose numbers describe another is the frozen-number defect at its worst. ***
#
#    PRE  = the assert as it stood at 13:35 today, OR-based:
#             (LEN | NODATA | ... | CMD) == ((1u << NBITS) - 1u)
#           pinned copy, md5 6366988a5156c59a9b6bc8cc7aab9ec2
#    POST = the assert the main loop landed at ~14:4x, SUM-based:
#             (LEN + NODATA + ... + CMD) == ((1u << NBITS) - 1u)
#           live file, md5 53dd0e22fcc46a5f9e2ba921d62ea9d9
#
#  Every state is run against BOTH.  Read the two columns, not one.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
BLD=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
PIN=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pin_20260829/dev_dreamcast_gdrom.c
LIVE=$SEC/src/devices/dev_dreamcast_gdrom.c
T=/tmp/gdromboth; rm -rf "$T"; mkdir -p "$T"
INC="-I $BLD -I $SEC/src/include -I $SEC/src/include/thirdparty"

echo "  PRE  (OR-based)  md5 $(md5sum "$PIN"  | cut -d' ' -f1)"
echo "  POST (SUM-based) md5 $(md5sum "$LIVE" | cut -d' ' -f1)"
echo

mk () {  # $1 out, $2 base-source, $3 shape
  cp "$2" "$1"
  python3 - "$1" "$3" <<'PYEOF'
import io, sys
p, shape = sys.argv[1], sys.argv[2]
L = io.open(p, encoding="utf-8").read().split(chr(10))
def find(tok):
    h = [i for i, s in enumerate(L) if s.strip().startswith(tok)]
    assert len(h) == 1, "want one %s, got %d" % (tok, len(h))
    return h[0]
if shape == "cmd_inplace":
    i = find("GDROM_W_CMD_B,"); L[i] = L[i].replace("GDROM_W_CMD_B,", "GDROM_W_CMD_B = GDROM_W_FMT_B,")
elif shape == "fmt_moved":
    i = find("GDROM_W_FMT_B,")
    line = L[i].replace("GDROM_W_FMT_B,", "GDROM_W_FMT_B = GDROM_W_OVERREAD_B,")
    del L[i]; j = find("GDROM_W_OVERREAD_B,"); L[j+1:j+1] = [line]
elif shape == "fmt_inplace":
    i = find("GDROM_W_FMT_B,"); L[i] = L[i].replace("GDROM_W_FMT_B,", "GDROM_W_FMT_B = GDROM_W_OVERREAD_B,")
elif shape == "define_alias":          # E1 as originally built: the #define side
    i = find("#define\tGDROM_W_FMT"); L[i] = "#define\tGDROM_W_FMT\t(1u << GDROM_W_OVERREAD_B)"
elif shape == "multibit":              # a mask redefined as a SUPERSET
    i = find("#define\tGDROM_W_FMT")
    L[i] = "#define\tGDROM_W_FMT\t((1u << GDROM_W_FMT_B) | (1u << GDROM_W_OVERREAD_B))"
elif shape == "tenth_back":            # a tenth bit, OR list not extended
    i = find("GDROM_W_CMD_B,"); L[i+1:i+1] = ["\tGDROM_W_TENTH_B,"]
elif shape == "tenth_front":
    i = find("GDROM_W_LEN_B,"); L[i:i] = ["\tGDROM_W_ZEROTH_B,"]
elif shape == "none":
    pass
else:
    raise SystemExit("unknown shape " + shape)
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(L))
PYEOF
}

cell () {  # $1 base-source, $2 shape  -> prints COMPILES|REFUSED
  mk "$T/f.c" "$1" "$2"
  if gcc -O2 -std=gnu99 -c "$T/f.c" -o "$T/f.o" $INC 2>"$T/e"; then echo COMPILES; else echo REFUSED; fi
}

rowline () {  # $1 label, $2 shape, $3 wantPRE, $4 wantPOST
  a=$(cell "$PIN" "$2"); b=$(cell "$LIVE" "$2")
  ma=ok; mb=ok
  [ "$a" = "$3" ] || ma="<-- ESCAPE"
  [ "$b" = "$4" ] || mb="<-- ESCAPE"
  printf '  %-44s  PRE(|): %-9s %-11s POST(+): %-9s %s\n' "$1" "$a" "$ma" "$b" "$mb"
}

echo "=== EVERY STATE, AGAINST BOTH ASSERT FORMS ==="
echo "    (want: COMPILES only for the correct source; REFUSED for every defect)"
echo
rowline "A0. unmodified"                              none         COMPILES COMPILES
echo "  -- #define-side aliases: both forms already caught these --"
rowline "A1. #define FMT -> OVERREAD_B  (E1 as built)" define_alias REFUSED  REFUSED
echo "  -- ENUM-side aliases: the gap this review found --"
rowline "A2. enum CMD_B = FMT_B (ONE TOKEN, M3shared)" cmd_inplace  REFUSED  REFUSED
rowline "A3. enum FMT_B = OVERREAD_B, MOVED (E1)"      fmt_moved    REFUSED  REFUSED
rowline "A4. enum FMT_B = OVERREAD_B, in place"        fmt_inplace  REFUSED  REFUSED
echo "  -- MULTI-BIT mask: the case the landed comment claims for '+' --"
rowline "A5. FMT redefined as a SUPERSET (2 bits)"     multibit     REFUSED  REFUSED
echo "  -- COMPLETENESS: does '+' keep what '|' had? --"
rowline "A6. tenth bit at BACK, OR list not extended"  tenth_back   REFUSED  REFUSED
rowline "A7. bit at FRONT, OR list not extended"       tenth_front  REFUSED  REFUSED
echo
echo "BOTHSTATES_DONE"
