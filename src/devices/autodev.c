/*
 *  DO NOT EDIT. AUTOMATICALLY CREATED
 */

/*
 *  Copyright (C) 2005-2009  Anders Gavare.  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright  
 *     notice, this list of conditions and the following disclaimer in the 
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
 *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 *  SUCH DAMAGE.
 *   
 *
 *  Automatically register all devices from the devices/ subdir.
 *
 *  NOTE: autodev_head.c, plus a line for each device, plus autodev_middle.c,
 *  plus another line (again) for each device, plus autodev_tail.c should be
 *  combined into one. See makeautodev.sh for more info.
 */

#include <stdio.h>

#include "bus_pci.h"
#include "device.h"

int devinit_8253(struct devinit *);
int devinit_8259(struct devinit *);
int devinit_adb(struct devinit *);
int devinit_ahc(struct devinit *);
int devinit_algor(struct devinit *);
int devinit_bebox(struct devinit *);
int devinit_clmpcc(struct devinit *);
int devinit_cons(struct devinit *);
int devinit_cpc700(struct devinit *);
int devinit_dec21030(struct devinit *);
int devinit_dec21143(struct devinit *);
int devinit_dec5800(struct devinit *);
int devinit_decbi(struct devinit *);
int devinit_disk(struct devinit *);
int devinit_dreamcast_asic(struct devinit *);
int devinit_dreamcast_g2(struct devinit *);
int devinit_dreamcast_gdrom(struct devinit *);
int devinit_dreamcast_maple(struct devinit *);
int devinit_dreamcast_rtc(struct devinit *);
int devinit_eagle(struct devinit *);
int devinit_ether(struct devinit *);
int devinit_fbctrl(struct devinit *);
int devinit_fdc(struct devinit *);
int devinit_footbridge(struct devinit *);
int devinit_gc(struct devinit *);
int devinit_hammerhead(struct devinit *);
int devinit_i80321(struct devinit *);
int devinit_igsfb(struct devinit *);
int devinit_iq80321_7seg(struct devinit *);
int devinit_irqc(struct devinit *);
int devinit_jazz(struct devinit *);
int devinit_kn02(struct devinit *);
int devinit_kn02ba(struct devinit *);
int devinit_kn230(struct devinit *);
int devinit_lca(struct devinit *);
int devinit_lpt(struct devinit *);
int devinit_luna88k(struct devinit *);
int devinit_lunafb(struct devinit *);
int devinit_m8820x(struct devinit *);
int devinit_malta_lcd(struct devinit *);
int devinit_mb8696x(struct devinit *);
int devinit_mb89352(struct devinit *);
int devinit_mk48txx(struct devinit *);
int devinit_mp(struct devinit *);
int devinit_mvme187(struct devinit *);
int devinit_ns16550(struct devinit *);
int devinit_ohci(struct devinit *);
int devinit_osiop(struct devinit *);
int devinit_palmbus(struct devinit *);
int devinit_pcc2(struct devinit *);
int devinit_pccmos(struct devinit *);
int devinit_pcic(struct devinit *);
int devinit_pmppc(struct devinit *);
int devinit_prep(struct devinit *);
int devinit_ps2_ether(struct devinit *);
int devinit_ps2_gif(struct devinit *);
int devinit_ps2_gs(struct devinit *);
int devinit_ps2_spd(struct devinit *);
int devinit_ps2(struct devinit *);
int devinit_pvr(struct devinit *);
int devinit_random(struct devinit *);
int devinit_rs5c313(struct devinit *);
int devinit_rtc(struct devinit *);
int devinit_rtl8139c(struct devinit *);
int devinit_sgi_ip19(struct devinit *);
int devinit_sgi_ip30(struct devinit *);
int devinit_mace(struct devinit *);
int devinit_sgi_mardigras(struct devinit *);
int devinit_sh4(struct devinit *);
int devinit_sn(struct devinit *);
int devinit_unreadable(struct devinit *);
int devinit_v3(struct devinit *);
int devinit_vme(struct devinit *);
int devinit_wdc(struct devinit *);
int devinit_z8530(struct devinit *);
int devinit_zero(struct devinit *);
void pciinit_igsfb(struct machine *, struct memory *, struct pci_device *);
void pciinit_s3_virge(struct machine *, struct memory *, struct pci_device *);
void pciinit_ali_m1543(struct machine *, struct memory *, struct pci_device *);
void pciinit_ali_m5229(struct machine *, struct memory *, struct pci_device *);
void pciinit_ahc(struct machine *, struct memory *, struct pci_device *);
void pciinit_gt64011(struct machine *, struct memory *, struct pci_device *);
void pciinit_gt64120(struct machine *, struct memory *, struct pci_device *);
void pciinit_gt64260(struct machine *, struct memory *, struct pci_device *);
void pciinit_pcn(struct machine *, struct memory *, struct pci_device *);
void pciinit_i31244(struct machine *, struct memory *, struct pci_device *);
void pciinit_piix3_isa(struct machine *, struct memory *, struct pci_device *);
void pciinit_piix4_isa(struct machine *, struct memory *, struct pci_device *);
void pciinit_i82378zb(struct machine *, struct memory *, struct pci_device *);
void pciinit_piix3_ide(struct machine *, struct memory *, struct pci_device *);
void pciinit_piix4_ide(struct machine *, struct memory *, struct pci_device *);
void pciinit_ibm_isa(struct machine *, struct memory *, struct pci_device *);
void pciinit_heuricon_pmppc(struct machine *, struct memory *, struct pci_device *);
void pciinit_vt82c586_isa(struct machine *, struct memory *, struct pci_device *);
void pciinit_vt82c586_ide(struct machine *, struct memory *, struct pci_device *);
void pciinit_symphony_83c553(struct machine *, struct memory *, struct pci_device *);
void pciinit_symphony_82c105(struct machine *, struct memory *, struct pci_device *);
void pciinit_rtl8139c(struct machine *, struct memory *, struct pci_device *);
void pciinit_dec21143(struct machine *, struct memory *, struct pci_device *);
void pciinit_dec21030(struct machine *, struct memory *, struct pci_device *);
void pciinit_eagle(struct machine *, struct memory *, struct pci_device *);
void pciinit_gc_obio(struct machine *, struct memory *, struct pci_device *);
void pciinit_uninorth(struct machine *, struct memory *, struct pci_device *);
void pciinit_ati_radeon_9200_2(struct machine *, struct memory *, struct pci_device *);

