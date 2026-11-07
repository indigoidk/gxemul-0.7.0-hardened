# GXemul hardened fork -- DRAFT A FIX for one filed issue, `catsmemwrap` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `catsmemwrap`, state `open`, severity `LOW`)

**title:** src/machines/machine_cats.c:59-61,110-111 -- physical_ram_in_mb * 1048576 is computed in 32 bits, so a -M of 4096 MB or more wraps the boot-info bt_memend; the > 256 test only warns -- WRAP (host -M option)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- requires a 64-bit cast to handle >4GB RAM arguments properly.

## The code at the cited lines

### `src/machines/machine_cats.c` around the row's cited line 59 (HEAD 2d25df65, lines 14-104)

```c
   14|  *
   15|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *   
   27|  *
   28|  *  COMMENT: Simtec Electronics' CATS board
   29|  */
   30| 
   31| #include <stdio.h>
   32| #include <stdlib.h>
   33| #include <string.h>
   34| 
   35| #include "bus_isa.h"
   36| #include "bus_pci.h"
   37| #include "cpu.h"
   38| #include "device.h"
   39| #include "devices.h"
   40| #include "machine.h"
   41| #include "memory.h"
   42| #include "misc.h"
   43| 
   44| #include "thirdparty/cyclone_boot.h"
   45| 
   46| 
   47| MACHINE_SETUP(cats)
   48| {
   49| 	struct ebsaboot ebsaboot;
   50| 	struct pci_data *pci_bus;
   51| 	char bs[300], tmpstr[400];
   52| 	int boot_id = machine->bootdev_id >= 0? machine->bootdev_id : 0;
   53| 
   54| 	machine->machine_name = strdup("CATS evaluation board");
   55| 
   56| 	if (machine->emulated_hz == 0)
   57| 		machine->emulated_hz = 50000000;
   58| 
   59| 	if (machine->physical_ram_in_mb > 256)
   60| 		fprintf(stderr, "WARNING! Real CATS machines cannot"
   61| 		    " have more than 256 MB RAM. Continuing anyway.\n");
   62| 
   63| 	snprintf(tmpstr, sizeof(tmpstr), "footbridge irq=%s.cpu[%i].irq"
   64| 	    " addr=0x42000000", machine->path, machine->bootstrap_cpu);
   65| 	pci_bus = (struct pci_data *) device_add(machine, tmpstr);
   66| 
   67| 	/*  DC21285_ROM_BASE (256 KB at 0x41000000)  */
   68| 	dev_ram_init(machine, 0x41000000, 256 * 1024, DEV_RAM_RAM, 0, NULL);
   69| 
   70| 	/*  NetBSD, OpenBSD, and Linux (?) clean their caches here:  */
   71| 	dev_ram_init(machine, 0x50000000, 0x10000, DEV_RAM_RAM, 0, NULL);
   72| 
   73| 	/*  Interrupt ack space?  */
   74| 	dev_ram_init(machine, 0x80000000, 0x1000, DEV_RAM_RAM, 0, NULL);
   75| 
   76| 	/*  Linux uses 0xc0000000 as phys.:  */
   77| 	dev_ram_init(machine, 0xc0000000, 0x20000000, DEV_RAM_MIRROR, 0x0, NULL);
   78| 
   79| 	/*  OpenBSD reboot needs 0xf??????? to be mapped to phys.:  */
   80| 	dev_ram_init(machine, 0xf0000000, 0x1000000, DEV_RAM_MIRROR, 0x0, NULL);
   81| 
   82| 	bus_pci_add(machine, pci_bus, machine->memory, 0xc0, 8, 0, "s3_virge");
   83| 
   84| 	if (!machine->prom_emulation)
   85| 		return;
   86| 
   87| 	/*  See cyclone_boot.h for details.  */
   88| 
   89| 	/*  DC21285_ROM_BASE "reboot" code:  (works with NetBSD)  */
   90| 	store_32bit_word(cpu, 0x41000008ULL, 0xef8c64ebUL);
   91| 
   92| 	cpu->cd.arm.r[0] = /* machine->physical_ram_in_mb */
   93| 	    7 * 1048576 - 0x1000;
   94| 
   95| 	memset(&ebsaboot, 0, sizeof(struct ebsaboot));
   96| 	store_32bit_word_in_host(cpu, (unsigned char *)
   97| 	    &(ebsaboot.bt_magic), BT_MAGIC_NUMBER_CATS);
   98| 	store_32bit_word_in_host(cpu, (unsigned char *)
   99| 	    &(ebsaboot.bt_vargp), 0);
  100| 	store_32bit_word_in_host(cpu, (unsigned char *)
  101| 	    &(ebsaboot.bt_pargp), 0);
  102| 	store_32bit_word_in_host(cpu, (unsigned char *)
  103| 	    &(ebsaboot.bt_args), cpu->cd.arm.r[0]
  104| 	    + sizeof(struct ebsaboot));
```

