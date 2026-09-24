Read-only review of a C test file and the device model it tests. Do not edit or build anything.

Files (frozen copies; read these, not any other copy of GXemul under the project root):
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2e\frozen\dev_footbridge.c      (device model, md5 783c0c7f)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2e\frozen\diff_footbridge.c     (test file, 862 test rows, md5 0263974b)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2e\frozen\diff_footbridge.707.c (the previous test file, 707 rows)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2e\frozen\gate_offline.sh       (the script that pins the row counts)

Background: DEVICE_ACCESS(footbridge) handles five register accesses that used to end the program (writes to
IRQ_STATUS 0x180, IRQ_RAW_STATUS 0x184, FIQ_STATUS 0x280, FIQ_RAW_STATUS 0x284; a read of IRQ_ENABLE_CLEAR 0x18c).
Each is now declined (no field changes, a declined read returns 0) and reported once per site through a flag field.
The test file includes the device source and calls its access function directly.  The new block X14 builds its own
device instances: the CPU interrupt counted separately from the timer interrupts, optionally the timer reset values
DEVINIT sets, and a device interrupt line raised through the real footbridge_interrupt_assert().  The comment above
the X6 rows (the CONTRACT) lists what the rows cover and what they do not.

Answer VERDICT first (one line), then:

TASK 1.  For each X14 test row, name the device behaviour it checks and a one-line change to dev_footbridge.c that
would make that row fail.  Say whether any X14 row can never fail because the value it checks cannot change.

TASK 2.  Find the smallest one-line change to the five register cases, the two tests before the switch (the idata
read and the timer-range fold), or footbridge_interrupt_assert/deassert, that changes device behaviour a guest can see
or changes how many reports are made, while EVERY one of the 862 rows would still pass, and that is NOT listed under
NOT COVERED in the contract.  Show the changed line and the rows you checked.  If you find none, list the change
shapes and cases you checked.

TASK 3.  Check the arithmetic: the IDENTITY comment says 862 = 707 + 32 + 8 + 8 + 8 + 60 + 20 + 19; gate_offline.sh
pins P 78, X[1-8] 440, X6 248, X7 148, X8 6, X9 100, X10 72, X11 80, X12 20, X13 20, X14 19.  Count the rows each loop
in the test file produces and say whether each number is right.

TASK 4.  Quote any comment sentence in the test file or gate_offline.sh that is false about the code as it is now.

End with: files read, and anything you ran.