/*
 *  autodev_init():
 */
void autodev_init(void)
{
	/*  printf("autodev_init()\n");  */

	/*  autodev_middle.c ends here.  */

	device_register("8253", devinit_8253);
	device_register("8259", devinit_8259);
	device_register("adb", devinit_adb);
	device_register("ahc", devinit_ahc);
	device_register("algor", devinit_algor);
	device_register("bebox", devinit_bebox);
	device_register("clmpcc", devinit_clmpcc);
	device_register("cons", devinit_cons);
	device_register("cpc700", devinit_cpc700);
	device_register("dec21030", devinit_dec21030);
	device_register("dec21143", devinit_dec21143);
	device_register("dec5800", devinit_dec5800);
	device_register("decbi", devinit_decbi);
	device_register("disk", devinit_disk);
	device_register("dreamcast_asic", devinit_dreamcast_asic);
	device_register("dreamcast_g2", devinit_dreamcast_g2);
	device_register("dreamcast_gdrom", devinit_dreamcast_gdrom);
	device_register("dreamcast_maple", devinit_dreamcast_maple);
	device_register("dreamcast_rtc", devinit_dreamcast_rtc);
	device_register("eagle", devinit_eagle);
	device_register("ether", devinit_ether);
	device_register("fbctrl", devinit_fbctrl);
	device_register("fdc", devinit_fdc);
	device_register("footbridge", devinit_footbridge);
	device_register("gc", devinit_gc);
	device_register("hammerhead", devinit_hammerhead);
	device_register("i80321", devinit_i80321);
	device_register("igsfb", devinit_igsfb);
	device_register("iq80321_7seg", devinit_iq80321_7seg);
	device_register("irqc", devinit_irqc);
	device_register("jazz", devinit_jazz);
	device_register("kn02", devinit_kn02);
	device_register("kn02ba", devinit_kn02ba);
	device_register("kn230", devinit_kn230);
	device_register("lca", devinit_lca);
	device_register("lpt", devinit_lpt);
	device_register("luna88k", devinit_luna88k);
	device_register("lunafb", devinit_lunafb);
	device_register("m8820x", devinit_m8820x);
	device_register("malta_lcd", devinit_malta_lcd);
	device_register("mb8696x", devinit_mb8696x);
	device_register("mb89352", devinit_mb89352);
	device_register("mk48txx", devinit_mk48txx);
	device_register("mp", devinit_mp);
	device_register("mvme187", devinit_mvme187);
	device_register("ns16550", devinit_ns16550);
	device_register("ohci", devinit_ohci);
	device_register("osiop", devinit_osiop);
	device_register("palmbus", devinit_palmbus);
	device_register("pcc2", devinit_pcc2);
	device_register("pccmos", devinit_pccmos);
	device_register("pcic", devinit_pcic);
	device_register("pmppc", devinit_pmppc);
	device_register("prep", devinit_prep);
	device_register("ps2_ether", devinit_ps2_ether);
	device_register("ps2_gif", devinit_ps2_gif);
	device_register("ps2_gs", devinit_ps2_gs);
	device_register("ps2_spd", devinit_ps2_spd);
	device_register("ps2", devinit_ps2);
	device_register("pvr", devinit_pvr);
	device_register("random", devinit_random);
	device_register("rs5c313", devinit_rs5c313);
	device_register("rtc", devinit_rtc);
	device_register("rtl8139c", devinit_rtl8139c);
	device_register("sgi_ip19", devinit_sgi_ip19);
	device_register("sgi_ip30", devinit_sgi_ip30);
	device_register("mace", devinit_mace);
	device_register("sgi_mardigras", devinit_sgi_mardigras);
	device_register("sh4", devinit_sh4);
	device_register("sn", devinit_sn);
	device_register("unreadable", devinit_unreadable);
	device_register("v3", devinit_v3);
	device_register("vme", devinit_vme);
	device_register("wdc", devinit_wdc);
	device_register("z8530", devinit_z8530);
	device_register("zero", devinit_zero);
	pci_register("igsfb", pciinit_igsfb);
	pci_register("s3_virge", pciinit_s3_virge);
	pci_register("ali_m1543", pciinit_ali_m1543);
	pci_register("ali_m5229", pciinit_ali_m5229);
	pci_register("ahc", pciinit_ahc);
	pci_register("gt64011", pciinit_gt64011);
	pci_register("gt64120", pciinit_gt64120);
	pci_register("gt64260", pciinit_gt64260);
	pci_register("pcn", pciinit_pcn);
	pci_register("i31244", pciinit_i31244);
	pci_register("piix3_isa", pciinit_piix3_isa);
	pci_register("piix4_isa", pciinit_piix4_isa);
	pci_register("i82378zb", pciinit_i82378zb);
	pci_register("piix3_ide", pciinit_piix3_ide);
	pci_register("piix4_ide", pciinit_piix4_ide);
	pci_register("ibm_isa", pciinit_ibm_isa);
	pci_register("heuricon_pmppc", pciinit_heuricon_pmppc);
	pci_register("vt82c586_isa", pciinit_vt82c586_isa);
	pci_register("vt82c586_ide", pciinit_vt82c586_ide);
	pci_register("symphony_83c553", pciinit_symphony_83c553);
	pci_register("symphony_82c105", pciinit_symphony_82c105);
	pci_register("rtl8139c", pciinit_rtl8139c);
	pci_register("dec21143", pciinit_dec21143);
	pci_register("dec21030", pciinit_dec21030);
	pci_register("eagle", pciinit_eagle);
	pci_register("gc_obio", pciinit_gc_obio);
	pci_register("uninorth", pciinit_uninorth);
	pci_register("ati_radeon_9200_2", pciinit_ati_radeon_9200_2);

	/*  autodev_tail.c  */
}

