/*
 *  Copyright (C) 2004-2021  Anders Gavare.  All rights reserved.
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
 *  Debugger commands. Included from debugger.c.
 */


/*
 *  debugger_cmd_allsettings():
 */
static void debugger_cmd_allsettings(struct machine *m, char *args)
{
	settings_debugdump(global_settings, GLOBAL_SETTINGS_NAME, 1);
}


/*
 *  debugger_cmd_breakpoint():
 *
 *  The subcommand name may be abbreviated to any unambiguous prefix,
 *  e.g. "breakpoint s" == "breakpoint show".
 */
static void debugger_cmd_breakpoint(struct machine *m, char *args)
{
	static const char *subcmd_name[] = { "add", "delete", "show",
	    "subsystem" };
	const int SUBCMD_ADD = 0, SUBCMD_DELETE = 1, SUBCMD_SHOW = 2,
	    SUBCMD_SUBSYSTEM = 3;
	const int n_subcmds = 4;
	int i, res, subcmd = -1, n_matches = 0;
	size_t wordlen;
	char *rest;

	while (args[0] != '\0' && args[0] == ' ')
		args ++;

	if (args[0] == '\0') {
		printf("syntax: breakpoint subcmd [args...]\n");
		printf("Available subcmds (and args) are:\n");
		printf("  add addr[, N] add a breakpoint for address addr"
		    " (N = ignore first N hits)\n");
		printf("  delete x      delete breakpoint nr x\n");
		printf("  show          show current breakpoints\n");
		printf("  subsystem [name error|warning|info|debug|off]\n");
		printf("                show or set breakpoints on subsystem"
		    " messages\n");
		printf("Subcmds may be abbreviated to any unambiguous prefix,"
		    " e.g. \"breakpoint sh\".\n");
		return;
	}

	/*  The first word of args is the subcommand. It may be abbreviated
	    to any prefix which matches exactly one of the subcommands:  */
	wordlen = 0;
	while (args[wordlen] != '\0' && args[wordlen] != ' ')
		wordlen ++;

	for (i=0; i<n_subcmds; i++)
		if (strncasecmp(args, subcmd_name[i], wordlen) == 0) {
			subcmd = i;
			n_matches ++;
		}

	if (n_matches == 0) {
		printf("Unknown breakpoint subcommand.\n");
		return;
	}
	if (n_matches > 1) {
		printf("Ambiguous breakpoint subcommand '%.*s'.\n",
		    (int) wordlen, args);
		return;
	}

	/*  Any arguments to the subcommand follow after the first word:  */
	rest = args + wordlen;
	while (rest[0] != '\0' && rest[0] == ' ')
		rest ++;

	if (subcmd == SUBCMD_SHOW) {
		if (rest[0] != '\0') {
			printf("syntax: breakpoint show\n");
			return;
		}
		if (m->breakpoints.n == 0)
			printf("No breakpoints set.\n");
		for (i=0; i<m->breakpoints.n; i++)
			show_breakpoint(m, i);
		return;
	}

	if (subcmd == SUBCMD_DELETE) {
		int x;

		if (rest[0] == '\0') {
			printf("syntax: breakpoint delete x\n");
			return;
		}

		x = atoi(rest);

		if (m->breakpoints.n == 0) {
			printf("No breakpoints set.\n");
			return;
		}
		if (x < 0 || x >= m->breakpoints.n) {
			printf("Invalid breakpoint nr %i. Use 'breakpoint "
			    "show' to see the current breakpoints.\n", x);
			return;
		}

		free(m->breakpoints.string[x]);

		for (i=x; i<m->breakpoints.n-1; i++) {
			m->breakpoints.addr[i]   = m->breakpoints.addr[i+1];
			m->breakpoints.string[i] = m->breakpoints.string[i+1];
			/*  #248: keep hit accounting in lockstep.  */
			m->breakpoints.hitcount[i]    =
			    m->breakpoints.hitcount[i+1];
			m->breakpoints.ignore_left[i] =
			    m->breakpoints.ignore_left[i+1];
		}
		m->breakpoints.n --;

		/*  Clear translations:  */
		for (i=0; i<m->ncpus; i++)
			if (m->cpus[i]->translation_cache != NULL)
				cpu_create_or_reset_tc(m->cpus[i]);
		return;
	}

	if (subcmd == SUBCMD_ADD) {
		uint64_t tmp;
		size_t breakpoint_buf_len;
		int64_t ignore = 0;		/*  #248  */
		char *comma;			/*  #248  */

		if (rest[0] == '\0') {
			printf("syntax: breakpoint add addr[, ignorecount]\n");
			return;
		}

		/*  #248: an optional ", N" tail means "run past the first N
		    hits before breaking" (skip boot noise / stop on the Nth
		    iteration). Address expressions never contain a comma.  */
		comma = strchr(rest, ',');
		if (comma != NULL) {
			*comma = '\0';
			ignore = strtoll(comma + 1, NULL, 0);
			if (ignore < 0)
				ignore = 0;
			while (comma > rest && comma[-1] == ' ')
				*(--comma) = '\0';
		}

		i = m->breakpoints.n;

		res = debugger_parse_expression(m, rest, 0, &tmp);
		if (!res) {
			printf("Couldn't parse '%s'\n", rest);
			return;
		}

		/*  #256: mirror add_breakpoints() (emul.c). The address is
		    parsed with writeflag=0, so debugger_parse_name() skips its
		    MIPS sign-extension. Un-extended, a kseg0/kseg1 breakpoint
		    never equals the sign-extended pc on a 64-bit-mode MIPS core
		    (R4000+/arc); 32-bit mode (R3000/pmax) masks it by truncating
		    both sides of the compare, so it only bit the arc rig.  */
		if (m->cpus[0]->cpu_family->arch == ARCH_MIPS) {
			if ((tmp >> 32) == 0 && ((tmp >> 31) & 1))
				tmp |= 0xffffffff00000000ULL;
		}

		CHECK_ALLOCATION(m->breakpoints.string = (char **) realloc(
		    m->breakpoints.string, sizeof(char *) *
		    (m->breakpoints.n + 1)));
		CHECK_ALLOCATION(m->breakpoints.addr = (uint64_t *) realloc(
		    m->breakpoints.addr, sizeof(uint64_t) *
		   (m->breakpoints.n + 1)));
		/*  #248: keep the hit-accounting arrays in lockstep.  */
		CHECK_ALLOCATION(m->breakpoints.hitcount = (uint64_t *) realloc(
		    m->breakpoints.hitcount, sizeof(uint64_t) *
		   (m->breakpoints.n + 1)));
		CHECK_ALLOCATION(m->breakpoints.ignore_left = (int64_t *)
		    realloc(m->breakpoints.ignore_left, sizeof(int64_t) *
		   (m->breakpoints.n + 1)));

		breakpoint_buf_len = strlen(rest) + 1;

		CHECK_ALLOCATION(m->breakpoints.string[i] = (char *)
		    malloc(breakpoint_buf_len));
		strlcpy(m->breakpoints.string[i], rest,
		    breakpoint_buf_len);
		m->breakpoints.addr[i] = tmp;
		m->breakpoints.hitcount[i] = 0;		/*  #248  */
		m->breakpoints.ignore_left[i] = ignore;	/*  #248  */

		m->breakpoints.n ++;
		show_breakpoint(m, i);

		/*  Clear translations:  */
		for (i=0; i<m->ncpus; i++)
			if (m->cpus[i]->translation_cache != NULL)
				cpu_create_or_reset_tc(m->cpus[i]);
		return;
	}

	if (subcmd == SUBCMD_SUBSYSTEM) {
		static const char *level_name[] = { "error", "warning",
		    "info", "debug", "off" };
		const int level_value[] = { VERBOSITY_ERROR,
		    VERBOSITY_WARNING, VERBOSITY_INFO, VERBOSITY_DEBUG, -1 };
		const int n_levels = 5;
		char *name, *level_word, *p;
		int level = -1, n_level_matches = 0;

		if (rest[0] == '\0') {
			debugmsg_print_breakpoints();
			return;
		}

		/*  The first word is the subsystem name, the second word
		    is the level. The level word may be abbreviated to any
		    unambiguous prefix, e.g. "warn" == "warning".  */
		name = rest;
		wordlen = 0;
		while (name[wordlen] != '\0' && name[wordlen] != ' ')
			wordlen ++;
		level_word = name + wordlen;
		if (level_word[0] == ' ') {
			*level_word++ = '\0';
			while (level_word[0] == ' ')
				level_word ++;
		}

		wordlen = 0;
		while (level_word[wordlen] != '\0' && level_word[wordlen] != ' ')
			wordlen ++;
		p = level_word + wordlen;
		while (p[0] == ' ')
			p ++;

		if (level_word[0] == '\0' || p[0] != '\0') {
			printf("syntax: breakpoint subsystem name "
			    "error|warning|info|debug|off\n");
			return;
		}

		for (i=0; i<n_levels; i++)
			if (strncasecmp(level_word, level_name[i],
			    wordlen) == 0) {
				level = level_value[i];
				n_level_matches ++;
			}

		if (n_level_matches != 1) {
			printf("%s breakpoint level '%.*s'. Levels are: "
			    "error, warning, info, debug, off.\n",
			    n_level_matches == 0 ? "Unknown" : "Ambiguous",
			    (int) wordlen, level_word);
			return;
		}

		if (!debugmsg_set_breakpoint(name, level)) {
			printf("Unknown subsystem name '%s'. Use the "
			    "'verbosity' command to see the list of "
			    "subsystems.\n", name);
			return;
		}

		debugmsg_print_breakpoints();
		return;
	}
}


