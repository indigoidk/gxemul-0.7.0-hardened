# STAGED_DIFFS_fmt.md -- what the fmtattr landing commits, against HEAD and against the working copy

HEAD 79df4277.  Round number #584 (derived: max round heading in HEAD's CHANGELOG.md (#583) + 1).  Built by the landing kit's build_staged_fmt.py at 2026-11-05 20:33 local from `git show HEAD:<path>`, the 47 FINAL files of `_scratchpad/codescan/fmtfix/stage/src/` (built from 79df4277) and the probe in `stage_regress/`.  This record lands as `regress/artifacts/fmtattr/landing_20261105/STAGED_DIFFS_fmt.md`.

## src/ -- 47 files

Every path's HEAD blob equals its blob at `79df4277` (asserted), so each staged file is the stage file -- except `src/cpus/cpu_alpha_palcode.c`, which is HEAD's blob plus the stage's one two-line replace at :136-137, found by exact anchor (owner ruling 2026-11-05, "Fix in both").  The four `#NNN` tags (misc.h's GX_PRINTF comment, the three unreachable `default:` comments) are set to `#584`, each inside a comment, same width, comment-free form equal (kit_fmt.fill).

| path | mode | HEAD md5 | staged md5 | hunks vs HEAD | lines | the working copy now |
|---|---|---|---|---|---|---|
| `src/console/x11.c` | copy | 2a5656a953dd | 34b6412192bb | 1 | +1 -1 | the staged file (post-update) |
| `src/core/emul.c` | copy | d1d25cca8564 | f760e0fd32c8 | 2 | +2 -2 | the staged file (post-update) |
| `src/core/memory.c` | copy | a8d9345c343f | b79e29c93ad4 | 2 | +2 -2 | the staged file (post-update) |
| `src/cpus/cpu_alpha.c` | copy | f83c2ca0b8cf | f91c60ad58ad | 2 | +6 -0 | the staged file (post-update) |
| `src/cpus/cpu_alpha_palcode.c` | anchor | 7d11fece2eb5 | f69c02e83030 | 1 | +2 -2 | post-update (the two lines applied) |
| `src/cpus/cpu_arm.c` | copy | 67805fcdda54 | d019bb1ee5e0 | 2 | +2 -2 | the staged file (post-update) |
| `src/cpus/cpu_i960.c` | copy | d151c45da84a | d9ba4020984f | 1 | +1 -1 | the staged file (post-update) |
| `src/cpus/cpu_m88k.c` | copy | 0321e2ba68c8 | 2362b2934aa1 | 15 | +17 -14 | the staged file (post-update) |
| `src/cpus/cpu_mips.c` | copy | c2bac40930d8 | 2b6d7b2c1f1c | 1 | +1 -1 | the staged file (post-update) |
| `src/cpus/cpu_ppc.c` | copy | c56dd16165cf | b92f3b38a8e0 | 3 | +3 -3 | the staged file (post-update) |
| `src/cpus/cpu_sh.c` | copy | db65b19bab44 | 8ccc9d995672 | 4 | +4 -4 | the staged file (post-update) |
| `src/debugger/debugger_cmds.c` | copy | 7c948ab0637e | 6321308b827f | 1 | +1 -1 | the staged file (post-update) |
| `src/devices/dev_8253.c` | copy | a081564373cf | 9d22fea71cf0 | 3 | +3 -3 | the staged file (post-update) |
| `src/devices/dev_ahc.c` | copy | 4c56ae0db0f4 | d819903a11d3 | 1 | +1 -1 | the staged file (post-update) |
| `src/devices/dev_asc.c` | copy | 5d7ac7a0989f | e95797d9f517 | 3 | +3 -3 | the staged file (post-update) |
| `src/devices/dev_bt455.c` | copy | 5e2fd01c859b | 0ed701f74416 | 2 | +3 -2 | the staged file (post-update) |
| `src/devices/dev_dc7085.c` | copy | 1ca658aa9480 | e9e859128512 | 2 | +4 -2 | the staged file (post-update) |
| `src/devices/dev_dec21030.c` | copy | f5c26a495844 | eefd5254cf33 | 2 | +2 -2 | the staged file (post-update) |
| `src/devices/dev_dec5800.c` | copy | e9997f51a4c0 | ec9e83fbb731 | 2 | +2 -4 | the staged file (post-update) |
| `src/devices/dev_dec_ioasic.c` | copy | 56a7c3ce2e94 | aa9d38c0d249 | 42 | +42 -42 | the staged file (post-update) |
| `src/devices/dev_ether.c` | copy | f4955db10c0b | 1fab480fbf36 | 1 | +1 -1 | the staged file (post-update) |
| `src/devices/dev_le.c` | copy | 55d47bdae410 | 63fec99befae | 6 | +10 -9 | the staged file (post-update) |
| `src/devices/dev_luna88k.c` | copy | e43c39ca5722 | 7c36aa91d24d | 2 | +2 -2 | the staged file (post-update) |
| `src/devices/dev_lunafb.c` | copy | 2e39fc412870 | d1807e8b501c | 4 | +4 -4 | the staged file (post-update) |
| `src/devices/dev_mb89352.c` | copy | 7dd3c468ec7a | dace84697dc0 | 5 | +5 -5 | the staged file (post-update) |
| `src/devices/dev_mp.c` | copy | bb97e0daeb22 | 2feef5951ad1 | 1 | +2 -2 | the staged file (post-update) |
| `src/devices/dev_ps2_gif.c` | copy | 844e185d4d17 | a31b79c0e3e1 | 1 | +1 -1 | the staged file (post-update) |
| `src/devices/dev_ps2_stuff.c` | copy | d3a9d9a64d8d | 6071d54ea3dd | 1 | +1 -1 | the staged file (post-update) |
| `src/devices/dev_pvr.c` | copy | f2fc508e34c5 | e5c5112242f1 | 1 | +1 -1 | the staged file (post-update) |
| `src/devices/dev_px.c` | copy | df90fbfe61c2 | 82f31abbb568 | 1 | +1 -1 | the staged file (post-update) |
| `src/devices/dev_sgi_ip32.c` | copy | 8c1d1545eedd | 12aa570c5be5 | 6 | +6 -6 | the staged file (post-update) |
| `src/devices/dev_sgi_mec.c` | copy | 055872383757 | 8e727289e9f5 | 7 | +18 -18 | the staged file (post-update) |
| `src/devices/dev_sgi_re.c` | copy | 23fa76aa9523 | 5df7da3731e2 | 12 | +13 -13 | the staged file (post-update) |
| `src/devices/dev_vga.c` | copy | e80cf7dcd2f8 | 6b0796e5c458 | 1 | +2 -2 | the staged file (post-update) |
| `src/devices/dev_vr41xx.c` | copy | 05b3a7ab01f5 | 420556184bf1 | 2 | +2 -2 | the staged file (post-update) |
| `src/devices/dev_wdc.c` | copy | 4a1bc4d46275 | 829f3b6217ec | 2 | +2 -2 | the staged file (post-update) |
| `src/disk/bootblock.c` | copy | 005747364ded | 1f1fb1da6288 | 2 | +3 -3 | the staged file (post-update) |
| `src/disk/diskimage.c` | copy | 8dc83c7ff26d | ded258963466 | 1 | +2 -2 | the staged file (post-update) |
| `src/disk/diskimage_scsicmd.c` | copy | 0154b237593b | c750a66eee89 | 13 | +13 -13 | the staged file (post-update) |
| `src/file/file_aout.c` | copy | 7ef978f187d3 | d091fc62d800 | 1 | +1 -1 | the staged file (post-update) |
| `src/file/file_ecoff.c` | copy | 9a5d6a2c5b94 | 5d9ec3502334 | 2 | +5 -4 | the staged file (post-update) |
| `src/file/file_macho.c` | copy | b399e0f8c84e | c483d5dd4518 | 1 | +1 -1 | the staged file (post-update) |
| `src/include/misc.h` | copy | ebe0280fdb51 | a824683b06a8 | 3 | +12 -4 | the staged file (post-update) |
| `src/net/net.c` | copy | 6f35d7457280 | 126cf437339a | 2 | +2 -2 | the staged file (post-update) |
| `src/net/net_ip.c` | copy | 7fc0661f262e | d988f27eb9cc | 1 | +1 -1 | the staged file (post-update) |
| `src/promemul/arcbios.c` | copy | c95dbc00e4f0 | 26dd7d061169 | 1 | +1 -2 | the staged file (post-update) |
| `src/promemul/ps2_bios.c` | copy | b754938484e3 | 1446dd812b08 | 1 | +1 -1 | the staged file (post-update) |

