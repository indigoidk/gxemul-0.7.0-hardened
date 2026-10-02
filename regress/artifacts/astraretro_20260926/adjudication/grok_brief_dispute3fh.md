# grok seat -- three of YOUR OWN severity rulings, disputed by the confirming seat (retro batches 3f and 3h)

READ-ONLY.  Write nothing, build nothing, run nothing.  The tree under review is
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\src\` at HEAD `db8b1a33` -- ignore any other `src/` you find under the project
root (there are pristine 2021 upstream copies; their line numbers differ by hundreds).

Open your answer with the token `GROK_DISPUTE_3FH_ALIVE_1002` followed, on the same line, by the first line of
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md` quoted verbatim.
The NEXT line is your verdict line, exactly in this form:

`VERDICT: <n> conceded, <m> held, of 3 disputed severities; <k> of 2 adopted amendments objected to`

## What happened

You ruled retro batches 3f, 3g and 3h
(`GXEMUL-SEC\regress\artifacts\astraretro_20260926\adjudication\grok_20261002\grok_rule3{f,g,h}.txt`).  GPT-6 Astra --
the model family that WROTE the findings -- then confirmed your rulings
(`...\adjudication\codex_astraconfirm_3{f,g,h}.txt`): 0 of 24, 0 of 23 and 1 of 26 wrong, with ten amendments.  Its
wording and scope amendments are adopted.  Three amendments RAISE THE SEVERITY of its own findings over your
independent downgrade.  That is a conflict-of-interest shape, so they are not adopted on its say-so: they come back to
you, with its reasons verbatim.

Please do not simply defend your ruling, and do not simply defer.  A ruling in your own favour is the one you are least
likely to test, so be HARDER on your own grade than on Astra's: open the lines, and say which facts decide it.  If a
premise below is wrong, say so -- the premises are stated so that you can check them, not so that you ratify them.

The severity rule, verbatim from your ruling brief: **HIGH** -- guest-controlled input makes the emulator process
terminate, makes one of its memory accesses leave a buffer's bounds, or stops it making progress; **MED** --
guest-visible behaviour differs from the hardware documentation; **LOW** -- diagnostics, latent code, test coverage.

All three disputes turn on the same question, which the rule's letter does not answer: **WHO must control the input?**
Each defect needs a precondition the GUEST does not control alone -- traffic from a network peer, or a size the host
operator chose on the command line.  State, in ONE sentence, the rule you apply to such a precondition, and apply the
same sentence to all three.

## D1 -- `devne2000:F1` `ne2krxbudget`.  You: CONFIRMED-NEW LOW.  Astra: CONFIRMED-NEW HIGH, conditional on sustained ingress.

Astra, verbatim: "`src/devices/dev_ne2000.c:333` rejects invalid rings without setting OVW; its receive loop at :452 has
no budget.  `src/net/net.c:302` polls distributed-network input again on every iteration.  A separately running peer can
replenish input while this guest is paused; the queue-size cap does not bound execution time.  Grok's change from the
draft's conditional HIGH was wrong."

Your own check line: "`src/devices/dev_ne2000.c:333-341` (return, no OVW) and `:452-485` (the enabled `while` stops only
when `net_ethernet_rx_avail` is false or OVW is set; the 16-packet budget is the other branch), plus
`src/net/net.c:293-337`."

Read by the main loop (check it): `src/net/net.c:302-330` -- when `net->local_port != 0` each call does `recvfrom` in a
`do ... while (res != -1 && nreceived < 100)` loop, so every call can take up to 100 fresh packets from the socket.

Questions: (a) the invalid ring is GUEST-configured -- is that right, and which register writes produce it?  (b) with the
ring invalid, does each iteration of the `:452` loop consume one queued packet, and does the loop end as soon as the
peer stops sending?  How fast must a peer send to keep it from ending -- one packet per iteration, or less, given the
100-per-call refill?  (c) is there ANY exit from that loop while input continues (a tick budget, an instruction count,
a return to the dyntrans main loop)?  (d) your grade under your one-sentence rule.

## D2 -- `bundle_net:F1` `taprxquota`.  You: CONFIRMED-NEW LOW.  Astra: CONFIRMED-NEW HIGH, conditional on sustained incoming traffic.

Astra, verbatim: "`src/net/net_tap.c:104` initializes the never-incremented counter; :112 therefore cannot enforce the
budget.  Nonblocking reads at :116 need not return a negative result while incoming traffic continues.  The synchronous
caller, `src/net/net.c:294`, consequently need not return to emulation.  A finite burst returning does not refute the
finding's continuing-input premise.  Grok's downgrade from the draft was wrong."