/*
 *  debugger_cmd_watchpoint():
 *
 *  #250: manipulate data write-watchpoints. A watchpoint breaks into the
 *  debugger when the guest writes to a watched (virtual) address range —
 *  the missing primitive for tracking down who corrupts a heap/GOT/pointer
 *  cell. Modelled on debugger_cmd_breakpoint().
 */
static void debugger_cmd_watchpoint(struct machine *m, char *args)
{
	static const char *subcmd_name[] = { "add", "delete", "show" };
	const int SUBCMD_ADD = 0, SUBCMD_DELETE = 1, SUBCMD_SHOW = 2;
	const int n_subcmds = 3;
	int i, res, subcmd = -1, n_matches = 0;
	size_t wordlen;
	char *rest;

	while (args[0] == ' ')
		args ++;

	if (args[0] == '\0') {
		printf("syntax: watchpoint subcmd [args...]\n");
		printf("Available subcmds (and args) are:\n");
		printf("  add addr[, len]  break on a guest write to the len-byte"
		    " range at addr\n");
		printf("                   (len defaults to 4)\n");
		printf("  delete x         delete watchpoint nr x\n");
		printf("  show             show current watchpoints\n");
		printf("Subcmds may be abbreviated to any unambiguous prefix.\n");
		return;
	}

	wordlen = 0;
	while (args[wordlen] != '\0' && args[wordlen] != ' ')
		wordlen ++;

	for (i=0; i<n_subcmds; i++)
		if (strncasecmp(args, subcmd_name[i], wordlen) == 0) {
			subcmd = i;
			n_matches ++;
		}

	if (n_matches == 0) {
		printf("Unknown watchpoint subcommand.\n");
		return;
	}
	if (n_matches > 1) {
		printf("Ambiguous watchpoint subcommand '%.*s'.\n",
		    (int) wordlen, args);
		return;
	}

	rest = args + wordlen;
	while (rest[0] == ' ')
		rest ++;

	if (subcmd == SUBCMD_SHOW) {
		if (m->watchpoints.n == 0)
			printf("No watchpoints set.\n");
		for (i=0; i<m->watchpoints.n; i++) {
			printf("%3i: paddr 0x", i);
			if (m->cpus[0]->is_32bit)
				printf("%08" PRIx32,
				    (uint32_t) m->watchpoints.addr[i]);
			else
				printf("%016" PRIx64,
				    (uint64_t) m->watchpoints.addr[i]);
			printf(", %" PRIi64 " byte(s)",
			    (int64_t) m->watchpoints.len[i]);
			if (m->watchpoints.string[i] != NULL)
				printf(" (%s)", m->watchpoints.string[i]);
			printf("\n");
		}
		return;
	}

	if (subcmd == SUBCMD_DELETE) {
		int x;

		if (rest[0] == '\0') {
			printf("syntax: watchpoint delete x\n");
			return;
		}

		x = atoi(rest);

		if (m->watchpoints.n == 0) {
			printf("No watchpoints set.\n");
			return;
		}
		if (x < 0 || x >= m->watchpoints.n) {
			printf("Invalid watchpoint nr %i. Use 'watchpoint "
			    "show' to see the current watchpoints.\n", x);
			return;
		}

		free(m->watchpoints.string[x]);

		for (i=x; i<m->watchpoints.n-1; i++) {
			m->watchpoints.addr[i]   = m->watchpoints.addr[i+1];
			m->watchpoints.len[i]    = m->watchpoints.len[i+1];
			m->watchpoints.string[i] = m->watchpoints.string[i+1];
		}
		m->watchpoints.n --;

		/*  Invalidate ALL translations (incl. the host_store data map)
		    so the fast-store suppression is recomputed on remap.  */
		for (i=0; i<m->ncpus; i++)
			if (m->cpus[i]->invalidate_translation_caches != NULL)
				m->cpus[i]->invalidate_translation_caches(
				    m->cpus[i], 0, INVALIDATE_ALL);
		return;
	}

	if (subcmd == SUBCMD_ADD) {
		uint64_t addr, paddr, len = 4;
		size_t buflen;
		char *comma;
		struct cpu *c;

		if (rest[0] == '\0') {
			printf("syntax: watchpoint add addr[, len]\n");
			return;
		}

		/*  Optional ", len" tail; expressions never contain a comma.  */
		comma = strchr(rest, ',');
		if (comma != NULL) {
			*comma = '\0';
			len = strtoull(comma + 1, NULL, 0);
			if (len < 1)
				len = 1;
			while (comma > rest && comma[-1] == ' ')
				*(--comma) = '\0';
		}

		res = debugger_parse_expression(m, rest, 0, &addr);
		if (!res) {
			printf("Couldn't parse '%s'\n", rest);
			return;
		}

		/*
		 *  #250: watchpoints are matched on PHYSICAL addresses, so a
		 *  write via any virtual alias (e.g. cached kseg0 vs uncached
		 *  kseg1 on MIPS) is caught and 32-bit sign-extension is a
		 *  non-issue. Translate the (virtual) address the user typed to
		 *  physical; if that fails (e.g. an unmapped mapped-segment
		 *  address), assume the value was already physical.
		 */
		c = m->cpus[m->bootstrap_cpu];
		paddr = addr;
		if (c != NULL && c->translate_v2p != NULL &&
		    !c->translate_v2p(c, addr, &paddr, FLAG_NOEXCEPTIONS)) {
			printf("(warning: couldn't translate 0x%" PRIx64 " to a "
			    "physical address; treating it as physical)\n",
			    (uint64_t) addr);
			paddr = addr;
		}

		i = m->watchpoints.n;

		CHECK_ALLOCATION(m->watchpoints.string = (char **) realloc(
		    m->watchpoints.string, sizeof(char *) * (i + 1)));
		CHECK_ALLOCATION(m->watchpoints.addr = (uint64_t *) realloc(
		    m->watchpoints.addr, sizeof(uint64_t) * (i + 1)));
		CHECK_ALLOCATION(m->watchpoints.len = (uint64_t *) realloc(
		    m->watchpoints.len, sizeof(uint64_t) * (i + 1)));

		buflen = strlen(rest) + 1;
		CHECK_ALLOCATION(m->watchpoints.string[i] = (char *)
		    malloc(buflen));
		strlcpy(m->watchpoints.string[i], rest, buflen);
		m->watchpoints.addr[i] = paddr;
		m->watchpoints.len[i] = len;
		m->watchpoints.n ++;

		/*  Invalidate ALL translations (incl. the host_store data map)
		    so the newly-watched page leaves the fast-store map and every
		    write to it now traps to memory_rw.  */
		for (i=0; i<m->ncpus; i++)
			if (m->cpus[i]->invalidate_translation_caches != NULL)
				m->cpus[i]->invalidate_translation_caches(
				    m->cpus[i], 0, INVALIDATE_ALL);

		printf("watchpoint %i: paddr 0x%" PRIx64 ", %" PRIi64
		    " byte(s) (%s)\n", m->watchpoints.n - 1, (uint64_t) paddr,
		    (int64_t) len, m->watchpoints.string[m->watchpoints.n - 1]);
		return;
	}
}


