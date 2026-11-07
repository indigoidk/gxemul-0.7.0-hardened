#!/usr/bin/env python3
"""STUB stand-in for regress/wdc_latch_census.py -- killdrivercrash witness 3 (killrow5c.sh's scorer).
Tests NOTHING in dev_wdc.c.  It prints the census tool's four end tokens (WDC_LATCH_SET/READ/BALANCED/
DECL, which HEAD's tool prints LAST), choosing each run's ending by the input file's basename:
  base.c / surv.c   6/6/6/11 -- the WANT value (a green baseline; a GENUINE survivor)
  kill.c            5/6/5/11 -- a GENUINE kill
  crash.c           raises before printing anything (a traceback on stderr, exit 1)
  crashlate.c       prints SET and READ, then raises: the run is TRUNCATED
"""
import os
import sys

b = os.path.basename(sys.argv[1])
if b == "crash.c":
    raise RuntimeError("stub census crash before any output")
vals = {"base.c": (6, 6, 6, 11), "surv.c": (6, 6, 6, 11), "kill.c": (5, 6, 5, 11),
        "crashlate.c": (6, 6, 6, 11)}[b]
print("WDC_LATCH_FILE=OK")
print("WDC_LATCH_SET=%d" % vals[0])
print("WDC_LATCH_READ=%d" % vals[1])
sys.stdout.flush()
if b == "crashlate.c":
    raise RuntimeError("stub census crash after two of four tokens")
print("WDC_LATCH_BALANCED=%d" % vals[2])
print("WDC_LATCH_DECL=%d" % vals[3])
