# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pckbcledparam` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pckbcledparam`, state `open`)

**title:** devices/dev_pckbc.c:dev_pckbc_command -- the Set-LEDs parameter byte is parsed as a new command (non-zero bytes get RESEND) -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T53 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-12).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/d2ff00eb9d9dc8e8b660672c9a155a8131cb2b20, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/c861ff6d1909a97715eddf7d30b8d8cabd352519.  Our site at de8c7547: src/devices/dev_pckbc.c:820-823, :812-818, :901-905.  Portable fix: yes -- port rs6000 d2ff00e, rs6000 c861ff6.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_pckbc.c:820

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_pckbc.c b/src/devices/dev_pckbc.c
index fd2cde1a..beb4d671 100644
--- a/src/devices/dev_pckbc.c
+++ b/src/devices/dev_pckbc.c
@@ -773,6 +773,13 @@ static void dev_pckbc_command(struct pckbc_data *d, int port_nr)
 		return;
 	}
 
+	if (d->state[port_nr] == 1000) {
+		/* #pckbcledparam: absorb parameter byte */
+		pckbc_add_code(d, KBR_ACK, port_nr);
+		d->state[port_nr] = STATE_NORMAL;
+		return;
+	}
+
 	if (d->state[port_nr] == STATE_WAITING_FOR_RATE) {
 		debug("[ pckbc: (port %i) received Typematic/Sample Rate data: "
 		    "0x%02x ]\n", port_nr, cmd);
@@ -820,6 +827,7 @@ static void dev_pckbc_command(struct pckbc_data *d, int port_nr)
 	case KBC_MODEIND:	/*  Set LEDs  */
 		/*  Just ACK, no LEDs are actually set.  */
 		pckbc_add_code(d, KBR_ACK, port_nr);
+		d->state[port_nr] = 1000;
 		break;
 
 	case KBC_ECHO:
```

## Every edited function, after the fix

### `src/devices/dev_pckbc.c` -- post-edit lines 735-914 (`+` marks a line the diff added or the point of a deletion)

```c
  735|  static void dev_pckbc_command(struct pckbc_data *d, int port_nr)
  736|  {
  737|  	int cmd = d->type == PCKBC_8242 ? d->reg[PS2_TXBUF] : d->reg[PC_CMD];
  738|  
  739|  #if 0
  740|  	// Mouse port debugging:
  741|  	if (port_nr == 1)
  742|  		fatal("[ pckbc: (port %i) command 0x%02x ]\n", port_nr, cmd);
  743|  #endif
  744|  
  745|  	if (d->state[port_nr] == STATE_WAITING_FOR_TRANSLTABLE) {
  746|  		debug("[ pckbc: (port %i) switching to translation table "
  747|  		    "0x%02x ]\n", port_nr, cmd);
  748|  
  749|  		switch (cmd) {
  750|  		case 0:	// TODO. "Writing 0xf0 followed by 0 queries the mode,
  751|  			//  resulting in a scancode byte 43, 41 or 3f from the
  752|  			//  keyboard." according to
  753|  			// https://www.win.tue.nl/~aeb/linux/kbd/scancodes-10.html#scancodesets
  754|  			fatal("[ pckbc: TODO: return current translation table ]\n");
  755|  			break;
  756|  		case 1:	// Fall-through.
  757|  		case 2:	// Fall-through.
  758|  		case 3:	d->translation_table = cmd;
  759|  			break;
  760|  		default:fatal("[ pckbc: (port %i) translation table "
  761|  			    "0x%02x is NOT YET IMPLEMENTED ]\n",
  762|  			    port_nr, cmd);
  763|  		}
  764|  
  765|  		// Hack for OpenBSD/cats and NetBSD/cats:
  766|  		if (d->type != PCKBC_8242) {
  767|  			fatal("[ pckbc: TODO: hack for non-8242. figure out how to deal with this ]\n");
  768|  			d->translation_table = 1;
  769|  		}
  770|  
  771|  		pckbc_add_code(d, KBR_ACK, port_nr);
  772|  		d->state[port_nr] = STATE_NORMAL;
  773|  		return;
  774|  	}
  775|  
  776|+ 	if (d->state[port_nr] == 1000) {
  777|+ 		/* #pckbcledparam: absorb parameter byte */
  778|+ 		pckbc_add_code(d, KBR_ACK, port_nr);
  779|+ 		d->state[port_nr] = STATE_NORMAL;
  780|+ 		return;
  781|+ 	}
  782|+ 
  783|  	if (d->state[port_nr] == STATE_WAITING_FOR_RATE) {
  784|  		debug("[ pckbc: (port %i) received Typematic/Sample Rate data: "
  785|  		    "0x%02x ]\n", port_nr, cmd);
  786|  		pckbc_add_code(d, KBR_ACK, port_nr);
  787|  		d->state[port_nr] = STATE_NORMAL;
  788|  		return;
  789|  	}
  790|  
  791|  	if (d->state[port_nr] == STATE_WAITING_FOR_ONEKEY_MB) {
  792|  		debug("[ pckbc: (port %i) received One-key make/break data: "
  793|  		    "0x%02x ]\n", port_nr, cmd);
  794|  		pckbc_add_code(d, KBR_ACK, port_nr);
  795|  		d->state[port_nr] = STATE_NORMAL;
  796|  		return;
  797|  	}
  798|  
  799|  	if (d->state[port_nr] == STATE_WAITING_FOR_AUX) {
  800|  		debug("[ pckbc: (port %i) received aux data: "
  801|  		    "0x%02x ]\n", port_nr, cmd);
  802|  		/*  Echo back.  */
  803|  		pckbc_add_code(d, cmd, port_nr);
  804|  		d->state[port_nr] = STATE_NORMAL;
  805|  		return;
  806|  	}
  807|  
  808|  	if (d->state[port_nr] == STATE_WAITING_FOR_AUX_OUT) {
  809|  		debug("[ pckbc: (port %i) received aux out data: "
  810|  		    "0x%02x ]\n", port_nr, cmd);
  811|  		/*  Echo back.  */
  812|  		pckbc_add_code(d, cmd, port_nr);
  813|  		d->state[port_nr] = STATE_NORMAL;
  814|  		return;
  815|  	}
  816|  
  817|  	switch (cmd) {
  818|  
  819|  	case 0x00:
  820|  		/*
  821|  		 *  TODO: What does this do? This is possibly due to an
  822|  		 *  error in the handling of some other command code.
  823|  		 */
  824|  		pckbc_add_code(d, KBR_ACK, port_nr);
  825|  		break;
  826|  
  827|  	case KBC_MODEIND:	/*  Set LEDs  */
  828|  		/*  Just ACK, no LEDs are actually set.  */
  829|  		pckbc_add_code(d, KBR_ACK, port_nr);
  830|+ 		d->state[port_nr] = 1000;
  831|  		break;
  832|  
  833|  	case KBC_ECHO:
  834|  		pckbc_add_code(d, KBR_ECHO, port_nr);
  835|  		break;
  836|  
  837|  	case KBC_SETTABLE:
  838|  		pckbc_add_code(d, KBR_ACK, port_nr);
  839|  		d->state[port_nr] = STATE_WAITING_FOR_TRANSLTABLE;
  840|  		break;
  841|  
  842|  	case KBC_ENABLE:
  843|  		d->scanning_enabled[port_nr] = 1;
  844|  		pckbc_add_code(d, KBR_ACK, port_nr);
  845|  		break;
  846|  
  847|  	case KBC_DISABLE:
  848|  		d->scanning_enabled[port_nr] = 0;
  849|  		pckbc_add_code(d, KBR_ACK, port_nr);
  850|  		break;
  851|  
  852|  	case KBC_SETDEFAULT:
  853|  		pckbc_add_code(d, KBR_ACK, port_nr);
  854|  		break;
  855|  
  856|  	case KBC_GETID:
  857|  		/*  Get keyboard/mouse ID.  NOTE/TODO: Ugly hardcoded answer.  */
  858|  		pckbc_add_code(d, KBR_ACK, port_nr);
  859|  		
  860|  		if (port_nr == 0) {
  861|  			// Keyboard:
  862|  			pckbc_add_code(d, 0xab, port_nr);
  863|  			pckbc_add_code(d, 0x41, port_nr);
  864|  		} else {
  865|  			// Mouse:
  866|  			pckbc_add_code(d, 0x00, port_nr);
  867|  			pckbc_add_code(d, 0x00, port_nr);
  868|  		}
  869|  		break;
  870|  
  871|  	case KBC_TYPEMATIC:
  872|  		/*
  873|  		 *  Keyboard: Set typematic (auto-repeat) delay/speed.
  874|  		 *  PS/2 mouse: Set sample ratre.
  875|  		 */
  876|  		pckbc_add_code(d, KBR_ACK, port_nr);
  877|  		d->state[port_nr] = STATE_WAITING_FOR_RATE;
  878|  		break;
  879|  
  880|  	case KBC_ALLKEYS_TMB:
  881|  		/*  "Make all keys typematic/make/break"  */
  882|  		pckbc_add_code(d, KBR_ACK, port_nr);
  883|  		break;
  884|  
  885|  	case KBC_ONEKEY_MB:
  886|  		/*  "Make one key typematic/make/break"  */
  887|  		pckbc_add_code(d, KBR_ACK, port_nr);
  888|  		d->state[port_nr] = STATE_WAITING_FOR_ONEKEY_MB;
  889|  		break;
  890|  
  891|  	case KBC_RESET:
  892|  		pckbc_add_code(d, KBR_ACK, port_nr);
  893|  		pckbc_add_code(d, KBR_RSTDONE, port_nr);
  894|  
  895|  		if (port_nr == 1) {
  896|  			// Mouse (based on NetBSD's pckbport/pms.c) sends
  897|  			// mouse ID after RSTDONE:
  898|  			pckbc_add_code(d, 0x00, port_nr);
  899|  		}
  900|  
  901|  		/*
  902|  		 *  Disable interrupts during reset, or Linux 2.6
  903|  		 *  prints warnings about spurious interrupts.
  904|  		 */
  905|  		// d->rx_int_enable = 0;
  906|  		d->scanning_enabled[port_nr] = 0;
  907|  		break;
  908|  
  909|  	default:
  910|  		pckbc_add_code(d, KBR_RESEND, port_nr); // Error
  911|  		debugmsg(SUBSYS_DEVICE, "pckbc", VERBOSITY_WARNING,
  912|  		    "UNIMPLEMENTED command 0x%02x (port %i)", cmd, port_nr);
  913|  	}
  914|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PCKBCLEDPARAM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_PCKBCLEDPARAM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
