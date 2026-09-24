#!/bin/bash
rm -rf /tmp/gxc4_q1wsl /tmp/gxc4_nl_* /tmp/gxc4_k16_* /tmp/gxc4_q2_* /tmp/gxc2_s4_* /tmp/gxc3_s4b_* /tmp/gxtok_* /tmp/gxcont_* /tmp/gxq1_*
ls -d /tmp/gxc4_* 2>/dev/null | wc -l | sed 's/^/remaining gxc4 dirs in WSL \/tmp: /'
echo CLEANUP_DONE