Read by the main loop (check it): `src/net/net_tap.c:104-135` -- `received_packets_this_tick` is set to 0 at `:104`,
compared with 200 at `:112` and never incremented; the `for (;;)` leaves only at `:118-121` on `read() < 0`; a read of
0 to 19 bytes takes the `continue` at `:128-129`.  There is NO guest precondition here at all: the trigger is traffic on
the host's TAP segment.

Questions: (a) can `read()` on this descriptor return 0 repeatedly (which would spin with no input at all), or is that
excluded for a TAP descriptor in non-blocking mode -- say what you rely on;  (b) what does one iteration cost against the
arrival rate needed to keep the loop from ending -- is "sustained" a flood, or ordinary traffic on a busy segment?
(c) your grade under the SAME one-sentence rule as D1.

## D3 -- `bundle_core:F1` `dyncacheoffset32`.  You: CONFIRMED-NEW LOW.  Astra: CONFIRMED-NEW HIGH, conditional on the oversized configured cache.

Astra, verbatim: "`src/cpus/cpu_dyntrans.c:797-804` narrows the allocation cursor and reconstructs a different page;
`:830-833` publishes instruction pointers from it, and `:114` calls the resulting host function pointer.  The allocation
also contains non-instruction data (`src/cpus/cpu.c:319-324`).  Remaining inside that allocation does not prevent
invalid indirect calls and host termination.  Both draft and grok stopped their impact analysis too early."

Your own check line: "`src/cpus/cpu_dyntrans.c:630` (`uint32_t physpage_ofs`), `:797` (assigned from the cache cursor),
`:804` (used as an index).  A truncated offset aliases inside the allocation, or lands on the 0 'empty' slot.  LOW."

Read by the main loop (check it): `src/core/main.c:401` sets `dyntrans_cache_size` from a command-line option; the
default is `DEFAULT_DYNTRANS_CACHE_SIZE` (`src/core/main.c:67`, `:238`).  So the precondition is the HOST OPERATOR's.

Questions: (a) the smallest configured size at which the `uint32_t` truncates, and whether `main.c`'s option parsing
accepts it (any upper bound there, or at the allocation in `src/cpus/cpu.c:314`);  (b) once truncated, is the consequence
confined to what your ruling says, or can a pointer the dispatch loop CALLS be taken from memory that holds something
other than an instruction-call entry -- Astra's `:830-833` -> `:114` chain: open those lines and say yes or no;  (c) your
grade under the SAME one-sentence rule.

## Two amendments adopted after a check -- object if either is wrong

A1 -- `arcbios:F6`.  You: CONFIRMED-FILED `arcsgiprivate` (the backlog clause at `OUTSTANDING_BUGS.md:2668-2671`).
Astra: CONFIRMED-NEW HIGH `arcsgiprivate`.  Checked at HEAD: that backlog was closed by `#234`-`#244`
(`OUTSTANDING_BUGS.md:2601-2619`); its only arcbios item is `#242` "`arcbios` non-SGI private call / `0x888` /
unimplemented vector" (`:2608-2609`); no row names the SGI default at `src/promemul/arcbios.c:1220-1226`
(`fatal()` then `cpu->running = 0`); and this campaign already ruled on the SAME backlog lines that "a closed item is
not a filing for its residual" (`DISPOSITIONS.md:646-647`).  Adopted: CONFIRMED-NEW HIGH `arcsgiprivate`.

A2 -- `devjazz:F2`.  You: CONFIRMED-NEW LOW `jazzpendingovf`.  Astra: MED, matching `rtcpendovf`
(`DISPOSITIONS.md:385`, "RAISED LOW -> MED": the same unsaturated signed interrupt backlog in `dev_rtc`).  Adopted: MED,
with Astra's qualifier (no claim of portable signed wrapping, no measured deadline).

## Answer format

For each of D1, D2, D3, one line: `D<n> | CONCEDE <grade> | HOLD <grade>` -- then one line naming what you opened
(`path:line`) and what it showed, then your answers to that item's lettered questions.  For A1 and A2:
`A<n> | AGREE` or `A<n> | OBJECT <reason with path:line>`.  Then the one-sentence rule, on its own line, starting `RULE:`.

Mark anything you could not settle by reading as UNSETTLED and name the measurement that would settle it -- an honest
UNSETTLED outranks a confident guess.

Last line: `DENOMINATOR: opened <n> of the <m> cited locations; D1 D2 D3 A1 A2 each answered or marked UNSETTLED`.
