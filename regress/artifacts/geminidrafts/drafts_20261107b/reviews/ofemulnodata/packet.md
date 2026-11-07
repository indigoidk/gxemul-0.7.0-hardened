# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ofemulnodata` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ofemulnodata`, state `open`)

**title:** src/promemul/of.c of_emul(): the OpenFirmware emulation entry calls fatal() + exit(1) when machine->md.of_data is NULL, which is true on every machine except macppc with PROM emulation on (machine_macppc.c returns before of_emul_init when it is off) -- and the ARM and PowerPC decoders route their OpenFirmware magic instruction to it with no machine or privilege check

**state_note (head):** filed 2026-10-16 from the adjudication of the agy pack's second readings (packet D, H1): all three seats FILE, HIGH, own row (regress/artifacts/adj_20261016/astra/D_secondreadings/codex_adjD.txt, grok/D_secondreadings/grok_adjD.txt, fable5/fable5_adj_D_secondreadings_v2_FABLE.md).  Source: prescreen_audits5.md of_two/F9.  READ at HEAD by all three: of.c:1096-1101 (the NULL check and the exit), :1078 (the only writer, of_emul_init, called only from machine_macppc.c:99); ARM decode cpu_arm_instr.c:5034-5036 -> X(openfirmware) :988-991; PowerPC decode cpu_ppc_instr.c:4400-4402 -> X(openfirmware) :3956-3958.  A guest instruction therefore ends the emulator process on machines that never set up OpenFirmware.  Not covered by ofopenexit or ofpeerexit (other sites in the same file); Fable 5.1: may share one round with them.  A rung-3 ATTEMPT exists, made by claude-opus-4-8 in the Fable seat's fallback run (so it is not a Fable ruling and owes review before it counts as the witness): regress/artifacts/adj_20261016/fable5/meas_D/witness_hostexit.py and .out, at HEAD e483d931 on the unmodified ARM test machine (the emulator prints `of_emul(): no of_data struct?' and the process exits 1), each with a benign-instruction liveness control that stays alive. ||  [2026-10-21] ARGON SCOPING (packet-fed, a reading not a measurement; regress/artifacts/ofemulnodata/argon_scope_20261021/gemini_web.out, dispositions DISPOSITIONS.md): THREE rounds, not one -- of.c:1100 (this row), :394 (ofpeerexit) and :448 (ofopenexit) differ in semantic class, fix design and detector (the round-scope rule); of.c:549, :577, :1120 and :1201 are UNREACHABLE (machine-setup helpers; arch-switch defaults only ARM and PowerPC reach).  DESIGN for this row: gate the magic word at the DECODERS (cpu_arm_instr.c's SWI case, cpu_ppc_instr.c's sc case) on `cpu->machine->md.of_data != NULL`, so a machine without OpenFirmware executes the word as the architectural SWI / system call it encodes (FAULT) -- NOT an early return inside of_emul, whose callers' tails then jump to the link register as if the call had returned.  Detector: the SWI-exception row on an ARM machine, the sc-exception rows on a non-macppc PowerPC machine and on macppc without PROM emulation, and macppc-with-PROM-emulation accept rows (an OF service still answers).  The title was corrected the same day: macppc without PROM emulation also has of_data NULL (read at machine_macppc.c's `if (!machine->prom_emulation) return;` before of_emul_init).

**The drafter's own reading:** STILL PRESENT: YES -- `src/promemul/of.c:1098`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/promemul/of.c b/src/promemul/of.c
index 85dcc76a..d750c8a6 100644
--- a/src/promemul/of.c
+++ b/src/promemul/of.c
@@ -1096,8 +1096,13 @@ int of_emul(struct cpu *cpu)
 	struct of_data *of_data = cpu->machine->md.of_data;
 
 	if (of_data == NULL) {
-		fatal("of_emul(): no of_data struct?\n");
-		exit(1);
+		/* #3399: guest-reachable diagnostic must not exit */
+		static int warned = 0;
+		if (!warned) {
+			fatal("of_emul(): no of_data struct? (once)\n");
+			warned = 1;
+		}
+		return 0;
 	}
 
 	/*
```

## Every edited function, after the fix

### `src/promemul/of.c` -- post-edit lines 1089-1210 (`+` marks a line the diff added or the point of a deletion)

```c
 1089|  int of_emul(struct cpu *cpu)
 1090|  {
 1091|  	int i, nargs, nret, ofs, retval = 0;
 1092|  	char service[50];
 1093|  	char *arg[OF_N_MAX_ARGS];
 1094|  	uint64_t base, ptr;
 1095|  	struct of_service *os;
 1096|  	struct of_data *of_data = cpu->machine->md.of_data;
 1097|  
 1098|  	if (of_data == NULL) {
 1099|+ 		/* #3399: guest-reachable diagnostic must not exit */
 1100|+ 		static int warned = 0;
 1101|+ 		if (!warned) {
 1102|+ 			fatal("of_emul(): no of_data struct? (once)\n");
 1103|+ 			warned = 1;
 1104|+ 		}
 1105|+ 		return 0;
 1106|  	}
 1107|  
 1108|  	/*
 1109|  	 *  The first argument register points to "prom_args":
 1110|  	 *
 1111|  	 *	char *service;		(probably 32 bit)
 1112|  	 *	int nargs;
 1113|  	 *	int nret;
 1114|  	 *	char *args[10];
 1115|  	 */
 1116|  
 1117|  	switch (cpu->cpu_family->arch) {
 1118|  	case ARCH_ARM:
 1119|  		base = cpu->cd.arm.r[0];
 1120|  		break;
 1121|  	case ARCH_PPC:
 1122|  		base = cpu->cd.ppc.gpr[3];
 1123|  		break;
 1124|  	default:fatal("of_emul(): unimplemented arch (TODO)\n");
 1125|  		exit(1);
 1126|  	}
 1127|  
 1128|  	/*  TODO: how about 64-bit OpenFirmware?  */
 1129|  	ptr   = load_32bit_word(cpu, base);
 1130|  	nargs = load_32bit_word(cpu, base + 4);
 1131|  	nret  = load_32bit_word(cpu, base + 8);
 1132|  
 1133|  	/*  #201: (Codex/Fable) nargs is guest-controlled; clamp it so the
 1134|  	    arg loop below can't run up to ~2^31 times (log flood / host
 1135|  	    hang). Args past OF_N_MAX_ARGS are ignored anyway.  */
 1136|  	if (nargs > OF_N_MAX_ARGS)
 1137|  		nargs = OF_N_MAX_ARGS;
 1138|  
 1139|  	readstr(cpu, ptr, service, sizeof(service));
 1140|  
 1141|  	debug("[ of: %s(", service);
 1142|  	ofs = 12;
 1143|  	for (i=0; i<nargs; i++) {
 1144|  		int x;
 1145|  		if (i > 0)
 1146|  			debug(", ");
 1147|  		if (i >= OF_N_MAX_ARGS) {
 1148|  			fatal("TOO MANY ARGS!");
 1149|  			continue;
 1150|  		}
 1151|  
 1152|  		ptr = load_32bit_word(cpu, base + ofs);
 1153|  
 1154|  		CHECK_ALLOCATION(arg[i] = (char *) malloc(OF_ARG_MAX_LEN + 1));
 1155|  		memset(arg[i], 0, OF_ARG_MAX_LEN + 1);
 1156|  
 1157|  		x = ptr;
 1158|  		if (x > -256 && x < 256) {
 1159|  			debug("%i", x);
 1160|  		} else {
 1161|  			readstr(cpu, ptr, arg[i], OF_ARG_MAX_LEN);
 1162|  			if (arg[i][0])
 1163|  				debug("\"%s\"", arg[i]);
 1164|  			else
 1165|  				debug("0x%x", x);
 1166|  		}
 1167|  		ofs += sizeof(uint32_t);
 1168|  	}
 1169|  	debug(") ]\n");
 1170|  
 1171|  	/*  Note: base + ofs points to the first return slot.  */
 1172|  
 1173|  	os = of_data->of_services;
 1174|  	while (os != NULL) {
 1175|  		if (strcmp(service, os->name) == 0 &&
 1176|  		    nargs == os->n_args && nret == os->n_ret_args) {
 1177|  			retval = os->f(cpu, arg, base, ofs);
 1178|  			break;
 1179|  		}
 1180|  		os = os->next;
 1181|  	}
 1182|  
 1183|  	if (os == NULL) {
 1184|  		quiet_mode = 0;
 1185|  		cpu_register_dump(cpu->machine, cpu, 1, 0);
 1186|  		printf("\n");
 1187|  		fatal("[ of: unimplemented service \"%s\" with %i input "
 1188|  		    "args and %i output values ]\n", service, nargs, nret);
 1189|  		/*  #219: (Codex/Fable) cpu->running=0 already halts cleanly for an
 1190|  		    unknown guest OF service; the exit(1) only defeats the debugger.  */
 1191|  		cpu->running = 0;
 1192|  	}
 1193|  
 1194|  	for (i=0; i<nargs; i++)
 1195|  		free(arg[i]);
 1196|  
 1197|  	/*  Return:  */
 1198|  	switch (cpu->cpu_family->arch) {
 1199|  	case ARCH_ARM:
 1200|  		cpu->cd.arm.r[0] = retval;
 1201|  		break;
 1202|  	case ARCH_PPC:
 1203|  		cpu->cd.ppc.gpr[3] = retval;
 1204|  		break;
 1205|  	default:fatal("of_emul(): TODO: unimplemented arch (Retval)\n");
 1206|  		exit(1);
 1207|  	}
 1208|  
 1209|  	return 1;
 1210|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_OFEMULNODATA: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_OFEMULNODATA: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