### the fills

```
src/cpus/cpu_alpha.c:353: /*  #584: unreachable (the enclosing switch admits only the
src/cpus/cpu_alpha.c:648: /*  #584: unreachable (the enclosing switch admits only the
src/cpus/cpu_m88k.c:1436: /*  #584: unreachable (the enclosing switch admits only the
src/include/misc.h:260: /*  #584: the diagnostic functions are printf-like; with GCC or clang a format
```

### added lines wider than 79 columns (tabs at 8; reported, not changed: the stage files are final)

81: src/core/memory.c:624, src/core/memory.c:636, src/cpus/cpu_alpha_palcode.c:136, src/cpus/cpu_m88k.c:703, src/cpus/cpu_m88k.c:708, src/cpus/cpu_m88k.c:713, src/cpus/cpu_m88k.c:718, src/cpus/cpu_m88k.c:723, src/cpus/cpu_m88k.c:728, src/cpus/cpu_m88k.c:733, src/cpus/cpu_m88k.c:738, src/cpus/cpu_m88k.c:743, src/cpus/cpu_m88k.c:748, src/cpus/cpu_m88k.c:753, src/cpus/cpu_m88k.c:758, src/cpus/cpu_m88k.c:762, src/cpus/cpu_m88k.c:777, src/cpus/cpu_m88k.c:1436, src/cpus/cpu_m88k.c:1437, src/cpus/cpu_mips.c:2118, src/devices/dev_bt455.c:77, src/devices/dev_dec21030.c:200, src/devices/dev_dec21030.c:205, src/devices/dev_dec_ioasic.c:100, src/devices/dev_dec_ioasic.c:111, src/devices/dev_dec_ioasic.c:122, src/devices/dev_dec_ioasic.c:133, src/devices/dev_dec_ioasic.c:144, src/devices/dev_dec_ioasic.c:155, src/devices/dev_dec_ioasic.c:166, src/devices/dev_dec_ioasic.c:321, src/devices/dev_dec_ioasic.c:365, src/devices/dev_le.c:928, src/devices/dev_le.c:938, src/devices/dev_le.c:1061, src/devices/dev_luna88k.c:916, src/devices/dev_lunafb.c:82, src/devices/dev_lunafb.c:174, src/devices/dev_mb89352.c:433, src/devices/dev_mb89352.c:678, src/devices/dev_mp.c:247, src/devices/dev_ps2_stuff.c:240, src/devices/dev_sgi_mec.c:461, src/devices/dev_sgi_mec.c:462, src/devices/dev_sgi_mec.c:470, src/devices/dev_sgi_mec.c:471, src/devices/dev_sgi_mec.c:474, src/devices/dev_sgi_mec.c:475, src/devices/dev_sgi_mec.c:607, src/devices/dev_sgi_mec.c:608, src/devices/dev_sgi_mec.c:609, src/devices/dev_sgi_mec.c:613, src/devices/dev_sgi_mec.c:614, src/devices/dev_sgi_mec.c:615, src/devices/dev_sgi_mec.c:621, src/devices/dev_sgi_mec.c:622, src/devices/dev_sgi_mec.c:623, src/devices/dev_sgi_mec.c:627, src/devices/dev_sgi_mec.c:628, src/devices/dev_sgi_mec.c:629, src/devices/dev_sgi_re.c:1258, src/devices/dev_sgi_re.c:1272, src/devices/dev_sgi_re.c:1280, src/devices/dev_sgi_re.c:1288, src/devices/dev_sgi_re.c:1296, src/devices/dev_sgi_re.c:1304, src/devices/dev_sgi_re.c:1312, src/devices/dev_sgi_re.c:1321, src/devices/dev_sgi_re.c:1335, src/devices/dev_sgi_re.c:1343, src/devices/dev_sgi_re.c:1726, src/devices/dev_wdc.c:1607, src/devices/dev_wdc.c:1641, src/disk/bootblock.c:435, src/disk/bootblock.c:442, src/disk/bootblock.c:443, src/disk/diskimage.c:2460, src/disk/diskimage_scsicmd.c:475, src/file/file_ecoff.c:256, src/include/misc.h:277, src/include/misc.h:278

