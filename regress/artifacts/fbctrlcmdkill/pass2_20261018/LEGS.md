**The shipped probe's two legs, one instrument** (`pass2_20261018/legs/LEGS.out`, 23:17:48; the probe run is the frozen
copy inlined in section 2, md5 `5d90c732...`; each leg first checked its tree held the named `dev_fbctrl.c`, carried no
sentinel, and had a binary newer than that source):

```
HEAD (/tmp/gx566, HEAD's dev_fbctrl.c; binary md5 25ac428c6592): rc=1 FBCMD_RESULT=36/95 FBCMD_CONTROL=OK last=FBCMD_DONE
FIX  (/tmp/gx567, the fix;            binary md5 004caa290db2): rc=0 FBCMD_RESULT=95/95 FBCMD_CONTROL=OK last=FBCMD_DONE
```

36/95 is the count the PRETABLE predicted for the pre-fix leg, and the draft instrument measured the same before the
`_mark` rename (`draft_20261018/PROBE95_prefix.out`, `PROBE95_postfix.out`).  The witness: 2/12 on HEAD, 12/12 on the fix.
