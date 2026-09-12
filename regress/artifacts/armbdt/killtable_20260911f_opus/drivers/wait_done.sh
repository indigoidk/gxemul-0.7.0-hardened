#!/usr/bin/env bash
for i in $(seq 1 120); do
  if [ -f /tmp/opus524_out/SCORES.txt ] && [ "$(grep -c . /tmp/opus524_out/SCORES.txt)" -ge 8 ]; then
      if ! pgrep -f '[t]able_opus.sh' > /dev/null; then echo TABLE_FINISHED; break; fi
  fi
  sleep 5
done
cat /tmp/opus524_out/SCORES.txt
echo "--- sentinel:"; ls -la /tmp/gxopus524c/.MUTANT 2>&1 | head -1
