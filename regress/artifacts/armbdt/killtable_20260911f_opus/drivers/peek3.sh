#!/usr/bin/env bash
for f in /tmp/opus524_out/ldmdb_*.out; do echo "### $f"; cat "$f"; done
