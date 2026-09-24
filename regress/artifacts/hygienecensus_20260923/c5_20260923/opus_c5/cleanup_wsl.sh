#!/bin/bash
rm -rf /tmp/gxc5_* /tmp/gxtok_* /tmp/gxcont_* /tmp/gxq1_*
echo "remaining gxc5 dirs in WSL /tmp: $(ls -d /tmp/gxc5_* 2>/dev/null | wc -l)"; echo CLEANUP_DONE
