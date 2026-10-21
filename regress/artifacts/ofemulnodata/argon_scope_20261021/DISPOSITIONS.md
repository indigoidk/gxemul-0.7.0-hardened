# Argon ofexits (2026-10-21 08:36-08:38, 167 s, extended OFF) -- the main loop's dispositions

A packet-fed SCOPING reading of src/promemul/of.c's exit(1) family; verdict SEVERAL ROUNDS.  The first control (08:31)
returned an app error ("I seem to be encountering an error") and the sender stopped as designed; kept as
failed_control_0831/.  The re-fire's control passed (08:35) and the packet answered.  Each point below was checked by
READING the tree at 7f48ea10; nothing was measured.

1. **`ofemulnodata`'s title -- BROKEN, corrected.**  machine_macppc.c: `if (!machine->prom_emulation) return;` precedes
   `of_emul_init(...)`, so macppc without PROM emulation has `of_data == NULL` too.
2. **"may share one round" (the row's note) -- a design dissent, recorded.**  Argon: three rounds under the round-scope
   rule (of.c:1100 is a decoder-level gate on machines WITHOUT OpenFirmware; :394 and :448 are service handlers on macppc
   WITH it, with different members and oracles).  For the rows' passes 1 to weigh; not a ruling.
3. **of.c:549, :577 (of_add_device / of_add_prop) and :1120, :1201 (of_emul's arch-switch defaults) -- UNREACHABLE,
   holds.**  The first two run only inside machine setup with fixed arguments; only ARM and PowerPC call of_emul.
4. **Design for of.c:1100 -- recorded as input.**  Gate the magic word at cpu_arm_instr.c's SWI case and
   cpu_ppc_instr.c's sc case on `of_data != NULL` (the default handlers `cond_instr(swi)` / `instr(sc)` are already set
   up there), so the word executes as the architectural SWI / system call; an early return inside of_emul would leave
   X(openfirmware) jumping to the link register.
5. **ARM's 0xef8c64eb reboot magic -- a DIFFERENT ROW: filed as `armrebootmagic` (MED).**  READ: the SWI decode case
   routes the word to X(reboot) (`cpu->running = 0`) with no machine or privilege test; machine_cats.c plants it at
   0x41000008 as the cats PROM's reboot entry.
