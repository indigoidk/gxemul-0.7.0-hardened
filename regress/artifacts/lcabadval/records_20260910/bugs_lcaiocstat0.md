
### `lcaiocstat0` (med) -- filed 2026-09-10

`dev_lca.c` `DEVICE_ACCESS(lca_ioc)` has no arm for four DOCUMENTED IOC registers -- STAT0 (`+0x040`),
STAT1 (`+0x060`), SFT_RST (`+0x0c0`), PAR_DIS (`+0x0e0`; `_scratchpad/21066_66a_hrm.txt:10461`,
`:10496`) -- and S6.4.14 items 1-2 REQUIRE the SROM initialisation sequence to write SFT_RST and STAT0.
Before `#518` those writes ended the emulator process in the `default:` arm; after `#518` they survive
as a once-announced declined write, and a later read answers zero rather than the written bits. That
is a strict improvement and still not the register: the disposition owed is option-set member 7,
IMPLEMENT (SFT_RST drives PCI `rst_l`; STAT0/STAT1 are the error log the rest of HRM chapter 6
writes). `alpha_lcareg.h` defines STAT0/STAT1 with full field masks and has no SFT_RST. Found by the
grok seat on `#518`'s pass 2, which also caught the default-arm comment calling these "unlisted"
offsets -- corrected in the diff. Rung-3 witness constructible from `regress/lca_badval_probe.py`'s
session shape (a quadword store to `+0x0c0`, read back); no guest that needs the registers has been
measured.