### src/cpus/cpu_alpha_palcode.c -- the peer's hold

HEAD md5 7d11fece2eb5bebdfb48dc51167ddf30; staged (HEAD + the two lines) md5 f69c02e83030dd1d990266dc2a6d76b6; the working copy md5 c7f148509f7c00e38d1b506ef8b87b33.  The working copy carries the peer session's uncommitted lines (1 hunk(s) against HEAD: HEAD line 421, insert, 0 -> 23 lines), which this commit does NOT carry; the tree update applies only the two lines to it (before md5 30c05d1594c50c1969236e4706be9681, after md5 c7f148509f7c00e38d1b506ef8b87b33).

### staged vs HEAD (the commit's change of this file)

1 hunk(s):

```
@@ replace  first side line 136 (2 lines) -> second side line 136 (2 lines)
-         default:fatal("[ Alpha PALcode: GXemul PROM getenv %i: TODO "
-                 "]\n", cpu->cd.alpha.r[ALPHA_A1]);
+         default:fatal("[ Alpha PALcode: GXemul PROM getenv %" PRIi64 ": TODO "
+                 "]\n", (int64_t)cpu->cd.alpha.r[ALPHA_A1]);
```

## regress/fmt_bootblock_probe.py (new)

Byte-identical to `_scratchpad/codescan/fmtfix/stage_regress/fmt_bootblock_probe.py` (md5 5728fc0761fd671b8d9426bc61e4bb15, 3392 bytes): compiles; no `#NNN`; section U's docstring reading against the pin 3 finds no stale claim.

