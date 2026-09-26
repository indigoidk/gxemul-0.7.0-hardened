#!/bin/bash
W=/tmp/opus551p1
grep -E 'error' $W/dev/pristine/regress/Abad.O2.cc | sed 's|.*/||' | cut -c1-120
echo ---- Tdrop k=22 vs ORIG k=22
diff $W/force/ORIGF.22.log $W/force/TdropF.22.log
echo ---- Tdouble k=22 vs ORIG k=22
diff $W/force/ORIGF.22.log $W/force/TdoubleF.22.log
echo ---- E_rows_h srstbit: FAIL lines and summary
grep -E '^  FAIL|rows,|WDC_|SELFCHECK' $W/dev/srstbit/regress/E_rows_h.O2.log
echo ---- ORIG srstbit summary
grep -E 'rows,|WDC_' $W/dev/srstbit/regress/ORIG.O2.log
echo ---- E_eq1 cyl13 vs ORIG cyl13
diff $W/dev/cyl13/regress/ORIG.O2.log $W/dev/cyl13/regress/E_eq1.O2.log
echo ---- E_noret rev255 FAIL/ok lines for SLAVE/base_drive
grep -E 'SLAVE|base_drive' $W/dev/rev255/regress/E_noret.O2.log
echo ---- A diff pristine O2
diff $W/dev/pristine/regress/ORIG.O2.log $W/dev/pristine/regress/A.O2.log
diff $W/dev/pristine/regress/ORIG.O2.log $W/dev/pristine/regress/Ahard.O2.log
