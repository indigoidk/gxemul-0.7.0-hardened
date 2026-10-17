# fable5 adj B: header media by EXACT replacement on the composite header; every find-text must occur once.
import hashlib, io, os, sys
BS = chr(92)
W = sys.argv[1]
src = io.open(os.path.join(W, "comp", "dreamcast_sysasicvar.h"), encoding="utf-8", newline="").read()
assert hashlib.md5(src.encode()).hexdigest() == "6b5cc64842911e4566ffff6d400a82c1", "composite header md5"
headsrc = io.open(os.path.join(W, "head", "dreamcast_sysasicvar.h"), encoding="utf-8", newline="").read()
RW = "\tcpu->memory_rw(cpu, cpu->mem, tmp1, buf, 8,\t\t\t" + BS + "\n"
SER = "\tmemory_writemax64(cpu, buf, 8, tmp2);\t\t\t\t" + BS + "\n"
BUF = "\tuint8_t buf[8];\t\t\t\t\t\t\t" + BS + "\n"
FLAGS = "\t    MEM_WRITE, PHYSICAL);"
R1 = "((e) >= 0 && (e) < 96)"
A1 = "4*((e)>>5)"
B1 = "(1 << ((e) & 31))"


def decl(text):
    return "\t" + text + "\t\t\t\t" + BS + "\n"


MED = [
  ("BASE", [], "the composite header (BASE)"),
  ("cand_buf4", [(BUF, BUF.replace("buf[8]", "buf[4]"))], "glm: buf[4] -- must RED under the extent pin"),
  ("cand_buf16", [(BUF, BUF.replace("buf[8]", "buf[16]"))], "a larger object, buf[16] -- must stay GREEN"),
  ("ptr8", [(BUF, decl("uint8_t raw[8], *buf = raw;"))], "pointer refactor of an 8-byte object -- must stay GREEN"),
  ("ptr4", [(BUF, decl("uint8_t raw[4], *buf = raw;"))], "pointer to a 4-byte allocation -- must go RED"),
  ("u64obj", [(BUF, decl("uint64_t raw; unsigned char *buf = (unsigned char *)&raw;"))], "pointer into an 8-byte scalar object -- must stay GREEN"),
  ("cast_uc", [(SER, SER.replace("cpu, buf, 8", "cpu, (unsigned char *)buf, 8")), (RW, RW.replace("tmp1, buf, 8", "tmp1, (unsigned char *)buf, 8"))], "a cast (unsigned char *) at both calls -- must stay GREEN"),
  ("cast_u8", [(SER, SER.replace("cpu, buf, 8", "cpu, (uint8_t *)buf, 8")), (RW, RW.replace("tmp1, buf, 8", "tmp1, (uint8_t *)buf, 8"))], "a cast (uint8_t *) at both calls -- must stay GREEN"),
  ("plus0", [(SER, SER.replace("cpu, buf, 8", "cpu, buf + 0, 8")), (RW, RW.replace("tmp1, buf, 8", "tmp1, buf + 0, 8"))], "buf + 0 at both calls -- must stay GREEN"),
  ("sz8", [(RW, RW.replace("buf, 8,", "buf, (size_t)8,"))], "memory_rw length (size_t)8 -- must stay GREEN"),
  ("cand_rwlen_hex", [(RW, RW.replace("buf, 8,", "buf, 0x100000008,"))], "grok: memory_rw length 0x100000008 -- must RED under pin A"),
  ("static8", [(BUF, BUF.replace("uint8_t buf[8]", "static uint8_t buf[8]"))], "static uint8_t buf[8] -- disclosed; GREEN expected"),
  ("e1noparen", [(R1, "(e >= 0 && (e) < 96)")], "RANGE_OK (e) -> e at the >= 0 site"),
  ("e2noparen", [(R1, "((e) >= 0 && e < 96)")], "RANGE_OK (e) -> e at the < 96 site"),
  ("A_enoparen", [(A1, "4*(e>>5)")], "ADDR (e) -> e at >>5"),
  ("B_enoparen", [(B1, "(1 << (e & 31))")], "BITMASK (e) -> e"),
  ("T54_MEM_WRITE_2", [(FLAGS, "\t    2, PHYSICAL);")], "TRIGGER passes the literal 2 for writeflag"),
]
for name, edits, what in MED:
    t = src
    for old, new in edits:
        assert t.count(old) == 1, (name, old, t.count(old))
        t = t.replace(old, new)
    d = os.path.join(W, "media", name, "thirdparty")
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "dreamcast_sysasicvar.h"), "w", encoding="utf-8", newline="").write(t)
    print("%s\t%s\t%s" % (name, hashlib.md5(t.encode()).hexdigest()[:12], what))
d = os.path.join(W, "media", "HEADH", "thirdparty")
os.makedirs(d, exist_ok=True)
io.open(os.path.join(d, "dreamcast_sysasicvar.h"), "w", encoding="utf-8", newline="").write(headsrc)
print("%s\t%s\t%s" % ("HEADH", hashlib.md5(headsrc.encode()).hexdigest()[:12], "the committed header e483d931 (uncomposited)"))
