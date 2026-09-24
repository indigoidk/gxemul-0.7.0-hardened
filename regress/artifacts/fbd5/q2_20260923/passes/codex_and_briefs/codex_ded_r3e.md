Read-only review of a C test file and the device model it tests. Do not edit or build anything.

Files (frozen copies; read these, not any other copy of GXemul under the project root):
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2h\frozen\dev_footbridge.c        (device model, md5 783c0c7f)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2h\frozen\diff_footbridge.c       (test file, 864 rows, md5 15a1c2a2)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2h\frozen\diff_footbridge.r3d.c   (the previous test file, md5 6c92d7e5)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2h\frozen\gate_offline.sh         (the script that pins the row counts)
  Measured results: C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbd5\q2_20260923\r3e_20260923\TABLE.txt

Background: DEVICE_ACCESS(footbridge) handles five register accesses that used to end the program; each is now declined
and reported once per site.  The test file includes the device source and calls its access function directly.  Since the
previous version no row was added (864).  Two things changed: (1) in block X14, the rows that make several accesses
(the DEVINIT declines rows and the "re-arm" row) now check five device fields after EACH access, through ZSNAP/ZKEPT,
instead of only at the end -- because a change that toggles a field on every declined write cancelled out over two
batches; (2) blocks X6, X9 and X10 now check, through pad_kept(), that the bytes of the data buffer above the access
width are untouched -- because a real ARM byte or halfword load passes a 1- or 2-byte buffer, so writing back more than
len bytes overflows it.  The comment above the X6 rows (the CONTRACT) lists what the rows cover and what they do not.

Answer VERDICT first (one line), then:

TASK 1.  For change (1), list every X14 row that makes more than one call to the access function, what its name or the
contract says it keeps, and whether that is now checked after every call.  For change (2), list every row that passes
a buffer to the access function with a length below 8, and whether a write-back or a fetch past that length is now
observed.  Name any gap.

TASK 2.  Find the smallest one-line change to dev_footbridge.c's five register cases, the Clear write in the same case
as the declined +0x18c read, the two tests before the switch, or the write-back at the end of the access function, that
changes guest-visible behaviour, host memory safety, or the number of reports while every one of the 864 rows still
passes, and that the contract's NOT COVERED list does not name.  If none, list every change shape and case you checked.

TASK 3.  Check that the row count is still 864 and each pin in gate_offline.sh still matches the loops.

TASK 4.  Quote any comment sentence in the test file, changed since the previous version, that is false about the code
as it is now; and check that every artifact path those changed comments cite exists under
C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbd5\.

End with: files read, and anything you ran.