### `src/include/machine.h` around the row's cited line 170 (HEAD 2d25df65, lines 125-215)

```c
  125| 	struct emul *emul;
  126| 
  127| 	/*  Settings:  */
  128| 	struct settings *settings;
  129| 
  130| 	/*  Name as choosen by the user:  */
  131| 	char	*name;
  132| 
  133| 	/*  Full "path" to the machine, e.g. "machine[0]":  */
  134| 	char	*path;
  135| 
  136| 	int	machine_type;		/*  MACHINE_PMAX, ..  */
  137| 	int	machine_subtype;	/*  MACHINE_DEC_3MAX_5000, ..  */
  138| 
  139| 	/*  Name set by code in src/machines/machine_*.c:  */
  140| 	const char *machine_name;
  141| 
  142| 	/*  The serial number is mostly used when emulating multiple machines
  143| 	    in a network. nr_of_nics is the current nr of network cards, which
  144| 	    is useful when emulating multiple cards in one machine:  */
  145| 	int	serial_nr;
  146| 	int	nr_of_nics;
  147| 
  148| 	/*  Main memory:  */
  149| 	struct memory *memory;
  150| 
  151| 	int	main_console_handle;
  152| 
  153| 	/*  Tick functions (e.g. hardware devices):  */
  154| 	struct tick_functions tick_functions;
  155| 
  156| 	char	*cpu_name;  /*  TODO: remove this, there could be several
  157| 				cpus with different names in a machine  */
  158| 	int	byte_order_override;
  159| 	int	bootstrap_cpu;
  160| 	int	use_random_bootstrap_cpu;
  161| 	bool	start_paused;
  162| 	int	ncpus;
  163| 	struct cpu **cpus;
  164| 
  165| 	struct diskimage *first_diskimage;
  166| 
  167| 	struct symbol_context symbol_context;
  168| 
  169| 	int	random_mem_contents;
  170| 	uint32_t physical_ram_in_mb;
  171| 	int	memory_offset_in_mb;
  172| 	int	prom_emulation;
  173| 	int	register_dump;
  174| 	int	arch_pagesize;
  175| 
  176| 	int	bootdev_type;
  177| 	int	bootdev_id;
  178| 	char	*bootstr;
  179| 	char	*bootarg;
  180| 
  181| 	/*  Breakpoints:  */
  182| 	struct breakpoints breakpoints;
  183| 
  184| 	/*  #250: data write-watchpoints:  */
  185| 	struct watchpoints watchpoints;
  186| 
  187| 	int	halt_on_nonexistant_memaccess;
  188| 	int	instruction_trace;
  189| 	int	show_nr_of_instructions;
  190| 	int	show_trace_tree;
  191| 	int	emulated_hz;
  192| 	int	allow_instruction_combinations;
  193| 	int	force_netboot;
  194| 	uint64_t file_loaded_end_addr;
  195| 	char	*boot_kernel_filename;
  196| 	char	*boot_string_argument;
  197| 	int	n_gfx_cards;
  198| 
  199| 	/*  Instruction statistics:  */
  200| 	struct statistics statistics;
  201| 
  202| 	/*  X11/framebuffer stuff (per machine):  */
  203| 	struct x11_md x11_md;
  204| 
  205| 	/*  Machine-dependent: (PROM stuff, etc.)  */
  206| 	union {
  207| 		struct machine_arcbios	*arc;
  208| 		struct machine_pmax	*pmax;
  209| 		struct of_data		*of_data;
  210| 	} md;
  211| 
  212| 	/*  Bus-specific interrupt data:  */
  213| 	/*  TODO: Remove!  */
  214| 	struct isa_pic_data isa_pic_data;
  215| };
```

