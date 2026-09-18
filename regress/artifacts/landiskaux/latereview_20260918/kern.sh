#!/bin/bash
zcat /mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd > /tmp/lax_kernel.elf
ls -la /tmp/lax_kernel.elf
python3 /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918/elfsyms.py /tmp/lax_kernel.elf wdc_obio obio_iomem wdcreset wdcprobe __wdcwait_reset wdc_reset_channel
