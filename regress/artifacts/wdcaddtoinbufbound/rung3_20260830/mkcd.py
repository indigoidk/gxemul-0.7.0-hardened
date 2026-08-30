"""Build the CD-ROM image for the wdcaddtoinbufbound rung-3 witness.

The oracle values are POISONED AT KNOWN OFFSETS so that every observed byte
names WHICH byte of the transfer it is.  READ(10) LBA 0, 32 blocks of 2048 =
65536 bytes; dev_wdc clamps chunk 1 to 32768, so chunk 2 begins at image
offset 32768 and is fetched as data_in[atapi_received + j].
"""
import sys

SIZE = 1048576          # 512 CD blocks of 2048; exact multiple, no rounding
FILL = 0x11

img = bytearray([FILL]) * SIZE
img[0]     = 0xC0       # chunk 1, first byte      -- disk-content control
img[32767] = 0xC1       # chunk 1, LAST byte       -- the read that fires the re-arm
img[32768] = 0xC2       # chunk 2, first byte      -- the FIXED-leg oracle
img[32769] = 0xC3       # chunk 2, second byte
img[32770] = 0xC4       # chunk 2, third byte

with open(sys.argv[1], "wb") as f:
    f.write(bytes(img))
print("wrote %s  size=%d  [0]=%02x [32767]=%02x [32768]=%02x [32769]=%02x [32770]=%02x"
      % (sys.argv[1], SIZE, img[0], img[32767], img[32768], img[32769], img[32770]))
