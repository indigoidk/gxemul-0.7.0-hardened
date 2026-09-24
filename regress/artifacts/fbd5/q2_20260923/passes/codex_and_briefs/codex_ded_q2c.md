Read-only code review task (C, GXemul hardened fork).  Do NOT edit, build or run anything.

Tree: C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2c\frozen\ -- read ONLY these frozen copies:
  dev_footbridge.c (md5 783c0c7f; the device model, function dev_footbridge_access -- written DEVICE_ACCESS(footbridge)),
  diff_footbridge.c (md5 4d7bdcc3; an offline test harness that #includes dev_footbridge.c and checks 707 rows),
  diff_footbridge.491.c (md5 ff8f87b6; the same harness one revision earlier, 491 rows),
  gate_offline.sh (md5 45d2b495; the gate that runs the harness and pins its row counts).
Ignore every other copy of GXemul under C:\DocumentNoSnc\cc\GXEMUL (./src/ and _archive/ are upstream 2021).

Background, one paragraph: five register arms of the access function -- writes to IRQ_STATUS, IRQ_RAW_STATUS,
FIQ_STATUS, FIQ_RAW_STATUS and the read of IRQ_ENABLE_CLEAR -- are "declined": no field changes, a declined read
returns 0, and each site reports once through its own warn-once flag (warned_*).  The newest harness revision added
rows X10 (every legal access with every warn-once flag already set: value and effect), X11 (each ordered pair of
sites: flag j set, then site i's first bad access reports once), X12 (the legal IRQ Clear write at widths 1 and 2
with data 0x70, and at widths 1, 2 and 4 with all-ones data), and a fourth field state "ones" (every bit of every
field set).  It also rewrote the CONTRACT comment above the X6 rows: THE SPACE (the inputs of the five arms), what
is COVERED, and what is NOT COVERED.  Measured today: the unchanged device passes 707/707.

TASK 1 -- read the CONTRACT comment in diff_footbridge.c and the access function.  (a) Is every input of the five
arms, and every condition their code TESTS, named in THE SPACE?  Include the two tests at the top of the function
(the write-data fetch and the timer-range fold) and say what each can change for the five arms' addresses
(0x180, 0x184, 0x18c, 0x280, 0x284) -- work out `address & ~0x060` for each.  (b) For each COVERED class, name the
row family that tests it and say whether those rows compare something that would actually differ if the class's
behaviour were wrong (a row that cannot see the difference does not test the class).  (c) For each NOT COVERED
item, say whether it is a behaviour of the five arms that a one-line code change could break while every row stays
green, and whether the comment's reason for leaving it out is true.

TASK 2 -- arithmetic, by enumeration from the loops: the IDENTITY row expects 707; the gate pins distinct green row
names per family (P 78; X1-X8 400; X6 216; X7 140; X8 6; X9 92; X10 64; X11 20; X12 20).  Derive each number from
the loop bounds and the state/width/data arrays, and say whether any row NAME can repeat (the gate counts DISTINCT
names, so a repeated name would make a pin undercount).

TASK 3 -- quote any comment sentence in diff_footbridge.c's X8, X9, X10-X12 or CONTRACT comments, or in
gate_offline.sh's footbridge comment, that the code or the rows contradict, with the file line.

TASK 4 -- name at least one question about this change that the tasks above did not ask.

Answer format: start with one line `VERDICT: <one sentence>`, then TASKS 1-4.  No "no findings" without the
denominator you checked.  End with what you read.