/*
 *  debugger_cmd_continue():
 */
static void debugger_cmd_continue(struct machine *m, char *args)
{
	if (*args) {
		printf("syntax: continue\n");
		return;
	}

	exit_debugger = true;
}


/*
 *  debugger_cmd_device():
 */
static void debugger_cmd_device(struct machine *m, char *args)
{
	int i;
	struct memory *mem;
	struct cpu *c;

	if (args[0] == '\0')
		goto return_help;

	if (m->cpus == NULL) {
		printf("No cpus (?)\n");
		return;
	}
	c = m->cpus[m->bootstrap_cpu];
	if (c == NULL) {
		printf("m->cpus[m->bootstrap_cpu] = NULL\n");
		return;
	}
	mem = m->cpus[m->bootstrap_cpu]->mem;

	if (m->cpus == NULL) {
		printf("No cpus (?)\n");
		return;
	}
	c = m->cpus[m->bootstrap_cpu];
	if (c == NULL) {
		printf("m->cpus[m->bootstrap_cpu] = NULL\n");
		return;
	}
	mem = m->cpus[m->bootstrap_cpu]->mem;

	if (strcmp(args, "all") == 0) {
		device_dumplist();
	} else if (strncmp(args, "add ", 4) == 0) {
		device_add(m, args+4);
	} else if (strcmp(args, "consoles") == 0) {
		console_debug_dump(m);
	} else if (strncmp(args, "remove ", 7) == 0) {
		i = atoi(args + 7);
		if (i==0 && args[7]!='0') {
			printf("Weird device number. Use 'device list'.\n");
		} else
			memory_device_remove(m->memory, i);
	} else if (strcmp(args, "list") == 0) {
		if (mem->n_mmapped_devices == 0)
			printf("No memory-mapped devices in this machine.\n");

		for (i=0; i<mem->n_mmapped_devices; i++) {
			printf("%2i: %25s @ 0x%011" PRIx64", len = 0x%" PRIx64,
			    i, mem->devices[i].name,
			    (uint64_t) mem->devices[i].baseaddr,
			    (uint64_t) mem->devices[i].length);

			if (mem->devices[i].flags) {
				printf(" (");
				if (mem->devices[i].flags & DM_DYNTRANS_OK)
					printf("DYNTRANS R");
				if (mem->devices[i].flags &DM_DYNTRANS_WRITE_OK)
					printf("+W");
				printf(")");
			}
			printf("\n");
		}
	} else
		goto return_help;

	return;

return_help:
	printf("syntax: devices cmd [...]\n");
	printf("Available cmds are:\n");
	printf("  add name_and_params    add a device to the current "
	    "machine\n");
	printf("  all                    list all registered devices\n");
	printf("  consoles               list all slave consoles\n");
	printf("  list                   list memory-mapped devices in the"
	    " current machine\n");
	printf("  remove x               remove device nr x from the "
	    "current machine\n");
}


/*
 *  debugger_addr_range_separator():
 *
 *  Helper for commands taking an "addr [endaddr]" argument string (dump
 *  and unassemble). Returns a pointer to the space character in s which
 *  separates the addr expression from the endaddr expression, or NULL if
 *  s contains only a single expression.
 *
 *  A space is only treated as the separator when it is not adjacent to a
 *  binary operator, so that a single expression containing spaces (e.g.
 *  "pc + 0x40") is kept together, while e.g. "0x1000 0x1040" (or even
 *  "pc+0x40 pc+0x80") is still split into two expressions.
 */
static char *debugger_addr_range_separator(char *s)
{
	const char *operators = "+-*/%&|^";
	char prevch = '\0';

	while (*s != '\0') {
		if (*s == ' ') {
			char *space = s;
			while (*s == ' ')
				s ++;
			/*  Split at this space, unless it is adjacent to an
			    operator (or leads/ends the string):  */
			if (*s != '\0' && prevch != '\0' &&
			    strchr(operators, *s) == NULL &&
			    strchr(operators, prevch) == NULL)
				return space;
		} else {
			prevch = *s;
			s ++;
		}
	}

	return NULL;
}


/*
 *  debugger_cmd_dump():
 *
 *  Dump emulated memory in hex and ASCII.
 *
 *  syntax: dump [addr [endaddr]]
 */
static void debugger_cmd_dump(struct machine *m, char *args)
{
	uint64_t addr, addr_start, addr_end;
	struct cpu *c;
	struct memory *mem;
	char *p = NULL;
	int x, r;

	if (args[0] != '\0') {
		uint64_t tmp;
		char *tmps;

		CHECK_ALLOCATION(tmps = strdup(args));

		/*  addr: (Note: spaces adjacent to operators belong to the
		    addr expression itself, e.g. "dump pc + 0x40", and do
		    not start the optional endaddr argument.)  */
		p = debugger_addr_range_separator(tmps);
		if (p != NULL) {
			*p = '\0';
			p = args + (p - tmps);
		}
		r = debugger_parse_expression(m, tmps, 0, &tmp);
		free(tmps);

		if (r == PARSE_NOMATCH || r == PARSE_MULTIPLE) {
			printf("Unparsable address: %s\n", args);
			return;
		} else {
			last_dump_addr = tmp;
		}
	}

	if (m->cpus == NULL) {
		printf("No cpus (?)\n");
		return;
	}
	c = m->cpus[m->bootstrap_cpu];
	if (c == NULL) {
		printf("m->cpus[m->bootstrap_cpu] = NULL\n");
		return;
	}
	mem = m->cpus[m->bootstrap_cpu]->mem;

	addr_start = last_dump_addr;

	if (addr_start == MAGIC_UNTOUCHED)
		addr_start = c->pc;

	addr_end = addr_start + 16 * 16;

	/*  endaddr:  */
	if (p != NULL) {
		while (*p == ' ' && *p)
			p++;
		r = debugger_parse_expression(m, p, 0, &addr_end);
		if (r == PARSE_NOMATCH || r == PARSE_MULTIPLE) {
			printf("Unparsable address: %s\n", args);
			return;
		}
	}

	addr = addr_start & ~0xf;

	ctrl_c = 0;

	while (addr < addr_end) {
		unsigned char buf[16];
		memset(buf, 0, sizeof(buf));
		r = c->memory_rw(c, mem, addr, &buf[0], sizeof(buf),
		    MEM_READ, CACHE_NONE | NO_EXCEPTIONS);

		if (c->is_32bit)
			printf("0x%08" PRIx32"  ", (uint32_t) addr);
		else
			printf("0x%016" PRIx64"  ", (uint64_t) addr);

		if (r == MEMORY_ACCESS_FAILED)
			printf("(memory access failed)\n");
		else {
			for (x=0; x<16; x++) {
				if (addr + x >= addr_start &&
				    addr + x < addr_end)
					printf("%02x%s", buf[x],
					    (x&3)==3? " " : "");
				else
					printf("  %s", (x&3)==3? " " : "");
			}
			printf(" ");
			for (x=0; x<16; x++) {
				if (addr + x >= addr_start &&
				    addr + x < addr_end)
					printf("%c", (buf[x]>=' ' &&
					    buf[x]<127)? buf[x] : '.');
				else
					printf(" ");
			}
			printf("\n");
		}

		if (ctrl_c)
			return;

		addr += sizeof(buf);
	}

	last_dump_addr = addr_end;

	strlcpy(repeat_cmd, "dump", MAX_CMD_BUFLEN);
}


/*
 *  debugger_cmd_emul():
 *
 *  Dump info about the current emulation.
 */
static void debugger_cmd_emul(struct machine *m, char *args)
{
	if (*args) {
		printf("syntax: emul\n");
		return;
	}

	if (debugger_emul->name != NULL)
		debugmsg(SUBSYS_EMUL, "", VERBOSITY_INFO, "\"%s\"", debugger_emul->name);

	debug_indentation(1);
	emul_dumpinfo(debugger_emul);
	debug_indentation(-1);
}


