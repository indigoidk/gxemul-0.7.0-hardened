"""#485's kill table.  Seven mutants; five of them ESCAPED the two-observable sweep I first
designed, and each is the reason one leg of the new detector exists."""
import io
import os
import shutil

NL, T = chr(10), chr(9)
SEC = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
BASE = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
        r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad")
DET = os.path.join(BASE, "r485c", "regress", "diff_wdc_identify.c")
OUT = os.path.join(BASE, "m485")

SEC_ARM = T*2 + "d->error |= WDCE_ABRT;" + NL + T*2 + "d->int_assert = 1;" + NL + T*2 + "break;" + NL
DEF_ARM = (T*2 + "d->error |= WDCE_ABRT;" + NL + T*2 + "d->int_assert = 1;" + NL +
           T*2 + "if (!d->warned_unimpl_cmd) {" + NL)


def uniq(t, x, n):
    c = t.count(x)
    assert c == 1, "%s: anchor occurs %d times" % (n, c)


def m1_defonly(t):
    """clause (b) at ONE site: the SEC arm loses its assert."""
    uniq(t, SEC_ARM, "M1")
    return t.replace(SEC_ARM, T*2 + "d->error |= WDCE_ABRT;" + NL + T*2 + "break;" + NL, 1)


def m2_seconly(t):
    """clause (b) at the OTHER site: the default arm loses its assert."""
    uniq(t, DEF_ARM, "M2")
    return t.replace(DEF_ARM, T*2 + "d->error |= WDCE_ABRT;" + NL +
                     T*2 + "if (!d->warned_unimpl_cmd) {" + NL, 1)


def m5_inlatch(t):
    """clause (d): move the default arm's assert INSIDE the latch."""
    uniq(t, DEF_ARM, "M5")
    return t.replace(DEF_ARM,
                     T*2 + "d->error |= WDCE_ABRT;" + NL +
                     T*2 + "if (!d->warned_unimpl_cmd) {" + NL +
                     T*3 + "d->int_assert = 1;" + NL, 1)


def m4_hoist(t):
    """one assert AFTER the switch: 'fixes' all 242 and breaks the three deferrals."""
    t = m1_defonly(t)
    t = m2_seconly(t)
    old = (T*2 + 'fatal("[ wdc: WARNING! Unimplemented command 0x%02x "' + NL)
    uniq(t, old, "M4/anchor")
    #  close the switch and assert unconditionally after it
    tail = NL + T + "}" + NL + "}" + NL
    i = t.index(old)
    j = t.index(tail, i)
    return t[:j] + NL + T + "}" + NL + T + "d->int_assert = 1;" + NL + "}" + NL + t[j + len(tail):]


def m7_noclear(t):
    """the STATUS read stops clearing the request: int_assert is a LEVEL."""
    old = T*3 + "INTERRUPT_DEASSERT(d->irq);" + NL + T*3 + "d->int_assert = 0;" + NL
    uniq(t, old, "M7")
    return t.replace(old, T*3 + "INTERRUPT_DEASSERT(d->irq);" + NL, 1)


def m8_sfabortonly(t):
    """SET_FEATURES asserts only on its ABORT sub-case."""
    old = (T*2 + "default:d->error |= WDCE_ABRT;" + NL + T*2 + "}" + NL +
           T*2 + "/*  TODO: always interrupt?  */" + NL + T*2 + "d->int_assert = 1;" + NL)
    uniq(t, old, "M8")
    return t.replace(old,
                     T*2 + "default:d->error |= WDCE_ABRT;" + NL +
                     T*3 + "d->int_assert = 1;" + NL + T*2 + "}" + NL, 1)


def m9_notailtick(t):
    """delete dev_wdc_access's tail tick: nothing reaches the wire from a command store."""
    old = T + "dev_wdc_tick(cpu, extra);" + NL
    uniq(t, old, "M9")
    return t.replace(old, T + "/*  M9: tail tick deleted  */" + NL, 1)


MUT = [("M1_defonly",    m1_defonly,    "clause (b): the SEC arm loses its assert"),
       ("M2_seconly",    m2_seconly,    "clause (b): the default arm loses its assert"),
       ("M5_inlatch",    m5_inlatch,    "clause (d): assert moved INSIDE the latch"),
       ("M4_hoist",      m4_hoist,      "one assert after the switch -- breaks the 3 deferrals"),
       ("M7_noclear",    m7_noclear,    "STATUS read stops clearing: a stuck LEVEL"),
       ("M8_sfabortonly", m8_sfabortonly, "SET_FEATURES asserts only on its abort sub-case"),
       ("M9_notailtick", m9_notailtick, "dev_wdc_access's tail tick deleted")]

if __name__ == "__main__":
    src = io.open(os.path.join(SEC, "src", "devices", "dev_wdc.c"),
                  encoding="utf-8", newline="").read()
    shutil.rmtree(OUT, ignore_errors=True)
    for name, fn, why in MUT:
        d = os.path.join(OUT, name)
        os.makedirs(os.path.join(d, "regress"))
        os.makedirs(os.path.join(d, "src", "devices"))
        shutil.copy(DET, os.path.join(d, "regress", "diff_wdc_identify.c"))
        try:
            t2 = fn(src)
        except AssertionError as e:
            print("  SKIP  %-15s %s" % (name, e))
            continue
        assert t2 != src, "MUTANT %s CHANGED NOTHING" % name
        io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
                "w", encoding="utf-8", newline="").write(t2)
        print("  built %-15s %s" % (name, why))
