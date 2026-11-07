# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pckbcgetid` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pckbcgetid`, state `open`)

**title:** devices/dev_pckbc.c KBC_GETID -- always answers AB 41 regardless of translation mode -- WRONG-RESULT (minor)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T102 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A5-14).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/94e3ed46472d2c17ffb5eaa2d58aa5ce7b1dae5a.  Our site at de8c7547: src/devices/dev_pckbc.c:848-861.  Portable fix: yes -- port rs6000 94e3ed4.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/devices/dev_pckbc.c:855`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_pckbc.c b/src/devices/dev_pckbc.c
index fd2cde1a..717a5cfb 100644
--- a/src/devices/dev_pckbc.c
+++ b/src/devices/dev_pckbc.c
@@ -852,7 +852,8 @@ static void dev_pckbc_command(struct pckbc_data *d, int port_nr)
 		if (port_nr == 0) {
 			// Keyboard:
 			pckbc_add_code(d, 0xab, port_nr);
-			pckbc_add_code(d, 0x41, port_nr);
+			/* #pckbcgetid: answer depends on translation mode */
+			pckbc_add_code(d, d->translation_table ? 0x41 : 0x83, port_nr);
 		} else {
 			// Mouse:
 			pckbc_add_code(d, 0x00, port_nr);
```

## Every edited function, after the fix