/*
 *  debugger_cmd_find():
 *
 *  Search a memory range for a value or a string; similar to 'put', but
 *  with a range. (See the TODO list.)
 */
static void debugger_cmd_find(struct machine *m, char *args)
{
	static char find_type = ' ';  /*  Remembered across multiple calls.  */
	char copy[200];
	char *p_start, *p_end, *p_data, *p2;
	uint64_t startaddr, endaddr, data = 0;
	unsigned char pattern[sizeof(copy)];
	unsigned char window[512];
	uint64_t base, scan_from;
	size_t pattern_len = 0, i;
	int res, syntax_ok = 0;
	int n_matches = 0, n_shown = 0, n_unreadable = 0;
	const int max_shown = 64;
	struct cpu *c;

	strncpy(copy, args, sizeof(copy));
	copy[sizeof(copy)-1] = '\0';

	/*  syntax: find [b|h|w|d|q|s|z] startaddr, endaddr, data  */

	p_end = strchr(copy, ',');
	if (p_end != NULL) {
		*p_end++ = '\0';
		p_data = strchr(p_end, ',');
		if (p_data != NULL) {
			*p_data++ = '\0';
			syntax_ok = 1;
		}
	}

	if (!syntax_ok) {
		printf("syntax: find [b|h|w|d|q|s|z] startaddr, endaddr,"
		    " data\n");
		printf("   b    byte        (8 bits)\n");
		printf("   h    half-word   (16 bits)\n");
		printf("   w    word        (32 bits)\n");
		printf("   d    doubleword  (64 bits)\n");
		printf("   q    quad-word   (128 bits)\n");
		printf("   s    string (without terminating nul)\n");
		printf("   z    nul-terminated string\n");
		return;
	}

	while (*p_end == ' ' && *p_end)
		p_end ++;
	while (*p_data == ' ' && *p_data)
		p_data ++;
	while (strlen(copy) >= 1 && copy[strlen(copy) - 1] == ' ')
		copy[strlen(copy) - 1] = '\0';

	p_start = copy;
	p2 = strchr(p_start, ' ');
	if (p2 != NULL) {
		*p2 = '\0';
		if (strlen(p_start) != 1) {
			printf("Invalid type '%s'\n", p_start);
			return;
		}
		find_type = *p_start;
		p_start = p2 + 1;
		while (*p_start == ' ' && *p_start)
			p_start ++;
	}

	if (find_type == ' ') {
		printf("No type specified.\n");
		return;
	}

	res = debugger_parse_expression(m, p_start, 0, &startaddr);
	switch (res) {
	case PARSE_NOMATCH:
		printf("Couldn't parse the start address.\n");
		return;
	case PARSE_MULTIPLE:
		printf("Multiple matches for the start address."
		    " Try prefixing with %%, $, or @.\n");
		return;
	case PARSE_SETTINGS:
	case PARSE_SYMBOL:
	case PARSE_NUMBER:
		break;
	default:
		printf("INTERNAL ERROR in debugger.c.\n");
		return;
	}

	res = debugger_parse_expression(m, p_end, 0, &endaddr);
	switch (res) {
	case PARSE_NOMATCH:
		printf("Couldn't parse the end address.\n");
		return;
	case PARSE_MULTIPLE:
		printf("Multiple matches for the end address."
		    " Try prefixing with %%, $, or @.\n");
		return;
	case PARSE_SETTINGS:
	case PARSE_SYMBOL:
	case PARSE_NUMBER:
		break;
	default:
		printf("INTERNAL ERROR in debugger.c.\n");
		return;
	}

	if (m->cpus == NULL) {
		printf("No cpus (?)\n");
		return;
	}
	c = m->cpus[m->bootstrap_cpu];
	if (c == NULL) {
		printf("m->cpus[m->bootstrap_cpu] = NULL\n");
		return;
	}

	/*  Build the pattern to search for:  */
	if (find_type == 's' || find_type == 'z') {
		/*  The data argument is taken literally (optionally
		    surrounded by double quotes):  */
		size_t len = strlen(p_data);

		if (len >= 2 && p_data[0] == '"' && p_data[len-1] == '"') {
			p_data ++;
			len -= 2;
			p_data[len] = '\0';
		}

		if (find_type == 'z')
			len ++;		/*  include the terminating nul  */

		if (len == 0) {
			printf("Empty search string.\n");
			return;
		}

		memcpy(pattern, p_data, len);
		pattern_len = len;
	} else {
		res = debugger_parse_expression(m, p_data, 0, &data);
		switch (res) {
		case PARSE_NOMATCH:
			printf("Couldn't parse the data.\n");
			return;
		case PARSE_MULTIPLE:
			printf("Multiple matches for the data value."
			    " Try prefixing with %%, $, or @.\n");
			return;
		case PARSE_SETTINGS:
		case PARSE_SYMBOL:
		case PARSE_NUMBER:
			break;
		default:
			printf("INTERNAL ERROR in debugger.c.\n");
			return;
		}

		switch (find_type) {
		case 'b':
			pattern[0] = data;
			pattern_len = 1;
			if (data > 0xff)
				printf("(NOTE: truncating %0" PRIx64")\n",
				    (uint64_t) data);
			break;
		case 'h':
			store_16bit_word_in_host(c, pattern, data);
			pattern_len = 2;
			if (data > 0xffff)
				printf("(NOTE: truncating %0" PRIx64")\n",
				    (uint64_t) data);
			break;
		case 'w':
			store_32bit_word_in_host(c, pattern, data);
			pattern_len = 4;
			if (data > 0xffffffff && (data >> 32) != 0
			    && (data >> 32) != 0xffffffff)
				printf("(NOTE: truncating %0" PRIx64")\n",
				    (uint64_t) data);
			break;
		case 'd':
			store_64bit_word_in_host(c, pattern, data);
			pattern_len = 8;
			break;
		case 'q':
			printf("quad-words: TODO\n");
			return;
		default:
			printf("Unimplemented type '%c'\n", find_type);
			return;
		}
	}

	if (endaddr <= startaddr) {
		printf("The end address must be larger than the start"
		    " address.\n");
		return;
	}

	ctrl_c = 0;

	/*
	 *  Scan the range using a sliding window, so that matches spanning
	 *  chunk boundaries are found. The window is refilled using 16-byte
	 *  aligned reads (like the dump command, avoiding page-crossing
	 *  reads); unreadable chunks are skipped.
	 */
	base = startaddr & ~((uint64_t) 0xf);
	scan_from = startaddr;	/*  first address not yet tested  */

	while (base < endaddr) {
		size_t fill = 0;
		int failed_at = -1;

		if (ctrl_c) {
			printf("(interrupted)\n");
			break;
		}

		while (fill < sizeof(window) && base + fill < endaddr) {
			size_t chunk = 16;
			res = c->memory_rw(c, c->mem, base + fill,
			    window + fill, chunk, MEM_READ,
			    CACHE_NONE | NO_EXCEPTIONS);
			if (res == MEMORY_ACCESS_FAILED) {
				failed_at = fill;
				break;
			}
			fill += chunk;
		}

		if (fill >= pattern_len) {
			for (i = 0; i + pattern_len <= fill; i++) {
				uint64_t maddr = base + i;
				if (maddr < scan_from)
					continue;
				if (maddr + pattern_len > endaddr)
					break;
				if (memcmp(window + i, pattern,
				    pattern_len) != 0)
					continue;

				n_matches ++;
				if (n_shown < max_shown) {
					if (c->is_32bit)
						printf("match at 0x%08" PRIx32
						    "\n", (uint32_t) maddr);
					else
						printf("match at 0x%016" PRIx64
						    "\n", (uint64_t) maddr);
					n_shown ++;
				} else if (n_shown == max_shown) {
					printf("(further matches not"
					    " shown)\n");
					n_shown ++;
				}
			}

			if (base + fill - pattern_len + 1 > scan_from)
				scan_from = base + fill - pattern_len + 1;
		}

		if (failed_at >= 0) {
			/*  Skip past the unreadable 16-byte chunk:  */
			n_unreadable ++;
			base = base + failed_at + 16;
			if (scan_from < base)
				scan_from = base;
		} else if (base + fill >= endaddr) {
			break;
		} else {
			/*  Slide the window, keeping pattern_len-1 bytes
			    of overlap, 16-byte aligned:  */
			uint64_t advance = fill - (pattern_len - 1);
			advance &= ~((uint64_t) 0xf);
			if (advance == 0)
				advance = 16;
			base += advance;
		}
	}

	if (n_unreadable > 0)
		printf("(skipped %i unreadable 16-byte chunk%s)\n",
		    n_unreadable, n_unreadable == 1? "" : "s");
	printf("%i match%s found.\n", n_matches, n_matches == 1? "" : "es");
}