### `src/core/main.c` around the row's cited line 416 (HEAD 2d25df65, lines 371-461)

```c
  371| 			exit(1);
  372| 		case 'h':
  373| 			usage(true);
  374| 			exit(1);
  375| 		case 'I':
  376| 			m->emulated_hz = atoi(optarg);
  377| 			machine_specific_options_used = true;
  378| 			break;
  379| 		case 'i':
  380| 			m->instruction_trace = 1;
  381| 			machine_specific_options_used = true;
  382| 			break;
  383| 		case 'J':
  384| 			m->allow_instruction_combinations = 0;
  385| 			machine_specific_options_used = true;
  386| 			break;
  387| 		case 'j':
  388| 			CHECK_ALLOCATION(m->boot_kernel_filename = strdup(optarg));
  389| 			machine_specific_options_used = true;
  390| 			break;
  391| 		case 'k':
  392| 			{
  393| 				/*  atoi() overflowed int before the old
  394| 				    "< 1" check ran; the value is multiplied
  395| 				    by 1 MB, so bound it by what fits in a
  396| 				    size_t (and 1 TB as a sanity cap).  */
  397| 				long long max_mb =
  398| 				    (long long) (SIZE_MAX / 1048576);
  399| 				if (max_mb > 1048576)
  400| 					max_mb = 1048576;
  401| 				dyntrans_cache_size = (size_t)
  402| 				    parse_int_option('k', optarg, 1, max_mb)
  403| 				    * 1048576;
  404| 			}
  405| 			break;
  406| 		case 'K':
  407| 			debugger_enter_at_end_of_run = true;
  408| 			break;
  409| 		case 'L':
  410| 			CHECK_ALLOCATION(*tap_devname = strdup(optarg));
  411| 			break;
  412| 		case 'M':
  413| 			/*  atoi() let negative/overflowed values through
  414| 			    to the uint32_t field.  */
  415| 			m->physical_ram_in_mb = (uint32_t)
  416| 			    parse_int_option('M', optarg, 1, 1048576);
  417| 			machine_specific_options_used = true;
  418| 			break;
  419| 		case 'N':
  420| 			m->show_nr_of_instructions = 1;
  421| 			machine_specific_options_used = true;
  422| 			break;
  423| 		case 'n':
  424| 			/*  atoi() accepted negative counts, which later
  425| 			    feed malloc()/memset() size calculations.  */
  426| 			m->ncpus = (int)
  427| 			    parse_int_option('n', optarg, 1, 256);
  428| 			machine_specific_options_used = true;
  429| 			break;
  430| 		case 'O':
  431| 			m->force_netboot = 1;
  432| 			machine_specific_options_used = true;
  433| 			break;
  434| 		case 'o':
  435| 			CHECK_ALLOCATION(m->boot_string_argument = strdup(optarg));
  436| 			machine_specific_options_used = true;
  437| 			break;
  438| 		case 'p':
  439| 			machine_add_breakpoint_string(m, optarg);
  440| 			machine_specific_options_used = true;
  441| 			break;
  442| 		case 'Q':
  443| 			m->prom_emulation = 0;
  444| 			machine_specific_options_used = true;
  445| 			break;
  446| 		case 'q':
  447| 			quiet_mode = 1;
  448| 			break;
  449| 		case 'R':
  450| 			m->use_random_bootstrap_cpu = 1;
  451| 			machine_specific_options_used = true;
  452| 			break;
  453| 		case 'r':
  454| 			m->register_dump = 1;
  455| 			machine_specific_options_used = true;
  456| 			break;
  457| 		case 'S':
  458| 			m->random_mem_contents = 1;
  459| 			machine_specific_options_used = true;
  460| 			break;
  461| 		case 's':
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_CATSMEMWRAP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
