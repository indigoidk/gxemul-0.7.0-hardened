# sgireunmapped -- RUNG-3 WITNESS (opus5 seat, 2026-08-30/31)

binary  : build/gxemul, two-part clearance RUN not asserted
          PART1 cmp vs SEC CLEAN ; PART2 binary -nt source YES ; no sentinel
machine : -E sgi -e ip32   UNMODIFIED in-tree machine description
          SGI-IP32 (O2), R10000, 128 MB, big-endian
probe   : sgi_re_unmapped_probe.py  (built on _scratchpad/gxprobe.py)
score   : 32/32

Every access is a GENUINE GUEST INSTRUCTION executed by `step'.  `put w' writes
only scratch RAM (instruction stubs); the device is never touched by `put d',
which the carrier forbids as laundering.

## CONTROLS
  live ram        guest sw/lw round-trip 0xdeadbeef in RAM        ok
  endian          big                                            ok
  devsig lina     4-byte store to MAPPED 0x1700 -> #497 width
                  decline, text only this device emits            ok
  lina survives   a declined access must NOT kill                 ok
  devsig destat   sibling de_status returns 0x1e000000
                  (CRIME_DE_IDLE|SETUP|PIXPIPE|MTE) -- RAM cannot ok
  enc sb/sw/sd/lw/ld   hand-assembled encodings checked against
                  the debugger's own unassemble                   ok
  NEGATIVE: sw to MAPPED 0x16dc (TEX) -- host alive, catch-all
            NOT reported                                          ok

## THE DEFECT -- host exit status taken with wait_exit() before close()
  width enumerated, not argued (the six window arms accept ONLY len==8):
    w1800b  len=1 write  -> exit 1   "unimplemented write to address 0x1800"
    w1800w  len=4 write  -> exit 1
    w1800d  len=8 write  -> exit 1
    r1800w  len=4 read   -> exit 1   "unimplemented read from address 0x1800"
    r1800d  len=8 read   -> exit 1
  both address runs reachable:
    w16e0d  0x16e0 -> exit 1     w16f8d 0x16f8 -> exit 1
    r16fcw  0x16fc -> exit 1     (the 32-byte CLIP_IDS run)
    w1ff8d  0x1ff8 -> exit 1     w1fffb 0x1fff len=1 -> exit 1

  So: NO width predicate and NO direction predicate, both MEASURED
  rather than read off the source.

## ONE ROW WAS MIS-CUT AND THAT IS A RESULT, NOT NOISE
  An early row read `lw' from 0x16ff and the host SURVIVED.  The log says
  `[ exception ADEL vaddr=0xffffffffb50016ff ]' -- an unaligned word load is
  refused by the CPU WITHOUT calling memory_rw, exactly as the two LINEAR
  site comments describe.  The row was re-cut to 0x16fc and kills.
  Carrier case 3: the row was rejected before its guard was reached.

## INDEPENDENT ATTRIBUTION, not designed for
  The debugger's own disassembly line resolves the target for us:
    [0xffffffffb5001800 = (sgi_re@0x15001000)+0x800]
  so the address is attributed to this device by the emulator itself.