/*
 *  debugger_cmd_focus():
 *
 *  Changes focus to specific cpu, in a specific machine (in a specific
 *  emulation).
 */
static void debugger_cmd_focus(struct machine *m, char *args)
{
	int x = -1, y = -1;
	char *p, *p2;

	if (!args[0]) {
		printf("syntax: focus x[,y]\n");
		printf("where x (cpu id) and y (machine number) "
		    "are integers as\nreported by the 'emul'"
		    " command.\n");
		goto print_current_focus_and_return;
	}

	x = atoi(args);
	p = strchr(args, ',');
	if (p == args) {
		printf("No cpu number specified?\n");
		return;
	}

	if (p != NULL) {
		y = atoi(p+1);
		p2 = strchr(p+1, ',');
		if (p2 == p+1) {
			printf("No machine number specified?\n");
			return;
		}
	}

	if (y != -1) {
		/*  Change machine:  */
		if (y < 0 || y >= debugger_emul->n_machines) {
			printf("Invalid machine number: %i\n", y);
			return;
		}

		debugger_cur_machine = y;
		debugger_machine = debugger_emul->machines[y];
	}

	/*  Change cpu:  */
	if (x < 0 || x >= debugger_machine->ncpus) {
		printf("Invalid cpu number: %i\n", x);
		return;
	}

	debugger_cur_cpu = x;

print_current_focus_and_return:
	if (debugger_emul->n_machines > 1)
		printf("current machine (%i): \"%s\"\n",
		    debugger_cur_machine, debugger_machine->name == NULL?
		    "(no name)" : debugger_machine->name);

	printf("current cpu (%i)\n", debugger_cur_cpu);
}


/*  This is defined below.  */
static void debugger_cmd_help(struct machine *m, char *args);


/*
 *  debugger_cmd_itrace():
 */
static void debugger_cmd_itrace(struct machine *m, char *args)
{
	if (*args) {
		printf("syntax: itrace\n");
		return;
	}

	m->instruction_trace = !m->instruction_trace;

	if (m->instruction_trace)
		verbose ++;
	else
		verbose --;

	printf("instruction_trace = %s\n", m->instruction_trace? "ON":"OFF");
}


/*
 *  debugger_cmd_lookup():
 */
static void debugger_cmd_lookup(struct machine *m, char *args)
{
	uint64_t addr;
	int res;
	char *symbol;
	uint64_t offset;

	if (args[0] == '\0') {
		printf("syntax: lookup name|addr\n");
		return;

	}

	/*  Addresses never need to be given in decimal form anyway,
	    so assuming hex here will be ok.  */
	addr = strtoull(args, NULL, 16);

	if (addr == 0) {
		uint64_t newaddr;
		res = get_symbol_addr(&m->symbol_context,
		    args, &newaddr);
		if (!res) {
			printf("lookup for '%s' failed\n", args);
			return;
		}
		printf("%s = 0x", args);
		if (m->cpus[0]->is_32bit)
			printf("%08" PRIx32"\n", (uint32_t) newaddr);
		else
			printf("%016" PRIx64"\n", (uint64_t) newaddr);
		return;
	}

	symbol = get_symbol_name(&m->symbol_context, addr, &offset);

	if (symbol != NULL) {
		if (m->cpus[0]->is_32bit)
			printf("0x%08" PRIx32, (uint32_t) addr);
		else
			printf("0x%016" PRIx64, (uint64_t) addr);
		printf(" = %s\n", symbol);
	} else
		printf("lookup for '%s' failed\n", args);
}


/*
 *  debugger_cmd_machine():
 *
 *  Dump info about the currently focused machine.
 */
static void debugger_cmd_machine(struct machine *m, char *args)
{
	if (*args) {
		printf("syntax: machine\n");
		return;
	}

	if (m->name != NULL && m->name[0])
		debugmsg(SUBSYS_MACHINE, "", VERBOSITY_INFO, "%s", m->name);
	else
		debugmsg(SUBSYS_MACHINE, "", VERBOSITY_INFO, "");

	debug_indentation(1);
	machine_dumpinfo(m);
	debug_indentation(-1);
}


/*
 *  debugger_cmd_ninstrs():
 */
static void debugger_cmd_ninstrs(struct machine *m, char *args)
{
	int toggle = 1;
	int previous_mode = m->show_nr_of_instructions;

	if (args[0] != '\0') {
		while (args[0] != '\0' && args[0] == ' ')
			args ++;
		switch (args[0]) {
		case '0':
			toggle = 0;
			m->show_nr_of_instructions = 0;
			break;
		case '1':
			toggle = 0;
			m->show_nr_of_instructions = 1;
			break;
		case 'o':
		case 'O':
			toggle = 0;
			switch (args[1]) {
			case 'n':
			case 'N':
				m->show_nr_of_instructions = 1;
				break;
			default:
				m->show_nr_of_instructions = 0;
			}
			break;
		default:
			printf("syntax: trace [on|off]\n");
			return;
		}
	}

	if (toggle)
		m->show_nr_of_instructions = !m->show_nr_of_instructions;

	printf("show_nr_of_instructions = %s",
	    m->show_nr_of_instructions? "ON" : "OFF");
	if (m->show_nr_of_instructions != previous_mode)
		printf("  (was: %s)", previous_mode? "ON" : "OFF");
	printf("\n");
}


/*
 *  debugger_cmd_pause():
 */
static void debugger_cmd_pause(struct machine *m, char *args)
{
	int cpuid = -1;

	if (args[0] != '\0')
		cpuid = atoi(args);
	else {
		printf("syntax: pause cpuid\n");
		return;
	}

	if (cpuid < 0 || cpuid >= m->ncpus) {
		printf("cpu%i doesn't exist.\n", cpuid);
		return;
	}

	m->cpus[cpuid]->running = !m->cpus[cpuid]->running;

	printf("cpu%i (%s) in machine \"%s\" is now %s\n", cpuid,
	    m->cpus[cpuid]->name, m->name,
	    m->cpus[cpuid]->running? "RUNNING" : "STOPPED");
}


/*
 *  debugger_cmd_print():
 */
static void debugger_cmd_print(struct machine *m, char *args)
{
	int res;
	uint64_t tmp;

	while (args[0] != '\0' && args[0] == ' ')
		args ++;

	if (args[0] == '\0') {
		printf("syntax: print expr\n");
		return;
	}

	res = debugger_parse_expression(m, args, 0, &tmp);
	switch (res) {
	case PARSE_NOMATCH:
		printf("No match.\n");
		break;
	case PARSE_MULTIPLE:
		printf("Multiple matches. Try prefixing with %%, $, or @.\n");
		break;
	case PARSE_SETTINGS:
		printf("%s = 0x%" PRIx64"\n", args, (uint64_t)tmp);
		break;
	case PARSE_SYMBOL:
		if (m->cpus[0]->is_32bit)
			printf("%s = 0x%08" PRIx32"\n", args, (uint32_t)tmp);
		else
			printf("%s = 0x%016" PRIx64"\n", args,(uint64_t)tmp);
		break;
	case PARSE_NUMBER:
		printf("0x%" PRIx64"\n", (uint64_t) tmp);
		break;
	}
}


/*
 *  debugger_cmd_put():
 */
