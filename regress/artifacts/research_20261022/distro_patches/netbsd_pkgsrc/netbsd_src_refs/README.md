# NetBSD source references (read-only evidence for B_distro_patches.md)

Copies of five NetBSD `sys/dev/ata` / `sys/dev/ic` sources consulted while cross-checking the FreeBSD/DragonFly
`dev_wdc.c` LBA patch (which register bit NetBSD sets on its CHS requests).  They carry a `.txt` suffix ON PURPOSE:
with their real names (`wdcreg.h`, `atareg.h`, `wd.c`, `wdc.c`, `ata_wdc.c`) a tracked copy here would be found by
precommit section D's header lookup (`git ls-files "*/wdcreg.h" | head -1`) BEFORE the fork's own
`src/include/thirdparty/wdcreg.h`, making every `wdcreg.h:NNN` citation in the records check against the wrong file.
Found by the records drafter's section-D emulation on 2026-10-22 before the directory was committed.
