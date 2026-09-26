#!/usr/bin/env python3
import io, os
SRC = "/tmp/gxopus549/src/devices/dev_fbctrl.c"
O = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/opus549/out/mutants"
os.makedirs(O, exist_ok=True)
base = io.open(SRC, encoding="utf-8", newline="").read()
assert "\r" not in base
T, N, BS = "\t", "\n", chr(92)
NL = BS + "n"   # the two characters backslash-n, to appear inside a C string literal
STRUCT = T + "int" + T + T + "port[DEV_FBCTRL_NPORTS];" + N
i = base.index(T + T + "else {"); j = base.index(T + T + "break;", i)
ELSE = base[i:j]
assert base.count(STRUCT) == 1 and base.count(ELSE) == 1


def build(struct=True, cmp="idata >= DEV_FBCTRL_NPORTS", store="d->current_port = idata;",
          latch_first=True, latch_ever=True, reset0=False, storeanyway=None):
    s = base
    if struct:
        s = s.replace(STRUCT, STRUCT + T + "int" + T + T + "warned_port;" + T + "/* #549 */" + N)
    ann = (T + T + T + 'fatal("[ fbctrl: port number is out of range; the "' + N +
           T + T + T + T + '"selector is unchanged (once) ]' + NL + '");' + N)
    setl = T + T + T + "d->warned_port = 1;" + N
    rst = (T + T + T + "d->current_port = 0;" + N) if reset0 else ""
    if storeanyway is not None:
        blk = (T + T + "d->current_port = " + storeanyway + ";" + N +
               T + T + "if (idata >= DEV_FBCTRL_NPORTS && !d->warned_port) {" + N +
               ann + setl + T + T + "}" + N)
    else:
        if latch_ever:
            body = (ann + setl) if latch_first else (setl + ann)
            inner = T + T + T + "if (!d->warned_port) {" + N + body + rst + T + T + T + "}" + N
        else:
            inner = ann + rst
        blk = (T + T + "else if (" + cmp + ") {" + N + inner + T + T + "} else" + N +
               T + T + T + store + N)
    return s.replace(ELSE, blk)


MUT = {
    "fix": dict(),
    "e_gt": dict(cmp="idata > DEV_FBCTRL_NPORTS"),
    "e_u32": dict(cmp="(uint32_t)idata >= DEV_FBCTRL_NPORTS"),
    "e_int": dict(cmp="(int)idata >= DEV_FBCTRL_NPORTS"),
    "e_latchnever": dict(latch_ever=False),
    "e_setbefore": dict(latch_first=False),
    "e_reset0": dict(reset0=True),
    "e_storeanyway": dict(storeanyway="idata & 7"),
}
for k, kw in MUT.items():
    io.open(os.path.join(O, k + ".c"), "w", encoding="utf-8", newline="").write(build(**kw))
print("wrote:", ", ".join(sorted(os.listdir(O))))
