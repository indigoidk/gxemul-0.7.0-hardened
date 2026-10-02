#!/usr/bin/env python3
"""mutate7.py NAME SRC DST -- #529 closing pass 7, Opus seat (measuring).  Each find-text must occur EXACTLY ONCE (a
missing find-text is a FAIL, so every mutant also pins the presence of what it edits).

K*: the accept guard GROWN by a conjunct keyed on the LATCH STATE at ONE cell -- RA3's d->warned-keyed shrink, but
    cell-keyed (table 10 built only the label-free W_8r / W_8w).  Once any refusal has set CRIME_W_LEN, that cell falls
    into the decline arm, which is SILENT because the latch is set.  Latch x5's prologue (latch clear) accepts it, so
    `latch said' cannot see it; the value rows all sit in refusal-free sessions, so they cannot either.
E*: SILENT bypasses at the cells item 6 calls EQUIVALENT, to check that claim.
"""
import io, sys

LEN8 = "\tif (len == 8) {\n"
LEN4 = "\t} else if (len == 4) {\n"
LATCHED = "(d->warned & CRIME_W_LEN)"
INWIN = "((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100"


def bypass(cond):
    return [(LEN8, "\tif (%s)\n\t\tgoto crime_declined;\n\n" % cond + LEN8)]


M = {
    "base": [],
    # K1: INTMASK 4W declined once latched (a guest sw to INTMASK after any narrow CRIME access does not land)
    "K1_w_imask4w": [(LEN4, "\t} else if (len == 4 && !(writeflag == MEM_WRITE && relative_addr == CRIME_INTMASK && "
                            + LATCHED + ")) {\n")],
    # K2: REV 4-byte declined once latched (the PROM-probe window's lw no longer redirects after any narrow access)
    "K2_w_rev4": [(LEN4, "\t} else if (len == 4 && !(relative_addr == CRIME_REV && " + LATCHED + ")) {\n")],
    # K3: CONTROL 8R declined once latched (an ld of CONTROL answers 0, not 0x100, after any narrow access)
    "K3_w_ctl8r": [(LEN8, "\tif (len == 8 && !(writeflag == MEM_READ && relative_addr == CRIME_CONTROL && "
                          + LATCHED + ")) {\n")],
    # E1: silent bypass, CONTROL 4R (item 6: EQUIVALENT, "reads 0 either way")
    "E1_byp_ctl4r": bypass("len == 4 && writeflag == MEM_READ && relative_addr == CRIME_CONTROL"),
    # E2: silent bypass, TIME 4W and 4R (item 6: EQUIVALENT, "the high half is 0; updates accumulate")
    "E2_byp_time4": bypass("len == 4 && relative_addr == CRIME_TIME"),
    # E3: silent bypass, REV 8W/4W/4R OUTSIDE the PROM window (item 6: EQUIVALENT, "the prelude rewrites REV; its high
    #     half is 0"), plus the default-arm 4W at +0x04 (REV's low lane; ACCEPTS' `sw 0x04', named by no item-6 clause)
    "E3_byp_revout": bypass("((relative_addr == CRIME_REV && !(len == 8 && writeflag == MEM_READ) && !(" + INWIN
                            + ")) || (len == 4 && writeflag == MEM_WRITE && relative_addr == 4))"),
    # ---- added mid-pass at the coordinator's request (the pass-7 panel's silent-form disputes) ----
    # F1 (glm, codex): silent bypass of an accepted CONTROL 8W carrying DOG set + leftover (0x0201) -- value x cell
    "F1_byp_ctl8w_0201": bypass("len == 8 && writeflag == MEM_WRITE && relative_addr == CRIME_CONTROL && idata == 0x0201"),
    # F1b: its 4-byte twin (sw 0x0201 at +0x08)
    "F1b_byp_ctl4w_0201": bypass("len == 4 && writeflag == MEM_WRITE && relative_addr == CRIME_CONTROL && idata == 0x0201"),
    # F3 (kimi CLI vs codex): silent bypass of the default-arm 4W at +0x04 alone
    "F3_byp_sw04": bypass("len == 4 && writeflag == MEM_WRITE && relative_addr == 4"),
    # F4a (deepseek): silent bypass of INTMASK 4R; F4b (kimi-k3): INTSTAT 4R -- controls predicted KILLED
    "F4a_byp_imask4r": bypass("len == 4 && writeflag == MEM_READ && relative_addr == CRIME_INTMASK"),
    "F4b_byp_istat4r": bypass("len == 4 && writeflag == MEM_READ && relative_addr == CRIME_INTSTAT"),
    # E3b: E3 restricted to the ACCEPT widths (E3 also bypassed the refused 1-byte free-running lb +0x00 -- mis-built)
    "E3b_byp_revout_acc": bypass("relative_addr == CRIME_REV && (len == 4 || (len == 8 && writeflag == MEM_WRITE)) && !("
                                 + INWIN + ")"),
}

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M)); sys.exit(0)
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    s = io.open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n)); sys.exit(2)
        s = s.replace(find, repl, 1)
    io.open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