static void debugger_cmd_put(struct machine *m, char *args)
{
	static char put_type = ' ';  /*  Remembered across multiple calls.  */
	char copy[200];
	int res, syntax_ok = 0;
	char *p, *p2, *q = NULL;
	uint64_t addr, data;
	unsigned char a_byte;

	strncpy(copy, args, sizeof(copy));
	copy[sizeof(copy)-1] = '\0';

	/*  syntax: put [b|h|w|d|q] addr, data  */

	p = strchr(copy, ',');
	if (p != NULL) {
		*p++ = '\0';
		while (*p == ' ' && *p)
			p++;
		while (strlen(copy) >= 1 &&
		    copy[strlen(copy) - 1] == ' ')
			copy[strlen(copy) - 1] = '\0';

		/*  printf("L = '%s', R = '%s'\n", copy, p);  */

		q = copy;
		p2 = strchr(q, ' ');

		if (p2 != NULL) {
			*p2 = '\0';
			if (strlen(q) != 1) {
				printf("Invalid type '%s'\n", q);
				return;
			}
			put_type = *q;
			q = p2 + 1;
		}

		/*  printf("type '%c', L '%s', R '%s'\n", put_type, q, p);  */
		syntax_ok = 1;
	}

	if (!syntax_ok) {
		printf("syntax: put [b|h|w|d|q|s|z] addr, data\n");
		printf("   b    byte        (8 bits)\n");
		printf("   h    half-word   (16 bits)\n");
		printf("   w    word        (32 bits)\n");
		printf("   d    doubleword  (64 bits)\n");
		printf("   q    quad-word   (128 bits)\n");
		printf("   s    string (without terminating nul)\n");
		printf("   z    nul-terminated string\n");
		return;
	}

	if (put_type == ' ') {
		printf("No type specified.\n");
		return;
	}

	/*  here: q is the address, p is the data.  */
	res = debugger_parse_expression(m, q, 0, &addr);
	switch (res) {
	case PARSE_NOMATCH:
		printf("Couldn't parse the address.\n");
		return;
	case PARSE_MULTIPLE:
		printf("Multiple matches for the address."
		    " Try prefixing with %%, $, or @.\n");
		return;
	case PARSE_SETTINGS:
	case PARSE_SYMBOL:
	case PARSE_NUMBER:
		break;
	default:
		printf("INTERNAL ERROR in debugger.c.\n");
		return;
	}

	/*  String modes ("s" and "z") take the data argument literally
	    (optionally surrounded by double quotes) and write it to memory
	    one byte at a time; "z" also writes a terminating nul:  */
	if (put_type == 's' || put_type == 'z') {
		size_t len = strlen(p);
		size_t i;

		if (len >= 2 && p[0] == '"' && p[len-1] == '"') {
			p ++;
			len -= 2;
			p[len] = '\0';
		}

		if (put_type == 'z')
			len ++;

		if (len == 0) {
			printf("Empty string.\n");
			return;
		}

		if (m->cpus[0]->is_32bit)
			printf("0x%08" PRIx32, (uint32_t) addr);
		else
			printf("0x%016" PRIx64, (uint64_t) addr);

		for (i=0; i<len; i++) {
			a_byte = p[i];
			res = m->cpus[0]->memory_rw(m->cpus[0],
			    m->cpus[0]->mem, addr + i, &a_byte, 1,
			    MEM_WRITE, CACHE_NONE | NO_EXCEPTIONS);
			if (!res) {
				printf(": FAILED (at byte offset %i)!\n",
				    (int) i);
				return;
			}
		}

		printf(": %i byte%s written%s\n", (int) len,
		    len == 1? "" : "s",
		    put_type == 'z'? " (including terminating nul)" : "");
		return;
	}

	res = debugger_parse_expression(m, p, 0, &data);
	switch (res) {
	case PARSE_NOMATCH:
		printf("Couldn't parse the data.\n");
		return;
	case PARSE_MULTIPLE:
		printf("Multiple matches for the data value."
		    " Try prefixing with %%, $, or @.\n");
		return;
	case PARSE_SETTINGS:
	case PARSE_SYMBOL:
	case PARSE_NUMBER:
		break;
	default:
		printf("INTERNAL ERROR in debugger.c.\n");
		return;
	}

	/*  TODO: haha, maybe this should be refactored  */

	switch (put_type) {
	case 'b':
		a_byte = data;
		if (m->cpus[0]->is_32bit)
			printf("0x%08" PRIx32, (uint32_t) addr);
		else
			printf("0x%016" PRIx64, (uint64_t) addr);
		printf(": %02x", a_byte);
		if (data > 255)
			printf(" (NOTE: truncating %0" PRIx64")",
			    (uint64_t) data);
		res = m->cpus[0]->memory_rw(m->cpus[0], m->cpus[0]->mem, addr,
		    &a_byte, 1, MEM_WRITE, CACHE_NONE | NO_EXCEPTIONS);
		if (!res)
			printf("  FAILED!\n");
		printf("\n");
		return;
	case 'h':
		if ((addr & 1) != 0)
			printf("WARNING: address isn't aligned\n");
		if (m->cpus[0]->is_32bit)
			printf("0x%08" PRIx32, (uint32_t) addr);
		else
			printf("0x%016" PRIx64, (uint64_t) addr);
		printf(": %04x", (int)data);
		if (data > 0xffff)
			printf(" (NOTE: truncating %0" PRIx64")",
			    (uint64_t) data);
		res = store_16bit_word(m->cpus[0], addr, data);
		if (!res)
			printf("  FAILED!\n");
		printf("\n");
		return;
	case 'w':
		if ((addr & 3) != 0)
			printf("WARNING: address isn't aligned\n");
		if (m->cpus[0]->is_32bit)
			printf("0x%08" PRIx32, (uint32_t) addr);
		else
			printf("0x%016" PRIx64, (uint64_t) addr);

		printf(": %08x", (int)data);

		if (data > 0xffffffff && (data >> 32) != 0
		    && (data >> 32) != 0xffffffff)
			printf(" (NOTE: truncating %0" PRIx64")",
			    (uint64_t) data);

		res = store_32bit_word(m->cpus[0], addr, data);
		if (!res)
			printf("  FAILED!\n");
		printf("\n");
		return;
	case 'd':
		if ((addr & 7) != 0)
			printf("WARNING: address isn't aligned\n");
		if (m->cpus[0]->is_32bit)
			printf("0x%08" PRIx32, (uint32_t) addr);
		else
			printf("0x%016" PRIx64, (uint64_t) addr);

		printf(": %016" PRIx64, (uint64_t) data);

		res = store_64bit_word(m->cpus[0], addr, data);
		if (!res)
			printf("  FAILED!\n");
		printf("\n");
		return;
	case 'q':
		printf("quad-words: TODO\n");
		/*  TODO  */
		return;
	default:
		printf("Unimplemented type '%c'\n", put_type);
		return;
	}
}


/*
 *  debugger_cmd_quiet():
 */
static void debugger_cmd_quiet(struct machine *m, char *args)
{
	int toggle = 1;
	int previous_mode = old_quiet_mode;

	if (args[0] != '\0') {
		while (args[0] != '\0' && args[0] == ' ')
			args ++;
		switch (args[0]) {
		case '0':
			toggle = 0;
			old_quiet_mode = 0;
			break;
		case '1':
			toggle = 0;
			old_quiet_mode = 1;
			break;
		case 'o':
		case 'O':
			toggle = 0;
			switch (args[1]) {
			case 'n':
			case 'N':
				old_quiet_mode = 1;
				break;
			default:
				old_quiet_mode = 0;
			}
			break;
		default:
			printf("syntax: quiet [on|off]\n");
			return;
		}
	}

	if (toggle)
		old_quiet_mode = 1 - old_quiet_mode;

	printf("quiet_mode = %s", old_quiet_mode? "ON" : "OFF");
	if (old_quiet_mode != previous_mode)
		printf(" (was: %s)", previous_mode? "ON" : "OFF");
	printf("; setting verbosity for all subsystems to %s\n",
	    old_quiet_mode ? "ERROR" : "WARNING");

	debugmsg_set_verbosity_level(SUBSYS_ALL,
	    old_quiet_mode ? VERBOSITY_ERROR : VERBOSITY_WARNING);
}


/*
 *  debugger_cmd_quit():
 */
static void debugger_cmd_quit(struct machine *m, char *args)
{
	if (*args) {
		printf("syntax: quit\n");
		return;
	}

	emul_shutdown = true;
	exit_debugger = true;
}


