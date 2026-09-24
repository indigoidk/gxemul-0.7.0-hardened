#!/bin/bash
echo "python3: $(command -v python3) $(python3 -V 2>&1)"
echo "git: $(command -v git 2>&1) $(git --version 2>&1)"
echo "bash: $BASH_VERSION"
echo "grep: $(grep -V | head -1)"; echo "date: $(date --version | head -1)"; echo "sed: $(sed --version | head -1)"
echo "sort: $(sort --version | head -1)"; echo "awk: $(awk --version 2>&1 | head -1)"
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress && git -C . ls-files --error-unmatch lca_badval_probe.py; echo "ls-files rc=$?"
echo "BASH_ENV=[${BASH_ENV:-}]"
