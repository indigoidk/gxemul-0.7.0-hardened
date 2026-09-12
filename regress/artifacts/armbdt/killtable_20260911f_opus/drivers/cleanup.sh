#!/usr/bin/env bash
#  Remove MY scratch clone.  A clone left holding PRE-FIX source with a matching
#  binary and no sentinel is exactly the trap this review is about to describe.
rm -rf /tmp/gxopus524c
echo "removed /tmp/gxopus524c: $( [ -d /tmp/gxopus524c ] && echo STILL THERE || echo gone )"
echo "main loop's clone untouched: $(ls -ld /tmp/gxarmbdt_clone 2>/dev/null | awk '{print $6,$7,$8}')"
echo "main loop's clone sentinel: $(ls /tmp/gxarmbdt_clone/.MUTANT 2>/dev/null || echo none)"
echo "my processes still alive: $(pgrep -f '[o]pus524' | wc -l)"
