# GXemul hardened fork -- DRAFT A FIX for one filed issue, `m88kaluignored` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `m88kaluignored`, state `open`, severity `LOW`)

**title:** src/cpus/cpu_m88k_instr.c:3660,3815 -- the register-form switch keys on bits 15:8, so a divu, mul, div or cmp word with nonzero bits 9:8, which the MC88100 does not decode, finds no case and reaches goto bad, stopping the CPU -- CPU-STOP

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Malformed undecoded input crashes the emulator via goto bad, violating robustness goals.

## The code at the cited lines

### `src/cpus/cpu_m88k_instr.c` around the row's cited line 3660 (HEAD d2a6f233, lines 3615-3705)

```c
 3615| 
 3616| 			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3617| 			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3618| 			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3619| 
 3620| 			if (op == 0 || op == 1) {
 3621| 				/*  ld or st:  */
 3622| 				ic->f = m88k_loadstore[ opsize
 3623| 				    + (op==1? M88K_LOADSTORE_STORE : 0)
 3624| 				    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
 3625| 				    + (cpu->byte_order == EMUL_BIG_ENDIAN?
 3626| 				       M88K_LOADSTORE_ENDIANNESS : 0)
 3627| 				    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
 3628| 				    + (user? M88K_LOADSTORE_USR : 0)
 3629| 				    + M88K_LOADSTORE_REGISTEROFFSET ];
 3630| 
 3631| 				if (d == M88K_ZERO_REG && op == 0)
 3632| 					ic->arg[0] = (size_t)&cpu->cd.m88k.zero_scratch;
 3633| 
 3634| 				if (opsize == 3 && d == 31) {
 3635| 					fatal("m88k load/store of register "
 3636| 					    "pair r31/r0: TODO\n");
 3637| 					goto bad;
 3638| 				}
 3639| 			} else if (op == 2) {
 3640| 				/*  lda:  */
 3641| 				if (scaled) {
 3642| 					switch (opsize) {
 3643| 					case 0: ic->f = instr(addu); break;
 3644| 					case 1: ic->f = instr(lda_reg_2); break;
 3645| 					case 2: ic->f = instr(lda_reg_4); break;
 3646| 					case 3: ic->f = instr(lda_reg_8); break;
 3647| 					}
 3648| 				} else {
 3649| 					ic->f = instr(addu);
 3650| 				}
 3651| 				if (d == M88K_ZERO_REG)
 3652| 					ic->f = instr(nop);
 3653| 			} else {
 3654| 				/*  xmem:  */
 3655| 				ic->f = instr(xmem_slow);
 3656| 				ic->arg[0] = iword;
 3657| 				if (d == M88K_ZERO_REG)
 3658| 					ic->f = instr(nop);
 3659| 			}
 3660| 		} else switch ((iword >> 8) & 0xff) {
 3661| 		case 0x40:	/*  and    */
 3662| 		case 0x44:	/*  and.c  */
 3663| 		case 0x50:	/*  xor    */
 3664| 		case 0x54:	/*  xor.c  */
 3665| 		case 0x58:	/*  or     */
 3666| 		case 0x5c:	/*  or.c   */
 3667| 		case 0x60:	/*  addu   */
 3668| 		case 0x61:	/*  addu.co  */
 3669| 		case 0x62:	/*  addu.ci  */
 3670| 		case 0x63:	/*  addu.cio */
 3671| 		case 0x64:	/*  subu   */
 3672| 		case 0x65:	/*  subu.co  */
 3673| 		case 0x66:	/*  subu.ci  */
 3674| 		case 0x67:	/*  subu.cio */
 3675| 		case 0x68:	/*  divu   */
 3676| 		case 0x6c:	/*  mul    */
 3677| 		case 0x70:	/*  add    */
 3678| 		case 0x78:	/*  div    */
 3679| 		case 0x7c:	/*  cmp    */
 3680| 		case 0x80:	/*  clr    */
 3681| 		case 0x88:	/*  set    */
 3682| 		case 0x90:	/*  ext    */
 3683| 		case 0x98:	/*  extu   */
 3684| 		case 0xa0:	/*  mak    */
 3685| 		case 0xa8:	/*  rot    */
 3686| 			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3687| 			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3688| 			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3689| 
 3690| 			switch ((iword >> 8) & 0xff) {
 3691| 			case 0x40: ic->f = instr(and);   break;
 3692| 			case 0x44: ic->f = instr(and_c); break;
 3693| 			case 0x50: ic->f = instr(xor);   break;
 3694| 			case 0x54: ic->f = instr(xor_c); break;
 3695| 			case 0x58: ic->f = instr(or);    break;
 3696| 			case 0x5c: ic->f = instr(or_c);  break;
 3697| 			case 0x60: ic->f = instr(addu);  break;
 3698| 			case 0x61: ic->f = instr(addu_co); break;
 3699| 			case 0x62: ic->f = instr(addu_ci); break;
 3700| 			case 0x63: ic->f = instr(addu_cio); break;
 3701| 			case 0x64: ic->f = instr(subu);  break;
 3702| 			case 0x65: ic->f = instr(subu_co); break;
 3703| 			case 0x66: ic->f = instr(subu_ci); break;
 3704| 			case 0x67: ic->f = instr(subu_cio); break;
 3705| 			case 0x68: ic->f = instr(divu);  break;
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

End with one line: `FIXDRAFT_M88KALUIGNORED: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL  edit 2 src/cpus/cpu_m88k_instr.c: old occurs 3 times
```

The previous edits:

```json
[
  {
    "file": "src/cpus/cpu_m88k_instr.c",
    "old": "\t\t} else switch ((iword >> 8) & 0xff) {",
    "new": "\t\t} else switch ((((iword >> 8) & 0xfc) == 0x68 ||\n\t\t    ((iword >> 8) & 0xfc) == 0x6c || ((iword >> 8) & 0xfc) == 0x78 ||\n\t\t    ((iword >> 8) & 0xfc) == 0x7c) ?\n\t\t    ((iword >> 8) & 0xfc) : ((iword >> 8) & 0xff)) { /* #m88kaluignored: mask bits 9:8 */",
    "why": "Mask bits 9:8 (which the MC88100 leaves undecoded for divu, mul, div, cmp) so they route to the correct case."
  },
  {
    "file": "src/cpus/cpu_m88k_instr.c",
    "old": "\t\t\tswitch ((iword >> 8) & 0xff) {",
    "new": "\t\t\tswitch ((((iword >> 8) & 0xfc) == 0x68 ||\n\t\t\t    ((iword >> 8) & 0xfc) == 0x6c || ((iword >> 8) & 0xfc) == 0x78 ||\n\t\t\t    ((iword >> 8) & 0xfc) == 0x7c) ?\n\t\t\t    ((iword >> 8) & 0xfc) : ((iword >> 8) & 0xff)) { /* #m88kaluignored: mask bits 9:8 */",
    "why": "Apply the same mask to the secondary switch to ensure it binds the correct handler."
  }
]
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
