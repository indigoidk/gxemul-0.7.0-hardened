# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pckbcledparam` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pckbcledparam`, state `open`, severity `MED`)

**title:** devices/dev_pckbc.c:dev_pckbc_command -- the Set-LEDs parameter byte is parsed as a new command (non-zero bytes get RESEND) -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T53 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-12).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/d2ff00eb9d9dc8e8b660672c9a155a8131cb2b20, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/c861ff6d1909a97715eddf7d30b8d8cabd352519.  Our site at de8c7547: src/devices/dev_pckbc.c:820-823, :812-818, :901-905.  Portable fix: yes -- port rs6000 d2ff00e, rs6000 c861ff6.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 d2ff00e, rs6000 c861ff6

## The code at the cited lines

### `src/devices/dev_pckbc.c` around the row's cited line 820 (HEAD d2a6f233, lines 775-865)

```c
  775| 
  776| 	if (d->state[port_nr] == STATE_WAITING_FOR_RATE) {
  777| 		debug("[ pckbc: (port %i) received Typematic/Sample Rate data: "
  778| 		    "0x%02x ]\n", port_nr, cmd);
  779| 		pckbc_add_code(d, KBR_ACK, port_nr);
  780| 		d->state[port_nr] = STATE_NORMAL;
  781| 		return;
  782| 	}
  783| 
  784| 	if (d->state[port_nr] == STATE_WAITING_FOR_ONEKEY_MB) {
  785| 		debug("[ pckbc: (port %i) received One-key make/break data: "
  786| 		    "0x%02x ]\n", port_nr, cmd);
  787| 		pckbc_add_code(d, KBR_ACK, port_nr);
  788| 		d->state[port_nr] = STATE_NORMAL;
  789| 		return;
  790| 	}
  791| 
  792| 	if (d->state[port_nr] == STATE_WAITING_FOR_AUX) {
  793| 		debug("[ pckbc: (port %i) received aux data: "
  794| 		    "0x%02x ]\n", port_nr, cmd);
  795| 		/*  Echo back.  */
  796| 		pckbc_add_code(d, cmd, port_nr);
  797| 		d->state[port_nr] = STATE_NORMAL;
  798| 		return;
  799| 	}
  800| 
  801| 	if (d->state[port_nr] == STATE_WAITING_FOR_AUX_OUT) {
  802| 		debug("[ pckbc: (port %i) received aux out data: "
  803| 		    "0x%02x ]\n", port_nr, cmd);
  804| 		/*  Echo back.  */
  805| 		pckbc_add_code(d, cmd, port_nr);
  806| 		d->state[port_nr] = STATE_NORMAL;
  807| 		return;
  808| 	}
  809| 
  810| 	switch (cmd) {
  811| 
  812| 	case 0x00:
  813| 		/*
  814| 		 *  TODO: What does this do? This is possibly due to an
  815| 		 *  error in the handling of some other command code.
  816| 		 */
  817| 		pckbc_add_code(d, KBR_ACK, port_nr);
  818| 		break;
  819| 
  820| 	case KBC_MODEIND:	/*  Set LEDs  */
  821| 		/*  Just ACK, no LEDs are actually set.  */
  822| 		pckbc_add_code(d, KBR_ACK, port_nr);
  823| 		break;
  824| 
  825| 	case KBC_ECHO:
  826| 		pckbc_add_code(d, KBR_ECHO, port_nr);
  827| 		break;
  828| 
  829| 	case KBC_SETTABLE:
  830| 		pckbc_add_code(d, KBR_ACK, port_nr);
  831| 		d->state[port_nr] = STATE_WAITING_FOR_TRANSLTABLE;
  832| 		break;
  833| 
  834| 	case KBC_ENABLE:
  835| 		d->scanning_enabled[port_nr] = 1;
  836| 		pckbc_add_code(d, KBR_ACK, port_nr);
  837| 		break;
  838| 
  839| 	case KBC_DISABLE:
  840| 		d->scanning_enabled[port_nr] = 0;
  841| 		pckbc_add_code(d, KBR_ACK, port_nr);
  842| 		break;
  843| 
  844| 	case KBC_SETDEFAULT:
  845| 		pckbc_add_code(d, KBR_ACK, port_nr);
  846| 		break;
  847| 
  848| 	case KBC_GETID:
  849| 		/*  Get keyboard/mouse ID.  NOTE/TODO: Ugly hardcoded answer.  */
  850| 		pckbc_add_code(d, KBR_ACK, port_nr);
  851| 		
  852| 		if (port_nr == 0) {
  853| 			// Keyboard:
  854| 			pckbc_add_code(d, 0xab, port_nr);
  855| 			pckbc_add_code(d, 0x41, port_nr);
  856| 		} else {
  857| 			// Mouse:
  858| 			pckbc_add_code(d, 0x00, port_nr);
  859| 			pckbc_add_code(d, 0x00, port_nr);
  860| 		}
  861| 		break;
  862| 
  863| 	case KBC_TYPEMATIC:
  864| 		/*
  865| 		 *  Keyboard: Set typematic (auto-repeat) delay/speed.
```

## The data structures those files define (every field that exists)

### `src/devices/dev_pckbc.c` -- `struct pckbc_data {` (HEAD lines 82-111)

```c
   82| struct pckbc_data {
   83| 	int		console_handle;
   84| 	int		in_use;
   85| 
   86| 	int		reg[DEV_PCKBC_LENGTH];
   87| 
   88| 	struct interrupt irq_keyboard;
   89| 	struct interrupt irq_mouse;
   90| 	int		currently_asserted[2];
   91| 	int		type;
   92| 	int		pc_style_flag;
   93| 
   94| 	/*  TODO: one of these for each port?  */
   95| 	int		clocksignal;
   96| 	int		rx_int_enable[2];
   97| 	int		tx_int_enable[2];
   98| 
   99| 	int		scanning_enabled[2];
  100| 	int		translation_table;
  101| 	int		state[2];
  102| 	int		cmdbyte;
  103| 	int		output_byte;
  104| 	int		last_scancode;
  105| 
  106| 	unsigned	key_queue[2][MAX_8042_QUEUELEN];
  107| 	int		head[2], tail[2];
  108| 	int		overrun_warned[2];	/*  #288  */
  109| 
  110| 	int		mouse_buttons;
  111| };
```

RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_PCKBCLEDPARAM: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
