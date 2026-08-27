"""Q3 on my own row, before a seat asks it: does row_rejected_cmd_resets() pass for
the RIGHT REASON?

It aims at the SECOND early-return guard in wdc_command():

    if (diskimage_is_a_cdrom(...) && d->cur_command == WDCC_IDENTIFY) {
            d->error |= WDCE_ABRT;
            d->int_assert = 1;
            return;
    }

and asserts `stub_scsi_cmds` unchanged and `atapi_cmd_in_progress == 0`.  BOTH of
those would ALSO hold if the guard never fired -- a plain IDENTIFY on a non-CD-ROM
runs the reset too and issues no SCSI command.  So the row might be green without
ever reaching the thing it is named for.

THE TEST: build a variant with `stub_cdrom_poison = 0` in that row only, so the
guard CANNOT fire, and see whether the row still passes.  If it does, the row is
under-specified and adding a WDCE_ABRT assertion has a MEASURED DELTA rather than
being "it cannot hurt".
"""
import io, os, shutil

C = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
     r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\r480")
O = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
     r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\q3")

s = io.open(os.path.join(C, "regress", "diff_wdc_identify.c"),
            encoding="utf-8", newline="").read()

#  locate the row, then edit ONLY inside it -- the poison assignment appears twice
#  in the file (set and restore) and elsewhere in other rows.
start = s.index("static void row_rejected_cmd_resets(void)")
end = s.index("static void row_refill_cmd_resets(void)")
body = s[start:end]

OLD = "\tstub_cdrom_poison = 1;\t\t/*  an ATAPI-only controller  */\n"
assert body.count(OLD) == 1, "poison set in row: %d" % body.count(OLD)
nb = body.replace(OLD, "\tstub_cdrom_poison = 0;\t\t/*  Q3: guard CANNOT fire  */\n", 1)
assert nb != body

if os.path.isdir(O):
    shutil.rmtree(O)
os.makedirs(os.path.join(O, "regress"))
os.makedirs(os.path.join(O, "src", "devices"))
io.open(os.path.join(O, "regress", "diff_wdc_identify.c"),
        "w", encoding="utf-8", newline="").write(s[:start] + nb + s[end:])
shutil.copy(os.path.join(C, "src", "devices", "dev_wdc.c"),
            os.path.join(O, "src", "devices", "dev_wdc.c"))
print("  Q3 variant written: the guard cannot fire in that row")
