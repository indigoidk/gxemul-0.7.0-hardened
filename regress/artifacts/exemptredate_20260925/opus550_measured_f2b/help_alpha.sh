cd /tmp/opus550f2b || exit 1
/tmp/opus550/gxemul -H > help.txt 2>&1
echo "-H lines mentioning alphabook1: $(grep -c alphabook1 help.txt)"
grep -n -iE '^ *alpha|alphabook1|"alpha"' help.txt | head -12
