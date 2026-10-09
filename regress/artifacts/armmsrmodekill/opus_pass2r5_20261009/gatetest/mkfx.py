"""Build adversarial gate fixtures from the preserved fixed log.  Each is a plausible producer state."""
import io
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fx")
fixed = io.open(os.path.join(D, "fixed.out"), newline="").read()
L = fixed.split("\n")


def w(name, lines):
    io.open(os.path.join(D, name), "w", newline="").write("\n".join(lines))


# 1. CONTROL=DEAD exactly as report_dead() prints it (no REDS line), e.g. `armed' red
dead = ["arm_msrmode_probe -- binary=X label=gate machine=testarm", "ARMMSRMODE_CONTROL=DEAD",
        "ARMMSRMODE_RESULT=0/0",
        "  *** SETUP FAILED (armed) -- the vehicle is not the vehicle.  NOT 'no defect'. ***",
        "  enc ok      got=clean            want=clean            CONTROL=DEAD. Decoder match on th",
        "  live        got=0x2a             want=0x2a             CONTROL=DEAD. Plant, step and dum",
        "  pc adv      got=0x8008           want=0x8008           CONTROL=DEAD. The words were tran",
        "  armed       got=?/?              want=0xd3/0x3fff000   CONTROL=DEAD. SVC32 privileged te",
        "ARMMSRMODE_DONE", ""]
w("dead.out", dead)
# 2. truncated: killed before the completion sentinel
w("trunc.out", [x for x in L if x != "ARMMSRMODE_DONE"])
# 3. an INCONSISTENT producer: one row printed FAIL while RESULT/REDS still say 47/47, none
inc = list(L)
for i, x in enumerate(inc):
    if x.startswith("  kill 14 "):
        inc[i] = x.replace(" ok   ", " FAIL ", 1)
        break
w("inconsistent.out", inc)
# 4. a DUPLICATED row replacing another (count still 47)
dup = list(L)
idx = [i for i, x in enumerate(dup) if x.startswith("  grid msr ")][0]
idx2 = [i for i, x in enumerate(dup) if x.startswith("  grid dpi ")][0]
dup[idx2] = dup[idx]
w("duprow.out", dup)
# 5. RESULT 47/47 but a SESSIONS change (a session silently dropped) -- not checked by the gate
ses = [x.replace("ARMMSRMODE_SESSIONS=43", "ARMMSRMODE_SESSIONS=42") for x in L]
w("sessions42.out", ses)
# 6. two DONE lines (a concatenated log)
w("twodone.out", L + ["ARMMSRMODE_DONE"])
# 7. REDS line present but EMPTY on a 47/47 (producer bug)
w("redsempty.out", [("ARMMSRMODE_REDS=" if x.startswith("ARMMSRMODE_REDS=") else x) for x in L])
print("fixtures:", sorted(os.listdir(D)))