/*
 *  debugger_cmd_reg():
 */
static void debugger_cmd_reg(struct machine *m, char *args)
{
	int cpuid = debugger_cur_cpu, coprocnr = -1;
	int gprs, coprocs;
	char *p;

	/*  [cpuid][,c]  */
	if (args[0] != '\0') {
		if (args[0] != ',') {
			cpuid = strtoull(args, NULL, 0);
			if (cpuid < 0 || cpuid >= m->ncpus) {
				printf("cpu%i doesn't exist.\n", cpuid);
				return;
			}
		}
		p = strchr(args, ',');
		if (p != NULL) {
			coprocnr = atoi(p + 1);
			if (coprocnr < 0 || coprocnr >= 4) {
				printf("Invalid coprocessor number.\n");
				return;
			}
		}
	}

	gprs = (coprocnr == -1)? 1 : 0;
	coprocs = (coprocnr == -1)? 0x0 : (1 << coprocnr);

	cpu_register_dump(m, m->cpus[cpuid], gprs, coprocs);
}


/*
 *  debugger_cmd_step():
 *
 *  With no argument (or a number n), single-step 1 (or n) instruction(s).
 *
 *  With the argument "call" (which may be abbreviated), single-step until
 *  the next function call or function return is traced, with function
 *  call trace output ("trace") implicitly turned on while stepping.
 */
static void debugger_cmd_step(struct machine *m, char *args)
{
	int n = 1;

	if (args[0] != '\0' && !isdigit((int)args[0])) {
		size_t wordlen = 0;
		while (args[wordlen] != '\0' && args[wordlen] != ' ')
			wordlen ++;

		if (strncasecmp(args, "call", wordlen) == 0 &&
		    args[wordlen] == '\0') {
			int i;

			/*  Single-step until a function call or return is
			    traced. Function call trace is implicitly turned
			    on while stepping (this takes effect immediately,
			    since all translations were cleared when the
			    debugger was entered). Clear any stale per-cpu
			    transition flags first:  */
			debugger_old_show_trace_tree = m->show_trace_tree;
			m->show_trace_tree = 1;

			for (i=0; i<m->ncpus; i++)
				m->cpus[i]->last_was_function_transition = 0;

			ctrl_c = 0;
			debugger_stepping_until_function_transition = 1;
			debugger_n_steps_left_before_interaction = 0;

			/*  Special hack, see the main debugger() loop.  */
			exit_debugger = true;
			exit_debugger_to_continue_single_stepping = true;

			strlcpy(repeat_cmd, "step call", MAX_CMD_BUFLEN);
			return;
		}

		printf("syntax: step [n | call]\n");
		return;
	}

	if (args[0] != '\0') {
		n = strtoull(args, NULL, 0);
		if (n < 1) {
			printf("invalid nr of steps\n");
			return;
		}
	}

	debugger_n_steps_left_before_interaction = n - 1;

	/*  Special hack, see the main debugger() loop for more info.  */
	exit_debugger = true;
	exit_debugger_to_continue_single_stepping = true;

	strlcpy(repeat_cmd, "step", MAX_CMD_BUFLEN);
}


/*
 *  debugger_cmd_tlbdump():
 *
 *  Dumps a CPU's TLB content.
 */
static void debugger_cmd_tlbdump(struct machine *m, char *args)
{
	int x = 0;
	int rawflag = 0;

	if (args[0] != '\0') {
		char *p;
		if (args[0] != ',') {
			x = strtoull(args, NULL, 0);
			if (x < 0 || x >= m->ncpus) {
				printf("cpu%i doesn't exist.\n", x);
				return;
			}
		}
		p = strchr(args, ',');
		if (p != NULL) {
			switch (p[1]) {
			case 'r':
			case 'R':
				rawflag = 1;
				break;
			default:
				printf("Unknown tlbdump flag.\n");
				printf("syntax: tlbdump [cpuid][,r]\n");
				return;
			}
		}
	}

	cpu_tlbdump(m->cpus[x], rawflag);
}


/*
 *  debugger_cmd_trace():
 */
static void debugger_cmd_trace(struct machine *m, char *args)
{
	int toggle = 1;
	int previous_mode = m->show_trace_tree;

	if (args[0] != '\0') {
		while (args[0] != '\0' && args[0] == ' ')
			args ++;
		switch (args[0]) {
		case '0':
			toggle = 0;
			m->show_trace_tree = 0;
			break;
		case '1':
			toggle = 0;
			m->show_trace_tree = 1;
			break;
		case 'o':
		case 'O':
			toggle = 0;
			switch (args[1]) {
			case 'n':
			case 'N':
				m->show_trace_tree = 1;
				break;
			default:
				m->show_trace_tree = 0;
			}
			break;
		default:
			printf("syntax: trace [on|off]\n");
			return;
		}
	}

	if (toggle)
		m->show_trace_tree = !m->show_trace_tree;

	printf("show_trace_tree = %s", m->show_trace_tree? "ON" : "OFF");
	if (m->show_trace_tree != previous_mode)
		printf("  (was: %s)", previous_mode? "ON" : "OFF");
	printf("\n");
}


/*
 *  debugger_cmd_unassemble():
 *
 *  Dump emulated memory as instructions.
 *
 *  syntax: unassemble [addr [endaddr]]
 */
static void debugger_cmd_unassemble(struct machine *m, char *args)
{
	uint64_t addr, addr_start, addr_end;
	struct cpu *c;
	struct memory *mem;
	char *p = NULL;
	int r, lines_left = -1;

	if (args[0] != '\0') {
		uint64_t tmp;
		char *tmps;

		CHECK_ALLOCATION(tmps = strdup(args));

		/*  addr: (Note: spaces adjacent to operators belong to the
		    addr expression itself, e.g. "unassemble pc + 0x40", and
		    do not start the optional endaddr argument.)  */
		p = debugger_addr_range_separator(tmps);
		if (p != NULL) {
			*p = '\0';
			p = args + (p - tmps);
		}
		r = debugger_parse_expression(m, tmps, 0, &tmp);
		free(tmps);

		if (r == PARSE_NOMATCH || r == PARSE_MULTIPLE) {
			printf("Unparsable address: %s\n", args);
			return;
		} else {
			last_unasm_addr = tmp;
		}
	}

	if (m->cpus == NULL) {
		printf("No cpus (?)\n");
		return;
	}
	c = m->cpus[m->bootstrap_cpu];
	if (c == NULL) {
		printf("m->cpus[m->bootstrap_cpu] = NULL\n");
		return;
	}
	mem = m->cpus[m->bootstrap_cpu]->mem;

	addr_start = last_unasm_addr;

	if (addr_start == MAGIC_UNTOUCHED)
		addr_start = c->pc;

	addr_end = addr_start + 1000;

	/*  endaddr:  */
	if (p != NULL) {
		while (*p == ' ' && *p)
			p++;
		r = debugger_parse_expression(m, p, 0, &addr_end);
		if (r == PARSE_NOMATCH || r == PARSE_MULTIPLE) {
			printf("Unparsable address: %s\n", args);
			return;
		}
	} else
		lines_left = 20;

	addr = addr_start;

	ctrl_c = 0;

	while (addr < addr_end) {
		unsigned int i, len;
		int failed = 0;
		unsigned char buf[17];	/*  TODO: How long can an
					    instruction be, on weird archs?  */
		memset(buf, 0, sizeof(buf));

		for (i=0; i<sizeof(buf); i++) {
			uint64_t actualaddr = addr;

			// Hack for ARM (THUMB): (Lowest bit = 1 means 16-bit encoding)
			if (c->cpu_family->arch == ARCH_ARM)
				actualaddr &= ~1;

			if (c->memory_rw(c, mem, actualaddr+i, buf+i, 1, MEM_READ,
			    CACHE_NONE | NO_EXCEPTIONS) == MEMORY_ACCESS_FAILED)
				failed ++;
		}

		if (failed == sizeof(buf)) {
			printf("(memory access failed)\n");
			break;
		}

		len = cpu_disassemble_instr(m, c, buf, 0, addr);

		if (ctrl_c)
			return;
		if (len == 0)
			break;

		addr += len;

		if (lines_left != -1) {
			lines_left --;
			if (lines_left == 0)
				break;
		}
	}

	last_unasm_addr = addr;

	strlcpy(repeat_cmd, "unassemble", MAX_CMD_BUFLEN);
}


