# opus5 seat -- `sgireunmapped` pass 1

## 1. THE ENUMERATION: CONFIRMED, and the brief is exactly right
Walked all 4096 addresses in a C program that `#include`s the REAL
`src/include/thirdparty/crmfbreg.h` (constants compiled, not transcribed) using
the six window predicates copy-pasted from the source:

    TLB_A 512  TLB_B 512  TLB_C 512  TEX 224  LIN_A 128  LIN_B 128
    KILL  2080   in exactly TWO contiguous runs
      0x16e0-0x16ff    32
      0x1800-0x1fff  2048
    sum 4096  (the denominator closes)

`0xb5001800 -> relative 0x1800 -> FALLS TO THE KILL`: confirmed.
Domain confirmed from the registration itself: `baseaddr + 0x1000`,
`DEV_SGI_RE_LENGTH 0x1000`, handler does `relative_addr += 0x1000`.
No masking line is skipped: the cascade masks nothing -- the masks
(`& 0x1ff`, `& 0xff`, `& 0x7f`) are all INSIDE the arms, after selection.

## 2. Q5 -- THE GAP IS REAL.  `+0xe0` IS CORRECT.  THREE INDEPENDENT PROOFS
  1. `crmfbreg.h` declares `CRIME_RE_CLIP_IDS 0x16e0`, sitting BETWEEN
     `CRIME_RE_TEX 0x1600` and `CRIME_RE_LINEAR_A 0x1700`.
  2. `re_tex[112]` uint16_t = 224 bytes = exactly 0xe0.
  3. `dev_sgi_re.c`'s struct carries `// todo: clip_ids registers.`
     immediately after `re_tex`.
TEX must NOT extend to 0x1700.  There IS a second finding, but not the one Q5
proposed: **the 32-byte run is a NAMED, DOCUMENTED register block that is
deliberately unmodelled -- not "unmapped space"**, and the brief's own window
table omits CLIP_IDS entirely, which is why the question arose.

## 3. SIBLING PARITY -- the warrant nobody has cited
All four devices in this file have a catch-all with the SAME message wording.
THREE OF THE FOUR ALREADY DECLINE:

  device          arm         announce   exit(1)   falls to tail
  sgi_re          else        fatal()    YES       no -- DIES
  sgi_de          default:    fatal()    no        yes
  sgi_mte         default:    fatal()    no        yes
  sgi_de_status   default:    debug()    no        yes

`sgi_re`'s catch-all is the ONLY one of four that kills.  The fix is not a
design question; it is RESTORING PARITY with three siblings in the same file
that share its message text verbatim.  That is a transferred in-tree warrant,
which the addition-licence rule prefers over reasoning from first principles.

## 4. TWO BOUND IDIOMS IN ONE CASCADE (minor, but it decides accept rows)
  TLB_A, TLB_B     upper bound = THE NEXT CONSTANT   (CRIME_RE_TLB_B/_TLB_C)
  TLB_C, TEX, LIN_A, LIN_B   upper bound = BASE + SIZE
Same numbers today.  They fail DIFFERENTLY under edits: a next-constant bound
follows the neighbour if the neighbour moves; a base+size bound does not.

## 5. A SEPARATE, NON-SAFETY OBSERVATION -- FILED, ranked below the live kill
The TEX arm indexes `((relative_addr & 0xff) >> 3) & 0xff` and then writes
`tlbi..tlbi+3`.  Enumerated: that reaches `re_tex[0..30]` of `[112]`.
NOT an out-of-bounds (30 < 112), so no safety consequence -- but three quarters
of the array is unreachable and consecutive 8-byte writes overlap by three
entries.  The three TLB arms use `>> 1`, which for TEX would give 0..111 and
exactly fill the array, exactly as TLB_A's `>>1` fills `re_tlb_a[256]`.
**UNKNOWN which is correct**: derived by `ls _scratchpad/*.pdf`, there are
fifteen manuals and NOT ONE is an SGI/CRIME/O2 document, so `crmfbreg.h` is the
only authority available and it does not describe the indexing.
