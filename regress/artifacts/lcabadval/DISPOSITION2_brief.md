# lcabadval -- DISPOSITION.  Six chipset registers end the host on an out-of-set value.

**PLEASE DO NOT RATIFY.**  This row has already had one panel OVERTURNED by a fact checkable in a
single grep, and its own census has been corrected twice.  **Check the premises, not just the
derivations**, and say plainly if the packet cannot settle something.

**Tree under review: `GXEMUL-SEC/src/`.**  Other `src/` copies under the project root are pristine
2021 upstream.

---

## 1.  THE SITES, verbatim

`dev_lca.c`, `DEVICE_ACCESS(lca_ioc)`.  Six write arms each end with a `fatal()` + `exit(1)` when
the value written is outside a small accepted set, plus a seventh in `default:`.

```c
 220| 	if (writeflag == MEM_WRITE)
 221| 		idata = memory_readmax64(cpu, data, len);
 222| 
 223| 	switch (relative_addr + LCA_IOC_BASE) {
 224| 
 225| 	case LCA_IOC_BASE:
 226| 		/*  Ignore? Linux reads from the base at startup.  */
 227| 		break;
 228| 
 229| 	case LCA_IOC_CONF:
 230| 		if (writeflag == MEM_READ) {
 231| 			odata = d->ioc_conf;
 232| 		} else {
 233| 			d->ioc_conf = idata;
 234| 			/*  Only bit 0 is implemented so far, the PCI bus 0 vs
 235| 			    bus non-0 selection bit.  */
 236| 			if (idata & ~1) {
 237| 				/*  #506: was `0x%x', (int)idata -- a 64-bit guarded value
 238| 				    narrowed to 32 in the KILL diagnostic, so a write of
 239| 				    0x100000000 trips `idata & ~1' and then reports "0x0",
 240| 				    which is a value this same guard ACCEPTS.  The five
 241| 				    sibling arms below already print the full width this
 242| 				    way; this arm was the outlier among the VALUE-guard
 243| 				    diagnostics.  (Not the file's only narrowing site --
 244| 				    the default arm below has the same cast, and this
 245| 				    round fixes it too.)  */
 246| 				fatal("TODO: Write to unimplemented bit of"
 247| 				    " IOC_CONF: 0x%" PRIx64 "\n", (uint64_t)idata);
 248| 				exit(1);
 249| 			}
 250| 		}
 251| 		break;
 252| 
 253| 	case LCA_IOC_TBIA:
 254| 		/*  TLB Invalidate All.  */
 255| 		/*  TODO: For now, let's just ignore it.  */
 256| 		break;
 257| 
 258| 	case LCA_IOC_TB_ENA:
 259| 		if (writeflag == MEM_READ) {
 260| 			odata = d->tlb_enable;
 261| 		} else {
 262| 			d->tlb_enable = idata;
 263| 			/*  TODO: Actually implement this.  */
 264| 			if (idata & ~IOC_TB_ENA_TEN) {
 265| 				fatal("TODO: LCA_IOC_TB_ENA value "
 266| 				    " (0x%" PRIx64") has unimplemented "
 267| 				    "bits.\n", (uint64_t)idata);
 268| 				exit(1);
 269| 			}
 270| 		}
 271| 		break;
 272| 
 273| 	case LCA_IOC_W_BASE0:
 274| 		if (writeflag == MEM_READ) {
 275| 			odata = d->window_base_0;
 276| 		} else {
 277| 			d->window_base_0 = idata;
 278| 			/*  TODO: Actually implement this.  */
 279| 			if (idata != 0ULL && idata != 0x300800000ULL) {
 280| 				fatal("TODO: LCA_IOC_W_BASE0 value differs"
 281| 				    " (0x%" PRIx64") from the only implemented"
 282| 				    " values\n", (uint64_t)idata);
 283| 				exit(1);
 284| 			}
 285| 		}
 286| 		break;
 287| 
 288| 	case LCA_IOC_W_MASK0:
 289| 		if (writeflag == MEM_READ) {
 290| 			odata = d->window_mask_0;
 291| 		} else {
 292| 			d->window_mask_0 = idata;
 293| 			/*  TODO: Actually implement this.  */
 294| 			if (idata != 0x700000ULL) {
 295| 				fatal("TODO: LCA_IOC_W_MASK0 value differs"
 296| 				    " (0x%" PRIx64") from the only implemented"
 297| 				    " value\n", (uint64_t)idata);
 298| 				exit(1);
 299| 			}
 300| 		}
 301| 		break;
 302| 
 303| 	case LCA_IOC_W_T_BASE0:
 304| 		if (writeflag == MEM_READ) {
 305| 			odata = d->window_t_base_0;
 306| 		} else {
 307| 			d->window_t_base_0 = idata;
 308| 			/*  TODO: Actually implement this.  */
 309| 		}
 310| 		break;
 311| 
 312| 	case LCA_IOC_W_BASE1:
 313| 		if (writeflag == MEM_READ) {
 314| 			odata = d->window_base_1;
 315| 		} else {
 316| 			d->window_base_1 = idata;
 317| 			/*  TODO: Actually implement this.  */
 318| 			if (idata != 0x240000000ULL) {
 319| 				fatal("TODO: LCA_IOC_W_BASE1 value differs"
 320| 				    " (0x%" PRIx64") from the only implemented"
 321| 				    " value\n", (uint64_t)idata);
 322| 				exit(1);
 323| 			}
 324| 		}
 325| 		break;
 326| 
 327| 	case LCA_IOC_W_MASK1:
 328| 		if (writeflag == MEM_READ) {
 329| 			odata = d->window_mask_1;
 330| 		} else {
 331| 			d->window_mask_1 = idata;
 332| 			/*  TODO: Actually implement this.  */
 333| 			if (idata != 0x3ff00000ULL) {
 334| 				fatal("TODO: LCA_IOC_W_MASK1 value differs"
 335| 				    " (0x%" PRIx64") from the only implemented"
 336| 				    " value\n", (uint64_t)idata);
 337| 				exit(1);
 338| 			}
 339| 		}
 340| 		break;
 341| 
 342| 	case LCA_IOC_W_T_BASE1:
 343| 		if (writeflag == MEM_READ) {
 344| 			odata = d->window_t_base_1;
 345| 		} else {
 346| 			d->window_t_base_1 = idata;
 347| 			/*  TODO: Actually implement this.  */
 348| 		}
 349| 		break;
 350| 
 351| 	default:fatal("[ lca_ioc: unimplemented %s to offset 0x%x",
 352| 		    writeflag == MEM_WRITE? "write" : "read", (int)
 353| 		    relative_addr);
 354| 		if (writeflag == MEM_WRITE)
 355| 			fatal(": 0x%" PRIx64, (uint64_t)idata);	/*  #506  */
 356| 		fatal(" ]\n");
 357| 		exit(1);
 358| 	}
 359| 
 360| 	if (writeflag == MEM_READ)
```

