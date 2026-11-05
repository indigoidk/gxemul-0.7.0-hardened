# D15_dom_ok -- the exact edit

Recorded beside SCORES.txt as ruled P9 (adj_20261104/ADJ_FABLE.md: "Record the exact edit beside the score so a later reader does not
expect ctl to red").  qhs_variants_1b.py replaces the closing line of the slow-path read's failure test in X(to_be_translated):

```
-		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
+		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION) || 1) {
```

So the four-arm block runs whatever the slow-path read returns.  It touches the SLOW path only: RAM fetches take the host-page fast path
and never reach this read, which is why `ctl` stays green under D15.  On the no-T route the read past RAM zero-fills and succeeds, so the
block runs with running 1 and MSR 0 and the checkstop fallback parks at the same pc; only the texts differ, and the two noT rows read them.

Scores (SCORES.txt): base 50/50 on the 50-row probe and 52/52 on the 52-row candidate; D15_dom_ok 50/50 on the 50-row probe (undetected)
and 50/52 on the candidate, red on noT_unimpl and noT_chkstop.