## regress/gate_build.sh

HEAD md5 3173f3d0c8027fd68a05858bcc204b42; staged md5 362b6640ce4057de52cdc0fe9a34f1c1; the working copy == HEAD.  One insert: the fmtattr block, 48 lines, directly after the `arc: build_tree ran to completion` check (line 247 of the staged file) and above `gate_end` (line 334), so its 14 checks count toward the verdict that decides publication.  `bash -n`: clean.  Section U (comment lines naming fmt_bootblock against the pin 3): no stale claim.

### staged vs HEAD

1 hunk(s):

```
@@ insert  first side line 247 (0 lines) -> second side line 247 (48 lines)
+ #  ------------------------------------------------------------ fmtattr (#584)
+ #  THE PRINTF-FORMAT CLASS IS ENFORCED HERE.  src/include/misc.h declares debug(), fatal(),
+ #  debugmsg() and debugmsg_cpu() with GX_PRINTF -- format(printf, ...) under __GNUC__ -- so a
+ #  format that does not match its arguments is a compiler WARNING, and build_tree() above
+ #  already fails this gate on any warning in either tree.  The build itself stays
+ #  warning-only, not -Werror: owner ruling 2026-11-05, the enforcement is a gate check.
+ #  The warning count cannot see two things, so they are checked here:
+ #
+ #   * THE ATTRIBUTES THEMSELVES.  Drop GX_PRINTF from a declaration, or define it empty,
+ #     and every mismatch goes silent while the count stays 0.  So one deliberate mismatch
+ #     per function, each on its own line, compiled with this tree's own CC and CWARNINGS
+ #     against the headers just built, must warn: four controls, four warnings, no others.
+ #   * A TYPE-COMPATIBLE WRONG VALUE.  PRIx64 -> PRIu64, or (uint64_t)(uint32_t)x, keeps the
+ #     argument's type, so no compiler sees it.  fmt_bootblock_probe.py pins ONE
+ #     representative wide-hex repair by its OUTPUT: bootblock.c's SGI loading line must
+ #     print disk offset 0x100000000, where it printed the low 32 bits before the fix.  The
+ #     rest of that class is disclosed in the probe's contract, not claimed.
+ FMTCTL=$LOGDIR/fmtctl.c
+ printf '%s\n' '#include <stdio.h>' '#include <stdint.h>' 'struct cpu;' '#include "misc.h"' \
+     'void fmtctl(struct cpu *c) {' \
+     'debug("%i", (int64_t)1);' \
+     'fatal("%i", (int64_t)1);' \
+     'debugmsg(0, "x", 0, "%i", (int64_t)1);' \
+     'debugmsg_cpu(c, 0, "x", 0, "%i", (int64_t)1);' \
+     '}' > "$FMTCTL"
+ fmtcc=$(sed -n 's/^CC=//p' "$ARC_TREE/src/Makefile" 2>/dev/null | head -1)
+ fmtcw=$(sed -n 's/^CWARNINGS=//p' "$ARC_TREE/src/Makefile" 2>/dev/null | head -1)
+ ( cd "$LOGDIR" && ${fmtcc:-cc} $fmtcw -fsyntax-only -I"$ARC_TREE/src/include" fmtctl.c ) \
+     > "$LOGDIR/fmtctl.log" 2>&1
+ check "fmt controls: the control file compiled"   "$?" "0"
+ check "fmt controls: warnings of every kind"      "$(grep -c 'warning:' "$LOGDIR/fmtctl.log")" "4"
+ for fmtfn in 6:debug 7:fatal 8:debugmsg 9:debugmsg_cpu; do
+     check "fmt control ${fmtfn#*:} (line ${fmtfn%%:*}) warns" \
+         "$(grep -cE "^fmtctl\.c:${fmtfn%%:*}:[0-9]+: warning: format .*\[-Wformat=?\]" "$LOGDIR/fmtctl.log")" "1"
+ done
+ FMTBBLOG=$LOGDIR/fmt_bootblock.log
+ python3 -u "$HERE/fmt_bootblock_probe.py" "$ARC_TREE/gxemul" gate > "$FMTBBLOG" 2>&1
+ fbres=$(grep -x 'FMTBB_RESULT=[0-9]*/[0-9]*' "$FMTBBLOG" | tail -1)
+ fbres=${fbres#FMTBB_RESULT=}
+ check "fmt_bootblock rows run"      "${fbres#*/}" 3
+ check "fmt_bootblock rows correct"  "${fbres%/*}" "3"
+ check "fmt_bootblock result line"   "$(grep -cx 'FMTBB_RESULT=3/3' "$FMTBBLOG")" "1"
+ check "fmt_bootblock control"       "$(grep -cx 'FMTBB_CONTROL=OK' "$FMTBBLOG")" "1"
+ check "fmt_bootblock sentinel last" "$(tail -n 1 "$FMTBBLOG")" "FMTBB_DONE"
+ for fmtrow in "session ended" "voldir parsed" "loading offset"; do
+     check "fmt_bootblock row: $fmtrow" "$(grep -c "^$fmtrow .* ok$" "$FMTBBLOG")" "1"
+ done
+ #  ------------------------------------------------------------ end fmtattr (#584)
```

