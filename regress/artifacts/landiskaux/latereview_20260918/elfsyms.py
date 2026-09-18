#!/usr/bin/env python3
"""elfsyms.py <elf> <substring>... -- list ELF32 symbols matching substrings (no deps)."""
import struct, sys
data = open(sys.argv[1], "rb").read()
assert data[:4] == b"\x7fELF" and data[4] == 1, "not ELF32"
end = "<" if data[5] == 1 else ">"
(e_shoff,) = struct.unpack_from(end + "I", data, 0x20)
e_shentsize, e_shnum, e_shstrndx = struct.unpack_from(end + "HHH", data, 0x2e)
secs = []
for i in range(e_shnum):
    secs.append(struct.unpack_from(end + "IIIIIIIIII", data, e_shoff + i * e_shentsize))
n_sym = 0
for s in secs:
    if s[1] != 2:          # SHT_SYMTAB
        continue
    strtab = secs[s[6]]
    for off in range(s[4], s[4] + s[5], 16):
        st_name, st_value, st_size, st_info, st_other, st_shndx = struct.unpack_from(end + "IIIBBH", data, off)
        n_sym += 1
        nm = data[strtab[4] + st_name: data.index(b"\0", strtab[4] + st_name)].decode()
        if any(k in nm for k in sys.argv[2:]):
            print("0x%08x size=%-5d %s" % (st_value, st_size, nm))
print("SYMBOLS_SCANNED=%d" % n_sym)
