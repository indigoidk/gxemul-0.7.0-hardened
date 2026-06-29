# GXemul est-0.7.0 — Battery Pass Map  (2026-06-28)

5 CPU arches · 13 OS images · 3 OS families (OpenBSD 2.2–7.7, NetBSD 8.2, Linux 3.2)

## Depth reached (what each OS image actually exercised)

```
 DEPTH                                                            OS IMAGE                 ARCH
 ════════════════════════════════════════════════════════════════════════════════════════════
 ███  FULL MULTIUSER     root · NAT 0% · disk cksum ·             OpenBSD 2.2 / pmax       MIPS
      (the deep rig)     syslogd · reboot-persist
 ────────────────────────────────────────────────────────────────────────────────────────────
 ██   INTERACTIVE        # shell · sysctl · dmesg                 OpenBSD 7.7 / luna88k    M88K
      SHELL                                                       NetBSD  8.2 / landisk    SH4
 ────────────────────────────────────────────────────────────────────────────────────────────
 █    BOOT +             banner · device-attach assert ·          OpenBSD 2.3 / arc        MIPS
      DEVICE-ATTACH      no panic / fatal / ASan                  NetBSD  8.2 / arc        MIPS
      + NO-PANIC                                                  NetBSD  8.2 / hpcmips    MIPS
                                                                  NetBSD  8.2 / sgi o2     MIPS
                                                                  Linux   3.2 / malta      MIPS
                                                                  NetBSD  8.2 / cats       ARM
                                                                  NetBSD  8.2 / prep       PPC
 ────────────────────────────────────────────────────────────────────────────────────────────
 ▒    PARTIAL            pre-existing GXemul skeletal-OF limit    NetBSD  8.2 / macppc g4     PPC
      (NOT a             — boots to OpenFirmware / ramdisk-       NetBSD  8.2 / macppc g4plus PPC
       regression)       userland-start, byte-identical on the   OpenBSD 3.4 / macppc       PPC
                         pristine baseline
```

## Full pass matrix

| OS / version | `-E` machine | Arch | Boot | Dev-attach | No-panic | Shell | Root | NAT | Disk | Daemons | Persist |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| OpenBSD 2.2 | pmax (3max)   | MIPS | ✅ multiuser | ✅ sd0/scsibus | ✅ | ✅ | ✅ uid=0 | ✅ 0% | ✅ cksum | ✅ syslogd | ✅ fsck-clean |
| OpenBSD 7.7 | luna-88k      | M88K | ✅ | ✅ (9) | ✅ | ✅ `#` | — | — | — | — | — |
| NetBSD 8.2  | landisk       | SH4  | ✅ | ✅ (14) | ✅ | ✅ `#` | — | — | — | — | — |
| OpenBSD 2.3 | arc (pica)    | MIPS | ✅ | ✅ jazzio | ✅ | — | — | — | — | — | — |
| NetBSD 8.2  | arc (pica)    | MIPS | ✅ | ✅ (22) | ✅ | — | — | — | — | — | — |
| NetBSD 8.2  | hpcmips       | MIPS | ✅ | ✅ (11) | ✅ | — | — | — | — | — | — |
| NetBSD 8.2  | sgi (o2/IP32) | MIPS | ✅ | ✅ (21) | ✅ | — | — | — | — | — | — |
| Linux 3.2   | malta         | MIPS | ✅ | ✅ (6)  | ✅ | — | — | — | — | — | — |
| NetBSD 8.2  | cats          | ARM  | ✅ | ✅ (2)  | ✅ | — | — | — | — | — | — |
| NetBSD 8.2  | prep          | PPC  | ✅ | ✅ (18) | ✅ | — | — | — | — | — | — |
| NetBSD 8.2  | macppc g4     | PPC  | ⚠️ OF wall | — | ✅ | — | — | — | — | — | — |
| NetBSD 8.2  | macppc g4plus | PPC  | ⚠️ BATs→OF | — | ✅ | — | — | — | — | — | — |
| OpenBSD 3.4 | macppc        | PPC  | ⚠️ rd-userland | — | ✅ | — | — | — | — | — | — |

**Legend:** ✅ pass · ⚠️ partial (pre-existing GXemul limit, not a regression) · — not exercised (no installed
userland on that image). Dev-attach (N) = number of asserted devices probed.

## Summary
- **10 / 13 OS images pass the core battery** (boot + device-attach + no-panic). The 3 macppc images are
  partial due to GXemul's pre-existing skeletal OpenFirmware — proven byte-identical on the pristine baseline,
  i.e. **not introduced by our changes**.
- **Deep coverage on 3 / 5 arches:** MIPS (full multiuser rig), M88K + SH4 (interactive shell).
- **Whole-tree (applies to every row — one binary):** gcc `-O3 -Wall -Wextra` **0/0**, clang-21 **0/0**,
  **0 spurious warnings** from the course-correction guards.
