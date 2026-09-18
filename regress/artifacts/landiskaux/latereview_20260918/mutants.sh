#!/bin/bash
#  mutants.sh -- build Q5's mutants, each in its OWN clone of the post-fix tree
#  (no in-place mutation, so no restore is owed and no sentinel can be left).
set -u
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918
F=/tmp/gxopus_lax_fix
FIXLINE='		alt_status_addr = devinit->addr + 0x16 * devinit->addr_mult;
'
mk() {
    local name="$1" pyexpr="$2"
    local T=/tmp/gxopus_lax_$name
    rm -rf "$T"; cp -a "$F" "$T"
    python3 - "$T/src/devices/dev_wdc.c" "$pyexpr" <<'PYEOF'
import sys
p, how = sys.argv[1], sys.argv[2]
s = open(p).read()
FIX = ("\tcase MACHINE_LANDISK:\n"
       "\t\talt_status_addr = devinit->addr + 0x16 * devinit->addr_mult;\n"
       "\t\tbreak;\n")
assert s.count(FIX) == 1, "fix anchor count %d" % s.count(FIX)
def sub(old, new):
    global s
    assert s.count(old) == 1, "anchor %r count %d" % (old, s.count(old))
    s = s.replace(old, new)
L = "alt_status_addr = devinit->addr + 0x16 * devinit->addr_mult;"
if how == "lit2c":
    sub(L, "alt_status_addr = devinit->addr + 0x2c;")
elif how == "nomult":
    sub(L, "alt_status_addr = devinit->addr + 0x16;")
elif how == "reg7":
    sub(L, "alt_status_addr = devinit->addr + 0x17 * devinit->addr_mult;")
elif how == "shift":
    sub(L, "alt_status_addr = devinit->addr + (0x16 << devinit->addr_mult);")
elif how == "winm1":
    sub(L, "alt_status_addr = devinit->addr + 0x16 * devinit->addr_mult - 1;")
elif how == "firstnobrk":
    #  the same case, placed FIRST and without its break: falls into MACPPC
    sub(FIX, "")
    sub("\tcase MACHINE_MACPPC:\n",
        "\tcase MACHINE_LANDISK:\n\t\t" + L + "\n\tcase MACHINE_MACPPC:\n")
elif how == "lastnobrk":
    sub(FIX, "\tcase MACHINE_LANDISK:\n\t\t" + L + "\n")
elif how == "both":
    #  an ADD-not-MOVE "fix": keep 0x206, register a second window at 0x2c
    sub(FIX, "")
    sub("\tmemory_device_register(devinit->machine->memory, devinit->name,\n",
        "\tif (devinit->machine->machine_type == MACHINE_LANDISK)\n"
        "\t\tmemory_device_register(devinit->machine->memory,\n"
        "\t\t    \"wdc_altstatus\", devinit->addr + 0x2c, 2,\n"
        "\t\t    dev_wdc_altstatus_access, d, DM_DEFAULT, NULL);\n"
        "\tmemory_device_register(devinit->machine->memory, devinit->name,\n")
elif how == "len1":
    sub("    alt_status_addr, 2, dev_wdc_altstatus_access,",
        "    alt_status_addr, 1, dev_wdc_altstatus_access,")
elif how == "guard":
    sub("\t\t" + L + "\n", "\t\tif (devinit->addr == 0x14000000)\n\t\t\t" + L + "\n")
else:
    raise SystemExit("unknown mutant " + how)
open(p, "w").write(s)
print("MUTANT_APPLIED " + how)
PYEOF
    diff -u "$F/src/devices/dev_wdc.c" "$T/src/devices/dev_wdc.c" > "$D/mut_$name.diff"
    cd "$T" && rm -f src/devices/dev_wdc.o && make > "$T.build.log" 2>&1
    if [ "$T/gxemul" -nt "$T/src/devices/dev_wdc.c" ] && [ -e "$T/src/devices/dev_wdc.o" ]; then
        echo "FRESH_OK $name hunks=$(grep -c '^@@' "$D/mut_$name.diff")"
    else
        echo "***BUILD_FAILED $name***"; grep -i error "$T.build.log" | head -5
    fi
}
for m in "$@"; do mk "$m" "$m"; done
echo MUTANTS_BUILT
