# `landiskaux` (#533) — PASS 2 on the real diff, plus the ONE permitted ask-again

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise stated wrongly. **Check the premises, not just the
derivations.** THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`; ignore the three pristine-2021 upstream copies under the
project root. If you cannot read files that is expected — everything is inlined. **VERDICT LINE FIRST.**

## 1. SETTLED PREMISES (from pass 1, panels 20260918_080238 and _080056, adjudicated by fable5)
* The address is `devinit->addr + 0x2c`, a LITERAL byte offset: NetBSD and OpenBSD landisk `wdc_obio.c` define
  `WDC_OBIO_AUXREG_OFFSET 0x2c` and map `or_addr + WDC_OBIO_AUXREG_OFFSET` unscaled; `AUXREG_SIZE` = 2. `0x16` is
  macppc's factorisation (`0x16 << 4 = 0x160`), not landisk's. Codex's disassembly of the 7.6 ramdisk: `add #44,r5`.
* Boot census (four runs, two instruments): OpenBSD 7.6 makes exactly 12 byte writes to 0x1400002c, 0 reads; the
  first is 0x0c = SRST|4BIT. `wdc_altstatus` at 0x14000206 receives ZERO accesses.
* Whole-machine collision check: landisk registers nothing between `wdc` (0x14000000..0x1400000f) and RAM at
  0x1e000000 except the old altstatus at 0x14000206. 0x1400002c..2d is free.
* The pre-switch `alt_status_addr = devinit->addr + 0x206;` is UNTOUCHED and still serves every machine without a case.
* The switch keys on machine_type: HPCMIPS 1004, MACPPC 2004, IQ80321 5005, LANDISK 6004 — no cross-arm reach.
* The fix DELIVERS the five WDCTL_IDS (nIEN) writes; the aux handler acts on WDCTL_RST only, so nIEN is NOT implemented.

## 2. THE DIFF (the whole product change)
```diff
diff --git a/src/devices/dev_wdc.c b/src/devices/dev_wdc.c
index 7b746bc..2567bc6 100644
--- a/src/devices/dev_wdc.c
+++ b/src/devices/dev_wdc.c
@@ -2107,6 +2107,18 @@ DEVINIT(wdc)
 	case MACHINE_IQ80321:
 		alt_status_addr = devinit->addr + 0x402;
 		break;
+	case MACHINE_LANDISK:
+		/*
+		 *  #533 (landiskaux): NetBSD/OpenBSD landisk wdc_obio.c map
+		 *  the aux (alt-status / Device Control) register at
+		 *  or_addr + WDC_OBIO_AUXREG_OFFSET, a literal byte offset
+		 *  of 0x2c.  Without this case landisk kept the PC-layout
+		 *  +0x206 and the kernel's twelve Device Control writes --
+		 *  the first a soft reset -- landed on unmapped memory.
+		 *  Delivering WDCTL_IDS writes does not implement nIEN.
+		 */
+		alt_status_addr = devinit->addr + 0x2c;
+		break;
 	}
 
 	/*  Get disk geometries:  */
```

## 3. THE DETECTOR, `regress/landisk_aux_probe.py`, 6 rows, three sessions on unmodified `-E landisk`
Each session: 8 x `mov.w` to DATA 0xb4000000 (fills the ring, DRQ, status 0x09), one `mov.b 0x0c` to a CTRL
address (or RAM), then `mov.b` loads of status 0xb400000e, 0xb400002c, 0xb4000206.
  live          RAM-ctrl session: status == 0x09     (control)
  aux 2c rest   RAM-ctrl session: read 0x2c == 0x09  (device signature: 0x2c answers STATUS)
  aux 206 gone  RAM-ctrl session: read 0x206 == 0x00 (unmapped on landisk)
  aux 2c reset  CTRL->0x2c session: status == 0x01  (soft reset purged the ring)
  aux 2c read   CTRL->0x2c session: read 0x2c == 0x01
  206 ctl dead  CTRL->0x206 session: status == 0x09 (the old address lands nowhere)
Wired into `regress/gate_sh_rounding.sh` in the same diff: rows-run pinned to the literal 6, each row pinned by name.

## 4. KILL TABLE — MEASURED 2026-09-18 (scratch clone, baseline cmp CLEAN, clone restored before the legs).
PRETABLE.out was written BEFORE the table and predicted every row below; all six matched.
    base (fix)  6/6  1,1,1,1,1,1
    pre-fix     1/6  1,0,0,0,0,0   (committed build, prefix_HEAD.out)
    M_head      1/6  1,0,0,0,0,0   no landisk case
    M_0x16      3/6  1,0,1,0,0,1   `+ 0x16'
    M_0x2d      3/6  1,0,1,0,0,1   `+ 0x2d'
    M_both      4/6  1,1,0,1,1,0   keep the 0x206 registration AND add 0x2c
    M_above     3/6  1,0,1,0,0,1   case above IQ80321 without break (falls to +0x402)
DISCLOSED, not rowed: initialiser `+0x206' changes (landisk overwrites it); IQ80321 losing its own break (no rig);
registration width 2->1 (all accesses are 1 byte at offset 0 -- filed as `wdcaltwidth'); machine_type-only keying.

## 5. QUESTIONS
Q1. Is the diff correct — does it do exactly what the comment claims, and is the comment itself true?
Q2. THE ASK-AGAIN (capped at one, per project rule): **name the smallest edit to the diff OR to the detector that
    breaks a property this round claims and still scores 6/6.**  The five above are already killed; find a sixth.
Q3. Is any detector row VACUOUS — i.e. can its named channel fail to vary under the mutant it claims to kill?
Q4. Does removing landisk's answer at 0x206 break anything a guest could legitimately do?
