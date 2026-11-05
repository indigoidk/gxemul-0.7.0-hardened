#!/bin/bash
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/pvrrenderexit/sibling_listcmd_20261104
md5sum /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul > $D/MD5.txt
python3 -u $D/listcmd_witness.py /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul > $D/witness_fixedbuild.out 2>&1
cat $D/witness_fixedbuild.out
