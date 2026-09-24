Read-only review of a C test file and the device model it tests. Do not edit or build anything.

Files (frozen copies; read these, not any other copy of GXemul under the project root):
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2f\frozen\dev_footbridge.c      (device model, md5 783c0c7f)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2f\frozen\diff_footbridge.c     (test file, 864 rows, md5 8309c5b7)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2f\frozen\diff_footbridge.862.c (the previous test file, 862 rows)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2f\frozen\gate_offline.sh       (the script that pins the row counts)

Background: DEVICE_ACCESS(footbridge) handles five register accesses that used to end the program; each is now declined
and reported once per site.  The test file includes the device source and calls its access function directly.  Since the
previous version, five rows of block X14 check more (interrupt calls, register fields, read values) and two rows were
added (864 = 862 + 2).  The comment above the X6 rows (the CONTRACT) lists what the rows cover and what they do not; it
now says the interrupt helper functions footbridge_interrupt_assert()/_deassert() are used only to set up test state and
are not themselves tested.

Answer VERDICT first (one line), then:

TASK 1.  For each changed or added X14 row, name a one-line change to dev_footbridge.c's five register cases or the two
tests before the switch that makes that row fail, and say whether any X14 row claims to check something it does not.

TASK 2.  Find the smallest one-line change to those five cases or two tests that changes guest-visible behaviour or the
number of reports while every one of the 864 rows still passes, and that the contract's NOT COVERED list does not name.
If none, list the change shapes and cases you checked.

TASK 3.  Check 864 = 862 + 2 and the pins in gate_offline.sh against the loops.

TASK 4.  Quote any comment sentence in the test file or gate_offline.sh that is false about the code as it is now.

End with: files read, and anything you ran.
