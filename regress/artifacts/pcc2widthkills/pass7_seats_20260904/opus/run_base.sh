#!/bin/bash
cd /tmp/p7logs
date +"%T START BASE"
python3 -u /tmp/p7logs/frozen_probe.py /tmp/gxopus_p7/gxemul BASE > /tmp/p7logs/base.out 2>&1
echo "PROBE_RC=$?"
date +"%T END BASE"
tail -4 /tmp/p7logs/base.out
