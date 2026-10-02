#!/usr/bin/env python3
"""predict46.py -- the Opus seat's READING, written BEFORE any measurement run (this file's mtime and PREDICT46.out's
are the order proof).  For each of the 46 ACCEPTS entries of crime_width_probe.r17.py (2fe7123b) and each latch
state (C = `d->warned & CRIME_W_LEN' clear at the access, S = set), the rows of the 226-row probe predicted to go
RED under a SILENT decline of exactly that access kind -- the access sent to `crime_declined' with no announce and
the latch untouched (the G6 bypass form with the latch clear; the K form, which is necessarily silent, with it set).

UNIT: an entry is (width, direction, CRIME offset); for offset 0 also the PROM-window flag (the `P' kinds); for a
CONTROL (+0x08) write also the stored value.  Every probe access of that kind in that latch state is declined.
Rows marked [C] below are CONTROL rows (they also turn CRIMEP_CONTROL to FAIL).  Writes: python3 predict46.py > PREDICT46.out"""

P = {
    1: ([], []),
    2: (["acc8 near"], ["p rev ld"]),
    3: ([], []),
    4: ([], []),
    5: (["rev pc ctl"], ["p revP lw pc"]),
    6: (["revP sw pc"], ["p revP sw pc"]),
    7: (["revP sd pc"], ["p revP sd pc"]),
    8: ([], []),
    9: (["acc ctl ld"], ["p acc ctl ld"]),
    10: (["ctldog sw msg", "latch ctl msg"], ["rearm ctl msg", "p acc ctl msg"]),
    11: (["sw08 msg ctl", "ctlrst sw msg", "latch ctl msg", "rst 4w msg"], ["rearm ctl msg", "p acc ctl msg"]),
    12: ([], []),
    13: ([], []),
    14: (["ctldog sd msg", "latch ctl msg"], ["rearm ctl msg", "p acc ctl msg"]),
    15: (["ctlrst sd msg", "latch ctl msg", "acc ctl sd", "rst 8w msg"], ["rearm ctl msg", "p acc ctl msg"]),
    16: ([], []),
    17: ([], []),
    18: (["istw sd"], ["p istw sd"]),
    19: (["acc istat ld"], ["p acc istat ld"]),
    20: (["istw sw"], ["p istw sw"]),
    21: (["acc istat lw"], ["istat ctl", "p acc istat lw"]),
    22: (["imask ctl", "imask keeps", "istat ctl", "gate line", "istw sd", "istw sw"],
         ["p istw sd", "p istw sw", "p imask st+ld"]),
    23: (["acc imask sw"], ["imask keeps", "p acc imask sw", "p imask st+ld"]),
    24: (["acc imask sw"], ["p acc imask sw"]),
    25: (["gate line"], ["imask ctl"]),
    26: (["acc8 st+ld", "acc4 rhi", "acc4 rlo", "acc4 wlo", "sb keeps", "sh keeps"],
         ["p dog st+ld", "p dog rhi", "p dog rlo", "p dog wlo"]),
    27: (["acc8 st+ld", "acc4 wlo", "acc4 whi"], ["sb keeps", "sh keeps", "p dog st+ld", "p dog wlo", "p dog whi"]),
    28: (["acc4 whi"], ["p dog whi"]),
    29: (["acc4 rhi"], ["p dog rhi"]),
    30: (["acc time sd"], ["p acc time sd"]),
    31: (["acc time sd", "c t4w gap", "c t4r gap"],
         ["time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl", "tl lb ctl", "tl sb ctl", "tl lh ctl",
          "tl sh ctl", "p acc time sd", "p t4w gap", "p t4r gap"]),
    32: (["c t4w gap"], ["p t4w gap"]),
    33: (["c t4r gap"], ["p t4r gap"]),
    34: ([], ["lo keeps"]),
    35: (["acc 40 sw"], ["lo keeps", "p acc 40 sw"]),
    36: (["acc 40 lw", "acc 40 sw"], ["p acc 40 lw", "p acc 40 sw"]),
    37: (["acc 40 lw"], ["p acc 40 lw"]),
    38: (["acc4 wlo", "acc4 whi"], ["p dog wlo", "p dog whi"]),
    39: (["acc4 rlo"], ["p dog rlo"]),
    40: ([], []),
    41: (["devsig", "dflt ctl"], ["p rev lw4"]),
    42: (["revP ld pc"], ["p revP ld pc"]),
    43: ([], []),
    44: ([], []),
    45: (["top8 clear", "top8 st+ld", "top4 rhi", "top4 rlo", "hi keeps"], ["p top st+ld"]),
    46: (["top8 clear"], ["top8 st+ld", "top4 w", "hi keeps", "p top st+ld"]),
}
CONTROL_ROWS = {"live", "devsig", "devsig hi", "dflt ctl", "rev pc ctl", "sw08 halts", "gate hardint", "gate line",
                "sw08 msg ctl", "imask pre", "imask ctl", "istat pre", "istat ctl", "time lb ctl", "time sb ctl",
                "time lh ctl", "time sh ctl", "tl lb ctl", "tl sb ctl", "tl lh ctl", "tl sh ctl"}

if __name__ == "__main__":
    assert sorted(P) == list(range(1, 47))
    print("PREDICT46 -- written before any run.  entry: C-rows | S-rows   ([C] = a CONTROL row)")
    for k in range(1, 47):
        c, s = P[k]
        f = lambda l: ", ".join(x + (" [C]" if x in CONTROL_ROWS else "") for x in l) or "-"
        print("%2d  C: %s" % (k, f(c)))
        print("    S: %s" % f(s))
    print("PREDICT46_DONE")