/*
 *  debugger_cmd_verbosity():
 */
static void debugger_cmd_verbosity(struct machine *m, char *args)
{
	char *subsystem = args;
	char *n = subsystem;
	if (*n) {
		while (*n && *n != ' ')
			n++;
		while (*n && *n == ' ')
			n++;
	}

	if (*n == '\0') {
		debugmsg_print_settings(subsystem);
		return;
	}

	char s[200];
	snprintf(s, sizeof(s), "%s", subsystem);
	size_t i = n - subsystem - 1;
	if (i < sizeof(s))
		s[i] = '\0';
	else {
		printf("syntax: verbosity [subsystem [n]]\n");
		return;
	}

	char *n2 = n;
	while (*n2 && *n2 != ' ')
		n2++;
	*n2 = '\0';

	/* printf("subsystem = '%s'\n", s);
	if (*n)
		printf("n = '%s'\n", n);
	*/

	debugmsg_change_settings(s, n);
}


/*
 *  debugger_cmd_version():
 */
static void debugger_cmd_version(struct machine *m, char *args)
{
	if (*args) {
		printf("syntax: version\n");
		return;
	}

	printf("%s, %s\n", VERSION, COMPILE_DATE);
}


/****************************************************************************/


struct cmd {
	const char	*name;
	const char	*args;
	int		tmp_flag;
	void		(*f)(struct machine *, char *args);
	const char	*description;
};

static struct cmd cmds[] = {
	{ "allsettings", "", 0, debugger_cmd_allsettings,
		"show all settings" },

	{ "breakpoint", "...", 0, debugger_cmd_breakpoint,
		"manipulate breakpoints" },

	/*  NOTE: Try to keep 'c' down to only one command. Having 'continue'
	    available as a one-letter command is very convenient.  */

	{ "continue", "", 0, debugger_cmd_continue,
		"continue execution" },

	{ "device", "...", 0, debugger_cmd_device,
		"show info about (or manipulate) devices" },

	{ "dump", "[addr [endaddr]]", 0, debugger_cmd_dump,
		"dump memory contents in hex and ASCII" },

	{ "emul", "", 0, debugger_cmd_emul,
		"Print a summary of the current emulation" },

	{ "find", "[b|h|w|d|q|s|z] addr, endaddr, data", 0, debugger_cmd_find,
		"search a memory range for a value or a string" },

	{ "focus", "x[,y[,z]]", 0, debugger_cmd_focus,
		"changes focus to cpu x, machine x, emul z" },

	{ "help", "", 0, debugger_cmd_help,
		"Print this help message" },

	{ "itrace", "", 0, debugger_cmd_itrace,
		"toggle instruction_trace on or off" },

	{ "lookup", "name|addr", 0, debugger_cmd_lookup,
		"lookup a symbol by name or address" },

	{ "machine", "", 0, debugger_cmd_machine,
		"Print a summary of the current machine" },

	{ "ninstrs", "[on|off]", 0, debugger_cmd_ninstrs,
		"toggle (set or unset) show_nr_of_instructions" },

	{ "pause", "cpuid", 0, debugger_cmd_pause,
		"pause (or unpause) a CPU" },

	{ "print", "expr", 0, debugger_cmd_print,
		"evaluate an expression without side-effects" },

	{ "put", "[b|h|w|d|q|s|z] addr, data", 0, debugger_cmd_put,
		"modify emulated memory contents" },

	{ "quiet", "[on|off]", 0, debugger_cmd_quiet,
		"toggle quiet_mode on or off" },

	{ "quit", "", 0, debugger_cmd_quit,
		"quit the emulator" },

	/*  NOTE: Try to keep 'r' down to only one command. Having 'reg'
	    available as a one-letter command is very convenient.  */

	{ "reg", "[cpuid][,c]", 0, debugger_cmd_reg,
		"show GPRs (or coprocessor c's registers)" },

	/*  NOTE: Try to keep 's' down to only one command. Having 'step'
	    available as a one-letter command is very convenient.  */

	{ "step", "[n|call]", 0, debugger_cmd_step,
		"single-step one (or n) instr(s), or until a call/return" },

	{ "tlbdump", "[cpuid][,r]", 0, debugger_cmd_tlbdump,
		"dump TLB contents (add ',r' for raw data)" },

	{ "trace", "[on|off]", 0, debugger_cmd_trace,
		"toggle show_trace_tree on or off" },

	/*  NOTE: Try to keep 'u' down to only one command. Having 'unassemble'
	    available as a one-letter command is very convenient.  */

	{ "unassemble", "[addr [endaddr]]", 0, debugger_cmd_unassemble,
		"dump memory contents as instructions" },

	{ "verbosity", "[subsystem [n]]", 0, debugger_cmd_verbosity,
		"sets or displays debug message verbosity levels" },

	{ "version", "", 0, debugger_cmd_version,
		"Print version information" },

	{ "watchpoint", "...", 0, debugger_cmd_watchpoint,
		"break on guest writes to an address range" },

	/*  Note: NULL handler.  */
	{ "x = expr", "", 0, NULL, "generic assignment" },

	{ NULL, NULL, 0, NULL, NULL }
};


/*
 *  debugger_cmd_help():
 *
 *  Print a list of available commands.
 *
 *  NOTE: This is placed after the cmds[] array, because it needs to
 *  access it.
 *
 *  TODO: Command completion (ie just type "help s" for "help step").
 */
static void debugger_cmd_help(struct machine *m, char *args)
{
	int only_one = 0, only_one_match = 0;
	char *nlines_env = getenv("LINES");
	int nlines = atoi(nlines_env != NULL? nlines_env : "999999"), curlines;
	size_t i, j, max_name_len = 0;

	if (args[0] != '\0') {
		only_one = 1;
	}

	i = 0;
	while (cmds[i].name != NULL) {
		size_t a = strlen(cmds[i].name);
		if (cmds[i].args != NULL)
			a += 1 + strlen(cmds[i].args);
		if (a > max_name_len)
			max_name_len = a;
		i++;
	}

	curlines = 0;
	if (!only_one) {
		printf("Available commands:\n");
		curlines++;
	}

	i = 0;
	while (cmds[i].name != NULL) {
		char buf[100];
		snprintf(buf, sizeof(buf), "%s", cmds[i].name);

		if (only_one) {
			if (strcmp(cmds[i].name, args) != 0) {
				i++;
				continue;
			}
			only_one_match = 1;
		}

		if (cmds[i].args != NULL)
			snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
			    " %s", cmds[i].args);

		printf("  ");
		for (j=0; j<max_name_len; j++)
			if (j < strlen(buf))
				printf("%c", buf[j]);
			else
				printf(" ");

		printf("  %s\n", cmds[i].description);
		i++;

		curlines ++;
		if (curlines >= nlines - 1) {
			char ch;
			printf("-- more --"); fflush(stdout);
			ch = debugger_readchar();
			printf("\n");
			if (ch == 'q' || ch == 'Q')
				return;
			curlines = 0;
		}
	}

	if (only_one) {
		if (!only_one_match)
			printf("%s: no such command\n", args);
		return;
	}

	/*  TODO: generalize/refactor  */
	curlines += 8;
	if (curlines > nlines - 1) {
		char ch;
		printf("-- more --"); fflush(stdout);
		ch = debugger_readchar();
		printf("\n");
		if (ch == 'q' || ch == 'Q')
			return;
		curlines = 0;
	}

	printf("\nIn generic assignments, x must be a register or other "
	    "writable settings\nvariable, and expr can contain registers/"
	    "settings, numeric values, or symbol\nnames, in combination with"
	    " parenthesis and + - * / & %% ^ | operators.\nIn case there are"
	    " multiple matches (i.e. a symbol that has the same name as a\n"
	    "register), you may add a prefix character as a hint: '#' for"
	    " registers, '@'\nfor symbols, and '$' for numeric values. Use"
	    " 0x for hexadecimal values.\n");
}

