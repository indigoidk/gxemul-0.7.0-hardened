#!/bin/sh
# --- configurable paths (override via env, or edit these defaults) ----------
GXEMUL="${GXEMUL:-../gxemul}"                 # built gxemul binary (./configure && make at the repo root)
DRIVE="${DRIVE:-$(dirname "$0")/drive.py}"    # expect driver (shipped in this folder)
KERNELS="${KERNELS:-./kernels}"               # guest test kernels / images -- PROVIDE YOUR OWN (see TEST_BATTERY.md)
RIGDIR="${RIGDIR:-./rig}"                      # OpenBSD/pmax installed-disk rig: bsd + disk.img -- PROVIDE YOUR OWN
WORK="${WORK:-./out}"; mkdir -p "$WORK"
# ---------------------------------------------------------------------------
# pmax post-boot DEPTH regression: login + uname + NAT ping + DISK write/read path (osiop/SCSI/diskimage)
# + multiuser daemon health. Non-destructive (throwaway disk copy). Retries past long-run death.
GX="$GXEMUL"
RIG="$RIGDIR"
S="$WORK"
DONE="$S/reg_pmax2.done"; LOG="$S/reg_pmax2.log"
cp -f "$RIG/bsd" /tmp/bsd.pmax
rm -f "$DONE"; : > "$LOG"
a=0
while [ $a -lt 3 ]; do
  a=$((a+1))
  echo "=== PMAX2 ATTEMPT $a $(date +%H:%M:%S) ===" >> "$LOG"
  pkill -9 -x gxemul 2>/dev/null; pkill -9 -x python3 2>/dev/null; sleep 2
  cp -f "$RIG/disk.img" /tmp/rz1.test.img
  python3 "$DRIVE" "$LOG" 300 "$GX" -q -e 3max -d 1:/tmp/rz1.test.img /tmp/bsd.pmax <<'EOF'
E:root device
S:rz1\n
E:login:
S:root\n
W:5
S:vt100\n
W:4
S:\n
W:2
S:echo RIG_TOKEN_START; uname -a; id; echo RIG_TOKEN_END\n
W:8
S:echo NIC_START; ifconfig le0 10.0.0.1 netmask 0xffffff00 up; route add default 10.0.0.254; ping -c 3 10.0.0.254; echo NIC_END\n
W:14
S:echo DISK_START; rm -f /var/tmp/gxpb.dat; dd if=/dev/zero of=/var/tmp/gxpb.dat bs=8192 count=128; cksum /var/tmp/gxpb.dat; dd if=/var/tmp/gxpb.dat of=/dev/null bs=8192; sync; cksum /var/tmp/gxpb.dat; echo DISK_END\n
W:12
S:echo DAEMON_START; ps -ax | grep -v grep | egrep 'syslogd|cron|inetd' | wc -l; logger GXPOSTBOOT_MARK; sync; grep GXPOSTBOOT_MARK /var/log/messages | tail -1; echo DAEMON_END\n
W:8
S:sync; sync; halt\n
E:halted
EOF
  if tr '\200-\377' '\000-\177' < "$LOG" | grep -aq DAEMON_END; then
    echo "PMAX2 reached end" > "$DONE"; break
  fi
  echo "  attempt $a incomplete" >> "$LOG"
done
D=$(tr '\200-\377' '\000-\177' < "$LOG")
echo "######## POST-BOOT CHECK RESULTS ########"
echo "root:    $(printf '%s' "$D" | grep -ac 'uid=0(root)')   (uname/id)"
echo "NIC:     $(printf '%s' "$D" | grep -aoE '[0-9]+% packet loss' | tail -1)"
# disk: the two cksum lines for gxpb.dat must match (write+read path exercised, value stable)
ck=$(printf '%s' "$D" | grep -aE 'gxpb\.dat' | grep -aoE '^[0-9]+ [0-9]+' | sort -u)
nck=$(printf '%s' "$ck" | grep -ac '[0-9]')
echo "DISK:    cksum(s) seen=[$ck]  -> $( [ "$nck" = 1 ] && echo 'OK (write+read path, stable cksum)' || echo 'CHECK (mismatch/none)')"
syslogok=$(printf '%s' "$D" | grep -acE 'rig [a-z]+: GXPOSTBOOT_MARK')
if [ "$syslogok" -gt 0 ]; then dstat="ALIVE (logger reached /var/log/messages)"; else dstat="NOT CONFIRMED"; fi
echo "DAEMONS: syslogd $dstat  [ps -ax name-check skipped: needs /bsd namelist]"
echo "halted:  $(printf '%s' "$D" | grep -ac halted)   real-panic/fatal: $(printf '%s' "$D" | grep -aciE 'panic[:! ]|Segmentation fault|fatal error|AddressSanitizer|kernel-mode .*trap|uvm_fault')"
echo "######## RESULT ########"; cat "$DONE"
