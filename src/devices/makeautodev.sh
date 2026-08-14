#!/bin/sh
###############################################################################
#
#  Copyright (C) 2005-2018  Anders Gavare.  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#  3. The name of the author may not be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  SUCH DAMAGE.


printf "Generating autodev.c... "

#  Build into a PID-unique temp file and atomically rename it into place at
#  the end.  The recursive-make rules (all -> objs -> autodev.o) can invoke
#  this script concurrently; appending directly to autodev.c then lets two
#  runs interleave their writes and drop a line's first printf, corrupting a
#  random device_register/pci_register entry (an intermittent build failure).
#  A unique temp file + atomic mv makes the output correct regardless.
AD="autodev.c.new.$$"
rm -f "$AD"

printf "/*\n *  DO NOT EDIT. AUTOMATICALLY CREATED\n */\n\n" >> "$AD"

cat autodev_head.c >> "$AD"

printf "5"
rm -f .index
for a in *.c; do
	B=`grep COMMENT $a`
	if [ z"$B" != z ]; then
		printf "$a " >> .index
		echo "$B"|cut -d : -f 2- >> .index
	fi
done

#  #406: ANCHOR the scrape, and SUPPRESS pathname expansion around the loops.
#
#  The four loops below used `grep DEVINIT` / `grep PCIINIT` UNANCHORED and then
#  iterated the result with an UNQUOTED `for B in $C`, which the shell subjects
#  to word splitting AND pathname expansion.  So any prose mention of the macro
#  name -- in a comment, anywhere in the file -- reached the generated output.
#  And because `cut` passes a line through unchanged when its delimiter is
#  absent, a comment line's leading `*` survived both cuts and became a glob
#  that expanded to the entire directory listing.
#
#  MEASURED, triggered by one prose line (dev_rs5c313.c:144, " *  ... the
#  DEVINIT defaults,"): 319 declarations instead of 77.  229 of the extras carry
#  a `.` in the name -- Makefile.skel, bus_isa.o, even this script's own
#  in-flight temp file autodev.c.new.NNNN -- and are syntax errors.  The other
#  14 are valid C identifiers (Makefile, README, fonts, and the comment's own
#  words), so they fail at LINK time instead.  358 compiler errors, no binary.
#
#  *** BOTH HALVES ARE LOAD-BEARING, they are not alternatives.  Anchoring is
#  what removes the prose words; `set -f` alone would leave all 14 of them and
#  merely change the failure from a parse error to an undefined symbol. ***
#
#  Anchoring is exact rather than a heuristic: all 77 `^DEVINIT(` sites and all
#  28 `^PCIINIT(` sites sit at column 1 (none indented, none under a nearby
#  #if), and the anchored name list is set- AND order-identical to the committed
#  autodev.c in both trees.  So this cannot change the shipped device table.
#
#  `set -f` is bracketed around each inner loop instead of being set once at the
#  top of the script, because a script-wide noglob would stop `for a in dev_*.c`
#  from expanding at all -- which would silently generate an EMPTY device table.
printf "4"
for a in dev_*.c; do
	B=`grep '^DEVINIT(' $a`
	if [ z"$B" != z ]; then
		C=`grep '^DEVINIT(' $a | cut -d \( -f 2|cut -d \) -f 1`
		set -f
		for B in $C; do
			printf "int devinit_$B(struct devinit *);\n" >> "$AD"
		done
		set +f
	fi
done

printf "3"
for a in bus_pci.c; do
	B=`grep '^PCIINIT(' $a`
	if [ z"$B" != z ]; then
		C=`grep '^PCIINIT(' $a | cut -d \( -f 2|cut -d \) -f 1`
		set -f
		for B in $C; do
			printf "void pciinit_$B(struct machine *, " >> "$AD"
			printf "struct memory *, struct pci_device *);\n" >> "$AD"
		done
		set +f
	fi
done

cat autodev_middle.c >> "$AD"

printf "2"
for a in dev_*.c; do
	B=`grep '^DEVINIT(' $a`
	if [ z"$B" != z ]; then
		C=`grep '^DEVINIT(' $a | cut -d \( -f 2|cut -d \) -f 1`
		set -f
		for B in $C; do
			printf "\tdevice_register(\""$B"\"," >> "$AD"
			printf " devinit_$B);\n" >> "$AD"
		done
		set +f
	fi
done

printf "1"
for a in bus_pci.c; do
	B=`grep '^PCIINIT(' $a`
	if [ z"$B" != z ]; then
		C=`grep '^PCIINIT(' $a | cut -d \( -f 2|cut -d \) -f 1`
		set -f
		for B in $C; do
			printf "\tpci_register(\""$B"\"," >> "$AD"
			printf " pciinit_$B);\n" >> "$AD"
		done
		set +f
	fi
done

cat autodev_tail.c >> "$AD"

#  Atomically replace autodev.c (see the temp-file note above).
mv -f "$AD" autodev.c

printf " done\n"