## tools/precommit_check.sh

HEAD md5 ce25fc040cc20d48c65221735910461d (SCORE_CLAIMS_MANIFEST=49); staged md5 7c878c20dc21195efdccf4b39eebdbb2 (=50); the working copy == HEAD.  `bash -n`: clean.

### staged vs HEAD

1 hunk(s):

```
@@ replace  first side line 382 (1 lines) -> second side line 382 (3 lines)
-     SCORE_CLAIMS_MANIFEST=49
+     #  RAISED 49 -> 50 ON 2026-11-05, DELIBERATELY.  One newly gated probe: fmt_bootblock_probe.py
+     #  (#584 fmtattr, pinned UNQUOTED in gate_build.sh at 3 rows under the stem fmt_bootblock; its docstring is checked).
+     SCORE_CLAIMS_MANIFEST=50
```

## .github/workflows/codeql.yml and .github/codeql/codeql-config.yml (new)

Verbatim from `_scratchpad/codescan/github/` (md5 271a042209e9, b1b233d8afe5): CodeQL ADVANCED setup -- C/C++, build-mode none, paths-ignore regress/artifacts and experiments (owner ruling 2026-11-05).  The repository setting is the OWNER's to flip after the next push; `codeqlscope` stays open for it.  The action tags it pins exist (`gh api`, 2026-11-05: actions/checkout v7 -> refs/tags/v7, github/codeql-action v4 -> refs/tags/v4).

## the four trees (TREES_fmt.txt)

```
est                                      part 1 PASS (46 == the SEC working copy; palcode == the committed file, held by the hook swap); part 2 N/A (source tree, no binary); sentinels none (.MUTANT, .LANDING*); vs the update: 0 pre, 47 post of 47
build                                    part 1 PASS (46 == the SEC working copy; palcode == the committed file, held by the hook swap); part 2 PASS: binary newer than all 47 (gxemul 11-05 20:25:15); sentinels none (.MUTANT, .LANDING*); vs the update: 0 pre, 47 post of 47
build-asan                               part 1 PASS (46 == the SEC working copy; palcode == the committed file, held by the hook swap); part 2 PASS: binary newer than all 47 (gxemul 11-05 20:25:26); sentinels none (.MUTANT, .LANDING*); vs the update: 0 pre, 47 post of 47
//wsl.localhost/Gentoo/tmp/gxsec-build   part 1 PASS (46 == the SEC working copy; palcode == the committed file, held by the hook swap); part 2 PASS: binary newer than all 47 (gxemul 11-05 20:25:26); sentinels none (.MUTANT, .LANDING*); vs the update: 0 pre, 47 post of 47
TREES_SUMMARY ATTRIBUTED; TREES ALL CLEAR: the tree update has run -- the SEC working copy and all four trees hold the 46 staged files and the palcode copy with only the two lines applied, and the three build trees' binaries are newer than all 47
```
