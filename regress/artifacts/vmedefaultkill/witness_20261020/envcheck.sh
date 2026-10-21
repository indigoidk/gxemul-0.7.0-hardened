#!/bin/bash
# envcheck.sh -- read-only look at the WSL environment the probe runs in.
echo "DISPLAY=[${DISPLAY:-}] WAYLAND_DISPLAY=[${WAYLAND_DISPLAY:-}]"
echo "xterm: $(command -v xterm || echo NONE)"
echo "python3: $(command -v python3) $(python3 --version 2>&1)"
echo "--- prior 2026-10-09 HEAD binary (informational only):"
ls -la --time-style=full-iso /tmp/gxppcwit/gxemul 2>&1
md5sum /tmp/gxppcwit/gxemul 2>&1
echo "--- dummy file from the earlier run, if any:"
ls -la --time-style=full-iso /tmp/vme_probe_dummy.bin 2>&1
echo "--- my binary:"
ls -la --time-style=full-iso /tmp/gxvme_head_20261020/gxemul
md5sum /tmp/gxvme_head_20261020/gxemul
echo "ENVCHECK_DONE"
