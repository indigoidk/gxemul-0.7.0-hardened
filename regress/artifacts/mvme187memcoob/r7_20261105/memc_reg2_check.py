#!/usr/bin/env python3
"""memc_reg2_check.py -- MODEL-ONLY checks for regress_20261105/REG2_MYTHOS_local.md items B and C (no measurement; memc_variants_5.py's
device model, used read-only, on the 213-row instrument table6/probe213_frozen.py).

B. Family (2)'s clause "or which lands on a set latch".  A latch toggle (`^= idata`, `^= 1`) LANDS ON A SET LATCH when it fires
   with the latch truthy and leaves it truthy.  It RELIES on that landing for its survival when the probe observes the latch after
   such a landing -- tested by a counterfactual device that makes every such landing CLEAR the latch instead: if any row then
   reds, the landing was load-bearing.  Run over every PRETABLE_5 UNOBSERVED cell (representatives and members) that the model
   keeps green on the 213 rows, and separately over the UNOBSERVED representatives table 6 MEASURED green.
C. Family (6)'s exclusion.  For each NOCHANGE group (PRETABLE_5 groups NOCHANGE cells by statement), the model's verdict on the 213
   rows for every member: red / green, and whether a green member has the repair path's own shape (memc_members_213.py's test).
Usage: python3 -I memc_reg2_check.py > REG2_CHECK.txt
"""
import importlib.util
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(HERE)
P213 = os.path.join(HERE, "table6", "probe213_frozen.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mv5 = load("mv5", os.path.join(MD, "r5_20261105", "memc_variants_5.py"))
mem = load("mem213", os.path.join(HERE, "memc_members_213.py"))
BaseDevice = mv5.Device
TOGGLES = ("xori", "xor1")


class CountDevice(BaseDevice):
    """The model as written, counting set-latch landings of the cell's toggle."""
    landings = 0

    def hook(self, P, env):
        c = self.cell
        if c is not None and c.shape == "L" and c.op in TOGGLES and c.P == P and self._fire(env):
            cur = self.M if c.T == "M" else self.D
            new = (cur ^ (1 if c.op == "xor1" else env[4])) & 0xffffffff
            if bool(cur) and bool(new):
                CountDevice.landings += 1
        BaseDevice.hook(self, P, env)


class CFDevice(BaseDevice):
    """Counterfactual: a toggle that lands on a set latch CLEARS it instead (every other statement as written)."""

    def hook(self, P, env):
        c = self.cell
        if c is not None and c.shape == "L" and c.op in TOGGLES and c.P == P and self._fire(env):
            cur = self.M if c.T == "M" else self.D
            new = (cur ^ (1 if c.op == "xor1" else env[4])) & 0xffffffff
            if bool(cur) and bool(new):
                self.devs.append(self.n)
                if c.T == "M":
                    self.M = 0
                else:
                    self.D = 0
                return
        BaseDevice.hook(self, P, env)


def red213(cell, dev):
    mv5.Device = dev
    try:
        return mv5.predict({"cell": cell}, P213)[0]
    finally:
        mv5.Device = BaseDevice


def main():
    w = mv5.walk()
    kind, rep_of = {}, {}
    groups = []
    for (sk, devs), members in w.green_groups.items():
        rep = sorted(members, key=mv5.cell_rank)[0]
        k = "UNFIRED" if not devs else ("UNOBSERVED" if w.changed_of[rep.key()] else "NOCHANGE")
        groups.append((k, rep, members))
        for c in members:
            kind[c.key()] = k
            rep_of[c.key()] = rep
    # NOCHANGE groups are per statement (memc_variants_5.py, Walk): merge the (statement, deviation set) groups
    noch = {}
    for k, rep, members in groups:
        if k == "NOCHANGE":
            noch.setdefault(mv5.stmt_key(rep), []).extend(members)
    s6 = {}
    for line in io.open(os.path.join(HERE, "table6", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        s6[p[0]] = p[3]
    out = ["REG2_CHECK -- MODEL ONLY (memc_variants_5.py's device on table6/probe213_frozen.py); table 6's SCORES.txt is read only to",
           "pick the representatives it measured green.", ""]
    # ---------------------------------------------------------------- B
    unobs = [c for k, rep, ms in groups if k == "UNOBSERVED" for c in ms]
    cand = [c for c in unobs if c.shape == "L" and c.op in TOGGLES]
    green_cand = [c for c in cand if not red213(c, BaseDevice)]
    out.append("B. UNOBSERVED cells (PRETABLE_5 class): %d; latch toggles among them: %d; toggles the model keeps green on 213 rows: %d"
               % (len(unobs), len(cand), len(green_cand)))
    land, rely = [], []
    for c in sorted(green_cand, key=mv5.cell_rank):
        CountDevice.landings = 0
        assert not red213(c, CountDevice)
        n = CountDevice.landings
        if n:
            land.append((c, n))
            r = red213(c, CFDevice)
            if r:
                rely.append((c, r))
    reps_green = [c for c in green_cand if rep_of[c.key()] is c and s6.get(c.name()) == "213/213"]
    out.append("   with at least one set-latch landing on the 213 rows: %d" % len(land))
    out.append("   whose landing the probe OBSERVES (counterfactual clear reds a row) -- they rely on the clause: %d" % len(rely))
    for c, r in rely:
        out.append("      %-30s rep %-30s %-10s cf red: %s" % (c.name(), rep_of[c.key()].name(),
                                                           "REP" if rep_of[c.key()] is c else "member", ",".join(r)))
    rr = [c for c, r in rely if rep_of[c.key()] is c]
    out.append("   UNOBSERVED REPRESENTATIVES that table 6 MEASURED green and are toggles: %d; of those relying on the clause (model): %d"
               % (len(reps_green), len([c for c in rr if c in reps_green])))
    out.append("   toggles with landings that the probe does not observe (counterfactual stays green): %d" % (len(land) - len(rely)))
    for c, n in land:
        if all(c is not x for x, _ in rely):
            out.append("      %-30s %-10s landings %d" % (c.name(), "REP" if rep_of[c.key()] is c else "member", n))
    out.append("")
    # ---------------------------------------------------------------- C
    red6 = [n for n, sc in s6.items() if sc != "213/213"]
    tot_r = tot_g = 0
    rows = []
    for sk, members in sorted(noch.items(), key=lambda kv: mv5.stmt_name(kv[0])):
        rep = sorted(members, key=mv5.cell_rank)[0]
        r = [c for c in members if red213(c, BaseDevice)]
        g = [c for c in members if c not in r]
        own_g = [c for c in g if mem.own_shape(c)]
        own_r = [c for c in r if mem.own_shape(c)]
        tot_r += len(r)
        tot_g += len(g)
        rows.append((rep, members, r, g, own_r, own_g))
    out.append("C. NOCHANGE groups (one per statement): %d; cells %d; model red on 213 rows %d, green %d" %
               (len(rows), tot_r + tot_g, tot_r, tot_g))
    redrep = [x for x in rows if x[0].name() in red6]
    out.append("   groups whose representative table 6 MEASURED red: %d (cells %d: model red %d, green %d; own-shape red %d, own-shape green %d)"
               % (len(redrep), sum(len(x[1]) for x in redrep), sum(len(x[2]) for x in redrep), sum(len(x[3]) for x in redrep),
                  sum(len(x[4]) for x in redrep), sum(len(x[5]) for x in redrep)))
    for rep, members, r, g, own_r, own_g in redrep:
        out.append("      %-26s members %3d  model red %3d (own-shape %2d)  green %3d (own-shape %d)%s" %
                   (rep.name(), len(members), len(r), len(own_r), len(g), len(own_g),
                    ("  e.g. green: " + ", ".join(c.name() for c in g[:3])) if g else ""))
    greenrep = [x for x in rows if x[0].name() not in red6]
    out.append("   groups whose representative table 6 MEASURED green: %d (cells %d: model red %d, green %d; own-shape green %d)"
               % (len(greenrep), sum(len(x[1]) for x in greenrep), sum(len(x[2]) for x in greenrep), sum(len(x[3]) for x in greenrep),
                  sum(len(x[5]) for x in greenrep)))
    for rep, members, r, g, own_r, own_g in greenrep:
        if r:
            out.append("      %-26s members %3d  model red %3d  e.g. %s" % (rep.name(), len(members), len(r), r[0].name()))
    out.append("REG2_CHECK_DONE")
    print("\n".join(out))


if __name__ == "__main__":
    main()