## 2.  ESTABLISHED FACTS (carried from this row's prior work, each verified when recorded)

* **The guards are TWO predicate shapes, not one:** BIT-MASKS (`CONF`, `TB_ENA`) and EQUALITY
  WHITELISTS (the four window registers).  **`W_BASE0` accepts TWO values**, so the row's original
  "four registers accept exactly one value each" framing was already false before the count was
  corrected to six.
* **Whole-file kill census: ELEVEN live `exit(1)`.**  Removing these six leaves five -- the
  `default:` arm (reads AND writes, covering STAT0/STAT1 and the rest of the 512 MB IOC window),
  `lca_pci_conf`'s `bus != 0`, `lca_isa`'s `ofs > len`, and the bare `lca_interrupt_assert` /
  `_deassert` TODO pair.  *Those last two are separate filed rows, not this round.*
* **A window offset of 0 silently succeeds**, so a miss control must not use `LCA_IOC_BASE + 0`.

## 3.  THE TWO DISPOSITIONS ON THE TABLE

**Please correct my statement of these if I have them wrong** -- they are reconstructed from this
row's prior panel, not quoted from a spec.

* **A -- delete the `exit(1)`, KEEP the store, optional latched announce.**  One design covers all
  six arms.
* **B -- treat the register as write-only backing state**: accept and store, and do not pretend the
  model acts on it.

**The prior codex verdict was:** *"Your argument for A fails as written: RCR1 also has no functional
consumer.  I recommend B for pass 1 as a conservative policy choice; hardware-correct
write/readback behavior remains unproved."*  A later note in the same row objects that *"B is a
coherent answer only for a consumed field, which five of these are not."*

**The `#447` precedent being invoked is `rtc_rcr1` in `dev_sh4.c`, and it was verified by grep to
have exactly FOUR occurrences -- declaration, readback, store, and one inside a comment -- i.e. NO
functional consumer.**

## 4.  QUESTIONS

**Q1 (THE HELD QUESTION).  Given that `rtc_rcr1` is measured to have zero functional consumers, does
the `#447` precedent support B for all six arms here -- or does it cut the other way, since the
thing that made B acceptable there was precisely that nothing consumed the field?**

**Q2 (THE ONE I THINK IS SHARPEST).  Is B even WELL-DEFINED AT RESET?**  `W_MASK0`, `W_BASE1` and
`W_MASK1` reset to 0, **and 0 is not in their accepted set**.  So the model's own reset state is one
its own guard would reject.  Does that make B incoherent for those three, make the GUARD wrong, or
neither?  **Derive it from the arms above rather than from the framing.**

**Q3 (OPTION-SET COMPLETENESS).  A and B are the two options this row has been arguing about.  What
is the third?**  This project has twice found that a two-membered option set produces a panel
arguing about two options while the right answer was never named -- and both times the member was
found by GREPPING THE FORK for an existing idiom rather than by reasoning.  **Look at what the
sibling arms in this same file and this same switch already do** (`LCA_IOC_BASE`, `LCA_IOC_TBIA`,
`LCA_IOC_W_T_BASE0/1` are right there and do NOT kill), and at what `default:` does.

**Q4 (PREMISE AUDIT).**  Which fact in section 2 is wrong?  The census is the one I would attack
first -- it has been corrected twice already.

**Verdict line first** -- A / B / a third member you name -- then the body.  **A verdict that merely
agrees is the least useful reply**; if you find nothing wrong, say what you CHECKED and how.
