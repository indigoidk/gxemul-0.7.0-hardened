"""Rebuild four representatives of the eleven measured escapes, one per new leg."""
import io
import os
import shutil

NL, T = chr(10), chr(9)
SEC = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
BASE = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
        r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad")
DET = os.path.join(SEC, "regress", "diff_wdc_identify.c")
OUT = os.path.join(BASE, "m11")

SEC_ASSERT = T*2 + "d->error |= WDCE_ABRT;" + NL + T*2 + "d->int_assert = 1;" + NL + T*2 + "break;" + NL
DEF_ASSERT = (T*2 + "d->error |= WDCE_ABRT;" + NL + T*2 + "d->int_assert = 1;" + NL +
              T*2 + "if (!d->warned_unimpl_cmd) {" + NL)


def uniq(t, x, n):
    c = t.count(x)
    assert c == 1, "%s: anchor occurs %d times" % (n, c)


def d1_def_seccnt(t):
    """The `default:` arm guarded on a TASK-FILE field the guarded body reads."""
    uniq(t, DEF_ASSERT, "D1")
    return t.replace(DEF_ASSERT,
                     T*2 + "d->error |= WDCE_ABRT;" + NL +
                     T*2 + "if (d->seccnt == 0)" + NL +
                     T*3 + "d->int_assert = 1;" + NL +
                     T*2 + "if (!d->warned_unimpl_cmd) {" + NL, 1)


def o1_macro_direct(t):
    """Assert the MACRO directly instead of setting the level."""
    uniq(t, SEC_ASSERT, "O1/sec")
    t = t.replace(SEC_ASSERT,
                  T*2 + "d->error |= WDCE_ABRT;" + NL +
                  T*2 + "INTERRUPT_ASSERT(d->irq);" + NL +
                  T*2 + "break;" + NL, 1)
    uniq(t, DEF_ASSERT, "O1/def")
    return t.replace(DEF_ASSERT,
                     T*2 + "d->error |= WDCE_ABRT;" + NL +
                     T*2 + "INTERRUPT_ASSERT(d->irq);" + NL +
                     T*2 + "if (!d->warned_unimpl_cmd) {" + NL, 1)


def o8_tick_edge(t):
    """The tick clears the request after asserting -- an EDGE, not a level."""
    old = T + "if (d->int_assert)" + NL + T*2 + "INTERRUPT_ASSERT(d->irq);" + NL
    uniq(t, old, "O8")
    return t.replace(old,
                     T + "if (d->int_assert) {" + NL +
                     T*2 + "INTERRUPT_ASSERT(d->irq);" + NL +
                     T*2 + "d->int_assert = 0;" + NL +
                     T + "}" + NL, 1)


def o4_abrt_deleted(t):
    """Delete the WDCE_ABRT from the SEC arm -- the half the fix did NOT add."""
    uniq(t, SEC_ASSERT, "O4")
    return t.replace(SEC_ASSERT,
                     T*2 + "d->int_assert = 1;" + NL + T*2 + "break;" + NL, 1)


MUT = [("D1_def_seccnt", d1_def_seccnt, "default arm guarded on seccnt -> ROW F"),
       ("O1_macro_direct", o1_macro_direct, "assert the macro, not the level -> ROW D"),
       ("O8_tick_edge", o8_tick_edge, "tick clears after asserting -> ROW D"),
       ("O4_abrt_deleted", o4_abrt_deleted, "WDCE_ABRT deleted from the SEC arm -> ROW E")]

if __name__ == "__main__":
    src = io.open(os.path.join(SEC, "src", "devices", "dev_wdc.c"),
                  encoding="utf-8", newline="").read()
    shutil.rmtree(OUT, ignore_errors=True)
    for name, fn, why in MUT:
        d = os.path.join(OUT, name)
        os.makedirs(os.path.join(d, "regress"))
        os.makedirs(os.path.join(d, "src", "devices"))
        shutil.copy(DET, os.path.join(d, "regress", "diff_wdc_identify.c"))
        t2 = fn(src)
        assert t2 != src, "MUTANT %s CHANGED NOTHING" % name
        io.open(os.path.join(d, "src", "devices", "dev_wdc.c"),
                "w", encoding="utf-8", newline="").write(t2)
        print("  built %-16s %s" % (name, why))