### `src/devices/dev_pckbc.c` -- post-edit lines 735-907 (`+` marks a line the diff added or the point of a deletion)

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
  776|  	if (d->state[port_nr] == STATE_WAITING_FOR_RATE) {
  777|  		debug("[ pckbc: (port %i) received Typematic/Sample Rate data: "
  778|  		    "0x%02x ]\n", port_nr, cmd);
  779|  		pckbc_add_code(d, KBR_ACK, port_nr);
  780|  		d->state[port_nr] = STATE_NORMAL;
  781|  		return;
  782|  	}
  783|  
  784|  	if (d->state[port_nr] == STATE_WAITING_FOR_ONEKEY_MB) {
  785|  		debug("[ pckbc: (port %i) received One-key make/break data: "
  786|  		    "0x%02x ]\n", port_nr, cmd);
  787|  		pckbc_add_code(d, KBR_ACK, port_nr);
  788|  		d->state[port_nr] = STATE_NORMAL;
  789|  		return;
  790|  	}
  791|  
  792|  	if (d->state[port_nr] == STATE_WAITING_FOR_AUX) {
  793|  		debug("[ pckbc: (port %i) received aux data: "
  794|  		    "0x%02x ]\n", port_nr, cmd);
  795|  		/*  Echo back.  */
  796|  		pckbc_add_code(d, cmd, port_nr);
  797|  		d->state[port_nr] = STATE_NORMAL;
  798|  		return;
  799|  	}
  800|  
  801|  	if (d->state[port_nr] == STATE_WAITING_FOR_AUX_OUT) {
  802|  		debug("[ pckbc: (port %i) received aux out data: "
  803|  		    "0x%02x ]\n", port_nr, cmd);
  804|  		/*  Echo back.  */
  805|  		pckbc_add_code(d, cmd, port_nr);
  806|  		d->state[port_nr] = STATE_NORMAL;
  807|  		return;
  808|  	}
  809|  
  810|  	switch (cmd) {
  811|  
  812|  	case 0x00:
  813|  		/*
  814|  		 *  TODO: What does this do? This is possibly due to an
  815|  		 *  error in the handling of some other command code.
  816|  		 */
  817|  		pckbc_add_code(d, KBR_ACK, port_nr);
  818|  		break;
  819|  
  820|  	case KBC_MODEIND:	/*  Set LEDs  */
  821|  		/*  Just ACK, no LEDs are actually set.  */
  822|  		pckbc_add_code(d, KBR_ACK, port_nr);
  823|  		break;
  824|  
  825|  	case KBC_ECHO:
  826|  		pckbc_add_code(d, KBR_ECHO, port_nr);
  827|  		break;
  828|  
  829|  	case KBC_SETTABLE:
  830|  		pckbc_add_code(d, KBR_ACK, port_nr);
  831|  		d->state[port_nr] = STATE_WAITING_FOR_TRANSLTABLE;
  832|  		break;
  833|  
  834|  	case KBC_ENABLE:
  835|  		d->scanning_enabled[port_nr] = 1;
  836|  		pckbc_add_code(d, KBR_ACK, port_nr);
  837|  		break;
  838|  
  839|  	case KBC_DISABLE:
  840|  		d->scanning_enabled[port_nr] = 0;
  841|  		pckbc_add_code(d, KBR_ACK, port_nr);
  842|  		break;
  843|  
  844|  	case KBC_SETDEFAULT:
  845|  		pckbc_add_code(d, KBR_ACK, port_nr);
  846|  		break;
  847|  
  848|  	case KBC_GETID:
  849|  		/*  Get keyboard/mouse ID.  NOTE/TODO: Ugly hardcoded answer.  */
  850|  		pckbc_add_code(d, KBR_ACK, port_nr);
  851|  		
  852|  		if (port_nr == 0) {
  853|  			// Keyboard:
  854|  			pckbc_add_code(d, 0xab, port_nr);
  855|+ 			/* #pckbcgetid: answer depends on translation mode */
  856|+ 			pckbc_add_code(d, d->translation_table ? 0x41 : 0x83, port_nr);
  857|  		} else {
  858|  			// Mouse:
  859|  			pckbc_add_code(d, 0x00, port_nr);
  860|  			pckbc_add_code(d, 0x00, port_nr);
  861|  		}
  862|  		break;
  863|  
  864|  	case KBC_TYPEMATIC:
  865|  		/*
  866|  		 *  Keyboard: Set typematic (auto-repeat) delay/speed.
  867|  		 *  PS/2 mouse: Set sample ratre.
  868|  		 */
  869|  		pckbc_add_code(d, KBR_ACK, port_nr);
  870|  		d->state[port_nr] = STATE_WAITING_FOR_RATE;
  871|  		break;
  872|  
  873|  	case KBC_ALLKEYS_TMB:
  874|  		/*  "Make all keys typematic/make/break"  */
  875|  		pckbc_add_code(d, KBR_ACK, port_nr);
  876|  		break;
  877|  
  878|  	case KBC_ONEKEY_MB:
  879|  		/*  "Make one key typematic/make/break"  */
  880|  		pckbc_add_code(d, KBR_ACK, port_nr);
  881|  		d->state[port_nr] = STATE_WAITING_FOR_ONEKEY_MB;
  882|  		break;
  883|  
  884|  	case KBC_RESET:
  885|  		pckbc_add_code(d, KBR_ACK, port_nr);
  886|  		pckbc_add_code(d, KBR_RSTDONE, port_nr);
  887|  
  888|  		if (port_nr == 1) {
  889|  			// Mouse (based on NetBSD's pckbport/pms.c) sends
  890|  			// mouse ID after RSTDONE:
  891|  			pckbc_add_code(d, 0x00, port_nr);
  892|  		}
  893|  
  894|  		/*
  895|  		 *  Disable interrupts during reset, or Linux 2.6
  896|  		 *  prints warnings about spurious interrupts.
  897|  		 */
  898|  		// d->rx_int_enable = 0;
  899|  		d->scanning_enabled[port_nr] = 0;
  900|  		break;
  901|  
  902|  	default:
  903|  		pckbc_add_code(d, KBR_RESEND, port_nr); // Error
  904|  		debugmsg(SUBSYS_DEVICE, "pckbc", VERBOSITY_WARNING,
  905|  		    "UNIMPLEMENTED command 0x%02x (port %i)", cmd, port_nr);
  906|  	}
  907|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PCKBCGETID: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PCKBCGETID: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
