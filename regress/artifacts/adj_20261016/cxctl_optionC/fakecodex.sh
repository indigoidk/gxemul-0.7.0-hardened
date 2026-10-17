#!/bin/bash
cat "$FX/stdout" 2>/dev/null; cat "$FX/stderr" 1>&2 2>/dev/null; exit $(cat "$FX/rc")
