# GXemul hardened fork -- DRAFT A FIX for one filed issue, `x11keycodes` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `x11keycodes`, state `open`, severity `MED`)

**title:** console/x11.c:x11_check_events_machine -- hard-coded pre-evdev keycodes: cursor/Home/End/PgUp/PgDn send nothing under evdev servers and several F-key sequences are wrong -- WRONG-RESULT (host input, -X)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T115 (class WRONG-RESULT; reach C, configuration, debugger, host environment or a non-default build; effort: small; report rows: A2-20).  Source URLs: https://github.com/rpajarola/gxemul/commit/1a27ff9330bbbde12fb174c1b529fb8a1211387c.  Our site at de8c7547: src/console/x11.c:839-900.  Portable fix: yes -- port rpajarola 1a27ff9.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 1a27ff9 to support evdev keycodes

## The code at the cited lines

### `src/console/x11.c` around the row's cited line 839 (HEAD d2a6f233, lines 794-884)

```c
  794| 						//    "RELEASE: unimplemented keycode %i", x);
  795| 				}
  796| 			}
  797| 
  798| 			if (event.type==KeyPress) {
  799| 				char text[15];
  800| 				KeySym key;
  801| 				XKeyPressedEvent *ke = &event.xkey;
  802| 
  803| 				memset(text, 0, sizeof(text));
  804| 
  805| 				if (XLookupString(&event.xkey, text,
  806| 				    sizeof(text), &key, 0) == 1) {
  807| 					console_makeavail(
  808| 					    m->main_console_handle, text[0]);
  809| 				} else {
  810| 					int x = ke->keycode;
  811| 					/*
  812| 					 *  Special key codes:
  813| 					 *
  814| 					 *  NOTE/TODO: I'm hardcoding these to
  815| 					 *  work with my key map. Maybe they
  816| 					 *  should be read from some file...
  817| 					 *
  818| 					 *  Important TODO 2:  It would be MUCH
  819| 					 *  better if these were converted into
  820| 					 *  'native scancodes', for example for
  821| 					 *  the DECstation's keyboard or the
  822| 					 *  PC-style 8042 controller.
  823| 					 */
  824| 					switch (x) {
  825| 					case 9:	/*  Escape  */
  826| 						console_makeavail(m->
  827| 						    main_console_handle, 27);
  828| 						break;
  829| #if 0
  830| 					/*  TODO  */
  831| 
  832| 					/*  The numeric keypad:  */
  833| 					90=Ins('0')  91=Del(',')
  834| 
  835| 					/*  Above the cursor keys:  */
  836| 					106=Ins  107=Del
  837| #endif
  838| 					/*  F1..F4:  */
  839| 					case 67:	/*  F1  */
  840| 					case 68:	/*  F2  */
  841| 					case 69:	/*  F3  */
  842| 					case 70:	/*  F4  */
  843| 						console_makeavail(m->
  844| 						    main_console_handle, 27);
  845| 						console_makeavail(m->
  846| 						    main_console_handle, '[');
  847| 						console_makeavail(m->
  848| 						    main_console_handle, 'O');
  849| 						console_makeavail(m->
  850| 						    main_console_handle, 'P' +
  851| 						    x - 67);
  852| 						break;
  853| 					case 71:	/*  F5  */
  854| 						console_makeavail(m->
  855| 						    main_console_handle, 27);
  856| 						console_makeavail(m->
  857| 						    main_console_handle, '[');
  858| 						console_makeavail(m->
  859| 						    main_console_handle, '1');
  860| 						console_makeavail(m->
  861| 						    main_console_handle, '5');
  862| 						break;
  863| 					case 72:	/*  F6  */
  864| 					case 73:	/*  F7  */
  865| 					case 74:	/*  F8  */
  866| 						console_makeavail(m->
  867| 						    main_console_handle, 27);
  868| 						console_makeavail(m->
  869| 						    main_console_handle, '[');
  870| 						console_makeavail(m->
  871| 						    main_console_handle, '1');
  872| 						console_makeavail(m->
  873| 						    main_console_handle, '7' +
  874| 						    x - 72);
  875| 						break;
  876| 					case 75:	/*  F9  */
  877| 					case 76:	/*  F10  */
  878| 						console_makeavail(m->
  879| 						    main_console_handle, 27);
  880| 						console_makeavail(m->
  881| 						    main_console_handle, '[');
  882| 						console_makeavail(m->
  883| 						    main_console_handle, '2');
  884| 						console_makeavail(m->
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

End with one line: `FIXDRAFT_X11KEYCODES: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
