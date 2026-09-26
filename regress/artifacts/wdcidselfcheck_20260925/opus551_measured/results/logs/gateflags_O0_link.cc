/usr/x86_64-pc-linux-gnu/binutils-bin/2.46.0/ld: /tmp/ccZKP2JE.o: warning: relocation against `quiet_mode' in read-only section `.text.dev_wdc_access'
/usr/x86_64-pc-linux-gnu/binutils-bin/2.46.0/ld: /tmp/ccZKP2JE.o: in function `wdc_command':
smoke.c:(.text.wdc_command+0x28e): undefined reference to `quiet_mode'
/usr/x86_64-pc-linux-gnu/binutils-bin/2.46.0/ld: smoke.c:(.text.wdc_command+0x30e): undefined reference to `quiet_mode'
/usr/x86_64-pc-linux-gnu/binutils-bin/2.46.0/ld: /tmp/ccZKP2JE.o: in function `dev_wdc_access':
smoke.c:(.text.dev_wdc_access+0x1818): undefined reference to `quiet_mode'
/usr/x86_64-pc-linux-gnu/binutils-bin/2.46.0/ld: warning: creating DT_TEXTREL in a PIE
collect2: error: ld returned 1 exit status
